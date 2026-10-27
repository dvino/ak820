"""Policy unit models only; synthetic current identities do not qualify firmware."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import ak820_beta_transition_policy as policy


def previous():
    rows = [{'profile': name, 'settings_identity': {'ihx_sha256': ihx, 'code_sha256': code},
             'configuration': {'profile': name}} for name, (ihx, code) in policy.PREVIOUS_IDENTITIES.items()]
    return {'profiles': rows, 'historical_profiles': [{'profile': 'older-beta'}],
            'historical_sources': [{'ihx_sha256': 'alpha-legacy'}],
            'settings_transitions': [{'source': 'obsolete', 'target': 'obsolete'}]}


def fresh():
    catalog = previous()
    for row in catalog['profiles']:
        name = row['profile']
        row['settings_identity'] = {'ihx_sha256': hashlib.sha256(('new-' + name).encode()).hexdigest(),
                                   'code_sha256': hashlib.sha256(('code-' + name).encode()).hexdigest()}
    return catalog


def backups(catalog):
    return {ihx: {'source_identity': (ihx, code)}
            for ihx, code in policy.source_identities(catalog).items()}


class PreviousBetaPolicyTests(unittest.TestCase):
    def test_only_previous_published_profiles_retained_without_mutation(self):
        old, new = previous(), fresh()
        before = deepcopy((old, new))
        result = policy.compose_catalog(new, old)
        self.assertEqual(result['historical_profiles'], old['profiles'])
        self.assertEqual(result['historical_sources'], [])
        self.assertEqual((old, new), before)

    def test_transition_scope_is_previous_and_current_to_current_only(self):
        result = policy.compose_catalog(fresh(), previous())
        current = {r['settings_identity']['ihx_sha256'] for r in result['profiles']}
        old = {p[0] for p in policy.PREVIOUS_IDENTITIES.values()}
        edges = {(r['source'], r['target']) for r in result['settings_transitions']}
        self.assertEqual(edges, {(source, target) for source in old | current for target in current})
        self.assertEqual(len(edges), 200)
        self.assertFalse(any(target in old for _, target in edges))

    def test_previous_validation_catalog_drops_ancestry(self):
        old = previous()
        result = policy.previous_source_catalog(old)
        self.assertEqual(result['profiles'], [])
        self.assertEqual(result['historical_profiles'], old['profiles'])
        self.assertEqual(result['historical_sources'], [])
        self.assertEqual(result['settings_transitions'], [])

    def test_older_alpha_beta1_beta2_and_unknown_backups_rejected(self):
        catalog = policy.compose_catalog(fresh(), previous())
        older = [
            ('alpha2', 'f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e'),
            ('alpha3', '652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880'),
            ('beta1', 'd505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18'),
            ('beta2', '4544d1fe4bb8e9baf262feef8bab0db60a9e98ca2d547266e6d5ecbc10fb4843'),
            ('unknown', '0' * 64)]
        for label, ihx in older:
            with self.subTest(label=label):
                values = backups(catalog)
                values[label] = {'source_identity': (ihx, '1' * 64)}
                with self.assertRaisesRegex(ValueError, 'exactly previous'):
                    policy.validate_backup_scope(values, catalog)

    def test_complete_previous_and_current_backups_need_no_alpha2(self):
        catalog = policy.compose_catalog(fresh(), previous())
        policy.validate_backup_scope(backups(catalog), catalog)

    def test_duplicate_backup_alias_does_not_inflate_coverage(self):
        catalog = policy.compose_catalog(fresh(), previous())
        values = backups(catalog)
        values['alias'] = deepcopy(next(iter(values.values())))
        with self.assertRaisesRegex(ValueError, 'Duplicate backup'):
            policy.validate_backup_scope(values, catalog)

    def test_missing_previous_profile_or_wrong_code_hash_rejected(self):
        catalog = policy.compose_catalog(fresh(), previous())
        values = backups(catalog)
        del values[next(iter(values))]
        with self.assertRaises(ValueError):
            policy.validate_backup_scope(values, catalog)
        values = backups(catalog)
        key = next(iter(values))
        values[key]['source_identity'] = (key, '0' * 64)
        with self.assertRaises(ValueError):
            policy.validate_backup_scope(values, catalog)

    def test_wrong_previous_profile_identity_rejected(self):
        old = previous()
        old['profiles'][0]['settings_identity']['ihx_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Previous beta image'):
            policy.compose_catalog(fresh(), old)

    def test_duplicate_current_image_rejected(self):
        new = fresh()
        new['profiles'][1]['settings_identity']['ihx_sha256'] = new['profiles'][0]['settings_identity']['ihx_sha256']
        with self.assertRaisesRegex(ValueError, 'Duplicate new'):
            policy.compose_catalog(new, previous())

    def test_unchanged_image_retained_once_only_with_identical_contract(self):
        old, new = previous(), fresh()
        new['profiles'][0] = deepcopy(old['profiles'][0])
        result = policy.compose_catalog(new, old)
        self.assertEqual(len(policy.source_identities(result)), 19)
        new['profiles'][0]['configuration']['changed'] = True
        with self.assertRaisesRegex(ValueError, 'conflicting settings contract'):
            policy.compose_catalog(new, old)

    def test_catalog_digest_is_checked_before_admitting_input(self):
        raw = json.dumps(previous()).encode()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'catalog.json'
            path.write_bytes(raw)
            with self.assertRaisesRegex(ValueError, 'authenticated published'):
                policy.load_previous_catalog(path)
            # Unit-only synthetic pin; production keeps the published beta.3 hash.
            with patch.object(policy, 'PREVIOUS_CATALOG_SHA256', hashlib.sha256(raw).hexdigest()):
                self.assertEqual(policy.load_previous_catalog(path), previous())
                path.write_bytes(raw + b' ')
                with self.assertRaises(ValueError):
                    policy.load_previous_catalog(path)


if __name__ == '__main__':
    unittest.main()
