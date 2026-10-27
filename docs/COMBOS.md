Русский перевод: [Комбинации клавиш](ru/COMBOS.md).

# Two-key Combos

Configure eight two-key combinations that send one key, a modified key or toggle Caps Word.

Caps Word is a valid output in published beta.3 and the current source.
Session controls are in the current source; check [Status](STATUS.md) for
their release availability.

Pressing two configured keys within the selected interval sends one key or
modified key instead, for example J + K → Escape or F + D → Ctrl+C. The interval
defaults to 40 ms; profiles with the QMK Settings module can change
it from 1 to 1000 ms. See [Status](STATUS.md) for release and device state.

`CM_ON`, `CM_OFF` and `CM_TOGG` control Combo matching for the current session.
They work on physical keys and start enabled after restart. Changing the actual
state first sends any buffered pending key, then clears held actions across the
keyboard. Keep held keys released before pressing new keys; the eight saved
slots are unchanged.

## Configure in Vial

Open the keyboard in Vial and configure one of the eight Combo slots. Set two
different input keys and one output. Set the third and fourth input fields to
zero; an all-zero slot is disabled. Read the slot back after saving it. If the
firmware rejects a value, choose a supported key or output instead.

Inputs must be ordinary keyboard keys from `KC_A` through `KC_EXSEL`. Outputs
can be ordinary keyboard keys, one of the eight modifier keys, or a modifier
combined with an ordinary key, or Caps Word (`CW_TOGG`). For example, A + S
can toggle Caps Word; the next matching Combo turns it off. Releasing the
input keys does not turn Caps Word off. Inputs cannot
be modifiers, Mod-Tap, Layer-Tap, macros, Repeat, encoder events or other
quantum keycodes. Outputs cannot be macros, layer actions, Mod-Tap, Layer-Tap,
Repeat, modified consumer or system keys, or reset. Unmodified consumer/media
actions from `KC_AUDIO_MUTE` through `KC_LAUNCHPAD` are supported. The Vial
editor may display choices that this firmware does not support.

The interval defaults to 40 ms. With QMK Settings enabled, change it from 1 to
1000 ms through QSID 2; all slots share the same interval. Three-key
and four-key Combos are not supported. Duplicate pairs are allowed; if a
pair appears in more than one slot, the lowest numbered slot takes priority.

## Key behavior

The first input is held for up to the configured interval while the firmware
waits for its pair. If the second key is pressed before that interval elapses,
both input keys are suppressed and the configured output is sent. Releasing either input releases the output;
the other input remains suppressed until it is released. A new Combo cannot
start while either input from the active Combo is still held.

If the second key is not pressed in time, or another key or event arrives first,
the first key is sent as an ordinary key. At exactly the configured interval
the pair no longer matches. Releasing the first key quickly still sends its
press before its release. A Combo key is resolved on the active layer when it is pressed; a
layer change while it is waiting does not change that key. Other keys continue
to work while the firmware waits.

## Backups

Backups save all eight slots, including empty ones. Restoring a backup applies
all eight saved slots, so empty slots clear their matching target slots. During
beta, supported cross-release restoration is limited to the immediately
preceding build and requires an explicit exact-image transition. See
[Settings backup and restore](SETTINGS-BACKUP.md) for validation and recovery steps.
