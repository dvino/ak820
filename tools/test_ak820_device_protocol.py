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
            bytes((8, 0x48))+bytes(30),  # unknown VialRGB command
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


class DirectRaw(Raw):
    def __init__(self):
        super().__init__()
        self.generation, self.state, self.coverage, self.ident = 4, 0, 0, 0
        self.palette = bytes((12,34,56))*82
        self.stale, self.bad_ack, self.fail_chunk = 0, False, False
        self.change_at = None

    def raw(self, packet):
        self.requests.append(packet)
        reply = bytearray(packet)
        if packet[:2] == b'\x08\x45':
            reply[2:14] = b'AD'+bytes((1,3,82,1,1,160,7,8,232,3))
        elif packet[:2] == b'\x08\x47':
            reply[2:11] = bytes((self.state,self.coverage))+self.ident.to_bytes(2,'little')+self.generation.to_bytes(4,'little')+b'\x03'
        elif packet[:2] == b'\x08\x46':
            first,count = packet[6:8]
            if first == self.change_at:
                self.change_at = None
                self.generation += 1
                self.palette = bytes((90,80,70))*82
            if self.stale:
                self.generation += 1
                self.stale -= 1
            status = 0 if int.from_bytes(packet[2:6],'little') == self.generation else 3
            reply[2:10] = bytes((status,first,count,3))+self.generation.to_bytes(4,'little')
            reply[10:10+3*count] = self.palette[3*first:3*(first+count)]
        elif packet[0] == 7:
            reply[2] = 0
            if packet[1] == 0x43:
                self.ident = int.from_bytes(packet[4:6],'little')
                self.state,self.coverage = 1,0
                self.stage = bytearray()
            elif packet[1] == 0x44:
                if self.fail_chunk: reply[2] = 1
                else:
                    self.coverage += packet[5]
                    self.stage.extend(packet[6:6+3*packet[5]])
            elif packet[1] == 0x45:
                self.generation += 1
                self.state = 2
                self.palette = bytes(self.stage)
            elif packet[1] == 0x46: self.state = 6
            if self.bad_ack: reply[31] = 1
        return bytes(reply)


class DirectTests(unittest.TestCase):
    def api(self, writes=False):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        raw = DirectRaw()
        api = protocol.DeviceAPI({},Path(temporary.name),lambda:raw,allow_writes=writes)
        self.addCleanup(api.close)
        return api,raw

    def test_snapshot_actual_palette_and_no_writes(self):
        api,raw = self.api()
        snapshot = api.direct_snapshot()
        self.assertEqual(snapshot['hsv_hex'],raw.palette.hex())
        self.assertEqual(snapshot['flags'],3)
        self.assertTrue(all(packet[0] == 8 for packet in raw.requests))
        self.assertEqual(len([p for p in raw.requests if p[1] == 0x46]),12)

    def test_stale_snapshot_restarts_and_bounded_failure(self):
        api,raw = self.api()
        raw.stale = 1
        self.assertEqual(api.direct_snapshot()['generation'],5)
        raw.stale = 10
        with self.assertRaisesRegex(ValueError,'bounded snapshot'): api.direct_snapshot()

    def test_old_image_unavailable(self):
        api,raw = self.api()
        api.app = Raw()
        self.assertIsNone(api.direct_snapshot())
        self.assertIsNone(api.direct_status())

    def test_full_frame_requires_explicit_writes(self):
        api,raw = self.api()
        with self.assertRaisesRegex(ValueError,'Writes are disabled'):
            api.set_direct_frame(raw.palette,frame_id=9,expected_generation=4)
        self.assertEqual(raw.requests,[])

    def test_commit_accepts_pending_publication(self):
        api,raw = self.api(True)
        result = api.set_direct_frame(raw.palette,frame_id=9,expected_generation=4)
        self.assertEqual(result['state'],2)
        self.assertEqual(result['generation'],5)
        self.assertEqual([p[5] for p in raw.requests if p[:2] == b'\x07\x44'],[8]*10+[2])

    def test_upload_normalizes_brightness_without_mutating_caller_bytes(self):
        api,raw = self.api(True)
        source = bytearray(bytes((1,2,255))*82)
        before = bytes(source)
        api.set_direct_frame(bytes(source), frame_id=9, expected_generation=4)
        chunks = [p for p in raw.requests if p[:2] == b'\x07\x44']
        transmitted = b''.join(p[6:6+3*p[5]] for p in chunks)
        self.assertEqual(transmitted, bytes((1,2,160))*82)
        self.assertEqual(bytes(source), before)

    def test_chunk_failure_stops_without_commit_or_abort(self):
        api,raw = self.api(True)
        raw.fail_chunk = True
        with self.assertRaisesRegex(ValueError,'status 1'):
            api.set_direct_frame(raw.palette,frame_id=9,expected_generation=4)
        self.assertNotIn(0x45,[p[1] for p in raw.requests if p[0] == 7])
        self.assertNotIn(0x46,[p[1] for p in raw.requests if p[0] == 7])

    def test_ack_corruption_stops(self):
        api,raw = self.api(True)
        raw.bad_ack = True
        with self.assertRaisesRegex(ValueError,'ACK mismatch'):
            api.set_direct_frame(raw.palette,frame_id=9,expected_generation=4)

    def test_partial_old_generation_is_discarded_on_concurrent_change(self):
        api,raw = self.api()
        raw.change_at = 7
        snapshot = api.direct_snapshot()
        self.assertEqual(snapshot['generation'],5)
        self.assertEqual(snapshot['hsv_hex'],bytes((90,80,70)).hex()*82)


if __name__ == '__main__':
    unittest.main()
