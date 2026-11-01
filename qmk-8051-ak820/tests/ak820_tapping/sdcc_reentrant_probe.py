#!/usr/bin/env python3
"""Check the model-large reentrant-record address-space boundary, not firmware safety."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from configure_firmware import validate_tools


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('toolchain', help='directory containing pinned SDCC 4.6 tools')
    toolchain = validate_tools(parser.parse_args().toolchain)
    compiler = toolchain / 'bin/sdcc'
    with tempfile.TemporaryDirectory(prefix='ak820-ph-abi-') as directory:
        work = Path(directory)
        source = work / 'probe.c'
        common = 'typedef struct { unsigned char data[9]; } record;\nvoid use(record __xdata *p);\n'
        command = [str(compiler), '-mmcs51', '--model-large', '--std-sdcc11', '-S', str(source), '-o', str(work / 'probe.asm')]
        source.write_text(common + 'void seam(void) __reentrant { static __xdata record r; use(&r); }\n')
        control = subprocess.run(command, capture_output=True, text=True)
        assert control.returncode == 0, control.stderr
        source.write_text(common + 'void seam(void) __reentrant { record r; use(&r); }\n')
        probe = subprocess.run(command, capture_output=True, text=True)
        assert probe.returncode != 0, 'automatic record unexpectedly accepted as XDATA'
        assert 'error 78: incompatible types' in probe.stderr, probe.stderr
        assert "near* auto'" in probe.stderr and "__xdata* fixed'" in probe.stderr, probe.stderr
        print('PASS: explicit static XDATA control compiles; reentrant automatic record is a near pointer, not XDATA')
        print('This proves neither reentrancy of static storage nor safety of a firmware seam.')


if __name__ == '__main__':
    main()
