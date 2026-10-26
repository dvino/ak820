#!/usr/bin/env python3
"""Select, build and inspect AK820 development profiles without opening USB.

Only named feature combinations are accepted. Every build is linked inside the
real memory windows and tested against its own IHX/MAP. The foreground, startup
and interrupt bounds must fit its stack. Release approval remains separate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
QMK = ROOT / 'qmk-8051-ak820'
sys.path.insert(0, str(QMK / 'util'))
import ak820_profiles as profiles
from build_ak820 import AK820_CALLEE_SAVES
import ak820_shortcalls as shortcalls
from ak820_build_inputs import validate_inputs
from ak820_diagnose import diagnostic_build
from pack_ak820 import read_symbols, validate_startup
from ak820_ci_authorization import validate_qualification_contract
from build_release_bundle import SDCC46_PINS
from test_keyboard import unittest_counts
from ak820_runtime_safety import combine as combine_runtime_safety

FORMAT = 'ak820-configured-build-1'
WINDOWS = ((0x28a0, 0x3000), (0x3027, 0xc700))
SYMBOLS = {'grave-escape': '_process_grave_esc', 'tap-dance': '_ak820_tap_dance_process', 'key-overrides': '_ak820_key_override_process', 'qmk-settings': '_ak820_settings_set', 'os-indicators': '_ak820_os_indicator_value', 'leader': '_ak820_leader_process', 'nkro-control': '_process_ak820_nkro', 'one-shot': '_ak820_oneshot_process',
           'mouse-keys': '_mousekey_task', 'auto-shift': '_ak820_autoshift_process',
           'dynamic-macros': '_ak820_dynamic_macro_process'}
STATIC_BITS = {'gui-lock': '_gui_disabled', 'ctrl-gui-swap': '_ctrl_gui_swapped', 'mac-pc': '_ak820_mac_mode'}
RELEASE_BLOCKERS = (
    'Run check-runtime to establish the exact-image foreground/startup/IRQ stack bound.',
    'No approved installer/settings transition for this feature identity.',
    'No independent release approval for this image and source.',
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON field: ' + key)
            result[key] = value
        return result
    value = json.loads(Path(path).read_text(), object_pairs_hook=pairs,
                       parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Invalid JSON number')))
    require(isinstance(value, dict), 'Expected a JSON object')
    return value


def validate_tools(toolchain):
    toolchain = Path(toolchain).resolve()
    for name, expected in {**SDCC46_PINS,
                         's51': '61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd'}.items():
        path = toolchain / 'bin' / name
        require(path.is_file() and sha(path) == expected, 'Wrong pinned tool: ' + name)
    return toolchain


def source_identity():
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()
    return {'commit': git('rev-parse', 'HEAD'),
            'dirty': bool(git('status', '--porcelain', '--untracked-files=normal'))}


def artifact(report, build, suffix):
    path = build / ('ajazz_ak820_vial.' + suffix)
    records = [row for row in report.get('artifacts', [])
               if row.get('path', '').replace('\\', '/').endswith('/' + path.name)]
    require(len(records) == 1 and path.is_file(), 'Missing or ambiguous artifact: ' + suffix)
    require(records[0].get('sha256') == sha(path) and records[0].get('size') == path.stat().st_size,
            'Artifact changed: ' + suffix)
    return path


def linked_symbols(mapfile):
    symbols = read_symbols(mapfile)
    absolute = re.findall(r'^\s+([0-9A-Fa-f]{8})\s+_ak820_led_dma\s+ak820_board\s*$',
                          Path(mapfile).read_text(), re.M)
    require(len(absolute) == 1, 'Missing or ambiguous absolute DMA symbol')
    symbols['_ak820_led_dma'] = int(absolute[0], 16)
    stage = re.findall(r'^\s+([0-9A-Fa-f]{8})\s+_ak820_flash_stage\s+ak820_flash\s*$',
                       Path(mapfile).read_text(), re.M)
    require(len(stage) <= 1, 'Ambiguous absolute IAP stage symbol')
    if stage:
        symbols['_ak820_flash_stage'] = int(stage[0], 16)
    return symbols


def check_absolute_xdata(report, build, *, historical=False):
    declarations = []
    for relative in report['expected_objects']:
        path = (QMK / relative).with_suffix('.asm').resolve()
        require(path.is_relative_to(build) and path.is_file(), 'Compiler ASM escapes build directory')
        records = [row for row in report['artifacts'] if row.get('path') == path.relative_to(QMK).as_posix()]
        require(len(records) == 1 and records[0].get('sha256') == sha(path) and
                records[0].get('size') == path.stat().st_size, 'Unbound compiler ASM')
        xdata = absolute = False
        for raw in path.read_text().splitlines():
            line = raw.split(';', 1)[0].strip()
            if line.startswith('.area'):
                xdata, absolute = 'XDATA' in line, 'ABS' in line
            elif xdata and line:
                if re.fullmatch(r'[A-Za-z_$][\w$]*\s*==\s*(?:0x[0-9A-Fa-f]+|\d+|\.)', line):
                    continue  # SDCC debug address equate; not a storage declaration.
                match = re.fullmatch(r'([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(0x[0-9A-Fa-f]+|\d+)', line)
                if match:
                    declarations.append((path.name, match[1], int(match[2], 0)))
                elif absolute:
                    raise ValueError('Unqualified absolute XDATA declaration: ' + line)
    expected = [('ak820_board.asm', '_ak820_led_dma', 0x200)]
    if not historical:
        expected.append(('ak820_flash.asm', '_ak820_flash_stage', 0x400))
        stage_asm = [(QMK / relative).with_suffix('.asm') for relative in report['expected_objects']
                     if Path(relative).stem == 'ak820_flash']
        require(len(stage_asm) == 1, 'Missing or ambiguous IAP stage allocation')
        metadata_asm = (build / 'allocation' / 'ak820_flash.asm').resolve()
        metadata = metadata_asm.with_suffix('.adb')
        require(metadata.is_relative_to(build) and metadata.is_file(), 'Missing IAP allocation metadata')
        for path in (metadata_asm, metadata):
            require(path.is_file(), 'Missing IAP allocation metadata')
            records = [row for row in report['artifacts']
                       if row.get('path') == path.relative_to(QMK).as_posix()]
            require(len(records) == 1 and records[0].get('sha256') == sha(path) and
                    records[0].get('size') == path.stat().st_size, 'Unbound IAP allocation metadata')
        require(re.findall(r'^_ak820_flash_stage\s*=\s*(0x[0-9A-Fa-f]+|\d+)\s*$',
                           metadata_asm.read_text(), re.M) == ['0x0400'],
                'IAP allocation metadata address disagrees')
        allocations = [line for line in metadata.read_text().splitlines()
                       if line.startswith('S:') and '$ak820_flash_stage$' in line]
        require(allocations == ['S:G$ak820_flash_stage$0_0$0({64}DA64d,SC:U),F,0,0'],
                'IAP stage allocation extent is not exactly 64 bytes')
    require(sorted(declarations) == sorted(expected),
            'Unqualified absolute XDATA object or hardware mapping')
    result = [{'symbol': '_ak820_led_dma', 'start': 0x200, 'reserved_end_exclusive': 0x400}]
    if not historical:
        result.append({'symbol': '_ak820_flash_stage', 'start': 0x400,
                       'reserved_end_exclusive': 0x440, 'bytes': 64})
    return result


def retained_static_symbols(report, build, code):
    """Resolve private functions and state without changing the firmware's ABI.

    Static functions need not be exported solely for a host checker. Bind the
    relocated listings and verify their instruction bytes against final IHX.
    """
    found = {}
    paths = sorted((build / 'dce').rglob('*.rst'))
    expected = [row.get('path') for row in report['artifacts']
                if row.get('path', '').endswith('.rst')]
    actual = [path.relative_to(QMK).as_posix() for path in paths]
    require(bool(expected) and len(expected) == len(set(expected)) and
            set(expected) == set(actual), 'Missing or unexpected relocated listing')
    for path in paths:
        name = path.relative_to(QMK).as_posix()
        records = [row for row in report['artifacts'] if row.get('path') == name]
        require(len(records) == 1 and records[0].get('sha256') == sha(path) and
                records[0].get('size') == path.stat().st_size, 'Unbound relocated listing')
        lines = path.read_text().splitlines()
        area = None
        for index, line in enumerate(lines):
            declaration = re.search(r'(?:^|\s)\.area\s+(\w+)\s*(\([^)]*\))?', line)
            if declaration:
                area = (declaration[1], declaration[2])
            label = re.match(r'^\s*([0-9A-F]{6})\s+\d+\s+(_[\w$]+):', line)
            if label and label[2] in (*SYMBOLS.values(), *STATIC_BITS.values()):
                require(label[2] not in found, 'Ambiguous feature symbol')
                if label[2] in STATIC_BITS.values():
                    allocation = re.match(r'^\s*([0-9A-F]{6})\s+\d+\s+\.ds\s+1\s*$',
                                          lines[index + 1] if index + 1 < len(lines) else '')
                    require(area == ('BSEG', '(BIT)') and allocation and
                            allocation[1] == label[1] and int(label[1], 16) < 128,
                            'Invalid feature bit allocation')
                found[label[2]] = int(label[1], 16)
            instruction = re.match(r'^\s*([0-9A-F]{6})\s+((?:[0-9A-F]{2}\s+)+)\[\s*\d+\]', line)
            if instruction:
                address, raw = int(instruction[1], 16), bytes.fromhex(instruction[2])
                require(all(code.get(address + i) == byte for i, byte in enumerate(raw)),
                        'Relocated instruction differs from IHX')
    return found


def check_feature_symbols(symbols, selected, code):
    for feature, symbol in SYMBOLS.items():
        require((symbol in symbols and symbols[symbol] in code) ==
                (feature in selected['optional_features']), 'Compiled feature differs from profile: ' + feature)
    for feature, symbol in STATIC_BITS.items():
        require((symbol in symbols) == (feature in selected['optional_features']),
                'Compiled feature state differs from profile: ' + feature)


def check_feature_defines(report, build, selected):
    """Bind inline options as well as standalone handlers to compiler inputs."""
    flags = build / 'obj_ajazz_ak820_vial/cflags.txt'
    relative = flags.relative_to(QMK).as_posix()
    records = [row for row in report.get('artifacts', [])
               if row.get('path', '').replace('\\', '/') == relative]
    require(len(records) == 1 and flags.is_file() and
            records[0].get('sha256') == sha(flags) and
            records[0].get('size') == flags.stat().st_size, 'Unbound compiler feature flags')
    tokens = flags.read_text().split()
    for feature, define in profiles.SWITCHES.items():
        actual = [token for token in tokens if re.match(r'^-[DU]' + re.escape(define) + r'(?:=|$)', token)]
        expected = ['-D' + define] if feature in selected['optional_features'] else []
        require(actual == expected, 'Compiler feature flag differs from profile: ' + feature)

    for feature, define, enabled in (
            ('nkro', 'NKRO_ENABLE', True), ('grave-escape', 'GRAVE_ESC_ENABLE', True),
            ('vialrgb-direct', 'VIALRGB_NO_DIRECT', False)):
        actual = [token for token in tokens if re.match(r'^-[DU]' + define + r'(?:=|$)', token)]
        expected = ['-D' + define] if (feature in selected['optional_features']) == enabled else []
        require(actual == expected, 'Compiler core feature flag differs from profile: ' + feature)
    require(not any('AK820_DIAG_' in token or 'AK820_OMIT_' in token for token in tokens),
            'Diagnostic feature switches cannot qualify')


def memory_report(code, symbols, memory, *, historical=False):
    """Validate allocated memory; deliberately do not infer a stack bound."""
    require(code and all(any(lo <= address < hi for lo, hi in WINDOWS) for address in code),
            'Linked CODE touches a protected address')
    windows = []
    for name, (lo, hi) in zip(('low', 'main'), WINDOWS):
        used = sorted(address for address in code if lo <= address < hi)
        require(bool(used), 'Missing CODE window: ' + name)
        windows.append({'name': name, 'start': lo, 'end_exclusive': hi,
                        'occupied_bytes': len(used), 'highest_address': used[-1],
                        'trailing_free_bytes': hi - used[-1] - 1})
    require('ERROR' not in memory and 'No room' not in memory, 'Linker memory error')
    matches = re.findall(r'EXTERNAL RAM\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\d+)\s+(\d+)', memory, re.I)
    require(len(matches) == 1, 'Missing external RAM allocation')
    start, end = (int(value, 16) for value in matches[0][:2])
    size, capacity = (int(value) for value in matches[0][2:])
    ordinary_start = 0x400 if historical else 0x440
    reserved = 0 if historical else 64
    require(start == ordinary_start and start <= end < 0x1000 and size == end - start + 1 and
            capacity == 3072 - reserved and size + reserved <= 3072,
            'External RAM exceeds the ordinary XRAM window')
    stack = re.findall(r'Stack starts at: 0x([0-9a-f]+) \(sp set to 0x([0-9a-f]+)\) with (\d+) bytes available', memory, re.I)
    require(len(stack) == 1, 'Missing linked stack allocation')
    stack_start, initial_sp = (int(value, 16) for value in stack[0][:2])
    stack_size = int(stack[0][2])
    require(0x20 <= stack_start <= 0xff and initial_sp + 1 == stack_start and
            stack_start + stack_size == 256 and symbols.get('s_SSEG') == stack_start and
            symbols.get('l_SSEG') == stack_size, 'MAP/MEM stack allocation disagrees')
    # SDCC's DSEG area is a logical 128-byte allocation arena, not a physical
    # 128-byte object. Use its linker occupancy grid for physical placement.
    grid = re.findall(r'^0x([0-9a-f]{2}):\|((?:[^|]\|){16})$', memory, re.I | re.M)
    require(len(grid) == 16 and [int(row[0], 16) for row in grid] == list(range(0, 256, 16)),
            'Incomplete or duplicate internal RAM occupancy grid')
    cells = ''.join(row[1][::2] for row in grid)
    require(len(cells) == 256 and cells[stack_start:] == 'S' * stack_size and
            'S' not in cells[:stack_start], 'Static internal RAM overlaps stack')
    require(symbols.get('s_DSEG') == 0 and 0 <= symbols.get('l_DSEG', -1) <= 128,
            'Unexpected direct internal RAM allocation')
    require(symbols.get('l_ISEG') == 0 and symbols.get('l_PSEG') == 0,
            'Unqualified indirect or paged RAM allocation')
    for area in ('REG_BANK_0', 'REG_BANK_1', 'REG_BANK_2', 'REG_BANK_3', 'BIT_BANK', 'BSEG_BYTES', 'OSEG'):
        length = symbols.get('l_' + area, 0)
        base = symbols.get('s_' + area, 0)
        require(0 <= base and 0 <= length and (not length or base + length <= stack_start),
                'Static IRAM area exceeds the stack base: ' + area)
    require(symbols.get('_ak820_led_dma') == 0x200, 'LED DMA buffer moved')
    require((historical and '_ak820_flash_stage' not in symbols) or
            (not historical and symbols.get('_ak820_flash_stage') == 0x400), 'IAP stage moved or missing')
    require(symbols.get('s_XSEG') == start and symbols.get('l_XSEG', -1) >= 0 and
            symbols.get('l_XISEG', -1) >= 0 and
            start + symbols['l_XSEG'] == symbols.get('s_XISEG') and
            symbols['l_XSEG'] + symbols['l_XISEG'] == size and
            symbols['s_XISEG'] + symbols['l_XISEG'] == end + 1,
            'MAP/MEM XRAM allocation disagrees')
    return {'code_bytes': len(code), 'code_windows': windows,
            'xram': {'start': start, 'end_inclusive': end, 'bytes': size, 'capacity': capacity,
                     'reserved_bytes': reserved, 'total_bytes': size + reserved, 'physical_capacity': 3072},
            'internal_ram': {'static_bytes': stack_start, 'initial_sp': initial_sp,
                             'stack_capacity': stack_size, 'runtime_stack_bound': None,
                             'stack_margin': None, 'stack_qualified': False},
            'protected_windows_clear': True}


def check_short_calls(report, build, image):
    summary = report.get('short_calls')
    proof_path = build/'short-calls.json'
    if summary is None:
        require(not proof_path.exists() and not (build/'shortcalls-input').exists(),
                'Missing opt-in short-call provenance')
        return None
    require(isinstance(summary,dict) and report.get('shortcalls_sha256') == sha(QMK/'util/ak820_shortcalls.py'),
            'Unqualified short-call tool')
    relative = proof_path.relative_to(QMK).as_posix()
    records = [row for row in report['artifacts'] if row.get('path') == relative]
    require(summary.get('report') == relative and len(records)==1 and proof_path.is_file(),
            'Missing or ambiguous short-call proof')
    require(summary.get('report_sha256') == sha(proof_path) == records[0].get('sha256') and
            records[0].get('size') == proof_path.stat().st_size, 'Unbound short-call proof')
    proof = load_json(proof_path)
    require(summary.get('algorithm') == proof.get('algorithm') and
            summary.get('selected') == len(proof.get('candidates',[])) and
            summary.get('saved_bytes') == proof.get('saved_bytes'), 'Short-call summary differs')
    shortcalls.validate_saved(build,image,proof)
    return summary


def check_pass30(report, build, toolchain):
    """Replay the finite audited transform chain; never accept arbitrary flags.

    Temporary proof outputs leave the saved build untouched. Spill replay uses
    pinned SDCC to recapture typed metadata from the source-bound inputs.
    """
    import copy
    import tempfile
    import ak820_dce as dce
    import ak820_default_keymap as defaults
    import ak820_parameter_spills as spills
    import ak820_register_saves as registers
    import ak820_tailshare as tails
    import ak820_outline_audit as outlines
    from ak820_build_inputs import input_snapshot
    expected_flags = ('--opt-code-size -DAK820_READ_HOOK_PRESERVES_RN=1'
                      ' -DAK820_READ_HOOK_PRESERVES_RN=1 --callee-saves ' +
                      ','.join(AK820_CALLEE_SAVES) +
                      ' -DAK820_COMPRESS_DEFAULT_KEYMAP -DAK820_WORD_HOOKS_PRESERVE_RN=1')
    require(report.get('compiler_extra_flags') == expected_flags and
            report.get('audited_callee_saves') == list(AK820_CALLEE_SAVES) and
            report.get('outline_max_helpers') == 400 and
            report.get('experimental_iram_overlay') is None and
            report.get('xram_window') == [0x440, 0x1000] and
            all(report.get(option) is True for option in
                ('compress_default_keymap', 'nvm_read_block_asm',
                 'nvm_update_block_asm', 'keymap_words_asm')) and
            isinstance(report.get('short_calls'), dict),
            'Unqualified pass30 compiler/ABI/transform configuration')
    # Every consumed intermediate must belong to the build report. This also
    # rejects duplicate records, traversal, symlink escape and stale proofs.
    bound = {}
    for row in report.get('artifacts', []):
        name = row.get('path')
        require(isinstance(name, str) and '\\' not in name, 'Invalid pass30 artifact path')
        path = (QMK / name).resolve()
        require(path.is_relative_to(build) and path not in bound and path.is_file() and
                sha(path) == row.get('sha256') and path.stat().st_size == row.get('size'),
                'Unbound or changed pass30 artifact: ' + name)
        bound[path] = row
    def saved(path):
        path = Path(path).resolve()
        require(path in bound, 'Missing pass30 proof artifact: ' + str(path))
        return path
    def tree(directory, suffixes=('.asm', '.lst', '.rel')):
        paths = {p.relative_to(directory).as_posix(): saved(p)
                 for p in directory.rglob('*') if p.suffix in suffixes}
        require(bool(paths), 'Missing pass30 intermediate tree: ' + str(directory))
        return paths
    def same_asm(first, second):
        a = {p.relative_to(first).as_posix(): sha(p) for p in first.rglob('*.asm')}
        b = {p.relative_to(second).as_posix(): sha(p) for p in second.rglob('*.asm')}
        require(bool(a) and a == b, 'Pass30 transformation chain differs')
    for field, module in (('builder', 'build_ak820'), ('dce', 'ak820_dce'),
                          ('outliner', 'ak820_outline_audit'),
                          ('parameter_spills', 'ak820_parameter_spills'),
                          ('register_saves', 'ak820_register_saves'),
                          ('tailshare', 'ak820_tailshare')):
        require(report.get(field + '_sha256') == sha(QMK / 'util' / (module + '.py')),
                'Pass30 implementation differs: ' + module)
    obj = build / 'obj_ajazz_ak820_vial'
    compiled = saved(obj / 'cflags.txt').read_text().split()
    for define in ('AK820_COMPRESS_DEFAULT_KEYMAP', 'AK820_KEYMAP_WORDS_ASM',
                   'AK820_NVM_READ_BLOCK_ASM', 'AK820_NVM_UPDATE_BLOCK_ASM'):
        require(compiled.count('-D' + define) == 1, 'Missing audited kernel define: ' + define)
    require(compiled.count('-DAK820_WORD_HOOKS_PRESERVE_RN=1') == 1 and
            compiled.count('-DAK820_READ_HOOK_PRESERVES_RN=1') == 1,
            'Compiled kernel ABI assertions differ')
    generation = load_json(saved(build / 'default-keymap/generation.json'))
    bootstrap = saved(build / 'default-keymap/bootstrap.asm')
    include = saved(build / 'default-keymap/ak820_default_keymap.inc')
    require(generation.get('compiler_sha256') == SDCC46_PINS['sdcc'] and
            generation.get('generator_sha256') == sha(QMK / 'util/ak820_default_keymap.py') and
            generation.get('bootstrap_sha256') == sha(bootstrap) and
            generation.get('include_sha256') == sha(include) and
            generation.get('final_tables_verified') is True and
            include.read_text() == defaults.generate(bootstrap.read_text()),
            'Default keymap generation differs')
    final_keymaps = [p for name, p in tree(obj, ('.asm',)).items()
                    if name.endswith('/keymap_introspection.asm')]
    require(len(final_keymaps) == 1, 'Missing compiler default-keymap output')
    defaults.verify_final(final_keymaps[0].read_text(), bootstrap.read_text())
    for key in ('dependencies', 'final_dependencies'):
        require(isinstance(generation.get(key), dict) and generation[key],
                'Missing default generator dependencies')
        for name, digest in generation[key].items():
            path = Path(name).resolve()
            require((path.is_relative_to(QMK.resolve()) or path.is_relative_to(toolchain)) and
                    path.is_file() and sha(path) == digest, 'Default generator input changed')
    summaries = {}
    with tempfile.TemporaryDirectory(prefix='ak820-pass30-proof-') as temporary:
        temporary = Path(temporary)
        roots = ['_USB_DeviceInterrupt', '__mcs51_genXINIT', '_ak820_led_irq', '_ak820_timer_irq']
        require(report.get('external_roots') == roots, 'Pass30 external roots differ')
        dce.optimize(obj, temporary / 'dce', roots)
        same_asm(temporary / 'dce', build / 'parameter-spills-input')
        for field, source, target, module in (
                ('parameter_spills', 'parameter-spills-input', 'parameter-spills-output', spills),
                ('register_saves', 'register-saves-input', 'register-saves-output', registers),
                ('tail_share', 'tailshare-input', 'shortcalls-input', tails)):
            summary = report.get(field)
            require(isinstance(summary, dict), 'Missing pass30 transform: ' + field)
            proof_path = saved(QMK / summary.get('report', ''))
            require(summary.get('report_sha256') == sha(proof_path), 'Pass30 report hash differs')
            proof = load_json(proof_path)
            source, target = build / source, build / target
            tree(source)
            tree(target)
            replay_path = temporary / (field + '.json')
            replay_target = temporary / field
            if module is spills:
                certificate = saved(build / 'parameter-spills-context.json')
                require(summary.get('context_sha256') == sha(certificate) and
                        proof.get('context_sha256') == sha(certificate) and
                        proof.get('algorithm') == spills.ALGORITHM, 'Spill context or algorithm differs')
                manifest_path = saved(build / 'parameter-spills-metadata/manifest.json')
                require(proof.get('metadata_manifest_sha256') == sha(manifest_path),
                        'Spill typed metadata manifest differs')
                manifest = load_json(manifest_path)
                require(manifest.get('compiler_sha256') == SDCC46_PINS['sdcc'],
                        'Spill metadata compiler differs')
                for metadata in manifest.get('modules', {}).values():
                    require(metadata.get('compiler_sha256') == SDCC46_PINS['sdcc'] and
                            metadata.get('flags') == spills.compiler_flags(obj),
                            'Spill metadata compiler flags differ')
                    for name, digest in metadata.get('files_sha256', {}).items():
                        require(sha(saved(build / 'parameter-spills-metadata' / name)) == digest,
                                'Saved spill typed metadata changed')
                replay = spills.prepare(QMK, obj, source, replay_target,
                    temporary / 'metadata', certificate, replay_path,
                    toolchain / 'bin/sdcc', input_snapshot(QMK, toolchain))
                for key in ('selected', 'rejected', 'input_sha256', 'output_sha256',
                            'nominal_object_saved_bytes', 'extra_stack_bytes'):
                    require(replay[key] == proof.get(key), 'Spill source/type/opcode proof differs: ' + key)
                require(summary.get('selected') == len(proof['selected']), 'Spill selection summary differs')
                require(proof.get('postlink_qualified') is True and
                        summary.get('postlink_qualified') is True,
                        'Missing exact-image spill postlink qualification')
            else:
                replay = module.prepare(source, replay_target, replay_path)
                for key, value in replay.items():
                    require(value == proof.get(key), 'Transform replay differs: ' + field + '/' + key)
            same_asm(replay_target, target)
            checked = copy.deepcopy(proof)
            module.verify_assembled(source, target, replay_path, checked)
            require(checked == proof, 'Saved assembled proof differs: ' + field)
            if module is spills:
                stack_path = saved(build / 'parameter-spills-stack.json')
                spills.postlink_audit(QMK, build, certificate, replay_path, checked, stack_path)
                require(checked == proof, 'Saved spill postlink proof differs')
            require(summary.get('object_saved_bytes') == proof.get('object_saved_bytes') and
                    summary.get('extra_stack_bytes') == 0,
                    'Pass30 saved-byte or stack summary differs')
            summaries[field] = sha(proof_path)
        # The replayed stages must be adjacent, without an unrecorded rewrite.
        same_asm(build / 'parameter-spills-output', build / 'register-saves-input')
        same_asm(build / 'register-saves-output', build / 'dce-input')
        tree(build / 'dce-input')
        outlined = temporary / 'outlined'
        replay = outlines.outline_assembled(build / 'dce-input', outlined, max_helpers=400, min_saving=1)
        require(replay == load_json(saved(build / 'dce/outlining.json')), 'Outlining replay differs')
        same_asm(outlined, build / 'tailshare-input')
        summary = report.get('outlining', {})
        require(summary.get('report') == (build / 'dce/outlining.json').relative_to(QMK).as_posix() and
                summary.get('algorithm') == replay['algorithm'] and
                summary.get('helpers') == len(replay['selected_exact']) and
                summary.get('call_sites') == sum(row['occurrences'] for row in replay['selected_exact']) and
                summary.get('nominal_saved_bytes') == replay['selected_nominal_net_bytes'] and
                summary.get('extra_stack_bytes') == replay['extra_stack_bytes'],
                'Outlining summary differs')
    return {'contract': 'ak820-audited-pass30-1', 'reports': summaries}


def inspect(build, toolchain):
    build, toolchain = Path(build).resolve(), validate_tools(toolchain)
    require(build.is_relative_to(QMK.resolve()), 'Build must be beneath the QMK source root')
    report_path = build / 'build-report.json'
    report = load_json(report_path)
    selected = profiles.validate_configuration(report.get('configuration'))
    require(report.get('keyboard') == 'ajazz/ak820' and report.get('keymap') == 'vial' and
            report.get('build_id') == selected['nvm_schema'] and report.get('hardware_validated') is False,
            'Wrong target, saved schema or hardware claim')
    require(report.get('code_window') == [0x3027, 0xc700] and
            {tuple(window) for window in report.get('code_windows', [])} == set(WINDOWS) and
            report.get('xram_window') in ([0x400, 0x1000], [0x440, 0x1000]), 'Experimental linker windows cannot qualify')
    validate_inputs(report, QMK, toolchain)
    check_feature_defines(report, build, selected)
    historical = report.get('xram_window') == [0x400, 0x1000]
    expected_flags = '--opt-code-size --callee-saves ' + ','.join(AK820_CALLEE_SAVES)
    require(report.get('compiler_sha256') == SDCC46_PINS['sdcc'] and
            report.get('assembler_sha256') == SDCC46_PINS['sdas8051'], 'Unqualified compiler tools')
    if selected['profile'] in profiles.RELEASE_PROFILES:
        optimization = check_pass30(report, build, toolchain)
    else:
        require(report.get('compiler_extra_flags') == expected_flags and
                report.get('audited_callee_saves') == list(AK820_CALLEE_SAVES) and
                isinstance(report.get('outlining'), dict), 'Unqualified compiler/ABI/transform configuration')
        optimization = {'contract': 'historical-baseline'}
    ihx, mapfile, mem = (artifact(report, build, suffix) for suffix in ('ihx', 'map', 'mem'))
    short_summary = check_short_calls(report, build, ihx)
    code = diagnostic_build(ihx, mapfile, report_path)
    symbols = linked_symbols(mapfile)
    if selected['profile'] in profiles.RELEASE_PROFILES:
        for symbol in ('_ak820_eeprom_read_block_xdata', '_ak820_eeprom_update_block_xdata',
                       '_dynamic_keymap_get_keycode', '_dynamic_keymap_set_keycode',
                       '_dynamic_keymap_get_encoder', '_dynamic_keymap_set_encoder'):
            require(symbol in symbols and symbols[symbol] in code, 'Missing audited ASM kernel: ' + symbol)
    direct_allocations = re.findall(r'^D:\s+([0-9A-Fa-f]{8})\s+_g_direct_mode_colors\s+vialrgb\s*$',
                                    mapfile.read_text(), re.M)
    require(len(direct_allocations) == (1 if 'vialrgb-direct' in selected['optional_features'] else 0),
            'Compiled Direct allocation differs from profile')
    validate_startup(code, symbols)
    check_feature_symbols(retained_static_symbols(report, build, code), selected, code)
    resources = memory_report(code, symbols, mem.read_text(), historical=historical)
    resources['absolute_xram'] = check_absolute_xdata(report, build, historical=historical)
    require(resources['code_bytes'] == report.get('code_bytes'), 'CODE byte count disagrees')
    for window in resources['code_windows']:
        require(window['occupied_bytes'] == report.get('code_' + window['name'] + '_bytes'),
                'CODE window count disagrees')
    source_manifest_sha = hashlib.sha256(canonical(report['sources'])).hexdigest()
    identity = {'profile': selected['profile'], 'configuration_sha256': hashlib.sha256(canonical(selected)).hexdigest(),
                'ihx_sha256': sha(ihx), 'map_sha256': sha(mapfile), 'mem_sha256': sha(mem),
                'build_report_sha256': sha(report_path), 'source_manifest_sha256': source_manifest_sha,
                'compiler_sha256': report['compiler_sha256'], 'nvm_schema': selected['nvm_schema']}
    return {'format': FORMAT, 'configuration': selected, 'identity': identity,
            'short_calls': short_summary, 'optimization': optimization,
            'resources': resources, 'hardware_validated': False, 'physical_device_commands': 0,
            'offline_tests_passed': False, 'release_approved': False,
            'release_blockers': list(RELEASE_BLOCKERS),
            'settings_compatibility': 'Same schema is insufficient; installer requires an exact approved image.'}


def validate_tests(path, identity):
    report = load_json(path)
    expected = {'ihx': identity['ihx_sha256'], 'map': identity['map_sha256']}
    require(report.get('format') == 'ak820-offline-tests-1' and report.get('passed') is True and
            report.get('require_toolchain') is True and report.get('build_unchanged') is True and
            report.get('build_hashes') == expected and report.get('hardware_validated') is False and
            report.get('physical_device_commands') == 0 and report.get('iap_fault_profile') == 'guarded-erase' and
            report.get('unit_tests', {}).get('skipped') == 0 and report.get('unit_tests', {}).get('run', 0) > 0,
            'Offline report is incomplete, failed, skipped or belongs to a different image')
    tests = report.get('tests', [])
    require(len(tests) >= 28 and all(row.get('exit_code') == 0 and row.get('build_before') == expected and
            row.get('build_after') == expected and row.get('unit_tests', {}).get('skipped', 0) == 0
            for row in tests), 'Required host/CPU regressions did not all pass')
    # Reuse the complete, duplicate-free suite and argument contract used by
    # CI. Repeating one successful command cannot replace missing coverage.
    validate_qualification_contract(report)
    return {'sha256': sha(path), 'suites': len(tests), 'unit_tests': report['unit_tests']}


def require_release_approval(report, build_report=None, build=None, toolchain=None):
    # A scalar bound or caller-edited boolean cannot replace committed,
    # independently reviewed witnesses for this exact compiled program.
    require(isinstance(build_report, dict) and isinstance(report.get('identity'), dict),
            'No profile is approved for packaging without exact build and safety evidence')
    from ak820_release_safety import validate
    proof = validate(build_report)
    require(all(report['identity'].get(extension + '_sha256') == expected
                for extension, expected in proof['build_identity'].items()),
            'Safety build differs from inspected image, MAP or MEM')
    require(report['configuration'] == build_report.get('configuration'), 'Safety profile differs from inspected image')
    require(report['resources']['internal_ram']['stack_capacity'] == proof['stack_capacity'],
            'Safety stack capacity differs from linked placement')
    require(build is not None and toolchain is not None, 'Missing exact-image regression directory')
    configured = load_json(build / 'configuration-report.json')
    require(configured.get('identity') == report['identity'] and configured.get('offline_tests_passed') is True,
            'Configuration has no complete exact-image offline pass')
    qualification = validate_tests(build / 'qualification.json', report['identity'])
    validate_profile_tests(load_json(build / 'profile-tests/results.json'),
                           report['configuration']['profile'], report['identity'], build, toolchain)
    report['resources']['internal_ram'].update(runtime_stack_bound=proof['stack_bound'],
        stack_margin=proof['stack_margin'], stack_qualified=True)
    report.update(release_approved=True, release_blockers=[], release_safety=proof,
                  offline_tests_passed=True, qualification=qualification)
    return proof


def run_runtime_analysis(build, identity):
    """Record exact-image progress without treating partial bounds as approval."""
    output = build / 'runtime-stack.json'
    runner = QMK / 'tests/ak820_stack/analyze.py'
    command = [sys.executable, '-I', str(runner), '--build-dir', str(build), '--output', str(output)]
    log = build / 'runtime-stack.log'
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=QMK, stdout=stream, stderr=subprocess.STDOUT)
    require(result.returncode in (0, 2) and output.is_file(), 'Runtime stack analysis failed')
    report = load_json(output)
    require(report.get('identity', {}).get('ihx_sha256') == identity['ihx_sha256'] and
            report.get('identity', {}).get('map_sha256') == identity['map_sha256'] and
            report.get('analyzer_sha256') == sha(runner) and
            report.get('decoder_source_sha256') == sha(QMK / 'util/ak820_linked_inventory.py') and
            report.get('whole_program_qualified') is False,
            'Runtime stack report differs from this image or claims unapproved qualification')
    roots = report.get('roots', {})
    require(set(roots) == {'_main', '_ak820_timer_irq', '_USB_DeviceInterrupt', '_ak820_led_irq'},
            'Runtime stack report omitted a required root')
    unknown = [name for name, value in roots.items() if value.get('bound') is None]
    require(result.returncode == (2 if unknown else 0), 'Runtime stack exit status disagrees with bounds')
    return {'report_sha256': sha(output), 'log_sha256': sha(log), 'exit_code': result.returncode,
            'whole_program_qualified': False, 'unresolved_roots': unknown,
            'root_bounds': {name: value.get('bound') for name, value in roots.items()}}


def runtime_source_snapshot():
    names = ('tools/configure_firmware.py', 'tools/ak820_runtime_safety.py',
             'qmk-8051-ak820/tests/ak820_stack/analyze.py',
             'qmk-8051-ak820/tests/ak820_startup/stack_contract.py',
             'qmk-8051-ak820/tests/ak820_irq/run.py',
             'qmk-8051-ak820/tests/ak820_irq/oem-wrappers.json',
             'qmk-8051-ak820/tests/ak820_iap/run.py',
             'qmk-8051-ak820/tests/ak820_emitted/run.py',
             'qmk-8051-ak820/util/ak820_linked_inventory.py',
             'qmk-8051-ak820/util/pack_ak820.py')
    return {name: sha(ROOT / name) for name in names}


def run_runtime_safety(build, inspected, toolchain):
    """Recompute every proof; stored booleans never grant a successful result."""
    output = build / 'runtime-safety'
    output.mkdir(exist_ok=True)
    summary = output / 'summary.json'
    summary.unlink(missing_ok=True)
    sources = runtime_source_snapshot()
    identity = inspected['identity']
    run_runtime_analysis(build, identity)
    commands = [
        ('startup', [sys.executable, '-I', str(QMK / 'tests/ak820_startup/stack_contract.py'),
                     '--build-dir', str(build), '--output', str(output / 'startup.json')]),
        ('irq', [sys.executable, '-I', str(QMK / 'tests/ak820_irq/run.py'),
                 '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                 '--wrapper-fixture', str(QMK / 'tests/ak820_irq/oem-wrappers.json'),
                 '--output-dir', str(output / 'irq')]),
    ]
    for name, command in commands:
        print('RUN RUNTIME', name, flush=True)
        with (output / (name + '.log')).open('w') as stream:
            result = subprocess.run(command, cwd=QMK, stdout=stream, stderr=subprocess.STDOUT)
        require(result.returncode == 0, 'Runtime proof failed: ' + name)
    require(runtime_source_snapshot() == sources, 'Runtime proof sources changed during checks')
    require(inspect(build, toolchain)['identity'] == identity, 'Build changed during runtime checks')
    paths = {'foreground': build / 'runtime-stack.json', 'startup': output / 'startup.json',
             'irq': output / 'irq/results.json'}
    report = combine_runtime_safety(*(load_json(paths[name]) for name in ('foreground', 'startup', 'irq')),
                                    identity, inspected['resources']['internal_ram'], sources)
    report['reports'] = {name: {'path': path.relative_to(build).as_posix(), 'sha256': sha(path)}
                         for name, path in paths.items()}
    report['logs'] = {name: sha(output / (name + '.log')) for name in ('startup', 'irq')}
    report['simulator_sha256'] = sha(toolchain / 'bin/s51')
    summary.write_bytes(canonical(report))
    require(report['passed'], 'Runtime stack does not fit or has unresolved paths; see ' + str(summary))
    return report


def apply_runtime_safety(result, proof):
    require(proof.get('passed') is True and proof.get('identity') == result['identity'] and
            proof.get('release_approved') is False, 'Invalid runtime proof for this build')
    require(proof.get('source_files') == runtime_source_snapshot(), 'Runtime proof sources changed after checks')
    result['runtime_analysis'] = proof
    result['release_approved'] = False
    result['resources']['internal_ram'].update(runtime_stack_bound=proof['stack_bound'],
        stack_margin=proof['stack_margin'], stack_qualified=True)
    result['release_blockers'] = list(RELEASE_BLOCKERS[1:])


def profile_test_plan(name, build, toolchain):
    selected = profiles.configuration(name)
    output = build / 'profile-tests'
    plan = [('gates', ROOT, [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tools',
                             '-p', 'test_configure_firmware.py'])]
    plan.extend([
        ('firmware-matrix-gates', ROOT, [sys.executable, '-B', '-m', 'unittest', 'discover',
                                       '-s', 'tools', '-p', 'test_firmware_matrix.py']),
        ('catalog-bundle-gates', ROOT, [sys.executable, '-B', '-m', 'unittest', 'discover',
                                      '-s', 'tools', '-p', 'test_build_profile_catalog.py']),
        ('settings-catalog-gates', ROOT, [sys.executable, '-B', '-m', 'unittest', 'discover',
                                        '-s', 'tools/installer', '-p', 'test_catalog_settings.py']),
        ('capability-catalog-gates', ROOT, [sys.executable, '-B', '-m', 'unittest', 'discover',
                                          '-s', 'tools', '-p', 'test_build_capability_catalog.py']),
        ('outline-gates', QMK, [sys.executable, 'tests/ak820_optimization/outline_unit.py']),
        ('short-call-gates', QMK, [sys.executable, '-B', '-m', 'unittest', 'discover',
                                 '-s', 'tests/ak820_shortcalls', '-p', 'test_*.py']),
        ('core-compact-host', QMK, [sys.executable, 'tests/ak820_core_compact/run.py',
                                  '--output', str(output / 'core-compact-host.json')]),
        ('core-compact-linked', QMK, [sys.executable, 'tests/ak820_core_compact/linked.py',
                                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                                    '--output-dir', str(output / 'core-compact')]),
        ('emitted-linked', QMK, [sys.executable, 'tests/ak820_emitted/run.py',
                               '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                               '--output-dir', str(output / 'emitted')]),
        ('transport-linked', QMK, [sys.executable, 'tests/ak820_transport_retry/run.py',
                                 '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                                 '--output-dir', str(output / 'transport')]),
        ('stack-gates', QMK, [sys.executable, '-B', '-m', 'unittest', 'discover',
                            '-s', 'tests/ak820_stack', '-p', 'test_*.py']),
        ('runtime-safety-gates', ROOT, [sys.executable, '-B', '-m', 'unittest', 'discover',
                                      '-s', 'tools', '-p', 'test_runtime_safety.py']),
        ('delay-abi', QMK, [sys.executable, '-I', 'tests/ak820_delay/run.py',
                            '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                            '--output-dir', str(output / 'delay-abi')]),
        ('startup-gates', QMK, [sys.executable, '-B', '-m', 'unittest', 'discover',
                               '-s', 'tests/ak820_startup', '-p', 'test_stack_contract.py']),
        ('startup-stack', QMK, [sys.executable, 'tests/ak820_startup/stack_contract.py',
                               '--build-dir', str(build), '--output', str(output / 'startup-stack.json')]),
        ('irq-gates', QMK, [sys.executable, '-B', '-m', 'unittest', 'discover',
                           '-s', 'tests/ak820_irq', '-p', 'test_*.py']),
        ('release-safety-gates', ROOT, [sys.executable, '-B', '-m', 'unittest', 'discover',
                                      '-s', 'tools', '-p', 'test_release_safety.py']),
        ('outline-integrity', QMK, [sys.executable, 'tests/ak820_optimization/outline_integrity.py',
                                   '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                                   '--output-dir', str(output / 'outline-integrity')]),
        ('vialrgb-linked', QMK, [sys.executable, 'tests/ak820_vialrgb/linked.py',
                                '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                                '--output-dir', str(output / 'vialrgb')]),
    ])
    for feature, folder in (('nkro-control', 'ak820_nkro_control'), ('one-shot', 'ak820_oneshot')):
        if feature not in selected['optional_features']:
            continue
        if feature == 'nkro-control':
            host = [sys.executable, 'tests/ak820_nkro_control/host.py']
        else:
            host = [sys.executable, 'tests/ak820_tapping/run.py', '--oneshot', '--negative-controls',
                    '--output', str(output / 'one-shot-host.json')]
            if 'space-cadet' in selected['optional_features']:
                host.append('--space-cadet')
        plan.append((feature + '-host', QMK, host))
        plan.append((feature + '-linked', QMK,
                     [sys.executable, 'tests/' + folder + '/linked.py', '--build-dir', str(build),
                      '--s51', str(toolchain / 'bin/s51'), '--output-dir', str(output / folder)]))
    if 'space-cadet' in selected['optional_features'] and 'one-shot' not in selected['optional_features']:
        plan.append(('space-cadet-host', QMK,
                     [sys.executable, 'tests/ak820_tapping/run.py', '--space-cadet', '--negative-controls',
                      '--output', str(output / 'space-cadet-host.json')]))
    if 'mouse-keys' in selected['optional_features']:
        plan.append(('mouse-keys-host', QMK, [sys.executable, 'tests/ak820_mousekeys/host.py']))
        plan.append(('mouse-keys-linked', QMK, [sys.executable, 'tests/ak820_mousekeys/run.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                    '--output-dir', str(output / 'mouse-keys')]))
    if 'auto-shift' in selected['optional_features']:
        plan.append(('auto-shift-host', QMK, [sys.executable, 'tests/ak820_autoshift/host.py',
                    '--output', str(output / 'auto-shift-host.json')]))
        plan.append(('auto-shift-linked', QMK, [sys.executable, 'tests/ak820_autoshift/linked.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                    '--output-dir', str(output / 'auto-shift')]))
    for feature, folder in (('tap-dance', 'ak820_tap_dance'), ('key-overrides', 'ak820_key_overrides'), ('qmk-settings', 'ak820_settings')):
        if feature not in selected['optional_features']:
            continue
        plan.append((feature + '-host', QMK, [sys.executable, 'tests/' + folder + '/host.py']))
        plan.append((feature + '-linked', QMK, [sys.executable, 'tests/' + folder + '/linked.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                    '--output-dir', str(output / folder)]))
    if 'leader' in selected['optional_features']:
        plan.append(('leader-host', QMK, [sys.executable, 'tests/ak820_leader/host.py',
                    '--output', str(output / 'leader-host.json')]))
        plan.append(('leader-linked', QMK, [sys.executable, 'tests/ak820_leader/linked.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin' / 's51'),
                    '--output-dir', str(output / 'leader')]))
    if 'os-indicators' in selected['optional_features']:
        plan.append(('os-indicators-host', QMK, [sys.executable, 'tests/ak820_os_indicators/host.py',
                    '--output', str(output / 'os-indicators-host.json')]))
        plan.append(('os-indicators-linked', QMK, [sys.executable, 'tests/ak820_os_indicators/linked.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                    '--output-dir', str(output / 'os-indicators')]))
    if 'mac-pc' in selected['optional_features']:
        plan.append(('mac-pc-host', QMK, [sys.executable, 'tests/ak820_mac_pc/host.py',
                    '--output', str(output / 'mac-pc-host.json')]))
        plan.append(('mac-pc-linked', QMK, [sys.executable, 'tests/ak820_mac_pc/linked.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                    '--output-dir', str(output / 'mac-pc')]))
    if 'dynamic-macros' in selected['optional_features']:
        plan.append(('dynamic-macro-host', QMK, [sys.executable, 'tests/ak820_dynamic_macro/host.py',
                    '--output', str(output / 'dynamic-macro-host.json')]))
        plan.append(('dynamic-macro-linked', QMK, [sys.executable, 'tests/ak820_dynamic_macro/linked.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                    '--output-dir', str(output / 'dynamic-macro')]))
    if 'gui-lock' in selected['optional_features']:
        plan.append(('gui-lock-host', QMK, [sys.executable, 'tests/ak820_gui_lock/host.py']))
        plan.append(('gui-lock-linked', QMK, [sys.executable, 'tests/ak820_gui_lock/linked.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                    '--output-dir', str(output / 'gui-lock')]))
    if 'ctrl-gui-swap' in selected['optional_features']:
        plan.append(('ctrl-gui-host', QMK, [sys.executable, 'tests/ak820_ctrl_gui/host.py']))
        plan.append(('ctrl-gui-flags', QMK, [sys.executable, 'tests/ak820_ctrl_gui/flags.py']))
        plan.append(('ctrl-gui-linked', QMK, [sys.executable, 'tests/ak820_ctrl_gui/linked.py',
                    '--build-dir', str(build), '--s51', str(toolchain / 'bin/s51'),
                    '--output-dir', str(output / 'ctrl-gui')]))
    return plan


def test_source_snapshot():
    names = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).split(b'\0')
    selected = {}
    for raw in names:
        name = os.fsdecode(raw)
        if not name or not name.startswith(('tools/', 'tests/', 'qmk-8051-ak820/tests/',
                                            'qmk-8051-ak820/util/',
                                            'qmk-8051-ak820/keyboards/ajazz/ak820/tests/')):
            continue
        path = ROOT / name
        if path.suffix not in ('.py', '.c', '.h', '.inc'):
            continue
        require(path.is_file() and path.resolve().is_relative_to(ROOT), 'Test source escapes repository')
        selected[name] = sha(path)
    return selected


def validate_profile_tests(report, name, identity, build, toolchain):
    require(report.get('format') == 'ak820-profile-tests-1' and report.get('profile') == name and
            report.get('identity') == identity and report.get('passed') is True and
            report.get('hardware_validated') is False and report.get('physical_device_commands') == 0,
            'Profile tests failed or belong to another image')
    expected = profile_test_plan(name, build, toolchain)
    rows = report.get('tests', [])
    require(len(rows) == len(expected), 'Profile qualification omitted or duplicated a suite')
    require(report.get('source_files') == test_source_snapshot(), 'Profile test sources changed')
    for row, (identifier, cwd, command) in zip(rows, expected):
        require(row.get('id') == identifier and row.get('cwd') == str(cwd) and row.get('command') == command and
                row.get('exit_code') == 0 and row.get('build_before') == identity and row.get('build_after') == identity,
                'Profile suite identity, arguments, result or build differs')
        log = build / 'profile-tests' / (identifier + '.log')
        require(log.is_file() and row.get('log_sha256') == sha(log), 'Profile log changed or is missing')
        if any(command[index:index + 2] == ['-m', 'unittest'] for index in range(len(command) - 1)):
            counts = unittest_counts(log.read_text())
            require(counts['run'] > 0 and counts['skipped'] == 0, 'Gate tests are empty or skipped')


def run_profile_tests(name, build, toolchain, identity):
    output = build / 'profile-tests'
    require(not output.is_symlink(), 'Profile test output must not be a symlink')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    sources = test_source_snapshot()
    records = []
    test_env = dict(os.environ, AK820_SDCC_BIN=str((Path(toolchain) / 'bin').resolve()))
    for identifier, cwd, command in profile_test_plan(name, build, toolchain):
        before = inspect(build, toolchain)['identity']
        require(before == identity, 'Build changed before profile tests')
        log = output / (identifier + '.log')
        print('RUN PROFILE', identifier, flush=True)
        with log.open('w') as stream:
            result = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT,
                                    env=test_env)
        after = inspect(build, toolchain)['identity']
        records.append({'id': identifier, 'cwd': str(cwd), 'command': command,
                        'exit_code': result.returncode, 'log_sha256': sha(log),
                        'build_before': before, 'build_after': after})
        report = {'format': 'ak820-profile-tests-1', 'profile': name, 'identity': identity,
                  'source_files': sources, 'tests': records, 'hardware_validated': False,
                  'physical_device_commands': 0, 'passed': False}
        (output / 'results.json').write_bytes(canonical(report))
        require(result.returncode == 0 and before == after == identity, 'Profile suite failed: ' + identifier)
    require(test_source_snapshot() == sources, 'Test sources changed during profile qualification')
    report['passed'] = True
    validate_profile_tests(report, name, identity, build, toolchain)
    (output / 'results.json').write_bytes(canonical(report))
    return {'sha256': sha(output / 'results.json'), 'suites': [row['id'] for row in records],
            'source_files_sha256': hashlib.sha256(canonical(sources)).hexdigest()}


def qualify(directory, toolchain, before=None):
    """Qualify an existing linked image, with runtime gates before regressions."""
    before = source_identity() if before is None else before
    result = inspect(directory, toolchain)
    name = result['configuration']['profile']
    result['source'] = before
    output = directory / 'configuration-report.json'
    output.write_bytes(canonical(result))
    apply_runtime_safety(result, run_runtime_safety(directory, result, toolchain))
    output.write_bytes(canonical(result))
    qualification = directory / 'qualification.json'
    subprocess.run([sys.executable, str(ROOT / 'tools/test_keyboard.py'), '--host', '--require-toolchain',
                    '--toolchain', str(toolchain), '--build-dir', str(directory),
                    '--iap-fault-profile', 'guarded-erase', '--output', str(qualification)], cwd=ROOT, check=True)
    fresh = inspect(directory, toolchain)
    require(fresh['identity'] == result['identity'], 'Build changed during qualification')
    require(source_identity() == before, 'Git source changed during qualification')
    result['qualification'] = validate_tests(qualification, result['identity'])
    result['profile_tests'] = run_profile_tests(name, directory, toolchain, result['identity'])
    apply_runtime_safety(result, result['runtime_analysis'])
    result['offline_tests_passed'] = True
    output.write_bytes(canonical(result))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='List explicit combinations and deferred options')
    build = sub.add_parser('build', help='Build and test a development profile')
    selection = build.add_mutually_exclusive_group()
    selection.add_argument('--profile', choices=tuple(profiles.PROFILES), help='Named profile; defaults to main')
    selection.add_argument('--features', nargs='*', help='Explicit optional feature names; empty selects standard')
    build.add_argument('--short-calls', action=argparse.BooleanOptionalAction, default=None,
                       help='Verified foreground ACALL/AJMP relaxation; default for curated profiles')
    build.add_argument('--parameter-spills-context', type=Path,
                       help='Fresh reviewed source/IRQ context required for the audited release transform chain')
    build.add_argument('--build-dir', type=Path, required=True)
    build.add_argument('--toolchain', type=Path, default=ROOT / 'toolchains/sdcc-4.6.0')
    build.add_argument('--qmk-bin', type=Path, default=QMK / '.venv/bin/qmk')
    build.add_argument('--python', type=Path, default=Path(sys.executable),
                       help='Python from the QMK build environment')
    for name, help_text in (('inspect', 'Inspect linked resources'),
                            ('qualify', 'Run all offline gates for an existing linked image'),
                            ('check-runtime', 'Prove the exact-image stack and IRQ bound offline'),
                            ('package', 'Check release eligibility')):
        command = sub.add_parser(name, help=help_text)
        command.add_argument('--build-dir', type=Path, required=True)
        command.add_argument('--toolchain', type=Path, default=ROOT / 'toolchains/sdcc-4.6.0')
    args = parser.parse_args(argv)
    if args.command == 'list':
        print(json.dumps({'profiles': [profiles.configuration(name) for name in profiles.PROFILES],
                          'default_profile': profiles.DEFAULT_PROFILE,
                          'release_profiles': list(profiles.RELEASE_PROFILES),
                          'deferred': profiles.DEFERRED, 'conflicts': profiles.CONFLICTS,
                          'costs': 'Measure each complete linked image; deltas are not additive.',
                          'release_blockers': list(RELEASE_BLOCKERS)}, indent=2))
        return 0
    directory = args.build_dir.resolve()
    toolchain = validate_tools(args.toolchain)
    if args.command == 'build':
        name = (args.profile if args.profile else profiles.select(args.features)
                if args.features is not None else profiles.DEFAULT_PROFILE)
        profiles.configuration(name)
        require(not directory.exists() and directory.is_relative_to(QMK.resolve()),
                'Select a fresh build directory beneath the QMK source root')
        before = source_identity()
        command = [str(args.python.resolve()), str(QMK / 'util/build_ak820.py'),
                   '--profile', name, '--toolchain', str(toolchain),
                   '--qmk-bin', str(args.qmk_bin.resolve()), '--build-dir', str(directory)]
        if name in profiles.RELEASE_PROFILES:
            require(args.short_calls is not False, 'Release profiles require audited short calls')
            require(args.parameter_spills_context is not None and args.parameter_spills_context.is_file(),
                    'Release profiles require --parameter-spills-context FILE for this source/IRQ context')
            command += ['--compress-default-keymap', '--nvm-update-block-asm', '--nvm-read-block-asm',
                        '--keymap-words-asm', '--trim-parameter-spills', '--parameter-spills-context',
                        str(args.parameter_spills_context.resolve()), '--trim-register-saves',
                        '--tail-share', '--outline-max-helpers', '400']
        if args.short_calls is not None:
            command.append('--short-calls' if args.short_calls else '--no-short-calls')
        subprocess.run(command, cwd=QMK, check=True)
        result = qualify(directory, toolchain, before)
    elif args.command == 'qualify':
        result = qualify(directory, toolchain)
    else:
        result = inspect(directory, toolchain)
        if args.command == 'check-runtime':
            apply_runtime_safety(result, run_runtime_safety(directory, result, toolchain))
        elif args.command == 'package':
            require_release_approval(result, load_json(directory / 'build-report.json'), directory, toolchain)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('STOP: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
