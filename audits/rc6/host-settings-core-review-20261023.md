# Host settings backup and restore review — 2026-10-23

## Scope

Independent review covered `tools/installer/settings_backup.py`,
`tools/installer/test_settings_backup.py` and the firmware contracts they use.
The implementation preserves supported saved settings through existing Vial
commands. It does not add firmware commands or import raw NVM. No USB device
was opened; all checks in this report are offline.

The current profile accepts one exact IHX checksum, `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.
Source and target must both use that reviewed image. Sharing a schema ID does
not authorize another firmware build. Every command requires an OEM recovery
session so expected packed CODE, including the 87-byte copied startup helper,
can be reconstructed independently of the captured ROM manifest.

## Contract checks

The export compares the complete expected CODE range and protected regions,
checks the permanent boot marker and clean journal header, and rejects storage
faults. It compares repeated NVM reads and getters. The backup explicitly says
these checks do not provide a firmware freeze or an atomic snapshot.

The manifest binds file sizes and checksums, device model, definition, exact
firmware profile, schema and array dimensions. Validation derives writable
values again from the validated saved NVM. JSON cannot provide arbitrary
addresses or packets. Published backups are not overwritten.

The six physical key layers and both encoder directions are restored through
typed setters. Logical blocks are read back, including neighboring persistent
bytes. The encoder wire order and big-endian NVM words agree with firmware.

Macro grammar agrees with `ak820_macro.c` and the packer's parser. Binary
operands are preserved. Upload chunks stay contiguous and no larger than
28 bytes. The final chunk crosses the sixteenth terminator and ends at the
saved published length, preserving accepted zero padding. More than 27 bytes
of publication padding is rejected. Bytes beyond the published length remain
evidence only and are not uploaded. The encoded low-zero extended keycode
conversion agrees with `dynamic_keymap.c`.

RGB validation uses the pinned effect mapping and eight-byte saved layout.
Disabled lighting restores the selected effect before OFF and Save. Direct
Control, flags or padding without an existing setter, and incompatible core
configuration are blocked during planning. Hidden current RGB fields and the
unreadable Direct palette are explicitly excluded from the preservation
claim. An exposed RAM/NVM mismatch stops export without sending Save.

The restore captures target state before writes, requires explicit write mode
and an unlocked target, checks the original files again, and stops on the
first failure. No retry, rollback, reset or recovery is implemented.

## Verification

The initial test run passed 13 of 14 cases. The failing changing-NVM fixture
XORed one byte on all 498 key getters, returning it to the original value;
that fixture did not model a persistent change. It was corrected to retain
the changed byte, consistent with the documented lack of atomic freezing.

A separate fault injection returned a successful ACK after corrupting the
written key word. Restore raised `Key readback differs` after exactly one
setter and sent no following write. This exercises the bad-readback stop path
in addition to timeout injection in the committed test suite.

`python tools/installer/test_settings_backup.py` passed all 16 corrected
offline tests in 22.751 seconds (root integration run). The two added cases
retain the corrupt-ACK regression and prove that a backup change inside the
write guard is detected before its setter. Both added test bodies were
independently reviewed; the core implementation is unchanged from the
previous independently executed 14-test run.
No concrete source correctness finding remains open from this review. Workflow,
GUI/CLI integration, package contents and documentation agreement need their
separate review. These offline checks do not prove actual writes, power-loss
persistence, key behavior, encoder behavior or visible lighting.
