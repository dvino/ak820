/* SPDX-License-Identifier: GPL-2.0-or-later
 * Complete CUSTOM_MATRIX=yes implementation. The hardware driver samples
 * during LED blanking; QMK's existing debounce handles the resulting rows.
 */
#include "sdcc_dummy_macros.h"
#include "matrix.h"
#include "debounce.h"
#include "ak820_board.h"

#if MATRIX_ROWS != AK820_SCAN_ROWS || MATRIX_COLS != AK820_SCAN_COLS
#    error "AK820 electrical matrix is16x8"
#endif

matrix_row_t raw_matrix[MATRIX_ROWS];
matrix_row_t matrix[MATRIX_ROWS];

uint8_t matrix_rows(void) { return MATRIX_ROWS; }
uint8_t matrix_cols(void) { return MATRIX_COLS; }

bool matrix_is_on(uint8_t row, uint8_t col) {
    return row < MATRIX_ROWS && col < MATRIX_COLS && (matrix[row] & (MATRIX_ROW_SHIFTER << col));
}

matrix_row_t matrix_get_row(uint8_t row) {
    return row < MATRIX_ROWS ? matrix[row] : 0;
}

bool peek_matrix(uint8_t row, uint8_t col, bool raw) {
    if (row >= MATRIX_ROWS || col >= MATRIX_COLS) {
        return false;
    }
    return ((raw ? raw_matrix[row] : matrix[row]) & (MATRIX_ROW_SHIFTER << col)) != 0;
}

/* SDCC cannot replace weak symbols. Define AK820_MATRIX_USER_HOOKS only when
 * a custom keymap supplies both user hooks itself. */
#ifndef AK820_MATRIX_USER_HOOKS
void matrix_init_user(void) {}
void matrix_scan_user(void) {}
#endif
void matrix_init_kb(void) { matrix_init_user(); }
void matrix_scan_kb(void) { matrix_scan_user(); }

void matrix_init_custom(void) { ak820_board_init(); }
bool matrix_scan_custom(matrix_row_t current_matrix[]) { return ak820_matrix_snapshot(current_matrix); }

void matrix_init(void) {
    uint8_t i;
    for (i = 0; i < MATRIX_ROWS; ++i) {
        raw_matrix[i] = 0;
        matrix[i] = 0;
    }
    debounce_init(MATRIX_ROWS);
    matrix_init_custom();
    matrix_init_kb();
}

uint8_t matrix_scan(void) {
    bool changed = matrix_scan_custom(raw_matrix);
    changed = debounce(raw_matrix, matrix, MATRIX_ROWS, changed);
    matrix_scan_kb();
    return changed;
}

/* This board's scan timing is implemented in the LED IRQ assembly. */
void matrix_output_select_delay(void) {}
void matrix_output_unselect_delay(uint8_t line, bool key_pressed) {
    (void)line;
    (void)key_pressed;
}
void matrix_io_delay(void) {}

/* No console transport is enabled in the AK820 release configuration. */
void matrix_print(void) {}
