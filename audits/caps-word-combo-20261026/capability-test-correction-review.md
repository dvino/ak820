Capability test correction review

The test-only change agrees with the current profile and catalog contracts. MAIN and Typing enable Auto Shift, so QMK setting 4 is active in those two profiles. Its consumer is compact-auto-shift. The checked Creative and Onehand profiles keep that field dormant. All other profile expectations and negative controls remain unchanged.

No actionable findings. The correction changes no production code or firmware behavior. The independent review covered the diff, the profile composition, and module_contract setting construction. The recorded targeted run passed all 13 tests. Physical behavior is outside this evidence.

Reviewed test SHA256: 30982f350b6da858107d295c31fc04f49ab57eb9921426a0230592c84bac287b.
