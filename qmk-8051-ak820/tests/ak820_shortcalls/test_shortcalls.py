"""Fail-closed controls for foreground short-transfer reassembly."""
import hashlib
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'util'))
import ak820_shortcalls as short
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'tools'))
from build_release_bundle import SDCC46_PINS


def encoding(target,kind='lcall'):
    return bytes([((target>>3)&0xe0)|(17 if kind=='lcall' else 1),target&255])


def instruction(address,opcode,operand,function='f',data=None):
    if data is None:
        data=bytes([18 if opcode=='lcall' else 2,0x11,0])
    return short.Instruction(address,data,opcode,operand,function,'CSEG')


def fixture():
    source=['; function f\n','_f:\n','\tlcall\t_g\n','\tret\n','; function g\n','_g:\n','\tret\n']
    return short.Module(source,{2:instruction(0x1000,'lcall','_g'),
        3:instruction(0x1003,'ret','','f',b'\x22'),
        6:instruction(0x1100,'ret','','g',b'\x22')},{('f','_f'):0x1000,('g','_g'):0x1100})


class ShortCallTests(unittest.TestCase):
    def test_recreated_empty_listing_directories_are_safe(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / 'source', root / 'target'
            (source / 'quantum').mkdir(parents=True)
            (source / 'quantum/test.asm').write_text('_test:\n\tret\n')
            (source / 'quantum/test.rst').write_text('stale listing')
            (source / 'reachability.json').write_text('{}\n')
            (target / 'quantum/empty').mkdir(parents=True)
            short.write_tree(source, target, [])
            self.assertEqual((target / 'quantum/test.asm').read_bytes(),
                             (source / 'quantum/test.asm').read_bytes())
            self.assertEqual((target / 'reachability.json').read_text(), '{}\n')
            self.assertFalse((target / 'quantum/test.rst').exists())

    def test_existing_outputs_and_links_are_rejected_without_changes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / 'source', root / 'target'
            source.mkdir()
            (source / 'test.asm').write_text('_test:\n\tret\n')
            target.mkdir()
            stale = target / 'stale.rst'
            stale.write_text('keep this')
            with self.assertRaisesRegex(ValueError, 'already exists'):
                short.write_tree(source, target, [])
            self.assertEqual(stale.read_text(), 'keep this')
            self.assertFalse((target / 'test.asm').exists())
            stale.unlink()
            stale.symlink_to(root / 'absent')
            with self.assertRaisesRegex(ValueError, 'already exists'):
                short.write_tree(source, target, [])
            self.assertTrue(stale.is_symlink())
            linked = root / 'linked'
            linked.symlink_to(target, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                short.write_tree(source, linked, [])
            regular = root / 'regular'
            regular.write_text('keep this too')
            with self.assertRaisesRegex(ValueError, 'already exists'):
                short.write_tree(source, regular, [])
            self.assertEqual(regular.read_text(), 'keep this too')

    def test_pc_plus_two_page_edge_for_both_kinds(self):
        for kind in ('lcall','ljmp'):
            self.assertTrue(short.short_valid(0x7fe,encoding(0x800,kind),0x800,kind))
            self.assertFalse(short.short_valid(0x7fe,encoding(0x7ff,kind),0x7ff,kind))
            self.assertTrue(short.short_valid(0x7fd,encoding(0x7ff,kind),0x7ff,kind))

    def test_wrong_opcode_target_length_and_kind_fail(self):
        for data,target,kind in ((encoding(0x1100,'ljmp'),0x1100,'lcall'),
            (encoding(0x1101),0x1100,'lcall'),(b'\x12\x11\x00',0x1100,'lcall'),
            (encoding(0x1100),0x1100,'unknown')):
            self.assertFalse(short.short_valid(0x1000,data,target,kind))

    def test_selection_excludes_hardware_outline_and_computed_functions(self):
        module=fixture()
        for name in ('ak820_flash.asm','ak820_nvm.asm','ak820_boot.asm','quantum/color.asm'):
            self.assertEqual(short.select({name:module},{})[0],[])
        candidates,_=short.select({'quantum/test.asm':module},{})
        self.assertEqual(len(candidates),1)
        for opcode,operand in [('jmp','@a+dptr'),('movc','a,@a+pc')]:
            modified=fixture();modified.instructions[8]=instruction(0x1020,opcode,operand,data=b'\x73')
            self.assertEqual(short.select({'quantum/test.asm':modified},{})[0],[])
        modified=fixture();modified.instructions[2]=instruction(0x1000,'lcall','_ak820_outline_0000')
        self.assertEqual(short.select({'quantum/test.asm':modified},{})[0],[])

    def test_full_name_symbols_disambiguate_truncated_map(self):
        with tempfile.TemporaryDirectory() as temporary:
            mapfile=Path(temporary)/'image.map'
            prefix='_'+'a'*31
            mapfile.write_text('C:   00001000  '+prefix+' module\nC:   00001100  '+prefix+' module\n')
            noice=mapfile.with_suffix('.noi')
            noice.write_text('DEF '+prefix+'one 0x1000\nDEF '+prefix+'two 0x1100\n')
            self.assertEqual(short.code_symbols(mapfile),{prefix+'one':0x1000,prefix+'two':0x1100})
            noice.write_text('DEF '+prefix+'one 0x1000\n')
            with self.assertRaisesRegex(ValueError,'Incomplete'):
                short.code_symbols(mapfile)

    def test_missing_or_disagreeing_symbols_fail(self):
        module=fixture()
        with self.assertRaisesRegex(ValueError,'ambiguous'):
            short.resolve(module,'f','_g',{'_g':0x1101})
        with self.assertRaisesRegex(ValueError,'Missing'):
            short.resolve(module,'f','_missing',{})

    def test_stale_source_hash_and_candidate_line_fail(self):
        module=fixture();candidate=short.select({'quantum/test.asm':module},{})[0][0]
        self.assertEqual(short.rewrite(module.source[2],candidate),'\tacall\t_g\n')
        with self.assertRaisesRegex(ValueError,'source hash'):
            short.rewrite('\tlcall\t_h\n',candidate)
        wrong={**candidate,'kind':'ljmp'}
        with self.assertRaisesRegex(ValueError,'instruction'):
            short.rewrite(module.source[2],wrong)

    def test_exact_source_and_all_edges_are_verified(self):
        module=fixture();name='quantum/test.asm'
        candidates=short.select({name:module},{})[0];candidate=candidates[0]
        after=fixture();after.source[2]=short.rewrite(after.source[2],candidate)
        after.instructions[2]=instruction(0x1000,'acall','_g',data=encoding(0x10ff))
        after.instructions[3]=instruction(0x1002,'ret','',data=b'\x22')
        after.instructions[6]=instruction(0x10ff,'ret','','g',b'\x22')
        after.labels[('g','_g')]=0x10ff
        result=short.verify({name:module},{name:after},{},{},candidates)
        self.assertEqual(result['verified_control_flow_edges'],1)
        after.instructions[2]=instruction(0x1000,'acall','_g',data=encoding(0x10fe))
        with self.assertRaisesRegex(ValueError,'edge differs'):
            short.verify({name:module},{name:after},{},{},candidates)
        after.source[3]='\tnop\n'
        with self.assertRaisesRegex(ValueError,'Unexpected'):
            short.verify({name:module},{name:after},{},{},candidates)

    def test_unchanged_nonedge_opcode_and_bytes_cannot_be_forged(self):
        name='quantum/test.asm';before=fixture();after=fixture()
        after.instructions[3]=instruction(0x1003,'ret','',data=b'\x00')
        with self.assertRaisesRegex(ValueError,'opcode/width'):
            short.verify({name:before},{name:after},{},{},[])
        before.source[3]=after.source[3]='\tmov\ta,#0x42\n'
        before.instructions[3]=instruction(0x1003,'mov','a,#0x42',data=b'\x74\x42')
        after.instructions[3]=instruction(0x1003,'mov','a,#0x42',data=b'\x74\x43')
        with self.assertRaisesRegex(ValueError,'nonrelocation'):
            short.verify({name:before},{name:after},{},{},[])

    def test_relative_branch_condition_bytes_are_invariant(self):
        name='quantum/test.asm';before=fixture();after=fixture()
        for module in (before,after):
            module.source[2]='\tcjne\ta,#0x01,001$\n'
            module.instructions[2]=instruction(0x1000,'cjne','a,#0x01,001$',data=b'\xb4\x01\x00')
        short.verify({name:before},{name:after},{},{},[])
        after.instructions[2]=instruction(0x1000,'cjne','a,#0x01,001$',data=b'\xb4\x02\x00')
        with self.assertRaisesRegex(ValueError,'condition bytes'):
            short.verify({name:before},{name:after},{},{},[])

    def test_preexisting_short_target_opcode_bits_may_relocate(self):
        name='quantum/test.asm';before=fixture();after=fixture()
        for module in (before,after):
            module.source[2]='\tacall\t_g\n'
        before.instructions[2]=instruction(0x1000,'acall','_g',data=encoding(0x1100))
        after.instructions[2]=instruction(0x1000,'acall','_g',data=encoding(0x1200))
        after.instructions[6]=instruction(0x1200,'ret','','g',b'\x22')
        after.labels[('g','_g')]=0x1200
        short.verify({name:before},{name:after},{},{},[])

    def test_diagnostic_page_marker_rejects_known_candidate_even_if_encoding_valid(self):
        with tempfile.TemporaryDirectory() as temporary:
            tree=Path(temporary);asm=tree/'quantum/test.asm';asm.parent.mkdir()
            asm.write_text('.area CSEG (CODE)\n; function f\n_f:\n\tacall\t_g\n')
            raw=(' '*34+'    1 .area CSEG (CODE)\n'+
                 ' '*34+'    2 ; function f\n'+
                 '      001000'+' '*22+'    3 _f:\n'+
                 '?ASlink-Warning-2K Page relocation error\n'+
                 '      001000 31 00            [24]    4 \tacall\t_g\n')
            rst=asm.with_suffix('.rst');rst.write_text(raw)
            candidate={'module':'quantum/test.asm','line':4,'function':'f','target':'_g','kind':'lcall',
                       'source_line_sha256':hashlib.sha256(b'\tlcall\t_g\n').hexdigest()}
            image={0x1000:0x31,0x1001:0}
            with self.assertRaisesRegex(ValueError,'unrecognized listing row'):
                short.modules(tree,image)
            with self.assertRaisesRegex(ValueError,'Unexpected diagnostic'):
                short.modules(tree,image,diagnostic_candidates=[],diagnostic_symbols={})
            rejected=[]
            short.modules(tree,image,diagnostic_candidates=[candidate],
                          diagnostic_symbols={'_g':0x1100},diagnostic_rejections=rejected)
            self.assertEqual(rejected,[{'module':'quantum/test.asm','line':4,
                'site':0x1000,'target':0x1100,'bytes':'3100','encoding_valid':True}])
            with self.assertRaisesRegex(ValueError,'candidate differs'):
                short.modules(tree,image,diagnostic_candidates=[{**candidate,'target':'_other'}],
                              diagnostic_symbols={'_other':0x1100})
            with self.assertRaises(ValueError):
                short.modules(tree,{0x1000:0x31,0x1001:1},diagnostic_candidates=[candidate],
                              diagnostic_symbols={'_g':0x1100})
            short.modules(tree,image,diagnostic_candidates=[candidate],diagnostic_symbols={'_g':0x1900})
            self.assertEqual(rst.read_text(),raw)
            rst.write_text(raw.replace('?ASlink-Warning-2K Page relocation error\n',
                '?ASlink-Warning-2K Page relocation error\n'*2))
            with self.assertRaisesRegex(ValueError,'Unexpected diagnostic'):
                short.modules(tree,image,diagnostic_candidates=[candidate],diagnostic_symbols={'_g':0x1100})
            rst.write_text(raw)
            with self.assertRaisesRegex(ValueError,'source hash'):
                short.modules(tree,image,diagnostic_candidates=[{**candidate,'source_line_sha256':'bad'}],
                              diagnostic_symbols={'_g':0x1100})
            rst.write_text(raw.replace('Page relocation error','Page relocation error for symbol  _wrong'))
            with self.assertRaisesRegex(ValueError,'marker symbol differs'):
                short.modules(tree,image,diagnostic_candidates=[candidate],diagnostic_symbols={'_g':0x1900})
            rst.write_text(raw.replace('2K Page relocation error','unrelated warning'))
            with self.assertRaisesRegex(ValueError,'unrecognized listing row'):
                short.modules(tree,image,diagnostic_candidates=[candidate],diagnostic_symbols={'_g':0x1900})

    def test_real_aslink_boundary_marker_is_authenticated_and_rejected(self):
        configured=os.environ.get('AK820_SDCC_BIN')
        tools=Path(configured) if configured else Path(__file__).resolve().parents[3]/'toolchains/sdcc-4.6.0/bin'
        if not configured and not (tools/'sdas8051').exists():
            self.skipTest('Pinned SDCC 4.6.0 toolchain unavailable; set AK820_SDCC_BIN')
        for name in ('sdas8051','sdld'):
            self.assertTrue((tools/name).is_file(),'Missing pinned tool: '+name)
            self.assertEqual(short.digest(tools/name),SDCC46_PINS[name],'Wrong pinned tool: '+name)
        with tempfile.TemporaryDirectory() as temporary:
            tree=Path(temporary)
            original='.area CSEG (CODE)\n.globl _g\n; function f\n_f:\n lcall _g\n'
            candidate={'module':'edge.asm','line':5,'function':'f','target':'_g',
                       'kind':'lcall','source_line_sha256':hashlib.sha256(b' lcall _g\n').hexdigest()}
            (tree/'edge.asm').write_text(original.replace('lcall','acall'))
            (tree/'target.asm').write_text('.area TARGET (CODE)\n.globl _g\n_g:\n ret\n')
            for name in ('edge','target'):
                subprocess.run([str(tools/'sdas8051'),'-plosgff',str(tree/(name+'.asm'))],check=True,capture_output=True)
            for site in (0x97fe,0x97ff):
                linked=subprocess.run([str(tools/'sdld'),'-n','-i','-m','-w','-u',
                    '-b',f'CSEG={site:#x}','-b','TARGET=0x9d26',str(tree/'layout'),
                    str(tree/'edge.rel'),str(tree/'target.rel')],capture_output=True,text=True)
                self.assertTrue(short.page_errors_only(linked.stderr+linked.stdout))
                image=short.ihx_bytes(tree/'layout.ihx');rejected=[]
                short.modules(tree,image,diagnostic_candidates=[candidate],
                              diagnostic_symbols={'_g':0x9d26},diagnostic_rejections=rejected)
                self.assertEqual(len(rejected),1)
                self.assertTrue(rejected[0]['encoding_valid'])
                self.assertEqual(rejected[0]['bytes'],'b126')
                with self.assertRaisesRegex(ValueError,'unrecognized listing row'):
                    short.modules(tree,image)

    def test_pc_relative_function_cannot_change_internal_offsets(self):
        name='quantum/test.asm';before=fixture();after=fixture()
        for module in (before,after):
            module.source[2]='\tmovc\ta,@a+pc\n'
            module.instructions[2]=instruction(0x1000,'movc','a,@a+pc',data=b'\x83')
        short.verify({name:before},{name:after},{},{},[])
        after.instructions[3]=instruction(0x1004,'ret','',data=b'\x22')
        with self.assertRaisesRegex(ValueError,'nonuniform'):
            short.verify({name:before},{name:after},{},{},[])

    def test_only_complete_page_diagnostics_may_be_retried(self):
        log=('\n?ASlink-Warning-2K Page relocation error for symbol  _f\n'
             '         file    module    area    offset\n'
             '  Refby  file    module    CSEG    000010\n'
             '  Defin  file    module    CSEG    000020\n')
        self.assertTrue(short.page_errors_only(log))
        for bad in ('',log+'ERROR: memory exhausted\n',log.replace('Defin','Unknown'),
                    '?ASlink-Warning-2K Page relocation error\n'):
            self.assertFalse(short.page_errors_only(bad))

    def test_source_mutation_during_baseline_callback_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);source=root/'input';source.mkdir()
            asm=source/'test.asm';asm.write_text('; original\n')
            def mutate(tree,image,label,allow):
                asm.write_text('; changed during callback\n')
                return 0
            with self.assertRaisesRegex(ValueError,'Immutable'):
                short.prepare(source,root/'work',mutate)

    def test_reversion_uses_immutable_original_and_converges(self):
        # Exercise prepare's control flow with one invalid trial, then an empty
        # selection. The second tree must contain the original LCALL source.
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);source=root/'input';source.mkdir()
            module=fixture();(source/'test.asm').write_text(''.join(module.source))
            candidate=short.select({'quantum/test.asm':module},{})[0][0]
            observed=[]
            def link(tree,image,label,allow):
                image.parent.mkdir(parents=True,exist_ok=True)
                image.write_text(label);image.with_suffix('.map').write_text('')
                observed.append((label,[p.read_text() for p in tree.rglob('*.asm')]))
                return 1 if label=='shortcalls-0' else 0
            with patch.object(short,'ihx_bytes',return_value={0x1000:0x12}),\
                 patch.object(short,'modules',side_effect=lambda *args,**kwargs:
                    (kwargs.get('diagnostic_rejections',[]).extend(
                        [{**candidate,'encoding_valid':True}] if len(observed)==2 else [])
                     or {'quantum/test.asm':module})),\
                 patch.object(short,'code_symbols',return_value={}),\
                 patch.object(short,'select',return_value=([candidate],{})),\
                 patch.object(short,'checks',side_effect=[[{**candidate,'valid':True}],[]]):
                # Reuse the real tree writer with a matching relative path.
                (source/'quantum').mkdir();(source/'test.asm').rename(source/'quantum/test.asm')
                plan=short.prepare(source,root/'work',link)
            self.assertEqual(plan['candidates'],[])
            self.assertEqual(plan['iterations'][0]['encoding_rejected_sites'],[])
            self.assertEqual(len(plan['iterations'][0]['linker_rejected_sites']),1)
            self.assertIn('acall',observed[1][1][0])
            self.assertIn('lcall',observed[2][1][0])
            self.assertEqual(plan['iterations'][-1]['link_exit_code'],0)

if __name__=='__main__':unittest.main()
