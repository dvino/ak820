# AK820 IRQ stack audit (offline)

From the QMK tree, after producing a linked build:

```sh
python tests/ak820_irq/run.py \
  --build-dir .build/rc5-baseline \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51 \
  --stock-rom /path/to/private-oem-references/releases/rc5/reference/stock-full.bin \
  --output-dir .build/rc5-baseline-irq \
  --main-sample-bytes 56
```

The ROM is an owner-held local reference from the private archive; it is not
stored in or distributed with this repository.

The runner checks relocated instruction bytes against the linked IHX, explores
the IRQ callback control flow, and counts balanced PUSH/POP, calls and tail
jumps. Unsupported stack writes, recursive calls and unknown indirect dispatch
fail the check. The recognized SDCC string-descriptor dispatch and LED selector
tables assume a valid table entry, as required by their source index checks.

It verifies the exact preserved OEM wrappers and their 17-byte entry overhead:
the two-byte hardware return frame, 13 saved registers, and the two-byte call
to the application callback. It then executes those actual wrapper bytes and
the linked callbacks in the generic uCsim C52 CPU. LCALL supplies the hardware
return frame; USB ACK side effects and an interrupt of higher priority are
injected explicitly. The USB SET_CONFIGURATION path exercises its largest
static stack frame. USB interrupted by Timer0 or LED is checked at that frame.
All register banks, ACC/B/DPTR/PSW, SP, and a representative main stack canary
must be preserved across the wrappers.

The RC4 baseline bounds are Timer0 19, USB 23 and LED 19 bytes, including the
wrapper. At most two simultaneous interrupt priority levels, following the
CH555 register contract, therefore add at most 42 bytes. The baseline link map
has 145 stack bytes available. A **representative** main frame of 56 bytes plus
42 IRQ bytes leaves 47 bytes. The 56 is the largest previously exercised RC4
main scenario, **not a global main-stack upper bound**. Supply a larger measured
main peak when validating a changed profile. The firmware currently preserves
inherited IP/IP_EX priority choices; the sum includes either priority order.

`results.json` and CPU logs bind these observations to exact IHX/MAP and runner
hashes. They do not model VS11K28A interrupt routing, LED DMA, USB timing, actual
peripheral semantics, stack depth of every main path, or physical hardware.
No USB device is opened and no firmware or device image is written.
