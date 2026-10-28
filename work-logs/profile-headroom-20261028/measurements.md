# Profile headroom evidence (2026-10-28)

Local physical-window builds; no image is included or authorized for installation.
Reported CODE headroom is window size minus the occupied-byte count from each
build report, **not** necessarily trailing space or placeable capacity: the main
window is `[0x3027, 0xc700)` (38,617 bytes) and the low window is `[0x28a0,
0x3000)` (1,888 bytes). XRAM headroom is 3,008 minus the ordinary external RAM
size in each linker `.mem` report. These estimates are image-specific and do not
predict whether an added module will link. Tables bind each result to its IHX and
source-manifest SHA-256, not a clean commit: builds record source commit
`a53ca97b8e748c4b88b89582f26e38032714d1b9` and `dirty: true`. SDCC compiler
SHA-256: `3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891`.
The source manifest is generated per profile and includes build-specific sources.

| Profile | Main CODE free | Low CODE free | XRAM free | IHX SHA-256 | Source-manifest SHA-256 |
| --- | ---: | ---: | ---: | --- | --- |
| main | 170 | 5 | 154 | `e9dbfc4167903838361e6a86d9554539ef408a9ea6ed67e7971b0b8d85c84797` | `3524de3b932bb137ddf2899dcd8923b5ad672c0d7db994175e4bee90d40720c2` |
| game | 210 | 5 | 81 | `84b161424ef0dd0388de0bbb753f7f40f4573cf2f00b944b9ac23a4505f0586d` | `eb3089b13b3f2332fdb64fc9d502356dad9621cf404aaf3aef0d6e414d89c16d` |
| mmo | 371 | 5 | 80 | `ee7316e555049a63c6d3216886857333137924261db4c820e4692392fb485559` | `bb3c16dcc6d4ff972d5f456237498c572a0b901d4aa8da728f4e8fdd2b8dd9e6` |
| typing | 1853 | 28 | 661 | `56ef06f6d77f3050712539ab0355a2c992a79813a94cd96163e005b399dd3e22` | `e9e10bb60ea22a05687f3d5f27778398021a2a2ab1ab0bf9ffc8e8af6889047c` |
| code | 2217 | 28 | 672 | `6405e35f6fadc8b7a382ee25229d22a170a43ae48ace3a5a0a3f7a99045eb123` | `98751170dc08456101fcdf4d49f1a77c0baede555b8be122070a3fb106d487be` |
| pointer | 1766 | 28 | 653 | `fb430fe10298edcd67dcf4d2ea69ac66af72083027aee7fd49ab51f87db9b010` | `6f6f7cfc486bf9c3fb48403831e5bcbb365a58eef445efd95302c609df3c4d64` |
| onehand | 1914 | 28 | 628 | `830fe773cc4f9254de21b49dc2f063b7f8f37fe60f99a96837798399007ca224` | `24524ba43d0c334ff79108f2be61eceaac9245119ec341d789c59b7b626cb3af` |
| creative | 820 | 5 | 147 | `a65e87aaf0b551261afa4cc9fa768270dde43d6de370c7f01eb80a45e03ee06f` | `0ad4df7c582621c27fa4d447fbf06c33d6d72b94db6e16448035a38d1f1279ab` |
| shortcuts | 1988 | 28 | 611 | `1f4dee91408e2d1a373586ddb0067a0888b955f6c4c7174bdd1f91657440d9da` | `197ceef6bc1135ee3130fce5d4fa47661aa4a25d4b101e503b867f17c2deeb2e` |
| multios | 2302 | 28 | 679 | `b3d966441cdd901ace82e68271e120820d50a7c155bad273071fc521d987becc` | `07586c0cba874c772532b99d84d503d8f0fd22664664e11ad4c1d921ca19f062` |

The local build and configuration reports, including source identities, memory
accounting, exact-image stack analysis and offline tests, are under
`qmk-8051-ak820/.build/headroom-retry-main/` for `main` and
`qmk-8051-ak820/.build/headroom-<profile>-final/<profile>/` for the other nine.
The corresponding build/configuration reports, linker `.mem`, qualification and
profile result files and their top-level suite logs are preserved in
[`evidence.tar.gz`](evidence.tar.gz) (unpack with `tar -xzf evidence.tar.gz`);
paths recorded inside the original JSON remain the original local paths. All
recorded suite-log hashes and IHX hashes were checked against the original files
before archiving. Firmware images are not included.
The headroom figures alone are not evidence that offline qualification passed or
that a device is safe to flash; see the [qualification summary](qualification-summary.md)
for those statuses. No physical-device validation was performed.
