#include "ak820_ph_frame.h"
#include <assert.h>
#include <stdio.h>

int main(void) {
    ak820_ph_frame_handle_t a = ak820_ph_frame_reserve();
    ak820_ph_frame_handle_t b = ak820_ph_frame_reserve();
    assert(a && b && a != b && !ak820_ph_frame_reserve());
    ak820_ph_frame_t *outer = ak820_ph_frame_get(a);
    ak820_ph_frame_t *inner = ak820_ph_frame_get(b);
    assert(outer && inner && outer != inner);
    outer->keycode = 0x7700;
    outer->event.time = 3;
    inner->keycode = 0x7701;
    inner->event.time = 5;
    assert(ak820_ph_frame_pin(a));
    assert(!ak820_ph_frame_reserve());
    assert(outer->keycode == 0x7700 && outer->event.time == 3);
    assert(inner->keycode == 0x7701 && inner->event.time == 5);
    assert(ak820_ph_frame_release(a) && ak820_ph_frame_get(a) == outer);
    assert(ak820_ph_frame_release(a) && !ak820_ph_frame_get(a));
    assert(!ak820_ph_frame_release(a) && !ak820_ph_frame_pin(a));
    ak820_ph_frame_handle_t replacement = ak820_ph_frame_reserve();
    assert(replacement && replacement != a && !ak820_ph_frame_get(a));
    assert(!ak820_ph_frame_pin(a) && !ak820_ph_frame_release(a));
    assert(ak820_ph_frame_get(replacement)->keycode == 0);
    assert(!ak820_ph_frame_get(replacement | 0x01000000UL));
    assert(!ak820_ph_frame_get(0) && !ak820_ph_frame_pin(0));
    for (unsigned i = 1; i < 255; ++i) assert(ak820_ph_frame_pin(replacement));
    assert(!ak820_ph_frame_pin(replacement));
    for (unsigned i = 0; i < 255; ++i) assert(ak820_ph_frame_release(replacement));
    assert(ak820_ph_frame_release(b));
    unsigned retired = 0;
    while ((replacement = ak820_ph_frame_reserve())) {
        ++retired;
        assert(ak820_ph_frame_release(replacement));
    }
    assert(retired > 130000 && !ak820_ph_frame_reserve());
    printf("PASS: nested ownership, stale handles, saturation and generation retirement (%u)\n", retired);
    return 0;
}
