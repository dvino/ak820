#!/usr/bin/env python3
"""Exhaustive host differential of production byte state against packed oracle."""
from pathlib import Path
import hashlib, json, subprocess, tempfile
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'keyboards/ajazz/ak820/ak820_tapping.c'
s = SOURCE.read_text()
a = s.index('static uint8_t source_state[')
b = s.index('static uint8_t pending', a)
production = s[a:b]
oracle = (HERE / 'packed_oracle.c').read_text().replace('source_state', 'packed_state').replace('SOURCE_STATE_BYTES', 'PACKED_STATE_BYTES')
program = '''#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#define SOURCES 130
#define SOURCE_STATE_BYTES SOURCES
#define SOURCE_STATE_BITS 5
#define SOURCE_STATE_MASK 31u
''' + oracle + production + '''
static uint8_t expected[SOURCES];
static unsigned long checks;
static void verify(void) {
    for (unsigned j=0; j<SOURCES; j++) {
        assert(source_state_get(j)==expected[j]);
        assert(packed_state_get(j)==expected[j]);
        checks++;
    }
}
static void set(unsigned id, unsigned value) {
    source_state_set(id,value); packed_state_set(id,value);
    expected[id]=value & 31;
    verify();
}
int main(void) {
    verify();
    /* Every source, all 256 setter inputs, every legal initial state.
       All other sources retain nonuniform canaries, including neighbors. */
    for (unsigned seed=0; seed<32; seed++) {
        for (unsigned j=0; j<SOURCES; j++) {
            expected[j]=(j*13+seed)&31;
            source_state_set(j,expected[j]); packed_state_set(j,expected[j]);
        }
        for (unsigned id=0; id<SOURCES; id++) {
            for (unsigned value=0; value<256; value++) set(id,value);
        }
    }
    /* Deterministic interleaving: every flag combination, cancellations,
       read/modify/write, arbitrary masked values, and encoder IDs 128/129. */
    uint32_t rng=0x8051820;
    for (unsigned step=0; step<100000; step++) {
        rng=rng*1664525u+1013904223u;
        unsigned id=(rng>>16)%SOURCES;
        unsigned state=expected[id];
        switch(step%5) {
        case 0: state^=1u<<((rng>>24)%5); break;
        case 1: state=(state&2)|((state&1)<<1); break;
        case 2: state|=24; break;
        case 3: state&=~24u; break;
        default: state=rng>>24; break;
        }
        set(id,state);
    }
    printf("{\\"source_count\\":130,\\"exhaustive_writes\\":1064960,\\"sequence_writes\\":100000,\\"source_comparisons\\":%lu,\\"status\\":\\"PASS\\"}\\n",checks);
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-state-bytes-') as d:
    p=Path(d); (p/'test.c').write_text(program)
    subprocess.run(['cc','-O2','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=undefined,bounds','-fno-sanitize-recover=all',str(p/'test.c'),'-o',str(p/'test')],check=True)
    result=json.loads(subprocess.check_output([str(p/'test')],text=True))
result['production_sha256']=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
result['oracle_sha256']=hashlib.sha256((HERE/'packed_oracle.c').read_bytes()).hexdigest()
print(json.dumps(result,indent=2))
