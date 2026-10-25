/* Exhaust all 16-bit words for the transformed full14 SETUP predicates.
 * This is a scalar CPU oracle, not execution of the production USB service.
 * Full14 interface constants: keyboard=0, raw=1, shared=2, total=3. */
#include <stdint.h>
#ifndef __SDCC_mcs51
#include <assert.h>
#include <stdio.h>
#define __xdata
#define __at(x)
#endif
volatile __xdata __at(0x2000) uint8_t result;
volatile __xdata __at(0x2001) uint16_t completed;
static uint16_t before(uint16_t word) {
    return (!word) | ((word <= 1) << 1) | ((word <= 127) << 2) |
        ((word == 0x0200) << 3) | ((word == 0x0206) << 4) |
        ((word == 0x0300) << 5) | ((word == 1) << 6) |
        ((word == 0) << 7) | ((word == 1) << 8) | ((word == 2) << 9) |
        (((word >> 8) == 1) << 10) | ((!(word >> 8)) << 11);
}
static uint16_t after(uint16_t word) {
    uint8_t lo = word, hi = word >> 8;
    uint8_t valid = word < 3;
    return (!(lo | hi)) | ((!hi && lo <= 1) << 1) | ((!hi && lo <= 127) << 2) |
        ((hi == 2 && !lo) << 3) | ((hi == 2 && lo == 6) << 4) |
        ((hi == 3 && !lo) << 5) | ((!hi && lo == 1) << 6) |
        ((valid && lo == 0) << 7) | ((valid && lo == 1) << 8) | ((valid && lo == 2) << 9) |
        ((hi == 1) << 10) | ((!hi) << 11);
}
#ifdef __SDCC_mcs51
static void stop(void) __naked { __asm 00001$: sjmp 00001$ __endasm; }
void main(void) {
#else
int main(void) {
#endif
    uint16_t word = 0;
    result = 0; completed = 0;
    do {
        if (before(word) != after(word)) {
            result = 1;
#ifdef __SDCC_mcs51
            stop();
#else
            assert(0);
#endif
        }
        ++completed;
    } while (++word);
    result = 0xa5;
#ifdef __SDCC_mcs51
    stop();
#else
    puts("PASS: 65536 exhaustive scalar SETUP predicate words");
    return 0;
#endif
}
