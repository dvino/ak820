# Independent review of seven optional feature fixtures — 2026-10-26

Scope: read-only review of the seven named linked simulator fixtures and their shared feature/trace helpers. No firmware build, simulator run, USB command or implementation edit was performed. These source conclusions are separate from pending scoped and full ten-image result files.

## Result

No actionable weakening or hidden firmware failure was established in the reviewed changes. The revised cases preserve the enabled NKRO/Grave Escape checks and add concrete disabled-feature checks. Final acceptance still requires the scoped runs on the exact revised fixture bytes and then the complete profile suites.

## Evidence by change

- `ak820_emitted/run.py:76-98` ties `compiled_feature('nkro')` to the exact build report's IHX and MAP hashes and the linked `_actual_keyboard_report` allocation. The reviewed reports identify `main` and `typing` as NKRO `no` and `game` as NKRO `yes`; all three include named IHX/MAP artifact records. This makes the branches image-bound rather than selecting by profile name.
- `ak820_key_overrides/linked.py:76-89` retains the original two overlap cases. A persisted NKRO request in a compiled-out image now expects the 6KRO outgoing projection; an enabled image still requires NKRO output. The test continues to inspect replacement, independent owner and release.
- `ak820_dynamic_macro/linked.py:50-56` retains the physical-owner replay case in both variants and checks that a stale NKRO setting stays set when code is absent. The 32-byte HID breakpoint dump now addresses `Trace.report_address`, the outgoing projection captured by `ak820_tapping/emitted.py:10-20`, which is also the address checked by the trace parser. The old dump addressed `_actual_keyboard_report`, potentially a different allocation after production projection.
- `ak820_autoshift/linked.py:133-152` keeps bitmap and owner-cancellation expectations for NKRO-enabled images. In disabled images it writes the stale setting, checks an 8-byte report and retained setting, and requires the disabled NKRO control to leave the deferred owner active until physical release. The 6KRO expected report is explicit.
- `ak820_mousekeys/run.py:109-118` still requires NKRO mode change to release a mouse owner when compiled. Without NKRO it requires the held button to remain through the disabled control, verifies the mode bit stays clear, and requires physical release to clear the report.
- `ak820_mac_pc/linked.py:87-118` and `ak820_ctrl_gui/linked.py:79-111` preserve the original enabled-NKRO modifier bitmap traces. Their disabled branches check a rejected control, stale mode bit, 6KRO report encoding, modifier transformations and independent owner releases.
- `ak820_settings/linked.py:45-62,106-117` binds the Grave Escape decision to IHX/MAP hashes, configuration and the linked `_process_grave_esc` symbol. Enabled images retain the old Grave/Escape consumer output. Disabled images require the setting getter to preserve the chosen value while the compile-omitted handler produces no Grave/Escape usage and leaves Shift held. This is a negative behavior check, not a skipped case.

The inspected build reports are under `ak820-beta2-qualified-a-20261025/qmk-8051-ak820/.build/next-{main,game}-release2-certified` and `ak820-beta2-qualified-b-20261025/qmk-8051-ak820/.build/next-typing-release2-certified`. The prior game Dynamic Macro failure was in trace framing: actual replay checks matched, while 4 HID pointers and 2 parsed HID reports disagreed because the breakpoint dumped the wrong allocation. The new source aligns the breakpoint with the parser's outgoing address. A passing rerun is still required to close this specific failure.

SHA256 of the reviewed fixture source, in the order above: Key Overrides `f3599b9134a9432280d680cb1549c00972906392e40b68a104ff93880c890ca7`; Dynamic Macro `379b4eef5adbe9c4d863449542962af22e801a5998c7b4bbc40c602fc18f461d`; Auto Shift `05782b87bd65fd79f6b9bf6316cca0bea05c10b67cd5d15ff3b9a0f623c6f558`; Mouse Keys `913cec5edfd9aec865be55244fcf18545dc18d27d87803dd5da7907704e1df69`; Mac/PC `09dadeb2387e2ef6021712935566669aa9eb487163298894d54aec2bcb485bf1`; Ctrl/GUI `bdf4bc1d66c66fe9280aceb546fa4835d455c241524f28cb524e7c599893116d`; Settings `60c5c2a7ae93d9a107ab941bda6a5103f5f8a5b93af552c92ddacf007b886e69`.

## Mac/PC disabled-NKRO expectation correction

The v3 multios scoped run exposed a wrong new fixture expectation, not an observed firmware failure. `quantum/action_util.c:461-472` applies Mac/PC Alt/GUI transformation to the aggregate physical modifiers before Ctrl/GUI transformation. Therefore physical left Ctrl (`1`) becomes GUI (`8`) when Ctrl/GUI swap is active and stays `8` when Mac/PC is also active; Mac/PC does not turn it into Alt (`4`). The revised expectation at `ak820_mac_pc/linked.py:111` matches that order.

The revised negative case also adds a physical left Alt owner (`4`). Under both transforms, Ctrl and Alt together project as `8|1 = 9`; releasing Ctrl leaves transformed Alt as `1`, and releasing Alt clears it (`ak820_mac_pc/linked.py:104-116`). This strengthens the negative case: it checks both transforms and owner release without reducing the retained enabled-NKRO bitmap trace at lines 88-100. Source SHA256 of the revised Mac/PC fixture: `f9b981668fe5905d15a10898deeacb80ba12ea06a4712e9bcc5a55f3ede5d2bf`.

The v4 scoped simulator run had not completed at this read. Its exact result must be checked before calling the corrected expectation locally verified. The multios typed spill proof failure is separate and remains open.
