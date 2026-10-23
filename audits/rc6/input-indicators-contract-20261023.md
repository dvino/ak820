# Caps language switching and indicators

## Result

The offline investigation stopped before firmware changes. Baseline: `5887e92`.
No candidate image was built, no release files were changed, and no device was
opened. There is no measured CODE/XRAM delta and no hardware acceptance claim.
The source findings below identify the decisions needed for a bounded candidate.

## Requested behavior

C follows the Caps Lock bit reported by the host. W is off when only the main
layer is active and on when an additional layer is active. Neither indicator
reports Win lock. Input language is not inferred from Caps presses.

The proposed Windows shortcut is Win+Space. A dedicated remappable user keycode
at the default Caps position is preferable to intercepting `KC_CAPS_LOCK`:
ordinary Caps Lock remains available in Vial, and the language action can move
to any key. Shift plus the dedicated key selects an ordinary Caps Lock action.
Both left and right Shift count, including their combined state. The decision
is made on the dedicated key's down event and cannot change on its up event.
The dedicated action must be excluded from Repeat and Alt Repeat history.
Existing stored maps must remain intact; changing a compiled default does not
migrate a saved keymap or authorize clearing settings. A Vial definition must
name the new user keycode before it is offered for normal use.

## Report ownership contract needed before implementation

Each physical key and remapped action retains ownership of its existing report
bits. A language action may temporarily mask held modifiers in the emitted
report, but must not alter the core's real or weak modifier state. A Shift+Caps
action emits Caps Lock without Shift; held Shift must resume afterward.
Both paths must restore the current report, including modifier changes that
occur while a pulse is pending. A second key event must not re-run the action
on release. An unlock, USB reset or cancellation must leave no synthetic key
or modifier held. Repeat must preserve the previous repeatable key.

An already held Space creates a conflict for Win+Space. An already held ordinary
Caps Lock creates the same conflict for Shift+Caps. Sending an artificial up,
down and restore retriggers another action's held key. Skipping the up fails to
create a new down edge. Calling QMK's ordinary tap helper also removes that
other action's report bit on completion. These outcomes do not meet the
requested ownership contract.

The unresolved product choice is whether to defer the action until its
conflicting key is released or to discard that activation. Deferral also needs
rules for repeated activations, ordering, timeout and unlock cancellation.
A silent discard is not assumed to meet the requested behavior.

The transport must retain each required down/up stage until accepted, rather
than replacing a pending stage with the restored report. Tests must cover both
6KRO and NKRO, endpoint timeout, reset, unlock, remapping while held, both Shift
keys, other modifiers, held Space/Caps and Repeat. Passing a CPU model still
does not prove Windows language switching.

## Source evidence

- `quantum/action.c`, `register_code`: an already pressed basic key is first
  removed and sent, then added again. `unregister_code` removes its bit; there
  is no per-action ownership count. A plain synthetic tap cannot preserve an
  already held Space or Caps Lock.
- `quantum/action_util.c`, `send_keyboard_report`: the transmitted modifiers
  come from real and weak modifier state, and duplicate reports are filtered.
  Writing only `keyboard_report->mods` is not sufficient to mask held Shift.
- `tmk_core/protocol/ch555/ch555_ak820.c`, `send_keyboard`: the transport keeps
  one latest desired report and a pending bit. A later call replaces the pending
  report after a timeout. A synchronous down/up macro therefore has no retained
  delivery queue for the intermediate down stage.
- `quantum/quantum.c`: Repeat history processing precedes the keyboard hook.
  Excluding a dedicated key only in the keyboard hook is too late.
- `tmk_core/protocol/ch555/ch555_ak820.c`, `keyboard_leds`: host LED bits are
  available as `KB_USB_SetReport`. This supplies the Caps state, not the physical
  C indicator's electrical address.
- `keyboards/ajazz/ak820/config.h` declares 82 keylights and their DMA slots.
  `ak820_board.c` initializes all DMA bytes to zero and exposes a slot writer,
  but contains no C/W address mapping or indicator output path. The remaining
  slots must not be guessed to be C/W. An OEM schematic or an independently
  checked ROM trace must establish the pins/slots and polarity first.

## Windows helper boundary

A later helper may report the active window's actual input language. It must
observe window changes and other switching methods, define stale/missing state,
and use RAM status updates. No helper, new protocol or language status bit is
implemented here. Caps counts cannot identify the active language.

## Candidate architecture and event cases

A bounded staged pulse is the preferred next design: wait for the conflicting
key to be released, send a modifier-only stage, send the selected key down,
send key up, then restore the latest physical report. Advance each stage only
after transport acceptance. Transport acceptance is not proof that Windows
acted on the shortcut. A bounded timeout must cancel the sequence safely and
retain any required synthetic release until accepted or USB reset discards the
old session. Normal Caps requests should coalesce; the precise user-visible
meaning of coalescing must be settled before code. Pending requests should be
cancelled on unlock, reset and relevant remap. Cancellation after a down stage
still owes a release; deleting the queue alone is unsafe.

An alternative is to reject conflicting-key activations explicitly. This costs
less state but changes requested behavior and needs a product decision. A
synchronous tap helper or synthetic all-keys-up sequence is rejected because
it loses report ownership or retriggers held input.

| Event case | Required check / unresolved decision |
| --- | --- |
| Dedicated key down/up with no modifiers | Exactly one Win+Space pulse; no release-triggered repeat. |
| Left Shift, right Shift, both Shifts | Exactly one unshifted Caps pulse; restore both current Shift bits. |
| Ctrl/Alt/GUI held, with and without Shift | Mask unrelated modifiers for the pulse; preserve their current ownership afterward. Windows behavior remains untested. |
| Space already down | Decide deferral or rejection; never release/retrigger its owner. |
| Ordinary Caps already down | Same decision for Shift+Caps; never release/retrigger its owner. |
| Modifier pressed/released while staged | Restore current state, never a stale saved modifier mask. |
| Remap while dedicated key held | Preserve cached release ownership; cancel queued action according to an explicit relevant-remap rule. |
| Vial unlock during wait/down/up | Suppress new action; cancel waiting work; deliver any owed synthetic release without affecting unlock keys. |
| Timeout at each USB stage | Do not overwrite an unaccepted down/up; bounded cancellation must avoid a stuck Win/Space/Caps. |
| Reset at each stage | Discard old-session pulse state and recover physical state through the existing reset path. |
| Repeat and Alt Repeat after activation | Repeat the previous ordinary key, never the shortcut or Caps action. |
| 6KRO full report / NKRO | No displaced physical keys and no report-format assumption. |
| Multiple language/Caps requests | Specify ordering, capacity and coalescing before implementation. |
| C/W output | Host Caps bit and non-main layer mask only; verify independently established electrical mapping. |

No event tests were added because no candidate implementation or accepted full
event contract exists. The table is the required test plan, not test evidence.
