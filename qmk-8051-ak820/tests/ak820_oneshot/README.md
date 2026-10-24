# Compact One Shot modifiers

`AK820_COMPACT_ONESHOT=yes` adds OSM without the upstream One Shot or tapping
engines. The default is `no`. Tap an OSM key to arm its modifiers for the next
accepted key. Several queued OSM modifier sets combine. Hold OSM to use it as an
ordinary held modifier. Pressing another key while OSM is held prevents arming
when OSM is released.

The modifiers remain owned until the consuming key is released. Rolled ordinary
keys do not consume another slot. While that consuming key is down, a new OSM
acts as a held modifier and cannot arm a new set. This is the one-target limit.
Physical modifier owners remain independent. Clear/unlock cancels both pending
and consumed modifiers. Modifier and layer controls do not spend an armed set.

Matrix and encoder sources are supported. Repeat uses its existing retained
modifier state. OSL, timeout, locking, tap-toggle, upstream One Shot settings and
OSM injected by Vial or macros are outside this initial implementation. There
is no saved One Shot state.

From the QMK directory, run the production host pipeline and complete-image CPU
checks:

```sh
python3 tests/ak820_tapping/run.py --oneshot
python3 tests/ak820_oneshot/linked.py \
  --build-dir .build/one-shot \
  --s51 /path/to/sdcc-4.6.0/bin/s51 \
  --output-dir /tmp/ak820-osm-linked
```

The host fixture checks modifier encodings, held chords, matching physical
owners, rolled keys, the busy fallback, cancellation, Repeat, Caps Word and
Combo output. It also runs 156 existing tap-hold differential traces. The CPU
fixture runs the real linked matrix/action/report pipeline. Neither fixture
establishes physical USB behavior, peripheral timing or interrupt safety.
