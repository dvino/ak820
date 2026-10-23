#!/usr/bin/env python3
"""AK820 offline plan, live backup, explicit update and readback verification.

No USB is opened for `plan`. Only `flash` writes firmware. Installing this file
does not install a service, driver, keyboard hook or resident helper.
"""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
from pack_ak820 import (APP_START,APP_END,CODE_END,NVM_START,NVM_END,MANIFEST_START,
                       STOCK_SHA,NATIVE_SHA,digest,pack,read_ihex,read_symbols,
                       verify_payload,write_package,validate_native)

ROOT=Path(__file__).resolve().parents[1]
IMAGES={'trial':'ak820-vial-trial.bin','permanent':'ak820-vial-permanent.bin','restore':'restore-native.bin'}


def hid_module():
    try:
        import hid
        return hid
    except ImportError as e:
        raise RuntimeError('Install Python package hidapi: python -m pip install hidapi') from e


def select_application():
    candidates=[d for d in hid_module().enumerate(0x320F,0x505B)
                if (d.get('usage_page'),d.get('usage')) in ((0xFF1C,0x92),(0xFF60,0x61))]
    if len(candidates)!=1:
        raise RuntimeError('Connect exactly one supported AK820 application and close other configurators')
    return candidates[0]


class Application:
    def __init__(self, descriptor=None):
        selected=select_application()
        if descriptor is not None and selected.get('path')!=descriptor.get('path'):
            raise RuntimeError('Application identity changed since selection; no device opened')
        self.descriptor=selected
        self.native=self.descriptor['usage_page']==0xFF1C
        self.dev=hid_module().device()
        self.dev.open_path(self.descriptor['path'])

    def close(self):
        self.dev.close()

    def raw(self,packet):
        if self.native or len(packet)!=32:
            raise ValueError('Expected Vial32-byte packet')
        if self.dev.write(b'\0'+packet)!=33:
            raise OSError('Short Raw HID write')
        result=bytes(self.dev.read(32,2500))
        if len(result)!=32:
            raise TimeoutError('No complete Raw HID reply')
        return result

    def rom(self,address,size):
        if not 0<=address<=65536 or size<0 or address+size>65536:
            raise ValueError('ROM read outside bounds')
        result=bytearray()
        chunk_size=24 if self.native else 27
        for delta in range(0,size,chunk_size):
            count=min(chunk_size,size-delta)
            addr=address+delta
            if self.native:
                request=bytearray(64)
                request[0]=4;request[3]=7;request[4]=count
                request[5:7]=((addr-0x7077)&65535).to_bytes(2,'little')
                request[1:3]=(sum(request[3:])&65535).to_bytes(2,'little')
                reply=None
                for attempt in range(3):
                    if self.dev.write(request)!=64:
                        raise OSError('Short native HID write')
                    end=time.monotonic()+2
                    while time.monotonic()<end:
                        candidate=bytes(self.dev.read(64,200))
                        if len(candidate)==64 and candidate[0]==4 and candidate[3:7]==request[3:7]:
                            if candidate[7]:
                                raise OSError('Native ROM read rejected')
                            reply=candidate;break
                    if reply is not None:
                        break
                if reply is None:
                    raise TimeoutError('Native ROM read timed out')
                result.extend(reply[8:8+count])
            else:
                request=bytes((0xFD,0,addr>>8,addr&255,count))+bytes(27)
                reply=self.raw(request)
                if reply[:5]!=request[:5]:
                    raise OSError('Unexpected diagnostic ROM reply')
                result.extend(reply[5:5+count])
            time.sleep(.001)
        return bytes(result)

    def vial_unlock_status(self, *, poll=False):
        request=bytes((0xFE, 7 if poll else 5))+bytes(30)
        reply=self.raw(request)
        if reply[0] not in (0,1) or reply[1] not in (0,1):
            raise ValueError('Malformed Vial unlock status')
        if poll:
            if reply[2]>30 or (reply[0] and (reply[1] or reply[2])):
                raise ValueError('Malformed Vial unlock counter')
        elif reply[2:] != bytes((0,0,0,5))+bytes((255,))*26:
            raise ValueError('Unexpected Vial physical unlock combination')
        return tuple(reply[:3]) if poll else tuple(reply[:2])

    def vial_unlock_command(self, command):
        if command not in (6,8):
            raise ValueError('Unsupported Vial unlock command')
        request=bytes((0xFE,command))+bytes(30)
        if self.raw(request)!=request:
            raise ValueError('Vial unlock command rejected')

    def enter_vial_loader(self):
        request=bytes((0x0B,))+bytes(31)
        if self.raw(request)!=request:
            raise ValueError('Vial bootloader command rejected')
        # The echo alone does not prove acceptance. Caller must find the loader.

    def enter_native_loader(self):
        if not self.native:
            raise RuntimeError('For the trial firmware, unplug/replug to enter its loader; for permanent firmware use Vial Unlock + Bootloader')
        if self.dev.write(bytes.fromhex('04eeee00')+bytes(60))!=64:
            raise OSError('Short loader transition write')


def loader_packet(command,first=0,second=0):
    packet=bytearray(64)
    packet[:4]=bytes((command,0xAA,0x55,0))
    packet[4:8]=first.to_bytes(4,'little')
    packet[8:12]=second.to_bytes(4,'little')
    return bytes(packet)


def loader_reply(reply,command):
    if len(reply)!=65 or reply[:5]!=bytes((0,command,0xAA,0x55,0)) or reply[5:9]!=bytes.fromhex('fafafafa'):
        raise ValueError('Unexpected loader reply/failed status')
    if command==1 and reply[9:13]!=bytes.fromhex('00112233'):
        raise ValueError('Unexpected loader identity')


def session_image(session,name):
    manifest=json.loads((session/'images.json').read_text(encoding='utf-8'))
    filename=IMAGES[name]
    payload=(session/filename).read_bytes()
    spec=manifest['images'][filename]
    if len(payload)!=APP_END-APP_START or digest(payload)!=spec['sha256'] or len(payload)!=spec['size']:
        raise ValueError('Image size/hash mismatch')
    backup=(session/'before-full-rom.bin').read_bytes()
    if len(backup)!=65536 or digest(backup)!=manifest['backup_sha256']:
        raise ValueError('Missing or damaged recovery backup')
    recovery=(session/'restore-native.bin').read_bytes()
    if recovery!=backup[APP_START:APP_END] or digest(recovery)!=manifest['images']['restore-native.bin']['sha256']:
        raise ValueError('Recovery image does not match the full backup')
    if name!='restore':
        info=verify_payload(payload)
        if info['trial']!=(name=='trial'):
            raise ValueError('Trial/permanent image mismatch')
    return manifest,payload,backup


def plan(session,name):
    _,payload,_=session_image(session,name)
    return {'image':IMAGES[name],'size':len(payload),'sha256':digest(payload),
            'start_address':'0x2800','end_exclusive':'0xEFC0','data_blocks':len(payload)//64,
            'checksum':sum(payload)&0xFFFFFFFF,'usb_opened':False,'device_write_performed':False}


def prepare(session):
    if session.exists():
        raise ValueError('Use a new session directory')
    app=Application()
    try:
        if not app.native:
            raise ValueError('Initial migration requires the known native Fn-layer firmware')
        print('Reading65536-byte native ROM; no flash writes...',flush=True)
        live=app.rom(0,65536)
        # Detect settings changing during a multi-second read.
        if app.rom(0xA000,0x3380)!=live[0xA000:0xD380]:
            raise RuntimeError('Settings changed while reading; close configurators and retry')
    finally:
        app.close()
    backups=ROOT/'backups'
    backups.mkdir(exist_ok=True)
    path=backups/f'native-{time.time_ns()}.bin'
    path.write_bytes(live)
    print('Backup:',path,flush=True)
    metadata=write_package(ROOT/'firmware/application.ihx',ROOT/'firmware/application.map',
                           ROOT/'reference/stock-full.bin',ROOT/'reference/native-installed.bin',path,session)
    print(json.dumps({'session':str(session),'backup_sha256':metadata['backup_sha256'],
                      'images':metadata['images'],'migration':metadata['migration']},ensure_ascii=False,indent=2))


def verify_live(live,expected,name,stock):
    if len(live)!=65536:
        raise ValueError('Unexpected full-ROM reference')
    validate_native(stock)
    if live[:0x27C0]!=stock[:0x27C0] or live[APP_END:]!=stock[APP_END:]:
        raise ValueError('Protected loader/tail verification failed')
    if name=='restore':
        if live[APP_START:APP_END]!=expected:
            raise ValueError('Restored native application/settings differ')
    else:
        if live[APP_START:CODE_END]!=expected[:CODE_END-APP_START] or live[MANIFEST_START:APP_END]!=expected[MANIFEST_START-APP_START:]:
            raise ValueError('Application code/readback does not match the selected image')
        # A completed transaction erases only its 64-byte header at EF40.
        # The preceding data page may retain the last successfully saved page.
        if any(live[NVM_END+64:MANIFEST_START]):
            raise ValueError('NVM journal header is not empty; retry after idle, investigate if persistent')
        # Read-only validation accepts a known older schema for explicit offline
        # migration. session_image/flash still reject an old application image.
        from pack_ak820 import validate_nvm
        metadata=verify_payload(expected,allow_legacy=True)
        validate_nvm(live[NVM_START:NVM_END],metadata['build_id'])
    marker=live[0x27C0:0x2800]
    if name=='trial':
        if any(marker):
            raise ValueError('Trial did not clear the boot marker; recovery on reset is not established')
    elif marker[:4]!=bytes.fromhex('aa5533cc'):
        raise ValueError('Permanent application validity marker is missing')


def verify(session,name):
    _,payload,_=session_image(session,name)
    app=Application()
    try:
        if app.native!=(name=='restore'):
            raise ValueError('Unexpected application transport')
        live=app.rom(0,65536)
        if name!='restore' and app.rom(NVM_START,NVM_END-NVM_START)!=live[NVM_START:NVM_END]:
            raise RuntimeError('Settings changed during readback; close Vial and retry')
    finally:
        app.close()
    stamp=str(time.time_ns())
    romfile=session/f'readback-{name}-{stamp}.bin'
    romfile.write_bytes(live)
    verify_live(live,payload,name,(ROOT/'reference/stock-full.bin').read_bytes())
    report={'image':name,'image_sha256':digest(payload),'readback':romfile.name,'readback_sha256':digest(live),
            'code_and_protected_regions_match':True,'marker_verified':True,
            'physical_key_rgb_encoder_tests':'not measured by this readback tool',
            'device_write_performed':False}
    (session/f'{name}-readback.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


def prepare_permanent(session):
    manifest,trial,_=session_image(session,'trial')
    stock=(ROOT/'reference/stock-full.bin').read_bytes()
    ihx,mapfile=ROOT/'firmware/application.ihx',ROOT/'firmware/application.map'
    for path,key in ((ihx,'ihx_sha256'),(mapfile,'map_sha256')):
        if digest(path.read_bytes())!=manifest.get(key):
            raise ValueError(f'Trial session build identity is missing or differs from this release: {path.name}')
    data,symbols=read_ihex(ihx),read_symbols(mapfile)
    # Bind the parsed code, constants, callbacks and bootstrap to the verified
    # session image too. Repacking its original settings must reproduce it.
    if pack(data,symbols,stock,trial[NVM_START-APP_START:NVM_END-APP_START],True)!=trial:
        raise ValueError('Current build inputs do not reproduce the session trial image')
    app=Application()
    try:
        if app.native:
            raise ValueError('Expected running Vial trial')
        live=app.rom(0,65536)
        if app.rom(NVM_START,NVM_END-NVM_START)!=live[NVM_START:NVM_END]:
            raise RuntimeError('Settings changed during readback; close Vial and retry')
    finally:
        app.close()
    (session/f'pre-permanent-{time.time_ns()}.bin').write_bytes(live)
    verify_live(live,trial,'trial',stock)
    permanent=pack(data,symbols,stock,live[NVM_START:NVM_END],False)
    metadata=verify_payload(permanent)
    (session/IMAGES['permanent']).write_bytes(permanent)
    manifest['images'][IMAGES['permanent']]=metadata
    manifest['permanent_prepared_from_verified_trial']=digest(live)
    (session/'images.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'permanent':metadata,'settings':'copied from verified running trial; native recovery backup retained'},indent=2))


UPDATE_PINS = {
    'ihx_sha256': 'd2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce',
    'map_sha256': '9e1ef5262685ea85f3362b378c28836d2af9b51f6699b970c61bafdf3dd5b000',
    'payload': '54290ce406fda133bd90703664f60559e23620f184f89033c98dddb56e2299ed',
    'snapshot': 'bf7bc0f89b7f17223384864a21699cb510fd573f2587277a9fb7d846ddd01333',
    'backup': '1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1',
}


def validate_prepared_update(session, snapshot=None):
    """Admit only the reviewed RC6 repair pair, never arbitrary update images."""
    manifest, payload, backup = session_image(session, 'permanent')
    if (any(manifest.get(key) != UPDATE_PINS[key] for key in ('ihx_sha256', 'map_sha256')) or
            digest(payload) != UPDATE_PINS['payload'] or digest(backup) != UPDATE_PINS['backup']):
        raise ValueError('Update requires the exact reviewed candidate and personal recovery backup')
    if snapshot is not None:
        current = Path(snapshot).read_bytes()
        if len(current) != 65536 or digest(current) != UPDATE_PINS['snapshot']:
            raise ValueError('Update requires the exact freshly saved fault snapshot')
        if (current[:APP_START] != backup[:APP_START] or current[APP_END:] != backup[APP_END:] or
                current[NVM_START:NVM_END] != payload[NVM_START-APP_START:NVM_END-APP_START] or
                payload[NVM_END-APP_START:0xEF80-APP_START] != bytes(0x80)):
            raise ValueError('Update protected regions, durable settings or cleared journal differ')
    return manifest, payload, backup


def flash(session,name,enter_loader,accept_hardware_check,*,reference_dir=None,
          application_descriptor=None,loader_descriptor=None,phase_guard=None,
          native_install=False, prepared_update_snapshot=None, host_update_snapshot=None):
    """Use the unchanged OEM loader protocol with optional orchestration guards.

    A guard is called before reset/erase/restart, after the corresponding local
    and identity checks. It must raise to refuse an operation. Frontends collect
    explicit consent before reset, while the user's keyboard can still type.
    ``reference_dir`` avoids depending on a historical archive directory layout.
    """
    manifest,payload,backup=session_image(session,name)
    references=Path(reference_dir) if reference_dir is not None else ROOT/'reference'
    stock=(references/'stock-full.bin').read_bytes()
    native=(references/'native-installed.bin').read_bytes()
    validate_native(backup,stock,native)
    if native_install:
        if (name != 'permanent' or not enter_loader or phase_guard is None or application_descriptor is None or
                manifest.get('native_install_backup_sha256') != digest(backup) or
                manifest.get('nvm_provenance') != {'mode': 'native_backup', 'source_sha256': digest(backup)}):
            raise ValueError('Direct permanent installation requires a guarded fresh native backup workflow')
    prepared_update = prepared_update_snapshot is not None
    if prepared_update:
        if name != 'permanent' or enter_loader or native_install or phase_guard is None or loader_descriptor is None:
            raise ValueError('Prepared update requires a guarded, explicitly authorized loader')
        validate_prepared_update(session, prepared_update_snapshot)
    host_update = host_update_snapshot is not None
    if host_update:
        if (name != 'permanent' or enter_loader or native_install or prepared_update or
                phase_guard is None or loader_descriptor is None):
            raise ValueError('Host update requires an exclusive guarded loader workflow')
        if host_update_snapshot != {'payload_sha256': digest(payload), 'backup_sha256': digest(backup)}:
            raise ValueError('Host update image/recovery binding changed')
        if manifest.get('nvm_provenance') != {'mode': 'native_backup', 'source_sha256': digest(backup)}:
            raise ValueError('Host update requires an original OEM migration')
    if name=='permanent' and not native_install and not prepared_update and not host_update and (not accept_hardware_check or 'permanent_prepared_from_verified_trial' not in manifest):
        raise ValueError('Verify physical operation of the trial, run prepare-permanent, then explicitly pass --accept-hardware-check')
    log=[]
    logfile=session/f'flash-{name}-{time.time_ns()}.json'
    def record(event,**fields):
        item={'time':time.time(),'event':event,**fields}
        log.append(item)
        logfile.write_text(json.dumps(log,indent=2)+'\n')
        print(event,fields,flush=True)
    record('image_and_recovery_validated',sha256=digest(payload),image=name)
    if enter_loader:
        if name!='trial' and not native_install:
            raise ValueError('--enter-loader is for the initial native-to-trial update only')
        if hid_module().enumerate(0x0C45,0x7687):
            raise RuntimeError('Loader already present; do not request a native transition')
        app=Application(application_descriptor) if application_descriptor is not None else Application()
        try:
            current=app.rom(0,65536)
            if current!=backup:
                raise RuntimeError('Live ROM differs from this session backup; run prepare into a new directory')
            record('native_backup_matches_before_transition')
            if phase_guard is not None:
                phase_guard('reset_to_loader',image=name,sha256=digest(payload))
            app.enter_native_loader()
        finally:
            app.close()
    deadline=time.monotonic()+10
    loader=None
    while time.monotonic()<deadline:
        matches=[d for d in hid_module().enumerate(0x0C45,0x7687)
                 if d.get('interface_number')==1 and d.get('usage_page')==12 and d.get('usage')==1]
        if len(matches)>1:
            raise RuntimeError('Multiple loader devices; no erase sent')
        if len(matches)==1:
            loader=matches[0];break
        time.sleep(.1)
    if loader is None:
        raise RuntimeError('OEM loader not found; no application erase sent')
    if loader_descriptor is not None and loader.get('path')!=loader_descriptor.get('path'):
        raise RuntimeError('Loader identity changed since selection; no erase sent')
    dev=hid_module().device()
    dev.open_path(loader['path'])
    def feature(packet):
        if dev.send_feature_report(b'\0'+packet)!=65:
            raise OSError('Incomplete loader feature report')
    def command(number,delay,first=0,second=0):
        feature(loader_packet(number,first,second))
        time.sleep(delay)
        reply=bytes(dev.get_feature_report(0,65))
        loader_reply(reply,number)
        record('command_accepted',command=number)
    try:
        command(1,.1)
        record('loader_identity_verified_before_erase')
        if phase_guard is not None:
            phase_guard('erase_and_flash',image=name,sha256=digest(payload),
                        loader_path=loader['path'])
        command(2,7.0)
        command(3,.1,APP_START,len(payload)//64)
        for offset in range(0,len(payload),64):
            feature(payload[offset:offset+64]);time.sleep(.01)
            if offset%4096==0:
                record('transferred',bytes=offset+64)
        command(4,1.0,0,sum(payload)&0xFFFFFFFF)
        record('loader_checksum_accepted',note='This is not a full-ROM readback or a physical functionality test')
        if phase_guard is not None:
            phase_guard('restart',image=name,sha256=digest(payload),loader_path=loader['path'])
        feature(loader_packet(5))
        record('restart_sent',note='Application startup and full-ROM readback are still required; loader acceptance is not success')
    finally:
        dev.close()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('inspect',help='Enumerate only, no firmware writes')
    for name in ('plan','prepare','verify','prepare-permanent','flash'):
        item=sub.add_parser(name)
        item.add_argument('--session',type=Path,required=True)
        if name in ('plan','verify','flash'):
            item.add_argument('--image',choices=IMAGES,default='trial')
        if name=='flash':
            item.add_argument('--enter-loader',action='store_true')
            item.add_argument('--accept-hardware-check',action='store_true')
    a=p.parse_args()
    if a.command=='inspect':
        fields=('vendor_id','product_id','interface_number','usage_page','usage','product_string')
        print(json.dumps([{k:d.get(k) for k in fields} for d in hid_module().enumerate()
                          if (d['vendor_id'],d['product_id']) in ((0x320F,0x505B),(0x0C45,0x7687))],indent=2))
    elif a.command=='plan':
        print(json.dumps(plan(a.session,a.image),indent=2))
    elif a.command=='prepare':
        prepare(a.session)
    elif a.command=='verify':
        verify(a.session,a.image)
    elif a.command=='prepare-permanent':
        prepare_permanent(a.session)
    elif a.command=='flash':
        flash(a.session,a.image,a.enter_loader,a.accept_hardware_check)


if __name__=='__main__':
    main()
