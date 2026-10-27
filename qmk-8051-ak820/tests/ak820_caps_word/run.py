#!/usr/bin/env python3
"""Exercise the real Caps Word state/handler with host timer/report stubs.

Only includes are removed from the two production C files. Firmware headers
define keycodes, keyrecord_t and timer expiry; an empty platform timer shim
avoids hardware headers. This tests host logic, not the SDCC/XDATA ABI or USB.
The second profile enables tapping to check the otherwise dormant LT bounds.
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=ROOT)
    parser.add_argument('--handler', type=Path, help='Override handler source for a negative control')
    parser.add_argument('--profile', choices=('active', 'tapping'), action='append')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.source_root.resolve()
    sources = [root / 'quantum/caps_word.c', (args.handler or root / 'quantum/process_keycode/process_caps_word.c').resolve()]
    fragments = [re.sub(r'^#\s*include[^\n]*\n', '', path.read_text(), flags=re.M) for path in sources]
    results = []
    with tempfile.TemporaryDirectory(prefix='ak820-caps-word-') as temp:
        work = Path(temp)
        (work / '_timer.h').write_text('#define FAST_TIMER_T_SIZE 16\n')
        (work / 'host.c').write_text((HERE / 'harness.c').read_text().replace('/* ACTUAL_CAPS_WORD */', '\n'.join(fragments)))
        for profile in args.profile or ('active', 'tapping'):
            binary = work / profile
            command = [os.environ.get('CC', 'cc'), '-std=gnu11', '-O1', '-g', '-Wall', '-Wextra',
                       '-Werror', '-Wno-unused-parameter', '-Wno-unknown-pragmas',
                       '-Wno-old-style-declaration', '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
                       '-DREPEAT_KEY_ENABLE',
                       *(['-DTEST_ACTION_TAPPING'] if profile == 'tapping' else []),
                       '-include', str(root / 'keyboards/ajazz/ak820/config.h'),
                       *['-I' + str(path) for path in (work, root / 'quantum', root / 'quantum/keymap_extras', root / 'quantum/sequencer',
                                                     root / 'platforms', root / 'tmk_core/protocol', root)],
                       str(work / 'host.c'), '-o', str(binary)]
            subprocess.run(command, check=True)
            env = os.environ.copy()
            env['ASAN_OPTIONS'] = 'detect_leaks=0'
            result = subprocess.run([str(binary)], env=env, text=True, capture_output=True)
            print(profile + ': ' + result.stdout.strip() + result.stderr.strip(), flush=True)
            results.append({'profile': profile, 'pass': result.returncode == 0, 'return_code': result.returncode,
                            'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()})
    paths = sources + [root / 'keyboards/ajazz/ak820/config.h', HERE / 'harness.c', HERE / 'run.py']
    report = {'pass': all(item['pass'] for item in results), 'level': 'Host C with ASan/UBSan; no SDCC ABI or hardware proof',
              'tests': results, 'source_sha256': {str(p.relative_to(root) if p.is_relative_to(root) else p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(0 if report['pass'] else 1)


if __name__ == '__main__':
    main()
