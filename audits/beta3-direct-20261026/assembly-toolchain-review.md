# Assembly toolchain review

Result: approved for the next audit-only commit and subsequent canonical assembly from synchronized original roots. This is a static and offline integration review, not a successful release assembly or hardware validation.

Reviewed SHA256 identities:

| File | SHA256 |
| --- | --- |
| `assemble_origins.py` | `c1acb5b1b266799e1ff0d8736bb31854f098cc2041feac1b8390a565e653177a` |
| `test_assemble_origins.py` | `b0915559ad7d9bc963c2c569e62b3f680bc2058aa7e4c0081b486de3081f7d38` |
| `assembly-toolchain-fix.md` | `4c0c3263616d0621d93bb1195a1218da657ed712deb14e023844ad26c41600f0` |

The first revision incorrectly applied repository-local symlink rejection to the original qualification toolchain path. All three actual isolated roots have a `toolchains` symlink, so that revision would fail before assembly. The correction restores the original `.resolve()` behavior for matrix and capability checks. The regression test now includes an origin symlink to an external shared proof directory and a separate local mirror. The blocking finding is closed.

Only `ci.assemble` receives the optional local mirror. Relative path checks and symlink rejection protect that assembly path. Both resolved toolchain trees reject internal symlinks and unsupported entries. Their complete relative-file SHA256 inventories must match before assembly and remain unchanged afterward. The original qualification command paths and proof inputs are preserved. Child failure details reach outer stderr while the original exception remains a failure.

Independent verification on 2026-10-26:

- `python audits/beta3-direct-20261026/test_assemble_origins.py`: 12 tests passed after correction.
- Every ordinary file in all four local toolchain copies was independently hashed and compared with `assembly-toolchain-copies.json`. SHA256, mode and size match for all 4,197 files in each copy, totaling 280,064,626 bytes. No symlinks were found.
- The unmodified original-root `tools/build_release_bundle.py` `validate_tools` function accepted the local mirror against the actual `build-report.json` for main, game, mmo, creative, typing, code, multios, pointer, onehand and shortcuts. Each check ran in its recorded original root with that root's modules. No assembly was invoked.
- All ten program policies exclude the three changed helper, test and explanation paths from `source_files`. Canonical tools, program policies, firmware, host code and qualification inputs are unchanged by this diff. Existing frozen 290-source qualification remains applicable; this audit helper correction does not require firmware or full qualification reruns.

Canonical repository-local tool validation, pinned compiler and assembler hashes, builder and input checks, qualification contracts, program authorization, source binding and bundle authorization remain unchanged. This approval permits those gates to run; it does not predict their outcome or waive them. No build, assembly, commit, synchronization, network or device operation was performed during this review.
