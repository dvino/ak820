// SPDX-License-Identifier: GPL-2.0-or-later
#include <assert.h>
#include "ak820_ph_vial.h"
#include "ak820_ph_queue.h"

static ak820_ph_queue queue;
static unsigned mode, depth, calls, waits;
static uint16_t trace[8];
static unsigned trace_count;

uint16_t timer_read(void) { return 42; }
bool ak820_ph_vial_basic(ak820_ph_frame_handle_t h) { (void)h; return false; }
bool ak820_ph_vial_dispatch(ak820_ph_frame_handle_t h) { (void)h; return false; }
bool ak820_ph_vial_wait(void) { return false; }

static bool hook(const ak820_ph_frame_t *f) {
    ++calls;
    if (mode == 1) {
        assert(depth == 0 && f->keycode == 0x7700 && f->event.pressed);
        assert(ak820_ph_queue_enqueue_scoped(&queue, f) == AK820_PH_QUEUE_OK);
    } else if (mode == 2) {
        if (!depth) {
            depth = 1;
            assert(ak820_ph_scoped_vial_down(0x7701));
            assert(f->keycode == 0x7700 && f->event.time == 43 && f->event.pressed);
            depth = 0;
        } else {
            assert(f->keycode == 0x7701);
            assert(!ak820_ph_scoped_vial_down(0x7702));
            assert(f->keycode == 0x7701);
        }
    } else if (mode == 3 || mode == 5 || mode == 6) {
        assert(trace_count < 8);
        trace[trace_count++] = f->keycode | (f->event.pressed ? 0 : 0x8000);
        if (mode == 6 && !f->event.pressed) return false;
    } else if (mode == 4) {
        return false;
    }
    return true;
}
bool ak820_ph_scoped_vial_basic(const ak820_ph_frame_t *f) { return hook(f); }
bool ak820_ph_scoped_vial_dispatch(const ak820_ph_frame_t *f) { return hook(f); }
bool ak820_ph_scoped_vial_wait(void) {
    ++waits;
    if (mode == 3) assert(ak820_ph_scoped_vial_down(0x7701));
    return mode != 5;
}

int main(void) {
    ak820_ph_queue_init(&queue);
    mode = 1;
    assert(ak820_ph_scoped_vial_down(0x7700));
    mode = 0;
    for (unsigned long i = 0; i < 70000; ++i) assert(ak820_ph_scoped_vial_down(0x7701));
    ak820_ph_slot *slot = 0;
    assert(ak820_ph_queue_claim(&queue, &slot) == AK820_PH_QUEUE_OK);
    const ak820_ph_frame_t *r = ak820_ph_queue_record(&queue, slot);
    assert(r && r->keycode == 0x7700 && r->event.type == KEY_EVENT && r->event.time == 43 &&
           r->event.key.row == 0xfe && r->event.key.col == 0xfe && r->event.pressed);
    assert(ak820_ph_queue_finish(&queue, slot));
    mode = 2;
    assert(ak820_ph_scoped_vial_down(0x7700));
    mode = 3;
    assert(ak820_ph_scoped_vial_tap(0x7700));
    assert(waits == 1 && trace_count == 3 && trace[0] == 0x7700 && trace[1] == 0x7701 && trace[2] == 0xf700);
    mode = 4;
    assert(!ak820_ph_scoped_vial_tap(0x7700) && waits == 1);

    /* These mock failures do not implement output cleanup. */
    mode = 5; trace_count = 0;
    assert(!ak820_ph_scoped_vial_tap(0x7700));
    assert(waits == 2 && trace_count == 1 && trace[0] == 0x7700);
    mode = 3; trace_count = 0;
    assert(ak820_ph_scoped_vial_tap(0x7700));
    assert(waits == 3 && trace_count == 3 && trace[0] == 0x7700 && trace[1] == 0x7701 && trace[2] == 0xf700);

    mode = 6; trace_count = 0;
    assert(!ak820_ph_scoped_vial_tap(0x7700));
    assert(waits == 4 && trace_count == 2 && trace[0] == 0x7700 && trace[1] == 0xf700);
    mode = 3; trace_count = 0;
    assert(ak820_ph_scoped_vial_tap(0x7700));
    assert(waits == 5 && trace_count == 3 && trace[0] == 0x7700 && trace[1] == 0x7701 && trace[2] == 0xf700);
    assert(calls >= 70007);
    return 0;
}
