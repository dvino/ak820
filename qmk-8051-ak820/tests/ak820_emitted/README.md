# AK820 emitted-code regressions

Run against an existing complete SDCC build:

```sh
python tests/ak820_emitted/run.py \
  --build-dir .build/ak820 \
  --s51 /path/to/sdcc-4.4.0/bin/s51 \
  --output-dir .build/ak820-emitted-checks
```

The runner does not build the firmware, modify its input files or access a
physical device. It executes the linked IHX in the supplied uCsim C52 simulator.
Addresses are read from the current linker map and relocated listings, including
static symbols; compiler-generated temporary suffixes are not hardcoded.

It checks these actual emitted paths:

- Matrix snapshot, five-millisecond debounce, Fn+F1, releasing Fn before F1,
  and an ordinary A key press/release.
- A matrix-triggered macro with extended layer down/up and guarded recursive
  macro dispatch. It checks return/final layer and keyboard state, not every
  intermediate text report.
- Nonzero solid RGB and per-LED Direct colors, including grayscale and the last
  LED index, with the configured CIE curve preserved.
- Immediate LED clearing on USB suspend, no relighting during suspend, and
  restored Direct colors on resume.

The old rc1 image is expected to fail RGB assertions: its aggregate-result
wrapper leaves the renderer's result buffer zero, and its USB transition does
not invoke the RGB sleep handler. This makes it a useful negative control.

The test fixtures supply simulated NVM, matrix rows, elapsed time and USB
endpoint status. Generic C52 does not model VS11K28A oscillator, USB, LED DMA or
IAP hardware. The reported stack peak is measured only for each exercised CPU
path without IRQ overlap; it is not a proven worst-case bound. The fixture is
for the 82-LED AK820 release configuration and its two compiled default layers.
The rc4 profile exposes six dynamic layers; this runner exercises the existing
base/Fn paths. Additional layer layout, migration and reset behavior is covered
by the package/keymap regressions. New feature or layout configurations need
corresponding tests.

`results.json`, simulator command streams and complete logs are retained in the
selected output directory. A failing assertion returns a nonzero exit code.
