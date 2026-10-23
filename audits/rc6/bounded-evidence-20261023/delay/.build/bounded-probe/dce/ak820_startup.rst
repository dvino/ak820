                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module ak820_startup
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl __mcs51_genXINIT
                                     12 ;--------------------------------------------------------
                                     13 ; special function registers
                                     14 ;--------------------------------------------------------
                                     15 	.area RSEG    (ABS,DATA)
      000000                         16 	.org 0x0000
                                     17 ;--------------------------------------------------------
                                     18 ; special function bits
                                     19 ;--------------------------------------------------------
                                     20 	.area RSEG    (ABS,DATA)
      000000                         21 	.org 0x0000
                                     22 ;--------------------------------------------------------
                                     23 ; overlayable register banks
                                     24 ;--------------------------------------------------------
                                     25 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                         26 	.ds 8
                                     27 ;--------------------------------------------------------
                                     28 ; internal ram data
                                     29 ;--------------------------------------------------------
                                     30 	.area DSEG    (DATA)
                                     31 ;--------------------------------------------------------
                                     32 ; overlayable items in internal ram
                                     33 ;--------------------------------------------------------
                                     34 ;--------------------------------------------------------
                                     35 ; indirectly addressable internal ram data
                                     36 ;--------------------------------------------------------
                                     37 	.area ISEG    (DATA)
                                     38 ;--------------------------------------------------------
                                     39 ; absolute internal ram data
                                     40 ;--------------------------------------------------------
                                     41 	.area IABS    (ABS,DATA)
                                     42 	.area IABS    (ABS,DATA)
                                     43 ;--------------------------------------------------------
                                     44 ; bit data
                                     45 ;--------------------------------------------------------
                                     46 	.area BSEG    (BIT)
                                     47 ;--------------------------------------------------------
                                     48 ; paged external ram data
                                     49 ;--------------------------------------------------------
                                     50 	.area PSEG    (PAG,XDATA)
                                     51 ;--------------------------------------------------------
                                     52 ; uninitialized external ram data
                                     53 ;--------------------------------------------------------
                                     54 	.area XSEG    (XDATA)
                                     55 ;--------------------------------------------------------
                                     56 ; absolute external ram data
                                     57 ;--------------------------------------------------------
                                     58 	.area XABS    (ABS,XDATA)
                                     59 ;--------------------------------------------------------
                                     60 ; initialized external ram data
                                     61 ;--------------------------------------------------------
                                     62 	.area XISEG   (XDATA)
                                     63 	.area HOME    (CODE)
                                     64 	.area GSINIT0 (CODE)
                                     65 	.area GSINIT1 (CODE)
                                     66 	.area GSINIT2 (CODE)
                                     67 	.area GSINIT3 (CODE)
                                     68 	.area GSINIT4 (CODE)
                                     69 	.area GSINIT5 (CODE)
                                     70 	.area GSINIT  (CODE)
                                     71 	.area GSFINAL (CODE)
                                     72 	.area CSEG    (CODE)
                                     73 ;--------------------------------------------------------
                                     74 ; global & static initialisations
                                     75 ;--------------------------------------------------------
                                     76 	.area HOME    (CODE)
                                     77 	.area GSINIT  (CODE)
                                     78 	.area GSFINAL (CODE)
                                     79 	.area GSINIT  (CODE)
                                     80 ;--------------------------------------------------------
                                     81 ; Home
                                     82 ;--------------------------------------------------------
                                     83 	.area HOME    (CODE)
                                     84 	.area HOME    (CODE)
                                     85 ;--------------------------------------------------------
                                     86 ; code
                                     87 ;--------------------------------------------------------
                                     88 	.area GSINIT3 (CODE)
                                     89 ;------------------------------------------------------------
                                     90 ;Allocation info for local variables in function '_mcs51_genXINIT'
                                     91 ;------------------------------------------------------------
                                     92 ;	keyboards/ajazz/ak820/ak820_startup.c:19: void _mcs51_genXINIT(void) __naked {
                                     93 ;	-----------------------------------------
                                     94 ;	 function _mcs51_genXINIT
                                     95 ;	-----------------------------------------
      0030B2                         96 __mcs51_genXINIT:
                                     97 ;	naked function: no prologue.
                                     98 ;	keyboards/ajazz/ak820/ak820_startup.c:53: __endasm;
                                     99 	.globl l_XINIT
                                    100 	.globl s_XINIT
                                    101 	.globl s_XISEG
      0030B2 79 75            [12]  102 	mov r1, #l_XINIT
      0030B4 E9               [12]  103 	mov a, r1
      0030B5 44 00            [12]  104 	orl a, #(l_XINIT >> 8)
      0030B7 60 25            [24]  105 	jz 00002$
      0030B9 7A 01            [12]  106 	mov r2, #((l_XINIT + 255) >> 8)
      0030BB 7B 7E            [12]  107 	mov r3, #s_XINIT
      0030BD 7C BD            [12]  108 	mov r4, #(s_XINIT >> 8)
      0030BF 7D 9E            [12]  109 	mov r5, #s_XISEG
      0030C1 7E 0B            [12]  110 	mov r6, #(s_XISEG >> 8)
      0030C3                        111 00001$:
      0030C3 8B 82            [24]  112 	mov dpl, r3
      0030C5 8C 83            [24]  113 	mov dph, r4
      0030C7 E4               [12]  114 	clr a
      0030C8 93               [24]  115 	movc a, @a+dptr
      0030C9 FF               [12]  116 	mov r7, a
      0030CA A3               [24]  117 	inc dptr
      0030CB AB 82            [24]  118 	mov r3, dpl
      0030CD AC 83            [24]  119 	mov r4, dph
      0030CF 8D 82            [24]  120 	mov dpl, r5
      0030D1 8E 83            [24]  121 	mov dph, r6
      0030D3 EF               [12]  122 	mov a, r7
      0030D4 F0               [24]  123 	movx @dptr, a
      0030D5 A3               [24]  124 	inc dptr
      0030D6 AD 82            [24]  125 	mov r5, dpl
      0030D8 AE 83            [24]  126 	mov r6, dph
      0030DA D9 E7            [24]  127 	djnz r1, 00001$
      0030DC DA E5            [24]  128 	djnz r2, 00001$
      0030DE                        129 00002$:
                                    130 ;	keyboards/ajazz/ak820/ak820_startup.c:54: }
                                    131 ;	naked function: no epilogue.
                                    132 	.area GSINIT3 (CODE)
                                    133 	.area CONST   (CODE)
                                    134 	.area XINIT   (CODE)
                                    135 	.area CABS    (ABS,CODE)
