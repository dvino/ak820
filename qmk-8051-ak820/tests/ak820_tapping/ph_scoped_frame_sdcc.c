// SPDX-License-Identifier: GPL-2.0-or-later
/* Synthetic consumers only; no real action or cancellation integration. */
#include "ak820_ph_vial.h"
#include "ak820_ph_queue.h"
#include "vial.h"
__xdata __at (0x0f00) volatile uint8_t result[8];
static __xdata ak820_ph_queue queue;
static __xdata ak820_ph_slot *slot;
static uint8_t depth, mode, marks;
uint16_t timer_read(void) { return 42; }
bool ak820_ph_vial_basic(ak820_ph_frame_handle_t h) __reentrant { (void)h; return false; }
bool ak820_ph_vial_dispatch(ak820_ph_frame_handle_t h) __reentrant { (void)h; return false; }
bool ak820_ph_vial_wait(void) __reentrant { return false; }
bool ak820_ph_scoped_vial_basic(const ak820_ph_frame_t __xdata *f) __reentrant { return ak820_ph_scoped_vial_dispatch(f); }
bool ak820_ph_scoped_vial_dispatch(const ak820_ph_frame_t __xdata *f) __reentrant {
    if (mode == 1) return ak820_ph_queue_enqueue_scoped(&queue, f) == AK820_PH_QUEUE_OK;
    if (mode == 2) {
        if (!depth) {
            depth = 1;
            if (!ak820_ph_scoped_vial_down(0x7701)) return false;
            depth = 0;
            if (f->keycode != 0x7700 || f->event.time != 43 || !f->event.pressed) return false;
        } else if (f->keycode != 0x7701 || ak820_ph_scoped_vial_down(0x7702) || f->keycode != 0x7701) return false;
    }
    if (mode == 3) result[marks++] = (f->event.pressed ? 0x10 : 0x20) | (f->keycode & 1);
    return true;
}
bool ak820_ph_scoped_vial_wait(void) __reentrant {
    if (mode == 3) return ak820_ph_scoped_vial_down(0x7701);
    return true;
}
void main(void) {
    ak820_ph_queue_init(&queue);
    mode = 1;
    if (!ak820_ph_scoped_vial_down(0x7700)) goto done;
    mode = 0;
    for (uint8_t i = 0; i < 20; ++i) if (!ak820_ph_scoped_vial_down(0x7701)) goto done;
    if (ak820_ph_queue_claim(&queue, &slot) != AK820_PH_QUEUE_OK) goto done;
    const ak820_ph_frame_t __xdata *f = ak820_ph_queue_record(&queue, slot);
    if (!f || f->keycode != 0x7700 || f->event.time != 43 || !f->event.pressed) goto done;
    if (!ak820_ph_queue_finish(&queue, slot)) goto done;
    mode = 2;
    if (!ak820_ph_scoped_vial_down(0x7700)) goto done;
    mode = 3; marks = 1;
    if (!ak820_ph_scoped_vial_tap(0x7700)) goto done;
    if (result[1] != 0x10 || result[2] != 0x11 || result[3] != 0x20) goto done;
    result[0] = 0xa5;
done:
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
}
