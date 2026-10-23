# RGB action table review

Independent review, 2026-10-23. GO for integrating the exact reviewed
`candidate.c` into source and then checking a combined build. No blocking
findings remain. This does not approve a packed release or a device update.

The reviewed private folder is
`qmk-8051-ak820/.build/rc6-rgb-action-table-probe-20261023`.
The candidate source SHA256 is
`2ddc67492d8c8e80f01b433a0d8ca00c3343dabe8f87f4ede82b3fdd991561a0`.
At review time, production `process_rgb.c` still matched `original.c`, SHA256
`658aee04c8015977c79db28bbd4917778b595059c877c385e6472c0d4fdd6f1e`.

I inspected the source difference, actual keycode enumeration, host harness,
probe and frozen link scripts, compile logs, emitted assembly, linked map,
memory reports, assembly evidence, CPU fixture and results, and the author
report `rgb-action-table-probe-20261023.md`. I did not run a compiler, touch
USB, modify production source or commit changes.

The ten keycodes occupy `0x7821` through `0x782A`. The compile-time check
covers every offset, including the existing forward/reverse aliases. Range
checking limits the index to zero through nine; Shift flips adjacent pairs
without leaving that range. The original edge test, one modifier read on
the selected edge, consumed return values and unknown-key return remain
intact. The table and removal of switch cases use matching opposite guards.
Generic, RGBLIGHT and disabled Matrix keycode profiles retain the original
source path. The host test executes board/generic and both trigger profiles;
RGBLIGHT and disabled profiles were checked by source inspection.

The SDCC output places twenty table bytes in CODE memory. Two `MOVC` reads
load a two-byte function address and `__sdcc_call_dptr` calls it. All ten
targets survive dead-code removal and appear in the linked map. The old
helper is removed. This agrees with `asm-evidence.json` and the pointer-width
assertion. There is no generic-pointer conversion in the table lookup.

The frozen control reproduces the baseline IHX exactly. Independently read
hashes agree with the reports: control
`ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`,
candidate
`c85ab09532aaba4332fa3ee14e5c1b10ecbd48696dbd7a8d5aa2096e667a3c4a`.
The link script copies baseline assembly and replaces only this translation
unit before the same removal, outlining and link steps. Thus the private
comparison does not include later unrelated production changes. It saves
216 CODE bytes and four XRAM bytes: 39,432 to 39,216 and 2,071 to 2,067.
Low-window use remains 1,859 bytes; available stack remains 152 bytes.

The saved host results pass 524,288 events in each of four profiles. The
harness compares returns, action identity/count, modifier state and modifier
read count for all 16-bit keycodes, both edges and four Shift combinations.
The C52 report passes 200 events for each of five state seeds, comparing
the actual linked RGB state, return, modifiers, dirty flag, change time,
render state and reactive ages. A separate 200-event callback fixture per
image checks exact action identity and count through the linked dispatch.
Its simulated-ROM callbacks use separate stubs reached by three-byte jumps,
so adjacent six-byte wrappers are not overwritten. The earlier fixture-only
overlap was corrected; no firmware correction was needed.

Actual-action CPU runs use 20 stack bytes for control and 22 for candidate.
The extra two bytes agree with the emitted register saves. These peaks cover
the exercised calls, without interrupt overlap; they are not a whole-firmware
worst-case stack proof. Host and simulated CPU results do not prove physical
RGB, timing, USB, persistence or device behavior. A combined source build and
its checks remain required after integration.
