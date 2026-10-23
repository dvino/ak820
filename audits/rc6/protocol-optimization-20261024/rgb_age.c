#include <stdint.h>
#include <assert.h>
#include <stdio.h>
int main(void) {
    unsigned cases=0;
    for (unsigned ticks=0;ticks<4096;++ticks) {
        uint8_t decay=ticks>255?255:(uint8_t)ticks;
        for(unsigned age=0;age<256;++age) {
            uint8_t control=ticks>=age?0:age-ticks;
            uint8_t candidate=decay>=age?0:age-decay;
            assert(control==candidate); ++cases;
        }
    }
    printf("PASS: %u RGB decay comparisons; every uint8 age and every 16-bit elapsed >> 4 tick count.\n",cases);
}
