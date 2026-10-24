"""Independent in-memory wire model; never imports hid or uses private ROMs."""
import json
import lzma
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import settings_backup as settings
from ak820_device_protocol import DeviceAPI

p = settings.pack


def base_nvm():
    nvm = bytearray(p.empty_nvm())
    nvm[3] = 1
    nvm[24:32] = bytes((5, 0, 255, 80, 96, 255, 0, 0))
    return nvm


def synthetic_profile():
    """Synthetic trusted image, deliberately not flashable on a real keyboard."""
    native = bytearray(b'S' * 65536)
    native[0x27C0:0x27C4] = bytes.fromhex('aa5533cc')
    payload = bytearray(p.APP_END-p.APP_START)
    payload[:p.CODE_END-p.APP_START] = b'\xA3' * (p.CODE_END-p.APP_START)
    payload[p.NVM_START-p.APP_START:p.NVM_END-p.APP_START] = base_nvm()
    code_hash = p.digest(payload[:p.CODE_END-p.APP_START])
    payload[p.MANIFEST_START-p.APP_START:] = (p.MAGIC + b'\1\0\0\0' + p.BUILD_ID.to_bytes(4, 'little') +
        bytes.fromhex(code_hash) + bytes.fromhex(p.digest(base_nvm()))[:16])
    definition = json.loads((settings.ROOT / 'releases/rc6/reference/vial.json').read_text())
    return {'payload': bytes(payload), 'backup': bytes(native), 'native_backup': bytes(native),
            'definition': definition, 'code': {}, 'ihx_sha256': settings.SUPPORTED_IHX,
            'definition_sha256': p.digest(settings.canonical(definition)), 'schema': p.BUILD_ID,
            'code_sha256': code_hash}


def transition_profiles():
    """Four modeled programs with the same settings contract and NVM schema."""
    old = synthetic_profile()
    middle, new, candidate = dict(old), dict(old), dict(old)
    profiles = [old, middle, new, candidate]
    for index, profile in enumerate(profiles, start=1):
        payload = bytearray(old['payload'])
        payload[:p.CODE_END-p.APP_START] = bytes((0xA3 + index,)) * (p.CODE_END-p.APP_START)
        code_hash = p.digest(payload[:p.CODE_END-p.APP_START])
        at = p.MANIFEST_START-p.APP_START
        payload[at:at+48] = (p.MAGIC + b'\1\0\0\0' + p.BUILD_ID.to_bytes(4, 'little') +
                             bytes.fromhex(code_hash))
        profile['payload'] = bytes(payload)
        profile['ihx_sha256'] = ('f1c4', 'feac', 'd584', '45f2')[index-1] + '0'*60
        profile['code_sha256'] = code_hash
    old['ihx_sha256'] = 'f1c4' + '0'*60
    images = {profile['ihx_sha256']: {'ihx_sha256': profile['ihx_sha256'],
                                      'code_sha256': profile['code_sha256'],
                                      'build_id': p.BUILD_ID}
              for profile in profiles}
    for profile in profiles:
        profile['compatible_images'] = images
    return old, middle, new, candidate


class WireDevice:
    """Models packet layout and firmware publication, independently of host code."""
    mode_ids = {1: 2, 2: 6, 3: 13, 4: 14, 5: 1, 6: 31}

    def __init__(self, profile, nvm=None):
        self.profile = profile
        self.nvm = bytearray(base_nvm() if nvm is None else nvm)
        self.ram_rgb = bytearray(self.nvm[24:32])
        self.compressed = lzma.compress(json.dumps(profile['definition']).encode())
        self.requests, self.writes = [], []
        self.unlocked = True
        self.unlock_active = False
        self.closed = False
        self.fault = None
        self.heartbeat = 0
        self.dev = self
        self.macro_end = 0
        self.rom_patch = {}

    def rom(self):
        rom = bytearray(self.profile['backup'])
        rom[p.APP_START:p.APP_END] = self.profile['payload']
        rom[p.NVM_START:p.NVM_END] = self.nvm
        for at, value in self.rom_patch.items():
            rom[at] = value
        return bytes(rom)

    def get_feature_report(self, report_id, count):
        self.heartbeat += 1
        return b'\0AKBT\1' + bytes((3, self.heartbeat % 256, 1))

    def _macro_chunk(self, offset, data):
        if not self.unlocked:
            raise AssertionError('firmware rejected locked macro upload')
        if offset == 0:
            self.nvm[2032] = 1
            self.macro_end = self.terms = self.operands = 0
            self.opcode_pending = False
        if offset != self.macro_end:
            raise AssertionError('firmware rejected noncontiguous chunk')
        self.nvm[2048+offset:2048+offset+len(data)] = data
        if not self.nvm[2032]:
            self.macro_end += len(data)
            return
        for value in data:
            if self.terms == 16:
                if value:
                    raise AssertionError('firmware rejected nonzero post-terminator data')
            elif self.opcode_pending:
                if not 1 <= value <= 7:
                    raise AssertionError('firmware rejected opcode')
                self.operands = 1 if value <= 3 else 2
                self.opcode_pending = False
            elif self.operands:
                if not value:
                    raise AssertionError('firmware rejected zero operand')
                self.operands -= 1
            elif value == 0:
                self.terms += 1
            elif value == 1:
                self.opcode_pending = True
            elif value >= 128:
                raise AssertionError('firmware rejected non-ASCII text')
        self.macro_end += len(data)
        if self.terms == 16:
            self.nvm[2032] = 0
            self.nvm[2033:2035] = self.macro_end.to_bytes(2, 'little')

    def raw(self, packet):
        self.requests.append(packet)
        cmd, sub = packet[:2]
        reply = bytearray(packet)
        write = cmd in (3, 5, 7, 9, 15) or (cmd, sub) == (254, 4)
        if write:
            self.writes.append(packet)
        if cmd == 254 and sub == 13:
            op, index = packet[2:4]
            at = 0x658 + index*10
            if op == 0:
                reply = bytearray(bytes((0, 8, 0)) + bytes(28) + b'\1')
            elif op == 3:
                raw = self.nvm[at:at+10]
                data = raw[:4] + bytes(4) + raw[8:] if raw[4:8] == b'\x20\x08\1\0' else bytes(10)
                reply[0] = 0
                reply[1:11] = data
            elif op == 4:
                self.writes.append(packet)
                self.nvm[at:at+10] = packet[4:8] + b'\x20\x08\1\0' + packet[12:14]
                reply[0] = 0
        elif cmd == 253 and sub == 0:
            at, count = int.from_bytes(packet[2:4], 'big'), packet[4]
            reply[5:5+count] = self.rom()[at:at+count]
        elif cmd == 253 and sub == 1:
            reply = bytearray(b'\xfd\1\1\xa8' + bytes(28))
            reply[17] = self.unlocked
            reply[18] = self.unlock_active
        elif cmd == 1:
            reply[1:3] = b'\0\x09'
        elif cmd == 254 and sub == 0:
            reply = bytearray((6).to_bytes(4, 'little') + bytes.fromhex(settings.UID) + b'\1' + bytes(19))
        elif cmd == 254 and sub == 1:
            reply[:4] = len(self.compressed).to_bytes(4, 'little')
        elif cmd == 254 and sub == 2:
            at = int.from_bytes(packet[2:6], 'little') * 32
            reply = bytearray(self.compressed[at:at+32].ljust(32, b'\0'))
        elif cmd == 17:
            reply[1] = 6
        elif cmd in (4, 5):
            at = 64 + packet[1]*256 + packet[2]*16 + packet[3]*2
            if cmd == 4:
                reply[4:6] = self.nvm[at:at+2]
            else:
                self.nvm[at:at+2] = packet[4:6]
        elif cmd == 254 and sub in (3, 4):
            at = 1600 + packet[2]*4
            if sub == 3:
                reply[:4] = self.nvm[at+2:at+4] + self.nvm[at:at+2]
            else:
                at += (1-packet[4])*2
                data = packet[5:7]
                self.nvm[at:at+2] = b'\0\0' if data == b'\x7c\0' and not self.unlocked else data
        elif cmd in (2, 3) and sub == 2:
            if cmd == 2:
                reply[2:6] = self.nvm[40].to_bytes(4, 'big')
            else:
                self.nvm[40] = packet[5]
        elif cmd == 12:
            reply[1] = 16
        elif cmd == 13:
            reply[1:3] = b'\x20\0'
        elif cmd == 14:
            at, count = int.from_bytes(packet[1:3], 'big'), packet[3]
            length = int.from_bytes(self.nvm[2033:2035], 'little') if not self.nvm[2032] else 0
            reply[4:4+count] = bytes(self.nvm[2048+i] if i < length else 0 for i in range(at, at+count))
        elif cmd == 15:
            self._macro_chunk(int.from_bytes(packet[1:3], 'big'), packet[4:4+packet[3]])
        elif cmd == 7 and sub == 65:
            mode = int.from_bytes(packet[2:4], 'little')
            if mode:
                internal = {value: key for key, value in self.mode_ids.items()}[mode]
                self.ram_rgb[0] = internal*4+1
            else:
                self.ram_rgb[0] &= 252
            self.ram_rgb[1:5] = bytes((packet[5], packet[6], min(packet[7], 160), packet[4]))
        elif cmd == 9:
            self.ram_rgb[6:8] = b'\0\0'
            self.nvm[24:32] = self.ram_rgb
        elif cmd == 8:
            if sub == 64:
                reply[2:5] = b'\1\0\xa0'
            elif sub == 65:
                mode = self.mode_ids[self.ram_rgb[0] >> 2] if self.ram_rgb[0] & 3 else 0
                reply[2:8] = mode.to_bytes(2, 'little') + bytes((self.ram_rgb[4], *self.ram_rgb[1:4]))
            elif sub == 66:
                after = int.from_bytes(packet[2:4], 'little')
                values = [i for i in (1, 2, 6, 13, 14, 31) if i > after]
                reply[2:] = b''.join(i.to_bytes(2, 'little') for i in values).ljust(30, b'\xff')
            elif sub == 67:
                reply[2:4] = b'R\0'
            elif sub == 68:
                row, col = settings.PHYSICAL[packet[2]]
                reply[2:7] = bytes((0, 0, 4, row, col))
            else:
                raise AssertionError(packet.hex())
        else:
            raise AssertionError('Unexpected wire request: ' + packet.hex())
        if self.fault:
            self.fault(self, packet, reply)
        return bytes(reply)

    def close(self):
        self.closed = True


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = synthetic_profile()
        # Real boot status uses a deliberate200ms delay between heartbeat reads.
        self.sleep = patch('ak820_device_protocol.time.sleep')
        self.sleep.start()
        self.addCleanup(self.sleep.stop)
        self.next_api = 0

    def api(self, nvm=None, writes=False, profile=None):
        self.next_api += 1
        output = self.root / ('run' + str(self.next_api))
        output.mkdir()
        profile = self.profile if profile is None else profile
        raw = WireDevice(profile, nvm)
        api = DeviceAPI(profile, output, lambda: raw, allow_writes=writes)
        self.addCleanup(api.close)
        return api, raw

    def backup(self, nvm=None, name='source'):
        api, raw = self.api(nvm)
        saved = settings.export_settings(api, self.root / name, self.profile)
        self.assertEqual(raw.writes, [])
        return saved

    def changed_nvm(self, stream=None, off=False):
        nvm = base_nvm()
        for layer in range(6):
            for index, key in enumerate(settings.PHYSICAL):
                at = 64+layer*256+key[0]*16+key[1]*2
                nvm[at:at+2] = (4+(index+layer) % 26).to_bytes(2, 'big')
            nvm[1600+layer*4:1604+layer*4] = bytes((0, 0xA9, 0, 0xAA))
        nvm[40] = 173
        nvm[24:32] = bytes((2*4+int(not off), 123, 234, 111, 149, 255, 0, 0))
        if stream is not None:
            nvm[2048:2048+len(stream)] = stream
            nvm[2033:2035] = len(stream).to_bytes(2, 'little')
        return nvm

    def test_readonly_export_roundtrips_all_arrays_and_is_never_overwritten(self):
        saved = self.backup(self.changed_nvm(b'ab\0'*16))
        self.assertEqual(len(saved['settings']['keys']), 498)
        self.assertEqual(len(saved['settings']['encoders']), 12)
        self.assertEqual(len(saved['settings']['macros']['commands']), 16)
        api, raw = self.api()
        with self.assertRaisesRegex(ValueError, 'already exists'):
            settings.export_settings(api, saved['path'], self.profile)
        self.assertEqual(raw.requests, [])
        self.assertEqual((saved['path']/'.gitignore').read_bytes(), b'*\n')

    def test_complete_restore_all_six_layers_encoders_binary_macros_and_off_RGB(self):
        macro = b'\1\1\xe0\1\4\xff\x80\1\5\1\xffx\0'
        source = self.changed_nvm(macro*16, off=True)
        saved = self.backup(source)
        api, raw = self.api(writes=True)
        result = settings.restore_settings(api, saved, self.profile)
        self.assertTrue(result['verified'])
        self.assertEqual(sum(packet[0] == 5 for packet in raw.writes), 498)
        self.assertEqual(sum(packet[:2] == b'\xfe\4' for packet in raw.writes), 12)
        self.assertEqual(raw.nvm[24:32], source[24:32])
        rgb_sets = [packet for packet in raw.writes if packet[0] == 7]
        self.assertEqual([int.from_bytes(packet[2:4], 'little') for packet in rgb_sets], [6, 0])
        self.assertEqual(raw.writes[-1][0], 9)
        self.assertTrue(Path(result['target_backup']).is_dir())

    def test_8192_bytes_and_published_padding_keep_exact_lengths(self):
        for stream in (b'x'*8176+bytes(16), b'y\0'*16+bytes(27)):
            with self.subTest(length=len(stream)):
                saved = self.backup(self.changed_nvm(stream), 'macro'+str(len(stream)))
                api, raw = self.api(writes=True)
                # Avoid redundant498 key writes in this macro-specific test.
                target = self.changed_nvm()
                raw.nvm[:] = target
                raw.ram_rgb[:] = target[24:32]
                settings.restore_settings(api, saved, self.profile)
                self.assertEqual(int.from_bytes(raw.nvm[2033:2035], 'little'), len(stream))
                self.assertEqual(raw.nvm[2048:2048+len(stream)], stream)
                packets = [packet for packet in raw.writes if packet[0] == 15]
                self.assertTrue(all(1 <= packet[3] <= 28 for packet in packets))

    def test_stale_macro_tail_is_evidence_only_and_never_uploaded(self):
        nvm = base_nvm()
        nvm[2048+16:] = b'\xff'*(8192-16)
        saved = self.backup(nvm)
        self.assertEqual(saved['settings']['macros']['data_hex'], '00'*16)
        api, raw = self.api(writes=True)
        settings.restore_settings(api, saved, self.profile)
        self.assertFalse(any(packet[0] == 15 for packet in raw.writes))
        self.assertEqual(raw.nvm[2064:], bytes(8176))

    def test_backup_hash_and_semantic_edits_are_rejected_before_writes(self):
        saved = self.backup()
        folder = saved['path']
        data = json.loads((folder/'settings.json').read_text())
        data['keys'][0]['keycode'] = 4
        encoded = settings.canonical(data)
        (folder/'settings.json').write_bytes(encoded)
        with self.assertRaisesRegex(ValueError, 'hash/size'):
            settings.validate_backup(folder, self.profile)
        manifest = json.loads((folder/'manifest.json').read_text())
        manifest['files']['settings.json'] = settings._record(encoded)
        (folder/'manifest.json').write_bytes(settings.canonical(manifest))
        with self.assertRaisesRegex(ValueError, 'JSON differs'):
            settings.validate_backup(folder, self.profile)
        with self.assertRaisesRegex(ValueError, 'manifest changed'):
            settings.validate_backup(folder, self.profile, saved['identity'])

    def test_unknown_schema_device_and_unsafe_json_paths_are_rejected(self):
        saved = self.backup()
        original = (saved['path']/'manifest.json').read_bytes()
        for change in ({'format': 'new'}, {'nvm_schema': 0x082001}, {'device': dict(settings.DEVICE, pid=1)},
                       {'source_ihx_sha256': '0'*64}, {'files': {'../outside': {}}}):
            with self.subTest(change=change):
                manifest = json.loads(original)
                manifest.update(change)
                (saved['path']/'manifest.json').write_bytes(settings.canonical(manifest))
                with self.assertRaises(ValueError):
                    settings.validate_backup(saved['path'], self.profile)
        (saved['path']/'manifest.json').write_bytes(b'{"format":"a","format":"b"}')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            settings.validate_backup(saved['path'], self.profile)

    def test_unrestorable_fields_block_preflight(self):
        cases = {'direct': (24, 21), 'direct-off': (24, 20), 'flags': (29, 4),
                 'padding': (30, 1), 'default-layer': (3, 2), 'unknown-keycode': (64, 0xFF)}
        for name, (offset, value) in cases.items():
            with self.subTest(case=name):
                nvm = base_nvm()
                nvm[offset] = value
                saved = self.backup(nvm, name)
                with self.assertRaisesRegex(ValueError, 'cannot be restored'):
                    settings.plan_restore(saved, self.profile)
        saved = self.backup(self.changed_nvm(b'z\0'*16+bytes(28)), 'padding28')
        with self.assertRaisesRegex(ValueError, 'padding'):
            settings.plan_restore(saved, self.profile)

    def test_malformed_macro_streams_fail_before_export_publish(self):
        for number, stream in enumerate((b'\1\4\xff\0'+bytes(16), b'\1\xff'+bytes(16),
                                         b'x\0'*15, b'\x80'+bytes(16), bytes(16)+b'x')):
            nvm = base_nvm()
            nvm[2048:2048+len(stream)] = stream
            nvm[2033:2035] = len(stream).to_bytes(2, 'little')
            api, raw = self.api(nvm)
            output = self.root/('bad'+str(number))
            with self.assertRaises(ValueError):
                settings.export_settings(api, output, self.profile)
            self.assertFalse(output.exists())
            self.assertEqual(raw.writes, [])

    def test_unsaved_RGB_and_changing_NVM_stop_readonly_export(self):
        api, raw = self.api()
        raw.ram_rgb[1] = 1
        with self.assertRaisesRegex(ValueError, 'RGB RAM'):
            settings.export_settings(api, self.root/'unsaved', self.profile)
        self.assertEqual(raw.writes, [])
        api, raw = self.api()
        def change(device, packet, reply):
            if packet[0] == 4:
                device.nvm[40] = 1
        raw.fault = change
        with self.assertRaises(ValueError):
            settings.export_settings(api, self.root/'changing', self.profile)
        self.assertEqual(raw.writes, [])

    def test_code_marker_journal_and_storage_faults_stop_before_publication(self):
        for name, at in (('code', p.APP_START), ('helper', p.ERASE_START), ('marker', 0x27C0),
                         ('protected', 0), ('journal', p.NVM_END+64)):
            api, raw = self.api()
            raw.rom_patch[at] = raw.rom()[at] ^ 1
            with self.subTest(name=name), self.assertRaises(ValueError):
                settings.export_settings(api, self.root/name, self.profile)
            self.assertFalse((self.root/name).exists())
        api, raw = self.api()
        raw.fault = lambda _, packet, reply: reply.__setitem__(10, 1) if packet[:2] == b'\xfd\1' else None
        with self.assertRaises(ValueError):
            settings.export_settings(api, self.root/'storage', self.profile)

    def test_failure_on_each_write_class_stops_without_retry_or_followup(self):
        stream = b'macro text\0'*16
        saved = self.backup(self.changed_nvm(stream))
        for command in (5, 254, 3, 15, 7, 9):
            with self.subTest(command=command):
                api, raw = self.api(writes=True)
                def failure(device, packet, reply):
                    if packet[0] == command and packet in device.writes:
                        raise TimeoutError('ACK lost after commit')
                raw.fault = failure
                with self.assertRaises(TimeoutError):
                    settings.restore_settings(api, saved, self.profile)
                self.assertEqual(raw.writes[-1][0], command)
                self.assertEqual(sum(packet[0] == command for packet in raw.writes), 1)
                if command == 15:
                    self.assertEqual(raw.nvm[2032], 1)

    def test_file_change_and_cancel_between_plan_and_first_write(self):
        saved = self.backup(self.changed_nvm())
        api, raw = self.api(writes=True)
        def cancel(stage):
            raise RuntimeError('cancelled')
        with self.assertRaisesRegex(RuntimeError, 'cancelled'):
            settings.restore_settings(api, saved, self.profile, before_write=cancel)
        self.assertEqual(raw.writes, [])
        api, raw = self.api(writes=True)
        # Coherent file change after the initial plan must be caught on next write.
        def change_after_first(device, packet, reply):
            if packet[0] == 5:
                with (saved['path']/'read-log.jsonl').open('ab') as trace:
                    trace.write(b'changed')
        raw.fault = change_after_first
        with self.assertRaisesRegex(ValueError, 'hash/size'):
            settings.restore_settings(api, saved, self.profile)
        self.assertEqual(len(raw.writes), 1)

    def test_locked_or_readonly_target_never_receives_a_setter(self):
        saved = self.backup(self.changed_nvm())
        for writable, unlocked in ((False, True), (True, False)):
            api, raw = self.api(writes=writable)
            raw.unlocked = unlocked
            with self.assertRaises(ValueError):
                settings.restore_settings(api, saved, self.profile)
            self.assertEqual(raw.writes, [])

    def test_successful_ACK_with_corrupt_durable_key_stops_after_one_setter(self):
        saved = self.backup(self.changed_nvm())
        api, raw = self.api(writes=True)
        def corrupt(device, packet, reply):
            if packet[0] == 5:
                at = 64 + packet[1]*256 + packet[2]*16 + packet[3]*2
                device.nvm[at+1] ^= 1
        raw.fault = corrupt
        with self.assertRaisesRegex(ValueError, 'Key readback differs'):
            settings.restore_settings(api, saved, self.profile)
        self.assertEqual(len(raw.writes), 1)

    def test_backup_changed_inside_write_guard_is_rejected_before_setter(self):
        saved = self.backup(self.changed_nvm())
        api, raw = self.api(writes=True)
        def change(stage):
            with (saved['path']/'read-log.jsonl').open('ab') as trace:
                trace.write(b'changed')
        with self.assertRaisesRegex(ValueError, 'hash/size'):
            settings.restore_settings(api, saved, self.profile, before_write=change)
        self.assertEqual(raw.writes, [])

    def test_keycodes_include_protected_boot_but_reject_unknown_features(self):
        for value in (0, 1, 4, 0xA9, 0xE7, 0x0100, 0x0129, 0x5225, 0x770F, 0x7C00, 0x7C7A):
            self.assertTrue(settings.keycode_supported(value), hex(value))
        for value in (True, -1, 65536, 0xFFFF, 0x5226, 0x7710, 0x5700, 0x7E40):
            self.assertFalse(settings.keycode_supported(value), str(value))

    def test_approved_old_backup_restores_to_new_program_and_preserves_provenance(self):
        old, middle, new, candidate = transition_profiles()
        source_nvm = self.changed_nvm()
        api, raw = self.api(source_nvm, profile=old)
        saved = settings.export_settings(api, self.root/'old-source', old)
        self.assertEqual(saved['source_identity'], (old['ihx_sha256'], old['code_sha256']))
        self.assertEqual(saved['manifest']['source_ihx_sha256'], old['ihx_sha256'])
        self.assertEqual(saved['manifest']['code_sha256'], old['code_sha256'])

        api, raw = self.api(writes=True, profile=candidate)
        result = settings.restore_settings(api, saved, candidate)
        self.assertTrue(result['verified'])
        self.assertEqual(settings._rom_identity(raw.rom(), candidate)['ihx_sha256'], candidate['ihx_sha256'])
        self.assertEqual(raw.nvm, source_nvm)

    def test_four_profile_transition_matrix_all_sixteen_pairs(self):
        profiles = transition_profiles()
        for source_rank, source in enumerate(profiles):
            source_api, _ = self.api(self.changed_nvm(), profile=source)
            saved = settings.export_settings(source_api, self.root/f'matrix-source-{source_rank}', source)
            for target_rank, target in enumerate(profiles):
                with self.subTest(source=source_rank, target=target_rank):
                    if source_rank <= target_rank:
                        self.assertIsInstance(settings.plan_restore(saved, target), dict)
                    else:
                        with self.assertRaisesRegex(ValueError, 'downgrade'):
                            settings.plan_restore(saved, target)

    def test_candidate_backup_cannot_be_restored_to_legacy_profile(self):
        old, middle, new, candidate = transition_profiles()
        api, _ = self.api(self.changed_nvm(), profile=candidate)
        saved = settings.export_settings(api, self.root/'candidate-source', candidate)
        self.assertEqual(saved['source_identity'], (candidate['ihx_sha256'], candidate['code_sha256']))
        with self.assertRaisesRegex(ValueError, 'downgrade'):
            settings.plan_restore(saved, old)

    def test_candidate_restore_rejects_legacy_target_snapshot_before_setters(self):
        old, middle, new, candidate = transition_profiles()
        source_api, _ = self.api(self.changed_nvm(), profile=old)
        saved = settings.export_settings(source_api, self.root/'legacy-source', old)
        target_api, raw = self.api(self.changed_nvm(), writes=True, profile=old)
        with self.assertRaisesRegex(ValueError, 'Target firmware differs'):
            settings.restore_settings(target_api, saved, candidate)
        self.assertEqual(raw.writes, [])

    def test_compatible_code_with_forged_manifest_identity_is_rejected(self):
        old, middle, new, candidate = transition_profiles()
        api, _ = self.api(profile=old)
        saved = settings.export_settings(api, self.root/'forged', old)
        manifest_path = saved['path']/'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['source_ihx_sha256'] = new['ihx_sha256']
        manifest['files']['before-full-rom.bin'] = settings._record(saved['rom'])
        manifest_path.write_bytes(settings.canonical(manifest))
        with self.assertRaisesRegex(ValueError, 'Unsupported backup firmware'):
            settings.validate_backup(saved['path'], candidate)

    def test_image_with_wrong_embedded_manifest_header_is_rejected(self):
        old, middle, new, candidate = transition_profiles()
        api, _ = self.api(profile=old)
        saved = settings.export_settings(api, self.root/'bad-header', old)
        rom = bytearray(saved['rom'])
        rom[p.MANIFEST_START] ^= 1
        rom_path = saved['path']/'before-full-rom.bin'
        rom_path.write_bytes(rom)
        manifest_path = saved['path']/'manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['files']['before-full-rom.bin'] = settings._record(bytes(rom))
        manifest_path.write_bytes(settings.canonical(manifest))
        with self.assertRaisesRegex(ValueError, 'Application manifest'):
            settings.validate_backup(saved['path'], candidate)

    def test_running_old_compatible_image_is_not_accepted_as_final_candidate(self):
        old, middle, new, candidate = transition_profiles()
        api, _ = self.api(profile=old)
        saved = settings.export_settings(api, self.root/'old-final', old)
        with self.assertRaisesRegex(ValueError, 'Final running firmware'):
            settings.verify_restore(api, saved, candidate)


class FullFeatureTests(unittest.TestCase):
    setUp = SettingsTests.setUp
    api = SettingsTests.api

    def full(self):
        old, _, _, full = transition_profiles()
        full['compatible_images'][full['ihx_sha256']]['features'] = sorted(settings.FULL_FEATURES)
        full['compatible_images'][full['ihx_sha256']]['combos_version'] = 1
        return old, full

    def test_exact_optional_keycode_domain(self):
        for code in (0x7011, 0x7012, 0x7013, 0x7C1A, 0x7C1B, 0x7C1E):
            self.assertFalse(settings.keycode_supported(code))
            self.assertTrue(settings.keycode_supported(code, features=settings.FULL_FEATURES))
        for code in (0x7010, 0x7014, 0x7C18, 0x7C19, 0x7C1C, 0x7C1D, 0x5280, 0x7C5A):
            self.assertFalse(settings.keycode_supported(code, features=settings.FULL_FEATURES))
        with self.assertRaisesRegex(ValueError, 'Unknown settings feature'):
            settings.keycode_supported(4, features=['future'])

    def test_full_matrix_encoder_assignments_roundtrip(self):
        _, full = self.full()
        nvm = base_nvm()
        codes = (0x52A2, 0x7011, 0x7012, 0x7013, 0x7C1A, 0x7C1B, 0x7C1E)
        for index, code in enumerate(codes):
            at = DeviceAPI.key_offset(0, settings.PHYSICAL[index])
            nvm[at:at+2] = code.to_bytes(2, 'big')
        for direction, code in enumerate((0x7013, 0x7C1E)):
            at = DeviceAPI.encoder_offset(0, direction)
            nvm[at:at+2] = code.to_bytes(2, 'big')
        api, _ = self.api(nvm, profile=full)
        saved = settings.export_settings(api, self.root/'full', full)
        target, raw = self.api(writes=True, profile=full)
        settings.restore_settings(target, saved, full)
        for index, code in enumerate(codes):
            self.assertEqual(target.get_key(0, settings.PHYSICAL[index]), code)
        self.assertEqual(target.get_encoder(0, 0), 0x7013)
        self.assertEqual(target.get_encoder(0, 1), 0x7C1E)

    def test_alpha2_backup_can_move_to_full(self):
        old, full = self.full()
        old['compatible_images'][old['ihx_sha256']]['combos_version'] = 1
        api, _ = self.api(profile=old)
        saved = settings.export_settings(api, self.root/'alpha2-full', old)
        self.assertEqual(settings.plan_restore(saved, full)['combo_entries'], [bytes(10).hex()]*8)
        full['compatible_images'][full['ihx_sha256']]['features'] = ['future']
        with self.assertRaisesRegex(ValueError, 'Unknown settings feature'):
            settings.plan_restore(saved, full)


class ComboTests(unittest.TestCase):
    setUp = SettingsTests.setUp
    api = SettingsTests.api
    def candidate(self):
        old, middle, new, candidate = transition_profiles()
        candidate['compatible_images'][candidate['ihx_sha256']]['combos_version'] = 1
        return old, candidate

    def test_combo_nonempty_roundtrip_and_explicit_clear(self):
        _, candidate = self.candidate()
        data = bytes.fromhex('04000500000000000600')
        source = base_nvm()
        source[0x658:0x662] = DeviceAPI.stored_combo(data)
        api, _ = self.api(source, profile=candidate)
        backup = settings.export_settings(api, self.root/'combo', candidate)
        target, raw = self.api(writes=True, profile=candidate)
        settings.restore_settings(target, backup, candidate)
        self.assertEqual(target.get_combo(0), data)
        empty, _ = self.api(profile=candidate)
        clear = settings.export_settings(empty, self.root/'clear', candidate)
        settings.restore_settings(target, clear, candidate)
        self.assertEqual(raw.nvm[0x658:0x662], DeviceAPI.stored_combo(bytes(10)))

    def test_legacy_does_not_clear_candidate(self):
        old, candidate = self.candidate()
        api, _ = self.api(profile=old)
        backup = settings.export_settings(api, self.root/'legacy-combo', old)
        self.assertNotIn('combos', backup['settings'])
        self.assertIsNone(settings.plan_restore(backup, candidate)['combo_entries'])
        nvm = base_nvm()
        nvm[0x658:0x662] = DeviceAPI.stored_combo(bytes.fromhex('04000500000000000600'))
        with self.assertRaisesRegex(ValueError, 'must not be cleared'):
            settings.plan_restore(backup, candidate, nvm)

    def test_invalid_marker_and_values_fail(self):
        _, candidate = self.candidate()
        for data in (bytes.fromhex('04000500200802000600'), bytes.fromhex('04000400200801000600')):
            nvm = base_nvm()
            nvm[0x658:0x662] = data
            with self.assertRaises(ValueError):
                settings.settings_from_nvm(nvm, settings.rgb_wire(nvm[24:32]), combos=True)

    def test_restore_combo_failures_stop_at_first_entry(self):
        _, candidate = self.candidate()
        source = base_nvm()
        data = bytes.fromhex('04000500000000000600')
        source[0x658:0x66C] = DeviceAPI.stored_combo(data)*2
        source_api, _ = self.api(source, profile=candidate)
        backup = settings.export_settings(source_api, self.root/'two-combos', candidate)
        for failure in ('timeout', 'ack', 'getter', 'storage', 'neighbor'):
            api, raw = self.api(writes=True, profile=candidate)
            terminal = []
            def fault(device, packet, reply):
                if packet[:3] == bytes((254, 13, 4)):
                    if failure == 'timeout':
                        terminal.append(packet)
                        raise TimeoutError('model timeout')
                    if failure == 'ack':
                        reply[0] = 255
                        terminal.append(packet)
                    if failure == 'getter':
                        device.nvm[0x658] = 7
                    if failure == 'neighbor':
                        device.nvm[0x700] ^= 1
                if device.writes:
                    if failure == 'storage' and packet[:2] == bytes((253, 1)):
                        reply[4] = 1
                        terminal.append(packet)
                    elif failure == 'getter' and packet[:3] == bytes((254, 13, 3)):
                        terminal.append(packet)
                    elif failure == 'neighbor':
                        # Full durable NVM read ends with a clean status packet.
                        if packet[:2] == bytes((253, 1)):
                            terminal.append(packet)
            raw.fault = fault
            with self.subTest(failure=failure):
                with self.assertRaises((ValueError, TimeoutError)):
                    settings.restore_settings(api, backup, candidate)
                self.assertEqual(len(raw.writes), 1)
                self.assertEqual(raw.writes[0][3], 0)
                self.assertTrue(terminal)
                self.assertEqual(raw.requests[-1], terminal[-1])

    def test_combo_fault_stops_without_retry(self):
        _, candidate = self.candidate()
        api, raw = self.api(writes=True, profile=candidate)
        def fault(device, packet, reply):
            if packet[:3] == bytes((254, 13, 4)):
                device.nvm[0x700] ^= 1
        raw.fault = fault
        with self.assertRaisesRegex(ValueError, 'neighboring bytes'):
            api.set_combo(0, bytes.fromhex('04000500000000000600'))
        self.assertEqual(len(raw.writes), 1)


if __name__ == '__main__':
    unittest.main()
