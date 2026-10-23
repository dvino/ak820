# AK820 16-bit keycode and modifier regression

Run from the firmware root:

```sh
python tests/ak820_keycode/run.py --build-dir .build/CANDIDATE \
  --s51 ../toolchains/sdcc-4.4.0/bin/s51 --output-dir .build/CANDIDATE-keycodes
```

Omit `--build-dir`/`--s51` for host-only validation. `--source-root` can point to
an isolated experiment. The host compiles actual production function bodies and
immutable RC4 decoder/code16 bodies under ASAN/UBSAN. Every 16-bit input checks
action decoding, modifier extraction and exact register/unregister call order.
The only action-decoder change from RC4 is the explicit LM contract: right-mod
marker bit 4 selects a HID nibble and must not change the requested layer.
All 512 LM values are checked; 128 even-layer/right-marker cases intentionally
change, while the other 65408 action results remain equal to RC4.

The optional CPU stage calls the actual linked action decoder and modifier
extractor for all 65536 inputs each. It compares every output byte against the
host reference table, records the IHX hash and reports sampled stack usage.
Synthetic counter/table/trampoline memory belongs only to generic C52 simulation;
this test never opens USB or modifies physical Flash. It does not prove a global
stack bound or peripheral behavior.
