"""Synthetic evidence tests only; no linked image is qualified by these tests."""
import unittest

import ak820_leader_marker as marker


class MarkerTests(unittest.TestCase):
    def evidence(self, value=300, address=0x3100):
        raw = marker.PREFIX + value.to_bytes(2, 'little')
        code = {address + i: byte for i, byte in enumerate(raw)}
        packed = bytearray(marker.CODE_END - marker.APP_START)
        packed[address - marker.APP_START:address - marker.APP_START + 6] = raw
        return f'C:   {address:08X}  {marker.SYMBOL} module\n', code, bytes(packed)

    def test_defaults_and_overrides(self):
        for value in (1, 300, 713, 1000):
            self.assertEqual(marker.extract(*self.evidence(value))['milliseconds'], value)

    def test_fail_closed(self):
        text, code, packed = self.evidence()
        bad_code = dict(code)
        del bad_code[0x3105]
        duplicate = dict(code)
        duplicate.update({0x3200 + i: byte for i, byte in enumerate(marker.PREFIX)})
        for args in ((text + text, code, packed), ('', code, packed),
                     (text.replace('C:', 'D:'), code, packed),
                     (text + 'C:   00003101  _other module\n', code, packed),
                     (text, bad_code, packed), (text, duplicate, packed),
                     (text, code, bytes(len(packed))), self.evidence(0),
                     self.evidence(1001), self.evidence(300, 0x2ffd)):
            with self.subTest(args=args[0][:60]), self.assertRaises(ValueError):
                marker.extract(*args)


if __name__ == '__main__':
    unittest.main()
