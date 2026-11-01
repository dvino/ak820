# Review closure — beta.5 integration, 2026-11-01

Two independent reviews of the integration state (firmware: del_mvx5x0s7_zahf;
host/release: del_mvx5xc1d_y6zi). Every finding below records disposition and
evidence. All retests below run on the current dirty worktree of
/home/agent/work/ak820 (main @ 78dc69e6 + integration changes).

## Host/release review

- BLOCKER B1 — `DeviceAPI._require_writes` implicit unverified branch
  (`tools/ak820_device_protocol.py`). Fixed: explicit `verification=()` opt-in
  for non-production doubles; verified production paths always bind a real
  release/session/approval triple, otherwise
  'Approved release, recovery session and approval are required'.
  Test doubles updated to `verification=()` at 8 construction sites
  (tools/test_ak820_device_protocol.py:36,221;
  tools/test_ak820_extension_settings.py:55,76,90;
  tools/installer/test_settings_backup.py:272;
  tools/installer/test_catalog_settings.py:773,808).
  tools/installer/test_settings_workflow.py run_scenario hand-built context
  (mocked workflow.prepare) gained `'verification': ()`.
  Spec test tools/test_ak820_leader_v3.py::test_untrusted_downgrade_binding_cannot_reach_transport
  now passes (was failing before the fix).
  Retest: device_protocol OK, extension_settings OK, leader_v3 OK,
  write_identity OK, installer test_settings_backup / test_settings_workflow /
  test_catalog_settings OK (`python3 -m unittest`; the script-mode
  '__mp_main__' vs '__main__' difference in the spawn test is an invocation
  artifact, the test passes as a module).

- MAJOR M1 — per-write identity revalidation in owned_setter finally caused a
  full bind()+read_code(0,65536) sweep per differing setting on restore.
  Fixed: `if not self._setter_depth and not self._restore_active:
  self._invalidate_write_identity()` — identity verified once per restore;
  the per-write file guard still revalidates pins.
  Retest: test_ak820_write_identity OK; installer restore suites OK.

- MINOR m2 — cryptic erased-record message at tools/installer/settings_backup.py:420.
  Fixed: message now states the record is erased (all zero/0xff), the image
  version is 2 or 3, and the code refuses to invent defaults without the
  authenticated QSID 22 backup record.
  Nits (settings_backup.py:173-177 assumes the 300 ms image default —
  the fallback matches the release image default; ak820.py:911) accepted with
  this note.

## Firmware review

- MAJOR — experiment seams `AK820_PH_ACTION_SEAM` / `AK820_PH_SEAM`
  (quantum/action.h, quantum/action.c, quantum/action_layer.h/c) plus 8
  untracked keyboards/ajazz/ak820/ak820_ph_*.{c,h}.
  Verified: no release profile, config or build script defines `AK820_PH_*`
  outside tests/ak820_tapping (zero matches in tools/, keyboards/ build files);
  the seams compile to nothing unless a test harness defines them.
  tests/ak820_tapping/ph_action_seam_test.py pins the `action_exec` body to
  ph_action_seam_legacy.fixture and proves the disabled seam adds zero
  instructions; the seam body is a deliberate alternative pipeline, not a
  synced copy. Closing as accepted experiment surface: files kept in place
  (moving them would touch 41 references across 33 frozen harnesses for no
  release effect), with a header comment at quantum/action.h pointing to the
  pinning test.

- MINOR — canonical gate did not check xmod stage presence
  (util/build_ak820.py). Fixed: gate now requires
  `(xmod_result is not None) == bool(args.tail_share_xmod)`. Canonical builds
  with `--tail-share-xmod` remain eligible (int6-main evidence
  'ak820-canonical-pass30-inputs-1' was verified with xmod enabled).

- MINOR — tests/ak820_autoshift/linked.py:115-152 combo_trace_result accepts
  either oracle. Accepted: both rotation directions are validated on host
  elsewhere in the suite; the dual-oracle helper only selects which trace a
  case asserts. Recorded, no change.

- MINOR — ak820_leader.c:20-24 byte-per-source leader_suppressed under
  AK820_COMPACT_KEY_OVERRIDE. Accepted: opt-in define, not enabled in any
  release profile.

- NIT — xmod `.globl` emission: already single-symbol lines in
  util/ak820_tailshare.py:123 and util/ak820_tailshare_xmod.py:229. No change.

- NIT — Caps Word both-Shifts gesture independent of
  DOUBLE_TAP_SHIFT_TURNS_ON_CAPS_WORD: defaults preserve release behavior;
  documented as a gesture switch. No change.

## Verification status

Combined main image unchanged by this closure: int6-main, ihx
sha256 3e5b53ff49e11e3bfd204289569cd9e77e55ae9e6bb05ed962dc843e9f3877b3,
code_bytes 40405, endpoint 0xc6a5, stack gate 165/183, canonical contract
ak820-canonical-pass30-inputs-1, full offline qualify 36/36 PASS.
The only firmware-source touch here is a comment block in
quantum/action.h; no release code changed.
