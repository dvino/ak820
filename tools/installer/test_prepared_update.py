"""Offline RC6 repair admission and failure-stop tests; no HID is opened."""
import contextlib
import io
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

import ak820 as app


class PreparedUpdateTests(unittest.TestCase):
    def run_update(self, failure=None):
        with tempfile.TemporaryDirectory() as directory, contextlib.ExitStack() as stack:
            root = Path(directory)
            (root / 'stock-full.bin').write_bytes(bytes(65536))
            (root / 'native-installed.bin').write_bytes(b'fixture')
            source = root / 'source'
            source.mkdir()
            payload = bytes(app.packer.APP_END-app.packer.APP_START)
            for name in ('images.json', 'before-full-rom.bin', 'restore-native.bin', 'ak820-vial-permanent.bin'):
                (source / name).write_bytes(b'fixture')
            release = {'files': {'firmware/application.ihx': {'sha256': 'ihx'},
                                 'firmware/application.map': {'sha256': 'map'}}}
            manifest = {'ihx_sha256': 'ihx', 'map_sha256': 'map'}
            events = []
            cancel_event = threading.Event()
            def capture(output, **kwargs):
                events.append('capture')
                output.mkdir()
                (output / 'rom.bin').write_bytes(bytes(65536))
                return {'completed': True, 'nvm_and_journal_stable_on_second_read': True,
                        'status': {'storage_failed': failure == 'storage'}}
            device = Mock()
            device.vial_unlock_status.side_effect = [(0,0), (0,1), (0,1,30), (1,0,0), (1,0)]
            def unlock(command):
                events.append('lock' if command == 8 else 'unlock-start')
                if failure == 'decline' and command == 6:
                    raise ValueError('unlock rejected')
            device.vial_unlock_command.side_effect = unlock
            device.enter_vial_loader.side_effect = lambda: events.append('bootloader')
            if failure == 'stale-unlocked':
                device.vial_unlock_status.side_effect = [(1,0)]
            elif failure == 'malformed':
                device.vial_unlock_status.side_effect = ValueError('Malformed status')
            elif failure == 'boot-rejected':
                device.enter_vial_loader.side_effect = ValueError('Boot command rejected')
            elif failure == 'unlock-cancel':
                def cancel_start(command):
                    unlock(command)
                    if command == 6:
                        cancel_event.set()
                device.vial_unlock_command.side_effect = cancel_start
            elif failure == 'unlock-timeout':
                device.vial_unlock_status.side_effect = [(0,0), (0,1)]
            def wait(*args, **kwargs):
                events.append('loader' if args[1] == 'LOADER' else 'application')
                if failure == 'loader':
                    raise TimeoutError('loader absent')
                if failure == 'cancel':
                    raise app.Cancelled('wait cancelled')
                return {'path': b'loader'}
            mocks = {}
            options = {
                'RECOVERY_REFERENCE': root,
                'CANCEL_EVENT': cancel_event,
                'load_release': Mock(return_value=release),
                'capture_references': Mock(), 'require_state': Mock(return_value={'path': b'app'}),
                'confirm': Mock(side_effect=AssertionError('update must not prompt')), 'boot_status': Mock(),
                'wait_state': Mock(side_effect=wait),
                'keyboard_smoke': Mock(side_effect=AssertionError('physical input must not be requested')),
            }
            for name, value in options.items():
                mocks[name] = stack.enter_context(patch.object(app, name, value))
            stack.enter_context(patch.object(app.packer, 'validate_native'))
            stack.enter_context(patch.object(app.transport, 'validate_prepared_update', return_value=(manifest, payload, bytes(65536))))
            stack.enter_context(patch.object(app.transport, 'plan', return_value={'sha256': app.sha(payload)}))
            stack.enter_context(patch.object(app.transport, 'Application', return_value=device))
            stack.enter_context(patch.object(app.time, 'sleep'))
            if failure == 'unlock-timeout':
                stack.enter_context(patch.object(app.time, 'monotonic', side_effect=[0,121]))
            def fake_flash(*args, **kwargs):
                if failure == 'late-cancel':
                    cancel_event.set()
                kwargs['phase_guard']('erase_and_flash', image='permanent', sha256=app.sha(payload), loader_path=b'loader')
                events.append('flash')
            flash = stack.enter_context(patch.object(app.transport, 'flash', side_effect=fake_flash))
            stack.enter_context(patch.object(app.transport, 'verify_live'))
            stack.enter_context(patch.object(app.diagnostic, 'diagnostic_build', return_value={1: 2}))
            stack.enter_context(patch.object(app.diagnostic, 'capture', side_effect=capture))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            error = None
            try:
                app.update_prepared(Mock(folder=root), Mock(), source)
            except (app.Cancelled, TimeoutError, ValueError) as caught:
                error = caught
            self.assertTrue((root / 'before-update-readback' / 'rom.bin').is_file())
            mocks['keyboard_smoke'].assert_not_called()
            return events, flash.call_count, error

    def test_cancel_inside_transport_stops_before_erase(self):
        events, calls, error = self.run_update('late-cancel')
        self.assertEqual(calls, 1)  # Transport entered, destructive phase denied.
        self.assertIsInstance(error, app.Cancelled)
        self.assertNotIn('flash', events)

    def test_physical_update_order_and_no_typed_prompt(self):
        events, count, error = self.run_update()
        self.assertIsNone(error)
        self.assertEqual(events, ['capture', 'lock', 'unlock-start', 'bootloader', 'loader', 'flash', 'application', 'capture'])
        self.assertEqual(count, 1)

    def test_declined_consent_or_missing_loader_never_flashes(self):
        for failure in ('decline', 'loader', 'cancel', 'stale-unlocked', 'malformed',
                        'boot-rejected', 'unlock-cancel', 'unlock-timeout'):
            with self.subTest(failure=failure):
                _, count, error = self.run_update(failure)
                self.assertIsNotNone(error)
                self.assertEqual(count, 0)

    def test_wire_helpers_reject_malformed_replies_without_retry(self):
        device = object.__new__(app.transport.Application)
        device.raw = Mock(return_value=bytes((2,0))+bytes(30))
        with self.assertRaisesRegex(ValueError, 'Malformed'):
            device.vial_unlock_status()
        device.raw.assert_called_once()
        device.raw = Mock(return_value=bytes((1,0,4))+bytes(29))
        with self.assertRaisesRegex(ValueError, 'counter'):
            device.vial_unlock_status(poll=True)
        device.raw.assert_called_once()
        device.raw = Mock(return_value=bytes(32))
        with self.assertRaisesRegex(ValueError, 'rejected'):
            device.enter_vial_loader()
        device.raw.assert_called_once()

    def test_wire_helpers_accept_exact_supported_protocol(self):
        device = object.__new__(app.transport.Application)
        device.raw = Mock(return_value=bytes((0,0,0,0,0,5))+bytes((255,))*26)
        self.assertEqual(device.vial_unlock_status(), (0,0))
        device.raw = Mock(side_effect=lambda request: request)
        device.vial_unlock_command(8)
        device.vial_unlock_command(6)
        device.enter_vial_loader()
        self.assertEqual([call.args[0][:2] for call in device.raw.call_args_list],
                         [b'\xfe\x08', b'\xfe\x06', b'\x0b\x00'])

    def test_cancelled_wait_never_enumerates_or_returns_loader(self):
        cancelled = threading.Event()
        cancelled.set()
        with patch.object(app, 'inspect') as inspect:
            with self.assertRaises(app.Cancelled):
                app.wait_state(Mock(), 'LOADER', seconds=120, cancel_event=cancelled)
            inspect.assert_not_called()

    def test_wait_cancel_during_enumeration_stops_before_next_poll(self):
        cancelled = threading.Event()
        def enumerate_cancel(hid):
            cancelled.set()
            return 'VIAL_APP', {}, []
        with patch.object(app, 'inspect', side_effect=enumerate_cancel) as inspect, patch.object(app.time, 'sleep'):
            with self.assertRaises(app.Cancelled):
                app.wait_state(Mock(), 'LOADER', seconds=120, cancel_event=cancelled)
            self.assertEqual(inspect.call_count, 1)

    def test_main_restores_callback_and_cancellation_globals_after_failure(self):
        previous_progress, previous_cancel = Mock(), threading.Event()
        with tempfile.TemporaryDirectory() as directory, patch.object(app, 'RUNS', Path(directory)), \
             patch.object(app, 'PROGRESS', previous_progress), patch.object(app, 'CANCEL_EVENT', previous_cancel), \
             patch.object(app, 'load_release', side_effect=ValueError('offline failure')), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(app.main(['verify'], progress=Mock(), cancel_event=threading.Event()), 1)
            self.assertIs(app.PROGRESS, previous_progress)
            self.assertIs(app.CANCEL_EVENT, previous_cancel)

    def test_postflash_storage_fault_stops_without_second_flash(self):
        _, count, error = self.run_update('storage')
        self.assertIsInstance(error, ValueError)
        self.assertEqual(count, 1)

    def test_admission_rejects_unknown_image_before_snapshot_read(self):
        with patch.object(app.transport, 'session_image', return_value=({}, b'wrong', b'wrong')):
            with self.assertRaisesRegex(ValueError, 'exact reviewed candidate'):
                app.transport.validate_prepared_update(Path('unused'), Path('absent'))

    def test_snapshot_pin_and_durable_regions_are_both_required(self):
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / 'rom.bin'
            backup = bytes(65536)
            current = bytes(65536)
            payload = bytes(app.packer.APP_END-app.packer.APP_START)
            manifest = {'ihx_sha256': 'ihx', 'map_sha256': 'map'}
            pins = dict(manifest, payload=app.sha(payload), backup=app.sha(backup), snapshot=app.sha(current))
            snapshot.write_bytes(current)
            with patch.object(app.transport, 'UPDATE_PINS', pins), \
                 patch.object(app.transport, 'session_image', return_value=(manifest, payload, backup)):
                app.transport.validate_prepared_update(Path(directory), snapshot)
                changed = bytearray(current)
                changed[app.packer.NVM_START] = 1
                snapshot.write_bytes(changed)
                with self.assertRaisesRegex(ValueError, 'fault snapshot'):
                    app.transport.validate_prepared_update(Path(directory), snapshot)
                pins['snapshot'] = app.sha(changed)
                with self.assertRaisesRegex(ValueError, 'durable settings'):
                    app.transport.validate_prepared_update(Path(directory), snapshot)

    def test_prepared_transport_cannot_request_reset_or_omit_guard(self):
        with patch.object(app.transport, 'session_image', return_value=({}, b'', b'')), \
             patch.object(app.transport, 'validate_native'), \
             patch.object(Path, 'read_bytes', return_value=b''), \
             patch.object(app.transport, 'hid_module') as hid:
            for options in ({'enter_loader': True, 'phase_guard': Mock(), 'loader_descriptor': {}},
                            {'enter_loader': False, 'phase_guard': None, 'loader_descriptor': {}}):
                with self.subTest(options=options), self.assertRaisesRegex(ValueError, 'explicitly authorized loader'):
                    app.transport.flash(Path('.'), 'permanent', accept_hardware_check=False,
                                        prepared_update_snapshot=Path('snapshot'), **options)
            hid.assert_not_called()

    def test_wrong_session_stops_main_before_hid(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(app, 'RUNS', Path(directory)), \
             patch.object(app, 'load_release'), patch.object(app.transport, 'validate_prepared_update',
                                                          side_effect=ValueError('wrong session')), \
             patch.object(app, 'hid_module') as hid, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(app.main(['update-prepared', '--session', 'unknown'], interactive=True), 1)
            hid.assert_not_called()

    def test_unstable_snapshot_stops_before_consent_or_flash(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Mock(folder=Path(directory))
            release = {'files': {'firmware/application.ihx': {'sha256': 'ihx'},
                                 'firmware/application.map': {'sha256': 'map'}}}
            manifest = {'ihx_sha256': 'ihx', 'map_sha256': 'map'}
            with patch.object(app, 'load_release', return_value=release), \
                 patch.object(app, 'RECOVERY_REFERENCE', Path(directory)), \
                 patch.object(app.transport, 'validate_prepared_update', return_value=(manifest, b'', b'')), \
                 patch.object(app, 'capture_references'), patch.object(app.packer, 'validate_native'), \
                 patch.object(Path, 'read_bytes', return_value=b''), patch.object(app, 'require_state'), \
                 patch.object(app.diagnostic, 'capture', return_value={'completed': True,
                             'nvm_and_journal_stable_on_second_read': False}), \
                 patch.object(app, 'confirm') as consent, patch.object(app.transport, 'flash') as flash:
                with self.assertRaisesRegex(ValueError, 'journal changed'):
                    app.update_prepared(log, Mock(), Path('session'))
                consent.assert_not_called()
                flash.assert_not_called()


if __name__ == '__main__':
    unittest.main()
