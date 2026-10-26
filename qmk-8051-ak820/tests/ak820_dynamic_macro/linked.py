#!/usr/bin/env python3
"""Exact linked C52 Dynamic Macro scenarios; fake peripherals, no USB access."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('tap',ROOT/'tests/ak820_tapping/emitted.py')
tap=importlib.util.module_from_spec(spec);spec.loader.exec_module(tap)
packet=tap.packet
class Trace(tap.Trace):
 def __init__(self,fw,name):
  super().__init__(fw,name);self.time=100
  self.map((0,0),4);self.map((0,1),5)
 def event(self,pos,down,time):
  self.commands+=self.fw.clock(time);super().event(pos,down,time)
 def tick(self,time):
  self.commands+=self.fw.clock(time);super().tick(time)
 def press(self,pos): self.time+=20;self.event(pos,1,self.time)
 def release(self,pos): self.time+=1;self.event(pos,0,self.time)
 def tap(self,pos): self.press(pos);self.release(pos)
 def ctl(self,code): self.map((0,2),code);self.tap((0,2))
 def step(self): self.time+=20;self.tick(self.time)
 def seed(self,mods=0):
  self.ctl(0x7c53)
  if mods:self.map((0,3),0xe1);self.press((0,3))
  self.tap((0,0))
  if mods:self.release((0,3))
  self.ctl(0x7c55)
 def memory(self,label,symbol,value):self.check_memory(label,symbol,0,value)
 def result(self):
  r=self.run();r['pass']=r.pop('pass_');return r

def cases(fw):
 t=Trace(fw,'dm-basic-playback');t.seed();t.memory('slot','_dm_taps',[4,0]);t.ctl(0x7c56);t.step();t.check('down',packet(0,4));t.step();t.check('up',packet());t.step();t.memory('done','_dm_play',[0]);yield t.result()
 t=Trace(fw,'dm-rolling-order');t.ctl(0x7c53);t.press((0,0));t.press((0,1));t.release((0,1));t.release((0,0));t.ctl(0x7c55);t.memory('ordered','_dm_taps',[4,0,5,0]);t.ctl(0x7c56);t.step();t.check('a',packet(0,4));t.step();t.step();t.check('b',packet(0,5));t.step();t.step();t.memory('done','_dm_play',[0]);yield t.result()
 t=Trace(fw,'dm-incomplete-compacted');t.ctl(0x7c53);t.press((0,0));t.tap((0,1));t.ctl(0x7c55);t.memory('length','_dm_lengths',[1,0]);t.memory('completed','_dm_taps',[5,0]);t.release((0,0));t.ctl(0x7c56);t.step();t.check('only-b',packet(0,5));yield t.result()
 t=Trace(fw,'dm-preheld-not-recorded');t.press((0,0));t.ctl(0x7c53);t.release((0,0));t.ctl(0x7c55);t.memory('empty','_dm_lengths',[0,0]);yield t.result()
 t=Trace(fw,'dm-capacity-overwrite-slots');t.ctl(0x7c53)
 for i in range(20):t.tap((0,0))
 t.ctl(0x7c55);t.memory('full','_dm_lengths',[16,0]);t.ctl(0x7c54);t.tap((0,1));t.ctl(0x7c55);t.memory('two-slots','_dm_lengths',[16,1]);t.ctl(0x7c53);t.tap((0,1));t.ctl(0x7c55);t.memory('overwritten','_dm_lengths',[1,1]);t.memory('second-slot','_dm_taps',[5,0]);t.ctl(0x7c57);t.step();t.check('slot2-down',packet(0,5));yield t.result()
 for first in (False,True):
  t=Trace(fw,'dm-shift-ownership-'+str(int(first)));t.seed(2);t.ctl(0x7c56);t.step();t.check('macro-shift',packet(2,4));t.time+=1;t.event((0,3),1,t.time)
  if first:t.release((0,3));t.check('macro-still-shift',packet(2,4));t.step();t.check('all-up',packet())
  else:t.step();t.check('physical-shift',packet(2));t.release((0,3));t.check('all-up',packet())
  yield t.result()
 t=Trace(fw,'dm-held-same-usage-skip');t.seed();t.press((0,0));t.ctl(0x7c56);t.step();t.check('physical-survives',packet(0,4));t.memory('not-owned','_dm_down',[0]);t.step();t.memory('done','_dm_play',[0]);t.release((0,0));t.check('released',packet());yield t.result()
 t=Trace(fw,'dm-new-physical-owner-survives');t.seed();t.ctl(0x7c56);t.step();t.time+=1;t.event((0,0),1,t.time);t.step();t.check('physical-survives',packet(0,4));t.release((0,0));t.check('released',packet());yield t.result()
 for source,code in [('oneshot',0x52a2),('encoded',0x0106)]:
  t=Trace(fw,'dm-effective-'+source);t.ctl(0x7c53);t.map((0,3),code);t.tap((0,3))
  if source=='oneshot':t.tap((0,0))
  t.ctl(0x7c55);t.memory('effective-mods','_dm_taps',[4,2] if source=='oneshot' else [6,1]);t.ctl(0x7c56);t.step();t.check('replay',packet(2,4) if source=='oneshot' else packet(1,6));t.step();t.check('released',packet());yield t.result()
 has_nkro=fw.compiled_feature('nkro')
 t=Trace(fw,'dm-nkro-duplicate-physical-owner' if has_nkro else 'dm-nkro-disabled-stale-setting-physical-owner');t.seed()
 if has_nkro:
  t.width=32
  t.commands=[c.replace(f'{t.report_address+7:#x} 16;',f'{t.report_address+31:#x} 16;') for c in t.commands]
 t.commands+=fw.write('_keymap_config',[128,0])+fw.write('_keyboard_protocol',[1]);t.press((0,0));t.ctl(0x7c56);t.step();t.check('physical-survives',[6,0,16]+[0]*29 if has_nkro else packet(0,4));t.step();t.release((0,0));t.check('physical-released',[6]+[0]*31 if has_nkro else packet());t.memory('setting-retained','_keymap_config',[128,0]);yield t.result()
 t=Trace(fw,'dm-generated-output-excluded');t.ctl(0x7c53);t.tap((0,0));t.map((0,3),0x7c79);t.tap((0,3));t.commands+=[tap.linked.memory('rom',0xcd40,[0,5])];t.event((253,0),1,300);t.event((253,0),0,301);t.macro([1,2,6,1,3,6]);t.ctl(0x7c55);t.memory('only-original','_dm_lengths',[1,0]);yield t.result()
 t=Trace(fw,'dm-generated-controls-excluded');t.seed();t.macro([1,5,0x56,0x7c,1,6,0x56,0x7c,1,5,0x54,0x7c,1,6,0x54,0x7c]);t.memory('not-playing','_dm_play',[0]);t.memory('not-recording','_dm_record',[0]);yield t.result()
 t=Trace(fw,'dm-nested-macro-pauses-playback');t.seed();t.ctl(0x7c56);t.time+=20;t.commands+=fw.clock(t.time);t.macro([1,6,0x54,0x7c,1,7,0x54,0x7c]);t.memory('no-nested-owner','_dm_down',[0]);t.memory('still-playing','_dm_play',[1]);t.step();t.check('foreground-press',packet(0,4));t.step();t.check('foreground-release',packet());yield t.result()
 t=Trace(fw,'dm-nested-macro-pauses-due-release');t.seed(2);t.ctl(0x7c56);t.step();t.time+=20;t.commands+=fw.clock(t.time);t.macro([1,6,0x54,0x7c,1,7,0x54,0x7c]);t.check('owned-through-primitive',packet(2,4));t.step();t.check('released-after-primitive',packet());t.step();t.memory('finished','_dm_play',[0]);yield t.result()
 t=Trace(fw,'dm-clear-replay');t.seed(2);t.ctl(0x7c56);t.step();t.commands+=fw.call('_clear_keyboard');t.check('cleared',packet());t.step();t.memory('cancelled','_dm_play',[0]);t.memory('retained','_dm_lengths',[1,0]);t.check('no-revival',packet());yield t.result()
 t=Trace(fw,'dm-clear-recording');t.ctl(0x7c53);t.tap((0,1));t.press((0,0));t.commands+=fw.call('_clear_keyboard');t.release((0,0));t.memory('stopped','_dm_record',[0]);t.memory('complete-only','_dm_lengths',[1,0]);t.memory('b-only','_dm_taps',[5,0]);yield t.result()
 t=Trace(fw,'dm-pending-gates-phases');t.seed();t.ctl(0x7c56);t.commands+=fw.write('_pending_reports',[1]);t.step();t.check('busy-no-press',packet());t.commands+=fw.write('_pending_reports',[0]);t.step();t.check('press',packet(0,4));t.commands+=fw.write('_pending_reports',[1]);t.step();t.check('busy-held',packet(0,4));t.commands+=fw.write('_pending_reports',[0]);t.step();t.check('release',packet());t.commands+=fw.write('_pending_reports',[1]);t.step();t.memory('release-wait','_dm_play',[1]);t.commands+=fw.write('_pending_reports',[0]);t.step();t.memory('done','_dm_play',[0]);yield t.result()
 t=Trace(fw,'dm-no-recursion-controls');t.seed();t.ctl(0x7c56);t.step();t.ctl(0x7c53);t.ctl(0x7c57);t.ctl(0x7c55);t.memory('retained','_dm_lengths',[1,0]);t.memory('not-recording','_dm_record',[0]);yield t.result()
 if fw.has_auto_shift:
  t=Trace(fw,'dm-auto-shift-effective');t.commands+=fw.call('_ak820_dynamic_macro_cancel');t.ctl(0x7c53);t.map((0,3),0x7c13);t.tap((0,3));t.press((0,0));t.time+=175;t.tick(t.time);t.release((0,0));t.ctl(0x7c55);t.memory('stored-shift','_dm_taps',[4,2]);t.ctl(0x7c56);t.step();t.check('shifted-replay',packet(2,4));t.step();t.check('released',packet());yield t.result()

def transport_cases(fw):
 spec=importlib.util.spec_from_file_location('transport',ROOT/'tests/ak820_transport_retry/run.py')
 transport=importlib.util.module_from_spec(spec);spec.loader.exec_module(transport)
 def seeded(name):
  t=Trace(fw,name);t.seed();t.ctl(0x7c56)
  return [c for c in t.commands if not c.startswith('break ') and not c.startswith('commands 1 ')],t.time
 def task(now):return fw.clock(now)+fw.call('_ak820_dynamic_macro_task',now)
 setup,now=seeded('dm-real-busy')
 busy=[tap.linked.memory('xram',0x2201,[0x10])]
 ready=transport.ready(1);post=transport.post(fw)
 yield transport.case(fw,'dm-real-busy-down-release-retry',setup,[
  ('busy-press-retained',fw.address('_pending_reports'),[1],busy+task(now+20)),
  ('macro-owns-down',fw.address('_dm_down'),[4],[]),
  ('busy-prevents-early-release',fw.address('_dm_down'),[4],task(now+40)),
  ('down-eventually-accepted',0x1040,packet(0,4),ready+post),
  ('busy-release-retained',fw.address('_pending_reports'),[1],task(now+60)),
  ('desired-release',fw.address('_last_keyboard_report'),packet(),[]),
  ('accepted-down-until-ready',0x1040,packet(0,4),task(now+80)+post),
  ('engine-waits-release',fw.address('_dm_play'),[1],[]),
  ('release-eventually-accepted',0x1040,packet(),ready+post),
  ('complete-after-release',fw.address('_dm_play'),[0],task(now+100)),
 ])
 setup,now=seeded('dm-resume')
 yield transport.case(fw,'dm-suspend-resume-cancels-playback',setup+task(now+20),[
  ('suspended-no-publication',0x2201,[0x12],fw.write('_USB_SleepStatus',[2])+ready+fw.call('_protocol_pre_task')+task(now+40)+post),
  ('resume-clears-replay',fw.address('_dm_play'),[0],fw.write('_USB_SleepStatus',[0])+fw.write('_keyboard_reset',[1])+fw.call('_protocol_pre_task')+post),
  ('resume-release',0x1040,packet(),[]),
  ('slots-retained',fw.address('_dm_lengths'),[1,0],task(now+100)),
 ])
 setup,now=seeded('dm-unconfigured')
 yield transport.case(fw,'dm-unconfigured-pauses-before-down',setup,[
  ('no-owner-unconfigured',fw.address('_dm_down'),[0],fw.write('_USB_EnumStatus',[0])+task(now+20)),
  ('configured-press',0x1040,packet(0,4),fw.write('_USB_EnumStatus',[1])+task(now+40)),
 ])
 setup,now=seeded('dm-reset')
 yield transport.case(fw,'dm-reset-guards-before-task',setup,[
  ('no-owner-resetting',fw.address('_dm_down'),[0],fw.write('_keyboard_reset',[1])+task(now+20)),
  ('reset-cancels',fw.address('_dm_play'),[0],fw.call('_protocol_pre_task')+post),
  ('no-revival',fw.address('_actual_keyboard_report'),packet(),task(now+40)),
 ])
 for recording in (False,True):
  t=Trace(fw,'dm-unlock-'+str(int(recording)));t.seed()
  if recording:t.ctl(0x7c54);t.tap((0,1));t.press((0,0))
  else:t.ctl(0x7c56);t.step()
  t.commands+=tap.vial(fw,6);t.check('unlock-clears',packet());t.memory('not-playing','_dm_play',[0]);t.memory('not-recording','_dm_record',[0]);t.step();t.check('no-revival',packet());yield t.result()

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build-dir',type=Path,required=True);p.add_argument('--s51',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
 fw=tap.linked.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
 if max(fw.code)>=0xc700:raise ValueError('Image crosses fake NVM boundary')
 r={'level':'Exact linked SDCC C52; simulated peripherals, no physical USB/IRQ proof','hardware_validated':False,'linked_image_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),'tests':list(cases(fw))+list(transport_cases(fw))};r['pass']=all(x['pass'] for x in r['tests']);(fw.output/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(not r['pass'])
if __name__=='__main__':main()
