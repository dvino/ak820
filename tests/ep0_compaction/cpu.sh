#!/bin/sh
# Run inside the pinned measurement container with writable output cwd.
set -eu
export PATH=/toolchains/sdcc-4.6.0/bin:$PATH
source_root=/home/danil/ChatGPT/ak820-max
cc -O2 -fsanitize=address,undefined "$source_root/tests/ep0_compaction/predicates.c" -o predicates-native
ASAN_OPTIONS=detect_leaks=0 ./predicates-native
sdcc -mmcs51 --model-large --opt-code-size "$source_root/tests/ep0_compaction/predicates.c" -o predicates.ihx
printf 'step 120000000\ndump xram 0x2000 0x2002\nquit\n' | timeout 60 s51 -t 8051 -c - predicates.ihx > predicates-cpu.log
cat predicates-cpu.log
grep -Eq '0x2000 +a5 00 00' predicates-cpu.log
