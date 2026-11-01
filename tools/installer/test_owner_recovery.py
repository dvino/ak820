"""Offline fake-device tests for owned check-device and recovery references."""
import contextlib
import io
import json
import unittest
from unittest.mock import Mock, patch

import ak820 as app
import test_installer as fixtures


class OwnerRecoveryTests(fixtures.BaseCase):
    def setUp(self):
        super().setUp()
        self.stock = (app.BUNDLE / 'reference/stock-full.bin').read_bytes()
        self.refs = self.root / 'owner'; self.refs.mkdir()

    def session(self, folder, backup):
        folder.mkdir()
        recovery = backup[app.packer.APP_START:app.packer.APP_END]
        (folder / 'before-full-rom.bin').write_bytes(backup)
        (folder / 'restore-native.bin').write_bytes(recovery)
        (folder / 'images.json').write_text(json.dumps({
            'backup_sha256': app.sha(backup),
            'images': {'restore-native.bin': {'size': len(recovery), 'sha256': app.sha(recovery)}}}))
        return folder

    def references(self, backup):
        (self.refs / 'stock-full.bin').write_bytes(backup)
        (self.refs / 'native-installed.bin').write_bytes(backup[app.packer.APP_START:app.packer.APP_END])

    def replace_session(self, target, backup):
        changed = bytearray(backup); changed[0xA200] ^= 1; changed = bytes(changed)
        app.packer.validate_native(changed)
        recovery = changed[app.packer.APP_START:app.packer.APP_END]
        (target / 'before-full-rom.bin').write_bytes(changed)
        (target / 'restore-native.bin').write_bytes(recovery)
        path = target / 'images.json'; meta = json.loads(path.read_bytes())
        meta['backup_sha256'] = app.sha(changed)
        meta['images']['restore-native.bin']['sha256'] = app.sha(recovery)
        path.write_text(json.dumps(meta))
        _, checked, checked_backup = app.transport.session_image(target, 'restore')
        self.assertEqual((checked, checked_backup), (recovery, changed))

    def test_recovery_real_transport_variants_and_session_swap(self):
        patched = bytearray(self.stock)
        patched[app.packer.APP_START:app.packer.APP_END] = (app.BUNDLE / 'reference/native-installed.bin').read_bytes()
        for variant, backup in (('factory', self.stock), ('patched', bytes(patched))):
            for case in ('default', 'exact', 'reference_swap', 'reference_erase_swap', 'source_swap', 'destination_swap'):
                with self.subTest(variant=variant, case=case):
                    self.references(backup)
                    source = self.session(self.root / (variant + '-' + case + '-source'), backup)
                    folder = self.root / (variant + '-' + case + '-output'); folder.mkdir()
                    hid = fixtures.TransportTests.loader(self)
                    if case in ('source_swap', 'destination_swap', 'reference_erase_swap'):
                        original_device = hid.device
                        def device():
                            dev = original_device()
                            send = dev.send_feature_report
                            def send_with_swap(packet):
                                result = send(packet)
                                if packet[1:5] == b'\x01\xaa\x55\x00' and case == 'reference_erase_swap':
                                    (self.refs / 'stock-full.bin').write_bytes(b'replaced')
                                elif packet[1:5] == b'\x01\xaa\x55\x00':
                                    target = source if case == 'source_swap' else folder / 'recovery-session'
                                    changed = bytearray(backup); changed[0xA200] ^= 1
                                    changed = bytes(changed)
                                    app.packer.validate_native(changed)
                                    recovery = changed[app.packer.APP_START:app.packer.APP_END]
                                    (target / 'before-full-rom.bin').write_bytes(changed)
                                    (target / 'restore-native.bin').write_bytes(recovery)
                                    path = target / 'images.json'; meta = json.loads(path.read_bytes())
                                    meta['backup_sha256'] = app.sha(changed)
                                    meta['images']['restore-native.bin']['sha256'] = app.sha(recovery)
                                    path.write_text(json.dumps(meta))
                                    _, checked, checked_backup = app.transport.session_image(target, 'restore')
                                    self.assertEqual((checked, checked_backup), (recovery, changed))
                                return result
                            dev.send_feature_report = send_with_swap
                            return dev
                        hid.device = device
                    def consent(_log, plan, **_kwargs):
                        if case == 'reference_swap':
                            (self.refs / 'stock-full.bin').write_bytes(b'replaced')
                            (self.refs / 'native-installed.bin').write_bytes(b'replaced')
                        return {'image': 'restore', 'sha256': plan['sha256'], 'reset': False,
                                'erase': True, 'flash': True, 'restart': True}
                    class StopAfterFlash(Exception): pass
                    with patch.object(app, 'RECOVERY_REFERENCE', object()), \
                         patch.object(app, 'consent', side_effect=consent), \
                         patch.object(app.transport, 'hid_module', return_value=hid), \
                         patch.object(app.transport.time, 'sleep'), \
                         patch.object(app, 'wait_state', side_effect=StopAfterFlash()):
                        error = ValueError if case in ('source_swap', 'destination_swap', 'reference_swap', 'reference_erase_swap') else StopAfterFlash
                        with self.assertRaises(error):
                            app.recover(fixtures.Log(folder), hid, source,
                                        reference_dir=None if case == 'default' else self.refs)
                    if case in ('source_swap', 'destination_swap', 'reference_erase_swap'):
                        self.assertEqual(hid.commands, [1])
                    elif case == 'reference_swap':
                        self.assertEqual(hid.commands, [])
                    else:
                        self.assertEqual(hid.commands, [1, 2, 3, 4, 5])
                        recovery = backup[app.packer.APP_START:app.packer.APP_END]
                        blocks = len(recovery)//64
                        self.assertEqual(b''.join(packet[1:] for packet in hid.writes[3:3+blocks]), recovery)

    def test_oem_present_is_unverified_no_write_outcome(self):
        changed_settings = bytearray(self.stock); changed_settings[0xA200] ^= 1
        patched = bytearray(self.stock)
        patched[app.packer.APP_START:app.packer.APP_END] = (app.BUNDLE / 'reference/native-installed.bin').read_bytes()
        for name, other_rom in (('settings', bytes(changed_settings)), ('image', bytes(patched))):
            with self.subTest(name=name):
                app.packer.validate_native(other_rom)
                source = self.session(self.root / ('present-source-'+name), self.stock)
                folder = self.root / ('present-output-'+name); folder.mkdir()
                hid = fixtures.FakeHid([fixtures.descriptor('OEM_APP')]); log = fixtures.Log(folder)
                output = io.StringIO(); application = Mock(); application.rom.return_value = other_rom
                with contextlib.redirect_stdout(output), patch.object(app.transport, 'flash') as flash, \
                     patch.object(app.transport, 'Application', return_value=application):
                    result = app.recover(log, hid, source)
                self.assertEqual(result, 'oem_present_unverified')
                self.assertIn('not verified or restored', output.getvalue())
                self.assertNotIn('oem_recovery_verified', [event['event'] for event in log.events])
                self.assertEqual(log.events[-1]['event'], 'oem_present_recovery_unverified')
                flash.assert_not_called(); application.rom.assert_not_called()
                self.assertEqual(hid.writes, [])

    def test_real_cli_and_gui_report_oem_present_as_unverified(self):
        import gui
        source = self.session(self.root / 'entry-source', self.stock)
        folder = self.root / 'entry-log'; folder.mkdir()
        hid = fixtures.FakeHid([fixtures.descriptor('OEM_APP')])
        args = ['recover', '--session', str(source)]
        with patch.object(app, 'Log', side_effect=lambda *_: Mock(folder=folder)), \
             patch.object(app, 'hid_module', return_value=hid), \
             patch.object(app.transport, 'flash') as flash, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(app.main(args, interactive=True), app.OEM_PRESENT_UNVERIFIED_EXIT)
            controller = gui.Controller(language='en')
            self.assertTrue(controller.start(args)); controller.worker.join(timeout=5)
            self.assertFalse(controller.worker.is_alive())
            events = []
            while not controller.events.empty(): events.append(controller.events.get_nowait())
        self.assertIn(('finished', app.OEM_PRESENT_UNVERIFIED_EXIT), events)
        self.assertIn('not performed or verified', gui.finished_text(app.OEM_PRESENT_UNVERIFIED_EXIT, 'en'))
        self.assertIn('не выполнено и не проверено', gui.finished_text(app.OEM_PRESENT_UNVERIFIED_EXIT, 'ru'))
        self.assertNotIn('Finished', gui.finished_text(app.OEM_PRESENT_UNVERIFIED_EXIT, 'en'))
        flash.assert_not_called(); self.assertEqual(hid.writes, [])

    def test_recovery_postflash_verifies_retained_original(self):
        source = self.session(self.root / 'complete-source', self.stock)
        folder = self.root / 'complete-output'; folder.mkdir()
        hid = fixtures.TransportTests.loader(self)
        def consent(_log, plan, **_kwargs):
            return {'image': 'restore', 'sha256': plan['sha256'], 'reset': False,
                    'erase': True, 'flash': True, 'restart': True}
        with patch.object(app, 'RECOVERY_REFERENCE', object()), \
             patch.object(app, 'consent', side_effect=consent), \
             patch.object(app.transport, 'hid_module', return_value=hid), \
             patch.object(app.transport.time, 'sleep'), \
             patch.object(app, 'wait_state', return_value={'path': b'fake'}), \
             patch.object(app, 'keyboard_smoke', return_value=True), \
             patch.object(app, 'capture_native', return_value=self.stock), \
             patch.object(app.transport, 'verify_live', wraps=app.transport.verify_live) as verify:
            app.recover(fixtures.Log(folder), hid, source)
        self.assertEqual(verify.call_args.args[:4], (self.stock,
            self.stock[app.packer.APP_START:app.packer.APP_END], 'restore', self.stock))
        self.assertEqual(hid.commands, [1, 2, 3, 4, 5])

    def test_failed_typing_never_records_recovery_verified(self):
        source = self.session(self.root / 'typing-source', self.stock)
        folder = self.root / 'typing-output'; folder.mkdir()
        hid = fixtures.TransportTests.loader(self); log = fixtures.Log(folder)
        def consent(_log, plan, **_kwargs):
            return {'image': 'restore', 'sha256': plan['sha256'], 'reset': False,
                    'erase': True, 'flash': True, 'restart': True}
        with patch.object(app, 'consent', side_effect=consent), \
             patch.object(app.transport, 'hid_module', return_value=hid), \
             patch.object(app.transport.time, 'sleep'), \
             patch.object(app, 'wait_state', return_value={'path': b'fake'}), \
             patch.object(app, 'keyboard_smoke', return_value=False), \
             patch.object(app, 'capture_native', return_value=self.stock):
            with self.assertRaisesRegex(ValueError, 'typing check failed'):
                app.recover(log, hid, source)
        self.assertNotIn('oem_recovery_verified', [event['event'] for event in log.events])

    def test_late_recovery_session_substitution_blocks_success(self):
        for phase in ('flash', 'capture'):
            for location in ('source', 'destination', 'reference'):
                with self.subTest(phase=phase, location=location):
                    self.references(self.stock)
                    source = self.session(self.root / (phase + location + '-source'), self.stock)
                    folder = self.root / (phase + location + '-output'); folder.mkdir()
                    log = fixtures.Log(folder)
                    hid = fixtures.TransportTests.loader(self)
                    target = source if location == 'source' else folder / 'recovery-session'
                    def substitute():
                        if location == 'reference': (self.refs / 'stock-full.bin').write_bytes(b'changed')
                        else: self.replace_session(target, self.stock)
                    if phase == 'flash':
                        original_device = hid.device
                        def device():
                            dev = original_device(); send = dev.send_feature_report
                            def send_with_swap(packet):
                                result = send(packet)
                                if packet[1:5] == b'\x03\xaa\x55\x00':
                                    substitute()
                                return result
                            dev.send_feature_report = send_with_swap
                            return dev
                        hid.device = device
                    def capture(*_args, **_kwargs):
                        if phase == 'capture': substitute()
                        return self.stock
                    def consent(_log, plan, **_kwargs):
                        return {'image': 'restore', 'sha256': plan['sha256'], 'reset': False,
                                'erase': True, 'flash': True, 'restart': True}
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output), \
                         patch.object(app, 'consent', side_effect=consent), \
                         patch.object(app.transport, 'hid_module', return_value=hid), \
                         patch.object(app.transport.time, 'sleep'), \
                         patch.object(app, 'wait_state', return_value={'path': b'fake'}), \
                         patch.object(app, 'keyboard_smoke', return_value=True), \
                         patch.object(app, 'capture_native', side_effect=capture):
                        with self.assertRaises(ValueError):
                            app.recover(log, hid, source, reference_dir=self.refs)
                    self.assertIn(2, hid.commands)
                    self.assertNotIn('oem_recovery_verified', [event['event'] for event in log.events])
                    self.assertNotIn('OEM restored:', output.getvalue())

    def test_explicit_historical_pinned_pair_rejected_for_different_owner_backup(self):
        backup = bytearray(self.stock); backup[0xA200] ^= 1; backup = bytes(backup)
        app.packer.validate_native(backup)
        (self.refs / 'stock-full.bin').write_bytes(self.stock)
        (self.refs / 'native-installed.bin').write_bytes((app.BUNDLE / 'reference/native-installed.bin').read_bytes())
        with self.assertRaises(ValueError):
            app.operation_references(backup, self.refs)
        self.references(backup)
        self.assertEqual(app.operation_references(backup, self.refs),
                         (backup, backup[app.packer.APP_START:app.packer.APP_END]))

    def test_check_device_and_recover_reject_explicit_mismatch_before_hid(self):
        source = self.session(self.root / 'source', self.stock)
        folder = self.root / 'prepared'; folder.mkdir()
        with patch.object(app, 'RECOVERY_REFERENCE', object()):
            installed, _ = app.prepare_trial(fixtures.Log(folder), self.stock, image='trial', context=self.context,
                reference_bytes=(self.stock, self.stock[app.packer.APP_START:app.packer.APP_END]))
        self.references(self.stock)
        (self.refs / 'native-installed.bin').write_bytes(b'bad')
        for mode, session in (('check-device', installed), ('recover', source)):
            with self.subTest(mode=mode):
                output = self.root / ('bad-' + mode); output.mkdir()
                args = [mode, '--session', str(session), '--reference-dir', str(self.refs)]
                if mode == 'check-device': args.append('--trial')
                with patch.object(app, 'RECOVERY_REFERENCE', object()), \
                     patch.object(app, 'Log', return_value=Mock(folder=output)), \
                     patch.object(app, 'release_context', return_value=self.context), \
                     patch.object(app, 'hid_module', side_effect=AssertionError('HID forbidden')) as hid:
                    self.assertEqual(app.main(args, interactive=True), 1)
                    hid.assert_not_called()
                self.assertFalse((output / 'recovery-session').exists())

    def test_check_device_real_diagnostics_and_late_session_substitution(self):
        files = dict(self.context.snapshot.files)
        ihx = files['firmware/application.ihx']; mapfile = files['firmware/application.map']
        files['reports/build-report.json'] = json.dumps({
            'code_window': [app.packer.CODE_START, app.packer.CODE_END],
            'artifacts': [{'path': 'application.ihx', 'sha256': app.sha(ihx)},
                          {'path': 'application.map', 'sha256': app.sha(mapfile)}]}).encode()
        manifest = {'files': {name: {'sha256': app.sha(data)} for name, data in files.items()}}
        snapshot = app.ReleaseSnapshot(json.dumps(manifest).encode(), files, {}, None)
        context = app.ReleaseContext('legacy', self.context.bundle, app.APPROVAL, manifest, snapshot=snapshot)
        for case in ('success', 'late_substitute', 'late_reference', 'late_release', 'typing_failed'):
            with self.subTest(case=case):
                self.references(self.stock)
                release_marker = self.root / ('release-marker-' + case); release_marker.write_text('approved')
                folder = self.root / ('real-' + case); folder.mkdir()
                session, _ = app.prepare_trial(fixtures.Log(folder), self.stock, image='trial', context=context,
                    reference_bytes=(self.stock, self.stock[app.packer.APP_START:app.packer.APP_END]))
                _, payload, _ = app.transport.session_image(session, 'trial')
                rom = (self.stock[:0x27C0] + bytes(0x40) + payload + self.stock[app.packer.APP_END:])
                output = self.root / ('real-output-' + case); output.mkdir()
                log = Mock(folder=output)
                test = self
                class FakeApplication:
                    native = False
                    def raw(self, packet):
                        if packet[:2] == b'\xfd\x01':
                            if case == 'late_substitute': test.replace_session(session, test.stock)
                            if case == 'late_reference': (test.refs / 'stock-full.bin').write_bytes(b'changed')
                            if case == 'late_release': release_marker.write_text('changed')
                            return b'\xfd\x01\x01\xa8' + bytes(28)
                        test.assertEqual(packet[:2], b'\xfd\x00')
                        address = int.from_bytes(packet[2:4], 'big'); size = packet[4]
                        return packet[:5] + rom[address:address+size] + bytes(27-size)
                    def close(self): pass
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout), \
                     patch.object(app, 'Log', return_value=log), \
                     patch.object(app, 'release_context', return_value=context), \
                     patch.object(app, 'load_release', side_effect=lambda **_k: context.manifest if release_marker.read_text() == 'approved' else (_ for _ in ()).throw(ValueError('release changed'))), \
                     patch.object(app, 'hid_module', return_value=Mock()), \
                     patch.object(app, 'require_state', return_value={'path': b'fake'}), \
                     patch.object(app, 'boot_status'), patch.object(app, 'keyboard_smoke', return_value=case != 'typing_failed'), \
                     patch.object(app.transport, 'Application', return_value=FakeApplication()), \
                     patch.object(app.diagnostic, 'capture', wraps=app.diagnostic.capture) as capture, \
                     patch.object(app.transport, 'verify_live', wraps=app.transport.verify_live) as verify:
                    status = app.main(['check-device', '--session', str(session), '--trial', '--reference-dir', str(self.refs)], interactive=True)
                capture.assert_called_once()
                verify.assert_called_once()
                self.assertEqual(verify.call_args.args[:4], (rom, payload, 'trial', self.stock))
                self.assertEqual((output / 'code-readback' / 'rom.bin').read_bytes(), rom)
                events = [call.args[0] for call in log.record.call_args_list]
                if case == 'success':
                    self.assertEqual(status, 0)
                    self.assertIn('application_readback_verified', events)
                    self.assertIn('Typing, CODE', stdout.getvalue())
                else:
                    self.assertEqual(status, 1)
                    self.assertNotIn('application_readback_verified', events)
                    self.assertNotIn('Typing, CODE', stdout.getvalue())
                    error = (output / 'error.txt').read_text()
                    self.assertIn({'late_substitute': 'Verification session changed',
                                   'late_reference': 'OEM references', 'late_release': 'release changed',
                                   'typing_failed': 'Typing check failed'}[case], error)

    def test_check_device_uses_original_session_and_detects_substitution(self):
        folder = self.root / 'prepared-check'; folder.mkdir()
        with patch.object(app, 'RECOVERY_REFERENCE', object()):
            session, _ = app.prepare_trial(fixtures.Log(folder), self.stock, image='trial', context=self.context,
                reference_bytes=(self.stock, self.stock[app.packer.APP_START:app.packer.APP_END]))
        initial = app.transport.session_image(session, 'trial')
        self.references(self.stock)
        for case in ('default', 'exact', 'substitute'):
            with self.subTest(case=case):
                output = self.root / ('check-' + case); output.mkdir()
                args = ['check-device', '--session', str(session), '--trial']
                if case != 'default': args += ['--reference-dir', str(self.refs)]
                def selected(*_args, **_kwargs):
                    if case == 'substitute':
                        backup = bytearray(self.stock); backup[0xA200] ^= 1; backup = bytes(backup)
                        recovery = backup[app.packer.APP_START:app.packer.APP_END]
                        (session / 'before-full-rom.bin').write_bytes(backup)
                        (session / 'restore-native.bin').write_bytes(recovery)
                        path = session / 'images.json'; meta = json.loads(path.read_bytes())
                        meta['backup_sha256'] = app.sha(backup)
                        meta['images']['restore-native.bin']['sha256'] = app.sha(recovery)
                        path.write_text(json.dumps(meta))
                    return {'path': b'fake'}
                with patch.object(app, 'RECOVERY_REFERENCE', object()), \
                     patch.object(app, 'Log', return_value=Mock(folder=output)), \
                     patch.object(app, 'release_context', return_value=self.context), \
                     patch.object(app, 'load_release', return_value=self.context.manifest), \
                     patch.object(app, 'hid_module', return_value=Mock()), \
                     patch.object(app, 'require_state', side_effect=selected), \
                     patch.object(app, 'boot_status'), patch.object(app, 'keyboard_smoke', return_value=True), \
                     patch.object(app.diagnostic, 'diagnostic_build_bytes', return_value={}), \
                     patch.object(app.diagnostic, 'capture', side_effect=AssertionError('stop before device capture')) as capture:
                    self.assertEqual(app.main(args, interactive=True), 1)
                    if case == 'substitute':
                        capture.assert_not_called()
                        self.assertIn('Verification session changed', (output / 'error.txt').read_text())
                    else:
                        capture.assert_called_once()
                        self.assertEqual(capture.call_args.kwargs['expected'], initial[1])


if __name__ == '__main__':
    unittest.main()
