# Module catalog correction review

Date: 2026-10-26. Result: APPROVED for the final delivery commit.

Scope: the uncommitted `web/module-descriptions.json` correction against C2
`d4dbc624d546dbb4f2c132ef60cd165759c84e31`, and its evidence in
`module-catalog-refresh.json`. No production files were edited during review.

## Verified correction

The tracked diff changes only derived fields of the `main` profile. Auto Shift
is added to optional features and the sorted feature list, its make option is
set to `yes`, runtime QMK setting 4 is included, and its timing is 175 ms. These
values match the existing registry. All ten IDs and their order remain
`main`, `game`, `mmo`, `typing`, `code`, `pointer`, `onehand`, `creative`,
`shortcuts`, `multios`. The default remains `main`. All feature description rows,
all profile descriptive fields, all other top-level fields, and the complete
other nine profiles compare equal to C2 after parsing JSON.

The catalog SHA256 is
`2947032a7f53c43d906c3ab909a7fb0beb31d83bae4e44368db422ef18afffc6`.
The registry `qmk-8051-ak820/util/ak820_profiles.py` SHA256 is
`485b8b40d4b78a80e568018ec7736700a11ea460739f4bc8f96a212ef1e056a2`;
its bytes equal BASE `b35b77cddbefdb509058f1fbaaeafaa3982ce172`.
The refresh report agrees with the observed change and catalog identity.

The actual `tools.build_beta_release_assets.validate_module_descriptions`
validator accepts the current JSON bytes. The existing focused command
`PYTHONPATH=tools python3 -B -m unittest test_build_beta_release_assets -v`
passes all 13 tests. No broader suite was run.

## Qualification and provenance

The catalog is absent from `source_files` in all ten
`releases/beta3/*/reviews/program-policy.json` records and from the
`settings-run.json` source snapshot. Every file bound by those ten policies and
the settings snapshot was hashed against its recorded SHA256 and still matches.
All 22 `PYTHON_PACKAGE_FILES` match C2 byte for byte. Thus this ancillary metadata
correction does not invalidate the approved exact binaries or their existing
runtime and host qualification.

`assembly-run.json` records the successful actual ten-profile assembly from C2,
exit code 0, and firmware archive SHA256
`c0b4a1a920ae0d5a6c2c4743c4703ec97dd9fc119d941e87a11dfe611d85d046`.
The ten worker reports are present. No firmware assembly was repeated for this
unbound metadata correction. Existing assembly evidence was inspected; no new
hardware or device validation is claimed.

The final assets catalog will contain the reviewed post-C2 metadata, while
firmware and the 22 host payload files continue to attest C2. Provenance text
must preserve that distinction: C2 must not be described as the source of every
final catalog byte. The catalog hash above and the final delivery commit bind
the correction. This labeling qualification does not require rebuilding
unchanged firmware and does not block approval of the metadata correction.
