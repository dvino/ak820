Русский перевод: [Компактный Leader](ru/COMPACT-LEADER.md).

# Compact Leader

Press Leader, then one selector within 300 ms to run a Vial macro.

The curated `work` package includes a one-key Leader sequence. Assign
`QK_LEAD` in Vial, press it, then press one selector within 300 ms. The prefix
and selector produce no ordinary key output. The selected Vial macro runs on
the next idle matrix tick. Edit its contents in Vial as usual.

| Selector | Vial macro slot |
| --- | --- |
| `1` through `9` | `0` through `8` |
| `0` | `9` |
| `A` through `F` | `10` through `15` |

Selectors use basic keycodes on the active layer. Shift and Caps Word do not
change the mapping. Encoded modifier keys, tap-hold keys and Space Cadet keys
are not selectors. This feature does not add saved settings or change the
existing keymap, macro or Combo storage layout.

## Cancellation and held keys

Pressing another ordinary nonmodifier keyboard key, including Escape, consumes
that key and cancels the sequence. Modifier keys and other controls cancel the
sequence and perform their normal action. At 300 ms the sequence expires; the next key acts normally.
A new, released-and-pressed Leader prefix restarts the timeout. Duplicate
presses of a held prefix do not restart it. Only one macro can wait for an idle
tick; additional prefix presses while it waits are consumed and ignored.

Keys held before Leader keep their normal release. Leader consumes the release
of each prefix or selector whose press it consumed, even after a layer change.
Clearing the keyboard, changing NKRO mode or starting Vial unlock cancels the
sequence and any macro waiting to run. Held keys must be released before they
can act again after that cancellation.

## Other features

Leader accepts physical matrix keys only. Encoder and virtual Leader triggers
are unsupported. Macro-generated keys, Repeat output and Combo output cannot
start or select a Leader sequence. Prefix and selector keys bypass Combo,
Repeat, Caps Word and One Shot processing. Any earlier buffered Combo input is
resolved before the prefix starts. Existing tap-hold handling resolves a prior
pending hold before admitting the prefix.

A queued One Shot modifier remains queued until the next ordinary consuming
key. Leader controls do not consume it. Macro output follows the existing Vial
macro rules: effective held or queued modifiers can affect that output, and
normal macro actions can change Caps Word or Repeat state. The existing Vial
interpreter runs synchronously once dispatched; this feature adds no second
macro engine or output queue.

The `work` package is the curated profile that includes Leader; the low-level
CLI also retains compatible historical names. Device timing and
physical behavior require separate validation; host and linked CPU tests do
not establish them.
