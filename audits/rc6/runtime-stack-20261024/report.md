# Runtime stack analysis, 2026-10-24

The exact development baseline has two closed application callback bounds:
timer uses at most 2 control-stack bytes and USB uses at most 6. The foreground
and LED callback remain unbounded by this analyzer. No installation or release
approval follows from this result.

## Exact input and results

The analyzed build is `qmk-8051-ak820/.build/baseline-dev`, produced from the
development configuration beginning at commit `48ce5fa`. Its IHX SHA256 is
`004bf2cbda40f9c90ab92e0ee6b6a29bc2098e39d5ee8bc6d0da5df638f2565a`.
[baseline.json](baseline.json) contains MAP, listing and analyzer hashes,
reachable instruction addresses and all unresolved paths.

| Root | Application control-stack bound | Remaining issue |
| --- | ---: | --- |
| `_main` | Unknown | Recursive input paths and indirect callbacks. The explored peak is 69 bytes, not an upper bound. |
| `_ak820_timer_irq` | 2 bytes | Hardware wrapper, routing and shared-state contract are separate. |
| `_USB_DeviceInterrupt` | 6 bytes | Hardware wrapper, routing and shared-state contract are separate. |
| `_ak820_led_irq` | Unknown | Selector register invariant is not encoded in the analyzer. |

The existing OEM wrapper check accounts for 17 bytes: hardware return address,
13 saved register bytes and the callback call's return address. Adding that
checked wrapper cost gives conditional totals of 19 timer bytes and 23 USB
bytes. These totals assume the checked OEM wrapper and callback routing. No
combined foreground/IRQ margin can be stated while foreground and LED paths
remain open. The existing two-priority-level nesting assumption still needs
the VS11 interrupt contract; a generic C52 model does not establish it.

The USB graph closes two formerly assumed switch transfers. At `0x5c68`, the
complete subtraction/range guard and split low/high table lookup selects only
12 entries. At `0x5aca`, the carry guard and doubled index select four adjacent
SJMP entries. The analyzer checks both complete instruction idioms and every
target byte against the IHX. Both range outcomes are explored. Constant SP
increments/decrements are also tracked instead of being rejected wholesale.

## Foreground blockers

The emitted graph has cycles through `_process_record_quantum`, Repeat,
`_repeat_key_invoke` and `_process_record`, plus paths through Vial macro
playback, virtual key injection and `_ak820_combo_tick`. These are graph cycles,
not evidence of unlimited feasible recursion: input ownership and cancellation
state may bound them. A proof must encode those state transitions or provide a
reviewed recursion-depth contract. Treating the cycle as a leaf would hide live
frames and undercount stack use.

Concrete guard candidates already exist: `process_repeat_key` bypasses Repeat
invocation while `get_repeat_key_count()` is nonzero; macro playback rejects
entry while its static `sending` flag is set; Combo `flush` clears `first`
before calling `process_record`. These explain why an unconstrained graph can
overstate recursion. They do not by themselves establish a numeric nested-frame
bound across all mixed Repeat/macro/Combo paths or prove that reentered SDCC
static parameter slots remain intact. The linked guards and their write order
must enter the model together.

Unbalanced returns at `0x6bcd` and `0x6c29` are compiler
indirect-call thunks. A local CALL pushes its continuation; the thunk pushes a
function address and RET transfers to that address. These need typed, finite
callback targets and argument-cleanup summaries, rather than a normal balanced
function-return rule. Their current rejection identifies an analyzer limitation,
not a demonstrated firmware fault.

The const RGB driver table supplies finite targets. Its eight IHX bytes at
`0xbcb4` encode `init=0x33df`,
`set_color=0x33e0`, `set_color_all=0x3425` and `flush=0x3461`. Their entry bounds
are respectively 0, 5, 13 and 0 bytes. The machine report records each raw
slot/target and target-entry analysis. Bounded value tracking now connects the
RGB callers' MOVC loads through register saves to RET thunks at `0x4f8e` and
`0x4fc6`. Each pointer byte retains its exact ROM address. Call-return bytes
carry separate provenance; the pushed pointer is consumed by RET while the
original call frame remains. No target allowlist substitutes for those loads.
The single-color sequence beginning at `0x4f62` has a local peak of 11 bytes
and 7 bytes live at callback entry; adding the callback bound gives 12. The
all-color sequence beginning at `0x4fa0` peaks locally at 8 and has 6 live at
entry; its callback raises the total to 19. These numbers start at those
sequences, not at main. Unknown instructions or values reject the recognizer.
Normal SDCC bank-0 execution is assumed; arbitrary register-bank states are
not supported. Host callbacks from RAM and remaining indirect calls stay open.

The analyzer now decodes unlisted runtime-library instructions directly from
the IHX with the existing 8051 opcode-length table. Boundaries cannot be inferred
from arbitrary listing row lengths, and overlapping entries fail closed.
`___gptr_cmp` at `0x3077`, memcpy at `0xbb59` and memset at `0xbbcf` each have
a control-stack bound of 2 bytes. Generic pointer get/put and multiplication
helpers at `0xbbf7`, `0xbc12` and `0xbc32` each use zero additional control-stack
bytes. These results close the listing gaps; they do not prove pointer safety
or preserved registers. `__sdcc_call_dptr` at `0x3075` decodes to an indirect
transfer and remains unresolved until its DPTR target set is proved.
Additional indirect dispatches remain in GPIO, action handling,
USB send, HSV conversion, RGB processing and Vial command handling; their exact
addresses are in the machine report.

## LED selector and interrupt sharing

LED dispatch at `0x32c4` triples A and jumps into sixteen CLR-bit/RET entries.
The immediately preceding JBC clears bit 4, without masking bits 5..7. The old
IRQ model assumed a valid table index. The source supplies a candidate invariant:
board initialization sets `LED_COMMON` (SFR `0xa6`) to `0xff`; the callback
increments it and writes `0x10` whenever the low nibble becomes zero, before
calling the selector. Thus the selector sees `0x10..0x1f` after the first IRQ,
provided the peripheral and other code do not modify this register and the
callback cannot reenter itself. Clearing bit 4 then produces `0..15`. No bad
index is demonstrated and no masking change is justified from this analysis.
The initialization, register ownership and non-reentry assumptions must be
made explicit before accepting the LED table's bound.

Observed foreground/IRQ code sharing is concrete: timer shares `timer_reload`;
USB shares `endpoints_reset` and `raw_abort`. Source inspection shows
`timer_init` masks EA around timer setup, and `USB_Device_Init` clears IE_USB
before those shared USB helpers. These are candidate exclusion arguments, not
a complete interrupt-state proof. The USB source comment now includes the
masked initialization call. USB's `#pragma nooverlay` gives
its static temporaries private allocation; it does not make those functions
reentrant or prove that every interrupt state is safe.

The existing callee-save CPU suite checks eleven selected source functions.
It deliberately excludes naked helpers and prebuilt runtime functions, so its
pass cannot establish whole-image ABI preservation. OEM wrapper register
restoration, shared non-reentrant temporaries and overlay allocation still need
review against all enabled interrupt priorities and the resolved call graph.

## Verification and next work

Seventeen focused unit tests pass, including call/return costs, tail transfers,
ACALL/AJMP, balanced loops, SP adjustment, recursion, malformed/checksum/overlap
IHX rejection, listing mismatch, and mutations of both bounded-switch idioms.
ROM thunk controls replace MOVC with unknown RAM reads, change pointer-register
provenance and reverse pointer pushes; all fail closed. Changing the actual ROM
pointer reaches a different, deeper callback and increases the computed bound.
The exact baseline command exits 2 as intended because unresolved roots remain.
All work is offline; no device access, reset, flash or physical timing test
occurred.

Next, resolve finite indirect callback tables and their ABI contracts; encode
the LED register invariant; bound input-pipeline cycles using actual ownership
state; then combine startup, foreground, wrappers and permitted IRQ nests.
Memory writes through generic pointers and all shared static temporaries need
separate safety checks before interpreting a control-stack bound as a complete
stack integrity proof. Packaging must remain blocked.

Initial independent review required opcode-length validation, overlapping-entry
rejection, direct-image runtime decoding, DJNZ-SP handling, a split-table
POP/index alias check and explicit analysis limits. Those corrections are in
the analyzer and negative tests; the baseline was regenerated afterward.
Independent second review approved the analyzer, ROM thunk recognizer, USB
comment, documentation and baseline evidence without further findings. All
17 tests passed independently. A separate baseline regeneration matched the
full recorded JSON exactly. This approval covers the analysis implementation
and its stated limits; it does not approve firmware installation or release.
