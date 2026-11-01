// SPDX-License-Identifier: GPL-2.0-or-later
/* Host-only contract model: real experimental frame/queue/slot APIs, mocked
 * logical output and physical sources. Raw queue traversal is not corruption
 * safe; injected result faults do not prove recovery from corrupted links.
 * Not firmware or IRQ-safe dispatch. */
#ifndef PH_CANCEL_HOST_MODEL
#    error This model is for explicitly enabled host tests only
#endif
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ak820_ph_queue.h"

#define CHECK(x) do { if (!(x)) { fprintf(stderr, "FAIL %s:%d: %s\n", __func__, __LINE__, #x); exit(1); } } while (0)
enum { SOURCES = 8, SCOPES = 4, OUTPUTS = 2 };
typedef struct model model;
typedef struct scope {
    ak820_ph_frame_handle_t frame;
    ak820_ph_slot *claim;
    bool active, revoked;
} scope;
struct model {
    ak820_ph_queue q;
    /* Model owns scopes and must not be reset or destroyed while any remain.
     * Borrowed scope pointers expire on normal close; faulted slots never reuse. */
    scope owned_scopes[SCOPES];
    scope *scopes[SCOPES];
    uint8_t physical, blocked, logical_owners, owner_output[SOURCES], asserted, pending_cleanup;
    bool quarantine, cleaning, cleanup_failed, invariant_failed, inject_finish_failure;
    unsigned claim_injection;
    ak820_ph_slot foreign;
    unsigned cleanup_attempts, dispatches, effects, continuations, normal_ups;
    bool (*cleanup)(model *m, unsigned output);
};

static void init(model *m) { memset(m, 0, sizeof(*m)); ak820_ph_queue_init(&m->q); }
static void cancel(model *m);
static void progress(model *m);

static bool take_output(model *m, unsigned source, unsigned output) {
    if (m->quarantine || source >= SOURCES || output >= OUTPUTS || (m->logical_owners & (1u << source))) return false;
    m->logical_owners |= (uint8_t)(1u << source);
    m->owner_output[source] = (uint8_t)output;
    m->asserted |= (uint8_t)(1u << output);
    return true;
}
static bool press(model *m, unsigned source) {
    uint8_t bit = (uint8_t)(1u << source);
    CHECK(source < SOURCES);
    if ((m->physical | m->blocked) & bit) return false;
    m->physical |= bit;
    if (m->quarantine) { m->blocked |= bit; return false; }
    return take_output(m, source, 0);
}
static void release(model *m, unsigned source) {
    uint8_t bit = (uint8_t)(1u << source);
    CHECK(source < SOURCES);
    if (!(m->physical & bit)) return;
    m->physical &= (uint8_t)~bit;
    if (m->blocked & bit) { m->blocked &= (uint8_t)~bit; return; }
    if (m->logical_owners & bit) {
        uint8_t output = m->owner_output[source];
        m->logical_owners &= (uint8_t)~bit;
        for (unsigned i = 0; i < SOURCES; ++i) {
            if ((m->logical_owners & (1u << i)) && m->owner_output[i] == output) return;
        }
        m->asserted &= (uint8_t)~(1u << output);
        ++m->normal_ups;
    }
}
static bool scope_open(model *m, scope **out) {
    *out = NULL;
    if (m->quarantine) return false;
    for (unsigned i = 0; i < SCOPES; ++i) if (!m->scopes[i]) {
        ak820_ph_frame_handle_t h = ak820_ph_frame_reserve();
        if (!h) {
#ifndef MUTANT_SCOPE_FRAME_FAIL_OPEN
            cancel(m);
#endif
            return false;
        }
        scope *s = &m->owned_scopes[i];
        memset(s, 0, sizeof(*s)); s->frame = h; s->active = true; m->scopes[i] = s;
        *out = s;
        return true;
    }
#ifndef MUTANT_SCOPE_TABLE_FAIL_OPEN
    cancel(m);
#endif
    return false;
}
static bool enqueue(model *m, uint16_t keycode) {
    if (m->quarantine) return false;
    ak820_ph_frame_handle_t h = ak820_ph_frame_reserve();
    if (!h) { cancel(m); return false; }
    ak820_ph_frame_t *f = ak820_ph_frame_get(h);
    CHECK(f); f->keycode = keycode; f->event.type = KEY_EVENT; f->event.pressed = true; f->event.time = keycode;
    ak820_ph_queue_result r = ak820_ph_queue_enqueue(&m->q, h);
    CHECK(ak820_ph_frame_release(h));
    if (r != AK820_PH_QUEUE_OK) { cancel(m); return false; }
    return true;
}
static void fault(model *m) {
    m->invariant_failed = true;
    cancel(m);
}
static bool member_claim(model *m, ak820_ph_slot *slot) {
    for (unsigned i = 0; i < AK820_PH_SLOT_CAPACITY; ++i) {
        if (slot == &m->q.slots.slots[i]) {
            if (slot->state != AK820_PH_CLAIMED || !slot->pins) return false;
            for (unsigned j = 0; j < SCOPES; ++j) if (m->scopes[j] && m->scopes[j]->claim == slot) return false;
            uint8_t cur = m->q.slots.head;
            for (unsigned n = 0; n < AK820_PH_SLOT_CAPACITY && cur != UINT8_MAX; ++n) {
                if (cur >= AK820_PH_SLOT_CAPACITY) return false;
                if (&m->q.slots.slots[cur] == slot) return true;
                cur = m->q.slots.slots[cur].next;
            }
            return false;
        }
    }
    return false;
}
/* Fault injection substitutes a result before the raw queue is touched. */
static ak820_ph_queue_result guarded_claim(model *m, scope *s, ak820_ph_queue *q) {
    if (m->quarantine) return AK820_PH_QUEUE_INVALID;
    bool registered = false;
    for (unsigned i = 0; i < SCOPES; ++i) if (m->scopes[i] == s && s) registered = true;
    if (!registered || !s->active || s->revoked || s->claim || (q && q != &m->q)) {
        fault(m); return AK820_PH_QUEUE_INVALID;
    }
    ak820_ph_slot *slot = NULL;
    ak820_ph_queue_result r;
    if (m->claim_injection == 1) r = AK820_PH_QUEUE_FULL;
    else if (m->claim_injection == 2) r = AK820_PH_QUEUE_OK;
    else if (m->claim_injection == 3) { slot = &m->foreign; r = AK820_PH_QUEUE_OK; }
    else if (m->claim_injection == 4) { slot = &m->q.slots.slots[1]; r = AK820_PH_QUEUE_OK; }
    else if (m->claim_injection == 5) { slot = &m->foreign; r = AK820_PH_QUEUE_NO_WAITING; }
    else if (m->claim_injection == 6) { slot = &m->q.slots.slots[0]; r = AK820_PH_QUEUE_OK; }
    else if (m->claim_injection == 7) { slot = &m->q.slots.slots[2]; r = AK820_PH_QUEUE_OK; }
    else r = ak820_ph_queue_claim(q, &slot);
    if (r == AK820_PH_QUEUE_OK) {
        if (!member_claim(m, slot)) { fault(m); return AK820_PH_QUEUE_INVALID; }
        s->claim = slot;
        return r;
    }
    if ((r == AK820_PH_QUEUE_NO_WAITING || r == AK820_PH_QUEUE_PIN_LIMIT) && slot) {
        fault(m); return AK820_PH_QUEUE_INVALID;
    }
    if (r == AK820_PH_QUEUE_NO_WAITING) return r;
    if (r == AK820_PH_QUEUE_PIN_LIMIT) {
#ifdef MUTANT_PIN_SKIP
        for (uint8_t i = m->q.slots.head; i != UINT8_MAX; i = m->q.slots.slots[i].next) {
            ak820_ph_slot *candidate = &m->q.slots.slots[i];
            if (candidate->state == AK820_PH_WAITING && candidate->pins != UINT8_MAX) {
                ++m->dispatches; ++m->effects; break;
            }
        }
#endif
#ifndef MUTANT_PIN_IDLE
        cancel(m);
#endif
        return r;
    }
#ifdef MUTANT_INVALID_IDLE
    return AK820_PH_QUEUE_NO_WAITING;
#endif
    fault(m);
    return AK820_PH_QUEUE_INVALID;
}
static bool scope_claim(model *m, scope *s) {
    return guarded_claim(m, s, &m->q) == AK820_PH_QUEUE_OK;
}
static void scope_close(model *m, scope *s) {
    CHECK(s->active);
#ifdef MUTANT_REPLAY_CLAIM
    if (s->claim && s->revoked) {
        ak820_ph_slot *again = NULL;
        CHECK(ak820_ph_queue_unclaim(&m->q, s->claim));
        s->claim = NULL;
        CHECK(ak820_ph_queue_claim(&m->q, &again) == AK820_PH_QUEUE_OK && again);
        ++m->dispatches; ++m->effects;
        CHECK(ak820_ph_queue_finish(&m->q, again));
    }
#endif
    if (m->invariant_failed) {
#ifdef MUTANT_FAULT_DROP_SCOPE
        for (unsigned i = 0; i < SCOPES; ++i) if (m->scopes[i] == s) m->scopes[i] = NULL;
#endif
#ifdef MUTANT_FAULT_RELEASE_FRAME
        CHECK(ak820_ph_frame_release(s->frame));
#endif
        return;
    }
    if (s->claim && (m->inject_finish_failure || !ak820_ph_queue_finish(&m->q, s->claim))) { fault(m); return; }
    s->claim = NULL;
    if (!ak820_ph_frame_release(s->frame)) { fault(m); return; }
    bool found = false;
    for (unsigned i = 0; i < SCOPES; ++i) if (m->scopes[i] == s) { m->scopes[i] = NULL; found = true; break; }
    CHECK(found); s->active = false;
    progress(m);
}
static void progress(model *m) {
    if (!m->quarantine || m->cleaning) return;
#ifndef MUTANT_FAULT_DRAIN
    if (m->invariant_failed) return;
#endif
    ak820_ph_slot *slot;
    ak820_ph_queue_result r;
    while ((r = ak820_ph_queue_claim(&m->q, &slot)) == AK820_PH_QUEUE_OK) {
#ifdef MUTANT_DISPATCH_WAITING
        ++m->dispatches;
#endif
        if (!ak820_ph_queue_finish(&m->q, slot)) { m->invariant_failed = true; return; }
    }
    if (r != AK820_PH_QUEUE_NO_WAITING && r != AK820_PH_QUEUE_PIN_LIMIT) { m->invariant_failed = true; return; }
    for (unsigned i = 0; i < SCOPES; ++i) if (m->scopes[i]) return;
#ifndef MUTANT_IGNORE_QUEUE
    if (m->q.slots.count) return;
#endif
    if (m->pending_cleanup || m->asserted || m->logical_owners || m->cleanup_failed || m->invariant_failed) return;
#ifdef MUTANT_CLEAR_BLOCKS
    m->blocked = 0;
#endif
    m->quarantine = false;
}
static void cancel(model *m) {
    if (m->quarantine) return;
    m->quarantine = true; m->cleaning = true;
    m->blocked |= m->physical;
#ifndef MUTANT_NO_REVOKE
    for (unsigned i = 0; i < SCOPES; ++i) if (m->scopes[i]) m->scopes[i]->revoked = true;
#endif
    m->logical_owners = 0;
    m->pending_cleanup = m->asserted;
    for (unsigned output = 0; output < OUTPUTS; ++output) {
        uint8_t bit = (uint8_t)(1u << output);
        if (!(m->pending_cleanup & bit)) continue;
        ++m->cleanup_attempts;
        if (m->cleanup && m->cleanup(m, output)) {
            m->pending_cleanup &= (uint8_t)~bit; m->asserted &= (uint8_t)~bit;
        } else {
#ifndef MUTANT_ACCEPT_FAILED_CLEANUP
            m->cleanup_failed = true;
            break;
#else
            m->pending_cleanup &= (uint8_t)~bit; m->asserted &= (uint8_t)~bit;
#endif
        }
    }
    m->cleaning = false;
    progress(m);
}
static void unpin(model *m, ak820_ph_slot *slot) {
    CHECK(ak820_ph_slot_unpin(&m->q.slots, slot));
    progress(m);
}
static bool cleanup_ok(model *m, unsigned output) { (void)m; (void)output; return true; }
static bool cleanup_fails_reentrant(model *m, unsigned output) {
    (void)output;
    CHECK(m->quarantine && m->cleaning && !m->logical_owners);
    CHECK(!take_output(m, 7, 0));
    CHECK(!press(m, 6) && (m->blocked & (1u << 6)));
    cancel(m);
    CHECK(m->cleanup_attempts == 1);
    return false;
}

static void claimed_and_pinned_waiting(void) {
    model m; scope *s; init(&m); m.cleanup = cleanup_ok;
    CHECK(scope_open(&m, &s));
    CHECK(enqueue(&m, 0x1111) && scope_claim(&m, s) && enqueue(&m, 0x2222));
    ak820_ph_slot *waiting = ak820_ph_slots_pin_at(&m.q.slots, 1);
    CHECK(waiting && waiting->state == AK820_PH_WAITING);
    cancel(&m);
    CHECK(m.quarantine && s->revoked && s->claim->state == AK820_PH_CLAIMED);
    CHECK(waiting->state == AK820_PH_RETIRED && waiting->pins == 1 && m.q.slots.count == 2);
    const ak820_ph_frame_t *record = ak820_ph_queue_record(&m.q, waiting);
    CHECK(record && record->keycode == 0x2222 && !m.dispatches);
    CHECK(!enqueue(&m, 0x3333));
    scope_close(&m, s);
    CHECK(m.quarantine && m.q.slots.count == 1 && record->keycode == 0x2222);
    unpin(&m, waiting);
    CHECK(!m.quarantine && !m.q.slots.count && !m.dispatches);
    puts("PASS: claimed plus pinned waiting: revoke, retire without dispatch, retain until unpin");
}
static void saturated_waiting(void) {
    model m; init(&m); CHECK(enqueue(&m, 1) && enqueue(&m, 2));
    ak820_ph_slot *waiting = ak820_ph_slots_pin_at(&m.q.slots, 0);
    CHECK(waiting);
    for (unsigned i = 1; i < UINT8_MAX; ++i) CHECK(ak820_ph_slot_pin(waiting));
    ak820_ph_slot *claim = NULL;
    CHECK(ak820_ph_queue_claim(&m.q, &claim) == AK820_PH_QUEUE_PIN_LIMIT && !claim);
    cancel(&m);
    CHECK(m.quarantine && m.q.slots.count == 2 && waiting->state == AK820_PH_WAITING && waiting->pins == UINT8_MAX && !m.dispatches);
    unpin(&m, waiting);
    CHECK(m.quarantine && m.q.slots.count == 1 && waiting->state == AK820_PH_RETIRED && waiting->pins == UINT8_MAX - 1 && !m.dispatches);
    for (unsigned i = 0; i < UINT8_MAX - 1; ++i) unpin(&m, waiting);
    CHECK(!m.quarantine && !m.q.slots.count && !m.dispatches);
    puts("PASS: saturated waiter blocks drain and exit; retry after unpin retains storage");
}
static void failed_cleanup(void) {
    model m; init(&m); m.cleanup = cleanup_fails_reentrant;
    CHECK(press(&m, 0));
    cancel(&m);
    CHECK(m.quarantine && m.cleanup_failed && m.pending_cleanup && m.asserted && !m.logical_owners);
    CHECK(m.cleanup_attempts == 1 && (m.blocked & 1) && (m.blocked & (1u << 6)));
    for (unsigned i = 0; i < 3; ++i) progress(&m);
    CHECK(m.quarantine && m.cleanup_attempts == 1 && !take_output(&m, 1, 0));
    puts("PASS: failed actual model cleanup remains quarantined without retry or reacquisition");
}
static bool cleanup_partial(model *m, unsigned output) {
    CHECK(m->quarantine && m->cleaning && !m->logical_owners);
    CHECK(!take_output(m, 7, output));
    if (output == 0) { CHECK(m->asserted == 3 && m->pending_cleanup == 3); return true; }
    CHECK(output == 1 && m->asserted == 2 && m->pending_cleanup == 2);
    return false;
}
static void partial_cleanup_failure(void) {
    model m; init(&m); m.cleanup = cleanup_partial;
    CHECK(press(&m, 0) && take_output(&m, 1, 0) && take_output(&m, 2, 1));
    CHECK(m.logical_owners == 7 && m.asserted == 3);
    cancel(&m);
    CHECK(m.quarantine && m.cleanup_failed && m.cleanup_attempts == 2);
    CHECK(!m.logical_owners && m.pending_cleanup == 2 && m.asserted == 2 && m.blocked == 1);
    for (unsigned i = 0; i < 3; ++i) progress(&m);
    CHECK(m.quarantine && m.cleanup_attempts == 2 && m.pending_cleanup == 2 && m.asserted == 2);
    puts("PASS: shared owners detach, partial model cleanup failure blocks exit without retry");
}
static void held_release_after_exit(void) {
    model m; init(&m); m.cleanup = cleanup_ok;
    CHECK(press(&m, 0)); cancel(&m);
    CHECK(!m.quarantine && m.blocked == 1 && m.physical == 1 && m.cleanup_attempts == 1);
    CHECK(press(&m, 1));
    release(&m, 0);
    CHECK(!m.blocked && m.asserted && m.logical_owners == 2 && !m.normal_ups);
    release(&m, 1);
    CHECK(!m.asserted && m.normal_ups == 1);
    CHECK(press(&m, 0)); release(&m, 0); CHECK(m.normal_ups == 2);
    puts("PASS: held source release after exit suppressed without releasing a new owner");
}
static void scope_allocation_failure(void) {
    model m; scope *held, *denied; ak820_ph_frame_handle_t extra[AK820_PH_FRAME_CAPACITY - 1];
    init(&m); m.cleanup = cleanup_ok;
    CHECK(press(&m, 0) && scope_open(&m, &held));
    for (unsigned i = 0; i < AK820_PH_FRAME_CAPACITY - 1; ++i) { extra[i] = ak820_ph_frame_reserve(); CHECK(extra[i]); }
    CHECK(!scope_open(&m, &denied));
    CHECK(m.quarantine && held->revoked && m.cleanup_attempts == 1 && !m.asserted && !m.logical_owners && m.blocked == 1);
    for (unsigned i = 0; i < AK820_PH_FRAME_CAPACITY - 1; ++i) CHECK(ak820_ph_frame_release(extra[i]));
    CHECK(m.quarantine);
    scope_close(&m, held);
    CHECK(!m.quarantine && m.blocked == 1);
    release(&m, 0); CHECK(!m.blocked && !m.normal_ups);
    puts("PASS: scope frame-pool exhaustion cancels, cleans and waits for scope unwind");
}
static void scope_table_failure(void) {
    model n; scope *full[SCOPES], *overflow;
    init(&n); n.cleanup = cleanup_ok;
    CHECK(press(&n, 0));
    for (unsigned i = 0; i < SCOPES; ++i) CHECK(scope_open(&n, &full[i]));
    CHECK(!scope_open(&n, &overflow));
    CHECK(n.quarantine && n.cleanup_attempts == 1 && !n.asserted && !n.logical_owners);
    for (unsigned i = 0; i < SCOPES; ++i) CHECK(full[i]->revoked);
    for (unsigned i = 0; i < SCOPES; ++i) { scope_close(&n, full[i]); if (i + 1 < SCOPES) CHECK(n.quarantine); }
    CHECK(!n.quarantine && n.blocked == 1);
    release(&n, 0); CHECK(!n.blocked && !n.normal_ups);
    puts("PASS: scope table exhaustion cancels, cleans and waits for scope unwind");
}
static void nested_cancel(model *m, scope *outer) {
    scope *inner, *denied;
    CHECK(scope_open(m, &inner) && scope_claim(m, inner));
    ak820_ph_slot *inner_pin = inner->claim;
    CHECK(ak820_ph_slot_pin(inner_pin));
    const ak820_ph_frame_t *inner_record = ak820_ph_queue_record(&m->q, inner_pin);
    CHECK(inner_record && inner_record->keycode == 0x5678);
    CHECK(enqueue(m, 0x9abc));
    ak820_ph_slot *waiting = ak820_ph_slots_pin_at(&m->q.slots, 2);
    CHECK(waiting && waiting->state == AK820_PH_WAITING);
    ++m->dispatches; ++m->effects;
    cancel(m);
    CHECK(m->quarantine && inner->revoked && outer->revoked);
    CHECK(inner->claim->state == AK820_PH_CLAIMED && outer->claim->state == AK820_PH_CLAIMED);
    CHECK(waiting->state == AK820_PH_RETIRED && waiting->pins == 1 && m->q.slots.count == 3);
    const ak820_ph_frame_t *waiting_record = ak820_ph_queue_record(&m->q, waiting);
    CHECK(waiting_record && waiting_record->keycode == 0x9abc && inner_record->keycode == 0x5678);
    CHECK(!scope_open(m, &denied) && !enqueue(m, 0x44) && !take_output(m, 3, 0));
    if (!inner->revoked) ++m->continuations;
    scope_close(m, inner);
    CHECK(m->quarantine && outer->active && inner_pin->state == AK820_PH_RETIRED && inner_pin->pins == 1);
    unpin(m, inner_pin);
    CHECK(m->quarantine && m->q.slots.count == 2);
    unpin(m, waiting);
    CHECK(m->quarantine && m->q.slots.count == 1);
}
static void nested_revocation_no_replay(void) {
    model m; scope *outer; init(&m); m.cleanup = cleanup_ok;
    CHECK(press(&m, 0) && scope_open(&m, &outer));
    CHECK(enqueue(&m, 0x1234) && scope_claim(&m, outer) && enqueue(&m, 0x5678));
    ak820_ph_slot *outer_pin = outer->claim;
    CHECK(ak820_ph_slot_pin(outer_pin));
    const ak820_ph_frame_t *r = ak820_ph_queue_record(&m.q, outer->claim);
    CHECK(r && r->keycode == 0x1234);
    ++m.dispatches; ++m.effects;
    nested_cancel(&m, outer);
    if (!outer->revoked) ++m.continuations;
    scope_close(&m, outer);
    CHECK(m.quarantine && outer_pin->state == AK820_PH_RETIRED && outer_pin->pins == 1);
    unpin(&m, outer_pin);
    CHECK(!m.quarantine && !m.q.slots.count && m.dispatches == 2 && m.effects == 2 && !m.continuations);
    ak820_ph_slot *again = NULL;
    CHECK(ak820_ph_queue_claim(&m.q, &again) == AK820_PH_QUEUE_NO_WAITING && !again);
    CHECK(m.cleanup_attempts == 1 && m.blocked == 1);
    puts("PASS: nested claimed/pinned scopes revoke, finish once and never replay");
}
static void claim_idle(void) {
    model m; scope *outer, *inner; init(&m); m.cleanup = cleanup_ok;
    CHECK(scope_open(&m, &outer));
    CHECK(guarded_claim(&m, outer, &m.q) == AK820_PH_QUEUE_NO_WAITING);
    CHECK(!m.quarantine && !outer->claim && !m.q.slots.count);
    CHECK(enqueue(&m, 0x1111) && scope_claim(&m, outer));
    CHECK(scope_open(&m, &inner));
    CHECK(guarded_claim(&m, inner, &m.q) == AK820_PH_QUEUE_NO_WAITING);
    CHECK(!m.quarantine && !inner->claim && outer->claim && m.q.slots.count == 1);
    CHECK(!m.dispatches && !m.effects);
    scope_close(&m, inner); scope_close(&m, outer);
    CHECK(!m.quarantine && !m.q.slots.count);
    puts("PASS: idle claim distinguishes empty from outstanding claimed record");
}
static void claim_saturation(void) {
    model m; scope *outer, *inner; init(&m); m.cleanup = cleanup_ok;
    CHECK(press(&m, 0) && scope_open(&m, &outer));
    CHECK(enqueue(&m, 0x1111) && scope_claim(&m, outer));
    CHECK(enqueue(&m, 0x2222) && enqueue(&m, 0x3333));
    ak820_ph_slot *waiting = ak820_ph_slots_pin_at(&m.q.slots, 1);
    CHECK(waiting && waiting->state == AK820_PH_WAITING);
    for (unsigned i = 1; i < UINT8_MAX; ++i) CHECK(ak820_ph_slot_pin(waiting));
    CHECK(scope_open(&m, &inner));
    CHECK(guarded_claim(&m, inner, &m.q) == AK820_PH_QUEUE_PIN_LIMIT);
    CHECK(m.quarantine && !m.invariant_failed && outer->revoked && inner->revoked && outer->claim && !inner->claim);
    CHECK(waiting->state == AK820_PH_WAITING && waiting->pins == UINT8_MAX && m.q.slots.count == 3);
    CHECK(!m.dispatches && !m.effects && m.cleanup_attempts == 1 && !m.asserted);
    if (!inner->revoked) ++m.continuations;
    if (!outer->revoked) ++m.continuations;
    progress(&m);
    CHECK(m.quarantine && waiting->state == AK820_PH_WAITING && m.q.slots.count == 3);
    unpin(&m, waiting);
    CHECK(m.quarantine && waiting->state == AK820_PH_RETIRED && waiting->pins == UINT8_MAX - 1 && m.q.slots.count == 2);
    for (unsigned i = 0; i < UINT8_MAX - 1; ++i) unpin(&m, waiting);
    CHECK(m.quarantine && m.q.slots.count == 1 && !m.dispatches && !m.effects && !m.continuations);
    scope_close(&m, inner); CHECK(m.quarantine);
    scope_close(&m, outer);
    CHECK(!m.quarantine && !m.q.slots.count && !m.dispatches && !m.effects && !m.continuations);
    release(&m, 0); CHECK(!m.blocked && !m.normal_ups);
    puts("PASS: guarded pin limit revokes and drains only after legitimate unpin");
}
static void claim_fault(unsigned injection) {
    model m; scope *outer, *inner; init(&m); m.cleanup = cleanup_ok;
    CHECK(press(&m, 0) && scope_open(&m, &outer));
    CHECK(enqueue(&m, 0x1111) && scope_claim(&m, outer));
    CHECK(enqueue(&m, 0x2222) && scope_open(&m, &inner));
    ak820_ph_slot *original = outer->claim;
    if (injection == 0) {
        ak820_ph_slot *sentinel = original;
        CHECK(ak820_ph_queue_claim(NULL, &sentinel) == AK820_PH_QUEUE_INVALID && sentinel == original);
    }
    if (injection == 7) { m.q.slots.slots[2].state = AK820_PH_CLAIMED; m.q.slots.slots[2].pins = 1; }
    m.claim_injection = injection;
    CHECK(guarded_claim(&m, inner, injection ? &m.q : NULL) == AK820_PH_QUEUE_INVALID);
    CHECK(m.quarantine && m.invariant_failed && outer->revoked && inner->revoked);
    CHECK(outer->claim == original && original->state == AK820_PH_CLAIMED && original->pins == 1 && !inner->claim);
    CHECK(m.q.slots.count == 2 && !m.dispatches && !m.effects && m.cleanup_attempts == 1);
    progress(&m); scope_close(&m, inner); scope_close(&m, outer);
    CHECK(m.quarantine && inner->active && outer->active && outer->claim == original && original->pins == 1);
    CHECK(m.q.slots.count == 2 && !m.dispatches && !m.effects);
    puts("PASS: invalid claim latches fault without using stale output or traversing queue");
}
static void claim_duplicate(void) {
    model m; scope *s; init(&m); m.cleanup = cleanup_ok;
    CHECK(scope_open(&m, &s) && enqueue(&m, 1) && scope_claim(&m, s));
    ak820_ph_slot *held = s->claim;
    CHECK(guarded_claim(&m, s, &m.q) == AK820_PH_QUEUE_INVALID);
    CHECK(m.quarantine && m.invariant_failed && s->revoked && s->claim == held && held->pins == 1);
    scope_close(&m, s); CHECK(s->active && m.quarantine && held->pins == 1);
    puts("PASS: second claim faults and preserves ownership");
}
static void finish_fault(void) {
    model m; scope *s; init(&m); m.cleanup = cleanup_ok;
    CHECK(scope_open(&m, &s) && enqueue(&m, 1) && scope_claim(&m, s));
    ak820_ph_slot *held = s->claim;
    m.inject_finish_failure = true;
    scope_close(&m, s);
    CHECK(m.quarantine && m.invariant_failed && s->active && s->revoked && s->claim == held);
    CHECK(held->state == AK820_PH_CLAIMED && held->pins == 1 && m.q.slots.count == 1);
    m.inject_finish_failure = false;
    scope_close(&m, s); progress(&m);
    CHECK(m.quarantine && s->active && s->claim == held && held->pins == 1 && m.q.slots.count == 1);
    puts("PASS: failed finish latches fault without retry or double release");
}
/* Local pointers expire on return; the model and its owned scopes do not. */
static void faulting_caller(model *m, bool fail_finish) {
    scope *outer, *inner;
    CHECK(scope_open(m, &outer) && enqueue(m, 0x1234) && scope_claim(m, outer));
    CHECK(scope_open(m, &inner));
    if (fail_finish) {
        m->inject_finish_failure = true;
        scope_close(m, outer);
        m->inject_finish_failure = false;
    } else {
        CHECK(guarded_claim(m, inner, NULL) == AK820_PH_QUEUE_INVALID);
    }
    scope_close(m, inner);
    scope_close(m, outer);
}
static void scope_lifetime(bool fail_finish) {
    model m; scope *denied; init(&m); m.cleanup = cleanup_ok;
    faulting_caller(&m, fail_finish);
    CHECK(m.quarantine && m.invariant_failed);
    CHECK(m.scopes[0] == &m.owned_scopes[0] && m.scopes[1] == &m.owned_scopes[1]);
    CHECK(m.scopes[0]->active && m.scopes[0]->revoked && m.scopes[1]->active && m.scopes[1]->revoked);
    CHECK(ak820_ph_frame_get(m.scopes[0]->frame) && ak820_ph_frame_get(m.scopes[1]->frame));
    ak820_ph_slot *held = m.scopes[0]->claim;
    CHECK(held && held->state == AK820_PH_CLAIMED && held->pins == 1 && m.q.slots.count == 1);
    for (unsigned i = 0; i < 3; ++i) { cancel(&m); progress(&m); }
    CHECK(!scope_open(&m, &denied) && !denied && !enqueue(&m, 0x4567) && !take_output(&m, 0, 0));
    CHECK(m.quarantine && m.scopes[0]->claim == held && held->pins == 1 && m.q.slots.count == 1);
    CHECK(!m.dispatches && !m.effects && !m.continuations);
    puts("PASS: model-owned scopes survive faulting caller return without replay or release");
}
int main(int argc, char **argv) {
    if (argc == 1 || !strcmp(argv[1], "claimed")) claimed_and_pinned_waiting();
    if (argc == 1 || !strcmp(argv[1], "saturated")) saturated_waiting();
    if (argc == 1 || !strcmp(argv[1], "failure")) failed_cleanup();
    if (argc == 1 || !strcmp(argv[1], "partial")) partial_cleanup_failure();
    if (argc == 1 || !strcmp(argv[1], "release")) held_release_after_exit();
    if (argc == 1 || !strcmp(argv[1], "scope_failure")) scope_allocation_failure();
    if (argc == 1 || !strcmp(argv[1], "scope_table")) scope_table_failure();
    if (argc == 1 || !strcmp(argv[1], "nested")) nested_revocation_no_replay();
    if (argc == 1 || !strcmp(argv[1], "claim_idle")) claim_idle();
    if (argc == 1 || !strcmp(argv[1], "claim_saturation")) claim_saturation();
    if (argc > 1 && !strncmp(argv[1], "claim_fault", 11)) claim_fault((unsigned)strtoul(argv[1] + 11, NULL, 10));
    if (argc > 1 && !strcmp(argv[1], "claim_duplicate")) claim_duplicate();
    if (argc > 1 && !strcmp(argv[1], "finish_fault")) finish_fault();
    if (argc > 1 && !strcmp(argv[1], "lifetime_claim")) scope_lifetime(false);
    if (argc > 1 && !strcmp(argv[1], "lifetime_finish")) scope_lifetime(true);
    return 0;
}
