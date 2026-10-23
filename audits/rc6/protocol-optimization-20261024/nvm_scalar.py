from pathlib import Path
import subprocess,json,os
import argparse
parser=argparse.ArgumentParser(description="Compare scalar/private block NVM behavior with immutable baseline 4b83bb9.")
parser.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parents[3]/'qmk-8051-ak820')
parser.add_argument('--output-dir',type=Path)
args=parser.parse_args()
root=args.source_root.resolve(); out=(args.output_dir or root/'.build/protocol-nvm-differential').resolve()
out.mkdir(parents=True,exist_ok=True);os.chdir(root)
files={'nvm':'keyboards/ajazz/ak820/ak820_nvm.c','driver':'drivers/eeprom/eeprom_driver.c'}
for key,path in files.items():
 (out/('control_'+key+'.c')).write_bytes(subprocess.check_output(['git','show','4b83bb9:qmk-8051-ak820/'+path]))
results={}
for variant in ['control','candidate']:
 sources=[str(out/('control_'+key+'.c')) if variant=='control' else path for key,path in files.items()]
 binary=out/('nvm_'+variant)
 subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-DEEPROM_CUSTOM','-DEEPROM_SIZE=0x2800','-DAK820_NVM_SCALAR_TEST',*(['-DCANDIDATE'] if variant=='candidate' else []),'-Ikeyboards/ajazz/ak820','-Idrivers/eeprom','-Iplatforms',str(Path(__file__).resolve().with_name('nvm_scalar.c')),*sources,'-o',str(binary)],check=True)
 results[variant]=subprocess.check_output([str(binary)],text=True).strip()
assert results['control']==results['candidate'],results
(out/'nvm-scalar-differential.json').write_text(json.dumps({'match':True,'results':results,'scope':'65536 addresses x byte/word/dword reads x uncached/dirty-cache/flushed states; flash read/program/erase ordered transcript, diagnostics, final complete flash image'},indent=2)+'\n')
print(results)
