
## 2026-10-31 23:45 integration state
- E25 xmod integrated into build recipe: configure_firmware.py release profiles now pass --tail-share-xmod (after --tail-share).
- Integration copy /home/agent/ak820-integration-20261031, combined build int5: endpoint 0xc6a5, code_bytes 40405, ihx 3e5b53ff..., canonical contract verified, xmod replay pass, safety gate PASS (stack 165/183 margin 18, unresolved_roots []).
- Canonical configure_firmware build+qualify run int6-main (primary): build OK (0xc6a5), qualify suite failures split: (a) environmental — docker --tmpfs /tmp defaults to noexec, native test binaries EACCES; fixed by --tmpfs /tmp:rw,nosuid,nodev,exec (ak820_usb PASS with fix); (b) real — uncommitted backup/TOCTOU work incomplete: tools/installer 30F+17E, device_protocol 3F+3E, package 1F. Worker del_mvx1r6zv_ulg1 completing implementation.
- Next: after worker green, re-run qualify on int6-main with exec tmpfs; then ledger update, reviews, docs, CI, release.

## 2026-11-01 00:07 review + fixes
- E25 xmod review del_mvx1yw7r_r1te: ACCEPT WITH CONDITIONS. Blocking: (1) match key lacks assembled bytes — immediate operands with per-module equates could merge different constants (current image benign: _raw_buffer single definition); fixed — key now includes item bytes hex. (2) control-SFR alias gate per-module only; fixed — global alias set (all-module equate scan, numeric 0x80-0xff control range + non-numeric equates) threaded into eligibility. Minor: docstring clarified (globl declared OR defined-in-exported-module); note: canonical-contract has no xmod term (not needed; replay branches on report key). Applied to primary qmk-8051-ak820/util/ak820_tailshare_xmod.py and synced to /home/agent/ak820-integration-20261031 and /home/agent/ak820-code-exp-25. Both rebuilt+replayed: int5 int6 0xc6a5 unchanged; gate-hardening changed NO group (sanity scripts: group dump identical).
- Ledger E25 status updated: applied to release main, endpoint 0xc754 -> 0xc6a5, review conditions closed.
- Worker del_mvx1r6zv_ulg1: package suite 90 OK, device_protocol 21 OK; installer tests in progress.
