                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module print
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _putchar_
                                     12 	.globl _print_set_sendchar
                                     13 ;--------------------------------------------------------
                                     14 ; special function registers
                                     15 ;--------------------------------------------------------
                                     16 	.area RSEG    (ABS,DATA)
      000000                         17 	.org 0x0000
                                     18 ;--------------------------------------------------------
                                     19 ; special function bits
                                     20 ;--------------------------------------------------------
                                     21 	.area RSEG    (ABS,DATA)
      000000                         22 	.org 0x0000
                                     23 ;--------------------------------------------------------
                                     24 ; overlayable register banks
                                     25 ;--------------------------------------------------------
                                     26 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                         27 	.ds 8
                                     28 ;--------------------------------------------------------
                                     29 ; internal ram data
                                     30 ;--------------------------------------------------------
                                     31 	.area DSEG    (DATA)
                                     32 ;--------------------------------------------------------
                                     33 ; overlayable items in internal ram
                                     34 ;--------------------------------------------------------
                                     35 ;--------------------------------------------------------
                                     36 ; indirectly addressable internal ram data
                                     37 ;--------------------------------------------------------
                                     38 	.area ISEG    (DATA)
                                     39 ;--------------------------------------------------------
                                     40 ; absolute internal ram data
                                     41 ;--------------------------------------------------------
                                     42 	.area IABS    (ABS,DATA)
                                     43 	.area IABS    (ABS,DATA)
                                     44 ;--------------------------------------------------------
                                     45 ; bit data
                                     46 ;--------------------------------------------------------
                                     47 	.area BSEG    (BIT)
                                     48 ;--------------------------------------------------------
                                     49 ; paged external ram data
                                     50 ;--------------------------------------------------------
                                     51 	.area PSEG    (PAG,XDATA)
                                     52 ;--------------------------------------------------------
                                     53 ; uninitialized external ram data
                                     54 ;--------------------------------------------------------
                                     55 	.area XSEG    (XDATA)
      00099F                         56 _print_set_sendchar_send_10000_6:
      00099F                         57 	.ds 2
      0009A1                         58 _putchar__character_10000_8:
      0009A1                         59 	.ds 1
                                     60 ;--------------------------------------------------------
                                     61 ; absolute external ram data
                                     62 ;--------------------------------------------------------
                                     63 	.area XABS    (ABS,XDATA)
                                     64 ;--------------------------------------------------------
                                     65 ; initialized external ram data
                                     66 ;--------------------------------------------------------
                                     67 	.area XISEG   (XDATA)
      000BFF                         68 _func:
      000BFF                         69 	.ds 2
                                     70 	.area HOME    (CODE)
                                     71 	.area GSINIT0 (CODE)
                                     72 	.area GSINIT1 (CODE)
                                     73 	.area GSINIT2 (CODE)
                                     74 	.area GSINIT3 (CODE)
                                     75 	.area GSINIT4 (CODE)
                                     76 	.area GSINIT5 (CODE)
                                     77 	.area GSINIT  (CODE)
                                     78 	.area GSFINAL (CODE)
                                     79 	.area CSEG    (CODE)
                                     80 ;--------------------------------------------------------
                                     81 ; global & static initialisations
                                     82 ;--------------------------------------------------------
                                     83 	.area HOME    (CODE)
                                     84 	.area GSINIT  (CODE)
                                     85 	.area GSFINAL (CODE)
                                     86 	.area GSINIT  (CODE)
                                     87 ;--------------------------------------------------------
                                     88 ; Home
                                     89 ;--------------------------------------------------------
                                     90 	.area HOME    (CODE)
                                     91 	.area HOME    (CODE)
                                     92 ;--------------------------------------------------------
                                     93 ; code
                                     94 ;--------------------------------------------------------
                                     95 	.area CSEG    (CODE)
                                     96 ;------------------------------------------------------------
                                     97 ;Allocation info for local variables in function 'null_sendchar_func'
                                     98 ;------------------------------------------------------------
                                     99 ;c             Allocated with name '_null_sendchar_func_c_10000_4'
                                    100 ;------------------------------------------------------------
                                    101 ;	quantum/logging/print.c:22: static int8_t null_sendchar_func(uint8_t c) {
                                    102 ;	-----------------------------------------
                                    103 ;	 function null_sendchar_func
                                    104 ;	-----------------------------------------
      009150                        105 _null_sendchar_func:
                           000007   106 	ar7 = 0x07
                           000006   107 	ar6 = 0x06
                           000005   108 	ar5 = 0x05
                           000004   109 	ar4 = 0x04
                           000003   110 	ar3 = 0x03
                           000002   111 	ar2 = 0x02
                           000001   112 	ar1 = 0x01
                           000000   113 	ar0 = 0x00
                                    114 ;	quantum/logging/print.c:23: return 0;
      009150 75 82 00         [24]  115 	mov	dpl, #0x00
                                    116 ;	quantum/logging/print.c:24: }
      009153 22               [24]  117 	ret
                                    118 ;------------------------------------------------------------
                                    119 ;Allocation info for local variables in function 'print_set_sendchar'
                                    120 ;------------------------------------------------------------
                                    121 ;send          Allocated with name '_print_set_sendchar_send_10000_6'
                                    122 ;------------------------------------------------------------
                                    123 ;	quantum/logging/print.c:27: void print_set_sendchar(sendchar_func_t send) {
                                    124 ;	-----------------------------------------
                                    125 ;	 function print_set_sendchar
                                    126 ;	-----------------------------------------
      009154                        127 _print_set_sendchar:
      009154 AF 83            [24]  128 	mov	r7,dph
      009156 E5 82            [12]  129 	mov	a,dpl
      009158 90 09 9F         [24]  130 	mov	dptr,#_print_set_sendchar_send_10000_6
      00915B F0               [24]  131 	movx	@dptr,a
      00915C EF               [12]  132 	mov	a,r7
      00915D A3               [24]  133 	inc	dptr
      00915E F0               [24]  134 	movx	@dptr,a
                                    135 ;	quantum/logging/print.c:28: func = send;
      00915F 90 09 9F         [24]  136 	mov	dptr,#_print_set_sendchar_send_10000_6
      009162 E0               [24]  137 	movx	a,@dptr
      009163 FE               [12]  138 	mov	r6,a
      009164 A3               [24]  139 	inc	dptr
      009165 E0               [24]  140 	movx	a,@dptr
      009166 FF               [12]  141 	mov	r7,a
      009167 90 0B FF         [24]  142 	mov	dptr,#_func
      00916A EE               [12]  143 	mov	a,r6
      00916B F0               [24]  144 	movx	@dptr,a
      00916C EF               [12]  145 	mov	a,r7
      00916D A3               [24]  146 	inc	dptr
      00916E F0               [24]  147 	movx	@dptr,a
                                    148 ;	quantum/logging/print.c:29: }
      00916F 22               [24]  149 	ret
                                    150 ;------------------------------------------------------------
                                    151 ;Allocation info for local variables in function 'putchar_'
                                    152 ;------------------------------------------------------------
                                    153 ;character     Allocated with name '_putchar__character_10000_8'
                                    154 ;------------------------------------------------------------
                                    155 ;	quantum/logging/print.c:31: void putchar_(char character) {
                                    156 ;	-----------------------------------------
                                    157 ;	 function putchar_
                                    158 ;	-----------------------------------------
      009170                        159 _putchar_:
      009170 E5 82            [12]  160 	mov	a,dpl
      009172 90 09 A1         [24]  161 	mov	dptr,#_putchar__character_10000_8
      009175 F0               [24]  162 	movx	@dptr,a
                                    163 ;	quantum/logging/print.c:32: func(character);
      009176 E0               [24]  164 	movx	a,@dptr
      009177 FF               [12]  165 	mov	r7,a
      009178 90 0B FF         [24]  166 	mov	dptr,#_func
      00917B E0               [24]  167 	movx	a,@dptr
      00917C C0 E0            [24]  168 	push	acc
      00917E A3               [24]  169 	inc	dptr
      00917F E0               [24]  170 	movx	a,@dptr
      009180 C0 E0            [24]  171 	push	acc
      009182 8F 82            [24]  172 	mov	dpl, r7
      009184 22               [24]  173 	ret
                                    174 ;	quantum/logging/print.c:33: }
      009185 22               [24]  175 	ret
                                    176 	.area CSEG    (CODE)
                                    177 	.area CONST   (CODE)
                                    178 	.area XINIT   (CODE)
      00BDDC                        179 __xinit__func:
      00BDDC 50 91                  180 	.byte _null_sendchar_func, (_null_sendchar_func >> 8)
                                    181 	.area CABS    (ABS,CODE)
