# Review of the local host-driver and Breathing build

2026-10-23. Independent read-only review after source integration. The reviewer
did not author the implementation or run a compiler, packer or device operation.
This review covers the guarded private pointer in `tmk_core/protocol/host.c`,
Breathing interpolation in `keyboards/ajazz/ak820/ak820_rgb.c`, its host harness,
the canonical build and the English/Russian README, STATUS, ROADMAP and
CONFIGURATION descriptions. Earlier unrelated working-tree changes are outside
this review.

Decision: the code and canonical artifact are suitable for continued local
candidate work. The documentation finding below is closed. This does
not approve a release, commit, live update or completion of the wider task.

## Independently checked evidence

- In Ubuntu WSL, `util.ak820_build_inputs.validate_inputs` accepted all 465
  canonical source/toolchain records against the current QMK tree and
  `../toolchains/sdcc-4.4.0`. The first reviewer invocation supplied the wrong
  toolchain root; correcting that command resolved its missing-file mismatch.
- Recomputed canonical IHX SHA256:
  `ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`.
  This matches the frozen combined image and its saved CPU report identity.
  Parsing actual IHX data gives 39,432 occupied bytes: 1,859 in
  `[0x28A0,0x3000)` and 37,573 in `[0x3027,0xC700)`, with none outside.
  Remaining capacity is 29 low and 1,044 main bytes. The MEM file gives
  2,071 XRAM bytes and 152 bytes available for stack. Stack capacity is not a
  worst-case execution or interrupt-overlap proof.
- The final MAP places the driver table at XDATA `0x0BA3`. The private pointer
  is board-guarded; public signatures and callback types remain generic.
  The stored table is the existing XDATA constructor, so dropping its generic
  space tag is valid here. A future CODE/IDATA constructor or concurrent
  replacement needs a fresh review. The getter is removed by DCE; its return
  conversion has translation-unit inspection, not linked execution evidence.
- The saved combined CPU evidence covers three emitted-path cases and eighteen
  focused host-driver observations. The host-only feature result covers 33
  cases. Exact canonical IHX equality transfers these existing machine-code
  checks to this build; it does not broaden their exercised paths. The initial
  host-fixture failure remains recorded and its report-ID expectations were
  corrected. Mouse callbacks are disabled in this configuration.
- All seven hashes in `host/runs/20261023-breathing-host-final.json` match
  current inputs. It records 69 versus 20 levels, maximum phase step 2 versus
  8, and measured red/color-matrix channel error 1. The assertions allow
  tolerance 2. The matrix includes colors, gray, brightness/speed choices and
  timer wrap. Interpolation runs once per frame and avoids double CIE
  application. Brightness is capped at 160; the irregular compact-table final
  interval is outside the supported range. Full-CIE/no-CIE builds have static
  review only.

README and STATUS distinguish the installed earlier candidate from this local
source/build. CONFIGURATION attributes working reactive light to the owner's
observation. STATUS correctly leaves the focused Breathing CPU fixture pending.
Host results do not prove visible smoothness, physical timing, DMA or device
behavior. The host-only saving is 49 CODE and one XRAM byte; combined Breathing
costs 85 CODE bytes over the earlier baseline, so it is not a net size saving.

The separate offline update-preparation component has its own independent
eight-test review in `general-update-preparation-review-20261023.md`. STATUS
accurately leaves delayed RGB save, live snapshot capture and GUI integration
unfinished. It makes no new live-updater claim.

## Finding and remaining limits

ROADMAP's current-evidence paragraph says combined Breathing CPU checks passed,
which can imply that the new focused Breathing CPU fixture has already passed.
Clarify both languages to identify the existing emitted/host-driver checks and
leave the new fixture pending until its report is available. This is a wording
finding, not a firmware defect. Closure requires rereading the revised paragraph.

Breathing-specific linked CPU execution was incomplete at the first checkpoint;
the follow-up below closes that evidence gap.
Physical input, USB timing, visible light, persistence, power loss and recovery
are outside this review. No USB write, reset, loader transition or flash was run.

## Focused CPU follow-up

The reviewer read the complete new `tests/ak820_breathing/run.py`, its README,
the reused emitted fixture's initialization/call/execution/observation paths,
`audits/rc6/breathing-cpu-20261023.md` and the saved result. No rerun or compiler
was needed. All five source hashes, all 66 linked metadata hashes and the
simulator hash were independently recomputed and match the report. Its image
identity is the exact canonical IHX above.

Both recorded groups pass: all 161 helper inputs and 50 complete 82-LED frames.
The independent 256-entry reference checks helper accuracy and monotonicity;
renderer expectations use those measured helper outputs and separately compare
with the full curve. Checks cover no second CIE application, the first eight
LED updates with untouched sentinels elsewhere, completion after eleven calls,
phase boundaries/wrap and the timer's 16-bit return across elapsed-time wrap.
The maximum observed stack increases are five helper bytes and eighteen renderer
bytes, without interrupt overlap. This supports the bounded linked execution
claim. Full-CIE/no-CIE variants, other brightness/speed combinations and physical
timing remain outside this fixture; the broader host matrix is separate evidence.

The revised EN/RU ROADMAP identifies the existing emitted/host-driver checks
explicitly, closing the original ambiguous wording. The reviewer also reread
the final EN/RU STATUS and ROADMAP updates: they accurately record the separate
focused Breathing PASS, 161 values, 50 frames and scoped stack limits. No code, artifact or
evidence-validity blocker remains for continued local candidate work.
