#!/usr/bin/env python3
"""Compile the actual target NVM reader and check it in s51; no device access."""
import argparse, hashlib, json, os, re, subprocess, tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--toolchain',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[2];qmk=root/'qmk-8051-ak820';out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
source=qmk/'keyboards/ajazz/ak820/ak820_nvm.c'
# One physical CODE fixture covers every in-range EEPROM address. Its bytes
# differ from the cached-page pattern, detecting incorrect cache selection.
fixture=',\n'.join(','.join(str((((0xc700+i+j)*37)^((0xc700+i+j)>>8))&255) for j in range(min(32,0x2800-i))) for i in range(0,0x2800,32))
wrappers=[]
for name,target in [('probe_read','_read_offset'),('probe_eeprom','_eeprom_read_byte')]:
 asm=['push 0x%02x'%i for i in range(8)]
 asm+=['mov a,sp','mov dptr,#_saved_sp','movx @dptr,a']
 asm+=['mov r%d,#0x%02x'%(i,0xa0+i) for i in range(8)]
 asm+=['mov dptr,#_tag','movx a,@dptr','mov b,a','mov dptr,#_test_addr','movx a,@dptr','push acc','inc dptr','movx a,@dptr','mov dph,a','pop dpl','lcall '+target,'mov b,dpl']
 asm+=['mov a,sp','mov dptr,#_saved_sp','movx a,@dptr','cjne a,0x81,00001$']
 asm+=['cjne r%d,#0x%02x,00001$'%(i,0xa0+i) for i in range(8)]
 asm+=['mov a,psw','anl a,#0x18','jnz 00001$','sjmp 00002$','00001$:','mov dptr,#_abi_failed','mov a,#1','movx @dptr,a','00002$:','mov dptr,#_value','mov a,b','movx @dptr,a']
 asm+=['pop 0x%02x'%i for i in reversed(range(8))]+['ret']
 wrappers.append('void '+name+'(void) __naked { __asm\n'+'\n'.join(asm)+'\n__endasm; }')
c='''#include <stdint.h>
#include <stdbool.h>
#define AK820_BOARD 1
#include "'''+str(source)+'''"
volatile __xdata __at(0x2000) uint8_t result[8];
static __xdata uint16_t test_addr;
static __xdata uint8_t tag,value,saved_sp,abi_failed;
__code __at(0xc700) const uint8_t physical[0x2800]={'''+fixture+'''};
uint8_t ak820_flash_read(uint16_t a) { return *((const __code uint8_t *)a); }
bool ak820_flash_erase(uint16_t a) { a; result[1]=0xee; return false; }
bool ak820_flash_program(uint16_t a,uint8_t v) { a;v;result[1]=0xee;return false; }
bool ak820_flash_program_page(uint16_t a,const uint8_t __xdata *v) { a;v;result[1]=0xee;return false; }
void ak820_macro_init(void) {}
'''+ '\n'.join(wrappers)+'''
static uint8_t expected(uint16_t a) {
 if(a>=AK820_NVM_SIZE) return 0;
 if(page_valid && (a/64)==cached_page) return (uint8_t)((a%64)^0xad);
 a+=0xc700; return (uint8_t)((a*37u)^(a>>8));
}
static bool check(void) {
 uint8_t e=expected(test_addr);
 probe_read(); if(abi_failed || value!=e) return false;
 probe_eeprom(); if(abi_failed || value!=e) return false;
 return true;
}
static __xdata uint8_t xbuf[18];
static __idata uint8_t ibuf[18];
static const __code uint16_t starts[9]={0,31,63,64,127,8191,10239,10240,65535};
static const __code uint8_t lengths[4]={0,1,2,16};
static bool check_blocks(void) {
 uint8_t valid,s,n,i,len;uint16_t start;uint8_t e;
 for(valid=0;valid<2;++valid) {
  page_valid=valid;cached_page=1;page_dirty=true;storage_failed=true;
  for(s=0;s<9;++s) for(n=0;n<4;++n) {
   start=starts[s];len=lengths[n];
   for(i=0;i<18;++i){xbuf[i]=0x5a;ibuf[i]=0x5a;}
   eeprom_read_block(xbuf+1,(const void *)start,len);
   eeprom_read_block(ibuf+1,(const void *)start,len);
   for(i=0;i<18;++i) {
    e=(i>0 && i<=len)?(((uint32_t)start+i-1>=AK820_NVM_SIZE)?0:expected(start+i-1)):0x5a;
    if(xbuf[i]!=e || ibuf[i]!=e)return false;
   }
   for(i=0;i<18;++i)xbuf[i]=0x5a;
   ak820_eeprom_read_block_xdata(xbuf+1,(const void *)start,len);
   for(i=0;i<18;++i) {
    e=(i>0 && i<=len)?(((uint32_t)start+i-1>=AK820_NVM_SIZE)?0:expected(start+i-1)):0x5a;
    if(xbuf[i]!=e)return false;
   }
  }
 }
 return true;
}
void done(void) __naked { __asm 00001$: sjmp 00001$ __endasm; }
void main(void) {
 uint8_t page,i;uint16_t offset;uint32_t count=0;
 for(i=0;i<8;++i)result[i]=0;abi_failed=0;
 for(i=0;i<64;++i)page_data[i]=i^0xad;
 page_valid=false;page_dirty=false;storage_failed=false;tag=0;
 offset=0; do {test_addr=offset;tag=(offset&3)<<6;if(!check())goto failed;++count;}while(++offset);
 page=0;do {page_valid=true;cached_page=page;page_dirty=(page&1)!=0;storage_failed=(page&2)!=0;
  for(i=0;i<64;++i){test_addr=(uint16_t)page*64+i;tag=(i&3)<<6;if(!check())goto failed;++count;}
 }while(++page);
 /* Each cache page must reject a different in-range page, including wrap. */
 page=0;do {cached_page=page;test_addr=((uint16_t)(uint8_t)(page+1))*64+31;if(!check())goto failed;++count;}while(++page);
 page_valid=true;cached_page=1;tag=0;do {test_addr=85;if(!check())goto failed;++count;test_addr=0x123;if(!check())goto failed;++count;}while(++tag);
 if(!check_blocks())goto failed;
 result[0]=0xa5;result[2]=(uint8_t)count;result[3]=(uint8_t)(count>>8);result[4]=(uint8_t)(count>>16);done();
failed:
 result[0]=0xf0;result[1]=abi_failed?2:1;result[5]=test_addr;result[6]=test_addr>>8;result[7]=value;done();
}
'''
c+='\n#include \"'+str(qmk/'keyboards/ajazz/ak820/ak820_crc.c')+'\"\n'
h=out/'harness.c';h.write_text(c);exe=out/'harness.ihx';cmd=[str(a.toolchain/'bin/sdcc'),'-mmcs51','--model-large','--std-sdcc11','--opt-code-size','--iram-size','0x100','--xram-loc','0x400','--xram-size','0xc00','--code-size','0x10000',str(h),'-I'+str(qmk/'keyboards/ajazz/ak820'),'-o',str(exe)]
r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/'compile.log').write_text(r.stdout);assert r.returncode==0,r.stdout
# Bounded execution; a missing terminal marker is failure, including timeout.
pcs=re.findall(r'^C:\s+([0-9A-Fa-f]+)\s+_done\s',exe.with_suffix('.map').read_text(),re.M);assert len(pcs)==1,pcs
terminal=int(pcs[0],16)
s=subprocess.run([str(a.toolchain/'bin/s51'),'-q','-c','-',str(exe)],input=f'break 0x{terminal:x}\nrun\ndx 0x2000 0x2007\nquit\n',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);(out/'cpu.log').write_text(s.stdout)
m=re.search(r'0x2000\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})',s.stdout);assert m,s.stdout[-2500:];status=bytes.fromhex(m[1]);assert status[:5]==bytes([0xa5,0,0,0x43,1]),status.hex()
record={'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sdcc_sha256':hashlib.sha256((a.toolchain/'bin/sdcc').read_bytes()).hexdigest(),'s51_sha256':hashlib.sha256((a.toolchain/'bin/s51').read_bytes()).hexdigest(),'pass':True,'cases_per_entry':82688,'compiled_c_block_calls':216,'entry_points':2,'cpu_marker':status.hex(),'nvm_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'ihx_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'limits':['Component CPU fixture; no IRQ/whole-firmware qualification','Flash writes stubbed and forbidden; CODE and cache reads exercised']};(out/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
