import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('startup_contract', Path(__file__).with_name('stack_contract.py'))
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)


class StartupStackTests(unittest.TestCase):
    def fixture(self):
        rows = {0: '75815d', 3: '120020', 6: '020010', 16: '120030', 19: '80fe',
                32: '758200', 35: '22', 48: 'c0e0', 50: '73'}
        instructions = {pc: bytes.fromhex(raw) for pc, raw in rows.items()}
        code = {pc + i: b for pc, raw in instructions.items() for i, b in enumerate(raw)}
        symbols = {'__sdcc_gsinit_startup': 0, '__sdcc_program_startup': 16, '_main': 48}
        return instructions, symbols, code

    def test_main_is_cutpoint_not_assumed_whole_program_leaf(self):
        result = contract.check(*self.fixture(), 0x5D)
        self.assertEqual(result['pre_main_control_stack_bound'], 2)
        self.assertEqual(result['main_entry_frame_bound'], 2)

    def test_extra_startup_frame_is_counted(self):
        instructions, symbols, code = self.fixture()
        # Use a balanced PUSH/POP helper instead of an untrusted expected scalar.
        del instructions[35]
        instructions[32] = b'\xc0\xe0'
        instructions[34] = b'\xd0\xe0'
        instructions[36] = b'\x22'
        code.update({pc + i: b for pc, raw in instructions.items() for i, b in enumerate(raw)})
        self.assertEqual(contract.check(instructions, symbols, code, 0x5D)['pre_main_control_stack_bound'], 3)

    def test_changed_stack_or_main_call_rejected(self):
        for location in ('stack', 'call'):
            instructions, symbols, code = self.fixture()
            if location == 'stack':
                instructions[0] = b'\x75\x81\x5c'
                code[2] = 0x5C
            else:
                code[16] = 0x02
            with self.assertRaises(ValueError):
                contract.check(instructions, symbols, code, 0x5D)

    def test_alternate_main_entry_rejected(self):
        instructions, symbols, code = self.fixture()
        instructions[6] = bytes.fromhex('6008')
        instructions[8] = bytes.fromhex('020030')
        code = {pc + i: b for pc, raw in instructions.items() for i, b in enumerate(raw)}
        with self.assertRaisesRegex(ValueError, 'Alternate main entry'):
            contract.check(instructions, symbols, code, 0x5D)

    def test_helper_tail_transfer_keeps_outer_frame(self):
        instructions, symbols, code = self.fixture()
        instructions[32] = bytes.fromhex('020010')
        del instructions[35]
        code = {pc + i: b for pc, raw in instructions.items() for i, b in enumerate(raw)}
        result = contract.check(instructions, symbols, code, 0x5D)
        self.assertEqual(result['pre_main_control_stack_bound'], 4)
        self.assertEqual(result['main_entry_frame_bound'], 4)

    def test_enabling_interrupts_or_unknown_startup_path_rejected(self):
        for raw in (b'\xd2\xaf', b'\x73'):
            instructions, symbols, code = self.fixture()
            instructions[32] = raw
            instructions[32 + len(raw)] = b'\x22'
            instructions.pop(35, None)
            with self.assertRaises(ValueError):
                contract.check(instructions, symbols, code, 0x5D)


if __name__ == '__main__':
    unittest.main()
