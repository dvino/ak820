// SPDX-License-Identifier: GPL-2.0-or-later
#include <stdio.h>
#include "ak820_ph_slots.h"
#define CHECK(x) do { if (!(x)) { fprintf(stderr, "check failed: %s at %d\n", #x, __LINE__); return 1; } } while (0)

int main(void) {
    ak820_ph_slots pool;
    ak820_ph_slot_event e = {.source=5,.time=10,.observed=0x2204,.committed=0x2204,.pressed=1}, snap;
    uint8_t state;
    ak820_ph_slots_init(&pool);
    CHECK(ak820_ph_slots_enqueue(&pool, &e));
    e.time=20; e.pressed=0;
    CHECK(ak820_ph_slots_enqueue(&pool, &e));
    e.time=30; e.pressed=1; e.observed=e.committed=0x4104;
    CHECK(ak820_ph_slots_enqueue(&pool, &e));
    CHECK(!ak820_ph_slots_enqueue(&pool, &e));
    ak820_ph_slot *first=ak820_ph_slots_claim(&pool);
    CHECK(first && first->event.time == 10);
    CHECK(ak820_ph_slots_snapshot(&pool,0,&snap,&state));
    CHECK(state == AK820_PH_CLAIMED && snap.time == 10);
    ak820_ph_slot *view=ak820_ph_slots_pin_at(&pool,1);
    CHECK(view && view->state == AK820_PH_WAITING && view->event.time == 20);
    ak820_ph_slot *second=ak820_ph_slots_claim(&pool);
    CHECK(second == view && second != first && second->event.time == 20);
    CHECK(ak820_ph_slot_finish(&pool,second));
    CHECK(view->state == AK820_PH_RETIRED && view->pins == 1);
    CHECK(!ak820_ph_slots_enqueue(&pool,&e));
    CHECK(!ak820_ph_slot_pin(view));
    CHECK(ak820_ph_slot_unpin(&pool,view));
    e.time=40; e.committed=0x3304;
    CHECK(ak820_ph_slots_enqueue(&pool,&e)); /* Interior hole is reused at the tail. */
    CHECK(first->state == AK820_PH_CLAIMED && first->event.time == 10);
    CHECK(ak820_ph_slots_snapshot(&pool,1,&snap,&state) && snap.time == 30);
    CHECK(ak820_ph_slots_snapshot(&pool,2,&snap,&state) && snap.time == 40);
    ak820_ph_slot *third=ak820_ph_slots_claim(&pool);
    CHECK(third && third->event.time == 30 && third != first);
    CHECK(ak820_ph_slot_pin(third)); /* Keep this reference when the claim is released. */
    CHECK(ak820_ph_slot_unclaim(third)); /* Caller stops pumping on an unresolved item. */
    CHECK(ak820_ph_slots_claim(&pool) == third);
    CHECK(ak820_ph_slot_unpin(&pool,third));
    CHECK(ak820_ph_slot_finish(&pool,third));
    ak820_ph_slot *fourth=ak820_ph_slots_claim(&pool);
    CHECK(fourth && fourth->event.time == 40 && fourth->event.committed == 0x3304);
    CHECK(ak820_ph_slot_finish(&pool,fourth));
    CHECK(!ak820_ph_slots_claim(&pool));
    CHECK(ak820_ph_slot_finish(&pool,first));
    CHECK(pool.count == 0 && !ak820_ph_slots_snapshot(&pool,0,&snap,&state));
    CHECK(ak820_ph_slots_enqueue(&pool,&e));
    ak820_ph_slot *bounded=ak820_ph_slots_claim(&pool);
    CHECK(bounded);
    for (unsigned i=0; i<254; ++i) CHECK(ak820_ph_slot_pin(bounded));
    CHECK(bounded->pins == UINT8_MAX && !ak820_ph_slot_pin(bounded));
    for (unsigned i=0; i<254; ++i) CHECK(ak820_ph_slot_unpin(&pool,bounded));
    CHECK(ak820_ph_slot_finish(&pool,bounded) && pool.count == 0);
    e.time=10; CHECK(ak820_ph_slots_enqueue(&pool,&e));
    e.time=20; CHECK(ak820_ph_slots_enqueue(&pool,&e));
    e.time=30; CHECK(ak820_ph_slots_enqueue(&pool,&e));
    first=ak820_ph_slots_claim(&pool);
    view=ak820_ph_slots_pin_at(&pool,1);
    CHECK(first && view && view->event.time == 20);
    CHECK(ak820_ph_slot_finish(&pool,first));
    CHECK(ak820_ph_slots_snapshot(&pool,0,&snap,&state) && snap.time == 20);
    second=ak820_ph_slots_claim(&pool);
    CHECK(second == view && ak820_ph_slot_finish(&pool,second));
    e.time=40; CHECK(ak820_ph_slots_enqueue(&pool,&e));
    CHECK(view->state == AK820_PH_RETIRED && view->event.time == 20);
    CHECK(ak820_ph_slot_unpin(&pool,view)); /* The old reference expires here. */
    third=ak820_ph_slots_claim(&pool);
    CHECK(third && third->event.time == 30 && ak820_ph_slot_finish(&pool,third));
    fourth=ak820_ph_slots_claim(&pool);
    CHECK(fourth && fourth->event.time == 40 && ak820_ph_slot_finish(&pool,fourth));
    CHECK(pool.count == 0);
    puts("PASS: nested claims, snapshots, pinned retirement, hole reuse and pin saturation");
    return 0;
}
