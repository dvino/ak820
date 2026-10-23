"""Offline independent wire fixture; never loads HID or opens the keyboard."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest import mock
import lzma

sys.path.insert(0, str(Path(__file__).parent))
import ak820_device_tests as runner
import ak820_device_protocol as protocol

class RawFixture:
    """Independent raw responder: getters decode persistent bytearray state."""
    def __init__(self, fault=None):
        self.nvm = bytearray(protocol.pack.empty_nvm())
        self.requests, self.setters, self.fault = [], 0, fault
        self.closed = False
        self.definition = json.loads((runner.ROOT/'releases/rc6/reference/vial.json').read_text())
        self.compressed = lzma.compress(json.dumps(self.definition).encode())
        self.ram_override = None
        self.rgb_mode = b'\2\0\x10\x20\x30\x40'

    def raw(self, packet):
        self.requests.append(packet)
        reply = bytearray(packet)
        cmd = packet[0]
        if cmd == 253 and packet[1] == 0:
            address = int.from_bytes(packet[2:4], 'big')
            rom = bytearray(65536)
            rom[0xC700:0xEF00] = self.nvm
            reply[5:5+packet[4]] = rom[address:address+packet[4]]
        elif cmd == 253:
            reply = bytearray(bytes((253, 1, 1, 168))+bytes(28))
            if self.fault == 'storage': reply[4] = 1
        elif cmd == 4:
            offset = 64+packet[1]*256+packet[2]*16+packet[3]*2
            reply[4:6] = self.nvm[offset:offset+2] if self.ram_override is None else self.ram_override
        elif cmd == 254 and packet[1] == 3:
            offset = 1600+packet[2]*4
            reply[:4] = self.nvm[offset+2:offset+4]+self.nvm[offset:offset+2]
        elif cmd in (5, 254) and (cmd == 5 or packet[1] == 4):
            self.setters += 1
            if cmd == 5:
                offset, data = 64+packet[1]*256+packet[2]*16+packet[3]*2, packet[4:6]
            else:
                offset, data = 1600+packet[2]*4+(1-packet[4])*2, packet[5:7]
            if self.fault == 'no_persist': self.ram_override = data
            elif self.fault != 'restore' or self.setters == 1: self.nvm[offset:offset+2] = data
            if self.fault == 'neighbor': self.nvm[offset+3] ^= 1
            if self.fault == 'missing_ack': raise TimeoutError('committed then ACK lost')
        elif cmd == 1: reply[1:3] = b'\0\x09'
        elif cmd == 254 and packet[1] == 0:
            reply = bytearray((6).to_bytes(4,'little')+bytes.fromhex('0470ff9001b915d3')+b'\1'+bytes(19))
        elif cmd == 254 and packet[1] == 1: reply[:4] = len(self.compressed).to_bytes(4,'little')
        elif cmd == 254 and packet[1] == 2:
            start = int.from_bytes(packet[2:6], 'little')*32
            reply = bytearray(self.compressed[start:start+32].ljust(32,b'\0'))
        elif cmd == 17: reply[1] = 6
        elif cmd == 12: reply[1] = 16
        elif cmd == 13: reply[1:3] = b'\x20\0'
        elif cmd == 14:
            offset = int.from_bytes(packet[1:3], 'big')
            length = int.from_bytes(self.nvm[2033:2035], 'little')
            ready = self.nvm[2032] == 0 and 16 <= length <= 8192
            for index in range(packet[3]):
                at = offset+index
                reply[4+index] = self.nvm[2048+at] if ready and at < length else 0
        elif cmd == 7:
            self.rgb_mode = packet[2:8]
        elif cmd == 8:
            sub = packet[1]
            if sub == 64: reply[2:5] = b'\1\0\xff'
            elif sub == 67: reply[2:4] = b'\x52\0'
            elif sub == 66:
                reply[2:] = b'\xff'*30
                if packet[2:4] == b'\0\0': reply[2:6] = b'\1\0\2\0'
            elif sub == 68: reply[2:7] = bytes((packet[2], 0, 4, packet[2]//8, packet[2]%8))
            elif sub == 65: reply[2:8] = self.rgb_mode
            else: raise AssertionError('Unknown RGB getter')
        else: raise AssertionError('Unexpected fixture command '+packet.hex())
        return bytes(reply)

    def close(self): self.closed = True

class DeviceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)

    def api(self, fault=None):
        raw = RawFixture(fault)
        api = protocol.DeviceAPI({'definition': raw.definition}, self.output, lambda: raw,
                                 allow_writes=True)
        self.addCleanup(api.close)
        return api, raw

    def report(self): return dict(checks=[], restore_pending=None)

    def test_default_does_not_import_transport_or_hid(self):
        with mock.patch.dict(sys.modules, {'hid': None}), mock.patch('builtins.__import__', wraps=__import__) as imports:
            with contextlib.redirect_stdout(io.StringIO()): self.assertEqual(runner.main([]), 0)
        self.assertNotIn('ak820_device_protocol', [call.args[0] for call in imports.call_args_list])

    def test_definition_and_all_getters_decode_independent_wire(self):
        api, raw = self.api()
        matrix = api.definition()
        self.assertEqual(len(matrix), 83)
        for layer in range(6):
            for key in matrix:
                self.assertEqual(api.get_key(layer, key), int.from_bytes(raw.nvm[64+layer*256+key[0]*16+key[1]*2:66+layer*256+key[0]*16+key[1]*2], 'big'))
        self.assertEqual(api.macros(), bytes(raw.nvm[2048:10240]))

    def test_locked_normal_remaps_and_all_encoder_slots_restore(self):
        api, raw = self.api()
        before = bytes(raw.nvm)
        report = self.report()
        report['rgb'] = {'effects':[1,2]}
        runner.check_reversible_settings(api, report, [(0,0)])
        self.assertEqual(raw.setters, 36)
        self.assertEqual(bytes(raw.nvm), before)
        self.assertIsNone(report['restore_pending'])
        self.assertEqual(report['checks'][-2]['status'], 'SKIP')
        self.assertEqual(sum(x['name'].startswith('encoder_') for x in report['checks']), 12)
        setters = [p for p in raw.requests if p[:2] == b'\xfe\x04']
        self.assertEqual(setters[0], bytes.fromhex('fe040000000000')+bytes(25))
        self.assertEqual(setters[1], bytes.fromhex('fe040000000001')+bytes(25))
        self.assertEqual(setters[2], bytes.fromhex('fe040000010000')+bytes(25))

    def test_faults_stop_before_blind_restore(self):
        for fault, error in [('missing_ack', TimeoutError), ('neighbor', runner.SafetyStop),
                             ('no_persist', runner.SafetyStop), ('restore', runner.SafetyStop)]:
            with self.subTest(fault=fault):
                api, raw = self.api(fault)
                report = self.report()
                with self.assertRaises(error):
                    runner.roundtrip(api, report, 'key', 64, lambda v: api.set_key(0,(0,0),v), lambda:api.get_key(0,(0,0)))
                self.assertEqual(raw.setters, 2 if fault == 'restore' else 1)
                self.assertIsNotNone(report['restore_pending'])

    def test_storage_fault_stops_before_setter(self):
        api, raw = self.api('storage')
        with self.assertRaises(ValueError):
            runner.roundtrip(api, self.report(), 'key',64,lambda v:api.set_key(0,(0,0),v),lambda:api.get_key(0,(0,0)))
        self.assertEqual(raw.setters,0)

    def test_RGB_protocol_all_leds_and_unsaved_RAM_state(self):
        api, raw = self.api()
        result = api.rgb()
        self.assertEqual(result['effects'], [1,2])
        self.assertEqual(len(result['leds']),82)
        self.assertFalse(result['RAM_matches_saved_hsv_speed'])
        self.assertEqual(raw.setters,0)

    def test_readonly_complete_suite_and_preexisting_fault(self):
        api, raw = self.api()
        api.initialize = lambda: None  # ROM/boot separately verified; no fake firmware image.
        report = self.report()
        self.assertEqual(len(runner.check_readonly(api,report)),83)
        self.assertEqual([r['status'] for r in report['checks']],['PASS']*3)

    def test_definition_mismatch_rejected(self):
        api, raw = self.api()
        api.binding['definition'] = {}
        with self.assertRaisesRegex(ValueError,'differs'): api.definition()

    def test_short_macro_protocol_view_hides_stale_durable_tail(self):
        api, raw = self.api()
        raw.nvm[2048:2066] = b'A\0B'+bytes(15)
        raw.nvm[2033:2035] = (18).to_bytes(2,'little')
        raw.nvm[2066:10240] = b'\x7f'*(10240-2066)
        expected = b'A\0B'+bytes(15)+bytes(8192-18)
        self.assertEqual(api.macros(), expected)
        self.assertEqual(api.macro_view(bytes(raw.nvm)), expected)
        self.assertNotEqual(expected,bytes(raw.nvm[2048:10240]))
        api.initialize = lambda:None
        runner.check_readonly(api,self.report())

    def test_macro_busy_and_invalid_length_fail_closed(self):
        api, raw = self.api()
        for busy, length in ((1,16),(0,15),(0,8193)):
            image = bytearray(raw.nvm)
            image[2032] = busy
            image[2033:2035] = length.to_bytes(2,'little')
            with self.subTest(busy=busy,length=length), self.assertRaises(ValueError):
                api.macro_view(bytes(image))
        raw.nvm[2032] = 1
        raw.nvm[2048:10240] = b'\x7f'*8192
        self.assertEqual(api.macros(), bytes(8192))

    def test_build_or_approval_failure_precedes_device_open(self):
        for message in ('bad approval', 'IHX/MAP mismatch', 'wrong recovery backup'):
            output = self.output/message.replace(' ','-').replace('/','-')
            with mock.patch.object(protocol,'bind',side_effect=ValueError(message)), mock.patch.object(protocol,'DeviceAPI') as opened, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(runner.main(['--run','--release-dir','unused','--session','unused','--output',str(output)]),2)
            opened.assert_not_called()

    def test_real_bind_rejects_mixed_session_build_and_payload_CODE(self):
        release = self.output/'release'; release.mkdir()
        (release/'firmware').mkdir()
        (release/'installer-release.json').write_text(json.dumps({'release':'fixture'}))
        for suffix in ('ihx','map'):
            (release/f'firmware/application.{suffix}').write_bytes(suffix.encode())
        images = {'ihx_sha256':protocol.pack.digest(b'ihx'), 'map_sha256':protocol.pack.digest(b'map')}
        spec = types.SimpleNamespace(loader=types.SimpleNamespace(exec_module=lambda module:setattr(module,'load_release',lambda **kwargs:None)))
        for failure in ('ihx_sha256','map_sha256','CODE'):
            selected = dict(images)
            if failure != 'CODE': selected[failure] = 'wrong'
            with mock.patch.object(protocol.importlib.util,'spec_from_file_location',return_value=spec), \
                 mock.patch.object(protocol.importlib.util,'module_from_spec',return_value=types.SimpleNamespace()), \
                 mock.patch.object(protocol.transport,'session_image',return_value=(selected,b'\0',bytes(65536))), \
                 mock.patch.object(protocol.pack,'validate_native'), \
                 mock.patch.object(protocol.diag,'diagnostic_build',return_value={protocol.pack.APP_START:1}), \
                 mock.patch.object(protocol.transport,'select_application') as opened:
                with self.subTest(failure=failure), self.assertRaisesRegex(ValueError,'different build|CODE differs'):
                    protocol.bind(release,self.output/'session',self.output/'approval')
                opened.assert_not_called()

    def test_real_bind_missing_approval_stops_before_session_or_open(self):
        with mock.patch.object(protocol.transport,'session_image') as session, mock.patch.object(protocol.transport,'select_application') as opened:
            with self.assertRaisesRegex(ValueError, 'approval is missing'):
                protocol.bind(runner.ROOT/'releases/rc6',self.output/'missing',self.output/'no-approval.json')
        session.assert_not_called(); opened.assert_not_called()

    def test_RGB_RAM_bad_readback_stops_without_restore(self):
        api, raw = self.api()
        original = raw.raw
        def mismatch(packet):
            reply = bytearray(original(packet))
            if packet[:2] == b'\x08\x41' and any(p[0] == 7 for p in raw.requests): reply[4] ^= 1
            return bytes(reply)
        raw.raw = mismatch
        report = self.report(); report['rgb'] = {'effects':[1,2]}
        with self.assertRaisesRegex(runner.SafetyStop,'changed getter'):
            runner.rgb_roundtrip(api,report)
        self.assertEqual(sum(p[0] == 7 for p in raw.requests),1)
        self.assertIsNotNone(report['restore_pending'])

    def test_stale_getter_stops_before_setter(self):
        api, raw = self.api()
        raw.ram_override = b'\x12\x34'
        with self.assertRaisesRegex(runner.SafetyStop, 'stale'):
            runner.roundtrip(api,self.report(),'key',64,lambda v:api.set_key(0,(0,0),v),lambda:api.get_key(0,(0,0)))
        self.assertEqual(raw.setters,0)

    def test_malformed_status_and_bad_macro_RGB_metadata(self):
        for kind in ('status','macro','rgb'):
            api, raw = self.api()
            original = raw.raw
            def corrupt(packet, kind=kind):
                reply = bytearray(original(packet))
                if kind == 'status' and packet[:2] == b'\xfd\1': reply[2] = 0
                if kind == 'macro' and packet[0] == 13: reply[1] = 0
                if kind == 'rgb' and packet[:2] == b'\x08\x44': reply[5] = 255
                return bytes(reply)
            raw.raw = corrupt
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                {'status':api.status, 'macro':api.macros, 'rgb':api.rgb}[kind]()

    def test_RGB_RAM_roundtrip_preserves_original_unsaved_state_and_NVM(self):
        api, raw = self.api()
        before, original = bytes(raw.nvm), raw.rgb_mode
        report = self.report(); report['rgb'] = {'effects':[1,2]}
        runner.rgb_roundtrip(api,report)
        self.assertEqual(raw.rgb_mode,original)
        self.assertEqual(bytes(raw.nvm),before)
        self.assertIsNone(report['restore_pending'])
        setters = [p for p in raw.requests if p[0] == 7]
        self.assertEqual(setters[0], bytes.fromhex('0741000011213140')[:7]+bytes((0,))+bytes(24))

    def test_cli_timeout_saved_as_failure(self):
        output = self.output/'run'
        with mock.patch.object(protocol,'bind',side_effect=TimeoutError('fixture')), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(['--run','--release-dir','unused','--session','unused','--output',str(output)]),2)
        report = json.loads((output/'report.json').read_text())
        self.assertIn('TimeoutError', report['error'])
        self.assertFalse(report['usb_opened'])
        self.assertTrue((output/'transport.jsonl').is_file())

    def test_consent_mismatch_stops_before_binding_or_open(self):
        with mock.patch.object(protocol,'bind') as bind, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(['--run','--allow-settings-write','--output',str(self.output/'denied')]),2)
        bind.assert_not_called()

if __name__ == '__main__': unittest.main()
