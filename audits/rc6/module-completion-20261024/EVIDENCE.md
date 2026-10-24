# Retaining one build

`retain_evidence.py` retains one image. Matrix coverage and record hashes must be
checked by the matrix coordinator; this tool makes no profile-count claim.

Run from the repository root after freezing a clean source commit. Supply the
full commit ID and a new external output directory:

```sh
python audits/rc6/module-completion-20261024/retain_evidence.py retain \
  --root . --source-commit COMMIT \
  --build-dir qmk-8051-ak820/.build/BUILD --toolchain /path/to/toolchain \
  --command-log /path/to/build.log --command-log /path/to/runtime.log \
  --final-dir /path/to/evidence/VARIANT
```

The build must already contain `configuration-report.json` and completed runtime
proofs. Existing reports and logs are copied byte for byte. Runtime-only mode
requires `offline_tests_passed: false`. The archive contains every build-report
artifact, generated source, foreground listing, runtime-safety file and the
configuration report, under the original `.build/...` prefix.

Add `--full` for a fully qualified build. This mode first runs the configuration,
base-suite, profile-suite and catalog validators, then retains every regular file
in the build directory, including qualification logs and linked profile results.
Symlinks and escaping archive paths are rejected. No build or test is executed.

Verify either mode without the original build directory or toolchain:

```sh
python audits/rc6/module-completion-20261024/retain_evidence.py verify \
  --root . --source-commit COMMIT --final-dir /path/to/evidence/VARIANT
```

Verification needs the frozen commit in Git and matching current compiler-input,
checker and test sources. It checks archive/file hashes, image and source
identities, generated sources, pinned LUFA inputs, linked memory placement and
the combined foreground/startup/interrupt contract. Full mode also checks base
suite identities, raw log hashes and counts, profile invocation plans, profile
log hashes and test-source identity. Original invocation paths are reconstructed
in memory; original report bytes are never rewritten. The catalog entry is
independently inspected before retention and its image/resource binding is
checked afterward. Portable verification does not rerun CPU suites or reproduce
the catalog inspection against a relocated build tree.

`build_source` and `qualification_source` preserve the reports' original source
metadata, including absent metadata or precommit/dirty descriptions. A manifest
match to the supplied frozen commit is recorded by successful verification; it
does not change those descriptions. Offline evidence does not establish physical
behavior, installed firmware, release approval or permission to write to a device.
