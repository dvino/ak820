Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

The source registry defines ten fixed [profiles](profiles/README.md), with
`main` as default. All ten include QMK Settings and schema `0x082003`.
Other profiles exchange selected `main` modules for task-specific functions;
these are complete compositions, not arbitrary toggles. Historical names remain
for reproduction; historical Typing uses `legacy-typing` in current builds.

Beta.3 is published with Caps Word Combo output, macro Layer-Tap, Auto Shift
in `main`, Direct snapshots and complete-frame updates, and the GUI-lock W
pulse. Beta.5 is published with updated profile compositions. Qualification, release
and hardware state are recorded in [Status](STATUS.md).

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

## Next work

- Integrate the firmware contracts into the separate AK Configurator project.
  The companion should identify the exact image before showing controls, read
  the Direct palette as one coherent snapshot, and submit complete frames through
  the begin/chunk/commit protocol. A partial upload must not replace the active
  palette. The firmware handoff documents the protocol.
- Validate Direct color conversion and LED publication on supported hardware.
  Host-side and source checks do not establish physical LED behavior.
- Continue hardware validation of the W indicator, including GUI lock timing,
  active and default layer priority, suspend and resume.

Future functions still require exact-image resource and runtime evidence
before release review.

## Current module limits

Tap Dance has eight entries with four basic or modified-basic outputs, one
pending decision and at most two presses per gesture; resolved holds may
overlap. Key Overrides has eight rows and one physical trigger at a time.
Leader selects saved macros with 1–0 or A–F after its prefix. One Shot supports
modifiers, not layers; its timeout is configurable and defaults to unlimited. Dynamic recording stores two temporary sequences of up
to 16 completed key taps each, separately from the 16 persistent Vial macros.

QMK Settings exposes base timing settings in all ten profiles. Auto Shift settings (QSID 3 and 4) are available in `main` and `typing`; One Shot timeout (QSID 6) follows One Shot availability. The 24-byte `QS` record uses version 2 and CRC; version 1 upgrades in RAM until a setting changes.
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
