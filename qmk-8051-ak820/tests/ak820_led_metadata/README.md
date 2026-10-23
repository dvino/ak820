# AK820 fixed LED metadata

`rc4-metadata.json` is an immutable oracle for all 82 VialRGB LED responses:
x/y, flags, row and column. The source keymap was checked byte-for-byte against
commit `cb9ff6ea` before replacing its redundant `g_led_config` representation.
The fixture records that source SHA256 and the original linked-image SHA256.

```sh
python tests/ak820_led_metadata/run.py \
  --build-dir .build/rc5-local --s51 ../toolchains/sdcc-4.4.0/bin/s51 \
  --output-dir .build/rc5-local/led-metadata-tests
```

The runner executes the actual linked VialRGB handler with XDATA packets and
CODE metadata. It checks all 82 complete 32-byte replies, four out-of-range LED
indices and eight invalid packet lengths: 94 CPU observations. The expected
responses come from the RC4 fixture, not from the new tables or lookup code.

The new representation stores immutable x/y coordinates in CODE, obtains
row/column from the existing electrical-slot table, and uses the board's
constant `LED_FLAG_KEYLIGHT`. No hardware model is implied. Existing
`tests/ak820_emitted` separately exercises solid/direct rendering and USB
suspend/resume against the linked image; it uses electrical slot addresses and
does not depend on the removed `g_led_config` symbol.
