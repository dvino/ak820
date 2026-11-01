#!/usr/bin/env python3
"""Host-only cancellation model against actual experimental queue/frame/slots."""
import argparse
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOARD = ROOT / 'keyboards/ajazz/ak820'
p = argparse.ArgumentParser()
p.add_argument('--out', type=Path, required=True)
out = p.parse_args().out
out.mkdir(parents=True, exist_ok=False)
out = out.resolve()
include = out / 'include'
include.mkdir()
(include / 'action.h').write_text('''#include <stdbool.h>\n#include <stdint.h>\n#define __xdata\ntypedef struct { uint8_t col, row; } keypos_t;\ntypedef enum { TICK_EVENT, KEY_EVENT } keyevent_type_t;\ntypedef struct { keypos_t key; uint16_t time; keyevent_type_t type; bool pressed; } keyevent_t;\n''')
variants = [
    ('candidate', None, None, None),
    ('ignore_queue', 'MUTANT_IGNORE_QUEUE', 'saturated', 'saturated_waiting'),
    ('dispatch_waiting', 'MUTANT_DISPATCH_WAITING', 'claimed', 'claimed_and_pinned_waiting'),
    ('no_revoke', 'MUTANT_NO_REVOKE', 'nested', 'nested_cancel'),
    ('scope_frame_fail_open', 'MUTANT_SCOPE_FRAME_FAIL_OPEN', 'scope_failure', 'scope_allocation_failure'),
    ('scope_table_fail_open', 'MUTANT_SCOPE_TABLE_FAIL_OPEN', 'scope_table', 'scope_table_failure'),
    ('replay_claim', 'MUTANT_REPLAY_CLAIM', 'nested', 'nested_revocation_no_replay'),
    ('accept_failed_cleanup', 'MUTANT_ACCEPT_FAILED_CLEANUP', 'failure', 'failed_cleanup'),
    ('accept_partial_cleanup', 'MUTANT_ACCEPT_FAILED_CLEANUP', 'partial', 'partial_cleanup_failure'),
    ('clear_blocks', 'MUTANT_CLEAR_BLOCKS', 'release', 'held_release_after_exit'),
    ('pin_idle', 'MUTANT_PIN_IDLE', 'claim_saturation', 'claim_saturation'),
    ('pin_skip', 'MUTANT_PIN_SKIP', 'claim_saturation', 'claim_saturation'),
    ('invalid_idle', 'MUTANT_INVALID_IDLE', 'claim_fault0', 'claim_fault'),
    ('fault_drain', 'MUTANT_FAULT_DRAIN', 'claim_fault0', 'claim_fault'),
    ('drop_fault_scope', 'MUTANT_FAULT_DROP_SCOPE', 'lifetime_claim', 'scope_lifetime'),
    ('release_fault_frame', 'MUTANT_FAULT_RELEASE_FRAME', 'lifetime_finish', 'scope_lifetime'),
]
commands = []
for name, mutant, case, expected_failure in variants:
    exe = out / name
    cmd = ['cc', '-std=c99', '-O1', '-g', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', '-DPH_CANCEL_HOST_MODEL', '-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=6', '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=3', '-DAK820_PH_QUEUE_ENABLE', '-I', str(include), '-I', str(BOARD)]
    if mutant:
        cmd.append('-D' + mutant)
    cmd += [str(HERE / 'ph_guarded_cancel_model.c'), str(BOARD / 'ak820_ph_frame.c'), str(BOARD / 'ak820_ph_slots.c'), str(BOARD / 'ak820_ph_queue.c'), '-o', str(exe)]
    commands.append(cmd)
    subprocess.run(cmd, check=True)
    command = [str(exe)] + ([case] if case else [])
    commands.append(command)
    run = subprocess.run(command, capture_output=True, text=True, timeout=5)
    (out / (name + '.log')).write_text(f'exit={run.returncode}\n' + run.stdout + run.stderr)
    if not mutant:
        assert run.returncode == 0, run.stderr
        assert len([x for x in run.stdout.splitlines() if x.startswith('PASS:')]) == 10, run.stdout
        print(run.stdout, end='')
        # Faults deliberately retain ownership and therefore run in isolated processes.
        for fault_case in [*(f'claim_fault{i}' for i in range(8)), 'claim_duplicate', 'finish_fault', 'lifetime_claim', 'lifetime_finish']:
            command = [str(exe), fault_case]
            commands.append(command)
            fault_run = subprocess.run(command, capture_output=True, text=True, timeout=5)
            (out / (fault_case + '.log')).write_text(f'exit={fault_run.returncode}\n' + fault_run.stdout + fault_run.stderr)
            assert fault_run.returncode == 0 and fault_run.stdout.startswith('PASS:'), (fault_case, fault_run.stdout, fault_run.stderr)
            print(f'PASS: {fault_case}: {fault_run.stdout.strip()}')
    else:
        assert run.returncode != 0 and 'FAIL ' + expected_failure + ':' in run.stderr, (name, run.stdout, run.stderr)
        print(f'PASS: negative {name} rejected by {expected_failure} (exit {run.returncode})')
(out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
print('PASS: isolated host model; no firmware output ownership or IRQ claim')
