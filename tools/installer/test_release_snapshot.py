"""Synthetic offline release snapshot integration tests; no HID."""
import json
import sys
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import Mock, patch

import ak820 as app
from ak820_release_manifest import host_manifest


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in app.HOST_FILES:
            source = app.ROOT / name
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
        self.bundle = self.root / 'releases/beta4/main'
        shutil.copytree(app.ROOT / 'releases/rc6', self.bundle)
        report_path = self.bundle / 'reports/build-report.json'
        report = json.loads(report_path.read_bytes())
        report['configuration'] = app.ak820_profiles.configuration('main')
        report_path.write_text(json.dumps(report), encoding='utf-8')
        manifest = json.loads((self.bundle / 'installer-release.json').read_bytes())
        manifest['host_files'] = host_manifest(self.root)
        names = manifest['files']
        review = {'format': 'ak820-offline-review-2', 'release': app.RELEASE,
                  'status': 'passed', 'hardware_validated': False,
                  'host_files': manifest['host_files'], 'build': {
                      key: app.sha((self.bundle / name).read_bytes()) for key, name in (
                          ('ihx_sha256', 'firmware/application.ihx'),
                          ('map_sha256', 'firmware/application.map'),
                          ('build_report_sha256', 'reports/build-report.json'))}}
        (self.bundle / 'reviews/independent-review.md').write_text(
            '```json\n' + json.dumps(review) + '\n```\n', encoding='utf-8')
        for name in names:
            data = (self.bundle / name).read_bytes()
            names[name] = {'size': len(data), 'sha256': app.sha(data)}
        self.manifest = manifest
        self.approval = self.bundle / 'approved-release.json'
        self.save_manifest()
        self.root_patch = patch.object(app, 'ROOT', self.root)
        self.root_patch.start(); self.addCleanup(self.root_patch.stop)

    def save_manifest(self):
        raw = (json.dumps(self.manifest, indent=2) + '\n').encode()
        (self.bundle / 'installer-release.json').write_bytes(raw)
        self.approval.write_text(json.dumps({'format': 'ak820-installer-approval-1',
                                            'release': app.RELEASE, 'manifest_sha256': app.sha(raw)}))

    def test_success_snapshot_and_path_wrapper(self):
        snapshot = app._release_snapshot(self.bundle, self.approval, approved=True)
        self.assertEqual(snapshot.manifest, self.manifest)
        self.assertEqual(app._load_release(self.bundle, self.approval, approved=True), self.manifest)
        context = app.release_context('main', approved=True)
        self.assertEqual(context.nvm_schema, app.ak820_profiles.configuration('main')['nvm_schema'])
        self.assertEqual(app.session_release_identity(context)['manifest_sha256'],
                         app.sha((self.bundle / 'installer-release.json').read_bytes()))
        with self.assertRaises(TypeError): snapshot.files['firmware/application.ihx'] = b'x'
        m = snapshot.manifest; m.clear(); self.assertEqual(snapshot.manifest, self.manifest)

    def test_cli_real_release_recheck_after_diagnostic_late_swap(self):
        import contextlib
        import io
        context = app.release_context('main', approved=True)
        stock = bytearray((address * 17 + 23) % 256 for address in range(65536))
        stock[0x27c0:0x27c4] = bytes.fromhex('aa5533cc')
        stock[0xa000:0xd200] = bytes(0x3200)
        for slot in (*app.packer.PHYSICAL, 87, 111):
            stock[0xa100+slot*3:0xa100+slot*3+3] = bytes.fromhex('200004')
        stock = bytes(stock)
        for name, value in {'PROTECTED_SHA': app.sha(stock[:0x27c0] + stock[app.packer.APP_END:]),
                            'FACTORY_CODE_SHA': app.sha(stock[app.packer.APP_START:0xa000] + stock[0xd200:app.packer.APP_END])}.items():
            patcher = patch.object(app.packer, name, value); patcher.start(); self.addCleanup(patcher.stop)
        folder = self.root / 'prepared'; folder.mkdir()
        refs = (stock, stock[app.packer.APP_START:app.packer.APP_END])
        session, _ = app.prepare_trial(Mock(folder=folder), stock, image='trial', context=context, reference_bytes=refs)
        _, payload, _ = app.transport.session_image(session, 'trial', target_build_id=context.nvm_schema)
        rom = stock[:0x27c0] + bytes(0x40) + payload + stock[app.packer.APP_END:]
        output = self.root / 'cli-output'; output.mkdir()
        log = Mock(folder=output); approval = self.approval
        class FakeApplication:
            native = False
            def raw(self, packet):
                if packet[:2] == b'\xfd\x01':
                    approval.write_text('{}')
                    return b'\xfd\x01\x01\xa8' + bytes(28)
                address = int.from_bytes(packet[2:4], 'big'); size = packet[4]
                return packet[:5] + rom[address:address+size] + bytes(27-size)
            def close(self): pass
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout), patch.object(app, 'Log', return_value=log), \
             patch.object(app, 'hid_module', return_value=Mock()), \
             patch.object(app, 'require_state', return_value={'path': b'fake'}), \
             patch.object(app, 'boot_status'), patch.object(app, 'keyboard_smoke', return_value=True), \
             patch.object(app.transport, 'Application', return_value=FakeApplication()), \
             patch.object(app.diagnostic, 'capture', wraps=app.diagnostic.capture) as capture, \
             patch.object(app, 'load_release', wraps=app.load_release) as load:
            status = app.main(['check-device', '--profile', 'main', '--session', str(session), '--trial'], interactive=True)
        self.assertEqual(status, 1)
        capture.assert_called_once()
        self.assertGreaterEqual(load.call_count, 2)
        self.assertNotIn('application_readback_verified', [call.args[0] for call in log.record.call_args_list])
        self.assertNotIn('Typing, CODE', stdout.getvalue())
        self.assertEqual(approval.read_text(), '{}')

    def test_artifact_changed_after_read_uses_original_and_recheck_fails(self):
        target = self.bundle / 'firmware/application.map'
        expected = target.read_bytes()
        read = Path.read_bytes
        def replace(path):
            raw = read(path)
            if path == target:
                path.write_bytes(b'replaced after capture')
            return raw
        with patch.object(Path, 'read_bytes', replace):
            context = app.release_context('main', approved=True)
        self.assertEqual(context.snapshot.files['firmware/application.map'], expected)
        with self.assertRaisesRegex(ValueError, 'modified or corrupted'):
            app.load_release(approved=True, context=context)

    def test_catalog_changed_after_read_uses_original_and_recheck_fails(self):
        target = self.root / 'tools/installer/profile-catalog.json'
        expected = target.read_bytes()
        read = Path.read_bytes
        def replace(path):
            raw = read(path)
            if path == target:
                path.write_bytes(b'{}')
            return raw
        with patch.object(Path, 'read_bytes', replace):
            context = app.release_context('main', approved=True)
        self.assertEqual(context.snapshot.host_files['tools/installer/profile-catalog.json'], expected)
        with self.assertRaises(ValueError): app.load_release(approved=True, context=context)

    def test_manifest_changed_after_read_uses_approved_original(self):
        target = self.bundle / 'installer-release.json'
        original = target.read_bytes()
        read = Path.read_bytes
        def replace(path):
            raw = read(path)
            if path == target:
                path.write_bytes(b'{}')
            return raw
        with patch.object(Path, 'read_bytes', replace):
            context = app.release_context('main', approved=True)
        self.assertEqual(context.snapshot.manifest_bytes, original)
        self.assertEqual(app.session_release_identity(context)['manifest_sha256'], app.sha(original))
        with self.assertRaises(ValueError): app.load_release(approved=True, context=context)

    def test_rehashed_review_semantic_tampering_still_rejected(self):
        path = self.bundle / 'reviews/independent-review.md'
        record = app.read_review_record(path.read_text(encoding='utf-8'))
        record['status'] = 'pending'
        data = ('```json\n' + json.dumps(record) + '\n```\n').encode()
        path.write_bytes(data)
        self.manifest['files']['reviews/independent-review.md'] = {'size': len(data), 'sha256': app.sha(data)}
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'not a completed offline pass'):
            app._load_release(self.bundle, self.approval, approved=True)

    def test_standalone_bind_reads_manifest_once_when_replaced(self):
        sys.path.insert(0, str(app.ROOT / 'tools'))
        self.addCleanup(sys.path.remove, str(app.ROOT / 'tools'))
        import ak820_device_protocol as protocol
        manifest = self.bundle / 'installer-release.json'
        original = manifest.read_bytes()
        ihx = (self.bundle / 'firmware/application.ihx').read_bytes()
        map_bytes = (self.bundle / 'firmware/application.map').read_bytes()
        report = (self.bundle / 'reports/build-report.json').read_bytes()
        code = app.diagnostic.diagnostic_build_bytes(ihx, map_bytes, report)
        payload = bytearray(app.packer.APP_END - app.packer.APP_START)
        for address, value in code.items():
            if app.packer.APP_START <= address < app.packer.CODE_END:
                payload[address-app.packer.APP_START] = value
        images = {'ihx_sha256': app.sha(ihx), 'map_sha256': app.sha(map_bytes)}
        read = Path.read_bytes
        reads = []
        def replace(path):
            raw = read(path)
            if path == manifest:
                reads.append(raw)
                path.write_bytes(b'{"release":"different"}')
            return raw
        with patch.object(protocol, 'ROOT', self.root), patch.object(Path, 'read_bytes', replace), \
             patch.object(protocol.transport, 'session_image', return_value=(images, bytes(payload), bytes(65536))), \
             patch.object(protocol.pack, 'validate_native'):
            binding = protocol.bind(self.bundle, self.root / 'session', self.approval)
        self.assertEqual(reads, [original])
        self.assertEqual(binding['release'], self.manifest['release'])
        self.assertEqual(binding['code'], code)
        self.assertNotEqual(manifest.read_bytes(), original)

    def test_standalone_bind_uses_snapshot_after_map_replacement(self):
        sys.path.insert(0, str(app.ROOT / 'tools'))
        self.addCleanup(sys.path.remove, str(app.ROOT / 'tools'))
        import ak820_device_protocol as protocol
        ihx = (self.bundle / 'firmware/application.ihx').read_bytes()
        mapfile = self.bundle / 'firmware/application.map'
        map_bytes = mapfile.read_bytes()
        report = (self.bundle / 'reports/build-report.json').read_bytes()
        code = app.diagnostic.diagnostic_build_bytes(ihx, map_bytes, report)
        payload = bytearray(app.packer.APP_END - app.packer.APP_START)
        for address, value in code.items():
            if app.packer.APP_START <= address < app.packer.CODE_END:
                payload[address-app.packer.APP_START] = value
        images = {'ihx_sha256': app.sha(ihx), 'map_sha256': app.sha(map_bytes)}
        read = Path.read_bytes
        def replace(path):
            raw = read(path)
            if path == mapfile:
                path.write_bytes(b'replaced')
            return raw
        with patch.object(protocol, 'ROOT', self.root), patch.object(Path, 'read_bytes', replace), \
             patch.object(protocol.transport, 'session_image', return_value=(images, bytes(payload), bytes(65536))), \
             patch.object(protocol.pack, 'validate_native'):
            binding = protocol.bind(self.bundle, self.root / 'session', self.approval)
        self.assertEqual(binding['code'], code)
        self.assertEqual(binding['definition'], json.loads((self.bundle / 'reference/vial.json').read_bytes()))
        self.assertEqual(mapfile.read_bytes(), b'replaced')

    def test_install_packing_uses_snapshot_during_replacement_then_guard_recheck(self):
        # Synthetic native inputs; this is an offline orchestration test, not device evidence.
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
        pins = {'PROTECTED_SHA': app.sha(stock[:0x27C0] + stock[app.packer.APP_END:]),
                'FACTORY_CODE_SHA': app.sha(stock[app.packer.APP_START:0xA000] + stock[0xD200:app.packer.APP_END]),
                'PATCHED_CODE_SHA': app.sha(native[:0xA000-app.packer.APP_START] + native[0xD380-app.packer.APP_START:]),
                'STOCK_SHA': app.sha(stock), 'NATIVE_SHA': app.sha(native),
                'NATIVE_PUBLIC_SHA': app.sha(public),
                'NATIVE_REFERENCE_HASHES': frozenset((app.sha(native), app.sha(public)))}
        for name, value in pins.items():
            p = patch.object(app.packer, name, value); p.start(); self.addCleanup(p.stop)
        reference = self.root / 'private-reference'; reference.mkdir()
        (reference / 'stock-full.bin').write_bytes(stock)
        (reference / 'native-installed.bin').write_bytes(native)
        context = app.release_context('main', approved=True)
        owner_ref = self.root / 'exact-owner-reference'; owner_ref.mkdir()
        owner_stock = owner_ref / 'stock-full.bin'
        owner_native = owner_ref / 'native-installed.bin'
        owner_backup = bytes(stock)
        owner_slice = owner_backup[app.packer.APP_START:app.packer.APP_END]
        owner_stock.write_bytes(owner_backup); owner_native.write_bytes(owner_slice)
        self.assertEqual(app.operation_references(owner_backup), (owner_backup, owner_slice))
        self.assertEqual(app.operation_references(owner_backup, owner_ref), (owner_backup, owner_slice))
        original_read = Path.read_bytes
        reads = []
        def read_once(path):
            if path in (owner_stock, owner_native):
                self.assertNotIn(path, reads)
                reads.append(path)
            return original_read(path)
        with patch.object(Path, 'read_bytes', read_once):
            self.assertEqual(app.operation_references(owner_backup, owner_ref), (owner_backup, owner_slice))
        self.assertEqual(reads, [owner_stock, owner_native])
        for bad_stock, bad_native in ((owner_backup[:-1], owner_slice),
                                     (owner_backup, owner_slice[:-1]),
                                     (owner_slice, owner_backup),
                                     (owner_backup[:0xA201] + bytes((owner_backup[0xA201] ^ 1,)) + owner_backup[0xA202:], owner_slice),
                                     (owner_backup, bytes(native))):
            owner_stock.write_bytes(bad_stock); owner_native.write_bytes(bad_native)
            with self.assertRaisesRegex(ValueError, 'exact operation backup'):
                app.operation_references(owner_backup, owner_ref)
        owner_stock.write_bytes(owner_backup); owner_native.write_bytes(owner_slice)
        backup_path = self.root / 'owner-rom.bin'; backup_path.write_bytes(owner_backup)
        def offline_prepare(reference_dir, expected_status):
            args = ['prepare', '--native-rom', str(backup_path), '--trial']
            if reference_dir is not None: args += ['--reference-dir', str(reference_dir)]
            with patch.object(app, 'Log', return_value=Mock(folder=self.root)), \
                 patch.object(app, 'release_context', return_value=context), \
                 patch.object(app, 'prepare_trial') as prepare, \
                 patch.object(app, 'hid_module', side_effect=AssertionError('HID forbidden')) as hid:
                self.assertEqual(app.main(args), expected_status)
                hid.assert_not_called()
                if expected_status == 0:
                    self.assertEqual(prepare.call_args.args[1], owner_backup)
                    self.assertEqual(prepare.call_args.kwargs['reference_bytes'], (owner_backup, owner_slice))
                else:
                    prepare.assert_not_called()
        offline_prepare(None, 0)
        offline_prepare(owner_ref, 0)
        for supplied in (False, True):
            output = self.root / ('offline-real-' + str(supplied)); output.mkdir()
            args = ['prepare', '--native-rom', str(backup_path), '--trial']
            if supplied: args += ['--reference-dir', str(owner_ref)]
            with patch.object(app, 'Log', return_value=Mock(folder=output)), \
                 patch.object(app, 'release_context', return_value=context), \
                 patch.object(app, 'hid_module', side_effect=AssertionError('HID forbidden')):
                self.assertEqual(app.main(args), 0)
            _, _, copied = app.transport.session_image(output / 'trial-session', 'trial',
                                                        target_build_id=context.nvm_schema)
            self.assertEqual(copied, owner_backup)
        owner_native.write_bytes(bytes(native))
        offline_prepare(owner_ref, 1)
        failed_output = self.root / 'offline-real-rejected'; failed_output.mkdir()
        with patch.object(app, 'Log', return_value=Mock(folder=failed_output)), \
             patch.object(app, 'release_context', return_value=context), \
             patch.object(app, 'hid_module', side_effect=AssertionError('HID forbidden')):
            self.assertEqual(app.main(['prepare', '--native-rom', str(backup_path), '--trial',
                                       '--reference-dir', str(owner_ref)]), 1)
        self.assertFalse((failed_output / 'trial-session').exists())
        owner_native.write_bytes(owner_slice)
        # Model a separately pinned native variant with a different erase helper.
        variant = bytearray(stock)
        variant[0xE650] ^= 1
        variant[0xD400] ^= 1
        variant[0xD200:0xD380] = b'\xff' * 0x180
        variant = bytes(variant)
        variant_code = app.sha(variant[app.packer.APP_START:0xA000] + variant[0xD380:app.packer.APP_END])
        with patch.object(app.packer, 'PATCHED_CODE_SHA', variant_code), \
             patch.object(app, 'RECOVERY_REFERENCE', reference):
            app.packer.validate_native(variant, bytes(stock), bytes(native))
            self.assertEqual(app.operation_references(variant),
                             (variant, variant[app.packer.APP_START:app.packer.APP_END]))
            owner_stock.write_bytes(variant)
            owner_native.write_bytes(variant[app.packer.APP_START:app.packer.APP_END])
            self.assertEqual(app.operation_references(variant, owner_ref),
                             (variant, variant[app.packer.APP_START:app.packer.APP_END]))
            for mode in ('trial', 'permanent'):
                folder = self.root / ('variant-' + mode); folder.mkdir()
                with self.assertRaisesRegex(ValueError, 'exact operation backup'):
                    app.prepare_trial(Mock(folder=folder), variant, image=mode, context=context,
                                      reference_bytes=(bytes(stock), bytes(native)))
                self.assertFalse((folder / (mode + '-session')).exists())
                session, _ = app.prepare_trial(Mock(folder=folder), variant, image=mode, context=context,
                    reference_bytes=(variant, variant[app.packer.APP_START:app.packer.APP_END]))
                _, payload, session_backup = app.transport.session_image(session, mode,
                                                                         target_build_id=context.nvm_schema)
                expected = app.expected_install_payload(context, variant, mode, variant)
                self.assertEqual(payload, expected)
                self.assertEqual(session_backup, variant)
                self.assertEqual(payload[app.packer.ERASE_START-app.packer.APP_START:
                                         app.packer.ERASE_START-app.packer.APP_START+0x57], variant[0xE650:0xE6A7])
                self.assertNotEqual(stock[0xE650:0xE6A7], variant[0xE650:0xE6A7])
        paths = [self.bundle / 'firmware/application.ihx', self.bundle / 'firmware/application.map']
        original = [path.read_bytes() for path in paths]
        expected_code = app.packer.parse_ihex_bytes(original[0])
        hole = next(address for address in range(app.packer.CODE_END - 1, app.packer.CODE_START, -1)
                    if address not in expected_code)
        record = bytes((1, hole >> 8, hole & 255, 0, 0x22))
        altered_ihx = original[0].replace(b':00000001FF',
            b':' + (record + bytes((-sum(record) & 255,))).hex().encode() + b'\n:00000001FF')
        altered_map = original[1] + b'\nC: 00003027 _race_marker\n'
        alternative = [altered_ihx, altered_map]
        self.assertNotEqual(alternative, original)
        alternate_info = app.write_trial_bytes(altered_ihx, altered_map, reference / 'stock-full.bin',
                                               reference / 'native-installed.bin', bytes(stock),
                                               self.root / 'alternate-session', target_build_id=context.nvm_schema)
        self.assertEqual(alternate_info['ihx_sha256'], app.sha(altered_ihx))
        self.assertEqual(alternate_info['map_sha256'], app.sha(altered_map))
        prepare = app.prepare_trial
        class StopBeforeDevice(Exception): pass
        for mode, corrupt in (('trial', False), ('permanent', False), ('trial', True)):
            with self.subTest(mode=mode, corrupt=corrupt):
                folder = self.root / (mode + ('-bad' if corrupt else '-good')); folder.mkdir()
                calls = []
                def swapped(*args, **kwargs):
                    for path, raw in zip(paths, alternative): path.write_bytes(raw)
                    try:
                        with patch.object(app.packer, 'parse_ihex_bytes', wraps=app.packer.parse_ihex_bytes) as ihx, \
                             patch.object(app.packer, 'parse_symbols_bytes', wraps=app.packer.parse_symbols_bytes) as symbols:
                            result = prepare(*args, **kwargs)
                        self.assertEqual([call.args[0] for call in ihx.call_args_list],
                                         [original[0]] * (2 if mode == 'permanent' else 1))
                        self.assertEqual([call.args[0] for call in symbols.call_args_list],
                                         [original[1]] * (2 if mode == 'permanent' else 1))
                        return result
                    finally:
                        for path, raw in zip(paths, original): path.write_bytes(raw)
                def fake_flash(session, image, *args, phase_guard, payload_guard, **kwargs):
                    _, retained_payload, retained_backup = app.transport.session_image(
                        session, image, target_build_id=context.nvm_schema)
                    payload_guard(retained_payload, retained_backup)
                    calls.append('guard')
                    if corrupt:
                        path = session / 'images.json'
                        data = json.loads(path.read_bytes()); data['map_sha256'] = app.sha(b'different')
                        path.write_text(json.dumps(data), encoding='utf-8')
                    phase_guard('erase_and_flash')
                    payload_guard(retained_payload, retained_backup)
                    raise StopBeforeDevice()
                with patch.object(app, 'RECOVERY_REFERENCE', reference), \
                     patch.object(app, 'confirm_preparation'), \
                     patch.object(app, 'inventory', return_value=('OEM_APP', {'path': b'fake'})), \
                     patch.object(app, 'capture_native', return_value=bytes(stock)), \
                     patch.object(app, 'consent', return_value={}), \
                     patch.object(app, 'phase_guard', return_value=lambda *_a, **_kw: None), \
                     patch.object(app, 'prepare_trial', side_effect=swapped), \
                     patch.object(app.transport, 'flash', side_effect=fake_flash):
                    expected = ValueError if corrupt else StopBeforeDevice
                    with self.assertRaises(expected) as error:
                        app.install(Mock(folder=folder), Mock(), image=mode, context=context)
                if corrupt:
                    self.assertIn('Session build differs', str(error.exception))
                self.assertEqual(calls, ['guard'])
                session = folder / (mode + '-session')
                meta, payload, _ = app.transport.session_image(session, mode, target_build_id=context.nvm_schema)
                self.assertEqual(meta['ihx_sha256'], app.sha(original[0]))
                if not corrupt: self.assertEqual(meta['map_sha256'], app.sha(original[1]))
                for address, value in expected_code.items():
                    self.assertEqual(payload[address - app.packer.APP_START], value)
                self.assertEqual([path.read_bytes() for path in paths], original)

        # The real transport reads a valid but substituted session; a fake HID
        # raises on any access, so rejection must happen before even a reset.
        actual_prepare, actual_flash = app.prepare_trial, app.transport.flash
        actual_session_image = app.transport.session_image
        for mode in ('trial', 'permanent'):
            for attack in ('filled_code', 'entry_stub', 'backup', 'restore_after_read'):
                with self.subTest(mode=mode, attack=attack):
                    folder = self.root / (mode + '-' + attack); folder.mkdir()
                    restored = []
                    inside_flash = [False]
                    saved = {}
                    def prepare_changed(*args, **kwargs):
                        session, _ = actual_prepare(*args, **kwargs)
                        metadata_path = session / 'images.json'
                        metadata_bytes = metadata_path.read_bytes()
                        metadata = json.loads(metadata_bytes)
                        filename = app.transport.IMAGES[mode]
                        image_path = session / filename
                        image_bytes = image_path.read_bytes()
                        saved.update(session=session, meta=metadata_bytes, image=image_bytes, filename=filename)
                        if attack == 'backup':
                            changed = bytearray(stock); changed[0xA200] ^= 1
                            changed = bytes(changed)
                            (session / 'before-full-rom.bin').write_bytes(changed)
                            recovery = changed[app.packer.APP_START:app.packer.APP_END]
                            (session / 'restore-native.bin').write_bytes(recovery)
                            metadata['backup_sha256'] = app.sha(changed)
                            metadata['images']['restore-native.bin']['sha256'] = app.sha(recovery)
                            metadata['native_install_backup_sha256'] = app.sha(changed)
                            metadata['nvm_provenance']['source_sha256'] = app.sha(changed)
                        else:
                            changed = bytearray(image_bytes)
                            address = app.packer.APP_START if attack == 'entry_stub' else hole
                            changed[address - app.packer.APP_START] ^= 1
                            manifest_offset = app.packer.MANIFEST_START - app.packer.APP_START
                            changed[manifest_offset+16:manifest_offset+48] = bytes.fromhex(
                                app.sha(changed[:app.packer.CODE_END-app.packer.APP_START]))
                            changed = bytes(changed)
                            info = app.packer.verify_payload(changed, target_build_id=context.nvm_schema)
                            image_path.write_bytes(changed)
                            metadata['images'][filename].update(info)
                        metadata_path.write_text(json.dumps(metadata), encoding='utf-8')
                        if attack == 'restore_after_read':
                            saved['attack_image'] = image_path.read_bytes()
                            saved['attack_meta'] = metadata_path.read_bytes()
                            image_path.write_bytes(image_bytes)
                            metadata_path.write_bytes(metadata_bytes)
                        return session, app.transport.plan(session, mode, target_build_id=context.nvm_schema)
                    def session_read(*args, **kwargs):
                        result = actual_session_image(*args, **kwargs)
                        if inside_flash[0] and attack == 'restore_after_read' and not restored:
                            (saved['session'] / saved['filename']).write_bytes(saved['image'])
                            (saved['session'] / 'images.json').write_bytes(saved['meta'])
                            restored.append(True)
                        return result
                    def real_flash(*args, **kwargs):
                        inside_flash[0] = True
                        if attack == 'restore_after_read':
                            (saved['session'] / saved['filename']).write_bytes(saved['attack_image'])
                            (saved['session'] / 'images.json').write_bytes(saved['attack_meta'])
                        try:
                            return actual_flash(*args, **kwargs)
                        finally:
                            inside_flash[0] = False
                    def authorize(_log, plan, **_kwargs):
                        return {'image': mode, 'sha256': plan['sha256'], 'reset': True,
                                'erase': True, 'flash': True, 'restart': True}
                    with patch.object(app, 'RECOVERY_REFERENCE', reference), \
                         patch.object(app, 'confirm_preparation'), \
                         patch.object(app, 'inventory', return_value=('OEM_APP', {'path': b'fake'})), \
                         patch.object(app, 'capture_native', return_value=bytes(stock)), \
                         patch.object(app, 'consent', side_effect=authorize), \
                         patch.object(app, 'prepare_trial', side_effect=prepare_changed), \
                         patch.object(app.transport, 'session_image', side_effect=session_read), \
                         patch.object(app.transport, 'flash', side_effect=real_flash), \
                         patch.object(app.transport, 'hid_module', side_effect=AssertionError('HID forbidden')) as hid:
                        message = 'Recovery session differs' if attack == 'backup' else 'Session image differs'
                        with self.assertRaisesRegex(ValueError, message):
                            app.install(Mock(folder=folder), Mock(), image=mode, context=context)
                        hid.assert_not_called()
                    self.assertEqual(bool(restored), attack == 'restore_after_read')
                    if restored:
                        self.assertEqual((saved['session'] / saved['filename']).read_bytes(), saved['image'])
                        self.assertEqual((saved['session'] / 'images.json').read_bytes(), saved['meta'])

        # Run the actual transport through its loader identity command; stop at
        # the second payload guard before its fake erase command can be sent.
        from test_installer import TransportTests, descriptor
        for mode in ('trial', 'permanent'):
            with self.subTest(mode=mode, attack='erase_guard_handoff'):
                folder = self.root / (mode + '-real-transport'); folder.mkdir()
                hid = TransportTests.loader(self)
                hid.descriptors = [descriptor('OEM_APP')]
                guards = []
                class Native:
                    def rom(self, _start, _size): return bytes(stock)
                    def enter_native_loader(self): hid.descriptors = [descriptor('LOADER')]
                    def close(self): pass
                def flash_to_guard(*args, payload_guard, **kwargs):
                    def check(payload, session_backup):
                        guards.append((payload, session_backup))
                        payload_guard(payload, session_backup)
                        if len(guards) == 2: raise StopBeforeDevice()
                    return actual_flash(*args, payload_guard=check, **kwargs)
                def authorize(_log, plan, **_kwargs):
                    return {'image': mode, 'sha256': plan['sha256'], 'reset': True,
                            'erase': True, 'flash': True, 'restart': True}
                with patch.object(app, 'RECOVERY_REFERENCE', reference), \
                     patch.object(app, 'confirm_preparation'), \
                     patch.object(app, 'capture_native', return_value=bytes(stock)), \
                     patch.object(app, 'consent', side_effect=authorize), \
                     patch.object(app.transport, 'flash', side_effect=flash_to_guard), \
                     patch.object(app.transport, 'hid_module', return_value=hid), \
                     patch.object(app.transport, 'Application', return_value=Native()), \
                     patch.object(app.transport.time, 'sleep'):
                    with self.assertRaises(StopBeforeDevice):
                        app.install(Mock(folder=folder), hid, image=mode, context=context)
                self.assertEqual(hid.commands, [1])
                self.assertEqual(len(guards), 2)
                self.assertIs(guards[0][0], guards[1][0])
                self.assertIs(guards[0][1], guards[1][1])
                self.assertEqual(guards[0][1], bytes(stock))

        # Complete real transport against a fake loader, including a midflight
        # session replacement after the initial payload read and before erase.
        for mode in ('trial', 'permanent'):
            for substitute in (False, True):
                with self.subTest(mode=mode, midflight_substitution=substitute):
                    folder = self.root / (mode + '-program-' + str(substitute)); folder.mkdir()
                    session = folder / (mode + '-session')
                    hid = TransportTests.loader(self)
                    hid.descriptors = [descriptor('OEM_APP')]
                    guarded = []
                    class Native:
                        def rom(self, _start, _size): return bytes(stock)
                        def enter_native_loader(self):
                            if substitute:
                                filename = app.transport.IMAGES[mode]
                                path = session / filename
                                changed = bytearray(path.read_bytes())
                                changed[0] ^= 1
                                offset = app.packer.MANIFEST_START - app.packer.APP_START
                                changed[offset+16:offset+48] = bytes.fromhex(
                                    app.sha(changed[:app.packer.CODE_END-app.packer.APP_START]))
                                changed = bytes(changed)
                                info = app.packer.verify_payload(changed, target_build_id=context.nvm_schema)
                                metadata_path = session / 'images.json'
                                metadata = json.loads(metadata_path.read_bytes())
                                metadata['images'][filename].update(info)
                                path.write_bytes(changed)
                                metadata_path.write_text(json.dumps(metadata), encoding='utf-8')
                            hid.descriptors = [descriptor('LOADER')]
                        def close(self): pass
                    def recording_flash(*args, payload_guard, **kwargs):
                        def check(payload, session_backup):
                            guarded.append((payload, session_backup))
                            payload_guard(payload, session_backup)
                        return actual_flash(*args, payload_guard=check, **kwargs)
                    def authorize(_log, plan, **_kwargs):
                        return {'image': mode, 'sha256': plan['sha256'], 'reset': True,
                                'erase': True, 'flash': True, 'restart': True}
                    with patch.object(app, 'RECOVERY_REFERENCE', reference), \
                         patch.object(app, 'confirm_preparation'), \
                         patch.object(app, 'capture_native', return_value=bytes(stock)), \
                         patch.object(app, 'consent', side_effect=authorize), \
                         patch.object(app.transport, 'flash', side_effect=recording_flash), \
                         patch.object(app.transport, 'hid_module', return_value=hid), \
                         patch.object(app.transport, 'Application', return_value=Native()), \
                         patch.object(app.transport.time, 'sleep'), \
                         patch.object(app, 'wait_state', side_effect=StopBeforeDevice()):
                        with self.assertRaises(ValueError if substitute else StopBeforeDevice):
                            app.install(Mock(folder=folder), hid, image=mode, context=context)
                    if substitute:
                        self.assertEqual(hid.commands, [1])
                        self.assertEqual(len(guarded), 1)
                        continue
                    self.assertEqual(hid.commands, [1, 2, 3, 4, 5])
                    self.assertEqual(len(guarded), 2)
                    self.assertIs(guarded[0][0], guarded[1][0])
                    payload = guarded[0][0]
                    self.assertEqual(payload, app.expected_install_payload(context, bytes(stock), mode, bytes(stock)))
                    self.assertEqual(guarded[0][1], bytes(stock))
                    blocks = len(payload) // 64
                    self.assertEqual(b''.join(packet[1:] for packet in hid.writes[3:3+blocks]), payload)
                    disk_payload = (session / app.transport.IMAGES[mode]).read_bytes()
                    self.assertEqual(disk_payload != payload, substitute)

        # Change all diagnostic files only after release revalidation; the
        # post-flash diagnostic must still consume the approved snapshot.
        session = self.root / 'trial-good/trial-session'
        report_path = self.bundle / 'reports/build-report.json'
        report_bytes = report_path.read_bytes()
        def replace_before_diagnostic(*_args, **_kwargs):
            for path in [*paths, report_path]: path.write_bytes(b'substituted after revalidation')
        try:
            with patch.object(app, 'require_state', side_effect=replace_before_diagnostic), \
                 patch.object(app, 'boot_status'), patch.object(app, 'keyboard_smoke', return_value=True), \
                 patch.object(app.diagnostic, 'diagnostic_build_bytes', wraps=app.diagnostic.diagnostic_build_bytes) as diag, \
                 patch.object(app.diagnostic, 'capture', side_effect=StopBeforeDevice()):
                with self.assertRaises(StopBeforeDevice):
                    app.verify_trial(Mock(folder=self.root), Mock(), session, {'path': b'fake'}, image='trial', context=context)
            self.assertEqual(diag.call_args.args, (original[0], original[1], report_bytes))
        finally:
            for path, raw in zip([*paths, report_path], [*original, report_bytes]): path.write_bytes(raw)

    def test_missing_and_symlink_follow_original_path_behavior(self):
        target = self.bundle / 'firmware/application.mem'
        data = target.read_bytes()
        target.unlink()
        with self.assertRaises(FileNotFoundError):
            app._load_release(self.bundle, self.approval, approved=True)
        other = self.root / 'linked-mem'; other.write_bytes(data)
        try: target.symlink_to(other)
        except (OSError, NotImplementedError): self.skipTest('symlinks unavailable')
        self.assertEqual(app._load_release(self.bundle, self.approval, approved=True), self.manifest)
        other.write_bytes(b'corrupted')
        with self.assertRaisesRegex(ValueError, 'modified or corrupted'):
            app._load_release(self.bundle, self.approval, approved=True)

    def test_traversal_malformed_and_approval(self):
        self.manifest['files']['../escape'] = {'size': 0, 'sha256': app.sha(b'')}
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'unexpected release contents'):
            app._load_release(self.bundle, self.approval, approved=True)
        del self.manifest['files']['../escape']; self.save_manifest()
        self.approval.write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Approval does not match'):
            app._load_release(self.bundle, self.approval, approved=True)
        (self.bundle / 'installer-release.json').write_bytes(b'{')
        with self.assertRaises(json.JSONDecodeError):
            app._load_release(self.bundle, self.approval, approved=False)


if __name__ == '__main__':
    unittest.main()
