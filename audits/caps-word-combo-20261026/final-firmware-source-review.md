# Final firmware source review

2026-10-26. Independent source review after deferring W pulsing in every profile. No actionable findings remain in this scope. Fresh exact-image build and runtime qualification is pending and is not approved by this report.

The following files were compared as bytes against Git HEAD and match exactly: `ak820_rgb.c`, `ak820_indicators.c`, `quantum/action_util.c`, `quantum/action_util.h`, the RGB harness, OS-indicator host runner and OS-indicator test include. `ak820_gui_pulse.h` is absent. A source search found no remaining pulse getter, pulse-state getter or waveform test marker. The previous W source/host review describes only the deferred candidate.

The external preservation hashes match `deferred-w-pulse.md`: `source.patch` is `a454b80fdb6999dddaac7e80526d278daaf4945f5e6ff249f3215a4a901b923e`, and the removed header is `63f1e0a93f83cdaacb67b2a17c57ac9901f60c9b32c9841c791609a00017cd76`. Existing GUI lock in game and MMO remains independent of the deferred indicator change.

Current MAIN adds Auto Shift to the seven-feature reference composition and excludes GUI lock. Other profile compositions retain their existing definitions. The CRC change against HEAD consists solely of the SDCC `AK820LOW` codeseg pragma. The complete CRC source is byte-identical to the preserved AS-low probe, SHA256 `53cb7272cfba994c12fbc2d7390e1a85c607d7580d55bf566f986b576ba57675`. Its algorithm, naked assembly ABI and lack of additional stack/calls are unchanged by this placement directive.

The preserved probe records 1,024 differential CPU cases for lengths 0–255 with ABI/canary checks, and a separate exact-image runtime result of 160/167 stack bytes for IHX `b6040e965dfa30a22049bec5591ff7ab074a89000d973f22f9f3b08736a33031`. Those CPU cases were not rerun in this review. The source identity match supports reuse of the CRC implementation assessment; the old image's size, stack and interrupt proof cannot qualify pending new images.

The frozen beta.2 catalog was independently transformed into a source-only view and parsed with the actual current AS MAIN definition. All 13 images were accepted. Old MAIN retains QSID list `[1, 2, 7, 18, 19]`, no macro Layer-Tap capability and no Caps Word Combo action capability. Current and historical validation remain separate.

The inspected English and Russian STATUS text states that W pulsing is deferred in all profiles, MAIN excludes GUI lock, and fresh ten-profile qualification is pending. Current feature text describes Auto Shift in MAIN and typing without claiming W pulsing. Documentation was still subject to its final update; this inspection does not approve later edits or generated catalogs/policies.

No firmware build, device command, flash, setting write, commit or publication occurred in this review. Only this report and an applicability note on the earlier W review were written.
