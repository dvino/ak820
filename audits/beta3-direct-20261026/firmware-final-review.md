# Final firmware source review

Date: 2026-10-26. Base: `b35b77cddbefdb509058f1fbaaeafaa3982ce172`.

## Decision

No blocking firmware source defect was found in the reviewed production diff.
The current GUI-lock W optimization is suitable for the exact-image qualification
now in progress. This is an independent source and retained-evidence review,
not final release approval. No source or test changes, builds or device actions
were performed in this review.

Release remains blocked until the fresh ten-profile qualification, generated
catalogs and policy/status reconciliation are complete, and the required actual
alpha.2 saved-ROM fixture is available. Component results do not replace each
configured image's foreground/startup/IRQ stack proof and full regression gates.
Pending STATUS and catalog updates were known integration work at review time.

## GUI-lock W optimization

`ak820_indicators.c` keeps the private timestamp and phase in four DATA bytes
and the started flag in bit storage. Its phase accumulator remains in 0..1999:
elapsed time is reduced modulo 2000 before addition, so neither the phase sum
nor its single final subtraction overflows. Unsigned timer subtraction handles
the ordinary 16-bit timer wrap; this is not a claim that arbitrary gaps of one
or more full timer periods preserve wall-clock phase.

The target `gui_pulse_angle` is a call-free naked leaf. It changes only A, B,
DPTR and arithmetic flags; R0..R7 remain intact for same-translation-unit callers.
Repeated subtraction forms the quotient by 125. The failed subtraction's low
byte is restored modulo 256, producing the remainder even when the input high
byte is nonzero. For all remainders 0..124, `floor(131*r/1024)` equals
`floor(16*r/125)`. Two rotates and the mask select the product shifted right ten
bits; adding the quotient contribution implements the documented angle with
byte wrap. The input is bounded to 1999, so there are at most 15 successful
subtractions. No division runtime helper or additional stack frame is needed.

The reviewed current source hashes match `optimization/w-pulse/source-hashes.json`.
The retained final linked report identifies image
`5351cfafa6eb8bc55272c55e67f86d60ab0dac04809cbe3f25df14c2137f5005`,
contains 17 passing tests, and includes all 2000 angle inputs with R0..R7
preservation. The host report covers five fixture variants; its source guard
difference is explicitly recorded in the source-hash report. Neither report
claims hardware validation or qualifies another linked image.

The indicator behavior agrees with `docs/INDICATORS.md`: upper active/default
layers take priority, GUI lock pulses only at the base layer, and suspend or an
unconfigured USB state clears the channels and resets pulse startup. C and OS
retain independent component bytes. Shared slot intensity is the union of W
and OS activity. The shared waveform retains the existing 256-phase arithmetic;
its trough is value 1, consistent with the linked observations.

## Direct transaction and native DMA

The active logical palette remains 82 HSV triples. The separate 246-byte stage
accepts only sequential coverage or exact normalized duplicates; bounds and ID
checks precede staging writes. Commit requires all 82 colors, copies the logical
palette, advances generation, and then either finishes while invisible or begins
bounded conversion. Accepted commit retries do not publish again. Legacy fastset
cancels an unfinished upload, advances generation, and cannot mutate staging
after acceptance. Generation-qualified reads operate on the foreground-owned
logical palette; the ISR consumes only staging and never edits that palette.

Conversion handles eight LEDs per task call and reuses each fully read HSV triple
as RGB. QUEUED and PUBLISH prevent foreground staging reuse and normal renderer
writes. The IRQ changes QUEUED to PUBLISH only at row zero, writes only mapped
key slots before their native transfer, and releases the stage only after row
15's native transfer. The inverse map excludes the independent indicators.
Suspend and USB keyboard reset cancel pending work while preserving the logical
palette. The single-core foreground/IRQ ownership makes the volatile one-byte
state transitions adequate for this protocol; no multi-byte shared index is
used by the ISR.

The OEM wrapper contract saves ACC, B, DPTR, PSW and R0..R7. Publication preserves
the row register R6 and uses no C/static-parameter helper. The native four groups
of eight MOVX reads, E_DIS/PSW.P setup, inter-group NOPs and key-input settling
sequence remain in place. Source preservation does not prove peripheral timing:
the new per-row work still requires physical LED/DMA validation.

Direct packets are intercepted in the production raw task before entering the
NVM transaction path. The fixed raw buffer remains transport-owned and the
specialized VIA/Vial/VialRGB entry points reject an incorrect buffer or length.
The EN/RU Direct guides agree with the source on packet offsets, brightness
normalization, timeout, generation, state ownership, retry behavior and RAM-only
storage. They distinguish logical commit from pending physical publication and
do not claim that host tests establish DMA behavior.

## Compact ABI leaves and retained evidence

The reviewed saturation leaves are the current A/B/DPTR-only implementations,
which preserve every GPR. The earlier rejected R6/R7 implementation is not the
production source. The slot writer intentionally uses caller-saved GPRs and has
both standalone and same-translation-unit caller evidence. It bounds the slot
before reading parameters, derives the native 0x0200 address correctly across
the carry boundary, and restores the LED interrupt-enable bit after its four
MOVX writes. Other interrupt wrappers' PSW restoration is part of its carry
preservation contract.

Retained records in `optimization/verified-components/` report:

| Component | Retained result | Scope limit |
| --- | --- | --- |
| Saturation | 131072 exhaustive CPU cases | Component image, not full runtime qualification |
| Slot writer | 8192 CPU cases | No interrupt-preemption simulation |
| Same-unit slot callers | 544 CPU cases | Checks full DMA and adjacent guards |
| Shared waveform | All 256 phases | Component CPU image |
| HSV kernel | 3473408 differential CPU cases and 544 exact-alias cases | Broader overlap extension retained separately in quick4 |
| Native arithmetic comparison | PASS | Host semantics and sanitizers, not SDCC ABI proof |

The HSV leaf reads all three source bytes before output writes, uses the
large-model XDATA parameter ABI, and retains compile-time byte-order selection.
Its cross-unit caller-saved-register contract differs from the private
same-unit saturation and W-angle leaves; these contracts were not conflated.

## Remaining admission checks

Root integration must bind the frozen source and final generated reports to the
canonical ten exact images, retain passing stack/IRQ gates before full suites,
and verify profile composition and image identities in catalogs. The W diagnostic
image and component CPU images are evidence of their stated scope only. The
actual alpha.2 saved-ROM fixture remains missing. No physical behavior, timing,
installation or live restoration was validated here. Final release approval is
withheld pending those requirements.
