# State summary — AK820 beta.5 completion, 2026-10-31

Read-only consolidation; no source or hardware changes made in this step.

## Ownership and activity

- Active checkout `/home/agent/work/ak820`, branch `main` @ `78dc69e6`, intentionally dirty (firmware, build utils, tests, installer, EN/RU docs). Preserve all.
- Previous session `cmvwpgtc00v4qn7015hjg87pw` ("Завершение прошивки AK820") idle, 0 pending — its work is transferred here by owner decision (full transfer to this session).
- No builds, containers (except `happier-server`), or reviewer processes running. Disk 147G free.
- `qmk-8051-ak820/core` and all `/home/agent/ak820-*` evidence trees: preserve.
- HANDOFF: `/home/agent/ak820-profile-handoff-20261031/HANDOFF.md` (never delete); transfer manifests verified per `worktree-verify.json`/`evidence-verify.json`.

## Optimization ledger state (`qmk-8051-ak820/.build/optimization-ledger.json`)

- Retained in primary, unqualified: E3–E6, E8, E11, E17, E19, E20.
- Rejected: E7, E9, E10, E12–E16, E18, E22.
- E21 (Combo flush argument removal): measured, not integrated; fresh isolated qualification at `/home/agent/ak820-code-exp-21-qualified` — main endpoint `0xc71d` (30 bytes over `0xc6ff`), pointer offline stack gate 167/185 with recorded assumptions, source Combo SHA256 `f7beb0c35145101eff306a4b2e68e44f992c3f5605e78f38c6387c70dbecee9c`; host Combo/Auto Shift tests and reviews in `/home/agent/ak820-code-exp-21/evidence/` and subagent artifact `93a4d9d0-d211-4f52-a0ac-ad48be1e270d_worker_output.md`.
- E24 (encoder lookup specialization): in progress at `/home/agent/ak820-code-exp-24`, claimed main `0xc751` vs clean `0xc754`; reviewer `f968fa53-...`; discrepancy: `_keycode_at_encodermap_location_raw` absent from exp21 main CSEG map — resolve before any application.
- New lead from this session: cross-module exact RET-tail sharing — 50 candidate groups, greedy 25 groups / nominal 191 bytes (4-byte tails: `mov dpl,#0x01;ret` 42 sites/41 nominal; `mov dpl,#0x00;ret` 38/37; `movx a,@dptr;mov dpl,a;ret` 15/14; `mov dptr,#0x0000;ret` 12/11). Unmeasured; transform candidate, no extra stack.
- sloc-extended outliner: only 2 candidate groups, nominal 2 bytes — deprioritized.

## Qualification blockers known

- Pointer exact qualification `qmk-8051-ak820/.build/pointer-qualification-retry-CQxeiw0J/` exited 1: fixture calls `config.inspect()` without `build/build-report.json` (gates.log:8-18, configure_firmware.py:746). Fix fixture/contract, keep exact XDATA-map assertions; do not weaken gate. 36 prior suites passed; pointer CODE 40,361 bytes, top `0xc690`.
- Combined main baseline (with E19+E20): endpoint `0xc754`, 85 bytes over; with E21: `0xc71d`, 30 over.

## Plan items and owner decisions (docs/PROFILE-IMPROVEMENTS-PLAN.md + HANDOFF)

- In scope: runtime Leader timeout candidate qualification, successful-Combo Auto Shift opt-in (`AK820_COMBO_AUTOSHIFT`, host evidence only) qualification where used, Caps Word build-time gesture switches + optional double-left-Shift interval candidate, Mouse Keys build-time overrides, beta.3 backup/defaults + beta.4/4.1 strict migration, deferred: invalid key after Leader, failed-Combo Auto Shift, QSID 22 conflict (documented risk), custom builder.
- Owner authorized replacing public beta.5 tag/release when ready and all mandatory gates pass; preserve old release proof; verify published artifacts.
- Compatibility: only immediately preceding beta.
- Hardware: no writes/flashes without separate permission.

## Open questions for owner (not blocking progress)

1. Exposing candidate runtime Leader timeout in Vial/AK Configurator clients (currently not exposed) — needed to satisfy "runtime setting" request, or document as deferred?
2. Confirm the earlier "real, justified substantial saving" exception to the ≤10-bytes-overflow experiment policy — owner message of this session already authorizes additional experiments; record as controlling.
