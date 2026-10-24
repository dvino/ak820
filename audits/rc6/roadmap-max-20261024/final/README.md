# Development profile qualification

All eight profiles passed complete offline regression qualification from source
`81cfc9609f10cfd5161b5fb128af5c8b5f5e0ad0` on 2026-10-24. The source was clean
and unchanged during each run. Builds ran sequentially within each of three
independent worktrees using the pinned SDCC 4.6.0 compiler and C52 simulator.
No device was opened. No profile is approved for release or installation.

The final images reproduce every preliminary IHX hash and resource measurement.
MAP and build-report hashes differ between execution directories because those
reports embed paths; each final qualification binds its own exact files.
[Machine matrix](matrix.json) records the final image, source, tool and test
identities. [SHA256SUMS](SHA256SUMS) covers every retained file in this directory.

## Exact linked resource use

| Profile | CODE | Main trailing free | Low trailing free | XRAM | Static IRAM | Allocated stack |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `standard` | 39,115 | 1,301 | 84 | 2,612 | 96 | 160 |
| `nkro` | 39,259 | 1,157 | 84 | 2,617 | 97 | 159 |
| `one-shot` | 39,765 | 719 | 16 | 2,622 | 96 | 160 |
| `nkro-one-shot` | 39,909 | 575 | 16 | 2,627 | 97 | 159 |
| `space-cadet` | 39,225 | 1,191 | 84 | 2,615 | 93 | 163 |
| `nkro-space-cadet` | 39,369 | 1,047 | 84 | 2,620 | 94 | 162 |
| `one-shot-space-cadet` | 39,874 | 610 | 16 | 2,625 | 93 | 163 |
| `full` | 40,018 | 466 | 16 | 2,630 | 94 | 162 |

All sizes are bytes. The CODE windows remain `0x28a0..0x2fff` and
`0x3027..0xc6ff`. Trailing free space is measured separately in each window;
alignment holes are not reported as trailing space. Ordinary XRAM remains
`0x0400..0x0fff`, with the fixed LED DMA reservation at `0x0200..0x03ff`.

Allocated stack capacity describes placement, not maximum runtime usage.
No profile has a qualified whole-program bound, exact-image interrupt/nesting
proof or approved installer transition. Same NVM schema is insufficient to
make a different image compatible with release settings restoration.

The standard profile uses 699 fewer CODE bytes than the starting `48ce5fa`
development image (39,814), and 1,198 fewer than published alpha.2 (40,313).
The full profile includes all three new optional features and remains 295
CODE bytes smaller than alpha.2. Its low window has only 16 trailing bytes.
These are complete-image comparisons; individual optimization costs are
nonadditive.

## Completed checks

Every profile passed 28 base suites and 270 unit tests with zero skips. Across
eight profiles, that is **224 base suite executions and 2,160 base unit-test
executions**. The selected features add **58 supplemental suite executions**.
These are repeated per-profile runs, not a count of unique test implementations.

Each profile's common supplements include 18 configurator gates, 13 outliner
unit tests, 17 stack-analyzer unit tests, exact outline integrity and 987 linked
VialRGB cases. NKRO and One Shot add their host and linked-CPU suites. Space
Cadet adds its host negative controls or joins the One Shot host suite; the base
tapping CPU runner detects the exact profile and includes its Space Cadet cases.
The combined profile also checks NKRO cancellation of pending, held and consuming
One Shot state, and pending/held Space Cadet actions.

| Profile | Base suites | Supplemental suites |
| --- | ---: | ---: |
| `standard` | 28 | 5 |
| `nkro` | 28 | 7 |
| `one-shot` | 28 | 7 |
| `nkro-one-shot` | 28 | 9 |
| `space-cadet` | 28 | 6 |
| `nkro-space-cadet` | 28 | 8 |
| `one-shot-space-cadet` | 28 | 7 |
| `full` | 28 | 9 |

The full profile passes 79 linked tapping/input cases, 15 One Shot cases and
seven NKRO cases. All profile gate reports bind source files, exact commands,
logs and before/after image identities. Repeated commands cannot replace a
missing suite. Compiler flags also bind inline Space Cadet to its declared
profile, independently of standalone handler symbols.

The full image's actual `package` invocation stops with the expected release
blockers; [guard result](package-guard.json). A successful offline qualification
does not bypass packaging restrictions.

## Runtime stack and physical limits

Each exact image has a runtime stack diagnostic, with the analyzer, instruction
decoder, MAP and relocated listings bound by hashes. All eight diagnostics
return status 2: `_main` and `_ak820_led_irq` remain unresolved. Timer and USB
callback bounds are two and six bytes, excluding hardware/OEM entry and any
nested-interrupt allowance. The analyzer explicitly records
`whole_program_qualified: false`.

No global stack allowance, exact-image interrupt/nesting proof, physical timing,
USB controller behavior, DMA behavior, flash persistence, power-loss behavior,
or installer transition is approved by these tests. The application IHX files
are development outputs, not complete flashable ROMs or installation packages.

## Environment failure retained

The first isolated runs for standard, NKRO and Space Cadet failed only in the
RGB host runner when LeakSanitizer could not read the process task directory
under `/proc`. Each failed report records the failure; none counts as a pass.
The other 27 base suites passed, with 270 unit tests and no skips.

The same RGB runner passed outside that process isolation with ASan, UBSan and
LeakSanitizer unchanged. Every final profile was then rebuilt in a fresh
`final2-*` directory and ran the complete unmodified qualification in that
execution environment. No sanitizer, assertion, feature or release gate was
disabled. [Failure evidence](environment-failure/summary.json) retains the three
original reports and compressed failing logs.

## Retained files and reproduction

Each profile directory includes the application IHX, MAP and MEM, build and
configuration reports, the complete base qualification, supplemental results,
outline/reachability manifests, compiler flags and runtime diagnostic. Logs are
stored as gzip-compressed verbatim bytes. Each `files.json` records both original
and stored SHA256 and size; original paths in reports identify the execution
location. The archive does not include generated object trees, simulator command
scripts or temporary simulated ROM fixtures. Those are regenerated by the checked
runners; retained logs and reports are evidence of the completed executions.

From this directory, verify the retained data with:

```sh
sha256sum -c SHA256SUMS
```

To reproduce a complete profile, follow [Build](../../../../docs/BUILD.md) to
prepare the pinned tools, then run from the repository root:

```sh
python tools/configure_firmware.py build --profile full \
  --build-dir qmk-8051-ak820/.build/recheck-full \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

Use a fresh directory for each of the eight named profiles. Host sanitizer
checks need an environment where their process-introspection facilities work;
a sanitizer startup failure remains a failed run and must not be hidden.

## Related evidence and review

- [Packing change and 3,104 CPU state comparisons](../packing.md).
- [Protocol representation and request comparisons](../protocol-size.md).
- [Compact Space Cadet behavior and interaction tests](../space-cadet.md).
- [Exact-image stack analysis and unresolved roots](../../runtime-stack-20261024/report.md).
- [Deferred feature build probes](../feature-probes.md).
- [QMK Settings storage and migration proposal](../qmk-settings-plan.md).
- [Independent final acceptance](../final-acceptance.md).

The published and installed firmware remains v0.6.0-alpha.2. This work neither
publishes nor installs a new release.
