# Shared extra-report tail probe, 2026-10-23

This probe measures whether a private helper saves space in `host.c` after
the private driver-pointer and Breathing changes. It changes no production
source and performs no USB or device operation.

## Candidate and required behavior

The candidate puts the null-driver check, three-byte report construction and
`send_extra` call in `host_extra_send(report_id, usage)`. Each public function
keeps its own duplicate check and last-usage update. The consumer function
keeps its Bluetooth branch before the helper call. The system function gains
no Bluetooth branch. A null driver must still update each last-usage value.

`host_driver_t`, public function signatures and callback pointer types stay
unchanged. System reports keep ID 3, consumer reports keep ID 4, and both keep
the complete 16-bit usage. The callback receives the same generic pointer to a
temporary `report_extra_t`, valid for the duration of the synchronous call.

The helper adds an extra call and parameter setup. These costs can offset the
saved duplicate instructions. Static inspection cannot establish a saving.

## Measurement

Private files are in
`qmk-8051-ak820/.build/rc6-host-extra-tail-probe-20261023/`.
The prepared `probe.py` compiles copied control and candidate translation
units with the saved flags. It then uses the frozen full-build assembly from
`rc6-optimized-breathing-20261023`, runs the existing reachability and outlining
passes, and links each variant. The control must reproduce the baseline IHX
file exactly before the candidate is linked. This compares the candidate with
the combined baseline; it does not add savings from separate experiments.

The canonical builder completed before this probe started. The control source
SHA256 matched its source manifest, and the linked control reproduced its IHX
file byte for byte. Both copied translation units compiled successfully with
the pinned SDCC 4.4.0 compiler. The compile logs contain no diagnostics.

| Measurement | Control | Candidate | Change |
| --- | ---: | ---: | ---: |
| Raw host translation-unit CODE | 663 | 633 | -30 |
| Linked CODE | 39,432 | 39,402 | -30 |
| Main CODE | 37,573 | 37,543 | -30 |
| Low CODE | 1,859 | 1,859 | 0 |
| XRAM | 2,071 | 2,071 | 0 |
| Available stack capacity | 152 | 152 | 0 |

Both links selected 32 outlining helpers at 221 sites, with a nominal saving
of 1,234 bytes. The measured 30-byte saving is against the combined baseline.

- Control IHX SHA256: `ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`.
- Candidate IHX SHA256: `ce0f5cdbed5e73f64006742364b282c5f6cf53c1f3e77037581783af9096cd42`.
- Control source SHA256: `74a7c83be7e335e3c6c1eeca24538758dcd6ba52d335b138b478e0a4b9ee22ad`.
- Candidate source SHA256: `e8392d708749fa32b5b1fec3123ca1eb604ece1ef1c4b4ae5d18dace0d09b65c`.

## CPU checks and limits

The same focused uCsim C52 fixture passed 25 assertions on each linked image.
It checked callback pointer tags, IDs 3 and 4, full 16-bit usage `0x1234`,
independent last-usage values, zero releases, null-driver updates and duplicate
suppression after restoring the driver. The fixture writes simulated memory
only. Results are saved in `cpu-control/results.json` and
`cpu-candidate/results.json` in the private probe directory.

All 25 named assertions passed on both images:

| Checks | Assertion names |
| --- | --- |
| Null driver | `null-led`, `null-callback-count`, `null-system-state`, `null-consumer-state` |
| Existing keyboard callback | `callback-led`, `keyboard-pointer`, `keyboard-payload`, `keyboard-count` |
| System callback | `system-duplicate`, `system-tag`, `system-payload`, `system-count` |
| Consumer callback | `consumer-duplicate`, `consumer-tag`, `consumer-payload`, `consumer-count`, `consumer-release` |
| Full usage and separate state | `system-full-usage`, `independent-consumer-state`, `system-release` |
| Null update and restore | `null-new-system-state`, `null-new-consumer-state`, `null-no-new-callback`, `null-updated-duplicates`, `restore-driver` |

The candidate reached SP 111 and used eight stack bytes in this fixture.
This is an observed path, not a bound for firmware interrupt nesting.
Bluetooth behavior on other boards has only been checked by reading the
unchanged control flow. No live protocol, USB, storage, physical keyboard or
other-board build was tested. No packed firmware image was produced.

The first launch accidentally used the default WSL distribution. It failed
before running Python because that distribution's VHDX path was missing.
The corrected run explicitly used Ubuntu and passed; this was a tool-launch
failure, not a firmware failure.

Reproduce in the repository's `qmk-8051-ak820` directory with explicit Ubuntu:

```text
rtk proxy wsl -d Ubuntu -- bash -lc 'cd /mnt/c/Users/vinok/git/AK820-git/qmk-8051-ak820 && python3 .build/rc6-host-extra-tail-probe-20261023/probe.py'
```

The script refuses to overwrite its existing control and candidate folders.
Preserve this run before choosing a new output path for another measurement.
Independent review passed: [host-extra-tail-review-20261023.md](host-extra-tail-review-20261023.md).
The exact candidate was integrated into the source. This does not approve
hardware flashing; a combined build still needs its own resource checks.
