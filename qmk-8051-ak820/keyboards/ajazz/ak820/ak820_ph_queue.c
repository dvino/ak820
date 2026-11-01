// SPDX-License-Identifier: GPL-2.0-or-later
#include "ak820_ph_queue.h"

#ifdef AK820_PH_QUEUE_ENABLE
/* Slot helpers and scratch are serialized; neither is IRQ-reentrant. */
void ak820_ph_queue_init(ak820_ph_queue __xdata *q) AK820_PH_FRAME_REENTRANT {
    ak820_ph_slots_init(&q->slots);
}

static ak820_ph_queue_result copy_frame(ak820_ph_queue __xdata *q, const ak820_ph_frame_t __xdata *frame) AK820_PH_FRAME_REENTRANT {
    if (!q || !frame) return AK820_PH_QUEUE_INVALID;
    q->scratch.source = frame->keycode;
    q->scratch.time = frame->event.time;
    q->scratch.observed = 0;
    q->scratch.committed = 0;
    q->scratch.pressed = frame->event.pressed;
    q->scratch.kind = frame->event.type;
    if (!ak820_ph_slots_enqueue(&q->slots, &q->scratch)) return AK820_PH_QUEUE_FULL;
    q->records[q->slots.tail] = *frame;
    return AK820_PH_QUEUE_OK;
}

ak820_ph_queue_result ak820_ph_queue_enqueue(ak820_ph_queue __xdata *q, ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT {
    if (!q) return AK820_PH_QUEUE_INVALID;
    return copy_frame(q, ak820_ph_frame_get(handle));
}

#ifdef AK820_PH_SCOPED_ENABLE
ak820_ph_queue_result ak820_ph_queue_enqueue_scoped(ak820_ph_queue __xdata *q, const ak820_ph_frame_t __xdata *frame) AK820_PH_FRAME_REENTRANT {
    return copy_frame(q, frame);
}
#endif

ak820_ph_queue_result ak820_ph_queue_claim(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata * __xdata *out) AK820_PH_FRAME_REENTRANT {
    if (!q || !out) return AK820_PH_QUEUE_INVALID;
    *out = ak820_ph_slots_claim(&q->slots);
    if (*out) return AK820_PH_QUEUE_OK;
    for (uint8_t i = q->slots.head; i != UINT8_MAX; i = q->slots.slots[i].next) {
        if (q->slots.slots[i].state == AK820_PH_WAITING) return AK820_PH_QUEUE_PIN_LIMIT;
    }
    return AK820_PH_QUEUE_NO_WAITING;
}

static uint16_t index_of(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata *slot) AK820_PH_FRAME_REENTRANT {
    if (!q || !slot) return AK820_PH_SLOT_CAPACITY;
    for (uint16_t i = 0; i < AK820_PH_SLOT_CAPACITY; ++i) {
        if (&q->slots.slots[i] == slot) return i;
    }
    return AK820_PH_SLOT_CAPACITY;
}

const ak820_ph_frame_t __xdata *ak820_ph_queue_record(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata *slot) AK820_PH_FRAME_REENTRANT {
    uint16_t i = index_of(q, slot);
    if (i == AK820_PH_SLOT_CAPACITY || !slot->pins ||
        (slot->state != AK820_PH_CLAIMED && slot->state != AK820_PH_RETIRED)) return 0;
    return &q->records[i];
}

bool ak820_ph_queue_finish(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata *slot) AK820_PH_FRAME_REENTRANT {
    if (index_of(q, slot) == AK820_PH_SLOT_CAPACITY) return false;
    return ak820_ph_slot_finish(&q->slots, slot);
}

bool ak820_ph_queue_unclaim(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata *slot) AK820_PH_FRAME_REENTRANT {
    if (index_of(q, slot) == AK820_PH_SLOT_CAPACITY) return false;
    return ak820_ph_slot_unclaim(slot);
}
#endif
