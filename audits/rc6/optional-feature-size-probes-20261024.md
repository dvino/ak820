# Optional feature size probes

Date: 2026-10-24. These isolated flag measurements use the earlier compact
candidate `24e97578ee469e5343d6949976fef96898d87c0e38ec6148374af1b1611a1655`
as control. That candidate contains the later-discovered Grave Escape defect
and is not approved for installation. These are code-size comparisons, not
functional qualification of the disabled profiles or current final-image costs.
The primary profile keeps both functions enabled and retains implementation
source.

| Profile | Populated CODE | Main / low CODE | XRAM | Allocated stack capacity | CODE saving |
| --- | ---: | ---: | ---: | ---: | ---: |
| Control | 40,414 | 38,603 / 1,811 | 2,512 | 154 | — |
| Grave Esc disabled only | 40,119 | 38,308 / 1,811 | 2,506 | 157 | 295 |
| NKRO disabled only | 39,744 | 37,933 / 1,811 | 2,428 | 154 | 670 |

Both full pinned SDCC 4.6.0 builds succeeded in the isolated checkout
`/tmp/ak820-grave-esc-probe`. Their output directories are
`qmk-8051-ak820/.build/grave-esc-disabled-20261023` and
`qmk-8051-ak820/.build/nkro-disabled-20261023`. IHX hashes:

- Grave Esc off: `d11c8526adca506b1210becdd495528c425dd116e8c8b50dee2d0665c37f5557`.
- NKRO off: `54c81077019494908bdd88134e55251895fd7d97ccbd3a4b663cfd98ae28deec`.

The later primary Grave Escape correction changes the exact control. Remeasure
before selecting a final profile; separate savings are not guaranteed to add.
NKRO implementation source is retained even if a future profile disables it.
No USB or device operation was performed.

## Combo probe: no linked size

The ordinary QMK/Vial Combos flag failed to compile on the pinned SDCC. Local
probe-only compatibility changes addressed the repeated combo_t typedef,
unsupported empty/aggregate initializers, and MAKE_COMBOEVENT's incompatible
aggregate expansion. Compilation then hit an internal SDCC validateLink error
in SDCCast.c:1904 while compiling process_combo.c. A further bounded attempt
with EXTRA_SHORT_COMBOS and four Vial entries hit the same compiler failure.
There is no final combo object or linked image, so no honest CODE delta exists.

Logs are retained under `.build/combos-enabled-probe-20261023`,
`.build/combos-sdcc-header-probe-20261023`, `.build/combos-sdcc-init-probe-20261023`,
`.build/combos-sdcc-event-probe-20261023` and
`.build/combos-four-short-probe-20261023` in that isolated checkout.
The complete uncommitted probe patch is preserved outside Git at
`/home/danil/Documents/ak820-private-backup-20261023/optimization-probes/optional-features/combo-port-probe.patch`.
The two untracked tapping production files and reconstruction metadata are
preserved beside that patch as well. None of these compatibility changes is
integrated into the primary firmware.

A bounded two-key compact implementation may target about 1 KiB; a planning
allowance of 1–2 KiB is an engineering estimate, not a measurement or promise.
Full QMK/Vial behavior is a different scope. Future implementation needs its
own event contract, Vial/NVM plan, selected capacity, interaction tests and
paired linked measurements. It remains future work in ROADMAP.
