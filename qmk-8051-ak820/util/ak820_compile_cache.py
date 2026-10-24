#!/usr/bin/env python3
"""Content-addressed SDCC TU cache; the original compiler runs on misses.

Keys bind compiler/preprocessor bytes, full preprocessed TU and all compiler
options. Only preprocessor-only arguments are excluded from the options key.
Dependencies are freshly generated on every invocation, including cache hits.
No link, DCE, assembler or outlining result is cached here.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SUFFIXES = ('.asm', '.rel', '.lst', '.sym')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def split_options(argv):
    """Return the preprocessing command and code-generation options key."""
    pp, code, output = [], [], None
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ('-o', '--output'):
            output = Path(argv[index + 1])
            index += 2
            continue
        if arg == '-c':
            index += 1
            continue
        if arg in ('-D', '-I', '--include'):
            pp.extend(argv[index:index + 2])
            index += 2
            continue
        pp.append(arg)
        if not (arg.startswith(('-D', '-I', '-Wp,'))):
            code.append(arg)
        index += 1
    if output is None or output.suffix != '.rel' or not any(arg.endswith('.c') for arg in argv):
        raise ValueError('Cache accepts only explicit C-to-REL compilation')
    # Output paths appear in generated assembly and cannot be normalized away.
    code.extend(['-o', str(output)])
    return ['-E', *pp], code, output


def run(compiler, cache, argv):
    compiler, cache = Path(compiler).resolve(), Path(cache).resolve()
    if '-c' not in argv:
        return subprocess.call([str(compiler), *argv])
    pp_args, options, output = split_options(argv)
    before = subprocess.run([str(compiler), *pp_args], stdout=subprocess.PIPE)
    if before.returncode:
        return before.returncode
    identity = {'compiler': sha(compiler), 'preprocessor': sha(compiler.with_name('sdcpp')),
                'options': options, 'preprocessed_sha256': hashlib.sha256(before.stdout).hexdigest()}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    cache.mkdir(parents=True, exist_ok=True)
    entry = cache / key
    if entry.is_dir():
        record = json.loads((entry / 'entry.json').read_text())
        if record['input'] != identity or set(record['outputs']) != set(SUFFIXES):
            raise ValueError('Malformed compiler cache entry')
        for suffix, expected in record['outputs'].items():
            if sha(entry / ('object' + suffix)) != expected:
                raise ValueError('Compiler cache output hash mismatch')
        for suffix in SUFFIXES:
            shutil.copyfile(entry / ('object' + suffix), output.with_suffix(suffix))
        output.with_suffix('.cache.json').write_text(json.dumps({'key': key, 'input': identity, 'outputs': record['outputs'], 'hit': True, 'argv': argv}, sort_keys=True))
        return 0
    result = subprocess.call([str(compiler), *argv])
    if result:
        return result
    after = subprocess.run([str(compiler), *pp_args], stdout=subprocess.PIPE)
    if after.returncode or before.stdout != after.stdout:
        raise ValueError('Preprocessed TU changed during compilation')
    with tempfile.TemporaryDirectory(prefix='pending-', dir=cache) as temporary:
        target = Path(temporary)
        hashes = {}
        for suffix in SUFFIXES:
            source = output.with_suffix(suffix)
            if not source.is_file():
                raise ValueError('Compiler omitted cache output: ' + suffix)
            shutil.copyfile(source, target / ('object' + suffix))
            hashes[suffix] = sha(source)
        (target / 'entry.json').write_text(json.dumps({'input': identity, 'outputs': hashes}, sort_keys=True))
        # Parallel Make invocations for the same TU are allowed only if bytes agree.
        try:
            os.rename(target, entry)
        except FileExistsError:
            existing = json.loads((entry / 'entry.json').read_text())
            if existing != {'input': identity, 'outputs': hashes}:
                raise ValueError('Nondeterministic compiler cache collision')
    output.with_suffix('.cache.json').write_text(json.dumps({'key': key, 'input': identity, 'outputs': hashes, 'hit': False, 'argv': argv}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(run(sys.argv[1], sys.argv[2], sys.argv[3:]))
