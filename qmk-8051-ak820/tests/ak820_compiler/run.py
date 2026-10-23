#!/usr/bin/env python3
"""Offline SDCC Boolean-store regression. Never opens a device."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--sdcc', required=True, type=Path)
    p.add_argument('--s51', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--extra-flag', action='append', default=[])
    a=p.parse_args()
    a.sdcc=a.sdcc.resolve(); a.s51=a.s51.resolve()
    a.output.mkdir(parents=True, exist_ok=False)
    src=Path(__file__).with_name('fixture.c').resolve()
    command=[str(a.sdcc), '-mmcs51', '--std-sdcc11', '--model-large', '--opt-code-size', *a.extra_flag, str(src), '-o', 'fixture.ihx']
    r=subprocess.run(command,cwd=a.output,capture_output=True,text=True,timeout=90)
    (a.output/'compile.log').write_text(r.stdout+r.stderr)
    if r.returncode: raise RuntimeError('Compile/link failed; see compile.log')
    # Fixed instruction budget is bounded and cannot run board peripherals.
    sim='step 20000\necho @@RESULT\ndump xram 0x8000 0x801f 16\nquit\n'
    r=subprocess.run([str(a.s51),'-t','C52','-b','-c','-',str((a.output/'fixture.ihx').resolve())],input=sim,capture_output=True,text=True,timeout=20)
    log=r.stdout+r.stderr
    (a.output/'cpu.log').write_text(log)
    values={}
    for addr,data in re.findall(r'^0x([0-9a-f]+)\s+((?:[0-9a-f]{2}\s+)+)',log.rsplit('@@RESULT',1)[-1],re.M):
        for i,v in enumerate(data.split()): values[int(addr,16)+i]=int(v,16)
    expected=[0]*7+[18]+[1]*7+[19]
    actual=[values.get(0x8000+i) for i in range(16)]
    names=['near','xdata','generic-xdata','generic-near','comparison-return','record-comparison','record-bool-parameter','bitfield-preserve-count']
    cases=[dict(name=names[i%8],input=bool(i//8),expected=v,actual=actual[i],passed=actual[i]==v) for i,v in enumerate(expected)]
    complete=values.get(0x801f)==0xa5 and r.returncode==0
    report=dict(command=command,compiler_version=subprocess.check_output([str(a.sdcc),'--version'],text=True),compiler_sha256=hashlib.sha256(a.sdcc.read_bytes()).hexdigest(),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),complete=complete,cases=cases,passed=complete and all(c['passed'] for c in cases))
    (a.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return 0 if report['passed'] else 1

if __name__=='__main__': raise SystemExit(main())
