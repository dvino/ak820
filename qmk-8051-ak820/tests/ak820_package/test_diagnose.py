#!/usr/bin/env python3
"""CODE-only diagnostic regressions; no HID module or hardware is used."""
import binascii
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'util'))
import ak820_diagnose as diagnostic


class FakeApplication:
    native = False

    def __init__(self, rom, fail_at=None, stale_at=None, corrupt_second=False):
        self.rom = rom
        self.requests = []
        self.closed = False
        self.fail_at, self.stale_at = fail_at, stale_at
        self.corrupt_second = corrupt_second
        self.finished_full = False

    def raw(self, packet):
        self.requests.append(packet)
        if packet[:2] == bytes((0xFD, 1)):
            return bytes((0xFD, 1, 1, 0xA8)) + bytes(28)
        assert packet[:2] == bytes((0xFD, 0)), 'Unexpected non-read command'
        address = int.from_bytes(packet[2:4], 'big')
        count = packet[4]
        assert 1 <= count <= 27 and address + count <= 65536
        if address == self.fail_at:
            raise TimeoutError('modeled missing reply')
        reply = bytearray(packet[:5] + self.rom[address:address + count] + bytes(27 - count))
        if address == self.stale_at:
            reply[2] ^= 1
        if self.finished_full and self.corrupt_second:
            reply[5] ^= 1
        if address + count == 65536:
            self.finished_full = True
        return bytes(reply)

    def close(self):
        self.closed = True


class DiagnoseTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='ak820-diagnose-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.rom = bytearray(65536)
        self.rom[0xC725:0xC728] = diagnostic.BUILD_ID.to_bytes(3, 'little')
        self.rom[0xC740:0xC742] = b'\x00\x04'

    def test_direct_code_key_ignores_ram_getter_value(self):
        result = diagnostic.analyze(bytes(self.rom), key=(0, 0, 0))
        self.assertEqual(result['key']['keycode'], 4)
        self.assertEqual(result['key']['code_address'], 0xC740)
        self.assertIn('directly from CODE', result['ram_cache'])
        for key in ((6, 0, 0), (0, 16, 0), (0, 0, 8), (-1, 0, 0)):
            with self.assertRaises(ValueError):
                diagnostic.key_address(*key)

    def test_schema_fault_is_decoded_without_hiding_its_stage(self):
        reply = bytearray((0xFD, 1, 1, 0xA8)) + bytearray(28)
        reply[4] = 1
        reply[10] = 16
        decoded = diagnostic.decode_status(reply)
        self.assertTrue(decoded['storage_failed'])
        self.assertEqual(decoded['first_failure_stage'], 16)
        self.assertEqual(decoded['first_failure_stage_name'], 'schema_mismatch')

    def test_completed_journal_retains_data(self):
        self.rom[0xEF00:0xEF40] = bytes(range(64))
        result = diagnostic.journal_report(bytes(self.rom))
        self.assertEqual(result['state'], 'empty_header')
        self.assertTrue(result['data_nonzero'])

    def committed_journal(self):
        data = bytes(range(64))
        crc = binascii.crc_hqx(data, 0xFFFF)
        metadata = bytes((1, 0)) + crc.to_bytes(2, 'little')
        self.rom[0xEF00:0xEF40] = data
        self.rom[0xEF40:0xEF49] = b'\xA5' + metadata + bytes(v ^ 0xFF for v in metadata)
        return data

    def test_committed_record_is_not_reported_as_clean(self):
        data = self.committed_journal()
        self.assertEqual(diagnostic.journal_report(bytes(self.rom))['state'], 'committed_target_differs')
        self.rom[0xC740:0xC780] = data
        self.assertEqual(diagnostic.journal_report(bytes(self.rom))['state'], 'committed_target_matches')
        self.rom[0xEF05] ^= 1
        self.assertEqual(diagnostic.journal_report(bytes(self.rom))['state'], 'committed_invalid_data_crc')

    def test_partial_header_is_preserved_not_erased(self):
        self.rom[0xEF41] = 1
        before = bytes(self.rom)
        self.assertEqual(diagnostic.journal_report(before)['state'], 'uncommitted_or_torn_header')
        self.assertEqual(bytes(self.rom), before)

    def test_capture_only_code_reads_and_no_status_without_build(self):
        app = FakeApplication(bytes(self.rom))
        output = self.root / 'capture'
        report = diagnostic.capture(output, app_factory=lambda: app)
        self.assertTrue(report['completed'])
        self.assertTrue(report['nvm_and_journal_stable_on_second_read'])
        self.assertFalse(report['fd01_requested'])
        self.assertEqual((output / 'rom.bin').read_bytes(), bytes(self.rom))
        self.assertFalse((output / 'rom-prefix.bin').exists())
        self.assertTrue(app.closed)
        self.assertTrue(all(p[:2] == b'\xfd\x00' for p in app.requests))

    def test_partial_capture_and_trace_survive_timeout(self):
        app = FakeApplication(bytes(self.rom), fail_at=54)
        output = self.root / 'capture'
        with self.assertRaises(TimeoutError):
            diagnostic.capture(output, app_factory=lambda: app)
        report = json.loads((output / 'report.json').read_text())
        self.assertEqual(report['bytes_captured'], 54)
        self.assertFalse(report['completed'])
        self.assertEqual((output / 'rom-prefix.bin').read_bytes(), bytes(self.rom[:54]))
        self.assertIn('modeled missing reply', (output / 'transport.jsonl').read_text())
        self.assertTrue(app.closed)

    def test_stale_reply_is_rejected_without_blind_retry(self):
        app = FakeApplication(bytes(self.rom), stale_at=27)
        with self.assertRaisesRegex(ValueError, 'Mismatched FD00'):
            diagnostic.capture(self.root / 'capture', app_factory=lambda: app)
        self.assertEqual(len(app.requests), 2)
        self.assertTrue(app.closed)

    def test_fd01_requires_exact_code_match(self):
        self.rom[0x3040] = 0x22
        app = FakeApplication(bytes(self.rom))
        report = diagnostic.capture(self.root / 'valid', code={0x3040: 0x22}, app_factory=lambda: app)
        self.assertTrue(report['fd01_requested'])
        self.assertEqual(app.requests[-1][:2], b'\xfd\x01')
        app = FakeApplication(bytes(self.rom))
        with self.assertRaisesRegex(ValueError, 'CODE differs'):
            diagnostic.capture(self.root / 'wrong', code={0x3040: 0}, app_factory=lambda: app)
        self.assertTrue(all(p[:2] == b'\xfd\x00' for p in app.requests))

    def test_fd01_is_not_sent_on_changing_nvm(self):
        app = FakeApplication(bytes(self.rom), corrupt_second=True)
        with self.assertRaisesRegex(ValueError, 'NVM/journal changed'):
            diagnostic.capture(self.root / 'changing', code={0x3040: 0}, app_factory=lambda: app)
        self.assertTrue(all(p[:2] == b'\xfd\x00' for p in app.requests))

    def test_unknown_schema_and_partial_rom_rejected(self):
        with self.assertRaisesRegex(ValueError, 'full 65536'):
            diagnostic.analyze(bytes(64))
        with self.assertRaisesRegex(ValueError, 'Unknown NVM schema'):
            diagnostic.analyze(bytes(65536), key=(0, 0, 0))

    def test_status_version_and_reserved_validation(self):
        good = bytearray((0xFD, 1, 1, 0xA8)) + bytearray(28)
        self.assertFalse(diagnostic.decode_status(good)['storage_failed'])
        for index, value in ((2, 2), (3, 0), (4, 2), (31, 1)):
            bad = bytearray(good)
            bad[index] = value
            with self.assertRaises(ValueError):
                diagnostic.decode_status(bad)

    def test_existing_output_never_overwritten(self):
        output = self.root / 'existing'
        output.mkdir()
        app = FakeApplication(bytes(self.rom))
        with self.assertRaises(FileExistsError):
            diagnostic.capture(output, app_factory=lambda: app)
        self.assertEqual(app.requests, [])

    def test_diagnostic_build_requires_bound_ihx_map_pair(self):
        ihx, mapfile, reportfile = (self.root / name for name in ('candidate.ihx', 'candidate.map', 'build-report.json'))
        def hex_image(value):
            body = bytes((1, 0x30, 0x27, 0, value))
            return ':' + (body + bytes((-sum(body) & 255,))).hex() + '\n:00000001FF\n'
        ihx.write_text(hex_image(0x22))
        mapfile.write_text('C: 00003027 _ak820_nvm_diagnostic\n')
        report = {'code_window': [diagnostic.CODE_START, diagnostic.CODE_END],
                  'artifacts': [{'path': 'original/candidate' + suffix, 'sha256': diagnostic.digest(path.read_bytes())}
                                for suffix, path in (('.ihx', ihx), ('.map', mapfile))]}
        reportfile.write_text(json.dumps(report))
        self.assertEqual(diagnostic.diagnostic_build(ihx, mapfile, reportfile), {0x3027: 0x22})
        ihx.write_text(hex_image(0x00))
        with self.assertRaisesRegex(ValueError, 'IHX/MAP pair'):
            diagnostic.diagnostic_build(ihx, mapfile, reportfile)
        ihx.write_text(hex_image(0x22))
        mapfile.write_text('C: 00003027 _different_symbol\n')
        with self.assertRaisesRegex(ValueError, 'IHX/MAP pair'):
            diagnostic.diagnostic_build(ihx, mapfile, reportfile)
        with self.assertRaisesRegex(ValueError, 'requires'):
            diagnostic.diagnostic_build(ihx, mapfile, None)
        self.assertIsNone(diagnostic.diagnostic_build(None, None, None))
        report['artifacts'].append(report['artifacts'][0])
        reportfile.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'IHX/MAP pair'):
            diagnostic.diagnostic_build(ihx, mapfile, reportfile)


if __name__ == '__main__':
    unittest.main()
