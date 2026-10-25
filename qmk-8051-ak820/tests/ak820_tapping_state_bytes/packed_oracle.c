#define SOURCE_STATE_BYTES ((SOURCES * SOURCE_STATE_BITS + 7) / 8)
static uint8_t source_state[SOURCE_STATE_BYTES];
static uint8_t source_state_get(uint8_t id) {
    uint16_t bit = (uint16_t)id * SOURCE_STATE_BITS;
    uint8_t offset = bit & 7;
    uint16_t pair = source_state[bit >> 3];
    if (offset > 3) pair |= (uint16_t)source_state[(bit >> 3) + 1] << 8;
    return (pair >> offset) & SOURCE_STATE_MASK;
}
static void source_state_set(uint8_t id, uint8_t state) {
    uint16_t bit = (uint16_t)id * SOURCE_STATE_BITS;
    uint8_t byte = bit >> 3, offset = bit & 7;
    uint16_t pair = source_state[byte];
    uint16_t mask = SOURCE_STATE_MASK;
    if (offset > 3) {
        pair |= (uint16_t)source_state[byte + 1] << 8;
        mask <<= offset;
        pair = (pair & ~mask) | (((uint16_t)(state & SOURCE_STATE_MASK)) << offset);
        source_state[byte] = pair;
        source_state[byte + 1] = pair >> 8;
    } else {
        mask <<= offset;
        pair = (pair & ~mask) | (((uint16_t)(state & SOURCE_STATE_MASK)) << offset);
        source_state[byte] = pair;
    }
}
