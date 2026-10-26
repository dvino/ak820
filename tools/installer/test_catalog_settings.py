"""Exact-image desktop settings contract; synthetic ROMs, no HID or flash."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import test_settings_backup as model

s = model.settings
p = s.pack


def profile_for(name, seed):
    assert name in s.ak820_profiles.RELEASE_PROFILES
    return _profile_for(name, seed)


def legacy_profile_for(name, seed):
    assert name not in s.ak820_profiles.RELEASE_PROFILES
    return _profile_for(name, seed)


def _profile_for(name, seed):
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
    data = s.settings_from_nvm(nvm, s.rgb_wire(nvm[24:32], image=s._profile_images(profile)[profile['ihx_sha256']]), combos=True)
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
        self.assertEqual(s.ak820_profiles.RELEASE_PROFILES,
            ('main', 'game', 'mmo', 'typing', 'code', 'pointer', 'onehand', 'creative', 'shortcuts', 'multios'))
        self.assertEqual(s.ak820_profiles.DEFAULT_PROFILE, 'main')
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
        _, row = profile_for('main', 31)
        edits = [lambda r: r['settings_identity'].update(extra=True),
                 lambda r: r['settings_identity']['supported_keycodes'].__setitem__(0, False),
                 lambda r: r['settings_identity']['features'].append('mouse-keys'),
                 lambda r: r['settings_identity']['features'].append('future'),
                 lambda r: r['settings_identity']['supported_keycodes'].append(0xCD),
                 lambda r: r['settings_identity'].update(nvm_schema=p.BUILD_ID),
                 lambda r: r['identity'].update(ihx_sha256='0'*64)]
        for edit in edits:
            poisoned = copy.deepcopy(row); edit(poisoned)
            with self.subTest(edit=edit), self.assertRaises(ValueError):
                s._catalog_images(catalog_for(poisoned))
        with self.assertRaises(ValueError): s._catalog_images(catalog_for(row, row))
        with self.assertRaises(ValueError): s._catalog_images(catalog_for(row, transitions=[{'source': '0'*64, 'target': row['settings_identity']['ihx_sha256']}]))

    def test_exact_code_mismatch_and_unknown_backup_fields_fail(self):
        profile, row = profile_for('main', 32)
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
        work, wr = profile_for('main', 40); mouse, mr = profile_for('game', 41)
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
        legacy, lr = legacy_profile_for('work', 42)
        typed, tr = profile_for('main', 43)
        catalog = catalog_for(lr, tr, transitions=[
            {'source': legacy['ihx_sha256'], 'target': typed['ihx_sha256']},
            {'source': typed['ihx_sha256'], 'target': legacy['ihx_sha256']}])
        bind(catalog, legacy, typed)
        with tempfile.TemporaryDirectory() as temp:
            backup = backup_at(Path(temp), legacy)
            self.assertIsNotNone(s.plan_restore(backup, typed)['extension_data'])
        with tempfile.TemporaryDirectory() as temp:
            backup = backup_at(Path(temp), typed)
            with self.assertRaisesRegex(ValueError, 'downgrade'):
                s.plan_restore(backup, legacy)

    def test_unsupported_encoder_and_macro_actions_block_preflight(self):
        for name, code, context in [('main',0x7C58,'encoder'), ('typing',0x7C13,'encoder'),
                                     ('creative',0x5700,'encoder'), ('main',0x7C58,'macro')]:
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
        profile,row=profile_for('main',63);bind(catalog_for(row),profile)
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
        profile,row=profile_for('main',64);bind(catalog_for(row),profile)
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
        source,sr=profile_for('game',61);target,tr=profile_for('main',62)
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

    def test_grave_escape_is_allowed_only_when_compiled(self):
        for name in s.ak820_profiles.RELEASE_PROFILES:
            features = s.ak820_profiles.configuration(name)['optional_features']
            self.assertEqual(s.keycode_supported(0x7c16, features=features), 'grave-escape' in features)

    def test_rgb_modes_follow_exact_profile_enum(self):
        for name in s.ak820_profiles.RELEASE_PROFILES:
            config = s.ak820_profiles.configuration(name)
            image = {'features': config['optional_features'], 'supported_keycodes': []}
            direct = 'vialrgb-direct' in config['optional_features']
            expected = {1:2,2:6,3:13,4:14,5:1,6:31} if direct else {1:2,2:6,3:13,4:14,5:31}
            self.assertEqual(s.rgb_modes(image), expected)
            raw = bytes((5*4+1,0,255,80,96,255,0,0))
            self.assertEqual(int.from_bytes(s.rgb_wire(raw,image=image)[:2], 'little'), 1 if direct else 31)
            if not direct:
                with self.assertRaisesRegex(ValueError, 'enable/mode'):
                    s.rgb_wire(bytes((6*4+1,0,255,80,96,255,0,0)),image=image)

    def test_reactive_mode_translates_between_direct_and_no_direct_enums(self):
        for source_name,target_name,enum in [('typing','main',5),('main','typing',6)]:
            source,row = profile_for(source_name,61)
            target,target_row = profile_for(target_name,62)
            edge = {'source': source['ihx_sha256'], 'target': target['ihx_sha256']}
            bind(catalog_for(row,target_row,transitions=[edge]),source,target)
            nvm = bytearray(source['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
            nvm[24] = enum*4+1
            with tempfile.TemporaryDirectory() as temp:
                backup = backup_at(Path(temp),source,nvm)
                plan = s.plan_restore(backup,target)
                self.assertEqual(int.from_bytes(plan['rgb_saved_mode'][:2],'little'),31)

    def test_direct_palette_is_blocked_before_restore_into_no_direct_image(self):
        source,row = profile_for('main',63)
        target,target_row = profile_for('typing',64)
        edge = {'source':source['ihx_sha256'],'target':target['ihx_sha256']}
        bind(catalog_for(row,target_row,transitions=[edge]),source,target)
        nvm = bytearray(source['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
        nvm[24] = 5*4+1
        with tempfile.TemporaryDirectory() as temp:
            backup = backup_at(Path(temp),source,nvm)
            with self.assertRaisesRegex(ValueError,'unsupported by the selected target'):
                s.plan_restore(backup,target)
            target_dir = Path(temp)/'target-snapshot'
            target_dir.mkdir()
            before = backup_at(target_dir,target)
            api = Mock(allow_writes=True)
            with self.assertRaisesRegex(ValueError,'unsupported by the selected target'):
                s.restore_settings(api,backup,target,target_backup=before)
            self.assertEqual(api.mock_calls, [])

    def test_known_beta1_work_source_requires_exact_pins_and_explicit_transition(self):
        # These are historical image descriptors, not invented ROM contents.
        source = {'ihx_sha256': '652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880',
                  'code_sha256': 'a7ad972f47acff20f3492ed846f5c6ca0825d43de263f26cc9328069a27cdd10'}
        for index, name in enumerate(s.ak820_profiles.RELEASE_PROFILES, 65):
            target, row = profile_for(name, index)
            edge = {'source': source['ihx_sha256'], 'target': target['ihx_sha256']}
            catalog = catalog_for(row, transitions=[edge])
            with self.subTest(target=name):
                with self.assertRaisesRegex(ValueError, 'Unknown settings transition'):
                    s._catalog_images(catalog)
                catalog['historical_sources'] = [copy.deepcopy(source)]
                images = s._catalog_images(catalog)
                legacy = images[s.WORK_IHX]
                self.assertEqual(legacy, s._legacy_images()[s.WORK_IHX])
                self.assertEqual(legacy['build_id'], p.BUILD_ID)
                self.assertEqual(images[target['ihx_sha256']]['build_id'], p.EXTENSION_BUILD_ID)
                self.assertNotIn('supported_keycodes', legacy)
                self.assertNotIn('profile', legacy)
                self.assertNotIn('qmk-settings', legacy['features'])
                catalog['historical_sources'][0]['code_sha256'] = '0' * 64
                with self.assertRaisesRegex(ValueError, 'historical settings source'):
                    s._catalog_images(catalog)


    def test_pinned_alpha2_source_requires_explicit_descriptor_and_edge(self):
        target,row = profile_for('main',91)
        source = s.SUPPORTED_IHX
        edge = {'source':source,'target':target['ihx_sha256']}
        catalog = catalog_for(row,transitions=[edge])
        with self.assertRaisesRegex(ValueError,'Unknown settings transition'):
            s._catalog_images(catalog)
        descriptor = {'ihx_sha256':source,'code_sha256':s._legacy_images()[source]['code_sha256']}
        catalog['historical_sources'] = [descriptor]
        self.assertEqual(s._catalog_images(catalog)[source],s._legacy_images()[source])
        catalog['historical_sources'].append(copy.deepcopy(descriptor))
        with self.assertRaisesRegex(ValueError,'duplicate historical'):
            s._catalog_images(catalog)
        catalog['historical_sources'] = [{'ihx_sha256':'f'*64,'code_sha256':'e'*64}]
        with self.assertRaisesRegex(ValueError,'Unknown or duplicate historical'):
            s._catalog_images(catalog)

    def test_restore_and_final_verification_translate_rgb_enum_both_directions(self):
        for source_name,target_name,source_enum,target_enum in [('main','typing',6,5),('typing','main',5,6)]:
            for enabled in (0,1):
                with self.subTest(source=source_name,target=target_name,enabled=enabled), tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    source,row = profile_for(source_name,71)
                    target,target_row = profile_for(target_name,72)
                    edge = {'source':source['ihx_sha256'],'target':target['ihx_sha256']}
                    bind(catalog_for(row,target_row,transitions=[edge]),source,target)
                    nvm = bytearray(source['payload'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START])
                    nvm[24] = source_enum*4+enabled
                    saved_dir,target_dir = root/'source',root/'target'
                    saved_dir.mkdir();target_dir.mkdir()
                    saved = backup_at(saved_dir,source,nvm)
                    before = backup_at(target_dir,target)
                    target_nvm = before['nvm']
                    raw = model.WireDevice(target,target_nvm)
                    raw.mode_ids = ({1:2,2:6,3:13,4:14,5:31} if target_name=='typing' else {1:2,2:6,3:13,4:14,5:1,6:31})
                    (root/'wire').mkdir()
                    api = s.DeviceAPI(target,root/'wire',lambda:raw,allow_writes=True)
                    config = s.ak820_profiles.configuration(target_name)
                    api.settings_query = Mock(return_value=config['runtime_qmk_settings'])
                    api.get_setting = lambda qsid:s.extensions.decode_settings(bytes(raw.nvm[0x6a8:0x6c0]))[str(qsid)]
                    api.dynamic_entry_counts = Mock(return_value=(0,8,8))
                    api.get_extension = lambda kind,index:bytes(raw.nvm[s.extensions.slot_offset(kind,index):s.extensions.slot_offset(kind,index)+10])
                    try:
                        with patch('ak820_device_protocol.time.sleep'):
                            result = s.restore_settings(api,saved,target,target_backup=before)
                        self.assertTrue(result['verified'])
                        self.assertEqual(raw.nvm[24],target_enum*4+enabled)
                        self.assertTrue(any(packet[0]==9 for packet in raw.writes))
                        with patch('ak820_device_protocol.time.sleep'):
                            self.assertTrue(s.verify_restore(api,saved,target)['verified'])
                    finally:
                        api.close()

    def test_loader_constructs_schema03_and_rejects_wrong_actual_code(self):
        profile,row=profile_for('main',50)
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
