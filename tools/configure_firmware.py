#!/usr/bin/env python3
"""Select, build and inspect AK820 development profiles without opening USB.

Only named feature combinations are accepted. Every build is linked inside the
real memory windows and tested against its own IHX/MAP. A passing CPU model is
not release approval: the missing whole-program stack proof blocks packaging.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
QMK = ROOT / 'qmk-8051-ak820'
sys.path.insert(0, str(QMK / 'util'))
import ak820_profiles as profiles
from build_ak820 import AK820_CALLEE_SAVES
from ak820_build_inputs import validate_inputs
from ak820_diagnose import diagnostic_build
from pack_ak820 import read_symbols, validate_startup
from ak820_ci_authorization import validate_qualification_contract
from build_release_bundle import SDCC46_PINS
from test_keyboard import unittest_counts

FORMAT = 'ak820-configured-build-1'
WINDOWS = ((0x28a0, 0x3000), (0x3027, 0xc700))
SYMBOLS = {'nkro-control': '_process_ak820_nkro', 'one-shot': '_ak820_oneshot_process'}
RELEASE_BLOCKERS = (
    'No reviewed whole-program foreground stack bound for this image.',
    'No exact-image IRQ/nesting proof combined with that foreground bound.',
    'No approved installer/settings transition for this feature identity.',
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
    return symbols


def check_absolute_xdata(report, build):
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
                match = re.fullmatch(r'([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(0x[0-9A-Fa-f]+|\d+)', line)
                if match:
                    declarations.append((path.name, match[1], int(match[2], 0)))
                elif absolute:
                    raise ValueError('Unqualified absolute XDATA declaration: ' + line)
    require(declarations == [('ak820_board.asm', '_ak820_led_dma', 0x200)],
            'Unqualified absolute XDATA object or hardware mapping')
    return [{'symbol': '_ak820_led_dma', 'start': 0x200, 'reserved_end_exclusive': 0x400}]


def retained_static_symbols(report, build, code):
    """Resolve private function labels without changing the firmware's ABI.

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
        for line in path.read_text().splitlines():
            label = re.match(r'^\s*([0-9A-F]{6})\s+\d+\s+(_[\w$]+):', line)
            if label and label[2] in SYMBOLS.values():
                require(label[2] not in found, 'Ambiguous feature handler')
                found[label[2]] = int(label[1], 16)
            instruction = re.match(r'^\s*([0-9A-F]{6})\s+((?:[0-9A-F]{2}\s+)+)\[\s*\d+\]', line)
            if instruction:
                address, raw = int(instruction[1], 16), bytes.fromhex(instruction[2])
                require(all(code.get(address + i) == byte for i, byte in enumerate(raw)),
                        'Relocated instruction differs from IHX')
    return found


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


def memory_report(code, symbols, memory):
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
    require(start == 0x400 and end < 0x1000 and size == end - start + 1 and capacity == 3072,
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
    require(symbols.get('s_XSEG') == start and symbols.get('s_XISEG', -1) +
            symbols.get('l_XISEG', -1) == end + 1, 'MAP/MEM XRAM allocation disagrees')
    return {'code_bytes': len(code), 'code_windows': windows,
            'xram': {'start': start, 'end_inclusive': end, 'bytes': size, 'capacity': capacity},
            'internal_ram': {'static_bytes': stack_start, 'initial_sp': initial_sp,
                             'stack_capacity': stack_size, 'runtime_stack_bound': None,
                             'stack_margin': None, 'stack_qualified': False},
            'protected_windows_clear': True}


def inspect(build, toolchain):
    build, toolchain = Path(build).resolve(), validate_tools(toolchain)
    require(build.is_relative_to(QMK.resolve()), 'Build must be beneath the QMK source root')
    report_path = build / 'build-report.json'
    report = load_json(report_path)
    selected = profiles.validate_configuration(report.get('configuration'))
    require(report.get('keyboard') == 'ajazz/ak820' and report.get('keymap') == 'vial' and
            report.get('build_id') == profiles.SCHEMA and report.get('hardware_validated') is False,
            'Wrong target, saved schema or hardware claim')
    require(report.get('code_window') == [0x3027, 0xc700] and
            {tuple(window) for window in report.get('code_windows', [])} == set(WINDOWS) and
            report.get('xram_window') == [0x400, 0x1000], 'Experimental linker windows cannot qualify')
    validate_inputs(report, QMK, toolchain)
    check_feature_defines(report, build, selected)
    expected_flags = '--opt-code-size --callee-saves ' + ','.join(AK820_CALLEE_SAVES)
    require(report.get('compiler_sha256') == SDCC46_PINS['sdcc'] and
            report.get('assembler_sha256') == SDCC46_PINS['sdas8051'] and
            report.get('compiler_extra_flags') == expected_flags and
            report.get('audited_callee_saves') == list(AK820_CALLEE_SAVES) and
            isinstance(report.get('outlining'), dict), 'Unqualified compiler/ABI/transform configuration')
    ihx, mapfile, mem = (artifact(report, build, suffix) for suffix in ('ihx', 'map', 'mem'))
    code = diagnostic_build(ihx, mapfile, report_path)
    symbols = linked_symbols(mapfile)
    validate_startup(code, symbols)
    handlers = retained_static_symbols(report, build, code)
    for feature, symbol in SYMBOLS.items():
        require((symbol in handlers and handlers[symbol] in code) ==
                (feature in selected['optional_features']), 'Compiled feature differs from profile: ' + feature)
    resources = memory_report(code, symbols, mem.read_text())
    resources['absolute_xram'] = check_absolute_xdata(report, build)
    require(resources['code_bytes'] == report.get('code_bytes'), 'CODE byte count disagrees')
    for window in resources['code_windows']:
        require(window['occupied_bytes'] == report.get('code_' + window['name'] + '_bytes'),
                'CODE window count disagrees')
    source_manifest_sha = hashlib.sha256(canonical(report['sources'])).hexdigest()
    identity = {'profile': selected['profile'], 'configuration_sha256': hashlib.sha256(canonical(selected)).hexdigest(),
                'ihx_sha256': sha(ihx), 'map_sha256': sha(mapfile), 'mem_sha256': sha(mem),
                'build_report_sha256': sha(report_path), 'source_manifest_sha256': source_manifest_sha,
                'compiler_sha256': report['compiler_sha256'], 'nvm_schema': profiles.SCHEMA}
    return {'format': FORMAT, 'configuration': selected, 'identity': identity,
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
    command = [sys.executable, str(runner), '--build-dir', str(build), '--output', str(output)]
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


def profile_test_plan(name, build, toolchain):
    selected = profiles.configuration(name)
    output = build / 'profile-tests'
    plan = [('gates', ROOT, [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tools',
                             '-p', 'test_configure_firmware.py'])]
    plan.extend([
        ('outline-gates', QMK, [sys.executable, 'tests/ak820_optimization/outline_unit.py']),
        ('stack-gates', QMK, [sys.executable, '-B', '-m', 'unittest', 'discover',
                            '-s', 'tests/ak820_stack', '-p', 'test_*.py']),
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
    return plan


def test_source_snapshot():
    names = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).split(b'\0')
    selected = {}
    for raw in names:
        name = os.fsdecode(raw)
        if not name or not name.startswith(('tools/', 'qmk-8051-ak820/tests/',
                                            'qmk-8051-ak820/keyboards/ajazz/ak820/tests/')):
            continue
        path = ROOT / name
        if path.suffix not in ('.py', '.c', '.h'):
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
        if identifier == 'gates':
            counts = unittest_counts(log.read_text())
            require(counts['run'] > 0 and counts['skipped'] == 0, 'Gate tests are empty or skipped')


def run_profile_tests(name, build, toolchain, identity):
    output = build / 'profile-tests'
    output.mkdir()
    sources = test_source_snapshot()
    records = []
    for identifier, cwd, command in profile_test_plan(name, build, toolchain):
        before = inspect(build, toolchain)['identity']
        require(before == identity, 'Build changed before profile tests')
        log = output / (identifier + '.log')
        print('RUN PROFILE', identifier, flush=True)
        with log.open('w') as stream:
            result = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT)
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='List explicit combinations and deferred options')
    build = sub.add_parser('build', help='Build and test a development profile')
    selection = build.add_mutually_exclusive_group(required=True)
    selection.add_argument('--profile', choices=tuple(profiles.PROFILES))
    selection.add_argument('--features', nargs='*', help='Explicit optional feature names; empty selects standard')
    build.add_argument('--build-dir', type=Path, required=True)
    build.add_argument('--toolchain', type=Path, default=ROOT / 'toolchains/sdcc-4.6.0')
    build.add_argument('--qmk-bin', type=Path, default=QMK / '.venv/bin/qmk')
    build.add_argument('--python', type=Path, default=Path(sys.executable),
                       help='Python from the QMK build environment')
    for name in ('inspect', 'package'):
        command = sub.add_parser(name, help='Inspect linked resources' if name == 'inspect' else 'Check release eligibility')
        command.add_argument('--build-dir', type=Path, required=True)
        command.add_argument('--toolchain', type=Path, default=ROOT / 'toolchains/sdcc-4.6.0')
    args = parser.parse_args(argv)
    if args.command == 'list':
        print(json.dumps({'profiles': [profiles.configuration(name) for name in profiles.PROFILES],
                          'deferred': profiles.DEFERRED, 'conflicts': profiles.CONFLICTS,
                          'costs': 'Measure each complete linked image; deltas are not additive.',
                          'release_blockers': list(RELEASE_BLOCKERS)}, indent=2))
        return 0
    directory = args.build_dir.resolve()
    toolchain = validate_tools(args.toolchain)
    if args.command == 'build':
        name = args.profile if args.profile else profiles.select(args.features)
        require(not directory.exists() and directory.is_relative_to(QMK.resolve()),
                'Select a fresh build directory beneath the QMK source root')
        before = source_identity()
        command = [str(args.python.resolve()), str(QMK / 'util/build_ak820.py'),
                   '--profile', name, '--toolchain', str(toolchain),
                   '--qmk-bin', str(args.qmk_bin.resolve()), '--build-dir', str(directory)]
        subprocess.run(command, cwd=QMK, check=True)
        result = inspect(directory, toolchain)
        result['source'] = before
        output = directory / 'configuration-report.json'
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
        result['runtime_analysis'] = run_runtime_analysis(directory, result['identity'])
        result['offline_tests_passed'] = True
        output.write_bytes(canonical(result))
    else:
        result = inspect(directory, toolchain)
        if args.command == 'package':
            require_release_approval(result, load_json(directory / 'build-report.json'), directory, toolchain)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('STOP: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
