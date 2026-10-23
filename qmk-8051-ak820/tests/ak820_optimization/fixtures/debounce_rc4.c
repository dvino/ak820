/* SPDX-License-Identifier: GPL-2.0-or-later */
/* Immutable function body from AK820 commit cb9ff6ea, renamed for comparison. */
bool rc4_debounce(matrix_row_t raw[], matrix_row_t cooked[], uint8_t num_rows, bool changed) {
    bool cooked_changed = false;

    if (changed) {
        rc4_debouncing      = true;
        rc4_debouncing_time = timer_read_fast();
    }

    if (rc4_debouncing && timer_elapsed_fast(rc4_debouncing_time) >= DEBOUNCE) {
        if (memcmp(cooked, raw, sizeof(matrix_row_t) * num_rows) != 0) {
            memcpy(cooked, raw, sizeof(matrix_row_t) * num_rows);
            cooked_changed = true;
            dprint("chd\n");
        }
        rc4_debouncing = false;
    }

    return cooked_changed;
}
