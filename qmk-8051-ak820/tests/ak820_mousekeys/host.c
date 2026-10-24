/* SPDX-License-Identifier: GPL-2.0-or-later */
#define AK820_MOUSEKEY_HOST_TEST
#include "../../keyboards/ajazz/ak820/ak820_mousekey.c"
#include <assert.h>
#include <stdio.h>
static uint16_t clock_ms;
static bool ready = true;
static unsigned attempts, sent;
static report_mouse_t last;
uint16_t timer_read(void) { return clock_ms; }
bool ak820_usb_try_send(uint8_t ep, const uint8_t *p, uint8_t n) {
    assert(ep == 2 && n == sizeof(last)); ++attempts;
    if (!ready) return false;
    last = *(const report_mouse_t *)p; ++sent; return true;
}
static void press(uint8_t code) { mousekey_on(code); mousekey_send(); }
static void release(uint8_t code) { mousekey_off(code); mousekey_send(); }
static void tick(uint16_t t) { clock_ms=t; mousekey_task(); }
static void clean(void) { ready=true; mousekey_clear(); mousekey_send(); attempts=sent=0; }
int main(void) {
    const uint8_t codes[]={0xcd,0xce,0xcf,0xd0,0xd9,0xda,0xdb,0xdc};
    const int8_t vectors[][4]={{0,-8,0,0},{0,8,0,0},{-8,0,0,0},{8,0,0,0},{0,0,1,0},{0,0,-1,0},{0,0,0,-1},{0,0,0,1}};
    for(unsigned i=0;i<8;i++) { clean(); press(codes[i]); assert(sent==1); assert(last.x==vectors[i][0]&&last.y==vectors[i][1]&&last.v==vectors[i][2]&&last.h==vectors[i][3]); release(codes[i]); assert(sent==1); }
    clean(); clock_ms=100; press(0xd0); tick(119); assert(sent==1); tick(120); assert(sent==2); tick(1000); assert(sent==3); tick(1000); assert(sent==3);
    press(0xcd); assert(last.x==0&&last.y==-8); tick(1020); assert(last.x==8&&last.y==-8);
    press(0xcf); assert(sent==5); tick(1040); assert(last.x==0&&last.y==-8); release(0xcd); tick(1060); assert(sent==6); release(0xcf); tick(1080); assert(last.x==8);
    clean(); clock_ms=200; press(0xd9); tick(279); assert(sent==1); tick(280); assert(sent==2);
    clean(); clock_ms=65530; press(0xd0); tick(13); assert(sent==1); tick(14); assert(sent==2);
    clean(); press(0xd0); unsigned before=sent; press(0xd1); assert(sent==before+1&&last.buttons==1&&last.x==0); tick(34); assert(last.buttons==1&&last.x==8); release(0xd1); assert(last.buttons==0&&last.x==0);
    for(uint8_t b=0xd1;b<=0xd5;b++) { clean(); press(b); assert(last.buttons==(1u<<(b-0xd1))); release(b); assert(last.buttons==0); }
    clean(); press(0xd1); ready=false; release(0xd1); assert(accepted_buttons==1&&buttons==0); unsigned failures=attempts; tick(35); assert(attempts==failures+1); ready=true; tick(36); assert(last.buttons==0&&accepted_buttons==0);
    clean(); press(0xd1); ready=false; mousekey_clear(); mousekey_send(); ready=true; tick(37); assert(last.buttons==0);
    clean(); clock_ms=100; press(0xd0); ready=false; tick(120); tick(200); ready=true; tick(201); assert(sent==1); tick(220); assert(sent==2&&last.x==8);
    before=sent; for(uint8_t c=0xd6;c<=0xdf;c++) if(c<0xd9||c>0xdc) {press(c);release(c);} assert(sent==before); tick(239); assert(sent==before); tick(240); assert(sent==before+1);
    puts("PASS: real compact Mouse Keys C: directions, cadence, wrap, gaps, opposites, drag, five buttons, clear, busy retry, unsupported keys");
}
