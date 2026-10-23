# Final compact tap-hold integration review

The exact d584 compact tap-hold program, host bindings and offline reproduction
policy are approved. No blocking finding remains in this review. This approval
does not authorize device operations or establish installed firmware behavior.

## Reviewed evidence

- Policy SHA256: `01ce9857aad8c36a32a93a25650e56d198e82d8454e60ae279dd5885b1f90781`.
- Packing receipt SHA256: `7ef3bfd8eab8f3369c34e2b89fe380bab62e1f6aa071822142f3f14717705c77`.
- Qualification SHA256: `0bb29a30fed47b8bf6649c95387384693f920f5bac5cd4450a3d585760d8d359`.
- Linked 65-case CPU report SHA256: `eea56e5800c8106fbd1053ad2ee5480ffb35070370b714d6d022f04401be557d`.

All 614 policy source records, 21 shared host-file records and nine legacy
bundle records matched sizes and hashes. The policy/packing receipt binding,
legacy review/manifest/installer-approval chain and shared host manifests
matched. The legacy firmware remains f1c4; the policy selects the new exact
IHX `d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3`.
The settings profile has three exact ordered pairs. Its third pair matches
permanent CODE prefix `7e6b90f51a99ac335c0cb910fffc85f1d1705e7159a12de46f8e492807c36d40`
in the sanitized packing report. The earlier unapproved 24e9 candidate was
replaced, not retained as a fourth accepted image. Same-image/forward rules,
exact identity, provenance and pre-write gates remain intact.

All 467 build input records and 77 artifact records matched actual bytes. The
image has 40,399 populated CODE bytes, ending at 0xc6e7, with 24 trailing bytes
before 0xc700. XRAM is 2,512 bytes; allocated stack capacity is 157 bytes.
The latest 65-case linked CPU report passed every expected memory snapshot and
supplied keyboard/extra trace. Peak SP was 147 from initial 98: 49 bytes exercised.
This is not a worst-case interrupt-nesting bound.

Production `validate_qualification_contract` and the package builder's
`_qualification` gate both accepted the fresh report: all 26 required suites,
258 unit tests, zero skips, pinned compiler/simulator and unchanged IHX/MAP.
All 26 log hashes matched. The report retained under
`compact-tapping-qualification-20261024/qualification.json` is byte-identical
to the original host run; all 26 copied logs match too. No suite was rerun or
silently omitted to produce this result.

## Findings and closure

The initial profile test omitted some ordered transitions. The author added
all nine pairs; independent directed runs passed, including a new run after
the exact third identity was replaced. The production allowlist matches the
new sanitized packing evidence. Initial profile review is historical as to
the superseded image hashes; this report supplies the current identity closure.

The failed complete run exposed a real Grave Escape cache/raw-owner fault.
The independently reviewed fix uses the Repeat-context discriminator and
owned basic registration/release. The independent host run rejected all eleven
mutations and matched 156 eligible QMK traces. Older fixture corrections use
public layer-state setup and effective owned modifier/layer semantics. The
fresh complete qualification includes these corrected suites. Details are in
`compact-tapping-gesc-fix-review-20261023.md`.

The old macro cancellation fixture assumed a reset branch absent from the
linked build. Its replacement hook was independently reviewed; the complete
new CPU run passed. The hook proves cancellation during playback, not EE_CLR,
EEPROM or reset execution. The earlier failed run remains failed evidence.

TESTING initially called the retained pointer-only 23-suite result the current
candidate. English and Russian documents now identify feac explicitly as
historical and distinguish the fresh d584 26-suite result. RESOURCE-BUDGET
now labels the older linked optimization review as pointer-only history.
These documentation findings are closed. README, configuration, tap-hold,
settings, status, testing and budget descriptions agree on source, built and
uninstalled state. Future selectable profiles and Combos are separated from
current support. The optional feature audit labels earlier-image size probes
and the 1–2 KiB Combo planning estimate without claiming a linked Combo result.

No production implementation, policy, packing receipt or qualification run was
authored by this review. No build, USB access, device write, reset, bootloader
transition, flash or commit was performed. Interactive Windows acceptance,
dev CI, physical input, USB timing, IRQ overlap, durable storage and power-loss
behavior remain outside this offline approval. No new distributable archive
was claimed as built by this review.
