# Fresh MAIN runtime review

2026-10-26. Independent review of the no-W MAIN build in `/home/danil/ak820-main-as-final-20261026/qmk-8051-ak820/.build/final-no-w/main`. No actionable findings were identified in its source binding, linked inspection or runtime evidence. Full regression qualification was still in progress when checked.

Fresh `configure_firmware.inspect` passed against `toolchains/sdcc-4.6.0`, including pass30 replay. The foreground, startup and IRQ component files matched their summary hashes. Their runtime proof was independently recombined using the fresh linked identity, current stack capacity and current runtime-checker source snapshot. Every recombined proof field matched the saved summary.

| Item | Result |
| --- | --- |
| IHX SHA256 | `b6040e965dfa30a22049bec5591ff7ab074a89000d973f22f9f3b08736a33031` |
| MAP SHA256 | `e0b68545e2d239e0db61d0cbdf88a3b6f7a35ff28cc5a1ad51989363f7f3e6b0` |
| Build report SHA256 | `7c8492a173859c3b9e7259658c5180b609b7fd900d9b87348e00e859ec80e3f4` |
| Source manifest SHA256 | `b64262abda66bba764fb5006c0b0216ec93dae84160d3a349ee840078b7c15f8` |
| CODE | 40,398 bytes |
| Foreground bound | 98 bytes |
| Main entry frame | 2 bytes |
| Combined IRQ allowance | 60 bytes |
| Combined stack | 160 of 167 bytes; 7 bytes spare |
| Pre-main startup | 2 bytes |
| Unresolved roots | None |

All 470 nongenerated source-origin entries from the build report were compared with the original Windows checkout and matched SHA256. Generated build inputs were checked by fresh inspection in the Linux checkout. The current configuration is MAIN with Auto Shift and without GUI lock or W pulsing. Equal IHX bytes to the earlier AS-low probe do not replace this build's fresh MAP, source-manifest and component evidence.

The audit README names the correct Linux working folder and its sequential `build_ci_profiles.py` command matches live producer PID 129572, including `final-no-w`, `final-no-w-bootstrap` and `audits/final-no-w/builds.json`. Its MAIN CODE, IHX and runtime statements agree with this inspection. It correctly leaves full regressions and the remaining nine profiles pending.

At the observation point, `qualification.json` and `profile-tests/results.json` did not exist for this build, and producer 129572 was active. This report therefore does not claim completed base or supplemental regression suites. Final ten-profile catalog/policy preparation, packing, migrations, release approval and physical behavior remain separate. No device operations or implementation edits were performed.
