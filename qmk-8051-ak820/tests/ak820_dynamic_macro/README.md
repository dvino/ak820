# Compact Dynamic Macro tests

`host.py` runs extracted production C with UBSan, including Auto Shift, One Shot,
Repeat and ownership helpers. Its six mutation controls must fail. `linked.py`
runs the exact built SDCC image in uCsim C52 with supplied NVM, matrix, endpoint,
suspend and reset state. No test opens USB or writes a physical device.

From the QMK directory:

```sh
python3 tests/ak820_dynamic_macro/host.py --output /tmp/dm-host.json
python3 tests/ak820_dynamic_macro/linked.py \
  --build-dir .build/dm-reviewed \
  --s51 /path/to/sdcc-4.6.0/bin/s51 --output-dir /tmp/dm-linked
```

The linked suite leaves Auto Shift disabled through `AS_OFF` for ordinary cases.
When compiled, a dedicated interaction enables it through `AS_ON` and checks
that the stored and replayed tap retains Shift. Physical USB, real interrupt
nesting, electrical timing and device acceptance remain untested.
