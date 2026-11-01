// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once

/* Unwired host-checked ownership experiment, not a PH scheduler or ABI gate.
 * A slot reference is valid only while its holder owns a pin. No generation
 * counter can substitute for that lifetime. Init requires an idle, unowned
 * pool; only the claim owner may finish or unclaim a claim, and pool/slot
 * pairs must match. Pins prevent reuse, but do not authorize foreign claim
 * mutation. The API does not enforce those caller contracts, cancellation,
 * IRQ exclusion or an SDCC reentrant ABI.
 * Capacity is a limit, not evidence of RAM fit or callback depth. */
#ifdef AK820_PH_EXPERIMENTAL_SLOTS
#include <stdbool.h>
#include <stdint.h>
#ifndef AK820_PH_SLOT_CAPACITY
#    error AK820_PH_SLOT_CAPACITY must be selected explicitly
#endif
#if AK820_PH_SLOT_CAPACITY < 1 || AK820_PH_SLOT_CAPACITY > 255
#    error AK820_PH_SLOT_CAPACITY must be between 1 and 255
#endif

#ifdef __SDCC_mcs51
#    define AK820_PH_MEM __xdata
#else
#    define AK820_PH_MEM
#endif

typedef struct {
    uint16_t source, time, observed, committed;
    uint8_t pressed, kind;
} ak820_ph_slot_event;

typedef enum { AK820_PH_FREE, AK820_PH_WAITING, AK820_PH_CLAIMED, AK820_PH_RETIRED } ak820_ph_slot_state;
typedef struct {
    ak820_ph_slot_event event;
    uint8_t state, pins, next;
} ak820_ph_slot;
typedef struct {
    ak820_ph_slot slots[AK820_PH_SLOT_CAPACITY];
    uint8_t head, tail, count;
} ak820_ph_slots;

void ak820_ph_slots_init(ak820_ph_slots AK820_PH_MEM *pool);
bool ak820_ph_slots_enqueue(ak820_ph_slots AK820_PH_MEM *pool, const ak820_ph_slot_event AK820_PH_MEM *event);
ak820_ph_slot AK820_PH_MEM *ak820_ph_slots_claim(ak820_ph_slots AK820_PH_MEM *pool);
bool ak820_ph_slot_pin(ak820_ph_slot AK820_PH_MEM *slot);
bool ak820_ph_slot_unpin(ak820_ph_slots AK820_PH_MEM *pool, ak820_ph_slot AK820_PH_MEM *slot);
bool ak820_ph_slot_finish(ak820_ph_slots AK820_PH_MEM *pool, ak820_ph_slot AK820_PH_MEM *slot);
bool ak820_ph_slot_unclaim(ak820_ph_slot AK820_PH_MEM *slot);
/* Indices include pinned retired slots. Copies are snapshots only; neither
 * the index nor a snapshot identifies a slot across a callback. Scan
 * visibility and mutation policy are not defined here. pin_at returns a
 * pinned reference, released with unpin; a non-owner must treat its fields
 * as read-only. It may fail on a
 * retired slot or saturated pin count. All operations
 * require caller-provided serialization and are not an SDCC ABI contract. */
bool ak820_ph_slots_snapshot(const ak820_ph_slots AK820_PH_MEM *pool, uint8_t index, ak820_ph_slot_event AK820_PH_MEM *event, uint8_t AK820_PH_MEM *state);
ak820_ph_slot AK820_PH_MEM *ak820_ph_slots_pin_at(ak820_ph_slots AK820_PH_MEM *pool, uint8_t index);
#endif
