# Combined optimization RGB CPU comparison

The combined optimization build passes the linked C52 CPU comparison against
the optimized-breathing baseline. This verifies the RGB key handling covered
by the model after the combined changes. It does not test the keyboard or
prove physical behavior.

The private verifier is
`qmk-8051-ak820/.build/rc6-optimization-batch-verification-20261023/rgb_cpu.py`.
It reuses the emitted-test C52 runner and accepts baseline, candidate and
output directories as arguments. It changes no firmware source. The result is
in `qmk-8051-ak820/.build/rc6-optimization-batch-verification-20261023/cpu-rgb/rgb-cpu-report.json`.

The run compares linked output from
`qmk-8051-ak820/.build/rc6-optimized-breathing-20261023` with
`qmk-8051-ak820/.build/rc6-optimization-batch-20261023`. The combined build
report records 39,144 code bytes. The compared IHX files are 94,368 bytes for
the baseline and 93,696 bytes for the combined build. Their SHA256 values are:

- Baseline IHX: `ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`
- Combined IHX: `4b68ae92d95538e4c0af1d445c723645b1d7f570b3ea206002d7521b45fe7ce3`
- Baseline BIN: `67726dd77d559b2098e765d4d9fd92eb0b82252441397b6ca180a8982adb398c`
- Combined BIN: `06a9d6a061113a0c4ac6ad7cafcacf43965f32331deae7368d30c91df25823b9`

For each image, the CPU runner tested 200 keycode, pressed-state and modifier
combinations at each of five RGB state seeds: 0, 1, 127, 240 and 255. It
compared the boolean return, all eight RGB configuration bytes, real modifier
state, dirty flag, timestamp, rendering flag and all 82 reactive LED ages.
Every baseline and combined observation matched. A separate 200-case pass in
each image checked the exact callback ID and call count. That pass substitutes
simulated ROM capture stubs at callback entries; the state passes execute the
linked production actions. The production three-byte generic-pointer ABI is
used, with an XDATA pointer and the pressed byte at offset five.

The baseline reached stack pointer 123 (20 tested bytes above the initialized
stack) in each state pass and in the callback pass. The combined build reached
125 (22 tested bytes) in each state pass and 123 (20 bytes) in the callback
pass. The two-byte increase applies to these tested state paths; it is not a
global stack bound, especially with interrupts.

The run used this command from the repository root:

```sh
python3 qmk-8051-ak820/.build/rc6-optimization-batch-verification-20261023/rgb_cpu.py \
  --baseline qmk-8051-ak820/.build/rc6-optimized-breathing-20261023 \
  --candidate qmk-8051-ak820/.build/rc6-optimization-batch-20261023 \
  --output qmk-8051-ak820/.build/rc6-optimization-batch-verification-20261023/cpu-rgb
```

This is CPU-model evidence only. It does not verify USB protocol behavior,
durable-storage writes, physical RGB output, timing or interrupt behavior.
No USB write, loader transition, reset or flash operation was performed.
