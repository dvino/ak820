Русский перевод: [Управление мышью с клавиатуры](ru/COMPACT-MOUSE-KEYS.md).

# Compact Mouse Keys

`AK820_COMPACT_MOUSEKEY=yes` enables the compact AK820 implementation and
`MOUSEKEY_ENABLE`. It uses the existing HID mouse report and shared USB endpoint.
Map these keycodes in Vial when using a firmware build that includes the option:

| Action | Keycodes in this QMK version |
| --- | --- |
| Move the pointer | `KC_MS_UP`, `KC_MS_DOWN`, `KC_MS_LEFT`, `KC_MS_RIGHT` |
| Hold or release a mouse button | `KC_MS_BTN1` through `KC_MS_BTN5` |
| Scroll vertically | `KC_MS_WH_UP`, `KC_MS_WH_DOWN` |
| Scroll horizontally | `KC_MS_WH_LEFT`, `KC_MS_WH_RIGHT` |

A direction press attempts its first movement immediately. Held cursor directions
repeat by 8 report units per axis every 20 ms; held wheel directions repeat by
one unit every 80 ms. Pointer scaling, acceleration and scroll distance depend
on the operating system and application. Opposing directions cancel on their
axis. Perpendicular directions combine without diagonal normalization.
Hold a button while moving to drag. Button events and direction releases do
not add movement.
Pressing another direction restarts the interval for its cursor or wheel group.

Speed is fixed. Acceleration keys `KC_MS_ACCEL0` through `KC_MS_ACCEL2` and
buttons 6–8 have no effect. The standard QMK mouse acceleration settings do
not configure this implementation. Key names and their general meanings are
listed in the [QMK Mouse Keys documentation](https://docs.qmk.fm/features/mouse_keys).

A busy USB endpoint drops relative movement rather than queuing a later burst.
The latest button state is retried until accepted, including a final release
and the release caused by clearing keyboard state. A delayed task sends at most
one report per call and restarts its repeat interval from the current time.
