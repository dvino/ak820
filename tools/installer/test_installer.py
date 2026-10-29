"""Offline safety/flow regressions. Every HID/device access is an explicit fake."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import struct
import tempfile
import types
import unittest
from unittest.mock import patch

import ak820 as app
from ak820_release_manifest import HOST_FILES, host_manifest


def descriptor(mode, path=b'device-one'):
    if mode == 'LOADER':
        return dict(vendor_id=0x0C45, product_id=0x7687, interface_number=1,
                    usage_page=12, usage=1, path=path)
    return dict(vendor_id=0x320F, product_id=0x505B, interface_number=1,
                usage_page=0xFF1C if mode == 'OEM_APP' else 0xFF60,
                usage=0x92 if mode == 'OEM_APP' else 0x61, path=path)


class FakeHid:
    def __init__(self, descriptors):
        self.descriptors = descriptors
        self.opens = []
        self.writes = []

    def enumerate(self, vid=0, pid=0):
        return [d for d in self.descriptors if not vid or (d['vendor_id'], d['product_id']) == (vid, pid)]

    def device(self):
        raise AssertionError('Unexpected device open in read-only enumeration test')


class Log:
    def __init__(self, folder):
        self.folder = folder
        self.events = []

    def record(self, event, **fields):
        self.events.append({'event': event, **fields})


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.log = Log(self.root)
        catalog_patch = patch.object(app, 'profile_catalog', return_value=None)
        catalog_patch.start()
        self.addCleanup(catalog_patch.stop)
        # Synthetic ROMs exercise validation/orchestration without redistributing
        # OEM bytes. Per-test hash patches identify only these generated fixtures;
        # they do not validate the production pinned hashes or hardware behavior.
        fixture = self.root / 'synthetic-bundle'
        reference = fixture / 'reference'
        reference.mkdir(parents=True)
        stock = bytearray((address * 17 + 23) % 256 for address in range(65536))
        stock[0x27C0:0x27C4] = bytes.fromhex('aa5533cc')
        stock[0xA000:0xD200] = bytes(0x3200)
        for slot in (*app.packer.PHYSICAL, 87, 111):
            stock[0xA100+slot*3:0xA100+slot*3+3] = bytes.fromhex('200004')
        native = bytearray(stock[app.packer.APP_START:app.packer.APP_END])
        native[0x3000-app.packer.APP_START] ^= 1
        native[0xD400-app.packer.APP_START] ^= 1
        native[0xD200-app.packer.APP_START:0xD380-app.packer.APP_START] = bytes(0x180)
        public = bytearray(native)
        public[0xA000-app.packer.APP_START:0xD380-app.packer.APP_START] = bytes(0x3380)
        (reference / 'stock-full.bin').write_bytes(stock)
        (reference / 'native-installed.bin').write_bytes(native)
        (fixture / 'firmware').mkdir()
        # The distributable linked application remains real; only OEM input is synthetic.
        for filename in ('application.ihx', 'application.map', 'application.mem'):
            shutil.copyfile(app.ROOT / 'releases' / app.RELEASE / 'firmware' / filename,
                            fixture / 'firmware' / filename)
        pins = {
            'PROTECTED_SHA': app.sha(stock[:0x27C0] + stock[app.packer.APP_END:]),
            'FACTORY_CODE_SHA': app.sha(stock[app.packer.APP_START:0xA000] + stock[0xD200:app.packer.APP_END]),
            'PATCHED_CODE_SHA': app.sha(native[:0xA000-app.packer.APP_START] + native[0xD380-app.packer.APP_START:]),
            'STOCK_SHA': app.sha(stock), 'NATIVE_SHA': app.sha(native),
            'NATIVE_PUBLIC_SHA': app.sha(public),
            'NATIVE_REFERENCE_HASHES': frozenset((app.sha(native), app.sha(public))),
        }
        for name, value in pins.items():
            patcher = patch.object(app.packer, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        for name, value in (('BUNDLE', fixture), ('RECOVERY_REFERENCE', reference),
                            ('BAD_IHX', app.BAD_IHX | {app.sha(b'known-bad-rc3-test-fixture')})):
            patcher = patch.object(app, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

        self.context = app.ReleaseContext('legacy', fixture, app.APPROVAL, {
            'files': {'firmware/application.ihx': {'sha256': app.sha((fixture/'firmware/application.ihx').read_bytes())}}})

        # Generated factory bytes form a synthetic ORIGINAL session so checks for
        # session integrity never depend on a machine's private evidence folder.
        reference = fixture / 'reference'
        backup = (reference / 'stock-full.bin').read_bytes()
        recovery = backup[app.packer.APP_START:app.packer.APP_END]
        original = self.root / 'synthetic-original-session'
        original.mkdir()
        (original / 'before-full-rom.bin').write_bytes(backup)
        (original / 'restore-native.bin').write_bytes(recovery)
        (original / 'images.json').write_text(json.dumps({
            'backup_sha256': app.sha(backup),
            'images': {'restore-native.bin': {'size': len(recovery), 'sha256': app.sha(recovery)}},
        }))
        for name, value in (
            ('ORIGINAL', original),
            ('EXPECTED_OEM', app.sha(backup)),
            ('EXPECTED_RESTORE', app.sha(recovery)),
        ):
            patcher = patch.object(app, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self):
        self.temp.cleanup()


class OfflineTests(BaseCase):
    def test_schema3_selected_context_prepares_trial_and_permanent_with_exact_schema(self):
        backup = (app.BUNDLE / 'reference/stock-full.bin').read_bytes()
        (app.BUNDLE / 'installer-release.json').write_text('synthetic approved manifest')
        context = app.ReleaseContext('main', app.BUNDLE, app.APPROVAL,
            self.context.manifest, nvm_schema=app.packer.EXTENSION_BUILD_ID)
        with contextlib.redirect_stdout(io.StringIO()):
            session, _ = app.prepare_trial(self.log, backup, context=context)
        for mode in ('trial', 'permanent'):
            manifest, payload, original = app.transport.session_image(
                session, mode, target_build_id=context.nvm_schema)
            self.assertEqual(original, backup)
            info = app.packer.verify_payload(payload, target_build_id=context.nvm_schema)
            self.assertEqual(info['build_id'], app.packer.EXTENSION_BUILD_ID)
            nvm = payload[app.packer.NVM_START-app.packer.APP_START:app.packer.NVM_END-app.packer.APP_START]
            app.packer.validate_nvm(nvm, app.packer.EXTENSION_BUILD_ID)
            self.assertEqual(nvm[37:40], app.packer.EXTENSION_BUILD_ID.to_bytes(3, 'little'))
            self.assertEqual(manifest['installer_release']['profile'], 'main')
            with self.assertRaises(ValueError):
                app.packer.verify_payload(payload)
        self.assertEqual((session / 'restore-native.bin').read_bytes(),
                         backup[app.packer.APP_START:app.packer.APP_END])


    def test_automatic_private_reference_uses_owner_backup_and_preserves_settings(self):
        backup = bytearray((app.RECOVERY_REFERENCE / 'stock-full.bin').read_bytes())
        backup[0xA050] ^= 1  # Owner-specific settings do not change code identity.
        backup = bytes(backup)
        with patch.object(app, 'RECOVERY_REFERENCE', None):
            folder = app.capture_references(self.log, backup)
            self.assertEqual((folder / 'stock-full.bin').read_bytes(), backup)
            self.assertEqual((folder / 'native-installed.bin').read_bytes(),
                             backup[app.packer.APP_START:app.packer.APP_END])
            app.packer.validate_native(backup, backup, (folder / 'native-installed.bin').read_bytes())

    def test_automatic_reference_rejects_modified_immutable_spans_before_output(self):
        backup = (app.RECOVERY_REFERENCE / 'stock-full.bin').read_bytes()
        for address in (0, 0x2800, 0xD200, 0xE650, 0xF000):
            modified = bytearray(backup)
            modified[address] ^= 1
            with self.subTest(address=hex(address)), patch.object(app, 'RECOVERY_REFERENCE', None):
                with self.assertRaises(ValueError):
                    app.capture_references(self.log, bytes(modified))
                self.assertFalse((self.root / 'private-oem-reference').exists())

    def test_mixed_factory_and_patched_code_is_rejected(self):
        stock = bytearray((app.RECOVERY_REFERENCE / 'stock-full.bin').read_bytes())
        native = (app.RECOVERY_REFERENCE / 'native-installed.bin').read_bytes()
        stock[0xD380:app.packer.APP_END] = native[0xD380-app.packer.APP_START:]
        with self.assertRaises(ValueError):
            app.packer.validate_native(bytes(stock))

    def test_explicit_missing_local_reference_fails_before_hid(self):
        with patch.object(app, 'RUNS', self.root / 'runs'), patch.object(app, 'load_release'), \
             patch.object(app, 'hid_module') as hid, contextlib.redirect_stdout(io.StringIO()):
            result = app.main(['install', '--reference-dir', str(self.root / 'missing')], interactive=True)
            self.assertEqual(result, 1)
            hid.assert_not_called()

    def test_public_reference_removes_all_settings_and_preserves_code(self):
        original = (app.RECOVERY_REFERENCE / 'native-installed.bin').read_bytes()
        public = app.packer.public_native_reference(original)
        start, end = 0xA000-app.packer.APP_START, 0xD380-app.packer.APP_START
        self.assertEqual(public[:start], original[:start])
        self.assertEqual(public[end:], original[end:])
        self.assertEqual(public[start:end], bytes(end-start))
        self.assertEqual(app.sha(public), app.packer.NATIVE_PUBLIC_SHA)
        self.assertEqual(app.packer.public_native_reference(public), public)
        app.packer.validate_native(app.check_original(),
            (app.RECOVERY_REFERENCE / 'stock-full.bin').read_bytes(), public)
        with self.assertRaisesRegex(ValueError, 'Unknown native reference'):
            app.packer.public_native_reference(bytes(len(public)))

    def test_factory_first_install_materializes_fn_and_keeps_exact_backup(self):
        backup = (app.BUNDLE / 'reference/stock-full.bin').read_bytes()
        app.packer.validate_native(backup, backup, (app.BUNDLE / 'reference/native-installed.bin').read_bytes())
        with contextlib.redirect_stdout(io.StringIO()):
            session, _ = app.prepare_trial(self.log, backup, context=self.context)
        manifest, image, actual_backup = app.transport.session_image(session, 'permanent')
        self.assertEqual(actual_backup, backup)
        self.assertEqual((session / 'restore-native.bin').read_bytes(), backup[app.packer.APP_START:app.packer.APP_END])
        self.assertEqual(manifest['migration']['native_variant'], 'factory OEM')
        data = app.packer.read_ihex(app.BUNDLE / 'firmware/application.ihx')
        symbols = app.packer.read_symbols(app.BUNDLE / 'firmware/application.map')
        keys = struct.unpack('<256H', app.packer.factory_keymaps(data, symbols))
        for slot in app.packer.PHYSICAL:
            address = app.packer.NVM_START-app.packer.APP_START + 0x40 + 256 + slot*2
            self.assertEqual(int.from_bytes(image[address:address+2], 'big'), keys[128+slot])
        unknown = bytearray(backup)
        unknown[0x5000] ^= 1
        with self.assertRaisesRegex(ValueError, 'Unsupported native'):
            app.packer.validate_native(bytes(unknown), backup, (app.BUNDLE / 'reference/native-installed.bin').read_bytes())

    def test_first_backup_preserves_partial_read_without_flash(self):
        native = unittest.mock.Mock(native=True)
        native.rom.side_effect = [bytes(1024), OSError('connection lost')]
        with patch.object(app.transport, 'Application', return_value=native), \
             patch.object(app.transport, 'flash') as flash, contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(OSError, 'connection lost'):
                app.capture_native(self.log, descriptor('OEM_APP'), references=app.BUNDLE / 'reference')
        self.assertEqual((self.root / 'native-prefix.bin').read_bytes(), bytes(1024))
        self.assertFalse((self.root / 'native-rom.bin').exists())
        native.close.assert_called_once()
        flash.assert_not_called()

    def test_first_factory_backup_is_complete_before_final_confirmation(self):
        backup = (app.BUNDLE / 'reference/stock-full.bin').read_bytes()
        native = unittest.mock.Mock(native=True)
        native.rom.side_effect = lambda start, size: backup[start:start+size]
        with patch.object(app, 'load_release', return_value={'install_modes': ['permanent', 'trial']}), \
             patch.object(app, 'inventory', return_value=('OEM_APP', descriptor('OEM_APP'))), \
             patch.object(app.transport, 'Application', return_value=native), \
             patch.object(app.transport, 'flash') as flash, patch('builtins.input', side_effect=['y', '']), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(app.Cancelled):
                app.install(self.log, FakeHid([]), context=self.context)
        self.assertEqual((self.root / 'native-rom.bin').read_bytes(), backup)
        self.assertEqual((self.root / 'permanent-session/before-full-rom.bin').read_bytes(), backup)
        flash.assert_not_called()

    def test_preparation_default_no_before_enumeration_or_backup(self):
        for answer in ('', 'n', 'N', 'no', 'yes'):
            with self.subTest(answer=answer), patch.object(app, 'load_release', return_value={
                    'install_modes': ['permanent', 'trial']}), patch.object(app, 'check_original'), \
                 patch.object(app, 'inventory') as inventory, patch.object(app, 'capture_native') as capture, \
                 patch.object(app.transport, 'flash') as flash, patch('builtins.input', return_value=answer), \
                 contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(app.Cancelled):
                    app.install(self.log, FakeHid([]), context=self.context)
                inventory.assert_not_called()
                capture.assert_not_called()
                flash.assert_not_called()

    def test_old_trial_approval_cannot_authorize_permanent(self):
        with patch.object(app, 'load_release', return_value={'trial_only': True}), \
             patch.object(app, 'inventory') as inventory, patch('builtins.input') as prompt:
            with self.assertRaisesRegex(ValueError, 'trial only'):
                app.install(self.log, FakeHid([]), context=self.context)
            inventory.assert_not_called()
            prompt.assert_not_called()

    def test_final_no_keeps_backup_and_never_flashes(self):
        for answer in ('', 'n', 'y', 'YES'):
            with self.subTest(answer=answer), patch.object(app, 'load_release', return_value={
                    'install_modes': ['permanent', 'trial']}), patch.object(app, 'check_original'), \
                 patch.object(app, 'inventory', return_value=('OEM_APP', descriptor('OEM_APP'))), \
                 patch.object(app, 'capture_native', return_value=b'personal backup') as capture, \
                 patch.object(app, 'prepare_trial', return_value=(self.root, {
                     'image': 'ak820-vial-permanent.bin', 'sha256': 'digest', 'size': 51136})) as prepare, \
                 patch.object(app.transport, 'flash') as flash, \
                 patch('builtins.input', side_effect=['y', answer]), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(app.Cancelled):
                    app.install(self.log, FakeHid([]), context=self.context)
                capture.assert_called_once()
                self.assertEqual(prepare.call_args.args[1], b'personal backup')
                flash.assert_not_called()

    def test_permanent_and_trial_bootstrap_and_personal_recovery(self):
        backup = app.check_original()
        with contextlib.redirect_stdout(io.StringIO()):
            session, plan = app.prepare_trial(self.log, backup, context=self.context)
        manifest, permanent, original = app.transport.session_image(session, 'permanent')
        _, trial, _ = app.transport.session_image(session, 'trial')
        _, restore, _ = app.transport.session_image(session, 'restore')
        self.assertEqual(plan['image'], 'ak820-vial-permanent.bin')
        self.assertEqual(original, backup)
        self.assertEqual(restore, backup[app.packer.APP_START:app.packer.APP_END])
        self.assertEqual(manifest['native_install_backup_sha256'], app.sha(backup))
        self.assertFalse(app.packer.verify_payload(permanent)['trial'])
        self.assertTrue(app.packer.verify_payload(trial)['trial'])
        self.assertNotEqual(permanent[:64], trial[:64])
        live = bytearray(backup)
        live[app.packer.APP_START:app.packer.APP_END] = permanent
        stock = (app.BUNDLE / 'reference/stock-full.bin').read_bytes()
        app.transport.verify_live(bytes(live), permanent, 'permanent', stock)
        live[0x27C0:0x2800] = bytes(64)
        with self.assertRaisesRegex(ValueError, 'marker'):
            app.transport.verify_live(bytes(live), permanent, 'permanent', stock)

    def test_repeated_setup_does_not_replace_running_venv_interpreter(self):
        local = self.root / 'venv'
        python = local / ('Scripts/python.exe' if app.os.name == 'nt' else 'bin/python')
        python.parent.mkdir(parents=True)
        python.write_bytes(b'existing interpreter must remain intact')
        with patch.object(app, 'VENV', local), \
             patch.object(app.venv, 'EnvBuilder', side_effect=PermissionError('python.exe is in use')), \
             patch.object(app.subprocess, 'run') as run, contextlib.redirect_stdout(io.StringIO()):
            app.setup()
        self.assertEqual(python.read_bytes(), b'existing interpreter must remain intact')
        commands = [call.args[0] for call in run.call_args_list]
        self.assertTrue(all(command[0] == str(python) for command in commands))
        self.assertTrue(any(command[1:3] == ['-m', 'ensurepip'] for command in commands))
        self.assertTrue(any(command[1:4] == ['-m', 'pip', 'install'] for command in commands))

    def test_linux_setup_builds_pinned_hidapi_from_source_with_hidraw_backend(self):
        local = self.root / 'linux-venv'
        python = local / 'bin/python'
        python.parent.mkdir(parents=True)
        python.write_bytes(b'existing interpreter')
        inherited = {'PATH': '/test/bin', 'KEEP_ME': 'yes'}
        with patch.object(app, 'VENV', local), patch.object(app.sys, 'platform', 'linux'), \
             patch.dict(app.os.environ, inherited, clear=True), patch.object(app.subprocess, 'run') as run, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            app.setup()
        pip_call = next(call for call in run.call_args_list if call.args[0][1:3] == ['-m', 'pip'])
        command = pip_call.args[0]
        self.assertEqual(command[:7], [str(python), '-m', 'pip', 'install', '--disable-pip-version-check',
                                           '--no-binary=hidapi', '--no-cache-dir'])
        self.assertEqual(command[7:9], ['--force-reinstall', '-r'])
        self.assertEqual(command[9], str(Path(app.__file__).with_name('requirements.txt')))
        self.assertEqual(pip_call.kwargs['env']['HIDAPI_WITH_HIDRAW'], '1')
        self.assertEqual(pip_call.kwargs['env']['HIDAPI_WITH_LIBUSB'], '0')
        self.assertEqual(pip_call.kwargs['env']['KEEP_ME'], 'yes')
        self.assertIn('libudev development files', output.getvalue())

    def test_windows_setup_keeps_wheel_install_flow(self):
        local = self.root / 'windows-venv'
        python = local / 'bin/python'
        python.parent.mkdir(parents=True)
        python.write_bytes(b'existing interpreter')
        with patch.object(app, 'VENV', local), patch.object(app.sys, 'platform', 'win32'), \
             patch.object(app.subprocess, 'run') as run, contextlib.redirect_stdout(io.StringIO()):
            app.setup()
        pip_call = next(call for call in run.call_args_list if call.args[0][1:3] == ['-m', 'pip'])
        self.assertEqual(pip_call.args[0], [str(python), '-m', 'pip', 'install', '--disable-pip-version-check',
                                               '-r', str(Path(app.__file__).with_name('requirements.txt'))])
        self.assertNotIn('env', pip_call.kwargs)

    def test_default_command_only_enumerates_no_device_or_feature(self):
        hid = FakeHid([descriptor('OEM_APP')])
        with patch.object(app, 'RUNS', self.root / 'runs'), patch.object(app, 'hid_module', return_value=hid), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(app.main([]), 0)
        self.assertEqual(hid.opens, [])
        self.assertEqual(hid.writes, [])
        self.assertEqual(len(list((self.root / 'runs').glob('*-logs.zip'))), 1)

    def test_selection_refuses_multiple_and_mixed_devices(self):
        for entries in ([descriptor('OEM_APP'), descriptor('VIAL_APP', b'two')],
                        [descriptor('LOADER'), descriptor('LOADER', b'two')],
                        [descriptor('VIAL_APP'), descriptor('LOADER')]):
            self.assertEqual(app.inspect(FakeHid(entries))[0], 'AMBIGUOUS')

    def test_second_unknown_target_interface_is_not_ignored(self):
        for mode in ('OEM_APP', 'VIAL_APP'):
            extra = descriptor(mode, b'unknown-second-device')
            extra.update(interface_number=2, usage_page=None, usage=None)
            self.assertEqual(app.inspect(FakeHid([descriptor(mode), extra]))[0], 'UNSUPPORTED_INTERFACE')

    def test_known_ancillary_collections_are_allowed(self):
        for mode in ('OEM_APP', 'VIAL_APP'):
            raw = descriptor(mode)
            keyboard = dict(raw, path=b'keyboard', interface_number=0, usage_page=1, usage=6)
            shared = dict(raw, path=b'shared', interface_number=1 if mode == 'OEM_APP' else 2,
                          usage_page=12, usage=1)
            self.assertEqual(app.inspect(FakeHid([raw, keyboard, shared]))[0], mode)
            self.assertEqual(app.inspect(FakeHid([raw, keyboard, dict(keyboard, path=b'other')]))[0], 'AMBIGUOUS')

    def test_wrong_control_interface_is_refused(self):
        self.assertEqual(app.inspect(FakeHid([dict(descriptor('VIAL_APP'), interface_number=2)]))[0],
                         'UNSUPPORTED_INTERFACE')

    def test_identity_changes_abort_phase_before_erase(self):
        authorization = {'image': 'trial', 'sha256': 'digest', 'reset': True, 'erase': True,
                         'flash': True, 'restart': True}
        hid = FakeHid([descriptor('LOADER', b'other')])
        guard = app.phase_guard(self.log, hid, authorization, descriptor('OEM_APP'))
        with self.assertRaisesRegex(ValueError, 'changed'):
            guard('erase_and_flash', image='trial', sha256='digest', loader_path=b'original')
        with self.assertRaisesRegex(ValueError, 'plan'):
            guard('reset_to_loader', image='trial', sha256='modified')

    def test_all_consents_precede_any_mutation(self):
        plan = {'image': 'ak820-vial-trial.bin', 'sha256': 'digest', 'size': 51136}
        for answers in ([''], ['y'], ['YES'], ['RESET TO LOADER']):
            with patch('builtins.input', side_effect=answers), contextlib.redirect_stdout(io.StringIO()), \
                 patch.object(app.transport, 'flash') as flash:
                with self.assertRaises(app.Cancelled):
                    app.consent(self.log, plan, recovery=False)
                flash.assert_not_called()
        output = io.StringIO()
        with patch('builtins.input', side_effect=['yes']), contextlib.redirect_stdout(output):
            result = app.consent(self.log, plan, recovery=False)
        self.assertIn('PERMANENT:', output.getvalue())
        self.assertNotIn('RC6 PERMANENT:', output.getvalue())
        self.assertTrue(result['reset'] and result['erase'] and result['flash'] and result['restart'])

    def fixture_release(self, *, use_bad_rc3=False, reproduction=False):
        bundle = self.root / 'bundle'
        for name in app.REQUIRED_FILES:
            path = bundle / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if name in ('reference/stock-full.bin', 'reference/native-installed.bin'):
                shutil.copyfile(app.RECOVERY_REFERENCE / Path(name).name, path)
                if name == 'reference/native-installed.bin':
                    path.write_bytes(app.packer.public_native_reference(path.read_bytes()))
            else:
                path.write_text(name + '\n', encoding='utf-8')
        if use_bad_rc3:
            (bundle / 'firmware/application.ihx').write_bytes(b'known-bad-rc3-test-fixture')
        names = set(app.REQUIRED_FILES)
        if reproduction:
            path = bundle / app.REPRODUCTION_BUILDER
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'actual reviewed builder fixture')
            app.json_write(bundle / 'reports/build-report.json', {'builder_sha256': app.sha(path.read_bytes())})
            names.add(app.REPRODUCTION_BUILDER)
        review = {'format': 'ak820-offline-review-2', 'release': app.RELEASE, 'status': 'passed',
                  'hardware_validated': False, 'host_files': host_manifest(app.ROOT),
                  'build': {key: app.sha((bundle / name).read_bytes()) for key, name in (
                      ('ihx_sha256', 'firmware/application.ihx'),
                      ('map_sha256', 'firmware/application.map'),
                      ('build_report_sha256', 'reports/build-report.json'))}}
        (bundle / 'reviews/independent-review.md').write_text(
            '# Fixture independent review\n\n```json\n' + json.dumps(review) + '\n```\n')
        manifest = {'format': 'ak820-installer-release-2', 'release': app.RELEASE, 'hardware': app.HARDWARE,
                    'host_files': host_manifest(app.ROOT),
                    'trial_only': True, 'hardware_validated': False,
                    'offline_review': {'status': 'passed', 'report': 'reviews/independent-review.md'},
                    'files': {name: {'size': (bundle / name).stat().st_size,
                                     'sha256': app.sha((bundle / name).read_bytes())}
                              for name in names}}
        app.json_write(bundle / 'installer-release.json', manifest)
        approval = self.root / 'approval.json'
        app.json_write(approval, {'format': 'ak820-installer-approval-1', 'release': app.RELEASE,
                                 'manifest_sha256': app.sha((bundle / 'installer-release.json').read_bytes())})
        return bundle, approval, manifest

    def test_old_and_reproduction_bundles_load_without_hid(self):
        for reproduction in (False, True):
            with self.subTest(reproduction=reproduction):
                bundle, approval, _ = self.fixture_release(reproduction=reproduction)
                with patch.object(app, 'BUNDLE', bundle), patch.object(app, 'APPROVAL', approval), \
                     patch.object(app.diagnostic, 'diagnostic_build', return_value={}), \
                     patch.object(app, 'hid_module') as hid:
                    app.load_release(approved=True)
                    hid.assert_not_called()

    def test_reproduction_builder_must_match_report_even_with_valid_manifest_hash(self):
        bundle, _, manifest = self.fixture_release(reproduction=True)
        path = bundle / app.REPRODUCTION_BUILDER
        path.write_bytes(b'different builder')
        manifest['files'][app.REPRODUCTION_BUILDER] = {
            'size': path.stat().st_size, 'sha256': app.sha(path.read_bytes())}
        app.json_write(bundle / 'installer-release.json', manifest)
        with patch.object(app, 'BUNDLE', bundle), patch.object(app.diagnostic, 'diagnostic_build') as diagnostics:
            with self.assertRaisesRegex(ValueError, 'Reproduction builder differs'):
                app.load_release(approved=False)
            diagnostics.assert_not_called()

    def test_reproduction_builder_bytes_are_hash_checked(self):
        bundle, _, _ = self.fixture_release(reproduction=True)
        (bundle / app.REPRODUCTION_BUILDER).write_bytes(b'corrupt')
        with patch.object(app, 'BUNDLE', bundle):
            with self.assertRaisesRegex(ValueError, 'modified or corrupted'):
                app.load_release(approved=False)

    def test_extra_unknown_manifest_file_still_rejected(self):
        for reproduction in (False, True):
            with self.subTest(reproduction=reproduction):
                bundle, _, manifest = self.fixture_release(reproduction=reproduction)
                manifest['files']['reproduction/unexpected.py'] = {'size': 0, 'sha256': app.sha(b'')}
                app.json_write(bundle / 'installer-release.json', manifest)
                with patch.object(app, 'BUNDLE', bundle):
                    with self.assertRaisesRegex(ValueError, 'unexpected release contents'):
                        app.load_release(approved=False)

    def test_offline_verify_never_loads_hid(self):
        bundle, approval, _ = self.fixture_release()
        self.assertFalse((bundle / 'reference/stock-full.bin').exists())
        self.assertFalse((bundle / 'reference/native-installed.bin').exists())
        with patch.object(app, 'BUNDLE', bundle), patch.object(app, 'APPROVAL', approval), \
             patch.object(app, 'RUNS', self.root / 'runs'), \
             patch.object(app.diagnostic, 'diagnostic_build', return_value={}), \
             patch.object(app, 'hid_module') as hid, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(app.main(['verify']), 0)
            hid.assert_not_called()

    def test_known_bad_rc3_is_rejected_even_with_renamed_manifest_and_approval(self):
        bundle, approval, _ = self.fixture_release(use_bad_rc3=True)
        with patch.object(app, 'BUNDLE', bundle), patch.object(app, 'APPROVAL', approval), \
             patch.object(app.diagnostic, 'diagnostic_build') as diagnostics:
            with self.assertRaisesRegex(ValueError, 'RC3'):
                app.load_release(approved=True)
            diagnostics.assert_not_called()

    def test_corrupt_mixed_and_unapproved_artifacts_rejected_before_hid(self):
        bundle, approval, manifest = self.fixture_release()
        with patch.object(app, 'BUNDLE', bundle), patch.object(app, 'APPROVAL', approval), \
             patch.object(app.diagnostic, 'diagnostic_build', return_value={}):
            app.load_release(approved=True)
            approval.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'Approval'):
                app.load_release(approved=True)
            # Preparation may inspect a candidate, but cannot authorize flash.
            app.load_release(approved=False)
            (bundle / 'firmware/application.map').write_text('wrong build')
            with self.assertRaisesRegex(ValueError, 'corrupted'):
                app.load_release(approved=False)

    def test_every_distributed_release_file_is_hash_checked(self):
        bundle, approval, _ = self.fixture_release()
        with patch.object(app, 'BUNDLE', bundle), patch.object(app, 'APPROVAL', approval), \
             patch.object(app.diagnostic, 'diagnostic_build', return_value={}):
            app.load_release(approved=True)
            for name in sorted(app.REQUIRED_FILES):
                path = bundle / name
                original = path.read_bytes()
                with self.subTest(file=name):
                    path.write_bytes(original + b'corrupt')
                    with self.assertRaisesRegex(ValueError, 'modified or corrupted'):
                        app.load_release(approved=True)
                    path.write_bytes(original)

    def test_missing_approval_blocks_install_before_hid(self):
        bundle, approval, _ = self.fixture_release()
        approval.unlink()
        with patch.object(app, 'BUNDLE', bundle), patch.object(app, 'APPROVAL', approval), \
             patch.object(app, 'RUNS', self.root / 'runs'), patch.object(app.sys.stdin, 'isatty', return_value=True), \
             patch.object(app.diagnostic, 'diagnostic_build', return_value={}), \
             patch.object(app, 'hid_module') as hid, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(app.main(['install']), 1)
            hid.assert_not_called()

    def test_changed_host_helper_rejected_before_hid(self):
        bundle, approval, _ = self.fixture_release()
        copied_root = self.root / 'checkout'
        for name in HOST_FILES:
            path = copied_root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(app.ROOT / name, path)
        helper = copied_root / 'qmk-8051-ak820/util/pack_ak820.py'
        helper.write_bytes(helper.read_bytes() + b'\n# changed after review\n')
        with patch.object(app, 'ROOT', copied_root), patch.object(app, 'BUNDLE', bundle), \
             patch.object(app, 'APPROVAL', approval), patch.object(app, 'RUNS', self.root / 'runs'), \
             patch.object(app.sys.stdin, 'isatty', return_value=True), \
             patch.object(app.diagnostic, 'diagnostic_build', return_value={}), \
             patch.object(app, 'hid_module') as hid, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(app.main(['install']), 1)
            hid.assert_not_called()

    def test_missing_host_manifest_is_rejected(self):
        bundle, _, manifest = self.fixture_release()
        del manifest['host_files']
        app.json_write(bundle / 'installer-release.json', manifest)
        with patch.object(app, 'BUNDLE', bundle), \
             patch.object(app.diagnostic, 'diagnostic_build', return_value={}):
            with self.assertRaisesRegex(ValueError, 'host-code'):
                app.load_release(approved=False)

    def test_review_for_another_build_is_rejected_even_with_matching_file_hash(self):
        bundle, _, manifest = self.fixture_release()
        path = bundle / 'reviews/independent-review.md'
        record = app.read_review_record(path.read_text())
        record['build']['ihx_sha256'] = 'old build'
        path.write_text('```json\n' + json.dumps(record) + '\n```\n')
        manifest['files']['reviews/independent-review.md'] = {
            'size': path.stat().st_size, 'sha256': app.sha(path.read_bytes())}
        app.json_write(bundle / 'installer-release.json', manifest)
        with patch.object(app, 'BUNDLE', bundle), \
             patch.object(app.diagnostic, 'diagnostic_build', return_value={}):
            with self.assertRaisesRegex(ValueError, 'different build'):
                app.load_release(approved=False)

    def test_recovery_copy_never_writes_original_session(self):
        before = {path.name: app.sha(path.read_bytes()) for path in app.ORIGINAL.iterdir() if path.is_file()}
        dest, backup = app.copy_recovery(self.log, app.ORIGINAL)
        self.assertEqual(dest.parent, self.root)
        self.assertEqual((dest / 'before-full-rom.bin').read_bytes(), backup)
        app.transport.plan(dest, 'restore')
        self.assertEqual(before, {path.name: app.sha(path.read_bytes()) for path in app.ORIGINAL.iterdir() if path.is_file()})

    def test_recover_does_not_reset_an_application(self):
        with patch.object(app.transport, 'flash') as flash, patch('builtins.input') as input_, \
             contextlib.redirect_stdout(io.StringIO()):
            app.recover(self.log, FakeHid([descriptor('OEM_APP')]), app.ORIGINAL)
            flash.assert_not_called()
            input_.assert_not_called()
            with self.assertRaisesRegex(ValueError, 'OEM loader'):
                app.recover(self.log, FakeHid([descriptor('VIAL_APP')]), app.ORIGINAL)
            flash.assert_not_called()

    def test_native_capture_retains_partial_rom_on_read_failure(self):
        class Device:
            native = True
            def rom(self, address, length):
                if address >= 2048:
                    raise TimeoutError('simulated disconnected keyboard')
                return bytes([0x55]) * length
            def close(self):
                pass
        with patch.object(app.transport, 'Application', return_value=Device()), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(TimeoutError):
                app.capture_native(self.log, descriptor('OEM_APP'), references=app.RECOVERY_REFERENCE)
        self.assertEqual((self.root / 'native-prefix.bin').stat().st_size, 2048)
        self.assertFalse((self.root / 'native-rom.bin').exists())


class BootStatusTests(BaseCase):
    def feature_device(self, reports):
        hid = FakeHid([descriptor('VIAL_APP')])
        values = iter(reports)
        class FeatureDevice:
            def open_path(self, path):
                hid.opens.append(path)
            def get_feature_report(self, report_id, length):
                if (report_id, length) != (0, 9):
                    raise AssertionError('Unexpected HID request')
                return next(values)
            def close(self):
                pass
            def write(self, _):
                raise AssertionError('Raw HID output is forbidden in the startup check')
            def send_feature_report(self, _):
                raise AssertionError('SET_REPORT is forbidden in the startup check')
        hid.device = FeatureDevice
        return hid

    @staticmethod
    def report(stage, heartbeat, flags=1):
        return b'\0AKBT\1' + bytes((stage, heartbeat, flags))

    def test_progress_on_ep0_without_raw_endpoint(self):
        hid = self.feature_device([self.report(1, 0), self.report(3, 2), self.report(3, 2), self.report(3, 8)])
        with patch.object(app.time, 'sleep'), patch.object(app.time, 'monotonic', side_effect=[0, 0, 0.2, 0.4, 0.6]):
            result = app.boot_status(hid, descriptor('VIAL_APP'), self.log)
        self.assertEqual(len(result), 4)
        self.assertEqual(hid.writes, [])
        self.assertTrue(any(row['event'] == 'main_loop_progress_observed' for row in self.log.events))

    def test_enumerated_but_stalled_main_loop_is_not_success(self):
        hid = self.feature_device([self.report(3, 7)] * 3)
        with patch.object(app.time, 'sleep'), patch.object(app.time, 'monotonic', side_effect=[0, 0, 1, 2, 6]):
            with self.assertRaisesRegex(TimeoutError, 'main loop'):
                app.boot_status(hid, descriptor('VIAL_APP'), self.log)
        self.assertFalse(any(row['event'] == 'main_loop_progress_observed' for row in self.log.events))

    def test_bad_feature_is_failure_without_blind_retry(self):
        hid = self.feature_device([b'\0' * 9])
        with self.assertRaisesRegex(ValueError, 'boot status'):
            app.boot_status(hid, descriptor('VIAL_APP'), self.log)
        self.assertEqual(hid.opens, [b'device-one'])

    def test_suspend_or_restart_cannot_forge_counter_progress(self):
        hid = self.feature_device([self.report(3, 1), self.report(3, 2, 3), self.report(3, 3)])
        with patch.object(app.time, 'sleep'), patch.object(app.time, 'monotonic', side_effect=[0, 0, 1, 2, 6]):
            with self.assertRaises(TimeoutError):
                app.boot_status(hid, descriptor('VIAL_APP'), self.log)


class TransportTests(BaseCase):
    def test_direct_permanent_requires_fresh_native_snapshot_and_guards(self):
        backup = app.check_original()
        with contextlib.redirect_stdout(io.StringIO()):
            session, _ = app.prepare_trial(self.log, backup, context=self.context)
        hid = self.loader()
        hid.descriptors = [descriptor('OEM_APP')]
        events = []
        class Native:
            def rom(self, start, size):
                return backup
            def enter_native_loader(self):
                events.append('native_reset')
                hid.descriptors = [descriptor('LOADER')]
            def close(self):
                pass
        def guard(phase, **fields):
            self.assertEqual(fields['image'], 'permanent')
            events.append(phase)
        with patch.object(app.transport, 'hid_module', return_value=hid), \
             patch.object(app.transport, 'Application', return_value=Native()), \
             patch.object(app.transport.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
            app.transport.flash(session, 'permanent', True, False, native_install=True,
                reference_dir=app.BUNDLE / 'reference', application_descriptor=descriptor('OEM_APP'),
                phase_guard=guard)
        self.assertEqual(events, ['reset_to_loader', 'native_reset', 'erase_and_flash', 'restart'])
        self.assertEqual(hid.commands, [1, 2, 3, 4, 5])

    def test_direct_permanent_cannot_bypass_guard_or_native_provenance(self):
        backup = app.check_original()
        with contextlib.redirect_stdout(io.StringIO()):
            session, _ = app.prepare_trial(self.log, backup, context=self.context)
        for changes in ({'phase_guard': None}, {'application_descriptor': None}, {'enter_loader': False}):
            options = dict(enter_loader=True, phase_guard=lambda *_a, **_kw: None,
                           application_descriptor=descriptor('OEM_APP'))
            options.update(changes)
            with self.subTest(changes=changes), patch.object(app.transport, 'hid_module') as hid:
                with self.assertRaisesRegex(ValueError, 'guarded fresh native backup'):
                    app.transport.flash(session, 'permanent', accept_hardware_check=False,
                        native_install=True, reference_dir=app.BUNDLE / 'reference', **options)
                hid.assert_not_called()
        metadata = json.loads((session / 'images.json').read_text())
        metadata['native_install_backup_sha256'] = 'stale'
        (session / 'images.json').write_text(json.dumps(metadata))
        with patch.object(app.transport, 'hid_module') as hid:
            with self.assertRaisesRegex(ValueError, 'guarded fresh native backup'):
                app.transport.flash(session, 'permanent', True, False, native_install=True,
                    reference_dir=app.BUNDLE / 'reference', application_descriptor=descriptor('OEM_APP'),
                    phase_guard=lambda *_a, **_kw: None)
            hid.assert_not_called()

    def test_direct_permanent_refuses_changed_live_native_rom_before_reset(self):
        backup = app.check_original()
        with contextlib.redirect_stdout(io.StringIO()):
            session, _ = app.prepare_trial(self.log, backup, context=self.context)
        native = unittest.mock.Mock()
        changed = bytearray(backup)
        changed[0xA000] ^= 1
        native.rom.return_value = bytes(changed)
        with patch.object(app.transport, 'hid_module', return_value=FakeHid([])), \
             patch.object(app.transport, 'Application', return_value=native), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, 'Live ROM differs'):
                app.transport.flash(session, 'permanent', True, False, native_install=True,
                    reference_dir=app.BUNDLE / 'reference', application_descriptor=descriptor('OEM_APP'),
                    phase_guard=lambda *_a, **_kw: None)
        native.enter_native_loader.assert_not_called()
        native.close.assert_called_once()

    def loader(self, *, fail_checksum=False):
        hid = FakeHid([descriptor('LOADER')])
        hid.commands = []
        hid.closed = False
        class Loader:
            command = None
            def open_path(self, path):
                hid.opens.append(path)
            def send_feature_report(self, packet):
                if len(packet) != 65 or packet[0] != 0:
                    raise AssertionError('Invalid report length/id')
                hid.writes.append(packet)
                if packet[2:5] == b'\xaa\x55\0':
                    self.command = packet[1]
                    hid.commands.append(self.command)
                return len(packet)
            def get_feature_report(self, report_id, length):
                response = bytearray(65)
                response[:9] = bytes((0, self.command, 0xAA, 0x55, 0)) + bytes.fromhex('fafafafa')
                if self.command == 1:
                    response[9:13] = bytes.fromhex('00112233')
                if self.command == 4 and fail_checksum:
                    response[5] = 0
                return response
            def close(self):
                hid.closed = True
        hid.device = Loader
        return hid

    def test_refused_phase_guard_stops_after_identity_without_erase(self):
        session, _ = app.copy_recovery(self.log, app.ORIGINAL)
        hid = self.loader()
        def guard(phase, **fields):
            self.assertEqual(phase, 'erase_and_flash')
            raise RuntimeError('operator authorization mismatch')
        with patch.object(app.transport, 'hid_module', return_value=hid), patch.object(app.transport.time, 'sleep'), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, 'authorization'):
                app.transport.flash(session, 'restore', False, False, reference_dir=app.RECOVERY_REFERENCE,
                                    loader_descriptor=descriptor('LOADER'), phase_guard=guard)
        self.assertEqual(hid.commands, [1])
        self.assertTrue(hid.closed)

    def test_loader_checksum_failure_never_restarts_or_auto_restores(self):
        session, _ = app.copy_recovery(self.log, app.ORIGINAL)
        hid = self.loader(fail_checksum=True)
        stages = []
        with patch.object(app.transport, 'hid_module', return_value=hid), patch.object(app.transport.time, 'sleep'), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'loader reply'):
                app.transport.flash(session, 'restore', False, False, reference_dir=app.RECOVERY_REFERENCE,
                                    loader_descriptor=descriptor('LOADER'),
                                    phase_guard=lambda phase, **_: stages.append(phase))
        self.assertEqual(hid.commands, [1, 2, 3, 4])
        self.assertEqual(stages, ['erase_and_flash'])
        self.assertTrue(hid.closed)

    def test_wrong_loader_path_is_rejected_before_open(self):
        session, _ = app.copy_recovery(self.log, app.ORIGINAL)
        hid = self.loader()
        with patch.object(app.transport, 'hid_module', return_value=hid), patch.object(app.transport.time, 'sleep'), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, 'identity changed'):
                app.transport.flash(session, 'restore', False, False, reference_dir=app.RECOVERY_REFERENCE,
                                    loader_descriptor=descriptor('LOADER', b'different'))
        self.assertEqual(hid.opens, [])
        self.assertEqual(hid.writes, [])


class InstallFlowTests(BaseCase):
    """Exercise the real orchestrator and boot probe, with fake device I/O."""
    def run_install(self, *, bad_boot=False, mismatched_nvm=False):
        events = []
        bundle = self.root / 'bundle'
        (bundle / 'reference').mkdir(parents=True)
        shutil.copyfile(app.RECOVERY_REFERENCE / 'stock-full.bin', bundle / 'reference/stock-full.bin')
        hid = FakeHid([descriptor('OEM_APP')])
        trial = bytes(app.packer.APP_END - app.packer.APP_START)
        backup = bytes(65536)
        rom = bytearray(backup)
        if mismatched_nvm:
            rom[app.packer.NVM_START] = 1
        session = self.root / 'trial-session'
        session.mkdir()
        plan = {'image': 'ak820-vial-trial.bin', 'sha256': app.sha(trial), 'size': len(trial)}
        manifest = {'ihx_sha256': 'ihx-identity', 'map_sha256': 'map-identity'}
        release = {'install_modes': ['permanent', 'trial'], 'files': {'firmware/application.ihx': {'sha256': 'ihx-identity'},
                             'firmware/application.map': {'sha256': 'map-identity'}}}
        answers = iter(['y', 'yes', 'ak820'])

        def prompt(message):
            if message.startswith('AK820>'):
                events.append('keyboard_input')
            else:
                events.append('consent')
            return next(answers)

        def capture_native(*_args, **_kwargs):
            events.append('fresh_backup')
            return backup

        def prepare(*_args, **_kwargs):
            events.append('prepare_trial')
            return session, plan

        def flash(*_args, **_kwargs):
            self.assertEqual(events, ['consent', 'fresh_backup', 'prepare_trial', 'consent'])
            events.append('flash')
            hid.descriptors = [descriptor('VIAL_APP')]

        class Feature:
            counter = 0
            def open_path(self, path):
                pass
            def get_feature_report(self, report_id, length):
                self.counter += 1
                events.append('ep0_feature')
                return bytes(9) if bad_boot else b'\0AKBT\1' + bytes((3, self.counter, 1))
            def close(self):
                pass
        hid.device = Feature

        def capture(output, **_kwargs):
            events.append('fd00_capture')
            output.mkdir()
            (output / 'rom.bin').write_bytes(rom)
            return {'nvm_and_journal_stable_on_second_read': True, 'status': {'storage_failed': False}}

        with patch.object(app, 'BUNDLE', bundle), \
             patch.object(app, 'load_release', return_value=release), patch.object(app, 'check_original'), \
             patch.object(app, 'capture_native', side_effect=capture_native), \
             patch.object(app, 'prepare_trial', side_effect=prepare), \
             patch.object(app.transport, 'flash', side_effect=flash) as flashing, \
             patch.object(app.transport, 'session_image', return_value=(manifest, trial, backup)), \
             patch.object(app.transport, 'verify_live') as verify_code, \
             patch.object(app.diagnostic, 'diagnostic_build', return_value={1: 2}), \
             patch.object(app.diagnostic, 'capture', side_effect=capture) as code_capture, \
             patch.object(app.time, 'sleep'), patch('builtins.input', side_effect=prompt), \
             contextlib.redirect_stdout(io.StringIO()):
            error = None
            try:
                app.install(self.log, hid, context=self.context)
            except ValueError as caught:
                error = caught
            self.assertEqual(flashing.call_count, 1)
            if bad_boot:
                self.assertIsNotNone(error)
                self.assertIn('boot status', str(error))
                code_capture.assert_not_called()
                verify_code.assert_not_called()
            else:
                self.assertEqual(code_capture.call_count, 1)
                self.assertEqual(verify_code.call_count, 1)
                if mismatched_nvm:
                    self.assertIsNotNone(error)
                    self.assertIn('Initial settings', str(error))
                else:
                    self.assertIsNone(error)
        return events

    def test_success_requires_fresh_backup_consent_ep0_typing_and_code_readback(self):
        events = self.run_install()
        self.assertLess(events.index('consent'), events.index('fresh_backup'))
        self.assertLess(events.index('consent'), events.index('flash'))
        self.assertLess(events.index('flash'), events.index('ep0_feature'))
        self.assertLess(events.index('ep0_feature'), events.index('keyboard_input'))
        self.assertLess(events.index('keyboard_input'), events.index('fd00_capture'))

    def test_failed_boot_status_stops_before_fd00_and_never_reflashes(self):
        events = self.run_install(bad_boot=True)
        self.assertNotIn('fd00_capture', events)
        self.assertNotIn('keyboard_input', events)

    def test_successful_loader_with_mismatched_initial_nvm_is_not_success(self):
        self.run_install(mismatched_nvm=True)


if __name__ == '__main__':
    unittest.main()
