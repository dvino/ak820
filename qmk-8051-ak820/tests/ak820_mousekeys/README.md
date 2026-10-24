# Compact Mouse Keys tests

Run the production C with host time and USB seams:

```sh
python3 tests/ak820_mousekeys/host.py
```

Run the linked SDCC code with the existing feature-test C52 fixture:

```sh
python3 tests/ak820_mousekeys/run.py \
  --build-dir .build/<mouse-enabled-bounded-build> \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 \
  --output-dir /tmp/ak820-mousekeys
```

The linked suite requires a Mouse Keys build with compact NKRO control enabled.
It checks each direction and button, cursor and wheel thresholds, wraparound,
long gaps, diagonal and opposing movement, dragging, busy endpoint retries,
dropped movement backlog, unsupported keycodes, physical matrix dispatch,
unlock cleanup and NKRO mode cleanup. Host checks use the same production C
and additionally count sends to detect duplicate reports.

`--diagnostic-overflow` runs only direct ABI cases without the simulated NVM
map. It can inspect an over-limit exploratory image; that image is not
installable and cannot qualify the complete action pipeline.

All checks are offline. CPU results describe linked instructions on a generic
C52 with simulated matrix, NVM and endpoint readiness. They do not validate
VS11K28A peripherals, interrupts, physical USB, application scrolling or pointer
behavior on an operating system. No test opens a physical device.
