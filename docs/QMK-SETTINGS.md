Русский перевод: [Настройки QMK](ru/QMK-SETTINGS.md).

# QMK Settings

QMK Settings adjusts how long the keyboard waits for certain actions and how
some keys behave. A profile is a fixed set of firmware features, not a layer.
All ten profiles include QMK Settings, but the available entries depend on
the profile. These settings tune features already in the firmware; they do not
add a missing feature or remap a key. See the [profile matrix](MODULE-MATRIX.md).

**Before changing settings:** In the upstream Vial GUI source at commit
`aef8222a2d0429a183b2ed692d5f9efcfd383f08`, setting 22 is called Permissive
Hold, while this firmware uses it for the Caps Word language. Save writes all
values shown in QMK Settings, so saving an unrelated setting can silently
change that language. On affected firmware, avoid Save and Reset in standard
Vial QMK Settings until the client and exact firmware image are confirmed
compatible. This finding comes from source inspection, not a keyboard test; it
does not establish the behavior of every Vial version.

## Using the settings

Open Vial, select the keyboard and open **QMK Settings** to view the available
values. Only change and save them with a client confirmed compatible with the
installed image and only when settings writes are authorized. Compatibility
alone does not authorize writes: the published beta.5 catalog does not authorize
them. See [settings backup and transition limits](SETTINGS-BACKUP.md). Settings
are saved across restarts. Reset restores the settings
defaults, not the keymap, macros, Combos or NKRO profile. Do not use standard
Vial Save or Reset on affected firmware as explained above.

In the inspected Vial version, settings appear in tabs with number fields and
checkboxes. **Undo** reloads values from the keyboard without saving edits;
**Reset** asks for confirmation and writes defaults. The controls and their
number ranges are not proof that the installed firmware supports every option
or value: use the firmware ranges below. In particular, the upstream
**Permissive Hold** checkbox for setting 22 is mislabeled for this firmware;
do not use it to set the language.

For example, increase **Combo → Time out period for combos** if you cannot
press both keys close enough together; decrease it if ordinary typing triggers
Combos accidentally. Under **Tap-Hold**, increase **Tapping Term** if a
hold is recognized too soon due to the timer, or decrease it if it takes too
long. Pressing another key can also trigger the hold before the timer expires;
increasing the term does not prevent that. In profiles
with Auto Shift, adjust **Auto Shift → Timeout** if shifted characters appear
too soon or too late. Change one value at a time only when writes are allowed,
then verify the intended behavior and read the value back with a compatible
client. If a readback fails or differs, stop; do not retry or reset blindly.

Defaults are the starting values for a fresh or reset settings record; saved
values can survive a restart or update. The same setting can have no practical
effect when its feature is not present or its key is not used, and behavior
can differ between profiles. Build settings select firmware features or fixed
parameters before compilation; they are not runtime QMK Settings and cannot be
changed by these controls. See [profile matrix](MODULE-MATRIX.md).

The table describes the current source and beta.5 defaults for a fresh or reset
record. Beta.5 is published; current source experiments are separate and not
qualified for release. See [status](STATUS.md). Defaults do not necessarily
replace saved settings after an update.

| Setting (QSID) | What it changes | Range; default |
| --- | --- | --- |
| Grave Escape modifiers (1) | Normally Escape, or Grave with Shift or GUI. Overrides force Escape with the selected modifiers. Only useful in `code`. See [Grave Escape](CONFIGURATION.md#grave-escape). | Flags: Alt 1, Ctrl 2, GUI 4, Shift 8; add them (e.g. 1 + 2 = 3). Default 0 |
| Combo time (2) | Maximum interval between the two keys of a [Combo](COMBOS.md). | 1–1000 ms; 40 ms |
| Auto Shift state (3) | Enables [Auto Shift](COMPACT_AUTOSHIFT.md) and can exclude punctuation, digits or letters. Only `main` and `typing`. | Flags: enabled 1, exclude punctuation 4, digits 8, letters 16; add the desired values. Default 1 |
| Auto Shift time (4) | How long to hold a key for its shifted form. Only `main` and `typing`. | 1–1000 ms; 175 ms |
| One Shot timeout (6) | How long a [One Shot modifier](CONFIGURATION.md#one-shot) waits for the next key. | 0–30000 ms; 0 means no timeout |
| Tap/hold time (7) | Time before a [dual-function key](TAP-HOLD.md) is treated as held; another key press can trigger the hold sooner. | 1–1000 ms; 200 ms |
| Tap-code delay (18) | Delay for certain generated key taps, including text sent by macros. It does not set the timing of dual-function keys, Tap Dance or explicit macro down/up actions. | 0–100 ms; 0 ms |
| Caps Lock tap delay (19) | Delay for generated Caps Lock taps using the same tap helpers. | 0–100 ms; 80 ms |
| Caps Word language (22) | Selects English or Russian rules for [Caps Word](CONFIGURATION.md#caps-word); it does not change the computer's keyboard layout. | 0 English, 1 Russian; 1 |

A retained beta.3 settings record migrates to English Caps Word rules; beta.4
and beta.4.1 records retain their saved selection. Check the saved value after
migration instead of assuming Russian. Record migration alone does not mean a
firmware update is supported: see [settings backup](SETTINGS-BACKUP.md) for
image compatibility and the unqualified candidate's limits. The `0x7e00`,
`0x7e01` and `0x7e02`
keycodes select English, select Russian or toggle the rules for the current
session; they do not change the saved setting. Restart, an explicit write of
setting 22 or a settings reset reapplies the saved or default selection.

A successful explicit write of setting 3 or 22 reapplies its saved state even
if the value is unchanged. Thus saving multiple settings can undo a session-only
`AS_OFF` or `AS_ON` or restore the saved Caps Word language.

When a setting actually changes, active outputs are released and pending input
is cancelled; release any held keys before continuing. A storage error stops the
write and the new value is not applied. Do not blindly retry, reset or restore
after an error.
