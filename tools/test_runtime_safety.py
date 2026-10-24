"""Negative controls for the combined application/CRT/interrupt stack bound."""
import copy
import itertools
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ak820_runtime_safety import combine, ROOTS


class RuntimeSafetyTests(unittest.TestCase):
    def setUp(self):
        self.identity = {'ihx_sha256': 'image', 'map_sha256': 'map', 'mem_sha256': 'mem'}
        self.memory = {'stack_capacity': 166, 'initial_sp': 89}
        self.sources = {name: name for name in (
            'qmk-8051-ak820/tests/ak820_stack/analyze.py',
            'qmk-8051-ak820/util/ak820_linked_inventory.py',
            'qmk-8051-ak820/tests/ak820_startup/stack_contract.py',
            'qmk-8051-ak820/tests/ak820_irq/run.py',
            'qmk-8051-ak820/tests/ak820_irq/oem-wrappers.json')}
        analyzer, decoder, startup, irq, fixture = self.sources.values()
        bounds = {'_main': 100, '_ak820_timer_irq': 2, '_USB_DeviceInterrupt': 6, '_ak820_led_irq': 2}
        roots = {name: {'bound': bound, 'unresolved': []} for name, bound in bounds.items()}
        self.runtime = {'identity': self.identity.copy(), 'analyzer_sha256': analyzer,
                        'decoder_source_sha256': decoder, 'roots': roots}
        self.startup = {'identity': self.identity.copy(), 'analyzer_sha256': analyzer,
                        'checker_sha256': startup, 'main_entry_frame_bound': 2,
                        'pre_main_control_stack_bound': 4, 'interrupt_enables_unchanged_until_main': True,
                        'crt_initial_sp': 89}
        irq_bounds = {name: 17 + bounds[symbol] for name, symbol in ROOTS.items()}
        orders = [order for length in range(1, 4) for order in itertools.permutations(ROOTS, length)]
        self.irq = {'pass': True, 'linked_image_sha256': 'image', 'linked_map_sha256': 'map',
                    'stack_analyzer_sha256': analyzer, 'runner_sha256': irq,
                    'wrapper_source': {'kind': 'public-pinned-wrapper-fixture', 'fixture_sha256': fixture,
                                       'instruction_bytes': 234},
                    'wrapper_bytes_on_stack': 17, 'irq_bounds': irq_bounds,
                    'callback_static_reports': {name: roots[symbol].copy() for name, symbol in ROOTS.items()},
                    'all_distinct_source_irq_bound': 61, 'stack_capacity': 166, 'initial_sp': 89,
                    'cpu_cases': [{'irq_order': list(order), 'canary_and_registers_preserved': True,
                                   'irq_stack_bytes': sum(irq_bounds[name] for name in order)} for order in orders],
                    'selector_cases': {'input_values_checked': 256, 'bounded_table_entries': 16},
                    'emitted_contracts': {'compiler_register_bank': 0, 'shared_helper_masked_init_calls': [1],
                                          'nonoverlay_allocations': [1]}}

    def check(self):
        return combine(self.runtime, self.startup, self.irq, self.identity, self.memory, self.sources)

    def test_exact_fit_arithmetic_is_separate_from_release_and_device_approval(self):
        result = self.check()
        self.assertTrue(result['passed'])
        self.assertTrue(result['whole_program_stack_qualified'])
        self.assertEqual((result['stack_bound'], result['stack_margin']), (163, 3))
        self.assertFalse(result['release_approved'])
        self.assertFalse(result['hardware_validated'])
        self.assertEqual(result['physical_device_commands'], 0)

    def test_overflow_is_reported_with_negative_margin(self):
        self.runtime['roots']['_main']['bound'] = 107
        result = self.check()
        self.assertFalse(result['passed'])
        self.assertEqual((result['stack_bound'], result['stack_margin']), (170, -4))

    def test_pre_main_peak_is_included(self):
        self.startup['pre_main_control_stack_bound'] = 170
        result = self.check()
        self.assertFalse(result['passed'])
        self.assertEqual(result['stack_bound'], 170)

    def test_unknown_root_does_not_use_explored_peak(self):
        self.runtime['roots']['_main'] = {'bound': None, 'explored_peak': 1, 'unresolved': ['indirect call']}
        result = self.check()
        self.assertFalse(result['passed'])
        self.assertIsNone(result['stack_bound'])
        self.assertIsNone(result['stack_margin'])
        self.assertEqual(result['unresolved_roots'], ['_main'])

    def test_missing_root_unresolved_bound_and_boolean_fail(self):
        original = copy.deepcopy(self.runtime['roots'])
        for mutation in ('missing', 'unresolved', 'bool', 'negative'):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.runtime['roots'] = copy.deepcopy(original)
                if mutation == 'missing':
                    del self.runtime['roots']['_ak820_led_irq']
                elif mutation == 'unresolved':
                    self.runtime['roots']['_main']['unresolved'] = ['still unknown']
                else:
                    self.runtime['roots']['_main']['bound'] = True if mutation == 'bool' else -1
                self.check()

    def test_stale_image_map_and_checker_fail(self):
        cases = [(self.runtime['identity'], 'ihx_sha256'), (self.startup['identity'], 'map_sha256'),
                 (self.irq, 'linked_image_sha256'), (self.irq, 'linked_map_sha256'),
                 (self.runtime, 'analyzer_sha256'), (self.startup, 'analyzer_sha256'),
                 (self.irq, 'stack_analyzer_sha256'), (self.startup, 'checker_sha256'),
                 (self.irq, 'runner_sha256'), (self.runtime, 'decoder_source_sha256'),
                 (self.irq['wrapper_source'], 'fixture_sha256')]
        for record, key in cases:
            old = record[key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                record[key] = 'stale'
                self.check()
            record[key] = old

    def test_incomplete_irq_orders_and_register_failure_fail(self):
        original = copy.deepcopy(self.irq['cpu_cases'])
        for mutation in ('missing', 'duplicate', 'registers', 'peak'):
            self.irq['cpu_cases'] = copy.deepcopy(original)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                if mutation == 'missing':
                    self.irq['cpu_cases'].pop()
                elif mutation == 'duplicate':
                    self.irq['cpu_cases'][0] = self.irq['cpu_cases'][1]
                elif mutation == 'registers':
                    self.irq['cpu_cases'][0]['canary_and_registers_preserved'] = False
                else:
                    self.irq['cpu_cases'][0]['irq_stack_bytes'] = 255
                self.check()

    def test_irq_total_callback_and_wrapper_frame_changes_fail(self):
        cases = [(self.irq, 'all_distinct_source_irq_bound', 60),
                 (self.irq, 'wrapper_bytes_on_stack', 15),
                 (self.irq['callback_static_reports']['timer'], 'bound', 1),
                 (self.irq['irq_bounds'], 'usb', 22)]
        for record, key, value in cases:
            old = record[key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                record[key] = value
                self.check()
            record[key] = old

    def test_startup_capacity_and_abi_mutations_fail(self):
        cases = [(self.startup, 'main_entry_frame_bound', 0), (self.startup, 'crt_initial_sp', 88),
                 (self.startup, 'interrupt_enables_unchanged_until_main', False),
                 (self.irq, 'stack_capacity', 167), (self.irq, 'initial_sp', 88),
                 (self.memory, 'stack_capacity', 167),
                 (self.irq['selector_cases'], 'input_values_checked', 255),
                 (self.irq['emitted_contracts'], 'compiler_register_bank', 1),
                 (self.irq['emitted_contracts'], 'shared_helper_masked_init_calls', []),
                 (self.irq['emitted_contracts'], 'nonoverlay_allocations', [])]
        for record, key, value in cases:
            old = record[key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                record[key] = value
                self.check()
            record[key] = old


if __name__ == '__main__':
    unittest.main()
