# Python payload staging smoke

Date: 2026-10-26

## Result

PASS for the bounded smoke scope. The real-source Python payload staged successfully, and its extracted `tools/installer/ak820.py --help` command exited 0 from outside the repository with `PYTHONPATH` removed. No USB or device operation was run.

This was a minimal staging smoke, not a releasable beta package. It called `python_package_files()` and `write_python_packages()` directly with one temporary synthetic profile context containing empty `installer-release.json` file metadata and `approved-release.json`. The top-level beta builder, ten approved profile bundles, firmware identities, release approvals, and release admission were not exercised. At the time of this smoke check, the alpha2 saved-ROM fixture was missing. That input was subsequently supplied and validated; see [input validation](alpha2-input-validation.json). The final package must still pass its own admission checks.

## Checks and evidence

- Payload contained 98 files totaling 6,094,166 uncompressed bytes.
- `AK820-Windows.zip` SHA256: `47e27fb8ebfcc64e01f519c623e780dd42f78523705fe2a257564a7c436ebe21`.
- `AK820-Linux-x86_64.tar.gz` SHA256: `39480b1475695ace0162f1e8d19e7c70c5cd16a1f44016ee562259c6f6c766b5`.
- Staged `tools/installer/ak820.py` SHA256: `6ce93cce23a6b8fc5be0032ad46eb7c7034cc23131de8a1c5985354ada474c22`.
- Installer help: exit 0; stdout began with usage and the expected profile/command options; stderr was empty.
- No `gui.py`, GUI build scripts, PyInstaller references, or GUI requirements files appeared in the staged file inventory.
- `AK820.cmd` targets `%~dp0tools\installer\ak820.py`; that file exists in the extracted Windows payload.
- All relative Markdown links in `INSTALL-en.md` and `INSTALL-ru.md` resolved within the extracted payload. Targets checked: `docs/ru/INSTALL.md`, `docs/INSTALL.md`, the English and Russian profile README, and each language's `SETTINGS-BACKUP.md`.

## Commands and method

From `/workspace/scratch/772c1403f0df/ak820`, inspected `AGENTS.md`, `tools/build_beta_release_assets.py` and `tools/build_windows_installer.py`. Then ran a single `python - <<'PY' ... PY` harness that:

1. Imported `build_beta_release_assets` and constructed one temporary profile context with an empty manifest file map.
2. Called `python_package_files([context])` to collect actual repository host files, Python installer files, and `guide_files()` content, plus the two actual install guides.
3. Called `write_python_packages(stage, files)` to create the Windows ZIP and Linux tarball under a temporary `/tmp` directory.
4. Extracted the ZIP, removed `PYTHONPATH` from a copy of the environment, and ran `[sys.executable, staged_script, '--help']` with `cwd` set to the temporary stage directory and a 30-second timeout.
5. Inspected the staged inventory, Windows launcher target, guide-relative links, and printed the JSON evidence above.

Temporary bundle metadata was created in a temporary directory under the repository because the staging API requires profile bundles beneath its repository root. The temporary directory was removed automatically. No repository source, firmware, tools, or tests were edited. No full firmware build or GUI/PyInstaller build was run.
