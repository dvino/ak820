Русский перевод: [Независимое ревью](ru/REVIEW.md).

# Independent RC6 review

Date: 2026-10-23. This review covers local source, documentation and offline
evidence. It does not authorize a device write or establish hardware operation.
The previous image passed independent offline review with no open correctness
findings. The requested Vial layout-gap change has now been checked against a
fresh linked image and its definition-page/GUI test. The binding below names that
image; the old geometry baseline remains historical.

## Independent ownership and scope

- The firmware reviewer authored portable build paths and guarded Alt Repeat/count
  changes; the RGB reviewer independently reviewed the Repeat changes. The root
  reviewer checked the copied build manifest against the original checkout.
- The RGB reviewer authored reactive lighting, compact CIE and the read/merge/block
  flash fix. The firmware reviewer independently inspected the flash bounds,
  aligned buffer, preserved neighboring bytes and unchanged journal commit order.
- The installer reviewer authored first-install backup, factory migration,
  permanent/trial orchestration and standalone GUI. The firmware reviewer reviewed
  these paths with the English/Russian installation instructions and reran all
  43 installer/GUI tests. The installer reviewer independently reviewed the root
  release builder and documentation.
- The RGB reviewer independently reviewed the root keyboard-check runner. Three
  findings were closed: fixed output directories prevented reruns; hashing only
  after tests could mix images; the RGB deviation wording described only the
  maximum input instead of the full 0–160 interval. The runner now uses distinct
  temporary directories and checks initial, per-suite before/after and final IHX
  and MAP identities. Two regression tests cover reruns and transient replacements.

## Findings and closure

The old byte-program path could acknowledge a command without persisting journal
metadata on the captured RC5 device. RC6 stages the current 64-byte page, merges
the requested bits, then uses the aligned DPTR block path. This preserves neighbors
under either overwrite or bit-setting models. Readback and commit-last checks remain.
The exact controller failure mechanism and the fix's real electrical behavior
remain unverified; CPU fixtures explicitly model those effects.

The Vial geometry follow-up changes only `info.json`, `vial.json` and the
definition assertions. Delete is at x=14.0 and its right edge aligns with the
two-unit Backspace at x=13.0; the F12-to-Delete gap remains 0.25u. The five-key
navigation column is at x=15.5, while the Right arrow remains at x=15.25. The
encoder press matrix IDs and the two rotation IDs remain unchanged; rotations
are at x=16.75 and x=18.0 with 0.25u spacing. The stock Vial web layout schema
does not represent the encoder press as a round control, so this review does not
claim a round press rendering. The linked C52 definition reader and actual GUI
`reload_layout`/KLE path pass 101/101 definition cases and retain 83 physical
keys and two encoder directions. HID is mocked; hardware validation remains false.

The GUI's unconditional power-loss claim was replaced with boot-marker retention
and an explicit cold-boot validation limit. Release bundles exclude OEM full/native reference images. The installer validates
a fresh complete device backup and creates session-private references automatically. Default
No preparation, exact lowercase `yes` write consent and rejection of every corrupted
required release file are covered by host tests. No correctness finding is waived.

The OEM-free host follow-up independently reviews all 15 `HOST_FILES` inputs,
with particular attention to the six changed files (packer, transport, release
builder, Windows builder, installer and GUI). No new runtime correctness blocker
was found. Protected loader/tail and complete factory or Fn-layer code hashes,
boot marker and native profile zero gate capture. Mixed code is rejected. A full
65,536-byte backup and settings reread precede private reference creation; the
transport rereads the full ROM before loader transition and requires exact backup
equality. Preparation defaults to No; lowercase `yes` binds image/mode/hash before
mutation. Phase guards recheck device state/path before reset, erase and restart.
Recovery requires the exact personal session and an already visible loader; no
automatic reset, retry or rollback is claimed.

The external OEM capture review's P1 synthetic package setup regression and P2
installer fixture dependency are closed: generated fixtures exercise real native
validation with fixture-specific immutable hashes, without requiring OEM files in
the checkout. Independent Windows reruns passed 47 installer/GUI tests, 17
`test_build*.py` tests, 64 package tests (two platform skips) and two runner tests.
The root separately ran the Linux/SDCC package suite: 67 tests passed with no
skips (`host/runs/rc6-resume-linux-package.log`). The root also refreshed the
private production-pin check: 13 fingerprint/settings/mutation checks and six
trial/permanent/restore packing/readback outputs passed; this is distinct from
synthetic tests and remains offline (`host/runs/rc6-oem-real-fixture-validation.json`).

The builder accepts owner-supplied `--oem-reference-dir` only for offline packing
validation. Its eight release files exclude the OEM pair; Windows `package_files()`
uses an allowlist of reviewed host files and manifest-bound release inputs. Normal
installation needs no separate reference download; `--reference-dir` is optional
for an owner's exact historical pair. Runtime payloads retain an 87-byte OEM erase
helper copied from the private ROM. Removing references or sanitizing settings is
not a vendor-code-free or unrestricted-redistribution conclusion. The prior public
sanitized-reference descriptions are superseded. Rebuilt release approval and
standalone executable validation remain separate artifact checks; this source
review does not authorize flashing.

Final documentation consistency review closed two minor findings: STATUS now
distinguishes the historical 43-test run from current 47; BUILD now supplies a
fresh output directory and explains promotion to the installer's fixed release
path. English/Russian wording agrees; `tools/check_docs.py` passes 31 documents.

## Evidence levels

| Evidence | Result and limit |
| --- | --- |
| Linked feature scenarios | 33 PASS, including 512 count-update states, Alt Repeat mappings, remap, unlock and overlapping owners |
| RGB CPU | 12 PASS; simulated peripheral state |
| IAP CPU | 11 PASS, including 12 encoder writes and 36 neighbor cases; modeled flash behavior |
| OEM IRQ CPU | 5 PASS; 153-byte stack span, conditional IRQ bound 42 and main reserve 80 leave 31 bytes |
| Startup | CRT and permanent two-entry checks PASS; no cold-boot hardware proof |
| Installer and GUI host | 44 installer + 3 GUI PASS; independent current-source rerun, no physical write |
| Release bundle, Windows recipe and combined runner | 7 + 3 + 2 PASS on current source |
| Vial geometry definition | 101 PASS against the fresh linked image; 83 GUI keys and two encoder directions; mocked HID |
| Fresh final3 regression rerun | features, IRQ, definition, layout-host, layout-CPU, IAP, RGB, recovery and startup all exited 0; linked reports identify the new image where applicable |
| Earlier combined offline rerun | All 17 suites PASS on the pre-geometry image `12260272ccf410b434e28aa661bce8f3f44baff6192b094f3df5f21c5c07e114`; historical runtime baseline, not a final3 full-suite claim |
| Earlier release builder review | 17 PASS, independently reported by the installer reviewer |
| Original-checkout binding | The root reviewer validated 465 build inputs against the original checkout; this reviewer independently matched the geometry JSON, test runner and final3 reports |

The geometry-bound candidate occupies 39,282 CODE bytes (37,423 main and 1,859
low) and 2,071 XRAM bytes. CODE headroom is 1,223 bytes: 1,194 main and 29 low;
the inclusive maximum code address is `0xC255`. The prior 39,262-byte candidate
is the explicitly pre-geometry comparison used by `SPACE-OPTIONS.md`; it is not
the current image. Four layers yielded exactly the same CODE/XRAM sizes; the
full-CIE control used 216 more CODE bytes. These are offline build measurements,
separate from installed RC5 and future hardware tests.

The local personal permanent image was regenerated from the exact geometry-bound
IHX/MAP and the verified trial readback. Its 51,136 bytes match SHA256
`f90a40dcad7364f2278fa5daf2bfa444060140a71401b2c4595bb035aff6aebe`. The
existing packer verifier accepts both local trial and permanent images, and the
permanent image's complete 10,240-byte NVM region is byte-identical to the
captured readback (`04885d9fcabe876947f003cf82dc246ab83bfcdd878c22d89e30463c48a9bfe5`).
The original native restore image remains present. Dirty RAM and uncommitted
journal data are excluded. This checks local preparation only; the captured
snapshot can become stale and does not establish RC6 hardware operation.

Standalone Windows executable packaging and GUI smoke results are recorded
separately in the final status; reviewing this source does not establish that an
executable has been built or that a physical installation succeeded.

The Fn+F12 report was resolved as a different physical key combination. The
captured installed RC5 bindings and eight CPU scenarios confirm F12 transparency
and the RGB toggle on Fn+Delete, including either release order. This required no
firmware change and is not an open RC6 defect.

## Exact reviewed inputs

```json
{
  "format": "ak820-offline-review-2",
  "release": "rc6",
  "status": "passed",
  "hardware_validated": false,
  "build": {
    "ihx_sha256": "7c25096e59412afc7a4aa1c030a7038c4b5d469a253319ef712ce4244c91ffb9",
    "map_sha256": "acf0120ef621b3212c8fcf28ff5543e0c9010cb10c70bd5fff1aba15745dd5de",
    "build_report_sha256": "f261b8cae83f8d05d0eb0d0523d3264e26f553f480279c7dd76532bc4030445b"
  },
  "resources": {
    "build_id": 532482,
    "code_bytes": 39282,
    "code_main_bytes": 37423,
    "code_low_bytes": 1859,
    "xram_bytes": 2071,
    "max_code_address": "0xC255",
    "free_code_bytes": {
      "total": 1223,
      "main": 1194,
      "low": 29
    },
    "packed_device_update": false,
    "vial_geometry": {
      "info_json_sha256": "4f951f956ce11ad3efc3c692669c1da833dd07875940a67055356ba6e625c5aa",
      "vial_json_sha256": "080192880c40c102022fe6b75dc865b1d36638ffd4e6585cfd429eed3478c071",
      "definition_runner_sha256": "9d0535ee9296a936134323cecf150c173fc3e38d72d989e5f1cb494361b7fa45",
      "definition_result_sha256": "f2aed329d77391763cef77e6bbdb7838a90093eb0abacdb9f34bb665e82274f9",
      "result": "101/101 PASS; linked C52 reader plus actual GUI reload_layout/KLE; 83 physical keys, two encoder directions; mocked HID"
    },
    "final3_suite_reports": {
      "directory": "qmk-8051-ak820/.build/rc6-final-3",
      "features": "ee340f1829c332ddf6ffd8e8f9d9a936475a3d29ad5aa103a089ff270e3d8f17",
      "irq": "1d472cc74db0ea4659e5d459353691860ba82c50ce2750ecef09bcc7a7a84383",
      "definition": "f2aed329d77391763cef77e6bbdb7838a90093eb0abacdb9f34bb665e82274f9",
      "layout_host": "67b4d944d58d302ae1277756772e648af0cddc5231ba64949daa40deed203d0f",
      "layout_cpu": "e0c08787e11c10e8551dfa5b533ad4eb12678f97a4421c881c5f0778ce09d8a8",
      "iap": "b143d35682711fa7acce6a6588cc06e87449c79fa9391d7b08411e58b21298db",
      "rgb": "05c4793567b37c4e32302779071781184fed8fea1f5f3611bd3ca4aba8fa3b3e",
      "recovery": "dc4967f038cf4728e582712fc4aa4ae86d9b5bdc7810ded9e1ae1408cf0e814f",
      "startup": "19febdf73eacc5e865ad8b2ca91ce92aa54137f3781ccf6304360946cf15c2de"
    },
    "personal_image": {
      "path": "host/runs/20261023-rc6-final-ready/ak820-vial-permanent.bin",
      "size": 51136,
      "sha256": "f90a40dcad7364f2278fa5daf2bfa444060140a71401b2c4595bb035aff6aebe",
      "nvm_source_sha256": "04885d9fcabe876947f003cf82dc246ab83bfcdd878c22d89e30463c48a9bfe5",
      "hardware_validated": false,
      "physical_operations": 0
    }
  },
  "host_files": {
    "AK820.cmd": {
      "size": 1149,
      "sha256": "dddbfaad0da2f79d3353bd2238eae323db53b0a066736c7743e84a845b77aaa0"
    },
    "AK820.sh": {
      "size": 515,
      "sha256": "9a8ebbc2ed64d2d0ac6ea7f4d1251d5de630c8af78465dee3acfdc833b4528fb"
    },
    "qmk-8051-ak820/util/ak820_diagnose.py": {
      "size": 13505,
      "sha256": "2a3dd74d73d1b135107468d330818896a7158e16f4e4031b1c1757f14854dc0d"
    },
    "qmk-8051-ak820/util/ak820_release_manifest.py": {
      "size": 2247,
      "sha256": "94fd30533d4c31912fba46b09a0ae0eb61a092f93603dcd89ece785dbdea4f0d"
    },
    "qmk-8051-ak820/util/ak820_tool.py": {
      "size": 18808,
      "sha256": "3783cc757cea09cf61a6267dc19ea42302d4c93d9d444d6281cf8fc60270f47a"
    },
    "qmk-8051-ak820/util/native_macro_import.py": {
      "size": 2499,
      "sha256": "572f153de6ec9a71eefa8fd87c5ba2bd7da602619131e3ec66fa63d9a742b07f"
    },
    "qmk-8051-ak820/util/pack_ak820.py": {
      "size": 23558,
      "sha256": "9e2454b0aaa790874bbb7117680c67fd134b45d4ece7281bf6b5b8ea17e59a7f"
    },
    "qmk-8051-ak820/util/prepare_ak820_trial.py": {
      "size": 5745,
      "sha256": "91458b9a14bad55f9bb9a056ec43f8daec0ffe996f21f4ffc15e9f6730aa9fc2"
    },
    "tools/build_release_bundle.py": {
      "size": 9399,
      "sha256": "c1ddd711e6e27fccd3f31d9a05f5395581af0c743f2909327a155867c8dd6ca8"
    },
    "tools/build_windows_installer.py": {
      "size": 3692,
      "sha256": "53fb19ad029610154a7a1c6a10d616f0f1c9f25ea6215eb44a36e84671a4bd09"
    },
    "tools/installer/70-ak820.rules": {
      "size": 339,
      "sha256": "f0b85bb730963057350a6a9cfe35e1f17e2859a5bfbcebfce9fccaa6534a3a52"
    },
    "tools/installer/ak820.py": {
      "size": 36800,
      "sha256": "86b4f52f0e222252a18eda4de2f5111b745667865f7c3193b084dd2d5f85f8f8"
    },
    "tools/installer/gui.py": {
      "size": 7006,
      "sha256": "2586fff5f99794e4d832ddf7ca33e6c6d1f5911b36ab14919a473076aa270a7c"
    },
    "tools/installer/requirements-build-windows.txt": {
      "size": 235,
      "sha256": "fe92377176d05e83a805899a51be8569cfc63768609bae64c543641f9d715bd5"
    },
    "tools/installer/requirements.txt": {
      "size": 15,
      "sha256": "6e78c6c5a61dbebf36f570a14685c795efcdb3d8bb6b6118b6aa78dd0aca54d4"
    }
  },
  "scope": "Independent source, documentation, host and linked CPU review; no device write approval",
  "open_correctness_findings": 0,
  "standalone_executable_validation": "separate artifact check pending; see STATUS",
  "host_followup": {
    "date": "2026-10-23",
    "independent_windows_tests": {
      "installer_gui": 47,
      "build_tools": 17,
      "package": 64,
      "package_skips": 2,
      "runner": 2
    },
    "root_linux_package_tests": 67,
    "root_linux_package_skips": 0,
    "production_private_validation": {
      "fingerprint_settings_checks": 13,
      "packing_readback_outputs": 6
    },
    "firmware_identities_rehashed_unchanged": true,
    "device_operations": 0,
    "docs_check": "31 documents; 0 failures"
  }
}
```
