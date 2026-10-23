#!/usr/bin/env python3
"""Run the real VIA/Vial recovery flow against production USB transport offline.

Relevant production handler and encoder EEPROM accessor bodies are extracted
verbatim. Hardware, NVM storage, unrelated accessors and boot jump are stubs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]


def function(text, signature):
    """Extract a complete function without counting braces in comments/strings."""
    start = text.index(signature)
    opening = text.index('{', start)
    depth = 0
    tokens = re.finditer(
        r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|/\*.*?\*/|//[^\n]*|[{}]',
        text[opening:], re.S)
    for token in tokens:
        if token[0] == '{':
            depth += 1
        elif token[0] == '}':
            depth -= 1
            if depth == 0:
                return text[start:opening + token.end()] + '\n'
    raise ValueError('Unclosed production function: ' + signature)


def extract_handlers():
    via = (ROOT / 'quantum/via.c').read_text()
    vial = (ROOT / 'quantum/vial.c').read_text()
    bootmagic = (ROOT / 'quantum/bootmagic/bootmagic_lite.c').read_text()
    keymap = (ROOT / 'quantum/dynamic_keymap.c').read_text()
    return '\n'.join([
        '\n'.join(re.findall(r'^#define (?:VIAL_ENCODERS_EEPROM_ADDR|DYNAMIC_KEYMAP_ENCODER_EEPROM_ADDR) .*$', keymap, re.M)),
        function(keymap, 'void *dynamic_keymap_encoder_to_eeprom_address'),
        function(keymap, 'uint16_t dynamic_keymap_get_encoder'),
        function(keymap, 'void dynamic_keymap_set_encoder'),
        vial[vial.index('#define VIAL_UNLOCK_HOLD_TIME_MS'):
             vial.index('#include "qmk_settings.h"')],
        function(vial, 'void vial_unlock_task'),
        function(vial, '__attribute__((unused)) static uint16_t vial_keycode_firewall'),
        vial[vial.index('#if defined(AK820_BOARD) && defined(__SDCC_mcs51)\nstatic void vial_fill_packet'):
             vial.index('void vial_handle_cmd')],
        function(vial, 'void vial_handle_cmd'),
        function(via, '__attribute__((weak)) void raw_hid_receive_kb'),
        function(via, 'void raw_hid_receive(uint8_t *packet'),
        function(bootmagic, '__attribute__((weak)) void bootmagic_lite_reset_eeprom'),
        function(bootmagic, '__attribute__((weak)) void bootmagic_lite(void)'),
    ])


def run(generated, output, compiler):
    (output / 'recovery-handler-fragments.inc').write_text(extract_handlers())
    info = json.loads((ROOT / 'keyboards/ajazz/ak820/info.json').read_text())
    includes = ['.', 'tests/ak820_usb', 'tmk_core', 'tmk_core/protocol',
                'tmk_core/protocol/ch555', 'tmk_core/protocol/ch555/lufa_utils',
                'quantum', 'quantum/keymap_extras', 'quantum/sequencer', 'platforms', 'platforms/mcs51', 'lib/ch555',
                str(generated.parent), str(output)]
    defines = [
        'AK820_USB_HOST_TEST', 'QMK_MCU_CH555', 'PROTOCOL_CH555', 'RAW_ENABLE',
        'SHARED_EP_ENABLE', 'EXTRAKEY_ENABLE', 'NKRO_ENABLE', 'VIAL_ENABLE',
        'VIALRGB_ENABLE', 'RGB_MATRIX_ENABLE', 'ENCODER_MAP_ENABLE', 'CAPS_WORD_ENABLE',
        'DYNAMIC_KEYMAP_ENABLE', 'BOOTMAGIC_LITE', 'EEPROM_CUSTOM',
        'EEPROM_SIZE=0x2800', 'FIXED_CONTROL_ENDPOINT_SIZE=64',
        'FIXED_NUM_CONFIGURATIONS=1', 'USB_POLLING_INTERVAL_MS=1',
        'USB_MAX_POWER_CONSUMPTION=500', 'ARCH=ARCH_MCS51',
        'VENDOR_ID=' + info['usb']['vid'], 'PRODUCT_ID=' + info['usb']['pid'],
        'DEVICE_VER=0x0100', 'MANUFACTURER=' + json.dumps(info['manufacturer']),
        'PRODUCT=' + json.dumps(info['keyboard_name']), 'SERIAL_NUMBER="vial:f64c2b3c"',
    ]
    binary = output / ('recovery-integration.exe' if os.name == 'nt' else 'recovery-integration')
    command = [
        compiler, '-std=gnu11', '-Wall', '-Wextra',
        '-Werror=implicit-function-declaration', '-Wno-unknown-pragmas',
        '-Wno-unused-parameter', '-Wno-old-style-declaration',
        '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-g', '-O1',
        '-include', 'keyboards/ajazz/ak820/config.h',
        *['-I' + item for item in includes], *['-D' + item for item in defines],
        'tests/ak820_recovery/harness.c', 'tmk_core/protocol/usb_descriptor.c',
        '-o', str(binary),
    ]
    sources = [
        'quantum/via.c', 'quantum/vial.c', 'quantum/dynamic_keymap.c', 'quantum/bootmagic/bootmagic_lite.c',
        'tmk_core/protocol/ch555/usb_ak820.c', 'tmk_core/protocol/usb_descriptor.c',
        'quantum/via.h', 'quantum/vial.h', 'quantum/vialrgb.h',
        'keyboards/ajazz/ak820/config.h', 'keyboards/ajazz/ak820/info.json',
        'tests/ak820_usb/ak820_usb_test_shim.h',
        'tests/ak820_recovery/harness.c', 'tests/ak820_recovery/run.py',
    ]
    report = {
        'result': 'FAIL', 'compile_command': command,
        'generated_definition': str(generated),
        'generated_definition_sha256': hashlib.sha256(generated.read_bytes()).hexdigest(),
        'source_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources},
        'level': 'host source integration; verbatim VIA/Vial/bootmagic + encoder address/get/set + production USB; hardware/storage/unrelated accessor/boot stubs',
        'physical_usb_opened': False,
    }
    compiled = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    (output / 'compile.log').write_text(compiled.stdout + compiled.stderr)
    report['compile_exit_code'] = compiled.returncode
    if compiled.returncode:
        print(compiled.stdout + compiled.stderr, end='')
        return_code = compiled.returncode
    else:
        # LeakSanitizer cannot enumerate threads in the restricted runner. This
        # fixture has no allocation; address and undefined checks remain active.
        env = os.environ.copy()
        env['ASAN_OPTIONS'] = 'detect_leaks=0'
        result = subprocess.run([str(binary)], cwd=ROOT, text=True, capture_output=True, env=env)
        (output / 'run.log').write_text(result.stdout + result.stderr)
        print(result.stdout + result.stderr, end='')
        report.update(result='PASS' if result.returncode == 0 else 'FAIL',
                      run_exit_code=result.returncode, output=result.stdout)
        return_code = result.returncode
    (output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    return return_code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', required=True, type=Path,
                        help='Existing firmware build containing one generated Vial definition; relative to the source root')
    parser.add_argument('--output-dir', type=Path,
                        help='New directory for evidence; relative to the source root (default: cleaned temporary directory)')
    parser.add_argument('--cc', default='cc', help='Host GCC/Clang executable with address/undefined sanitizer support')
    args = parser.parse_args()
    build = (ROOT / args.build_dir).resolve()
    generated = sorted(build.glob('obj_*/src/vial_generated_keyboard_definition.h'))
    if len(generated) != 1:
        parser.error(f'Expected one generated Vial definition in {build}; found {len(generated)}. Build the vial keymap first.')
    try:
        if args.output_dir is None:
            with tempfile.TemporaryDirectory(prefix='ak820-recovery-') as temp:
                return run(generated[0], Path(temp), args.cc)
        output = (ROOT / args.output_dir).resolve()
        output.mkdir(parents=True, exist_ok=False)
        return run(generated[0], output, args.cc)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    raise SystemExit(main())
