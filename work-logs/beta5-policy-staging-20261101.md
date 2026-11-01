# Beta.5 policy staging, 2026-11-01

The offline catalog frozen at `12653ad269d10fe8b2fffcb59104479fcb4214b9`
was used to prepare the ten profile policies. It contains ten current images and
the ten published beta.4.1 predecessor images. The installer and web catalog
copies have the same SHA256:
`83864a0276fb4892253f1897c95fafbd4a750ada211a6aa868b09d083d9e2a41`.

The ten images were built at `3f71dd1005cd7ec7e1ca41248041b1d5b04acfa8` and
requalified with source `37264ad914edb0ecd4a061f1222ff6f315443c57`; they were
not rebuilt from the catalog-freeze commit. The previous requalification and
private reference evidence are recorded in `work-logs/beta5-v3-draft-20261101.md`.

A fresh frozen settings test run is retained in
`audits/beta5-proof-settings-20261101/`. It reports 249 tests, no skips,
exit code 0, offline only, and zero physical device commands. The first capture
attempt was rejected before tests because its output path overlapped a protected
audits directory; its log and exit code are retained under the proof checkout's
`qmk-8051-ak820/.build/settings-capture-attempt1.*`.

The policy producer remeasured the original build roots and generated evidence
under `audits/beta5-proof-policy-20261101/`. Its frozen catalog and transition
checks passed, including 200 source-to-target cases and 100 cases for each of
the two current-image action matrices. Its first staging attempt rejected
reserved backup fixture names before creating any output; the renamed copies
were used for the successful attempt. Both attempt logs and exit codes remain
under the proof checkout's `qmk-8051-ak820/.build/v3-policy*`. Private packed data and backup
fixtures remain outside the repository under
`/home/agent/ak820-beta5-private-20261101/`.

The staged safety, packing and program policies were copied into the ten
`ci/profiles/` directories in the isolated proof checkout. The canonical safety
validator passed there for each retained image and its staged witnesses. The
lead-run `work-logs/beta5-verify-policy-20261101.py` and its JSON result also
record the source, catalog, staged-policy and test-log cross-checks. This is an
offline pre-commit check: the final committed tree, CI rebuild, release
assembly and downloaded assets still require validation. The first local policy
commit omitted eleven required logs because Git ignored them; the follow-up
commit explicitly adds those unchanged logs before committed-tree validation. There was no hardware
access, device write, reset or flash; physical behavior and settings persistence
remain untested. Public settings v3 and device-write gates remain closed.
