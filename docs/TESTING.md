Русский перевод: [Проверки](ru/TESTING.md).

# Testing

The released and installed `v0.6.0-alpha.2` passed 28 suites and 270 unit
tests with no skips in tag CI. Exact build and device evidence are in
[Status](STATUS.md). Host models and linked CPU execution do not prove physical
keyboard behavior.

## Offline regression suite

From the repository root, run the offline suite and its supporting unit tests:

```sh
python tools/test_keyboard.py
python -B -m unittest discover -s tools/installer -p 'test_*.py' -v
python -B -m unittest discover -s qmk-8051-ak820/tests/ak820_inventory -p 'test_*.py' -v
```

The combined runner records commands, exit codes, hashes and skips. For the full
qualification with pinned tools and a fresh firmware build:

```sh
python tools/test_keyboard.py --host --require-toolchain \
  --toolchain toolchains/sdcc-4.6.0 \
  --build-dir qmk-8051-ak820/.build/local-1 \
  --iap-fault-profile guarded-erase --output host/runs/qualification.json
```

This checks input/report handling, Caps Word, Repeat and Alt Repeat, Grave
Escape, Tri Layer, tap-hold, Combos, macro processing, RGB and NVM behavior
covered by host or CPU fixtures. Coverage depends on the selected runner and
build; consult the generated report. IRQ/device fixtures may require private
OEM references. CPU fixtures model peripheral operations and do not emulate
VS11K28A USB or flash silicon. A tested stack peak is not a global bound.

For `standard`, `nkro` or `one-shot`, use the dedicated [profile build
command](BUILD-PROFILES.md). It runs the required offline suites against the
exact linked image and records the result in that build directory. Profile
results do not prove physical behavior or release eligibility. In particular,
there is no reviewed whole-program stack bound, exact-image interrupt/nesting
proof or approved installer transition yet; see the
[qualification report](../audits/rc6/configurable-20261024/qualification.md).

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
lighting appearance or durable storage. The installed image's final backup
read 498 key assignments, 12 encoder assignments, 16 macro slots, eight RGB
bytes and eight empty Combo getters. Nonempty Combo writes and manual GUI use
remain untested; see [Status](STATUS.md).

For later authorized read-only diagnosis, use a private session and a fresh
output directory:

```sh
python tools/ak820_device_tests.py --run \
  --release-dir /path/to/extracted-alpha2-firmware-bundle \
  --approval /path/to/exact-alpha2-approved-release.json \
  --session /path/to/permanent-session-for-the-same-alpha2-image \
  --output host/runs/post-flash-1
```

The release directory and approval file must identify the exact alpha.2 image installed on the keyboard. The session must be a valid permanent installation/recovery session for that same image; an OEM-only backup or settings backup is not sufficient. Do not use the legacy `releases/rc6` directory with the current default approval for alpha.2. The plan and results remain in the private output directory. Setting-write checks need the runner's explicit write options and authorization. These tests do not flash the keyboard or perform physical actions.

## Physical acceptance

Physical checks require explicit confirmation before any flash. Verify typing,
modifiers, media keys, each physical key, encoder press and both directions,
Combo timing, lighting appearance, unlock/update behavior and settings after
restart and full power removal. Record the exact image hash, device variant,
steps and results. Host or CPU passes do not substitute for these checks.

## CI

[CI and releases](CI.md) describes branch checks and tag publication. CI runs
offline regressions and builds packages; it does not operate a device.
