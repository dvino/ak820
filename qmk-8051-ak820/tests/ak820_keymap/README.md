# AK820 VIA keymap regression

Run `python3 tests/ak820_keymap/run.py` from the source root with a host C
compiler supporting AddressSanitizer and UndefinedBehaviorSanitizer.

The runner extracts the current VIA dispatcher and keymap functions unchanged,
and links the production EEPROM, NVM and macro backend against a bounded flash
array. It checks normal editing, the locked one-key boot assignment's explicit
`id_unhandled` response and unchanged old mapping, unlocked assignment, the
existing bulk restriction, and out-of-range requests. The test's loader stub
asserts if called. No USB device or physical flash is used.

This validates protocol dispatch and persistence behavior in the host model.
It does not prove SDCC calling conventions, physical flash behavior, or the
complete Vial graphical interface workflow.
