# E24 investigation record — encoder-default lookup specialization

Findings (read-only, maps and sources only):

1. `_keycode_at_encodermap_location_raw` in `qmk-8051-ak820/quantum/keymap_introspection.c:98` is **inlined** by SDCC into `_keycode_at_encodermap_location` (dynamic_keymap); no standalone CSEG symbol exists in any recent map (exp21 b2, exp24 b2). Its D: sloc entries remain. My earlier "symbol absent" observation described linkage reality but did not mean the code is gone; an inlined-body change can still shift size.
2. exp24 candidate build failed: `Linked code outside permitted interval: 0xc700..0xc751` (50 bytes over). Claimed delta vs clean 0xc754 is 3 bytes.
3. exp24's own baseline build b1 reported `highest_address 0xc921` (41,041 code bytes) — a different, larger baseline than the combined baseline 0xc754. Baseline provenance across copies is therefore not controlled; the 3-byte attribution is as unproven as E22's.
4. Ledger already records E23 stopped before implementation and E24 "in progress"; reviewer f968fa53 exists.

Verdict: **do not apply E24 as a main-image saver.** Expected effect ≤3 bytes with uncontrolled attribution; the direction cannot close the 30-byte E21 gap. The encoder-getter idea is closed unless a future profile image actually links the raw getter standalone. Recorded in ledger context; no source changes made.
