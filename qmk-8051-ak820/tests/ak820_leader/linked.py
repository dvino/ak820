#!/usr/bin/env python3
"""Exact linked Leader ownership scenarios; no device access."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('tap',ROOT/'tests/ak820_tapping/emitted.py')
tap=importlib.util.module_from_spec(spec);spec.loader.exec_module(tap)
class Trace(tap.Trace):
 def __init__(self,fw,name):
  super().__init__(fw,name);self.map((0,0),0x7c58);self.map((0,1),0x1e);self.map((0,2),4)
 def memory(self,label,symbol,value):self.check_memory(label,symbol,0,value)
 def result(self):
  r=self.run();r['pass']=r.pop('pass_');return r
 def lead(self):self.event((0,0),1,100);self.event((0,0),0,101)
 def select(self):self.event((0,1),1,120);self.event((0,1),0,121)
def cases(fw):
 for i in range(16):
  t=Trace(fw,'leader-selector-'+str(i));t.map((0,1),0x1e+i if i<10 else 4+i-10);t.lead();t.event((0,1),1,120);t.memory('slot','_leader_pending',[i]);t.event((0,1),0,121);t.check('consumed',tap.packet());t.tick(122);t.memory('dispatched','_leader_pending',[255]);yield t.result()
 t=Trace(fw,'leader-preheld-release');t.event((0,2),1,90);t.lead();t.event((0,2),0,110);t.check('released',tap.packet());t.memory('still-waiting','_leader_waiting',[1]);yield t.result()
 t=Trace(fw,'leader-timeout');t.lead();t.event((0,2),1,400);t.check('normal-key',tap.packet(0,4));t.event((0,2),0,401);t.check('normal-release',tap.packet());yield t.result()
 t=Trace(fw,'leader-wrap');t.event((0,0),1,65520);t.event((0,0),0,65521);t.event((0,1),1,20);t.memory('selected','_leader_pending',[0]);yield t.result()
 t=Trace(fw,'leader-clear-held');t.event((0,0),1,100);t.event((0,1),1,120);t.commands+=fw.call('_clear_keyboard');t.event((0,0),0,130);t.event((0,1),0,131);t.tick(132);t.memory('cancelled','_leader_pending',[255]);t.check('empty',tap.packet());yield t.result()
 t=Trace(fw,'leader-oneshot-retained');t.map((0,3),0x52a2);t.event((0,3),1,80);t.event((0,3),0,81);t.lead();t.select();t.tick(122);t.memory('queued','_ak820_oneshot_mods',[2]);t.event((0,2),1,130);t.memory('consumed','_ak820_oneshot_mods',[0]);t.check('shifted',tap.packet(2,4));t.event((0,2),0,131);t.check('released',tap.packet());yield t.result()
 t=Trace(fw,'leader-nonempty-macro-oneshot');t.macro([1,2,29,1,3,29]);t.map((0,3),0x52a2);t.event((0,3),1,80);t.event((0,3),0,81);t.lead();t.select();t.tick(122);t.memory('retained-after-output','_ak820_oneshot_mods',[2]);t.event((0,2),1,130);t.check('next-ordinary-shifted',tap.packet(2,4));t.event((0,2),0,131);t.check('all-released',tap.packet());r=t.result();r['pass']=r['pass'] and tap.packet(2,29) in r['hid_send_trace'];yield r
 t=Trace(fw,'leader-extended-macro-tail-no-clobber');t.macro([1,6,0x58,0x7c,1,7,0x58,0x7c]);t.memory('virtual-prefix-ignored','_leader_waiting',[0]);t.lead();t.select();t.event((0,2),1,125);t.check('physical-before-dispatch',tap.packet(0,4));t.tick(126);t.memory('no-recursion','_leader_waiting',[0]);t.check('physical-after-dispatch',tap.packet(0,4));t.event((0,2),0,127);t.check('released',tap.packet());yield t.result()
 t=Trace(fw,'leader-pending-busy');t.map((0,3),0x7c58);t.map((0,4),9);t.lead();t.select();t.event((0,3),1,125);t.event((0,3),0,126);t.event((0,4),1,127);t.memory('first-retained','_leader_pending',[0]);t.memory('not-waiting','_leader_waiting',[0]);t.tick(130);t.memory('dispatched','_leader_pending',[255]);yield t.result()
 t=Trace(fw,'leader-encoder-excluded');t.commands+=[tap.linked.memory('rom',0xcd40,[0x7c,0x58])];t.event((253,0),1,100);t.event((253,0),0,101);t.memory('ignored','_leader_waiting',[0]);yield t.result()
 t=Trace(fw,'leader-unknown-basic-consumed');t.map((0,1),0x29);t.lead();t.select();t.memory('cancelled','_leader_waiting',[0]);t.memory('empty','_leader_pending',[255]);t.check('no-escape',tap.packet());yield t.result()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build-dir',type=Path,required=True);p.add_argument('--s51',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
 fw=tap.linked.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve());tests=list(cases(fw));r={'pass':all(t['pass'] for t in tests),'tests':tests,'hardware_validated':False,'image_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest()};(fw.output/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'pass':r['pass'],'tests':len(tests),'failed':[t['name'] for t in tests if not t['pass']]}));raise SystemExit(not r['pass'])
if __name__=='__main__':main()
