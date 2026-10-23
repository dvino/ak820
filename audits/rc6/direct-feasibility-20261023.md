# Saving a Direct Control layout

Research dated 2026-10-23. No implementation, build, USB access, settings write,
reset or flash was performed for this report. Direct Control remains present.

## Answer

A useful saved per-LED layout is plausible without a large new renderer. The
firmware already holds and displays all 82 HSV colors. The missing parts are
a usable editor, palette readback, explicit save and startup restore. The
available storage can hold one full-color layout, or two smaller layouts with
a shared 16-color palette. Whether either design fits CODE is still unproved.
The next step should be an isolated offline size experiment, not mode removal.
Removal requires the owner's explicit permission.

The full-color design preserves every LED's present HSV precision but cannot
retain both the old and new complete layout in the current unused NVM gap.
The 16-color design can preserve the last complete saved layout during an
interrupted save, at the cost of a visible color-count limit. That limit needs
the owner's agreement before it becomes a product requirement.

## What the current files establish

Local sources inspected:

- `qmk-8051-ak820/quantum/vialrgb.c`: `g_direct_mode_colors` stores 82 HSV
  triples, or 246 payload bytes. Direct fast-set accepts up to nine LEDs per
  32-byte packet and clamps value to 160. A complete preview needs ten packets.
  The protocol exposes LED count, positions and matrix locations. It does not
  expose a getter for the color array. `vialrgb_save()` saves only RGB config.
- `qmk-8051-ak820/keyboards/ajazz/ak820/ak820_rgb.c`: Direct reads this RAM
  array and renders at most eight LEDs per task. Startup reloads the eight-byte
  RGB config, not the array. Global HSV controls do not replace Direct colors.
  Ordinary persisted RGB changes have a one-second debounce; the Direct
  fast-set path itself has no EEPROM write.
- `config.h`, `ak820_macro.h`, `quantum/dynamic_keymap.c` and `rules.mk`:
  six 16-by-8 keymap layers occupy logical `0x0040..0x063F`; encoders occupy
  `0x0640..0x0657`. Disabled QMK settings, tap dance, combos and overrides add
  no storage here. Macro metadata starts at `0x07F0`; 8192 macro bytes start
  at `0x0800`. Thus the presently unused gap is `0x0658..0x07EF`, 408 bytes.
  New compile-time bounds must reserve any claimed palette region explicitly.
- `ak820_nvm.h` and `.c`: logical NVM is `0x2800` bytes, mapped at physical
  `0xC700..0xEEFF`, with 64-byte pages and a separate redo journal at
  `0xEF00..0xEF7F`. The journal protects one page operation, not a multi-page
  palette transaction. Storage failures latch and stop further writes.
- `quantum/via.c`: the schema/build identity is tied to
  `AK820_NVM_BUILD_ID` (`0x082002`). Incompatible schemas stop writes rather
  than silently regenerating settings.

The candidate's existing `.mem` file at
`qmk-8051-ak820/.build/rc6-candidate-erase-20261023/ajazz_ak820_vial.mem`
reports 39,347 CODE bytes, 2,071 XRAM bytes and 152 stack bytes. The highest
occupied CODE address is `0xC296`. Against the project's 40,505-byte CODE and
3,072-byte XRAM limits, subtraction leaves 1,158 CODE and 1,001 XRAM bytes.
These are measured existing-build figures, not measurements of this proposal;
placement in both code windows and emitted stack use still matter. Current
working sources can change independently of this frozen candidate.

## What Vial provides

[Vial's lighting documentation](https://get.vial.today/docs/lighting.html)
describes Direct as computer-script control. It lists effect, color,
brightness and speed controls in the GUI and a raw HID API for other programs.
It does not promise a saved per-LED layout editor.

The upstream GUI source was read from the repository archive entirely in
memory. The ZIP comment and `git ls-remote` both identified commit
`aef8222a2d0429a183b2ed692d5f9efcfd383f08`.
[Its RGB editor](https://github.com/vial-kb/vial-gui/blob/aef8222a2d0429a183b2ed692d5f9efcfd383f08/src/main/python/editor/rgb_configurator.py)
offers Direct in the effect list but builds only global effect, color,
brightness and speed controls, plus Save. It has no per-LED selection or paint
surface. This supports the reported Vial Web screen limitation; the live Web
deployment itself was not inspected. A firmware change alone will not turn
that screen into the requested editor.

Use an AK820 editor page or an upstream editor extension, selected separately.
The editor must draw all 82 reported LED positions, select one or several LEDs,
paint or clear them, show the current colors, and offer explicit Preview and
Save layout actions. Reading the saved layout on reconnect is necessary: a
blank local editor must not overwrite an existing layout. Show unsaved state
and a successful save only after exact readback and clean storage status.
File export/import is useful but does not replace saving in the keyboard.
No Windows helper or packaging work is proposed here.

## Bounded storage choices

All sizes below are calculated layouts. No proposed CODE delta was measured.

| Choice | Saved bytes | Behavior and cost |
| --- | --- | --- |
| One full HSV record | 246 color bytes + 10 header bytes = 256 | Fits logical `0x0680..0x077F` (physical `0xCD80..0xCE7F`), four pages. Keeps arbitrary color per LED. Invalidate before changing payload and commit last. Interrupted save may leave no valid layout; startup must use a documented safe fallback. It cannot promise the previous layout survives. |
| Two 16-color records | Each: 48 HSV palette bytes + 41 packed LED-index bytes + at most 39 metadata/padding bytes = 128; total 256 | Two page-aligned slots at `0x0680..0x06FF` and `0x0700..0x077F`. Save inactive slot, validate, commit last, then choose the newest valid generation at startup. Keeps the prior slot until the replacement is complete. Every LED remains independently assignable, with at most 16 distinct colors. |
| Two full HSV records | At least 512 | Does not fit the current 408-byte gap. Requires a storage-layout trade, such as reducing macros or layer capacity, or another separately proven physical allocation. None is authorized here. |

For both fitting choices, retain the existing 246-byte runtime array. Decode
the stored representation once at startup and reuse the current renderer.
Do not add a second full runtime array merely to stage saves. Stream records
through the existing page cache, with small scalar state. Proposed RAM budget:
at most 32 additional bytes for full HSV, or 64 for indexed state/scratch;
these are design targets, not linked measurements. A full shadow buffer would
add 246 RAM bytes and needs its own justification.

CODE planning target: attempt the full-HSV loader, getter, explicit save,
validation and status response within 700 extra bytes. Two-slot selection and
indexed conversion may exceed that target; no numerical saving is claimed.
The hard limit is the actual linked image and placement, not the target.
Existing CRC/page routines may help, but reuse can enlarge call frames or
generic-pointer code under SDCC. A new build must measure this.

## Save and protocol contract

Keep standard Direct fast-set as a RAM-only preview. Add a small versioned
AK820 capability/read/save extension with bounded offsets and lengths. Do not
repurpose unknown Vial command IDs without checking the dispatcher and client
contract. A save request must be distinguishable from routine preview traffic.
The current generic RGB Save must either invoke the documented palette save
in Direct mode or clearly remain settings-only; two buttons with misleading
identical promises are unacceptable.

Freeze edits while the save is in progress. Commit only the exact preview
generation that the editor requested. Verify the whole record and CRC before
success. Stop on timeout, storage fault, unexpected ACK or bad readback. Do not
retry, restore, reset or recover automatically. Never save once per frame or
once per LED packet. Unchanged saves should avoid new page writes.

The record needs magic, format version, LED count, length, validity/commit
state and CRC; dual slots also need generation selection with a defined wrap
rule. Exact header encoding and commit ordering must be specified before code.
For a two-slot record, invalidate the inactive slot before reuse, write payload
and metadata through the existing journal, then commit it last. Preserve the
active slot. Verify crash states at every page/journal/commit boundary in the
CPU model. The existing single-page journal alone does not prove this contract.

On startup, validate before copying anything to the active array. Unknown
format, wrong LED count or failed CRC must not display mixed or unchecked
colors. Choose a documented solid fallback without silently writing flash.
For dual slots, choose the newest valid slot; keep the older one on an
incomplete new save. Selecting Direct and restarting after a successful save
must require no running PC application. Rendering remains entirely on-device.

Reserve the region in all address assertions, packers, snapshot tools and
migration checks. Decide explicitly whether introducing this formerly unused
region requires a new NVM schema ID; a new ID with migration is the clearer
contract. Migrate from a fresh validated snapshot, preserving exact keymaps,
encoders, macros, global lighting and other settings. Initialize the palette
as absent without guessing previous RAM colors. Never treat arbitrary old gap
bytes as a palette, and never reuse the old schema if its meaning changes.
Older firmware may ignore or overwrite new data, so downgrade preservation
also needs a policy. Installer and image validators must recognize the schema
before any separately authorized flash can be considered.

## Minimal next experiment and stop conditions

1. Choose full HSV with an explicit interrupted-save fallback, or obtain
   agreement for 16 colors and retained prior save. Do not silently substitute
   reduced color precision or remove Direct.
2. Specify packet, record, save/readback and migration contracts. Make an
   offline editor mock using the existing 82 LED map; demonstrate selection,
   painting, current-layout loading and explicit save using a fake transport.
3. In a separate owned experiment, add only the chosen loader/getter/save
   path, with no unrelated effect removal. Build once against a frozen current
   baseline and compare MAP/MEM/ASM, image bounds, stack and exact linked delta.
4. Run host/CPU tests for all 82 indices, packet truncation and overflow,
   clamping, old schema, invalid records, save generation, page sharing,
   journal failure and every interrupted-save boundary. Assert that preview
   traffic performs zero NVM writes and that neighboring settings stay exact.
   Review code, documentation and evidence independently.

Stop if the record overlaps any setting or metadata, the image crosses either
CODE window, stack bounds are unproved, a fault reports success, a power-cut
model restores mixed data, or migration changes unrelated bytes. Stop rather
than trading away macros, layers, effects or precision without owner approval.
Keep the experiment offline if current layout or compiler evidence is missing.

This report proves neither durable writes on the keyboard nor physical LED
order, brightness, restart behavior or power-loss recovery. Physical, power,
Alt Repeat and storage testing remain deferred. Any future live write or
flash requires the applicable explicit authorization; this research grants none.
