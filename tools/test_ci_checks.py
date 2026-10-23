from pathlib import Path
import tempfile
import unittest

import ci_checks


class SyntaxCheckTests(unittest.TestCase):
    def test_python_syntax_reports_invalid_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'broken.py'
            source.write_text('def broken(:\n', encoding='utf-8')
            errors = ci_checks.check_python([source], root)
        self.assertEqual(len(errors), 1)
        self.assertIn('broken.py', errors[0])

    def test_python_compile_rules_reject_invalid_module_statements(self):
        invalid_sources = (
            'return 1\n',
            'break\n',
            'nonlocal value\n',
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index, source_text in enumerate(invalid_sources):
                with self.subTest(source=source_text.strip()):
                    source = root / f'invalid_{index}.py'
                    source.write_text(source_text, encoding='utf-8')
                    self.assertEqual(len(ci_checks.check_python([source], root)), 1)

    def test_python_syntax_accepts_valid_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'valid.py'
            source.write_text('value = 42\n', encoding='utf-8')
            self.assertEqual(ci_checks.check_python([source], root), [])

    def test_shell_syntax_reports_invalid_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'broken.sh'
            source.write_text('if true; then\n', encoding='utf-8')
            errors = ci_checks.check_shell([source], root)
        self.assertEqual(len(errors), 1)
        self.assertIn('broken.sh', errors[0])


if __name__ == '__main__':
    unittest.main()
