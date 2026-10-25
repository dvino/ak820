#!/usr/bin/env python3
"""Compare the integrated getter body against current compiler-resolved defaults."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[2]
QMK=ROOT/'qmk-8051-ak820'
sys.path.insert(0,str(QMK/'util'))
import ak820_default_keymap as codec
p=argparse.ArgumentParser();p.add_argument('bootstrap',type=Path);a=p.parse_args()
raw=codec.literal_block(a.bootstrap.read_text(),'_keymaps')
source=(QMK/'quantum/keymap_introspection.c').read_text()
start=source.index('uint16_t keycode_at_keymap_location_raw(')
end=source.index('\n#ifndef VIA_ENABLE',start)
getter=source[start:end]
with tempfile.TemporaryDirectory(prefix='ak820-default-decoder-') as temporary:
    directory=Path(temporary)
    c='#include <stdint.h>\n#include <stdio.h>\n#define __code\n#define AK820_COMPRESS_DEFAULT_KEYMAP\n#define MATRIX_ROWS 16\n#define MATRIX_COLS 8\n#define KC_NO 0\n#define KC_TRNS 1\n#define NUM_KEYMAP_LAYERS_RAW 2\n'
    c+=codec.generate(a.bootstrap.read_text())+getter
    c+='\nstatic const uint8_t reference[] = {'+','.join(map(str,raw))+'};\n'
    c+='int main(void){unsigned l,r,c;for(l=0;l<256;l++)for(r=0;r<256;r++)for(c=0;c<256;c++){uint16_t expected=1;if(l<2&&r<16&&c<8){unsigned i=((l*16+r)*8+c)*2;expected=reference[i]|((uint16_t)reference[i+1]<<8);}if(keycode_at_keymap_location_raw(l,r,c)!=expected)return 1;}puts("PASS: integrated getter, all 16777216 uint8 triples");return 0;}\n'
    (directory/'check.c').write_text(c)
    subprocess.run(['cc','-std=c11','-O1','-fsanitize=address,undefined','-fno-omit-frame-pointer',str(directory/'check.c'),'-o',str(directory/'check')],check=True)
    subprocess.run([str(directory/'check')],check=True)
