#!/usr/bin/env python3
"""Actual s51 same-TU slot writer, per-color wrapper and all-color loop check."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser(__doc__)
p.add_argument('--output',type=Path,required=True);p.add_argument('--sdcc',type=Path,required=True);p.add_argument('--simulator',type=Path,required=True)
a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
root=Path(__file__).resolve().parents[2];path=root/'keyboards/ajazz/ak820/ak820_board.c';source=path.read_text();config=(root/'keyboards/ajazz/ak820/config.h').read_text()
def function(signature):
 start=source.index(signature);return source[start:source.index('\n}',start)+2]
map_definition=re.search(r'^#define AK820_RGB_SLOT_MAP .*$',config,re.M)[0]
count_definition=re.search(r'^#define RGB_MATRIX_LED_COUNT .*$',config,re.M)[0]
header='''#include <stdint.h>
#define AK820_SCAN_ROWS 8
#define AK820_SCAN_COLS 16
#define AK820_LED_DMA_ADDRESS 0x0200
__sfr __at(0xe8) IE_EX;
__sbit __at(0xed) IE_PWM_I2C;
'''+map_definition+'\n'+count_definition+'\nconst __code uint8_t ak820_rgb_slots[]=AK820_RGB_SLOT_MAP;\n'
functions='\n'.join(function(s) for s in ['void ak820_set_slot_rgb(uint8_t slot,','void ak820_rgb_set_color(uint8_t index,','void ak820_rgb_set_color_all(uint8_t r,'])
main='''
__xdata __at(0x01ff) uint8_t dma_with_guards[514];
__xdata __at(0x0500) volatile uint8_t status;
__xdata __at(0x0501) volatile uint32_t cases;
static const __code uint8_t colors[][3]={{0,0,0},{255,0,0},{0,255,0},{0,0,255},{1,127,128},{254,255,1},{128,1,254},{255,255,255}};
void done(void) __naked { __asm ret __endasm; }
void main(void) {
    uint16_t index,j,base;
    uint8_t irq,other,color,ie,want,k;
    cases=0;status=0;
    for(index=0;index<256;++index) for(irq=0;irq<2;++irq) {
        for(j=0;j<514;++j) dma_with_guards[j]=0xa6;
        ie=0x8b|(irq<<5);IE_EX=ie;
        ak820_rgb_set_color(index,1,127,254);
        if(IE_EX!=ie) {status=0xe1;goto failed;}
        base=index<RGB_MATRIX_LED_COUNT ? 1+ak820_rgb_slots[index]*4:0xffff;
        for(j=0;j<514;++j) {
            want=0xa6;
            if(j>=base && j<base+4) {
                if(j==base) want=255;
                else if(j==base+1) want=1;
                else if(j==base+2) want=127;
                else want=254;
            }
            if(dma_with_guards[j]!=want) {status=0xe2;goto failed;}
        }
        ++cases;
    }
    for(irq=0;irq<2;++irq) for(other=0;other<2;++other) for(color=0;color<8;++color) {
        for(j=0;j<514;++j) dma_with_guards[j]=0xa6;
        ie=(other ? 0xdf:0)|(irq<<5);IE_EX=ie;
        ak820_rgb_set_color_all(colors[color][0],colors[color][1],colors[color][2]);
        if(IE_EX!=ie) {status=0xe3;goto failed;}
        for(j=0;j<514;++j) {
            want=0xa6;
            for(k=0;k<RGB_MATRIX_LED_COUNT;++k) {
                base=1+ak820_rgb_slots[k]*4;
                if(j>=base && j<base+4) {
                    want=(j==base) ? ((colors[color][0]|colors[color][1]|colors[color][2]) ? 255:0):colors[color][j-base-1];
                    break;
                }
            }
            if(dma_with_guards[j]!=want) {status=0xe4;goto failed;}
        }
        ++cases;
    }
    status=0xa5;
failed:
    done();for(;;){}
}
'''
c=out/'test.c';c.write_text(header+functions+main);image=out/'test.ihx'
subprocess.run([str(a.sdcc.resolve()),'-mmcs51','--model-large','--opt-code-size',str(c),'-o',str(image)],check=True)
mapping=image.with_suffix('.map').read_text();addr=int(re.search(r'^\s*C:\s*([0-9A-Fa-f]+)\s+_done\s',mapping,re.M)[1],16)
r=subprocess.run([str(a.simulator.resolve()),'-t','8051','-c','-',str(image)],input=f'break 0x{addr:x}\nrun\ndump xram 0x500 0x504\nquit\n',text=True,capture_output=True,timeout=60,check=True)
(out/'cpu.log').write_text(r.stdout+r.stderr);rows=re.findall(r'^0x0500\s+((?:[0-9a-fA-F]{2}\s+)+)',r.stdout,re.M);data=bytes.fromhex(' '.join(rows));assert data==bytes.fromhex('a5 20 02 00 00'),(data,r.stdout[-2000:])
report={'status':'PASS','cases':544,'scope':'Three production functions compiled together; all256 byteindices x IRQ0/1 plus32all-color combinations. Every DMA byte and adjacent guards verified; no interrupt preemption simulation.','production_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'fixture_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'generated_source_sha256':hashlib.sha256(c.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'cpu_log_sha256':hashlib.sha256((out/'cpu.log').read_bytes()).hexdigest()};(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS:544same-TU wrapper/all-color cases, fullDMA+guards andIE_EX checked; actual8051 CPU')
