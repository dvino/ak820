# Report pointers and short-call rebuilds

These are development checks against baseline `348b45e`. No device commands
were sent. The published alpha.3 image and release policy are unchanged.
Exact image identities, resource reports and the initial failure are retained
in [probes.json](probes.json) and its `probes/` files.

## Report pointer ABI

AK820 SDCC report helpers now accept XDATA pointers in both declarations and
definitions. Their retained callers pass `actual_keyboard_report`, which is
allocated in XDATA. The previous helpers already narrowed their generic
pointers internally. Moving that same memory-space contract to the call
boundary removes redundant pointer tags. Host builds and other targets retain
their previous types; mouse reports are unchanged.

| Full profile | Baseline | Report ABI candidate |
| --- | ---: | ---: |
| CODE | 38,924 | 38,890 |
| XRAM | 2,607 | 2,600 |
| Stack bound / capacity | 160 / 166 | 160 / 166 |

The exact-image runtime gate passed before regression tests. The initial base
run passed 27 of 28 suites. RGB host testing stopped because LeakSanitizer
could not read sandboxed `/proc` task information. The unchanged RGB suite
passed outside that restriction with AddressSanitizer, UBSan and LeakSanitizer
enabled. A supplementary run with leak checking disabled is excluded from
acceptance evidence. The integrated matrix repeats the complete suite with
the normal sanitizer configuration and no external sanitizer overrides.

The independent reviewer checked all ten declarations and definitions, the
retained call sites, helper-to-helper NKRO dispatch and the linked SDCC
parameter layout. No source correctness finding remained.

## Short-call rebuild

The diagnostic linker recreated empty original listing directories after the
post-outline tree had been renamed. `write_tree` treated those empty
directories as stale output and rejected an otherwise fresh build.

The copy step now accepts a tree containing only real directories. Existing
files, root or nested symlinks, and special objects still stop it. It deletes
nothing and copies only ASM and JSON from the immutable source. Eighteen
short-call unit tests pass, including preservation of rejected output and
exclusion of stale listings. Independent review found no remaining blocker.

The corrected `full-auto-shift-dynamic-macro --short-calls` build passes its
runtime gate, all 28 base suites with 273 unit tests and no skips, and all 24
supplemental suites. The normal sanitizer configuration is retained. Its IHX is byte-identical to
the prior qualified image:

`de8fa10d00cf2844fca89846639ddd1745f95b7542b957c1520c9fa99f6e7233`

## Rejected experiment

Narrowing `process_record_handler` at its call boundary was also measured. It
saved one XRAM byte but added 24 CODE bytes and raised the stack bound from
160 to 163 bytes relative to the report-only candidate. That change is not
included. Its build and runtime records are retained; remaining regression
tests were stopped after the unfavorable measurement.

## References

The independent package review also checked the English/Russian status notes
and every retained probe file's SHA256 and byte count. The original RGB
failure, unrestricted rerun and fully passing short-call rebuild agree with
the report. No finding remains open for this bounded package.

- [SDCC Compiler User Guide](https://sdcc.sourceforge.net/doc/sdccman.pdf),
  section on pointers to MCS-51 named address spaces.
- [Runtime stack check](../../../docs/RUNTIME-STACK.md) for proof scope.
