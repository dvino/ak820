"""Offline catalog negative controls, with real shared evidence validators."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_capability_catalog as catalog
config = catalog.configured


class CatalogTests(unittest.TestCase):
    def test_ten_current_profile_contracts_use_main_default_and_schema03(self):
        names = ('main', 'game', 'mmo', 'typing', 'code', 'pointer',
                 'onehand', 'creative', 'shortcuts', 'multios')
        self.assertEqual(config.profiles.RELEASE_PROFILES, names)
        self.assertEqual(config.profiles.DEFAULT_PROFILE, 'main')
        for name in names:
            selected = config.profiles.configuration(name)
            self.assertEqual(selected['nvm_schema'], config.profiles.EXTENSION_SCHEMA)
            contract = catalog.module_contract(selected, {'tap_dance': 8, 'key_overrides': 8})
            for feature, module in (('tap-dance', 'tap_dance'), ('key-overrides', 'key_overrides')):
                self.assertEqual(contract['modules'][module]['enabled_entries'],
                                 8 if feature in selected['optional_features'] else 0)
            self.assertEqual(contract['modules']['qmk_settings']['enabled_qsids'],
                             [1,2,4,7,18,19] if name in ('main', 'typing') else [1,2,7,18,19])
            self.assertFalse(contract['restore']['write_authorization_granted'])
            self.assertFalse(contract['physical_behavior_verified'])

    def test_individual_module_contracts_are_capability_aware(self):
        limits={'tap_dance':8,'key_overrides':8}
        for name,td,ko,qsids in (('creative',8,0,[1,2,7,18,19]),
                ('main',0,8,[1,2,4,7,18,19]), ('onehand',8,0,[1,2,7,18,19])):
            with self.subTest(name=name):
                contract=catalog.module_contract(config.profiles.configuration(name),limits)
                modules=contract['modules']
                self.assertEqual(modules['tap_dance']['enabled_entries'],td)
                self.assertEqual(modules['key_overrides']['enabled_entries'],ko)
                self.assertEqual(modules['qmk_settings']['enabled_qsids'],qsids)
                self.assertEqual(modules['tap_dance']['stored_entries'],8)
                self.assertEqual(modules['key_overrides']['stored_entries'],8)
                fields={f['qsid']:f for f in modules['qmk_settings']['fields']}
                self.assertEqual(fields[4]['enabled'], name == 'main')
                self.assertEqual(fields[4]['consumers'], ['compact-auto-shift'] if name == 'main' else [])
                self.assertEqual(fields[7]['maximum'],1000)
                self.assertFalse(contract['limits']['qmk_settings']['tap_dance_term_uses_qsid7'])
                self.assertFalse(contract['restore']['write_authorization_granted'])
                self.assertFalse(contract['physical_behavior_verified'])
                for module in ('tap_dance','key_overrides'):
                    for offset in modules[module]['entry_offsets']:
                        self.assertEqual(offset//64,(offset+9)//64)

    def test_explicit_legacy_schema02_has_no_extension_storage_or_enabled_settings(self):
        contract=catalog.module_contract(config.profiles.configuration('full'),{'tap_dance':8,'key_overrides':8})
        self.assertEqual(contract['modules']['tap_dance']['stored_entries'],0)
        self.assertEqual(contract['modules']['qmk_settings']['fields'],[])
        self.assertFalse(contract['migration']['schema03_downgrade_supported'])
        forged=config.profiles.configuration('full-tap-dance')
        forged['runtime_qmk_settings']=[1,2,7,18,19]
        with self.assertRaises(ValueError):catalog.module_contract(forged,{'tap_dance':8,'key_overrides':8})
        with self.assertRaises(ValueError):catalog.module_contract(config.profiles.configuration('full-tap-dance'),{'tap_dance':7,'key_overrides':8})

    def test_fingerprint_binds_bytes_addresses_and_holes(self):
        image = {0x28a0: 2, 0x3027: 0x22}
        identity = catalog.code_identity(image)
        self.assertEqual(identity, catalog.code_identity(dict(reversed(list(image.items())))))
        for changed in ({0x28a1: 2, 0x3027: 0x22}, {0x28a0: 3, 0x3027: 0x22},
                        {0x28a0: 2, 0x3028: 1, 0x3027: 0x22}):
            self.assertNotEqual(identity['sha256'], catalog.code_identity(changed)['sha256'])
        for invalid in ({}, {-1: 1}, {1: 256}):
            with self.assertRaises(ValueError):
                catalog.code_identity(invalid)

    def test_fingerprint_zero_fills_absent_code_bytes(self):
        image = {0x28a0: 2, 0x3027: 0x22}
        with_explicit_zero = {**image, 0x28a1: 0}
        with_nonzero_hole = {**image, 0x28a1: 1}

        fingerprint = catalog.code_identity(image)['sha256']
        self.assertEqual(fingerprint, catalog.code_identity(with_explicit_zero)['sha256'])
        self.assertNotEqual(fingerprint, catalog.code_identity(with_nonzero_hole)['sha256'])

    def test_deterministic_order_and_duplicate_identity(self):
        entries = [{'code_identity': {'sha256': name}} for name in ('b', 'a')]
        with patch.object(config, 'validate_tools', return_value=Path('/tools')), \
             patch.object(catalog, 'inspect_entry', side_effect=entries):
            first = catalog.catalog(['one', 'two'], '/tools')
        with patch.object(config, 'validate_tools', return_value=Path('/tools')), \
             patch.object(catalog, 'inspect_entry', side_effect=list(reversed(entries))):
            second = catalog.catalog(['two', 'one'], '/tools')
        self.assertEqual(config.canonical(first), config.canonical(second))
        self.assertFalse(first['flashing_authorized'])
        with patch.object(config, 'validate_tools', return_value=Path('/tools')), \
             patch.object(catalog, 'inspect_entry', return_value=entries[0]), \
             self.assertRaisesRegex(ValueError, 'Duplicate CODE'):
            catalog.catalog(['one', 'alias'], '/tools')

    def test_artifact_tampering_and_profile_claim_fail_shared_verifiers(self):
        with tempfile.TemporaryDirectory() as temporary:
            build = Path(temporary)
            image = build / 'ajazz_ak820_vial.ihx'
            image.write_bytes(b'exact image')
            report = {'artifacts': [{'path': 'build/' + image.name,
                       'sha256': config.sha(image), 'size': image.stat().st_size}]}
            config.artifact(report, build, 'ihx')
            image.write_bytes(b'other image')
            with self.assertRaisesRegex(ValueError, 'Artifact changed'):
                config.artifact(report, build, 'ihx')
        selected = copy.deepcopy(config.profiles.configuration('main'))
        selected['optional_features'] = ['os-indicators']
        with self.assertRaises(ValueError):
            config.profiles.validate_configuration(selected)

    def test_missing_base_and_supplemental_suites_fail_real_validators(self):
        with tempfile.TemporaryDirectory() as temporary:
            build = Path(temporary)
            path = build / 'qualification.json'
            path.write_text(json.dumps({'format': 'ak820-offline-tests-1', 'passed': True}))
            with self.assertRaises(ValueError):
                config.validate_tests(path, {'ihx_sha256': 'x', 'map_sha256': 'y'})
            report = {'format': 'ak820-profile-tests-1', 'profile': 'main',
                      'identity': {}, 'passed': True, 'hardware_validated': False,
                      'physical_device_commands': 0, 'tests': []}
            with self.assertRaisesRegex(ValueError, 'omitted or duplicated'):
                config.validate_profile_tests(report, 'main', {}, build, Path('/tools'))

    def test_runtime_evidence_cannot_be_replaced_by_summary_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            build = Path(temporary)
            (build / 'runtime-safety').mkdir()
            (build / 'runtime-safety/summary.json').write_text('{"passed":true}')
            with self.assertRaises(FileNotFoundError):
                catalog.runtime_proof(build, {'identity': {}, 'resources': {'internal_ram': {}}}, Path('/tools'))


class EntryEvidenceTests(unittest.TestCase):
    """Exercise the entry pipeline with real report/log validators, no compiler."""
    def setUp(self):
        import test_runtime_safety
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.build = Path(self.temp.name).resolve()
        self.toolchain = self.build / 'toolchain'
        (self.toolchain / 'bin').mkdir(parents=True)
        (self.toolchain / 'bin/s51').write_text('simulator fixture')
        for suffix in ('ihx', 'map', 'mem'):
            (self.build / ('ajazz_ak820_vial.' + suffix)).write_text(suffix)
        self.source = self.build / 'source.c'; self.source.write_text('compiled fixture')
        self.source_sha = config.sha(self.source)
        self.identity = {key + '_sha256': config.sha(self.build / ('ajazz_ak820_vial.' + key))
                         for key in ('ihx', 'map', 'mem')}
        self.identity['profile'] = 'main'
        self.inspected = {'format': config.FORMAT, 'configuration': config.profiles.configuration('main'),
            'identity': self.identity, 'short_calls': None,
            'resources': {'internal_ram': {'stack_capacity': 166, 'initial_sp': 89}},
            'hardware_validated': False, 'physical_device_commands': 0, 'release_approved': False,
            'release_blockers': list(config.RELEASE_BLOCKERS),
            'settings_compatibility': 'fixture', 'offline_tests_passed': False}
        limits = config.QMK / 'keyboards/ajazz/ak820/config.h'
        self.write('build-report.json', {'sources': [{'origin': 'source',
            'path': 'keyboards/ajazz/ak820/config.h', 'sha256': config.sha(limits)}]})
        fixture = test_runtime_safety.RuntimeSafetyTests(); fixture.setUp()
        self.sources = fixture.sources
        for evidence in (fixture.runtime, fixture.startup):
            evidence['identity'] = self.identity
        fixture.irq.update(linked_image_sha256=self.identity['ihx_sha256'],
                           linked_map_sha256=self.identity['map_sha256'])
        paths = {'foreground': 'runtime-stack.json', 'startup': 'runtime-safety/startup.json',
                 'irq': 'runtime-safety/irq/results.json'}
        for name, evidence in zip(paths.values(), (fixture.runtime, fixture.startup, fixture.irq)):
            self.write(name, evidence)
        for name in ('startup', 'irq'):
            (self.build / 'runtime-safety' / (name + '.log')).write_text('CPU fixture passed')
        proof = config.combine_runtime_safety(fixture.runtime, fixture.startup, fixture.irq,
            self.identity, self.inspected['resources']['internal_ram'], self.sources)
        proof['reports'] = {key: {'path': path, 'sha256': config.sha(self.build / path)}
                            for key, path in paths.items()}
        proof['logs'] = {name: config.sha(self.build / 'runtime-safety' / (name + '.log'))
                         for name in ('startup', 'irq')}
        proof['simulator_sha256'] = config.sha(self.toolchain / 'bin/s51')
        self.write('runtime-safety/summary.json', proof)
        self.write_base()
        self.source_patch = patch.object(config, 'runtime_source_snapshot', return_value=self.sources)
        self.source_patch.start(); self.addCleanup(self.source_patch.stop)
        self.inspect_patch = patch.object(config, 'inspect', side_effect=self.fake_inspect)
        self.inspect_patch.start(); self.addCleanup(self.inspect_patch.stop)
        self.code_patch = patch.object(config, 'diagnostic_build', return_value={0x28a0: 2, 0x3027: 0x22})
        self.code_patch.start(); self.addCleanup(self.code_patch.stop)
        profile = {'format': 'ak820-profile-tests-1', 'profile': 'main', 'identity': self.identity,
            'passed': True, 'hardware_validated': False, 'physical_device_commands': 0,
            'source_files': config.test_source_snapshot(), 'tests': []}
        for identifier, cwd, command in config.profile_test_plan('main', self.build, self.toolchain):
            log = self.build / 'profile-tests' / (identifier + '.log'); log.parent.mkdir(exist_ok=True)
            log.write_text('Ran 1 test in 0.001s\n\nOK\n')
            profile['tests'].append({'id': identifier, 'cwd': str(cwd), 'command': command,
                'exit_code': 0, 'build_before': self.identity, 'build_after': self.identity,
                'log_sha256': config.sha(log)})
        self.write('profile-tests/results.json', profile)
        stored = self.fake_inspect(self.build, self.toolchain)
        config.apply_runtime_safety(stored, proof)
        stored.update(offline_tests_passed=True,
            qualification=config.validate_tests(self.build / 'qualification.json', self.identity),
            profile_tests={'sha256': config.sha(self.build / 'profile-tests/results.json'),
                           'suites': [row['id'] for row in profile['tests']]})
        self.write('configuration-report.json', stored)

    def write(self, name, value):
        path = self.build / name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(config.canonical(value))

    def fake_inspect(self, build, toolchain):
        # Stand-in for the expensive compiler inventory, retaining real profile validation.
        config.require(config.sha(self.source) == self.source_sha, 'Source differs from linked build')
        config.profiles.validate_configuration(self.inspected['configuration'])
        return copy.deepcopy(self.inspected)

    def write_base(self):
        py = sys.executable
        commands = [[py, '-B', '-m', 'unittest', 'discover', '-s', directory, '-p', pattern]
            for directory, pattern in (('tools/installer', 'test_*.py'),
                ('tools', 'test_build_release_bundle.py'), ('tools', 'test_build_windows_installer.py'),
                ('tools', 'test_keyboard_runner.py'), ('tools', 'test_ak820_device_tests.py'),
                ('tools', 'test_ak820_device_protocol.py'),
                ('qmk-8051-ak820/tests/ak820_package', 'test_*.py'),
                ('qmk-8051-ak820/tests/ak820_inventory', 'test_*.py'))]
        commands.append([py, 'tools/check_docs.py'])
        commands.extend([[py, 'tests/' + name + '/run.py'] for name in (
            'ak820_usb', 'ak820_keymap', 'ak820_caps_word', 'ak820_macro_guard',
            'ak820_diagnostic', 'ak820_optimization', 'ak820_rgb', 'ak820_via_decode',
            'ak820_bounded', 'ak820_combo')])
        commands.append([py, 'tests/ak820_tapping/run.py', '--negative-controls', '--output', '/tmp/tapping.json'])
        for script in [*(f'tests/{name}/run.py' for name in ('ak820_features', 'ak820_unlock', 'ak820_tri_layer', 'ak820_iap')),
                       *(f'tests/{name}/emitted.py' for name in ('ak820_rgb', 'ak820_bounded', 'ak820_tapping', 'ak820_combo'))]:
            command = [py, script, '--build-dir', str(self.build), '--s51', str(self.toolchain / 'bin/s51'),
                       '--output-dir', str(self.build / 'cpu')]
            if 'ak820_iap/' in script:
                command.extend(['--iap-fault-profile', 'guarded-erase'])
            commands.append(command)
        hashes = {key: self.identity[key + '_sha256'] for key in ('ihx', 'map')}
        rows = []
        for index, command in enumerate(commands):
            log = self.build / 'qualification-logs-fixture' / f'{index:02d}.txt'
            log.parent.mkdir(exist_ok=True); log.write_text('Ran 1 test in 0.001s\n\nOK\n')
            rows.append({'command': command, 'cwd': str(config.ROOT if index < 9 else config.QMK),
                'exit_code': 0, 'log': str(log), 'log_sha256': config.sha(log),
                'unit_tests': {'run': 1, 'skipped': 0}, 'build_before': hashes, 'build_after': hashes})
        self.write('qualification.json', {'format': 'ak820-offline-tests-1', 'passed': True,
            'require_toolchain': True, 'build_unchanged': True, 'build_hashes': hashes,
            'hardware_validated': False, 'physical_device_commands': 0, 'iap_fault_profile': 'guarded-erase',
            'tools': {'s51': {'path': str(self.toolchain / 'bin/s51')}},
            'unit_tests': {'run': len(rows), 'skipped': 0}, 'tests': rows})

    def test_entry_is_deterministic_and_development_only(self):
        first = catalog.inspect_entry(self.build, self.toolchain)
        self.assertEqual(config.canonical(first), config.canonical(catalog.inspect_entry(self.build, self.toolchain)))
        self.assertFalse(first['release_approved']); self.assertFalse(first['flashing_authorized'])
        self.assertEqual(first['fixed_limits']['layers'], 6)

    def test_stale_configuration_and_runtime_evidence_are_rejected(self):
        path = self.build / 'configuration-report.json'; original = path.read_bytes()
        report = config.load_json(path); report['identity']['ihx_sha256'] = 'stale'; self.write(path.name, report)
        with self.assertRaisesRegex(ValueError, 'Configuration report differs'):
            catalog.inspect_entry(self.build, self.toolchain)
        path.write_bytes(original)
        evidence = config.load_json(self.build / 'runtime-stack.json')
        evidence['identity']['ihx_sha256'] = 'stale'; self.write('runtime-stack.json', evidence)
        with self.assertRaisesRegex(ValueError, 'another image'):
            catalog.inspect_entry(self.build, self.toolchain)

    def test_retained_base_log_tamper_and_count_forgery_are_rejected(self):
        log = self.build / 'qualification-logs-fixture/00.txt'; log.write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'Base suite log changed'):
            catalog.inspect_entry(self.build, self.toolchain)
        report = config.load_json(self.build / 'qualification.json')
        report['tests'][0]['log_sha256'] = config.sha(log); self.write('qualification.json', report)
        with self.assertRaisesRegex(ValueError, 'counts differ'):
            catalog.inspect_entry(self.build, self.toolchain)

    def test_source_and_profile_mismatch_are_rejected(self):
        self.source.write_text('changed source')
        with self.assertRaisesRegex(ValueError, 'Source differs'):
            catalog.inspect_entry(self.build, self.toolchain)
        self.source.write_text('compiled fixture')
        self.inspected['configuration']['optional_features'] = ['os-indicators']
        with self.assertRaisesRegex(ValueError, 'configuration differs'):
            catalog.inspect_entry(self.build, self.toolchain)


if __name__ == '__main__':
    unittest.main()
