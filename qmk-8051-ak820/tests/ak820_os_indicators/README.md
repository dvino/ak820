# OS indicator offline checks

Run the host suite from any directory:

```sh
python tests/ak820_os_indicators/host.py --output /tmp/ak820-os-host.json
```

The host suite compiles the production USB controller, protocol descriptors,
lease module and indicator update function. AddressSanitizer and
UndefinedBehaviorSanitizer remain enabled. It runs with the feature disabled,
with it enabled, and with it enabled without mouse support, and with Mac/PC mode enabled. The disabled run
checks that FD02 retains its unknown-command behavior.

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
lifecycle functions. It records the exact image SHA256 and simulator logs.
Timer, Raw HID readiness and USB registers are controlled memory fixtures.
The simulator acknowledges USB write-one-to-clear flags through a memory
breakpoint because ordinary simulated RAM has no controller side effects.

Neither suite opens a USB device. These checks do not establish physical LED
identity, light output, USB electrical behavior or interrupt timing on hardware.
