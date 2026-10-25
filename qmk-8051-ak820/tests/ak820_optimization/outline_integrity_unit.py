#!/usr/bin/env python3
"""Adversarial byte fixtures for following outlined, shared return tails."""
import unittest
from outline import flattened_helper


def memory(at, raw):
    return {at+i: value for i,value in enumerate(bytes.fromhex(raw))}


class HelperTails(unittest.TestCase):
    body = bytes.fromhex('e4f822')

    def test_direct_and_long_tail(self):
        self.assertEqual(flattened_helper(memory(0, 'e4f822'),0,self.body),self.body)
        code = memory(0,'e4020010') | memory(0x10,'f822')
        self.assertEqual(flattened_helper(code,0,self.body),self.body)

    def test_short_absolute_uses_next_pc_page(self):
        code = memory(0x7fe,'0108') | memory(0x808,'e4f822')
        self.assertEqual(flattened_helper(code,0x7fe,self.body),self.body)

    def test_signed_relative_tail(self):
        code = memory(0x20,'80ee') | memory(0x10,'e4f822')
        self.assertEqual(flattened_helper(code,0x20,self.body),self.body)

    def test_multiple_tails(self):
        code = memory(0,'020010') | memory(0x10,'e4800d') | memory(0x20,'f822')
        self.assertEqual(flattened_helper(code,0,self.body),self.body)

    def test_rejects_cycle_and_missing_target(self):
        for code in (memory(0,'80fe'),memory(0,'020010'),memory(0,'e4f8')):
            with self.assertRaises((ValueError,KeyError)):
                flattened_helper(code,0,self.body)

    def test_rejects_calls_conditional_jumps_and_byte_changes(self):
        for raw in ('120010','1100','6000','e5f822','e4f922','e4f800'):
            with self.subTest(raw=raw),self.assertRaises((ValueError,KeyError)):
                flattened_helper(memory(0,raw),0,self.body)


if __name__ == '__main__':
    unittest.main()
