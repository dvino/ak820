# Linked VIA → NVM → IAP regression

This is an **offline CPU test with an explicit peripheral model**. It never
enumerates or opens USB, calls a loader, or modifies a physical keyboard.
The simulator executes the supplied linked SDCC instructions. The runner
supplies Flash effects and ROM_STATUS values at the actual controller register
accesses. It does not simulate physical IAP delays, electrical USB, voltage,
interrupt overlap, or a physical restart.

## Run

Use Python 3, an SDCC 4.4.0 `s51` executable, the sibling
`tests/ak820_emitted/run.py`, and an already linked build directory containing
`ajazz_ak820_vial.{ihx,map,mem}` plus `dce/**/*.rst`.
The output directory must not exist before the run.

```sh
python3 -B tests/ak820_iap/run.py \
  --build-dir .build/your-candidate \
  --s51 /absolute/path/to/sdcc-4.4.0/bin/s51 \
  --output-dir /absolute/path/to/new-iap-evidence \
  --iap-fault-profile guarded-erase \
  --baseline-build-dir /absolute/path/to/unchanged-rc2-build
```

The baseline is optional. Supplying it adds the measured old/new operation-count
comparison and the separately labeled GUI latency model. It must be a complete
rc2 build, with its own matching linked map/listings. No build inputs are edited.
The `--iap-fault-profile` value binds the failure-case expectation to the image:
use `guarded-erase` for the candidate whose erase helper verifies all 64 erased
bytes, or `legacy-iap` for the earlier implementation. This profile applies to
`--build-dir`; the optional baseline is used only for the count comparison. The
suite fails if the selected image does not match the expected behavior.
Each case writes a complete simulator log and JSON observations, including the
IHX SHA-256, actual IAP commands, source DPTR, status reads, and observed stack
peak. `results.json` collects the cases and limitations.

## Cases and distinguishing assertions

| Case | What it verifies |
|---|---|
| Normal remap | VIA `05`, locked Vial, actual CODE change, zero journal header, ACK only after persistence; repeated identical setter adds no IAP; backend reinitialization, ordinary getter and FD00 agree |
| Dense remap | Same path with 32 valid `Ctrl+A` assignments in one page, changing the first to `Ctrl+B`; exactly two block programs, at most 14 IAP commands |
| Command error | Injected `ROM_STATUS=C2` during journal block program; latched failure, no setter ACK, old target CODE, FD01 captures the actual `C0→C2` status |
| Partial journal program | Command reports success but only a prefix is programmed; full readback rejects it, old target survives, no setter ACK |
| Partial target program | Committed journal survives a target readback failure; backend reinitialization replays the complete page and cleans the header |
| Invalid address status | `bROM_ADDR_OK=0` rejects the first erase without issuing a command; failure remains observable through FD01 |
| Bounds and ABI | Low/high/protected/unaligned addresses are rejected without IAP; both writable boundary pages program correctly through the actual SDCC pointer ABI |
| Invalid block pre-status | The naked block helper receives a valid aligned source but `bROM_ADDR_OK=0`; emits no opcode, preserves raw before/after status, returns false, and restores IE/write protection |
| Ineffective erase and boot replay | Start from the observed OEM encoder word `00A9` at `CD40`, request the observed temporary CW value `0000`, and make `A6` report success without erasing. Both profiles must retain the committed journal and original target, withhold ACK, and fail replay at recovery-write stage 3. `legacy-iap` expects the old target `9A` program followed by stage-12 readback failure; `guarded-erase` expects erase readback to fail at stage 12 before any target `9A` program |

The ROM_STATUS read model derives block validity from source DPTR and the Flash
address, including the matching low six bits required by the OEM routine. It
does not force an unconditional success status. This rejects the intermediate
implementation that checked status with DPTR still pointing at a C temporary.
The corrected helper must hold the source DPTR across both the precheck and
the `9A` opcode, then return status bytes using the SDCC `uint16_t` ABI.

Every actual IAP command is checked for the permitted `C700..EF7F` range,
operation and mode, EA clear, CODE_WE enabled, and aligned in-range XRAM source
for block programming. All normal and injected failure paths check restoration
of IE and CODE_WE. The model uses the supplied ROM's zero-erased Flash and
zero-to-one program semantics. Partial block writes are deliberately possible;
the test never assumes that a block program is atomic.

FD01 assertions run when that symbol exists in the linked image. They check
first failure stage, cache state, the last actual IAP record, and read-only
routing. The ordinary cached getter is explicitly shown to return new data
after a failed write. FD00 and journal contents provide the durable evidence.

The ineffective-erase scenario is a **failure-model hypothesis test** based on
the reported status and readback symptom. It does not claim that either behavior
has been confirmed on the keyboard's Flash controller or that this is the
physical cause. In both profiles, it verifies that the linked firmware
withholds setter ACK, preserves its committed redo record, and tries that
record again at initialization when the modeled erase remains ineffective.
The expected final opcode is selected before the run, so the test cannot pass
merely by accepting whichever failure path occurred. RAM cache observations
are kept separate from target-page evidence.

## Count and latency interpretation

For the dense fixture, unchanged rc2 performs 139 IAP commands; the block
candidate performs 13. The normal first-page fixture goes from 56 to 14. Counts
are observed at executed ROM_CTRL writes, not inferred from source loops.

The optional latency comparison executes the **unchanged** `hid_send` function
extracted by AST from the bundled official Vial GUI v0.7.5 source. Its fake HID
device answers according to `command count × 5 ms`, where 5 ms is the typical
CH555 TERPG figure. This reproduces the old dense fixture's
`failed to communicate with the device` at 695 ms versus the client's 500 ms
timeout, and accepts the candidate's 65 ms estimate. The model is labeled
`LATENCY_MODEL_ONLY`: neither a physical duration nor the user's original
failure cause has been established. Whole-map reset and other multiple-page
operations can still exceed the GUI timeout.

## Primary-source provenance

- `fixtures/vial-v0.7.5-util.py`: unchanged official GPL-2.0-or-later source,
  SHA-256 `729fddb4792774cfebc149d303a640f353d585c4cf133c0cec76d1fb5de52336`.
  [Pinned upstream file](https://github.com/vial-kb/vial-gui/blob/e42622c352b69eff523a467718db487ab9c9cbf2/src/main/python/util.py).
  `fixtures/vial-v0.7.5-ref.json` records the official tag reference to commit
  `e42622c352b69eff523a467718db487ab9c9cbf2`. GUI/PyQt and HID imports are not
  executed by this test; only its `hid_send` function is extracted.
- CH555 manual supplied in the handoff research input,
  `ak820/work/movx-addressing/CH555DS1-1D.pdf` / `.txt`: §6.5.3 describes block
  programming and DPTR/XRAM alignment; §19.5 gives TERPG 2/5/8 ms. This is
  compatible-family timing evidence, not a measured VS11K28A guarantee.
- The supplied device's historical private `release/rc2/reference/stock-full.bin` contains the
  native block programming helper at `11B7..1260`; it sets source DPTR at
  `1230..1233`, checks ROM_STATUS at `1235`, issues `9A` at `123A`, and reads
  post-status at `123D`. This is evidence from the target OEM image, separate
  from the compatible-family datasheet.
