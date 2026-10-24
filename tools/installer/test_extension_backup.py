"""Offline schema03 typed backup validation, with synthetic image metadata."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import test_settings_backup as model
s=model.settings
p=s.pack

class ExtensionBackup(unittest.TestCase):
    def fixture(self, directory, name='full-qmk-settings'):
        profile=model.synthetic_profile()
        nvm,_=p.migrate_vial_nvm(model.base_nvm(),p.BUILD_ID,target_build_id=p.EXTENSION_BUILD_ID)
        payload=bytearray(profile['payload'])
        payload[p.NVM_START-p.APP_START:p.NVM_END-p.APP_START]=nvm
        at=p.MANIFEST_START-p.APP_START
        payload[at+12:at+16]=p.EXTENSION_BUILD_ID.to_bytes(4,'little')
        profile.update(payload=bytes(payload),schema=p.EXTENSION_BUILD_ID)
        profile['compatible_images']={profile['ihx_sha256']:{'ihx_sha256':profile['ihx_sha256'],
            'code_sha256':profile['code_sha256'],'build_id':p.EXTENSION_BUILD_ID,
            'extensions_version':1,'combos_version':1,'profile':name,
            'features':s.ak820_profiles.configuration(name)['optional_features']}}
        rom=model.WireDevice(profile,nvm).rom()
        settings=s.settings_from_nvm(nvm,s.rgb_wire(nvm[24:32]),combos=True)
        files={'settings.json':s.canonical(settings),'before-full-rom.bin':rom,'saved-nvm.bin':nvm,
               'read-log.jsonl':b'', '.gitignore':b'*\n'}
        manifest={'format':s.FORMAT_V2,'device':s.DEVICE,'definition_sha256':profile['definition_sha256'],
            'source_ihx_sha256':profile['ihx_sha256'],'code_sha256':profile['code_sha256'],
            'nvm_schema':p.EXTENSION_BUILD_ID,'source_build_id':p.EXTENSION_BUILD_ID,
            'counts':{'layers':6,'physical_keys':83,'assignments':498,'encoder_assignments':12,'macros':16,'macro_capacity':8192},
            'files':{name:s._record(data) for name,data in files.items()}}
        for name,data in {**files,'manifest.json':s.canonical(manifest)}.items():
            (directory/name).write_bytes(data)
        return profile

    def test_v2_roundtrip_missing_metadata_and_downgrade(self):
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp)
            profile=self.fixture(directory)
            backup=s.validate_backup(directory,profile)
            self.assertIn('extensions',backup['settings'])
            with self.assertRaisesRegex(ValueError,'downgrade'):
                s.plan_restore(backup,profile,model.base_nvm())
            del profile['compatible_images'][profile['ihx_sha256']]['extensions_version']
            with self.assertRaisesRegex(ValueError,'reviewed typed'):
                s.validate_backup(directory,profile)

    def test_actual_individual_profiles_and_inactive_preflight(self):
        from unittest.mock import Mock
        for name in ('full-tap-dance','full-key-overrides','full-qmk-settings'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp:
                directory=Path(temp); profile=self.fixture(directory,name)
                backup=s.validate_backup(directory,profile)
                config=s.ak820_profiles.configuration(name)
                features=config['optional_features']
                self.assertEqual(s.keycode_supported(0x5700,features=features),name=='full-tap-dance')
                self.assertEqual(s.keycode_supported(0x7C5D,features=features),name=='full-key-overrides')
                self.assertFalse(s.keycode_supported(0x5708,features=features))
                api=Mock()
                api.settings_query.return_value=config['runtime_qmk_settings']
                api.get_setting.side_effect=lambda qsid: backup['settings']['extensions']['qmk_settings'][str(qsid)]
                api.dynamic_entry_counts.return_value=(8 if name=='full-tap-dance' else 0,8,8 if name=='full-key-overrides' else 0)
                api.get_extension.return_value=bytes(10)
                # Isolate typed getters from the existing base protocol model.
                typed={'extensions':backup['settings']['extensions'],'keys':[], 'encoders':[],
                       'layout_options':0,'macros':{'data_hex':bytes(16).hex()},'rgb':{'current_mode_hex':''}}
                api.get_layout_options.return_value=0
                api.macros.return_value=bytes(8192)
                api.rgb_mode.return_value=b''
                s._check_getters(api,typed,profile['compatible_images'][profile['ihx_sha256']])
                self.assertEqual(api.get_extension.call_count,8 if name!='full-qmk-settings' else 0)
                target=bytearray(backup['nvm'])
                if name!='full-tap-dance':
                    target[0x6C0:0x6CA]=bytes.fromhex('04000000000000000000')
                else:
                    values=s.extensions.decode_settings(bytes(target[0x6A8:0x6C0]));values['2']=41
                    target[0x6A8:0x6C0]=s.extensions.settings_record(values)
                with self.assertRaisesRegex(ValueError,'Inactive'):
                    s.plan_restore(backup,profile,target)
                image=profile['compatible_images'][profile['ihx_sha256']]
                image['features']=image['features']+['tap-dance']
                with self.assertRaises(ValueError):s.validate_backup(directory,profile)

    def test_v2_duplicate_and_missing_fields(self):
        for replacement in (b'{"version":1,"version":1}', b'{}'):
            with self.subTest(replacement=replacement), tempfile.TemporaryDirectory() as temp:
                directory=Path(temp); profile=self.fixture(directory)
                path=directory/'settings.json'; path.write_bytes(replacement)
                manifest=json.loads((directory/'manifest.json').read_bytes())
                manifest['files']['settings.json']=s._record(replacement)
                (directory/'manifest.json').write_bytes(s.canonical(manifest))
                with self.assertRaises(ValueError): s.validate_backup(directory,profile)

if __name__=='__main__': unittest.main()
