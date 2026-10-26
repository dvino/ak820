"""Synthetic offline authorization consistency checks; no USB or firmware build."""
import json
from pathlib import Path, PureWindowsPath
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'qmk-8051-ak820/util'))
import ak820_ci_authorization as auth
import ak820_profiles
import pack_ak820 as pack
from ak820_release_manifest import read_review_record


def raw(item):
    return (json.dumps(item, sort_keys=True) + '\n').encode()


def markdown(item):
    return b'Independent review evidence\n```json\n' + raw(item) + b'```\n'


def full_qualification_tests(hashes):
    root = '/ci/project'
    py = '/usr/bin/python3'
    commands = []
    for directory, pattern in (
        ('tools/installer', 'test_*.py'), ('tools', 'test_build_release_bundle.py'),
        ('tools', 'test_build_windows_installer.py'), ('tools', 'test_keyboard_runner.py'),
        ('tools', 'test_ak820_device_tests.py'), ('tools', 'test_ak820_device_protocol.py'),
        ('qmk-8051-ak820/tests/ak820_package', 'test_*.py'),
        ('qmk-8051-ak820/tests/ak820_inventory', 'test_*.py')):
        commands.append((root, [py,'-B','-m','unittest','discover','-s',directory,'-p',pattern], 1))
    commands.append((root, [py,'tools/check_docs.py'],0))
    for name in ('ak820_usb','ak820_keymap','ak820_caps_word','ak820_macro_guard',
                 'ak820_diagnostic','ak820_optimization','ak820_rgb','ak820_via_decode','ak820_bounded','ak820_combo'):
        commands.append((root+'/qmk-8051-ak820', [py,'tests/'+name+'/run.py'],0))
    commands.append((root+'/qmk-8051-ak820', [py,'tests/ak820_tapping/run.py','--negative-controls',
                     '--output','/ci/logs/tapping-host.json'],0))
    for script in ('ak820_features/run.py','ak820_unlock/run.py','ak820_tri_layer/run.py',
                   'ak820_iap/run.py','ak820_rgb/emitted.py','ak820_bounded/emitted.py','ak820_tapping/emitted.py','ak820_combo/emitted.py'):
        command=[py,'tests/'+script,'--build-dir',root+'/qmk-8051-ak820/.build/candidate',
                 '--s51','/ci/sdcc/bin/s51','--output-dir','/ci/logs/'+script.split('/')[0]]
        if script=='ak820_iap/run.py': command+=['--iap-fault-profile','guarded-erase']
        commands.append((root+'/qmk-8051-ak820',command,0))
    return [dict(cwd=cwd,command=command,exit_code=0,unit_tests={'run':count,'skipped':0},
                 build_before=hashes,build_after=hashes) for cwd,command,count in commands]


class AuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.host = {'host.py': {'sha256': 'a' * 64, 'size': 1}}
        self.program = dict(ihx_sha256='a' * 64, symbols_sha256='b' * 64, schema=pack.BUILD_ID,
                            keyboard='ajazz/ak820', keymap='vial', sdcc_version='4.6.0')
        self.receipt = dict(format='ak820-ci-packing-receipt-1', hardware_validated=False,
            host_files=self.host, program={k:self.program[k] for k in ('ihx_sha256','symbols_sha256','schema')},
            packing=dict(physical_usb_opened=False, hardware_validated=False, recovery_byte_equal=True,
                install_modes=['permanent','trial'], images={'ak820-vial-trial.bin':{'trial':True,'build_id':pack.BUILD_ID,'size':51136,'sha256':'c'*64},
                    'restore-native.bin':{'size':51136,'sha256':'d'*64}},
                permanent={'trial':False,'build_id':pack.BUILD_ID,'size':51136,'sha256':'e'*64}))
        self.policy = dict(format='ak820-ci-program-policy-1', program=self.program, host_files=self.host,
                           packing_receipt_sha256=auth.digest(raw(self.receipt)))
        self.review = dict(format='ak820-ci-program-review-1', status='passed', hardware_validated=False,
                           policy_sha256=auth.digest(raw(self.policy)))

    def validate(self):
        auth.validate_policy(self.policy, self.host, raw(self.receipt), markdown(self.review))

    def test_pass(self):
        self.validate()

    def test_extension_schema_receipt_and_mixed_schema_rejected(self):
        self.program['schema'] = pack.EXTENSION_BUILD_ID
        self.receipt['program']['schema'] = pack.EXTENSION_BUILD_ID
        for image in (self.receipt['packing']['images']['ak820-vial-trial.bin'],
                      self.receipt['packing']['permanent']):
            image['build_id'] = pack.EXTENSION_BUILD_ID
        self.policy['packing_receipt_sha256'] = auth.digest(raw(self.receipt))
        self.validate()
        for image in (self.receipt['packing']['images']['ak820-vial-trial.bin'],
                      self.receipt['packing']['permanent']):
            image['build_id'] = pack.BUILD_ID
            self.policy['packing_receipt_sha256'] = auth.digest(raw(self.receipt))
            with self.assertRaisesRegex(ValueError, 'schema differs'):
                self.validate()
            image['build_id'] = pack.EXTENSION_BUILD_ID
        for invalid in (True, pack.EXTENSION_BUILD_ID + 1):
            self.program['schema'] = invalid
            with self.assertRaisesRegex(ValueError, 'Unsupported policy'):
                self.validate()

    def test_corruption(self):
        for mutate in (lambda: self.policy['program'].update(sdcc_version='4.4.0'),
                       lambda: self.policy.update(packing_receipt_sha256='0'*64),
                       lambda: self.review.update(status='pending'),
                       lambda: self.review.update(hardware_validated=True)):
            with self.subTest(mutate=mutate):
                self.setUp(); mutate()
                with self.assertRaises(ValueError): self.validate()

    def test_rehashed_bad_receipt(self):
        for key,value in (('program',{}), ('host_files',{}), ('packing',{})):
            with self.subTest(key=key):
                self.setUp(); self.receipt[key] = value
                self.policy['packing_receipt_sha256'] = auth.digest(raw(self.receipt))
                with self.assertRaises(ValueError): self.validate()

    def test_review_ambiguity(self):
        with self.assertRaises(ValueError):
            auth.validate_policy(self.policy, self.host, raw(self.receipt), markdown(self.review)*2)

    def test_symbols_canonical(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'a.map'
            path.write_text('C: 00008010 foo\nC: 00008020 bar\n')
            first = auth.symbols_sha256(path)
            path.write_text('header\nC: 00008020 bar\nC: 00008010 foo\n')
            self.assertEqual(first, auth.symbols_sha256(path))
            path.write_text('C: 00008011 foo\nC: 00008020 bar\n')
            self.assertNotEqual(first, auth.symbols_sha256(path))

    def test_mixed_format_rejected(self):
        with self.assertRaises(ValueError):
            auth.validate_bundle_authorization(Path('.'), {'files':{next(iter(auth.CI_EXTRA_FILES)): {}}},
                                               {'format':'ak820-offline-review-2'})

    def bundle_fixture(self, folder):
        bundle = Path(folder)
        def write(name, value):
            path = bundle / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)
        for name in ('firmware/application.ihx', 'firmware/application.mem'):
            write(name, b'fixture')
        config = ak820_profiles.configuration('main') if self.program['schema'] == pack.EXTENSION_BUILD_ID else ak820_profiles.legacy_configuration('work')
        write('reports/build-report.json', raw({'build_id': self.program['schema'], 'configuration': config}))
        write('firmware/application.map', b'C: 00008010 foo\n')
        self.program.update(ihx_sha256=auth.digest(b'fixture'),
                            symbols_sha256=auth.symbols_sha256(bundle/'firmware/application.map'))
        self.receipt['program'] = {k:self.program[k] for k in ('ihx_sha256','symbols_sha256','schema')}
        self.policy['packing_receipt_sha256'] = auth.digest(raw(self.receipt))
        self.review['policy_sha256'] = auth.digest(raw(self.policy))
        write('reviews/program-policy.json', raw(self.policy))
        write('reviews/program-review.md', markdown(self.review))
        write('reports/packing-validation.json', raw(self.receipt))
        hashes = {'ihx':auth.digest(b'fixture'), 'map':auth.digest((bundle/'firmware/application.map').read_bytes())}
        qualification = dict(format='ak820-offline-tests-1', passed=True, require_toolchain=True,
            hardware_validated=False, physical_device_commands=0, build_unchanged=True,
            iap_fault_profile='guarded-erase', build_hashes=hashes, unit_tests={'run':8,'skipped':0},
            tools={k:{'sha256':'a'*64,'path':'/ci/sdcc/bin/'+k} for k in ('sdcc','s51')},
            tests=full_qualification_tests(hashes))
        write('reports/qualification.json', raw(qualification))
        attestation = dict(format='ak820-ci-build-attestation-1', source_commit='a'*40,
            build=dict(ihx_sha256=hashes['ihx'],map_sha256=hashes['map'],mem_sha256=auth.digest(b'fixture'),
                       build_report_sha256=auth.digest((bundle/'reports/build-report.json').read_bytes())),
            policy_sha256=auth.digest(raw(self.policy)), program_review_sha256=auth.digest(markdown(self.review)),
            qualification_sha256=auth.digest(raw(qualification)), host_files=self.host, hardware_validated=False)
        write('reports/build-attestation.json', raw(attestation))
        record = dict(format='ak820-reproduced-review-1',policy_sha256=attestation['policy_sha256'],
            program_review_sha256=attestation['program_review_sha256'],attestation_sha256=auth.digest(raw(attestation)))
        manifest = {'files':{name:{} for name in auth.CI_EXTRA_FILES},'host_files':self.host}
        return bundle, manifest, record

    def test_complete_bundle_and_corruptions(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle, manifest, record = self.bundle_fixture(folder)
            auth.validate_bundle_authorization(bundle, manifest, record)
            for name, field, value in (
                ('reports/qualification.json','passed',False),
                ('reports/qualification.json','require_toolchain',False),
                ('reports/qualification.json','build_unchanged',False),
                ('reports/qualification.json','unit_tests',{'run':1,'skipped':1}),
                ('reports/build-attestation.json','source_commit','branch'),
                ('reviews/program-policy.json','host_files',{})):
                with self.subTest(name=name,field=field):
                    path=bundle/name; previous=path.read_bytes()
                    item=json.loads(previous);item[field]=value;path.write_bytes(raw(item))
                    with self.assertRaises(ValueError): auth.validate_bundle_authorization(bundle,manifest,record)
                    path.write_bytes(previous)

    def test_extension_bundle_schema_matches_report_and_receipt(self):
        self.program['schema'] = pack.EXTENSION_BUILD_ID
        self.receipt['program']['schema'] = pack.EXTENSION_BUILD_ID
        self.receipt['packing']['images']['ak820-vial-trial.bin']['build_id'] = pack.EXTENSION_BUILD_ID
        self.receipt['packing']['permanent']['build_id'] = pack.EXTENSION_BUILD_ID
        with tempfile.TemporaryDirectory() as folder:
            bundle, manifest, record = self.bundle_fixture(folder)
            auth.validate_bundle_authorization(bundle, manifest, record)
            report_path = bundle/'reports/build-report.json'
            original = report_path.read_bytes()
            for changed in ({'build_id': pack.BUILD_ID, 'configuration': ak820_profiles.configuration('main')},
                            {'build_id': pack.EXTENSION_BUILD_ID, 'configuration': ak820_profiles.legacy_configuration('work')}):
                report_path.write_bytes(raw(changed))
                with self.assertRaises(ValueError):
                    auth.validate_bundle_authorization(bundle, manifest, record)
            report_path.write_bytes(original)

    def test_linux_report_paths_are_portable_to_windows_installer(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle, _, _ = self.bundle_fixture(folder)
            report=json.loads((bundle/'reports/qualification.json').read_bytes())
            with patch.object(auth, 'Path', PureWindowsPath):
                auth.validate_qualification_contract(report)

    def test_qualification_contract_rejects_each_missing_suite(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle, _, _ = self.bundle_fixture(folder)
            report=json.loads((bundle/'reports/qualification.json').read_bytes())
            self.assertEqual(len(report['tests']),28)
            auth.validate_qualification_contract(report)
            for index in range(28):
                with self.subTest(omitted=index):
                    bad=json.loads(json.dumps(report));del bad['tests'][index]
                    with self.assertRaises(ValueError): auth.validate_qualification_contract(bad)

    def test_qualification_contract_rejects_flags_duplicates_and_counts(self):
        with tempfile.TemporaryDirectory() as folder:
            bundle, _, _ = self.bundle_fixture(folder)
            original=json.loads((bundle/'reports/qualification.json').read_bytes())
            def iap_missing(r):
                row=next(t for t in r['tests'] if 'tests/ak820_iap/run.py' in t['command'])
                row['command']=row['command'][:-2]
            def tapping_controls_missing(r):
                row=next(t for t in r['tests'] if 'tests/ak820_tapping/run.py' in t['command'])
                row['command'].remove('--negative-controls')
            def cpu_tool(r): r['tests'][-1]['command'][5]='/wrong/s51'
            def zero(r): r['tests'][0]['unit_tests']['run']=0;r['unit_tests']['run']-=1
            for mutate in (iap_missing,tapping_controls_missing,cpu_tool,zero,
                           lambda r:r['tests'].append(r['tests'][0]),
                           lambda r:r['unit_tests'].update(run=99),
                           lambda r:r['tests'][0]['command'].append('--extra'),
                           lambda r:r['tests'][-1]['command'].__setitem__(3,'/other/build')):
                with self.subTest(mutation=mutate):
                    bad=json.loads(json.dumps(original));mutate(bad)
                    with self.assertRaises(ValueError): auth.validate_qualification_contract(bad)

    def test_review_format_does_not_allow_two_records(self):
        base = dict(status='passed',hardware_validated=False,release='rc6')
        for fmt in ('ak820-offline-review-2','ak820-reproduced-review-1'):
            record=dict(base,format=fmt)
            self.assertEqual(read_review_record(markdown(record).decode()),record)
        with self.assertRaises(ValueError):
            read_review_record((markdown(dict(base,format='ak820-offline-review-2')) +
                               markdown(dict(base,format='ak820-reproduced-review-1'))).decode())

if __name__ == '__main__':
    unittest.main()
