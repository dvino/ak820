Русский перевод: [Варианты экономии](ru/SPACE-OPTIONS.md).

# Further code-space options

Measure the complete linked image before changing code to save space. Compare
behavior, both CODE windows, XRAM and stack against a fixed control. Shared
code and outlining make individual feature costs non-additive. Keep six layers,
16 macros, 8192 macro bytes and eight Combo slots unless a separate format and
migration change is approved.

Current measurements and limits are in [Resource budget](RESOURCE-BUDGET.md).
The [development matrix](../audits/rc6/compact-runtime-20261024/final/README.md)
records the measured feature images; it predates whole-stack proof for the new
candidate. Resource allocation alone is not a runtime bound. Each new profile
must pass exact-image startup, foreground and IRQ stack analysis, with all paths
bounded and the combined allocation within capacity. See the [runtime stack
report](../audits/rc6/runtime-stack-20261024/README.md). A pass does not prove
physical behavior. See [Roadmap](ROADMAP.md) for further work.
