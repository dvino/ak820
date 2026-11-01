import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import types
import sys
import subprocess
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('prepare_release', HERE / 'prepare_release.py')
producer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(producer)


class EvidenceOutput(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'audits' / 'old').mkdir(parents=True)
        (self.root / 'tools' / 'installer').mkdir(parents=True)
        (self.root / 'web').mkdir()
        self.root_patch = patch.object(producer, 'ROOT', self.root)
        self.audit_patch = patch.object(producer, 'AUDIT', self.root / 'audits' / 'old')
        self.root_patch.start(); self.audit_patch.start()
        self.addCleanup(self.root_patch.stop); self.addCleanup(self.audit_patch.stop)

    def test_fresh_and_unsafe_paths(self):
        (self.root / 'link').symlink_to(self.root / 'audits', target_is_directory=True)
        (self.root / 'audits' / 'leaf').symlink_to(self.root / 'absent')
        for path in ('/tmp/output', 'audits/../output', 'link/new', 'audits/leaf',
                     'audits/old/new', 'tools/new', 'audits', 'audits/input/new'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                producer.fresh_evidence(Path(path), [self.root / 'audits' / 'input'])
        output = producer.fresh_evidence(Path('audits/new'))
        self.assertEqual(output, self.root / 'audits' / 'new')
        with self.assertRaises(ValueError):
            producer.fresh_evidence(Path('audits/new'))

    def test_both_catalogs_must_match_exact_bytes(self):
        catalog = {'profiles': []}
        data = (json.dumps(catalog, indent=2, sort_keys=True) + '\n').encode()
        targets = [self.root / 'tools/installer/settings-catalog.json', self.root / 'web/firmware-matrix.json']
        for target in targets:
            target.write_bytes(data)
        producer.require_frozen_catalog(catalog)
        for target in targets:
            target.write_bytes(data + b' ')
            with self.assertRaises(ValueError):
                producer.require_frozen_catalog(catalog)
            target.write_bytes(data)

    def test_invalid_profile_before_reservation_or_subprocess(self):
        marker = self.root / 'audits/old/historical.json'
        marker.write_bytes(b'history')
        arguments = ['producer', '--builds-root', str(self.root), '--toolchain', str(self.root),
                     '--oem-reference-dir', str(self.root), '--private-output', str(self.root.parent / 'not-created-private'),
                     '--historical-catalog', str(marker), '--source-backups-root', str(self.root),
                     '--profile-build', 'bad=missing', '--evidence-output', 'audits/new']
        with patch.object(sys, 'argv', arguments), patch.object(subprocess, 'run') as run:
            with self.assertRaises(ValueError):
                producer.main()
        run.assert_not_called()
        self.assertFalse((self.root / 'audits/new').exists())
        self.assertEqual(marker.read_bytes(), b'history')

    def test_entrypoint_rejects_cross_kind_and_reserved_labels_before_output(self):
        marker = self.root / 'audits/old/history'
        marker.write_bytes(b'unchanged')
        backups = self.root / 'backups'
        backups.mkdir()
        (backups / 'saved').mkdir()
        (backups / 'saved/manifest.json').write_text('{}')
        rom = self.root / 'rom'
        rom.write_bytes(b'rom')
        bundle = self.root / 'bundle'
        bundle.mkdir()
        private = self.root.parent / (self.root.name + '-private')
        base = ['producer', '--builds-root', str(self.root), '--toolchain', str(self.root),
                '--oem-reference-dir', str(self.root), '--private-output', str(private),
                '--historical-catalog', str(marker), '--source-backups-root', str(backups),
                '--evidence-output', 'audits/new']
        for extra in (['--source-rom', 'same=' + str(rom), '--source-bundle', 'same=' + str(bundle)],
                      ['--source-rom', 'saved=' + str(rom)],
                      ['--source-rom', 'fresh-main=' + str(rom)]):
            with self.subTest(extra=extra), patch.object(sys, 'argv', base + extra), \
                 patch.object(subprocess, 'run') as run, self.assertRaises(ValueError):
                producer.main()
            run.assert_not_called()
            self.assertFalse((self.root / 'audits/new').exists())
            self.assertFalse(private.exists())
            self.assertEqual(marker.read_bytes(), b'unchanged')

    def test_entrypoint_rejects_historical_identity_before_output(self):
        names = list(producer.beta_policy.BETA4_IDENTITIES)
        builds = self.root / 'qmk-8051-ak820/build'
        for name in names:
            build = builds / name
            for leaf in ('build-report.json', 'ajazz_ak820_vial.ihx', 'ajazz_ak820_vial.map',
                         'runtime-stack.json', 'runtime-safety/summary.json',
                         'runtime-safety/startup.json', 'runtime-safety/irq/results.json'):
                path = build / leaf
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'input')
        oem = self.root / 'oem'
        oem.mkdir()
        for leaf in ('stock-full.bin', 'native-installed.bin'):
            (oem / leaf).write_bytes(b'oem')
        backups = self.root / 'backups'
        backups.mkdir()
        historical = self.root / 'historical'
        historical.mkdir()
        marker = self.root / 'audits/old/history'
        marker.write_bytes(b'unchanged')
        old = {'profiles': [{'profile': name, 'settings_identity': {'ihx_sha256': 'good', 'code_sha256': 'good'}} for name in names]}
        fake = types.SimpleNamespace(pack=types.SimpleNamespace(validate_native=lambda *a: None),
                    _catalog_images=lambda catalog: None,
                    load_profile=lambda *a, **k: {'ihx_sha256': 'bad', 'code_sha256': 'good'})
        modules = {'settings_backup': fake, 'firmware_matrix': types.SimpleNamespace(candidate_names=lambda: tuple(names)),
                   'build_ci_release': types.SimpleNamespace()}
        private = self.root.parent / (self.root.name + '-private')
        arguments = ['producer', '--builds-root', str(builds), '--toolchain', str(self.root),
                     '--oem-reference-dir', str(oem), '--private-output', str(private),
                     '--historical-catalog', str(marker), '--source-backups-root', str(backups),
                     '--historical-bundles-root', str(historical), '--evidence-output', 'audits/new']
        with patch.object(sys, 'argv', arguments), patch.dict(sys.modules, modules), \
             patch.object(producer.beta_policy, 'load_previous_catalog', return_value=old), \
             patch.object(producer.beta_policy, 'previous_source_catalog', return_value={}), \
             patch.object(producer, 'preflight_origin'), patch.object(producer, 'preflight_backup_files'), \
             patch.object(subprocess, 'run') as run, self.assertRaisesRegex(ValueError, 'Historical build identity differs'):
            producer.main()
        run.assert_not_called()
        self.assertFalse((self.root / 'audits/new').exists())
        self.assertFalse(private.exists())
        self.assertEqual(marker.read_bytes(), b'unchanged')

    def test_policy_entrypoint_rejects_unsupported_target_before_output(self):
        names = list(producer.beta_policy.BETA4_IDENTITIES)
        builds = self.root / 'qmk-8051-ak820/build'
        rows = []
        for name in names:
            rows.append({'profile': name, 'settings_identity': {'ihx_sha256': name, 'code_sha256': name}})
            for leaf in ('build-report.json', 'ajazz_ak820_vial.ihx', 'ajazz_ak820_vial.map',
                         'runtime-stack.json', 'runtime-safety/summary.json',
                         'runtime-safety/startup.json', 'runtime-safety/irq/results.json'):
                path = builds / name / leaf
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(name.encode())
        definition = self.root / 'qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/vial.json'
        definition.parent.mkdir(parents=True)
        definition.write_bytes(b'{}')
        for leaf in ('tools/installer/settings-catalog.json', 'web/firmware-matrix.json'):
            (self.root / leaf).write_text(json.dumps({'profiles': rows}))
        oem = self.root / 'oem'
        oem.mkdir()
        for leaf in ('stock-full.bin', 'native-installed.bin'):
            (oem / leaf).write_bytes(b'oem')
        backups = self.root / 'backups'
        (backups / 'saved').mkdir(parents=True)
        (backups / 'saved/manifest.json').write_text('{}')
        marker = self.root / 'audits/old/history'
        marker.write_bytes(b'unchanged')
        record = self.root / 'settings-run.json'
        record.write_text(json.dumps({'exit_code': 0, 'command': ['test'], 'source_files': {'x': 'digest'},
                                      'log_path': 'x', 'log_sha256': 'digest',
                                      'unit_tests': {'run': 1, 'skipped': 0}}))
        def load_profile(root, stock, trusted_catalog, release_files):
            name = release_files['firmware/application.ihx'].decode()
            return {'ihx_sha256': name, 'code_sha256': name}
        def plan(backup, profile):
            if profile['ihx_sha256'] == names[-1]:
                raise ValueError('Unsupported keycode')
        fake = types.SimpleNamespace(pack=types.SimpleNamespace(validate_native=lambda *a: None),
                 _catalog_images=lambda catalog: None, load_profile=load_profile,
                 validate_backup=lambda *a: {'source_identity': ('source', 'code')}, plan_restore=plan)
        old = {'profiles': rows}
        modules = {'settings_backup': fake, 'firmware_matrix': types.SimpleNamespace(candidate_names=lambda: tuple(names)),
                   'build_ci_release': types.SimpleNamespace()}
        private = self.root.parent / (self.root.name + '-private')
        arguments = ['producer', '--builds-root', str(builds), '--toolchain', str(self.root),
                     '--oem-reference-dir', str(oem), '--private-output', str(private),
                     '--historical-catalog', str(marker), '--source-backups-root', str(backups),
                     '--settings-run', str(record), '--write-policies', '--evidence-output', 'audits/new']
        with patch.object(sys, 'argv', arguments), patch.dict(sys.modules, modules), \
             patch.object(producer, 'digest', return_value='digest'), \
             patch.object(producer.safety, 'safe_path', return_value=marker), \
             patch.object(producer.beta_policy, 'load_previous_catalog', return_value=old), \
             patch.object(producer.beta_policy, 'previous_source_catalog', return_value={}), \
             patch.object(producer.beta_policy, 'validate_catalog_scope'), \
             patch.object(producer.beta_policy, 'source_identities', return_value={'source': 'code'}), \
             patch.object(producer, 'preflight_origin'), patch.object(producer, 'preflight_backup_files'), \
             patch.object(subprocess, 'run') as run, self.assertRaisesRegex(ValueError, 'Unsupported keycode'):
            producer.main()
        run.assert_not_called()
        self.assertFalse((self.root / 'audits/new').exists())
        self.assertFalse(private.exists())
        self.assertEqual(marker.read_bytes(), b'unchanged')

    def test_draft_semantic_failure_preserves_installed_tree(self):
        settings_path = str(HERE.parents[1] / 'tools/installer')
        with patch.object(sys, 'path', [settings_path] + sys.path):
            import settings_backup as settings
        names = list(producer.beta_policy.BETA4_IDENTITIES)
        builds = self.root / 'qmk-8051-ak820/build'
        for name in names:
            for leaf in ('build-report.json', 'ajazz_ak820_vial.ihx', 'ajazz_ak820_vial.map',
                         'runtime-stack.json', 'runtime-safety/summary.json',
                         'runtime-safety/startup.json', 'runtime-safety/irq/results.json'):
                path = builds / name / leaf
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(json.dumps({'build_id': 1}).encode() if leaf == 'build-report.json' else b'input')
        definition = self.root / 'qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/vial.json'
        definition.parent.mkdir(parents=True)
        definition.write_bytes(b'{}')
        oem = self.root / 'oem'
        oem.mkdir()
        for leaf in ('stock-full.bin', 'native-installed.bin'):
            (oem / leaf).write_bytes(b'native')
        backup = self.root / 'backups/saved'
        backup.mkdir(parents=True)
        records = {}
        for name in settings.FILES:
            data = b'*\n' if name == '.gitignore' else b'{}'
            (backup / name).write_bytes(data)
            records[name] = settings._record(data)
        (backup / 'manifest.json').write_text(json.dumps({'format': settings.FORMAT,
                                                         'device': {}, 'files': records}))
        # Exercise the actual structural preflight, then the actual semantic validator.
        producer.preflight_backup_files(backup.parent, settings)
        for leaf in ('audits/old/history', 'tools/installer/settings-catalog.json',
                     'web/firmware-matrix.json', 'ci/profiles/main/release-policy.json'):
            path = self.root / leaf
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(('protected ' + leaf).encode())
        before = {path.relative_to(self.root): path.read_bytes()
                  for path in self.root.rglob('*') if path.is_file()}
        before_dirs = {path.relative_to(self.root) for path in self.root.rglob('*') if path.is_dir()}
        old = {'profiles': [{'profile': name} for name in names]}
        code_hash = hashlib.sha256(b'packed').hexdigest()
        measured = []
        def measure(build, origin, toolchain, native, output):
            measured.append(build.name)
            output.mkdir(parents=True)
            for name in ('binding.json', 'matrix.json', 'measurement.log'):
                (output / name).write_bytes(b'synthetic measurement')
            return {'profile': build.name, 'runtime_status': 'exact-image-pass',
                    'offline_tests_status': 'exact-image-pass', 'identity': {},
                    'settings_identity': {'code_sha256': code_hash}}
        fake_pack = types.SimpleNamespace(
            validate_native=lambda *a: None, BUILD_ID=1, APP_START=0, APP_END=1, CODE_END=6,
            read_ihex=lambda *a: b'code', read_symbols=lambda *a: {},
            migrate=lambda *a: (b'nvm', None), pack=lambda *a, **k: b'packed',
            verify_payload=lambda *a, **k: {}, digest=lambda data: hashlib.sha256(data).hexdigest())
        fake_settings = types.SimpleNamespace(pack=fake_pack, _catalog_images=lambda *a: None,
            _read_file=settings._read_file, _json=settings._json, _record=settings._record,
            FORMAT=settings.FORMAT, FORMAT_V2=settings.FORMAT_V2, FILES=settings.FILES,
            load_profile=lambda *a, **k: {}, validate_backup=settings.validate_backup)
        fake_matrix = types.SimpleNamespace(candidate_names=lambda: tuple(names), matrix=lambda rows: {})
        fake_ci = types.SimpleNamespace(reproducible_identity=lambda *a: {})
        modules = {'settings_backup': fake_settings, 'firmware_matrix': fake_matrix,
                   'build_ci_release': fake_ci, 'measure_origin': types.SimpleNamespace(measured_row=measure)}
        with tempfile.TemporaryDirectory() as private_parent:
            private = Path(private_parent) / 'private'
            arguments = ['producer', '--builds-root', str(builds), '--toolchain', str(self.root),
                         '--oem-reference-dir', str(oem), '--private-output', str(private),
                         '--historical-catalog', str(self.root / 'audits/old/history'),
                         '--source-backups-root', str(backup.parent), '--evidence-output', 'audits/new']
            with patch.object(sys, 'argv', arguments), patch.dict(sys.modules, modules), \
                 patch.object(producer.beta_policy, 'load_previous_catalog', return_value=old), \
                 patch.object(producer.beta_policy, 'previous_source_catalog', return_value={}), \
                 patch.object(producer.beta_policy, 'compose_catalog', return_value={}), \
                 patch.object(producer.beta_policy, 'source_identities', return_value={}), \
                 patch.object(producer, 'preflight_origin'), patch.object(subprocess, 'run') as run, \
                 self.assertRaisesRegex(ValueError, 'Backup device identity differs'):
                producer.main()
            run.assert_not_called()
            self.assertEqual(measured, names)
            self.assertTrue(private.is_dir())
            self.assertTrue((self.root / 'audits/new/origin-measurements').is_dir())
            self.assertFalse((self.root / 'audits/new/policies').exists())
            after = {path.relative_to(self.root): path.read_bytes()
                     for path in self.root.rglob('*') if path.is_file()
                     and not path.is_relative_to(self.root / 'audits/new')}
            self.assertEqual(after, before)
            after_dirs = {path.relative_to(self.root) for path in self.root.rglob('*')
                          if path.is_dir() and not path.is_relative_to(self.root / 'audits/new')}
            self.assertEqual(after_dirs, before_dirs)
            self.assertEqual(list(Path(private_parent).iterdir()), [private])
            self.assertFalse((self.root / 'audits/new/profile-policy-preparation.json').exists())

    def test_capture_snapshot_failure_does_not_reserve_or_run(self):
        capture_spec = importlib.util.spec_from_file_location('capture_settings_tests', HERE / 'capture_settings_tests.py')
        capture = importlib.util.module_from_spec(capture_spec)
        capture_spec.loader.exec_module(capture)
        with patch.object(sys, 'argv', ['capture', '--evidence-output', 'audits/new']), \
             patch.object(capture, 'snapshot', side_effect=ValueError('bad source')), \
             patch.object(subprocess, 'run') as run:
            with self.assertRaises(ValueError):
                capture.main()
        run.assert_not_called()
        self.assertFalse((self.root / 'audits/new').exists())

    def test_exclusive_output_does_not_replace_existing_file(self):
        out = self.root / 'audits/new'
        out.mkdir()
        target = out / 'file.json'
        target.write_bytes(b'original')
        with patch.object(producer, 'OUTPUT', out), self.assertRaises(FileExistsError):
            producer.write(target, {})
        self.assertEqual(target.read_bytes(), b'original')

    def test_origin_mismatch_and_interpreter_fail_without_subprocess(self):
        build = self.root / 'build'
        original = self.root / 'origin/build'
        build.mkdir()
        (original / 'profile-tests').mkdir(parents=True)
        results = original / 'profile-tests/results.json'
        results.write_text(json.dumps({'tests': [{'command': [sys.executable]}]}))
        tools = self.root / 'toolchain'
        tools.mkdir()
        (self.root / 'origin/toolchain').mkdir()
        fake = types.SimpleNamespace(source_files=lambda path: {},
                                     tree=lambda path: {'value': str(path)})
        with patch.dict(sys.modules, {'measure_origin': fake}), patch.object(subprocess, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'Copied build differs'):
                producer.preflight_origin(build, self.root / 'origin', tools)
            fake.tree = lambda path: {'value': 'same'}
            results.write_text(json.dumps({'tests': [{'command': ['/missing/python']}]}))
            with self.assertRaisesRegex(ValueError, 'another Python'):
                producer.preflight_origin(build, self.root / 'origin', tools)
        run.assert_not_called()
        self.assertFalse((self.root / 'audits/new').exists())

    def test_malformed_backup_fails_before_subprocess(self):
        backup = self.root / 'backup' / 'one'
        backup.mkdir(parents=True)
        (backup / 'manifest.json').write_text('{}')
        settings_path = str(HERE.parents[1] / 'tools/installer')
        with patch.object(sys, 'path', [settings_path] + sys.path):
            import settings_backup
            with patch.object(subprocess, 'run') as run, self.assertRaisesRegex(ValueError, 'Unknown backup format'):
                producer.preflight_backup_files(backup.parent, settings_backup)
            run.assert_not_called()
        self.assertFalse((self.root / 'audits/new').exists())

    def test_frozen_semantic_backup_failure_before_any_output(self):
        installed = [self.root / 'tools/installer/settings-catalog.json',
                     self.root / 'web/firmware-matrix.json']
        catalog = {'profiles': [{'profile': 'main', 'settings_identity': {'ihx_sha256': 'a' * 64, 'code_sha256': 'b' * 64}}]}
        for path in installed:
            path.write_text(json.dumps(catalog))
        build = self.root / 'qmk-8051-ak820/build/main'
        build.mkdir(parents=True)
        for name in ('ajazz_ak820_vial.ihx', 'ajazz_ak820_vial.map', 'build-report.json'):
            (build / name).write_bytes(b'input')
        definition = self.root / 'qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/vial.json'
        definition.parent.mkdir(parents=True)
        definition.write_bytes(b'{}')
        backup = self.root / 'backups/one'
        backup.mkdir(parents=True)
        (backup / 'manifest.json').write_text('{}')
        args = types.SimpleNamespace(build_overrides={}, builds_root=build.parent,
                                     source_backups_root=backup.parent, source_rom=[], source_bundle=[])
        settings = types.SimpleNamespace(load_profile=lambda *a, **k: {'ihx_sha256': 'a' * 64, 'code_sha256': 'b' * 64},
            validate_backup=lambda *a: (_ for _ in ()).throw(ValueError('invalid NVM')))
        with patch.object(producer.beta_policy, 'validate_catalog_scope'), \
             patch.object(subprocess, 'run') as run, self.assertRaisesRegex(ValueError, 'invalid NVM'):
            producer.preflight_frozen_backups(args, settings, b'stock', {})
        run.assert_not_called()
        self.assertFalse((self.root / 'audits/new').exists())
        self.assertEqual([json.loads(p.read_text()) for p in installed], [catalog, catalog])

    def test_policy_rejects_unplanned_rom_and_bundle_fixtures(self):
        for leaf in ('tools/installer/settings-catalog.json', 'web/firmware-matrix.json'):
            (self.root / leaf).write_text('{}')
        for roms, bundles in ((['source=file'], []), ([], ['source=dir'])):
            args = types.SimpleNamespace(source_rom=roms, source_bundle=bundles)
            with self.subTest(roms=roms, bundles=bundles), \
                 patch.object(producer.beta_policy, 'validate_catalog_scope'), \
                 self.assertRaisesRegex(ValueError, 'draft-only'):
                producer.preflight_frozen_backups(args, object(), b'', {})
        self.assertFalse((self.root / 'audits/new').exists())

    def test_symlink_collision_does_not_touch_target(self):
        out = self.root / 'audits/new'
        out.mkdir()
        original = self.root / 'audits/old/evidence.json'
        original.write_bytes(b'preserve')
        (out / 'file.json').symlink_to(original)
        with patch.object(producer, 'OUTPUT', out), self.assertRaises(FileExistsError):
            producer.write(out / 'file.json', {})
        self.assertEqual(original.read_bytes(), b'preserve')

    def test_producer_source_remains_canonical(self):
        self.assertEqual(Path(producer.__file__).resolve(), HERE / 'prepare_release.py')
        self.assertIn('audits/beta3-direct-20261026/prepare_release.py', producer.safety.REQUIRED_SOURCES)


if __name__ == '__main__':
    unittest.main()
