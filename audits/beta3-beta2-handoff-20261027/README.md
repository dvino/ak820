# Beta.2 to beta.3 handoff

Русский перевод: [Проверка переноса](README-ru.md).

The release priority is settings transfer from published beta.2 to beta.3.
The ten firmware compositions, images, Python host files and existing migration
catalog remain unchanged. Migration from alpha releases is not extended by this
work.

The [offline checker](verify_beta2_handoff.py) authenticates the published beta.2
firmware bundle and matrix, then compares them with the actual delivered beta.3
package. It binds all ten source images and all ten target images to their exact
settings identities, the explicit catalog transitions and the retained source
fixtures. The [result](beta2-handoff.json) records the 100 source/target pairs.

The completed migration plans come from the original beta.3
[preparation run](../beta3-direct-20261026/transition-preflight.json). This follow-up
checks their correspondence with the published artifacts; it does not execute
new restore plans or hardware operations. Existing checks still reject settings
that the selected target profile cannot represent.

The [independent review](independent-review.md) covers the checker, its actual
output and this scope. The existing release ZIP remains valid. A small follow-up
Git bundle adds only this verification and documentation to commit
`59d323f5d1ca7b15b82b9050223b531056378ede`.
