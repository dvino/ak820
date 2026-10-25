#!/usr/bin/env python3
"""Compile only maximal preprocessed tapping TU, before and after accessors."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--build-dir',type=Path,required=True); p.add_argument('--sdcc',type=Path,required=True)
a=p.parse_args(); here=Path(__file__).resolve().parent
pre=a.build_dir/'parameter-spills-metadata/ak820_tapping.i'
text=pre.read_text(); start=text.index('static uint8_t source_state['); end=text.index('static uint8_t pending',start)
s=(here.parents[1]/'keyboards/ajazz/ak820/ak820_tapping.c').read_text(); b=s.index('static uint8_t source_state['); e=s.index('static uint8_t pending',b)
replacement=s[b:e].replace('SOURCE_STATE_BYTES','SOURCES').replace('SOURCES','(16 * 8 + 2 * 1)').replace('SOURCE_STATE_MASK','31u')
flags=['-mmcs51','--model-large','--disable-warning','115','--disable-warning','85','--disable-warning','117','--disable-warning','190','--iram-size','0x0100','--xram-size','0x0c00','--xram-loc','0x0400','--code-size','0xc700','--opt-code-speed','-g','-Os','--std-sdcc11','--opt-code-size','--callee-saves','timer_read,timer_read32,ak820_nvm_ok,get_mods,get_weak_mods,matrix_get_row,readPin,eeprom_read_byte,eeprom_update_byte,ak820_flash_read,mDelaymS,get_repeat_key_count']
result={'candidate_sha256':hashlib.sha256(s.encode()).hexdigest(),'input_sha256':hashlib.sha256(pre.read_bytes()).hexdigest(),'flags':flags,'compiler_sha256':hashlib.sha256(a.sdcc.read_bytes()).hexdigest(),'areas':{}}
with tempfile.TemporaryDirectory(prefix='ak820-state-byte-size-') as d:
 for name,source in [('packed',text),('bytes',text[:start]+replacement+text[end:])]:
  work=Path(d)/name;work.mkdir();(work/'tapping.c').write_text(re.sub(r'^#line[^\n]*\n','',source,flags=re.M))
  subprocess.run([str(a.sdcc),*flags,'-c','tapping.c','-o','tapping.rel'],cwd=work,check=True)
  rel=(work/'tapping.rel').read_text()
  result['areas'][name]={k:int(n,16) for k,n in re.findall(r'^A (CSEG|DSEG|XSEG|OSEG) size ([0-9A-F]+)',rel,re.M)}
result['delta']={k:result['areas']['bytes'].get(k,0)-v for k,v in result['areas']['packed'].items()}
print(json.dumps(result,indent=2))
