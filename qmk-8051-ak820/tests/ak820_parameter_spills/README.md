# Parameter-copy guard checks

Run from the repository root:

```sh
python3 qmk-8051-ak820/tests/ak820_parameter_spills/test_integration.py
```

The eleven tests use frozen SDCC typed output for normal, volatile, pointer and
escaped formals. They check ambiguous/missing metadata, inline assembly,
escaped literals, unsupported ABI flags and wrong-image rejection. Fixture
hashes are in `fixtures/sha256.json`; `adversaries-noasm.c` is their source.
The ADB fixture shows why debug types alone cannot prove nonvolatile storage.
These tests do not invoke a compiler or simulator and do not qualify firmware.

The pass is experimental and default-off. A full build needs an independently
reviewed context certificate, then a new-image postlink audit. See
[compression status](../../../docs/MAXIMUM-FUNCTIONALITY-STATUS.md) for exact
linked measurements, CPU comparisons and remaining resource/hardware gates.

## Immediate DPTR overwrite

The v2 pass may omit the final three-byte DPTR restore only when the next
instruction is a source/listing-aligned, contiguous, three-byte `0x90`
`MOV DPTR,#...` using a bare C symbol or fixed 16-bit literal. Expressions,
including the assembler's current-location counter, are rejected because
removing bytes moves the instruction. Only blank lines and comments may intervene. Labels,
directives, area changes and every other instruction block this enhancement.
The following instruction stays unchanged. Existing private-formal, valid-C,
byte, storage, context and postlink checks still apply.

Reports retain `boundary_state_replacement_only` and add
`emitted_replacement`. For an admitted site the prefix endpoints may differ
in DPL and DPH. The report claims equivalence only after the identical
following instruction overwrites both bytes. Ordinary foreground execution
and IRQ wrappers that preserve DPTR remain prerequisites. This saves three
object bytes per admitted site before outlining interactions; it predicts no
linked-image saving.

Run the admission tests and the isolated CPU comparison with:

```sh
python3 -m unittest discover -s qmk-8051-ak820/tests/ak820_parameter_spills -p 'test*.py'
python3 qmk-8051-ak820/tests/ak820_parameter_spills/cpu_dptr_restore.py \
  --s51 /absolute/path/to/sdcc-4.6.0/bin/s51 --output-dir /tmp/dptr-results
```

The CPU comparison uses representative machine-code replacements for the
existing prefix plus the next full overwrite and the shortened prefix plus
that same overwrite. It does not replay each selected compiler instance.
It covers widths one through four, all 256 initial PSW values, all four
register banks, full IRAM and SFR observations, XRAM canaries and a shared
continuation PC. Interrupts and timers are disabled; cycle counts differ.
This isolates the new enhancement. It does not replace original-spill CPU
checks, exact-image stack/IRQ checks, linking or physical validation.

Component verification on 2026-10-25: all 15 host tests passed. The pinned
SDCC 4.6.0 `s51` comparison passed 1,024 cases (2,048 executions). Simulator
SHA256: `61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd`.
The command script, complete CPU log and `results.json` are retained in the
external `continuation-artifacts/dptr-component-final` evidence directory.
