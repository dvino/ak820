// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#ifndef AK820_LEADER_TIMEOUT
#    define AK820_LEADER_TIMEOUT 300
#endif
#if AK820_LEADER_TIMEOUT < 1 || AK820_LEADER_TIMEOUT > 1000
#    error "Leader timeout must be 1..1000 ms"
#endif
