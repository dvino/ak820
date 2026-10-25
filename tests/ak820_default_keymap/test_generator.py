#!/usr/bin/env python3
"""Strict compiler-data extraction and representation boundaries; no hardware."""
import importlib.util
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'qmk-8051-ak820/util'))
import ak820_default_keymap as codec


def assembly(words, metadata=(16,8,2,2,0,1)):
    lines = ['.area CONST (CODE)', '_keymaps:']
    lines += ['.byte #0x%02x, #0x%02x' % (v&255,v>>8) for v in words]
    lines += ['_ak820_default_metadata:']
    lines += ['.db #0x%02x' % v for v in metadata]
    lines += ['.area CSEG (CODE)']
    return '\n'.join(lines)


class GeneratorTests(unittest.TestCase):
    def test_current_values_high_word_and_specials(self):
        words=[0]*256
        for index,value in enumerate((0,1,0x1234,0x3412,255,256,65535)):
            words[index]=value
        raw=codec.literal_block(assembly(words),'_keymaps')
        classes,payload,offsets=codec.encode(raw,[16,8,2,2,0,1])
        self.assertEqual(payload,[0x34,0x12,0x12,0x34,255,0,1,255,255])
        self.assertEqual(offsets[1],9)
        self.assertNotEqual(codec.generate(assembly(words)),codec.generate(assembly([0]*256)))
        self.assertEqual(len(classes),64)
    def test_private_phase_is_reserved(self):
        for args in (['-DAK820_DEFAULT_KEYMAP_EXTRACT'],
                     ['-DAK820_DEFAULT_KEYMAP_EXTRACT=0'],
                     ['-UAK820_DEFAULT_KEYMAP_EXTRACT'],
                     ['-D', 'AK820_DEFAULT_KEYMAP_EXTRACT=1'],
                     ['-Wp,-DAK820_DEFAULT_KEYMAP_EXTRACT=1']):
            with self.assertRaises(ValueError):
                codec.reject_phase_overrides(args)
    def test_final_requires_exact_tables_without_bootstrap(self):
        bootstrap=assembly([0]*256)
        arrays=codec.encode(codec.literal_block(bootstrap,'_keymaps'),[16,8,2,2,0,1])
        final='.area CONST (CODE)\n'
        for name,values in zip(('classes','payload','offsets'),arrays):
            # Empty payload cannot occur in the supported current defaults.
            if not values: continue
            final+='_ak820_default_'+name+':\n.byte '+','.join('#0x%02x'%v for v in values)+'\n'
        with self.assertRaises(ValueError):codec.verify_final(final,bootstrap)
        words=[0]*256;words[0]=42
        bootstrap=assembly(words)
        arrays=codec.encode(codec.literal_block(bootstrap,'_keymaps'),[16,8,2,2,0,1])
        final='.area CONST (CODE)\n'
        for name,values in zip(('classes','payload','offsets'),arrays):
            final+='_ak820_default_'+name+':\n.byte '+','.join('#0x%02x'%v for v in values)+'\n'
        codec.verify_final(final,bootstrap)
        for bad in (final+'\n_keymaps:\n.byte #0x00',
                    final+'\n_ak820_default_metadata:\n.byte #0x00',
                    final.replace('#0x2a','#0x2b')):
            with self.assertRaises(ValueError):codec.verify_final(bad,bootstrap)
    def test_invalid_metadata(self):
        for index in range(6):
            metadata=[16,8,2,2,0,1];metadata[index]+=1
            with self.assertRaises(ValueError):codec.generate(assembly([0]*256,metadata))
    def test_count_payload(self):
        for words in ([0]*255,[0]*257,[65535]*256):
            with self.assertRaises(ValueError):codec.generate(assembly(words))
    def test_malformed(self):
        valid=assembly([0]*256)
        for bad in (valid.replace('_keymaps:', '_missing:'),valid+'\n_keymaps:',valid.replace('.area CONST (CODE)','.area XSEG (XDATA)'),valid.replace('.byte #0x00, #0x00','.word 0',1),valid.replace('.byte #0x00, #0x00','.byte #symbol, #0x00',1),valid.replace('.byte #0x00, #0x00','.byte #0x00+1, #0x00',1),valid.replace('.byte #0x00, #0x00','.byte #0x00',1)):
            with self.assertRaises(ValueError):codec.generate(bad)
    def test_all_classes_each_column(self):
        for col in range(8):
            for value in (0,1,254,0xbeef):
                words=[0]*256;words[31*8+col]=value
                codec.generate(assembly(words))

if __name__=='__main__':unittest.main()
