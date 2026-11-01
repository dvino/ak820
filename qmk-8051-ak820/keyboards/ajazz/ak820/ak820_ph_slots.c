// SPDX-License-Identifier: GPL-2.0-or-later
#include "ak820_ph_slots.h"
#ifdef AK820_PH_EXPERIMENTAL_SLOTS
#define NO_SLOT UINT8_MAX

static void reap(ak820_ph_slots AK820_PH_MEM *pool) {
    uint8_t prev = NO_SLOT, cur = pool->head;
    while (cur != NO_SLOT) {
        ak820_ph_slot AK820_PH_MEM *slot = &pool->slots[cur];
        uint8_t next = slot->next;
        if (slot->state == AK820_PH_RETIRED && !slot->pins) {
            if (prev == NO_SLOT) pool->head = next;
            else pool->slots[prev].next = next;
            if (pool->tail == cur) pool->tail = prev;
            slot->state = AK820_PH_FREE;
            --pool->count;
        } else {
            prev = cur;
        }
        cur = next;
    }
}

void ak820_ph_slots_init(ak820_ph_slots AK820_PH_MEM *pool) {
    pool->head = pool->tail = NO_SLOT;
    pool->count = 0;
    for (uint16_t i = 0; i < AK820_PH_SLOT_CAPACITY; ++i) {
        pool->slots[i].state = AK820_PH_FREE;
        pool->slots[i].pins = 0;
        pool->slots[i].next = NO_SLOT;
    }
}

bool ak820_ph_slots_enqueue(ak820_ph_slots AK820_PH_MEM *pool, const ak820_ph_slot_event AK820_PH_MEM *event) {
    reap(pool);
    if (pool->count == AK820_PH_SLOT_CAPACITY) return false;
    uint16_t i;
    for (i = 0; i < AK820_PH_SLOT_CAPACITY; ++i) if (pool->slots[i].state == AK820_PH_FREE) break;
    if (i == AK820_PH_SLOT_CAPACITY) return false;
    ak820_ph_slot AK820_PH_MEM *slot = &pool->slots[i];
    slot->event = *event;
    slot->pins = 0;
    slot->next = NO_SLOT;
    slot->state = AK820_PH_WAITING;
    if (pool->tail == NO_SLOT) pool->head = (uint8_t)i;
    else pool->slots[pool->tail].next = (uint8_t)i;
    pool->tail = (uint8_t)i;
    ++pool->count;
    return true;
}

ak820_ph_slot AK820_PH_MEM *ak820_ph_slots_claim(ak820_ph_slots AK820_PH_MEM *pool) {
    for (uint8_t i = pool->head; i != NO_SLOT; i = pool->slots[i].next) {
        ak820_ph_slot AK820_PH_MEM *slot = &pool->slots[i];
        if (slot->state == AK820_PH_WAITING) {
            if (slot->pins == UINT8_MAX) return 0;
            ++slot->pins;
            slot->state = AK820_PH_CLAIMED;
            return slot;
        }
    }
    return 0;
}

bool ak820_ph_slot_pin(ak820_ph_slot AK820_PH_MEM *slot) {
    if (!slot || (slot->state != AK820_PH_WAITING && slot->state != AK820_PH_CLAIMED) || slot->pins == UINT8_MAX) return false;
    ++slot->pins;
    return true;
}

bool ak820_ph_slot_unpin(ak820_ph_slots AK820_PH_MEM *pool, ak820_ph_slot AK820_PH_MEM *slot) {
    if (!slot || !slot->pins || (slot->state == AK820_PH_CLAIMED && slot->pins == 1)) return false;
    --slot->pins;
    reap(pool);
    return true;
}

bool ak820_ph_slot_finish(ak820_ph_slots AK820_PH_MEM *pool, ak820_ph_slot AK820_PH_MEM *slot) {
    if (!slot || slot->state != AK820_PH_CLAIMED || !slot->pins) return false;
    slot->state = AK820_PH_RETIRED;
    --slot->pins;
    reap(pool);
    return true;
}

bool ak820_ph_slot_unclaim(ak820_ph_slot AK820_PH_MEM *slot) {
    if (!slot || slot->state != AK820_PH_CLAIMED || !slot->pins) return false;
    --slot->pins;
    slot->state = AK820_PH_WAITING;
    return true;
}

static uint8_t at_index(const ak820_ph_slots AK820_PH_MEM *pool, uint8_t index) {
    uint8_t i = pool->head;
    while (i != NO_SLOT && index) { i = pool->slots[i].next; --index; }
    return i;
}

bool ak820_ph_slots_snapshot(const ak820_ph_slots AK820_PH_MEM *pool, uint8_t index, ak820_ph_slot_event AK820_PH_MEM *event, uint8_t AK820_PH_MEM *state) {
    uint8_t i = at_index(pool, index);
    if (i == NO_SLOT || !event || !state) return false;
    *event = pool->slots[i].event;
    *state = pool->slots[i].state;
    return true;
}

ak820_ph_slot AK820_PH_MEM *ak820_ph_slots_pin_at(ak820_ph_slots AK820_PH_MEM *pool, uint8_t index) {
    uint8_t i = at_index(pool, index);
    if (i == NO_SLOT || !ak820_ph_slot_pin(&pool->slots[i])) return 0;
    return &pool->slots[i];
}
#endif
