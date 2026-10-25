/* SPDX-License-Identifier: GPL-2.0-or-later */
#include "ak820_crc.h"
__xdata __at(0x2000) volatile uint8_t result;
__xdata __at(0x2001) volatile uint16_t cases;
__xdata __at(0x2003) volatile uint8_t abi_result;
__xdata __at(0x2100) uint8_t storage[257];
static uint16_t reference_step(uint16_t crc, uint8_t byte) {
    uint8_t bit;
    crc^=(uint16_t)byte<<8;
    for(bit=0;bit<8;bit++) crc=crc&0x8000 ? (crc<<1)^0x1021 : crc<<1;
    return crc;
}
static uint8_t abi_check(void) __naked {
    __asm
        push 0x00
        push 0x01
        push 0x06
        push 0x07
        mov r0,#0x12
        mov r1,#0x34
        mov r6,#0x56
        mov r7,#0x78
        mov dptr,#_ak820_crc16_PARM_2
        clr a
        movx @dptr,a
        mov dptr,#0xffff
        lcall _ak820_crc16
        mov a,dpl
        cjne a,#0xff,00001$
        mov a,dph
        cjne a,#0xff,00001$
        cjne r0,#0x12,00001$
        cjne r1,#0x34,00001$
        mov dpl,#0
        sjmp 00002$
00001$:
        mov dpl,#1
00002$:
        pop 0x07
        pop 0x06
        pop 0x01
        pop 0x00
        ret
    __endasm;
}
void done(void) __naked {
    __asm
00001$:
        sjmp 00001$
    __endasm;
}
void main(void) {
    uint16_t n, expected;
    uint8_t pattern,i;
    result=0; cases=0; abi_result=0;
    if(abi_check()) {result=3;done();}
    abi_result=0xa5;
    storage[0]=0xa5; storage[256]=0x5a;
    for(pattern=0;pattern<4;pattern++) {
        for(i=0;i<255;i++) storage[i+1]=pattern==0 ? 0 : pattern==1 ? 255 : pattern==2 ? i : (i*73u+19u);
        expected=0xffff;
        for(n=0;n<256;n++) {
            if(ak820_crc16(storage+1,(uint8_t)n)!=expected) {result=1;done();}
            if(storage[0]!=0xa5 || storage[256]!=0x5a) {result=2;done();}
            ++cases;
            if(n<255) expected=reference_step(expected,storage[n+1]);
        }
    }
    if(cases!=1024) {result=4;done();}
    result=0xa5;
    done();
}
