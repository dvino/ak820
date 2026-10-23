#!/usr/bin/env python3
"""Exhaustive host checks for bounded journal-pointer and macro-delay probes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
# Rejected SDCC 4.6 probe: exact arithmetic, but three more linked CODE bytes.
REJECTED_DELAY = """uint16_t high = (uint16_t)(d1 - 1);
uint16_t ms = (uint16_t)((high << 8) - high) + (uint16_t)(d0 - 1);"""

MACRO_SLOT_CHECKS = r'''
    /* Every retained macro ID decodes the same zero/max delay and recovers
     * after zero delay operands; the prefix consists of empty slots. */
    for (uint8_t slot = 0; slot < 16; ++slot) {
        for (unsigned maximum = 0; maximum < 2; ++maximum) {
            memset(stream, 0, sizeof(stream));
            stream[slot] = 1; stream[slot + 1] = 4;
            stream[slot + 2] = stream[slot + 3] = maximum ? 255 : 1;
            stream[slot + 4] = 'X';
            stream_length = slot + 6 + (15 - slot);
            events = texts = waits = 0;
            dynamic_keymap_macro_send(slot);
            assert(!events && texts == 1 && waits == (maximum ? 65024u : 0u));
        }
        for (unsigned available = 2; available <= 3; ++available) {
            memset(stream, 0, sizeof(stream));
            stream[slot] = 1; stream[slot + 1] = 4;
            stream[slot + 2] = stream[slot + 3] = 255;
            stream[slot + available] = 0;
            stream_length = slot + 5 + (15 - slot);
            events = texts = waits = 0;
            dynamic_keymap_macro_send(slot);
            assert(!events && !texts && !waits);
            memset(stream, 0, sizeof(stream)); stream[slot] = 'X';
            stream_length = slot + 2 + (15 - slot);
            dynamic_keymap_macro_send(slot);
            assert(texts == 1);
        }
    }
'''

def playback(root, cc, work, env):
    import importlib.util
    spec = importlib.util.spec_from_file_location("macro_guard", ROOT / "tests/ak820_macro_guard/run.py")
    guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
    source = (root / "quantum/dynamic_keymap.c").read_text()
    vial = (root / "quantum/vial.h").read_text()
    sender = (root / "quantum/send_string/send_string.c").read_text()
    constants = [re.search(r"^#define " + name + r" \d+$", vial, re.M)[0] for name in ("VIAL_MACRO_EXT_TAP", "VIAL_MACRO_EXT_DOWN", "VIAL_MACRO_EXT_UP")]
    actual = "\n".join(constants + [guard.definition(sender, n) for n in ("send_string", "send_string_with_delay")] + [guard.definition(source, n) for n in ("decode_keycode", "dynamic_keymap_macro_send")])
    harness = (ROOT / "tests/ak820_macro_guard/harness.c").read_text().replace("/* AK820_ACTUAL_SOURCE */", actual)
    harness = harness.replace('    puts("PASS: real macro/string playback', MACRO_SLOT_CHECKS + '    puts("PASS: real macro/string playback')
    (work / "playback.c").write_text(harness)
    subprocess.run([cc, "-O1", "-g", "-Wall", "-Wextra", "-Werror", "-fsanitize=address,undefined", "-fno-omit-frame-pointer", "-I" + str(root / "quantum/send_string"), str(work / "playback.c"), "-o", str(work / "playback")], check=True)
    subprocess.run([str(work / "playback")], check=True, env=env)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, default=ROOT)
    parser.add_argument('--cc', default=os.environ.get('CC', 'cc'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.source_root.resolve()
    paths = [root / 'keyboards/ajazz/ak820/ak820_nvm.c', root / 'quantum/dynamic_keymap.c']
    nvm, macro = (p.read_text() for p in paths)
    header = re.search(r'static bool journal_header_valid\([^\n]*\) \{.*?\n}', nvm, re.S)
    delay = re.search(r'                (uint16_t (?:high|ms) = .*?)\n                while \(ms--\)', macro, re.S)
    if not header or not delay:
        raise ValueError('Expected bounded production functions are absent; review extraction')
    source = '''#include <stdint.h>
#include <stdbool.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define AK820_XDATA
''' + header[0] + '\nstatic uint16_t actual(uint8_t d0,uint8_t d1) {\n' + delay[1] + '\nreturn ms; }\nstatic uint16_t rejected(uint8_t d0,uint8_t d1) {\n' + REJECTED_DELAY + '''
return ms; }
int main(void) {
unsigned delays=0, headers=0;
for(unsigned a=1;a<=255;a++) for(unsigned b=1;b<=255;b++) {
 unsigned expected=(a-1)+(b-1)*255u;
 assert(actual(a,b)==expected); assert(rejected(a,b)==expected); ++delays;
}
const uint8_t valid[9]={0xa5,0,0,0x34,0x1c,255,255,0xcb,0xe3}; uint8_t h[9];
for(unsigned i=0;i<9;i++) for(unsigned v=0;v<256;v++) {
 memcpy(h,valid,9);h[i]=v;assert(journal_header_valid(h)==(v==valid[i]));++headers;
}
for(unsigned i=1;i<5;i++) for(unsigned a=0;a<256;a++) for(unsigned b=0;b<256;b++) {
 memcpy(h,valid,9);h[i]=a;h[i+4]=b;assert(journal_header_valid(h)==((a^b)==255));++headers;
}
printf("PASS: %u legal delay pairs (production and rejected probe), %u journal header cases\\n",delays,headers);
}
'''
    with tempfile.TemporaryDirectory(prefix='ak820-bounded-') as temporary:
        work = Path(temporary)
        (work / 'check.c').write_text(source)
        subprocess.run([args.cc, '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror',
                        '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
                        str(work / 'check.c'), '-o', str(work / 'check')], check=True)
        env = os.environ.copy(); env['ASAN_OPTIONS'] = 'detect_leaks=0'
        result = subprocess.run([str(work / 'check')], check=True, text=True, capture_output=True, env=env)
        print(result.stdout.strip())
        playback(root, args.cc, work, env)
    report = {'pass': True, 'legal_delay_pairs': 65025, 'journal_header_cases': 264448, 'all_macro_slots': 16,
              'playback_checks': 'zero/maximum delays, zero operands and subsequent guard release per slot; existing recursive/busy/legacy checks',
              'source_sha256': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              'rejected_delay_source': REJECTED_DELAY,
              'limits': 'Host C with sanitizers. Does not prove SDCC execution, physical flash, timing or IRQ behavior.'}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')

if __name__ == '__main__':
    main()
