# Isolated-origin assembly toolchain

The qualification matrix and capability checks continue to use `--toolchain`,
resolved exactly as before, including an origin symlink to the shared pinned
toolchain. Isolated origins can pass `--assembly-toolchain` with a repository-
local, regular-file copy of that toolchain. Only the existing
`ci.assemble` call uses this optional path.

Before assembly, each worker checks that the proof and assembly toolchain
trees contain the same relative file names and SHA256 hashes. Symlinks inside
either resolved toolchain tree and unsupported entries are rejected. The
assembly path must also be inside the worker repository with no symlink in its
path; the original proof path keeps its prior symlink resolution behavior.
The inventories are checked again after assembly and included in worker
metadata. This keeps the original qualification command binding intact while
allowing a self-contained toolchain inside an isolated worker root.

Worker failures retain their exit status. Captured child output remains in the
aggregate report log and is also written to the outer process' standard error,
so a failed temporary staging directory does not hide the diagnostic.

Focused verification: `python3 audits/beta3-direct-20261026/test_assemble_origins.py -v`
passes 12 offline boundary tests. The tests cover distinct matching proof and
assembly paths, changed toolchain content, symlink and external-path rejection,
and preservation of failed-worker diagnostics. No qualification, build,
release assembly or device operation was run for this change.
