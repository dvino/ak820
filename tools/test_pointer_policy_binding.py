import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import configure_firmware as config
from ak820_build_inputs import FORMAT as INPUT_FORMAT
from ak820_profiles_compile_policy import expected_flags, expected_units


class PointerBindingTest(unittest.TestCase):
    def canonical_fixture(self, root):
        build = root / '.build/example'
        obj = '.build/example/obj_ajazz_ak820_vial'
        toolchain, qmk = root / 'toolchain', root / 'qmk/bin/qmk'
        compiler = toolchain / 'bin/sdcc'
        compiler.parent.mkdir(parents=True)
        compiler.write_text('synthetic compiler')
        compiler.chmod(0o755)
        qmk.parent.mkdir(parents=True)
        environment = {'PATH': str(compiler.parent) + ':' + str(qmk.parent),
                       'AK820_CAPTURE_BUILD_ROOT': str(build.resolve()),
                       'AK820_CAPTURE_OBJECT_ROOT': str((root / obj).resolve())}
        units, flags = expected_units('main', obj), expected_flags('main', obj)
        objects = [output[:-2] + '.rel' for output in units]
        sources, artifacts = set(), []

        def source(name):
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text('synthetic input\n')
            sources.add(name)
            return path

        def artifact(path):
            artifacts.append({'path': path.relative_to(root).as_posix(),
                              'sha256': config.sha(path), 'size': path.stat().st_size})

        for output, primary in units.items():
            source_path = source(primary)
            dep = output[:-2] + '.d'
            args = flags + ['-Wp,-MD,-MF,' + dep, primary, '-o', output]
            wrapper = primary == 'quantum/keymap_introspection.c'
            argv = (['python3', '-s', 'util/ak820_default_keymap.py', 'sdcc'] if wrapper else ['sdcc']) + args
            record, dep_path = root / (output + '.compile.json'), root / dep
            record.parent.mkdir(parents=True, exist_ok=True)
            generated = {str(source_path): config.sha(source_path)} if source_path.is_relative_to(build) else {}
            record.write_text(json.dumps({'argv': argv, 'cwd': str(root), 'environment': environment,
                                          'exit_code': 0, 'fresh_dependency': dep,
                                          'generated_inputs': generated}))
            dep_path.write_text(Path(output).name + ': ' + primary + '\n')
            artifact(record)
            artifact(dep_path)
            if wrapper:
                outer, wrapper_output = argv[4:], output

        directory = str(build / 'default-keymap')
        base = [str(compiler)] + outer
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
                bootstrap.append('-Wp,-MD,-MF,' + directory + '/bootstrap.d')
            else:
                bootstrap.append(arg)
        bootstrap += ['-DAK820_DEFAULT_KEYMAP_EXTRACT', '-o', directory + '/bootstrap.asm']
        dependency = bootstrap[:-2].copy()
        dependency[dependency.index('-S')] = '-E'
        final = base + ['-I' + directory]
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
                discovery.append('-Wp,-MD,-MF,' + directory + '/final-discovery.d')
            else:
                discovery.append(arg)
        invocations = [{'argv': command, 'cwd': str(root), 'environment': environment, 'exit_code': 0,
                        **({'fresh_dependency': next(arg.removeprefix('-Wp,-MD,-MF,') for arg in command
                                                    if arg.startswith('-Wp,-MD,-MF,'))} if index else {})}
                       for index, command in enumerate(([str(compiler), '--version'], dependency, bootstrap, discovery, final))]
        generation = build / 'default-keymap/generation.json'
        generation.parent.mkdir(parents=True, exist_ok=True)
        dependencies = {}
        for name, hash_key, paths_key in (('bootstrap.d', 'dependency_sha256', 'dependencies'),
                                           ('final-discovery.d', 'final_dependency_sha256', 'final_dependencies')):
            path = generation.parent / name
            path.write_text('keymap_introspection.o: quantum/keymap_introspection.c\n')
            dependencies[hash_key] = config.sha(path)
            dependencies[paths_key] = {str(root / 'quantum/keymap_introspection.c'):
                                       config.sha(root / 'quantum/keymap_introspection.c')}
        generation.write_text(json.dumps({'compiler_invocations': invocations, **dependencies}))
        artifact(generation)
        manifest = build / 'obj_ajazz_ak820_vial/obj.txt'
        manifest.write_text('\n'.join(objects) + '\n')
        artifact(manifest)
        cflags = manifest.parent / 'cflags.txt'
        cflags.write_text(' '.join(flags))
        artifact(cflags)
        for name in ('util/build_ak820.py', 'keyboards/ajazz/ak820/ak820_mousekey.c',
                     'util/ak820_capture_compile.py', 'util/ak820_default_keymap.py',
                     'util/ak820_pointer_compile_policy.py', 'util/ak820_pointer_compile_environment.py',
                     'util/ak820_profiles_compile_policy.py'):
            source(name)
        log = build / 'compile.log'
        log.write_text('synthetic compile log')
        selected = config.profiles.configuration('main')
        command = ['QMK_BIN=' + str(qmk), 'NOLTO_CFLAGS=', 'INIT_HOOK_CFLAGS='] + [
            define + '=' + str(config.profiles.MOUSE_DEFAULTS[key])
            for key, define in config.profiles.MOUSE_DEFINES.items()]
        report = {'configuration': selected, 'keyboard': 'ajazz/ak820', 'keymap': 'vial',
                  'build_id': selected['nvm_schema'], 'hardware_validated': False,
                  'code_window': [0x3027, 0xc700], 'code_windows': [list(w) for w in config.WINDOWS],
                  'xram_window': [0x440, 0x1000], 'compiler_input_contract': config.CANONICAL_POLICY,
                  'builder_sha256': config.sha(root / 'util/build_ak820.py'),
                  'source_manifest_format': INPUT_FORMAT,
                  'sources': [{'origin': 'source', 'path': name, 'sha256': config.sha(root / name)}
                              for name in sorted(sources)],
                  'artifacts': artifacts, 'expected_objects': objects,
                  'compiler_sha256': config.SDCC46_PINS['sdcc'],
                  'assembler_sha256': config.SDCC46_PINS['sdas8051'],
                  'commands': [{'label': 'compile', 'argv': command, 'exit_code': 0,
                                'log': log.relative_to(root).as_posix(), 'log_sha256': config.sha(log)}]}
        return build, toolchain, report

    def test_inspect_requires_real_canonical_evidence_before_pass30(self):
        with tempfile.TemporaryDirectory(prefix='ak820-orchestration-') as directory:
            root = Path(directory).resolve()
            build, toolchain, report = self.canonical_fixture(root)
            report_path = build / 'build-report.json'

            def inspect(candidate):
                report_path.write_text(json.dumps(candidate))
                return config.inspect(build, toolchain)

            with patch.object(config, 'QMK', root), patch.object(config, 'validate_tools', return_value=toolchain), \
                    patch.object(config, 'check_pass30', wraps=config.check_pass30) as pass30:
                with self.assertRaisesRegex(ValueError, 'Unqualified pass30 compiler/ABI/transform configuration'):
                    inspect(report)
                pass30.assert_called_once()
                config.check_feature_defines(report, build, report['configuration'], toolchain=toolchain)
                with self.assertRaisesRegex(ValueError, 'compiler-input contract is not closed'):
                    config.check_feature_defines(report, build, report['configuration'])
                with self.assertRaises(ValueError):
                    config.profiles.require_release_qualification(report)

                for kind in ('missing-marker', 'unknown-marker', 'legacy-marker', 'missing-source', 'forged-source',
                             'missing-capture', 'wrong-profile'):
                    changed = copy.deepcopy(report)
                    if kind == 'missing-marker': changed.pop('compiler_input_contract')
                    if kind == 'unknown-marker': changed['compiler_input_contract'] = 'forged'
                    if kind == 'legacy-marker': changed['compiler_input_contract'] = config.POINTER_POLICY
                    if kind == 'missing-source': changed['sources'] = []
                    if kind == 'forged-source': changed['sources'][0]['sha256'] = '0' * 64
                    if kind == 'missing-capture':
                        changed['artifacts'] = [row for row in changed['artifacts']
                                                if not row['path'].endswith('.o.compile.json')]
                    if kind == 'wrong-profile': changed['configuration'] = config.profiles.configuration('game')
                    pass30.reset_mock()
                    with self.subTest(kind=kind), self.assertRaises(ValueError):
                        inspect(changed)
                    pass30.assert_not_called()
                    with self.subTest(direct=kind), self.assertRaises(ValueError):
                        config.check_feature_defines(changed, build, report['configuration'], toolchain=toolchain)

                # Rebind the modified capture artifact: policy, not merely its hash, must reject it.
                victim = next(row for row in report['artifacts'] if row['path'].endswith('ak820_board.o.compile.json'))
                capture = root / victim['path']
                original = capture.read_text()
                for field in ('fresh_dependency', 'argv'):
                    data = json.loads(original)
                    if field == 'fresh_dependency': data.pop(field)
                    else: data['argv'].insert(-3, '-DAK820_UNRECOGNIZED')
                    capture.write_text(json.dumps(data))
                    changed = copy.deepcopy(report)
                    row = next(row for row in changed['artifacts'] if row['path'] == victim['path'])
                    row.update(sha256=config.sha(capture), size=capture.stat().st_size)
                    pass30.reset_mock()
                    with self.subTest(capture=field), self.assertRaises(ValueError):
                        inspect(changed)
                    pass30.assert_not_called()
                capture.write_text(original)

            # Isolate the real exact-image artifact gate after the synthetic pass30
            # fixture, without claiming a replay or image qualification.
            with patch.object(config, 'QMK', root), patch.object(config, 'validate_tools', return_value=toolchain), \
                    patch.object(config, 'check_pass30', return_value={'contract': 'synthetic'}):
                with self.assertRaisesRegex(ValueError, 'Missing or ambiguous artifact: ihx'):
                    inspect(report)
                image = build / 'ajazz_ak820_vial.ihx'
                image.write_text('synthetic image')
                changed = copy.deepcopy(report)
                changed['artifacts'].append({'path': image.relative_to(root).as_posix(),
                                             'sha256': '0' * 64, 'size': image.stat().st_size})
                with self.assertRaisesRegex(ValueError, 'Artifact changed: ihx'):
                    inspect(changed)
                forged = copy.deepcopy(changed)
                forged.pop('compiler_input_contract')
                with self.assertRaisesRegex(ValueError, 'compiler-input contract is not closed'):
                    inspect(forged)

    def test_historical_inspection_still_reaches_exact_image_checks(self):
        with tempfile.TemporaryDirectory(prefix='ak820-historical-') as directory:
            root = Path(directory).resolve()
            build = root / '.build/historical'
            flags = build / 'obj_ajazz_ak820_vial/cflags.txt'
            flags.parent.mkdir(parents=True)
            selected = config.profiles.configuration('full')
            flags.write_text(' '.join('-D' + config.profiles.SWITCHES[name]
                                      for name in selected['optional_features']) +
                             ' -DNKRO_ENABLE -DGRAVE_ESC_ENABLE')
            names = ('util/build_ak820.py', 'keyboards/ajazz/ak820/ak820_mousekey.c')
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('different current source')
            hashes = config.profiles.HISTORICAL_COMPILER_INPUT_PAIR
            report = {'configuration': selected, 'keyboard': 'ajazz/ak820', 'keymap': 'vial',
                      'build_id': selected['nvm_schema'], 'hardware_validated': False,
                      'code_window': [0x3027, 0xc700], 'code_windows': [list(w) for w in config.WINDOWS],
                      'xram_window': [0x400, 0x1000], 'builder_sha256': hashes[0],
                      'sources': [{'origin': 'source', 'path': name, 'sha256': value}
                                  for name, value in zip(names, hashes)],
                      'artifacts': [{'path': flags.relative_to(root).as_posix(),
                                     'sha256': config.sha(flags), 'size': flags.stat().st_size}],
                      'compiler_sha256': config.SDCC46_PINS['sdcc'],
                      'assembler_sha256': config.SDCC46_PINS['sdas8051'],
                      'compiler_extra_flags': '--opt-code-size --callee-saves ' + ','.join(config.AK820_CALLEE_SAVES),
                      'audited_callee_saves': list(config.AK820_CALLEE_SAVES), 'outlining': {}}
            (build / 'build-report.json').write_text(json.dumps(report))
            with patch.object(config, 'QMK', root), patch.object(config, 'validate_tools', return_value=root), \
                    patch.object(config, 'validate_inputs') as inputs, \
                    patch.object(config, 'check_pointer_compiler_inputs') as compiler, \
                    patch.object(config, 'artifact', side_effect=RuntimeError('exact-image sentinel')) as artifact:
                with self.assertRaisesRegex(RuntimeError, 'exact-image sentinel'):
                    config.inspect(build, root)
                inputs.assert_called_once()
                compiler.assert_not_called()
                artifact.assert_called_once()
                config.check_feature_defines(report, build, selected)
                for marker in ('unknown', config.CANONICAL_POLICY, config.POINTER_POLICY):
                    changed = copy.deepcopy(report)
                    changed['compiler_input_contract'] = marker
                    with self.subTest(marker=marker), self.assertRaisesRegex(ValueError, 'Unknown compiler-input'):
                        config.check_feature_defines(changed, build, selected)

    def test_compiler_markers_and_provenance(self):
        paths = ('util/build_ak820.py', 'keyboards/ajazz/ak820/ak820_mousekey.c')
        hashes = config.profiles.HISTORICAL_COMPILER_INPUT_PAIR
        historical = {'builder_sha256': hashes[0], 'sources': [
            {'origin': 'source', 'path': path, 'sha256': digest}
            for path, digest in zip(paths, hashes)]}
        current = copy.deepcopy(historical)
        current['builder_sha256'] = 'different'
        absent = object()
        for provenance, report in (('historical', historical), ('current', current)):
            for marker, outcome in ((absent, False), (None, None), ('unverified', None),
                                    ('unknown', None), (config.POINTER_POLICY, provenance == 'current'),
                                    (config.CANONICAL_POLICY, provenance == 'current')):
                candidate = copy.deepcopy(report)
                if marker is not absent:
                    candidate['compiler_input_contract'] = marker
                with self.subTest(provenance=provenance, marker=marker):
                    if outcome is None or (marker in (config.POINTER_POLICY, config.CANONICAL_POLICY) and not outcome):
                        with self.assertRaisesRegex(ValueError, 'Unknown compiler-input'):
                            config.check_compiler_marker(candidate)
                    else:
                        self.assertIs(config.check_compiler_marker(candidate), outcome)
                    if marker is not absent:
                        with self.assertRaises(ValueError):
                            config.profiles.require_release_qualification(candidate)

    @unittest.skipUnless(os.environ.get('AK820_POINTER_EVIDENCE_DIR') and
                         os.environ.get('AK820_POINTER_TOOLCHAIN'),
                         'requires same-location retained pointer evidence and toolchain')
    def test_retained_pointer_evidence_without_mocks(self):
        build = Path(os.environ['AK820_POINTER_EVIDENCE_DIR']).resolve()
        toolchain = config.validate_tools(os.environ['AK820_POINTER_TOOLCHAIN'])
        report_path = build / 'build-report.json'
        report = config.load_json(report_path)
        selected = config.profiles.configuration('pointer')
        self.assertEqual(report['configuration'], selected)
        self.assertTrue(config.check_compiler_marker(report))
        config.validate_inputs(report, config.QMK, toolchain)
        config.check_pointer_compiler_inputs(report, build, toolchain, selected)
        with self.assertRaisesRegex(ValueError, 'Current compiler-input contract is not closed'):
            config.check_feature_defines(report, build, selected)
        result = config.check_pass30(report, build, toolchain)
        self.assertEqual(result['contract'], 'ak820-audited-pass30-1')
        image = config.artifact(report, build, 'ihx')
        mapfile = config.artifact(report, build, 'map')
        config.artifact(report, build, 'mem')
        config.check_short_calls(report, build, image)
        self.assertTrue(config.diagnostic_build(image, mapfile, report_path))
        with tempfile.TemporaryDirectory(prefix='ak820-image-mutation-') as temporary:
            altered = Path(temporary) / image.name
            altered.write_bytes(image.read_bytes() + b'\n')
            with self.assertRaisesRegex(ValueError, 'Short-call input/output evidence changed'):
                config.check_short_calls(report, build, altered)

        for origin in ('source', 'toolchain'):
            changed = copy.deepcopy(report)
            next(row for row in changed['sources'] if row['origin'] == origin)['sha256'] = '0' * 64
            with self.subTest(input_origin=origin), self.assertRaises(ValueError):
                config.validate_inputs(changed, config.QMK, toolchain)
        object_name = Path(report['expected_objects'][0])
        artifact_names = (object_name.with_suffix('.o.compile.json').as_posix(),
                          object_name.with_suffix('.d').as_posix(),
                          (build / 'obj_ajazz_ak820_vial/obj.txt').relative_to(config.QMK).as_posix(),
                          (build / 'default-keymap/generation.json').relative_to(config.QMK).as_posix())
        for name in artifact_names:
            changed = copy.deepcopy(report)
            next(row for row in changed['artifacts'] if row['path'] == name)['sha256'] = '0' * 64
            with self.subTest(artifact=name, mutation='changed'), self.assertRaises(ValueError):
                config.check_pointer_compiler_inputs(changed, build, toolchain, selected)
            changed = copy.deepcopy(report)
            changed['artifacts'] = [row for row in changed['artifacts'] if row['path'] != name]
            with self.subTest(artifact=name, mutation='missing'), self.assertRaises(ValueError):
                config.check_pointer_compiler_inputs(changed, build, toolchain, selected)
        changed = copy.deepcopy(report)
        changed['expected_objects'].pop()
        with self.assertRaises(ValueError):
            config.check_pointer_compiler_inputs(changed, build, toolchain, selected)
        dep = config.QMK / object_name.with_suffix('.d')
        dependency = next(path.relative_to(config.QMK).as_posix()
                          for path in config.dependency_paths(dep, config.QMK)
                          if path.is_relative_to(config.QMK))
        changed = copy.deepcopy(report)
        changed['sources'] = [row for row in changed['sources']
                              if not (row['origin'] == 'source' and row['path'] == dependency)]
        with self.assertRaisesRegex(ValueError, 'Unbound compiler dependency'):
            config.check_pointer_compiler_inputs(changed, build, toolchain, selected)
        for suffix in ('/parameter-spills.json', '/short-calls.json'):
            changed = copy.deepcopy(report)
            rows = [row for row in changed['artifacts'] if row['path'].endswith(suffix)]
            self.assertEqual(len(rows), 1)
            rows[0]['sha256'] = '0' * 64
            with self.subTest(transform=suffix), self.assertRaises(ValueError):
                config._replay_pass30(changed, build, toolchain)
        for suffix in ('ihx', 'map', 'mem'):
            changed = copy.deepcopy(report)
            next(row for row in changed['artifacts'] if row['path'].endswith('/ajazz_ak820_vial.' + suffix))['sha256'] = '0' * 64
            with self.subTest(image=suffix), self.assertRaises(ValueError):
                config.artifact(changed, build, suffix)
        with self.assertRaises(ValueError):
            config.profiles.require_release_qualification(report)

    def test_report_artifacts_and_dependencies_are_required(self):
        with tempfile.TemporaryDirectory(prefix='ak820-binding-') as directory:
            root = Path(directory).resolve()
            build = root / '.build/pointer'
            obj = build / 'obj_ajazz_ak820_vial/board.rel'
            source = root / 'board.c'
            source.write_text('int value;\n')
            manifest = build / 'obj_ajazz_ak820_vial/obj.txt'
            generation = build / 'default-keymap/generation.json'
            capture, dep = obj.with_suffix('.o.compile.json'), obj.with_suffix('.d')
            for path in (manifest, generation, capture, dep):
                path.parent.mkdir(parents=True, exist_ok=True)
            relative = obj.relative_to(root).as_posix()
            manifest.write_text(relative + '\n')
            generation.write_text('{}\n')
            capture.write_text('{}\n')
            dep.write_text('board.o: board.c\n')
            paths = (manifest, generation, capture, dep)
            report = {'compiler_input_contract': config.POINTER_POLICY,
                      'expected_objects': [relative],
                      'artifacts': [{'path': p.relative_to(root).as_posix(), 'sha256': config.sha(p),
                                     'size': p.stat().st_size} for p in paths],
                      'sources': [{'origin': 'source', 'path': name} for name in (
                          'board.c', 'util/ak820_capture_compile.py', 'util/ak820_default_keymap.py',
                          'util/ak820_pointer_compile_policy.py', 'util/ak820_pointer_compile_environment.py')],
                      'commands': [{'label': 'compile', 'argv': ['QMK_BIN=/tmp/qmk']}]}
            selected = config.profiles.configuration('pointer')
            with patch.object(config, 'QMK', root), patch.object(config, 'validate_pointer_commands',
                                                                 return_value=config.POINTER_POLICY):
                config.check_pointer_compiler_inputs(report, build, root / 'toolchain', selected)
                for field in ('artifacts', 'sources', 'commands'):
                    changed = copy.deepcopy(report)
                    changed[field] = []
                    with self.subTest(field=field), self.assertRaises(ValueError):
                        config.check_pointer_compiler_inputs(changed, build, root / 'toolchain', selected)
                capture.write_text('tampered')
                with self.assertRaisesRegex(ValueError, 'Unbound compiler artifact'):
                    config.check_pointer_compiler_inputs(report, build, root / 'toolchain', selected)
                capture.write_text('{}\n')
                changed = copy.deepcopy(report)
                changed['sources'] = [row for row in changed['sources'] if row['path'] != 'board.c']
                with self.assertRaisesRegex(ValueError, 'Unbound compiler dependency'):
                    config.check_pointer_compiler_inputs(changed, build, root / 'toolchain', selected)
                changed = copy.deepcopy(selected)
                changed['profile'] = 'main'
                with self.assertRaisesRegex(ValueError, 'Unknown compiler-input'):
                    config.check_pointer_compiler_inputs(report, build, root / 'toolchain', changed)
                report['compiler_input_contract'] = config.CANONICAL_POLICY
                report['sources'].append({'origin': 'source', 'path': 'util/ak820_profiles_compile_policy.py'})
                with patch.object(config, 'validate_canonical_commands', return_value=config.CANONICAL_POLICY) as canonical:
                    config.check_pointer_compiler_inputs(report, build, root / 'toolchain', selected)
                    canonical.assert_called_once()
                    del report['sources'][-1]
                    with self.assertRaisesRegex(ValueError, 'Missing compiler policy source'):
                        config.check_pointer_compiler_inputs(report, build, root / 'toolchain', selected)


if __name__ == '__main__':
    unittest.main()
