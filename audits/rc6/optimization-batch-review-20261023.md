# Combined optimization review

Independent review, 2026-10-23. GO: code, completed offline evidence and
documentation agree. No blocking finding remains. This is a local
source/build verdict, not approval for a packed release or device update.

I reviewed the combined audit and its linked reports, source identities,
full build manifest, IHX, memory report and saved test evidence. I did not
author the implementation, compile, link, run a simulator or access USB.
Only this review and the separate verifier review were written by me.

The three current production files match the independently approved exact
candidates:

| File | SHA256 |
| --- | --- |
| `tmk_core/protocol/host.c` | `e8392d708749fa32b5b1fec3123ca1eb604ece1ef1c4b4ae5d18dace0d09b65c` |
| `keyboards/ajazz/ak820/ak820_rgb.c` | `810ac091fb9f0206ab6e6db86e6ab2f51a8003f647c64f35ebb8602db6d23415` |
| `quantum/process_keycode/process_rgb.c` | `2ddc67492d8c8e80f01b433a0d8ca00c3343dabe8f87f4ede82b3fdd991561a0` |

The prior host-driver, shared-report-tail, Breathing/arithmetic and RGB table
reviews remain applicable. This review checks their joint artifact and
evidence; it does not add overlapping private-probe savings together.

I independently rehashed all 465 source/toolchain records and all 76 artifact
records in `.build/rc6-optimization-batch-20261023/build-report.json`.
Toolchain-relative records were resolved under the pinned SDCC installation.
There were no mismatches; artifact sizes also match. Compiler identity is
4.4.0 #14620. The artifact is marked neither hardware-validated nor packed.

Independent IHX parsing checked record checksums, unique output addresses and
both supported code windows. The result is 39,144 CODE bytes: 37,285 main and
1,859 low, with highest address `0xC1CB`. Its SHA256 is
`4b68ae92d95538e4c0af1d445c723645b1d7f570b3ea206002d7521b45fe7ce3`.
The memory report confirms 2,067 XRAM bytes and 152 available stack bytes.
The stated 288-byte CODE saving against the 39,432-byte Breathing baseline,
four XRAM bytes saved, and 1,332/29 free CODE bytes in the two windows agree
with the artifact. Separate window capacity cannot be exchanged.

All seven base suites have successful saved logs whose hashes I checked.
The package suite reports two skips. The production-C RGB report passes
16,777,216 compact HSV cases and reactive/Direct checks, with all seven
recorded source hashes matching current files. Its Breathing sweep reports
69 levels and maximum phase step two. This remains host evidence.

All focused CPU reports bind to the combined IHX hash above. The Breathing
suite passes all 161 supported helper inputs and 50 complete 82-LED frames;
maximum full-curve channel error is one. Its recorded runner/source,
linked metadata and simulator hashes match current files. The host report
fixture has 25 passing assertions with actual values equal to expected
values, and uses eight tested foreground stack bytes.

The combined RGB CPU report compares the expected baseline hash
`ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`
against this combined image. It passes 200 events at each of five seeds per
image, comparing returns, config, modifiers, dirty/time/render state and 82
reactive ages. Both images pass another 200 exact callback ID/count checks.
The separately reviewed parametrized verifier preserves the private probe's
matrix and corrected simulated-ROM fixture. Foreground stack use is 20 bytes
for baseline state runs and 22 for combined state runs; capture runs use 20
in both. These results close the pending combined RGB comparison gate.

Available stack and tested peaks do not establish a global bound with
interrupts. No physical RGB smoothness, timing, USB behavior, EEPROM durability,
power-loss behavior or installed-device change follows from these tests.
The installed firmware remains separate from this local artifact.

## Documentation closure

The final combined audit, English and Russian STATUS and ROADMAP pages
agree on the current build, hashes, measurements, completed CPU tests and
two skipped package checks. README translations keep local source changes
separate from installed firmware. The earlier Breathing CPU evidence is
now identified as belonging to the earlier build. The outdated running and
pending-RGB descriptions were replaced. These documentation follow-ups are
closed; no firmware correction or additional test was needed.
