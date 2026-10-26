# Bounded optimization checks

Run from the QMK source directory:

```sh
python tests/ak820_bounded/run.py --output .build/bounded-host.json
python tests/ak820_bounded/emitted.py --build-dir .build/ak820 --s51 /path/to/s51
```

The host runner extracts the production journal validator and macro delay
expression. It checks every legal nonzero delay byte pair (65,025), every
single-byte header mutation, and every complement-byte pair in all four header
positions (264,448 header cases). It also compares the rejected shift/subtract
expression, so its arithmetic remains reproducible without adopting it.

The real macro interpreter and string walkers run with the existing guard
harness. Extra cases cover all sixteen macro IDs with zero and maximum delays,
zero delay operands and playback after each early exit. Complete stored streams
are the publication contract. Arbitrarily truncated encoded operands are not
accepted input to this playback harness; publication validation is checked by
the separate macro storage suites.

The linked runner calls the retained private journal helper in an existing
SDCC image. It checks 2,304 single-byte mutations against a literal valid header,
reads the Boolean return from DPL and reports the exercised helper stack peak.
It supports both the earlier generic pointer and the private XDATA pointer.
The nine-byte simulated XRAM buffer starts immediately after all retained
XDATA areas in the exact linked map, including initialized XDATA. The map's
end must agree with the memory report. The whole buffer must fit inside
ordinary XRAM, 0x0440 through 0x0fff, above the fixed native, LED DMA and IAP
stage reservations. Missing bounds, conflicting reports or insufficient space
stop the run. Results record the areas, fixture bounds and image/map hashes.
The runner changes simulated memory only.

Host agreement, linked CPU execution and stack capacity are separate evidence.
These checks do not prove electrical flash durability, real peripheral timing,
USB interaction, physical inputs or stack usage with interrupt overlap. Run the
existing NVM diagnostic, power-cut and linked IAP suites for recovery and fault
propagation coverage.
