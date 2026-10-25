# Work source-context independent review

Date: 2026-10-25. Decision: **approved for bounded parameter-spills diagnostic reuse** with unchanged protected compiler assembly, pinned tools/runtime and reserved-memory map. This is a source-context approval, not whole-image qualification, configured-regression permission or deployment approval. No full build, source edit, configured regression or device action was performed by this review.

Certificate: `work-parameter-spills-context.json`, SHA256 `b59ed1451f90cf290532271179895864be822aa5273ece9ea562bf33b2ef50a9`.

## Independently checked

- All79 provenance entries exist and match recorded bytes, including work bootstrap IHX/MAP, report, stack report and linked listings.
- All496 build-manifest inputs exist and match the current files, including tools. The current source report is separate from the earlier maximal context.
- All three protected original compiler-ASM canonical hashes match: board, timer and USB. Regeneration through the current `make_context_certificate` produces an object identical to the supplied certificate. The normal `validate_context` succeeds against the actual object and DCE trees.
- A temporary changed provenance digest is rejected. A temporary protected timer ASM instruction changed from RET to NOP is rejected as protected-module drift. Only temporary copied inputs were mutated. An initial attempted mutation of the word in a comment left canonical code unchanged; that correctly did not test an instruction change and was replaced by the explicit instruction mutation.
- Exact work IHX SHA256 is `989f0107297818755a10dc156bbffd01899c7264aca44876e4f718cd246bb1e7`; map SHA256 is `ded6d0963dd15ee7510e0dd7bbb41260394dde02d0157b2e7ec38430f9f14479`.
- The fresh stack and startup reports have the same full image identity. Foreground/USB/timer/LED static bounds are98/5/2/2 with no unresolved roots. Startup bounds are two pre-main control bytes and two main-entry frame bytes, with unchanged interrupt enables until main.

## Reuse scope

The certificate locks whole original compiler modules contributing reachable application IRQ instructions, not arbitrary later linked output. Foreground trimming may use it only while the validator continues to accept the protected assembly, provenance, exact compiler/runtime hashes and fixed-map source hashes. The transform's original capture, object-area checks and postlink IRQ exclusion audit remain required. Changing protected assembly or input provenance requires fresh evidence and review; digest substitution is not permitted.

The38,047-byte work bootstrap,171-byte stack capacity and its static roots do not qualify a trim-on build. That build needs its own exact linked resource, startup, foreground and interrupt checks. The certificate explicitly says application IRQ only, whole image unqualified and hardware unqualified. The incomplete OEM IRQ routing/wrapper/nesting contract remains an external limitation despite legal work CODE placement. The new work context does not substitute for the maximal context or reproduce missing external handoff artifacts.
