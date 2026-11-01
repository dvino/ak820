#pragma once

#ifdef AK820_PH_FRAME_ENABLE
#include "action.h"
#include <stdint.h>

#ifndef AK820_PH_FRAME_CAPACITY
#    error AK820_PH_FRAME_CAPACITY must be explicitly supplied
#endif
#if AK820_PH_FRAME_CAPACITY < 1 || AK820_PH_FRAME_CAPACITY > 255
#    error AK820_PH_FRAME_CAPACITY must be between 1 and 255
#endif

#ifdef __SDCC_mcs51
#    define AK820_PH_FRAME_REENTRANT __reentrant
#else
#    define AK820_PH_FRAME_REENTRANT
#endif

typedef uint32_t ak820_ph_frame_handle_t;
typedef struct {
    keyevent_t event;
    uint16_t keycode;
} ak820_ph_frame_t;

/* Zero is failure; slots retire at generation 65535 rather than reuse a handle.
 * A borrowed pointer is valid only while its reference is held. Each successful
 * pin adds one reference; callers must release only their own references. */
ak820_ph_frame_handle_t ak820_ph_frame_reserve(void) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_frame_pin(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_frame_release(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT;
ak820_ph_frame_t __xdata *ak820_ph_frame_get(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT;

#ifdef AK820_PH_ACTION_SEAM
/* Foreground-only, synchronous, no escape; false means no free context.
 * No cancellation or downstream callback safety is provided. */
bool ak820_ph_action_run(uint8_t row, uint8_t col, bool pressed, keyevent_type_t type) AK820_PH_FRAME_REENTRANT;
#endif

#ifdef AK820_PH_SCOPED_ENABLE
/* Private, foreground-only staging contract: the sole consumer must be audited
 * with every transitive callback. No pointer or alias may escape its call, be
 * retained by an IRQ, or survive reuse. C cannot detect an escaped pointer.
 * This pool is separate from the legacy handle pool and is not cancellation. */
bool ak820_ph_scoped_run(uint16_t keycode, bool pressed, bool tap) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_scoped_consume(ak820_ph_frame_t __xdata *frame, bool tap) AK820_PH_FRAME_REENTRANT;
#endif
#endif
