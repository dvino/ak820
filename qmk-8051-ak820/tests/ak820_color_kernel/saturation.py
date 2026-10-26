#!/usr/bin/env python3
"""Exhaust byte saturation inputs on actual s51 execution; no device access."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser(__doc__)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--sdcc',type=Path,required=True)
p.add_argument('--simulator',type=Path,required=True)
a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
root=Path(__file__).resolve().parents[2];path=root/'keyboards/ajazz/ak820/ak820_rgb.c';source=path.read_text()
kernels=[]
for name in ('add_sat','sub_sat'):
    start=source.index(f'static uint8_t {name}(uint8_t x, uint8_t y) __naked')
    end=source.index('\n}',start)+2;kernels.append(source[start:end])
main='''
__xdata __at(0x2000) volatile uint8_t status;
__xdata __at(0x2001) volatile uint32_t cases;
__xdata __at(0x2005) volatile uint8_t failed_x,failed_y,failed_result,failed_expected;
void done(void) __naked { __asm ret __endasm; }
void main(void) {
    uint16_t x,y,sum;
    uint8_t actual,expected;
    status=0;cases=0;
    for(x=0;x<256;++x) for(y=0;y<256;++y) {
        sum=x+y;expected=sum>255 ? 255:sum;
        actual=add_sat(x,y);
        if(actual!=expected) {status=0xe1;goto failed;}
        ++cases;
        expected=x<y ? 0:x-y;
        actual=sub_sat(x,y);
        if(actual!=expected) {status=0xe2;goto failed;}
        ++cases;
    }
    status=0xa5;done();for(;;){}
failed:
    failed_x=x;failed_y=y;failed_result=actual;failed_expected=expected;
    done();for(;;){}
}
'''
c=out/'test.c';c.write_text('#include <stdint.h>\n'+'\n'.join(kernels)+main)
image=out/'test.ihx'
subprocess.run([str(a.sdcc.resolve()),'-mmcs51','--model-large','--opt-code-size',str(c),'-o',str(image)],check=True)
mapping=image.with_suffix('.map').read_text();address=int(re.search(r'^\s*C:\s*([0-9A-Fa-f]+)\s+_done\s',mapping,re.M)[1],16)
r=subprocess.run([str(a.simulator.resolve()),'-t','8051','-c','-',str(image)],input=f'break 0x{address:x}\nrun\ndump xram 0x2000 0x2008\nquit\n',text=True,capture_output=True,timeout=60,check=True)
(out/'cpu.log').write_text(r.stdout+r.stderr)
rows=re.findall(r'^0x200[08]\s+((?:[0-9a-fA-F]{2}\s+)+)',r.stdout,re.M)
data=bytes.fromhex(' '.join(rows));assert data[:5]==bytes.fromhex('a5 00 00 02 00'),(data,r.stdout[-2000:])
report={'cases_per_operation':65536,'total_cases':131072,'status':'PASS','production_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kernel_sha256':hashlib.sha256('\n'.join(kernels).encode()).hexdigest(),'fixture_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'generated_source_sha256':hashlib.sha256(c.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'cpu_log_sha256':hashlib.sha256((out/'cpu.log').read_bytes()).hexdigest()}
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: all65536 bytepairs peroperation,131072 actual8051 comparisons against integer oracle; no device access')
