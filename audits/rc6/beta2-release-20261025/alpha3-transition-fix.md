# Alpha.3 settings transition correction

Offline planning passes from the authenticated public alpha.3 image to all ten
beta.2 profiles. The catalog and web matrix add only its immutable historical
IHX/CODE descriptor and ten explicit outgoing edges. No installer runtime,
firmware, feature implementation or test source changes are included here.

The public ZIP SHA256 is
`3c8ac08db82141a00468bb0839b972d1bdb6ac16652ade89d5f65706448a4d97`.
`load_profile` reconstructs alpha.3 from that bundle and private OEM bytes,
checks IHX `d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`,
and verifies packed CODE
`01f0f7a979d8cfa8217b3bba333758ae3509cf7f3f8e35fbffb1ed034b808e5d`.
The alpha.3 tag resolves to `b17d7c8b52ec7a234a742a64380e22354698030b`.
The JSON records hashes of its Combo, storage, RGB and packing contracts.

The canonical matrix retains the original 120 case objects and appends ten
actual `plan_restore` results: 498 key assignments, 12 encoder assignments,
16 macros, eight Combo slots, schema02 to schema03, preserved target default
extensions and checked RGB translation. The policy producer requires 130
cases and 13 incoming cases per target.

Ten separate nondefault fixture plans preserve a basic key, encoder key,
nonempty Combo and RGB effect 31 with HSV, brightness and speed. Four negative
cases retain rejection for a missing edge, unsupported target NKRO keycode,
an unsupported Direct effect and Direct without a palette getter. Fixture
NVM changes are deliberately offline; they are not device captures.

`produce_alpha3_transition.py` creates new private output directories with
mode 0700 and files with mode 0600. The public JSON/log contain no OEM or
backup bytes. `alpha3-transition-fix.log` records the successful execution.
No USB operation, live settings capture or physical migration was performed.
This evidence does not establish durable restore or device behavior.
