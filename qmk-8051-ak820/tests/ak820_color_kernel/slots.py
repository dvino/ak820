#!/usr/bin/env python3
"""Execute the production slot writer in s51; no interrupt preemption/device test."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser(__doc__)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--sdcc',type=Path,required=True)
p.add_argument('--simulator',type=Path,required=True)
a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
root=Path(__file__).resolve().parents[2];path=root/'keyboards/ajazz/ak820/ak820_board.c';source=path.read_text()
start=source.index('void ak820_set_slot_rgb(uint8_t slot, uint8_t r, uint8_t g, uint8_t b) __naked')
end=source.index('\n}',start)+2;kernel=source[start:end]
native_header=(root/'lib/ch555/ch555.h').read_text()
assert re.search(r'SFR\(IE_EX,\s*0xE8\)',native_header)
assert re.search(r'SBIT\(IE_PWM_I2C,\s*0xE8,\s*5\)',native_header)
header='''#include <stdint.h>
#define AK820_SCAN_ROWS 8
#define AK820_SCAN_COLS 16
#define AK820_LED_DMA_ADDRESS 0x0200
__sfr __at(0xe8) IE_EX;
__sbit __at(0xed) IE_PWM_I2C;
'''
main=header+'''void ak820_set_slot_rgb(uint8_t,uint8_t,uint8_t,uint8_t);
__xdata __at(0x01ff) uint8_t dma_with_guards[514];
__xdata __at(0x0500) volatile uint8_t status;
__xdata __at(0x0501) volatile uint32_t cases;
static const __code uint8_t colors[][3]={{0,0,0},{255,0,0},{0,255,0},{0,0,255},{1,127,128},{254,255,1},{128,1,254},{255,255,255}};
void done(void) __naked { __asm ret __endasm; }
void main(void) {
    uint16_t slot,j,base;
    uint8_t irq,other,color,ie,want;
    cases=0;status=0;
    for(slot=0;slot<256;++slot) for(irq=0;irq<2;++irq)
    for(other=0;other<2;++other) for(color=0;color<8;++color) {
        for(j=0;j<514;++j) dma_with_guards[j]=0xa6;
        ie=(other ? 0xdf:0)|(irq<<5);IE_EX=ie;
        ak820_set_slot_rgb(slot,colors[color][0],colors[color][1],colors[color][2]);
        if(IE_EX!=ie) {status=0xe1;done();for(;;){}}
        base=1+slot*4;
        for(j=0;j<514;++j) {
            want=0xa6;
            if(slot<128 && j>=base && j<base+4) {
                if(j==base) want=(colors[color][0]|colors[color][1]|colors[color][2]) ? 255:0;
                else want=colors[color][j-base-1];
            }
            if(dma_with_guards[j]!=want) {status=0xe2;done();for(;;){}}
        }
        ++cases;
    }
    status=0xa5;done();for(;;){}
}
'''
# The masked MOVX interval must not modify carry between saving/restoring it.
interval=kernel.split('mov c,_IE_PWM_I2C')[1].split('mov _IE_PWM_I2C,c')[0]
instructions=[re.sub(r'\s+',' ',line.strip()) for line in interval.splitlines() if line.strip()]
assert all(line in {'clr _IE_PWM_I2C','movx @dptr,a','inc dptr','mov a,r2','mov a,r3','mov a,r4'} for line in instructions)
assert 'clr _IE_PWM_I2C' in interval
for name,text in [('kernel',header+kernel),('main',main)]:
    c=out/(name+'.c');c.write_text(text)
    subprocess.run([str(a.sdcc.resolve()),'-mmcs51','--model-large','--opt-code-size','-c',str(c),'-o',str(out/(name+'.rel'))],check=True)
image=out/'test.ihx'
subprocess.run([str(a.sdcc.resolve()),'-mmcs51','--model-large',*map(str,out.glob('*.rel')),'-o',str(image)],check=True)
mapping=image.with_suffix('.map').read_text();address=int(re.search(r'^\s*C:\s*([0-9A-Fa-f]+)\s+_done\s',mapping,re.M)[1],16)
r=subprocess.run([str(a.simulator.resolve()),'-t','8051','-c','-',str(image)],input=f'break 0x{address:x}\nrun\ndump xram 0x500 0x504\nquit\n',text=True,capture_output=True,timeout=300,check=True)
(out/'cpu.log').write_text(r.stdout+r.stderr)
rows=re.findall(r'^0x0500\s+((?:[0-9a-fA-F]{2}\s+)+)',r.stdout,re.M)
data=bytes.fromhex(' '.join(rows));assert data==bytes.fromhex('a5 00 20 00 00'),(data,r.stdout[-2000:])
report={'cases':8192,'status':'PASS','coverage':'All256 slots, IRQ enabled/disabled, other IE_EX bits allclear/allset, eight colors; each case checks full512-byte DMA and both adjacent guards. No interrupt preemption is simulated.','production_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kernel_sha256':hashlib.sha256(kernel.encode()).hexdigest(),'fixture_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'cpu_log_sha256':hashlib.sha256((out/'cpu.log').read_bytes()).hexdigest()}
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS:8192 actual8051 slot/color/IRQ cases; allDMAbytes+guards checked; IE_EX preserved; no device/preemption test')
