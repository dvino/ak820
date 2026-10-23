"""Validate a version tag and emit GitHub step outputs; no Git or network use."""
from __future__ import annotations

import argparse
import re

NUMBER = r'(?:0|[1-9][0-9]*)'
PRERELEASE = r'(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)'
TAG = re.compile(
    rf'v{NUMBER}\.{NUMBER}\.{NUMBER}'
    rf'(?:-({PRERELEASE}(?:\.{PRERELEASE})*))?'
    r'(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?'
)


def release_values(tag: str) -> dict:
    match = TAG.fullmatch(tag)
    if match is None:
        raise ValueError('Expected a SemVer tag such as v0.6.0 or v0.6.0-rc.1')
    return {'tag': tag, 'prerelease': match.group(1) is not None}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tag')
    args = parser.parse_args(argv)
    try:
        result = release_values(args.tag)
    except ValueError as error:
        parser.error(str(error))
    print('tag=' + result['tag'])
    print('prerelease=' + str(result['prerelease']).lower())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
