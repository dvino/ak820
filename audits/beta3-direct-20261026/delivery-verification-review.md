# Final package verification review

Date: 2026-10-26. Result: APPROVED for the final delivery commit and subsequent
Git-bundle and outer-archive verification. No blocking findings remain in this
scope. The final Git bundle and outer delivery ZIP do not exist in this review's
scope and still require their actual import and byte checks.

## Reviewed identities

Approved firmware and Python host source: C2
`d4dbc624d546dbb4f2c132ef60cd165759c84e31`.
The later ancillary module catalog has SHA256
`2947032a7f53c43d906c3ab909a7fb0beb31d83bae4e44368db422ef18afffc6`.
It is separately reviewed in [module-catalog-review.md](module-catalog-review.md)
and must be bound by the final delivery commit, rather than attributed to C2.

| Actual archive | SHA256 |
| --- | --- |
| `AK820-Windows.zip` | `5c255415c4671665619a7d11b781ffeac062e2adfaeab397c19e6726fd83595c` |
| `AK820-Linux-x86_64.tar.gz` | `a8dc3fd3a0aaf0caace130f9c229eee7ae442f732bee8c051c05125568c113ff` |
| `AK820-Beta3-Catalog.zip` | `25a5d3f0363cb91f77804456efa3ebe3a1de93e9c0afef81bbc837cfd4b6338c` |
| `firmware-bundle.zip` | `c0b4a1a920ae0d5a6c2c4743c4703ec97dd9fc119d941e87a11dfe611d85d046` |

## Independent actual-output checks

The Windows and Linux archives contain exactly the same 246 payload files and
24,405,475 uncompressed bytes. All 22 explicit Python host/package inputs and
all explicit public guides and images match C2 blobs. Generated English and
Russian installation guides match the reviewed link-normalization function.
Each profile payload matches both its actual assembled directory and the
approved staging directory, including manifests and approval records.

The Catalog ZIP contains exactly 231 expected files. Its complete member set
and every byte were compared with the approved profile bundles, explicit public
guides, C2 catalog inputs and the separately reviewed module catalog correction.
The matrix and capability catalogs match the builder's explicit canonical
release-status transformations. The generated release catalog and manifest
cover the complete preceding payload with matching sizes and SHA256 values.
Every uncompressed catalog file matches its ZIP member. The full asset directory
contains only that catalog payload, three archives, three detached checksums
and `SHA256SUMS`. All 234 checksum rows are unique, complete and correct; the
three detached checksum files also match their exact archive bytes.

The profile set is exactly main, game, mmo, typing, code, pointer, onehand,
creative, shortcuts and multios. Each manifest has the exact canonical public
file allowlist. All manifest file hashes and sizes and all approval digests
match. Every manifest host binding matches the corresponding C2 blob. Each
application IHX matches its qualified build output. The complete inventories
contain no GUI installer sources, frozen runtimes, bundled runtime libraries,
private OEM images or arbitrary extra input files. This conclusion uses full
allowlist and byte comparisons, rather than only filename exclusions.

All ten worker source snapshots are identical. Every one of their 9,516 file
SHA256 values was independently compared with its committed C2 blob through
`git cat-file`. Each actual worker build tree and bundle tree matches the
recorded hashes. The ten individual profile ZIPs and the aggregate 150-member
firmware ZIP have exactly those approved members and bytes.

The retained [assembly report archive](assembly-linked-reports.json) has SHA256
`acba1081df20eed6090ae243c4c423c81270711443c6adb68d703b0d187518ea`.
Its complete 23-file inventory, sizes, hashes and bytes match the actual assembly
reports and logs. Assembly and packaging run records report success, and their
recorded log hashes match the retained logs. Both committed-origin synchronization
receipts report PASS; the actual worker snapshots independently confirm C2.

## Executed CLI and helper review

The retained package verification report contains eleven successful actual
extracted commands: `--help` and one `--profile NAME verify` for each profile.
The exact reviewed helper was independently rerun against the actual assets;
all eleven commands passed again. Its temporary result is
`/tmp/ak820-beta3-independent-package-review.json`. Only help and offline
verification were invoked. Linux launcher execution permission is present.
Archive path, duplicate and regular-file restrictions passed.

All four retained delivery helpers match their source manifest hashes and their
execution copies. The outer helper's bounded diff adds the two public catalog
metadata reports and corrects provenance labels in Russian, English and the
manifest. Its SHA256 is
`beb7e2763925118c5c55e26a86d547031a954f9c1f6eaa4f95f8235867b8d31f`.
Existing clean-tree, exact assets, complete checksums, assembly identity,
bundle receipt and output-byte checks remain intact. The updated audit README
agrees with the inspected evidence and distinguishes failed preliminary runs,
successful actual assembly, later catalog metadata and physical limitations.
`git diff --check` passes.

The separate import baseline has no alternates. Both C1 and C2 candidate commit
objects are absent (`git cat-file -e` returns 1 for each), while the recorded
preexisting base remains available. The final HEAD must likewise be confirmed
absent before the real incremental bundle import. No baseline import was
performed in this review.

No tracked source or assets were changed during review. Only this review record
was added. No USB, device, network, publication, commit or flashing operation
was performed. Offline package success does not establish physical hardware
behavior, durable settings retention or successful installation.
