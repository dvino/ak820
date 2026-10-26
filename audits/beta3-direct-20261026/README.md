# Beta.3 firmware preparation

## Scope

The work preserves the ten prepared profile compositions from commit
`b35b77cddbefdb509058f1fbaaeafaa3982ce172`. The profile registry is byte-identical;
[preserved-profiles.json](preserved-profiles.json) records its hash and every
composition. No optional module was removed to make room.

Direct v1 adds coherent readback of the 82-entry HSV palette and complete frame
transactions with generation checks. The 246-byte staging buffer freezes an
accepted frame while foreground conversion and scan-boundary publication finish.
The palette remains in RAM. The wire contract and cancellation rules are in
[the Direct guide](../../docs/DIRECT.md).

The existing GUI-lock profiles, `game` and `mmo`, use the shared W indicator for
a 2000 ms brightness cycle. An active or default layer above zero takes priority
and holds W steadily on. The independent Caps and OS channels retain their
behavior. GUI lock remains off by default. Release assets use Python installation
scripts for Windows and Linux x86_64; standalone GUI installers and their bundled
dependencies are excluded.

## Current gate state

The independently reviewed [alpha.2 correction](alpha2-admission-review.md)
records the actual legacy restore plan: the saved source has no Combo version,
so the plan performs zero Combo writes and preserves the target defaults.
The linked firmware is unchanged. All ten images completed canonical
requalification after the checker correction, and the full strict preparation
regenerated every measurement, transition result and policy. The retained
records below describe this final source freeze.

All ten fresh final builds passed full exact-image qualification on the
[frozen source](final-source-freeze.json). The [final qualification record](final-qualification.json)
binds each image, resource measurement, runtime result and retained machine
evidence archive. Every profile passed 28 base suites with 351 unit tests and
zero skips, plus 32–37 supplementary suites. Startup, foreground and all enabled
interrupt paths fit the stack capacity. The [status tables](../../docs/STATUS.md)
list the final CODE, XRAM and stack values.

The [strict preparation run](preparation-policies-run.json) passed in 1113.531
seconds. It repeated
all ten original-root measurements, checked permanent and trial packing and
recovery bytes, and completed the full settings-transition matrix. The frozen
installer suite passed 186 tests with zero skips; its source and log hashes are
in [settings-run.json](settings-run.json). Independent generated-policy admission
is recorded in [the final review](final-generated-admission-review.md). Final
platform package assembly follows from the reviewed committed inputs and is
recorded separately. Earlier build reports and interrupted preparation attempts
are diagnostic or superseded evidence; they do not qualify the final source
manifest.

The actual historical alpha.2 ROM is available and validated. Its archived
capture, full-ROM identity, CODE identity and unchanged derived backup are
recorded in [input provenance](alpha2-input-provenance.json) and
[input validation](alpha2-input-validation.json). The frozen historical catalog
contains 23 source images: two ten-profile generations and three older images.
Together with the ten new images, the completed preparation checked 33 sources
for each target profile. All 330 ordinary transition plans, 100 Caps Word Combo
plans and 100 macro Layer-Tap plans passed. The exact source/target identities and
results are in [transition-preflight.json](transition-preflight.json). These are
offline plans from validated saved backups or explicitly derived default
fixtures; they do not prove a physical settings restore.

## Reviews and retained checks

| Evidence | Scope |
| --- | --- |
| [Firmware review](firmware-final-review.md) | Direct ownership, publication, cancellation, naked-function ABI and W behavior |
| [Host review](host-final-review.md) | Strict acknowledgements, normalized brightness, Python payload and guide closure |
| [Metadata review](metadata-final-review.md) | Exact C/D symbol spaces, data bounds and original-root measurement paths |
| [Stack review](stack-final-review.md) | Exact outlined multiplication, guarded RGB target set and call-frame accounting |
| [Origin assembly review](origin-assembly-review.md) | Full canonical per-profile gates and complete atomic aggregation |
| [Release handoff review](release-handoff-review.md) | Matching installation commands, recovery links, catalog semantics and English/Russian guides |
| [Direct fixture review](direct-fixture-review.md) | Exact-image Direct limitation metadata in offline fixtures; ten real roundtrips retained separately |
| [Alpha.2 admission review](alpha2-admission-review.md) | Exact legacy identity, zero Combo writes, preserved target defaults and strict preflight binding |
| [Final policy admission](final-generated-admission-review.md) | Exact frozen source, image, packing and transition bindings before committed assembly |
| [Delivery helper review](delivery-helpers-review.md) | Committed source synchronization and an independent Git bundle import with explicit prerequisite and object-absence checks |
| [Outer delivery preflight](outer-delivery-preflight-review.md) | Exact package inventory, archive and checksum bindings, and fresh output records |
| [Python payload smoke](python-payload-smoke.md) | Real staged CLI import and `--help`, excluded GUI inputs and guide links; a minimal smoke payload |
| [Historical CI inputs](historical-ci-inputs.json) | Authenticated previous candidate artifacts and exact retained image identities |

The [MMO diagnostic](mmo-stack-dispatch.md) explains why the stack checker was
extended. Its linked image contains an outlined leaf with exactly
`MOV B,#2; MUL AB; RET`. The checker verifies the complete body and retains all
existing dispatch guards, ROM checks and spill provenance. It counts the extra
two-byte call frame. This partial diagnostic does not replace full runtime
qualification. The analyzer belongs to the final build source manifest, so all
ten final builds were regenerated after the change.

## Optimization evidence

The component evidence in [verified-components](optimization/verified-components/inventory.json)
is separate from whole-image qualification. It records portable HSV comparison,
target CPU checks, overlapping input/output cases, DMA slot writes and
same-translation-unit callers. The compact HSV kernel measures 154 CODE bytes
against the earlier 410-byte implementation. Saturation helpers preserve the
registers required by their callers, with 131,072 checked input pairs. The shared
waveform matches all 256 phases.

The [W pulse evidence](optimization/w-pulse/final-linked-results.json) includes
all 2000 phase values and R0–R7 preservation. The angle calculation replaces
division by a bounded subtraction loop and an exact small reciprocal multiply.
The diagnostic `game` image saved 157 allocated CODE bytes. The final `game`
image occupies 40,462 CODE bytes with 17 bytes of stack margin; `mmo` occupies
40,343 CODE bytes with 16 bytes of stack margin. Both retain their full prepared
composition, Direct v1 and the W pulse. The tightest final main CODE window is
`main`, with 28 trailing bytes free; its stack margin is 22 bytes.

## Preparation and physical scope

The preparation utilities retain exact source, build-tree, runtime, settings and
packing checks. [Preparation reuse](preparation-reuse.json) identifies the reused
utilities and reviewed path-normalization changes. Builds stay in their original
roots because generator dependencies and test commands bind those paths. The
reviewed aggregation helper invokes the canonical checks in those roots before
copying and validating approved bundles; it does not rewrite retained evidence.

The preparation findings were resolved before the final strict successful run.
Historical beta.2 fixtures use the authenticated frozen catalog when deriving
private backups; they retain their exact original IHX and packed CODE identities.
The new-image fixture helper now derives Direct limitation metadata from the
exact image, matching the production backup validator. The bounded correction
passed independent review, 14 helper tests and [ten real fixture roundtrips](direct-fixture-roundtrip.json).
No RAM palette was fabricated. The earlier discovery inventory predates recovery
of the actual alpha.2 input and is superseded by the provenance above.

The alpha.2 checker correction required a fresh complete qualification, followed
by the full preparation above. The current [group A](final-requalification-group-a.json),
[group B](final-requalification-group-b.json) and
[group C](final-requalification-group-c.json) reports bind those invocations.
The main invocation's outer console capture was truncated; its complete
canonical per-suite logs and results are retained in the machine archive.
The original compilation reports remain build history. The qualification
inventory identifies the current archives and the exact requalification reports.

The [retained helper sources](delivery-helper-sources.json) preserve the exact
reviewed delivery scripts. Their preflight reviews cover code; execution and
final package checks are recorded separately after committed assembly.

No USB, bootloader, reset or flash commands were sent. Static bounds, host tests
and CPU models do not verify physical USB timing, added LED interrupt timing,
display publication, retention after power removal or flash failure behavior.
Private OEM ROMs and saved settings remain outside the Git deliverable.
