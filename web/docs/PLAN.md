Русский перевод: [План](ru/PLAN.md).

# AK820 Web implementation plan

This plan turns the agreed [requirements](REQUIREMENTS.md) into reviewable work. See [REVIEW.md](REVIEW.md) for the source reuse findings. It does not select the final UI foundation or authorize a live keyboard operation. Stage completion means the evidence exists; it does not prove installation or device behavior.

## 1. Test the Entropy prototype and settle recovery rules

**Work.** Start with Entropy's native Rust/egui editor and browser/Wasm path. Use recorded AK820 device replies to check the editor/model with a fake transport. Separately check the real browser WebHID permission flow and a read-only Feature Report request; recorded replies cannot test browser permissions or loader access. Do not reset, enter the loader, or write to the keyboard in this stage. Always compare a bounded Pipette baseline: its Pages build, required feature coverage and the same fixture failures. Develop a larger alternative prototype only if Entropy cannot meet a required function or its measured adaptation cost is unacceptable. Include Vialite only if it changes that decision. Keep the chosen base's appearance. Assess native loader feasibility independently and read-only.

Before implementation, define a safe OEM source image: required per-device bytes, protected regions, source validation, and how the source is tied to the connected keyboard. A saved recovery archive is not mandatory for installation, but safe source acquisition and protected-image validation are mandatory. If device identity is ambiguous, block writes and rollback. Do not issue reset, loader-transition, or write commands without explicit confirmation for that specific operation.

**Results.** Fixture-backed editor test, separate browser permission/read-request result, source revisions and license notes, loader feasibility report, and a recorded base choice. Record a separate project-image policy for custom builds. Do not weaken the existing AK820 native installer's exact alpha3 and personal-reference checks to accept custom images.

**Completion / stop.** Continue when the editor test and browser read-only proof succeed, one maintainable base is justified, and safe source/identity rules are concrete. Stop browser flashing work if the loader protocol, source bytes, protected regions, or device identity cannot be established safely. The native loader assessment can proceed independently.

## 2. Establish the shared client and project data

**Current groundwork.** The repository now has an offline development capability-catalog generator and verifier, plus the FD02 OS-indicator firmware protocol contract. These are partial foundations for this stage, not the generated release catalog, installed-image detector, or a user interface. The firmware indicator module also implements part of AKW-063; the desktop helper and OS-layout detection remain planned.

Use `web-dev` for the browser, `desktop-dev` for native development and
`desktop` for the native version prepared for release. Start the native branches
from a common reviewed base. Merge shared changes between development branches;
do not maintain copied implementations. CI must check both targets for shared
changes. Pages deployment uses approved browser revisions, not `desktop`.

**Work.** Add the selected base under `web/`, preserving upstream notices and recording local changes. Keep protocol/model, validation, firmware packaging, backup format, and UI concerns in clear modules. A possible layout is `web/src/{app,model,protocol,firmware,backup,release,help,platform}` with fixture and test data alongside the relevant module; adapt it to the chosen language instead of committing to TypeScript before the Entropy prototype decides that question. Reuse `tools/installer/settings_backup.py` and `settings_workflow.py` as behavioral references; port rather than depend on Python at runtime. Use `qmk-8051-ak820/util/pack_ak820.py` as the packaging reference and `qmk-8051-ak820/util/ak820_tool.py` for protocol behavior. Reuse release/configuration tooling for generated catalog and capability data.

Define bundle versioning and revocation data, prerelease policy, image-source policy, model identity, and capability metadata before screens depend on them. The catalog must distinguish released, development, and installed firmware capabilities. Generate the finite nine-package profile matrix and bilingual popup/help descriptions from the source registries; `work` is the default project package and excludes Mouse Keys and Mac/PC mapping. Keep historical CLI profiles out of the desktop selector. Show a package as installable only after its exact image qualifies. Add modules only where implementation, resource use, and ABI impact are supported by evidence; do not infer a need for MCU GETFEATURES without protocol evidence.

**Results.** Shared data contracts, custom-image project format and verifier, generated release/capability catalog, source map, license inventory, and fixtures. Demonstrate identical acceptance/rejection behavior for the JS/Rust packer and Python packer, including negative cases and exact output bytes. Validate schema and bundled references offline.

**Completion / stop.** No UI may enable a write from unverified metadata or a partial/ambiguous image. Stop if packers disagree, a negative fixture is accepted, or project-image policy cannot be checked independently of a warning.

## 3. Adapt the native client and browser in parallel

**Work.** If Entropy is selected, begin with its existing native client, then share the model, editors and validation with the browser/Wasm build. Work on native HID and browser WebHID in parallel after stage 2. If Pipette is selected, start with its browser version. Add exclusive device ownership, explicit selection when identity is not unique, live capability detection, full settings read, editors for supported layers, key and encoder mappings, macros, Combo and RGB, help, and RU/EN selection. Match AK820 behavior instead of copying unrelated Vial screens. Add backup import/export and local backup history. Cache public app files and help for offline use; keep personal backups out of the public cache and verify local persistence. Pin the visible UI/bundle version so a background update cannot change an active operation. Any cloud feature stays optional, isolated, and opt-in. OEM and recovery data always stay local. Remove analytics; do not collect telemetry.

**Results.** Offline browser build, shared backup fixtures, schema/help coverage, recorded-response transport tests, and checks for storage denial, disconnect, malformed response, timeout, and occupied device. These checks use a fake transport; they do not prove WebHID access. Saved settings use readback and stop on error; fixture tests are host evidence only.

**Completion / stop.** All supported controls and backup operations pass fixtures and fail-stop checks; offline UI and help open after initial caching. A failed read or persistence operation must never appear successful. No physical writes are part of this stage.

## 4. Add browser update, restore, and OEM rollback

**Work.** Implement release selection, stable/prerelease and revocation rules, custom image selection, compatibility preview, fresh settings backup, confirmed update flow, cancellation before erase, device reconnect, installed-image verification, and optional settings restore with readback. First release must perform actual flash, restore, and OEM rollback entirely in the browser. An installer fallback does not satisfy this requirement. Download and validate every input before erase; after erase begins, any timeout, storage fault, disconnect, or bad readback stops the sequence. Never retry, reset, blindly restore, or continue automatically. OEM restore uses only a validated image with proven ownership and never applies project settings over it.

**Results.** Offline host-model coverage for the operation state machine, negative fixtures for hashes, addresses, protected regions, truncation and mismatched identity, and a reviewed browser permission/loader design. Hardware checks are separate and require explicit owner confirmation for each transition or write.

**Completion / stop.** Host checks prove ordering and fail-stop behavior, not hardware. The browser feature is not release-ready until the required loader, flash, installed image, settings restore, and OEM rollback have been separately qualified on hardware with operation-specific authorization. Any unresolved identity or image-preparation ambiguity blocks writes.

## 5. Qualification, help, and first browser release

**Work.** Cover every supported behavior and remapping in the reusable suite, including both encoder directions. Regression checks use fixtures and require no physical key presses or knob movement. Include protocol parsing, backups, packaging parity, release/revocation, offline cache, local storage, and UI/help consistency. Help modules and catalog fields must match actual firmware support. CI builds and checks browser assets and fixtures offline; publish to GitHub Pages and firmware/catalog/help data to GitHub Releases. Report device behavior and durable storage separately from static checks and host models.

**Results.** Acceptance matrix, CI artifacts, release manifest and hashes, deployment instructions, and qualification record listing passed, skipped, and unproven conditions. The paired firmware release retains the existing standalone Windows/Linux x86_64 firmware installers, SHA256 files and RU/EN instructions. The shared desktop configurator has its own packages and release gate; neither product must wait for the other to finish.

**Completion / stop.** All acceptance rows applicable to the browser release have evidence and no unresolved release-blocking failure. Desktop and helper requirements have their own release gates and do not block the website. Do not claim a physical feature from source presence or a host-model pass.

## 6. Native release and optional helper

This stage runs alongside stages 3–5 if Entropy is selected; native configuration and packaging can be completed and released before the website. With Pipette, it follows the browser release. Reuse the shared editor and model in a Windows, Linux, and macOS application. If Entropy was selected, reuse its native egui client and the shared Rust model; if Pipette was selected, assess Tauri and its native HID backend before committing to an OS shell. Add offline installation, bundled firmware/catalog/help, and per-OS installers and instructions. Treat helper autostart, tray behavior, and active-layout detection as separate features. Prove three OS-layout mappings and supported desktop environments per platform. Treat the helper as conditional on firmware support. Define the three layout states and helper integration before implementation. Firmware support for the OS indicator override and optional Mac/PC baseline now exists in source profiles; helper work still needs integration, platform tests, and the exact-image qualification required for each changed profile. Coordinate the helper with browser flashing and suspend it during device operations. Measure application memory and startup on target systems; do not infer them from installer size.

**Completion / stop.** Release the native configurator after its applicable per-platform package, offline-use, HID and function checks pass. Add the helper in an application release once layout detection, background lifecycle and firmware-resource checks also pass. It may follow in a later version. Native release does not require website completion. Unsupported OS environments must be named plainly.

## Acceptance coverage

| Requirements | Evidence required before release |
| --- | --- |
| AKW-001–005, AKW-082: scope and foundation | Shared editor/transport prototype, reviewed reuse decision and RU/EN coverage |
| AKW-010–014: device and capabilities | Unique identity or blocked write; installed-image capabilities, not release assumptions |
| AKW-020–023, AKW-040–042: settings and help | Layers, keys, both wheel directions, macros, Combo, RGB, backup/restore and documented limits |
| AKW-030–034: releases and custom builds | Stable/prerelease/revocation behavior; schema, model, address, hash and protected-region checks |
| AKW-043–044, AKW-050–054: firmware and OEM recovery | Validated source/identity, browser loader, cancellation boundary, flash/readback/restore/rollback results |
| AKW-023, AKW-070–072: offline and privacy | Cached UI/help, verified local backups, no required account or upload, private diagnostic report |
| AKW-060–064: desktop and helper | Three OS packages, platform-specific HID/layout checks and measured resource use |
| AKW-080–084: checks and release | Coordinated CI for code/catalog/help, Pages deployment and a separate hardware qualification record |

This table summarizes coverage; it does not replace the detailed requirements.
