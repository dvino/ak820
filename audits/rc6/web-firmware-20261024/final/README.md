# Four fully qualified development images

All four images pass from clean frozen source
`1187d4cedd439733bd0c7ceb5c41daac9089de5b`. Each image first passes whole-image
foreground, CRT startup and all enabled interrupt bounds, then 28 base suites,
273 unit tests without skips and its supplemental suites. The supplemental
counts are 21 for `full`, 23 for each single module and 25 for both: 92 executions.
Normal sanitizer configuration is retained, with no external overrides.

| Profile | CODE bytes | XRAM bytes | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: |
| [full](full/record.json) | 38,890 | 2,600 | 160 / 166 | 6 |
| [full-mac-pc](full-mac-pc/record.json) | 39,177 | 2,603 | 164 / 166 | 2 |
| [full-mac-pc-os-indicators](full-mac-pc-os-indicators/record.json) | 39,614 | 2,612 | 164 / 166 | 2 |
| [full-os-indicators](full-os-indicators/record.json) | 39,342 | 2,609 | 160 / 166 | 6 |

Mac/PC passes all 10 linked cases in both applicable images. OS passes 13 cases
alone and 19 with Mac/PC. Host fixtures also cover malformed requests, lease
boundaries, waveform, modifier ownership and C/W independence.
The baseline `full` reproduces accepted IHX
`898bfa2fc1bfc02562820611a7b652017bbfabf9d67a3b02d60f3d48e337c114`.

Each row retains complete compressed raw build files, identities, runtime
proofs, all base/profile logs and linked test results. [matrix.json](matrix.json)
binds them. The [development catalog](capability-catalog.json) was generated
twice with identical bytes: SHA256
`5afdf80018b410d5ef073b2ed5c8e1a15ef002ce7f8c16ebcec9b94277b4923e`.
It describes only these four fully checked images and grants no write, flash
or release permission. It is not an installed-image detector.

```sh
python3 audits/rc6/web-firmware-20261024/verify_matrix.py
```

The [all-profile runtime matrix](../runtime-all/README.md) separately covers
all 21 named profiles and 23 variants. Full regression coverage in this package
is the four images above. Static analysis and host/CPU models do not establish
physical behavior. No device commands, installation or release occurred.
Independent final review passed: both retained-evidence verifiers, all image
identities, the 23-row EN/RU resource tables and documentation scope were checked.
