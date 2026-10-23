"""Regression for constant-only headers omitted by the RC4 ASM-comment manifest."""
import copy
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'util'))
from ak820_build_inputs import FORMAT, collect_inputs, dependency_paths, input_snapshot, validate_inputs


class BuildInputTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='ak820-build-inputs-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / 'source'
        self.toolchain = self.root / 'toolchain'
        self.build = self.source / '.build/test'
        self.obj = self.build / 'obj_fixture'
        self.obj.mkdir(parents=True)
        self.object_name = '.build/test/obj_fixture/main.rel'
        for name, text in {
            'main.c': '#include "constants.h"\nint answer(void) { return ANSWER; }\n',
            'constants.h': '#define ANSWER 42\n',
            'Makefile': 'fixture:\n',
            'requirements-ak820-build.txt': '',
            'util/build_id.py': '', 'util/vial_generate_definition.py': '',
            'util/ak820_dce.py': '', 'util/build_ak820.py': '', 'util/ak820_build_inputs.py': '',
            'util/ak820_outline_audit.py': '',
            'quantum/effects.inc': 'EFFECT(test)\n',
        }.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        for name in ('bin/sdcc', 'bin/sdcpp', 'bin/sdas8051', 'bin/sdld',
                     'share/sdcc/lib/large/mcs51.lib', 'share/sdcc/include/stdint.h'):
            path = self.toolchain / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'pinned fixture input')
        (self.obj / 'main.d').write_text('main.o: main.c constants.h quantum/effects.inc \\\n ../toolchain/share/sdcc/include/stdint.h\n')
        (self.obj / 'makefiles.txt').write_text('Makefile\n')

    def report(self, before=None):
        if before is None:
            before = input_snapshot(self.source, self.toolchain)
        records, evidence = collect_inputs(self.source, self.toolchain, self.build,
                                          [self.object_name], before)
        self.assertEqual(len(evidence), 2)
        return {'source_manifest_format': FORMAT, 'sources': records}

    def test_constant_only_header_and_inc_and_toolchain_are_bound(self):
        report = self.report()
        names = {(item['origin'], item['path']) for item in report['sources']}
        for item in (('source', 'constants.h'), ('source', 'quantum/effects.inc'),
                     ('source', 'util/ak820_outline_audit.py'),
                     ('toolchain', 'share/sdcc/include/stdint.h'),
                     ('toolchain', 'share/sdcc/lib/large/mcs51.lib')):
            self.assertIn(item, names)
        validate_inputs(report, self.source, self.toolchain)
        (self.source / 'constants.h').write_text('#define ANSWER 43\n')
        with self.assertRaisesRegex(ValueError, 'Source differs.*constants.h'):
            validate_inputs(report, self.source, self.toolchain)

    def test_relevant_edit_during_compile_is_rejected(self):
        before = input_snapshot(self.source, self.toolchain)
        (self.source / 'constants.h').write_text('#define ANSWER 43\n')
        with self.assertRaisesRegex(ValueError, 'changed during compilation'):
            self.report(before)

    def test_missing_dependency_file_does_not_fall_back_to_asm_comments(self):
        (self.obj / 'main.d').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing compiler dependency'):
            self.report()

    def test_relocated_checkout_and_toolchain_keep_identity(self):
        report = self.report()
        moved = self.root / 'moved'
        shutil.copytree(self.source, moved / 'source')
        shutil.copytree(self.toolchain, moved / 'toolchain')
        validate_inputs(report, moved / 'source', moved / 'toolchain')

    def test_manifest_paths_are_portable_and_legacy_windows_paths_validate(self):
        report = self.report()
        self.assertTrue(all('\\' not in item['path'] for item in report['sources']))
        for item in report['sources']:
            item['path'] = item['path'].replace('/', '\\')
        validate_inputs(report, self.source, self.toolchain)

    def test_cross_host_absolute_paths_and_separator_alias_duplicates_rejected(self):
        report = self.report()
        for name in ('C:/constants.h', 'C:constants.h', '\\constants.h',
                     '\\\\server\\share\\constants.h', '..\\outside.h'):
            invalid = copy.deepcopy(report)
            invalid['sources'][0]['path'] = name
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'escapes'):
                validate_inputs(invalid, self.source, self.toolchain)
        nested = next(item for item in report['sources'] if '/' in item['path'])
        alias = dict(nested, path=nested['path'].replace('/', '\\'))
        report['sources'].append(alias)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            validate_inputs(report, self.source, self.toolchain)

    def test_malformed_duplicate_and_escaping_records_are_rejected(self):
        report = self.report()
        for change in ({'path': '../outside.h'}, {'path': str(self.source / 'constants.h')},
                       {'origin': 'unknown'}, {'sha256': 'stale'}):
            invalid = copy.deepcopy(report)
            invalid['sources'][0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_inputs(invalid, self.source, self.toolchain)
        invalid = copy.deepcopy(report)
        invalid['sources'].append(invalid['sources'][0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            validate_inputs(invalid, self.source, self.toolchain)
        with self.assertRaisesRegex(ValueError, 'complete compiler dependency'):
            validate_inputs({'sources': report['sources']}, self.source, self.toolchain)

    def test_escaped_spaces_in_dependency_path(self):
        header = self.source / 'a header.h'
        header.write_text('#define VALUE 1\n')
        depfile = self.obj / 'space.d'
        depfile.write_text('space.o: main.c a\\ header.h\n')
        self.assertEqual(dependency_paths(depfile, self.source), {self.source / 'main.c', header})

    def test_real_sdcc_dependency_generation_includes_macro_header(self):
        sdcc_dir = os.environ.get('AK820_SDCC_BIN')
        if not sdcc_dir:
            self.skipTest('AK820_SDCC_BIN required for the real preprocessor check')
        sdcc = Path(sdcc_dir) / 'sdcc'
        subprocess.run([str(sdcc), '-mmcs51', '-c', '-Wp,-MD,-MF,' + str(self.obj / 'real.d'),
                        str(self.source / 'main.c'), '-o', str(self.obj / 'real.rel')],
                       check=True, capture_output=True, text=True)
        dependencies = dependency_paths(self.obj / 'real.d', self.source)
        self.assertIn(self.source / 'constants.h', dependencies)
        self.assertIn(self.source / 'main.c', dependencies)


if __name__ == '__main__':
    unittest.main()
