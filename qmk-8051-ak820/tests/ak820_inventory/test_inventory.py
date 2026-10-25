import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('inventory', Path(__file__).resolve().parents[2]/'util/ak820_linked_inventory.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class InventoryTests(unittest.TestCase):
    def test_explicit_stage_selection(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            contents = {'final/a.ihx': ':0101000022DC\n:00000001FF\n',
                        'final/a.map': 'CSEG 00000100 00000001 = 1. bytes (CODE)\n',
                        'final/dce/reachability.json': '{}',
                        'final/dce/a.rst': '                                      1 \t.area CSEG (CODE)\n'
                            '      000100 22               [24]    2 \tret\n',
                        'proof/a.ihx': 'retained proof',
                        'proof/a.map': 'retained map',
                        'proof/dce/reachability.json': '{}',
                        'proof/dce/a.rst': 'not a final listing'}
            for name, content in contents.items():
                path = root/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            report = {'artifacts': [{'path': name, 'size': (root/name).stat().st_size,
                                     'sha256': m.digest(root/name)} for name in contents],
                      'code_bytes': 1, 'code_min': 256, 'code_max_inclusive': 256,
                      'code_windows': [[256,512],[0,32]], 'code_window': [256,512],
                      'code_main_bytes': 1, 'code_low_bytes': 0}
            report_path = root/'report.json'
            report_path.write_text(json.dumps(report))
            selected = dict(ihx='final/a.ihx', map_file='final/a.map',
                            reachability='final/dce/reachability.json')
            with self.assertRaisesRegex(ValueError, 'exactly one .ihx'):
                m.inventory(root, report_path)
            result = m.inventory(root, report_path, **selected)
            self.assertEqual(result['validated_listing_instruction_bytes'], 1)
            self.assertEqual([e['path'] for e in result['listing_evidence']], ['final/dce/a.rst'])
            for bad in ('../outside.ihx', 'final/../final/a.ihx', 'missing.ihx'):
                with self.assertRaisesRegex(ValueError, 'report artifact'):
                    m.inventory(root, report_path, **dict(selected, ihx=bad))
            with self.assertRaisesRegex(ValueError, 'requires'):
                m.inventory(root, report_path, ihx='final/a.ihx')
            extra = root/'final/dce/unrecorded.rst'
            extra.write_text('')
            with self.assertRaisesRegex(ValueError, 'unrecorded listing'):
                m.inventory(root, report_path, **selected)
            extra.unlink()
            # Legacy manifests with a unique image keep the original invocation.
            legacy = dict(report, artifacts=[e for e in report['artifacts']
                                            if e['path'].startswith('final/')])
            report_path.write_text(json.dumps(legacy))
            self.assertEqual(m.inventory(root, report_path)['occupied_bytes'], 1)
            report_path.write_text(json.dumps(report))
            (root/'proof/a.ihx').write_text('changed proof')
            with self.assertRaisesRegex(ValueError, 'identity mismatch'):
                m.inventory(root, report_path, **selected)

    def test_page_uses_short_instruction_pc(self):
        self.assertFalse(m.page_eligible(0x7fd,0x800))
        self.assertTrue(m.page_eligible(0x7fe,0x800))
        self.assertFalse(m.page_eligible(0x7fe,0x7ff))
        self.assertTrue(m.page_eligible(0xfffe,0))

    def test_windows_recomputed_from_image(self):
        report={'code_windows':[[0x100,0x200],[0x20,0x40]],'code_window':[0x100,0x200],
                'code_main_bytes':1,'code_low_bytes':1}
        image={0x100:0,0x20:0}
        self.assertEqual(m.validate_windows(report,image),[1,1])
        for key in ('code_main_bytes','code_low_bytes'):
            wrong=dict(report,**{key:2})
            with self.assertRaisesRegex(ValueError,'totals mismatch'):m.validate_windows(wrong,image)
        with self.assertRaisesRegex(ValueError,'outside'):m.validate_windows(report,{**image,0x50:0})
        with self.assertRaisesRegex(ValueError,'overlapping'):
            m.validate_windows(dict(report,code_windows=[[0x100,0x200],[0x100,0x150]]),image)

    def test_artifact_escape_and_normalized_alias(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);artifact=root/'a.ihx';artifact.write_bytes(b'original')
            record={'path':'a.ihx','size':8,'sha256':m.digest(artifact)}
            report=root/'build-report.json'
            for path in ('../outside','nested/../a.ihx'):
                report.write_text(json.dumps({'artifacts':[record,dict(record,path=path)]}))
                with self.assertRaisesRegex(ValueError,'escape or duplicate'):m.inventory(root,report)

    def test_nontransfer_instruction_length(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.rst'
            p.write_text('                                      1 \t.area CSEG (CODE)\n'
                         '      000100 75 80            [24]    2 \tmov _P0,#0x01\n')
            with self.assertRaisesRegex(ValueError,'instruction length'):
                m.listing(p,{256:0x75,257:0x80,258:1},'a.asm')
        self.assertEqual(len(m.OPCODE_LENGTHS),256)
        self.assertEqual(m.OPCODE_LENGTHS[0xA5],0)

    def test_bad_hex(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.ihx'
            for content in (':0100000022DE\n:00000001FF\n', ':0100000022DD\n', ':00000001FF\n:00000001FF\n'):
                p.write_text(content)
                with self.assertRaises(ValueError):m.ihx_bytes(p)

    def test_listing_identity_and_local_names(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.rst'
            p.write_text('                                      1 \t.area CSEG (CODE)\n'
                         '      000100                          2 _local:\n'
                         '      000100 22               [24]    3 \tret\n')
            rows, labels=m.listing(p,{256:34},'a.asm')
            self.assertEqual(rows[0]['function'],'a.asm:_local')
            rows2,_=m.listing(p,{256:34},'b.asm')
            self.assertNotEqual(rows[0]['function'],rows2[0]['function'])
            with self.assertRaisesRegex(ValueError,'mismatch'):m.listing(p,{256:0},'a.asm')
            p.write_text('                                      1 \t.area CONST (CODE)\n')
            self.assertEqual(m.listing(p,{256:34},'a.asm'),([],{}))
            p.write_text('nonsense\n')
            with self.assertRaises(ValueError):m.listing(p,{256:34},'a.asm')

    def test_replaced_artifact_rejected_before_analysis(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); artifact=root/'a.ihx';artifact.write_bytes(b'replaced')
            report=root/'build-report.json'
            report.write_text(json.dumps({'artifacts':[{'path':'a.ihx','size':8,'sha256':hashlib.sha256(b'original').hexdigest()}]}))
            with self.assertRaisesRegex(ValueError,'identity mismatch'):m.inventory(root,report)


if __name__=='__main__':unittest.main()
