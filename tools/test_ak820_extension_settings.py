"""Offline schema03 codec and migration regression tests."""
import json
import struct
import sys
from pathlib import Path
import unittest
import tempfile
from unittest.mock import Mock, patch
import ak820_device_protocol as protocol
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'qmk-8051-ak820/util'))
import ak820_extension_settings as e
import pack_ak820 as p

class Extensions(unittest.TestCase):
    def test_settings_crc_and_reserved(self):
        raw = e.settings_record()
        self.assertEqual(e.decode_settings(raw)['7'], 200)
        self.assertEqual(e.decode_settings(bytes(24)), e.decode_settings(raw))
        for i in range(24):
            bad = bytearray(raw); bad[i] ^= 1
            with self.assertRaises(ValueError): e.decode_settings(bytes(bad))

    def test_entries(self):
        for kind in ('tap_dance','key_overrides'):
            self.assertEqual(e.slot_offset(kind, 6) % 64, 0)
        e.validate_entry('tap_dance', struct.pack('<5H', 4, 0x104, 0, 0, 32767))
        for raw in (struct.pack('<5H', 1,0,0,0,0), struct.pack('<5H',4,0,0,0,32768)):
            with self.assertRaises(ValueError): e.validate_entry('tap_dance', raw)
        e.validate_entry('key_overrides', struct.pack('<HHHBBBB',4,5,63,1,0,0,1))
        with self.assertRaises(ValueError): e.validate_entry('key_overrides', struct.pack('<HHHBBBB',4,5,63,1,0,0,65))

    def test_migration_preserves_combos_and_legacy(self):
        nvm = p.empty_nvm()
        nvm[0x658:0x662] = bytes.fromhex('04000500200801000600')
        migrated,_ = p.migrate_vial_nvm(nvm,p.BUILD_ID,target_build_id=e.SCHEMA)
        self.assertEqual(migrated[:37],nvm[:37])
        self.assertEqual(migrated[40:0x6A8],nvm[40:0x6A8])
        self.assertEqual(migrated[0x7F0:],nvm[0x7F0:])
        self.assertEqual(p.migrate_vial_nvm(nvm,p.BUILD_ID)[0],nvm)
        with self.assertRaises(ValueError): p.migrate_vial_nvm(migrated,e.SCHEMA)
        value=e.from_nvm(migrated)
        self.assertEqual(e.loads(json.dumps(value)),value)
        with self.assertRaises(ValueError): e.loads('{"version":1,"version":1}')
        del value['qmk_settings']['1']
        with self.assertRaises(ValueError): e.validate_json(value)

class ProtocolFailure(unittest.TestCase):
    def test_extension_readback_failure_stops_without_retry(self):
        nvm,_ = p.migrate_vial_nvm(p.empty_nvm(),p.BUILD_ID,target_build_id=e.SCHEMA)
        payload = bytearray(p.APP_END-p.APP_START)
        payload[p.NVM_START-p.APP_START:p.NVM_END-p.APP_START] = nvm
        raw = Mock()
        raw.raw.side_effect = lambda packet: b'\0' + packet[1:]
        with tempfile.TemporaryDirectory() as directory:
            api = protocol.DeviceAPI({'payload': bytes(payload)}, Path(directory), lambda: raw, allow_writes=True)
            try:
                api.read_nvm = Mock(return_value=nvm)
                api.status = Mock()
                api.get_extension = Mock(return_value=bytes(10))
                with self.assertRaisesRegex(ValueError, 'readback differs'):
                    api.set_extension('tap_dance',0,struct.pack('<5H',4,0,0,0,0))
                self.assertEqual(raw.raw.call_count,1)
                self.assertEqual(api.read_nvm.call_count,1)
            finally:
                api.close()

    def test_blank_settings_noop_preserves_raw_record(self):
        nvm,_=p.migrate_vial_nvm(p.empty_nvm(),p.BUILD_ID,target_build_id=e.SCHEMA)
        for blank in (bytes(24),b'\xff'*24):
            before=bytearray(nvm);before[0x6A8:0x6C0]=blank;before=bytes(before)
            payload=bytearray(p.APP_END-p.APP_START)
            payload[p.NVM_START-p.APP_START:p.NVM_END-p.APP_START]=before
            with tempfile.TemporaryDirectory() as directory:
                raw=Mock()
                api=protocol.DeviceAPI({'payload':bytes(payload)},Path(directory),lambda:raw,allow_writes=True)
                try:
                    api.read_nvm=Mock(return_value=before)
                    api.get_setting=Mock(side_effect=lambda qsid:e.FIELDS[qsid][4])
                    api.settings_query=Mock(return_value=[1,2,7,18,19])
                    self.assertTrue(api.set_setting(2,40))
                    self.assertTrue(api.reset_settings())
                    raw.raw.assert_not_called()
                finally:api.close()

    def test_widths_rejected_before_transport(self):
        with tempfile.TemporaryDirectory() as directory:
            raw=Mock()
            api=protocol.DeviceAPI({},Path(directory),lambda:raw,allow_writes=True)
            try:
                for qsid,value in ((1,16),(2,0),(7,1001),(18,101),(4,True)):
                    with self.assertRaises(ValueError): api.set_setting(qsid,value)
                raw.raw.assert_not_called()
            finally: api.close()

if __name__ == '__main__': unittest.main()
