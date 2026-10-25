#!/usr/bin/env python3
"""Compare the AK820 fastset helper with the frozen 09330ab implementation."""
import hashlib
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ROOT / "quantum/vialrgb.c"
BASE = "09330ab708e1eb3671571f63894c583e01743eef"


def extract(text):
    start = text.index("static void fast_set_leds(")
    opening = text.index("{", start)
    depth = 0
    for end in range(opening, len(text)):
        if text[end] == "{":
            depth += 1
        elif text[end] == "}":
            depth -= 1
            if depth == 0:
                return text[start : end + 1]
    raise ValueError("unclosed helper")


def extract_setter(text):
    start = text.index("void vialrgb_set_value(")
    opening = text.index("{", start)
    depth = 0
    for end in range(opening, len(text)):
        if text[end] == "{":
            depth += 1
        elif text[end] == "}":
            depth -= 1
            if depth == 0:
                return text[start : end + 1]
    raise ValueError("unclosed setter")


def harness(helper, setter, fastset_call):
    return r'''#include <stdint.h>
#include <stdio.h>
#include <string.h>
#define VIALRGB_BUFFER
#define AK820_BOARD
#define RGB_MATRIX_LED_COUNT 82
#define RGB_MATRIX_MAXIMUM_BRIGHTNESS 127
#define VIAL_RAW_EPSIZE 32
#define RGB_MATRIX_EFFECT_VIALRGB_DIRECT 1
#define vialrgb_set_mode 1
#define vialrgb_direct_fastset 2
typedef struct { uint8_t h, s, v; } HSV;
HSV g_direct_mode_colors[RGB_MATRIX_LED_COUNT + 2];
static void set_mode(uint16_t mode) { (void)mode; }
static void rgb_matrix_set_speed_noeeprom(uint8_t x) { (void)x; }
static void rgb_matrix_sethsv_noeeprom(uint8_t h,uint8_t s,uint8_t v) { (void)h;(void)s;(void)v; }
''' + helper + "\n#define FASTSET(p) " + fastset_call + r'''
''' + setter + r'''
int main(void) {
  uint8_t args[30], before[30];
  for (unsigned index=0; index<256; ++index) for (unsigned count=0; count<256; ++count) {
    memset(args, 0xA5, sizeof args); args[0]=(uint8_t)index; args[1]=(uint8_t)(index>>8); args[2]=(uint8_t)count;
    for (unsigned j=3; j<30; ++j) args[j]=(uint8_t)(j*37u+count);
    memcpy(before,args,sizeof args);
    for (unsigned k=0;k<RGB_MATRIX_LED_COUNT+2;++k) g_direct_mode_colors[k]=(HSV){0xD1,0xD2,0xD3};
    FASTSET(args);
    if (memcmp(args,before,sizeof args)) { fprintf(stderr,"packet mutation index=%u count=%u\\n",index,count); return 1; }
    for (unsigned k=0;k<RGB_MATRIX_LED_COUNT+2;++k) {
      HSV expected={0xD1,0xD2,0xD3};
      if ((index>>8)==0 && index<RGB_MATRIX_LED_COUNT && count<=9 && k>=index && k-index<count && k<RGB_MATRIX_LED_COUNT) {
        expected.h=before[3+3*(k-index)]; expected.s=before[4+3*(k-index)]; expected.v=before[5+3*(k-index)];
        if (expected.v>RGB_MATRIX_MAXIMUM_BRIGHTNESS) expected.v=RGB_MATRIX_MAXIMUM_BRIGHTNESS;
      }
      HSV got=g_direct_mode_colors[k];
      if (memcmp(&got,&expected,sizeof got)) { fprintf(stderr,"color mismatch idx=%u count=%u k=%u got=%u,%u,%u exp=%u,%u,%u\\n",index,count,k,got.h,got.s,got.v,expected.h,expected.s,expected.v); return 2; }
    }
  }
  const unsigned boundary_counts[]={0,1,9,10,255};
  for (unsigned high=1; high<256; ++high) for(unsigned low=0;low<256;++low) for(unsigned ci=0;ci<5;++ci) {
    unsigned count=boundary_counts[ci], index=(high<<8)|low;
    memset(args,0xA5,sizeof args); args[0]=(uint8_t)low; args[1]=(uint8_t)high; args[2]=(uint8_t)count; memcpy(before,args,sizeof args);
    for(unsigned k=0;k<RGB_MATRIX_LED_COUNT+2;++k) g_direct_mode_colors[k]=(HSV){0xD1,0xD2,0xD3};
    FASTSET(args);
    if(memcmp(args,before,sizeof args)) return 1;
    for(unsigned k=0;k<RGB_MATRIX_LED_COUNT+2;++k) { HSV got=g_direct_mode_colors[k], sentinel={0xD1,0xD2,0xD3}; if(memcmp(&got,&sentinel,sizeof got)) return 2; }
  }
  for (unsigned edge=0;edge<2;++edge) for (unsigned val=0; val<256; ++val) {
    uint8_t packet[30]={0}; packet[0]=edge ? RGB_MATRIX_LED_COUNT-1 : 0; packet[2]=1; packet[3]=0x31; packet[4]=0x52; packet[5]=(uint8_t)val;
    for (unsigned k=0;k<RGB_MATRIX_LED_COUNT+2;++k) g_direct_mode_colors[k]=(HSV){0xD1,0xD2,0xD3};
    FASTSET(packet);
    HSV got=g_direct_mode_colors[packet[0]]; uint8_t expected=(val>RGB_MATRIX_MAXIMUM_BRIGHTNESS)?RGB_MATRIX_MAXIMUM_BRIGHTNESS:(uint8_t)val;
    if (got.h!=0x31 || got.s!=0x52 || got.v!=expected) return 4;
    if (packet[0]==0 ? g_direct_mode_colors[1].h!=0xD1 : g_direct_mode_colors[RGB_MATRIX_LED_COUNT-2].h!=0xD1) return 5;
  }
  /* Execute the extracted public setter for every possible length. */
  for(unsigned length=0;length<256;++length) {
    uint8_t packet[32]={0}; packet[1]=vialrgb_direct_fastset; packet[2]=0; packet[4]=1; packet[5]=1; packet[6]=10;
    for(unsigned k=0;k<RGB_MATRIX_LED_COUNT+2;++k) g_direct_mode_colors[k]=(HSV){0xD1,0xD2,0xD3};
    vialrgb_set_value(packet,(uint8_t)length);
    if(length==VIAL_RAW_EPSIZE) { if(g_direct_mode_colors[0].h!=1) return 6; }
    else if(g_direct_mode_colors[0].h!=0xD1) return 7;
  }
  return 0;
}
'''


def run(label, helper, setter):
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "test.c"
        exe = pathlib.Path(tmp) / "test"
        call = "fast_set_leds(p)" if "static void fast_set_leds(uint8_t VIALRGB_BUFFER *args)" in helper else "fast_set_leds(p, 30)"
        src.write_text(harness(helper, setter, call))
        subprocess.run(["cc", "-std=c11", "-O1", "-g", "-fsanitize=address,undefined", str(src), "-o", str(exe)], check=True)
        subprocess.run([str(exe)], check=True)
    print(f"PASS {label}: high=0 all low/count pairs; high=1..255 all low bytes at counts 0,1,9,10,255; edge HSV and extracted setter lengths 0..255; helper sha256={hashlib.sha256(helper.encode()).hexdigest()}")


current = extract(SOURCE.read_text())
current_setter = extract_setter(SOURCE.read_text())
baseline_text = subprocess.check_output(["git", "show", f"{BASE}:qmk-8051-ak820/quantum/vialrgb.c"], cwd=ROOT, text=True)
baseline = extract(baseline_text)
baseline_setter = extract_setter(baseline_text)
run("frozen 09330ab oracle", baseline, baseline_setter)
run("production helper", current, current_setter)
