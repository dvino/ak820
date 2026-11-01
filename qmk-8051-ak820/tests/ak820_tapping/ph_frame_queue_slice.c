// SPDX-License-Identifier: GPL-2.0-or-later
/* Host-only synchronous copy edge, not a PH scheduler, cancellation or IRQ model. */
#ifdef __SDCC_mcs51
#    error This slice is host-only
#endif
#include "ak820_ph_frame.h"
#include "ak820_ph_slots.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    ak820_ph_slots slots;
    ak820_ph_frame_t records[AK820_PH_SLOT_CAPACITY];
    bool failed;
} slice_queue;
typedef enum { SLICE_OK, SLICE_INVALID, SLICE_FULL, SLICE_FAILED } enqueue_result;
typedef enum { PUMP_OK, PUMP_BLOCKED, PUMP_ERROR } pump_result;
typedef enum { CALLBACK_OK, CALLBACK_BLOCKED, CALLBACK_COMMITTED_FAILURE } callback_result;
typedef callback_result (*slice_callback)(slice_queue *, ak820_ph_slot *, const ak820_ph_frame_t *, void *);

static void init(slice_queue *q) { memset(q, 0, sizeof(*q)); ak820_ph_slots_init(&q->slots); }
/* Borrow only during this serialized operation. No ownership transfer on any return. */
static enqueue_result enqueue(slice_queue *q, ak820_ph_frame_handle_t handle) {
    if (q->failed) return SLICE_FAILED;
    const ak820_ph_frame_t *frame = ak820_ph_frame_get(handle);
    if (!frame) return SLICE_INVALID;
    ak820_ph_slot_event event = {.source = frame->keycode, .time = frame->event.time,
                                 .pressed = frame->event.pressed, .kind = frame->event.type};
    if (!ak820_ph_slots_enqueue(&q->slots, &event)) return SLICE_FULL;
#ifndef PH_MUTANT_ALIAS
    q->records[q->slots.tail] = *frame;
#else
    (void)frame; /* negative control: lose the owned payload */
#endif
    return SLICE_OK;
}
static const ak820_ph_frame_t *claimed_record(slice_queue *q, ak820_ph_slot *slot) {
    if (!slot || slot->state != AK820_PH_CLAIMED || !slot->pins) return NULL;
    return &q->records[slot - q->slots.slots];
}
/* This drains storage only; it does not undo output or model cancellation. */
static void drain_waiting(slice_queue *q) {
    ak820_ph_slot *slot;
    while ((slot = ak820_ph_slots_claim(&q->slots))) {
        if (!ak820_ph_slot_finish(&q->slots, slot)) return;
    }
}
/* Retry storage cleanup after external pins are released; never clear the latch. */
static bool cleanup_failed(slice_queue *q) {
    if (!q->failed) return false;
    drain_waiting(q);
    return !q->slots.count;
}
static pump_result committed_failure(slice_queue *q, ak820_ph_slot *slot) {
#ifdef PH_MUTANT_RETRY_COMMITTED
    (void)q;
    return ak820_ph_slot_unclaim(slot) ? PUMP_BLOCKED : PUMP_ERROR;
#else
    q->failed = true;
    if (!ak820_ph_slot_finish(&q->slots, slot)) return PUMP_ERROR;
    drain_waiting(q);
    return PUMP_ERROR;
#endif
}
/* BLOCKED is retryable only before effects; a committed failure latches stop. */
static pump_result pump(slice_queue *q, slice_callback callback, void *context) {
    if (q->failed) return PUMP_ERROR;
    ak820_ph_slot *slot;
    while ((slot = ak820_ph_slots_claim(&q->slots))) {
        const ak820_ph_frame_t *record = claimed_record(q, slot);
        if (!record) return committed_failure(q, slot);
        callback_result result = callback(q, slot, record, context);
        if (q->failed || result == CALLBACK_COMMITTED_FAILURE) return committed_failure(q, slot);
        if (result == CALLBACK_BLOCKED) {
            if (ak820_ph_slot_unclaim(slot)) return PUMP_BLOCKED;
            return committed_failure(q, slot);
        }
        if (result != CALLBACK_OK) return committed_failure(q, slot);
        if (!ak820_ph_slot_finish(&q->slots, slot)) { q->failed = true; return PUMP_ERROR; }
    }
    for (uint8_t i = q->slots.head; i != UINT8_MAX; i = q->slots.slots[i].next) {
        if (q->slots.slots[i].state == AK820_PH_WAITING) return PUMP_ERROR;
    }
    return PUMP_OK;
}
static ak820_ph_frame_handle_t make(uint16_t code, uint8_t row, uint8_t col, uint16_t time, bool pressed) {
    ak820_ph_frame_handle_t h = ak820_ph_frame_reserve();
    assert(h);
    ak820_ph_frame_t *f = ak820_ph_frame_get(h);
    assert(f);
    f->keycode = code; f->event.key.row = row; f->event.key.col = col;
    f->event.type = KEY_EVENT; f->event.time = time; f->event.pressed = pressed;
    return h;
}
static void put_release(slice_queue *q, uint16_t code, uint8_t row, uint8_t col, uint16_t time, bool pressed) {
    ak820_ph_frame_handle_t h = make(code, row, col, time, pressed);
    assert(enqueue(q, h) == SLICE_OK);
    assert(ak820_ph_frame_release(h));
    assert(!ak820_ph_frame_get(h));
}
typedef struct { unsigned macro_count, rows, nested_done; } trace_state;
static callback_result trace(slice_queue *q, ak820_ph_slot *slot, const ak820_ph_frame_t *r, void *arg) {
    trace_state *s = arg;
    assert(r && slot->pins && slot->event.source == r->keycode && slot->event.time == r->event.time);
    assert(slot->event.pressed == r->event.pressed && slot->event.kind == r->event.type);
    assert(r->event.type == KEY_EVENT && r->event.key.row == 4);
    if (r->keycode == 0x7700) {
        if (++s->macro_count != 1) return CALLBACK_COMMITTED_FAILURE;
        assert(r->event.key.col == 1 && r->event.pressed && r->event.time == 110);
        printf("%u %04x %u\n", r->event.time, r->keycode, r->event.pressed);
        ++s->rows;
        if (pump(q, trace, s) != PUMP_OK) return CALLBACK_COMMITTED_FAILURE;
        assert(slot->state == AK820_PH_CLAIMED && slot->pins);
        assert(r->keycode == 0x7700 && r->event.key.row == 4 && r->event.key.col == 1 &&
               r->event.time == 110 && r->event.type == KEY_EVENT && r->event.pressed);
        s->nested_done = 1;
        return CALLBACK_OK;
    }
    if (r->keycode == 0x2105) {
        assert(r->event.key.col == 2);
        assert((r->event.pressed && r->event.time == 121) || (!r->event.pressed && r->event.time == 125));
        printf("%u %04x %u\n", r->event.time, r->keycode, r->event.pressed);
        if (r->event.pressed) puts("wait 5");
        ++s->rows;
        return CALLBACK_OK;
    }
    if (r->keycode == 0x2204) {
        assert(r->event.key.col == 0 && !r->event.pressed && r->event.time == 120);
        printf("%u %04x %u\n", r->event.time, r->keycode, r->event.pressed);
        ++s->rows;
        return CALLBACK_OK;
    }
    return CALLBACK_BLOCKED;
}
static callback_result blocked(slice_queue *q, ak820_ph_slot *slot, const ak820_ph_frame_t *r, void *ctx) {
    (void)q; (void)slot; (void)r; (void)ctx; return CALLBACK_BLOCKED;
}
static callback_result consume(slice_queue *q, ak820_ph_slot *slot, const ak820_ph_frame_t *r, void *ctx) {
    (void)q; (void)slot; (void)r; ++*(unsigned *)ctx; return CALLBACK_OK;
}
typedef struct { unsigned macros, attempts, child_effects; bool child_commits; } failure_state;
static callback_result nested_failure(slice_queue *q, ak820_ph_slot *slot, const ak820_ph_frame_t *r, void *ctx) {
    failure_state *s = ctx;
    if (r->keycode == 0x7700) {
        ++s->macros; /* Already-visible macro dispatch. */
        pump_result nested = pump(q, nested_failure, ctx);
        assert(nested != PUMP_OK);
        assert(slot->state == AK820_PH_CLAIMED && slot->pins && r->keycode == 0x7700);
        return CALLBACK_COMMITTED_FAILURE;
    }
    assert(r->keycode == 0x2105);
    ++s->attempts;
    if (!s->child_commits) return CALLBACK_BLOCKED;
    ++s->child_effects;
    return CALLBACK_COMMITTED_FAILURE;
}
static void check_nested_failure(bool child_commits) {
    slice_queue q;
    init(&q);
    put_release(&q, 0x7700, 4, 1, 110, true);
    put_release(&q, 0x2105, 4, 2, 121, true);
    put_release(&q, 0x2204, 4, 0, 120, false);
    ak820_ph_slot *pinned = ak820_ph_slots_pin_at(&q.slots, 0);
    assert(pinned);
    failure_state state = {.child_commits = child_commits};
    assert(pump(&q, nested_failure, &state) == PUMP_ERROR);
    assert(q.failed && state.macros == 1 && state.attempts == 1 && state.child_effects == (unsigned)child_commits);
    assert(pinned->state == AK820_PH_RETIRED && pinned->pins == 1 && q.slots.count == 1);
    assert(q.records[pinned - q.slots.slots].keycode == 0x7700);
    assert(pump(&q, nested_failure, &state) == PUMP_ERROR && state.macros == 1 && state.attempts == 1);
    ak820_ph_frame_handle_t h = make(0x9999, 7, 8, 130, true);
    assert(enqueue(&q, h) == SLICE_FAILED && ak820_ph_frame_get(h));
    assert(ak820_ph_frame_release(h));
    assert(ak820_ph_slot_unpin(&q.slots, pinned) && cleanup_failed(&q) && !q.slots.count);
    fprintf(stderr, "nested-failure child-committed=%u macro-effects=%u child-effects=%u; no replay, drained\n",
            child_commits, state.macros, state.child_effects);
}
static void check_nested_saturated_failure(void) {
    slice_queue q;
    init(&q);
    put_release(&q, 0x7700, 4, 1, 110, true);
    put_release(&q, 0x2105, 4, 2, 121, true);
    put_release(&q, 0x2204, 4, 0, 120, false);
    ak820_ph_slot *child = ak820_ph_slots_pin_at(&q.slots, 1);
    assert(child);
    for (unsigned i = 1; i < UINT8_MAX; ++i) assert(ak820_ph_slot_pin(child));
    failure_state state = {0};
    assert(pump(&q, nested_failure, &state) == PUMP_ERROR);
    assert(q.failed && state.macros == 1 && !state.attempts && !cleanup_failed(&q));
    assert(pump(&q, nested_failure, &state) == PUMP_ERROR && state.macros == 1);
    for (unsigned i = 0; i < UINT8_MAX; ++i) assert(ak820_ph_slot_unpin(&q.slots, child));
    assert(cleanup_failed(&q) && !q.slots.count && q.failed);
    fprintf(stderr, "nested-failure saturated-child macro-effects=%u; no replay, drained after unpin\n", state.macros);
}
int main(void) {
    slice_queue q;
    init(&q);
    put_release(&q, 0x7700, 4, 1, 110, true);
    put_release(&q, 0x2105, 4, 2, 121, true);
    put_release(&q, 0x2105, 4, 2, 125, false);
    put_release(&q, 0x2204, 4, 0, 120, false);
    ak820_ph_frame_handle_t full = make(0x4321, 9, 8, 999, true);
    assert(enqueue(&q, full) == SLICE_FULL);
    ak820_ph_frame_t *held = ak820_ph_frame_get(full);
    assert(held && held->keycode == 0x4321 && held->event.key.row == 9 && held->event.key.col == 8 &&
           held->event.time == 999 && held->event.type == KEY_EVENT && held->event.pressed);
    assert(ak820_ph_frame_release(full));
    assert(enqueue(&q, full) == SLICE_INVALID && q.slots.count == 4);
    trace_state state = {0};
    assert(pump(&q, trace, &state) == PUMP_OK);
    assert(state.rows == 4 && state.macro_count == 1 && state.nested_done && q.slots.count == 0);

    put_release(&q, 0x8888, 5, 6, 42, false);
    assert(pump(&q, blocked, NULL) == PUMP_BLOCKED && q.slots.count == 1);
    assert(q.slots.slots[q.slots.head].state == AK820_PH_WAITING);
    ak820_ph_slot *slot = ak820_ph_slots_claim(&q.slots);
    assert(slot);
#ifndef PH_MUTANT_NO_PIN
    assert(ak820_ph_slot_pin(slot));
#endif
    const ak820_ph_frame_t *pinned = claimed_record(&q, slot);
    assert(pinned && pinned->keycode == 0x8888 && pinned->event.key.row == 5 && pinned->event.key.col == 6 &&
           pinned->event.time == 42 && pinned->event.type == KEY_EVENT && !pinned->event.pressed);
    assert(ak820_ph_slot_finish(&q.slots, slot));
    assert(slot->state == AK820_PH_RETIRED && slot->pins == 1 && pinned->keycode == 0x8888 && pinned->event.time == 42);
    put_release(&q, 0x9999, 7, 8, 43, true);
    assert(pinned->keycode == 0x8888 && pinned->event.key.row == 5 && pinned->event.key.col == 6 &&
           pinned->event.time == 42 && pinned->event.type == KEY_EVENT && !pinned->event.pressed);
    assert(ak820_ph_slot_unpin(&q.slots, slot) && q.slots.count == 1);
    unsigned consumed = 0;
    assert(pump(&q, consume, &consumed) == PUMP_OK && consumed == 1 && !q.slots.count);
    put_release(&q, 0xaaaa, 1, 3, 44, true);
    slot = &q.slots.slots[q.slots.head];
    for (unsigned i = 0; i < UINT8_MAX; ++i) assert(ak820_ph_slot_pin(slot));
    assert(pump(&q, consume, &consumed) == PUMP_ERROR && slot->state == AK820_PH_WAITING);
    for (unsigned i = 0; i < UINT8_MAX; ++i) assert(ak820_ph_slot_unpin(&q.slots, slot));
    assert(pump(&q, consume, &consumed) == PUMP_OK && consumed == 2 && !q.slots.count);
    check_nested_failure(false);
    check_nested_failure(true);
    check_nested_saturated_failure();
    return 0;
}
