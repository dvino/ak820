# Settings word reads

```sh
python3 tests/ak820_settings_word/run.py --toolchain /toolchains/sdcc-4.6.0 --output /tmp/settings-word-check
```

SDCC and s51 execute the actual production helper for all 65536 word values,
cycling through 256 XDATA pointer positions including page crossing. Eight
register canaries, restored SP and bank-zero bits are checked. The five actual
compiled settings getters make another 327680 calls with matching expected words.
A fresh map resolves the terminal breakpoint; timeout or a missing success
marker fails. Result JSON binds source, fixture, test and tool hashes.

The fixture does not enumerate all XDATA addresses or entry register banks. It
does not qualify the complete image, IRQs, storage transactions or device timing.
The normal settings host model separately checks validation and persistence
behavior, with and without Auto Shift.
