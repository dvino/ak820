Русский перевод: [Проверка стека](ru/RUNTIME-STACK.md).

# Offline runtime stack check

`configure_firmware.py check-runtime` checks whether the linked firmware has enough internal RAM for its foreground call stack, startup path and interrupt handlers. The check uses the exact image and map file in an existing build directory; it does not rebuild the firmware or communicate with a keyboard.

Run it from the repository root:

```sh
python tools/configure_firmware.py check-runtime \
  --build-dir qmk-8051-ak820/.build/candidate \
  --toolchain toolchains/sdcc-4.6.0
```

The command returns success only when all required paths have known bounds and the combined bound fits the linked stack capacity. A failure means the evidence is missing, inconsistent, unresolved, or exceeds capacity. Inspect `runtime-safety/summary.json` and the reports and logs beside it. The check records hashes for the image, map, checkers and evidence so results cannot be reused for a different build. Every new source profile or image must pass this proof before any other regression checks. The build fails if a required bound is unknown or stack capacity is exceeded. `check-runtime` reruns the evidence for an existing build.

The bound begins at C runtime entry with `IE=IE_EX=0`, as supplied by the packer, and includes the persistent call frame entering `main`. This premise is part of the proof; it does not cover pre-CRT trial erase. It assumes valid C memory accesses, the SDCC register-bank-0 ABI and MCS-51 interrupt in-service behavior. Interrupt wrappers are checked against a pinned public instruction fixture. The fixture does not establish a connected device's identity.

This check produces static and CPU-model evidence. Pre-CRT trial erase, physical timing, power loss and device behavior require separate checks. Source code, linked-image CPU results and behavior of the installed or released alpha.3 image are separate facts; this check proves only the exact linked image named in its report. Runtime stack success does not approve a release or a settings transition. Results and independent review are in the [technical report](../audits/rc6/web-firmware-20261024/runtime-all/README.md).


## Whole-image coverage

The foreground root is `_main`, including every reachable call required by the
linked feature set. Startup is checked separately, including the frame left
on the stack when CRT calls `main`. USB, timer and LED are the three enabled
interrupt sources. Their wrappers and callback roots are included for all
15 possible orders of distinct sources. Unknown required calls or IRQ behavior
fail the gate. The combined allowance is compared with the stack capacity in
that image's MAP/MEM, not with a value from another profile.

## References

- [SDCC Compiler User Guide](https://sdcc.sourceforge.net/doc/sdccman.pdf)
- [Intel MCS-51 Microcontroller Family User's Manual (1994)](https://bitsavers.trailing-edge.com/components/intel/8051/MCS-51_Users_Manual_Feb94.pdf)
