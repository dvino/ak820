/* Copyright 2020 Nick Brassel (tzarc)
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

// USB strings contain UTF-16 code units; SDCC's wchar_t is 32 bits.
#define USBCONCAT(a, b) a##b
#ifdef PROTOCOL_CH555
#    define USBSTR(s) USBCONCAT(u, s)
_Static_assert(sizeof(USBSTR("A")[0]) == 2, "USB literal must use 16-bit code units");
#else
#    define USBSTR(s) USBCONCAT(L, s)
#endif

#define HID_VALUE_16(v) ((uint8_t)(v & 0xFF)), ((uint8_t)(v >> 8))

/////////////////////
// RAW Usage page and ID configuration

#ifndef RAW_USAGE_PAGE
#    define RAW_USAGE_PAGE 0xFF60
#endif

#ifndef RAW_USAGE_ID
#    define RAW_USAGE_ID 0x61
#endif
