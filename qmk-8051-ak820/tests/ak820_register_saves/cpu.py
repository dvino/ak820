#!/usr/bin/env python3
"""Real pinned SDCC/aslink/s51 differential fixture; no device access."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'util'))
import ak820_register_saves as trim
from test_register_saves import ASM
root=Path(sys.argv[1]);root.mkdir(parents=True,exist_ok=False)
source=root/'input';(source/'quantum').mkdir(parents=True)
asm=source/'quantum/test.asm';asm.write_text(ASM.replace('mov a,#42','push ar2\n\tmov a,r2\n\tpop ar2\n\tmov a,#42\n\tjz 00100$').replace('\tret\n; function caller','00100$:\n\tret\n; function caller').replace(' ar0 = 0x00',' ar2 = 0x02\n ar0 = 0x00').replace('\t.area CSEG','\t.globl _caller\n\t.globl _leaf\n\t.area CSEG'))
assembler=os.environ['AK820_ASSEMBLER']
def assemble(path):subprocess.run([assembler,'-plosgffw',str(path.with_suffix('.rel')),str(path)],check=True)
assemble(asm)
r=trim.prepare(source,root/'output',root/'report.json');other=root/'output/quantum/test.asm';assemble(other)
trim.verify_assembled(source,root/'output',root/'report.json',r)
main=root/'fixture.c'
main.write_text('''void main(void) { __asm
 mov sp,#0x60
 mov r0,#0x10
 mov r1,#0x21
 mov r2,#0x32
 mov r3,#0x43
 mov r4,#0x54
 mov r5,#0x65
 mov r6,#0x76
 mov r7,#0x87
 lcall _caller
 mov 0x30,a
 mov 0x31,dpl
 mov dptr,#0x2000
 mov a,r0
 movx @dptr,a
 inc dptr
 mov a,r1
 movx @dptr,a
 inc dptr
 mov a,r2
 movx @dptr,a
 inc dptr
 mov a,r3
 movx @dptr,a
 inc dptr
 mov a,r4
 movx @dptr,a
 inc dptr
 mov a,r5
 movx @dptr,a
 inc dptr
 mov a,r6
 movx @dptr,a
 inc dptr
 mov a,r7
 movx @dptr,a
 inc dptr
 mov a,0x30
 movx @dptr,a
 inc dptr
 mov a,0x31
 movx @dptr,a
 inc dptr
 mov a,sp
 movx @dptr,a
 00100$:
 sjmp 00100$
 __endasm; }
''')
results={}
for label,obj in [('before',asm.with_suffix('.rel')),('after',other.with_suffix('.rel'))]:
    ihx=root/(label+'.ihx')
    subprocess.run(['sdcc','-mmcs51','--model-large',str(main),str(obj),'-o',str(ihx)],check=True)
    mapping=ihx.with_suffix('.map').read_text()
    address=int(re.search(r'^\s*C:\s*([0-9A-Fa-f]+)\s+_leaf\s',mapping,re.M)[1],16)
    commands=f'break 0x{address:x}\nrun\ndump sfr 0x81 0x81\nstep 1000\ndump xram 0x2000 0x200a\nquit\n'
    out=subprocess.run(['s51','-t','8051','-c','-',str(ihx)],input=commands,text=True,capture_output=True,timeout=20,check=True).stdout
    (root/(label+'.cpu.log')).write_text(out)
    sp=re.findall(r'^0x81 SP:.*?0x([0-9a-fA-F]{2})\b',out,re.M)
    rows=re.findall(r'^0x200[08]\s+((?:[0-9a-fA-F]{2}\s+)+)',out,re.M)
    data=bytes.fromhex(' '.join(rows))
    assert data==bytes.fromhex('10 21 32 43 54 65 76 87 2a 2a 60'),(label,data,out)
    assert sp,(label,out)
    results[label]={'leaf_sp':int(sp[0],16),'output':data.hex(),'ihx_sha256':trim.sha(ihx),'cpu_log_sha256':trim.sha(root/(label+'.cpu.log'))}
assert results['before']['leaf_sp']-results['after']['leaf_sp']==2,results
results['provenance']={'pass_sha256':trim.sha(Path(trim.__file__)),'fixture_sha256':trim.sha(Path(__file__)),'assembly_input_sha256':trim.sha(asm),'c_fixture_sha256':trim.sha(main),'compiler_version':subprocess.check_output(['sdcc','--version'],text=True).splitlines()[0],'assembler_sha256':trim.sha(Path(assembler))}
(root/'cpu-result.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS real SDCC/aslink/s51: eight register canaries, return A/DPL, restored SP, leaf SP reduced by two; component CPU fixture only')
