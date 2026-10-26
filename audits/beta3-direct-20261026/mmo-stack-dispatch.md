# MMO outlined callback stack check

The beta.3 MMO final attempt stopped at parameter-spills-postlink-stack. The multiplication call site at 0xA386 calls a leaf at 0x5210 containing exactly MOV B,#2; MUL AB; RET (75 F0 02 A4 22). The checker previously required that multiplication inline. The guarded ROM lookup and pointer invocation otherwise use the existing supported pattern.

The checker now accepts this exact leaf at the multiplication position, verifies its complete instruction body, records its reachable instructions and accounts for its two-byte call frame. All guard, private spill, getter, ROM and invocation checks remain required. No firmware source or failed build artifact was changed.

The 33 stack analyzer tests pass, including outlined multiplication success and negative controls for changed helper instructions, missing helper bytes, changed guards, wrong XOR, unsupported invocation, absent spill provenance and missing ROM bytes.

A read-only check of /tmp/ak820-beta3-isolated/a/qmk-8051-ak820/.build/beta3-qualified/mmo reports foreground bound 102 and application IRQ bounds 2, 5 and 2, with no unresolved paths. This is a static partial result, not complete runtime or hardware qualification. The output is /tmp/ak820-mmo-outlined-multiply-stack.json.

Image SHA256: 963aff70931a3ac4530fa8a8fd9f2dd4ad43125c3dce963ce1c8a7cce3009821

Fresh final builds are required for all profiles: util/build_ak820.py includes the analyzer in the final build source manifest, and configure_firmware.inspect validates those source hashes. Requalification alone cannot qualify the old final reports. Existing unchanged bootstrap context certificates can be reused: validate_context checks tools, reserved-map sources, immutable provenance files and protected compiler ASM, without comparing the bootstrap source manifest against the current analyzer. Certificates and reports must not be edited by hand.
