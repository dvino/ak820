// SPDX-License-Identifier: GPL-2.0-or-later
/* Synthetic consumer; no action callbacks, cancellation or IRQs. */
#include "ak820_ph_frame.h"
__xdata __at (0x0f00) volatile uint8_t result[2];
static uint8_t depth, failures, seen;
static uint16_t clock_value;
uint16_t timer_read(void) { return ++clock_value; }
void ak820_ph_action_continue(ak820_ph_action_context_t __xdata *ctx) __reentrant {
    ++seen;
    if (!depth) {
        if (ctx->event.key.row != 4 || ctx->event.key.col != 5 || ctx->event.time != clock_value || !ctx->event.pressed || ctx->event.type != KEY_EVENT) ++failures;
        ctx->record.event.key.row = 42;
        depth = 1;
        if (!ak820_ph_action_run(7, 8, false, ENCODER_CW_EVENT)) ++failures;
        depth = 0;
        if (ctx->event.key.row != 4 || ctx->event.key.col != 5 || ctx->event.time != clock_value - 1 || ctx->record.event.key.row != 42) ++failures;
    } else {
        if (ctx->event.key.row != 7 || ctx->event.key.col != 8 || ctx->event.pressed || ctx->event.type != ENCODER_CW_EVENT) ++failures;
        if (ak820_ph_action_run(9, 0, true, KEY_EVENT)) ++failures;
    }
}
void main(void) {
    for (uint8_t i = 0; i < 10; ++i) if (!ak820_ph_action_run(4, 5, true, KEY_EVENT)) ++failures;
    result[0] = failures ? 0x5a : 0xa5;
    result[1] = seen;
    __asm
        .globl _probe_done
    _probe_done:
        sjmp _probe_done
    __endasm;
}
