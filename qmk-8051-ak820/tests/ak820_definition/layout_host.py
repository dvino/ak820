#!/usr/bin/env python3
"""Differential check of the real VIA layout option bodies against RC4."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("ak820_extract", ROOT / "tests/ak820_recovery/run.py")
extract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extract)

HARNESS = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#define VIA_EEPROM_LAYOUT_OPTIONS_ADDR 0x28
static uint8_t memory[256];
struct observation { uint32_t events[12][3]; unsigned count; } trace;
static void event(uint32_t kind, uint32_t address, uint32_t value) {
    assert(trace.count < 12);
    trace.events[trace.count][0]=kind;
    trace.events[trace.count][1]=address;
    trace.events[trace.count++][2]=value;
}
static uint8_t eeprom_read_byte(const uint8_t *p) {
    uintptr_t a=(uintptr_t)p; assert(a < sizeof memory);
    event(1,a,memory[a]); return memory[a];
}
static void eeprom_update_byte(uint8_t *p, uint8_t v) {
    uintptr_t a=(uintptr_t)p; assert(a < sizeof memory);
    event(2,a,v); memory[a]=v;
}
static void via_set_layout_options_kb(uint32_t value) { event(3,0,value); }
/* FUNCTIONS */
int main(void) {
    uint8_t before[256], expected[256];
    struct observation old;
    unsigned long cases=0;
    for(unsigned v=0;v<256;v++) {
        memset(memory,0xA5,sizeof memory);
        for(unsigned i=0;i<VIA_EEPROM_LAYOUT_OPTIONS_SIZE;i++) memory[0x28+i]=(v+71*i)&255;
        memcpy(before,memory,sizeof memory); memset(&trace,0,sizeof trace);
        uint32_t ref=baseline_get(); old=trace;
        memset(&trace,0,sizeof trace); uint32_t got=candidate_get();
        assert(got==ref && !memcmp(&trace,&old,sizeof trace) && !memcmp(memory,before,sizeof memory));
        if(VIA_EEPROM_LAYOUT_OPTIONS_SIZE==1) assert(got==v);
        cases++;
    }
    for(uint32_t low=0;low<65536;low++) for(unsigned high=0;high<19;high++) {
        uint32_t top=high==0?0:high==1?0xA55A:high==2?0xFFFF:1u<<(high-3);
        uint32_t value=(top<<16)|low;
        memset(memory,0xA5,sizeof memory); memset(&trace,0,sizeof trace);
        baseline_set(value); old=trace; memcpy(expected,memory,sizeof memory);
        memset(memory,0xA5,sizeof memory); memset(&trace,0,sizeof trace);
        candidate_set(value);
        assert(!memcmp(&trace,&old,sizeof trace) && !memcmp(memory,expected,sizeof memory));
        assert(trace.count==1+VIA_EEPROM_LAYOUT_OPTIONS_SIZE);
        assert(trace.events[0][0]==3 && trace.events[0][2]==value);
        for(unsigned i=0;i<VIA_EEPROM_LAYOUT_OPTIONS_SIZE;i++) {
            assert(trace.events[i+1][0]==2);
            assert(trace.events[i+1][1]==0x28+VIA_EEPROM_LAYOUT_OPTIONS_SIZE-1-i);
            assert(trace.events[i+1][2]==((value>>(8*i))&255));
        }
        cases++;
    }
    printf("PASS %lu layout read/write cases, size=%u, exact callback/EEPROM trace\n",cases,VIA_EEPROM_LAYOUT_OPTIONS_SIZE);
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    path = args.source_root.resolve() / "quantum/via.c"
    candidate = path.read_text()
    baseline = subprocess.check_output(["git", "show", "cb9ff6ea:qmk-8051-ak820/quantum/via.c"], cwd=ROOT.parent, text=True)
    functions = []
    bodies = {}
    for label, source in (("baseline", baseline), ("candidate", candidate)):
        for kind, signature in (("get", "uint32_t via_get_layout_options"), ("set", "void via_set_layout_options(")):
            body = extract.function(source, signature)
            bodies[label + "_" + kind] = hashlib.sha256(body.encode()).hexdigest()
            body = body.replace("via_" + kind + "_layout_options(", label + "_" + kind + "(", 1)
            functions.append(body)
    generated = out / "layout-host.c"
    generated.write_text(HARNESS.replace("/* FUNCTIONS */", "\n".join(functions)))
    tests = []
    for size in (1, 2, 3, 4):
        binary = out / f"layout-size-{size}"
        subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-O2", "-fsanitize=undefined", "-fno-sanitize-recover=undefined",
                        "-DAK820_BOARD", f"-DVIA_EEPROM_LAYOUT_OPTIONS_SIZE={size}", str(generated), "-o", str(binary)], check=True)
        run = subprocess.run([str(binary)], capture_output=True, text=True, check=True)
        print(run.stdout, end="")
        tests.append({"size": size, "pass": True, "stdout": run.stdout})
    (out / "results.json").write_text(json.dumps({"result": "PASS", "hardware_validated": False,
        "level": "host UBSan, actual production bodies vs immutable RC4; EEPROM/callback trace fixtures",
        "baseline_commit": "cb9ff6ea", "body_sha256": bodies,
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "tests": tests}, indent=2) + "\n")


if __name__ == "__main__":
    main()
