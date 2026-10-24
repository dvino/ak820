# Accepted baseline and web firmware modules

## Input acceptance

Input `ak820-dev-stack-irq-20261024.tar.gz`: 535,122,859 bytes,
SHA256 `23e843d4eb6da5352c7d3fb5ed06e1cb877e8afc43b4bd085aebab99845cebe6`.
The clean full repository is at `f53ec73e038ed415600d2d0b405014ddb240e1c2`.
Archive paths were checked before extraction; `git fsck --full --strict` passed.

Independent source review accepted this development baseline. The retained
Leader matrix verifier passed all 20 records, including frozen source, raw
archives, identities, runtime contracts and suite plans. Repeated checker
tests passed: 32 stack, 10 IRQ and nine runtime-gate cases.

A clean `full` rebuild reproduced IHX
`898bfa2fc1bfc02562820611a7b652017bbfabf9d67a3b02d60f3d48e337c114`:
38,890 CODE bytes, 2,600 XRAM bytes and stack 160/166. All 28 base suites,
273 unit tests without skips, and supplemental suites passed. The first
sandbox run failed because LeakSanitizer could not inspect process threads.
A trial with leak checking disabled was not used for acceptance. The ordinary
complete build passed outside that restriction with no sanitizer overrides.

Remote `web-dev` `e8ba2bcb352cd5c35e9cff4c645f89a463484e10` was fetched
and merged without conflicts in `f15e4bd`. Its firmware was still at
`5cbc66f`; the later Leader work was preserved. Independent merge review
checked the 16 documentation files, 42 matching EN/RU requirements, links
and the 53-document checker.

## Implementation

Three development choices add independent modules: `full-os-indicators`,
`full-mac-pc`, `full-mac-pc-os-indicators`.

FD02 v1 supplies a volatile OS lease, firmware breathing and lifecycle
cancellation. Mac/PC swaps Alt/GUI at report aggregation without changing
modifier ownership or NVM. OS uses component 3; W keeps component 1.
The deterministic development catalog binds features to linked artifacts and
complete qualification. It grants no device or release permission.

Contracts: [indicators](../../../docs/INDICATORS.md),
[Mac/PC](../../../docs/MAC-PC.md),
[FD02](../../../web/docs/OS-INDICATOR-PROTOCOL.md),
[catalog](../../../web/docs/CAPABILITY-CATALOG.md).
Six layers, 16 macro slots, 8192 macro bytes, eight Combos and schema
`0x082002` are unchanged. Loader, installer approval and release policy
were not modified.

## OEM OS-channel evidence

The matching OEM ROM was recovered from an earlier archive and inspected
privately: SHA256
`1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1`.
No OEM image, private backup or settings were added to the working tree.

| OEM location | Observed dataflow |
| --- | --- |
| `64CE..64E9` | Action 20 sets OS state 0A84 and clears Win-lock 0A79. |
| `64EB..6501` | Action 21 clears OS state 0A84. |
| Tables `6F4B`, `6FCB` | Positions 0B (A) and 13 (S) select those Fn actions. |
| `EAAB..EAD3` | Nonzero OS state changes Alt/GUI roles. |
| `EA53..EA63` | OS state selects 0/FF, component 3, slot 4F (79), calls EC9C. |
| `EC9C..ECC9` | Writes intensity and the selected component. |
| `DD75..DE05` | Copies four-byte slots from staging 066D to DMA 0200. |

OS therefore reaches address 033F, array index 13F. W uses 13D and shares
intensity 13C. An early probe targeted W and was rejected after target
clarification; only independent OS control is retained in source.

This closes the static mode-to-channel trace. Physical LED connection,
brightness and timing remain untested. Mac/PC here is a compact modifier mode;
the OEM's F-row tables are not reproduced.

## Review and verification

The first corrected-channel combined candidate passed stack 164/166 and all
19 linked OS cases. Mac/PC tests found two One Shot failures: mode controls
consumed a queued modifier or marked a held One Shot used. The exact three AG
commands now bypass consumption. The unchanged tests pass all 10 Mac/PC
cases and all 19 OS cases on corrected IHX
`9e049f97a4ed6335f71b90a49e486b9be44b3e2e953d342358a2473889e03470`.

The first full candidate also exposed an old RGB fixture expectation: slot 79
component 3 was previously unowned, so the fixture expected a preserved sentinel.
Enabled OS/Mac profiles now correctly write that component. The fixture retains
the nonzero sentinel, checks off for enabled modules, preserves it for disabled
modules, and adds Mac OS/W independence cases. Independent review accepted the
correction; no firmware change was needed. The repeated full qualification
passed 28 base suites, 273 unit tests without skips and 25 supplemental suites.
The development catalog also passed end-to-end reconstruction of this candidate.

Independent review found an included C fixture outside the source snapshot.
The snapshot now hashes `.inc`, and a regression proves that editing an
included fixture invalidates it. The catalog also checks actual base logs
and zero-filled executable windows, rather than accepting report booleans or
ignoring CODE gaps.

Independent source-freeze review accepted the code, documentation and exact
candidate evidence. The review independently reconstructed the catalog entry,
checked all 25 supplemental results, 10 Mac/PC and 19 OS cases, the 164/166
runtime bound and both corrected findings. [Candidate summaries](candidate/manifest.json)
retain their identities; these are dirty-source pre-freeze evidence, not the
final clean matrix. The catalog's ten tests include zero-fill equivalence.

Final clean-image qualification and matrix review remain pending; their
scope is recorded in [the matrix report](final/README.md).
Source, offline qualified artifacts and installed firmware remain distinct.
No device commands, reset, flash, settings write or publication occurred.
Published and installed alpha.3 is unchanged.
