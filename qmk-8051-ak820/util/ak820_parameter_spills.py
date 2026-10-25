#!/usr/bin/env python3
"""Experimental private SDCC first-argument spill folding.

DRAFT integration packet: opt-in, source/type/byte/context proofs fail closed.
No USB or installation action. Prelink context and postlink image audit are
separate. Valid C object accesses and the normal large-model ABI are explicit
prerequisites; physical/startup/IRQ-wrapper/stack acceptance is not implied.
"""
from __future__ import annotations
import collections
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import ak820_outline_audit as audit
import ak820_register_saves as architecture
from ak820_build_inputs import dependency_paths

ALGORITHM='experimental-private-formal-spills-v1'
FORMAT='ak820-private-formal-context-1'
IRQ_ROOTS=('_USB_DeviceInterrupt','_ak820_timer_irq','_ak820_led_irq')
CONTRACT='valid-c-unescaped-nonvolatile-private-formal-v1'
EXCLUDED=re.compile(r'irq|interrupt|naked|usb|ch555|gpio|hal\.asm|iap|nvm|flash|eeprom|boot',re.I)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n')

def canonical(text):
    """Ignore comments/spacing outside literals; retain all assembler semantics."""
    output=[]
    for line in text.splitlines():
        quoted=False;escaped=False;result=[]
        for char in line:
            if not quoted and char==';':break
            if char=='"' and not escaped:quoted=not quoted
            if quoted or not char.isspace():result.append(char)
            escaped=char=='\\' and not escaped if quoted else False
        if result:output.append(''.join(result))
    return hashlib.sha256('\n'.join(output).encode()).hexdigest()

@dataclass
class Inventory:
    source: Path
    functions: list
    symbol_refs: dict
    allocs: dict
    symbols_globl: set
    hashes: dict

def inventory(source: Path):
    functions=[];symbol_refs=collections.defaultdict(list);allocs=collections.defaultdict(list);sources={};symbols_globl=set()
    for p in sorted(source.rglob('*.asm')):
     module=p.relative_to(source).as_posix();lines=p.read_text().splitlines();listing=p.with_suffix('.lst');byline={}
     sources[module]={'asm_sha256':sha(p),'lst_sha256':sha(listing)}
     for text in listing.read_text().splitlines():
      m=audit.LISTED.match(text)
      if not m:continue
      n=int(m[3])
      if n in byline or not 1<=n<=len(lines):raise ValueError('Ambiguous listing line')
      op=m[4].lower();args=re.sub(r'\s+','',m[5].split(';',1)[0])
      raw=lines[n-1].split(';',1)[0].strip().split(None,1)
      if not raw or raw[0].lower()!=op or re.sub(r'\s+','',raw[1] if len(raw)>1 else '')!=args:raise ValueError('ASM/listing mismatch')
      byline[n]={'line':n,'address':int(m[1],16),'op':op,'args':args,'bytes':re.sub('[rstup*\\s]','',m[2]).lower()}
     current=None;area='';marker=None;last_label=None
     for n,line in enumerate(lines,1):
      text=line.split(';',1)[0].strip();m=re.fullmatch(r';\s*function\s+(\w+)',line.strip())
      if m:marker=m[1];current=None
      if text.startswith('.area'):area=text.split()[1];current=None
      if text.startswith('.globl'):symbols_globl.update(re.findall(r'_[A-Za-z_]\w*',text))
      for symbol in set(re.findall(r'(?<![\w$])_[A-Za-z_]\w*',text)):
       symbol_refs[symbol].append({'module':module,'line':n,'text':text,'area':area})
      label=re.fullmatch(r'(_[A-Za-z_]\w*):(:?)',text)
      if label:
       last_label=(label[1],n)
       if area=='CSEG':
        current={'module':module,'name':label[1],'marker':marker,'body':[]};functions.append(current)
      if text.startswith('.ds') and last_label:
       allocs[last_label[0]].append({'module':module,'area':area,'label_line':last_label[1],'ds_line':n,'size':text.split()[1]});last_label=None
      if current is not None and n in byline:current['body'].append(byline[n])
    return Inventory(source,functions,symbol_refs,allocs,symbols_globl,sources)

def candidates(inv: Inventory):
    records=[];rejected=collections.Counter()
    INITIAL={**{f'r{i}':'oldr'+str(i) for i in range(8)},'dpl':'p0','dph':'p1','b':'p2','a':'p3'}
    for f in inv.functions:
     if f['marker'] is None or '_'+f['marker']!=f['name']:continue
     body=f['body'];state=dict(INITIAL);obj=None;offset=None;memory={};stores=[];reads=[];pointers=[];width=None;end=None;lastread=None
     for n,i in enumerate(body[:45]):
      op,args=i['op'],i['args'];parts=args.split(',')
      if op=='mov' and len(parts)==2 and parts[0]=='dptr' and re.fullmatch(r'#_[A-Za-z_]\w*',parts[1]):
       name=parts[1][1:]
       if obj is None:
        a=inv.allocs.get(name,[])
        if len(a)!=1 or a[0]['area']!='XSEG' or a[0]['size'] not in {'1','2','3','4'}:break
        obj=name;width=int(a[0]['size'])
       if name!=obj:break
       offset=0;pointers.append(i['line']);state['dpl']=('object',0,'lo');state['dph']=('object',0,'hi');continue
      if op=='mov' and len(parts)==2:
       dst,src=parts
       if dst not in state or src not in state or dst in {'dpl','dph','b'}:break
       if obj is None and dst=='a' and src not in {'dpl','dph','b'}:break
       state[dst]=state[src]
       if reads:lastread=n+1
       continue
      if op=='inc' and args=='dptr' and obj is not None and offset is not None:
       offset+=1
       if offset>=width:break
       state['dpl']=('object',offset,'lo');state['dph']=('object',offset,'hi');continue
      if op=='movx' and args=='@dptr,a' and obj is not None and not reads and offset is not None:
       if offset!=len(stores) or state['a']!='p'+str(offset):break
       stores.append(offset);memory[offset]=state['a'];continue
      if op=='movx' and args=='a,@dptr' and obj is not None and len(stores)==width and offset is not None:
       if offset!=len(reads) or offset not in memory:break
       state['a']=memory[offset];reads.append(offset);lastread=n+1
       if len(reads)==width:
        if n+1<len(body) and body[n+1]['op']=='mov' and re.fullmatch(r'r[0-7],a',body[n+1]['args']):
         state[body[n+1]['args'].split(',')[0]]=state['a'];lastread=n+2
        break
       continue
      break
     if obj is None or not reads or len(stores)!=width or lastread is None:continue
     seq=body[:lastread]
     # Recover exact endpoint state, avoiding accidentally included trailing MOVs
     # after a partial reload when the data pointer begins another object.
     if offset!=reads[-1] or state['a']!='p'+str(reads[-1]):continue
     if any(y['address']!=x['address']+len(bytes.fromhex(x['bytes'])) for x,y in zip(seq,seq[1:])):continue
     lines=(inv.source/f['module']).read_text().splitlines()
     if any(re.fullmatch(r'\s*(?:\d+\$|_[A-Za-z_]\w*):+',l) for l in lines[seq[0]['line']:seq[-1]['line']-1]):continue
     # Optimal straightforward register assignment for this finite state class:
     # no scratch registers or active-bank assumptions. Capture input ACC before
     # changing A; all other tokens remain in DPL/DPH/B until final DPTR restore.
     replacement=[];supported=True
     for token in ['p3','p0','p1','p2']:
      for r in [f'r{k}' for k in range(8)]:
       if state[r]!=token or state[r]==INITIAL[r]:continue
       replacement.append('mov '+r+','+{'p3':'a','p0':'dpl','p1':'dph','p2':'b'}[token])
     for r in [f'r{k}' for k in range(8)]:
      if state[r]!=INITIAL[r] and state[r] not in {'p0','p1','p2','p3'}:supported=False
     if not supported or state['b']!='p2':continue
     newbytes=sum(1 if x.endswith(',a') else 2 for x in replacement)
     if True: # Baseline MOVX writes A: reproduce final parity even if A's token equals its incoming value.
      holders=[r for r in [f'r{k}' for k in range(8)] if state[r]==state['a']]
      if holders:replacement.append('mov a,'+holders[0]);newbytes+=1
      elif state['a'] in {'p0','p1','p2'}:replacement.append('mov a,'+{'p0':'dpl','p1':'dph','p2':'b'}[state['a']]);newbytes+=2
      elif state['a']=='p3':replacement.append('mov a,acc');newbytes+=2
      else:continue
     replacement.append('mov dptr,#('+obj+'+0x'+format(reads[-1],'04x')+')');newbytes+=3
     oldbytes=sum(len(bytes.fromhex(i['bytes'])) for i in seq)
     # Symbolic boundary-state re-execution proves copies, not memory equivalence.
     actual=dict(INITIAL)
     for instruction in replacement[:-1]:
      dst,src=instruction[4:].split(',');actual[dst]=actual['a' if src=='acc' else src]
     actual['dpl']=('object',reads[-1],'lo');actual['dph']=('object',reads[-1],'hi')
     if actual!=state:continue
     refs=inv.symbol_refs[obj];uses=[r for r in refs if not re.fullmatch(re.escape(obj)+r'::?',r['text'])]
     pointers=[i['line'] for i in seq if i['op']=='mov' and i['args']=='dptr,#'+obj]
     private=obj not in inv.symbols_globl and len(uses)==len(pointers) and all(r['module']==f['module'] and r['line'] in pointers for r in uses)
     record={'module':f['module'],'function':f['name'],'object':obj,'width':width,'read_bytes':len(reads),'complete_reload':len(reads)==width,'private_unique_symbol_uses':private,'allocation':inv.allocs[obj],'references':refs,'entry':seq,'boundary_state_replacement_only':replacement,'old_bytes':oldbytes,'replacement_bytes':newbytes,'net_bytes':oldbytes-newbytes,'qualified':False}
     records.append(record)
    return records

def strip_c_literals(text):
    output=[];n=0
    while n<len(text):
        if text.startswith('//',n):
            end=text.find('\n',n);n=len(text) if end<0 else end;output.append(' ');continue
        if text.startswith('/*',n):
            end=text.find('*/',n+2)
            if end<0:raise ValueError('Unterminated C comment')
            n=end+2;output.append(' ');continue
        if text[n] in {'"',"'"}:
            quote=text[n];n+=1
            while n<len(text):
                if text[n]=='\\':n+=2;continue
                if text[n]==quote:n+=1;break
                n+=1
            else:raise ValueError('Unterminated C literal')
            output.append(' ');continue
        output.append(text[n]);n+=1
    return ''.join(output)


def source_proof(candidate,raw,ast,preprocessed):
    if not preprocessed:return False,'Missing preprocessed source'
    try:lexical=strip_c_literals(preprocessed)
    except ValueError as exc:return False,str(exc)
    if re.search(r'\b(?:asm|__asm|__asm__)\b',lexical):return False,'Source inline assembly has no object-alias proof'
    obj,fn=candidate['object'],candidate['function']
    binds=[line for line in raw.splitlines() if re.search(r'\b'+re.escape(obj)+r'\s+\[',line) and re.search(r'= recv '+re.escape(fn)+r'\s+\[',line)]
    if len(binds)!=1:return False,'Missing/ambiguous typed recv identity'
    left=binds[0].split(' = recv ',1)[0]
    types=re.findall(r'\{([^{}]*)\}',left)
    if len(types)<2 or not re.search(r'char|int|float|double|struct|generic|__xdata|__code',types[-1]):return False,'Missing formal type'
    typ=types[-1]
    # A volatile pointee is distinct from a volatile parameter object.
    if 'volatile' in (typ.rsplit('*',1)[-1] if '*' in typ else typ):return False,'Volatile parameter object'
    if re.search(r'&\[\s*'+re.escape(obj)+r'\s+\[',raw):return False,'Formal address taken'
    sections=re.split(r'^FUNCTION \(',ast,flags=re.M)
    own=[section for section in sections if section.startswith(fn+'=')]
    if len(own)!=1:return False,'Missing/ambiguous AST function identity'
    if re.search(r'\b(?:ASM|INLINEASM|INLINE_ASM|__asm)\b',own[0],re.I):return False,'Inline assembly has no object-alias proof'
    return True,typ


def opcode_proof(c,source_tree):
    source=source_tree/c['module'];sym=source.with_suffix('.sym').read_text();rel=source.with_suffix('.rel').read_text()
    matches=re.findall(r'^\s*([0-9A-F]+)\s+'+re.escape(c['object'])+r'\s+([0-9A-F]{6})\s+R\s*$',sym,re.M)
    areas=re.findall(r'^\s*([0-9A-F]+)\s+XSEG\s+size\s+([0-9A-F]+)\s+flags\s+40\s*$',sym,re.M)
    if len(matches)!=1 or len(areas)!=1:return False,'Missing/ambiguous local symbol/area identity'
    if matches[0][0]!=areas[0][0]:return False,'Object is not in XSEG'
    offset=int(matches[0][1],16);size=int(areas[0][1],16)
    if not 0<=offset<=size-c['width']:return False,'Object allocation exceeds local area'
    if not re.search(r'^A XSEG size '+format(size,'X')+r' flags 40 addr 0$',rel,re.M):return False,'REL/XSEG identity mismatch'
    for i in c['entry']:
        op,args=i['op'],i['args'];b=bytes.fromhex(i['bytes']);expected=None
        if op=='movx':expected=bytes([0xf0 if args=='@dptr,a' else 0xe0]) if args in {'@dptr,a','a,@dptr'} else None
        elif op=='inc' and args=='dptr':expected=b'\xa3'
        elif op=='mov':
            dst,src=args.split(',')
            if dst=='dptr' and src=='#'+c['object']:expected=bytes([0x90,offset>>8,offset&255])
            elif re.fullmatch(r'r[0-7]',dst) and src in {'dpl','dph','b'}:expected=bytes([0xa8+int(dst[1]),{'dpl':0x82,'dph':0x83,'b':0xf0}[src]])
            elif re.fullmatch(r'r[0-7]',dst) and src=='a':expected=bytes([0xf8+int(dst[1])])
            elif dst=='a' and re.fullmatch(r'r[0-7]',src):expected=bytes([0xe8+int(src[1])])
            elif dst=='a' and src in {'dpl','dph','b'}:expected=bytes([0xe5,{'dpl':0x82,'dph':0x83,'b':0xf0}[src]])
        if expected is None or expected!=b:return False,'Exact instruction byte mismatch'
    return True,{'allocation_area':'XSEG','local_offset_not_linked_address':offset,'sym_sha256':sha(source.with_suffix('.sym')),'rel_sha256':sha(source.with_suffix('.rel'))}


def tail_private_access(c,inv):
    f=next(f for f in inv.functions if (f['module'],f['name'])==(c['module'],c['function']));body=f['body'];end=c['entry'][-1]['line'];tail=[i for i in body if i['line']>end]
    if not tail:return False,'No return suffix'
    if not any(i['op'] in {'movx','lcall','acall'} or (i['op'] in {'ljmp','ajmp','sjmp'} and i['args'].startswith('_')) for i in tail):
        return True,'No further XDATA access or call; private object cannot be read again'
    lines=(inv.source/c['module']).read_text().splitlines();labels={}
    for n,i in enumerate(tail):
        previous=tail[n-1]['line'] if n else end
        for line in lines[previous:i['line']-1]:
            m=re.fullmatch(r'\s*(\d+\$):\s*',line)
            if m:
                if m[1] in labels:return False,'Duplicate local label'
                labels[m[1]]=n
    pending=[(0,0)];seen=set()
    while pending:
        n,changed=pending.pop()
        if (n,changed) in seen:continue
        seen.add((n,changed))
        if n>=len(tail):return False,'Suffix falls out of function with private DPTR'
        i=tail[n];op,args=i['op'],i['args'];parts=args.split(',')
        if not architecture.instruction_format(op,bytes.fromhex(i['bytes'])):return False,'Unknown instruction before private DPTR discarded'
        if op=='mov' and len(parts)==2:
            if parts[0]=='dptr':continue # Complete overwrite: previous address is lost.
            if re.search(r'\b(?:dpl|dph|dptr)\b',parts[1]):return False,'Private object address copied before discard'
            if parts[0] in {'dpl','dph'}:changed|=1 if parts[0]=='dpl' else 2
            if changed==3:continue
        elif re.search(r'\b(?:dpl|dph|dptr)\b',args):return False,'Private DPTR used before complete overwrite'
        if op in {'movx','lcall','acall'}:return False,'Memory/call can observe residual private address'
        if op=='ret':continue
        successors=[]
        if op in {'sjmp','ljmp','ajmp','jz','jnz','jc','jnc','jb','jnb','jbc','djnz','cjne'}:
            if parts[-1] not in labels:return False,'Unresolved control path before private DPTR discarded'
            successors.append(labels[parts[-1]])
        if op not in {'sjmp','ljmp','ajmp'}:successors.append(n+1)
        pending.extend((successor,changed) for successor in successors)
    return True,'Every suffix path discards private DPTR before further memory access/call'


def tool_hashes(toolchain):
    paths=[toolchain/'bin'/name for name in ('sdcc','sdcpp','sdas8051','sdld')]
    paths+=sorted((toolchain/'share/sdcc/lib/large').glob('*.lib'))
    if len(paths)<=4 or any(not p.is_file() for p in paths):
        raise ValueError('Missing pinned compiler/linker/runtime library')
    return {p.relative_to(toolchain).as_posix():sha(p) for p in paths}


def fixed_map(root):
    """AK820 hardware contract; identities must also match the context certificate."""
    paths=['keyboards/ajazz/ak820/ak820_board.h','keyboards/ajazz/ak820/ak820_board.c','lib/ch555/ch555.h']
    header,board,sdk=[(root/name).read_text() for name in paths]
    required=[('#define AK820_LED_DMA_ADDRESS 0x0200',header),('#define AK820_LED_DMA_BYTES 512',header),
              ('LED_DMA_H   = AK820_LED_DMA_ADDRESS >> 8;',board),('LED_DMA_L   = AK820_LED_DMA_ADDRESS & 0xff;',board)]
    if any(text not in body for text,body in required) or not re.search(r'#define pUSB_BUF_BASE\s+\(\(uint8_t __xdata \*\)0x1000\)',sdk):
        raise ValueError('Unproved AK820 reserved XDATA map')
    return {name:sha(root/name) for name in paths}


def absolute_map(tree):
    aliases={}
    for path in sorted(tree.rglob('*.asm')):
        area=''
        for line in path.read_text().splitlines():
            text=line.split(';',1)[0].strip()
            if text.startswith('.area'):area=text.split()[1]
            if area not in {'XSEG','XABS','XISEG'}:continue
            m=re.fullmatch(r'(_\w+)\s*=\s*(0x[0-9a-fA-F]+)',text)
            if m:
                value=int(m[2],16)
                if m[1] in aliases and aliases[m[1]]!=value:raise ValueError('Conflicting absolute XDATA alias')
                aliases[m[1]]=value
            elif '=' in text:raise ValueError('Unknown absolute XDATA alias')
            if area=='XABS' and text and not text.startswith('.area'):raise ValueError('Unbounded absolute XDATA allocation')
            if text.startswith(('.org','.equ')):raise ValueError('Unbounded XDATA directive')
    if aliases!={'_ak820_flash_stage':0x400,'_ak820_led_dma':0x200}:
        raise ValueError('Absolute XDATA aliases differ from accepted fixed allocations')
    return aliases


def make_context_certificate(root,build,stack_path,toolchain,output):
    """Export a reviewable source-lock from a prior exact application IRQ audit.

    This does not approve that image for installation. It binds ALL compiler
    ASM in every module contributing an IRQ instruction, plus tools/runtime and
    reserved-map sources. Changed protected source requires a fresh certificate.
    """
    report=json.loads((build/'build-report.json').read_text());stack=json.loads(stack_path.read_text())
    image=build/'ajazz_ak820_vial.ihx';mapping=image.with_suffix('.map')
    if report['keyboard']!='ajazz/ak820' or report['xram_window']!=[0x440,0x1000]:raise ValueError('Unsupported context configuration')
    tools=tool_hashes(toolchain)
    prior_tools={r['path']:r['sha256'] for r in report['sources'] if r['origin']=='toolchain'}
    if any(prior_tools.get(name)!=digest for name,digest in tools.items()):raise ValueError('Context image compiler/runtime differs from selected toolchain')
    if stack['identity']['ihx_sha256']!=sha(image) or stack['identity']['map_sha256']!=sha(mapping):raise ValueError('IRQ audit image identity mismatch')
    reachable=set()
    for name in IRQ_ROOTS:
        result=stack['roots'].get(name)
        if not result or result['unresolved'] or result['bound'] is None:raise ValueError('Incomplete configured IRQ closure: '+name)
        reachable.update(result['reachable'])
    objects=[root/name for name in report['expected_objects']]
    roots={p.parent for p in objects if p.name=='ak820_board.rel'}
    if len(roots)!=1:raise ValueError('Missing compiler object root')
    obj=roots.pop();protected={};provenance={str(stack_path.resolve()):sha(stack_path),str(image.resolve()):sha(image),str(mapping.resolve()):sha(mapping),str((build/'build-report.json').resolve()):sha(build/'build-report.json')}
    for rst in sorted((build/'dce').rglob('*.rst')):
        relative=rst.relative_to(build).as_posix()
        if stack['identity']['listing_sha256'].get(relative)!=sha(rst):raise ValueError('IRQ audit listing mismatch')
        provenance[str(rst.resolve())]=sha(rst)
        if any(int(m[1],16) in reachable for line in rst.read_text().splitlines() if (m:=audit.LISTED.match(line))):
            module=rst.relative_to(build/'dce').with_suffix('.asm').as_posix();original=obj/module
            if not original.is_file():raise ValueError('IRQ code has no original module identity: '+module)
            protected[module]=canonical(original.read_text())
    if not protected:raise ValueError('No source-locked IRQ modules')
    certificate={'format':FORMAT,'target':'ajazz/ak820','contract':CONTRACT,'irq_roots':list(IRQ_ROOTS),
        'ordinary_xram':[0x440,0x1000],'reserved_xdata':[[0x200,0x400],[0x400,0x440],[0x1000,0x1400]],
        'tools':tool_hashes(toolchain),'map_sources':fixed_map(root),'protected_modules':protected,
        'provenance_sha256':provenance,'application_irq_only':True,'whole_image_qualified':False,'hardware_qualified':False}
    save(output,certificate)
    return certificate


def validate_context(root,obj,source,toolchain,certificate_path):
    cert=json.loads(certificate_path.read_text())
    if (cert.get('format')!=FORMAT or cert.get('target')!='ajazz/ak820' or cert.get('contract')!=CONTRACT
            or cert.get('irq_roots')!=list(IRQ_ROOTS) or cert.get('ordinary_xram')!=[0x440,0x1000]
            or cert.get('reserved_xdata')!=[[0x200,0x400],[0x400,0x440],[0x1000,0x1400]]
            or not cert.get('application_irq_only') or not cert.get('protected_modules')):
        raise ValueError('Incomplete or incompatible spill context certificate')
    if cert['tools']!=tool_hashes(toolchain) or cert['map_sources']!=fixed_map(root):raise ValueError('Compiler/runtime/map context changed')
    if not cert.get('provenance_sha256'):raise ValueError('Missing independently reviewable context provenance')
    for name,digest in cert['provenance_sha256'].items():
        path=Path(name)
        if not path.is_file() or sha(path)!=digest:raise ValueError('Context provenance changed: '+name)
    for module,digest in cert['protected_modules'].items():
        path=(obj/module).resolve()
        if not path.is_relative_to(obj.resolve()) or not path.is_file() or canonical(path.read_text())!=digest:
            raise ValueError('Protected IRQ module changed; require a fresh source-context certificate: '+module)
    absolute_map(source)
    return cert


def compiler_flags(obj):
    # QMK records shell-escaped Make text. No shell executes any of these strings.
    flags=[x.replace('\\"','"') for x in shlex.split((obj/'cflags.txt').read_text())]
    if any(flag.startswith('--sdcccall') for flag in flags):raise ValueError('Mixed calling convention option')
    if '-mmcs51' not in flags or '--model-large' not in flags or any(x in flags for x in ('--stack-auto','--xstack','--model-huge','--model-small','--model-medium')):
        raise ValueError('Unsupported or mixed parameter ABI')
    return flags


def capture(root,obj,module,destination,sdcc,initial_inputs):
    """Feed one frozen preprocessed input to SDCC c1 with typed dumps.

    Relative output naming retains .module identity. Full original noncomment compiler ASM
    must match canonically (including strings, areas, symbols and operands); changed code/options/types never get guessed.
    Only four semantic/provenance files are retained per TU.
    """
    original=obj/module;dep=original.with_suffix('.d');deps=dependency_paths(dep,root)
    before={str(p):sha(p) for p in sorted(deps)}
    for path,digest in before.items():
        p=Path(path)
        if not p.is_relative_to(obj) and initial_inputs.get(p.resolve())!=digest:raise ValueError('Source changed during capture: '+path)
    sources=[p for p in deps if p.suffix=='.c' and p.is_file()]
    # The first prerequisite is the translation unit, unlike included .c files.
    source_name=shlex.split(dep.read_text().replace('\\\n',' ').split(':',1)[1])[0]
    if (root/source_name).resolve() not in sources:raise ValueError('Missing primary C source identity')
    dest=destination/Path(module).parent;dest.mkdir(parents=True,exist_ok=True);stem=Path(module).stem
    flags=compiler_flags(obj)
    for path in deps:
        if re.search(r'\b(?:__DATE__|__TIME__|__TIMESTAMP__)\b',strip_c_literals(path.read_text(encoding='latin-1'))):raise ValueError('Nondeterministic preprocessing builtin in compile inputs')
    dest_dependency=dest/(stem+'.pre.d')
    pre_command=[str(sdcc),*flags,'-E','-Wp,-MD,-MF,'+str(dest_dependency),source_name]
    pre=subprocess.run(pre_command,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=120)
    pre_path=dest/(stem+'.i');pre_path.write_bytes(pre.stdout)
    if dependency_paths(dest_dependency,root)!=deps:raise ValueError('Preprocessor include closure differs from original compile')
    command=[str(sdcc),*flags,'--c1mode','--dump-ast','--dump-i-code','-o',stem+'.asm']
    proc=subprocess.run(command,cwd=dest,input=pre.stdout,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
    ast_path=dest/(stem+'.ast.log');ast_path.write_bytes(proc.stdout)
    if proc.returncode:raise ValueError('Typed SDCC capture failed: '+module)
    assembly=dest/(stem+'.asm');raw=dest/(stem+'.dumpraw0')
    if not assembly.is_file() or not raw.is_file() or canonical(assembly.read_text())!=canonical(original.read_text()):raise ValueError('Typed compiler ASM identity mismatch: '+module)
    if any(sha(Path(p))!=digest for p,digest in before.items()):raise ValueError('Input changed while capturing typed metadata')
    keep={assembly,raw,ast_path,pre_path,dest_dependency}
    for path in dest.glob(stem+'.dump*'):
        if path not in keep:path.unlink()
    record={'module':module,'compiler_sha256':sha(sdcc),'flags':flags,'preprocess_argv':pre_command,'compile_argv':command,
        'input_sha256':before,'original_compiler_asm_sha256':sha(original),'captured_compiler_asm_sha256':sha(assembly),'canonical_compiler_asm_sha256':canonical(assembly.read_text()),'files_sha256':{p.relative_to(destination).as_posix():sha(p) for p in keep}}
    return record


def prepare(root,obj,source,target,metadata_dir,certificate_path,report_path,sdcc,initial_inputs):
    if target.exists() or metadata_dir.exists():raise ValueError('Spill pass outputs must be fresh')
    root,obj,source,target,metadata_dir=[p.resolve() for p in (root,obj,source,target,metadata_dir)]
    if target.is_relative_to(source) or source.is_relative_to(target) or metadata_dir.is_relative_to(source):raise ValueError('Overlapping spill input/output trees')
    context_digest=sha(certificate_path)
    toolchain=sdcc.resolve().parents[1];cert=validate_context(root,obj,source,toolchain,certificate_path)
    inv=inventory(source);all_candidates=candidates(inv);metadata_dir.mkdir(parents=True)
    chosen=[];rejected=[];metadata={};metadata_errors={}
    for module in sorted({c['module'] for c in all_candidates if not EXCLUDED.search(c['module']+' '+c['function']) and c['module'] not in cert['protected_modules']}):
        try:metadata[module]=capture(root,obj,module,metadata_dir,sdcc,initial_inputs)
        except ValueError as exc:metadata_errors[module]=str(exc)
    for c in all_candidates:
        reason=None;module=c['module'];record=metadata.get(module)
        if EXCLUDED.search(module+' '+c['function']):reason='Hardware/IRQ/boot or mixed-ABI scope excluded'
        elif module in cert['protected_modules']:reason='Source-locked IRQ module excluded'
        elif not c['private_unique_symbol_uses']:reason='Private allocation has other references/address uses'
        elif record is None:reason=metadata_errors.get(module,'Missing typed compiler capture')
        else:
            path=metadata_dir/module
            proved,detail=source_proof(c,path.with_suffix('.dumpraw0').read_text(encoding='latin-1'),path.with_suffix('.ast.log').read_text(encoding='latin-1'),path.with_suffix('.i').read_text(encoding='latin-1'))
            if not proved:reason=detail
            if reason is None:
                proved,detail=opcode_proof(c,source)
                if not proved:reason=detail
            if reason is None:
                proved,detail=tail_private_access(c,inv)
                if not proved:reason=detail
        if reason:rejected.append({'module':module,'function':c['function'],'reason':reason})
        else:chosen.append(c)
    shutil.copytree(source,target,ignore=shutil.ignore_patterns('*.rel','*.lst','*.rst','*.sym'))
    outputs={};changes=collections.defaultdict(list)
    for c in chosen:changes[c['module']].append(c)
    for module,hashes in inv.hashes.items():
        original=source/module
        if sha(original)!=hashes['asm_sha256'] or sha(original.with_suffix('.lst'))!=hashes['lst_sha256']:raise ValueError('Spill input changed during proof')
        lines=original.read_text().splitlines(keepends=True);replacements={};used=set()
        for c in changes[module]:
            first,last=c['entry'][0]['line'],c['entry'][-1]['line'];region=set(range(first,last+1))
            if used&region:raise ValueError('Overlapping parameter spill windows')
            used|=region;replacements[first]=(last,'\t'+'\n\t'.join(c['boundary_state_replacement_only'])+'\n')
        result=[];n=1
        while n<=len(lines):
            if n in replacements:
                last,text=replacements[n];result.append(text);n=last+1
            else:result.append(lines[n-1]);n+=1
        (target/module).write_text(''.join(result));outputs[module]=sha(target/module)
    if sha(certificate_path)!=context_digest:raise ValueError('Spill context changed during proof')
    metadata_manifest={'compiler_sha256':sha(sdcc),'modules':metadata,'rejected':metadata_errors}
    save(metadata_dir/'manifest.json',metadata_manifest)
    result={'algorithm':ALGORITHM,'context_sha256':sha(certificate_path),'metadata_manifest_sha256':sha(metadata_dir/'manifest.json'),
        'input_sha256':inv.hashes,'output_sha256':outputs,'selected':chosen,'rejected':rejected,
        'nominal_object_saved_bytes':sum(c['net_bytes'] for c in chosen),'extra_stack_bytes':0,'postlink_qualified':False,'hardware_qualified':False,'linked_saved_bytes':None}
    save(report_path,result)
    return result


def verify_assembled(source,target,report_path,report):
    def areas(path):
        return {m[1]:(int(m[2],16),m[3],m[4]) for m in re.finditer(r'^A (\S+) size ([0-9A-Fa-f]+) flags ([0-9A-Fa-f]+) addr ([0-9A-Fa-f]+)$',path.read_text(),re.M)}
    expected=collections.Counter()
    for c in report['selected']:expected[c['module']]+=c['net_bytes']
    measurements={}
    for module,inputs in report['input_sha256'].items():
        before,after=source/module,target/module
        if sha(before)!=inputs['asm_sha256'] or sha(before.with_suffix('.lst'))!=inputs['lst_sha256'] or sha(after)!=report['output_sha256'][module]:raise ValueError('Spill provenance changed')
        first,last=areas(before.with_suffix('.rel')),areas(after.with_suffix('.rel'))
        if 'CSEG' not in first or 'CSEG' not in last:raise ValueError('Missing CSEG')
        delta=first['CSEG'][0]-last['CSEG'][0]
        if delta!=expected[module]:raise ValueError('Unexpected spill object delta: '+module)
        first.pop('CSEG');last.pop('CSEG')
        if first!=last:raise ValueError('Spill pass changed storage or another CODE area')
        measurements[module]={'object_saved_bytes':delta,'input_rel_sha256':sha(before.with_suffix('.rel')),'output_rel_sha256':sha(after.with_suffix('.rel')),'output_lst_sha256':sha(after.with_suffix('.lst'))}
    # Fresh listings must still match exact rewritten ASM spelling/addresses.
    inventory(target)
    report['assembled_objects']=measurements;report['object_saved_bytes']=sum(m['object_saved_bytes'] for m in measurements.values());save(report_path,report)
    return report


def postlink_audit(root,build,certificate_path,report_path,report,stack_path):
    """Bind the NEW exact image; old context never substitutes for this check."""
    cert=json.loads(certificate_path.read_text());stack=json.loads(stack_path.read_text());image=build/'ajazz_ak820_vial.ihx';mapping=image.with_suffix('.map')
    if report['context_sha256']!=sha(certificate_path) or stack['identity']['ihx_sha256']!=sha(image) or stack['identity']['map_sha256']!=sha(mapping):raise ValueError('Postlink spill/image identity mismatch')
    reachable=set()
    for root_name in IRQ_ROOTS:
        result=stack['roots'].get(root_name)
        if not result or result['unresolved'] or result['bound'] is None:raise ValueError('Unproved new-image IRQ closure')
        reachable.update(result['reachable'])
    if cert['map_sources']!=fixed_map(root):raise ValueError('Reserved map source changed during linking')
    bindings=[]
    for c in report['selected']:
        rst=(build/'dce'/c['module']).with_suffix('.rst');relative=rst.relative_to(build).as_posix()
        if stack['identity']['listing_sha256'].get(relative)!=sha(rst):raise ValueError('Postlink listing identity mismatch')
        text=rst.read_text()
        def address(symbol):
            matches=re.findall(r'^\s*([0-9A-F]{6})\s+\d+ '+re.escape(symbol)+r':\s*$',text,re.M)
            if len(matches)!=1:raise ValueError('Missing/ambiguous linked spill symbol')
            return int(matches[0],16)
        entry=address(c['function']);obj=address(c['object'])
        if entry in reachable:raise ValueError('Rewritten function became IRQ-reachable')
        if not cert['ordinary_xram'][0]<=obj or obj+c['width']>cert['ordinary_xram'][1]:raise ValueError('Private object overlaps reserved memory')
        if any(start<obj+c['width'] and obj<end for start,end in cert['reserved_xdata']):raise ValueError('Private object overlaps DMA/flash/FIFO')
        bindings.append({'module':c['module'],'function':c['function'],'object':c['object'],'function_address':entry,'object_address':obj,'width':c['width'],'listing_sha256':sha(rst)})
    report['postlink_qualified']=True;report['postlink']={'ihx_sha256':sha(image),'map_sha256':sha(mapping),'stack_report_sha256':sha(stack_path),'bindings':bindings,'scope':'Application IRQ closure and private-object placement only; startup/wrappers/nesting/stack capacity/hardware remain separate.'};save(report_path,report)
    return report
