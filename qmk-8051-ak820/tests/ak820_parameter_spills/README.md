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
