# Mod-Tap and Layer-Tap contract

Date: 2026-10-23. Source inspection at `453fa7c`. This is an implementation
proposal, not evidence of implemented or installed tap-hold support. No build,
CPU execution, USB command or device test was performed for this report.
Caps behavior and the default Caps assignment stay unchanged.

## Current source and ABI

`keyboards/ajazz/ak820/config.h` defines `NO_ACTION_TAPPING`,
`NO_ACTION_ONESHOT` and `HOLD_ON_OTHER_KEY_PRESS`. The last flag currently has
no tapping engine to configure. `quantum/action.c:action_exec()` passes records
directly to `process_record()`. The AK820 byte decoder in
`quantum/keymap_common.c` converts both MT and LT into `ACTION_KEY(low_byte)`.
Holding either therefore holds its tap key; it does not activate its encoded
modifier or layer.

The wire and storage keycode remains 16 bits. MT is `0x2000..0x3fff`: five
modifier bits and an eight-bit tap key. LT is `0x4000..0x4fff`: four layer bits
and an eight-bit tap key. MT bit 4 selects the right-hand group for all four
modifier bits; mixed left/right combinations cannot be encoded. Runtime HID
modifier state must still retain all eight independent modifier bits.

The current installer allowlist (`tools/installer/settings_backup.py`,
`keycode_supported`) accepts MT with a basic low byte and LT with the same
low-byte test and layer 0..5. Its basic predicate accepts 0, 1, `0x04..0xc2`
and `0xe0..0xe7`. Those ranges include usages that are not ordinary keyboard
letters. The validator's acceptance is not proof that every low byte has a
useful tap action. The firmware decoder, host validator, Vial presentation and
regression expectations must agree explicitly before enrollment.
`keymaps/vial/vial.json` currently has `"vial": {}`; no literal
`tapping_disabled` field was found in the repository. Generated definitions
and the installed Vial client must be checked separately rather than assuming
that an absent field advertises a tested function.

Keep six layers, 16 macros, 8192 macro bytes, the current UID and NVM layout.
MT/LT need runtime state, not a new keycode or persistent format. Layer targets
6..15 remain unsupported. No reduction of those capacities funds this feature.

## Reuse decision before a new engine

The retained QMK engine already provides one pending `tapping_key`, a waiting
ring and `process_tapping()`. `action_tapping.h` defaults to 200 ms, quick tap
200 ms, and eight ring entries (seven usable slots with head/tail indexing).
`action_tapping.c` clears the keyboard and queue on overflow. That recovery
loses events and is unsuitable for the contract below without correction.
Its static state also needs an explicit cancellation API for unlock/reset.

The existing `tests/ak820_tap_state_experiment/README.md` records historical
SDCC 4.4 measurements: tapping plus One Shot grew CODE from 40461 to 46444,
and XRAM from 2323 to 2526. A common output tail reduced that variant by 274
CODE bytes. Those builds used expanded `--code-end 0xf700`, crossed NVM and
were size probes, not installable artifacts. They are not a current MT/LT-only
price. The later One Shot-only probe grew CODE 38929 to 40198 and XRAM 1975
to 1995 while MT/LT stayed disabled; linked characterization proved OSM/OSL
fallback, not working One Shot. Removing one feature guard is not enrollment.

First measure a current, isolated MT/LT-only QMK opt-in, retaining
`NO_ACTION_ONESHOT`, with explicit 200 ms and quick-tap zero. Inspect guards
for changed TT/OSM/OSL behavior: activating tapping must not silently enroll
those features. Port only required SDCC constructs and measure the complete
linked result. Keep QMK as a differential oracle even if its full engine does
not fit. A compact engine is justified only after this comparison and must
meet the same public MT/LT timing contract plus the ownership requirements
below. Source brevity or an A/Shift demonstration is insufficient evidence.

## Proposed public behavior

Use QMK `HOLD_ON_OTHER_KEY_PRESS` behavior for both MT and LT, a fixed
`TAPPING_TERM=200`, and `QUICK_TAP_TERM=0`. Do not enable permissive hold,
retro tapping or tap-toggle as part of this work.

A press starts undecided. Release before 200 ms, without another key press,
produces exactly one tap down/up. At elapsed time 200 ms or later, hold wins;
the hold starts before processing the event at that boundary. Any other
physical key press before the timeout commits the earlier undecided key to
hold before resolving the new press under the resulting layer/modifier state.
Thus both nested chords and rolls that overlap a second press choose hold.
A second key release alone does not choose hold. This policy deliberately
trades forgiving rolls for immediate chords; it must be stated in user docs.

A second press after a completed tap starts a fresh decision, even inside
200 ms. Holding that press produces the hold action, not tap-key auto-repeat.
No double-tap lock or repeated-tap shortcut is implied. The ordinary host can
repeat a tap key only while a genuinely emitted tap-down remains held under
an explicitly tested path; this contract normally emits a completed short tap.

Every MT modifier mask 0..31 must decode consistently with the pinned QMK
encoding, including zero and right-group masks. LT accepts layers 0..5,
including layer zero. Do not replace the eight-bit tap field with a small
letter-only whitelist. Retain the existing accepted basic-byte domain after
characterizing each class: no-op/transparent, keyboard usages, modifiers and
extra usages. If any accepted byte cannot safely execute as a tap, document
and reject it consistently in validator and firmware before enrollment;
never silently reinterpret it as a different key. Extended 16-bit actions,
macros, RGB commands and nested MT/LT cannot fit the tap byte.

## Event and state ownership

Use press identity (matrix position or encoder direction plus a generation),
not keycode equality, as ownership. Freeze a resolved keycode for every
accepted press until its release. A live remap cannot redirect release or
change an already pending MT/LT. A later press resolves against the new map.
For an interrupting press, first commit older pending holds, then resolve and
cache that press using the resulting layer; the current pre-tapping cache
lookup in `pre_process_record_quantum()` must be audited and adjusted so it
does not freeze a base-layer key prematurely. Do not look up releases anew.

Track modifier ownership per bit and layer ownership per layer. Releasing
one of two MT holds for the same modifier cannot release the other's bit;
neither may it release a physical modifier, LM hold or synthetic Repeat
owner. A tap of a modifier byte must obey the same rule. Keep strong and weak
modifier contributions separate. Effective layer state combines persistent
TO/TG/default state and momentary owners (MO, LM, LT, Tri Layer inputs).
Removing an LT owner must preserve another owner and persistent state;
Tri Layer recomputes its managed layer after each effective input change.
Simple `del_mods()`/`layer_off()` on release is insufficient for this policy.

Persistent layer state is separate from momentary owners. `TG(n)` toggles
the persistent bit, not the effective bit. `TO(n)` replaces the persistent
mask with bit n; active MO/LM/LT owners remain effective until their own
release. Layer-off/clear operations alter persistent state only unless the
explicit cancellation path invalidates every owner. Tri Layer derives its
managed contribution from the combined effective input layers. Adjust is
active when Lower and Upper are active, OR when Adjust has an explicit
persistent bit or momentary owner. Releasing the derived contribution cannot
clear an explicit Adjust owner. The derived contribution is excluded while
computing its own inputs; aliases of Lower/Upper/Adjust must follow an
explicitly validated distinct-layer configuration. Test TO/TG while an
LT/MO/LM owner holds the same layer and while multiple owners overlap. This
is an explicit ownership policy, not an assertion of every upstream QMK
layer_move side effect.

Accepted releases are processed immediately in event order. In particular,
Shift down, MT down, Shift up, MT up before 200 ms emits an unshifted tap.
The upstream QMK engine may retain the older modifier release while deciding
the MT and emit a shifted tap instead. Preserve this trace in differential
tests as an intentional difference; do not call the engines fully equivalent.
The same immediate-release rule applies to an older layer owner. A compact
engine must commit a pending hold before resolving a subsequent press but
must never delay an unrelated accepted release merely to mimic QMK's queue.


With immediate hold-on-other-press, at most one ordinary undecided physical
press is needed: a subsequent press commits it. Arbitrarily many resolved
holds still require tracked owners. Resolve pending state before admitting
the next press; never accumulate an unbounded undecided chain. If a queue is
needed for reentrancy or delayed tap emission, publish its exact capacity and
prove its bound against matrix scanning, encoder pulses and synthetic events.
A queue-full path must commit and drain in order before accepting more input,
or prevent admission before consuming the source event. It may not discard,
overwrite or clear releases. A fixed eight-event queue with clear-all overflow
is not an acceptable substitute. Do not recurse into non-reentrant SDCC
functions while replaying events; inspect generated call/storage use.

Preserve the order of accepted press/release pairs. Two dual-role positions
pressed in one scan follow the existing deterministic scan order: first hold
is established before the second lookup. Test same-keycode pairs and reverse
release order. Use unsigned elapsed subtraction across timer wrap; test
199/200/201 ms and wrap at `0xffff`. Process elapsed deadlines even with no
matrix change. No stale timer can resurrect a cancelled press.

6KRO and NKRO are report modes, not limits on ownership. Track all physical
holds even when a boot report cannot represent every ordinary key. Test
rollover, removal and later report promotion without stuck modifiers or
reordered release. Do not cap dual-role state at six keys.

Encoder CW and CCW are distinct synthetic positions. Their normal pulse
press/release pair resolves MT/LT as a tap when no intervening press or elapsed
hold exists. Encoder presses interrupt a pending physical MT/LT before their
own layer lookup. A pending encoder record cannot alias a matrix position,
the other direction or a subsequent pulse. Test both directions, alternating
pulses, bursts, and physical holds around pulses.

Repeat/Alternate Repeat must remember the resolved tap key and active modifier
snapshot, not an undecided MT/LT or a pure hold. A hold must not replace the
last repeatable key. Generated Repeat events carry explicit `record.keycode`
and `tap.count`; do not run them through physical-position cache lookup or
start another MT decision. Test recursive guards, hold/release cancellation,
modifier overlap, and Alt Repeat mapping after MT/LT taps.

Unlock currently calls `vial_release_held_state()`, releases MO/LM/Tri Layer
from cached physical keys, cancels Repeat, and clears HID state. Add one
explicit tap-hold cancellation before suppression starts: discard pending
undecided taps without typing them, release each owned hold, empty deferred
events, invalidate identities, and send released reports. Physical keys still
held through unlock stay suppressed until release and a fresh press. Cancel
on shutdown/reset, report clear paths and settings reset where held state is
invalidated. Review all `clear_keyboard*` call sites, especially layer changes,
so ordinary layer updates do not accidentally cancel legitimate LT owners.
Cancellation never initiates reset, bootloader entry or a storage write.

## Evidence required before enrollment

1. Add table-driven host traces using actual decoder, action pipeline, source
   cache, tap decision code, modifier/layer owners and Repeat integration.
   Assert ordered HID reports and final ownership, not only final modifier
   bytes. Cover all MT masks, layers 0..5, tap-byte classes and invalid layers.
2. Compare eligible timing traces against the retained QMK engine with the
   chosen flags. Explicitly separate intentional ownership/overflow fixes
   from QMK equivalence. Include a negative control for early release, wrong
   right-hand decoding, premature cache lookup and queue release loss.
3. Run real linked 8051 CPU traces through the same public event/task entry
   points. Cover nested dual-role keys, same-modifier overlaps with ordinary
   modifiers/LM/Repeat, MO/LT/TG/TO/Tri Layer overlap, live remap while held,
   unlock/reset cancellation, both encoder directions, 6KRO/NKRO and wrap.
   Require stable complete report traces and no remaining owners at the end.
4. Measure current baseline and candidate with the same pinned compiler and
   fresh distinct build directories. Record hashes, CODE windows, XRAM,
   internal DATA/stack budget, maximum call depth and worst-case task latency.
   The normal builder's main ceiling is `0xc700`; low-code windows and all
   protected/NVM ranges remain enforced. No expanded ceiling, reduced layers,
   reduced macro space or moved NVM may count as success. The exact current
   headroom must come from those paired reports, not historical deltas.
5. Keep default regression commands offline or read-only. Live remap or NVM
   checks require an explicit execution option and authorization. Host/CPU
   PASS does not prove physical timing, USB scheduling, encoder hardware or
   durable storage. Report these as untested until separately authorized.
6. Independently review implementation, generated machine reports, validator,
   definition, README/INSTALL/STATUS and translations before committing.
   Record finding closure and rerun substantive corrections. Do not advertise
   support or change the approved release until these gates pass.

No tap-hold code or feature advertisement is approved by this report alone.

Independent architecture review, 2026-10-23: review_modtap_contract approved
this implementation basis after clarifying persistent TG/TO state, explicit
Adjust ownership and immediate unrelated releases as an intentional QMK
difference. Source, resource and runtime approval remain separate gates.
