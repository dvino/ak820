# CI assembly command review

Decision: PASS for the one-line assembly launcher correction against HEAD `cd36cf446c1bae8070ee8f61750df550ea53230d`. Policy renewal and final all-profile approval remain pending their frozen inputs.

The authentic assembly job `121379439444` log shows `python tools/build_ci_release.py` reaching `settings_matrix_from_builds` and failing with `Profile suite identity, arguments, result or build differs`. The downloaded main archive from CI run `40258163824` has SHA256 `0c6c1e123f580babb3cdb094a07029ac14329f3a55b4fe6ed6eafd83bd353d56`.

Independent execution of `reproduce.py` against that archive produced output byte-identical to `result.json`. All 280 test-source entries equal the current checkout. The 32 suite commands differ only at argument zero: qualification records `/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3.12`, while the original assembly interpreter produces `/opt/hostedtoolcache/Python/3.12.15/x64/bin/python`. Suite order, working directories, arguments, results, image identities and retained logs pass with the resolved interpreter. The original spelling fails. Wrong interpreter, missing flag, wrong module, wrong working directory, wrong image and changed log hash are each rejected.

The production build command already resolves `args.python` before launching the QMK build. The new quoted `readlink -f qmk-8051-ak820/.venv/bin/python` launcher uses that same resolved Python for assembly and its exact-command expectations. The virtual environment is created in the assembly job before this step. No validator, comparison, source snapshot, qualification result or firmware source was changed. Failure to resolve or execute the interpreter stops assembly.

No actionable implementation finding remains. This review establishes the bounded command mismatch and strict contract replay; it does not establish a successful complete assembly, committed-source admission, native package checks, publication or hardware behavior. No full firmware build or physical device command was performed.

## Frozen policies and genuine program approval

Decision: PASS for all ten exact refreshed policies. Independent structural comparison against HEAD found only the workflow source entry SHA256 and size changed in each policy. Exact program identities, host files, safety, packing and qualification bindings are unchanged. All 25,026 input hashes in the retained precommit receipt were independently checked against actual files with zero mismatches. All ten substantive profile checks passed; the receipt defers only committed inputs and independent review records. Its SHA256 is `4d323872a8153ca0ac40e19840fe766d93a5b826e75fdf4ffa1a45856935ce51`. Test-source snapshot remains `a469c44707139d70f4541d9018716e6eb6bc19628b4f99de8030a34d8e7283fe`.

All ten current program review records were authored after this inspection and passed production `validate_policy` against their current host files and actual packing receipt. The independent decision covers the bounded launcher correction and preservation of previously qualified programs. It grants no hardware or publication acceptance.

| Profile | Exact policy SHA256 |
| --- | --- |
| code | `f961ec307552e206c787edfc284568ec1077aa276e3b2d5b039b35dcba2948e5` |
| creative | `f256726330103400fc36e7c54f1840a8bca3d9f5b2f15d86220f3c3573f6d8f2` |
| game | `a750eaada2d7402c591b5b73809f98fcf8e30f4bac09a5507cf0af9120d09049` |
| main | `60161aa9b1eab79e824850eb70c363e5532828eb389c8ac116a517ffd3777713` |
| mmo | `12d0b604f095606a84fe979dfbf7cf48248d621cb0ef1fadb6d81b7f1f77ef18` |
| multios | `28c610c6424eb4a81bedf5cd2f105ffce12a3fa8ef2868420dc299add695c16f` |
| onehand | `dfc0285de7312c8bab5d2c49e9b45618bb0a165a965f6df3c6bc7582a6c05443` |
| pointer | `c6947b9c0b48fb5d5b13b83f9882c75cc072d09866daba991ea643b44b8016d0` |
| shortcuts | `68441baec6f7f8b7bd17995e39770874d2b3774bab246b513738f2466c9c6b0c` |
| typing | `513033f9170e35f3aa09ea972fae5b28b984c60b7fbc89c6409f4a00380a961c` |
