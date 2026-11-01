// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once

#ifdef AK820_PH_QUEUE_ENABLE
#if !defined(AK820_PH_FRAME_ENABLE) || !defined(AK820_PH_EXPERIMENTAL_SLOTS)
#    error AK820_PH_QUEUE_ENABLE requires the experimental frame and slot pools
#endif
#include "ak820_ph_frame.h"
#include "ak820_ph_slots.h"

/* Unwired ownership staging only, not a PH dispatcher. Callers serialize
 * access, including IRQs, and must not access scratch. Queue initialization
 * requires an idle queue with no outstanding pins. */
typedef struct {
    ak820_ph_slots slots;
    ak820_ph_slot_event scratch;
    ak820_ph_frame_t records[AK820_PH_SLOT_CAPACITY];
} ak820_ph_queue;
typedef enum { AK820_PH_QUEUE_OK, AK820_PH_QUEUE_NO_WAITING, AK820_PH_QUEUE_FULL, AK820_PH_QUEUE_INVALID, AK820_PH_QUEUE_PIN_LIMIT } ak820_ph_queue_result;

void ak820_ph_queue_init(ak820_ph_queue __xdata *q) AK820_PH_FRAME_REENTRANT;
/* Borrows handle for this call only; caller retains it on every return. */
ak820_ph_queue_result ak820_ph_queue_enqueue(ak820_ph_queue __xdata *q, ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT;
#ifdef AK820_PH_SCOPED_ENABLE
/* Synchronously copies a live scoped borrow; never retains its pointer. */
ak820_ph_queue_result ak820_ph_queue_enqueue_scoped(ak820_ph_queue __xdata *q, const ak820_ph_frame_t __xdata *frame) AK820_PH_FRAME_REENTRANT;
#endif
/* The claim owner must finish or unclaim; out must point to owned XDATA. */
ak820_ph_queue_result ak820_ph_queue_claim(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata * __xdata *out) AK820_PH_FRAME_REENTRANT;
/* A returned pointer is valid only while the caller owns a slot pin. */
const ak820_ph_frame_t __xdata *ak820_ph_queue_record(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata *slot) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_queue_finish(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata *slot) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_queue_unclaim(ak820_ph_queue __xdata *q, ak820_ph_slot __xdata *slot) AK820_PH_FRAME_REENTRANT;
#endif
