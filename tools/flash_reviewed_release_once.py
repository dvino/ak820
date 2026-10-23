#!/usr/bin/env python3
"""One-off reviewed update. Default preparation is offline; --execute writes USB.

Settings reset to the normal OEM migration. The local current-settings backup
is evidence only and is not restored. No firmware/protocol changes are needed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools/installer'))
import ak820 as installer
import ak820_tool as transport
import ak820_diagnose as diagnostic
import pack_ak820 as p

SOURCE_IHX = 'd2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce'
SOURCE_MAP = '9e1ef5262685ea85f3362b378c28836d2af9b51f6699b970c61bafdf3dd5b000'
TARGET_IHX = 'f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e'
FORMAT = 'ak820-oneoff-as-is-1'
SOURCE_BUILD = ROOT/'qmk-8051-ak820/.build/rc6-candidate-erase-20261023'


def sha(data): return hashlib.sha256(data).hexdigest()


def require(value, message):
    if not value: raise ValueError(message)


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf-8')


def checked_status(app):
    status = diagnostic.decode_status(app.raw(bytes((0xFD,1))+bytes(30)))
    require(not any(status[key] for key in ('storage_failed','page_dirty','batch_depth','first_failure_stage')),
            'Storage is dirty, batched or failed; stopped without retry')
    return status


def source_check(rom, source_image, stock):
    require(len(rom) == 65536, 'Incomplete source ROM')
    require(rom[:0x27C0] == stock[:0x27C0] and rom[p.APP_END:] == stock[p.APP_END:]
            and rom[0x27C0:0x27C4] == bytes.fromhex('aa5533cc'), 'Source protected regions or marker differ')
    require(rom[p.APP_START:p.CODE_END] == source_image[:p.CODE_END-p.APP_START]
            and rom[p.MANIFEST_START:p.MANIFEST_START+48] == source_image[p.MANIFEST_START-p.APP_START:p.MANIFEST_START-p.APP_START+48],
            'Installed source is not the exact supported d2d48 build')
    p.validate_nvm(rom[p.NVM_START:p.NVM_END])
    require(not any(rom[p.NVM_END+64:p.MANIFEST_START]), 'Source journal header is not empty')


def prepare(folder, snapshot, reference_dir):
    installer.load_release(approved=True)
    ihx, mapfile = installer.BUNDLE/'firmware/application.ihx', installer.BUNDLE/'firmware/application.map'
    source_ihx, source_map = SOURCE_BUILD/'ajazz_ak820_vial.ihx', SOURCE_BUILD/'ajazz_ak820_vial.map'
    require(sha(ihx.read_bytes()) == TARGET_IHX, 'Unexpected reviewed target')
    require(sha(source_ihx.read_bytes()) == SOURCE_IHX and sha(source_map.read_bytes()) == SOURCE_MAP, 'Unexpected source build inputs')
    backup = (ROOT/'evidence/oem-backup/before-full-rom.bin').read_bytes()
    stock, native = (reference_dir/name for name in ('stock-full.bin','native-installed.bin'))
    stock, native = stock.read_bytes(), native.read_bytes()
    p.validate_native(backup,stock,native)
    require(sha(backup) == installer.EXPECTED_OEM, 'Unexpected personal native backup')
    target_data, target_symbols = p.read_ihex(ihx), p.read_symbols(mapfile)
    nvm, migration = p.migrate(backup,target_data,target_symbols)
    image = p.pack(target_data,target_symbols,stock,nvm,False)
    old_data, old_symbols = p.read_ihex(source_ihx), p.read_symbols(source_map)
    old_nvm, _ = p.migrate(backup,old_data,old_symbols)
    old = p.pack(old_data,old_symbols,stock,old_nvm,False)
    rom = snapshot.read_bytes()
    source_check(rom,old,stock)
    files = {'source-rom.bin':rom,'source-image.bin':old,'native-backup.bin':backup,
             'stock-full.bin':stock,'native-installed.bin':native,'payload.bin':image,
             'settings-backup.bin':rom[p.NVM_START:p.NVM_END],
             'target.ihx':ihx.read_bytes(),'target.map':mapfile.read_bytes(),
             'source.ihx':source_ihx.read_bytes(),'source.map':source_map.read_bytes()}
    manifest = {'format':FORMAT,'settings_policy':'reset to original native migration; local backup is not restored',
                'migration':migration,'runner_sha256':sha(Path(__file__).read_bytes()),
                'files':{name:{'size':len(data),'sha256':sha(data)} for name,data in files.items()}}
    folder.mkdir(parents=True,exist_ok=False)
    for name,data in files.items(): (folder/name).write_bytes(data)
    save_json(folder/'oneoff.json',manifest)
    validate(folder)
    print('Offline session:',folder,'\nPayload SHA256:',sha(image),'\nSettings will reset; backup is not restored.')


def validate(folder, identity=None):
    raw = (folder/'oneoff.json').read_bytes()
    if identity is not None: require(sha(raw) == identity,'Session manifest changed')
    manifest = json.loads(raw)
    names = {'source-rom.bin','source-image.bin','native-backup.bin','stock-full.bin','native-installed.bin',
             'payload.bin','settings-backup.bin','target.ihx','target.map','source.ihx','source.map'}
    require(manifest.get('format') == FORMAT and set(manifest.get('files',{})) == names,'Unknown one-off session')
    require(manifest.get('runner_sha256') == sha(Path(__file__).read_bytes()),'Runner changed since preparation')
    files = {name:(folder/name).read_bytes() for name in names}
    for name,data in files.items(): require(manifest['files'][name] == {'size':len(data),'sha256':sha(data)},'Changed file: '+name)
    installer.load_release(approved=True)
    require(files['target.ihx'] == (installer.BUNDLE/'firmware/application.ihx').read_bytes()
            and files['target.map'] == (installer.BUNDLE/'firmware/application.map').read_bytes()
            and sha(files['target.ihx']) == TARGET_IHX,'Target differs from approved release')
    require(sha(files['source.ihx']) == SOURCE_IHX and sha(files['source.map']) == SOURCE_MAP,'Source input identity differs')
    backup,stock = files['native-backup.bin'],files['stock-full.bin']
    p.validate_native(backup,stock,files['native-installed.bin'])
    require(sha(backup) == installer.EXPECTED_OEM,'Native backup identity differs')
    for prefix,filename in (('target','payload.bin'),('source','source-image.bin')):
        data,symbols = p.read_ihex(folder/(prefix+'.ihx')),p.read_symbols(folder/(prefix+'.map'))
        nvm,_ = p.migrate(backup,data,symbols)
        require(p.pack(data,symbols,stock,nvm,False) == files[filename],'Packed image does not reproduce '+prefix)
    source_check(files['source-rom.bin'],files['source-image.bin'],stock)
    require(files['settings-backup.bin'] == files['source-rom.bin'][p.NVM_START:p.NVM_END],'Settings backup differs')
    return files


def flash_once(folder, identity, hid, loader, image):
    """Unchanged OEM packet format; exactly one erase/transfer/checksum/restart."""
    files = validate(folder,identity)
    require(image == files['payload.bin'] and len(image) == p.APP_END-p.APP_START,'Loader payload differs from validated session')
    require(installer.require_state(hid,'LOADER',loader['path'])['path'] == loader['path'],'Loader changed')
    device = hid.device(); device.open_path(loader['path'])
    events = []
    def feature(packet):
        require(device.send_feature_report(b'\0'+packet) == 65,'Short loader feature report')
    def command(number,delay,first=0,second=0):
        events.append(number); save_json(folder/'loader-events.json',events)
        feature(transport.loader_packet(number,first,second)); time.sleep(delay)
        transport.loader_reply(bytes(device.get_feature_report(0,65)),number)
    try:
        command(1,.1)
        validate(folder,identity)
        installer.require_state(hid,'LOADER',loader['path'])
        command(2,7)
        command(3,.1,p.APP_START,len(image)//64)
        for offset in range(0,len(image),64): feature(image[offset:offset+64]); time.sleep(.01)
        command(4,1,0,sum(image)&0xffffffff)
        validate(folder,identity)
        installer.require_state(hid,'LOADER',loader['path'])
        events.append(5); save_json(folder/'loader-events.json',events)
        feature(transport.loader_packet(5))
    finally: device.close()


def execute(folder):
    require(not (folder/'execution-started.json').exists(),'This one-off session was already attempted; no retry')
    identity = sha((folder/'oneoff.json').read_bytes())
    files = validate(folder,identity)
    hid = installer.hid_module()
    selected = installer.require_state(hid,'VIAL_APP')
    app = transport.Application(selected)
    try:
        status = checked_status(app)
        rom = app.rom(0,65536)
        (folder/'fresh-preflash-rom.bin').write_bytes(rom)
        (folder/'fresh-settings-backup.bin').write_bytes(rom[p.NVM_START:p.NVM_END])
        save_json(folder/'fresh-preflash-status.json',status)
        source_check(rom,files['source-image.bin'],files['stock-full.bin'])
        require(rom == files['source-rom.bin'],'Current ROM changed; prepare a new session explicitly')
        require(app.rom(p.NVM_START,p.MANIFEST_START-p.NVM_START) == rom[p.NVM_START:p.MANIFEST_START], 'Settings changed during backup')
        checked_status(app)
        validate(folder,identity)
        print('SETTINGS WILL RESET. Local backup is NOT restored. / Настройки сбросятся; локальная копия не восстанавливается.\n'
              'Payload SHA256: '+sha(files['payload.bin'])+'\n'
              'Hold Esc + left Ctrl 3 seconds. Keep alternate input and stable power. / '
              'Удерживайте Esc + левый Ctrl 3 секунды. Подготовьте запасную клавиатуру и стабильное питание.',flush=True)
        save_json(folder/'execution-started.json',{'source_sha256':sha(rom),'payload_sha256':sha(files['payload.bin'])})
        app.vial_unlock_command(8)
        require(app.vial_unlock_status() == (0,0),'Fresh Vial lock failed')
        app.vial_unlock_command(6)
        require(app.vial_unlock_status() == (0,1),'Fresh physical unlock did not start')
        deadline = time.monotonic()+120
        while True:
            require(time.monotonic()<deadline,'Physical consent timeout; no automatic retry')
            installer.require_state(hid,'VIAL_APP',selected['path'])
            unlocked,active,counter = app.vial_unlock_status(poll=True)
            if (unlocked,active,counter) == (1,0,0): break
            require(unlocked == 0 and active == 1,'Physical consent rejected')
            time.sleep(.1)
        validate(folder,identity)
        checked_status(app)
        require(app.rom(0,65536) == rom,'ROM changed after confirmation; no loader entry')
        require(app.vial_unlock_status() == (1,0),'Physical unlock changed')
        installer.require_state(hid,'VIAL_APP',selected['path'])
        app.enter_vial_loader()
    finally: app.close()
    loader = installer.wait_state(hid,'LOADER',seconds=25)
    flash_once(folder,identity,hid,loader,files['payload.bin'])
    running = installer.wait_state(hid,'VIAL_APP')
    app = transport.Application(running)
    try:
        rom = app.rom(0,65536)
        (folder/'postflash-rom.bin').write_bytes(rom)
        status = checked_status(app)
        save_json(folder/'postflash-status.json',status)
        transport.verify_live(rom,files['payload.bin'],'permanent',files['stock-full.bin'])
        require(rom[p.NVM_START:p.NVM_END] == files['payload.bin'][p.NVM_START-p.APP_START:p.NVM_END-p.APP_START], 'Initial target NVM differs')
        require(app.rom(p.NVM_START,p.MANIFEST_START-p.NVM_START) == rom[p.NVM_START:p.MANIFEST_START], 'Target settings changed during readback')
        checked_status(app)
    finally: app.close()
    save_json(folder/'result.json',{'passed':True,'payload_sha256':sha(files['payload.bin']),
              'rom_sha256':sha(rom),'settings_restored':False,'physical_typing':'not tested','power_loss_persistence':'not tested'})
    print('CODE, protected regions and initial NVM verified. Physical typing and power-loss persistence not tested.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session',type=Path,required=True)
    parser.add_argument('--source-rom',type=Path)
    parser.add_argument('--reference-dir',type=Path)
    parser.add_argument('--execute',action='store_true')
    args = parser.parse_args(argv)
    if args.execute:
        require(args.source_rom is None and args.reference_dir is None,'Execution uses only the prepared session')
        execute(args.session)
    else:
        require(args.source_rom is not None and args.reference_dir is not None,'Offline preparation needs --source-rom and --reference-dir')
        prepare(args.session,args.source_rom,args.reference_dir)
    return 0


if __name__ == '__main__':
    try: raise SystemExit(main())
    except (Exception,KeyboardInterrupt) as error:
        print('STOPPED; no automatic retry, reset, restore or recovery:',error,file=sys.stderr)
        raise SystemExit(1)
