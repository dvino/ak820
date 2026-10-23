# Breathing interpolation review, 2026-10-23

Decision: proceed to an isolated SDCC compile and full link. This review does
not approve a release, a commit, or a device update. No blocking defect was
found in the supported brightness range, 0 through 160.

The reviewer did not author the change. Review covered `ak820_rgb.c`, the host
RGB harness and runner, `color.c`, the CIE tables, and the saved host report
`host/runs/20261023-breathing-host.json`. All seven source hashes in that
report match the files reviewed. The reviewer read the report but did not
rerun a build or test and did not access USB.

The earlier compiled source comments in
`qmk-8051-ak820/.build/rc6-candidate-erase-20261023/obj_ajazz_ak820_vial/keyboards/ajazz/ak820/ak820_rgb.asm`
show the old sine scaling and `hsv_to_rgb_into(hsv, true, &rgb)` call. This
separates the small breathing change from earlier uncommitted reactive work.

The new path applies CIE once to the frame value, then disables CIE in the
HSV converter only for Breathing. It does not apply the curve twice. Other
effects retain their previous conversion. The full-CIE build selects the
256-entry table directly. Without CIE, the helper and its call are omitted
and conversion remains unchanged. These alternate builds were checked by
reading the source, not by compiling them.

For supported values, the compact interpolation uses monotone table entries
and a 16-bit product. Its largest possible product is 36 times 7, so it cannot
overflow 16 bits; its result stays within the two selected table values.
Black remains zero. The renderer still processes at most eight LEDs in one
task and flushes after all 82. Interpolation runs only when a new breathing
frame begins, before the first batch.

The host report records 69 red-channel levels instead of 20, maximum phase
step 2, and maximum error 1 against the full CIE table. The harness sweeps all
256 phases at configured brightness 160 and checks all 82 LED outputs. It
also retains reactive transition tests and the exhaustive 16,777,216-case
compact HSV comparison. These are meaningful host checks, but the breathing
sweep uses fully saturated red and does not independently exercise every hue,
saturation, brightness, or build option. The phase-step assertion allows 2;
the error assertion also allows 2, although this run measured 1. The harness
does not measure the previous path's maximum phase step of 8.

Two limits must remain explicit:

- The helper is not a general full-range accurate interpolator. The compact
  table ends with samples at 240 and 255. Values 240 through 247 interpolate
  toward the final sample over eight steps, and 248 through 255 return 255.
  The supported renderer caps brightness at 160, so it cannot reach that
  range. Claims of error at most 1 must retain the tested bound.
- Lower CPU cost is a hypothesis. One interpolation per frame replaces many
  table conversions, but the per-LED mode-dependent Boolean can add work.
  SDCC output, linked size and CPU timing are still needed to judge the cost.

Host output does not prove smoother light, USB timing, DMA behavior, or any
installed-device behavior.

## Expanded checks and documentation follow-up

The reviewer checked the expanded harness and
`host/runs/20261023-breathing-host-expanded.json`. All seven hashes match the
current files. The added checks cover six hues, three saturations, four
brightness values (0, 8, 80, 160), four speeds (0, 96, 224, 255), and 2048
frames per combination. They compare all three channels against the
independent historical full-CIE converter with tolerance 2, compare LED 0
and LED 81, and cross timer wrap. This closes the earlier limited-color test
qualification. It still does not compile alternate full-CIE/no-CIE builds.
The original saturated-red sweep separately measures error 1 and 69 levels.

The source comment now states the brightness cap and irregular final table
interval. README, STATUS and CONFIGURATION and their Russian translations
separate the local source change from the installed candidate and attribute
the reactive-light observation to the owner. That closes the missing-docs
qualification. Final linked size and CPU evidence remain pending.

The final follow-up closes both documentation precision points. The harness
now calculates the old maximum step, including wrap, and records the measured
maximum channel error across the broader color matrix. All seven hashes in
`host/runs/20261023-breathing-host-final.json` match the files reviewed. That
report records 69 levels versus 20, step 2 versus 8, saturated-red error 1
and color-matrix error 1. Both STATUS translations link this final evidence.
Their reported error 1 is now supported by the broader recorded measurement,
although the regression assertion deliberately allows tolerance 2.

No breathing review findings remain open for the supported compact-CIE
configuration. The full-CIE/no-CIE options still have static review only;
the above-160 limitation remains, and no device smoothness or timing claim
is approved. Combined host-pointer build/CPU evidence is outside this
bounded breathing review and must be covered by the root's integration
record and its independent review.
