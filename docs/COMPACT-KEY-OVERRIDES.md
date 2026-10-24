Русский перевод: [Key Overrides](ru/COMPACT-KEY-OVERRIDES.md).

# Key Overrides

Key Overrides replace a keyboard key when the selected modifiers are held.
For example, Shift + Backspace can send Delete. Eight rows are available in
Vial. Each row selects a trigger, replacement, layers, required and forbidden
modifiers, and modifiers to hide from the host while the replacement is active.

## Supported rows

Triggers are ordinary keyboard keys from `KC_A` through `KC_EXSEL`.
Replacements accept the same keys, optionally with QMK modifier prefixes such
as `LSFT(KC_A)`, or `KC_NO` to send no key. The layer mask selects any of the
six layers. Both sides of the same required modifier mean either side.

All six Vial options are supported: activation on trigger press, required
modifier press or forbidden modifier release; any required modifier; no trigger
re-registration; and keeping the replacement when another key is pressed.
The first matching enabled row wins. Activation on a modifier change checks
that the changed modifier belongs to that row. Changing layers can deactivate
an override but does not activate one by itself.

Only one physical trigger is captured at a time. Other keys continue normally.
A second key press ends the replacement unless the row keeps it active. When
an override ends, the original trigger returns until release unless the row
forbids re-registration. The original trigger also returns when overrides are
switched off, subject to that option. `KO_ON`, `KO_OFF` and `KO_TOGG` control
runtime enablement; the switch is not stored across restart.

Rows with mouse, consumer, system, layer, macro or standalone modifier outputs,
non-keyboard triggers, layers outside the six available layers, reserved option
bits or no activation option are rejected. Disabled rows follow the same
validation rules; an all-zero row is an empty slot. There are no callbacks,
custom contexts or delayed trigger re-registration.

## Integration contract

`ak820_key_override_process()` receives physical records after tapping admission
and Repeat/Caps Word bookkeeping. A false return consumes the physical record
and needs a report send. The unsuppressed modifier argument includes the
compact One Shot owner's modifiers. That owner retains them until the physical
source releases; the override does not clear or copy that ownership.

Before sending a report, `ak820_key_override_sync()` receives the unsuppressed
modifier aggregate and highest active layer. `ak820_key_override_key()` adds
this owner's key to the outgoing report copy. `ak820_key_override_mods()`
projects suppressed and replacement modifiers before Mac/PC conversion.
These functions do not change the shared key report, modifier state or key
reference counts. The projection must be applied to both 6KRO and NKRO output.
A physical key or macro that owns the same replacement usage therefore remains
held when the override releases.

The shared clear path calls `ak820_key_override_cancel()` and blocks held
physical sources. An accepted settings write clears input before persistence. A successful
write reloads rows. A failed durable write leaves the old runtime rows loaded;
input has already been cleared. `reload()` validates each stored row and
disables invalid rows. It keeps eight ten-byte rows without callback pointers.
Storage addresses and journal padding are defined by the shared dynamic-keymap
layout.

## Offline check

Run `python3 tests/test_compact_key_overrides.py` from the repository root.
The C host model checks activation, negative modifier release, deactivation,
modifier projection, independent owners, One Shot owner preservation, runtime
switches and invalid rows. It does not qualify the linked 8051 image, its stack
or interrupt paths, report-hook integration, storage durability or physical
keyboard behavior. Those checks belong to the integrated firmware qualification.
