#!/usr/bin/env python3
"""Pinned-s51 DPTR-elision comparison, isolated from the existing spill proof."""
import argparse,hashlib,json,random,re,subprocess
from pathlib import Path

def memory(space,address,data):return f'set memory {space} {address:#x} '+' '.join(f'{v:#x}' for v in data)
def extract(log,label,address,count):
 tail=log.rsplit('@@'+label,1)[1];values={}
 for row,data in re.findall(r'^0x([0-9a-f]+)\s+((?:[0-9a-f]{1,2}\s+)+)',tail,re.M):
  for offset,value in enumerate(data.split()):values[int(row,16)+offset]=int(value,16)
  if all(address+i in values for i in range(count)):return bytes(values[address+i] for i in range(count))
 raise ValueError('Missing dump '+label)
def main():
 p=argparse.ArgumentParser();p.add_argument('--s51',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
 rng=random.Random(8051);commands=[];cases=[]
 for psw in range(256):
  for width in range(1,5):
   name=f'p{psw:02x}-w{width}';cases.append(name)
   iram=rng.randbytes(256);sfr=bytearray(128);sfr[1]=0x70;sfr[2:4]=rng.randbytes(2);sfr[0x50]=psw;sfr[0x60]=rng.randrange(256);sfr[0x70]=rng.randrange(256)
   # Same token-to-register assignment order as the generator, including
   # capture of incoming ACC before other assignments and final ACC parity.
   prefix=bytearray()
   if width==4:prefix+=bytes([0xff]) # mov r7,a
   for i,source in enumerate([0x82,0x83,0xf0][:min(width,3)]):prefix+=bytes([0xac+i,source])
   prefix+=bytes([0xec+width-1]) # mov a,r4..r7
   for variant in ('old','new'):
    code=prefix+(bytes.fromhex('9022ff') if variant=='old' else b'')+bytes.fromhex('901234')
    # Both executions stop at exactly the same PC.
    start=0x200-len(code)
    commands += [memory('rom',start,code),memory('iram',0,iram),memory('sfr',0x80,sfr[:0x19]),memory('sfr',0x9a,sfr[0x1a:]),memory('sfr',0x88,[0]),'fill xram 0x3000 0x30ff 0xa5',f'run {start:#x} 0x200']
    for space,address,count in [('iram',0,256),('sfr',128,128),('xram',0x3000,256)]:commands += [f'echo @@{name}-{variant}-{space}',f'dump /h {space} {address:#x} {address+count-1:#x} 16']
 script=a.output_dir/'dptr.sim';script.write_text('\n'.join(commands+['quit'])+'\n')
 run=subprocess.run([str(a.s51),'-t','C52','-b','-c','-'],input='exec '+json.dumps(str(script.resolve()))+'\n',text=True,capture_output=True,timeout=60)
 (a.output_dir/'dptr.log').write_text(run.stdout+'\n'+run.stderr)
 if run.returncode:raise RuntimeError('Simulator failed')
 chunks=re.split(r'^@@([^\n]+)\n',run.stdout,flags=re.M);observations={chunks[i]:chunks[i+1] for i in range(1,len(chunks)-1,2)}
 for name in cases:
  for space,address,count in [('iram',0,256),('sfr',128,128),('xram',0x3000,256)]:
   if extract('@@'+name+'-old-'+space+observations[name+'-old-'+space],name+'-old-'+space,address,count)!=extract('@@'+name+'-new-'+space+observations[name+'-new-'+space],name+'-new-'+space,address,count):raise AssertionError((name,space))
 result={'pass':True,'cases':len(cases),'executions':len(cases)*2,'all_256_initial_psw':True,'all_four_banks':True,'observations':['IRAM 256 bytes','SFR 128 bytes','XRAM 256 canaries','shared continuation PC 0x0200'],'s51_sha256':hashlib.sha256(a.s51.read_bytes()).hexdigest(),'scope':'existing equivalent replacement plus overwrite versus elided replacement plus identical overwrite; widths 1..4; ordinary foreground, disabled interrupts and timers; IRQ wrappers must preserve DPTR; time/cycle counts intentionally differ; not an original-spill or firmware qualification'}
 result['evidence_sha256']={str(path.name):hashlib.sha256(path.read_bytes()).hexdigest() for path in (Path(__file__),script,a.output_dir/'dptr.log')}
 (a.output_dir/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
