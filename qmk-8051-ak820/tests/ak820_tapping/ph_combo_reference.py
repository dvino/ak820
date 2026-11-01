#!/usr/bin/env python3
"""Retained successful Combo/tapping boundary; host adapter, not firmware proof."""
from pathlib import Path
import os
import re
import subprocess
import tempfile
import ph_layer_reference as reference

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def stripped(path):
    return re.sub(r'^#\s*(?:include[^\n]*|pragma once)\n', '', (ROOT / path).read_text(), flags=re.M)


def source(mutation=None):
    h = (HERE / 'ph_layer_reference_harness.c').read_text()
    old = 'typedef struct { keyevent_t event; tap_t tap; } keyrecord_t;'
    assert h.count(old) == 1
    h = h.replace(old, 'typedef struct { keyevent_t event; tap_t tap; uint16_t keycode; } keyrecord_t;')
    config = '''
#define COMBO_ENABLE
#define VIAL_COMBO_ENABLE
#define VIAL_COMBO_ENTRIES 1
#define COMBO_TERM 40
#define TICK_EVENT 0
#define COMBO_EVENT 4
#define MAKE_KEYPOS(r,c) ((keypos_t){.row=(r),.col=(c)})
/* Retained keyboard.h factory is declaration-valued; initializer needs expression. */
#define MAKE_COMBOEVENT(p) ((keyevent_t){.key=MAKE_KEYPOS(0,0),.time=now,.pressed=(p),.type=COMBO_EVENT})
#define pgm_read_word(p) (*(p))
'''
    h = h.replace('#define PERMISSIVE_HOLD', config + '\n#define PERMISSIVE_HOLD')
    declarations = stripped('quantum/process_keycode/process_combo.h') + '''
static void clear_weak_mods(void) {}
static uint16_t timer_read(void) { return now; }
static uint16_t timer_elapsed(uint16_t start) { return (uint16_t)(now-start); }
static uint8_t get_highest_layer(layer_state_t state) {
    uint8_t result=0; while (state >>= 1) ++result; return result;
}
static const uint16_t chord[] = {KC_A, KC_B, COMBO_END};
combo_t key_combos[1] = { COMBO(chord, KC_C) };
'''
    h = h.replace('#include "retained.inc"', declarations + '\n#include "retained.inc"\n' + stripped('quantum/process_keycode/process_combo.c'))
    old_action = 'a.code=store_or_get_action(r->event.pressed,r->event.key);'
    assert h.count(old_action) == 1
    h = h.replace(old_action, 'a.code=r->keycode ? action_for_keycode(r->keycode) : store_or_get_action(r->event.pressed,r->event.key);')
    h = h[:h.index('int main(void) {')] + '''
int main(void) {
    unsigned a,b,c; char op;
    while (scanf(" %c", &op)==1) {
        if (op=='M') { if(scanf("%u %u %x",&a,&b,&c)!=3 || a>=2 || b>=16 || c>65535)return 2;map[a][b]=c; }
        else if (op=='E') {
            if(scanf("%u %u %u",&a,&b,&c)!=3 || a>65535 || b>=16 || c>1)return 2;
            now=a;keyevent_t e={.key={.row=0,.col=b},.time=now,.pressed=c,.type=1};initialized_physical_record(e);
        } else if (op=='C') { if(scanf("%u",&a)!=1 || a>65535)return 2; now=a;combo_task(); }
        else if (op=='T') { if(scanf("%u",&a)!=1 || a>65535)return 2;now=a;keyevent_t e={.time=now,.type=0};initialized_physical_record(e); }
        else if (op=='S') { assert_pending_lt(2); } else return 2;
    }
    return 0;
}
'''
    if mutation:
        old, new = mutation
        assert h.count(old) == 1, old
        h = h.replace(old, new)
    return h


def main():
    trace = ('M 0 2 4129\nM 1 2 1\nM 0 3 4\nM 0 4 5\nM 0 0 7\nM 1 0 8\n'
             'E 10 2 1\nS\nE 20 3 1\nE 30 4 1\nC 70\nC 71\nE 75 3 0\nE 80 4 0\nE 90 2 0\n')
    expected = [
        'F 10 80 2 1 4129 a129 0 2',
        'F 30 80 0 1 0006 0006 0 2',
        'F 80 80 0 0 0006 0006 0 2',
        'F 90 90 2 0 4129 a129 0 0',
    ]
    # Adapter explicitly decodes generated keycodes; it is not process_action.
    with tempfile.TemporaryDirectory(prefix='.ph-combo-reference-', dir=HERE) as directory:
        work = Path(directory)
        (work / 'retained.inc').write_text(reference.source())
        src = work / 'probe.c'
        exe = work / 'probe'
        cmd = [os.environ.get('CC', 'cc'), '-std=c99', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-Wno-type-limits', '-Wno-unused-parameter', '-fsanitize=undefined', '-fno-sanitize-recover=undefined']
        cmd += ['-I' + str(p) for p in (ROOT / 'quantum', ROOT / 'quantum/keymap_extras', ROOT / 'quantum/sequencer', ROOT / 'platforms', work)]
        cmd += [str(src), '-o', str(exe)]
        def run(text, events):
            src.write_text(text)
            subprocess.run(cmd, check=True)
            return subprocess.run([str(exe)], input=events, text=True, capture_output=True, check=True).stdout
        output = run(source(), trace)
        print(output, end='')
        rows = [r for r in output.splitlines() if r.startswith('F ')]
        assert rows == expected, rows
        assert output.splitlines()[:2] == ['P 10 10 2 1 4129', 'PENDING LT count=0 interrupted=0 layer=0']
        assert 'OVERFLOW' not in output
        reverse = trace.replace('E 75 3 0\nE 80 4 0', 'E 75 4 0\nE 80 3 0')
        reversed_output = run(source(), reverse)
        assert [r for r in reversed_output.splitlines() if r.startswith('F ')] == expected
        assert reversed_output.splitlines()[:2] == output.splitlines()[:2]
        assert 'OVERFLOW' not in reversed_output
        mutated = run(source(('action_tapping_process(*record);', 'process_record(record);')), trace)
        print('compiled direct-dispatch mutant:\n' + mutated, end='')
        mutant_rows = [r for r in mutated.splitlines() if r.startswith('F ')]
        assert 'OVERFLOW' not in mutated
        assert mutant_rows != expected
        assert mutant_rows[0] == 'F 30 71 0 1 0006 0006 0 0', mutant_rows
        print('PASS: pending initialized LT; both member-release orders; compiled mutant dispatches Combo before LT hold')


if __name__ == '__main__':
    main()
