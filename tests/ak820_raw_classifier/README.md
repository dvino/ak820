# Raw request classifier regression

Run `python3 tests/ak820_raw_classifier/run.py` from the `ak820-max` directory. The test is offline and needs Python 3 plus a host `gcc` or `cc`, or Docker with the `ak820-nkro-study-env:local` image. It has no USB or device dependency.

The runner reads the current classifier, its adjacent enum assertions, and the enum definitions in `via.h`, `vial.h`, and `vialrgb.h`. It compares every three-byte packet prefix against the saved original switch oracle, checks that all 32 packet bytes stay unchanged, and confirms that setter-admitting mutations are detected. Source SHA-256 values and outcomes are printed as JSON lines. Extraction, compilation, mismatch, or mutation-detection failures return a nonzero status.
