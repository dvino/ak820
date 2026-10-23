#!/usr/bin/env python3
"""Host CPU regression for actual ak820_boot.c, without production test hooks.

Requires SDCC and s51 on PATH, or AK820_SDCC_BIN pointing at their directory.
The generic CPU model does not emulate flash. Marker bytes are seeded as the
readback result, and tests check the erase request, reset path and IE restore.
No physical device interface or firmware update command is used.
"""
import os
from pathlib import Path
import re
import select
import shutil
import subprocess
import tempfile
import time
import unittest

if os.name == 'posix':
    import pty
else:
    pty = None

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


class BootloaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if pty is None:
            raise unittest.SkipTest('The SDCC/8051 boot regression requires a POSIX host (for example Linux or WSL)')
        bindir = os.environ.get('AK820_SDCC_BIN')
        sdcc = str(Path(bindir) / 'sdcc') if bindir else shutil.which('sdcc')
        cls.sim = str(Path(bindir) / 's51') if bindir else shutil.which('s51')
        if not sdcc or not cls.sim:
            raise unittest.SkipTest('Set AK820_SDCC_BIN to run the SDCC/8051 boot regression')
        cls.temp = tempfile.TemporaryDirectory(prefix='ak820-boot-cpu-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.work = Path(cls.temp.name)
        board = ROOT / 'keyboards/ajazz/ak820'
        flags = ['-mmcs51', '--model-large', '--std-sdcc11', '--opt-code-size',
                 '--iram-size', '0x100', '--xram-size', '0x0c00',
                 '-I' + str(board), '-I' + str(ROOT / 'lib/ch555')]
        cls.image = cls.work / 'boot_test.ihx'
        commands = [
            [sdcc, *flags, '-c', str(board / 'ak820_boot.c'), '-o', str(cls.work / 'boot.rel')],
            [sdcc, *flags, '-c', str(HERE / 'boot_harness.c'), '-o', str(cls.work / 'harness.rel')],
            [sdcc, *flags, '--code-loc', '0x3000', '--xram-loc', '0x0410',
             str(cls.work / 'harness.rel'), str(cls.work / 'boot.rel'), '-o', str(cls.image)],
        ]
        for command in commands:
            subprocess.run(command, cwd=cls.work, check=True, capture_output=True, text=True)
        cls.symbols = {name: int(address, 16) for address, name in re.findall(
            r'^C:\s+([0-9A-Fa-f]{8})\s+(\S+)', cls.image.with_suffix('.map').read_text(), re.M)}
        code = {}
        for line in cls.image.read_text().splitlines():
            record = bytes.fromhex(line[1:])
            assert len(record) == record[0] + 5 and sum(record) % 256 == 0
            if record[3] == 0:
                address = int.from_bytes(record[1:3], 'big')
                code.update({address + i: value for i, value in enumerate(record[4:-1])})
            else:
                assert record[3] == 1, 'Unexpected harness address mode'
        # mcu_reset's terminal loop follows its actual safe-mode/reset writes.
        cls.reset_stop = cls.symbols['_bootloader_jump'] - 2
        assert cls.reset_stop > cls.symbols['_mcu_reset']
        assert bytes(code[a] for a in range(cls.reset_stop, cls.reset_stop + 2)) == b'\x80\xfe'

    def cpu(self, nvm_good, marker, erase_allowed=True):
        stops = {self.reset_stop: 'reset', self.symbols['_test_returned']: 'returned'}
        setup = [
            'fill xram 0 0xffff 0', 'fill iram 0 0xff 0',
            'set memory sfr 0x81 0x70', 'set memory sfr 0xa8 0x82',
            'set memory sfr 0xb1 2', f'set memory sfr 0x86 {0x40 if erase_allowed else 0}',
            f'set memory xram 0x0400 {int(nvm_good)} 0 0',
            'set memory rom 0x27c0 ' + ' '.join(str(v) for v in marker),
            *(f'break {address}' for address in stops), f'run {self.symbols["_main"]}',
        ]
        argv = [self.sim, '-q', '-c', '-']
        for command in setup:
            argv += ['-e', command]
        argv.append(str(self.image))
        master, slave = pty.openpty()
        proc = subprocess.Popen(argv, stdin=slave, stdout=slave, stderr=slave)
        os.close(slave)
        raw = bytearray()
        deadline = time.monotonic() + 10
        stopped = None
        try:
            while time.monotonic() < deadline:
                if select.select([master], [], [], .1)[0]:
                    try:
                        block = os.read(master, 65536)
                    except OSError:
                        break
                    if not block:
                        break
                    raw.extend(block)
                    if stopped is None:
                        for address, outcome in stops.items():
                            signature = f'F 0x{address:06x}'.encode()
                            if signature in raw:
                                stopped = (signature, outcome)
                                os.write(master, b'dump sfr 0x80 0xbf\ndump xram 0x0400 0x0402\nquit\n')
                                break
                elif proc.poll() is not None:
                    break
            self.assertIsNotNone(stopped, raw.decode(errors='replace'))
            proc.wait(timeout=2)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            os.close(master)
        text = raw.decode(errors='replace').replace('\r', '')
        values = {}
        for address, payload in re.findall(
            r'(?:^|> )0x([0-9a-fA-F]{2,4})\s{2,}((?:[0-9a-fA-F]{2} ?)+)',
            text.split(stopped[0].decode(), 1)[1], re.M):
            values.update({int(address, 16) + i: value for i, value in enumerate(bytes.fromhex(payload))})
        # uCsim formats recognized SFRs (including IE) as named bit fields.
        for address, value in re.findall(
            r'(?:^|> )0x([0-9a-fA-F]{2})\s+\S+:\s+0b[01]{8}\s+0x([0-9a-fA-F]{2})',
            text.split(stopped[0].decode(), 1)[1], re.M):
            values[int(address, 16)] = int(value, 16)
        self.assertEqual(values[0x401], 1, 'Best-effort flush must be attempted once')
        self.assertEqual(values[0x402], int(nvm_good))
        self.assertEqual(values[0x84], 0xc0)
        self.assertEqual(values[0x85], 0x27)
        self.assertEqual(values[0x8e], 0)
        self.assertEqual(values[0x8f], 0x80)
        self.assertEqual(values[0x86], 0xa6 if erase_allowed else 0)
        self.assertEqual(values[0xb1] & 0x08, 0, 'CODE_WE must be closed before return/reset')
        return stopped[1], values

    def test_faulted_and_healthy_storage_allow_reset_after_erased_marker(self):
        for good in (False, True):
            with self.subTest(nvm_good=good):
                outcome, values = self.cpu(good, bytes(4))
                self.assertEqual(outcome, 'reset')
                self.assertEqual(values[0xb1], 0x12)
                self.assertEqual(values[0xa8] & 0x80, 0)

    def test_any_uncleared_marker_byte_blocks_reset_and_restores_ie(self):
        for good in (False, True):
            for offset in range(4):
                with self.subTest(nvm_good=good, marker_byte=offset):
                    marker = bytearray(4)
                    marker[offset] = 1
                    outcome, values = self.cpu(good, marker)
                    self.assertEqual(outcome, 'returned')
                    self.assertEqual(values[0xb1], 2)
                    self.assertEqual(values[0xa8], 0x82)
                    self.assertEqual(values[0xa1], 0)

    def test_denied_erase_with_valid_marker_never_resets(self):
        for good in (False, True):
            with self.subTest(nvm_good=good):
                outcome, values = self.cpu(good, bytes.fromhex('aa5533cc'), False)
                self.assertEqual(outcome, 'returned')
                self.assertEqual(values[0xb1], 2)
                self.assertEqual(values[0xa8], 0x82)


if __name__ == '__main__':
    unittest.main()
