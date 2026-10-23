# Compact Combo build probes

These are offline source probes against baseline `4b83bb9`. They retain the
existing features, six layers and sixteen macros with 8192 shared bytes. They
use SDCC 4.6.0 and the existing DCE, outlining and callee-save tooling. They do
not change USB, flash, journal, OEM recovery or bootloader code.

All successful builds below deliberately widen `--code-end` to 0xD700. Their
CODE crosses the real 0xC700 NVM boundary. They are unusable probes, not flashable
firmware or installer artifacts. No hardware was accessed.

## Build commands

Run from `qmk-8051-ak820` with the prepared read-only dependency links:

```sh
.venv/bin/python util/build_ak820.py --toolchain ../toolchains/sdcc-4.6.0 --qmk-bin .venv/bin/qmk --build-dir .build/combo-probe07 --code-end 0xd700
```

Each probe uses a fresh build directory. Probe 01 used expanded end 0xF700 but
failed during compilation, so it provides no size result. Probe 02 used 0xD700
and also failed during compilation. Probe 03 is the first linked result.

| Probe | Change from previous linked probe | Total CODE | Main CODE | Low CODE | XRAM | Available internal stack |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 03 | First complete eight-entry engine, modified outputs, versioned storage | 42818 | 40931 | 1887 | 2644 | 143 |
| 04 | Private XDATA entry views in validation and storage helpers | 42733 | 40846 | 1887 | 2643 | 151 |
| 05 | Remove duplicate reload validation and duplicate entry readback | 42403 | 40516 | 1887 | 2625 | 151 |
| 06 | Share entry scan between eligibility and pair matching | 42301 | 40414 | 1887 | 2628 | 151 |
| 07 | Validate fields in stages to shorten live values across calls | 42256 | 40369 | 1887 | 2628 | 155 |

The root control reports 40477 CODE bytes and 2512 XRAM bytes. Probe 07 therefore
adds 1779 CODE bytes and 116 XRAM bytes. The control has 157 bytes available for
the internal stack; probe 07 has 155. These are linked memory allocations, not a
measured worst-case stack depth. Root integration savings are not included.

Probe 07's highest address is 0xCDDC. The real main window is
0x3027–0xC6FF; probe 07 uses 1752 more main-window bytes than that window allows.
The low window has one byte left. Fits must be established separately for both
windows after complete integration; subtracting isolated savings is insufficient.

| Probe | IHX SHA256 |
| --- | --- |
| 03 | `2f285ceacf6e345a5ab75113c36af3131e40889f5ea872d66892840095dd16b6` |
| 04 | `e23e9fad3bda9638046f018fa4f50a378786828fccf6d75421f0ba48125643c0` |
| 05 | `402ce1afa8257dc578c6136f9bbd5d9bda319a9ff4564d0cfbab0c30321e2897` |
| 06 | `67a4006e667dcffce0cc1fe648785c8efc85567e24bb8299dd59a1f53e01f736` |
| 07 | `b97dad321aff4ba689a129e32a745e9374e37d02fa47396d6579f5295f96acb4` |

## Initial failures and corrections

Probe 01 failed because the public pre-process function carries a generic
record pointer, while the new private engine expects XDATA. The only board
callers are `action_exec`'s model-large automatic record. The engine hook now
narrows that pointer at the call site with an explicit proof comment; the public
ABI remains generic.

Probe 02 failed on SDCC's nested-array initializer requirement. Vial Combo
initializers now use `{ { 0 }, 0 }`. No successful build is inferred from either
failed probe.

Probe 05 removes a per-entry readback only because the existing
`ak820_nvm_flush` calls `write_page`, which erases, programs and reads back all
64 bytes. A failed verification latches an NVM fault and prevents success. The
setter still flushes and checks NVM status before the Vial handler reloads RAM.
No storage verification was removed from the NVM driver.

## Host checks

The following commands passed after the final source changes:

```sh
python3 tests/ak820_combo/run.py
python3 tests/ak820_tapping/run.py --output .build/combo-tapping-host.json
```

The dedicated Combo fixture runs 13 production-engine event traces and
configuration validation under host C/UBSan. A second fixture extracts the
production storage getters/setters and checks bounds, extension markers,
invalid stored records, empty entries, validation without writes, latched NVM
failure and verified-flush failure. The lower-level flash journal is modeled in
this fixture; actual power-loss durability is not proved here.

The production tapping/cache/action fixture now includes configured Combos in
both report modes, either release order, shared output owners, Repeat learning
and replay, modified output ownership, Caps Word, pending/active cancellation,
Mod-Tap interruption and Layer-Tap lookup ordering. Existing traces and the
156 eligible retained-QMK HID comparisons also pass. The configured Combo cases
are checked against explicit ownership assertions, not against QMK's broader
Combo behavior.

The public behavior and saved format are in [Combos](../../docs/COMBOS.md).
Independent review, a fitting full application build, linked 8051 checks and
physical/GUI/durable-storage acceptance remain required. Nothing in this report
approves installation or changes the pinned installer image.
