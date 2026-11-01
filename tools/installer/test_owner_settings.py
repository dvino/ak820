"""Offline owner-session settings preparation and transport tests; no device access."""
import contextlib
import io
import json
from pathlib import Path
from unittest.mock import Mock, patch
import unittest

import ak820 as app
import settings_workflow as workflow
import test_installer as fixtures
import test_owner_recovery


class OwnerSettingsTests(fixtures.BaseCase):
    session = test_owner_recovery.OwnerRecoveryTests.session
    references = test_owner_recovery.OwnerRecoveryTests.references

    def setUp(self):
        super().setUp()
        self.stock = (app.BUNDLE / 'reference/stock-full.bin').read_bytes()
        self.refs = self.root / 'owner'; self.refs.mkdir()

    def backup_fixture(self, path, value):
        path.mkdir()
        for name in (*workflow.settings.FILES, 'manifest.json'):
            (path / name).write_bytes(b'')
        (path / 'read-log.jsonl').write_text(value)

    def replace_session(self, path, backup):
        changed = bytearray(backup); changed[0xA200] ^= 1; changed = bytes(changed)
        recovery = changed[app.packer.APP_START:app.packer.APP_END]
        (path / 'before-full-rom.bin').write_bytes(changed)
        (path / 'restore-native.bin').write_bytes(recovery)
        manifest_path = path / 'images.json'; manifest = json.loads(manifest_path.read_bytes())
        manifest['backup_sha256'] = app.sha(changed)
        manifest['images']['restore-native.bin']['sha256'] = app.sha(recovery)
        manifest_path.write_text(json.dumps(manifest))

    def make_context(self, backup):
        bundle = self.context.bundle
        files = dict(self.context.snapshot.files)
        files['reference/vial.json'] = (app.ROOT / 'releases/rc6/reference/vial.json').read_bytes()
        files['reports/build-report.json'] = json.dumps({
            'code_window': [app.packer.CODE_START, app.packer.CODE_END],
            'artifacts': [{'path': 'application.ihx', 'sha256': app.sha(files['firmware/application.ihx'])},
                          {'path': 'application.map', 'sha256': app.sha(files['firmware/application.map'])}]}).encode()
        for name, data in files.items():
            path = bundle / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        manifest = {'files': {name: {'sha256': app.sha(data)} for name, data in files.items()}, 'host_files': {}}
        raw = json.dumps(manifest).encode()
        (bundle / 'installer-release.json').write_bytes(raw)
        approval = self.root / 'approval'; approval.write_bytes(b'approval')
        snapshot = app.ReleaseSnapshot(raw, files, {}, b'approval')
        context = app.ReleaseContext('legacy', bundle, approval, manifest, snapshot=snapshot)
        payload = app.expected_install_payload(context, backup, 'permanent', backup)
        ihx_sha = app.sha(files['firmware/application.ihx'])
        code_sha = app.sha(payload[:app.packer.CODE_END-app.packer.APP_START])
        images = {ihx_sha: {'ihx_sha256': ihx_sha, 'code_sha256': code_sha, 'build_id': app.packer.BUILD_ID}}
        return context, images

    def prepare(self, backup, suffix, reference_dir=None):
        source = self.session(self.root / ('source-'+suffix), backup)
        output = self.root / ('output-'+suffix); output.mkdir()
        context, images = self.make_context(backup)
        with patch.object(app, 'load_release', return_value=context.manifest), \
             patch.object(workflow.settings, '_legacy_images', return_value=images):
            result = workflow.prepare(app, fixtures.Log(output), source,
                                      release_context=context, reference_dir=reference_dir)
        return result, context, images

    def test_prepare_supported_variants_and_exact_explicit_refs(self):
        patched = bytearray(self.stock)
        patched[app.packer.APP_START:app.packer.APP_END] = (app.BUNDLE / 'reference/native-installed.bin').read_bytes()
        patched[0xA000:0xD200] = self.stock[0xA000:0xD200]
        patched[0xD200:0xD380] = b'\xff' * 0x180
        for name, value in (('factory', self.stock), ('patched', bytes(patched))):
            backup = bytearray(value); backup[0xA200] ^= 1; backup = bytes(backup)
            with self.subTest(name=name):
                self.references(backup)
                ctx, _, _ = self.prepare(backup, name, self.refs)
                self.assertEqual(ctx['native'], backup)
                self.assertEqual(ctx['references'], (backup, backup[app.packer.APP_START:app.packer.APP_END]))
                for path in (ctx['source'], ctx['recovery'], ctx['target']):
                    app.require_operation_recovery(path, backup)
                self.assertEqual(ctx['profile']['payload'], app.expected_install_payload(ctx['release_context'], backup, 'permanent', backup))

    def test_mismatch_fails_before_target_or_device(self):
        self.references(self.stock)
        changed = bytearray(self.stock); changed[0xA200] ^= 1; changed = bytes(changed)
        source = self.session(self.root / 'bad-source', changed)
        output = self.root / 'bad-output'; output.mkdir()
        context, images = self.make_context(changed)
        with patch.object(app, 'load_release', return_value=context.manifest), \
             patch.object(workflow.settings, '_legacy_images', return_value=images), \
             patch.object(app, 'hid_module') as hid:
            with self.assertRaises(ValueError):
                workflow.prepare(app, fixtures.Log(output), source, release_context=context, reference_dir=self.refs)
            hid.assert_not_called()
        self.assertEqual(list(output.iterdir()), [])

    def test_session_and_reference_swaps_before_unlock_send_no_write(self):
        for case in ('source', 'destination', 'target', 'reference'):
            with self.subTest(case=case):
                self.references(self.stock)
                ctx, release, images = self.prepare(self.stock, case, self.refs)
                saved = self.root / ('saved-'+case); self.backup_fixture(saved, 'saved')
                hid = Mock(); device = hid.device.return_value
                selected = {'path': b'fake'}
                def state(*_args, **_kwargs):
                    if case == 'reference':
                        (self.refs / 'stock-full.bin').write_bytes(b'changed')
                    else:
                        self.replace_session(ctx[{'source':'source', 'destination':'recovery', 'target':'target'}[case]], self.stock)
                    return selected
                with patch.object(app, 'load_release', return_value=release.manifest), \
                     patch.object(workflow.settings, '_legacy_images', return_value=images), \
                     patch.object(workflow, 'backup', return_value={'path': saved, 'identity': {}}), \
                     patch.object(workflow.settings, 'plan_restore', return_value={}), \
                     patch.object(workflow.settings, 'validate_backup', side_effect=lambda *a, **k: ({'path': saved, 'identity': {}}, {}) if k.get('retain_files') else {'path': saved, 'identity': {}}), \
                     patch.object(workflow, 'describe'), patch.object(app, 'require_state', side_effect=state), \
                     patch.object(app.transport, 'Application', return_value=device), \
                     contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(ValueError): workflow.update(app, fixtures.Log(self.root), hid, ctx, saved)
                device.vial_unlock_command.assert_not_called()
                device.enter_vial_loader.assert_not_called()

    def test_restore_rechecks_inputs_before_settings_setter(self):
        for case in ('normal', 'source', 'reference'):
            with self.subTest(case=case):
                self.references(self.stock)
                ctx, release, images = self.prepare(self.stock, 'restore-'+case, self.refs)
                saved = self.root / ('restore-backup-'+case); self.backup_fixture(saved, 'saved')
                setter = Mock(); api = Mock()
                def source_recheck(*_args):
                    if case == 'source': self.replace_session(ctx['source'], self.stock)
                    if case == 'reference': (self.refs / 'native-installed.bin').write_bytes(b'changed')
                def fake_restore(_api, _saved, _profile, *, before_write, target_backup):
                    before_write(); setter(); return {'verified': True}
                def unlock(_host, _log, _hid, _selected, _digest, **kwargs): kwargs['prewrite']()
                with patch.object(app, 'load_release', return_value=release.manifest), \
                     patch.object(workflow.settings, '_legacy_images', return_value=images), \
                     patch.object(workflow.settings, 'validate_backup', side_effect=lambda *a, **k: ({'path': saved, 'identity': {}}, {}) if k.get('retain_files') else {'path': saved, 'identity': {}}), \
                     patch.object(workflow.settings, 'require_target_backup', return_value={'path': saved, 'identity': {}, 'nvm': b''}), \
                     patch.object(workflow.settings, 'plan_restore', return_value={}), \
                     patch.object(workflow.settings, 'recheck_source', side_effect=source_recheck), \
                     patch.object(workflow.settings, 'restore_settings', side_effect=fake_restore), \
                     patch.object(workflow, 'open_api', return_value=api), \
                     patch.object(workflow, 'physical_unlock', side_effect=unlock), \
                     patch.object(workflow, 'describe'), \
                     patch.object(app, 'require_state', return_value={'path': b'fake'}), \
                     contextlib.redirect_stdout(io.StringIO()):
                    if case == 'normal':
                        workflow.restore(app, fixtures.Log(self.root), Mock(), ctx, saved, target_backup={'nvm': b''})
                        setter.assert_called_once()
                    else:
                        with self.assertRaises(ValueError):
                            workflow.restore(app, fixtures.Log(self.root), Mock(), ctx, saved, target_backup={'nvm': b''})
                        setter.assert_not_called()

    def test_nested_restore_does_not_complete_update_before_final_checks(self):
        for case in ('normal', 'reference', 'backup', 'target'):
            with self.subTest(case=case):
                self.references(self.stock)
                ctx, release, images = self.prepare(self.stock, 'nested-'+case, self.refs)
                saved = self.root / ('nested-backup-'+case); self.backup_fixture(saved, 'saved'); marker = saved / 'read-log.jsonl'
                payload = ctx['profile']['payload']
                rom = bytes(app.packer.APP_START) + payload
                target_dir = self.root / ('nested-target-'+case); self.backup_fixture(target_dir, 'target')
                target = {'path': target_dir, 'identity': {}, 'rom': rom, 'nvm': payload[app.packer.NVM_START-app.packer.APP_START:app.packer.NVM_END-app.packer.APP_START]}
                source = {'path': saved, 'identity': {}}
                application = Mock(); application.vial_unlock_status.return_value = (1, 0)
                api = Mock(); stages = []
                def emit(_host, stage, purpose, **_kwargs): stages.append((stage, purpose))
                def unlock(_host, _log, _hid, _selected, _digest, **kwargs): kwargs['prewrite']()
                real_restore = workflow.restore
                def nested(*args, **kwargs):
                    result = real_restore(*args, **kwargs)
                    if case == 'reference': (self.refs / 'stock-full.bin').write_bytes(b'changed')
                    if case == 'backup': marker.write_text('changed')
                    if case == 'target': (target_dir / 'read-log.jsonl').write_text('changed')
                    return result
                def restore_settings(_api, _saved, _profile, *, before_write, target_backup):
                    before_write(); return {'verified': True}
                output = io.StringIO(); log = fixtures.Log(self.root)
                with patch.multiple(app, load_release=Mock(return_value=release.manifest),
                                    require_state=Mock(return_value=fixtures.descriptor('VIAL_APP')),
                                    wait_state=Mock(return_value=fixtures.descriptor('VIAL_APP')), boot_status=Mock()), \
                     patch.multiple(workflow.settings, _legacy_images=Mock(return_value=images),
                                    validate_backup=Mock(side_effect=lambda path, *_a, **kw: ((target if Path(path) == target_dir else source), {}) if kw.get('retain_files') else (target if Path(path) == target_dir else source)),
                                    require_target_backup=Mock(return_value=target),
                                    plan_restore=Mock(return_value={}), recheck_source=Mock(),
                                    restore_settings=Mock(side_effect=restore_settings)), \
                     patch.multiple(workflow, backup=Mock(side_effect=[source, target]), restore=Mock(side_effect=nested),
                                    emit=Mock(side_effect=emit), open_api=Mock(return_value=api),
                                    physical_unlock=Mock(side_effect=unlock), describe=Mock()), \
                     patch.multiple(app.transport, Application=Mock(return_value=application), flash=Mock()), \
                     contextlib.redirect_stdout(output):
                    if case == 'normal': workflow.update(app, log, Mock(), ctx, saved)
                    else:
                        with self.assertRaises(ValueError): workflow.update(app, log, Mock(), ctx, saved)
                events = [event['event'] for event in log.events]
                self.assertIn('nested_settings_restore_verified', events)
                self.assertNotIn('settings_restore_verified', events)
                self.assertEqual('settings_update_verified' in events, case == 'normal')
                self.assertIn(('verifying', 'restore'), stages)
                self.assertNotIn(('complete', 'restore'), stages)
                self.assertEqual(('complete', 'update') in stages, case == 'normal')
                self.assertEqual('Settings restored and verified' in output.getvalue(), case == 'normal')

    def test_update_fake_loader_retains_bytes_and_fails_closed_on_race(self):
        for case in ('normal', 'source', 'destination', 'target', 'reference', 'release', 'progress_backup', 'progress_cancel'):
            with self.subTest(case=case):
                self.references(self.stock)
                ctx, release, images = self.prepare(self.stock, 'flash-'+case, self.refs)
                saved = self.root / ('backup-'+case); self.backup_fixture(saved, 'saved')
                hid = fixtures.TransportTests.loader(self)
                descriptor = fixtures.descriptor('LOADER')
                if case not in ('normal', 'progress_backup', 'progress_cancel'):
                    original_device = hid.device
                    def device():
                        dev = original_device(); send = dev.send_feature_report
                        def send_with_swap(packet):
                            result = send(packet)
                            if packet[1:5] == b'\x01\xaa\x55\x00':
                                if case == 'reference':
                                    (self.refs / 'stock-full.bin').write_bytes(b'changed')
                                elif case == 'release':
                                    (release.bundle / 'firmware/application.ihx').write_bytes(b'changed')
                                else:
                                    self.replace_session(ctx[{'source':'source', 'destination':'recovery', 'target':'target'}[case]], self.stock)
                            return result
                        dev.send_feature_report = send_with_swap
                        return dev
                    hid.device = device
                application = Mock(); application.vial_unlock_status.return_value = (1, 0)
                api = Mock()
                class StopAfterFlash(Exception): pass
                def wait(_hid, mode, **_kwargs):
                    if mode == 'LOADER': return descriptor
                    raise StopAfterFlash()
                def unlock(_host, _log, _hid, _selected, _digest, **kwargs): kwargs['prewrite']()
                import threading
                cancel_event = threading.Event()
                def progress(stage, _payload):
                    if stage == 'flashing':
                        if case == 'progress_backup': (saved/'read-log.jsonl').write_text('changed')
                        if case == 'progress_cancel': cancel_event.set()
                with patch.object(app, 'PROGRESS', progress), patch.object(app, 'CANCEL_EVENT', cancel_event), \
                     patch.object(app, 'load_release', return_value=release.manifest), \
                     patch.object(workflow.settings, '_legacy_images', return_value=images), \
                     patch.object(workflow, 'backup', return_value={'path': saved, 'identity': {}}), \
                     patch.object(workflow.settings, 'plan_restore', return_value={}), \
                     patch.object(workflow.settings, 'validate_backup', side_effect=lambda *a, **k: ({'path': saved, 'identity': {}}, {}) if k.get('retain_files') else {'path': saved, 'identity': {}}), \
                     patch.object(workflow.settings, 'recheck_source'), \
                     patch.object(workflow, 'open_api', return_value=api), \
                     patch.object(workflow, 'physical_unlock', side_effect=unlock), \
                     patch.object(workflow, 'describe'), \
                     patch.object(app, 'require_state', return_value=descriptor), \
                     patch.object(app, 'wait_state', side_effect=wait), \
                     patch.object(app.transport, 'Application', return_value=application), \
                     patch.object(app.transport, 'hid_module', return_value=hid), \
                     patch.object(app.transport.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
                    expected = StopAfterFlash if case == 'normal' else app.Cancelled if case == 'progress_cancel' else ValueError
                    with self.assertRaises(expected):
                        workflow.update(app, fixtures.Log(self.root), hid, ctx, saved)
                if case == 'normal':
                    self.assertEqual(hid.commands, [1, 2, 3, 4, 5])
                    payload = ctx['profile']['payload']; blocks = len(payload)//64
                    self.assertEqual(b''.join(packet[1:] for packet in hid.writes[3:3+blocks]), payload)
                else:
                    self.assertEqual(hid.commands, [1])


if __name__ == '__main__':
    unittest.main()
