# Compact runtime features — 2026-10-24

All 16 named development profiles passed 18 frozen build variants. The firmware
and tests are from clean commit `55acbb0`; later changes add documentation and
retained evidence only. This work continues source `06b8f0f`. Published and
installed alpha.3 is unchanged; no device commands were issued.

## Results

| Build | CODE bytes | Main / low trailing free | XRAM |
| --- | ---: | ---: | ---: |
| `full` | 38,964 | 1,520 / 16 | 2,607 |
| `full --short-calls` | 38,717 | 1,767 / 16 | 2,607 |
| `full-mouse` | 39,814 | 670 / 16 | 2,637 |
| `full-auto-shift` | 39,577 | 907 / 16 | 2,624 |
| `full-mouse-auto-shift` | 40,427 | 57 / 16 | 2,654 |
| `full-mouse-auto-shift --short-calls` | 40,203 | 281 / 16 | 2,654 |
| `full-gui-lock` | 39,199 | 1,285 / 16 | 2,610 |
| `full-dynamic-macro` | 40,084 | 400 / 16 | 2,693 |
| `full-dynamic-macro-gui` | 40,319 | 165 / 16 | 2,696 |
| `full-mouse-auto-shift-gui --short-calls` | 40,432 | 52 / 16 | 2,657 |
| `full-auto-shift-dynamic-macro --short-calls` | 40,466 | 18 / 16 | 2,710 |

The complete [matrix](final/README.md) records all 18 variants, exact image
hashes and raw build archives. Compared with the incoming source, `full`
shrinks from 39,145 to 38,964 CODE bytes and from 2638 to 2607 XRAM bytes. Its
short-call variant shrinks from 38,907 to 38,717 CODE bytes. The combined
Mouse Keys + Auto Shift short-call image shrinks from 40,403 to 40,203 CODE bytes
and from 2687 to 2654 XRAM bytes. That combination also fits without short calls:
40,427 CODE bytes, leaving 57 trailing bytes in the main window.

Main and low trailing space cannot be exchanged. The full-feature variants in the table retain 16
low-window trailing bytes; simpler profiles without One Shot retain 84. XRAM capacity is 3072 bytes, separate from 512 DMA
bytes. Stack capacity remains an allocation, not a runtime bound.

## Compact implementations

The encoder reuses one event object while retaining both waits and a fresh
release time. Mouse Keys cancels opposing direction pairs once. Numeric-string
buffers use normal implicit static zero initialization, allowing dead objects
and redundant stores to disappear. The Vial interpreter uses a 16-bit EEPROM
offset with the existing pointer-token call boundary; all 8192 macro bytes
remain available. See [optimization](optimization.md) and [review](review.md).

[GUI controls](../../../docs/GUI-CONTROL.md) add GU_ON, GU_OFF and GU_TOGG.
One output mask controls both GUI bits while preserving other modifiers,
One Shot and Repeat. The setting lasts until restart and writes no flash.

[Dynamic Macros](../../../docs/COMPACT-DYNAMIC-MACROS.md) add two volatile slots
of 16 completed keyboard taps. Each tap uses two bytes for usage and modifiers;
the unused high usage bit marks an unfinished press. Replay serializes taps
with at least 10 ms between phases, respects pending USB output and preserves
physical owners. Nested Vial primitives pause playback. The user guide lists
excluded event types and the difference from the full upstream engine.

Six layers, 16 Vial macros, 8192 macro bytes, eight two-key Combos, Combo offset
`0x658` and NVM schema `0x082002` remain unchanged. No base feature was removed.

## Verification and release boundary

Every variant passed 28 base suites and 273 base unit tests without skips, plus
14–24 selected supplemental suites. The same test-source hash binds every
variant. Exact linked tests include 25–27 Auto Shift scenarios, 26 Dynamic Macro
scenarios (27 with Auto Shift), and 11 GUI scenarios (12 with Dynamic Macros or
Mouse Keys + Auto Shift). The latter cases check raw GUI capture, GUI masking,
Auto Shift timing and balanced modifier release. Host checks include all 65,536
mouse direction pairs and the full 8192-byte EEPROM interval with sanitizers.

Independent review found and closed One Shot consumption by GUI controls,
Dynamic Macro execution inside Vial primitive ownership, a wheel-priority
change, host EEPROM-token fixture issues and a custom-toolchain test assumption.
See [review closure](review.md). Complete commands, logs and exact hashes are
retained with each image.

The foreground stack root remains unresolved; exact-image stack/IRQ release
qualification is not established. The real `package` command rejected the
changed `full` image because the committed source witness differs. This is the
expected result, recorded in [package-gate.json](final/package-gate.json).
Physical USB timing, scan behavior and power-loss persistence were not tested.

## Rejected experiments and tool repair

Adding Dynamic Macros to Mouse Keys + Auto Shift produced 41,288 CODE bytes,
ending at `0xca23`: 804 bytes lie above the permitted main window. The strict
build rejected it and the unsupported profile was removed. Its raw build is
retained in `integration-probes/full-mouse-auto-shift-dynamic-macro/`.

Broader callee-save lists made complete images larger. The smaller trial added 50
CODE bytes; the broader one overflowed. Neither flag change was retained.
Earlier isolated/probe evidence is retained under its original hashes and is
superseded for current measurements by the final frozen matrix.

The [short-call repair](shortcall-diagnostics.md) restores the original long
transfer when the pinned linker rejects a selected site, including a PC+2
boundary encoding that independent decoding accepts. It rebuilds from immutable
inputs and keeps strict final authentication. All 16 short-call tests run with
the selected pinned toolchain and zero skips.

## Research and reproduction

The [SDCC manual](https://sdcc.sourceforge.net/doc/sdccman.pdf) documents
three-byte generic MCS-51 pointers. EEPROM tokens in this port need 16 bits;
explicit bounds and the existing call boundary make the smaller cursor valid.
[SDCC patch 490](https://sourceforge.net/p/sdcc/patches/490/) discusses DPTR and
register tracking; [patch 504](https://sourceforge.net/p/sdcc/patches/504/)
discusses peephole rules and their liveness checks. Compiler replacement and
unqualified instruction rewriting were not imported. All measurements use the
pinned SDCC 4.6.0 toolchain. The [QMK Dynamic Macro controls](https://docs.qmk.fm/features/dynamic_macros)
and [Magic keycodes](https://docs.qmk.fm/keycodes_magic) provide familiar names;
the bounded AK820 behavior is described in its own guides.

See [Build profiles](../../../docs/BUILD-PROFILES.md) for setup and commands.
Only `full-mouse-auto-shift-gui` and `full-auto-shift-dynamic-macro` require
`--short-calls`; it remains optional and off by default for other profiles.
Use a fresh build directory for each configured build. No development image
inherits the published alpha.3 release approval.
