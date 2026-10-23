#include "sdcc_dummy_macros.h"
/*
Copyright 2013 Jun Wako <wakojun@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
#include "host.h"
#include "report.h"
#include "debug.h"
#include "action_util.h"
#include "action_layer.h"
#include "timer.h"
#include "keycode_config.h"
#include "qmk_settings.h"
#include <string.h>

extern keymap_config_t keymap_config;

static uint8_t real_mods = 0;
static uint8_t weak_mods = 0;
#ifdef AK820_COMPACT_TAPPING
/* Raw temporary modifiers (Caps Word, macros) and held action owners are
 * separate. Clearing temporary weak state cannot release an encoded action. */
static uint8_t owned_mod_refs[8], owned_weak_refs[8];
static uint8_t owned_mods, owned_weak_mods;
static uint8_t macro_mods[2];
bool ak820_macro_primitive, ak820_macro_cancelled;
bool ak820_macro_change(uint8_t AK820_STATE_MEM *bits, uint8_t index, bool pressed) {
    if (!ak820_macro_primitive) return true;
    uint8_t mask = 1u << (index & 7);
    bits += index >> 3;
    if (((*bits & mask) != 0) == pressed) return false;
    *bits ^= mask;
    return true;
}
static void change_owned(uint8_t mods, uint8_t mode) {
    uint8_t kind = mode >> 1;
    bool pressed = (mode & 1) != 0;
    uint8_t AK820_STATE_MEM *refs = kind ? owned_weak_refs : owned_mod_refs;
    if (ak820_macro_primitive) {
        uint8_t old = macro_mods[kind];
        macro_mods[kind] = pressed ? old | mods : old & ~mods;
        mods &= pressed ? ~old : old;
    }
    uint8_t result = 0;
    for (uint8_t i = 0, bit = 1; i < 8; ++i, bit <<= 1) {
        if (mods & bit) {
            if (pressed) ++refs[i];
            else if (refs[i]) --refs[i];
        }
        if (refs[i]) result |= bit;
    }
    if (kind) owned_weak_mods = result;
    else owned_mods = result;
}
void add_owned_mods(uint8_t mods) { change_owned(mods, 1); }
void del_owned_mods(uint8_t mods) { change_owned(mods, 0); }
void add_owned_weak_mods(uint8_t mods) { change_owned(mods, 3); }
void del_owned_weak_mods(uint8_t mods) { change_owned(mods, 2); }
void clear_owned_mods(void) {
    for (uint8_t i = 0; i < 8; ++i) owned_mod_refs[i] = owned_weak_refs[i] = 0;
    owned_mods = owned_weak_mods = macro_mods[0] = macro_mods[1] = 0;
    ak820_macro_cancelled = true;
}
/* Keyboard usages need ownership even when a 6KRO packet has no free slot.
 * The usage-domain bound also covers synthetic Repeat and immediate taps. */
static uint8_t key_refs[KC_EXSEL + 1];
static uint8_t distinct_keys;
static uint8_t macro_keys[(KC_EXSEL + 8) / 8];
void clear_owned_keys(void) {
    for (uint8_t i = 0; i <= KC_EXSEL; ++i) key_refs[i] = 0;
    distinct_keys = 0;
    for (uint8_t i = 0; i < sizeof(macro_keys); ++i) macro_keys[i] = 0;
}
bool add_owned_key(uint8_t code) {
    if (!ak820_macro_change(macro_keys, code, true)) return false;
    if (key_refs[code]++) return false;
    ++distinct_keys;
#ifdef NKRO_ENABLE
    if (keyboard_protocol && keymap_config.nkro) { add_key(code); return true; }
#endif
    if (distinct_keys > KEYBOARD_REPORT_KEYS) {
        for (uint8_t i = 0; i < KEYBOARD_REPORT_KEYS; ++i) keyboard_report->keys[i] = 1; /* HID ErrorRollOver */
    } else add_key(code);
    return true;
}
bool del_owned_key(uint8_t code) {
    if (!ak820_macro_change(macro_keys, code, false)) return false;
    if (!key_refs[code] || --key_refs[code]) return false;
    --distinct_keys;
#ifdef NKRO_ENABLE
    if (keyboard_protocol && keymap_config.nkro) { del_key(code); return true; }
#endif
    if (distinct_keys > KEYBOARD_REPORT_KEYS) return true;
    if (distinct_keys == KEYBOARD_REPORT_KEYS) {
        clear_keys();
        /* Leaving rollover: every surviving owner is now representable. */
        for (uint8_t key = KC_A; key <= KC_EXSEL; ++key) if (key_refs[key]) add_key(key);
    } else del_key(code);
    return true;
}

/* Each namespace is a bounded activation-order list. A second owner of the
 * same usage keeps its original priority; removing the winner restores the
 * most recently activated remaining usage, never a later deferred tap. */
#define USAGE_COUNT (KC_LAUNCHPAD - KC_SYSTEM_POWER + 1)
#define SYSTEM_COUNT (KC_SYSTEM_WAKE - KC_SYSTEM_POWER + 1)
static uint8_t usage_refs[USAGE_COUNT], usage_order[USAGE_COUNT], usage_lengths[2];
static uint8_t macro_usages[(USAGE_COUNT + 7) / 8];
_Static_assert(USAGE_COUNT == 30 && SYSTEM_COUNT == 3, "owned extra usage domain");
void clear_owned_usages(void) {
    for (uint8_t i = 0; i < USAGE_COUNT; ++i) usage_refs[i] = usage_order[i] = 0;
    usage_lengths[0] = usage_lengths[1] = 0;
    for (uint8_t i = 0; i < sizeof(macro_usages); ++i) macro_usages[i] = 0;
}
void owned_usage_key(uint8_t code, bool pressed) {
    uint8_t which = code >= KC_AUDIO_MUTE;
    uint8_t base = which ? SYSTEM_COUNT : 0;
    uint8_t count = usage_lengths[which];
    uint8_t index = code - KC_SYSTEM_POWER;
    if (!ak820_macro_change(macro_usages, index, pressed)) return;
    if (pressed) {
        if (usage_refs[index]++) return;
        usage_order[base + count++] = index;
    } else {
        if (!usage_refs[index] || --usage_refs[index]) return;
        uint8_t pos = 0;
        while (usage_order[base + pos] != index) ++pos;
        --count;
        for (uint8_t i = pos; i < count; ++i) usage_order[base + i] = usage_order[base + i + 1];
        usage_lengths[which] = count;
        if (pos != count) return; /* A non-winning owner changed only storage. */
    }
    usage_lengths[which] = count;
    code = count ? usage_order[base + count - 1] + KC_SYSTEM_POWER : 0;
    if (which) host_consumer_send(code ? KEYCODE2CONSUMER(code) : 0);
    else host_system_send(code ? KEYCODE2SYSTEM(code) : 0);
}

#endif

#ifdef KEY_OVERRIDE_ENABLE
static uint8_t weak_override_mods = 0;
static uint8_t suppressed_mods    = 0;
#endif

// TODO: pointer variable is not needed
// report_keyboard_t keyboard_report = {};
//report_keyboard_t *keyboard_report = &(report_keyboard_t){};
report_keyboard_t actual_keyboard_report = {.raw={0,0,0,0,0,0,0,0}};
// = {} raise error. ={.raw={}} and ={.raw={0}} compiles but sdcc just refuses to initialize them as 0. damm you sdcc.
#ifndef AK820_BOARD
report_keyboard_t *keyboard_report = &actual_keyboard_report;
#endif

extern inline void add_key(uint8_t key);
extern inline void del_key(uint8_t key);
extern inline void clear_keys(void);

#ifndef NO_ACTION_ONESHOT
static uint8_t oneshot_mods        = 0;
static uint8_t oneshot_locked_mods = 0;
uint8_t        get_oneshot_locked_mods(void) {
    return oneshot_locked_mods;
}
void add_oneshot_locked_mods(uint8_t mods) {
    if ((oneshot_locked_mods & mods) != mods) {
        oneshot_locked_mods |= mods;
        oneshot_locked_mods_changed_kb(oneshot_locked_mods);
    }
}
void set_oneshot_locked_mods(uint8_t mods) {
    if (mods != oneshot_locked_mods) {
        oneshot_locked_mods = mods;
        oneshot_locked_mods_changed_kb(oneshot_locked_mods);
    }
}
void clear_oneshot_locked_mods(void) {
    if (oneshot_locked_mods) {
        oneshot_locked_mods = 0;
        oneshot_locked_mods_changed_kb(oneshot_locked_mods);
    }
}
void del_oneshot_locked_mods(uint8_t mods) {
    if (oneshot_locked_mods & mods) {
        oneshot_locked_mods &= ~mods;
        oneshot_locked_mods_changed_kb(oneshot_locked_mods);
    }
}
static uint16_t oneshot_time = 0;
bool            has_oneshot_mods_timed_out(void) {
    return QS_oneshot_timeout > 0 && TIMER_DIFF_16(timer_read(), oneshot_time) >= QS_oneshot_timeout;
}
#endif

/* oneshot layer */
#ifndef NO_ACTION_ONESHOT
/** \brief oneshot_layer_data bits
 * LLLL LSSS
 * where:
 *   L => are layer bits
 *   S => oneshot state bits
 */
static uint8_t oneshot_layer_data = 0;

inline uint8_t get_oneshot_layer(void) {
    return oneshot_layer_data >> 3;
}
inline uint8_t get_oneshot_layer_state(void) {
    return oneshot_layer_data & 0b111;
}

#    ifdef SWAP_HANDS_ENABLE
enum {
    SHO_OFF,
    SHO_ACTIVE,  // Swap hands button was pressed, and we didn't send any swapped keys yet
    SHO_PRESSED, // Swap hands button is currently pressed
    SHO_USED,    // Swap hands button is still pressed, and we already sent swapped keys
} swap_hands_oneshot = SHO_OFF;
#    endif

static uint16_t oneshot_layer_time = 0;
inline bool     has_oneshot_layer_timed_out(void) {
    return TIMER_DIFF_16(timer_read(), oneshot_layer_time) >= QS_oneshot_timeout && !(get_oneshot_layer_state() & ONESHOT_TOGGLED);
}
#        ifdef SWAP_HANDS_ENABLE
static uint16_t oneshot_swaphands_time = 0;
inline bool     has_oneshot_swaphands_timed_out(void) {
    return TIMER_DIFF_16(timer_read(), oneshot_swaphands_time) >= QS_oneshot_timeout && (swap_hands_oneshot == SHO_ACTIVE);
}
#        endif

#    ifdef SWAP_HANDS_ENABLE

void set_oneshot_swaphands(void) {
    swap_hands_oneshot = SHO_PRESSED;
    swap_hands         = true;
    oneshot_swaphands_time = timer_read();
    if (oneshot_layer_time != 0) {
        oneshot_layer_time = oneshot_swaphands_time;
    }
}

void release_oneshot_swaphands(void) {
    if (swap_hands_oneshot == SHO_PRESSED) {
        swap_hands_oneshot = SHO_ACTIVE;
    }
    if (swap_hands_oneshot == SHO_USED) {
        clear_oneshot_swaphands();
    }
}

void use_oneshot_swaphands(void) {
    if (swap_hands_oneshot == SHO_PRESSED) {
        swap_hands_oneshot = SHO_USED;
    }
    if (swap_hands_oneshot == SHO_ACTIVE) {
        clear_oneshot_swaphands();
    }
}

void clear_oneshot_swaphands(void) {
    swap_hands_oneshot = SHO_OFF;
    swap_hands         = false;
    oneshot_swaphands_time = 0;
}

#    endif

/** \brief Set oneshot layer
 *
 * FIXME: needs doc
 */
void set_oneshot_layer(uint8_t layer, uint8_t state) {
    if (keymap_config.oneshot_enable) {
        oneshot_layer_data = layer << 3 | state;
        layer_on(layer);
        oneshot_layer_time = timer_read();
        oneshot_layer_changed_kb(get_oneshot_layer());
    } else {
        layer_on(layer);
    }
}
/** \brief Reset oneshot layer
 *
 * FIXME: needs doc
 */
void reset_oneshot_layer(void) {
    oneshot_layer_data = 0;
    oneshot_layer_time = 0;
    oneshot_layer_changed_kb(get_oneshot_layer());
}
/** \brief Clear oneshot layer
 *
 * FIXME: needs doc
 */
void clear_oneshot_layer_state(oneshot_fullfillment_t state) {
    uint8_t start_state = oneshot_layer_data;
    oneshot_layer_data &= ~state;
    if ((!get_oneshot_layer_state() && start_state != oneshot_layer_data) && keymap_config.oneshot_enable) {
        layer_off(get_oneshot_layer());
        reset_oneshot_layer();
    }
}
/** \brief Is oneshot layer active
 *
 * FIXME: needs doc
 */
bool is_oneshot_layer_active(void) {
    return get_oneshot_layer_state();
}

/** \brief set oneshot
 *
 * FIXME: needs doc
 */
void oneshot_set(bool active) {
    if (keymap_config.oneshot_enable != active) {
        keymap_config.oneshot_enable = active;
        eeconfig_update_keymap(keymap_config.raw);
        clear_oneshot_layer_state(ONESHOT_OTHER_KEY_PRESSED);
        dprintf("Oneshot: active: %d\n", active);
    }
}

/** \brief toggle oneshot
 *
 * FIXME: needs doc
 */
void oneshot_toggle(void) {
    oneshot_set(!keymap_config.oneshot_enable);
}

/** \brief enable oneshot
 *
 * FIXME: needs doc
 */
void oneshot_enable(void) {
    oneshot_set(true);
}

/** \brief disable oneshot
 *
 * FIXME: needs doc
 */
void oneshot_disable(void) {
    oneshot_set(false);
}

bool is_oneshot_enabled(void) {
    return keymap_config.oneshot_enable;
}

#endif

/** \brief Send keyboard report
 *
 * FIXME: needs doc
 */
void send_keyboard_report(void) {
    keyboard_report->mods = real_mods;
    keyboard_report->mods |= weak_mods;
#ifdef AK820_COMPACT_TAPPING
    keyboard_report->mods |= owned_mods | owned_weak_mods;
#endif

#ifndef NO_ACTION_ONESHOT
    if (oneshot_mods) {
        if (QS_oneshot_timeout > 0 && has_oneshot_mods_timed_out()) {
            dprintf("Oneshot: timeout\n");
            clear_oneshot_mods();
        }
        keyboard_report->mods |= oneshot_mods;
        if (has_anykey(keyboard_report)) {
            clear_oneshot_mods();
        }
    }

#endif

#ifdef KEY_OVERRIDE_ENABLE
    // These need to be last to be able to properly control key overrides
    keyboard_report->mods &= ~suppressed_mods;
    keyboard_report->mods |= weak_override_mods;
#endif

#ifdef PROTOCOL_VUSB
    host_keyboard_send(keyboard_report);
#else
    static report_keyboard_t last_report;

    /* Only send the report if there are changes to propagate to the host. */
#ifdef AK820_BOARD
    _Static_assert(sizeof(report_keyboard_t) <= UINT8_MAX, "Report byte index range");
    bool changed = false;
#    if defined(__SDCC_mcs51)
    uint8_t __xdata *dest = (uint8_t __xdata *)&last_report;
    const uint8_t __xdata *src = (const uint8_t __xdata *)keyboard_report;
#    else
    uint8_t *dest = (uint8_t *)&last_report;
    const uint8_t *src = (const uint8_t *)keyboard_report;
#    endif
    for (uint8_t i = 0; i < sizeof(report_keyboard_t); ++i) {
        if (dest[i] != src[i]) {
            dest[i] = src[i];
            changed = true;
        }
    }
    if (changed) host_keyboard_send(keyboard_report);
#else
    if (memcmp(keyboard_report, &last_report, sizeof(report_keyboard_t)) != 0) {
        memcpy(&last_report, keyboard_report, sizeof(report_keyboard_t));
        host_keyboard_send(keyboard_report);
    }
#endif
#endif
}

/** \brief Get mods
 *
 * FIXME: needs doc
 */
uint8_t get_mods(void) {
    return real_mods
#ifdef AK820_COMPACT_TAPPING
        | owned_mods
#endif
        ;
}
/** \brief add mods
 *
 * FIXME: needs doc
 */
void add_mods(uint8_t mods) {
    real_mods |= mods;
}
/** \brief del mods
 *
 * FIXME: needs doc
 */
void del_mods(uint8_t mods) {
    real_mods &= ~mods;
}
/** \brief set mods
 *
 * FIXME: needs doc
 */
void set_mods(uint8_t mods) {
    real_mods = mods;
}
/** \brief clear mods
 *
 * FIXME: needs doc
 */
void clear_mods(void) {
    real_mods = 0;
}

/** \brief get weak mods
 *
 * FIXME: needs doc
 */
uint8_t get_weak_mods(void) {
    return weak_mods
#ifdef AK820_COMPACT_TAPPING
        | owned_weak_mods
#endif
        ;
}
/** \brief add weak mods
 *
 * FIXME: needs doc
 */
void add_weak_mods(uint8_t mods) {
    weak_mods |= mods;
}
/** \brief del weak mods
 *
 * FIXME: needs doc
 */
void del_weak_mods(uint8_t mods) {
    weak_mods &= ~mods;
}
/** \brief set weak mods
 *
 * FIXME: needs doc
 */
void set_weak_mods(uint8_t mods) {
    weak_mods = mods;
}
/** \brief clear weak mods
 *
 * FIXME: needs doc
 */
void clear_weak_mods(void) {
    weak_mods = 0;
}

#ifdef KEY_OVERRIDE_ENABLE
/** \brief set weak mods used by key overrides. DO not call this manually
 */
void set_weak_override_mods(uint8_t mods) {
    weak_override_mods = mods;
}
/** \brief clear weak mods used by key overrides. DO not call this manually
 */
void clear_weak_override_mods(void) {
    weak_override_mods = 0;
}

/** \brief set suppressed mods used by key overrides. DO not call this manually
 */
void set_suppressed_override_mods(uint8_t mods) {
    suppressed_mods = mods;
}
/** \brief clear suppressed mods used by key overrides. DO not call this manually
 */
void clear_suppressed_override_mods(void) {
    suppressed_mods = 0;
}
#endif

#ifndef NO_ACTION_ONESHOT
/** \brief get oneshot mods
 *
 * FIXME: needs doc
 */
uint8_t get_oneshot_mods(void) {
    return oneshot_mods;
}

void add_oneshot_mods(uint8_t mods) {
    if ((oneshot_mods & mods) != mods) {
        oneshot_time = timer_read();
        oneshot_mods |= mods;
        oneshot_mods_changed_kb(mods);
    }
}

void del_oneshot_mods(uint8_t mods) {
    if (oneshot_mods & mods) {
        oneshot_mods &= ~mods;
        oneshot_time = oneshot_mods ? timer_read() : 0;
        oneshot_mods_changed_kb(oneshot_mods);
    }
}

/** \brief set oneshot mods
 *
 * FIXME: needs doc
 */
void set_oneshot_mods(uint8_t mods) {
    if (keymap_config.oneshot_enable) {
        if (oneshot_mods != mods) {
            oneshot_time = timer_read();
            oneshot_mods = mods;
            oneshot_mods_changed_kb(mods);
        }
    }
}

/** \brief clear oneshot mods
 *
 * FIXME: needs doc
 */
void clear_oneshot_mods(void) {
    if (oneshot_mods) {
        oneshot_mods = 0;
        oneshot_time = 0;
        oneshot_mods_changed_kb(oneshot_mods);
    }
}
#endif

/** \brief Called when the one shot modifiers have been changed.
 *
 * \param mods Contains the active modifiers active after the change.
 */
__attribute__((weak)) void oneshot_locked_mods_changed_user(uint8_t mods) {}

/** \brief Called when the locked one shot modifiers have been changed.
 *
 * \param mods Contains the active modifiers active after the change.
 */
__attribute__((weak)) void oneshot_locked_mods_changed_kb(uint8_t mods) {
    oneshot_locked_mods_changed_user(mods);
}

/** \brief Called when the one shot modifiers have been changed.
 *
 * \param mods Contains the active modifiers active after the change.
 */
__attribute__((weak)) void oneshot_mods_changed_user(uint8_t mods) {}

/** \brief Called when the one shot modifiers have been changed.
 *
 * \param mods Contains the active modifiers active after the change.
 */
__attribute__((weak)) void oneshot_mods_changed_kb(uint8_t mods) {
    oneshot_mods_changed_user(mods);
}

/** \brief Called when the one shot layers have been changed.
 *
 * \param layer Contains the layer that is toggled on, or zero when toggled off.
 */
__attribute__((weak)) void oneshot_layer_changed_user(uint8_t layer) {}

/** \brief Called when the one shot layers have been changed.
 *
 * \param layer Contains the layer that is toggled on, or zero when toggled off.
 */
__attribute__((weak)) void oneshot_layer_changed_kb(uint8_t layer) {
    oneshot_layer_changed_user(layer);
}

/** \brief inspect keyboard state
 *
 * FIXME: needs doc
 */
uint8_t has_anymod(void) {
    return bitpop(get_mods());
}

#ifdef DUMMY_MOD_NEUTRALIZER_KEYCODE
/** \brief Send a dummy keycode in between the register and unregister event of a modifier key, to neutralize the "flashing modifiers" phenomenon.
 *
 * \param active_mods 8-bit packed bit-array describing the currently active modifiers (in the format GASCGASC).
 *
 * Certain QMK features like  key overrides or retro tap must unregister a previously
 * registered modifier before sending another keycode but this can trigger undesired
 * keyboard shortcuts if the clean tap of a single modifier key is bound to an action
 * on the host OS, as is for example the case for the left GUI key on Windows, which
 * opens the Start Menu when tapped.
 */
void neutralize_flashing_modifiers(uint8_t active_mods) {
    // In most scenarios, the flashing modifiers phenomenon is a problem
    // only for a subset of modifier masks.
    const static uint8_t mods_to_neutralize[] = MODS_TO_NEUTRALIZE;
    const static uint8_t n_mods               = ARRAY_SIZE(mods_to_neutralize);
    for (uint8_t i = 0; i < n_mods; ++i) {
        if (active_mods == mods_to_neutralize[i]) {
            tap_code(DUMMY_MOD_NEUTRALIZER_KEYCODE);
            break;
        }
    }
}
#endif
