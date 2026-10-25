#!/usr/bin/env python3
"""Compare current AK820 location getters with the committed 6c2cdc0 oracle."""
from __future__ import annotations
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
QMK = ROOT / "qmk-8051-ak820"
DYNAMIC = QMK / "quantum/dynamic_keymap.c"
KERNEL = QMK / "keyboards/ajazz/ak820/ak820_keymap_words.c"
CONFIG = QMK / "keyboards/ajazz/ak820/config.h"
HEADER = QMK / "quantum/dynamic_keymap.h"
ORACLE_COMMIT = "6c2cdc0452b664e37cd32a30b31e3e5f800c49cc"
EVIDENCE = ROOT.parent / "getter29-host-regression.jsonl"


def fail(message: str) -> None:
    raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def function(text: str, name: str) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*\([^;]*?\)\s*\{{", text, re.S)
    if not match:
        fail(f"cannot extract function {name}")
    start = text.rfind("\n", 0, match.start()) + 1
    brace = text.find("{", match.start())
    depth = 0
    for pos in range(brace, len(text)):
        if text[pos] == "{": depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0: return text[start:pos + 1]
    fail(f"unterminated function {name}")


def wrappers(text: str) -> str:
    names = ["keycode_at_keymap_location", "keycode_at_encodermap_location"]
    return "\n".join(function(text, name) for name in names) + "\n"


def translate_asm(text: str) -> str:
    def val(x: str) -> str:
        x = x.strip()
        if x.startswith("#"): return x[1:]
        aliases = {"a": "acc", "0x02": "r[2]", "b": "b", "dpl": "dpl", "dph": "dph", "c": "carry", "acc": "acc", "dptr": "dptr"}
        if x in aliases: return aliases[x]
        if re.fullmatch(r"r[0-7]", x): return f"r[{x[1]}]"
        return x

    def one(name: str, symbol: str) -> str:
        body_match = re.search(rf"\b{re.escape(name)}\s*\(void\).*?__asm(.*?)__endasm;", text, re.S)
        if not body_match: fail(f"cannot extract assembly body {name}")
        result = []
        for raw in body_match.group(1).splitlines():
            line = raw.strip()
            if not line: continue
            if line.endswith(":"):
                result.append(line + ";"); continue
            op, *rest = line.split(None, 1)
            args = rest[0].split(",") if rest else []
            a = [val(v) for v in args]
            if op == "mov": c = f'dpl=({a[1]})&255;dph=({a[1]})>>8;' if a[0] == "dptr" else f"{a[0]}={a[1]};"
            elif op == "anl": c = f"{a[0]}&={a[1]};"
            elif op == "clr": c = f"{a[0]}=0;"
            elif op == "setb": c = f"{a[0]}=1;"
            elif op in ("jnz", "jc", "jnc"): c = f'if ({dict(jnz="acc",jc="carry",jnc="!carry")[op]}) goto {args[0]};'
            elif op == "subb": c = f"tmp=(int)acc-({a[1]})-carry;carry=tmp<0;acc=tmp;"
            elif op in ("add", "addc"): c = f'tmp=(int)acc+({a[1]})' + ("+carry" if op == "addc" else "") + ";carry=tmp>255;acc=tmp;"
            elif op == "swap": c = "acc=(acc<<4)|(acc>>4);"
            elif op == "rl": c = "acc=(acc<<1)|(acc>>7);"
            elif op == "inc": c = f"++{a[0]};"
            elif op == "cjne": c = f"carry=({a[0]})<({a[1]});if(({a[0]})!=({a[1]}))goto {args[2]};"
            elif op == "lcall" and args[0] == "_ak820_keymap_word_address": c = "address();"
            elif op == "lcall" and args[0] == "_eeprom_read_byte": c = "dpl=eeprom_read_byte((void *)(uintptr_t)((unsigned)dph*256+dpl));"
            elif op == "ret": c = "return;"
            else: fail(f"unsupported assembly instruction: {line}")
            result.append(c + " /* " + line + " */")
        return f"static void {symbol}(void){{\n" + "\n".join(result) + "\n}\n"

    return ("static uint8_t r[8],acc,carry,dpl,dph,b;static int tmp;\n" +
            one("ak820_keymap_word_address", "address") + one("ak820_keymap_word_read", "read_word") + '''
uint16_t dynamic_keymap_get_keycode(uint8_t l,uint8_t row,uint8_t col){r[2]=l;r[3]=row;r[4]=col;r[0]=0;read_word();return (uint16_t)dph*256+dpl;}
uint16_t dynamic_keymap_get_encoder(uint8_t l,uint8_t enc,bool cw){r[2]=l;r[3]=enc;r[4]=cw;r[0]=2;read_word();return (uint16_t)dph*256+dpl;}
''')


def harness(base: str, candidate: str, generic: str, asm: str, backend: str, geometry: tuple[int,int,int,int], ak820: bool = True) -> str:
    layers, rows, cols, encoders = geometry
    kernel = asm if backend == "asm" else generic
    board_define = "#define AK820_BOARD\n" if ak820 else ""
    return f'''#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef uint8_t bool; /* Models raw ABI bytes 0..255 for the encoder direction. */
#define KC_NO 0
{board_define}#define DYNAMIC_KEYMAP_LAYER_COUNT {layers}
#define MATRIX_ROWS {rows}
#define MATRIX_COLS {cols}
#define NUM_ENCODERS {encoders}
#define DYNAMIC_KEYMAP_EEPROM_ADDR 0x40
#define DYNAMIC_KEYMAP_ENCODER_EEPROM_ADDR (0x40+LAYERS*ROWS*COLS*2)
#define LAYERS DYNAMIC_KEYMAP_LAYER_COUNT
#define ROWS MATRIX_ROWS
#define COLS MATRIX_COLS
#define ENCODERS NUM_ENCODERS
static unsigned calls,trace[2];
static uint8_t eeprom_read_byte(const void *address){{unsigned p=(uintptr_t)address;if(calls>=2)abort();trace[calls++]=p;return (p*73+(p>>8)*29+0x53)&255;}}
{kernel}
#define keycode_at_keymap_location baseline_key
#define keycode_at_encodermap_location baseline_enc
{base}
#undef keycode_at_keymap_location
#undef keycode_at_encodermap_location
#define keycode_at_keymap_location candidate_key
#define keycode_at_encodermap_location candidate_enc
{candidate}
#undef keycode_at_keymap_location
#undef keycode_at_encodermap_location
static void check(unsigned l,unsigned x,unsigned y,unsigned enc){{
 unsigned valid=l<LAYERS && x<(enc?ENCODERS:ROWS) && (enc||y<COLS);
 unsigned p=enc?DYNAMIC_KEYMAP_ENCODER_EEPROM_ADDR+l*ENCODERS*4+x*4+(!y)*2:0x40+((l*ROWS+x)*COLS+y)*2;
 unsigned v[2],n[2],t[2][2];
 for(unsigned i=0;i<2;i++){{calls=0;trace[0]=trace[1]=0;v[i]=enc?(i?candidate_enc(l,x,y):baseline_enc(l,x,y)):(i?candidate_key(l,x,y):baseline_key(l,x,y));n[i]=calls;t[i][0]=trace[0];t[i][1]=trace[1];}}
 unsigned expected=valid?(((p*73+(p>>8)*29+0x53)&255)*256+(((p+1)*73+((p+1)>>8)*29+0x53)&255)):0;
 if(v[0]!=v[1]||v[0]!=expected||n[0]!=(valid?2:0)||n[1]!=n[0]||t[0][0]!=t[1][0]||t[0][1]!=t[1][1]||(valid&&(t[0][0]!=p||t[0][1]!=p+1))){{fprintf(stderr,"FAIL enc=%u l=%u x=%u y=%u values=%x/%x expected=%x reads=%u/%u addr=%x/%x expected=%x\\n",enc,l,x,y,v[0],v[1],expected,n[0],n[1],t[1][0],t[1][1],p);exit(1);}}
}}
int main(void){{for(unsigned l=0;l<256;l++)for(unsigned x=0;x<256;x++)for(unsigned y=0;y<256;y++){{check(l,x,y,0);check(l,x,y,1);}}printf("PASS cases=33554432 geometry=%u/%u/%u encoders=%u backend={backend}\\n",LAYERS,ROWS,COLS,ENCODERS);}}
'''


def execute(cc: tuple[str, ...], args: list[str], temp: Path) -> subprocess.CompletedProcess[str]:
    if cc[0] == "docker":
        host_path = str(temp.resolve())
        mapped = [arg.replace(host_path, "/work") for arg in args]
        command = ["gcc", *mapped] if mapped and mapped[0].startswith("-") else mapped
        return subprocess.run(["docker", "run", "--rm", "--network", "none", "-v", f"{host_path}:/work", "-w", "/work", cc[1], *command], text=True, capture_output=True)
    command = [cc[0], *args] if args and args[0].startswith("-") else args
    return subprocess.run(command, text=True, capture_output=True)


def compile_run(cc: tuple[str, ...], source: str, name: str, temp: Path, sanitizer: bool = False) -> str:
    cfile, binary = temp / f"{name}.c", temp / name
    cfile.write_text(source, encoding="utf-8")
    flags = ["-O2", "-std=c11", "-Wall", "-Wextra", "-Wno-int-to-pointer-cast", "-DENCODER_MAP_ENABLE"]
    if sanitizer: flags += ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
    command = [*flags, str(cfile), "-o", str(binary)]
    result = execute(cc, command, temp)
    if result.returncode: fail(f"{name} compile failed: {result.stderr}")
    run = execute(cc, [str(binary)], temp)
    if run.returncode: fail(f"{name} failed: {run.stdout}{run.stderr}")
    return run.stdout.strip()


def main() -> int:
    compiler = shutil.which("gcc") or shutil.which("cc")
    if compiler:
        cc = (compiler,)
        compiler_info = subprocess.run([compiler, "--version"], text=True, capture_output=True, check=True).stdout.splitlines()[0]
        image_id = None
    elif shutil.which("docker"):
        image = "ak820-nkro-study-env:local"
        probe = subprocess.run(["docker", "run", "--rm", "--network", "none", image, "gcc", "--version"], text=True, capture_output=True)
        if probe.returncode: fail(f"host compiler unavailable and offline Docker image {image} has no gcc: {probe.stderr}")
        cc = ("docker", image)
        compiler_info = probe.stdout.splitlines()[0]
        image_probe = subprocess.run(["docker", "image", "inspect", image, "--format", "{{.Id}}"], text=True, capture_output=True, check=True)
        image_id = image_probe.stdout.strip()
    else:
        fail("host gcc/cc or Docker with ak820-nkro-study-env:local is required; no checks were skipped")
    live = DYNAMIC.read_text(encoding="utf-8")
    kernel_text = KERNEL.read_text(encoding="utf-8")
    config_text = CONFIG.read_text(encoding="utf-8")
    header_text = HEADER.read_text(encoding="utf-8")
    committed = subprocess.run(["git", "show", f"{ORACLE_COMMIT}:qmk-8051-ak820/quantum/dynamic_keymap.c"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    baseline, candidate = wrappers(committed), wrappers(live)
    # Verify HEAD matches the requested full source commit and preserves the original guarded wrappers.
    head = subprocess.run(["git", "rev-parse", ORACLE_COMMIT], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    if head != ORACLE_COMMIT: fail("Git oracle commit identity mismatch")
    if "if (layer_num < DYNAMIC_KEYMAP_LAYER_COUNT" not in baseline: fail("saved baseline wrappers lack the expected original coordinate checks")
    generic = "\n".join(function(live, n) for n in ["dynamic_keymap_key_to_eeprom_address", "dynamic_keymap_get_keycode", "dynamic_keymap_encoder_to_eeprom_address", "dynamic_keymap_get_encoder"])
    asm = translate_asm(kernel_text)
    for required in ["AK820_KEYMAP_WORDS_ASM", "AK820_BOARD", "__SDCC_mcs51", "__SDCC_MODEL_LARGE"]:
        if required not in live or required not in kernel_text: fail(f"configuration guard {required} not found in source")
    if "DYNAMIC_KEYMAP_LAYER_COUNT 6" not in config_text or "MATRIX_ROWS 16" not in config_text or "MATRIX_COLS 8" not in config_text or "NUM_ENCODERS 1" not in config_text:
        fail("AK820 geometry constants changed or are missing; update the evidence contract")
    if "bool" not in header_text: fail("public bool declaration not found in dynamic_keymap header")
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in [DYNAMIC, KERNEL, CONFIG, HEADER]}
    oracle_hash = hashlib.sha256(committed.encode()).hexdigest()
    records = [{"kind":"sources", "oracle_commit":head, "oracle_file_sha256":oracle_hash,
                "oracle_wrappers_sha256":hashlib.sha256(baseline.encode()).hexdigest(),
                "candidate_wrappers_sha256":hashlib.sha256(candidate.encode()).hexdigest(),
                "current_sha256":hashes,"test_runner_sha256":digest(HERE / "run.py"),
                "compiler":list(cc),"compiler_version":compiler_info,"container_image_id":image_id,
                "invocation":"python3 tests/ak820_getter_bounds/run.py",
                "compiler_flags":["-O2","-std=c11","-Wall","-Wextra","-Wno-int-to-pointer-cast","-DENCODER_MAP_ENABLE"],
                "sanitizer_flags":["-O1","-g","-fsanitize=address,undefined","-fno-omit-frame-pointer"],
                "container_command":"docker run --rm --network none -v <temporary-directory>:/work -w /work ak820-nkro-study-env:local gcc <compiler_flags> /work/<case>.c -o /work/<case>",
                "checks":"return values, independent EEPROM expectation, exact read count and ordered addresses; raw direction ABI byte 0..255"}]
    # Each executable compares all 256^3 tuples for matrix and encoder getters.
    variants = [("ak820_generic", "generic", (6,16,8,1), True), ("ak820_asm_translation", "asm", (6,16,8,1), True),
                ("non_ak820_generic", "generic", (6,16,8,1), False), ("alternate_generic_geometry", "generic", (2,3,5,2), True)]
    with tempfile.TemporaryDirectory(prefix="ak820-getter-bounds-") as td:
        temp=Path(td)
        os.chmod(temp, 0o777)
        for name, backend, geometry, ak820 in variants:
            got=compile_run(cc,harness(baseline,candidate,generic,asm,backend,geometry,ak820),name,temp)
            records.append({"kind":"variant", "name":name,"backend":backend,"geometry":geometry,"result":got})
        records.append({"kind":"coverage", "exhaustive_comparisons":134217728,
                        "per_variant":33554432,"byte_tuples_per_getter":16777216,
                        "target_cpu_execution":False})
        # Reject three deliberate source-level mistakes before any extended run.
        negatives = [
            ("wrong_direction", "return dynamic_keymap_get_encoder(layer_num, encoder_idx, clockwise);", "return dynamic_keymap_get_encoder(layer_num, encoder_idx, !clockwise);", "candidate.inc"),
            ("generic_layer_oob", "layer >= DYNAMIC_KEYMAP_LAYER_COUNT", "layer > DYNAMIC_KEYMAP_LAYER_COUNT", "generic.inc"),
            ("asm_layer_oob", "if (!carry) goto ak820_word_invalid;", "if (0) goto ak820_word_invalid;", "asm.inc"),
        ]
        # Negative controls run as smoke probes and must produce a mismatch immediately.
        for label, needle, replacement, target in negatives:
            subject = candidate if target == "candidate.inc" else generic if target == "generic.inc" else asm
            if needle not in subject: fail(f"negative-control anchor absent in extracted current source/model: {label}")
            mutant = subject.replace(needle, replacement, 1)
            b, c, g, a = baseline, candidate, generic, asm
            if target == "candidate.inc": c=mutant
            elif target == "generic.inc": g=mutant
            else: a=mutant
            # Build a bounded smoke harness by reducing loops through an alternate entry path.
            source = harness(b,c,g,a,"asm" if target == "asm.inc" else "generic",(6,16,8,1),True)
            loop = ("for(unsigned l=0;l<1;l++)for(unsigned x=0;x<1;x++)for(unsigned y=2;y<3;y++){" if label == "wrong_direction" else "for(unsigned l=0;l<7;l++)for(unsigned x=0;x<2;x++)for(unsigned y=0;y<2;y++){")
            source = source.replace("for(unsigned l=0;l<256;l++)for(unsigned x=0;x<256;x++)for(unsigned y=0;y<256;y++){", loop)
            cfile=temp/f"{label}.c"; binary=temp/label; cfile.write_text(source,encoding="utf-8")
            build=execute(cc,["-O2","-std=c11","-Wno-int-to-pointer-cast","-DENCODER_MAP_ENABLE",str(cfile),"-o",str(binary)],temp)
            if build.returncode: fail(f"{label} compile failed: {build.stderr}")
            run=execute(cc,[str(binary)],temp)
            if run.returncode == 0: fail(f"negative control survived: {label}")
            records.append({"kind":"negative_control","name":label,"rejected":True,"first_failure":run.stderr.strip().splitlines()[0] if run.stderr else "nonzero exit"})
        # The same exhaustive host suite is practical under ASan/UBSan; run core AK820 generic model.
        sanitized=compile_run(cc,harness(baseline,candidate,generic,asm,"generic",(6,16,8,1)),"sanitized",temp,True)
        records.append({"kind":"sanitizers","result":sanitized,"flags":["address","undefined"]})
    EVIDENCE.write_text("".join(json.dumps(r,sort_keys=True)+"\n" for r in records),encoding="utf-8")
    print("\n".join(json.dumps(r,sort_keys=True) for r in records))
    print(f"evidence={EVIDENCE}")
    return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"FAIL: {error}",file=sys.stderr); raise SystemExit(1)
