"""Offline equivalence and malformed-input checks for byte parsers."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

UTIL = Path(__file__).resolve().parents[2] / 'util' / 'pack_ak820.py'
spec = importlib.util.spec_from_file_location('pack_ak820_byte_test', UTIL)
pack = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pack)


def record(address, kind, payload=b''):
    raw = bytes((len(payload), address >> 8, address & 255, kind)) + payload
    return b':' + (raw + bytes((-sum(raw) & 255,))).hex().upper().encode() + b'\n'


class ByteParserTests(unittest.TestCase):
    def compare(self, data, path_parser, byte_parser):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'input'
            path.write_bytes(data)
            try:
                expected = path_parser(path)
            except Exception as error:
                with self.assertRaises(type(error)) as actual:
                    byte_parser(data)
                self.assertEqual(str(actual.exception), str(error))
            else:
                self.assertEqual(expected, byte_parser(data))

    def test_ihex_equivalence_and_rejection(self):
        start = record(pack.CODE_START, 0, b'\x01\x02')
        end = record(0, 1)
        self.assertEqual(pack.parse_ihex_bytes(start + end), {pack.CODE_START: 1, pack.CODE_START + 1: 2})
        cases = [start + end, start.replace(b'\n', b'\r\n') + end,
                 b'', start, start + end + end, b'not hex\n',
                 start[:-3] + b'00\n' + end,
                 record(pack.CODE_START - 1, 0, b'\x01') + end,
                 start + record(pack.CODE_START, 0, b'\x03') + end,
                 record(0, 5, b'') + end, b'\xff']
        for index, data in enumerate(cases):
            with self.subTest(data=data):
                self.compare(data, pack.read_ihex, pack.parse_ihex_bytes)
                if index >= 2:
                    with self.assertRaises((ValueError, UnicodeError)):
                        pack.parse_ihex_bytes(data)

    def test_map_equivalence(self):
        # Original parser uses the last occurrence; duplicate names are not uniqueness proof.
        self.assertEqual(pack.parse_symbols_bytes(b'C: 00003027 _symbol\nC: 00003028 _symbol\n'),
                         {'_symbol': 0x3028})
        # Lines from retained main MAP; original parser's last-address results.
        linked = (b'C:   00007E68  _notify_usb_device_state_change_   usb_device_state\n'
                  b'C:   00007E74  _notify_usb_device_state_change_   usb_device_state\n'
                  b'C:   00009600  _dynamic_keymap_macro_get_buffer   dynamic_keymap\n'
                  b'C:   00009604  _dynamic_keymap_macro_get_buffer   dynamic_keymap\n')
        self.assertEqual(pack.parse_symbols_bytes(linked), {
            '_notify_usb_device_state_change_': 0x7E74,
            '_dynamic_keymap_macro_get_buffer': 0x9604})
        for data in (b'', b'C: 00003027 _symbol\r\nC: 000028A0 _other\n',
                     b'C: 00003027 _symbol\nC: 00003028 _symbol\n', b'\xff'):
            with self.subTest(data=data):
                self.compare(data, pack.read_symbols, pack.parse_symbols_bytes)


if __name__ == '__main__':
    unittest.main()
