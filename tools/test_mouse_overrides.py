"""Offline Mouse Keys build configuration and flag binding tests."""
import ast
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import configure_firmware as config
import build_ak820
from build_ak820 import build_environment


class MouseOverrideTests(unittest.TestCase):
    def test_inherited_make_and_toolchain_injection_is_removed(self):
        injected = {'PATH': '/tools', 'SYSTEMROOT': 'C:/Windows', 'WINDIR': 'C:/Windows',
                    'NOLTO_CFLAGS': '--include keyboards/ajazz/ak820/override.h',
                    'CFLAGS': '--include override.h', 'MCUFLAGS': '--include override.h',
                    'OPT_DEFS': '-DAK820_MOUSE_CURSOR_STEP=9', 'MAKEFLAGS': '-e',
                    'GNUMAKEFLAGS': '-f injected.mk', 'CPATH': '/tmp/include',
                    'SDCC_HOME': '/tmp/sdcc', 'LD_PRELOAD': '/tmp/inject.so',
                    'PYTHONPATH': '/tmp/python', 'QMK_BIN': '/tmp/qmk'}
        self.assertEqual(build_environment(injected),
                         {key: injected[key] for key in ('PATH', 'SYSTEMROOT', 'WINDIR')})

    def test_builder_passes_filtered_environment_to_toolchain(self):
        injected = {'PATH': '/tools', 'NOLTO_CFLAGS': '--include override.h',
                    'CFLAGS': '--include override.h', 'CPATH': '/tmp/include',
                    'MAKEFLAGS': '-e', 'LD_PRELOAD': '/tmp/inject.so'}
        with tempfile.TemporaryDirectory(dir=config.QMK) as tmp:
            argv = ['build_ak820.py', '--profile', 'pointer', '--mouse-cursor-step', '9',
                    '--build-dir', str(Path(tmp) / 'build')]
            def version(command, *, env, text):
                self.assertEqual(set(env), {'PATH', 'QMK_HOME', 'AK820_BUILD_ID'})
                self.assertEqual(env['PATH'], '/tools')
                raise RuntimeError('stop before build')
            with patch.dict(build_ak820.os.environ, injected, clear=True), \
                 patch.object(build_ak820.sys, 'argv', argv), \
                 patch.object(build_ak820.shutil, 'which', return_value='/tools/sdcc'), \
                 patch.object(build_ak820.subprocess, 'check_output', side_effect=version), \
                 self.assertRaisesRegex(RuntimeError, 'stop before build'):
                build_ak820.main()

    def test_builder_explicitly_clears_indirect_make_flags(self):
        with tempfile.TemporaryDirectory(dir=config.QMK) as tmp:
            argv = ['build_ak820.py', '--profile', 'pointer', '--build-dir', str(Path(tmp) / 'build')]
            def compile_command(command, *, cwd, env, stdout, stderr, timeout):
                self.assertIn('NOLTO_CFLAGS=', command)
                self.assertIn('INIT_HOOK_CFLAGS=', command)
                self.assertNotIn('NOLTO_CFLAGS', env)
                raise RuntimeError('stop before compile')
            with patch.dict(build_ak820.os.environ, {'PATH': '/tools', 'NOLTO_CFLAGS': '--include override.h'}, clear=True), \
                 patch.object(build_ak820.sys, 'argv', argv), \
                 patch.object(build_ak820.shutil, 'which', return_value='/tools/sdcc'), \
                 patch.object(build_ak820.subprocess, 'check_output', return_value='version'), \
                 patch.object(build_ak820, 'validate_sdcc_version'), \
                 patch.object(build_ak820, 'input_snapshot', return_value={}), \
                 patch.object(build_ak820.subprocess, 'run', side_effect=compile_command), \
                 self.assertRaisesRegex(RuntimeError, 'stop before compile'):
                build_ak820.main()

    def test_configure_filters_environment_before_python_starts(self):
        injected = {'PATH': '/tools', 'PYTHONPATH': '/tmp/inject', 'PYTHONSTARTUP': '/tmp/startup',
                    'NOLTO_CFLAGS': '--include override.h', 'MAKEFLAGS': '-e',
                    'CPATH': '/tmp/include', 'LD_PRELOAD': '/tmp/inject.so'}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            context = root / 'context.json'; context.write_text('{}')
            def run(command, *, cwd, env, check):
                self.assertEqual(command[1], '-s')
                self.assertEqual(env, {'PATH': '/tools'})
                self.assertTrue(check)
                raise RuntimeError('stop before build')
            with patch.dict(config.os.environ, injected, clear=True), \
                 patch.object(config, 'QMK', root), \
                 patch.object(config, 'validate_tools', return_value=root), \
                 patch.object(config, 'source_identity', return_value={}), \
                 patch.object(config.subprocess, 'run', side_effect=run), \
                 self.assertRaisesRegex(RuntimeError, 'stop before build'):
                config.main(['build', '--profile', 'pointer', '--build-dir', str(root / 'build'),
                             '--parameter-spills-context', str(context)])

    def test_configuration_and_canonical_gate(self):
        p = config.profiles
        for name in ('pointer', 'onehand'):
            default = p.configuration(name)
            self.assertEqual(default, p.configuration(name, mouse_keys=dict(p.MOUSE_DEFAULTS)))
            for key in p.MOUSE_DEFAULTS:
                for bound in (1, 127 if key.endswith('step') else 255):
                    knobs = {**p.MOUSE_DEFAULTS, key: bound}
                    selected = p.configuration(name, mouse_keys=knobs)
                    self.assertEqual(p.validate_build_configuration(selected), selected)
                    if knobs != p.MOUSE_DEFAULTS:
                        with self.assertRaises(ValueError):
                            p.validate_configuration(selected)
            knobs = dict(p.MOUSE_DEFAULTS, cursor_step=13, cursor_period=7, wheel_step=3, wheel_period=9)
            selected = p.configuration(name, mouse_keys=knobs)
            self.assertEqual(selected['timing_ms']['mouse_cursor'], 7)
            self.assertEqual(selected['timing_ms']['mouse_wheel'], 9)
            for key in knobs:
                bad = dict(knobs, **{key: True})
                with self.assertRaises(ValueError): p.configuration(name, mouse_keys=bad)
                for bound in (0, 128 if key.endswith('step') else 256):
                    with self.assertRaises(ValueError): p.configuration(name, mouse_keys=dict(knobs, **{key: bound}))
            for field in ('mouse_keys', 'timing_ms', 'make_options'):
                bad = copy.deepcopy(selected); bad[field]['unexpected'] = 1
                with self.assertRaises(ValueError): p.validate_build_configuration(bad)
        with self.assertRaises(ValueError): p.configuration('main', mouse_keys=dict(p.MOUSE_DEFAULTS))

    def test_timing_metadata_rejects_bool_and_float_for_every_field(self):
        p = config.profiles
        for name in ('pointer', 'onehand'):
            for selected in (p.configuration(name), p.configuration(name, mouse_keys=dict(
                    p.MOUSE_DEFAULTS, cursor_period=1, wheel_period=1))):
                for field, value in selected['timing_ms'].items():
                    for invalid in (True, float(value)):
                        altered = copy.deepcopy(selected)
                        altered['timing_ms'][field] = invalid
                        with self.subTest(profile=name, field=field, invalid=invalid), \
                             self.assertRaisesRegex(ValueError, 'timing values must be integers'):
                            p.validate_build_configuration(altered)
                        if 'mouse_keys' not in selected:
                            with self.assertRaisesRegex(ValueError, 'timing values must be integers'):
                                p.validate_configuration(altered)

    def test_compiler_flags_are_bound_and_unambiguous(self):
        p = config.profiles
        selected = p.configuration('pointer', mouse_keys=dict(p.MOUSE_DEFAULTS, cursor_step=12))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); build = root / 'build'; flags = build / 'obj_ajazz_ak820_vial/cflags.txt'
            flags.parent.mkdir(parents=True)
            log = build / 'compile.log'; log.write_text('fixture')
            sources = []
            for path in ('util/build_ak820.py', 'keyboards/ajazz/ak820/ak820_mousekey.c'):
                target = root / path; target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((config.QMK / path).read_bytes())
                sources.append({'origin': 'source', 'path': path, 'sha256': config.sha(target)})
            feature = ['-D' + define for key, define in p.SWITCHES.items() if key in selected['optional_features']]
            feature += ['-DGRAVE_ESC_ENABLE'] if 'grave-escape' in selected['optional_features'] else []
            feature += ['-DNKRO_ENABLE'] if 'nkro' in selected['optional_features'] else []
            feature += ['-DVIALRGB_NO_DIRECT'] if 'vialrgb-direct' not in selected['optional_features'] else []
            mouse = ['-D' + define + '=' + str(selected['mouse_keys'][key]) for key, define in p.MOUSE_DEFINES.items()]
            def check(tokens, extra=(), records=None, omit_nolto=False):
                flags.write_text(' '.join(tokens))
                knobs = selected.get('mouse_keys', p.MOUSE_DEFAULTS)
                argv = ['make'] + ([] if omit_nolto else ['NOLTO_CFLAGS=']) + ['INIT_HOOK_CFLAGS='] + [define + '=' + str(knobs[key])
                        for key, define in p.MOUSE_DEFINES.items()]
                report = {'sources': sources if records is None else records, 'builder_sha256': sources[0]['sha256'],
                    'commands': [{'label': 'compile', 'argv': argv + list(extra), 'exit_code': 0,
                                        'log': log.relative_to(root).as_posix(), 'log_sha256': config.sha(log)}],
                    'artifacts': [{'path': flags.relative_to(root).as_posix(),
                    'sha256': config.sha(flags), 'size': flags.stat().st_size}]}
                with patch.object(config, 'QMK', root): config.check_feature_defines(report, build, selected)
            with self.assertRaisesRegex(ValueError, 'compiler-input contract is not closed'):
                check(feature + mouse)
            for bad in (feature + mouse[:-1], feature + mouse + [mouse[0]],
                        feature + ['-DAK820_MOUSE_CURSOR_STEP=7'] + mouse[1:],
                        feature + mouse + ['-UAK820_MOUSE_CURSOR_STEP'],
                        feature + mouse + ['-D', 'AK820_MOUSE_CURSOR_STEP=5']):
                with self.assertRaises(ValueError): check(bad)
            for records in (sources[1:], sources + sources[:1], [sources[0]],
                            [dict(sources[0], sha256='0' * 64), sources[1]]):
                with self.assertRaises(ValueError): check(feature + mouse, records=records)
            with self.assertRaisesRegex(ValueError, 'NOLTO_CFLAGS'):
                check(feature + mouse, omit_nolto=True)
            for extra in (['NOLTO_CFLAGS=--include override.h'],
                          ['INIT_HOOK_CFLAGS=-DAK820_MOUSE_CURSOR_STEP=5'],
                          ['AK820_MOUSE_CURSOR_STEP=5']):
                with self.assertRaises(ValueError): check(feature + mouse, extra)
            with self.assertRaisesRegex(ValueError, 'compiler-input contract is not closed'):
                check(feature + mouse)
            selected = p.configuration('pointer')
            default_flags = ['-D' + define + '=' + str(p.MOUSE_DEFAULTS[key])
                             for key, define in p.MOUSE_DEFINES.items()]
            with self.assertRaisesRegex(ValueError, 'compiler-input contract is not closed'):
                check(feature + default_flags)
            with self.assertRaises(ValueError): check(feature, records=sources[1:])
            with self.assertRaises(ValueError): check(feature)

    def test_historical_flag_exception_requires_pinned_pair(self):
        p = config.profiles
        selected = p.configuration('pointer')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); build = root / 'build'; flags = build / 'obj_ajazz_ak820_vial/cflags.txt'
            flags.parent.mkdir(parents=True)
            sources = []
            for path, digest in (('util/build_ak820.py', '5d6e4f9eacab8bfe5e2b6e34f376f5825e60eba3a5c9b60900755bee3fd7bc01'),
                                 ('keyboards/ajazz/ak820/ak820_mousekey.c', '359a0fc97c2239090b84812a5000ed5dd8b6a91bdb5b14e62489857cb5949b25')):
                target = root / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_text('new source')
                sources.append({'origin': 'source', 'path': path, 'sha256': digest})
            flags.write_text(' '.join(['-D' + define for key, define in p.SWITCHES.items()
                                      if key in selected['optional_features']] + ['-DVIALRGB_NO_DIRECT']))
            report = {'sources': sources, 'builder_sha256': sources[0]['sha256'], 'artifacts': [
                {'path': flags.relative_to(root).as_posix(), 'sha256': config.sha(flags), 'size': flags.stat().st_size}]}
            with patch.object(config, 'QMK', root):
                config.check_feature_defines(report, build, selected)
                for records in (sources[1:], [sources[0], dict(sources[1], sha256='0' * 64)], sources + sources[:1]):
                    with self.assertRaises(ValueError): config.check_feature_defines({**report, 'sources': records}, build, selected)
                with self.assertRaises(ValueError): config.check_feature_defines({**report, 'builder_sha256': '0' * 64}, build, selected)

    def test_linked_send_count_oracle_at_period_endpoints(self):
        path = config.QMK / 'tests/ak820_mousekeys/run.py'
        tree = ast.parse(path.read_text())
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'cadence_case')
        namespace = {'key': lambda fw, code: [], 'tick': lambda fw, time: fw.clock(time)}
        exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), 'exec'), namespace)
        class Fixture:
            def __init__(self, duplicate=False): self.clocks = []; self.duplicate = duplicate
            def address(self, symbol): return 0x100
            def clock(self, value): self.clocks.append(value); return []
            def write(self, *args): return []
            def dump_symbol(self, *args): return []
            def extract(self, segment, label, address, size):
                return [0xa5] * 6 if label in ('before@', 'no_catchup@') else [2, 0, 8, 0, 0, 0]
            def execute(self, name, commands):
                counts = [1, 0, 1, 2 if self.duplicate else 1, 0]
                labels = ('first', 'before', 'repeat', 'long_gap', 'no_catchup')
                log = ''.join('@@BEGIN_' + label + '\n' + '@@MOUSE_SEND\n' * count +
                              '@@END_' + label + '\n' for label, count in zip(labels, counts))
                return log, {}
        for period in (1, 255):
            for duplicate in (False, True):
                fixture = Fixture(duplicate)
                result = namespace['cadence_case'](fixture, [], 'fixture', 0xd0, period,
                                                    [2, 0, 8, 0, 0, 0], 65530)
                self.assertEqual(result['pass'], not duplicate)
                self.assertEqual(fixture.clocks, [65530, (65530 + period - 1) & 65535,
                    (65530 + period) & 65535, (65530 + period + 1000) & 65535,
                    (65530 + period + 1000) & 65535])

    def test_release_rejects_unverified_compiler_inputs(self):
        with self.assertRaisesRegex(ValueError, 'Unverified compiler-input contract'):
            config.profiles.require_release_qualification({
                'configuration': config.profiles.configuration('pointer'),
                'compiler_input_contract': 'unverified'})

    def test_release_requires_pinned_historical_pair_not_a_marker(self):
        import ak820_release_safety
        p = config.profiles
        builder, mouse = p.HISTORICAL_COMPILER_INPUT_PAIR
        records = [{'origin': 'source', 'path': path, 'sha256': digest} for path, digest in (
            ('util/build_ak820.py', builder),
            ('keyboards/ajazz/ak820/ak820_mousekey.c', mouse))]
        report = {'configuration': p.configuration('pointer'), 'builder_sha256': builder, 'sources': records}
        with patch.object(ak820_release_safety, 'validate') as validate:
            p.require_release_qualification(report)
            validate.assert_called_once_with(report)
            for marker in ('unverified', 'ak820-compiler-inputs-1', 'unknown', None):
                for candidate in (report, {'builder_sha256': next(iter(p.LEGACY_BUILDERS))}):
                    with self.subTest(marker=marker, configured='configuration' in candidate), self.assertRaises(ValueError):
                        p.require_release_qualification({**candidate, 'compiler_input_contract': marker})
            for sources in (records[:1], records + records[:1],
                            [records[0], {**records[1], 'sha256': '0' * 64}]):
                with self.assertRaises(ValueError):
                    p.require_release_qualification({**report, 'sources': sources})
            with self.assertRaises(ValueError):
                p.require_release_qualification({**report, 'builder_sha256': '0' * 64})
            self.assertEqual(validate.call_count, 1)

    def test_release_witness_rejects_variant(self):
        import ak820_release_safety
        selected = config.profiles.configuration('pointer', mouse_keys=dict(config.profiles.MOUSE_DEFAULTS, cursor_step=9))
        with self.assertRaises(ValueError):
            ak820_release_safety.manifest_name(selected)

    def test_plan_carries_selected_values(self):
        p = config.profiles
        selected = p.configuration('pointer', mouse_keys=dict(p.MOUSE_DEFAULTS, wheel_period=17))
        plan = config.profile_test_plan('pointer', Path('/build'), Path('/tools'), selected)
        for name, _, command in plan:
            if name in ('mouse-keys-host', 'mouse-keys-linked'):
                index = command.index('--mouse-wheel-period')
                self.assertEqual(command[index + 1], '17')


if __name__ == '__main__':
    unittest.main()
