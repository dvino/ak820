"""Offline regression for exact beta.2 catalog edge coverage."""
import unittest

from verify_beta2_handoff import checked_transition_edges


class TransitionEdgesTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{'source': f'source-{source}', 'target': f'target-{target}'}
                     for source in range(33) for target in range(10)]
        self.expected = {(f'source-{source}', f'target-{target}')
                         for source in range(10) for target in range(10)}

    def test_complete_catalog(self):
        edges = checked_transition_edges(self.rows, self.expected)
        self.assertEqual(len(edges), 330)

    def test_duplicate_expected_edge_with_unchanged_row_count(self):
        self.rows[-1] = dict(self.rows[0])
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            checked_transition_edges(self.rows, self.expected)

    def test_missing_expected_edge_with_unchanged_row_count(self):
        self.rows[0] = {'source': 'unrelated', 'target': 'unrelated'}
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            checked_transition_edges(self.rows, self.expected)

    def test_incomplete_catalog(self):
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            checked_transition_edges(self.rows[:-1], self.expected)


if __name__ == '__main__':
    unittest.main()
