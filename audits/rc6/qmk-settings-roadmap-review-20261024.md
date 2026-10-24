# QMK Settings roadmap review

Date: 2026-10-24. Scope: the current changes in `docs/ROADMAP.md`,
`docs/ru/ROADMAP.md`, `docs/CONFIGURATION.md` and
`docs/ru/CONFIGURATION.md`. Independent static review; no build or device test.

Decision: approved. No factual or translation findings remain in this scope.
The candidate list describes future work, not available build profiles.

## Evidence

- `keyboards/ajazz/ak820/rules.mk` disables QMK Settings, Magic, Leader,
  Space Cadet and dynamic macros. NKRO reporting remains enabled. The new
  candidates match those source settings. Recording dynamic macros differs
  from the 16 Vial macros configured in `config.h`.
- `quantum/qmk_settings.h` asserts a 36-byte `qmk_settings_t`. The structure
  contains saved values and also has a RAM instance. `qmk_settings.c` adds
  descriptors, persistence, callbacks and Magic keymap settings; 36 bytes is
  not the total feature cost. `builddefs/build_vial.mk:23-30` additionally
  enables Auto Shift and per-key/per-Combo hooks when QMK Settings is enabled.
- `quantum/dynamic_keymap.c:104-114` places QMK Settings before subsequent
  dynamic data. Lines 129-133 fix the compact Combo base at `0x658`. Adding
  the existing 36-byte structure shifts that base by `0x24`, failing the
  assertion with the compact layout unchanged. The roadmap correctly requires
  storage design and migration rather than enabling the flag alone.
- `qmk_settings.c` exposes Grave Escape, Combo, Auto Shift, One Shot,
  tapping, Mouse Keys, tap delay and Magic settings. Enabled handlers must
  actually consume any offered setting. Grave Escape and generic tap delays
  have consumers; disabled feature settings do not add their handlers.
- `ak820_tapping.c:62` uses a fixed 200 ms threshold;
  `ak820_combo.c:46` uses a fixed 40 ms threshold. Neither compact engine
  consumes QMK Settings. Configurable timing and fuller behavior therefore
  need separate work, as the roadmap states.
- English and Russian changes agree on availability, candidate scope,
  integration, persistence and unmeasured costs. The configuration guides
  correctly state that the current build lacks QMK Settings.

## Completeness boundary

The new rows make the former grouped candidates explicit and add Magic.
They do not claim a complete inventory of upstream QMK features. The final English and Russian changes include the requested inventory of
disabled, partially supported and build-only options before selecting
profiles. Runtime settings and build switches are separated from deliberately
excluded diagnostics. The earlier completeness suggestion is closed.

The final diff also removes Caps language switching and a Windows language
helper from both roadmaps, following the supplied scope decision that this
is configuration rather than future implementation work. Physical acceptance
and VialRGB persistence limits remain. No new firmware claim is introduced.

No firmware, built artifact, package or installed-state claim was validated
by a build or hardware action. No device commands were issued.
