Русский перевод: [Каталог возможностей](ru/DEVELOPMENT-CATALOG.md).

# Development capability catalog

`tools/build_capability_catalog.py` describes exact development builds for a
desktop client. It does not authorize settings writes, firmware installation
or release publication. A catalog entry requires the complete exact-image
foreground, startup and interrupt proof, base regression logs and profile tests.
A source profile alone cannot produce a verified catalog entry.

The generated [nine-image capability catalog](../web/capability-catalog.json)
contains the qualified typed storage and settings contract. Join it to
[firmware-matrix.json](../web/firmware-matrix.json) by exact IHX SHA256, using
profile IDs for display. Its linked-window `code_identity` is not the packed
permanent CODE identity used to authorize a settings restore.

The additive `module_storage` field uses format
`ak820-module-storage-contract-1`. Its `modules` object separates stored
capacity from enabled commands. Schema03 reserves eight Tap Dance rows, eight
Key Override rows and the QMK Settings record even when a module is inactive.
The curated `tap-dance`, `key-overrides` and `settings` packages each enable
their named extension. Legacy `full-*` names remain available in the low-level
CLI for reproducing older builds. Desktop controls must use `enabled_entries`
and `enabled_qsids`; stored values alone do not make a control available.
Schema02 entries declare no extension storage. The nine curated packages and
their measured costs are summarized in the [module matrix](MODULE-MATRIX.md).

Settings fields describe QSID, width, little-endian encoding, range, default,
NVM offset and active consumers. QSID 4 remains reserved; none of the nine curated packages enables both QMK
Settings and Auto Shift. It must not be exposed as an available control. Tap-code
delays apply only to the helpers listed in the contract. They do not affect compact tapping, Space
Cadet, Tap Dance gestures or explicit Vial macro down/up timing. Tap Dance
uses its row term, with zero selecting 200 ms; it does not use QSID 7.
The shared codec remains the authority for validating records and rows.

The contract also records padded row addresses, protocol operations, runtime
limits and restore restrictions. Migration requires an explicit target and
preserves schema02 Combos. Macro capacity checks remain mandatory. A schema03
backup cannot restore to schema02. Differences in inactive tables or settings
without a setter block restore before any write. See
[Module settings storage](MODULE-STORAGE.md) for the complete storage contract.

Catalog verification is offline. Physical behavior and persistence after power
loss remain separate checks. No catalog for an unqualified image is supplied
by the source-level contract or its unit tests.
