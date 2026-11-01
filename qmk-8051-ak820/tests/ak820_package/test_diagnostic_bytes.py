"""Offline diagnostic build byte/path equivalence and validation checks."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

UTIL = Path(__file__).resolve().parents[2] / 'util'
sys.path.insert(0, str(UTIL))
spec = importlib.util.spec_from_file_location('diagnostic_byte_test', UTIL / 'ak820_diagnose.py')
diagnostic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostic)


def record(address, kind, payload=b''):
    data = bytes((len(payload), address >> 8, address & 255, kind)) + payload
    return b':' + (data + bytes((-sum(data) & 255,))).hex().upper().encode() + b'\n'


def report(ihx, symbols):
    return {'code_window': [diagnostic.CODE_START, diagnostic.CODE_END],
            'artifacts': [{'path': 'app.ihx', 'sha256': hashlib.sha256(ihx).hexdigest()},
                          {'path': 'app.map', 'sha256': hashlib.sha256(symbols).hexdigest()}]}


def encoded(value):
    return json.dumps(value).encode('utf-8')


class DiagnosticBytesTests(unittest.TestCase):
    def setUp(self):
        self.ihx = record(diagnostic.CODE_START, 0, b'\x12') + record(0, 1)
        self.symbols = b'C: 00003027 _ak820_nvm_diagnostic\n'
        self.report = report(self.ihx, self.symbols)

    def compare(self, ihx, symbols, build_report, error=None):
        with tempfile.TemporaryDirectory() as folder:
            paths = [Path(folder) / name for name in ('app.ihx', 'app.map', 'report.json')]
            for path, data in zip(paths, (ihx, symbols, build_report)):
                path.write_bytes(data)
            if error is None:
                self.assertEqual(diagnostic.diagnostic_build(*paths),
                                 diagnostic.diagnostic_build_bytes(ihx, symbols, build_report))
            else:
                with self.assertRaisesRegex(error[0], error[1]) as path_error:
                    diagnostic.diagnostic_build(*paths)
                with self.assertRaises(type(path_error.exception)) as byte_error:
                    diagnostic.diagnostic_build_bytes(ihx, symbols, build_report)
                self.assertEqual(str(path_error.exception), str(byte_error.exception))

    def test_valid_and_absent_inputs(self):
        self.compare(self.ihx, self.symbols, encoded(self.report))
        self.assertIsNone(diagnostic.diagnostic_build(None, None, None))
        self.assertIsNone(diagnostic.diagnostic_build_bytes(None, None, None))
        for inputs in ((None, b'x', b'x'), (b'x', None, b'x'), (b'x', b'x', None)):
            with self.assertRaisesRegex(ValueError, 'FD01 requires'):
                diagnostic.diagnostic_build_bytes(*inputs)
            with self.assertRaisesRegex(ValueError, 'FD01 requires'):
                diagnostic.diagnostic_build(*inputs)

    def test_tampering_and_validation_gates(self):
        bad_window = copy.deepcopy(self.report); bad_window['code_window'] = [0, 1]
        missing = copy.deepcopy(self.report); missing['artifacts'].pop()
        duplicate = copy.deepcopy(self.report); duplicate['artifacts'].append(duplicate['artifacts'][0])
        bad_ihx = self.ihx.replace(b'12', b'13', 1)
        no_symbol = b'C: 00003027 _other\n'
        wrong_symbol = b'C: 00003028 _ak820_nvm_diagnostic\n'
        outside = record(diagnostic.CODE_START - 1, 0, b'\x12') + record(0, 1)
        cases = [
            (self.ihx + b'x', self.symbols, encoded(self.report), 'IHX/MAP pair'),
            (self.ihx, self.symbols + b'x', encoded(self.report), 'IHX/MAP pair'),
            (self.ihx, self.symbols, encoded(bad_window), 'CODE window'),
            (self.ihx, self.symbols, encoded(missing), 'IHX/MAP pair'),
            (self.ihx, self.symbols, encoded(duplicate), 'IHX/MAP pair'),
            (self.ihx, no_symbol, encoded(report(self.ihx, no_symbol)), 'does not declare'),
            (self.ihx, wrong_symbol, encoded(report(self.ihx, wrong_symbol)), 'does not declare'),
            (bad_ihx, self.symbols, encoded(report(bad_ihx, self.symbols)), 'checksum'),
            (outside, self.symbols, encoded(report(outside, self.symbols)), 'outside application'),
        ]
        for ihx, symbols, build_report, message in cases:
            with self.subTest(message=message):
                self.compare(ihx, symbols, build_report, (ValueError, message))
        self.compare(self.ihx, self.symbols, b'\xff', (UnicodeDecodeError, 'utf-8'))
        self.compare(self.ihx, self.symbols, b'{', (json.JSONDecodeError, 'Expecting'))

    def test_bytes_not_reopened_after_capture(self):
        captured = (self.ihx, self.symbols, encoded(self.report))
        with tempfile.TemporaryDirectory() as folder:
            paths = [Path(folder) / name for name in ('app.ihx', 'app.map', 'report.json')]
            for path, data in zip(paths, captured):
                path.write_bytes(data)
            retained = tuple(path.read_bytes() for path in paths)
            paths[0].write_bytes(b'tampered')
            self.assertEqual(diagnostic.diagnostic_build_bytes(*retained),
                             {diagnostic.CODE_START: 0x12})
            with self.assertRaisesRegex(ValueError, 'IHX/MAP pair'):
                diagnostic.diagnostic_build(*paths)


if __name__ == '__main__':
    unittest.main()
