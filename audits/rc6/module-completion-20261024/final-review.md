# Final independent acceptance review

Decision: APPROVED for committing the reviewed offline evidence package and associated documentation. No blocking findings remain. This approval does not authorize release, settings writes, device transitions or flashing.

## Reviewed scope

Repository AGENTS.md, retention verifier, follow-up commits c60259c081f9b763af5c5e413fad7fe27ead18ad and 147508ee9008b69ab74e61ad8718f3e7b0712b30, final matrix/catalog/README, four full retained records and archives, 22 runtime-only records and archives, English/Russian STATUS and RESOURCE-BUDGET, and both desktop handoff updates.

The complete diff from firmware freeze ac48c65ab2da30ec0d9d45bba29ff8b7d5062272 to full qualification freeze 147508ee9008b69ab74e61ad8718f3e7b0712b30 contains host/CPU fixtures and audit records only. Firmware compiler inputs and runtime proof sources do not change.

## Independent verification

- All 22 runtime-only archives passed portable retention verification in the earlier independent pass. Final archive hashes match those exact reviewed archives.
- All four full archives passed independent portable retention verification against 147508ee9008b69ab74e61ad8718f3e7b0712b30. Verification binds frozen source, compiler pins, source/configuration/image manifests, startup/memory, foreground/startup/IRQ runtime proof, and successful base/profile suite invocation and log hashes. It does not rerun CPU suites.
- All 26 matrix record hashes and archive hashes match retained bytes. Image SHA256, source commit, regression scope, archived short-call status, CODE/XRAM values and stack capacity/bound/margin agree. All 24 named source profiles are covered. Two extra variants are full-short and full-mouse-auto-shift-short.
- Four fully qualified images each retain 28 base suites, 276 unit tests and zero skipped tests. Supplemental totals are 21 + 23 + 23 + 23 = 90.
- Four catalog entries exactly equal retained catalog_entry objects, have distinct CODE identities and no additional entries. Catalog bytes match the matrix catalog hash.
- Both 26-row RESOURCE-BUDGET tables match every matrix resource number. STATUS and final README distinguish the four full regressions from 22 runtime-only rows, document schema03 only for three extension profiles, and preserve development versus installed/release distinctions. Desktop handoffs point to the completed four-image catalog.
- Authority flags inspected recursively in matrix/catalog remain false; recorded physical device commands are zero.
- Focused typed extension codec suite independently passed six tests without failures or skips; codec.log retains output.

## Finding closure

The compact Repeat fixture qualifier is confined to its host preamble and leaves firmware address-space declarations unchanged. The later common feature fixture now observes the outgoing projected report when present, rejects ambiguous projections and checks the host callback pointer; explicit internal ownership assertions remain directed at their original symbols. No expected report data is weakened by this change. Successful final qualification is bound to these fixtures. Historical failed fixture and restricted-environment attempts remain raw evidence and are not used as successful qualification.

## Limits

The minimum calculated stack margin is zero for Tap Dance and Key Overrides; Key Overrides has 20 trailing main CODE bytes. Changed images require new exact-image proof. Twenty-two variants have runtime qualification only, not repeated full functional regression. Offline static/CPU/host results do not prove physical USB timing, durable device writes, power-loss behavior or installer transitions. Published and installed alpha.3 is unchanged. No builds, USB operations, commits or repository edits were performed during this independent review.

## Exact package identities

Matrix SHA256: `8355125eef058ef94dab7ba59d4e39f783aaaccf0cd6deaa461bacb6c6b2e2df`

Catalog SHA256: `a6c73c77c8cf571faed038f41ef39e161ac6ab7417ddee277806051acaf77505`

### full

IHX SHA256: `53efb6c09d05ef8b75136df041bf695f1d93ecb5cb7c4e299331a3f06a16fefa`

Archive SHA256: `274ad5dd961c207e5db08a3962e278d6e0093527994a83281c5b9456ac2e6916`

### full-key-overrides

IHX SHA256: `708b19d10fe8e5e6a1564ee865e6ddc4c2683d0a696f18d44defa35ef162f288`

Archive SHA256: `9dc23824e6fb49501b8f7d3eb79d4b324f43442499e1ec49a64261c3202b1d8d`

### full-qmk-settings

IHX SHA256: `57196efa465e33bec62d7e0faed8080b417e33548bdda81f552220a8cde6fb28`

Archive SHA256: `68d8124c170e9756d30f91f631643cb17d2924c0f0fae016aa5254e07cc3b83e`

### full-tap-dance

IHX SHA256: `ad48287366117e500bf6581b95720669d1f6eb7bd50ba2b87b8e1bb15965547e`

Archive SHA256: `761945feef7c1196d16ceaeaf00b45c6d467fdc99528bd4de3d07cd0a610913b`

Detailed verification outputs: runtime22-verification.log, runtime22.json, full4-verification.log, full4.json and codec.log in this external review directory.
