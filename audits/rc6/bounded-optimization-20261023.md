# Two bounded optimization probes

Date: 2026-10-23. Base commit: `5887e92`. All work was offline. No USB,
reset, loader transition or firmware installation was performed.

The private journal pointer is adopted in source after independent review:
it saves 31 linked CODE bytes and one XRAM byte. The macro delay replacement is rejected: it adds
three CODE bytes. Its arithmetic is exact, but SDCC 4.6 already emits a compact
hardware multiply for the original expression.

## Controlled builds

Three separate shared Git clones of the same base were used beneath
`/workspace/scratch/664bab7a0eb4/probes`. The control contains no firmware
changes. `bounded-pointer` changes only the private journal validator parameter.
`bounded-delay` changes only the delay expression. The latter also contains
probe-only host harness additions; these are not firmware build inputs.

The pinned SDCC 4.6.0 #16555 installation is
`/workspace/scratch/664bab7a0eb4/ak820/toolchains/sdcc-4.6.0`.
Its compiler SHA256 is
`3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891`;
assembler SHA256 is
`2ae1a62eb7454d80787352fc398ffe87847b1bb048988908f2241d1a4a37d877`.
The canonical pinned LUFA tree was copied into each clone. The shared QMK CLI
was read from the canonical virtual environment. No shared toolchain or virtual
environment files were changed by these probes.

From each clone's `qmk-8051-ak820` directory, the build command was:

```sh
/workspace/scratch/664bab7a0eb4/ak820/qmk-8051-ak820/.venv/bin/python util/build_ak820.py \
  --toolchain /workspace/scratch/664bab7a0eb4/ak820/toolchains/sdcc-4.6.0 \
  --qmk-bin /workspace/scratch/664bab7a0eb4/ak820/qmk-8051-ak820/.venv/bin/qmk \
  --build-dir .build/bounded-probe
```

The control used `.build/bounded-control` instead. Each build preserves its
`build-report.json`, input hashes, logs, linked map, memory report and relocated
listings. Default size optimization, exact outlining and the existing eleven
callee-save functions were retained. No short calls were enabled.

| Build | Linked CODE | Main window | Low window | XRAM | Initial SP | Stack capacity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Control | 38,100 | 36,292 | 1,808 | 2,067 | 0x62 | 157 |
| Private XDATA pointer | 38,069 | 36,261 | 1,808 | 2,066 | 0x62 | 157 |
| Rejected delay | 38,103 | 36,295 | 1,808 | 2,067 | 0x62 | 157 |

The CODE windows remain `0x3027..0xC6FF` and `0x28A0..0x2FFF`.
Both candidates fit. The IRAM layout and allocated stack capacity are unchanged.
All three compile logs contain the same multiset of 137 warning messages;
there are no new warning messages. This comparison does not dismiss inherited
warnings as harmless.

| Build | IHX SHA256 |
| --- | --- |
| Control | `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e` |
| Private XDATA pointer | `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8` |
| Rejected delay | `847f4c8be31c62dc652d23e0bd0c147b8f910d28ca6869d121855a07b2dbe448` |

## Private journal pointer

The adopted source edit is:

```diff
-static bool journal_header_valid(uint8_t *header) {
+static bool journal_header_valid(uint8_t AK820_XDATA *header) {
```

This function is static and has exactly one call, in `recover_journal`.
That call passes its local nine-byte `header` array. The large-model compiler
allocates the array in XDATA: control address `0x0529`, candidate `0x0528`.
The relocation moves it because the preceding private pointer parameter shrinks
from three bytes to two. No pointer cast or public ABI change is required.

The linked helper begins at `0x394B` in both images. Its body shrinks from
113 to 85 bytes. Three generic reads become direct `MOVX A,@DPTR` accesses;
the third pointer byte is removed. The caller no longer supplies a generic
memory-space tag, accounting for the remaining three CODE bytes saved.
The NVM format, all nine journal bytes, CRC, commit-last order, replay gates
and flash operations are unchanged. Six layers, sixteen macros and all other
feature settings remain unchanged.

Direct linked helper execution passed all 2,304 single-byte mutations in both
images. The exercised helper stack use falls from six to four bytes, with
peak SP `0x68` versus `0x66`. This is a measured path result; the 157-byte
capacity is a separate allocation figure and is not a global stack bound.

## Rejected delay expression

```diff
-uint16_t ms = (uint16_t)(d0 - 1) + (uint16_t)(d1 - 1) * 255u;
+uint16_t high = (uint16_t)(d1 - 1);
+uint16_t ms = (uint16_t)((high << 8) - high) + (uint16_t)(d0 - 1);
```

Both bytes must be nonzero before this expression runs. Thus `high` is
0 through 254, its shifted value is at most 65,024, the subtraction is
nonnegative, and the final delay is 0 through 65,024. Host checks with address
and undefined-behavior sanitizers compare every one of the 65,025 legal pairs.
The rejected expression remains in the focused regression runner as a fixture.

The old deep-local inventory described a call to `__mulint` in an earlier
artifact. The fresh SDCC 4.6 control instead uses `MUL AB` at `0x85BD`.
The replacement emits a longer shift/subtract sequence and increases the
complete linked image by three bytes. The zero-or-negative-benefit stop rule
therefore rejects it. No combined build was needed, and no delay source change
is proposed for adoption. Arithmetic host agreement is not claimed as target
execution proof for the rejected expression.

## Verification

The reusable additions are `tests/ak820_bounded/run.py` and `emitted.py`.
The host runner checks 264,448 header cases, all 65,025 delay pairs and real
macro playback for all sixteen IDs at zero/maximum delay and after early exits.
The linked runner checks the private helper in an already built image and binds
its report to the exact IHX hash. Its README gives commands and limits.

Additional existing suites passed against the pointer build:

- NVM diagnostic host suite and 10,944 host power-cut cases, using the production
  backend and the documented `-Wno-clobbered` compiler option.
- Twelve linked IAP cases, including partial journal/target programming,
  recovery replay, failed target readback, no ACK and retained committed journal.
- Three linked emitted suites covering matrix/layer release, recursive macro
  protection and RGB suspend/resume.

The rejected delay build also passed the existing 196,019 macro differential
traces and the strengthened sixteen-slot guard cases. These passes establish
that the rejected expression is arithmetically plausible; they do not reverse
its linked size regression.

Playback assumes a complete grammar validated before publication. A probe
that supplied an arbitrarily truncated encoded operand directly to playback
exposed an inherited read past the reported stream length. No parser fix is
included in this bounded package. Zero operands and valid stored streams are
tested; storage publication validation remains covered by separate suites.

No physical timing, USB interaction, flash durability, power-loss behavior or
interrupt overlap was tested. These builds do not describe installed firmware. Independent review passed
for the private pointer, tests and retained evidence. The canonical source
build reproduces the pointer IHX exactly; the installer release is unchanged.
The source candidate is not a device-update approval.


## Retained evidence and review

The [evidence manifest](bounded-evidence-20261023/manifest.json) locates the
portable control, pointer and rejected-delay roots. All 76 artifact records in
each build report are retained with exact size and SHA256, alongside 64 relocated
listings per build, compile warnings and linked test results. Original absolute
paths describe where the probes ran; they are not prerequisites for using these
copies. The manifests record input hashes but do not bundle downloaded compiler,
LUFA or Python environments. Install pinned dependencies for a source rebuild.

An independent reviewer verified 426 size-bearing manifest entries, all 228
build artifact references and three canonical reproduction files. The reviewer
recomputed identical 137-warning multisets and reran the header helper on all
three retained roots: 2304 cases each, without the transient probe directories.
The linked inventories also regenerate from the retained roots. The finding
about transient-only evidence was closed. The [review record](bounded-optimization-review-20261023.md)
keeps the ABI checks, independent reruns and limits.

The complete canonical regression is a separate
[23-suite run](roadmap-qualification-20261023/final/report.json), with 247 unit
tests and zero skips. Supplementary production NVM and macro-storage host checks
are retained in [storage checks](roadmap-qualification-20261023/supplementary/storage-checks.json).
None of these tests grants Windows, device, durability or release approval.
