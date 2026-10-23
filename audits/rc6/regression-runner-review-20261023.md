# Regression runner review

Independent precommit review, 2026-10-23: PASS. The reviewer did not author
`tools/test_keyboard.py`, its tests, or the corresponding EN/RU instructions.
Nine targeted orchestration regressions passed independently, with no skips.

The review checked explicit/default compiler selection, child environment
propagation, required-tool failures, visible unit skips, saved launch failures,
fresh CPU output directories, and initial/per-suite/final image hashes. A
transient image replacement remains a failure even if restored before the end.

## Findings closed

The Russian status still said no firmware rebuild had occurred and presented
the earlier missing-tool skips as current. It now identifies the earlier run
and records the fresh control build. The packaging audit referred to JSON
below itself; it now links to the actual release review record.

The reviewer independently checked all nineteen host bindings, all nine
release-file hashes, the unchanged eight non-review release files and the
approval hash `2556d1e53017e6977762ca421bc45c6086dc864ee18fec689d6eafef264cef53`.
Only the Windows builder changed within the bound host set. Source installer
`verify` passed without importing HID or opening USB. The public-document
check passed 31 documents with no failures.

## Integration evidence and limits

The first twenty-suite control run had eighteen passes and two failures. The
device test stopped at the intentionally stale Windows-builder binding. The
RGB host check could not run LeakSanitizer under the restricted process view.
After independent builder review and binding refresh, the device suite passed
all nineteen tests. With `ASAN_OPTIONS=detect_leaks=0`, the RGB host suite
passed breathing/reactive cases and all 16,777,216 compact-HSV cases. Those
reruns were reported by integration, not independently repeated by this reviewer.
Address and undefined-behavior checks stayed enabled; leak checking was excluded.
The first combined report remains a failed historical attempt, not an all-pass
qualification. Later complete results must identify their own report and image.

No Windows binary build, native GUI interaction, live keyboard operation or
power-loss test is established by this source review. The separate firmware
pointer and linked-inventory changes are outside this approval.
