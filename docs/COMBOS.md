Русский перевод: [Комбинации клавиш](ru/COMBOS.md).

# Two-key Combos

Firmware version 0.6.0-alpha.2 adds eight configurable two-key Combos for the
AK820. Pressing two configured keys within 40 ms sends one key or modified key
instead, for example J + K → Escape or F + D → Ctrl+C. Alpha.1 does not support
Combos. See [Status](STATUS.md) for release and device state, and the retained
[Combo technical report](../audits/rc6/combos-20261024.md) for
implementation and verification details.

## Configure in Vial

Open the keyboard in Vial and configure one of the eight Combo slots. Set two
different input keys and one output. Set the third and fourth input fields to
zero; an all-zero slot is disabled. Read the slot back after saving it. If the
firmware rejects a value, choose a supported key or output instead.

Inputs must be ordinary keyboard keys from `KC_A` through `KC_EXSEL`. Outputs
can be ordinary keyboard keys, one of the eight modifier keys, or a modifier
combined with an ordinary key. For example, Ctrl+C is supported. Inputs cannot
be modifiers, Mod-Tap, Layer-Tap, macros, Repeat, encoder events or other
quantum keycodes. Outputs cannot be macros, layer actions, Mod-Tap, Layer-Tap,
Repeat, consumer or system keys, or reset. The Vial editor may display choices
that this firmware does not support.

The interval is fixed at 40 ms. Three-key and four-key Combos, and a separate
interval for each slot, are not supported. Duplicate pairs are allowed; if a
pair appears in more than one slot, the lowest numbered slot takes priority.

## Key behavior

The first input is held for up to 40 ms while the firmware waits for its pair.
If the second key is pressed before 40 ms elapses, both input keys are suppressed
and the configured output is sent. Releasing either input releases the output;
the other input remains suppressed until it is released. A new Combo cannot
start while either input from the active Combo is still held.

If the second key is not pressed in time, or another key or event arrives first,
the first key is sent as an ordinary key. At exactly 40 ms the pair no longer
matches. Releasing the first key quickly still sends its press before its
release. A Combo key is resolved on the active layer when it is pressed; a
layer change while it is waiting does not change that key. Other keys continue
to work while the firmware waits.

## Backups

Backups from alpha.2 save all eight slots, including empty ones. Restoring an
alpha.1 backup to alpha.2 is allowed only when every target Combo slot is
empty. Restoring an alpha.2 backup applies all eight saved slots, so empty slots
clear their matching target slots. See [Settings backup and restore](SETTINGS-BACKUP.md)
for migration behavior and recovery steps.
