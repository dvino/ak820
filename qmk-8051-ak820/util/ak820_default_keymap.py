#!/usr/bin/env python3
"""Compile current defaults twice; only the final object may enter the link."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from ak820_build_inputs import dependency_paths, input_snapshot


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def literal_block(assembly, symbol):
    """Accept only SDCC literal byte data in the named CONST symbol."""
    lines = assembly.splitlines()
    matches = [i for i, line in enumerate(lines) if line.strip() == symbol + ':']
    if len(matches) != 1:
        raise ValueError('Missing or duplicate symbol: ' + symbol)
    start = matches[0]
    area = next((line.strip() for line in reversed(lines[:start]) if line.strip().startswith('.area ')), '')
    if not re.fullmatch(r'\.area\s+CONST\s+\(CODE\)', area):
        raise ValueError('Expected CONST CODE: ' + symbol)
    result = []
    for line in lines[start + 1:]:
        code = line.split(';', 1)[0].strip()
        if not code:
            continue
        if re.fullmatch(r'[_A-Za-z]\w*:', code) or code.startswith('.area '):
            break
        match = re.fullmatch(r'\.(?:byte|db)\s+(#0x[0-9a-fA-F]{2}(?:\s*,\s*#0x[0-9a-fA-F]{2})*)', code)
        if not match:
            raise ValueError('Unsupported constant directive: ' + code)
        result.extend(int(value.strip()[1:], 16) for value in match[1].split(','))
    if not result:
        raise ValueError('Empty symbol: ' + symbol)
    return result


def encode(raw, metadata):
    if metadata != [16, 8, 2, 2, 0, 1] or len(raw) != 512:
        raise ValueError('Unsupported dimensions/count/word size/NO/TRNS')
    words = [raw[i] | raw[i+1] << 8 for i in range(0, len(raw), 2)]
    classes, payload, offsets = [], [], []
    for row in range(32):
        offsets.append(len(payload))
        packed = [0, 0]
        for col, value in enumerate(words[row*8:row*8+8]):
            kind = value if value < 2 else (2 if value <= 255 else 3)
            packed[col//4] |= kind << ((col % 4)*2)
            if kind >= 2:
                payload.append(value & 255)
            if kind == 3:
                payload.append(value >> 8)
        classes.extend(packed)
    if len(payload) > 255:
        raise ValueError('Payload exceeds uint8 offsets')
    for row in range(32):
        pos = offsets[row]
        for col in range(8):
            kind = (classes[row*2+col//4] >> ((col%4)*2)) & 3
            if kind < 2:
                value = kind
            else:
                if pos + kind - 1 > len(payload):
                    raise ValueError('Payload read exceeds boundary')
                value = payload[pos] | (payload[pos+1] << 8 if kind == 3 else 0)
                pos += kind-1
            if value != words[row*8+col]:
                raise ValueError('Roundtrip mismatch')
        if pos != (offsets[row+1] if row < 31 else len(payload)):
            raise ValueError('Row end mismatch')
    return classes, payload, offsets


def generate(assembly):
    arrays = encode(literal_block(assembly, '_keymaps'), literal_block(assembly, '_ak820_default_metadata'))
    text = '#define AK820_DEFAULT_LAYERS 2\n'
    for name, values in zip(('classes', 'payload', 'offsets'), arrays):
        text += 'static const uint8_t __code ak820_default_' + name + '[] = {' + ','.join(map(str, values)) + '};\n'
        text += '_Static_assert(sizeof(ak820_default_' + name + ') == ' + str(len(values)) + ', "default table size");\n'
    text += '_Static_assert(MATRIX_ROWS == 16 && MATRIX_COLS == 8 && sizeof(uint16_t) == 2 && KC_NO == 0 && KC_TRNS == 1, "default table configuration");\n'
    return text


def reject_phase_overrides(argv):
    # The extraction phase belongs exclusively to this wrapper, including =0.
    if any(re.search(r'(?:-D|-U|^)(?:AK820_DEFAULT_KEYMAP_EXTRACT)(?:=|$|,)', arg)
           or arg == 'AK820_DEFAULT_KEYMAP_EXTRACT' for arg in argv):
        raise ValueError('Caller cannot override private extraction phase')


def verify_final(assembly, bootstrap):
    for symbol in ('_keymaps', '_ak820_default_metadata'):
        if re.search(r'^' + re.escape(symbol) + r':', assembly, re.MULTILINE):
            raise ValueError('Bootstrap allocation remains in final assembly: ' + symbol)
    expected = encode(literal_block(bootstrap, '_keymaps'),
                      literal_block(bootstrap, '_ak820_default_metadata'))
    for name, values in zip(('classes', 'payload', 'offsets'), expected):
        if literal_block(assembly, '_ak820_default_' + name) != values:
            raise ValueError('Final default table differs: ' + name)


def compile_current(argv):
    reject_phase_overrides(argv)
    compiler = Path(shutil.which(argv[0]) or argv[0]).resolve()
    root = Path(__file__).resolve().parents[1]
    toolchain = compiler.parents[1]
    if '-c' not in argv or argv.count('-o') != 1 or '--model-large' not in argv:
        raise ValueError('Unsupported compiler invocation')
    if '4.6.0' not in subprocess.check_output([str(compiler), '--version'], text=True):
        raise ValueError('Default compression requires SDCC 4.6.0')
    output = Path(argv[argv.index('-o') + 1])
    # obj_TARGET/quantum/output.o -> BUILD/default-keymap (not object ASM manifest).
    directory = output.parent.parent.parent / 'default-keymap'
    directory.mkdir(parents=True, exist_ok=True)
    include = directory / 'ak820_default_keymap.inc'
    include.unlink(missing_ok=True)
    (directory/'generation.json').unlink(missing_ok=True)
    output.unlink(missing_ok=True)
    output.with_suffix('.rel').unlink(missing_ok=True)
    bootstrap, dep = directory/'bootstrap.asm', directory/'bootstrap.d'
    before = input_snapshot(root, toolchain)
    for path in (root/'.build').rglob('*'):
        if path.is_file() and path.suffix in {'.h', '.inc'}:
            before[path.resolve()] = sha(path)
    wrapper_sha, compiler_sha = sha(__file__), sha(compiler)
    base = [str(compiler)] + argv[1:]
    bootstrap_cmd = []
    skip = False
    for item in base:
        if skip:
            skip = False
            continue
        if item == '-o':
            skip = True
        elif item == '-c':
            bootstrap_cmd.append('-S')
        elif item.startswith('-Wp,-MD,-MF,'):
            bootstrap_cmd.append('-Wp,-MD,-MF,' + str(dep))
        else:
            bootstrap_cmd.append(item)
    bootstrap_cmd += ['-DAK820_DEFAULT_KEYMAP_EXTRACT', '-o', str(bootstrap)]
    dependency_cmd = bootstrap_cmd[:-2]
    dependency_cmd[dependency_cmd.index('-S')] = '-E'
    subprocess.run(dependency_cmd, check=True, stdout=subprocess.DEVNULL)
    paths = dependency_paths(dep, root)
    # Generated QMK headers already exist but are excluded by the broad source
    # snapshot. Hash their exact discovered closure before the bootstrap compile.
    for path in paths:
        if path not in before and '.build' in path.parts:
            before[path] = sha(path)
    subprocess.run(bootstrap_cmd, check=True)
    if dependency_paths(dep, root) != paths:
        raise ValueError('Dependency closure changed during generation')
    def verify():
        if sha(__file__) != wrapper_sha or sha(compiler) != compiler_sha:
            raise ValueError('Generator/compiler changed during compilation')
        for path in paths:
            if before.get(path) != sha(path):
                raise ValueError('Source changed during default generation: ' + str(path))
    verify()
    generated = generate(bootstrap.read_text())
    temporary = include.with_suffix('.tmp')
    temporary.write_text(generated)
    os.replace(temporary, include)
    final_cmd = base + ['-I' + str(directory)]
    final_dep = directory/'final-discovery.d'
    # Freeze generated headers before discovery as well: a final-only conditional
    # dependency must not silently become the current input after an intervening edit.
    final_before = dict(before)
    final_before[include.resolve()] = sha(include)
    final_discovery = []
    skip = False
    for item in final_cmd:
        if skip:
            skip = False
            continue
        if item == '-o':
            skip = True
        elif item == '-c':
            final_discovery.append('-E')
        elif item.startswith('-Wp,-MD,-MF,'):
            final_discovery.append('-Wp,-MD,-MF,' + str(final_dep))
        else:
            final_discovery.append(item)
    try:
        subprocess.run(final_discovery, check=True, stdout=subprocess.DEVNULL)
        final_paths = dependency_paths(final_dep, root)
        def verify_final_inputs():
            verify()
            for path in final_paths:
                if final_before.get(path) != sha(path):
                    raise ValueError('Source changed during final compilation: ' + str(path))
        verify_final_inputs()
        subprocess.run(final_cmd, check=True)
        actual_dep = next(Path(arg[len('-Wp,-MD,-MF,'):]) for arg in final_cmd
                          if arg.startswith('-Wp,-MD,-MF,'))
        if dependency_paths(actual_dep, root) != final_paths:
            raise ValueError('Final dependency closure changed during compilation')
        verify_final_inputs()
        verify_final(output.with_suffix('.asm').read_text(), bootstrap.read_text())
    except BaseException:
        include.unlink(missing_ok=True)
        output.unlink(missing_ok=True)
        output.with_suffix('.rel').unlink(missing_ok=True)
        raise
    report = {'dependency_command': dependency_cmd, 'bootstrap_command': bootstrap_cmd, 'final_command': final_cmd,
              'compiler_sha256': compiler_sha, 'generator_sha256': wrapper_sha,
              'dependencies': {str(path): sha(path) for path in sorted(paths)},
              'bootstrap_sha256': sha(bootstrap), 'dependency_sha256': sha(dep),
              'include_sha256': sha(include),
              'final_dependency_command': final_discovery,
              'final_dependencies': {str(path): final_before[path] for path in sorted(final_paths)},
              'final_dependency_sha256': sha(final_dep),
              'generated_dependency_difference': [str(include.resolve())],
              'final_only_dependencies': [str(path) for path in sorted(final_paths - paths)],
              'bootstrap_only_dependencies': [str(path) for path in sorted(paths - final_paths)],
              'final_tables_verified': True}
    (directory/'generation.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    compile_current(sys.argv[1:])
