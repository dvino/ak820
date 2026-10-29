import json
import unittest
from unittest.mock import patch

import audit_documentation as audit


class DocumentationAuditTests(unittest.TestCase):
    def test_current_catalog_matches_computed_profiles(self):
        errors = []
        audit.check_catalog(errors)
        self.assertEqual(errors, [])

    def test_missing_derived_feature_is_rejected(self):
        path = audit.ROOT / 'web/module-descriptions.json'
        catalog = json.loads(path.read_text(encoding='utf-8'))
        catalog['features'] = [f for f in catalog['features'] if f['id'] != 'nkro-reports']
        with patch.object(audit.json, 'loads', return_value=catalog):
            errors = []
            audit.check_catalog(errors)
        self.assertIn('Feature catalog optional IDs differ from SWITCHES', errors)

    def test_missing_derived_profile_feature_is_rejected(self):
        path = audit.ROOT / 'web/module-descriptions.json'
        catalog = json.loads(path.read_text(encoding='utf-8'))
        main = next(profile for profile in catalog['profiles'] if profile['id'] == 'main')
        main['configuration']['base_features'].remove('vialrgb-direct-ram')
        main['features'].remove('vialrgb-direct-ram')
        with patch.object(audit.json, 'loads', return_value=catalog):
            errors = []
            audit.check_catalog(errors)
        self.assertIn('Profile catalog configuration differs from source: main', errors)
        self.assertIn('Profile catalog derived features differ from source: main', errors)


if __name__ == '__main__':
    unittest.main()
