import json
import tempfile
import unittest
from pathlib import Path

from ak820_capture_compile import validate_default_keymap
from ak820_build_inputs import digest
from ak820_pointer_compile_policy import (expected_flags, expected_units, validate_pointer_arguments,
                                          validate_pointer_commands)


class PointerCommandTest(unittest.TestCase):
    def test_independent_historical_fixture(self):
        fixture_path = Path(__file__).resolve().parents[1] / 'tests/ak820_package/fixtures/pointer-pass30-historical-capture.json'
        fixture = json.loads(fixture_path.read_text())
        build = '.build/pointer'
        obj = build + '/obj_ajazz_ak820_vial'
        replace = lambda value: value.replace('{obj}', obj).replace('{build}', build)
        units = {replace(row['object']): replace(row['source']) for row in fixture['units']}
        self.assertEqual(len(units), 79)
        self.assertEqual(units, expected_units(obj))
        self.assertEqual([replace(flag) for flag in fixture['flags']], expected_flags(obj))
        wrappers = [row for row in fixture['units'] if row['wrapper']]
        self.assertEqual([row['source'] for row in wrappers], ['quantum/keymap_introspection.c'])
        altered = [replace(flag).replace('AK820_MOUSE_CURSOR_STEP=8', 'AK820_MOUSE_CURSOR_STEP=9')
                   for flag in fixture['flags']]
        self.assertNotEqual(altered, expected_flags(obj))
        with tempfile.TemporaryDirectory(prefix='ak820-historical-') as directory:
            root = Path(directory).resolve()
            compiler = root / 'toolchain/bin/sdcc'
            compiler.parent.mkdir(parents=True)
            compiler.write_text('')
            compiler.chmod(0o755)
            env = {'PATH': str(compiler.parent)}
            output = obj + '/quantum/keymap_introspection.o'
            dep = output[:-2] + '.d'
            argv = (['python3', '-s', 'util/ak820_default_keymap.py', 'sdcc'] +
                    [replace(flag) for flag in fixture['flags']] +
                    ['-Wp,-MD,-MF,' + dep, 'quantum/keymap_introspection.c', '-o', output])
            capture = root / (output + '.compile.json')
            capture.parent.mkdir(parents=True)
            capture.write_text(json.dumps({'argv': argv, 'cwd': str(root), 'environment': env, 'exit_code': 0}))
            commands = [[replace(arg.replace('{build}/default-keymap', str(root / build / 'default-keymap')))
                         .replace('{compiler}', str(compiler)).replace('{root}', str(root))
                         for arg in command] for command in fixture['nested_commands']]
            generation = root / build / 'default-keymap/generation.json'
            generation.parent.mkdir(parents=True)
            source = root / 'quantum/keymap_introspection.c'
            source.parent.mkdir(parents=True)
            source.write_text('source')
            evidence = {}
            for name, hash_key, paths_key in (('bootstrap.d', 'dependency_sha256', 'dependencies'),
                                               ('final-discovery.d', 'final_dependency_sha256', 'final_dependencies')):
                path = generation.parent / name
                path.write_text('keymap_introspection.o: quantum/keymap_introspection.c\n')
                evidence.update({hash_key: digest(path), paths_key: {str(source): digest(source)}})
            generation.write_text(json.dumps({'compiler_invocations': [
                {'argv': command, 'cwd': str(root), 'environment': env, 'exit_code': 0,
                 **({'fresh_dependency': next(arg.removeprefix('-Wp,-MD,-MF,') for arg in command
                                              if arg.startswith('-Wp,-MD,-MF,'))} if index else {})}
                for index, command in enumerate(commands)], **evidence}))
            validate_default_keymap([capture], root / build)
            self.assertEqual(len(commands), 5)

    def test_complete_argument_vector_and_mutations(self):
        obj = '.build/pointer/obj_ajazz_ak820_vial'
        flags = expected_flags(obj)
        dep, source, output = obj + '/ak820_board.d', 'keyboards/ajazz/ak820/ak820_board.c', obj + '/ak820_board.o'
        argv = ['sdcc'] + flags + ['-Wp,-MD,-MF,' + dep, source, '-o', output]
        self.assertEqual(validate_pointer_arguments(argv, flags, dep, source, output), 'direct')
        for extra in (['--include', '/tmp/evil.h'], ['@/tmp/flags.rsp'], ['-I/tmp'],
                      ['-D', 'AK820_MOUSE_CURSOR_STEP=9'], ['-DAK820_MOUSE_CURSOR_STEP=9'],
                      ['--stack-auto'], ['-UAK820_QMK_SETTINGS']):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                validate_pointer_arguments(argv[:2] + extra + argv[2:], flags, dep, source, output)
        for bad in (argv[:-1] + ['other.o'], argv[:-3] + ['other.c'] + argv[-2:],
                    argv[:2] + argv[3:], ['unknown'] + argv[1:]):
            with self.assertRaises(ValueError):
                validate_pointer_arguments(bad, flags, dep, source, output)
        wrong_order = argv.copy()
        wrong_order[2:4] = reversed(wrong_order[2:4])
        with self.assertRaises(ValueError):
            validate_pointer_arguments(wrong_order, flags, dep, source, output)

    def test_wrapper_is_only_for_keymap(self):
        obj = '.build/pointer/obj_ajazz_ak820_vial'
        flags = expected_flags(obj)
        dep, source, output = obj + '/quantum/keymap_introspection.d', 'quantum/keymap_introspection.c', obj + '/quantum/keymap_introspection.o'
        args = flags + ['-Wp,-MD,-MF,' + dep, source, '-o', output]
        self.assertEqual(validate_pointer_arguments(['python3', '-s', 'util/ak820_default_keymap.py', 'sdcc'] + args,
                                                    flags, dep, source, output), 'wrapper')
        with self.assertRaises(ValueError):
            validate_pointer_arguments(['sdcc'] + args, flags, dep, source, output)
        with self.assertRaises(ValueError):
            validate_pointer_arguments(['python3', '-s', 'util/ak820_default_keymap.py', 'sdcc'] + args,
                                       flags, dep, 'other.c', output)

    def test_complete_fixture_and_coherent_mutations(self):
        with tempfile.TemporaryDirectory(prefix='ak820-policy-') as directory:
            root = Path(directory).resolve()
            build = root / '.build/pointer'
            obj = '.build/pointer/obj_ajazz_ak820_vial'
            toolchain, qmk = root / 'toolchain', root / 'qmk/bin/qmk'
            compiler = toolchain / 'bin/sdcc'
            compiler.parent.mkdir(parents=True)
            compiler.write_text('')
            compiler.chmod(0o755)
            qmk.parent.mkdir(parents=True)
            environment = {'PATH': str(compiler.parent) + ':' + str(qmk.parent) + ':/usr/bin',
                           'AK820_CAPTURE_BUILD_ROOT': str(build),
                           'AK820_CAPTURE_OBJECT_ROOT': str(build / 'obj_ajazz_ak820_vial')}
            flags = expected_flags(obj)
            units = expected_units(obj)
            objects = [name[:-2] + '.rel' for name in units]
            records = {}
            for output, source in units.items():
                dep = output[:-2] + '.d'
                args = flags + ['-Wp,-MD,-MF,' + dep, source, '-o', output]
                wrapper = source == 'quantum/keymap_introspection.c'
                argv = (['python3', '-s', 'util/ak820_default_keymap.py', 'sdcc'] if wrapper else ['sdcc']) + args
                record = root / (output + '.compile.json')
                record.parent.mkdir(parents=True, exist_ok=True)
                data = {'argv': argv, 'cwd': str(root), 'environment': environment, 'exit_code': 0,
                        'fresh_dependency': dep}
                record.write_text(json.dumps(data))
                (root / dep).write_text(output + ': ' + source + '\n')
                records[output] = (record, data, dep)
            output = obj + '/quantum/keymap_introspection.o'
            outer = records[output][1]['argv'][4:]
            base = [str(compiler)] + outer
            keydir = str(build / 'default-keymap')
            prefix = [arg for arg in base if arg not in ('-c', '-o', output)
                      and not arg.startswith('-Wp,-MD,-MF,')]
            dep_index = 1 + len(flags)
            prefix.insert(1, '-S')
            prefix.insert(dep_index, '-Wp,-MD,-MF,' + keydir + '/bootstrap.d')
            bootstrap = prefix + ['-DAK820_DEFAULT_KEYMAP_EXTRACT', '-o', keydir + '/bootstrap.asm']
            dependency = bootstrap[:-2].copy()
            dependency[dependency.index('-S')] = '-E'
            final = base + ['-I' + keydir]
            discovery = [arg for arg in final if arg not in ('-c', '-o', output)
                         and not arg.startswith('-Wp,-MD,-MF,')]
            discovery.insert(1, '-E')
            discovery.insert(dep_index, '-Wp,-MD,-MF,' + keydir + '/final-discovery.d')
            commands = ([str(compiler), '--version'], dependency, bootstrap, discovery, final)
            invocations = [{'argv': command, 'cwd': str(root), 'environment': environment, 'exit_code': 0,
                            **({'fresh_dependency': next(arg.removeprefix('-Wp,-MD,-MF,') for arg in command
                                                         if arg.startswith('-Wp,-MD,-MF,'))} if index else {})}
                           for index, command in enumerate(commands)]
            generation = build / 'default-keymap/generation.json'
            generation.parent.mkdir(parents=True)
            source = root / 'quantum/keymap_introspection.c'
            source.parent.mkdir(parents=True)
            source.write_text('source')
            evidence = {}
            for name, hash_key, paths_key in (('bootstrap.d', 'dependency_sha256', 'dependencies'),
                                               ('final-discovery.d', 'final_dependency_sha256', 'final_dependencies')):
                path = generation.parent / name
                path.write_text('keymap_introspection.o: quantum/keymap_introspection.c\n')
                evidence.update({hash_key: digest(path), paths_key: {str(source): digest(source)}})
            generation.write_text(json.dumps({'compiler_invocations': invocations, **evidence}))
            def validate(names=objects):
                return validate_pointer_commands(root, build, names, toolchain, qmk)
            self.assertEqual(validate(), 'ak820-pointer-pass30-arguments-1')
            self.assertEqual(len(objects), 79)
            victim = obj + '/ak820_board.o'
            record, data, dep = records[victim]
            original = record.read_text()
            record.unlink()
            with self.assertRaisesRegex(ValueError, 'object membership'):
                validate([name for name in objects if name != victim[:-2] + '.rel'])
            record.write_text(original)
            with self.assertRaisesRegex(ValueError, 'object membership'):
                validate(objects + [objects[0]])
            with self.assertRaisesRegex(ValueError, 'object membership'):
                validate(objects + [obj + '/extra.rel'])
            changed = dict(data)
            changed['argv'] = data['argv'][:-3] + ['keyboards/ajazz/ak820/replacement.c'] + data['argv'][-2:]
            record.write_text(json.dumps(changed))
            (root / dep).write_text(victim + ': keyboards/ajazz/ak820/replacement.c\n')
            with self.assertRaisesRegex(ValueError, 'object/source mapping'):
                validate()
            (root / dep).write_text(victim + ': ' + units[victim] + '\n')
            record.write_text(original)
            bad = dict(data, environment={**environment, 'CPATH': '/tmp'})
            record.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, 'environment'):
                validate()
            record.write_text(original)
            invocations[-1]['argv'] = invocations[-1]['argv'] + ['@evil']
            generation.write_text(json.dumps({'compiler_invocations': invocations, **evidence}))
            with self.assertRaisesRegex(ValueError, 'nested compiler capture'):
                validate()


if __name__ == '__main__':
    unittest.main()
