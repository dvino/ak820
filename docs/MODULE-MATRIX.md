Русский перевод: [Матрица модулей](ru/MODULE-MATRIX.md).

# Module and profile matrix

The application catalog contains **nine profiles**, selected as whole packages. **`work`** is the default. The catalog covers all 14 existing optional modules; it does not offer arbitrary module combinations.

Profile membership comes from the [firmware registry](../qmk-8051-ak820/util/ak820_profiles.py). Machine-readable data is in [firmware-matrix.json](../web/firmware-matrix.json). The [feature catalog](FEATURES.md) describes behavior and limits; [Status](STATUS.md) records qualification and release state.

## Profiles

| Code | Profile | Purpose |
| --- | --- | --- |
| W | `work` | Recommended general-purpose profile. Adds Leader and two temporary Dynamic Macro slots, with OS indicator support. Mouse Keys and Mac/PC mapping are not included. |
| E | `essential` | A compact everyday option with NKRO control, One Shot and Space Cadet. |
| T | `typing` | Use when holding supported letter or number keys should produce their shifted form. |
| M | `mouse` | Use keyboard keys to control pointer movement and scrolling. |
| MT | `mouse-typing` | For users who need keyboard mouse actions and shifted output from supported held keys. |
| S | `system` | Use to adapt modifier output for Windows, Linux or macOS. All mappings reset on restart. |
| TD | `tap-dance` | Choose different supported keyboard actions for taps, holds and repeated taps. |
| KO | `key-overrides` | Replace a selected key when the configured modifier and layer conditions match. |
| QS | `settings` | Adjust supported Combo, tap-hold, Grave Escape and related values through Vial. |

All nine profiles include six layers, 16 Vial macros with a shared 8192-byte buffer, eight two-key Combos, Mod-Tap/Layer-Tap, both encoder directions, media/system keys, NKRO reports, Caps Word, Repeat and Alt Repeat, Grave Escape, Tri Layer, RGB effects and VialRGB Direct in RAM. NKRO control, One Shot and Space Cadet are also common to all nine.

## Module membership

| Module | W | E | T | M | MT | S | TD | KO | QS |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Compact Tap Dance | — | — | — | — | — | — | ✓ | — | — |
| Key Overrides | — | — | — | — | — | — | — | ✓ | — |
| QMK Settings | — | — | — | — | — | — | — | — | ✓ |
| Mac/PC mode | — | — | — | — | — | ✓ | — | — | — |
| OS indicator override | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — |
| Compact Leader | ✓ | — | — | — | — | — | — | — | — |
| NKRO control | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| One Shot | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Space Cadet | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Compact Mouse Keys | — | — | — | ✓ | ✓ | — | — | — | — |
| Compact Auto Shift | — | — | ✓ | — | ✓ | — | — | — | — |
| GUI lock | — | — | — | — | ✓ | ✓ | — | — | — |
| Ctrl/GUI swap | — | — | — | — | — | ✓ | — | — | — |
| Compact Dynamic Macros | ✓ | — | — | — | — | — | — | — | — |

A dash means that the module is absent from that profile. A pair absent from every profile is reported as “No available profile”; this does not prove that the combination is impossible to implement. Other combinations are outside this catalog.

## Memory

Sizes come from each final IHX/MAP/MEM linked with pinned SDCC 4.6.0 and checked short calls. Individual module sizes are not additive; each complete image is measured. Free space in one CODE window cannot extend the other window.

| Profile | CODE bytes | Main / low trailing bytes | XRAM / 3072 | Stack bound / capacity | Stack margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| `work` | 40386 | 22 / 92 | 2676 | 162 / 165 | 3 |
| `essential` | 38660 | 1748 / 92 | 2564 | 162 / 167 | 5 |
| `typing` | 39281 | 1127 / 92 | 2581 | 162 / 166 | 4 |
| `mouse` | 39523 | 885 / 92 | 2594 | 162 / 167 | 5 |
| `mouse-typing` | 40285 | 123 / 92 | 2614 | 162 / 166 | 4 |
| `system` | 39082 | 1326 / 92 | 2567 | 162 / 166 | 4 |
| `tap-dance` | 40173 | 311 / 16 | 2795 | 166 / 166 | 0 |
| `key-overrides` | 40464 | 20 / 16 | 2734 | 162 / 162 | 0 |
| `settings` | 40075 | 409 / 16 | 2640 | 162 / 166 | 4 |

The stack bound includes foreground code, startup and every enabled interrupt source for the exact image. `tap-dance` and `key-overrides` have zero stack margin; they meet the current bound but have no room for growth without a new analysis. [Status](STATUS.md) records qualification and its limits. XRAM excludes the separate 512 DMA bytes. Macro storage and NVM are not executable CODE.

## Default profile

`work` adds Leader, Dynamic Macros and companion-controlled OS indication to the common base. Leader selects one of 16 saved Vial macros with a prefix and selector key; Dynamic Macros record two short temporary sequences. These support navigation layers, editor commands and repeated work tasks.

Mac/PC and Mouse Keys are excluded from the default. Auto Shift has its own `typing` profile because it changes held-key typing. Tap Dance, Key Overrides and QMK Settings are separate packages. Only small changes to existing code were made to fit `work`; no new module was introduced.

## Application contract

`firmware-matrix.json` binds profile IDs, compiler switches, capabilities, measurements and exact image SHA256. Memory, runtime, regression and installation states are separate. These candidates retain `release_approved=false` and `installable=false`; a profile name never grants write permission.

`module-descriptions.json` supplies Russian/English titles, popup summaries, limits and guide links. Each module summary also introduces its guide section. Settings restore requires the exact packed CODE `settings_identity`, derived with a validated OEM reference. It remains `null` before packaging; cross-image transitions require explicit hash pairs. See the [desktop handoff](../web/docs/FIRMWARE-HANDOFF.md).

### Fields used by the desktop

Use `default_profile` for the initial selection. The optional CLI `--resolve`
filters the existing packages by requested modules and chooses the smallest
superset; it does not change the default or compile a new combination.

| Field | Use |
| --- | --- |
| `profiles[].id`, `profile` | Stable package IDs; join to translated descriptions by ID. |
| `configuration` and `build_recipe` | Exact feature switches, schema, fixed defaults and short-call selection. |
| `capabilities.optional_modules` | Enable only the controls implemented by this image. |
| `capabilities.dynamic_entries` | Eight Combos; eight Tap Dance or Key Override entries only in their corresponding package. |
| `capabilities.runtime_qmk_settings_ids` | IDs available for live settings; stored but inactive fields are excluded. |
| `identity` and `resources` | Artifact hashes and exact linked CODE, XRAM and control-stack measurements. |
| `measurement_status`, `runtime_status`, `offline_tests_status` | Independent build and qualification results. |
| `feature_pairs` | Which curated packages contain each of the 91 pairs of optional modules. |
| `settings_identity`, `settings_transitions` | Exact packed settings contract and explicitly approved restore pairs. |
| `release_approved`, `installable` | Separate approval state; offline success does not turn these on. |

The candidate ZIP uses `profiles/<id>/firmware/application.ihx`, `.map` and
`.mem`, plus configuration and qualification summaries. Its manifest lists every
file and SHA256. It contains nine applications; it is not an installer bundle
or the complete independent qualification evidence. Full build files, listings,
witnesses and logs are retained in the technical report referenced by Status.
