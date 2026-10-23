Русский перевод: [Планы](ru/ROADMAP.md).

## Installer backup/restore plan, 2026-10-23

Implement preservation later in the PC installer only: export a verified local backup, flash once, restore with existing Vial commands and read back. No firmware freeze/token/import protocol. The as-is console flash with package defaults is complete; its backup is evidence, not an automatic restore. Detailed implementation: [host-only plan](../audits/rc6/general-update-implementation-plan-20261023.md).

# Roadmap

## Current priorities — 2026-10-23

SDCC 4.6 RC6 with smoother Breathing and the reviewed optimizations is installed. Full readback and read-only device tests passed; physical typing was confirmed separately. Current implementation evidence is in [Status](STATUS.md). Preserve the existing 38100-byte CODE image; no firmware backup protocol is included.

Local settings export and restoration are deferred PC-installer work. Implement the shared Windows GUI/CLI and Linux/WSL path in the [host-only plan](../audits/rc6/general-update-implementation-plan-20261023.md). Current as-is flashing uses package defaults, with a separate local backup and no restoration.

Direct Control remains research-only and cannot be removed without permission. Indicators, Caps language switching, the Windows helper, physical persistence tests and further optimizations remain deferred. Reactive lighting worked normally before this update; appearance on the new image is not yet confirmed.

SDCC bool near-pointer fixtures still fail two of sixteen cases on both compilers. No affected shape was found in the reviewed current image; rebuild/backport the compiler only if an affected retained path is identified. Keep the documented negative result.

### Future optimization research

Deep local and compiler research remains future work after current 4.6.0 release
review and preparation.
The [analysis](../audits/rc6/optimization-deep-analysis-20261023.md),
[local inventory](../audits/rc6/optimization-deep-local-20261023.md),
[SDCC research](../audits/rc6/optimization-deep-sdcc-research-20261023.md)
and [independent review](../audits/rc6/optimization-deep-review-20261023.md)
record evidence and limits. The ranked bounded probes are:

1. Test a private XDATA pointer for the NVM journal header.
2. Test a bounded replacement for the macro delay multiply by 255.
3. Consider a typed private event pointer only after every event origin and
   record placement is proved; preserve the public ABI.
4. Inspect one repeated protocol field decode or response tail at a time.
5. Try typed leaf copies only where address space, range and callers are proved.
6. Consider a bounded peephole rule only with instruction-level proofs and a
   complete controlled link.
7. Short calls are blocked: the fixture run stopped after six of 42 cases when
   the linker crashed on an invalid destination. The remaining cases and valid
   boundary behavior are unproved. Do not count short calls as available bytes.

None of these probes has a promised saving. Do not set a target such as 1 KB;
accept a future change only after its actual linked benefit and behavior checks
are measured. Preserve the detailed stop conditions in the linked audits.

## Earlier SDCC 4.4 checkpoint — historical, 2026-10-23

The previous work package ended with a firmware candidate, its device tests
and an independently checked handoff. Local work continues under the priorities
above. Git integration and publication remain out of scope.

- [x] Record the RC6 encoder-write failure and preserve the personal recovery
  data. Startup, typing and one cold power cycle passed before the failed write.
- [x] Add the automatic nonphysical test runner and its 19 offline regressions;
  complete independent review. Macro uploads and durable RGB save remain
  explicit skips in the live runner.
- [x] Add the linked CPU regression for unchanged target data, no ACK, retained
  committed journal and failed replay. This is a conditional failure model.
- [x] Implement one bounded erase/write-path correction, with erase readback
  and useful fault evidence. Preserve the format, protected areas and intended
  original encoder mapping; do not replay the temporary KC_NO into the image.
- [x] Build a fresh candidate, inspect its emitted instructions and resource
  limits, run the affected tests and close independent review findings.
- [x] Finish the integrated RU/EN GUI and independently check its update path for an installed
  Vial image. The flash was performed through the new GUI after confirmation.
- [x] Assemble and verify its exact release and personal recovery session.
  Obtain explicit confirmation immediately before any flash.
- [x] Flash once after confirmation, verify startup and full readback, then
  run the automatic nonphysical tests. Record every failure and skip; do not
  retry, reset or restore blindly.
- [x] Update status and write the external handoff with exact paths, hashes,
  evidence, remaining work and stop conditions. Obtain independent handoff
  review and close its findings before delivery.

Current step: the candidate was installed through the integrated RU/EN GUI.
Startup, full ROM and read-only tests passed. With separate consent,
six key, twelve encoder and one RGB RAM round trip passed; all settings were
restored. Independent device review passed. The external handoff and its
independent review are complete, with no open findings. No commit or publication was made.

### Requirements for the next agent

These requirements remain in the plan. The current priorities above decide
which ones to work on now; their evidence and stop conditions still apply.

- Deferred: add a modal unlock popup: show the key hold, close after unlock, and stop
  before erase when Cancel is clicked.
- General updates must preserve the latest supported keyboard settings from
  a fresh snapshot, rather than reusing an earlier prepared settings image.
- Make Breathing smoother. Visible jumps from large brightness steps were
  reported. Check the step, update interval, visual result on the
  keyboard, memory cost and processing time.
- Research feasibility only for now. The eventual Direct Control goal is a usable per-LED editor,
  explicit palette save and restore after restart. Investigate the shown Vial
  Web client, which has no visible per-LED editor. If a working implementation
  cannot be delivered, obtain explicit permission before removing
  the effect from available modes rather than
  presenting protocol-only RAM support as a finished feature.

### Current goal additions — 2026-10-23

These additions remain planned but are deferred by the current priorities
above. Recording them does not authorize implementation or device writes.

- [ ] Keep C as the actual Caps Lock indicator, using the state from Windows.
- [ ] Use W to indicate an active additional layer: off on the main layer,
  on when an additional layer is active. It no longer indicates Win lock.
- [ ] Make the Caps key switch the Windows input language; Shift+Caps toggles
  actual Caps Lock without switching language. Choose and document the Windows
  shortcut before implementation. Handle both Shift keys, held modifiers and
  releases correctly; preserve remapping through Vial. Prefer a small firmware
  change and measure its linked CODE/XRAM cost. Test event handling offline;
  those tests do not prove Windows behavior or visible LEDs on the keyboard.

Deferred Windows software:

- [ ] Plan a small helper that reports the actual active-window input language
  to OS: Russian on, English off. It may extend the existing AutoHotkey script.
  Handle window changes, other language-switch methods and missing helper
  updates. Define unknown-state behavior before implementation. Do not infer
  the language by counting Caps presses or write flash for status updates.
  This helper and OS language indication are deferred, not part of the current
  firmware implementation work.

## Longer-term plan

This page lists work that remains. For what has already been built, packaged,
installed or checked, see [current status](STATUS.md). The prior offline
baseline was the final RC6 image after the layout change, SHA-256
`7c25096e59412afc7a4aa1c030a7038c4b5d469a253319ef712ce4244c91ffb9`.
It uses 39,282 of 40,505 bytes of program memory (CODE). The remaining 1,223
bytes are split between two address ranges: 1,194 in the main range and 29 in
the lower range. It uses 2,071 of 3,072 bytes of working memory (XRAM), and the
linker allocated a 153-byte stack. These are measurements of the built image,
not tests on a keyboard. The image already includes reactive lighting, Alt
Repeat, the NVM fix and compact CIE; the remaining work for those features is
listed below as testing.

## Previous release checklist

The following checklist records work on the installed SDCC 4.4.0 candidate.
The previous image's `target_write` failure remains a regression. The next
agent should follow the current priorities above. The popup and release work
below are deferred, with new review and approval required before another flash.

1. The current SDCC 4.6.0 Windows GUI and command-line package is assembled and
   checked locally. No public download is available. Publication requires
   approval, and each operation that writes to a keyboard requires confirmation.
   Permission to read the keyboard does not include permission to flash it.
2. Deferred: check Alt Repeat and saved settings on the keyboard. Reactive
   lighting previously worked normally.
   Include a cold start, restart, power loss and recovery. Say how each result
   was checked: by reading code, running a computer model, building offline or
   testing a keyboard. A result from one kind of check does not prove another.
3. Keep six layers unless a separately reviewed storage design proves a
   worthwhile, compatible result. Four layers have measured zero CODE and
   XRAM savings and free 520 logical NVM bytes only; moving the encoder base
   requires schema migration. Keep the existing 16-macro capacity unless an
   explicitly approved product trade changes it.

## Future work: bounded code-space experiments

The experiments below are future research only. They do not replace the current
SDCC 4.6.0 qualification and release task, and they do not authorize another
optimization implementation now.

The remaining CODE headroom is small and split between two placement windows.
Every experiment must start from a fresh copy of the same baseline and report
the complete linked image, both window usages, XRAM, stack, IHX hash and
behavior checks. A source-level estimate or candidate count is not a saving.
Keep each probe isolated; reject a candidate that loses a required behavior,
violates an ABI/memory contract, increases risk beyond its measured benefit,
or cannot fit the linker/packer windows. Preserve the existing six-layer and
macro feature contracts unless a separately approved design changes them.

| Order / work item | Resource target and evidence today | Dependencies and acceptance / stop rule |
| --- | --- | --- |
| P1.1 Typed pointers and shared protocol tails | CODE hypothesis; current inventory counts 57 generic-pointer call sites. Earlier controlled probes found some useful small savings, but results depend on ABI and call shape. XRAM/stack may move. | Rank call sites and common tails from fresh relocated MAP/ASM, then change one bounded group per clean build. Verify pointer address spaces, return values, register/stack preservation, protocol boundary cases and linked deltas. Stop when measured savings are zero/negative or correctness/ABI proof is incomplete. |
| P1.2 Whole-image hotspot and repeated-work pass | CODE hypothesis; historical RC5 function sizes are not a ranking for this RC6 image. | Regenerate a current linked MAP/ASM call-graph and emitted-size/hot-path ranking. Examine repeated work, common tails, branch structure and removable unreachable work, including DCE roots and retained OEM hooks. Do not remove or rewrite startup/IRQ hooks or protocol/NVM checks without a separate safety contract. Require complete linked and behavior evidence; stop at no measured win or any lost contract. |
| P1.3 Relocation-aware ACALL/AJMP | CODE hypothesis. A previous inventory found 1,317 long transfers, of which 531 were one-byte page candidates at that layout (285 LCALL, 246 LJMP). This is neither an implementation nor a guaranteed saving. | First implement a separate relocation/layout-aware prototype. Recheck every relocation, page boundary and final packed image after placement changes; test control flow and linked bytes. Stop if relocation provenance or exhaustive post-layout validation is unavailable. |
| P1.4 Callee-save, inlining and call-graph variants | CODE hypothesis with possible RAM/stack and placement costs. The selected current callees are already measured features of the baseline, not a future task. | Explore only candidate extensions or isolated compiler controls against the final linked caller/callee graph. Preserve register-bank/ABI contracts; measure worst relevant stack paths and both placement windows. Accept only a reproducible net improvement with equivalent execution. |
| P1.5 Narrow arithmetic/timer/decoder experiments | CODE hypothesis, potentially changing timing or state behavior. Prior exact decoder, RGB arithmetic and repeated-computation improvements are already in the build. | Use the current assembly and execution profile to identify a specific unmeasured operation; exhaustively compare finite domains where possible and run linked CPU/host traces. Stop if it duplicates existing work, cannot be bounded, changes output/timing contract, or gives no linked gain. |
| P1.6 RGB Direct representation | RAM opportunity only: packing Direct HSV has been estimated to save 82 RAM bytes, but adds conversion CODE and color loss. Do not claim CODE savings. | Define acceptable color error and wire/NVM compatibility first. Compare exact linked CODE/XRAM/stack and full RGB output domain or a justified error bound. Reject if conversion consumes the scarce CODE margin or color loss is unacceptable. |

## Future work: research beyond the completed optimization audits

The known option registry is **not an exhaustive search of every possible
optimization**. The 57 generic-pointer sites and the 531 short-transfer
candidates describe specific inventories, not all potential improvements.
Before proposing broad implementation, run a bounded discovery phase and
append its evidence and accepted/rejected candidates to this roadmap:

1. Rebuild a complete active-source and linked call-graph inventory from the
   exact current source, build inputs, MAP, relocated ASM/listings and DCE
   report. Rank emitted size and repeated work by the final linked image, not
   historical RC5 function sizes. Include code outside obvious hot functions
   and inspect boundaries between modules.
2. Independently repeat the search from a different angle: inspect state
   machines, protocol dispatch, cross-module algorithms and data
   representations for alternate algorithms, shared tails, redundant state,
   or repeated computation. Do not assume an attractive C rewrite shrinks 8051
   output. Record false starts and duplicate findings.
3. Compare compiler versions, flags, ABI choices and targeted optimizer
   controls only as isolated controls. SDCC 4.5 previously failed in compiler
   optimization at `usb_ak820.c` (`validateOpType` / `OP_USES`,
   `SDCCopt.c:2823`); it produced no usable linked image. Compatibility work
   must first yield a correct build before size comparisons. Keep production
   pinned to SDCC 4.4.0 until a replacement is fully qualified.
4. Where a reproducible execution profile exists, use it to direct performance
   and timing analysis. Inspect cycle counts, interrupt/USB timing and stack
   depth alongside CODE; do not infer runtime value from source length or CODE
   reduction alone. A functional simulation is not hardware timing evidence.
5. For each candidate, record: source/linked location, hypothesis, expected
   CODE/RAM/NVM/timing effects, existing evidence, required controlled probe,
   acceptance checks, and the reason for acceptance or rejection. Refresh the
   plan from this inventory. Bound discovery to the current active image and
   its reachable build inputs; make no claim that every possible optimization
   has been found.

### External research workstream

The discovery pass also includes a thorough, source-backed web search; local
code inspection alone is not enough. Begin with primary references and keep a
curated reading list with the question each source answers, the relevant
revision/date, and applicability limits. Initial seed references checked on
2026-10-23 (this is a starting set, not completed exhaustive research):

- [SDCC Compiler User Guide](https://sdcc.sourceforge.net/doc/sdccman.pdf):
  MCS-51 memory spaces and generic versus typed pointers; calling convention,
  callee-saves, optimizer options, assembler/linker and relocation behavior.
- [SDCC release history](https://sdcc.sourceforge.net/previous.php):
  version-specific feature and compatibility context. Do not treat a release
  note as evidence that a feature improves this target's linked image.
- [QMK configuration options](https://docs.qmk.fm/config_options):
  feature compile-time switches and their behavior contracts; use as context
  for feature dependencies, not as an assumed SDCC size result.
- [Intel MCS-51 instruction set reference hosted by Keil](https://www.keil.com/support/man/docs/is51/is51_instructions.asp):
  instruction encoding and the 2-KiB page constraint for ACALL/AJMP.

Search primary SDCC documentation, source, release notes and issue/commit
history for MCS-51 ABI, generic-pointer lowering, code generation, DCE,
peepholes, inlining, stack use, placement and relocation. Search authoritative
8051 manuals and assembler/linker documentation for ACALL/AJMP page rules,
relocations, opcode sizing and layout stability. Search upstream QMK source,
documentation and history for state-machine alternatives, compile-time feature
boundaries, memory representation and compiler-specific assumptions. Then
search analogous 8051 projects and public peer experiments for candidate
techniques; treat forum/blog ideas as hypotheses until primary references and
local controls confirm them. Record queries and useful negative results so the
search is repeatable.

For every external claim, verify that its compiler version, MCS-51 variant,
memory map, ABI, runtime/compiler flags and device behavior apply to this
VS11K28A + SDCC 4.4.0 build. When they do not, label the source as background
only and design a minimal isolated local experiment. External reports and
generic benchmark wins never substitute for this target's linked delta,
behavioral regression checks, stack analysis and release-window validation.
Do not claim the web search covers all possible optimizations; it should make
the candidate search broader and better evidenced, then update this plan.

This research phase is not authorization to implement features or alter the
firmware. Keep feature requests and semantic changes separate from size
experiments. Use a written event contract before investigating compact One
Shot or tap/hold: OSM/OSL hold, lock, timeout, interruption, remap/unlock,
release ownership, simultaneous keys and layer behavior must be specified.
The flag-only One Shot probe reached 40,549 CODE (+1,287 over the old RC6
control), 2,091 XRAM (+20) and exceeded the 40,505-byte limit by 44; it also
placed the highest C745 address 70 bytes beyond the NVM boundary, and tapping
was disabled. It is incomplete and unusable as-is. Any complete design must
start from the current baseline and re-prove the full event contract.

## Explicitly retain prior negative results and constraints

- Four layers: zero CODE/XRAM change; 520 logical NVM bytes only. A layout
  move needs migration and a schema decision. Do not present it as code-space
  work.
- Four-layer and six-layer builds already include only two compiled default
  tables; fewer runtime layers do not remove compiled tables.
- Reducing macro NVM capacity does not create CODE under the current memory
  map. Any NVM-to-CODE proposal needs a complete memory-map, packaging, schema
  and migration design, must account for changed macro capacity, and must
  demonstrate a real linked-window benefit. Preserve protected loader/tail and
  journal bounds; change the NVM base only through that explicit layout design.
- The prior compact-CIE comparison measured 216 CODE bytes saved and is already
  implemented. Treat a different table/definition-compression proposal as a
  new, independently measured candidate. Vial definition data is already
  compressed. Do not credit a smaller source/data blob with net CODE savings
  until a complete linked comparison includes all required reader/decoder code.
- Previous four-layer, RGB HSV packing, flag-only One Shot, compiler 4.5 and
  transfer-count results retain their resource-specific limits above. An
  inventory count, theoretical byte reduction or isolated build is not a
  release image.
- No new broad peephole rules are planned without instruction-level proofs;
  carry, PSW, pointer address space, register bank, ABI, stack and memory side
  effects are part of the acceptance contract. Existing DCE is reachability
  based and is not full LTO. DCE root and hook retention must be reviewed from
  the linked call graph; deleting a startup, IRQ or OEM hook is not a routine
  dead-code optimization.

## Review and release gate

Before a code change is committed, an independent reviewer who did not author
it must review code, documentation and verification evidence. Save review
findings and their closure in the relevant documentation; retest substantive
corrections. Keep README and `docs/STATUS.md` aligned when current behavior,
release state, commands or measured resources change. Regenerate affected
machine reports and reconcile artifact sizes, hashes, versions, addresses and
commands. Do not merge evidence from different build levels. Public release
and hardware writes require separate explicit authorization.
