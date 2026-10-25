# Experimental register-save pass

`python3 tests/ak820_register_saves/test_register_saves.py` runs offline parser,
encoding and preservation checks. Set `AK820_ASSEMBLER` to pinned SDCC 4.6.0's
`sdas8051` to include real assembly and CFG adversaries. No device is opened.

With that assembler, SDCC 4.6.0 and s51 on PATH, run:

```
python3 tests/ak820_register_saves/cpu.py /tmp/new-register-cpu-result
```

The output directory must not exist. The fixture assembles both variants, links
with SDCC/aslink and executes both in s51. It checks eight register canaries,
A/DPL return values, restored SP and the two-byte reduction in SP at the callee.
The callee contains a local conditional branch and a private PUSH/POP pair.
Logs, HEX images and hashes remain in the output directory. This proves this
component fixture; it does not execute the complete firmware or qualify an IRQ,
startup, stack capacity or physical device.

`util/build_ak820.py --trim-register-saves` enables the experimental pass after
DCE's first assembly and before outlining. The default is off. Fresh listings,
source hashes, exact opcode checks, complete local control flow, balanced stack
joins and transitive clobbers are required. The window must contain one call,
contiguous unique register pushes and reversed pops, with no interior label.
Unknown callee paths, stack inspection, indirect IRAM, PSW/bank writes, computed
jumps and unrecognized instructions reject the proof. Ordinary caller operations
outside the window stay unchanged; their complete local CFG is still required.
Only XDATA/CODE reads are admitted in proved callees. No feature is removed.

`--outline-max-helpers N` separately changes the existing exact outliner cap;
it must be positive and defaults to 200. It does not enable register trimming.
