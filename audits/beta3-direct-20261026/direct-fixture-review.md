# Direct fixture correction review

Scope: `make_backup` in `prepare_release.py`, the focused regression, and
`direct-fixture-fix.md`. Production firmware and installer code were read for
comparison and were not changed by this review.

The added `direct_capable=image.get('direct_protocol') == 1` argument matches
`capture_settings` and `validate_backup` in `tools/installer/settings_backup.py`.
The flag changes the derived limitations text to the exact-image Direct
contract. It does not create RAM palette data or claim a physical capture.

`validate_rom` still runs before derivation. `_rom_identity` requires one
reviewed CODE hash and its matching manifest. The final `validate_backup`
still verifies the saved ROM, NVM, hashes and canonical settings comparison.
Unknown-image rejection and the canonical gate remain intact. The fixture
file set still contains no `direct-ram.json`, and its scope explicitly states
that it is derived offline without getter validation.

Independent verification on 2026-10-26:

```text
python3 audits/beta3-direct-20261026/test_prepare_direct_fixture.py
Ran 1 test in 0.005s
OK
```

The test covers forwarding true and false from the resolved identity. Its
parser and validators are mocked, so this result does not establish a real
canonical backup roundtrip. The correction note states that limit accurately.
Strict preparation with fresh private inputs remains a separate release gate.
No firmware builds, device commands or full measurement runs were performed
for this bounded review.

One minor review item concerned a test comment that implied canonical parser
coverage despite the mocks. The corrected comment explicitly describes
forwarding-only coverage and mocked parsers and validators. The item is closed.
The bounded correction is accepted; no implementation findings were identified.
