# Source cleanup production build review

Independent review, 2026-10-23. PASS for offline assembly of the exact build
and current sixteen host files recorded below. This does not approve a commit,
installer approval, publication, USB commands or hardware flashing.

The build is qmk-8051-ak820/.build/source-trim-production-sdcc46-20261023.
I independently ran validate_tools, including validate_inputs, against the
current source and toolchains/sdcc-4.6.0. All 465 input records match. All 76
artifact records match their actual size and SHA256. The diagnostic build gate
passes. The IHX is byte-identical to the previously reviewed SDCC 4.6 candidate:
f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e.
CODE remains 38,100 bytes: 36,292 main and 1,808 low.

After normalizing build-directory and toolchain-root paths, the old and new
source manifests differ only at util/build_ak820.py. Compiler flags, callee-save
list, external roots, build ID and linked CODE metrics agree. I compared the
production builder with the copied experimental builder as text: changes are
the description, explicit version selection/guard and root layout. The compile,
assemble and link logic is unchanged. Byte equality permits reuse of the
previous exact-IHX CPU evidence described in sdcc46-release-review-20261023.md;
no simulator or physical tests were rerun in this review.

I reviewed the assembler correction: exact production path is accepted only
when the report hash and dependency manifest match it; alternative builders
still require the immutable experimental hash. Six compiler executable pins,
review/build/host binding and the second host snapshot remain enforced. Twelve
release-assembler tests pass independently, including production-builder
admission and changed-tool/report rejection. Earlier independent checks passed
seven LUFA and eight SDCC dependency-installer tests.

The saved combined offline report host/runs/20261023-source-trim-offline.json
records seven passing suites and zero physical commands. I verified each saved
log SHA256. These are host results, not device tests. The installed keyboard
remains on its earlier firmware. Final candidate-tree inspection is separate.

```json
{
  "format": "ak820-offline-review-2",
  "release": "rc6",
  "status": "passed",
  "hardware_validated": false,
  "build": {
    "ihx_sha256": "f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e",
    "map_sha256": "13474dc963ab0a292017164209862dff760ea09176bee622c6a1e1e200333d10",
    "build_report_sha256": "a8c35eda197ef2c9c86aaafa37a0948d28d4b4f95f34e9fa4be7afb033c744eb"
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
      "size": 2279,
      "sha256": "d5e2a9ddaf47e17db30735df565bfe1277f3b610a802acd808071d1e6c2e632f"
    },
    "qmk-8051-ak820/util/ak820_tool.py": {
      "size": 22039,
      "sha256": "3a0cd520d0ba0b0125300095e5537e5abab2740f7098c836dc562c39eb6d4e1b"
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
      "size": 12204,
      "sha256": "46a839afbdda100cd57fd8e9c3f9a13f7e984c36c0ed72b054e0bc3ae2f96a91"
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
      "size": 47011,
      "sha256": "b6eff1487c07d4d871b0df7bab44e58e870a23170ac827d066eab8777e2c905d"
    },
    "tools/installer/gui.py": {
      "size": 15632,
      "sha256": "c7406dc28815a7bf5daa2084adc8c8fffb7280daa9566a21161db346a38cdea6"
    },
    "tools/installer/i18n.py": {
      "size": 14399,
      "sha256": "c72831bc8e9b3a5f036e56d72baf2dc8fc0c5e9ba4c6801178a6115b87956018"
    },
    "tools/installer/requirements-build-windows.txt": {
      "size": 235,
      "sha256": "fe92377176d05e83a805899a51be8569cfc63768609bae64c543641f9d715bd5"
    },
    "tools/installer/requirements.txt": {
      "size": 15,
      "sha256": "6e78c6c5a61dbebf36f570a14685c795efcdb3d8bb6b6118b6aa78dd0aca54d4"
    }
  }
}
```
