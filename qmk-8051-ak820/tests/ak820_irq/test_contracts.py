"""Negative instruction checks for the IRQ architectural contract."""
import importlib.util
import copy
import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('irq_runner', Path(__file__).with_name('run.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class PublicWrappers(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads(runner.WRAPPER_FIXTURE.read_text())

    def check_rejected(self, fixture):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'wrappers.json'
            path.write_text(json.dumps(fixture))
            with self.assertRaises(ValueError):
                runner.load_wrapper_fixture(path)

    def test_fixture_matches_retained_public_evidence(self):
        wrappers, source = runner.load_wrappers()
        self.assertEqual(source['kind'], 'public-pinned-wrapper-fixture')
        self.assertEqual(source['instruction_bytes'], 234)
        records = {}
        for evidence in self.fixture['origin']['evidence']:
            path = runner.ROOT.parent / evidence['path']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), evidence['sha256'])
            records[path.name] = path.read_text()
        contract = json.loads(records['static-contract.json'])
        self.assertEqual(contract['oem_sha256'], runner.WRAPPER_ORIGIN_SHA256)
        self.assertEqual(json.loads(records['results.json'])['stock_rom_sha256'], runner.WRAPPER_ORIGIN_SHA256)
        for name, (address, raw) in wrappers.items():
            self.assertEqual(hashlib.sha256(raw).hexdigest(), next(
                row['wrapper_sha256'] for row in contract['wrappers'] if row['callback'] == name))
        for address, raw in [*wrappers.values(), (runner.HELPER_ADDRESS, runner.HELPER_BYTES)]:
            matches = re.findall(r'^set memory rom ' + hex(address) + r' ((?:0x[0-9a-f]+(?: |$))+)',
                                 records['timer-usb-led.log'], re.M)
            self.assertEqual(len(matches), 1)
            self.assertEqual(bytes(int(value, 16) for value in matches[0].split()), raw)

    def test_every_changed_instruction_byte_fails_even_with_updated_checksum(self):
        for name in (None, *runner.IRQ):
            original = self.fixture['helper'] if name is None else self.fixture['wrappers'][name]
            for offset in range(original['bytes']):
                with self.subTest(wrapper=name, offset=offset):
                    fixture = copy.deepcopy(self.fixture)
                    record = fixture['helper'] if name is None else fixture['wrappers'][name]
                    changed = bytearray.fromhex(record['hex'])
                    changed[offset] ^= 1
                    record['hex'] = changed.hex()
                    record['sha256'] = hashlib.sha256(changed).hexdigest()
                    self.check_rejected(fixture)

    def test_missing_or_relabelled_wrapper_fails(self):
        for name in runner.IRQ:
            for field in ('hex', 'sha256', 'bytes', 'address', 'ordinal'):
                with self.subTest(wrapper=name, field=field):
                    fixture = copy.deepcopy(self.fixture)
                    del fixture['wrappers'][name][field]
                    self.check_rejected(fixture)
            fixture = copy.deepcopy(self.fixture)
            del fixture['wrappers'][name]
            self.check_rejected(fixture)
            for field in ('ordinal', 'address', 'bytes'):
                fixture = copy.deepcopy(self.fixture)
                fixture['wrappers'][name][field] += 1
                self.check_rejected(fixture)
        fixture = copy.deepcopy(self.fixture)
        fixture['wrappers']['extra'] = fixture['wrappers']['timer']
        self.check_rejected(fixture)

    def test_missing_helper_or_changed_origin_fails(self):
        for field in ('helper', 'origin', 'format'):
            fixture = copy.deepcopy(self.fixture)
            del fixture[field]
            self.check_rejected(fixture)
        for field in ('stock_rom_sha256', 'protected_region_sha256'):
            fixture = copy.deepcopy(self.fixture)
            fixture['origin'][field] = '0' * 64
            self.check_rejected(fixture)

    def test_private_rom_validation_is_not_bypassed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid-rom.bin'
            path.write_bytes(b'not a complete OEM ROM')
            with self.assertRaisesRegex(ValueError, 'Incorrect ROM/reference image'):
                runner.load_wrappers(stock_path=path)
            with self.assertRaisesRegex(ValueError, 'Choose either'):
                runner.load_wrappers(stock_path=path, fixture_path=runner.WRAPPER_FIXTURE)


class PriorityWrites(unittest.TestCase):
    def test_reject_direct_and_bit_write_forms(self):
        for raw in ('75b800', '75e900', 'f5b8', '85a0e9', 'd0b8', 'c5b8', 'd2b8', 'c2bd', '92b9', '10b800'):
            with self.subTest(raw=raw), self.assertRaises(AssertionError):
                runner.reject_priority_write(bytes.fromhex(raw), 0x4000)

    def test_reads_and_distinct_extended_enable_bit_are_allowed(self):
        # E9 as a bit address is IE_EX.1; E9 as a byte address is IP_EX.
        for raw in ('e5b8', 'e5e9', 'd2e9', 'c2ae', 'd2d0'):
            runner.reject_priority_write(bytes.fromhex(raw), 0x4000)



class DirectTransfers(unittest.TestCase):
    def test_all_page_encodings_reach_shared_helper(self):
        for page in range(8):
            for low in (1, 0x11):
                raw = bytes(((page << 5) | low, 0x42))
                target = 0x4800 | page << 8 | 0x42
                self.assertEqual(runner.direct_references({0x47FE: raw}, target), [0x47FE])
        self.assertEqual(runner.direct_target(0x1234, bytes.fromhex('124567')), 0x4567)
        self.assertEqual(runner.direct_target(0x1234, bytes.fromhex('024567')), 0x4567)

    def test_unmasked_short_transfer_mutation_fails_contract(self):
        for opcode in range(1, 256, 32):
            for call_bit in (0, 0x10):
                raw = bytes((opcode | call_bit, 0x42))
                target = runner.direct_target(0x4000, raw)
                with self.subTest(opcode=raw[0]), self.assertRaises(AssertionError):
                    runner.masked_helper_calls({0x4000: raw}, target, set(), {0x4000, target}, 0x4010, 0x4020)

    def test_ajmp_mutation_cannot_skip_initialization_mask(self):
        class Fixture:
            def __init__(self, raw):
                self.rows = {0x4000: raw, 0x4002: bytes.fromhex('c2af'), 0x4004: b'\x22'}
            def instruction(self, pc):
                return self.rows.get(pc)
        for opcode in range(1, 256, 32):
            with self.subTest(opcode=opcode), self.assertRaises(AssertionError):
                runner.linear_init_pcs(Fixture(bytes((opcode, 4))), 'mutated_init', 0x4000)
        self.assertEqual(runner.linear_init_pcs(Fixture(bytes.fromhex('1104')), 'call_init', 0x4000), [0x4000, 0x4002, 0x4004])

if __name__ == '__main__':
    unittest.main()
