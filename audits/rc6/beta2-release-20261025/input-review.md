# Packaging inputs and RGB changes

Independent source review covered the exact inputs recorded in
[root-owned-input-proof.json](root-owned-input-proof.json). It did not cover the
installer or profile documentation authored in the same work package.

No correction was required in the reviewed changes. The compressed factory
keymap decoder checks complete tables, row continuity, canonical encodings,
payload bounds and table overlap. The exported three tables retain the bytes
checked by the generator. The emitted-model initializer preserves the compiled
little-endian to saved big-endian conversion. Startup acceptance remains limited
to the two supported XRAM layouts and the exact emitted CRT sequence.

The RGB saturation change uses unsigned byte wrap detection. The new host test
checks all 65,536 input pairs. The no-Direct renderer avoids absent palette
storage; the linked VialRGB test checks the expected mode mapping for the
configured image.

The host RGB suite passed in the local pinned Docker environment with network
access disabled. Eight factory-keymap unit tests passed. Commands, observed
results and source hashes are in the linked evidence file. These checks do not
establish SDCC execution, physical timing, DMA behavior, device compatibility,
release approval or installation approval. No firmware build or device access
was performed by this review.

The later core-selection and strict inspector review found no required source
corrections. It covered finite pass30 flags, compiler feature defines and
symbols, path-bound artifacts, source and tool identities, factory-table
regeneration, typed spill metadata recapture, transformer replay and assembled
proofs, stage adjacency, outlining and linked short-call checks. The 38 offline
configuration tests passed. Exact source hashes and the command are recorded in
`additional_source_review` in the evidence file. Fresh builds and inspector
execution remain separate from this source review.
