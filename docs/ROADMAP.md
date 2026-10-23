Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

## After alpha

`v0.6.0-alpha.1` is published and installed; results are in [Status](STATUS.md).
The source now has a bounded two-key Combo candidate that fits the memory
windows. The candidate is not in the published alpha or the installed
installer bundle. Its settings format needs a reviewed backup/restore extension
and migration before a future installer package can use it. The full qualification passed 28 suites and 258 unit tests without skips;
see [Status](STATUS.md). The post-restart
`open failed` installer stop still needs diagnosis and a correction. Power-cycle persistence,
native Windows interactive acceptance and physical timing remain open.


Updated 2026-10-24. Completed work and exact image identities are in
[Status](STATUS.md). The development source and installer release now differ;
a successful source build does not promote the candidate into the installer.

## Completed work

- [x] Add eight dynamic two-key Combos with a fixed 40 ms term. Fit the complete
  image by optimizing the existing code, preserving Grave Escape, NKRO, six
  layers and the full macro store. The normal build uses 40,313 CODE bytes;
  the new linked Combo tests pass 26 cases. Complete qualification is recorded
  separately in [Status](STATUS.md).
- [x] Keep the existing host settings backup, restore and in-installer update
  workflow; retain its exact-image compatibility checks and fresh physical unlock.
- [x] Configure CI for branch pushes, pull requests, manual runs and version
  tags. Linux builds and tests fresh firmware; Windows packages that bundle.
  SemVer tags reachable from `main` publish after both jobs pass. Earlier GitHub
  Linux/Windows runs passed; the tap-hold candidate also passed dev run 40026118029.
  Visible Windows dialog acceptance remains pending.
- [x] Reproduce the stable firmware with pinned SDCC 4.6.0 and run the complete
  offline suite for that image: 23 suites, 257 unit tests, zero skips. The new
  compact tap-hold candidate passed 26 suites and 258 unit tests without skips.
  The earlier 247-test qualification is historical.
  Keep initial failures and final results in the evidence.
- [x] Assemble a fresh firmware bundle from commit `073047d` after review of
  the source and policy. The installer accepted it with
  `load_release(approved=True)`; no device was accessed. This source-package
  check does not establish Windows packaging or device behavior.
- [x] Test the private XDATA journal pointer in a controlled build. Adopt it in
  source after review: 31 fewer CODE bytes and one fewer XRAM byte.
- [x] Test the macro delay replacement. Reject it: three more CODE bytes;
  SDCC 4.6 already uses `MUL AB` for the original expression.
- [x] Add a repeatable linked instruction inventory, validate report artifacts
  and retain control/candidate listings. Partial coverage is explicit; a complete
  call graph and execution profile are not claimed.
- [x] Investigate Caps language switching and C/W indicators. Record source
  constraints and the event test plan. Caps remapping remains deferred. C/W
  outputs are included in alpha; manual smoke checks reported both working.

See the [bounded probes](../audits/rc6/bounded-optimization-20261023.md),
[inventory](../audits/rc6/linked-inventory-20261023.md) and
[input contract](../audits/rc6/input-indicators-contract-20261023.md).

## Next acceptance steps

| Work | Required result and current dependency |
| --- | --- |
| Windows package | Complete a GitHub run or native Windows build from this branch. Retain both EXEs, package provenance and CLI/GUI smoke reports. Check the visible RU/EN update and settings dialogs. Tap-hold CI packaging and startup checks passed in run 40026118029. Visible dialog acceptance remains pending. |
| Host settings on a keyboard | Check backup, guarded restore and update with a valid private OEM session and separately authorized device operations. Test macro upload, saved RGB, cancellation, failure stops and cold-start persistence. Offline passes do not close this step. |
| Candidate release | If a development image is selected for release, create a new exact artifact review and package using the private OEM inputs. Review settings compatibility explicitly before changing any image pin. Keep the existing release usable until this is done. |
| Physical behavior | Check every key, encoder press and both rotation directions, lighting appearance, Alt Repeat, unlock and power-loss behavior. Record the image hash and distinguish ordinary restarts from complete power removal. |

A timeout, bad readback or storage fault stops the operation. Do not retry,
reset, restore or enter the loader blindly. Every hardware write needs the
required explicit confirmation; the current offline work grants none.

## Input and lighting features

| Feature | Next bounded task / blocker |
| --- | --- |
| C indicator | The source candidate drives OEM slot 71, component 1 from the host Caps LED bit. Verify the physical C connection and visible behavior; [source and CPU evidence](INDICATORS.md) do not establish device behavior. |
| W indicator | The source candidate drives OEM slot 79, component 1 from additional-layer activity. Verify the physical W connection and visible behavior; the project meaning is layer activity rather than OEM lock state. |
| Caps language key | Deferred by the current request; keep Caps and its mapping unchanged. The retained future plan uses a dedicated remappable keycode; Win+Space is the proposed Windows shortcut, either Shift selects ordinary Caps Lock. First settle deferral versus rejection when Space/Caps is already held, request ordering/coalescing, timeout and cancellation. Implement staged report delivery without losing held-key ownership, and test 6KRO/NKRO, modifiers, remap, unlock, reset and Repeat exclusion. Windows acceptance remains separate. |
| Windows language helper | Report the actual active-window language, including window changes and other switch methods. Define stale/unknown state and a RAM-only status path before implementation. Do not count Caps presses or write flash for language updates. It depends on the indicator/status design and Windows testing. |
| Direct Control | Keep RAM-only VialRGB Direct. Persistent palette work was cancelled on 2026-10-23 to prioritize keyboard input functions. Its code is retained only in the separate experimental branch `codex/experiment-direct-palette`; it is not approved for installation. |

## Compact functions and selectable builds

The bounded two-key Combo implementation is complete in development source
and fits alongside the existing functions. Its full-image size is 164 bytes
below the installed alpha image; separate probe savings do not add up to the
final linked size. Further compact functions and selectable profiles remain
future work. Other possible candidates are One Shot, Tap Dance, Key Overrides
and Mouse Keys.

For each function, record the linked CODE and RAM cost against a fixed control,
its behavior and limits, required dependencies, host/CPU tests and interactions
with other functions. A flag-only size probe does not establish a usable
implementation. Preserve implementation source when a build profile disables a
function. Measure complete profiles too: separate savings do not necessarily
add up after linking. Profile selection and distribution are future design work. Remaining Combo
acceptance includes physical timing and behavior,
settings backup/restore migration, installer packaging and release review.

## Further optimization only when needed

The Combo candidate fits with 120 trailing main-window bytes and 67 low-window
bytes; see [the resource table](RESOURCE-BUDGET.md). The private event-pointer
and ownership reductions are measured. Earlier protocol-field probes were
rejected; the current USB dispatch, descriptor and EEPROM changes save code. Probe savings are non-additive. The complete image is
164 bytes below the installed alpha. See [Status](STATUS.md) for the exact image
and separate qualification state.

Further byte-by-byte reduction is not a promise of room for major features.
After this feature, choose the needed functions and a build budget first;
optional feature profiles can trade unused functions for new ones. The research
options below are conditional, not an active instruction to keep shrinking the
current image. Any new experiment needs a fresh independent control:


1. Prove every origin and memory placement before trying a typed private event
   pointer. Preserve the public event ABI and release ownership.
2. Inspect one repeated protocol field decode or response tail at a time;
   include malformed requests, bounds, ACK behavior and storage faults.
3. Try typed leaf copies only where source/destination spaces, lengths and every
   caller are proved. Include overlap and out-of-range cases where applicable.
4. Extend the linked inventory with explicit indirect/IRQ/OEM roots and a
   justified execution profile before claiming a complete call graph or hot paths.
   Investigate callee-save, inlining or alternate algorithms only with their
   register, stack and timing contracts.
5. Consider a bounded peephole rule only after instruction-level proofs covering
   carry, PSW, register banks, pointer spaces, stack and memory side effects.
   Rebuild and check the complete image, both placement windows and behavior.
6. Keep short calls blocked until relocation and boundary fixtures are complete.
   The previous linker run stopped after six of 42 fixtures on an invalid-target
   crash. The current inventory's page-eligible transfers are observations,
   not available bytes or a safe rewrite.
7. Keep any compiler backport conditional. SDCC bool near-pointer fixtures
   previously failed two of sixteen cases on both compared compilers; no matching
   shape was found in the reviewed retained paths. Reproduce a relevant defect
   before changing the pinned compiler.

Record each hypothesis, exact input versions, controlled linked delta, behavior
checks and acceptance/rejection reason. Compare all CODE windows, XRAM and stack;
reject zero/negative benefit or an incomplete correctness contract. No saving
target such as 1 KB is promised. Source length and generic-pointer call counts
are not linked savings.

The prior [deep analysis](../audits/rc6/optimization-deep-analysis-20261023.md),
[SDCC research](../audits/rc6/optimization-deep-sdcc-research-20261023.md) and
[review](../audits/rc6/optimization-deep-review-20261023.md) remain research
references. Their older artifact counts are superseded by the retained linked
inventory for the current control/candidate. Extend the primary-source search
when investigating a new compiler or relocation claim, recording revisions,
queries, applicability and useful negative results. External wins do not prove
benefit on this VS11K28A + SDCC 4.6.0 target.

## Constraints and negative results to retain

- Keep six layers and sixteen macros with 8192 shared bytes. The historical
  four-layer build saved zero CODE/XRAM bytes and only 520 logical NVM addresses.
  Moving the encoder base requires an explicit schema/migration design.
- Reducing macro capacity does not create CODE under the current memory map.
  Any NVM-to-CODE change needs a complete layout, packer, protected-region and
  migration review. The compact CIE saving is already implemented; do not count it again.
- Direct HSV packing could save 82 RAM bytes but adds code and color loss.
  Require an accepted precision bound and a complete linked comparison.
- The old flag-only One Shot probe used 40,549 CODE bytes, 44 above the total
  limit, and crossed the NVM boundary by 70 bytes. It was incomplete and remains
  unusable. Compact tap-hold now has its own event contract and candidate; a
  future One Shot proposal still needs a complete separate contract.
- SDCC 4.5 failed in compiler optimization and produced no usable comparison.
  SDCC 4.4 measurements are historical; production tooling remains pinned to 4.6.0.
- Existing DCE is reachability-based, not full LTO. Startup, IRQ and retained
  OEM hooks cannot be removed as routine dead code.

Before committing, obtain independent review of code, documentation and evidence,
close findings and repeat affected checks. Keep source, application build,
approved update package and device results separate. Public release and device
writes have separate approval requirements.
