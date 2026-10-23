#!/usr/bin/env python3
"""Compile the retained QMK tapping state machine; run offline traces.

Only action_tapping.c is executed as reference production logic. The adapter
models mapping, action decoding and output state; mask/layer assertions describe
that adapter, not the firmware decoder or HID pipeline. No layer-sensitive map,
cache mutation, modifier ownership, encoder, cancellation or CPU timing is proved.
The upstream eight-slot queue (seven usable) still clears state on overflow;
these short traces exclude overflow and reject an observed overflow marker.
The compact contract intentionally processes older modifier releases immediately,
whereas this reference queues them. Therefore full equivalence is not claimed.
"""
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
Q = ROOT / 'quantum'

def build(directory, mutation=None):
    directory = pathlib.Path(directory)
    source = (Q / 'action_tapping.c').read_text()
    if mutation:
        source = mutation(source)
    # Only includes are removed. Every executable engine statement is retained.
    (directory / 'retained_engine.inc').write_text(re.sub(r'^#include .*\n', '', source, flags=re.M))
    out = directory / 'qmk-tapping-oracle'
    subprocess.run(['cc', '-std=c99', '-O0', '-Wall', '-Wextra', '-Wno-type-limits',
                    '-I', str(Q), '-I', str(directory),
                    str(pathlib.Path(__file__).with_name('oracle_harness.c')), '-o', str(out)], check=True)
    return out

def trace(exe, text):
    result = subprocess.run([str(exe)], input=text, text=True, capture_output=True, check=True)
    if 'OVERFLOW' in result.stdout:
        raise AssertionError('upstream queue overflow: oracle trace is outside eligible boundary')
    return [tuple(int(x, 16 if i in (4, 5, 6) else 10) for i, x in enumerate(line.split()))
            for line in result.stdout.splitlines()]

def check(exe):
    count = 0
    for elapsed in (199, 200, 201):
        rows = trace(exe, f'M 0 2204\nE 100 0 1\nE {100+elapsed} 0 0\n')
        assert [r[3] for r in rows] == ([1, 1] if elapsed == 199 else [0, 0]), rows
        count += 1
    rows=trace(exe,'M 0 2204\nE 65500 0 1\nE 163 0 0\n')
    assert [r[3] for r in rows]==[1,1]; count+=1
    rows=trace(exe,'M 0 2204\nE 65500 0 1\nT 164\nE 165 0 0\n')
    assert [r[3] for r in rows]==[0,0]; count+=1
    for mask in range(32):
        rows=trace(exe,f'M 0 {0x2004|(mask<<8):x}\nE 100 0 1\nT 300\nE 301 0 0\n')
        assert rows[0][5]==(mask&15)<<(4 if mask&16 else 0) and rows[-1][5]==0, rows
        count+=1
    for layer in range(6):
        rows=trace(exe,f'M 0 {0x4004|(layer<<8):x}\nM 1 5\nE 100 0 1\nE 110 1 1\nE 120 0 0\nE 130 1 0\n')
        assert [r[1] for r in rows]==[0,1,0,1] and rows[0][3]==0 and rows[1][6]==1<<layer and rows[-1][6]==0,rows
        count+=1
    rows=trace(exe,'M 0 2204\nM 1 2105\nE 100 0 1\nE 110 1 1\nE 120 1 0\nE 130 0 0\n')
    assert [(r[1],r[3]) for r in rows]==[(0,0),(1,1),(1,1),(0,0)], rows;count+=1
    rows=trace(exe,'M 0 2204\nE 100 0 1\nE 110 0 0\nE 120 0 1\nT 320\nE 321 0 0\n')
    assert [r[3] for r in rows]==[1,1,0,0], rows;count+=1
    rows=trace(exe,'M 0 e1\nM 1 2104\nE 100 0 1\nE 110 1 1\nE 120 0 0\nE 130 1 0\n')
    assert [(r[1],r[2],r[5]) for r in rows]==[(0,1,2),(1,1,2),(0,0,0),(1,0,0)],rows
    count+=1
    print(f'PASS: {count} retained-QMK timing/adapter traces; older Shift release is intentionally queued')

def negative_control():
    # A deliberately wrong deadline must fail the same public timing checks.
    with tempfile.TemporaryDirectory(prefix='ak820-qmk-negative-') as tmp:
        exe = build(tmp, lambda s: s.replace('< GET_TAPPING_TERM(', '<= GET_TAPPING_TERM('))
        try:
            check(exe)
        except AssertionError:
            print('PASS: wrong 200 ms deadline negative control rejected')
        else:
            raise AssertionError('deadline negative control escaped')

if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='ak820-qmk-oracle-') as tmp:
        check(build(tmp))
    negative_control()
