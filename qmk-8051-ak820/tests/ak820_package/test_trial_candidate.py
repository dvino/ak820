#!/usr/bin/env python3
"""Trial-only offline packaging: preserve personal recovery and physical NVM."""
import json
from pathlib import Path
from unittest.mock import patch

import test_preparation as preparation
import prepare_ak820_trial as trial_builder
import pack_ak820 as packer
import ak820_tool as updater


class TrialCandidateTest(preparation.PreparationTest):
    # Reuse the recovery fixture and its fake hardware without inheriting its
    # tests a second time in the final test count.
    def setUp(self):
        super().setUp()
        native_reference = self.native
        backup = bytearray(self.backup)
        backup[0xA040] = 0  # The supported native migration profile.
        self.backup = bytes(backup)
        self.native = self.backup[packer.APP_START:packer.APP_END]
        (self.session / 'before-full-rom.bin').write_bytes(self.backup)
        (self.session / updater.IMAGES['restore']).write_bytes(self.native)
        self.manifest['backup_sha256'] = packer.digest(self.backup)
        self.manifest['images'][updater.IMAGES['restore']]['sha256'] = packer.digest(self.native)
        self.save_manifest()
        self.nativepath = self.root / 'reference/native-installed.bin'
        self.nativepath.write_bytes(native_reference)
        self.stack.enter_context(patch.object(packer, 'NATIVE_SHA', packer.digest(native_reference)))

    def build_trial(self, out):
        return trial_builder.write_trial(self.ihx, self.mapfile,
            self.root / 'reference/stock-full.bin', self.nativepath,
            self.backup, out, current_rom=bytes(self.live), current_trial=self.payloads['trial'])

    def test_trial_only_preserves_current_nvm_and_original_recovery(self):
        self.completed_save()
        self.live[packer.NVM_START:packer.NVM_START + 2] = bytes.fromhex('e6fe')
        self.live[packer.NVM_START + 37:packer.NVM_START + 40] = packer.BUILD_ID.to_bytes(3, 'little')
        before = self.session_bytes()
        out = self.root / 'candidate'
        metadata = self.build_trial(out)
        self.assertEqual(self.session_bytes(), before)
        self.assertFalse((out / updater.IMAGES['permanent']).exists())
        self.assertNotIn(updater.IMAGES['permanent'], metadata['images'])
        self.assertTrue(metadata['trial_only'])
        _, payload, backup = updater.session_image(out, 'trial')
        self.assertEqual(backup, self.backup)
        self.assertEqual(payload[packer.NVM_START - packer.APP_START:packer.NVM_END - packer.APP_START],
                         self.live[packer.NVM_START:packer.NVM_END])
        self.assertEqual(payload[packer.NVM_END - packer.APP_START:packer.MANIFEST_START - packer.APP_START], bytes(128))
        self.assertEqual((out / updater.IMAGES['restore']).read_bytes(), self.native)
        self.application.assert_not_called()
        self.hid.assert_not_called()

    def test_trial_candidate_rejects_journal_before_creating_output(self):
        self.live[packer.NVM_END + 64] = 0xA5
        out = self.root / 'rejected'
        with self.assertRaisesRegex(ValueError, 'journal header'):
            self.build_trial(out)
        self.assertFalse(out.exists())
        self.application.assert_not_called()

    def test_trial_candidate_rejects_wrong_code_and_schema(self):
        out = self.root / 'rejected'
        self.live[packer.NVM_START+37] ^= 1
        with self.assertRaisesRegex(ValueError, 'magic/schema'):
            self.build_trial(out)
        self.live[packer.CODE_START] ^= 1
        with self.assertRaisesRegex(ValueError, 'code/readback'):
            self.build_trial(out)
        self.assertFalse(out.exists())
        self.application.assert_not_called()


# unittest discovers inherited test methods; keep only the three new cases
# while using the existing fixture setup and helpers.
for _name in dir(preparation.PreparationTest):
    if _name.startswith('test_'):
        setattr(TrialCandidateTest, _name, None)
