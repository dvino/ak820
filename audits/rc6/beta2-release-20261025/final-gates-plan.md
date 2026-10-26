# Beta.2 final policy gates

Read-only preparation, 2026-10-26. No final program approval. No USB, compiler proof or regression rerun performed. Existing exact-program and final-tree source reviews explicitly retain final approval as pending.

## Freeze and regenerate

Wait for all ten full qualification and profile-specific results, freeze code/tests/docs, then run from `/home/danil/ChatGPT/ak820-beta2-20261025`:

```bash
python audits/rc6/beta2-release-20261025/prepare_profile_policy.py --settings-run audits/rc6/beta2-release-20261025/settings-final-run.json
```

The settings run must be the real completed frozen run; the helper validates its successful exit, source SHA256 snapshot and log SHA256. It does not create independent approval. It also does not validate complete qualification/profile suites, so successful regeneration alone cannot close those gates.

Canonical builds: group a = main/game/mmo/creative; b = typing/code/multios; c = pointer/onehand/shortcuts. Each path is `/home/danil/ChatGPT/ak820-beta2-qualified-GROUP-20261025/qmk-8051-ak820/.build/next-PROFILE-release2-certified`. Canonical release order is main/game/mmo/typing/code/pointer/onehand/creative/shortcuts/multios.

## Concrete independent validator proposal

Write an external scratch validator, not a tracked approval generator. For each canonical build B and frozen repository R:

1. Load `build-report.json`, `configuration-report.json`, `qualification.json`, `profile-tests/results.json`, `runtime-safety/summary.json` and `runtime-stack.json`. Require configuration == `ak820_profiles.configuration(profile)`, report target ajazz/ak820/vial, compiler 4.6.0, build schema == configured NVM schema, hardware_validated false. Use `ak820_profiles.require_release_qualification(report)`; verify each artifact size/hash at its actual B location. Identity must match actual IHX/MAP and all stable configuration-report identity fields.
2. Call `build_ci_release._qualification(q, B/'qualification.json', ihx, map, R/'toolchains/sdcc-4.6.0')` and `ak820_ci_authorization.validate_qualification_contract(q)`. These validate existing evidence, without executing tests. Require configuration report offline_tests_passed true. Validate per-profile tests against the frozen `configure_firmware.test_source_snapshot()`, original command/cwd/build/simulator paths, unchanged before/after identity and every original log hash. To reuse `configure_firmware.validate_profile_tests` without rewriting old evidence, temporarily set that module's ROOT/QMK to the original group checkout and `sys.executable` to the recorded interpreter, while overriding `test_source_snapshot` to return the frozen root's already captured snapshot. Pass the original toolchain path actually recorded in the profile commands; independently validate its binary pins. Restore globals afterward. Do not accept a command mismatch or silently normalize away suite flags.
3. For policy `ci/profiles/P/release-policy.json`, check every source record via `ak820_release_safety.checked_record(R, name, record)`; also require every non-generated source row in the actual build report represented with the same SHA256. Check the committed LUFA lock and its special dependency closure as implemented by `_validate_policy_sources` (after commit, call that function directly). Require IHX SHA256 and `authorization.symbols_sha256(map)` equality; normalized symbols are intentional, raw MAP is not the cross-workspace program identity.
4. Validate exact safety witnesses through `ak820_release_safety.validate(report, scratch_root)`. Because actual artifacts live in other worktrees, populate a fresh temporary root with ordinary copies of the frozen safety manifest, all its declared source files, all witness files, transition logs/preflight result, and IHX/MAP/MEM at the report's original relative `qmk-8051-ak820/.build/next-P-release2-certified/...` paths. Do not edit report bytes or substitute symlinks: `safe_path` deliberately rejects symlinks. Copy only from frozen R for source/witness/log files and canonical B for artifacts. This executes the complete existing capacity/startup/IRQ/transition checker without rerunning its producers. Check full original runtime summary source snapshot against frozen R too.
5. Independently compare transition matrix target IHX, 12 cases/profile, 120 overall, all passed, exact alpha2 preflight counts 498/12/8, settings code hash and settings catalog identities with measured actual builds. The checker validates the alpha2 evidence hash but does not itself reconstruct the entire 120-case matrix. Confirm helper-generated manifest includes both current transition verifier and legacy REQUIRED_SOURCES transition closure.
6. Once the independent reviewer actually completes that inspection, validate the real review bytes with `authorization.validate_policy(policy, host_manifest(R), receipt_bytes, review_bytes)`; additionally require parsed review.policy_sha256 == SHA256(exact policy bytes, including newline). This separate hash check is essential: validate_policy itself does not check policy_sha256. Require policy/receipt/current host manifests identical. Packing recovery_byte_equal true, both permanent/trial modes and schema/image sizes/hashes must agree with the already measured preflight.
7. Record a per-profile validation summary with input hashes, full/profile result counts, source snapshot identity, IHX/normalized-symbol identity, safety result including capacity/margin, real review record hash, and `hardware_validated:false`, `physical_device_commands:0`. Any missing, failed, stale, skipped, mixed-image or unknown evidence blocks approval. Check snapshots unchanged at the end.

The custom precommit validator should report all missing evidence explicitly and must not manufacture review records. Hashes establish consistency, not reviewer independence.

## Review record format

Each `ci/profiles/P/program-review.md` must contain exactly one fenced JSON record:

```json
{
  "format": "ak820-ci-program-review-1",
  "status": "passed",
  "hardware_validated": false,
  "policy_sha256": "<SHA256 of final release-policy.json bytes>"
}
```

These are the fields consumed by the production gate. Additional useful fields are profile, IHX SHA256, normalized-symbol SHA256, reviewed source snapshot, linked final review report path/hash and explicit zero-device-command scope. They do not replace the four required fields or actual independent review. Never place a passed placeholder into the tree before completion. The source commit cannot be a required self-referential field inside a policy-bound review; CI's build-attestation binds the final committed source separately.

## Committed admission and actual packaging

After independent review and commit, run `_validate_policy_sources(policy, report)` for all ten from frozen R; it checks actual source bytes against HEAD, including bound safety witnesses. `_require_committed_input` must pass for policy, review, packing receipt and settings catalog. Source commit must be current exact HEAD.

Do not pass canonical external group build paths directly to `build_ci_release.py`: both single/all-profile entry points require builds inside the release repository. Do not solve this with symlinks or changing artifact report paths. For local packaging, copy the complete qualified trees and required original-relative provenance paths into an isolated committed reproduction checkout; preserve report-relative paths, then use a canonical ten-directory layout for `--builds-root`. Verify each report's actual artifacts exist at its original report paths as well. This requires care because the local certified names differ from CI's `.build/ci-profiles/P` layout. A validation-only scratch root is simpler and avoids claiming local package acceptance prematurely.

The supported CI command already preserves original producer paths before assembly:

```bash
python tools/build_ci_release.py --all-profiles --builds-root qmk-8051-ak820/.build/ci-profiles --policies-root ci/profiles --settings-catalog tools/installer/settings-catalog.json --output dist/ci-firmware --toolchain toolchains/sdcc-4.6.0 --source-commit "$GITHUB_SHA"
```

CI admission remains separate: all ten profile jobs and shared regression job must succeed; assembly only downloads successful qualified artifacts, restores both final/bootstrap provenance, rechecks exact committed approvals, measured catalog and bundle identities. Failed/cancelled diagnostic artifacts use separate names and cannot stand in for qualification. Windows/Linux standalone artifact checks, help inventory/checksums, native smoke, final downloads/publication identity remain separate release gates.

## Blocking state

No newly established code defect in this bounded preparation. At inspection, per-profile program-review.md is absent (main checked directly), and full ten-profile final qualification is still reported running. Therefore independent program approval, committed input admission, CI bundle reproduction and publication remain blocked. This plan grants no hardware permission or hardware-validation claim.
