# Linked CPU tests

`emitted.py` runs an existing linked SDCC image in uCsim C52. It does not build
firmware or open a USB device. Run from the repository root:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/emitted.py \
  --build-dir qmk-8051-ak820/.build/compact-modtap-defaults-20261023 \
  --s51 toolchains/sdcc-4.6.0/bin/s51 \
  --output-dir host/runs/compact-tapping-linked-20261023
```

The fixture runs the linked CRT and calls the public `action_exec` entry with
its emitted six-byte event ABI. Production code performs decoding, tap and
hold decisions, layer lookup, release caching, ownership and Repeat. Simulated
ROM supplies keymap and encoder settings. A simulator breakpoint observes each
production keyboard-send call, including the brief press and release of a tap.
The breakpoint supplies USB-ready bits before continuing. The linked callback
and report code still execute.

The checks cover the 199/200 ms boundary and timer wrap, every MT mask and LT
target, held remaps, lookup after a layer hold, overlapping modifier owners,
Repeat, duplicate key owners, 6KRO rollover and promotion, NKRO, both encoder
directions, cancellation, default layers, TO, TG, Tri Layer and duplicate
system/consumer usages. A separate test feeds all matrix positions through
`protocol_task` and debounce. Reports, expected snapshots, complete simulator scripts
and logs are saved with the image hash. NKRO snapshots include all 32 bytes.
The Tri Layer configuration-change case changes simulated configuration RAM
while a key is held, then checks release through `action_exec`. The configuration
setter is removed from the linked image; this case does not execute that setter.

Clock counts come from the emulator and include the offline call trampoline.
The scan clock samples each cover two task calls and all changed positions.
The maximum stack pointer covers these exercised calls without interrupt
nesting. These measurements do not prove physical timing. The generic C52 does
not model the board's USB, flash, DMA, oscillator or interrupt behavior. Matrix
contacts, knob movement, live USB and durable storage need separate checks.

Macro cases publish grammar-checked simulated streams with the logical length
and busy metadata, then call the linked `dynamic_keymap_macro_send`. They check
unmatched UP, 257 duplicate DOWN operations, separate DOWN/UP streams, TAP while
held, and extended MT/LT low-byte actions. Owner counts and actual report traces
must agree. These bounded CPU cases complement the full 8192-byte host cases.

One cancellation case changes one simulated macro DOWN call to a test hook.
The hook calls the original `register_code`, saves bank-0 registers, ACC, B,
DPTR and PSW, calls the real `clear_keyboard`, restores the registers and
returns to the interpreter. The caller's saved r5/r6/r7 sequence identifies
the patch location; a missing or ambiguous match stops the test. The hook
occupies unused simulated ROM at 0x2640..0x267A, outside the call trampoline
at 0x2600..0x2605 and its stop at 0x2700. The image overlap checks still apply.
The result records the original call, replacement, hook bytes and registers.

This models a public clear between the first macro DOWN and the next stream
instruction. The linked code must clear held key, modifier and consumer owners,
stop the stream before its next DOWN, and accept a fresh key after release.
It tests the real clear and interpreter cancellation check. It does not test
EE_CLR, EEPROM reset, reset timing, persistent storage, power-fail behavior or
interrupt overlap. Every other case loads the original image in a separate
simulator process.

The cancellation hook check does not establish a complete suite pass. Current
exact-image results are recorded in the
[development matrix](../../../audits/rc6/compact-runtime-20261024/final/README.md).
