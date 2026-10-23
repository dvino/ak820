#!/usr/bin/env python3
"""Legacy readback -> current trial: lossless migration before any output/USB.

The old package is a synthetic format fixture, not an executable rc3 image.
Startup CPU correctness has its own independently generated instruction tests.
"""
import test_trial_candidate as candidate
from test_entropy_schema import legacy_nvm
import pack_ak820 as packer
import ak820_tool as updater


class LegacyTrialMigrationTest(candidate.TrialCandidateTest):
    def use_legacy(self, nvm):
        payload = bytearray(self.payloads['trial'])
        payload[packer.NVM_START - packer.APP_START:packer.NVM_END - packer.APP_START] = nvm
        manifest = packer.MANIFEST_START - packer.APP_START
        payload[manifest + 12:manifest + 16] = packer.LEGACY_BUILD_ID.to_bytes(4, 'little')
        payload[manifest + 48:manifest + 64] = bytes.fromhex(packer.digest(nvm))[:16]
        self.payloads['trial'] = bytes(payload)
        self.live[packer.APP_START:packer.APP_END] = payload
        return bytes(payload)

    def test_legacy_package_is_readable_only_with_explicit_legacy_policy(self):
        old = self.use_legacy(legacy_nvm())
        with self.assertRaisesRegex(ValueError, 'Unknown application manifest'):
            packer.verify_payload(old)
        self.assertEqual(packer.verify_payload(old, allow_legacy=True)['build_id'], 0x082001)
        updater.verify_live(self.live, old, 'trial', self.stock)
        self.hid.assert_not_called()

    def test_legacy_trial_preserves_live_macros_and_original_recovery(self):
        self.use_legacy(legacy_nvm())
        live_nvm = legacy_nvm(b'edited on keyboard\0' + b'\x01\x05\x01\xff\0' + bytes(14))
        self.live[packer.NVM_START:packer.NVM_END] = live_nvm
        expected, _ = packer.migrate_vial_nvm(live_nvm, 0x082001)
        source_files = self.session_bytes()
        out = self.root / 'migrated'
        metadata = self.build_trial(out)
        _, new_payload, backup = updater.session_image(out, 'trial')
        self.assertEqual(new_payload[packer.NVM_START - packer.APP_START:packer.NVM_END - packer.APP_START], expected)
        self.assertEqual(backup, self.backup)
        self.assertEqual((out / updater.IMAGES['restore']).read_bytes(), self.native)
        self.assertEqual(self.session_bytes(), source_files)
        self.assertEqual(metadata['migration']['source_build_id'], 0x082001)
        self.assertEqual(metadata['migration']['target_build_id'], 0x082002)
        self.assertFalse((out / updater.IMAGES['permanent']).exists())
        self.application.assert_not_called()
        self.hid.assert_not_called()

    def test_oversized_macro_content_stops_before_creating_output(self):
        self.use_legacy(legacy_nvm())
        self.live[packer.NVM_START:packer.NVM_END] = legacy_nvm(b'A' * (8193 - 16) + bytes(16))
        source_files = self.session_bytes()
        before = bytes(self.live)
        out = self.root / 'oversize-rejected'
        with self.assertRaisesRegex(ValueError, 'Nothing was truncated or written'):
            self.build_trial(out)
        self.assertFalse(out.exists())
        self.assertEqual(self.live, before)
        self.assertEqual(self.session_bytes(), source_files)
        self.application.assert_not_called()
        self.hid.assert_not_called()


for _name in dir(candidate.TrialCandidateTest):
    if _name.startswith('test_'):
        setattr(LegacyTrialMigrationTest, _name, None)
