Русский перевод: [Проверки](ru/TESTING.md).

# Testing

Keep source review, build/integrity checks, host/CPU execution and physical
keyboard behavior separate. None substitutes for another.

## Indicator candidate

The C/W candidate `45f28e80cd9e269cb507d6fff47b43cea2766b00967912599a98b036b638011d`
passed 11 focused indicator cases and 12 reactive RGB observations in the linked
CPU model, including an independent rerun. Main-checkout reproduction matched
the same IHX. The [full local qualification](../audits/rc6/oem-indicators-qualification-20261024/qualification.json)
passed all 26 suites and 258 unit tests with no skips and unchanged IHX/MAP.
Local LeakSanitizer detection was disabled; ASan/UBSan checks remained active.
New CI is pending; the retained result below applies to the earlier tap-hold-only image. See [indicators](INDICATORS.md)
for state-fixture and physical-test limits.

## Retained tap-hold offline result

The [compact tap-hold qualification](../audits/rc6/compact-tapping-qualification-20261024/qualification.json)
passed all 26 required suites and 258 unit tests with no skips on 2026-10-24.
IHX `d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3`
and MAP hashes stayed unchanged. This is offline host/CPU evidence; no device
commands were sent. LeakSanitizer was excluded; address and undefined-behavior
checks remained active. [Independent offline review](../audits/rc6/compact-tapping-final-integration-review-20261024.md)
passed. The [fresh bundle check](../audits/rc6/compact-tapping-fresh-bundle-20261024/check.json)
also passed from commit `3c96e37`: the installer accepted the generated bundle
with exact approval checks and no HID access. [Dev CI 40026118029](https://github.com/dvino/ak820/actions/runs/40026118029)
passed on `586ac20`: Linux rebuilt the same IHX, passed 26 suites and 258 unit
tests without skips, and Windows built both applications with that fresh bundle.
CLI help, offline verification and Tk startup passed. Publication was skipped.
[Retained checks](../audits/rc6/ci-tap-hold-20261024/firmware-check.json)
and [Windows input checks](../audits/rc6/ci-tap-hold-20261024/windows-check.json)
bind the downloaded artifacts; visible dialogs and device behavior were not tested.

## Historical offline result

The retained [qualification report](../audits/rc6/roadmap-qualification-20261023/final/report.json)
records 23 passing suites, 247 unit tests with no skips, and unchanged IHX/MAP
hashes throughout the run. Eight host C suites and six linked CPU suites passed;
one suite checks public documentation. This historical result applies to the
pointer-only image `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8`,
not the current compact tap-hold candidate in [Status](STATUS.md).

| Unit suite | Tests passed |
| --- | ---: |
| Installer and GUI logic | 111 |
| Release assembler | 12 |
| Windows package recipe | 12 |
| Combined runner | 10 |
| Device test runner | 19 |
| Device protocol | 9 |
| Low-level package, including real SDCC checks | 67 |
| Linked inventory parser | 7 |

Settings tests use synthetic raw protocol responses and temporary files. They
do not read private ROM captures or open a keyboard. Restore compatibility is
limited to the exact reviewed image pairs in [Settings backup](SETTINGS-BACKUP.md);
that does not establish a successful live restore. Source
`verify` passes without HID access. The [source/package review](../releases/rc6/reviews/independent-review.md)
binds the approved release and host files; it does not bind the new development
image or a Windows binary.

The [evidence manifest](../audits/rc6/roadmap-qualification-20261023/manifest.json)
keeps the failed initial attempt as well as the final run. The final run disables
LeakSanitizer because process metadata is inaccessible in the sandbox. Address
and undefined-behavior checks remain active in the C harnesses that use them;
leak checking is excluded. The later Windows CI builds and Tk startup checks are recorded in
[Status](STATUS.md). Interactive dialog acceptance, live settings writes and
physical persistence remain unperformed. Live-runner skips listed
below are separate from the zero-skip unit result.

## Run the offline suite

From the repository root:

```sh
python tools/test_keyboard.py
python -B -m unittest discover -s tools/installer -p 'test_*.py' -v
python -B -m unittest discover -s qmk-8051-ak820/tests/ak820_inventory -p 'test_*.py' -v
```

The combined runner records each command, exit code, log hash, tool hashes and
reported unit-test skips under `host/runs/`. It selects the local SDCC 4.6.0
pair, or an explicit `--toolchain` installation. `AK820_SDCC_BIN` remains
supported. The selected compiler and simulator reach all child suites.
Inventory tests run by default; `--host` adds the bounded C checks, and
`--build-dir` adds the linked CPU suites. The compact tap-hold candidate raises
the required qualification to 26 suites: it adds actual VIA decoding, tap-hold
host tests with negative controls, and linked tap-hold execution. This is a
new requirement, not a result for the retained 23-suite run.
No device commands or flash tests are run.

For qualification with installed tools and a fresh completed build:

```sh
python tools/test_keyboard.py --host --require-toolchain \
  --toolchain toolchains/sdcc-4.6.0 \
  --build-dir qmk-8051-ak820/.build/local-1 \
  --iap-fault-profile guarded-erase --output host/runs/qualification.json
```

`--require-toolchain` rejects missing tools and fails the final result if a
unit suite reports a skip. Without it, the ordinary offline command can run
without a compiler and records any skips. Launch failures are recorded as
failures. Initial, per-suite and final IHX/MAP hashes detect a transient image
replacement even if the final files are restored.

Host C runners require GCC/Clang on Linux/WSL. The report records supplied
sanitizer environment settings. Use `ASAN_OPTIONS=detect_leaks=0` only when the
sandbox prevents LeakSanitizer from inspecting processes, and record that
limitation. For example, prefix the qualification command with that assignment
in Bash. This was the environment used for the retained final run.

Native Windows packaging commands are in [Build](BUILD.md). The twelve recipe
tests simulate collected payloads and smoke failures. Only a real Windows run
can produce the EXEs and exercise creation of the native Tk interface;
interactive acceptance of its visible dialogs is a further check.

## Reuse the retained firmware evidence

The source archive contains controlled build reports, their referenced
artifacts and relocated listings. No transient probe directory is needed to
regenerate the pointer inventory. From the repository root:

```sh
python qmk-8051-ak820/util/ak820_linked_inventory.py \
  --root audits/rc6/bounded-evidence-20261023/pointer \
  --report audits/rc6/bounded-evidence-20261023/pointer/.build/bounded-probe/build-report.json \
  --output /tmp/ak820-pointer-inventory.json
python qmk-8051-ak820/tests/ak820_bounded/emitted.py \
  --build-dir audits/rc6/bounded-evidence-20261023/pointer/.build/bounded-probe \
  --s51 toolchains/sdcc-4.6.0/bin/s51 \
  --output-dir host/runs/linked-header-1
```

The second command needs the pinned simulator; install it as described in
[Build](BUILD.md). Use a fresh output directory. The retained reports preserve
original paths as provenance; the evidence manifests locate their portable
copies. The inventory checks all recorded artifact identities and instruction
bytes but deliberately reports partial coverage. See its
[limits and control command](../audits/rc6/linked-inventory-20261023.md).

The bounded host test extracts production functions and checks 264,448 journal
headers and 65,025 legal delay pairs. The linked test executes 2,304 header
mutations and measures that helper's exercised stack. Valid macro playback
covers all sixteen slots. Arbitrarily truncated encoded operands supplied
directly to playback are outside this harness's complete published-stream
contract; the inherited issue and separate storage-validation scope are
recorded in the [probe report](../audits/rc6/bounded-optimization-20261023.md).

Other linked runners accept a fresh build and the pinned simulator. From
`qmk-8051-ak820/`, for example:

```sh
python tests/ak820_features/run.py --build-dir .build/local-1 \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 --output-dir .build/local-1-features
python tests/ak820_irq/run.py --build-dir .build/local-1 \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 \
  --stock-rom /path/to/private-oem-references/stock-full.bin \
  --output-dir .build/local-1-irq --main-sample-bytes 80
```

The IRQ fixture needs a private OEM ROM that is absent from the source archive;
it was not part of this final combined run. Do not add private reference images
to a release. CPU fixtures model peripheral operations. They do not emulate
VS11K28A USB/flash silicon or establish safety for every stack/interrupt path.

## Automatic checks without physical input

The automatic test work needs no key presses, knob rotation, cable reconnect or
manual unlock. Start with the offline runner:

```sh
python tools/test_keyboard.py
python -B -m unittest discover -s tools -p 'test_ak820_device_tests.py' -v
python tools/ak820_device_tests.py
```

The last command prints a plan. It must not open HID or write a setting in its
default mode. The combined runner includes its offline regressions. With a
completed Linux build, `--host --build-dir qmk-8051-ak820/.build/local-1`
also runs host and linked CPU checks; those still send no device commands.
Add --iap-fault-profile guarded-erase for the candidate with erase readback.
The default legacy-iap profile is for the earlier image; selecting a profile
does not identify or validate the image by itself.

| Area | Automatic check | What it does not prove |
| --- | --- | --- |
| Keys and layers | Read all 83 physical matrix slots on all six layers; compare protocol values with saved bytes. Opt-in write tests change a representative key on each layer and restore it. | Physical switch wiring, scan timing or typing from every key |
| Encoder | Read both directions on six layers; opt-in tests change and restore each direction. One hardware encoder has 12 assignment slots in total. | Rotation signals, detents or encoder push input |
| Macros | Check 16 slots, the 8192-byte protocol view and saved length metadata. Macro writes are reported as SKIP; tests never start unlock or execute a macro. | Macro upload round trips and triggering a macro from a physical key |
| RGB | Read capabilities, 82 LED records and settings; opt-in tests change and restore RAM settings while proving saved bytes stay unchanged. | Durable RGB save (SKIP), LED appearance, color accuracy or reactive light from a real press |
| Input features | Existing host/CPU cases cover report handling, Caps Word, Repeat/Alt Repeat, Grave Escape, Tri Layer and macro processing where implemented. | Physical input and electrical USB behavior |
| Storage failures | Test missing ACK, getter-only changes, bad durable readback, changed neighboring bytes and failed restoration. | Every possible controller failure or power-loss timing |

Live protocol checks are intended for later post-flash runs. Setting writes
need explicit authorization and opt-in arguments; a read-only run does not
grant it. Before every write, the runner must require a healthy stable snapshot.
After a change it must verify the reply, getter, exact saved bytes and unchanged
neighbors before trying one restoration. On a timeout or mismatch it stops and
saves the evidence. It never resets, retries, starts a bootloader or restores
blindly. Reports must list failures and skipped checks rather than call all
functions tested.

For a future read-only run after flashing, use Python with `hidapi` installed
and the matching personal session. The release is checked against its approval
before HID is opened:

```sh
python tools/ak820_device_tests.py --run --release-dir releases/rc6 \
  --session /path/to/personal-session --output host/runs/post-flash-1
```

Use a new output directory. To include the reversible mapping and RGB RAM
checks, add **both** `--allow-settings-write --owner-authorized`, only after
authorization for those changes. The plan, individual PASS/FAIL/SKIP results,
snapshots and request trace stay in the private output folder. These commands
never flash the keyboard or ask for physical actions.

The earlier SDCC 4.4 RC6 candidate failed its encoder write at `target_write`
despite a successful cold boot. This is a historical regression case, retained
in the offline tests. Later SDCC 4.6 evidence is listed in [status](STATUS.md);
it does not replace a new settings or power-loss acceptance test.

## Physical acceptance checklist

Only start after the owner confirms the flash and has alternate input ready.
Keep cable and power stable while writing. Preserve the personal recovery folder.

1. Verify progressing boot status and type ordinary text, modifiers and media keys.
2. Test every physical key, encoder press and both directions; check release of chords.
3. Remap keys/layers/encoder, save a macro and global lighting, then restart.
4. Disconnect power and reconnect twice. Confirm the permanent application starts
   and retained settings work; a trial must instead follow its documented loader path.
5. Check reactive LEDs: idle black, correct key, chords, re-hit, fade, brightness
   and mode switches. Inspect actual appearance; a numerical model cannot do this.
6. Test Vial unlock/lock and Bootloader recovery using the personal session.

Record the exact image SHA256, device variant, OS, steps and results. A failed
step is a failure even when the loader checksum or another test passed.

## Continuous integration

Push and pull-request checks, native Windows packaging and version-tag releases
are described in [CI and releases](CI.md). The workflow also runs the NVM and
macro interrupted-write models. It performs no device operations.
