Русский перевод: [Комбинации клавиш](ru/COMBOS.md).

# Two-key Combos

A Combo lets two keys act as one shortcut: for example, press J and K almost
together to send Escape. There are eight slots. A result can also include a
modifier such as Ctrl, or toggle Caps Word (which capitalizes a word until it
ends). All ten published beta.5 profiles include Combos; a profile is a set of
firmware features, not a keyboard layer. See [Status](STATUS.md) for release
and device state. The current source is separate and not release-qualified.

**Before changing anything:** the published beta.5 catalog does not authorize
settings writes. A compatible Vial client alone does not authorize them. See
[QMK Settings](QMK-SETTINGS.md) for the Vial Save/Reset compatibility warning
and [backup and restore](SETTINGS-BACKUP.md) for write and recovery limits.

Pressing two configured keys within the selected interval sends one key or
modified key instead, for example J + K → Escape or F + D → Ctrl+C. The interval
defaults to 40 ms; profiles with the QMK Settings module can change
it from 1 to 1000 ms. See [Status](STATUS.md) for release and device state.

In beta.5 and current source, `CM_ON`, `CM_OFF` and `CM_TOGG` turn Combo
matching on, off or switch it for the current session. Assign one to a physical
key in Vial only when that write is authorized. Combos start enabled after restart. Changing the actual
state first sends any buffered pending key, then clears held actions across the
keyboard. Keep held keys released before pressing new keys; the eight saved
slots are unchanged.

## Configure in Vial

When settings writes are authorized, open the keyboard in Vial, open **Combos**
and select a slot. Choose two different input keys and a result, for example
J, K and Escape. Leave the third and fourth input fields at zero; an all-zero
slot is disabled. Read the slot back after saving it. If a value is confirmed
unsupported, choose a supported key or result instead. On timeout, storage error
or bad readback, stop; do not blindly retry, reset or restore. Then press the
two input keys within the interval to send the result.

Inputs must be ordinary keyboard keys from `KC_A` through `KC_EXSEL`. Outputs
can be ordinary keyboard keys, one of the eight modifier keys, or a modifier
combined with an ordinary key, or Caps Word (`CW_TOGG`). For example, A + S
can toggle Caps Word; the next matching Combo turns it off. Releasing the
input keys does not turn Caps Word off. Inputs cannot be modifiers such as Shift, dual-function keys (different
actions for tap and hold), macros, Repeat, knob turns or other special QMK
actions. Outputs cannot be macros, layer actions, dual-function keys, Repeat,
modified media or system keys, or reset. Unmodified media actions from
`KC_AUDIO_MUTE` through `KC_LAUNCHPAD` are supported. The Vial
editor may display choices that this firmware does not support.

The interval defaults to 40 ms for fresh or reset settings; saved settings can
differ. All slots share it. QMK Settings entry 2 permits 1–1000 ms, but do not
use standard Vial Save or Reset on affected firmware until the client and exact
image are confirmed compatible; write authorization is still required. Three-key
and four-key Combos are not supported. Duplicate pairs are allowed; if a
pair appears in more than one slot, the lowest numbered slot takes priority.

## Key behavior

The first input is held for up to the configured interval while the firmware
waits for its pair. If the second key is pressed before that interval elapses,
both input keys are suppressed and the configured output is sent. Releasing either input releases the output;
the other input remains suppressed until it is released. A new Combo cannot
start while either input from the active Combo is still held. Successful outputs
bypass Auto Shift by default. An experimental compile-time opt-in for non-catalog
source builds can delay eligible outputs from completion of the pair; see
[Compact Auto Shift](COMPACT_AUTOSHIFT.md) for its limits and qualification status.

If the second key is not pressed in time, or another key or knob event arrives first,
the first key is sent as an ordinary key in the original beta.5 commit
`78dc69e6f45eac4432949590cc1c9a86c0b1a181`. In both beta.5 and current firmware source,
the first key is sent directly, bypassing Auto Shift (holding it will not
produce its shifted form). Auto Shift for a failed Combo is deferred. At exactly the configured interval
the pair no longer matches. Releasing the first key quickly still sends its
press before its release. A Combo key is resolved on the active layer when it is pressed; a
layer change while it is waiting does not change that key. Other keys continue
to work while the firmware waits.

## Backups

Backups save all eight slots, including empty ones. Restoring a backup applies
all eight saved slots, so empty slots clear their matching target slots. During
beta, the policy for future builds requires compatibility only with the
immediately preceding build. For the original published beta.5, recognized
sources include exact
published beta.3, beta.4, beta.4.1 and beta.5 images, subject to transition and
validation checks; this does not authorize writes. The current, unqualified
candidate has a narrower source-image policy; see [Settings backup and
restore](SETTINGS-BACKUP.md) for that policy, validation and recovery steps.
