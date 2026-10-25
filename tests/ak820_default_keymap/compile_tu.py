#!/usr/bin/env python3
"""Offline one-TU check using an existing configured build's exact flags."""
import argparse
import json
import os
import tempfile
from unittest.mock import patch
from pathlib import Path
import shlex
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
QMK=ROOT/'qmk-8051-ak820'
sys.path.insert(0,str(QMK/'util'))
import ak820_default_keymap as codec


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--flags',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--compiler',type=Path,required=True)
    a=p.parse_args()
    out=a.output.resolve()
    if out.exists():raise ValueError('Fresh output directory required')
    flags=shlex.split(a.flags.read_text())
    obj=out/'obj_ajazz_ak820_vial/quantum/keymap_introspection.o'
    obj.parent.mkdir(parents=True)
    command=[sys.executable,'util/ak820_default_keymap.py',str(a.compiler.resolve()),'-c']+flags+['-DAK820_COMPRESS_DEFAULT_KEYMAP','-Wp,-MD,-MF,'+str(obj.with_suffix('.d')),'quantum/keymap_introspection.c','-o',str(obj)]
    subprocess.run(command,cwd=QMK,check=True)
    generated=out/'default-keymap/ak820_default_keymap.inc'
    expected=generated.read_bytes()
    final=obj.with_suffix('.asm').read_text()
    bootstrap=(out/'default-keymap/bootstrap.asm').read_text()
    assert '_keymaps:' not in final
    assert len(codec.literal_block(bootstrap,'_keymaps'))==512
    for symbol in ('_encoder_map','_ak820_led_points'):
        assert codec.literal_block(bootstrap,symbol)==codec.literal_block(final,symbol)
    # A poisoned header is replaced on every compilation, including incremental TU recompiles.
    generated.write_text('#error stale include\n')
    subprocess.run(command,cwd=QMK,check=True)
    assert generated.read_bytes()==expected
    off=out/'off';off.mkdir()
    subprocess.run([str(a.compiler.resolve()),'-c']+flags+['-Wp,-MD,-MF,'+str(off/'off.d'),'quantum/keymap_introspection.c','-o',str(off/'off.o')],cwd=QMK,check=True)
    assert codec.literal_block((off/'off.asm').read_text(),'_keymaps')==codec.literal_block(bootstrap,'_keymaps')
    with tempfile.TemporaryDirectory(prefix='default-phase-',dir=QMK/'.build') as temp:
        temp=Path(temp)
        force=temp/'force.h'
        force.write_text('#define AK820_DEFAULT_KEYMAP_EXTRACT 1\n')
        result=subprocess.run(command+['--include',str(force)],cwd=QMK,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        assert result.returncode != 0
        assert not obj.exists() and not generated.exists()
        final_header=temp/'final.h'
        final_header.write_text('#define DEFAULT_FINAL_ONLY 1\n')
        force.write_text('#ifndef AK820_DEFAULT_KEYMAP_EXTRACT\n#include "final.h"\n#endif\n')
        racing=command[2:]+['--include',str(force)]
        real_run=subprocess.run
        changed=[]
        def run_with_edit(args, **kwargs):
            result=real_run(args,**kwargs)
            if '-E' in args and any('final-discovery.d' in arg for arg in args):
                final_header.write_text('#define DEFAULT_FINAL_ONLY 2\n')
                changed.append(True)
            return result
        previous=Path.cwd()
        try:
            os.chdir(QMK)
            with patch.object(codec.subprocess,'run',side_effect=run_with_edit):
                try:
                    codec.compile_current(racing)
                except ValueError as error:
                    assert 'Source changed during final compilation' in str(error), str(error)
                else:
                    raise AssertionError('Final-only header mutation accepted')
        finally:
            os.chdir(previous)
        assert changed and not obj.exists() and not generated.exists()
    subprocess.run(command,cwd=QMK,check=True)
    (out/'checks.json').write_text(json.dumps({'clean':True,'incremental_stale_replaced':True,'option_off_table_original':True,'encoder_unchanged':True,'led_unchanged':True,'private_phase_indirect_rejected':True,'final_only_header_change_rejected':True,'hardware':False},indent=2)+'\n')
    print('PASS: clean/incremental TU; stale include replaced; original off-table; encoder/LED bytes')

if __name__=='__main__':main()
