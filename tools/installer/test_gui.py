"""GUI orchestration tests without a display or HID backend."""
import unittest

from gui import Controller, is_yes_confirmation


class ControllerTests(unittest.TestCase):
    def test_highlight_yes_only_for_exact_backend_confirmation(self):
        self.assertTrue(is_yes_confirmation('Полное объяснение\nSHA256: 123\nВведите yes (Enter — отмена): '))
        self.assertTrue(is_yes_confirmation('Explanation\nSHA256: 123\nType yes (Enter to cancel): '))
        for prompt in ('AK820> ', 'Type ak820', 'yes', 'Введите ready (Enter — отмена): ',
                       'Start preparation? [y/N] '):
            self.assertFalse(is_yes_confirmation(prompt))

    def test_launch_is_idle_and_has_no_implicit_runner(self):
        calls = []
        controller = Controller(lambda *a, **k: calls.append(a))
        self.assertFalse(controller.busy)
        self.assertTrue(controller.events.empty())
        self.assertEqual(calls, [])

    def test_explicit_response_and_busy_lock(self):
        def runner(args, *, prompt, interactive, progress, cancel_event):
            if not interactive:
                raise AssertionError('GUI must identify its interactive prompts')
            answer = prompt('Start preparation? [y/N] ')
            return 2 if answer == '' else 0
        controller = Controller(runner, language='en')
        self.assertTrue(controller.start(['install']))
        kind, message = controller.events.get(timeout=5)
        self.assertEqual(kind, 'prompt')
        self.assertIn('[y/N]', message)
        self.assertFalse(controller.start(['install']))
        controller.respond('')
        self.assertEqual(controller.events.get(timeout=5), ('finished', 2))
        controller.finished()
        self.assertFalse(controller.busy)

    def test_wait_cancel_exits_worker_without_write(self):
        writes = []
        def runner(args, *, prompt, interactive, progress, cancel_event):
            progress('loader_wait', 'instructions')
            if cancel_event.wait(5):
                return 2
            writes.append('unexpected write')
            return 1
        controller = Controller(runner, language='en')
        controller.start(['update-prepared'])
        self.assertEqual(controller.events.get(timeout=5), ('progress', ('loader_wait', 'instructions')))
        controller.cancel_wait()
        self.assertEqual(controller.events.get(timeout=5), ('finished', 2))
        controller.worker.join(5)
        self.assertFalse(controller.worker.is_alive())
        self.assertEqual(writes, [])

    def test_error_is_reported_and_finishes(self):
        def runner(*args, **kwargs):
            raise OSError('offline fake failure')
        controller = Controller(runner)
        controller.start(['verify'])
        self.assertEqual(controller.events.get(timeout=5), ('output', '\nStopped: offline fake failure\n'))
        self.assertEqual(controller.events.get(timeout=5), ('finished', 1))


if __name__ == '__main__':
    unittest.main()
