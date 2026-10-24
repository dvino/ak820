# Compact runtime features — 2026-10-24

This work continues source `06b8f0f`. Sixteen named development profiles retain
all base functions and add bounded GUI controls and Dynamic Macros. Published
and installed alpha.3 is unchanged. No USB device was opened.

## Implementation checkpoint

The encoder now reuses one event object, Mouse Keys normalizes opposing pairs
once, and unused numeric buffers avoid redundant explicit zero stores. The
Vial macro interpreter uses a 16-bit EEPROM offset instead of a generic pointer.
The API boundary keeps its existing pointer token; logical storage remains
`0x0800..0x27ff`. See [optimization](optimization.md) and
[cursor review](review.md).

GUI controls mask left/right GUI at final report composition, preserving other
owners, One Shot and Repeat. Dynamic Macros store two 16-tap slots in RAM and
replay completed keyboard taps with modifier snapshots. Shared clear cancels
playback, pending USB output blocks progression, and nested Vial primitives
cannot acquire or release Dynamic Macro ownership. Public behavior is in
[GUI controls](../../../docs/GUI-CONTROL.md) and
[Dynamic Macros](../../../docs/COMPACT-DYNAMIC-MACROS.md).

The short-call pass now restores the original long transfer when the pinned
linker rejects a selected instruction, even if independent decoding accepts
its PC+2 target. Authentication and the strict final gate remain unchanged.
See [diagnostic reproduction](shortcall-diagnostics.md).

## Integrated probes

| Profile | Short calls | CODE | Main / low free | XRAM |
| --- | --- | ---: | ---: | ---: |
| `full-mouse-auto-shift` | No | 40,427 | 57 /16 | 2,654 |
| `full-dynamic-macro-gui` | No | 40,319 | 165 /16 | 2,696 |
| `full-mouse-auto-shift-gui` | Yes | 40,432 | 52 /16 | 2,657 |

Exact reports and images are in `integration-probes/`. These measured builds
precede the final profile-list cleanup; their original source hashes are
retained as provenance. Final frozen-source qualification is pending.

The exploratory `full-mouse-auto-shift-dynamic-macro --short-calls` image
contains 41,288 CODE bytes and reaches `0xca23`: 804 bytes lie above the main
window. The strict build rejected it. Its profile was removed; the failed
image and raw build are retained solely as experimental evidence. Features,
macro storage, layers and the protected loader/NVM windows were not reduced.

An earlier integrated Auto Shift + Dynamic Macro image used 40,459 CODE bytes
and passed 27 exact-linked scenarios, including effective Auto Shift capture.
It predates the portability cast correction and is not the final source
measurement. The final matrix must rebuild this combination.

## Review and verification

The [review record](review.md) lists independent reviews, findings and closure.
Isolated evidence is in [Dynamic Macros](dynamic-macro.md),
[GUI controls](gui-lock.md), [optimization](optimization.md) and
[short calls](shortcall-diagnostics.md). Host checks execute production C;
C52 checks execute the exact linked image with simulated peripherals.

The final matrix will rerun the 28 base suites and each selected feature's
supplemental suites against each frozen image. CPU results do not prove
physical USB/scan timing, IRQ overlap, persistent writes or a whole-program
stack bound. The release safety gate remains unchanged and rejects these
unqualified images.

## Research and rejected alternatives

The [SDCC manual](https://sdcc.sourceforge.net/doc/sdccman.pdf) documents
three-byte generic MCS-51 pointers. Here EEPROM addresses are numeric 16-bit
tokens, so removing the unnecessary address-space byte is a source-level
optimization with explicit bounds and an unchanged call boundary.

[SDCC patch 490](https://sourceforge.net/p/sdcc/patches/490/) discusses improved
DPTR/register tracking; [patch 504](https://sourceforge.net/p/sdcc/patches/504/)
contains further peephole work. Unqualified global instruction rewriting and
compiler replacement were not imported. Only changes measured with the pinned
SDCC 4.6.0 toolchain were retained. Broad and smaller callee-save expansions
made complete images larger; their measurements are in `optimization.md`.
The [QMK Dynamic Macro controls](https://docs.qmk.fm/features/dynamic_macros)
and [Magic keycodes](https://docs.qmk.fm/keycodes_magic) supply familiar keycodes;
the compact behavior is bounded as documented in the AK820 guides.
