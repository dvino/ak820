"""Offline selected-image admission and propagation; no HID or device access."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import ak820 as app


class ProfileSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.catalog = json.loads(Path(__file__).with_name('profile-catalog.json').read_text())
        path = self.root / 'tools/installer/profile-catalog.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(self.catalog))
        self.addCleanup(patch.stopall)
        patch.object(app, 'ROOT', self.root).start()
        self.loader = patch.object(app, '_load_release', side_effect=self.load).start()
        for row in self.catalog['profiles']:
            path = self.root / row['bundle'] / 'reports/build-report.json'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({'configuration': app.ak820_profiles.configuration(row['id'])}))
            (path.parents[1] / 'installer-release.json').write_text(row['id'])
            (path.parents[1] / 'approved-release.json').write_text('test approval')

    def load(self, bundle, approval, *, approved):
        return {'files': {'firmware/application.ihx': {'sha256': bundle.name},
                          'firmware/application.map': {'sha256': bundle.name + '-map'}},
                'host_files': {'tools/installer/profile-catalog.json': {}},
                'install_modes': ['permanent','trial']}

    def test_all_ten_contexts_and_default(self):
        contexts = app.release_contexts(approved=True)
        self.assertEqual([c.profile for c in contexts], [r['id'] for r in self.catalog['profiles']])
        self.assertEqual(app.release_context(approved=True).profile, 'main')
        for context in contexts:
            self.assertEqual(context.bundle, self.root / ('releases/beta4/' + context.profile))
            self.assertEqual(context.approval, context.bundle / 'approved-release.json')
        self.assertTrue(all(c.kwargs['approved'] for c in self.loader.call_args_list))

    def test_unknown_missing_invalid_catalog_never_falls_back(self):
        with self.assertRaisesRegex(ValueError, 'Unknown installer profile'):
            app.release_context('work', approved=True)
        path = self.root / 'tools/installer/profile-catalog.json'
        bad = copy.deepcopy(self.catalog)
        bad['profiles'][0]['bundle'] = '../another'
        path.write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, 'asset path'):
            app.release_context('main', approved=True)
        path.unlink()
        with self.assertRaisesRegex(ValueError, 'catalog is missing'):
            app.release_context('main', approved=True)

    def test_release_directory_must_be_reviewed_and_paths_cannot_escape(self):
        path = self.root / 'tools/installer/profile-catalog.json'
        for version in ('../beta4', 'beta4/../../elsewhere', 'beta5', '', None):
            bad = copy.deepcopy(self.catalog)
            bad['release_dir'] = version
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, 'release directory'):
                app.profile_catalog()
        bad = copy.deepcopy(self.catalog)
        bad['profiles'][0]['bundle'] = 'releases/beta3/main'
        path.write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, 'asset path'):
            app.profile_catalog()
        path.write_text(json.dumps(self.catalog))
        # An absent or mixed release is rejected before opening the keyboard.
        missing = self.root / self.catalog['profiles'][0]['bundle'] / 'approved-release.json'
        missing.unlink(missing_ok=True)
        with self.assertRaisesRegex(ValueError, 'Exact approved profile assets'):
            app.release_context('main', approved=True)

    def test_wrong_image_profile_and_unbound_catalog(self):
        report = self.root / 'releases/beta4/game/reports/build-report.json'
        report.write_text(json.dumps({'configuration': app.ak820_profiles.configuration('main')}))
        with self.assertRaisesRegex(ValueError, 'build configuration'):
            app.release_context('game', approved=True)
        self.loader.side_effect = lambda *a, **kw: {'host_files': {}}
        with self.assertRaisesRegex(ValueError, 'bound to approved'):
            app.release_context('main', approved=True)

    def test_revalidation_detects_changed_approval_or_manifest(self):
        context = app.release_context('typing', approved=True)
        self.loader.side_effect = ValueError('Approval does not match exact release bytes')
        with self.assertRaisesRegex(ValueError, 'Approval'):
            app.load_release(approved=True, context=context)
        self.loader.side_effect = lambda *a, **kw: {'host_files': {'tools/installer/profile-catalog.json': {}}, 'changed': True}
        with self.assertRaisesRegex(ValueError, 'inputs changed'):
            app.load_release(approved=True, context=context)

    def test_cross_profile_session_rejected_even_with_same_firmware(self):
        main = app.release_context('main', approved=True)
        game = app.release_context('game', approved=True)
        session = {'installer_release': app.session_release_identity(main)}
        app.require_session_release(session, main)
        with self.assertRaisesRegex(ValueError, 'another profile'):
            app.require_session_release(session, game)
        with self.assertRaisesRegex(ValueError, 'another profile'):
            app.require_session_release({}, main)

    def test_verify_rejects_session_before_opening_device(self):
        context = app.release_context('code', approved=True)
        with patch.object(app.transport, 'session_image', return_value=({},b'',b'')), \
             patch.object(app, 'require_state') as state:
            with self.assertRaisesRegex(ValueError, 'another profile'):
                app.verify_trial(Mock(), Mock(), self.root, {'path': b'no-device'}, context=context)
            state.assert_not_called()

    def test_trial_preparation_uses_selected_assets_and_records_identity(self):
        context = app.release_context('mmo', approved=True)
        folder = self.root / 'session-log'
        folder.mkdir()
        backup = bytes(65536)
        def write_trial(ihx, mapfile, stock, native, before, dest, *, target_build_id):
            self.assertEqual(target_build_id, app.packer.EXTENSION_BUILD_ID)
            dest.mkdir()
            return {'images': {'ak820-vial-trial.bin': {}, 'restore-native.bin': {}}, 'migration': {}}
        plan = {'sha256': app.sha(backup[app.packer.APP_START:app.packer.APP_END])}
        with patch.object(app, 'capture_references'), patch.object(app, 'RECOVERY_REFERENCE', self.root), \
             patch.object(app, 'write_trial', side_effect=write_trial) as writer, \
             patch.object(app.transport, 'plan', return_value=plan):
            session, _ = app.prepare_trial(Mock(folder=folder), backup, image='trial', context=context)
        self.assertEqual(writer.call_args.args[:2],
                         (context.bundle/'firmware/application.ihx', context.bundle/'firmware/application.map'))
        metadata = json.loads((session/'images.json').read_text())
        self.assertEqual(metadata['installer_release'], app.session_release_identity(context))

    def test_install_keeps_one_selected_context_through_consent_and_verification(self):
        context = app.release_context('creative', approved=True)
        backup = bytes(65536)
        payload = bytes(app.packer.APP_END-app.packer.APP_START)
        metadata = {'installer_release': app.session_release_identity(context)}
        plan = {'sha256': app.sha(payload)}
        with patch.object(app, 'confirm_preparation'), \
             patch.object(app, 'inventory', return_value=('OEM_APP', {'path': b'fake'})), \
             patch.object(app, 'capture_native', return_value=backup), \
             patch.object(app, 'prepare_trial', return_value=(self.root, plan)) as prepare, \
             patch.object(app, 'consent', return_value={}) as consent, \
             patch.object(app.transport, 'flash') as flash, \
             patch.object(app, 'wait_state', return_value={'path': b'fake'}), \
             patch.object(app, 'verify_trial', return_value=backup) as verify, \
             patch.object(app.transport, 'session_image', return_value=(metadata,payload,backup)):
            app.install(Mock(), Mock(), context=context)
        self.assertIs(prepare.call_args.kwargs['context'], context)
        self.assertIs(consent.call_args.kwargs['context'], context)
        self.assertIs(verify.call_args.kwargs['context'], context)
        self.assertEqual(flash.call_args.args[0], self.root)

    def test_manifest_snapshot_cannot_be_mutated_by_a_caller(self):
        context = app.release_context('main', approved=True)
        changed = context.manifest
        changed['files']['firmware/application.ihx']['sha256'] = 'modified'
        self.assertEqual(context.manifest['files']['firmware/application.ihx']['sha256'], 'main')
        app.load_release(approved=True, context=context)

    def test_cli_verify_propagates_selected_context_without_hid(self):
        with patch.object(app, 'Log'), patch.object(app, 'hid_module', side_effect=AssertionError('HID forbidden')):
            self.assertEqual(app.main(['verify','--profile','pointer']), 0)
        self.assertEqual(self.loader.call_args.args[0].name, 'pointer')


if __name__ == '__main__':
    unittest.main()
