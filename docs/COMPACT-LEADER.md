Русский перевод: [Компактный Leader](ru/COMPACT-LEADER.md).

# Compact Leader

Press Leader, then one selector within 300 ms by default to run a Vial macro.

**Before changing assignments or macros:** The published beta.5 catalog does not
authorize settings writes. See [settings backup](SETTINGS-BACKUP.md) and [write-failure limits](QMK-SETTINGS.md).

Leader is available in `main`, `typing`, `code`, `pointer`, `onehand`,
`creative`, `shortcuts` and `multios`, but not `game` or `mmo`. Assign
`QK_LEAD` to a physical key in Vial and edit the desired macro in Vial. For
example, press and release Leader, then press `1` within 300 ms to run macro
slot `0`. The two keys do not type their usual characters; the macro runs on
the next idle matrix tick.

| Selector | Vial macro slot |
| --- | --- |
| `1` through `9` | `0` through `8` |
| `0` | `9` |
| `A` through `F` | `10` through `15` |

Selectors use basic keycodes on the active layer. Shift and Caps Word do not
change the mapping. Encoded modifier keys, tap-hold keys and Space Cadet keys
are not selectors. The published beta.5 feature adds no saved settings. The
unqualified source candidate adds a runtime timeout setting without changing
keymap, macro or Combo storage. The firmware source in this tree can define
`AK820_LEADER_TIMEOUT` at build time from 1 to 1000 ms; the default is
300 ms. For a direct QMK Make build, pass e.g.
`EXTRAFLAGS=-DAK820_LEADER_TIMEOUT=500`; a bare Make variable of that name does
not set the C define. The qualified release builder does not expose this option.
Vial and AK Configurator do not expose the candidate runtime setting. A changed image is an
unqualified development image, not approved for installation without its own
safety, regression and installer checks. Published beta.5 (commit
`78dc69e6f45eac4432949590cc1c9a86c0b1a181`) has a fixed 300 ms timeout and
does not support this build option.

## Cancellation and held keys

Pressing another ordinary nonmodifier keyboard key, including Escape, consumes
that key and cancels the sequence. Modifier keys and other controls cancel the
sequence and perform their normal action. At the configured timeout the
sequence expires; the next key acts normally.
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

See the [profile matrix](MODULE-MATRIX.md) for profiles that include Leader.
Device timing and physical behavior require separate validation; host and linked
CPU tests do not establish them.

A runtime timeout setting is under development. Its record migration and
exact-image qualification are not complete; the installer rejects settings
version 3 until those checks are implemented and reviewed. An erased version 2
or 3 settings record is also rejected during backup interpretation until the
source image's QSID 22 default can be authenticated.
