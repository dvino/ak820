# Stack and interrupt checks, 2026-10-24

The compact RGB callback is now resolved from its complete range checks and
ROM table. Its temporary byte must match the unique one-byte `process_rgb`
XSEG allocation. An unrelated or coherently relocated cell cannot grant a
callback target. Every requested root closes in all 18 retained images from
the previous development matrix.

Closing the graph exposed six images whose conservative stack allowance was
larger than the available stack. These are the **previous images**, before the
delay correction:

| Previous build | Complete allowance | Capacity |
| --- | ---: | ---: |
| `standard` | 165 | 162 |
| `nkro` | 166 | 162 |
| `nkro-one-shot` | 163 | 162 |
| `full-gui-lock` | 169 | 166 |
| `full-dynamic-macro-gui` | 169 | 165 |
| `full-mouse-auto-shift-gui --short-calls` | 170 | 166 |

Exact identities and all 18 results are in [baseline-summary.json](baseline-summary.json).
A conservative bound exceeding capacity does not establish that overflow
occurred on a device. It prevents qualification until the bound or code is
corrected.

## Firmware correction

`mDelaymS` uses the callee-save convention. Its call to the previously unlisted
`mDelayuS` preserved all eight registers. The shared header now marks that leaf
callee-save too; SDCC preserves its two changed registers instead. The delay
loop is unchanged. Seven linked CPU cases check register preservation, stack
balance and loop completion. Physical elapsed time is not measured.

The corrected `full` candidate uses 38,924 CODE and 2,607 XRAM bytes. Its
foreground bound is 97 bytes. Adding the two-byte CRT frame and 61 bytes for
all three IRQs gives 160 of 166 bytes, leaving six. The complete [final profile matrix](final/README.md) is being regenerated
from integrated source.

A host debug-loop experiment saved three additional CODE bytes but changed
overlay placement and reduced stack capacity to 163 bytes while requiring
164. It was rejected; the delivered firmware does not contain it.

## Ctrl/GUI development feature

`full-ctrl-gui` adds volatile left/right Ctrl/GUI swapping to `full-gui-lock`.
The output mapping precedes GUI lock and preserves raw modifier ownership.
It uses no NVM record and keeps schema `0x082002`. Host checks cover all
keycodes and modifier masks; eight linked cases cover held keys, mode changes,
One Shot, Mod-Tap, report modes, Repeat and built-in macros.

Independent review found that the early One Shot handler consumed queued
modifiers on a Ctrl/GUI control and marked held One Shot keys used. An exact,
feature-guarded bypass fixes both cases. The corrected CPU tests fully release
the control before consuming the queued modifier; a held One Shot case checks
that release still queues it. Earlier case failures from inactive fixture
coordinates were corrected without weakening their expected reports.

The integrated image uses 39,302 CODE and 2,610 XRAM bytes. Its foreground
bound is 101 bytes; CRT and IRQ use bring the total to 164 of 166 bytes.
It passes the runtime gate before all 28 base suites, 273 base unit tests
without skips and 25 supplemental suites. Its [candidate evidence](integrated-ctrl-gui/record.json)
retains the exact artifacts and raw build. The private state bit and
exact feature flags must agree with the selected profile; the shared GUI
handler alone cannot establish that swapping is present.

## Interrupts and repeatable checks

The Timer0, USB and LED callbacks require 2, 6 and 2 bytes. Each OEM wrapper
adds 17 bytes: the hardware return frame, saved registers and callback call.
All three sources therefore require at most 61 bytes together. The model
executes all 15 nonempty source orders and all 256 LED selector values.

The public fixture contains only 234 actual wrapper/helper instruction bytes
from retained alpha.3 evidence. Independent hashes and addresses are pinned.
Changing any instruction byte is rejected even with a rewritten checksum.
The private-ROM route and the packer's complete native-image validation remain
unchanged.

`configure_firmware.py build` now runs the combined check before regression
suites. [check-runtime](../../../docs/RUNTIME-STACK.md) can repeat it on an
existing build. It recomputes each component, binds image/MAP/MEM and checker
identities, checks stack capacity and records failed arithmetic as a failure.
Missing paths never use the partial explored peak as an upper bound. The
checkers run with Python environment flags isolated; proof sources are checked
again after the regression suites.

## Review and evidence

- [ISR source audit](reviews/isr-source.json): architectural contract, shared storage and IRQ masking.
- [Analyzer review](reviews/stack-analyzer.json): 32 independent unit checks; local-spill finding closed.
- [Delay ABI review](reviews/delay-abi.json): seven independent CPU cases; rejected overlay experiment.
- [Runtime combiner review](reviews/runtime-core.json): original nine arithmetic/identity tests and 25 configurator tests.
- [Ctrl/GUI and integration review](reviews/ctrl-gui-integration.json): One Shot correction, feature checks, final source recheck and 28 configurator tests; the subsequent checkpoint review covers integrated documentation and candidate evidence.
- [Implementation checkpoint review](reviews/implementation-checkpoint.json): source/document agreement and full integrated candidate qualification. The clean-source matrix receives separate final review.

The first complete base-regression attempt failed only because LeakSanitizer
could not inspect its own process under the execution sandbox. The same RGB
harness passed without that restriction and with leak detection enabled.
The [failed base report](initial-base-attempt/qualification-failed.json),
[sandbox failure](initial-base-attempt/rgb-sandbox-failure.log) and
[successful RGB rerun](initial-base-attempt/rgb-completed.log) remain distinct
from subsequent final qualification.

## Proof boundary

The application bound begins at CRT entry with `IE=IE_EX=0`, supplied by the
packer. It assumes valid C memory, the normal SDCC bank-0 ABI and MCS-51
in-service/RETI behavior. All three distinct interrupt sources are included;
no particular number of hardware priority levels is assumed. IRQ allocation
checks establish that interrupt storage does not overlap the local RGB spill.

Pre-CRT trial erase, VS11 peripheral timing, physical scanning, USB delivery,
flash endurance and power-loss behavior remain separate. No device commands
were sent. The published and installed alpha.3 image is unchanged. Passing
this check does not change release policy or approve an installer transition.

The calling-convention and interrupt premises follow the
[SDCC manual](https://sdcc.sourceforge.net/doc/sdccman.pdf) and the
[Intel MCS-51 manual](https://bitsavers.trailing-edge.com/components/intel/8051/MCS-51_Users_Manual_Feb94.pdf).
