# Review of the shared extra-report tail, 2026-10-23

Decision: GO for source integration of the exact private candidate below.
No blocking finding remains. This review does not approve a commit, packed
firmware, USB testing or flashing. A full production build and its checks
still belong to integration.

The reviewer did not author the candidate. Review was read-only except for
this note. No compiler, linker, simulator or device operation was run. Saved
CPU results were inspected, not rerun.

## Files and measured result

The candidate and control are under
`qmk-8051-ak820/.build/rc6-host-extra-tail-probe-20261023/`.
Review covered `probe.py`, the reused frozen-link script, both `host.c`
copies, generated assembly, compile logs, linked images and memory report,
both JSON reports, the CPU fixture and its two result files. It also covered
the public host declarations, report layout and AK820 callback implementation.

Actual hashes match the probe note:

| File | SHA256 |
| --- | --- |
| Control `host.c` | `74a7c83be7e335e3c6c1eeca24538758dcd6ba52d335b138b478e0a4b9ee22ad` |
| Candidate `host.c` | `e8392d708749fa32b5b1fec3123ca1eb604ece1ef1c4b4ae5d18dace0d09b65c` |
| Control IHX | `ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837` |
| Candidate IHX | `ce0f5cdbed5e73f64006742364b282c5f6cf53c1f3e77037581783af9096cd42` |

The control source matches the canonical build manifest and the current
production source at review time. The control IHX matches the canonical
`rc6-optimized-breathing-20261023` IHX. The link script uses frozen full-build
assembly for the control and replaces only host assembly for the candidate;
it stops unless the control IHX reproduces the baseline exactly. Thus the
linked control is the frozen baseline, not the separately compiled control
object. Both translation-unit compile logs are empty.

Independent parsing of the saved IHX files gives CODE 39,432 -> 39,402 bytes,
main CODE 37,573 -> 37,543 and low CODE 1,859 -> 1,859. The raw object CSEG
sizes are hexadecimal `297` -> `279`, or 663 -> 633 bytes. The candidate
memory report gives XRAM 2,071 bytes and stack capacity 152 bytes, agreeing
with the reports. The supported saving is 30 linked CODE bytes against the
combined baseline. It must not be added to overlapping probe savings.

## Behavior and ABI

The actual diff moves only the common null-driver/report/callback tail into
a private helper. Public declarations and `host_driver_t` are unchanged.
Both wrappers retain their own duplicate check and last-usage update before
the helper. Null-driver requests still update state, restoring the driver
still suppresses an unchanged request, and zero usage still sends a release.
System ID 3 and consumer ID 4 remain separate, with complete 16-bit usage.

The Bluetooth consumer branch still runs after its state update and before
the helper. System sending gains no Bluetooth branch. Other-board pointer
declarations remain generic. Other-board behavior was inspected in source;
it was not built or tested.

Generated AK820 assembly keeps the private XDATA driver pointer, reads the
same callback table slot at offset six and passes the report as a generic
pointer with tag zero. Both wrappers tail-jump to the helper. The existing
AK820 table is the mutable `ch555_usb_stack_driver`; this change introduces
no new table, cast or registration path. The AK820 callback consumes the
report synchronously and does not retain its pointer or reenter host send.
The helper uses shared static XDATA storage under this SDCC model; no new
claim of recursive or interrupt-safe host sending is made. The existing
AK820 interrupt path does not call these host send wrappers.

The separate pending system/consumer bits and system-first retry/release
order in the AK820 protocol task are untouched. No EEPROM code, storage
format, USB descriptor, report layout or wire format changes in this diff.

## Evidence limits and closure

Both saved linked CPU fixtures contain 25 passing assertions, with actual
values equal to expected values and the correct image hashes. They cover
pointer tags, IDs, full usage, independent state, releases, null updates and
restored-driver duplicate suppression. Both observed peak SP 111, eight
bytes above the fixture's initial stack. This is a measured path, not a
bound for interrupt nesting, recursive callbacks or all firmware paths.

The probe note accurately separates source, linked artifacts, CPU evidence
and device behavior. It still says independent review is pending; integration
should replace that sentence with a link to this completed review. That is
the only documentation follow-up, not a code blocker. No code finding needs
closure or retesting before the exact candidate is integrated.

No live protocol, durable storage, USB timing, physical keys, encoder,
Bluetooth device or installed firmware was verified here. Integration must
keep those limits and must not treat this GO as hardware authorization.
