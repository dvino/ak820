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
      000591                         96 _eeprom_read_byte_addr_10000_77:
      000591                         97 	.ds 3
      000594                         98 _eeprom_read_byte_ret_10000_78:
      000594                         99 	.ds 1
      000595                        100 _eeprom_read_word_addr_10000_79:
      000595                        101 	.ds 3
      000598                        102 _eeprom_read_word_ret_10000_80:
      000598                        103 	.ds 2
      00059A                        104 _eeprom_read_dword_addr_10000_81:
      00059A                        105 	.ds 3
      00059D                        106 _eeprom_read_dword_ret_10000_82:
      00059D                        107 	.ds 4
      0005A1                        108 _eeprom_write_byte_PARM_2:
      0005A1                        109 	.ds 1
      0005A2                        110 _eeprom_write_byte_addr_10000_83:
      0005A2                        111 	.ds 3
      0005A5                        112 _eeprom_write_word_PARM_2:
      0005A5                        113 	.ds 2
      0005A7                        114 _eeprom_write_word_addr_10000_85:
      0005A7                        115 	.ds 3
      0005AA                        116 _eeprom_write_dword_PARM_2:
      0005AA                        117 	.ds 4
      0005AE                        118 _eeprom_write_dword_addr_10000_87:
      0005AE                        119 	.ds 3
      0005B1                        120 _eeprom_update_block_PARM_2:
      0005B1                        121 	.ds 3
      0005B4                        122 _eeprom_update_block_PARM_3:
      0005B4                        123 	.ds 2
      0005B6                        124 _eeprom_update_block_buf_10000_89:
      0005B6                        125 	.ds 3
      0005B9                        126 _eeprom_update_byte_PARM_2:
      0005B9                        127 	.ds 1
      0005BA                        128 _eeprom_update_byte_addr_10000_95:
      0005BA                        129 	.ds 3
      0005BD                        130 _eeprom_update_word_PARM_2:
      0005BD                        131 	.ds 2
      0005BF                        132 _eeprom_update_word_addr_10000_99:
      0005BF                        133 	.ds 3
      0005C2                        134 _eeprom_update_dword_PARM_2:
      0005C2                        135 	.ds 4
      0005C6                        136 _eeprom_update_dword_addr_10000_103:
      0005C6                        137 	.ds 3
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
      00441B                        182 _eeprom_read_byte:
                           000007   183 	ar7 = 0x07
                           000006   184 	ar6 = 0x06
                           000005   185 	ar5 = 0x05
                           000004   186 	ar4 = 0x04
                           000003   187 	ar3 = 0x03
                           000002   188 	ar2 = 0x02
                           000001   189 	ar1 = 0x01
                           000000   190 	ar0 = 0x00
      00441B C0 07            [24]  191 	push	ar7
      00441D C0 06            [24]  192 	push	ar6
      00441F C0 05            [24]  193 	push	ar5
      004421 AF F0            [24]  194 	mov	r7,b
      004423 AE 83            [24]  195 	mov	r6,dph
      004425 E5 82            [12]  196 	mov	a,dpl
      004427 90 05 91         [24]  197 	mov	dptr,#_eeprom_read_byte_addr_10000_77
      00442A F0               [24]  198 	movx	@dptr,a
      00442B EE               [12]  199 	mov	a,r6
      00442C A3               [24]  200 	inc	dptr
      00442D F0               [24]  201 	movx	@dptr,a
      00442E EF               [12]  202 	mov	a,r7
      00442F A3               [24]  203 	inc	dptr
      004430 F0               [24]  204 	movx	@dptr,a
                                    205 ;	drivers/eeprom/eeprom_driver.c:23: uint8_t ret = 0;
      004431 90 05 94         [24]  206 	mov	dptr,#_eeprom_read_byte_ret_10000_78
      004434 E4               [12]  207 	clr	a
      004435 F0               [24]  208 	movx	@dptr,a
                                    209 ;	drivers/eeprom/eeprom_driver.c:24: eeprom_read_block(&ret, addr, 1);
      004436 90 05 91         [24]  210 	mov	dptr,#_eeprom_read_byte_addr_10000_77
      004439 E0               [24]  211 	movx	a,@dptr
      00443A FD               [12]  212 	mov	r5,a
      00443B A3               [24]  213 	inc	dptr
      00443C E0               [24]  214 	movx	a,@dptr
      00443D FE               [12]  215 	mov	r6,a
      00443E A3               [24]  216 	inc	dptr
      00443F E0               [24]  217 	movx	a,@dptr
      004440 FF               [12]  218 	mov	r7,a
      004441 90 05 3E         [24]  219 	mov	dptr,#_eeprom_read_block_PARM_2
      004444 ED               [12]  220 	mov	a,r5
      004445 F0               [24]  221 	movx	@dptr,a
      004446 EE               [12]  222 	mov	a,r6
      004447 A3               [24]  223 	inc	dptr
      004448 F0               [24]  224 	movx	@dptr,a
      004449 EF               [12]  225 	mov	a,r7
      00444A A3               [24]  226 	inc	dptr
      00444B F0               [24]  227 	movx	@dptr,a
      00444C 90 05 41         [24]  228 	mov	dptr,#_eeprom_read_block_PARM_3
      00444F 74 01            [12]  229 	mov	a,#0x01
      004451 F0               [24]  230 	movx	@dptr,a
      004452 E4               [12]  231 	clr	a
      004453 A3               [24]  232 	inc	dptr
      004454 F0               [24]  233 	movx	@dptr,a
      004455 90 05 94         [24]  234 	mov	dptr,#_eeprom_read_byte_ret_10000_78
      004458 F5 F0            [12]  235 	mov	b,a
      00445A C0 07            [24]  236 	push	ar7
      00445C C0 06            [24]  237 	push	ar6
      00445E C0 05            [24]  238 	push	ar5
      004460 C0 04            [24]  239 	push	ar4
      004462 C0 03            [24]  240 	push	ar3
      004464 C0 02            [24]  241 	push	ar2
      004466 C0 01            [24]  242 	push	ar1
      004468 C0 00            [24]  243 	push	ar0
      00446A 12 3D 5C         [24]  244 	lcall	_eeprom_read_block
      00446D D0 00            [24]  245 	pop	ar0
      00446F D0 01            [24]  246 	pop	ar1
      004471 D0 02            [24]  247 	pop	ar2
      004473 D0 03            [24]  248 	pop	ar3
      004475 D0 04            [24]  249 	pop	ar4
      004477 D0 05            [24]  250 	pop	ar5
      004479 D0 06            [24]  251 	pop	ar6
      00447B D0 07            [24]  252 	pop	ar7
                                    253 ;	drivers/eeprom/eeprom_driver.c:25: return ret;
      00447D 90 05 94         [24]  254 	mov	dptr,#_eeprom_read_byte_ret_10000_78
      004480 E0               [24]  255 	movx	a,@dptr
      004481 F5 82            [12]  256 	mov	dpl,a
                                    257 ;	drivers/eeprom/eeprom_driver.c:26: }
      004483 D0 05            [24]  258 	pop	ar5
      004485 D0 06            [24]  259 	pop	ar6
      004487 D0 07            [24]  260 	pop	ar7
      004489 22               [24]  261 	ret
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
      00448A                        272 _eeprom_read_word:
      00448A AF F0            [24]  273 	mov	r7,b
      00448C AE 83            [24]  274 	mov	r6,dph
      00448E E5 82            [12]  275 	mov	a,dpl
      004490 90 05 95         [24]  276 	mov	dptr,#_eeprom_read_word_addr_10000_79
      004493 F0               [24]  277 	movx	@dptr,a
      004494 EE               [12]  278 	mov	a,r6
      004495 A3               [24]  279 	inc	dptr
      004496 F0               [24]  280 	movx	@dptr,a
      004497 EF               [12]  281 	mov	a,r7
      004498 A3               [24]  282 	inc	dptr
      004499 F0               [24]  283 	movx	@dptr,a
                                    284 ;	drivers/eeprom/eeprom_driver.c:29: uint16_t ret = 0;
      00449A 90 05 98         [24]  285 	mov	dptr,#_eeprom_read_word_ret_10000_80
      00449D E4               [12]  286 	clr	a
      00449E F0               [24]  287 	movx	@dptr,a
      00449F A3               [24]  288 	inc	dptr
      0044A0 F0               [24]  289 	movx	@dptr,a
                                    290 ;	drivers/eeprom/eeprom_driver.c:30: eeprom_read_block(&ret, addr, 2);
      0044A1 90 05 95         [24]  291 	mov	dptr,#_eeprom_read_word_addr_10000_79
      0044A4 E0               [24]  292 	movx	a,@dptr
      0044A5 FD               [12]  293 	mov	r5,a
      0044A6 A3               [24]  294 	inc	dptr
      0044A7 E0               [24]  295 	movx	a,@dptr
      0044A8 FE               [12]  296 	mov	r6,a
      0044A9 A3               [24]  297 	inc	dptr
      0044AA E0               [24]  298 	movx	a,@dptr
      0044AB FF               [12]  299 	mov	r7,a
      0044AC 90 05 3E         [24]  300 	mov	dptr,#_eeprom_read_block_PARM_2
      0044AF ED               [12]  301 	mov	a,r5
      0044B0 F0               [24]  302 	movx	@dptr,a
      0044B1 EE               [12]  303 	mov	a,r6
      0044B2 A3               [24]  304 	inc	dptr
      0044B3 F0               [24]  305 	movx	@dptr,a
      0044B4 EF               [12]  306 	mov	a,r7
      0044B5 A3               [24]  307 	inc	dptr
      0044B6 F0               [24]  308 	movx	@dptr,a
      0044B7 90 05 41         [24]  309 	mov	dptr,#_eeprom_read_block_PARM_3
      0044BA 74 02            [12]  310 	mov	a,#0x02
      0044BC F0               [24]  311 	movx	@dptr,a
      0044BD E4               [12]  312 	clr	a
      0044BE A3               [24]  313 	inc	dptr
      0044BF F0               [24]  314 	movx	@dptr,a
      0044C0 90 05 98         [24]  315 	mov	dptr,#_eeprom_read_word_ret_10000_80
      0044C3 F5 F0            [12]  316 	mov	b,a
      0044C5 12 3D 5C         [24]  317 	lcall	_eeprom_read_block
                                    318 ;	drivers/eeprom/eeprom_driver.c:31: return ret;
      0044C8 90 05 98         [24]  319 	mov	dptr,#_eeprom_read_word_ret_10000_80
      0044CB E0               [24]  320 	movx	a,@dptr
      0044CC FE               [12]  321 	mov	r6,a
      0044CD A3               [24]  322 	inc	dptr
      0044CE E0               [24]  323 	movx	a,@dptr
                                    324 ;	drivers/eeprom/eeprom_driver.c:32: }
      0044CF 8E 82            [24]  325 	mov	dpl,r6
      0044D1 F5 83            [12]  326 	mov	dph,a
      0044D3 22               [24]  327 	ret
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
      0044D4                        338 _eeprom_read_dword:
      0044D4 AF F0            [24]  339 	mov	r7,b
      0044D6 AE 83            [24]  340 	mov	r6,dph
      0044D8 E5 82            [12]  341 	mov	a,dpl
      0044DA 90 05 9A         [24]  342 	mov	dptr,#_eeprom_read_dword_addr_10000_81
      0044DD F0               [24]  343 	movx	@dptr,a
      0044DE EE               [12]  344 	mov	a,r6
      0044DF A3               [24]  345 	inc	dptr
      0044E0 F0               [24]  346 	movx	@dptr,a
      0044E1 EF               [12]  347 	mov	a,r7
      0044E2 A3               [24]  348 	inc	dptr
      0044E3 F0               [24]  349 	movx	@dptr,a
                                    350 ;	drivers/eeprom/eeprom_driver.c:35: uint32_t ret = 0;
      0044E4 90 05 9D         [24]  351 	mov	dptr,#_eeprom_read_dword_ret_10000_82
      0044E7 E4               [12]  352 	clr	a
      0044E8 F0               [24]  353 	movx	@dptr,a
      0044E9 A3               [24]  354 	inc	dptr
      0044EA F0               [24]  355 	movx	@dptr,a
      0044EB A3               [24]  356 	inc	dptr
      0044EC F0               [24]  357 	movx	@dptr,a
      0044ED A3               [24]  358 	inc	dptr
      0044EE F0               [24]  359 	movx	@dptr,a
                                    360 ;	drivers/eeprom/eeprom_driver.c:36: eeprom_read_block(&ret, addr, 4);
      0044EF 90 05 9A         [24]  361 	mov	dptr,#_eeprom_read_dword_addr_10000_81
      0044F2 E0               [24]  362 	movx	a,@dptr
      0044F3 FD               [12]  363 	mov	r5,a
      0044F4 A3               [24]  364 	inc	dptr
      0044F5 E0               [24]  365 	movx	a,@dptr
      0044F6 FE               [12]  366 	mov	r6,a
      0044F7 A3               [24]  367 	inc	dptr
      0044F8 E0               [24]  368 	movx	a,@dptr
      0044F9 FF               [12]  369 	mov	r7,a
      0044FA 90 05 3E         [24]  370 	mov	dptr,#_eeprom_read_block_PARM_2
      0044FD ED               [12]  371 	mov	a,r5
      0044FE F0               [24]  372 	movx	@dptr,a
      0044FF EE               [12]  373 	mov	a,r6
      004500 A3               [24]  374 	inc	dptr
      004501 F0               [24]  375 	movx	@dptr,a
      004502 EF               [12]  376 	mov	a,r7
      004503 A3               [24]  377 	inc	dptr
      004504 F0               [24]  378 	movx	@dptr,a
      004505 90 05 41         [24]  379 	mov	dptr,#_eeprom_read_block_PARM_3
      004508 74 04            [12]  380 	mov	a,#0x04
      00450A F0               [24]  381 	movx	@dptr,a
      00450B E4               [12]  382 	clr	a
      00450C A3               [24]  383 	inc	dptr
      00450D F0               [24]  384 	movx	@dptr,a
      00450E 90 05 9D         [24]  385 	mov	dptr,#_eeprom_read_dword_ret_10000_82
      004511 F5 F0            [12]  386 	mov	b,a
      004513 12 3D 5C         [24]  387 	lcall	_eeprom_read_block
                                    388 ;	drivers/eeprom/eeprom_driver.c:37: return ret;
      004516 90 05 9D         [24]  389 	mov	dptr,#_eeprom_read_dword_ret_10000_82
      004519 E0               [24]  390 	movx	a,@dptr
      00451A FC               [12]  391 	mov	r4,a
      00451B A3               [24]  392 	inc	dptr
      00451C E0               [24]  393 	movx	a,@dptr
      00451D FD               [12]  394 	mov	r5,a
      00451E A3               [24]  395 	inc	dptr
      00451F E0               [24]  396 	movx	a,@dptr
      004520 FE               [12]  397 	mov	r6,a
      004521 A3               [24]  398 	inc	dptr
      004522 E0               [24]  399 	movx	a,@dptr
      004523 8C 82            [24]  400 	mov	dpl,r4
      004525 8D 83            [24]  401 	mov	dph,r5
      004527 8E F0            [24]  402 	mov	b,r6
                                    403 ;	drivers/eeprom/eeprom_driver.c:38: }
      004529 22               [24]  404 	ret
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
      00452A                        415 _eeprom_write_byte:
      00452A AF F0            [24]  416 	mov	r7,b
      00452C AE 83            [24]  417 	mov	r6,dph
      00452E E5 82            [12]  418 	mov	a,dpl
      004530 90 05 A2         [24]  419 	mov	dptr,#_eeprom_write_byte_addr_10000_83
      004533 F0               [24]  420 	movx	@dptr,a
      004534 EE               [12]  421 	mov	a,r6
      004535 A3               [24]  422 	inc	dptr
      004536 F0               [24]  423 	movx	@dptr,a
      004537 EF               [12]  424 	mov	a,r7
      004538 A3               [24]  425 	inc	dptr
      004539 F0               [24]  426 	movx	@dptr,a
                                    427 ;	drivers/eeprom/eeprom_driver.c:41: eeprom_write_block(&value, addr, 1);
      00453A 90 05 A2         [24]  428 	mov	dptr,#_eeprom_write_byte_addr_10000_83
      00453D E0               [24]  429 	movx	a,@dptr
      00453E FD               [12]  430 	mov	r5,a
      00453F A3               [24]  431 	inc	dptr
      004540 E0               [24]  432 	movx	a,@dptr
      004541 FE               [12]  433 	mov	r6,a
      004542 A3               [24]  434 	inc	dptr
      004543 E0               [24]  435 	movx	a,@dptr
      004544 FF               [12]  436 	mov	r7,a
      004545 90 05 49         [24]  437 	mov	dptr,#_eeprom_write_block_PARM_2
      004548 ED               [12]  438 	mov	a,r5
      004549 F0               [24]  439 	movx	@dptr,a
      00454A EE               [12]  440 	mov	a,r6
      00454B A3               [24]  441 	inc	dptr
      00454C F0               [24]  442 	movx	@dptr,a
      00454D EF               [12]  443 	mov	a,r7
      00454E A3               [24]  444 	inc	dptr
      00454F F0               [24]  445 	movx	@dptr,a
      004550 90 05 4C         [24]  446 	mov	dptr,#_eeprom_write_block_PARM_3
      004553 74 01            [12]  447 	mov	a,#0x01
      004555 F0               [24]  448 	movx	@dptr,a
      004556 E4               [12]  449 	clr	a
      004557 A3               [24]  450 	inc	dptr
      004558 F0               [24]  451 	movx	@dptr,a
      004559 90 05 A1         [24]  452 	mov	dptr,#_eeprom_write_byte_PARM_2
      00455C F5 F0            [12]  453 	mov	b,a
                                    454 ;	drivers/eeprom/eeprom_driver.c:42: }
      00455E 02 3E 86         [24]  455 	ljmp	_eeprom_write_block
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
      004561                        466 _eeprom_write_word:
      004561 AF F0            [24]  467 	mov	r7,b
      004563 AE 83            [24]  468 	mov	r6,dph
      004565 E5 82            [12]  469 	mov	a,dpl
      004567 90 05 A7         [24]  470 	mov	dptr,#_eeprom_write_word_addr_10000_85
      00456A F0               [24]  471 	movx	@dptr,a
      00456B EE               [12]  472 	mov	a,r6
      00456C A3               [24]  473 	inc	dptr
      00456D F0               [24]  474 	movx	@dptr,a
      00456E EF               [12]  475 	mov	a,r7
      00456F A3               [24]  476 	inc	dptr
      004570 F0               [24]  477 	movx	@dptr,a
                                    478 ;	drivers/eeprom/eeprom_driver.c:45: eeprom_write_block(&value, addr, 2);
      004571 90 05 A7         [24]  479 	mov	dptr,#_eeprom_write_word_addr_10000_85
      004574 E0               [24]  480 	movx	a,@dptr
      004575 FD               [12]  481 	mov	r5,a
      004576 A3               [24]  482 	inc	dptr
      004577 E0               [24]  483 	movx	a,@dptr
      004578 FE               [12]  484 	mov	r6,a
      004579 A3               [24]  485 	inc	dptr
      00457A E0               [24]  486 	movx	a,@dptr
      00457B FF               [12]  487 	mov	r7,a
      00457C 90 05 49         [24]  488 	mov	dptr,#_eeprom_write_block_PARM_2
      00457F ED               [12]  489 	mov	a,r5
      004580 F0               [24]  490 	movx	@dptr,a
      004581 EE               [12]  491 	mov	a,r6
      004582 A3               [24]  492 	inc	dptr
      004583 F0               [24]  493 	movx	@dptr,a
      004584 EF               [12]  494 	mov	a,r7
      004585 A3               [24]  495 	inc	dptr
      004586 F0               [24]  496 	movx	@dptr,a
      004587 90 05 4C         [24]  497 	mov	dptr,#_eeprom_write_block_PARM_3
      00458A 74 02            [12]  498 	mov	a,#0x02
      00458C F0               [24]  499 	movx	@dptr,a
      00458D E4               [12]  500 	clr	a
      00458E A3               [24]  501 	inc	dptr
      00458F F0               [24]  502 	movx	@dptr,a
      004590 90 05 A5         [24]  503 	mov	dptr,#_eeprom_write_word_PARM_2
      004593 F5 F0            [12]  504 	mov	b,a
                                    505 ;	drivers/eeprom/eeprom_driver.c:46: }
      004595 02 3E 86         [24]  506 	ljmp	_eeprom_write_block
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
      004598                        517 _eeprom_write_dword:
      004598 AF F0            [24]  518 	mov	r7,b
      00459A AE 83            [24]  519 	mov	r6,dph
      00459C E5 82            [12]  520 	mov	a,dpl
      00459E 90 05 AE         [24]  521 	mov	dptr,#_eeprom_write_dword_addr_10000_87
      0045A1 F0               [24]  522 	movx	@dptr,a
      0045A2 EE               [12]  523 	mov	a,r6
      0045A3 A3               [24]  524 	inc	dptr
      0045A4 F0               [24]  525 	movx	@dptr,a
      0045A5 EF               [12]  526 	mov	a,r7
      0045A6 A3               [24]  527 	inc	dptr
      0045A7 F0               [24]  528 	movx	@dptr,a
                                    529 ;	drivers/eeprom/eeprom_driver.c:49: eeprom_write_block(&value, addr, 4);
      0045A8 90 05 AE         [24]  530 	mov	dptr,#_eeprom_write_dword_addr_10000_87
      0045AB E0               [24]  531 	movx	a,@dptr
      0045AC FD               [12]  532 	mov	r5,a
      0045AD A3               [24]  533 	inc	dptr
      0045AE E0               [24]  534 	movx	a,@dptr
      0045AF FE               [12]  535 	mov	r6,a
      0045B0 A3               [24]  536 	inc	dptr
      0045B1 E0               [24]  537 	movx	a,@dptr
      0045B2 FF               [12]  538 	mov	r7,a
      0045B3 90 05 49         [24]  539 	mov	dptr,#_eeprom_write_block_PARM_2
      0045B6 ED               [12]  540 	mov	a,r5
      0045B7 F0               [24]  541 	movx	@dptr,a
      0045B8 EE               [12]  542 	mov	a,r6
      0045B9 A3               [24]  543 	inc	dptr
      0045BA F0               [24]  544 	movx	@dptr,a
      0045BB EF               [12]  545 	mov	a,r7
      0045BC A3               [24]  546 	inc	dptr
      0045BD F0               [24]  547 	movx	@dptr,a
      0045BE 90 05 4C         [24]  548 	mov	dptr,#_eeprom_write_block_PARM_3
      0045C1 74 04            [12]  549 	mov	a,#0x04
      0045C3 F0               [24]  550 	movx	@dptr,a
      0045C4 E4               [12]  551 	clr	a
      0045C5 A3               [24]  552 	inc	dptr
      0045C6 F0               [24]  553 	movx	@dptr,a
      0045C7 90 05 AA         [24]  554 	mov	dptr,#_eeprom_write_dword_PARM_2
      0045CA F5 F0            [12]  555 	mov	b,a
                                    556 ;	drivers/eeprom/eeprom_driver.c:50: }
      0045CC 02 3E 86         [24]  557 	ljmp	_eeprom_write_block
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
      0045CF                        576 _eeprom_update_block:
      0045CF AF F0            [24]  577 	mov	r7,b
      0045D1 AE 83            [24]  578 	mov	r6,dph
      0045D3 E5 82            [12]  579 	mov	a,dpl
      0045D5 90 05 B6         [24]  580 	mov	dptr,#_eeprom_update_block_buf_10000_89
      0045D8 F0               [24]  581 	movx	@dptr,a
      0045D9 EE               [12]  582 	mov	a,r6
      0045DA A3               [24]  583 	inc	dptr
      0045DB F0               [24]  584 	movx	@dptr,a
      0045DC EF               [12]  585 	mov	a,r7
      0045DD A3               [24]  586 	inc	dptr
      0045DE F0               [24]  587 	movx	@dptr,a
                                    588 ;	drivers/eeprom/eeprom_driver.c:53: const uint8_t *source = (const uint8_t *)buf;
      0045DF 90 05 B6         [24]  589 	mov	dptr,#_eeprom_update_block_buf_10000_89
      0045E2 E0               [24]  590 	movx	a,@dptr
      0045E3 FD               [12]  591 	mov	r5,a
      0045E4 A3               [24]  592 	inc	dptr
      0045E5 E0               [24]  593 	movx	a,@dptr
      0045E6 FE               [12]  594 	mov	r6,a
      0045E7 A3               [24]  595 	inc	dptr
      0045E8 E0               [24]  596 	movx	a,@dptr
      0045E9 FF               [12]  597 	mov	r7,a
                                    598 ;	drivers/eeprom/eeprom_driver.c:54: const uint8_t *target = (const uint8_t *)addr;
      0045EA 90 05 B1         [24]  599 	mov	dptr,#_eeprom_update_block_PARM_2
      0045ED E0               [24]  600 	movx	a,@dptr
      0045EE F5 14            [12]  601 	mov	_eeprom_update_block_sloc3_1_0,a
      0045F0 A3               [24]  602 	inc	dptr
      0045F1 E0               [24]  603 	movx	a,@dptr
      0045F2 F5 15            [12]  604 	mov	(_eeprom_update_block_sloc3_1_0 + 1),a
      0045F4 A3               [24]  605 	inc	dptr
      0045F5 E0               [24]  606 	movx	a,@dptr
      0045F6 F5 16            [12]  607 	mov	(_eeprom_update_block_sloc3_1_0 + 2),a
      0045F8 85 14 0E         [24]  608 	mov	_eeprom_update_block_sloc0_1_0,_eeprom_update_block_sloc3_1_0
      0045FB 85 15 0F         [24]  609 	mov	(_eeprom_update_block_sloc0_1_0 + 1),(_eeprom_update_block_sloc3_1_0 + 1)
      0045FE 85 16 10         [24]  610 	mov	(_eeprom_update_block_sloc0_1_0 + 2),(_eeprom_update_block_sloc3_1_0 + 2)
                                    611 ;	drivers/eeprom/eeprom_driver.c:58: for (i = 0; i < len; ++i) {
      004601 90 05 B4         [24]  612 	mov	dptr,#_eeprom_update_block_PARM_3
      004604 E0               [24]  613 	movx	a,@dptr
      004605 F8               [12]  614 	mov	r0,a
      004606 A3               [24]  615 	inc	dptr
      004607 E0               [24]  616 	movx	a,@dptr
      004608 F9               [12]  617 	mov	r1,a
      004609 E4               [12]  618 	clr	a
      00460A F5 11            [12]  619 	mov	_eeprom_update_block_sloc1_1_0,a
      00460C F5 12            [12]  620 	mov	(_eeprom_update_block_sloc1_1_0 + 1),a
      00460E                        621 00105$:
      00460E C3               [12]  622 	clr	c
      00460F E5 11            [12]  623 	mov	a,_eeprom_update_block_sloc1_1_0
      004611 98               [12]  624 	subb	a,r0
      004612 E5 12            [12]  625 	mov	a,(_eeprom_update_block_sloc1_1_0 + 1)
      004614 99               [12]  626 	subb	a,r1
      004615 50 64            [24]  627 	jnc	00107$
                                    628 ;	drivers/eeprom/eeprom_driver.c:59: if (eeprom_read_byte(target + i) != source[i]) {
      004617 E5 11            [12]  629 	mov	a,_eeprom_update_block_sloc1_1_0
      004619 25 0E            [12]  630 	add	a, _eeprom_update_block_sloc0_1_0
      00461B FA               [12]  631 	mov	r2,a
      00461C E5 12            [12]  632 	mov	a,(_eeprom_update_block_sloc1_1_0 + 1)
      00461E 35 0F            [12]  633 	addc	a, (_eeprom_update_block_sloc0_1_0 + 1)
      004620 FB               [12]  634 	mov	r3,a
      004621 AC 10            [24]  635 	mov	r4,(_eeprom_update_block_sloc0_1_0 + 2)
      004623 8A 82            [24]  636 	mov	dpl, r2
      004625 8B 83            [24]  637 	mov	dph, r3
      004627 8C F0            [24]  638 	mov	b, r4
      004629 12 44 1B         [24]  639 	lcall	_eeprom_read_byte
      00462C 85 82 13         [24]  640 	mov	_eeprom_update_block_sloc2_1_0,dpl
      00462F E5 11            [12]  641 	mov	a,_eeprom_update_block_sloc1_1_0
      004631 2D               [12]  642 	add	a, r5
      004632 FA               [12]  643 	mov	r2,a
      004633 E5 12            [12]  644 	mov	a,(_eeprom_update_block_sloc1_1_0 + 1)
      004635 3E               [12]  645 	addc	a, r6
      004636 FB               [12]  646 	mov	r3,a
      004637 8F 04            [24]  647 	mov	ar4,r7
      004639 8A 82            [24]  648 	mov	dpl,r2
      00463B 8B 83            [24]  649 	mov	dph,r3
      00463D 8C F0            [24]  650 	mov	b,r4
      00463F 12 B5 97         [24]  651 	lcall	__gptrget
      004642 B5 13 02         [24]  652 	cjne	a,_eeprom_update_block_sloc2_1_0,00131$
      004645 80 2A            [24]  653 	sjmp	00106$
      004647                        654 00131$:
                                    655 ;	drivers/eeprom/eeprom_driver.c:60: eeprom_write_block(buf, addr, len);
      004647 90 05 B6         [24]  656 	mov	dptr,#_eeprom_update_block_buf_10000_89
      00464A E0               [24]  657 	movx	a,@dptr
      00464B FA               [12]  658 	mov	r2,a
      00464C A3               [24]  659 	inc	dptr
      00464D E0               [24]  660 	movx	a,@dptr
      00464E FB               [12]  661 	mov	r3,a
      00464F A3               [24]  662 	inc	dptr
      004650 E0               [24]  663 	movx	a,@dptr
      004651 FC               [12]  664 	mov	r4,a
      004652 90 05 49         [24]  665 	mov	dptr,#_eeprom_write_block_PARM_2
      004655 E5 14            [12]  666 	mov	a,_eeprom_update_block_sloc3_1_0
      004657 F0               [24]  667 	movx	@dptr,a
      004658 E5 15            [12]  668 	mov	a,(_eeprom_update_block_sloc3_1_0 + 1)
      00465A A3               [24]  669 	inc	dptr
      00465B F0               [24]  670 	movx	@dptr,a
      00465C E5 16            [12]  671 	mov	a,(_eeprom_update_block_sloc3_1_0 + 2)
      00465E A3               [24]  672 	inc	dptr
      00465F F0               [24]  673 	movx	@dptr,a
      004660 90 05 4C         [24]  674 	mov	dptr,#_eeprom_write_block_PARM_3
      004663 E8               [12]  675 	mov	a,r0
      004664 F0               [24]  676 	movx	@dptr,a
      004665 E9               [12]  677 	mov	a,r1
      004666 A3               [24]  678 	inc	dptr
      004667 F0               [24]  679 	movx	@dptr,a
      004668 8A 82            [24]  680 	mov	dpl, r2
      00466A 8B 83            [24]  681 	mov	dph, r3
      00466C 8C F0            [24]  682 	mov	b, r4
                                    683 ;	drivers/eeprom/eeprom_driver.c:61: return;
      00466E 02 3E 86         [24]  684 	ljmp	_eeprom_write_block
      004671                        685 00106$:
                                    686 ;	drivers/eeprom/eeprom_driver.c:58: for (i = 0; i < len; ++i) {
      004671 05 11            [12]  687 	inc	_eeprom_update_block_sloc1_1_0
      004673 E4               [12]  688 	clr	a
      004674 B5 11 97         [24]  689 	cjne	a,_eeprom_update_block_sloc1_1_0,00105$
      004677 05 12            [12]  690 	inc	(_eeprom_update_block_sloc1_1_0 + 1)
      004679 80 93            [24]  691 	sjmp	00105$
      00467B                        692 00107$:
                                    693 ;	drivers/eeprom/eeprom_driver.c:64: }
      00467B 22               [24]  694 	ret
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
      00467C                        706 _eeprom_update_byte:
      00467C C0 07            [24]  707 	push	ar7
      00467E C0 06            [24]  708 	push	ar6
      004680 C0 05            [24]  709 	push	ar5
      004682 C0 04            [24]  710 	push	ar4
      004684 AF F0            [24]  711 	mov	r7,b
      004686 AE 83            [24]  712 	mov	r6,dph
      004688 E5 82            [12]  713 	mov	a,dpl
      00468A 90 05 BA         [24]  714 	mov	dptr,#_eeprom_update_byte_addr_10000_95
      00468D F0               [24]  715 	movx	@dptr,a
      00468E EE               [12]  716 	mov	a,r6
      00468F A3               [24]  717 	inc	dptr
      004690 F0               [24]  718 	movx	@dptr,a
      004691 EF               [12]  719 	mov	a,r7
      004692 A3               [24]  720 	inc	dptr
      004693 F0               [24]  721 	movx	@dptr,a
                                    722 ;	drivers/eeprom/eeprom_driver.c:67: uint8_t orig = eeprom_read_byte(addr);
      004694 90 05 BA         [24]  723 	mov	dptr,#_eeprom_update_byte_addr_10000_95
      004697 E0               [24]  724 	movx	a,@dptr
      004698 FD               [12]  725 	mov	r5,a
      004699 A3               [24]  726 	inc	dptr
      00469A E0               [24]  727 	movx	a,@dptr
      00469B FE               [12]  728 	mov	r6,a
      00469C A3               [24]  729 	inc	dptr
      00469D E0               [24]  730 	movx	a,@dptr
      00469E FF               [12]  731 	mov	r7,a
      00469F 8D 82            [24]  732 	mov	dpl, r5
      0046A1 8E 83            [24]  733 	mov	dph, r6
      0046A3 8F F0            [24]  734 	mov	b, r7
      0046A5 12 44 1B         [24]  735 	lcall	_eeprom_read_byte
      0046A8 AF 82            [24]  736 	mov	r7, dpl
                                    737 ;	drivers/eeprom/eeprom_driver.c:68: if (orig != value) {
      0046AA 90 05 B9         [24]  738 	mov	dptr,#_eeprom_update_byte_PARM_2
      0046AD E0               [24]  739 	movx	a,@dptr
      0046AE FE               [12]  740 	mov	r6,a
      0046AF EF               [12]  741 	mov	a,r7
      0046B0 B5 06 02         [24]  742 	cjne	a,ar6,00112$
      0046B3 80 39            [24]  743 	sjmp	00103$
      0046B5                        744 00112$:
                                    745 ;	drivers/eeprom/eeprom_driver.c:69: eeprom_write_byte(addr, value);
      0046B5 90 05 BA         [24]  746 	mov	dptr,#_eeprom_update_byte_addr_10000_95
      0046B8 E0               [24]  747 	movx	a,@dptr
      0046B9 FC               [12]  748 	mov	r4,a
      0046BA A3               [24]  749 	inc	dptr
      0046BB E0               [24]  750 	movx	a,@dptr
      0046BC FD               [12]  751 	mov	r5,a
      0046BD A3               [24]  752 	inc	dptr
      0046BE E0               [24]  753 	movx	a,@dptr
      0046BF FF               [12]  754 	mov	r7,a
      0046C0 90 05 A1         [24]  755 	mov	dptr,#_eeprom_write_byte_PARM_2
      0046C3 EE               [12]  756 	mov	a,r6
      0046C4 F0               [24]  757 	movx	@dptr,a
      0046C5 8C 82            [24]  758 	mov	dpl, r4
      0046C7 8D 83            [24]  759 	mov	dph, r5
      0046C9 8F F0            [24]  760 	mov	b, r7
      0046CB C0 07            [24]  761 	push	ar7
      0046CD C0 06            [24]  762 	push	ar6
      0046CF C0 05            [24]  763 	push	ar5
      0046D1 C0 04            [24]  764 	push	ar4
      0046D3 C0 03            [24]  765 	push	ar3
      0046D5 C0 02            [24]  766 	push	ar2
      0046D7 C0 01            [24]  767 	push	ar1
      0046D9 C0 00            [24]  768 	push	ar0
      0046DB 12 45 2A         [24]  769 	lcall	_eeprom_write_byte
      0046DE D0 00            [24]  770 	pop	ar0
      0046E0 D0 01            [24]  771 	pop	ar1
      0046E2 D0 02            [24]  772 	pop	ar2
      0046E4 D0 03            [24]  773 	pop	ar3
      0046E6 D0 04            [24]  774 	pop	ar4
      0046E8 D0 05            [24]  775 	pop	ar5
      0046EA D0 06            [24]  776 	pop	ar6
      0046EC D0 07            [24]  777 	pop	ar7
      0046EE                        778 00103$:
                                    779 ;	drivers/eeprom/eeprom_driver.c:71: }
      0046EE D0 04            [24]  780 	pop	ar4
      0046F0 D0 05            [24]  781 	pop	ar5
      0046F2 D0 06            [24]  782 	pop	ar6
      0046F4 D0 07            [24]  783 	pop	ar7
      0046F6 22               [24]  784 	ret
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
      0046F7                        796 _eeprom_update_word:
      0046F7 AF F0            [24]  797 	mov	r7,b
      0046F9 AE 83            [24]  798 	mov	r6,dph
      0046FB E5 82            [12]  799 	mov	a,dpl
      0046FD 90 05 BF         [24]  800 	mov	dptr,#_eeprom_update_word_addr_10000_99
      004700 F0               [24]  801 	movx	@dptr,a
      004701 EE               [12]  802 	mov	a,r6
      004702 A3               [24]  803 	inc	dptr
      004703 F0               [24]  804 	movx	@dptr,a
      004704 EF               [12]  805 	mov	a,r7
      004705 A3               [24]  806 	inc	dptr
      004706 F0               [24]  807 	movx	@dptr,a
                                    808 ;	drivers/eeprom/eeprom_driver.c:74: uint16_t orig = eeprom_read_word(addr);
      004707 90 05 BF         [24]  809 	mov	dptr,#_eeprom_update_word_addr_10000_99
      00470A E0               [24]  810 	movx	a,@dptr
      00470B FD               [12]  811 	mov	r5,a
      00470C A3               [24]  812 	inc	dptr
      00470D E0               [24]  813 	movx	a,@dptr
      00470E FE               [12]  814 	mov	r6,a
      00470F A3               [24]  815 	inc	dptr
      004710 E0               [24]  816 	movx	a,@dptr
      004711 FF               [12]  817 	mov	r7,a
      004712 8D 82            [24]  818 	mov	dpl, r5
      004714 8E 83            [24]  819 	mov	dph, r6
      004716 8F F0            [24]  820 	mov	b, r7
      004718 12 44 8A         [24]  821 	lcall	_eeprom_read_word
      00471B AE 82            [24]  822 	mov	r6, dpl
      00471D AF 83            [24]  823 	mov	r7, dph
                                    824 ;	drivers/eeprom/eeprom_driver.c:75: if (orig != value) {
      00471F 90 05 BD         [24]  825 	mov	dptr,#_eeprom_update_word_PARM_2
      004722 E0               [24]  826 	movx	a,@dptr
      004723 FC               [12]  827 	mov	r4,a
      004724 A3               [24]  828 	inc	dptr
      004725 E0               [24]  829 	movx	a,@dptr
      004726 FD               [12]  830 	mov	r5,a
      004727 EE               [12]  831 	mov	a,r6
      004728 B5 04 05         [24]  832 	cjne	a,ar4,00112$
      00472B EF               [12]  833 	mov	a,r7
      00472C B5 05 01         [24]  834 	cjne	a,ar5,00112$
      00472F 22               [24]  835 	ret
      004730                        836 00112$:
                                    837 ;	drivers/eeprom/eeprom_driver.c:76: eeprom_write_word(addr, value);
      004730 90 05 BF         [24]  838 	mov	dptr,#_eeprom_update_word_addr_10000_99
      004733 E0               [24]  839 	movx	a,@dptr
      004734 FB               [12]  840 	mov	r3,a
      004735 A3               [24]  841 	inc	dptr
      004736 E0               [24]  842 	movx	a,@dptr
      004737 FE               [12]  843 	mov	r6,a
      004738 A3               [24]  844 	inc	dptr
      004739 E0               [24]  845 	movx	a,@dptr
      00473A FF               [12]  846 	mov	r7,a
      00473B 90 05 A5         [24]  847 	mov	dptr,#_eeprom_write_word_PARM_2
      00473E EC               [12]  848 	mov	a,r4
      00473F F0               [24]  849 	movx	@dptr,a
      004740 ED               [12]  850 	mov	a,r5
      004741 A3               [24]  851 	inc	dptr
      004742 F0               [24]  852 	movx	@dptr,a
      004743 8B 82            [24]  853 	mov	dpl, r3
      004745 8E 83            [24]  854 	mov	dph, r6
      004747 8F F0            [24]  855 	mov	b, r7
                                    856 ;	drivers/eeprom/eeprom_driver.c:78: }
      004749 02 45 61         [24]  857 	ljmp	_eeprom_write_word
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
      00474C                        869 _eeprom_update_dword:
      00474C AF F0            [24]  870 	mov	r7,b
      00474E AE 83            [24]  871 	mov	r6,dph
      004750 E5 82            [12]  872 	mov	a,dpl
      004752 90 05 C6         [24]  873 	mov	dptr,#_eeprom_update_dword_addr_10000_103
      004755 F0               [24]  874 	movx	@dptr,a
      004756 EE               [12]  875 	mov	a,r6
      004757 A3               [24]  876 	inc	dptr
      004758 F0               [24]  877 	movx	@dptr,a
      004759 EF               [12]  878 	mov	a,r7
      00475A A3               [24]  879 	inc	dptr
      00475B F0               [24]  880 	movx	@dptr,a
                                    881 ;	drivers/eeprom/eeprom_driver.c:81: uint32_t orig = eeprom_read_dword(addr);
      00475C 90 05 C6         [24]  882 	mov	dptr,#_eeprom_update_dword_addr_10000_103
      00475F E0               [24]  883 	movx	a,@dptr
      004760 FD               [12]  884 	mov	r5,a
      004761 A3               [24]  885 	inc	dptr
      004762 E0               [24]  886 	movx	a,@dptr
      004763 FE               [12]  887 	mov	r6,a
      004764 A3               [24]  888 	inc	dptr
      004765 E0               [24]  889 	movx	a,@dptr
      004766 FF               [12]  890 	mov	r7,a
      004767 8D 82            [24]  891 	mov	dpl, r5
      004769 8E 83            [24]  892 	mov	dph, r6
      00476B 8F F0            [24]  893 	mov	b, r7
      00476D 12 44 D4         [24]  894 	lcall	_eeprom_read_dword
      004770 AC 82            [24]  895 	mov	r4, dpl
      004772 AD 83            [24]  896 	mov	r5, dph
      004774 AE F0            [24]  897 	mov	r6, b
      004776 FF               [12]  898 	mov	r7, a
                                    899 ;	drivers/eeprom/eeprom_driver.c:82: if (orig != value) {
      004777 90 05 C2         [24]  900 	mov	dptr,#_eeprom_update_dword_PARM_2
      00477A E0               [24]  901 	movx	a,@dptr
      00477B F8               [12]  902 	mov	r0,a
      00477C A3               [24]  903 	inc	dptr
      00477D E0               [24]  904 	movx	a,@dptr
      00477E F9               [12]  905 	mov	r1,a
      00477F A3               [24]  906 	inc	dptr
      004780 E0               [24]  907 	movx	a,@dptr
      004781 FA               [12]  908 	mov	r2,a
      004782 A3               [24]  909 	inc	dptr
      004783 E0               [24]  910 	movx	a,@dptr
      004784 FB               [12]  911 	mov	r3,a
      004785 EC               [12]  912 	mov	a,r4
      004786 B5 00 0D         [24]  913 	cjne	a,ar0,00112$
      004789 ED               [12]  914 	mov	a,r5
      00478A B5 01 09         [24]  915 	cjne	a,ar1,00112$
      00478D EE               [12]  916 	mov	a,r6
      00478E B5 02 05         [24]  917 	cjne	a,ar2,00112$
      004791 EF               [12]  918 	mov	a,r7
      004792 B5 03 01         [24]  919 	cjne	a,ar3,00112$
      004795 22               [24]  920 	ret
      004796                        921 00112$:
                                    922 ;	drivers/eeprom/eeprom_driver.c:83: eeprom_write_dword(addr, value);
      004796 90 05 C6         [24]  923 	mov	dptr,#_eeprom_update_dword_addr_10000_103
      004799 E0               [24]  924 	movx	a,@dptr
      00479A FD               [12]  925 	mov	r5,a
      00479B A3               [24]  926 	inc	dptr
      00479C E0               [24]  927 	movx	a,@dptr
      00479D FE               [12]  928 	mov	r6,a
      00479E A3               [24]  929 	inc	dptr
      00479F E0               [24]  930 	movx	a,@dptr
      0047A0 FF               [12]  931 	mov	r7,a
      0047A1 90 05 AA         [24]  932 	mov	dptr,#_eeprom_write_dword_PARM_2
      0047A4 E8               [12]  933 	mov	a,r0
      0047A5 F0               [24]  934 	movx	@dptr,a
      0047A6 E9               [12]  935 	mov	a,r1
      0047A7 A3               [24]  936 	inc	dptr
      0047A8 F0               [24]  937 	movx	@dptr,a
      0047A9 EA               [12]  938 	mov	a,r2
      0047AA A3               [24]  939 	inc	dptr
      0047AB F0               [24]  940 	movx	@dptr,a
      0047AC EB               [12]  941 	mov	a,r3
      0047AD A3               [24]  942 	inc	dptr
      0047AE F0               [24]  943 	movx	@dptr,a
      0047AF 8D 82            [24]  944 	mov	dpl, r5
      0047B1 8E 83            [24]  945 	mov	dph, r6
      0047B3 8F F0            [24]  946 	mov	b, r7
                                    947 ;	drivers/eeprom/eeprom_driver.c:85: }
      0047B5 02 45 98         [24]  948 	ljmp	_eeprom_write_dword
                                    949 	.area CSEG    (CODE)
                                    950 	.area CONST   (CODE)
                                    951 	.area XINIT   (CODE)
                                    952 	.area CABS    (ABS,CODE)
