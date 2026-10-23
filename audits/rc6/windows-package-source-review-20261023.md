# Windows package source review

Independent source review, 2026-10-23. PASS for the Windows package builder,
its regression tests and English/Russian build instructions. The root reviewer
did not author these changes. All nineteen bound host files were compared with
the previous approval; only `tools/build_windows_installer.py` changed.

## Findings and closure

The first revision looked for collected files beside the executable. PyInstaller
6 places data in `_internal`; the corrected recipe explicitly selects that
folder and verifies both applications there. Tests use that real layout.
The builder now snapshots approved files before compilation and checks the
source and both collected trees after smoke tests. A changed or missing file
stops packaging. Existing output directories and ZIPs are not overwritten.

Independent rerun: `python3 -B -m unittest discover -s tools -p
 test_build_windows_installer.py -v` passed twelve tests. They cover both
application trees, full ZIP contents, source mutation, missing/mismatched
payloads, each smoke failure, and no success reports after a failed smoke.
These are synthetic packaging tests, not a native Windows executable build.

The manual-only Windows workflow uses read-only repository permission and
pinned action revisions. It was not run remotely. Native Windows packaging,
Tk smoke, manual GUI interaction and physical device checks remain pending.
The old Windows package predates the settings feature.

## Preserved firmware and installer behavior

All eight non-review release-file records were checked against their sizes and
SHA256 and remain unchanged. A fresh pinned SDCC 4.6.0 control build independently
reproduced the released IHX exactly (`f1c4347e...`); it does not change the stored
build report or claim a new packed image.

The existing backup/restore protocol and exact-image restrictions were reviewed
independently again; no correctness finding was found. Thirteen shared-workflow
and nine protocol regressions passed. The previous detailed reviews remain:
`audits/rc6/host-settings-protocol-review-20261023.md`,
`audits/rc6/host-settings-core-review-20261023.md` and
`audits/rc6/host-settings-workflow-review-20261023.md`.

The JSON in `releases/rc6/reviews/independent-review.md` binds only the retained
RC6 release and current host source.
It permits refreshing the offline manifest/approval identity. It does not
approve an experimental firmware, a Windows binary, publication or a hardware
operation. No USB commands were sent.

## Bound implementation

- `tools/build_windows_installer.py`: SHA256 `8fd2f9eb5c337da8fce82e58ab7efcd7a82be407136bfb253b82973c3288899d`.
- `tools/test_build_windows_installer.py`: SHA256 `83d436763574a09cb226e80d0a1d6e76388985e95d84cb678729431579160740`.
- `.github/workflows/windows-installer.yml`: SHA256 `689d9b2f5ba13991c21da04c35b0aaee9db548d8dfbe59492d29851c8a6d429c`.

Refreshed installer manifest SHA256: `2556d1e53017e6977762ca421bc45c6086dc864ee18fec689d6eafef264cef53`.
