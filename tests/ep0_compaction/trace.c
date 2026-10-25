/* Included after the production USB fixture; compares visible state at IRQ edges. */
static uint32_t trace_hash = 2166136261u;
static void byte_hash(uint8_t v) { trace_hash = (trace_hash ^ v) * 16777619u; }
static void trace(void) {
    for (unsigned j = 0; j < sizeof(test_mmio); ++j) byte_hash(test_mmio[j]);
    byte_hash(D0SetupReqCode); byte_hash(D0SetupLen); byte_hash(D0SetupLen >> 8);
    byte_hash(D0UsbConfig); byte_hash(USB_EnumStatus); byte_hash(USB_SleepStatus);
    byte_hash(control_phase); byte_hash(output_kind); byte_hash(output_report_id);
    byte_hash(control_zlp); byte_hash(raw_state); byte_hash(keyboard_protocol);
    byte_hash(keyboard_idle); byte_hash(keyboard_reset); byte_hash(KB_USB_SetReport);
    for (unsigned j = 0; j < sizeof(raw_buffer); ++j) byte_hash(raw_buffer[j]);
}
int main(void) {
    original_main();
    uint8_t data[64];
    static const uint8_t types[] = {0,1,2,0x21,0x80,0x81,0x82,0xa1};
    static const uint16_t values[] = {0,1,2,127,128,255,256,0x100,0x200,0x206,0x300,0x2100,0x2200,0xffff};
    static const uint16_t indexes[] = {0,1,2,3,0x80,0x81,0x82,0x83,0x84,0x100,0x101,0x409,0xffff};
    static const uint16_t lengths[] = {0,1,2,8,31,32,33,63,64,65,255,256,65535};
    unsigned cases = 0;
    for (unsigned field = 0; field < 2; ++field)
    for (unsigned word = 0; word < 65536; ++word) {
        fresh();
        D0UsbConfig = (word & 1); USB_EnumStatus = D0UsbConfig;
        raw_state = (word >> 1) % 8;
        uint16_t value = field ? values[(word >> 3) % (sizeof(values)/2)] : word;
        uint16_t index = field ? word : indexes[(word >> 3) % (sizeof(indexes)/2)];
        setup(types[(word >> 5) % sizeof(types)], (word >> 8) % 12, value, index,
              lengths[(word >> 2) % (sizeof(lengths)/2)]);
        trace();
        for (unsigned j = 0; j < sizeof(data); ++j) data[j] = word + j;
        if (word & 1) { out(data, (word >> 2) % 65, false); trace(); }
        if (word & 2) { out(data, (word >> 3) % 65, true); trace(); }
        for (unsigned j = 0; j < 4; ++j) { in(0); trace(); }
        reset(); trace();
        ++cases;
    }
    printf("trace %u %08x\n",cases,trace_hash);
}
