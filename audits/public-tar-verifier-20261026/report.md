# Public archive verifier correction

The external public-asset verifier now accepts internal archive links. The Linux packaging helper permits internal relative symlinks and writes them without dereferencing. Rejecting every nonregular tar member would reject a valid package produced by that helper.

The change is limited to tar parsing in the external verifier, its retained exact copy and SHA256 mapping. Product code, packaging, CI, policies and release acceptance gates are unchanged.

All member names are checked before reading payloads. Duplicate names include directories; noncanonical names, unsafe paths, special members and file/link ancestors are rejected. Symlinks resolve relative to their parent; hardlinks resolve relative to the archive root. Absolute, escaping, missing, directory and cyclic targets are rejected. Resolution follows only named archive members and must end at a regular file. Before collapsing parent components, every intermediate target component must name an explicit or implicit archive directory. Missing parents, file parents and link parents fail closed, including through nested aliases; a broken public link therefore cannot become a working scratch file.

The returned mapping contains bytes under each regular or linked name. Scratch extraction writes separate regular files, including for hardlinks. No filesystem links are created. Linked names receive the resolved regular target's mode, preserving executable files; extraction retains the existing permission mask of 0777.

`python audits/public-tar-verifier-20261026/test_tar_links.py` passes two tests: a valid forward-reference link graph and 29 adversarial cases checked through both public tar helpers. Fixtures cover relative symlinks, root-relative hardlinks, mixed chains, executable modes, regular scratch files, missing targets, cycles, unsafe paths, duplicates, directory targets, file/link ancestors and special members. Results are retained in `fixture-results.txt`.

The published v0.6.0-beta.1 Linux archive and sidecar were downloaded from the repository release. `check_real_fixture.py` verifies its sidecar, resolves every file and compares bytes with Python tarfile's reference reads. Results are retained in `real-fixture-results.json`. That archive has no links, so this is real regular-archive compatibility evidence; link behavior is covered by the fixtures. No native binary was executed. The beta.2 linked archive and complete release asset checks remain separate release gates.

No firmware tests, rebuild, USB access, device writes, commit or publication were performed in this correction. Independent review remains required before commit.

Independent review found that normalization could accept broken `missing/../file` or `file/../file` targets. Component traversal validation corrects this finding. Six additional rejection fixtures and a valid directory-parent traversal fixture pass. Fresh independent review is pending.
