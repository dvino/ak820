from pathlib import Path
import subprocess, json, os, hashlib
import argparse
parser=argparse.ArgumentParser(description="Compare production USB SETUP behavior with immutable baseline 4b83bb9.")
parser.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parents[3]/'qmk-8051-ak820')
parser.add_argument('--output-dir',type=Path)
args=parser.parse_args()
root=args.source_root.resolve(); out=(args.output_dir or root/'.build/protocol-usb-differential').resolve()
out.mkdir(parents=True,exist_ok=True);os.chdir(root)
ns={'__file__':str(root/'tests/ak820_usb/run.py')}
exec((root/'tests/ak820_usb/run.py').read_text().split('with tempfile.TemporaryDirectory')[0],ns)
original=subprocess.check_output(['git','show','4b83bb9:qmk-8051-ak820/tmk_core/protocol/ch555/usb_ak820.c'],text=True)
(out/'usb_control.c').write_text(original)
harness=(root/'tests/ak820_usb/test_usb.c').read_text(); harness=harness[:harness.index('int main(void)')]
main=r'''
static uint64_t hash = UINT64_C(1469598103934665603);
static void add(uint8_t x) { hash = (hash ^ x) * UINT64_C(1099511628211); }
static uint32_t rng = 0x954a3129;
static uint32_t next(void) { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }
int main(void) {
    static const uint16_t edges[] = {0,1,2,3,4,7,8,9,15,31,32,63,64,65,127,128,129,255,256,257,0x100,0x101,0x200,0x201,0x300,0x301,0x409,0xff00,0xffff};
    for (uint32_t n=0; n<2000000; ++n) {
        fresh();
        D0UsbConfig = next() & 1; USB_EnumStatus = D0UsbConfig;
        USB_SleepStatus = next() & 3;
        raw_state = next() % 5;
        for (uint8_t k=0;k<sizeof(input_snapshot);++k) input_snapshot[k]=(uint8_t)next();
        uint8_t type = n < 65536 ? n >> 8 : (uint8_t)next();
        uint8_t request = n < 65536 ? n : next() % 13;
        uint16_t value=edges[next() % (sizeof(edges)/sizeof(edges[0]))];
        uint16_t index=edges[next() % (sizeof(edges)/sizeof(edges[0]))];
        uint16_t length=edges[next() % (sizeof(edges)/sizeof(edges[0]))];
        setup(type,request,value,index,length);
        add(D0SetupReqCode); add(D0SetupLen); add(D0SetupLen >> 8);
        add(control_phase); add(control_zlp); add(raw_state); add(output_kind); add(output_report_id);
        add(D0UsbConfig); add(USB_EnumStatus); add(USB_SleepStatus); add(keyboard_protocol); add(keyboard_idle); add(keyboard_reset);
        add(D0_EP0RES); add(D0_EP0T_L); add(D0_EP1RES); add(D0_EP2RES); add(D0_EP3RES);
        for(uint8_t k=0;k<64;++k) add(pD0_EP0_BUF[k]);
    }
    printf("%016llx\n", (unsigned long long)hash);
}
'''
results={}
for label,src in [('control',out/'usb_control.c'),('candidate',root/'tmk_core/protocol/ch555/usb_ak820.c')]:
    test=out/(label+'_harness.c'); test.write_text(harness.replace('#include "../../tmk_core/protocol/ch555/usb_ak820.c"', '#include "'+str(src)+'"')+main)
    binary=out/label
    cmd=['cc','-std=gnu11','-w','-O2',*['-I'+x for x in ns['includes']],*['-D'+x for x in ns['defines']],str(test),'tmk_core/protocol/usb_descriptor.c','-o',str(binary)]
    subprocess.run(cmd,check=True)
    results[label]=subprocess.check_output([str(binary)],text=True).strip()
assert results['control']==results['candidate'],results
(out/'usb-differential.json').write_text(json.dumps({'cases_per_image':2000000,'results':results,'match':True,'candidate_sha256':hashlib.sha256((root/'tmk_core/protocol/ch555/usb_ak820.c').read_bytes()).hexdigest()},indent=2)+'\n')
print(results)
