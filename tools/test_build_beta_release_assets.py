import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from types import SimpleNamespace

import build_beta_release_assets as assets


class BundleValidationTests(unittest.TestCase):
    def test_accepts_ci_reproduced_bundle_and_current_pins(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); bundle = root / 'bundle'
            for part in ('firmware', 'reports', 'reviews'):
                (bundle / part).mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(assets.CANDIDATE_ZIP) as catalog:
                ihx = catalog.read('profiles/work/firmware/application.ihx')
            content = {'firmware/application.ihx': ihx, 'firmware/application.map': b'm',
                       'reports/build-report.json': b'r'}
            for name, data in content.items(): (bundle / name).write_bytes(data)
            (root / 'example.py').write_bytes(b'x')
            policy = {'source_files': {'example.py': {'sha256': assets.sha(b'x'), 'size': 1}}}
            (root / 'ci').mkdir()
            (root / 'ci/release-policy.json').write_text(json.dumps(policy))
            (root / 'ci/release-safety.json').write_text(json.dumps({'program': {'ihx_sha256': assets.WORK_IHX}, 'source_files': {}, 'witnesses': {}}))
            (bundle / 'reviews/program-policy.json').write_bytes((root / 'ci/release-policy.json').read_bytes())
            content['reviews/program-policy.json'] = (bundle / 'reviews/program-policy.json').read_bytes()
            files = {name: {'sha256': assets.sha(data), 'size': len(data)} for name, data in content.items()}
            (bundle / 'reviews/independent-review.md').write_text('review')
            files['reviews/independent-review.md'] = {'sha256': assets.sha(b'review'), 'size': 6}
            manifest = {'files': files, 'host_files': {}}
            (bundle / 'installer-release.json').write_text(json.dumps(manifest))
            record = {'format': 'ak820-reproduced-review-1', 'host_files': {}, 'build': {
                'ihx_sha256': files['firmware/application.ihx']['sha256'],
                'map_sha256': files['firmware/application.map']['sha256'],
                'build_report_sha256': files['reports/build-report.json']['sha256']}}
            identity = root / 'identity.json'
            identity.write_text(json.dumps({'ihx_sha256': assets.WORK_IHX, 'code_sha256': assets.WORK_CODE}))
            with patch.object(assets, 'ROOT', root), patch.object(assets, 'WORK_IDENTITY', identity), \
                 patch.object(assets, 'read_review_record', return_value=record), \
                 patch.object(assets, 'validate_host_manifest'), \
                 patch.object(assets.authorization, 'validate_bundle_authorization') as auth:
                result = assets.validate_bundle(bundle)
                self.assertEqual(result['files']['firmware/application.ihx']['size'], len(ihx))
                auth.assert_called_once()

    def test_rejects_modified_manifest_file(self):
        with tempfile.TemporaryDirectory() as temp:
            bundle = Path(temp); (bundle / 'firmware').mkdir()
            (bundle / 'firmware/application.ihx').write_bytes(b'changed')
            (bundle / 'installer-release.json').write_text(json.dumps({'files': {
                'firmware/application.ihx': {'sha256': '0' * 64, 'size': 1}}}))
            with patch.object(assets, 'ROOT', bundle), self.assertRaisesRegex(ValueError, 'hash/size mismatch'):
                assets.validate_bundle(bundle)

    def test_rejects_unsafe_paths(self):
        for value in ('../escape', '/absolute', 'a\\..\\b', 'a//b', 'a/./b'):
            with self.subTest(value=value), self.assertRaises(ValueError): assets._safe_name(value)

    def test_rejects_symlink_ancestor_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); bundle = root / 'bundle'; outside = root / 'outside'
            (bundle / 'firmware').mkdir(parents=True); outside.mkdir()
            (bundle / 'firmware/application.ihx').write_bytes(b'i')
            (outside / 'build-report.json').write_bytes(b'private')
            (bundle / 'reports').symlink_to(outside, target_is_directory=True)
            files = {
                'firmware/application.ihx': {'sha256': assets.sha(b'i'), 'size': 1},
                'reports/build-report.json': {'sha256': assets.sha(b'private'), 'size': 7},
            }
            (bundle / 'installer-release.json').write_text(json.dumps({'files': files}))
            with patch.object(assets, 'ROOT', root), self.assertRaisesRegex(ValueError, 'Missing or unsafe'):
                assets.validate_bundle(bundle)

    def test_rejects_symlinked_bundle_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); outside = root / 'outside'; outside.mkdir()
            (root / 'linked-bundle').symlink_to(outside, target_is_directory=True)
            with patch.object(assets, 'ROOT', root), self.assertRaisesRegex(ValueError, 'Symlink in bundle path'):
                assets.validate_bundle(root / 'linked-bundle')


class PromotionTests(unittest.TestCase):
    profiles = assets.RELEASE_PROFILES

    @staticmethod
    def ihex_record(address, kind, data):
        body = bytes([len(data), address >> 8, address & 0xff, kind]) + data
        checksum = (-sum(body)) & 0xff
        return ':' + (body + bytes([checksum])).hex().upper() + '\n'

    @classmethod
    def sparse_ihex(cls, value):
        return (cls.ihex_record(0x3027, 0, bytes([value])) +
                cls.ihex_record(0, 1, b'')).encode()

    def make_inputs(self, root):
        import ak820_profiles
        import firmware_matrix
        bundles_root = root / 'bundles'; bundles_root.mkdir()
        contexts, rows, settings_rows, images = [], [], [], []
        for index, profile in enumerate(self.profiles):
            bundle = bundles_root / profile; bundle.mkdir()
            configuration = ak820_profiles.configuration(profile)
            contents = {}
            for name in sorted(set(assets.CI_PUBLIC_FILES) - {'installer-release.json'}):
                path = bundle / name; path.parent.mkdir(parents=True, exist_ok=True)
                if name == 'reports/build-report.json':
                    value = {'configuration': configuration, 'sources': [],
                             'compiler_sha256': f'{index + 1:064x}',
                             'build_id': configuration['nvm_schema'],
                             'hardware_validated': False}
                    data = json.dumps(value).encode()
                elif name == 'firmware/application.ihx':
                    data = self.sparse_ihex(index + 1)
                else:
                    data = (f'{profile}:{name}').encode()
                path.write_bytes(data); contents[name] = data
            files = {name: {'sha256': assets.sha(data), 'size': len(data)}
                     for name, data in contents.items()}
            manifest = {'files': files}
            manifest_path = bundle / 'installer-release.json'
            manifest_path.write_text(json.dumps(manifest))
            approval_path = bundle / 'approved-release.json'; approval_path.write_text('{}')
            ihx, map_hash, mem = (files[f'firmware/application.{ext}']['sha256']
                                  for ext in ('ihx', 'map', 'mem'))
            report_bytes = contents['reports/build-report.json']
            identity = {'profile': profile,
                'configuration_sha256': assets.sha(assets.configure_firmware.canonical(configuration)),
                'ihx_sha256': ihx, 'map_sha256': map_hash, 'mem_sha256': mem,
                'build_report_sha256': assets.sha(report_bytes),
                'source_manifest_sha256': assets.sha(assets.configure_firmware.canonical([])),
                'compiler_sha256': f'{index + 1:064x}', 'nvm_schema': configuration['nvm_schema']}
            code_sha = f'{index + 101:064x}'; definition_sha = f'{index + 201:064x}'
            settings_identity = assets.settings.catalog_settings_identity(
                configuration, ihx, code_sha, definition_sha)
            contexts.append(SimpleNamespace(profile=profile, bundle=bundle,
                manifest=manifest, approval=approval_path))
            row = firmware_matrix.default_row(profile)
            row.update(identity=identity, settings_identity=settings_identity,
                       release_approved=False, installable=False)
            rows.append(row)
            settings_row = firmware_matrix.default_row(profile)
            settings_row.update(identity=identity, settings_identity=settings_identity)
            settings_rows.append(settings_row)
            import build_capability_catalog as capability_builder
            linked_identity = capability_builder.code_identity(
                assets.pack_ak820.read_ihex(bundle / 'firmware/application.ihx'))
            images.append({'profile': profile, 'build_identity': dict(identity),
                'settings_schema': configuration['nvm_schema'],
                'code_identity': linked_identity,
                'features': sorted(configuration['base_features'] + configuration['optional_features'])})
        (root / 'docs/ru').mkdir(parents=True)
        (root / 'docs/INSTALL.md').write_text('AK820-Beta3-Catalog.zip')
        (root / 'docs/ru/INSTALL.md').write_text('AK820-Beta3-Catalog.zip')
        for name in assets.guide_files():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# public guide\n', encoding='utf-8')
        (root / 'tools/installer').mkdir(parents=True)
        (root / 'tools/installer/profile-catalog.json').write_text('{}')
        settings_catalog = {'format': firmware_matrix.FORMAT, 'profiles': settings_rows,
                            'settings_transitions': []}
        capability_catalog = {'images': images}
        matrix = {'format': firmware_matrix.FORMAT, 'profiles': rows}
        (root / 'tools/installer/settings-catalog.json').write_text(json.dumps(settings_catalog))
        (root / 'web').mkdir(exist_ok=True)
        (root / 'web/firmware-matrix.json').write_bytes(assets.canonical(matrix))
        module_profiles = []
        feature_ids = set()
        for profile in self.profiles:
            configuration = ak820_profiles.configuration(profile)
            features = sorted(configuration['base_features'] + configuration['optional_features'])
            feature_ids.update(features)
            module_profiles.append({'id': profile, 'profile': profile, 'default': profile == 'main',
                'title': {'en': profile, 'ru': profile}, 'summary': {'en': 'x', 'ru': 'x'},
                'purpose': {'en': 'x', 'ru': 'x'},
                'optional_features': configuration['optional_features'],
                'configuration': configuration, 'features': features})
        module_descriptions = {'schema': 'ak820-module-descriptions-1',
            'features': [{'id': feature, 'title': {'en': feature, 'ru': feature}}
                         for feature in sorted(feature_ids)], 'profiles': module_profiles}
        (root / 'web/module-descriptions.json').write_bytes(assets.canonical(module_descriptions))
        (root / 'web/capability-catalog.json').write_bytes(assets.canonical(capability_catalog))
        return bundles_root, tuple(contexts), matrix, settings_catalog, capability_catalog

    def test_build_emits_exact_ten_bundles_and_full_public_dependency_closure(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bundles, contexts, *_ = self.make_inputs(root)
            output = root / 'output'
            with patch.object(assets, 'ROOT', root), patch.object(
                    assets.ak820, 'release_contexts', return_value=contexts):
                result = assets.build(bundles, output, 'v0.6.0-beta.2')
            self.assertEqual(result['profiles'], 10)
            archive = output / 'AK820-Beta3-Catalog.zip'
            self.assertEqual((output / 'AK820-Beta3-Catalog.zip.sha256').read_text().split()[0],
                             assets.sha(archive.read_bytes()))
            with zipfile.ZipFile(archive) as zf:
                members = {name: zf.read(name) for name in zf.namelist()}
            descriptor = json.loads(members['release-catalog.json'])
            self.assertEqual(descriptor['default_profile'], 'main')
            self.assertEqual(descriptor['installable_profiles'], list(self.profiles))
            for profile in self.profiles:
                prefix = f'profiles/{profile}/'
                self.assertIn(prefix + 'reference/vial.json', members)
                self.assertIn(prefix + 'reports/qualification.json', members)
                self.assertIn(prefix + 'reviews/program-review.md', members)
                self.assertIn(prefix + 'approved-release.json', members)
            for name in assets.guide_files():
                self.assertIn(name, members)
            manifest = json.loads(members['release-manifest.json'])
            for name, item in manifest['files'].items():
                self.assertEqual({'sha256': assets.sha(members[name]), 'size': len(members[name])}, item)

    def test_rejects_wrong_configuration_identity_settings_or_capability_rows(self):
        for mutation, expected in (
            ('configuration', 'Web matrix identity differs'),
            ('identity', 'Web matrix identity differs'),
            ('settings', 'Build configuration differs'),
            ('capability', 'Capability image differs'),
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                root = Path(temp); bundles, contexts, matrix, setting, capability = self.make_inputs(root)
                profile = self.profiles[0]
                if mutation == 'configuration': matrix['profiles'][0]['configuration']['profile'] = 'game'
                elif mutation == 'identity': matrix['profiles'][0]['identity']['ihx_sha256'] = 'f' * 64
                elif mutation == 'settings': setting['profiles'][0]['configuration']['profile'] = 'game'
                else: capability['images'][0]['build_identity']['profile'] = 'game'
                (root / 'web/firmware-matrix.json').write_bytes(assets.canonical(matrix))
                (root / 'tools/installer/settings-catalog.json').write_text(json.dumps(setting))
                (root / 'web/capability-catalog.json').write_bytes(assets.canonical(capability))
                output = root / 'output'
                with patch.object(assets, 'ROOT', root), patch.object(
                        assets.ak820, 'release_contexts', return_value=contexts), \
                     self.assertRaisesRegex(ValueError, expected):
                    assets.build(bundles, output, 'v0.6.0-beta.2')
                self.assertFalse(output.exists())

    def test_beta3_asset_builder_fails_closed_without_all_ten_approved_contexts(self):
        with tempfile.TemporaryDirectory() as temp:
            bundles, output = Path(temp) / 'bundles', Path(temp) / 'assets'
            bundles.mkdir()
            with patch.object(assets.ak820, 'release_contexts', return_value=()):
                with self.assertRaisesRegex(ValueError, 'all ten'):
                    assets.build(bundles, output, 'v0.6.0-beta.2')
            self.assertFalse(output.exists())

    def test_rejects_duplicate_or_reordered_contexts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); bundles, contexts, *_ = self.make_inputs(root)
            with self.assertRaisesRegex(ValueError, 'exact ten-profile'):
                with patch.object(assets.ak820, 'release_contexts', return_value=contexts[:-1] + (contexts[0],)):
                    with patch.object(assets, 'ROOT', root):
                        assets.build(bundles, root / 'out', 'v0.6.0-beta.2')

    def test_capability_image_order_is_irrelevant_but_profiles_must_be_unique_and_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); bundles, contexts, matrix, setting, capability = self.make_inputs(root)
            capability['images'].reverse()
            (root / 'web/capability-catalog.json').write_bytes(assets.canonical(capability))
            with patch.object(assets, 'ROOT', root), patch.object(
                    assets.ak820, 'release_contexts', return_value=contexts):
                assets.build(bundles, root / 'out', 'v0.6.0-beta.2')
            for invalid in ('duplicate', 'missing'):
                with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as temp2:
                    root = Path(temp2); bundles, contexts, _, _, capability = self.make_inputs(root)
                    if invalid == 'duplicate':
                        capability['images'][-1] = dict(capability['images'][0])
                    else:
                        capability['images'].pop()
                    (root / 'web/capability-catalog.json').write_bytes(assets.canonical(capability))
                    with patch.object(assets, 'ROOT', root), patch.object(
                            assets.ak820, 'release_contexts', return_value=contexts), \
                         self.assertRaisesRegex(ValueError, 'capability catalog needs ten unique'):
                        assets.build(bundles, root / 'out', 'v0.6.0-beta.2')

    def test_linked_code_identity_uses_complete_windows_algorithm_not_settings_code_hash(self):
        import build_capability_catalog as capability_builder
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); bundles, contexts, matrix, setting, capability = self.make_inputs(root)
            expected = capability_builder.code_identity(
                assets.pack_ak820.read_ihex(contexts[0].bundle / 'firmware/application.ihx'))
            self.assertEqual(capability['images'][0]['code_identity'], expected)
            packed_code_hash = setting['profiles'][0]['settings_identity']['code_sha256']
            self.assertNotEqual(expected['sha256'], packed_code_hash)
            payload = {'firmware-matrix.json': assets.canonical(matrix)}
            for context in contexts:
                for ext in ('ihx', 'map', 'mem'):
                    name = f'profiles/{context.profile}/firmware/application.{ext}'
                    payload[name] = (context.bundle / f'firmware/application.{ext}').read_bytes()
            assets.validate_profile_links(payload,
                contexts, setting, capability)

    def test_rejects_module_description_registry_drift_preserving_descriptive_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); self.make_inputs(root)
            value = json.loads((root / 'web/module-descriptions.json').read_bytes())
            value['profiles'][1]['configuration']['profile'] = 'main'
            with self.assertRaisesRegex(ValueError, 'Module description profile'):
                assets.validate_module_descriptions(value)


class StandaloneGuideTests(unittest.TestCase):
    def test_rebases_english_and_russian_links_preserving_external_and_anchors(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for language, directory in [('en', 'docs'), ('ru', 'docs/ru')]:
                source = root / directory / 'INSTALL.md'
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text('[profiles](profiles/README.md#limits) [status](STATUS.md) '
                                  '[web](https://example.com) [anchor](#local)')
                with patch.object(assets, 'ROOT', root):
                    data = assets.standalone_guide(source).decode()
                self.assertIn('](' + directory + '/profiles/README.md#limits)', data)
                self.assertIn('](' + directory + '/STATUS.md)', data)
                self.assertIn('](https://example.com)', data)
                self.assertIn('](#local)', data)


if __name__ == '__main__': unittest.main()
