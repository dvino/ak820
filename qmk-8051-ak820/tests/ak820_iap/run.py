#!/usr/bin/env python3
"""Execute linked AK820 VIA/NVM/IAP code with an explicit peripheral model.

No device is enumerated or opened. uCsim models CPU instructions, while this
runner supplies CH555 ROM_STATUS and Flash effects at actual ROM_CTRL writes.
IAP latency is not modeled by uCsim; latency results are separately labeled.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import select
import subprocess
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ak820_emitted", HERE.parent / "ak820_emitted/run.py")
emitted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emitted)


class Console:
    def __init__(self, simulator: Path, image: Path):
        self.process = subprocess.Popen([str(simulator), "-t", "C52", "-b", "-c", "-", str(image)],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.log, self.sequence = "", 0

    def command(self, commands: str | list[str]) -> str:
        self.sequence += 1
        marker = f"__DONE_{self.sequence}__"
        if isinstance(commands, str): commands = [commands]
        self.process.stdin.write(("\n".join(commands + ["echo " + marker]) + "\n").encode())
        self.process.stdin.flush()
        data, deadline = b"", time.monotonic() + 20
        while ("\n" + marker + "\n").encode() not in data:
            timeout = deadline - time.monotonic()
            if timeout <= 0: raise TimeoutError(data.decode(errors="replace"))
            ready, _, _ = select.select([self.process.stdout], [], [], timeout)
            if not ready: continue
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk: raise RuntimeError("Simulator ended: " + data.decode(errors="replace"))
            data += chunk
        answer = data.decode(errors="replace")
        self.log += answer
        if "Stack overflow" in answer: raise AssertionError("CPU stack overflow")
        return answer

    def read(self, space: str, address: int, length: int) -> list[int]:
        label = f"read{self.sequence}"
        output = self.command(emitted.Firmware.dump(label, space, address, length))
        if space != "sfr": return emitted.Firmware.extract(output, label, address, length)
        values = {}
        for row, data in re.findall(r"^0x([0-9a-f]+)\s+((?:[0-9a-f]{2}\s+)+)", output, re.M):
            for offset, value in enumerate(data.split()): values[int(row, 16) + offset] = int(value, 16)
        for row, value in re.findall(r"^0x([0-9a-f]+)\s+\w+:\s+0b[01]+\s+0x([0-9a-f]+)", output, re.M):
            values[int(row, 16)] = int(value, 16)
        return [values[address + index] for index in range(length)]

    def close(self):
        try:
            self.process.stdin.write(b"quit\n")
            self.process.stdin.flush()
            self.process.wait(timeout=5)
        finally:
            if self.process.poll() is None:
                self.process.kill()
                self.process.wait()


class Fixture:
    def __init__(self, build: Path, simulator: Path, output: Path, name: str, dense=False, ie=0):
        self.output, self.name = output, name
        self.fw = emitted.Firmware(build, simulator, output)
        self.has_diagnostics = "_ak820_nvm_diagnostic" in self.fw.symbols
        self.console = Console(simulator, self.fw.image)
        self.operations, self.status_reads = [], []
        self.fault_at = self.partial_at = None
        self.pending_post_status = None
        self.force_invalid_address_status = False
        self.byte_program_noop = False
        self.erase_noop = False
        self.replace_block = False
        self.console.command(self.fw.initialize())
        if dense: self.console.command(emitted.memory("rom", 0xC740, [1, 4] * 32))
        self.console.command(self.fw.call("_eeprom_driver_init"))
        self.console.command(["set memory sfr 0x86 0xc0", f"set memory sfr 0xa8 {ie}",
                              "break sfr w 0x86", "break sfr r 0x86", "break 0x2700"])

    def write(self, symbol: str, data):
        self.console.command(self.fw.write(symbol, data))

    def read(self, space: str, address: int, length: int):
        return self.console.read(space, address, length)

    def symbol(self, name: str, length: int):
        return self.read("xram", self.fw.address(name), length)

    def call(self, symbol: str, argument=None):
        output = self.console.command(self.fw.call(symbol, argument))
        while "Event break" in output:
            if "Event `read' at sfr[0x86]" in output: self._status_read(output)
            else: self._iap()
            output = self.console.command("run")
        assert "0x2700" in output, output

    def _status_read(self, output):
        # uCsim traps after the read instruction. Supply the modeled value to
        # its actual destination register before the following instruction.
        # In block mode bROM_ADDR_OK depends on source DPTR as well as the ROM
        # address, reproducing the OEM source/target low-six-bit constraint.
        pc = int(re.findall(r"F 0x([0-9a-f]+)", output)[-1], 16)
        values = self.read("sfr", 0x82, 14)
        pointer, address, mode = values[0] | values[1] << 8, values[2] | values[3] << 8, values[13]
        is_post = self.pending_post_status is not None
        if is_post:
            status = self.pending_post_status
            self.pending_post_status = None
        else:
            valid = 0xC700 <= address < 0xEF80
            if mode != 0x80:
                valid = valid and (pointer & 63) == (address & 63) and 0x400 <= pointer <= 0xFC0
            if self.force_invalid_address_status: valid = False
            status = (values[4] & ~0x40) | (0x40 if valid else 0)
        if self.fw.code.get(pc - 2) == 0xE5 and self.fw.code.get(pc - 1) == 0x86:
            destination = 0xE0
        elif self.fw.code.get(pc - 3) == 0x85 and self.fw.code.get(pc - 2) == 0x86:
            destination = self.fw.code[pc - 1]
        else: raise AssertionError(f"Unmodeled ROM_STATUS read instruction before {pc:#x}")
        self.status_reads.append(dict(pc=pc, address=address, dptr=pointer, mode=mode, status=status, post=is_post))
        self.console.command(f"set memory sfr {destination:#x} {status:#x}")

    def _iap(self):
        values = self.read("sfr", 0x80, 0x40)
        address, pointer = values[4] | values[5] << 8, values[2] | values[3] << 8
        opcode, value, mode, ie, config = values[6], values[14], values[15], values[40], values[49]
        event = dict(address=address, opcode=opcode, value=value, mode=mode, dptr=pointer, ie=ie, config=config)
        self.operations.append(event)
        assert 0xC700 <= address < 0xEF80, event
        assert opcode in (0x9A, 0xA6) and mode in (0x80, 0x3F), event
        assert config & 8 and not ie & 0x80, event
        status = 0xC0
        if self.fault_at == len(self.operations):
            status = 0xC2
        elif opcode == 0xA6:
            assert mode == 0x80 and address % 64 == 0, event
            if self.erase_noop:
                event['accepted_without_effect'] = True
            else:
                self.console.command(f"fill rom {address:#x} {address + 63:#x} 0")
        elif mode == 0x80:
            # Explicit negative control matching the observed RC5 hardware
            # symptom: accepted status does not prove this unverified mode
            # wrote a byte. Production must use the OEM-backed block path.
            if self.byte_program_noop:
                event['accepted_without_effect'] = True
            else:
                old = self.read("rom", address, 1)[0]
                self.console.command(emitted.memory("rom", address, [old | value]))
        else:
            assert address % 64 == 0 and pointer % 64 == 0, event
            assert 0x400 <= pointer <= 0xFC0, event
            data, old = self.read("xram", pointer, 64), self.read("rom", address, 64)
            if self.partial_at == len(self.operations):
                # Accepted command with bad physical readback: preserve a
                # prefix only, while reporting success at the SFR layer.
                data = data[:13] + [0] * 51
            event["data_sha256"] = hashlib.sha256(bytes(data)).hexdigest()
            programmed = data if self.replace_block else [a | b for a, b in zip(old, data)]
            self.console.command(emitted.memory("rom", address, programmed))
        self.console.command(f"set memory sfr 0x86 {status:#x}")
        self.pending_post_status = status

    def packet(self, packet):
        # Supply host completion for a previous reply and a newly received
        # packet. Electrical USB reception/IRQ timing is outside this fixture.
        self.console.command("set memory xram 0x2203 0x12")
        self.write("_raw_buffer", list(packet) + [0] * (32 - len(packet)))
        self.write("_raw_state", [2])
        self.call("_ak820_usb_raw_task")
        return self.symbol("_raw_buffer", 32)

    def ack(self):
        return self.symbol("_raw_state", 1) == [5] and self.read("xram", 0x2203, 1)[0] & 3 == 0

    def healthy(self):
        self.call("_ak820_nvm_ok")
        return self.read("sfr", 0x82, 1)[0] == 1

    def finish(self, result):
        try:
            self.console.command("state")
            peaks = re.findall(r"Most value of stack pointer=\s+0x([0-9a-f]+)", self.console.log)
            result.update(name=self.name, passed=True, operations=self.operations, status_reads=self.status_reads,
                          peak_sp=int(peaks[-1], 16),
                          image_sha256=hashlib.sha256(self.fw.image.read_bytes()).hexdigest())
            (self.output / (self.name + ".json")).write_text(json.dumps(result, indent=2) + "\n")
            return result
        finally:
            self.close()

    def close(self):
        (self.output / (self.name + ".log")).write_text(self.console.log)
        self.console.close()


def remap(build, simulator, output, dense=False, byte_program_noop=False):
    fixture = Fixture(build, simulator, output, "dense-remap" if dense else "normal-remap", dense=dense, ie=0x80)
    try:
        fixture.byte_program_noop = byte_program_noop
        packet = [5, 0, 0, 0, int(dense), 5]
        assert fixture.packet(packet)[:6] == packet and fixture.ack() and fixture.healthy()
        expected = ([1, 5] + [1, 4] * 31) if dense else None
        page = fixture.read("rom", 0xC740, 64)
        assert page[:2] == [int(dense), 5]
        if expected: assert page == expected
        assert fixture.read("rom", 0xEF40, 64) == [0] * 64
        assert fixture.read("sfr", 0xA8, 1) == [0x80]
        assert fixture.read("sfr", 0xB1, 1)[0] & 8 == 0
        initial_count = len(fixture.operations)
        diagnostic = None
        if fixture.has_diagnostics:
            diagnostic = fixture.packet([0xFD, 1])
            assert diagnostic[:4] == [0xFD, 1, 1, 0xA8]
            assert diagnostic[4:11] == [0, 1, 0, 0, 1, 0, 0]
            assert diagnostic[11:17] == [1, 0xA6, 0xC0, 0xC0, 0x40, 0xEF]
            assert diagnostic[17:22] == [0, 0, 1, 0, 3]
            assert len(fixture.operations) == initial_count
        fixture.packet(packet)
        assert fixture.ack() and len(fixture.operations) == initial_count
        fixture.call("_eeprom_driver_init")
        assert fixture.healthy() and len(fixture.operations) == initial_count
        assert fixture.packet([4, 0, 0, 0])[4:6] == [int(dense), 5]
        assert fixture.packet([0xFD, 0, 0xC7, 0x40, 2])[5:7] == [int(dense), 5]
        assert len(fixture.operations) == initial_count
        return fixture.finish(dict(iap_count=initial_count, physical_page=page,
                                   retry_adds_no_iap=True, backend_reinit_and_fd00_match=True, fd01=diagnostic,
                                   unverified_byte_mode_noop=byte_program_noop))
    except BaseException:
        fixture.close()
        raise


def fault(build, simulator, output, kind):
    fixture = Fixture(build, simulator, output, kind, dense=True, ie=0x80)
    try:
        before = fixture.read("rom", 0xC740, 64)
        if kind == "command-error": fixture.fault_at = 3
        elif kind == "partial-journal-program": fixture.partial_at = 3
        elif kind == "partial-target-program": fixture.partial_at = 12
        elif kind == "address-status-invalid": fixture.force_invalid_address_status = True
        fixture.packet([5, 0, 0, 0, 1, 5])
        assert not fixture.ack() and not fixture.healthy()
        assert fixture.read("sfr", 0xA8, 1) == [0x80]
        assert fixture.read("sfr", 0xB1, 1)[0] & 8 == 0
        if kind != "partial-target-program": assert fixture.read("rom", 0xC740, 64) == before
        count = len(fixture.operations)
        diagnostic = None
        if fixture.has_diagnostics:
            diagnostic = fixture.packet([0xFD, 1])
            expected_stage = 5 if kind == "address-status-invalid" else 12 if kind == "partial-target-program" else 7
            expected_address = 0xEF40 if kind == "address-status-invalid" else 0xC740 if kind == "partial-target-program" else 0xEF00
            before_status = 0x80 if kind == "address-status-invalid" else 0xC0
            after_status = 0xC2 if kind == "command-error" else before_status
            operation = 0xA6 if kind == "address-status-invalid" else 0x9A
            assert diagnostic[:4] == [0xFD, 1, 1, 0xA8]
            assert diagnostic[4:11] == [1, 1, 1, 0, 1, 0, expected_stage]
            assert diagnostic[11:17] == [1, operation, before_status, after_status, expected_address & 255, expected_address >> 8]
            assert fixture.ack() and len(fixture.operations) == count
        getter = fixture.packet([4, 0, 0, 0])
        assert fixture.ack() and getter[4:6] == [1, 5]  # RAM cache only
        fd00 = fixture.packet([0xFD, 0, 0xC7, 0x40, 27])
        assert fixture.ack() and len(fixture.operations) == count
        if kind != "partial-target-program": assert fd00[5:7] == before[:2]
        if kind == "partial-target-program":
            assert fixture.read("rom", 0xEF40, 1) == [0xA5]
            fixture.partial_at = None
            fixture.call("_eeprom_driver_init")
            assert fixture.healthy()
            assert fixture.read("rom", 0xC740, 64) == [1, 5] + [1, 4] * 31
            assert fixture.read("rom", 0xEF40, 64) == [0] * 64
        return fixture.finish(dict(no_setter_ack=True, cached_getter_is_not_durable_evidence=True,
                                   fd00_direct_read=True, recovery_replayed=kind == "partial-target-program", fd01=diagnostic))
    except BaseException:
        fixture.close()
        raise


def bounds(build, simulator, output):
    fixture = Fixture(build, simulator, output, "bounds-and-low-level-abi", ie=0x80)
    try:
        source = 0x0F00
        pattern = [(i * 7 + 3) & 255 for i in range(64)]
        fixture.console.command(emitted.memory("xram", source, pattern))
        fixture.write("_ak820_flash_program_page_PARM_2", list(source.to_bytes(2, "little")))
        rejected = []
        for symbol, addresses in [
            ("_ak820_flash_program_page", [0, 0x27C0, 0xC6C0, 0xC701, 0xEF80, 0xFFFF]),
            ("_ak820_flash_erase", [0, 0x27C0, 0xC6C0, 0xC701, 0xEF80, 0xFFFF]),
            ("_ak820_flash_program", [0, 0x27C0, 0xC6FF, 0xEF80, 0xFFFF]),
        ]:
            for address in addresses:
                fixture.call(symbol, address)
                assert fixture.read("sfr", 0x82, 1) == [0] and not fixture.operations
                rejected.append([symbol, address])
        for address in (0xC700, 0xEF40):
            fixture.call("_ak820_flash_erase", address)
            fixture.call("_ak820_flash_program_page", address)
            assert fixture.read("sfr", 0x82, 1) == [1]
            assert fixture.read("rom", address, 64) == pattern
            assert fixture.read("sfr", 0xA8, 1) == [0x80]
            assert fixture.read("sfr", 0xB1, 1)[0] & 8 == 0
        return fixture.finish(dict(rejected=rejected, aligned_dptr_checked_at_opcode=True))
    except BaseException:
        fixture.close()
        raise


def block_invalid_status(build, simulator, output):
    fixture = Fixture(build, simulator, output, "block-invalid-prestatus", ie=0x80)
    try:
        source = 0x0F00
        fixture.console.command(emitted.memory("xram", source, [0x5A] * 64))
        fixture.write("_ak820_flash_program_page_PARM_2", list(source.to_bytes(2, "little")))
        fixture.force_invalid_address_status = True
        before = fixture.read("rom", 0xC700, 64)
        fixture.call("_ak820_flash_program_page", 0xC700)
        assert fixture.read("sfr", 0x82, 1) == [0]
        assert not fixture.operations and fixture.pending_post_status is None
        assert fixture.read("rom", 0xC700, 64) == before
        assert fixture.read("sfr", 0xA8, 1) == [0x80]
        assert fixture.read("sfr", 0xB1, 1)[0] & 8 == 0
        assert len(fixture.status_reads) == 1
        read = fixture.status_reads[0]
        assert read["mode"] == 0x3F and read["dptr"] % 64 == 0 and read["status"] == 0x80
        if fixture.has_diagnostics:
            assert fixture.symbol("_ak820_flash_diagnostic", 6) == [1, 0x9A, 0x80, 0x80, 0, 0xC7]
        return fixture.finish(dict(no_opcode=True, physical_page_unchanged=True,
                                   raw_before_after_preserved=True, interrupt_and_write_protection_restored=True))
    except BaseException:
        fixture.close()
        raise


def byte_block_preservation(build, simulator, output, replace):
    name = 'byte-readmerge-replacement-model' if replace else 'byte-readmerge-setbits-model'
    fixture = Fixture(build, simulator, output, name, ie=0x80)
    try:
        fixture.byte_program_noop = True
        fixture.replace_block = replace
        tested = []
        for offset in (0, 1, 8, 31, 62, 63):
            for value in (0, 0xA5, 255):
                page = [(i * 7 + 3) & 255 for i in range(64)]
                fixture.console.command(emitted.memory('rom', 0xEF40, page))
                fixture.write('_ak820_flash_program_PARM_2', [value])
                fixture.call('_ak820_flash_program', 0xEF40 + offset)
                assert fixture.read('sfr', 0x82, 1) == [1]
                page[offset] |= value
                assert fixture.read('rom', 0xEF40, 64) == page
                event = fixture.operations[-1]
                assert event['opcode'] == 0x9A and event['mode'] == 0x3F
                assert event['address'] == 0xEF40 and event['dptr'] % 64 == 0
                assert fixture.read('sfr', 0xA8, 1) == [0x80]
                assert not fixture.read('sfr', 0xB1, 1)[0] & 8
                tested.append([offset, value])
        return fixture.finish(dict(cases=tested, neighbouring_bytes_preserved=True,
                                   block_semantics='replace' if replace else 'set-bits',
                                   unverified_byte_mode_noop=True))
    except BaseException:
        fixture.close()
        raise


def encoder_remap(build, simulator, output):
    fixture = Fixture(build, simulator, output, 'encoder-web-all-layers-directions', ie=0x80)
    try:
        fixture.byte_program_noop = True
        expected_page = [0] * 64
        tested = []
        for layer in range(6):
            for direction in range(2):
                code = 0x0404 + layer * 16 + direction
                packet = [0xFE, 4, layer, 0, direction, code >> 8, code & 255]
                assert fixture.packet(packet)[:7] == packet and fixture.ack() and fixture.healthy()
                offset = layer * 4 + (0 if direction else 2)
                expected_page[offset:offset+2] = [code >> 8, code & 255]
                assert fixture.read('rom', 0xCD40, 64) == expected_page
                response = fixture.packet([0xFE, 3, layer, 0])
                assert fixture.ack() and response[direction*2:direction*2+2] == [code >> 8, code & 255]
                assert fixture.read('rom', 0xEF40, 64) == [0] * 64
                tested.append([layer, direction, code])
        return fixture.finish(dict(cases=tested, all_six_layers_both_directions=True,
                                   physical_encoder_page=0xCD40, commit_cleanup_each_write=True,
                                   byte_mode_noop=True, no_false_ack=True))
    except BaseException:
        fixture.close()
        raise


def latency(baseline, current):
    upstream = HERE / "fixtures/vial-v0.7.5-util.py"
    tree = ast.parse(upstream.read_text())
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "hid_send")
    namespace = {"MSG_LEN": 32, "time": time}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(upstream), "exec"), namespace)
    class Device:
        def __init__(self, delay): self.delay, self.timeout = delay, None
        def write(self, data): self.reply = data[1:]; return len(data)
        def read(self, length, timeout_ms):
            self.timeout = timeout_ms
            return self.reply[:length] if self.delay <= timeout_ms else []
    results = []
    for label, record in (("baseline", baseline), ("candidate", current)):
        device, error = Device(record["iap_count"] * 5), None
        try: namespace["hid_send"](device, b"\x05\x00\x00\x00\x01\x05")
        except RuntimeError as exception: error = str(exception)
        results.append(dict(label=label, iap_count=record["iap_count"], assumed_typical_ms=device.delay,
                            upstream_timeout_ms=device.timeout, error=error))
    assert results[0]["error"] == "failed to communicate with the device"
    assert results[1]["error"] is None
    return dict(passed=True, scope="LATENCY_MODEL_ONLY", results=results,
                assumption="CH555 TERPG typical 5 ms per command; no physical chip timing measured",
                official_source="https://github.com/vial-kb/vial-gui/blob/e42622c352b69eff523a467718db487ab9c9cbf2/src/main/python/util.py",
                source_sha256=hashlib.sha256(upstream.read_bytes()).hexdigest())


def reproduce_byte_noop(build, simulator, output):
    fixture = Fixture(build, simulator, output, 'byte-mode-noop-reproduces-stage9', dense=True, ie=0x80)
    try:
        fixture.byte_program_noop = True
        before = fixture.read('rom', 0xC740, 64)
        fixture.packet([5, 0, 0, 0, 1, 5])
        assert not fixture.ack() and not fixture.healthy()
        diagnostic = fixture.packet([0xFD, 1])
        assert fixture.ack() and diagnostic[4] == 1 and diagnostic[10] == 9
        assert fixture.read('rom', 0xEF40, 64) == [0] * 64
        assert fixture.read('rom', 0xC740, 64) == before
        assert any(event.get('accepted_without_effect') for event in fixture.operations)
        return fixture.finish(dict(no_false_ack=True, first_failure_stage=9, header_unchanged=True,
                                   target_unchanged=True, fd01=diagnostic,
                                   limitation='Matches observed failure mechanism conditionally; does not model real controller electronics.'))
    except BaseException:
        fixture.close()
        raise


def ineffective_erase_target(build, simulator, output, profile):
    """Check preselected legacy or guarded-erase behavior under Flash fault."""
    if profile not in ('legacy-iap', 'guarded-erase'):
        raise ValueError(f"Unknown IAP fault profile: {profile}")
    fixture = Fixture(build, simulator, output, 'ineffective-erase-target-and-replay', ie=0x80)
    try:
        # OEM ROM observation: the encoder CW word starts as 00A9 at CD40.
        original_target = [0x00, 0xA9] + [0] * 62
        fixture.console.command(emitted.memory('rom', 0xCD40, original_target))
        fixture.erase_noop = True
        fixture.byte_program_noop = True

        # Existing firmware writes this logical CW slot through NVM page CD40.
        # Model A6 as accepted but ineffective and 9A as accepted zero-to-one
        # programming. The committed redo record should remain after readback.
        # Match the observed temporary CW value. Zero is a subset of 00A9's
        # programmed bits, so an OR-program attempt cannot change the old page.
        desired = 0x0000
        setter = [0xFE, 4, 0, 0, 1, desired >> 8, desired & 255]
        assert fixture.packet(setter)[:7] == setter
        assert not fixture.ack() and not fixture.healthy()
        assert fixture.read('rom', 0xCD40, 64) == original_target
        header = fixture.read('rom', 0xEF40, 9)
        assert header[0] == 0xA5
        assert all((header[index] ^ header[index + 4]) == 0xFF for index in range(1, 5))
        diagnostic = fixture.packet([0xFD, 1])
        assert fixture.ack()
        assert diagnostic[4:11] == [1, 1, 1, 0, 0x19, 0x00, 12]
        expected_opcode = 0xA6 if profile == 'guarded-erase' else 0x9A
        assert diagnostic[11:17] == [1, expected_opcode, 0xC0, 0xC0, 0x40, 0xCD]
        target_ops = [event for event in fixture.operations if event['address'] == 0xCD40]
        if profile == 'guarded-erase':
            assert target_ops and target_ops[-1]['opcode'] == 0xA6
            assert not any(event['opcode'] == 0x9A for event in target_ops)
        else:
            assert target_ops and target_ops[-1]['opcode'] == 0x9A
        # The setter's cache can expose the requested word while the durable
        # target page is still the OEM value. Treat this as diagnostic only.
        getter = fixture.packet([0xFE, 3, 0, 0])
        assert fixture.ack()

        # Reinitialization retries the valid journal. The same ineffective
        # erase leaves the target unchanged and reports recovery-write stage 3.
        fixture.call('_eeprom_driver_init')
        assert not fixture.healthy()
        assert fixture.read('rom', 0xCD40, 64) == original_target
        assert fixture.read('rom', 0xEF40, 1) == [0xA5]
        recovery = fixture.packet([0xFD, 1])
        assert fixture.ack() and recovery[4] == 1 and recovery[10] == 3
        target_ops = [event for event in fixture.operations if event['address'] == 0xCD40]
        if profile == 'guarded-erase':
            assert not any(event['opcode'] == 0x9A for event in target_ops)
        return fixture.finish(dict(
            iap_fault_profile=profile,
            failure_model='A6 erase no-op; any 9A reports success but only OR-programs bits',
            initial_encoder_cw=[0, 0xA9], desired_encoder_cw=[desired >> 8, desired & 255],
            target_unchanged=True, journal_header_remains_committed=True,
            setter_acknowledged=False, first_failure_stage=12,
            last_target_iap=[expected_opcode, 0xC0, 0xC0, 0xCD40],
            target_9a_program_issued=any(event['opcode'] == 0x9A for event in target_ops),
            cached_getter_response=getter[:8], getter_not_durable_evidence=True,
            boot_replay_failure_stage=3,
            hardware_cause_confirmed=False,
            limitation='Conditional CPU/peripheral-model reproduction; does not establish the physical controller failure cause.'))
    except BaseException:
        fixture.close()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--s51", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--baseline-build-dir", type=Path)
    parser.add_argument('--reproduce-byte-noop-only', action='store_true')
    parser.add_argument('--ineffective-erase-target-only', action='store_true')
    parser.add_argument('--iap-fault-profile', choices=('legacy-iap', 'guarded-erase'),
                        help='Expected linked behavior for the ineffective-erase case; bind this to the selected image.')
    args = parser.parse_args()
    if args.output_dir.exists(): raise ValueError("Use a new output directory")
    args.output_dir.mkdir(parents=True)
    build, simulator = args.build_dir.resolve(), args.s51.resolve()
    if args.reproduce_byte_noop_only:
        record = reproduce_byte_noop(build, simulator, args.output_dir)
        (args.output_dir / 'results.json').write_text(json.dumps(record, indent=2) + '\n')
        print('PASS: linked negative control reproduces metadata readback fault 9 with accepted byte-mode no-op.')
        return
    if not args.iap_fault_profile:
        parser.error('--iap-fault-profile is required for the IAP suite; bind the expected behavior to the linked image')
    if args.ineffective_erase_target_only:
        record = ineffective_erase_target(build, simulator, args.output_dir, args.iap_fault_profile)
        (args.output_dir / 'results.json').write_text(json.dumps(record, indent=2) + '\n')
        print('PASS: linked failure-model scenario retains committed journal, rejects target readback, and retries on boot.')
        return
    cases = [remap(build, simulator, args.output_dir, byte_program_noop=True),
             remap(build, simulator, args.output_dir, dense=True, byte_program_noop=True)]
    assert all(event['mode'] == 0x3F for event in cases[1]['operations'] if event['opcode'] == 0x9A)
    assert cases[1]["iap_count"] <= 14
    for kind in ("command-error", "partial-journal-program", "partial-target-program", "address-status-invalid"):
        cases.append(fault(build, simulator, args.output_dir, kind))
    cases.append(bounds(build, simulator, args.output_dir))
    cases.append(block_invalid_status(build, simulator, args.output_dir))
    cases += [byte_block_preservation(build, simulator, args.output_dir, False),
              byte_block_preservation(build, simulator, args.output_dir, True)]
    cases.append(encoder_remap(build, simulator, args.output_dir))
    cases.append(ineffective_erase_target(build, simulator, args.output_dir, args.iap_fault_profile))
    report = dict(scope="OFFLINE_CPU_AND_EXPLICIT_PERIPHERAL_MODEL", cases=cases,
                  hardware_validated=False,
                  limits="No electrical USB, real IAP, voltage, interrupt overlap, or physical reset validation")
    if args.baseline_build_dir:
        baseline = remap(args.baseline_build_dir.resolve(), simulator, args.output_dir / "baseline", dense=True)
        report["baseline"] = baseline
        report["latency"] = latency(baseline, cases[1])
    (args.output_dir / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(passed=True, cases=len(cases), dense_iap_count=cases[1]["iap_count"],
                          hardware_validated=False)))


if __name__ == "__main__": main()
