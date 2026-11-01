#!/usr/bin/env python3
"""Host-only dynamic-scope staging checks; not a firmware qualification."""
from pathlib import Path
import resource
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
BOARD = HERE.parents[1] / 'keyboards/ajazz/ak820'
defines = ['-DAK820_PH_FRAME_ENABLE', '-DAK820_PH_FRAME_CAPACITY=2',
           '-DAK820_PH_SCOPED_ENABLE', '-DAK820_PH_VIAL_ENABLE',
           '-DAK820_PH_EXPERIMENTAL_SLOTS', '-DAK820_PH_SLOT_CAPACITY=2',
           '-DAK820_PH_QUEUE_ENABLE']
with tempfile.TemporaryDirectory(prefix='ak820-scoped-host-') as tmp:
    tmp = Path(tmp)
    (tmp / 'action.h').write_text('''#pragma once\n#include <stdbool.h>\n#include <stdint.h>\n#define __xdata\ntypedef struct { uint8_t col, row; } keypos_t;\ntypedef enum { TICK_EVENT, KEY_EVENT } keyevent_type_t;\ntypedef struct { keypos_t key; uint16_t time; keyevent_type_t type; bool pressed; } keyevent_t;\n''')
    (tmp / 'vial.h').write_text('''#pragma once\n#include <stdint.h>\n#define QK_MODS_MAX 0xff\n#define VIAL_MATRIX_MAGIC 0xfe\nuint16_t timer_read(void);\n''')
    frame = (BOARD / 'ak820_ph_frame.c').read_text()
    queue = (BOARD / 'ak820_ph_queue.c').read_text()
    vial = (BOARD / 'ak820_ph_vial.c').read_text()
    up = '        if (ok) ok = ak820_ph_scoped_vial_up(frame->keycode);'
    assert vial.count(up) == 1
    assert frame.count('if (!scoped_active[i])') == 1
    assert queue.count('    q->records[q->slots.tail] = *frame;') == 1
    (tmp / 'frame_mutant.c').write_text(frame.replace('if (!scoped_active[i])', 'if (1)'))
    (tmp / 'queue_mutant.c').write_text(queue.replace('    q->records[q->slots.tail] = *frame;', '    /* omit copy */'))
    (tmp / 'up_after_failure.c').write_text(vial.replace(up, '        ok = ak820_ph_scoped_vial_up(frame->keycode);'))
    (tmp / 'ignore_up_failure.c').write_text(vial.replace(up, '        if (ok) (void)ak820_ph_scoped_vial_up(frame->keycode);'))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    for name in ('check', 'reuse_active', 'no_copy', 'up_after_failure', 'ignore_up_failure'):
        vial_source = tmp / (name + '.c') if name in ('up_after_failure', 'ignore_up_failure') else BOARD / 'ak820_ph_vial.c'
        sources = [HERE / 'ph_scoped_frame_host.c', tmp / 'frame_mutant.c' if name == 'reuse_active' else BOARD / 'ak820_ph_frame.c', BOARD / 'ak820_ph_slots.c', tmp / 'queue_mutant.c' if name == 'no_copy' else BOARD / 'ak820_ph_queue.c', vial_source]
        cmd = ['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', '-fsanitize=undefined', '-fno-sanitize-recover=undefined', *defines, '-I', str(tmp), '-I', str(BOARD), *map(str, sources), '-o', str(tmp / name)]
        subprocess.run(cmd, check=True)
        run = subprocess.run([str(tmp / name)], capture_output=True, text=True, timeout=15)
        if name == 'check':
            assert run.returncode == 0, run.stderr
        else:
            assert run.returncode != 0 and 'Assertion' in run.stderr, run.stderr
        print(f'PASS: {name} exit {run.returncode}')
print('PASS: 70000 reuses, nested exhaustion, queue copy, and Vial tap failure paths; cleanup unresolved')
