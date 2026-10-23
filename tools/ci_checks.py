#!/usr/bin/env python3
"""Run repository Python and shell syntax checks without executing source."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def tracked_files(root: Path = ROOT) -> list[Path]:
    result = subprocess.run(
        ['git', 'ls-files', '-z'], cwd=root, check=True, stdout=subprocess.PIPE
    )
    paths = [root / path.decode('utf-8') for path in result.stdout.split(b'\0') if path]
    # Include these newly added checks before their first commit as well.
    paths.extend(path for name in ('tools/ci_checks.py', 'tools/test_ci_checks.py')
                 if (path := root / name).is_file() and path not in paths)
    return paths


def check_python(paths: list[Path], root: Path = ROOT) -> list[str]:
    errors = []
    for path in paths:
        if path.suffix != '.py' or not path.is_file():
            continue
        try:
            compile(path.read_bytes(), path.as_posix(), 'exec')
        except (SyntaxError, UnicodeDecodeError) as error:
            errors.append(f'{path.relative_to(root)}: {error}')
    return errors


def check_shell(paths: list[Path], root: Path = ROOT) -> list[str]:
    errors = []
    for path in paths:
        if path.suffix != '.sh' or not path.is_file():
            continue
        result = subprocess.run(['bash', '-n', str(path)], cwd=root,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode:
            errors.append(f'{path.relative_to(root)}: {result.stderr.strip()}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT,
                        help='Repository root (defaults to this checkout)')
    args = parser.parse_args()
    root = args.root.resolve()
    paths = tracked_files(root)
    errors = check_python(paths, root) + check_shell(paths, root)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Syntax checks passed for {sum(p.suffix == ".py" for p in paths)} repository Python files '
          f'and {sum(p.suffix == ".sh" for p in paths)} repository shell files.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
