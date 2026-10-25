#!/usr/bin/env python3
"""Differential native IRQ traces; does not contact USB hardware."""
from pathlib import Path
import os, subprocess, tempfile
here = Path(__file__).resolve().parent
repo = here.parents[1]
qmk = repo/'qmk-8051-ak820'
ns = {'__file__': str(qmk/'tests/ak820_usb/run.py')}
source = (qmk/'tests/ak820_usb/run.py').read_text().split('with tempfile.TemporaryDirectory')[0]
exec(source, ns)
fixture = (qmk/'tests/ak820_usb/test_usb.c').read_text()
outputs = []
with tempfile.TemporaryDirectory(prefix='ep0-native-') as tmp:
    for name, path in [('before', here/'usb.before.c'), ('after', qmk/'tmk_core/protocol/ch555/usb_ak820.c')]:
        unit = fixture.replace('../../tmk_core/protocol/ch555/usb_ak820.c', str(path)).replace('int main(void)', 'int original_main(void)')
        c = Path(tmp)/(name+'.c'); c.write_text(unit+'\n'+(here/'trace.c').read_text())
        binary = Path(tmp)/name
        subprocess.run(['cc','-std=gnu11','-w','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer', *['-I'+str(qmk/x) for x in ns['includes']], *['-D'+x for x in ns['defines']], '-DAK820_OS_INDICATORS','-DAK820_MAC_PC', str(c), str(qmk/'tmk_core/protocol/usb_descriptor.c'),'-o',str(binary)],check=True)
        env = dict(os.environ, ASAN_OPTIONS='detect_leaks=0')
        output = subprocess.check_output([str(binary)],env=env,text=True)
        outputs.append(output); print(name,output)
    assert outputs[0] == outputs[1], 'differential trace mismatch'
print('PASS: baseline and candidate full fixture and 131072 IRQ traces match')
