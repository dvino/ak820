# Protocol source size, 2026-10-24

The retained source changes save 47 occupied CODE bytes against `48ce5fa`.
They preserve the public protocol, descriptor checks and report lengths.
The complete standard image keeps 160 allocated stack bytes and 2612 XRAM
bytes. No device was opened. This application is not approved for installation.

| Complete build under QMK `.build` | CODE | Main | Low | XRAM | Stack capacity |
| --- | ---: | ---: | ---: | ---: | ---: |
| `protocol-baseline` | 39814 | 38010 | 1804 | 2612 | 160 |
| `protocol-control2`: byte mode table | 39788 | 37984 | 1804 | 2612 | 160 |
| `protocol-usb-pointer`: defer mode result loads | 39786 | 37982 | 1804 | 2612 | 160 |
| `protocol-final2`: add checked USB width casts | 39767 | 37963 | 1804 | 2612 | 160 |

The final image SHA256 is
`7bb55a7f53e5952039146095435d61a35363cdd9e9c43eb73b3a0f6fffde102b`.
Main code ends at `0xc476`, leaving 649 trailing main bytes. Low code leaves
84 bytes. These windows are separate. [Measurements](protocol-measurements.json)
record each full image and rejected probe. The final build used the separately
reviewed cached outliner, which reproduces the original helper selection.

## Source changes

The private AK820 VialRGB table stores one-byte IDs. Both mode enums fit;
compile-time assertions check their current upper bounds. Other targets retain
the two-byte table. Wire IDs and both conversion arguments remain 16-bit, so
unsupported values with nonzero high bytes still map to zero. Supported-mode
replies still emit two bytes per ID. Conversion loops read the returned field
only after finding its matching input field.

USB descriptor table indexing narrows the interface number only after the
existing full 16-bit bounds check. A compile-time assertion requires at most
256 interfaces. The HID input snapshot loop narrows the host
length only after clamping it to the selected report's length. The snapshot
length comes from a one-byte table or the eight-byte keyboard constant. No
request, interface, descriptor, endpoint or report validation was removed.

## Verification

The VialRGB host differential compares production functions with `48ce5fa`.
Both conversion directions pass all 65536 IDs. Supported-mode output matches
for all 65536 thresholds and lengths 0 through 30: 2031616 requests per image.
Known mode mappings have separate assertions. See
[host results](vialrgb-differential.json).

The linked C52 fixture passes 987 cases: both conversions for 261 IDs each,
including byte boundaries and invalid high bytes, plus 465 supported-mode
requests across all lengths 0 through 30. It checks the actual 14 linked table
bytes. The observed stack use is eight bytes for these paths, not a whole-program
bound. See [linked results](vialrgb-linked.json).

The production USB host suite passes. The existing two-million-case SETUP
differential also passes with digest `ab47fa10b13357b7` for both sources. See
[USB differential](protocol-usb-differential.json). The exact linked descriptor
checker passes; see [descriptor results](protocol-usb-image.json).
No USB timing, IRQ nesting, durable storage or physical behavior was tested.

From the repository root:

```sh
python3 -B qmk-8051-ak820/tests/ak820_vialrgb/host.py \
  --output audits/rc6/roadmap-max-20261024/vialrgb-differential.json
python3 -B qmk-8051-ak820/tests/ak820_vialrgb/linked.py \
  --build-dir qmk-8051-ak820/.build/protocol-final2 \
  --s51 /path/to/sdcc-4.6.0/bin/s51 \
  --output-dir qmk-8051-ak820/.build/protocol-final2/vialrgb-linked
python3 -B qmk-8051-ak820/tests/ak820_usb/run.py
python3 -B audits/rc6/protocol-optimization-20261024/usb_differential.py \
  --source-root qmk-8051-ak820 --output-dir /tmp/ak820-usb-differential
python3 -B qmk-8051-ak820/util/check_ak820_usb_image.py \
  qmk-8051-ak820/.build/protocol-final2/ajazz_ak820_vial.ihx \
  qmk-8051-ak820/.build/protocol-final2/ajazz_ak820_vial.map
```

The standard full-build command runs inside `qmk-8051-ak820`:

```sh
PYTHONDONTWRITEBYTECODE=1 /path/to/qmk-venv/bin/python util/build_ak820.py \
  --toolchain /path/to/sdcc-4.6.0 --qmk-bin /path/to/qmk-venv/bin/qmk \
  --build-dir .build/protocol-final2
```

## Rejected probes and fixture corrections

- CRC shift-once and a saturated 16-bit unlock subtraction loop together grew
  CODE to 39849 and reduced stack capacity to 159. Emitted CRC code grew from
  71 to 104 bytes; unlock code grew from 162 to 192. Both were reverted.
- Incrementing USB destination and snapshot pointers grew CODE by one byte and
  reduced stack capacity to 159. The original copy loop remains.
- Narrowing the supported-mode threshold after testing its high byte saved five
  more CODE bytes but reduced stack capacity to 159. It was reverted.
- Storing IRQ-private `control_zlp` in bit memory saved 12 additional bytes and
  one XRAM byte but reduced stack capacity to 159. It was reverted.
- The first build rejected a source edit made before final input verification.
  The fresh untouched baseline reproduced the expected 39814-byte image.
- The first linked fixture used observation labels that were prefixes of later
  labels. The shared extractor therefore read the later observation. Delimited
  labels fix the fixture; the full linked run then passed. No firmware change
  was needed.

## Review

Independent root review approved the source, tests, documentation and evidence.
The review required an explicit `TOTAL_INTERFACES <= 256` assertion and reusable
fixtures under `tests/ak820_vialrgb`; both corrections are retained. A fresh
`protocol-final2` build reproduced the image hash and resource values above.
The moved host and linked fixtures, USB suite, differential and descriptor
checker pass. The reviewer independently reran the host differential and
confirmed digest `aaefd5a89c174348`.
