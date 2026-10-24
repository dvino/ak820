#!/usr/bin/env python3
"""Compare private mode conversion and protocol output with an immutable source.

No USB access. Each executable contains the extracted production functions and
actual effects include, with the compact board's seven QMK mode constants.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--reference', default='48ce5fa')
parser.add_argument('--output', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
path = 'qmk-8051-ak820/quantum/vialrgb.c'
reference = subprocess.check_output(['git', 'show', f'{args.reference}:{path}'], cwd=root, text=True)
candidate = (root / path).read_text()
effects = (root / 'qmk-8051-ak820/quantum/vialrgb_effects.inc').read_text()
preamble = r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#define AK820_BOARD
#define PROGMEM
#define VIALRGB_BUFFER
#define pgm_read_byte(p) (*(const uint8_t *)(p))
#define pgm_read_word(p) (*(const uint16_t *)(p))
#define RGB_MATRIX_EFFECT_VIALRGB_DIRECT
#define RGB_MATRIX_EFFECT_SOLID_COLOR
#define RGB_MATRIX_EFFECT_BREATHING
#define RGB_MATRIX_EFFECT_CYCLE_ALL
#define RGB_MATRIX_EFFECT_CYCLE_LEFT_RIGHT
#define RGB_MATRIX_EFFECT_SOLID_REACTIVE_SIMPLE
enum { RGB_MATRIX_NONE, RGB_MATRIX_SOLID_COLOR, RGB_MATRIX_BREATHING,
       RGB_MATRIX_CYCLE_ALL, RGB_MATRIX_CYCLE_LEFT_RIGHT,
       RGB_MATRIX_VIALRGB_DIRECT, RGB_MATRIX_SOLID_REACTIVE_SIMPLE,
       RGB_MATRIX_EFFECT_MAX };
'''
main = r'''
static uint64_t hash = UINT64_C(1469598103934665603);
static void add(uint8_t x) { hash = (hash ^ x) * UINT64_C(1099511628211); }
int main(void) {
    static const uint8_t vial_ids[] = {0, 2, 6, 13, 14, 1, 31};
    for (uint32_t id = 0; id <= UINT16_MAX; ++id) {
        uint16_t forward = qmk_id_to_vialrgb_id(id);
        uint16_t reverse = vialrgb_id_to_qmk_id(id);
        assert(forward == (id < sizeof(vial_ids) ? vial_ids[id] : 0));
        uint16_t expected = 0;
        for (unsigned i=0; i<sizeof(vial_ids); ++i) if (vial_ids[i] == id) expected=i;
        assert(reverse == expected);
        add(forward); add(forward >> 8); add(reverse); add(reverse >> 8);
        for (unsigned length=0; length<=30; ++length) {
            uint8_t packet[32]; memset(packet, 0xa5, sizeof(packet));
            packet[0]=id; packet[1]=id>>8;
            get_supported(packet, length);
            for (unsigned i=0; i<sizeof(packet); ++i) add(packet[i]);
        }
    }
    printf("%016llx\n", (unsigned long long)hash);
}
'''
results = {}
with tempfile.TemporaryDirectory(prefix='ak820-vialrgb-differential-') as td:
    for name, source in [('reference', reference), ('candidate', candidate)]:
        start = source.index('/* Both private') if '/* Both private' in source else source.index('typedef struct {')
        table = source[start:source.index('#ifdef RGB_MATRIX_EFFECT_VIALRGB_DIRECT\nHSV')]
        table = table.replace('#include "vialrgb_effects.inc"', effects)
        functions = source[source.index('static void get_supported('):source.index('static uint16_t get_mode(')]
        c = Path(td) / f'{name}.c'
        c.write_text(preamble + table + functions + main)
        binary = Path(td) / name
        subprocess.run(['cc', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror', str(c), '-o', str(binary)], check=True)
        results[name] = subprocess.check_output([str(binary)], text=True).strip()
assert results['reference'] == results['candidate'], results
report = {'pass': True, 'reference_commit': args.reference,
          'mode_ids_per_direction': 65536, 'supported_requests_per_image': 65536 * 31,
          'results': results,
          'candidate_sha256': hashlib.sha256(candidate.encode()).hexdigest(),
          'limits': 'Host production C with fixed compact QMK enum fixture; no SDCC ABI or physical device validation.'}
if args.output:
    args.output.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
