/* Copyright 2021 QMK
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
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
#include <LUFA/Drivers/USB/USB.h>
#include "usb_util.h"
#include "wait.h"
#ifdef AK820_BOARD
#    include "usb_device.h"
#endif

void usb_disconnect(void) {
#ifdef AK820_BOARD
    IE_USB = 0;
    USB_CTRL = 0;
    USB_EnumStatus = D0UsbConfig = 0;
#else
    //USB_Disable();TODO implement this
    //USB_DeviceState = DEVICE_STATE_Unattached;TODO implement this
#endif
}

bool usb_connected_state(void) {
#ifdef AK820_BOARD
    return D0UsbConfig != 0;
#else
    //return USB_Device_IsAddressSet(); TODO implement this
    return true; 
#endif
}

#if defined(OTGPADE)
bool usb_vbus_state(void) {
    USB_OTGPAD_On(); // enables VBUS pad
    wait_us(5);

    return USB_VBUS_GetStatus(); // checks state of VBUS
}
#endif
