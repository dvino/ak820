#!/usr/bin/env python3
"""Conservative control-stack analysis of exact linked instructions; no device I/O."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'util'))
from ak820_linked_inventory import OPCODE_LENGTHS

ROW = re.compile(r'^\s*([0-9A-F]{6})\s+((?:[0-9A-F]{2}\s+)+)\[\s*\d+\]\s+\d+\s+(.+)$')


def load(build):
    image = build / 'ajazz_ak820_vial.ihx'
    mapping = build / 'ajazz_ak820_vial.map'
    code = {}
    eof = False
    for line in image.read_text().splitlines():
        if not line.startswith(':') or eof:
            raise ValueError('Malformed IHX')
        data = bytes.fromhex(line[1:])
        if len(data) < 5 or len(data) != data[0] + 5 or sum(data) & 255:
            raise ValueError('Invalid IHX length/checksum')
        if data[3] == 1:
            if data[0] or data[1:3] != b'\0\0':
                raise ValueError('Malformed EOF')
            eof = True
        elif data[3] == 0:
            start = int.from_bytes(data[1:3], 'big')
            for i, value in enumerate(data[4:-1]):
                address = start + i
                if address > 65535 or address in code:
                    raise ValueError('Overlapping or out-of-range IHX')
                code[address] = value
        else:
            raise ValueError('Only 16-bit IHX accepted')
    if not eof:
        raise ValueError('Missing IHX EOF')
    instructions, listings = {}, {}
    for path in sorted((build / 'dce').rglob('*.rst')):
        listings[str(path.relative_to(build))] = hashlib.sha256(path.read_bytes()).hexdigest()
        for row in path.read_text().splitlines():
            match = ROW.match(row)
            if not match:
                continue
            address, raw = int(match[1], 16), bytes.fromhex(match[2])
            if not OPCODE_LENGTHS[raw[0]] or len(raw) != OPCODE_LENGTHS[raw[0]]:
                raise ValueError(f'Invalid opcode length at {path}:{address:04x}')
            if any(code.get(address + i) != value for i, value in enumerate(raw)):
                raise ValueError(f'Listing/IHX mismatch: {path}:{address:04x}')
            if address in instructions and instructions[address] != raw:
                raise ValueError(f'Conflicting instruction at {address:04x}')
            instructions[address] = raw
    owners = {}
    for pc, raw in instructions.items():
        for byte in range(pc, pc + len(raw)):
            if byte in owners and owners[byte] != pc:
                raise ValueError(f'Overlapping instruction listings at {byte:04x}')
            owners[byte] = pc
    symbols = {name: int(address, 16) for address, name in re.findall(
        r'^(?:[CD]:)?\s+([0-9A-F]{8})\s+(_\S+)', mapping.read_text(), re.M)}
    return instructions, symbols, code, {'ihx_sha256': hashlib.sha256(image.read_bytes()).hexdigest(),
        'map_sha256': hashlib.sha256(mapping.read_bytes()).hexdigest(), 'listing_sha256': listings}


class Analyzer:
    def __init__(self, instructions, code=None):
        self.instructions = dict(instructions)
        occupied = set()
        for pc, raw in instructions.items():
            if not raw or not OPCODE_LENGTHS[raw[0]] or len(raw) != OPCODE_LENGTHS[raw[0]]:
                raise ValueError(f'Invalid instruction size at {pc:04x}')
            addresses = set(range(pc, pc + len(raw)))
            if occupied.intersection(addresses):
                raise ValueError(f'Overlapping instructions at {pc:04x}')
            occupied.update(addresses)
        self.code = code or {pc + i: value for pc, raw in instructions.items() for i, value in enumerate(raw)}
        self.memo = {}
        self.active = []
        self.owners = {pc + i: pc for pc, raw in instructions.items() for i in range(len(raw))}
        self.decoded_from_image = set()
        self.pointer_transfers = {}

    def rom_pointer_thunk(self, start):
        """Bounded straight-line value tracking through a const-ROM RET thunk.

        Only the small instruction subset below is accepted. Data values carry
        their ROM-byte provenance; call return bytes carry separate provenance.
        A callback transfer requires consecutive ROM bytes above a genuine
        LCALL return pair. The pushed pointer is consumed by RET, while the
        original LCALL frame remains live throughout the callback.
        """
        first = self.instruction(start)
        if not first or first[0] != 0x90:
            return None
        regs, stack, seen, pc, peak = {}, [], set(), start, 0
        def get(direct):
            return regs.get(direct)
        def put(direct, value):
            if direct not in (*range(8), 0x82, 0x83, 0xE0, 0xF0):
                return False
            regs[direct] = value
            return True
        for _ in range(128):
            if pc in seen or len(stack) > 32:
                return None
            seen.add(pc)
            raw = self.instruction(pc)
            if not raw:
                return None
            op, following = raw[0], pc + len(raw)
            if op == 0x90:
                regs[0x83], regs[0x82] = (raw[1], None), (raw[2], None)
            elif op == 0xE4:
                regs[0xE0] = (0, None)
            elif op == 0x93:
                hi, lo, acc = get(0x83), get(0x82), get(0xE0)
                if hi is None or lo is None or acc is None:
                    return None
                at = (((hi[0] << 8) | lo[0]) + acc[0]) & 65535
                if at not in self.code:
                    return None
                regs[0xE0] = (self.code[at], at)
            elif op == 0xA3:
                hi, lo = get(0x83), get(0x82)
                if hi is None or lo is None:
                    return None
                value = (((hi[0] << 8) | lo[0]) + 1) & 65535
                regs[0x83], regs[0x82] = (value >> 8, None), (value & 255, None)
            elif 0xF8 <= op <= 0xFF:
                regs[op & 7] = get(0xE0)
            elif 0xE8 <= op <= 0xEF:
                regs[0xE0] = get(op & 7)
            elif 0x78 <= op <= 0x7F:
                regs[op & 7] = (raw[1], None)
            elif op == 0xE0:
                regs[0xE0] = None  # External RAM contents are never constants.
            elif op == 0xE5:
                if raw[1] not in (*range(8), 0x82, 0x83, 0xE0, 0xF0):
                    return None
                regs[0xE0] = get(raw[1])
            elif op == 0xF5:
                if not put(raw[1], get(0xE0)):
                    return None
            elif 0x88 <= op <= 0x8F:
                if not put(raw[1], get(op & 7)):
                    return None
            elif op == 0xC0:
                stack.append(get(raw[1]))
            elif op == 0x12:
                stack.extend(((following & 255, ('return', following, 0)),
                              (following >> 8, ('return', following, 1))))
                peak = max(peak, len(stack))
                pc = int.from_bytes(raw[1:], 'big')
                continue
            elif op == 0x22:
                if len(stack) < 2:
                    return None
                high, low = stack.pop(), stack.pop()
                if high is None or low is None:
                    return None
                if (isinstance(low[1], tuple) and isinstance(high[1], tuple)
                        and low[1] == ('return', low[1][1], 0)
                        and high[1] == ('return', low[1][1], 1)):
                    pc = low[1][1]
                    continue
                if not (type(low[1]) is int and type(high[1]) is int and low[1] + 1 == high[1]
                        and len(stack) >= 2):
                    return None
                return_high, return_low = stack[-1], stack[-2]
                if (return_high is None or return_low is None
                        or not isinstance(return_low[1], tuple)
                        or return_low[1] != ('return', return_low[1][1], 0)
                        or return_high[1] != ('return', return_low[1][1], 1)):
                    return None
                return {'target': low[0] | high[0] << 8, 'rom_slot': low[1],
                        'continuation': return_low[1][1], 'height_at_callback': len(stack),
                        'height_after_return': len(stack) - 2, 'peak': peak,
                        'reachable': sorted(seen)}
            else:
                return None
            peak = max(peak, len(stack))
            pc = following
        return None

    def instruction(self, pc):
        """Decode missing library bodies from image bytes, rejecting overlapping entry."""
        if pc in self.owners and self.owners[pc] != pc:
            return None
        if pc in self.instructions:
            return self.instructions[pc]
        opcode = self.code.get(pc)
        if opcode is None or not OPCODE_LENGTHS[opcode]:
            return None
        size = OPCODE_LENGTHS[opcode]
        if any(pc+i not in self.code or (pc+i in self.owners and self.owners[pc+i] != pc)
               for i in range(size)):
            return None
        raw = bytes(self.code[pc+i] for i in range(size))
        self.instructions[pc] = raw
        self.owners.update((pc+i, pc) for i in range(size))
        self.decoded_from_image.add(pc)
        return raw

    def split_dispatch(self, pc):
        """Recognize one complete SDCC bounded split-table idiom, not a JMP alone.

        CLR C; MOV A,#max; SUBB A,iram; POP Rn; JNC in_range;
        LJMP default; MOV A,iram; MOV B,A; ADD A,#low_offset;
        MOVC A,@A+PC; MOV DPL,A; MOV A,B; ADD A,#high_offset;
        MOVC A,@A+PC; MOV DPH,A; CLR A; JMP @A+DPTR.
        Both outcomes are explored. Unknown entry into the idiom still fails at
        its indirect jump. Table data comes from the checksum-checked IHX.
        """
        lengths = (1,2,2,2,2,3,2,2,2,1,2,2,2,1,2,1,1)
        rows, at = [], pc
        for length in lengths:
            row = self.instructions.get(at)
            if row is None or len(row) != length:
                return None
            rows.append(row); at += length
        r = rows
        if not (r[0] == b'\xc3' and r[1][0] == 0x74 and r[2][0] == 0x95
                and r[2][1] < 0x80 and r[3][0] == 0xD0 and r[3][1] < 8
                and r[2][1] != r[3][1]
                and r[4] == b'\x50\x03' and r[5][0] == 2
                and r[6] == bytes((0xE5, r[2][1])) and r[7] == b'\xf5\xf0'
                and r[8][0] == 0x24 and r[9] == b'\x83' and r[10] == b'\xf5\x82'
                and r[11] == b'\xe5\xf0' and r[12][0] == 0x24
                and r[13] == b'\x83' and r[14] == b'\xf5\x83'
                and r[15] == b'\xe4' and r[16] == b'\x73'):
            return None
        maximum = r[1][1]
        if maximum + max(r[8][1], r[12][1]) > 255:
            return None
        low = pc + sum(lengths[:10]) + r[8][1]
        high = pc + sum(lengths[:14]) + r[12][1]
        if any(base + index not in self.code for base in (low, high) for index in range(maximum + 1)):
            return None
        targets = [int.from_bytes(r[5][1:], 'big')]
        targets += [self.code[low+i] | self.code[high+i] << 8 for i in range(maximum+1)]
        return targets

    def short_dispatch(self, pc):
        """MOV Rn,A / ADD #-N / JC default / MOV A,Rn / double / DPTR table."""
        lengths = (1,2,2,1,1,3,1)
        rows, at = [], pc
        for length in lengths:
            row = self.instructions.get(at)
            if row is None or len(row) != length:
                return None
            rows.append(row); at += length
        r = rows
        if not (0xF8 <= r[0][0] <= 0xFF and r[1][0] == 0x24
                and r[1][1] >= 128 and r[2][0] == 0x40
                and r[3] == bytes((0xE8 + (r[0][0] & 7),))
                and r[4] == bytes((0x28 + (r[0][0] & 7),))
                and r[5] == bytes((0x90, at >> 8, at & 255)) and r[6] == b'\x73'):
            return None
        count = 256 - r[1][1]
        targets = [pc + 5 + (r[2][1] if r[2][1] < 128 else r[2][1] - 256)]
        for index in range(count):
            target = at + 2 * index
            if self.instructions.get(target, b'')[:1] != b'\x80':
                return None
            targets.append(target)
        return targets

    def bound(self, entry):
        if entry in self.memo:
            return self.memo[entry]
        if entry in self.active:
            return {'bound': None, 'explored_peak': 0, 'unresolved': [{'pc': entry, 'reason': 'recursive call',
                'call_chain': self.active + [entry]}], 'reachable': []}
        if len(self.active) >= 128:
            return {'bound': None, 'explored_peak': 0, 'unresolved': [{'pc': entry,
                'reason': 'analysis call-depth limit reached'}], 'reachable': []}
        self.active.append(entry)
        work, heights, failures, maximum, transitive = [(entry, 0)], {}, [], 0, set()
        def fail(pc, reason):
            item = {'pc': pc, 'reason': reason}
            if item not in failures:
                failures.append(item)
        while work:
            pc, height = work.pop()
            maximum = max(maximum, height)
            if height < 0:
                fail(pc, 'stack underflow'); continue
            if height > 255:
                fail(pc, 'stack height exceeds 8051 address space'); continue
            if pc in heights:
                if heights[pc] != height:
                    fail(pc, 'inconsistent stack height or growing loop')
                continue
            heights[pc] = height
            raw = self.instruction(pc)
            if not raw:
                fail(pc, 'missing, reserved or overlapping image instruction'); continue
            pointer = self.rom_pointer_thunk(pc)
            if pointer is not None:
                child = self.bound(pointer['target'])
                maximum = max(maximum, height + pointer['peak'],
                              height + pointer['height_at_callback'] + child['explored_peak'])
                failures.extend(item for item in child['unresolved'] if item not in failures)
                transitive.update(pointer['reachable'])
                transitive.update(child['reachable'])
                self.pointer_transfers[pc] = pointer
                work.append((pointer['continuation'], height + pointer['height_after_return']))
                continue
            dispatch = self.split_dispatch(pc)
            if dispatch is not None:
                work.extend((target, height - 1) for target in dispatch)
                continue
            dispatch = self.short_dispatch(pc)
            if dispatch is not None:
                work.extend((target, height) for target in dispatch)
                continue
            op, following = raw[0], pc + len(raw)
            # All direct-byte destinations that can modify SP. MOV direct,direct
            # encodes source first. POP SP cannot be modeled as ordinary POP.
            destination = raw[2] if op == 0x85 else raw[1] if len(raw) > 1 and (
                op in (0x05, 0x15, 0x42, 0x43, 0x52, 0x53, 0x62, 0x63, 0x75, 0x86, 0x87, 0xC5, 0xD0, 0xD5, 0xF5)
                or 0x88 <= op <= 0x8F) else None
            if destination == 0x81 and op in (0x05, 0x15):
                height += 1 if op == 0x05 else -1
                maximum = max(maximum, height)
                work.append((following, height)); continue
            if destination == 0x81:
                fail(pc, 'explicit SP write needs ABI-specific proof'); continue
            if op == 0xA5:
                fail(pc, 'reserved opcode'); continue
            if op in (0x22, 0x32):
                if op == 0x32 or height:
                    fail(pc, 'RETI or unbalanced RET at ordinary function boundary')
                continue
            if op == 0x73:
                fail(pc, 'indirect jump/call dispatch has no proved target set'); continue
            if op == 0xC0:
                height += 1
            elif op == 0xD0:
                height -= 1
            maximum = max(maximum, height)
            if op in (0x02, 0x12) or op & 0x1F in (0x01, 0x11):
                target = int.from_bytes(raw[1:3], 'big') if op in (0x02, 0x12) else (
                    (following & 0xF800) | ((op & 0xE0) << 3) | raw[1])
                if op == 0x12 or op & 0x1F == 0x11:
                    child = self.bound(target)
                    transitive.update(child['reachable'])
                    maximum = max(maximum, height + 2 + child['explored_peak'])
                    failures.extend(item for item in child['unresolved'] if item not in failures)
                else:  # Tail transfers preserve the caller's current frame.
                    work.append((target, height)); continue
            elif op in (0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0xD5) or 0xB4 <= op <= 0xBF or 0xD8 <= op <= 0xDF:
                delta = raw[-1] if raw[-1] < 128 else raw[-1] - 256
                work.append((following + delta, height))
                if op == 0x80:
                    continue
            work.append((following, height))
        self.active.pop()
        result = {'bound': None if failures else maximum, 'explored_peak': maximum,
                  'unresolved': sorted(failures, key=lambda item: (item['pc'], item['reason'])),
                  'reachable': sorted(set(heights) | transitive)}
        self.memo[entry] = result
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    instructions, symbols, code, identity = load(args.build_dir)
    analyzer = Analyzer(instructions, code)
    roots = {}
    for name in ('_main', '_ak820_timer_irq', '_USB_DeviceInterrupt', '_ak820_led_irq'):
        roots[name] = analyzer.bound(symbols[name]) if name in symbols else {
            'bound': None, 'unresolved': [{'reason': 'root absent from MAP'}]}
    foreground = set(roots['_main'].get('reachable', []))
    intersections = {name: sorted(foreground.intersection(root.get('reachable', [])))
                     for name, root in roots.items() if name != '_main'}
    helpers = {name: analyzer.bound(symbols[name]) for name in (
        '___gptr_cmp', '___memcpy', '_memset', '__gptrput', '__mulint', '__gptrget', '__sdcc_call_dptr')
        if name in symbols}
    callback_tables = {}
    if '_rgb_matrix_driver' in symbols:
        base = symbols['_rgb_matrix_driver']
        entries = []
        for index, field in enumerate(('init', 'set_color', 'set_color_all', 'flush')):
            at = base + 2 * index
            if at not in code or at + 1 not in code:
                raise ValueError('Incomplete const RGB callback table')
            target = code[at] | code[at + 1] << 8
            entries.append({'field': field, 'slot': at, 'target': target,
                            'proved_ret_thunk_sites': sorted(pc for pc, thunk in analyzer.pointer_transfers.items()
                                                            if thunk['rom_slot'] == at),
                            'target_entry_analysis': analyzer.bound(target)})
        callback_tables['_rgb_matrix_driver'] = {'address': base, 'entries': entries,
            'caller_target_propagation_proved': False,
            'scope': 'Project-specific four-field const table inventory; no indirect transfer is approved from this inventory alone.'}
    report = {'schema': 1, 'identity': identity, 'roots': roots, 'whole_program_qualified': False,
        'runtime_helpers': helpers,
        'const_callback_tables': callback_tables,
        'proved_rom_pointer_thunks': analyzer.pointer_transfers,
        'analyzer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'decoder_source_sha256': hashlib.sha256((Path(__file__).resolve().parents[2] / 'util/ak820_linked_inventory.py').read_bytes()).hexdigest(),
        'image_decoded_instruction_addresses': sorted(analyzer.decoded_from_image),
        'observed_foreground_irq_instruction_intersections': intersections,
        'limits': ['Bounds exclude root entry return address; each direct call adds two bytes.',
                  'Explored peak is a partial observation, never an upper bound when unresolved paths exist.',
                  'No indirect target or reentrant-frame SP write is accepted without a separate proof.',
                  'No proof of data-pointer safety, shared static temporaries, overlay allocation or callee-save ABI.',
                  'ROM pointer-thunk tracking assumes the normal SDCC bank-0 calling convention; unknown instructions and values fail closed.',
                  'OEM wrappers and interrupt routing are outside this application-only instruction graph.',
                  'Conditional nesting budget: add 17 bytes per OEM wrapper plus callback bound; at most two priority levels is an unverified silicon assumption.',
                  'Boot/startup before main, stack capacity and actual hardware behavior remain separately unqualified.']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'roots': {name: {k: v for k, v in result.items() if k != 'reachable'} for name, result in roots.items()}, 'whole_program_qualified': False}, indent=2))
    return 2 if any(root['bound'] is None for root in roots.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
