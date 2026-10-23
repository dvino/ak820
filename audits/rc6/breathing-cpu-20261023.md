# Breathing CPU check, 2026-10-23

The linked compact-CIE firmware passes the focused offline breathing checks.
No keyboard was opened, reset or flashed. No firmware build was started by this
test task.

The tested image is `qmk-8051-ak820/.build/rc6-optimized-breathing-20261023/ajazz_ak820_vial.ihx`.
Its SHA256 is `ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`.
The runner is `qmk-8051-ak820/tests/ak820_breathing/run.py`. Its README gives the
reusable command. Private commands, logs, source and linked-metadata hashes, and
the JSON result are under `qmk-8051-ak820/.build/rc6-breathing-cpu-20261023/`.

The test calls the actual linked `breathing_cie` helper for every value from 0
through 160. Results are monotonic, black stays black and the maximum difference
from the independent existing 256-entry source curve is one. This comparison
does not use a second copy of the interpolation formula as its sole oracle.

The actual renderer produces 50 complete frames: ten phase values crossed with
red, green, blue, a partially saturated color and grayscale. Each frame checks
all 82 LED records. The expected HSV conversion uses the measured helper result
without a second CIE lookup; the complete-frame comparison therefore detects a
second brightness correction. The maximum sampled channel difference from full
CIE is one.

After the first task call exactly the first eight LED records change from the
sentinel value. Eleven calls finish all 82 records and clear the rendering flag.
Phase checks include 0, 1, 127, 128 and 255; phase 0 starts with a seeded value
that crosses the 16-bit phase wrap when production code adds its speed increment.
The source timer is called with a simulated count of `0x10020`; its 16-bit return
is `0x0020`. A frame starts across the corresponding 16-bit elapsed-time wrap.

The linked initial SP is `0x67`, with 152 bytes available. The largest observed
SP in these renderer calls is `0x79`, or 18 bytes above the initial value. The
helper-only run uses five bytes. These are scoped CPU measurements without IRQ
overlap, not a global firmware stack bound.

The fixture reuses the emitted-test initialization and only changes simulated
memory. Symbols come from the supplied map and relocated listings, without
hardcoded addresses for static variables or generated name suffixes. The runner
also rejects an image that occupies its simulator call-trampoline bytes.

The first test drafts had two fixture errors: prefix-overlapping observation
labels, and an expected nonzero DMA header for black. The runner now uses padded
labels and follows the driver's zero header for black. Both were test-fixture
corrections; firmware was not changed to make a test pass.

Full-CIE and no-CIE configurations were not compiled or executed here. Generic
C52 simulation checks instructions, ABI and simulated DMA memory. It does not
prove physical frame timing, visible smoothness, DMA transfer, USB behavior,
storage durability or the installed keyboard firmware. Independent review is
still required before a commit.
