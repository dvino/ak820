Русский перевод: [Состояние и обзор](ru/REVIEW.md).

# Configurator status and review

Date: 2026-10-24. This work package adds requirements, an implementation plan
and documentation links. It does not import an upstream application or change
firmware, installer code, release policy or device settings. No browser or
desktop configurator was built or deployed by this work package.

## Sources for the implementation plan

| Source | Inspected revision | Relevant result |
| --- | --- | --- |
| AK820 | `5cbc66fbaf22bf5372e76e892207f58d453d9183` | Existing settings, packer, update and qualification code remain the behavioral references. |
| [Entropy](https://github.com/ergohaven/entropy/tree/5b222b5d6349fb351f53b36c66169095b3039fc1) | `5b222b5d6349fb351f53b36c66169095b3039fc1` | Native Rust/egui editor, EN/RU input-language tracking and Wasm groundwork; a working WebHID path was not found. |
| [Pipette fork](https://github.com/Tymon3310/pipette-desktop/tree/99914fd07cef3bbf9bbf76c06ce0db79069b8c98) | `99914fd07cef3bbf9bbf76c06ce0db79069b8c98` | Shared browser/Tauri interface, browser API gaps and a different DFU loader. |
| [Vialite](https://github.com/tcyeee/vialite/tree/6a3c61c8f34adb08f0e11e4294245890f3371fd8) | `6a3c61c8f34adb08f0e11e4294245890f3371fd8` | Browser alternative; incomplete layout backup, retries and license details require attention. |

Entropy's `Cargo.toml` declares GPL-3.0-or-later and egui/eframe. Its native
entry point and HID gates do not establish a working browser build. The
framework supports Wasm, so a shared Rust interface is a candidate to test,
not a reason to rewrite the UI in TypeScript.

Entropy's layout detector currently normalizes EN/RU only; the planned helper
needs configurable identifiers for more layouts. Hiding or minimizing its
window does not demonstrate GUI memory release. The source contains some
write readback, but its retry policy must be changed for AK820. Package sizes
are not measurements of running memory or speed.

The existing AK820 installer permits only its exact qualified images and
requires personal source data. New custom-build support and installation
without a saved OEM archive require a separately defined, tested policy.
These requirements do not relax the existing installer gates. Safe source
reads, protected-region checks and device identity remain necessary.

## Checks and remaining work

The completed fork study is source inspection. It does not prove browser
permissions, real loader access, physical input, storage retention, successful
flashing or platform performance. No USB commands, resets, loader transitions
or device tests were run for this documentation package.

Hardware work requires separate operation-specific permission.

## Documentation verification and finding closure

The package contains eight new EN/RU Markdown documents and navigation updates
in README, Index, Roadmap and Status. The local link/language check covers all
eight new files and confirms the same 42 requirement IDs in EN/RU, with no
duplicates or unfinished placeholders. `python3 tools/check_docs.py` passes
for the 49 public documents at that revision. After integration with firmware
source `f53ec73`, the check passes for 53 public documents. The initial new-file check found two
misplaced translation links; both were corrected and the check passed again.
`git diff --check` passes. No firmware tests or builds are needed to validate
this documentation-only change; no such result is claimed.

An independent review covered the requirements, plan, translations, navigation
and verification limits before commit. Findings and closure:

| Finding | Correction | Recheck |
| --- | --- | --- |
| D1: firmware installer packages could be mistaken for the later configurator application | Existing firmware installers and shared configurator packages are separate in requirements and plan. | Closed in EN/RU. |
| D2: Pipette comparison was mandatory in requirements but conditional in the plan | The bounded comparison is always required; a larger fallback prototype remains conditional. | Closed in EN/RU. |
| D3: the revised native-first schedule retained browser-first wording | Entropy starts natively with parallel web development and independent applicable release gates; the stale introduction was corrected. | Closed in EN/RU. |

The final recheck found no blocking findings and confirmed the agreed branch
roles: browser `web-dev`, native development `desktop-dev`, native release
preparation `desktop`. Shared code changes are merged and checked for both
targets. This records review of the documentation, not qualification of a
configurator, firmware image or deployed site.
