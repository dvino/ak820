Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-23. The keyboard still runs the earlier SDCC 4.4 RC6 candidate.
The SDCC 4.6 image has not been installed. The owner rejected snapshot-only
updating: finish the general settings-preserving updater first.

## Source and build

Only ajazz/ak820:vial is supported. Foreign boards, unused platforms, the old
desktop app, native research tools and previous releases were removed after
external backup. SDCC and LUFA are pinned external dependencies.
See [Build](BUILD.md) for setup on another computer.

The production builder defaults to SDCC 4.6.0; 4.4.0 remains an explicit control.
Fresh build: qmk-8051-ak820/.build/source-trim-production-sdcc46-20261023/.
CODE: 38,100 bytes (36,292 main, 1,808 low); XRAM: 2,067; linker stack capacity:
157 bytes. Free CODE: 2,405 bytes across two windows. The map also counts five
reserved HOME addresses absent from IHX.
IHX SHA256: f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e.
It is byte-for-byte identical to the reviewed pre-cleanup image.
All 465 inputs and 76 artifacts were independently checked.

Active source-installer bundle: releases/rc6.
Manifest SHA256: f181619c824bd93778bffe0e842d15bb0917ed5af15f65bd294ec4c461773402.
Source installer verify passes. This is not hardware approval.
[Exact build review](../audits/rc6/source-trim-release-review-20261023.md).

The Windows package remains dist/AK820-sdcc46-breathing-20261023.zip,
SHA256 a80338dafdc06f39534db53d4cf23eecdfa18383883549248fdea8f769035fa6.
It contains the earlier reviewed host tools and has not been rebuilt after
the packaging changes. No push or public download was made.

## Validation and device

The identical earlier image passed 19 host/CPU suites and focused CPU checks.
The general SDCC Boolean near-pointer fixture still fails two of sixteen
cases on both compilers; no affected shape was found in reviewed retained
paths. A compiler backport remains conditional future work.

After cleanup, seven Windows offline suites passed. Dependency fixtures
passed seven LUFA and eight SDCC tests; version selection passed three tests
and packaging passed twelve. The new production host/CPU run is not yet
complete. Its intermediate failures are not passes.

Latest read-only capture: host/runs/20261023-sdcc46-before-console-update/.
All 65,536 bytes were saved; installed CODE matches the known 4.4 image.
NVM/journal repeat reads match, journal header is empty and FD01 reports no
storage fault or dirty/batched write. Pending RGB RAM is not covered.
No loader entry, erase or flash was sent during this work.
Earlier authorized round trips covered six keys, twelve encoder slots and
RGB RAM; all 10,240 durable bytes matched afterward. Macro upload, durable
RGB save and power-cycle persistence remain untested. The owner reports
normal reactive lighting.

## Remaining work

The general updater needs firmware support to freeze settings, save pending
RGB state, export the declared state and stop loader entry on storage failure.
The installed legacy source lacks this capability; the first transition is
unresolved. A bridge alone does not solve it.
[Implementation plan](../audits/rc6/general-update-implementation-plan-20261023.md).

Direct Control remains research-only and requires permission before removal.
Further optimizations, indicators and the Windows helper stay in
[Roadmap](ROADMAP.md). Final tree review, clean history commit and later
merge/push remain pending.
