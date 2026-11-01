#pragma once

#ifdef AK820_PH_VIAL_ENABLE
#ifndef AK820_PH_FRAME_ENABLE
#    error AK820_PH_VIAL_ENABLE requires AK820_PH_FRAME_ENABLE
#endif
#include "ak820_ph_frame.h"
#if defined(AK820_PH_FRAME_CAPACITY) && AK820_PH_FRAME_CAPACITY < 2
#    error AK820_PH_VIAL_ENABLE requires at least two frames
#endif

/* False stops the operation; caller must handle possible partial output. */
bool ak820_ph_vial_down(uint16_t keycode) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_vial_up(uint16_t keycode) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_vial_tap(uint16_t keycode) AK820_PH_FRAME_REENTRANT;

/* Hooks are synchronous. Pin to retain a frame beyond the call; never release
 * the producer's reference. False may mean output was partially performed.
 * Dispatch must use the frame keycode; this seam does not set Vial's global. */
bool ak820_ph_vial_basic(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_vial_dispatch(ak820_ph_frame_handle_t handle) AK820_PH_FRAME_REENTRANT;
/* The integration must implement the existing QS_tap_code_delay wait.
 * The current frame pool can permanently exhaust and must not be wired. */
bool ak820_ph_vial_wait(void) AK820_PH_FRAME_REENTRANT;

#ifdef AK820_PH_SCOPED_ENABLE
/* Separate unwired path. Hooks and their callees must not retain a frame or
 * alias; queue work must copy it synchronously. No IRQ access is permitted.
 * Failure requires external cancellation; no output cleanup is provided. */
bool ak820_ph_scoped_vial_down(uint16_t keycode) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_scoped_vial_up(uint16_t keycode) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_scoped_vial_tap(uint16_t keycode) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_scoped_vial_basic(const ak820_ph_frame_t __xdata *frame) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_scoped_vial_dispatch(const ak820_ph_frame_t __xdata *frame) AK820_PH_FRAME_REENTRANT;
bool ak820_ph_scoped_vial_wait(void) AK820_PH_FRAME_REENTRANT;
#endif
#endif
