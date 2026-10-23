# VIA bulk field decoding regression

Run from any directory with Python 3 and a C compiler:

```sh
python3 qmk-8051-ak820/tests/ak820_via_decode/run.py
```

The runner extracts the four production VIA bulk command case bodies from
`quantum/via.c` and compiles those exact bodies into a small host harness. It
checks high-byte-first offset decoding for `0`, `0x00ff`, `0x0100`, `1535`,
`1536` and `0xffff`; sizes `0`, `1`, `28` and `29`; and the exact data pointer
passed to storage. It also checks the macro setter's no-reply return for a
storage failure and an oversized request. The cases are extracted at run time,
so the fixture follows the production source.

The regression exercises dispatch decoding and argument forwarding. The stub
storage functions record calls; they do not prove keymap or macro capacity
checks, NVM durability, USB endpoint ACK/NAK timing, or physical behavior.
Those lower-level bounds and transport fault cases remain covered separately
by `tests/ak820_keymap/harness.c` and `tests/ak820_usb/test_usb.c`.

The proposed shared decoder was rejected after its controlled build increased
linked CODE from 38,069 to 38,179 bytes (+110). The retained firmware source
uses the original inline expressions. This regression is useful for guarding
those existing wire-field contracts; it does not imply that the rejected
helper is beneficial.
