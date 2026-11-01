# Beta.5 evidence preparation review, 2026-11-01

CI run [41297661542](https://github.com/dvino/ak820/actions/runs/41297661542)
qualified ten profiles offline but failed release assembly because the safety
witness configuration did not match the built images. This is not a physical
keyboard test or a release approval.

The opt-in evidence workflow writes to fresh directories. It requires a
trusted, isolated workspace without concurrent readers or writers. Draft
outputs are disposable and unapproved. Policy outputs are staged, not installed;
ROM and bundle source fixtures must be converted to validated backups before
policy staging. Independent validation and review of the complete final tree
remain necessary before release assembly.

Independent reviews on 2026-11-01:

- Documentation corrections: reviewer approved the README and STATUS changes;
  a separate reviewer approved the corrected candidate release notes.
- Transition action coverage: reviewer approved the consumer checks and
  synthetic tests for all current-profile pairs.
- Evidence producer: reviewer approved the opt-in workflow with the isolation
  and final-tree conditions above. Earlier findings on output paths, source and
  interpreter binding, frozen input validation, staged policy integration and
  draft failure isolation were addressed or constrained and retested.
- Integration design: reviewer accepted an isolated, offline worktree and a
  validated commit as the consumer boundary, provided no consumer can read the
  intermediate tree and all final evidence and reviews are checked again.

The focused synthetic suites passed: 15 evidence-output tests, 2 path tests,
39 release-safety tests and 17 transition-policy tests. These do not qualify
firmware. Review output remains in the session's retained subagent artifacts;
final-image evidence and reviews have not yet been produced.

GitHub release metadata for `v0.6.0-beta.4.1` identifies the catalog ZIP by
SHA256 `064ead1c4f5ec0aebdaa318b5a406e7caec9f597495b33c0d3f10dbccc859e9e`
and firmware bundle by
`fa18b3aa28fd9f805bfc99711f67dcf25dd85835a77982eed8d2d92c4f1e41ce`.
Both match the retained local archives. This verifies consistency with the
published assets, not the physical provenance of the OEM references or a
physical restore.
