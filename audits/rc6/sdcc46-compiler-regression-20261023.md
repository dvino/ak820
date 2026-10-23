# Boolean stores in SDCC 4.6

Date: 2026-10-23. No keyboard command, compiler patch or firmware source change
was made for this check. The supplied plain-language rules and writing-style
skill were applied; no personal writing retrieval was available or claimed.

The offline compiler gate **fails in both SDCC 4.4.0 and 4.6.0**. The tested
near-pointer store leaves the old Boolean byte unchanged, for both false and
true. This is a real compiler defect, not a new 4.6-only regression. The actual
4.6 linked image passes the eight targeted key-event checks below. That result
does not turn the general compiler gate into a PASS.

[Patch 513](https://sourceforge.net/p/sdcc/patches/513/) describes a comparison
result held in carry with size zero. Pointer-store generation can discard
that value. Its accepted change makes the operand size one for `POINTER_SET`;
it was applied in r16814 on 2026-08-26, after the tested 4.6.0 #16555 release.
[Bug 3845](https://sourceforge.net/p/sdcc/bugs/3845/) gives the Boolean member
example. Both official pages were read on 2026-10-23. No fix was backported.

## Isolated compiler and CPU checks

`tests/ak820_compiler/fixture.c` tests eight shapes with false and true inputs.
The destination starts at the opposite value, so omitting a store fails both
cases. The bitfield check also checks that the adjacent count stays nine.

| Compiler and flags | Correct cases | Result |
| --- | ---: | --- |
| 4.4.0 #14620, size, large, SDCC11 | 14/16 | FAIL: near pointer |
| 4.6.0 #16555, same flags | 14/16 | FAIL: near pointer |
| 4.4.0, same plus current audited callee list | 14/16 | Same failure |
| 4.6.0, same plus current audited callee list | 14/16 | Same failure |

In each run, false expected zero but read one; true expected one but read zero.
The 4.6 `near_store` ASM ends after the comparison with `free result` and
`ret`; it has no store through the saved near pointer. The XDATA and generic
pointer stores, comparison return, key-record comparison/parameter stores and
bitfield stores pass. The callee list is exactly the eleven names recorded in
the full build report. The fixture calls none of those functions, so this
control tests flag interaction, not their calling conventions.

Private evidence is under `qmk-8051-ak820/.build/`:
`compiler-gate44-v3-20261023`, `compiler-gate46-v3-20261023`,
`compiler-gate44-callee-v3-20261023`, and
`compiler-gate46-callee-v3-20261023`. Each contains `results.json`, the linked
fixture, emitted ASM and CPU/compile logs. Earlier v1/v2 scratch runs are not
the final evidence. The reusable command and output rules are in the test README.

## What the retained image actually does

The inspected 4.6 image is
`qmk-8051-ak820/.build/rc6-sdcc46-full-experiment-20261023/ajazz_ak820_vial.ihx`,
SHA256 `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.

The near-space search covered `quantum`, `keyboards/ajazz/ak820`,
`platforms/mcs51`, `tmk_core/protocol/ch555` and `lib/ch555`, including headers.
There are no explicit `__data`/`__idata` Boolean pointer signatures or casts in
these source trees. The only active explicit near declarations are ten scalar
`uint8_t` GPIO locals (`port` and `pinmask` in five GPIO functions), and integer
typedefs in `lib/ch555/ch555.h`. Its near-pointer aliases `PUINT8I`, `PUINT16I`,
`PUINT32I` and `PUINT8DV` have no uses beyond their declarations in those trees.
The commented timer declaration is inactive. The host-only dummy macro header
does not establish target memory placement. With model-large, the unqualified
record locals are XDATA; unqualified public record pointers are generic.
Their emitted objects and generic tag zero at calls confirm the current case.

A search of all 64 retained `dce/**/*.asm` files found one `mov @r0/1,...`
near indirect store: `quantum/main.asm:607`, in the compiler-supplied
`sdcc_atomic_compare_exchange_idata_impl`. It writes the supplied r3 byte after
comparison, not an `AOP_CRY` Boolean result. The atomic exchange near helper
uses `xch`. No C near Boolean-member store candidate was found in this source
inventory. Absence of a store instruction alone is not proof: the defective
fixture omits that instruction, which is why both source and emission were
checked. The inventory is scoped to the retained firmware and these target
trees, not every optional QMK platform or an arbitrary future configuration.

| Retained source shape | Emitted code and applicability |
| --- | --- |
| `keyboard.c:600,604`: mask to Boolean, then `MAKE_KEYEVENT` | `keyboard.asm:1140` materializes carry with `clr a; rlc a`, keeps the byte in r0 and writes it with `movx @dptr,a` at event offset five. The event is XDATA, not a typed near destination. |
| `action.c:103`: copy event to current record | `action.asm:696` calls `___memcpy` for six event bytes to XDATA; offset five carries the already materialized Boolean. No new comparison-to-near store. |
| `encoder.c:180,183,192,195`: four event factories | The retained encoder ASM writes explicit 1/0 bytes through DPTR for CW/CCW press/release. CW row is 0xfd and CCW row is 0xfc. |
| `repeat_key.c:62,96,116`: record/event copies | Retained ASM uses whole-record/event copies, not a comparison result stored through a near Boolean pointer. These copies were inspected statically; this new test does not execute the repeat-key feature. |
| `action.h:41` tap Boolean bitfields | `config.h:18` defines `NO_ACTION_TAPPING`; the current `keyrecord_t` omits `tap`. There is no retained `action_tapping.asm`. The private fixture exercises the bitfield independently. |

`linked.py` executes the actual 4.6 IHX and checks eight observations: matrix
press/release objects, their action records, and all four encoder event
objects. All eight pass. The same test against the 4.4 control build also
passes 8/8. Final CPU evidence is in `compiler-linked46-v3-20261023` and
`compiler-linked44-v3-20261023`; the former records peak simulated SP 150,
52 bytes above its linked initial SP. That is exercised stack use only.

For these retained key-event paths, the discovered defective near-store shape
is absent and both Boolean values execute correctly. Other Boolean uses and
all possible input paths have not been exhaustively proved here. Optional
features, future near-pointer changes and a new compiler still require the
failing general gate to be addressed explicitly. Release acceptance must not
claim global compiler correctness from this bounded applicability result.

Independent review is required before commit. The lead owns review closure and
the wider regression/release decision. No physical or installed-device test
was run by this work package.
