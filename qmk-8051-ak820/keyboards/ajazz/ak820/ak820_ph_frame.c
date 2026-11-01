#include "ak820_ph_frame.h"

#ifdef AK820_PH_FRAME_ENABLE
/* Single-threaded synchronous entry only; this pool is not IRQ atomic. */
static __xdata ak820_ph_frame_t frames[AK820_PH_FRAME_CAPACITY];
static __xdata uint16_t generations[AK820_PH_FRAME_CAPACITY];
static __xdata uint8_t references[AK820_PH_FRAME_CAPACITY];

ak820_ph_frame_handle_t ak820_ph_frame_reserve(void) AK820_PH_FRAME_REENTRANT {
    for (uint16_t i = 0; i < AK820_PH_FRAME_CAPACITY; ++i) {
        if (!references[i] && generations[i] != UINT16_MAX) {
            ++generations[i];
            references[i] = 1;
            frames[i].event.key.row = 0;
            frames[i].event.key.col = 0;
            frames[i].event.time = 0;
            frames[i].event.type = TICK_EVENT;
            frames[i].event.pressed = false;
            frames[i].keycode = 0;
            return ((uint32_t)generations[i] << 8) | i;
        }
    }
    return 0;
}

static bool valid(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT {
    uint8_t index = (uint8_t)handle;
    return !(handle >> 24) && index < AK820_PH_FRAME_CAPACITY && references[index] &&
           generations[index] == (uint16_t)(handle >> 8);
}

bool ak820_ph_frame_pin(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT {
    uint8_t index = (uint8_t)handle;
    if (!valid(handle) || references[index] == UINT8_MAX) return false;
    ++references[index];
    return true;
}

bool ak820_ph_frame_release(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT {
    if (!valid(handle)) return false;
    --references[(uint8_t)handle];
    return true;
}

ak820_ph_frame_t __xdata *ak820_ph_frame_get(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT {
    if (!valid(handle)) return 0;
    return &frames[(uint8_t)handle];
}
#ifdef AK820_PH_ACTION_SEAM
/* Reservation precedes timer_read and all action callbacks. */
static __xdata ak820_ph_action_context_t action_contexts[AK820_PH_FRAME_CAPACITY];
static __xdata uint8_t action_active[AK820_PH_FRAME_CAPACITY];
bool ak820_ph_action_run(uint8_t row, uint8_t col, bool pressed, keyevent_type_t type) AK820_PH_FRAME_REENTRANT {
    for (uint16_t i = 0; i < AK820_PH_FRAME_CAPACITY; ++i) {
        if (!action_active[i]) {
            action_active[i] = 1;
            action_contexts[i].event.key.row = row;
            action_contexts[i].event.key.col = col;
            action_contexts[i].event.time = timer_read();
            action_contexts[i].event.type = type;
            action_contexts[i].event.pressed = pressed;
            ak820_ph_action_continue(&action_contexts[i]);
            action_active[i] = 0;
            return true;
        }
    }
    return false;
}
#endif
#ifdef AK820_PH_SCOPED_ENABLE
/* Only the dynamic call owns a slot; no operation exports ownership. */
static __xdata ak820_ph_frame_t scoped_frames[AK820_PH_FRAME_CAPACITY];
static __xdata uint8_t scoped_active[AK820_PH_FRAME_CAPACITY];

bool ak820_ph_scoped_run(uint16_t keycode, bool pressed, bool tap) AK820_PH_FRAME_REENTRANT {
    for (uint16_t i = 0; i < AK820_PH_FRAME_CAPACITY; ++i) {
        if (!scoped_active[i]) {
            scoped_active[i] = 1;
            scoped_frames[i].event.key.row = 0;
            scoped_frames[i].event.key.col = 0;
            scoped_frames[i].event.time = 0;
            scoped_frames[i].event.type = TICK_EVENT;
            scoped_frames[i].event.pressed = pressed;
            scoped_frames[i].keycode = keycode;
            bool ok = ak820_ph_scoped_consume(&scoped_frames[i], tap);
            scoped_active[i] = 0;
            return ok;
        }
    }
    return false;
}
#endif
#endif
