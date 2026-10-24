#!/usr/bin/env python3
"""Compile the production compact NKRO handler with observable host seams."""
import re, subprocess, tempfile
from pathlib import Path
root = Path(__file__).resolve().parents[2]
text = (root/'quantum/quantum.c').read_text()
start = text.index('static bool process_ak820_nkro(')
end = text.index('\n}\n', start) + 3
source = '''#include <stdbool.h>
#include <stdint.h>
#include <assert.h>
#define QK_MAGIC_NKRO_ON 0x7011
#define QK_MAGIC_NKRO_OFF 0x7012
#define QK_MAGIC_TOGGLE_NKRO 0x7013
typedef struct { struct { bool pressed; } event; } keyrecord_t;
static union { uint16_t raw; struct { unsigned other:7; unsigned nkro:1; unsigned upper:8; }; } keymap_config;
static int clears, saves; static uint16_t saved; static bool old_mode;
void clear_keyboard(void) { ++clears; old_mode = keymap_config.nkro; }
void eeconfig_update_keymap(uint16_t value) { ++saves; saved = value; }
''' + text[start:end] + '''
int main(void) {
 keyrecord_t down = {{true}}, up = {{false}};
 keymap_config.raw = 0x1255;
 assert(process_ak820_nkro(4,&down)); assert(!clears && !saves);
 assert(!process_ak820_nkro(QK_MAGIC_NKRO_ON,&up)); assert(!clears && !saves);
 assert(!process_ak820_nkro(QK_MAGIC_NKRO_ON,&down));
 assert(!old_mode && keymap_config.nkro && clears==1 && saves==0);
 assert(!process_ak820_nkro(QK_MAGIC_NKRO_OFF,&down));
 assert(old_mode && !keymap_config.nkro && clears==2 && saves==0);
 assert(!process_ak820_nkro(QK_MAGIC_TOGGLE_NKRO,&down)); assert(keymap_config.nkro);
 assert(!process_ak820_nkro(QK_MAGIC_TOGGLE_NKRO,&up)); assert(keymap_config.nkro && saves==0);
 assert(!process_ak820_nkro(QK_MAGIC_TOGGLE_NKRO,&down)); assert(!keymap_config.nkro && saves==0);
 return 0;
}
'''
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp); (p/'test.c').write_text(source)
 subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=undefined',str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
print('PASS production NKRO handler: controls, releases, old-report cleanup, unrelated bits, volatile mode; no persistence call')
