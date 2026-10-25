#!/bin/sh
# SPDX-License-Identifier: GPL-2.0-or-later
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
toolchains=${AK820_TOOLCHAINS:-/home/danil/ChatGPT/ak820-beta1/toolchains}
image=${AK820_TEST_IMAGE:-ak820-nkro-study-env:local}
out=$(mktemp -d)
chmod 777 "$out"
trap 'rm -rf "$out"' EXIT HUP INT TERM
docker run --rm -v "$root:/src:ro" -v "$toolchains:/toolchains:ro" -v "$out:/out" "$image" sh -eu -c '
 export PATH=/toolchains/sdcc-4.6.0/bin:$PATH
 cd /out
 inc=/src/qmk-8051-ak820/keyboards/ajazz/ak820
 gcc -O2 -I"$inc" /src/tests/ak820_crc/native.c "$inc/ak820_crc.c" -o native
 ./native
 sdcc -mmcs51 --model-large -I"$inc" -c "$inc/ak820_crc.c"
 grep "^A CSEG " ak820_crc.rel
 sdcc -mmcs51 --model-large -I"$inc" /src/tests/ak820_crc/cpu.c ak820_crc.rel -o cpu.ihx
 printf "step 50000000\ndump xram 0x2000 0x2003\nquit\n" | timeout 120 s51 -t 8051 -c - cpu.ihx > cpu.log || { cat cpu.log; exit 1; }
 cat cpu.log
 grep -Eq "0x2000 +a5 00 04 a5" cpu.log
 echo "PASS: emitted 8051 CRC versus C reference, 1024 cases, lengths 0..255, ABI and canaries"
 sdcc --version > compiler.txt
 python3 /src/tests/ak820_crc/report.py
'
cp "$out/result.json" "${AK820_CRC_RESULT:-$root/tests/ak820_crc/latest-result.json}"
