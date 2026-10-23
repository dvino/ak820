# AK820 package and recovery regression tests

These are offline tests. The updater tests use synthetic ROM files and fake application/HID objects; the new preparation fixture makes the real HID import function raise if reached. The boot test compiles the production `ak820_boot.c` with a small NVM stub and executes it in the generic 8051 CPU simulator. No physical keyboard interface or firmware update command is used.

## Candidate fixes, 2026-10-22

| Audit finding | Production change | Regression evidence |
|---|---|---|
| A-01: completed saves rejected as pending journals | Live verification requires the 64-byte header at `0xEF40..0xEF7F` to be erased. A retained data page at `0xEF00..0xEF3F` is allowed. | Completed-save verification and permanent preparation succeed. Nonzero header bytes, including partial clear, are rejected. Fresh installation payloads still require **both** journal pages to be zero. |
| A-02: NVM fault prevents an explicit loader request | `bootloader_jump` attempts a best-effort NVM flush, then proceeds to the existing marker erase/readback gate even when NVM is faulted. | Both healthy and faulted NVM stub states reach the reset path when the first four marker bytes read zero. Any uncleared marker byte or denied erase with an intact marker returns without reset and restores IE. |
| A-03: permanent preparation can use a different build | Before opening an application interface, both current IHX/map hashes must equal the session's recorded hashes, and repacking the original trial settings must reproduce the complete session trial image. Permanent packing uses those already parsed inputs. | Matching preparation preserves edited settings, executable bytes outside the existing entry difference, and original recovery files. Different/missing hashes, changed compiled constants, and changed callback mappings are rejected before opening a device or modifying session files. |

The trial bootstrap and `pack_ak820.py` are unchanged. The new provenance checks apply only to permanent preparation. Existing restore sessions remain usable without current IHX/map files or new metadata; their existing recovery/backup validation is retained.

Historical checkpoint: the known-good release restore and native reference were rechecked during the original audit, with native SHA256 `d7152819712470cf37a0c29d69b756edc4a51aca1d20c13e1fcf4b96f9638535`, 51,136 bytes, `0x2800..0xEFC0` exclusive. OEM reference images now reside in the owner's private archive outside this checkout and are not distributed. The current package tests use synthetic fixtures.

## Run

From the candidate source root, with the pinned SDCC 4.4.0 directory supplied explicitly:

```sh
AK820_SDCC_BIN=/workspace/scratch/7d6a4e85d7c6/toolchain/sdcc-4.4.0/bin \
PYTHONDONTWRITEBYTECODE=1 \
python3 -m unittest discover -s tests/ak820_package -p 'test_*.py' -v
```

For another checkout, set `AK820_SDCC_BIN` to that installation's `bin` directory, or provide `sdcc` and `s51` on PATH. The CPU runner requires a POSIX host for its pseudo-terminal. If neither executable location is configured, only the boot test class is skipped; a release verification run must include it.

Recorded result: **29 test methods passed**, including **12 target-CPU boot cases**. A negative-control run using the frozen rc1 updater failed the completed-journal and changed-build regressions, as intended. The same boot regression against frozen rc1 failed for faulted NVM while its healthy-NVM control passed. Those expected failures establish that the tests detect the audited regressions.

`test_native_import.py` and `test_flash_guards.py` retain their existing coverage. `test_preparation.py` adds ten journal/provenance tests. `test_bootloader.py` and `boot_harness.c` provide three boot test methods with the 12 state combinations.

## Evidence limits and integration follow-up

The boot harness stubs NVM persistence and supplies marker bytes representing the outcome observed at readback. Its CPU executes the real erase-register sequence and verifies the exact `0x27C0` target, command, write-enable cleanup, interrupt restoration and software-reset path. It does **not** simulate electrical flash erasure, Safe Mode enforcement, or an actual reset into the OEM loader. No production test hooks are added.

The boot function fix establishes that a requested loader call is no longer blocked by NVM health. End-to-end recovery also depends on reaching that call through the application protocol. At this checkpoint, ordinary Vial replies remain gated on NVM health; availability of identification/unlock/status replies after a fresh faulted boot is an integration follow-up with the USB reviewer. The narrow FD00 readback exception alone is not proof that GUI Unlock + Bootloader works in that state.

No complete candidate firmware build was run for this change while the other owners were editing. The coordinator must inspect the final linked memory windows and independently review the combined source and emitted image. These host/CPU results are not hardware acceptance.
