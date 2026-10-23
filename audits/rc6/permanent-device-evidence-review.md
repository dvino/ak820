# RC6 installed-device evidence review

Date: 2026-10-23. Independent, read-only review of the first permanent RC6
installation evidence and the private encoder probe. No device transport or
probe was executed during this review. No firmware or settings were changed.

## Installation evidence: PASS within the stated scope

Reviewed `first-permanent-device-check.json`, the private
`host/runs/20261023-rc6-final-ready/flash-permanent-1792745330711461600.json`,
and `verification.json`, `boot-status.json`, and `readback/report.json` under
`host/runs/20261023T084938.227000Z-rc6-permanent-postflash-readonly/`.

Independently read the saved binary files and checked their hashes and ranges:

- Permanent payload: 51,136 bytes; SHA256
  `f90a40dcad7364f2278fa5daf2bfa444060140a71401b2c4595bb035aff6aebe`.
- Captured ROM: 65,536 bytes; SHA256
  `20608dac9d21320ca113b97a6a398c473f3d188a14a6ea0fd8ff86240fc883b1`.
- The whole application window, `[0x2800, 0xEFC0)`, equals the payload,
  including initial NVM and the manifest.
- Protected ranges `[0, 0x2800)` and `[0xEFC0, 0x10000)` equal the private
  archived `stock-full.bin`. That reference has SHA256
  `03c6bd3351f272c855b9bc736d597170f694b5260b2001d1fc9cbfba8b382994`,
  matching the packer's stock reference constant. No private bytes are reproduced.

The flash log records one loader transfer, checksum acceptance and restart.
That log alone would not establish startup. The later capture supplies the
readback, and two stage-3 heartbeat samples show main-loop progress. FD01 reports
no storage failure, dirty page, active batch or prior IAP failure. The summary
attributes ordinary typing, Backspace, Enter, Shift and Ctrl to the owner;
these are an owner report, not captured OS input events.

Reviewed current `README.md`, `docs/STATUS.md`, `docs/ru/README.md` and
`docs/ru/STATUS.md`. Their installation claims agree with this evidence. The
RC5 observations are under explicit pre-installation headings. The frozen
offline build/review fields remain historical and were not changed here.
Cold boot, setting changes, encoder remapping, reactive lighting and recovery
after a failed update remain unverified. The initial NVM match does not prove
that a later settings write will survive a power cycle.

## Private encoder probe: static review PASS with operating conditions

Reviewed `host/runs/rc6_encoder_probe.py` and the relevant packer, diagnostic,
transport and Vial encoder handlers. No safety blocker was found in the planned
mutation/restore order. The root reports offline compilation and default dry-run
PASS; this reviewer did not rerun the probe or open USB.

The default path returns before device selection. Execution requires both
explicit flags, the exact permanent payload hash, a bound diagnostic IHX/MAP,
one selected application and a complete matching live CODE/manifest capture.
Before the setter it verifies a stable NVM/journal snapshot, valid NVM, an empty
journal header, healthy storage and all twelve encoder values. The setter's
clockwise selector and getter ordering agree with `quantum/vial.c`.

The temporary change is limited to layer 0, encoder 0, clockwise. Restoration
is attempted only after the echoed setter packet, FD01, all encoder getters,
full durable NVM and clean journal header pass. A fault stops without automatic
retry, restore, reset or recovery. The final check requires the original NVM
and encoder values. Journal data may retain the latest transaction; the script
correctly requires an empty header rather than falsely requiring identical
journal data. An echoed setter alone is not treated as proof of persistence.

Fresh owner consent for the settings write is still required. Its scope must
cover the temporary setter and its one restoration, with all configurators
closed and no encoder rotation until restoration is verified. A failed check
may leave the temporary setting or a storage fault: preserve evidence and stop
for review rather than promise automatic restoration. A successful run would
prove a live durable change and restoration only; physical encoder input and
cold-power persistence still need their own evidence.
