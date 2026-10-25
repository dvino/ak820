#!/usr/bin/env python3
"""Experimental exact per-module RET suffix sharing; no added return frame."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import ak820_outline_audit as audit

PREFIX = '_ak820_tailshare_'
FORBIDDEN = re.compile(r'(?<![\w])_?(?:sp|psw|pc)(?![\w])|\b\d+\$|(?<![\w.])\.(?![\w.])', re.I)
EXCLUDED = re.compile(r'(?:ch555|usb|irq|interrupt|flash|nvm|eeprom|boot|iap|timer|board|rgb)', re.I)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(source: Path, target: Path, report_path: Path):
    """Require fresh assembler listings, write a separate tree and exact audit."""
    if target.exists():
        raise ValueError('Tail-share destination exists')
    modules = sorted(source.rglob('*.asm'))
    if not modules:
        raise ValueError('No assembler input')
    changes, inputs, outputs, groups = {}, {}, {}, []
    for assembly in modules:
        module = assembly.relative_to(source).as_posix()
        listing = assembly.with_suffix('.lst')
        lines = assembly.read_text().splitlines(keepends=True)
        if not listing.is_file():
            raise ValueError('Missing fresh listing: ' + module)
        if PREFIX in ''.join(lines):
            raise ValueError('Reserved tail-share symbol collision: ' + module)
        inputs[module] = {'asm_sha256': sha(assembly), 'lst_sha256': sha(listing)}
        # SFR aliases are absolute assembler definitions. Only ordinary data
        # registers may appear; control SFRs (including aliased SP/PSW) cannot.
        control_aliases = set()
        for line in lines:
            assignment = re.fullmatch(r'\s*([\w$]+)\s*=\s*(.*?)\s*(?:;.*)?', line.strip())
            if assignment and not re.fullmatch(r'0x[0-9a-fA-F]+|[0-9]+', assignment[2]):
                control_aliases.add(assignment[1])
            definition = re.fullmatch(r'\s*([\w$]+)\s*=\s*(0x[0-9a-fA-F]+|[0-9]+)\s*(?:;.*)?', line.strip())
            if definition:
                value = int(definition[2], 0)
                if 0x80 <= value <= 0xff and value not in {0x82,0x83,0xe0,0xf0}:
                    control_aliases.add(definition[1])
        byline = {}
        for line in listing.read_text().splitlines():
            match = audit.LISTED.match(line)
            if match:
                number = int(match[3])-1
                if number in byline or not 0 <= number < len(lines):
                    raise ValueError('Ambiguous listing: ' + module)
                byline[number] = (int(match[1],16), bytes.fromhex(re.sub('[rstup*]', '', match[2])), match[4].lower(), re.sub(r'\s+', '', match[5].split(';',1)[0]))
        blocks, block, area, function = [], [], '', ''
        previous_end = None
        for number, line in enumerate(lines):
            text = line.split(';',1)[0].strip()
            fn = re.fullmatch(r';\s*function\s+(\w+)\s*', line.strip())
            if fn:
                function = fn[1]
                block = []; previous_end = None
            if not text:
                continue
            if text.startswith('.area'):
                fields = text.split()
                if len(fields)<2:
                    raise ValueError('Malformed area: '+module)
                area = fields[1]
            ins = byline.get(number)
            if ins:
                address, data, op, args = ins
                pieces = text.split(None,1)
                if pieces[0].lower()!=op or re.sub(r'\s+','',pieces[1] if len(pieces)>1 else '')!=args:
                    raise ValueError(f'ASM/listing mismatch {module}:{number+1}')
            valid = (ins is not None and function and area=='CSEG'
                     and audit.eligible_module(module,function)
                     and not EXCLUDED.search(module+' '+function))
            if valid:
                valid = (op in audit.SAFE_OPS | {'push','pop','ret'} and not FORBIDDEN.search(args)
                         and (op!='movc' or args=='a,@a+dptr') and (op!='ret' or not args))
            if valid:
                for operand in args.split(','):
                    if operand.startswith('#'):
                        continue
                    names = set(re.findall(r'[A-Za-z_$][\w$]*', operand))
                    if names & control_aliases:
                        valid = False
                    if re.fullmatch(r'(?:0x[0-9a-fA-F]+|[0-9]+)(?:\.[0-7])?', operand):
                        value = int(operand.split('.')[0], 0)
                        if 0x80 <= value <= 0xff and value not in {0x82,0x83,0xe0,0xf0}:
                            valid = False
            if not valid:
                block=[]; previous_end=None; continue
            if previous_end is not None and address != previous_end:
                raise ValueError('Noncontiguous listing: '+module)
            item = {'line':number+1,'opcode':op,'operands':args,'bytes':data.hex(),'size':len(data),'function':function}
            block.append(item); previous_end=address+len(data)
            if op=='ret':
                blocks.append(block); block=[]; previous_end=None
        matches = {}
        for block in blocks:
            for count in range(2,len(block)+1):
                seq=block[-count:]
                # Source spelling, including relocation operands, stays exact.
                key=tuple((i['opcode'],i['operands'],i['size']) for i in seq)
                matches.setdefault(key,[]).append(seq)
        choices=[]
        for key, sites in matches.items():
            size=sum(i['size'] for i in sites[0])
            saving=(len(sites)-1)*(size-3)
            if len(sites)>1 and saving>0:
                choices.append((saving,size,key,sites))
        used=set(); insert={}; replace={}
        for _, size, key, sites in sorted(choices,key=lambda c:(-c[0],-c[1],str(c[2]))):
            sites=[s for s in sites if not used.intersection(i['line'] for i in s)]
            if len(sites)<2:
                continue
            used.update(i['line'] for s in sites for i in s)
            name=PREFIX+str(len(groups)).zfill(5)
            insert[sites[0][0]['line']-1]=f'\t.globl {name}\n{name} = .\n'
            for site in sites[1:]:
                replace[site[0]['line']-1]=(site[-1]['line'],f'\tljmp\t{name}\n')
            groups.append({'module':module,'symbol':name,'body':sites[0],
                           'retained_line':sites[0][0]['line'],
                           'replacements':[{'start_line':s[0]['line'],'end_line':s[-1]['line'],'original':''.join(lines[s[0]['line']-1:s[-1]['line']])} for s in sites[1:]],
                           'estimated_object_saved_bytes':(len(sites)-1)*(size-3)})
        result=[]; number=0
        while number<len(lines):
            if number in insert: result.append(insert[number])
            if number in replace:
                end,replacement=replace[number]; result.append(replacement); number=end
            else:
                result.append(lines[number]); number+=1
        changes[module]=''.join(result)
    shutil.copytree(source,target,ignore=shutil.ignore_patterns('*.rel','*.lst','*.rst','*.sym'))
    for module,text in changes.items():
        path=target/module; path.write_text(text); outputs[module]=sha(path)
    report={'algorithm':'experimental-exact-per-module-ret-tail-v1','extra_stack_bytes':0,
            'inputs':inputs,'outputs_sha256':outputs,'groups':groups,
            'estimated_object_saved_bytes':sum(g['estimated_object_saved_bytes'] for g in groups),
            'linked_saved_bytes':None,'hardware_validated':False}
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    return report


def verify_assembled(source: Path, target: Path, report_path: Path, report: dict):
    """Check fresh object area deltas; this is not a claim about linked gain."""
    def cseg_size(path):
        matches = re.findall(r'^A CSEG size ([0-9A-Fa-f]+) flags', path.read_text(), re.M)
        if len(matches) != 1:
            raise ValueError('Missing/ambiguous object CSEG: '+str(path))
        return int(matches[0], 16)
    expected = {}
    for group in report['groups']:
        expected[group['module']] = expected.get(group['module'],0)+group['estimated_object_saved_bytes']
    measurements = {}
    for module, hashes in report['inputs'].items():
        original, rewritten = source/module, target/module
        if sha(original)!=hashes['asm_sha256'] or sha(original.with_suffix('.lst'))!=hashes['lst_sha256']:
            raise ValueError('Tail-share input changed: '+module)
        if sha(rewritten)!=report['outputs_sha256'][module]:
            raise ValueError('Tail-share output changed: '+module)
        before, after = cseg_size(original.with_suffix('.rel')), cseg_size(rewritten.with_suffix('.rel'))
        if before-after != expected.get(module,0):
            raise ValueError('Unexpected tail-share object size: '+module)
        measurements[module] = {'before_cseg_bytes':before,'after_cseg_bytes':after,
                                'input_rel_sha256':sha(original.with_suffix('.rel')),
                                'output_rel_sha256':sha(rewritten.with_suffix('.rel')),
                                'output_lst_sha256':sha(rewritten.with_suffix('.lst'))}
    report['assembled_objects'] = measurements
    report['object_saved_bytes'] = sum(i['before_cseg_bytes']-i['after_cseg_bytes'] for i in measurements.values())
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    return report
