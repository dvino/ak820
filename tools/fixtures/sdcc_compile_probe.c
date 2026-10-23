/* Own offline toolchain fixture. No board drivers, peripherals or firmware flashing. */
typedef unsigned char u8;

__xdata volatile u8 probe_output[4];
__code const u8 probe_constants[4] = {3, 5, 8, 13};

u8 probe_generic_read(const u8 *source) {
    return *source;
}

void probe_generic_copy(u8 *destination, const u8 *source) {
    *destination = *source;
}

void main(void) {
    u8 local = 0x55;
    probe_generic_copy((u8 *)&probe_output[0], &probe_constants[0]);
    probe_output[1] = probe_generic_read(&local);
    probe_output[2] = probe_generic_read(&probe_constants[1]);
    probe_output[3] = probe_generic_read((const u8 *)&probe_output[0]);
}
