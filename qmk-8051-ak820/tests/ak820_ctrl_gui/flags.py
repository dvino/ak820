#!/usr/bin/env python3
"""Check independently enabled, disabled, and default-off feature gates."""
from pathlib import Path
import importlib.util
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
source_text=(ROOT/'quantum/action_util.c').read_text()
def function(name):
    start=source_text.index(name)
    return source_text[start:source_text.index('\n}\n',start)+3]
control=function('bool ak820_gui_process(')
prefix=r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#define QK_MAGIC_GUI_ON 0x7009
#define QK_MAGIC_GUI_OFF 0x700a
#define QK_MAGIC_TOGGLE_GUI 0x700b
#define QK_MAGIC_SWAP_CTL_GUI 0x701b
#define QK_MAGIC_UNSWAP_CTL_GUI 0x701c
#define QK_MAGIC_TOGGLE_CTL_GUI 0x701d
static unsigned sends;
void send_keyboard_report(void) { ++sends; }
'''
cases={
    'swap-only':('''#define AK820_COMPACT_CTRL_GUI_SWAP\nstatic bool ctrl_gui_swapped;\n''',r'''
int main(void) {
 assert(ak820_gui_process(0x7009,true));
 assert(ak820_gui_process(0x700a,false));
 assert(!ak820_gui_process(0x701b,true) && ctrl_gui_swapped && sends==1);
 assert(!ak820_gui_process(0x701b,false) && ctrl_gui_swapped && sends==1);
 assert(!ak820_gui_process(0x701c,true) && !ctrl_gui_swapped && sends==2);
 return 0;
}
'''),
    'lock-only':('''#define AK820_COMPACT_GUI_LOCK\nstatic bool gui_disabled;\n''',r'''
int main(void) {
 assert(ak820_gui_process(0x701b,true));
 assert(ak820_gui_process(0x701c,false));
 assert(ak820_gui_process(0x701d,true));
 assert(!ak820_gui_process(0x700a,true) && gui_disabled && sends==1);
 assert(!ak820_gui_process(0x700a,false) && gui_disabled && sends==1);
 assert(!ak820_gui_process(0x7009,true) && !gui_disabled && sends==2);
 return 0;
}
'''),
}
with tempfile.TemporaryDirectory(prefix='ak820-ctrl-gui-flags-') as directory:
    path=Path(directory)
    for name,(flags,main) in cases.items():
        c=path/(name+'.c'); exe=path/name
        c.write_text(prefix+flags+control+main)
        subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror',str(c),'-o',str(exe)],check=True)
        subprocess.run([str(exe)],check=True)

# The normal profile leaves the optional path off. With neither flag enabled,
# the declarations and pipeline call are excluded by their matching guards.
spec=importlib.util.spec_from_file_location('profiles',ROOT/'util/ak820_profiles.py')
profiles=importlib.util.module_from_spec(spec); spec.loader.exec_module(profiles)
assert profiles.configuration('standard')['make_options']['AK820_COMPACT_CTRL_GUI_SWAP']=='no'
assert profiles.configuration('full')['make_options']['AK820_COMPACT_CTRL_GUI_SWAP']=='no'
header=(ROOT/'quantum/action_util.h').read_text()
quantum=(ROOT/'quantum/quantum.c').read_text()
rules=(ROOT/'keyboards/ajazz/ak820/rules.mk').read_text()
assert '#if defined(AK820_COMPACT_GUI_LOCK) || defined(AK820_COMPACT_CTRL_GUI_SWAP)' in header
assert '#if defined(AK820_COMPACT_GUI_LOCK) || defined(AK820_COMPACT_CTRL_GUI_SWAP)' in quantum
assert 'AK820_COMPACT_CTRL_GUI_SWAP ?= no' in rules
# Both controls are handled in the short-circuit preprocessor chain before
# Dynamic Macro recording and Repeat history can see them.
start=quantum.index('if (!(',quantum.index('bool process_record_quantum_helper('))
end=quantum.index('            true)) {',start)
pipeline=quantum[start:end]
assert pipeline.index('ak820_gui_process(keycode, record->event.pressed)') < pipeline.index('process_dynamic_macro(keycode, record)')
assert pipeline.index('process_dynamic_macro(keycode, record)') < pipeline.index('process_last_key(keycode, record)')
print('PASS feature gates: swap-only and lock-only behavior, standard/full default-off profile wiring')
