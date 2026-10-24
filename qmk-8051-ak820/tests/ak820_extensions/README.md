# Compact extension storage host checks

Run `python3 tests/ak820_extensions/storage.py` from the QMK root. Both
`tests/ak820_tap_dance/host.py` and `tests/ak820_key_overrides/host.py` also run
this check after their engine fixtures.

The fixture extracts the compact production getters, setters, validators and
Vial record types. It includes the production extension address header and
models only the EEPROM backend, keyboard cancellation and NVM status.

The checks cover all eight slots for both modules, page padding, unchanged
neighboring bytes, round trips, malformed-row sanitization, empty rows,
invalid indices and keycodes, cancellation before writes, verified-flush
failure and latched NVM failure. Invalid setters must produce no cancellation,
write or flush. Compilation uses UBSan and treats warnings as errors.

This host model does not establish SDCC ABI, flash durability, power-loss
behavior, USB transfers or physical key behavior.
