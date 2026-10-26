#!/usr/bin/env python3
"""Compile production USB controller/descriptor sources against host MMIO only."""
import json
import os
import sys
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
info = json.loads((root/'keyboards/ajazz/ak820/info.json').read_text())
includes = ['.', 'tests/ak820_usb', 'tmk_core', 'tmk_core/protocol',
            'tmk_core/protocol/ch555', 'tmk_core/protocol/ch555/lufa_utils',
            'quantum', 'platforms', 'platforms/mcs51', 'lib/ch555']
defines = ['AK820_BOARD', 'AK820_USB_HOST_TEST', 'QMK_MCU_CH555',
           'PROTOCOL_CH555', 'RAW_ENABLE', 'SHARED_EP_ENABLE', 'MOUSE_ENABLE',
           'MOUSE_SHARED_EP', 'EXTRAKEY_ENABLE', 'NKRO_ENABLE',
           'MATRIX_ROWS=16', 'MATRIX_COLS=8', 'EEPROM_CUSTOM', 'EEPROM_SIZE=0x2800',
           'FIXED_CONTROL_ENDPOINT_SIZE=64', 'FIXED_NUM_CONFIGURATIONS=1',
           'USB_POLLING_INTERVAL_MS=1', 'USB_MAX_POWER_CONSUMPTION=500',
           'ARCH=ARCH_MCS51', 'VENDOR_ID='+info['usb']['vid'],
           'PRODUCT_ID='+info['usb']['pid'], 'DEVICE_VER=0x0100',
           'MANUFACTURER='+json.dumps(info['manufacturer']),
           'PRODUCT='+json.dumps(info['keyboard_name']),
           'SERIAL_NUMBER="vial:f64c2b3c"']
if '--os-indicators' in sys.argv:
    defines.append('AK820_OS_INDICATORS')
if '--mac-pc' in sys.argv:
    defines.append('AK820_MAC_PC')
if '--gui-lock' in sys.argv:
    defines.append('AK820_COMPACT_GUI_LOCK')
if '--without-mouse' in sys.argv:
    defines = [item for item in defines if item not in ('MOUSE_ENABLE','MOUSE_SHARED_EP')]
with tempfile.TemporaryDirectory(prefix='ak820-usb-') as temp:
    binary = str(Path(temp)/'test_usb')
    command = ['cc','-std=gnu11','-Wall','-Wextra',
               '-Wno-unknown-pragmas','-Wno-unused-parameter','-Wno-old-style-declaration','-fsanitize=address,undefined',
               '-fno-omit-frame-pointer','-g','-O1',*['-I'+x for x in includes],
               *['-D'+x for x in defines], 'tests/ak820_usb/test_usb.c',
               'tmk_core/protocol/usb_descriptor.c','-o',binary]
    subprocess.run(command,cwd=root,check=True)
    # LeakSanitizer cannot enumerate threads in the restricted runner; this
    # harness has no dynamic allocation. Address/undefined checks remain active.
    env = os.environ.copy()
    env['ASAN_OPTIONS'] = 'detect_leaks=0'
    subprocess.run([binary],cwd=root,env=env,check=True)
