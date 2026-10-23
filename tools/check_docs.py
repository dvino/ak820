"""Check public documentation links and translation pairs, entirely offline."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = [ROOT / 'README.md', ROOT / 'CONTRIBUTING.md']
PUBLIC += sorted((ROOT / 'docs').glob('*.md'))
PUBLIC += sorted((ROOT / 'docs/ru').glob('*.md'))


def main():
    failures = []
    for path in PUBLIC:
        text = path.read_text(encoding='utf-8')
        first = text.splitlines()[0]
        russian = path.parent.name == 'ru'
        expected = 'English source of truth:' if russian else 'Русский перевод:'
        if not first.startswith(expected):
            failures.append(f'{path.relative_to(ROOT)}: missing language link at top')
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\s]+)\)', text):
            if re.match(r'\w+:', target) or target.startswith('#'):
                continue
            local = (path.parent / target.split('#')[0]).resolve()
            if not local.is_relative_to(ROOT) or not local.exists():
                failures.append(f'{path.relative_to(ROOT)}: broken link {target}')
    for failure in failures:
        print('FAIL', failure)
    print(f'{len(PUBLIC)} public documents; {len(failures)} failures')
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
