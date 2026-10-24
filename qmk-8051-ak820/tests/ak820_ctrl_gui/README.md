# Ctrl/GUI swap checks

`host.py` compiles the production control and report functions with a small
host harness. It checks every keycode value and press/release state, all 256
effective modifier masks against a separately written mapping, modifier owners,
and GUI-lock masking after the swap.

`flags.py` checks swap-only and GUI-lock-only builds separately, plus the
standard and full profile's default-off setting. It also checks that controls
are consumed before Dynamic Macro recording and Repeat history.

`linked.py` runs the selected SDCC image in the repository's generic C52 CPU
fixture. It covers physical modifiers, held-key releases, One Shot, Mod-Tap,
the built-in macro interpreter, and both 6KRO and NKRO reports. The simulator
does not model the AK820 USB controller, physical USB, interrupt timing, flash,
or installed firmware.

```sh
python3 qmk-8051-ak820/tests/ak820_ctrl_gui/host.py
python3 qmk-8051-ak820/tests/ak820_ctrl_gui/linked.py \
  --build-dir qmk-8051-ak820/.build/cg-full \
  --s51 /path/to/sdcc-4.6.0/bin/s51 \
  --output-dir /tmp/ak820-ctrl-gui-linked
```
