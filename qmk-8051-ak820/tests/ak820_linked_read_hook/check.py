#!/usr/bin/env python3
"""Finite, fail-closed effect proof for the exact linked AK820 read hook."""
import argparse, hashlib, importlib.util, json, pathlib, re

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def prove(instructions, code, entry, reader, analyzer):
    a=analyzer.Analyzer(instructions,code)
    raw=a.instruction(entry)
    if raw != bytes([2,reader>>8,reader&255]): raise ValueError('wrapper must LJMP exact read_offset')
    bound=a.bound(entry)
    if bound['unresolved'] or bound['bound'] is None: raise ValueError('unresolved/unbalanced analyzer stack')
    seen=set(); active=set(); rows={}; peaks=[]
    def walk(pc, stack=(), returns=()):
        state=(pc,stack,returns)
        if state in active: raise ValueError('cyclic control flow')
        if state in seen:return
        if len(stack)>32 or len(returns)>8:raise ValueError('excess stack/calls')
        active.add(state)
        raw=a.instruction(pc)
        if not raw:raise ValueError('missing opcode')
        rows[pc]=raw.hex();op=raw[0]; nxt=pc+len(raw)
        peaks.append(len(stack)+2*len(returns))
        def go(target,s=stack,r=returns):walk(target,s,r)
        if op==0x22:
            if returns:
                dest,prior=returns[-1]
                if stack!=prior:raise ValueError('callee stack imbalance')
                go(dest,stack,returns[:-1])
            elif stack:raise ValueError('return stack imbalance')
        elif op==0xc0:
            if raw[1] not in (0x82,0x83):raise ValueError('push outside DPTR')
            go(nxt,stack+(raw[1],))
        elif op==0xd0:
            if not stack or (returns and len(stack)<=len(returns[-1][1])) or raw[1]!=stack[-1]:raise ValueError('wrong pop or return-frame alias')
            go(nxt,stack[:-1])
        elif op in (2,0x12) or op&31 in (1,17):
            target=int.from_bytes(raw[1:],'big') if op in (2,0x12) else ((nxt&0xf800)|((op&0xe0)<<3)|raw[1])
            if op==0x12 or op&31==17:go(target,stack,returns+((nxt,stack),))
            else:go(target)
        elif op in (0x20,0x30,0x40,0x50,0x60,0x70,0x80):
            rel=raw[-1] if raw[-1]<128 else raw[-1]-256
            go(nxt+rel)
            if op!=0x80:go(nxt)
        elif op in (0xe5,0x45,0x65):
            if raw[1] not in (0x82,0x83,0xf0):raise ValueError('unexpected direct read')
            go(nxt)
        elif op in (0x75,0xf5):
            if raw[1] not in (0x82,0x83,0xf0):raise ValueError('direct write outside A/B/DPTR')
            go(nxt)
        elif op in (0x23,0xc3,0xe4,0xe0,0x93,0x90,0x94,0x54,0x24,0x34):go(nxt)
        else:raise ValueError(f'forbidden opcode {op:02x} at {pc:04x}')
        active.remove(state);seen.add(state)
    walk(entry)
    if set(rows)!=set(bound['reachable']):raise ValueError('closure differs from analyzer')
    if max(peaks)!=bound['bound']:raise ValueError('stack bound differs from analyzer')
    return {'entry':entry,'read_offset':reader,'extra_stack_bytes':bound['bound'],'reachable_instructions':[{ 'pc':p,'bytes':rows[p]} for p in sorted(rows)],'states':len(seen)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--build',type=pathlib.Path,required=True);p.add_argument('--analyzer',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);args=p.parse_args()
    spec=importlib.util.spec_from_file_location('linked_analyzer',args.analyzer);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    ins,sym,code,identity=m.load(args.build)
    matches=[]
    for rst in (args.build/'dce').rglob('*.rst'):
        matches += [(int(x,16),str(rst.relative_to(args.build))) for x in re.findall(r'^\s*([0-9A-F]{6})\s+\d+\s+_read_offset:',rst.read_text(),re.M)]
    if len(matches)!=1:raise ValueError('read_offset label not unique')
    entry=sym['_eeprom_read_byte'];reader=matches[0][0]
    result=prove(ins,code,entry,reader,m)
    tests={}
    # Mutations replace a reached complete instruction; both image and listing are
    # changed consistently, so rejection does not merely test hash disagreement.
    target=next(x['pc'] for x in result['reachable_instructions'] if x['bytes']=='f5f0')
    pop=next(x['pc'] for x in result['reachable_instructions'] if x['bytes']=='d083')
    cases={'R0_write':(target,b'\x78\x00'),'PSW_bank_write':(target,b'\xf5\xd0'),'indirect_IRAM_write':(target,b'\x76\x00'),'SP_alias_write':(target,b'\xf5\x81'),'wrong_pop':(pop,b'\xd0\x82'),'pop_register_alias':(pop,b'\xd0\x00'),'storage_write':(target,b'\xf0')}
    for name,(pc,raw) in cases.items():
        altered=dict(ins);altered[pc]=raw;c=dict(code)
        for j,v in enumerate(raw):c[pc+j]=v
        try:prove(altered,c,entry,reader,m)
        except (ValueError,IndexError) as e:tests[name]={'rejected':True,'reason':str(e)}
        else:raise ValueError('mutation accepted: '+name)
    out={'status':'PASS','scope':'Conditional exact-linked eeprom_read_byte R0-R7 preservation and absence of storage writes','build':str(args.build.resolve()),'code_input_hashes':identity,'checker_sha256':sha(pathlib.Path(__file__)),'analyzer_sha256':sha(args.analyzer),'reader_listing':matches[0][1],'proof':result,'mutations':tests,'assumptions':['8051 instruction semantics; register bank zero at entry. No instruction writes R0-R7 in any bank or PSW bank-select bits. Arithmetic may modify flags.','Valid nonwrapping internal stack wholly disjoint from register banks, live data and SFRs, with space for caller return frame, reported extra stack and enabled IRQ overlays.','Interrupt handlers preserve interrupted R0-R7, PSW bank, SP and interrupted stack; enabled IRQ bounds and stack capacity require separate exact-image whole-program evidence.','Initial return frame valid; no concurrent corruption of code or stack. All conditional paths considered without relying on page_valid values.'],'limits':['Static machine-code effect proof, not CPU execution or hardware validation.','Does not prove read value correctness, cache coherence, timing, flash semantics, or writer behavior.','No eeprom_update_byte writer proof is claimed. Original external hook checker was unavailable; this checker is newly authored.']}
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','output':str(args.output),'stack':result['extra_stack_bytes'],'instructions':len(result['reachable_instructions']),'mutations':len(tests)}))
if __name__=='__main__':main()
