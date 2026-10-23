#!/usr/bin/env python3
"""Independent event/delay checks for the production native macro converter."""
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'util'))
from native_macro_import import convert_native_macros


def native_image(macros):
    """Documented Evision pointer table and fixed four-byte event format."""
    image = bytearray(16+len(macros)*2)
    for index,events in enumerate(macros):
        struct.pack_into('<H',image,16+index*2,len(image))
        image.extend(struct.pack('<HH',len(events),0))
        for delay,kind,value,down in events:
            image.extend(struct.pack('<HBB',delay,kind | (0x80 if down else 0),value))
    struct.pack_into('<HHH',image,0,0x55aa,len(image),len(macros))
    assert len(image) <= 9472
    return bytes(image)+bytes(9472-len(image))


def vial_events(stream):
    """Decode QMK down/up events and accumulate following base255 delays."""
    result=[]
    offset=0
    while offset < len(stream):
        assert stream[offset] == 1
        op=stream[offset+1]
        if op in (2,3):
            result.append([stream[offset+2],op==2,0])
            offset+=3
        elif op==4:
            assert result and stream[offset+2] and stream[offset+3]
            result[-1][2] += stream[offset+2]-1+(stream[offset+3]-1)*255
            offset+=4
        else:
            raise AssertionError('Unexpected generated opcode')
    return result


class NativeImportTest(unittest.TestCase):
    def test_all_keys_modifiers_and_delay_boundaries(self):
        keys=[(10,key,key) for key in range(4,0xa5)]
        keys += [(9,1<<bit,0xe0+bit) for bit in range(8)]
        for kind,value,key in keys:
            for delay in (0,1,254,255,256,65024,65025,65535):
                encoded=convert_native_macros(native_image([[(delay,kind,value,True),(delay,kind,value,False)]]))
                self.assertEqual(encoded.count(b'\0'),16)
                self.assertTrue(encoded.endswith(bytes(16)))
                self.assertEqual(vial_events(encoded.split(b'\0')[0]),[[key,True,delay],[key,False,delay]])

    def test_balanced_chords_and_empty_images(self):
        events=[(20,9,1,True),(30,10,6,True),(20,10,6,False),(0,9,1,False)]
        encoded=convert_native_macros(native_image([events]*16))
        self.assertEqual(len(encoded.split(b'\0')),17)
        self.assertEqual(vial_events(encoded.split(b'\0')[0]),[[0xe0,True,20],[6,True,30],[6,False,20],[0xe0,False,0]])
        self.assertEqual(convert_native_macros(bytes(9472)),bytes(16))
        self.assertEqual(convert_native_macros(native_image([])),bytes(16))

    def test_rejects_unknown_masks_options_unbalanced_and_overflow(self):
        for events in [[(0,9,3,True),(0,9,3,False)],[(0,10,4,True)],
                       [(0,10,4,False)],[(0,10,4,True),(0,10,4,True)],
                       [(0,11,4,True)],[(0,10,0,True)]]:
            with self.assertRaises(ValueError): convert_native_macros(native_image([events]))
        original=bytearray(native_image([[]]))
        variants=[]
        for index in (0,6,19,20):
            variant=bytearray(original); variant[index]=0xff; variants.append(variant)
        variant=bytearray(native_image([[],[]])); variant[18:20]=variant[16:18]; variants.append(variant)
        for variant in variants:
            with self.assertRaises(ValueError): convert_native_macros(variant)
        events=[(65024,10,4,True),(65024,10,4,False)]*1000
        with self.assertRaises(ValueError): convert_native_macros(native_image([events]))


if __name__ == '__main__':
    unittest.main()
