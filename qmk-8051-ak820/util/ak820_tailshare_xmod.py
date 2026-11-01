#!/usr/bin/env python3
"""Experimental exact CROSS-MODULE RET suffix sharing; no added return frame.

Runs AFTER the per-module ak820_tailshare pass. Replaces byte-identical,
RET-terminated instruction suffixes that occur in several assembler modules
with an LJMP to one retained, globally exported copy. Unlike helper outlining
this adds no call/return frame and no stack bytes.

Safety rules (stricter than the per-module pass):
- identical source spelling of opcode+operands AND identical byte sizes;
- suffix bodies use only architectural registers, immediates, @a+dptr MOVC and
  relocations to symbols that are defined in exactly one module and exported
  with .globl there (so every reference resolves to the same address);
- no control SFRs/aliased direct RAM (same rules as ak820_tailshare);
- no local numeric labels, no SP/PSW/PC, hardware/IRQ modules stay excluded;
- a replaced range must not contain labels, directives or non-instruction
  lines: branch targets inside a shared suffix would be lost;
- one retained site per exact suffix, LJMP elsewhere (3 bytes, no page
  constraint; the later short-call pass may relax jumps where valid).
The pass never edits firmware sources; it rewrites a separate assembler tree.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import ak820_outline_audit as audit
import ak820_tailshare as ts

PREFIX = '_ak820_xtail_'
LABEL = re.compile(r'^\s*([A-Za-z_$][\w$]*)\s*:')
REGISTERS = {'a', 'b', 'c', 'ab', 'dpl', 'dph', 'dptr', 'sp', 'psw', 'pc'} | {f'r{i}' for i in range(8)}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect_symbols(modules, lines_by_module):
    """Return symbols defined in exactly one module and .globl-exported there."""
    definitions = {}  # name -> module (single definition enforced)
    exported = set()
    ambiguous = set()
    for module, lines in lines_by_module.items():
        declared = set()
        for line in lines:
            text = line.split(';', 1)[0].strip()
            m = re.fullmatch(r'\.globl\s+(\S+)', text)
            if m:
                declared.add(m[1])
                exported.add(m[1])
        for line in lines:
            text = line.split(';', 1)[0].strip()
            m = re.fullmatch(r'([A-Za-z_$][\w$]*)\s*=', text)
            if m:
                name = m[1]
            else:
                m = LABEL.match(line)
                if not m:
                    continue
                name = m[1]
            if name in definitions and definitions[name] != module:
                ambiguous.add(name)
            definitions.setdefault(name, module)
            if name in declared:
                exported.add(name)
    shared = {name for name, module in definitions.items()
              if name in exported and name not in ambiguous
              and definitions[name] == module}
    return shared, ambiguous, definitions


def eligible_suffix_blocks(assembly: Path, listing: Path, module: str):
    """RET-terminated eligible instruction blocks for one post-tailshare module.

    Mirrors ak820_tailshare.prepare eligibility; additionally records operand
    symbol names so cross-module identity can be verified against the global
    symbol table.
    """
    lines = assembly.read_text().splitlines(keepends=True)
    control_aliases = set()
    for line in lines:
        assignment = re.fullmatch(r'\s*([\w$]+)\s*=\s*(.*?)\s*(?:;.*)?', line.strip())
        if assignment and not re.fullmatch(r'0x[0-9a-fA-F]+|[0-9]+', assignment[2]):
            control_aliases.add(assignment[1])
        definition = re.fullmatch(r'\s*([\w$]+)\s*=\s*(0x[0-9a-fA-F]+|[0-9]+)\s*(?:;.*)?', line.strip())
        if definition:
            value = int(definition[2], 0)
            if 0x80 <= value <= 0xff and value not in {0x82, 0x83, 0xe0, 0xf0}:
                control_aliases.add(definition[1])
    byline = {}
    for line in listing.read_text().splitlines():
        match = audit.LISTED.match(line)
        if match:
            number = int(match[3]) - 1
            if number in byline or not 0 <= number < len(lines):
                raise ValueError('Ambiguous listing: ' + module)
            byline[number] = (int(match[1], 16),
                              bytes.fromhex(re.sub('[rstup*]', '', match[2])),
                              match[4].lower(),
                              re.sub(r'\s+', '', match[5].split(';', 1)[0]))
    blocks, block, area, function = [], [], '', ''
    previous_end = None
    for number, line in enumerate(lines):
        text = line.split(';', 1)[0].strip()
        fn = re.fullmatch(r';\s*function\s+(\w+)\s*', line.strip())
        if fn:
            function = fn[1]
            block = []
            previous_end = None
        if not text:
            continue
        if text.startswith('.area'):
            fields = text.split()
            if len(fields) < 2:
                raise ValueError('Malformed area: ' + module)
            area = fields[1]
        ins = byline.get(number)
        if ins:
            address, data, op, args = ins
            pieces = text.split(None, 1)
            if pieces[0].lower() != op or re.sub(r'\s+', '', pieces[1] if len(pieces) > 1 else '') != args:
                raise ValueError(f'ASM/listing mismatch {module}:{number+1}')
        valid = (ins is not None and function and area == 'CSEG'
                 and audit.eligible_module(module, function)
                 and not ts.EXCLUDED.search(module + ' ' + function))
        if valid:
            valid = (op in audit.SAFE_OPS | {'push', 'pop', 'ret'}
                     and not ts.FORBIDDEN.search(args)
                     and (op != 'movc' or args == 'a,@a+dptr')
                     and (op != 'ret' or not args))
        symbols = []
        if valid:
            for operand in args.split(','):
                if operand.startswith('#'):
                    continue
                names = set(re.findall(r'[A-Za-z_$][\w$]*', operand)) - REGISTERS
                if names & control_aliases:
                    valid = False
                symbols.extend(names)
                if re.fullmatch(r'(?:0x[0-9a-fA-F]+|[0-9]+)(?:\.[0-7])?', operand):
                    value = int(operand.split('.')[0], 0)
                    if 0x80 <= value <= 0xff and value not in {0x82, 0x83, 0xe0, 0xf0}:
                        valid = False
        if not valid:
            block = []
            previous_end = None
            continue
        if previous_end is not None and address != previous_end:
            raise ValueError('Noncontiguous listing: ' + module)
        item = {'line': number + 1, 'opcode': op, 'operands': args, 'bytes': data.hex(),
                'size': len(data), 'function': function, 'symbols': tuple(sorted(set(symbols)))}
        block.append(item)
        previous_end = address + len(data)
        if op == 'ret':
            blocks.append(block)
            block = []
            previous_end = None
    return blocks, lines


def prepare(source: Path, target: Path, report_path: Path):
    """Require fresh post-tailshare assembler listings; write a separate tree."""
    if target.exists():
        raise ValueError('Cross-module tail-share destination exists')
    modules = sorted(source.rglob('*.asm'))
    if not modules:
        raise ValueError('No assembler input')
    inputs, outputs = {}, {}
    all_blocks = {}
    lines_by_module = {}
    for assembly in modules:
        module = assembly.relative_to(source).as_posix()
        listing = assembly.with_suffix('.lst')
        if not listing.is_file():
            raise ValueError('Missing fresh listing: ' + module)
        if PREFIX in assembly.read_text():
            raise ValueError('Reserved cross-module tail-share symbol collision: ' + module)
        inputs[module] = {'asm_sha256': sha(assembly), 'lst_sha256': sha(listing)}
        lines_by_module[module] = assembly.read_text().splitlines(keepends=True)
        all_blocks[module] = eligible_suffix_blocks(assembly, listing, module)[0]
    shared, ambiguous, definitions = collect_symbols(modules, lines_by_module)

    matches = {}
    for module, blocks in all_blocks.items():
        lines = lines_by_module[module]
        for block in blocks:
            for count in range(2, len(block) + 1):
                seq = block[-count:]
                # Every relocatable symbol in every instruction must resolve
                # globally. Pure immediates/registers trivially pass.
                if not all(set(item['symbols']) <= shared for item in seq):
                    continue
                covered = {item['line'] - 1 for item in seq}
                span_ok = True
                for ln in range(seq[0]['line'] - 1, seq[-1]['line']):
                    if ln not in covered:
                        text = lines[ln].split(';', 1)[0].strip()
                        if text:
                            span_ok = False
                if not span_ok:
                    continue
                key = tuple((item['opcode'], item['operands'], item['size']) for item in seq)
                matches.setdefault(key, []).append({'module': module, 'seq': seq})
    choices = []
    for key, sites in matches.items():
        if len({s['module'] for s in sites}) < 2:
            continue
        size = sum(item['size'] for item in sites[0]['seq'])
        saving = (len(sites) - 1) * (size - 3)
        if len(sites) > 1 and saving > 0:
            choices.append((saving, size, key, sites))

    changes, groups = {}, []
    used = set()
    for saving, size, key, sites in sorted(choices, key=lambda c: (-c[0], -c[1], str(c[2]))):
        taken = [s for s in sites if not {(s['module'], i['line']) for i in s['seq']} & used]
        if len({s['module'] for s in taken}) < 2:
            continue
        used.update((s['module'], i['line']) for s in taken for i in s['seq'])
        name = PREFIX + str(len(groups)).zfill(5)
        retained = sorted(taken, key=lambda s: s['module'])[0]
        replacements = sorted(taken, key=lambda s: s['module'])[1:]
        insert_at = retained['seq'][0]['line'] - 1
        line_text = lines_by_module[retained['module']][insert_at]
        changes.setdefault(retained['module'], {})[insert_at] = (
            retained['seq'][0]['line'], None,
            f'\t.globl {name}\n{name} = .\n' + line_text)
        for site in replacements:
            start = site['seq'][0]['line'] - 1
            changes.setdefault(site['module'], {})[start] = (
                site['seq'][0]['line'], site['seq'][-1]['line'],
                f'\tljmp\t{name}\n')
        groups.append({'symbol': name, 'size': size, 'sites': len(taken),
                       'modules': sorted({s['module'] for s in taken}),
                       'replaced_sites': sorted([s['module'], s['seq'][0]['line']] for s in replacements),
                       'body': [f"{i['opcode']}\t{i['operands']}" for i in retained['seq']],
                       'retained': {'module': retained['module'], 'line': retained['seq'][0]['line']},
                       'estimated_object_saved_bytes': (len(taken) - 1) * (size - 3)})

    shutil.copytree(source, target, ignore=shutil.ignore_patterns('*.rel', '*.lst', '*.rst', '*.sym'))
    for assembly in modules:
        module = assembly.relative_to(source).as_posix()
        path = target / module
        if module in changes:
                edits = changes[module]
                lines = lines_by_module[module]
                result = []
                number = 0
                while number < len(lines):
                    if number in edits:
                        _, end_line, replacement = edits[number]
                        result.append(replacement)
                        number = end_line if end_line is not None else number + 1
                        continue
                    result.append(lines[number])
                    number += 1
                path.write_text(''.join(result))
        outputs[module] = sha(path)
    report = {'algorithm': 'experimental-exact-cross-module-ret-tail-v1',
              'extra_stack_bytes': 0,
              'shared_global_symbols': sorted(shared),
              'ambiguous_symbols_excluded': sorted(ambiguous),
              'inputs': inputs, 'outputs_sha256': outputs, 'groups': groups,
              'estimated_object_saved_bytes': sum(g['estimated_object_saved_bytes'] for g in groups),
              'linked_saved_bytes': None, 'hardware_validated': False}
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    return report


def verify_assembled(source: Path, target: Path, report_path: Path, report: dict):
    """Check fresh object area deltas; not a claim about linked gain."""
    def cseg_size(path):
        matches = re.findall(r'^A CSEG size ([0-9A-Fa-f]+) flags', path.read_text(), re.M)
        if len(matches) != 1:
            raise ValueError('Missing/ambiguous object CSEG: ' + str(path))
        return int(matches[0], 16)
    # Per-module expectation: each replaced site in that module saves
    # (size - 3); the retained module keeps its copy.
    per_module = {}
    for group in report['groups']:
        for site_module, _ in group['replaced_sites']:
            per_module[site_module] = per_module.get(site_module, 0) + group['size'] - 3
    measurements = {}
    for module, hashes in report['inputs'].items():
        original, rewritten = source / module, target / module
        if sha(original) != hashes['asm_sha256'] or sha(original.with_suffix('.lst')) != hashes['lst_sha256']:
            raise ValueError('Cross-module tail-share input changed: ' + module)
        if sha(rewritten) != report['outputs_sha256'][module]:
            raise ValueError('Cross-module tail-share output changed: ' + module)
        before, after = cseg_size(original.with_suffix('.rel')), cseg_size(rewritten.with_suffix('.rel'))
        if before - after != per_module.get(module, 0):
            raise ValueError('Unexpected cross-module tail-share object size: ' + module)
        measurements[module] = {'before_cseg_bytes': before, 'after_cseg_bytes': after,
                                'input_rel_sha256': sha(original.with_suffix('.rel')),
                                'output_rel_sha256': sha(rewritten.with_suffix('.rel'))}
    report['assembled_objects'] = measurements
    report['object_saved_bytes'] = sum(i['before_cseg_bytes'] - i['after_cseg_bytes'] for i in measurements.values())
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    return report
