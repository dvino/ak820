#!/usr/bin/env python3
"""Capture the argv executed by the C object recipe; not qualification evidence."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from ak820_build_inputs import dependency_paths, digest


def capture_environment(environ):
    return {name: environ[name] for name in ('PATH', 'SYSTEMROOT', 'WINDIR',
            'AK820_CAPTURE_BUILD_ROOT', 'AK820_CAPTURE_OBJECT_ROOT') if name in environ}


def validate_manifest(root, build, objects, object_root):
    captures = sorted(build.rglob('*.o.compile.json'))
    expected = [(root / name).with_suffix('.o.compile.json') for name in objects]
    if len(set(expected)) != len(expected) or set(captures) != set(expected):
        raise ValueError('Compiler invocation/object manifest mismatch')
    for path in captures:
        capture = json.loads(path.read_text(encoding='utf-8'))
        argv = capture.get('argv')
        environment = capture.get('environment')
        output = str(path.relative_to(root))[:-len('.compile.json')]
        if (not isinstance(environment, dict) or
                environment.get('AK820_CAPTURE_BUILD_ROOT') != str(build.resolve()) or
                environment.get('AK820_CAPTURE_OBJECT_ROOT') != str(object_root.resolve()) or
                not object_root.resolve().is_relative_to(build.resolve()) or
                object_root.resolve() == build.resolve() or
                not path.resolve().is_relative_to(object_root.resolve()) or
                capture.get('cwd') != str(root) or capture.get('exit_code') != 0 or
                not isinstance(argv, list) or len(argv) < 5 or
                not all(isinstance(arg, str) for arg in argv) or
                argv[-2:] != ['-o', output] or not argv[-3].endswith('.c') or
                capture.get('fresh_dependency') != str(Path(output).with_suffix('.d')) or
                '-c' not in argv):
            raise ValueError('Invalid compiler invocation capture: ' + str(path))
    return captures


def validate_default_keymap(captures, build):
    wrappers = [json.loads(path.read_text(encoding='utf-8')) for path in captures
                if json.loads(path.read_text(encoding='utf-8')).get('argv', [])[:3] ==
                ['python3', '-s', 'util/ak820_default_keymap.py']]
    if len(wrappers) != 1:
        raise ValueError('Expected one default-keymap compiler wrapper')
    wrapper = wrappers[0]
    argv, env = wrapper['argv'][3:], wrapper['environment']
    compiler = shutil.which(argv[0], path=env.get('PATH', ''))
    if compiler is None or argv.count('-o') != 1 or argv.count('-c') != 1:
        raise ValueError('Invalid default-keymap compiler invocation')
    directory = build / 'default-keymap'
    base = [str(Path(compiler).resolve())] + argv[1:]
    bootstrap = []
    skip = False
    for arg in base:
        if skip:
            skip = False
        elif arg == '-o':
            skip = True
        elif arg == '-c':
            bootstrap.append('-S')
        elif arg.startswith('-Wp,-MD,-MF,'):
            bootstrap.append('-Wp,-MD,-MF,' + str(directory / 'bootstrap.d'))
        else:
            bootstrap.append(arg)
    bootstrap += ['-DAK820_DEFAULT_KEYMAP_EXTRACT', '-o', str(directory / 'bootstrap.asm')]
    dependency = bootstrap[:-2].copy()
    dependency[dependency.index('-S')] = '-E'
    final = base + ['-I' + str(directory)]
    discovery = []
    skip = False
    for arg in final:
        if skip:
            skip = False
        elif arg == '-o':
            skip = True
        elif arg == '-c':
            discovery.append('-E')
        elif arg.startswith('-Wp,-MD,-MF,'):
            discovery.append('-Wp,-MD,-MF,' + str(directory / 'final-discovery.d'))
        else:
            discovery.append(arg)
    expected = [[str(Path(compiler).resolve()), '--version'], dependency, bootstrap, discovery, final]
    generation = json.loads((build / 'default-keymap/generation.json').read_text(encoding='utf-8'))
    invocations = generation.get('compiler_invocations')
    if (not isinstance(invocations, list) or len(invocations) != len(expected) or
            any(not isinstance(record, dict) or record.get('argv') != command or
                record.get('cwd') != wrapper['cwd'] or record.get('environment') != env or
                record.get('exit_code') != 0 or
                (index and record.get('fresh_dependency') != next(
                    (arg.removeprefix('-Wp,-MD,-MF,') for arg in command if arg.startswith('-Wp,-MD,-MF,')), None))
                for index, (record, command) in enumerate(zip(invocations, expected)))):
        raise ValueError('Default-keymap nested compiler capture mismatch')
    root = Path(wrapper['cwd'])
    primary = argv[argv.index('-o') - 1]
    target = Path(argv[argv.index('-o') + 1]).name
    for filename, hash_key, paths_key in (
            ('bootstrap.d', 'dependency_sha256', 'dependencies'),
            ('final-discovery.d', 'final_dependency_sha256', 'final_dependencies')):
        dep = build / 'default-keymap' / filename
        paths = dependency_paths(dep, root, target=target, primary=primary)
        if (generation.get(hash_key) != digest(dep) or
                generation.get(paths_key) != {str(path): digest(path) for path in sorted(paths)}):
            raise ValueError('Default-keymap dependency evidence mismatch: ' + filename)


def main(argv):
    if len(argv) < 6 or argv[3] != '--' or not argv[1] or not argv[2]:
        raise ValueError('Expected capture path, build root, output root, --, and compiler command')
    record, command = Path(argv[0]), argv[4:]
    build, object_dir = Path(argv[1]).resolve(), Path(argv[2]).resolve()
    object_path = str(record)[:-len('.compile.json')]
    dependency = str(Path(object_path).with_suffix('.d'))
    trusted_build = os.environ.get('AK820_CAPTURE_BUILD_ROOT')
    trusted_objects = os.environ.get('AK820_CAPTURE_OBJECT_ROOT')
    if (not trusted_build or not trusted_objects or not Path(trusted_build).is_absolute() or
            not Path(trusted_objects).is_absolute() or Path(trusted_build).resolve() != build or
            Path(trusted_objects).resolve() != object_dir or
            not str(record).endswith('.o.compile.json') or not build.is_dir() or
            not object_dir.is_relative_to(build) or object_dir == build or
            not Path(object_path).resolve().is_relative_to(object_dir) or
            not record.resolve().is_relative_to(object_dir) or
            not Path(dependency).resolve().is_relative_to(object_dir)):
        raise ValueError('Invalid compiler build or output root')
    # Keep the exclusive claim on failure or interruption: the compiler may still run.
    with record.open('x', encoding='utf-8') as output:
        capture = {'cwd': os.getcwd(), 'argv': command, 'environment': capture_environment(os.environ),
                   'exit_code': None}
        json.dump(capture, output, sort_keys=True)
        output.write('\n')
        output.flush()
        generated_before = {}
        if command[0] == 'sdcc' or command[:3] == ['python3', '-s', 'util/ak820_default_keymap.py']:
            if command[-2:] != ['-o', object_path] or [x for x in command if x.startswith('-Wp,-MD,-MF,')] != ['-Wp,-MD,-MF,' + dependency]:
                raise ValueError('Compiler dependency/output mismatch')
            for p in build.rglob('*'):
                if p.is_file() and p.suffix in ('.c', '.h', '.inc'):
                    if not p.resolve().is_relative_to(build):
                        raise ValueError('Generated compiler input escapes build root')
                    generated_before[str(p.resolve())] = digest(p)
            Path(dependency).unlink(missing_ok=True)
        else:
            dependency = None
        result = subprocess.run(command, env=capture['environment'], check=False)
        capture['exit_code'] = result.returncode
        if dependency is not None and result.returncode == 0 and not Path(dependency).is_file():
            raise ValueError('Compiler did not generate dependency file: ' + dependency)
        if dependency is not None and result.returncode == 0:
            paths = dependency_paths(Path(dependency), Path.cwd(), target=Path(object_path).name, primary=command[-3])
            generated = {str(p): digest(p) for p in paths if p.is_relative_to(build)}
            for name, value in generated.items():
                prior = generated_before.get(name)
                if prior is None and command[:3] == ['python3', '-s', 'util/ak820_default_keymap.py'] and Path(name) == build / 'default-keymap/ak820_default_keymap.inc':
                    generation = json.loads((build / 'default-keymap/generation.json').read_text())
                    prior = generation.get('final_dependencies', {}).get(name)
                if prior != value:
                    raise ValueError('Generated compiler input changed during compilation: ' + name)
            capture['generated_inputs'] = generated
            capture['fresh_dependency'] = dependency
        output.seek(0)
        json.dump(capture, output, sort_keys=True)
        output.write('\n')
        output.truncate()
    return result.returncode


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
