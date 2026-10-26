# CI catalog source review

Result: PASS for the bounded source change. No actionable findings remain in this scope.

The review covers fresh capability-catalog generation in `tools/build_ci_release.py`, its assembly regression in `tools/test_build_ci_release.py`, the publication overlay in `.github/workflows/windows-installer.yml`, and agreement with English and Russian CI documentation. The existing publisher and native package host-manifest paths were inspected for compatibility. No source files were changed by this review.

The assembler passes all ten measured build directories, in release-profile order, to the existing capability catalog verifier. That verifier checks exact linked image, runtime and qualification evidence. Its complete result is written alongside the measured matrix in the atomic output stage; raw identities are not rewritten to match a local catalog. The new focused test verifies those exact arguments and the unchanged serialized report. Its mocked build evidence proves orchestration, not real ten-profile qualification.

Publication downloads the same assembly artifact and overlays both reports before the catalog packer runs. The packer still requires ten unique capability profiles, compares each complete raw build identity to its approved bundle, checks linked CODE identity and firmware hashes, and rejects missing or changed rows before writing output. The native installer host manifest includes the web protocol documents but neither overlaid JSON report; this later overlay does not alter native package inputs. Committed policy, source hash and per-profile approval gates remain intact.

The CI documents describe this behavior in both languages. Existing packer regressions cover changed capability identity, missing/duplicate profiles, and failure before output creation. The author reported 10 focused CI assembly tests passing; no tests or hardware commands were run during this independent review.

This is source review only. It does not approve the complete firmware program, prove all ten final qualification runs, prove native release execution or publication, or establish device behavior. Those acceptance gates remain separate.

Reviewed SHA256:

- `tools/build_ci_release.py`: `5d88cd4435ad7f6827649b7057a15dc79b393d93fd856c2b9436ee8f118f7acc`
- `tools/test_build_ci_release.py`: `8bcb0160f3d6862d099c40b3d1190b1b7a528cce128a0b12fd95c1d7eadb51fb`
- `.github/workflows/windows-installer.yml`: `dc3d0d294329c7e7d1c4a149272524f846e068ae9dfffa517da4b0150d27ea9c`
- `tools/build_beta_release_assets.py`: `755eef0906fa7bca8aab780296a3e0ba209e8d4f3cc596959f0b743fc2a666d9`
- `tools/test_build_beta_release_assets.py`: `34b9839cd803a1637177d6a4f7f60b4d24dfbead45e9b66b280faf149be16072`
- `docs/CI.md`: `6dc3c406f026c11f9a366892caeaa1a976506c0b81158d5c6a140dc71ad4a1f0`
- `docs/ru/CI.md`: `34b9f17653579945d3150e68ea59d51b400cad46e541e4e1ca8e22870cc2cdf5`

## Combined runtime proof field correction

Result: PASS for the bounded correction in `tools/build_ci_profiles.py` and its regression fixture. The saved `configuration-report.json` at `/home/danil/ChatGPT/ak820-beta2-qualified-a-20261025/qmk-8051-ak820/.build/next-main-release2-certified/` was inspected directly. Its runtime analysis uses format `ak820-runtime-safety-1`, `whole_program_stack_qualified: true`, no unresolved roots, stack bound 160 and capacity 168. This is a previously saved producer example, not evidence qualifying the current changed source.

`tools/ak820_runtime_safety.py` emits `whole_program_stack_qualified` from its combined startup, foreground and IRQ bound result. The CI builder now requires that exact field to be the boolean `true`. The obsolete foreground field cannot satisfy the gate. The regression uses the real combined field for success and rejects both the obsolete field alone and a false combined result. Configuration equality, offline pass and required qualification/profile report checks remain in place. The correction closes the producer/consumer field mismatch without substituting foreground analysis for whole-program proof.

The lead reported six focused orchestration tests passing. No tests were rerun during this review. Full current-source ten-profile qualification and release acceptance remain pending.

Reviewed SHA256:

- `tools/build_ci_profiles.py`: `e35b43cdc29f8b0ae74b7a9810cc2ac032f7a3db85444e58b6bdc258a6bc4f10`
- `tools/test_build_ci_profiles.py`: `13fd83cb26bce0872a9789903a5b82d9c191966413a5d4e8b759a7d920b472f6`
- `tools/ak820_runtime_safety.py`: `09276f2659e53dfbee17e59887ef8e4d6052fb3e3c4232d617d9c6f4ccbe1503`
