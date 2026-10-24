import importlib.util
from pathlib import Path
import unittest
import tempfile

spec = importlib.util.spec_from_file_location('stack_analyze', Path(__file__).with_name('analyze.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class StackTests(unittest.TestCase):
    def analyze(self, rows):
        return m.Analyzer({pc: bytes.fromhex(raw) for pc, raw in rows.items()}).bound(0)

    def test_call_frame_and_tail_transfer(self):
        result = self.analyze({0:'c0e0', 2:'120010', 5:'d0e0', 7:'22',
                               16:'020020', 32:'c0f0', 34:'d0f0', 36:'22'})
        self.assertEqual(result['bound'], 4)  # caller PUSH + return PC + callee PUSH

    def test_acall_page_and_ajmp(self):
        result = self.analyze({0:'1110', 2:'22', 16:'0120', 32:'22'})
        self.assertEqual(result['bound'], 2)

    def test_balanced_loop(self):
        self.assertEqual(self.analyze({0:'c0e0', 2:'d0e0', 4:'70fa', 6:'22'})['bound'], 1)

    def test_recursion_fails_closed(self):
        result = self.analyze({0:'120000', 3:'22'})
        self.assertIsNone(result['bound'])
        self.assertIn('recursive', result['unresolved'][0]['reason'])

    def test_unknown_indirect_and_external_target(self):
        for rows in ({0:'73'}, {0:'020100'}, {0:'120100', 3:'22'}):
            self.assertIsNone(self.analyze(rows)['bound'])

    def test_unbalanced_stack_and_growing_loop(self):
        for rows in ({0:'c0e0', 2:'22'}, {0:'d0e0', 2:'22'}, {0:'c0e0', 2:'80fc'}):
            self.assertIsNone(self.analyze(rows)['bound'])

    def test_all_sp_destinations(self):
        for raw in ('758100', '858281', '438101', '5281', 'd58100',
                    '638100', '8681', '8881', 'c581', 'd081', 'f581'):
            with self.subTest(raw=raw):
                self.assertIsNone(self.analyze({0:raw})['bound'])

    def test_constant_sp_adjustment(self):
        self.assertEqual(self.analyze({0:'0581', 2:'1581', 4:'22'})['bound'], 1)
        self.assertIsNone(self.analyze({0:'1581', 2:'22'})['bound'])

    def test_guarded_short_table_and_mutations(self):
        rows = {0:'fe', 1:'24fe', 3:'4010', 5:'ee', 6:'2e', 7:'90000b',
                10:'73', 11:'8008', 13:'8006', 21:'22'}
        self.assertEqual(self.analyze(rows)['bound'], 0)
        for pc, bad in ((1,'24fd'), (3,'5010'), (5,'ef'), (7,'90000c'), (13,'22')):
            with self.subTest(pc=pc):
                self.assertIsNone(self.analyze({**rows, pc:bad})['bound'])

    def test_guarded_split_table_and_mutations(self):
        rows = {0:'c0e0', 2:'c3', 3:'7401', 5:'9526', 7:'d007', 9:'5003',
                11:'020050', 14:'e526', 16:'f5f0', 18:'240b', 20:'83',
                21:'f582', 23:'e5f0', 25:'2406', 27:'83', 28:'f583', 30:'e4',
                31:'73', 64:'22', 80:'22'}
        instructions = {pc:bytes.fromhex(raw) for pc,raw in rows.items()}
        code = {pc+i:value for pc,raw in instructions.items() for i,value in enumerate(raw)}
        code.update({32:64, 33:64, 34:0, 35:0})
        self.assertEqual(m.Analyzer(instructions, code).bound(0)['bound'], 1)
        for pc, bad in ((3,'7402'), (5,'95a6'), (9,'4003'), (14,'e527'), (25,'24ff')):
            with self.subTest(pc=pc):
                self.assertIsNone(m.Analyzer({**instructions,pc:bytes.fromhex(bad)},code).bound(0)['bound'])

    def test_sp_read_is_not_write(self):
        self.assertEqual(self.analyze({0:'858182', 3:'22'})['bound'], 0)

    def test_partial_peak_never_reported_as_bound(self):
        result = self.analyze({0:'c0e0', 2:'6001', 4:'73', 5:'d0e0', 7:'22'})
        self.assertIsNone(result['bound'])
        self.assertEqual(result['explored_peak'], 1)

    def test_instruction_boundaries_and_library_decoder(self):
        for rows in ({0:b'\xc0\xe0\xc0\xf0'}, {0:b'\x12\x00\x10',1:b'\x00'}):
            with self.assertRaises(ValueError): m.Analyzer(rows)
        # Known instruction interior cannot become a second entry.
        self.assertIsNone(self.analyze({0:'020001'})['bound'])
        # A library callee without a listing is decoded from the IHX bytes.
        result = m.Analyzer({0:b'\x12\x00\x10',3:b'\x22'},
            {0:0x12,1:0,2:16,3:0x22,16:0xc0,17:0xe0,18:0xd0,19:0xe0,20:0x22}).bound(0)
        self.assertEqual(result['bound'], 3)

    def test_split_pop_cannot_overwrite_index(self):
        rows = {0:'c0e0', 2:'c3', 3:'7401', 5:'9507', 7:'d007', 9:'5003',
                11:'020050', 14:'e507', 16:'f5f0', 18:'240b', 20:'83',
                21:'f582', 23:'e5f0', 25:'2406', 27:'83', 28:'f583', 30:'e4',
                31:'73', 64:'22', 80:'22'}
        instructions={pc:bytes.fromhex(raw) for pc,raw in rows.items()}
        code={pc+i:value for pc,raw in instructions.items() for i,value in enumerate(raw)}
        code.update({32:64,33:64,34:0,35:0})
        self.assertIsNone(m.Analyzer(instructions,code).bound(0)['bound'])

    def test_analysis_depth_limit_fails_closed(self):
        rows = {pc:bytes((0x12,(pc+4)>>8,(pc+4)&255)) for pc in range(0,600,4)}
        rows.update({pc+3:b'\x22' for pc in range(0,600,4)})
        rows[600]=b'\x22'
        result=m.Analyzer(rows).bound(0)
        self.assertIsNone(result['bound'])
        self.assertTrue(any('depth limit' in item['reason'] for item in result['unresolved']))

    def test_rom_pointer_thunk_provenance_and_frames(self):
        rows = {0:'900080',3:'e4',4:'93',5:'fc',6:'a3',7:'e4',8:'93',9:'fd',
                10:'c005',12:'c004',14:'e0',15:'c0e0',17:'120020',20:'801a',
                32:'c004',34:'c005',36:'22',48:'1581',50:'d004',52:'d005',54:'22',
                64:'c0e0',66:'d0e0',68:'22'}
        instructions={pc:bytes.fromhex(raw) for pc,raw in rows.items()}
        code={pc+i:value for pc,raw in instructions.items() for i,value in enumerate(raw)}
        code.update({128:64,129:0})
        analyzer=m.Analyzer(instructions,code)
        result=analyzer.bound(0)
        self.assertEqual(result['bound'],7)  # saved pair + argument + call PC + pushed pointer
        pointer=analyzer.pointer_transfers[0]
        self.assertEqual((pointer['target'],pointer['rom_slot']), (64,128))
        self.assertEqual(pointer['height_at_callback'],5)  # Pointer consumed; CALL frame retained.
        self.assertEqual(pointer['height_after_return'],3)
        for pc,bad in ((4,'e0'),(8,'e0'),(32,'c005'),(34,'c004'),(5,'fb')):
            with self.subTest(pc=pc):
                changed={**instructions,pc:bytes.fromhex(bad)}
                self.assertIsNone(m.Analyzer(changed,code).bound(0)['bound'])
        # Changing the actual ROM entry changes the reached callback and peak.
        deeper={96+2*i:b'\xc0\xe0' for i in range(5)}
        deeper.update({106+2*i:b'\xd0\xe0' for i in range(5)})
        deeper[116]=b'\x22'
        changed_code={**code,128:96}
        changed_code.update({pc+i:value for pc,raw in deeper.items() for i,value in enumerate(raw)})
        changed=m.Analyzer({**instructions,**deeper},changed_code)
        self.assertEqual(changed.bound(0)['bound'],10)  # live5 plus callback5
        self.assertEqual(changed.pointer_transfers[0]['target'],96)

    def test_exact_listing_and_ihx_rejections(self):
        with tempfile.TemporaryDirectory() as folder:
            build = Path(folder)
            (build/'dce').mkdir()
            image = build/'ajazz_ak820_vial.ihx'
            listing = build/'dce/test.rst'
            (build/'ajazz_ak820_vial.map').write_text('C:  00000000 _main\n')
            listing.write_text('  000000 22 [24] 1 ret\n')
            valid = ':0100000022DD\n:00000001FF\n'
            image.write_text(valid)
            instructions, symbols, code, identity = m.load(build)
            self.assertEqual(instructions, {0:b'\x22'})
            self.assertEqual(symbols['_main'], 0)
            self.assertEqual(len(identity['listing_sha256']), 1)
            for invalid in (valid.replace('DD','DC'), valid.splitlines()[0]+'\n',
                            valid.replace(':00000001FF', ':0100000022DD\n:00000001FF')):
                image.write_text(invalid)
                with self.assertRaises(ValueError): m.load(build)
            image.write_text(valid)
            listing.write_text('  000000 00 [12] 1 nop\n')
            with self.assertRaises(ValueError): m.load(build)
            image.write_text(':04000000C0E0C0F0AC\n:00000001FF\n')
            listing.write_text('  000000 C0 E0 C0 F0 [12] 1 push\n')
            with self.assertRaises(ValueError): m.load(build)


if __name__ == '__main__':
    unittest.main()
