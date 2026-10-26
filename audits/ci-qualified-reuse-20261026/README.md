# Reuse completed firmware qualification

An optional `qualified_run_id` input on manual workflow dispatch reuses the ten
qualified profile archives from a completed run of the same workflow and
repository. The dispatch must select a version tag. An empty input retains the
full qualification path; pushes and pull requests also retain that path.

Before download, the workflow checks the latest successful qualification job for
each of the ten profiles, the exact ten nonexpired archive names, the source SHA
and its ancestry. Source changes may affect this workflow, Markdown guides,
release notes, audits and the four authorization files for each known profile.
Other changes reject reuse. Current shared checks still run. Assembly still
checks current source, compiler/runtime evidence, policies and packing receipts.
The existing release trigger source and main ancestry checks remain in place.

`validate-qualified-reuse.py` is a byte-for-byte copy of the inline validator.
`check-contract.py` checks that identity, adversarial fixtures and saved public
GitHub metadata. `run.json`, `jobs.json`, `artifacts.json` and `workflow.json` were
read from GitHub on 2026-10-26 for run `40258163824`. Its overall assembly failed;
all ten latest profile qualification jobs succeeded. Overall run success is not
required because current assembly must run again.

Local evidence:

- `python audits/ci-qualified-reuse-20261026/check-contract.py`: nine checks passed.
- `actionlint .github/workflows/windows-installer.yml`: passed (empty log).
- `source-replay.json`: source `cd36cf446c1bae8070ee8f61750df550ea53230d`
  is an ancestor of checkout `31ab52c`; every committed changed path is allowed.
- `git diff --check`: passed.

These checks cover the reuse contract and metadata, not a dispatched reuse run,
package publication or device behavior. No CI run, release or USB operation was
started for this change. Independent review is required before commit.
