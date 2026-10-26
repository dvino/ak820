"""Wrapper routing and worker-boundary checks; no firmware build or device I/O."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import ci_parallel_assembly as wrapper


def entry():
    return ('a' * 64, {'contract': 'ak820-audited-pass30-1', 'reports': {
        name: 'b' * 64 for name in ('parameter_spills', 'register_saves', 'tail_share')}})


class ParallelAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.saved = dict(wrapper.configured._PASS30_CACHE)
        wrapper.configured._PASS30_CACHE.clear()
        self.key = (Path('/build/main'), Path('/tools'))

    def tearDown(self):
        wrapper.configured._PASS30_CACHE.clear()
        wrapper.configured._PASS30_CACHE.update(self.saved)

    def test_accept_only_requested_success_and_deepcopy(self):
        value = entry()
        wrapper._accept(self.key, (self.key, value))
        value[1]['reports']['tail_share'] = 'c' * 64
        self.assertEqual(wrapper.configured._PASS30_CACHE[self.key][1]['reports']['tail_share'], 'b' * 64)
        for result in ((('/wrong', '/tools'), entry()), (self.key, ('x', entry()[1])),
                       (self.key, ('a' * 64, {'contract': 'anything', 'reports': {}}))):
            with self.subTest(result=result), self.assertRaises(ValueError):
                wrapper._accept(self.key, result)
        wrapper._accept(self.key, (self.key, None))
        self.assertNotIn(self.key, wrapper.configured._PASS30_CACHE)

    def test_worker_clears_prior_cache_and_inspects(self):
        wrapper.configured._PASS30_CACHE[self.key] = entry()
        def inspect(*key):
            self.assertNotIn(self.key, wrapper.configured._PASS30_CACHE)
            wrapper.configured._PASS30_CACHE[key] = entry()
        with patch.object(wrapper.configured, 'inspect', side_effect=inspect) as checked:
            self.assertEqual(wrapper._prewarm(self.key), (self.key, entry()))
        checked.assert_called_once_with(*self.key)

    def test_parallel_forwarding_and_spawn(self):
        calls = []
        class Future:
            def __init__(self, key): self.key = key
            def result(self): return self.key, entry()
        class Pool:
            def __init__(self, **kwargs): calls.append(kwargs)
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def submit(self, function, key):
                if function is not wrapper._prewarm:
                    raise AssertionError('unexpected worker')
                return Future(key)
        args = ['--all-profiles', '--builds-root', 'builds', '--source-commit', 'abc',
                '--output', 'out', '--validation-workers', '3', '--unknown-original-option']
        with patch.object(wrapper, 'ProcessPoolExecutor', Pool), \
             patch.object(wrapper.ci, 'release_profile_names', return_value=('main', 'game')), \
             patch.object(wrapper.ci, 'main', side_effect=lambda: list(sys.argv[1:])):
            result = wrapper.main(args)
        self.assertEqual(result, args[:7] + args[9:])
        self.assertEqual(calls[0]['max_workers'], 3)
        self.assertEqual(calls[0]['mp_context'].get_start_method(), 'spawn')
        self.assertEqual(len(wrapper.configured._PASS30_CACHE), 2)

    def test_failure_does_not_assemble(self):
        class Future:
            def result(self): raise RuntimeError('cold validation failed')
        class Pool:
            def __init__(self, **kwargs): pass
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def submit(self, *args): return Future()
        with patch.object(wrapper, 'ProcessPoolExecutor', Pool), \
             patch.object(wrapper.ci, 'release_profile_names', return_value=('main',)), \
             patch.object(wrapper.ci, 'main') as original:
            with self.assertRaisesRegex(RuntimeError, 'cold validation failed'):
                wrapper.main(['--all-profiles', '--builds-root', 'builds'])
            original.assert_not_called()

    def test_serial_and_help_never_spawn(self):
        with patch.object(wrapper, 'ProcessPoolExecutor', side_effect=AssertionError('spawn')), \
             patch.object(wrapper.ci, 'release_profile_names', return_value=('main',)), \
             patch.object(wrapper, '_prewarm', side_effect=lambda key: (key, None)) as warm, \
             patch.object(wrapper.ci, 'main', return_value=42) as original:
            self.assertEqual(wrapper.main(['--all-profiles', '--builds-root', 'builds',
                                           '--validation-workers=1']), 42)
            warm.assert_called_once()
            warm.reset_mock()
            with patch.object(wrapper.argparse.ArgumentParser, 'print_help'):
                self.assertEqual(wrapper.main(['--help']), 42)
            warm.assert_not_called()
            self.assertEqual(original.call_count, 2)

    def test_reject_worker_range_and_single_profile(self):
        with patch.object(wrapper.ci, 'main') as original:
            for args in (['--validation-workers=0'], ['--validation-workers=5'],
                         ['--validation-workers=x'], ['--build-dir=build']):
                with self.subTest(args=args), self.assertRaises(SystemExit):
                    wrapper.main(args)
            original.assert_not_called()

    def test_parent_rechecks_snapshot_before_cache_hit(self):
        wrapper._accept(self.key, (self.key, entry()))
        with patch.object(wrapper.configured, '_pass30_snapshot', return_value='a' * 64), \
             patch.object(wrapper.configured, '_replay_pass30') as replay:
            self.assertEqual(wrapper.configured.check_pass30({}, *self.key), entry()[1])
            replay.assert_not_called()
        changed = entry()[1]
        with patch.object(wrapper.configured, '_pass30_snapshot', return_value='c' * 64), \
             patch.object(wrapper.configured, '_replay_pass30', return_value=changed) as replay:
            self.assertEqual(wrapper.configured.check_pass30({}, *self.key), changed)
            replay.assert_called_once_with({}, *self.key)
        self.assertEqual(wrapper.configured._PASS30_CACHE[self.key][0], 'c' * 64)


if __name__ == '__main__':
    unittest.main()
