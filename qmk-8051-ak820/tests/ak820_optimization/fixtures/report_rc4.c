/* SPDX-License-Identifier: GPL-2.0-or-later */
/* Immutable function body from AK820 commit cb9ff6ea, renamed for comparison. */
void rc4_send_keyboard_report(void) {
    keyboard_report->mods = real_mods;
    keyboard_report->mods |= weak_mods;

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
    if (memcmp(keyboard_report, &last_report, sizeof(report_keyboard_t)) != 0) {
        memcpy(&last_report, keyboard_report, sizeof(report_keyboard_t));
        host_keyboard_send(keyboard_report);
    }
#endif
}
