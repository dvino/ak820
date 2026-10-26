Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

The source registry defines ten fixed [profiles](profiles/README.md), with
`main` as default. All ten include QMK Settings and schema `0x082003`.
Other profiles exchange selected `main` modules for task-specific functions;
these are complete compositions, not arbitrary toggles. Historical names remain
for reproduction; historical Typing uses `legacy-typing` in current builds.

Beta.2 is published. The beta.3 source adds Caps Word Combo output, macro
Layer-Tap and Auto Shift in main. All ten local images have passed qualification;
publication remains on hold. See [Status](STATUS.md) for artifact and hardware state.

## Configurator

The companion is developed in [AK Configurator](https://github.com/dvino/ak-configurator).
Firmware catalogs and protocol contracts provide its integration baseline.
New module development is paused while existing functions, defects,
documentation and application contracts are completed.

The browser and desktop clients should present the ten complete compositions,
with `main` as the project default. Detect the installed exact image; reserved
storage alone does not enable a control. Unmeasured source rows must remain
unqualified. Backup and restore use the typed storage contract and reject
settings the selected image cannot represent. See the
[requirements](../web/docs/REQUIREMENTS.md), [plan](../web/docs/PLAN.md) and
[development catalog](DEVELOPMENT-CATALOG.md).

## Next firmware work

- Read the current Direct palette from the keyboard, with a coherent snapshot
  across USB packets. This requires a firmware protocol change; application-side
  color caches cannot supply the actual state.
- Apply a complete Direct frame atomically. Stage and validate all LED values
  before commit; incomplete or interrupted uploads must leave the active frame
  unchanged. Define the renderer/DMA publication boundary as well as the palette
  swap. Existing fastset packets do not provide this guarantee.
- Try to fit the GUI-lock W pulse alongside that work: a smooth 2000 ms cycle,
  disabled lock by default, and any nonbase active/default layer overriding W to
  full brightness. Keep Caps and OS indications independent. Main must retain
  Auto Shift; do not silently remove modules to make room. The previous pulse
  candidates overflowed main by 600 bytes and game by 160 bytes.

The detailed continuation instructions are kept in a local handoff outside Git.
New exact-image CODE, XRAM, startup, foreground and IRQ bounds are required after
these changes, before full regressions. No release or device write is authorized
by this plan.

## Current module limits

Tap Dance has eight entries with four basic or modified-basic outputs, one
pending decision and at most two presses per gesture; resolved holds may
overlap. Key Overrides has eight rows and one physical trigger at a time.
Leader selects saved macros with 1–0 or A–F after its prefix. One Shot supports
modifiers, not layers. Dynamic recording stores two temporary sequences of up
to 16 completed key taps each, separately from the 16 persistent Vial macros.

QMK Settings exposes QSID 1, 2, 7, 18 and 19 in all ten profiles, plus QSID 4
for Auto Shift in `main` and `typing`. Its typed, versioned 24-byte record has a CRC.
Tap Dance uses its row term rather than QSID 7. Individual guides describe
rejected inputs and remaining limits.

Other Magic actions remain future work. GUI controls, Mac/PC and modifier swaps
are temporary. Caps variants and persistent Magic settings are outside the
current contract. Any extension needs defined behavior, storage and migration
rules, exact-image resources and startup/stack/IRQ proof before release review.

## Storage and release gates

Current schema03 preserves six layers, 16 macros with an 8192-byte shared
buffer, eight Combos and Combo offset `0x658`. Historical schema02 remains a
supported migration source. Extension records use reserved space documented in
[module storage](MODULE-STORAGE.md); upstream QMK Settings storage must not move
the fixed Combo layout.

All current builds require pass30 and fresh source/IRQ context. Resource use
is measured for each complete linked image. Source composition, host models,
release approval and physical behavior are separate. Future publication needs
independent review, complete exact-image qualification and matching installer
evidence. The [module matrix](MODULE-MATRIX.md) describes composition;
[Status](STATUS.md) records actual evidence and release state.
