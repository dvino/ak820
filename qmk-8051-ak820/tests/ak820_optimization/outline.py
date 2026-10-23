#!/usr/bin/env python3
"""Verify every outlined helper/replacement and compare its linked CPU effects.

The input is pre-outline ASM with assembler .lst (or linked .rst) listings. The
output image supplies current symbol addresses. Only immediate relocations are
accepted by the outliner, so independently folding those expressions reconstructs
the expected helper bytes without relinking a second firmware image.
"""
from __future__ import annotations
import argparse
import ast
import gzip
import hashlib
import importlib.util
import json
import operator
from pathlib import Path
import random
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1] / "util"))
import ak820_outline_audit as outlining
_spec=importlib.util.spec_from_file_location("ak820_emitted_support",HERE.parent / "ak820_emitted/run.py")
_module=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_module)
Firmware,memory=_module.Firmware,_module.memory


def resolve(expression,symbols):
    expression=outlining.SYMBOL.sub(lambda m:str(symbols[m[0]]),expression)
    ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.LShift:operator.lshift,
         ast.RShift:operator.rshift,ast.BitOr:operator.or_,ast.BitAnd:operator.and_,ast.BitXor:operator.xor}
    def evaluate(node):
        if isinstance(node,ast.Constant) and isinstance(node.value,int):return node.value
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd,ast.Invert)):
            value=evaluate(node.operand)
            return -value if isinstance(node.op,ast.USub) else ~value if isinstance(node.op,ast.Invert) else value
        if isinstance(node,ast.BinOp) and type(node.op) in ops:return ops[type(node.op)](evaluate(node.left),evaluate(node.right))
        raise ValueError("Unrecognized assembler immediate expression: "+expression)
    return evaluate(ast.parse(expression,mode="eval").body)


def linked_locals(firmware):
    result={}
    for listing in sorted((firmware.build / "dce").rglob("*.rst")):
        symbols=dict(firmware.symbols)
        for address,name in re.findall(r"^\s*([0-9A-F]{6})\s+\d+\s+(_[\w$]+):",listing.read_text(),re.M):
            symbols[name]=int(address,16)
        result[listing.relative_to(firmware.build / "dce").with_suffix(".asm").as_posix()]=symbols
    return result


def relocate(instruction,symbols):
    encoded=bytearray(instruction.data)
    immediate=[operand[1:] for operand in instruction.operands.split(",") if operand.startswith("#")]
    if immediate:
        assert len(immediate)==1
        width=2 if instruction.opcode=="mov" and instruction.operands.startswith("dptr,#") else 1
        value=resolve(immediate[0],symbols)&((1<<(8*width))-1)
        encoded[-width:]=value.to_bytes(width,"big")
    return bytes(encoded)


def integrity(firmware,input_dce,manifest,suffix):
    blocks,_=outlining.parse_dce(input_dce,suffix)
    starts={(insn.module,insn.line+1):(block,index) for block in blocks for index,insn in enumerate(block)}
    locals_by_module=linked_locals(firmware)
    helpers=[];expected_calls={}
    for index,group in enumerate(manifest["selected_exact"]):
        name=f"_ak820_outline_{index:04d}";entry=firmware.address(name)
        expected=None
        for location in group["locations"]:
            block,position=starts[(location["module"],location["line"])]
            sequence=block[position:position+len(group["body"])]
            assert [i.assembly for i in sequence]==group["body"],(name,location)
            encoded=b"".join(relocate(i,locals_by_module[location["module"]]) for i in sequence)+bytes([0x22])
            if expected is None:expected=encoded
            assert encoded==expected,("Relocations disagree between callers",name,location)
        actual=bytes(firmware.code[entry+i] for i in range(len(expected)))
        assert actual==expected,("Linked helper differs from relocated original instructions",name,actual.hex(),expected.hex())
        expected_calls[name]=len(group["locations"])
        helpers.append({"name":name,"address":entry,"body":expected[:-1],"sites":len(group["locations"]),"saving":group["nominal_net_bytes"]})
    actual_calls={name:0 for name in expected_calls}
    for listing in sorted((firmware.build/"dce").rglob("*.rst")):
        for line in listing.read_text().splitlines():
            match=outlining.LISTED.match(line)
            if not match or match[4].lower()!="lcall":continue
            target=match[5].strip()
            if target not in actual_calls:continue
            address=int(match[1],16);destination=firmware.address(target)
            expected=bytes([0x12,destination>>8,destination&255])
            assert bytes(firmware.code[address+i] for i in range(3))==expected
            actual_calls[target]+=1
    assert actual_calls==expected_calls,(actual_calls,expected_calls)
    for relative,digest in manifest.get("input_asm_sha256",{}).items():
        assert hashlib.sha256((input_dce/relative).read_bytes()).hexdigest()==digest
    return helpers


def snapshot(log,label,address,count):
    marker="@@"+label
    if marker not in log:raise ValueError("Missing observation: "+label)
    tail=log.rsplit(marker,1)[1].split("\necho @@",1)[0]
    result=bytearray()
    for match in re.finditer(r"^0x([0-9a-f]+)\s+(?:(?:\w+):\s+0b[01]+\s+0x([0-9a-f]{2})|((?:[0-9a-f]{2}\s+)+))",tail,re.M):
        row=int(match[1],16)
        if row!=address+len(result):
            if result:raise ValueError("Discontinuous memory observation: "+label)
            continue
        values=bytes.fromhex(match[2] or match[3])[:16]
        result.extend(values[:count-len(result)])
        if len(result)==count:return bytes(result)
    raise ValueError("Incomplete memory observation: "+label)


def differential(firmware,helper,cases):
    commands=[]
    # The inline path and linked helper receive identical state. All four
    # register banks, carry values, DPTR wrap and whole 64 KiB XRAM are compared.
    # SP=0x7f keeps the two permitted return-address bytes outside IRAM0..31.
    snapshots=[("banks","iram",0,32),("sp","sfr",0x81,3),
               ("psw","sfr",0xd0,1),("a","sfr",0xe0,1),("b","sfr",0xf0,1),
               ("xram","xram",0,65536)]
    for seed in range(cases):
        rng=random.Random(0x820000+seed)
        registers=[rng.randrange(256) for _ in range(32)]
        dptr=[0x0000,0xffff,0x00ff,0x0fff][seed%4] if seed<4 else rng.randrange(65536)
        for mode in ("inline","outlined"):
            commands += [f"fill xram 0 0xffff {(seed*29+165)&255}",memory("iram",0,registers),
                         memory("sfr",0x81,[0x7f,dptr&255,dptr>>8]),
                         memory("sfr",0xe0,[(seed*73+91)&255]),
                         memory("sfr",0xf0,[(seed*31+37)&255]),
                         memory("sfr",0xd0,[(seed%4)<<3 | ((seed//4)%2)<<7 | ((seed//8)%2)<<2])]
            if mode=="inline":code=list(helper["body"])
            else:code=[0x12,helper["address"]>>8,helper["address"]&255]
            commands += [memory("rom",0x2000,code+[0x02,0x27,0]),"run 0x2000 0x2700"]
            for tag,space,address,count in snapshots:
                commands+=firmware.dump(f"{seed}_{mode}_{tag}@",space,address,count)
    log,_=firmware.execute(helper["name"],commands)
    for seed in range(cases):
        for tag,space,address,count in snapshots:
            inline=snapshot(log,f"{seed}_inline_{tag}@",address,count)
            outlined=snapshot(log,f"{seed}_outlined_{tag}@",address,count)
            assert inline==outlined,(helper["name"],seed,tag)
    # Preserve complete observations without hundreds of MB of repetitive text.
    path=firmware.output/(helper["name"]+".log")
    compressed=path.with_suffix(".log.gz")
    compressed.write_bytes(gzip.compress(path.read_bytes(),mtime=0));path.unlink()
    return {"name":helper["name"],"pass":True,"state_cases":cases,"call_sites":helper["sites"],
            "body_bytes":len(helper["body"]),"nominal_net_bytes":helper["saving"],
            "linked_body_hex":helper["body"].hex(),"complete_log_sha256":hashlib.sha256(compressed.read_bytes()).hexdigest()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir",type=Path,required=True)
    parser.add_argument("--input-dce",type=Path,required=True)
    parser.add_argument("--manifest",type=Path)
    parser.add_argument("--listing-suffix",choices=(".lst",".rst"),default=".lst")
    parser.add_argument("--s51",type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True)
    parser.add_argument("--state-cases",type=int,default=16)
    args=parser.parse_args()
    if args.state_cases<8:parser.error("At least eight cases cover all banks and both carry states")
    build=args.build_dir.resolve();output=args.output_dir.resolve()
    manifest_path=(args.manifest or build/"dce/outlining.json").resolve()
    manifest=json.loads(manifest_path.read_text())
    firmware=Firmware(build,args.s51.resolve(),output)
    helpers=integrity(firmware,args.input_dce.resolve(),manifest,args.listing_suffix)
    tests=[]
    for helper in helpers:tests.append(differential(firmware,helper,args.state_cases))
    report={"pass":True,"linked_image_sha256":hashlib.sha256(firmware.image.read_bytes()).hexdigest(),
            "runner_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "outline_manifest_sha256":hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            "verified_helpers":len(helpers),"verified_replacements":sum(h["sites"] for h in helpers),
            "nominal_net_bytes":sum(h["saving"] for h in helpers),"tests":tests,
            "limits":"CPU and relocation equivalence of chosen straight-line blocks; LCALL adds two live stack bytes. No physical timing, interrupt latency, USB, flash or DMA validation."}
    (output/"results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k!="tests"},indent=2))

if __name__=="__main__":main()
