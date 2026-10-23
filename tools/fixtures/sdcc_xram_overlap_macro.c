/* Own compile/link-only fixture, modeling the fixed pointer style of CH555. */
#ifndef ORDINARY_SIZE
#define ORDINARY_SIZE 0x1000
#endif
volatile __xdata unsigned char ordinary[ORDINARY_SIZE];
#define FIXED_FIFO ((__xdata volatile unsigned char *)0x1000)
void main(void) {
    ordinary[0] = 1;
    ordinary[ORDINARY_SIZE - 1] = 2;
    FIXED_FIFO[0] = 3;
    for (;;) { }
}
