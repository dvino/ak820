// SPDX-License-Identifier: GPL-2.0-or-later
#include "ph_scan_slots.h"

static bool same_key(ph_scan_key a, ph_scan_key b) { return a.row == b.row && a.col == b.col; }

void ph_scan_init(ph_scan_queue *queue) { ak820_ph_slots_init(&queue->slots); }

bool ph_scan_enqueue(ph_scan_queue *queue, const ph_scan_record *record) {
    ak820_ph_slot_event event = {.time = record->event.time, .pressed = record->event.pressed};
    if (!ak820_ph_slots_enqueue(&queue->slots, &event)) return false;
    queue->records[queue->slots.tail] = *record;
    return true;
}

ph_scan_result ph_scan_typed(ph_scan_queue *queue, ph_scan_event event) {
    for (uint8_t i = queue->slots.head; i != UINT8_MAX; i = queue->slots.slots[i].next) {
        ak820_ph_slot *slot = &queue->slots.slots[i];
        if (slot->state == AK820_PH_RETIRED) continue;
        if (!ak820_ph_slot_pin(slot)) return PH_SCAN_ERROR;
        ph_scan_event other = queue->records[i].event;
        bool matches = same_key(event.key, other.key) && event.pressed != other.pressed;
        if (!ak820_ph_slot_unpin(&queue->slots, slot)) return PH_SCAN_ERROR;
        if (matches) return PH_SCAN_YES;
    }
    return PH_SCAN_NO;
}

ph_scan_result ph_scan_tap(ph_scan_queue *queue, ph_scan_record *tapping, uint16_t term, void (*callback)(void *), void *context) {
    if (tapping->tap.count > 0 || !tapping->event.pressed) return PH_SCAN_NO;
    for (uint8_t i = queue->slots.head; i != UINT8_MAX; i = queue->slots.slots[i].next) {
        ak820_ph_slot *slot = &queue->slots.slots[i];
        if (slot->state == AK820_PH_RETIRED) continue;
        if (!ak820_ph_slot_pin(slot)) return PH_SCAN_ERROR;
        ph_scan_record *candidate = &queue->records[i];
        if (candidate->event.type && same_key(candidate->event.key, tapping->event.key) && !candidate->event.pressed && (uint16_t)(candidate->event.time - tapping->event.time) < term) {
            tapping->tap.count = 1;
            candidate->tap.count = 1;
            callback(context);
            if (!ak820_ph_slot_unpin(&queue->slots, slot)) return PH_SCAN_ERROR;
            return PH_SCAN_YES;
        }
        if (!ak820_ph_slot_unpin(&queue->slots, slot)) return PH_SCAN_ERROR;
    }
    return PH_SCAN_NO;
}
