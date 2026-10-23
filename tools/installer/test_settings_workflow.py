"""Offline workflow stop conditions, without a USB device."""
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import settings_workflow as workflow


class WorkflowTests(unittest.TestCase):
    def host(self):
        class Cancelled(Exception):
            pass
        def require(condition, message):
            if not condition:
                raise ValueError(message)
        return SimpleNamespace(CANCEL_EVENT=None, Cancelled=Cancelled, require=require,
                               PROGRESS=None, transport=Mock(), require_state=Mock())

    def test_update_and_restore_require_distinct_fresh_unlock_sequences(self):
        host = self.host()
        host.PROGRESS = Mock()
        app = host.transport.Application.return_value
        app.vial_unlock_status.side_effect = [(0, 0), (0, 1), (1, 0, 0)] * 2
        log = Mock()
        with contextlib.redirect_stdout(io.StringIO()):
            workflow.physical_unlock(host, log, Mock(), {'path': b'app'}, 'a'*64, purpose='update')
            workflow.physical_unlock(host, log, Mock(), {'path': b'app'}, 'a'*64, purpose='restore')
        self.assertEqual([call.args[0] for call in app.vial_unlock_command.call_args_list], [8, 6, 8, 6])
        self.assertEqual([call.args[0] for call in host.PROGRESS.call_args_list],
                         ['unlock_wait', 'restore_unlock_wait'])
        self.assertEqual([call.args[1]['purpose'] for call in host.PROGRESS.call_args_list],
                         ['update', 'restore'])
        app.enter_vial_loader.assert_not_called()

    def test_cancel_before_unlock_sends_no_unlock_packet(self):
        host = self.host()
        host.CANCEL_EVENT = Mock()
        host.CANCEL_EVENT.is_set.return_value = True
        with self.assertRaises(host.Cancelled):
            workflow.physical_unlock(host, Mock(), Mock(), {'path': b'app'}, 'a'*64)
        app = host.transport.Application.return_value
        app.vial_unlock_command.assert_not_called()
        app.enter_vial_loader.assert_not_called()
        app.close.assert_called_once()

    def test_unlock_failure_stops_without_retry_reset_or_cleanup_write(self):
        host = self.host()
        app = host.transport.Application.return_value
        app.vial_unlock_status.return_value = (1, 0)
        with self.assertRaisesRegex(ValueError, 'Fresh Vial lock'):
            workflow.physical_unlock(host, Mock(), Mock(), {'path': b'app'}, 'a'*64)
        self.assertEqual(app.vial_unlock_command.call_args_list[0].args, (8,))
        self.assertEqual(app.vial_unlock_command.call_count, 1)
        app.enter_vial_loader.assert_not_called()
        app.close.assert_called_once()

    def test_coherently_replaced_backup_stops_even_when_validation_passes(self):
        host = self.host()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path/'manifest.json').write_text('old')
            pinned = workflow.fingerprint(path)
            (path/'manifest.json').write_text('new')
            with patch.object(workflow.settings, 'validate_backup', return_value={}):
                with self.assertRaisesRegex(ValueError, 'changed'):
                    workflow.check_backup(host, path, pinned, {}, {})

    def test_failed_backup_always_closes_api(self):
        host = self.host()
        api = Mock()
        with patch.object(workflow, 'open_api', return_value=api), \
             patch.object(workflow.settings, 'export_settings', side_effect=TimeoutError('read failed')):
            with self.assertRaises(TimeoutError):
                workflow.backup(host, Mock(), Mock(), {'profile': {}}, Path('unused'))
        api.close.assert_called_once()
        host.transport.flash.assert_not_called()

    def test_update_restore_blocker_precedes_unlock_and_flash(self):
        host = self.host()
        host.packer = SimpleNamespace(NVM_START=2, NVM_END=4, APP_START=0)
        context = {'profile': {'payload': b'1234'}}
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            with patch.object(workflow, 'backup', return_value={'path': output}), \
                 patch.object(workflow.settings, 'plan_restore', side_effect=ValueError('unsupported')), \
                 patch.object(workflow, 'physical_unlock') as unlock:
                with self.assertRaisesRegex(ValueError, 'unsupported'):
                    workflow.update(host, Mock(), Mock(), context, output)
                unlock.assert_not_called()
                host.transport.flash.assert_not_called()

    def test_offline_reconstruction_failure_precedes_any_usb_open(self):
        host = self.host()
        host.load_release = Mock(side_effect=ValueError('approval'))
        with self.assertRaises(ValueError):
            workflow.prepare(host, Mock(), Path('unused'))
        host.transport.Application.assert_not_called()


import contextlib
import io
import multiprocessing
import test_installer as fixtures


def _run_gui_scenario_child(test_method_name, operation, failure, result_queue):
    """Run the complete mocked backend scenario in a killable child process."""
    try:
        test_case = EndToEndWorkflowTests(test_method_name)
        result_queue.put((True, test_case.run_scenario(
            gui=True, operation=operation, failure=failure, _isolated_child=True)))
    except BaseException as error:
        result_queue.put((False, (type(error).__name__, str(error))))


def _hang_child():
    import time
    while True:
        time.sleep(1)


def _stop_child(process, timeout):
    process.join(timeout)
    timed_out = process.is_alive()
    if timed_out:
        process.terminate()
        process.join(5)
    if process.is_alive():
        process.kill()
        process.join()
    return timed_out, not process.is_alive()


def _test_case_id_child(test_method_name, result_queue):
    result_queue.put(EndToEndWorkflowTests(test_method_name).id())


def _process_context():
    methods = multiprocessing.get_all_start_methods()
    return multiprocessing.get_context('fork' if 'fork' in methods else 'spawn')


class HostUpdateTransportTests(fixtures.BaseCase):
    def prepare_host_update(self):
        import ak820 as app
        with contextlib.redirect_stdout(io.StringIO()):
            session, plan = app.prepare_trial(self.log, app.check_original())
        return session, {'payload_sha256': plan['sha256'],
                         'backup_sha256': app.sha(app.check_original())}

    def test_host_update_gate_requires_exact_hashes_guard_and_selected_loader(self):
        import ak820 as app
        session, snapshot = self.prepare_host_update()
        for changed in ({'phase_guard': None}, {'loader_descriptor': None},
                        {'enter_loader': True}, {'native_install': True},
                        {'host_update_snapshot': {**snapshot, 'payload_sha256': 'bad'}}):
            options = dict(enter_loader=False, phase_guard=Mock(),
                           loader_descriptor=fixtures.descriptor('LOADER'),
                           host_update_snapshot=snapshot)
            options.update(changed)
            with patch.object(app.transport, 'hid_module') as hid:
                with self.assertRaises(ValueError):
                    app.transport.flash(session, 'permanent', accept_hardware_check=False,
                                        reference_dir=app.RECOVERY_REFERENCE, **options)
                hid.assert_not_called()

    def test_host_update_erase_guard_failure_sends_only_loader_identity(self):
        import ak820 as app
        session, snapshot = self.prepare_host_update()
        hid = fixtures.TransportTests.loader(self)
        def guard(phase, **_fields):
            self.assertEqual(phase, 'erase_and_flash')
            raise RuntimeError('cancelled before erase')
        with patch.object(app.transport, 'hid_module', return_value=hid), \
             patch.object(app.transport.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, 'before erase'):
                app.transport.flash(session, 'permanent', False, False,
                                    reference_dir=app.RECOVERY_REFERENCE,
                                    loader_descriptor=fixtures.descriptor('LOADER'),
                                    host_update_snapshot=snapshot, phase_guard=guard)
        self.assertEqual(hid.commands, [1])
        self.assertTrue(hid.closed)

    def test_host_update_reuses_loader_once(self):
        import ak820 as app
        session, snapshot = self.prepare_host_update()
        hid = fixtures.TransportTests.loader(self)
        phases = []
        with patch.object(app.transport, 'hid_module', return_value=hid), \
             patch.object(app.transport.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
            app.transport.flash(session, 'permanent', False, False,
                                reference_dir=app.RECOVERY_REFERENCE,
                                loader_descriptor=fixtures.descriptor('LOADER'),
                                host_update_snapshot=snapshot,
                                phase_guard=lambda phase, **_fields: phases.append(phase))
        self.assertEqual(hid.commands, [1, 2, 3, 4, 5])
        self.assertEqual(phases, ['erase_and_flash', 'restart'])


class EndToEndWorkflowTests(unittest.TestCase):
    def test_gui_timeout_stops_and_joins_child(self):
        process = multiprocessing.get_context('spawn').Process(target=_hang_child)
        process.start()
        timed_out, stopped = _stop_child(process, 0.05)
        self.assertTrue(timed_out)
        self.assertTrue(stopped)
        self.assertFalse(process.is_alive())
        process.close()

    def test_spawn_can_transfer_test_case_to_scenario_worker(self):
        context = multiprocessing.get_context('spawn')
        result_queue = context.Queue()
        process = context.Process(target=_test_case_id_child,
                                  args=(self._testMethodName, result_queue))
        try:
            process.start()
            timed_out, stopped = _stop_child(process, 10)
            self.assertFalse(timed_out)
            self.assertTrue(stopped)
            self.assertEqual(result_queue.get(timeout=2), self.id())
            self.assertEqual(process.exitcode, 0)
        finally:
            if process.pid is not None and process.is_alive():
                _stop_child(process, 0)
            result_queue.close()
            result_queue.join_thread()
            if not process.is_alive():
                process.close()

    def run_scenario(self, gui=False, operation='restore', failure=None,
                     _isolated_child=False):
        if gui and not _isolated_child:
            # A stuck GUI worker can outlive unittest fixture teardown. Run the
            # whole scenario in a forked process so timeout cleanup can kill
            # every thread and discard its inherited mocks safely.
            context = _process_context()
            result_queue = context.Queue()
            process = context.Process(target=_run_gui_scenario_child,
                                      args=(self._testMethodName, operation, failure, result_queue))
            try:
                process.start()
                timed_out, stopped = _stop_child(process, 90)
                if timed_out:
                    self.fail('GUI end-to-end scenario exceeded 90 seconds; child process was stopped and joined')
                if not stopped:
                    self.fail('GUI end-to-end child could not be stopped and joined')
                try:
                    succeeded, result = result_queue.get(timeout=2)
                except Exception as error:
                    self.fail(f'GUI end-to-end child exited without a result (exit={process.exitcode}): {error}')
            finally:
                if process.pid is not None and process.is_alive():
                    _stop_child(process, 0)
                exitcode = process.exitcode if process.pid is not None else None
                result_queue.close()
                result_queue.join_thread()
                if not process.is_alive():
                    process.close()
            if not succeeded:
                self.fail(f'GUI end-to-end child failed: {result[0]}: {result[1]}')
            self.assertEqual(exitcode, 0)
            return result
        import ak820 as app
        import gui as installer_gui
        import test_settings_backup as wire
        import threading
        with tempfile.TemporaryDirectory() as folder, contextlib.ExitStack() as stack:
            root = Path(folder)
            profile = wire.synthetic_profile()
            source_nvm = wire.SettingsTests.changed_nvm(None, b'ab\0'*16, off=True)
            raw = wire.WireDevice(profile, source_nvm)
            events = []
            def unlock_command(command):
                events.append(('unlock', command))
                raw.unlocked = False
                raw.unlock_active = command == 6
            def unlock_status(poll=False):
                if poll:
                    raw.unlocked, raw.unlock_active = True, False
                    return (1, 0, 0)
                return (int(raw.unlocked), int(raw.unlock_active))
            raw.vial_unlock_command = unlock_command
            raw.vial_unlock_status = unlock_status
            raw.enter_vial_loader = lambda: events.append(('loader', 1))
            context = {'profile': profile, 'native': profile['backup'], 'target': root/'target',
                       'plan': {'sha256': app.sha(profile['payload'])}, 'pins': {}}
            selected = {'path': b'wire-app'}
            progress = []
            stack.enter_context(patch.object(app, 'RUNS', root/'runs'))
            stack.enter_context(patch.object(app, 'RECOVERY_REFERENCE', root))
            stack.enter_context(patch.object(app, 'hid_module', return_value=Mock()))
            stack.enter_context(patch.object(app, 'require_state', return_value=selected))
            stack.enter_context(patch.object(app, 'wait_state', return_value=selected))
            stack.enter_context(patch.object(app, 'phase_guard', return_value=Mock()))
            stack.enter_context(patch.object(app, 'boot_status'))
            stack.enter_context(patch.object(app.transport, 'Application', return_value=raw))
            stack.enter_context(patch.object(workflow, 'prepare', return_value=context))
            stack.enter_context(patch.object(workflow, 'revalidate'))
            stack.enter_context(patch.object(workflow, 'recheck_pins'))
            stack.enter_context(patch('ak820_device_protocol.time.sleep'))
            def flash(*_args, **kwargs):
                kwargs['phase_guard']('erase_and_flash', image='permanent',
                                      sha256=context['plan']['sha256'], loader_path=b'wire-app')
                events.append(('flash', 1))
                raw.nvm = wire.base_nvm()
                raw.ram_rgb = bytearray(raw.nvm[24:32])
                raw.unlocked = False
                if failure == 'manifest':
                    at = wire.p.APP_END-1
                    raw.rom_patch[at] = profile['payload'][-1] ^ 1
                kwargs['phase_guard']('restart', image='permanent',
                                      sha256=context['plan']['sha256'], loader_path=b'wire-app')
            stack.enter_context(patch.object(app.transport, 'flash', side_effect=flash))
            def run(args):
                if gui:
                    controller = installer_gui.Controller(runner=app.main, language='en')
                    controller.start(args)
                    controller.worker.join()
                    status = None
                    while not controller.events.empty():
                        kind, value = controller.events.get_nowait()
                        if kind == 'finished':
                            status = value
                        elif kind == 'progress':
                            progress.append(value)
                    return status
                with patch.object(sys, 'stdin', Mock(isatty=Mock(return_value=True))), \
                     contextlib.redirect_stdout(io.StringIO()):
                    return app.main(args, progress=lambda stage, payload: progress.append((stage, payload)))
            saved = root/'source-settings'
            if operation == 'restore':
                self.assertEqual(run(['backup', '--session', str(root), '--output', str(saved)]), 0)
                self.assertEqual(raw.writes, [])
                raw.nvm = wire.base_nvm()
                raw.ram_rgb = bytearray(raw.nvm[24:32])
                self.assertEqual(run(['restore', '--session', str(root), '--backup', str(saved)]), 0)
                self.assertNotIn(('flash', 1), events)
            else:
                status = run(['update', '--session', str(root), '--backup-dir', str(saved)])
                if failure == 'manifest':
                    self.assertEqual(status, 1)
                    self.assertEqual([value for kind, value in events if kind == 'unlock'], [8, 6])
                    self.assertEqual(events.count(('flash', 1)), 1)
                    self.assertEqual(raw.writes, [])
                    self.assertTrue(saved.is_dir())
                    return [kind for kind, _ in progress]
                self.assertEqual(status, 0)
                self.assertEqual(events.count(('flash', 1)), 1)
                self.assertEqual(events.count(('loader', 1)), 1)
                self.assertEqual([value for kind, value in events if kind == 'unlock'], [8, 6, 8, 6])
            backup = wire.settings.validate_backup(saved, profile)
            actual = wire.settings.settings_from_nvm(bytes(raw.nvm), wire.settings.rgb_wire(raw.ram_rgb))
            self.assertEqual(actual, backup['settings'])
            self.assertTrue(raw.writes)
            return [kind for kind, _ in progress]

    def test_cli_and_gui_use_same_actual_backup_restore_backend(self):
        cli = self.run_scenario(gui=False)
        gui = self.run_scenario(gui=True)
        self.assertEqual(cli, gui)
        self.assertIn('restore_unlock_wait', cli)
        self.assertIn('restoring', cli)
        self.assertIn('complete', cli)

    def test_changed_manifest_config_hash_stops_before_restore_unlock(self):
        stages = self.run_scenario(operation='update', failure='manifest')
        self.assertNotIn('restore_unlock_wait', stages)

    def test_update_one_flash_then_second_unlock_and_real_typed_restore(self):
        stages = self.run_scenario(operation='update')
        self.assertLess(stages.index('unlock_wait'), stages.index('flashing'))
        self.assertLess(stages.index('flashing'), stages.index('restore_unlock_wait'))
        self.assertEqual(stages[-1], 'complete')


if __name__ == '__main__':
    unittest.main()
