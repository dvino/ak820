#!/usr/bin/env python3
"""Lossless rc1-3 migration and Entropy's 8192-byte wire contract; offline only."""
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'util'))
import pack_ak820 as packer
import ak820_diagnose as diagnostic


def legacy_nvm(stream=b'hello\0' + bytes(15), *, padding=0):
    data = bytearray(10240)
    data[:2] = bytes.fromhex('e6fe')
    data[3] = 1
    data[24:32] = bytes((5, 12, 120, 90, 88, 255, 0, 0))
    data[37:40] = bytes.fromhex('012008')
    for index in range(256):
        struct.pack_into('>H', data, 0x40 + 2 * index, index + 4)
    data[0x240:0x248] = bytes.fromhex('00a900aa00bb00bc')
    data[0x2f1:0x2f3] = (len(stream) + padding).to_bytes(2, 'little')
    data[0x300:0x300 + len(stream)] = stream
    return bytes(data)


class EntropySchemaTest(unittest.TestCase):
    def test_migration_preserves_both_keymaps_encoders_lighting_and_macro_bytes(self):
        source = legacy_nvm(b'hello\0' + b'\x01\x05\x01\xff\0' + bytes(14))
        original = bytes(source)
        migrated, report = packer.migrate_vial_nvm(source, 0x082001)
        self.assertEqual(source, original)
        self.assertEqual(len(migrated), 10240)
        self.assertEqual(migrated[:37], source[:37])
        self.assertEqual(migrated[0x40:0x240], source[0x40:0x240])
        self.assertEqual(migrated[0x640:0x648], source[0x240:0x248])
        self.assertEqual(migrated[0x240:0x640], b'\x00\x01' * 512)
        self.assertEqual(migrated[0x648:0x658], b'\x00\x01' * 8)
        self.assertEqual(migrated[0x800:0x800+25], source[0x300:0x300+25])
        self.assertEqual(migrated[37:40], bytes.fromhex('022008'))
        self.assertEqual(migrated[0x7f0:0x7f3], b'\0\x19\0')
        self.assertEqual(report['preserved_layers'], 2)
        self.assertEqual(report['layers'], 6)
        self.assertEqual(report['macro_bytes'], 8192)
        packer.validate_nvm(migrated)

    def test_exact_capacity_fits_and_one_more_byte_fails(self):
        for size in (8192, 8193, 9472):
            source = legacy_nvm(b'A' * (size - 16) + bytes(16))
            before = bytes(source)
            if size == 8192:
                migrated, _ = packer.migrate_vial_nvm(source, 0x082001)
                self.assertEqual(migrated[0x800:], source[0x300:0x300+8192])
            else:
                with self.assertRaisesRegex(ValueError, 'Nothing was truncated or written'):
                    packer.migrate_vial_nvm(source, 0x082001)
            self.assertEqual(source, before)

    def test_only_zero_padding_after_sixteenth_macro_can_be_discarded(self):
        source = legacy_nvm(b'A' + bytes(16), padding=9000)
        migrated, report = packer.migrate_vial_nvm(source, 0x082001)
        self.assertEqual(report['preserved_macro_stream_bytes'], 17)
        self.assertEqual(report['discarded_zero_padding_bytes'], 9000)
        self.assertEqual(migrated[0x7f1:0x7f3], b'\x11\0')
        broken = bytearray(source)
        broken[0x300 + 8193] = 1
        with self.assertRaisesRegex(ValueError, 'Nonzero data'):
            packer.migrate_vial_nvm(broken, 0x082001)

    def test_invalid_or_unpublished_data_never_migrates(self):
        for address, value in ((0, 0), (37, 0), (0x2f0, 1), (0x2f1, 0), (0x2f2, 255)):
            broken = bytearray(legacy_nvm())
            broken[address] = value
            with self.subTest(address=address), self.assertRaises(ValueError):
                packer.migrate_vial_nvm(broken, 0x082001)
        for stream in (b'\x01\0' + bytes(16), b'\x01\x04\0\x01' + bytes(16),
                       b'\x80' + bytes(16), b'\x01\x08\x01' + bytes(16), b'A' + bytes(15)):
            with self.subTest(stream=stream), self.assertRaises(ValueError):
                packer.migrate_vial_nvm(legacy_nvm(stream), 0x082001)
        with self.assertRaisesRegex(ValueError, 'Unknown NVM schema'):
            packer.migrate_vial_nvm(legacy_nvm(), 0x082000)

    def test_current_schema_is_copied_byte_exactly(self):
        current, _ = packer.migrate_vial_nvm(legacy_nvm(), 0x082001)
        changed = bytearray(current)
        changed[0x580:0x582] = b'\x52\x25'
        changed[0x900] = 0xA5  # Inactive physical tail must stay hidden and intact.
        result, report = packer.migrate_vial_nvm(changed, 0x082002)
        self.assertEqual(result, changed)
        self.assertEqual(report['mode'], 'byte_exact_nvm_copy')

    def test_diagnostic_uses_the_dump_schema_for_layer_bounds(self):
        self.assertEqual(diagnostic.key_address(5, 15, 7), 0xCD3E)
        with self.assertRaises(ValueError):
            diagnostic.key_address(2, 0, 0, build_id=0x082001)
        rom = bytearray(65536)
        rom[0xc700:0xef00] = legacy_nvm()
        self.assertEqual(diagnostic.analyze(rom, key=(1, 0, 0))['key']['keycode'], 132)


if __name__ == '__main__':
    unittest.main()
