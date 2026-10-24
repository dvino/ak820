# Compact NKRO controls

`AK820_NKRO_CONTROL=yes` adds `NK_ON`, `NK_OFF` and `NK_TOGG` without the
Magic engine. The default is `no`. Each accepted press clears the old report,
held owners and deferred actions before selecting the new report mode. A release
does not change the mode. Keys already held at a switch must be released before
they can produce a new press.

The mode is temporary. These controls do not write `EECONFIG_KEYMAP` or change
saved settings. Restart uses the existing saved/default mode. The typed settings
backup does not export this temporary state.

Run the production-handler host check from the QMK directory:

```sh
python3 tests/ak820_nkro_control/host.py
```

Run complete-image CPU checks with a production-bounded NKRO-control build:

```sh
python3 tests/ak820_nkro_control/linked.py \
  --build-dir .build/nkro \
  --s51 /path/to/sdcc-4.6.0/bin/s51 \
  --output-dir /tmp/ak820-nkro-linked
```

The CPU checks run real matrix, action, report and cancellation code on a generic
C52 CPU. They check both report representations, ON/OFF/TOGGLE, inert releases
and cleanup of held keys, modifiers and tap-hold state. They do not test a USB
host, VS11K28A interrupts, flash retention or a physical keyboard.
