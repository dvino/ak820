#!/usr/bin/env python3
"""Real SDCC/s51 check of all phases and the waveform's embedded CODE table."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
p=argparse.ArgumentParser(__doc__)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--sdcc',type=Path,required=True)
p.add_argument('--simulator',type=Path,required=True)
a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
root=Path(__file__).resolve().parents[2]
path=root/'keyboards/ajazz/ak820/ak820_rgb_shared.c';source=path.read_text()
start=source.index('uint8_t ak820_breathing_wave(uint8_t theta) __naked')
end=source.index('\n#else',start)
kernel=source[start:end]
start=source.index('uint8_t ak820_breathing_wave(uint8_t theta) {',end)
end=source.index('\n}',start)+2
reference=source[start:end].replace('ak820_breathing_wave','reference_wave')
table=[int(v.strip()) for line in re.findall(r'\.db ([0-9, ]+)',kernel) for v in line.split(',')]
assert table==[0,49,49,41,90,27,117,10]
assert re.search(r'ret\s+00923\$:\s+\.db',kernel)
assert kernel.count('movc a,@a+dptr')==2
main='''#include <stdint.h>
uint8_t ak820_breathing_wave(uint8_t);
uint8_t reference_wave(uint8_t);
__xdata __at(0x2000) uint8_t actual[256];
__xdata __at(0x2100) uint8_t expected[256];
__xdata __at(0x2200) uint8_t status;
void done(void) __naked { __asm ret __endasm; }
void main(void) {
    uint16_t i;
    status=0;
    for(i=0;i<256;++i) {
        actual[i]=ak820_breathing_wave(i);
        expected[i]=reference_wave(i);
        if(actual[i]!=expected[i]) {status=0xee;done();for(;;){}}
    }
    status=0xa5;done();for(;;){}
}
'''
for name,text in [('kernel','#include <stdint.h>\n'+kernel),('reference','#include <stdint.h>\n'+reference),('main',main)]:
    c=out/(name+'.c');c.write_text(text)
    subprocess.run([str(a.sdcc.resolve()),'-mmcs51','--model-large','--opt-code-size','-c',str(c),'-o',str(out/(name+'.rel'))],check=True)
image=out/'test.ihx'
subprocess.run([str(a.sdcc.resolve()),'-mmcs51','--model-large',*map(str,out.glob('*.rel')),'-o',str(image)],check=True)
mapping=image.with_suffix('.map').read_text()
address=int(re.search(r'^\s*C:\s*([0-9A-Fa-f]+)\s+_done\s',mapping,re.M)[1],16)
cmd=f'break 0x{address:x}\nrun\ndump xram 0x2000 0x2200\nquit\n'
r=subprocess.run([str(a.simulator.resolve()),'-t','8051','-c','-',str(image)],input=cmd,text=True,capture_output=True,timeout=30,check=True)
(out/'cpu.log').write_text(r.stdout+r.stderr)
rows=re.findall(r'^0x[0-9a-fA-F]+\s+((?:[0-9a-fA-F]{2}\s+)+)',r.stdout,re.M)
data=bytes.fromhex(' '.join(rows));assert len(data)==513 and data[-1]==0xa5,(len(data),data[-10:],r.stdout[-1500:])
assert data[:256]==data[256:512]
# An independent Python calculation also checks the compiled portable oracle.
coefficients=[0,49,49,41,90,27,117,10]
for theta in range(256):
    offset=((255-theta) if theta&0x40 else theta)&63
    fraction=(offset&15)+(1 if theta&0x40 else 0)
    section=(offset>>4)*2
    value=coefficients[section]+((coefficients[section+1]*fraction)>>4)
    expected=((128-value) if theta&0x80 else (128+value))&255
    assert data[theta]==expected,(theta,data[theta],expected)
report={'cases':256,'status':'PASS','production_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kernel_sha256':hashlib.sha256(kernel.encode()).hexdigest(),'fixture_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'cpu_log_sha256':hashlib.sha256((out/'cpu.log').read_bytes()).hexdigest(),'all_results':data[:256].hex(),'code_table':'Eight bytes remain in the kernel CODE section after RET; two MOVC reads index offsets0..7.'}
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: all256 phases match compiled portable fallback and independent integer reference; actual8051 CPU; no device access')
