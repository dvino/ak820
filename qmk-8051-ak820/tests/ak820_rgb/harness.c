/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#define AK820_BOARD
#define USE_CIE1931_CURVE
#define __xdata
#define PROGMEM
#define pgm_read_byte(p) (*(const uint8_t *)(p))
#define MATRIX_ROWS 16
#define MATRIX_COLS 8
#define RGB_MATRIX_LED_COUNT 82
#define RGB_MATRIX_MAXIMUM_BRIGHTNESS 160
#define RGB_MATRIX_DEFAULT_MODE RGB_MATRIX_SOLID_COLOR
#define RGB_MATRIX_DEFAULT_VAL 80
#define RGB_MATRIX_DEFAULT_SPD 96
#define RGB_MATRIX_LED_FLUSH_LIMIT 16
#define LED_FLAG_ALL 255
#define LED_FLAG_KEYLIGHT 4
#define EECONFIG_RGB_MATRIX ((void *)0)
enum { RGB_MATRIX_NONE, RGB_MATRIX_SOLID_COLOR, RGB_MATRIX_BREATHING,
       RGB_MATRIX_CYCLE_ALL, RGB_MATRIX_CYCLE_LEFT_RIGHT, RGB_MATRIX_VIALRGB_DIRECT,
       RGB_MATRIX_SOLID_REACTIVE_SIMPLE, RGB_MATRIX_EFFECT_MAX };
typedef struct { uint8_t h,s,v; } HSV;
typedef struct { uint8_t r,g,b; } RGB;
typedef uint8_t led_flags_t;
typedef union { uint64_t raw; struct __attribute__((packed)) { uint8_t enable:2, mode:6; HSV hsv; uint8_t speed,flags; }; } rgb_config_t;
static uint16_t now;
static uint16_t timer_read(void) { return now; }
static uint16_t timer_elapsed(uint16_t then) { return (uint16_t)(now - then); }
static uint8_t eeprom[8];
static void eeprom_update_block(const void *p, void *a, unsigned n) { (void)a; memcpy(eeprom,p,n); }
static void eeprom_read_block(void *p, const void *a, unsigned n) { (void)a; memcpy(p,eeprom,n); }
static RGB output[82];
static void init(void) {}
static void set_color(int i,uint8_t r,uint8_t g,uint8_t b) { output[i]=(RGB){r,g,b}; }
static void set_all(uint8_t r,uint8_t g,uint8_t b) { for(int i=0;i<82;++i) set_color(i,r,g,b); }
static void flush(void) {}
static struct { void (*init)(void); void (*set_color)(int,uint8_t,uint8_t,uint8_t);
    void (*set_color_all)(uint8_t,uint8_t,uint8_t); void (*flush)(void); }
    rgb_matrix_driver = {init,set_color,set_all,flush};
HSV g_direct_mode_colors[82];
static const uint8_t ak820_rgb_slots[82] = /* SLOT MAP */;
static const struct { uint8_t x,y; } ak820_led_points[82];
/* TABLE */
/* COLOR */
/* REFERENCE TABLE */
/* REFERENCE COLOR */
/* RGB */
static void frame(unsigned elapsed) {
    now += elapsed;
    for(unsigned i=0;i<11;++i) rgb_matrix_task();
}
static bool lit(unsigned i) { return output[i].r || output[i].g || output[i].b; }
static void breathing(void) {
    unsigned seen[256] = {0}, old_seen[256] = {0};
    unsigned previous = 0, first = 0, max_step = 0, max_error = 0;
    unsigned old_previous = 0, old_first = 0, old_max_step = 0, color_max_error = 0;
    rgb_matrix_set_suspend_state(false);
    rgb_matrix_enable_noeeprom();
    rgb_matrix_mode_noeeprom(RGB_MATRIX_BREATHING);
    rgb_matrix_sethsv_noeeprom(0,255,160);
    rgb_matrix_set_speed_noeeprom(224); /* Exactly one phase unit per frame. */
    phase = 0;
    for (unsigned i = 0; i < 256; ++i) {
        frame(16);
        unsigned value = (160u * sine8(frame_phase - 64)) >> 8;
        unsigned actual = output[0].r;
        unsigned old_actual = CIE1931_CURVE[value >> 3];
        unsigned reference = reference_cie[value];
        unsigned error = actual > reference ? actual - reference : reference - actual;
        if (error > max_error) max_error = error;
        seen[actual] = old_seen[CIE1931_CURVE[value >> 3]] = 1;
        for (unsigned led = 0; led < 82; ++led) {
            assert(output[led].r == actual && output[led].g == 0 && output[led].b == 0);
        }
        if (!i) { first = actual; old_first = old_actual; }
        else {
            unsigned step = actual > previous ? actual - previous : previous - actual;
            if (step > max_step) max_step = step;
            unsigned old_step = old_actual > old_previous ? old_actual - old_previous : old_previous - old_actual;
            if (old_step > old_max_step) old_max_step = old_step;
        }
        previous = actual;
        old_previous = old_actual;
    }
    unsigned wrap_step = previous > first ? previous - first : first - previous;
    unsigned old_wrap_step = old_previous > old_first ? old_previous - old_first : old_first - old_previous;
    if (old_wrap_step > old_max_step) old_max_step = old_wrap_step;
    assert(wrap_step <= 2 && max_step <= 2 && max_error <= 2);
    assert(old_max_step > max_step);
    unsigned levels = 0, old_levels = 0;
    for (unsigned i = 0; i < 256; ++i) { levels += seen[i]; old_levels += old_seen[i]; }
    assert(levels > old_levels * 2);
    /* Check colored/grayscale frames, low brightness and all speed extremes.
     * Compare against the independent historical full-CIE implementation. */
    static const uint8_t hues[] = {0,42,85,128,170,213};
    static const uint8_t saturations[] = {0,128,255};
    static const uint8_t values[] = {0,8,80,160};
    static const uint8_t speeds[] = {0,96,224,255};
    for (unsigned h = 0; h < sizeof(hues); ++h)
    for (unsigned s = 0; s < sizeof(saturations); ++s)
    for (unsigned v = 0; v < sizeof(values); ++v)
    for (unsigned speed = 0; speed < sizeof(speeds); ++speed) {
        rgb_matrix_sethsv_noeeprom(hues[h],saturations[s],values[v]);
        rgb_matrix_set_speed_noeeprom(speeds[speed]);
        phase = 0;
        now = 65520; /* Exercise the 16-bit timer wrap. */
        frame_at = now;
        for (unsigned tick = 0; tick < 2048; ++tick) {
            frame(16);
            uint8_t value = ((unsigned)values[v] * sine8(frame_phase - 64)) >> 8;
            RGB reference = rc4_hsv_to_rgb_impl((HSV){hues[h],saturations[s],value},true);
            const uint8_t *a = (void *)&output[0], *b = (void *)&reference;
            for (unsigned channel = 0; channel < 3; ++channel) {
                unsigned error = a[channel] > b[channel] ? a[channel] - b[channel] : b[channel] - a[channel];
                if (error > color_max_error) color_max_error = error;
                assert(error <= 2);
            }
            assert(!memcmp(&output[0], &output[81], sizeof(RGB)));
        }
    }
    printf("PASS breathing: %u levels (previous %u), phase step %u (previous %u), red full-CIE error %u, color-matrix error %u; ",
           levels, old_levels, max_step, old_max_step, max_error, color_max_error);
}
static void hit(unsigned i) { process_rgb_matrix(ak820_rgb_slots[i]>>3,ak820_rgb_slots[i]&7,true); }
static void reactive(void) {
    rgb_matrix_set_suspend_state(false);
    rgb_matrix_enable_noeeprom();
    rgb_matrix_mode_noeeprom(RGB_MATRIX_SOLID_COLOR);
    rgb_matrix_mode_noeeprom(RGB_MATRIX_SOLID_REACTIVE_SIMPLE);
    rgb_matrix_sethsv_noeeprom(0,255,160);
    rgb_matrix_set_speed_noeeprom(0);
}
int main(void) {
    assert(sizeof(rgb_config_t)==8);
    rgb_matrix_init();
    breathing();
    reactive(); frame(16);
    for(unsigned i=0;i<82;++i) assert(!lit(i));
    /* Every electrical slot; only physical LED slots can produce light. */
    for(unsigned slot=0;slot<128;++slot) {
        reactive(); process_rgb_matrix(slot>>3,slot&7,true); frame(16);
        for(unsigned i=0;i<82;++i) assert(lit(i)==(ak820_rgb_slots[i]==slot));
    }
    reactive(); process_rgb_matrix(255,255,true); frame(16);
    for(unsigned i=0;i<82;++i) assert(!lit(i));
    for(unsigned band=0;band<4;++band) {
        reactive(); rgb_matrix_set_speed_noeeprom(band*64); hit(0); frame(16);
        unsigned duration=2048>>band;
        unsigned previous=output[0].r;
        for(unsigned t=16;t<duration+16;t+=16) {
            frame(16); assert(output[0].r<=previous); previous=output[0].r;
        }
        assert(!lit(0));
    }
    reactive(); hit(0); frame(512); hit(81); frame(16);
    assert(lit(0)&&lit(81));
    process_rgb_matrix(0,0,false); frame(16); assert(lit(0)&&lit(81));
    frame(1800); assert(!lit(0)&&lit(81));
    hit(81); frame(512); assert(lit(81)); frame(2048); assert(!lit(81));
    reactive(); now=65520; clear_reactive(); hit(0); frame(32); assert(lit(0));
    frame(2048); assert(!lit(0));
    reactive(); hit(0); rgb_matrix_disable_noeeprom(); frame(16); assert(!lit(0));
    rgb_matrix_enable_noeeprom(); frame(16); assert(!lit(0));
    hit(0); rgb_matrix_set_suspend_state(true); assert(!lit(0));
    rgb_matrix_set_suspend_state(false); frame(16); assert(!lit(0));
    hit(0); rgb_matrix_mode_noeeprom(RGB_MATRIX_SOLID_COLOR); frame(16); assert(lit(0));
    rgb_matrix_mode_noeeprom(RGB_MATRIX_SOLID_REACTIVE_SIMPLE); frame(16); assert(!lit(0));
    hit(0); frame(16); assert(lit(0));
    rgb_matrix_enable_noeeprom(); rgb_matrix_mode_noeeprom(RGB_MATRIX_SOLID_REACTIVE_SIMPLE);
    frame(16); assert(lit(0)); /* Reapplying an unchanged mode is harmless. */
    eeconfig_update_rgb_matrix(); rgb_matrix_reload_from_eeprom(); frame(16); assert(!lit(0));
    reactive(); hit(0); frame(16); assert(lit(0));
    rgb_matrix_toggle_noeeprom(); frame(16); assert(!lit(0));
    rgb_matrix_toggle_noeeprom(); frame(16); assert(!lit(0));
    g_direct_mode_colors[81]=(HSV){0,255,160};
    rgb_matrix_mode_noeeprom(RGB_MATRIX_VIALRGB_DIRECT); frame(16);
    assert(!lit(0)&&lit(81));
    unsigned max_error=0;
    assert(CIE1931_CURVE[0]==0 && CIE1931_CURVE[31]==255);
    for(unsigned i=1;i<32;++i) assert(CIE1931_CURVE[i]>=CIE1931_CURVE[i-1]);
    for(unsigned h=0;h<256;++h) for(unsigned s=0;s<256;++s) for(unsigned v=0;v<256;++v) {
        HSV hsv={h,s,v}; RGB a; hsv_to_rgb_into(hsv,true,&a);
        unsigned quantized=v==255 ? 255 : (v>=248 ? 255 : v&~7u);
        RGB b=rc4_hsv_to_rgb_impl((HSV){h,s,quantized},true);
        assert(!memcmp(&a,&b,sizeof(a)));
        RGB full=rc4_hsv_to_rgb_impl(hsv,true);
        if(v<=160) {
            const uint8_t *x=(void *)&a,*y=(void *)&full;
            for(unsigned c=0;c<3;++c) { unsigned e=x[c]>y[c]?x[c]-y[c]:y[c]-x[c]; if(e>max_error) max_error=e; }
        }
    }
    assert(max_error<=8);
    printf("PASS reactive slot/chord/timing/wrap/transitions/Direct; 16777216 compact HSV cases; max channel error v<=160: %u\n",max_error);
}
