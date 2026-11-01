#!/usr/bin/env python3
"""Offline checks for the linked Auto Shift test's provenance and HID oracle."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('autoshift_linked', Path(__file__).with_name('linked.py'))
linked = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linked)


class LinkedComboTests(unittest.TestCase):
    def test_existing_report_is_preserved_and_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            linked.require_fresh_output(output)
            report = output / 'results.json'
            report.write_text('earlier evidence')
            with self.assertRaisesRegex(ValueError, 'earlier run; choose a fresh output directory'):
                linked.require_fresh_output(output)
            self.assertEqual(report.read_text(), 'earlier evidence')

    def test_complete_trace_and_invalid_variants(self):
        plain = [linked.report(4), linked.report(), linked.report(6), linked.report()]
        shifted = [linked.report(4), linked.report(), linked.report(6, 2), linked.report(0, 2), linked.report()]
        for mode, trace, combo, held in (
            ('plain', plain, linked.report(6), linked.report(6)),
            ('shifted', shifted, linked.report(), linked.report(6, 2)),
        ):
            def result(packets, passed=True, first=combo, second=held):
                return linked.combo_trace_result({'pass_': passed, 'hid_send_trace': packets, 'checks': [
                    {'label': 'combo_report', 'actual': first, 'expected': None},
                    {'label': 'combo_held_report', 'actual': second, 'expected': None},
                ]})
            with self.subTest(mode=mode):
                valid = result(trace)
                self.assertTrue(valid['pass'])
                self.assertEqual(valid['observed_combo_behavior'], mode)
                self.assertEqual(valid['expected_hid_send_trace'], trace)
                self.assertIn('not proof of configured option', valid['combo_behavior_evidence'])
                for invalid in ([], trace[:-1], trace + [linked.report()], plain + shifted, [None], trace[1:]):
                    self.assertFalse(result(invalid)['pass'], invalid)
                self.assertFalse(result(trace, passed=False)['pass'])
                self.assertFalse(result(trace, first=linked.report(99))['pass'])
                self.assertFalse(result(trace, second=linked.report(99))['pass'])

    def test_alternative_checks_are_deferred_not_ignored(self):
        choice = linked.ComboReportAlternatives(linked.report(6), linked.report())
        self.assertTrue(linked.report(6) == choice)
        self.assertTrue(linked.report() == choice)
        self.assertFalse(linked.report(7) == choice)

    def test_snapshot_extraction_is_bounded(self):
        extract = linked.emitted.Firmware.extract
        valid = '@@first\ndump xram 0x100 0x107 16\n0x0100                      00 00 04 00 00 00 00 00 ........\n'
        later = 'echo @@later\n@@later\ndump xram 0x100 0x107 16\n0x0100                      00 00 04 00 00 00 00 00 ........\n'
        self.assertEqual(extract(valid + later, 'first', 0x100, 8), [0, 0, 4, 0, 0, 0, 0, 0])
        for body in ('', '0x0100                      00 00 04 00 ....\n',
                     '0x0100                      00 00 04 00 ....\n0x0102                      04 00 00 00 ....\n',
                     '0x0100                      00 00 04 00 00 00 00 00 ........\n0x0100                      00 00 04 00 00 00 00 00 ........\n'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                extract('@@first\ndump xram 0x100 0x107 16\n' + body + later, 'first', 0x100, 8)
        for tail in ('', '\n' + later, 'diagnostic\n0x0100                      00 00 04 00 00 00 00 00 ........\nstate\n', valid):
            with self.subTest(tail=tail), self.assertRaises(ValueError):
                extract(valid + tail, 'first', 0x100, 8)
        self.assertEqual(extract('@@flag@\ndump bits 0x13 0x13 16\n0x13                      1 .\nstate\n', 'flag@', 0x13, 1), [1])
        row = '00 ' * 16 + '.' * 16 + '\n'
        self.assertEqual(extract('@@large\ndump xram 0x100 0x11f 16\n0x0100                      ' + row + '0x0110                      ' + row + 'state\n', 'large', 0x100, 32), [0] * 32)
        for tail in ('@@later\n0x82                      00 01 ..\nSimulation started, PC=0x000100\n',
                     '0x82                      00 .\n@@later\n0x82                      00 01 ..\nSimulation started, PC=0x000100\n'):
            with self.assertRaises(ValueError):
                extract('@@pointer\n' + tail, 'pointer', 0x82, 2)

    def test_report_width_uses_selected_projection(self):
        spec = importlib.util.spec_from_file_location('tap_emitted', linked.ROOT / 'tests/ak820_tapping/emitted.py')
        tap = importlib.util.module_from_spec(spec); spec.loader.exec_module(tap)
        class Firmware:
            def __init__(self, projected):
                self.symbols = {'_send_keyboard_report_projected_1': 0x100} if projected else {}
            def initialize(self): return []
            def address(self, name): return {'_send_keyboard_report_projected_1': 0x100, '_actual_keyboard_report': 0x200, '_ak820_host_send_keyboard': 0x300}[name]
        for projected in (False, True):
            trace = tap.Trace(Firmware(projected), 'width')
            address = 0x100 if projected else 0x200
            self.assertTrue(any(f'dump xram {address:#x} {address+7:#x} 16;' in c for c in trace.commands))
            trace.set_report_width(32)
            self.assertTrue(any(f'dump xram {address:#x} {address+31:#x} 16;' in c for c in trace.commands))
            self.assertEqual(trace.width, 32)
            row = '00 ' * 16 + '.' * 16
            data, end = tap.hid_dump([f'{address:#06x}                      {row}', f'{address+16:#06x}                      {row}'], 0, address, 32)
            self.assertEqual((data, end), ([0] * 32, 2))
            with self.assertRaises(ValueError): trace.set_report_width(32)

    def test_hid_dump_boundaries_and_rows(self):
        spec = importlib.util.spec_from_file_location('tap_emitted', linked.ROOT / 'tests/ak820_tapping/emitted.py')
        tap = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tap)
        packet = '0x0100                      00 00 04 00 00 00 00 00 ........\n'
        pointer = '0x82                      00 01 ..\n'
        space = "@@HIDB\n0xf0 B:                   0b00000000 0x00 '.'   0\n"
        resume = 'Simulation started, PC=0x00617c\n'
        def check(body, valid, width=8, prefix='', stop='Stop at 0x002700: (104) Breakpoint\n'):
            binding = f'commands 1 "echo @@HID; dump xram 0x100 {0x100+width-1:#x} 16; echo @@HIDPTR; dump sfr 0x82 0x83 16; echo @@HIDB; dump sfr 0xf0 0xf0 16; fill xram 0x2201 0x2203 0x12; run"'
            commands = ['break 0x617c', binding, 'run 0x2600 0x2700']
            log = prefix + 'break 0x617c\nBreakpoint 1 at 0x00617c (cond="")\n' + binding + '\nrun 0x2600 0x2700\nSimulation started, PC=0x002600\n' + body + stop
            if valid:
                tap.observe_hid(log, commands, 0x617c, 0x100, width)
            else:
                with self.assertRaises(ValueError): tap.observe_hid(log, commands, 0x617c, 0x100, width)
        record = '@@HID\n' + packet + '@@HIDPTR\n' + pointer + space + resume
        check('', True)
        check(record, True)
        check(record + record, True)
        check(resume, False)
        check(record.replace('@@HID\n', '', 1), False)
        check(record.replace('@@HIDPTR\n', '', 1), False)
        check(record.replace('@@HIDB\n', '', 1), False)
        check(record.replace('PC=0x00617c', 'PC=0x00617d'), False)
        check(record.replace('0b00000000 0x00', '0b00000001 0x00'), False)
        check(record.replace("0x00 '.'", "0x00 'X'"), False)
        check(record, False, stop='')
        check(record, False, stop='Stop at 0x002701: (104) Breakpoint\n')
        check('', True, prefix='echo @@HID\necho Simulation started, PC=0x00617c\n')
        for bad in ('', '0x0100                      00 00 04 00 ....\n', packet + packet,
                    '0x0100                      00 00 04 00 ....\n0x0102                      04 00 00 00 ....\n'):
            check('@@HID\n' + bad + '@@HIDPTR\n' + pointer + space + resume, False)
        for bad in ('', '0x82                      00 .\n', pointer + pointer, pointer + '\n' + pointer):
            check('@@HID\n' + packet + '@@HIDPTR\n' + bad + space + resume, False)
        row = '00 ' * 16 + '.' * 16 + '\n'
        check('@@HID\n0x0100                      ' + row + '0x0110                      ' + row + '@@HIDPTR\n' + pointer + space + resume, True, 32)
        check('@@HID\n0x0100                      ' + row + '0x0108                      ' + row + '@@HIDPTR\n' + pointer + space + resume, False, 32)

    def test_observer_setup_and_extra_callback(self):
        spec = importlib.util.spec_from_file_location('tap_emitted', linked.ROOT / 'tests/ak820_tapping/emitted.py')
        tap = importlib.util.module_from_spec(spec); spec.loader.exec_module(tap)
        binding = 'commands 1 "echo @@HID; dump xram 0x100 0x107 16; echo @@HIDPTR; dump sfr 0x82 0x83 16; fill xram 0x2201 0x2203 0x12; run"'
        setup = 'break 0x617c\nBreakpoint 1 at 0x00617c (cond="")\n' + binding + '\n'
        run = 'run 0x2600 0x2700\nSimulation started, PC=0x002600\n'
        stop = 'Stop at 0x002700: (104) Breakpoint\n'
        commands = ['break 0x617c', binding, 'run 0x2600 0x2700']
        self.assertEqual(tap.observe_hid(setup + run + stop, commands, 0x617c, 0x100, 8, capture_b=False)[3], 0)
        for log, cmds in ((run + stop + setup, ['run 0x2600 0x2700', 'break 0x617c', binding]),
                          (setup + 'delete 1\n' + run + stop, commands[:2] + ['delete 1'] + commands[2:]),
                          (setup.replace('0x00617c', '0x00617d') + run + stop, commands)):
            with self.assertRaises(ValueError): tap.observe_hid(log, cmds, 0x617c, 0x100, 8, capture_b=False)
        extra = 'commands 2 "echo @@EXTRA; dump xram 0x200 0x202 16; fill xram 0x2201 0x2203 0x12; run"'
        extra_setup = 'break 0x7000\nBreakpoint 2 at 0x007000 (cond="")\n' + extra + '\n'
        cmds = commands[:2] + ['break 0x7000', extra] + commands[2:]
        kw = dict(capture_b=False, extra_callback=0x7000, extra_address=0x200)
        record = '@@EXTRA\n0x0200                      04 e2 00 ...\nSimulation started, PC=0x007000\n'
        self.assertEqual(tap.observe_hid(setup + extra_setup + run + record + stop, cmds, 0x617c, 0x100, 8, **kw)[3], 0)
        with self.assertRaises(ValueError): tap.observe_hid(setup + extra_setup + run + 'Simulation started, PC=0x007000\n' + stop, cmds, 0x617c, 0x100, 8, **kw)
        for log, commands in ((setup + run + stop + extra_setup, commands[:2] + [commands[2], 'break 0x7000', extra]),
                              (setup + extra_setup + run + stop, cmds[:4] + [extra] + cmds[4:]),
                              (setup + extra_setup + 'commands 2 "run"\n' + run + stop, cmds[:4] + ['commands 2 "run"'] + cmds[4:]),
                              (setup + extra_setup + run + stop + 'Simulation started, PC=0x007000\n', cmds),
                              (setup + extra_setup + run + stop + '@@HID\n', cmds)):
            with self.assertRaises(ValueError): tap.observe_hid(log, commands, 0x617c, 0x100, 8, **kw)


if __name__ == '__main__':
    unittest.main()
