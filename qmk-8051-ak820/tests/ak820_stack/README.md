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
explored. Recursion, inconsistent loop heights, unbalanced returns, other SP
writes and unknown indirect transfers prevent an upper bound.

Two exact SDCC switch idioms are supported: a range-checked adjacent SJMP
table, and a range-checked pair of low/high target-byte tables. The complete
guard and dispatch sequence must match. The table bytes come from the IHX.
An isolated indirect jump never acquires targets merely because a table
follows it. Tests include changed guards, destinations, table lengths and
offsets that must fail closed.

A bounded value tracker also follows straight-line const-ROM pointer loads,
register moves and LCALL/RET thunks. Loaded bytes retain their ROM addresses;
call return bytes have separate provenance. Only a proven adjacent ROM-byte
pair above an actual call frame can select a callback. Its pushed pointer is
consumed by RET and its original call frame stays live during the callback.
Unknown values or instructions stop this recognizer. This uses the normal
SDCC bank-0 ABI and does not prove all dynamic callback tables.

`bound` excludes the root's entry return frame. It is a control-stack bound
under valid memory accesses and the normal instruction semantics. A null bound
means unknown; `explored_peak` then gives only a partial model observation.
Reachable instruction intersections help locate shared foreground/IRQ code,
but an empty intersection cannot establish absence while paths remain unknown.

This tool does not certify release safety. Shared static storage, data-pointer
safety, ABI preservation, startup, OEM wrappers, peripheral behavior and IRQ
nesting need separate evidence. No USB device is opened. The concrete first
analysis and remaining work are in
[the runtime report](../../../audits/rc6/runtime-stack-20261024/report.md).
