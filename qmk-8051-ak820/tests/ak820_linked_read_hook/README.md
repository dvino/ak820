# Linked EEPROM read hook check

`check.py` checks the actual linked `eeprom_read_byte` entry, its exact tail jump to the unique `read_offset` listing label, and every reachable instruction, including outlined helpers. The existing stack analyzer loads and validates the IHX against linked RST bytes. Its bounded closure must agree exactly with the new finite effect walk.

Both `pass25.json` and `final26b.json` pass. Each closure contains 45 instructions and requires two additional stack bytes beyond its incoming return frame. The closure writes only A, B, DPTR, arithmetic flags and its own bounded stack. It contains no R0–R7 write, PSW bank-select write, indirect IRAM write or storage write. The read operations are MOVX and MOVC. Push/pop operands must match in LIFO order; a callee cannot pop through its return frame. Unknown opcodes, indirect control transfers, cycles, missing bytes, unequal closures and unequal stack bounds fail the check.

Seven negative controls change both the instruction map and image bytes consistently. R0 writes, PSW writes, indirect IRAM writes, SP writes, wrong DPTR pops, register-alias pops and storage writes are all rejected. These controls test effect checks rather than relying solely on an IHX/RST mismatch.

The result assumes bank zero on entry, a valid nonwrapping stack disjoint from register banks and live data, and sufficient capacity for the incoming return frame, two extra bytes and enabled interrupts. Interrupt handlers must preserve interrupted registers, bank selection, SP and live stack. Whole-program stack capacity and interrupt bounds require separate evidence for the same image. The result proves register preservation under these assumptions; it does not prove read values, flash behavior or device behavior. No writer-hook proof is included.

The original external hook checker was unavailable. This checker was authored for these linked images. Each JSON report records the IHX, map, linked listing, analyzer and checker SHA256 hashes, the complete reachable byte sequence and mutation outcomes.

Run from the repository root:

```sh
python3 qmk-8051-ak820/tests/ak820_linked_read_hook/check.py \
  --build qmk-8051-ak820/.build/resume26b-state-bytes \
  --analyzer qmk-8051-ak820/tests/ak820_stack/analyze.py \
  --output /tmp/read-hook.json
```

The reviewed final result is retained in
[read-hook.json](../../../audits/maximal-continuation-20261025/read-hook.json).
