# VialRGB direct-fastset helper check

Run `ASAN_OPTIONS=detect_leaks=0 python3 tests/vialrgb_fastset/compare.py` from
`qmk-8051-ak820`. The script extracts the helper from the production source and
the frozen `09330ab708e1eb3671571f63894c583e01743eef` source revision, then
compiles each with AddressSanitizer and UndefinedBehaviorSanitizer.

Both implementations use an 82-LED fixture. The check covers every low-byte
first index and LED count with high byte zero, then every low byte with high
bytes 1 through 255 at counts 0, 1, 9, 10 and 255. It verifies all LED colors
for valid indices, the out-of-range canary, and that the input packet remains
unchanged. A second sweep checks every possible HSV value byte at both valid
edges against the brightness clamp. The script also extracts and executes the
public setter for lengths 0 through 255. It prints each extracted helper's
SHA256 and the coverage partitions.

This is a host test of the private helper and extracted setter. It does not
prove target stack use, interrupt bounds, full-image size, or keyboard
behavior.
