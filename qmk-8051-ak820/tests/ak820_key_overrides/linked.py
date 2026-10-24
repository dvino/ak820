#!/usr/bin/env python3
"""Observe outgoing projected reports from an existing exact linked image."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('tapping', ROOT / 'tests/ak820_tapping/emitted.py')
tapping = importlib.util.module_from_spec(spec); spec.loader.exec_module(tapping)
emitted = tapping.linked

class Trace(tapping.Trace):
    def __init__(self, fw, name):
        super().__init__(fw, name)
        names = [n for n in fw.symbols if n.startswith('_send_keyboard_report_projected_')]
        if len(names) != 1:
            raise ValueError(f'Expected one linked outgoing report projection, got {names}')
        self.projected = fw.address(names[0])
        self.commands = [c.replace(f'dump xram {self.report_address:#x} {self.report_address+7:#x} 16;',
                                  f'dump xram {self.projected:#x} {self.projected+31:#x} 16;') for c in self.commands]
        self.width = 32
        self.observations = []
    def output(self, label, mods=0, keys=(), nkro=False):
        self.commands += self.fw.dump(label, 'xram', self.projected, 32)
        self.observations.append((label, mods, sorted(keys), nkro))
    def run(self):
        result = super().run()
        log = (self.fw.output / (self.name + '.log')).read_text()
        checks = []
        for label, mods, keys, nkro in self.observations:
            report = self.fw.extract(log, label, self.projected, 32)
            if nkro:
                actual_mods = report[1]
                actual_keys = [k for k in range(4, 165) if report[2 + (k >> 3)] & (1 << (k & 7))]
                ok = report[0] == 6 and actual_mods == mods and actual_keys == keys
            else:
                actual_mods, actual_keys = report[0], sorted(k for k in report[2:8] if k)
                ok = actual_mods == mods and actual_keys == keys
            checks.append(dict(label=label, actual_report=report, expected_mods=mods,
                               expected_keys=keys, report_type='NKRO' if nkro else '6KRO', pass_=ok))
        pointers = result['outgoing_pointer_checks']
        result['outgoing_checks'] = checks
        result['outgoing_pointer_checks'] = pointers
        result['outgoing_projection_address'] = self.projected
        result['pass_'] &= bool(pointers) and all(p == [self.projected & 255, self.projected >> 8] for p in pointers) and all(c['pass_'] for c in checks)
        return result

def row(trigger=4, replacement=5, required=2, suppressed=2, options=0x87):
    return list(trigger.to_bytes(2,'little') + replacement.to_bytes(2,'little') + bytes([63,0,required,0,suppressed,options]))
def setup(fw, name, *, options=0x87, required=2, suppressed=2, replacement=5):
    t = Trace(fw, name)
    t.commands += [emitted.memory('rom', 0xc700 + 0x740, row(replacement=replacement,required=required,suppressed=suppressed,options=options))]
    t.commands += fw.call('_ak820_key_override_reload')
    for pos, code in [((0,0),4),((0,1),0xe1),((0,2),5),((0,3),0x7c79),((0,4),0x52a2),((0,5),0x7c5f),((0,6),0x7c5e)]:
        t.map(pos, code)
    return t

def memory_check(t, label, address, expected, space='xram'):
    label += '@'
    symbol = '_ko_fixture_' + label
    t.fw.symbols[symbol] = address
    t.fw.symbol_spaces[symbol] = space
    t.commands += t.fw.dump(label, space, address, len(expected))
    t.expected.append((label, symbol, list(expected)))

def storage_api(t, operation, index, expected_status=0):
    # Public dynamic-entry ABI retains a generic pointer to the XDATA fixture.
    t.commands += t.fw.write('_dynamic_keymap_' + operation + '_key_override_PARM_2', [0,0x24,0])
    t.commands += t.fw.call('_dynamic_keymap_' + operation + '_key_override', index)
    memory_check(t, operation + '-' + str(index), 0x82,
                 list((expected_status & 65535).to_bytes(2,'little')), 'sfr')

def cases(fw):
    results=[]
    for nkro in (False, True):
        t=setup(fw,'ko-output-and-overlap-'+str(nkro),options=0xa7)
        if nkro:t.commands += fw.write('_keymap_config',[128,0])+fw.write('_keyboard_protocol',[1])
        t.event((0,1),1,100);t.event((0,0),1,110);t.output('replacement',0,[5],nkro)
        t.event((0,2),1,120);t.event((0,0),0,130);t.output('independent-owner',2,[5],nkro)
        t.event((0,2),0,140);t.event((0,1),0,150);t.output('empty',0,[],nkro)
        results.append(t.run())
    t=setup(fw,'ko-modifier-sync-and-switch')
    t.event((0,0),1,100);t.output('plain-trigger',0,[4])
    t.event((0,1),1,110);t.output('modifier-activation',0,[5])
    t.event((0,5),1,120);t.output('switch-off-restores-trigger',2,[4])
    t.event((0,5),0,121);t.event((0,0),0,130);t.event((0,1),0,140)
    t.event((0,6),1,150);t.event((0,6),0,151);t.event((0,1),1,160);t.event((0,0),1,170);t.output('switch-on',0,[5])
    t.commands+=fw.call('_clear_keyboard');t.output('clear',0,[])
    t.event((0,0),0,180);t.event((0,1),0,181);t.output('late-release',0,[])
    results.append(t.run())
    if '_ak820_oneshot_process' in fw.symbols:
        t=setup(fw,'ko-oneshot-owner')
        t.event((0,4),1,100);t.event((0,4),0,101);t.event((0,0),1,110);t.output('oneshot-override',0,[5])
        t.check_memory('oneshot-retained','_owned_mods',0,[2])
        t.event((0,0),0,120);t.output('oneshot-consumed',0,[]);t.check_memory('owner-clean','_owned_mods',0,[0]);results.append(t.run())
    t=setup(fw,'ko-repeat-generated-owner')
    t.event((0,1),1,100);t.event((0,0),1,110);t.event((0,0),0,120);t.event((0,1),0,130)
    t.event((0,3),1,140);t.output('repeat-original-with-remembered-modifier',2,[4])
    t.event((0,3),0,150);t.output('repeat-release',0,[]);results.append(t.run())
    t=setup(fw,'ko-6kro-overlay-rollover',options=0xa7)
    for i in range(6):t.map((1,i),6+i)
    t.event((0,1),1,90)
    for i in range(6):t.event((1,i),1,100+i)
    t.event((0,0),1,110);t.output('seven-distinct-rollover',0,[1]*6)
    t.event((0,0),0,120);t.output('six-original-owners',2,list(range(6,12)))
    t.commands+=fw.call('_clear_keyboard');t.output('clear-rollover',0,[]);results.append(t.run())
    # Combo-generated output traverses the production record pipeline and
    # must release the captured owner on either input's first release.
    for release_first in (0,2):
        for other_releases_first in (False,True):
            t=setup(fw,f'ko-combo-overlap-{release_first}-{other_releases_first}',options=0xa7)
            t.map((0,0),6);t.map((0,2),7);t.map((1,0),5)
            combo=[6,0,7,0,0x20,8,1,0,4,0]
            t.commands += [emitted.memory('rom',0xc700+0x658,combo)]+fw.call('_ak820_combo_reload')
            t.event((0,1),1,90);t.event((1,0),1,95)
            t.event((0,0),1,100);t.event((0,2),1,110);t.output('combo-and-physical',0,[5])
            if other_releases_first:
                t.event((1,0),0,120);t.output('combo-survives',0,[5])
            t.event((0,release_first),0,130)
            t.output('combo-owner-released',2,[] if other_releases_first else [5])
            t.event((0,2 if release_first==0 else 0),0,140)
            if not other_releases_first:t.event((1,0),0,150)
            t.event((0,1),0,160);t.output('all-combo-owners-clean',0,[]);results.append(t.run())
    t=setup(fw,'ko-caps-word-shift-cleanup',suppressed=0)
    t.commands += fw.call('_caps_word_on')
    t.event((0,0),1,100);t.output('caps-word-replacement',2,[5])
    t.event((0,0),0,110);t.output('caps-release',2,[])
    t.commands += fw.call('_caps_word_off')+fw.call('_send_keyboard_report')
    t.output('caps-disabled-clean',0,[])
    t.event((0,0),1,120);t.output('plain-next-trigger',0,[4])
    t.event((0,0),0,130);t.output('plain-release',0,[]);results.append(t.run())
    # Seed the aggregate owner byte to model one atomic mixed transition;
    # eligibility runs through the real report sync, not a fixture helper.
    t=setup(fw,'ko-mixed-modifier-transition',required=1,suppressed=1,options=0x84)
    transition_row=row(required=1,suppressed=1,options=0x84);transition_row[7]=4
    t.commands += [emitted.memory('rom',0xc700+0x740,transition_row)]+fw.call('_ak820_key_override_reload')
    t.commands += fw.write('_real_mods',[8])+fw.call('_send_keyboard_report')
    t.event((0,0),1,100);t.output('unmatched-trigger',8,[4])
    t.commands += fw.write('_real_mods',[1])+fw.call('_send_keyboard_report')
    t.output('unrelated-fall-cannot-activate',1,[4])
    t.commands += fw.write('_real_mods',[5])+fw.call('_send_keyboard_report')
    t.output('forbidden-held',5,[4])
    t.commands += fw.write('_real_mods',[1])+fw.call('_send_keyboard_report')
    t.output('actual-forbidden-release-activates',0,[5])
    t.event((0,0),0,110);t.commands += fw.write('_real_mods',[0])+fw.call('_send_keyboard_report')
    t.output('transition-clean',0,[]);results.append(t.run())
    t=setup(fw,'ko-padded-getters-and-rejected-write')
    image=[0]*128
    malformed=row();malformed[1]=0x20
    image[:10]=malformed
    row6=row(trigger=6,replacement=7,required=0,suppressed=0)
    row7=row(trigger=8,replacement=9,required=0,suppressed=0)
    image[64:74]=row6;image[74:84]=row7
    t.commands += [emitted.memory('rom',0xc700+0x740,image)]
    for index,expected in ((0,[0]*10),(6,row6),(7,row7)):
        t.commands += [emitted.memory('xram',0x2400,[0xa5]*10)]
        storage_api(t,'get',index);memory_check(t,'row-'+str(index),0x2400,expected)
    t.commands += [emitted.memory('xram',0x2400,[0xa5]*10)]
    storage_api(t,'get',8,-1);memory_check(t,'bad-index-buffer',0x2400,[0xa5]*10)
    t.map((1,7),9);t.event((1,7),1,100);t.output('owner-before-rejection',0,[9])
    t.commands += [emitted.memory('xram',0x2400,malformed)]
    storage_api(t,'set',6,-1);t.output('rejection-keeps-owner',0,[9])
    memory_check(t,'unchanged-nvm',0xc700+0x740,image,'rom')
    memory_check(t,'no-cache-dirty',fw.address('_page_dirty'),[0],fw.symbol_space('_page_dirty'))
    t.event((1,7),0,110);t.output('rejection-clean-release',0,[]);results.append(t.run())
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for option in ('build-dir','s51','output-dir'):p.add_argument('--'+option,type=Path,required=True)
    a=p.parse_args();fw=emitted.Firmware(a.build_dir.resolve(),a.s51.resolve(),a.output_dir.resolve())
    fw.address('_ak820_key_override_process')
    tests=cases(fw)
    for t in tests:t['pass']=t.pop('pass_')
    report=dict(level='exact linked C52 outgoing-report projection and physical action_exec pipeline',image_sha256=hashlib.sha256(fw.image.read_bytes()).hexdigest(),runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),tests=tests,limits='Simulated ROM rows and USB-ready state. No physical USB, IAP durability, IRQ overlap or physical timing proof.',pass_=all(t['pass'] for t in tests))
    report['pass']=report.pop('pass_');(fw.output/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'pass':report['pass'],'tests':len(tests),'failed':[t['name'] for t in tests if not t['pass']]},indent=2));return int(not report['pass'])
if __name__=='__main__':raise SystemExit(main())
