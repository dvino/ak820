# AK820 recovery request integration regression

This offline host regression exercises the production Raw HID transport with the actual VIA, Vial, and bootmagic handler bodies. It verifies that a locked keyboard with a faulted NVM backend can identify itself, provide its Vial definition, complete the existing physical unlock sequence, and dispatch an authorized boot request. It also verifies that persistence failures do not produce successful setter replies.

## Run

Use Python 3 and a host GCC or Clang with AddressSanitizer and UndefinedBehaviorSanitizer support. Linux or WSL with `cc` is the verified environment. Supply an existing firmware build so the test uses its generated Vial definition. From the source root:

```sh
python3 tests/ak820_recovery/run.py --build-dir .build/rc4-release
```

The build directory is required; there is no fallback to a fixed build or copied definition. It must contain exactly one `obj_*/src/vial_generated_keyboard_definition.h`. The current fixture targets the release's `vial` keymap and feature configuration. Relative paths for both directory options are interpreted from the source root, so invocation from another current directory also works.

By default the runner uses a temporary directory and removes its generated fragments, binary, and logs on exit. To retain evidence, choose a new directory:

```sh
python3 tests/ak820_recovery/run.py --build-dir .build/rc4-release \
  --output-dir .build/recovery-regression
```

The output directory must not already exist. It contains `compile.log`, `run.log`, `results.json`, the extracted handler fragments, and the host binary. The JSON records the exact compiler command, selected source hashes, and generated definition hash. `--cc /path/to/clang` selects a different host compiler. A missing definition, changed extraction signature, compile failure, or failed assertion fails the run.

## Coverage

- Faulted, locked discovery: VIA protocol version, Vial ID and UID, size, every page of the selected build's definition, six layers, 8192-byte macro buffer and Caps Word feature bit 0. Accessor stubs model the capacities; compiled firmware bounds are verified by build/package checks.
- Physical unlock: status reports the configured two-key combination; no keys or one key cannot advance unlocking. Physical matrix tasks measure a continuous three-second hold; repeated host polls alone cannot advance it. A release between polls restarts the hold, lock cancels it, and a hold crossing the 32-bit timer wrap succeeds without host polling.
- Authorization: locked boot requests and requests while unlocking cannot dispatch the jump; locked matrix reads remain blocked; after unlocking, matrix read and boot dispatch succeed despite the NVM fault; relocking blocks the jump again.
- Failure replies: 15 setter request forms and 7 unknown request forms remain gated. The enabled setters reach their handler/accessor stubs, so the reply test is not merely rejecting all commands before dispatch.
- Request isolation: the temporary nonpersistent-reply exemption is cleared after every request. The `FD 00` identity response makes no NVM begin, flush, or end call.
- Bootmagic: holding the configured Esc position dispatches recovery while locked and faulted; an unheld key does not.

The fixture uses production enum headers, board UID/unlock configuration, generated definition, USB reply publisher, and endpoint completion code. It extracts whole production handler bodies verbatim instead of duplicating their decision logic. The USB register model is shared with `tests/ak820_usb`, which separately exercises controller/SIE dispatch.

## Proof limits

MMIO, time, matrix state, NVM storage, unrelated feature accessors, and `bootloader_jump` are host stubs. This test does not open USB, execute a device erase or reset, or run the Vial GUI. It proves the source-level request flow for the release configuration, including the physical-unlock policy. It does not prove SDCC code generation, real peripheral timing, successful flash erasure, or hardware recovery. The target-CPU boot regression in `tests/ak820_package/test_bootloader.py` separately checks the actual boot function and independent marker readback gate.

Features disabled in the release, including QMK Settings and the dynamic advanced features, are not enabled by this test or by their request IDs appearing in the whitelist. Their setter IDs are included to ensure the exception remains default-deny as the protocol evolves.
