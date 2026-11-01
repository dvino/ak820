Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

## Current candidate

The current main image ends at `0xc6a5`, below the exclusive `0xc700` CODE
limit. Its offline stack bound is 165 of 183 bytes. All ten profiles passed
CI qualification in [CI run 41297661542](https://github.com/dvino/ak820/actions/runs/41297661542),
but release assembly failed on stale exact-image safety witnesses; publication
and physical validation remain unconfirmed.

A fresh split offline run qualified all ten images and remeasured their linked,
stack, interrupt and regression evidence together. Draft release preparation
then stopped at the pending settings v3 identity gate; this run does not approve
a release, a settings write or a physical restore.

## Earlier source experiments

The following section records the candidate and inspection state before
2026-11-01. Present-tense statements in it describe that earlier state, not the
current candidate or the CI result above.

The permissive-hold action seam is experimental, disabled and not wired into
catalog builds. A synthetic SDCC test of a deliberately nested callback found
that shared argument storage in `ak820_tapping_before` can suppress a press and
admit its duplicate. The injected callback is not proof that this route is
reachable in firmware. The test-only reentrant control does not qualify a fix;
callback reachability, transitive ABI safety, cancellation, stack and interrupt
bounds still need verification. The separate experimental generation-based
frame pool can permanently exhaust and must not be wired into firmware.

Before the settings index optimization, a pointer build stopped at the CODE
limit: linked addresses reached
`0xc78e`, beyond the `0xc700` exclusive limit by 143 address bytes. The failed
IHX SHA256 is `ebc897ecdac1a018fe89d7ccfb9a022a9b51189baf78785c6f85e529d3dc85ef`.
A separate main build reached `0xc7ee`, 239 address bytes beyond the same limit;
its IHX SHA256 is `4bdff3025ece90e8e33d5a64c0ec65c66c839da7b71e0905de59d2d20e407369`.
Neither failed image has a successful build report or exact-image stack/IRQ
qualification. The bootstrap images used an enlarged diagnostic window; their
resolved stack roots do not qualify the failed images or prove complete safety.

In an isolated source copy, the retained settings index change reduced linked
CODE occupancy by 27 bytes for pointer and 16 bytes for main. Both still failed:
pointer reached `0xc773` (116 address bytes over) and main reached `0xc7de`
(223 over). Their failed IHX SHA256 values are respectively
`1227e3678e66b370023b0e2a1937ba16d3d55e06ccc072ae481394c5c3203135` and
`f28b0a8de921b6fa0a8b148c069cc703292a03dea18f09e618c93ba9da2a61d7`.
Eight host settings configurations passed; neither image has exact-image
stack/IRQ qualification or hardware validation.

A further isolated CRC-store change, retained in the source, reduced CODE by
another 58 bytes for pointer and 36 for main. Both still exceeded `0xc700`:
pointer ended at `0xc739` (58 address bytes over) and main at `0xc7ba` (187
over). Their failed IHX SHA256 values are respectively
`bf649311cf4b27bc6ad444fa183f13f3727a506ad93888f11be3af682c8b0cd8` and
`8919f87a821ccbc1465d13ebf4fa17861cb5553ca26654dc23231d8a64436e58`.
Eight host settings configurations passed, including exhaustive out-of-range
IDs; the failed images have no exact-image stack/IRQ or hardware qualification.

Encoding field width in the existing positions table reduced CODE by a further
36 bytes for pointer and 38 for main in isolated builds. The change is retained,
but both links still exceeded `0xc700`: pointer reached `0xc715` (22 address
bytes over) and main `0xc794` (149 over). Their failed IHX SHA256 values are
`6f7ce0814080320f85a7ae3df92ab8d152b41cde34e930a63e1fda953e96f237` and
`1ab07a49d78e27b1022426c0597ce3e1881d9f75de6ccc7dba59db2cf80f9b5d`.
Eight host settings configurations passed, including invalid IDs and supported
field capacity checks. These images have no exact-image stack/IRQ or hardware
qualification.

A validation-loop change saved a further 3 bytes for pointer and 4 for main.
In the isolated builds, pointer reached `0xc712` (19 address bytes over) and
main `0xc790` (145 over). Their failed IHX SHA256 values are
`0c0adaa3174f63e44fe8c75b4a15ed28f093b584554bc45bbdd53f7627174e8d` and
`380f0a55e2334e6f36586694b4556fea9b1e8f69384715c5d25775d59485621d`.
The change is retained with a comment explaining the visited fields; that comment
was added after measurement. Host settings tests passed in eight configurations.
The failed images remain unqualified and have not been tested on hardware.

A Key Override layer-mask change, retained after isolated measurement and host
predicate testing, reduced occupied CODE by another 20 bytes for pointer and 25
for main. The host test covers all layer and trigger-mask bytes, but its modifier
sweep is limited. The main link still failed at `0xc777`,
120 address bytes beyond the limit; its IHX SHA256 is
`6361cf0582ae203e25fdfd5447ce15982b3162818ed0a734e33bce207b3a3ef3`.
The pointer image reached `0xc6fe`, one address byte below the exclusive limit.
Its IHX SHA256 is
`cca7678ab3c875b7decc30ea059b3b08cf0751df178b2b5bc94ced3144d14f50`.
For that exact image, the offline startup, foreground and IRQ stack gate passed
with a bound of 167 bytes within the 184-byte capacity. The result depends on
its recorded CRT, ABI, memory-access and OEM-wrapper assumptions; it is not a
hardware or release qualification. Main has no corresponding safety result.

The retained encoder state update saves a further 7 occupied CODE bytes in each
isolated build. Main still failed at `0xc770`, 113 address bytes over the limit;
its IHX SHA256 is `287c760e6e46bb7a08770c432ef840b986b8653b9c6411beb5752e7d5b1bdf66`.
The pointer image reached `0xc6f7` with 8 address bytes of headroom; its IHX
SHA256 is `9fd5505686b47b855042e2b1aa8ab314700d20af9f5ddc782ec4aa19a4d7b6b8`.
Its exact-image offline stack/IRQ gate passed at 167 of 184 bytes, under the
recorded CRT, ABI, memory-access and OEM-wrapper assumptions. The host encoder
comparison covered both directions in a non-split, non-mapping fixture; it did
not test hardware. Neither the main image nor a release is qualified by this.

The retained invalid-settings classification change reduced the linked span by
another 13 bytes for pointer and 9 for main. Main still failed at `0xc767`, 104
address bytes over the limit; its IHX SHA256 is
`b7146a4bcb611eda9c0367cd7dcb273229e330e41b6ef3a4f0578147b5dd35e5`.
Pointer reached `0xc6ea`, with 21 address bytes of headroom; its IHX SHA256 is
`c8d313c3206b85e5222cc24b0def2755cfaf9feb543224cc2b8852465468267e`.
For that pointer image, the offline stack/IRQ gate passed at 167 of 184 bytes
under the recorded CRT, ABI, memory-access and OEM-wrapper assumptions. Eight
host settings configurations passed the blank and malformed-record checks.
These results do not qualify main, a release or physical hardware.

A retained Leader keycode predicate was measured separately from that baseline.
Main still failed at `0xc75f`, 96 address bytes over the limit; its IHX SHA256
is `5186fb06def6606c178a873fef7bdef6c9d4046328b0878cbc16677c1bc3b464`.
Pointer reached `0xc6e5`, with 26 address bytes of headroom; its IHX SHA256 is
`3d1eb6def4db29e0bb5bd8ef228418979da4279286f82cb20eed8ba44431b7a1`.
The offline pointer stack/IRQ gate passed at 167 of 184 bytes with the recorded
assumptions. Host tests covered all 65,536 keycodes. These results do not
qualify main, a release or physical hardware.

A retained Combo control expression was measured separately from that baseline.
Main still failed at `0xc75c`, 93 address bytes over the limit; its IHX SHA256
is `e0620a1d0471703166f913bf591f3e7f5b0feeb6dc48ccf013541c8807b77454`.
Pointer reached `0xc6ec`, with 19 address bytes of headroom; its IHX SHA256 is
`dd618df83d48f8af9d70cf4d399acc3b412f6f99801cd23cb83dba1ab8242647`.
The offline pointer stack/IRQ gate passed at 167 of 184 bytes with the recorded
assumptions. Host tests covered the control transitions and cancellation. These
results do not qualify main, a release or physical hardware. These Leader and
Combo results are from separate images.

A subsequent main build combined both changes. It failed the CODE interval
check at `0xc754`, 85 address bytes over the limit; its IHX SHA256 is
`3959610b2953f56c40fd44ebd8a35965d71cbbc47eedd00e94b30158936e8d34`.
This failed image is not qualified for release or hardware.

The current, unqualified candidate admits only authenticated published beta.4.1
profile image identities and its own current profile image identities as settings
sources; restore targets are candidate profiles only. Beta.3 sources are not
admitted. Beta.4 and beta.4.1 images have identical image identities, so they
cannot be distinguished by image identity. This policy does not qualify the
candidate, authorize settings writes or establish physical restore behavior.

These are historical candidate-policy observations; they do not establish
qualification or publication of the current beta.5 candidate.

The source candidate adds runtime Leader timeout storage and a linked default
marker. Focused host tests cover the codec, synthetic marker checks and blocked
writes; these do not qualify an image. Settings v3 profile loading, restore and
protocol writes remain blocked pending the exact-image authorization and
migration gates. Erased settings records are rejected when the source QSID 22
value cannot be authenticated. Before each standalone write transaction, the
adapter revalidates the approved release and compares live CODE, manifest and
protected ranges on the open handle. Direct uses one check for its bounded
multi-packet upload; restore retains its backup, unlock and per-write guards.
This is not device attestation or an OS-wide lock. Another raw-HID client can
change the loader marker after the check, including on a failed loader entry.
During a transaction close other clients, do not press keys or trigger a reset or
loader transition. A transport fault stops the transaction. The remaining race
and exact-image qualification still block candidate release.
No candidate CI, release or device result is claimed by these tests.

Configured-build inspection rejects current-source builds until the compiler-input
contract is closed. The configured build entry point filters the environment
before starting Python and disables its user site; the builder also filters the
Make environment and explicitly clears `NOLTO_CFLAGS` and `INIT_HOOK_CFLAGS`.
The C object recipe records ordered command arguments and only `PATH`,
`SYSTEMROOT`, `WINDIR` and the build and object roots supplied by the builder;
it passes those values to the compiler and nested generator calls. The builder
checks the exact roots and capture completeness. Direct Make without those roots
uses the legacy default-keymap path and does not produce qualified captures.
Source snapshots and hashes identify the inputs used and detect changes at
checks; they do not independently establish source provenance or continuous
stability. Qualification assumes a trusted checkout, runner and compiler and
requires review of the recorded inputs. A capture is claimed before compilation and retained on
failure or interruption, so a duplicate cannot start another compiler. Incomplete
captures are invalid and require a fresh build directory. The pointer pass30
policy checks exact ordered flags, object/source mapping and nested calls. The
builder records its policy marker only after validation; inspection checks the
bound captures, dependency files, source inputs and toolchain before the existing
fail-closed gate. Other profiles and modes are not covered and remain unverified. Historical verification
is unchanged. Offline pointer builds captured 76 successful C invocations for
both the default and cursor-step 9 configurations, but both linked beyond the
CODE limit at `0xc700..0xcbf6` and produced no qualified report. A fresh
pointer pass30 build subsequently linked at highest address `0xc6cc`; it
recorded 79 object commands and all five nested default-keymap SDCC commands;
the builder checks the nested commands against the wrapper and its environment.
Qualification stopped at the unverified compiler-input contract, before the
full offline gates. The pointer policy matched those 79 historical argument
vectors; a reconstructed copy with redacted environment fields passed the nested
check. Current captures record the environment actually passed to the compiler.
The pointer policy is limited to Linux: it permits absolute PATH entries and
checkout paths with spaces, but not whitespace in the relative build directory.
Captures contain absolute working-directory and tool paths, so validation requires
the original checkout and toolchain locations; relocated evidence is not supported.
The pointer policy includes an explicit 79-entry source/object mapping and
rejects missing, extra and substituted units. A later pointer pass30 build recorded
the policy marker; its input closure and artifact binding passed separate checks,
and its runtime-safety report passed. Its profile regression report failed at
`release-safety-gates` (19 earlier entries passed): a test expected `Build
configuration differs` but received `Build timing values must be integers`.
The build process exit status was unavailable, and this is not a qualified image.
A non-mocked retained-evidence test also replayed the pass30 transforms, checked
the linked image and rejected changed or missing report-bound evidence. It tests
these stages individually, not a successful end-to-end inspection or release.
A subsequent fresh pointer production build produced IHX SHA256
`bf09a9ae810c5efb8848e7ef5a87eeef01ad9fe5c6b7ee03482f6fc429bcd25f` and exited
1 at the closed inspection gate, before its runtime or regression gates. It is
not qualified. Independent integration review is still required; the inspection
and release gates remain closed. Explicit unknown and `unverified` markers are rejected even for
pinned historical provenance; marker-free historical inspection remains supported.
QMK tooling and generated inputs remain inside the
trusted local-builder boundary, not a package attestation. Neither build
establishes physical behavior.
This also blocks qualification of explicit Mouse Keys overrides. Release entry
points reject configured reports with missing or unknown current provenance;
a contract marker alone cannot approve a build. The historical configured
exception requires the pinned builder and Mouse Keys source hash pair and the
existing exact-image safety witnesses.

Failed-Combo Auto Shift is deferred after the candidate main link exceeded its
CODE window by 156 bytes. Current source bypasses it; no new image fit or release
qualification is claimed.

`AK820_COMBO_AUTOSHIFT` is a non-catalog compile-time opt-in for eligible
successful Combo outputs. Host tests do not qualify an image: exact-image stack,
interrupt and regression checks are pending. Catalog profile names and existing
build metadata do not identify this option; see [Compact Auto Shift](COMPACT_AUTOSHIFT.md).

## v0.6.0-beta.5

The current beta.5 candidate is not yet published. The ten profiles passed offline qualification in
CI run 41297661542, but release assembly failed because the configuration differs from the reviewed
exact-image witness. The safety evidence must be updated and checked before
release. No physical keyboard test is claimed.

## v0.6.0-beta.4, published 2026-10-28

All ten beta.4 profiles passed offline exact-image firmware qualification:
28 base suites, 353 unit tests without skips per profile, and each profile's
supplementary regression suites. The offline settings suite passed 188 tests
without skips. The candidate supports settings transitions from the immediately
preceding beta.3 build and between its own profiles. The release is published.
The published catalog does not authorize flashing, and no physical device
testing has been performed.

### Beta.4 offline measurements

These historical measurements describe beta.4, not beta.5.

| Profile | CODE bytes | XRAM bytes / 3008 | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: |
| main | 40,468 | 2,853 / 3,008 | 161 / 182 | 21 |
| game | 40,381 | 2,925 / 3,008 | 161 / 177 | 16 |
| mmo | 40,272 | 2,928 / 3,008 | 165 / 179 | 14 |
| typing | 38,741 | 2,346 / 3,008 | 161 / 184 | 23 |
| code | 38,398 | 2,335 / 3,008 | 161 / 184 | 23 |
| pointer | 38,807 | 2,354 / 3,008 | 161 / 184 | 23 |
| onehand | 38,768 | 2,381 / 3,008 | 165 / 185 | 20 |
| creative | 39,849 | 2,862 / 3,008 | 165 / 183 | 18 |
| shortcuts | 38,673 | 2,398 / 3,008 | 165 / 185 | 20 |
| multios | 38,309 | 2,328 / 3,008 | 161 / 183 | 22 |

## v0.6.0-beta.3 firmware qualification, 2026-10-26

All ten unchanged profile configurations have completed exact-image firmware
qualification. Each profile passed 28 base qualification suites with 351 unit tests and
zero skips. The separate profile regression runs passed 32 to 37 supplementary
suites. Stack bounds cover startup, foreground code and every enabled
interrupt source; all are within the reported capacity.

| Profile | CODE bytes | XRAM bytes / 3008 | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: |
| main | 40,466 | 2,858 / 3,008 | 160 / 182 | 22 |
| game | 40,462 | 2,932 / 3,008 | 160 / 177 | 17 |
| mmo | 40,343 | 2,935 / 3,008 | 164 / 180 | 16 |
| typing | 38,720 | 2,351 / 3,008 | 160 / 184 | 24 |
| code | 38,467 | 2,342 / 3,008 | 160 / 184 | 24 |
| pointer | 38,902 | 2,361 / 3,008 | 160 / 184 | 24 |
| onehand | 38,806 | 2,388 / 3,008 | 164 / 185 | 21 |
| creative | 39,903 | 2,869 / 3,008 | 164 / 183 | 19 |
| shortcuts | 38,796 | 2,405 / 3,008 | 164 / 185 | 21 |
| multios | 38,415 | 2,335 / 3,008 | 160 / 184 | 24 |

Direct v1 is present in `main`, `game`, `mmo` and `creative`. It supports RAM-only
readback of the 82-color HSV palette and atomic full-frame uploads. In `game`
and `mmo`, GUI lock is off by default. When enabled, it pulses W through a
2000 ms brightness cycle; an active or default layer above zero takes
steady-light priority.

The release uses Python installation packages for Windows and Linux x86_64.
The GUI installer is excluded; the companion application is separate. Firmware
qualification, package assembly and independent approval have separate
records for each exact image. Source evidence is indexed in
`audits/beta3-direct-20261026/README.md`.
Release acceptance on 2026-10-27 passed 303 host tests, 186 installer/settings
tests, four catalog-edge regression tests and checks of 79 public documents.
Independent firmware and host reviews are retained alongside the source evidence.
Publication requires successful CI for the final merged `main` commit and its
release tag. No hardware or device writes were performed during acceptance.
Physical USB, LED and DMA timing, and power-loss or durable-storage behavior
remain unverified.

The last historical installation was alpha.3 on 2026-10-24, image SHA256
`d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`. This is
a historical device record and does not establish beta.3 device behavior.
