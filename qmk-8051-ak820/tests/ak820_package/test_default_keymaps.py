"""Exact factory keymap decoding; no firmware build or physical operations."""
import struct
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'util'))
import ak820_default_keymap as defaults
import pack_ak820 as packer


class DefaultKeymapsTest(unittest.TestCase):
    def fixture(self, words=None):
        # Exercise implicit NO/TRNS and one/two-byte payloads within 255 bytes.
        words = words or ([0, 1, 2, 255, 256, 0xffff, 0, 1] * 16 + [0, 1] * 64)
        raw = struct.pack('<256H', *words)
        classes, payload, offsets = defaults.encode(list(raw), [16, 8, 2, 2, 0, 1])
        symbols = {'_ak820_default_classes': 0x4000,
                   '_ak820_default_payload': 0x4100, '_ak820_default_offsets': 0x4200}
        data = {}
        for name, values in (('classes', classes), ('payload', payload), ('offsets', offsets)):
            data.update(enumerate(values, symbols['_ak820_default_' + name]))
        return data, symbols, raw

    def test_compressed_defaults_recover_exact_little_endian_words(self):
        data, symbols, raw = self.fixture()
        self.assertEqual(packer.factory_keymaps(data, symbols), raw)

    def test_payload_free_tables_are_valid(self):
        data, symbols, raw = self.fixture([0, 1] * 128)
        self.assertEqual(packer.factory_keymaps(data, symbols), raw)

    def test_raw_defaults_are_exact_and_cannot_mix_with_compressed_tables(self):
        raw = struct.pack('<256H', *range(256))
        symbols = {'_keymaps': 0x4000}
        data = dict(enumerate(raw, 0x4000))
        self.assertEqual(packer.factory_keymaps(data, symbols), raw)
        for name in ('classes', 'payload', 'offsets'):
            with self.assertRaisesRegex(ValueError, 'Ambiguous'):
                packer.factory_keymaps(data, {**symbols, '_ak820_default_' + name: 0x4200})
        del data[0x4000 + 511]
        with self.assertRaisesRegex(ValueError, 'Missing compiled constant'):
            packer.factory_keymaps(data, symbols)

    def test_incomplete_or_overlapping_tables_and_changed_offsets_fail(self):
        data, symbols, _ = self.fixture()
        for name in symbols:
            partial = dict(symbols)
            del partial[name]
            with self.assertRaisesRegex(ValueError, 'Missing compressed'):
                packer.factory_keymaps(data, partial)
        for name in symbols:
            truncated = dict(data)
            del truncated[symbols[name]]
            with self.assertRaisesRegex(ValueError, 'Missing compiled constant'):
                packer.factory_keymaps(truncated, symbols)
        changed = dict(data)
        changed[symbols['_ak820_default_offsets'] + 1] += 1
        with self.assertRaisesRegex(ValueError, 'Non-contiguous'):
            packer.factory_keymaps(changed, symbols)
        data, symbols, _ = self.fixture([0] * 256)
        # Zero-filled tables make overlap otherwise invisible to the decoder.
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            packer.factory_keymaps(data, {**symbols, '_ak820_default_offsets': 0x4000})

    def test_noncanonical_payload_values_fail(self):
        data, symbols, _ = self.fixture()
        for low, high, position in ((1, None, 0), (1, 0, 2)):
            changed = dict(data)
            payload = symbols['_ak820_default_payload']
            changed[payload + position] = low
            if high is not None:
                changed[payload + position + 1] = high
            with self.assertRaisesRegex(ValueError, 'Non-canonical'):
                packer.factory_keymaps(changed, symbols)

    def test_payload_length_cannot_wrap_byte_offsets(self):
        symbols = {'_ak820_default_classes': 0x4000,
                   '_ak820_default_payload': 0x4100, '_ak820_default_offsets': 0x4300}
        data = dict(enumerate([0xaa] * 64, 0x4000))
        data.update(enumerate([2] * 256, 0x4100))
        data.update(enumerate(range(0, 256, 8), 0x4300))
        with self.assertRaisesRegex(ValueError, 'exceeds byte offsets'):
            packer.factory_keymaps(data, symbols)

    def test_startup_accepts_reserved_staging_layout_and_retains_exact_crt_check(self):
        from startup_fixture import add_startup_fixture
        data, symbols = {}, {}
        add_startup_fixture(data, symbols)
        for start in (0x400, 0x440):
            layout = {**symbols, 's_XSEG': start, 'l_XSEG': 0xa00 - start}
            packer.validate_startup(data, layout)
        for layout in ({**symbols, 's_XSEG': 0x420, 'l_XSEG': 0x5e0},
                       {**symbols, 's_XSEG': 0x440},
                       {**symbols, 'l_PSEG': 1}):
            with self.assertRaisesRegex(ValueError, 'startup XRAM/PSEG'):
                packer.validate_startup(data, layout)
        data[symbols['__mcs51_genXINIT']] ^= 1
        with self.assertRaisesRegex(ValueError, 'Unsupported XINIT'):
            packer.validate_startup(data, {**symbols, 's_XSEG': 0x440, 'l_XSEG': 0x5c0})

    def test_generator_exports_exact_three_tables_for_map_only_packaging(self):
        _, _, raw = self.fixture()
        def table(name, values):
            return '.area CONST (CODE)\n' + name + ':\n' + ''.join(
                '\t.db #0x%02x\n' % value for value in values)
        bootstrap = table('_keymaps', raw) + table('_ak820_default_metadata', [16, 8, 2, 2, 0, 1])
        generated = defaults.generate(bootstrap)
        self.assertNotIn('static', generated)
        for name in ('classes', 'payload', 'offsets'):
            self.assertEqual(generated.count('const uint8_t __code ak820_default_' + name + '[]'), 1)


if __name__ == '__main__':
    unittest.main()
