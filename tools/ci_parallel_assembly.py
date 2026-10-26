#!/usr/bin/env python3
"""Prewarm in-memory validation, then run the unchanged CI release assembler.

No qualification or release gate is skipped. Each parent inspection checks its
current input snapshot before reusing a worker's successful transform replay.
"""
from __future__ import annotations

import argparse
import copy
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from pathlib import Path
import re
import sys

import build_ci_release as ci
import configure_firmware as configured


def _workers(value):
    try:
        count = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError('must be an integer from 1 to 4') from None
    if not 1 <= count <= 4:
        raise argparse.ArgumentTypeError('must be an integer from 1 to 4')
    return count


def _prewarm(key):
    """Export only the requested entry after a complete successful inspection."""
    configured._PASS30_CACHE.pop(key, None)
    configured.inspect(*key)
    return key, configured._PASS30_CACHE.get(key)


def _accept(expected, response):
    if not isinstance(response, tuple) or len(response) != 2 or response[0] != expected:
        raise ValueError('Validation worker returned an unexpected build key')
    entry = response[1]
    if entry is None:
        configured._PASS30_CACHE.pop(expected, None)
        return
    def digest(value):
        return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None
    if not isinstance(entry, tuple) or len(entry) != 2 or not digest(entry[0]):
        raise ValueError('Validation worker returned an invalid cache digest')
    result = entry[1]
    fields = {'parameter_spills', 'register_saves', 'tail_share'}
    if (not isinstance(result, dict) or set(result) != {'contract', 'reports'}
            or result['contract'] != 'ak820-audited-pass30-1'
            or not isinstance(result['reports'], dict) or set(result['reports']) != fields
            or not all(digest(value) for value in result['reports'].values())):
        raise ValueError('Validation worker returned an invalid replay result')
    configured._PASS30_CACHE[expected] = copy.deepcopy(entry)


def _delegate(argv):
    previous = sys.argv
    try:
        sys.argv = [previous[0], *argv]
        return ci.main()
    finally:
        sys.argv = previous


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument('--validation-workers', type=_workers, default=4,
                        help='Parallel cold inspections, from 1 to 4 (default: 4)')
    options, forwarded = parser.parse_known_args(argv)
    if '--help' in forwarded or '-h' in forwarded:
        parser.print_help()
        return _delegate(forwarded)
    # Extract only the paths needed for prewarming. The original parser still
    # receives every original argument except this wrapper's worker option.
    paths = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    paths.add_argument('--all-profiles', action='store_true')
    paths.add_argument('--builds-root', type=Path)
    paths.add_argument('--toolchain', type=Path, default=Path('toolchains/sdcc-4.6.0'))
    selected, _ = paths.parse_known_args(forwarded)
    if not selected.all_profiles:
        parser.error('parallel assembly requires --all-profiles')
    if selected.builds_root is None:
        # Preserve the original parser's required-input diagnostic.
        return _delegate(forwarded)
    def rooted(path):
        return (path if path.is_absolute() else ci.ROOT / path).resolve()
    toolchain = rooted(selected.toolchain)
    keys = [(rooted(selected.builds_root) / name, toolchain)
            for name in ci.release_profile_names()]
    keys = [(build.resolve(), tools) for build, tools in keys]
    if options.validation_workers == 1:
        for key in keys:
            _accept(key, _prewarm(key))
    else:
        with ProcessPoolExecutor(max_workers=options.validation_workers,
                                 mp_context=multiprocessing.get_context('spawn')) as pool:
            futures = [(key, pool.submit(_prewarm, key)) for key in keys]
            for key, future in futures:
                _accept(key, future.result())
    return _delegate(forwarded)


if __name__ == '__main__':
    main()
