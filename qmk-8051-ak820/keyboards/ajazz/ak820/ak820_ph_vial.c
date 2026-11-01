#include "ak820_ph_vial.h"

#ifdef AK820_PH_VIAL_ENABLE
#include "vial.h"

static bool event(uint16_t keycode, bool pressed) AK820_PH_FRAME_REENTRANT {
#ifdef AK820_COMPACT_TAPPING
    if (keycode >= QK_MOD_TAP && keycode <= QK_LAYER_TAP_MAX) {
        keycode = (uint8_t)keycode;
        if (keycode <= KC_TRANSPARENT) return true;
    }
#endif
    ak820_ph_frame_handle_t handle = ak820_ph_frame_reserve();
    if (!handle) return false;
    ak820_ph_frame_t __xdata *frame = ak820_ph_frame_get(handle);
    frame->keycode = keycode;
    frame->event.pressed = pressed;
    bool ok;
    if (keycode <= QK_MODS_MAX) {
        ok = ak820_ph_vial_basic(handle);
    } else {
        frame->event.type = KEY_EVENT;
        frame->event.key.row = VIAL_MATRIX_MAGIC;
        frame->event.key.col = VIAL_MATRIX_MAGIC;
        frame->event.time = timer_read() | 1;
        ok = ak820_ph_vial_dispatch(handle);
    }
    if (!ak820_ph_frame_release(handle)) return false;
    return ok;
}

bool ak820_ph_vial_down(uint16_t keycode) AK820_PH_FRAME_REENTRANT {
    return event(keycode, true);
}

bool ak820_ph_vial_up(uint16_t keycode) AK820_PH_FRAME_REENTRANT {
    return event(keycode, false);
}

bool ak820_ph_vial_tap(uint16_t keycode) AK820_PH_FRAME_REENTRANT {
    ak820_ph_frame_handle_t handle = ak820_ph_frame_reserve();
    if (!handle) return false;
    ak820_ph_frame_t __xdata *frame = ak820_ph_frame_get(handle);
    frame->keycode = keycode;
    bool ok = ak820_ph_vial_down(frame->keycode);
    if (ok) ok = ak820_ph_vial_wait();
    if (ok) ok = ak820_ph_vial_up(frame->keycode);
    if (!ak820_ph_frame_release(handle)) return false;
    return ok;
}

#ifdef AK820_PH_SCOPED_ENABLE
bool ak820_ph_scoped_consume(ak820_ph_frame_t __xdata *frame, bool tap) AK820_PH_FRAME_REENTRANT {
    if (tap) {
        bool ok = ak820_ph_scoped_vial_down(frame->keycode);
        if (ok) ok = ak820_ph_scoped_vial_wait();
        if (ok) ok = ak820_ph_scoped_vial_up(frame->keycode);
        return ok;
    }
#ifdef AK820_COMPACT_TAPPING
    if (frame->keycode >= QK_MOD_TAP && frame->keycode <= QK_LAYER_TAP_MAX) {
        frame->keycode = (uint8_t)frame->keycode;
        if (frame->keycode <= KC_TRANSPARENT) return true;
    }
#endif
    if (frame->keycode <= QK_MODS_MAX) return ak820_ph_scoped_vial_basic(frame);
    frame->event.type = KEY_EVENT;
    frame->event.key.row = VIAL_MATRIX_MAGIC;
    frame->event.key.col = VIAL_MATRIX_MAGIC;
    frame->event.time = timer_read() | 1;
    return ak820_ph_scoped_vial_dispatch(frame);
}

bool ak820_ph_scoped_vial_down(uint16_t keycode) AK820_PH_FRAME_REENTRANT {
    return ak820_ph_scoped_run(keycode, true, false);
}
bool ak820_ph_scoped_vial_up(uint16_t keycode) AK820_PH_FRAME_REENTRANT {
    return ak820_ph_scoped_run(keycode, false, false);
}
bool ak820_ph_scoped_vial_tap(uint16_t keycode) AK820_PH_FRAME_REENTRANT {
    return ak820_ph_scoped_run(keycode, false, true);
}
#endif
#endif
