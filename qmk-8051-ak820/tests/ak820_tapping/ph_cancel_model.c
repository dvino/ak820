// SPDX-License-Identifier: GPL-2.0-or-later
/* Host-only bounded lifecycle model. Not linked to action dispatch or firmware. */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ak820_ph_slots.h"
#define CHECK(x) do { if (!(x)) { fprintf(stderr, "check failed: %s:%d: %s\n", __FILE__, __LINE__, #x); exit(1); } } while (0)
enum { PHYSICAL = 8, GENERATED = 8, COMBO = 9, OWNERS = 10, OUTPUTS = 4, NONE = 255 };
typedef struct model model;
struct model {
    ak820_ph_slots slots;
    uint8_t depth, owner[OWNERS], refs[OUTPUTS], downs[OUTPUTS], ups[OUTPUTS];
    bool physical[PHYSICAL], blocked[PHYSICAL], quarantine, cleaning, combo_live;
    uint8_t combo_members;
    uint16_t combo_up_time;
    void (*on_up)(model *, uint8_t);
};
static void init(model *m) { memset(m, 0, sizeof(*m)); memset(m->owner, NONE, sizeof(m->owner)); ak820_ph_slots_init(&m->slots); }
static bool take(model *m, uint8_t owner, uint8_t output) {
    if (m->quarantine || owner >= OWNERS || output >= OUTPUTS || m->owner[owner] != NONE) return false;
    m->owner[owner] = output;
    if (!m->refs[output]++) ++m->downs[output];
    return true;
}
static void drop(model *m, uint8_t owner) {
    uint8_t output = m->owner[owner];
    if (output == NONE) return;
    m->owner[owner] = NONE;
    CHECK(m->refs[output]);
    if (!--m->refs[output]) { ++m->ups[output]; if (m->on_up) m->on_up(m, output); }
}
static bool press(model *m, uint8_t pos, uint8_t output) {
    if (pos >= PHYSICAL || m->physical[pos] || m->blocked[pos]) return false;
    m->physical[pos] = true;
    if (m->quarantine) { m->blocked[pos] = true; return false; }
    return take(m, pos, output);
}
static bool member_press(model *m, uint8_t pos) {
    if (pos >= PHYSICAL || m->physical[pos] || m->blocked[pos]) return false;
    m->physical[pos] = true;
    if (m->quarantine) { m->blocked[pos] = true; return false; }
    return true;
}
static bool combo_start(model *m, uint8_t a, uint8_t b, uint8_t output) {
    if (a >= PHYSICAL || b >= PHYSICAL || a == b || !m->physical[a] || !m->physical[b] || m->combo_live || m->blocked[a] || m->blocked[b]) return false;
    if (!take(m, COMBO, output)) return false;
    m->combo_members = (uint8_t)((1u << a) | (1u << b)); m->combo_live = true;
    return true;
}
static void release(model *m, uint8_t pos, uint16_t now) {
    CHECK(pos < PHYSICAL);
    if (!m->physical[pos]) return;
    m->physical[pos] = false;
    if (m->blocked[pos]) { m->blocked[pos] = false; return; }
    uint8_t bit = (uint8_t)(1u << pos);
    if (m->combo_live && (m->combo_members & bit)) {
        m->combo_members &= (uint8_t)~bit;
        if (!m->combo_members) {
            m->combo_live = false;
            m->combo_up_time = now;
            drop(m, COMBO);
        }
        return;
    }
    drop(m, pos);
}
static void drain_waiting(model *m) {
    ak820_ph_slot *slot;
    while ((slot = ak820_ph_slots_claim(&m->slots))) CHECK(ak820_ph_slot_finish(&m->slots, slot));
}
static void maybe_exit(model *m) {
    if (!m->cleaning && !m->depth && !m->slots.count) m->quarantine = false;
}
static void cancel(model *m) {
    if (m->cleaning) return;
    m->quarantine = true;
    m->cleaning = true;
    for (unsigned i = 0; i < PHYSICAL; ++i) if (m->physical[i]) m->blocked[i] = true;
    memset(m->owner, NONE, sizeof(m->owner));
    m->combo_live = false; m->combo_members = 0;
    uint8_t had[OUTPUTS];
    for (unsigned i = 0; i < OUTPUTS; ++i) { had[i] = m->refs[i]; m->refs[i] = 0; }
    drain_waiting(m);
    for (unsigned i = 0; i < OUTPUTS; ++i) if (had[i]) { ++m->ups[i]; if (m->on_up) m->on_up(m, i); }
    m->cleaning = false;
    maybe_exit(m);
}
static bool enqueue(model *m, uint16_t id) {
    if (m->quarantine) return false;
    ak820_ph_slot_event event = {.source=id};
    if (ak820_ph_slots_enqueue(&m->slots, &event)) return true;
    cancel(m);
    return false;
}
static void unwind(model *m) { CHECK(m->depth); --m->depth; if (m->quarantine) { drain_waiting(m); maybe_exit(m); } }
static void finish_claim(model *m, ak820_ph_slot *slot) { CHECK(ak820_ph_slot_finish(&m->slots, slot)); if (m->quarantine) { drain_waiting(m); maybe_exit(m); } }
static void release_pin(model *m, ak820_ph_slot *slot) { CHECK(ak820_ph_slot_unpin(&m->slots, slot)); if (m->quarantine) { drain_waiting(m); maybe_exit(m); } }
static unsigned reentrant_calls;
static void reenter(model *m, uint8_t output) {
    (void)output;
    ++reentrant_calls;
    CHECK(m->quarantine && m->cleaning);
    CHECK(!take(m, GENERATED, 0));
    CHECK(!press(m, 7, 0) && m->physical[7] && m->blocked[7]);
    cancel(m);
}
static void nested_overflow(void) {
    model m; init(&m);
    CHECK(press(&m, 0, 0) && press(&m, 1, 0) && press(&m, 2, 1) && press(&m, 3, 2));
    CHECK(member_press(&m, 4) && member_press(&m, 5) && combo_start(&m, 4, 5, 3));
    CHECK(m.refs[0] == 2 && m.downs[0] == 1 && m.downs[1] == 1 && m.downs[2] == 1 && m.downs[3] == 1);
    m.depth = 2;
    CHECK(enqueue(&m, 10));
    ak820_ph_slot *claimed = ak820_ph_slots_claim(&m.slots);
    CHECK(claimed && enqueue(&m, 11) && enqueue(&m, 12));
    m.on_up = reenter; reentrant_calls = 0;
    CHECK(!enqueue(&m, 13));
    CHECK(m.quarantine && !m.cleaning && m.slots.count == 1 && reentrant_calls == OUTPUTS);
    for (unsigned i = 0; i < OUTPUTS; ++i) CHECK(m.refs[i] == 0 && m.ups[i] == 1);
    for (unsigned i = 0; i < 6; ++i) CHECK(m.physical[i] && m.blocked[i]);
    CHECK(!take(&m, GENERATED, 0));
    CHECK(!press(&m, 6, 0) && m.physical[6] && m.blocked[6]);
    finish_claim(&m, claimed);
    unwind(&m); CHECK(m.quarantine && m.depth == 1 && !take(&m, GENERATED, 0));
    unwind(&m); CHECK(!m.quarantine && !m.depth);
    m.on_up = NULL;
    for (unsigned i = 0; i < 8; ++i) release(&m, i, 200);
    for (unsigned i = 0; i < OUTPUTS; ++i) CHECK(m.ups[i] == 1);
    CHECK(press(&m, 0, 0)); release(&m, 0, 210);
    CHECK(m.downs[0] == 2 && m.ups[0] == 2);
    puts("PASS: overflow cancellation releases each output once, blocks stale releases, unwinds claims");
}
static void vial_zero_depth(void) {
    model m; init(&m); CHECK(press(&m, 0, 0)); m.on_up = reenter; reentrant_calls = 0;
    cancel(&m);
    CHECK(!m.quarantine && !m.depth && !m.slots.count && m.ups[0] == 1 && m.blocked[0] && reentrant_calls == 1);
    CHECK(!press(&m, 0, 0)); release(&m, 0, 200); release(&m, 7, 200); CHECK(m.ups[0] == 1 && !m.blocked[0] && !m.blocked[7]);
    m.on_up = NULL; CHECK(press(&m, 0, 0)); release(&m, 0, 210); CHECK(m.ups[0] == 2);
    puts("PASS: zero-depth Vial-style cancellation exits but held source remains suppressed");
}
static void vial_zero_depth_claimed(void) {
    model m; init(&m); CHECK(press(&m, 0, 0) && enqueue(&m, 1));
    ak820_ph_slot *slot = ak820_ph_slots_claim(&m.slots);
    CHECK(slot);
    cancel(&m);
    CHECK(m.quarantine && !m.depth && m.slots.count == 1 && m.ups[0] == 1);
    finish_claim(&m, slot);
    CHECK(!m.quarantine && !m.slots.count && m.blocked[0]);
    release(&m, 0, 200); CHECK(m.ups[0] == 1);
    CHECK(press(&m, 0, 0)); release(&m, 0, 210); CHECK(m.ups[0] == 2);
    puts("PASS: zero-depth cancellation exits when its final claimed slot finishes");
}
static void vial_zero_depth_pinned(void) {
    model m; init(&m); CHECK(press(&m, 0, 0) && enqueue(&m, 1));
    ak820_ph_slot *slot = ak820_ph_slots_claim(&m.slots);
    CHECK(slot && ak820_ph_slot_pin(slot) && ak820_ph_slot_finish(&m.slots, slot));
    cancel(&m);
    CHECK(m.quarantine && !m.depth && m.slots.count == 1 && m.ups[0] == 1);
    release_pin(&m, slot);
    CHECK(!m.quarantine && !m.slots.count && m.blocked[0]);
    release(&m, 0, 200); CHECK(m.ups[0] == 1);
    puts("PASS: zero-depth quarantine exits after the final independent pin");
}
static void saturated_waiter(void) {
    model m; init(&m); CHECK(enqueue(&m, 1));
    ak820_ph_slot *slot = ak820_ph_slots_pin_at(&m.slots, 0);
    CHECK(slot);
    for (unsigned i = 1; i < 255; ++i) CHECK(ak820_ph_slot_pin(slot));
    cancel(&m);
    CHECK(m.quarantine && m.slots.count == 1 && slot->state == AK820_PH_WAITING);
    release_pin(&m, slot);
    CHECK(m.quarantine && m.slots.count == 1 && slot->state == AK820_PH_RETIRED);
    for (unsigned i = 1; i < 255; ++i) release_pin(&m, slot);
    CHECK(!m.quarantine && !m.slots.count);
    puts("PASS: saturated waiting slot drains after pin release, with no premature exit");
}
static void combo_both_orders(void) {
    for (unsigned reverse = 0; reverse < 2; ++reverse) {
        model m; init(&m); CHECK(member_press(&m, 4) && member_press(&m, 5) && combo_start(&m, 4, 5, 3));
        release(&m, reverse ? 5 : 4, 75); CHECK(m.ups[3] == 0 && m.combo_live);
        release(&m, reverse ? 4 : 5, 80); CHECK(m.ups[3] == 1 && !m.combo_live);
        printf("combo-last %u\n", m.combo_up_time);
    }
    model m; init(&m);
    CHECK(member_press(&m, 4) && member_press(&m, 5) && combo_start(&m, 4, 5, 3));
    release(&m, 4, 75); CHECK(press(&m, 4, 0));
    release(&m, 5, 80); CHECK(m.ups[3] == 1 && m.physical[4] && m.refs[0] == 1);
    release(&m, 4, 90); CHECK(m.ups[0] == 1);
    puts("PASS: repressed first member has a separate lifecycle");
}
int main(void) { vial_zero_depth(); nested_overflow(); vial_zero_depth_claimed(); vial_zero_depth_pinned(); saturated_waiter(); combo_both_orders(); return 0; }
