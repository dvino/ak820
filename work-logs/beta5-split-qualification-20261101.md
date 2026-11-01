# Beta.5 split offline qualification, 2026-11-01

Candidate source commit: `3f71dd1005cd7ec7e1ca41248041b1d5b04acfa8`.
This is evidence for the local candidate, not a release approval or hardware test.
The isolated source and evidence are retained at
`/home/agent/ak820-beta5-proof-20261101`; private reference and draft inputs are
retained separately at `/home/agent/ak820-beta5-private-20261101`.

The first run passed `main`, `game`, `mmo`, `typing` and `code`; `pointer`
failed its mouse-keys configuration gate. A separate diagnostic attributed the
failure to a temporary directory in the read-only QMK root; that diagnostic was
not retained as a machine report. The remaining five passed in a separate
restricted run with temporary root entries monitored and core dumps disabled. The combined exact-image remeasurement
reported linked-memory, runtime and offline-test passes for all ten images;
combined module coverage was complete. These results do not validate physical
behavior or authorize settings writes, restore, flash or release.

| Evidence under `qmk-8051-ak820/.build/` | SHA256 |
| --- | --- |
| `proof.log` | `0a2b9fb8c03c1b74b77192aaba16497fab55d7b51b3dbf19eadcc8899f5188d1` |
| `proof-retry.log` | `e2406363332d0ea068d947875d49fc2a06112531b33351f5cbcc5d312becf189` |
| `proof-retry-report.json` | `b64fde5c619e3901e8987ed78f75b0f381ace614c58bb9229421501c581b00c8` |
| `proof-combined-measurements.json` | `8cf381c61f5b352f38b92ed671e834de49e8523e6f33d469a44f8c8f7853be22` |
| `proof-combined-catalog.json` | `9014f2d8e8ee8b14311087d3adf941ee3e07235b077d27c22dda0a998c213a5b` |
| `proof-retry-source-events.jsonl` | `3455cee1eae97aeaede530f14d8034db895005be658bf5511f28018283a64000` |
| `proof-source-locked-before.json` | `9dbf11edc2805a1cf475e22baaaf2ad71bea872dc1f1646d43f71d93e2af3e93` |
| `proof-source-locked-after.json` | `9dbf11edc2805a1cf475e22baaaf2ad71bea872dc1f1646d43f71d93e2af3e93` |
| `proof-draft.log` | `b8d08eb32bc9b6e53167636e0adb63cf631f3f22ef788d3c1bf6a9952285e106` |

The combined catalog is a derived offline draft, not a release catalog. The
source inventories match. The monitored root events were four temporary
directory creation/deletion pairs. The draft release preparation stopped at
`Settings v3 exact-image qualification and identity gates are pending`; its
partial outputs are unapproved. The draft log is retained, and the partial
output was moved from the proof checkout to
`/home/agent/ak820-beta5-original-evidence-20261101/failed-draft` before
requalification; it is not relabelled as successful evidence. The settings identity, migration and write
contracts remain separate from linked-image qualification.

Before any requalification, the complete original `.build` tree was copied to
`/home/agent/ak820-beta5-original-evidence-20261101/build`. The source and copy
matched in a 138,942-entry content, mode and ownership inventory; the retained
`inventory.json` SHA256 is
`17d960d44e66ca1e32845d190089cabbe777b421e6199859ece052839d4a46a4`.
The copy preserves the original evidence; later qualification cannot change the
commit at which the images were built.
