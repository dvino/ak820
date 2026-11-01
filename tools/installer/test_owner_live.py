"""Offline fake-device tests for operation-owned OEM references."""
import json
from unittest.mock import Mock, patch

import ak820 as app
import test_installer as fixtures
import unittest


class OwnerLiveTests(fixtures.BaseCase):
    def setUp(self):
        super().setUp()
        self.backup = (app.BUNDLE / 'reference/stock-full.bin').read_bytes()
        self.refs = self.root / 'owner'; self.refs.mkdir()
        (self.refs / 'stock-full.bin').write_bytes(self.backup)
        (self.refs / 'native-installed.bin').write_bytes(self.backup[app.packer.APP_START:app.packer.APP_END])

    def native(self, hid):
        owner = self
        class Native:
            native = True
            def rom(self, address, size): return owner.backup[address:address+size]
            def enter_native_loader(self): hid.descriptors = [fixtures.descriptor('LOADER')]
            def close(self): pass
        return Native()

    def test_rc6_validated_reopen_cannot_approve_different_retained_image(self):
        transport = app.transport
        payload = bytearray(self.backup[app.packer.APP_START:app.packer.APP_END])
        payload[app.packer.NVM_END-app.packer.APP_START:0xef80-app.packer.APP_START] = bytes(0x80)
        payload = bytes(payload)
        manifest = {'ihx_sha256': 'i', 'map_sha256': 'm'}
        pins = {'ihx_sha256': 'i', 'map_sha256': 'm', 'payload': app.sha(payload),
                'backup': app.sha(self.backup), 'snapshot': app.sha(self.backup)}
        snapshot = self.root / 'snapshot.bin'; snapshot.write_bytes(self.backup)
        for case in ('payload', 'backup', 'manifest'):
            with self.subTest(case=case):
                changed = bytearray(payload); changed[0] ^= 1
                other = bytearray(self.backup); other[0xa200] ^= 1
                first = (dict(manifest, extra='changed') if case == 'manifest' else manifest,
                         bytes(changed) if case == 'payload' else payload,
                         bytes(other) if case == 'backup' else self.backup)
                approved = (manifest, payload, self.backup)
                with patch.object(transport, 'UPDATE_PINS', pins), \
                     patch.object(transport, 'session_image', side_effect=[first, approved]), \
                     patch.object(transport, 'hid_module', side_effect=AssertionError('HID forbidden')) as hid:
                    with self.assertRaisesRegex(ValueError, 'Prepared update bytes changed'):
                        transport.flash(self.root, 'permanent', False, False, prepared_update_snapshot=snapshot,
                                        reference_bytes=(self.backup, self.backup[app.packer.APP_START:app.packer.APP_END]),
                                        phase_guard=Mock(), loader_descriptor={'path': b'fake'})
                    hid.assert_not_called()

    def test_live_prepare_default_exact_and_reject_mismatch(self):
        for case in ('default', 'exact', 'mismatch'):
            with self.subTest(case=case):
                folder = self.root / ('prepare-' + case); folder.mkdir()
                if case == 'mismatch':
                    (self.refs / 'native-installed.bin').write_bytes(b'wrong')
                args = ['prepare', '--trial']
                if case != 'default': args += ['--reference-dir', str(self.refs)]
                hid = fixtures.FakeHid([fixtures.descriptor('OEM_APP')])
                with patch.object(app, 'Log', return_value=Mock(folder=folder)), \
                     patch.object(app, 'release_context', return_value=self.context), \
                     patch.object(app, 'confirm_preparation'), \
                     patch.object(app, 'hid_module', return_value=hid), \
                     patch.object(app.transport, 'Application', return_value=self.native(hid)), \
                     patch.object(app, 'RECOVERY_REFERENCE', object()):
                    status = app.main(args, interactive=True)
                self.assertEqual(status, 1 if case == 'mismatch' else 0)
                session = folder / 'trial-session'
                self.assertEqual(session.exists(), case != 'mismatch')
                if session.exists():
                    _, _, backup = app.transport.session_image(session, 'trial')
                    self.assertEqual(backup, self.backup)
                self.assertEqual(hid.writes, [])

    def test_post_flash_verification_requires_original_bytes(self):
        payload = b'approved payload'
        manifest = {'ihx_sha256': app.sha(self.context.snapshot.files['firmware/application.ihx']),
                    'map_sha256': app.sha(self.context.snapshot.files['firmware/application.map'])}
        release = self.context.manifest
        references = (self.backup, self.backup[app.packer.APP_START:app.packer.APP_END])
        def capture(output, **kwargs):
            self.assertEqual(kwargs['expected'], payload)
            output.mkdir()
            (output / 'rom.bin').write_bytes(self.backup)
            return {'nvm_and_journal_stable_on_second_read': True, 'status': {'storage_failed': False}}
        for changed in (False, True):
            with self.subTest(changed=changed):
                folder = self.root / ('verify-' + str(changed)); folder.mkdir()
                with patch.object(app, 'RECOVERY_REFERENCE', object()), \
                     patch.object(app, 'load_release', return_value=release), \
                     patch.object(app.transport, 'session_image', return_value=(manifest, b'changed' if changed else payload, self.backup)), \
                     patch.object(app, 'require_state'), patch.object(app, 'boot_status'), \
                     patch.object(app, 'keyboard_smoke', return_value=True), \
                     patch.object(app.diagnostic, 'diagnostic_build_bytes', return_value={}), \
                     patch.object(app.diagnostic, 'capture', side_effect=capture) as readback, \
                     patch.object(app.transport, 'verify_live') as verify:
                    if changed:
                        with self.assertRaisesRegex(ValueError, 'Verification session differs'):
                            app.verify_trial(fixtures.Log(folder), Mock(), folder, {'path': b'fake'}, image='trial',
                                             context=self.context, operation_backup=self.backup,
                                             expected_payload=payload, reference_bytes=references)
                        readback.assert_not_called()
                    else:
                        app.verify_trial(fixtures.Log(folder), Mock(), folder, {'path': b'fake'}, image='trial',
                                         context=self.context, operation_backup=self.backup,
                                         expected_payload=payload, reference_bytes=references)
                        self.assertEqual(verify.call_args.args[:4], (self.backup, payload, 'trial', self.backup))

    def test_install_fake_loader_retains_references_and_rejects_mismatch(self):
        class StopAfterFlash(Exception): pass
        original = app.operation_references
        for case, mode in ((case, mode) for case in ('default', 'exact', 'swapped_after_read', 'mismatch', 'midflight_recovery')
                           for mode in ('trial', 'permanent')):
            with self.subTest(case=case, mode=mode):
                (self.refs / 'stock-full.bin').write_bytes(self.backup)
                (self.refs / 'native-installed.bin').write_bytes(self.backup[app.packer.APP_START:app.packer.APP_END])
                if case == 'mismatch':
                    (self.refs / 'stock-full.bin').write_bytes(self.backup[:-1])
                folder = self.root / ('install-' + case + '-' + mode); folder.mkdir()
                hid = fixtures.TransportTests.loader(self)
                hid.descriptors = [fixtures.descriptor('OEM_APP')]
                native = self.native(hid)
                if case == 'midflight_recovery':
                    def replace_recovery():
                        session = folder / (mode + '-session')
                        changed = bytearray(self.backup); changed[0xA200] ^= 1
                        changed = bytes(changed)
                        app.packer.validate_native(changed)
                        recovery = changed[app.packer.APP_START:app.packer.APP_END]
                        manifest_path = session / 'images.json'
                        manifest = json.loads(manifest_path.read_bytes())
                        manifest['backup_sha256'] = app.sha(changed)
                        manifest['images']['restore-native.bin']['sha256'] = app.sha(recovery)
                        if mode == 'permanent':
                            manifest['native_install_backup_sha256'] = app.sha(changed)
                        manifest['nvm_provenance']['source_sha256'] = app.sha(changed)
                        (session / 'before-full-rom.bin').write_bytes(changed)
                        (session / 'restore-native.bin').write_bytes(recovery)
                        manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
                        _, validated_recovery, validated_backup = app.transport.session_image(session, 'restore')
                        self.assertEqual((validated_backup, validated_recovery), (changed, recovery))
                        hid.descriptors = [fixtures.descriptor('LOADER')]
                    native.enter_native_loader = replace_recovery
                def references(backup, directory=None):
                    result = original(backup, directory)
                    if case == 'swapped_after_read':
                        (self.refs / 'stock-full.bin').write_bytes(b'swapped')
                        (self.refs / 'native-installed.bin').write_bytes(b'swapped')
                    return result
                def consent(_log, plan, **_kwargs):
                    return {'image': mode, 'sha256': plan['sha256'], 'reset': True,
                            'erase': True, 'flash': True, 'restart': True}
                with patch.object(app, 'RECOVERY_REFERENCE', object()), \
                     patch.object(app, 'load_release', return_value={'install_modes': ['permanent', 'trial']}), \
                     patch.object(app, 'confirm_preparation'), patch.object(app, 'consent', side_effect=consent), \
                     patch.object(app, 'operation_references', side_effect=references), \
                     patch.object(app.transport, 'hid_module', return_value=hid) as transport_hid, \
                     patch.object(app.transport, 'Application', return_value=native), \
                     patch.object(app.transport.time, 'sleep'), \
                     patch.object(app, 'wait_state', side_effect=StopAfterFlash()):
                    expected_error = ValueError if case in ('mismatch', 'midflight_recovery', 'swapped_after_read') else StopAfterFlash
                    with self.assertRaises(expected_error) as error:
                        app.install(fixtures.Log(folder), hid, image=mode, context=self.context,
                                    reference_dir=None if case == 'default' else self.refs)
                    if case == 'mismatch': transport_hid.assert_not_called()
                    if case == 'midflight_recovery':
                        self.assertIn('backup differs', str(error.exception))
                if case == 'midflight_recovery':
                    self.assertEqual(hid.commands, [1])
                elif case in ('mismatch', 'swapped_after_read'):
                    self.assertEqual(hid.commands, [])
                    if case == 'mismatch':
                        self.assertFalse((folder / (mode + '-session')).exists())
                else:
                    self.assertEqual(hid.commands, [1, 2, 3, 4, 5])
                    expected = app.expected_install_payload(self.context, self.backup, mode, self.backup)
                    blocks = len(expected)//64
                    self.assertEqual(b''.join(packet[1:] for packet in hid.writes[3:3+blocks]), expected)
                    self.assertEqual((folder / (mode + '-session') / 'before-full-rom.bin').read_bytes(), self.backup)

    def test_reference_change_after_loader_identity_stops_before_erase(self):
        folder = self.root / 'reference-before-erase'; folder.mkdir()
        hid = fixtures.TransportTests.loader(self); hid.descriptors = [fixtures.descriptor('OEM_APP')]
        native = self.native(hid); original_device = hid.device
        def device():
            dev = original_device(); send = dev.send_feature_report
            def change_after_identity(packet):
                result = send(packet)
                if packet[1:5] == b'\x01\xaa\x55\x00': (self.refs / 'stock-full.bin').write_bytes(b'changed')
                return result
            dev.send_feature_report = change_after_identity
            return dev
        hid.device = device
        def consent(_log, plan, **_kwargs):
            return {'image': 'trial', 'sha256': plan['sha256'], 'reset': True,
                    'erase': True, 'flash': True, 'restart': True}
        with patch.object(app, 'RECOVERY_REFERENCE', object()), \
             patch.object(app, 'load_release', return_value={'install_modes': ['permanent', 'trial']}), \
             patch.object(app, 'confirm_preparation'), patch.object(app, 'consent', side_effect=consent), \
             patch.object(app.transport, 'hid_module', return_value=hid), \
             patch.object(app.transport, 'Application', return_value=native), patch.object(app.transport.time, 'sleep'):
            with self.assertRaises(ValueError):
                app.install(fixtures.Log(folder), hid, image='trial', context=self.context, reference_dir=self.refs)
        self.assertEqual(hid.commands, [1])

    def test_changes_during_live_rom_read_stop_before_loader_transition(self):
        for case in ('reference', 'session', 'release'):
            with self.subTest(case=case):
                (self.refs / 'stock-full.bin').write_bytes(self.backup)
                (self.refs / 'native-installed.bin').write_bytes(self.backup[app.packer.APP_START:app.packer.APP_END])
                path = self.context.bundle / 'firmware/application.ihx'
                path.write_bytes(self.context.snapshot.files['firmware/application.ihx'])
                folder = self.root / ('during-rom-' + case); folder.mkdir()
                hid = fixtures.TransportTests.loader(self); hid.descriptors = [fixtures.descriptor('OEM_APP')]
                native = self.native(hid); enter = Mock(wraps=native.enter_native_loader)
                native.enter_native_loader = enter
                def rom(address, size):
                    if size == 65536:
                        if case == 'reference': (self.refs / 'stock-full.bin').write_bytes(b'changed')
                        elif case == 'session': (folder / 'trial-session' / 'before-full-rom.bin').write_bytes(b'changed')
                        else: path.write_bytes(b'changed')
                    return self.backup[address:address+size]
                native.rom = rom
                def release(**_kwargs):
                    app.require(path.read_bytes() == self.context.snapshot.files['firmware/application.ihx'], 'Release changed')
                    return {'install_modes': ['permanent', 'trial']}
                def consent(_log, plan, **_kwargs):
                    return {'image': 'trial', 'sha256': plan['sha256'], 'reset': True,
                            'erase': True, 'flash': True, 'restart': True}
                with patch.object(app, 'RECOVERY_REFERENCE', object()), patch.object(app, 'load_release', side_effect=release), \
                     patch.object(app, 'confirm_preparation'), patch.object(app, 'consent', side_effect=consent), \
                     patch.object(app.transport, 'hid_module', return_value=hid), \
                     patch.object(app.transport, 'Application', return_value=native), patch.object(app.transport.time, 'sleep'):
                    with self.assertRaises(ValueError):
                        app.install(fixtures.Log(folder), hid, image='trial', context=self.context, reference_dir=self.refs)
                enter.assert_not_called()
                self.assertEqual(hid.commands, [])


if __name__ == '__main__':
    unittest.main()
