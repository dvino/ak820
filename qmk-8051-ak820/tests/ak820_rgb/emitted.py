#!/usr/bin/env python3
"""CPU tests of linked reactive RGB; simulated memory only, no physical device."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('emitted_support', HERE.parent / 'ak820_emitted/run.py')
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)


def reactive_mode(fw):
    """Bind the fixture's enum selection to the exact configured linked image."""
    report = json.loads((fw.build / 'configuration-report.json').read_text())
    image_sha256 = hashlib.sha256(fw.image.read_bytes()).hexdigest()
    if report['identity']['ihx_sha256'] != image_sha256:
        raise ValueError('RGB configuration report does not match the linked image')
    direct = report['configuration']['make_options']['AK820_VIALRGB_DIRECT']
    if direct not in ('yes', 'no'):
        raise ValueError('Missing explicit compiled Direct configuration')
    if ('_g_direct_mode_colors' in fw.symbols) != (direct == 'yes'):
        raise ValueError('Direct configuration disagrees with linked symbols')
    # AK820 appends Reactive after the four base effects and optional Direct.
    return 6 if direct == 'yes' else 5


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--s51', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    fw = support.Firmware(args.build_dir.resolve(), args.s51.resolve(),
                          (args.output_dir or args.build_dir / 'rgb-emitted').resolve())
    mode = reactive_mode(fw)
    indicator_commands = fw.initialize()
    dma = fw.address('_ak820_led_dma')
    # Dedicated slots 71/79 are absent from the published RGB slot map.
    slot_caps, slot_layer = dma + 71 * 4, dma + 79 * 4
    slotmap = [fw.code[fw.address('_ak820_rgb_slots') + i] for i in range(82)]
    assert 71 not in slotmap and 79 not in slotmap
    indicator_cases = []
    mac_pc = '_ak820_mac_mode' in fw.symbols
    os_owned = mac_pc or '_ak820_os_indicator_mode' in fw.symbols
    # Optional OS modules own component 3; otherwise it remains unrelated.
    # PC/no helper is off. Keep a nonzero sentinel in memory to prove the write.
    os_idle = 0 if os_owned else 0xc3

    def indicator_case(label, report, layer, default, configured, sleeping, irq, expected, producer=()):
        nonlocal indicator_commands
        indicator_commands += fw.write('_KB_USB_SetReport', [report])
        indicator_commands += fw.write('_layer_state', [layer])
        indicator_commands += fw.write('_default_layer_state', [default])
        indicator_commands += fw.write('_D0UsbConfig', [configured])
        indicator_commands += fw.write('_USB_SleepStatus', [2 if sleeping else 0])
        for action in producer:
            indicator_commands += action
        # Preserve unrelated component bytes around each owned indicator.
        indicator_commands += [support.memory('xram', slot_caps + 2, [0x5a, 0xa5]),
                               support.memory('xram', slot_layer + 2, [0x3c, 0xc3]),
                               support.memory('sfr', 0xe8, [0x20 if irq else 0])]
        indicator_commands += fw.call('_ak820_update_indicators')
        for suffix, address, extra in (('caps', slot_caps, [0x5a, 0xa5]),
                                       ('layer', slot_layer, [0x3c, 0xc3])):
            indicator_commands += fw.dump(f'{label}_{suffix}', 'xram', address, 4)
        indicator_commands += fw.dump(f'{label}_irq', 'sfr', 0xe8, 1)
        indicator_cases.append((label, expected, irq))

    indicator_case('base_caps_with_unrelated_leds', 0xff, 0, 1, 1, False, True,
                   {'caps': [255, 255, 0x5a, 0xa5], 'layer': [0, 0, 0x3c, os_idle]})
    indicator_case('unrelated_host_led_bits', 0xfd, 0, 1, 1, False, True,
                   {'caps': [0, 0, 0x5a, 0xa5], 'layer': [0, 0, 0x3c, os_idle]})
    if '_layer_on' in fw.symbols and '_layer_off' in fw.symbols:
        indicator_case('layer_on_api', 0, 0, 1, 1, False, False,
                       {'caps': [0, 0, 0x5a, 0xa5], 'layer': [255, 255, 0x3c, os_idle]},
                       producer=(fw.call('_layer_on', 2),))
        indicator_case('layer_off_api', 0, 0, 1, 1, False, True,
                       {'caps': [0, 0, 0x5a, 0xa5], 'layer': [0, 0, 0x3c, os_idle]},
                       producer=(fw.call('_layer_on', 2), fw.call('_layer_off', 2)))
    else:
        # Optimized profiles retain the state-set API used by active actions.
        indicator_case('layer_state_set_api', 0, 0, 1, 1, False, False,
                       {'caps': [0, 0, 0x5a, 0xa5], 'layer': [255, 255, 0x3c, os_idle]},
                       producer=(fw.call('_layer_state_set', 4),))
    indicator_case('default_layer_api', 0, 0, 1, 1, False, True,
                   {'caps': [0, 0, 0x5a, 0xa5], 'layer': [255, 255, 0x3c, os_idle]},
                   producer=(fw.call('_default_layer_set', 3),))
    if '_layer_on' in fw.symbols:
        indicator_case('tri_layer_api', 0, 0, 1, 1, False, True,
                       {'caps': [0, 0, 0x5a, 0xa5], 'layer': [255, 255, 0x3c, os_idle]},
                       producer=(fw.call('_layer_on', 1), fw.call('_layer_on', 2)))
    indicator_case('capsword_without_host_led', 0, 0, 1, 1, False, True,
                   {'caps': [0, 0, 0x5a, 0xa5], 'layer': [0, 0, 0x3c, os_idle]})
    indicator_case('suspended', 2, 2, 1, 1, True, False,
                   {'caps': [0, 0, 0x5a, 0xa5], 'layer': [0, 0, 0x3c, os_idle]})
    indicator_case('resumed', 2, 2, 1, 1, False, True,
                   {'caps': [255, 255, 0x5a, 0xa5], 'layer': [255, 255, 0x3c, os_idle]})
    indicator_case('reset_unconfigured', 0, 2, 1, 0, False, True,
                   {'caps': [0, 0, 0x5a, 0xa5], 'layer': [0, 0, 0x3c, os_idle]})
    indicator_case('disconnected', 2, 2, 1, 0, False, True,
                   {'caps': [0, 0, 0x5a, 0xa5], 'layer': [0, 0, 0x3c, os_idle]})
    if mac_pc:
        indicator_case('mac_os_without_layer', 0, 0, 1, 1, False, True,
                       {'caps': [0, 0, 0x5a, 0xa5], 'layer': [255, 0, 0x3c, 255]},
                       producer=(fw.write('_ak820_mac_mode', [1]),))
        indicator_case('mac_os_with_layer', 0, 2, 1, 1, False, True,
                       {'caps': [0, 0, 0x5a, 0xa5], 'layer': [255, 255, 0x3c, 255]})
        indicator_case('pc_os_without_layer', 0, 0, 1, 1, False, True,
                       {'caps': [0, 0, 0x5a, 0xa5], 'layer': [0, 0, 0x3c, 0]},
                       producer=(fw.write('_ak820_mac_mode', [0]),))
    indicator_log, indicator_stack = fw.execute('dedicated-indicators', indicator_commands)
    for label, expected, irq in indicator_cases:
        actual = {
            'caps': fw.extract(indicator_log, f'{label}_caps', slot_caps, 4),
            'layer': fw.extract(indicator_log, f'{label}_layer', slot_layer, 4),
            'irq': fw.extract(indicator_log, f'{label}_irq', 0xe8, 1),
        }
        target = {**expected, 'irq': [0x20 if irq else 0]}
        indicator_cases[indicator_cases.index((label, expected, irq))] = {
            'name': label, 'pass': actual == target, 'actual': actual, 'expected': target}
    indicator_report = {'name': 'dedicated_host_and_layer_indicators',
                        'pass': all(case['pass'] for case in indicator_cases),
                        'cases': indicator_cases, 'os_component_owned': os_owned,
                        'mac_pc_compiled': mac_pc, **indicator_stack,
                        'scope': 'Linked updater CPU model with simulated USB/layer state; CapsWord key activity and USB report generation are not invoked here.'}
    commands = fw.initialize() + fw.clock(0)
    # SDCC packs enable in bits 0..1 and the configured mode in bits 2..7.
    commands += fw.write('_rgb_matrix_config', [(mode << 2) | 1, 0, 255, 160, 0, 255, 0, 0])
    observations = []

    def observe(label, index, expected):
        commands.extend(fw.dump(label, 'xram', fw.led_address(index), 4))
        observations.append((label, fw.led_address(index), expected))

    def event(slot, pressed=True):
        commands.extend(fw.write('_process_rgb_matrix_PARM_2', [slot & 7]))
        commands.extend(fw.write('_process_rgb_matrix_PARM_3', [int(pressed)]))
        commands.extend(fw.call('_process_rgb_matrix', slot >> 3))

    commands += fw.frame(16)
    observe('idle', 0, [0, 0, 0, 0])
    event(0)
    commands += fw.frame(32)
    # V=158 quantizes to152 -> CIE=71.
    observe('first_press', 0, [255, 71, 0, 0])
    observe('other_dark', 81, [0, 0, 0, 0])
    commands += fw.clock(512)
    event(125)
    event(0, False)
    commands += fw.frame(528)
    observe('chord_first', 0, [255, 41, 0, 0])
    observe('chord_last', 81, [255, 71, 0, 0])
    commands += fw.frame(2064)
    observe('first_expired', 0, [0, 0, 0, 0])
    commands += fw.frame(2560)
    observe('all_expired', 81, [0, 0, 0, 0])
    event(104)  # Encoder switch has no LED.
    commands += fw.frame(2576)
    observe('encoder_hole', 0, [0, 0, 0, 0])
    event(0)
    commands += fw.call('_rgb_matrix_set_suspend_state', 1)
    observe('suspend_immediate', 0, [0, 0, 0, 0])
    commands += fw.call('_rgb_matrix_set_suspend_state', 0) + fw.frame(2592)
    observe('resume_black', 0, [0, 0, 0, 0])
    commands += fw.clock(65520)
    event(0)
    commands += fw.frame(65552)
    observe('wrap_lit', 0, [255, 71, 0, 0])
    commands += fw.frame(67600)
    observe('wrap_expired', 0, [0, 0, 0, 0])
    log, stack = fw.execute('reactive-chords-expiry-suspend-wrap', commands)
    cases = []
    for label, address, expected in observations:
        actual = fw.extract(log, label, address, 4)
        cases.append({'name': label, 'pass': actual == expected, 'actual': actual, 'expected': expected})
    report = {'pass': all(c['pass'] for c in cases) and indicator_report['pass'], 'cases': cases,
              'indicators': indicator_report, **stack,
              'reactive_mode': mode,
              'linked_image_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(),
              'limits': 'uCsim C52 CPU/linked-code fixtures; no VS11K28A peripheral, physical timing or device validation.'}
    (fw.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    if not report['pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
