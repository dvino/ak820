"""Offline v3 codec and pending-qualification safety checks; not image evidence."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'qmk-8051-ak820' / 'util'))
sys.path.insert(0, str(ROOT / 'tools'))
import ak820_extension_settings as codec
from ak820_device_protocol import DeviceAPI


class LeaderV3(unittest.TestCase):
    def test_custom_default_migration_preserves_v2(self):
        original = codec.decode_settings(codec.settings_record(version=2))
        migrated = codec.decode_settings(codec.settings_record(original, version=2), version=3, default_leader=517)
        self.assertEqual(migrated['23'], 517)
        self.assertEqual({k: v for k, v in migrated.items() if k != '23'}, original)
        self.assertEqual(codec.decode_settings(codec.settings_record(migrated, version=3)), migrated)

    def test_invalid_default_and_corrupt_record_rejected(self):
        for default in (None, 0, 1001, True):
            with self.subTest(default=default), self.assertRaises(ValueError):
                codec.decode_settings(bytes(24), version=3, default_leader=default)
        raw = bytearray(codec.settings_record(version=3, default_leader=517))
        raw[21] ^= 1
        with self.assertRaises(ValueError):
            codec.decode_settings(bytes(raw), version=3, default_leader=517)

    def test_v3_getter_reads_leader_and_rejects_invalid_reply(self):
        api = DeviceAPI.__new__(DeviceAPI)
        api.binding = {'settings_record_version': 3}
        api.exchange = lambda packet: b'\0' + (517).to_bytes(2, 'little') + bytes(29)
        self.assertEqual(api.get_setting(23), 517)
        api.exchange = lambda packet: bytes(32)
        with self.assertRaises(ValueError):
            api.get_setting(23)

    def test_raw_v2_getter_rejects_v3_only_qsid(self):
        api = DeviceAPI.__new__(DeviceAPI)
        api.binding = {'settings_record_version': 2}
        api._require_extension_schema = lambda: None
        with self.assertRaisesRegex(ValueError, 'Unknown settings ID'):
            api._validate_request(api.packet(254, 10, 23, 0))

    def test_untrusted_downgrade_binding_cannot_reach_transport(self):
        for binding in ({}, {'settings_record_version': 2},
                        {'ihx_sha256': 'claimed', 'compatible_images': {
                            'claimed': {'settings_record_version': 2}}}):
            with tempfile.TemporaryDirectory() as tmp:
                app = Mock()
                api = DeviceAPI(binding, Path(tmp), lambda: app, allow_writes=True)
                try:
                    for packet in (api.packet(9), api.packet(5, 0, 0, 0, 0, 4),
                                   api.packet(7, 0x41), api.packet(7, 0x43, 1, 82, 1, 0, 0, 0, 0, 0)):
                        with self.subTest(binding=binding, packet=packet), self.assertRaisesRegex(ValueError, 'Approved release'):
                            api.exchange(packet)
                    app.raw.assert_not_called()
                finally:
                    api.close()


if __name__ == '__main__':
    unittest.main()
