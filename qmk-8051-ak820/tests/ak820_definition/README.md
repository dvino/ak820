# Vial definition and one-byte layout options

All runners are offline. They do not open USB or program flash.

`run.py` executes the actual linked Vial definition reader in uCsim C52. It
checks size, every valid page, boundary/out-of-range page IDs, each high bit of
the 32-bit wire page ID, combined high values and invalid packet lengths.
The repository GUI's actual `reload_layout()` body and KLE parser then consume
captured CPU responses through a fake HID transport. The resulting definition
must match the source JSON exactly, with 83 physical keys and two encoder
directions. GUI widgets, real HID timing and Entropy's Rust decoder are outside
this test.

The negative control with a 396-byte definition had 49 failures out of 102
packets: high page bits were ignored. The corrected 396-byte image passes all
102; compact XZ produces 384 bytes / 12 full pages and 101 packet cases.
The report includes the actual IHX, generated blob, runner and GUI source
hashes, and explicitly marks whether the tested image fits the release CODE
windows. Early size experiments that do not fit are not release candidates.

`compression.py` compares the actual generator CLI with immutable RC4. Without
the new option, the complete header must remain identical. Compact mode keeps
XZ/LZMA2/CRC64, preserves the exact minified JSON bytes and chooses the smaller
of the old and new encoding. Six inputs verify Python and independent `xz`
CLI decoding; a longer input verifies fallback to the ordinary encoding.
LZMA-alone was measured separately and is not enabled.

`layout_host.py` extracts the real getter/setter bodies from candidate `via.c`
and immutable RC4. For each field size 1 through 4, UBSan checks 1,245,440
read/write cases against exact callback and EEPROM traces. It includes all
low 16-bit values combined with zero, mixed, all-one and every individual high
bit. The callback must receive the complete uint32 value before the same
persisted bytes are written. The AK820 specialization applies only to size 1;
other sizes keep the original implementation.

`layout_cpu.py` checks the real SDCC uint32 argument/return ABI, 256 CODE-backed
read values and 816 setter values through the actual EEPROM adapters. A
64-byte page cache under an explicit batch permits writes without invoking
flash programming in the CPU model. Only byte offset `0x28` (decimal 40) may
change; all other bytes and storage fault state are checked. This is not a
flash persistence test.

Run from the QMK directory, using the exact final build under review:

```sh
python3 tests/ak820_definition/run.py --build-dir .build/FINAL --s51 ../toolchains/sdcc-4.4.0/bin/s51 --output-dir .build/FINAL/definition-tests
python3 tests/ak820_definition/layout_cpu.py --build-dir .build/FINAL --s51 ../toolchains/sdcc-4.4.0/bin/s51 --output-dir .build/FINAL/layout-cpu-tests
python3 tests/ak820_definition/layout_host.py --output-dir .build/FINAL/layout-host-tests
python3 tests/ak820_definition/compression.py --output-dir .build/FINAL/compression-tests
```
