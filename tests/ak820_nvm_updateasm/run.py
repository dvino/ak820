#!/usr/bin/env python3
"""Actual separate-TU SDCC/s51 comparison with frozen C updater; offline only."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--toolchain',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[2];qmk=root/'qmk-8051-ak820';out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
ref='''#include "ak820_nvm.h"
extern uint8_t eeprom_read_byte(const uint8_t *);
void reference(const void __xdata *buf,void *addr,size_t len) {
 const uint8_t __xdata *source=buf;uint16_t offset=(uint16_t)(uintptr_t)addr;size_t i;
 for(i=0;i<len;++i) {
  if(eeprom_read_byte((const uint8_t *)(uint16_t)(offset+i))!=source[i]) {
   ak820_eeprom_write_block_xdata(buf,addr,len);return;
  }
 }
}
'''
(out/'reference.c').write_text(ref)
h='''#include "ak820_nvm.h"
void reference(const void __xdata *,void *,size_t);
volatile __xdata __at(0x3000) uint8_t result[8];
static __xdata uint8_t buf[260];
static __xdata uint16_t reads[258], saved_reads[258];
static __xdata uint16_t count, calls, got_buf,got_addr,got_len;
static __xdata uint8_t got_tag, mutate, failure;
static __xdata uint16_t expected_count,expected_calls,expected_buf,expected_addr,expected_len;
static __xdata uint8_t expected_tag;
uint8_t eeprom_read_byte(const uint8_t *addr) {
 uint16_t off=(uint16_t)(uintptr_t)addr;
 reads[count]=off;
 /* A scalar read can change source before its comparison. */
 if(mutate)buf[count+1]=off<AK820_NVM_SIZE?(uint8_t)(off*13u+7u):0;
 ++count;return off<AK820_NVM_SIZE?(uint8_t)(off*13u+7u):0;
}
void ak820_eeprom_write_block_xdata(const void __xdata *b,void *addr,size_t len) {
 ++calls;got_buf=(uint16_t)b;got_addr=(uint16_t)(uintptr_t)addr;
 got_tag=((const __xdata uint8_t *)&addr)[2];got_len=len;
 /* Writer failures are observable here; no retry or delayed writer call. */
 if(failure)return;
 buf[259]=0x36;
}
static void reset(uint16_t start,uint16_t len,uint16_t mismatch) {
 uint16_t i;count=calls=got_buf=got_addr=got_len=got_tag=0;
 for(i=0;i<260;++i)buf[i]=0x5a;
 for(i=0;i<len;++i) {uint16_t off=start+i;buf[i+1]=off<AK820_NVM_SIZE?(uint8_t)(off*13u+7u):0;}
 if(mismatch<len)buf[mismatch+1]^=0x80;
}
static __xdata uint8_t tag,pass,sp_before;
static __xdata uint16_t start,len,mismatch;
static void * tagged(void) {
 void *p=(void *)start;((__xdata uint8_t *)&p)[2]=tag;return p;
}
static void probe(void) __naked {
 __asm
 push 0x00
 push 0x01
 mov r0,#0xa0
 mov r1,#0xa1
 mov a,sp
 mov dptr,#_sp_before
 movx @dptr,a
 lcall _invoke
 mov dptr,#_sp_before
 movx a,@dptr
 cjne a,0x81,00001$
 cjne r0,#0xa0,00001$
 cjne r1,#0xa1,00001$
 mov a,psw
 anl a,#0x18
 jz 00002$
00001$:
 mov dptr,#_pass
 clr a
 movx @dptr,a
00002$:
 pop 0x01
 pop 0x00
 ret
 __endasm;
}
void invoke(void) {ak820_eeprom_update_block_xdata(buf+1,tagged(),len);}
void done(void) __naked {__asm 00001$: sjmp 00001$ __endasm;}
static const __code uint16_t starts[]={0,31,63,64,127,10238,10239,10240,10241,0xfffe,0xffff};
static const __code uint16_t lengths[]={0,1,2,16,64,257};
void main(void) {
 uint8_t s,n,t,m,f,u;uint16_t i,cases=0;
 pass=1;
 for(s=0;s<11;++s)for(n=0;n<6;++n)for(t=0;t<4;++t)for(m=0;m<3;++m)for(f=0;f<2;++f)for(u=0;u<2;++u) {
 start=starts[s];len=lengths[n];tag=t*0x40;failure=f;mutate=u;
 mismatch=m==0?len:(m==1?0:(len?len-1:0));
 reset(start,len,mismatch);reference(buf+1,tagged(),len);
 expected_count=count;expected_calls=calls;expected_buf=got_buf;expected_addr=got_addr;expected_tag=got_tag;expected_len=got_len;
 for(i=0;i<count;++i)saved_reads[i]=reads[i];
 reset(start,len,mismatch);probe();
 if(!pass || count!=expected_count || calls!=expected_calls || got_buf!=expected_buf || got_addr!=expected_addr || got_tag!=expected_tag || got_len!=expected_len || buf[0]!=0x5a || buf[258]!=0x5a || buf[259]!=(calls&&!failure?0x36:0x5a))goto failed;
 for(i=0;i<count;++i)if(reads[i]!=saved_reads[i] || reads[i]!=(uint16_t)(start+i))goto failed;
 ++cases;
 }
 /* Maximum API length: first mismatch must forward 65535 unchanged. */
 start=0xffff;len=0xffff;tag=0xc0;mutate=0;failure=1;
 reset(start,1,0);reference(buf+1,tagged(),len);
 if(count!=1 || calls!=1 || got_len!=0xffff || got_tag!=0xc0)goto failed;
 reset(start,1,0);probe();
 if(!pass || count!=1 || calls!=1 || got_len!=0xffff || got_addr!=0xffff || got_tag!=0xc0)goto failed;
 ++cases;
 result[0]=0xa5;result[1]=cases;result[2]=cases>>8;done();
failed: result[0]=0xf0;result[1]=s;result[2]=n;result[3]=t;result[4]=m;result[5]=f;result[6]=u;result[7]=pass;done();
}
'''
(out/'harness.c').write_text(h)
flags=['-mmcs51','--model-large','--std-sdcc11','--opt-code-size','--callee-saves','eeprom_read_byte','-I'+str(qmk/'keyboards/ajazz/ak820')]
sdcc=str(a.toolchain/'bin/sdcc');logs=[]
for name,path,extra in [('reference',out/'reference.c',[]),('kernel',qmk/'keyboards/ajazz/ak820/ak820_nvm_update_block.c',['-DAK820_BOARD','-DAK820_NVM_UPDATE_BLOCK_ASM','-DAK820_READ_HOOK_PRESERVES_RN=1']),('harness',out/'harness.c',[])]:
 cmd=[sdcc,*flags,*extra,'-c',str(path),'-o',str(out/(name+'.rel'))];r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);logs.append(r.stdout);assert r.returncode==0,r.stdout
exe=out/'test.ihx';r=subprocess.run([sdcc,*flags,'--xram-loc','0x400','--xram-size','0x2000','--iram-size','0x100',*[str(out/(n+'.rel')) for n in ['harness','reference','kernel']],'-o',str(exe)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);logs.append(r.stdout);(out/'compile.log').write_text('\n'.join(logs));assert r.returncode==0,r.stdout
terminal=int(re.findall(r'^C:\s+([0-9A-Fa-f]+)\s+_done\s',exe.with_suffix('.map').read_text(),re.M)[0],16)
r=subprocess.run([str(a.toolchain/'bin/s51'),'-q','-c','-',str(exe)],input=f'break 0x{terminal:x}\nrun\ndx 0x3000 0x3007\nquit\n',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);(out/'cpu.log').write_text(r.stdout)
m=re.search(r'0x3000\s+((?:[0-9a-fA-F]{2}\s+){7}[0-9a-fA-F]{2})',r.stdout);assert m,r.stdout[-1500:];marker=bytes.fromhex(m[1]);assert marker[0]==0xa5,marker.hex()
def areas(name):return {k:int(v,16) for k,v in re.findall(r'^A (\w+) size ([0-9A-Fa-f]+)',(out/(name+'.rel')).read_text(),re.M)}
record={'pass':True,'cases':int.from_bytes(marker[1:3],'little'),'reference_areas':areas('reference'),'kernel_areas':areas('kernel'),'marker':marker.hex(),'limits':['Component mock scalar and writer only; no full firmware, IRQ, flash or device qualification'],'sha256':{str(p.relative_to(root)) if p.is_relative_to(root) else p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),qmk/'keyboards/ajazz/ak820/ak820_nvm_update_block.c',out/'reference.c',exe,a.toolchain/'bin/sdcc',a.toolchain/'bin/s51']}}
(out/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
