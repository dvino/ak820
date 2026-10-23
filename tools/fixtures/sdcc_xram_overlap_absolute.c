/* Own compile/link-only fixture. Never execute or flash this memory probe. */
#ifndef ORDINARY_SIZE
#define ORDINARY_SIZE 0x1000
#endif
volatile __xdata unsigned char ordinary[ORDINARY_SIZE];
volatile __xdata __at(0x1000) unsigned char absolute_fifo[64];
void main(void) {
    ordinary[0] = 1;
    ordinary[ORDINARY_SIZE - 1] = 2;
    absolute_fifo[0] = 3;
    for (;;) { }
}
