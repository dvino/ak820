# Delay register preservation

Run against the selected linked image:

```sh
python3 -I tests/ak820_delay/run.py --build-dir .build/candidate \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 --output-dir .build/candidate/delay-abi
```

The AK820 header adds `mDelayuS` to SDCC's callee-save set. Its generated
prologue preserves R6 and R7, so `mDelaymS` no longer saves all eight registers
around each call. All callers and the definition include the same header.

Seven CPU cases execute the actual linked microsecond and millisecond delay
functions. They check all eight registers, stack balance and completion of the
loop counter, including zero and a count that crosses a byte boundary.
`configure_firmware.py build` includes this check for every profile.

The loop body is unchanged. Call overhead is smaller; the CPU model does not
measure physical elapsed time or prove USB wake timing.
