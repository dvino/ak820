// SPDX-License-Identifier: GPL-2.0-or-later
/* Instrumented callbacks for the source-derived producer ABI probe only. */
#include "action.h"
#include "matrix.h"
#include "debug.h"
#include "ak820_ph_frame.h"

__xdata __at (0x0e00) volatile uint8_t result[64];
debug_config_t debug_config;
static uint16_t clock_value;
static uint8_t nesting, sequence;
static bool failed, matrix_pressed;

void probe_matrix(void);
#ifdef TEST_OWNED
void probe_encoder(uint8_t index, bool clockwise) __reentrant;
#else
void probe_encoder(uint8_t index, bool clockwise);
#endif
uint16_t timer_read(void) { return ++clock_value; }
bool matrix_can_read(void) { return PROBE_CASE != 0 && PROBE_CASE != 9; }
uint8_t matrix_scan(void) { return 0; }
matrix_row_t matrix_get_row(uint8_t row) { return row == 0 && matrix_pressed ? 2 : 0; }
void matrix_scan_perf_task(void) {}
void vial_unlock_task(void) {}
bool should_process_keypress(void) { return true; }
void matrix_print(void) {}
void switch_events(uint8_t row, uint8_t col, bool pressed) { (void)row; (void)col; (void)pressed; }
void wait_ms(uint16_t ms) { (void)ms; ++result[2]; result[4 + sequence++] = 0x80; }

void observe(const keyevent_t __xdata *event) __reentrant {
    uint8_t entry = result[0]++;
    const uint8_t __xdata *bytes = (const uint8_t __xdata *)event;
    for (uint8_t i = 0; i < 6; ++i) result[16 + 6 * entry + i] = bytes[i];
    result[4 + sequence++] = event->pressed ? 0x11 : 0x10;
    if (nesting) {
        nesting = 0;
#if PROBE_CASE == 1
        probe_encoder(2, false);
#elif PROBE_CASE == 2
        probe_matrix();
#elif PROBE_CASE == 3 || PROBE_CASE == 5
        probe_encoder(2, false);
#endif
        for (uint8_t i = 0; i < 6; ++i) result[48 + i] = bytes[i];
    }
}

/* The non-owned control reaches the real extracted adapter and this mocked
 * by-value core. This is not the firmware action_exec implementation. */
void action_exec(keyevent_t event) { observe(&event); }

#ifdef TEST_OWNED
void test_failure(void) { ++result[1]; failed = true; }
bool test_dispatch(ak820_ph_frame_handle_t h) __reentrant {
    ak820_ph_frame_t __xdata *frame = ak820_ph_frame_get(h);
#ifdef TEST_UNSAFE_ADAPTER
    ak820_action_exec(&frame->event);
#else
    observe(&frame->event);
#endif
    return !failed;
}
void test_emit(uint8_t row, uint8_t col, bool pressed, keyevent_type_t type) __reentrant {
    ak820_ph_frame_handle_t h = ak820_ph_frame_reserve();
    if (!h) { test_failure(); return; }
    ak820_ph_frame_t __xdata *frame = ak820_ph_frame_get(h);
    frame->event.key.row = row;
    frame->event.key.col = col;
    frame->event.time = timer_read();
    frame->event.type = type;
    frame->event.pressed = pressed;
    test_dispatch(h);
    ak820_ph_frame_release(h);
}
#endif

int main(void) {
    for (uint8_t i = 0; i < 64; ++i) result[i] = 0;
    clock_value = 100;
    nesting = (PROBE_CASE == 1 || PROBE_CASE == 2 || PROBE_CASE == 3 || PROBE_CASE == 5);
    sequence = 0;
    failed = false;
    matrix_pressed = true;
#if PROBE_CASE == 10 || PROBE_CASE == 11
    probe_matrix();
#    if PROBE_CASE == 11
    result[3] = result[0];
    for (uint8_t i = 0; i < 6; ++i) result[56 + i] = result[16 + i];
    for (uint8_t i = 0; i < 56; ++i) if (i != 3) result[i] = 0;
#    else
    for (uint8_t i = 0; i < 64; ++i) result[i] = 0;
#    endif
    clock_value = 100;
    sequence = 0;
    matrix_pressed = false;
#    if PROBE_CASE == 11
    ak820_ph_frame_handle_t a = ak820_ph_frame_reserve();
    ak820_ph_frame_handle_t b = ak820_ph_frame_reserve();
    if (!a || !b) { result[62] = 1; goto done; }
    probe_matrix(); /* The release cannot reserve, but matrix_previous advances. */
    result[54] = result[0]; result[55] = result[1];
    if (!ak820_ph_frame_release(a) || !ak820_ph_frame_release(b)) result[62] = 2;
    probe_matrix(); /* Unchanged scan: tick, not a release retry. */
#    else
    probe_matrix();
#    endif
#elif PROBE_CASE == 4 || PROBE_CASE == 9
    ak820_ph_frame_handle_t a = ak820_ph_frame_reserve();
    ak820_ph_frame_handle_t b = ak820_ph_frame_reserve();
    if (!a || !b) { result[62] = 1; goto done; }
    probe_matrix();
    if (!ak820_ph_frame_release(a) || !ak820_ph_frame_release(b)) result[62] = 2;
#elif PROBE_CASE == 0 || PROBE_CASE == 1 || PROBE_CASE == 6
    probe_matrix();
#else
    probe_encoder(1, PROBE_CASE != 8);
#endif
#if PROBE_CASE == 4 || PROBE_CASE == 9 || PROBE_CASE == 11
 done:
#endif
    result[63] = 0xa5;
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
    return 0;
}
