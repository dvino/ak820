#!/usr/bin/env python3
"""One host-only Vial/first-tap experiment; not a production scheduler.

The candidate uses retained process_tapping and extracted producer code, but
replaces only its top-level pump with the experimental owned slots. Its
reference waiting-buffer mirror is rebuilt per call: propagation of scan
mutations, concurrent IRQs and other traces are not implemented or proved.
"""
import contextlib
import io
import os
from pathlib import Path
import re
import runpy
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOARD = ROOT / 'keyboards/ajazz/ak820'
with contextlib.redirect_stdout(io.StringIO()):
    fixture = runpy.run_path(str(HERE / 'ph_vial_first_tap_reference.py'))
adapter = fixture['adapter']
tapping = adapter['tapping']
start = tapping.index('void action_tapping_process(keyrecord_t record) {')
end = tapping.index('{', start) + 1
depth = 1
while depth:
    depth += (tapping[end] == '{') - (tapping[end] == '}')
    end += 1
wrapper = r'''
/* Trace-specific host adapter. It does not implement scan write-back. */
static ak820_ph_slots candidate_slots;
static keyrecord_t candidate_records[AK820_PH_SLOT_CAPACITY];
static bool candidate_initialized;
static void candidate_mirror(void) {
    waiting_buffer_head = waiting_buffer_tail = 0;
    for (uint8_t i = candidate_slots.head; i != UINT8_MAX; i = candidate_slots.slots[i].next) {
        if (candidate_slots.slots[i].state == AK820_PH_RETIRED) continue;
        if ((waiting_buffer_head + 1) % WAITING_BUFFER_SIZE == waiting_buffer_tail) abort();
        waiting_buffer[waiting_buffer_head] = candidate_records[i];
        waiting_buffer_head = (waiting_buffer_head + 1) % WAITING_BUFFER_SIZE;
    }
}
static void candidate_release_check(keyrecord_t *r) {
    if (r->event.key.col != 0 || r->event.pressed) return;
    for (unsigned i = 0; i < AK820_PH_SLOT_CAPACITY; ++i) {
        if (&candidate_records[i] == r && candidate_slots.slots[i].state == AK820_PH_CLAIMED && candidate_slots.slots[i].pins) return;
    }
    _Exit(90); /* release was not held by its original claimed continuation */
}
static void candidate_enqueue(keyrecord_t *record) {
    ak820_ph_slot_event event = {.source=record->event.key.col, .time=record->event.time, .pressed=record->event.pressed};
    if (!IS_EVENT(record->event)) return;
    if (!ak820_ph_slots_enqueue(&candidate_slots, &event)) abort();
    candidate_records[candidate_slots.tail] = *record;
}
void action_tapping_process(keyrecord_t record) {
    if (!candidate_initialized) { ak820_ph_slots_init(&candidate_slots); candidate_initialized = true; }
    candidate_mirror();
    if (!process_tapping(&record)) candidate_enqueue(&record);
    for (;;) {
        ak820_ph_slot *owned = ak820_ph_slots_claim(&candidate_slots);
        if (!owned) return;
        unsigned index = (unsigned)(owned - candidate_slots.slots);
        candidate_mirror();
        if (!process_tapping(&candidate_records[index])) {
            if (!ak820_ph_slot_unclaim(owned)) abort();
            return;
        }
        if (!ak820_ph_slot_finish(&candidate_slots, owned)) abort();
    }
}
'''
wrapper = wrapper.replace('abort();', '_Exit(92);')
body = tapping[:start] + wrapper + tapping[end:]
# This trace must not rely on the unimplemented mirror-to-slot scan write-back.
scan_write = 'candidate->tap.count  = 1;'
assert body.count(scan_write) == 1
body = body.replace(scan_write, '_Exit(91); /* unimplemented scan write-back */')
harness = adapter['harness']
declaration = 'static void process_record(keyrecord_t *r) {'
first = '    uint16_t k=cached[r->event.key.col]; bool down=r->event.pressed;'
assert harness.count(declaration) == 1 and harness.count(first) == 1
harness = harness.replace(declaration, 'static void candidate_release_check(keyrecord_t *r);\n' + declaration)
harness = harness.replace(first, first + '\n    candidate_release_check(r);')
stream = 'static const uint8_t macro_stream[] = {1, 5, 4, 0x22, 0};'
assert harness.count(stream) == 1
harness = harness.replace(stream, 'static const uint8_t macro_stream[] = {1, 5, 5, 0x21, 0};')
flags = [os.environ.get('CC', 'cc'), '-std=c99', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-Wno-type-limits', '-Wno-unused-function', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=3', '-DQUICK_TAP_TERM=0']
with tempfile.TemporaryDirectory(prefix='.ph-vial-slot-slice-', dir=HERE) as directory:
    path = Path(directory)
    slots = (BOARD / 'ak820_ph_slots.c').read_text()
    claim = '        if (slot->state == AK820_PH_WAITING) {'
    assert slots.count(claim) == 1
    barrier = slots.replace(claim, '        if (slot->state == AK820_PH_CLAIMED) return 0;\n' + claim)
    replay = slots.replace(claim, '        if (slot->state == AK820_PH_WAITING || slot->state == AK820_PH_CLAIMED) {')
    pin_check = 'if (&candidate_records[i] == r && candidate_slots.slots[i].state == AK820_PH_CLAIMED && candidate_slots.slots[i].pins) return;'
    assert body.count(pin_check) == 1
    drop_pin = body.replace(pin_check, 'if (&candidate_records[i] == r && candidate_slots.slots[i].state == AK820_PH_CLAIMED && candidate_slots.slots[i].pins) { if (!ak820_ph_slot_unclaim(&candidate_slots.slots[i])) _Exit(93); }')
    same_keycode = harness.replace('{1, 5, 5, 0x21, 0}', '{1, 5, 4, 0x22, 0}')
    zero_wait = harness.replace('#define QS_tap_code_delay 5', '#define QS_tap_code_delay 0')
    variants = [('candidate', body, harness, slots), ('barrier', body, harness, barrier), ('replay', body, harness, replay),
                ('drop-pin', drop_pin, harness, slots),
                ('same-keycode', body, same_keycode, slots), ('zero-wait', body, zero_wait, slots)]
    trace = 'M 0 2204\nM 1 7700\nE 100 0 1\nE 110 1 1\nE 120 0 0\nE 130 1 0\n'
    results = {}
    for name, engine, producer, slot_source in variants:
        (path / 'retained_engine.inc').write_text(re.sub(r'^#include .*\n', '', engine, flags=re.M))
        (path / 'probe.c').write_text('#include "ak820_ph_slots.h"\n' + producer)
        (path / 'slots.c').write_text(slot_source)
        exe = path / name
        subprocess.run(flags + ['-I', str(ROOT / 'quantum'), '-I', str(BOARD), '-I', str(path), str(path / 'probe.c'), str(path / 'slots.c'), '-o', str(exe)], check=True)
        results[name] = subprocess.run([str(exe)], input=trace, text=True, capture_output=True, timeout=5)
    expected = [
        '100 120 0 1 1 2204 00 0',
        '110 120 1 1 0 7700 00 0',
        '121 120 2 1 0 2105 01 0',
        'wait 120 5',
        '125 125 2 0 0 2105 00 0',
        '120 125 0 0 1 2204 00 0',
        '130 130 1 0 0 7700 00 0',
    ]
    candidate = results['candidate']
    assert candidate.returncode == 0, candidate.stderr
    assert candidate.stdout.splitlines() == expected, candidate.stdout
    reference = fixture['outputs']['literal-reference']
    assert expected[:6] == [reference[i] for i in (0, 1, 2, 3, 4, 6)]
    assert reference[5] == reference[7] == '110 125 1 1 0 7700 00 0'
    assert reference[8] == 'diagnostic-callback-limit'
    assert results['barrier'].returncode == 0 and results['barrier'].stdout.splitlines()[2] == 'wait 120 5'
    assert results['replay'].returncode == 92
    assert results['drop-pin'].returncode == 90
    assert '121 120 2 1 0 2204 02 0' in results['same-keycode'].stdout.splitlines()
    assert 'wait 120 0' in results['zero-wait'].stdout.splitlines()
    for name in ('barrier', 'replay', 'drop-pin', 'same-keycode', 'zero-wait'):
        result = results[name]
        assert result.returncode != 0 or result.stdout.splitlines() != expected, name
        print(f'PASS: {name} differs or fails (exit {result.returncode}):\n{result.stdout}', end='')
    print('PASS: pinned slot slice ordered trace; literal reference replay rows excluded')
    print(candidate.stdout, end='')
