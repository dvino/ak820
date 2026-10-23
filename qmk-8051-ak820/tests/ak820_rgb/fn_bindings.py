#!/usr/bin/env python3
"""Check captured Fn bindings offline without opening or writing a keyboard."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('emitted', Path(__file__).parents[1] / 'ak820_emitted/run.py')
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build-dir', type=Path, required=True)
    p.add_argument('--s51', type=Path, required=True)
    p.add_argument('--snapshot', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    a = p.parse_args()
    snapshot = a.snapshot.read_bytes()
    assert len(snapshot) == 65536
    fw = emitted.Firmware(a.build_dir.resolve(), a.s51.resolve(), a.output_dir.resolve())
    commands = fw.initialize()
    # Only captured settings/keymaps enter simulator ROM; no personal ROM is
    # copied into reports or application artifacts.
    for address in range(0xC700, 0xCD80, 32):
        commands += [emitted.memory('rom', address, snapshot[address:address+32])]
    commands += fw.write('_storage_failed', [1])
    commands += fw.write('_rgb_matrix_config', [5, 0, 255, 80, 96, 255, 0, 0])
    cases = []

    def rows(fn=False, f12=False, delete=False):
        out = [0] * 16
        out[10] = 32 if fn else 0
        out[12] = 1 if f12 else 0
        out[14] = 4 if delete else 0
        return out

    def observe(label, symbol, count, expected):
        commands.extend(fw.dump_symbol(label, symbol, count))
        cases.append((label, symbol, count, expected))

    commands += fw.transition(rows(fn=True), 100)
    observe('fn_layer', '_layer_state', 1, [2])
    commands += fw.transition(rows(fn=True, f12=True), 120)
    observe('fn_f12_sends_f12', '_actual_keyboard_report', 8, [0, 0, 0x45, 0, 0, 0, 0, 0])
    commands += fw.transition(rows(fn=True), 140)
    observe('fn_f12_does_not_toggle', '_rgb_matrix_config', 1, [5])
    commands += fw.transition(rows(), 160)
    commands += fw.transition(rows(fn=True), 180) + fw.transition(rows(fn=True, delete=True), 200)
    observe('delete_press_not_yet_toggle', '_rgb_matrix_config', 1, [5])
    commands += fw.transition(rows(fn=True), 220) + fw.frame(240)
    observe('fn_delete_release_toggles_off', '_rgb_matrix_config', 1, [4])
    commands += fw.dump('led_off', 'xram', fw.led_address(0), 4)
    commands += fw.transition(rows(), 260) + fw.transition(rows(fn=True), 280)
    commands += fw.transition(rows(fn=True, delete=True), 300)
    commands += fw.transition(rows(delete=True), 320) + fw.transition(rows(), 340) + fw.frame(360)
    observe('fn_first_release_toggle_on', '_rgb_matrix_config', 1, [5])
    observe('fault_remains_latched', '_storage_failed', 1, [1])
    log, stack = fw.execute('captured-fn-f12-delete-faulted', commands)
    result = []
    for label, symbol, count, expected in cases:
        actual = fw.extract(log, label, fw.address(symbol), count)
        result.append(dict(name=label, pass_=actual == expected, actual=actual, expected=expected))
    off = fw.extract(log, 'led_off', fw.led_address(0), 4)
    result.append(dict(name='off_reaches_dma', pass_=off == [0]*4, actual=off, expected=[0]*4))
    report = dict(passed=all(c['pass_'] for c in result), cases=result, **stack,
                  image_sha256=hashlib.sha256(fw.image.read_bytes()).hexdigest(),
                  snapshot_sha256=hashlib.sha256(snapshot).hexdigest(),
                  limits='CPU with captured keymap and injected latched fault; no device, physical scan or DMA validation.')
    (fw.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'passed': report['passed'], 'cases': len(result), 'image_sha256': report['image_sha256']}))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
