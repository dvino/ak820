// Copyright 2026 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

/*******************************************************************************
  88888888888 888      d8b                .d888 d8b 888               d8b
      888     888      Y8P               d88P"  Y8P 888               Y8P
      888     888                        888        888
      888     88888b.  888 .d8888b       888888 888 888  .d88b.       888 .d8888b
      888     888 "88b 888 88K           888    888 888 d8P  Y8b      888 88K
      888     888  888 888 "Y8888b.      888    888 888 88888888      888 "Y8888b.
      888     888  888 888      X88      888    888 888 Y8b.          888      X88
      888     888  888 888  88888P'      888    888 888  "Y8888       888  88888P'
                                                        888                 888
                                                        888                 888
                                                        888                 888
     .d88b.   .d88b.  88888b.   .d88b.  888d888 8888b.  888888 .d88b.   .d88888
    d88P"88b d8P  Y8b 888 "88b d8P  Y8b 888P"      "88b 888   d8P  Y8b d88" 888
    888  888 88888888 888  888 88888888 888    .d888888 888   88888888 888  888
    Y88b 888 Y8b.     888  888 Y8b.     888    888  888 Y88b. Y8b.     Y88b 888
     "Y88888  "Y8888  888  888  "Y8888  888    "Y888888  "Y888 "Y8888   "Y88888
         888
    Y8b d88P
     "Y88P"
*******************************************************************************/

#pragma once
#include "quantum.h"

// Layout content

#define LAYOUT(k0A, k1A, k2A, k3A, k4A, k5A, k6A, k7A, k8A, k9A, kAA, kBA, kCA, kEC, kDA, k0B, k1B, k2B, k3B, k4B, k5B, k6B, k7B, k8B, k9B, kAB, kBB, kCB, kDB, kFB, k0C, k1C, k2C, k3C, k4C, k5C, k6C, k7C, k8C, k9C, kAC, kBC, kCC, kDC, kFC, k0D, k1D, k2D, k3D, k4D, k5D, k6D, k7D, k8D, k9D, kAD, kBD, kDD, kED, k0E, k2E, k3E, k4E, k5E, k6E, k7E, k8E, k9E, kAE, kBE, kDE, kEE, kFD, k0F, k1F, k2F, k5F, k9F, kAF, kBF, kDF, kEF, kFF) { \
	 {k0A, k0B, k0C, k0D, k0E, k0F, KC_NO, KC_NO}, \
	 {k1A, k1B, k1C, k1D, KC_NO, k1F, KC_NO, KC_NO}, \
	 {k2A, k2B, k2C, k2D, k2E, k2F, KC_NO, KC_NO}, \
	 {k3A, k3B, k3C, k3D, k3E, KC_NO, KC_NO, KC_NO}, \
	 {k4A, k4B, k4C, k4D, k4E, KC_NO, KC_NO, KC_NO}, \
	 {k5A, k5B, k5C, k5D, k5E, k5F, KC_NO, KC_NO}, \
	 {k6A, k6B, k6C, k6D, k6E, KC_NO, KC_NO, KC_NO}, \
	 {k7A, k7B, k7C, k7D, k7E, KC_NO, KC_NO, KC_NO}, \
	 {k8A, k8B, k8C, k8D, k8E, KC_NO, KC_NO, KC_NO}, \
	 {k9A, k9B, k9C, k9D, k9E, k9F, KC_NO, KC_NO}, \
	 {kAA, kAB, kAC, kAD, kAE, kAF, KC_NO, KC_NO}, \
	 {kBA, kBB, kBC, kBD, kBE, kBF, KC_NO, KC_NO}, \
	 {kCA, kCB, kCC, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO}, \
	 {kDA, kDB, kDC, kDD, kDE, kDF, KC_NO, KC_NO}, \
	 {KC_NO, KC_NO, kEC, kED, kEE, kEF, KC_NO, KC_NO}, \
	 {KC_NO, kFB, kFC, kFD, KC_NO, kFF, KC_NO, KC_NO} \
}

// Keycode content
