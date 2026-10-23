# Compact tapping pointer check

Date: 2026-10-23. This note records a source change and the pointer checks behind
it. A new build still needs to measure its effect. No keyboard was opened,
reset or flashed.

The generic-pointer control is `.build/compact-modtap-macros-20261023` under
`qmk-8051-ak820`. Its normal link failed the CODE ceiling: main code ended at
`0xc9c5`, beyond `0xc700`. The reported CODE span was 41135 bytes, including
1808 bytes in the existing low window. XRAM was 2452 bytes. This is a rejected
size probe, not an installable artifact.

The candidate gives four private helper parameters an explicit XDATA pointer
on SDCC: `bit_get`, `bit_set`, `change_owned` and `ak820_macro_change`. XDATA is
the 8051 external RAM address space. The qualifier is empty for host C tests.
Public event, action, Vial and storage interfaces keep their signatures. The
cross-file macro helper has a matching declaration and definition; its callers
are listed below. No state capacity, timing constant or decision changes.

## Pointer origins

The control assembly puts every pointed-to object in `.area XSEG (XDATA)`.
The source call sites pass only these objects:

| Helper | Objects | Control assembly |
| --- | --- | --- |
| `bit_get`, `bit_set` | `active`, `blocked`, `held` | `obj_ajazz_ak820_vial/ak820_tapping.asm` |
| `change_owned` | `owned_mod_refs`, `owned_weak_refs` | `obj_ajazz_ak820_vial/quantum/action_util.asm` |
| `ak820_macro_change` | `macro_keys`, `macro_usages`, `macro_layers` | `obj_ajazz_ak820_vial/quantum/action_util.asm`, `quantum/action_layer.asm` |

A repository search found no other production callers. None passes a stack,
code-memory or external packet pointer. The control reserves three bytes for
`ak820_macro_change_bits` and `change_owned_refs`. The candidate should remove
the generic pointer's address-space selector. Only a fresh SDCC link can show
whether that saves enough CODE.

## Source hashes

| Source | Generic control SHA256 | Typed candidate SHA256 |
| --- | --- | --- |
| `quantum/action_util.c` | `aa64ecee57fd5268ff345ba5a38b3167faced3e146108fe27dc6b9eb9b5865fe` | `d854a46e51bfd67269a58a316b24e6ae047bc5c0e9bedefdb1100acb06019658` |
| `quantum/action_util.h` | `0809fd9cefd5427f1aa49fd30fbf4d1d520f84a3831b82e6a2bfd3d6c5c36e6f` | `a36a3c31909f90591ece52432cbf4f6d561b38699dafff413b46994b6d020909` |
| `keyboards/ajazz/ak820/ak820_tapping.c` | `448982ba3d7baa1dc11ac2d6efe789303b481a7b1fa3ac50478aa7d42b4f431f` | `aa6b5cc5f8c089f878ddfff2097e59d01a4059e2b63a74b4460c946c65faea12` |

The generic control assembly hashes are:

- `ak820_tapping.asm`: `e81c9a526a2d227dafbbe54a52108f837bf2fde6ac0366e20a696babe36b1e72`.
- `quantum/action_util.asm`: `a8cb8198df3bd02c9c49a105b98beb913c3a16c11e0e10170bdbc56f83a7a8d6`.
- `quantum/action_layer.asm`: `ee387b5a9ff3368e0fb6bf0e60ef5798e56023f51b4521b818e11c867bab8776`.

Host C checks exercise the same function bodies with an empty qualifier. They
can check behavior and reject broken deadlines or ownership, but cannot prove
the SDCC pointer ABI, linked size, stack use or task latency. Those checks remain
separate gates for the typed candidate.

## Measured XDATA result

The fresh `.build/compact-modtap-typed-20261023` link still failed the normal
ceiling. Its highest main address was `0xc935`, compared with `0xc9c5` in the
generic control: 144 CODE bytes saved. XRAM fell from 2452 to 2448 bytes.
The link still extends 566 bytes beyond the allowed main window. The source
hashes above identify this measured candidate. It is not an installable result.

## Private hook pointer candidate

A second, separate change replaces the private before hook's copied event with
`const keyevent_t __xdata *` and gives the private decision hook a
`keyrecord_t __xdata *`. The host qualifiers remain empty. The public
`action_exec` and `process_record` signatures stay unchanged.

Both hooks have one production caller, `action_exec`. The sixth build's
`obj_ajazz_ak820_vial/quantum/action.asm` places `_action_exec_PARM_1` (six bytes)
and `_action_exec_record` (nine bytes) in XSEG. The caller passes their addresses;
neither hook retains the pointer after returning. The control before-hook
call copies the six-byte event into another parameter object. The candidate
removes that copy and permits direct XDATA reads of the record. No other
optimization is included in this step.

Control `quantum/action.asm` SHA256:
`980dcf16c26114a2c9e0a7cc0f8127235f2324c1f3f845fe62ef29398976c84e`.

| Source | Sixth-build control SHA256 | Hook-pointer candidate SHA256 |
| --- | --- | --- |
| `keyboards/ajazz/ak820/ak820_tapping.c` | `aa6b5cc5f8c089f878ddfff2097e59d01a4059e2b63a74b4460c946c65faea12` | `2cf0a14fb5c1a579844c99f6ccbf7a2c45a7780d1509c6e71f410788f52130ef` |
| `keyboards/ajazz/ak820/ak820_tapping.h` | `dcd59a6e70015c0e3addec5483ca2f2ec22c63dffadb87415a16582eea2a71a4` | `29b8fd58ac8cb33c740feb7c15f7a688d4022eaa7335e2af7f47e02805ce1c1c` |
| `quantum/action.c` | `8e4b620cc013d483eba42eadd36ff1a774d4d23e32394e36b93f8a543f12b679` | `853685f3bca24d8949b4fe5d650627542c6d258c7f2f3a4d21c4d0d009e2f2a6` |

A fresh link must measure this second candidate separately. Its source change
is not evidence that it fits, or that the SDCC ABI and task latency pass.

## Measured hook result

The fresh `.build/compact-modtap-hook-pointers-20261023` link still failed.
Its highest main address was `0xc911`, compared with `0xc935` before changing
the hook pointers: 36 more CODE bytes saved. The reported CODE span was
40955 bytes. Main code still extends 530 bytes beyond the allowed window.
The hook-pointer source hashes above identify this measured control.

## Source flag candidate

The next isolated change replaces three 17-byte bit planes with one 130-byte
array. Each entry retains three flags: ACTIVE for an admitted press, HELD for
a resolved dual-role hold, and BLOCKED for cancellation suppression. All 128
matrix slots and both encoder directions keep their separate identities.
This costs 79 additional state bytes and removes the engine's bit-plane helper
calls and mask shifts. Modifier, usage and layer state do not change.

Cancellation keeps existing BLOCKED flags and blocks only ACTIVE sources.
An accepted release clears ACTIVE before downstream hooks run. If cancellation
occurs in one of those hooks, a remaining HELD flag must not block a source
that has already released. The host fixture cancels at that exact point,
checks a fresh press, and rejects a mutation that treats HELD as ACTIVE.
The cancellation loop now visits 130 entries instead of 17. Its linked latency
still needs measurement.

Only `keyboards/ajazz/ak820/ak820_tapping.c` changes in this production step:

- Hook-pointer control: `2cf0a14fb5c1a579844c99f6ccbf7a2c45a7780d1509c6e71f410788f52130ef`.
- Source-flag candidate: `cd1d12a4f9f3c870786b769a7db9ff8bf684abe3417cf6ace20a3d51b1bea482`.

No queue, source limit, timing policy or supported action is removed. A fresh
`.build/compact-modtap-byte-state-20261023` link must measure the CODE/XRAM
trade before any fit claim.

## Measured source flag result

The `.build/compact-modtap-byte-state-20261023` link still failed. Its highest
main address was `0xc821`, compared with `0xc911` for the bit planes: 240 CODE
bytes saved. The reported CODE span was 40715 bytes and XRAM was 2515 bytes.
Main code still extends 290 bytes beyond the allowed window. All source
identities and cancellation checks remain present; this is still a rejected
size probe.

## Derived layer mask candidate

The next separate change caches two bytes in `tri_layer.c`: the combined
Lower/Upper input mask and the Adjust bit. The initial targets have compile-time
range and distinctness checks. The target variables are static. A source search
found writes only in the three validated individual setters and the validated
combined setter. Each successful setter recomputes both masks and refreshes the
effective layer state. Rejected setter calls leave both targets and masks alone.
No storage field or user setting changes.

The effective layer refresh calls the new private derived-bit helper with
persistent and momentary state combined with `default_layer_state`. It ORs the
result into the effective state. Explicit Adjust owners therefore survive when
the derived contribution disappears. Public `update_tri_layer` keeps its
signature; other profiles keep the original implementation.

The compact Tri Layer key processor no longer calls another layer update after
`layer_hold_on` or `layer_hold_off`, because those functions already refresh the
effective state. Macro duplicate DOWN/UP paths with no ownership change do not
need a refresh; target setters refresh immediately. Other profiles keep that
original update call.

| Source | Source-flag control SHA256 | Derived-mask candidate SHA256 |
| --- | --- | --- |
| `quantum/action_layer.c` | `b82526d369a53d06d1cd4bb6ecbe7e1550ccf39af514c0edbf469b1dcc154712` | `a0ef205836f84dc13ba9fb50821188752c428f86478c9446bd707791e80c64f6` |
| `quantum/action_layer.h` | `7768fb18e96a87892e9a76ccafc2b31fd30e98fac5de12aa1ea21bb9dab5a824` | `e6e04818637f7f0bccccf4898bd781ed97682239b8c695196482b964984a1151` |
| `quantum/tri_layer.c` | `22d373c6ecf0f638fe0086aeee9701c5a49eafb0ff047f0e11553e45bc8819c8` | `68fdc973e724c95035bf10ddf2f108e1941b754a28edf87f497ea1760fda49f2` |
| `quantum/tri_layer.h` | `6a7a1bb62acd8a16315b3dccc99954288b3a894e4c9c253875b6805e7c399aa8` | `8e79aaf53bf2d17bfe372f236e69ff315e202535763ea83b4778524705a9da58` |
| `quantum/process_keycode/process_tri_layer.c` | `a96801e0812c9e4f787d32c7116c1d0b236f354ddd3e4f07fad3869d5c579807` | `33bd8d03455804c858f777e276bd2911cd2096946c9d6c2704773efc91fc4790` |

Default-layer changes, TO/TG, all momentary owners, explicit Adjust ownership
and mutable Tri Layer targets remain host test cases. The next fresh link must
measure this candidate separately; no other optimization is included.

## Measured derived-mask result and Caps Word fix

The `.build/compact-modtap-tri-masks-20261023` link still failed. Its highest
main address was `0xc7b6`, leaving 183 bytes beyond the normal window. This
saved 107 CODE bytes against the source-flag control.

A separate correctness check then found that Caps Word adds temporary Shift
through the raw modifier API but removed it through the wrapper now used for
owned weak modifiers. Turning Caps Word off could remove an encoded, Repeat or
macro Shift owner and retain its own temporary Shift. The actual Caps Word
integration fixture reproduced the failure before correction. Compact cleanup
now calls raw `del_weak_mods(MOD_MASK_SHIFT)` and sends a report. Other profiles
keep their existing wrapper call.

The cleanup-only link still failed at `0xc7c6`, with 199 bytes beyond the allowed
window. The main code grew by 16 bytes. Correctness is retained despite that
size cost. Corrected `quantum/caps_word.c` SHA256:
`2631e90b7a73ac228f94597c3a08383242683dfeefc1aff2e799d7ca2fbdaf3b`.

Host tests cover raw cleanup alongside encoded, Repeat and macro weak owners,
idle cleanup, capitalized MT/LT taps and the documented pure-hold mode policy.
Shift MT and LT retain Caps Word; after a Control MT hold, the next ordinary key
ends it. Timeout and interrupting-press cases use the actual Caps Word handler.
These differences from QMK feature bookkeeping are explicit; matching timing
traces do not imply matching every QMK feature callback.

## Modifier dispatch candidate

The next independent size change affects only the private modifier helper in
`quantum/action_util.c`. Its four public wrappers keep their signatures. They
pass one mode byte: bit zero selects add/remove, and bit one selects strong or
weak ownership. The static helper has only those four constant-mode callers.
It selects the same two XDATA reference arrays, applies the same macro primitive
filter, updates the same eight counters and stores the same effective mask.

This removes repeated pointer, pressed/kind argument setup and per-wrapper mask
stores. No modifier owner, raw modifier state or cancellation behavior changes.
The next normal link must measure it separately.

- Cleanup control SHA256: `d854a46e51bfd67269a58a316b24e6ae047bc5c0e9bedefdb1100acb06019658`.
- Modifier dispatch candidate SHA256: `1666efc06119c9624f0de1868780ace34df40a49133d032c79e8bf3660986d16`.

## Measured modifier dispatch result

The modifier-mode link still failed at `0xc78d`. It saved 57 CODE bytes against
the cleanup control, leaving 142 bytes beyond the normal main window. The
modifier dispatch source hash above identifies this positive but insufficient
size change. Caps Word ownership and pure-hold tests passed independently with
nine rejected mutations and 156 eligible QMK comparisons.

## Byte namespace candidate

The next isolated change removes the single-use `dual(uint16_t)` helper and
checks the high byte directly in the decision hook. The static assertion pins
MT through LT to `0x2000..0x4fff`; for every 16-bit code, this is exactly the
high-byte interval `0x20..0x4f`. The low byte cannot affect membership.
No lookup is moved, and no tap-byte, source, layer or modifier limit changes.
The helper had one production caller and no external interface.

Only `keyboards/ajazz/ak820/ak820_tapping.c` changes in this step:

- Modifier-mode control SHA256: `cd1d12a4f9f3c870786b769a7db9ff8bf684abe3417cf6ace20a3d51b1bea482`.
- Byte namespace candidate SHA256: `ce2c7c04b2f9d98e8a4f1eb8482aa63d651ccd972e4635b6b3a65f807af9a6d2`.

The normal link must measure this candidate before any fit claim. The host
suite still runs the full decoder/action/cache/ownership path and the timing
comparison; the predicate change is not a substitute for those tests.

## Measured byte namespace result

The byte-namespace link failed at `0xc75b`, leaving 92 CODE bytes beyond the
normal main window. It saved 50 bytes against the modifier-mode control. The
source hash above identifies the measured candidate. The production host suite
passed with all nine mutations rejected and 156 eligible retained-QMK
comparisons (`/tmp/ak820-compact-host-byte-namespace.json`). This is host evidence;
it does not establish linked CPU timing or device behavior.

## Cancellation flag expression candidate

This isolated change replaces the active-bit ternary with a left shift. A static
assertion pins BLOCKED to ACTIVE shifted once. For all 256 possible byte states,
`(state & BLOCKED) | ((state & ACTIVE) << 1)` preserves an existing block and
blocks an active source. It clears all other bits, including HELD. A released
source with HELD alone remains unblocked. The source count and cancellation
order are unchanged. No other production file changes in this step.

- Byte namespace control SHA256: `ce2c7c04b2f9d98e8a4f1eb8482aa63d651ccd972e4635b6b3a65f807af9a6d2`.
- Cancellation expression candidate SHA256: `f7aa9586fdccdf3b2a6b6d9b79e60824bb9c5df35e6146c7cbdcc839d0275010`.

The next normal link must measure this candidate separately.

## Measured cancellation result and admission candidate

The cancellation-expression link ended at `0xc755`, saving six CODE bytes. It
still exceeds the normal main window by 86 bytes. The host suite passed with
nine mutations rejected and 156 QMK comparisons.

The next isolated change replaces the two ACTIVE set/clear branches with XOR.
The preceding equality check returns for duplicate presses and unmatched
releases. Therefore every admitted edge has a pressed value opposite to the
current ACTIVE bit. Toggling ACTIVE sets it on an admitted press and clears it
on an admitted release, preserving every other bit. No callback or state write
occurs between that check and the toggle. The earlier BLOCKED path still
returns before admission.

- Cancellation control SHA256: `f7aa9586fdccdf3b2a6b6d9b79e60824bb9c5df35e6146c7cbdcc839d0275010`.
- Admission XOR candidate SHA256: `beaa2a96510fcaada9685d3b7fe46346a8bd85c17edecfd7a5126a907dcfa313`.

This candidate requires a separate normal link. Neither isolated mapping nor
send-string size changes are included.

## Measured admission XOR result

The admission-XOR link ended at `0xc748`, saving 13 CODE bytes against the
cancellation control. It still exceeds the normal main window by 73 bytes.
The full host run passed with nine mutations rejected and 156 retained-QMK
comparisons (`/tmp/ak820-compact-host-admission-xor.json`). Its source snapshot
remained unchanged throughout the run. No linked CPU or device result follows
from this host check.

## Host input binding correction

The tapping host fixture now includes `report.h` and the remaining directly
included production headers in its source snapshot. This binds the system
mapping implementation to both the saved hashes and the unchanged-input check
at the end of the run. Only the test runner changes; production behavior is
unchanged. A fresh mapped-source host report is required.

The corrected runner passed against the stable mapped source, with nine
mutations rejected and 156 QMK comparisons. The report
`/tmp/ak820-compact-host-mapped-header-bound.json` includes `report.h` in its
source hashes; the final unchanged-input check passed.
