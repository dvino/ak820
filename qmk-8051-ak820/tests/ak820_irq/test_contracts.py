"""Negative instruction checks for the IRQ architectural contract."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('irq_runner', Path(__file__).with_name('run.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


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
