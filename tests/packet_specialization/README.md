# Fixed packet buffer regression

Run `ASAN_OPTIONS=detect_leaks=0 python tests/packet_specialization/run.py` from the repository root. The leak detector is disabled because the sandbox does not expose the process information it requires. Address and undefined-behavior checks remain enabled.

The runner extracts `raw_hid_receive` from production source twice. It compares the generic branch with the AK820 SDCC branch, using a native model of XDATA and the transport's fixed `raw_buffer`. The test also rejects a foreign packet pointer and checks all 256 fill values against every byte of the production Vial fill helper. All 524,288 packet cases compare the full reply and ordered calls, including all command bytes, bulk sizes, unlock states, storage failures and malformed lengths.

The target branch requires the transport's buffer and a 32-byte packet. Its only firmware caller passes that buffer and size. Vial receives the same buffer through VIA. Other boards and native builds retain the generic pointer parser. The fixed buffer is also used by the target Vial packet-fill helper.

This test models VIA parsing and forwarding. It does not execute SDCC instructions or prove USB timing, Vial command bodies, NVM durability or physical behavior. Exact linked stack and interrupt qualification remains required for the resulting image.
