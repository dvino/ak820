# Compact Combo host checks

Run `python3 tests/ak820_combo/run.py` from the QMK root. The command uses only
temporary host files and never accesses a keyboard. It builds the production
`ak820_combo.c` with small event/output stubs, then builds the same engine with
extracted production `dynamic_keymap_get_combo` and `dynamic_keymap_set_combo`
functions and an EEPROM/NVM model. Both runs use UBSan.

The event fixture checks the local state machine, including Caps Word toggle
outputs in both key and release orders. The storage fixture checks record
validation, slot bounds, version markers, wire conversion, empty entries,
Caps Word toggle acceptance, rejection of other unsupported outputs, latched
NVM failure and failure returned by verified flush. The existing flash journal
suite must establish the lower-level durability contract. These checks do not
prove USB, 8051 ABI, physical timing or power-loss behavior.

The user contract and stored format are in [Combos](../../../docs/COMBOS.md).

## Linked 8051 checks

From the QMK root, run the CPU suite against an existing linked build:

```sh
python3 tests/ak820_combo/emitted.py \
  --build-dir .build/combos-candidate \
  --s51 ../toolchains/sdcc-4.6.0/bin/s51 \
  --output-dir .build/combos-cpu-no-usb
```

The command never builds firmware or opens USB. It uses the linked production
`action_exec`, report pipeline and Vial packet dispatcher in the C52 simulator.
The cases cover both key orders and release orders in 6KRO and NKRO,
39/40 ms and timer wrap, pending-key flush before ordinary keys, modifiers,
Mod-Tap and an encoder event, modifier and encoded-modifier outputs, physical
output ownership, Repeat, Caps Word toggle-on and toggle-off through the combo,
no A/S leak from the combo sources, both release orders and cancellation.
Packet cases check the advertised eight entries, stored-marker masking, empty and out-of-range slots,
invalid setters preserving a pending Combo, and an unsupported record version.

A valid setter case supplies an identical marked record in simulated ROM.
The production setter returns success, leaves its cache clean with no storage
fault, and reloads the Combo table. This checks the setter ABI and reload path
without changing flash. Changed-record writes remain in the host storage
fixture; the CPU suite does not establish flash persistence.

Each output directory contains simulator command files, logs and `results.json`
with checks, HID callback traces, stack peaks and hashes of the linked image,
map, runner, imported support and simulator. The NKRO callback is captured before
the USB driver assigns its report ID; state checks also inspect the resulting
report. Caps Word retains its weak Shift after typing A or S and turns off via a
second combo press. The combo source keys stay suppressed; A and S appear only
when typed separately afterward.
Stack peaks cover these paths without interrupt overlap. Physical key scanning,
encoder behavior, USB transfers, IAP, power loss and real timing are not tested.
