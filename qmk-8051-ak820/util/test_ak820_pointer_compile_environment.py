import unittest
from pathlib import Path
from unittest.mock import patch

from ak820_pointer_compile_environment import validate_pointer_environment


class PointerEnvironmentTest(unittest.TestCase):
    def test_recorded_path_and_mutations(self):
        root = Path('/workspace/qmk')
        build = root / '.build/pointer'
        toolchain = Path('/tools/sdcc')
        qmk = Path('/tools/qmk/bin/qmk')
        environment = {'PATH': '/tools/sdcc/bin:/tools/qmk/bin:/usr/local/bin:/usr/bin:/bin',
                       'AK820_CAPTURE_BUILD_ROOT': str(build),
                       'AK820_CAPTURE_OBJECT_ROOT': str(build / 'obj_ajazz_ak820_vial')}
        validate_pointer_environment(environment, root, build, toolchain, qmk)
        spaced_build = Path('/workspace/my qmk/.build/pointer')
        validate_pointer_environment({**environment, 'PATH': environment['PATH'] + ':/extra tools/bin',
                                      'AK820_CAPTURE_BUILD_ROOT': str(spaced_build),
                                      'AK820_CAPTURE_OBJECT_ROOT': str(spaced_build / 'obj_ajazz_ak820_vial')},
                                     Path('/workspace/my qmk'), spaced_build, toolchain, qmk)
        for bad in ({}, {**environment, 'PATH': '/tmp/bin:' + environment['PATH']},
                    {**environment, 'AK820_CAPTURE_BUILD_ROOT': str(root)},
                    {**environment, 'AK820_CAPTURE_OBJECT_ROOT': str(build)},
                    {**environment, 'CPATH': '/tmp'}, {**environment, 'SYSTEMROOT': '/tmp'}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                validate_pointer_environment(bad, root, build, toolchain, qmk)
        with self.assertRaises(ValueError):
            validate_pointer_environment(environment, root, Path('/outside'), toolchain, qmk)
        with self.assertRaises(ValueError):
            validate_pointer_environment(environment, root, root / '.build/bad name', toolchain, qmk)
        with patch('ak820_pointer_compile_environment.sys.platform', 'win32'):
            with self.assertRaisesRegex(ValueError, 'Linux only'):
                validate_pointer_environment(environment, root, build, toolchain, qmk)


if __name__ == '__main__':
    unittest.main()
