#!/usr/bin/env python3
"""Run compact Tap Dance against an existing linked SDCC image; no USB access."""
import argparse, hashlib, importlib.util, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('tap', ROOT / 'tests/ak820_tapping/emitted.py')
tap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tap)

class Trace(tap.Trace):
    def __init__(self, fw, name):
        super().__init__(fw, 'tap-dance-' + name)
        self.map((0, 0), 0x5700)
        self.map((0, 1), 0x5701)
        self.entry(0)
        self.entry(1)
        self.required = []
    def entry(self, index, actions=(4, 5, 6, 7), term=200):
        offset = index * 10 if index < 6 else 64 + (index - 6) * 10
        data = b''.join(v.to_bytes(2, 'little') for v in (*actions, term))
        self.commands += [tap.linked.memory('rom', 0xc700 + 0x6c0 + offset, data)]
    def press(self, time=100, pos=(0, 0)):
        self.event(pos, 1, time)
    def release(self, time=101, pos=(0, 0)):
        self.event(pos, 0, time)
    def short(self, time=100, pos=(0, 0)):
        self.press(time, pos)
        self.release(time + 1, pos)
    def require(self, *reports):
        self.required.extend(reports)
    def result(self):
        r = self.run()
        r['required_hid_packets'] = self.required
        r['pass'] = r.pop('pass_') and all(p in r['hid_send_trace'] for p in self.required)
        return r

def cases(fw):
    t=Trace(fw,'single');t.short();t.check('deferred',tap.packet());t.tick(300);t.check('released',tap.packet());t.require(tap.packet(0,4));yield t.result()
    t=Trace(fw,'hold');t.press();t.tick(300);t.check('held',tap.packet(0,5));t.release(301);t.check('released',tap.packet());yield t.result()
    t=Trace(fw,'double');t.short();t.short(120);t.tick(320);t.check('released',tap.packet());t.require(tap.packet(0,6));yield t.result()
    t=Trace(fw,'tap-hold');t.short();t.press(120);t.tick(320);t.check('held',tap.packet(0,7));t.release(321);t.check('released',tap.packet());yield t.result()
    t=Trace(fw,'empty-hold');t.entry(0,(4,0,6,7));t.press();t.tick(300);t.check('tap-held',tap.packet(0,4));t.release(301);t.check('released',tap.packet());yield t.result()
    t=Trace(fw,'empty-double');t.entry(0,(4,5,0,7));t.short();t.short(120);t.tick(320);t.check('released',tap.packet());r=t.result();r['pass'] &= r['hid_send_trace'].count(tap.packet(0,4))==2;yield r
    t=Trace(fw,'empty-tap-hold');t.entry(0,(4,5,6,0));t.short();t.press(120);t.tick(320);t.check('held',tap.packet(0,5));t.require(tap.packet(0,4));t.release(321);t.check('released',tap.packet());yield t.result()
    t=Trace(fw,'interrupt');t.map((0,2),8);t.press();t.press(120,(0,2));t.check('both',tap.packet(0,4,8));t.release(121);t.check('ordinary-survives',[0,0,0,8,0,0,0,0]);t.release(122,(0,2));t.check('released',tap.packet());yield t.result()
    t=Trace(fw,'overlapping-holds');t.press();t.tick(300);t.press(301,(0,1));t.tick(501);t.check('same-key-two-owners',tap.packet(0,5));t.release(502);t.check('other-owner-survives',tap.packet(0,5));t.release(503,(0,1));t.check('released',tap.packet());yield t.result()
    t=Trace(fw,'physical-owner');t.map((0,2),5);t.press(90,(0,2));t.press();t.tick(300);t.release(301);t.check('physical-survives',tap.packet(0,5));t.release(302,(0,2));t.check('released',tap.packet());yield t.result()
    t=Trace(fw,'duplicate-entry-source');t.map((0,1),0x5700);t.press();t.tick(300);t.press(301,(0,1));t.release(302,(0,1));t.check('original-survives',tap.packet(0,5));t.release(303);t.check('released',tap.packet());yield t.result()
    for unlock in (False,True):
        t=Trace(fw,'cancel-unlock' if unlock else 'cancel-clear');t.press();t.tick(300);t.commands += tap.vial(fw,6) if unlock else fw.call('_clear_keyboard');t.check('cleared',tap.packet());t.press(301);t.check('duplicate-blocked',tap.packet());
        if unlock:t.commands += tap.vial(fw,8)
        t.release(302);t.short(310);t.tick(510);t.check('fresh-released',tap.packet());t.require(tap.packet(0,4));yield t.result()
    t=Trace(fw,'timer-wrap');t.short(65520);t.tick(184);t.check('released',tap.packet());t.require(tap.packet(0,4));yield t.result()
    t=Trace(fw,'oneshot');t.map((0,2),0x52a1);t.short(80,(0,2));t.short();t.tick(300);t.check('released',tap.packet());t.require(tap.packet(1,4));yield t.result()
    t=Trace(fw,'repeat');t.map((0,2),0x7c79);t.short();t.tick(300);t.press(301,(0,2));t.check('repeat-held',tap.packet(0,4));t.release(302,(0,2));t.check('repeat-released',tap.packet());yield t.result()
    # A held layer disappears while this source is released between taps.
    # Base-layer replacement must receive its own release after the old tap.
    for replacement in (8,0x5701):
        t=Trace(fw,'layer-remap-'+hex(replacement));t.map((0,0),replacement);t.map((0,0),0x5700,1);t.map((0,2),0x5221);t.press(80,(0,2));t.short();t.release(110,(0,2));t.press(120);t.require(tap.packet(0,4));
        if replacement==8:t.check('new-ordinary-down',tap.packet(0,8));t.release(121)
        else:t.tick(320);t.check('new-dance-hold',tap.packet(0,5));t.release(321)
        t.check('new-mapping-released',tap.packet());yield t.result()
    for index in (6,7):
        t=Trace(fw,'padded-entry-'+str(index));t.entry(index,(8,9,10,11));t.map((0,0),0x5700+index);t.short();t.tick(300);t.check('released',tap.packet());t.require(tap.packet(0,8));yield t.result()
    t=Trace(fw,'encoder-excluded');t.commands += [tap.linked.memory('rom',0xcd40,[0x57,0])];t.press(100,(253,0));t.release(101,(253,0));t.tick(400);t.check('empty',tap.packet());r=t.result();r['pass'] &= not any(p[2] in (4,5,6,7) for p in r['hid_send_trace']);yield r

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build-dir',type=Path,required=True)
    p.add_argument('--s51',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    fw=tap.linked.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
    if any(0x2600<=address<0x2703 or address>=0xc700 for address in fw.code):
        raise ValueError('Image overlaps simulator trampoline or NVM fixture')
    tests=list(cases(fw))
    r={'pass':all(t['pass'] for t in tests),'tests':tests,'image_sha256':hashlib.sha256(fw.image.read_bytes()).hexdigest(),'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'hardware_validated':False,'limits':'Exact linked CPU with simulated ROM/USB-ready fixtures. No physical timing, USB transfer, NVM persistence, power-loss or interrupt overlap proof.'}
    (fw.output/'results.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'pass':r['pass'],'tests':len(tests),'failed':[t['name'] for t in tests if not t['pass']],'peak_sp':max(t['peak_sp'] for t in tests)},indent=2))
    return 0 if r['pass'] else 1
if __name__=='__main__':raise SystemExit(main())
