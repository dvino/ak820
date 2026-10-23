#!/usr/bin/env python3
"""Host tests of the production reactive renderer and compact CIE conversion.

No peripheral/device access. Source is compiled with small driver/timer fixtures.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def stripped(path):
    return re.sub(r'^#\s*include[^\n]*\n', '', path.read_text(), flags=re.M)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rgb = ROOT / 'keyboards/ajazz/ak820/ak820_rgb.c'
    color = ROOT / 'quantum/color.c'
    tables = ROOT / 'quantum/led_tables.c'
    reference = ROOT / 'tests/ak820_optimization/fixtures/color_rc4.c'
    config = ROOT / 'keyboards/ajazz/ak820/config.h'
    full = re.search(r'const uint8_t CIE1931_CURVE\[256\].*?\{(.*?)\};', tables.read_text(), re.S)[1]
    body = (HERE / 'harness.c').read_text()
    body = body.replace('/* SLOT MAP */', re.search(r'^#define AK820_RGB_SLOT_MAP (.*)$', config.read_text(), re.M)[1])
    body = body.replace('/* TABLE */', stripped(tables))
    body = body.replace('/* COLOR */', stripped(color))
    body = body.replace('/* REFERENCE TABLE */', 'const uint8_t reference_cie[256] = {' + full + '};')
    body = body.replace('/* REFERENCE COLOR */', reference.read_text().replace('CIE1931_CURVE[', 'reference_cie['))
    body = body.replace('/* RGB */', stripped(rgb))
    with tempfile.TemporaryDirectory(prefix='ak820-rgb-') as td:
        source, binary = Path(td) / 'rgb.c', Path(td) / 'rgb'
        source.write_text(body)
        subprocess.run([os.environ.get('CC', 'gcc'), '-std=gnu11', '-O2', '-g', '-Wall', '-Wextra', '-Werror',
                        '-fsanitize=address,undefined', '-fno-omit-frame-pointer', str(source), '-o', str(binary)], check=True)
        result = subprocess.run([str(binary)], capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        print(result.stdout)
    paths = [rgb, color, tables, reference, config, HERE / 'harness.c', Path(__file__)]
    report = {'pass': True, 'summary': result.stdout.strip(),
              'limits': 'Host production C with fixtures; no SDCC ABI, physical timing, DMA or device validation.',
              'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
