Русский перевод: [Каталог возможностей](ru/CAPABILITY-CATALOG.md).

# Development capability catalog

`tools/build_capability_catalog.py` creates an offline catalog from fully tested
configured development builds. This is the development part of PLAN §2 and
AKW-012/034. It does not implement a released-image registry, revocation service,
installed-image detector or an approved settings transition.

```sh
python tools/build_capability_catalog.py \
  --build-dir qmk-8051-ak820/.build/example \
  --toolchain /path/to/pinned-toolchain --output /tmp/capabilities.json
```

Repeat `--build-dir` to include several images. Build directories must be beneath
the QMK source root. Run the configured builder's complete qualification first.
Generation reads local files and never opens a device. A missing, stale, changed,
unknown or incomplete input stops generation. An existing output is replaced only
after every selected build passes verification.

The verifier repeats configured-build inspection: compiler input hashes, named
profile, actual linked feature symbols and instruction bytes, IHX/MAP/MEM hashes,
startup, memory windows and resources. It reconstructs runtime safety from the
foreground, startup and IRQ reports, checks their current checker identities,
and compares the summary and configuration report. The required base and
supplemental suites must pass for that image. Retained base logs must stay inside
the build directory and match their SHA256 and parsed test counts, including
aggregate counts. Supplemental logs and current test sources must match. These are local build and host/CPU evidence, not independent
release approval or physical measurements.

JSON uses `ak820-development-capability-catalog-1`. Each image records the model
`ajazz/ak820`, saved-settings schema, features, fixed limits from bound compiler
source, fixed profile timing, linked resources and artifact/evidence hashes.
The CODE identity uses `sha256-code-windows-zero-v1`. SHA256 covers the ASCII
prefix `ak820-code-windows-zero-v1`, a NUL byte, then each ordered range's start
and exclusive end as four-byte unsigned big-endian integers, followed by every
byte in that range. Ranges are `[0x28a0,0x3000)` and `[0x3027,0xc700)`; absent
IHX addresses are filled with zero, matching the packer's application clear
before it overlays linked CODE. JSON includes the ranges, fill byte and covered
byte count. Extra nonzero bytes in gaps change the identity. Explicit zero
records and implicit zero fill describe the same bytes. Repeated identities
are rejected. Ordering and JSON formatting are deterministic; catalog entries
contain no timestamps or local build paths.

This fingerprint identifies the two linked CODE windows. It does not cover the
packer's generated startup/IRQ area, settings, protected regions or a whole
installed image. A future detector must read every byte of both windows,
including gaps, and separately verify all outside-window image regions using
the bound IHX and packer contract. Matching only occupied IHX addresses or
ignoring unknown bytes cannot establish an installed-image identity. No device
detector is implemented here. Private OEM reference bytes are not exported.

Report hashes establish local consistency, not signatures or authentication.
Self-supplied reports and logs cannot establish independent review.
Source support, a qualified development image and installed firmware remain
separate. A source feature or a profile name cannot identify an installed image.
A future consumer needs complete installed-image verification before showing
that image's development capabilities. Partial reads and unknown images provide
no capability authorization. The development catalog explicitly sets
`release_approved` and `hardware_validated` to false, grants no settings writes
or flashing, and lists no compatible transitions. A release catalog may
separately approve exact images for a beta installation test; that does not
change physical-validation status or authorize settings writes. Existing
installer checks and fresh per-operation confirmation still apply.
