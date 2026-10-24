#!/usr/bin/env python3
"""Bound the linked IRQ callbacks and exercise real OEM wrappers in uCsim.

The C52 CPU does not implement VS11K28A interrupt routing or peripherals.
Calls below supply the two-byte hardware return frame with LCALL, then run
the unchanged OEM prologue/epilogue and linked application callback. USB
ACK side effects and all distinct-source IRQ orderings are supplied explicitly.
This proves neither electrical IRQ timing nor whole-program stack bounds.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import itertools
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'util'))
import pack_ak820 as packer

spec = importlib.util.spec_from_file_location('irq_iap_support', HERE.parent / 'ak820_iap/run.py')
iap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(iap)
emitted = iap.emitted

IRQ = {'timer': (1, '_ak820_timer_irq'), 'usb': (7, '_USB_DeviceInterrupt'),
       'led': (10, '_ak820_led_irq')}
WRAPPER_FIXTURE = HERE / 'oem-wrappers.json'
WRAPPER_ORIGIN_SHA256 = '1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1'
WRAPPER_SHA256 = {
    1: 'f921c9a3adfd6426385f74d38b426a20384399af3f50239081fbdfaa6faf7604',
    7: 'f4032f22e88be0585c01997aa639d4a5053148023c61373b2ee61b2fbdde7787',
    10: '6a8dc9d11b317c78a9f0e7291210738370bc0d454dc76399842914d4327d12b4',
}
HELPER_ADDRESS, HELPER_BYTES = 0x0DC4, bytes.fromhex('8a838982e473')
ROW = re.compile(r'^\s*([0-9A-F]{6})\s+((?:[0-9A-F]{2}\s+)+)\[\s*\d+\]\s+\d+\s+(.+)$')


def direct_target(pc, raw):
    """Decode LJMP/LCALL and page-relative AJMP/ACALL using post-PC page."""
    if raw[0] in (0x02, 0x12):
        return int.from_bytes(raw[1:3], 'big')
    if raw[0] & 0x1F in (0x01, 0x11):
        return ((pc + 2) & 0xF800) | ((raw[0] & 0xE0) << 3) | raw[1]
    return None


def direct_references(instructions, target):
    return [pc for pc, raw in instructions.items() if direct_target(pc, raw) == target]


def masked_helper_calls(instructions, target, irq_pcs, reached, clear, enable):
    outside = [pc for pc in direct_references(instructions, target) if pc not in irq_pcs]
    assert target in reached, (target, 'helper absent from initialization')
    assert all(pc in reached and clear < pc < enable for pc in outside), (target, outside)
    return outside


def linear_init_pcs(analyzer, init, entry):
    at, linear = entry, []
    while True:
        raw = analyzer.instruction(at)
        assert raw is not None and len(linear) < 512, (init, at)
        linear.append(at)
        if raw[0] == 0x22:
            return linear
        jump = raw[0] == 0x02 or raw[0] & 0x1F == 0x01
        assert not jump and raw[0] not in (0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x73, 0x80, 0xD5) and not (0xB4 <= raw[0] <= 0xBF or 0xD8 <= raw[0] <= 0xDF), (init, at, 'nonlinear initialization')
        at += len(raw)


def reject_priority_write(raw, pc):
    """Decode direct/bit destinations, independent of assembler symbol names."""
    op = raw[0]
    direct = None
    if op in (0x05, 0x15, 0x42, 0x43, 0x52, 0x53, 0x62, 0x63,
              0x75, 0x86, 0x87, 0xC5, 0xD0, 0xD5, 0xF5) or 0x88 <= op <= 0x8F:
        direct = raw[1]
    elif op == 0x85:
        direct = raw[2]
    bit = raw[1] if op in (0x10, 0x92, 0xB2, 0xC2, 0xD2) else None
    assert direct not in (0xB8, 0xE9), f'IRQ priority write at {pc:#x}'
    assert bit is None or bit & 0xF8 != 0xB8, f'IRQ priority bit write at {pc:#x}'


def wrapper_bytes(stock, ordinal):
    address = 0x1858 + ordinal * 76
    raw = stock[address:address + 76]
    prefix = bytes.fromhex('c0e0c0f0c083c082c0d075d000') + b''.join(bytes((0xC0, r)) for r in range(8))
    suffix = b''.join(bytes((0xD0, r)) for r in reversed(range(8))) + bytes.fromhex('d0d0d082d083d0f0d0e032')
    assert raw[:29] == prefix and raw[49:] == suffix
    assert raw[29:35] == bytes.fromhex('7b007a30') + bytes((0x79, ordinal * 3))
    assert raw[46:49] == bytes.fromhex('120dc4')
    assert stock[0x0DC4:0x0DCA] == bytes.fromhex('8a838982e473')
    return address, raw


def load_wrapper_fixture(path=WRAPPER_FIXTURE):
    """Load only the reviewed OEM instructions; never construct an OEM ROM."""
    serialized = path.read_bytes()
    try:
        fixture = json.loads(serialized)
        if fixture['format'] != 'ak820-public-irq-wrappers-1':
            raise ValueError('Unsupported IRQ wrapper fixture')
        origin = fixture['origin']
        if (origin['stock_rom_sha256'] != WRAPPER_ORIGIN_SHA256 or
                origin['protected_region_sha256'] != packer.PROTECTED_SHA):
            raise ValueError('Unrecognized IRQ wrapper origin')

        def block(record, address, expected_sha):
            raw = bytes.fromhex(record['hex'])
            if (record['address'] != address or record['bytes'] != len(raw) or
                    record['sha256'] != expected_sha or packer.digest(raw) != expected_sha):
                raise ValueError('IRQ wrapper bytes or identity differ from the reviewed reference')
            return address, raw

        block(fixture['helper'], HELPER_ADDRESS, packer.digest(HELPER_BYTES))
        if set(fixture['wrappers']) != set(IRQ):
            raise ValueError('IRQ fixture must contain exactly Timer0, USB and LED')
        wrappers = {}
        for name, (ordinal, _) in IRQ.items():
            record = fixture['wrappers'][name]
            if record['ordinal'] != ordinal:
                raise ValueError('Incorrect IRQ wrapper ordinal')
            wrappers[name] = block(record, 0x1858 + ordinal * 76, WRAPPER_SHA256[ordinal])
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError('Incomplete IRQ wrapper fixture') from error
    return wrappers, {'kind': 'public-pinned-wrapper-fixture',
                      'fixture_sha256': packer.digest(serialized), 'origin': origin,
                      'instruction_bytes': len(HELPER_BYTES) + sum(len(raw) for _, raw in wrappers.values())}


def load_wrappers(stock_path=None, fixture_path=None):
    if stock_path is not None and fixture_path is not None:
        raise ValueError('Choose either a complete OEM ROM or the public wrapper fixture')
    if stock_path is None:
        return load_wrapper_fixture(fixture_path or WRAPPER_FIXTURE)
    stock = stock_path.read_bytes()
    packer.validate_native(stock)
    wrappers = {name: wrapper_bytes(stock, ordinal) for name, (ordinal, _) in IRQ.items()}
    return wrappers, {'kind': 'validated-private-stock-rom', 'stock_rom_sha256': packer.digest(stock)}


def cpu_case(fw, wrappers, order, reserve):
    """Inject each distinct source at callback entry, then unwind real wrappers."""
    console = iap.Console(fw.simulator, fw.image)
    try:
        console.command(fw.initialize())
        console.command(emitted.memory('rom', HELPER_ADDRESS, HELPER_BYTES))
        for name, (ordinal, symbol) in IRQ.items():
            address, raw = wrappers[name]
            console.command([emitted.memory('rom', address, raw),
                             emitted.memory('rom', 0x3000 + ordinal * 3, packer.ljmp(fw.address(symbol)))])
        stack_start = fw.initial_sp + reserve
        assert stack_start < 0xE0
        registers = bytes((0x30 + i) & 255 for i in range(32))
        console.command([emitted.memory('iram', 0, registers),
                         f'fill iram {fw.initial_sp + 1:#x} {stack_start:#x} 0xa7',
                         emitted.memory('sfr', 0x81, [stack_start, 0x34, 0x12]),
                         emitted.memory('sfr', 0xA8, [0]),
                         emitted.memory('sfr', 0xD0, [0xD0]),
                         emitted.memory('sfr', 0xE0, [0xA5]),
                         emitted.memory('sfr', 0xF0, [0x5A]),
                         emitted.memory('sfr', 0xA6, [0x1E]),
                         emitted.memory('xram', 0x1000, [0, 9, 1, 0, 0, 0, 0, 0]),
                         emitted.memory('xram', 0x220F, [0x38]),
                         emitted.memory('xram', 0x223D, [0x20]),
                         'break xram w 0x220f'])

        def snapshot():
            return (console.read('iram', 0, 8),
                    {a: console.read('sfr', a, 1) for a in (0x81, 0x82, 0x83, 0xD0, 0xE0, 0xF0)})

        def run_to(start, stop):
            result = console.command(f'run {start:#x} {stop:#x}')
            while "Event `write' at xram[0x220f]" in result:
                console.command(emitted.memory('xram', 0x223D, [0]))
                result = console.command('run')
            assert f'0x{stop:04x}' in result.lower(), result

        def invoke(depth):
            name = order[depth]
            before = snapshot()
            wrapper, _ = wrappers[name]
            stub, trap = 0x2600 + depth * 16, 0x2700 + depth * 16
            console.command(emitted.memory('rom', stub, [0x12, wrapper >> 8, wrapper & 255,
                                                         0x02, trap >> 8, trap & 255]))
            entry = fw.address(IRQ[name][1])
            run_to(stub, entry)
            if depth + 1 < len(order):
                invoke(depth + 1)
            run_to(entry, trap)
            assert snapshot() == before, (order, depth, 'register/frame preservation')

        invoke(0)
        assert console.read('iram', fw.initial_sp + 1, reserve) == [0xA7] * reserve
        state = console.command('state')
        peak = int(re.findall(r'Most value of stack pointer=\s+0x([0-9a-f]+)', state)[-1], 16)
        return {'irq_order': list(order), 'reserved_main_bytes': reserve,
                'peak_sp': peak, 'irq_stack_bytes': peak - stack_start,
                'canary_and_registers_preserved': True}
    finally:
        (fw.output / ('-'.join(order) + '.log')).write_text(console.log)
        console.close()


def emitted_contracts(fw, analyzer, callback_reports):
    irq_pcs = set().union(*(set(r['reachable']) for r in callback_reports.values()))
    def destination(raw):
        op = raw[0]
        if op in (5, 0x15, 0x42, 0x43, 0x52, 0x53, 0x62, 0x63, 0x75,
                  0x86, 0x87, 0xC5, 0xD0, 0xD5, 0xF5) or 0x88 <= op <= 0x8F:
            return raw[1]
        return raw[2] if op == 0x85 else None
    enabled, restored_masks = [], []
    for pc, raw in analyzer.instructions.items():
        direct = destination(raw)
        bit = raw[1] if raw[0] in (0x10, 0x92, 0xB2, 0xC2, 0xD2) else None
        # Bank0 is the compiler ABI. Other banks may contain DSEG objects.
        assert direct != 0xD0 and bit not in (0xD3, 0xD4), f'Register bank change {pc:#x}'
        if bit is not None and bit & 0xF8 in (0xA8, 0xE8) and raw[0] in (0x92, 0xB2, 0xD2):
            assert bit in (0xA9, 0xAE, 0xAF, 0xE9, 0xED), f'Unexpected enabled source {pc:#x}'
            enabled.append({'pc': pc, 'bit': bit})
        if direct in (0xA8, 0xE8):
            # Only two foreground save/restore sites write IE as a byte.
            assert raw == bytes((0xF5, 0xA8)), f'Unknown source-mask write {pc:#x}'
            assert pc not in irq_pcs, f'IRQ mask byte write {pc:#x}'
            load = analyzer.instruction(pc - 4)
            assert load and load[0] == 0x90 and analyzer.instruction(pc - 1) == b'\xe0', ('unknown IE restore', pc)
            address = int.from_bytes(load[1:], 'big')
            names = [name for name, at in fw.symbols.items() if at == address and
                     (name.startswith('_flash_operation_previous_ie_') or name.startswith('_bootloader_jump_saved_ie_'))]
            assert len(names) == 1, ('unrecognized saved IE cell', pc, address)
            uses = []
            for listing in (fw.build / 'dce').rglob('*.rst'):
                uses.extend(row.split(';', 1)[0] for row in listing.read_text().splitlines() if names[0] in row.split(';', 1)[0])
            # One private allocation and exactly two direct DPTR accesses: no
            # compiler-emitted address escape, parameter passing or other use.
            assert len(uses) == 3 and sum('mov' in row and 'dptr,#' + names[0] in row for row in uses) == 2, ('saved IE escapes', names, uses)
            saves = [at for at, row in analyzer.instructions.items() if row == load and
                     analyzer.instruction(at + 3) == bytes((0xE5, 0xA8)) and
                     analyzer.instruction(at + 5) == b'\xf0']
            assert len(saves) == 1 and saves[0] < pc, ('IE save provenance', names, saves)
            restored_masks.append({'restore_pc': pc, 'save_pc': saves[0], 'saved_byte': names[0], 'address': address})
    sharing = []
    for init, bit, helpers in (('_timer_init', 0xAF, ('_timer_reload',)),
                              ('_USB_Device_Init', 0xE9, ('_endpoints_reset', '_raw_abort'))):
        report = analyzer.bound(fw.address(init))
        assert report['bound'] is not None, (init, report['unresolved'])
        reached = set(report['reachable'])
        # Initialization roots must execute their mask and calls in order.
        linear = linear_init_pcs(analyzer, init, fw.address(init))
        clears = [pc for pc in linear if analyzer.instruction(pc) == bytes((0xC2, bit))]
        sets = [pc for pc in linear if analyzer.instruction(pc) == bytes((0xD2, bit))]
        assert len(clears) == len(sets) == 1, (init, clears, sets)
        for helper in helpers:
            target = fw.address(helper)
            outside = masked_helper_calls(analyzer.instructions, target, irq_pcs, reached, clears[0], sets[0])
            sharing.append({'helper': helper, 'foreground_calls': outside,
                            'disabled_bit': bit, 'clear_pc': clears[0], 'enable_pc': sets[0]})
    modules = ('ak820_timer.rst', 'protocol/ch555/usb_ak820.rst', 'ak820_board.rst')
    allocations = []
    for path in sorted((fw.build / 'dce').rglob('*.rst')):
        module = str(path.relative_to(fw.build / 'dce'))
        area = ''
        for row in path.read_text().splitlines():
            section = re.search(r'\.area\s+(\w+)', row)
            if section:
                area = section[1]
            allocation = re.match(r'^\s*([0-9A-F]{6})\s+\d+\s+\.ds\s+(\d+)', row)
            if allocation and int(allocation[2]):
                assert module not in modules[:2] or area != 'OSEG', f'IRQ module overlay allocation: {module}'
                if area in ('DSEG', 'OSEG', 'XSEG', 'BSEG'):
                    allocations.append({'module': module, 'area': area,
                                        'address': int(allocation[1], 16), 'size': int(allocation[2])})
    irq_storage = [a for a in allocations if a['module'] in modules[:2] or (a['module'] == 'ak820_board.rst' and a['area'] == 'XSEG')]
    for own in irq_storage:
        for other in allocations:
            if own is other:
                continue
            direct = {'DSEG', 'OSEG', 'BSEG'}
            same_space = own['area'] == other['area'] or {own['area'], other['area']} <= direct
            if same_space:
                left, right = own, other
                if (own['area'] == 'BSEG') != (other['area'] == 'BSEG'):
                    def byte_range(item):
                        start, end = item['address'], item['address'] + item['size']
                        return (0x20 + start // 8, 0x20 + (end + 7) // 8) if item['area'] == 'BSEG' else (start, end)
                    a, b = byte_range(left), byte_range(right)
                else:
                    a, b = (left['address'], left['address'] + left['size']), (right['address'], right['address'] + right['size'])
                assert a[1] <= b[0] or b[1] <= a[0], ('IRQ storage overlap', own, other)
    return {'compiler_register_bank': 0, 'source_enable_sites': enabled, 'saved_ie_restores': restored_masks,
            'shared_helper_masked_init_calls': sharing, 'nonoverlay_allocations': irq_storage,
            'limits': ['Nooverlay storage and masked shared helper calls are checked; foreground/ISR protocol state still uses its explicit concurrency protocol.']}


def selector_cases(fw, analyzer):
    masks = [pc for pc in analyzer.instructions if analyzer.masked_bit_dispatch(pc) is not None]
    assert len(masks) == 1, masks
    mask = masks[0]
    assert analyzer.instruction(mask) == bytes((0x54, 15))
    # Native selector prelude: MOV A,LED_COLUMN; JBC ACC.4,masked arm.
    entries = [pc for pc, raw in analyzer.instructions.items()
               if raw == bytes((0xE5, 0xA6)) and analyzer.instruction(pc + 2)
               and analyzer.instruction(pc + 2)[:2] == bytes((0x10, 0xE4))
               and pc + 5 + analyzer.instruction(pc + 2)[2] == mask]
    assert len(entries) == 1, entries
    entry = entries[0]
    console = iap.Console(fw.simulator, fw.image)
    try:
        console.command(fw.initialize())
        for value in range(256):
            console.command([emitted.memory('sfr', 0xA6, [value]),
                             emitted.memory('sfr', 0x80, [255]),
                             emitted.memory('sfr', 0xB0, [255]),
                             emitted.memory('sfr', 0xF1, [255]),
                             emitted.memory('rom', 0x2600, [0x12, entry >> 8, entry & 255, 2, 0x27, 0]),
                             'run 0x2600 0x2700'])
            actual = [console.read('sfr', a, 1)[0] for a in (0x80, 0xB0, 0xF1)]
            expected = [255, 255, 255]
            if value & 16:
                index = value & 15
                expected[index // 8] &= ~(1 << (index % 8))
            else:
                expected[2] = (~((value & 1) + 1) - 1) & 255
            assert actual == expected, (value, actual, expected)
        return {'input_values_checked': 256, 'valid_native_values_unchanged': '0x10..0x1f',
                'entry': entry, 'mask': mask, 'bounded_table_entries': 16}
    finally:
        (fw.output / 'selector-256.log').write_text(console.log)
        console.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--s51', type=Path, required=True)
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--stock-rom', type=Path,
                        help='Validate a complete private OEM ROM and use its actual IRQ wrappers')
    source.add_argument('--wrapper-fixture', type=Path,
                        help='Use a hash-pinned public instruction fixture (default: bundled oem-wrappers.json)')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--main-sample-bytes', type=int, default=56,
                        help='Representative main stack reservation, not a whole-program bound')
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    wrappers, wrapper_source = load_wrappers(args.stock_rom, args.wrapper_fixture)
    spec = importlib.util.spec_from_file_location('irq_stack_analysis', HERE.parent / 'ak820_stack/analyze.py')
    stack = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stack)
    instructions, _, code, provenance = stack.load(fw.build)
    analyzer = stack.Analyzer(instructions, code)
    callback_reports = {name: analyzer.bound(fw.address(symbol)) for name, (_, symbol) in IRQ.items()}
    for name, report in callback_reports.items():
        assert report['bound'] is not None, (name, report['unresolved'])
        for pc in report['reachable']:
            raw = analyzer.instruction(pc)
            reject_priority_write(raw, pc)
            assert raw[0] != 0x32, f'Early RETI in callback at {pc:#x}'
    bounds = {name: 17 + report['bound'] for name, report in callback_reports.items()}
    orders = [order for length in range(1, 4) for order in itertools.permutations(IRQ, length)]
    total = sum(bounds.values())
    if not 0 < args.main_sample_bytes or args.main_sample_bytes + total > fw.stack_capacity:
        raise ValueError('Representative main frame plus nested IRQ exceeds the linked stack capacity')
    contracts = emitted_contracts(fw, analyzer, callback_reports)
    cases = [cpu_case(fw, wrappers, order, args.main_sample_bytes) for order in orders]
    for case in cases:
        expected = sum(bounds[name] for name in case['irq_order'])
        assert case['irq_stack_bytes'] <= expected, (case, bounds)
    selector = selector_cases(fw, analyzer)
    result = {'pass': True, 'scope': 'linked CPU instructions and explicit peripheral/interrupt model',
              'linked_image_sha256': packer.digest(fw.image.read_bytes()),
              'linked_map_sha256': packer.digest((fw.build / 'ajazz_ak820_vial.map').read_bytes()),
              'stock_rom_sha256': wrapper_source.get('stock_rom_sha256'),
              'wrapper_source': wrapper_source,
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'initial_sp': fw.initial_sp, 'stack_capacity': fw.stack_capacity,
              'wrapper_bytes_on_stack': 17, 'irq_bounds': bounds,
              'callback_static_reports': callback_reports,
              'stack_analyzer_sha256': hashlib.sha256((HERE.parent / 'ak820_stack/analyze.py').read_bytes()).hexdigest(),
              'all_distinct_source_irq_bound': total,
              'ordered_nests': [{'irq_order': list(order), 'stack_bound': sum(bounds[n] for n in order)} for order in orders],
              'sample_main_plus_nested_irq_bytes': args.main_sample_bytes + total,
              'sample_remaining_bytes': fw.stack_capacity - args.main_sample_bytes - total,
              'cpu_cases': cases, 'selector_cases': selector, 'emitted_contracts': contracts,
              'limits': ['Main stack reservation is an observed-scenario example, not a whole-program bound.',
                         'Indirect dispatch bounds use the shared analyzer complete guarded or masked table idioms.',
                         'MCS51 in-service/RETI semantics are an explicit target architectural assumption; no priority-level count is assumed.',
                         'Boot entry does not normalize IP/IP_EX; all 15 distinct-source ordered nests are bounded and exercised.',
                         'USB ACK side effect and nested hardware return frames are supplied by the fixture.',
                         'No physical USB, flash, LED DMA or interrupt timing test; shared protocol-state synchronization remains separate.']}
    (fw.output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
