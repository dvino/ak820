# Root source inventory, 2026-10-23

This is a read-only inventory for the source trim. It does not approve a flash,
change the installed firmware, or remove files. The lead owns all moves and
deletions. Counts below describe the working tree at inspection time.

The current installer does not need the old Vial desktop application. `AK820.cmd`
and `AK820.sh` call `tools/installer/ak820.py`. The Windows builder imports that
installer and `qmk-8051-ak820/util/ak820_release_manifest.py`; its package inputs
come from the explicit `HOST_FILES` list and the approved release manifest.
The device regression adapter imports the current QMK loader/diagnostic tools
and the current installer. None of those entry points imports root `src/`.

## Remove with the obsolete desktop app

| Path | What it contains | Action |
| --- | --- | --- |
| `src/` | 120 tracked files, 1,522,262 bytes including two ignored bytecode files; upstream Vial GUI plus old AK820 native-firmware adapter | Remove after retiring the old consumers listed below. It is not part of the current installer or current device regression suite. |
| `util/` | Eight tracked files, 2,710 bytes; old Vial Docker/AppImage builder, macro fuzzers and Python 3.6 setup | Remove with `src/`. The Linux builder installs root `requirements.txt`, calls `fbs`, and packages `misc/Vial.yml`. |
| `misc/` | One tracked 533-byte Vial AppImage recipe | Remove with the old Linux desktop builder. |
| `.python-version` | Pins Python 3.6.0 | Remove. Current source installer requires Python 3.10 or later. |
| `requirements.txt`, `test-requirements.txt` | Old Vial PyQt/fbs/PyInstaller 3 dependencies | Remove with the desktop app. Current installer has `tools/installer/requirements.txt` and `requirements-build-windows.txt`. |
| `requirements-ak820.txt` | Dependencies for the old PyQt AK820 app | Remove when old app and inventory generator consumers are retired. |
| `requirements-analysis.txt` | Disassembly libraries for old native-firmware research | Remove only with the retired research tool set, or move its requirements next to any retained research script. |

The two untracked or ignored `src/` files are only
`src/main/python/__pycache__/kle_serial.cpython-312.pyc` and
`src/main/python/__pycache__/kle_serial.cpython-314.pyc`. A targeted `git diff
--name-only` for the paths in this inventory returned no modified tracked files.
That check does not cover other agents' later edits or staged differences.

Old consumers must be removed or deliberately revised in the same change:

- `tools/analyze_native_gui_geometry.py`, `analyze_vial_resource_budget.py`,
  `build_vial_keycode_catalog.py`, `build_vial_native_definition.py`,
  `build_vial_readonly_dispatcher.py`, `check_port_review.py`,
  `check_vial_keycode_catalog.py` and `flash_candidate.py` read root `src/`.
- `tools/package_port.py` packages `AK820-Vial-v2.exe` and the old source tree,
  and copies root `COPYING` and `COPYING-GPLv3`.
- `tools/inventory_firmware.py` inventories the two old root AK820/analysis
  requirement files.
- Old `docs/vial-*.json` reports record Vial GUI source paths. Some mean pinned
  remote source paths rather than local imports. Preserve needed evidence in the
  external private backup before removing retired reports and their generators.

Do not delete all root `tools/`: current installer packaging, tests and device
regressions live there. Keep `tools/installer/`, `build_release_bundle.py`,
`build_windows_installer.py`, their current tests, `ak820_device_protocol.py`,
`ak820_device_tests.py`, `test_ak820_device_tests.py`, `test_keyboard.py` and
`test_keyboard_runner.py`, plus their actual imports and fixtures.

## Preserve recovery and evidence before trimming

| Path | Inventory | Why it is different from upstream app source |
| --- | --- | --- |
| `firmware/` | 19 tracked files, 54,458 bytes | Old native AK820 build, physical-check and recovery records; two loader tools. This directory is evidence, not a full upstream clone. Several original-native research tools read its records or now-absent private binaries. |
| `history/` | 2,141 tracked files, 55,510,739 bytes | Historical local AK820 work. It is currently ignored for new files but its existing files remain tracked. No current installer/device-suite consumer was found. Preserve in external private backup before removing obsolete tree contents. |
| `investigation/` | 137 tracked files, 458,919 bytes | Original disassembly and scripts. No current installer/device-suite consumer was found. Preserve unique recovery/research evidence externally before removing obsolete tree contents. |
| `host/windows/` | 12 tracked files, 54,541 bytes | Old RC3 trial and OEM recovery wrappers, including recovery tests. It points to `releases/rc3` and `evidence/oem-backup`; `tools/verify_repository.py` still requires four wrappers. It is not the current Windows installer. Preserve original OEM recovery evidence and revise/retire the old verifier before trimming. |
| `host/runs/` | Ignored private sessions | Keep original backup and current device evidence. They are not upstream source and were not inventoried or read here. |

Root `CONTRIBUTING.md` is a short current project contribution guide. Keep it.
Root `LICENSE` is the current project license. Keep it. `COPYING` is GPLv2 text
and `COPYING-GPLv3` is GPLv3 text. Their explicit root tool consumer is the old
`package_port.py`. They may be removed as duplicate app-package copies only
after checking retained third-party notices and retaining required license text
for the remaining source. Do not strip individual copyright/SPDX notices.

The current documentation already says the old portable ZIP is superseded.
README and current guides should direct users only to the current installer.
`docs/LICENSING.md` must describe the retained QMK subset and actual current
license files after the trim, without claiming that all Vial GUI source remains.

## Local dependencies are separate

Root `.build*`, `dist`, `.venv-*`, and `toolchains` are build outputs, Python
environments or installed local toolchains. They are not evidence that the
maintained source must include a full upstream app. Do not remove the current
release, required toolchain, OEM backup, or session evidence merely to reduce
the visible source tree. This inventory did not inspect or modify their contents.

## Evidence and limits

Inspection used native Git tracked-file lists, targeted differences, filesystem
counts and text searches across current entry points, tools and documentation.
No build, tests, USB operation, reset, write or commit was run. The QMK tree is
outside this inventory and has a separate dependency review. A consumer search
shows source relationships; it does not prove future users never call a retired
script. Run the retained offline suites and documentation checks after trimming.
