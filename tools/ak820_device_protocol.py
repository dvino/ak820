"""Restricted VIA/Vial adapter. Importing this module never imports HID."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import re
import sys
import time
import lzma

ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[1]))
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
    def __init__(self, binding, output, app_factory=None, *, allow_writes=False):
        self.binding, self.output = binding, output
        require(type(allow_writes) is bool, 'allow_writes must be an explicit boolean')
        self.allow_writes = allow_writes
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
        self._validate_request(packet)
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

    def _validate_request(self, packet):
        """Accept only fixed, typed VIA/Vial requests used by this adapter."""
        require(isinstance(packet, bytes) and len(packet) == 32, 'Protocol request must be exactly 32 bytes')
        command, sub = packet[0], packet[1]
        zero_tail = lambda start: packet[start:] == bytes(32-start)
        write = False
        if command == 1:
            require(zero_tail(1), 'Malformed protocol-version request')
        elif command == 2:
            require(sub == 2 and zero_tail(2), 'Unknown or malformed keyboard-value request')
        elif command == 3:
            write = True
            require(sub == 2 and packet[2:5] == bytes(3) and zero_tail(6),
                    'Unknown or malformed keyboard-value setter')
        elif command == 4:
            require(packet[1] < 6 and packet[2] < 16 and packet[3] < 6 and zero_tail(4), 'Malformed key getter')
        elif command == 5:
            write = True
            require(packet[1] < 6 and packet[2] < 16 and packet[3] < 6 and zero_tail(6), 'Malformed key setter')
        elif command == 7:
            write = True
            require(sub == 0x41 and zero_tail(8), 'Unknown or malformed RGB setter')
        elif command == 8:
            require(sub in (0x40, 0x41, 0x42, 0x43, 0x44), 'Unknown VialRGB getter')
            if sub in (0x40, 0x41, 0x43): require(zero_tail(2), 'Malformed VialRGB getter')
            elif sub == 0x42: require(zero_tail(4), 'Malformed VialRGB effect query')
            else: require(packet[2] < 82 and packet[3] == 0 and zero_tail(4), 'Malformed VialRGB LED query')
        elif command == 9:
            write = True
            require(zero_tail(1), 'Malformed RGB save request')
        elif command in (12, 13):
            require(zero_tail(1), 'Malformed macro metadata getter')
        elif command == 14:
            offset, count = int.from_bytes(packet[1:3], 'big'), packet[3]
            require(1 <= count <= 28 and offset <= 8192-count and zero_tail(4), 'Malformed macro getter')
        elif command == 15:
            write = True
            offset, count = int.from_bytes(packet[1:3], 'big'), packet[3]
            require(1 <= count <= 28 and offset <= 8192-count and zero_tail(4+count), 'Malformed macro upload chunk')
        elif command == 17:
            require(zero_tail(1), 'Malformed layer-count getter')
        elif command == 253:
            require(sub in (0, 1), 'Unknown FD diagnostic command')
            if sub == 0:
                address, count = int.from_bytes(packet[2:4], 'big'), packet[4]
                require(1 <= count <= 27 and address <= 65536-count and zero_tail(5), 'Malformed FD00 read')
            else: require(zero_tail(2), 'Malformed FD01 status request')
        elif command == 254:
            require(sub in (0, 1, 2, 3, 4, 13), 'Unknown FE Vial command')
            if sub in (0, 1): require(zero_tail(2), 'Malformed Vial metadata request')
            elif sub == 2: require(packet[4:6] == bytes(2) and zero_tail(6), 'Malformed Vial definition page request')
            elif sub == 3: require(packet[2] < 6 and packet[3] == 0 and zero_tail(4), 'Malformed encoder getter')
            elif sub == 13:
                require(packet[2] in (0, 3, 4), 'Unknown Combo operation')
                if packet[2] == 0:
                    require(zero_tail(3), 'Malformed Combo count request')
                else:
                    require(packet[3] < 8, 'Invalid Combo index')
                    if packet[2] == 3:
                        require(zero_tail(4), 'Malformed Combo getter')
                    else:
                        write = True
                        self.validate_combo(packet[4:14])
                        require(zero_tail(14), 'Malformed Combo setter')
            else:
                write = True
                require(packet[2] < 6 and packet[3] == 0 and packet[4] in (0, 1) and zero_tail(7), 'Malformed encoder setter')
        else:
            raise ValueError('Forbidden command')
        if write:
            require(self.allow_writes, 'Writes are disabled for this DeviceAPI instance')

    def _require_writes(self):
        require(self.allow_writes, 'Writes are disabled for this DeviceAPI instance')

    def read_code(self, address, size):
        require(0 <= address <= 65536 and 0 <= size <= 65536 and address <= 65536-size,
                'Invalid CODE read range')
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
        require(status['first_failure_stage'] == 0 and not status['storage_failed'] and not status['page_dirty'] and status['batch_depth'] == 0
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
        require(0 <= layer < 6 and len(key) == 2 and 0 <= key[0] < 16 and 0 <= key[1] < 6,
                'Invalid key getter arguments')
        reply = self.exchange(self.packet(4, layer, *key))
        require(reply[:4] == bytes((4, layer, *key)), 'Key getter header mismatch')
        return int.from_bytes(reply[4:6], 'big')

    def get_encoder(self, layer, direction):
        require(0 <= layer < 6 and direction in (0, 1), 'Invalid encoder getter arguments')
        reply = self.exchange(self.packet(254, 3, layer, 0))
        return int.from_bytes(reply[direction*2:direction*2+2], 'big')

    def set_key(self, layer, key, value):
        self._require_writes()
        require(0 <= layer < 6 and len(key) == 2 and 0 <= key[0] < 16 and 0 <= key[1] < 6
                and 0 <= value <= 0xFFFF, 'Invalid key setter arguments')
        packet = self.packet(5, layer, *key, value >> 8, value & 255)
        return self.exchange(packet) == packet

    def set_encoder(self, layer, direction, value):
        self._require_writes()
        require(0 <= layer < 6 and direction in (0, 1) and 0 <= value <= 0xFFFF, 'Invalid encoder setter arguments')
        packet = self.packet(254, 4, layer, 0, direction, value >> 8, value & 255)
        return self.exchange(packet) == packet

    COMBO_OFFSET = 0x658
    COMBO_MARKER = b'\x20\x08\x01\x00'

    @staticmethod
    def validate_combo(data):
        require(isinstance(data, bytes) and len(data) == 10, 'Combo requires ten bytes')
        a, b, c, d, output = (int.from_bytes(data[i:i+2], 'little') for i in range(0, 10, 2))
        require(c == d == 0, 'Unsupported Combo format/version')
        valid = (a == b == output == 0) or (4 <= a <= 0xA4 and 4 <= b <= 0xA4 and a != b
                and output < 0x2000 and (4 <= (output & 255) <= 0xA4 or 0xE0 <= (output & 255) <= 0xE7))
        require(valid, 'Unsupported Combo keys/output')
        return data

    @classmethod
    def stored_combo(cls, data):
        data = cls.validate_combo(data)
        return data[:4] + cls.COMBO_MARKER + data[8:]

    def combo_count(self):
        reply = self.exchange(self.packet(254, 13, 0))
        require(reply == bytes((0, 8, 0)) + bytes(28) + b'\x01', 'Combo capabilities differ')
        return 8

    def get_combo(self, index):
        require(type(index) is int and 0 <= index < 8, 'Invalid Combo index')
        packet = self.packet(254, 13, 3, index)
        reply = self.exchange(packet)
        require(reply[0] == 0 and reply[11:] == packet[11:], 'Combo getter ACK mismatch')
        return self.validate_combo(reply[1:11])

    def set_combo(self, index, data):
        self._require_writes()
        require(type(index) is int and 0 <= index < 8, 'Invalid Combo index')
        data = self.validate_combo(data)
        before = self.read_nvm()
        packet = self.packet(254, 13, 4, index, *data)
        require(self.exchange(packet) == b'\0' + packet[1:], 'Combo setter ACK mismatch')
        self.status()
        require(self.get_combo(index) == data, 'Combo getter readback differs')
        expected = bytearray(before)
        offset = self.COMBO_OFFSET + 10*index
        expected[offset:offset+10] = self.stored_combo(data)
        require(self.read_nvm() == bytes(expected), 'Combo durable settings or neighboring bytes differ')
        return True

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

    def get_macro_buffer(self, offset, count):
        """Read a published logical macro range through VIA 0x0E.

        The firmware intentionally hides in-progress upload data from this
        getter. During an upload, verify physical bytes with read_code() at
        pack.NVM_START + pack.MACRO_ADDR + offset instead.
        """
        require(0 <= offset <= 8192 and 0 <= count <= 28 and offset <= 8192-count,
                'Invalid macro read range')
        if count == 0:
            return b''
        packet = self.packet(14, offset >> 8, offset & 255, count)
        reply = self.exchange(packet)
        require(reply[:4] == packet[:4], 'Macro getter header mismatch')
        return reply[4:4+count]

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
        self._require_writes()
        require(isinstance(mode, (bytes, bytearray)) and len(mode) == 6, 'RGB mode requires six bytes')
        packet = self.packet(7, 0x41, *mode)
        return self.exchange(packet) == packet

    def get_layout_options(self):
        reply = self.exchange(self.packet(2, 2))
        require(reply[:2] == b'\x02\x02', 'Layout options response mismatch')
        require(reply[2:5] == bytes(3), 'Layout options exceed the persisted one-byte field')
        return int.from_bytes(reply[2:6], 'big')

    def set_layout_options(self, value):
        self._require_writes()
        require(0 <= value <= 0xFF, 'Layout options must fit the persisted one-byte field')
        packet = self.packet(3, 2, value >> 24, (value >> 16) & 255, (value >> 8) & 255, value & 255)
        return self.exchange(packet) == packet

    def upload_macro_chunk(self, offset, data):
        """Upload one existing VIA macro chunk; caller must satisfy Vial unlock."""
        self._require_writes()
        require(isinstance(data, (bytes, bytearray)) and 1 <= len(data) <= 28
                and 0 <= offset <= 8192-len(data), 'Invalid macro upload chunk')
        packet = self.packet(15, offset >> 8, offset & 255, len(data), *data)
        return self.exchange(packet) == packet

    def save_rgb(self):
        """Persist current VialRGB values through VIA lighting-save command."""
        self._require_writes()
        packet = self.packet(9)
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
