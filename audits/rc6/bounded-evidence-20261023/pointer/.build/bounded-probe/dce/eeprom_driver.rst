                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module eeprom_driver
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _eeprom_write_block
                                     12 	.globl _eeprom_read_block
                                     13 	.globl _eeprom_update_dword_PARM_2
                                     14 	.globl _eeprom_update_word_PARM_2
                                     15 	.globl _eeprom_update_byte_PARM_2
                                     16 	.globl _eeprom_update_block_PARM_3
                                     17 	.globl _eeprom_update_block_PARM_2
                                     18 	.globl _eeprom_write_dword_PARM_2
                                     19 	.globl _eeprom_write_word_PARM_2
                                     20 	.globl _eeprom_write_byte_PARM_2
                                     21 	.globl _eeprom_read_byte
                                     22 	.globl _eeprom_read_word
                                     23 	.globl _eeprom_read_dword
                                     24 	.globl _eeprom_write_byte
                                     25 	.globl _eeprom_write_word
                                     26 	.globl _eeprom_write_dword
                                     27 	.globl _eeprom_update_block
                                     28 	.globl _eeprom_update_byte
                                     29 	.globl _eeprom_update_word
                                     30 	.globl _eeprom_update_dword
                                     31 ;--------------------------------------------------------
                                     32 ; special function registers
                                     33 ;--------------------------------------------------------
                                     34 	.area RSEG    (ABS,DATA)
      000000                         35 	.org 0x0000
                                     36 ;--------------------------------------------------------
                                     37 ; special function bits
                                     38 ;--------------------------------------------------------
                                     39 	.area RSEG    (ABS,DATA)
      000000                         40 	.org 0x0000
                                     41 ;--------------------------------------------------------
                                     42 ; overlayable register banks
                                     43 ;--------------------------------------------------------
                                     44 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                         45 	.ds 8
                                     46 ;--------------------------------------------------------
                                     47 ; overlayable bit register bank
                                     48 ;--------------------------------------------------------
                                     49 	.area BIT_BANK	(REL,OVR,DATA)
      000023                         50 bits:
      000023                         51 	.ds 1
                           008000    52 	b0 = bits[0]
                           008100    53 	b1 = bits[1]
                           008200    54 	b2 = bits[2]
                           008300    55 	b3 = bits[3]
                           008400    56 	b4 = bits[4]
                           008500    57 	b5 = bits[5]
                           008600    58 	b6 = bits[6]
                           008700    59 	b7 = bits[7]
                                     60 ;--------------------------------------------------------
                                     61 ; internal ram data
                                     62 ;--------------------------------------------------------
                                     63 	.area DSEG    (DATA)
      00000E                         64 _eeprom_update_block_sloc0_1_0:
      00000E                         65 	.ds 3
      000011                         66 _eeprom_update_block_sloc1_1_0:
      000011                         67 	.ds 2
      000013                         68 _eeprom_update_block_sloc2_1_0:
      000013                         69 	.ds 1
      000014                         70 _eeprom_update_block_sloc3_1_0:
      000014                         71 	.ds 3
                                     72 ;--------------------------------------------------------
                                     73 ; overlayable items in internal ram
                                     74 ;--------------------------------------------------------
                                     75 ;--------------------------------------------------------
                                     76 ; indirectly addressable internal ram data
                                     77 ;--------------------------------------------------------
                                     78 	.area ISEG    (DATA)
                                     79 ;--------------------------------------------------------
                                     80 ; absolute internal ram data
                                     81 ;--------------------------------------------------------
                                     82 	.area IABS    (ABS,DATA)
                                     83 	.area IABS    (ABS,DATA)
                                     84 ;--------------------------------------------------------
                                     85 ; bit data
                                     86 ;--------------------------------------------------------
                                     87 	.area BSEG    (BIT)
                                     88 ;--------------------------------------------------------
                                     89 ; paged external ram data
                                     90 ;--------------------------------------------------------
                                     91 	.area PSEG    (PAG,XDATA)
                                     92 ;--------------------------------------------------------
                                     93 ; uninitialized external ram data
                                     94 ;--------------------------------------------------------
                                     95 	.area XSEG    (XDATA)
      000590                         96 _eeprom_read_byte_addr_10000_77:
      000590                         97 	.ds 3
      000593                         98 _eeprom_read_byte_ret_10000_78:
      000593                         99 	.ds 1
      000594                        100 _eeprom_read_word_addr_10000_79:
      000594                        101 	.ds 3
      000597                        102 _eeprom_read_word_ret_10000_80:
      000597                        103 	.ds 2
      000599                        104 _eeprom_read_dword_addr_10000_81:
      000599                        105 	.ds 3
      00059C                        106 _eeprom_read_dword_ret_10000_82:
      00059C                        107 	.ds 4
      0005A0                        108 _eeprom_write_byte_PARM_2:
      0005A0                        109 	.ds 1
      0005A1                        110 _eeprom_write_byte_addr_10000_83:
      0005A1                        111 	.ds 3
      0005A4                        112 _eeprom_write_word_PARM_2:
      0005A4                        113 	.ds 2
      0005A6                        114 _eeprom_write_word_addr_10000_85:
      0005A6                        115 	.ds 3
      0005A9                        116 _eeprom_write_dword_PARM_2:
      0005A9                        117 	.ds 4
      0005AD                        118 _eeprom_write_dword_addr_10000_87:
      0005AD                        119 	.ds 3
      0005B0                        120 _eeprom_update_block_PARM_2:
      0005B0                        121 	.ds 3
      0005B3                        122 _eeprom_update_block_PARM_3:
      0005B3                        123 	.ds 2
      0005B5                        124 _eeprom_update_block_buf_10000_89:
      0005B5                        125 	.ds 3
      0005B8                        126 _eeprom_update_byte_PARM_2:
      0005B8                        127 	.ds 1
      0005B9                        128 _eeprom_update_byte_addr_10000_95:
      0005B9                        129 	.ds 3
      0005BC                        130 _eeprom_update_word_PARM_2:
      0005BC                        131 	.ds 2
      0005BE                        132 _eeprom_update_word_addr_10000_99:
      0005BE                        133 	.ds 3
      0005C1                        134 _eeprom_update_dword_PARM_2:
      0005C1                        135 	.ds 4
      0005C5                        136 _eeprom_update_dword_addr_10000_103:
      0005C5                        137 	.ds 3
                                    138 ;--------------------------------------------------------
                                    139 ; absolute external ram data
                                    140 ;--------------------------------------------------------
                                    141 	.area XABS    (ABS,XDATA)
                                    142 ;--------------------------------------------------------
                                    143 ; initialized external ram data
                                    144 ;--------------------------------------------------------
                                    145 	.area XISEG   (XDATA)
                                    146 	.area HOME    (CODE)
                                    147 	.area GSINIT0 (CODE)
                                    148 	.area GSINIT1 (CODE)
                                    149 	.area GSINIT2 (CODE)
                                    150 	.area GSINIT3 (CODE)
                                    151 	.area GSINIT4 (CODE)
                                    152 	.area GSINIT5 (CODE)
                                    153 	.area GSINIT  (CODE)
                                    154 	.area GSFINAL (CODE)
                                    155 	.area CSEG    (CODE)
                                    156 ;--------------------------------------------------------
                                    157 ; global & static initialisations
                                    158 ;--------------------------------------------------------
                                    159 	.area HOME    (CODE)
                                    160 	.area GSINIT  (CODE)
                                    161 	.area GSFINAL (CODE)
                                    162 	.area GSINIT  (CODE)
                                    163 ;--------------------------------------------------------
                                    164 ; Home
                                    165 ;--------------------------------------------------------
                                    166 	.area HOME    (CODE)
                                    167 	.area HOME    (CODE)
                                    168 ;--------------------------------------------------------
                                    169 ; code
                                    170 ;--------------------------------------------------------
                                    171 	.area CSEG    (CODE)
                                    172 ;------------------------------------------------------------
                                    173 ;Allocation info for local variables in function 'eeprom_read_byte'
                                    174 ;------------------------------------------------------------
                                    175 ;addr          Allocated with name '_eeprom_read_byte_addr_10000_77'
                                    176 ;ret           Allocated with name '_eeprom_read_byte_ret_10000_78'
                                    177 ;------------------------------------------------------------
                                    178 ;	drivers/eeprom/eeprom_driver.c:22: uint8_t eeprom_read_byte(const uint8_t *addr) {
                                    179 ;	-----------------------------------------
                                    180 ;	 function eeprom_read_byte
                                    181 ;	-----------------------------------------
      0043FC                        182 _eeprom_read_byte:
                           000007   183 	ar7 = 0x07
                           000006   184 	ar6 = 0x06
                           000005   185 	ar5 = 0x05
                           000004   186 	ar4 = 0x04
                           000003   187 	ar3 = 0x03
                           000002   188 	ar2 = 0x02
                           000001   189 	ar1 = 0x01
                           000000   190 	ar0 = 0x00
      0043FC C0 07            [24]  191 	push	ar7
      0043FE C0 06            [24]  192 	push	ar6
      004400 C0 05            [24]  193 	push	ar5
      004402 AF F0            [24]  194 	mov	r7,b
      004404 AE 83            [24]  195 	mov	r6,dph
      004406 E5 82            [12]  196 	mov	a,dpl
      004408 90 05 90         [24]  197 	mov	dptr,#_eeprom_read_byte_addr_10000_77
      00440B F0               [24]  198 	movx	@dptr,a
      00440C EE               [12]  199 	mov	a,r6
      00440D A3               [24]  200 	inc	dptr
      00440E F0               [24]  201 	movx	@dptr,a
      00440F EF               [12]  202 	mov	a,r7
      004410 A3               [24]  203 	inc	dptr
      004411 F0               [24]  204 	movx	@dptr,a
                                    205 ;	drivers/eeprom/eeprom_driver.c:23: uint8_t ret = 0;
      004412 90 05 93         [24]  206 	mov	dptr,#_eeprom_read_byte_ret_10000_78
      004415 E4               [12]  207 	clr	a
      004416 F0               [24]  208 	movx	@dptr,a
                                    209 ;	drivers/eeprom/eeprom_driver.c:24: eeprom_read_block(&ret, addr, 1);
      004417 90 05 90         [24]  210 	mov	dptr,#_eeprom_read_byte_addr_10000_77
      00441A E0               [24]  211 	movx	a,@dptr
      00441B FD               [12]  212 	mov	r5,a
      00441C A3               [24]  213 	inc	dptr
      00441D E0               [24]  214 	movx	a,@dptr
      00441E FE               [12]  215 	mov	r6,a
      00441F A3               [24]  216 	inc	dptr
      004420 E0               [24]  217 	movx	a,@dptr
      004421 FF               [12]  218 	mov	r7,a
      004422 90 05 3D         [24]  219 	mov	dptr,#_eeprom_read_block_PARM_2
      004425 ED               [12]  220 	mov	a,r5
      004426 F0               [24]  221 	movx	@dptr,a
      004427 EE               [12]  222 	mov	a,r6
      004428 A3               [24]  223 	inc	dptr
      004429 F0               [24]  224 	movx	@dptr,a
      00442A EF               [12]  225 	mov	a,r7
      00442B A3               [24]  226 	inc	dptr
      00442C F0               [24]  227 	movx	@dptr,a
      00442D 90 05 40         [24]  228 	mov	dptr,#_eeprom_read_block_PARM_3
      004430 74 01            [12]  229 	mov	a,#0x01
      004432 F0               [24]  230 	movx	@dptr,a
      004433 E4               [12]  231 	clr	a
      004434 A3               [24]  232 	inc	dptr
      004435 F0               [24]  233 	movx	@dptr,a
      004436 90 05 93         [24]  234 	mov	dptr,#_eeprom_read_byte_ret_10000_78
      004439 F5 F0            [12]  235 	mov	b,a
      00443B C0 07            [24]  236 	push	ar7
      00443D C0 06            [24]  237 	push	ar6
      00443F C0 05            [24]  238 	push	ar5
      004441 C0 04            [24]  239 	push	ar4
      004443 C0 03            [24]  240 	push	ar3
      004445 C0 02            [24]  241 	push	ar2
      004447 C0 01            [24]  242 	push	ar1
      004449 C0 00            [24]  243 	push	ar0
      00444B 12 3D 3D         [24]  244 	lcall	_eeprom_read_block
      00444E D0 00            [24]  245 	pop	ar0
      004450 D0 01            [24]  246 	pop	ar1
      004452 D0 02            [24]  247 	pop	ar2
      004454 D0 03            [24]  248 	pop	ar3
      004456 D0 04            [24]  249 	pop	ar4
      004458 D0 05            [24]  250 	pop	ar5
      00445A D0 06            [24]  251 	pop	ar6
      00445C D0 07            [24]  252 	pop	ar7
                                    253 ;	drivers/eeprom/eeprom_driver.c:25: return ret;
      00445E 90 05 93         [24]  254 	mov	dptr,#_eeprom_read_byte_ret_10000_78
      004461 E0               [24]  255 	movx	a,@dptr
      004462 F5 82            [12]  256 	mov	dpl,a
                                    257 ;	drivers/eeprom/eeprom_driver.c:26: }
      004464 D0 05            [24]  258 	pop	ar5
      004466 D0 06            [24]  259 	pop	ar6
      004468 D0 07            [24]  260 	pop	ar7
      00446A 22               [24]  261 	ret
                                    262 ;------------------------------------------------------------
                                    263 ;Allocation info for local variables in function 'eeprom_read_word'
                                    264 ;------------------------------------------------------------
                                    265 ;addr          Allocated with name '_eeprom_read_word_addr_10000_79'
                                    266 ;ret           Allocated with name '_eeprom_read_word_ret_10000_80'
                                    267 ;------------------------------------------------------------
                                    268 ;	drivers/eeprom/eeprom_driver.c:28: uint16_t eeprom_read_word(const uint16_t *addr) {
                                    269 ;	-----------------------------------------
                                    270 ;	 function eeprom_read_word
                                    271 ;	-----------------------------------------
      00446B                        272 _eeprom_read_word:
      00446B AF F0            [24]  273 	mov	r7,b
      00446D AE 83            [24]  274 	mov	r6,dph
      00446F E5 82            [12]  275 	mov	a,dpl
      004471 90 05 94         [24]  276 	mov	dptr,#_eeprom_read_word_addr_10000_79
      004474 F0               [24]  277 	movx	@dptr,a
      004475 EE               [12]  278 	mov	a,r6
      004476 A3               [24]  279 	inc	dptr
      004477 F0               [24]  280 	movx	@dptr,a
      004478 EF               [12]  281 	mov	a,r7
      004479 A3               [24]  282 	inc	dptr
      00447A F0               [24]  283 	movx	@dptr,a
                                    284 ;	drivers/eeprom/eeprom_driver.c:29: uint16_t ret = 0;
      00447B 90 05 97         [24]  285 	mov	dptr,#_eeprom_read_word_ret_10000_80
      00447E E4               [12]  286 	clr	a
      00447F F0               [24]  287 	movx	@dptr,a
      004480 A3               [24]  288 	inc	dptr
      004481 F0               [24]  289 	movx	@dptr,a
                                    290 ;	drivers/eeprom/eeprom_driver.c:30: eeprom_read_block(&ret, addr, 2);
      004482 90 05 94         [24]  291 	mov	dptr,#_eeprom_read_word_addr_10000_79
      004485 E0               [24]  292 	movx	a,@dptr
      004486 FD               [12]  293 	mov	r5,a
      004487 A3               [24]  294 	inc	dptr
      004488 E0               [24]  295 	movx	a,@dptr
      004489 FE               [12]  296 	mov	r6,a
      00448A A3               [24]  297 	inc	dptr
      00448B E0               [24]  298 	movx	a,@dptr
      00448C FF               [12]  299 	mov	r7,a
      00448D 90 05 3D         [24]  300 	mov	dptr,#_eeprom_read_block_PARM_2
      004490 ED               [12]  301 	mov	a,r5
      004491 F0               [24]  302 	movx	@dptr,a
      004492 EE               [12]  303 	mov	a,r6
      004493 A3               [24]  304 	inc	dptr
      004494 F0               [24]  305 	movx	@dptr,a
      004495 EF               [12]  306 	mov	a,r7
      004496 A3               [24]  307 	inc	dptr
      004497 F0               [24]  308 	movx	@dptr,a
      004498 90 05 40         [24]  309 	mov	dptr,#_eeprom_read_block_PARM_3
      00449B 74 02            [12]  310 	mov	a,#0x02
      00449D F0               [24]  311 	movx	@dptr,a
      00449E E4               [12]  312 	clr	a
      00449F A3               [24]  313 	inc	dptr
      0044A0 F0               [24]  314 	movx	@dptr,a
      0044A1 90 05 97         [24]  315 	mov	dptr,#_eeprom_read_word_ret_10000_80
      0044A4 F5 F0            [12]  316 	mov	b,a
      0044A6 12 3D 3D         [24]  317 	lcall	_eeprom_read_block
                                    318 ;	drivers/eeprom/eeprom_driver.c:31: return ret;
      0044A9 90 05 97         [24]  319 	mov	dptr,#_eeprom_read_word_ret_10000_80
      0044AC E0               [24]  320 	movx	a,@dptr
      0044AD FE               [12]  321 	mov	r6,a
      0044AE A3               [24]  322 	inc	dptr
      0044AF E0               [24]  323 	movx	a,@dptr
                                    324 ;	drivers/eeprom/eeprom_driver.c:32: }
      0044B0 8E 82            [24]  325 	mov	dpl,r6
      0044B2 F5 83            [12]  326 	mov	dph,a
      0044B4 22               [24]  327 	ret
                                    328 ;------------------------------------------------------------
                                    329 ;Allocation info for local variables in function 'eeprom_read_dword'
                                    330 ;------------------------------------------------------------
                                    331 ;addr          Allocated with name '_eeprom_read_dword_addr_10000_81'
                                    332 ;ret           Allocated with name '_eeprom_read_dword_ret_10000_82'
                                    333 ;------------------------------------------------------------
                                    334 ;	drivers/eeprom/eeprom_driver.c:34: uint32_t eeprom_read_dword(const uint32_t *addr) {
                                    335 ;	-----------------------------------------
                                    336 ;	 function eeprom_read_dword
                                    337 ;	-----------------------------------------
      0044B5                        338 _eeprom_read_dword:
      0044B5 AF F0            [24]  339 	mov	r7,b
      0044B7 AE 83            [24]  340 	mov	r6,dph
      0044B9 E5 82            [12]  341 	mov	a,dpl
      0044BB 90 05 99         [24]  342 	mov	dptr,#_eeprom_read_dword_addr_10000_81
      0044BE F0               [24]  343 	movx	@dptr,a
      0044BF EE               [12]  344 	mov	a,r6
      0044C0 A3               [24]  345 	inc	dptr
      0044C1 F0               [24]  346 	movx	@dptr,a
      0044C2 EF               [12]  347 	mov	a,r7
      0044C3 A3               [24]  348 	inc	dptr
      0044C4 F0               [24]  349 	movx	@dptr,a
                                    350 ;	drivers/eeprom/eeprom_driver.c:35: uint32_t ret = 0;
      0044C5 90 05 9C         [24]  351 	mov	dptr,#_eeprom_read_dword_ret_10000_82
      0044C8 E4               [12]  352 	clr	a
      0044C9 F0               [24]  353 	movx	@dptr,a
      0044CA A3               [24]  354 	inc	dptr
      0044CB F0               [24]  355 	movx	@dptr,a
      0044CC A3               [24]  356 	inc	dptr
      0044CD F0               [24]  357 	movx	@dptr,a
      0044CE A3               [24]  358 	inc	dptr
      0044CF F0               [24]  359 	movx	@dptr,a
                                    360 ;	drivers/eeprom/eeprom_driver.c:36: eeprom_read_block(&ret, addr, 4);
      0044D0 90 05 99         [24]  361 	mov	dptr,#_eeprom_read_dword_addr_10000_81
      0044D3 E0               [24]  362 	movx	a,@dptr
      0044D4 FD               [12]  363 	mov	r5,a
      0044D5 A3               [24]  364 	inc	dptr
      0044D6 E0               [24]  365 	movx	a,@dptr
      0044D7 FE               [12]  366 	mov	r6,a
      0044D8 A3               [24]  367 	inc	dptr
      0044D9 E0               [24]  368 	movx	a,@dptr
      0044DA FF               [12]  369 	mov	r7,a
      0044DB 90 05 3D         [24]  370 	mov	dptr,#_eeprom_read_block_PARM_2
      0044DE ED               [12]  371 	mov	a,r5
      0044DF F0               [24]  372 	movx	@dptr,a
      0044E0 EE               [12]  373 	mov	a,r6
      0044E1 A3               [24]  374 	inc	dptr
      0044E2 F0               [24]  375 	movx	@dptr,a
      0044E3 EF               [12]  376 	mov	a,r7
      0044E4 A3               [24]  377 	inc	dptr
      0044E5 F0               [24]  378 	movx	@dptr,a
      0044E6 90 05 40         [24]  379 	mov	dptr,#_eeprom_read_block_PARM_3
      0044E9 74 04            [12]  380 	mov	a,#0x04
      0044EB F0               [24]  381 	movx	@dptr,a
      0044EC E4               [12]  382 	clr	a
      0044ED A3               [24]  383 	inc	dptr
      0044EE F0               [24]  384 	movx	@dptr,a
      0044EF 90 05 9C         [24]  385 	mov	dptr,#_eeprom_read_dword_ret_10000_82
      0044F2 F5 F0            [12]  386 	mov	b,a
      0044F4 12 3D 3D         [24]  387 	lcall	_eeprom_read_block
                                    388 ;	drivers/eeprom/eeprom_driver.c:37: return ret;
      0044F7 90 05 9C         [24]  389 	mov	dptr,#_eeprom_read_dword_ret_10000_82
      0044FA E0               [24]  390 	movx	a,@dptr
      0044FB FC               [12]  391 	mov	r4,a
      0044FC A3               [24]  392 	inc	dptr
      0044FD E0               [24]  393 	movx	a,@dptr
      0044FE FD               [12]  394 	mov	r5,a
      0044FF A3               [24]  395 	inc	dptr
      004500 E0               [24]  396 	movx	a,@dptr
      004501 FE               [12]  397 	mov	r6,a
      004502 A3               [24]  398 	inc	dptr
      004503 E0               [24]  399 	movx	a,@dptr
      004504 8C 82            [24]  400 	mov	dpl,r4
      004506 8D 83            [24]  401 	mov	dph,r5
      004508 8E F0            [24]  402 	mov	b,r6
                                    403 ;	drivers/eeprom/eeprom_driver.c:38: }
      00450A 22               [24]  404 	ret
                                    405 ;------------------------------------------------------------
                                    406 ;Allocation info for local variables in function 'eeprom_write_byte'
                                    407 ;------------------------------------------------------------
                                    408 ;value         Allocated with name '_eeprom_write_byte_PARM_2'
                                    409 ;addr          Allocated with name '_eeprom_write_byte_addr_10000_83'
                                    410 ;------------------------------------------------------------
                                    411 ;	drivers/eeprom/eeprom_driver.c:40: void eeprom_write_byte(uint8_t *addr, uint8_t value) {
                                    412 ;	-----------------------------------------
                                    413 ;	 function eeprom_write_byte
                                    414 ;	-----------------------------------------
      00450B                        415 _eeprom_write_byte:
      00450B AF F0            [24]  416 	mov	r7,b
      00450D AE 83            [24]  417 	mov	r6,dph
      00450F E5 82            [12]  418 	mov	a,dpl
      004511 90 05 A1         [24]  419 	mov	dptr,#_eeprom_write_byte_addr_10000_83
      004514 F0               [24]  420 	movx	@dptr,a
      004515 EE               [12]  421 	mov	a,r6
      004516 A3               [24]  422 	inc	dptr
      004517 F0               [24]  423 	movx	@dptr,a
      004518 EF               [12]  424 	mov	a,r7
      004519 A3               [24]  425 	inc	dptr
      00451A F0               [24]  426 	movx	@dptr,a
                                    427 ;	drivers/eeprom/eeprom_driver.c:41: eeprom_write_block(&value, addr, 1);
      00451B 90 05 A1         [24]  428 	mov	dptr,#_eeprom_write_byte_addr_10000_83
      00451E E0               [24]  429 	movx	a,@dptr
      00451F FD               [12]  430 	mov	r5,a
      004520 A3               [24]  431 	inc	dptr
      004521 E0               [24]  432 	movx	a,@dptr
      004522 FE               [12]  433 	mov	r6,a
      004523 A3               [24]  434 	inc	dptr
      004524 E0               [24]  435 	movx	a,@dptr
      004525 FF               [12]  436 	mov	r7,a
      004526 90 05 48         [24]  437 	mov	dptr,#_eeprom_write_block_PARM_2
      004529 ED               [12]  438 	mov	a,r5
      00452A F0               [24]  439 	movx	@dptr,a
      00452B EE               [12]  440 	mov	a,r6
      00452C A3               [24]  441 	inc	dptr
      00452D F0               [24]  442 	movx	@dptr,a
      00452E EF               [12]  443 	mov	a,r7
      00452F A3               [24]  444 	inc	dptr
      004530 F0               [24]  445 	movx	@dptr,a
      004531 90 05 4B         [24]  446 	mov	dptr,#_eeprom_write_block_PARM_3
      004534 74 01            [12]  447 	mov	a,#0x01
      004536 F0               [24]  448 	movx	@dptr,a
      004537 E4               [12]  449 	clr	a
      004538 A3               [24]  450 	inc	dptr
      004539 F0               [24]  451 	movx	@dptr,a
      00453A 90 05 A0         [24]  452 	mov	dptr,#_eeprom_write_byte_PARM_2
      00453D F5 F0            [12]  453 	mov	b,a
                                    454 ;	drivers/eeprom/eeprom_driver.c:42: }
      00453F 02 3E 67         [24]  455 	ljmp	_eeprom_write_block
                                    456 ;------------------------------------------------------------
                                    457 ;Allocation info for local variables in function 'eeprom_write_word'
                                    458 ;------------------------------------------------------------
                                    459 ;value         Allocated with name '_eeprom_write_word_PARM_2'
                                    460 ;addr          Allocated with name '_eeprom_write_word_addr_10000_85'
                                    461 ;------------------------------------------------------------
                                    462 ;	drivers/eeprom/eeprom_driver.c:44: void eeprom_write_word(uint16_t *addr, uint16_t value) {
                                    463 ;	-----------------------------------------
                                    464 ;	 function eeprom_write_word
                                    465 ;	-----------------------------------------
      004542                        466 _eeprom_write_word:
      004542 AF F0            [24]  467 	mov	r7,b
      004544 AE 83            [24]  468 	mov	r6,dph
      004546 E5 82            [12]  469 	mov	a,dpl
      004548 90 05 A6         [24]  470 	mov	dptr,#_eeprom_write_word_addr_10000_85
      00454B F0               [24]  471 	movx	@dptr,a
      00454C EE               [12]  472 	mov	a,r6
      00454D A3               [24]  473 	inc	dptr
      00454E F0               [24]  474 	movx	@dptr,a
      00454F EF               [12]  475 	mov	a,r7
      004550 A3               [24]  476 	inc	dptr
      004551 F0               [24]  477 	movx	@dptr,a
                                    478 ;	drivers/eeprom/eeprom_driver.c:45: eeprom_write_block(&value, addr, 2);
      004552 90 05 A6         [24]  479 	mov	dptr,#_eeprom_write_word_addr_10000_85
      004555 E0               [24]  480 	movx	a,@dptr
      004556 FD               [12]  481 	mov	r5,a
      004557 A3               [24]  482 	inc	dptr
      004558 E0               [24]  483 	movx	a,@dptr
      004559 FE               [12]  484 	mov	r6,a
      00455A A3               [24]  485 	inc	dptr
      00455B E0               [24]  486 	movx	a,@dptr
      00455C FF               [12]  487 	mov	r7,a
      00455D 90 05 48         [24]  488 	mov	dptr,#_eeprom_write_block_PARM_2
      004560 ED               [12]  489 	mov	a,r5
      004561 F0               [24]  490 	movx	@dptr,a
      004562 EE               [12]  491 	mov	a,r6
      004563 A3               [24]  492 	inc	dptr
      004564 F0               [24]  493 	movx	@dptr,a
      004565 EF               [12]  494 	mov	a,r7
      004566 A3               [24]  495 	inc	dptr
      004567 F0               [24]  496 	movx	@dptr,a
      004568 90 05 4B         [24]  497 	mov	dptr,#_eeprom_write_block_PARM_3
      00456B 74 02            [12]  498 	mov	a,#0x02
      00456D F0               [24]  499 	movx	@dptr,a
      00456E E4               [12]  500 	clr	a
      00456F A3               [24]  501 	inc	dptr
      004570 F0               [24]  502 	movx	@dptr,a
      004571 90 05 A4         [24]  503 	mov	dptr,#_eeprom_write_word_PARM_2
      004574 F5 F0            [12]  504 	mov	b,a
                                    505 ;	drivers/eeprom/eeprom_driver.c:46: }
      004576 02 3E 67         [24]  506 	ljmp	_eeprom_write_block
                                    507 ;------------------------------------------------------------
                                    508 ;Allocation info for local variables in function 'eeprom_write_dword'
                                    509 ;------------------------------------------------------------
                                    510 ;value         Allocated with name '_eeprom_write_dword_PARM_2'
                                    511 ;addr          Allocated with name '_eeprom_write_dword_addr_10000_87'
                                    512 ;------------------------------------------------------------
                                    513 ;	drivers/eeprom/eeprom_driver.c:48: void eeprom_write_dword(uint32_t *addr, uint32_t value) {
                                    514 ;	-----------------------------------------
                                    515 ;	 function eeprom_write_dword
                                    516 ;	-----------------------------------------
      004579                        517 _eeprom_write_dword:
      004579 AF F0            [24]  518 	mov	r7,b
      00457B AE 83            [24]  519 	mov	r6,dph
      00457D E5 82            [12]  520 	mov	a,dpl
      00457F 90 05 AD         [24]  521 	mov	dptr,#_eeprom_write_dword_addr_10000_87
      004582 F0               [24]  522 	movx	@dptr,a
      004583 EE               [12]  523 	mov	a,r6
      004584 A3               [24]  524 	inc	dptr
      004585 F0               [24]  525 	movx	@dptr,a
      004586 EF               [12]  526 	mov	a,r7
      004587 A3               [24]  527 	inc	dptr
      004588 F0               [24]  528 	movx	@dptr,a
                                    529 ;	drivers/eeprom/eeprom_driver.c:49: eeprom_write_block(&value, addr, 4);
      004589 90 05 AD         [24]  530 	mov	dptr,#_eeprom_write_dword_addr_10000_87
      00458C E0               [24]  531 	movx	a,@dptr
      00458D FD               [12]  532 	mov	r5,a
      00458E A3               [24]  533 	inc	dptr
      00458F E0               [24]  534 	movx	a,@dptr
      004590 FE               [12]  535 	mov	r6,a
      004591 A3               [24]  536 	inc	dptr
      004592 E0               [24]  537 	movx	a,@dptr
      004593 FF               [12]  538 	mov	r7,a
      004594 90 05 48         [24]  539 	mov	dptr,#_eeprom_write_block_PARM_2
      004597 ED               [12]  540 	mov	a,r5
      004598 F0               [24]  541 	movx	@dptr,a
      004599 EE               [12]  542 	mov	a,r6
      00459A A3               [24]  543 	inc	dptr
      00459B F0               [24]  544 	movx	@dptr,a
      00459C EF               [12]  545 	mov	a,r7
      00459D A3               [24]  546 	inc	dptr
      00459E F0               [24]  547 	movx	@dptr,a
      00459F 90 05 4B         [24]  548 	mov	dptr,#_eeprom_write_block_PARM_3
      0045A2 74 04            [12]  549 	mov	a,#0x04
      0045A4 F0               [24]  550 	movx	@dptr,a
      0045A5 E4               [12]  551 	clr	a
      0045A6 A3               [24]  552 	inc	dptr
      0045A7 F0               [24]  553 	movx	@dptr,a
      0045A8 90 05 A9         [24]  554 	mov	dptr,#_eeprom_write_dword_PARM_2
      0045AB F5 F0            [12]  555 	mov	b,a
                                    556 ;	drivers/eeprom/eeprom_driver.c:50: }
      0045AD 02 3E 67         [24]  557 	ljmp	_eeprom_write_block
                                    558 ;------------------------------------------------------------
                                    559 ;Allocation info for local variables in function 'eeprom_update_block'
                                    560 ;------------------------------------------------------------
                                    561 ;sloc0         Allocated with name '_eeprom_update_block_sloc0_1_0'
                                    562 ;sloc1         Allocated with name '_eeprom_update_block_sloc1_1_0'
                                    563 ;sloc2         Allocated with name '_eeprom_update_block_sloc2_1_0'
                                    564 ;sloc3         Allocated with name '_eeprom_update_block_sloc3_1_0'
                                    565 ;addr          Allocated with name '_eeprom_update_block_PARM_2'
                                    566 ;len           Allocated with name '_eeprom_update_block_PARM_3'
                                    567 ;buf           Allocated with name '_eeprom_update_block_buf_10000_89'
                                    568 ;source        Allocated with name '_eeprom_update_block_source_10000_90'
                                    569 ;target        Allocated with name '_eeprom_update_block_target_10000_90'
                                    570 ;i             Allocated with name '_eeprom_update_block_i_10000_90'
                                    571 ;------------------------------------------------------------
                                    572 ;	drivers/eeprom/eeprom_driver.c:52: void eeprom_update_block(const void *buf, void *addr, size_t len) {
                                    573 ;	-----------------------------------------
                                    574 ;	 function eeprom_update_block
                                    575 ;	-----------------------------------------
      0045B0                        576 _eeprom_update_block:
      0045B0 AF F0            [24]  577 	mov	r7,b
      0045B2 AE 83            [24]  578 	mov	r6,dph
      0045B4 E5 82            [12]  579 	mov	a,dpl
      0045B6 90 05 B5         [24]  580 	mov	dptr,#_eeprom_update_block_buf_10000_89
      0045B9 F0               [24]  581 	movx	@dptr,a
      0045BA EE               [12]  582 	mov	a,r6
      0045BB A3               [24]  583 	inc	dptr
      0045BC F0               [24]  584 	movx	@dptr,a
      0045BD EF               [12]  585 	mov	a,r7
      0045BE A3               [24]  586 	inc	dptr
      0045BF F0               [24]  587 	movx	@dptr,a
                                    588 ;	drivers/eeprom/eeprom_driver.c:53: const uint8_t *source = (const uint8_t *)buf;
      0045C0 90 05 B5         [24]  589 	mov	dptr,#_eeprom_update_block_buf_10000_89
      0045C3 E0               [24]  590 	movx	a,@dptr
      0045C4 FD               [12]  591 	mov	r5,a
      0045C5 A3               [24]  592 	inc	dptr
      0045C6 E0               [24]  593 	movx	a,@dptr
      0045C7 FE               [12]  594 	mov	r6,a
      0045C8 A3               [24]  595 	inc	dptr
      0045C9 E0               [24]  596 	movx	a,@dptr
      0045CA FF               [12]  597 	mov	r7,a
                                    598 ;	drivers/eeprom/eeprom_driver.c:54: const uint8_t *target = (const uint8_t *)addr;
      0045CB 90 05 B0         [24]  599 	mov	dptr,#_eeprom_update_block_PARM_2
      0045CE E0               [24]  600 	movx	a,@dptr
      0045CF F5 14            [12]  601 	mov	_eeprom_update_block_sloc3_1_0,a
      0045D1 A3               [24]  602 	inc	dptr
      0045D2 E0               [24]  603 	movx	a,@dptr
      0045D3 F5 15            [12]  604 	mov	(_eeprom_update_block_sloc3_1_0 + 1),a
      0045D5 A3               [24]  605 	inc	dptr
      0045D6 E0               [24]  606 	movx	a,@dptr
      0045D7 F5 16            [12]  607 	mov	(_eeprom_update_block_sloc3_1_0 + 2),a
      0045D9 85 14 0E         [24]  608 	mov	_eeprom_update_block_sloc0_1_0,_eeprom_update_block_sloc3_1_0
      0045DC 85 15 0F         [24]  609 	mov	(_eeprom_update_block_sloc0_1_0 + 1),(_eeprom_update_block_sloc3_1_0 + 1)
      0045DF 85 16 10         [24]  610 	mov	(_eeprom_update_block_sloc0_1_0 + 2),(_eeprom_update_block_sloc3_1_0 + 2)
                                    611 ;	drivers/eeprom/eeprom_driver.c:58: for (i = 0; i < len; ++i) {
      0045E2 90 05 B3         [24]  612 	mov	dptr,#_eeprom_update_block_PARM_3
      0045E5 E0               [24]  613 	movx	a,@dptr
      0045E6 F8               [12]  614 	mov	r0,a
      0045E7 A3               [24]  615 	inc	dptr
      0045E8 E0               [24]  616 	movx	a,@dptr
      0045E9 F9               [12]  617 	mov	r1,a
      0045EA E4               [12]  618 	clr	a
      0045EB F5 11            [12]  619 	mov	_eeprom_update_block_sloc1_1_0,a
      0045ED F5 12            [12]  620 	mov	(_eeprom_update_block_sloc1_1_0 + 1),a
      0045EF                        621 00105$:
      0045EF C3               [12]  622 	clr	c
      0045F0 E5 11            [12]  623 	mov	a,_eeprom_update_block_sloc1_1_0
      0045F2 98               [12]  624 	subb	a,r0
      0045F3 E5 12            [12]  625 	mov	a,(_eeprom_update_block_sloc1_1_0 + 1)
      0045F5 99               [12]  626 	subb	a,r1
      0045F6 50 64            [24]  627 	jnc	00107$
                                    628 ;	drivers/eeprom/eeprom_driver.c:59: if (eeprom_read_byte(target + i) != source[i]) {
      0045F8 E5 11            [12]  629 	mov	a,_eeprom_update_block_sloc1_1_0
      0045FA 25 0E            [12]  630 	add	a, _eeprom_update_block_sloc0_1_0
      0045FC FA               [12]  631 	mov	r2,a
      0045FD E5 12            [12]  632 	mov	a,(_eeprom_update_block_sloc1_1_0 + 1)
      0045FF 35 0F            [12]  633 	addc	a, (_eeprom_update_block_sloc0_1_0 + 1)
      004601 FB               [12]  634 	mov	r3,a
      004602 AC 10            [24]  635 	mov	r4,(_eeprom_update_block_sloc0_1_0 + 2)
      004604 8A 82            [24]  636 	mov	dpl, r2
      004606 8B 83            [24]  637 	mov	dph, r3
      004608 8C F0            [24]  638 	mov	b, r4
      00460A 12 43 FC         [24]  639 	lcall	_eeprom_read_byte
      00460D 85 82 13         [24]  640 	mov	_eeprom_update_block_sloc2_1_0,dpl
      004610 E5 11            [12]  641 	mov	a,_eeprom_update_block_sloc1_1_0
      004612 2D               [12]  642 	add	a, r5
      004613 FA               [12]  643 	mov	r2,a
      004614 E5 12            [12]  644 	mov	a,(_eeprom_update_block_sloc1_1_0 + 1)
      004616 3E               [12]  645 	addc	a, r6
      004617 FB               [12]  646 	mov	r3,a
      004618 8F 04            [24]  647 	mov	ar4,r7
      00461A 8A 82            [24]  648 	mov	dpl,r2
      00461C 8B 83            [24]  649 	mov	dph,r3
      00461E 8C F0            [24]  650 	mov	b,r4
      004620 12 B5 78         [24]  651 	lcall	__gptrget
      004623 B5 13 02         [24]  652 	cjne	a,_eeprom_update_block_sloc2_1_0,00131$
      004626 80 2A            [24]  653 	sjmp	00106$
      004628                        654 00131$:
                                    655 ;	drivers/eeprom/eeprom_driver.c:60: eeprom_write_block(buf, addr, len);
      004628 90 05 B5         [24]  656 	mov	dptr,#_eeprom_update_block_buf_10000_89
      00462B E0               [24]  657 	movx	a,@dptr
      00462C FA               [12]  658 	mov	r2,a
      00462D A3               [24]  659 	inc	dptr
      00462E E0               [24]  660 	movx	a,@dptr
      00462F FB               [12]  661 	mov	r3,a
      004630 A3               [24]  662 	inc	dptr
      004631 E0               [24]  663 	movx	a,@dptr
      004632 FC               [12]  664 	mov	r4,a
      004633 90 05 48         [24]  665 	mov	dptr,#_eeprom_write_block_PARM_2
      004636 E5 14            [12]  666 	mov	a,_eeprom_update_block_sloc3_1_0
      004638 F0               [24]  667 	movx	@dptr,a
      004639 E5 15            [12]  668 	mov	a,(_eeprom_update_block_sloc3_1_0 + 1)
      00463B A3               [24]  669 	inc	dptr
      00463C F0               [24]  670 	movx	@dptr,a
      00463D E5 16            [12]  671 	mov	a,(_eeprom_update_block_sloc3_1_0 + 2)
      00463F A3               [24]  672 	inc	dptr
      004640 F0               [24]  673 	movx	@dptr,a
      004641 90 05 4B         [24]  674 	mov	dptr,#_eeprom_write_block_PARM_3
      004644 E8               [12]  675 	mov	a,r0
      004645 F0               [24]  676 	movx	@dptr,a
      004646 E9               [12]  677 	mov	a,r1
      004647 A3               [24]  678 	inc	dptr
      004648 F0               [24]  679 	movx	@dptr,a
      004649 8A 82            [24]  680 	mov	dpl, r2
      00464B 8B 83            [24]  681 	mov	dph, r3
      00464D 8C F0            [24]  682 	mov	b, r4
                                    683 ;	drivers/eeprom/eeprom_driver.c:61: return;
      00464F 02 3E 67         [24]  684 	ljmp	_eeprom_write_block
      004652                        685 00106$:
                                    686 ;	drivers/eeprom/eeprom_driver.c:58: for (i = 0; i < len; ++i) {
      004652 05 11            [12]  687 	inc	_eeprom_update_block_sloc1_1_0
      004654 E4               [12]  688 	clr	a
      004655 B5 11 97         [24]  689 	cjne	a,_eeprom_update_block_sloc1_1_0,00105$
      004658 05 12            [12]  690 	inc	(_eeprom_update_block_sloc1_1_0 + 1)
      00465A 80 93            [24]  691 	sjmp	00105$
      00465C                        692 00107$:
                                    693 ;	drivers/eeprom/eeprom_driver.c:64: }
      00465C 22               [24]  694 	ret
                                    695 ;------------------------------------------------------------
                                    696 ;Allocation info for local variables in function 'eeprom_update_byte'
                                    697 ;------------------------------------------------------------
                                    698 ;value         Allocated with name '_eeprom_update_byte_PARM_2'
                                    699 ;addr          Allocated with name '_eeprom_update_byte_addr_10000_95'
                                    700 ;orig          Allocated with name '_eeprom_update_byte_orig_10000_96'
                                    701 ;------------------------------------------------------------
                                    702 ;	drivers/eeprom/eeprom_driver.c:66: void eeprom_update_byte(uint8_t *addr, uint8_t value) {
                                    703 ;	-----------------------------------------
                                    704 ;	 function eeprom_update_byte
                                    705 ;	-----------------------------------------
      00465D                        706 _eeprom_update_byte:
      00465D C0 07            [24]  707 	push	ar7
      00465F C0 06            [24]  708 	push	ar6
      004661 C0 05            [24]  709 	push	ar5
      004663 C0 04            [24]  710 	push	ar4
      004665 AF F0            [24]  711 	mov	r7,b
      004667 AE 83            [24]  712 	mov	r6,dph
      004669 E5 82            [12]  713 	mov	a,dpl
      00466B 90 05 B9         [24]  714 	mov	dptr,#_eeprom_update_byte_addr_10000_95
      00466E F0               [24]  715 	movx	@dptr,a
      00466F EE               [12]  716 	mov	a,r6
      004670 A3               [24]  717 	inc	dptr
      004671 F0               [24]  718 	movx	@dptr,a
      004672 EF               [12]  719 	mov	a,r7
      004673 A3               [24]  720 	inc	dptr
      004674 F0               [24]  721 	movx	@dptr,a
                                    722 ;	drivers/eeprom/eeprom_driver.c:67: uint8_t orig = eeprom_read_byte(addr);
      004675 90 05 B9         [24]  723 	mov	dptr,#_eeprom_update_byte_addr_10000_95
      004678 E0               [24]  724 	movx	a,@dptr
      004679 FD               [12]  725 	mov	r5,a
      00467A A3               [24]  726 	inc	dptr
      00467B E0               [24]  727 	movx	a,@dptr
      00467C FE               [12]  728 	mov	r6,a
      00467D A3               [24]  729 	inc	dptr
      00467E E0               [24]  730 	movx	a,@dptr
      00467F FF               [12]  731 	mov	r7,a
      004680 8D 82            [24]  732 	mov	dpl, r5
      004682 8E 83            [24]  733 	mov	dph, r6
      004684 8F F0            [24]  734 	mov	b, r7
      004686 12 43 FC         [24]  735 	lcall	_eeprom_read_byte
      004689 AF 82            [24]  736 	mov	r7, dpl
                                    737 ;	drivers/eeprom/eeprom_driver.c:68: if (orig != value) {
      00468B 90 05 B8         [24]  738 	mov	dptr,#_eeprom_update_byte_PARM_2
      00468E E0               [24]  739 	movx	a,@dptr
      00468F FE               [12]  740 	mov	r6,a
      004690 EF               [12]  741 	mov	a,r7
      004691 B5 06 02         [24]  742 	cjne	a,ar6,00112$
      004694 80 39            [24]  743 	sjmp	00103$
      004696                        744 00112$:
                                    745 ;	drivers/eeprom/eeprom_driver.c:69: eeprom_write_byte(addr, value);
      004696 90 05 B9         [24]  746 	mov	dptr,#_eeprom_update_byte_addr_10000_95
      004699 E0               [24]  747 	movx	a,@dptr
      00469A FC               [12]  748 	mov	r4,a
      00469B A3               [24]  749 	inc	dptr
      00469C E0               [24]  750 	movx	a,@dptr
      00469D FD               [12]  751 	mov	r5,a
      00469E A3               [24]  752 	inc	dptr
      00469F E0               [24]  753 	movx	a,@dptr
      0046A0 FF               [12]  754 	mov	r7,a
      0046A1 90 05 A0         [24]  755 	mov	dptr,#_eeprom_write_byte_PARM_2
      0046A4 EE               [12]  756 	mov	a,r6
      0046A5 F0               [24]  757 	movx	@dptr,a
      0046A6 8C 82            [24]  758 	mov	dpl, r4
      0046A8 8D 83            [24]  759 	mov	dph, r5
      0046AA 8F F0            [24]  760 	mov	b, r7
      0046AC C0 07            [24]  761 	push	ar7
      0046AE C0 06            [24]  762 	push	ar6
      0046B0 C0 05            [24]  763 	push	ar5
      0046B2 C0 04            [24]  764 	push	ar4
      0046B4 C0 03            [24]  765 	push	ar3
      0046B6 C0 02            [24]  766 	push	ar2
      0046B8 C0 01            [24]  767 	push	ar1
      0046BA C0 00            [24]  768 	push	ar0
      0046BC 12 45 0B         [24]  769 	lcall	_eeprom_write_byte
      0046BF D0 00            [24]  770 	pop	ar0
      0046C1 D0 01            [24]  771 	pop	ar1
      0046C3 D0 02            [24]  772 	pop	ar2
      0046C5 D0 03            [24]  773 	pop	ar3
      0046C7 D0 04            [24]  774 	pop	ar4
      0046C9 D0 05            [24]  775 	pop	ar5
      0046CB D0 06            [24]  776 	pop	ar6
      0046CD D0 07            [24]  777 	pop	ar7
      0046CF                        778 00103$:
                                    779 ;	drivers/eeprom/eeprom_driver.c:71: }
      0046CF D0 04            [24]  780 	pop	ar4
      0046D1 D0 05            [24]  781 	pop	ar5
      0046D3 D0 06            [24]  782 	pop	ar6
      0046D5 D0 07            [24]  783 	pop	ar7
      0046D7 22               [24]  784 	ret
                                    785 ;------------------------------------------------------------
                                    786 ;Allocation info for local variables in function 'eeprom_update_word'
                                    787 ;------------------------------------------------------------
                                    788 ;value         Allocated with name '_eeprom_update_word_PARM_2'
                                    789 ;addr          Allocated with name '_eeprom_update_word_addr_10000_99'
                                    790 ;orig          Allocated with name '_eeprom_update_word_orig_10000_100'
                                    791 ;------------------------------------------------------------
                                    792 ;	drivers/eeprom/eeprom_driver.c:73: void eeprom_update_word(uint16_t *addr, uint16_t value) {
                                    793 ;	-----------------------------------------
                                    794 ;	 function eeprom_update_word
                                    795 ;	-----------------------------------------
      0046D8                        796 _eeprom_update_word:
      0046D8 AF F0            [24]  797 	mov	r7,b
      0046DA AE 83            [24]  798 	mov	r6,dph
      0046DC E5 82            [12]  799 	mov	a,dpl
      0046DE 90 05 BE         [24]  800 	mov	dptr,#_eeprom_update_word_addr_10000_99
      0046E1 F0               [24]  801 	movx	@dptr,a
      0046E2 EE               [12]  802 	mov	a,r6
      0046E3 A3               [24]  803 	inc	dptr
      0046E4 F0               [24]  804 	movx	@dptr,a
      0046E5 EF               [12]  805 	mov	a,r7
      0046E6 A3               [24]  806 	inc	dptr
      0046E7 F0               [24]  807 	movx	@dptr,a
                                    808 ;	drivers/eeprom/eeprom_driver.c:74: uint16_t orig = eeprom_read_word(addr);
      0046E8 90 05 BE         [24]  809 	mov	dptr,#_eeprom_update_word_addr_10000_99
      0046EB E0               [24]  810 	movx	a,@dptr
      0046EC FD               [12]  811 	mov	r5,a
      0046ED A3               [24]  812 	inc	dptr
      0046EE E0               [24]  813 	movx	a,@dptr
      0046EF FE               [12]  814 	mov	r6,a
      0046F0 A3               [24]  815 	inc	dptr
      0046F1 E0               [24]  816 	movx	a,@dptr
      0046F2 FF               [12]  817 	mov	r7,a
      0046F3 8D 82            [24]  818 	mov	dpl, r5
      0046F5 8E 83            [24]  819 	mov	dph, r6
      0046F7 8F F0            [24]  820 	mov	b, r7
      0046F9 12 44 6B         [24]  821 	lcall	_eeprom_read_word
      0046FC AE 82            [24]  822 	mov	r6, dpl
      0046FE AF 83            [24]  823 	mov	r7, dph
                                    824 ;	drivers/eeprom/eeprom_driver.c:75: if (orig != value) {
      004700 90 05 BC         [24]  825 	mov	dptr,#_eeprom_update_word_PARM_2
      004703 E0               [24]  826 	movx	a,@dptr
      004704 FC               [12]  827 	mov	r4,a
      004705 A3               [24]  828 	inc	dptr
      004706 E0               [24]  829 	movx	a,@dptr
      004707 FD               [12]  830 	mov	r5,a
      004708 EE               [12]  831 	mov	a,r6
      004709 B5 04 05         [24]  832 	cjne	a,ar4,00112$
      00470C EF               [12]  833 	mov	a,r7
      00470D B5 05 01         [24]  834 	cjne	a,ar5,00112$
      004710 22               [24]  835 	ret
      004711                        836 00112$:
                                    837 ;	drivers/eeprom/eeprom_driver.c:76: eeprom_write_word(addr, value);
      004711 90 05 BE         [24]  838 	mov	dptr,#_eeprom_update_word_addr_10000_99
      004714 E0               [24]  839 	movx	a,@dptr
      004715 FB               [12]  840 	mov	r3,a
      004716 A3               [24]  841 	inc	dptr
      004717 E0               [24]  842 	movx	a,@dptr
      004718 FE               [12]  843 	mov	r6,a
      004719 A3               [24]  844 	inc	dptr
      00471A E0               [24]  845 	movx	a,@dptr
      00471B FF               [12]  846 	mov	r7,a
      00471C 90 05 A4         [24]  847 	mov	dptr,#_eeprom_write_word_PARM_2
      00471F EC               [12]  848 	mov	a,r4
      004720 F0               [24]  849 	movx	@dptr,a
      004721 ED               [12]  850 	mov	a,r5
      004722 A3               [24]  851 	inc	dptr
      004723 F0               [24]  852 	movx	@dptr,a
      004724 8B 82            [24]  853 	mov	dpl, r3
      004726 8E 83            [24]  854 	mov	dph, r6
      004728 8F F0            [24]  855 	mov	b, r7
                                    856 ;	drivers/eeprom/eeprom_driver.c:78: }
      00472A 02 45 42         [24]  857 	ljmp	_eeprom_write_word
                                    858 ;------------------------------------------------------------
                                    859 ;Allocation info for local variables in function 'eeprom_update_dword'
                                    860 ;------------------------------------------------------------
                                    861 ;value         Allocated with name '_eeprom_update_dword_PARM_2'
                                    862 ;addr          Allocated with name '_eeprom_update_dword_addr_10000_103'
                                    863 ;orig          Allocated with name '_eeprom_update_dword_orig_10000_104'
                                    864 ;------------------------------------------------------------
                                    865 ;	drivers/eeprom/eeprom_driver.c:80: void eeprom_update_dword(uint32_t *addr, uint32_t value) {
                                    866 ;	-----------------------------------------
                                    867 ;	 function eeprom_update_dword
                                    868 ;	-----------------------------------------
      00472D                        869 _eeprom_update_dword:
      00472D AF F0            [24]  870 	mov	r7,b
      00472F AE 83            [24]  871 	mov	r6,dph
      004731 E5 82            [12]  872 	mov	a,dpl
      004733 90 05 C5         [24]  873 	mov	dptr,#_eeprom_update_dword_addr_10000_103
      004736 F0               [24]  874 	movx	@dptr,a
      004737 EE               [12]  875 	mov	a,r6
      004738 A3               [24]  876 	inc	dptr
      004739 F0               [24]  877 	movx	@dptr,a
      00473A EF               [12]  878 	mov	a,r7
      00473B A3               [24]  879 	inc	dptr
      00473C F0               [24]  880 	movx	@dptr,a
                                    881 ;	drivers/eeprom/eeprom_driver.c:81: uint32_t orig = eeprom_read_dword(addr);
      00473D 90 05 C5         [24]  882 	mov	dptr,#_eeprom_update_dword_addr_10000_103
      004740 E0               [24]  883 	movx	a,@dptr
      004741 FD               [12]  884 	mov	r5,a
      004742 A3               [24]  885 	inc	dptr
      004743 E0               [24]  886 	movx	a,@dptr
      004744 FE               [12]  887 	mov	r6,a
      004745 A3               [24]  888 	inc	dptr
      004746 E0               [24]  889 	movx	a,@dptr
      004747 FF               [12]  890 	mov	r7,a
      004748 8D 82            [24]  891 	mov	dpl, r5
      00474A 8E 83            [24]  892 	mov	dph, r6
      00474C 8F F0            [24]  893 	mov	b, r7
      00474E 12 44 B5         [24]  894 	lcall	_eeprom_read_dword
      004751 AC 82            [24]  895 	mov	r4, dpl
      004753 AD 83            [24]  896 	mov	r5, dph
      004755 AE F0            [24]  897 	mov	r6, b
      004757 FF               [12]  898 	mov	r7, a
                                    899 ;	drivers/eeprom/eeprom_driver.c:82: if (orig != value) {
      004758 90 05 C1         [24]  900 	mov	dptr,#_eeprom_update_dword_PARM_2
      00475B E0               [24]  901 	movx	a,@dptr
      00475C F8               [12]  902 	mov	r0,a
      00475D A3               [24]  903 	inc	dptr
      00475E E0               [24]  904 	movx	a,@dptr
      00475F F9               [12]  905 	mov	r1,a
      004760 A3               [24]  906 	inc	dptr
      004761 E0               [24]  907 	movx	a,@dptr
      004762 FA               [12]  908 	mov	r2,a
      004763 A3               [24]  909 	inc	dptr
      004764 E0               [24]  910 	movx	a,@dptr
      004765 FB               [12]  911 	mov	r3,a
      004766 EC               [12]  912 	mov	a,r4
      004767 B5 00 0D         [24]  913 	cjne	a,ar0,00112$
      00476A ED               [12]  914 	mov	a,r5
      00476B B5 01 09         [24]  915 	cjne	a,ar1,00112$
      00476E EE               [12]  916 	mov	a,r6
      00476F B5 02 05         [24]  917 	cjne	a,ar2,00112$
      004772 EF               [12]  918 	mov	a,r7
      004773 B5 03 01         [24]  919 	cjne	a,ar3,00112$
      004776 22               [24]  920 	ret
      004777                        921 00112$:
                                    922 ;	drivers/eeprom/eeprom_driver.c:83: eeprom_write_dword(addr, value);
      004777 90 05 C5         [24]  923 	mov	dptr,#_eeprom_update_dword_addr_10000_103
      00477A E0               [24]  924 	movx	a,@dptr
      00477B FD               [12]  925 	mov	r5,a
      00477C A3               [24]  926 	inc	dptr
      00477D E0               [24]  927 	movx	a,@dptr
      00477E FE               [12]  928 	mov	r6,a
      00477F A3               [24]  929 	inc	dptr
      004780 E0               [24]  930 	movx	a,@dptr
      004781 FF               [12]  931 	mov	r7,a
      004782 90 05 A9         [24]  932 	mov	dptr,#_eeprom_write_dword_PARM_2
      004785 E8               [12]  933 	mov	a,r0
      004786 F0               [24]  934 	movx	@dptr,a
      004787 E9               [12]  935 	mov	a,r1
      004788 A3               [24]  936 	inc	dptr
      004789 F0               [24]  937 	movx	@dptr,a
      00478A EA               [12]  938 	mov	a,r2
      00478B A3               [24]  939 	inc	dptr
      00478C F0               [24]  940 	movx	@dptr,a
      00478D EB               [12]  941 	mov	a,r3
      00478E A3               [24]  942 	inc	dptr
      00478F F0               [24]  943 	movx	@dptr,a
      004790 8D 82            [24]  944 	mov	dpl, r5
      004792 8E 83            [24]  945 	mov	dph, r6
      004794 8F F0            [24]  946 	mov	b, r7
                                    947 ;	drivers/eeprom/eeprom_driver.c:85: }
      004796 02 45 79         [24]  948 	ljmp	_eeprom_write_dword
                                    949 	.area CSEG    (CODE)
                                    950 	.area CONST   (CODE)
                                    951 	.area XINIT   (CODE)
                                    952 	.area CABS    (ABS,CODE)
