# USB setup comparison

Run `python3 tests/ep0_compaction/run.py` with GCC available. This compares the
saved USB implementation with the current source under ASan/UBSan, including
the existing USB fixture and 131072 generated IRQ traces. Hardware and storage
are mocked; this is not execution of the full linked firmware.

`cpu.sh` compiles the scalar predicates using SDCC and runs them in s51.
It checks all 65536 words for twelve value/interface predicates. This emitted
code check does not establish full USB timing, IRQ ownership or stack safety.
The three cached BIT locals still need exact-image allocation/IRQ checks.
