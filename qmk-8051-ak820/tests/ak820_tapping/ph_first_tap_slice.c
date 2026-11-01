// SPDX-License-Identifier: GPL-2.0-or-later
/* Narrow host-only first-tap experiment, not a production scheduler. */
#include <stdbool.h>
#include <stdio.h>
#include "ak820_ph_slots.h"

typedef struct {
    ak820_ph_slots slots;
    ak820_ph_slot_event tapping;
    uint8_t tap_count;
    bool nested_ok, no_replay;
} slice;

static void emit(slice *s, const ak820_ph_slot_event *event, uint8_t count);

/* Only the positive-tap, different-source ordinary release branch. */
static bool ordinary_release(slice *s, const ak820_ph_slot_event *event) {
    if (s->tap_count != 1 || event->pressed || event->source == s->tapping.source || event->committed != 6) return false;
    if (!ak820_ph_slots_enqueue(&s->slots, event)) return false;
    ak820_ph_slot *owned = ak820_ph_slots_claim(&s->slots);
    if (!owned || owned->event.source != event->source || owned->event.pressed) return false;
    emit(s, &owned->event, 0);
    if (!ak820_ph_slot_finish(&s->slots, owned)) return false;
    s->no_replay = !ak820_ph_slots_claim(&s->slots);
    return s->no_replay;
}

/* action_tapping.c first tap: commit count before callback, retain the
 * matching release, and dispatch it once with the saved tap decision. */
static bool first_tap_release(slice *s, const ak820_ph_slot_event *event) {
    if (s->tap_count || !s->tapping.pressed || event->pressed || event->source != s->tapping.source || event->committed != s->tapping.committed || (uint16_t)(event->time - s->tapping.time) >= 200) return false;
    if (!ak820_ph_slots_enqueue(&s->slots, event)) return false;
    ak820_ph_slot *owned = ak820_ph_slots_claim(&s->slots);
    if (!owned || owned->event.source != event->source || owned->event.pressed) return false;
    s->tap_count = 1;
    uint8_t decision = s->tap_count;
    ak820_ph_slot_event original = s->tapping;
    emit(s, &s->tapping, decision);
    if (!s->nested_ok || !s->no_replay || s->tap_count != decision ||
        s->tapping.source != original.source || s->tapping.time != original.time ||
        s->tapping.committed != original.committed || !s->tapping.pressed ||
        owned->state != AK820_PH_CLAIMED) return false;
    emit(s, &owned->event, decision);
    return ak820_ph_slot_finish(&s->slots, owned);
}

static void emit(slice *s, const ak820_ph_slot_event *event, uint8_t count) {
    printf("%u 110 %u %u %u %04x 00 0\n", event->time, event->source, event->pressed, count, event->committed);
    if (event->source == 1 && event->pressed && count == 1) {
        const ak820_ph_slot_event nested = {.source=0,.time=110,.committed=6,.observed=6,.pressed=0};
        s->nested_ok = ordinary_release(s, &nested);
    }
}

int main(void) {
    slice s = {.tapping={.source=1,.time=100,.committed=0x2204,.observed=0x2204,.pressed=1}};
    const ak820_ph_slot_event release = {.source=1,.time=110,.committed=0x2204,.observed=0x2204,.pressed=0};
    ak820_ph_slots_init(&s.slots);
    puts("90 90 0 1 0 0006 00 0"); /* Preheld ordinary owner, supplied by adapter. */
    if (!first_tap_release(&s, &release) || s.slots.count) return 1;
    return 0;
}
