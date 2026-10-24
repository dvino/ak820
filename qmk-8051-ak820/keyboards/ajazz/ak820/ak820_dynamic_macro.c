// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_dynamic_macro.h"

/* Two 16-tap slots, two bytes per tap. Bit 7 marks an incomplete press;
 * only HID keyboard usages 0x04..0x7f are recorded. No keyrecord arrays. */
typedef struct { uint8_t code, mods; } dm_tap_t;
static dm_tap_t dm_taps[32];
static uint8_t dm_lengths[2];
static uint8_t dm_record; /* 0 idle, 1/2 recording slot */
static uint8_t dm_play;   /* 0 idle, 1/2 playback slot */
static uint8_t dm_index, dm_down, dm_mods;
static uint16_t dm_time;
bool ak820_dynamic_macro_source;

static void dm_finish(void) {
    if (dm_record) {
        uint8_t slot = dm_record - 1, base = slot * 16, out = 0;
        for (uint8_t i = 0; i < dm_lengths[slot]; ++i) {
            if (!(dm_taps[base + i].code & 0x80)) {
                /* Keep this two-byte move in XDATA. A struct assignment makes
                 * SDCC call generic memcpy and save its live loop registers.
                 * out <= i, so both self-copy and downward compaction are safe. */
                dm_taps[base + out].code = dm_taps[base + i].code;
                dm_taps[base + out].mods = dm_taps[base + i].mods;
                ++out;
            }
        }
        dm_lengths[slot] = out;
        dm_record = 0;
    }
}
void ak820_dynamic_macro_cancel(void) {
    dm_finish();
    /* Shared clear_keyboard path immediately clears every owned key/mod.
     * Do not emit a stale intermediate report during that transaction. */
    dm_play = dm_down = 0;
    ak820_dynamic_macro_source = false;
}
bool ak820_dynamic_macro_process(uint16_t code, bool pressed) {
    if (code < QK_DYNAMIC_MACRO_RECORD_START_1 || code > QK_DYNAMIC_MACRO_PLAY_2) return true;
    if (!pressed || get_repeat_key_count()) return false;
    /* A playing slot cannot be overwritten or recursively invoked. Stop
     * controls are also ignored until playback has released its own output. */
    if (dm_play) return false;
    dm_finish();
    if (code <= QK_DYNAMIC_MACRO_RECORD_START_2) {
        dm_record = code - QK_DYNAMIC_MACRO_RECORD_START_1 + 1;
        dm_lengths[dm_record - 1] = 0;
    } else if (code >= QK_DYNAMIC_MACRO_PLAY_1) {
        dm_play = code - QK_DYNAMIC_MACRO_PLAY_1 + 1;
        dm_index = dm_down = 0;
        dm_time = timer_read();
    }
    return false;
}
void ak820_dynamic_macro_observe(uint8_t code, bool pressed) {
    if (!dm_record || !ak820_dynamic_macro_source || code < KC_A || code >= 0x80) return;
    uint8_t slot = dm_record - 1, base = slot * 16;
    if (pressed) {
        uint8_t i = dm_lengths[slot];
        if (i == 16) return; /* Full: retain first 16; still accept releases. */
        dm_taps[base + i].code = code | 0x80;
        dm_taps[base + i].mods = get_mods() | get_weak_mods();
        dm_lengths[slot] = i + 1;
    } else {
        for (uint8_t i = 0; i < dm_lengths[slot]; ++i) {
            if (dm_taps[base + i].code == (uint8_t)(code | 0x80)) {
                dm_taps[base + i].code = code;
                break;
            }
        }
    }
}
void ak820_dynamic_macro_task(uint16_t now) {
    if (!dm_play || ak820_macro_primitive || ak820_keyboard_report_pending() || (uint16_t)(now - dm_time) < 10) return;
    dm_time = now;
    if (dm_down) {
        del_owned_key(dm_down);
        del_owned_mods(dm_mods);
        dm_down = 0;
        send_keyboard_report();
    } else if (dm_index == dm_lengths[dm_play - 1]) {
        dm_play = 0;
    } else {
        uint8_t i = (dm_play - 1) * 16 + dm_index++;
        uint8_t code = dm_taps[i].code;
        /* add/del balances even an existing owner and rollover-hidden keys.
         * An already-held usage cannot form a fresh tap; skip it. */
        if (!add_owned_key(code)) {
            del_owned_key(code);
            return;
        }
        dm_down = code;
        dm_mods = dm_taps[i].mods;
        add_owned_mods(dm_mods);
        send_keyboard_report();
    }
}
