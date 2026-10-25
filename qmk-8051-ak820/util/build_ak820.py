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
import shlex
import subprocess
import sys
from pathlib import Path

from ak820_dce import optimize
from ak820_outline_audit import outline_assembled
import ak820_shortcalls as shortcalls
import ak820_tailshare as tailshare
import ak820_register_saves as register_saves
import ak820_parameter_spills as parameter_spills
from ak820_build_inputs import FORMAT as INPUT_FORMAT, collect_inputs, input_snapshot
from ak820_profiles import DEFAULT_PROFILE, PROFILES, RELEASE_PROFILES, configuration


# Audited C functions only: SDCC emits their register-preserving prologues and
# protects calls to unlisted children. Apply the same ABI list to every TU.
# The AK820 startup/IRQ wrappers select register bank 0 for application C.
AK820_CALLEE_SAVES = (
    'timer_read', 'timer_read32', 'ak820_nvm_ok', 'get_mods', 'get_weak_mods',
    'matrix_get_row', 'readPin', 'eeprom_read_byte', 'eeprom_update_byte',
    'ak820_flash_read', 'mDelaymS',
    'get_repeat_key_count',
)


def word_hook_abi_flag(callee_saves, extra_flags):
    """Certify only the audited bank-zero word-hook ABI, never public APIs."""
    public = {'dynamic_keymap_get_keycode', 'dynamic_keymap_set_keycode',
              'dynamic_keymap_get_encoder', 'dynamic_keymap_set_encoder'}
    names = set(callee_saves)
    tokens = shlex.split(extra_flags)
    for index, token in enumerate(tokens):
        if token in ('--stack-auto', '--xstack', '--parms-in-bank1', '--all-callee-saves') or token.startswith('--sdcccall'):
            raise ValueError('Unsupported AK820 word-hook ABI option: ' + token)
        if token == '--callee-saves':
            if index + 1 == len(tokens):
                raise ValueError('Missing callee-saves names')
            names.update(tokens[index + 1].split(','))
        elif token.startswith('--callee-saves='):
            names.update(token.split('=', 1)[1].split(','))
        if 'AK820_WORD_HOOKS_PRESERVE_RN' in token:
            raise ValueError('Word-hook ABI assertion is owned by the builder')
    if public & {name.lstrip('_') for name in names}:
        raise ValueError('AK820 word APIs must remain caller-clobbered')
    if {'eeprom_read_byte', 'eeprom_update_byte'} <= set(callee_saves):
        return ' -DAK820_WORD_HOOKS_PRESERVE_RN=1'
    return ''


def read_block_abi_flag(enabled, keyboard, version, callee_saves, extra_flags):
    tokens = shlex.split(extra_flags)
    if any('AK820_READ_HOOK_PRESERVES_RN' in t or 'AK820_NVM_READ_BLOCK_ASM' in t for t in tokens):
        raise ValueError('Read kernel assertions and feature switch are owned by the builder')
    if not enabled:
        return ''
    if keyboard != 'ajazz/ak820' or version != '4.6.0':
        raise ValueError('Read kernel requires AK820 and pinned SDCC 4.6.0')
    bad = ('--stack-auto', '--xstack', '--parms-in-bank1', '--all-callee-saves', '--model-small', '--model-medium', '--model-huge')
    if any(t in bad or t.startswith('--sdcccall') for t in tokens):
        raise ValueError('Unsupported read kernel ABI option')
    names = set(callee_saves)
    for i, token in enumerate(tokens):
        if token == '--callee-saves':
            if i+1 == len(tokens): raise ValueError('Missing callee-saves names')
            names.update(tokens[i+1].split(','))
        elif token.startswith('--callee-saves='):
            names.update(token.split('=',1)[1].split(','))
    if 'ak820_eeprom_read_block_xdata' in {n.lstrip('_') for n in names}:
        raise ValueError('Read block API must remain caller-clobbered')
    if 'eeprom_read_byte' not in callee_saves:
        raise ValueError('Read kernel needs the audited preserving scalar hook')
    return ' -DAK820_READ_HOOK_PRESERVES_RN=1'


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
    p.add_argument('--profile', choices=tuple(PROFILES), default=DEFAULT_PROFILE,
                   help='Explicit development feature set; this does not approve an installer')
    p.add_argument('--code-start', type=integer, default=0x3027)
    p.add_argument('--code-end', type=integer, default=0xc700)
    p.add_argument('--low-code-start', type=integer, default=0x28a0)
    p.add_argument('--low-code-end', type=integer, default=0x3000)
    p.add_argument('--xram-start', type=integer, default=None,
                   help='Ordinary XRAM start (AK820: 0x440; other targets: 0x400)')
    p.add_argument('--xram-end', type=integer, default=0x1000)
    p.add_argument('--root', action='append', default=[])
    p.add_argument('--build-id', type=integer, default=None, help='Stable Vial EEPROM schema identifier')
    p.add_argument('--extra-flags', default='--opt-code-size', help='Additional compiler flags; board config owns feature flags')
    p.add_argument('--iram-overlay-diagnostic', type=Path, default=None, help='Opt-in external diagnostic integration directory; never production admission')
    p.add_argument('--iram-overlay-certificate', type=Path)
    p.add_argument('--iram-overlay-certificate-sha256')
    p.add_argument('--short-calls', action=argparse.BooleanOptionalAction, default=None,
                   help='Verified foreground ACALL/AJMP relaxation; enabled by default for curated profiles')
    p.add_argument('--nvm-read-block-asm', action='store_true', help='Diagnostic separate-TU read kernel (default off)')
    p.add_argument('--keymap-words-asm', action='store_true', help='Experimental fixed-layout keymap word kernel (opt-in)')
    p.add_argument('--trim-parameter-spills', action='store_true', help='Experimental private first-argument spill folding (requires explicit source-context certificate)')
    p.add_argument('--parameter-spills-context', type=Path, help='Reviewed source-context certificate for private argument spills')
    p.add_argument('--trim-register-saves', action='store_true', help='Experimental conservative assembled register-save trimming')
    p.add_argument('--outline-max-helpers', type=int, default=200, help='Maximum exact outliner helpers (default: 200)')
    p.add_argument('--tail-share', action='store_true', help='Experimental exact RET tail sharing (opt-in; no added stack frame)')
    p.add_argument('--no-outline', action='store_true', help='Disable AK820 exact instruction outlining for comparison builds')
    p.add_argument('--no-callee-saves', action='store_true', help='Disable the audited AK820 callee-saves list for comparison builds')
    args = p.parse_args()
    if args.xram_start is None:
        args.xram_start = 0x440 if args.keyboard == 'ajazz/ak820' else 0x400
    if args.trim_parameter_spills:
        if args.keyboard != 'ajazz/ak820' or args.sdcc_version != '4.6.0':
            p.error('--trim-parameter-spills requires ajazz/ak820 and pinned SDCC 4.6.0')
        if args.parameter_spills_context is None or not args.parameter_spills_context.is_file():
            p.error('--trim-parameter-spills requires --parameter-spills-context FILE')
        if [args.xram_start,args.xram_end] != [0x440,0x1000]:
            p.error('--trim-parameter-spills requires ordinary XRAM 0x440..0x1000')
    selected = configuration(args.profile)
    if args.keymap_words_asm and (args.keyboard != 'ajazz/ak820' or args.sdcc_version != '4.6.0'):
        p.error('--keymap-words-asm requires ajazz/ak820 and pinned SDCC 4.6.0')
    if args.keymap_words_asm and any(flag in shlex.split(args.extra_flags) for flag in
                                    ('--model-small', '--model-medium', '--model-huge')):
        p.error('--keymap-words-asm requires the large memory model')
    if args.outline_max_helpers < 1:
        p.error('--outline-max-helpers must be positive')
    if args.trim_register_saves and (args.keyboard != 'ajazz/ak820' or args.sdcc_version != '4.6.0'):
        p.error('--trim-register-saves requires ajazz/ak820 and SDCC 4.6.0')
    if args.short_calls is None:
        args.short_calls = args.profile in RELEASE_PROFILES
    if args.build_id is None:
        args.build_id = selected['nvm_schema']
    if args.short_calls and (args.keyboard != 'ajazz/ak820' or args.sdcc_version != '4.6.0'):
        raise ValueError('Short calls require the AK820 target and pinned SDCC 4.6.0')
    if args.tail_share and (args.keyboard != 'ajazz/ak820' or args.sdcc_version != '4.6.0'):
        raise ValueError('Tail sharing requires AK820 and pinned SDCC 4.6.0')
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
    # Do not inherit Make's -e or command-line overrides from a parent build.
    for name in ('MAKEFLAGS', 'MFLAGS', 'GNUMAKEFLAGS', 'MAKEOVERRIDES'):
        env.pop(name, None)
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

    def run(label, argv, timeout=300, allow_page_errors=False):
        log = build/(label+'.log')
        with log.open('w') as f:
            proc = subprocess.run(argv,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
        commands.append({'label':label,'argv':argv,'exit_code':proc.returncode,'log':log.relative_to(root).as_posix(),'log_sha256':sha(log)})
        if proc.returncode and not (allow_page_errors and shortcalls.page_errors_only(log.read_text())):
            raise RuntimeError(label+' failed; see '+str(log))
        return proc.returncode

    target = args.keyboard.replace('/','_')+'_'+args.keymap
    relative_build = str(build.relative_to(root))
    callee_saves = AK820_CALLEE_SAVES if args.keyboard == 'ajazz/ak820' and not args.no_callee_saves else ()
    read_abi = read_block_abi_flag(args.nvm_read_block_asm, args.keyboard, args.sdcc_version, callee_saves, args.extra_flags)
    compile_flags = args.extra_flags + read_abi
    if callee_saves:
        compile_flags += ' --callee-saves ' + ','.join(callee_saves)
    if args.keyboard == 'ajazz/ak820':
        compile_flags += word_hook_abi_flag(callee_saves, args.extra_flags)
    qmk = str(args.qmk_bin.resolve()) if args.qmk_bin else shutil.which('qmk',path=env['PATH'])
    if not qmk:
        raise ValueError('QMK CLI unavailable')
    run('compile',['make','-r','-R','-f','builddefs/build_keyboard.mk','sdcc-objects',
        'KEYBOARD='+args.keyboard,'KEYMAP='+args.keymap,'QMK_BIN='+qmk,'SILENT=false','COLOR=false',
        'SKIP_GIT=yes','SKIP_VERSION=yes','BUILD_DIR='+relative_build,'EXTRAFLAGS='+compile_flags,
        *(name+'='+value for name,value in selected['make_options'].items()),
        'AK820_NVM_READ_BLOCK_ASM='+('yes' if args.nvm_read_block_asm else 'no'),
        'AK820_KEYMAP_WORDS_ASM='+('yes' if args.keymap_words_asm else 'no'), '-j'+str(args.jobs)])
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
    parameter_result = None
    if args.trim_parameter_spills:
        context_copy = build/'parameter-spills-context.json'
        shutil.copyfile(args.parameter_spills_context.resolve(), context_copy)
        parameter_input = build/'parameter-spills-input'
        parameter_output = build/'parameter-spills-output'
        dce_input.rename(parameter_input)
        parameter_result = parameter_spills.prepare(root,obj,parameter_input,parameter_output,
            build/'parameter-spills-metadata',context_copy,build/'parameter-spills.json',Path(sdcc),inputs_before)
        assemble_tree(parameter_output,'assemble-parameter-spills-')
        parameter_spills.verify_assembled(parameter_input,parameter_output,build/'parameter-spills.json',parameter_result)
        shutil.copytree(parameter_output,dce_input)
    register_result = None
    if args.trim_register_saves:
        register_input = build/'register-saves-input'
        dce_input.rename(register_input)
        register_output = build/'register-saves-output'
        register_result = register_saves.prepare(register_input, register_output, build/'register-saves.json')
        assemble_tree(register_output, 'assemble-register-saves-')
        register_saves.verify_assembled(register_input, register_output, build/'register-saves.json', register_result)
        shutil.copytree(register_output, dce_input)
    outlining = None
    if apply_outlining:
        outlining = outline_assembled(dce_input, dce, max_helpers=args.outline_max_helpers, min_saving=1)
        assemble_tree(dce, 'assemble-outlined-')
    tail_result = None
    if args.tail_share:
        tail_input = build/'tailshare-input'
        dce.rename(tail_input)
        tail_result = tailshare.prepare(tail_input, dce, build/'tail-share.json')
        assemble_tree(dce, 'assemble-tailshare-')
        tailshare.verify_assembled(tail_input, dce, build/'tail-share.json', tail_result)
    ihx = build/(target+'.ihx')
    extra_link = []
    windows = [(args.code_start,args.code_end)]
    if args.keyboard == 'ajazz/ak820':
        extra_link.append('-Wl-bAK820LOW='+hex(args.low_code_start))
        windows.append((args.low_code_start,args.low_code_end))
    def link_command(tree, image, code_end):
        return [sdcc,'-mmcs51','--model-large','--iram-size','0x100',
            '--xram-loc',hex(args.xram_start),'--xram-size',hex(args.xram_end-args.xram_start),
            '--code-loc',hex(args.code_start),'--code-size',hex(code_end),
            '--opt-code-size',*(['-Wl-j'] if args.short_calls else []),*extra_link,
            *sorted(str(path) for path in tree.rglob('*.rel')),
            '-o',str(image)]

    short_plan = None
    short_input = build/'shortcalls-input'
    if args.short_calls:
        # Final consumers keep their established dce path. Only this immutable
        # post-outline preimage is used to construct every diagnostic iteration.
        dce.rename(short_input)
        def diagnostic_link(tree, image, label, allow_page_errors):
            assemble_tree(tree, label+'-assemble-')
            return run(label, link_command(tree,image,0x10000), allow_page_errors=allow_page_errors)
        short_plan = shortcalls.prepare(short_input, build/'shortcalls', diagnostic_link)
        shortcalls.write_tree(short_input, dce, short_plan['candidates'])
        assemble_tree(dce, 'assemble-shortcalls-final-')
    # Diagnostic images are never accepted firmware. Repeat the link with the
    # original strict memory limits and independently validate its final bytes.
    run('link',link_command(dce,ihx,args.code_end))
    short_result = None
    overlay_cert = None
    overlay_result = None
    if args.iram_overlay_diagnostic is not None:
        if not args.iram_overlay_certificate or not args.iram_overlay_certificate_sha256:
            raise ValueError('Overlay diagnostic requires exact certificate and hash')
        sys.path.insert(0, str(args.iram_overlay_diagnostic.resolve()))
        import integration as iram_overlay
        iram_overlay.check_tools(Path(sdcc), Path(assembler))
        if short_plan is not None:
            short_result = shortcalls.finish(short_input,dce,build/'shortcalls/baseline.ihx',
                ihx,short_plan,build/'short-calls.json')
        overlay_cert = iram_overlay.prepare(build, args.iram_overlay_certificate,
            args.iram_overlay_certificate_sha256, args.iram_overlay_diagnostic.parent/'ak820-iram-overlay-integration')
        assemble_tree(dce, 'assemble-overlay-diagnostic-')
        run('link-overlay-diagnostic', link_command(dce, ihx, args.code_end))
        overlay_stack = build/'overlay-stack.json'
        run('overlay-exact-stack', [sys.executable, str(root/'tests/ak820_stack/analyze.py'),
            '--build-dir', str(build), '--output', str(overlay_stack)])
        overlay_result = iram_overlay.finish(build, root/'tests/ak820_stack/analyze.py', overlay_cert, overlay_stack)
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
    if overlay_result is None and short_plan is not None:
        short_result = shortcalls.finish(short_input,dce,build/'shortcalls/baseline.ihx',
            ihx,short_plan,build/'short-calls.json')
    if parameter_result is not None:
        spill_stack = build/'parameter-spills-stack.json'
        run('parameter-spills-postlink-stack',[sys.executable,str(root/'tests/ak820_stack/analyze.py'),
            '--build-dir',str(build),'--output',str(spill_stack)])
        parameter_spills.postlink_audit(root,build,build/'parameter-spills-context.json',
            build/'parameter-spills.json',parameter_result,spill_stack)
    # This output is intentionally not padded to a device update payload.
    binary = ihx.with_suffix('.bin')
    binary.write_bytes(bytes(data.get(a,0xff) for a in range(min(data),max(data)+1)))
    artifacts = [ihx,binary,ihx.with_suffix('.map'),ihx.with_suffix('.mem'),dce/'reachability.json',
                 obj/'obj.txt',obj/'cflags.txt',obj/'ldflags.txt',obj/'src/version.h',obj/'src/info_config.h']
    if outlining is not None:
        artifacts.append(dce/'outlining.json')
    # Absolute XDATA declarations are not represented by ordinary linker
    # area lengths. Preserve compiler ASM for the profile resource checker.
    if short_result is not None:
        artifacts.append(build/'short-calls.json')
        artifacts.append(ihx.with_suffix('.noi'))
        artifacts.extend(sorted(dce.rglob('*.asm')))
        artifacts.extend(sorted(dce.rglob('*.rel')))
    if tail_result is not None:
        artifacts.append(build/'tail-share.json')
        artifacts.extend(sorted((build/'tailshare-input').rglob('*.asm')))
        artifacts.extend(sorted((build/'tailshare-input').rglob('*.lst')))
        artifacts.extend(sorted(dce.rglob('*.asm')))
    if register_result is not None:
        artifacts.append(build/'register-saves.json')
        for pattern in ('*.asm','*.lst','*.rel'):
            artifacts.extend(sorted((build/'register-saves-input').rglob(pattern)))
            artifacts.extend(sorted((build/'register-saves-output').rglob(pattern)))
    if parameter_result is not None:
        artifacts.extend([build/'parameter-spills.json',build/'parameter-spills-context.json',build/'parameter-spills-stack.json'])
        artifacts.extend(sorted(path for path in (build/'parameter-spills-metadata').rglob('*') if path.is_file()))
        for folder in ('parameter-spills-input','parameter-spills-output'):
            for pattern in ('*.asm','*.lst','*.rel','*.sym'):
                artifacts.extend(sorted((build/folder).rglob(pattern)))
    if overlay_result is not None:
        artifacts.extend([build/'overlay-link-diagnostic.json', build/'overlay-stack.json'])
        artifacts.extend(sorted(path for path in (build/'overlay-proof-src').rglob('*') if path.is_file()))
        artifacts.extend(sorted(dce.rglob('*.asm')))
    artifacts.extend(asm_paths)
    if args.keyboard == 'ajazz/ak820':
        allocation_paths = [build/'allocation'/'ak820_flash.asm', build/'allocation'/'ak820_flash.adb']
        if any(not path.is_file() for path in allocation_paths):
            raise ValueError('Missing compiler allocation metadata')
        artifacts.extend(allocation_paths)
    artifacts.extend(sorted(dce.rglob('*.rst')))
    source_records, dependency_evidence = collect_inputs(root, toolchain, build, expected, inputs_before)
    artifacts.extend(dependency_evidence)
    if parameter_result is not None:
        existing_source_paths={(r['origin'],r['path']) for r in source_records}
        for name in ('util/ak820_parameter_spills.py','util/ak820_register_saves.py','tests/ak820_stack/analyze.py'):
            path=(root/name).resolve()
            if inputs_before.get(path)!=sha(path):raise ValueError('Spill proof implementation changed during build: '+name)
            if ('source',name) not in existing_source_paths:
                source_records.append({'path':name,'origin':'source','sha256':sha(path)})
    # Optional passes can retain the same final ASM artifact. Record each
    # resolved file once so strict consumers reject real aliases, not our list.
    artifacts = list(dict.fromkeys(path.resolve() for path in artifacts))
    report = {
        'configuration': selected,
        'keyboard':args.keyboard,'keymap':args.keymap,'compiler_version':version.strip(),
        'build_id':args.build_id,'skip_version':True,
        'experimental_iram_overlay':overlay_result,
        'compiler_sha256':sha(Path(sdcc)), 'assembler_sha256':sha(Path(assembler)),
        'builder_sha256':sha(Path(__file__)), 'dce_sha256':sha(root/'util/ak820_dce.py'),
        'outliner_sha256':sha(root/'util/ak820_outline_audit.py'),
        'outline_max_helpers':args.outline_max_helpers,
        'nvm_read_block_asm':args.nvm_read_block_asm,
        'keymap_words_asm':args.keymap_words_asm,
        'parameter_spills_sha256':sha(root/'util/ak820_parameter_spills.py'),
        'parameter_spills': None if parameter_result is None else {
            'report':(build/'parameter-spills.json').relative_to(root).as_posix(),
            'report_sha256':sha(build/'parameter-spills.json'),
            'context_sha256':sha(build/'parameter-spills-context.json'),
            'selected':len(parameter_result['selected']),
            'object_saved_bytes':parameter_result['object_saved_bytes'],
            'postlink_qualified':parameter_result['postlink_qualified'],
            'linked_saved_bytes':None, 'extra_stack_bytes':0,
        },
        'register_saves_sha256':sha(root/'util/ak820_register_saves.py'),
        'register_saves': None if register_result is None else {
            'report':(build/'register-saves.json').relative_to(root).as_posix(),
            'report_sha256':sha(build/'register-saves.json'),
            'object_saved_bytes':register_result['object_saved_bytes'],
            'linked_saved_bytes':None, 'extra_stack_bytes':0,
        },
        'tailshare_sha256':sha(root/'util/ak820_tailshare.py'),
        'tail_share': None if tail_result is None else {
            'report':(build/'tail-share.json').relative_to(root).as_posix(),
            'report_sha256':sha(build/'tail-share.json'),
            'estimated_object_saved_bytes':tail_result['estimated_object_saved_bytes'],
            'object_saved_bytes':tail_result['object_saved_bytes'],
            'linked_saved_bytes':None, 'extra_stack_bytes':0,
        },
        'shortcalls_sha256':sha(root/'util/ak820_shortcalls.py'),
        'short_calls': None if short_result is None else {
            'algorithm':short_result['algorithm'], 'report':(build/'short-calls.json').relative_to(root).as_posix(),
            'report_sha256':sha(build/'short-calls.json'), 'selected':len(short_plan['candidates']),
            'saved_bytes':short_result['saved_bytes'],
        },
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
