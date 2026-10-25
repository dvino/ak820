# VIA parser compaction model

Run from the repository root:

```sh
docker run --rm --network none -v "$PWD":/work -w /work ak820-nkro-study-env:local python3 tests/protocol_compaction/run.py
```

The test compiles the complete production VIA parser and the saved pre-change
parser with native AddressSanitizer and UndefinedBehaviorSanitizer. It compares
all 32 reply bytes and ordered operation traces for 524288 packets. Cases cover
all command IDs and buffer size bytes, with randomized remaining packet bytes,
unlocked and unlocking states,
macro-write success and failure, and valid and invalid packet lengths.

Storage and transport operations are trace-producing stubs. This checks parser
routing and reply semantics; it does not qualify storage, firmware size, target
ABI, stack usage, IRQ behavior or a physical device. Vial dispatch is a stub;
this experiment does not change the Vial parser or its existing packet adapters.
