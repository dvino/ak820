# Beta.3 source admission review

Independent review, 2026-10-26. No actionable findings remain in this bounded
source review. This accepts the inspected source structure and documentation
contracts. It does not approve generated catalogs, policies, packages, a commit
or publication. The final immutable outputs require a separate review.

The tracked candidate was captured in the external private backup as
`20261026-beta3-review/source-candidate.patch`, SHA256
`d9eec50ad59db02b0bdc25d5f636721ec7c11dabb49e9a7baa7078a0aba4eacb`.
Production code was not changed during this review. Only this report was added.

## Source and contracts

Combo output admission adds only Caps Word toggle. Inputs retain their existing
restrictions. Firmware and host protocol checks agree on the added output.
The compact macro Layer-Tap namespace is six layers times sixteen macro slots:
high bytes 40 through 45 and low bytes F0 through FF. Encoder sources are rejected
before acquiring pending or held state. A short accepted matrix-key release
uses the existing macro sender; timeout, interruption and cancellation retain
the existing tapping ownership rules. Generated macro records do not enter
this physical decision path. The new direct call still requires fresh linked
stack and interrupt qualification for every image.

The CRC relocation is guarded for SDCC mcs51 and does not change the CRC
algorithm. Source inspection alone does not establish the new linked layout,
memory fit or stack bound.

Current profile validation remains strict. Frozen beta.2 configurations have a
separate source reader, preserving old MAIN without Auto Shift and its old
runtime settings IDs. New exact-image identities explicitly declare Combo and
macro Layer-Tap support. Missing historical fields mean no support. Backup and
restore validation reject the new namespace for encoders, macro commands and
unsupported exact images. Historical rows remain migration sources rather
than restore targets.

English and Russian guides agree on the keycode formula, physical-key limit,
Caps layout example, MAIN Auto Shift, deferred MAIN GUI lock, and earlier image
limits. INSTALL, installer asset paths and workflow staging consistently target
beta.3. Release notes describe user-visible changes and limits. STATUS retains
the distinction between the source candidate, incomplete release preparation
and untested physical behavior. The later final evidence update is outside
this snapshot review.

## Measurement and preparation

`measure_origin.py` calls the unchanged canonical firmware matrix CLI in the
retained original source root. It compares current test/runtime/build-source
inputs, every copied build file and the native reference before and after the
measurement. The retained qualification interpreter must be the same binary.
The selected row must pass exact-image runtime and offline-test admission.
The receipt binds command, interpreter, native input, sources, whole build
tree, matrix and log. The test source snapshot includes the canonical matrix
and other tools; it is not limited to firmware sources.

`prepare_release.py` retains the binding, matrix and log in policy source
closure. It keeps the frozen previous catalog unchanged, constructs a separate
source-only view for historical loading, and creates transitions only to new
images. It compares packed CODE identity and complete macro fixture bytes.
Private outputs remain outside the repository. No helper edits canonical
proofs, rewrites qualification paths or generates independent approval.

Reviewed untracked input SHA256 values:

| File | SHA256 |
| --- | --- |
| `measure_origin.py` | `114c3eb7262eaadba6800a1b54b432765141fac82091b416e655be76ee2ed80e` |
| `prepare_release.py` | `f5b09cb533327c03599622105c160e6e835ae0af0c3957852dad06e41bf6c270` |
| `test_measure_origin.py` | `e9e5e4c5d1bdac7c491740592ec01d4220ee16dae3dfee6b0e09d21c6ebc557d` |
| `test_prepare_paths.py` | `674c79a03efdfa1d8fafd66a3cd2a7ee8780acbd5156f919ea400967fa320cb5` |
| `ci/beta3-release-notes.md` | `0c468953e0897316d56b5d71dae245d42da30e5d1197d164663cf2a2c1e24d2a` |

## Independent checks

- `python tools/installer/test_catalog_settings.py`: 21 tests passed.
- The three selected exact-image macro, Combo and historical-source contract
  tests also passed separately.
- `python tools/check_docs.py`: 77 public documents, zero failures.
- In explicitly selected WSL Ubuntu, `test_measure_origin.py` and
  `test_prepare_paths.py` passed two tests each. Negative controls cover source
  mismatch, copied-build mismatch, failed canonical measurement, unsafe build
  paths and explicit path preservation.

The initial native Windows helper-test attempts failed on the Store Python
executable shim and missing symlink privilege. The same tests passed in their
intended Ubuntu environment. These failures do not qualify native Windows
execution of the audit helpers.

No build, full firmware regression, physical key check, settings write,
bootloader transition, reset or flash was performed by this review. Final
ten-profile measurements, packing, migration outputs and source-bound policies
remain required before release admission.
