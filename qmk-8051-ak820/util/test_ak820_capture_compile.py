import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from pathlib import Path

from ak820_build_inputs import digest
from ak820_capture_compile import main as capture_main, validate_default_keymap, validate_manifest
from ak820_default_keymap import run_compiler

SCRIPT = Path(__file__).with_name('ak820_capture_compile.py')


class CaptureTest(unittest.TestCase):
    def trust(self, build, objects):
        self.enterContext(patch.dict(os.environ, {'AK820_CAPTURE_BUILD_ROOT': str(build.resolve()),
                                                   'AK820_CAPTURE_OBJECT_ROOT': str(objects.resolve())}))

    def test_records_ordered_arguments_and_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / 'object.o.compile.json'
            self.trust(record.parent.parent, record.parent)
            command = [sys.executable, str(SCRIPT), str(record), str(record.parent.parent), str(record.parent), '--', sys.executable,
                       '-c', 'import sys; sys.exit(7)', '--include', 'x.h']
            result = subprocess.run(command, check=False)
            self.assertEqual(result.returncode, 7)
            data = json.loads(record.read_text())
            self.assertEqual(data['argv'], command[6:])
            self.assertEqual(data['exit_code'], 7)
            self.assertEqual(data['cwd'], str(Path.cwd()))
            original = record.read_bytes()
            result = subprocess.run(command, capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(record.read_bytes(), original)

    def test_concurrent_claim_prevents_second_compiler(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record, started, release, second = (root / name for name in ('capture.o.compile.json', 'started', 'release', 'second'))
            self.trust(record.parent.parent, record.parent)
            code = ("import pathlib, sys, time; "
                    "pathlib.Path(sys.argv[1]).touch(); "
                    "\nwhile not pathlib.Path(sys.argv[2]).exists(): time.sleep(0.01)")
            first = subprocess.Popen([sys.executable, str(SCRIPT), str(record), str(record.parent.parent), str(record.parent), '--',
                                      sys.executable, '-c', code, str(started), str(release)])
            try:
                deadline = time.monotonic() + 5
                while not started.exists() and first.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertTrue(started.exists(), 'first compiler did not start')
                self.assertIsNone(json.loads(record.read_text())['exit_code'])
                competitor = subprocess.run([sys.executable, str(SCRIPT), str(record), str(record.parent.parent), str(record.parent), '--',
                                             sys.executable, '-c', 'import pathlib, sys; pathlib.Path(sys.argv[1]).touch()',
                                             str(second)], capture_output=True, timeout=5, check=False)
                self.assertNotEqual(competitor.returncode, 0)
                self.assertFalse(second.exists())
            finally:
                release.touch()
                first.wait(timeout=5)
            self.assertEqual(first.returncode, 0)
            self.assertEqual(json.loads(record.read_text())['exit_code'], 0)

    def test_failed_launch_retains_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / 'capture.o.compile.json'
            self.trust(record.parent.parent, record.parent)
            command = [sys.executable, str(SCRIPT), str(record), str(record.parent.parent), str(record.parent), '--', str(Path(directory) / 'missing'), '--version']
            result = subprocess.run(command, capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIsNone(json.loads(record.read_text())['exit_code'])
            self.assertNotEqual(subprocess.run(command, capture_output=True, check=False).returncode, 0)

    @unittest.skipUnless(os.name == 'posix', 'POSIX signals required')
    def test_signalled_compiler_retains_failed_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / 'capture.o.compile.json'
            code = 'import os, signal; os.kill(os.getpid(), signal.SIGTERM)'
            self.trust(record.parent.parent, record.parent)
            command = [sys.executable, str(SCRIPT), str(record), str(record.parent.parent), str(record.parent), '--', sys.executable, '-c', code]
            result = subprocess.run(command, capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(record.read_text())['exit_code'], -signal.SIGTERM)
            self.assertNotEqual(subprocess.run(command, capture_output=True, check=False).returncode, 0)

    @unittest.skipUnless(os.name == 'posix', 'POSIX signals required')
    def test_interrupted_wrapper_retains_incomplete_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            record, started = (Path(directory) / name for name in ('capture.o.compile.json', 'started'))
            self.trust(record.parent.parent, record.parent)
            code = 'import pathlib, sys, time; pathlib.Path(sys.argv[1]).touch(); time.sleep(30)'
            process = subprocess.Popen([sys.executable, str(SCRIPT), str(record), str(record.parent.parent), str(record.parent), '--',
                                        sys.executable, '-c', code, str(started)], start_new_session=True)
            try:
                deadline = time.monotonic() + 5
                while not started.exists() and process.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertTrue(started.exists(), 'compiler did not start')
            finally:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=5)
            self.assertIsNone(json.loads(record.read_text())['exit_code'])
            result = subprocess.run([sys.executable, str(SCRIPT), str(record), str(record.parent.parent), str(record.parent), '--', sys.executable, '-c', 'pass'],
                                    capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)

    @unittest.skipIf(os.name == 'nt', 'make recipe requires POSIX shell quoting')
    @unittest.skipUnless(shutil.which('make'), 'make is not installed')
    def test_direct_make_capture_omits_secret_including_nested(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outer = root / 'unit.o.compile.json'
            nested = root / 'nested.json'
            sentinel = 'ak820-secret-sentinel-94f3'
            code = ("import json, os, sys; "
                    f"sys.path.insert(0, {str(SCRIPT.parent)!r}); "
                    "from ak820_default_keymap import run_compiler; "
                    "records = []; "
                    "assert sys.flags.no_user_site == 1; "
                    "assert 'AK820_TEST_SECRET' not in os.environ; "
                    "assert 'MAKEFLAGS' not in os.environ; "
                    "assert sys.argv[1:] == ['-DAK820_BUILD_ID=0x82003']; "
                    "os.environ['AK820_TEST_SECRET'] = 'injected'; "
                    "run_compiler([sys.executable, '-s', '-c', \"import os, sys; assert sys.flags.no_user_site == 1; assert 'AK820_TEST_SECRET' not in os.environ\"], records); "
                    f"open({str(nested)!r}, 'w').write(json.dumps(records))")
            command = [sys.executable, '-s', str(SCRIPT), str(outer), str(root.parent), str(root), '--', sys.executable, '-s', '-c', code,
                       '-DAK820_BUILD_ID=0x82003']
            (root / 'Makefile').write_text('.PHONY: all\nall:\n\t' + shlex.join(command) + '\n')
            env = {'PATH': os.environ.get('PATH', ''), 'AK820_CAPTURE_COMPILE': 'yes',
                   'AK820_CAPTURE_BUILD_ROOT': str(root.parent), 'AK820_CAPTURE_OBJECT_ROOT': str(root),
                   'AK820_TEST_SECRET': sentinel, 'SYSTEMROOT': 'test-root', 'WINDIR': 'test-windir',
                   'PYTHONUSERBASE': str(root / 'userbase')}
            usersite = Path(subprocess.check_output([sys.executable, '-m', 'site', '--user-site'],
                                                    env=env, text=True).strip())
            usersite.mkdir(parents=True)
            marker = root / 'user-site-loaded'
            (usersite / 'sitecustomize.py').write_text(f'open({str(marker)!r}, "w").write("loaded")\n')
            result = subprocess.run(['make', '-f', 'Makefile'], cwd=root, env=env,
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
            rules = (SCRIPT.parent.parent / 'builddefs/common_rules.mk').read_text()
            self.assertIn('python3 -s util/ak820_capture_compile.py', rules)
            self.assertIn('python3 -s util/ak820_default_keymap.py', rules)
            expected = {key: env[key] for key in ('PATH', 'SYSTEMROOT', 'WINDIR', 'AK820_CAPTURE_BUILD_ROOT', 'AK820_CAPTURE_OBJECT_ROOT')}
            self.assertEqual(json.loads(outer.read_text())['environment'], expected)
            self.assertEqual(json.loads(nested.read_text())[0]['environment'], expected)
            self.assertNotIn(sentinel, outer.read_text())
            self.assertNotIn(sentinel, nested.read_text())

    def test_stale_dependency_is_removed_and_missing_is_not_fresh(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'obj_test'
            root.mkdir()
            self.trust(root.parent, root)
            dep, record = root / 'unit.d', root / 'unit.o.compile.json'
            dep.write_text('stale')
            command = ['sdcc', '-c', '-Wp,-MD,-MF,' + str(dep), 'unit.c', '-o', str(root / 'unit.o')]
            with patch('ak820_capture_compile.subprocess.run') as run:
                def fake(*args, **kwargs):
                    self.assertFalse(dep.exists())
                    return subprocess.CompletedProcess(command, 0)
                run.side_effect = fake
                with self.assertRaisesRegex(ValueError, 'did not generate dependency file'):
                    capture_main([str(record), str(root.parent), str(root), '--'] + command)
            self.assertNotIn('fresh_dependency', json.loads(record.read_text()))
            dep.write_text('stale')
            with patch('ak820_default_keymap.subprocess.run') as run:
                run.side_effect = lambda *a, **kw: subprocess.CompletedProcess(command, 0)
                with self.assertRaisesRegex(ValueError, 'did not generate'):
                    run_compiler(command, [], dependency=dep)
            self.assertFalse(dep.exists())

    def test_capture_binds_fresh_generated_header(self):
        with tempfile.TemporaryDirectory() as directory:
            obj = Path(directory) / 'obj_test'
            obj.mkdir()
            self.trust(obj.parent, obj)
            source, header = obj / 'unit.c', obj / 'generated.h'
            source.write_text('')
            header.write_text('stable')
            dep, record = obj / 'unit.d', obj / 'unit.o.compile.json'
            command = ['sdcc', '-c', '-Wp,-MD,-MF,' + str(dep), str(source), '-o', str(obj / 'unit.o')]
            def fake(*args, **kwargs):
                dep.write_text('unit.o: ' + str(source) + ' ' + str(header) + '\n')
                return subprocess.CompletedProcess(command, 0)
            with patch('ak820_capture_compile.subprocess.run', side_effect=fake):
                self.assertEqual(capture_main([str(record), str(obj.parent), str(obj), '--'] + command), 0)
            saved = json.loads(record.read_text())
            self.assertEqual(saved['fresh_dependency'], str(dep))
            self.assertEqual(saved['generated_inputs'], {str(source): digest(source), str(header): digest(header)})

    def test_capture_rejects_generated_header_change(self):
        with tempfile.TemporaryDirectory() as directory:
            obj = Path(directory) / 'obj_test'
            obj.mkdir()
            self.trust(obj.parent, obj)
            source, header = obj / 'unit.c', obj / 'generated.h'
            source.write_text('')
            header.write_text('before')
            dep, record = obj / 'unit.d', obj / 'unit.o.compile.json'
            command = ['sdcc', '-c', '-Wp,-MD,-MF,' + str(dep), str(source), '-o', str(obj / 'unit.o')]
            def fake(*args, **kwargs):
                dep.write_text('unit.o: ' + str(source) + ' ' + str(header) + '\n')
                header.write_text('after')
                return subprocess.CompletedProcess(command, 0)
            with patch('ak820_capture_compile.subprocess.run', side_effect=fake):
                with self.assertRaisesRegex(ValueError, 'Generated compiler input changed'):
                    capture_main([str(record), str(obj.parent), str(obj), '--'] + command)
            self.assertIsNone(json.loads(record.read_text())['exit_code'])

    def test_explicit_roots_nested_relative_and_wrong_roots(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            build = base / 'obj_collision' / 'build'
            obj = build / 'obj_test'
            nested = obj / '.build' / 'build' / 'obj_test' / 'src'
            nested.mkdir(parents=True)
            self.trust(build, obj)
            source, header = obj / 'source.c', obj / 'generated.h'
            source.write_text('source')
            header.write_text('header')
            record = nested / 'default_keyboard.o.compile.json'
            dep = nested / 'default_keyboard.d'
            old = Path.cwd()
            os.chdir(base)
            try:
                rel = lambda path: str(path.relative_to(base))
                output = rel(record)[:-len('.compile.json')]
                command = ['sdcc', '-c', '-Wp,-MD,-MF,' + rel(dep), rel(source), '-o', output]
                def fake(*args, **kwargs):
                    dep.write_text('default_keyboard.o: ' + rel(source) + ' ' + rel(header) + '\n')
                    return subprocess.CompletedProcess(command, 0)
                with patch('ak820_capture_compile.subprocess.run', side_effect=fake):
                    capture_main([rel(record), rel(build), rel(obj), '--'] + command)
                self.assertEqual(json.loads(record.read_text())['generated_inputs'],
                                 {str(source): digest(source), str(header): digest(header)})
                record.unlink()
                for bad_build, bad_obj in ((base, obj), (nested.parent.parent, obj), (build, build),
                                           (build, base / 'obj_collision' / 'build-other')):
                    with self.assertRaisesRegex(ValueError, 'Invalid compiler build or output root'):
                        capture_main([rel(record), rel(bad_build), rel(bad_obj), '--'] + command)
                    self.assertFalse(record.exists())
                with patch.dict(os.environ, {'AK820_CAPTURE_BUILD_ROOT': ''}):
                    with self.assertRaisesRegex(ValueError, 'Invalid compiler build or output root'):
                        capture_main([rel(record), rel(build), rel(obj), '--'] + command)
                self.assertFalse(record.exists())
                dep.write_text('preserve')
                with self.assertRaisesRegex(ValueError, 'dependency/output mismatch'):
                    capture_main([rel(record), rel(build), rel(obj), '--'] + command[:-1] + ['other.o'])
                self.assertEqual(dep.read_text(), 'preserve')
            finally:
                os.chdir(old)

    def test_new_generated_header_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            obj = Path(directory) / 'obj_test'
            obj.mkdir()
            self.trust(obj.parent, obj)
            source, header = obj / 'unit.c', obj / 'new.h'
            source.write_text('source')
            dep, record = obj / 'unit.d', obj / 'unit.o.compile.json'
            command = ['sdcc', '-c', '-Wp,-MD,-MF,' + str(dep), str(source), '-o', str(obj / 'unit.o')]
            def fake(*args, **kwargs):
                header.write_text('new')
                dep.write_text('unit.o: ' + str(source) + ' ' + str(header) + '\n')
                return subprocess.CompletedProcess(command, 0)
            with patch('ak820_capture_compile.subprocess.run', side_effect=fake):
                with self.assertRaisesRegex(ValueError, 'Generated compiler input changed'):
                    capture_main([str(record), str(obj.parent), str(obj), '--'] + command)
            self.assertIsNone(json.loads(record.read_text())['exit_code'])

    def test_default_keymap_roots_for_legacy_and_captured_nested_output(self):
        from ak820_default_keymap import compile_current
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            compiler = root / 'toolchain/bin/sdcc'
            compiler.parent.mkdir(parents=True)
            compiler.write_text('compiler')
            for nested in (False, True):
                build = root / ('nested' if nested else 'legacy')
                obj = build / 'obj_test'
                parent = obj / ('obj_test/src' if nested else 'quantum')
                parent.mkdir(parents=True)
                output = parent / 'keymap.o'
                primary = root / 'keymap.c'
                primary.write_text('source')
                dep = output.with_suffix('.d')
                argv = ['sdcc', '-c', '--model-large', '-Wp,-MD,-MF,' + str(dep), str(primary), '-o', str(output)]
                build_root = build / 'default-keymap'
                env = ({'AK820_CAPTURE_BUILD_ROOT': str(build), 'AK820_CAPTURE_OBJECT_ROOT': str(obj)}
                       if nested else {})
                def fake(command, invocations, dependency=None, **kwargs):
                    if command[-1] == '--version':
                        return subprocess.CompletedProcess(command, 0, stdout='4.6.0')
                    if dependency is not None:
                        include = build_root / 'ak820_default_keymap.inc'
                        extra = ' ' + str(include) if include.is_file() else ''
                        dependency.write_text('keymap.o: ' + str(primary) + extra + '\n')
                    if '-S' in command:
                        (build_root / 'bootstrap.asm').write_text('asm')
                    elif '-c' in command:
                        output.with_suffix('.asm').write_text('asm')
                    return subprocess.CompletedProcess(command, 0)
                with patch.dict(os.environ, env, clear=True), \
                     patch('ak820_default_keymap.shutil.which', return_value=str(compiler)), \
                     patch('ak820_default_keymap.input_snapshot', return_value={primary: digest(primary)}), \
                     patch('ak820_default_keymap.run_compiler', side_effect=fake), \
                     patch('ak820_default_keymap.generate', return_value='generated'), \
                     patch('ak820_default_keymap.verify_final'):
                    compile_current(argv)
                self.assertTrue((build_root / 'generation.json').is_file())

    def test_nested_compiler_commands_reject_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / 'build'
            (build / 'default-keymap').mkdir(parents=True)
            obj = build / 'obj' / 'quantum' / 'keymap.o'
            dep = obj.with_suffix('.d')
            base = [str(Path(sys.executable).resolve()), '-c', '-Wp,-MD,-MF,' + str(dep),
                    'keymap.c', '-o', str(obj)]
            wrapper = {'argv': ['python3', '-s', 'util/ak820_default_keymap.py'] + base,
                       'cwd': str(root), 'environment': {'PATH': str(Path(sys.executable).parent)}}
            capture = build / 'keymap.o.compile.json'
            capture.write_text(json.dumps(wrapper))
            keydir = build / 'default-keymap'
            prefix = [base[0], '-S', '-Wp,-MD,-MF,' + str(keydir / 'bootstrap.d'),
                      'keymap.c', '-DAK820_DEFAULT_KEYMAP_EXTRACT']
            dependency = prefix.copy()
            dependency[1] = '-E'
            bootstrap = prefix + ['-o', str(keydir / 'bootstrap.asm')]
            final = base + ['-I' + str(keydir)]
            discovery = [base[0], '-E', '-Wp,-MD,-MF,' + str(keydir / 'final-discovery.d'),
                         'keymap.c', '-I' + str(keydir)]
            commands = [[base[0], '--version'], dependency, bootstrap, discovery, final]
            records = [{'argv': command, 'cwd': str(root), 'environment': wrapper['environment'],
                        'exit_code': 0, **({'fresh_dependency': next(
                            a.removeprefix('-Wp,-MD,-MF,') for a in command if a.startswith('-Wp,-MD,-MF,'))}
                                           if index else {})}
                       for index, command in enumerate(commands)]
            generation = build / 'default-keymap/generation.json'
            source = root / 'keymap.c'
            source.write_text('')
            meta = {}
            for name, hash_key, paths_key in (('bootstrap.d', 'dependency_sha256', 'dependencies'),
                                               ('final-discovery.d', 'final_dependency_sha256', 'final_dependencies')):
                path = keydir / name
                path.write_text('keymap.o: keymap.c\n')
                meta[hash_key] = digest(path)
                meta[paths_key] = {str(source): digest(source)}
            generation.write_text(json.dumps({'compiler_invocations': records, **meta}))
            validate_default_keymap([capture], build)
            for change in ('argv', 'cwd', 'environment', 'exit_code', 'fresh_dependency'):
                bad = [dict(item) for item in records]
                bad[-1][change] = None
                generation.write_text(json.dumps({'compiler_invocations': bad, **meta}))
                with self.assertRaises(ValueError):
                    validate_default_keymap([capture], build)

    def test_manifest_rejects_missing_extra_and_malformed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / 'build'
            build.mkdir()
            obj = build / 'obj_target'
            obj.mkdir()
            record = obj / 'unit.o.compile.json'
            data = {'cwd': str(root), 'argv': ['sdcc', '-c', 'unit.c', '-o', 'build/obj_target/unit.o'],
                    'environment': {'AK820_CAPTURE_BUILD_ROOT': str(build), 'AK820_CAPTURE_OBJECT_ROOT': str(obj)},
                    'exit_code': 0, 'fresh_dependency': 'build/obj_target/unit.d'}
            record.write_text(json.dumps(data))
            self.assertEqual(validate_manifest(root, build, ['build/obj_target/unit.rel'], obj), [record])
            for objects in ([], ['build/obj_target/unit.rel'] * 2, ['build/missing.rel']):
                with self.assertRaises(ValueError):
                    validate_manifest(root, build, objects, obj)
            for change in ({'exit_code': 1}, {'fresh_dependency': None},
                           {'argv': ['sdcc', '-c', 'unit.c', '-o', 'wrong.o']},
                           {'argv': ['sdcc', '-c', 4, '-o', 'build/obj_target/unit.o']},
                           {'environment': {'AK820_CAPTURE_BUILD_ROOT': str(build), 'AK820_CAPTURE_OBJECT_ROOT': str(build)}}):
                record.write_text(json.dumps({**data, **change}))
                with self.assertRaises(ValueError):
                    validate_manifest(root, build, ['build/obj_target/unit.rel'], obj)


if __name__ == '__main__':
    unittest.main()
