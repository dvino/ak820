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


def private_guard_source_contract(text, variable):
    """Accept only the four literal uses of an unexposed private bool.

    Line splicing precedes C tokenization. Comments and string/character
    literals cannot create accepted identifier occurrences. Every identifier
    occurrence must belong to a complete whitelisted statement; parentheses,
    address taking, macro arguments and other uses fail closed.
    """
    text = re.sub(r'\\\r?\n', '', text)
    token = re.compile(r'''/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*' ''', re.S | re.X)
    code = token.sub(lambda match: ''.join('\n' if c == '\n' else ' ' for c in match[0]), text)
    name = re.escape(variable)
    allowed = (
        r'static\s+bool\s+' + name + r'\s*;',
        r'if\s*\(\s*' + name + r'\s*\)\s*return\s*;',
        name + r'\s*=\s*true\s*;',
        name + r'\s*=\s*false\s*;')
    spans = []
    for statement in allowed:
        matches = list(re.finditer(r'^\s*' + statement + r'\s*$', code, re.M))
        if len(matches) != 1:
            return False
        spans.append(matches[0].span())
    occurrences = list(re.finditer(r'\b' + name + r'\b', code))
    return len(occurrences) == 4 and all(
        any(start <= match.start() and match.end() <= end for start,end in spans)
        for match in occurrences)


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
    for path in sorted((build / 'dce').rglob('*.rst')):
        for address, name in re.findall(r'^\s*([0-9A-F]{6})\s+\d+\s+(_(?:dynamic_keymap_macro_send_sending_\w+|ak820_repeat_invoking|ak820_td_invoking)):', path.read_text(), re.M):
            symbols[name] = int(address,16)
    callback_spills = {}
    candidates = []
    for path in (build / 'dce').rglob('process_rgb.rst'):
        area = None
        lines = path.read_text().splitlines()
        for index, line in enumerate(lines):
            match = re.search(r'\.area\s+(\w+)', line)
            if match:
                area = match[1]
            match = re.match(r'^\s*([0-9A-F]{6})\s+\d+\s+(_process_rgb_action_\w+):\s*$', line)
            if match:
                allocation = re.match(r'^\s*([0-9A-F]{6})\s+\d+\s+\.ds\s+(\d+)\s*$',
                                      lines[index+1] if index+1 < len(lines) else '')
                candidates.append((path,area,match,allocation))
    if len(candidates) == 1:
        path, area, match, allocation = candidates[0]
        if area == 'XSEG' and allocation and allocation[1] == match[1] and allocation[2] == '1':
            callback_spills[int(match[1],16)] = {'symbol': match[2],
                'listing': str(path.relative_to(build)),
                'listing_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    return instructions, symbols, code, {'ihx_sha256': hashlib.sha256(image.read_bytes()).hexdigest(),
        'map_sha256': hashlib.sha256(mapping.read_bytes()).hexdigest(), 'listing_sha256': listings, 'compact_callback_spills': callback_spills}


class Analyzer:
    def __init__(self, instructions, code=None, callback_spills=()):
        self.callback_spills = frozenset(callback_spills)
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
        self.guarded_callback_transfers = {}
        self.guard_reads = {}
        self.guard_writes = {}

    def configure_guards(self, cells):
        """Private, address-unexposed C bool cells under valid-memory semantics.

        Reads must be the whole MOV DPTR/MOVX/JZ/RET early-return idiom.
        Only an exact immediate nonzero write establishes ownership. Any other
        direct reference drops the fact, so unproved stores cannot grant it.
        Aliasing/corruption is outside the same valid-memory premise as stack
        instruction analysis; callers must establish private object identity.
        """
        for pc, raw in list(self.instructions.items()):
            if raw[0] != 0x90:
                continue
            cell = int.from_bytes(raw[1:], 'big')
            if cell not in cells:
                continue
            a, b, c = (self.peek_instruction(pc + x) for x in (3,4,6))
            if a == b'\xe0' and b == b'\x60\x01' and c == b'\x22':
                self.guard_reads[pc] = (cell, pc + 6)
            elif a is not None and a[0] == 0x74 and self.peek_instruction(pc+5) == b'\xf0':
                self.guard_writes[pc] = (cell, bool(a[1]))
            else:
                self.guard_writes[pc] = (cell, False)


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
        while True:
            if pc in seen or len(stack) > 255:
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
            elif op == 0x73:
                low, high, acc = get(0x82), get(0x83), get(0xE0)
                if not (low is not None and high is not None and acc is not None and acc[0] == 0
                        and type(low[1]) is int and type(high[1]) is int and high[1] == low[1] + 1
                        and len(stack) >= 2):
                    return None
                return_low, return_high = stack[-2], stack[-1]
                if (return_low is None or return_high is None or not isinstance(return_low[1], tuple)
                        or return_low[1] != ('return', return_low[1][1], 0)
                        or return_high[1] != ('return', return_low[1][1], 1)):
                    return None
                return {'target': low[0] | high[0] << 8, 'rom_slot': low[1],
                        'continuation': return_low[1][1], 'height_at_callback': len(stack),
                        'height_after_return': len(stack) - 2, 'peak': peak,
                        'reachable': sorted(seen)}
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

    def guarded_pop_split_dispatch(self, pc):
        """Prove the complete byte guard, two POPs and PC-relative split table.

        Recognition starts only at CLR C. Neither a dispatch-body entry nor its
        JMP acquires the guard's range fact. POP destinations must be registers,
        preserving carry and the direct IRAM index until both MOVC reads.
        """
        lengths = (1,2,2,2,2,2,3,2,2,2,1,2,2,2,1,2,1,1)
        rows, addresses, at = [], [], pc
        for length in lengths:
            row = self.peek_instruction(at)
            if row is None or len(row) != length:
                return None
            rows.append(row); addresses.append(at); at += length
        r = rows
        if not (r[0] == b'\xc3' and r[1][0] == 0x74 and r[2][0] == 0x95
                and r[2][1] < 0x80
                and all(row[0] == 0xD0 and row[1] < 8 and row[1] != r[2][1]
                        for row in r[3:5])
                and r[5] == b'\x50\x03' and r[6][0] == 0x02
                and r[7] == bytes((0xE5, r[2][1])) and r[8] == b'\xf5\xf0'
                and r[9][0] == 0x24 and r[10] == b'\x83' and r[11] == b'\xf5\x82'
                and r[12] == b'\xe5\xf0' and r[13][0] == 0x24
                and r[14] == b'\x83' and r[15] == b'\xf5\x83'
                and r[16] == b'\xe4' and r[17] == b'\x73'):
            return None
        count = r[1][1] + 1
        if count - 1 + max(r[9][1], r[13][1]) > 255:
            return None
        low = addresses[10] + 1 + r[9][1]
        high = addresses[14] + 1 + r[13][1]
        # This idiom has adjacent low/high tables immediately after the JMP.
        if low != at or high != low + count:
            return None
        table_bytes = set(range(low, high + count))
        if any(slot not in self.code or slot in self.owners for slot in table_bytes):
            return None
        targets = [int.from_bytes(r[6][1:], 'big')] + [
            self.code[low+i] | self.code[high+i] << 8 for i in range(count)]
        if any(pc <= target < high + count or self.peek_instruction(target) is None
               for target in targets):
            return None
        return {'targets': targets, 'stack_delta': -2, 'reachable': addresses}

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

    def peek_instruction(self, pc):
        """Read a candidate idiom without claiming speculative instruction bytes."""
        if pc in self.owners and self.owners[pc] != pc:
            return None
        if pc in self.instructions:
            return self.instructions[pc]
        op = self.code.get(pc)
        if op is None or not OPCODE_LENGTHS[op]:
            return None
        size = OPCODE_LENGTHS[op]
        if any(pc+i not in self.code or (pc+i in self.owners and self.owners[pc+i] != pc)
               for i in range(size)):
            return None
        return bytes(self.code[pc+i] for i in range(size))

    def range16_dispatch(self, pc):
        """Complete unsigned 16-bit lower/upper guard and normalized split table."""
        lengths = (1,1,2,1,2,2,3,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,1)
        rows, addresses, at = [], [], pc
        for length in lengths:
            row = self.peek_instruction(at)
            if row is None or len(row) != length:
                return None
            rows.append(row); addresses.append(at); at += length
        r = rows
        lo, hi = r[1][0] & 7, r[3][0] & 7
        if not (r[0] == r[7] == b'\xc3' and 0xE8 <= r[1][0] <= 0xEF
                and 0xE8 <= r[3][0] <= 0xEF and lo != hi
                and r[2][0] == r[4][0] == 0x94 and r[5] == b'\x50\x03'
                and r[6][0] == 0x02 and r[8][0] == r[10][0] == 0x74
                and r[9] == bytes((0x98 + lo,)) and r[11] == bytes((0x98 + hi,))
                and r[12][0] == 0x40 and r[4][1] == r[10][1]
                and r[2][1] <= r[8][1] and r[13] == r[19] == r[1]
                and r[14] == bytes((0x24, (-r[2][1]) & 255))
                and r[15] == bytes((0xF8 + lo,)) and r[16][0] == r[20][0] == 0x24
                and r[17] == r[21] == b'\x83' and r[18] == b'\xf5\x82'
                and r[22] == b'\xf5\x83' and r[23] == b'\xe4' and r[24] == b'\x73'):
            return None
        count = r[8][1] - r[2][1] + 1
        if count - 1 + max(r[16][1], r[20][1]) > 255:
            return None
        low, high = addresses[17] + 1 + r[16][1], addresses[21] + 1 + r[20][1]
        if any(base+i not in self.code for base in (low, high) for i in range(count)):
            return None
        delta = r[12][1] if r[12][1] < 128 else r[12][1] - 256
        return [int.from_bytes(r[6][1:], 'big'), addresses[13] + delta] + [
            self.code[low+i] | self.code[high+i] << 8 for i in range(count)]

    def register_helper_dispatch(self, pc):
        """Exact leaf MOVX getter proves equal A/Rn at the following guard."""
        call = self.peek_instruction(pc)
        if call is None or call[0] != 0x12:
            return None
        at = int.from_bytes(call[1:], 'big')
        rows, seen = [], set()
        for length in (3, 1, 1, 1):
            row = self.peek_instruction(at)
            if row is None or len(row) != length:
                return None
            rows.append(row); seen.add(at); at += length
        if not (rows[0][0] == 0x90 and rows[1] == b'\xe0'
                and 0xF8 <= rows[2][0] <= 0xFF and rows[3] == b'\x22'):
            return None
        targets = self.register_dispatch(pc + 3, rows[2][0] & 7)
        return None if targets is None else (targets, seen)

    def masked_helper_dispatch(self, pc):
        """Prove a leaf accumulator helper followed by an adjacent SJMP table."""
        call = self.peek_instruction(pc)
        if call is None or call[0] != 0x12:
            return None
        helper = int.from_bytes(call[1:], 'big')
        values, seen, at = set(range(256)), set(), helper
        while True:
            if at in seen:
                return None
            seen.add(at)
            raw = self.peek_instruction(at)
            if raw is None:
                return None
            if raw[0] == 0x22:
                break
            if raw[0] == 0x90:  # DPTR changes do not alter the accumulator.
                pass
            elif raw[0] == 0xE0:
                values = set(range(256))
            elif raw[0] == 0x03:
                values = {(v >> 1) | ((v & 1) << 7) for v in values}
            elif raw[0] == 0x54:
                values = {v & raw[1] for v in values}
            else:
                return None
            at += len(raw)
        rows, at = [], pc + 3
        for length in (1, 1, 3, 1):
            raw = self.peek_instruction(at)
            if raw is None or len(raw) != length:
                return None
            rows.append(raw); at += length
        r = rows
        if not (0xF8 <= r[0][0] <= 0xFF and r[1] == bytes((0x28 + (r[0][0] & 7),))
                and r[2] == bytes((0x90, at >> 8, at & 255)) and r[3] == b'\x73'):
            return None
        targets = [at + ((2 * v) & 255) for v in sorted(values)]
        if any(self.peek_instruction(t) is None or self.peek_instruction(t)[0] != 0x80 for t in targets):
            return None
        return targets, seen

    def masked_bit_dispatch(self, pc):
        """ANL A,#mask; save index; triple; dispatch to CLR bit/RET slots."""
        rows, at = [], pc
        for length in (2, 1, 1, 1, 3, 1):
            row = self.peek_instruction(at)
            if row is None or len(row) != length:
                return None
            rows.append(row); at += length
        r = rows
        if not (r[0][0] == 0x54 and 0xF8 <= r[1][0] <= 0xFF
                and r[2] == r[3] == bytes((0x28 + (r[1][0] & 7),))
                and r[4] == bytes((0x90, at >> 8, at & 255)) and r[5] == b'\x73'):
            return None
        # Enumerate actual eight-bit arithmetic, including multiplication wrap.
        indices = {value & r[0][1] for value in range(256)}
        targets = [at + (3 * index & 255) for index in sorted(indices)]
        for target in targets:
            clear, ret = self.peek_instruction(target), self.peek_instruction(target + 2)
            if clear is None or clear[0] != 0xC2 or ret != b'\x22':
                return None
        return targets

    def register_dispatch(self, pc, proven_reg=None):
        """Prove a finite register-index table from its complete carry guard.

        ADD A,#-count sets carry exactly for index >= count. The saved
        register must still contain that same index when the table is read.
        No calls or unmodelled writes may intervene in this sequence.
        """
        first = self.peek_instruction(pc)
        if proven_reg is None:
            if not first or not (0xE8 <= first[0] <= 0xEF or 0xF8 <= first[0] <= 0xFF):
                return None
            reg, guard_start = first[0] & 7, pc + 1
        else:
            reg, guard_start = proven_reg, pc
        add, guard = self.peek_instruction(guard_start), self.peek_instruction(guard_start + 2)
        if not add or add[0] != 0x24 or add[1] < 128 or not guard or guard[0] not in (0x40, 0x50):
            return None
        count = 256 - add[1]
        delta = guard[1] if guard[1] < 128 else guard[1] - 256
        taken, fall = guard_start + 4 + delta, guard_start + 4
        dispatch, default = (fall, taken) if guard[0] == 0x40 else (taken, fall)
        # The contiguous table recognizer starts only at the in-range arm.
        at = dispatch
        rows = []
        for length in (1, 2, 1, 2, 1, 2, 1, 2, 1, 1):
            row = self.peek_instruction(at)
            if row is None or len(row) != length:
                break
            rows.append(row); at += length
        r = rows
        if (len(r) == 10 and r[0] == bytes((0xE8 + reg,))
                and r[1][0] == 0x24 and r[2] == b'\x83' and r[3] == b'\xf5\x82'
                and r[4] == r[0] and r[5][0] == 0x24 and r[6] == b'\x83'
                and r[7] == b'\xf5\x83' and r[8] == b'\xe4' and r[9] == b'\x73'):
            if count - 1 + max(r[1][1], r[5][1]) > 255:
                return None
            low, high = dispatch + 4 + r[1][1], dispatch + 10 + r[5][1]
            if any(base + i not in self.code for base in (low, high) for i in range(count)):
                return None
            return [default] + [self.code[low+i] | self.code[high+i] << 8 for i in range(count)]
        # Three-byte slots: A = index + index + index. A final slot may
        # start its case body directly; each selected entry is analyzed normally.
        rows, at = [], dispatch
        for length in (1, 1, 1, 3, 1):
            row = self.peek_instruction(at)
            if row is None or len(row) != length:
                return None
            rows.append(row); at += length
        if not (rows[0] == bytes((0xE8 + reg,))
                and rows[1] == rows[2] == bytes((0x28 + reg,))
                and rows[3] == bytes((0x90, at >> 8, at & 255)) and rows[4] == b'\x73'
                and 3 * (count - 1) <= 255):
            return None
        targets = [at + 3 * i for i in range(count)]
        if any(self.peek_instruction(target) is None for target in targets):
            return None
        return [default] + targets

    def guarded_rom_callback_dispatch(self, pc):
        """Unsigned 16-bit range, normalized byte/XOR, ROM function pointer.

        All register identities, carry flow, both branch destinations, local
        spill/reload, multiply, ROM getter and call helper must match. The
        callback's LCALL frame and two saved registers stay live.
        """
        lengths = (2,2,1,1,2,1,2,2,2,1,2,1,2,1,2,1,3,1,1,2,3,2,1,1,3,1,3,1,2,2,2,2,2,3,2,2)
        r, addresses, at = [], [], pc
        for length in lengths:
            raw = self.peek_instruction(at)
            if raw is None or len(raw) != length:
                return None
            r.append(raw); addresses.append(at); at += length
        if not (r[0] == b'\x8d\x03' and r[1] == b'\x8e\x04' and r[2] == b'\xc3'
                and r[3] == b'\xeb' and r[4][0] == 0x94 and r[5] == b'\xec'
                and r[6][0] == 0x94 and r[7][0] == 0x40 and r[8][0] == 0x74
                and r[9] == b'\x9b' and r[10] == bytes((0x74,r[6][1]))
                and r[11] == b'\x9c' and r[12][0] == 0x40
                and r[13] == b'\xed' and r[14] == bytes((0x24,(-r[4][1])&255))
                and r[15] == b'\xfd' and r[16][0] == 0x90 and r[17] == b'\xf0'
                and r[18] == b'\xef' and r[19] == b'\x60\x07' and r[20] == r[16]
                and r[21] == b'\x74\x01' and r[22] == b'\x6d' and r[23] == b'\xf0'
                and r[24] == r[16] and r[25] == b'\xe0' and r[26] == b'\x75\xf0\x02'
                and r[27] == b'\xa4' and r[28][0] == 0x24 and r[29] == b'\xf5\x82'
                and r[30][0] == 0x74 and r[31] == b'\x35\xf0' and r[32] == b'\xf5\x83'
                and r[33][0] == 0x12 and r[34] == b'\xc0\x07' and r[35] == b'\xc0\x06'):
            return None
        # Final two LCALLs are read separately so their complete helper bodies
        # can be checked without relying on symbol names.
        set_dptr, invoke = self.peek_instruction(at), self.peek_instruction(at+3)
        if not set_dptr or set_dptr[0] != 0x12 or not invoke or invoke[0] != 0x12:
            return None
        low, high = r[4][1], r[8][1]
        if low > high:
            return None
        def relative(index):
            value = r[index][-1]
            return addresses[index] + len(r[index]) + (value if value < 128 else value-256)
        if relative(7) != relative(12) or relative(19) != addresses[24]:
            return None
        helper_reachable = set()
        def body(call, expected):
            entry = int.from_bytes(call[1:], 'big')
            offset = 0
            while offset < len(expected):
                row = self.peek_instruction(entry+offset)
                if row is None or row != expected[offset:offset+len(row)]:
                    return False
                helper_reachable.add(entry+offset)
                offset += len(row)
            return offset == len(expected)
        if not (body(r[33], b'\xe4\x93\xfe\xa3\xe4\x93\xff\x22')
                and body(set_dptr,b'\x8e\x82\x8f\x83\x22')
                and body(invoke,b'\xe4\x73')):
            return None
        base = r[28][1] | r[30][1] << 8
        indices = {index ^ shift for index in range(high-low+1) for shift in (0,1)}
        slots = [base + 2*index for index in sorted(indices)]
        if any(slot+1 > 65535 or slot not in self.code or slot+1 not in self.code for slot in slots):
            return None
        return {'targets': sorted({self.code[slot] | self.code[slot+1]<<8 for slot in slots}),
                'default': relative(7), 'continuation': at+6, 'rom_slots': slots,
                'reachable': sorted(set(addresses + [at,at+3]) | helper_reachable)}

    def compact_rom_callback_dispatch(self, pc):
        """Byte normalization, nonzero/range guards and outlined ROM callback.

        The modifier getter may only read RAM and alter A, R7 and DPTR. Its
        complete straight-line call tree is checked, including balanced R7
        saves, so the saved index and private spill cannot be changed.
        """
        lengths = (1,2,1,2,3,2,1,2,2,1,2,1,3,1,3,2,2,2,3,2,1,1,
                   3,1,3,1,2,2,2,3,1,1,1,1,1,2,2,3,3)
        r, addresses, at = [], [], pc
        multiply_call = None
        for index, length in enumerate(lengths):
            # The exact outliner may replace MOV B,#2 / MUL AB with one
            # LCALL. Keep logical row numbers stable; prove its complete body
            # below before granting any callback targets.
            if index == 25 and multiply_call is not None:
                r.append(b'\xa4'); addresses.append(addresses[-1])
                continue
            row = self.peek_instruction(at)
            if index == 24 and row is not None and row[0] == 0x12:
                multiply_call = row
                r.append(b'\x75\xf0\x02'); addresses.append(at)
                at += len(row)
                continue
            if row is None or len(row) != length:
                return None
            r.append(row); addresses.append(at); at += length
        def relative(i):
            delta = r[i][-1]
            return addresses[i]+len(r[i])+(delta if delta < 128 else delta-256)
        if not (r[0] == b'\xed' and r[1][0] == 0x24 and r[2] == b'\xff'
                and r[3] == b'\x70\x05' and r[4][0] == 0x12 and r[5][0] == 0x80
                and relative(3) == addresses[6] and r[6] == b'\xef'
                and r[7][0] == 0x24 and r[7][1] >= 128 and r[8][0] == 0x40
                and r[9] == b'\xed' and r[10] == bytes((0x24,(r[1][1]-1)&255))
                and r[11] == b'\xfe' and r[12][0] == 0x90 and r[13] == b'\xf0'
                and r[14][0] == 0x12 and r[15] == b'\xe5\x82' and r[16][0] == 0x54
                and r[17] == b'\x60\x07' and r[18] == r[12] and r[19] == b'\x74\x01'
                and r[20] == b'\x6e' and r[21] == b'\xf0' and r[22] == r[12]
                and relative(17) == addresses[22] and r[23] == b'\xe0'
                and r[24] == b'\x75\xf0\x02' and r[25] == b'\xa4'
                and r[26][0] == 0x24 and r[27] == b'\xf5\x82' and r[28][0] == 0x74
                and r[29][0] == 0x12 and r[30] == b'\xfd' and r[31] == b'\xa3'
                and r[32] == b'\xe4' and r[33] == b'\x93' and r[34] == b'\xfe'
                and r[35] == b'\xc0\x06' and r[36] == b'\xc0\x05'
                and r[37][0] == r[38][0] == 0x12):
            return None
        spill = int.from_bytes(r[12][1:], 'big')
        if spill not in self.callback_spills:
            return None
        seen, active = set(), set()
        def getter(entry):
            if entry in active:
                return None
            active.add(entry)
            cursor, height, peak = entry, 0, 0
            local = set()
            while cursor not in local:
                local.add(cursor); seen.add(cursor)
                row = self.peek_instruction(cursor)
                if row is None:
                    break
                if row == b'\x22':
                    active.remove(entry)
                    return peak if height == 0 else None
                if row[0] == 0x12:
                    child = getter(int.from_bytes(row[1:], 'big'))
                    if child is None:
                        break
                    peak = max(peak,height+2+child)
                elif row == b'\xc0\x07':
                    height += 1
                elif row == b'\xd0\x07':
                    height -= 1
                    if height < 0:
                        break
                elif not (row[0] == 0x90 or row in (b'\xe0',b'\xff',b'\xef',b'\x4f',b'\x42\x07',b'\x8f\x82',b'\xf5\x82')):
                    break
                peak = max(peak,height)
                cursor += len(row)
            active.remove(entry)
            return None
        getter_peak = getter(int.from_bytes(r[14][1:], 'big'))
        def body(call, expected):
            cursor = int.from_bytes(call[1:], 'big')
            offset = 0
            while offset < len(expected):
                row = self.peek_instruction(cursor+offset)
                if row is None or row != expected[offset:offset+len(row)]:
                    return False
                seen.add(cursor+offset); offset += len(row)
            return offset == len(expected)
        if (multiply_call is not None and not body(multiply_call, b'\x75\xf0\x02\xa4\x22')):
            return None
        if (getter_peak is None or not body(r[29], b'\x35\xf0\xf5\x83\xe4\x93\x22')
                or not body(r[37], b'\x8d\x82\x8e\x83\x22')
                or not body(r[38], b'\xe4\x73')):
            return None
        # Nonzero normalized action and carry guard prove 1..count-1.
        count = 256-r[7][1]
        indices = {index ^ shift for index in range(count-1) for shift in (0,1)}
        base = r[26][1] | r[28][1] << 8
        slots = [base+2*i for i in sorted(indices)]
        if any(slot+1 > 65535 or slot not in self.code or slot+1 not in self.code for slot in slots):
            return None
        return {'targets': sorted({self.code[slot] | self.code[slot+1]<<8 for slot in slots}),
                'default': relative(8), 'continuation': at, 'rom_slots': slots,
                'direct_target': int.from_bytes(r[4][1:], 'big'), 'direct_continuation': relative(5),
                'getter_peak': getter_peak, 'multiply_peak': 2 if multiply_call is not None else 0, 'spill': spill, 'reachable': sorted(set(addresses)|seen)}

    def bound(self, entry, context=frozenset()):
        key = (entry, context)
        if key in self.memo:
            return self.memo[key]
        if key in self.active:
            return {'bound': None, 'explored_peak': 0, 'unresolved': [{'pc': entry, 'reason': 'recursive call',
                'call_chain': [frame[0] for frame in self.active] + [entry]}], 'reachable': []}
        self.active.append(key)
        work, heights, failures, maximum, transitive = [(entry, 0, context)], {}, [], 0, set()
        def fail(pc, reason):
            item = {'pc': pc, 'reason': reason}
            if item not in failures:
                failures.append(item)
        while work:
            pc, height, flags = work.pop()
            maximum = max(maximum, height)
            if height < 0:
                fail(pc, 'stack underflow'); continue
            if height > 255:
                fail(pc, 'stack height exceeds 8051 address space'); continue
            state = (pc, flags)
            if state in heights:
                if heights[state] != height:
                    fail(pc, 'inconsistent stack height or growing loop')
                continue
            heights[state] = height
            raw = self.instruction(pc)
            if not raw:
                fail(pc, 'missing, reserved or overlapping image instruction'); continue
            if pc in self.guard_reads and self.guard_reads[pc][0] in flags:
                transitive.update((pc+3,pc+4))
                work.append((self.guard_reads[pc][1], height, flags))
                continue
            if pc in self.guard_writes:
                cell, owned = self.guard_writes[pc]
                flags = flags | {cell} if owned else flags - {cell}
            callback_dispatch = self.guarded_rom_callback_dispatch(pc)
            if callback_dispatch is not None:
                self.guarded_callback_transfers[pc] = callback_dispatch
                work.append((callback_dispatch['default'], height, flags))
                work.append((callback_dispatch['continuation'], height + 2, flags))
                transitive.update(callback_dispatch['reachable'])
                for target in callback_dispatch['targets']:
                    child = self.bound(target, flags)
                    maximum = max(maximum, height + 4 + child['explored_peak'])
                    transitive.update(child['reachable'])
                    failures.extend(item for item in child['unresolved'] if item not in failures)
                continue
            compact = self.compact_rom_callback_dispatch(pc)
            if compact is not None:
                self.guarded_callback_transfers[pc] = compact
                transitive.update(compact['reachable'])
                maximum = max(maximum, height + 2 + compact['getter_peak'],
                              height + compact['multiply_peak'], height + 4)
                work.append((compact['default'], height, flags))
                work.append((compact['continuation'], height + 2, flags))
                work.append((compact['direct_continuation'], height, flags))
                for target, frame in [(compact['direct_target'],2)] + [(t,4) for t in compact['targets']]:
                    child = self.bound(target, flags)
                    maximum = max(maximum,height+frame+child['explored_peak'])
                    transitive.update(child['reachable'])
                    failures.extend(item for item in child['unresolved'] if item not in failures)
                continue
            pointer = self.rom_pointer_thunk(pc)
            if pointer is not None:
                child = self.bound(pointer['target'], flags)
                maximum = max(maximum, height + pointer['peak'],
                              height + pointer['height_at_callback'] + child['explored_peak'])
                failures.extend(item for item in child['unresolved'] if item not in failures)
                transitive.update(pointer['reachable'])
                transitive.update(child['reachable'])
                self.pointer_transfers[pc] = pointer
                work.append((pointer['continuation'], height + pointer['height_after_return'], flags))
                continue
            pop_split = self.guarded_pop_split_dispatch(pc)
            if pop_split is not None:
                transitive.update(pop_split['reachable'])
                work.extend((target, height + pop_split['stack_delta'], flags)
                            for target in pop_split['targets'])
                continue
            dispatch = self.split_dispatch(pc)
            if dispatch is not None:
                work.extend((target, height - 1, flags) for target in dispatch)
                continue
            helper_dispatch = self.register_helper_dispatch(pc)
            if helper_dispatch is None:
                helper_dispatch = self.masked_helper_dispatch(pc)
            if helper_dispatch is not None:
                targets, helper_seen = helper_dispatch
                maximum = max(maximum, height + 2)
                transitive.update(helper_seen)
                work.extend((target, height, flags) for target in targets)
                continue
            dispatch = self.range16_dispatch(pc)
            if dispatch is not None:
                work.extend((target, height, flags) for target in dispatch)
                continue
            dispatch = self.masked_bit_dispatch(pc)
            if dispatch is not None:
                work.extend((target, height, flags) for target in dispatch)
                continue
            dispatch = self.register_dispatch(pc)
            if dispatch is not None:
                work.extend((target, height, flags) for target in dispatch)
                continue
            dispatch = self.short_dispatch(pc)
            if dispatch is not None:
                work.extend((target, height, flags) for target in dispatch)
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
                work.append((following, height, flags)); continue
            if destination == 0x81:
                fail(pc, 'explicit SP write needs ABI-specific proof'); continue
            if op == 0xA5:
                fail(pc, 'reserved opcode'); continue
            if op in (0x22, 0x32):
                if not context.issubset(flags):
                    fail(pc, 'callee does not preserve incoming guard ownership')
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
                    child = self.bound(target, flags)
                    transitive.update(child['reachable'])
                    maximum = max(maximum, height + 2 + child['explored_peak'])
                    failures.extend(item for item in child['unresolved'] if item not in failures)
                else:  # Tail transfers preserve the caller's current frame.
                    work.append((target, height, flags)); continue
            elif op in (0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0xD5) or 0xB4 <= op <= 0xBF or 0xD8 <= op <= 0xDF:
                delta = raw[-1] if raw[-1] < 128 else raw[-1] - 256
                work.append((following + delta, height, flags))
                if op == 0x80:
                    continue
            work.append((following, height, flags))
        self.active.pop()
        result = {'bound': None if failures else maximum, 'explored_peak': maximum,
                  'unresolved': sorted(failures, key=lambda item: (item['pc'], item['reason'])),
                  'reachable': sorted({state[0] for state in heights} | transitive)}
        self.memo[key] = result
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    instructions, symbols, code, identity = load(args.build_dir)
    analyzer = Analyzer(instructions, code, identity['compact_callback_spills'])
    private_guards = {}
    source_root = Path(__file__).resolve().parents[2]
    for prefix, source, declaration in (
            ('_dynamic_keymap_macro_send_sending_', 'quantum/dynamic_keymap.c', 'static bool sending;'),
            ('_ak820_repeat_invoking', 'quantum/repeat_key.c', 'static bool ak820_repeat_invoking;'),
            ('_ak820_td_invoking', 'keyboards/ajazz/ak820/ak820_tap_dance.c', 'static bool ak820_td_invoking;')):
        path = source_root / source
        text = path.read_text()
        variable = declaration.split()[-1].rstrip(';')
        # Address-unexposed private objects are disjoint from valid pointer
        # accesses to other C objects. Do not silently assume an escaped cell.
        if not private_guard_source_contract(text, variable):
            raise ValueError('Private guard object declaration/address contract changed: ' + source)
        for name, address in symbols.items():
            if name.startswith(prefix):
                private_guards[address] = {'symbol': name, 'source': source,
                    'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    analyzer.configure_guards(private_guards)
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
        'proved_guarded_rom_callbacks': analyzer.guarded_callback_transfers,
        'private_guard_objects': private_guards,
        'private_guard_reads': analyzer.guard_reads,
        'private_guard_writes': analyzer.guard_writes,
        'analyzer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'decoder_source_sha256': hashlib.sha256((Path(__file__).resolve().parents[2] / 'util/ak820_linked_inventory.py').read_bytes()).hexdigest(),
        'image_decoded_instruction_addresses': sorted(analyzer.decoded_from_image),
        'observed_foreground_irq_instruction_intersections': intersections,
        'limits': ['Bounds exclude root entry return address; each direct call adds two bytes.',
                  'Explored peak is a partial observation, never an upper bound when unresolved paths exist.',
                  'No indirect target or reentrant-frame SP write is accepted without a separate proof.',
                  'No proof of data-pointer safety, shared static temporaries, overlay allocation or callee-save ABI.',
                  'ROM pointer-thunk tracking assumes the normal SDCC bank-0 calling convention; unknown instructions and values fail closed.',
                  'Compact callbacks require the identified one-byte XSEG process_rgb action allocation, no address escape and no concurrent clobber; IRQ storage disjointness needs separate evidence.',
                  'Guard contexts require private C bool objects whose addresses do not escape, valid memory accesses and the usual compiler object layout; arbitrary aliasing/corruption is not proved safe.',
                  'OEM wrappers and interrupt routing are outside this application-only instruction graph.',
                  'Interrupt wrapper frames and nesting require the separate exact-image all-three-source IRQ contract; no priority-count limit is assumed here.',
                  'Boot/startup before main, stack capacity and actual hardware behavior remain separately unqualified.']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'roots': {name: {k: v for k, v in result.items() if k != 'reachable'} for name, result in roots.items()}, 'whole_program_qualified': False}, indent=2))
    return 2 if any(root['bound'] is None for root in roots.values()) else 0


if __name__ == '__main__':
    raise SystemExit(main())
