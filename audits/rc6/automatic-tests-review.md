# Automatic test review

The review was reopened after the root found that the original macro oracle
compared all durable macro bytes with a logical getter. Firmware hides old tail
bytes and an incomplete upload. This finding is closed: the final oracle uses
the published length and a zero tail, and rejects busy or invalid metadata.
An independent fixture covers a shortened stream with stale nonzero tail and
the all-zero getter during a busy upload. The initial 17-test pass is historical;
the final result and hashes below replace it.

Reviewed independently on 2026-10-23. Scope: the new device-test runner,
protocol adapter, offline fixtures, combined-runner discovery and English and
Russian testing instructions. No USB commands, settings writes, resets or
flashing were performed during this review.

The three new Python files pass review for offline use. The reviewer ran:

```sh
rtk proxy python -B -m unittest discover -s tools -p test_ak820_device_tests.py -v
```

All 19 tests passed in 6.054 seconds. These tests use an independent raw-packet
fixture whose getters read saved bytes. They do not validate a real controller.

Reviewed SHA256 values:

| File under `tools/` | SHA256 |
| --- | --- |
| `ak820_device_tests.py` | `62b029be8316ef36b3925ff1a23cb3499f9c982d1c0a2861b5bf702cde86b2f3` |
| `ak820_device_protocol.py` | `a361a55cf3939a5fbd4a9b068f42dbde9fa4677b934b9c8758ac56e300a9d986` |
| `test_ak820_device_tests.py` | `64e8ee39b4da3f0262d7d37394ef1ca27ba2b942bc0ae9c48927d9037f3f931f` |

The default command prints a plan without importing the adapter or HID. The
live path validates the exact approved release and personal session before
opening a device. It then checks live ROM identity, boot liveness, storage
status and the journal before settings tests. Missing fields and mismatched
builds fail closed. The offline tests cover missing approval and mixed session
build or CODE; some session checks use mocked validated inputs to avoid OEM
backup files.

The mapping oracle covers 83 keys on six layers and both directions of one
encoder on six layers: 498 key values and 12 encoder slots. Packet layouts,
byte order and encoder direction match the firmware source. Each optional
mapping round trip checks the ACK, ordinary getter and exact full NVM image
before one restoration. Missing ACK, RAM-only change, neighboring corruption,
stale getter, storage fault and failed restoration stop the sequence and leave
the pending change recorded. The runner catches failures and saves a report.

RGB tests restore the original RAM state, including an unsaved state, and
require durable NVM to stay unchanged. Macro writes and durable RGB save are
explicitly skipped. No unlock sequence is sent. The journal check correctly
requires an empty EF40 header while allowing retained EF00 journal data after
a completed transaction.

The English and Russian instructions keep host/CPU evidence separate from
live protocol, saved bytes and physical behavior. They describe the installed
encoder-write failure and prohibit a new live run on that faulted keyboard.
Physical switches, rotation signals, LED appearance, restart persistence and
electrical USB behavior remain untested by this suite.

Review closure: the initial binding-test gap was addressed with tests that
exercise the real binding function. The initial RGB round-trip coverage gap
was addressed with success and bad-readback cases. No blocking finding remains
in these three Python files. This review does not authorize a live run or a
flash. The linked CPU fault case has a separate verification record below.

The new `ineffective_erase_target` CPU case also passes review. It deliberately
models ineffective erase and OR-only programming; it does not claim that this
is the physical failure cause. The reviewer inspected the corrected source and
the author's targeted result at
`qmk-8051-ak820/.build/rc6-iap-target-replay-pass2-20261023/results.json`
(SHA256 `6885219cf2dc32afedd07b7fab43366501898ad3f0bc51aa00e951f401aa2ac6`).
That result uses IHX
`7c25096e59412afc7a4aa1c030a7038c4b5d469a253319ef712ce4244c91ffb9`.
It shows unchanged `00A9` after a requested `0000`, no setter ACK, retained
committed journal, failure stage 12 and replay failure stage 3. Replay is an
offline firmware test; the live runner does not attempt it. The author reports
11 earlier baseline cases passed separately. A completed aggregate run of all
12 cases was not repeated, and this review does not claim one.
