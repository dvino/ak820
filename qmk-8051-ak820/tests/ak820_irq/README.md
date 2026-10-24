# Offline IRQ checks

Run from the QMK tree after building the image:

```sh
python3 tests/ak820_irq/run.py \
  --build-dir /path/to/build \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 \
  --stock-rom /path/to/private/before-full-rom.bin \
  --output-dir /path/to/irq-results \
  --main-sample-bytes 56
```

The OEM reference stays outside the repository. The packer's native-image
validation checks its supported code variant and protected regions. Exact
wrapper instructions are checked separately.

The shared stack analyzer checks relocated listing bytes against the IHX and
bounds every IRQ callback path. Unknown transfers, recursion, unbalanced stack
use and unproved indirect dispatch fail the check. Each OEM wrapper adds 17
bytes: two for the hardware return address, 13 saved registers and two for the
callback call. All 15 ordered nonempty subsets of Timer0, USB and LED are
bounded. The largest bound adds all three callbacks and their wrappers; it
does not depend on a particular number or ordering of priority levels.

This uses the MCS51 architectural rule that an interrupt cannot preempt an
active interrupt of equal or higher priority. RETI ends that active state;
ordinary RET does not. See the original [Intel MCS-51 manual, printed pages
3-24 and 3-25](https://bitsavers.trailing-edge.com/components/intel/8051/MCS-51_Users_Manual_Feb94.pdf).
The checker rejects priority writes and early RETI in reachable callbacks.
The target is assumed to follow these interrupt and instruction semantics.
This is an explicit architectural assumption, not physical VS11 validation.

The CPU fixture injects all 15 source orderings at callback entry and runs the
actual OEM wrappers and linked callbacks. Each nested return must preserve
bank0 R0..R7, ACC, B, DPTR, PSW and SP. A reserved foreground stack canary must
also survive. Banks 1–3 can contain compiler data and are not part of the
register preservation contract. Injection at entry exercises preservation;
the static sum covers interrupts arriving at other callback phases.

The emitted checks also reject unexpected source enables and register-bank
changes. Shared timer/USB helpers must run under their initialization
mask for both long and page-relative call/jump forms. Initialization jumps
are rejected. Timer/USB private storage must have no overlay or conflicting
allocation. The LED IRQ has no C local storage. The LED selector
is executed for all 256 input values. Values 0x10–0x1f retain their native
meaning, and the mask limits the table path to its 16 entries.

`results.json` binds results to the image, map, runner and stack analyzer.
The foreground reservation is a sample, not a global bound. Combine the
static IRQ sum with the separate main-path and startup bounds for a whole
image stack result. USB ACK effects and hardware entry frames are supplied
by the fixture. Peripheral timing, LED DMA, physical key scanning and actual
silicon interrupt delivery remain outside these offline checks. No device is
opened or written.
