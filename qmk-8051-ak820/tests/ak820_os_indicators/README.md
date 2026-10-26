# OS indicator offline checks

Run the host suite from any directory:

```sh
python tests/ak820_os_indicators/host.py --output /tmp/ak820-os-host.json
```

The host suite compiles the production USB controller, protocol descriptors,
lease module and indicator update function. AddressSanitizer and
UndefinedBehaviorSanitizer remain enabled. It covers the feature-disabled,
OS-indicator, no-mouse, Mac/PC and GUI-lock builds. The GUI-lock build checks
the W pulse and its priority against Caps, layer, suspend and USB configuration.
The USB transport fixture also verifies Direct replies bypass NVM even after an
NVM fault, while ordinary Raw commands retain the NVM transaction path.

Run the linked suite after the selected image passes its stack and interrupt
check:

```sh
python tests/ak820_os_indicators/linked.py \
  --build-dir BUILD_DIRECTORY --s51 PATH_TO_S51 \
  --output-dir /tmp/ak820-os-linked
```

The linked suite executes the supplied image's SDCC instructions in a generic
C52 CPU. It checks lease boundaries, 32-bit wrap, long foreground gaps,
malformed requests, unlock cancellation, phase continuity, independent C/W/OS
DMA channels, Mac-mode fallback where compiled, and the production
lifecycle functions. When the image includes `AK820_COMPACT_GUI_LOCK`, it also
checks the shared W pulse at quarter-period samples across the 2,000 ms cycle,
16-bit timer wrap, non-base layer priority and suspend clearing. It exhausts all
2,000 inputs to the linked pulse-angle helper and checks that each call preserves
R0–R7. The helper address comes from the supplied linked image. Test code at
simulated ROM `0x2000`, stop address `0x2700` and result XRAM
`0x3000..0x37cf` exist only in the simulator; the image file remains unchanged.
It records the
exact image SHA256 and simulator logs.
Timer, Raw HID readiness and USB registers are controlled memory fixtures.
The simulator acknowledges USB write-one-to-clear flags through a memory
breakpoint because ordinary simulated RAM has no controller side effects.

Neither suite opens a USB device. These checks do not establish physical LED
identity, light output, USB electrical behavior or interrupt timing on hardware.
