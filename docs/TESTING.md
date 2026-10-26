Русский перевод: [Проверки](ru/TESTING.md).

# Testing

The offline suite checks the selected source and linked firmware image. It does
not prove physical keyboard behavior. The ten beta.2 profiles passed offline
qualification; results and limits are recorded in [Status](STATUS.md).

## Offline regression suite

From the repository root, run the general offline checks:

```sh
python tools/test_keyboard.py
python -B -m unittest discover -s tools/installer -p 'test_*.py' -v
python -B -m unittest discover -s qmk-8051-ak820/tests/ak820_inventory -p 'test_*.py' -v
```

To build and qualify a release profile, first prepare a fresh, reviewed
source/IRQ context certificate for the current source. Use a fresh build
directory for each profile:

```sh
python tools/configure_firmware.py build --profile main \
  --parameter-spills-context /path/to/current-source-irq-context.json \
  --build-dir qmk-8051-ak820/.build/beta2-main \
  --toolchain toolchains/sdcc-4.6.0
```

The build uses the context-gated release transforms and then qualifies that
exact linked image. Qualification checks linked memory and proves foreground,
startup and enabled interrupt stack bounds before running the full base and
profile-specific offline suites. To requalify an existing linked image:

```sh
python tools/configure_firmware.py qualify \
  --build-dir qmk-8051-ak820/.build/beta2-main \
  --toolchain toolchains/sdcc-4.6.0
```

Repeat the build with each selected profile name from
`python tools/configure_firmware.py list`. `main` is the default profile.
Feature tests run only when the selected image enables the corresponding
module; Grave Escape is not part of `main`. Check each generated qualification
report for the suites run and skipped. Beta.2 has ten source profiles, but
source definitions and earlier profile results do not qualify a new image.
Each of the ten beta.2 images passed 28 base suites, 331 unit tests without
skips and 32–37 supplemental suites. The [qualification record](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/audits/rc6/beta2-release-20261025/qualification-final.json)
binds these results to exact images. Every new build requires its own checks.

The standard IRQ analysis uses a public OEM instruction fixture and does not
require private ROM. CPU fixtures model peripheral operations but do not
emulate VS11K28A USB or flash silicon. Host and CPU results do not establish
physical behavior or durability after full power loss.

The automatic suite does not require key presses, encoder movement, cable
reconnect or manual Vial unlock, and does not write to the keyboard. Live
protocol checks are separate and read-only by default. Settings writes require
the runner's explicit write options and authorization. Timeouts, storage faults
and failed readbacks stop the run; do not blindly retry, reset or restore.

## Live checks and limits

The live runner reads matrix and encoder assignments, macro slots, RGB settings
and supported getters. Read-only results do not prove physical switches, scan
timing, encoder signals, macro playback, lighting appearance or durable
storage. A live check requires an approved bundle and session for the exact
selected image. For an authorized read-only check, set `release-dir` to the
extracted approved bundle and use a fresh private output directory:

```sh
python tools/ak820_device_tests.py --run \
  --release-dir /path/to/extracted-approved-selected-bundle \
  --approval /path/to/exact-approved-release.json \
  --session /path/to/permanent-session-for-the-same-image \
  --output host/runs/post-flash-1
```

The bundle, approval and session must identify the same image. Do not use an
approval for a different image or an old `releases/rc6` directory. The command
does not flash the keyboard or require physical actions.

## Physical acceptance

Physical checks require separate explicit confirmation before flashing. Check
typing, modifiers, media keys, physical keys, encoder press and both directions,
Combo timing, lighting, update behavior, and settings after restart and full
power removal. Record the image hash, device variant, steps and results. Host
or CPU passes do not replace these checks.

## CI

[CI and releases](CI.md) describes branch checks and publication. CI runs
offline regressions and builds packages; it does not operate a device.
