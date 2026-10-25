# Direct action backend comparison

Run `python tests/direct_action_backend/run.py --output /tmp/ak820-direct-action-check` with GCC available. The command writes the generated native source, executable, standalone SDCC inputs and a checksummed result outside the repository.

The fixture retains the pre-change `action_for_keycode` and `process_action` bodies. The candidate is extracted from the current `process_record_handler`. The comparison uses the actual system and consumer usage conversions, all 65,536 keycodes, both edges and four explicit/cache keycode cases: 524,288 comparisons. Ordered calls, arguments and keyboard-report boundaries must match. Matching these leaf calls preserves their state transitions for arbitrary initial layers and modifier ownership; the test does not replace the leaf implementations with a separate behavioral specification.

The native oracle disables the shift-base sanitizer because its layer mask expression promotes an 8-bit mask to signed 32-bit `int`; malformed layer 31 can overflow that host type before truncation. Other undefined-behavior checks remain enabled. Production direct dispatch explicitly bounds shifts to the 8-bit layer bank.

This comparison does not qualify SDCC execution, interrupt stack bounds, upstream feature interactions, USB or physical behavior. The whole-image checks remain required. The fixture functions originate from QMK and retain the repository's GPL-2.0-or-later licensing.
