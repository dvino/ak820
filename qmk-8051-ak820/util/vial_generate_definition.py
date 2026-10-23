#!/usr/bin/env python3
import sys
import json
import lzma
import argparse

def compress_definition(data, compact_xz=False):
    ordinary = lzma.compress(data)
    if not compact_xz:
        return ordinary
    # Keep the standard XZ container and CRC64 used by existing Vial clients.
    # Small JSON benefits from fewer literal/position contexts; keep the
    # ordinary encoding if a future, larger definition compresses better there.
    compact = lzma.compress(data, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64,
                            filters=[{"id": lzma.FILTER_LZMA2, "dict_size": 4096,
                                      "lc": 0, "lp": 0, "pb": 0,
                                      "mode": lzma.MODE_NORMAL, "nice_len": 273,
                                      "mf": lzma.MF_BT4, "depth": 0}])
    return min((ordinary, compact), key=len)

def main():
    parser = argparse.ArgumentParser(description="Generate a compressed Vial keyboard definition header")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--compact-xz", action="store_true", help="Choose the smaller of two compatible XZ/CRC64 encodings")
    args = parser.parse_args()

    with open(args.input, "r") as inf:
        data = inf.read()

    # minify json
    data = json.dumps(json.loads(data), separators=(',', ':')).strip()

    # compress
    data = compress_definition(data.encode("utf-8"), args.compact_xz)

    with open(args.output, "w") as outf:
        outf.write("#pragma once\n")
        outf.write("static const unsigned char keyboard_definition[] PROGMEM = {")
        arr = ["0x{:02X}".format(b) for b in data]
        outf.write(", ".join(arr))
        outf.write("};\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
