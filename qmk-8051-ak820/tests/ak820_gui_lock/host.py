#!/usr/bin/env python3
"""Check the production GUI control and final report mask on the host."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / 'quantum/action_util.c').read_text()
def function(name):
    begin = text.index(name)
    end = text.index('\n}\n', begin) + 3
    return text[begin:end]

source = r'''
#include <stdbool.h>
#include <stdint.h>
#include <assert.h>
#define AK820_COMPACT_GUI_LOCK
#define AK820_COMPACT_TAPPING
#define AK820_BOARD
#define NO_ACTION_ONESHOT
#define QK_MAGIC_GUI_ON 0x7009
#define QK_MAGIC_GUI_OFF 0x700a
#define QK_MAGIC_TOGGLE_GUI 0x700b
#define KC_LGUI 0xe3
#define KC_RGUI 0xe7
#define MOD_BIT(k) (1u << ((k) & 7))
typedef struct { uint8_t mods, reserved, keys[6]; } report_keyboard_t;
static report_keyboard_t actual_keyboard_report, sent;
#define keyboard_report (&actual_keyboard_report)
static uint8_t real_mods, weak_mods, owned_mods, owned_weak_mods;
static bool gui_disabled;
static unsigned sends;
void host_keyboard_send(report_keyboard_t *report) { sent = *report; ++sends; }
void send_keyboard_report(void);
''' + function('bool ak820_gui_process(') + function('void send_keyboard_report(') + r'''
int main(void) {
    for (uint32_t code=0; code<=65535; ++code) {
        for (unsigned disabled=0; disabled<2; ++disabled) {
            for (unsigned pressed=0; pressed<2; ++pressed) {
                gui_disabled=disabled;
                const unsigned before=sends;
                bool passthrough=ak820_gui_process(code, pressed);
                const bool control=code>=0x7009 && code<=0x700b;
                assert(passthrough == !control);
                assert(gui_disabled == (control && pressed ?
                    (code==0x700b ? !disabled : code==0x700a) : disabled));
                if (!control || !pressed) assert(sends==before);
            }
        }
    }
    /* Each possible effective modifier set from every owner class. */
    for (unsigned mods=0; mods<256; ++mods) {
        for (unsigned source=0; source<4; ++source) {
            real_mods = source==0 ? mods : 0;
            weak_mods = source==1 ? mods : 0;
            owned_mods = source==2 ? mods : 0;
            owned_weak_mods = source==3 ? mods : 0;
            actual_keyboard_report.keys[0]=4;
            assert(!ak820_gui_process(QK_MAGIC_GUI_OFF, true));
            assert(actual_keyboard_report.mods==(mods & ~0x88));
            assert(actual_keyboard_report.keys[0]==4);
            assert((real_mods|weak_mods|owned_mods|owned_weak_mods)==mods);
            assert(!ak820_gui_process(QK_MAGIC_GUI_ON, true));
            assert(actual_keyboard_report.mods==mods);
            assert((real_mods|weak_mods|owned_mods|owned_weak_mods)==mods);
        }
    }
    /* Mixed owners, immediate change, release and repeated state commands. */
    real_mods=0x09; weak_mods=0x82; owned_mods=0x24; owned_weak_mods=0x40;
    ak820_gui_process(QK_MAGIC_GUI_ON, true);
    assert(sent.mods==0xef);
    ak820_gui_process(QK_MAGIC_GUI_OFF, true);
    assert(sent.mods==0x67);
    unsigned before=sends;
    ak820_gui_process(QK_MAGIC_GUI_OFF, true);
    ak820_gui_process(QK_MAGIC_TOGGLE_GUI, false);
    assert(sends==before && gui_disabled);
    ak820_gui_process(QK_MAGIC_TOGGLE_GUI, true);
    assert(sent.mods==0xef && !gui_disabled);
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='ak820-gui-host-') as directory:
    path=Path(directory)
    (path/'test.c').write_text(source)
    subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=undefined',
                    str(path/'test.c'),'-o',str(path/'test')],check=True)
    subprocess.run([str(path/'test')],check=True)
print('PASS GUI controls: exhaustive keycodes/states, all modifier masks and owner classes, immediate report updates, preserved keys and owners')
