// SPDX-License-Identifier: GPL-2.0-or-later
#include <assert.h>
#include "ak820_ph_slots.h"
int main(void) {
    ak820_ph_slots pool;
    ak820_ph_slot_event event = {0};
    ak820_ph_slots_init(&pool);
    for (unsigned i = 0; i < AK820_PH_SLOT_CAPACITY; ++i) {
        event.time = i;
        assert(ak820_ph_slots_enqueue(&pool, &event));
    }
    assert(!ak820_ph_slots_enqueue(&pool, &event));
    for (unsigned i = 0; i < AK820_PH_SLOT_CAPACITY; ++i) {
        ak820_ph_slot *slot = ak820_ph_slots_claim(&pool);
        assert(slot && slot->event.time == i);
        assert(ak820_ph_slot_finish(&pool, slot));
    }
    assert(!pool.count && !ak820_ph_slots_claim(&pool));
    return 0;
}
