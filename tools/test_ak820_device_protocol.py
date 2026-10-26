"""Focused tests for the constrained, default-read-only protocol adapter."""
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))
import ak820_device_protocol as protocol


class Raw:
    def __init__(self):
        self.requests = []

    def raw(self, packet):
        self.requests.append(packet)
        reply = bytearray(packet)
        if packet[0] == 2:
            reply[2:6] = b'\0\0\0\x78'
        elif packet[0] == 14:
            count = packet[3]
            reply[4:4+count] = bytes(range(count))
        elif packet[:2] == b'\xfd\x01':
            reply = bytearray(bytes((253, 1, 1, 0xA8))+bytes(28))
        return bytes(reply)

    def close(self):
        pass


class ProtocolTests(unittest.TestCase):
    def api(self, allow_writes=False):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        raw = Raw()
        api = protocol.DeviceAPI({}, Path(self.tmp.name), lambda: raw, allow_writes=allow_writes)
        self.addCleanup(api.close)
        return api, raw

    def test_combo_set_is_read_only_by_default(self):
        api, raw = self.api()
        with self.assertRaisesRegex(ValueError, 'Writes are disabled'):
            api.set_combo(0, bytes(10))
        self.assertEqual(raw.requests, [])

    def test_combo_caps_word_validation_is_narrow_and_offline(self):
        data = bytes.fromhex('0400160000000000737c')
        self.assertEqual(protocol.DeviceAPI.validate_combo(data), data)
        self.assertEqual(protocol.DeviceAPI.stored_combo(data),
                         data[:4] + protocol.DeviceAPI.COMBO_MARKER + data[8:])
        for output in (0x7C72, 0x7C74, 0x2004, 0x5000):
            with self.subTest(output=output), self.assertRaises(ValueError):
                protocol.DeviceAPI.validate_combo(data[:8] + output.to_bytes(2, 'little'))

    def test_combo_validation_rejects_unsupported_input_without_transport(self):
        api, raw = self.api(True)
        for data in (bytes(9), bytes.fromhex('04000400000000000600'),
                     bytes.fromhex('04000500010000000600')):
            with self.assertRaises(ValueError):
                api.set_combo(0, data)
        self.assertEqual(raw.requests, [])
        for packet in (api.packet(254, 13, 1), api.packet(254, 13, 3, 8),
                       api.packet(254, 13, 0, 1)):
            with self.assertRaises(ValueError):
                api.exchange(packet)
        self.assertEqual(raw.requests, [])

    def test_default_is_read_only_and_typed_getter_still_works(self):
        api, raw = self.api()
        self.assertFalse(api.allow_writes)
        self.assertEqual(api.get_layout_options(), 0x78)
        for setter in (
            lambda: api.set_key(0, (0, 0), 4),
            lambda: api.set_encoder(0, 0, 4),
            lambda: api.set_layout_options(4),
            lambda: api.upload_macro_chunk(0, b'\x01'),
            lambda: api.set_rgb_mode(bytes(6)),
            api.save_rgb,
        ):
            with self.subTest(setter=setter):
                with self.assertRaisesRegex(ValueError, 'Writes are disabled'):
                    setter()
        self.assertEqual(raw.requests, [bytes((2, 2))+bytes(30)])

    def test_write_mode_cannot_be_enabled_by_truthy_non_boolean(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'explicit boolean'):
                protocol.DeviceAPI({}, Path(tmp), lambda: Raw(), allow_writes='false')
            self.assertFalse((Path(tmp) / 'transport.jsonl').exists())

    def test_writable_typed_calls_emit_only_expected_packets(self):
        api, raw = self.api(allow_writes=True)
        self.assertTrue(api.set_layout_options(0x78))
        self.assertTrue(api.upload_macro_chunk(28, b'abc'))
        self.assertTrue(api.save_rgb())
        self.assertEqual(raw.requests, [
            bytes((3, 2, 0, 0, 0, 0x78))+bytes(26),
            bytes((15, 0, 28, 3))+b'abc'+bytes(25),
            bytes((9,))+bytes(31),
        ])

    def test_macro_getter_is_typed_and_bounded(self):
        api, raw = self.api()
        self.assertEqual(api.get_macro_buffer(28, 3), b'\0\1\2')
        self.assertEqual(raw.requests, [bytes((14, 0, 28, 3))+bytes(28)])
        for offset, count in ((0, 29), (8192, 1), (-1, 1), (0, -1)):
            with self.subTest(offset=offset, count=count):
                with self.assertRaises(ValueError):
                    api.get_macro_buffer(offset, count)

    def test_layout_high_bytes_are_rejected_on_getter_and_setter(self):
        api, raw = self.api(allow_writes=True)
        def bad_layout_reply(packet):
            raw.requests.append(packet)
            return bytes((2, 2, 1, 0, 0, 7))+bytes(26)
        raw.raw = bad_layout_reply
        with self.assertRaisesRegex(ValueError, 'one-byte'):
            api.get_layout_options()
        with self.assertRaisesRegex(ValueError, 'one-byte'):
            api.set_layout_options(256)
        self.assertEqual(len(raw.requests), 1)

    def test_status_rejects_latched_failure_stage(self):
        api, raw = self.api()
        raw.raw = lambda packet: bytes((253, 1, 1, 0xA8, 0, 0, 0, 0, 0, 0, 1))+bytes(21)
        with self.assertRaisesRegex(ValueError, 'Storage failure'):
            api.status()

    def test_rejects_unknown_commands_and_malformed_shapes_before_io(self):
        api, raw = self.api(allow_writes=True)
        for packet in (
            bytes((253, 2))+bytes(30),  # unknown FD subcommand
            bytes((254, 5))+bytes(30),  # unknown FE subcommand
            bytes((4, 6, 0, 0))+bytes(28),  # invalid layer
            bytes((8, 0x45))+bytes(30),  # unknown VialRGB command
            bytes((15, 0, 0, 29))+bytes(28),  # oversized macro chunk
            bytes((7, 0x40))+bytes(30),  # forbidden RGB setter family
            bytes((253, 0, 0, 0, 28))+bytes(27),  # FD read >27-byte transfer
            bytes((254, 3, 0, 1))+bytes(28),  # malformed encoder getter
        ):
            with self.subTest(packet=packet.hex()):
                with self.assertRaises(ValueError):
                    api.exchange(packet)
        self.assertEqual(raw.requests, [])

    def test_valid_write_packet_is_blocked_at_exchange_boundary(self):
        api, raw = self.api()
        with self.assertRaisesRegex(ValueError, 'Writes are disabled'):
            api.exchange(bytes((3, 2, 0, 0, 0, 1))+bytes(26))
        self.assertEqual(raw.requests, [])

    def test_bad_typed_write_arguments_are_rejected(self):
        api, raw = self.api(allow_writes=True)
        invalid = (
            lambda: api.set_key(6, (0, 0), 1),
            lambda: api.set_encoder(0, 2, 1),
            lambda: api.set_layout_options(-1),
            lambda: api.upload_macro_chunk(8192, b'x'),
            lambda: api.upload_macro_chunk(0, bytes(29)),
            lambda: api.set_rgb_mode(b'bad'),
        )
        for operation in invalid:
            with self.subTest(operation=operation):
                with self.assertRaises(ValueError):
                    operation()
        self.assertEqual(raw.requests, [])


if __name__ == '__main__':
    unittest.main()
