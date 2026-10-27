"""Offline synthetic witness contract tests; these do not qualify firmware."""
import copy
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'qmk-8051-ak820/util'))
import ak820_release_safety as gate
from ak820_profiles import configuration


class ReleaseSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.configuration = configuration('main')
        self.proof = {'format': 'ak820-release-safety-1', 'source_files': {}, 'witnesses': {}}
        for name in gate.REQUIRED_SOURCES:
            self.proof['source_files'][name] = self.write(name, ('synthetic ' + name).encode())
        self.report = {'configuration': self.configuration, 'artifacts': []}
        for ext, data in [('ihx', b'synthetic image'), ('map', b'C: 00001234 _main\n'), ('mem', b'Stack starts at: 0x5e (sp set to 0x5d) with 162 bytes available')]:
            name = 'build/ajazz_ak820_vial.' + ext
            self.report['artifacts'].append(dict(path=name, **self.write('qmk-8051-ak820/' + name, data)))
        ihx = self.report['artifacts'][0]['sha256']
        analyzer = self.proof['source_files']['qmk-8051-ak820/tests/ak820_stack/analyze.py']['sha256']
        sources = self.proof['source_files']
        self.proof['program'] = {'ihx_sha256': ihx, 'symbols_sha256': gate.sha(b'{"_main":4660}'), 'configuration': self.configuration}
        self.data = {
            'stack': {'identity': {'ihx_sha256': ihx}, 'analyzer_sha256': analyzer,
                      'decoder_source_sha256': sources['qmk-8051-ak820/util/ak820_linked_inventory.py']['sha256'],
                      'roots': {name: {'bound': 10, 'unresolved': []} for name in gate.ROOT_NAMES}},
            'startup': {'identity': {'ihx_sha256': ihx}, 'analyzer_sha256': analyzer,
                        'checker_sha256': sources['qmk-8051-ak820/tests/ak820_startup/stack_contract.py']['sha256'],
                        'interrupt_enables_unchanged_until_main': True, 'crt_initial_sp': 93, 'main_entry_frame_bound': 2, 'pre_main_control_stack_bound': 4},
            'irq': {'pass': True, 'linked_image_sha256': ihx, 'stack_analyzer_sha256': analyzer,
                    'runner_sha256': sources['qmk-8051-ak820/tests/ak820_irq/run.py']['sha256'],
                    'wrapper_bytes_on_stack': 17, 'irq_bounds': dict.fromkeys(['timer', 'usb', 'led'], 27),
                    'all_distinct_source_irq_bound': 81, 'stack_capacity': 162, 'initial_sp': 93,
                    'cpu_cases': [{'irq_order': order, 'canary_and_registers_preserved': True}
                                  for n in range(1, 4) for order in itertools.permutations(['timer', 'usb', 'led'], n)],
                    'selector_cases': {'input_values_checked': 256, 'bounded_table_entries': 16},
                    'emitted_contracts': {'compiler_register_bank': 0, 'shared_helper_masked_init_calls': [1], 'nonoverlay_allocations': [1]}},
            'transition': {}}
        self.previous = {'profiles': [
            {'profile': name, 'settings_identity': {'ihx_sha256': hashes[0], 'code_sha256': hashes[1]}}
            for name, hashes in gate.beta_policy.PREVIOUS_IDENTITIES.items()]}
        raw = json.dumps(self.previous).encode()
        pin = patch.object(gate.beta_policy, 'PREVIOUS_CATALOG_SHA256', gate.sha(raw))
        pin.start()
        self.addCleanup(pin.stop)
        self.audit = self.root / 'audit'
        self.write('audit/previous-beta-catalog.json', raw)
        rows = []
        for name in gate.beta_policy.PREVIOUS_IDENTITIES:
            config = self.configuration if name == 'main' else configuration(name)
            image = ihx if name == 'main' else gate.sha(('new ' + name).encode())
            rows.append({'profile': name, 'configuration': config,
                         'settings_identity': {'ihx_sha256': image,
                           'code_sha256': gate.sha(('code ' + name).encode()),
                           'nvm_schema': config['nvm_schema']}})
        self.catalog = gate.beta_policy.compose_catalog({'profiles': rows}, self.previous)
        self.matrix = {'format': 'ak820-settings-transition-matrix-2', 'offline_only': True,
                       'physical_device_commands': 0, 'hardware_validated': False,
                       'sources_per_target': len(gate.beta_policy.source_identities(self.catalog)), 'cases': []}
        for source, code in gate.beta_policy.source_identities(self.catalog).items():
            for row in rows:
                self.matrix['cases'].append({'source': source, 'source_code_sha256': code,
                    'target': row['settings_identity']['ihx_sha256'],
                    'target_code_sha256': row['settings_identity']['code_sha256'],
                    'source_case': source, 'target_profile': row['profile'], 'passed': True,
                    'offline_only': True, 'physical_device_commands': 0,
                    'key_count': 498, 'encoder_count': 12, 'combo_count': 8,
                    'source_scope': 'Synthetic policy unit model; no device capture',
                    'backup_manifest_sha256': gate.sha(source.encode())})
        self.write('audit/settings-catalog-draft.json', json.dumps(self.catalog).encode())
        self.write('audit/transition-preflight.json', json.dumps(self.matrix).encode())
        log = self.write('evidence/transition.log', b'synthetic successful log')
        tests = [{'exit_code': 0, 'command': ['python', '-m', 'unittest'], 'source_files': {name: rec['sha256'] for name, rec in sources.items()},
                  'log_path': 'evidence/transition.log', 'log_sha256': log['sha256']}]
        path = ROOT / 'audits/beta3-direct-20261026/prepare_release.py'
        spec = importlib.util.spec_from_file_location('beta_prepare_for_tests', path)
        producer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(producer)
        self.producer = producer
        self.data['transition'] = producer.produce_transition_evidence(
            self.root, self.audit, 'main', {'configuration': self.configuration,
                'build_id': self.configuration['nvm_schema']},
            {'build': {'ihx_sha256': ihx}, 'settings_code_sha256': rows[0]['settings_identity']['code_sha256']}, tests)
        for key in ('previous_beta_catalog', 'settings_catalog', 'preflight_matrix'):
            ref = self.data['transition'][key]
            sources[ref['path']] = {k: ref[k] for k in ('size', 'sha256')}

    def refresh_document(self, key, value):
        ref = self.data['transition'][key]
        rec = self.write(ref['path'], json.dumps(value).encode())
        ref.update(rec)
        self.proof['source_files'][ref['path']] = rec

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return {'size': len(data), 'sha256': gate.sha(data)}

    def validate(self):
        for key, value in self.data.items():
            name = 'witnesses/' + key + '.json'
            self.proof['witnesses'][key] = dict(path=name, **self.write(name, json.dumps(value).encode()))
        self.write(gate.manifest_name(self.configuration), json.dumps(self.proof).encode())
        return gate.validate(self.report, self.root)

    def test_positive_exact_synthetic_identity(self):
        result = self.validate()
        self.assertEqual(result['stack_bound'], 93)
        self.assertEqual(result['stack_margin'], 69)

    def test_current_profiles_require_their_own_witness(self):
        from ak820_profiles import RELEASE_PROFILES
        for name in RELEASE_PROFILES:
            with self.subTest(profile=name):
                self.assertEqual(gate.manifest_name(configuration(name)),
                                 'ci/profiles/' + name + '/release-safety.json')
                report = dict(self.report, configuration=configuration(name))
                with self.assertRaises(ValueError):
                    gate.validate(report, self.root)

    def test_reject_profile_outside_previous_current_catalog(self):
        self.configuration.clear()
        self.configuration.update(configuration('work'))
        with self.assertRaises(ValueError):
            self.validate()

    def test_reject_unreviewed_profile(self):
        self.report['configuration'] = configuration('work')
        with self.assertRaisesRegex(ValueError, 'missing witness/source'):
            self.validate()

    def test_reject_noncanonical_reviewed_configuration(self):
        self.configuration['optional_features'] = []
        with self.assertRaisesRegex(ValueError, 'selected profile'):
            self.validate()

    def test_reject_transition_for_other_feature_set(self):
        self.data['transition']['target']['optional_features'] = configuration('work')['optional_features']
        with self.assertRaisesRegex(ValueError, 'transition not qualified'):
            self.validate()

    def test_reject_unresolved_root(self):
        self.data['stack']['roots']['_main']['unresolved'] = ['indirect call']
        with self.assertRaises(ValueError): self.validate()

    def test_reject_missing_root(self):
        del self.data['stack']['roots']['_ak820_led_irq']
        with self.assertRaises(ValueError): self.validate()

    def test_reject_other_image(self):
        self.data['startup']['identity']['ihx_sha256'] = '0' * 64
        with self.assertRaises(ValueError): self.validate()

    def test_reject_overflow(self):
        self.data['stack']['roots']['_main']['bound'] = 100
        with self.assertRaises(ValueError): self.validate()

    def test_reject_boolean_bound(self):
        self.data['stack']['roots']['_main']['bound'] = True
        with self.assertRaises(ValueError): self.validate()

    def test_reject_incomplete_irq_order_coverage(self):
        self.data['irq']['cpu_cases'][-1] = self.data['irq']['cpu_cases'][0]
        with self.assertRaises(ValueError): self.validate()

    def test_reject_changed_source_pin(self):
        self.proof['source_files'][next(iter(gate.REQUIRED_SOURCES))]['sha256'] = '0' * 64
        with self.assertRaises(ValueError): self.validate()

    def test_reject_traversal_and_symlink(self):
        for name in ('../outside', '/absolute', 'foo//bar', 'foo/./bar', 'foo/../bar', 'foo\\bar'):
            with self.subTest(name=name), self.assertRaises(ValueError): gate.safe_path(self.root, name)
        (self.root / 'link').symlink_to(self.root / 'build')
        with self.assertRaises(ValueError): gate.safe_path(self.root, 'link/file')

    def test_reject_changed_artifact(self):
        self.write('qmk-8051-ak820/build/ajazz_ak820_vial.ihx', b'other image')
        with self.assertRaises(ValueError): self.validate()

    def test_reject_forged_capacity(self):
        self.data['irq']['stack_capacity'] = 256
        with self.assertRaisesRegex(ValueError, 'placement'): self.validate()

    def test_reject_changed_startup_sp(self):
        self.data['startup']['crt_initial_sp'] = 92
        with self.assertRaisesRegex(ValueError, 'placement'): self.validate()

    def test_reject_changed_nested_log(self):
        self.write('evidence/transition.log', b'changed')
        with self.assertRaisesRegex(ValueError, 'log changed'): self.validate()

    def test_reject_changed_nested_source_pin(self):
        self.data['transition']['tests'][0]['source_files']['tools/ak820_device_protocol.py'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'source changed'): self.validate()

    def test_reject_missing_transition_source(self):
        del self.data['transition']['tests'][0]['source_files']['tools/ak820_device_protocol.py']
        with self.assertRaisesRegex(ValueError, 'source closure'): self.validate()

    def test_actual_producer_generates_complete_previous_current_witness(self):
        transition = self.data['transition']
        self.assertEqual(transition['format'], 'ak820-settings-transition-2')
        self.assertEqual(len(transition['source_images']), 20)
        self.assertEqual(len(self.matrix['cases']), 200)
        self.assertNotIn('actual_alpha2_preflight', transition)
        self.assertEqual(self.validate()['stack_bound'], 93)

    def test_actual_producer_rejects_incomplete_matrix_and_wrong_build(self):
        report = {'configuration': self.configuration, 'build_id': self.configuration['nvm_schema']}
        target = self.catalog['profiles'][0]['settings_identity']
        packed = {'build': {'ihx_sha256': target['ihx_sha256']},
                  'settings_code_sha256': target['code_sha256']}
        tests = self.data['transition']['tests']
        incomplete = copy.deepcopy(self.matrix)
        incomplete['cases'].pop()
        self.refresh_document('preflight_matrix', incomplete)
        with self.assertRaisesRegex(ValueError, 'Incomplete beta transition matrix'):
            self.producer.produce_transition_evidence(self.root, self.audit, 'main', report, packed, tests)
        self.refresh_document('preflight_matrix', self.matrix)
        packed['settings_code_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'producer target differs'):
            self.producer.produce_transition_evidence(self.root, self.audit, 'main', report, packed, tests)

    def test_old_alpha_witness_format_never_falls_back(self):
        self.data['transition']['format'] = 'ak820-settings-transition-1'
        self.data['transition']['actual_alpha2_preflight'] = {'passed': True}
        with self.assertRaisesRegex(ValueError, 'transition not qualified'):
            self.validate()

    def test_reject_changed_matrix_payload(self):
        self.write('audit/transition-preflight.json', b'changed')
        with self.assertRaisesRegex(ValueError, 'changed witness/source'):
            self.validate()

    def test_reject_semantically_invalid_matrix_even_with_rebound_hash(self):
        for mutation in (
            lambda m: m['cases'].pop(),
            lambda m: m['cases'].__setitem__(1, copy.deepcopy(m['cases'][0])),
            lambda m: m['cases'][0].update(source='f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e'),
            lambda m: m['cases'][0].update(source_code_sha256='0' * 64),
            lambda m: m['cases'][0].update(target='0' * 64),
            lambda m: m['cases'][0].update(passed=False),
            lambda m: m['cases'][0].update(physical_device_commands=False),
            lambda m: m['cases'][0].update(key_count=497),
            lambda m: m['cases'][0].update(combo_count=0),
            lambda m: m['cases'][0].update(backup_manifest_sha256='0' * 64),
            lambda m: m.update(sources_per_target=19)):
            with self.subTest(mutation=mutation):
                altered = copy.deepcopy(self.matrix)
                mutation(altered)
                self.refresh_document('preflight_matrix', altered)
                with self.assertRaises(ValueError):
                    self.validate()
        self.refresh_document('preflight_matrix', self.matrix)

    def test_reject_previous_catalog_change_with_rebound_hash(self):
        changed = copy.deepcopy(self.previous)
        changed['profiles'][0]['settings_identity']['code_sha256'] = '0' * 64
        self.refresh_document('previous_beta_catalog', changed)
        with self.assertRaisesRegex(ValueError, 'authenticated published'):
            self.validate()

    def test_reject_ancestry_or_rollback_policy_with_rebound_hash(self):
        for field, value in [('historical_sources', [{'ihx_sha256': 'old'}]),
                             ('historical_profiles', []),
                             ('settings_transitions', [])]:
            changed = copy.deepcopy(self.catalog)
            changed[field] = value
            self.refresh_document('settings_catalog', changed)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'catalog scope'):
                self.validate()
        self.refresh_document('settings_catalog', self.catalog)

    def test_reject_wrong_target_code_or_incomplete_source_scope(self):
        self.data['transition']['target']['code_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'target differs'):
            self.validate()
        self.data['transition']['target']['code_sha256'] = self.catalog['profiles'][0]['settings_identity']['code_sha256']
        self.data['transition']['source_images'].pop()
        with self.assertRaisesRegex(ValueError, 'source scope'):
            self.validate()

    def test_reject_boolean_usb_count_or_test_exit_and_missing_command(self):
        original = copy.deepcopy(self.data['transition'])
        for mutate in (lambda t: t.update(physical_device_commands=False),
                       lambda t: t['tests'][0].update(exit_code=False),
                       lambda t: t['tests'][0].pop('command')):
            self.data['transition'] = copy.deepcopy(original)
            mutate(self.data['transition'])
            with self.assertRaisesRegex(ValueError, 'transition not qualified'):
                self.validate()

    def test_reject_nested_document_absent_from_review_snapshot(self):
        del self.proof['source_files']['audit/settings-catalog-draft.json']
        with self.assertRaisesRegex(ValueError, 'absent from reviewed'):
            self.validate()

    def test_inspected_identity_binding(self):
        sys.path.insert(0, str(ROOT / 'tools'))
        import configure_firmware
        proof = self.validate()
        inspected = {'identity': {ext + '_sha256': value for ext, value in proof['build_identity'].items()},
                     'configuration': copy.deepcopy(self.configuration),
                     'resources': {'internal_ram': {'stack_capacity': 162}}}
        with patch.object(gate, 'validate', return_value=proof):
            with self.assertRaisesRegex(ValueError, 'regression directory'):
                configure_firmware.require_release_approval(copy.deepcopy(inspected), self.report)
            with patch.object(configure_firmware, 'load_json', return_value={
                    'identity': inspected['identity'], 'offline_tests_passed': True}), \
                    patch.object(configure_firmware, 'validate_tests', return_value={'suites': 28}), \
                    patch.object(configure_firmware, 'validate_profile_tests'):
                configure_firmware.require_release_approval(copy.deepcopy(inspected), self.report, self.root, self.root)
            for ext in ('ihx', 'map', 'mem'):
                wrong = copy.deepcopy(inspected)
                wrong['identity'][ext + '_sha256'] = '0' * 64
                with self.subTest(extension=ext), self.assertRaisesRegex(ValueError, 'inspected image'):
                    configure_firmware.require_release_approval(wrong, self.report)

    def test_ci_policy_requires_safety_manifest_sources_and_witnesses(self):
        sys.path.insert(0, str(ROOT / 'tools'))
        import build_ci_release as ci
        self.validate()
        lock_name = 'qmk-8051-ak820/dependencies/lufa.json'
        lock = {'format': 'ak820-external-dependency-1', 'name': 'lufa', 'destination': 'lib/lufa',
                'revision': '549b97320d515bfca2f95c145a67bd13be968faa', 'required_files': {}}
        names = {lock_name, '.github/workflows/windows-installer.yml', 'tools/ci_checks.py',
                 'tools/test_keyboard.py', 'tools/build_ci_release.py', 'tools/build_ci_profiles.py',
                 gate.manifest_name(self.configuration)}
        names.update(self.proof['source_files'])
        names.update(record['path'] for record in self.proof['witnesses'].values())
        self.write(lock_name, json.dumps(lock).encode())
        declared = {}
        for name in names:
            path = self.root / name
            if not path.exists(): self.write(name, b'synthetic policy source')
            declared[name] = {'size': path.stat().st_size, 'sha256': gate.sha(path.read_bytes())}
        with patch.object(ci, 'ROOT', self.root), patch.object(ci, 'host_manifest', return_value={}), \
                patch.object(ci, '_git_blob', side_effect=lambda path: path.read_bytes()):
            ci._validate_policy_sources({'source_files': declared}, self.report)
            for missing in (gate.manifest_name(self.configuration), 'witnesses/irq.json',
                            'tools/ak820_device_protocol.py', 'tools/build_ci_profiles.py'):
                incomplete = {name: record for name, record in declared.items() if name != missing}
                with self.subTest(missing=missing), self.assertRaisesRegex(ValueError, 'omits required'):
                    ci._validate_policy_sources({'source_files': incomplete}, self.report)

    def test_release_profile_selects_its_own_safety_manifest_without_fallback(self):
        self.assertEqual(gate.manifest_name(configuration('main')),
                         'ci/profiles/main/release-safety.json')
        with self.assertRaisesRegex(ValueError, 'Build configuration differs'):
            gate.manifest_name({'profile': 'main'})

    def test_local_review_requires_safety_manifest_hash(self):
        sys.path.insert(0, str(ROOT / 'tools'))
        import build_release_bundle as bundle
        self.validate()
        ihx = self.root / 'qmk-8051-ak820/build/ajazz_ak820_vial.ihx'
        mapfile = ihx.with_suffix('.map')
        report = self.root / 'report.json'
        report.write_text(json.dumps(self.report))
        review = self.root / 'review.md'
        review.write_text('synthetic review')
        record = {'build': {'ihx_sha256': bundle.sha(ihx), 'map_sha256': bundle.sha(mapfile),
                            'build_report_sha256': bundle.sha(report)}, 'host_files': {}}
        with patch.object(bundle, 'ROOT', self.root), patch.object(bundle, 'host_manifest', return_value={}), \
                patch.object(bundle, 'read_review_record', return_value=record):
            with self.assertRaisesRegex(ValueError, 'release safety evidence'):
                bundle.validate_review(review, ihx, mapfile, report)
            record['release_safety_manifest_sha256'] = bundle.sha(self.root / gate.manifest_name(self.configuration))
            bundle.validate_review(review, ihx, mapfile, report)
            self.write(gate.manifest_name(self.configuration), b'changed manifest')
            with self.assertRaisesRegex(ValueError, 'release safety evidence'):
                bundle.validate_review(review, ihx, mapfile, report)

    def test_generated_unchanged_source_keeps_complete_exact_coverage(self):
        previous = copy.deepcopy(self.previous)
        rows = copy.deepcopy(self.catalog['profiles'])
        # One current image is byte-for-byte the published previous image.
        rows[1] = copy.deepcopy(previous['profiles'][1])
        catalog = gate.beta_policy.compose_catalog({'profiles': rows}, previous)
        backups, generated, calls = {}, {}, []
        for prefix, source_rows in [('historical', previous['profiles']), ('fresh', rows)]:
            for row in source_rows:
                identity = row['settings_identity']
                profile = dict(identity, schema='same-schema', definition_sha256='definition',
                               definition={'keys': []}, payload=identity['code_sha256'].encode())
                label = prefix + '-' + row['profile']
                def create(profile=profile, label=label):
                    calls.append(label)
                    return {'source_identity': (profile['ihx_sha256'], profile['code_sha256'])}
                self.producer.add_generated_backup(backups, generated, label, profile, create)
        gate.beta_policy.validate_backup_scope(backups, catalog)
        self.assertEqual(len(backups), 19)
        self.assertEqual(len(calls), 19)
        self.assertNotIn('fresh-game', calls)
        self.assertIn('historical-game', backups)
        matrix = copy.deepcopy(self.matrix)
        sources = gate.beta_policy.source_identities(catalog)
        matrix['sources_per_target'] = len(sources)
        matrix['cases'] = [case for case in matrix['cases'] if case['source'] in sources]
        for case in matrix['cases']:
            if case['target_profile'] == 'game':
                case['target'] = rows[1]['settings_identity']['ihx_sha256']
                case['target_code_sha256'] = rows[1]['settings_identity']['code_sha256']
        self.write('audit/settings-catalog-draft.json', json.dumps(catalog).encode())
        self.write('audit/transition-preflight.json', json.dumps(matrix).encode())
        witness = self.producer.produce_transition_evidence(
            self.root, self.audit, 'main', {'configuration': self.configuration,
                'build_id': self.configuration['nvm_schema']},
            {'build': {'ihx_sha256': rows[0]['settings_identity']['ihx_sha256']},
             'settings_code_sha256': rows[0]['settings_identity']['code_sha256']},
            self.data['transition']['tests'])
        self.assertTrue(witness['passed'])
        self.assertEqual(len(witness['source_images']), 19)
        self.assertEqual(len(matrix['cases']), 190)

    def test_generated_duplicate_conflicts_fail_before_creation(self):
        profile = {'ihx_sha256': 'a' * 64, 'code_sha256': 'b' * 64,
                   'schema': 'schema', 'definition_sha256': 'definition',
                   'definition': {'keys': []}, 'payload': b'exact default'}
        for field, changed in [('code_sha256', 'c' * 64), ('schema', 'other'),
                               ('definition_sha256', 'other'), ('definition', {'keys': [1]}),
                               ('payload', b'different settings')]:
            with self.subTest(field=field):
                backups, generated = {}, {}
                self.producer.add_generated_backup(backups, generated, 'historical', profile,
                    lambda: {'source_identity': ('a' * 64, 'b' * 64)})
                conflicting = dict(profile, **{field: changed})
                with self.assertRaisesRegex(ValueError, 'Conflicting generated'):
                    self.producer.add_generated_backup(backups, generated, 'fresh', conflicting,
                                                       lambda: self.fail('must not create conflict'))
                self.assertEqual(len(backups), 1)

    def test_actual_backup_producer_normalizes_settings_by_image_version(self):
        sys.path.insert(0, str(ROOT / 'tools/installer'))
        import test_catalog_settings as fixtures
        import test_settings_backup as model

        settings = model.settings
        for previous, record, expected_count in (
                (False, settings.extensions.settings_record(version=1), 9),
                (True, bytes(24), 6),
                (True, bytes([0xff]) * 24, 6)):
            with self.subTest(previous=previous, record=record.hex()):
                profile, row = fixtures.profile_for('main', 91)
                if previous:
                    profiles = settings.ak820_profiles
                    config = profiles._configuration('main', profiles.PROFILES['main'])
                    row['configuration'] = config
                    row['settings_identity'] = settings._settings_identity(
                        config, profile['ihx_sha256'], profile['code_sha256'],
                        profile['definition_sha256'], combo_actions=[], macro_layer_tap=False)
                fixtures.bind(fixtures.catalog_for(row), profile)
                nvm = bytearray(profile['payload'][settings.pack.NVM_START-settings.pack.APP_START:
                                                   settings.pack.NVM_END-settings.pack.APP_START])
                nvm[0x6a8:0x6c0] = record
                device = model.WireDevice(profile, nvm)
                folder = self.root / ('backup-' + str(previous) + '-' + record.hex())
                backup = self.producer.make_backup(folder, device.rom(), profile)
                self.assertEqual(len(backup['settings']['extensions']['qmk_settings']), expected_count)
                self.assertEqual(backup['settings']['extensions']['qmk_settings'],
                                 settings.extensions.decode_settings(
                                     settings.extensions.settings_record(version=1 if previous else 2)))
                self.assertEqual(device.requests, [])
                self.assertEqual(device.writes, [])

    def test_generated_sources_do_not_deduplicate_user_backups(self):
        profile = {'ihx_sha256': 'a' * 64, 'code_sha256': 'b' * 64,
                   'schema': 'schema', 'definition_sha256': 'definition',
                   'definition': {}, 'payload': b'default'}
        backup = {'source_identity': ('a' * 64, 'b' * 64)}
        backups = {'physical-user-backup': backup}
        self.producer.add_generated_backup(backups, {}, 'fresh', profile, lambda: backup)
        with self.assertRaisesRegex(ValueError, 'Duplicate backup'):
            gate.beta_policy.validate_backup_scope(backups, {'profiles': [
                {'settings_identity': {'ihx_sha256': 'a' * 64, 'code_sha256': 'b' * 64}}]})

    def test_reject_duplicate_json_key(self):
        path = self.root / 'duplicate.json'
        path.write_text('{"pass": true, "pass": false}')
        with self.assertRaises(ValueError): gate.load(path)


if __name__ == '__main__':
    unittest.main()
