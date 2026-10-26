# Final generated-data review

Independent review, 2026-10-26. No actionable findings. The reviewed source and
generated evidence are accepted for the requested source commit and push.
This does not approve a release, tag, device operation or hardware behavior.

The earlier source review and ROADMAP review remain applicable. This final
pass checked the generated data without rerunning builds or CPU suites.
Only this report and the ten independent `program-review.md` records were
written by this reviewer.

## Checked bindings

All ten current profiles were checked: main, game, mmo, typing, code, pointer,
onehand, creative, shortcuts and multios.

- All 8,386 policy source records match actual file sizes and SHA256 values.
  Host manifests, safety source manifests and every stack/startup/IRQ/transition
  witness also match current Windows file bytes.
- Policy, safety record, packing receipt, measured catalog and exact-image
  settings identity agree on their target. Receipt hashes and normalized symbol
  identities agree. The unchanged policy validator accepts every new review.
- Each retained origin binding has a successful canonical measurement, matching
  matrix/log hashes and current source hashes. Every selected matrix row passes
  exact-image runtime and offline-test admission.
- The unchanged runtime combiner was run against each retained foreground,
  startup and IRQ witness, current checker sources and recorded memory limits.
  Every reconstructed result equals its runtime summary and passes.
- Permanent/trial packing records and recovery hashes agree with the packing
  preflight. Recovery equality and no physical USB access are explicit.
- The frozen settings record reports 180 tests with no skips and successful
  exit. Its tested sources and retained log still match their recorded hashes.
- The 230 transition cases cover exactly the catalog edges: 23 sources to ten
  current targets. Separate Caps Word and macro Layer-Tap grids each cover all
  100 current-profile pairs. All cases pass. Historical images remain sources.

The pinned `f1c4347e...` historical source retains CODE SHA256
`6ff7b1653925da7dc12bdb6f7ef5fc1dc4319c5b931def50c68b9cf45c4054d7`.
The transition evidence describes offline-derived full-ROM fixtures and does
not claim live capture, getter verification or a physical restore.

The inventory helper and its location metadata were also inspected. They
report retained qualification flags and identities, and explicitly distinguish
that inventory from canonical original-root admission. They do not replace the
canonical checks above.

## Review records and limits

The ten new review records bind their own current policy SHA256, IHX SHA256,
normalized symbols SHA256 and test source snapshot SHA256:
`6c1ccb04abb429fd93f9521fcb3a7aa3433b30d785b3728e0964ff878c47721c`.
They report `status: passed`, `hardware_validated: false` and zero physical
device commands. Any later change to a bound input requires renewed checking.

These checks establish source and offline-evidence consistency. They do not
establish committed-HEAD reproduction, native installer assembly, publication,
physical installation, durable settings, input behavior or DMA behavior.
Those remain separate gates. No keyboard command was sent during this review.
