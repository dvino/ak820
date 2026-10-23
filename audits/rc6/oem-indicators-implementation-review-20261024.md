# Indicator implementation review

The bounded source and emitted-code review found no blocking implementation or
ABI defect. The candidate was not installed or tested on hardware. Final
integration approval still requires the matching documentation, full regression
suite and package checks.

The reviewed source is in the isolated worktree
`/home/danil/.codex/worktrees/ak820-oem-indicators/ak820`, based on `586ac20`.
The linked image `.build/indicators-fitcheck/ajazz_ak820_vial.ihx` has SHA256
`45f28e80cd9e269cb507d6fff47b43cea2766b00967912599a98b036b638011d`.
The review covers `ak820_indicators.c`, its declaration and build inclusion,
the `protocol_post_task` call, and the added RGB CPU fixtures.

The emitted helper occupies 76 bytes at `0x28A0..0x28EB`. It makes no calls
and adds no register saves or local stack allocation. R5–R7, ACC, carry and
DPTR are ordinary caller-clobbered registers. The protocol task ends with
`LJMP 0x28A0`; the helper returns through the task's existing return address.
No caller value remains live after that jump. The IRQ snapshot uses allocated
BSEG bit `0x01`, not an XRAM parameter or a fixed register. Existing loader
IRQ wrappers preserve the register context; the scan callback calls no C
helper. The helper is called only from the main protocol task and is not
reentrant. No IRQ implementation changed.

Exactly four MOVX stores write `0x031C`, `0x031D`, `0x033C` and `0x033D`.
These are intensity and component 1 of slots 71 and 79 within the 512-byte
DMA buffer at `0x0200`. Components 2 and 3 remain unchanged. The current
82-entry RGB slot map excludes both slots. The scan interrupt is masked before
the four stores and its previous enable bit is restored afterwards. USB stays
enabled. A USB state change during the short helper can be reflected on the
next main-loop iteration; this is not an atomic USB-state snapshot.

Caps follows bit 1 of `KB_USB_SetReport`. The layer expression includes both
active and default layer state and excludes only base-layer bit zero. The
linked expression is a byte OR followed by AND `0xFE`, matching the configured
8-bit layer type. Held, toggled and TriLayer results are visible through that
state; this helper does not independently process those actions. Unconfigured
or suspended USB makes both owned channels zero. Resume reads retained host
and layer state again. The USB reset path clears the host report and USB
configuration. Generic LED hooks and existing RGB features remain unchanged.

An independent run used:

```sh
cd /home/danil/.codex/worktrees/ak820-oem-indicators/ak820/qmk-8051-ak820
python3 tests/ak820_rgb/emitted.py --build-dir .build/indicators-fitcheck --s51 /home/danil/Documents/git/ak820/toolchains/sdcc-4.6.0/bin/s51 --output-dir .build/indicators-fitcheck/independent-indicators-review
```

The result is PASS for 12 reactive observations and eight indicator cases.
The latter cover Caps, active and default non-base layers, zero host LED state,
suspend, resume, reset/unconfigured and disconnected state. Both interrupt
enable values and preservation of the other two slot components are checked.
The helper fixture uses four tested stack bytes; the reactive fixture uses 23.
These are linked C52 CPU models with injected state. They do not execute a
CapsWord action, TriLayer key sequence or USB output-report transaction.

The physical C/W connection, visible brightness, polarity, interrupt timing
and device behavior remain unverified. The OEM source supports the selected
slot/component candidates; W as a non-base-layer indication is the requested
project behavior, not a claim that it matches the OEM lock state. This review
does not claim an installed change or authorize a live operation.

The earlier OEM trace's instruction to establish the physical connection before
changing code needs a dated status correction in integration: the candidate is
authorized from source, while physical mapping remains an explicit test limit.
The integrated README, STATUS, policy and package evidence have not yet been
reviewed here. No commit, USB command, reset or flash was performed.

## Final fixture closure, 2026-10-24

The final test revision supersedes the eight-case run above. A second independent
run used the same command with output directory
`.build/indicators-fitcheck/independent-indicators-final`. It passed all 12 RGB
observations and 11 indicator cases against the unchanged image SHA256
`45f28e80cd9e269cb507d6fff47b43cea2766b00967912599a98b036b638011d`.

The added coverage calls the linked production `layer_on`, `layer_off` and
`default_layer_set` functions. Two successive `layer_on` calls also pass through
the production TriLayer state calculation before indicator refresh. The
indicator assertion checks the resulting non-base indication; it does not
separately assert the derived layer bit or a physical key sequence. Host values
`0xFF` and `0xFD` verify that unrelated LED report bits do not control Caps.
The indicator fixture now uses seven tested stack bytes because it includes
layer API calls. The reactive fixture remains at 23. The helper itself remains
the same 76-byte leaf reviewed above.

The new translation unit's license header is now `GPL-3.0-only`. This comment
correction changes no emitted instruction. No additional implementation finding
was identified. Integration documentation, full-suite and package review remain
separate pending checks; no device behavior is claimed.
