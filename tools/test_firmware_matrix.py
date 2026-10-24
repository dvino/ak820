#!/usr/bin/env python3
"""Curated candidate coverage, selection and fail-closed status tests."""
import copy
import json
from pathlib import Path
import tempfile
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import firmware_matrix as matrix


class MatrixTests(unittest.TestCase):
    def setUp(self):
        self.catalog = ('standard', 'full', 'full-leader', 'full-mouse')
        self.patch = patch.object(matrix.profiles, 'RELEASE_PROFILES', self.catalog, create=True)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_only_curated_profiles_are_exposed(self):
        result = matrix.matrix()
        self.assertEqual([row['profile'] for row in result['profiles']], list(self.catalog))
        self.assertEqual(len(result['modules']), len(matrix.profiles.SWITCHES))
        for row in result['profiles']:
            self.assertIsNone(row['resources'])
            self.assertEqual(row['runtime_status'], 'not-proven')
            self.assertFalse(row['installable'])
            self.assertIsNone(row['settings_identity'])
            self.assertTrue(row['build_recipe']['short_calls'])

    def test_exact_then_smallest_superset_catalog_tiebreak(self):
        self.assertEqual(matrix.resolve([])[0], 'standard')
        self.assertEqual(matrix.resolve(['leader']), ['full-leader'])
        self.assertEqual(matrix.resolve(['one-shot'])[0], 'full')
        self.assertEqual(matrix.resolve(['one-shot', 'space-cadet', 'nkro-control'])[0], 'full')
        self.assertEqual(matrix.resolve(['leader', 'mouse-keys']), [])

    def test_unknown_and_duplicate_features_rejected(self):
        for features in (['unknown'], ['leader', 'leader']):
            with self.assertRaises(ValueError):
                matrix.resolve(features)

    def test_uncovered_modules_are_explicit(self):
        result = matrix.matrix()
        self.assertFalse(result['complete_module_coverage'])
        self.assertIn('tap-dance', result['uncovered_modules'])
        leader = next(row for row in result['modules'] if row['feature'] == 'leader')
        self.assertEqual(leader['profiles'], ['full-leader'])

    def test_measurements_must_match_catalog(self):
        measured = matrix.default_row('full')
        measured['configuration']['nvm_schema'] += 1
        with self.assertRaises(ValueError):
            matrix.matrix({'full': measured})
        with self.assertRaises(ValueError):
            matrix.matrix({'not-a-candidate': {}})

    def test_catalog_rejects_duplicates_and_unknowns(self):
        for catalog in ((), ('standard', 'standard'), ('unknown',)):
            with patch.object(matrix.profiles, 'RELEASE_PROFILES', catalog):
                with self.assertRaises(ValueError):
                    matrix.candidate_names()

    def test_pairwise_scope_and_reason(self):
        result = matrix.matrix()
        self.assertEqual(len(result['feature_pairs']), 91)
        pair = next(row for row in result['feature_pairs'] if row['features'] == ['leader', 'mouse-keys'])
        self.assertEqual(pair['disabled_reason'], 'no_catalog_profile')
        self.assertEqual(pair['profiles'], [])

    def test_import_rejects_stale_identity_and_failed_inspection(self):
        import configure_firmware as configured
        fresh = {'configuration': matrix.profiles.configuration('full'),
                 'identity': {'ihx_sha256': 'current'}, 'resources': {}, 'short_calls': None}
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / 'configuration-report.json').write_text(json.dumps({'identity': {'ihx_sha256': 'stale'}}))
            with patch.object(configured, 'inspect', return_value=fresh):
                with self.assertRaisesRegex(ValueError, 'different image'):
                    matrix.measured_row(directory, directory)
            with patch.object(configured, 'inspect', side_effect=ValueError('link failed')):
                with self.assertRaisesRegex(ValueError, 'link failed'):
                    matrix.measured_row(directory, directory)

    def test_import_does_not_promote_unproved_pass_claim(self):
        import configure_firmware as configured
        fresh = {'configuration': matrix.profiles.configuration('full'),
                 'identity': {'ihx_sha256': 'current'}, 'resources': {}, 'short_calls': None}
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            (directory / 'configuration-report.json').write_text(json.dumps({'identity': fresh['identity'], 'offline_tests_passed': True}))
            with patch.object(configured, 'inspect', return_value=fresh), \
                    patch.object(configured, 'validate_tests', side_effect=ValueError('empty suite')):
                with self.assertRaisesRegex(ValueError, 'empty suite'):
                    matrix.measured_row(directory, directory)

    def test_settings_contract_uses_single_catalog_shape(self):
        sys.path.insert(0, str(matrix.ROOT / 'tools/installer'))
        import settings_backup as settings
        row = matrix.default_row('full')
        row['identity'] = {'ihx_sha256': '1' * 64, 'nvm_schema': row['configuration']['nvm_schema']}
        row['settings_identity'] = settings.catalog_settings_identity(row['configuration'], '1' * 64, '2' * 64, '3' * 64)
        catalog = matrix.matrix({'full': row})
        images = settings._catalog_images(catalog)
        self.assertEqual(list(images), ['1' * 64])
        self.assertEqual(images['1' * 64]['code_sha256'], '2' * 64)
        self.assertEqual(catalog['settings_transitions'], [])
        row['settings_identity']['supported_keycodes'].append(65535)
        with self.assertRaises(ValueError):
            settings._catalog_images(matrix.matrix({'full': row}))

    def test_settings_hash_covers_contiguous_packed_code(self):
        import pack_ak820 as pack
        captured = {}
        def helper(configuration, ihx, code, definition):
            captured.update(configuration=configuration, ihx=ihx, code=code, definition=definition)
            return captured
        settings = SimpleNamespace(catalog_settings_identity=helper, canonical=lambda value: b'definition')
        payload = bytes((index % 251 for index in range(pack.APP_END - pack.APP_START)))
        fresh = {'configuration': matrix.profiles.configuration('full'), 'identity': {'ihx_sha256': 'linked-hash'}}
        with tempfile.TemporaryDirectory() as tmp:
            native = Path(tmp) / 'native.bin'
            native.write_bytes(b'native')
            with patch.dict(sys.modules, {'settings_backup': settings}), \
                    patch.object(pack, 'validate_native') as validate, \
                    patch.object(pack, 'read_ihex', return_value={}), \
                    patch.object(pack, 'read_symbols', return_value={}), \
                    patch.object(pack, 'pack', return_value=payload) as packed, \
                    patch.object(pack, 'verify_payload'):
                result = matrix.settings_identity(Path(tmp), fresh, native)
            validate.assert_called_once_with(b'native')
            self.assertFalse(packed.call_args.args[4])
            self.assertEqual(result['code'], pack.digest(payload[:pack.CODE_END - pack.APP_START]))
            self.assertEqual(result['ihx'], 'linked-hash')

    def test_matrix_does_not_modify_measurement(self):
        measured = matrix.default_row('full')
        measured.update(measurement_status='linked-memory-pass', resources={'code_bytes': 123})
        original = copy.deepcopy(measured)
        result = matrix.matrix({'full': measured})
        result['profiles'][1]['resources']['code_bytes'] = 999
        self.assertEqual(measured, original)
        self.assertFalse(original['release_approved'])


if __name__ == '__main__':
    unittest.main()
