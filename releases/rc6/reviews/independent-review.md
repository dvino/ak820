# Installer source review

Independent source review on 2026-10-24 approved the fourth exact settings
profile and its unchanged identity, provenance and downgrade gates. See
`audits/rc6/oem-indicators-final-integration-review-20261024.md` for scope and
verification. The 21 host-file records below bind that reviewed source.
The legacy firmware remains unchanged. This source binding does not approve
the new C/W firmware or a device operation; its full regression and CI policy
review are separate. No device write or interactive Windows acceptance is
established by this record.

Host bindings refreshed for the reviewed Combo-capable installer and full 28-suite CI contract on 2026-10-24. This retained bundle still selects its earlier firmware; alpha.2 uses the fresh CI bundle. Independent closure is recorded in `audits/rc6/combos-alpha-release-review-20261024.md`.

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
    "qmk-8051-ak820/util/ak820_ci_authorization.py": {
      "size": 13337,
      "sha256": "91e7f29dfed79968e7a32c3f29b1c46470a1294f97765981b02790d0f504c561"
    },
    "qmk-8051-ak820/util/ak820_diagnose.py": {
      "size": 13505,
      "sha256": "2a3dd74d73d1b135107468d330818896a7158e16f4e4031b1c1757f14854dc0d"
    },
    "qmk-8051-ak820/util/ak820_release_manifest.py": {
      "size": 2517,
      "sha256": "a97a8b902b4bbf7cb7799109c00fa9e5d068d06417146e85736fc5cd04bbee30"
    },
    "qmk-8051-ak820/util/ak820_tool.py": {
      "size": 22775,
      "sha256": "9f7fcacc803be7c3e1bc18dcfc11f50b24960be9f1c48a3e6268fbacc1113f92"
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
    "tools/ak820_device_protocol.py": {
      "size": 22064,
      "sha256": "d60ef46fdbff3277df52924753b5a6070ea33eac24c0081dc6388da8d771aba2"
    },
    "tools/build_ci_release.py": {
      "size": 20973,
      "sha256": "0246b827de8dabeb291910857c69aca7c1303799261bf18585143c2743115d3a"
    },
    "tools/build_release_bundle.py": {
      "size": 12204,
      "sha256": "46a839afbdda100cd57fd8e9c3f9a13f7e984c36c0ed72b054e0bc3ae2f96a91"
    },
    "tools/build_windows_installer.py": {
      "size": 8190,
      "sha256": "8fd2f9eb5c337da8fce82e58ab7efcd7a82be407136bfb253b82973c3288899d"
    },
    "tools/installer/70-ak820.rules": {
      "size": 339,
      "sha256": "f0b85bb730963057350a6a9cfe35e1f17e2859a5bfbcebfce9fccaa6534a3a52"
    },
    "tools/installer/ak820.py": {
      "size": 49478,
      "sha256": "23d4fa854d3bf7471c4b9a25a11390ac960ec4fe2c63cfea490d06d66a730a84"
    },
    "tools/installer/gui.py": {
      "size": 21396,
      "sha256": "1a4d315ee9c49fcd2f9827809eb464e1122aeb81c6841a2c6c7160a047436469"
    },
    "tools/installer/i18n.py": {
      "size": 21250,
      "sha256": "94901c2826c7936410f9e799518c4a6ccdff7d1800f10784d03d81c53dc45dd5"
    },
    "tools/installer/requirements-build-windows.txt": {
      "size": 235,
      "sha256": "fe92377176d05e83a805899a51be8569cfc63768609bae64c543641f9d715bd5"
    },
    "tools/installer/requirements.txt": {
      "size": 15,
      "sha256": "6e78c6c5a61dbebf36f570a14685c795efcdb3d8bb6b6118b6aa78dd0aca54d4"
    },
    "tools/installer/settings_backup.py": {
      "size": 31925,
      "sha256": "b68a4841607b1371456eb5a496b2beeab4577493e7d0ba8d151819604ff649eb"
    },
    "tools/installer/settings_workflow.py": {
      "size": 11413,
      "sha256": "677d93b42a8e58baf903bf6d2ae64ee40a4f8a97f4a001f6cfa530537728d4b1"
    }
  }
}
```
