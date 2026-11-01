#!/usr/bin/env python3
"""Offline checks for interactive simulator observation framing."""
import importlib.util
import io
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('iap', Path(__file__).with_name('run.py'))
iap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(iap)

# Retained pointer IRQ timer.log, lines 689-694.
RESPONSE = ('echo @@read6\n'
            'dump iram 0x0 0x7 16\n'
            'echo __DONE_7__\n'
            '@@read6\n'
            '0x00                      30 31 32 33 34 35 36 37 01234567\n'
            '__DONE_7__\n')


class ConsoleObservationTests(unittest.TestCase):
    def test_rom_hex_captured_framing(self):
        log = ('echo @@read1\ndump /h rom 0xef00 0xef3f 16\n'
               'echo __DONE_2__\n@@read1\n' +
               ''.join(f'0x{address:x} ' + 'ff ' * 16 + '.' * 16 + '\n'
                       for address in range(0xef00, 0xef40, 16)) + '__DONE_2__\n')
        def parse(text):
            console = iap.Console.__new__(iap.Console)
            console.sequence = 1
            def command(commands):
                self.assertEqual(commands, ['echo @@read1', 'dump /h rom 0xef00 0xef3f 16'])
                console.sequence += 1
                return text
            console.command = command
            return console.read('rom', 0xef00, 64)
        self.assertEqual(parse(log), [255] * 64)
        for bad in (log.replace('/h rom', 'rom'), log.replace('/h rom', '/h xram'),
                    log.replace('0xef10 ', '0xef11 '), log.replace('ff ff', '31 ff', 1),
                    log.replace('................', '...............X', 1),
                    log.replace('0xef10 ', '0xef00 '), log.rsplit('__DONE_', 1)[0]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse(bad)
        echoed = '@@read1\ndump /h rom 0xef00 0xef3f 16\n' + ''.join(log.splitlines(keepends=True)[4:8]) + 'quit\n'
        self.assertEqual(iap.emitted.Firmware.extract(echoed, 'read1', 0xef00, 64), [255] * 64)
        for bad in (echoed.replace('/h rom', 'rom'), echoed.replace('/h rom', '/h xram')):
            with self.assertRaises(ValueError):
                iap.emitted.Firmware.extract(bad, 'read1', 0xef00, 64)

    def test_timeout_invalidates_console(self):
        console = iap.Console.__new__(iap.Console)
        console.sequence, console.log = 0, ''
        console.process = SimpleNamespace(stdin=io.BytesIO(), stdout=SimpleNamespace(fileno=lambda: 4))
        with patch.object(iap.time, 'monotonic', side_effect=[0, 21]):
            with self.assertRaises(TimeoutError):
                console.read('rom', 0xef00, 64)
        with self.assertRaisesRegex(RuntimeError, 'unusable'):
            console.command('state')

    def test_read_io_error_invalidates_console(self):
        console = iap.Console.__new__(iap.Console)
        console.sequence, console.log = 0, ''
        console.process = SimpleNamespace(stdin=io.BytesIO(), stdout=SimpleNamespace(fileno=lambda: 4))
        with patch.object(iap.select, 'select', side_effect=OSError('read failed')):
            with self.assertRaises(OSError):
                console.read('rom', 0xef00, 64)
        with self.assertRaisesRegex(RuntimeError, 'unusable'):
            console.command('state')

    @unittest.skipUnless(os.environ.get('AK820_S51') and os.environ.get('AK820_IHX'), 'requires pinned simulator and image')
    def test_real_rom_hex_and_negative_framing(self):
        console = iap.Console(Path(os.environ['AK820_S51']), Path(os.environ['AK820_IHX']))
        try:
            # Consume the startup banner before testing the framed exchange.
            console.command('state')
            original = console.command
            captures = []
            def capture(commands):
                text = original(commands)
                captures.append(text)
                return text
            console.command = capture
            values = console.read('rom', 0xef00, 64)
            self.assertEqual(values, [255] * 64)
            log = captures[0]
            self.assertIn('dump /h rom 0xef00 0xef3f 16\n', log)
            self.assertEqual(len(log.splitlines()), 9)
            rows = log.splitlines(keepends=True)
            for bad in (
                log.replace('dump /h rom', 'dump rom'),
                log.replace('dump /h rom', 'dump /h xram'),
                log.replace('0xef00 ', '0xef01 ', 1),
                log.replace(rows[4], ''),
                log.replace(rows[4], rows[4] * 2),
                log.replace('ff ff', '31 ff', 1),
                log.replace('................', '...............X', 1),
                log.rsplit('__DONE_', 1)[0],
                log + 'chatter\n',
            ):
                broken = iap.Console.__new__(iap.Console)
                broken.sequence = 1
                def command(commands):
                    broken.sequence += 1
                    return bad
                broken.command = command
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    broken.read('rom', 0xef00, 64)
                self.assertTrue(broken.invalid_observation)
                with self.assertRaisesRegex(RuntimeError, 'unusable'):
                    iap.Console.command(broken, 'state')
        finally:
            console.close()
            console.process.stdin.close()
            console.process.stdout.close()

    def read_response(self, response):
        console = iap.Console.__new__(iap.Console)
        console.sequence = 6
        def command(commands):
            self.assertEqual(commands, ['echo @@read6', 'dump iram 0x0 0x7 16'])
            console.sequence += 1
            return response
        console.command = command
        return console.read('iram', 0, 8)

    def test_retained_response(self):
        self.assertEqual(self.read_response(RESPONSE), list(range(48, 56)))

    def test_retained_sfr_and_malformed_responses(self):
        log = Path(__file__).with_name('retained_sfr.txt').read_text()
        rows = log.splitlines(keepends=True)
        def parse(text):
            console = iap.Console.__new__(iap.Console)
            console.sequence = 43
            def command(commands):
                self.assertEqual(commands, ['echo @@read43', 'dump sfr 0x80 0xbf 16'])
                console.sequence += 1
                return text
            console.command = command
            try:
                return console.read('sfr', 0x80, 64)
            except ValueError:
                self.assertTrue(console.invalid_observation)
                raise
        values = parse(log)
        self.assertEqual(len(values), 64)
        self.assertEqual(values[:9], [255, 0x61, 0xed, 4, 0, 0xc7, 0xa6, 0, 0])
        for bad in (
            log.replace(rows[4], ''),
            log.replace(rows[4], rows[4] * 2),
            log.replace(rows[4] + rows[5], rows[5] + rows[4]),
            log.replace(rows[4], 'chatter\n' + rows[4]),
            log.replace(rows[4], rows[4].replace('0xff', '0xfe')),
            log.replace(rows[6], rows[6].replace('ed 04', 'ed')),
            log.replace('@@read43\n0x80', '@@read43\n@@read43\n0x80'),
            log.replace('dump sfr 0x80 0xbf 16', 'dump sfr 0x80 0xbe 16'),
            log.replace('echo __DONE_44__', 'echo __DONE_45__'),
            log.rsplit('__DONE_44__\n', 1)[0],
            log + 'chatter\n',
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse(bad)

    def test_retained_single_sfr_and_spaces(self):
        lines = Path(__file__).with_name('retained_sfr_single.txt').read_text().splitlines(keepends=True)
        def parse(text, sequence, address, length=1):
            console = iap.Console.__new__(iap.Console)
            console.sequence = sequence
            def command(commands):
                console.sequence += 1
                return text
            console.command = command
            return console.read('sfr', address, length)
        self.assertEqual(parse(''.join(lines[:6]), 2, 0x80), [255])
        raw = ''.join(lines[6:])
        self.assertEqual(parse(raw, 4, 0xf1), [0xfd])
        fourteen = Path(__file__).with_name('retained_sfr_14.txt').read_text()
        self.assertEqual(parse(fourteen, 40, 0x82, 14), [0xed, 4, 0, 0xc7, 0xc0] + [0] * 8 + [0x80])
        padded = fourteen.replace('ed 04 00 c7 c0', '20 04 00 c7 c0').replace('.....\n', ' ....\n', 1)
        self.assertEqual(parse(padded, 40, 0x82, 14)[0], 0x20)
        for bad in (padded.replace(' ....\n', '....\n', 1), padded.replace(' ....\n', '  ....\n', 1)):
            with self.assertRaises(ValueError):
                parse(bad, 40, 0x82, 14)
        self.assertEqual(parse(raw.replace('fd .', '20  '), 4, 0xf1), [0x20])
        multi = raw.replace('0xf1 0xf1', '0xf1 0xf2').replace('fd .', '20 61  a')
        self.assertEqual(parse(multi, 4, 0xf1, 2), [0x20, 0x61])
        for bad in (multi.replace('20 61  a', '20 61 a'), multi.replace('20 61  a', '20 61   a')):
            with self.assertRaises(ValueError):
                parse(bad, 4, 0xf1, 2)

    def test_multirow_and_bits(self):
        extract = iap.emitted.Firmware.extract
        def response(space, end, rows):
            return (f'echo @@sample\ndump {space} 0x0 {end:#x} 16\n'
                    f'echo __DONE_1__\n@@sample\n{rows}__DONE_1__\n')
        row = '0x00                      ' + '00 ' * 16 + '.' * 16 + '\n'
        last = '0x10                      01 .\n'
        log = response('iram', 16, row + last)
        self.assertEqual(extract(log, 'sample', 0, 17, console_space='iram', terminal='__DONE_1__'), [0] * 16 + [1])
        for bad in (log.replace(last, ''), log.replace('0x10 ', '0x11 ')):
            with self.assertRaises(ValueError):
                extract(bad, 'sample', 0, 17, console_space='iram', terminal='__DONE_1__')
        bits = response('bits', 1, '0x00                      0 1 ..\n')
        self.assertEqual(extract(bits, 'sample', 0, 2, console_space='bits', terminal='__DONE_1__'), [0, 1])

    def test_retained_padded_final_row(self):
        log = Path(__file__).with_name('retained_read23.txt').read_text()
        extract = iap.emitted.Firmware.extract
        def parse(text):
            return extract(text, 'read23', 0x48, 56, console_space='iram', terminal='__DONE_24__')
        self.assertEqual(parse(log), [0xa7] * 56)
        changed = log.replace('0x78                      a7', '0x78                      a8')
        self.assertEqual(parse(changed), [0xa7] * 48 + [0xa8] + [0xa7] * 7)
        lines = log.splitlines(keepends=True)
        final = lines[7]
        for bad in (
            log.replace('a7                         ........', 'a7                        ........'),
            log.replace('a7                         ........', 'a7                          ........'),
            log.replace(lines[4], lines[4].replace(' ................', '                         ................')),
            log.replace('0x78 ', '0x79 '),
            log.replace(final, final.replace('a7 ', '', 1)),
            log.replace(final, final.replace('a7 ', 'a7 a7 ', 1)),
            log.replace(final, final.replace('a7 a7 ', '31 30 ', 1)),
            log.replace(lines[5], ''),
            log.replace(lines[5], lines[5] + lines[5]),
            log.replace(lines[4] + lines[5], lines[5] + lines[4]),
            log.replace('........\n__DONE_24__', '.......X\n__DONE_24__'),
            log.replace(final, 'chatter\n' + final),
            log.replace(final, '__DONE_24__\n' + final),
            log.rsplit('__DONE_24__\n', 1)[0],
            log.rsplit('__DONE_24__\n', 1)[0] + '__DONE_25__\n',
            log.replace('@@read23\n0x48', '@@read23\n@@read23\n0x48'),
            log + 'chatter\n',
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse(bad)
        single = RESPONSE.replace('37 01234567', '37                         01234567')
        with self.assertRaises(ValueError):
            self.read_response(single)
        bits = ('echo @@sample\ndump bits 0x0 0x17 16\necho __DONE_1__\n@@sample\n'
                + '0x00  ' + '0 ' * 16 + '.' * 16 + '\n'
                + '0x10  ' + '0 ' * 8 + ' ' * 24 + '.' * 8 + '\n__DONE_1__\n')
        with self.assertRaises(ValueError):
            extract(bits, 'sample', 0, 24, console_space='bits', terminal='__DONE_1__')

    def test_early_terminal_poison_console(self):
        console = iap.Console.__new__(iap.Console)
        console.sequence, console.log = 6, ''
        console.process = SimpleNamespace(stdin=io.BytesIO(), stdout=SimpleNamespace(fileno=lambda: 4))
        early = b'echo @@read6\ndump iram 0x0 0x7 16\necho __DONE_7__\n@@read6\n__DONE_7__\n'
        with patch.object(iap.select, 'select', return_value=([console.process.stdout], [], [])), \
             patch.object(iap.os, 'read', return_value=early):
            with self.assertRaises(ValueError):
                console.read('iram', 0, 8)
            with self.assertRaisesRegex(RuntimeError, 'unusable'):
                console.command('state')

    def test_rejects_malformed_responses(self):
        row = '0x00                      30 31 32 33 34 35 36 37 01234567\n'
        for bad in (
            RESPONSE.replace('__DONE_7__\n', '__DONE_8__\n', 1),
            RESPONSE.rsplit('__DONE_7__\n', 1)[0],
            RESPONSE.replace('__DONE_7__\n', '__DONE_8__\n', 2),
            RESPONSE.replace('@@read6\n' + row, '@@read6\n@@read6\n' + row),
            RESPONSE.replace(row, ''),
            RESPONSE.replace(row, '0x00                      30 31 32 33 0123\n'),
            RESPONSE.replace(row, row + row),
            RESPONSE.replace('0x00                      ', '0x01                      '),
            RESPONSE.replace('30 31', 'zz 31'),
            RESPONSE.replace('01234567', '0123456X'),
            RESPONSE.replace(row, 'diagnostic\n' + row),
            RESPONSE.replace('__DONE_7__\n', '__DONE_7__\nchatter\n', 1),
            RESPONSE + 'chatter\n',
            'chatter\n' + RESPONSE,
            RESPONSE.replace('dump iram 0x0 0x7 16', 'dump iram 0x0 0x8 16'),
            RESPONSE.replace('@@read6\n' + row, '@@read6\ndump iram 0x0 0x7 16\n' + row),
            RESPONSE.replace(row, row + 'diagnostic\n'),
            RESPONSE.replace('echo __DONE_7__\n', '__DONE_7__\n'),
        ):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.read_response(bad)


if __name__ == '__main__':
    unittest.main()
