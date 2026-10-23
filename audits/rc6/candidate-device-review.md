# RC6 device evidence review

Date: 2026-10-23. Independent review of saved files only. The reviewer did
not author the updater or test runner and did not open USB, change a setting,
reset, enter the loader, build firmware or flash the keyboard.

Result: PASS for the completed GUI update and the recorded protocol tests.
No blocker was found in this evidence. This is not approval for another flash.

## Installed image

The owner completed the GUI update saved in
`host/runs/20261023-gui-physical-update-success`. Its events record a fresh
FE08 lock, FE06 physical unlock request, FE07 polling from counter 30 to zero,
then physical consent at 10:51:24.532476 UTC. Consent names the displayed
permanent image SHA256
`54290ce406fda133bd90703664f60559e23620f184f89033c98dddb56e2299ed`.
The 0B loader request follows consent. The log contains one erase/flash attempt.
The nested loader log records identity acceptance before erase, one erase,
transfer, checksum acceptance and restart. The completed event reports exit 0.

After restart, two EP0 samples show main-loop progress. The saved 65,536-byte
ROM has SHA256
`55b088028b6a1f11b12390ab7fc31233ea1a036a538d44a6c9de6917fae9bff6`.
I independently compared its application bytes at `[0x2800, 0xEFC0)` with the
51,136-byte prepared permanent image: they match exactly. The bytes before
0x2800 and from 0xEFC0 onward match the fresh pre-update ROM. The diagnostic
report records matching application code, stable repeated NVM/journal reads,
an empty journal header and no storage failure.

The prepared session records IHX SHA256
`d2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce`
and MAP SHA256
`9e1ef5262685ea85f3362b378c28836d2af9b51f6699b970c61bafdf3dd5b000`.
These identify the source build inputs; the full ROM comparison identifies the
installed bytes. The separate physical GUI artifact and source reviews remain
the evidence for standalone packaging and the updater's offline checks.

## Automatic device tests

Both `host/runs/20261023-candidate-device-readonly/report.json` and
`host/runs/20261023-candidate-device-roundtrips/report.json` finish with PASS.
The lead confirmed that the second process completed with exit 0 before this
review was finalized. Both captured initial ROMs have the installed full-ROM
hash above. Their report bindings name the prepared candidate image above.

Read-only checks cover 498 key mappings, all 12 encoder mappings, 16 macros
through the published 8,192-byte view, and RGB protocol data for 82 LEDs.
The authorized write run changes and restores one representative key on each
of six layers, both encoder directions on every layer, and RGB RAM settings.
Every one of these checks records PASS and `restored: true`;
`restore_pending` is null and neither report records an error.

I checked the current runner and protocol file hashes against both reports:
`62b029be8316ef36b3925ff1a23cb3499f9c982d1c0a2861b5bf702cde86b2f3`
and `a361a55cf3939a5fbd4a9b068f42dbde9fa4677b934b9c8758ac56e300a9d986`.
The bound runner compares each temporary durable change against the complete
expected NVM image, checks unchanged neighbors, verifies stable reads before
restore, and requires exact full NVM restoration. It checks storage status
throughout and stops on failure without automatic recovery.

Independent file comparisons confirm that both final NVM captures equal their
10,240-byte baselines, SHA256
`04885d9fcabe876947f003cf82dc246ab83bfcdd878c22d89e30463c48a9bfe5`.
The write run's last mutation baseline also equals that original baseline.
Both final journal headers are zero. RGB RAM changes leave durable NVM equal
to baseline. These are direct durable-storage readbacks during the same run;
they do not establish persistence after a power cycle.

## Limits

Macro writes were skipped because Vial was locked; no unlock was attempted.
RGB durable save was skipped because the packed saved-config mode has no
implemented comparison oracle. No durable-save command was sent. The runner's
transport log records the EP0 startup samples and request/reply traffic.
Intermediate patch/restore results come from the hash-bound runner's completed
checks. Its final stored NVM bytes were independently compared here.

The checks do not prove physical typing, knob rotation in either direction,
actual LED appearance, restart persistence or power-loss behavior. Those
remain separate device tests. Offline builds and CPU/host models likewise do
not establish those physical results.
