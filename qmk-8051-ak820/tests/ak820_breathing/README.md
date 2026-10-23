# Breathing CPU check

Run this against an existing compact-CIE SDCC build. It does not compile firmware
or access a keyboard. Use a Linux Python and the supplied Linux `s51` binary;
on Windows run them through WSL.

```sh
python3 tests/ak820_breathing/run.py \
  --build-dir .build/rc6-optimized-breathing-20261023 \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51 \
  --output-dir .build/rc6-breathing-cpu-20261023
```

The runner loads the actual IHX image in uCsim C52. It resolves retained symbols
from the map and relocated listings, then supplies simulated timer and peripheral
memory through the existing emitted-test fixture. Results, simulator commands
and logs go to the chosen output directory. A failed check or timeout returns a
nonzero exit status. Nothing is restored, retried or sent to USB.

Checks cover all 161 supported inputs to the breathing curve helper and 50
complete frames of 82 LEDs. Frames include saturated colors, grayscale, phase
boundaries and wrap, eight-LED task cooperation and the 16-bit timer return ABI.
The helper is compared with the separate full 256-entry source curve; channel
error must stay within one. Full-CIE and no-CIE build variants are not executed.

The reported stack peak covers these calls without interrupt overlap. Generic
C52 simulation cannot prove physical timing, visible smoothness, DMA transfer,
USB behavior, storage durability or a global stack bound.
