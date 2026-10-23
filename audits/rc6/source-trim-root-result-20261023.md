# Root source trim result, 2026-10-23

Removed the obsolete root Vial desktop application, its Python 3.6 build
files, and the old native-firmware research tree. The current installer,
release packaging, device regression tools, QMK source tree, and release files
remain in place.

Before deleting the recovery and research evidence, I resolved the source and
backup paths and copied `firmware/`, `history/`, and `investigation/` to:

`C:\Users\vinok\Documents\Codex\AK820-private-backups\source-trim-20261023`

The backup contains 19 firmware files (54,458 bytes), 2,141 history files
(55,510,739 bytes), and 137 investigation files (458,919 bytes). A per-file
byte count and SHA-256 list is in `inventory-sha256.json` in that backup.
Every copied file matched its source hash before removal. The resolved source
paths were inside `C:\Users\vinok\git\AK820-git`; the resolved backup path
was inside the requested private-backup directory.

Removed root paths: `firmware/`, `history/`, `investigation/`, `src/`,
`util/`, `misc/`, `.python-version`, `requirements.txt`,
`test-requirements.txt`, `requirements-ak820.txt`, and
`requirements-analysis.txt`. The removed `src/` had 120 tracked files and two
ignored Python bytecode caches; the caches were generated files, not source.

Removed 35 obsolete root tools that read the old `src/` or native firmware
evidence, built or checked the retired FN layer, or packaged the old Vial
desktop app. This includes `analyze_native_gui_geometry.py`, the retired
Vial catalog/descriptor/native-definition/dispatcher tools, the candidate
flash and physical-check scripts, `inventory_firmware.py`, and
`package_port.py`. Their consumers are gone with their inputs. In particular,
`package_port.py` was the remaining tool that copied the root `COPYING` files;
those license files themselves were left untouched in this work.

The current Windows installer and its bundle use `tools/installer/` and
`qmk-8051-ak820/util/ak820_release_manifest.py`. The device regression
adapter uses the current QMK loader/diagnostic tools and installer. These
entry points do not import root `src/` or the removed root requirements.
Root tools that used `firmware/backups/`, `firmware/stable/`, or
`firmware/fn-layer/` were retired with that evidence. The QMK subtree's own
`util/` and build requirements are separate and remain present.

The backup hash comparison passed before removal. A follow-up static search
found no remaining root tool importing the removed Vial Python source or the
removed requirements. No build, test, USB operation, reset, firmware write,
commit, or push was run. This does not establish anything about installed
firmware behavior. Documentation reports outside this root-source work package
were left to the lead's documentation cleanup.
