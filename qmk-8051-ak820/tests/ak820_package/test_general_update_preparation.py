"""Synthetic offline preparation; no hardware freshness claim."""
import json
from unittest.mock import patch

import test_preparation as fixture
from test_entropy_schema import legacy_nvm
import pack_ak820 as packer
import ak820_tool as updater
import prepare_ak820_update as builder


class GeneralUpdateTest(fixture.PreparationTest):
    def setUp(self):
        super().setUp()
        self.source = self.payloads['permanent']
        self.live = bytearray(self.stock)
        self.live[packer.APP_START:packer.APP_END] = self.source
        self.status = bytes((0xFD, 1, 1, 0xA8)) + bytes(28)

    def prepare(self, out, **changes):
        args = dict(ihx=self.ihx, mapfile=self.mapfile, stock=self.stock,
                    native_reference=self.native, original_backup=self.backup,
                    source_payload=self.source, source_rom=bytes(self.live),
                    second_nvm_journal=bytes(self.live[packer.NVM_START:packer.MANIFEST_START]),
                    status_reply=self.status, policy={
                        'format': 'ak820-durable-source-policy-1',
                        'source_sha256': packer.digest(self.source),
                        'source_build_id': packer.verify_payload(self.source, allow_legacy=True)['build_id'],
                        'status_protocol': 'FD01-v1', 'scope': 'durable-snapshot-only'}, out=out)
        args.update(changes)
        return builder.prepare_durable_update(**args)

    def test_current_exact_and_unflashable(self):
        self.completed_save()
        # Distinct saved values expose dropped layers, swapped directions and
        # accidental defaulting. Even unpublished macro capacity must survive.
        self.live[packer.NVM_START + 24:packer.NVM_START + 32] = bytes(range(8))
        for layer in range(6):
            for slot in range(128):
                address = packer.NVM_START + packer.KEYMAP_ADDR + layer*256 + slot*2
                self.live[address:address+2] = (0x1000 + layer*128 + slot).to_bytes(2, 'big')
            for direction in range(2):
                address = packer.NVM_START + packer.ENCODER_ADDR + layer*4 + direction*2
                self.live[address:address+2] = (0x3000 + layer*2 + direction).to_bytes(2, 'big')
        macros = b''.join(f'macro-{number:02d}'.encode('ascii') + b'\0' for number in range(16))
        meta = packer.NVM_START + packer.MACRO_BUSY_ADDR
        self.live[meta+1:meta+3] = len(macros).to_bytes(2, 'little')
        start = packer.NVM_START + packer.MACRO_ADDR
        self.live[start:start+len(macros)] = macros
        self.live[start+len(macros):packer.NVM_END] = bytes(
            (i*37+11) & 255 for i in range(packer.NVM_END-start-len(macros)))
        packer.validate_nvm(bytes(self.live[packer.NVM_START:packer.NVM_END]))
        before, files = bytes(self.live), self.session_bytes()
        out = self.root / 'plan'
        result = self.prepare(out)
        payload = bytes.fromhex(result['payload_hex'])
        self.assertEqual(payload[packer.NVM_START-packer.APP_START:packer.NVM_END-packer.APP_START],
                         before[packer.NVM_START:packer.NVM_END])
        self.assertEqual(payload[packer.NVM_END-packer.APP_START:packer.MANIFEST_START-packer.APP_START], bytes(128))
        self.assertFalse(result['live_freshness_verified'])
        self.assertEqual(set(p.name for p in out.iterdir()), {'durable-update-plan.json'})
        self.assertEqual(json.loads((out / 'durable-update-plan.json').read_text()), result)
        with self.assertRaises(FileNotFoundError):
            updater.session_image(out, 'permanent')
        with self.assertRaises(FileExistsError):
            self.prepare(out)
        self.assertEqual(bytes(self.live), before)
        self.assertEqual(files, self.session_bytes())
        self.application.assert_not_called()
        self.hid.assert_not_called()

    def use_legacy(self):
        nvm = legacy_nvm()
        old = bytearray(self.source)
        old[packer.NVM_START-packer.APP_START:packer.NVM_END-packer.APP_START] = nvm
        pos = packer.MANIFEST_START-packer.APP_START
        old[pos+12:pos+16] = packer.LEGACY_BUILD_ID.to_bytes(4, 'little')
        old[pos+48:pos+64] = bytes.fromhex(packer.digest(nvm))[:16]
        self.source = bytes(old)
        self.live[packer.APP_START:packer.APP_END] = old

    def test_legacy_migration(self):
        self.use_legacy()
        expected, _ = packer.migrate_vial_nvm(bytes(self.live[packer.NVM_START:packer.NVM_END]), packer.LEGACY_BUILD_ID)
        result = self.prepare(self.root / 'legacy')
        payload = bytes.fromhex(result['payload_hex'])
        self.assertEqual(payload[packer.NVM_START-packer.APP_START:packer.NVM_END-packer.APP_START], expected)

    def test_bad_status_and_untrusted_freshness(self):
        for offset, value in ((2, 2), (4, 1), (6, 1), (7, 1), (10, 1), (22, 1)):
            status = bytearray(self.status)
            status[offset] = value
            out = self.root / ('bad-status-' + str(offset))
            with self.assertRaises(ValueError):
                self.prepare(out, status_reply=bytes(status))
            self.assertFalse(out.exists())
        with self.assertRaises(TypeError):
            self.prepare(self.root / 'bool', status_reply={'clean': True})

    def test_bad_snapshots_fail_before_output(self):
        for address in (0, 0x27C0, packer.CODE_START, packer.NVM_START+37,
                        packer.NVM_END+64, packer.MANIFEST_START, packer.APP_END):
            live = bytearray(self.live)
            live[address] ^= 1
            out = self.root / str(address)
            with self.assertRaises(ValueError):
                self.prepare(out, source_rom=bytes(live))
            self.assertFalse(out.exists())
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.prepare(self.root / 'changed', second_nvm_journal=bytes(10368))

    def test_bad_macros_fail_before_output(self):
        for offset, value in ((packer.MACRO_BUSY_ADDR, 1), (packer.MACRO_ADDR, 128)):
            live = bytearray(self.live)
            live[packer.NVM_START+offset] = value
            out = self.root / ('macro' + str(offset))
            with self.assertRaises(ValueError):
                self.prepare(out, source_rom=bytes(live))
            self.assertFalse(out.exists())
        self.use_legacy()
        self.live[packer.NVM_START:packer.NVM_END] = legacy_nvm(b'A' * (8193-16) + bytes(16))
        out = self.root / 'overflow'
        with self.assertRaisesRegex(ValueError, 'Nothing was truncated'):
            self.prepare(out)
        self.assertFalse(out.exists())

    def test_source_policy_is_exact_and_fail_closed(self):
        baseline = {'format': 'ak820-durable-source-policy-1',
                    'source_sha256': packer.digest(self.source),
                    'source_build_id': packer.BUILD_ID,
                    'status_protocol': 'FD01-v1', 'scope': 'durable-snapshot-only'}
        for key, value in (('source_sha256', '0'*64), ('source_build_id', 0x082003),
                           ('status_protocol', 'FD01-v2'), ('scope', 'live-ready'),
                           ('live_fresh', True)):
            policy = dict(baseline)
            policy[key] = value
            out = self.root / key
            with self.assertRaises(ValueError):
                self.prepare(out, policy=policy)
            self.assertFalse(out.exists())

    def test_bad_original_recovery_and_references(self):
        before, files = bytes(self.live), self.session_bytes()
        for name, original in (('original_backup', self.backup),
                               ('native_reference', self.native), ('stock', self.stock)):
            changed = bytearray(original)
            changed[0] ^= 1
            evidence = bytes(changed)
            out = self.root / ('bad-' + name)
            with self.assertRaises(ValueError):
                self.prepare(out, **{name: evidence})
            self.assertFalse(out.exists())
            self.assertEqual(bytes(changed), evidence)
        self.assertEqual(bytes(self.live), before)
        self.assertEqual(self.session_bytes(), files)
        self.application.assert_not_called()
        self.hid.assert_not_called()

    def test_target_input_read_race_stops_before_output(self):
        before, files = bytes(self.live), self.session_bytes()
        for path, reader in ((self.ihx, 'read_ihex'), (self.mapfile, 'read_symbols')):
            original = path.read_bytes()
            real_reader = getattr(packer, reader)

            def change_after_parse(filename):
                parsed = real_reader(filename)
                filename.write_bytes(original + b'\n')
                return parsed

            out = self.root / ('raced-' + reader)
            try:
                with patch.object(packer, reader, side_effect=change_after_parse):
                    with self.assertRaisesRegex(ValueError, 'Target build inputs changed'):
                        self.prepare(out)
                self.assertFalse(out.exists())
                # Only the simulated external edit changed a file.
                self.assertEqual(path.read_bytes(), original + b'\n')
                self.assertEqual(bytes(self.live), before)
                self.assertEqual(self.session_bytes(), files)
            finally:
                path.write_bytes(original)
        self.application.assert_not_called()
        self.hid.assert_not_called()


for _name in dir(fixture.PreparationTest):
    if _name.startswith('test_'):
        setattr(GeneralUpdateTest, _name, None)
