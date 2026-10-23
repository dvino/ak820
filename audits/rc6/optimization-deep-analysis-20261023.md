# What is optimized and what to try next

Date: 2026-10-23. This report combines current build evidence, source inspection
and external research. It does not authorize a device write or feature removal.
The current priority is qualification and release of the existing fixes on
SDCC 4.6. Remaining optimizations are future work; Direct stays research only
and the general settings-preserving updater is unfinished. Six layers,
sixteen macros and supported behavior remain the comparison contract.

## Reference result on SDCC 4.4.0

The current complete SDCC 4.4.0 build is
`qmk-8051-ak820/.build/rc6-optimization-batch-20261023`.
Its IHX SHA256 is
`4b68ae92d95538e4c0af1d445c723645b1d7f570b3ea206002d7521b45fe7ce3`.
It uses 39,144 CODE bytes and 2,067 XRAM bytes. The main CODE window has
1,332 bytes free and the lower window has 29: 1,361 total. Reported stack
capacity is 152 bytes, not a measured worst-case stack bound.

All 465 source/toolchain records and 76 artifact records matched after the
build. Independent review of source, artifacts, documentation and offline
checks passed. The installed candidate remains unchanged. Detailed commands,
test limits and the two package-test skips are in
[the combined build report](optimization-batch-20261023.md) and
[its independent review](optimization-batch-review-20261023.md).

The owner subsequently selected testing and release preparation of these
current fixes on 4.6. Further optimization implementation is deferred; the
remaining candidates in this report are future work.

## What is already paid for

| Change | Evidence and cost | Meaning for further work |
| --- | --- | --- |
| Feature configuration | Console, command, mouse keys, Magic, Space Cadet, tapping, One Shot and several other features are disabled in the current target. Layer state is already eight bits; only two compiled default layers back six writable layers. | Repeating these recommendations cannot produce a new saving. Removing supported media keys, NKRO, Repeat, Caps Word, Grave Escape, Tri Layer or RGB changes the product contract. |
| Dead-function removal | Current reachability report: 576 functions, 399 retained, 177 removed across 64 modules. Packer/IRQ/startup and address-taken callbacks remain roots. | This is already part of every controlled build. A zero ordinary call count does not make a callback or OEM entry removable. |
| Repeated-code outlining | 32 helpers at 221 sites; the existing report records 1,234 nominal bytes removed and two additional stack bytes at outlined calls. | This is baseline behavior. The nominal count is not a fresh linked saving; rerunning the existing pass found no new default-threshold groups. |
| Compact CIE table | Earlier matched control: 216 fewer linked CODE bytes than the full table, with an existing color-error trade. | Already included; cannot count the 216 bytes again. Masking HSV values without changing storage saves nothing. |
| Typed private host-driver pointer | Separate controlled link: 49 fewer CODE bytes and one fewer XRAM byte; public pointer/callback ABI preserved. | A useful example for other private, proven address spaces. It does not justify global casts of public pointers. |
| Shared system/consumer report tail | Separate controlled link: 30 fewer CODE bytes; independent last-usage state, null handling and callback ABI retained. | Search for other repeated emitted work, but account for argument setup and helper overhead. |
| Breathing arithmetic | Separate controlled link: 42 fewer CODE bytes, identical interpolation output for all 256 helper inputs. Compact-table product is at most 252. | More narrow arithmetic requires a similarly proved input range. This is not permission to narrow arbitrary timers or lengths. |
| RGB action table | Separate controlled link: 216 fewer CODE bytes and four fewer XRAM bytes. Host comparison covers 2,097,152 events. Linked CPU comparison passes. Tested foreground stack rises by two bytes. | Tables can beat repeated dispatch code here, but table bytes, CODE-pointer loads, indirect-call ABI and DCE roots must all be charged. |

The last three changes together save **288 CODE bytes** against the previous
39,432-byte build with smoother Breathing. The current image is **203 bytes
smaller than the installed 39,347-byte candidate**, while adding that curve.
Those are measured whole-image differences. The table's separate deltas use
different controls and are not an independent additive size certificate.

The compact Breathing curve is a behavior improvement, not a pure saving.
It keeps the existing 32-entry table and interpolates once per frame. Host
tests find 69 brightness levels instead of 20 and maximum adjacent phase step
two instead of eight. The linked CPU checks cover 161 helper inputs and
50 complete frames. Physical smoothness and hardware timing remain untested.

## What the external search changes

The reading was checked against this MCS51 target and the pinned source,
rather than treating any 8051 or QMK benchmark as our result.

| Primary source checked | Useful finding | Application here |
| --- | --- | --- |
| [QMK size guide](https://raw.githubusercontent.com/qmk/qmk_firmware/master/docs/squeezing_avr.md) | Its main levers are AVR LTO, disabling features, narrower layer state and fewer effects. | The guide is explicitly for AVR. Most applicable feature switches are already set here; GCC LTO and AVR printf figures are not SDCC measurements. No supported feature is silently removed. |
| [QMK 8051 port](https://github.com/vuhuycan/qmk-8051/tree/sdcc_mcs51_ch55x) and [its lto.sh](https://raw.githubusercontent.com/vuhuycan/qmk-8051/sdcc_mcs51_ch55x/lto.sh) | Its named LTO script invokes dead-code removal and reuses generated ASM. | The current builder already has a target-specific DCE pass. This is not a second unclaimed whole-program optimizer. The port's CH555 figures do not prove VS11K28A size, timing or hardware compatibility. |
| [Current upstream dynamic keymap](https://raw.githubusercontent.com/qmk/qmk_firmware/master/quantum/dynamic_keymap.c) | Modern upstream separates NVM operations and shares macro playback through the send-string interface. | A design comparison for common work, not a drop-in replacement: it uses different NVM APIs and 32-bit macro offsets. A wholesale import could add abstraction and pointer costs to our bounded 8-KiB stream. |
| [SDCC author comparison](https://sourceforge.net/p/sdcc/mailman/message/36359926/) | Pointer-space and library design affect code-size comparisons between compilers. | Supports inspecting actual accesses and helper calls. It provides no percentage saving for this firmware and does not justify moving constants into scarce RAM. |
| [SDCC memory-model discussion](https://sourceforge.net/p/sdcc/mailman/sdcc-user/thread/BLU0-SMTP43391B34E9896F2E2E0040E8E40%40phx.gbl/) | The maintainer corrects a claim that medium model supplies compressed two-byte generic pointers. | Reject that proposed automatic saving. A model change also changes allocation/ABI assumptions; it is not a local optimization switch. |
| [SDCC builtin implementation notes](https://sourceforge.net/p/sdcc/wiki/Builtins/) | The illustrated specialized memcpy builtins belong to a target's builtin table; the example is DS390. | Do not assume DS390 dual-DPTR or copy builtins exist for this MCS51 variant. Typed local loops remain candidates only after a linked comparison. |
| [Contiki banking design](https://github.com/contiki-os/contiki/wiki/8051-Code-Banking) | Banking requires hardware mapping and trampolines, adding call and stack costs. | Background only: no compatible bank-switch hardware or extra safe executable region has been proved here. It does not create free CODE inside our fixed windows. |
| [SDCC code-size regression discussion](https://sourceforge.net/p/sdcc/discussion/1865/thread/9589cc8d57/) | Newer compiler versions can grow MCS51 output, even when other backends improve. | Compare a complete linked image and execution before adopting a release. The release number itself is not a saving. |
| [Accepted bool-store fix, patch 513](https://sourceforge.net/p/sdcc/patches/513/) and [bug 3845](https://sourceforge.net/p/sdcc/bugs/3845/) | A comparison held in carry can be stored incorrectly through a pointer; the fix was applied in August 2026, after the 4.6.0 release. | Compiler-adoption checks must include both true and false bool/member stores. Presence of the old source path does not prove our firmware triggers it. Do not install a smaller image solely because it compiles. |
| [Switch-table bug 4066](https://sourceforge.net/p/sdcc/bugs/4066/?limit=25) | A reported interaction shortens then widens individual jump-table entries under particular options. | Our size flags are different. This is a boundary-test lead, not a proven current defect; it reinforces validating table stride and all computed targets before ASM rewriting. |

Version-specific compiler/source findings and exact release hashes are in
[the compiler research](optimization-deep-sdcc-research-20261023.md).
Current linked function and helper counts, source locations and candidate
contracts are in [the local inventory](optimization-deep-local-20261023.md).

## Compiler and short-transfer experiments

SDCC 4.5 previously stopped with an internal compiler error in the USB module.
The full 4.6.0 experiment has now compiled and linked: 38,100 build-report CODE
bytes, 36,292 main and 1,808 low, with 2,067 XRAM bytes. This is 1,044 fewer
CODE bytes than the 4.4 control above. Its reported stack capacity is 157
bytes. Free CODE is 2,405 bytes: 2,325 main and 80 low. The working 4.4 builder
and toolchain are unchanged. Full CPU/compiler qualification and release review
remain required; a successful link is not adoption approval.
See [the experiment record](sdcc46-probe-20261023.md).

The official 4.4 release source is now available and independently reviewed.
Its J11 relocation page check appears to use the instruction site instead of
the hardware next PC. The binary fixture run stopped after six of 42 cases:
an intentionally invalid absolute destination crashed the linker and left an
empty IHX. The 36 remaining cases, including the actual boundary mismatch,
were not run. This does not prove a crash on a valid firmware input.

Consequently short calls are **blocked from firmware integration**, not a
promised reserve of hundreds of bytes. Any resumed investigation first needs
a separately reviewed fixture correction, complete boundary evidence and an
independent final `(site + 2)` page decoder. A global REL rewriter additionally
needs all relocations, computed jumps, function/data pointers, runtime members
and packer references accounted for. See [the fixture record](short-transfer-fixtures-20261023.md).

## Directions not to count as available savings

- Four layers measured zero CODE/XRAM savings; only logical NVM addresses
  changed. Six layers remain.
- Fewer macro bytes do not move the CODE/NVM boundary automatically. Sixteen
  macros and their current capacity remain.
- Packing Direct HSV targets RAM, adds conversion CODE and changes precision.
  It is not a CODE-saving substitute for making Direct usable.
- The callee-save RGB probe grew CODE by 66 bytes and tested stack by ten;
  its caller had no spills to remove. It was rejected.
- Replacing all switches with tables is not a general rule: table payload,
  bounds, pointer loads, liveness and indirect calls can cost more.
- Reentrancy, register-bank changes, small/medium models, dual-DPTR, CODE in
  RAM, banking and protected-region reuse require new ABI/hardware contracts.
  None is a default size experiment for the current release.
- Runtime compression needs decompressor CODE and usable output storage.
  Smaller compressed input alone is not a net linked saving.

## Search record and limits

Searches covered official SDCC manuals, releases, source archives, issue and
patch trackers, maintainer discussions, upstream QMK source and size advice,
the original QMK-8051 port, and the Contiki 8051 port. Representative queries:

1. `site:docs.qmk.fm squeezing_avr maximum firmware size LTO features`
2. `site:github.com qmk 8051 sdcc optimization code size`
3. `site:sourceforge.net/p/sdcc mcs51 code size optimization function pointer generic pointer`
4. `site:sourceforge.net/p/sdcc mcs51 code size switch jump table`
5. `"sdcc_MCS51_rm" github`
6. `"8051" "SDCC" "outlining" optimization`
7. `"SDCC" "memcpy" "generic" "xdata" site:sourceforge.net/p/sdcc`
8. `site:github.com/DeqingSun/ch55xduino "__xdata" "memcpy"`
9. `site:github.com/contiki-os/contiki "SDCC" "code size"`
10. `site:sourceforge.net/p/sdcc "mcs51" "switch" "nojtbound"`

The exact release archives provide the version anchors; live upstream pages
can change. Some broad queries returned old or unrelated architecture results;
those were not accepted as evidence. The raw external DCE implementation URL
returned 404; the wrapper script was available. Related historical RFE links
575–577 could not be retrieved and supply no claim in this report. No usable
CH55x memcpy comparison or automatic MCS51 whole-program saving was established
from those queries. This is a bounded research pass, not proof that every
possible optimization has been discovered.
