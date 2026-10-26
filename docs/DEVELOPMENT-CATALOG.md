Русский перевод: [Каталог возможностей](ru/DEVELOPMENT-CATALOG.md).

# Development capability catalog

`tools/build_capability_catalog.py` describes exact qualified development images.
Each entry needs the image's foreground, startup and interrupt proof, base logs
and profile tests. Source presence and passing unit tests do not supply that
qualification or authorize installation, settings writes or publication.

The current source registry has ten [profiles](profiles/README.md), with `main`
as default. All use schema `0x082003` and QMK Settings. The source
[firmware matrix](../web/firmware-matrix.json) may contain unmeasured rows;
[capability-catalog.json](../web/capability-catalog.json) has no qualified entries
until exact-image qualification is imported. Never substitute design-build
hashes or a previous release's results. Published beta.1 on 2026-10-25 supplied
a nine-profile catalog and standalone installers for exact `work`; its image
identities remain separate.

Join qualified records by exact IHX SHA256. Profile names are display labels.
The linked-window `code_identity` does not replace the permanent packed CODE
identity used for settings restoration. Packing includes entry, callbacks and
the native erase helper absent from the sparse linked windows.

`module_storage` uses `ak820-module-storage-contract-1`. Schema03 reserves eight
Tap Dance rows, eight Key Override rows and the QMK Settings record even when
those commands are disabled. Use `enabled_entries` and `enabled_qsids` to show
controls. Historical schema02 has no extension storage. See the
[module matrix](MODULE-MATRIX.md) for current composition; missing measurements
remain unknown.

Settings fields specify QSID, width, little-endian encoding, range, default,
NVM offset and consumers. All ten enable QSID 1, 2, 7, 18 and 19; `typing` also
enables QSID 4 for Auto Shift. Tap-code delays apply only to the listed helpers,
not compact tapping, Space Cadet, Tap Dance gestures or explicit macro down/up
timing. Tap Dance uses its own row term; zero selects 200 ms, independently of
QSID 7. The shared codec validates stored records.

Current builds require the audited pass30 chain and a fresh source/IRQ context;
see [Build profiles](BUILD-PROFILES.md). Qualification checks exact sources,
pinned tools, transform proofs and image before full regressions. Catalog
export preserves these distinctions and does not promote a successful host
model to physical behavior or power-loss persistence.

Settings migration names an explicit target and preserves schema02 Combos.
Known beta.1 `work` is represented by its pinned historical IHX/CODE descriptor,
not by reinterpreting its name through the current registry. Cross-image restore
requires an explicit reviewed edge and supported target settings. Schema03
cannot downgrade to schema02. Unsupported keycodes, inactive nonempty tables
or missing setters stop before writes. See [module storage](MODULE-STORAGE.md).
