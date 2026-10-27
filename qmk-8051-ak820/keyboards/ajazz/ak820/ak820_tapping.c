// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_tapping.h"
#ifdef AK820_QMK_SETTINGS
#    include "ak820_settings.h"
#    define AK820_TAPPING_TERM ak820_settings_tapping_term()
#else
#    define AK820_TAPPING_TERM 200
#endif
#include "encoder.h"
#ifdef VIAL_ENABLE
#    include "vial.h"
#endif
#include "dynamic_keymap.h"

#define SOURCES (MATRIX_ROWS * MATRIX_COLS + 2 * NUM_ENCODERS)
#define SOURCE_ACTIVE 1
#define SOURCE_BLOCKED 2
#define SOURCE_HELD 4
#define SOURCE_ONESHOT 8
#define SOURCE_ONESHOT_USED 16
#define SOURCE_STATE_BITS 5
#define SOURCE_STATE_MASK ((1u << SOURCE_STATE_BITS) - 1)
_Static_assert(SOURCE_BLOCKED == (SOURCE_ACTIVE << 1), "cancel active-to-blocked shift");
#define NONE 255
_Static_assert(SOURCES < NONE, "tap source index width");
_Static_assert(MAX_LAYER == 6, "tap layer domain");
_Static_assert(QK_MOD_TAP == 0x2000 && QK_LAYER_TAP_MAX == 0x4fff, "dual-role byte namespace");
/* One pending decision; other presses resolve it before admission. No event
 * queue, replay recursion or rollover-dependent owner limit is needed. */
/* ACTIVE tracks admission until its accepted release. HELD is the resolved
 * dual-role owner. BLOCKED survives cancellation until the physical release.
 * A release clears ACTIVE before downstream hooks; cancellation must not
 * infer a still-pressed source from HELD alone. */
/* All five flags coexist independently. One masked byte per source avoids
 * cross-byte extraction in the code-size-limited maximal profile. */
#define SOURCE_STATE_BYTES SOURCES
static uint8_t source_state[SOURCE_STATE_BYTES];
static uint8_t source_state_get(uint8_t id) {
    return source_state[id];
}
static void source_state_set(uint8_t id, uint8_t state) {
    source_state[id] = state & SOURCE_STATE_MASK;
}
static uint8_t pending = NONE;
static uint16_t pending_time, pending_code;

#ifndef AK820_COMPACT_ONESHOT
/* Keep the existing private ABI when no external One Shot caller exists. */
#define ak820_tapping_source source
static
#endif
uint8_t ak820_tapping_source(keypos_t key) {
    if (key.row < MATRIX_ROWS && key.col < MATRIX_COLS) return key.row * MATRIX_COLS + key.col;
    if (key.col < NUM_ENCODERS) {
        if (key.row == KEYLOC_ENCODER_CW) return MATRIX_ROWS * MATRIX_COLS + key.col;
        if (key.row == KEYLOC_ENCODER_CCW) return MATRIX_ROWS * MATRIX_COLS + NUM_ENCODERS + key.col;
    }
    return NONE;
}
static void hold(uint16_t code, bool pressed) {
    if (code < QK_LAYER_TAP) {
        uint8_t mods = (code >> 8) & 31;
        if (mods & 16) mods <<= 4;
        if (pressed) register_mods(mods);
        else unregister_mods(mods);
    } else {
        uint8_t layer = (code >> 8) & 15;
        if (pressed) layer_hold_on(layer);
        else layer_hold_off(layer);
    }
}
static void commit_pending(void) {
    uint8_t id = pending;
    pending = NONE; /* A report callback cannot resurrect the decision. */
    source_state_set(id, source_state_get(id) | SOURCE_HELD);
    hold(pending_code, true);
}
bool ak820_tapping_before(const keyevent_t AK820_STATE_MEM *event) {
    uint8_t id = ak820_tapping_source(event->key);
#ifdef VIAL_ENABLE
    if (vial_unlock_in_progress) {
        if (IS_EVENT(*event) && id != NONE && !event->pressed) source_state_set(id, source_state_get(id) & ~SOURCE_BLOCKED);
        return false;
    }
#endif
    if (pending != NONE && ((uint16_t)(event->time - pending_time) >= AK820_TAPPING_TERM ||
        (IS_EVENT(*event) && event->pressed && (id == NONE || id != pending)))) commit_pending();
    if (IS_NOEVENT(*event) || id == NONE) return true;
    if ((source_state_get(id) & SOURCE_BLOCKED)) {
        if (!event->pressed) source_state_set(id, source_state_get(id) & ~SOURCE_BLOCKED);
        return false;
    }
    /* Duplicate presses and unmatched releases cannot acquire/drop owners. */
    if (event->pressed == ((source_state_get(id) & SOURCE_ACTIVE) != 0)) return false;
    source_state_set(id, source_state_get(id) ^ SOURCE_ACTIVE);
    return true;
}
bool ak820_tapping_process(keyrecord_t AK820_STATE_MEM *record) {
    uint8_t id, kind;
    uint16_t code;
#ifdef AK820_COMPACT_SPACE_CADET
    uint8_t sc_mods = 0;
#endif
    if (IS_NOEVENT(record->event)) return true;
    id = ak820_tapping_source(record->event.key);
    if (id == NONE) return true;
    code = record->keycode;
    kind = code >> 8;
    /* This compact encoding is a physical matrix-key feature. Reject it
     * before a non-matrix source can acquire pending or hold state. */
    if ((kind >= 0x40 && kind <= 0x45) && (code & 0x00f0) == 0x00f0 && id >= MATRIX_ROWS * MATRIX_COLS) return false;
#ifdef AK820_COMPACT_SPACE_CADET
    if (code == SC_LSPO) { code = MT(MOD_LSFT, KC_9); sc_mods = MOD_BIT(KC_LEFT_SHIFT); }
    else if (code == SC_RSPC) { code = MT(MOD_RSFT, KC_0); sc_mods = MOD_BIT(KC_RIGHT_SHIFT); }
    else if (code == SC_SENT) code = MT(MOD_RSFT, KC_ENTER);
#endif
    kind = code >> 8;
    if (kind < 0x20 || kind >= 0x50) return true;
    if (kind >= 0x40 && (kind & 15) >= MAX_LAYER) return false;
    if (record->event.pressed) {
        pending = id;
        pending_time = record->event.time;
        pending_code = code;
    } else if (id == pending) {
        pending = NONE;
#ifdef AK820_COMPACT_SPACE_CADET
        if (sc_mods) add_owned_mods(sc_mods);
#endif
        /* F0..FF are the compact layer-tap macro form. The source check
         * above admits matrix keys only; generated macro/Repeat records do
         * not enter this physical event path. */
        if (id < MATRIX_ROWS * MATRIX_COLS && (code & 0x00f0) == 0x00f0 && kind >= 0x40 && kind <= 0x45) {
            dynamic_keymap_macro_send(code & 15);
            return false;
        }
        /* NO and transparent are opaque dual-role taps that emit nothing.
         * All other accepted basic bytes use the real basic decoder/pipeline. */
        record->keycode = (uint8_t)code;
        if (record->keycode > KC_TRANSPARENT) {
            record->tap.count = 1;
            record->event.pressed = true;
            process_record(record);
            record->event.pressed = false;
            process_record(record);
        }
#ifdef AK820_COMPACT_SPACE_CADET
        if (sc_mods) {
            del_owned_mods(sc_mods);
            send_keyboard_report();
        }
#endif
    } else if ((source_state_get(id) & SOURCE_HELD)) {
        source_state_set(id, source_state_get(id) & ~SOURCE_HELD);
        hold(code, false);
    }
    return false;
}
void ak820_tapping_cancel(void) {
    pending = NONE;
    for (uint8_t i = 0; i < SOURCES; ++i) {
        uint8_t state = source_state_get(i);
        source_state_set(i, (state & SOURCE_BLOCKED) | ((state & SOURCE_ACTIVE) << 1));
    }
}

#ifdef AK820_COMPACT_ONESHOT
/* One queued modifier set and one consuming source. While a consuming key
 * remains down, a new OSM works as a held modifier but cannot arm again. */
uint8_t ak820_oneshot_mods, ak820_oneshot_consumed;
uint8_t ak820_oneshot_target = NONE;
bool ak820_oneshot_process(uint16_t code, uint8_t id, bool pressed) {
    uint8_t mods;
    if (id == NONE || get_repeat_key_count()) return true;
#ifdef AK820_COMPACT_GUI_LOCK
    /* Output controls must not consume a queued modifier or mark held OSM used. */
    if (code >= QK_MAGIC_GUI_ON && code <= QK_MAGIC_TOGGLE_GUI) return true;
#endif
#ifdef AK820_COMPACT_CTRL_GUI_SWAP
    /* Session Ctrl/GUI controls also leave queued and held OSM ownership alone. */
    if (code == QK_MAGIC_SWAP_CTL_GUI || code == QK_MAGIC_UNSWAP_CTL_GUI || code == QK_MAGIC_TOGGLE_CTL_GUI) return true;
#endif
#ifdef AK820_MAC_PC
    /* Changing the output mapping is not the key that consumes One Shot. */
    if (code == QK_MAGIC_SWAP_ALT_GUI || code == QK_MAGIC_UNSWAP_ALT_GUI || code == QK_MAGIC_TOGGLE_ALT_GUI) return true;
#endif
    if ((code >> 8) == 0x52 && ((uint8_t)code & 0xe0) == 0xa0) {
        mods = code & 15;
        if (code & 16) mods <<= 4;
        if (pressed) {
            source_state_set(id, source_state_get(id) | SOURCE_ONESHOT);
            source_state_set(id, source_state_get(id) & ~SOURCE_ONESHOT_USED);
            if (ak820_oneshot_target != NONE) source_state_set(id, source_state_get(id) | SOURCE_ONESHOT_USED);
            register_mods(mods);
        } else if (source_state_get(id) & SOURCE_ONESHOT) {
            if (!(source_state_get(id) & SOURCE_ONESHOT_USED)) {
                add_owned_mods(mods & ~ak820_oneshot_mods);
                ak820_oneshot_mods |= mods;
            }
            unregister_mods(mods);
            source_state_set(id, source_state_get(id) & ~(SOURCE_ONESHOT | SOURCE_ONESHOT_USED));
        }
        return false;
    }
    if (pressed && code > KC_TRANSPARENT &&
        !(code >= KC_LCTL && code <= KC_RGUI) &&
        !(code >= QK_TO && code <= QK_LAYER_TAP_TOGGLE_MAX)) {
        for (uint8_t i = 0; i < SOURCES; ++i)
            if (source_state_get(i) & SOURCE_ONESHOT) source_state_set(i, source_state_get(i) | SOURCE_ONESHOT_USED);
        if (ak820_oneshot_mods) {
            ak820_oneshot_consumed = ak820_oneshot_mods;
            ak820_oneshot_target = id;
            ak820_oneshot_mods = 0;
        }
    }
    return true;
}
#endif
