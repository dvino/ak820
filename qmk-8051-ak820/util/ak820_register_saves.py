#!/usr/bin/env python3
"""Opt-in conservative register-save trimming on assembled SDCC output.

A finite 8051 decoder, complete local CFG, balanced private stack and transitive
call closure prove preservation. Unknown instructions, aliases, indirect IRAM,
stack inspection, PSW/bank changes and unknown calls reject whole functions.
Valid ABI stack storage and ordinary interrupt preservation are prerequisites;
this component pass never qualifies full-image stack or device behavior.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import ak820_outline_audit as audit


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


LOCAL = re.compile(r'\d+\$')
DIRECT = {'a':0xe0,'acc':0xe0,'b':0xf0,'dpl':0x82,'dph':0x83,**{f'ar{i}':i for i in range(8)}}
BRANCHES = {'sjmp','ljmp','jc','jnc','jz','jnz','djnz','cjne'}


def number(text):
    return int(text,0) if re.fullmatch(r'0x[0-9a-f]+|[0-9]+',text) else None


def decode(op,args,data,address=None,labels=None):
    """Written R indices, or None; verify every byte of the finite subset.

    Only LCALL's relocated destination bytes are not independently decoded:
    its exact symbol is matched against the source and resolved in call closure.
    Local control transfers have their exact target and displacement checked.
    No destination denotes arbitrary DATA, BIT, SFR or indirect IRAM storage.
    """
    writes=set(); expected=None
    parts=args.split(',') if args else []
    reg=lambda x: int(x[1]) if re.fullmatch(r'r[0-7]',x) else None
    imm=lambda x: number(x[1:]) if x.startswith('#') else None
    if op=='ret' and not args: expected=b'\x22'
    elif op=='nop' and not args: expected=b'\x00'
    elif op=='lcall' and re.fullmatch(r'_[a-z_]\w*',args):
        return set() if len(data)==3 and data[0]==0x12 else None
    elif op in {'push','pop'} and re.fullmatch(r'ar[0-7]',args):
        expected=bytes([0xc0 if op=='push' else 0xd0,int(args[-1])])
        if op=='pop':writes.add(int(args[-1]))
    elif op in BRANCHES:
        if not parts or not LOCAL.fullmatch(parts[-1]) or labels is None or parts[-1] not in labels or address is None: return None
        target=labels[parts[-1]]
        if op=='ljmp' and len(parts)==1: expected=bytes([2,target>>8,target&255])
        else:
            prefix=None
            if op in {'sjmp','jc','jnc','jz','jnz'} and len(parts)==1:
                prefix=[{'sjmp':0x80,'jc':0x40,'jnc':0x50,'jz':0x60,'jnz':0x70}[op]]
            elif op=='djnz' and len(parts)==2 and reg(parts[0]) is not None:
                r=reg(parts[0]);prefix=[0xd8+r];writes.add(r)
            elif op=='cjne' and len(parts)==3 and imm(parts[1]) is not None and 0<=imm(parts[1])<=255:
                if parts[0]=='a':prefix=[0xb4,imm(parts[1])]
                elif reg(parts[0]) is not None:prefix=[0xb8+reg(parts[0]),imm(parts[1])]
            if prefix is not None:
                delta=target-(address+len(prefix)+1)
                if -128<=delta<=127:expected=bytes(prefix+[delta&255])
    elif op=='mov' and len(parts)==2:
        dst,src=parts;rd,rs=reg(dst),reg(src);value=imm(src)
        if value is not None and not 0<=value<=255 and dst!='dptr': return None
        if dst=='dptr' and value is not None and 0<=value<=65535:expected=bytes([0x90,value>>8,value&255])
        elif rd is not None and value is not None:expected=bytes([0x78+rd,value]);writes.add(rd)
        elif rd is not None and src=='a':expected=bytes([0xf8+rd]);writes.add(rd)
        elif dst=='a' and rs is not None:expected=bytes([0xe8+rs])
        elif dst=='a' and value is not None:expected=bytes([0x74,value])
        elif dst=='dptr' and re.fullmatch(r'#(?:_[a-z_]\w*|\(_[a-z_]\w*\+0x[0-9a-f]+\))',src):
            return set() if len(data)==3 and data[0]==0x90 else None
        elif dst in DIRECT and value is not None:
            expected=bytes([0x75,DIRECT[dst],value])
            if dst.startswith('ar'):writes.add(int(dst[-1]))
        elif dst=='a' and src in DIRECT:expected=bytes([0xe5,DIRECT[src]])
        elif dst in DIRECT and src=='a':expected=bytes([0xf5,DIRECT[dst]])
        elif dst in DIRECT and src in DIRECT:expected=bytes([0x85,DIRECT[src],DIRECT[dst]])
        elif dst in DIRECT and rs is not None:expected=bytes([0x88+rs,DIRECT[dst]])
        elif rd is not None and src in DIRECT:expected=bytes([0xa8+rd,DIRECT[src]]);writes.add(rd)
        elif dst in DIRECT and src=='a':expected=bytes([0xf5,DIRECT[dst]])
        elif dst=='a' and src in DIRECT:expected=bytes([0xe5,DIRECT[src]])
        if expected is not None and dst.startswith('ar'):writes.add(int(dst[-1]))
    elif op=='movx' and args=='a,@dptr':expected=b'\xe0'
    elif op=='movc' and args=='a,@a+dptr':expected=b'\x93'
    elif op in {'inc','dec'}:
        r=reg(args)
        if r is not None:expected=bytes([(0x08 if op=='inc' else 0x18)+r]);writes.add(r)
        elif args=='a':expected=bytes([4 if op=='inc' else 0x14])
        elif op=='inc' and args=='dptr':expected=b'\xa3'
    elif op in {'add','addc','subb','anl','orl','xrl'} and len(parts)==2 and parts[0]=='a':
        base={'add':0x24,'addc':0x34,'subb':0x94,'anl':0x54,'orl':0x44,'xrl':0x64}[op]
        src=parts[1];value=imm(src);r=reg(src)
        if value is not None and 0<=value<=255:expected=bytes([base,value])
        elif r is not None:expected=bytes([base+4+r])
        elif src in DIRECT:expected=bytes([base+1,DIRECT[src]])
    elif (op,args) in {('clr','a'),('cpl','a'),('clr','c'),('cpl','c'),('setb','c'),('rl','a'),('rr','a'),('rlc','a'),('rrc','a'),('swap','a'),('mul','ab'),('div','ab')}:
        expected=bytes([{('clr','a'):0xe4,('cpl','a'):0xf4,('clr','c'):0xc3,('cpl','c'):0xb3,('setb','c'):0xd3,('rl','a'):0x23,('rr','a'):3,('rlc','a'):0x33,('rrc','a'):0x13,('swap','a'):0xc4,('mul','ab'):0xa4,('div','ab'):0x84}[(op,args)]])
    return writes if expected is not None and data==expected else None


def instruction_format(op, data):
    """Independent opcode/length classification, including caller-only ops."""
    table={0x00:('nop',1),0x02:('ljmp',3),0x03:('rr',1),0x04:('inc',1),0x05:('inc',2),0x06:('inc',1),0x07:('inc',1),
           0x10:('jbc',3),0x12:('lcall',3),0x13:('rrc',1),0x14:('dec',1),0x15:('dec',2),0x16:('dec',1),0x17:('dec',1),
           0x20:('jb',3),0x22:('ret',1),0x23:('rl',1),0x30:('jnb',3),0x33:('rlc',1),
           0x40:('jc',2),0x50:('jnc',2),0x60:('jz',2),0x70:('jnz',2),0x80:('sjmp',2),
           0x74:('mov',2),0x75:('mov',3),0x76:('mov',2),0x77:('mov',2),0x85:('mov',3),0x86:('mov',2),0x87:('mov',2),0x90:('mov',3),
           0xa2:('mov',2),0x92:('mov',2),0xa3:('inc',1),0x93:('movc',1),0x83:('movc',1),0x84:('div',1),0xa4:('mul',1),
           0xb2:('cpl',2),0xb3:('cpl',1),0xc2:('clr',2),0xc3:('clr',1),0xc4:('swap',1),0xc0:('push',2),0xd0:('pop',2),
           0xd2:('setb',2),0xd3:('setb',1),0xd4:('da',1),0xd5:('djnz',3),0xe0:('movx',1),0xe2:('movx',1),0xe3:('movx',1),0xe4:('clr',1),
           0xe5:('mov',2),0xe6:('mov',1),0xe7:('mov',1),0xf0:('movx',1),0xf2:('movx',1),0xf3:('movx',1),0xf4:('cpl',1),0xf5:('mov',2),0xf6:('mov',1),0xf7:('mov',1)}
    for base,name in [(0x08,'inc'),(0x18,'dec'),(0x78,'mov'),(0x88,'mov'),(0xa8,'mov'),(0xb8,'cjne'),(0xc8,'xch'),(0xd8,'djnz'),(0xe8,'mov'),(0xf8,'mov')]:
        for r in range(8):table[base+r]=(name,3 if base==0xb8 else 2 if base in {0x78,0x88,0xa8,0xd8} else 1)
    for base,name in [(0x24,'add'),(0x34,'addc'),(0x44,'orl'),(0x54,'anl'),(0x64,'xrl'),(0x94,'subb')]:
        table[base]=(name,2);table[base+1]=(name,2)
        for k in range(2,12):table[base+k]=(name,1)
    for base,name in [(0x42,'orl'),(0x52,'anl'),(0x62,'xrl')]:table[base]=(name,2);table[base+1]=(name,3)
    for opcode,name in [(0x72,'orl'),(0x82,'anl'),(0xa0,'orl'),(0xb0,'anl')]:table[opcode]=(name,2)
    for opcode in range(0xb4,0xb8):table[opcode]=('cjne',3)
    for opcode in (0xc5,0xc6,0xc7):table[opcode]=('xch',2 if opcode==0xc5 else 1)
    return bool(data) and table.get(data[0])==(op,len(data))


def validate(f, effects=True):
    body=f['body'];labels=f['labels']
    if not body or len(body)>2000:return False
    addresses={i['address']:n for n,i in enumerate(body)}
    if len(addresses)!=len(body):return False
    for i in body:
        if not instruction_format(i['op'],bytes.fromhex(i['bytes'])):return False
        effect=decode(i['op'],i['args'],bytes.fromhex(i['bytes']),i['address'],labels)
        if effect is None and effects:return False
        if not effects and i['op'] not in audit.SAFE_OPS | {'push','pop','ret','lcall','setb','jbc','jb','jnb','cjne','djnz'} | BRANCHES:return False
        if i['op'] in {'jbc','jb','jnb'}:
            if effects:return False
            parts=i['args'].split(',')
            if len(parts)!=2 or parts[-1] not in labels:return False
            target=labels[parts[-1]];data=bytes.fromhex(i['bytes']);delta=target-i['address']-3
            if len(data)!=3 or data[0]!={'jb':0x20,'jnb':0x30,'jbc':0x10}[i['op']] or not -128<=delta<=127 or data[-1]!=delta&255:return False
        elif i['op'] in BRANCHES and effect is None:
            # For caller-only arithmetic variants of CJNE/DJNZ, validate the
            # branch format and exact local target even if DATA effects unknown.
            parts=i['args'].split(',');data=bytes.fromhex(i['bytes']);target=labels.get(parts[-1])
            if target is None:return False
            expected_size=3 if i['op']=='cjne' or (i['op']=='djnz' and not re.fullmatch(r'r[0-7]',parts[0])) else 2
            if len(data)!=expected_size or i['op'] not in {'cjne','djnz'}:return False
            if i['op']=='cjne' and not 0xb4<=data[0]<=0xbf:return False
            if i['op']=='djnz' and data[0]!=0xd5:return False
            delta=target-i['address']-expected_size
            if not -128<=delta<=127 or data[-1]!=delta&255:return False
        i['writes']=sorted(effect or [])
    # Worklist proves every reachable instruction uses a matching private
    # register stack. Every join has exactly one stack shape. No underflow,
    # stack-dependent address, inter-function jump or unbalanced return exists.
    states={0:()};pending=[0];returns=0
    while pending:
        n=pending.pop();i=body[n];stack=states[n];op=i['op']
        if op=='push':stack=stack+(i['args'],)
        elif op=='pop':
            if not stack or stack[-1]!=i['args']:return False
            stack=stack[:-1]
        if len(stack)>32:return False
        if op=='ret':
            if stack:return False
            returns+=1;continue
        successors=[]
        if op in BRANCHES | {'jb','jnb','jbc'}:
            destination=labels.get(i['args'].split(',')[-1])
            if destination not in addresses:return False
            successors.append(addresses[destination])
        if op not in {'sjmp','ljmp'}:successors.append(n+1)
        for successor in successors:
            if successor>=len(body):return False
            if successor in states:
                if states[successor]!=stack:return False
            else:states[successor]=stack;pending.append(successor)
    # Unreachable instructions are rejected, rather than treated as proofs of
    # dead code that could have another entry or hide an assembler directive.
    return returns>0 and len(states)==len(body)


def load(source):
    functions={};inputs={};duplicates=set()
    for path in sorted(source.rglob('*.asm')):
        module=path.relative_to(source).as_posix();lines=path.read_text().splitlines(keepends=True)
        listing=path.with_suffix('.lst')
        if not listing.is_file():raise ValueError('Missing listing: '+module)
        inputs[module]={'asm_sha256':sha(path),'lst_sha256':sha(listing)}
        listed={}
        for text in listing.read_text().splitlines():
            m=audit.LISTED.match(text)
            if not m:continue
            n=int(m[3])-1
            if n in listed or not 0<=n<len(lines):raise ValueError('Ambiguous listing: '+module)
            data=bytes.fromhex(re.sub('[rstup*]','',m[2]));op=m[4].lower();args=re.sub(r'\s+','',m[5].split(';',1)[0]).lower()
            actual=lines[n].split(';',1)[0].strip().lower().split(None,1)
            if not actual or actual[0]!=op or re.sub(r'\s+','',actual[1] if len(actual)>1 else '')!=args:raise ValueError('ASM/listing mismatch: '+module)
            listed[n]=(int(m[1],16),data,op,args)
        current=None;area='';marker=None;pending_labels=[]
        bad_alias=any(re.match(r'\s*(?:r[0-7]|a|acc|b|dpl|dph|dptr)\s*=',l,re.I) or
                      (re.match(r'\s*ar[0-7]\s*=',l,re.I) and not re.fullmatch(r'\s*ar([0-7])\s*=\s*0x0\1\s*',l.split(';',1)[0],re.I)) for l in lines)
        for n,line in enumerate(lines):
            text=line.split(';',1)[0].strip().lower();fn=re.fullmatch(r';\s*function\s+(\w+)\s*',line.strip(),re.I)
            if fn:marker='_'+fn[1].lower();current=None;pending_labels=[]
            if not text:continue
            if text.startswith('.area'):
                fields=text.split();area=fields[1] if len(fields)>1 else '';current=None;marker=None;pending_labels=[];continue
            if re.fullmatch(r'_[a-z_]\w*::?',text) and area=='cseg':
                name=text.rstrip(':')
                if name in functions:duplicates.add(name)
                current={'module':module,'name':name,'body':[],'labels':{},'valid':marker==name and not bad_alias and audit.eligible_module(module,name[1:]) and not re.search(r'irq|interrupt|naked|usb|timer|flash|boot|nvm|iap',name)}
                functions[name]=current;marker=None;pending_labels=[];continue
            if current is None:continue
            if re.fullmatch(r'ar([0-7])\s*=\s*0x0\1',text):continue
            if re.fullmatch(r'\d+\$:',text):pending_labels.append(text[:-1]);continue
            item=listed.get(n)
            if item is None:current['valid']=False;continue
            address,data,op,args=item;body=current['body']
            if body and address!=body[-1]['address']+len(bytes.fromhex(body[-1]['bytes'])):current['valid']=False
            for label in pending_labels:
                if label in current['labels']:current['valid']=False
                current['labels'][label]=address
            pending_labels=[]
            body.append({'line':n+1,'address':address,'bytes':data.hex(),'op':op,'args':args,'writes':[]})
    for name,f in functions.items():
        provenance=f['valid'] and name not in duplicates
        f['caller_valid']=provenance and validate(f,effects=False)
        f['valid']=provenance and validate(f)
    return functions,inputs

def prepare(source: Path,target: Path,report_path: Path):
    if target.exists(): raise ValueError('Register-save destination exists')
    functions,inputs=load(source)
    memo={}
    def clobber(name,active=()):
        if name in memo: return memo[name]
        f=functions.get(name)
        if name in active or f is None or not f['valid']: return None
        result=set()
        for i in f['body']:
            result.update(i['writes'])
            if i['op']=='lcall':
                other=clobber(i['args'],active+(name,))
                if other is None: return None
                result.update(other)
        memo[name]=result
        return result
    groups=[]; removed={}
    for name,f in functions.items():
        if not f['caller_valid']: continue
        body=f['body']; p=0
        while p<len(body):
            if body[p]['op']!='push': p+=1; continue
            start=p; regs=[]
            while p<len(body) and body[p]['op']=='push': regs.append(body[p]['args']); p+=1
            mid=p
            while p<len(body) and body[p]['op'] not in {'pop','push','ret'} and p-mid<30: p+=1
            end=p+len(regs)
            if any(i['op'] in BRANCHES | {'jb','jnb','jbc'} or decode(i['op'],i['args'],bytes.fromhex(i['bytes']),i['address'],f['labels']) is None for i in body[start:end]): continue
            if any(body[start]['address'] < address <= body[min(end-1,len(body)-1)]['address'] for address in f['labels'].values()): continue
            if len(set(regs)) != len(regs) or [i['args'] for i in body[p:end] if i['op']=='pop'] != list(reversed(regs)): continue
            calls=[i for i in body[mid:p] if i['op']=='lcall']
            if len(calls)!=1: continue
            effects=clobber(calls[0]['args'])
            if effects is None: continue
            effects=effects | set().union(*(set(i['writes']) for i in body[mid:p]))
            safe=[r for r in regs if int(r[-1]) not in effects]
            if not safe: continue
            selected=[i for i in body[start:mid]+body[p:end] if i['args'] in safe]
            removed.setdefault(f['module'],set()).update(i['line'] for i in selected)
            groups.append({'module':f['module'],'caller':name,'callee':calls[0]['args'],'preserved':safe,'removed':selected,'transitive_clobbers':sorted(effects)})
            p=end
    shutil.copytree(source,target,ignore=shutil.ignore_patterns('*.rel','*.lst','*.rst','*.sym'))
    outputs={}
    for module in inputs:
        lines=(source/module).read_text().splitlines(keepends=True)
        (target/module).write_text(''.join(l for n,l in enumerate(lines,1) if n not in removed.get(module,set())))
        outputs[module]=sha(target/module)
    report={'algorithm':'experimental-cfg-register-saves-v1','inputs':inputs,'outputs_sha256':outputs,'groups':groups,'estimated_object_saved_bytes':sum(len(g['removed'])*2 for g in groups),'extra_stack_bytes':0,'linked_saved_bytes':None,'hardware_validated':False}
    report_path.write_text(json.dumps(report,indent=2)+'\n')
    return report


def verify_assembled(source,target,report_path,report):
    # Reuse strict input/output hash and CSEG delta checks, then independently
    # parse every output listing and check each surviving instruction spelling.
    import ak820_tailshare as tail
    proxy=dict(report)
    proxy['groups']=[dict(g,estimated_object_saved_bytes=len(g['removed'])*2) for g in report['groups']]
    tail.verify_assembled(source,target,report_path,proxy)
    original_functions,_ = load(source)
    output_functions,_ = load(target)
    for name, original in original_functions.items():
        if not original['valid'] and not any(g['caller']==name for g in report['groups']):
            continue
        final=output_functions.get(name)
        if final is None or not final['caller_valid'] or (original['valid'] and not final['valid']):
            raise ValueError('Reassembled caller no longer proven: '+name)
        # Include every group in this caller when checking its surviving body.
        removed={i['line'] for g in report['groups'] if g['caller']==name for i in g['removed']}
        before=[i for i in original_functions[name]['body'] if i['line'] not in removed]
        after=final['body']
        if len(before)!=len(after): raise ValueError('Unexpected instruction count: '+name)
        for a,b in zip(before,after):
            if (a['op'],a['args']) != (b['op'],b['args']) or (a['op'] not in BRANCHES | {'lcall','jb','jnb','jbc'} and a['bytes']!=b['bytes']):
                raise ValueError('Unexpected reassembled instruction: '+name)
    report['assembled_objects']=proxy['assembled_objects']
    report['object_saved_bytes']=proxy['object_saved_bytes']
    report_path.write_text(json.dumps(report,indent=2)+'\n')
