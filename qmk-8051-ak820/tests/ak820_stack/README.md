# Exact-image control-stack analysis

Run from the repository root:

```sh
python -m unittest discover -s qmk-8051-ak820/tests/ak820_stack -v
python qmk-8051-ak820/tests/ak820_stack/analyze.py \
  --build-dir qmk-8051-ak820/.build/new \
  --output qmk-8051-ak820/.build/new/control-stack.json
```

The analyzer reads IHX, MAP and every relocated RST listing. It checks IHX
checksums, validates opcode lengths independently and compares each listed
instruction byte with the image. Missing runtime-library bodies are decoded
directly from the image using the shared 8051 opcode-length table. Overlapping
instruction entries are rejected. The report hashes the image, map, listings,
analyzer and decoder source. Exit status 2 means a requested root has unresolved
paths; malformed inputs fail before producing a new report.

Direct calls add the two-byte return address. Tail jumps retain the current
frame. PUSH, POP and constant INC/DEC SP are tracked. Every branch outcome is
explored. Unproved recursion, inconsistent loop heights, unbalanced returns, other SP
writes and unknown indirect transfers prevent an upper bound. There is no
arbitrary call-depth limit; cyclic contexts fail closed.

Exact SDCC switch idioms include: a range-checked adjacent SJMP
table, and a range-checked pair of low/high target-byte tables. The complete
guard and dispatch sequence must match. The table bytes come from the IHX.
An isolated indirect jump never acquires targets merely because a table
follows it. Tests include changed guards, destinations, table lengths and
offsets that must fail closed.

Register-index tables also accept a complete ADD #-count carry guard with
either branch polarity. The same register supplies the guarded index and both
ROM-byte lookups, or the index multiplied by three selects adjacent three-byte case slots.
The recognizer rejects intervening instructions, changed index registers,
wrapped offsets, incomplete tables and entry at an unguarded indirect jump.
A complete pair of unsigned 16-bit comparisons can also bound a normalized
split-table index. Small straight-line ROM getters can establish equal A/Rn
values before the guard, or return a masked accumulator for an SJMP table.
Only the documented instruction subsets are accepted. Candidate reads do not
claim instruction boundaries until actual traversal reaches them.

A masked bit table accepts ANL A,#mask, a saved register, multiplication by
three and adjacent CLR bit/RET slots. All 256 possible input bytes are checked,
including byte arithmetic wrap. Hardware-register ranges are not inferred.

A bounded value tracker also follows straight-line const-ROM pointer loads,
register moves and LCALL/RET thunks. Loaded bytes retain their ROM addresses;
call return bytes have separate provenance. Only a proven adjacent ROM-byte
pair can select a callback. The pair must be pushed above a real call frame
for a RET thunk, or loaded into DPTR with a zero accumulator for a tail jump. Its pushed pointer is
consumed by RET and its original call frame stays live during the callback.
Unknown values or instructions stop this recognizer. This uses the normal
SDCC bank-0 ABI and does not prove all dynamic callback tables.

A separate ROM callback recognizer checks the complete unsigned 16-bit range
comparisons, normalization, optional XOR, local spill/reload, multiplication by
two and const-ROM pointer getter. Both guarded exits and every selected table
slot are analyzed. Helper bodies and saved registers are included in the bound.
Tests change guards, register identities, XOR, spills and helper targets.

Private bool guards can close a recursive path. The report records the private
object, source hash and exact read/write sites. After C line splicing and
comment/literal stripping, every identifier use must be one of four complete
statements: the private bool declaration, early-return guard, true setter and
false reset. Each must occur once. Address taking, parentheses around an escape,
macro arguments and any other use fail closed. An exact immediate nonzero write
establishes an owned state; an unproved reference discards it. Only the complete
MOV DPTR/MOVX/JZ/RET sequence can use that state for an early return. Calls carry
the state in their analysis context, and callees must preserve incoming owned
states. A changed guard, zero setter, wrong cell or callee clear fails closed.
This relies on valid C memory accesses and the normal compiler object layout;
it does not establish safety against arbitrary RAM aliasing or corruption.

`bound` excludes the root's entry return frame. It is a control-stack bound
under valid memory accesses and the normal instruction semantics. A null bound
means unknown; `explored_peak` then gives only a partial model observation.
Reachable instruction intersections help locate shared foreground/IRQ code,
but an empty intersection cannot establish absence while paths remain unknown.

This tool does not certify release safety. Shared static storage, data-pointer
safety, ABI preservation, startup, OEM wrappers, peripheral behavior and IRQ
nesting need separate evidence. No USB device is opened. Current development images have an unresolved foreground stack root; see the
[development matrix](../../../audits/rc6/compact-runtime-20261024/final/README.md).
The exact published alpha.3 image has separate
[release evidence](../../../audits/rc6/alpha3-release-20261024/review.md).
