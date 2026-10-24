# Development firmware checks

All 16 named profiles passed 18 frozen build variants from clean source
`55acbb0f7977d4c7840d49143e9b40a15b1dc3c8`. Each passed 28 base suites,
273 base unit tests with zero skips and 14–24 selected supplemental suites.
The [matrix](final/README.md) records CODE, RAM, stack allocations and exact
image identities. Every variant retains its IHX, MAP, MEM, reports and complete
raw build with simulator commands and logs. The raw archive hashes and sizes
are recorded in each `record.json`.

Current profiles include compact Mouse Keys, Auto Shift, GUI controls and
Dynamic Macros in supported combinations. Six layers, 16 Vial macros,
8192 macro bytes, eight two-key Combos, Combo offset `0x658` and schema
`0x082002` are unchanged. Feature behavior is described in
[Build profiles](../../../docs/BUILD-PROFILES.md) and its linked guides.

[Independent review](review.md) records the findings and corrections. The
[integration acceptance](acceptance.md) records host rechecks and artifact
identity checks. Earlier intermediate and rejected builds were removed after
external backup; their original bytes remain in Git history and that backup.
Only the final matrix supports current resource claims.

The foreground stack root remains unresolved. These images are not qualified
for release or installation. The [package gate](final/package-gate.json)
rejects the changed full image because its source differs from the approved
release witness. CPU models do not prove physical USB timing, scan behavior,
interrupt behavior or power-loss persistence. Published and installed alpha.3
remains separate; see [Status](../../../docs/STATUS.md).
