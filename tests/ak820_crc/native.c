/* SPDX-License-Identifier: GPL-2.0-or-later */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "ak820_crc.h"
static uint16_t step(uint16_t c,uint8_t b) { c ^= (uint16_t)b<<8; for(unsigned k=0;k<8;k++) c=c&0x8000 ? (uint16_t)((c<<1)^0x1021):(uint16_t)(c<<1); return c; }
int main(void) {
 uint8_t b[255]; uint8_t seen[65536]={0}; unsigned transitions=0;
 for(unsigned a=0;a<65536;a++) {
  b[0]=a>>8;b[1]=a;
  uint16_t state=step(step(0xffff,b[0]),b[1]);
  if(seen[state]++) return 1;
  for(unsigned v=0;v<256;v++) { b[2]=v; if(ak820_crc16(b,3)!=step(state,v)) return 2; transitions++; }
 }
 uint32_t rng=0x820a55;
 for(unsigned n=0;n<256;n++) for(unsigned trial=0;trial<100;trial++) {
  uint16_t c=0xffff;
  for(unsigned i=0;i<n;i++){rng=rng*1664525u+1013904223u;b[i]=rng>>24;c=step(c,b[i]);}
  if(ak820_crc16(b,n)!=c) return 3;
 }
 if(ak820_crc16((const uint8_t*)"123456789",9)!=0x29b1) return 4;
 printf("PASS %u exhaustive transitions; 25600 random buffers lengths 0..255; known vector 29b1\n",transitions);
 return 0;
}
