#!/usr/bin/env python3
"""Offline journal and trial-provenance regressions for the production updater.

Synthetic references and a fake Application replace every physical operation.
The HID import function raises immediately if a test reaches it.
"""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'util'))
import ak820_tool as updater
import pack_ak820 as packer
from startup_fixture import add_startup_fixture
from oem_fixture import make_synthetic_oem, patch_synthetic_oem


def ihex(data):
    records = []
    for address, value in sorted(data.items()):
        record = bytes((1, address >> 8, address & 255, 0, value))
        records.append(':' + (record + bytes((-sum(record) & 255,))).hex())
    return '\n'.join(records + [':00000001FF']) + '\n'


class PreparationTest(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory(prefix='ak820-preparation-')))
        self.session = self.root / 'session'
        for subdir in ('session', 'firmware', 'reference'):
            (self.root / subdir).mkdir()
        self.stock, self.native, _, _ = make_synthetic_oem()
        self.backup = self.stock
        self.stack.enter_context(patch.object(updater, 'ROOT', self.root))
        patch_synthetic_oem(self.stack, updater, self.stock)
        (self.root / 'reference/stock-full.bin').write_bytes(self.stock)
        self.symbols = {name: packer.CODE_START + 3 + i for i, name in enumerate((
            '__sdcc_gsinit_startup', '_USB_DeviceInterrupt', '_ak820_timer_irq',
            '_ak820_led_irq', '_keymaps', '_encoder_map'))}
        self.data = dict(enumerate(packer.ljmp(self.symbols['__sdcc_gsinit_startup']), packer.CODE_START))
        self.data.update({address: 0x22 for address in self.symbols.values()})
        add_startup_fixture(self.data, self.symbols)
        self.ihx = self.root / 'firmware/application.ihx'
        self.mapfile = self.root / 'firmware/application.map'
        self.write_build_inputs()
        self.manifest = {'backup_sha256': packer.digest(self.backup), 'images': {},
                         'ihx_sha256': packer.digest(self.ihx.read_bytes()),
                         'map_sha256': packer.digest(self.mapfile.read_bytes())}
        self.payloads = {name: packer.pack(self.data, self.symbols, self.stock,
                         bytes(packer.empty_nvm()), trial)
                         for name, trial in (('trial', True), ('permanent', False))}
        self.payloads['restore'] = self.native
        for name, payload in self.payloads.items():
            filename = updater.IMAGES[name]
            (self.session / filename).write_bytes(payload)
            self.manifest['images'][filename] = {'sha256': packer.digest(payload), 'size': len(payload)}
        (self.session / 'before-full-rom.bin').write_bytes(self.backup)
        self.save_manifest()
        self.live = bytearray(self.stock)
        self.live[packer.APP_START:packer.APP_END] = self.payloads['trial']
        self.live[0x27c0:packer.APP_START] = bytes(64)
        owner = self

        class FakeApplication:
            native = False
            closed = False

            def rom(self, address, size):
                return bytes(owner.live[address:address + size])

            def close(self):
                self.closed = True

        self.app = FakeApplication()
        self.application = self.stack.enter_context(patch.object(updater, 'Application', return_value=self.app))
        self.hid = self.stack.enter_context(patch.object(
            updater, 'hid_module', side_effect=AssertionError('Physical HID access is forbidden in this test')))
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))

    def write_build_inputs(self):
        self.ihx.write_text(ihex(self.data))
        self.mapfile.write_text(''.join(f'C: {address:08X} {name}\n' for name, address in self.symbols.items()))

    def save_manifest(self):
        (self.session / 'images.json').write_text(json.dumps(self.manifest))

    def session_bytes(self):
        return {path.name: path.read_bytes() for path in self.session.iterdir()}

    def completed_save(self):
        page = bytes(range(1, 65))
        self.live[packer.NVM_START + 0x40:packer.NVM_START + 0x80] = page
        self.live[packer.NVM_END:packer.NVM_END + 64] = page
        self.assertEqual(self.live[packer.NVM_END + 64:packer.MANIFEST_START], bytes(64))

    def reject_unchanged(self, message):
        before = self.session_bytes()
        with self.assertRaisesRegex(ValueError, message):
            updater.prepare_permanent(self.session)
        self.assertEqual(self.session_bytes(), before)
        self.application.assert_not_called()
        self.hid.assert_not_called()

    def test_live_verification_accepts_completed_journal_with_retained_data(self):
        self.completed_save()
        updater.verify_live(bytes(self.live), self.payloads['trial'], 'trial', self.stock)
        self.hid.assert_not_called()

    def test_live_verification_rejects_nonempty_header_including_partial_clear(self):
        self.completed_save()
        for offset in (0, 1, 8, 63):
            with self.subTest(header_offset=offset):
                changed = bytearray(self.live)
                changed[packer.NVM_END + 64 + offset] = 0xa5
                with self.assertRaisesRegex(ValueError, 'journal header'):
                    updater.verify_live(changed, self.payloads['trial'], 'trial', self.stock)

    def test_fresh_installation_still_requires_both_journal_pages_zero(self):
        for address in (packer.NVM_END, packer.NVM_END + 63, packer.NVM_END + 64, packer.MANIFEST_START - 1):
            with self.subTest(address=hex(address)):
                changed = bytearray(self.payloads['trial'])
                changed[address - packer.APP_START] = 1
                with self.assertRaisesRegex(ValueError, 'Journal must be empty'):
                    packer.verify_payload(changed)

    def test_matching_trial_preserves_live_settings_code_and_original_recovery(self):
        self.completed_save()
        before = self.session_bytes()
        updater.prepare_permanent(self.session)
        permanent = (self.session / updater.IMAGES['permanent']).read_bytes()
        info = packer.verify_payload(permanent)
        self.assertFalse(info['trial'])
        self.assertEqual(permanent[packer.NVM_START - packer.APP_START:packer.NVM_END - packer.APP_START],
                         self.live[packer.NVM_START:packer.NVM_END])
        self.assertEqual(permanent[packer.ERASE_START - packer.APP_START:packer.CODE_END - packer.APP_START],
                         self.payloads['trial'][packer.ERASE_START - packer.APP_START:packer.CODE_END - packer.APP_START])
        self.assertEqual(permanent[packer.NVM_END - packer.APP_START:packer.MANIFEST_START - packer.APP_START], bytes(128))
        for name in ('before-full-rom.bin', 'restore-native.bin', updater.IMAGES['trial']):
            self.assertEqual((self.session / name).read_bytes(), before[name])
        manifest = json.loads((self.session / 'images.json').read_text())
        self.assertEqual(manifest['permanent_prepared_from_verified_trial'], packer.digest(self.live))
        self.assertEqual(manifest['images'][updater.IMAGES['permanent']], info)
        self.assertTrue(self.app.closed)
        self.hid.assert_not_called()

    def test_different_valid_ihx_rejected_before_open_or_file_change(self):
        self.data[self.symbols['_keymaps']] ^= 1
        self.write_build_inputs()
        self.reject_unchanged('build identity.*application.ihx')

    def test_different_valid_map_rejected_before_open_or_file_change(self):
        self.symbols['_USB_DeviceInterrupt'] = self.symbols['_ak820_timer_irq']
        self.write_build_inputs()
        self.reject_unchanged('build identity.*application.map')

    def test_missing_build_identity_rejected_before_open_or_file_change(self):
        for key in ('ihx_sha256', 'map_sha256'):
            with self.subTest(key=key):
                value = self.manifest.pop(key)
                self.save_manifest()
                self.reject_unchanged('build identity')
                self.manifest[key] = value

    def test_rehashed_changed_code_still_must_reproduce_the_trial(self):
        self.data[self.symbols['_keymaps']] ^= 1
        self.write_build_inputs()
        self.manifest['ihx_sha256'] = packer.digest(self.ihx.read_bytes())
        self.save_manifest()
        self.reject_unchanged('do not reproduce the session trial')

    def test_rehashed_changed_callbacks_still_must_reproduce_the_trial(self):
        self.symbols['_USB_DeviceInterrupt'] = self.symbols['_ak820_timer_irq']
        self.write_build_inputs()
        self.manifest['map_sha256'] = packer.digest(self.mapfile.read_bytes())
        self.save_manifest()
        self.reject_unchanged('do not reproduce the session trial')

    def test_old_restore_session_needs_no_build_inputs_or_new_metadata(self):
        self.manifest.pop('ihx_sha256')
        self.manifest.pop('map_sha256')
        self.save_manifest()
        self.ihx.unlink()
        self.mapfile.unlink()
        _, recovery, backup = updater.session_image(self.session, 'restore')
        self.assertEqual(recovery, self.native)
        self.assertEqual(backup, self.backup)
        plan = updater.plan(self.session, 'restore')
        self.assertEqual(plan['sha256'], packer.digest(self.native))
        self.assertEqual(plan['data_blocks'], 799)
        self.assertFalse(plan['usb_opened'])
        self.application.assert_not_called()
        self.hid.assert_not_called()


if __name__ == '__main__':
    unittest.main()
