#!/usr/bin/env python3
"""Compile the production kernel and immutable portable reference; compare on s51.

Standalone CPU fixture only; does not access a device or qualify linked firmware.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
p=argparse.ArgumentParser(__doc__)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--quick',action='store_true',help='Smoke check all hue regions on a 17-step grid')
p.add_argument('--sdcc',type=Path,required=True)
p.add_argument('--simulator',type=Path,required=True)
a=p.parse_args(); fixture_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
root=Path(__file__).resolve().parents[2]
header='''#include <stdint.h>
#include <stdbool.h>
#define AK820_BOARD
#define USE_CIE1931_CURVE
#define WS2812_BYTE_ORDER_GRB 1
#define WS2812_BYTE_ORDER_RGB 0
#define WS2812_BYTE_ORDER_BGR 2
#ifndef WS2812_BYTE_ORDER
#define WS2812_BYTE_ORDER 1
#endif
#define PROGMEM __code
#define pgm_read_byte(p) (*(p))
#if WS2812_BYTE_ORDER == 1
typedef struct {uint8_t g,r,b;} RGB;
#elif WS2812_BYTE_ORDER == 0
typedef struct {uint8_t r,g,b;} RGB;
#else
typedef struct {uint8_t b,g,r;} RGB;
#endif
typedef struct {uint8_t h,s,v;} HSV;
extern const __code uint8_t CIE1931_CURVE[];
void hsv_to_rgb_into(const HSV __xdata *,bool,RGB __xdata *);
RGB hsv_to_rgb_impl(HSV,bool);
'''
def strip(s): return re.sub(r'^#\s*include.*$','',s,flags=re.M)
source=header+strip((root/'quantum/color.c').read_text())
reference=strip((root/'tests/ak820_optimization/fixtures/color_rc4.c').read_text())
# The historical reference returns an aggregate; its CIE index is adjusted to
# the production curve in compact builds, while the HSV arithmetic is intact.
reference=reference.replace('CIE1931_CURVE[hsv.v]','CIE1931_CURVE[CIE_INDEX(hsv.v)]')
# This fixture uses the original curve only via an explicit value correction;
# reference conversion receives already-corrected v with use_cie=false.
reference=reference.replace('RGB rc4_hsv_to_rgb_impl(HSV hsv, bool use_cie) {','void rc4_hsv_to_rgb_impl(const HSV __xdata *in, bool use_cie, RGB __xdata *out) {\n    HSV hsv=*in;').replace('return rgb;','*out=rgb; return;')
reference=header+"#define CIE_INDEX(v) (v)\n"+reference
main=header+'''void rc4_hsv_to_rgb_impl(const HSV __xdata *,bool,RGB __xdata *);
__xdata HSV input;
__xdata RGB actual,expected;
__xdata uint8_t alias_buffer[5];
__xdata volatile uint8_t status;
__xdata volatile uint32_t cases;
void failed(void) __naked { __asm 02100$: sjmp 02100$ __endasm; }
static void check(uint8_t cie) {
    HSV ref=input;
    if(cie) {
#ifdef AK820_FULL_CIE
        ref.v=CIE1931_CURVE[ref.v];
#else
        ref.v=CIE1931_CURVE[ref.v >> 3];
#endif
    }
    rc4_hsv_to_rgb_impl(&ref,false,&expected);
    hsv_to_rgb_into(&input,cie,&actual);
    if(actual.r!=expected.r || actual.g!=expected.g || actual.b!=expected.b) {
        status=0xee;
        failed();
    }
    ++cases;
}
void finished(void) __naked { __asm ret __endasm; }
void main(void) {
    uint16_t h,s,v;
    uint8_t cie,i;
    static const __code uint8_t values[]={0,1,2,7,8,15,16,127,128,254,255};
    status=0;cases=0;
    for(cie=0;cie<2;++cie) {
        for(h=0;h<256;++h) for(s=0;s<256;++s) {
            input.h=h;input.s=s;
            for(i=0;i<sizeof(values);++i) {input.v=values[i];check(cie);}
        }
        for(h=0;h<256;++h) for(v=0;v<256;++v) {
            input.h=h;input.v=v; input.s=255;check(cie);
            input.s=0;check(cie);
        }
    }
    /* Every three-byte overlap: output begins before, at or after HSV. */
    for(h=0;h<256;++h) for(i=0;i<3;++i) {
        input.h=h;input.s=173;input.v=241;
        rc4_hsv_to_rgb_impl(&input,false,&expected);
        *(HSV __xdata *)&alias_buffer[1]=input;
        hsv_to_rgb_into((HSV __xdata *)&alias_buffer[1],false,(RGB __xdata *)&alias_buffer[i]);
        if(((RGB __xdata *)&alias_buffer[i])->r!=expected.r || ((RGB __xdata *)&alias_buffer[i])->g!=expected.g || ((RGB __xdata *)&alias_buffer[i])->b!=expected.b) {
            status=0xef;
            failed();
        }
    }
    status=0xa5;finished();
    for(;;) {}
}
'''
results=[]
for full,order in [(False,1),(True,1),(False,0),(False,2)]:
    label=f'{"full" if full else "compact"}-{order}';folder=out/label;folder.mkdir()
    flags=['-mmcs51','--model-large','--opt-code-size',f'-DWS2812_BYTE_ORDER={order}']+(['-DAK820_FULL_CIE'] if full else [])
    table=header+strip((root/'quantum/led_tables.c').read_text()).replace('const uint8_t CIE1931_CURVE','const __code uint8_t CIE1931_CURVE').replace(' PROGMEM','')
    # Narrow secondary layouts to representative coverage; all h/s plus value
    # edges execute in both curve modes using the production GRB layout.
    body=main if order==1 else main.replace('sizeof(values)','2').replace('h<256','h<16')
    if a.quick: body=body.replace('++h','h+=17').replace('++s','s+=17').replace('++v','v+=17')
    for name,text in [('kernel',source),('reference',reference),('table',table),('main',body)]:
        path=folder/(name+'.c');path.write_text(text)
        subprocess.run([str(a.sdcc.resolve()),*flags,'-c',str(path),'-o',str(folder/(name+'.rel'))],check=True)
    image=folder/'test.ihx'
    subprocess.run([str(a.sdcc.resolve()),*flags,*map(str,folder.glob('*.rel')),'-o',str(image)],check=True)
    mapping=image.with_suffix('.map').read_text()
    def addr(n):return int(re.search(r'^\s*(?:C:|D:)?\s*([0-9A-Fa-f]+)\s+_'+n+r'\s',mapping,re.M)[1],16)
    commands=f'break 0x{addr("finished"):x}\nbreak 0x{addr("failed"):x}\nrun\ndump xram 0x{addr("status"):x} 0x{addr("status")+4:x}\nquit\n'
    run=subprocess.run([str(a.simulator.resolve()),'-t','8051','-c','-',str(image)],input=commands,text=True,capture_output=True,timeout=900)
    (folder/'cpu.log').write_text(run.stdout+run.stderr)
    rows=re.findall(r'^0x[0-9a-fA-F]+\s+((?:[0-9a-fA-F]{2}\s+)+)',run.stdout,re.M)
    data=bytes.fromhex(' '.join(rows)); assert data and data[0]==0xa5,(label,data,run.stdout[-2000:])
    expected_count=(6656 if order==1 else 128) if a.quick else (1703936 if order==1 else 32768)
    assert int.from_bytes(data[1:5],'little')==expected_count,(label,data,expected_count)
    results.append({'configuration':label,'status':data.hex(),'differential_cases':expected_count,'alias_cases':3*((16 if order==1 else 1) if a.quick else (256 if order==1 else 16)),'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest()})
    print('PASS',label,flush=True)
report={'configurations':results,'production_sha256':hashlib.sha256((root/'quantum/color.c').read_bytes()).hexdigest(),'reference_sha256':hashlib.sha256((root/'tests/ak820_optimization/fixtures/color_rc4.c').read_bytes()).hexdigest(),'fixture_sha256':fixture_sha256,'compiler_version':subprocess.check_output([str(a.sdcc.resolve()),'--version'],text=True).splitlines()[0],'quick':a.quick}
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
