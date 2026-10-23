# RC6 erase candidate release review

Date: 2026-10-23. Independent reviewer did not author the firmware candidate, IAP test/profile changes, runner integration or personal-image preparation. No build, CPU rerun or device access was performed by this reviewer.

Firmware and bounded GUI update independent offline reviews passed with no open blockers. The physical-confirmation workflow and fresh offline test results are recorded in audits/rc6/physical-update-review.md. Earlier typed-confirmation GUI reviews are superseded. The host binding below covers the exact reviewed sources for release assembly; a standalone GUI rebuild and offline verification remain required before use. It does not authorize a USB write, reset, loader transition or flash, and it does not establish that erase works on the physical controller. The earlier first-image review in docs/REVIEW.md remains historical evidence for that image.

Scope and reasoning: audits/rc6/candidate-erase-review.md. Reviewed source hash b5ef5524ff1206a7d49fc5e3aa3436b9feed9bba33c2a1062429f42c21c1b34b, bounded erase delta, emitted ABI/caller preservation, bounds/protection, stack and documentation agreement.

Evidence: host/runs/rc6-candidate-base-tests.json (seven base suites); host/runs/rc6-candidate-cpu-summary.json (six linked suites, 79 cases); qmk-8051-ak820/.build/rc6-iap-candidate-erase-retry1-20261023/results.json (12 guarded IAP cases). The first IAP attempt timed out during simulator startup after two passing cases and remains preserved separately in .build/rc6-iap-candidate-erase-20261023; it is not a completed PASS. Tested stack paths fit, but no whole-program or arbitrary interrupt-overlap bound is claimed.

The independently repacked personal permanent payload in host/runs/20261023-rc6-erase-candidate-ready has size 51136 and SHA256 54290ce406fda133bd90703664f60559e23620f184f89033c98dddb56e2299ed. It retains the saved durable original encoder word and clears the failed probe journal. The native recovery payload is unchanged. These are offline byte checks.

```json
{
  "format": "ak820-offline-review-2",
  "release": "rc6",
  "status": "passed",
  "hardware_validated": false,
  "build": {
    "ihx_sha256": "d2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce",
    "map_sha256": "9e1ef5262685ea85f3362b378c28836d2af9b51f6699b970c61bafdf3dd5b000",
    "build_report_sha256": "976a98b72c3db45cb8950df4a3b544e40334bb04cf785aea30c876a4f34aafcd"
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
      "size": 46609,
      "sha256": "2f23ca0fab713c905b66586ebdcf51cb630702a2d42cdb21237e44de74b95698"
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
