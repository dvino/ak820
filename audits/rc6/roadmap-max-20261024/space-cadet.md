# Bounded Space Cadet support

The compact tapping engine supports three Space Cadet keys behind
`AK820_COMPACT_SPACE_CADET`:

| Keycode | Tap | Hold |
| --- | --- | --- |
| `SC_LSPO` | Shift + `9` (`(`) | Left Shift |
| `SC_RSPC` | Shift + `0` (`)`) | Right Shift |
| `SC_SENT` | Enter | Right Shift |

Tap and hold use the existing compact tap-hold source state after translating
to the corresponding mod-tap key. No persistent state or dynamic-keymap
format changes are added. Parenthesis taps add an owned Shift around the
normal record pipeline, then send the modifier-up report after releasing that
owner. This preserves other modifier owners and lets Repeat retain Shift with
the digit it learned. Held Space Cadet modifiers use the normal mod-tap
registration path, which sends both the modifier-down and modifier-up reports.
Overlapping Space Cadet and ordinary modifier sources therefore release
independently. `SC_SENT` has the same tap and hold behavior as right-shift /
Enter MT.

The compact Combo engine accepts ordinary basic keycodes as inputs, so these
Space Cadet keycodes cannot be assigned as Combo inputs. Existing ordinary
Combos continue through the existing pipeline. Generated tap records use the
normal record pipeline, including Repeat and Caps Word processing. Both
encoder directions remain supported as tap-hold sources.

The host fixture covers both parenthesis outputs, `SC_SENT` tap and hold, One
Shot interaction, Caps Word interaction, shifted Repeat output, multiple held
sources, both press and release orders against physical Shift, encoder taps in
both directions, and cancellation after a hold. The UBSan run passed with 156
eligible differential traces. Two negative controls also passed: removing
the final modifier-up report or the held-modifier report makes the fixture
fail. Results are in `space-cadet-host.json`.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/ak820_tapping/run.py \
  --space-cadet --oneshot --negative-controls \
  --output /tmp/space-cadet-host.json
```

The linked SDCC 8051 CPU suite also passes against the production action and
report pipeline: 78 cases for Space Cadet alone and 79 for Space Cadet with One
Shot. Both runs reached a peak exercised stack pointer of 132. They check
parenthesis and Enter report traces, shifted Repeat, both encoder directions,
both press and release orders against physical Shift, cancellation, Caps Word
continuation, and One Shot consumption. Results are in `space-cadet-cpu.json`
and `space-cadet-oneshot-cpu.json`.

With the pinned compiler and outliner, the standard image is 39,146 CODE bytes.
Its SHA256 is identical with the feature-disabled source and with Space Cadet
source under the standard profile:
`6781b5766a021a6b550ceae06431528946bd92e6684a1fb98d4add84c9acb9a8`. The
Space Cadet-only image is 39,256 bytes (+110) with SHA256
`5fc6121185143c47768b0351d8fbf981d21432c1b78bad35a5f5e04402257f04`. Space
Cadet with One Shot is 39,905 bytes (+759) with SHA256
`9b1ca80b247b6d3e416ecbc6b07190ac7999f3c4e374fb9212abfcdb57d2d596`. All
three fit the linked CODE window. These are development images; no image was
installed. CPU emulation does not establish physical timing, board USB or IRQ
behavior, NVM behavior, or installed firmware behavior.

These component measurements use the reviewed Space Cadet changes before
protocol narrowing; they do not represent the later aggregate profile sizes.
Independent review approved the source, tests, and evidence on 2026-10-24.
