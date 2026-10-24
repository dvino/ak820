"""Exact-image desktop settings contract; synthetic ROMs, no HID or flash."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import test_settings_backup as model

s = model.settings
p = s.pack


def profile_for(name, seed):
    profile = model.synthetic_profile()
    config = s.ak820_profiles.configuration(name)
    nvm = model.base_nvm()
    if config['nvm_schema'] != p.BUILD_ID:
        nvm, _ = p.migrate_vial_nvm(nvm, p.BUILD_ID, target_build_id=config['nvm_schema'])
    payload = bytearray(profile['payload'])
    payload[:p.CODE_END-p.APP_START] = bytes((seed,)) * (p.CODE_END-p.APP_START)
    code_hash = p.digest(payload[:p.CODE_END-p.APP_START])
    at = p.MANIFEST_START-p.APP_START
    payload[at:at+48] = p.MAGIC + b'\1\0\0\0' + config['nvm_schema'].to_bytes(4, 'little') + bytes.fromhex(code_hash)
    payload[p.NVM_START-p.APP_START:p.NVM_END-p.APP_START] = nvm
    profile.update(payload=bytes(payload), ihx_sha256=p.digest(bytes((seed,))), code_sha256=code_hash, schema=config['nvm_schema'])
    contract = s.catalog_settings_identity(config, profile['ihx_sha256'], code_hash, profile['definition_sha256'])
    row = {'profile': name, 'configuration': config, 'identity': {'ihx_sha256': profile['ihx_sha256'], 'nvm_schema': config['nvm_schema']}, 'settings_identity': contract}
    return profile, row


def catalog_for(*rows, transitions=()):
    return {'format': 'ak820-firmware-matrix-1', 'profiles': list(rows), 'settings_transitions': list(transitions)}


def bind(catalog, *profiles):
    images = s._catalog_images(catalog)
    for profile in profiles:
        profile['compatible_images'] = images
        profile['settings_transitions'] = catalog['settings_transitions']


def backup_at(folder, profile, nvm=None):
    nvm = bytes(nvm if nvm is not None else profile['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
    data = s.settings_from_nvm(nvm, s.rgb_wire(nvm[24:32]), combos=True)
    files = {'settings.json': s.canonical(data), 'before-full-rom.bin': model.WireDevice(profile, nvm).rom(),
             'saved-nvm.bin': nvm, 'read-log.jsonl': b'', '.gitignore': b'*\n'}
    manifest = {'format': s.FORMAT_V2 if profile['schema'] == s.extensions.SCHEMA else s.FORMAT,
                'device': s.DEVICE, 'definition_sha256': profile['definition_sha256'],
                'source_ihx_sha256': profile['ihx_sha256'], 'code_sha256': profile['code_sha256'],
                'nvm_schema': profile['schema'], 'source_build_id': profile['schema'],
                'counts': {'layers': 6, 'physical_keys': 83, 'assignments': 498, 'encoder_assignments': 12, 'macros': 16, 'macro_capacity': 8192},
                'files': {name: s._record(value) for name, value in files.items()}}
    for name, value in {**files, 'manifest.json': s.canonical(manifest)}.items():
        (folder/name).write_bytes(value)
    return s.validate_backup(folder, profile)


class CatalogSettings(unittest.TestCase):
    def test_all_curated_contracts_exact_and_no_release_approval(self):
        for i, name in enumerate(s.ak820_profiles.RELEASE_PROFILES, 20):
            with self.subTest(name=name):
                profile, row = profile_for(name, i)
                catalog = catalog_for(row)
                bind(catalog, profile)
                self.assertEqual(s._profile_images(profile)[profile['ihx_sha256']]['build_id'], profile['schema'])
                self.assertNotIn('release_approved', row['settings_identity'])
                self.assertEqual(row['settings_identity']['supported_keycodes'], sorted(set(row['settings_identity']['supported_keycodes'])))
                with tempfile.TemporaryDirectory() as temp:
                    backup = backup_at(Path(temp), profile)
                    self.assertEqual(s.plan_restore(backup, profile)['key_count'], 498)

    def test_wrong_unknown_duplicate_and_feature_poisoned_metadata_fail(self):
        _, row = profile_for('work', 31)
        edits = [lambda r: r['settings_identity'].update(extra=True),
                 lambda r: r['settings_identity']['supported_keycodes'].__setitem__(0, False),
                 lambda r: r['settings_identity']['features'].append('mouse-keys'),
                 lambda r: r['settings_identity']['features'].append('future'),
                 lambda r: r['settings_identity']['supported_keycodes'].append(0xCD),
                 lambda r: r['settings_identity'].update(nvm_schema=s.extensions.SCHEMA),
                 lambda r: r['identity'].update(ihx_sha256='0'*64)]
        for edit in edits:
            poisoned = copy.deepcopy(row); edit(poisoned)
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                s._catalog_images(catalog_for(poisoned))
        with self.assertRaises(ValueError): s._catalog_images(catalog_for(row, row))
        with self.assertRaises(ValueError): s._catalog_images(catalog_for(row, transitions=[{'source': '0'*64, 'target': row['settings_identity']['ihx_sha256']}]))

    def test_exact_code_mismatch_and_unknown_backup_fields_fail(self):
        profile, row = profile_for('work', 32)
        bind(catalog_for(row), profile)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp); backup_at(path, profile)
            manifest = json.loads((path/'manifest.json').read_bytes()); manifest['extra'] = True
            (path/'manifest.json').write_bytes(s.canonical(manifest))
            with self.assertRaisesRegex(ValueError, 'Unknown backup manifest'): s.validate_backup(path, profile)
        rom = bytearray(model.WireDevice(profile).rom()); rom[p.APP_START] ^= 1
        with self.assertRaisesRegex(ValueError, 'exact reviewed'): s.validate_rom(rom, profile)

    def test_command_domains_and_source_restrictions(self):
        domains = {'nkro-control': (0x7011,0x7012,0x7013), 'space-cadet': (0x7C1A,0x7C1B,0x7C1E),
                   'gui-lock': (0x7009,0x700A,0x700B), 'ctrl-gui-swap': (0x701B,0x701C,0x701D),
                   'mac-pc': (0x7014,0x7015,0x7016), 'auto-shift': (0x7C13,0x7C14,0x7C15),
                   'dynamic-macros': tuple(range(0x7C53,0x7C58)), 'leader': (0x7C58,),
                   'mouse-keys': tuple(range(0xCD,0xD6)) + tuple(range(0xD9,0xDD)),
                   'tap-dance': tuple(range(0x5700,0x5708)), 'key-overrides': (0x7C5D,0x7C5E,0x7C5F)}
        for feature, values in domains.items():
            for code in values:
                self.assertTrue(s.keycode_supported(code, features=[feature]), (feature, code))
                self.assertFalse(s.keycode_supported(code), (feature, code))
        for code in (0xD6,0xD7,0xD8,0xDD,0xDE,0xDF,0x7005,0x7017,0x7C10,0x7C18,0x7C5A,0x5280):
            self.assertFalse(s.keycode_supported(code, features=list(s.MODULE_FEATURES)), hex(code))
        for feature, code in [('tap-dance',0x5700), ('leader',0x7C58), ('auto-shift',0x7C13)] + [('dynamic-macros', code) for code in range(0x7C53,0x7C58)]:
            image = {'features':[feature]}
            self.assertTrue(s.image_keycode_supported(code, image))
            for context in ('encoder','macro'): self.assertFalse(s.image_keycode_supported(code,image,context=context))

    def test_reviewed_transition_does_not_override_module_or_schema(self):
        work, wr = profile_for('work', 40); mouse, mr = profile_for('mouse', 41)
        transition = {'source': work['ihx_sha256'], 'target': mouse['ihx_sha256']}
        catalog = catalog_for(wr,mr); bind(catalog,work,mouse)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp); backup=backup_at(path,work)
            self.assertIsNotNone(s.plan_restore(backup,work))
            with self.assertRaisesRegex(ValueError,'explicitly reviewed'): s.plan_restore(backup,mouse)
            catalog['settings_transitions'].append(transition)
            self.assertIsNotNone(s.plan_restore(backup,mouse))
        nvm=bytearray(work['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
        at=s.DeviceAPI.key_offset(0,s.PHYSICAL[0]);nvm[at:at+2]=(0x7C58).to_bytes(2,'big')
        with tempfile.TemporaryDirectory() as temp:
            backup=backup_at(Path(temp),work,nvm)
            with self.assertRaisesRegex(ValueError,'Unsupported keycode'): s.plan_restore(backup,mouse)
        typed,tr=profile_for('settings',42)
        catalog=catalog_for(wr,tr,transitions=[{'source':work['ihx_sha256'],'target':typed['ihx_sha256']}, {'source':typed['ihx_sha256'],'target':work['ihx_sha256']}]);bind(catalog,work,typed)
        with tempfile.TemporaryDirectory() as temp:
            backup=backup_at(Path(temp),work);self.assertIsNotNone(s.plan_restore(backup,typed)['extension_data'])
        with tempfile.TemporaryDirectory() as temp:
            backup=backup_at(Path(temp),typed)
            with self.assertRaisesRegex(ValueError,'downgrade'):s.plan_restore(backup,work)

    def test_unsupported_encoder_and_macro_actions_block_preflight(self):
        for name, code, context in [('work',0x7C58,'encoder'), ('typing',0x7C13,'encoder'),
                                     ('tap-dance',0x5700,'encoder'), ('work',0x7C58,'macro')]:
            with self.subTest(name=name,context=context):
                profile,row=profile_for(name,60);bind(catalog_for(row),profile)
                nvm=bytearray(profile['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
                if context=='encoder':
                    at=s.DeviceAPI.encoder_offset(0,0);nvm[at:at+2]=code.to_bytes(2,'big')
                else:
                    stream=b'\1\5'+code.to_bytes(2,'little')+bytes(16)
                    nvm[p.MACRO_ADDR:p.MACRO_ADDR+len(stream)]=stream
                    nvm[p.MACRO_BUSY_ADDR+1:p.MACRO_BUSY_ADDR+3]=len(stream).to_bytes(2,'little')
                with tempfile.TemporaryDirectory() as temp:
                    backup=backup_at(Path(temp),profile,nvm)
                    with self.assertRaisesRegex(ValueError,'Unsupported keycode'):s.plan_restore(backup,profile)

    def test_dynamic_macro_controls_require_physical_matrix_for_every_opcode(self):
        profile,row=profile_for('work',63);bind(catalog_for(row),profile)
        image=profile['compatible_images'][profile['ihx_sha256']]
        for code in range(0x7C53,0x7C58):
            self.assertTrue(s.image_keycode_supported(code,image,context='matrix'))
            for context in ('encoder','macro-tap','macro-down','macro-up'):
                with self.subTest(code=hex(code),context=context):
                    nvm=bytearray(profile['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
                    if context=='encoder':
                        at=s.DeviceAPI.encoder_offset(0,0);nvm[at:at+2]=code.to_bytes(2,'big')
                    else:
                        opcode={'macro-tap':5,'macro-down':6,'macro-up':7}[context]
                        stream=bytes((1,opcode))+code.to_bytes(2,'little')+bytes(16)
                        nvm[p.MACRO_ADDR:p.MACRO_ADDR+len(stream)]=stream
                        nvm[p.MACRO_BUSY_ADDR+1:p.MACRO_BUSY_ADDR+3]=len(stream).to_bytes(2,'little')
                    with tempfile.TemporaryDirectory() as temp:
                        backup=backup_at(Path(temp),profile,nvm)
                        with self.assertRaisesRegex(ValueError,'Unsupported keycode'):s.plan_restore(backup,profile)

    def test_key_override_macro_controls_accept_tap_and_reject_down_up(self):
        profile,row=profile_for('key-overrides',64);bind(catalog_for(row),profile)
        image=profile['compatible_images'][profile['ihx_sha256']]
        for code in range(0x7C5D,0x7C60):
            for opcode,context in ((5,'macro-tap'),(6,'macro-down'),(7,'macro-up')):
                with self.subTest(code=hex(code),context=context):
                    self.assertEqual(s.image_keycode_supported(code,image,context=context),opcode==5)
                    nvm=bytearray(profile['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
                    stream=bytes((1,opcode))+code.to_bytes(2,'little')+bytes(16)
                    nvm[p.MACRO_ADDR:p.MACRO_ADDR+len(stream)]=stream
                    nvm[p.MACRO_BUSY_ADDR+1:p.MACRO_BUSY_ADDR+3]=len(stream).to_bytes(2,'little')
                    with tempfile.TemporaryDirectory() as temp:
                        backup=backup_at(Path(temp),profile,nvm)
                        if opcode==5:self.assertIsNotNone(s.plan_restore(backup,profile))
                        else:
                            with self.assertRaisesRegex(ValueError,'Unsupported keycode in macro'):s.plan_restore(backup,profile)

    def test_macro_module_keycode_cannot_cross_profile_even_with_transition(self):
        source,sr=profile_for('system',61);target,tr=profile_for('work',62)
        catalog=catalog_for(sr,tr,transitions=[{'source':source['ihx_sha256'],'target':target['ihx_sha256']}])
        bind(catalog,source,target)
        nvm=bytearray(source['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
        stream=bytes.fromhex('01050970')+bytes(16)
        nvm[p.MACRO_ADDR:p.MACRO_ADDR+len(stream)]=stream
        nvm[p.MACRO_BUSY_ADDR+1:p.MACRO_BUSY_ADDR+3]=len(stream).to_bytes(2,'little')
        with tempfile.TemporaryDirectory() as temp:
            backup=backup_at(Path(temp),source,nvm)
            self.assertIsNotNone(s.plan_restore(backup,source))
            with self.assertRaisesRegex(ValueError,'Unsupported keycode in macro'):s.plan_restore(backup,target)

    def test_loader_constructs_schema03_and_rejects_wrong_actual_code(self):
        profile,row=profile_for('settings',50)
        with tempfile.TemporaryDirectory() as temp:
            bundle=Path(temp);(bundle/'firmware').mkdir();(bundle/'reference').mkdir()
            ihx=b'synthetic ihx';(bundle/'firmware/application.ihx').write_bytes(ihx)
            row['identity']['ihx_sha256']=p.digest(ihx);row['settings_identity']['ihx_sha256']=p.digest(ihx)
            (bundle/'reference/vial.json').write_bytes(s.canonical(profile['definition']))
            with patch.object(p,'validate_native'),patch.object(s.diagnostic,'diagnostic_build',return_value={}),patch.object(p,'read_symbols',return_value={}),patch.object(p,'migrate',return_value=(model.base_nvm(),{})),patch.object(p,'pack',return_value=profile['payload']) as packed:
                result=s.load_profile(bundle,profile['backup'],trusted_catalog=catalog_for(row))
                self.assertEqual(result['schema'],s.extensions.SCHEMA)
                self.assertEqual(packed.call_args.kwargs['target_build_id'],s.extensions.SCHEMA)
                row['settings_identity']['code_sha256']='0'*64
                with self.assertRaisesRegex(ValueError,'CODE does not match'):s.load_profile(bundle,profile['backup'],trusted_catalog=catalog_for(row))
                with self.assertRaisesRegex(ValueError,'Unsupported firmware'):s.load_profile(bundle,profile['backup'])


if __name__ == '__main__': unittest.main()
