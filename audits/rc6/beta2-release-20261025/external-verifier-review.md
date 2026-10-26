# External beta.2 verifier review

Bounded independent read-only review, 2026-10-26. Scope: the two external verifier scripts and their agreement with the repository production validation contracts and `/tmp/ak820-beta2-final-gates-plan.md`. No source/script modification, compiler invocation, qualification producer, USB command or packaged binary execution was performed by this reviewer. This report is not program approval, release acceptance or downloaded-asset verification.

Reviewed final bytes:

- `/tmp/ak820-beta2-validate-final-evidence.py`: SHA256 `7998ed63e697ab58134f3ba85d074265bd2d977e0f7bc2ff04f4a6c35f88571f`.
- `/tmp/ak820-beta2-verify-public.py`: SHA256 `d75fca36dde4c10af1a71d78cc1f16f0fbbea243cdd760b31dbce3c15ef27654`.

No remaining actionable defect established in these reviewed bytes. This conclusion is limited to static inspection and syntax/refusal checks, not acceptance of absent or still-running evidence.

## Findings resolved during review

1. Public release-manifest membership included its own file, producing unavoidable refusal for the production generator's output. Corrected at `/tmp/ak820-beta2-verify-public.py:88`: the manifest excludes itself, matching `tools/build_beta_release_assets.py:382`.
2. Public release-catalog membership included release-manifest.json even though the descriptor is constructed before that file. Corrected at `/tmp/ak820-beta2-verify-public.py:110` to exclude both descriptor and manifest, matching production construction at lines 375–384.
3. Scratch extraction discarded Linux executable mode bits, so optional CLI smoke always refused at its executable check. Corrected at `/tmp/ak820-beta2-verify-public.py:65` and `:219`: validated regular tar member modes are restored with permission bits masked to 0777.
4. Public catalog and firmware/native packages were independent checksum islands. Corrected at `/tmp/ak820-beta2-verify-public.py:135` through `:183`: exact host identities bind to requested Git commit; actual approval/review and CI bundle authorization are checked; whole profile payloads agree across catalog and bundle; production `validate_profile_links` checks matrix/settings/capability/module and actual image identities. Native package release inputs remain byte-compared against that bundle at lines 201–214.
5. Final-evidence profile command paths named container toolchain locations while only a different host path was pinned. Corrected at `/tmp/ak820-beta2-validate-final-evidence.py:68` through `:96`: actual binaries, report compiler/assembler, qualification tool paths/hashes and profile compiler identity bind to the producer's explicit read-only Docker mount. `/tmp/ak820-beta2-streams-build-qualify.py:9` independently confirms that mapping; requiring the container mount to exist on the host would be incorrect.

## Inspected contracts and limits

The final-evidence validator calls production qualification, exact profile command/log/source validation, committed policy-source closure including LUFA lock, safety witness validation on ordinary scratch copies, policy authorization and exact policy-byte review hash checks. Scratch witness/source paths use production safe_path; report bytes are not rewritten or substituted with symlinks. Input hashes and source snapshots are revisited at the end. In precommit mode both committed inputs and real review records are explicitly deferred and per-profile/global `passed` stay false. It does not manufacture independent approval.

The public verifier rejects missing required inputs, checksum disagreement, archive traversal and link members, and compares bilingual guide closure to current source. Packaged smoke commands are exclusively `--help`, `verify` and profile-selected `verify`. The current source CLI resolves approved release context and handles verify before `hid_module()` in `tools/installer/ak820.py:904`–`:933`. This establishes intended command scope; no assertion is made about executing downloaded binaries, Windows behavior, physical device behavior or publisher authentication.

Both final scripts parsed successfully using Python AST with bytecode disabled. Missing public assets were refused with exit 1 and `FAIL: assets directory is missing`. Full final-evidence validation and public positive-asset validation were not run in this review. Ten-profile qualification, real independent program approval, committed admission, CI/package reproduction and publication remain separate gates.
