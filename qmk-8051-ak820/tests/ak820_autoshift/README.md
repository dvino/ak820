# Compact Auto Shift tests

Run these commands from `qmk-8051-ak820`. They run offline and do not open USB:

```sh
python tests/ak820_autoshift/host.py --output .build/as-host.json
python tests/ak820_autoshift/linked.py \
  --build-dir .build/full-auto-shift \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 \
  --output-dir .build/as-linked
```

The linked runner requires an image built with `AK820_COMPACT_AUTOSHIFT=yes`,
One Shot, Space Cadet and NKRO controls. Its highest code address must be below
`0xc700`, where the simulator places fake NVM. An overflow diagnostic image must
not be used. The build report must identify the enabled features before a
release; an environment-only probe does not update the profile catalog.

The host suite compiles the production Auto Shift engine, action pipeline,
Combo engine, modifier owners and relevant Quantum handlers. It shares the
existing tap-hold fixture's hardware hooks. UBSan is enabled. Four deliberate
mutations must fail: an early threshold, a changed release keycode, a missing
Shift release and a missing cancellation.

Coverage includes every accepted keycode,174/175ms boundaries, timer wrap,
interruption order, remapping, real Shift ownership, Ctrl and One Shot bypass,
Caps Word, shifted Repeat and Alternate Repeat, Combo fallback and outputs,
dual-role taps, Space Cadet, encoder and generated key exclusion, cancellation
and session controls. The C52 runner observes the production pipeline's reports
and actual send callbacks. Unlock and NKRO-switch cancellation are executed in
the linked code.

The fixtures simulate CPU execution and endpoint-ready state. They do not model
physical keys, the VS11K28A peripherals, interrupt overlap, USB host repeat or
persistent NVM writes. Firmware is not flashed by either command.
