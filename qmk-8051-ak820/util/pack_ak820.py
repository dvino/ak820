#!/usr/bin/env python3
"""Package the linked AK820 application; never opens a USB device.

Input and output addresses are absolute in metadata. Device update binaries
contain only 0x2800..0xEFBF, as required by the unchanged OEM loader.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

APP_START, APP_END = 0x2800, 0xEFC0
CODE_START, CODE_END = 0x3027, 0xC700
LOW_START, LOW_END = 0x28A0, 0x3000
ERASE_START, MARKER_CHECK_START = 0x2830, 0x2888
NVM_START, NVM_END = 0xC700, 0xEF00
MANIFEST_START = 0xEF80
BUILD_ID = 0x082002
EXTENSION_BUILD_ID = 0x082003
LEGACY_BUILD_ID = 0x082001
LAYER_COUNT = 6
KEYMAP_ADDR = 0x0040
ENCODER_ADDR = KEYMAP_ADDR + LAYER_COUNT * 256
MACRO_ADDR, MACRO_SIZE, MACRO_COUNT = 0x0800, 8192, 16
MACRO_BUSY_ADDR = 0x07F0
STOCK_SHA = '03c6bd3351f272c855b9bc736d597170f694b5260b2001d1fc9cbfba8b382994'
NATIVE_SHA = 'd7152819712470cf37a0c29d69b756edc4a51aca1d20c13e1fcf4b96f9638535'
NATIVE_PUBLIC_SHA = '29446ba54e21990dbb5cbb1df542df9dc0c59b3b5f0098dcfdf13ee3a780faf6'
NATIVE_REFERENCE_HASHES = frozenset((NATIVE_SHA, NATIVE_PUBLIC_SHA))
MAGIC = b'AKV1PKG\0'
MATRIX_MASK = (0x3F,0x2F,0x3F,0x1F,0x1F,0x3F,0x1F,0x1F,0x1F,0x3F,0x3F,0x3F,0x07,0x3F,0x3C,0x2E)
PHYSICAL = tuple(r*8+c for r,m in enumerate(MATRIX_MASK) for c in range(8) if m & (1<<c))
MEDIA = {0xE2:0xA8,0xE9:0xA9,0xEA:0xAA,0xB5:0xAB,0xB6:0xAC,
         0xB7:0xAD,0xCD:0xAE,0x183:0xAF,0xB8:0xB0,0x18A:0xB1,
         0x192:0xB2,0x194:0xB3,0x221:0xB4,0x223:0xB5,0x224:0xB6,
         0x225:0xB7,0x226:0xB8,0x227:0xB9,0x22A:0xBA,0xB3:0xBB,0xB4:0xBC}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_ihex(path):
    data, base, eof = {}, 0, False
    for line in path.read_text().splitlines():
        if eof or not line.startswith(':'):
            raise ValueError('Malformed HEX or record after EOF')
        record = bytes.fromhex(line[1:])
        if len(record)<5 or len(record)!=record[0]+5 or sum(record)&255:
            raise ValueError('HEX checksum/length mismatch')
        n, kind = record[0], record[3]
        addr = int.from_bytes(record[1:3],'big')
        raw = record[4:-1]
        if kind==0:
            for i,v in enumerate(raw):
                a=base+addr+i
                if not (CODE_START<=a<CODE_END or LOW_START<=a<LOW_END):
                    raise ValueError(f'Code outside application window: {a:04X}')
                if a in data and data[a]!=v:
                    raise ValueError('Conflicting HEX records')
                data[a]=v
        elif kind==1 and n==0 and addr==0:
            eof=True
        elif kind in (2,4) and n==2 and addr==0:
            base=int.from_bytes(raw,'big')<<(4 if kind==2 else 16)
        else:
            raise ValueError('Unexpected HEX record')
    if not eof or not data or CODE_START not in data:
        raise ValueError('Incomplete linked application')
    return data


def read_symbols(path):
    return {name:int(address,16) for address,name in
            re.findall(r'^C:\s+([0-9A-Fa-f]{8})\s+(\S+)',path.read_text(),re.M)}


def code_bytes(data,address,count):
    try:
        return bytes(data[a] for a in range(address,address+count))
    except KeyError as e:
        raise ValueError('Missing compiled constant data') from e



def factory_keymaps(data, symbols):
    """Decode the two compiled default layers into 256 little-endian keys."""
    names = ('_ak820_default_classes', '_ak820_default_offsets',
             '_ak820_default_payload')
    compressed = [name in symbols for name in names]
    if '_keymaps' in symbols:
        if any(compressed):
            raise ValueError('Ambiguous compiled default keymaps')
        return code_bytes(data, symbols['_keymaps'], 512)
    if not all(compressed):
        raise ValueError('Missing compressed default keymap tables')
    classes = code_bytes(data, symbols[names[0]], 64)
    offsets = code_bytes(data, symbols[names[1]], 32)
    cursor, keys = 0, []
    for row in range(32):
        if offsets[row] != cursor:
            raise ValueError('Non-contiguous default keymap payload')
        for col in range(8):
            kind = (classes[row * 2 + col // 4] >> ((col % 4) * 2)) & 3
            if kind < 2:
                value = kind
            else:
                raw = code_bytes(data, symbols[names[2]] + cursor, kind - 1)
                value = int.from_bytes(raw, 'little')
                if value < (2 if kind == 2 else 256):
                    raise ValueError('Non-canonical default keymap encoding')
                cursor += kind - 1
            keys.append(value)
    if cursor > 255:
        raise ValueError('Default keymap payload exceeds byte offsets')
    ranges = [(symbols[names[0]], 64), (symbols[names[1]], 32),
              (symbols[names[2]], cursor)]
    for index, (start, count) in enumerate(ranges):
        for other, size in ranges[index + 1:]:
            if count and size and max(start, other) < min(start + count, other + size):
                raise ValueError('Overlapping default keymap tables')
    return struct.pack('<256H', *keys)


def action(record, stock_default=None):
    if len(record)!=3:
        raise ValueError('Invalid native action length')
    kind,arg,key=record
    if record==b'\xff\xff\xff' and stock_default is not None:
        return stock_default
    if record==bytes.fromhex('a00100'):
        return 0x5221  # MO(1), QMK keycodes.h in the pinned tree
    if kind==0x70 and key==0 and arg<16:
        return 0x7700+arg
    if kind==0x30 and (arg|(key<<8)) in MEDIA:
        return MEDIA[arg|(key<<8)]
    if kind==0x20 and (key<=0xA4 or 0xE0<=key<=0xE7):
        if key==0 and arg and not arg&(arg-1):
            return 0xE0+arg.bit_length()-1
        if arg==0:
            return key
        if not arg&0xF0:
            return (arg<<8)|key
        if not arg&0x0F:
            return ((0x10|(arg>>4))<<8)|key
    raise ValueError('Native action cannot be migrated without changing its meaning: '+record.hex())


def public_native_reference(native):
    """Remove every mutable setting/macro/Fn byte from the public code reference.

    Historical snapshots stay untouched. The reference is used only for immutable
    code comparison; settings are always read from the installing user's backup.
    """
    if len(native) != APP_END-APP_START or digest(native) not in NATIVE_REFERENCE_HASHES:
        raise ValueError('Unknown native reference; cannot sanitize')
    public = bytearray(native)
    public[0xA000-APP_START:0xD380-APP_START] = bytes(0xD380-0xA000)
    if digest(public) != NATIVE_PUBLIC_SHA:
        raise ValueError('Sanitized native reference differs from the pinned public image')
    return bytes(public)


PROTECTED_SHA = '9c4d481c14fe26b58f0f3eee81e84f45f118e06d755fd051da8d1cea5d78eb33'
FACTORY_CODE_SHA = '431db5e715957be1b158e122a2ee95034dcb248c091b3e423e50c6a139983595'
PATCHED_CODE_SHA = '92ddc3c33a23a216e360ee137c08309336c8a95250bd5523f44cfbafab9d8a72'


def validate_native(live, stock=None, native=None):
    """Identify supported complete OEM variants using immutable span hashes.

    Settings are intentionally excluded; protected loader/tail and each complete
    code variant remain pinned. No OEM code bytes are needed for identification.
    Optional historical references retain integrity checks for offline callers.
    """
    if len(live) != 65536:
        raise ValueError('Incorrect ROM/reference image')
    if digest(live[:0x27C0] + live[APP_END:]) != PROTECTED_SHA:
        raise ValueError('OEM loader or protected tail differs from this hardware revision')
    factory = digest(live[APP_START:0xA000] + live[0xD200:APP_END]) == FACTORY_CODE_SHA
    patched = digest(live[APP_START:0xA000] + live[0xD380:APP_END]) == PATCHED_CODE_SHA
    if not (factory or patched):
        raise ValueError('Unsupported native application: expected known factory or Fn-layer OEM code')
    if live[0x27C0:0x27C4] != bytes.fromhex('aa5533cc'):
        raise ValueError('OEM boot marker is missing')
    if live[0xA040] != 0:
        raise ValueError('Select native profile 0 before migration')
    if stock is not None:
        if stock != live:
            validate_native(stock)
        if native is not None and digest(native) not in NATIVE_REFERENCE_HASHES and native != stock[APP_START:APP_END]:
            raise ValueError('Incorrect ROM/reference image')
    return 'factory' if factory else 'patched'


def nvm_layout(build_id):
    """Known, explicit layouts only. Physical NVM/journal bounds never move."""
    if build_id in (BUILD_ID, EXTENSION_BUILD_ID):
        return {'layers': LAYER_COUNT, 'encoder_addr': ENCODER_ADDR,
                'macro_addr': MACRO_ADDR, 'macro_size': MACRO_SIZE,
                'macro_busy_addr': MACRO_BUSY_ADDR}
    if build_id == LEGACY_BUILD_ID:
        return {'layers': 2, 'encoder_addr': 0x0240,
                'macro_addr': 0x0300, 'macro_size': 9472,
                'macro_busy_addr': 0x02F0}
    raise ValueError(f'Unknown NVM schema: {build_id:#08x}')


def macro_stream_length(stream):
    """Validate Vial6 bytecode and return the end of its 16th terminator.

    Bytes after that terminator may only be zero padding. Validate operands
    before counting NULs, matching the firmware publication validator.
    """
    terminated = arguments = logical_end = 0
    for offset, value in enumerate(stream):
        if terminated == MACRO_COUNT:
            if value:
                raise ValueError('Nonzero data follows the 16th macro terminator')
        elif arguments == 3:
            if not 1 <= value <= 7:
                raise ValueError('Unsupported Vial macro opcode')
            arguments = 1 if value <= 3 else 2
        elif arguments:
            if value == 0:
                raise ValueError('Zero byte inside a Vial macro operand')
            arguments -= 1
        elif value == 0:
            terminated += 1
            logical_end = offset + 1
        elif value == 1:
            arguments = 3
        elif value >= 128:
            raise ValueError('Vial macro plain text must be ASCII')
    if terminated != MACRO_COUNT or arguments:
        raise ValueError('Incomplete Vial macro stream; all 16 terminators are required')
    return logical_end


def validate_nvm(nvm, build_id=BUILD_ID):
    layout = nvm_layout(build_id)
    if (len(nvm) != NVM_END - NVM_START or nvm[:2] != bytes.fromhex('e6fe')
            or nvm[37:40] != build_id.to_bytes(3, 'little')):
        raise ValueError('NVM magic/schema differs; an explicit migration is required')
    if build_id == EXTENSION_BUILD_ID:
        import ak820_extension_settings as extensions
        extensions.from_nvm(nvm)
    meta = layout['macro_busy_addr']
    if nvm[meta]:
        raise ValueError('An incomplete macro upload is still disabled; finish/retry it before migration')
    length = int.from_bytes(nvm[meta + 1:meta + 3], 'little')
    if not MACRO_COUNT <= length <= layout['macro_size']:
        raise ValueError('Invalid published Vial macro length')
    start = layout['macro_addr']
    logical = macro_stream_length(nvm[start:start + length])
    return {'build_id': build_id, **layout, 'macro_count': MACRO_COUNT,
            'published_macro_length': length, 'logical_macro_length': logical}


def empty_nvm():
    nvm = bytearray(NVM_END - NVM_START)
    nvm[:2] = bytes.fromhex('e6fe')
    nvm[37:40] = BUILD_ID.to_bytes(3, 'little')
    # New layers and encoders inherit lower layers, without another CODE table.
    nvm[KEYMAP_ADDR:ENCODER_ADDR + LAYER_COUNT * 4] = b'\x00\x01' * (LAYER_COUNT * 130)
    nvm[MACRO_BUSY_ADDR + 1:MACRO_BUSY_ADDR + 3] = MACRO_COUNT.to_bytes(2, 'little')
    return nvm


def migrate_vial_nvm(nvm, source_build_id, *, target_build_id=BUILD_ID):
    """Lossless migration of known live Vial settings; never truncate macros."""
    nvm_layout(target_build_id)
    source = validate_nvm(nvm, source_build_id)
    if source_build_id == EXTENSION_BUILD_ID and target_build_id != EXTENSION_BUILD_ID:
        raise ValueError('Schema03 downgrade is forbidden')
    if target_build_id == EXTENSION_BUILD_ID:
        if source_build_id == EXTENSION_BUILD_ID:
            return bytes(nvm), {'mode': 'byte_exact_nvm_copy', 'target_build_id': target_build_id}
        base, report = migrate_vial_nvm(nvm, source_build_id)
        result = bytearray(base)
        # Preserve all schema02 fields, including nonempty Combos.
        result[0x6A8:0x7F0] = bytes(0x7F0-0x6A8)
        result[37:40] = target_build_id.to_bytes(3, 'little')
        import ak820_extension_settings as extensions
        result[0x6A8:0x6C0] = extensions.settings_record()
        validate_nvm(result, target_build_id)
        return bytes(result), {**report, 'mode': 'explicit_schema_migration',
                               'target_build_id': target_build_id, 'source_build_id': source_build_id}
    if target_build_id != BUILD_ID:
        raise ValueError('Unsupported migration target')
    if source_build_id == BUILD_ID:
        return bytes(nvm), {'mode': 'byte_exact_nvm_copy', 'nvm_bytes': len(nvm),
                            'layers': LAYER_COUNT, 'macro_count': MACRO_COUNT,
                            'macro_bytes': MACRO_SIZE, 'source_nvm_sha256': digest(nvm)}
    length = source['logical_macro_length']
    if length > MACRO_SIZE:
        raise ValueError(f'The 16 macros require {length} bytes; Entropy profile has {MACRO_SIZE}. '
                         'Nothing was truncated or written; retain the old backup and reduce macros explicitly.')
    result = empty_nvm()
    result[:KEYMAP_ADDR] = nvm[:KEYMAP_ADDR]
    result[37:40] = BUILD_ID.to_bytes(3, 'little')
    result[KEYMAP_ADDR:KEYMAP_ADDR + 512] = nvm[KEYMAP_ADDR:KEYMAP_ADDR + 512]
    encoders = source['encoder_addr']
    result[ENCODER_ADDR:ENCODER_ADDR + 8] = nvm[encoders:encoders + 8]
    start = source['macro_addr']
    result[MACRO_ADDR:MACRO_ADDR + length] = nvm[start:start + length]
    result[MACRO_BUSY_ADDR + 1:MACRO_BUSY_ADDR + 3] = length.to_bytes(2, 'little')
    validate_nvm(result)
    report = {'mode': 'explicit_schema_migration', 'source_build_id': source_build_id,
              'target_build_id': BUILD_ID, 'source_nvm_sha256': digest(nvm),
              'layers': LAYER_COUNT, 'preserved_layers': source['layers'],
              'new_layers': 'transparent', 'macro_bytes': MACRO_SIZE,
              'previous_macro_bytes': source['macro_size'], 'macro_count': MACRO_COUNT,
              'preserved_macro_stream_bytes': length,
              'discarded_zero_padding_bytes': source['published_macro_length'] - length}
    return bytes(result), report


def migrate(live,data,symbols):
    factory = validate_native(live) == 'factory'
    # EEPROM keycodes are big endian, compiled uint16_t constants little endian.
    keys=struct.unpack('<256H',factory_keymaps(data,symbols))
    encoders=struct.unpack('<4H',code_bytes(data,symbols['_encoder_map'],8))
    nvm=empty_nvm()
    nvm[3]=1
    # Pinned rgb_config_t: 2 enable bits,6 mode bits; HSV, speed, flags.
    nvm[24:32]=bytes((5,0,255,80,96,255,0,0))
    nvm[0x40:0x240]=struct.pack('>256H',*keys)
    # Compiled ENCODER_CCW_CW is [CCW,CW]; EEPROM stores [CW,CCW].
    nvm[ENCODER_ADDR:ENCODER_ADDR+8]=struct.pack('>4H',encoders[1],encoders[0],encoders[3],encoders[2])
    report={'physical_keys':len(PHYSICAL),'layers':LAYER_COUNT,'preserved_native_layers':1 if factory else 2,
            'native_variant':'factory OEM' if factory else 'Fn-layer OEM',
            'factory_fn':'materialized from pinned compiled defaults' if factory else 'editable OEM Fn table',
            'new_layers':'transparent','macro_count':MACRO_COUNT,
            'macro_bytes':MACRO_SIZE,'stock_fn_actions_materialized':[],
            'native_lighting':'New VialRGB defaults; OEM effect numbers are not interchangeable.',
            'native_unused_slots':'Only the83 physical keys and2 encoder directions are migrated.'}
    for layer,base in enumerate((0xA100,0xD200)):
        for slot in PHYSICAL:
            old=b'\xff\xff\xff' if factory and layer else live[base+slot*3:base+slot*3+3]
            default=keys[layer*128+slot]
            if old==b'\xff\xff\xff':
                report['stock_fn_actions_materialized'].append(slot)
            new=action(old,default if layer else None)
            struct.pack_into('>H',nvm,0x40+layer*256+slot*2,new)
        for direction,slot in enumerate((87,111)):  # CW, CCW
            old=b'\xff\xff\xff' if factory and layer else live[base+slot*3:base+slot*3+3]
            default=int.from_bytes(nvm[ENCODER_ADDR+layer*4+direction*2:ENCODER_ADDR+2+layer*4+direction*2],'big')
            new=action(old,default if layer else None)
            struct.pack_into('>H',nvm,ENCODER_ADDR+layer*4+direction*2,new)
    # Reject unsupported actions or expansion beyond the available storage.
    raw=live[0xAD00:0xD200]
    if any(raw):
        from native_macro_import import convert_native_macros
        encoded=convert_native_macros(raw)
        if len(encoded)>MACRO_SIZE:
            raise ValueError(f'Converted macros require {len(encoded)} bytes; Entropy profile has {MACRO_SIZE}. '
                             'Nothing was truncated or written; reduce macros explicitly before installing.')
        nvm[MACRO_ADDR:MACRO_ADDR+len(encoded)]=encoded
        report['macros']='converted from native event streams'
    else:
        report['macros']='all16 empty, as in the native snapshot'
    encoded_length=len(encoded) if any(raw) else 16
    nvm[MACRO_BUSY_ADDR+1:MACRO_BUSY_ADDR+3]=encoded_length.to_bytes(2,'little')
    validate_nvm(nvm)
    return bytes(nvm),report


def ljmp(address):
    return b'\x02'+address.to_bytes(2,'big')


def validate_startup(data, symbols):
    """Bind packaging to the linked, board-specific DPTR-only XINIT routine.

    A symbol name alone also exists in the generic SDCC CRT. Check its actual
    emitted instructions and relocated operands, and reject PSEG allocations:
    the generic PSEG clear still assumes short-MOVX paging on this target.
    """
    names = ('__mcs51_genXINIT', 's_GSINIT3', 'l_GSINIT3', 's_XINIT',
             'l_XINIT', 's_XISEG', 'l_XISEG', 's_XSEG', 'l_XSEG', 'l_PSEG')
    if any(name not in symbols for name in names):
        raise ValueError('Missing linked AK820 startup contract symbols')
    source, destination, length = (symbols[name] for name in ('s_XINIT', 's_XISEG', 'l_XINIT'))
    if (symbols['l_PSEG'] != 0 or length != symbols['l_XISEG'] or
            symbols['s_XSEG'] not in (0x0400, 0x0440) or
            destination != symbols['s_XSEG'] + symbols['l_XSEG'] or
            destination + length > 0x1000):
        raise ValueError('Unsupported startup XRAM/PSEG layout')
    expected = (bytes((0x79, length & 255, 0xe9, 0x44, length >> 8,
                       0x60, 0x25, 0x7a, (length + 255) >> 8,
                       0x7b, source & 255, 0x7c, source >> 8,
                       0x7d, destination & 255, 0x7e, destination >> 8)) +
                bytes.fromhex('8b828c83e493ffa3ab82ac838d828e83eff0a3ad82ae83d9e7dae5'))
    entry = symbols['__mcs51_genXINIT']
    if (entry != symbols['s_GSINIT3'] or symbols['l_GSINIT3'] != len(expected) or
            code_bytes(data, entry, len(expected)) != expected):
        raise ValueError('Unsupported XINIT: expected linked AK820 single-DPTR CRT, not generic MOVX @Ri')


def pack(data,symbols,stock,nvm,trial, *, target_build_id=BUILD_ID):
    if len(nvm)!=NVM_END-NVM_START:
        raise ValueError('Incorrect settings/reference size')
    validate_native(stock)
    validate_nvm(nvm, target_build_id)
    required=['__sdcc_gsinit_startup','_USB_DeviceInterrupt','_ak820_timer_irq','_ak820_led_irq','_encoder_map']
    for name in required:
        if name not in symbols or symbols[name] not in data:
            raise ValueError('Missing reachable symbol '+name)
    if '_keymaps' not in symbols:
        factory_keymaps(data, symbols)
    elif any(name in symbols for name in ('_ak820_default_classes', '_ak820_default_offsets', '_ak820_default_payload')):
        raise ValueError('Ambiguous compiled default keymaps')
    elif symbols['_keymaps'] not in data:
        raise ValueError('Missing reachable symbol _keymaps')
    if code_bytes(data,CODE_START,3)!=ljmp(symbols['__sdcc_gsinit_startup']):
        raise ValueError('Unexpected SDCC CRT entry instruction')
    validate_startup(data, symbols)
    full=bytearray(stock)
    full[APP_START:APP_END]=bytes(APP_END-APP_START)
    # Run before the CRT, with interrupts disabled. This is the exact native
    # page-erase routine; its internal branches are all relative and it has no
    # absolute calls. R6:R7=27C0 selects only the boot validity marker page.
    erase = stock[0xE650:0xE6A7]
    full[ERASE_START:ERASE_START+len(erase)] = erase
    # The AK820 CRT uses explicit DPTR for XINIT. Pin DPTR0 and disable MOVX
    # auto-increment before the CRT or its native erase helper can use DPTR.
    # Preserve unrelated XBUS_AUX bits. Clear the inherited XSFR-only mode as
    # well; no startup correctness claim relies on P2/short-MOVX paging.
    normalize=bytes.fromhex('53a2fa75a15575a1aa53b1fde4f5a1')
    # Do not inherit enabled interrupts/E_DIS from a loader handoff. Every
    # intended source (Timer0, USB, LED) is explicitly enabled by the app.
    disable_interrupts=bytes.fromhex('75a80075e800')
    # The loader may reach entry by a software handoff, not just POR. Its
    # remaining stack frame is never returned to. Match OEM bank0/SP20 before
    # calling the leaf erase helper, which uses registers and IRAM bit03.
    initialize_registers = bytes.fromhex('75d000758120')
    erase_call = bytes.fromhex('7fc07e2712') + ERASE_START.to_bytes(2, 'big')
    prefix = disable_interrupts + initialize_registers + normalize
    entry=(prefix+erase_call+ljmp(MARKER_CHECK_START)
           if trial else prefix+ljmp(CODE_START))
    marker_check=bytes.fromhex('9027c07f40e4937006a3dff9')+ljmp(CODE_START)+bytes.fromhex('80fe')
    if (APP_START+len(entry)>ERASE_START or ERASE_START+len(erase)>MARKER_CHECK_START or
            MARKER_CHECK_START+len(marker_check)>LOW_START):
        raise ValueError('Startup helpers overlap each other or linked low code')
    full[APP_START:APP_START+len(entry)]=entry
    # Trial check: all64 marker bytes must read zero after the native erase.
    # On failure stop here instead of starting an unprotected trial app.
    full[MARKER_CHECK_START:MARKER_CHECK_START+len(marker_check)]=marker_check
    for ordinal in range(13):
        full[0x3000+ordinal*3:0x3003+ordinal*3]=b'\x22\x00\x00'
    for ordinal,name in ((1,'_ak820_timer_irq'),(7,'_USB_DeviceInterrupt'),(10,'_ak820_led_irq')):
        full[0x3000+ordinal*3:0x3003+ordinal*3]=ljmp(symbols[name])
    for address,value in data.items():
        full[address]=value
    full[NVM_START:NVM_END]=nvm
    code_hash=bytes.fromhex(digest(full[APP_START:CODE_END]))
    config_hash=bytes.fromhex(digest(nvm))[:16]
    full[MANIFEST_START:APP_END]=MAGIC+bytes((1,int(trial)))+b'\0\0'+target_build_id.to_bytes(4,'little')+code_hash+config_hash
    if full[:APP_START]!=stock[:APP_START] or full[APP_END:]!=stock[APP_END:]:
        raise AssertionError('Protected ROM changed')
    return bytes(full[APP_START:APP_END])


def verify_payload(payload, *, allow_legacy=False, target_build_id=BUILD_ID):
    if len(payload)!=APP_END-APP_START:
        raise ValueError('Wrong update image length; never use a full-ROM image')
    manifest=payload[MANIFEST_START-APP_START:]
    build_id=int.from_bytes(manifest[12:16],'little')
    nvm_layout(target_build_id)
    allowed=(target_build_id,LEGACY_BUILD_ID) if allow_legacy else (target_build_id,)
    if manifest[:8]!=MAGIC or manifest[8]!=1 or manifest[9] not in (0,1) or build_id not in allowed:
        raise ValueError('Unknown application manifest')
    if bytes.fromhex(digest(payload[:CODE_END-APP_START]))!=manifest[16:48]:
        raise ValueError('Application checksum mismatch')
    if bytes.fromhex(digest(payload[NVM_START-APP_START:NVM_END-APP_START]))[:16]!=manifest[48:64]:
        raise ValueError('Initial configuration checksum mismatch')
    if any(payload[NVM_END-APP_START:MANIFEST_START-APP_START]):
        raise ValueError('Journal must be empty before installation')
    validate_nvm(payload[NVM_START-APP_START:NVM_END-APP_START],build_id)
    return {'trial':bool(manifest[9]),'build_id':build_id,'sha256':digest(payload),'size':len(payload)}


def write_package(ihx,mapfile,stockpath,nativepath,livepath,out):
    stock,native,live=(p.read_bytes() for p in (stockpath,nativepath,livepath))
    validate_native(live,stock,native)
    data,symbols=read_ihex(ihx),read_symbols(mapfile)
    nvm,migration=migrate(live,data,symbols)
    out.mkdir(parents=True,exist_ok=False)
    images={}
    for name,trial in (('ak820-vial-trial.bin',True),('ak820-vial-permanent.bin',False)):
        payload=pack(data,symbols,stock,nvm,trial)
        (out/name).write_bytes(payload)
        images[name]=verify_payload(payload)
    recovery=live[APP_START:APP_END]
    (out/'restore-native.bin').write_bytes(recovery)
    images['restore-native.bin']={'size':len(recovery),'sha256':digest(recovery),'restores':'native application and settings from this exact backup'}
    (out/'before-full-rom.bin').write_bytes(live)
    manifest={'format':'ak820-vial-release-1','hardware':'AJAZZ AK820 wired RGB / VS11K28A /320F:505B',
              'address':APP_START,'length':APP_END-APP_START,'preserved':[[0,APP_START],[APP_END,65536]],
              'backup_sha256':digest(live),'ihx_sha256':digest(ihx.read_bytes()),'map_sha256':digest(mapfile.read_bytes()),
              'images':images,'migration':migration,'hardware_validated':False,
              'trial_recovery':'After the trial entry successfully clears27C0, the next reset enters the OEM loader. No guarantee if execution never reaches that entry.'}
    (out/'images.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return manifest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ihx',type=Path,required=True)
    p.add_argument('--map',type=Path,required=True)
    p.add_argument('--stock-rom',type=Path,required=True)
    p.add_argument('--native-reference',type=Path,required=True)
    p.add_argument('--native-rom',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(write_package(a.ihx,a.map,a.stock_rom,a.native_reference,a.native_rom,a.out),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
