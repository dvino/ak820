Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

The source registry defines nine curated profile packages that cover all 14
optional modules. The default `work` package includes Leader, Dynamic Macros
and OS indicator control; it excludes Mouse Keys and Mac/PC mapping. The
packages are fixed combinations, not independent toggles. Older profile names
remain available in the low-level CLI for reproducing earlier builds. New
source images have their own qualification records; published and installed alpha.3
is unchanged. See [Status](STATUS.md), [Build profiles](BUILD-PROFILES.md) and the
[module matrix](MODULE-MATRIX.md).

## Configurator

New module development is paused for the beta. Firmware work now covers the
existing profiles, defects, documentation and application contracts.

The next product phase is the browser and desktop configurator. The client
should use an exact-image catalog, distinguish reserved storage from enabled
controls, and show only commands supported by the installed profile. Present
the nine curated packages as whole choices, with `work` as the default when
selecting a project package. Backup and restore must use the typed module
storage contract and reject settings the target image cannot represent. See
the [requirements](../web/docs/REQUIREMENTS.md),
[implementation plan](../web/docs/PLAN.md), and
[development catalog](DEVELOPMENT-CATALOG.md).

## Module limits and future work

The modules have bounded behavior. Tap Dance has eight entries, four basic or
modified-basic outputs per entry, one pending decision and at most two presses
per gesture; resolved holds can overlap. Key Overrides has eight rows and
captures one physical trigger at a time. QMK Settings exposes QSID 1, 2, 7, 18
and 19 in the `settings` package. QSID 4 remains reserved for a future package
that combines QMK Settings and Auto Shift. Its settings record is versioned,
typed, 24 bytes and protected by CRC; backup and migration are supported. The
individual guides document rejected inputs and limits.

Other Magic actions remain future work. Current GUI controls and modifier
swaps are temporary. Caps variants and persistent Magic settings are outside
the current module contract. Any extension needs defined user behavior,
storage and migration rules where applicable, and exact-image resource and
runtime qualification before release consideration.

## Storage and compatibility

Profiles that enable Tap Dance, Key Overrides or QMK Settings use schema
`0x082003`; other profiles retain `0x082002`. Both schemas preserve six layers,
16 macros with 8,192 bytes of macro storage, eight Combos and the fixed Combo
offset at `0x658`. Extension records use reserved space described in
[module storage](MODULE-STORAGE.md). Do not enable upstream QMK Settings
storage; it moves the fixed Combo layout.

Resource use depends on the complete linked image. The [module matrix](MODULE-MATRIX.md)
records each package's measurements; [Status](STATUS.md) records current
qualification and release state. A source profile does not establish physical
behavior or release approval.

## Later releases

The published and installed alpha.3 image remains the approved release. A new
profile package requires the existing independent release review and installer
transition process before publication.
