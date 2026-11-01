// SPDX-License-Identifier: GPL-2.0-or-later
/* Ownership-only adapter: no tapping transitions or real output callbacks. */
#include <stdio.h>
#include "ak820_ph_slots.h"
int main(void) {
    ak820_ph_slots pool;
    ak820_ph_slot_event e={.source=1,.time=110,.pressed=1};
    ak820_ph_slots_init(&pool);
    if (!ak820_ph_slots_enqueue(&pool,&e)) return 1;
    e.time=120; e.pressed=0;
    if (!ak820_ph_slots_enqueue(&pool,&e)) return 2;
    ak820_ph_slot *outer=ak820_ph_slots_claim(&pool);
    if (!outer || !outer->event.pressed) return 3;
    puts("callback-before");
    puts("generated-down-begin");
    ak820_ph_slot *nested=ak820_ph_slots_claim(&pool);
    if (!nested || nested==outer || nested->event.pressed) return 4;
    puts("queued-release");
    if (!ak820_ph_slot_finish(&pool,nested)) return 5;
    puts("generated-between-edges");
    puts("generated-up-end");
    puts("callback-after");
    if (!ak820_ph_slot_finish(&pool,outer) || pool.count) return 6;
    return 0;
}
