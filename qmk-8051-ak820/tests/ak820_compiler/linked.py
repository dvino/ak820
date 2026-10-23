#!/usr/bin/env python3
"""Inspect key-event Boolean bytes after executing the actual linked image."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re

p=argparse.ArgumentParser()
p.add_argument('--build',required=True,type=Path)
p.add_argument('--s51',required=True,type=Path)
p.add_argument('--output',required=True,type=Path)
a=p.parse_args()
if a.output.exists(): raise ValueError('Output directory must be new')
spec=importlib.util.spec_from_file_location('emitted',Path(__file__).parents[1]/'ak820_emitted'/'run.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
fw=m.Firmware(a.build.resolve(),a.s51.resolve(),a.output.resolve())
def unique(prefix):
    names=[s for s in fw.symbols if s.startswith(prefix)]
    if len(names)!=1: raise ValueError(f'Expected one retained symbol for {prefix}: {names}')
    return names[0]
matrix_asm=(a.build/'dce/quantum/keyboard.asm').read_text()
matrix_match=re.search(r'MAKE_KEYEVENT\(row, col, key_pressed\);.*?mov\s+dptr,#(_matrix_task_dummy_event_\w+)',matrix_asm,re.S)
if not matrix_match: raise ValueError('Missing retained matrix key-event factory')
matrix=matrix_match[1]
record=unique('_action_exec_record_')
commands=fw.initialize(); observations=[]; rows=[0]*16
for label,value,clock in [('press',8,100),('release',0,120)]:
    rows[1]=value
    commands+=fw.transition(rows,clock)
    for kind,symbol in [('matrix',matrix),('record',record)]:
        tag=kind+'_'+label
        commands+=fw.dump_symbol(tag,symbol,6)
        observations.append((tag,symbol,[3,1,clock+6,0,1,int(value!=0)]))
# Call both retained encoder branches. Inspect all four event objects after
# return, including both release records, instead of inferring stores from USB.
encoder_asm=(a.build/'dce/quantum/encoder.asm').read_text()
events=re.findall(r';\s*quantum/encoder.c:\d+: MAKE_ENCODER_(CW|CCW)_EVENT\(index, (true|false)\);(.*?)(?=;\s*quantum/encoder.c:)',encoder_asm,re.S)
if len(events)!=4: raise ValueError('Expected four retained encoder event factories')
for clockwise in [1,0]:
    commands+=fw.write('_encoder_exec_mapping_PARM_2',[clockwise])+fw.call('_encoder_exec_mapping',0)
for direction,pressed,body in events:
    symbols=re.findall(r'mov\s+dptr,#(_encoder_exec_mapping_dummy_event_\w+)',body)
    if len(set(symbols))!=1: raise ValueError('Cannot identify event factory object')
    symbol=symbols[0]; tag='encoder_'+direction+'_'+pressed
    commands+=fw.dump_symbol(tag,symbol,6)
    observations.append((tag,symbol,[0,0xfd if direction=='CW' else 0xfc,None,None,2 if direction=='CW' else 3,int(pressed=='true')]))
log,stack=fw.execute('linked-bool-stores',commands)
cases=[]
for tag,symbol,expected in observations:
    actual=fw.extract(log,tag,fw.address(symbol),6)
    # Matrix event timestamp can be the first or debounce frame; test the
    # actual Boolean and event identity, not scheduler-specific timestamp.
    if tag.startswith(('matrix_','record_')): expected[2:4]=[None,None]
    cases.append(dict(name=tag,symbol=symbol,address=fw.address(symbol),expected=expected,actual=actual,passed=all(e is None or e==v for e,v in zip(expected,actual))))
report=dict(image_sha256=hashlib.sha256(fw.image.read_bytes()).hexdigest(),cases=cases,stack=stack,passed=all(c['passed'] for c in cases))
(a.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['passed'] else 1)
