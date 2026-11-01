#!/usr/bin/env python3
"""Exact compiler argument policy for canonical pointer/pass30; not approval."""
from pathlib import Path
import json
import shlex

from ak820_capture_compile import validate_default_keymap, validate_manifest
from ak820_pointer_compile_environment import validate_pointer_environment

POLICY = 'ak820-pointer-pass30-arguments-1'

# Fixed from the AK820 pointer/pass30 Make sources and VPATH rules. This is
# independent of obj.txt, depfiles and capture records at validation time.
BOARD = '''ak820_board ak820_boot ak820_combo ak820_crc ak820_dynamic_macro
ak820_flash ak820_indicators ak820_key_override ak820_keymap_words ak820_leader
ak820_macro ak820_nvm ak820_nvm_read_block ak820_nvm_update_block ak820_oneshot
ak820_os_indicators ak820_rgb_shared ak820_settings ak820_startup ak820_tap_dance
ak820_tapping ak820_timer matrix'''.split()
SAME = '''keyboards/ajazz/ak820/ak820_mousekey keyboards/ajazz/ak820/ak820_rgb
lib/ch555/gpio lib/ch555/hal platforms/mcs51/hardware_id platforms/mcs51/platform
platforms/mcs51/suspend platforms/suspend platforms/synchronization_util platforms/timer
quantum/action quantum/action_layer quantum/action_tapping quantum/action_util
quantum/bitwise quantum/bootmagic/bootmagic_lite quantum/bootmagic/magic
quantum/caps_word quantum/color quantum/debounce/sym_defer_g quantum/dynamic_keymap
quantum/eeconfig quantum/encoder quantum/keyboard quantum/keycode_config
quantum/keymap_common quantum/keymap_introspection quantum/led quantum/led_tables
quantum/logging/debug quantum/logging/print quantum/logging/sendchar quantum/main
quantum/process_keycode/process_caps_word quantum/process_keycode/process_repeat_key
quantum/process_keycode/process_rgb quantum/process_keycode/process_tri_layer
quantum/quantum quantum/repeat_key quantum/rgb_matrix/rgb_matrix_drivers
quantum/send_string/send_string quantum/sync_timer quantum/tri_layer quantum/via
quantum/vial quantum/vialrgb'''.split()
SPECIAL = {
    'ch555_ak820': 'tmk_core/protocol/ch555/ch555_ak820',
    'eeprom_driver': 'drivers/eeprom/eeprom_driver',
    'protocol/ch555/usb_ak820': 'tmk_core/protocol/ch555/usb_ak820',
    'protocol/ch555/usb_util': 'tmk_core/protocol/ch555/usb_util',
    'protocol/host': 'tmk_core/protocol/host',
    'protocol/report': 'tmk_core/protocol/report',
    'protocol/usb_device_state': 'tmk_core/protocol/usb_device_state',
    'protocol/usb_util': 'tmk_core/protocol/usb_util',
    'usb_descriptor': 'tmk_core/protocol/usb_descriptor',
}


def expected_units(obj):
    units = {obj + '/' + name + '.o': 'keyboards/ajazz/ak820/' + name + '.c' for name in BOARD}
    units.update({obj + '/' + name + '.o': name + '.c' for name in SAME})
    units.update({obj + '/' + name + '.o': source + '.c' for name, source in SPECIAL.items()})
    units[obj + '/' + obj + '/src/default_keyboard.o'] = obj + '/src/default_keyboard.c'
    if len(units) != 79:
        raise ValueError('Invalid pointer policy object map')
    return units

# These tokens are the AK820 platform, QMK feature and pointer/pass30 rules.
# Keep them independent of the recorded command and cflags.txt.
PREFIX = '''-c -mmcs51 --model-large --disable-warning 115 --disable-warning 85
--disable-warning 117 --disable-warning 190 --iram-size 0x0100 --xram-size 0x0c00
--xram-loc 0x0400 --code-size 0xc700 -DF_CPU=32000000 --opt-code-speed -g -Os
--std-sdcc11 --opt-code-size -DAK820_READ_HOOK_PRESERVES_RN=1 --callee-saves
 timer_read,timer_read32,ak820_nvm_ok,get_mods,get_weak_mods,matrix_get_row,readPin,eeprom_read_byte,eeprom_update_byte,ak820_flash_read,mDelaymS,get_repeat_key_count
-DAK820_COMPRESS_DEFAULT_KEYMAP -DAK820_WORD_HOOKS_PRESERVE_RN=1 -DSKIP_VERSION
-DVIALRGB_NO_DIRECT -DAK820_COMPACT_ONESHOT -DAK820_COMPACT_MOUSEKEY
-DAK820_MOUSE_CURSOR_STEP=8 -DAK820_MOUSE_CURSOR_PERIOD=20 -DAK820_MOUSE_WHEEL_STEP=1
-DAK820_MOUSE_WHEEL_PERIOD=80 -DAK820_COMPACT_DYNAMIC_MACRO -DAK820_COMPACT_LEADER
-DAK820_OS_INDICATORS -DAK820_COMPACT_TAP_DANCE -DAK820_COMPACT_KEY_OVERRIDE
-DAK820_QMK_SETTINGS -DAK820_KEYMAP_WORDS_ASM -DAK820_NVM_READ_BLOCK_ASM
-DAK820_NVM_UPDATE_BLOCK_ASM -DKEYBOARD_ -DKEYBOARD_ajazz -DKEYBOARD_ajazz_ak820
-DKEYMAP_C="keyboards/ajazz/ak820/keymaps/vial/keymap.c"
-DPRINTF_SUPPORT_DECIMAL_SPECIFIERS=0 -DPRINTF_SUPPORT_EXPONENTIAL_SPECIFIERS=0
-DPRINTF_SUPPORT_LONG_LONG=0 -DPRINTF_SUPPORT_WRITEBACK_SPECIFIER=0
-DSUPPORT_MSVC_STYLE_INTEGER_SPECIFIERS=0 -DPRINTF_ALIAS_STANDARD_FUNCTION_NAMES=1
-DMOUSEKEY_ENABLE -DEEPROM_ENABLE -DEEPROM_DRIVER -DEEPROM_CUSTOM -DRGB_MATRIX_ENABLE
-DUSE_CIE1931_CURVE -DVIA_ENABLE -DVIAL_ENABLE -DNO_DEBUG -DSERIAL_NUMBER="vial:f64c2b3c"
-DVIALRGB_ENABLE -DBOOTMAGIC_LITE -DSEND_STRING_ENABLE -DENCODER_ENABLE -DENCODER_MAP_ENABLE
-DCAPS_WORD_ENABLE -DDYNAMIC_KEYMAP_ENABLE -DREPEAT_KEY_ENABLE -DTRI_LAYER_ENABLE
-DMOUSE_ENABLE -DMOUSE_SHARED_EP -DEXTRAKEY_ENABLE -DRAW_ENABLE -DSHARED_EP_ENABLE
-DBOOTLOADER_SIZE=4096 -DF_USB=UL -DARCH=ARCH_MCS51 -DFIXED_CONTROL_ENDPOINT_SIZE=64
-DFIXED_NUM_CONFIGURATIONS=1 -DPROTOCOL_CH555 -DQMK_MCU=ch555 -DQMK_MCU_CH555
-DQMK_KEYBOARD="ajazz/ak820"'''.split()


def expected_flags(obj):
    return PREFIX + [f'-DQMK_KEYBOARD_H="{obj}/src/default_keyboard.h"'] + '''
-DQMK_KEYMAP="vial" -DQMK_KEYMAP_H="vial.h"
-DQMK_KEYMAP_CONFIG_H="keyboards/ajazz/ak820/keymaps/vial/config.h"
-Ikeyboards/ajazz/ak820/keymaps/vial -Iusers/vial -Ikeyboards/. -Ikeyboards/ajazz
-Ikeyboards/ajazz/ak820 -I. -Itmk_core -Iquantum -Iquantum/keymap_extras
-Iquantum/process_keycode -Iquantum/sequencer -Idrivers -Iplatforms/mcs51/drivers/eeprom
-Idrivers/eeprom -Iquantum/rgb_matrix -Iquantum/rgb_matrix/animations
-Iquantum/rgb_matrix/animations/runners -Iquantum/bootmagic -Iquantum/send_string'''.split() + [
        '-I' + obj + '/src'] + '''-Iquantum/logging -Ilib/printf/src -Ilib/printf/src/printf
-Itmk_core/protocol -Iplatforms -Iplatforms/mcs51 -Iplatforms/mcs51/drivers
-Itmk_core/protocol/ch555 -Ilib/ch555 -Itmk_core/protocol/ch555/lufa_utils
--include keyboards/ajazz/ak820/config.h'''.split() + [
        '--include', obj + '/src/info_config.h', '--include',
        'keyboards/ajazz/ak820/keymaps/vial/config.h', '--include',
        'quantum/rgb_matrix/post_config.h', '--include', 'keyboards/ajazz/ak820/config.h',
        '--include', obj + '/src/info_config.h', '--include',
        'keyboards/ajazz/ak820/keymaps/vial/config.h']


def validate_pointer_arguments(argv, flags, dep, source, output):
    if argv[:4] == ['python3', '-s', 'util/ak820_default_keymap.py', 'sdcc']:
        if source != 'quantum/keymap_introspection.c' or not output.endswith('/quantum/keymap_introspection.o'):
            raise ValueError('Default-keymap wrapper used for an unexpected translation unit')
        category, compiler_args = 'wrapper', argv[4:]
    elif argv[:1] == ['sdcc']:
        if source == 'quantum/keymap_introspection.c':
            raise ValueError('Default-keymap translation unit requires wrapper')
        category, compiler_args = 'direct', argv[1:]
    else:
        raise ValueError('Unknown compiler command category')
    if compiler_args != flags + ['-Wp,-MD,-MF,' + dep, source, '-o', output]:
        raise ValueError('Pointer compiler arguments differ from policy: ' + output)
    return category


def validate_pointer_commands(root, build, objects, toolchain, qmk_bin):
    root, build = Path(root).resolve(), Path(build).resolve()
    obj = (build / 'obj_ajazz_ak820_vial').relative_to(root).as_posix()
    units = expected_units(obj)
    expected_objects = {name[:-2] + '.rel' for name in units}
    if len(objects) != len(expected_objects) or set(objects) != expected_objects:
        raise ValueError('Pointer object membership differs from policy')
    captures = validate_manifest(root, build, objects, build / 'obj_ajazz_ak820_vial')
    flags = expected_flags(obj)
    wrapper_count = 0
    sources = set()
    for path in captures:
        data = json.loads(path.read_text(encoding='utf-8'))
        validate_pointer_environment(data.get('environment'), root, build, toolchain, qmk_bin)
        argv = data['argv']
        output = path.relative_to(root).as_posix()[:-len('.compile.json')]
        dep = output[:-2] + '.d'
        prerequisites = shlex.split((root / dep).read_text(encoding='utf-8').replace('\\\n', ' ').split(':', 1)[1])
        if not prerequisites or not prerequisites[0].endswith('.c'):
            raise ValueError('Missing primary translation unit')
        source = prerequisites[0]
        source_path = Path(source)
        if (source_path.is_absolute() or '..' in source_path.parts or source.startswith('@') or
                source in sources or not output.startswith(obj + '/')):
            raise ValueError('Invalid or duplicate translation unit')
        sources.add(source)
        if units.get(output) != source:
            raise ValueError('Pointer object/source mapping differs from policy: ' + output)
        if validate_pointer_arguments(argv, flags, dep, source, output) == 'wrapper':
            wrapper_count += 1
    if wrapper_count != 1:
        raise ValueError('Expected one compressed default-keymap invocation')
    validate_default_keymap(captures, build)
    return POLICY
