// SPDX-License-Identifier: GPL-2.0-or-later
#include "timer.h"
#include "ch555.h"
#pragma nooverlay

volatile uint32_t timer_count;

static void timer_reload(void) {
    // Match the OEM clock divider. 32 MHz / 12 / 1000 -> 1 ms nominal.
    const uint16_t reload = (uint16_t)(0u - (F_CPU / 12u / 1000u));
    TL0 = (uint8_t)reload;
    TH0 = (uint8_t)(reload >> 8);
}

void timer_init(void) {
    EA = 0;
    timer_count = 0;
    T2MOD &= (uint8_t)~bT0_CLK;
    TMOD = (TMOD & 0xF0) | 0x01;
    timer_reload();
    TF0 = 0;
    ET0 = 1;
    TR0 = 1;
    EA = 1;
}

// The immutable OEM wrapper at18A4 saves all registers and executes RETI.
// This callback MUST end in RET, not an SDCC __interrupt epilogue.
void ak820_timer_irq(void) {
    timer_reload();
    ++timer_count;
}

void timer_clear(void) { __critical { timer_count = 0; } }
uint32_t timer_read32(void) {
    uint32_t value;
    __critical { value = timer_count; }
    return value;
}
uint16_t timer_read(void) { return (uint16_t)timer_read32(); }
uint16_t timer_elapsed(uint16_t last) { return (uint16_t)(timer_read() - last); }
uint32_t timer_elapsed32(uint32_t last) { return timer_read32() - last; }

