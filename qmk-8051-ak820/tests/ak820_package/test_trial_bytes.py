"""Offline parity of path and retained-byte trial preparation."""
import test_trial_candidate as candidate
import prepare_ak820_trial as trial_builder


class TrialBytesTest(candidate.TrialCandidateTest):
    def test_path_and_bytes_produce_same_sessions(self):
        self.completed_save()
        ihx, map_bytes = self.ihx.read_bytes(), self.mapfile.read_bytes()
        stock = self.root / 'reference/stock-full.bin'
        current = {'current_rom': bytes(self.live), 'current_trial': self.payloads['trial']}
        path_dir, bytes_dir = self.root / 'migration-path', self.root / 'migration-bytes'
        path_info = trial_builder.write_trial(self.ihx, self.mapfile, stock, self.nativepath,
                                               self.backup, path_dir, **current)
        byte_info = trial_builder.write_trial_bytes(ihx, map_bytes, stock, self.nativepath,
                                                     self.backup, bytes_dir, **current)
        self.assertEqual(path_info, byte_info)
        for name in ('images.json', 'ak820-vial-trial.bin', 'restore-native.bin', 'before-full-rom.bin'):
            self.assertEqual((path_dir / name).read_bytes(), (bytes_dir / name).read_bytes())

    def test_invalid_bytes_do_not_create_output(self):
        out = self.root / 'bad'
        with self.assertRaises(ValueError):
            trial_builder.write_trial_bytes(b'invalid', self.mapfile.read_bytes(),
                self.root / 'reference/stock-full.bin', self.nativepath, self.backup, out)
        self.assertFalse(out.exists())


for _name in dir(candidate.TrialCandidateTest):
    if _name.startswith('test_'):
        setattr(TrialBytesTest, _name, None)
