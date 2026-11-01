// SPDX-License-Identifier: GPL-2.0-or-later
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ph_scan_slots.h"
#define CHECK(x) do { if (!(x)) { fprintf(stderr, "check failed: %s:%d: %s\n", __FILE__, __LINE__, #x); exit(1); } } while (0)
typedef ph_scan_event keyevent_t;
typedef ph_scan_record keyrecord_t;
#define WAITING_BUFFER_SIZE 8
#define KEYEQ(a,b) ((a).row == (b).row && (a).col == (b).col)
#define IS_EVENT(e) ((e).type != 0)
#define WITHIN_TAPPING_TERM(e) ((uint16_t)((e).time - tapping_key.event.time) < ref_term)
#define ac_dprintf(...) ((void)0)
#define debug_waiting_buffer() ((void)0)
static keyrecord_t tapping_key, waiting_buffer[WAITING_BUFFER_SIZE];
static uint8_t waiting_buffer_head, waiting_buffer_tail;
static uint16_t ref_term;
static unsigned reference_calls;
static uint8_t callback_tap, callback_release;
static void process_record(keyrecord_t *record) {
    ++reference_calls;
    callback_tap = record->tap.count;
    callback_release = waiting_buffer[1].tap.count;
}
#include "retained_scan.inc"
static ph_scan_record make(uint8_t row, uint8_t col, uint16_t time, bool down, uint8_t type) {
    ph_scan_record record = {.event = {.key = {row, col}, .time = time, .pressed = down, .type = type}};
    return record;
}
typedef struct {
    ph_scan_queue *queue;
    ph_scan_record *tapping;
    ak820_ph_slot *slot;
    unsigned index, calls;
    bool finish_claim;
} callback_context;
static void on_tap(void *opaque) {
    callback_context *ctx = opaque;
    ++ctx->calls;
    CHECK(ctx->tapping->tap.count == 1);
    CHECK(ctx->queue->records[ctx->index].tap.count == 1);
    CHECK(ctx->slot->pins >= 1);
    CHECK(ph_scan_typed(ctx->queue, ctx->tapping->event) == PH_SCAN_YES);
    CHECK(ph_scan_tap(ctx->queue, ctx->tapping, 200, on_tap, ctx) == PH_SCAN_NO);
    if (ctx->finish_claim) {
        CHECK(ctx->slot->state == AK820_PH_CLAIMED && ctx->slot->pins >= 2);
        CHECK(ak820_ph_slot_finish(&ctx->queue->slots, ctx->slot));
        CHECK(ctx->slot->state == AK820_PH_RETIRED && ctx->slot->pins == 1);
        ph_scan_record next = make(0, 9, 115, true, 1);
        CHECK(ph_scan_enqueue(ctx->queue, &next));
        CHECK(ctx->queue->slots.tail != ctx->index);
        CHECK(ctx->queue->records[ctx->index].tap.count == 1);
    }
}
static void compare_reference_and_claimed(void) {
    ph_scan_queue q; ph_scan_init(&q);
    ph_scan_record a = make(0, 3, 105, true, 1), release = make(0, 1, 110, false, 1), other = make(0, 1, 120, false, 1);
    ph_scan_record tap = make(0, 1, 100, true, 1);
    CHECK(ph_scan_enqueue(&q, &a) && ph_scan_enqueue(&q, &release) && ph_scan_enqueue(&q, &other));
    ak820_ph_slot *first = ak820_ph_slots_claim(&q.slots);
    ak820_ph_slot *target = ak820_ph_slots_claim(&q.slots);
    CHECK(first && target && target == &q.slots.slots[1]);
    waiting_buffer[0] = a; waiting_buffer[1] = release; waiting_buffer[2] = other;
    waiting_buffer_tail = 0; waiting_buffer_head = 3; tapping_key = tap; ref_term = 200;
    ph_scan_event query = tap.event;
    CHECK(waiting_buffer_typed(query));
    CHECK(ph_scan_typed(&q, query) == PH_SCAN_YES);
    ph_scan_event claimed_only = a.event; claimed_only.pressed = false;
    CHECK(waiting_buffer_typed(claimed_only) && ph_scan_typed(&q, claimed_only) == PH_SCAN_YES);
    query.key.row = 1;
    CHECK(!waiting_buffer_typed(query) && ph_scan_typed(&q, query) == PH_SCAN_NO);
    reference_calls = 0; waiting_buffer_scan_tap();
    callback_context ctx = {.queue=&q, .tapping=&tap, .slot=target, .index=1};
    CHECK(ph_scan_tap(&q, &tap, 200, on_tap, &ctx) == PH_SCAN_YES);
    CHECK(reference_calls == 1 && ctx.calls == 1 && callback_tap == 1 && callback_release == 1);
    CHECK(tapping_key.tap.count == tap.tap.count && waiting_buffer[1].tap.count == q.records[1].tap.count);
    CHECK(waiting_buffer[2].tap.count == 0 && q.records[2].tap.count == 0);
    CHECK(target->state == AK820_PH_CLAIMED && target->pins == 1);
    CHECK(ak820_ph_slot_finish(&q.slots, target));
    CHECK(ak820_ph_slot_finish(&q.slots, first));
    puts("PASS: retained scan and typed rows match with a claimed release");
}
static void valid_event_and_settled(void) {
    ph_scan_queue q; ph_scan_init(&q);
    ph_scan_record invalid = make(0, 1, 105, false, 0), release = make(0, 1, 110, false, 1), tap = make(0, 1, 100, true, 1);
    CHECK(ph_scan_enqueue(&q, &invalid));
    waiting_buffer[0] = invalid; waiting_buffer_tail = 0; waiting_buffer_head = 1;
    CHECK(waiting_buffer_typed(tap.event) && ph_scan_typed(&q, tap.event) == PH_SCAN_YES);
    CHECK(ph_scan_enqueue(&q, &release));
    waiting_buffer[1] = release;
    waiting_buffer_tail = 0; waiting_buffer_head = 2; tapping_key = tap; ref_term = 200;
    CHECK(waiting_buffer_typed(tap.event) && ph_scan_typed(&q, tap.event) == PH_SCAN_YES);
    reference_calls = 0; waiting_buffer_scan_tap();
    callback_context ctx = {.queue=&q, .tapping=&tap, .slot=&q.slots.slots[1], .index=1};
    CHECK(ph_scan_tap(&q, &tap, 200, on_tap, &ctx) == PH_SCAN_YES);
    CHECK(reference_calls == 1 && ctx.calls == 1 && waiting_buffer[0].tap.count == 0 && q.records[0].tap.count == 0);
    CHECK(waiting_buffer[1].tap.count == 1 && q.records[1].tap.count == 1);
    tapping_key = tap; reference_calls = 0;
    waiting_buffer_scan_tap();
    CHECK(!reference_calls && ph_scan_tap(&q, &tap, 200, on_tap, &ctx) == PH_SCAN_NO);
    tap.tap.count = 0; tap.event.pressed = false; tapping_key = tap;
    waiting_buffer_scan_tap();
    CHECK(!reference_calls && ph_scan_tap(&q, &tap, 200, on_tap, &ctx) == PH_SCAN_NO);
    puts("PASS: scan skips invalid events and settled/released tapping records");
}
static void finish_during_callback(void) {
    ph_scan_queue q; ph_scan_init(&q);
    ph_scan_record release = make(0, 1, 110, false, 1), tap = make(0, 1, 100, true, 1);
    CHECK(ph_scan_enqueue(&q, &release));
    ak820_ph_slot *slot = ak820_ph_slots_claim(&q.slots);
    CHECK(slot);
    callback_context ctx = {.queue=&q, .tapping=&tap, .slot=slot, .index=0, .finish_claim=true};
    CHECK(ph_scan_tap(&q, &tap, 200, on_tap, &ctx) == PH_SCAN_YES);
    CHECK(ctx.calls == 1 && q.slots.count == 1 && q.slots.head == 1 && q.slots.tail == 1);
    puts("PASS: callback finishes claim but scan pin prevents payload reuse until return");
}
typedef struct {
    ph_scan_queue *queue;
    ph_scan_record *outer_tap, inner_tap;
    ak820_ph_slot *outer, *inner;
    unsigned outer_calls, inner_calls;
} nested_context;
static void nested_inner(void *opaque) {
    nested_context *ctx = opaque;
    ++ctx->inner_calls;
    CHECK(ctx->outer->pins >= 2 && ctx->inner->pins >= 2);
    CHECK(ctx->outer_tap->tap.count == 1 && ctx->inner_tap.tap.count == 1);
    CHECK(ctx->queue->records[0].tap.count == 1 && ctx->queue->records[1].tap.count == 1);
}
static void nested_outer(void *opaque) {
    nested_context *ctx = opaque;
    ++ctx->outer_calls;
    CHECK(ctx->outer->pins >= 2);
    CHECK(ph_scan_tap(ctx->queue, &ctx->inner_tap, 200, nested_inner, ctx) == PH_SCAN_YES);
    CHECK(ctx->outer->pins >= 2 && ctx->inner->pins == 1);
}
static void recursive_distinct_scan(void) {
    ph_scan_queue q; ph_scan_init(&q);
    ph_scan_record release1 = make(0, 1, 110, false, 1), release2 = make(0, 2, 111, false, 1), tap = make(0, 1, 100, true, 1);
    CHECK(ph_scan_enqueue(&q, &release1) && ph_scan_enqueue(&q, &release2));
    ak820_ph_slot *outer = ak820_ph_slots_claim(&q.slots);
    CHECK(outer);
    ak820_ph_slot *inner = ak820_ph_slots_pin_at(&q.slots, 1);
    CHECK(inner);
    nested_context ctx = {.queue=&q, .outer_tap=&tap, .inner_tap=make(0, 2, 100, true, 1), .outer=outer, .inner=inner};
    CHECK(ph_scan_tap(&q, &tap, 200, nested_outer, &ctx) == PH_SCAN_YES);
    CHECK(ctx.outer_calls == 1 && ctx.inner_calls == 1 && outer->pins == 1);
    CHECK(ak820_ph_slot_unpin(&q.slots, inner));
    CHECK(ak820_ph_slot_finish(&q.slots, outer));
    puts("PASS: nested distinct scan retains outer pin and both write-backs");
}
static void bounds_and_visibility(void) {
    for (unsigned difference = 9; difference <= 10; ++difference) {
        ph_scan_queue q; ph_scan_init(&q);
        ph_scan_record release = make(0, 1, (uint16_t)(65530 + difference), false, 1), tap = make(0, 1, 65530, true, 1);
        CHECK(ph_scan_enqueue(&q, &release));
        waiting_buffer[0] = release; waiting_buffer_tail = 0; waiting_buffer_head = 1; tapping_key = tap; ref_term = 10; reference_calls = 0;
        waiting_buffer_scan_tap();
        callback_context ctx = {.queue=&q, .tapping=&tap, .slot=&q.slots.slots[0], .index=0};
        ph_scan_result got = ph_scan_tap(&q, &tap, 10, on_tap, &ctx);
        CHECK(got == (difference == 9 ? PH_SCAN_YES : PH_SCAN_NO));
        CHECK(reference_calls == ctx.calls && tapping_key.tap.count == tap.tap.count && waiting_buffer[0].tap.count == q.records[0].tap.count);
    }
    ph_scan_queue q; ph_scan_init(&q);
    ph_scan_record release = make(0, 1, 110, false, 1), tap = make(0, 1, 100, true, 1);
    CHECK(ph_scan_enqueue(&q, &release));
    ak820_ph_slot *slot = ak820_ph_slots_claim(&q.slots);
    CHECK(slot && ak820_ph_slot_pin(slot) && ak820_ph_slot_finish(&q.slots, slot));
    CHECK(slot->state == AK820_PH_RETIRED && ph_scan_typed(&q, tap.event) == PH_SCAN_NO);
    callback_context ctx = {.queue=&q, .tapping=&tap, .slot=slot, .index=0};
    CHECK(ph_scan_tap(&q, &tap, 200, on_tap, &ctx) == PH_SCAN_NO && ctx.calls == 0);
    CHECK(ak820_ph_slot_unpin(&q.slots, slot));
    CHECK(ph_scan_enqueue(&q, &release));
    slot = &q.slots.slots[q.slots.tail];
    for (unsigned i = 0; i < 255; ++i) CHECK(ak820_ph_slot_pin(slot));
    CHECK(ph_scan_typed(&q, tap.event) == PH_SCAN_ERROR);
    CHECK(ph_scan_tap(&q, &tap, 200, on_tap, &ctx) == PH_SCAN_ERROR);
    CHECK(tap.tap.count == 0 && q.records[q.slots.tail].tap.count == 0);
    for (unsigned i = 0; i < 255; ++i) CHECK(ak820_ph_slot_unpin(&q.slots, slot));
    puts("PASS: wrap boundary, retired invisibility and saturated-pin errors");
}
int main(void) { compare_reference_and_claimed(); valid_event_and_settled(); finish_during_callback(); recursive_distinct_scan(); bounds_and_visibility(); return 0; }
