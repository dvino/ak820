"""Synthetic transport checks; these do not qualify an image or a physical device."""
import copy
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import time
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent / 'installer'))
import test_settings_backup as model
import ak820_device_protocol as protocol
from ak820_device_protocol import DeviceAPI


class Wire(model.WireDevice):
    def raw(self, packet):
        if packet[:2] in (b'\x07\x43', b'\x07\x44', b'\x07\x45', b'\x07\x46'):
            self.requests.append(packet)
            self.writes.append(packet)
            return packet[:2] + b'\0' + packet[3:]
        return super().raw(packet)


class ApprovedInputs(unittest.TestCase):
    def test_fresh_approved_snapshot_and_catalog_are_required(self):
        profile = model.synthetic_profile()
        snapshot = SimpleNamespace(host_files={'tools/installer/settings-catalog.json': b'{}'}, files={})
        installer = SimpleNamespace(_release_snapshot=Mock(return_value=snapshot))
        settings = SimpleNamespace(load_profile=Mock(return_value=profile))
        spec = SimpleNamespace(loader=SimpleNamespace(exec_module=Mock()))
        checked = {'release': 'synthetic', 'backup': profile['backup'], 'payload': profile['payload']}
        with patch.object(protocol, 'bind', return_value=checked), \
             patch.object(protocol, '_installer', return_value=installer), \
             patch.object(protocol.importlib.util, 'spec_from_file_location', return_value=spec), \
             patch.object(protocol.importlib.util, 'module_from_spec', return_value=settings):
            found_settings, found = protocol._approved_write_profile(('release', 'recovery', 'approval'))
            self.assertIs(found_settings, settings)
            self.assertIs(found, profile)
            self.assertTrue(installer._release_snapshot.call_args.kwargs['approved'])
            self.assertEqual(settings.load_profile.call_args.kwargs['trusted_catalog'], {})
            snapshot.host_files.clear()
            with self.assertRaisesRegex(ValueError, 'catalog is missing'):
                protocol._approved_write_profile(('release', 'recovery', 'approval'))
            snapshot.host_files['tools/installer/settings-catalog.json'] = b'{}'
            checked['payload'] = b'stale'
            with self.assertRaisesRegex(ValueError, 'payload changed'):
                protocol._approved_write_profile(('release', 'recovery', 'approval'))


class WriteIdentity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.profile = model.synthetic_profile()
        self.profile['settings_record_version'] = 2
        self.wire = Wire(self.profile)
        self.api = DeviceAPI({}, Path(self.temp.name), lambda: self.wire, allow_writes=True,
                             verification=('release', 'recovery', 'approval'))
        self.addCleanup(self.api.close)
        self.approved = patch('ak820_device_protocol._approved_write_profile',
                              side_effect=lambda paths: (model.settings, copy.deepcopy(self.profile)))
        self.get_profile = self.approved.start()
        self.addCleanup(self.approved.stop)

    def test_raw_writes_revalidate_per_transaction(self):
        self.api.exchange(self.api.packet(9))
        self.api.exchange(self.api.packet(9))
        self.assertEqual(len(self.wire.writes), 2)
        self.assertEqual(self.get_profile.call_count, 2)
        self.assertGreater(sum(p[0] == 253 for p in self.wire.requests), 4000)

    def test_mutated_code_and_manifest_fail_before_write(self):
        for at in (model.p.APP_START, model.p.MANIFEST_START):
            with self.subTest(address=at):
                self.wire.rom_patch[at] = self.wire.rom()[at] ^ 1
                with self.assertRaises(ValueError):
                    self.api.exchange(self.api.packet(9))
                self.assertEqual(self.wire.writes, [])
                self.wire.rom_patch.clear()

    def test_unapproved_and_v3_fail_before_write(self):
        self.get_profile.side_effect = ValueError('stale approval')
        with self.assertRaisesRegex(ValueError, 'stale approval'):
            self.api.exchange(self.api.packet(9))
        self.get_profile.side_effect = lambda paths: (model.settings, dict(self.profile, settings_record_version=3))
        with self.assertRaisesRegex(ValueError, 'qualification and identity gates are pending'):
            self.api.exchange(self.api.packet(9))
        self.assertEqual(self.wire.writes, [])

    def test_direct_one_preflight_for_begin_chunks_commit(self):
        begin = self.api.packet(7, 0x43, 1, 82, 7, 0, 0, 0, 0, 0)
        chunk = self.api.packet(7, 0x44, 7, 0, 0, 1, 9)
        commit = self.api.packet(7, 0x45, 7, 0)
        for packet in (begin, chunk, commit):
            self.api.exchange(packet)
        self.assertEqual(self.get_profile.call_count, 1)
        self.assertEqual(len(self.wire.writes), 3)
        self.assertIsNone(self.api._verified_handle)
        with self.assertRaisesRegex(ValueError, 'no verified begin'):
            self.api.exchange(chunk)
        self.assertEqual(len(self.wire.writes), 3)

    def test_direct_frame_preserves_full_upload_without_rechecking_chunks(self):
        with patch.object(self.api, 'direct_info', return_value={'supported': True}), \
             patch.object(self.api, '_direct_status', return_value={
                 'frame_id': 7, 'coverage': 82, 'generation': 5, 'state': 2}):
            self.api.set_direct_frame(bytes(246), frame_id=7, expected_generation=4)
        self.assertEqual(self.get_profile.call_count, 1)
        self.assertEqual(len(self.wire.writes), 13)
        self.assertEqual([p[1] for p in self.wire.writes], [0x43] + [0x44] * 11 + [0x45])

    def test_direct_rejection_and_expiry_invalidate(self):
        begin = self.api.packet(7, 0x43, 1, 82, 7, 0, 0, 0, 0, 0)
        chunk = self.api.packet(7, 0x44, 7, 0, 0, 1, 9)
        self.api.exchange(begin)
        self.api._direct_active = (b'\x07\x00', time.monotonic() - 1)
        with self.assertRaisesRegex(ValueError, 'expired'):
            self.api.exchange(chunk)
        self.api.exchange(begin)
        with patch.object(self.api.app, 'raw', return_value=bytes((7, 0x44, 1)) + chunk[3:]):
            self.api.exchange(chunk)
        self.assertIsNone(self.api._verified_handle)
        with self.assertRaisesRegex(ValueError, 'no verified begin'):
            self.api.exchange(chunk)

    def test_mutated_binding_during_direct_cannot_authorize_chunk(self):
        self.api.exchange(self.api.packet(7, 0x43, 1, 82, 7, 0, 0, 0, 0, 0))
        self.api.binding['settings_record_version'] = 1
        with self.assertRaisesRegex(ValueError, 'binding changed'):
            self.api.exchange(self.api.packet(7, 0x44, 7, 0, 0, 1, 9))
        self.assertEqual(len(self.wire.writes), 1)

    def test_marker_changed_during_direct_is_detected_at_next_boundary(self):
        begin = self.api.packet(7, 0x43, 1, 82, 7, 0, 0, 0, 0, 0)
        chunk = self.api.packet(7, 0x44, 7, 0, 0, 1, 9)
        commit = self.api.packet(7, 0x45, 7, 0)
        self.api.exchange(begin)
        self.wire.rom_patch[0x27c0] = 0
        self.api.exchange(chunk)
        self.api.exchange(commit)
        with self.assertRaises(ValueError):
            self.api.exchange(self.api.packet(9))
        self.assertEqual(len(self.wire.writes), 3)

    def test_direct_handle_change_or_transport_error_invalidates(self):
        begin = self.api.packet(7, 0x43, 1, 82, 7, 0, 0, 0, 0, 0)
        chunk = self.api.packet(7, 0x44, 7, 0, 0, 1, 9)
        self.api.exchange(begin)
        original = self.api.app
        self.api.app = Wire(self.profile)
        with self.assertRaises(ValueError):
            self.api.exchange(chunk)
        self.assertEqual(self.api.app.writes, [])
        self.api.app = original
        self.api.exchange(begin)
        with patch.object(original, 'raw', side_effect=OSError('transport fault')):
            with self.assertRaisesRegex(OSError, 'transport fault'):
                self.api.exchange(chunk)
        self.assertIsNone(self.api._verified_handle)
        with self.assertRaises(ValueError):
            self.api.exchange(chunk)


if __name__ == '__main__':
    unittest.main()
