"""Offline adversarial fixtures and replay of saved GitHub API metadata."""
import copy
import importlib.util
import json
import io
import subprocess
from pathlib import Path
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('reuse', HERE / 'validate-qualified-reuse.py')
reuse = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reuse)


class Contract(unittest.TestCase):
    def setUp(self):
        self.run = json.loads((HERE / 'run.json').read_text())
        self.jobs = json.loads((HERE / 'jobs.json').read_text())['jobs']
        self.artifacts = json.loads((HERE / 'artifacts.json').read_text())['artifacts']
        self.workflow = json.loads((HERE / 'workflow.json').read_text())

    def validate(self):
        return reuse.validate_metadata(self.run, self.jobs, self.artifacts,
                                       'dvino/ak820', '40258163824', self.workflow['id'])

    def test_real_metadata(self):
        self.assertEqual(self.validate(), 'cd36cf446c1bae8070ee8f61750df550ea53230d')

    def test_each_failed_job(self):
        for profile in reuse.PROFILES:
            with self.subTest(profile=profile):
                saved = copy.deepcopy(self.jobs)
                next(j for j in self.jobs if j['name'] == f'Qualify firmware ({profile})')['conclusion'] = 'failure'
                with self.assertRaises(SystemExit):
                    self.validate()
                self.jobs = saved

    def test_missing_duplicate_and_expired_artifact(self):
        selected = [a for a in self.artifacts if a['name'].startswith('ak820-qualified-profile-')]
        for artifacts in [selected[:-1], selected + [selected[0]],
                          [dict(a, expired=True) for a in selected],
                          selected[:-1] + [dict(selected[-1], name='ak820-qualified-profile-unknown')]]:
            self.artifacts = artifacts
            with self.assertRaises(SystemExit):
                self.validate()

    def test_repository_workflow_and_run_identity(self):
        for field, bad in [('repository', {'full_name': 'other/ak820'}),
                           ('head_repository', {'full_name': 'other/ak820'}),
                           ('workflow_id', -1), ('path', '.github/workflows/other.yml'),
                           ('status', 'in_progress'), ('id', 1), ('head_sha', 'bad')]:
            with self.subTest(field=field):
                saved = self.run[field]
                self.run[field] = bad
                with self.assertRaises(SystemExit):
                    self.validate()
                self.run[field] = saved

    def test_latest_job_missing_duplicate(self):
        job = next(j for j in self.jobs if j['name'] == 'Qualify firmware (main)')
        self.jobs.remove(job)
        with self.assertRaises(SystemExit):
            self.validate()
        self.jobs += [job, job]
        with self.assertRaises(SystemExit):
            self.validate()

    def test_source_allowlist(self):
        for path in ['tools/build_ci_release.py', 'tools/installer/profile-catalog.json',
                     'qmk-8051-ak820/keyboards/ajazz/ak820/ak820.c', '.github/workflows/other.yml',
                     'ci/profiles/main/config.h', 'ci/profiles/unknown/release-policy.json']:
            self.assertFalse(reuse.allowed_path(path), path)
        for path in ['README.md', 'docs/STATUS.md', 'docs/ru/STATUS.md',
                     'audits/example.json', reuse.WORKFLOW, 'ci/beta2-release-notes.md']:
            self.assertTrue(reuse.allowed_path(path), path)
        for profile in reuse.PROFILES:
            for name in ['release-policy.json', 'program-review.md', 'release-safety.json', 'packing-validation.json']:
                self.assertTrue(reuse.allowed_path(f'ci/profiles/{profile}/{name}'))

    def test_input_and_tag_guards_before_api(self):
        base = {'QUALIFIED_RUN_ID': '40258163824', 'EVENT_NAME': 'workflow_dispatch', 'REF': 'refs/tags/v0.6.0-beta.2'}
        for change in [{'QUALIFIED_RUN_ID': '123; bad'}, {'QUALIFIED_RUN_ID': ''},
                       {'QUALIFIED_RUN_ID': '-1'}, {'EVENT_NAME': 'push'}, {'REF': 'refs/heads/main'}]:
            with patch.dict(reuse.os.environ, base | change, clear=True):
                with self.assertRaises(SystemExit):
                    reuse.main()

    def test_full_source_gate(self):
        env = {'QUALIFIED_RUN_ID': '40258163824', 'EVENT_NAME': 'workflow_dispatch',
               'REF': 'refs/tags/v0.6.0-beta.2', 'GITHUB_REPOSITORY': 'dvino/ak820',
               'GITHUB_API_URL': 'https://api.github.com', 'GH_TOKEN': 'fixture',
               'GITHUB_SHA': '1' * 40}

        def response(request, timeout):
            url = request.full_url
            data = self.workflow if '/workflows/' in url else self.run
            if '/jobs?' in url:
                data = {'jobs': self.jobs}
            if '/artifacts?' in url:
                data = {'artifacts': self.artifacts}
            return io.BytesIO(json.dumps(data).encode())

        for changed, ancestry_ok, accepted in [
                (b'docs/STATUS.md\0', True, True),
                (b'tools/build_ci_release.py\0', True, False),
                (b'qmk-8051-ak820/config.h\0', True, False),
                (b'docs/STATUS.md\0', False, False)]:
            with self.subTest(changed=changed, ancestry_ok=ancestry_ok):
                with patch.dict(reuse.os.environ, env, clear=True), \
                     patch.object(reuse.urllib.request, 'urlopen', side_effect=response), \
                     patch.object(reuse.subprocess, 'check_output', side_effect=['1' * 40 + '\n', changed]), \
                     patch.object(reuse.subprocess, 'run', side_effect=None if ancestry_ok else subprocess.CalledProcessError(1, 'git')):
                    if accepted:
                        reuse.main()
                    else:
                        with self.assertRaises((SystemExit, subprocess.CalledProcessError)):
                            reuse.main()

    def test_inline_copy_exact_and_gates(self):
        workflow = (ROOT / '.github/workflows/windows-installer.yml').read_text()
        marker = "          python - <<'PYTHON'\n"
        start = workflow.index(marker, workflow.index('name: Validate prior qualification')) + len(marker)
        end = workflow.index('          PYTHON\n', start)
        inline = ''.join(line[10:] + '\n' for line in workflow[start:end].splitlines())
        self.assertEqual(inline, (HERE / 'validate-qualified-reuse.py').read_text())
        self.assertIn("needs.linux-regression.result == 'success'", workflow)
        self.assertIn("needs.linux-profile.result == 'skipped' && github.event_name == 'workflow_dispatch'", workflow)
        self.assertIn("if: startsWith(github.ref, 'refs/tags/v') && (github.event_name == 'push' || (github.event_name == 'workflow_dispatch' && inputs.qualified_run_id != ''))", workflow)
        self.assertLess(workflow.index('name: Validate prior qualification'), workflow.index('pattern: ak820-qualified-profile-*'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
