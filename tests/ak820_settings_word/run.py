#!/usr/bin/env python3
"""Actual settings word/getter code in SDCC+s51, no device access."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--toolchain',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[2];qmk=root/'qmk-8051-ak820';out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);source=qmk/'keyboards/ajazz/ak820/ak820_settings.c'
asm=['push 0x%02x'%i for i in range(8)]+['mov a,sp','mov dptr,#_saved_sp','movx @dptr,a']+['mov r%d,#0x%02x'%(i,0xa0+i) for i in range(8)]
asm+=['mov dptr,#_ptr_value','movx a,@dptr','push acc','inc dptr','movx a,@dptr','mov dph,a','pop dpl','lcall _word','mov a,dpl','push acc','mov b,dph','mov dptr,#_received','pop acc','movx @dptr,a','inc dptr','mov a,b','movx @dptr,a','mov a,sp','mov dptr,#_saved_sp','movx a,@dptr','cjne a,0x81,00001$']
asm+=['cjne r%d,#0x%02x,00001$'%(i,0xa0+i) for i in range(8)]
asm+=['mov a,psw','anl a,#0x18','jnz 00001$','sjmp 00002$','00001$:','mov dptr,#_abi_failed','mov a,#1','movx @dptr,a','00002$:']+['pop 0x%02x'%i for i in reversed(range(8))]+['ret']
c='''#include <stdint.h>
#include <stdbool.h>
#include "'''+str(source)+'''"
#include "'''+str(qmk/'keyboards/ajazz/ak820/ak820_crc.c')+'''"
volatile __xdata __at(0x2000) uint8_t result[8];
static __xdata uint8_t work[258];
static uint8_t __xdata *ptr_value;
static __xdata uint16_t received;
static __xdata uint8_t saved_sp,abi_failed;
bool ak820_nvm_ok(void){return true;}
void ak820_nvm_begin(void){}
void ak820_nvm_end(void){}
void ak820_nvm_schema_fault(void){}
void clear_keyboard(void){}
void ak820_eeprom_read_block_xdata(void __xdata *b,const void *p,size_t n){b;p;n;}
void ak820_eeprom_update_block_xdata(const void __xdata *b,void *p,size_t n){b;p;n;}
void probe(void) __naked { __asm
'''+ '\n'.join(asm)+'''
__endasm; }
void done(void) __naked { __asm 00001$: sjmp 00001$ __endasm; }
void main(void){
 uint16_t v=0;uint8_t i,pos;for(i=0;i<8;++i)result[i]=0;abi_failed=0;
 do {
  pos=v;ptr_value=work+pos;work[pos]=v;work[(uint16_t)pos+1]=v>>8;
  probe();if(abi_failed || received!=v)goto failed;
  for(i=6;i<=14;i+=2){current[i]=v;current[i+1]=v>>8;}
  if(ak820_settings_combo_term()!=v || ak820_settings_tapping_term()!=v ||
     ak820_settings_tap_code_delay()!=v || ak820_settings_caps_delay()!=v ||
     ak820_settings_autoshift_timeout()!=v)goto failed;
 }while(++v);
 result[0]=0xa5;result[1]=0;done();
failed:result[0]=0xf0;result[1]=abi_failed?2:1;result[2]=v;result[3]=v>>8;result[4]=received;result[5]=received>>8;done();
}
'''
h=out/'harness.c';h.write_text(c);ihx=out/'harness.ihx';cmd=[str(a.toolchain/'bin/sdcc'),'-mmcs51','--model-large','--std-sdcc11','--opt-code-size','--iram-size','0x100','--xram-loc','0x400','--xram-size','0xc00','-I'+str(qmk/'keyboards/ajazz/ak820'),str(h),'-o',str(ihx)]
r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/'compile.log').write_text(r.stdout);assert r.returncode==0,r.stdout
pcs=re.findall(r'^C:\s+([0-9A-Fa-f]+)\s+_done\s',ihx.with_suffix('.map').read_text(),re.M);assert len(pcs)==1,pcs
terminal=int(pcs[0],16)
r=subprocess.run([str(a.toolchain/'bin/s51'),'-q','-c','-',str(ihx)],input=f'break 0x{terminal:x}\nrun\ndx 0x2000 0x2007\nquit\n',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);(out/'cpu.log').write_text(r.stdout);m=re.search(r'0x2000\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})',r.stdout);assert m,r.stdout[-1500:];status=bytes.fromhex(m[1]);assert status==bytes([0xa5,0,0,0,0,0,0,0]),status.hex()
d={'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sdcc_sha256':hashlib.sha256((a.toolchain/'bin/sdcc').read_bytes()).hexdigest(),'s51_sha256':hashlib.sha256((a.toolchain/'bin/s51').read_bytes()).hexdigest(),'pass':True,'direct_word_cases':65536,'compiled_c_getter_calls':327680,'cpu_marker':status.hex(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'ihx_sha256':hashlib.sha256(ihx.read_bytes()).hexdigest(),'limits':['Component CPU and ABI fixture, no full-image/IRQ qualification']};(out/'result.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
