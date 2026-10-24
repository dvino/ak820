Русский перевод: [Проверки](ru/TESTING.md).

# Testing

The published `v0.6.0-alpha.3` image passed the recorded CI suites and has
limited device-check evidence. Exact build and device results are in
[Status](STATUS.md). Host models and linked CPU execution do not prove physical
keyboard behavior. Detailed feature checks and behavior after full power loss
remain untested.

## Offline regression suite

From the repository root, run the offline suite and its supporting unit tests:

```sh
python tools/test_keyboard.py
python -B -m unittest discover -s tools/installer -p 'test_*.py' -v
python -B -m unittest discover -s qmk-8051-ak820/tests/ak820_inventory -p 'test_*.py' -v
```

The combined runner records commands, exit codes, hashes and skips. For full
qualification of an already linked image with pinned tools:

```sh
python tools/configure_firmware.py qualify \
  --build-dir qmk-8051-ak820/.build/local-1 \
  --toolchain toolchains/sdcc-4.6.0
```

This checks input/report handling, Caps Word, Repeat and Alt Repeat, Grave
Escape, Tri Layer, tap-hold, Combos, macro processing, RGB and NVM behavior
covered by host or CPU fixtures. Coverage depends on the selected runner and
build; consult the generated report. The standard offline IRQ check uses a
public OEM instruction fixture and does not require private ROM. CPU fixtures
model peripheral operations and do not emulate VS11K28A USB or flash silicon.
A tested stack peak is not a global bound.

For the nine curated packages, use the finite profile-catalog builder. List its
nine-row CI matrix with `--list`, then build and qualify all selected exact
images:

```sh
python tools/build_profile_catalog.py --list
python tools/build_profile_catalog.py \
  --build-root qmk-8051-ak820/.build/catalog \
  --output .build/profile-catalog
```

The output path names a fresh directory; the ZIP and its SHA256 file are created
beside it. The builder checks stack and interrupt bounds for each exact image before its
regression gates. `--resume` requalifies existing linked images and reruns the
gates; it does not skip checks. The catalog is offline evidence, not approval to
flash a device. Current qualification and release state are in [Status](STATUS.md).
See [Build profiles](BUILD-PROFILES.md) for individual package builds and legacy
CLI profiles.

The automatic suite requires no key presses, encoder movement, cable reconnect
or manual Vial unlock. It does not write to the keyboard. Live protocol tests
are a separate later procedure. Their default plan is read-only; setting writes
require explicit execution options and authorization. Timeouts, storage faults
and failed readbacks are failures and stop the run. The runner must not blindly
retry, reset, restore or enter the loader.

## Live checks and limits

The live regression runner can check all 83 matrix assignments on six layers,
encoder assignments in both directions on six layers, 16 macro slots and the
8192-byte macro view, RGB settings and supported getters. Read-only results do
not prove physical switches, scan timing, encoder signals, macro playback,
lighting appearance or durable storage. The published image has been installed
and its settings backup and restore path was checked; see [Status](STATUS.md)
for the exact scope. Separate physical feature checks and power-loss durability
remain untested.

For later authorized read-only diagnosis, use a private session and a fresh
output directory:

```sh
python tools/ak820_device_tests.py --run \
  --release-dir /path/to/extracted-alpha3-firmware-bundle \
  --approval /path/to/exact-alpha3-approved-release.json \
  --session /path/to/permanent-session-for-the-same-alpha3-image \
  --output host/runs/post-flash-1
```

The release directory, approval file and session must identify the exact image being diagnosed. A fresh installation/recovery session is required; an OEM-only backup or settings backup is not sufficient. Do not use the legacy `releases/rc6` directory with an approval for a different image. The plan and results remain in the private output directory. Setting-write checks need the runner's explicit write options and authorization. These tests do not flash the keyboard or require physical actions.

## Physical acceptance

Physical checks require explicit confirmation before any flash. Verify typing,
modifiers, media keys, each physical key, encoder press and both directions,
Combo timing, lighting appearance, unlock/update behavior and settings after
restart and full power removal. Record the exact image hash, device variant,
steps and results. Host or CPU passes do not substitute for these checks.

## CI

[CI and releases](CI.md) describes branch checks and tag publication. CI runs
offline regressions and builds packages; it does not operate a device.
