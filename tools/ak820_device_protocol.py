"""Restricted VIA/Vial adapter. Importing this module never imports HID."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import re
import sys
import time
import lzma

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'qmk-8051-ak820/util'))
import pack_ak820 as pack
import ak820_diagnose as diag
import ak820_tool as transport


def require(ok, message):
    if not ok:
        raise ValueError(message)


def bind(release: Path, session: Path, approval: Path):
    """Validate reviewed release and personal recovery inputs before opening HID."""
    spec = importlib.util.spec_from_file_location('ak820_test_installer', ROOT / 'tools/installer/ak820.py')
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    installer.BUNDLE, installer.APPROVAL = release, approval
    manifest = json.loads((release / 'installer-release.json').read_text(encoding='utf-8'))
    installer.RELEASE = manifest['release']
    installer.load_release(approved=True)
    images, payload, backup = transport.session_image(session, 'permanent')
    pack.validate_native(backup)
    for key, name in (('ihx_sha256', 'firmware/application.ihx'), ('map_sha256', 'firmware/application.map')):
        require(images.get(key) == pack.digest((release / name).read_bytes()), 'Personal image belongs to a different build')
    code = diag.diagnostic_build(release / 'firmware/application.ihx', release / 'firmware/application.map',
                                 release / 'reports/build-report.json')
    # The manifest binds CODE, while the personal payload binds its own NVM.
    require(all(payload[a-pack.APP_START] == v for a, v in code.items()
                if pack.APP_START <= a < pack.CODE_END), 'Personal payload CODE differs from release')
    return {'release': manifest['release'], 'release_dir': str(release.resolve()),
            'session': str(session.resolve()), 'payload_sha256': pack.digest(payload),
            'backup_sha256': pack.digest(backup), 'payload': payload, 'backup': backup,
            'code': code, 'definition': json.loads((release / 'reference/vial.json').read_text(encoding='utf-8'))}


class DeviceAPI:
    def __init__(self, binding, output, app_factory=None):
        self.binding, self.output = binding, output
        self.trace = (output / 'transport.jsonl').open('a', encoding='utf-8')
        self.app = None
        try:
            if app_factory is not None:
                self.app = app_factory()
            else:
                selected = transport.select_application()
                require((selected.get('vendor_id'), selected.get('product_id'), selected.get('usage_page'), selected.get('usage'))
                        == (0x320F, 0x505B, 0xFF60, 0x61), 'Expected exactly one Vial application')
                self.app = transport.Application(selected)
        except Exception:
            self.trace.close()
            raise
        self.baseline = None
        self.pending = None

    def close(self):
        try:
            if self.app is not None:
                self.app.close()
        finally:
            self.trace.close()

    def packet(self, *values):
        return bytes(values) + bytes(32-len(values))

    def exchange(self, packet):
        # Allowlist only the getters and two benign mapping setters used below.
        require(packet[0] in (1, 4, 5, 7, 8, 12, 13, 14, 17, 253, 254), 'Forbidden command')
        if packet[0] == 7:
            require(packet[1] == 0x41, 'Forbidden RGB command')
        if packet[0] == 254:
            require(packet[1] in (0, 1, 2, 3, 4), 'Forbidden Vial command')
        row = {'request_hex': packet.hex()}
        try:
            reply = bytes(self.app.raw(packet))
            row['reply_hex'] = reply.hex()
            require(len(reply) == 32, 'Short protocol response')
            return reply
        except Exception as exc:
            row['error'] = repr(exc)
            raise
        finally:
            self.trace.write(json.dumps(row)+'\n'); self.trace.flush()

    def read_code(self, address, size):
        data = bytearray()
        for delta in range(0, size, 27):
            at, count = address+delta, min(27, size-delta)
            request = self.packet(253, 0, at >> 8, at & 255, count)
            reply = self.exchange(request)
            require(reply[:5] == request[:5], 'FD00 response mismatch')
            data.extend(reply[5:5+count])
        return bytes(data)

    def boot_liveness(self):
        previous = None
        samples = []
        try:
            deadline = time.monotonic()+5
            while time.monotonic() < deadline:
                row = {'get_feature_report': [0, 9]}
                try:
                    raw = bytes(self.app.dev.get_feature_report(0, 9))
                    row['reply_hex'] = raw.hex()
                except Exception as exc:
                    row['error'] = repr(exc)
                    raise
                finally:
                    self.trace.write(json.dumps(row)+'\n'); self.trace.flush()
                require(len(raw) == 9 and raw[:6] == b'\0AKBT\1', 'Invalid boot feature')
                stage, heartbeat, flags = raw[6:]
                require(stage in (1, 2, 3) and not flags & 252, 'Unknown boot feature fields')
                samples.append(list(raw))
                if stage == 3 and flags == 1:
                    if previous is not None and previous != heartbeat:
                        return
                    previous = heartbeat
                else:
                    previous = None
                time.sleep(.2)
            raise TimeoutError('Main loop liveness not observed; stop without reset')
        finally:
            (self.output / 'boot-status.json').write_text(json.dumps(samples), encoding='utf-8')

    def initialize(self):
        self.boot_liveness()
        rom = self.read_code(0, 65536)
        (self.output / 'before-rom.bin').write_bytes(rom)
        require(all(rom[a] == v for a, v in self.binding['code'].items()), 'Live diagnostic CODE differs')
        transport.verify_live(rom, self.binding['payload'], 'permanent', self.binding['backup'])
        self.baseline = rom[pack.NVM_START:pack.NVM_END]
        (self.output / 'baseline-nvm.bin').write_bytes(self.baseline)
        require(self.read_nvm() == self.baseline, 'NVM unstable or stale')
        self.status()

    def status(self):
        status = diag.decode_status(self.exchange(self.packet(253, 1)))
        require(not status['storage_failed'] and not status['page_dirty'] and status['batch_depth'] == 0
                and not status['vial_unlock_in_progress'], 'Storage failure, busy storage or unlock in progress')
        return status

    def read_nvm(self):
        region = self.read_code(pack.NVM_START, pack.MANIFEST_START-pack.NVM_START)
        (self.output / 'current-nvm-journal.bin').write_bytes(region)
        require(not any(region[pack.NVM_END-pack.NVM_START+64:]), 'Dirty journal header')
        nvm = region[:pack.NVM_END-pack.NVM_START]
        pack.validate_nvm(nvm)
        require(self.read_code(pack.NVM_START, len(nvm)) == nvm, 'Unstable NVM')
        self.status()
        return nvm

    def definition(self):
        require(self.exchange(self.packet(1))[1:3] == b'\0\x09', 'VIA version mismatch')
        ident = self.exchange(self.packet(254, 0))
        require(ident[:4] == (6).to_bytes(4, 'little') and ident[4:12] == bytes.fromhex('0470ff9001b915d3') and ident[12] == 1,
                'Vial identity/version/RGB mismatch')
        size = int.from_bytes(self.exchange(self.packet(254, 1))[:4], 'little')
        require(0 < size <= 65504, 'Definition size invalid')
        compressed = b''.join(self.exchange(self.packet(254, 2, p & 255, p >> 8, 0, 0))
                              for p in range((size+31)//32))[:size]
        definition = json.loads(lzma.decompress(compressed))
        require(definition == self.binding['definition'], 'Live definition differs from release')
        matrix, rotations = [], []
        for row in definition['layouts']['keymap']:
            for key in row:
                if isinstance(key, str):
                    coordinate = key.split('\n')[0]
                    if re.fullmatch(r'\d+,\d+', coordinate):
                        pair = tuple(map(int, coordinate.split(',')))
                        if '\ne' in key: rotations.append(pair)
                        else: matrix.append(pair)
        require(len(matrix) == len(set(matrix)) == 83 and len(rotations) == 2, 'Definition key/rotation count mismatch')
        require(self.exchange(self.packet(17))[1] == 6, 'Layer count mismatch')
        return matrix

    @staticmethod
    def key_offset(layer, key):
        return pack.KEYMAP_ADDR+layer*256+key[0]*16+key[1]*2

    @staticmethod
    def encoder_offset(layer, direction):
        # Wire direction 0=CCW, 1=CW; persistent order is CW, CCW.
        return pack.ENCODER_ADDR+layer*4+(1-direction)*2

    def get_key(self, layer, key):
        reply = self.exchange(self.packet(4, layer, *key))
        require(reply[:4] == bytes((4, layer, *key)), 'Key getter header mismatch')
        return int.from_bytes(reply[4:6], 'big')

    def get_encoder(self, layer, direction):
        reply = self.exchange(self.packet(254, 3, layer, 0))
        return int.from_bytes(reply[direction*2:direction*2+2], 'big')

    def set_key(self, layer, key, value):
        packet = self.packet(5, layer, *key, value >> 8, value & 255)
        return self.exchange(packet) == packet

    def set_encoder(self, layer, direction, value):
        packet = self.packet(254, 4, layer, 0, direction, value >> 8, value & 255)
        return self.exchange(packet) == packet

    def macros(self):
        require(self.exchange(self.packet(12))[1] == 16, 'Macro count mismatch')
        require(int.from_bytes(self.exchange(self.packet(13))[1:3], 'big') == 8192, 'Macro size mismatch')
        data = bytearray()
        for offset in range(0, 8192, 28):
            count = min(28, 8192-offset)
            packet = self.packet(14, offset >> 8, offset & 255, count)
            reply = self.exchange(packet)
            require(reply[:4] == packet[:4], 'Macro getter header mismatch')
            data.extend(reply[4:4+count])
        return bytes(data)

    @staticmethod
    def macro_view(nvm):
        """Protocol hides stale tail after the published logical upload length.

        dynamic_keymap_macro_get_buffer uses ak820_macro_length(), not the
        physical allocation size. Busy or invalid metadata is a hard failure.
        """
        metadata = pack.validate_nvm(nvm)
        start = metadata['macro_addr']
        length = metadata['published_macro_length']
        return nvm[start:start+length] + bytes(metadata['macro_size']-length)

    def rgb_mode(self):
        reply = self.exchange(self.packet(8, 0x41))
        require(reply[:2] == b'\x08\x41', 'RGB mode response mismatch')
        return reply[2:8]

    def set_rgb_mode(self, mode):
        require(len(mode) == 6, 'RGB mode requires six bytes')
        packet = self.packet(7, 0x41, *mode)
        return self.exchange(packet) == packet

    def rgb(self):
        def query(command, *args):
            reply = self.exchange(self.packet(8, command, *args))
            require(reply[:2] == bytes((8, command)), 'RGB getter header mismatch')
            return reply[2:]
        info = query(0x40)
        require(int.from_bytes(info[:2], 'little') == 1, 'VialRGB version mismatch')
        require(int.from_bytes(query(0x43)[:2], 'little') == 82, 'RGB LED count mismatch')
        effects, previous = [], 0
        while True:
            result = query(0x42, previous & 255, previous >> 8)
            values = [int.from_bytes(result[i:i+2], 'little') for i in range(0, 30, 2)]
            values = [v for v in values if v != 65535]
            if not values: break
            require(all(v > previous for v in values) and values == sorted(set(values)), 'Invalid RGB effect page')
            effects.extend(values); previous = values[-1]
            require(len(effects) <= 256, 'RGB effect list too long')
        require(effects, 'RGB effect list empty')
        leds = [list(query(0x44, i, 0)[:5]) for i in range(82)]
        require(all(led[2] == 4 and 0 <= led[3] < 16 and 0 <= led[4] < 8 for led in leds), 'Invalid LED metadata')
        require(len({tuple(led[3:5]) for led in leds}) == 82, 'Duplicate LED matrix positions')
        mode = query(0x41)[:6]
        require(int.from_bytes(mode[:2], 'little') in [0]+effects, 'RGB mode unsupported')
        # Hue/saturation/value/speed have a stable persistent representation.
        nvm = self.read_nvm()
        require(mode[5] <= info[2], 'RGB brightness outside firmware limit')
        return {'effects': effects, 'leds': leds, 'mode_hex': mode.hex(), 'info_hex': info[:3].hex(),
                'saved_rgb_config_hex': nvm[24:32].hex(),
                'RAM_matches_saved_hsv_speed': mode[2:] == bytes((nvm[28], nvm[25], nvm[26], nvm[27]))}
