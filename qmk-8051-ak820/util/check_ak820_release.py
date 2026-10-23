#!/usr/bin/env python3
"""Check packed release bytes and embedded constants; no HID dependency."""
import argparse
import json
import lzma
import struct
from pathlib import Path

from check_ak820_usb_image import validate as validate_usb_image

from pack_ak820 import (APP_START,APP_END,CODE_START,CODE_END,LOW_START,LOW_END,
    NVM_START,NVM_END,MANIFEST_START,BUILD_ID,digest,read_ihex,read_symbols,
    verify_payload,validate_native,validate_nvm,ENCODER_ADDR,PHYSICAL,action,
    ERASE_START,MARKER_CHECK_START,validate_startup,ljmp)

def image_variants(root, meta):
    """Keep historical dual-image checks; trial-only releases cannot hide a permanent image."""
    trial_only = meta.get('trial_only', False)
    if not isinstance(trial_only, bool):
        raise ValueError('trial_only must be a boolean')
    variants = [('ak820-vial-trial.bin', True)]
    if trial_only:
        if (root / 'snapshot/ak820-vial-permanent.bin').exists():
            raise ValueError('A trial-only release contains a permanent image')
    else:
        variants.append(('ak820-vial-permanent.bin', False))
    expected = {name for name, _ in variants} | {'restore-native.bin'}
    if set(meta['images']) != expected:
        raise ValueError('Image manifest does not match the declared release variants')
    return variants


def check(root):
    meta=json.loads((root/'snapshot/images.json').read_text())
    variants=image_variants(root,meta)
    stock=(root/'reference/stock-full.bin').read_bytes()
    native=(root/'reference/native-installed.bin').read_bytes()
    backup=(root/'snapshot/before-full-rom.bin').read_bytes()
    validate_native(backup,stock,native)
    assert digest(backup)==meta['backup_sha256']
    assert (root/'snapshot/restore-native.bin').read_bytes()==backup[APP_START:APP_END]
    data=read_ihex(root/'firmware/application.ihx')
    symbols=read_symbols(root/'firmware/application.map')
    validate_startup(data,symbols)
    usb=validate_usb_image(root/'firmware/application.ihx',root/'firmware/application.map',
                           json.loads((root/'reference/info.json').read_text()),
                           'vial:f64c2b3c')
    images={}
    for name,trial in variants:
        blob=(root/'snapshot'/name).read_bytes()
        info=verify_payload(blob)
        assert info['trial']==trial and info['sha256']==meta['images'][name]['sha256']
        prefix=bytes.fromhex('75a80075e80075d00075812053a2fa75a15575a1aa53b1fde4f5a1')
        entry=(prefix+bytes.fromhex('7fc07e2712')+ERASE_START.to_bytes(2,'big')+ljmp(MARKER_CHECK_START)
               if trial else prefix+ljmp(CODE_START))
        assert blob[:len(entry)]==entry
        assert not any(blob[len(entry):ERASE_START-APP_START])
        assert blob[ERASE_START-APP_START:ERASE_START-APP_START+0x57]==stock[0xE650:0xE6A7]
        assert blob[MARKER_CHECK_START-APP_START:MARKER_CHECK_START-APP_START+17]==bytes.fromhex('9027c07f40e4937006a3dff902302780fe')
        assert ERASE_START+0x57<=MARKER_CHECK_START and MARKER_CHECK_START+17<=LOW_START
        for a,v in data.items():
            assert blob[a-APP_START]==v,(name,hex(a))
        callbacks={1:'_ak820_timer_irq',7:'_USB_DeviceInterrupt',10:'_ak820_led_irq'}
        for i in range(13):
            value=blob[0x3000-APP_START+i*3:0x3003-APP_START+i*3]
            expected=(b'\x02'+symbols[callbacks[i]].to_bytes(2,'big')) if i in callbacks else b'\x22\0\0'
            assert value==expected
        irq_at=symbols['_ak820_led_irq']-APP_START
        irq=blob[irq_at:irq_at+400]
        # Independent comparison against immutable OEM machine instructions:
        # DMA transfer cadence, key sense settling, and16 output selectors.
        for start,end in ((0xE274,0xE29D),(0xD5ED,0xD612),(0xE2B1,0xE2E1)):
            assert stock[start:end] in irq,(hex(start),hex(end))
        nvm=blob[NVM_START-APP_START:NVM_END-APP_START]
        assert nvm[:2]==bytes.fromhex('e6fe') and nvm[3]==1
        assert nvm[37:40]==BUILD_ID.to_bytes(3,'little')
        validate_nvm(nvm)
        assert nvm[24:32]==bytes((5,0,255,80,96,255,0,0))
        assert nvm[0x40+85*2:0x42+85*2]==bytes.fromhex('5221')
        for slot in PHYSICAL:
            assert int.from_bytes(nvm[0x40+2*slot:0x42+2*slot],'big')==action(backup[0xA100+3*slot:0xA103+3*slot])
        assert struct.unpack_from('>4H',nvm,ENCODER_ADDR)==(0xA9,0xAA,0xBB,0xBC)
        assert nvm[0x240:ENCODER_ADDR] == b'\x00\x01' * 512
        assert nvm[ENCODER_ADDR+8:ENCODER_ADDR+24] == b'\x00\x01' * 8
        assert not any(blob[NVM_END-APP_START:MANIFEST_START-APP_START])
        # Exactly one embedded XZ-compressed Vial definition must match source.
        magic=bytes.fromhex('fd377a585a00')
        starts=[i for i in range(len(blob)) if blob.startswith(magic,i)]
        assert len(starts)==1
        decoder=lzma.LZMADecompressor()
        definition=json.loads(decoder.decompress(blob[starts[0]:]))
        assert definition==json.loads((root/'reference/vial.json').read_text())
        assert definition['matrix']=={'rows':16,'cols':8}
        assert definition['lighting']=='vialrgb'
        device_at=symbols['_DeviceDescriptor']-APP_START
        device=blob[device_at:device_at+18]
        assert device[0:2]==bytes((18,1)) and device[7]==64
        assert device[8:12]==bytes.fromhex('0f325b50')
        config_at=symbols['_ConfigurationDescriptor']-APP_START
        config=blob[config_at:config_at+84]
        assert config[:5]==bytes((9,2,84,0,3))
        eps=[];at=0
        while at<len(config):
            length,kind=config[at:at+2]
            assert length>=2 and at+length<=len(config)
            if kind==5:eps.append(config[at+2])
            at+=length
        assert set(eps)=={0x81,0x82,0x83} and len(eps)==3
        # Damaged bytes in code and config are rejected independently of the
        # outer JSON hash, as is a full-ROM/truncated payload.
        for index in (0,CODE_START-APP_START,NVM_START-APP_START):
            bad=bytearray(blob);bad[index]^=1
            try:verify_payload(bad)
            except ValueError:pass
            else:raise AssertionError('Changed byte accepted')
        images[name]=info
    if not meta.get('trial_only',False):
        a=(root/'snapshot/ak820-vial-trial.bin').read_bytes()
        b=(root/'snapshot/ak820-vial-permanent.bin').read_bytes()
        assert a[ERASE_START-APP_START:MANIFEST_START-APP_START]==b[ERASE_START-APP_START:MANIFEST_START-APP_START]
    return {'result':'PASS','images':images,'usb_descriptors':usb,'compiled_bytes':len(data),
            'trial_only':meta.get('trial_only',False),
            'low_code_bytes':sum(LOW_START<=a<LOW_END for a in data),
            'main_code_bytes':sum(CODE_START<=a<CODE_END for a in data),
            'highest_code_address':hex(max(data)),
            'validated':'exact IHEX bytes, callback routing, OEM DMA/settling/selector instruction sequences, protected references, entry, NVM migration, compressed Vial definition, emitted USB/HID descriptors and UTF-16LE strings, integrity rejection',
            'usb_opened':False,'device_write_performed':False,'hardware_validated':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('release',type=Path)
    p.add_argument('--report',type=Path)
    a=p.parse_args()
    result=json.dumps(check(a.release),indent=2)+'\n'
    if a.report:a.report.write_text(result)
    print(result)
