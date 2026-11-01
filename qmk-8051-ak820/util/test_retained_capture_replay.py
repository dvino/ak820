"""Offline replay of the retained capture and dependency file."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ak820_build_inputs import dependency_paths, digest
from ak820_capture_compile import main


class RetainedCaptureReplay(unittest.TestCase):
    def test_actual_capture_and_dependency_bytes(self):
        source = Path(__file__).resolve().parents[1] / 'tests/ak820_package/fixtures/retained-nested'
        relbuild = Path('.build/pointer-qualification-o0SOART8/bootstrap/pointer')
        relobj = relbuild / 'obj_ajazz_ak820_vial'
        relrecord = relobj / relobj / 'src/default_keyboard.o.compile.json'
        record = source / 'default_keyboard.o.compile.json'
        dep = source / 'default_keyboard.d'
        self.assertEqual(digest(record), 'dc544e87a2b7a5b4cc71d616e837272ccfb22559e7c1fbd9a13f1d3f613d8a59')
        self.assertEqual(digest(dep), 'eb5ed59ea951f0ac45700cfdd942cccf6651dac85a26fef5a0a9d96f584d2070')
        old = json.loads(record.read_text())
        self.assertEqual(old['generated_inputs'], {})
        contents = dep.read_bytes()
        names = shlex.split(contents.decode().replace('\\\n', ' ').partition(':')[2])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in names:
                path = Path(name)
                if not path.is_absolute():
                    destination = root / path
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    if path.is_relative_to(relobj):
                        shutil.copyfile(source / path.name, destination)
                    else:
                        destination.write_text('offline unavailable source header')
                elif path.is_relative_to('/toolchain'):
                    destination = root / 'toolchain' / path.relative_to('/toolchain')
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text('offline unavailable system header')
                else:
                    raise AssertionError('Unexpected absolute dependency: ' + name)
            # The historical container /toolchain is absent; remap those paths only.
            contents = contents.replace(b'/toolchain/', (str(root / 'toolchain') + '/').encode())
            output = root / relrecord
            output.parent.mkdir(parents=True, exist_ok=True)
            build, obj = root / relbuild, root / relobj
            original_cwd = Path.cwd()
            try:
                os.chdir(root)
                environment = {'AK820_CAPTURE_BUILD_ROOT': str(build), 'AK820_CAPTURE_OBJECT_ROOT': str(obj)}
                def compiler(*args, **kwargs):
                    (root / old['fresh_dependency']).write_bytes(contents)
                    return subprocess.CompletedProcess(old['argv'], 0)
                with patch.dict(os.environ, environment), patch('ak820_capture_compile.subprocess.run', side_effect=compiler):
                    self.assertEqual(main([str(relrecord), str(relbuild), str(relobj), '--'] + old['argv']), 0)
                result = json.loads(output.read_text())
                expected = {str(p): digest(p) for p in dependency_paths(root / old['fresh_dependency'], root)
                            if p.is_relative_to(build)}
                self.assertEqual(len(expected), 3)
                self.assertEqual(result['generated_inputs'], expected)
            finally:
                os.chdir(original_cwd)


if __name__ == '__main__':
    unittest.main()
