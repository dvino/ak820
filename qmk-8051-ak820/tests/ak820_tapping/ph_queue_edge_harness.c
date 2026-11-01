// SPDX-License-Identifier: GPL-2.0-or-later
/* Unwired queue API probe, not action dispatch or a scheduler. */
#include "ak820_ph_queue.h"
#ifndef __SDCC_mcs51
#    include <stdio.h>
#    define __at(x)
#endif
__xdata __at (0x0f00) volatile uint8_t result[8];
static __xdata ak820_ph_queue queue;
static __xdata ak820_ph_slot *outer, *inner;
static __xdata ak820_ph_slot foreign;
#define CHECK(c) do { if (!(c)) { result[0] = __LINE__; goto done; } } while (0)

int main(void) {
    for (uint8_t i = 0; i < 8; ++i) result[i] = 0;
    ak820_ph_queue_init(&queue);
    ak820_ph_frame_handle_t h = ak820_ph_frame_reserve();
    CHECK(h);
    ak820_ph_frame_t __xdata *f = ak820_ph_frame_get(h);
    CHECK(f);
    f->keycode = 0x7700; f->event.type = KEY_EVENT; f->event.time = 3;
    f->event.key.row = 0xf0; f->event.key.col = 0xf1; f->event.pressed = true;
    CHECK(ak820_ph_queue_enqueue(&queue, h) == AK820_PH_QUEUE_OK);
    CHECK(ak820_ph_frame_release(h));
    CHECK(ak820_ph_queue_enqueue(&queue, h) == AK820_PH_QUEUE_INVALID);
    h = ak820_ph_frame_reserve();
    CHECK(h);
    f = ak820_ph_frame_get(h);
    f->keycode = 0x7701; f->event.type = KEY_EVENT; f->event.time = 5;
    f->event.key.row = 4; f->event.key.col = 3; f->event.pressed = false;
    CHECK(ak820_ph_queue_enqueue(&queue, h) == AK820_PH_QUEUE_OK);
    CHECK(ak820_ph_frame_release(h));
    CHECK(ak820_ph_queue_claim(&queue, &outer) == AK820_PH_QUEUE_OK);
    const ak820_ph_frame_t __xdata *r = ak820_ph_queue_record(&queue, outer);
    CHECK(r && r->keycode == 0x7700 && r->event.time == 3 && r->event.type == KEY_EVENT &&
          r->event.key.row == 0xf0 && r->event.key.col == 0xf1 && r->event.pressed);
    CHECK(ak820_ph_queue_claim(&queue, &inner) == AK820_PH_QUEUE_OK && inner != outer);
    r = ak820_ph_queue_record(&queue, inner);
    CHECK(r && r->keycode == 0x7701 && r->event.time == 5 && r->event.type == KEY_EVENT &&
          r->event.key.row == 4 && r->event.key.col == 3 && !r->event.pressed);
    h = ak820_ph_frame_reserve();
    CHECK(h && ak820_ph_queue_enqueue(&queue, h) == AK820_PH_QUEUE_FULL && ak820_ph_frame_get(h));
    CHECK(ak820_ph_frame_release(h));
    CHECK(!ak820_ph_queue_finish(&queue, &foreign) && !ak820_ph_queue_record(&queue, &foreign));
    CHECK(ak820_ph_slot_pin(inner));
    CHECK(ak820_ph_queue_finish(&queue, inner));
    r = ak820_ph_queue_record(&queue, inner);
    CHECK(r && r->keycode == 0x7701 && r->event.time == 5);
    CHECK(ak820_ph_slot_unpin(&queue.slots, inner));
    CHECK(!ak820_ph_queue_record(&queue, inner));
    r = ak820_ph_queue_record(&queue, outer);
    CHECK(r && r->keycode == 0x7700 && r->event.time == 3 && r->event.key.col == 0xf1);
    CHECK(ak820_ph_queue_unclaim(&queue, outer));
    CHECK(ak820_ph_queue_claim(&queue, &outer) == AK820_PH_QUEUE_OK);
    CHECK(ak820_ph_queue_finish(&queue, outer));
    CHECK(ak820_ph_queue_claim(&queue, &outer) == AK820_PH_QUEUE_NO_WAITING && !outer);
    h = ak820_ph_frame_reserve();
    CHECK(h && ak820_ph_queue_enqueue(&queue, h) == AK820_PH_QUEUE_OK && ak820_ph_frame_release(h));
    inner = &queue.slots.slots[queue.slots.head];
    for (uint16_t i = 0; i < UINT8_MAX; ++i) CHECK(ak820_ph_slot_pin(inner));
    CHECK(ak820_ph_queue_claim(&queue, &outer) == AK820_PH_QUEUE_PIN_LIMIT && !outer);
    for (uint16_t i = 0; i < UINT8_MAX; ++i) CHECK(ak820_ph_slot_unpin(&queue.slots, inner));
    CHECK(ak820_ph_queue_claim(&queue, &outer) == AK820_PH_QUEUE_OK);
    CHECK(ak820_ph_queue_finish(&queue, outer));
    result[1] = 0xa5;
done:
#ifdef __SDCC_mcs51
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
    return 0;
#else
    if (result[0] || result[1] != 0xa5) { fprintf(stderr, "failed line %u\n", result[0]); return 1; }
    puts("PASS: copied event, nested claims, pin lifetime and bounded failures");
    return 0;
#endif
}
