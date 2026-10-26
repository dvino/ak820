# Beta.3 release handoff review, 2026-10-26

## Scope and method

Independent bounded static review of `docs/INSTALL.md`, `docs/ru/INSTALL.md`,
`docs/DIRECT.md`, `docs/ru/DIRECT.md`, `docs/STATUS.md`, `docs/ru/STATUS.md`,
`web/docs/FIRMWARE-HANDOFF.md`, its Russian translation, `ci/beta3-release-notes.md`,
`README.md`, `docs/ru/README.md`, `.github/workflows/windows-installer.yml`, and
`docs/CI.md`. Package instructions were compared with
`tools/build_beta_release_assets.py`, the guide allowlist in
`tools/build_windows_installer.py`, `HOST_FILES`, launchers, pinned requirements,
and the relevant installer command paths. No production files or tests were
changed. No builds, network requests, USB access or device actions were run.

The final exact-image qualification and STATUS result table were explicitly
pending during this review. This known temporary state is not a finding.

## Findings and accepted closure

All three findings below were closed after independently rereading the lead's
applied English/Russian guide corrections on 2026-10-26. No remaining blocker
was found within this bounded documentation and packaging review.

1. **INSTALL describes the wrong confirmation for `install`.** English says
   that `install` requests a fresh physical confirmation; Russian explicitly
   describes a fresh physical key hold. The OEM `install` path invokes
   `consent()`, which requests typed `yes`. Fresh Esc + left Control belongs to
   the prepared-update/update path. Describe the OEM installation confirmation
   accurately and distinguish the update command if documented. This finding
   concerns the guide, not a request to change the established CLI behavior.
   **Closed:** both guides now describe typed `yes` for OEM installation and
   separately document existing-QMK `update --session OEM_DIR --backup-dir
   NEW_BACKUP_DIR`, fresh three-second Esc + left Control confirmation and the
   second physical confirmation before restoring settings. This agrees with
   the installer consent and settings-workflow paths.
2. **The README recovery deep links no longer resolve.** English links to
   `docs/INSTALL.md#oem-recovery`; Russian links to
   `INSTALL.md#oem-восстановление`. The rewritten guides have neither heading.
   Add a matching recovery section or point both links at the existing guide
   location. Recovery information should be reachable before installation.
   **Closed:** the exact `OEM recovery` and `OEM-восстановление` headings are
   restored, so both existing README fragments resolve to recovery guidance.
3. **Handoff step 5 overstates qualification in English.** It says the
   OS-indicator/Mac-PC profiles “have completed exact-image offline firmware
   qualification” while final qualification is still running. Russian says
   they require qualification before release. Use conditional wording tied to
   STATUS, or replace with final evidence only after qualification completes.
   **Closed:** English now states that these profiles require exact-image
   offline qualification before release, matching the Russian prerequisite.

## Accepted within this scope

- The handoff explicitly calls the capability catalog development-only and
  separates it from installer approval, approved per-profile bundles, settings
  identities and transitions. It grants no release or device-write authority.
- The release asset builder constructs source-only Windows ZIP and Linux
  x86_64 tar.gz packages under `AK820-Python/`, with deterministic archive
  metadata and matching SHA256 sidecars. Linux preserves the launcher execute
  bit. Names, extraction root, local environment and launcher usage agree with
  INSTALL. Setup installs pinned `hidapi==0.15.0`; the Linux prerequisites agree
  with its explicit hidraw source-build path.
- The Python payload is an explicit HOST_FILES/launcher/guide/profile-bundle
  allowlist. GUI source and bundled Python/Tk/PyInstaller runtime dependencies
  are not selected. Reusing the existing GUI packager's guide-list helper does
  not itself package its GUI.
- The release workflow assembles all ten approved profiles, invokes the beta
  release asset builder, verifies all three archive checksums and publishes
  Python Windows/Linux packages, the catalog and English/Russian guides. It
  does not call standalone GUI installer builders.
- Direct EN/RU agree on 82 HSV8 entries, 246 bytes, brightness 160, coherent
  readback, sequential upload, explicit commit, RAM-only storage, fail-stop
  host behavior and the separation between logical commit and scan-boundary
  publication. These are documentation checks, not a repeat firmware review.
- Release notes contain user-visible features and relevant limits, without
  test results, audit process or packaging/licence details. EN/RU both identify
  the game/mmo W pulse and steady higher-layer priority.

## Limits

### ROADMAP follow-up

The subsequent documentation-only edits to `docs/ROADMAP.md` and
`docs/ru/ROADMAP.md` were reread on 2026-10-26. Accepted: their introductions
describe beta.3 source features and direct qualification, release and hardware
state to STATUS instead of retaining a temporary qualification-progress claim.
The repeated status paragraph is removed. Both versions retain the future
exact-image qualification/release gates and identify Direct LED publication
and W behavior as remaining physical validation. No build, test or device
action was needed for this bounded wording check.

This review does not approve final image identities, final policy evidence,
packed firmware, migration results or final release archives. It does not
establish Windows/Linux execution, physical USB timing, LED/DMA publication,
typing, encoder behavior, power-loss persistence or hardware compatibility.
No device write is authorized by this report. The three documentation findings
are closed; final image, policy and archive qualification remain separate gates.
