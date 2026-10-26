#!/usr/bin/env python3
"""Execute Repeat/Alt Repeat/Grave Escape in the linked SDCC image, offline.

The real Quantum pipeline and its recursive Repeat/macro calls run on a
generic C52 CPU. Simulated matrix, NVM and endpoint-ready values are fixtures,
not a model of VS11K28A peripherals, interrupts or a physical USB host.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("ak820_unlock", ROOT / "tests/ak820_unlock/run.py")
unlock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(unlock)
emitted = unlock.emitted


def run_case(fw, name, setup, checks):
    # Reports describe what the host receives; ownership assertions keep their
    # explicit internal symbols even when Key Override projects outgoing data.
    return unlock.run_case(fw, name, setup, checks, outgoing_reports=True)


def rows(*keys):
    result = [0] * 16
    for row, col in keys:
        result[row] |= 1 << col
    return result


def assign(row, col, keycode, layer=0):
    return [emitted.memory("rom", 0xC740 + 256 * layer + 2 * (8 * row + col),
                           keycode.to_bytes(2, "big"))]


def report(keycode=0, mods=0):
    return [mods, 0, keycode, 0, 0, 0, 0, 0]


def cases(fw):
    options = json.loads((fw.build / "build-report.json").read_text())["configuration"]["make_options"]
    # Prove the multiplication-free count update against the former signed
    # product for all int8 states, including the unreachable -128 sentinel.
    for direction in (-1, 1):
        for start in (-128, 0):
            checks = []
            for count in range(start, start + 128):
                product = direction * count
                expected = direction if product < 0 else count + direction if product < 127 else count
                checks.append(("count_" + str(count), "_last_repeat_count", 1, [expected & 255],
                               fw.write("_last_repeat_count", [count & 255]) +
                               fw.call("_update_last_repeat_count", direction & 255)))
            yield run_case(fw, "repeat-count-exhaustive-" + str(direction) + "-" + str(start),
                           fw.initialize(), checks)
    # Keep the normal layout intact in the artifact. Only the CPU's fake NVM
    # maps Q to Repeat and Esc to Grave Escape for these test scenarios.
    a, b, rep, shift, ctrl = (1, 3), (6, 4), (1, 2), (0, 4), (0, 5)
    setup = fw.initialize() + assign(*rep, 0x7C79)
    yield run_case(fw, "repeat-basic-rolled-new-key", setup, [
        ("no_history", "_actual_keyboard_report", 8, report(), fw.transition(rows(rep), 100) + fw.transition(rows(), 120)),
        ("remember_a", "_actual_keyboard_report", 8, report(4), fw.transition(rows(a), 140)),
        ("repeat_down", "_actual_keyboard_report", 8, report(4), fw.transition(rows(), 160) + fw.transition(rows(rep), 180)),
        ("other_down", "_actual_keyboard_report", 8, [0, 0, 4, 5, 0, 0, 0, 0], fw.transition(rows(rep, b), 200)),
        ("release_original", "_actual_keyboard_report", 8, [0, 0, 0, 5, 0, 0, 0, 0], fw.transition(rows(b), 220)),
        ("next_repeat", "_actual_keyboard_report", 8, report(5), fw.transition(rows(), 240) + fw.transition(rows(rep), 260)),
        ("physical_after_repeat", "_actual_keyboard_report", 8, report(4), fw.transition(rows(), 280) + fw.transition(rows(a), 300)),
    ])
    yield run_case(fw, "repeat-modifiers-combine-and-release", setup, [
        ("ctrl_a", "_actual_keyboard_report", 8, report(4, 1), fw.transition(rows(ctrl, a), 100)),
        ("restored_mods", "_actual_keyboard_report", 8, report(4, 3),
         fw.transition(rows(), 120) + fw.transition(rows(shift), 140) + fw.transition(rows(shift, rep), 160)),
        ("physical_mod_preserved", "_actual_keyboard_report", 8, report(0, 2), fw.transition(rows(shift), 180)),
        ("all_released", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
    ])
    yield run_case(fw, "repeat-new-key-preserves-held-mod-owner", setup, [
        ("old_hotkey", "_actual_keyboard_report", 8, report(4, 1),
         fw.transition(rows(ctrl, a), 100) + fw.transition(rows(), 120) + fw.transition(rows(rep), 140)),
        ("new_key_with_held_ctrl", "_actual_keyboard_report", 8, [1, 0, 4, 5, 0, 0, 0, 0], fw.transition(rows(rep, b), 160)),
        ("old_repeat_up", "_actual_keyboard_report", 8, [0, 0, 0, 5, 0, 0, 0, 0], fw.transition(rows(b), 180)),
        ("new_repeat_captured_ctrl", "_actual_keyboard_report", 8, report(5, 1), fw.transition(rows(), 200) + fw.transition(rows(rep), 220)),
        ("plain_repeat_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 240)),
    ])
    # Layer controls must not replace the last printable action. In the
    # original disabled Repeat source, LM was remembered and replayed its
    # layer from a physical Repeat key, so unlock could not release that layer.
    lm_setup = setup + assign(*a, 0x5041)
    yield run_case(fw, "repeat-ignores-layer-mod-before-unlock", lm_setup, [
        ("last_letter", "_actual_keyboard_report", 8, report(5), fw.transition(rows(b), 100)),
        ("letter_repeated", "_actual_keyboard_report", 8, report(5),
         fw.transition(rows(), 120) + fw.transition(rows(a), 140) + fw.transition(rows(), 160) + fw.transition(rows(rep), 180)),
        ("no_replayed_layer", "_layer_state", 1, [0], []),
        ("unlock_no_layer", "_layer_state", 1, [0], unlock.vial(fw, 6)),
    ])
    yield run_case(fw, "repeat-ignores-default-layer", setup + assign(*a, 0x5241), [
        ("before_default_change", "_actual_keyboard_report", 8, report(5), fw.transition(rows(b), 100)),
        ("new_default_layer", "_default_layer_state", 1, [2],
         fw.transition(rows(), 120) + fw.transition(rows(a), 140) + fw.transition(rows(), 160)),
        ("letter_after_default", "_actual_keyboard_report", 8, report(5), fw.transition(rows(rep), 180)),
        ("letter_after_default_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
    ])
    yield run_case(fw, "repeat-live-remap-release", setup, [
        ("repeat_origin", "_actual_keyboard_report", 8, report(4),
         fw.transition(rows(a), 100) + fw.transition(rows(), 120) + fw.transition(rows(rep), 140)),
        ("remapped_release", "_actual_keyboard_report", 8, report(), assign(*rep, 5) + fw.transition(rows(), 160)),
        ("remapped_next", "_actual_keyboard_report", 8, report(5), fw.transition(rows(rep), 180)),
    ])
    yield run_case(fw, "repeat-release-after-noop", setup + assign(*b, 0), [
        ("repeat_active", "_actual_keyboard_report", 8, report(4),
         fw.transition(rows(a), 100) + fw.transition(rows(), 120) + fw.transition(rows(rep), 140)),
        ("origin_released", "_actual_keyboard_report", 8, report(),
         fw.transition(rows(rep, b), 160) + fw.transition(rows(b), 180)),
        ("history_preserved", "_actual_keyboard_report", 8, report(4),
         fw.transition(rows(), 200) + fw.transition(rows(rep), 220)),
        ("history_released", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 240)),
    ])
    yield run_case(fw, "repeat-unlock-cleans-report", setup, [
        ("repeat_held", "_actual_keyboard_report", 8, report(4, 1),
         fw.transition(rows(ctrl, a), 100) + fw.transition(rows(), 120) + fw.transition(rows(rep), 140)),
        ("unlock_clean", "_actual_keyboard_report", 8, report(), unlock.vial(fw, 6)),
        ("cancel_clean", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 160) + unlock.vial(fw, 8)),
        ("owner_reusable", "_actual_keyboard_report", 8, report(4, 1), fw.transition(rows(rep), 180)),
        ("owner_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
    ])
    # A single owner holds Repeat. A second Repeat mapping is ignored, and
    # neither release ordering may replace or strand the owner's action.
    second_rep = (1, 5)
    dual_setup = setup + assign(*second_rep, 0x7C79)
    for owner_first in (False, True):
        first_up = rows(second_rep) if owner_first else rows(rep)
        expected_first = report() if owner_first else report(4)
        yield run_case(fw, "repeat-two-origins-" + ("owner-up-first" if owner_first else "secondary-up-first"), dual_setup, [
            ("first_owner", "_actual_keyboard_report", 8, report(4),
             fw.transition(rows(a), 100) + fw.transition(rows(), 120) + fw.transition(rows(rep), 140)),
            ("second_ignored", "_actual_keyboard_report", 8, report(4),
             fw.transition(rows(rep, b), 160) + fw.transition(rows(rep), 180) + fw.transition(rows(rep, second_rep), 200)),
            ("first_release", "_actual_keyboard_report", 8, expected_first, fw.transition(first_up, 220)),
            ("both_released", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 240)),
            ("new_owner", "_actual_keyboard_report", 8, report(5), fw.transition(rows(second_rep), 260)),
            ("new_owner_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 280)),
        ])
    # Exercise nested process_record -> Repeat -> macro -> synthetic MO/Repeat.
    # The macro's Repeat command attempts to replay the same macro; the real
    # playback guard must stop the cycle, with no layer or HID state left over.
    macro = bytes([1, 6, 0x21, 0x52, ord("a"), 1, 7, 0x21, 0x52,
                   1, 5, 0x79, 0x7C]) + bytes(16)
    macro_key = (0, 0)
    macro_setup = (setup + assign(*macro_key, 0x7700) +
                   [emitted.memory("rom", 0xCEF0, [0, len(macro), 0]),
                    emitted.memory("rom", 0xCF00, macro)] + fw.call("_ak820_macro_init"))
    yield run_case(fw, "repeat-macro-recursion-and-following-event", macro_setup, [
        ("first_macro_report", "_actual_keyboard_report", 8, report(), fw.transition(rows(macro_key), 100)),
        ("first_macro_layer", "_layer_state", 1, [0], []),
        ("repeated_macro_report", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 120) + fw.transition(rows(rep), 140)),
        ("repeated_macro_layer", "_layer_state", 1, [0], []),
        ("following_physical", "_actual_keyboard_report", 8, report(4), fw.transition(rows(), 160) + fw.transition(rows(a), 180)),
    ])
    # An extended macro up event overwrites SDCC action_exec's static record.
    # The Repeat down path must not mistake that nested up for its own release.
    macro = bytes([1, 7, 0x21, 0x52, 1, 2, 4]) + bytes(16)
    macro_setup = (setup + assign(*macro_key, 0x7700) +
                   [emitted.memory("rom", 0xCEF0, [0, len(macro), 0]),
                    emitted.memory("rom", 0xCF00, macro)] + fw.call("_ak820_macro_init"))
    yield run_case(fw, "repeat-recursive-macro-preserves-down-state", macro_setup, [
        ("original_ctrl_a", "_actual_keyboard_report", 8, report(4, 1),
         fw.transition(rows(ctrl), 100) + fw.transition(rows(ctrl, macro_key), 120)),
        ("macro_cleanup", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 140) + fw.call("_clear_keyboard")),
        ("recursive_repeat_down", "_actual_keyboard_report", 8, report(4, 1), fw.transition(rows(rep), 160)),
        ("recursive_effective_report", "_actual_keyboard_report", 8, report(4, 1), []),
    ])

    alt = (1, 5)
    alt_setup = (fw.initialize() + assign(*rep, 0x7C79) + assign(*alt, 0x7C7A) +
                 assign(*a, 0x50))  # Left -> alternate Right.
    yield run_case(fw, "alt-repeat-history-and-opposing-arrows", alt_setup, [
        ("empty_history", "_actual_keyboard_report", 8, report(), fw.transition(rows(alt), 100)),
        ("left", "_actual_keyboard_report", 8, report(0x50), fw.transition(rows(), 120) + fw.transition(rows(a), 140)),
        ("right", "_actual_keyboard_report", 8, report(0x4F), fw.transition(rows(), 160) + fw.transition(rows(alt), 180)),
        ("right_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
        ("repeat_still_left", "_actual_keyboard_report", 8, report(0x50), fw.transition(rows(rep), 220)),
        ("all_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 240)),
    ])
    for name, source, opposite, modifiers, modifier_key in (
        ("ctrl-forward-back", 9, 5, 1, ctrl),
        ("plain-word-back", 26, 5, 0, None),
        ("shift-brackets", 0x2F, 0x30, 2, shift),
    ):
        pressed = rows(a, modifier_key) if modifier_key else rows(a)
        yield run_case(fw, "alt-repeat-mapping-" + name, alt_setup + assign(*a, source), [
            ("original", "_actual_keyboard_report", 8, report(source, modifiers), fw.transition(pressed, 100)),
            ("opposite", "_actual_keyboard_report", 8, report(opposite, modifiers),
             fw.transition(rows(), 120) + fw.transition(rows(alt), 140)),
            ("released", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 160)),
        ])
    yield run_case(fw, "alt-repeat-consumer-volume-opposite", alt_setup + assign(*a, 0xA9), [
        ("volume_up", "_last_consumer_usage", 2, [0xE9, 0], fw.transition(rows(a), 100)),
        ("volume_down", "_last_consumer_usage", 2, [0xEA, 0],
         fw.transition(rows(), 120) + fw.transition(rows(alt), 140)),
        ("volume_release", "_last_consumer_usage", 2, [0, 0], fw.transition(rows(), 160)),
    ])
    yield run_case(fw, "alt-repeat-mods-history-change-and-remap", alt_setup, [
        ("ctrl_left", "_actual_keyboard_report", 8, report(0x50, 1), fw.transition(rows(ctrl, a), 100)),
        ("ctrl_right", "_actual_keyboard_report", 8, report(0x4F, 1), fw.transition(rows(), 120) + fw.transition(rows(alt), 140)),
        # A new press clears raw weak mods, but the held Alt Repeat keeps
        # its owned Ctrl until its own release.
        ("other_key", "_actual_keyboard_report", 8, [1, 0, 0x4F, 5, 0, 0, 0, 0], fw.transition(rows(alt, b), 160)),
        ("captured_release", "_actual_keyboard_report", 8, [0, 0, 0, 5, 0, 0, 0, 0], assign(*alt, 4) + fw.transition(rows(b), 180)),
        ("remapped_press", "_actual_keyboard_report", 8, report(4), fw.transition(rows(), 200) + fw.transition(rows(alt), 220)),
        ("remapped_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 240)),
    ])
    yield run_case(fw, "alt-repeat-no-opposite-does-not-claim-owner", alt_setup + assign(*b, 6), [
        ("unpaired_c", "_actual_keyboard_report", 8, report(6), fw.transition(rows(b), 100)),
        ("no_alternate", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 120) + fw.transition(rows(alt), 140)),
        ("normal_repeat", "_actual_keyboard_report", 8, report(6), fw.transition(rows(alt, rep), 160)),
        ("ignored_alt_release", "_actual_keyboard_report", 8, report(6), fw.transition(rows(rep), 180)),
        ("repeat_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
    ])
    yield run_case(fw, "alt-repeat-unlock-cleans-owner", alt_setup, [
        ("held", "_actual_keyboard_report", 8, report(0x4F, 1),
         fw.transition(rows(ctrl, a), 100) + fw.transition(rows(), 120) + fw.transition(rows(alt), 140)),
        ("unlock_clean", "_actual_keyboard_report", 8, report(), unlock.vial(fw, 6)),
        ("release_cancel", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 160) + unlock.vial(fw, 8)),
        ("reusable", "_actual_keyboard_report", 8, report(0x4F, 1), fw.transition(rows(alt), 180)),
        ("reusable_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
    ])
    for alt_owner in (False, True):
        owner, secondary = (alt, rep) if alt_owner else (rep, alt)
        held = report(0x4F if alt_owner else 0x50)
        for owner_first in (False, True):
            yield run_case(fw, "repeat-alt-shared-owner-" + str(int(alt_owner)) + "-" + str(int(owner_first)), alt_setup, [
                ("owner", "_actual_keyboard_report", 8, held,
                 fw.transition(rows(a), 100) + fw.transition(rows(), 120) + fw.transition(rows(owner), 140)),
                ("secondary_ignored", "_actual_keyboard_report", 8, held, fw.transition(rows(owner, secondary), 160)),
                ("first_up", "_actual_keyboard_report", 8, report() if owner_first else held,
                 fw.transition(rows(secondary) if owner_first else rows(owner), 180)),
                ("both_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
            ])

    if options.get("AK820_GRAVE_ESCAPE") != "yes":
        gesc = (0, 0)
        yield run_case(fw, "grave-escape-disabled", fw.initialize() + assign(*gesc, 0x7C16), [
            ("disabled_press", "_actual_keyboard_report", 8, report(), fw.transition(rows(gesc), 100)),
            ("disabled_release", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 120)),
        ])
        return
    gesc = (0, 0)
    setup = fw.initialize() + assign(*gesc, 0x7C16)
    yield run_case(fw, "grave-escape-release-uses-press-state", setup, [
        ("plain_escape", "_actual_keyboard_report", 8, report(0x29), fw.transition(rows(gesc), 100)),
        ("shift_added", "_actual_keyboard_report", 8, report(0x29, 2), fw.transition(rows(gesc, shift), 120)),
        ("plain_release", "_actual_keyboard_report", 8, report(0, 2), fw.transition(rows(shift), 140)),
        ("shifted_grave", "_actual_keyboard_report", 8, report(0x35, 2), fw.transition(rows(shift, gesc), 160)),
        ("shift_removed", "_actual_keyboard_report", 8, report(0x35), fw.transition(rows(gesc), 180)),
        ("shifted_release", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
    ])
    yield run_case(fw, "grave-escape-live-remap-release", setup, [
        ("gesc_origin", "_actual_keyboard_report", 8, report(0x29), fw.transition(rows(gesc), 100)),
        ("gesc_released", "_actual_keyboard_report", 8, report(), assign(*gesc, 5) + fw.transition(rows(), 120)),
    ])
    setup += assign(*rep, 0x7C79)
    yield run_case(fw, "repeat-shifted-grave-escape", setup, [
        ("original_grave", "_actual_keyboard_report", 8, report(0x35, 2),
         fw.transition(rows(shift), 100) + fw.transition(rows(shift, gesc), 120)),
        ("repeated_grave", "_actual_keyboard_report", 8, report(0x35, 2),
         fw.transition(rows(), 140) + fw.transition(rows(rep), 160)),
        ("repeat_grave_release", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 180)),
    ])
    yield run_case(fw, "grave-escape-overlaps-repeat", setup, [
        ("physical_escape", "_actual_keyboard_report", 8, report(0x29), fw.transition(rows(gesc), 100)),
        ("two_resolved_actions", "_actual_keyboard_report", 8, [2, 0, 0x29, 0x35, 0, 0, 0, 0],
         fw.transition(rows(gesc, shift), 120) + fw.transition(rows(gesc, shift, rep), 140)),
        ("physical_up", "_actual_keyboard_report", 8, [2, 0, 0, 0x35, 0, 0, 0, 0], fw.transition(rows(shift, rep), 160)),
        ("repeated_up", "_actual_keyboard_report", 8, report(0, 2), fw.transition(rows(shift), 180)),
        ("everything_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
    ])
    second_gesc = (1, 5)
    yield run_case(fw, "grave-escape-two-physical-origins", setup + assign(*second_gesc, 0x7C16), [
        ("first_plain", "_actual_keyboard_report", 8, report(0x29), fw.transition(rows(gesc), 100)),
        ("second_shifted", "_actual_keyboard_report", 8, [2, 0, 0x29, 0x35, 0, 0, 0, 0],
         fw.transition(rows(gesc, shift), 120) + fw.transition(rows(gesc, shift, second_gesc), 140)),
        ("first_plain_up", "_actual_keyboard_report", 8, [2, 0, 0, 0x35, 0, 0, 0, 0], fw.transition(rows(shift, second_gesc), 160)),
        ("second_shifted_up", "_actual_keyboard_report", 8, report(0, 2), fw.transition(rows(shift), 180)),
        ("both_plain_up", "_actual_keyboard_report", 8, report(), fw.transition(rows(), 200)),
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--s51", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    if max(fw.code) >= 0xC700:
        raise ValueError("Feature tests require a bounded image below the NVM fixture")
    result = {"linked_image_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              "level": "uCsim C52 linked code; no physical peripheral/USB/IRQ validation",
              "tests": list(cases(fw)), "hardware_validated": False}
    result["pass"] = all(item["pass"] for item in result["tests"])
    (fw.output / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
