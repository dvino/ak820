Русский перевод: [Варианты экономии](ru/SPACE-OPTIONS.md).

# Further code-space options

The current plan is to qualify the existing fixes on SDCC 4.6 and prepare a
new firmware release. Further optimization implementation is deferred.
The [deep analysis](../audits/rc6/optimization-deep-analysis-20261023.md),
[current linked inventory](../audits/rc6/optimization-deep-local-20261023.md)
and [release-source research](../audits/rc6/optimization-deep-sdcc-research-20261023.md)
record the future experiments and rejected leads. Current sizes and release
gates are in [status](STATUS.md).

The best future bounded probes are the private journal-header pointer,
macro-delay arithmetic, event-pointer provenance and one shared protocol
operation. Their gains are unmeasured. Short-call rewriting cannot proceed
after the incomplete fixture run and linker crash without closing its tests.
Another kilobyte was a planning reserve, not a proved requirement or promised
saving. Preserve six layers, sixteen macros and supported behavior.
