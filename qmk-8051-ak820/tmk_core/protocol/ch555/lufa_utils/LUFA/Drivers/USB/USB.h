#include "sdcc_dummy_macros.h"
#include "progmem.h"
#include <stddef.h>
#include <inttypes.h>

/* This shim replaces Common.h, including its architecture definitions. Keep
 * MCS51 distinct from AVR so descriptors use uint16_t, not SDCC's wchar_t. */
#define __INCLUDE_FROM_COMMON_H
#include "lib/lufa/LUFA/Common/Architectures.h"
#undef __INCLUDE_FROM_COMMON_H
#define ARCH_MCS51 3

#define ATTR_PACKED __attribute__((packed))
/** Concatenates the given input into a single token, via the C Preprocessor.
 *
 *  \param[in] x  First item to concatenate.
 *  \param[in] y  Second item to concatenate.
 *
 *  \return Concatenated version of the input.
 */
#define CONCAT(x, y) x##y

/** CConcatenates the given input into a single token after macro expansion, via the C Preprocessor.
 *
 *  \param[in] x  First item to concatenate.
 *  \param[in] y  Second item to concatenate.
 *
 *  \return Concatenated version of the expanded input.
 */
#define CONCAT_EXPANDED(x, y) CONCAT(x, y)
#define CPU_TO_LE16(x) (x)

// We don't need anything from the following files, or we have defined it already
#define __LUFA_COMMON_H__
#define __USBMODE_H__
#define __USBEVENTS_H__
#define __HIDPARSER_H__
#define __USBCONTROLLER_AVR8_H__

#define __INCLUDE_FROM_USB_DRIVER
#define __INCLUDE_FROM_HID_DRIVER
#define __INCLUDE_FROM_CDC_DRIVER
#define __INCLUDE_FROM_AUDIO_DRIVER
#define __INCLUDE_FROM_MIDI_DRIVER
#include "lib/lufa/LUFA/Drivers/USB/Class/Common/HIDClassCommon.h"
#include "lib/lufa/LUFA/Drivers/USB/Class/Common/HIDReportData.h"
#include "lib/lufa/LUFA/Drivers/USB/Class/Common/CDCClassCommon.h"
#include "lib/lufa/LUFA/Drivers/USB/Class/Common/AudioClassCommon.h"
#include "lib/lufa/LUFA/Drivers/USB/Class/Common/MIDIClassCommon.h"
#include "lib/lufa/LUFA/Drivers/USB/Core/USBController.h"

_Static_assert(sizeof(((USB_Descriptor_String_t *)0)->UnicodeString[0]) == 2,
               "USB string payload must use 16-bit code units");
_Static_assert(offsetof(USB_Descriptor_String_t, UnicodeString) == 2,
               "USB string header must be two bytes");
