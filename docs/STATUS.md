Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-23. SDCC 4.6 RC6 is installed. Physical typing was confirmed separately.
The approved as-is console flash used package defaults. Previous settings
were saved locally and were not restored.

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
and packaging passed twelve. The production host/CPU run finished with 17 suites passing initially; two
invocation failures were closed by separate Linux reruns (19 device-adapter
and 75 package tests). The original failed report remains unchanged.

Installed evidence: host/runs/20261023-as-is-flash/. Payload SHA256:
a1b8beec9a2a675c955bac946339e31f1823e17cdfb60f4755796e550530c711.
Full ROM SHA256: 56b2de776924c48bda6d08a2604edc8ab94f24e5ec7365f7b584c0fe7dd70fc5.
One loader command sequence 1,2,3,4,5 completed. Full CODE, manifest, protected
regions, initial NVM and clean storage/journal were verified after restart.
Physical typing was confirmed separately.

Read-only post-install suite passed: 498 key assignments, 12 encoder slots,
16 macros with an 8192-byte view and 82 LED descriptors. Evidence:
host/runs/20261023-sdcc46-installed-readonly/report.json. No settings writes
were requested. Macro upload, durable RGB save, physical encoder/lighting
behavior and power-cycle persistence were not tested on this image.

## Remaining work

The firmware preservation protocol was cancelled. Its uncommitted code
was archived outside the repository and removed. Local export and restoration
will use existing Vial commands in one shared GUI/CLI installer module.
Implementation is deferred; no freeze, token or import record is added to firmware.
[Implementation plan](../audits/rc6/general-update-implementation-plan-20261023.md).

Direct Control remains research-only and requires permission before removal.
Further optimizations, indicators and the Windows helper stay in
[Roadmap](ROADMAP.md). The tree passed independent review and the clean source commit is c1779a8a.
Old local ancestry was archived and removed; Git pack size is 1.84 MiB.
Merge/push remain pending. See [cleanup result](../audits/rc6/clean-history-result-20261023.md).
