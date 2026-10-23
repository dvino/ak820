#include <stdint.h>
#include <stdbool.h>
/* Same fields/order as keyboard.h/action.h with NO_ACTION_TAPPING and
 * REPEAT_KEY_ENABLE, as used by the current AK820 build. */
typedef struct { uint8_t col, row; } keypos_t;
typedef enum { TICK_EVENT=0, KEY_EVENT=1, ENCODER_CW_EVENT=2,
               ENCODER_CCW_EVENT=3, COMBO_EVENT=4 } event_type_t;
typedef struct { keypos_t key; uint16_t time; event_type_t type; bool pressed; } event_t;
typedef struct { event_t event; uint16_t keycode; } record_t;
typedef struct { bool interrupted:1; bool reserved2:1; bool reserved1:1;
                 bool reserved0:1; uint8_t count:4; } tap_t;
typedef struct { bool a; } box_t;
volatile int input;
volatile __xdata __at(0x8000) uint8_t results[32];
box_t __data near_box;
box_t __xdata far_box;
record_t __xdata record;
tap_t __xdata tap;
int bar(void) { return input; }
void near_store(box_t __data *p) { p->a = bar() > 0; }
void xdata_store(box_t __xdata *p) { p->a = bar() > 0; }
void generic_store(box_t *p) { p->a = bar() > 0; }
bool comparison_return(void) { return bar() > 0; }
void record_store(record_t *p) { p->event.pressed = bar() > 0; }
void record_constant(record_t *p, bool pressed) { p->event.pressed = pressed; }
void bitfield_store(tap_t __xdata *p) { p->interrupted = bar() > 0; }
void main(void) {
    uint8_t i;
    for (i=0; i<2; i++) {
        input = i ? 1 : -1;
        near_box.a = !i; near_store(&near_box); results[i*8] = near_box.a;
        far_box.a = !i; xdata_store(&far_box); results[i*8+1] = far_box.a;
        far_box.a = !i; generic_store(&far_box); results[i*8+2] = far_box.a;
        near_box.a = !i; generic_store(&near_box); results[i*8+3] = near_box.a;
        results[i*8+4] = comparison_return();
        record.event.pressed = !i; record_store(&record); results[i*8+5] = record.event.pressed;
        record_constant(&record, i); results[i*8+6] = record.event.pressed;
        tap.interrupted = !i; tap.count=9; bitfield_store(&tap);
        results[i*8+7] = tap.interrupted | (tap.count << 1);
    }
    results[31]=0xa5;
    while (1) {}
}
