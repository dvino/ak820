# Exact work bundle review

The retained exact work image, current host code and reviewed safety evidence
are approved for offline bundle assembly. This approval grants no device access
or physical validation. Native Windows/Linux package acceptance remains pending.

The independent review and finding closure are in [review.md](review.md).
The current combined qualification passes 28 base suites, 291 unit tests with
zero skips and 30 supplemental suites. The complete supplemental phase was rerun
after an asset-tool source change; the initial stopped attempt is retained.

```json
{
  "format": "ak820-offline-review-2",
  "release": "rc6",
  "status": "passed",
  "hardware_validated": false,
  "build": {
    "ihx_sha256": "652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880",
    "map_sha256": "064ac921f225b7af1793c19de27d6811700dd8ab95ee108636a09383df671542",
    "build_report_sha256": "0a7df97b688929951cca0dfca951e0724c8213e3dee98c09a014499720f465e6"
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
    "qmk-8051-ak820/util/ak820_extension_settings.py": {
      "size": 4191,
      "sha256": "89bd2be1774ee3d3cdd7d53d023ff93d9498d184673b378dd979887c6ca21339"
    },
    "qmk-8051-ak820/util/ak820_profiles.py": {
      "size": 7864,
      "sha256": "f763251ef138f42773b79f9cf74eccee8b7498f3ef862914f04e68f822983a2f"
    },
    "qmk-8051-ak820/util/ak820_release_manifest.py": {
      "size": 2701,
      "sha256": "ce88a92cf70129648fffa0063227e1db513e1f91900bc1065d56551971faa40b"
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
      "size": 24994,
      "sha256": "b97efc8b82e995144146c87d5bfd0f1086dab98aed9f530410eedc2258661b2b"
    },
    "qmk-8051-ak820/util/prepare_ak820_trial.py": {
      "size": 5745,
      "sha256": "91458b9a14bad55f9bb9a056ec43f8daec0ffe996f21f4ffc15e9f6730aa9fc2"
    },
    "tools/ak820_device_protocol.py": {
      "size": 28081,
      "sha256": "6fc381c0ffb0553f238afc531a3a9a81fee19ec78b623959befb4a4f80584d5a"
    },
    "tools/build_ci_release.py": {
      "size": 21540,
      "sha256": "3931f1a6939fe5d00ce726b41c92cbb68a3c19b2df2834ebd96283e9220a3acf"
    },
    "tools/build_linux_installer.py": {
      "size": 7823,
      "sha256": "8865cf30731c905ffb15933e28428ccc0ca34d1509f1e2da6a705e4d7fc28f97"
    },
    "tools/build_release_bundle.py": {
      "size": 12554,
      "sha256": "47a2f544f4a814c414bf67c10959ccd4ea9fca7c2f7a94b55a0ee419b974d3e7"
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
    "tools/installer/requirements-build-linux.txt": {
      "size": 451,
      "sha256": "34661fb47f32cc9c7151b7e22f91ddb416edd3bdacdff6cf3bf1693d3825993e"
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
      "size": 45837,
      "sha256": "4146f7f4ec48c4bbee84f792381a73e6c4dcc774813dafe67ad70852fb8b9185"
    },
    "tools/installer/settings_workflow.py": {
      "size": 11413,
      "sha256": "677d93b42a8e58baf903bf6d2ae64ee40a4f8a97f4a001f6cfa530537728d4b1"
    }
  },
  "release_safety_manifest_sha256": "83eb57275f1d06c73a6b3f7038a66d0bfbb52ce6587df170f021ed0f1ce2ec4e"
}
```
