"""Runtime logs remain outside a frozen Linux/Windows application directory."""
import os
import tempfile
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import ak820


class RuntimePaths(unittest.TestCase):
    def test_source_runs_stay_in_workspace(self):
        self.assertEqual(ak820.runs_directory(False), ak820.ROOT / 'host/runs')

    def test_linux_uses_state_directory(self):
        with patch.object(sys, 'platform', 'linux'), patch.dict(os.environ, {'XDG_STATE_HOME': '/tmp/ak820-state'}):
            self.assertEqual(ak820.runs_directory(True), Path('/tmp/ak820-state/ak820/runs'))
        with patch.object(sys, 'platform', 'linux'), patch.dict(os.environ, {'XDG_STATE_HOME': ''}):
            self.assertEqual(ak820.runs_directory(True), Path.home() / '.local/state/ak820/runs')

    def test_windows_retains_local_appdata(self):
        with patch.object(sys, 'platform', 'win32'), patch.dict(os.environ, {'LOCALAPPDATA': '/tmp/ak820-appdata'}):
            self.assertEqual(ak820.runs_directory(True), Path('/tmp/ak820-appdata/AK820/runs'))

    def test_frozen_udev_uses_collected_rule_without_usb(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            rule = root / 'tools/installer/70-ak820.rules'
            rule.parent.mkdir(parents=True)
            rule.write_text('mock rule')
            with patch.object(ak820, 'ROOT', root), patch.object(ak820, '__file__', str(root / 'ak820.py')), \
                    patch.object(sys, 'platform', 'linux'), patch.object(os, 'geteuid', return_value=1000), \
                    patch.object(ak820.subprocess, 'run') as run:
                ak820.udev(True)
            self.assertEqual(run.call_args_list[0].args[0], ['sudo', 'install', '-m', '0644', str(rule), '/etc/udev/rules.d/70-ak820.rules'])
            self.assertEqual(len(run.call_args_list), 3)
