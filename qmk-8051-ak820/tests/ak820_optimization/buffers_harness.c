/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "report.h"
#define dprint(...) ((void)0)
static uint8_t real_mods, weak_mods;
static report_keyboard_t report;
#define keyboard_report (&report)
static unsigned sent;
static report_keyboard_t sent_report;
void host_keyboard_send(report_keyboard_t *value) {
    ++sent;
    sent_report = *value;
}
typedef uint8_t matrix_row_t;
typedef uint16_t fast_timer_t;
_Static_assert(MATRIX_COLS <= 8, "This harness models the configured byte rows");
static bool debouncing, rc4_debouncing;
static fast_timer_t debouncing_time, rc4_debouncing_time, clock_value;
fast_timer_t timer_read_fast(void) { return clock_value; }
fast_timer_t timer_elapsed_fast(fast_timer_t start) { return (fast_timer_t)(clock_value - start); }
/* SOURCES */
static void compare_report(void) {
    sent = 0;
    rc4_send_keyboard_report();
    unsigned expected_count = sent;
    report_keyboard_t expected_report = sent_report;
    sent = 0;
    send_keyboard_report();
    assert(sent == expected_count);
    if (sent) assert(memcmp(&sent_report, &expected_report, sizeof(sent_report)) == 0);
    /* Both implementations suppress an immediate repeated report. */
    sent = 0;
    rc4_send_keyboard_report();
    send_keyboard_report();
    assert(sent == 0);
}
static uint32_t prng = 0x28511000;
static uint32_t random_word(void) {
    prng ^= prng << 13;
    prng ^= prng >> 17;
    prng ^= prng << 5;
    return prng;
}
int main(void) {
    compare_report();
    for (unsigned byte = 0; byte < sizeof(report.raw); ++byte)
        for (unsigned value = 0; value <= UINT8_MAX; ++value) {
            report.raw[byte] = value;
            compare_report();
        }
    for (unsigned real = 0; real <= UINT8_MAX; ++real)
        for (unsigned weak = 0; weak <= UINT8_MAX; ++weak) {
            real_mods = real; weak_mods = weak;
            compare_report();
        }
    for (unsigned event = 0; event < 10000; ++event) {
        for (unsigned byte = 0; byte < sizeof(report.raw); ++byte) report.raw[byte] = random_word();
        real_mods = random_word(); weak_mods = random_word();
        compare_report();
    }
    matrix_row_t raw[UINT8_MAX], actual[UINT8_MAX], expected[UINT8_MAX];
    const unsigned widths[] = {0,1,MATRIX_ROWS,UINT8_MAX};
    for (unsigned width = 0; width < sizeof(widths)/sizeof(widths[0]); ++width) {
        debouncing = rc4_debouncing = false;
        clock_value = UINT16_MAX - 16;
        memset(actual,0,sizeof(actual)); memset(expected,0,sizeof(expected)); memset(raw,0,sizeof(raw));
        for (unsigned event = 0; event < 10000; ++event) {
            bool changed = (random_word() & 7) == 0;
            if (changed && widths[width]) raw[random_word() % widths[width]] = random_word();
            /* Includes 0 ms, exact 5 ms expiry, restarts, and timer rollover. */
            clock_value += random_word() % (DEBOUNCE + 2);
            bool a = debounce(raw, actual, widths[width], changed);
            bool b = rc4_debounce(raw, expected, widths[width], changed);
            assert(a == b && memcmp(actual,expected,sizeof(actual)) == 0);
            assert(debouncing == rc4_debouncing);
        }
    }
    puts("PASS: report send/suppression all byte values and 65536 modifier combinations; randomized reports and 40000 debounce events including timer rollover and row bounds equal RC4.");
}
