// SPDX-License-Identifier: GPL-2.0-or-later
#if defined(__SDCC_mcs51)
/* Two short foreground helpers use the remaining low CODE window. */
#pragma codeseg AK820LOW
#endif
#include "quantum.h"
#include "ak820_tapping.h"
#ifdef AK820_COMPACT_ONESHOT
extern uint8_t ak820_oneshot_mods, ak820_oneshot_consumed, ak820_oneshot_target;
void ak820_oneshot_post(uint8_t id, bool pressed) {
    if (!pressed && id == ak820_oneshot_target && !get_repeat_key_count()) {
        unregister_mods(ak820_oneshot_consumed);
        ak820_oneshot_consumed = 0;
        ak820_oneshot_target = 255;
    }
}
void ak820_oneshot_cancel(void) {
    ak820_oneshot_mods = ak820_oneshot_consumed = 0;
    ak820_oneshot_target = 255;
}
#endif
