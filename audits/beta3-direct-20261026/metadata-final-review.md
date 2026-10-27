# Metadata review, 2026-10-26

## Result

The bounded parser and measurement-path changes pass independent review. No
blocking defect was found in the four reviewed files. This result covers host
metadata and local negative controls. It does not approve firmware release,
physical display behavior, device writes or installation.

The review did not author the implementation. The reviewed SHA256 values are:

| File | SHA256 |
| --- | --- |
| `tools/build_capability_catalog.py` | `6e28dbb11bacfdaa491a23cef60c03341261508fe8549569dbd6c2b37e6a3e3b` |
| `tools/test_build_capability_catalog.py` | `098dea8db3b1fca9ac6d450d03d20590a5e9f777fc8a688de60e812f5db41286` |
| `audits/beta3-direct-20261026/measure_origin.py` | `e8e366c04d7bd27dde984489aafa2bd31cd6091c9110d3d627571abb40c71bca` |
| `audits/beta3-direct-20261026/test_measure_origin.py` | `6f1a9ea687840af5c90b1b805ed3ea9cf13ca9b52caacf062c183ab0d38e2413` |

## Parser and source binding

The actual main map at
`qmk-8051-ak820/.build/beta3-qualified/main/ajazz_ak820_vial.map`
has SHA256 `18d1277c5330f9770045e185327be15ce817a9d18e81f9db6542a8fe2c76d637`.
It records `_ak820_direct_tick` at `C:0000B6B0`,
`_ak820_direct_cancel` at `C:00002EF2`, `_ak820_direct_stage` at
`D:00000DDF` and `_ak820_direct_state` at `D:00000ED5`.
The fixture reproduces these records and includes the XSEG origin `0x440`.
The D addresses are absolute; adding the XSEG origin would reject valid RAM.

The new parser requires one well-formed record for each exact symbol and the
expected address space. Missing, duplicate, malformed and swapped records fail.
Functions must fall inside the existing application CODE windows. The complete
246-byte stage and one-byte state must fit inside `[0x440, 0x1000)` without
overlap. Tests cover the last valid stage start `0xF0A`, the first invalid start
`0xF0B`, both CODE-window boundaries and a valid last RAM byte `0xFFF`.

Direct availability still requires a unique compiled-source record whose hash
matches each current `quantum/vialrgb.c` and `quantum/vialrgb.h` file. Existing
full build inspection remains in `inspect_entry` before the contract is used.
The returned contract retains runtime negotiation and explicitly leaves
physical display verification false. Profiles without Direct return an explicit
unavailable value. This change agrees with the observed map format and does
not weaken the source-hash or symbol-bound requirements.

## Measurement paths

Resolving the output directory before launching the child process prevents a
relative output path from changing meaning when the child uses the original
root as its working directory. Resolving the mapped original toolchain follows
the shared toolchain symlink, matching the canonical qualifier's recorded
absolute path. Source equality, complete build-tree equality, Python identity,
native-reference stability and post-measurement equality remain required.
The code still uses the canonical matrix tool and rejects its failed exit.

Commands repeated during this review:

```text
python -B -m unittest discover -s tools -p test_build_capability_catalog.py
Ran 19 tests: OK
python -B -m unittest discover -s audits/beta3-direct-20261026 -p test_measure_origin.py
Ran 2 tests: OK
```

The measurement file contains two test methods. Its source/build rejection
method executes two subcases. The review does not claim four helper methods or
a new successful original-root measurement. The path assertions exercise an
absolute output fixture and a shared toolchain symlink; successful canonical
measurement remains an integration requirement.

## Qualification execution boundary

Run qualification sequentially in the consolidated source root. Although no
firmware rebuild is planned, `qualify()` runs host compilation and SDCC test
compilation through its regression suites. AGENTS.md prohibits simultaneous
builds sharing a working tree or output paths. Sequential execution avoids an
exception to that rule and does not require changing any validator.

The inspected output routing is otherwise suitable for distinct profiles:

- Configuration and qualification JSON, runtime-stack JSON/log, runtime-safety
  reports and profile-tests all reside below the selected profile build.
- `test_keyboard.py` creates a unique log directory below the qualification
  output's parent and passes its child paths to linked CPU suites.
- Host harnesses use unique `TemporaryDirectory` directories for generated C
  and binaries. Short-call assembler/linker tests and real SDCC dependency
  tests also use private temporary trees. Linked simulators receive explicit
  profile-specific output directories.
- Normal Python imports may update shared `__pycache__` files. Source hashes
  exclude these files. The pinned compiler and simulator installation is read
  as shared tooling; no installation mutation was found in these paths.

No fixed shared host binary or CPU-result path was found in the inspected
qualification plan. This is a static assessment, not a parallel stress test.

Do not hardlink mutable retained evidence into the consolidated root. The
qualifier overwrites `configuration-report.json`, `qualification.json`,
`runtime-stack.json`, runtime logs and runtime-safety files. A hardlink would
also alter the file retained at the former root, even when the two profile
paths differ. `run_profile_tests()` removes and recreates its output directory,
but that does not protect the other in-place report writes. Copy build trees,
or hardlink only immutable build inputs and give every regenerated report its
own inode. Check image/map hashes before and after canonical qualification.

Only regenerate evidence through the canonical tools. Saved command and CWD
validation must remain strict; no report-path editing or manual evidence
substitution is supported by this review. Discovery of the saved alpha2 ROM
permits the separate strict preparation/admission work to proceed, but that
work was not executed or approved here. No device operation was performed.
