"""Offline versioned compact controls and historical image ABI boundaries."""
import binascii
import struct
import unittest
from unittest.mock import Mock
from installer import settings_backup as s
from ak820_device_protocol import DeviceAPI

e=s.extensions
p=s.ak820_profiles

class CompactContract(unittest.TestCase):
    def test_v1_roundtrip_and_forward_only_normalization(self):
        old=e.settings_record(version=1)
        values=e.decode_settings(old)
        self.assertEqual(set(map(int,values)),set(e.LEGACY_FIELDS))
        self.assertEqual(e.settings_record(values,version=1),old)
        current=e.decode_settings(old,version=2)
        self.assertEqual({i:current[i] for i in ('3','6','22')},{'3':1,'6':0,'22':0})
        self.assertEqual(e.decode_settings(e.settings_record(current)),current)
        with self.assertRaisesRegex(ValueError,'downgrade'):
            e.decode_settings(e.settings_record(),version=1)

    def test_v2_range_mask_reserved_and_crc(self):
        raw=e.settings_record()
        self.assertEqual(raw[:5],bytes.fromhex('5153020f7f'))
        self.assertEqual(raw[16:22],bytes([1,0,0,0,0,0]))
        for qsid,valid,invalid in ((3,(0,1,4,8,16,29),(2,3,30)),(6,(0,1,30000),(-1,30001)),(22,(0,1),(-1,2))):
            for value in valid:e.field_value(qsid,value)
            for value in invalid:
                with self.assertRaises(ValueError):e.field_value(qsid,value)
        for version in (1,2):
            record=e.settings_record(version=version)
            for offset in range(24):
                broken=bytearray(record);broken[offset]^=1
                with self.assertRaises(ValueError):e.decode_settings(bytes(broken))
            for offset in ((16,17,18,19,20,21) if version==1 else (20,21)):
                broken=bytearray(record);broken[offset]=1
                broken[22:]=binascii.crc_hqx(broken[:22],0xffff).to_bytes(2,'little')
                with self.assertRaises(ValueError):e.decode_settings(bytes(broken))

    def test_historical_identity_stays_frozen(self):
        for name in p.RELEASE_PROFILES:
            old=p._configuration(name,p.PROFILES[name])
            p.validate_source_configuration(old)
            self.assertNotIn('compact_controls_version',old)
            self.assertFalse(set((3,6,22)) & set(old['runtime_qmk_settings']))
            current=p.configuration(name)
            self.assertEqual(current['compact_controls_version'],2)
            self.assertEqual(current['optional_features'],old['optional_features'])
            image=s._settings_identity(old,'a'*64,'b'*64,'c'*64,combo_actions=['caps-word-toggle'],macro_layer_tap=True)
            self.assertNotIn('settings_record_version',image)
            for code in (0x7c50,0x7c51,0x7c52,0x7c5a,0x7c5b,0x7c5c,0x7e00,0x7e01,0x7e02):
                self.assertNotIn(code,image['supported_keycodes'])
        for name in p.RELEASE_PROFILES:
            self.assertNotIn('compact_controls_version',p.historical_configuration(name))

    def test_equal_set_and_reset_reapply_runtime_without_persistence(self):
        for record in (e.settings_record(version=1),e.settings_record(),bytes(24),b'\xff'*24):
            for operation in (3,22,'reset'):
                with self.subTest(record=record.hex(),operation=operation):
                    before=bytearray(0x2800)
                    before[37:40]=e.SCHEMA.to_bytes(3,'little')
                    before[0x6a8:0x6c0]=record
                    before=bytes(before)
                    api=object.__new__(DeviceAPI)
                    api.binding={'settings_record_version':2}
                    api.allow_writes=True
                    api.read_nvm=Mock(return_value=before)
                    api.status=Mock()
                    api.settings_query=Mock(return_value=[1,2,3,4,6,7,18,19,22])
                    api.get_setting=Mock(side_effect=lambda qsid:e.FIELDS[qsid][4])
                    runtime={'3':0,'22':1}
                    def exchange(packet):
                        if packet[1:3]==bytes([12,0]):
                            runtime.update({'3':1,'22':0})
                        else:
                            runtime[str(packet[2])]=packet[4]
                        return b'\0'+packet[1:]
                    api.exchange=Mock(side_effect=exchange)
                    if operation=='reset':
                        api.reset_settings()
                        self.assertEqual(runtime,{'3':1,'22':0})
                    else:
                        api.set_setting(operation,e.FIELDS[operation][4])
                        self.assertEqual(runtime[str(operation)],e.FIELDS[operation][4])
                    api.exchange.assert_called_once()
                    self.assertEqual(api.read_nvm.call_count,2)
                    api.status.assert_called_once()

    def test_legacy_default_reset_sends_command_without_upgrading_storage(self):
        for record in (e.settings_record(version=1),bytes(24),b'\xff'*24):
            before=bytearray(0x2800)
            before[37:40]=e.SCHEMA.to_bytes(3,'little')
            before[0x6a8:0x6c0]=record
            api=object.__new__(DeviceAPI)
            api.binding={'settings_record_version':1}
            api.allow_writes=True
            api.read_nvm=Mock(return_value=bytes(before))
            api.status=Mock()
            api.settings_query=Mock(return_value=list(e.LEGACY_FIELDS))
            api.get_setting=Mock(side_effect=lambda qsid:e.LEGACY_FIELDS[qsid][4])
            api.exchange=Mock(side_effect=lambda packet:b'\0'+packet[1:])
            api.reset_settings()
            api.exchange.assert_called_once_with(api.packet(254,12))
            self.assertEqual(api.read_nvm.call_count,2)

    def test_media_write_requires_explicit_exact_capability_before_transport(self):
        for binding in ({},{'settings_record_version':1},{'settings_record_version':1,'combo_media':True},{'settings_record_version':2},
                        {'ihx_sha256':'old','combo_media':True,'compatible_images':{'old':{'settings_record_version':1}}}):
            api=object.__new__(DeviceAPI)
            api.binding=binding
            api.allow_writes=True
            api.exchange=Mock()
            api.read_nvm=Mock()
            for output in (0xa8,0xc2):
                with self.assertRaisesRegex(ValueError,'Media Combo unsupported'):
                    api.set_combo(0,struct.pack('<5H',4,5,0,0,output))
            api.exchange.assert_not_called()
            api.read_nvm.assert_not_called()

    def test_media_write_accepts_current_exact_capability(self):
        data=struct.pack('<5H',4,5,0,0,0xa8)
        before=bytes(0x2800)
        after=bytearray(before)
        after[DeviceAPI.COMBO_OFFSET:DeviceAPI.COMBO_OFFSET+10]=DeviceAPI.stored_combo(data)
        for binding in ({'settings_record_version':2,'combo_media':True},
                        {'ihx_sha256':'current','compatible_images':{'current':{'settings_record_version':2,'combo_media':True}}}):
            api=object.__new__(DeviceAPI)
            api.binding=binding
            api.allow_writes=True
            api.read_nvm=Mock(side_effect=[before,bytes(after)])
            api.exchange=Mock(side_effect=lambda packet:b'\0'+packet[1:])
            api.status=Mock()
            api.get_combo=Mock(return_value=data)
            self.assertTrue(api.set_combo(0,data))
            api.exchange.assert_called_once()

    def test_legacy_protocol_rejects_new_fields_before_transport(self):
        api=object.__new__(DeviceAPI)
        api.binding={'settings_record_version':1}
        api.allow_writes=True
        api.exchange=Mock()
        for qsid in (3,6,22):
            with self.assertRaisesRegex(ValueError,'unsupported'):
                api.get_setting(qsid)
            with self.assertRaisesRegex(ValueError,'unsupported'):
                api.set_setting(qsid,e.FIELDS[qsid][4])
        api.exchange.assert_not_called()

    def test_physical_controls_and_media_combo_boundary(self):
        old={'features':['one-shot']}
        current={**old,'compact_controls_version':2,'combo_media':True}
        for code in (*range(0x7c50,0x7c53),*range(0x7e00,0x7e03)):
            self.assertFalse(s.image_keycode_supported(code,old))
            self.assertTrue(s.image_keycode_supported(code,current))
            for context in ('encoder','macro','macro-tap','macro-down','macro-up'):
                self.assertFalse(s.image_keycode_supported(code,current,context=context))
        # One Shot session controls are outside the compact version 2 contract.
        for code in range(0x7c5a,0x7c5d):
            for features in ([],['one-shot']):
                image={'compact_controls_version':2,'features':features}
                self.assertFalse(s.keycode_supported(code,features=features))
                for context in ('matrix','encoder','macro','macro-tap','macro-down','macro-up'):
                    self.assertFalse(s.image_keycode_supported(code,image,context=context))
        for output in range(0xa8,0xc3):
            raw=struct.pack('<5H',4,5,0,0,output)
            DeviceAPI.validate_combo(raw)
            combo={'entries_hex':[raw.hex()]}
            s._validate_combo_actions(combo,current)
            with self.assertRaises(ValueError):s._validate_combo_actions(combo,old)
            with self.assertRaises(ValueError):DeviceAPI.validate_combo(struct.pack('<5H',4,5,0,0,0x100|output))

if __name__=='__main__':unittest.main()
