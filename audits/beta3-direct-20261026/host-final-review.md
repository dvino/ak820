# Beta.3 final host and release review

Date: 2026-10-26. Scope: uncommitted host/release changes against
`b35b77cddbefdb509058f1fbaaeafaa3982ce172`, plus the bounded journal fixture.
No production or test files were edited during this review.

## Disposition

The reviewed host/release changes and bounded fixture have no remaining findings
in this scope after the focused closure review below. This report does not admit
pending generated catalogs, final images or release approvals. It does not
authorize device writes.

## Closed finding: Direct guides missing from package allowlist

The initial `tools/build_windows_installer.py:PUBLIC_GUIDES`, also used by the Python asset
builder, omitted `docs/DIRECT.md` and `docs/ru/DIRECT.md`. The actual packaged
README, CONFIGURATION, FEATURES and SETTINGS-BACKUP documents contain eight
relative links to these absent files. Both Python packages and the catalog
archive therefore lost the new Direct protocol guide.

The initial asset suite passed because `PromotionTests.make_inputs` replaced every
guide with `# public guide`; its link assertion never saw the real links.

Closure: both Direct guides are now in the explicit English/Russian allowlists.
The test fixture copies real allowlisted guide and asset bytes from the source
tree, so ZIP and tar link checks exercise the actual documents. A focused
independent rerun passed all 13 asset tests. A separate scan of actual public
guides found zero unresolved local file links. The packaging blocker is closed;
no production firmware code changed for this correction.

## Reviewed corrections

- `set_direct_frame` copies and clamps V bytes to 160 before BEGIN. Strict ACK
  equality remains in place, and chunk failures stop without automatic abort,
  commit or retry. Write permission is checked before device I/O.
- Direct backup metadata requires exact-image capability and runtime negotiation.
  RAM palette recovery remains separate from NVM recovery, uses a fresh
  generation, and checks palette readback.
- English and Russian installation commands use `.\AK820.cmd` in PowerShell.
  The launcher invokes the Python CLI and the guides describe Python setup.
- `HOST_FILES` removes the GUI entry point, standalone builders and bundled
  build requirements. `validate_host_manifest` still requires exact set equality
  and matching size/hash records. Historical manifests containing the removed
  entries fail validation; no compatibility bypass was introduced.
- The Python asset builder still requires the exact ordered ten approved
  contexts, validates bundle payload sizes/hashes and image/catalog identities,
  and writes deterministic archives with matching checksums. CI invokes this
  builder and checks the published checksums. The publish heredoc is terminated.
  This review does not substitute for running the workflow on GitHub.

## Bounded fixture

The fixture now follows all parsed linked XDATA areas, including initialized
XDATA, and requires the memory report to agree with the map's exclusive end.
Missing bounds, out-of-range areas or insufficient nine-byte space stop the run.
Source and README agree on ordinary XRAM `[0x0440, 0x1000)`.

The inspected main image has XSEG `[0x0440, 0x0f03)` and XISEG
`[0x0f03, 0x0f6a)`. Its fixture is `[0x0f6a, 0x0f73)`. Existing
`qmk-8051-ak820/.build/beta3-final/main/bounded-fixture-recheck/results.json`
records 2,304 passing mutations. The independently hashed image and map match
that report:

- IHX: `391d6dbca948b46cfc4be989b0055f310fbdfaf832bdc634c76ff2bf5e23b34e`
- MAP: `d339c81bb4e28635b2561371980ae45bca46c4a238af6d4897c3d0ab2e4a363a`

The recorded helper peak is 18 bytes without interrupt overlap. This is CPU
helper evidence, not a new whole-image stack admission or physical durability
test. No firmware was built or device accessed during review.

## Independent reruns

| Suite | Result |
| --- | --- |
| `tools/test_build_beta_release_assets.py` | 13 passed |
| `tools/test_build_ci_release.py` | 10 passed |
| `tools/test_ak820_device_protocol.py` | 21 passed |
| `tools/installer/test_settings_backup.py` | 42 passed |

The initial read-only scan found the eight missing Direct links described above.
After correction, the same scan found none, and the 13 asset tests passed again
with actual guide content. Final multi-profile qualification, generated catalog
validation and exact final-image release admission remain separate gates.
