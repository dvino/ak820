"""Approved schema propagation through offline transport admission; no HID."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import ak820 as host
import test_settings_backup as model

p = host.packer
t = host.transport


class TransportSchemaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        source = model.synthetic_profile()
        self.backup = source['backup']
        self.payload = bytearray(source['payload'])
        nvm, _ = p.migrate_vial_nvm(model.base_nvm(), p.BUILD_ID, target_build_id=p.EXTENSION_BUILD_ID)
        self.payload[p.NVM_START-p.APP_START:p.NVM_END-p.APP_START] = nvm
        self.payload[p.MANIFEST_START-p.APP_START+12:p.MANIFEST_START-p.APP_START+16] = p.EXTENSION_BUILD_ID.to_bytes(4,'little')
        self.payload[-16:] = bytes.fromhex(p.digest(nvm))[:16]
        self.payload = bytes(self.payload)
        recovery = self.backup[p.APP_START:p.APP_END]
        (self.folder/'before-full-rom.bin').write_bytes(self.backup)
        (self.folder/'restore-native.bin').write_bytes(recovery)
        (self.folder/'ak820-vial-permanent.bin').write_bytes(self.payload)
        self.manifest = {'backup_sha256': p.digest(self.backup), 'images': {
            'restore-native.bin': {'sha256': p.digest(recovery), 'size': len(recovery)},
            'ak820-vial-permanent.bin': {'sha256':p.digest(self.payload), 'size':len(self.payload)}},
            'ihx_sha256':'test-ihx','map_sha256':'test-map'}
        self.save()

    def save(self):
        (self.folder/'images.json').write_text(json.dumps(self.manifest))

    def test_explicit_schema3_session_and_plan_and_wrong_schema_fail_closed(self):
        self.assertEqual(t.session_image(self.folder,'permanent',target_build_id=p.EXTENSION_BUILD_ID)[1], self.payload)
        self.assertEqual(t.plan(self.folder,'permanent',target_build_id=p.EXTENSION_BUILD_ID)['sha256'], p.digest(self.payload))
        self.manifest['nvm_schema'] = p.EXTENSION_BUILD_ID
        self.save()
        with self.assertRaisesRegex(ValueError,'Unknown application manifest'):
            t.session_image(self.folder,'permanent')
        with self.assertRaisesRegex(ValueError,'Unknown application manifest'):
            t.flash(self.folder,'permanent',False,False)

    def test_schema3_readback_uses_explicit_expected_schema(self):
        live = bytearray(self.backup)
        live[p.APP_START:p.APP_END] = self.payload
        with patch.object(t,'validate_native'):
            t.verify_live(bytes(live),self.payload,'permanent',self.backup,target_build_id=p.EXTENSION_BUILD_ID)
            with self.assertRaisesRegex(ValueError,'Unknown application manifest'):
                t.verify_live(bytes(live),self.payload,'permanent',self.backup)

    def test_prepared_update_forwards_exact_schema_before_reviewed_pins(self):
        pins={'ihx_sha256':'test-ihx','map_sha256':'test-map','payload':p.digest(self.payload),'backup':p.digest(self.backup)}
        with patch.object(t,'UPDATE_PINS',pins):
            self.assertEqual(t.validate_prepared_update(self.folder,target_build_id=p.EXTENSION_BUILD_ID)[1],self.payload)
            with self.assertRaisesRegex(ValueError,'Unknown application manifest'):
                t.validate_prepared_update(self.folder)

    def test_flash_schema3_reaches_local_guard_checks_without_hid(self):
        with patch.object(t,'validate_native'), patch.object(t,'hid_module',side_effect=AssertionError('HID forbidden')), \
             patch.object(t,'Application',side_effect=AssertionError('Device open forbidden')):
            # Missing references fail after schema admission, before any USB access.
            with self.assertRaises(FileNotFoundError):
                t.flash(self.folder,'permanent',False,False,reference_dir=self.folder,target_build_id=p.EXTENSION_BUILD_ID)

if __name__ == '__main__': unittest.main()
