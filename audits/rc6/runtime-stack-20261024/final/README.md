# Integrated profile qualification

The 17 named profiles and two additional short-call variants are scheduled for
fresh qualification from one frozen source commit. Every build must close the
exact foreground, CRT and IRQ bound before its base and feature regressions.
This page will record only completed results, identities and retained logs.

The integrated `full-ctrl-gui` candidate has passed its runtime proof:
101 foreground + 2 CRT + 61 IRQ = 164 of 166 stack bytes. Its 28 base suites, 273 base unit tests without skips and 25 feature suites
also pass. Clean-source matrix results are not yet recorded here. See the parent
[technical report](../README.md) for reviewed implementation and scope.
