#!/usr/bin/env python3
"""Build the pinned AK820 QMK8051 port using SDCC 4.6 (or the 4.4 control).

No USB device is opened and no flash command is run. The result is a linked
application Intel HEX image plus exact build/reachability provenance. The image
packer must add the loader-facing entry/callbacks and verify all flash boundaries.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from ak820_dce import optimize
from ak820_outline_audit import outline_assembled
from ak820_build_inputs import FORMAT as INPUT_FORMAT, collect_inputs, input_snapshot


# Audited C functions only: SDCC emits their register-preserving prologues and
# protects calls to unlisted children. Apply the same ABI list to every TU.
# The AK820 startup/IRQ wrappers select register bank 0 for application C.
AK820_CALLEE_SAVES = (
    'timer_read', 'timer_read32', 'ak820_nvm_ok', 'get_mods', 'get_weak_mods',
    'matrix_get_row', 'readPin', 'eeprom_read_byte', 'eeprom_update_byte',
    'ak820_flash_read', 'mDelaymS',
)


def integer(s):
    return int(s, 0)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def validate_sdcc_version(output, expected):
    if not re.search(r'\b' + re.escape(expected) + r'\b', output):
        raise ValueError('Selected SDCC version is ' + expected + ', but the compiler reports a different version')


def ihex_data(path):
    result = {}
    base = 0
    eof = False
    for line in path.read_text().splitlines():
        if not line.startswith(':'):
            raise ValueError('Invalid Intel HEX record')
        b = bytes.fromhex(line[1:])
        if len(b) != b[0]+5 or sum(b)&255:
            raise ValueError('Invalid Intel HEX length/checksum')
        kind = b[3]
        addr = (b[1]<<8)|b[2]
        payload = b[4:-1]
        if kind == 0:
            if eof:
                raise ValueError('Data after EOF')
            for i,val in enumerate(payload):
                key = base+addr+i
                if key in result and result[key] != val:
                    raise ValueError('Conflicting Intel HEX bytes')
                result[key] = val
        elif kind == 1:
            eof = True
        elif kind == 2:
            base = int.from_bytes(payload,'big')<<4
        elif kind == 4:
            base = int.from_bytes(payload,'big')<<16
        else:
            raise ValueError('Unexpected Intel HEX record type: '+str(kind))
    if not eof or not result:
        raise ValueError('Incomplete Intel HEX image')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--keyboard', default='ajazz/ak820')
    p.add_argument('--keymap', default='vial')
    p.add_argument('--jobs', type=int, default=4)
    p.add_argument('--toolchain', type=Path, help='SDCC installation directory (containing bin/sdcc)')
    p.add_argument('--sdcc-version', choices=('4.4.0', '4.6.0'), default='4.6.0',
                   help='Required compiler version (default: %(default)s; 4.4.0 remains available as a control)')
    p.add_argument('--qmk-bin', type=Path, help='QMK executable from its virtual environment')
    p.add_argument('--build-dir', type=Path, default=Path('.build/ak820'))
    p.add_argument('--code-start', type=integer, default=0x3027)
    p.add_argument('--code-end', type=integer, default=0xc700)
    p.add_argument('--low-code-start', type=integer, default=0x28a0)
    p.add_argument('--low-code-end', type=integer, default=0x3000)
    p.add_argument('--xram-start', type=integer, default=0x0400)
    p.add_argument('--xram-end', type=integer, default=0x1000)
    p.add_argument('--root', action='append', default=[])
    p.add_argument('--build-id', type=integer, default=0x082002, help='Stable Vial EEPROM schema identifier')
    p.add_argument('--extra-flags', default='--opt-code-size', help='Additional compiler flags; board config owns feature flags')
    p.add_argument('--no-outline', action='store_true', help='Disable AK820 exact instruction outlining for comparison builds')
    p.add_argument('--no-callee-saves', action='store_true', help='Disable the audited AK820 callee-saves list for comparison builds')
    args = p.parse_args()
    if args.keyboard == 'ajazz/ak820':
        # These calls originate in the preserved OEM loader and are inserted
        # by the image packer, so application ASM cannot express their edges.
        args.root = sorted(set(args.root) | {
            '_USB_DeviceInterrupt', '_ak820_timer_irq', '_ak820_led_irq',
            '__mcs51_genXINIT',  # GSINIT3 fall-through, referenced by SDCC CRT
        })
    root = Path(__file__).resolve().parents[1]
    build = args.build_dir if args.build_dir.is_absolute() else root/args.build_dir
    if not re.fullmatch(r'[A-Za-z0-9_/]+', args.keyboard) or not re.fullmatch(r'[A-Za-z0-9_]+', args.keymap):
        raise ValueError('Invalid target name')
    if build.exists():
        raise ValueError('Build directory already exists; select a fresh --build-dir')
    if not build.resolve().is_relative_to(root):
        raise ValueError('Build directory must be beneath source root')
    build.mkdir(parents=True)
    env = os.environ.copy()
    extra_paths = []
    if args.toolchain:
        extra_paths.append(str(args.toolchain.resolve()/'bin'))
    if args.qmk_bin:
        extra_paths.append(str(args.qmk_bin.resolve().parent))
        env['QMK_BIN'] = str(args.qmk_bin.resolve())
    env['PATH'] = os.pathsep.join(extra_paths+[env.get('PATH','')])
    env['QMK_HOME'] = str(root)
    env['AK820_BUILD_ID'] = hex(args.build_id)
    sdcc = shutil.which('sdcc',path=env['PATH'])
    assembler = shutil.which('sdas8051',path=env['PATH'])
    if not sdcc or not assembler:
        raise ValueError('SDCC/assembler unavailable')
    version = subprocess.check_output([sdcc,'--version'],env=env,text=True)
    validate_sdcc_version(version, args.sdcc_version)
    toolchain = Path(sdcc).resolve().parents[1]
    inputs_before = input_snapshot(root, toolchain)
    commands = []

    def run(label, argv, timeout=300):
        log = build/(label+'.log')
        with log.open('w') as f:
            proc = subprocess.run(argv,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
        commands.append({'label':label,'argv':argv,'exit_code':proc.returncode,'log':log.relative_to(root).as_posix(),'log_sha256':sha(log)})
        if proc.returncode:
            raise RuntimeError(label+' failed; see '+str(log))

    target = args.keyboard.replace('/','_')+'_'+args.keymap
    relative_build = str(build.relative_to(root))
    callee_saves = AK820_CALLEE_SAVES if args.keyboard == 'ajazz/ak820' and not args.no_callee_saves else ()
    compile_flags = args.extra_flags
    if callee_saves:
        compile_flags += ' --callee-saves ' + ','.join(callee_saves)
    qmk = str(args.qmk_bin.resolve()) if args.qmk_bin else shutil.which('qmk',path=env['PATH'])
    if not qmk:
        raise ValueError('QMK CLI unavailable')
    run('compile',['make','-r','-R','-f','builddefs/build_keyboard.mk','sdcc-objects',
        'KEYBOARD='+args.keyboard,'KEYMAP='+args.keymap,'QMK_BIN='+qmk,'SILENT=false','COLOR=false',
        'SKIP_GIT=yes','SKIP_VERSION=yes','BUILD_DIR='+relative_build,'EXTRAFLAGS='+compile_flags,'-j'+str(args.jobs)])
    obj = build/('obj_'+target)
    expected = (obj/'obj.txt').read_text().split()
    if not expected or any(not name.endswith('.rel') or not (root/name).is_file() for name in expected):
        raise ValueError('Not every expected object was produced')
    asm_paths = sorted(obj.rglob('*.asm'))
    expected_stems = {str((root/name).resolve().with_suffix('')) for name in expected}
    actual_stems = {str(path.resolve().with_suffix('')) for path in asm_paths}
    if expected_stems != actual_stems:
        raise ValueError('ASM/object manifest mismatch')
    dce = build/'dce'
    apply_outlining = args.keyboard == 'ajazz/ak820' and not args.no_outline
    dce_input = build/'dce-input' if apply_outlining else dce
    optimize(obj.resolve(),dce_input.resolve(),args.root)

    def assemble_tree(tree, prefix):
        for i,asm in enumerate(sorted(tree.rglob('*.asm'))):
            run(prefix+str(i),[assembler,'-plosgffw',str(asm.with_suffix('.rel')),str(asm)],timeout=60)

    # The first assembly supplies exact instruction lengths/relocations. No
    # unoptimized image is linked, so it need not fit the final CODE window.
    assemble_tree(dce_input, 'assemble-input-' if apply_outlining else 'assemble-')
    outlining = None
    if apply_outlining:
        outlining = outline_assembled(dce_input, dce, max_helpers=200, min_saving=1)
        assemble_tree(dce, 'assemble-outlined-')
    objects = sorted(str(path) for path in dce.rglob('*.rel'))
    ihx = build/(target+'.ihx')
    extra_link = []
    windows = [(args.code_start,args.code_end)]
    if args.keyboard == 'ajazz/ak820':
        extra_link.append('-Wl-bAK820LOW='+hex(args.low_code_start))
        windows.append((args.low_code_start,args.low_code_end))
    run('link',[sdcc,'-mmcs51','--model-large','--iram-size','0x100',
        '--xram-loc',hex(args.xram_start),'--xram-size',hex(args.xram_end-args.xram_start),
        '--code-loc',hex(args.code_start),'--code-size',hex(args.code_end),
        '--opt-code-size',*extra_link,*objects,'-o',str(ihx)])
    data = ihex_data(ihx)
    invalid = [a for a in data if not any(lo<=a<hi for lo,hi in windows)]
    if invalid:
        raise ValueError('Linked code outside permitted interval: '+hex(min(invalid))+'..'+hex(max(invalid)))
    memory = ihx.with_suffix('.mem').read_text()
    ranges = re.findall(r'EXTERNAL RAM\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)',memory)
    if len(ranges)!=1 or not args.xram_start<=int(ranges[0][0],16)<=int(ranges[0][1],16)<args.xram_end:
        raise ValueError('XRAM allocation outside permitted interval')
    if 'ERROR' in memory or 'No room' in memory:
        raise ValueError('Memory allocation failure')
    # This output is intentionally not padded to a device update payload.
    binary = ihx.with_suffix('.bin')
    binary.write_bytes(bytes(data.get(a,0xff) for a in range(min(data),max(data)+1)))
    artifacts = [ihx,binary,ihx.with_suffix('.map'),ihx.with_suffix('.mem'),dce/'reachability.json',
                 obj/'obj.txt',obj/'cflags.txt',obj/'ldflags.txt',obj/'src/version.h',obj/'src/info_config.h']
    if outlining is not None:
        artifacts.append(dce/'outlining.json')
    source_records, dependency_evidence = collect_inputs(root, toolchain, build, expected, inputs_before)
    artifacts.extend(dependency_evidence)
    report = {
        'keyboard':args.keyboard,'keymap':args.keymap,'compiler_version':version.strip(),
        'build_id':args.build_id,'skip_version':True,
        'compiler_sha256':sha(Path(sdcc)), 'assembler_sha256':sha(Path(assembler)),
        'builder_sha256':sha(Path(__file__)), 'dce_sha256':sha(root/'util/ak820_dce.py'),
        'outliner_sha256':sha(root/'util/ak820_outline_audit.py'),
        'audited_callee_saves':list(callee_saves),
        'compiler_extra_flags':compile_flags,
        'outlining': None if outlining is None else {
            'algorithm':outlining['algorithm'], 'report':(dce/'outlining.json').relative_to(root).as_posix(),
            'helpers':len(outlining['selected_exact']),
            'call_sites':sum(item['occurrences'] for item in outlining['selected_exact']),
            'nominal_saved_bytes':outlining['selected_nominal_net_bytes'],
            'extra_stack_bytes':outlining['extra_stack_bytes'],
        },
        'code_min':min(data),'code_max_inclusive':max(data),'code_bytes':len(data),
        'code_window':[args.code_start,args.code_end], 'code_windows':windows,
        'code_main_bytes':sum(args.code_start<=a<args.code_end for a in data),
        'code_low_bytes':sum(args.low_code_start<=a<args.low_code_end for a in data),
        'binary_load_address':min(data),'xram_window':[args.xram_start,args.xram_end],
        'external_roots':args.root,'expected_objects':expected,'commands':commands,
        'source_manifest_format': INPUT_FORMAT, 'sources': source_records,
        'artifacts':[{'path':f.relative_to(root).as_posix(),'size':f.stat().st_size,'sha256':sha(f)} for f in artifacts],
        'hardware_validated':False,'packed_device_update':False,
    }
    (build/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'image':str(ihx),'code_bytes':len(data),'highest_address':hex(max(data)),'hardware_validated':False}))


if __name__ == '__main__':
    main()
