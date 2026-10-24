Русский перевод: [Каталог возможностей](ru/DEVELOPMENT-CATALOG.md).

# Development capability catalog

`tools/build_capability_catalog.py` describes exact development builds for a
desktop client. It does not authorize settings writes, firmware installation
or release publication. A catalog entry requires the complete exact-image
foreground, startup and interrupt proof, base regression logs and profile tests.
A source profile alone cannot produce a verified catalog entry.

The additive `module_storage` field uses format
`ak820-module-storage-contract-1`. Its `modules` object separates stored
capacity from enabled commands. Schema03 reserves eight Tap Dance rows, eight
Key Override rows and the QMK Settings record even when a module is inactive.
The `full-tap-dance`, `full-key-overrides` and `full-qmk-settings` profiles each
enable only their named module. Desktop controls must use `enabled_entries`
and `enabled_qsids`; stored values alone do not make a control available.
Schema02 entries declare no extension storage.

Settings fields describe QSID, width, little-endian encoding, range, default,
NVM offset and active consumers. QSID 4 remains stored but is unavailable
without both QMK Settings and Auto Shift. Tap-code delays apply only to the
helpers listed in the contract. They do not affect compact tapping, Space
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
