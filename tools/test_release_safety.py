"""Offline synthetic witness contract tests; these do not qualify firmware."""
import copy
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
        self.configuration = configuration('full')
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
            'transition': {'format': 'ak820-settings-transition-1', 'passed': True, 'offline_only': True,
                           'physical_device_commands': 0, 'target': {'ihx_sha256': ihx, 'schema': 532482, 'optional_features': self.configuration['optional_features']},
                           'source_images': [gate.ALPHA2_IHX_SHA256], 'tests': [{'exit_code': 0}]}}

        transition = self.data['transition']
        log = self.write('evidence/transition.log', b'synthetic successful log')
        transition['tests'][0].update(source_files={name: record['sha256'] for name, record in sources.items()},
                                     log_path='evidence/transition.log', log_sha256=log['sha256'])
        self.alpha = dict(passed=True, offline_only=True, physical_device_commands=0,
                          key_count=498, encoder_count=12, combo_count=0,
                          source=gate.ALPHA2_IHX_SHA256, source_case='alpha2-saved-rom',
                          target=ihx, target_profile=self.configuration['profile'],
                          combo_restore=copy.deepcopy(gate.ALPHA2_COMBO_RESTORE))
        self.refresh_alpha()

    def refresh_alpha(self):
        record = self.write('evidence/preflight.json', json.dumps(self.alpha).encode())
        self.data['transition']['actual_alpha2_preflight'] = dict(
            self.alpha, result_path='evidence/preflight.json', result_sha256=record['sha256'])

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return {'size': len(data), 'sha256': gate.sha(data)}

    def validate(self):
        for key, value in self.data.items():
            name = 'witnesses/' + key + '.json'
            self.proof['witnesses'][key] = dict(path=name, **self.write(name, json.dumps(value).encode()))
        self.write('ci/release-safety.json', json.dumps(self.proof).encode())
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

    def test_positive_reviewed_work_configuration(self):
        self.configuration.clear()
        self.configuration.update(configuration('work'))
        self.data['transition']['target']['optional_features'] = self.configuration['optional_features']
        self.alpha['target_profile'] = 'work'
        self.refresh_alpha()
        self.assertEqual(self.validate()['stack_bound'], 93)

    def test_reject_unreviewed_profile(self):
        self.report['configuration'] = configuration('work')
        with self.assertRaisesRegex(ValueError, 'reviewed exact image'):
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

    def test_reject_changed_preflight(self):
        self.write('evidence/preflight.json', b'changed')
        with self.assertRaisesRegex(ValueError, 'preflight evidence changed'): self.validate()

    def test_positive_alpha2_preserves_target_combos(self):
        self.assertEqual(self.alpha['combo_restore']['plan_combo_entries'], None)
        self.assertEqual(self.validate()['stack_bound'], 93)

    def test_reject_alpha2_wrong_identity(self):
        for key, value in (('source', '0' * 64), ('target', '0' * 64),
                           ('target_profile', 'other'), ('source_case', 'other')):
            with self.subTest(key=key):
                original = self.alpha[key]
                self.alpha[key] = value
                self.refresh_alpha()
                with self.assertRaisesRegex(ValueError, 'source/target'): self.validate()
                self.alpha[key] = original
        self.refresh_alpha()
        self.data['transition']['source_images'] = ['other image']
        with self.assertRaisesRegex(ValueError, 'source/target'): self.validate()

    def test_reject_alpha2_invalid_preservation_plan(self):
        for key, value in (('combo_count', 8), ('combo_count', False),
                           ('key_count', 497), ('encoder_count', 11),
                           ('physical_device_commands', False), ('offline_only', False),
                           ('combo_restore', None), ('combo_restore', {}),
                           ('combo_restore', dict(gate.ALPHA2_COMBO_RESTORE, source_combos_version=1)),
                           ('combo_restore', dict(gate.ALPHA2_COMBO_RESTORE, plan_combo_entries=[])),
                           ('combo_restore', dict(gate.ALPHA2_COMBO_RESTORE, target_policy='overwrite'))):
            with self.subTest(key=key, value=value):
                original = self.alpha[key]
                self.alpha[key] = value
                self.refresh_alpha()
                with self.assertRaisesRegex(ValueError, 'preservation'): self.validate()
                self.alpha[key] = original

    def test_reject_alpha2_evidence_wrapper_disagreement(self):
        self.data['transition']['actual_alpha2_preflight']['target'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'content differs'): self.validate()

    def test_reject_alpha2_malformed_evidence_with_matching_hash(self):
        for content in (b'not JSON', b'[]', b'{"passed": true, "passed": true}'):
            with self.subTest(content=content):
                record = self.write('evidence/preflight.json', content)
                self.data['transition']['actual_alpha2_preflight']['result_sha256'] = record['sha256']
                with self.assertRaises(ValueError): self.validate()

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
                 'ci/release-safety.json'}
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
            for missing in ('ci/release-safety.json', 'witnesses/irq.json',
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
            record['release_safety_manifest_sha256'] = bundle.sha(self.root / 'ci/release-safety.json')
            bundle.validate_review(review, ihx, mapfile, report)
            self.write('ci/release-safety.json', b'changed manifest')
            with self.assertRaisesRegex(ValueError, 'release safety evidence'):
                bundle.validate_review(review, ihx, mapfile, report)

    def test_reject_duplicate_json_key(self):
        path = self.root / 'duplicate.json'
        path.write_text('{"pass": true, "pass": false}')
        with self.assertRaises(ValueError): gate.load(path)


if __name__ == '__main__':
    unittest.main()
