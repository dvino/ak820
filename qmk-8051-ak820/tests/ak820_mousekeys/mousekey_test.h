/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <stdbool.h>
#include <stdint.h>
#define __xdata
#define MOUSE_SHARED_EP
#define MOUSE_IN_EPNUM 2
#define REPORT_ID_MOUSE 2
#define KC_MS_UP 0xcd
#define KC_MS_RIGHT 0xd0
#define KC_MS_BTN1 0xd1
#define KC_MS_BTN5 0xd5
#define KC_MS_WH_UP 0xd9
#define KC_MS_WH_RIGHT 0xdc
typedef struct { uint8_t report_id, buttons; int8_t x,y,v,h; } report_mouse_t;
uint16_t timer_read(void);
bool ak820_usb_try_send(uint8_t, const uint8_t *, uint8_t);
