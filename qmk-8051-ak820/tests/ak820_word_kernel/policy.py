#!/usr/bin/env python3
"""Exercise the actual builder's register-preserving word-hook policy."""
import ast
from pathlib import Path
import shlex
import unittest

builder = Path(__file__).resolve().parents[2] / 'util/build_ak820.py'
tree = ast.parse(builder.read_text())
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'word_hook_abi_flag')
namespace = {'shlex': shlex}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(builder), 'exec'), namespace)
policy = namespace['word_hook_abi_flag']
HOOKS = ('eeprom_read_byte', 'eeprom_update_byte')
APIS = ('dynamic_keymap_get_keycode', 'dynamic_keymap_set_keycode',
        'dynamic_keymap_get_encoder', 'dynamic_keymap_set_encoder')


class WordPolicy(unittest.TestCase):
    def test_assertion_requires_both_audited_hooks(self):
        self.assertEqual(policy(HOOKS, '--opt-code-size'), ' -DAK820_WORD_HOOKS_PRESERVE_RN=1')
        for hooks in ((), HOOKS[:1], HOOKS[1:]):
            self.assertEqual(policy(hooks, '--opt-code-size'), '')

    def test_incompatible_abi_and_manual_assertion_reject(self):
        for flags in ('--stack-auto', '--xstack', '--parms-in-bank1', '--all-callee-saves',
                      '--sdcccall 1', '--sdcccall=1', '-DAK820_WORD_HOOKS_PRESERVE_RN=1',
                      '-D AK820_WORD_HOOKS_PRESERVE_RN=1'):
            with self.subTest(flags=flags), self.assertRaises(ValueError):
                policy(HOOKS, flags)

    def test_public_entries_remain_caller_clobbered(self):
        for api in APIS:
            for flags in ('--callee-saves '+api, '--callee-saves='+api, '--callee-saves _'+api):
                with self.subTest(flags=flags), self.assertRaises(ValueError):
                    policy(HOOKS, flags)
            with self.subTest(audited=api), self.assertRaises(ValueError):
                policy((*HOOKS, api), '')


if __name__ == '__main__':
    unittest.main()
