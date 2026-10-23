import os
import random


def main():
    fixed = os.environ.get("AK820_BUILD_ID")
    build_id = int(fixed, 0) if fixed is not None else random.randrange(0, 2 ** 24 - 1)
    if not 0 <= build_id < 2 ** 24:
        raise ValueError("BUILD_ID must fit in the Vial 24-bit EEPROM magic")
    print("#define BUILD_ID ((uint32_t)0x{:08X})".format(build_id))


if __name__ == "__main__":
    main()
