import unittest

from release_version import release_values


class ReleaseVersionTests(unittest.TestCase):
    def test_stable_and_prerelease_with_build_metadata(self):
        for tag, expected in [('v0.6.0', False), ('v1.2.3+build.01', False),
                              ('v0.6.0-rc.1', True), ('v1.2.3-0+build.01', True),
                              ('v1.2.3-01a', True), ('v1.2.3-alpha-beta', True)]:
            with self.subTest(tag=tag):
                self.assertEqual(release_values(tag), {'tag': tag, 'prerelease': expected})

    def test_invalid_tags_cannot_be_published(self):
        for tag in ['v01.2.3', 'v1.02.3', 'v1.2.03', 'v1.2.3-rc.',
                    'v1.2.3-01', 'v1.2.3+foo.', 'v1.2.3-', 'v1.2.3+',
                    'v1.2', '1.2.3', 'v1.2.3\n', 'v1.2.3;echo injected']:
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                release_values(tag)


if __name__ == '__main__':
    unittest.main()
