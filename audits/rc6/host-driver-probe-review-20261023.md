# Host-driver pointer probe review, 2026-10-23

Independent reviewer: optimization-sources agent. Author: optimization_inventory.
Scope: `.build/rc6-host-driver-probe-20261023/` under `qmk-8051-ak820`, current
host API/source, saved baseline constructor assembly and probe provenance.
No production file was changed. No build or device operation was run.

**Decision: GO for an isolated full-link experiment.** There is no blocking
finding for that experiment. This is not approval to promote or flash it.

## Evidence checked

- The report's source SHA256 matches current `tmk_core/protocol/host.c`.
  Both variants' ASM/REL hashes match their saved files. Both compile logs are
  empty and report successful exit. The command uses the pinned SDCC 4.4.0
  path and the saved baseline flags, including large memory model, board
  configuration and the same callee-saves list.
- Independently counted raw CSEG: control `0x2D5` (725), candidate `0x297`
  (663), delta -62. Generic helper transfers count 13 versus 3. Candidate
  `_driver` reserves two XRAM bytes versus the control's three. These are
  translation-unit facts before reachability, outlining, final placement and
  packing; they are not linked CODE/XRAM savings.
- `control_asm_matches_saved` is false because the copied source has a
  different path in source comments. Removing ASM comment lines yields
  identical control and saved-baseline ASM. This review did not silently
  reinterpret the report's exact-byte comparison as true.

## Pointer and ABI contract

Only the board's private stored driver pointer changes to XDATA. Public
`host_set_driver(host_driver_t *)` and `host_get_driver(void)` signatures and
`host_driver_t` callback types remain generic and unchanged. Other boards
retain the original private pointer.

The saved active AK820 constructor is `ch555_usb_stack_driver`, a non-const
eight-byte object in XISEG (XDATA). `protocol_post_init` passes its address
with generic tag B=0. The candidate setter stores the address bytes and
discards the tag. Its getter reconstructs the address with B=0. This is valid
for that constructor; the cast would be invalid for a later CODE/IDATA driver.
No cast drops a const qualifier here. Do not change the callback parameter
types or table placement as part of this experiment.

The candidate tests the two address bytes for null before table access.
Setter conversion of ordinary null (zero address) remains zero; getter
returns zero address with XDATA tag zero. The general command module has a
save/null/restore pattern, but the active baseline ASM inventory contains
only the AK820 initialization setter reference. Recheck the full-link
reachable graph instead of relying on a whole-tree caller search.

Callback table entries remain two-byte code function pointers. Candidate
`host_keyboard_leds` reads them through MOVX and calls through
`__sdcc_call_dptr`; the return remains in DPL. Public report arguments are
unchanged generic pointers. The remaining generic helpers occur in report
access, not private driver-table lookup. These observations support the
pointer-space change; they are not an execution test of all callbacks.

Initialization happens in the main path after `ak820_nvm_end`. The glue says
report generation remains outside the USB interrupt; saved baseline ASM has
no other setter/getter caller. No new shared mutable field or ISR write is
introduced. Pointer updates are still multiple byte operations, so this
review does not claim atomic replacement if a future interrupt starts using
or replacing the driver.

## Gates for the next experiment

1. Build clean control and candidate images from the same exact inputs.
   Keep production untouched and preserve source/command/artifact hashes.
2. Recheck every reachable setter caller and the constructor's final XDATA
   location. Stop if a non-XDATA driver or concurrent replacement exists.
3. Compare final CODE in both windows, XRAM, stack, retained roots and packed
   boundaries. Stop at no net benefit or incomplete relocation/ABI proof.
4. Run offline linked checks for initial null, set/get, null/restore and each
   supported callback, including report byte equality and return/register
   preservation. Confirm existing keyboard/NKRO, mouse configuration and
   system/consumer behavior remain equivalent.

The probe report does not snapshot hashes for all included headers or record
an executable version banner. The parent baseline's provenance and full-link
input snapshot must close that gap before accepting a final saving. It is
not a blocker to preparing the controlled full-link comparison.

No device behavior, USB timing, physical input or durable-storage behavior
was established by this review.

## Full-link follow-up

**Decision: GO for source integration of the exact board-guarded private
pointer change reviewed above.** No blocking code finding remains. This
decision does not approve a packed image, installation, commit or device
operation. Breathing behavior itself needs its separate review.

Read `link_probe.py`, `combined_probe.py`, `host_cpu.py`, both linked reports,
MAPs and saved CPU results. The pipeline reconstructs frozen baseline ASM,
substitutes only the host ASM (and RGB ASM for the combined control), reruns
the existing reachability pass, assembly, exact outlining, assembly and link.
This is not a fresh full production build. The reconstructed control IHX is
byte-for-byte equal to the baseline; independently recomputed SHA256:
`d2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce`.
That exact control closes the relevant pipeline comparison concern.

| Frozen linked variant | CODE total / main / low | XRAM | Stack capacity | IHX SHA256 |
| --- | --- | --- | --- | --- |
| Control | 39,347 / 37,488 / 1,859 | 2,071 | 152 | `d2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce` |
| Host pointer | 39,298 / 37,439 / 1,859 | 2,070 | 152 | `319824985e75b636c0f4dc433d7fa4602f2d86f24ea76166b3c1c273ae057871` |
| Host pointer plus current RGB | 39,432 / 37,573 / 1,859 | 2,071 | 152 | `ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837` |

All three IHX hashes and address counts were independently recomputed. All
occupied bytes fit `[0x28A0,0x3000)` or `[0x3027,0xC700)`; the low range has
29 free bytes. Host-only saves 49 linked CODE bytes and one XRAM byte against
the exact baseline. Combined is 85 CODE bytes larger than baseline and uses
the same XRAM: the host saving does not make Breathing free. Its main range
has 1,044 free bytes, total 1,073. These are linked application figures before
image packing.

MAP places the eight-byte driver table in XISEG at `0x0BA2` host-only and
`0x0BA3` combined. Both remain XDATA within the allowed range. The reachable
constructor call remains in `protocol_post_init`; no new setter caller is
introduced by this substitution. `host_get_driver` is removed by DCE in all
three images: its generic return conversion has translation-unit ASM proof,
not a linked CPU execution result. Do not describe the focused tests as
testing that removed getter.

The combined source snapshot records only `ak820_rgb.c` differing from the
baseline input manifest; its saved source and snapshot hashes agree. The
combined generator explicitly compiles that snapshot and substitutes it.
The report's inherited `production_changes_included=false` is misleading
without qualification because it includes the current RGB change. This
wording correction was requested from the author; it does not invalidate
the explicit source hashes, script or linked bytes. It must not be read as
proof that combined is host-only.

Saved CPU evidence, with matching linked image hashes:

- Host-only: emitted 3/3, feature 33/33 and corrected focused host 18/18 PASS.
- Combined: emitted 3/3 and focused host 18/18 PASS.
- Focused host covers null suppression, LED callback return, keyboard pointer
  tag/payload, system/consumer duplicate suppression, changed payload/release
  and restoration to the real table. It uses simulated callbacks and memory.
- The original focused run is retained as FAIL. Its three wrong expectations
  used report IDs 2/3 instead of 3/4. The corrected fixture uses the current
  report IDs; this was a test expectation correction, not a production fix.

The focused fixture does not exercise a mouse callback (disabled in this
configuration), every possible keyboard report or arbitrary interrupt overlap.
Its executed-path stack observations are not a worst-case IRQ stack proof.
The unchanged callback API, table layout, constructor space, emitted call
shape and tested paths are sufficient for this bounded source integration.
After integration, run the normal production builder and affected offline
checks before claiming production artifacts match this reconstruction.
