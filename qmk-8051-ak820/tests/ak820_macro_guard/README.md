# AK820 macro playback guard regression

From the QMK source root:

```sh
python3 tests/ak820_macro_guard/run.py
```

Requires Python3 and a host C compiler with AddressSanitizer and
UndefinedBehaviorSanitizer. `--cc clang` selects another compiler;
`--no-sanitize` runs the same assertions on a compiler without sanitizers.
No USB device is opened and no firmware is written.

The runner extracts the current `decode_keycode()` and
`dynamic_keymap_macro_send()` bodies from `quantum/dynamic_keymap.c`, plus the
real `send_string()` and `send_string_with_delay()` bodies, at run time.
The harness supplies EEPROM, key-emission endpoints and timing stubs. It checks
recursive playback through every extended tap/down/up operation, subsequent
playback after early returns and breaks, and a Vial delay of 65024 ms.

Every combination of extended and basic macro actions is consumed by the real
string walker. Its short command must be terminated even after an extended
command used the fourth byte. Non-ASCII keycode operands remain supported;
plain-text bytes 128 through 255 from legacy streams must stop before the ASCII
sender. The next macro must remain usable. Temporary outputs are removed after
the run. The strengthened test reproduces an AddressSanitizer overflow on rc1.

This is a host regression for the production interpreter's guard and control
flow. It does not execute the complete QMK event pipeline or prove timing,
stack usage, or USB behavior on the keyboard. The target build and emitted-code
tests are separate checks; a successful SDCC compilation alone does not prove
that its ABI or physical peripheral behavior is correct.
