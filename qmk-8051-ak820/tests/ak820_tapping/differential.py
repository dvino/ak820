"""Eligible QMK decision/output comparison, with the release-order difference explicit."""
import subprocess
import oracle

def compact_trace(exe,text):
    out=subprocess.check_output([str(exe),'--trace'],input=text,text=True)
    rows=[];final=None
    for line in out.splitlines():
        values=[int(x) for x in line.split()[1:]]
        if line.startswith('H '):rows.append((values[0],values[1],tuple(sorted(k for k in values[3:] if k))))
        elif line.startswith('F '):final=tuple(values)
    return rows,final

def qmk_reports(exe,text):
    keys=set();previous=(0,());reports=[];mods=layers=0
    for time,pos,down,taps,code,mods,layers in oracle.trace(exe,text):
        if code>=0x2000 and code<0x5000:
            key=(code&255) if taps else 0
        else:key=code
        if 4<=key<=0xa4:
            if down:keys.add(key)
            else:keys.discard(key)
        state=mods,tuple(sorted(keys))
        if state!=previous:reports.append((time,*state));previous=state
    return reports,(mods,layers)

def check(compact,work):
    qmk=oracle.build(work)
    traces=[]
    for code in [0x2004|(m<<8) for m in range(32)]+[0x4004|(l<<8) for l in range(6)]:
        for elapsed in (199,200,201):traces.append(f'M 0 {code:x}\nE 100 0 1\nE {100+elapsed} 0 0\n')
        traces.append(f'M 0 {code:x}\nM 1 5\nE 100 0 1\nE 110 1 1\nE 120 0 0\nE 130 1 0\n')
    traces += [
        'M 0 2204\nE 65500 0 1\nE 163 0 0\n',
        'M 0 2204\nE 65500 0 1\nT 164\nE 165 0 0\n',
        'M 0 2204\nE 100 0 1\nE 110 0 0\nE 120 0 1\nT 320\nE 321 0 0\n',
        'M 0 2204\nM 1 2105\nE 100 0 1\nE 110 1 1\nE 120 1 0\nE 130 0 0\n']
    for text in traces:
        actual=compact_trace(compact,text);expected=qmk_reports(qmk,text)
        assert actual==expected,(text,actual,expected)
    difference='M 0 e1\nM 1 2104\nE 100 0 1\nE 110 1 1\nE 120 0 0\nE 130 1 0\n'
    actual=compact_trace(compact,difference);expected=qmk_reports(qmk,difference)
    assert actual != expected
    assert (130,0,(4,)) in actual[0] and (130,2,(4,)) in expected[0]
    print(f'PASS: {len(traces)} eligible retained-QMK/compact HID traces; immediate old Shift release differs as specified')
    return {'eligible_traces':len(traces),'intentional_differences':['older Shift release accepted immediately before later MT tap']}
