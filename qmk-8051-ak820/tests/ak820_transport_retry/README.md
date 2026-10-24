# AK820 pending HID reports

These tests cover a confirmed release-loss defect: a keyboard, NKRO, system or
consumer release can time out while its IN endpoint is still busy. QMK has
already updated its change detector, so that release is not sent again without
a backend retry. A pending report holds the latest desired state, while USB's
GET_REPORT snapshot continues to describe the last accepted publication.

```sh
python tests/ak820_transport_retry/run.py \
  --build-dir .build/rc5-local --s51 ../toolchains/sdcc-4.4.0/bin/s51 \
  --output-dir .build/rc5-local/transport-tests
python tests/ak820_transport_retry/host.py \
  --output-dir .build/rc5-local/transport-host-tests
```

The linked CPU suite covers ten cases: boot keyboard and NKRO releases,
consumer/system releases, independent pending report IDs on the shared
endpoint, latest-state replacement, reset, suspend/resume and configuration
guards. It supplies endpoint completion state in simulated MMIO; it does not
claim to emulate the physical SIE, host scheduling, USB timing or IRQ delivery.

The host ASan/UBSan test includes the production USB implementation and
verbatim backend/host bodies, with MMIO, timer and unrelated QMK hooks replaced
by fixtures. It checks 136 endpoint/state/length/EA combinations, independent
pending reports, accepted-versus-desired ownership and reset/suspend cleanup.
It also checks that a null driver blocks startup publication, while the fixed
AK820 transport dispatches directly when the driver marker is nonnull.
Repeated calls while busy must make zero `wait_us`/`wait_ms` calls, and the
atomic publication wrapper must preserve both initial EA values.

Candidate-3 is a negative control: eight of ten CPU cases fail. The two reset
and suspend controls already passed. The first atomic retry experiment also
includes the LED metadata optimization and exceeds the release CODE window by
19 bytes; its CPU results demonstrate behavior only. `within_release_code_windows`
records this distinction. A final bounded build must repeat the suite before
packaging. No test opens a physical device.

The active profile has no mouse reports. Relative mouse movement would require
a separate accumulation policy and is not covered by latest-state HID retries.
