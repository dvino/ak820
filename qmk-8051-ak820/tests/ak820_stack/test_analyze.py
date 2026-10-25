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

    def test_two_pop_guarded_split_dispatch(self):
        for base in (0, 0x2340):
            sequence = ['c0e0','c0f0','c3','7401','9516','d006','d005',
                        '5003',f'02{base+96:04x}','e516','f5f0','240b','83',
                        'f582','e5f0','2406','83','f583','e4','73']
            rows, addresses, at = {}, [], base
            for raw in sequence:
                addresses.append(at); rows[at] = bytes.fromhex(raw); at += len(rows[at])
            rows[base+80] = rows[base+96] = b'\x22'
            code = {pc+i:v for pc,raw in rows.items() for i,v in enumerate(raw)}
            code.update({at: (base+80)&255, at+1:(base+80)&255,
                         at+2:(base+80)>>8, at+3:(base+80)>>8})
            guard = addresses[2]
            proof = m.Analyzer(rows,code).guarded_pop_split_dispatch(guard)
            self.assertEqual(proof['stack_delta'], -2)
            self.assertEqual(m.Analyzer(rows,code).bound(base)['bound'], 2)
            for entry in (addresses[9], addresses[-1]):
                self.assertIsNone(m.Analyzer(rows,code).bound(entry)['bound'])
            # Each instruction contract is essential; register POPs may not
            # overwrite the range index, carry, SP, accumulator or B.
            for index, raw in ((2,'d3'), (3,'7402'), (4,'9517'), (5,'d016'),
                               (5,'d081'), (5,'d0d0'), (6,'d0e0'), (6,'d0f0'),
                               (7,'4003'), (7,'5004'), (9,'e517'), (10,'f582'),
                               (11,'240c'), (12,'93'), (13,'f583'), (14,'e516'),
                               (15,'24ff'), (16,'93'), (17,'f582'), (18,'00')):
                with self.subTest(base=base,index=index,raw=raw):
                    changed = {**rows, addresses[index]:bytes.fromhex(raw)}
                    self.assertIsNone(m.Analyzer(changed,code).guarded_pop_split_dispatch(guard))
                    self.assertIsNone(m.Analyzer(changed,code).bound(base)['bound'])
            missing = dict(code); del missing[at+3]
            self.assertIsNone(m.Analyzer(rows,missing).guarded_pop_split_dispatch(guard))
            self.assertIsNone(m.Analyzer(rows,missing).bound(base)['bound'])
            # Guard/body/table destinations cannot turn data into instructions.
            for destination in (guard, addresses[9], at):
                bad = {**code, at:destination&255, at+2:destination>>8}
                self.assertIsNone(m.Analyzer(rows,bad).guarded_pop_split_dispatch(guard))
            # Known instruction bytes cannot also serve as table data.
            self.assertIsNone(m.Analyzer({**rows,at:b'\x22'},code)
                              .guarded_pop_split_dispatch(guard))
            # A table destination in the middle of a known instruction fails.
            interior = base+97
            bad = {**code, at:interior&255, at+2:interior>>8}
            overlapping = {**rows, base+96:b'\x90\x00\x00'}
            self.assertIsNone(m.Analyzer(overlapping,bad).guarded_pop_split_dispatch(guard))
            # Entering with fewer than two saved bytes remains a failure.
            for entry in (guard, addresses[1]):
                self.assertIsNone(m.Analyzer(rows,code).bound(entry)['bound'])

    def test_register_split_dispatch_and_mutations(self):
        rows = {0:'ee', 1:'24fe', 3:'403b', 5:'ee', 6:'240a', 8:'83',
                9:'f582', 11:'ee', 12:'2406', 14:'83', 15:'f583',
                17:'e4', 18:'73', 48:'22', 64:'22'}
        instructions = {pc:bytes.fromhex(raw) for pc,raw in rows.items()}
        code = {pc+i:v for pc,raw in instructions.items() for i,v in enumerate(raw)}
        code.update({19:48, 20:48, 21:0, 22:0})
        self.assertEqual(m.Analyzer(instructions,code).bound(0)['bound'], 0)
        for pc, raw in ((0,'ef'), (1,'24fd'), (3,'503b'), (11,'ef'), (12,'24ff')):
            with self.subTest(pc=pc):
                self.assertIsNone(m.Analyzer({**instructions,pc:bytes.fromhex(raw)},code).bound(0)['bound'])
        self.assertIsNone(m.Analyzer(instructions,code).bound(18)['bound'])

    def test_register_triple_dispatch_and_mutations(self):
        rows = {0:'ed', 1:'24fe', 3:'4010', 5:'ed', 6:'2d', 7:'2d',
                8:'90000c', 11:'73', 12:'020015', 15:'020015', 21:'22'}
        self.assertEqual(self.analyze(rows)['bound'], 0)
        for pc, raw in ((0,'ec'), (1,'24fd'), (6,'2e'), (8,'90000d'), (15,'73')):
            with self.subTest(pc=pc):
                self.assertIsNone(self.analyze({**rows,pc:raw})['bound'])
        # Saving the accumulator instead of loading it preserves the index too.
        self.assertEqual(self.analyze({**rows,0:'fd'})['bound'], 0)
        self.assertEqual(self.analyze({**rows,15:'22'})['bound'], 0)
        self.assertIsNone(m.Analyzer({pc:bytes.fromhex(raw) for pc,raw in rows.items()}).bound(11)['bound'])

    def test_full_16bit_range_dispatch(self):
        sequence = ['c3','ee','9420','ef','9478','5003','020080','c3',
                    '7421','9e','7478','9f','4000','ee','24e0','fe',
                    '240a','83','f582','ee','2406','83','f583','e4','73']
        rows, addresses, at = {}, [], 0
        for raw in sequence:
            addresses.append(at); rows[at] = bytes.fromhex(raw); at += len(rows[at])
        rows[addresses[12]] = bytes((0x40, 128 - addresses[13]))
        rows[96] = rows[128] = b'\x22'
        code = {pc+i:v for pc,raw in rows.items() for i,v in enumerate(raw)}
        code.update({at:96,at+1:96,at+2:0,at+3:0})
        self.assertEqual(m.Analyzer(rows,code).bound(0)['bound'], 0)
        for index, raw in ((10,'7479'), (9,'9f'), (14,'24e1'), (8,'741f'), (5,'4003')):
            with self.subTest(index=index):
                self.assertIsNone(m.Analyzer({**rows,addresses[index]:bytes.fromhex(raw)},code).bound(0)['bound'])
        self.assertIsNone(m.Analyzer(rows,code).bound(addresses[24])['bound'])

    def test_candidate_reads_do_not_claim_instruction_boundaries(self):
        analyzer = m.Analyzer({0:b'\x22'}, {0:0x22, 16:0x90, 17:0x22, 18:0})
        self.assertEqual(analyzer.peek_instruction(16), b'\x90\x22\x00')
        self.assertNotIn(16, analyzer.instructions)
        self.assertEqual(analyzer.instruction(17), b'\x22')
        self.assertIsNone(analyzer.peek_instruction(16))

    def test_getter_register_guard(self):
        rows = {0:'120030', 3:'24fe', 5:'4010', 7:'ef', 8:'2f', 9:'2f',
                10:'90000e', 13:'73', 14:'020017', 17:'020017', 23:'22',
                48:'900100', 51:'e0', 52:'ff', 53:'22'}
        self.assertEqual(self.analyze(rows)['bound'], 2)
        for pc, raw in ((52,'fe'), (3,'24fd'), (5,'5010'), (53,'32')):
            with self.subTest(pc=pc):
                self.assertIsNone(self.analyze({**rows,pc:raw})['bound'])

    def test_masked_helper_dispatch(self):
        rows = {0:'120020', 3:'fe', 4:'2e', 5:'900009', 8:'73',
                9:'8002', 11:'8000', 13:'22', 32:'900100', 35:'e0',
                36:'03', 37:'5401', 39:'22'}
        self.assertEqual(self.analyze(rows)['bound'], 2)
        for pc, raw in ((37,'5403'), (39,'32'), (36,'04'), (3,'ff'), (11,'73')):
            with self.subTest(pc=pc):
                self.assertIsNone(self.analyze({**rows,pc:raw})['bound'])

    def test_masked_bit_dispatch(self):
        rows = {0:'5401', 2:'ff', 3:'2f', 4:'2f', 5:'900009', 8:'73',
                9:'c280', 11:'22', 12:'c281', 14:'22'}
        self.assertEqual(self.analyze(rows)['bound'], 0)
        for pc, raw in ((0,'5403'), (2,'fe'), (3,'2e'), (5,'90000a'), (12,'d281')):
            with self.subTest(pc=pc):
                self.assertIsNone(self.analyze({**rows,pc:raw})['bound'])
        self.assertIsNone(m.Analyzer({pc:bytes.fromhex(raw) for pc,raw in rows.items()}).bound(8)['bound'])

    def test_register_dispatch_jnc_in_range(self):
        rows = {0:'fd', 1:'24fe', 3:'5001', 5:'22', 6:'ed', 7:'2d', 8:'2d',
                9:'90000d', 12:'73', 13:'020016', 16:'020016', 22:'22'}
        self.assertEqual(self.analyze(rows)['bound'], 0)
        self.assertIsNone(self.analyze({**rows,3:'5002'})['bound'])
        self.assertIsNone(self.analyze({**rows,1:'2480'})['bound'])

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

    def test_deep_acyclic_graph_has_no_arbitrary_depth_limit(self):
        rows = {pc:bytes((0x12,(pc+4)>>8,(pc+4)&255)) for pc in range(0,600,4)}
        rows.update({pc+3:b'\x22' for pc in range(0,600,4)})
        rows[600]=b'\x22'
        result=m.Analyzer(rows).bound(0)
        self.assertEqual(result['bound'], 300)
        self.assertEqual(result['unresolved'], [])

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

    def test_rom_dptr_tail_callback(self):
        rows = {0:'900080',3:'e4',4:'93',5:'fe',6:'a3',7:'e4',8:'93',9:'ff',
                10:'120020',13:'22',32:'8e82',34:'8f83',36:'e4',37:'73',
                64:'c0e0',66:'d0e0',68:'22'}
        instructions = {pc:bytes.fromhex(raw) for pc,raw in rows.items()}
        code = {pc+i:v for pc,raw in instructions.items() for i,v in enumerate(raw)}
        code.update({128:64,129:0})
        analyzer = m.Analyzer(instructions,code)
        self.assertEqual(analyzer.bound(0)['bound'], 3)
        self.assertEqual(analyzer.pointer_transfers[0]['height_at_callback'], 2)
        for pc, raw in ((34,'8e83'), (36,'04'), (4,'e0')):
            with self.subTest(pc=pc):
                self.assertIsNone(m.Analyzer({**instructions,pc:bytes.fromhex(raw)},code).bound(0)['bound'])

    def test_private_guard_source_all_identifier_uses_are_checked(self):
        source = ('static bool owned;\nif (owned) return;\n'
                  'owned = true;\nowned = false;\n')
        self.assertTrue(m.private_guard_source_contract(source, 'owned'))
        commented = source.replace('if (owned)', 'if (/**/owned/**/)')
        self.assertTrue(m.private_guard_source_contract(commented, 'owned'))
        self.assertTrue(m.private_guard_source_contract(source + '// &owned\n', 'owned'))
        for extra in ('use(&owned);', 'use(&(owned));', 'use(&/**/(owned));',
                      'PASS(owned);', '#define ALIAS owned', 'void *p = &owned;',
                      'owned = false;', 'use(owned);', '#define owned other'):
            with self.subTest(extra=extra):
                self.assertFalse(m.private_guard_source_contract(source+extra+'\n', 'owned'))
        for changed in (source.replace('static bool', 'bool'),
                        source.replace('if (owned)', 'if ((owned))'),
                        source.replace('= true', '= value'),
                        source.replace('owned = false;', 'CLEAR(owned);')):
            self.assertFalse(m.private_guard_source_contract(changed, 'owned'))

    def test_context_guard_proves_owned_recursion(self):
        rows = {0:'900123',3:'e0',4:'6001',6:'22',7:'900123',10:'7401',
                12:'f0',13:'120000',16:'900123',19:'e4',20:'f0',21:'22'}
        instructions = {pc:bytes.fromhex(raw) for pc,raw in rows.items()}
        analyzer = m.Analyzer(instructions)
        analyzer.configure_guards({0x123})
        self.assertEqual(analyzer.bound(0)['bound'], 2)
        for pc, raw in ((10,'7400'), (4,'7001'), (7,'900124')):
            with self.subTest(pc=pc):
                mutant = m.Analyzer({**instructions,pc:bytes.fromhex(raw)})
                mutant.configure_guards({0x123})
                self.assertIsNone(mutant.bound(0)['bound'])

    def test_guard_callee_must_preserve_ancestor_ownership(self):
        rows = {0:'900123',3:'e0',4:'6001',6:'22',7:'900123',10:'7401',
                12:'f0',13:'120020',16:'900123',19:'e4',20:'f0',21:'22',
                32:'900123',35:'e4',36:'f0',37:'22'}
        analyzer = m.Analyzer({pc:bytes.fromhex(raw) for pc,raw in rows.items()})
        analyzer.configure_guards({0x123})
        self.assertIsNone(analyzer.bound(0)['bound'])

    def test_guarded_rom_callback_full_range_and_mutations(self):
        raw = bytes.fromhex('8d038e04c3eb9421ec94784041742a9b74789c4039'
            'ed24dffd900123f0ef600790012374016df0900123e075f002a4'
            '2400f582740335f0f583120200c007c006120210120220d006d00722')
        rows, pc = {}, 0
        while pc < len(raw):
            length = m.OPCODE_LENGTHS[raw[pc]]
            rows[pc] = raw[pc:pc+length]
            pc += length
        rows[0x4e] = b'\x22'
        for base, body in ((0x200,'e493fea3e493ff22'),(0x210,'8e828f8322'),
                           (0x220,'e473'),(0x400,'c0e0d0e022')):
            data, offset = bytes.fromhex(body), 0
            while offset < len(data):
                size = m.OPCODE_LENGTHS[data[offset]]
                rows[base+offset] = data[offset:offset+size]
                offset += size
        code = {pc+i:value for pc,row in rows.items() for i,value in enumerate(row)}
        code.update({0x300+i:value for i,value in enumerate(b'\x00\x04'*10)})
        analyzer = m.Analyzer(rows,code)
        self.assertEqual(analyzer.bound(0)['bound'],5)
        proof = analyzer.guarded_rom_callback_dispatch(0)
        self.assertEqual(len(proof['rom_slots']),10)
        # Range polarity/limit, saved register identity, XOR, local reload,
        # helper target and ROM byte completeness all fail closed.
        for address in (0,5,9,11,13,18,22,30,35,40,45,49,56,60):
            with self.subTest(address=address):
                mutated = bytearray(raw)
                mutated[address] ^= 1
                changed = {pc:bytes(mutated[pc:pc+len(row)]) for pc,row in rows.items() if pc < len(raw)}
                candidate = {**rows,**changed}
                try:
                    result = m.Analyzer(candidate,{**code,address:mutated[address]}).guarded_rom_callback_dispatch(0)
                except ValueError:
                    result = None
                self.assertIsNone(result)
        missing = dict(code)
        del missing[0x313]
        self.assertIsNone(m.Analyzer(rows,missing).guarded_rom_callback_dispatch(0))

    def test_compact_callback_guards_getter_and_rom_provenance(self):
        raw = bytes.fromhex(
            'ed24e0ff70051204008054ef24f5403eed24dffe900123f0'
            '120200e5825422600790012374016ef0900123e075f002a4'
            '2400f5827403120220fda3e493fec006c005120230120240')
        rows = {}
        def add(base, data):
            offset = 0
            while offset < len(data):
                size = m.OPCODE_LENGTHS[data[offset]]
                rows[base+offset] = data[offset:offset+size]
                offset += size
        add(0,raw)
        # The guard's default and the toggle's continuation are real exits.
        add(0x4e,b'\x22'); add(0x5f,b'\x22')
        add(len(raw), b'\xd0\x05\xd0\x06\x22')
        for base, body in ((0x200,'c007900500e0ff900501120210d00722'),
                           (0x210,'e042078f8222'),
                           (0x220,'35f0f583e49322'),(0x230,'8d828e8322'),
                           (0x240,'e473'),(0x400,'c0e0d0e022')):
            add(base,bytes.fromhex(body))
        code = {pc+i:value for pc,row in rows.items() for i,value in enumerate(row)}
        code.update({0x300+i:value for i,value in enumerate(b'\x00\x04'*10)})
        analyzer = m.Analyzer(rows,code,{0x123})
        self.assertIsNone(m.Analyzer(rows,code).compact_rom_callback_dispatch(0))
        relocated = {pc:(b'\x90\x01\x24' if row == b'\x90\x01\x23' else row)
                     for pc,row in rows.items()}
        self.assertIsNone(m.Analyzer(relocated,code,{0x123}).compact_rom_callback_dispatch(0))
        proof = analyzer.compact_rom_callback_dispatch(0)
        self.assertIsNotNone(proof)
        self.assertEqual(proof['rom_slots'],list(range(0x300,0x314,2)))
        self.assertEqual(proof['getter_peak'],3)
        self.assertEqual(analyzer.bound(0)['bound'],5)
        # Structural opcodes and register identities are part of the proof. Changed helper
        # bodies, memory writes and register clobbers must not grant targets.
        for address in (0,2,3,4,6,12,14,17,19,21,25,28,32,35,37,40,
                        42,45,47,49,51,54,57,60,61,62,63,64,66,68,71):
            with self.subTest(address=address):
                mutated = bytearray(raw); mutated[address] ^= 1
                changed = {pc:bytes(mutated[pc:pc+len(row)])
                           for pc,row in rows.items() if pc < len(raw)}
                try:
                    candidate = m.Analyzer({**rows,**changed},
                        {**code,**{i:v for i,v in enumerate(mutated)}},{0x123})
                    self.assertIsNone(candidate.compact_rom_callback_dispatch(0))
                except ValueError:
                    pass
        for address, row in ((0x205,b'\xf0'),(0x206,b'\xfe'),
                             (0x210,b'\xf0'),(0x220,b'\x25\xf0'),
                             (0x230,b'\x8e\x82'),(0x240,b'\x04')):
            with self.subTest(helper=address):
                self.assertIsNone(m.Analyzer({**rows,address:row},code,{0x123})
                                  .compact_rom_callback_dispatch(0))
        # The table's actual bytes select the analyzed target; target numbers
        # are never inferred from a symbol name or neighboring code.
        deeper = dict(rows)
        deeper[0x500] = b'\xc0\xe0'
        deeper[0x502] = b'\xc0\xe0'
        deeper[0x504] = b'\xd0\xe0'
        deeper[0x506] = b'\xd0\xe0'
        deeper[0x508] = b'\x22'
        changed_code = {**code,0x300:0,0x301:5}
        changed = m.Analyzer(deeper,changed_code,{0x123})
        self.assertEqual(changed.bound(0)['bound'],6)
        self.assertIn(0x500,changed.guarded_callback_transfers[0]['targets'])
        missing = dict(code); del missing[0x313]
        self.assertIsNone(m.Analyzer(rows,missing,{0x123}).compact_rom_callback_dispatch(0))
        self.assertIsNone(m.Analyzer(rows,code,{0x123}).bound(0x241)['bound'])

    def test_compact_spill_requires_unique_one_byte_xseg_allocation(self):
        with tempfile.TemporaryDirectory() as folder:
            build = Path(folder)
            (build/'dce').mkdir()
            (build/'ajazz_ak820_vial.ihx').write_text(':0100000022DD\n:00000001FF\n')
            (build/'ajazz_ak820_vial.map').write_text('C:  00000000 _main\n')
            listing = build/'dce/process_rgb.rst'
            allocation = ('  1 .area XSEG (XDATA)\n'
                          '  000123 2 _process_rgb_action_10000_277:\n'
                          '  000123 3 .ds 1\n')
            listing.write_text(allocation)
            identity = m.load(build)[3]
            self.assertEqual(identity['compact_callback_spills'][0x123]['symbol'],
                             '_process_rgb_action_10000_277')
            for changed in (allocation.replace('XSEG','XABS'),
                            allocation.replace('.ds 1','.ds 2'),
                            allocation.replace('000123 3','000124 3'),
                            allocation+allocation,
                            allocation.replace('_process_rgb_action_','_other_action_')):
                with self.subTest(allocation=changed):
                    listing.write_text(changed)
                    self.assertEqual(m.load(build)[3]['compact_callback_spills'],{})

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
