#pragma once

#include <stdbool.h>

/* Volatile session mode: zero at startup means PC. */
#ifdef AK820_MAC_PC
#    if defined(__SDCC_mcs51)
extern __bit ak820_mac_mode;
#    else
extern bool ak820_mac_mode;
#    endif
#endif
