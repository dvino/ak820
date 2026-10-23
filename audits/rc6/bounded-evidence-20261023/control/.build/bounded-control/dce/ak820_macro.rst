                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module ak820_macro
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _eeprom_update_byte
                                     12 	.globl _eeprom_write_block
                                     13 	.globl _eeprom_read_byte
                                     14 	.globl _ak820_nvm_end
                                     15 	.globl _ak820_nvm_flush
                                     16 	.globl _ak820_nvm_begin
                                     17 	.globl _ak820_nvm_ok
                                     18 	.globl _ak820_macro_write_PARM_3
                                     19 	.globl _ak820_macro_write_PARM_2
                                     20 	.globl _ak820_macro_init
                                     21 	.globl _ak820_macro_ready
                                     22 	.globl _ak820_macro_length
                                     23 	.globl _ak820_macro_write
                                     24 	.globl _ak820_macro_reset
                                     25 ;--------------------------------------------------------
                                     26 ; special function registers
                                     27 ;--------------------------------------------------------
                                     28 	.area RSEG    (ABS,DATA)
      000000                         29 	.org 0x0000
                                     30 ;--------------------------------------------------------
                                     31 ; special function bits
                                     32 ;--------------------------------------------------------
                                     33 	.area RSEG    (ABS,DATA)
      000000                         34 	.org 0x0000
                                     35 ;--------------------------------------------------------
                                     36 ; overlayable register banks
                                     37 ;--------------------------------------------------------
                                     38 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                         39 	.ds 8
                                     40 ;--------------------------------------------------------
                                     41 ; internal ram data
                                     42 ;--------------------------------------------------------
                                     43 	.area DSEG    (DATA)
      00000A                         44 _ak820_macro_write_sloc0_1_0:
      00000A                         45 	.ds 2
                                     46 ;--------------------------------------------------------
                                     47 ; overlayable items in internal ram
                                     48 ;--------------------------------------------------------
                                     49 	.area	OSEG    (OVR,DATA)
      00005D                         50 _parse_byte_sloc1_1_0:
      00005D                         51 	.ds 2
                                     52 ;--------------------------------------------------------
                                     53 ; indirectly addressable internal ram data
                                     54 ;--------------------------------------------------------
                                     55 	.area ISEG    (DATA)
                                     56 ;--------------------------------------------------------
                                     57 ; absolute internal ram data
                                     58 ;--------------------------------------------------------
                                     59 	.area IABS    (ABS,DATA)
                                     60 	.area IABS    (ABS,DATA)
                                     61 ;--------------------------------------------------------
                                     62 ; bit data
                                     63 ;--------------------------------------------------------
                                     64 	.area BSEG    (BIT)
      000001                         65 _parse_byte_sloc0_1_0:
      000001                         66 	.ds 1
      000002                         67 _ak820_macro_ready_sloc0_1_0:
      000002                         68 	.ds 1
                                     69 ;--------------------------------------------------------
                                     70 ; paged external ram data
                                     71 ;--------------------------------------------------------
                                     72 	.area PSEG    (PAG,XDATA)
                                     73 ;--------------------------------------------------------
                                     74 ; uninitialized external ram data
                                     75 ;--------------------------------------------------------
                                     76 	.area XSEG    (XDATA)
      0004B4                         77 _parsed:
      0004B4                         78 	.ds 2
      0004B6                         79 _covered:
      0004B6                         80 	.ds 2
      0004B8                         81 _used_length:
      0004B8                         82 	.ds 2
      0004BA                         83 _uploading:
      0004BA                         84 	.ds 1
      0004BB                         85 _macro_byte_offset_10000_63:
      0004BB                         86 	.ds 2
      0004BD                         87 _busy_write_value_10000_65:
      0004BD                         88 	.ds 1
      0004BE                         89 _commit_length_length_10000_67:
      0004BE                         90 	.ds 2
      0004C0                         91 _commit_length_metadata_10000_68:
      0004C0                         92 	.ds 3
      0004C3                         93 _parse_byte_PARM_2:
      0004C3                         94 	.ds 1
      0004C4                         95 _parse_byte_state_10000_70:
      0004C4                         96 	.ds 2
      0004C6                         97 _matches_PARM_2:
      0004C6                         98 	.ds 2
      0004C8                         99 _matches_PARM_3:
      0004C8                        100 	.ds 2
      0004CA                        101 _matches_offset_10000_85:
      0004CA                        102 	.ds 2
      0004CC                        103 _ak820_macro_write_PARM_2:
      0004CC                        104 	.ds 2
      0004CE                        105 _ak820_macro_write_PARM_3:
      0004CE                        106 	.ds 3
      0004D1                        107 _ak820_macro_write_offset_10000_95:
      0004D1                        108 	.ds 2
      0004D3                        109 _ak820_macro_write_next_10000_96:
      0004D3                        110 	.ds 2
                                    111 ;--------------------------------------------------------
                                    112 ; absolute external ram data
                                    113 ;--------------------------------------------------------
                                    114 	.area XABS    (ABS,XDATA)
                                    115 ;--------------------------------------------------------
                                    116 ; initialized external ram data
                                    117 ;--------------------------------------------------------
                                    118 	.area XISEG   (XDATA)
                                    119 	.area HOME    (CODE)
                                    120 	.area GSINIT0 (CODE)
                                    121 	.area GSINIT1 (CODE)
                                    122 	.area GSINIT2 (CODE)
                                    123 	.area GSINIT3 (CODE)
                                    124 	.area GSINIT4 (CODE)
                                    125 	.area GSINIT5 (CODE)
                                    126 	.area GSINIT  (CODE)
                                    127 	.area GSFINAL (CODE)
                                    128 	.area CSEG    (CODE)
                                    129 ;--------------------------------------------------------
                                    130 ; global & static initialisations
                                    131 ;--------------------------------------------------------
                                    132 	.area HOME    (CODE)
                                    133 	.area GSINIT  (CODE)
                                    134 	.area GSFINAL (CODE)
                                    135 	.area GSINIT  (CODE)
                                    136 ;--------------------------------------------------------
                                    137 ; Home
                                    138 ;--------------------------------------------------------
                                    139 	.area HOME    (CODE)
                                    140 	.area HOME    (CODE)
                                    141 ;--------------------------------------------------------
                                    142 ; code
                                    143 ;--------------------------------------------------------
                                    144 	.area AK820LOW(CODE)
                                    145 ;------------------------------------------------------------
                                    146 ;Allocation info for local variables in function 'macro_byte'
                                    147 ;------------------------------------------------------------
                                    148 ;offset        Allocated with name '_macro_byte_offset_10000_63'
                                    149 ;------------------------------------------------------------
                                    150 ;	keyboards/ajazz/ak820/ak820_macro.c:34: static uint8_t macro_byte(uint16_t offset) {
                                    151 ;	-----------------------------------------
                                    152 ;	 function macro_byte
                                    153 ;	-----------------------------------------
      0028A0                        154 _macro_byte:
                           000007   155 	ar7 = 0x07
                           000006   156 	ar6 = 0x06
                           000005   157 	ar5 = 0x05
                           000004   158 	ar4 = 0x04
                           000003   159 	ar3 = 0x03
                           000002   160 	ar2 = 0x02
                           000001   161 	ar1 = 0x01
                           000000   162 	ar0 = 0x00
      0028A0 AF 83            [24]  163 	mov	r7,dph
      0028A2 E5 82            [12]  164 	mov	a,dpl
      0028A4 90 04 BB         [24]  165 	mov	dptr,#_macro_byte_offset_10000_63
      0028A7 F0               [24]  166 	movx	@dptr,a
      0028A8 EF               [12]  167 	mov	a,r7
      0028A9 A3               [24]  168 	inc	dptr
      0028AA F0               [24]  169 	movx	@dptr,a
                                    170 ;	keyboards/ajazz/ak820/ak820_macro.c:35: return eeprom_read_byte((const uint8_t *)(uintptr_t)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + offset));
      0028AB 90 04 BB         [24]  171 	mov	dptr,#_macro_byte_offset_10000_63
      0028AE E0               [24]  172 	movx	a,@dptr
      0028AF FE               [12]  173 	mov	r6,a
      0028B0 A3               [24]  174 	inc	dptr
      0028B1 E0               [24]  175 	movx	a,@dptr
      0028B2 24 08            [12]  176 	add	a,#0x08
      0028B4 FF               [12]  177 	mov	r7,a
      0028B5 7D 00            [12]  178 	mov	r5,#0x00
      0028B7 8E 82            [24]  179 	mov	dpl, r6
      0028B9 8F 83            [24]  180 	mov	dph, r7
      0028BB 8D F0            [24]  181 	mov	b, r5
                                    182 ;	keyboards/ajazz/ak820/ak820_macro.c:36: }
      0028BD 02 44 1B         [24]  183 	ljmp	_eeprom_read_byte
                                    184 ;------------------------------------------------------------
                                    185 ;Allocation info for local variables in function 'busy_write'
                                    186 ;------------------------------------------------------------
                                    187 ;value         Allocated with name '_busy_write_value_10000_65'
                                    188 ;------------------------------------------------------------
                                    189 ;	keyboards/ajazz/ak820/ak820_macro.c:38: static void busy_write(uint8_t value) {
                                    190 ;	-----------------------------------------
                                    191 ;	 function busy_write
                                    192 ;	-----------------------------------------
      0028C0                        193 _busy_write:
      0028C0 E5 82            [12]  194 	mov	a,dpl
      0028C2 90 04 BD         [24]  195 	mov	dptr,#_busy_write_value_10000_65
      0028C5 F0               [24]  196 	movx	@dptr,a
                                    197 ;	keyboards/ajazz/ak820/ak820_macro.c:39: eeprom_update_byte((uint8_t *)(uintptr_t)AK820_MACRO_BUSY_ADDR, value);
      0028C6 E0               [24]  198 	movx	a,@dptr
      0028C7 90 05 B9         [24]  199 	mov	dptr,#_eeprom_update_byte_PARM_2
      0028CA F0               [24]  200 	movx	@dptr,a
      0028CB 90 07 F0         [24]  201 	mov	dptr,#0x07f0
      0028CE 75 F0 00         [24]  202 	mov	b, #0x00
      0028D1 12 46 7C         [24]  203 	lcall	_eeprom_update_byte
                                    204 ;	keyboards/ajazz/ak820/ak820_macro.c:40: ak820_nvm_flush();
                                    205 ;	keyboards/ajazz/ak820/ak820_macro.c:41: }
      0028D4 02 3A EA         [24]  206 	ljmp	_ak820_nvm_flush
                                    207 ;------------------------------------------------------------
                                    208 ;Allocation info for local variables in function 'commit_length'
                                    209 ;------------------------------------------------------------
                                    210 ;length        Allocated with name '_commit_length_length_10000_67'
                                    211 ;metadata      Allocated with name '_commit_length_metadata_10000_68'
                                    212 ;------------------------------------------------------------
                                    213 ;	keyboards/ajazz/ak820/ak820_macro.c:43: static void commit_length(uint16_t length) {
                                    214 ;	-----------------------------------------
                                    215 ;	 function commit_length
                                    216 ;	-----------------------------------------
      0028D7                        217 _commit_length:
      0028D7 AF 83            [24]  218 	mov	r7,dph
      0028D9 E5 82            [12]  219 	mov	a,dpl
      0028DB 90 04 BE         [24]  220 	mov	dptr,#_commit_length_length_10000_67
      0028DE F0               [24]  221 	movx	@dptr,a
      0028DF EF               [12]  222 	mov	a,r7
      0028E0 A3               [24]  223 	inc	dptr
      0028E1 F0               [24]  224 	movx	@dptr,a
                                    225 ;	keyboards/ajazz/ak820/ak820_macro.c:45: metadata[0] = 0;
      0028E2 90 04 C0         [24]  226 	mov	dptr,#_commit_length_metadata_10000_68
      0028E5 E4               [12]  227 	clr	a
      0028E6 F0               [24]  228 	movx	@dptr,a
                                    229 ;	keyboards/ajazz/ak820/ak820_macro.c:46: metadata[1] = (uint8_t)length;
      0028E7 90 04 BE         [24]  230 	mov	dptr,#_commit_length_length_10000_67
      0028EA E0               [24]  231 	movx	a,@dptr
      0028EB FE               [12]  232 	mov	r6,a
      0028EC A3               [24]  233 	inc	dptr
      0028ED E0               [24]  234 	movx	a,@dptr
      0028EE FF               [12]  235 	mov	r7,a
      0028EF 8E 05            [24]  236 	mov	ar5,r6
      0028F1 90 04 C1         [24]  237 	mov	dptr,#(_commit_length_metadata_10000_68 + 0x0001)
      0028F4 ED               [12]  238 	mov	a,r5
      0028F5 F0               [24]  239 	movx	@dptr,a
                                    240 ;	keyboards/ajazz/ak820/ak820_macro.c:47: metadata[2] = (uint8_t)(length >> 8);
      0028F6 8F 05            [24]  241 	mov	ar5,r7
      0028F8 90 04 C2         [24]  242 	mov	dptr,#(_commit_length_metadata_10000_68 + 0x0002)
      0028FB ED               [12]  243 	mov	a,r5
      0028FC F0               [24]  244 	movx	@dptr,a
                                    245 ;	keyboards/ajazz/ak820/ak820_macro.c:48: eeprom_write_block(metadata, (void *)(uintptr_t)AK820_MACRO_BUSY_ADDR, sizeof(metadata));
      0028FD 90 05 49         [24]  246 	mov	dptr,#_eeprom_write_block_PARM_2
      002900 74 F0            [12]  247 	mov	a,#0xf0
      002902 F0               [24]  248 	movx	@dptr,a
      002903 74 07            [12]  249 	mov	a,#0x07
      002905 A3               [24]  250 	inc	dptr
      002906 F0               [24]  251 	movx	@dptr,a
      002907 E4               [12]  252 	clr	a
      002908 A3               [24]  253 	inc	dptr
      002909 F0               [24]  254 	movx	@dptr,a
      00290A 90 05 4C         [24]  255 	mov	dptr,#_eeprom_write_block_PARM_3
      00290D 74 03            [12]  256 	mov	a,#0x03
      00290F F0               [24]  257 	movx	@dptr,a
      002910 E4               [12]  258 	clr	a
      002911 A3               [24]  259 	inc	dptr
      002912 F0               [24]  260 	movx	@dptr,a
      002913 90 04 C0         [24]  261 	mov	dptr,#_commit_length_metadata_10000_68
      002916 F5 F0            [12]  262 	mov	b,a
      002918 C0 07            [24]  263 	push	ar7
      00291A C0 06            [24]  264 	push	ar6
      00291C 12 3E 86         [24]  265 	lcall	_eeprom_write_block
                                    266 ;	keyboards/ajazz/ak820/ak820_macro.c:49: ak820_nvm_flush();
      00291F 12 3A EA         [24]  267 	lcall	_ak820_nvm_flush
      002922 D0 06            [24]  268 	pop	ar6
      002924 D0 07            [24]  269 	pop	ar7
                                    270 ;	keyboards/ajazz/ak820/ak820_macro.c:50: if (ak820_nvm_ok()) used_length = length;
      002926 12 3A D2         [24]  271 	lcall	_ak820_nvm_ok
      002929 E5 82            [12]  272 	mov	a, dpl
      00292B 60 08            [24]  273 	jz	00103$
      00292D 90 04 B8         [24]  274 	mov	dptr,#_used_length
      002930 EE               [12]  275 	mov	a,r6
      002931 F0               [24]  276 	movx	@dptr,a
      002932 EF               [12]  277 	mov	a,r7
      002933 A3               [24]  278 	inc	dptr
      002934 F0               [24]  279 	movx	@dptr,a
      002935                        280 00103$:
                                    281 ;	keyboards/ajazz/ak820/ak820_macro.c:51: }
      002935 22               [24]  282 	ret
                                    283 ;------------------------------------------------------------
                                    284 ;Allocation info for local variables in function 'parse_byte'
                                    285 ;------------------------------------------------------------
                                    286 ;value         Allocated with name '_parse_byte_PARM_2'
                                    287 ;state         Allocated with name '_parse_byte_state_10000_70'
                                    288 ;sloc1         Allocated with name '_parse_byte_sloc1_1_0'
                                    289 ;------------------------------------------------------------
                                    290 ;	keyboards/ajazz/ak820/ak820_macro.c:55: static bool parse_byte(macro_parse_t AK820_XDATA *state, uint8_t value) {
                                    291 ;	-----------------------------------------
                                    292 ;	 function parse_byte
                                    293 ;	-----------------------------------------
      002936                        294 _parse_byte:
      002936 AF 83            [24]  295 	mov	r7,dph
      002938 E5 82            [12]  296 	mov	a,dpl
      00293A 90 04 C4         [24]  297 	mov	dptr,#_parse_byte_state_10000_70
      00293D F0               [24]  298 	movx	@dptr,a
      00293E EF               [12]  299 	mov	a,r7
      00293F A3               [24]  300 	inc	dptr
      002940 F0               [24]  301 	movx	@dptr,a
                                    302 ;	keyboards/ajazz/ak820/ak820_macro.c:56: if (state->terminated == DYNAMIC_KEYMAP_MACRO_COUNT) return value == 0;
      002941 90 04 C4         [24]  303 	mov	dptr,#_parse_byte_state_10000_70
      002944 E0               [24]  304 	movx	a,@dptr
      002945 FE               [12]  305 	mov	r6,a
      002946 A3               [24]  306 	inc	dptr
      002947 E0               [24]  307 	movx	a,@dptr
      002948 FF               [12]  308 	mov	r7,a
      002949 8E 04            [24]  309 	mov	ar4,r6
      00294B 8F 05            [24]  310 	mov	ar5,r7
      00294D 8C 82            [24]  311 	mov	dpl,r4
      00294F 8D 83            [24]  312 	mov	dph,r5
      002951 E0               [24]  313 	movx	a,@dptr
      002952 FB               [12]  314 	mov	r3,a
      002953 BB 10 0E         [24]  315 	cjne	r3,#0x10,00102$
      002956 90 04 C3         [24]  316 	mov	dptr,#_parse_byte_PARM_2
      002959 E0               [24]  317 	movx	a,@dptr
      00295A B4 01 00         [24]  318 	cjne	a,#0x01,00191$
      00295D                        319 00191$:
      00295D 92 01            [24]  320 	mov  _parse_byte_sloc0_1_0,c
      00295F E4               [12]  321 	clr	a
      002960 33               [12]  322 	rlc	a
      002961 F5 82            [12]  323 	mov	dpl, a
      002963 22               [24]  324 	ret
      002964                        325 00102$:
                                    326 ;	keyboards/ajazz/ak820/ak820_macro.c:57: if (state->arguments == 3) {
      002964 0E               [12]  327 	inc	r6
      002965 BE 00 01         [24]  328 	cjne	r6,#0x00,00192$
      002968 0F               [12]  329 	inc	r7
      002969                        330 00192$:
      002969 8E 82            [24]  331 	mov	dpl,r6
      00296B 8F 83            [24]  332 	mov	dph,r7
      00296D E0               [24]  333 	movx	a,@dptr
      00296E FA               [12]  334 	mov	r2,a
      00296F BA 03 2C         [24]  335 	cjne	r2,#0x03,00120$
                                    336 ;	keyboards/ajazz/ak820/ak820_macro.c:58: if (value < 1 || value > 7) return false;
      002972 90 04 C3         [24]  337 	mov	dptr,#_parse_byte_PARM_2
      002975 E0               [24]  338 	movx	a,@dptr
      002976 F9               [12]  339 	mov	r1,a
      002977 B9 01 00         [24]  340 	cjne	r1,#0x01,00195$
      00297A                        341 00195$:
      00297A 40 05            [24]  342 	jc	00103$
      00297C E9               [12]  343 	mov	a,r1
      00297D 24 F8            [12]  344 	add	a,#0xff - 0x07
      00297F 50 04            [24]  345 	jnc	00104$
                                    346 ;	free result
      002981                        347 00103$:
      002981 75 82 00         [24]  348 	mov	dpl, #0x00
      002984 22               [24]  349 	ret
      002985                        350 00104$:
                                    351 ;	keyboards/ajazz/ak820/ak820_macro.c:59: state->arguments = value <= 3 ? 1 : 2;
      002985 8E 5D            [24]  352 	mov	_parse_byte_sloc1_1_0,r6
      002987 8F 5E            [24]  353 	mov	(_parse_byte_sloc1_1_0 + 1),r7
      002989 E9               [12]  354 	mov	a,r1
      00298A 24 FC            [12]  355 	add	a,#0xff - 0x03
      00298C 40 04            [24]  356 	jc	00124$
                                    357 ;	free result
      00298E 79 01            [12]  358 	mov	r1,#0x01
      002990 80 02            [24]  359 	sjmp	00125$
      002992                        360 00124$:
      002992 79 02            [12]  361 	mov	r1,#0x02
      002994                        362 00125$:
      002994 85 5D 82         [24]  363 	mov	dpl,_parse_byte_sloc1_1_0
      002997 85 5E 83         [24]  364 	mov	dph,(_parse_byte_sloc1_1_0 + 1)
      00299A E9               [12]  365 	mov	a,r1
      00299B F0               [24]  366 	movx	@dptr,a
      00299C 80 3A            [24]  367 	sjmp	00121$
      00299E                        368 00120$:
                                    369 ;	keyboards/ajazz/ak820/ak820_macro.c:60: } else if (state->arguments) {
      00299E EA               [12]  370 	mov	a,r2
      00299F 60 12            [24]  371 	jz	00117$
                                    372 ;	keyboards/ajazz/ak820/ak820_macro.c:61: if (!value) return false;
      0029A1 90 04 C3         [24]  373 	mov	dptr,#_parse_byte_PARM_2
      0029A4 E0               [24]  374 	movx	a,@dptr
      0029A5 70 03            [24]  375 	jnz	00107$
      0029A7 F5 82            [12]  376 	mov	dpl,a
      0029A9 22               [24]  377 	ret
      0029AA                        378 00107$:
                                    379 ;	keyboards/ajazz/ak820/ak820_macro.c:62: --state->arguments;
      0029AA 1A               [12]  380 	dec	r2
      0029AB 8E 82            [24]  381 	mov	dpl,r6
      0029AD 8F 83            [24]  382 	mov	dph,r7
      0029AF EA               [12]  383 	mov	a,r2
      0029B0 F0               [24]  384 	movx	@dptr,a
      0029B1 80 25            [24]  385 	sjmp	00121$
      0029B3                        386 00117$:
                                    387 ;	keyboards/ajazz/ak820/ak820_macro.c:63: } else if (!value) {
      0029B3 90 04 C3         [24]  388 	mov	dptr,#_parse_byte_PARM_2
      0029B6 E0               [24]  389 	movx	a,@dptr
      0029B7 FA               [12]  390 	mov	r2,a
      0029B8 70 09            [24]  391 	jnz	00114$
                                    392 ;	keyboards/ajazz/ak820/ak820_macro.c:64: ++state->terminated;
      0029BA 0B               [12]  393 	inc	r3
      0029BB 8C 82            [24]  394 	mov	dpl,r4
      0029BD 8D 83            [24]  395 	mov	dph,r5
      0029BF EB               [12]  396 	mov	a,r3
      0029C0 F0               [24]  397 	movx	@dptr,a
      0029C1 80 15            [24]  398 	sjmp	00121$
      0029C3                        399 00114$:
                                    400 ;	keyboards/ajazz/ak820/ak820_macro.c:65: } else if (value == 1) {
      0029C3 BA 01 09         [24]  401 	cjne	r2,#0x01,00111$
                                    402 ;	keyboards/ajazz/ak820/ak820_macro.c:66: state->arguments = 3;
      0029C6 8E 82            [24]  403 	mov	dpl,r6
      0029C8 8F 83            [24]  404 	mov	dph,r7
      0029CA 74 03            [12]  405 	mov	a,#0x03
      0029CC F0               [24]  406 	movx	@dptr,a
      0029CD 80 09            [24]  407 	sjmp	00121$
      0029CF                        408 00111$:
                                    409 ;	keyboards/ajazz/ak820/ak820_macro.c:67: } else if (value >= 128) {
      0029CF BA 80 00         [24]  410 	cjne	r2,#0x80,00204$
      0029D2                        411 00204$:
      0029D2 40 04            [24]  412 	jc	00121$
                                    413 ;	keyboards/ajazz/ak820/ak820_macro.c:70: return false;
      0029D4 75 82 00         [24]  414 	mov	dpl, #0x00
      0029D7 22               [24]  415 	ret
      0029D8                        416 00121$:
                                    417 ;	keyboards/ajazz/ak820/ak820_macro.c:72: return true;
      0029D8 75 82 01         [24]  418 	mov	dpl, #0x01
                                    419 ;	keyboards/ajazz/ak820/ak820_macro.c:73: }
      0029DB 22               [24]  420 	ret
                                    421 ;------------------------------------------------------------
                                    422 ;Allocation info for local variables in function 'matches'
                                    423 ;------------------------------------------------------------
                                    424 ;size          Allocated with name '_matches_PARM_2'
                                    425 ;data          Allocated with name '_matches_PARM_3'
                                    426 ;offset        Allocated with name '_matches_offset_10000_85'
                                    427 ;value         Allocated with name '_matches_value_20000_87'
                                    428 ;------------------------------------------------------------
                                    429 ;	keyboards/ajazz/ak820/ak820_macro.c:75: static bool matches(uint16_t offset, uint16_t size, const uint8_t AK820_XDATA *data) {
                                    430 ;	-----------------------------------------
                                    431 ;	 function matches
                                    432 ;	-----------------------------------------
      0029DC                        433 _matches:
      0029DC AF 83            [24]  434 	mov	r7,dph
      0029DE E5 82            [12]  435 	mov	a,dpl
      0029E0 90 04 CA         [24]  436 	mov	dptr,#_matches_offset_10000_85
      0029E3 F0               [24]  437 	movx	@dptr,a
      0029E4 EF               [12]  438 	mov	a,r7
      0029E5 A3               [24]  439 	inc	dptr
      0029E6 F0               [24]  440 	movx	@dptr,a
                                    441 ;	keyboards/ajazz/ak820/ak820_macro.c:76: while (size--) {
      0029E7 90 04 C8         [24]  442 	mov	dptr,#_matches_PARM_3
      0029EA E0               [24]  443 	movx	a,@dptr
      0029EB FE               [12]  444 	mov	r6,a
      0029EC A3               [24]  445 	inc	dptr
      0029ED E0               [24]  446 	movx	a,@dptr
      0029EE FF               [12]  447 	mov	r7,a
      0029EF 90 04 CA         [24]  448 	mov	dptr,#_matches_offset_10000_85
      0029F2 E0               [24]  449 	movx	a,@dptr
      0029F3 FC               [12]  450 	mov	r4,a
      0029F4 A3               [24]  451 	inc	dptr
      0029F5 E0               [24]  452 	movx	a,@dptr
      0029F6 FD               [12]  453 	mov	r5,a
      0029F7 90 04 C6         [24]  454 	mov	dptr,#_matches_PARM_2
      0029FA E0               [24]  455 	movx	a,@dptr
      0029FB FA               [12]  456 	mov	r2,a
      0029FC A3               [24]  457 	inc	dptr
      0029FD E0               [24]  458 	movx	a,@dptr
      0029FE FB               [12]  459 	mov	r3,a
      0029FF                        460 00103$:
      0029FF 8A 00            [24]  461 	mov	ar0,r2
      002A01 8B 01            [24]  462 	mov	ar1,r3
      002A03 1A               [12]  463 	dec	r2
      002A04 BA FF 01         [24]  464 	cjne	r2,#0xff,00147$
      002A07 1B               [12]  465 	dec	r3
      002A08                        466 00147$:
      002A08 E8               [12]  467 	mov	a,r0
      002A09 49               [12]  468 	orl	a,r1
      002A0A 60 60            [24]  469 	jz	00105$
                                    470 ;	keyboards/ajazz/ak820/ak820_macro.c:77: uint8_t value = !uploading && offset >= used_length ? 0 : macro_byte(offset);
      002A0C 90 04 BA         [24]  471 	mov	dptr,#_uploading
      002A0F E0               [24]  472 	movx	a,@dptr
      002A10 70 13            [24]  473 	jnz	00108$
      002A12 90 04 B8         [24]  474 	mov	dptr,#_used_length
      002A15 E0               [24]  475 	movx	a,@dptr
      002A16 F8               [12]  476 	mov	r0,a
      002A17 A3               [24]  477 	inc	dptr
      002A18 E0               [24]  478 	movx	a,@dptr
      002A19 F9               [12]  479 	mov	r1,a
      002A1A C3               [12]  480 	clr	c
      002A1B EC               [12]  481 	mov	a,r4
      002A1C 98               [12]  482 	subb	a,r0
      002A1D ED               [12]  483 	mov	a,r5
      002A1E 99               [12]  484 	subb	a,r1
      002A1F 40 04            [24]  485 	jc	00108$
      002A21 79 00            [12]  486 	mov	r1,#0x00
      002A23 80 23            [24]  487 	sjmp	00109$
      002A25                        488 00108$:
      002A25 8C 82            [24]  489 	mov	dpl, r4
      002A27 8D 83            [24]  490 	mov	dph, r5
      002A29 C0 07            [24]  491 	push	ar7
      002A2B C0 06            [24]  492 	push	ar6
      002A2D C0 05            [24]  493 	push	ar5
      002A2F C0 04            [24]  494 	push	ar4
      002A31 C0 03            [24]  495 	push	ar3
      002A33 C0 02            [24]  496 	push	ar2
      002A35 12 28 A0         [24]  497 	lcall	_macro_byte
      002A38 A8 82            [24]  498 	mov	r0, dpl
      002A3A D0 02            [24]  499 	pop	ar2
      002A3C D0 03            [24]  500 	pop	ar3
      002A3E D0 04            [24]  501 	pop	ar4
      002A40 D0 05            [24]  502 	pop	ar5
      002A42 D0 06            [24]  503 	pop	ar6
      002A44 D0 07            [24]  504 	pop	ar7
      002A46 88 01            [24]  505 	mov	ar1,r0
      002A48                        506 00109$:
                                    507 ;	keyboards/ajazz/ak820/ak820_macro.c:78: if (value != *data++) return false;
      002A48 8E 82            [24]  508 	mov	dpl,r6
      002A4A 8F 83            [24]  509 	mov	dph,r7
      002A4C E0               [24]  510 	movx	a,@dptr
      002A4D F8               [12]  511 	mov	r0,a
      002A4E A3               [24]  512 	inc	dptr
      002A4F AE 82            [24]  513 	mov	r6,dpl
      002A51 AF 83            [24]  514 	mov	r7,dph
      002A53 E9               [12]  515 	mov	a,r1
      002A54 B5 00 02         [24]  516 	cjne	a,ar0,00151$
      002A57 80 04            [24]  517 	sjmp	00102$
      002A59                        518 00151$:
      002A59 75 82 00         [24]  519 	mov	dpl, #0x00
      002A5C 22               [24]  520 	ret
      002A5D                        521 00102$:
                                    522 ;	keyboards/ajazz/ak820/ak820_macro.c:79: ++offset;
      002A5D 0C               [12]  523 	inc	r4
      002A5E BC 00 01         [24]  524 	cjne	r4,#0x00,00152$
      002A61 0D               [12]  525 	inc	r5
      002A62                        526 00152$:
      002A62 90 04 CA         [24]  527 	mov	dptr,#_matches_offset_10000_85
      002A65 EC               [12]  528 	mov	a,r4
      002A66 F0               [24]  529 	movx	@dptr,a
      002A67 ED               [12]  530 	mov	a,r5
      002A68 A3               [24]  531 	inc	dptr
      002A69 F0               [24]  532 	movx	@dptr,a
      002A6A 80 93            [24]  533 	sjmp	00103$
      002A6C                        534 00105$:
                                    535 ;	keyboards/ajazz/ak820/ak820_macro.c:81: return true;
      002A6C 75 82 01         [24]  536 	mov	dpl, #0x01
                                    537 ;	keyboards/ajazz/ak820/ak820_macro.c:82: }
      002A6F 22               [24]  538 	ret
                                    539 ;------------------------------------------------------------
                                    540 ;Allocation info for local variables in function 'ak820_macro_init'
                                    541 ;------------------------------------------------------------
                                    542 ;	keyboards/ajazz/ak820/ak820_macro.c:84: void ak820_macro_init(void) {
                                    543 ;	-----------------------------------------
                                    544 ;	 function ak820_macro_init
                                    545 ;	-----------------------------------------
      002A70                        546 _ak820_macro_init:
                                    547 ;	keyboards/ajazz/ak820/ak820_macro.c:85: covered = 0;
      002A70 90 04 B6         [24]  548 	mov	dptr,#_covered
      002A73 E4               [12]  549 	clr	a
      002A74 F0               [24]  550 	movx	@dptr,a
      002A75 A3               [24]  551 	inc	dptr
      002A76 F0               [24]  552 	movx	@dptr,a
                                    553 ;	keyboards/ajazz/ak820/ak820_macro.c:86: uploading = false;
      002A77 90 04 BA         [24]  554 	mov	dptr,#_uploading
      002A7A F0               [24]  555 	movx	@dptr,a
                                    556 ;	keyboards/ajazz/ak820/ak820_macro.c:87: parsed.terminated = parsed.arguments = 0;
      002A7B 90 04 B5         [24]  557 	mov	dptr,#(_parsed + 0x0001)
      002A7E F0               [24]  558 	movx	@dptr,a
      002A7F 90 04 B4         [24]  559 	mov	dptr,#_parsed
      002A82 F0               [24]  560 	movx	@dptr,a
                                    561 ;	keyboards/ajazz/ak820/ak820_macro.c:88: used_length = eeprom_read_byte((const uint8_t *)(uintptr_t)AK820_MACRO_LENGTH_ADDR);
      002A83 90 07 F1         [24]  562 	mov	dptr,#0x07f1
      002A86 F5 F0            [12]  563 	mov	b,a
      002A88 12 44 1B         [24]  564 	lcall	_eeprom_read_byte
      002A8B AF 82            [24]  565 	mov	r7, dpl
      002A8D 90 04 B8         [24]  566 	mov	dptr,#_used_length
      002A90 EF               [12]  567 	mov	a,r7
      002A91 F0               [24]  568 	movx	@dptr,a
      002A92 E4               [12]  569 	clr	a
      002A93 A3               [24]  570 	inc	dptr
      002A94 F0               [24]  571 	movx	@dptr,a
                                    572 ;	keyboards/ajazz/ak820/ak820_macro.c:89: used_length |= (uint16_t)eeprom_read_byte((const uint8_t *)(uintptr_t)(AK820_MACRO_LENGTH_ADDR + 1)) << 8;
      002A95 90 07 F2         [24]  573 	mov	dptr,#0x07f2
      002A98 F5 F0            [12]  574 	mov	b,a
      002A9A 12 44 1B         [24]  575 	lcall	_eeprom_read_byte
      002A9D AE 82            [24]  576 	mov	r6,dpl
      002A9F 7F 00            [12]  577 	mov	r7,#0x00
      002AA1 90 04 B8         [24]  578 	mov	dptr,#_used_length
      002AA4 E0               [24]  579 	movx	a,@dptr
      002AA5 4F               [12]  580 	orl	a,r7
      002AA6 F0               [24]  581 	movx	@dptr,a
      002AA7 A3               [24]  582 	inc	dptr
      002AA8 E0               [24]  583 	movx	a,@dptr
      002AA9 4E               [12]  584 	orl	a,r6
      002AAA F0               [24]  585 	movx	@dptr,a
                                    586 ;	keyboards/ajazz/ak820/ak820_macro.c:90: }
      002AAB 22               [24]  587 	ret
                                    588 ;------------------------------------------------------------
                                    589 ;Allocation info for local variables in function 'ak820_macro_ready'
                                    590 ;------------------------------------------------------------
                                    591 ;	keyboards/ajazz/ak820/ak820_macro.c:92: bool ak820_macro_ready(void) {
                                    592 ;	-----------------------------------------
                                    593 ;	 function ak820_macro_ready
                                    594 ;	-----------------------------------------
      002AAC                        595 _ak820_macro_ready:
                                    596 ;	keyboards/ajazz/ak820/ak820_macro.c:93: return ak820_nvm_ok() && used_length >= DYNAMIC_KEYMAP_MACRO_COUNT &&
      002AAC 12 3A D2         [24]  597 	lcall	_ak820_nvm_ok
      002AAF E5 82            [12]  598 	mov	a, dpl
      002AB1 60 25            [24]  599 	jz	00103$
      002AB3 90 04 B8         [24]  600 	mov	dptr,#_used_length
      002AB6 E0               [24]  601 	movx	a,@dptr
      002AB7 FE               [12]  602 	mov	r6,a
      002AB8 A3               [24]  603 	inc	dptr
      002AB9 E0               [24]  604 	movx	a,@dptr
      002ABA FF               [12]  605 	mov	r7,a
      002ABB C3               [12]  606 	clr	c
      002ABC EE               [12]  607 	mov	a,r6
      002ABD 94 10            [12]  608 	subb	a,#0x10
      002ABF EF               [12]  609 	mov	a,r7
      002AC0 94 00            [12]  610 	subb	a,#0x00
                                    611 ;	keyboards/ajazz/ak820/ak820_macro.c:94: used_length <= DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE &&
      002AC2 40 14            [24]  612 	jc	00103$
      002AC4 E4               [12]  613 	clr	a
      002AC5 9E               [12]  614 	subb	a,r6
      002AC6 74 20            [12]  615 	mov	a,#0x20
      002AC8 9F               [12]  616 	subb	a,r7
      002AC9 40 0D            [24]  617 	jc	00103$
                                    618 ;	free result
                                    619 ;	keyboards/ajazz/ak820/ak820_macro.c:95: eeprom_read_byte((const uint8_t *)(uintptr_t)AK820_MACRO_BUSY_ADDR) == 0;
      002ACB 90 07 F0         [24]  620 	mov	dptr,#0x07f0
      002ACE 75 F0 00         [24]  621 	mov	b, #0x00
      002AD1 12 44 1B         [24]  622 	lcall	_eeprom_read_byte
      002AD4 E5 82            [12]  623 	mov	a, dpl
      002AD6 60 04            [24]  624 	jz	00104$
      002AD8                        625 00103$:
                                    626 ;	assignBit
      002AD8 C2 02            [12]  627 	clr	_ak820_macro_ready_sloc0_1_0
      002ADA 80 02            [24]  628 	sjmp	00105$
      002ADC                        629 00104$:
                                    630 ;	assignBit
      002ADC D2 02            [12]  631 	setb	_ak820_macro_ready_sloc0_1_0
      002ADE                        632 00105$:
      002ADE A2 02            [12]  633 	mov	c,_ak820_macro_ready_sloc0_1_0
      002AE0 E4               [12]  634 	clr	a
      002AE1 33               [12]  635 	rlc	a
      002AE2 F5 82            [12]  636 	mov	dpl, a
                                    637 ;	keyboards/ajazz/ak820/ak820_macro.c:96: }
      002AE4 22               [24]  638 	ret
                                    639 ;------------------------------------------------------------
                                    640 ;Allocation info for local variables in function 'ak820_macro_length'
                                    641 ;------------------------------------------------------------
                                    642 ;	keyboards/ajazz/ak820/ak820_macro.c:98: uint16_t ak820_macro_length(void) { return ak820_macro_ready() ? used_length : 0; }
                                    643 ;	-----------------------------------------
                                    644 ;	 function ak820_macro_length
                                    645 ;	-----------------------------------------
      002AE5                        646 _ak820_macro_length:
      002AE5 12 2A AC         [24]  647 	lcall	_ak820_macro_ready
      002AE8 E5 82            [12]  648 	mov	a, dpl
      002AEA 60 0A            [24]  649 	jz	00103$
      002AEC 90 04 B8         [24]  650 	mov	dptr,#_used_length
      002AEF E0               [24]  651 	movx	a,@dptr
      002AF0 FE               [12]  652 	mov	r6,a
      002AF1 A3               [24]  653 	inc	dptr
      002AF2 E0               [24]  654 	movx	a,@dptr
      002AF3 FF               [12]  655 	mov	r7,a
      002AF4 80 04            [24]  656 	sjmp	00104$
      002AF6                        657 00103$:
      002AF6 7E 00            [12]  658 	mov	r6,#0x00
      002AF8 7F 00            [12]  659 	mov	r7,#0x00
      002AFA                        660 00104$:
      002AFA 8E 82            [24]  661 	mov	dpl, r6
      002AFC 8F 83            [24]  662 	mov	dph, r7
      002AFE 22               [24]  663 	ret
                                    664 ;------------------------------------------------------------
                                    665 ;Allocation info for local variables in function 'ak820_macro_write'
                                    666 ;------------------------------------------------------------
                                    667 ;sloc0         Allocated with name '_ak820_macro_write_sloc0_1_0'
                                    668 ;size          Allocated with name '_ak820_macro_write_PARM_2'
                                    669 ;packet        Allocated with name '_ak820_macro_write_PARM_3'
                                    670 ;offset        Allocated with name '_ak820_macro_write_offset_10000_95'
                                    671 ;data          Allocated with name '_ak820_macro_write_data_10000_96'
                                    672 ;next          Allocated with name '_ak820_macro_write_next_10000_96'
                                    673 ;i             Allocated with name '_ak820_macro_write_i_10000_96'
                                    674 ;end           Allocated with name '_ak820_macro_write_end_10000_96'
                                    675 ;complete      Allocated with name '_ak820_macro_write_complete_10000_96'
                                    676 ;------------------------------------------------------------
                                    677 ;	keyboards/ajazz/ak820/ak820_macro.c:100: bool ak820_macro_write(uint16_t offset, uint16_t size, const uint8_t *packet) {
                                    678 ;	-----------------------------------------
                                    679 ;	 function ak820_macro_write
                                    680 ;	-----------------------------------------
      002AFF                        681 _ak820_macro_write:
      002AFF AF 83            [24]  682 	mov	r7,dph
      002B01 E5 82            [12]  683 	mov	a,dpl
      002B03 90 04 D1         [24]  684 	mov	dptr,#_ak820_macro_write_offset_10000_95
      002B06 F0               [24]  685 	movx	@dptr,a
      002B07 EF               [12]  686 	mov	a,r7
      002B08 A3               [24]  687 	inc	dptr
      002B09 F0               [24]  688 	movx	@dptr,a
                                    689 ;	keyboards/ajazz/ak820/ak820_macro.c:103: const uint8_t AK820_XDATA *data = (const uint8_t AK820_XDATA *)packet;
      002B0A 90 04 CE         [24]  690 	mov	dptr,#_ak820_macro_write_PARM_3
      002B0D E0               [24]  691 	movx	a,@dptr
      002B0E FE               [12]  692 	mov	r6,a
      002B0F A3               [24]  693 	inc	dptr
      002B10 E0               [24]  694 	movx	a,@dptr
      002B11 FF               [12]  695 	mov	r7,a
                                    696 ;	keyboards/ajazz/ak820/ak820_macro.c:109: if (!ak820_nvm_ok() || !size || offset >= DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE ||
      002B12 12 3A D2         [24]  697 	lcall	_ak820_nvm_ok
      002B15 E5 82            [12]  698 	mov	a, dpl
      002B17 60 2B            [24]  699 	jz	00101$
      002B19 90 04 CC         [24]  700 	mov	dptr,#_ak820_macro_write_PARM_2
      002B1C E0               [24]  701 	movx	a,@dptr
      002B1D FC               [12]  702 	mov	r4,a
      002B1E A3               [24]  703 	inc	dptr
      002B1F E0               [24]  704 	movx	a,@dptr
      002B20 FD               [12]  705 	mov	r5,a
      002B21 4C               [12]  706 	orl	a,r4
      002B22 60 20            [24]  707 	jz	00101$
      002B24 90 04 D1         [24]  708 	mov	dptr,#_ak820_macro_write_offset_10000_95
      002B27 E0               [24]  709 	movx	a,@dptr
      002B28 FA               [12]  710 	mov	r2,a
      002B29 A3               [24]  711 	inc	dptr
      002B2A E0               [24]  712 	movx	a,@dptr
      002B2B FB               [12]  713 	mov	r3,a
      002B2C 8A 00            [24]  714 	mov	ar0,r2
      002B2E 8B 01            [24]  715 	mov	ar1,r3
      002B30 74 E0            [12]  716 	mov	a,#0x100 - 0x20
      002B32 29               [12]  717 	add	a,r1
      002B33 40 0F            [24]  718 	jc	00101$
                                    719 ;	keyboards/ajazz/ak820/ak820_macro.c:110: size > DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE - offset) return false;
      002B35 E4               [12]  720 	clr	a
      002B36 C3               [12]  721 	clr	c
      002B37 9A               [12]  722 	subb	a,r2
      002B38 F8               [12]  723 	mov	r0,a
      002B39 74 20            [12]  724 	mov	a,#0x20
      002B3B 9B               [12]  725 	subb	a,r3
      002B3C F9               [12]  726 	mov	r1,a
      002B3D C3               [12]  727 	clr	c
      002B3E E8               [12]  728 	mov	a,r0
      002B3F 9C               [12]  729 	subb	a,r4
      002B40 E9               [12]  730 	mov	a,r1
      002B41 9D               [12]  731 	subb	a,r5
      002B42 50 04            [24]  732 	jnc	00102$
                                    733 ;	free result
      002B44                        734 00101$:
      002B44 75 82 00         [24]  735 	mov	dpl, #0x00
      002B47 22               [24]  736 	ret
      002B48                        737 00102$:
                                    738 ;	keyboards/ajazz/ak820/ak820_macro.c:111: end = offset + size;
      002B48 EC               [12]  739 	mov	a,r4
      002B49 2A               [12]  740 	add	a, r2
      002B4A F8               [12]  741 	mov	r0,a
      002B4B ED               [12]  742 	mov	a,r5
      002B4C 3B               [12]  743 	addc	a, r3
      002B4D F9               [12]  744 	mov	r1,a
                                    745 ;	keyboards/ajazz/ak820/ak820_macro.c:114: if (end <= covered && (uploading || offset || end == covered) && matches(offset, size, data)) return true;
      002B4E 90 04 B6         [24]  746 	mov	dptr,#_covered
      002B51 E0               [24]  747 	movx	a,@dptr
      002B52 F5 0A            [12]  748 	mov	_ak820_macro_write_sloc0_1_0,a
      002B54 A3               [24]  749 	inc	dptr
      002B55 E0               [24]  750 	movx	a,@dptr
      002B56 F5 0B            [12]  751 	mov	(_ak820_macro_write_sloc0_1_0 + 1),a
      002B58 C3               [12]  752 	clr	c
      002B59 E5 0A            [12]  753 	mov	a,_ak820_macro_write_sloc0_1_0
      002B5B 98               [12]  754 	subb	a,r0
      002B5C E5 0B            [12]  755 	mov	a,(_ak820_macro_write_sloc0_1_0 + 1)
      002B5E 99               [12]  756 	subb	a,r1
      002B5F 40 51            [24]  757 	jc	00107$
                                    758 ;	free result
      002B61 90 04 BA         [24]  759 	mov	dptr,#_uploading
      002B64 E0               [24]  760 	movx	a,@dptr
      002B65 70 0C            [24]  761 	jnz	00111$
      002B67 EA               [12]  762 	mov	a,r2
      002B68 4B               [12]  763 	orl	a,r3
      002B69 70 08            [24]  764 	jnz	00111$
      002B6B E8               [12]  765 	mov	a,r0
      002B6C B5 0A 43         [24]  766 	cjne	a,_ak820_macro_write_sloc0_1_0,00107$
      002B6F E9               [12]  767 	mov	a,r1
      002B70 B5 0B 3F         [24]  768 	cjne	a,(_ak820_macro_write_sloc0_1_0 + 1),00107$
      002B73                        769 00111$:
      002B73 90 04 D1         [24]  770 	mov	dptr,#_ak820_macro_write_offset_10000_95
      002B76 E0               [24]  771 	movx	a,@dptr
      002B77 FA               [12]  772 	mov	r2,a
      002B78 A3               [24]  773 	inc	dptr
      002B79 E0               [24]  774 	movx	a,@dptr
      002B7A FB               [12]  775 	mov	r3,a
      002B7B 90 04 C6         [24]  776 	mov	dptr,#_matches_PARM_2
      002B7E EC               [12]  777 	mov	a,r4
      002B7F F0               [24]  778 	movx	@dptr,a
      002B80 ED               [12]  779 	mov	a,r5
      002B81 A3               [24]  780 	inc	dptr
      002B82 F0               [24]  781 	movx	@dptr,a
      002B83 90 04 C8         [24]  782 	mov	dptr,#_matches_PARM_3
      002B86 EE               [12]  783 	mov	a,r6
      002B87 F0               [24]  784 	movx	@dptr,a
      002B88 EF               [12]  785 	mov	a,r7
      002B89 A3               [24]  786 	inc	dptr
      002B8A F0               [24]  787 	movx	@dptr,a
      002B8B 8A 82            [24]  788 	mov	dpl, r2
      002B8D 8B 83            [24]  789 	mov	dph, r3
      002B8F C0 07            [24]  790 	push	ar7
      002B91 C0 06            [24]  791 	push	ar6
      002B93 C0 05            [24]  792 	push	ar5
      002B95 C0 04            [24]  793 	push	ar4
      002B97 C0 01            [24]  794 	push	ar1
      002B99 C0 00            [24]  795 	push	ar0
      002B9B 12 29 DC         [24]  796 	lcall	_matches
      002B9E E5 82            [12]  797 	mov	a, dpl
      002BA0 D0 00            [24]  798 	pop	ar0
      002BA2 D0 01            [24]  799 	pop	ar1
      002BA4 D0 04            [24]  800 	pop	ar4
      002BA6 D0 05            [24]  801 	pop	ar5
      002BA8 D0 06            [24]  802 	pop	ar6
      002BAA D0 07            [24]  803 	pop	ar7
      002BAC 60 04            [24]  804 	jz	00107$
      002BAE 75 82 01         [24]  805 	mov	dpl, #0x01
      002BB1 22               [24]  806 	ret
      002BB2                        807 00107$:
                                    808 ;	keyboards/ajazz/ak820/ak820_macro.c:116: if (!uploading) {
      002BB2 90 04 BA         [24]  809 	mov	dptr,#_uploading
      002BB5 E0               [24]  810 	movx	a,@dptr
      002BB6 60 03            [24]  811 	jz	00371$
      002BB8 02 2C 53         [24]  812 	ljmp	00130$
      002BBB                        813 00371$:
                                    814 ;	keyboards/ajazz/ak820/ak820_macro.c:117: if (offset) {
      002BBB 90 04 D1         [24]  815 	mov	dptr,#_ak820_macro_write_offset_10000_95
      002BBE E0               [24]  816 	movx	a,@dptr
      002BBF FA               [12]  817 	mov	r2,a
      002BC0 A3               [24]  818 	inc	dptr
      002BC1 E0               [24]  819 	movx	a,@dptr
      002BC2 FB               [12]  820 	mov	r3,a
      002BC3 90 04 D1         [24]  821 	mov	dptr,#_ak820_macro_write_offset_10000_95
      002BC6 E0               [24]  822 	movx	a,@dptr
      002BC7 F5 F0            [12]  823 	mov	b,a
      002BC9 A3               [24]  824 	inc	dptr
      002BCA E0               [24]  825 	movx	a,@dptr
      002BCB 45 F0            [12]  826 	orl	a,b
      002BCD 60 78            [24]  827 	jz	00120$
                                    828 ;	keyboards/ajazz/ak820/ak820_macro.c:121: if (!covered || offset != covered || !ak820_macro_ready()) return false;
      002BCF 90 04 B6         [24]  829 	mov	dptr,#_covered
      002BD2 E0               [24]  830 	movx	a,@dptr
      002BD3 F5 0A            [12]  831 	mov	_ak820_macro_write_sloc0_1_0,a
      002BD5 A3               [24]  832 	inc	dptr
      002BD6 E0               [24]  833 	movx	a,@dptr
      002BD7 F5 0B            [12]  834 	mov	(_ak820_macro_write_sloc0_1_0 + 1),a
      002BD9 90 04 B6         [24]  835 	mov	dptr,#_covered
      002BDC E0               [24]  836 	movx	a,@dptr
      002BDD F5 F0            [12]  837 	mov	b,a
      002BDF A3               [24]  838 	inc	dptr
      002BE0 E0               [24]  839 	movx	a,@dptr
      002BE1 45 F0            [12]  840 	orl	a,b
      002BE3 60 27            [24]  841 	jz	00112$
      002BE5 EA               [12]  842 	mov	a,r2
      002BE6 B5 0A 23         [24]  843 	cjne	a,_ak820_macro_write_sloc0_1_0,00112$
      002BE9 EB               [12]  844 	mov	a,r3
      002BEA B5 0B 1F         [24]  845 	cjne	a,(_ak820_macro_write_sloc0_1_0 + 1),00112$
      002BED C0 07            [24]  846 	push	ar7
      002BEF C0 06            [24]  847 	push	ar6
      002BF1 C0 05            [24]  848 	push	ar5
      002BF3 C0 04            [24]  849 	push	ar4
      002BF5 C0 01            [24]  850 	push	ar1
      002BF7 C0 00            [24]  851 	push	ar0
      002BF9 12 2A AC         [24]  852 	lcall	_ak820_macro_ready
      002BFC E5 82            [12]  853 	mov	a, dpl
      002BFE D0 00            [24]  854 	pop	ar0
      002C00 D0 01            [24]  855 	pop	ar1
      002C02 D0 04            [24]  856 	pop	ar4
      002C04 D0 05            [24]  857 	pop	ar5
      002C06 D0 06            [24]  858 	pop	ar6
      002C08 D0 07            [24]  859 	pop	ar7
      002C0A 70 04            [24]  860 	jnz	00200$
      002C0C                        861 00112$:
      002C0C 75 82 00         [24]  862 	mov	dpl, #0x00
      002C0F 22               [24]  863 	ret
                                    864 ;	keyboards/ajazz/ak820/ak820_macro.c:122: for (i = 0; i < size; ++i) if (data[i]) return false;
      002C10                        865 00200$:
      002C10 7A 00            [12]  866 	mov	r2,#0x00
      002C12 7B 00            [12]  867 	mov	r3,#0x00
      002C14                        868 00148$:
      002C14 C3               [12]  869 	clr	c
      002C15 EA               [12]  870 	mov	a,r2
      002C16 9C               [12]  871 	subb	a,r4
      002C17 EB               [12]  872 	mov	a,r3
      002C18 9D               [12]  873 	subb	a,r5
      002C19 50 20            [24]  874 	jnc	00118$
      002C1B C0 00            [24]  875 	push	ar0
      002C1D C0 01            [24]  876 	push	ar1
      002C1F EA               [12]  877 	mov	a,r2
      002C20 2E               [12]  878 	add	a, r6
      002C21 F8               [12]  879 	mov	r0,a
      002C22 EB               [12]  880 	mov	a,r3
      002C23 3F               [12]  881 	addc	a, r7
      002C24 F9               [12]  882 	mov	r1,a
      002C25 88 82            [24]  883 	mov	dpl,r0
      002C27 89 83            [24]  884 	mov	dph,r1
      002C29 E0               [24]  885 	movx	a,@dptr
      002C2A D0 01            [24]  886 	pop	ar1
      002C2C D0 00            [24]  887 	pop	ar0
      002C2E 60 04            [24]  888 	jz	00149$
      002C30 75 82 00         [24]  889 	mov	dpl, #0x00
      002C33 22               [24]  890 	ret
      002C34                        891 00149$:
      002C34 0A               [12]  892 	inc	r2
      002C35 BA 00 DC         [24]  893 	cjne	r2,#0x00,00148$
      002C38 0B               [12]  894 	inc	r3
      002C39 80 D9            [24]  895 	sjmp	00148$
      002C3B                        896 00118$:
                                    897 ;	keyboards/ajazz/ak820/ak820_macro.c:123: covered = end;
      002C3B 90 04 B6         [24]  898 	mov	dptr,#_covered
      002C3E E8               [12]  899 	mov	a,r0
      002C3F F0               [24]  900 	movx	@dptr,a
      002C40 E9               [12]  901 	mov	a,r1
      002C41 A3               [24]  902 	inc	dptr
      002C42 F0               [24]  903 	movx	@dptr,a
                                    904 ;	keyboards/ajazz/ak820/ak820_macro.c:124: return true;
      002C43 75 82 01         [24]  905 	mov	dpl, #0x01
      002C46 22               [24]  906 	ret
      002C47                        907 00120$:
                                    908 ;	keyboards/ajazz/ak820/ak820_macro.c:126: next.terminated = next.arguments = 0;
      002C47 90 04 D4         [24]  909 	mov	dptr,#(_ak820_macro_write_next_10000_96 + 0x0001)
      002C4A E4               [12]  910 	clr	a
      002C4B F0               [24]  911 	movx	@dptr,a
      002C4C 90 04 D3         [24]  912 	mov	dptr,#_ak820_macro_write_next_10000_96
      002C4F F0               [24]  913 	movx	@dptr,a
      002C50 02 2D 0E         [24]  914 	ljmp	00208$
      002C53                        915 00130$:
                                    916 ;	keyboards/ajazz/ak820/ak820_macro.c:128: if (offset > covered) return false; /* A hole is never old EEPROM data. */
      002C53 90 04 D1         [24]  917 	mov	dptr,#_ak820_macro_write_offset_10000_95
      002C56 E0               [24]  918 	movx	a,@dptr
      002C57 FA               [12]  919 	mov	r2,a
      002C58 A3               [24]  920 	inc	dptr
      002C59 E0               [24]  921 	movx	a,@dptr
      002C5A FB               [12]  922 	mov	r3,a
      002C5B 90 04 B6         [24]  923 	mov	dptr,#_covered
      002C5E E0               [24]  924 	movx	a,@dptr
      002C5F F5 0A            [12]  925 	mov	_ak820_macro_write_sloc0_1_0,a
      002C61 A3               [24]  926 	inc	dptr
      002C62 E0               [24]  927 	movx	a,@dptr
      002C63 F5 0B            [12]  928 	mov	(_ak820_macro_write_sloc0_1_0 + 1),a
      002C65 C3               [12]  929 	clr	c
      002C66 E5 0A            [12]  930 	mov	a,_ak820_macro_write_sloc0_1_0
      002C68 9A               [12]  931 	subb	a,r2
      002C69 E5 0B            [12]  932 	mov	a,(_ak820_macro_write_sloc0_1_0 + 1)
      002C6B 9B               [12]  933 	subb	a,r3
      002C6C 50 04            [24]  934 	jnc	00122$
                                    935 ;	free result
      002C6E 75 82 00         [24]  936 	mov	dpl, #0x00
      002C71 22               [24]  937 	ret
      002C72                        938 00122$:
                                    939 ;	keyboards/ajazz/ak820/ak820_macro.c:129: if (offset == covered) {
      002C72 EA               [12]  940 	mov	a,r2
      002C73 B5 0A 3C         [24]  941 	cjne	a,_ak820_macro_write_sloc0_1_0,00127$
      002C76 EB               [12]  942 	mov	a,r3
      002C77 B5 0B 38         [24]  943 	cjne	a,(_ak820_macro_write_sloc0_1_0 + 1),00127$
                                    944 ;	keyboards/ajazz/ak820/ak820_macro.c:130: next = parsed;
      002C7A 90 0B 90         [24]  945 	mov	dptr,#___memcpy_PARM_2
      002C7D 74 B4            [12]  946 	mov	a,#_parsed
      002C7F F0               [24]  947 	movx	@dptr,a
      002C80 74 04            [12]  948 	mov	a,#(_parsed >> 8)
      002C82 A3               [24]  949 	inc	dptr
      002C83 F0               [24]  950 	movx	@dptr,a
      002C84 E4               [12]  951 	clr	a
      002C85 A3               [24]  952 	inc	dptr
      002C86 F0               [24]  953 	movx	@dptr,a
      002C87 90 0B 93         [24]  954 	mov	dptr,#___memcpy_PARM_3
      002C8A 74 02            [12]  955 	mov	a,#0x02
      002C8C F0               [24]  956 	movx	@dptr,a
      002C8D E4               [12]  957 	clr	a
      002C8E A3               [24]  958 	inc	dptr
      002C8F F0               [24]  959 	movx	@dptr,a
      002C90 90 04 D3         [24]  960 	mov	dptr,#_ak820_macro_write_next_10000_96
      002C93 F5 F0            [12]  961 	mov	b,a
      002C95 C0 07            [24]  962 	push	ar7
      002C97 C0 06            [24]  963 	push	ar6
      002C99 C0 05            [24]  964 	push	ar5
      002C9B C0 04            [24]  965 	push	ar4
      002C9D C0 01            [24]  966 	push	ar1
      002C9F C0 00            [24]  967 	push	ar0
      002CA1 12 B4 BE         [24]  968 	lcall	___memcpy
      002CA4 D0 00            [24]  969 	pop	ar0
      002CA6 D0 01            [24]  970 	pop	ar1
      002CA8 D0 04            [24]  971 	pop	ar4
      002CAA D0 05            [24]  972 	pop	ar5
      002CAC D0 06            [24]  973 	pop	ar6
      002CAE D0 07            [24]  974 	pop	ar7
      002CB0 80 5C            [24]  975 	sjmp	00208$
      002CB2                        976 00127$:
                                    977 ;	keyboards/ajazz/ak820/ak820_macro.c:135: next.terminated = next.arguments = 0;
      002CB2 90 04 D4         [24]  978 	mov	dptr,#(_ak820_macro_write_next_10000_96 + 0x0001)
      002CB5 E4               [12]  979 	clr	a
      002CB6 F0               [24]  980 	movx	@dptr,a
      002CB7 90 04 D3         [24]  981 	mov	dptr,#_ak820_macro_write_next_10000_96
      002CBA F0               [24]  982 	movx	@dptr,a
                                    983 ;	keyboards/ajazz/ak820/ak820_macro.c:136: for (i = 0; i < offset; ++i) if (!parse_byte(&next, macro_byte(i))) return false;
      002CBB F5 0A            [12]  984 	mov	_ak820_macro_write_sloc0_1_0,a
      002CBD F5 0B            [12]  985 	mov	(_ak820_macro_write_sloc0_1_0 + 1),a
      002CBF                        986 00151$:
      002CBF C3               [12]  987 	clr	c
      002CC0 E5 0A            [12]  988 	mov	a,_ak820_macro_write_sloc0_1_0
      002CC2 9A               [12]  989 	subb	a,r2
      002CC3 E5 0B            [12]  990 	mov	a,(_ak820_macro_write_sloc0_1_0 + 1)
      002CC5 9B               [12]  991 	subb	a,r3
      002CC6 50 46            [24]  992 	jnc	00208$
      002CC8 85 0A 82         [24]  993 	mov	dpl, _ak820_macro_write_sloc0_1_0
      002CCB 85 0B 83         [24]  994 	mov	dph, (_ak820_macro_write_sloc0_1_0 + 1)
      002CCE C0 07            [24]  995 	push	ar7
      002CD0 C0 06            [24]  996 	push	ar6
      002CD2 C0 05            [24]  997 	push	ar5
      002CD4 C0 04            [24]  998 	push	ar4
      002CD6 C0 03            [24]  999 	push	ar3
      002CD8 C0 02            [24] 1000 	push	ar2
      002CDA C0 01            [24] 1001 	push	ar1
      002CDC C0 00            [24] 1002 	push	ar0
      002CDE 12 28 A0         [24] 1003 	lcall	_macro_byte
      002CE1 E5 82            [12] 1004 	mov	a, dpl
      002CE3 90 04 C3         [24] 1005 	mov	dptr,#_parse_byte_PARM_2
      002CE6 F0               [24] 1006 	movx	@dptr,a
      002CE7 90 04 D3         [24] 1007 	mov	dptr,#_ak820_macro_write_next_10000_96
      002CEA 12 29 36         [24] 1008 	lcall	_parse_byte
      002CED E5 82            [12] 1009 	mov	a, dpl
      002CEF D0 00            [24] 1010 	pop	ar0
      002CF1 D0 01            [24] 1011 	pop	ar1
      002CF3 D0 02            [24] 1012 	pop	ar2
      002CF5 D0 03            [24] 1013 	pop	ar3
      002CF7 D0 04            [24] 1014 	pop	ar4
      002CF9 D0 05            [24] 1015 	pop	ar5
      002CFB D0 06            [24] 1016 	pop	ar6
      002CFD D0 07            [24] 1017 	pop	ar7
      002CFF 70 03            [24] 1018 	jnz	00152$
      002D01 F5 82            [12] 1019 	mov	dpl,a
      002D03 22               [24] 1020 	ret
      002D04                       1021 00152$:
      002D04 05 0A            [12] 1022 	inc	_ak820_macro_write_sloc0_1_0
      002D06 E4               [12] 1023 	clr	a
                                   1024 ;	keyboards/ajazz/ak820/ak820_macro.c:139: for (i = 0; i < size; ++i) if (!parse_byte(&next, data[i])) return false;
      002D07 B5 0A B5         [24] 1025 	cjne	a,_ak820_macro_write_sloc0_1_0,00151$
      002D0A 05 0B            [12] 1026 	inc	(_ak820_macro_write_sloc0_1_0 + 1)
      002D0C 80 B1            [24] 1027 	sjmp	00151$
      002D0E                       1028 00208$:
      002D0E 7A 00            [12] 1029 	mov	r2,#0x00
      002D10 7B 00            [12] 1030 	mov	r3,#0x00
      002D12                       1031 00154$:
      002D12 C3               [12] 1032 	clr	c
      002D13 EA               [12] 1033 	mov	a,r2
      002D14 9C               [12] 1034 	subb	a,r4
      002D15 EB               [12] 1035 	mov	a,r3
      002D16 9D               [12] 1036 	subb	a,r5
      002D17 50 4A            [24] 1037 	jnc	00134$
      002D19 C0 00            [24] 1038 	push	ar0
      002D1B C0 01            [24] 1039 	push	ar1
      002D1D EA               [12] 1040 	mov	a,r2
      002D1E 2E               [12] 1041 	add	a, r6
      002D1F F5 82            [12] 1042 	mov	dpl,a
      002D21 EB               [12] 1043 	mov	a,r3
      002D22 3F               [12] 1044 	addc	a, r7
      002D23 F5 83            [12] 1045 	mov	dph,a
      002D25 E0               [24] 1046 	movx	a,@dptr
      002D26 F9               [12] 1047 	mov	r1,a
      002D27 90 04 C3         [24] 1048 	mov	dptr,#_parse_byte_PARM_2
      002D2A F0               [24] 1049 	movx	@dptr,a
      002D2B 90 04 D3         [24] 1050 	mov	dptr,#_ak820_macro_write_next_10000_96
      002D2E C0 07            [24] 1051 	push	ar7
      002D30 C0 06            [24] 1052 	push	ar6
      002D32 C0 05            [24] 1053 	push	ar5
      002D34 C0 04            [24] 1054 	push	ar4
      002D36 C0 03            [24] 1055 	push	ar3
      002D38 C0 02            [24] 1056 	push	ar2
      002D3A C0 01            [24] 1057 	push	ar1
      002D3C C0 00            [24] 1058 	push	ar0
      002D3E 12 29 36         [24] 1059 	lcall	_parse_byte
      002D41 E5 82            [12] 1060 	mov	a, dpl
      002D43 D0 00            [24] 1061 	pop	ar0
      002D45 D0 01            [24] 1062 	pop	ar1
      002D47 D0 02            [24] 1063 	pop	ar2
      002D49 D0 03            [24] 1064 	pop	ar3
      002D4B D0 04            [24] 1065 	pop	ar4
      002D4D D0 05            [24] 1066 	pop	ar5
      002D4F D0 06            [24] 1067 	pop	ar6
      002D51 D0 07            [24] 1068 	pop	ar7
      002D53 D0 01            [24] 1069 	pop	ar1
      002D55 D0 00            [24] 1070 	pop	ar0
      002D57 70 03            [24] 1071 	jnz	00155$
      002D59 F5 82            [12] 1072 	mov	dpl,a
      002D5B 22               [24] 1073 	ret
      002D5C                       1074 00155$:
      002D5C 0A               [12] 1075 	inc	r2
      002D5D BA 00 B2         [24] 1076 	cjne	r2,#0x00,00154$
      002D60 0B               [12] 1077 	inc	r3
      002D61 80 AF            [24] 1078 	sjmp	00154$
      002D63                       1079 00134$:
                                   1080 ;	keyboards/ajazz/ak820/ak820_macro.c:140: complete = next.terminated == DYNAMIC_KEYMAP_MACRO_COUNT;
      002D63 90 04 D3         [24] 1081 	mov	dptr,#_ak820_macro_write_next_10000_96
      002D66 E0               [24] 1082 	movx	a,@dptr
      002D67 FB               [12] 1083 	mov	r3,a
      002D68 E4               [12] 1084 	clr	a
      002D69 BB 10 01         [24] 1085 	cjne	r3,#0x10,00389$
      002D6C 04               [12] 1086 	inc	a
      002D6D                       1087 00389$:
                                   1088 ;	keyboards/ajazz/ak820/ak820_macro.c:141: if (!complete && end == DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE) return false;
      002D6D F5 0A            [12] 1089 	mov	_ak820_macro_write_sloc0_1_0,a
      002D6F 70 0E            [24] 1090 	jnz	00136$
      002D71 88 02            [24] 1091 	mov	ar2,r0
      002D73 89 03            [24] 1092 	mov	ar3,r1
      002D75 BA 00 07         [24] 1093 	cjne	r2,#0x00,00136$
      002D78 BB 20 04         [24] 1094 	cjne	r3,#0x20,00136$
      002D7B 75 82 00         [24] 1095 	mov	dpl, #0x00
      002D7E 22               [24] 1096 	ret
      002D7F                       1097 00136$:
                                   1098 ;	keyboards/ajazz/ak820/ak820_macro.c:143: ak820_nvm_begin();
      002D7F C0 07            [24] 1099 	push	ar7
      002D81 C0 06            [24] 1100 	push	ar6
      002D83 C0 05            [24] 1101 	push	ar5
      002D85 C0 04            [24] 1102 	push	ar4
      002D87 C0 01            [24] 1103 	push	ar1
      002D89 C0 00            [24] 1104 	push	ar0
      002D8B 12 3C 83         [24] 1105 	lcall	_ak820_nvm_begin
      002D8E D0 00            [24] 1106 	pop	ar0
      002D90 D0 01            [24] 1107 	pop	ar1
      002D92 D0 04            [24] 1108 	pop	ar4
      002D94 D0 05            [24] 1109 	pop	ar5
      002D96 D0 06            [24] 1110 	pop	ar6
      002D98 D0 07            [24] 1111 	pop	ar7
                                   1112 ;	keyboards/ajazz/ak820/ak820_macro.c:144: if (!uploading) {
      002D9A 90 04 BA         [24] 1113 	mov	dptr,#_uploading
      002D9D E0               [24] 1114 	movx	a,@dptr
      002D9E 70 2C            [24] 1115 	jnz	00141$
                                   1116 ;	keyboards/ajazz/ak820/ak820_macro.c:146: busy_write(1);
      002DA0 75 82 01         [24] 1117 	mov	dpl, #0x01
      002DA3 C0 07            [24] 1118 	push	ar7
      002DA5 C0 06            [24] 1119 	push	ar6
      002DA7 C0 05            [24] 1120 	push	ar5
      002DA9 C0 04            [24] 1121 	push	ar4
      002DAB C0 01            [24] 1122 	push	ar1
      002DAD C0 00            [24] 1123 	push	ar0
      002DAF 12 28 C0         [24] 1124 	lcall	_busy_write
      002DB2 D0 00            [24] 1125 	pop	ar0
      002DB4 D0 01            [24] 1126 	pop	ar1
      002DB6 D0 04            [24] 1127 	pop	ar4
      002DB8 D0 05            [24] 1128 	pop	ar5
      002DBA D0 06            [24] 1129 	pop	ar6
      002DBC D0 07            [24] 1130 	pop	ar7
                                   1131 ;	keyboards/ajazz/ak820/ak820_macro.c:147: if (!ak820_nvm_ok()) { ak820_nvm_end(); return false; }
      002DBE 12 3A D2         [24] 1132 	lcall	_ak820_nvm_ok
      002DC1 E5 82            [12] 1133 	mov	a, dpl
      002DC3 70 07            [24] 1134 	jnz	00141$
      002DC5 12 3C 98         [24] 1135 	lcall	_ak820_nvm_end
      002DC8 75 82 00         [24] 1136 	mov	dpl, #0x00
      002DCB 22               [24] 1137 	ret
      002DCC                       1138 00141$:
                                   1139 ;	keyboards/ajazz/ak820/ak820_macro.c:149: eeprom_write_block(data, (void *)(uintptr_t)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + offset), size);
      002DCC C0 00            [24] 1140 	push	ar0
      002DCE C0 01            [24] 1141 	push	ar1
      002DD0 7B 00            [12] 1142 	mov	r3,#0x00
      002DD2 90 04 D1         [24] 1143 	mov	dptr,#_ak820_macro_write_offset_10000_95
      002DD5 E0               [24] 1144 	movx	a,@dptr
      002DD6 F9               [12] 1145 	mov	r1,a
      002DD7 A3               [24] 1146 	inc	dptr
      002DD8 E0               [24] 1147 	movx	a,@dptr
      002DD9 24 08            [12] 1148 	add	a,#0x08
      002DDB FA               [12] 1149 	mov	r2,a
      002DDC 90 05 49         [24] 1150 	mov	dptr,#_eeprom_write_block_PARM_2
      002DDF E9               [12] 1151 	mov	a,r1
      002DE0 F0               [24] 1152 	movx	@dptr,a
      002DE1 EA               [12] 1153 	mov	a,r2
      002DE2 A3               [24] 1154 	inc	dptr
      002DE3 F0               [24] 1155 	movx	@dptr,a
      002DE4 E4               [12] 1156 	clr	a
      002DE5 A3               [24] 1157 	inc	dptr
      002DE6 F0               [24] 1158 	movx	@dptr,a
      002DE7 90 05 4C         [24] 1159 	mov	dptr,#_eeprom_write_block_PARM_3
      002DEA EC               [12] 1160 	mov	a,r4
      002DEB F0               [24] 1161 	movx	@dptr,a
      002DEC ED               [12] 1162 	mov	a,r5
      002DED A3               [24] 1163 	inc	dptr
      002DEE F0               [24] 1164 	movx	@dptr,a
      002DEF 8E 82            [24] 1165 	mov	dpl, r6
      002DF1 8F 83            [24] 1166 	mov	dph, r7
      002DF3 8B F0            [24] 1167 	mov	b, r3
      002DF5 C0 01            [24] 1168 	push	ar1
      002DF7 C0 00            [24] 1169 	push	ar0
      002DF9 12 3E 86         [24] 1170 	lcall	_eeprom_write_block
                                   1171 ;	keyboards/ajazz/ak820/ak820_macro.c:150: ak820_nvm_flush();
      002DFC 12 3A EA         [24] 1172 	lcall	_ak820_nvm_flush
      002DFF D0 00            [24] 1173 	pop	ar0
      002E01 D0 01            [24] 1174 	pop	ar1
                                   1175 ;	keyboards/ajazz/ak820/ak820_macro.c:151: if (complete && ak820_nvm_ok()) commit_length(end);
      002E03 D0 01            [24] 1176 	pop	ar1
      002E05 D0 00            [24] 1177 	pop	ar0
      002E07 E5 0A            [12] 1178 	mov	a,_ak820_macro_write_sloc0_1_0
      002E09 60 16            [24] 1179 	jz	00143$
      002E0B 12 3A D2         [24] 1180 	lcall	_ak820_nvm_ok
      002E0E E5 82            [12] 1181 	mov	a, dpl
      002E10 60 0F            [24] 1182 	jz	00143$
      002E12 88 82            [24] 1183 	mov	dpl, r0
      002E14 89 83            [24] 1184 	mov	dph, r1
      002E16 C0 01            [24] 1185 	push	ar1
      002E18 C0 00            [24] 1186 	push	ar0
      002E1A 12 28 D7         [24] 1187 	lcall	_commit_length
      002E1D D0 00            [24] 1188 	pop	ar0
      002E1F D0 01            [24] 1189 	pop	ar1
      002E21                       1190 00143$:
                                   1191 ;	keyboards/ajazz/ak820/ak820_macro.c:152: ak820_nvm_end();
      002E21 C0 01            [24] 1192 	push	ar1
      002E23 C0 00            [24] 1193 	push	ar0
      002E25 12 3C 98         [24] 1194 	lcall	_ak820_nvm_end
      002E28 D0 00            [24] 1195 	pop	ar0
      002E2A D0 01            [24] 1196 	pop	ar1
                                   1197 ;	keyboards/ajazz/ak820/ak820_macro.c:153: if (!ak820_nvm_ok()) return false;
      002E2C 12 3A D2         [24] 1198 	lcall	_ak820_nvm_ok
      002E2F E5 82            [12] 1199 	mov	a, dpl
      002E31 70 03            [24] 1200 	jnz	00146$
      002E33 F5 82            [12] 1201 	mov	dpl,a
      002E35 22               [24] 1202 	ret
      002E36                       1203 00146$:
                                   1204 ;	keyboards/ajazz/ak820/ak820_macro.c:154: covered = end;
      002E36 90 04 B6         [24] 1205 	mov	dptr,#_covered
      002E39 E8               [12] 1206 	mov	a,r0
      002E3A F0               [24] 1207 	movx	@dptr,a
      002E3B E9               [12] 1208 	mov	a,r1
      002E3C A3               [24] 1209 	inc	dptr
      002E3D F0               [24] 1210 	movx	@dptr,a
                                   1211 ;	keyboards/ajazz/ak820/ak820_macro.c:155: parsed = next;
      002E3E 90 0B 90         [24] 1212 	mov	dptr,#___memcpy_PARM_2
      002E41 74 D3            [12] 1213 	mov	a,#_ak820_macro_write_next_10000_96
      002E43 F0               [24] 1214 	movx	@dptr,a
      002E44 74 04            [12] 1215 	mov	a,#(_ak820_macro_write_next_10000_96 >> 8)
      002E46 A3               [24] 1216 	inc	dptr
      002E47 F0               [24] 1217 	movx	@dptr,a
      002E48 E4               [12] 1218 	clr	a
      002E49 A3               [24] 1219 	inc	dptr
      002E4A F0               [24] 1220 	movx	@dptr,a
      002E4B 90 0B 93         [24] 1221 	mov	dptr,#___memcpy_PARM_3
      002E4E 74 02            [12] 1222 	mov	a,#0x02
      002E50 F0               [24] 1223 	movx	@dptr,a
      002E51 E4               [12] 1224 	clr	a
      002E52 A3               [24] 1225 	inc	dptr
      002E53 F0               [24] 1226 	movx	@dptr,a
      002E54 90 04 B4         [24] 1227 	mov	dptr,#_parsed
      002E57 F5 F0            [12] 1228 	mov	b,a
      002E59 12 B4 BE         [24] 1229 	lcall	___memcpy
                                   1230 ;	keyboards/ajazz/ak820/ak820_macro.c:156: uploading = !complete;
      002E5C 90 04 BA         [24] 1231 	mov	dptr,#_uploading
      002E5F E5 0A            [12] 1232 	mov	a,_ak820_macro_write_sloc0_1_0
      002E61 B4 01 00         [24] 1233 	cjne	a,#0x01,00399$
      002E64                       1234 00399$:
      002E64 E4               [12] 1235 	clr	a
      002E65 33               [12] 1236 	rlc	a
      002E66 F0               [24] 1237 	movx	@dptr,a
                                   1238 ;	keyboards/ajazz/ak820/ak820_macro.c:157: return true;
      002E67 75 82 01         [24] 1239 	mov	dpl, #0x01
                                   1240 ;	keyboards/ajazz/ak820/ak820_macro.c:158: }
      002E6A 22               [24] 1241 	ret
                                   1242 ;------------------------------------------------------------
                                   1243 ;Allocation info for local variables in function 'ak820_macro_reset'
                                   1244 ;------------------------------------------------------------
                                   1245 ;i             Allocated with name '_ak820_macro_reset_i_10000_123'
                                   1246 ;------------------------------------------------------------
                                   1247 ;	keyboards/ajazz/ak820/ak820_macro.c:160: bool ak820_macro_reset(void) {
                                   1248 ;	-----------------------------------------
                                   1249 ;	 function ak820_macro_reset
                                   1250 ;	-----------------------------------------
      002E6B                       1251 _ak820_macro_reset:
                                   1252 ;	keyboards/ajazz/ak820/ak820_macro.c:162: ak820_nvm_begin();
      002E6B 12 3C 83         [24] 1253 	lcall	_ak820_nvm_begin
                                   1254 ;	keyboards/ajazz/ak820/ak820_macro.c:163: busy_write(1);
      002E6E 75 82 01         [24] 1255 	mov	dpl, #0x01
      002E71 12 28 C0         [24] 1256 	lcall	_busy_write
                                   1257 ;	keyboards/ajazz/ak820/ak820_macro.c:164: if (ak820_nvm_ok()) {
      002E74 12 3A D2         [24] 1258 	lcall	_ak820_nvm_ok
      002E77 E5 82            [12] 1259 	mov	a, dpl
      002E79 60 3E            [24] 1260 	jz	00105$
                                   1261 ;	keyboards/ajazz/ak820/ak820_macro.c:165: for (i = 0; i < DYNAMIC_KEYMAP_MACRO_COUNT; ++i)
      002E7B 7E 00            [12] 1262 	mov	r6,#0x00
      002E7D 7F 00            [12] 1263 	mov	r7,#0x00
      002E7F                       1264 00106$:
                                   1265 ;	keyboards/ajazz/ak820/ak820_macro.c:166: eeprom_update_byte((uint8_t *)(uintptr_t)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + i), 0);
      002E7F 8E 04            [24] 1266 	mov	ar4,r6
      002E81 8F 05            [24] 1267 	mov	ar5,r7
      002E83 74 08            [12] 1268 	mov	a,#0x08
      002E85 2D               [12] 1269 	add	a, r5
      002E86 FD               [12] 1270 	mov	r5,a
      002E87 7B 00            [12] 1271 	mov	r3,#0x00
      002E89 90 05 B9         [24] 1272 	mov	dptr,#_eeprom_update_byte_PARM_2
      002E8C E4               [12] 1273 	clr	a
      002E8D F0               [24] 1274 	movx	@dptr,a
      002E8E 8C 82            [24] 1275 	mov	dpl, r4
      002E90 8D 83            [24] 1276 	mov	dph, r5
      002E92 8B F0            [24] 1277 	mov	b, r3
      002E94 12 46 7C         [24] 1278 	lcall	_eeprom_update_byte
                                   1279 ;	keyboards/ajazz/ak820/ak820_macro.c:165: for (i = 0; i < DYNAMIC_KEYMAP_MACRO_COUNT; ++i)
      002E97 0E               [12] 1280 	inc	r6
      002E98 BE 00 01         [24] 1281 	cjne	r6,#0x00,00140$
      002E9B 0F               [12] 1282 	inc	r7
      002E9C                       1283 00140$:
      002E9C 8E 04            [24] 1284 	mov	ar4,r6
      002E9E 8F 05            [24] 1285 	mov	ar5,r7
      002EA0 C3               [12] 1286 	clr	c
      002EA1 EC               [12] 1287 	mov	a,r4
      002EA2 94 10            [12] 1288 	subb	a,#0x10
      002EA4 ED               [12] 1289 	mov	a,r5
      002EA5 94 00            [12] 1290 	subb	a,#0x00
      002EA7 40 D6            [24] 1291 	jc	00106$
                                   1292 ;	keyboards/ajazz/ak820/ak820_macro.c:167: ak820_nvm_flush();
      002EA9 12 3A EA         [24] 1293 	lcall	_ak820_nvm_flush
                                   1294 ;	keyboards/ajazz/ak820/ak820_macro.c:168: if (ak820_nvm_ok()) commit_length(DYNAMIC_KEYMAP_MACRO_COUNT);
      002EAC 12 3A D2         [24] 1295 	lcall	_ak820_nvm_ok
      002EAF E5 82            [12] 1296 	mov	a, dpl
      002EB1 60 06            [24] 1297 	jz	00105$
      002EB3 90 00 10         [24] 1298 	mov	dptr,#0x0010
      002EB6 12 28 D7         [24] 1299 	lcall	_commit_length
      002EB9                       1300 00105$:
                                   1301 ;	keyboards/ajazz/ak820/ak820_macro.c:170: ak820_nvm_end();
      002EB9 12 3C 98         [24] 1302 	lcall	_ak820_nvm_end
                                   1303 ;	keyboards/ajazz/ak820/ak820_macro.c:171: ak820_macro_init();
      002EBC 12 2A 70         [24] 1304 	lcall	_ak820_macro_init
                                   1305 ;	keyboards/ajazz/ak820/ak820_macro.c:172: return ak820_nvm_ok();
                                   1306 ;	keyboards/ajazz/ak820/ak820_macro.c:173: }
      002EBF 02 3A D2         [24] 1307 	ljmp	_ak820_nvm_ok
                                   1308 	.area AK820LOW(CODE)
                                   1309 	.area CONST   (CODE)
                                   1310 	.area XINIT   (CODE)
                                   1311 	.area CABS    (ABS,CODE)
