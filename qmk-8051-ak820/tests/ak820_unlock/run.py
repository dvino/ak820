#!/usr/bin/env python3
"""Exercise unlock cleanup and live-remap release in linked 8051 code.

Use the shared CPU fixture's simulated matrix and USB registers. The Vial
dispatcher, layer cache, action pipeline and report clear are production code.
The generic C52 CPU does not model VS11K28A peripherals or IRQ timing.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("ak820_emitted", ROOT / "tests/ak820_emitted/run.py")
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)


def vial(fw, subcommand):
    packet = fw.address("_raw_buffer")
    return ([emitted.memory("xram", packet, [0xFE, subcommand] + [0] * 30)] +
            fw.write("_vial_handle_cmd_PARM_2", [32]) +
            fw.call("_vial_handle_cmd", packet))


def run_case(fw, name, setup, checks, *, outgoing_reports=False):
    commands, observations = list(setup), []
    report_address=None
    if outgoing_reports:
        projections=[symbol for symbol in fw.symbols if symbol.startswith('_send_keyboard_report_projected_')]
        if len(projections)>1:raise ValueError('Ambiguous outgoing report projection')
        report_symbol=projections[0] if projections else '_actual_keyboard_report'
        report_address=fw.address(report_symbol)
        commands += [f'break {fw.address("_ak820_host_send_keyboard"):#x}',
                     'commands 1 "echo @@OUTPTR; dump sfr 0x82 0x83 16; fill xram 0x2201 0x2203 0x12; run"']
    for label, symbol, size, expected, transition in checks:
        if outgoing_reports and symbol=='_actual_keyboard_report':symbol=report_symbol
        # Terminate markers so e.g. "held" cannot match "held_released" in
        # the shared fixture's substring-based log extractor.
        commands += transition + fw.dump_symbol(label + "@", symbol, size)
        observations.append((label, symbol, size, expected))
    log, stack = fw.execute(name, commands)
    actual = {label: fw.extract(log, label + "@", fw.address(symbol), size)
              for label, symbol, size, _ in observations}
    expected = {label: value for label, _, _, value in observations}
    pointers=[fw.extract('@@pointer\n'+part,'pointer',0x82,2) for part in log.split('@@OUTPTR\n')[1:]] if outgoing_reports else []
    pointer_ok=all(pointer==[report_address&255,report_address>>8] for pointer in pointers)
    return {"name": name, "pass": actual == expected and pointer_ok, "observations": actual,
            "expected": expected, "outgoing_report_address":report_address,
            "outgoing_pointer_checks":pointers, **stack}


def cases(fw):
    # A down before unlock and up while suppressed used to remain held forever.
    rows = [0, 8] + [0] * 14
    yield run_case(fw, "ordinary-key-unlock-cancel", fw.initialize(), [
        ("held", "_actual_keyboard_report", 8, [0, 0, 4, 0, 0, 0, 0, 0], fw.transition(rows, 100)),
        ("start_clears", "_actual_keyboard_report", 8, [0] * 8, vial(fw, 6)),
        ("release_suppressed", "_actual_keyboard_report", 8, [0] * 8, fw.transition([0] * 16, 120)),
        ("cancel_clean", "_actual_keyboard_report", 8, [0] * 8, vial(fw, 8)),
        ("new_press", "_actual_keyboard_report", 8, [0, 0, 4, 0, 0, 0, 0, 0], fw.transition(rows, 140)),
    ])
    # Physical Ctrl/Shift plus consumer and macro-held modifiers all release.
    rows = [0x30] + [0] * 15
    yield run_case(fw, "modifier-consumer-cleanup", fw.initialize(), [
        ("mods_held", "_actual_keyboard_report", 8, [3, 0, 0, 0, 0, 0, 0, 0], fw.transition(rows, 100)),
        ("consumer_held", "_last_consumer_usage", 2, [0xE9, 0], fw.call("_host_consumer_send", 0xE9)),
        ("mods_clear", "_actual_keyboard_report", 8, [0] * 8, ["fill xram 0x2201 0x2203 0x12"] + vial(fw, 6)),
        ("consumer_clear", "_last_consumer_usage", 2, [0, 0], []),
        ("macro_mod_clear", "_actual_keyboard_report", 8, [0] * 8,
         vial(fw, 8) + fw.transition([0] * 16, 120) + fw.call("_register_code", 0xE2) + vial(fw, 6)),
    ])
    # MO(1) is masked by a different code on its active layer. The press-time
    # cache, not the current layer, identifies what needs to be released.
    rows = [0] * 16
    rows[10] = 0x20
    setup = fw.initialize() + [emitted.memory("rom", 0xC740 + 256 + (10 * 8 + 5) * 2, [0, 5])]
    yield run_case(fw, "momentary-layer-cache-and-toggle-preservation", setup, [
        ("mo_held", "_layer_state", 1, [2], fw.transition(rows, 100)),
        ("retained_toggle", "_layer_state", 1, [0x20], fw.call("_layer_state_set", 0x20) + vial(fw, 6)),
        ("repeat_idempotent", "_layer_state", 1, [0x20], vial(fw, 6)),
        ("released_clean", "_layer_state", 1, [0x20], fw.transition([0] * 16, 120) + vial(fw, 8)),
    ])
    # LM(2,LCTL) has both a layer and a HID modifier to release.
    setup = fw.initialize() + [emitted.memory("rom", 0xC740 + (1 * 8 + 3) * 2, [0x50, 0x41])]
    rows = [0, 8] + [0] * 14
    yield run_case(fw, "layer-mod-cleanup", setup, [
        ("lm_down_layer", "_layer_state", 1, [4], fw.transition(rows, 100)),
        ("lm_down_mods", "_actual_keyboard_report", 8, [1, 0, 0, 0, 0, 0, 0, 0], []),
        ("lm_layer_clear", "_layer_state", 1, [0], vial(fw, 6)),
        ("lm_mod_clear", "_actual_keyboard_report", 8, [0] * 8, []),
    ])
    # The right-hand flag in LM's five-bit modifier encoding must not carry
    # into the action's layer field after shifting the HID modifier mask.
    setup = fw.initialize() + [emitted.memory("rom", 0xC740, [0x50, 0x51])]
    yield run_case(fw, "right-layer-mod-cleanup", setup, [
        ("right_lm_layer", "_layer_state", 1, [4], fw.transition([1] + [0] * 15, 100)),
        ("right_lm_modifier", "_actual_keyboard_report", 8, [16, 0, 0, 0, 0, 0, 0, 0], []),
        ("right_lm_layer_clear", "_layer_state", 1, [0], vial(fw, 6)),
        ("right_lm_modifier_clear", "_actual_keyboard_report", 8, [0] * 8, []),
    ])
    # A new TG key pressed and released while unlocking must never toggle.
    setup = fw.initialize() + [emitted.memory("rom", 0xC740 + (1 * 8 + 3) * 2, [0x52, 0x65])]
    yield run_case(fw, "suppressed-toggle-and-default-layer", setup, [
        ("tg_suppressed", "_layer_state", 1, [0], vial(fw, 6) + fw.transition(rows, 100) + fw.transition([0] * 16, 120)),
        ("default_preserved", "_default_layer_state", 1, [4], fw.write("_default_layer_state", [4]) + vial(fw, 8) + vial(fw, 6)),
    ])

    # The Vial editor can change NVM between physical down/up. Both the
    # Quantum handlers and the final action decoder must see the old code on
    # release. The following press must then use the new assignment.
    rows = [0, 8] + [0] * 14
    yield run_case(fw, "live-remap-normal-key", fw.initialize(), [
        ("original_key", "_actual_keyboard_report", 8, [0, 0, 4, 0, 0, 0, 0, 0], fw.transition(rows, 100)),
        ("released_original", "_actual_keyboard_report", 8, [0] * 8,
         [emitted.memory("rom", 0xC756, [0, 5])] + fw.transition([0] * 16, 120)),
        ("new_assignment", "_actual_keyboard_report", 8, [0, 0, 5, 0, 0, 0, 0, 0], fw.transition(rows, 140)),
    ])
    rows = [0x20] + [0] * 15
    yield run_case(fw, "live-remap-modifier", fw.initialize(), [
        ("original_modifier", "_actual_keyboard_report", 8, [1, 0, 0, 0, 0, 0, 0, 0], fw.transition(rows, 100)),
        ("released_modifier", "_actual_keyboard_report", 8, [0] * 8,
         [emitted.memory("rom", 0xC74A, [0, 5])] + fw.transition([0] * 16, 120)),
    ])
    rows = [0] * 16
    rows[10] = 0x20
    yield run_case(fw, "live-remap-momentary-layer", fw.initialize(), [
        ("origin_layer", "_layer_state", 1, [2], fw.transition(rows, 100)),
        ("layer_released", "_layer_state", 1, [0],
         [emitted.memory("rom", 0xC7EA, [0, 5])] + fw.transition([0] * 16, 120)),
    ])
    yield run_case(fw, "live-remap-before-unlock", fw.initialize(), [
        ("origin_mo", "_layer_state", 1, [2], fw.transition(rows, 100)),
        ("unlock_releases_origin", "_layer_state", 1, [0],
         [emitted.memory("rom", 0xC7EA, [0, 5])] + vial(fw, 6)),
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--s51", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    fw = emitted.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
    if max(fw.code) >= 0xC700:
        raise ValueError("Runtime tests require a bounded image below the NVM fixture")
    result = {"linked_image_sha256": hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              "level": "uCsim C52 linked code; no physical peripheral/USB/IRQ validation",
              "tests": list(cases(fw)), "hardware_validated": False}
    result["pass"] = all(item["pass"] for item in result["tests"])
    (fw.output / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
