#!/usr/bin/env python3
"""Conservative SDCC function reachability for this pinned firmware build.

Unlike the upstream remover, every assembler symbol reference is an edge,
including address expressions and data tables. All code/data outside recognized
C functions is retained and roots every function it references. Unused function
locals and string pools are removed after a second symbol-reference check.
Initialized storage is retained. This is not a general assembly optimizer.
Input is immutable; output is a separate tree plus a reachability manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

SYMBOL = re.compile(r'(?<![\w$])(_[A-Za-z_$][\w$]*)(?![\w$])')
FUNCTION = re.compile(r'^;\s+function\s+([A-Za-z_$][\w$]*)\s*$')
AREA = re.compile(r'^\s*\.area\b')
GLOBAL = re.compile(r'^\s*\.globl\s+(\S+)\s*$')
EQUATE = re.compile(r'^\s*[A-Za-z_$][\w$]*\s*=')


def code(line: str) -> str:
    # SDCC comments never occur inside an assembler string containing a function
    # reference. Ignore strings entirely to avoid rooting names in debug text.
    return re.sub(r'"(?:[^"\\]|\\.)*"', '""', line.split(';', 1)[0])


@dataclass
class Function:
    module: str
    name: str
    first: int
    label: int
    end: int
    refs: set[str]

    @property
    def key(self):
        return self.module + ':' + self.name


def optimize(source: Path, target: Path, external_roots=()):
    if target.exists():
        raise ValueError('Output tree already exists: ' + str(target))
    files = {str(p.relative_to(source)): p.read_text() for p in sorted(source.rglob('*.asm'))}
    if not files:
        raise ValueError('No SDCC assembly inputs')
    functions = {}
    by_module = {}
    exports = {}
    roots = set()
    root_reasons = {}
    modules = {}
    for path, text in files.items():
        lines = text.splitlines(keepends=True)
        starts = [(i, FUNCTION.match(line.rstrip()).group(1)) for i, line in enumerate(lines) if FUNCTION.match(line.rstrip())]
        parsed = []
        for idx, (first, name) in enumerate(starts):
            symbol = '_' + name
            stop = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
            labels = [i for i in range(first, stop) if code(lines[i]).strip() in (symbol + ':', symbol + '::')]
            if len(labels) != 1:
                raise ValueError(f'{path}: expected exactly one label for {symbol}')
            label = labels[0]
            end = next((i for i in range(label + 1, stop) if AREA.match(code(lines[i]))), stop)
            refs = set()
            for line in lines[label + 1:end]:
                refs.update(SYMBOL.findall(code(line)))
            fn = Function(path, symbol, first, label, end, refs)
            if (path, symbol) in by_module:
                raise ValueError('Duplicate function in module')
            by_module[path, symbol] = fn.key
            functions[fn.key] = fn
            parsed.append(fn)
        module_globals = {m.group(1) for line in lines if (m := GLOBAL.match(code(line)))}
        for fn in parsed:
            if fn.name in module_globals:
                if fn.name in exports:
                    raise ValueError('Duplicate exported function: ' + fn.name)
                exports[fn.name] = fn.key
        owner = {}
        for fn in parsed:
            for i in range(fn.first, fn.end):
                owner[i] = fn.key
        modules[path] = (lines, parsed, owner)

    def resolve(module, symbol):
        return by_module.get((module, symbol), exports.get(symbol))

    edges = {}
    for key, fn in functions.items():
        edges[key] = {dst for ref in fn.refs if (dst := resolve(fn.module, ref)) is not None}
    for path, (lines, parsed, owner) in modules.items():
        for i, line in enumerate(lines):
            if i in owner:
                continue
            c = code(line)
            if GLOBAL.match(c) or EQUATE.match(c):
                continue
            for symbol in SYMBOL.findall(c):
                dst = resolve(path, symbol)
                if dst is not None:
                    roots.add(dst)
                    root_reasons.setdefault(dst, []).append({'module': path, 'line': i + 1, 'text': c.strip()})
    # Runtime libraries can call these application entry points without a
    # relocation in an application ASM input. Keep them if compiled.
    for symbol in ('_main', '__sdcc_external_startup', '_putchar', '_putchar_', '_getchar'):
        if symbol in exports:
            roots.add(exports[symbol])
            root_reasons.setdefault(exports[symbol], []).append({'runtime_root': symbol})
    for symbol in external_roots:
        if symbol not in exports:
            raise ValueError('Missing explicit external root: ' + symbol)
        roots.add(exports[symbol])
        root_reasons.setdefault(exports[symbol], []).append({'external_root': symbol})
    reachable = set(roots)
    todo = list(roots)
    while todo:
        for child in edges[todo.pop()]:
            if child not in reachable:
                reachable.add(child)
                todo.append(child)
    removed = set(functions) - reachable
    if not any(functions[k].name == '_main' for k in reachable):
        raise ValueError('No reachable main function')

    target.mkdir(parents=True)
    optimized = {}
    for path, (lines, parsed, owner) in modules.items():
        output = []
        for i, line in enumerate(lines):
            c = code(line)
            if owner.get(i) in removed:
                # ar0..ar7 aliases are only emitted in the first function and
                # can be referenced by all following retained functions.
                if EQUATE.match(c):
                    output.append(line)
                continue
            m = GLOBAL.match(c)
            if m and resolve(path, m.group(1)) in removed:
                continue
            output.append(line)
        blob = ''.join(output)
        # Independent retained-text check: no removed callable symbol may remain
        # as any actual reference (declarations and equates excluded).
        for i, line in enumerate(blob.splitlines()):
            c = code(line)
            if GLOBAL.match(c) or EQUATE.match(c):
                continue
            for symbol in SYMBOL.findall(c):
                if resolve(path, symbol) in removed:
                    raise AssertionError(f'dangling function {path}:{i+1}: {symbol}')
        optimized[path] = blob

    # Do not change initialized sections: their size/order must match XINIT.
    labels = re.compile(r'^\s*(_[A-Za-z_$][\w$]*):{1,2}\s*$')
    defs = {}
    variable_exports = {}
    refs = {}
    allocation_candidates = {}
    string_candidates = {}
    for path, blob in optimized.items():
        lines = blob.splitlines(keepends=True)
        area = ''
        for i, line in enumerate(lines):
            c = code(line)
            m = re.match(r'^\s*\.area\s+(\w+)', c)
            if m:
                area = m.group(1)
            m = labels.match(c)
            if m:
                name = m.group(1)
                defs[path, name] = i
                dead_owner = any(fn.module == path and name.startswith(fn.name+'_') for key, fn in functions.items() if key in removed)
                if dead_owner and area in ('DSEG','OSEG','BSEG','PSEG','XSEG') and i+1 < len(lines) and re.match(r'^\s*\.ds\s+\d+\s*$', code(lines[i+1])):
                    allocation_candidates[path, name] = (i, i+2)
                if area == 'CONST' and re.fullmatch(r'___str_\d+', name):
                    stop = next((j for j in range(i+1,len(lines)) if labels.match(code(lines[j])) or AREA.match(code(lines[j]))), len(lines))
                    string_candidates[path, name] = (i, stop)
            m = GLOBAL.match(c)
            if m:
                variable_exports.setdefault(m.group(1), set()).add(path)
                continue
            if labels.match(c) or EQUATE.match(c):
                continue
            for name in SYMBOL.findall(c):
                refs.setdefault(name,set()).add(path)

    deletions = {}
    pruned = []
    for (path,name), (first,end) in {**allocation_candidates, **string_candidates}.items():
        referenced = path in refs.get(name,set())
        if path in variable_exports.get(name,set()):
            referenced |= any((other,name) not in defs for other in refs.get(name,set()))
        if referenced:
            continue
        deletions.setdefault(path,set()).update(range(first,end))
        pruned.append({'module':path,'symbol':name,'kind':'string' if (path,name) in string_candidates else 'uninitialized_function_local'})
    pruned_keys = {(x['module'],x['symbol']) for x in pruned}
    hashes = []
    for path, blob in optimized.items():
        output = []
        for i,line in enumerate(blob.splitlines(keepends=True)):
            if i in deletions.get(path,set()):
                continue
            m = GLOBAL.match(code(line))
            if m and ((path,m.group(1)) in pruned_keys or (m.group(1) not in refs and any(n==m.group(1) for _,n in pruned_keys))):
                continue
            output.append(line)
        blob = ''.join(output)
        dst = target / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(blob)
        hashes.append({'path': path, 'before_sha256': hashlib.sha256(files[path].encode()).hexdigest(), 'after_sha256': hashlib.sha256(blob.encode()).hexdigest()})
    manifest = {
        'input': str(source), 'output': str(target), 'modules': len(files),
        'functions': len(functions), 'retained': len(reachable), 'removed_count': len(removed),
        'roots': root_reasons,
        'removed': sorted(removed),
        'pruned_storage': pruned,
        'retained_edges': {key: sorted(edges[key]) for key in sorted(reachable)},
        'input_output_hashes': hashes,
        'limits': [
            'No code execution or hardware validation is implied.',
            'Initialized storage and every referenced local allocation are preserved.',
            'All function-address expressions in retained code/data are retained conservatively.',
            'Applies to compiler-produced symbolic code; arbitrary computed numeric internal function pointers are not supported.'
        ],
    }
    (target/'reachability.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({k:manifest[k] for k in ('modules','functions','retained','removed_count')}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--root', action='append', default=[], help='Function referenced by external loader/packer')
    args = p.parse_args()
    optimize(args.source.resolve(), args.output.resolve(), args.root)
