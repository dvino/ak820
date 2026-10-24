#!/usr/bin/env python3
"""Retain and verify whole-image runtime proofs for every named profile/variant."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tarfile

SOURCE = '1187d4cedd439733bd0c7ceb5c41daac9089de5b'
SHORT_REQUIRED = {'full-mouse-auto-shift-gui', 'full-auto-shift-dynamic-macro'}
FULL = {'full', 'full-os-indicators', 'full-mac-pc', 'full-mac-pc-os-indicators'}

def need(ok, why):
    if not ok:
        raise ValueError(why)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def sha(path):
    return digest(path.read_bytes())

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')

def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)

def expected(cf):
    return {(name, name in SHORT_REQUIRED) for name in cf.profiles.PROFILES} | {
        ('full', True), ('full-mouse-auto-shift', True)}

def variant(profile, short):
    return profile + ('-short' if short else '')

def frozen(root, name):
    return digest(git(root, 'show', SOURCE + ':' + name))

def report_from_log(path):
    text = path.read_text()
    start = text.find('\n{')
    need(start >= 0, 'Runtime log has no final JSON')
    return json.loads(text[start + 1:])

def retain(args, cf):
    root, final = args.root.resolve(), args.final_dir.resolve()
    rows = read(args.inputs)['builds']
    need(len(rows) == 23 and {(x['profile'], x['short_calls']) for x in rows} == expected(cf),
         'Expected all 21 named profiles and two additional short-call variants')
    need(not final.exists(), 'Refuse to overwrite retained runtime evidence')
    final.mkdir(parents=True)
    records = []
    for row in rows:
        profile, short = row['profile'], row['short_calls']
        build = Path(row['build_dir']).resolve()
        clone = build.parents[2]
        need((clone / 'qmk-8051-ak820').is_dir(), 'Cannot determine source checkout')
        need(git(clone, 'rev-parse', 'HEAD').decode().strip() == SOURCE and
             not git(clone, 'status', '--porcelain', '--untracked-files=normal').strip(),
             'Runtime build checkout is not clean frozen source')
        # Reinspect linked resources, source inputs and the runtime components in
        # their original checkout before retaining portable copies.
        oldroot, oldqmk = cf.ROOT, cf.QMK
        try:
            cf.ROOT, cf.QMK = clone, clone / 'qmk-8051-ak820'
            inspected = cf.inspect(build, args.toolchain)
            proof = read(build / 'runtime-safety/summary.json')
            cf.apply_runtime_safety(inspected, proof)
        finally:
            cf.ROOT, cf.QMK = oldroot, oldqmk
        c = (read(build / 'configuration-report.json') if row['full_regression']
             else report_from_log(Path(row['runtime_log'])))
        for key in ('configuration', 'identity', 'resources', 'runtime_analysis', 'short_calls'):
            need(c[key] == inspected[key], 'Stored/runtime inspection differs: ' + key)
        need(c['configuration']['profile'] == profile and bool(c['short_calls']) == short,
             'Unexpected variant identity')
        need(c.get('offline_tests_passed') is row['full_regression'], 'Regression scope differs')
        br = read(build / 'build-report.json')
        ident = c['identity']
        folder = final / variant(profile, short)
        folder.mkdir()
        prefix = next(Path(x['path']).parent.as_posix() for x in br['artifacts']
                      if x['path'].endswith('/ajazz_ak820_vial.ihx'))
        need(prefix == build.relative_to(clone / 'qmk-8051-ak820').as_posix(), 'Wrong archive prefix')
        names = {'build-report.json', 'runtime-stack.json'}
        names.update(x['path'][len(prefix)+1:] for x in br['artifacts'])
        need(all(x['path'].startswith(prefix + '/') for x in br['artifacts']), 'Escaping artifact')
        names.update(x['path'][len(prefix)+1:] for x in br['sources']
                     if x['origin'] == 'source' and x['path'].startswith(prefix + '/'))
        names.update(read(build / 'runtime-stack.json')['identity']['listing_sha256'])
        names.update(p.relative_to(build).as_posix() for p in (build/'runtime-safety').rglob('*') if p.is_file())
        # This subset retains every compiler artifact/source used by the runtime
        # proof, all relocated listings, and complete runtime CPU logs/scripts.
        archive = folder / 'runtime-artifacts.tar.xz'
        with tarfile.open(archive, 'w:xz', preset=6) as tf:
            for name in sorted(names):
                path = build / name
                need(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(build),
                     'Missing or escaping runtime artifact')
                tf.add(path, arcname=prefix + '/' + name, recursive=False)
        for name in ('ajazz_ak820_vial.ihx', 'ajazz_ak820_vial.map', 'ajazz_ak820_vial.mem',
                     'build-report.json', 'runtime-stack.json', 'runtime-safety/summary.json',
                     'runtime-safety/startup.json', 'runtime-safety/irq/results.json'):
            out = folder / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes((build / name).read_bytes())
        log_hashes = {}
        for label in ('build_log', 'runtime_log'):
            path = Path(row[label])
            out = folder / (label + '.txt')
            out.write_bytes(path.read_bytes())
            log_hashes[out.name] = sha(out)
        record = {'variant': variant(profile, short), 'profile': profile, 'short_calls': short,
                  'source': {'commit': SOURCE, 'dirty': False}, 'identity': ident,
                  'configuration': c['configuration'], 'resources': c['resources'],
                  'runtime': c['runtime_analysis'], 'full_regression': row['full_regression'],
                  'runtime_qualified': True, 'hardware_validated': False, 'release_approved': False,
                  'physical_device_commands': 0, 'archive_sha256': sha(archive),
                  'archive_bytes': archive.stat().st_size, 'logs': log_hashes}
        write(folder / 'record.json', record)
        records.append({'variant': record['variant'], 'record_sha256': sha(folder/'record.json')})
        print('RETAINED', record['variant'], flush=True)
    write(final / 'matrix.json', {'format': 'ak820-all-profile-runtime-1', 'source_commit': SOURCE,
          'named_profiles': 21, 'build_variants': 23, 'full_regression_variants': 4,
          'runtime_only_variants': 19,
          'full_regression_matrix_sha256': sha(root/'audits/rc6/web-firmware-20261024/final/matrix.json'),
          'hardware_validated': False, 'release_approved': False,
          'physical_device_commands': 0, 'variants': sorted(records, key=lambda x:x['variant'])})
    verify(args, cf)

def verify(args, cf):
    root, final = args.root.resolve(), args.final_dir.resolve()
    index = read(final / 'matrix.json')
    need(index['source_commit'] == SOURCE and index['named_profiles'] == len(cf.profiles.PROFILES) == 21
         and index['build_variants'] == 23 and index['full_regression_variants'] == 4
         and index['runtime_only_variants'] == 19, 'Wrong complete runtime matrix')
    for key in ('hardware_validated', 'release_approved'):
        need(index[key] is False, 'Invalid matrix approval')
    need(index['physical_device_commands'] == 0, 'Unexpected device command')
    files = sorted(final.glob('*/record.json'))
    need(len(files) == len(index['variants']) == 23, 'Missing/duplicate runtime row')
    indexed = {x['variant']: x['record_sha256'] for x in index['variants']}
    need(len(indexed) == 23, 'Duplicate index row')
    tracked = set(git(root, 'ls-tree', '-r', '--name-only', SOURCE).decode().splitlines())
    full_dir=root/'audits/rc6/web-firmware-20261024/final'
    need(sha(full_dir/'matrix.json')==index['full_regression_matrix_sha256'], 'Full regression matrix changed')
    actual, summaries = set(), []
    for path in files:
        folder, rec = path.parent, read(path)
        name = variant(rec['profile'], rec['short_calls'])
        need(name == folder.name == rec['variant'] and indexed.get(name) == sha(path), 'Record binding differs')
        actual.add((rec['profile'], rec['short_calls']))
        need(rec['source'] == {'commit':SOURCE,'dirty':False}, 'Non-frozen row')
        need(rec['configuration'] == cf.profiles.configuration(rec['profile']), 'Configuration differs')
        need(rec['runtime_qualified'] is True and rec['full_regression'] ==
             (rec['profile'] in FULL and not rec['short_calls']), 'Qualification scope differs')
        for key in ('hardware_validated','release_approved'):
            need(rec[key] is False, 'Invalid runtime approval')
        need(rec['physical_device_commands'] == 0, 'Unexpected device command')
        archive = folder / 'runtime-artifacts.tar.xz'
        need(sha(archive) == rec['archive_sha256'] and archive.stat().st_size == rec['archive_bytes'], 'Archive differs')
        with tarfile.open(archive) as tf:
            members=tf.getmembers()
            need(all(m.isfile() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts for m in members), 'Unsafe archive member')
            need(len(members) == len({m.name for m in members}), 'Duplicate archive member')
            payload={m.name:tf.extractfile(m).read() for m in members}
        prefixes={name.rsplit('/ajazz_ak820_vial.ihx',1)[0] for name in payload if name.endswith('/ajazz_ak820_vial.ihx')}
        need(len(prefixes)==1,'Ambiguous image');prefix=prefixes.pop()
        def raw(name):return payload[prefix+'/'+name]
        def hs(name, value):need(digest(raw(name))==value, 'Artifact hash differs: '+name)
        for item in folder.rglob('*'):
            if item.is_file() and item.name not in ('record.json','runtime-artifacts.tar.xz','build_log.txt','runtime_log.txt'):
                need(raw(item.relative_to(folder).as_posix())==item.read_bytes(), 'Loose/archive bytes differ')
        br=json.loads(raw('build-report.json'));ident=rec['identity'];r=rec['runtime']
        if rec['full_regression']:
            full=read(full_dir/rec['profile']/'record.json')
            need(full['identity']==ident and full['resources']==rec['resources'] and
                 full['runtime']==r and full['offline_tests_passed'] is True, 'Full regression image differs')
        need(br['configuration']==rec['configuration'],'Build configuration differs')
        need(bool(br['short_calls'])==rec['short_calls'],'Short-call configuration differs')
        for suffix in ('ihx','map','mem'):hs('ajazz_ak820_vial.'+suffix,ident[suffix+'_sha256'])
        hs('build-report.json',ident['build_report_sha256'])
        need(digest(cf.canonical(br['sources']))==ident['source_manifest_sha256'],'Source manifest differs')
        need(digest(cf.canonical(rec['configuration']))==ident['configuration_sha256'],'Configuration hash differs')
        need(ident['compiler_sha256']==br['compiler_sha256']==cf.SDCC46_PINS['sdcc'] and
             br['assembler_sha256']==cf.SDCC46_PINS['sdas8051'],'Unpinned compiler')
        for item in br['artifacts']:
            need(digest(payload[item['path']])==item['sha256'] and len(payload[item['path']])==item['size'],'Compiler artifact differs')
        for item in br['sources']:
            if item['origin']!='source':continue
            name=item['path']
            if name.startswith(prefix+'/'):need(digest(payload[name])==item['sha256'],'Generated source differs')
            elif 'qmk-8051-ak820/'+name in tracked:
                need(frozen(root,'qmk-8051-ak820/'+name)==item['sha256'],'Frozen source differs: '+name)
            else:
                need(name.startswith('lib/lufa/'),'Unexpected compiler source')
                lock=json.loads(git(root,'show',SOURCE+':qmk-8051-ak820/dependencies/lufa.json'))
                need(lock['required_files'][name.removeprefix('lib/lufa/')]==item['sha256'],'Unpinned LUFA source')
        need(r==json.loads(raw('runtime-safety/summary.json')) and r['identity']==ident, 'Runtime identity differs')
        need(r['source_files']==cf.runtime_source_snapshot(),'Runtime checker source set differs')
        for source,h in r['source_files'].items():need(frozen(root,source)==h,'Runtime checker not frozen')
        fg=json.loads(raw('runtime-stack.json'));start=json.loads(raw('runtime-safety/startup.json'));irq=json.loads(raw('runtime-safety/irq/results.json'))
        proof=cf.combine_runtime_safety(fg,start,irq,ident,rec['resources']['internal_ram'],r['source_files'])
        need(all(r[key]==value for key,value in proof.items()),'Runtime component contract differs')
        for report in r['reports'].values():hs(report['path'],report['sha256'])
        for label,h in r['logs'].items():hs('runtime-safety/'+label+'.log',h)
        for listing,h in fg['identity']['listing_sha256'].items():hs(listing,h)
        need(r['simulator_sha256']=='61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd', 'Unpinned simulator')
        need(r['passed'] and r['whole_program_stack_qualified'] and not r['unresolved_roots'], 'Unresolved/unqualified runtime')
        need(r['root_bounds']=={'_main':r['foreground_bound'],'_USB_DeviceInterrupt':6,'_ak820_led_irq':2,'_ak820_timer_irq':2},'Wrong roots')
        need(r['irq_bound']==61 and r['main_entry_frame_bound']==2 and r['pre_main_bound']==2,'Incomplete startup/IRQ bound')
        need(r['stack_bound']==r['foreground_bound']+63 and r['stack_margin']==r['stack_capacity']-r['stack_bound']>=0,'Stack overflow or incorrect total')
        orders={x for n in range(1,4) for x in itertools.permutations(('timer','usb','led'),n)}
        need(len(irq['ordered_nests'])==len(irq['cpu_cases'])==15 and
             {tuple(x['irq_order']) for x in irq['ordered_nests']}==orders and
             {tuple(x['irq_order']) for x in irq['cpu_cases']}==orders and
             all(x['canary_and_registers_preserved'] for x in irq['cpu_cases']) and
             irq['selector_cases']['input_values_checked']==256,'Incomplete IRQ CPU coverage')
        from pack_ak820 import read_ihex
        code=read_ihex(folder/'ajazz_ak820_vial.ihx');symbols=cf.linked_symbols(folder/'ajazz_ak820_vial.map')
        measured=cf.memory_report(code,symbols,(folder/'ajazz_ak820_vial.mem').read_text())
        cf.validate_startup(code,symbols)
        for key in ('code_bytes','code_windows','xram','protected_windows_clear'):
            need(measured[key]==rec['resources'][key],'Resource reconstruction differs: '+key)
        for key in ('static_bytes','initial_sp','stack_capacity'):
            need(measured['internal_ram'][key]==rec['resources']['internal_ram'][key],'IRAM reconstruction differs')
        need(rec['resources']['internal_ram']['stack_qualified'] is True and
             rec['resources']['internal_ram']['runtime_stack_bound']==r['stack_bound'] and
             rec['resources']['internal_ram']['stack_margin']==r['stack_margin'],'Resource/runtime mismatch')
        for log,h in rec['logs'].items():need(sha(folder/log)==h,'Command log differs')
        log=(folder/'runtime_log.txt').read_text()
        need(0<=log.find('RUN RUNTIME startup')<log.find('RUN RUNTIME irq'),'Missing runtime invocation order')
        summaries.append({'variant':rec['variant'],'profile':rec['profile'],'short_calls':rec['short_calls'],
                          'code':rec['resources']['code_bytes'],'xram':rec['resources']['xram']['bytes'],
                          'main':r['foreground_bound'],'crt':r['main_entry_frame_bound'],'irq':r['irq_bound'],
                          'bound':r['stack_bound'],'capacity':r['stack_capacity'],'margin':r['stack_margin'],
                          'full_regression':rec['full_regression']})
        print('VERIFIED', rec['variant'], r['stack_bound'], '/', r['stack_capacity'], flush=True)
    need(actual==expected(cf), 'Missing/extra supported variant')
    print(json.dumps({'validated':len(summaries),'minimum_stack_margin':min(x['margin'] for x in summaries),'rows':summaries},indent=2))
    return summaries

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=('retain','verify'))
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--final-dir',type=Path,required=True)
    p.add_argument('--inputs',type=Path)
    p.add_argument('--toolchain',type=Path)
    args=p.parse_args()
    sys.path.insert(0,str(args.root.resolve()/'tools'))
    import configure_firmware as cf
    for name in ('tools/configure_firmware.py',
                 'qmk-8051-ak820/util/ak820_profiles.py',
                 'qmk-8051-ak820/util/ak820_ci_authorization.py',
                 'qmk-8051-ak820/util/ak820_build_inputs.py'):
        need(frozen(args.root.resolve(),name)==sha(args.root/name),'Validator changed since freeze: '+name)
    if args.command=='retain':
        need(args.inputs and args.toolchain,'Retention needs inputs and toolchain')
        retain(args,cf)
    else:verify(args,cf)

if __name__=='__main__':
    main()
