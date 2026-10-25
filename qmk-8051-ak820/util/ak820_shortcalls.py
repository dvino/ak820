"""Opt-in 8051 short transfers from immutable post-outline assembly.

Only compiler-generated foreground code without computed/PC-relative transfers
is eligible. Reassembly regenerates relocations; IHX bytes and intended symbols
are checked independently of linker diagnostics. No binary patching or device IO.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile

from ak820_linked_inventory import ihx_bytes, listing, page_eligible
from ak820_outline_audit import LISTED

ALGORITHM = 'foreground-short-transfers-v2'
# Keep hardware, boot, NVM, IRQ and USB control modules outside this scope.
# color.c contains handwritten inline assembly and is explicitly excluded.
FOREGROUND = frozenset({
    'ak820_tapping.asm', 'ak820_combo.asm', 'ak820_oneshot.asm',
    'ak820_macro.asm', 'ak820_settings.asm', 'ak820_tap_dance.asm',
    'ak820_key_override.asm', 'keyboards/ajazz/ak820/ak820_rgb.asm',
    'protocol/report.asm', 'protocol/host.asm',
})
SYMBOL = re.compile(r'_[A-Za-z_$][\w$]*|\d+\$')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def eligible(module):
    return (module.startswith('quantum/') and module != 'quantum/color.asm') or module in FOREGROUND


@dataclass(frozen=True)
class Instruction:
    address: int
    data: bytes
    opcode: str
    operand: str
    function: str
    area: str


@dataclass
class Module:
    source: list[str]
    instructions: dict[int, Instruction]
    labels: dict[tuple[str, str], int]


def modules(tree, image, *, diagnostic_candidates=None, diagnostic_symbols=None,
            diagnostic_rejections=None):
    """Authenticate relocated rows and match every instruction to its ASM line."""
    result, warning_sites = {}, []
    admitted_warnings = {(c['module'],c['line']):c for c in (diagnostic_candidates or [])}
    for asm in sorted(tree.rglob('*.asm')):
        module = asm.relative_to(tree).as_posix()
        rst = asm.with_suffix('.rst')
        # ASlink inserts an unnumbered page-warning marker into failed trial
        # listings. Strip only that exact diagnostic, only for trials; keep
        # baseline/final authentication strict and never hide another row.
        raw_listing = rst.read_text()
        if diagnostic_candidates is not None:
            rows = raw_listing.splitlines(keepends=True)
            cleaned = []
            for index, raw in enumerate(rows):
                marker = re.fullmatch(r'\?ASlink-Warning-2K Page relocation error(?: for symbol\s+(\S+))?\n',raw)
                if not marker:
                    cleaned.append(raw)
                    continue
                following = LISTED.match(rows[index+1]) if index+1<len(rows) else None
                key = (module,int(following[3])) if following else None
                if key not in admitted_warnings or following[4].lower() not in ('acall','ajmp'):
                    raise ValueError('Unexpected diagnostic listing page marker')
                candidate = admitted_warnings[key]
                if marker[1] is not None and marker[1] != candidate['target']:
                    raise ValueError('Diagnostic marker symbol differs')
                if key in warning_sites:
                    raise ValueError('Duplicate diagnostic listing page marker')
                warning_sites.append(key)
            with tempfile.NamedTemporaryFile(mode='w+',suffix='.rst') as temporary:
                temporary.write(''.join(cleaned))
                temporary.flush()
                listing(Path(temporary.name), image, module)
        else:
            listing(rst, image, module)
        source = asm.read_text().splitlines(keepends=True)
        context = {}
        area, function = '', ''
        for number, original in enumerate(source):
            text = original.split(';', 1)[0].strip()
            match = re.fullmatch(r';\s*function\s+(\w+)\s*', original.strip())
            if match:
                function = match[1]
            match = re.match(r'\.area\s+(\w+)', text)
            if match:
                area = match[1]
            context[number] = area, function
        instructions, labels = {}, {}
        for raw in raw_listing.splitlines():
            match = LISTED.match(raw)
            if match:
                number = int(match[3]) - 1
                if number not in context or number in instructions:
                    raise ValueError('Invalid/duplicate listing source line: ' + module)
                opcode = match[4].lower()
                operand = re.sub(r'\s+', '', match[5].split(';', 1)[0])
                text = source[number].split(';', 1)[0].strip().split(None, 1)
                if not text or text[0].lower() != opcode or re.sub(r'\s+', '', text[1] if len(text)>1 else '') != operand:
                    raise ValueError('Stale ASM/listing instruction: ' + module + ':' + str(number+1))
                area, function = context[number]
                instructions[number] = Instruction(int(match[1], 16),
                    bytes.fromhex(re.sub(r'[rstup*]', '', match[2])), opcode, operand, function, area)
            source_row = re.match(r'^\s*(\d+)\s+(.*)$', raw[34:])
            address = re.match(r'^      ([0-9A-F]{6})', raw)
            if source_row and address:
                number = int(source_row[1]) - 1
                label = re.fullmatch(r'([\w.$]+)::?', source_row[2].strip())
                if label and number in context:
                    key = context[number][1], label[1]
                    value = int(address[1], 16)
                    if key in labels and labels[key] != value:
                        raise ValueError('Ambiguous listing label: ' + module)
                    labels[key] = value
        result[module] = Module(source, instructions, labels)
    if not result:
        raise ValueError('No short-call input assembly')
    for name,line in warning_sites:
        candidate = admitted_warnings[(name,line)]
        row = result[name].instructions[line-1]
        target = resolve(result[name],candidate['function'],candidate['target'],diagnostic_symbols)
        expected = 'acall' if candidate['kind'] == 'lcall' else 'ajmp'
        original = re.sub(r'\b'+expected+r'\b', candidate['kind'],
                          result[name].source[line-1], count=1)
        if (candidate['kind'] not in ('lcall', 'ljmp') or row.opcode != expected
                or row.operand != candidate['target'] or row.function != candidate['function']
                or rewrite(original, candidate) != result[name].source[line-1]):
            raise ValueError('Diagnostic marker candidate differs from source row')
        # ASlink can reject a boundary transfer whose PC+2 decoding is valid.
        # Such a trial is never a final artifact: restore this exact site to
        # its immutable long instruction and relink, preserving strict checks.
        if diagnostic_rejections is not None:
            diagnostic_rejections.append({'module':name, 'line':line,
                'site':row.address, 'target':target, 'bytes':row.data.hex(),
                'encoding_valid':short_valid(row.address,row.data,target,candidate['kind'])})
    return result


def code_symbols(mapfile):
    # Even ASlink's wide map truncates names at 32 characters. NoICE DEF rows
    # retain the full names; require each CODE map entry to match that output.
    code = set()
    for raw in mapfile.read_text().splitlines():
        match = re.match(r'C:\s+([0-9A-F]{8})\s+(_\S+)', raw)
        if match:
            code.add((match[2], int(match[1],16)))
    result, matched = {}, set()
    for raw in mapfile.with_suffix('.noi').read_text().splitlines():
        match = re.fullmatch(r'DEF (_\S+) 0x([0-9A-Fa-f]+)',raw)
        if not match:
            continue
        name, value = match[1], int(match[2],16)
        key = name[:32], value
        if key not in code:
            continue
        if name in result and result[name] != value:
            raise ValueError('Ambiguous CODE symbol: ' + name)
        result[name] = value
        matched.add(key)
    if not code or matched != code:
        raise ValueError('Incomplete full-name CODE symbol evidence')
    return result


def resolve(module, function, operand, symbols):
    values = {address for (owner, name), address in module.labels.items()
              if name == operand and (operand.startswith('_') or owner == function)}
    if operand.startswith('_') and operand in symbols:
        values.add(symbols[operand])
    if len(values) != 1:
        raise ValueError('Missing/ambiguous short-transfer target: ' + operand)
    return values.pop()


def short_valid(site, data, target, kind):
    """Use the following instruction's PC for the 2 KiB page, including edges."""
    return (kind in ('lcall', 'ljmp') and len(data) == 2
            and data[0] & 31 == (17 if kind == 'lcall' else 1)
            and (((site+2) & 0xf800) | ((data[0] & 0xe0) << 3) | data[1]) == target
            and page_eligible(site, target))


def edge(instruction):
    data, site = instruction.data, instruction.address
    opcode = data[0]
    if opcode in (2, 18):
        return int.from_bytes(data[1:], 'big')
    if opcode & 31 in (1, 17):
        return ((site+2) & 0xf800) | ((opcode & 0xe0) << 3) | data[1]
    if opcode in (0x10,0x20,0x30,0x40,0x50,0x60,0x70,0x80,0xd5) or 0xb4<=opcode<=0xbf or 0xd8<=opcode<=0xdf:
        return (site+len(data)+int.from_bytes(data[-1:], signed=True)) & 65535
    return None


def select(baseline, symbols):
    candidates, excluded = [], Counter()
    for name, module in sorted(baseline.items()):
        if not eligible(name):
            continue
        unsafe = {r.function for r in module.instructions.values()
                  if r.opcode == 'jmp' or 'pc' in r.operand.lower()}
        for line, row in module.instructions.items():
            if row.opcode not in ('lcall', 'ljmp') or row.area != 'CSEG':
                continue
            # Outliner calls use the same immutable source identity and full
            # relocated-edge checks as compiler calls. Scope belongs to the
            # caller: a helper name never admits an excluded module/function.
            if not row.function or row.function in unsafe:
                excluded['computed_or_pc_relative_function'] += 1
                continue
            if not SYMBOL.fullmatch(row.operand):
                excluded['complex_target'] += 1
                continue
            target = resolve(module, row.function, row.operand, symbols)
            if edge(row) != target:
                raise ValueError('Baseline transfer differs from intended symbol')
            if not page_eligible(row.address, target):
                excluded['baseline_crosspage'] += 1
                continue
            candidates.append({'module': name, 'line': line+1, 'function': row.function,
                'kind': row.opcode, 'target': row.operand,
                'source_line_sha256': hashlib.sha256(module.source[line].encode()).hexdigest(),
                'baseline_site': row.address, 'baseline_target': target})
    return candidates, dict(excluded)


def rewrite(original, candidate):
    if hashlib.sha256(original.encode()).hexdigest() != candidate['source_line_sha256']:
        raise ValueError('Stale candidate source hash')
    pieces = original.split(';', 1)[0].strip().split()
    if pieces != [candidate['kind'], candidate['target']]:
        raise ValueError('Stale candidate instruction')
    return re.sub(r'\b'+candidate['kind']+r'\b',
                  'acall' if candidate['kind']=='lcall' else 'ajmp', original, count=1)


def write_tree(source, target, candidates):
    """Always derive trials from the immutable input; copy no stale listings."""
    # ASlink may recreate the original listing directories after their tree
    # was renamed to the immutable preimage. Empty directories contain no
    # build input. Reject every file, link or special object as before.
    if target.is_symlink() or (target.exists() and (
            not target.is_dir() or any(path.is_symlink() or not path.is_dir()
                                      for path in target.rglob('*')))):
        raise ValueError('Short-call output already exists: ' + str(target))
    for path in sorted(source.rglob('*')):
        if path.is_file() and path.suffix in ('.asm', '.json'):
            output = target/path.relative_to(source)
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, output)
    grouped = defaultdict(list)
    for candidate in candidates:
        grouped[candidate['module']].append(candidate)
    for name, sites in grouped.items():
        asm = target/name
        lines = asm.read_text().splitlines(keepends=True)
        for candidate in sites:
            number = candidate['line']-1
            if not 0 <= number < len(lines):
                raise ValueError('Stale candidate line number')
            lines[number] = rewrite(lines[number], candidate)
        asm.write_text(''.join(lines))


def checks(final, symbols, candidates):
    result = []
    for candidate in candidates:
        row = final[candidate['module']].instructions[candidate['line']-1]
        target = resolve(final[candidate['module']], candidate['function'], candidate['target'], symbols)
        result.append({**candidate, 'final_site': row.address, 'intended_target': target,
            'bytes': row.data.hex(), 'decoded_target': edge(row),
            'valid': short_valid(row.address, row.data, target, candidate['kind'])})
    return result


def verify(baseline, final, before_symbols, after_symbols, candidates):
    """Check exact source edits, every listed edge, and fixed/PC slot widths."""
    if baseline.keys() != final.keys():
        raise ValueError('Changed short-call module set')
    admitted, _ = select(baseline, before_symbols)
    admitted_by_line = {(c['module'],c['line']):c for c in admitted}
    if any(admitted_by_line.get((c['module'],c['line'])) != c for c in candidates):
        raise ValueError('Short-call candidate outside the verified scope')
    selected = {(c['module'], c['line']-1): c for c in candidates}
    if len(selected) != len(candidates):
        raise ValueError('Duplicate short-call candidate')
    mapping = {}
    def add(before, after):
        if before in mapping and mapping[before] != after:
            raise ValueError('Inconsistent relocated instruction identity')
        mapping[before] = after
    for name, module in baseline.items():
        current = final[name]
        if module.instructions.keys() != current.instructions.keys() or len(module.source) != len(current.source):
            raise ValueError('Changed short-call instruction/source layout')
        for line, original in enumerate(module.source):
            candidate = selected.get((name, line))
            expected = rewrite(original, candidate) if candidate else original
            if current.source[line] != expected:
                raise ValueError('Unexpected short-call ASM edit: ' + name)
        for line, row in module.instructions.items():
            add(row.address, current.instructions[line].address)
    # Exported library functions do not have listings in this build tree.
    for name, address in before_symbols.items():
        if name in after_symbols:
            add(address, after_symbols[name])
    edges, hazards = 0, defaultdict(set)
    for name, module in baseline.items():
        dangerous = {r.function for r in module.instructions.values()
                     if r.opcode=='jmp' or 'pc' in r.operand.lower()}
        for line, row in module.instructions.items():
            current = final[name].instructions[line]
            target = edge(row)
            if (name,line) not in selected:
                old_short = row.data[0]&31 in (1,17)
                opcode_matches = ((row.data[0]&31)==(current.data[0]&31) if old_short
                                  else row.data[0]==current.data[0])
                if len(row.data) != len(current.data) or not opcode_matches:
                    raise ValueError('Unchanged instruction opcode/width differs')
                if target is None:
                    immediates = [part[1:] for part in row.operand.split(',') if part.startswith('#')]
                    symbolic = any(re.search(r'(?<![\w])(?:[A-Za-z_$][\w$]*|\d+\$)',part)
                                   for part in immediates)
                    width = (2 if row.opcode=='mov' and row.operand.startswith('dptr,#') else 1) if symbolic else 0
                    if (row.data[:-width] != current.data[:-width] if width else row.data != current.data):
                        raise ValueError('Unchanged nonrelocation instruction bytes differ')
            if target is not None:
                if (row.data[0] not in (2,18) and row.data[0]&31 not in (1,17)
                        and row.data[:-1] != current.data[:-1]):
                    raise ValueError('Relative branch condition bytes differ')
                if edge(current) != mapping.get(target, target):
                    raise ValueError('Relocated control-flow edge differs: '+name+':'+str(line+1))
                edges += 1
            if row.function in dangerous:
                if (row.opcode,row.operand,len(row.data)) != (current.opcode,current.operand,len(current.data)):
                    raise ValueError('Computed/PC-relative instruction width changed')
                hazards[(name,row.function,row.area)].add(current.address-row.address)
    if any(len(shifts)!=1 for shifts in hazards.values()):
        raise ValueError('Computed/PC-relative function has nonuniform relocation')
    exact = checks(final, after_symbols, candidates)
    if any(not item['valid'] for item in exact):
        raise ValueError('Invalid final short-transfer encoding')
    return {'verified_control_flow_edges':edges, 'uniform_hazard_sections':len(hazards), 'sites':exact}


def page_errors_only(log):
    """Recognize only pinned ASlink's complete page-error diagnostic blocks."""
    block = (r'\?ASlink-Warning-2K Page relocation error(?: for symbol\s+\S+)?\n'
             r'\s*file\s+module\s+area\s+offset\n'
             r'\s*Refby[^\n]+\n\s*Defin[^\n]+(?:\n|$)')
    text = log.replace('\r\n','\n')
    return bool(re.search(block, text)) and not re.sub(block, '', text).strip()


def source_snapshot(source):
    return {p.relative_to(source).as_posix():digest(p) for p in sorted(source.rglob('*'))
            if p.is_file() and p.suffix in ('.asm','.json')}


def require_immutable(source, initial):
    if source_snapshot(source) != initial:
        raise ValueError('Immutable short-call source changed')


def prepare(source, work, link):
    """Return stable candidates; link(tree, image, label, allow_page_errors).

    The callback assembles the fresh tree and links diagnostic-only layouts with
    a 64 KiB CODE ceiling. The caller must do a final strict link and finish().
    """
    if work.exists():
        raise ValueError('Short-call work directory already exists')
    initial = source_snapshot(source)
    work.mkdir(parents=True)
    image = work/'baseline.ihx'
    link(source, image, 'shortcalls-baseline', False)
    require_immutable(source, initial)
    before_image = ihx_bytes(image)
    baseline = modules(source, before_image)
    symbols = code_symbols(image.with_suffix('.map'))
    candidates, excluded = select(baseline, symbols)
    active = candidates[:]
    history = []
    for iteration in range(len(candidates)+1):
        trial = work/('iteration-'+str(iteration))
        tree = trial/'dce'
        require_immutable(source, initial)
        write_tree(source, tree, active)
        image = trial/'layout.ihx'
        exit_code = link(tree, image, 'shortcalls-'+str(iteration), True)
        require_immutable(source, initial)
        trial_symbols = code_symbols(image.with_suffix('.map'))
        linker_rejections = []
        final = modules(tree, ihx_bytes(image), diagnostic_candidates=active,
                        diagnostic_symbols=trial_symbols, diagnostic_rejections=linker_rejections)
        rows = checks(final, trial_symbols, active)
        encoding_rejections = {(r['module'],r['line']) for r in rows if not r['valid']}
        invalid = encoding_rejections | {(r['module'],r['line']) for r in linker_rejections}
        history.append({'iteration':iteration, 'selected':len(active), 'invalid':len(invalid),
                        'encoding_rejected_sites':[{'module':name,'line':line}
                            for name,line in sorted(encoding_rejections)],
                        'linker_rejected_sites':linker_rejections,
                        'link_exit_code':exit_code})
        (trial/'checks.json').write_text(json.dumps(rows, indent=2)+'\n')
        if not invalid:
            if exit_code:
                raise ValueError('Linker rejected independently valid short transfers')
            return {'candidates':active, 'initial_candidates':len(candidates),
                    'excluded':excluded, 'iterations':history,
                    'baseline_image_sha256':digest(work/'baseline.ihx'),
                    'baseline_occupied_bytes':len(before_image),
                    'input_sources_sha256':initial}
        active = [c for c in active if (c['module'],c['line']) not in invalid]
    raise ValueError('Short-call relaxation did not converge')


def finish(source, target, baseline_image, image, plan, report):
    """Only call after the strict final link and memory-window checks succeed."""
    require_immutable(source, plan['input_sources_sha256'])
    if digest(baseline_image) != plan['baseline_image_sha256']:
        raise ValueError('Immutable short-call input changed')
    before_data, after_data = ihx_bytes(baseline_image), ihx_bytes(image)
    evidence = verify(modules(source, before_data), modules(target, after_data),
        code_symbols(baseline_image.with_suffix('.map')), code_symbols(image.with_suffix('.map')),
        plan['candidates'])
    saved = len(before_data)-len(after_data)
    if saved != len(plan['candidates']):
        raise ValueError('Short-call occupied-byte saving differs from selected count')
    input_files = [baseline_image, baseline_image.with_suffix('.map'), baseline_image.with_suffix('.noi')]
    input_files.extend(p for p in sorted(source.rglob('*')) if p.is_file() and p.suffix in ('.asm','.rel','.rst','.json'))
    records = [{'path':p.relative_to(report.parent).as_posix(), 'sha256':digest(p),
                'size':p.stat().st_size} for p in input_files]
    result = {'algorithm':ALGORITHM, 'tool_sha256':digest(Path(__file__)), **plan,
        'input_artifacts':records,
        'final_image_sha256':digest(image), 'final_noice_sha256':digest(image.with_suffix('.noi')),
        'final_occupied_bytes':len(after_data),
        'saved_bytes':saved, **evidence, 'hardware_validated':False}
    report.write_text(json.dumps(result, indent=2)+'\n')
    return result


def validate_saved(build, image, report):
    """Recheck a saved manifest against its immutable inputs and final image."""
    if report.get('algorithm') != ALGORITHM or report.get('tool_sha256') != digest(Path(__file__)):
        raise ValueError('Unqualified short-call algorithm/tool')
    source, baseline_image = build/'shortcalls-input', build/'shortcalls/baseline.ihx'
    require_immutable(source, report['input_sources_sha256'])
    expected = [baseline_image, baseline_image.with_suffix('.map'), baseline_image.with_suffix('.noi')]
    expected.extend(p for p in sorted(source.rglob('*')) if p.is_file() and p.suffix in ('.asm','.rel','.rst','.json'))
    records = [{'path':p.relative_to(build).as_posix(),'sha256':digest(p),'size':p.stat().st_size} for p in expected]
    if (records != report.get('input_artifacts') or digest(image) != report.get('final_image_sha256')
            or digest(image.with_suffix('.noi')) != report.get('final_noice_sha256')):
        raise ValueError('Short-call input/output evidence changed')
    before, after = ihx_bytes(baseline_image), ihx_bytes(image)
    evidence = verify(modules(source,before), modules(build/'dce',after),
        code_symbols(baseline_image.with_suffix('.map')),code_symbols(image.with_suffix('.map')),
        report['candidates'])
    if any(report.get(key) != value for key,value in evidence.items()):
        raise ValueError('Short-call exact verification evidence differs')
    if (report.get('baseline_occupied_bytes') != len(before)
            or report.get('final_occupied_bytes') != len(after)
            or report.get('saved_bytes') != len(before)-len(after)
            or report.get('saved_bytes') != len(report['candidates'])
            or report.get('hardware_validated') is not False):
        raise ValueError('Short-call size/validation evidence differs')
    return evidence
