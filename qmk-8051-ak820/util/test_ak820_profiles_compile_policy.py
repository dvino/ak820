import copy
import json
import tempfile
import unittest
from pathlib import Path

from ak820_build_inputs import digest
from ak820_profiles import configuration
from ak820_pointer_compile_policy import expected_flags as pointer_flags, expected_units as pointer_units
from ak820_profiles_compile_policy import canonical, expected_flags, expected_units, validate_commands, POLICY

# Hand-specified ordered board blocks and deltas against the retained pointer capture.
# They are source-derived synthetic expectations, not non-pointer captures.
BOARD = {
 'main': '-DAK820_COMPACT_AUTOSHIFT -DAK820_VIALRGB_DIRECT -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_LEADER -DAK820_OS_INDICATORS -DAK820_COMPACT_KEY_OVERRIDE',
 'game': '-DAK820_NKRO -DAK820_VIALRGB_DIRECT -DAK820_NKRO_CONTROL -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_GUI_LOCK -DAK820_OS_INDICATORS -DAK820_COMPACT_KEY_OVERRIDE',
 'mmo': '-DAK820_NKRO -DAK820_VIALRGB_DIRECT -DAK820_NKRO_CONTROL -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_GUI_LOCK -DAK820_OS_INDICATORS -DAK820_COMPACT_TAP_DANCE',
 'typing': '-DAK820_COMPACT_AUTOSHIFT -DVIALRGB_NO_DIRECT -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_SPACE_CADET -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_LEADER -DAK820_OS_INDICATORS -DAK820_COMPACT_TAP_DANCE -DAK820_COMPACT_KEY_OVERRIDE',
 'code': '-DAK820_GRAVE_ESCAPE -DVIALRGB_NO_DIRECT -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_SPACE_CADET -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_LEADER -DAK820_OS_INDICATORS -DAK820_COMPACT_TAP_DANCE -DAK820_COMPACT_KEY_OVERRIDE',
 'pointer': '-DVIALRGB_NO_DIRECT -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_MOUSEKEY -DAK820_MOUSE_CURSOR_STEP=8 -DAK820_MOUSE_CURSOR_PERIOD=20 -DAK820_MOUSE_WHEEL_STEP=1 -DAK820_MOUSE_WHEEL_PERIOD=80 -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_LEADER -DAK820_OS_INDICATORS -DAK820_COMPACT_TAP_DANCE -DAK820_COMPACT_KEY_OVERRIDE',
 'onehand': '-DVIALRGB_NO_DIRECT -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_MOUSEKEY -DAK820_MOUSE_CURSOR_STEP=8 -DAK820_MOUSE_CURSOR_PERIOD=20 -DAK820_MOUSE_WHEEL_STEP=1 -DAK820_MOUSE_WHEEL_PERIOD=80 -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_LEADER -DAK820_OS_INDICATORS -DAK820_COMPACT_TAP_DANCE',
 'creative': '-DAK820_NKRO -DAK820_VIALRGB_DIRECT -DAK820_NKRO_CONTROL -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_LEADER -DAK820_OS_INDICATORS -DAK820_COMPACT_TAP_DANCE',
 'shortcuts': '-DAK820_NKRO -DVIALRGB_NO_DIRECT -DAK820_NKRO_CONTROL -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_LEADER -DAK820_OS_INDICATORS -DAK820_COMPACT_TAP_DANCE -DAK820_COMPACT_KEY_OVERRIDE',
 'multios': '-DVIALRGB_NO_DIRECT -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_CTRL_GUI_SWAP -DAK820_COMPACT_LEADER -DAK820_OS_INDICATORS -DAK820_MAC_PC -DAK820_COMPACT_TAP_DANCE -DAK820_COMPACT_KEY_OVERRIDE',
}
REMOVED = {'main':'M T', 'game':'M L T', 'mmo':'M L K', 'typing':'M', 'code':'M',
           'pointer':'', 'onehand':'K', 'creative':'M K', 'shortcuts':'M', 'multios':'M'}
COUNTS = dict(zip(BOARD, (78, 76, 76, 79, 79, 79, 78, 77, 78, 78)))
PATHS = {'M':'keyboards/ajazz/ak820/ak820_mousekey', 'L':'ak820_leader',
         'T':'ak820_tap_dance', 'K':'ak820_key_override'}

class PolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This path is relative to the QMK util directory in the proposed patch.
        cls.fixture = json.loads((Path(__file__).resolve().parents[1] / 'tests/ak820_package/fixtures/pointer-pass30-historical-capture.json').read_text())

    def vectors(self, name, obj):
        replace = lambda s: s.replace('{obj}', obj).replace('{build}', obj.rsplit('/', 1)[0])
        units = {replace(row['object']): replace(row['source']) for row in self.fixture['units']}
        for letter in REMOVED[name].split():
            del units[obj + '/' + PATHS[letter] + '.o']
        if name in ('main', 'typing'):
            units[obj + '/ak820_autoshift.o'] = 'keyboards/ajazz/ak820/ak820_autoshift.c'
        if name == 'code':
            path = 'quantum/process_keycode/process_grave_esc'
            units[obj + '/' + path + '.o'] = path + '.c'
        flags = [replace(flag) for flag in self.fixture['flags']]
        flags[flags.index('-DVIALRGB_NO_DIRECT'):flags.index('-DAK820_QMK_SETTINGS')] = BOARD[name].split()
        if name not in ('pointer', 'onehand'):
            for token in ('-DMOUSEKEY_ENABLE', '-DMOUSE_ENABLE', '-DMOUSE_SHARED_EP'):
                flags.remove(token)
        if name == 'code':
            flags.insert(flags.index('-DREPEAT_KEY_ENABLE'), '-DGRAVE_ESC_ENABLE')
        if name in ('game', 'mmo', 'creative', 'shortcuts'):
            flags.insert(flags.index('-DSHARED_EP_ENABLE'), '-DNKRO_ENABLE')
        return units, flags

    def test_pointer_policy_equivalence(self):
        for obj in ('.build/example/obj_ajazz_ak820_vial', '.build/other/obj_ajazz_ak820_vial'):
            with self.subTest(obj=obj):
                self.assertEqual(expected_units('pointer', obj), pointer_units(obj))
                self.assertEqual(expected_flags('pointer', obj), pointer_flags(obj))

    def test_vectors_and_canonical_rejection(self):
        obj = '.build/example/obj_ajazz_ak820_vial'
        for name in BOARD:
            with self.subTest(profile=name):
                units, flags = self.vectors(name, obj)
                self.assertEqual(len(units), COUNTS[name])
                self.assertEqual(units, expected_units(name, obj))
                self.assertEqual(flags, expected_flags(name, obj))
                selected = configuration(name)
                self.assertEqual(canonical(selected), name)
                for mutate in ('extra', 'feature', 'option', 'mouse', 'timing'):
                    bad = copy.deepcopy(selected)
                    if mutate == 'extra': bad['extra'] = True
                    if mutate == 'feature': bad['optional_features'].append('unknown')
                    if mutate == 'option': bad['make_options']['AK820_UNKNOWN'] = 'yes'
                    if mutate == 'mouse': bad['mouse_keys'] = {'cursor_step': 9}
                    if mutate == 'timing': bad['timing_ms']['combo'] = True
                    with self.assertRaises(ValueError): canonical(bad)
        with self.assertRaises(ValueError): canonical(configuration('maximal'))

    def test_synthetic_commands_and_coherent_mutations(self):
        for name in BOARD:
            with self.subTest(profile=name), tempfile.TemporaryDirectory(prefix='ak820-synthetic-') as directory:
                root = Path(directory).resolve()
                build = root / '.build/example'
                obj = '.build/example/obj_ajazz_ak820_vial'
                toolchain, qmk = root / 'toolchain', root / 'qmk/bin/qmk'
                compiler = toolchain / 'bin/sdcc'
                compiler.parent.mkdir(parents=True)
                compiler.write_text('')
                compiler.chmod(0o755)
                qmk.parent.mkdir(parents=True)
                env = {'PATH': str(compiler.parent) + ':' + str(qmk.parent),
                       'AK820_CAPTURE_BUILD_ROOT': str(build),
                       'AK820_CAPTURE_OBJECT_ROOT': str(build / 'obj_ajazz_ak820_vial')}
                units, flags = self.vectors(name, obj)
                objects = [output[:-2] + '.rel' for output in units]
                records = {}
                for output, source in units.items():
                    dep = output[:-2] + '.d'
                    args = flags + ['-Wp,-MD,-MF,' + dep, source, '-o', output]
                    argv = (['python3', '-s', 'util/ak820_default_keymap.py', 'sdcc'] if source == 'quantum/keymap_introspection.c' else ['sdcc']) + args
                    record = root / (output + '.compile.json')
                    record.parent.mkdir(parents=True, exist_ok=True)
                    source_path = root / source
                    source_path.parent.mkdir(parents=True, exist_ok=True)
                    source_path.touch()
                    generated = {str(source_path): digest(source_path)} if source_path.is_relative_to(build) else {}
                    record.write_text(json.dumps({'argv': argv, 'cwd': str(root), 'environment': env,
                                                  'exit_code': 0, 'fresh_dependency': dep, 'generated_inputs': generated}))
                    (root / dep).write_text(Path(output).name + ': ' + source + '\n')
                    records[output] = record
                output = obj + '/quantum/keymap_introspection.o'
                outer = json.loads(records[output].read_text())['argv'][4:]
                base = [str(compiler)] + outer
                keydir = str(build / 'default-keymap')
                bootstrap = [a for a in base if a not in ('-c', '-o', output) and not a.startswith('-Wp,-MD,-MF,')]
                bootstrap.insert(1, '-S')
                bootstrap.insert(1 + len(flags), '-Wp,-MD,-MF,' + keydir + '/bootstrap.d')
                bootstrap += ['-DAK820_DEFAULT_KEYMAP_EXTRACT', '-o', keydir + '/bootstrap.asm']
                dependency = bootstrap[:-2].copy()
                dependency[dependency.index('-S')] = '-E'
                final = base + ['-I' + keydir]
                discovery = [a for a in final if a not in ('-c', '-o', output) and not a.startswith('-Wp,-MD,-MF,')]
                discovery.insert(1, '-E')
                discovery.insert(1 + len(flags), '-Wp,-MD,-MF,' + keydir + '/final-discovery.d')
                invocations = [{'argv': command, 'cwd': str(root), 'environment': env, 'exit_code': 0,
                                **({'fresh_dependency': next(a.removeprefix('-Wp,-MD,-MF,') for a in command
                                                              if a.startswith('-Wp,-MD,-MF,'))} if index else {})}
                               for index, command in enumerate(([str(compiler), '--version'], dependency, bootstrap, discovery, final))]
                generation = build / 'default-keymap/generation.json'
                generation.parent.mkdir(parents=True)
                source = root / 'quantum/keymap_introspection.c'
                generated_deps = {}
                for filename, hash_key, paths_key in (('bootstrap.d', 'dependency_sha256', 'dependencies'),
                                                       ('final-discovery.d', 'final_dependency_sha256', 'final_dependencies')):
                    path = generation.parent / filename
                    path.write_text('keymap_introspection.o: quantum/keymap_introspection.c\n')
                    generated_deps[hash_key] = digest(path)
                    generated_deps[paths_key] = {str(source): digest(source)}
                metadata = {'compiler_invocations': invocations, **generated_deps}
                generation.write_text(json.dumps(metadata))
                def validate(): return validate_commands(root, build, objects, toolchain, qmk, configuration(name))
                self.assertEqual(validate(), POLICY)
                objects.append(obj + '/unexpected.rel')
                with self.assertRaises(ValueError): validate()
                objects.pop()
                missing = objects.pop()
                with self.assertRaises(ValueError): validate()
                objects.append(missing)
                other = 'game' if name != 'game' else 'main'
                with self.assertRaises(ValueError):
                    validate_commands(root, build, objects, toolchain, qmk, configuration(other))
                victim = obj + '/ak820_board.o'
                record = records[victim]
                original = record.read_text()
                data = json.loads(original)
                # Coherent argv + depfile substitution cannot redefine the primary source.
                data['argv'][-3] = 'keyboards/ajazz/ak820/other.c'
                record.write_text(json.dumps(data))
                dep = root / (victim[:-2] + '.d')
                dep.write_text(Path(victim).name + ': keyboards/ajazz/ak820/other.c\n')
                with self.assertRaises(ValueError): validate()
                dep.write_text(Path(victim).name + ': ' + units[victim] + '\n')
                record.write_text(original)
                data = json.loads(original)
                data['argv'][1], data['argv'][2] = data['argv'][2], data['argv'][1]
                record.write_text(json.dumps(data))
                with self.assertRaises(ValueError): validate()
                data = json.loads(original)
                data['environment']['PATH'] = '/invalid'
                record.write_text(json.dumps(data))
                with self.assertRaises(ValueError): validate()
                record.write_text(original)
                wrapper = records[output]
                wrapper_original = wrapper.read_text()
                data = json.loads(wrapper_original)
                data['argv'][1] = '-E'
                wrapper.write_text(json.dumps(data))
                with self.assertRaises(ValueError): validate()
                wrapper.write_text(wrapper_original)
                # Same forged extra option in every outer capture must still fail.
                for path in records.values():
                    data = json.loads(path.read_text())
                    data['argv'].insert(-3, '-DAK820_UNRECOGNIZED')
                    path.write_text(json.dumps(data))
                with self.assertRaises(ValueError): validate()
                for path in records.values():
                    data = json.loads(path.read_text())
                    data['argv'].remove('-DAK820_UNRECOGNIZED')
                    path.write_text(json.dumps(data))
                for index in range(len(invocations)):
                    for field in ('argv', 'environment'):
                        with self.subTest(profile=name, invocation=index, field=field):
                            altered = copy.deepcopy(invocations)
                            if field == 'argv':
                                altered[index]['argv'].append('@extra')
                            else:
                                altered[index]['environment']['PATH'] = '/invalid'
                            generation.write_text(json.dumps({**metadata, 'compiler_invocations': altered}))
                            with self.assertRaises(ValueError): validate()
                generation.write_text(json.dumps(metadata))
                self.assertEqual(validate(), POLICY)
                for filename in ('bootstrap.d', 'final-discovery.d'):
                    path = generation.parent / filename
                    original = path.read_text()
                    path.write_text('wrong.o: quantum/keymap_introspection.c\n')
                    with self.assertRaises(ValueError): validate()
                    path.write_text('keymap_introspection.o: quantum/keymap_introspection.c \n')
                    with self.assertRaises(ValueError): validate()
                    path.unlink()
                    with self.assertRaises(FileNotFoundError): validate()
                    path.write_text(original)
                altered = copy.deepcopy(metadata)
                del altered['compiler_invocations'][1]['fresh_dependency']
                generation.write_text(json.dumps(altered))
                with self.assertRaises(ValueError): validate()

if __name__ == '__main__': unittest.main()
