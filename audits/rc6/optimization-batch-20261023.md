# Combined optimization build

Date: 2026-10-23. This is a local build and offline verification record.
The installed keyboard firmware is unchanged. No USB operation was performed.

The full build contains the typed host-driver pointer, shared system/consumer
report tail, smoother Breathing with bounded arithmetic, and RGB action table.
The individual source changes passed independent review before integration.
Six layers, sixteen macros and the supported feature configuration remain.

Build directory inside QMK: `.build/rc6-optimization-batch-20261023`.
Pinned compiler: SDCC 4.4.0 #14620. The full builder exited successfully.
The input verifier subsequently accepted all 465 source/toolchain records and
76 artifact records against the current files.

| Measurement | Previous Breathing build | Combined build |
| --- | ---: | ---: |
| CODE bytes | 39,432 | 39,144 |
| Main CODE window | 37,573 | 37,285 |
| Low CODE window | 1,859 | 1,859 |
| XRAM bytes | 2,071 | 2,067 |
| Stack space available | 152 | 152 |

The combined image saves 288 CODE bytes and four XRAM bytes against the
previous Breathing build. Against the installed candidate's 39,347 CODE
bytes, it saves 203 bytes while including the new Breathing curve. Free CODE
space is 1,361 bytes: 1,332 in the main window and 29 in the low window.
Free space in one window cannot substitute for space in the other.
Stack capacity is not a proof of worst-case stack use with interrupts.

IHX SHA256:
`4b68ae92d95538e4c0af1d445c723645b1d7f570b3ea206002d7521b45fe7ce3`.
Highest linked address: `0xC1CB`. No packed update was produced.

The seven base offline suites pass; their report is
`host/runs/20261023-optimization-batch-offline.json`. The production-C RGB
harness passes all 16,777,216 compact HSV inputs and reactive/Direct checks.
Its Breathing phase sweep finds 69 levels versus 20 previously and a maximum
step of two versus eight. Its report is
`host/runs/20261023-optimization-batch-rgb-host.json`.

The package suite reports 72 tests and two skips: the POSIX SDCC/8051 boot
regression cannot run on its Windows host, and the real-preprocessor check
needs `AK820_SDCC_BIN`. These checks were not executed by this base run.

The focused linked C52 Breathing suite passes all 161 supported helper inputs
and 50 complete 82-LED frames. Maximum channel error against the independent
full curve is one. Results are in
`.build/rc6-optimization-batch-breathing-cpu-20261023/results.json` inside QMK.
The focused host-driver/report-tail CPU fixture passes 25 assertions against
this IHX; its tested stack use is eight bytes. Results are in
`.build/rc6-optimization-batch-host-cpu-20261023` inside QMK.

The combined RGB action CPU comparison passes 200 events for each of five
state seeds and 200 callback cases in each image. Tested foreground stack use
is 20 bytes in the baseline and 22 in the combined image. Results are in
`.build/rc6-optimization-batch-verification-20261023/cpu-rgb/rgb-cpu-report.json`
inside QMK. Independent code and artifact review passed; final documentation
closure is pending in `optimization-batch-review-20261023.md`.
CPU and host results do not prove physical smoothness, LED timing,
USB behavior, EEPROM durability or a global stack bound. No device test,
flash, commit or publication is authorized by this report.
