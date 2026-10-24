Русский перевод: [Комбинации клавиш](ru/COMBOS.md).

# Two-key Combos

The development source includes eight configurable two-key Combos. Each Combo
replaces two ordinary keys pressed within 40 ms with one key or a modified key,
for example J + K → Escape or F + D → Ctrl+C. The implementation is specific to
the AK820. The standard QMK Combo engine remains disabled.

The current candidate fits the original memory windows with all earlier
functions enabled, including Grave Escape and NKRO. It uses 40,313 CODE bytes,
with 120 trailing main-window bytes and 67 low-window bytes free. Published
alpha.1 does not include Combos. The planned alpha.2 candidate has not been
installed or released; [Status](STATUS.md) records its verification state.

## Configuration

Vial's dynamic Combo commands report eight entries. Each entry uses the standard
10-byte Vial structure: four little-endian input words followed by one output
word. Only the first two inputs may be set. The third and fourth must be zero.
An all-zero entry disables that slot. Unsupported entries return an error before
changing settings.

Inputs must be distinct, ordinary keyboard usages from `KC_A` through
`KC_EXSEL` (0x0004–0x00A4). Modifier inputs, encoded modifiers, Mod-Tap,
Layer-Tap, macros, Repeat, encoder events and other quantum keycodes cannot
start a Combo. Outputs support those ordinary keyboard usages, the eight
ordinary modifier keys, and QMK's encoded modifiers with one of those low-byte
usages. For example, Ctrl+C uses output 0x0106. Outputs cannot invoke a macro,
a layer action, Mod-Tap, Layer-Tap, Repeat, a consumer/system usage or reset.

The generic Vial editor may offer unsupported inputs and outputs. The firmware
rejects those records; GUI error display and readback still need interactive
acceptance. Read the entry back after editing it.

The term is fixed at 40 ms. Per-entry terms and three/four-key Combos are not
implemented. Duplicate pairs are allowed; the lowest slot number wins.

## Event behavior

Only an ordinary candidate key press is delayed. Its resolved keycode and
physical position are saved after the normal press-time layer lookup. A
matching second press before the 40 ms boundary suppresses both ordinary
inputs and presses the output through the normal key pipeline. The first
member release releases the output. The other member stays suppressed until
its release. Another Combo cannot begin while either member remains held.
Other keys continue through the normal pipeline during that time.

At elapsed time 40 ms or later, the first key is sent normally before the next
event is handled. The same happens before any admitted nonmatching event,
including a modifier, Mod-Tap, Layer-Tap or encoder event. A quick release sends
the delayed press before that release. The timeout uses unsigned 16-bit timer
subtraction, including timer wraparound. Events are not replayed through
press-time layer lookup, so the saved keycode cannot change with the layer.

The Compact Tapping admission hook remains responsible for duplicate presses,
unmatched releases and cancellation. Combo timeout processing runs before that
hook. Combo matching runs only for physical records in the pre-process hook;
generated Repeat, macro and dual-role tap records bypass it. Outputs use the
normal pipeline, including Caps Word, Repeat learning and shared key/modifier
ownership. Repeat therefore learns the Combo output. A normal delayed input
learns its original keycode when it is sent.

`clear_keyboard()` cancels the pending Combo or held output with the existing
shared owner clear. Compact Tapping blocks any still-held physical sources until
their release. Starting Vial unlock uses that same clear path. A successful
Combo setting change clears held input state before storage changes; a failed
validation changes neither settings nor input state. Unrelated dynamic keymap
changes retain their existing cancellation behavior.

## Saved format

The existing base settings schema remains 0x082002. Keymaps, encoder settings,
macro metadata, six layers and sixteen macros with 8192 shared bytes keep their
addresses and sizes. Combos use a versioned extension in the existing gap at
0x0658–0x06A7. No old byte is treated as a valid Combo without both version
markers and a valid record.

Each of the eight saved entries occupies 10 bytes:

| Offset | Saved value |
| --- | --- |
| 0–1 | First input, little endian |
| 2–3 | Second input, little endian |
| 4–5 | Extension marker 0x0820, little endian |
| 6–7 | Extension version 1, little endian |
| 8–9 | Output, little endian |

On the wire, offsets 4–7 are always zero. A missing marker, another version or
invalid data reads as an empty entry without writing or initializing the gap.
Setting an empty entry writes the same markers with zero inputs and output.
A full raw NVM copy preserves the extension bytes; legacy firmware does not
interpret them. The installer backup distinguishes a legacy image, which has
no Combo section, from an alpha.2 image, which stores a version-1 section with
all eight entries, including empty entries. A backup with an unknown marker or
extension version stops during preflight. When restoring a legacy backup to an
alpha.2 target, all eight target Combos must be empty; otherwise restore stops
before writing and preserves the existing entries. An alpha.2 backup with an
explicit empty section clears all eight target entries. This prevents a legacy
backup from silently clearing Combos.

Each complete entry fits within one 64-byte EEPROM page: the entry start offsets
within their page are 24, 34, 44, 54, 0, 10, 20 and 30. The existing journal
therefore commits a complete entry and its markers together. The setter flushes
before success and checks the latched NVM status before reloading RAM. The NVM
flush verifies every byte of the programmed target page. Any storage failure
returns an error and prevents reload; the existing NVM failure latch stops later
writes. This relies on the existing journal implementation; the journal format, write order and recovery policy are unchanged. The same
work package separately optimizes USB and EEPROM implementation code.

## Offline checks and remaining checks

Run from `qmk-8051-ak820`:

```sh
python3 tests/ak820_combo/run.py
python3 tests/ak820_tapping/run.py --negative-controls --output .build/combo-tapping-host.json
python3 tests/ak820_combo/emitted.py --build-dir .build/combos-candidate \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 --output-dir .build/combo-cpu
```

The first command compiles the production Combo engine and extracted production
storage functions with host C and UBSan. It covers both press orders, first and
second member releases, the 39/40 ms boundary, timer wraparound, quick taps,
interruption, active overlap exclusion, first-slot priority, cancellation,
configuration bounds, marker decoding, invalid requests without writes, NVM
failure and verified-flush failure. The storage fixture models the EEPROM and
NVM status; it does not execute IAP or prove power-loss behavior.

The tapping suite runs the existing production tapping/cache/action/ownership
traces with empty Combo entries, then configured Combo traces through the real
admission, cache, action and output-owner functions. The configured checks cover
6KRO and NKRO, either release order, shared output owners, Repeat learning and
replay, modified outputs, Caps Word, pending/active cancellation, Mod-Tap
interruption and Layer-Tap lookup ordering. It also compares 156 eligible HID
traces with the retained QMK tapping implementation.
The linked C52 suite executes the actual Combo engine, storage reads, Vial
dispatcher and action pipeline. It checks both report modes, output ownership,
timing boundaries, interruption, cancellation and packet results. The identical
record setter case verifies successful reload without changing flash. CPU
execution does not establish physical USB timing, durable settings, interrupt
concurrency, real unlock or GUI acceptance. Hardware acceptance remains open.
