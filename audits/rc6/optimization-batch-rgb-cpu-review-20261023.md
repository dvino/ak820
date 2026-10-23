# Combined RGB CPU check review

Independent code review, 2026-10-23. The parametrized CPU check is suitable
for the planned offline comparison. No code findings block execution.
The completed combined-image evidence also passes, as recorded below.

Reviewed file:
`qmk-8051-ak820/.build/rc6-optimization-batch-verification-20261023/rgb_cpu.py`.
Compared it directly with the completed private RGB table probe's
`cpu_probe.py`, and inspected the imported emitted-test runner during the
preceding independent review. No compiler, simulator or USB operation was
run by this reviewer; no production files were changed.

The adaptation preserves the original matrix: 25 keycodes, both edges and
four Shift states give 200 events per seed and image. The five seeds remain
0, 1, 127, 240 and 255. Each event compares the boolean return, eight config
bytes, real modifiers, dirty flag, change timestamp, rendering flag and 82
reactive ages. Baseline and candidate observations are compared after both
complete. Each image also gets 200 callback checks against an explicit
expected action and call count. The corrected three-byte jumps into separate
simulated-ROM capture stubs are preserved.

At this file location, `parents[2]` resolves to the QMK directory, so the
runner path is correct. CLI paths select existing linked inputs and a private
output directory. The script imports the existing CPU runner and invokes
the C52 simulator; it contains no build, programmer or USB call. Reports
record resolved input paths and both IHX hashes. Check those against the
completed build reports before accepting results. Keep input files stable
during the run and use a fresh output directory so an older PASS cannot be
mistaken for a failed rerun. Run normal Python without `-O`, because the
inherited assertions enforce the comparisons.

The inherited oracle targets the current key-up RGB profile, three-byte
generic pointer with XDATA tag zero, pressed byte at offset five and the
current keycode range. It is not a generic test for other layouts or trigger
profiles. Real-action state runs execute linked code; callback runs replace
only simulated action entries. State comparison can preserve a shared
baseline bug; the explicit callback oracle adds an independent action check.
The limited keycode/state sample complements the exhaustive host dispatch
test. It does not replace it. CPU results cover no physical USB, EEPROM,
LED timing, interrupts or whole-firmware worst-case stack behavior.

## Completed combined run

The saved `cpu-rgb/rgb-cpu-report.json` records PASS for the matrix described
above. Its resolved paths select the optimized-breathing baseline and the
new combined build. The baseline IHX hash is
`ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`;
the combined hash is
`4b68ae92d95538e4c0af1d445c723645b1d7f570b3ea206002d7521b45fe7ce3`.
Both agree with the actual reviewed images. Real-action foreground stack use
is 20 bytes for baseline and 22 for combined; capture runs use 20 for both.
The accompanying `optimization-batch-rgb-cpu-20261023.md` agrees with the
report and keeps the CPU and hardware boundaries clear. No findings remain
for this verifier or this run's recorded result.
