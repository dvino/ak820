"""Synthetic release-context comparison; no release or device is qualified."""
import unittest
from unittest.mock import patch

import ak820 as app


class SnapshotBinding(unittest.TestCase):
    def test_revalidated_snapshot_compares_all_retained_bytes(self):
        def context(snapshot):
            return app.ReleaseContext('main', '/release', '/approval', {},
                                      nvm_schema=app.packer.EXTENSION_BUILD_ID,
                                      snapshot=snapshot)

        good = app.ReleaseSnapshot(b'{}', {'ihx': b'image'}, {'catalog': b'catalog'}, b'approval')
        actual = context(good)
        cases = (
            app.ReleaseSnapshot(b'{ }', dict(good.files), dict(good.host_files), good.approval_bytes),
            app.ReleaseSnapshot(good.manifest_bytes, {'ihx': b'altered'}, dict(good.host_files), good.approval_bytes),
            app.ReleaseSnapshot(good.manifest_bytes, dict(good.files), {'catalog': b'altered'}, good.approval_bytes),
            app.ReleaseSnapshot(good.manifest_bytes, dict(good.files), dict(good.host_files), b'altered'),
        )
        with patch.object(app, 'release_context', return_value=actual) as fresh:
            copy = app.ReleaseSnapshot(good.manifest_bytes, dict(good.files), dict(good.host_files), good.approval_bytes)
            self.assertEqual(app.load_release(approved=True, context=context(copy)), {})
            fresh.assert_called_with('main', approved=True)
            for snapshot in cases:
                with self.subTest(snapshot=snapshot), self.assertRaisesRegex(ValueError, 'Selected release inputs changed'):
                    app.load_release(approved=True, context=context(snapshot))
            mutable = dict(good.files)
            selected = context(app.ReleaseSnapshot(good.manifest_bytes, mutable, dict(good.host_files), good.approval_bytes))
            mutable['ihx'] = b'after selection'
            with self.assertRaisesRegex(ValueError, 'Selected release inputs changed'):
                app.load_release(approved=True, context=selected)


if __name__ == '__main__':
    unittest.main()
