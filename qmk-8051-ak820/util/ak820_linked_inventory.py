#!/usr/bin/env python3
"""Conservative linked-byte inventory; no firmware mutation or timing model."""
import argparse
import hashlib
import json
from pathlib import Path
import re


# Classic 8051 instruction lengths, indexed by opcode (row = high nibble).
# A5 is reserved and deliberately rejected; no CH555 extension is assumed.
OPCODE_LENGTHS = tuple(int(n) for row in (
    '1231121111111111', '3231121111111111',
    '3211221111111111', '3211221111111111',
    '2223221111111111', '2223221111111111',
    '2223221111111111', '2221232222222222',
    '2221132222222222', '3221221111111111',
    '2221102222222222', '2221333333333333',
    '2221121111111111', '2221131122222222',
    '1211121111111111', '1211121111111111',
) for n in row)


def validate_windows(report, image):
    windows = report['code_windows']
    if not isinstance(windows, list) or len(windows) != 2:
        raise ValueError('Expected main and low CODE windows')
    for window in windows:
        if (not isinstance(window, list) or len(window) != 2
                or any(type(v) is not int for v in window)
                or not 0 <= window[0] < window[1] <= 65536):
            raise ValueError('Invalid CODE window')
    main, low = windows
    if main != report['code_window'] or max(main[0],low[0]) < min(main[1],low[1]):
        raise ValueError('Inconsistent or overlapping CODE windows')
    counts = [sum(start <= address < end for address in image) for start,end in windows]
    if sum(counts) != len(image):
        raise ValueError('IHX bytes outside declared CODE windows')
    if counts != [report['code_main_bytes'],report['code_low_bytes']]:
        raise ValueError('Build report main/low byte totals mismatch')
    return counts


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ihx_bytes(path):
    data, base, eof = {}, 0, False
    for line in path.read_text().splitlines():
        if eof or not line.startswith(':'):
            raise ValueError('Malformed Intel HEX or record after EOF')
        try:
            record = bytes.fromhex(line[1:])
        except ValueError as exc:
            raise ValueError('Malformed Intel HEX') from exc
        if len(record) < 5 or len(record) != record[0] + 5 or sum(record) & 255:
            raise ValueError('Intel HEX length/checksum failure')
        n, addr, kind = record[0], int.from_bytes(record[1:3], 'big'), record[3]
        payload = record[4:-1]
        if kind == 0:
            for offset, byte in enumerate(payload):
                key = base + addr + offset
                if key in data:
                    raise ValueError('Overlapping Intel HEX records')
                data[key] = byte
        elif kind == 1 and n == 0 and addr == 0:
            eof = True
        elif kind in (2, 4) and n == 2 and addr == 0:
            base = int.from_bytes(payload, 'big') << (4 if kind == 2 else 16)
        else:
            raise ValueError('Unsupported Intel HEX record')
    if not eof or not data or max(data) > 65535:
        raise ValueError('Missing EOF, empty image, or non-mcs51 address')
    return data


def page_eligible(site, target):
    return ((site + 2) & 0xF800) == (target & 0xF800)


def listing(path, image, module):
    """Count only relocated CODE rows carrying assembler instruction cycles.

    Listing labels are descriptive, not independently authenticated semantics.
    Function buckets use nonnumeric labels and are qualified by module.
    """
    area, function = None, '<unattributed>'
    rows, labels = [], {}
    for number, line in enumerate(path.read_text().splitlines(), 1):
        # ASxxxx's fixed columns separate bytes from cycles/source line/text.
        source = re.match(r'^\s*\d+\s+(.*)$', line[34:])
        if not source:
            if line.strip() and not line.startswith('\f'):
                raise ValueError(f'{path}:{number}: unrecognized listing row')
            continue
        text = source[1].strip()
        match = re.match(r'\.area\s+(\w+)\s*(.*)', text)
        if match:
            area = (match[1], 'CODE' in match[2])
            function = '<unattributed>'
        address = re.match(r'^      ([0-9A-F]{6})', line)
        label = re.fullmatch(r'([A-Za-z_.$][\w.$]*)::?', text)
        if label and address and area and area[1]:
            function = label[1]
            labels.setdefault(int(address[1], 16), []).append(module + ':' + function)
        if '[' not in line[:32]:
            continue
        if not address or not area or not area[1]:
            raise ValueError(f'{path}:{number}: instruction outside known CODE area')
        raw = line[13:28].strip()
        if not re.fullmatch(r'[0-9A-F]{2}(?: [0-9A-F]{2}){0,2}', raw):
            raise ValueError(f'{path}:{number}: unrecognized instruction bytes {raw!r}')
        encoded = bytes.fromhex(raw)
        site = int(address[1], 16)
        if any(image.get(site+i) != b for i, b in enumerate(encoded)):
            raise ValueError(f'{path}:{number}: listing byte mismatch at {site:04x}')
        opcode = encoded[0]
        if OPCODE_LENGTHS[opcode] == 0 or len(encoded) != OPCODE_LENGTHS[opcode]:
            raise ValueError(f'{path}:{number}: invalid 8051 instruction length')
        transfer = None
        if opcode in (0x02, 0x12):
            if len(encoded) != 3:
                raise ValueError('Invalid long transfer length')
            transfer = {'kind': 'lcall' if opcode == 0x12 else 'ljmp',
                        'target': int.from_bytes(encoded[1:], 'big')}
        elif opcode & 0x1F in (1, 0x11):
            if len(encoded) != 2:
                raise ValueError('Invalid short transfer length')
            transfer = {'kind': 'acall' if opcode & 0x1F == 0x11 else 'ajmp',
                        'target': ((site+2)&0xF800) | ((opcode&0xE0)<<3) | encoded[1]}
        rows.append({'site': site, 'bytes': encoded.hex(), 'size': len(encoded),
                     'module': module, 'function': module+':'+function,
                     'transfer': transfer})
    return rows, labels


def inventory(root, report_path, *, ihx=None, map_file=None, reachability=None):
    root, report_path = Path(root).resolve(), Path(report_path).resolve()
    report = json.loads(report_path.read_text())
    entries = report['artifacts']
    paths = {}
    for entry in entries:
        path = (root / entry['path']).resolve()
        if not path.is_relative_to(root) or entry['path'] in paths or path in paths.values():
            raise ValueError('Artifact path escape or duplicate')
        if path.stat().st_size != entry['size'] or digest(path) != entry['sha256']:
            raise ValueError(f'Artifact identity mismatch: {path}')
        paths[entry['path']] = path
    def one(suffix):
        found = [p for p in paths.values() if p.name.endswith(suffix)]
        if len(found) != 1:
            raise ValueError(f'Expected exactly one {suffix}')
        return found[0]
    selected = (ihx, map_file, reachability)
    explicit = any(value is not None for value in selected)
    if explicit and not all(value is not None for value in selected):
        raise ValueError('Explicit selection requires IHX, MAP and reachability paths')
    def select(value, suffix):
        # Require the exact manifest spelling, not aliases or unrecorded files.
        if not isinstance(value, str) or value not in paths or not value.endswith(suffix):
            raise ValueError(f'Selected {suffix} must name a report artifact')
        return paths[value]
    if explicit:
        image_path, map_path, reach_path = [select(value, suffix) for value, suffix in
                                          zip(selected, ('.ihx', '.map', 'reachability.json'))]
    else:
        image_path, map_path, reach_path = one('.ihx'), one('.map'), one('reachability.json')
    image = ihx_bytes(image_path)
    if len(image) != report['code_bytes'] or min(image) != report['code_min'] or max(image) != report['code_max_inclusive']:
        raise ValueError('Build report/image extent mismatch')
    main_bytes, low_bytes = validate_windows(report, image)
    reach = json.loads(reach_path.read_text())
    areas = {}
    for name, start, size, attrs in re.findall(r'^(\w+)\s+([0-9A-F]{8})\s+([0-9A-F]{8}) =\s+\d+\. bytes \(([^)]+)\)', map_path.read_text(), re.M):
        if 'CODE' in attrs:
            value = (int(start,16), int(size,16))
            if name in areas and areas[name] != value:
                raise ValueError('Conflicting MAP areas')
            areas[name] = value
    if not areas:
        raise ValueError('No CODE areas parsed')
    rows, labels, evidence = [], {}, []
    for address, name, module in re.findall(r'^C:[ \t]+([0-9A-F]{8})[ \t]+(\S+)[ \t]+([^ \t\r\n]*)[ \t]*$', map_path.read_text(), re.M):
        if int(address,16) in image:
            labels.setdefault(int(address,16), []).append('MAP:'+module+':'+name)
    listing_paths = sorted(reach_path.parent.rglob('*.rst'))
    if explicit and any(path.resolve() not in paths.values() for path in listing_paths):
        raise ValueError('Selected listing tree contains an unrecorded listing')
    for path in listing_paths:
        if not path.resolve().is_relative_to(root):
            raise ValueError('Listing path escape')
        module = path.relative_to(reach_path.parent).with_suffix('.asm').as_posix()
        part, names = listing(path, image, module)
        rows.extend(part)
        for address, values in names.items():
            labels.setdefault(address, []).extend(values)
        evidence.append({'path': path.relative_to(root).as_posix(), 'sha256': digest(path)})
    occupied = set()
    modules, functions, transfers = {}, {}, []
    for row in rows:
        addresses = set(range(row['site'], row['site']+row['size']))
        if addresses & occupied:
            raise ValueError('Overlapping listing instructions')
        occupied |= addresses
        for grouping, key in ((modules,row['module']), (functions,row['function'])):
            grouping.setdefault(key, {'instruction_bytes':0,'instructions':0,'start':row['site'],'end_exclusive':0})
            value = grouping[key]
            value['instruction_bytes'] += row['size']
            value['instructions'] += 1
            value['start'] = min(value['start'],row['site'])
            value['end_exclusive'] = max(value['end_exclusive'],row['site']+row['size'])
        if row['transfer']:
            transfer = dict(row['transfer'], site=row['site'], caller=row['function'])
            transfer['target_labels'] = labels.get(transfer['target'], [])
            transfer['same_2k_page_for_two_byte_encoding'] = page_eligible(row['site'],transfer['target'])
            transfers.append(transfer)
    def ranking(values):
        return [dict(name=k,**v) for k,v in sorted(values.items(),key=lambda item:(-item[1]['instruction_bytes'],item[0]))]
    return {'schema':1,'build_report_sha256':digest(report_path),'ihx_sha256':digest(image_path),
            'occupied_bytes':len(image),'main_bytes':main_bytes,'low_bytes':low_bytes,
            'map_code_areas':{k:{'start':v[0],'size':v[1]} for k,v in areas.items()},
            'map_code_area_size_sum':sum(v[1] for v in areas.values()),
            'map_area_unoccupied_addresses':{k:[a for a in range(v[0],v[0]+v[1]) if a not in image] for k,v in areas.items()},
            'validated_listing_instruction_bytes':len(occupied),'uncovered_bytes':len(set(image)-occupied),
            'listing_evidence':evidence,'module_ranking':ranking(modules),'function_label_ranking':ranking(functions),
            'direct_transfers':transfers,
            'generic_helper_calls':[t for t in transfers if t['kind'] in ('lcall','acall') and any('__gptr' in name for name in t['target_labels'])],
            'reachability_summary':{k:reach.get(k) for k in ('modules','functions','retained','removed_count')},
            'selection':{'mode':'explicit' if explicit else 'unique-suffix',
                         'ihx':image_path.relative_to(root).as_posix(),
                         'map':map_path.relative_to(root).as_posix(),
                         'reachability':reach_path.relative_to(root).as_posix()},
            'limitations':[('Selected listings are authenticated build-report artifacts.' if explicit else
              'Listing hashes bind this inventory snapshot, not the original build report: that report may not hash relocated listings.'),
              'Instruction spans are assembler-listed CODE rows with cycles, checked classic-8051 opcode lengths and matching IHX bytes; uncovered bytes include data, library code and missing listings.',
              'Function names are listing labels qualified by module; sizes count validated rows, not complete function extents. No ranking establishes complete function coverage.',
              'Direct transfers are byte-decoded only from covered rows. Computed jumps, loader entries, interrupt edges and external roots are not an exhaustive call graph.',
              'Two-byte page eligibility uses (site+2), assumes current placement and excludes linker relaxation, timing, stack and available-savings claims.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--report',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--ihx', help='Exact root-relative report artifact; requires --map and --reachability')
    parser.add_argument('--map', dest='map_file', help='Exact root-relative MAP report artifact')
    parser.add_argument('--reachability', help='Exact root-relative report artifact; its directory selects listings')
    args = parser.parse_args()
    try:
        result = inventory(args.root,args.report,ihx=args.ihx,map_file=args.map_file,reachability=args.reachability)
    except (ValueError,KeyError,OSError,TypeError) as exc:
        parser.exit(1,f'inventory refused: {exc}\n')
    args.output.write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
