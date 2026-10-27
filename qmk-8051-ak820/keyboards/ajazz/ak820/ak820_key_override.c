// SPDX-License-Identifier: GPL-2.0-or-later
#include "quantum.h"
#include "ak820_key_override.h"
#include "dynamic_keymap.h"

#define NONE 255
#define ENABLED 0x80
#define ACTIVATIONS 7
static vial_key_override_entry_t entries[VIAL_KEY_OVERRIDE_ENTRIES];
static uint8_t source = NONE, trigger, active = NONE, previous_mods;
/* This engine never dispatches records, reports or callbacks. Helpers share
 * one synchronous context instead of model-large parameter spill slots. */
static uint8_t current_mods, current_layer;
#if defined(__SDCC_mcs51)
static __bit enabled = true, blocked, hidden;
#else
static bool enabled = true, blocked, hidden;
#endif

/* Inline this tiny predicate: a model-large helper spills its argument and
 * saves registers at each of the three call sites. */
#define basic(key) ((key) >= KC_A && (key) <= KC_EXSEL)
ak820_key_override_result_t ak820_key_override_valid(const vial_key_override_entry_t AK820_STATE_MEM *e) {
    const uint8_t AK820_STATE_MEM *bytes = (const uint8_t AK820_STATE_MEM *)e;
    uint8_t any = 0;
    /* The packed Vial ABI is little endian. Empty disabled slots are zero;
     * every other row receives the same validation, enabled or disabled. */
    for (uint8_t i = 0; i < 10; ++i) any |= bytes[i];
    if (!any) return true;
    if (bytes[1] || !basic(bytes[0])) return false;
    if (bytes[5] || !bytes[4] || (bytes[4] & 0xC0)) return false;
    if ((bytes[9] & 0x40) || !(bytes[9] & ACTIVATIONS)) return false;
    /* Replacement is KC_NO or an ordinary usage with QK_MODS prefixes. */
    if (bytes[2] | bytes[3]) return bytes[3] < 32 && basic(bytes[2]);
    return true;
}
/* A mask containing both sides means either side, as in upstream QMK. */
static ak820_key_override_result_t eligible(uint8_t index) {
    vial_key_override_entry_t AK820_STATE_MEM *e = &entries[index];
    uint8_t low = e->trigger_mods & 15, high = e->trigger_mods >> 4;
    if (current_layer >= 6 || !((uint8_t)e->layers & ((uint8_t)1 << current_layer)) ||
        (current_mods & e->negative_mod_mask)) return false;
    if (e->options & 8) return !(low | high) || (current_mods & e->trigger_mods);
    return ((current_mods & low) | ((current_mods >> 4) & high)) == (low | high);
}
static void deactivate(void) {
    if (active != NONE && (entries[active].options & 16)) hidden = true;
    active = NONE;
}
void ak820_key_override_cancel(void) {
    source = active = NONE;
    previous_mods = 0;
    blocked = hidden = false;
}
void ak820_key_override_reload(void) {
    ak820_key_override_cancel();
    for (uint8_t i = 0; i < VIAL_KEY_OVERRIDE_ENTRIES; ++i) {
        /* The compact getter validates and zeros malformed stored rows. */
        if (dynamic_keymap_get_key_override(i, &entries[i]))
            entries[i].options = 0;
    }
}
static void activate(bool trigger_down) {
    if (!enabled || source == NONE || blocked || hidden || active != NONE) return;
    for (uint8_t i = 0; i < VIAL_KEY_OVERRIDE_ENTRIES; ++i) {
        vial_key_override_entry_t AK820_STATE_MEM *e = &entries[i];
        if ((uint8_t)e->trigger == trigger && (e->options & ENABLED) && (trigger_down ? (e->options & 1) :
            (((e->options & 2) && (e->trigger_mods & current_mods & ~previous_mods)) ||
             ((e->options & 4) && (e->negative_mod_mask & previous_mods & ~current_mods)))) && eligible(i)) {
            active = i;
            return;
        }
    }
}
void ak820_key_override_sync(uint8_t mods, uint8_t layer) {
    current_mods = mods; current_layer = layer;
    if (active != NONE && !eligible(active)) deactivate();
    activate(false);
    previous_mods = mods;
}
ak820_key_override_result_t ak820_key_override_process(keyrecord_t AK820_STATE_MEM *record, uint8_t mods, uint8_t layer) {
    uint16_t key;
    uint8_t id;
    ak820_key_override_sync(mods, layer);
    key = record->keycode;
    if (key >= QK_KEY_OVERRIDE_TOGGLE && key <= QK_KEY_OVERRIDE_OFF) {
        if (record->event.pressed) {
            if (key == QK_KEY_OVERRIDE_ON) enabled = true;
            else if (key == QK_KEY_OVERRIDE_OFF) enabled = false;
            else enabled = !enabled;
            if (!enabled) { deactivate(); blocked = true; }
        }
        return false;
    }
    if (record->event.key.row >= MATRIX_ROWS || record->event.key.col >= MATRIX_COLS) return true;
    id = record->event.key.row * MATRIX_COLS + record->event.key.col;
    if (source == id) {
        if (!record->event.pressed) ak820_key_override_cancel();
        return false;
    }
    if (!record->event.pressed) return true;
    if (active != NONE && !(entries[active].options & 32) && !(key >= KC_LEFT_CTRL && key <= KC_RIGHT_GUI)) {
        deactivate(); blocked = true;
    }
    if (source != NONE || !enabled || !basic(key)) return true;
    for (uint8_t i = 0; i < VIAL_KEY_OVERRIDE_ENTRIES; ++i) {
        if ((uint8_t)entries[i].trigger == (uint8_t)key && (entries[i].options & ENABLED)) {
            source = id; trigger = key; hidden = blocked = false;
            activate(true);
            return false;
        }
    }
    return true;
}
uint8_t ak820_key_override_key(void) {
    if (source == NONE || hidden) return 0;
    return active == NONE ? trigger : (uint8_t)entries[active].replacement;
}
uint8_t ak820_key_override_mods(uint8_t mods) {
    uint8_t replacement;
    if (active == NONE) return mods;
    replacement = entries[active].replacement >> 8;
    if (replacement & 16) replacement = (replacement & 15) << 4;
    return (mods & ~entries[active].suppressed_mods) | replacement;
}
ak820_key_override_result_t ak820_key_override_enabled(void) { return enabled; }
