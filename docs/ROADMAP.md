Русский перевод: [Планы](ru/ROADMAP.md).

# Roadmap

The source tree contains 24 named development profiles. The three compact modules
Tap Dance, Key Overrides and QMK Settings each have a separate profile that adds
only that module to `full`; no profile combines all three. These source profiles
are not approved for release. Published and installed alpha.3 remains unchanged.
See [Build profiles](BUILD-PROFILES.md) for the profile list and module guides
for exact limits.

## Next work

The next product phase is the desktop configurator contract and capability
catalog. The client should derive controls from the exact linked build's
catalog, distinguish stored capacity from enabled features, and expose only
commands supported by that profile. Backup and restore must use the typed
module-storage contract and reject settings that cannot be represented by the
target image. See the [configurator requirements](../web/docs/REQUIREMENTS.md),
[implementation plan](../web/docs/PLAN.md), and
[development catalog](DEVELOPMENT-CATALOG.md).

## Future feature work

The current modules intentionally have narrow contracts. Tap Dance has eight
entries, four basic or modified-basic outputs per entry, one pending decision,
and at most two presses per gesture; holds that have resolved can overlap.
Key Overrides has eight rows and captures one physical trigger at a time.
QMK Settings exposes QSIDs 1, 2, 7, 18 and 19; QSID 4 is reserved for a future
profile combining this module with Auto Shift. The settings record is a typed,
versioned 24-byte record with CRC and backup/migration support. See the module
guides for rejected actions and behavior details.

Other Magic actions remain future work. Current GUI controls and modifier swaps
are volatile. Caps variants and persistent Magic settings are outside the
current contract. Any extension needs a defined user-visible behavior, storage
and migration rules where applicable, and exact-image resource and runtime
qualification before it can be considered for a release.

## Storage and compatibility

Schema `0x082003` is limited to the three new module profiles. Existing
schema `0x082002` formats and release defaults remain unchanged. Six layers,
16 macros with 8192 bytes of macro data, eight Combos and their fixed offset at
`0x658` are retained. New module records use the reserved space documented in
[module storage](MODULE-STORAGE.md). Do not enable upstream QMK Settings storage:
it moves the fixed Combo layout.

New profile combinations must preserve existing capacity and storage behavior.
Feature costs depend on the complete linked image, so each profile requires its
own CODE, RAM and stack measurements. Runtime and regression evidence is kept in
[Status](STATUS.md); a source profile does not qualify a release or describe the
installed alpha.3 image.

## Later releases

The published and installed alpha.3 image remains the approved release. New
source profiles require the existing release review and installer transition
process before publication. This roadmap does not change that policy.
