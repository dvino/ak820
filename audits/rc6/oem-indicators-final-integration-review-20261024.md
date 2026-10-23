# C/W integration review

Review date: 2026-10-24. The exact source policy and offline qualification are approved for CI
reproduction. Public CI, fresh bundle acceptance and device behavior remain
separate checks.
No device was opened, reset, programmed or flashed during this review.

## Settings source scope

The settings-source change is approved for host-source binding. It appends the
fourth exact image pair to the ordered allowlist and extends the in-memory
transition model to all sixteen pairs. The unchanged runtime requires the
exact IHX and permanent CODE pair, embedded manifest and schema; backward
transitions and a mismatched target snapshot remain rejected before setters.
This approval does not approve a new firmware package or an installed change.

The new pair is IHX
`45f28e80cd9e269cb507d6fff47b43cea2766b00967912599a98b036b638011d`
and permanent CODE prefix
`cc5af6cc86724103fbc3e2c1815bf7a2235edc0ed85a932fd3e993cd6b4f7931`.
An independent hash of the locally packed permanent image confirmed that
CODE prefix over `0x2800..0xc700`. The private image is 51,136 bytes, SHA256
`5840ad705c66459f006e55661225afdcb4a11650aaefb59d9daf8d70798f3eba`.
The main-checkout packing metadata binds that image to the exact IHX and MAP
`9295030abd133d57048486721f222f83d27a0420aaa4369b92ad538776b0e5b2`.
Private image bytes are outside Git. An independent temporary bundle using
the main IHX, MAP, build report and retained Vial definition also passed the
production `load_profile` function with the private OEM full ROM. It returned
the same exact IHX/CODE pair, schema `0x082002` and four compatible profiles.
The temporary bundle was removed after the check.

The English and Russian settings guides agree with the ordered profiles and
separate the in-memory model, local packing, CI/release qualification and
untested device behavior. README, indicator guides, STATUS, TESTING, resource
budget, roadmap and indexes were reviewed in both languages while they still
reported full qualification as pending. Those final claims must be checked
again after qualification is recorded.

The independent command `python3 -m unittest discover -s tools/installer -p
test_settings_backup.py -v` passed all 23 tests in 102.364 seconds, with no
skips. This includes the sixteen-pair matrix: ten same-image/forward pairs
accepted and six backward pairs rejected. Corruption, storage faults, target
identity mismatch and write-stop checks also passed. These tests use an
in-memory device model; they send no commands to a physical keyboard.

## Binding checks

All 615 policy source records and 21 shared host records match current bytes.
The packing receipt and legacy installer review contain the same host table;
the legacy manifest's nine bundle records also match current bytes. Installer
approval binds the legacy manifest hash
`e9137148a111581969158b69403a809817ccdf9650bce910ace83b1469d40d3b`.
Its firmware remains the legacy `f1c4347e...` image.

All 468 build input records, including the pinned toolchain inputs, and all
78 artifact records match their current hashes (and recorded sizes where
present). The new policy hash is
`93f60dcf6ac827c2315e88fff8fd266168585aaf330429128900954a3f2184b7`;
it binds packing receipt hash
`3ca05df08d592743c9b5fb8f027edd168c671b4cd23634f014656a5ba2a8cd32`.
The normalized symbol hash is
`11e50e3e0d6e1e9831d4ca85822a65306907753bed5000f7d4301f69af8ade06`.
## Final offline approval

The complete retained qualification passed all 26 required suites, 258 unit
tests and zero skips with unchanged exact IHX/MAP. All 26 saved logs and the
27-file retained evidence manifest match their recorded sizes and hashes.
The suite commands match the required host/linked contract, including guarded
erase; the recorded compiler and simulator match their actual pinned hashes.
The 12 RGB and 11 indicator expected/actual observations match. All 65 linked
tap-hold cases match their snapshots and supplied HID/callback expectations.

The final English and Russian STATUS and TESTING changes accurately record
that local result separately from pending CI, package acceptance and physical
behavior. LeakSanitizer exclusion is explicit; ASan/UBSan remain active. INSTALL
now documents selecting a released bundle in a clean matching-tag checkout
and preserves exact verification, fresh backup and per-update confirmation.
No blocking source, ABI, settings, documentation or evidence disagreement
remains. The exact policy is approved for CI reproduction in
`ci/program-review.md`.

This is offline approval. It does not establish native interactive Windows
acceptance, physical C/W connection or polarity, key/encoder timing, physical
USB behavior, IRQ overlap, durable storage, reset execution or an installed
image. The macro cancellation fixture uses the disclosed simulator hook.
No authorization to flash is created by this review.
