                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module tri_layer
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _get_tri_layer_lower_layer
                                     12 	.globl _get_tri_layer_upper_layer
                                     13 	.globl _get_tri_layer_adjust_layer
                                     14 ;--------------------------------------------------------
                                     15 ; special function registers
                                     16 ;--------------------------------------------------------
                                     17 	.area RSEG    (ABS,DATA)
      000000                         18 	.org 0x0000
                                     19 ;--------------------------------------------------------
                                     20 ; special function bits
                                     21 ;--------------------------------------------------------
                                     22 	.area RSEG    (ABS,DATA)
      000000                         23 	.org 0x0000
                                     24 ;--------------------------------------------------------
                                     25 ; overlayable register banks
                                     26 ;--------------------------------------------------------
                                     27 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                         28 	.ds 8
                                     29 ;--------------------------------------------------------
                                     30 ; internal ram data
                                     31 ;--------------------------------------------------------
                                     32 	.area DSEG    (DATA)
                                     33 ;--------------------------------------------------------
                                     34 ; overlayable items in internal ram
                                     35 ;--------------------------------------------------------
                                     36 ;--------------------------------------------------------
                                     37 ; indirectly addressable internal ram data
                                     38 ;--------------------------------------------------------
                                     39 	.area ISEG    (DATA)
                                     40 ;--------------------------------------------------------
                                     41 ; absolute internal ram data
                                     42 ;--------------------------------------------------------
                                     43 	.area IABS    (ABS,DATA)
                                     44 	.area IABS    (ABS,DATA)
                                     45 ;--------------------------------------------------------
                                     46 ; bit data
                                     47 ;--------------------------------------------------------
                                     48 	.area BSEG    (BIT)
                                     49 ;--------------------------------------------------------
                                     50 ; paged external ram data
                                     51 ;--------------------------------------------------------
                                     52 	.area PSEG    (PAG,XDATA)
                                     53 ;--------------------------------------------------------
                                     54 ; uninitialized external ram data
                                     55 ;--------------------------------------------------------
                                     56 	.area XSEG    (XDATA)
                                     57 ;--------------------------------------------------------
                                     58 ; absolute external ram data
                                     59 ;--------------------------------------------------------
                                     60 	.area XABS    (ABS,XDATA)
                                     61 ;--------------------------------------------------------
                                     62 ; initialized external ram data
                                     63 ;--------------------------------------------------------
                                     64 	.area XISEG   (XDATA)
      000C04                         65 _tri_layer_lower_layer:
      000C04                         66 	.ds 1
      000C05                         67 _tri_layer_upper_layer:
      000C05                         68 	.ds 1
      000C06                         69 _tri_layer_adjust_layer:
      000C06                         70 	.ds 1
                                     71 	.area HOME    (CODE)
                                     72 	.area GSINIT0 (CODE)
                                     73 	.area GSINIT1 (CODE)
                                     74 	.area GSINIT2 (CODE)
                                     75 	.area GSINIT3 (CODE)
                                     76 	.area GSINIT4 (CODE)
                                     77 	.area GSINIT5 (CODE)
                                     78 	.area GSINIT  (CODE)
                                     79 	.area GSFINAL (CODE)
                                     80 	.area CSEG    (CODE)
                                     81 ;--------------------------------------------------------
                                     82 ; global & static initialisations
                                     83 ;--------------------------------------------------------
                                     84 	.area HOME    (CODE)
                                     85 	.area GSINIT  (CODE)
                                     86 	.area GSFINAL (CODE)
                                     87 	.area GSINIT  (CODE)
                                     88 ;--------------------------------------------------------
                                     89 ; Home
                                     90 ;--------------------------------------------------------
                                     91 	.area HOME    (CODE)
                                     92 	.area HOME    (CODE)
                                     93 ;--------------------------------------------------------
                                     94 ; code
                                     95 ;--------------------------------------------------------
                                     96 	.area CSEG    (CODE)
                                     97 ;------------------------------------------------------------
                                     98 ;Allocation info for local variables in function 'set_tri_layer_lower_layer'
                                     99 ;------------------------------------------------------------
                                    100 ;layer         Allocated with name '_set_tri_layer_lower_layer_layer_10000_8'
                                    101 ;------------------------------------------------------------
                                    102 ;	quantum/tri_layer.c:11: void set_tri_layer_lower_layer(uint8_t layer) {
                                    103 ;	-----------------------------------------
                           000007   104 	ar7 = 0x07
                           000006   105 	ar6 = 0x06
                           000005   106 	ar5 = 0x05
                           000004   107 	ar4 = 0x04
                           000003   108 	ar3 = 0x03
                           000002   109 	ar2 = 0x02
                           000001   110 	ar1 = 0x01
                           000000   111 	ar0 = 0x00
                                    112 ;	 function get_tri_layer_lower_layer
                                    113 ;	-----------------------------------------
      00A01C                        114 _get_tri_layer_lower_layer:
                                    115 ;	quantum/tri_layer.c:30: return tri_layer_lower_layer;
      00A01C 90 0C 04         [24]  116 	mov	dptr,#_tri_layer_lower_layer
      00A01F E0               [24]  117 	movx	a,@dptr
                                    118 ;	quantum/tri_layer.c:31: }
      00A020 F5 82            [12]  119 	mov	dpl,a
      00A022 22               [24]  120 	ret
                                    121 ;------------------------------------------------------------
                                    122 ;Allocation info for local variables in function 'get_tri_layer_upper_layer'
                                    123 ;------------------------------------------------------------
                                    124 ;	quantum/tri_layer.c:33: uint8_t get_tri_layer_upper_layer(void) {
                                    125 ;	-----------------------------------------
                                    126 ;	 function get_tri_layer_upper_layer
                                    127 ;	-----------------------------------------
      00A023                        128 _get_tri_layer_upper_layer:
                                    129 ;	quantum/tri_layer.c:34: return tri_layer_upper_layer;
      00A023 90 0C 05         [24]  130 	mov	dptr,#_tri_layer_upper_layer
      00A026 E0               [24]  131 	movx	a,@dptr
                                    132 ;	quantum/tri_layer.c:35: }
      00A027 F5 82            [12]  133 	mov	dpl,a
      00A029 22               [24]  134 	ret
                                    135 ;------------------------------------------------------------
                                    136 ;Allocation info for local variables in function 'get_tri_layer_adjust_layer'
                                    137 ;------------------------------------------------------------
                                    138 ;	quantum/tri_layer.c:37: uint8_t get_tri_layer_adjust_layer(void) {
                                    139 ;	-----------------------------------------
                                    140 ;	 function get_tri_layer_adjust_layer
                                    141 ;	-----------------------------------------
      00A02A                        142 _get_tri_layer_adjust_layer:
                                    143 ;	quantum/tri_layer.c:38: return tri_layer_adjust_layer;
      00A02A 90 0C 06         [24]  144 	mov	dptr,#_tri_layer_adjust_layer
      00A02D E0               [24]  145 	movx	a,@dptr
                                    146 ;	quantum/tri_layer.c:39: }
      00A02E F5 82            [12]  147 	mov	dpl,a
      00A030 22               [24]  148 	ret
                                    149 	.area CSEG    (CODE)
                                    150 	.area CONST   (CODE)
                                    151 	.area XINIT   (CODE)
      00BDC3                        152 __xinit__tri_layer_lower_layer:
      00BDC3 01                     153 	.db #0x01	; 1
      00BDC4                        154 __xinit__tri_layer_upper_layer:
      00BDC4 02                     155 	.db #0x02	; 2
      00BDC5                        156 __xinit__tri_layer_adjust_layer:
      00BDC5 03                     157 	.db #0x03	; 3
                                    158 	.area CABS    (ABS,CODE)
