# Direct fixture metadata correction

`make_backup` derived settings without passing the exact-image Direct
capability. On Direct images, `settings_from_nvm` therefore wrote legacy
`limitations` metadata even though `validate_backup` derived Direct metadata
from the same ROM identity. Canonical settings comparison rejected the fresh
fixture with `Settings JSON differs from validated NVM or RGB contract`.

Fixture generation now passes `direct_capable=image.get('direct_protocol') ==
1`, matching the production capture and validator paths. The canonical
`validate_backup` gate remains in place. The focused test checks that the
exact-image flag is forwarded as true for Direct and false for legacy images;
it does not manufacture a palette sidecar or claim physical capture evidence.

Verification: `python3 audits/beta3-direct-20261026/test_prepare_direct_fixture.py`
passes, and both changed Python files pass `py_compile`. This test isolates the
forwarding contract; it does not exercise a private fresh-main backup
roundtrip. No ROM or settings bytes are included here.
