                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module ak820_nvm
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _eeprom_driver_erase
                                     12 	.globl _eeprom_write_block
                                     13 	.globl _eeprom_read_block
                                     14 	.globl _eeprom_driver_init
                                     15 	.globl _ak820_macro_init
                                     16 	.globl _ak820_flash_program_page
                                     17 	.globl _ak820_flash_program
                                     18 	.globl _ak820_flash_erase
                                     19 	.globl _ak820_flash_read
                                     20 	.globl _eeprom_write_block_PARM_3
                                     21 	.globl _eeprom_write_block_PARM_2
                                     22 	.globl _eeprom_read_block_PARM_3
                                     23 	.globl _eeprom_read_block_PARM_2
                                     24 	.globl _ak820_nvm_diagnostic
                                     25 	.globl _ak820_nvm_ok
                                     26 	.globl _ak820_nvm_schema_fault
                                     27 	.globl _ak820_nvm_flush
                                     28 	.globl _ak820_nvm_begin
                                     29 	.globl _ak820_nvm_end
                                     30 ;--------------------------------------------------------
                                     31 ; special function registers
                                     32 ;--------------------------------------------------------
                                     33 	.area RSEG    (ABS,DATA)
      000000                         34 	.org 0x0000
                                     35 ;--------------------------------------------------------
                                     36 ; special function bits
                                     37 ;--------------------------------------------------------
                                     38 	.area RSEG    (ABS,DATA)
      000000                         39 	.org 0x0000
                                     40 ;--------------------------------------------------------
                                     41 ; overlayable register banks
                                     42 ;--------------------------------------------------------
                                     43 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                         44 	.ds 8
                                     45 ;--------------------------------------------------------
                                     46 ; internal ram data
                                     47 ;--------------------------------------------------------
                                     48 	.area DSEG    (DATA)
      00000C                         49 _eeprom_write_block_sloc0_1_0:
      00000C                         50 	.ds 2
                                     51 ;--------------------------------------------------------
                                     52 ; overlayable items in internal ram
                                     53 ;--------------------------------------------------------
                                     54 ;--------------------------------------------------------
                                     55 ; indirectly addressable internal ram data
                                     56 ;--------------------------------------------------------
                                     57 	.area ISEG    (DATA)
                                     58 ;--------------------------------------------------------
                                     59 ; absolute internal ram data
                                     60 ;--------------------------------------------------------
                                     61 	.area IABS    (ABS,DATA)
                                     62 	.area IABS    (ABS,DATA)
                                     63 ;--------------------------------------------------------
                                     64 ; bit data
                                     65 ;--------------------------------------------------------
                                     66 	.area BSEG    (BIT)
      000003                         67 _ak820_nvm_ok_sloc0_1_0:
      000003                         68 	.ds 1
      000004                         69 _load_page_sloc0_1_0:
      000004                         70 	.ds 1
                                     71 ;--------------------------------------------------------
                                     72 ; paged external ram data
                                     73 ;--------------------------------------------------------
                                     74 	.area PSEG    (PAG,XDATA)
                                     75 ;--------------------------------------------------------
                                     76 ; uninitialized external ram data
                                     77 ;--------------------------------------------------------
                                     78 	.area XSEG    (XDATA)
      0004D5                         79 _page_data:
      0004D5                         80 	.ds 64
      000515                         81 _cached_page:
      000515                         82 	.ds 2
      000517                         83 _page_valid:
      000517                         84 	.ds 1
      000518                         85 _page_dirty:
      000518                         86 	.ds 1
      000519                         87 _storage_failed:
      000519                         88 	.ds 1
      00051A                         89 _batch_depth:
      00051A                         90 	.ds 1
      00051B                         91 _first_failure_stage:
      00051B                         92 	.ds 1
      00051C                         93 _nvm_fail_stage_10000_17:
      00051C                         94 	.ds 1
      00051D                         95 _ak820_nvm_diagnostic_out_10000_20:
      00051D                         96 	.ds 2
      00051F                         97 _crc_byte_PARM_2:
      00051F                         98 	.ds 1
      000520                         99 _crc_byte_crc_10000_22:
      000520                        100 	.ds 2
      000522                        101 _page_crc_crc_10000_27:
      000522                        102 	.ds 2
      000524                        103 _write_page_address_10000_29:
      000524                        104 	.ds 2
      000526                        105 _journal_header_valid_header_10000_36:
      000526                        106 	.ds 2
      000528                        107 _recover_journal_header_10000_43:
      000528                        108 	.ds 9
      000531                        109 _ak820_nvm_flush_header_10000_59:
      000531                        110 	.ds 9
      00053A                        111 _ak820_nvm_flush_stage_10000_59:
      00053A                        112 	.ds 1
      00053B                        113 _load_page_page_10000_84:
      00053B                        114 	.ds 2
      00053D                        115 _eeprom_read_block_PARM_2:
      00053D                        116 	.ds 3
      000540                        117 _eeprom_read_block_PARM_3:
      000540                        118 	.ds 2
      000542                        119 _eeprom_read_block_buf_10000_90:
      000542                        120 	.ds 3
      000545                        121 _eeprom_read_block_out_10000_91:
      000545                        122 	.ds 3
      000548                        123 _eeprom_write_block_PARM_2:
      000548                        124 	.ds 3
      00054B                        125 _eeprom_write_block_PARM_3:
      00054B                        126 	.ds 2
      00054D                        127 _eeprom_write_block_buf_10000_96:
      00054D                        128 	.ds 3
                                    129 ;--------------------------------------------------------
                                    130 ; absolute external ram data
                                    131 ;--------------------------------------------------------
                                    132 	.area XABS    (ABS,XDATA)
                                    133 ;--------------------------------------------------------
                                    134 ; initialized external ram data
                                    135 ;--------------------------------------------------------
                                    136 	.area XISEG   (XDATA)
                                    137 	.area HOME    (CODE)
                                    138 	.area GSINIT0 (CODE)
                                    139 	.area GSINIT1 (CODE)
                                    140 	.area GSINIT2 (CODE)
                                    141 	.area GSINIT3 (CODE)
                                    142 	.area GSINIT4 (CODE)
                                    143 	.area GSINIT5 (CODE)
                                    144 	.area GSINIT  (CODE)
                                    145 	.area GSFINAL (CODE)
                                    146 	.area CSEG    (CODE)
                                    147 ;--------------------------------------------------------
                                    148 ; global & static initialisations
                                    149 ;--------------------------------------------------------
                                    150 	.area HOME    (CODE)
                                    151 	.area GSINIT  (CODE)
                                    152 	.area GSFINAL (CODE)
                                    153 	.area GSINIT  (CODE)
                                    154 ;--------------------------------------------------------
                                    155 ; Home
                                    156 ;--------------------------------------------------------
                                    157 	.area HOME    (CODE)
                                    158 	.area HOME    (CODE)
                                    159 ;--------------------------------------------------------
                                    160 ; code
                                    161 ;--------------------------------------------------------
                                    162 	.area CSEG    (CODE)
                                    163 ;------------------------------------------------------------
                                    164 ;Allocation info for local variables in function 'nvm_fail'
                                    165 ;------------------------------------------------------------
                                    166 ;stage         Allocated with name '_nvm_fail_stage_10000_17'
                                    167 ;------------------------------------------------------------
                                    168 ;	keyboards/ajazz/ak820/ak820_nvm.c:17: static void nvm_fail(uint8_t stage) {
                                    169 ;	-----------------------------------------
                                    170 ;	 function nvm_fail
                                    171 ;	-----------------------------------------
      0037A6                        172 _nvm_fail:
                           000007   173 	ar7 = 0x07
                           000006   174 	ar6 = 0x06
                           000005   175 	ar5 = 0x05
                           000004   176 	ar4 = 0x04
                           000003   177 	ar3 = 0x03
                           000002   178 	ar2 = 0x02
                           000001   179 	ar1 = 0x01
                           000000   180 	ar0 = 0x00
      0037A6 E5 82            [12]  181 	mov	a,dpl
      0037A8 90 05 1C         [24]  182 	mov	dptr,#_nvm_fail_stage_10000_17
      0037AB F0               [24]  183 	movx	@dptr,a
                                    184 ;	keyboards/ajazz/ak820/ak820_nvm.c:18: if (!storage_failed) first_failure_stage = stage;
      0037AC 90 05 19         [24]  185 	mov	dptr,#_storage_failed
      0037AF E0               [24]  186 	movx	a,@dptr
      0037B0 70 08            [24]  187 	jnz	00102$
      0037B2 90 05 1C         [24]  188 	mov	dptr,#_nvm_fail_stage_10000_17
      0037B5 E0               [24]  189 	movx	a,@dptr
      0037B6 90 05 1B         [24]  190 	mov	dptr,#_first_failure_stage
      0037B9 F0               [24]  191 	movx	@dptr,a
      0037BA                        192 00102$:
                                    193 ;	keyboards/ajazz/ak820/ak820_nvm.c:19: storage_failed = true;
      0037BA 90 05 19         [24]  194 	mov	dptr,#_storage_failed
      0037BD 74 01            [12]  195 	mov	a,#0x01
      0037BF F0               [24]  196 	movx	@dptr,a
                                    197 ;	keyboards/ajazz/ak820/ak820_nvm.c:20: }
      0037C0 22               [24]  198 	ret
                                    199 ;------------------------------------------------------------
                                    200 ;Allocation info for local variables in function 'ak820_nvm_diagnostic'
                                    201 ;------------------------------------------------------------
                                    202 ;out           Allocated with name '_ak820_nvm_diagnostic_out_10000_20'
                                    203 ;------------------------------------------------------------
                                    204 ;	keyboards/ajazz/ak820/ak820_nvm.c:22: void ak820_nvm_diagnostic(uint8_t AK820_XDATA *out) {
                                    205 ;	-----------------------------------------
                                    206 ;	 function ak820_nvm_diagnostic
                                    207 ;	-----------------------------------------
      0037C1                        208 _ak820_nvm_diagnostic:
      0037C1 AF 83            [24]  209 	mov	r7,dph
      0037C3 E5 82            [12]  210 	mov	a,dpl
      0037C5 90 05 1D         [24]  211 	mov	dptr,#_ak820_nvm_diagnostic_out_10000_20
      0037C8 F0               [24]  212 	movx	@dptr,a
      0037C9 EF               [12]  213 	mov	a,r7
      0037CA A3               [24]  214 	inc	dptr
      0037CB F0               [24]  215 	movx	@dptr,a
                                    216 ;	keyboards/ajazz/ak820/ak820_nvm.c:23: out[0] = storage_failed;
      0037CC 90 05 1D         [24]  217 	mov	dptr,#_ak820_nvm_diagnostic_out_10000_20
      0037CF E0               [24]  218 	movx	a,@dptr
      0037D0 FE               [12]  219 	mov	r6,a
      0037D1 A3               [24]  220 	inc	dptr
      0037D2 E0               [24]  221 	movx	a,@dptr
      0037D3 FF               [12]  222 	mov	r7,a
      0037D4 90 05 19         [24]  223 	mov	dptr,#_storage_failed
      0037D7 E0               [24]  224 	movx	a,@dptr
      0037D8 8E 82            [24]  225 	mov	dpl,r6
      0037DA 8F 83            [24]  226 	mov	dph,r7
      0037DC F0               [24]  227 	movx	@dptr,a
                                    228 ;	keyboards/ajazz/ak820/ak820_nvm.c:24: out[1] = page_valid;
      0037DD 74 01            [12]  229 	mov	a,#0x01
      0037DF 2E               [12]  230 	add	a, r6
      0037E0 FC               [12]  231 	mov	r4,a
      0037E1 E4               [12]  232 	clr	a
      0037E2 3F               [12]  233 	addc	a, r7
      0037E3 FD               [12]  234 	mov	r5,a
      0037E4 90 05 17         [24]  235 	mov	dptr,#_page_valid
      0037E7 E0               [24]  236 	movx	a,@dptr
      0037E8 8C 82            [24]  237 	mov	dpl,r4
      0037EA 8D 83            [24]  238 	mov	dph,r5
      0037EC F0               [24]  239 	movx	@dptr,a
                                    240 ;	keyboards/ajazz/ak820/ak820_nvm.c:25: out[2] = page_dirty;
      0037ED 74 02            [12]  241 	mov	a,#0x02
      0037EF 2E               [12]  242 	add	a, r6
      0037F0 FC               [12]  243 	mov	r4,a
      0037F1 E4               [12]  244 	clr	a
      0037F2 3F               [12]  245 	addc	a, r7
      0037F3 FD               [12]  246 	mov	r5,a
      0037F4 90 05 18         [24]  247 	mov	dptr,#_page_dirty
      0037F7 E0               [24]  248 	movx	a,@dptr
      0037F8 8C 82            [24]  249 	mov	dpl,r4
      0037FA 8D 83            [24]  250 	mov	dph,r5
      0037FC F0               [24]  251 	movx	@dptr,a
                                    252 ;	keyboards/ajazz/ak820/ak820_nvm.c:26: out[3] = batch_depth;
      0037FD 74 03            [12]  253 	mov	a,#0x03
      0037FF 2E               [12]  254 	add	a, r6
      003800 FC               [12]  255 	mov	r4,a
      003801 E4               [12]  256 	clr	a
      003802 3F               [12]  257 	addc	a, r7
      003803 FD               [12]  258 	mov	r5,a
      003804 90 05 1A         [24]  259 	mov	dptr,#_batch_depth
      003807 E0               [24]  260 	movx	a,@dptr
      003808 8C 82            [24]  261 	mov	dpl,r4
      00380A 8D 83            [24]  262 	mov	dph,r5
      00380C F0               [24]  263 	movx	@dptr,a
                                    264 ;	keyboards/ajazz/ak820/ak820_nvm.c:27: out[4] = (uint8_t)cached_page;
      00380D 74 04            [12]  265 	mov	a,#0x04
      00380F 2E               [12]  266 	add	a, r6
      003810 FC               [12]  267 	mov	r4,a
      003811 E4               [12]  268 	clr	a
      003812 3F               [12]  269 	addc	a, r7
      003813 FD               [12]  270 	mov	r5,a
      003814 90 05 15         [24]  271 	mov	dptr,#_cached_page
      003817 E0               [24]  272 	movx	a,@dptr
      003818 8C 82            [24]  273 	mov	dpl,r4
      00381A 8D 83            [24]  274 	mov	dph,r5
      00381C F0               [24]  275 	movx	@dptr,a
                                    276 ;	keyboards/ajazz/ak820/ak820_nvm.c:28: out[5] = (uint8_t)(cached_page >> 8);
      00381D 74 05            [12]  277 	mov	a,#0x05
      00381F 2E               [12]  278 	add	a, r6
      003820 FC               [12]  279 	mov	r4,a
      003821 E4               [12]  280 	clr	a
      003822 3F               [12]  281 	addc	a, r7
      003823 FD               [12]  282 	mov	r5,a
      003824 90 05 15         [24]  283 	mov	dptr,#_cached_page
      003827 E0               [24]  284 	movx	a,@dptr
      003828 A3               [24]  285 	inc	dptr
      003829 E0               [24]  286 	movx	a,@dptr
      00382A 8C 82            [24]  287 	mov	dpl,r4
      00382C 8D 83            [24]  288 	mov	dph,r5
      00382E F0               [24]  289 	movx	@dptr,a
                                    290 ;	keyboards/ajazz/ak820/ak820_nvm.c:29: out[6] = first_failure_stage;
      00382F 74 06            [12]  291 	mov	a,#0x06
      003831 2E               [12]  292 	add	a, r6
      003832 FE               [12]  293 	mov	r6,a
      003833 E4               [12]  294 	clr	a
      003834 3F               [12]  295 	addc	a, r7
      003835 FF               [12]  296 	mov	r7,a
      003836 90 05 1B         [24]  297 	mov	dptr,#_first_failure_stage
      003839 E0               [24]  298 	movx	a,@dptr
      00383A 8E 82            [24]  299 	mov	dpl,r6
      00383C 8F 83            [24]  300 	mov	dph,r7
      00383E F0               [24]  301 	movx	@dptr,a
                                    302 ;	keyboards/ajazz/ak820/ak820_nvm.c:30: }
      00383F 22               [24]  303 	ret
                                    304 ;------------------------------------------------------------
                                    305 ;Allocation info for local variables in function 'crc_byte'
                                    306 ;------------------------------------------------------------
                                    307 ;value         Allocated with name '_crc_byte_PARM_2'
                                    308 ;crc           Allocated with name '_crc_byte_crc_10000_22'
                                    309 ;bit           Allocated with name '_crc_byte_bit_10000_23'
                                    310 ;------------------------------------------------------------
                                    311 ;	keyboards/ajazz/ak820/ak820_nvm.c:32: static uint16_t crc_byte(uint16_t crc, uint8_t value) {
                                    312 ;	-----------------------------------------
                                    313 ;	 function crc_byte
                                    314 ;	-----------------------------------------
      003840                        315 _crc_byte:
      003840 AF 83            [24]  316 	mov	r7,dph
      003842 E5 82            [12]  317 	mov	a,dpl
      003844 90 05 20         [24]  318 	mov	dptr,#_crc_byte_crc_10000_22
      003847 F0               [24]  319 	movx	@dptr,a
      003848 EF               [12]  320 	mov	a,r7
      003849 A3               [24]  321 	inc	dptr
      00384A F0               [24]  322 	movx	@dptr,a
                                    323 ;	keyboards/ajazz/ak820/ak820_nvm.c:34: crc ^= (uint16_t)value << 8;
      00384B 90 05 1F         [24]  324 	mov	dptr,#_crc_byte_PARM_2
      00384E E0               [24]  325 	movx	a,@dptr
      00384F FF               [12]  326 	mov	r7,a
      003850 7E 00            [12]  327 	mov	r6,#0x00
      003852 90 05 20         [24]  328 	mov	dptr,#_crc_byte_crc_10000_22
      003855 E0               [24]  329 	movx	a,@dptr
      003856 6E               [12]  330 	xrl	a,r6
      003857 F0               [24]  331 	movx	@dptr,a
      003858 A3               [24]  332 	inc	dptr
      003859 E0               [24]  333 	movx	a,@dptr
      00385A 6F               [12]  334 	xrl	a,r7
      00385B F0               [24]  335 	movx	@dptr,a
                                    336 ;	keyboards/ajazz/ak820/ak820_nvm.c:35: for (bit = 0; bit != 8; ++bit) {
      00385C 7F 00            [12]  337 	mov	r7,#0x00
      00385E                        338 00102$:
                                    339 ;	keyboards/ajazz/ak820/ak820_nvm.c:36: crc = (crc & 0x8000u) ? (uint16_t)((crc << 1) ^ 0x1021u) : (uint16_t)(crc << 1);
      00385E 90 05 20         [24]  340 	mov	dptr,#_crc_byte_crc_10000_22
      003861 E0               [24]  341 	movx	a,@dptr
      003862 FD               [12]  342 	mov	r5,a
      003863 A3               [24]  343 	inc	dptr
      003864 E0               [24]  344 	movx	a,@dptr
      003865 FE               [12]  345 	mov	r6,a
      003866 30 E7 0E         [24]  346 	jnb	acc.7,00106$
      003869 ED               [12]  347 	mov	a,r5
      00386A 2D               [12]  348 	add	a,r5
      00386B FB               [12]  349 	mov	r3,a
      00386C EE               [12]  350 	mov	a,r6
      00386D 33               [12]  351 	rlc	a
      00386E FC               [12]  352 	mov	r4,a
      00386F 63 03 21         [24]  353 	xrl	ar3,#0x21
      003872 63 04 10         [24]  354 	xrl	ar4,#0x10
      003875 80 06            [24]  355 	sjmp	00107$
      003877                        356 00106$:
      003877 ED               [12]  357 	mov	a,r5
      003878 2D               [12]  358 	add	a,r5
      003879 FB               [12]  359 	mov	r3,a
      00387A EE               [12]  360 	mov	a,r6
      00387B 33               [12]  361 	rlc	a
      00387C FC               [12]  362 	mov	r4,a
      00387D                        363 00107$:
      00387D 90 05 20         [24]  364 	mov	dptr,#_crc_byte_crc_10000_22
      003880 EB               [12]  365 	mov	a,r3
      003881 F0               [24]  366 	movx	@dptr,a
      003882 EC               [12]  367 	mov	a,r4
      003883 A3               [24]  368 	inc	dptr
      003884 F0               [24]  369 	movx	@dptr,a
                                    370 ;	keyboards/ajazz/ak820/ak820_nvm.c:35: for (bit = 0; bit != 8; ++bit) {
      003885 0F               [12]  371 	inc	r7
      003886 BF 08 D5         [24]  372 	cjne	r7,#0x08,00102$
                                    373 ;	keyboards/ajazz/ak820/ak820_nvm.c:38: return crc;
      003889 8B 82            [24]  374 	mov	dpl, r3
      00388B 8C 83            [24]  375 	mov	dph, r4
                                    376 ;	keyboards/ajazz/ak820/ak820_nvm.c:39: }
      00388D 22               [24]  377 	ret
                                    378 ;------------------------------------------------------------
                                    379 ;Allocation info for local variables in function 'page_crc'
                                    380 ;------------------------------------------------------------
                                    381 ;crc           Allocated with name '_page_crc_crc_10000_27'
                                    382 ;i             Allocated with name '_page_crc_i_10000_27'
                                    383 ;------------------------------------------------------------
                                    384 ;	keyboards/ajazz/ak820/ak820_nvm.c:41: static uint16_t page_crc(void) {
                                    385 ;	-----------------------------------------
                                    386 ;	 function page_crc
                                    387 ;	-----------------------------------------
      00388E                        388 _page_crc:
                                    389 ;	keyboards/ajazz/ak820/ak820_nvm.c:42: uint16_t crc = 0xFFFFu;
      00388E 90 05 22         [24]  390 	mov	dptr,#_page_crc_crc_10000_27
      003891 74 FF            [12]  391 	mov	a,#0xff
      003893 F0               [24]  392 	movx	@dptr,a
      003894 A3               [24]  393 	inc	dptr
      003895 F0               [24]  394 	movx	@dptr,a
                                    395 ;	keyboards/ajazz/ak820/ak820_nvm.c:44: for (i = 0; i != AK820_FLASH_PAGE; ++i) crc = crc_byte(crc, page_data[i]);
      003896 7F 00            [12]  396 	mov	r7,#0x00
      003898                        397 00102$:
      003898 90 05 22         [24]  398 	mov	dptr,#_page_crc_crc_10000_27
      00389B E0               [24]  399 	movx	a,@dptr
      00389C FD               [12]  400 	mov	r5,a
      00389D A3               [24]  401 	inc	dptr
      00389E E0               [24]  402 	movx	a,@dptr
      00389F FE               [12]  403 	mov	r6,a
      0038A0 EF               [12]  404 	mov	a,r7
      0038A1 24 D5            [12]  405 	add	a, #_page_data
      0038A3 F5 82            [12]  406 	mov	dpl,a
      0038A5 E4               [12]  407 	clr	a
      0038A6 34 04            [12]  408 	addc	a, #(_page_data >> 8)
      0038A8 F5 83            [12]  409 	mov	dph,a
      0038AA E0               [24]  410 	movx	a,@dptr
      0038AB 90 05 1F         [24]  411 	mov	dptr,#_crc_byte_PARM_2
      0038AE F0               [24]  412 	movx	@dptr,a
      0038AF 8D 82            [24]  413 	mov	dpl, r5
      0038B1 8E 83            [24]  414 	mov	dph, r6
      0038B3 C0 07            [24]  415 	push	ar7
      0038B5 12 38 40         [24]  416 	lcall	_crc_byte
      0038B8 AD 82            [24]  417 	mov	r5, dpl
      0038BA AE 83            [24]  418 	mov	r6, dph
      0038BC D0 07            [24]  419 	pop	ar7
      0038BE 90 05 22         [24]  420 	mov	dptr,#_page_crc_crc_10000_27
      0038C1 ED               [12]  421 	mov	a,r5
      0038C2 F0               [24]  422 	movx	@dptr,a
      0038C3 EE               [12]  423 	mov	a,r6
      0038C4 A3               [24]  424 	inc	dptr
      0038C5 F0               [24]  425 	movx	@dptr,a
      0038C6 0F               [12]  426 	inc	r7
      0038C7 BF 40 CE         [24]  427 	cjne	r7,#0x40,00102$
                                    428 ;	keyboards/ajazz/ak820/ak820_nvm.c:45: return crc;
      0038CA 8D 82            [24]  429 	mov	dpl, r5
      0038CC 8E 83            [24]  430 	mov	dph, r6
                                    431 ;	keyboards/ajazz/ak820/ak820_nvm.c:46: }
      0038CE 22               [24]  432 	ret
                                    433 ;------------------------------------------------------------
                                    434 ;Allocation info for local variables in function 'write_page'
                                    435 ;------------------------------------------------------------
                                    436 ;address       Allocated with name '_write_page_address_10000_29'
                                    437 ;i             Allocated with name '_write_page_i_10000_30'
                                    438 ;------------------------------------------------------------
                                    439 ;	keyboards/ajazz/ak820/ak820_nvm.c:48: static bool write_page(uint16_t address) {
                                    440 ;	-----------------------------------------
                                    441 ;	 function write_page
                                    442 ;	-----------------------------------------
      0038CF                        443 _write_page:
      0038CF AF 83            [24]  444 	mov	r7,dph
      0038D1 E5 82            [12]  445 	mov	a,dpl
      0038D3 90 05 24         [24]  446 	mov	dptr,#_write_page_address_10000_29
      0038D6 F0               [24]  447 	movx	@dptr,a
      0038D7 EF               [12]  448 	mov	a,r7
      0038D8 A3               [24]  449 	inc	dptr
      0038D9 F0               [24]  450 	movx	@dptr,a
                                    451 ;	keyboards/ajazz/ak820/ak820_nvm.c:50: if (!ak820_flash_erase(address)) return false;
      0038DA 90 05 24         [24]  452 	mov	dptr,#_write_page_address_10000_29
      0038DD E0               [24]  453 	movx	a,@dptr
      0038DE FE               [12]  454 	mov	r6,a
      0038DF A3               [24]  455 	inc	dptr
      0038E0 E0               [24]  456 	movx	a,@dptr
      0038E1 FF               [12]  457 	mov	r7,a
      0038E2 8E 82            [24]  458 	mov	dpl, r6
      0038E4 8F 83            [24]  459 	mov	dph, r7
      0038E6 C0 07            [24]  460 	push	ar7
      0038E8 C0 06            [24]  461 	push	ar6
      0038EA 12 36 1F         [24]  462 	lcall	_ak820_flash_erase
      0038ED E5 82            [12]  463 	mov	a, dpl
      0038EF D0 06            [24]  464 	pop	ar6
      0038F1 D0 07            [24]  465 	pop	ar7
      0038F3 70 03            [24]  466 	jnz	00102$
      0038F5 F5 82            [12]  467 	mov	dpl,a
      0038F7 22               [24]  468 	ret
      0038F8                        469 00102$:
                                    470 ;	keyboards/ajazz/ak820/ak820_nvm.c:51: if (!ak820_flash_program_page(address, page_data)) return false;
      0038F8 90 04 B0         [24]  471 	mov	dptr,#_ak820_flash_program_page_PARM_2
      0038FB 74 D5            [12]  472 	mov	a,#_page_data
      0038FD F0               [24]  473 	movx	@dptr,a
      0038FE 74 04            [12]  474 	mov	a,#(_page_data >> 8)
      003900 A3               [24]  475 	inc	dptr
      003901 F0               [24]  476 	movx	@dptr,a
      003902 8E 82            [24]  477 	mov	dpl, r6
      003904 8F 83            [24]  478 	mov	dph, r7
      003906 12 37 33         [24]  479 	lcall	_ak820_flash_program_page
      003909 E5 82            [12]  480 	mov	a, dpl
      00390B 70 03            [24]  481 	jnz	00120$
      00390D F5 82            [12]  482 	mov	dpl,a
                                    483 ;	keyboards/ajazz/ak820/ak820_nvm.c:52: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      00390F 22               [24]  484 	ret
      003910                        485 00120$:
      003910 7F 00            [12]  486 	mov	r7,#0x00
      003912                        487 00108$:
                                    488 ;	keyboards/ajazz/ak820/ak820_nvm.c:53: if (ak820_flash_read(address + i) != page_data[i]) return false;
      003912 8F 05            [24]  489 	mov	ar5,r7
      003914 7E 00            [12]  490 	mov	r6,#0x00
      003916 90 05 24         [24]  491 	mov	dptr,#_write_page_address_10000_29
      003919 E0               [24]  492 	movx	a,@dptr
      00391A FB               [12]  493 	mov	r3,a
      00391B A3               [24]  494 	inc	dptr
      00391C E0               [24]  495 	movx	a,@dptr
      00391D FC               [12]  496 	mov	r4,a
      00391E ED               [12]  497 	mov	a,r5
      00391F 2B               [12]  498 	add	a, r3
      003920 FB               [12]  499 	mov	r3,a
      003921 EE               [12]  500 	mov	a,r6
      003922 3C               [12]  501 	addc	a, r4
      003923 FC               [12]  502 	mov	r4,a
      003924 8B 82            [24]  503 	mov	dpl, r3
      003926 8C 83            [24]  504 	mov	dph, r4
      003928 12 35 12         [24]  505 	lcall	_ak820_flash_read
      00392B AE 82            [24]  506 	mov	r6, dpl
      00392D EF               [12]  507 	mov	a,r7
      00392E 24 D5            [12]  508 	add	a, #_page_data
      003930 F5 82            [12]  509 	mov	dpl,a
      003932 E4               [12]  510 	clr	a
      003933 34 04            [12]  511 	addc	a, #(_page_data >> 8)
      003935 F5 83            [12]  512 	mov	dph,a
      003937 E0               [24]  513 	movx	a,@dptr
      003938 FD               [12]  514 	mov	r5,a
      003939 EE               [12]  515 	mov	a,r6
      00393A B5 05 02         [24]  516 	cjne	a,ar5,00149$
      00393D 80 04            [24]  517 	sjmp	00109$
      00393F                        518 00149$:
      00393F 75 82 00         [24]  519 	mov	dpl, #0x00
      003942 22               [24]  520 	ret
      003943                        521 00109$:
                                    522 ;	keyboards/ajazz/ak820/ak820_nvm.c:52: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003943 0F               [12]  523 	inc	r7
      003944 BF 40 CB         [24]  524 	cjne	r7,#0x40,00108$
                                    525 ;	keyboards/ajazz/ak820/ak820_nvm.c:55: return true;
      003947 75 82 01         [24]  526 	mov	dpl, #0x01
                                    527 ;	keyboards/ajazz/ak820/ak820_nvm.c:56: }
      00394A 22               [24]  528 	ret
                                    529 ;------------------------------------------------------------
                                    530 ;Allocation info for local variables in function 'journal_header_valid'
                                    531 ;------------------------------------------------------------
                                    532 ;header        Allocated with name '_journal_header_valid_header_10000_36'
                                    533 ;i             Allocated with name '_journal_header_valid_i_10000_37'
                                    534 ;------------------------------------------------------------
                                    535 ;	keyboards/ajazz/ak820/ak820_nvm.c:58: static bool journal_header_valid(uint8_t AK820_XDATA *header) {
                                    536 ;	-----------------------------------------
                                    537 ;	 function journal_header_valid
                                    538 ;	-----------------------------------------
      00394B                        539 _journal_header_valid:
      00394B AF 83            [24]  540 	mov	r7,dph
      00394D E5 82            [12]  541 	mov	a,dpl
      00394F 90 05 26         [24]  542 	mov	dptr,#_journal_header_valid_header_10000_36
      003952 F0               [24]  543 	movx	@dptr,a
      003953 EF               [12]  544 	mov	a,r7
      003954 A3               [24]  545 	inc	dptr
      003955 F0               [24]  546 	movx	@dptr,a
                                    547 ;	keyboards/ajazz/ak820/ak820_nvm.c:60: if (header[0] != 0xA5u) return false;
      003956 90 05 26         [24]  548 	mov	dptr,#_journal_header_valid_header_10000_36
      003959 E0               [24]  549 	movx	a,@dptr
      00395A FE               [12]  550 	mov	r6,a
      00395B A3               [24]  551 	inc	dptr
      00395C E0               [24]  552 	movx	a,@dptr
      00395D FF               [12]  553 	mov	r7,a
      00395E 8E 82            [24]  554 	mov	dpl,r6
      003960 8F 83            [24]  555 	mov	dph,r7
      003962 E0               [24]  556 	movx	a,@dptr
      003963 FD               [12]  557 	mov	r5,a
      003964 BD A5 02         [24]  558 	cjne	r5,#0xa5,00138$
      003967 80 04            [24]  559 	sjmp	00116$
      003969                        560 00138$:
      003969 75 82 00         [24]  561 	mov	dpl, #0x00
                                    562 ;	keyboards/ajazz/ak820/ak820_nvm.c:61: for (i = 1; i != 5; ++i) {
      00396C 22               [24]  563 	ret
      00396D                        564 00116$:
      00396D 7D 01            [12]  565 	mov	r5,#0x01
      00396F                        566 00106$:
                                    567 ;	keyboards/ajazz/ak820/ak820_nvm.c:62: if ((uint8_t)(header[i] ^ header[i + 4]) != 0xFFu) return false;
      00396F ED               [12]  568 	mov	a,r5
      003970 2E               [12]  569 	add	a, r6
      003971 F5 82            [12]  570 	mov	dpl,a
      003973 E4               [12]  571 	clr	a
      003974 3F               [12]  572 	addc	a, r7
      003975 F5 83            [12]  573 	mov	dph,a
      003977 E0               [24]  574 	movx	a,@dptr
      003978 FC               [12]  575 	mov	r4,a
      003979 8D 02            [24]  576 	mov	ar2,r5
      00397B 7B 00            [12]  577 	mov	r3,#0x00
      00397D 74 04            [12]  578 	mov	a,#0x04
      00397F 2A               [12]  579 	add	a, r2
      003980 FA               [12]  580 	mov	r2,a
      003981 E4               [12]  581 	clr	a
      003982 3B               [12]  582 	addc	a, r3
      003983 FB               [12]  583 	mov	r3,a
      003984 EA               [12]  584 	mov	a,r2
      003985 2E               [12]  585 	add	a, r6
      003986 F5 82            [12]  586 	mov	dpl,a
      003988 EB               [12]  587 	mov	a,r3
      003989 3F               [12]  588 	addc	a, r7
      00398A F5 83            [12]  589 	mov	dph,a
      00398C E0               [24]  590 	movx	a,@dptr
      00398D 62 04            [12]  591 	xrl	ar4,a
      00398F BC FF 02         [24]  592 	cjne	r4,#0xff,00139$
      003992 80 04            [24]  593 	sjmp	00107$
      003994                        594 00139$:
      003994 75 82 00         [24]  595 	mov	dpl, #0x00
      003997 22               [24]  596 	ret
      003998                        597 00107$:
                                    598 ;	keyboards/ajazz/ak820/ak820_nvm.c:61: for (i = 1; i != 5; ++i) {
      003998 0D               [12]  599 	inc	r5
      003999 BD 05 D3         [24]  600 	cjne	r5,#0x05,00106$
                                    601 ;	keyboards/ajazz/ak820/ak820_nvm.c:64: return true;
      00399C 75 82 01         [24]  602 	mov	dpl, #0x01
                                    603 ;	keyboards/ajazz/ak820/ak820_nvm.c:65: }
      00399F 22               [24]  604 	ret
                                    605 ;------------------------------------------------------------
                                    606 ;Allocation info for local variables in function 'recover_journal'
                                    607 ;------------------------------------------------------------
                                    608 ;header        Allocated with name '_recover_journal_header_10000_43'
                                    609 ;i             Allocated with name '_recover_journal_i_10000_43'
                                    610 ;page          Allocated with name '_recover_journal_page_10000_43'
                                    611 ;crc           Allocated with name '_recover_journal_crc_10000_43'
                                    612 ;------------------------------------------------------------
                                    613 ;	keyboards/ajazz/ak820/ak820_nvm.c:67: static void recover_journal(void) {
                                    614 ;	-----------------------------------------
                                    615 ;	 function recover_journal
                                    616 ;	-----------------------------------------
      0039A0                        617 _recover_journal:
                                    618 ;	keyboards/ajazz/ak820/ak820_nvm.c:71: for (i = 0; i != sizeof(header); ++i) header[i] = ak820_flash_read(AK820_JOURNAL_HEADER + i);
      0039A0 7F 00            [12]  619 	mov	r7,#0x00
      0039A2                        620 00115$:
      0039A2 EF               [12]  621 	mov	a,r7
      0039A3 24 28            [12]  622 	add	a, #_recover_journal_header_10000_43
      0039A5 FD               [12]  623 	mov	r5,a
      0039A6 E4               [12]  624 	clr	a
      0039A7 34 05            [12]  625 	addc	a, #(_recover_journal_header_10000_43 >> 8)
      0039A9 FE               [12]  626 	mov	r6,a
      0039AA 8F 04            [24]  627 	mov	ar4,r7
      0039AC 7B 00            [12]  628 	mov	r3,#0x00
      0039AE 74 40            [12]  629 	mov	a,#0x40
      0039B0 2C               [12]  630 	add	a, r4
      0039B1 FC               [12]  631 	mov	r4,a
      0039B2 74 EF            [12]  632 	mov	a,#0xef
      0039B4 3B               [12]  633 	addc	a, r3
      0039B5 FB               [12]  634 	mov	r3,a
      0039B6 8C 82            [24]  635 	mov	dpl, r4
      0039B8 8B 83            [24]  636 	mov	dph, r3
      0039BA 12 35 12         [24]  637 	lcall	_ak820_flash_read
      0039BD AC 82            [24]  638 	mov	r4, dpl
      0039BF 8D 82            [24]  639 	mov	dpl,r5
      0039C1 8E 83            [24]  640 	mov	dph,r6
      0039C3 EC               [12]  641 	mov	a,r4
      0039C4 F0               [24]  642 	movx	@dptr,a
      0039C5 0F               [12]  643 	inc	r7
      0039C6 BF 09 D9         [24]  644 	cjne	r7,#0x09,00115$
                                    645 ;	keyboards/ajazz/ak820/ak820_nvm.c:74: if (!journal_header_valid(header)) return;
      0039C9 90 05 28         [24]  646 	mov	dptr,#_recover_journal_header_10000_43
      0039CC 12 39 4B         [24]  647 	lcall	_journal_header_valid
      0039CF E5 82            [12]  648 	mov	a, dpl
      0039D1 70 01            [24]  649 	jnz	00103$
      0039D3 22               [24]  650 	ret
      0039D4                        651 00103$:
                                    652 ;	keyboards/ajazz/ak820/ak820_nvm.c:75: page = (uint16_t)header[1] | ((uint16_t)header[2] << 8);
      0039D4 90 05 29         [24]  653 	mov	dptr,#(_recover_journal_header_10000_43 + 0x0001)
      0039D7 E0               [24]  654 	movx	a,@dptr
      0039D8 FF               [12]  655 	mov	r7,a
      0039D9 7E 00            [12]  656 	mov	r6,#0x00
      0039DB 90 05 2A         [24]  657 	mov	dptr,#(_recover_journal_header_10000_43 + 0x0002)
      0039DE E0               [24]  658 	movx	a,@dptr
      0039DF FC               [12]  659 	mov	r4,a
      0039E0 E4               [12]  660 	clr	a
      0039E1 42 07            [12]  661 	orl	ar7,a
      0039E3 EC               [12]  662 	mov	a,r4
      0039E4 42 06            [12]  663 	orl	ar6,a
                                    664 ;	keyboards/ajazz/ak820/ak820_nvm.c:76: crc = (uint16_t)header[3] | ((uint16_t)header[4] << 8);
      0039E6 90 05 2B         [24]  665 	mov	dptr,#(_recover_journal_header_10000_43 + 0x0003)
      0039E9 E0               [24]  666 	movx	a,@dptr
      0039EA FD               [12]  667 	mov	r5,a
      0039EB 7C 00            [12]  668 	mov	r4,#0x00
      0039ED 90 05 2C         [24]  669 	mov	dptr,#(_recover_journal_header_10000_43 + 0x0004)
      0039F0 E0               [24]  670 	movx	a,@dptr
      0039F1 FA               [12]  671 	mov	r2,a
      0039F2 E4               [12]  672 	clr	a
      0039F3 42 05            [12]  673 	orl	ar5,a
      0039F5 EA               [12]  674 	mov	a,r2
      0039F6 42 04            [12]  675 	orl	ar4,a
                                    676 ;	keyboards/ajazz/ak820/ak820_nvm.c:77: if (page >= AK820_NVM_SIZE / AK820_FLASH_PAGE) {
      0039F8 C3               [12]  677 	clr	c
      0039F9 EF               [12]  678 	mov	a,r7
      0039FA 94 A0            [12]  679 	subb	a,#0xa0
      0039FC EE               [12]  680 	mov	a,r6
      0039FD 94 00            [12]  681 	subb	a,#0x00
      0039FF 40 06            [24]  682 	jc	00134$
                                    683 ;	keyboards/ajazz/ak820/ak820_nvm.c:78: nvm_fail(AK820_NVM_FAULT_RECOVERY_PAGE);
      003A01 75 82 01         [24]  684 	mov	dpl, #0x01
                                    685 ;	keyboards/ajazz/ak820/ak820_nvm.c:79: return;
      003A04 02 37 A6         [24]  686 	ljmp	_nvm_fail
                                    687 ;	keyboards/ajazz/ak820/ak820_nvm.c:81: for (i = 0; i != AK820_FLASH_PAGE; ++i) page_data[i] = ak820_flash_read(AK820_JOURNAL_DATA + i);
      003A07                        688 00134$:
      003A07 7B 00            [12]  689 	mov	r3,#0x00
      003A09                        690 00117$:
      003A09 C0 05            [24]  691 	push	ar5
      003A0B C0 04            [24]  692 	push	ar4
      003A0D EB               [12]  693 	mov	a,r3
      003A0E 24 D5            [12]  694 	add	a, #_page_data
      003A10 F9               [12]  695 	mov	r1,a
      003A11 E4               [12]  696 	clr	a
      003A12 34 04            [12]  697 	addc	a, #(_page_data >> 8)
      003A14 FA               [12]  698 	mov	r2,a
      003A15 8B 00            [24]  699 	mov	ar0,r3
      003A17 7D 00            [12]  700 	mov	r5,#0x00
      003A19 74 EF            [12]  701 	mov	a,#0xef
      003A1B 2D               [12]  702 	add	a, r5
      003A1C FD               [12]  703 	mov	r5,a
      003A1D 88 82            [24]  704 	mov	dpl, r0
      003A1F 8D 83            [24]  705 	mov	dph, r5
      003A21 12 35 12         [24]  706 	lcall	_ak820_flash_read
      003A24 AD 82            [24]  707 	mov	r5, dpl
      003A26 89 82            [24]  708 	mov	dpl,r1
      003A28 8A 83            [24]  709 	mov	dph,r2
      003A2A ED               [12]  710 	mov	a,r5
      003A2B F0               [24]  711 	movx	@dptr,a
      003A2C 0B               [12]  712 	inc	r3
      003A2D BB 40 02         [24]  713 	cjne	r3,#0x40,00190$
      003A30 80 06            [24]  714 	sjmp	00191$
      003A32                        715 00190$:
      003A32 D0 04            [24]  716 	pop	ar4
      003A34 D0 05            [24]  717 	pop	ar5
      003A36 80 D1            [24]  718 	sjmp	00117$
      003A38                        719 00191$:
      003A38 D0 04            [24]  720 	pop	ar4
      003A3A D0 05            [24]  721 	pop	ar5
                                    722 ;	keyboards/ajazz/ak820/ak820_nvm.c:82: if (page_crc() != crc) nvm_fail(AK820_NVM_FAULT_RECOVERY_CRC);
      003A3C C0 07            [24]  723 	push	ar7
      003A3E C0 06            [24]  724 	push	ar6
      003A40 C0 05            [24]  725 	push	ar5
      003A42 C0 04            [24]  726 	push	ar4
      003A44 12 38 8E         [24]  727 	lcall	_page_crc
      003A47 AA 82            [24]  728 	mov	r2, dpl
      003A49 AB 83            [24]  729 	mov	r3, dph
      003A4B D0 04            [24]  730 	pop	ar4
      003A4D D0 05            [24]  731 	pop	ar5
      003A4F D0 06            [24]  732 	pop	ar6
      003A51 D0 07            [24]  733 	pop	ar7
      003A53 EA               [12]  734 	mov	a,r2
      003A54 B5 05 06         [24]  735 	cjne	a,ar5,00192$
      003A57 EB               [12]  736 	mov	a,r3
      003A58 B5 04 02         [24]  737 	cjne	a,ar4,00192$
      003A5B 80 06            [24]  738 	sjmp	00113$
      003A5D                        739 00192$:
      003A5D 75 82 02         [24]  740 	mov	dpl, #0x02
      003A60 02 37 A6         [24]  741 	ljmp	_nvm_fail
      003A63                        742 00113$:
                                    743 ;	keyboards/ajazz/ak820/ak820_nvm.c:83: else if (!write_page(AK820_NVM_BASE + page * AK820_FLASH_PAGE)) nvm_fail(AK820_NVM_FAULT_RECOVERY_WRITE);
      003A63 EE               [12]  744 	mov	a,r6
      003A64 54 03            [12]  745 	anl	a,#0x03
      003A66 A2 E0            [12]  746 	mov	c,acc.0
      003A68 CF               [12]  747 	xch	a,r7
      003A69 13               [12]  748 	rrc	a
      003A6A CF               [12]  749 	xch	a,r7
      003A6B 13               [12]  750 	rrc	a
      003A6C A2 E0            [12]  751 	mov	c,acc.0
      003A6E CF               [12]  752 	xch	a,r7
      003A6F 13               [12]  753 	rrc	a
      003A70 CF               [12]  754 	xch	a,r7
      003A71 13               [12]  755 	rrc	a
      003A72 CF               [12]  756 	xch	a,r7
      003A73 24 C7            [12]  757 	add	a,#0xc7
      003A75 FE               [12]  758 	mov	r6,a
      003A76 8F 82            [24]  759 	mov	dpl, r7
      003A78 8E 83            [24]  760 	mov	dph, r6
      003A7A 12 38 CF         [24]  761 	lcall	_write_page
      003A7D E5 82            [12]  762 	mov	a, dpl
      003A7F 70 06            [24]  763 	jnz	00110$
      003A81 75 82 03         [24]  764 	mov	dpl, #0x03
      003A84 02 37 A6         [24]  765 	ljmp	_nvm_fail
      003A87                        766 00110$:
                                    767 ;	keyboards/ajazz/ak820/ak820_nvm.c:84: else if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) nvm_fail(AK820_NVM_FAULT_RECOVERY_CLEANUP);
      003A87 90 EF 40         [24]  768 	mov	dptr,#0xef40
      003A8A 12 36 1F         [24]  769 	lcall	_ak820_flash_erase
      003A8D E5 82            [12]  770 	mov	a, dpl
      003A8F 70 06            [24]  771 	jnz	00119$
      003A91 75 82 04         [24]  772 	mov	dpl, #0x04
                                    773 ;	keyboards/ajazz/ak820/ak820_nvm.c:85: }
      003A94 02 37 A6         [24]  774 	ljmp	_nvm_fail
      003A97                        775 00119$:
      003A97 22               [24]  776 	ret
                                    777 ;------------------------------------------------------------
                                    778 ;Allocation info for local variables in function 'eeprom_driver_init'
                                    779 ;------------------------------------------------------------
                                    780 ;	keyboards/ajazz/ak820/ak820_nvm.c:87: void eeprom_driver_init(void) {
                                    781 ;	-----------------------------------------
                                    782 ;	 function eeprom_driver_init
                                    783 ;	-----------------------------------------
      003A98                        784 _eeprom_driver_init:
                                    785 ;	keyboards/ajazz/ak820/ak820_nvm.c:88: storage_failed = false;
      003A98 90 05 19         [24]  786 	mov	dptr,#_storage_failed
      003A9B E4               [12]  787 	clr	a
      003A9C F0               [24]  788 	movx	@dptr,a
                                    789 ;	keyboards/ajazz/ak820/ak820_nvm.c:89: first_failure_stage = AK820_NVM_FAULT_NONE;
      003A9D 90 05 1B         [24]  790 	mov	dptr,#_first_failure_stage
      003AA0 F0               [24]  791 	movx	@dptr,a
                                    792 ;	keyboards/ajazz/ak820/ak820_nvm.c:90: page_valid = page_dirty = false;
      003AA1 90 05 18         [24]  793 	mov	dptr,#_page_dirty
      003AA4 F0               [24]  794 	movx	@dptr,a
      003AA5 90 05 17         [24]  795 	mov	dptr,#_page_valid
      003AA8 F0               [24]  796 	movx	@dptr,a
                                    797 ;	keyboards/ajazz/ak820/ak820_nvm.c:91: batch_depth = 0;
      003AA9 90 05 1A         [24]  798 	mov	dptr,#_batch_depth
      003AAC F0               [24]  799 	movx	@dptr,a
                                    800 ;	keyboards/ajazz/ak820/ak820_nvm.c:92: recover_journal();
      003AAD 12 39 A0         [24]  801 	lcall	_recover_journal
                                    802 ;	keyboards/ajazz/ak820/ak820_nvm.c:94: ak820_macro_init();
                                    803 ;	keyboards/ajazz/ak820/ak820_nvm.c:96: }
      003AB0 02 2A 70         [24]  804 	ljmp	_ak820_macro_init
                                    805 ;------------------------------------------------------------
                                    806 ;Allocation info for local variables in function 'ak820_nvm_ok'
                                    807 ;------------------------------------------------------------
                                    808 ;	keyboards/ajazz/ak820/ak820_nvm.c:98: bool ak820_nvm_ok(void) { return !storage_failed; }
                                    809 ;	-----------------------------------------
                                    810 ;	 function ak820_nvm_ok
                                    811 ;	-----------------------------------------
      003AB3                        812 _ak820_nvm_ok:
      003AB3 C0 07            [24]  813 	push	ar7
      003AB5 90 05 19         [24]  814 	mov	dptr,#_storage_failed
      003AB8 E0               [24]  815 	movx	a,@dptr
      003AB9 B4 01 00         [24]  816 	cjne	a,#0x01,00103$
      003ABC                        817 00103$:
      003ABC 92 03            [24]  818 	mov  _ak820_nvm_ok_sloc0_1_0,c
      003ABE E4               [12]  819 	clr	a
      003ABF 33               [12]  820 	rlc	a
      003AC0 F5 82            [12]  821 	mov	dpl, a
      003AC2 D0 07            [24]  822 	pop	ar7
      003AC4 22               [24]  823 	ret
                                    824 ;------------------------------------------------------------
                                    825 ;Allocation info for local variables in function 'ak820_nvm_schema_fault'
                                    826 ;------------------------------------------------------------
                                    827 ;	keyboards/ajazz/ak820/ak820_nvm.c:100: void ak820_nvm_schema_fault(void) { nvm_fail(AK820_NVM_FAULT_SCHEMA); }
                                    828 ;	-----------------------------------------
                                    829 ;	 function ak820_nvm_schema_fault
                                    830 ;	-----------------------------------------
      003AC5                        831 _ak820_nvm_schema_fault:
      003AC5 75 82 10         [24]  832 	mov	dpl, #0x10
      003AC8 02 37 A6         [24]  833 	ljmp	_nvm_fail
                                    834 ;------------------------------------------------------------
                                    835 ;Allocation info for local variables in function 'ak820_nvm_flush'
                                    836 ;------------------------------------------------------------
                                    837 ;header        Allocated with name '_ak820_nvm_flush_header_10000_59'
                                    838 ;crc           Allocated with name '_ak820_nvm_flush_crc_10000_59'
                                    839 ;i             Allocated with name '_ak820_nvm_flush_i_10000_59'
                                    840 ;stage         Allocated with name '_ak820_nvm_flush_stage_10000_59'
                                    841 ;------------------------------------------------------------
                                    842 ;	keyboards/ajazz/ak820/ak820_nvm.c:102: void ak820_nvm_flush(void) {
                                    843 ;	-----------------------------------------
                                    844 ;	 function ak820_nvm_flush
                                    845 ;	-----------------------------------------
      003ACB                        846 _ak820_nvm_flush:
                                    847 ;	keyboards/ajazz/ak820/ak820_nvm.c:107: if (!page_dirty || storage_failed) return;
      003ACB 90 05 18         [24]  848 	mov	dptr,#_page_dirty
      003ACE E0               [24]  849 	movx	a,@dptr
      003ACF 60 06            [24]  850 	jz	00101$
      003AD1 90 05 19         [24]  851 	mov	dptr,#_storage_failed
      003AD4 E0               [24]  852 	movx	a,@dptr
      003AD5 60 01            [24]  853 	jz	00102$
      003AD7                        854 00101$:
      003AD7 22               [24]  855 	ret
      003AD8                        856 00102$:
                                    857 ;	keyboards/ajazz/ak820/ak820_nvm.c:108: crc = page_crc();
      003AD8 12 38 8E         [24]  858 	lcall	_page_crc
      003ADB AE 82            [24]  859 	mov	r6, dpl
      003ADD AF 83            [24]  860 	mov	r7, dph
                                    861 ;	keyboards/ajazz/ak820/ak820_nvm.c:109: header[0] = 0xA5u;
      003ADF 90 05 31         [24]  862 	mov	dptr,#_ak820_nvm_flush_header_10000_59
      003AE2 74 A5            [12]  863 	mov	a,#0xa5
      003AE4 F0               [24]  864 	movx	@dptr,a
                                    865 ;	keyboards/ajazz/ak820/ak820_nvm.c:110: header[1] = (uint8_t)cached_page;
      003AE5 90 05 15         [24]  866 	mov	dptr,#_cached_page
      003AE8 E0               [24]  867 	movx	a,@dptr
      003AE9 90 05 32         [24]  868 	mov	dptr,#(_ak820_nvm_flush_header_10000_59 + 0x0001)
      003AEC F0               [24]  869 	movx	@dptr,a
                                    870 ;	keyboards/ajazz/ak820/ak820_nvm.c:111: header[2] = (uint8_t)(cached_page >> 8);
      003AED 90 05 15         [24]  871 	mov	dptr,#_cached_page
      003AF0 E0               [24]  872 	movx	a,@dptr
      003AF1 A3               [24]  873 	inc	dptr
      003AF2 E0               [24]  874 	movx	a,@dptr
      003AF3 90 05 33         [24]  875 	mov	dptr,#(_ak820_nvm_flush_header_10000_59 + 0x0002)
      003AF6 F0               [24]  876 	movx	@dptr,a
                                    877 ;	keyboards/ajazz/ak820/ak820_nvm.c:112: header[3] = (uint8_t)crc;
      003AF7 8E 05            [24]  878 	mov	ar5,r6
      003AF9 90 05 34         [24]  879 	mov	dptr,#(_ak820_nvm_flush_header_10000_59 + 0x0003)
      003AFC ED               [12]  880 	mov	a,r5
      003AFD F0               [24]  881 	movx	@dptr,a
                                    882 ;	keyboards/ajazz/ak820/ak820_nvm.c:113: header[4] = (uint8_t)(crc >> 8);
      003AFE 8F 06            [24]  883 	mov	ar6,r7
      003B00 90 05 35         [24]  884 	mov	dptr,#(_ak820_nvm_flush_header_10000_59 + 0x0004)
      003B03 EE               [12]  885 	mov	a,r6
      003B04 F0               [24]  886 	movx	@dptr,a
                                    887 ;	keyboards/ajazz/ak820/ak820_nvm.c:114: for (i = 1; i != 5; ++i) header[i + 4] = (uint8_t)~header[i];
      003B05 7F 01            [12]  888 	mov	r7,#0x01
      003B07                        889 00128$:
      003B07 8F 06            [24]  890 	mov	ar6,r7
      003B09 EE               [12]  891 	mov	a,r6
      003B0A 24 04            [12]  892 	add	a,#0x04
      003B0C FE               [12]  893 	mov	r6,a
      003B0D 33               [12]  894 	rlc	a
      003B0E 95 E0            [12]  895 	subb	a,acc
      003B10 FD               [12]  896 	mov	r5,a
      003B11 EE               [12]  897 	mov	a,r6
      003B12 24 31            [12]  898 	add	a, #_ak820_nvm_flush_header_10000_59
      003B14 FE               [12]  899 	mov	r6,a
      003B15 ED               [12]  900 	mov	a,r5
      003B16 34 05            [12]  901 	addc	a, #(_ak820_nvm_flush_header_10000_59 >> 8)
      003B18 FD               [12]  902 	mov	r5,a
      003B19 EF               [12]  903 	mov	a,r7
      003B1A 24 31            [12]  904 	add	a, #_ak820_nvm_flush_header_10000_59
      003B1C F5 82            [12]  905 	mov	dpl,a
      003B1E E4               [12]  906 	clr	a
      003B1F 34 05            [12]  907 	addc	a, #(_ak820_nvm_flush_header_10000_59 >> 8)
      003B21 F5 83            [12]  908 	mov	dph,a
      003B23 E0               [24]  909 	movx	a,@dptr
      003B24 FC               [12]  910 	mov	r4,a
      003B25 63 04 FF         [24]  911 	xrl	ar4,#0xff
      003B28 8E 82            [24]  912 	mov	dpl,r6
      003B2A 8D 83            [24]  913 	mov	dph,r5
      003B2C EC               [12]  914 	mov	a,r4
      003B2D F0               [24]  915 	movx	@dptr,a
      003B2E 0F               [12]  916 	inc	r7
      003B2F BF 05 D5         [24]  917 	cjne	r7,#0x05,00128$
                                    918 ;	keyboards/ajazz/ak820/ak820_nvm.c:117: stage = AK820_NVM_FAULT_HEADER_ERASE;
      003B32 90 05 3A         [24]  919 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003B35 74 05            [12]  920 	mov	a,#0x05
      003B37 F0               [24]  921 	movx	@dptr,a
                                    922 ;	keyboards/ajazz/ak820/ak820_nvm.c:118: if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) goto failed;
      003B38 90 EF 40         [24]  923 	mov	dptr,#0xef40
      003B3B 12 36 1F         [24]  924 	lcall	_ak820_flash_erase
      003B3E E5 82            [12]  925 	mov	a, dpl
      003B40 70 03            [24]  926 	jnz	00269$
      003B42 02 3C 5B         [24]  927 	ljmp	00127$
      003B45                        928 00269$:
                                    929 ;	keyboards/ajazz/ak820/ak820_nvm.c:119: stage = AK820_NVM_FAULT_HEADER_ZERO;
      003B45 90 05 3A         [24]  930 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003B48 74 06            [12]  931 	mov	a,#0x06
      003B4A F0               [24]  932 	movx	@dptr,a
                                    933 ;	keyboards/ajazz/ak820/ak820_nvm.c:120: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003B4B 7F 00            [12]  934 	mov	r7,#0x00
      003B4D                        935 00130$:
                                    936 ;	keyboards/ajazz/ak820/ak820_nvm.c:121: if (ak820_flash_read(AK820_JOURNAL_HEADER + i)) goto failed;
      003B4D 8F 06            [24]  937 	mov	ar6,r7
      003B4F 7D 00            [12]  938 	mov	r5,#0x00
      003B51 74 40            [12]  939 	mov	a,#0x40
      003B53 2E               [12]  940 	add	a, r6
      003B54 FE               [12]  941 	mov	r6,a
      003B55 74 EF            [12]  942 	mov	a,#0xef
      003B57 3D               [12]  943 	addc	a, r5
      003B58 FD               [12]  944 	mov	r5,a
      003B59 8E 82            [24]  945 	mov	dpl, r6
      003B5B 8D 83            [24]  946 	mov	dph, r5
      003B5D 12 35 12         [24]  947 	lcall	_ak820_flash_read
      003B60 E5 82            [12]  948 	mov	a, dpl
      003B62 60 03            [24]  949 	jz	00270$
      003B64 02 3C 5B         [24]  950 	ljmp	00127$
      003B67                        951 00270$:
                                    952 ;	keyboards/ajazz/ak820/ak820_nvm.c:120: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003B67 0F               [12]  953 	inc	r7
      003B68 BF 40 E2         [24]  954 	cjne	r7,#0x40,00130$
                                    955 ;	keyboards/ajazz/ak820/ak820_nvm.c:123: stage = AK820_NVM_FAULT_JOURNAL_WRITE;
      003B6B 90 05 3A         [24]  956 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003B6E 74 07            [12]  957 	mov	a,#0x07
      003B70 F0               [24]  958 	movx	@dptr,a
                                    959 ;	keyboards/ajazz/ak820/ak820_nvm.c:124: if (!write_page(AK820_JOURNAL_DATA)) goto failed;
      003B71 90 EF 00         [24]  960 	mov	dptr,#0xef00
      003B74 12 38 CF         [24]  961 	lcall	_write_page
      003B77 E5 82            [12]  962 	mov	a, dpl
      003B79 70 03            [24]  963 	jnz	00273$
      003B7B 02 3C 5B         [24]  964 	ljmp	00127$
      003B7E                        965 00273$:
                                    966 ;	keyboards/ajazz/ak820/ak820_nvm.c:125: stage = AK820_NVM_FAULT_METADATA_PROGRAM;
      003B7E 90 05 3A         [24]  967 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003B81 74 08            [12]  968 	mov	a,#0x08
      003B83 F0               [24]  969 	movx	@dptr,a
                                    970 ;	keyboards/ajazz/ak820/ak820_nvm.c:126: for (i = 1; i != sizeof(header); ++i) {
      003B84 7F 01            [12]  971 	mov	r7,#0x01
      003B86                        972 00132$:
                                    973 ;	keyboards/ajazz/ak820/ak820_nvm.c:127: if (header[i] && !ak820_flash_program(AK820_JOURNAL_HEADER + i, header[i])) goto failed;
      003B86 EF               [12]  974 	mov	a,r7
      003B87 24 31            [12]  975 	add	a, #_ak820_nvm_flush_header_10000_59
      003B89 F5 82            [12]  976 	mov	dpl,a
      003B8B E4               [12]  977 	clr	a
      003B8C 34 05            [12]  978 	addc	a, #(_ak820_nvm_flush_header_10000_59 >> 8)
      003B8E F5 83            [12]  979 	mov	dph,a
      003B90 E0               [24]  980 	movx	a,@dptr
      003B91 FE               [12]  981 	mov	r6,a
      003B92 60 23            [24]  982 	jz	00133$
      003B94 8F 05            [24]  983 	mov	ar5,r7
      003B96 7C 00            [12]  984 	mov	r4,#0x00
      003B98 74 40            [12]  985 	mov	a,#0x40
      003B9A 2D               [12]  986 	add	a, r5
      003B9B FD               [12]  987 	mov	r5,a
      003B9C 74 EF            [12]  988 	mov	a,#0xef
      003B9E 3C               [12]  989 	addc	a, r4
      003B9F FC               [12]  990 	mov	r4,a
      003BA0 90 04 AD         [24]  991 	mov	dptr,#_ak820_flash_program_PARM_2
      003BA3 EE               [12]  992 	mov	a,r6
      003BA4 F0               [24]  993 	movx	@dptr,a
      003BA5 8D 82            [24]  994 	mov	dpl, r5
      003BA7 8C 83            [24]  995 	mov	dph, r4
      003BA9 C0 07            [24]  996 	push	ar7
      003BAB 12 36 7F         [24]  997 	lcall	_ak820_flash_program
      003BAE E5 82            [12]  998 	mov	a, dpl
      003BB0 D0 07            [24]  999 	pop	ar7
      003BB2 70 03            [24] 1000 	jnz	00275$
      003BB4 02 3C 5B         [24] 1001 	ljmp	00127$
      003BB7                       1002 00275$:
      003BB7                       1003 00133$:
                                   1004 ;	keyboards/ajazz/ak820/ak820_nvm.c:126: for (i = 1; i != sizeof(header); ++i) {
      003BB7 0F               [12] 1005 	inc	r7
      003BB8 BF 09 CB         [24] 1006 	cjne	r7,#0x09,00132$
                                   1007 ;	keyboards/ajazz/ak820/ak820_nvm.c:129: stage = AK820_NVM_FAULT_METADATA_READBACK;
      003BBB 90 05 3A         [24] 1008 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003BBE 74 09            [12] 1009 	mov	a,#0x09
      003BC0 F0               [24] 1010 	movx	@dptr,a
                                   1011 ;	keyboards/ajazz/ak820/ak820_nvm.c:130: for (i = 1; i != sizeof(header); ++i) {
      003BC1 7F 01            [12] 1012 	mov	r7,#0x01
      003BC3                       1013 00134$:
                                   1014 ;	keyboards/ajazz/ak820/ak820_nvm.c:131: if (ak820_flash_read(AK820_JOURNAL_HEADER + i) != header[i]) goto failed;
      003BC3 8F 06            [24] 1015 	mov	ar6,r7
      003BC5 7D 00            [12] 1016 	mov	r5,#0x00
      003BC7 74 40            [12] 1017 	mov	a,#0x40
      003BC9 2E               [12] 1018 	add	a, r6
      003BCA FE               [12] 1019 	mov	r6,a
      003BCB 74 EF            [12] 1020 	mov	a,#0xef
      003BCD 3D               [12] 1021 	addc	a, r5
      003BCE FD               [12] 1022 	mov	r5,a
      003BCF 8E 82            [24] 1023 	mov	dpl, r6
      003BD1 8D 83            [24] 1024 	mov	dph, r5
      003BD3 12 35 12         [24] 1025 	lcall	_ak820_flash_read
      003BD6 AE 82            [24] 1026 	mov	r6, dpl
      003BD8 EF               [12] 1027 	mov	a,r7
      003BD9 24 31            [12] 1028 	add	a, #_ak820_nvm_flush_header_10000_59
      003BDB F5 82            [12] 1029 	mov	dpl,a
      003BDD E4               [12] 1030 	clr	a
      003BDE 34 05            [12] 1031 	addc	a, #(_ak820_nvm_flush_header_10000_59 >> 8)
      003BE0 F5 83            [12] 1032 	mov	dph,a
      003BE2 E0               [24] 1033 	movx	a,@dptr
      003BE3 FD               [12] 1034 	mov	r5,a
      003BE4 EE               [12] 1035 	mov	a,r6
      003BE5 B5 05 73         [24] 1036 	cjne	a,ar5,00127$
                                   1037 ;	keyboards/ajazz/ak820/ak820_nvm.c:130: for (i = 1; i != sizeof(header); ++i) {
      003BE8 0F               [12] 1038 	inc	r7
      003BE9 BF 09 D7         [24] 1039 	cjne	r7,#0x09,00134$
                                   1040 ;	keyboards/ajazz/ak820/ak820_nvm.c:134: stage = AK820_NVM_FAULT_COMMIT_PROGRAM;
      003BEC 90 05 3A         [24] 1041 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003BEF 74 0A            [12] 1042 	mov	a,#0x0a
      003BF1 F0               [24] 1043 	movx	@dptr,a
                                   1044 ;	keyboards/ajazz/ak820/ak820_nvm.c:135: if (!ak820_flash_program(AK820_JOURNAL_HEADER, header[0])) goto failed;
      003BF2 90 05 31         [24] 1045 	mov	dptr,#_ak820_nvm_flush_header_10000_59
      003BF5 E0               [24] 1046 	movx	a,@dptr
      003BF6 90 04 AD         [24] 1047 	mov	dptr,#_ak820_flash_program_PARM_2
      003BF9 F0               [24] 1048 	movx	@dptr,a
      003BFA 90 EF 40         [24] 1049 	mov	dptr,#0xef40
      003BFD 12 36 7F         [24] 1050 	lcall	_ak820_flash_program
      003C00 E5 82            [12] 1051 	mov	a, dpl
      003C02 60 57            [24] 1052 	jz	00127$
                                   1053 ;	keyboards/ajazz/ak820/ak820_nvm.c:136: stage = AK820_NVM_FAULT_COMMIT_READBACK;
      003C04 90 05 3A         [24] 1054 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C07 74 0B            [12] 1055 	mov	a,#0x0b
      003C09 F0               [24] 1056 	movx	@dptr,a
                                   1057 ;	keyboards/ajazz/ak820/ak820_nvm.c:137: if (ak820_flash_read(AK820_JOURNAL_HEADER) != header[0]) goto failed;
      003C0A 90 EF 40         [24] 1058 	mov	dptr,#0xef40
      003C0D 12 35 12         [24] 1059 	lcall	_ak820_flash_read
      003C10 AF 82            [24] 1060 	mov	r7, dpl
      003C12 90 05 31         [24] 1061 	mov	dptr,#_ak820_nvm_flush_header_10000_59
      003C15 E0               [24] 1062 	movx	a,@dptr
      003C16 FE               [12] 1063 	mov	r6,a
      003C17 EF               [12] 1064 	mov	a,r7
      003C18 B5 06 40         [24] 1065 	cjne	a,ar6,00127$
                                   1066 ;	keyboards/ajazz/ak820/ak820_nvm.c:138: stage = AK820_NVM_FAULT_TARGET_WRITE;
      003C1B 90 05 3A         [24] 1067 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C1E 74 0C            [12] 1068 	mov	a,#0x0c
      003C20 F0               [24] 1069 	movx	@dptr,a
                                   1070 ;	keyboards/ajazz/ak820/ak820_nvm.c:139: if (!write_page(AK820_NVM_BASE + cached_page * AK820_FLASH_PAGE)) goto failed;
      003C21 90 05 15         [24] 1071 	mov	dptr,#_cached_page
      003C24 E0               [24] 1072 	movx	a,@dptr
      003C25 FE               [12] 1073 	mov	r6,a
      003C26 A3               [24] 1074 	inc	dptr
      003C27 E0               [24] 1075 	movx	a,@dptr
      003C28 54 03            [12] 1076 	anl	a,#0x03
      003C2A A2 E0            [12] 1077 	mov	c,acc.0
      003C2C CE               [12] 1078 	xch	a,r6
      003C2D 13               [12] 1079 	rrc	a
      003C2E CE               [12] 1080 	xch	a,r6
      003C2F 13               [12] 1081 	rrc	a
      003C30 A2 E0            [12] 1082 	mov	c,acc.0
      003C32 CE               [12] 1083 	xch	a,r6
      003C33 13               [12] 1084 	rrc	a
      003C34 CE               [12] 1085 	xch	a,r6
      003C35 13               [12] 1086 	rrc	a
      003C36 CE               [12] 1087 	xch	a,r6
      003C37 24 C7            [12] 1088 	add	a,#0xc7
      003C39 FF               [12] 1089 	mov	r7,a
      003C3A 8E 82            [24] 1090 	mov	dpl, r6
      003C3C 8F 83            [24] 1091 	mov	dph, r7
      003C3E 12 38 CF         [24] 1092 	lcall	_write_page
      003C41 E5 82            [12] 1093 	mov	a, dpl
      003C43 60 16            [24] 1094 	jz	00127$
                                   1095 ;	keyboards/ajazz/ak820/ak820_nvm.c:140: stage = AK820_NVM_FAULT_CLEANUP;
      003C45 90 05 3A         [24] 1096 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C48 74 0D            [12] 1097 	mov	a,#0x0d
      003C4A F0               [24] 1098 	movx	@dptr,a
                                   1099 ;	keyboards/ajazz/ak820/ak820_nvm.c:141: if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) goto failed;
      003C4B 90 EF 40         [24] 1100 	mov	dptr,#0xef40
      003C4E 12 36 1F         [24] 1101 	lcall	_ak820_flash_erase
      003C51 E5 82            [12] 1102 	mov	a, dpl
      003C53 60 06            [24] 1103 	jz	00127$
                                   1104 ;	keyboards/ajazz/ak820/ak820_nvm.c:142: page_dirty = false;
      003C55 90 05 18         [24] 1105 	mov	dptr,#_page_dirty
      003C58 E4               [12] 1106 	clr	a
      003C59 F0               [24] 1107 	movx	@dptr,a
                                   1108 ;	keyboards/ajazz/ak820/ak820_nvm.c:143: return;
                                   1109 ;	keyboards/ajazz/ak820/ak820_nvm.c:144: failed:
      003C5A 22               [24] 1110 	ret
      003C5B                       1111 00127$:
                                   1112 ;	keyboards/ajazz/ak820/ak820_nvm.c:145: nvm_fail(stage);
      003C5B 90 05 3A         [24] 1113 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C5E E0               [24] 1114 	movx	a,@dptr
      003C5F F5 82            [12] 1115 	mov	dpl,a
                                   1116 ;	keyboards/ajazz/ak820/ak820_nvm.c:146: }
      003C61 02 37 A6         [24] 1117 	ljmp	_nvm_fail
                                   1118 ;------------------------------------------------------------
                                   1119 ;Allocation info for local variables in function 'ak820_nvm_begin'
                                   1120 ;------------------------------------------------------------
                                   1121 ;	keyboards/ajazz/ak820/ak820_nvm.c:148: void ak820_nvm_begin(void) {
                                   1122 ;	-----------------------------------------
                                   1123 ;	 function ak820_nvm_begin
                                   1124 ;	-----------------------------------------
      003C64                       1125 _ak820_nvm_begin:
                                   1126 ;	keyboards/ajazz/ak820/ak820_nvm.c:149: if (batch_depth == 255u) nvm_fail(AK820_NVM_FAULT_BATCH_OVERFLOW);
      003C64 90 05 1A         [24] 1127 	mov	dptr,#_batch_depth
      003C67 E0               [24] 1128 	movx	a,@dptr
      003C68 FF               [12] 1129 	mov	r7,a
      003C69 BF FF 06         [24] 1130 	cjne	r7,#0xff,00102$
      003C6C 75 82 0F         [24] 1131 	mov	dpl, #0x0f
      003C6F 02 37 A6         [24] 1132 	ljmp	_nvm_fail
      003C72                       1133 00102$:
                                   1134 ;	keyboards/ajazz/ak820/ak820_nvm.c:150: else ++batch_depth;
      003C72 90 05 1A         [24] 1135 	mov	dptr,#_batch_depth
      003C75 EF               [12] 1136 	mov	a,r7
      003C76 04               [12] 1137 	inc	a
      003C77 F0               [24] 1138 	movx	@dptr,a
                                   1139 ;	keyboards/ajazz/ak820/ak820_nvm.c:151: }
      003C78 22               [24] 1140 	ret
                                   1141 ;------------------------------------------------------------
                                   1142 ;Allocation info for local variables in function 'ak820_nvm_end'
                                   1143 ;------------------------------------------------------------
                                   1144 ;	keyboards/ajazz/ak820/ak820_nvm.c:153: void ak820_nvm_end(void) {
                                   1145 ;	-----------------------------------------
                                   1146 ;	 function ak820_nvm_end
                                   1147 ;	-----------------------------------------
      003C79                       1148 _ak820_nvm_end:
                                   1149 ;	keyboards/ajazz/ak820/ak820_nvm.c:154: if (batch_depth) --batch_depth;
      003C79 90 05 1A         [24] 1150 	mov	dptr,#_batch_depth
      003C7C E0               [24] 1151 	movx	a,@dptr
      003C7D FF               [12] 1152 	mov	r7,a
      003C7E E0               [24] 1153 	movx	a,@dptr
      003C7F 60 06            [24] 1154 	jz	00102$
      003C81 EF               [12] 1155 	mov	a,r7
      003C82 14               [12] 1156 	dec	a
      003C83 90 05 1A         [24] 1157 	mov	dptr,#_batch_depth
      003C86 F0               [24] 1158 	movx	@dptr,a
      003C87                       1159 00102$:
                                   1160 ;	keyboards/ajazz/ak820/ak820_nvm.c:155: if (!batch_depth) ak820_nvm_flush();
      003C87 90 05 1A         [24] 1161 	mov	dptr,#_batch_depth
      003C8A E0               [24] 1162 	movx	a,@dptr
      003C8B 70 03            [24] 1163 	jnz	00105$
                                   1164 ;	keyboards/ajazz/ak820/ak820_nvm.c:156: }
      003C8D 02 3A CB         [24] 1165 	ljmp	_ak820_nvm_flush
      003C90                       1166 00105$:
      003C90 22               [24] 1167 	ret
                                   1168 ;------------------------------------------------------------
                                   1169 ;Allocation info for local variables in function 'load_page'
                                   1170 ;------------------------------------------------------------
                                   1171 ;page          Allocated with name '_load_page_page_10000_84'
                                   1172 ;i             Allocated with name '_load_page_i_10000_85'
                                   1173 ;------------------------------------------------------------
                                   1174 ;	keyboards/ajazz/ak820/ak820_nvm.c:158: static bool load_page(uint16_t page) {
                                   1175 ;	-----------------------------------------
                                   1176 ;	 function load_page
                                   1177 ;	-----------------------------------------
      003C91                       1178 _load_page:
      003C91 AF 83            [24] 1179 	mov	r7,dph
      003C93 E5 82            [12] 1180 	mov	a,dpl
      003C95 90 05 3B         [24] 1181 	mov	dptr,#_load_page_page_10000_84
      003C98 F0               [24] 1182 	movx	@dptr,a
      003C99 EF               [12] 1183 	mov	a,r7
      003C9A A3               [24] 1184 	inc	dptr
      003C9B F0               [24] 1185 	movx	@dptr,a
                                   1186 ;	keyboards/ajazz/ak820/ak820_nvm.c:160: if (page_valid && cached_page == page) return !storage_failed;
      003C9C 90 05 17         [24] 1187 	mov	dptr,#_page_valid
      003C9F E0               [24] 1188 	movx	a,@dptr
      003CA0 60 26            [24] 1189 	jz	00102$
      003CA2 90 05 15         [24] 1190 	mov	dptr,#_cached_page
      003CA5 E0               [24] 1191 	movx	a,@dptr
      003CA6 FE               [12] 1192 	mov	r6,a
      003CA7 A3               [24] 1193 	inc	dptr
      003CA8 E0               [24] 1194 	movx	a,@dptr
      003CA9 FF               [12] 1195 	mov	r7,a
      003CAA 90 05 3B         [24] 1196 	mov	dptr,#_load_page_page_10000_84
      003CAD E0               [24] 1197 	movx	a,@dptr
      003CAE FC               [12] 1198 	mov	r4,a
      003CAF A3               [24] 1199 	inc	dptr
      003CB0 E0               [24] 1200 	movx	a,@dptr
      003CB1 FD               [12] 1201 	mov	r5,a
      003CB2 EE               [12] 1202 	mov	a,r6
      003CB3 B5 04 12         [24] 1203 	cjne	a,ar4,00102$
      003CB6 EF               [12] 1204 	mov	a,r7
      003CB7 B5 05 0E         [24] 1205 	cjne	a,ar5,00102$
      003CBA 90 05 19         [24] 1206 	mov	dptr,#_storage_failed
      003CBD E0               [24] 1207 	movx	a,@dptr
      003CBE B4 01 00         [24] 1208 	cjne	a,#0x01,00150$
      003CC1                       1209 00150$:
      003CC1 92 04            [24] 1210 	mov  _load_page_sloc0_1_0,c
      003CC3 E4               [12] 1211 	clr	a
      003CC4 33               [12] 1212 	rlc	a
      003CC5 F5 82            [12] 1213 	mov	dpl, a
      003CC7 22               [24] 1214 	ret
      003CC8                       1215 00102$:
                                   1216 ;	keyboards/ajazz/ak820/ak820_nvm.c:161: ak820_nvm_flush();
      003CC8 12 3A CB         [24] 1217 	lcall	_ak820_nvm_flush
                                   1218 ;	keyboards/ajazz/ak820/ak820_nvm.c:162: if (storage_failed) return false;
      003CCB 90 05 19         [24] 1219 	mov	dptr,#_storage_failed
      003CCE E0               [24] 1220 	movx	a,@dptr
      003CCF 60 04            [24] 1221 	jz	00119$
      003CD1 75 82 00         [24] 1222 	mov	dpl, #0x00
                                   1223 ;	keyboards/ajazz/ak820/ak820_nvm.c:163: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003CD4 22               [24] 1224 	ret
      003CD5                       1225 00119$:
      003CD5 90 05 3B         [24] 1226 	mov	dptr,#_load_page_page_10000_84
      003CD8 E0               [24] 1227 	movx	a,@dptr
      003CD9 FE               [12] 1228 	mov	r6,a
      003CDA A3               [24] 1229 	inc	dptr
      003CDB E0               [24] 1230 	movx	a,@dptr
      003CDC FF               [12] 1231 	mov	r7,a
      003CDD 7D 00            [12] 1232 	mov	r5,#0x00
      003CDF                       1233 00107$:
                                   1234 ;	keyboards/ajazz/ak820/ak820_nvm.c:164: page_data[i] = ak820_flash_read(AK820_NVM_BASE + page * AK820_FLASH_PAGE + i);
      003CDF ED               [12] 1235 	mov	a,r5
      003CE0 24 D5            [12] 1236 	add	a, #_page_data
      003CE2 FB               [12] 1237 	mov	r3,a
      003CE3 E4               [12] 1238 	clr	a
      003CE4 34 04            [12] 1239 	addc	a, #(_page_data >> 8)
      003CE6 FC               [12] 1240 	mov	r4,a
      003CE7 8E 01            [24] 1241 	mov	ar1,r6
      003CE9 8F 02            [24] 1242 	mov	ar2,r7
      003CEB EA               [12] 1243 	mov	a,r2
      003CEC 54 03            [12] 1244 	anl	a,#0x03
      003CEE A2 E0            [12] 1245 	mov	c,acc.0
      003CF0 C9               [12] 1246 	xch	a,r1
      003CF1 13               [12] 1247 	rrc	a
      003CF2 C9               [12] 1248 	xch	a,r1
      003CF3 13               [12] 1249 	rrc	a
      003CF4 A2 E0            [12] 1250 	mov	c,acc.0
      003CF6 C9               [12] 1251 	xch	a,r1
      003CF7 13               [12] 1252 	rrc	a
      003CF8 C9               [12] 1253 	xch	a,r1
      003CF9 13               [12] 1254 	rrc	a
      003CFA C9               [12] 1255 	xch	a,r1
      003CFB 24 C7            [12] 1256 	add	a,#0xc7
      003CFD FA               [12] 1257 	mov	r2,a
      003CFE 8D 00            [24] 1258 	mov	ar0,r5
      003D00 C0 06            [24] 1259 	push	ar6
      003D02 C0 07            [24] 1260 	push	ar7
      003D04 7F 00            [12] 1261 	mov	r7,#0x00
      003D06 E8               [12] 1262 	mov	a,r0
      003D07 29               [12] 1263 	add	a, r1
      003D08 F9               [12] 1264 	mov	r1,a
      003D09 EF               [12] 1265 	mov	a,r7
      003D0A 3A               [12] 1266 	addc	a, r2
      003D0B FA               [12] 1267 	mov	r2,a
      003D0C 89 82            [24] 1268 	mov	dpl, r1
      003D0E 8A 83            [24] 1269 	mov	dph, r2
      003D10 12 35 12         [24] 1270 	lcall	_ak820_flash_read
      003D13 AF 82            [24] 1271 	mov	r7, dpl
      003D15 8B 82            [24] 1272 	mov	dpl,r3
      003D17 8C 83            [24] 1273 	mov	dph,r4
      003D19 EF               [12] 1274 	mov	a,r7
      003D1A F0               [24] 1275 	movx	@dptr,a
                                   1276 ;	keyboards/ajazz/ak820/ak820_nvm.c:163: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003D1B 0D               [12] 1277 	inc	r5
      003D1C BD 40 02         [24] 1278 	cjne	r5,#0x40,00152$
      003D1F 80 06            [24] 1279 	sjmp	00153$
      003D21                       1280 00152$:
      003D21 D0 07            [24] 1281 	pop	ar7
      003D23 D0 06            [24] 1282 	pop	ar6
      003D25 80 B8            [24] 1283 	sjmp	00107$
      003D27                       1284 00153$:
      003D27 D0 07            [24] 1285 	pop	ar7
      003D29 D0 06            [24] 1286 	pop	ar6
                                   1287 ;	keyboards/ajazz/ak820/ak820_nvm.c:166: cached_page = page;
      003D2B 90 05 15         [24] 1288 	mov	dptr,#_cached_page
      003D2E EE               [12] 1289 	mov	a,r6
      003D2F F0               [24] 1290 	movx	@dptr,a
      003D30 EF               [12] 1291 	mov	a,r7
      003D31 A3               [24] 1292 	inc	dptr
      003D32 F0               [24] 1293 	movx	@dptr,a
                                   1294 ;	keyboards/ajazz/ak820/ak820_nvm.c:167: page_valid = true;
      003D33 90 05 17         [24] 1295 	mov	dptr,#_page_valid
      003D36 74 01            [12] 1296 	mov	a,#0x01
      003D38 F0               [24] 1297 	movx	@dptr,a
                                   1298 ;	keyboards/ajazz/ak820/ak820_nvm.c:168: return true;
      003D39 75 82 01         [24] 1299 	mov	dpl, #0x01
                                   1300 ;	keyboards/ajazz/ak820/ak820_nvm.c:169: }
      003D3C 22               [24] 1301 	ret
                                   1302 ;------------------------------------------------------------
                                   1303 ;Allocation info for local variables in function 'eeprom_read_block'
                                   1304 ;------------------------------------------------------------
                                   1305 ;addr          Allocated with name '_eeprom_read_block_PARM_2'
                                   1306 ;len           Allocated with name '_eeprom_read_block_PARM_3'
                                   1307 ;buf           Allocated with name '_eeprom_read_block_buf_10000_90'
                                   1308 ;offset        Allocated with name '_eeprom_read_block_offset_10000_91'
                                   1309 ;out           Allocated with name '_eeprom_read_block_out_10000_91'
                                   1310 ;------------------------------------------------------------
                                   1311 ;	keyboards/ajazz/ak820/ak820_nvm.c:171: void eeprom_read_block(void *buf, const void *addr, size_t len) {
                                   1312 ;	-----------------------------------------
                                   1313 ;	 function eeprom_read_block
                                   1314 ;	-----------------------------------------
      003D3D                       1315 _eeprom_read_block:
      003D3D AF F0            [24] 1316 	mov	r7,b
      003D3F AE 83            [24] 1317 	mov	r6,dph
      003D41 E5 82            [12] 1318 	mov	a,dpl
      003D43 90 05 42         [24] 1319 	mov	dptr,#_eeprom_read_block_buf_10000_90
      003D46 F0               [24] 1320 	movx	@dptr,a
      003D47 EE               [12] 1321 	mov	a,r6
      003D48 A3               [24] 1322 	inc	dptr
      003D49 F0               [24] 1323 	movx	@dptr,a
      003D4A EF               [12] 1324 	mov	a,r7
      003D4B A3               [24] 1325 	inc	dptr
      003D4C F0               [24] 1326 	movx	@dptr,a
                                   1327 ;	keyboards/ajazz/ak820/ak820_nvm.c:172: uint16_t offset = (uint16_t)(uintptr_t)addr;
      003D4D 90 05 3D         [24] 1328 	mov	dptr,#_eeprom_read_block_PARM_2
      003D50 E0               [24] 1329 	movx	a,@dptr
      003D51 FE               [12] 1330 	mov	r6,a
      003D52 A3               [24] 1331 	inc	dptr
      003D53 E0               [24] 1332 	movx	a,@dptr
      003D54 FF               [12] 1333 	mov	r7,a
                                   1334 ;	keyboards/ajazz/ak820/ak820_nvm.c:173: uint8_t *out = (uint8_t *)buf;
      003D55 90 05 42         [24] 1335 	mov	dptr,#_eeprom_read_block_buf_10000_90
      003D58 E0               [24] 1336 	movx	a,@dptr
      003D59 FB               [12] 1337 	mov	r3,a
      003D5A A3               [24] 1338 	inc	dptr
      003D5B E0               [24] 1339 	movx	a,@dptr
      003D5C FC               [12] 1340 	mov	r4,a
      003D5D A3               [24] 1341 	inc	dptr
      003D5E E0               [24] 1342 	movx	a,@dptr
      003D5F FD               [12] 1343 	mov	r5,a
      003D60 90 05 45         [24] 1344 	mov	dptr,#_eeprom_read_block_out_10000_91
      003D63 EB               [12] 1345 	mov	a,r3
      003D64 F0               [24] 1346 	movx	@dptr,a
      003D65 EC               [12] 1347 	mov	a,r4
      003D66 A3               [24] 1348 	inc	dptr
      003D67 F0               [24] 1349 	movx	@dptr,a
      003D68 ED               [12] 1350 	mov	a,r5
      003D69 A3               [24] 1351 	inc	dptr
      003D6A F0               [24] 1352 	movx	@dptr,a
                                   1353 ;	keyboards/ajazz/ak820/ak820_nvm.c:174: while (len--) {
      003D6B 90 05 40         [24] 1354 	mov	dptr,#_eeprom_read_block_PARM_3
      003D6E E0               [24] 1355 	movx	a,@dptr
      003D6F FC               [12] 1356 	mov	r4,a
      003D70 A3               [24] 1357 	inc	dptr
      003D71 E0               [24] 1358 	movx	a,@dptr
      003D72 FD               [12] 1359 	mov	r5,a
      003D73                       1360 00107$:
      003D73 8C 02            [24] 1361 	mov	ar2,r4
      003D75 8D 03            [24] 1362 	mov	ar3,r5
      003D77 1C               [12] 1363 	dec	r4
      003D78 BC FF 01         [24] 1364 	cjne	r4,#0xff,00148$
      003D7B 1D               [12] 1365 	dec	r5
      003D7C                       1366 00148$:
      003D7C EA               [12] 1367 	mov	a,r2
      003D7D 4B               [12] 1368 	orl	a,r3
      003D7E 70 01            [24] 1369 	jnz	00149$
      003D80 22               [24] 1370 	ret
      003D81                       1371 00149$:
                                   1372 ;	keyboards/ajazz/ak820/ak820_nvm.c:175: if (offset >= AK820_NVM_SIZE) { *out++ = 0; continue; }
      003D81 8E 02            [24] 1373 	mov	ar2,r6
      003D83 8F 03            [24] 1374 	mov	ar3,r7
      003D85 74 D8            [12] 1375 	mov	a,#0x100 - 0x28
      003D87 2B               [12] 1376 	add	a,r3
      003D88 50 2C            [24] 1377 	jnc	00102$
      003D8A C0 04            [24] 1378 	push	ar4
      003D8C C0 05            [24] 1379 	push	ar5
      003D8E 90 05 45         [24] 1380 	mov	dptr,#_eeprom_read_block_out_10000_91
      003D91 E0               [24] 1381 	movx	a,@dptr
      003D92 F8               [12] 1382 	mov	r0,a
      003D93 A3               [24] 1383 	inc	dptr
      003D94 E0               [24] 1384 	movx	a,@dptr
      003D95 F9               [12] 1385 	mov	r1,a
      003D96 A3               [24] 1386 	inc	dptr
      003D97 E0               [24] 1387 	movx	a,@dptr
      003D98 FD               [12] 1388 	mov	r5,a
      003D99 88 82            [24] 1389 	mov	dpl,r0
      003D9B 89 83            [24] 1390 	mov	dph,r1
      003D9D 8D F0            [24] 1391 	mov	b,r5
      003D9F E4               [12] 1392 	clr	a
      003DA0 12 B5 3D         [24] 1393 	lcall	__gptrput
      003DA3 90 05 45         [24] 1394 	mov	dptr,#_eeprom_read_block_out_10000_91
      003DA6 04               [12] 1395 	inc	a
      003DA7 28               [12] 1396 	add	a, r0
      003DA8 F0               [24] 1397 	movx	@dptr,a
      003DA9 E4               [12] 1398 	clr	a
      003DAA 39               [12] 1399 	addc	a, r1
      003DAB A3               [24] 1400 	inc	dptr
      003DAC F0               [24] 1401 	movx	@dptr,a
      003DAD ED               [12] 1402 	mov	a,r5
      003DAE A3               [24] 1403 	inc	dptr
      003DAF F0               [24] 1404 	movx	@dptr,a
      003DB0 D0 05            [24] 1405 	pop	ar5
      003DB2 D0 04            [24] 1406 	pop	ar4
      003DB4 80 BD            [24] 1407 	sjmp	00107$
      003DB6                       1408 00102$:
                                   1409 ;	keyboards/ajazz/ak820/ak820_nvm.c:176: if (page_valid && (offset / AK820_FLASH_PAGE) == cached_page)
      003DB6 90 05 17         [24] 1410 	mov	dptr,#_page_valid
      003DB9 E0               [24] 1411 	movx	a,@dptr
      003DBA 60 67            [24] 1412 	jz	00104$
      003DBC C0 04            [24] 1413 	push	ar4
      003DBE C0 05            [24] 1414 	push	ar5
      003DC0 8A 00            [24] 1415 	mov	ar0,r2
      003DC2 EB               [12] 1416 	mov	a,r3
      003DC3 A2 E7            [12] 1417 	mov	c,acc.7
      003DC5 C8               [12] 1418 	xch	a,r0
      003DC6 33               [12] 1419 	rlc	a
      003DC7 C8               [12] 1420 	xch	a,r0
      003DC8 33               [12] 1421 	rlc	a
      003DC9 A2 E7            [12] 1422 	mov	c,acc.7
      003DCB C8               [12] 1423 	xch	a,r0
      003DCC 33               [12] 1424 	rlc	a
      003DCD C8               [12] 1425 	xch	a,r0
      003DCE 33               [12] 1426 	rlc	a
      003DCF C8               [12] 1427 	xch	a,r0
      003DD0 54 03            [12] 1428 	anl	a,#0x03
      003DD2 F9               [12] 1429 	mov	r1,a
      003DD3 90 05 15         [24] 1430 	mov	dptr,#_cached_page
      003DD6 E0               [24] 1431 	movx	a,@dptr
      003DD7 FC               [12] 1432 	mov	r4,a
      003DD8 A3               [24] 1433 	inc	dptr
      003DD9 E0               [24] 1434 	movx	a,@dptr
      003DDA FD               [12] 1435 	mov	r5,a
      003DDB E8               [12] 1436 	mov	a,r0
      003DDC B5 04 06         [24] 1437 	cjne	a,ar4,00152$
      003DDF E9               [12] 1438 	mov	a,r1
      003DE0 B5 05 02         [24] 1439 	cjne	a,ar5,00152$
      003DE3 80 06            [24] 1440 	sjmp	00153$
      003DE5                       1441 00152$:
      003DE5 D0 05            [24] 1442 	pop	ar5
      003DE7 D0 04            [24] 1443 	pop	ar4
      003DE9 80 38            [24] 1444 	sjmp	00104$
      003DEB                       1445 00153$:
                                   1446 ;	keyboards/ajazz/ak820/ak820_nvm.c:177: *out++ = page_data[offset % AK820_FLASH_PAGE];
      003DEB 90 05 45         [24] 1447 	mov	dptr,#_eeprom_read_block_out_10000_91
      003DEE E0               [24] 1448 	movx	a,@dptr
      003DEF F8               [12] 1449 	mov	r0,a
      003DF0 A3               [24] 1450 	inc	dptr
      003DF1 E0               [24] 1451 	movx	a,@dptr
      003DF2 F9               [12] 1452 	mov	r1,a
      003DF3 A3               [24] 1453 	inc	dptr
      003DF4 E0               [24] 1454 	movx	a,@dptr
      003DF5 FD               [12] 1455 	mov	r5,a
      003DF6 53 02 3F         [24] 1456 	anl	ar2,#0x3f
      003DF9 7B 00            [12] 1457 	mov	r3,#0x00
      003DFB EA               [12] 1458 	mov	a,r2
      003DFC 24 D5            [12] 1459 	add	a, #_page_data
      003DFE F5 82            [12] 1460 	mov	dpl,a
      003E00 EB               [12] 1461 	mov	a,r3
      003E01 34 04            [12] 1462 	addc	a, #(_page_data >> 8)
      003E03 F5 83            [12] 1463 	mov	dph,a
      003E05 E0               [24] 1464 	movx	a,@dptr
      003E06 88 82            [24] 1465 	mov	dpl,r0
      003E08 89 83            [24] 1466 	mov	dph,r1
      003E0A 8D F0            [24] 1467 	mov	b,r5
      003E0C 12 B5 3D         [24] 1468 	lcall	__gptrput
      003E0F 90 05 45         [24] 1469 	mov	dptr,#_eeprom_read_block_out_10000_91
      003E12 74 01            [12] 1470 	mov	a,#0x01
      003E14 28               [12] 1471 	add	a, r0
      003E15 F0               [24] 1472 	movx	@dptr,a
      003E16 E4               [12] 1473 	clr	a
      003E17 39               [12] 1474 	addc	a, r1
      003E18 A3               [24] 1475 	inc	dptr
      003E19 F0               [24] 1476 	movx	@dptr,a
      003E1A ED               [12] 1477 	mov	a,r5
      003E1B A3               [24] 1478 	inc	dptr
      003E1C F0               [24] 1479 	movx	@dptr,a
      003E1D D0 05            [24] 1480 	pop	ar5
      003E1F D0 04            [24] 1481 	pop	ar4
      003E21 80 3C            [24] 1482 	sjmp	00105$
      003E23                       1483 00104$:
                                   1484 ;	keyboards/ajazz/ak820/ak820_nvm.c:178: else *out++ = ak820_flash_read(AK820_NVM_BASE + offset);
      003E23 C0 04            [24] 1485 	push	ar4
      003E25 C0 05            [24] 1486 	push	ar5
      003E27 90 05 45         [24] 1487 	mov	dptr,#_eeprom_read_block_out_10000_91
      003E2A E0               [24] 1488 	movx	a,@dptr
      003E2B F9               [12] 1489 	mov	r1,a
      003E2C A3               [24] 1490 	inc	dptr
      003E2D E0               [24] 1491 	movx	a,@dptr
      003E2E FA               [12] 1492 	mov	r2,a
      003E2F A3               [24] 1493 	inc	dptr
      003E30 E0               [24] 1494 	movx	a,@dptr
      003E31 FB               [12] 1495 	mov	r3,a
      003E32 8E 00            [24] 1496 	mov	ar0,r6
      003E34 8F 05            [24] 1497 	mov	ar5,r7
      003E36 74 C7            [12] 1498 	mov	a,#0xc7
      003E38 2D               [12] 1499 	add	a, r5
      003E39 FD               [12] 1500 	mov	r5,a
      003E3A 88 82            [24] 1501 	mov	dpl, r0
      003E3C 8D 83            [24] 1502 	mov	dph, r5
      003E3E 12 35 12         [24] 1503 	lcall	_ak820_flash_read
      003E41 AD 82            [24] 1504 	mov	r5, dpl
      003E43 89 82            [24] 1505 	mov	dpl,r1
      003E45 8A 83            [24] 1506 	mov	dph,r2
      003E47 8B F0            [24] 1507 	mov	b,r3
      003E49 ED               [12] 1508 	mov	a,r5
      003E4A 12 B5 3D         [24] 1509 	lcall	__gptrput
      003E4D 90 05 45         [24] 1510 	mov	dptr,#_eeprom_read_block_out_10000_91
      003E50 74 01            [12] 1511 	mov	a,#0x01
      003E52 29               [12] 1512 	add	a, r1
      003E53 F0               [24] 1513 	movx	@dptr,a
      003E54 E4               [12] 1514 	clr	a
      003E55 3A               [12] 1515 	addc	a, r2
      003E56 A3               [24] 1516 	inc	dptr
      003E57 F0               [24] 1517 	movx	@dptr,a
      003E58 EB               [12] 1518 	mov	a,r3
      003E59 A3               [24] 1519 	inc	dptr
      003E5A F0               [24] 1520 	movx	@dptr,a
                                   1521 ;	keyboards/ajazz/ak820/ak820_nvm.c:179: ++offset;
      003E5B D0 05            [24] 1522 	pop	ar5
      003E5D D0 04            [24] 1523 	pop	ar4
                                   1524 ;	keyboards/ajazz/ak820/ak820_nvm.c:178: else *out++ = ak820_flash_read(AK820_NVM_BASE + offset);
      003E5F                       1525 00105$:
                                   1526 ;	keyboards/ajazz/ak820/ak820_nvm.c:179: ++offset;
      003E5F 0E               [12] 1527 	inc	r6
      003E60 BE 00 01         [24] 1528 	cjne	r6,#0x00,00154$
      003E63 0F               [12] 1529 	inc	r7
      003E64                       1530 00154$:
                                   1531 ;	keyboards/ajazz/ak820/ak820_nvm.c:181: }
      003E64 02 3D 73         [24] 1532 	ljmp	00107$
                                   1533 ;------------------------------------------------------------
                                   1534 ;Allocation info for local variables in function 'eeprom_write_block'
                                   1535 ;------------------------------------------------------------
                                   1536 ;sloc0         Allocated with name '_eeprom_write_block_sloc0_1_0'
                                   1537 ;addr          Allocated with name '_eeprom_write_block_PARM_2'
                                   1538 ;len           Allocated with name '_eeprom_write_block_PARM_3'
                                   1539 ;buf           Allocated with name '_eeprom_write_block_buf_10000_96'
                                   1540 ;offset        Allocated with name '_eeprom_write_block_offset_10000_97'
                                   1541 ;in            Allocated with name '_eeprom_write_block_in_10000_97'
                                   1542 ;value         Allocated with name '_eeprom_write_block_value_20000_100'
                                   1543 ;------------------------------------------------------------
                                   1544 ;	keyboards/ajazz/ak820/ak820_nvm.c:183: void eeprom_write_block(const void *buf, void *addr, size_t len) {
                                   1545 ;	-----------------------------------------
                                   1546 ;	 function eeprom_write_block
                                   1547 ;	-----------------------------------------
      003E67                       1548 _eeprom_write_block:
      003E67 AF F0            [24] 1549 	mov	r7,b
      003E69 AE 83            [24] 1550 	mov	r6,dph
      003E6B E5 82            [12] 1551 	mov	a,dpl
      003E6D 90 05 4D         [24] 1552 	mov	dptr,#_eeprom_write_block_buf_10000_96
      003E70 F0               [24] 1553 	movx	@dptr,a
      003E71 EE               [12] 1554 	mov	a,r6
      003E72 A3               [24] 1555 	inc	dptr
      003E73 F0               [24] 1556 	movx	@dptr,a
      003E74 EF               [12] 1557 	mov	a,r7
      003E75 A3               [24] 1558 	inc	dptr
      003E76 F0               [24] 1559 	movx	@dptr,a
                                   1560 ;	keyboards/ajazz/ak820/ak820_nvm.c:184: uint16_t offset = (uint16_t)(uintptr_t)addr;
      003E77 90 05 48         [24] 1561 	mov	dptr,#_eeprom_write_block_PARM_2
      003E7A E0               [24] 1562 	movx	a,@dptr
      003E7B FE               [12] 1563 	mov	r6,a
      003E7C A3               [24] 1564 	inc	dptr
      003E7D E0               [24] 1565 	movx	a,@dptr
      003E7E FF               [12] 1566 	mov	r7,a
                                   1567 ;	keyboards/ajazz/ak820/ak820_nvm.c:185: const uint8_t *in = (const uint8_t *)buf;
      003E7F 90 05 4D         [24] 1568 	mov	dptr,#_eeprom_write_block_buf_10000_96
      003E82 E0               [24] 1569 	movx	a,@dptr
      003E83 FB               [12] 1570 	mov	r3,a
      003E84 A3               [24] 1571 	inc	dptr
      003E85 E0               [24] 1572 	movx	a,@dptr
      003E86 FC               [12] 1573 	mov	r4,a
      003E87 A3               [24] 1574 	inc	dptr
      003E88 E0               [24] 1575 	movx	a,@dptr
      003E89 FD               [12] 1576 	mov	r5,a
                                   1577 ;	keyboards/ajazz/ak820/ak820_nvm.c:187: if (offset > AK820_NVM_SIZE || len > AK820_NVM_SIZE - offset) {
      003E8A 8E 01            [24] 1578 	mov	ar1,r6
      003E8C 8F 02            [24] 1579 	mov	ar2,r7
      003E8E C3               [12] 1580 	clr	c
      003E8F E4               [12] 1581 	clr	a
      003E90 99               [12] 1582 	subb	a,r1
      003E91 74 28            [12] 1583 	mov	a,#0x28
      003E93 9A               [12] 1584 	subb	a,r2
      003E94 40 23            [24] 1585 	jc	00101$
                                   1586 ;	free result
      003E96 C0 03            [24] 1587 	push	ar3
      003E98 C0 04            [24] 1588 	push	ar4
      003E9A C0 05            [24] 1589 	push	ar5
      003E9C E4               [12] 1590 	clr	a
      003E9D C3               [12] 1591 	clr	c
      003E9E 9E               [12] 1592 	subb	a,r6
      003E9F F9               [12] 1593 	mov	r1,a
      003EA0 74 28            [12] 1594 	mov	a,#0x28
      003EA2 9F               [12] 1595 	subb	a,r7
      003EA3 FA               [12] 1596 	mov	r2,a
      003EA4 90 05 4B         [24] 1597 	mov	dptr,#_eeprom_write_block_PARM_3
      003EA7 E0               [24] 1598 	movx	a,@dptr
      003EA8 F8               [12] 1599 	mov	r0,a
      003EA9 A3               [24] 1600 	inc	dptr
      003EAA E0               [24] 1601 	movx	a,@dptr
      003EAB FD               [12] 1602 	mov	r5,a
      003EAC C3               [12] 1603 	clr	c
      003EAD E9               [12] 1604 	mov	a,r1
      003EAE 98               [12] 1605 	subb	a,r0
      003EAF EA               [12] 1606 	mov	a,r2
      003EB0 9D               [12] 1607 	subb	a,r5
      003EB1 D0 05            [24] 1608 	pop	ar5
      003EB3 D0 04            [24] 1609 	pop	ar4
      003EB5 D0 03            [24] 1610 	pop	ar3
      003EB7 50 06            [24] 1611 	jnc	00125$
                                   1612 ;	free result
      003EB9                       1613 00101$:
                                   1614 ;	keyboards/ajazz/ak820/ak820_nvm.c:188: nvm_fail(AK820_NVM_FAULT_WRITE_RANGE);
      003EB9 75 82 0E         [24] 1615 	mov	dpl, #0x0e
                                   1616 ;	keyboards/ajazz/ak820/ak820_nvm.c:189: return;
      003EBC 02 37 A6         [24] 1617 	ljmp	_nvm_fail
                                   1618 ;	keyboards/ajazz/ak820/ak820_nvm.c:191: while (len--) {
      003EBF                       1619 00125$:
      003EBF 8E 0C            [24] 1620 	mov	_eeprom_write_block_sloc0_1_0,r6
      003EC1 8F 0D            [24] 1621 	mov	(_eeprom_write_block_sloc0_1_0 + 1),r7
      003EC3 90 05 4B         [24] 1622 	mov	dptr,#_eeprom_write_block_PARM_3
      003EC6 E0               [24] 1623 	movx	a,@dptr
      003EC7 F9               [12] 1624 	mov	r1,a
      003EC8 A3               [24] 1625 	inc	dptr
      003EC9 E0               [24] 1626 	movx	a,@dptr
      003ECA FA               [12] 1627 	mov	r2,a
      003ECB                       1628 00108$:
      003ECB 89 00            [24] 1629 	mov	ar0,r1
      003ECD 8A 07            [24] 1630 	mov	ar7,r2
      003ECF 19               [12] 1631 	dec	r1
      003ED0 B9 FF 01         [24] 1632 	cjne	r1,#0xff,00159$
      003ED3 1A               [12] 1633 	dec	r2
      003ED4                       1634 00159$:
      003ED4 E8               [12] 1635 	mov	a,r0
      003ED5 4F               [12] 1636 	orl	a,r7
      003ED6 70 03            [24] 1637 	jnz	00160$
      003ED8 02 3F 6F         [24] 1638 	ljmp	00110$
      003EDB                       1639 00160$:
                                   1640 ;	keyboards/ajazz/ak820/ak820_nvm.c:192: uint8_t value = *in++;
      003EDB C0 01            [24] 1641 	push	ar1
      003EDD C0 02            [24] 1642 	push	ar2
      003EDF 8B 82            [24] 1643 	mov	dpl,r3
      003EE1 8C 83            [24] 1644 	mov	dph,r4
      003EE3 8D F0            [24] 1645 	mov	b,r5
      003EE5 12 B5 78         [24] 1646 	lcall	__gptrget
      003EE8 FF               [12] 1647 	mov	r7,a
      003EE9 A3               [24] 1648 	inc	dptr
      003EEA AB 82            [24] 1649 	mov	r3,dpl
      003EEC AC 83            [24] 1650 	mov	r4,dph
                                   1651 ;	keyboards/ajazz/ak820/ak820_nvm.c:193: if (!load_page(offset / AK820_FLASH_PAGE)) return;
      003EEE A8 0C            [24] 1652 	mov	r0,_eeprom_write_block_sloc0_1_0
      003EF0 AE 0D            [24] 1653 	mov	r6,(_eeprom_write_block_sloc0_1_0 + 1)
      003EF2 88 01            [24] 1654 	mov	ar1,r0
      003EF4 EE               [12] 1655 	mov	a,r6
      003EF5 A2 E7            [12] 1656 	mov	c,acc.7
      003EF7 C9               [12] 1657 	xch	a,r1
      003EF8 33               [12] 1658 	rlc	a
      003EF9 C9               [12] 1659 	xch	a,r1
      003EFA 33               [12] 1660 	rlc	a
      003EFB A2 E7            [12] 1661 	mov	c,acc.7
      003EFD C9               [12] 1662 	xch	a,r1
      003EFE 33               [12] 1663 	rlc	a
      003EFF C9               [12] 1664 	xch	a,r1
      003F00 33               [12] 1665 	rlc	a
      003F01 C9               [12] 1666 	xch	a,r1
      003F02 54 03            [12] 1667 	anl	a,#0x03
      003F04 FA               [12] 1668 	mov	r2,a
      003F05 89 82            [24] 1669 	mov	dpl, r1
      003F07 8A 83            [24] 1670 	mov	dph, r2
      003F09 C0 07            [24] 1671 	push	ar7
      003F0B C0 06            [24] 1672 	push	ar6
      003F0D C0 05            [24] 1673 	push	ar5
      003F0F C0 04            [24] 1674 	push	ar4
      003F11 C0 03            [24] 1675 	push	ar3
      003F13 C0 02            [24] 1676 	push	ar2
      003F15 C0 01            [24] 1677 	push	ar1
      003F17 C0 00            [24] 1678 	push	ar0
      003F19 12 3C 91         [24] 1679 	lcall	_load_page
      003F1C E5 82            [12] 1680 	mov	a, dpl
      003F1E D0 00            [24] 1681 	pop	ar0
      003F20 D0 01            [24] 1682 	pop	ar1
      003F22 D0 02            [24] 1683 	pop	ar2
      003F24 D0 03            [24] 1684 	pop	ar3
      003F26 D0 04            [24] 1685 	pop	ar4
      003F28 D0 05            [24] 1686 	pop	ar5
      003F2A D0 06            [24] 1687 	pop	ar6
      003F2C D0 07            [24] 1688 	pop	ar7
      003F2E D0 02            [24] 1689 	pop	ar2
      003F30 D0 01            [24] 1690 	pop	ar1
      003F32 70 01            [24] 1691 	jnz	00105$
      003F34 22               [24] 1692 	ret
      003F35                       1693 00105$:
                                   1694 ;	keyboards/ajazz/ak820/ak820_nvm.c:194: if (page_data[offset % AK820_FLASH_PAGE] != value) {
      003F35 C0 01            [24] 1695 	push	ar1
      003F37 C0 02            [24] 1696 	push	ar2
      003F39 53 00 3F         [24] 1697 	anl	ar0,#0x3f
      003F3C 7E 00            [12] 1698 	mov	r6,#0x00
      003F3E E8               [12] 1699 	mov	a,r0
      003F3F 24 D5            [12] 1700 	add	a, #_page_data
      003F41 F8               [12] 1701 	mov	r0,a
      003F42 EE               [12] 1702 	mov	a,r6
      003F43 34 04            [12] 1703 	addc	a, #(_page_data >> 8)
      003F45 FE               [12] 1704 	mov	r6,a
      003F46 88 82            [24] 1705 	mov	dpl,r0
      003F48 8E 83            [24] 1706 	mov	dph,r6
      003F4A E0               [24] 1707 	movx	a,@dptr
      003F4B B5 07 06         [24] 1708 	cjne	a,ar7,00162$
      003F4E D0 02            [24] 1709 	pop	ar2
      003F50 D0 01            [24] 1710 	pop	ar1
      003F52 80 10            [24] 1711 	sjmp	00107$
      003F54                       1712 00162$:
      003F54 D0 02            [24] 1713 	pop	ar2
      003F56 D0 01            [24] 1714 	pop	ar1
                                   1715 ;	keyboards/ajazz/ak820/ak820_nvm.c:195: page_data[offset % AK820_FLASH_PAGE] = value;
      003F58 88 82            [24] 1716 	mov	dpl,r0
      003F5A 8E 83            [24] 1717 	mov	dph,r6
      003F5C EF               [12] 1718 	mov	a,r7
      003F5D F0               [24] 1719 	movx	@dptr,a
                                   1720 ;	keyboards/ajazz/ak820/ak820_nvm.c:196: page_dirty = true;
      003F5E 90 05 18         [24] 1721 	mov	dptr,#_page_dirty
      003F61 74 01            [12] 1722 	mov	a,#0x01
      003F63 F0               [24] 1723 	movx	@dptr,a
      003F64                       1724 00107$:
                                   1725 ;	keyboards/ajazz/ak820/ak820_nvm.c:198: ++offset;
      003F64 05 0C            [12] 1726 	inc	_eeprom_write_block_sloc0_1_0
      003F66 E4               [12] 1727 	clr	a
      003F67 B5 0C 02         [24] 1728 	cjne	a,_eeprom_write_block_sloc0_1_0,00163$
      003F6A 05 0D            [12] 1729 	inc	(_eeprom_write_block_sloc0_1_0 + 1)
      003F6C                       1730 00163$:
      003F6C 02 3E CB         [24] 1731 	ljmp	00108$
      003F6F                       1732 00110$:
                                   1733 ;	keyboards/ajazz/ak820/ak820_nvm.c:200: if (!batch_depth) ak820_nvm_flush();
      003F6F 90 05 1A         [24] 1734 	mov	dptr,#_batch_depth
      003F72 E0               [24] 1735 	movx	a,@dptr
      003F73 70 03            [24] 1736 	jnz	00113$
                                   1737 ;	keyboards/ajazz/ak820/ak820_nvm.c:201: }
      003F75 02 3A CB         [24] 1738 	ljmp	_ak820_nvm_flush
      003F78                       1739 00113$:
      003F78 22               [24] 1740 	ret
                                   1741 ;------------------------------------------------------------
                                   1742 ;Allocation info for local variables in function 'eeprom_driver_erase'
                                   1743 ;------------------------------------------------------------
                                   1744 ;page          Allocated with name '_eeprom_driver_erase_page_10000_106'
                                   1745 ;i             Allocated with name '_eeprom_driver_erase_i_10000_106'
                                   1746 ;------------------------------------------------------------
                                   1747 ;	keyboards/ajazz/ak820/ak820_nvm.c:203: void eeprom_driver_erase(void) {
                                   1748 ;	-----------------------------------------
                                   1749 ;	 function eeprom_driver_erase
                                   1750 ;	-----------------------------------------
      003F79                       1751 _eeprom_driver_erase:
                                   1752 ;	keyboards/ajazz/ak820/ak820_nvm.c:206: ak820_nvm_flush();
      003F79 12 3A CB         [24] 1753 	lcall	_ak820_nvm_flush
                                   1754 ;	keyboards/ajazz/ak820/ak820_nvm.c:207: for (page = 0; page != AK820_NVM_SIZE / AK820_FLASH_PAGE && !storage_failed; ++page) {
      003F7C 7E 00            [12] 1755 	mov	r6,#0x00
      003F7E 7F 00            [12] 1756 	mov	r7,#0x00
      003F80                       1757 00111$:
      003F80 8E 04            [24] 1758 	mov	ar4,r6
      003F82 8F 05            [24] 1759 	mov	ar5,r7
      003F84 BC A0 04         [24] 1760 	cjne	r4,#0xa0,00165$
      003F87 BD 00 01         [24] 1761 	cjne	r5,#0x00,00165$
      003F8A 22               [24] 1762 	ret
      003F8B                       1763 00165$:
      003F8B 90 05 19         [24] 1764 	mov	dptr,#_storage_failed
      003F8E E0               [24] 1765 	movx	a,@dptr
      003F8F 70 46            [24] 1766 	jnz	00113$
                                   1767 ;	keyboards/ajazz/ak820/ak820_nvm.c:208: if (!load_page(page)) return;
      003F91 8E 82            [24] 1768 	mov	dpl, r6
      003F93 8F 83            [24] 1769 	mov	dph, r7
      003F95 C0 07            [24] 1770 	push	ar7
      003F97 C0 06            [24] 1771 	push	ar6
      003F99 12 3C 91         [24] 1772 	lcall	_load_page
      003F9C E5 82            [12] 1773 	mov	a, dpl
      003F9E D0 06            [24] 1774 	pop	ar6
      003FA0 D0 07            [24] 1775 	pop	ar7
      003FA2 70 01            [24] 1776 	jnz	00126$
                                   1777 ;	keyboards/ajazz/ak820/ak820_nvm.c:209: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003FA4 22               [24] 1778 	ret
      003FA5                       1779 00126$:
      003FA5 7D 00            [12] 1780 	mov	r5,#0x00
      003FA7                       1781 00107$:
                                   1782 ;	keyboards/ajazz/ak820/ak820_nvm.c:210: if (page_data[i]) { page_data[i] = 0; page_dirty = true; }
      003FA7 ED               [12] 1783 	mov	a,r5
      003FA8 24 D5            [12] 1784 	add	a, #_page_data
      003FAA FB               [12] 1785 	mov	r3,a
      003FAB E4               [12] 1786 	clr	a
      003FAC 34 04            [12] 1787 	addc	a, #(_page_data >> 8)
      003FAE FC               [12] 1788 	mov	r4,a
      003FAF 8B 82            [24] 1789 	mov	dpl,r3
      003FB1 8C 83            [24] 1790 	mov	dph,r4
      003FB3 E0               [24] 1791 	movx	a,@dptr
      003FB4 60 0B            [24] 1792 	jz	00108$
      003FB6 8B 82            [24] 1793 	mov	dpl,r3
      003FB8 8C 83            [24] 1794 	mov	dph,r4
      003FBA E4               [12] 1795 	clr	a
      003FBB F0               [24] 1796 	movx	@dptr,a
      003FBC 90 05 18         [24] 1797 	mov	dptr,#_page_dirty
      003FBF 04               [12] 1798 	inc	a
      003FC0 F0               [24] 1799 	movx	@dptr,a
      003FC1                       1800 00108$:
                                   1801 ;	keyboards/ajazz/ak820/ak820_nvm.c:209: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003FC1 0D               [12] 1802 	inc	r5
      003FC2 BD 40 E2         [24] 1803 	cjne	r5,#0x40,00107$
                                   1804 ;	keyboards/ajazz/ak820/ak820_nvm.c:212: ak820_nvm_flush();
      003FC5 C0 07            [24] 1805 	push	ar7
      003FC7 C0 06            [24] 1806 	push	ar6
      003FC9 12 3A CB         [24] 1807 	lcall	_ak820_nvm_flush
      003FCC D0 06            [24] 1808 	pop	ar6
      003FCE D0 07            [24] 1809 	pop	ar7
                                   1810 ;	keyboards/ajazz/ak820/ak820_nvm.c:207: for (page = 0; page != AK820_NVM_SIZE / AK820_FLASH_PAGE && !storage_failed; ++page) {
      003FD0 0E               [12] 1811 	inc	r6
      003FD1 BE 00 AC         [24] 1812 	cjne	r6,#0x00,00111$
      003FD4 0F               [12] 1813 	inc	r7
      003FD5 80 A9            [24] 1814 	sjmp	00111$
      003FD7                       1815 00113$:
                                   1816 ;	keyboards/ajazz/ak820/ak820_nvm.c:214: }
      003FD7 22               [24] 1817 	ret
                                   1818 	.area CSEG    (CODE)
                                   1819 	.area CONST   (CODE)
                                   1820 	.area XINIT   (CODE)
                                   1821 	.area CABS    (ABS,CODE)
