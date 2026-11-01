// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
/* Host-only scan experiment. Not an SDCC ABI or a production scheduler.
 * Single-threaded callers serialize all pool access. Only the scan operation
 * may update a live record's tap count; that update is visible to its claim
 * owner before any callback. A pin, not an index, protects callback lifetime.
 * Only the claim owner may finish/unclaim. The caller keeps tapping and
 * callback context alive throughout the callback; callback is non-null, and
 * init cannot run until all calls unwind. The supplied term is fixed for one
 * scan. This contract does not implement cancellation, IRQ exclusion,
 * overflow policy, per-key term callbacks, or an action continuation. */
#ifdef __SDCC_mcs51
#    error Host-only PH scan experiment
#endif
#include "ak820_ph_slots.h"

typedef struct { uint8_t row, col; } ph_scan_key;
typedef struct { ph_scan_key key; uint16_t time; bool pressed; uint8_t type; } ph_scan_event;
typedef struct { uint8_t count; bool interrupted; } ph_scan_tap_state;
typedef struct { ph_scan_event event; ph_scan_tap_state tap; } ph_scan_record;
typedef struct {
    ak820_ph_slots slots;
    ph_scan_record records[AK820_PH_SLOT_CAPACITY];
} ph_scan_queue;

typedef enum { PH_SCAN_ERROR = -1, PH_SCAN_NO = 0, PH_SCAN_YES = 1 } ph_scan_result;
void ph_scan_init(ph_scan_queue *queue);
bool ph_scan_enqueue(ph_scan_queue *queue, const ph_scan_record *record);
ph_scan_result ph_scan_typed(ph_scan_queue *queue, ph_scan_event event);
ph_scan_result ph_scan_tap(ph_scan_queue *queue, ph_scan_record *tapping, uint16_t term, void (*callback)(void *), void *context);
