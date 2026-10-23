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
      000526                        106 	.ds 3
      000529                        107 _recover_journal_header_10000_43:
      000529                        108 	.ds 9
      000532                        109 _ak820_nvm_flush_header_10000_59:
      000532                        110 	.ds 9
      00053B                        111 _ak820_nvm_flush_stage_10000_59:
      00053B                        112 	.ds 1
      00053C                        113 _load_page_page_10000_84:
      00053C                        114 	.ds 2
      00053E                        115 _eeprom_read_block_PARM_2:
      00053E                        116 	.ds 3
      000541                        117 _eeprom_read_block_PARM_3:
      000541                        118 	.ds 2
      000543                        119 _eeprom_read_block_buf_10000_90:
      000543                        120 	.ds 3
      000546                        121 _eeprom_read_block_out_10000_91:
      000546                        122 	.ds 3
      000549                        123 _eeprom_write_block_PARM_2:
      000549                        124 	.ds 3
      00054C                        125 _eeprom_write_block_PARM_3:
      00054C                        126 	.ds 2
      00054E                        127 _eeprom_write_block_buf_10000_96:
      00054E                        128 	.ds 3
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
                                    535 ;	keyboards/ajazz/ak820/ak820_nvm.c:58: static bool journal_header_valid(uint8_t *header) {
                                    536 ;	-----------------------------------------
                                    537 ;	 function journal_header_valid
                                    538 ;	-----------------------------------------
      00394B                        539 _journal_header_valid:
      00394B AF F0            [24]  540 	mov	r7,b
      00394D AE 83            [24]  541 	mov	r6,dph
      00394F E5 82            [12]  542 	mov	a,dpl
      003951 90 05 26         [24]  543 	mov	dptr,#_journal_header_valid_header_10000_36
      003954 F0               [24]  544 	movx	@dptr,a
      003955 EE               [12]  545 	mov	a,r6
      003956 A3               [24]  546 	inc	dptr
      003957 F0               [24]  547 	movx	@dptr,a
      003958 EF               [12]  548 	mov	a,r7
      003959 A3               [24]  549 	inc	dptr
      00395A F0               [24]  550 	movx	@dptr,a
                                    551 ;	keyboards/ajazz/ak820/ak820_nvm.c:60: if (header[0] != 0xA5u) return false;
      00395B 90 05 26         [24]  552 	mov	dptr,#_journal_header_valid_header_10000_36
      00395E E0               [24]  553 	movx	a,@dptr
      00395F FD               [12]  554 	mov	r5,a
      003960 A3               [24]  555 	inc	dptr
      003961 E0               [24]  556 	movx	a,@dptr
      003962 FE               [12]  557 	mov	r6,a
      003963 A3               [24]  558 	inc	dptr
      003964 E0               [24]  559 	movx	a,@dptr
      003965 FF               [12]  560 	mov	r7,a
      003966 8D 82            [24]  561 	mov	dpl,r5
      003968 8E 83            [24]  562 	mov	dph,r6
      00396A 8F F0            [24]  563 	mov	b,r7
      00396C 12 B5 97         [24]  564 	lcall	__gptrget
      00396F FC               [12]  565 	mov	r4,a
      003970 BC A5 02         [24]  566 	cjne	r4,#0xa5,00138$
      003973 80 04            [24]  567 	sjmp	00116$
      003975                        568 00138$:
      003975 75 82 00         [24]  569 	mov	dpl, #0x00
                                    570 ;	keyboards/ajazz/ak820/ak820_nvm.c:61: for (i = 1; i != 5; ++i) {
      003978 22               [24]  571 	ret
      003979                        572 00116$:
      003979 7C 01            [12]  573 	mov	r4,#0x01
      00397B                        574 00106$:
                                    575 ;	keyboards/ajazz/ak820/ak820_nvm.c:62: if ((uint8_t)(header[i] ^ header[i + 4]) != 0xFFu) return false;
      00397B EC               [12]  576 	mov	a,r4
      00397C 2D               [12]  577 	add	a, r5
      00397D F9               [12]  578 	mov	r1,a
      00397E E4               [12]  579 	clr	a
      00397F 3E               [12]  580 	addc	a, r6
      003980 FA               [12]  581 	mov	r2,a
      003981 8F 03            [24]  582 	mov	ar3,r7
      003983 89 82            [24]  583 	mov	dpl,r1
      003985 8A 83            [24]  584 	mov	dph,r2
      003987 8B F0            [24]  585 	mov	b,r3
      003989 12 B5 97         [24]  586 	lcall	__gptrget
      00398C F9               [12]  587 	mov	r1,a
      00398D 8C 02            [24]  588 	mov	ar2,r4
      00398F 7B 00            [12]  589 	mov	r3,#0x00
      003991 74 04            [12]  590 	mov	a,#0x04
      003993 2A               [12]  591 	add	a, r2
      003994 FA               [12]  592 	mov	r2,a
      003995 E4               [12]  593 	clr	a
      003996 3B               [12]  594 	addc	a, r3
      003997 FB               [12]  595 	mov	r3,a
      003998 EA               [12]  596 	mov	a,r2
      003999 2D               [12]  597 	add	a, r5
      00399A FA               [12]  598 	mov	r2,a
      00399B EB               [12]  599 	mov	a,r3
      00399C 3E               [12]  600 	addc	a, r6
      00399D F8               [12]  601 	mov	r0,a
      00399E 8F 03            [24]  602 	mov	ar3,r7
      0039A0 8A 82            [24]  603 	mov	dpl,r2
      0039A2 88 83            [24]  604 	mov	dph,r0
      0039A4 8B F0            [24]  605 	mov	b,r3
      0039A6 12 B5 97         [24]  606 	lcall	__gptrget
      0039A9 62 01            [12]  607 	xrl	ar1,a
      0039AB B9 FF 02         [24]  608 	cjne	r1,#0xff,00139$
      0039AE 80 04            [24]  609 	sjmp	00107$
      0039B0                        610 00139$:
      0039B0 75 82 00         [24]  611 	mov	dpl, #0x00
      0039B3 22               [24]  612 	ret
      0039B4                        613 00107$:
                                    614 ;	keyboards/ajazz/ak820/ak820_nvm.c:61: for (i = 1; i != 5; ++i) {
      0039B4 0C               [12]  615 	inc	r4
      0039B5 BC 05 C3         [24]  616 	cjne	r4,#0x05,00106$
                                    617 ;	keyboards/ajazz/ak820/ak820_nvm.c:64: return true;
      0039B8 75 82 01         [24]  618 	mov	dpl, #0x01
                                    619 ;	keyboards/ajazz/ak820/ak820_nvm.c:65: }
      0039BB 22               [24]  620 	ret
                                    621 ;------------------------------------------------------------
                                    622 ;Allocation info for local variables in function 'recover_journal'
                                    623 ;------------------------------------------------------------
                                    624 ;header        Allocated with name '_recover_journal_header_10000_43'
                                    625 ;i             Allocated with name '_recover_journal_i_10000_43'
                                    626 ;page          Allocated with name '_recover_journal_page_10000_43'
                                    627 ;crc           Allocated with name '_recover_journal_crc_10000_43'
                                    628 ;------------------------------------------------------------
                                    629 ;	keyboards/ajazz/ak820/ak820_nvm.c:67: static void recover_journal(void) {
                                    630 ;	-----------------------------------------
                                    631 ;	 function recover_journal
                                    632 ;	-----------------------------------------
      0039BC                        633 _recover_journal:
                                    634 ;	keyboards/ajazz/ak820/ak820_nvm.c:71: for (i = 0; i != sizeof(header); ++i) header[i] = ak820_flash_read(AK820_JOURNAL_HEADER + i);
      0039BC 7F 00            [12]  635 	mov	r7,#0x00
      0039BE                        636 00115$:
      0039BE EF               [12]  637 	mov	a,r7
      0039BF 24 29            [12]  638 	add	a, #_recover_journal_header_10000_43
      0039C1 FD               [12]  639 	mov	r5,a
      0039C2 E4               [12]  640 	clr	a
      0039C3 34 05            [12]  641 	addc	a, #(_recover_journal_header_10000_43 >> 8)
      0039C5 FE               [12]  642 	mov	r6,a
      0039C6 8F 04            [24]  643 	mov	ar4,r7
      0039C8 7B 00            [12]  644 	mov	r3,#0x00
      0039CA 74 40            [12]  645 	mov	a,#0x40
      0039CC 2C               [12]  646 	add	a, r4
      0039CD FC               [12]  647 	mov	r4,a
      0039CE 74 EF            [12]  648 	mov	a,#0xef
      0039D0 3B               [12]  649 	addc	a, r3
      0039D1 FB               [12]  650 	mov	r3,a
      0039D2 8C 82            [24]  651 	mov	dpl, r4
      0039D4 8B 83            [24]  652 	mov	dph, r3
      0039D6 12 35 12         [24]  653 	lcall	_ak820_flash_read
      0039D9 AC 82            [24]  654 	mov	r4, dpl
      0039DB 8D 82            [24]  655 	mov	dpl,r5
      0039DD 8E 83            [24]  656 	mov	dph,r6
      0039DF EC               [12]  657 	mov	a,r4
      0039E0 F0               [24]  658 	movx	@dptr,a
      0039E1 0F               [12]  659 	inc	r7
      0039E2 BF 09 D9         [24]  660 	cjne	r7,#0x09,00115$
                                    661 ;	keyboards/ajazz/ak820/ak820_nvm.c:74: if (!journal_header_valid(header)) return;
      0039E5 90 05 29         [24]  662 	mov	dptr,#_recover_journal_header_10000_43
      0039E8 75 F0 00         [24]  663 	mov	b, #0x00
      0039EB 12 39 4B         [24]  664 	lcall	_journal_header_valid
      0039EE E5 82            [12]  665 	mov	a, dpl
      0039F0 70 01            [24]  666 	jnz	00103$
      0039F2 22               [24]  667 	ret
      0039F3                        668 00103$:
                                    669 ;	keyboards/ajazz/ak820/ak820_nvm.c:75: page = (uint16_t)header[1] | ((uint16_t)header[2] << 8);
      0039F3 90 05 2A         [24]  670 	mov	dptr,#(_recover_journal_header_10000_43 + 0x0001)
      0039F6 E0               [24]  671 	movx	a,@dptr
      0039F7 FF               [12]  672 	mov	r7,a
      0039F8 7E 00            [12]  673 	mov	r6,#0x00
      0039FA 90 05 2B         [24]  674 	mov	dptr,#(_recover_journal_header_10000_43 + 0x0002)
      0039FD E0               [24]  675 	movx	a,@dptr
      0039FE FC               [12]  676 	mov	r4,a
      0039FF E4               [12]  677 	clr	a
      003A00 42 07            [12]  678 	orl	ar7,a
      003A02 EC               [12]  679 	mov	a,r4
      003A03 42 06            [12]  680 	orl	ar6,a
                                    681 ;	keyboards/ajazz/ak820/ak820_nvm.c:76: crc = (uint16_t)header[3] | ((uint16_t)header[4] << 8);
      003A05 90 05 2C         [24]  682 	mov	dptr,#(_recover_journal_header_10000_43 + 0x0003)
      003A08 E0               [24]  683 	movx	a,@dptr
      003A09 FD               [12]  684 	mov	r5,a
      003A0A 7C 00            [12]  685 	mov	r4,#0x00
      003A0C 90 05 2D         [24]  686 	mov	dptr,#(_recover_journal_header_10000_43 + 0x0004)
      003A0F E0               [24]  687 	movx	a,@dptr
      003A10 FA               [12]  688 	mov	r2,a
      003A11 E4               [12]  689 	clr	a
      003A12 42 05            [12]  690 	orl	ar5,a
      003A14 EA               [12]  691 	mov	a,r2
      003A15 42 04            [12]  692 	orl	ar4,a
                                    693 ;	keyboards/ajazz/ak820/ak820_nvm.c:77: if (page >= AK820_NVM_SIZE / AK820_FLASH_PAGE) {
      003A17 C3               [12]  694 	clr	c
      003A18 EF               [12]  695 	mov	a,r7
      003A19 94 A0            [12]  696 	subb	a,#0xa0
      003A1B EE               [12]  697 	mov	a,r6
      003A1C 94 00            [12]  698 	subb	a,#0x00
      003A1E 40 06            [24]  699 	jc	00134$
                                    700 ;	keyboards/ajazz/ak820/ak820_nvm.c:78: nvm_fail(AK820_NVM_FAULT_RECOVERY_PAGE);
      003A20 75 82 01         [24]  701 	mov	dpl, #0x01
                                    702 ;	keyboards/ajazz/ak820/ak820_nvm.c:79: return;
      003A23 02 37 A6         [24]  703 	ljmp	_nvm_fail
                                    704 ;	keyboards/ajazz/ak820/ak820_nvm.c:81: for (i = 0; i != AK820_FLASH_PAGE; ++i) page_data[i] = ak820_flash_read(AK820_JOURNAL_DATA + i);
      003A26                        705 00134$:
      003A26 7B 00            [12]  706 	mov	r3,#0x00
      003A28                        707 00117$:
      003A28 C0 05            [24]  708 	push	ar5
      003A2A C0 04            [24]  709 	push	ar4
      003A2C EB               [12]  710 	mov	a,r3
      003A2D 24 D5            [12]  711 	add	a, #_page_data
      003A2F F9               [12]  712 	mov	r1,a
      003A30 E4               [12]  713 	clr	a
      003A31 34 04            [12]  714 	addc	a, #(_page_data >> 8)
      003A33 FA               [12]  715 	mov	r2,a
      003A34 8B 00            [24]  716 	mov	ar0,r3
      003A36 7D 00            [12]  717 	mov	r5,#0x00
      003A38 74 EF            [12]  718 	mov	a,#0xef
      003A3A 2D               [12]  719 	add	a, r5
      003A3B FD               [12]  720 	mov	r5,a
      003A3C 88 82            [24]  721 	mov	dpl, r0
      003A3E 8D 83            [24]  722 	mov	dph, r5
      003A40 12 35 12         [24]  723 	lcall	_ak820_flash_read
      003A43 AD 82            [24]  724 	mov	r5, dpl
      003A45 89 82            [24]  725 	mov	dpl,r1
      003A47 8A 83            [24]  726 	mov	dph,r2
      003A49 ED               [12]  727 	mov	a,r5
      003A4A F0               [24]  728 	movx	@dptr,a
      003A4B 0B               [12]  729 	inc	r3
      003A4C BB 40 02         [24]  730 	cjne	r3,#0x40,00190$
      003A4F 80 06            [24]  731 	sjmp	00191$
      003A51                        732 00190$:
      003A51 D0 04            [24]  733 	pop	ar4
      003A53 D0 05            [24]  734 	pop	ar5
      003A55 80 D1            [24]  735 	sjmp	00117$
      003A57                        736 00191$:
      003A57 D0 04            [24]  737 	pop	ar4
      003A59 D0 05            [24]  738 	pop	ar5
                                    739 ;	keyboards/ajazz/ak820/ak820_nvm.c:82: if (page_crc() != crc) nvm_fail(AK820_NVM_FAULT_RECOVERY_CRC);
      003A5B C0 07            [24]  740 	push	ar7
      003A5D C0 06            [24]  741 	push	ar6
      003A5F C0 05            [24]  742 	push	ar5
      003A61 C0 04            [24]  743 	push	ar4
      003A63 12 38 8E         [24]  744 	lcall	_page_crc
      003A66 AA 82            [24]  745 	mov	r2, dpl
      003A68 AB 83            [24]  746 	mov	r3, dph
      003A6A D0 04            [24]  747 	pop	ar4
      003A6C D0 05            [24]  748 	pop	ar5
      003A6E D0 06            [24]  749 	pop	ar6
      003A70 D0 07            [24]  750 	pop	ar7
      003A72 EA               [12]  751 	mov	a,r2
      003A73 B5 05 06         [24]  752 	cjne	a,ar5,00192$
      003A76 EB               [12]  753 	mov	a,r3
      003A77 B5 04 02         [24]  754 	cjne	a,ar4,00192$
      003A7A 80 06            [24]  755 	sjmp	00113$
      003A7C                        756 00192$:
      003A7C 75 82 02         [24]  757 	mov	dpl, #0x02
      003A7F 02 37 A6         [24]  758 	ljmp	_nvm_fail
      003A82                        759 00113$:
                                    760 ;	keyboards/ajazz/ak820/ak820_nvm.c:83: else if (!write_page(AK820_NVM_BASE + page * AK820_FLASH_PAGE)) nvm_fail(AK820_NVM_FAULT_RECOVERY_WRITE);
      003A82 EE               [12]  761 	mov	a,r6
      003A83 54 03            [12]  762 	anl	a,#0x03
      003A85 A2 E0            [12]  763 	mov	c,acc.0
      003A87 CF               [12]  764 	xch	a,r7
      003A88 13               [12]  765 	rrc	a
      003A89 CF               [12]  766 	xch	a,r7
      003A8A 13               [12]  767 	rrc	a
      003A8B A2 E0            [12]  768 	mov	c,acc.0
      003A8D CF               [12]  769 	xch	a,r7
      003A8E 13               [12]  770 	rrc	a
      003A8F CF               [12]  771 	xch	a,r7
      003A90 13               [12]  772 	rrc	a
      003A91 CF               [12]  773 	xch	a,r7
      003A92 24 C7            [12]  774 	add	a,#0xc7
      003A94 FE               [12]  775 	mov	r6,a
      003A95 8F 82            [24]  776 	mov	dpl, r7
      003A97 8E 83            [24]  777 	mov	dph, r6
      003A99 12 38 CF         [24]  778 	lcall	_write_page
      003A9C E5 82            [12]  779 	mov	a, dpl
      003A9E 70 06            [24]  780 	jnz	00110$
      003AA0 75 82 03         [24]  781 	mov	dpl, #0x03
      003AA3 02 37 A6         [24]  782 	ljmp	_nvm_fail
      003AA6                        783 00110$:
                                    784 ;	keyboards/ajazz/ak820/ak820_nvm.c:84: else if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) nvm_fail(AK820_NVM_FAULT_RECOVERY_CLEANUP);
      003AA6 90 EF 40         [24]  785 	mov	dptr,#0xef40
      003AA9 12 36 1F         [24]  786 	lcall	_ak820_flash_erase
      003AAC E5 82            [12]  787 	mov	a, dpl
      003AAE 70 06            [24]  788 	jnz	00119$
      003AB0 75 82 04         [24]  789 	mov	dpl, #0x04
                                    790 ;	keyboards/ajazz/ak820/ak820_nvm.c:85: }
      003AB3 02 37 A6         [24]  791 	ljmp	_nvm_fail
      003AB6                        792 00119$:
      003AB6 22               [24]  793 	ret
                                    794 ;------------------------------------------------------------
                                    795 ;Allocation info for local variables in function 'eeprom_driver_init'
                                    796 ;------------------------------------------------------------
                                    797 ;	keyboards/ajazz/ak820/ak820_nvm.c:87: void eeprom_driver_init(void) {
                                    798 ;	-----------------------------------------
                                    799 ;	 function eeprom_driver_init
                                    800 ;	-----------------------------------------
      003AB7                        801 _eeprom_driver_init:
                                    802 ;	keyboards/ajazz/ak820/ak820_nvm.c:88: storage_failed = false;
      003AB7 90 05 19         [24]  803 	mov	dptr,#_storage_failed
      003ABA E4               [12]  804 	clr	a
      003ABB F0               [24]  805 	movx	@dptr,a
                                    806 ;	keyboards/ajazz/ak820/ak820_nvm.c:89: first_failure_stage = AK820_NVM_FAULT_NONE;
      003ABC 90 05 1B         [24]  807 	mov	dptr,#_first_failure_stage
      003ABF F0               [24]  808 	movx	@dptr,a
                                    809 ;	keyboards/ajazz/ak820/ak820_nvm.c:90: page_valid = page_dirty = false;
      003AC0 90 05 18         [24]  810 	mov	dptr,#_page_dirty
      003AC3 F0               [24]  811 	movx	@dptr,a
      003AC4 90 05 17         [24]  812 	mov	dptr,#_page_valid
      003AC7 F0               [24]  813 	movx	@dptr,a
                                    814 ;	keyboards/ajazz/ak820/ak820_nvm.c:91: batch_depth = 0;
      003AC8 90 05 1A         [24]  815 	mov	dptr,#_batch_depth
      003ACB F0               [24]  816 	movx	@dptr,a
                                    817 ;	keyboards/ajazz/ak820/ak820_nvm.c:92: recover_journal();
      003ACC 12 39 BC         [24]  818 	lcall	_recover_journal
                                    819 ;	keyboards/ajazz/ak820/ak820_nvm.c:94: ak820_macro_init();
                                    820 ;	keyboards/ajazz/ak820/ak820_nvm.c:96: }
      003ACF 02 2A 70         [24]  821 	ljmp	_ak820_macro_init
                                    822 ;------------------------------------------------------------
                                    823 ;Allocation info for local variables in function 'ak820_nvm_ok'
                                    824 ;------------------------------------------------------------
                                    825 ;	keyboards/ajazz/ak820/ak820_nvm.c:98: bool ak820_nvm_ok(void) { return !storage_failed; }
                                    826 ;	-----------------------------------------
                                    827 ;	 function ak820_nvm_ok
                                    828 ;	-----------------------------------------
      003AD2                        829 _ak820_nvm_ok:
      003AD2 C0 07            [24]  830 	push	ar7
      003AD4 90 05 19         [24]  831 	mov	dptr,#_storage_failed
      003AD7 E0               [24]  832 	movx	a,@dptr
      003AD8 B4 01 00         [24]  833 	cjne	a,#0x01,00103$
      003ADB                        834 00103$:
      003ADB 92 03            [24]  835 	mov  _ak820_nvm_ok_sloc0_1_0,c
      003ADD E4               [12]  836 	clr	a
      003ADE 33               [12]  837 	rlc	a
      003ADF F5 82            [12]  838 	mov	dpl, a
      003AE1 D0 07            [24]  839 	pop	ar7
      003AE3 22               [24]  840 	ret
                                    841 ;------------------------------------------------------------
                                    842 ;Allocation info for local variables in function 'ak820_nvm_schema_fault'
                                    843 ;------------------------------------------------------------
                                    844 ;	keyboards/ajazz/ak820/ak820_nvm.c:100: void ak820_nvm_schema_fault(void) { nvm_fail(AK820_NVM_FAULT_SCHEMA); }
                                    845 ;	-----------------------------------------
                                    846 ;	 function ak820_nvm_schema_fault
                                    847 ;	-----------------------------------------
      003AE4                        848 _ak820_nvm_schema_fault:
      003AE4 75 82 10         [24]  849 	mov	dpl, #0x10
      003AE7 02 37 A6         [24]  850 	ljmp	_nvm_fail
                                    851 ;------------------------------------------------------------
                                    852 ;Allocation info for local variables in function 'ak820_nvm_flush'
                                    853 ;------------------------------------------------------------
                                    854 ;header        Allocated with name '_ak820_nvm_flush_header_10000_59'
                                    855 ;crc           Allocated with name '_ak820_nvm_flush_crc_10000_59'
                                    856 ;i             Allocated with name '_ak820_nvm_flush_i_10000_59'
                                    857 ;stage         Allocated with name '_ak820_nvm_flush_stage_10000_59'
                                    858 ;------------------------------------------------------------
                                    859 ;	keyboards/ajazz/ak820/ak820_nvm.c:102: void ak820_nvm_flush(void) {
                                    860 ;	-----------------------------------------
                                    861 ;	 function ak820_nvm_flush
                                    862 ;	-----------------------------------------
      003AEA                        863 _ak820_nvm_flush:
                                    864 ;	keyboards/ajazz/ak820/ak820_nvm.c:107: if (!page_dirty || storage_failed) return;
      003AEA 90 05 18         [24]  865 	mov	dptr,#_page_dirty
      003AED E0               [24]  866 	movx	a,@dptr
      003AEE 60 06            [24]  867 	jz	00101$
      003AF0 90 05 19         [24]  868 	mov	dptr,#_storage_failed
      003AF3 E0               [24]  869 	movx	a,@dptr
      003AF4 60 01            [24]  870 	jz	00102$
      003AF6                        871 00101$:
      003AF6 22               [24]  872 	ret
      003AF7                        873 00102$:
                                    874 ;	keyboards/ajazz/ak820/ak820_nvm.c:108: crc = page_crc();
      003AF7 12 38 8E         [24]  875 	lcall	_page_crc
      003AFA AE 82            [24]  876 	mov	r6, dpl
      003AFC AF 83            [24]  877 	mov	r7, dph
                                    878 ;	keyboards/ajazz/ak820/ak820_nvm.c:109: header[0] = 0xA5u;
      003AFE 90 05 32         [24]  879 	mov	dptr,#_ak820_nvm_flush_header_10000_59
      003B01 74 A5            [12]  880 	mov	a,#0xa5
      003B03 F0               [24]  881 	movx	@dptr,a
                                    882 ;	keyboards/ajazz/ak820/ak820_nvm.c:110: header[1] = (uint8_t)cached_page;
      003B04 90 05 15         [24]  883 	mov	dptr,#_cached_page
      003B07 E0               [24]  884 	movx	a,@dptr
      003B08 90 05 33         [24]  885 	mov	dptr,#(_ak820_nvm_flush_header_10000_59 + 0x0001)
      003B0B F0               [24]  886 	movx	@dptr,a
                                    887 ;	keyboards/ajazz/ak820/ak820_nvm.c:111: header[2] = (uint8_t)(cached_page >> 8);
      003B0C 90 05 15         [24]  888 	mov	dptr,#_cached_page
      003B0F E0               [24]  889 	movx	a,@dptr
      003B10 A3               [24]  890 	inc	dptr
      003B11 E0               [24]  891 	movx	a,@dptr
      003B12 90 05 34         [24]  892 	mov	dptr,#(_ak820_nvm_flush_header_10000_59 + 0x0002)
      003B15 F0               [24]  893 	movx	@dptr,a
                                    894 ;	keyboards/ajazz/ak820/ak820_nvm.c:112: header[3] = (uint8_t)crc;
      003B16 8E 05            [24]  895 	mov	ar5,r6
      003B18 90 05 35         [24]  896 	mov	dptr,#(_ak820_nvm_flush_header_10000_59 + 0x0003)
      003B1B ED               [12]  897 	mov	a,r5
      003B1C F0               [24]  898 	movx	@dptr,a
                                    899 ;	keyboards/ajazz/ak820/ak820_nvm.c:113: header[4] = (uint8_t)(crc >> 8);
      003B1D 8F 06            [24]  900 	mov	ar6,r7
      003B1F 90 05 36         [24]  901 	mov	dptr,#(_ak820_nvm_flush_header_10000_59 + 0x0004)
      003B22 EE               [12]  902 	mov	a,r6
      003B23 F0               [24]  903 	movx	@dptr,a
                                    904 ;	keyboards/ajazz/ak820/ak820_nvm.c:114: for (i = 1; i != 5; ++i) header[i + 4] = (uint8_t)~header[i];
      003B24 7F 01            [12]  905 	mov	r7,#0x01
      003B26                        906 00128$:
      003B26 8F 06            [24]  907 	mov	ar6,r7
      003B28 EE               [12]  908 	mov	a,r6
      003B29 24 04            [12]  909 	add	a,#0x04
      003B2B FE               [12]  910 	mov	r6,a
      003B2C 33               [12]  911 	rlc	a
      003B2D 95 E0            [12]  912 	subb	a,acc
      003B2F FD               [12]  913 	mov	r5,a
      003B30 EE               [12]  914 	mov	a,r6
      003B31 24 32            [12]  915 	add	a, #_ak820_nvm_flush_header_10000_59
      003B33 FE               [12]  916 	mov	r6,a
      003B34 ED               [12]  917 	mov	a,r5
      003B35 34 05            [12]  918 	addc	a, #(_ak820_nvm_flush_header_10000_59 >> 8)
      003B37 FD               [12]  919 	mov	r5,a
      003B38 EF               [12]  920 	mov	a,r7
      003B39 24 32            [12]  921 	add	a, #_ak820_nvm_flush_header_10000_59
      003B3B F5 82            [12]  922 	mov	dpl,a
      003B3D E4               [12]  923 	clr	a
      003B3E 34 05            [12]  924 	addc	a, #(_ak820_nvm_flush_header_10000_59 >> 8)
      003B40 F5 83            [12]  925 	mov	dph,a
      003B42 E0               [24]  926 	movx	a,@dptr
      003B43 FC               [12]  927 	mov	r4,a
      003B44 63 04 FF         [24]  928 	xrl	ar4,#0xff
      003B47 8E 82            [24]  929 	mov	dpl,r6
      003B49 8D 83            [24]  930 	mov	dph,r5
      003B4B EC               [12]  931 	mov	a,r4
      003B4C F0               [24]  932 	movx	@dptr,a
      003B4D 0F               [12]  933 	inc	r7
      003B4E BF 05 D5         [24]  934 	cjne	r7,#0x05,00128$
                                    935 ;	keyboards/ajazz/ak820/ak820_nvm.c:117: stage = AK820_NVM_FAULT_HEADER_ERASE;
      003B51 90 05 3B         [24]  936 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003B54 74 05            [12]  937 	mov	a,#0x05
      003B56 F0               [24]  938 	movx	@dptr,a
                                    939 ;	keyboards/ajazz/ak820/ak820_nvm.c:118: if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) goto failed;
      003B57 90 EF 40         [24]  940 	mov	dptr,#0xef40
      003B5A 12 36 1F         [24]  941 	lcall	_ak820_flash_erase
      003B5D E5 82            [12]  942 	mov	a, dpl
      003B5F 70 03            [24]  943 	jnz	00269$
      003B61 02 3C 7A         [24]  944 	ljmp	00127$
      003B64                        945 00269$:
                                    946 ;	keyboards/ajazz/ak820/ak820_nvm.c:119: stage = AK820_NVM_FAULT_HEADER_ZERO;
      003B64 90 05 3B         [24]  947 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003B67 74 06            [12]  948 	mov	a,#0x06
      003B69 F0               [24]  949 	movx	@dptr,a
                                    950 ;	keyboards/ajazz/ak820/ak820_nvm.c:120: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003B6A 7F 00            [12]  951 	mov	r7,#0x00
      003B6C                        952 00130$:
                                    953 ;	keyboards/ajazz/ak820/ak820_nvm.c:121: if (ak820_flash_read(AK820_JOURNAL_HEADER + i)) goto failed;
      003B6C 8F 06            [24]  954 	mov	ar6,r7
      003B6E 7D 00            [12]  955 	mov	r5,#0x00
      003B70 74 40            [12]  956 	mov	a,#0x40
      003B72 2E               [12]  957 	add	a, r6
      003B73 FE               [12]  958 	mov	r6,a
      003B74 74 EF            [12]  959 	mov	a,#0xef
      003B76 3D               [12]  960 	addc	a, r5
      003B77 FD               [12]  961 	mov	r5,a
      003B78 8E 82            [24]  962 	mov	dpl, r6
      003B7A 8D 83            [24]  963 	mov	dph, r5
      003B7C 12 35 12         [24]  964 	lcall	_ak820_flash_read
      003B7F E5 82            [12]  965 	mov	a, dpl
      003B81 60 03            [24]  966 	jz	00270$
      003B83 02 3C 7A         [24]  967 	ljmp	00127$
      003B86                        968 00270$:
                                    969 ;	keyboards/ajazz/ak820/ak820_nvm.c:120: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003B86 0F               [12]  970 	inc	r7
      003B87 BF 40 E2         [24]  971 	cjne	r7,#0x40,00130$
                                    972 ;	keyboards/ajazz/ak820/ak820_nvm.c:123: stage = AK820_NVM_FAULT_JOURNAL_WRITE;
      003B8A 90 05 3B         [24]  973 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003B8D 74 07            [12]  974 	mov	a,#0x07
      003B8F F0               [24]  975 	movx	@dptr,a
                                    976 ;	keyboards/ajazz/ak820/ak820_nvm.c:124: if (!write_page(AK820_JOURNAL_DATA)) goto failed;
      003B90 90 EF 00         [24]  977 	mov	dptr,#0xef00
      003B93 12 38 CF         [24]  978 	lcall	_write_page
      003B96 E5 82            [12]  979 	mov	a, dpl
      003B98 70 03            [24]  980 	jnz	00273$
      003B9A 02 3C 7A         [24]  981 	ljmp	00127$
      003B9D                        982 00273$:
                                    983 ;	keyboards/ajazz/ak820/ak820_nvm.c:125: stage = AK820_NVM_FAULT_METADATA_PROGRAM;
      003B9D 90 05 3B         [24]  984 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003BA0 74 08            [12]  985 	mov	a,#0x08
      003BA2 F0               [24]  986 	movx	@dptr,a
                                    987 ;	keyboards/ajazz/ak820/ak820_nvm.c:126: for (i = 1; i != sizeof(header); ++i) {
      003BA3 7F 01            [12]  988 	mov	r7,#0x01
      003BA5                        989 00132$:
                                    990 ;	keyboards/ajazz/ak820/ak820_nvm.c:127: if (header[i] && !ak820_flash_program(AK820_JOURNAL_HEADER + i, header[i])) goto failed;
      003BA5 EF               [12]  991 	mov	a,r7
      003BA6 24 32            [12]  992 	add	a, #_ak820_nvm_flush_header_10000_59
      003BA8 F5 82            [12]  993 	mov	dpl,a
      003BAA E4               [12]  994 	clr	a
      003BAB 34 05            [12]  995 	addc	a, #(_ak820_nvm_flush_header_10000_59 >> 8)
      003BAD F5 83            [12]  996 	mov	dph,a
      003BAF E0               [24]  997 	movx	a,@dptr
      003BB0 FE               [12]  998 	mov	r6,a
      003BB1 60 23            [24]  999 	jz	00133$
      003BB3 8F 05            [24] 1000 	mov	ar5,r7
      003BB5 7C 00            [12] 1001 	mov	r4,#0x00
      003BB7 74 40            [12] 1002 	mov	a,#0x40
      003BB9 2D               [12] 1003 	add	a, r5
      003BBA FD               [12] 1004 	mov	r5,a
      003BBB 74 EF            [12] 1005 	mov	a,#0xef
      003BBD 3C               [12] 1006 	addc	a, r4
      003BBE FC               [12] 1007 	mov	r4,a
      003BBF 90 04 AD         [24] 1008 	mov	dptr,#_ak820_flash_program_PARM_2
      003BC2 EE               [12] 1009 	mov	a,r6
      003BC3 F0               [24] 1010 	movx	@dptr,a
      003BC4 8D 82            [24] 1011 	mov	dpl, r5
      003BC6 8C 83            [24] 1012 	mov	dph, r4
      003BC8 C0 07            [24] 1013 	push	ar7
      003BCA 12 36 7F         [24] 1014 	lcall	_ak820_flash_program
      003BCD E5 82            [12] 1015 	mov	a, dpl
      003BCF D0 07            [24] 1016 	pop	ar7
      003BD1 70 03            [24] 1017 	jnz	00275$
      003BD3 02 3C 7A         [24] 1018 	ljmp	00127$
      003BD6                       1019 00275$:
      003BD6                       1020 00133$:
                                   1021 ;	keyboards/ajazz/ak820/ak820_nvm.c:126: for (i = 1; i != sizeof(header); ++i) {
      003BD6 0F               [12] 1022 	inc	r7
      003BD7 BF 09 CB         [24] 1023 	cjne	r7,#0x09,00132$
                                   1024 ;	keyboards/ajazz/ak820/ak820_nvm.c:129: stage = AK820_NVM_FAULT_METADATA_READBACK;
      003BDA 90 05 3B         [24] 1025 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003BDD 74 09            [12] 1026 	mov	a,#0x09
      003BDF F0               [24] 1027 	movx	@dptr,a
                                   1028 ;	keyboards/ajazz/ak820/ak820_nvm.c:130: for (i = 1; i != sizeof(header); ++i) {
      003BE0 7F 01            [12] 1029 	mov	r7,#0x01
      003BE2                       1030 00134$:
                                   1031 ;	keyboards/ajazz/ak820/ak820_nvm.c:131: if (ak820_flash_read(AK820_JOURNAL_HEADER + i) != header[i]) goto failed;
      003BE2 8F 06            [24] 1032 	mov	ar6,r7
      003BE4 7D 00            [12] 1033 	mov	r5,#0x00
      003BE6 74 40            [12] 1034 	mov	a,#0x40
      003BE8 2E               [12] 1035 	add	a, r6
      003BE9 FE               [12] 1036 	mov	r6,a
      003BEA 74 EF            [12] 1037 	mov	a,#0xef
      003BEC 3D               [12] 1038 	addc	a, r5
      003BED FD               [12] 1039 	mov	r5,a
      003BEE 8E 82            [24] 1040 	mov	dpl, r6
      003BF0 8D 83            [24] 1041 	mov	dph, r5
      003BF2 12 35 12         [24] 1042 	lcall	_ak820_flash_read
      003BF5 AE 82            [24] 1043 	mov	r6, dpl
      003BF7 EF               [12] 1044 	mov	a,r7
      003BF8 24 32            [12] 1045 	add	a, #_ak820_nvm_flush_header_10000_59
      003BFA F5 82            [12] 1046 	mov	dpl,a
      003BFC E4               [12] 1047 	clr	a
      003BFD 34 05            [12] 1048 	addc	a, #(_ak820_nvm_flush_header_10000_59 >> 8)
      003BFF F5 83            [12] 1049 	mov	dph,a
      003C01 E0               [24] 1050 	movx	a,@dptr
      003C02 FD               [12] 1051 	mov	r5,a
      003C03 EE               [12] 1052 	mov	a,r6
      003C04 B5 05 73         [24] 1053 	cjne	a,ar5,00127$
                                   1054 ;	keyboards/ajazz/ak820/ak820_nvm.c:130: for (i = 1; i != sizeof(header); ++i) {
      003C07 0F               [12] 1055 	inc	r7
      003C08 BF 09 D7         [24] 1056 	cjne	r7,#0x09,00134$
                                   1057 ;	keyboards/ajazz/ak820/ak820_nvm.c:134: stage = AK820_NVM_FAULT_COMMIT_PROGRAM;
      003C0B 90 05 3B         [24] 1058 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C0E 74 0A            [12] 1059 	mov	a,#0x0a
      003C10 F0               [24] 1060 	movx	@dptr,a
                                   1061 ;	keyboards/ajazz/ak820/ak820_nvm.c:135: if (!ak820_flash_program(AK820_JOURNAL_HEADER, header[0])) goto failed;
      003C11 90 05 32         [24] 1062 	mov	dptr,#_ak820_nvm_flush_header_10000_59
      003C14 E0               [24] 1063 	movx	a,@dptr
      003C15 90 04 AD         [24] 1064 	mov	dptr,#_ak820_flash_program_PARM_2
      003C18 F0               [24] 1065 	movx	@dptr,a
      003C19 90 EF 40         [24] 1066 	mov	dptr,#0xef40
      003C1C 12 36 7F         [24] 1067 	lcall	_ak820_flash_program
      003C1F E5 82            [12] 1068 	mov	a, dpl
      003C21 60 57            [24] 1069 	jz	00127$
                                   1070 ;	keyboards/ajazz/ak820/ak820_nvm.c:136: stage = AK820_NVM_FAULT_COMMIT_READBACK;
      003C23 90 05 3B         [24] 1071 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C26 74 0B            [12] 1072 	mov	a,#0x0b
      003C28 F0               [24] 1073 	movx	@dptr,a
                                   1074 ;	keyboards/ajazz/ak820/ak820_nvm.c:137: if (ak820_flash_read(AK820_JOURNAL_HEADER) != header[0]) goto failed;
      003C29 90 EF 40         [24] 1075 	mov	dptr,#0xef40
      003C2C 12 35 12         [24] 1076 	lcall	_ak820_flash_read
      003C2F AF 82            [24] 1077 	mov	r7, dpl
      003C31 90 05 32         [24] 1078 	mov	dptr,#_ak820_nvm_flush_header_10000_59
      003C34 E0               [24] 1079 	movx	a,@dptr
      003C35 FE               [12] 1080 	mov	r6,a
      003C36 EF               [12] 1081 	mov	a,r7
      003C37 B5 06 40         [24] 1082 	cjne	a,ar6,00127$
                                   1083 ;	keyboards/ajazz/ak820/ak820_nvm.c:138: stage = AK820_NVM_FAULT_TARGET_WRITE;
      003C3A 90 05 3B         [24] 1084 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C3D 74 0C            [12] 1085 	mov	a,#0x0c
      003C3F F0               [24] 1086 	movx	@dptr,a
                                   1087 ;	keyboards/ajazz/ak820/ak820_nvm.c:139: if (!write_page(AK820_NVM_BASE + cached_page * AK820_FLASH_PAGE)) goto failed;
      003C40 90 05 15         [24] 1088 	mov	dptr,#_cached_page
      003C43 E0               [24] 1089 	movx	a,@dptr
      003C44 FE               [12] 1090 	mov	r6,a
      003C45 A3               [24] 1091 	inc	dptr
      003C46 E0               [24] 1092 	movx	a,@dptr
      003C47 54 03            [12] 1093 	anl	a,#0x03
      003C49 A2 E0            [12] 1094 	mov	c,acc.0
      003C4B CE               [12] 1095 	xch	a,r6
      003C4C 13               [12] 1096 	rrc	a
      003C4D CE               [12] 1097 	xch	a,r6
      003C4E 13               [12] 1098 	rrc	a
      003C4F A2 E0            [12] 1099 	mov	c,acc.0
      003C51 CE               [12] 1100 	xch	a,r6
      003C52 13               [12] 1101 	rrc	a
      003C53 CE               [12] 1102 	xch	a,r6
      003C54 13               [12] 1103 	rrc	a
      003C55 CE               [12] 1104 	xch	a,r6
      003C56 24 C7            [12] 1105 	add	a,#0xc7
      003C58 FF               [12] 1106 	mov	r7,a
      003C59 8E 82            [24] 1107 	mov	dpl, r6
      003C5B 8F 83            [24] 1108 	mov	dph, r7
      003C5D 12 38 CF         [24] 1109 	lcall	_write_page
      003C60 E5 82            [12] 1110 	mov	a, dpl
      003C62 60 16            [24] 1111 	jz	00127$
                                   1112 ;	keyboards/ajazz/ak820/ak820_nvm.c:140: stage = AK820_NVM_FAULT_CLEANUP;
      003C64 90 05 3B         [24] 1113 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C67 74 0D            [12] 1114 	mov	a,#0x0d
      003C69 F0               [24] 1115 	movx	@dptr,a
                                   1116 ;	keyboards/ajazz/ak820/ak820_nvm.c:141: if (!ak820_flash_erase(AK820_JOURNAL_HEADER)) goto failed;
      003C6A 90 EF 40         [24] 1117 	mov	dptr,#0xef40
      003C6D 12 36 1F         [24] 1118 	lcall	_ak820_flash_erase
      003C70 E5 82            [12] 1119 	mov	a, dpl
      003C72 60 06            [24] 1120 	jz	00127$
                                   1121 ;	keyboards/ajazz/ak820/ak820_nvm.c:142: page_dirty = false;
      003C74 90 05 18         [24] 1122 	mov	dptr,#_page_dirty
      003C77 E4               [12] 1123 	clr	a
      003C78 F0               [24] 1124 	movx	@dptr,a
                                   1125 ;	keyboards/ajazz/ak820/ak820_nvm.c:143: return;
                                   1126 ;	keyboards/ajazz/ak820/ak820_nvm.c:144: failed:
      003C79 22               [24] 1127 	ret
      003C7A                       1128 00127$:
                                   1129 ;	keyboards/ajazz/ak820/ak820_nvm.c:145: nvm_fail(stage);
      003C7A 90 05 3B         [24] 1130 	mov	dptr,#_ak820_nvm_flush_stage_10000_59
      003C7D E0               [24] 1131 	movx	a,@dptr
      003C7E F5 82            [12] 1132 	mov	dpl,a
                                   1133 ;	keyboards/ajazz/ak820/ak820_nvm.c:146: }
      003C80 02 37 A6         [24] 1134 	ljmp	_nvm_fail
                                   1135 ;------------------------------------------------------------
                                   1136 ;Allocation info for local variables in function 'ak820_nvm_begin'
                                   1137 ;------------------------------------------------------------
                                   1138 ;	keyboards/ajazz/ak820/ak820_nvm.c:148: void ak820_nvm_begin(void) {
                                   1139 ;	-----------------------------------------
                                   1140 ;	 function ak820_nvm_begin
                                   1141 ;	-----------------------------------------
      003C83                       1142 _ak820_nvm_begin:
                                   1143 ;	keyboards/ajazz/ak820/ak820_nvm.c:149: if (batch_depth == 255u) nvm_fail(AK820_NVM_FAULT_BATCH_OVERFLOW);
      003C83 90 05 1A         [24] 1144 	mov	dptr,#_batch_depth
      003C86 E0               [24] 1145 	movx	a,@dptr
      003C87 FF               [12] 1146 	mov	r7,a
      003C88 BF FF 06         [24] 1147 	cjne	r7,#0xff,00102$
      003C8B 75 82 0F         [24] 1148 	mov	dpl, #0x0f
      003C8E 02 37 A6         [24] 1149 	ljmp	_nvm_fail
      003C91                       1150 00102$:
                                   1151 ;	keyboards/ajazz/ak820/ak820_nvm.c:150: else ++batch_depth;
      003C91 90 05 1A         [24] 1152 	mov	dptr,#_batch_depth
      003C94 EF               [12] 1153 	mov	a,r7
      003C95 04               [12] 1154 	inc	a
      003C96 F0               [24] 1155 	movx	@dptr,a
                                   1156 ;	keyboards/ajazz/ak820/ak820_nvm.c:151: }
      003C97 22               [24] 1157 	ret
                                   1158 ;------------------------------------------------------------
                                   1159 ;Allocation info for local variables in function 'ak820_nvm_end'
                                   1160 ;------------------------------------------------------------
                                   1161 ;	keyboards/ajazz/ak820/ak820_nvm.c:153: void ak820_nvm_end(void) {
                                   1162 ;	-----------------------------------------
                                   1163 ;	 function ak820_nvm_end
                                   1164 ;	-----------------------------------------
      003C98                       1165 _ak820_nvm_end:
                                   1166 ;	keyboards/ajazz/ak820/ak820_nvm.c:154: if (batch_depth) --batch_depth;
      003C98 90 05 1A         [24] 1167 	mov	dptr,#_batch_depth
      003C9B E0               [24] 1168 	movx	a,@dptr
      003C9C FF               [12] 1169 	mov	r7,a
      003C9D E0               [24] 1170 	movx	a,@dptr
      003C9E 60 06            [24] 1171 	jz	00102$
      003CA0 EF               [12] 1172 	mov	a,r7
      003CA1 14               [12] 1173 	dec	a
      003CA2 90 05 1A         [24] 1174 	mov	dptr,#_batch_depth
      003CA5 F0               [24] 1175 	movx	@dptr,a
      003CA6                       1176 00102$:
                                   1177 ;	keyboards/ajazz/ak820/ak820_nvm.c:155: if (!batch_depth) ak820_nvm_flush();
      003CA6 90 05 1A         [24] 1178 	mov	dptr,#_batch_depth
      003CA9 E0               [24] 1179 	movx	a,@dptr
      003CAA 70 03            [24] 1180 	jnz	00105$
                                   1181 ;	keyboards/ajazz/ak820/ak820_nvm.c:156: }
      003CAC 02 3A EA         [24] 1182 	ljmp	_ak820_nvm_flush
      003CAF                       1183 00105$:
      003CAF 22               [24] 1184 	ret
                                   1185 ;------------------------------------------------------------
                                   1186 ;Allocation info for local variables in function 'load_page'
                                   1187 ;------------------------------------------------------------
                                   1188 ;page          Allocated with name '_load_page_page_10000_84'
                                   1189 ;i             Allocated with name '_load_page_i_10000_85'
                                   1190 ;------------------------------------------------------------
                                   1191 ;	keyboards/ajazz/ak820/ak820_nvm.c:158: static bool load_page(uint16_t page) {
                                   1192 ;	-----------------------------------------
                                   1193 ;	 function load_page
                                   1194 ;	-----------------------------------------
      003CB0                       1195 _load_page:
      003CB0 AF 83            [24] 1196 	mov	r7,dph
      003CB2 E5 82            [12] 1197 	mov	a,dpl
      003CB4 90 05 3C         [24] 1198 	mov	dptr,#_load_page_page_10000_84
      003CB7 F0               [24] 1199 	movx	@dptr,a
      003CB8 EF               [12] 1200 	mov	a,r7
      003CB9 A3               [24] 1201 	inc	dptr
      003CBA F0               [24] 1202 	movx	@dptr,a
                                   1203 ;	keyboards/ajazz/ak820/ak820_nvm.c:160: if (page_valid && cached_page == page) return !storage_failed;
      003CBB 90 05 17         [24] 1204 	mov	dptr,#_page_valid
      003CBE E0               [24] 1205 	movx	a,@dptr
      003CBF 60 26            [24] 1206 	jz	00102$
      003CC1 90 05 15         [24] 1207 	mov	dptr,#_cached_page
      003CC4 E0               [24] 1208 	movx	a,@dptr
      003CC5 FE               [12] 1209 	mov	r6,a
      003CC6 A3               [24] 1210 	inc	dptr
      003CC7 E0               [24] 1211 	movx	a,@dptr
      003CC8 FF               [12] 1212 	mov	r7,a
      003CC9 90 05 3C         [24] 1213 	mov	dptr,#_load_page_page_10000_84
      003CCC E0               [24] 1214 	movx	a,@dptr
      003CCD FC               [12] 1215 	mov	r4,a
      003CCE A3               [24] 1216 	inc	dptr
      003CCF E0               [24] 1217 	movx	a,@dptr
      003CD0 FD               [12] 1218 	mov	r5,a
      003CD1 EE               [12] 1219 	mov	a,r6
      003CD2 B5 04 12         [24] 1220 	cjne	a,ar4,00102$
      003CD5 EF               [12] 1221 	mov	a,r7
      003CD6 B5 05 0E         [24] 1222 	cjne	a,ar5,00102$
      003CD9 90 05 19         [24] 1223 	mov	dptr,#_storage_failed
      003CDC E0               [24] 1224 	movx	a,@dptr
      003CDD B4 01 00         [24] 1225 	cjne	a,#0x01,00150$
      003CE0                       1226 00150$:
      003CE0 92 04            [24] 1227 	mov  _load_page_sloc0_1_0,c
      003CE2 E4               [12] 1228 	clr	a
      003CE3 33               [12] 1229 	rlc	a
      003CE4 F5 82            [12] 1230 	mov	dpl, a
      003CE6 22               [24] 1231 	ret
      003CE7                       1232 00102$:
                                   1233 ;	keyboards/ajazz/ak820/ak820_nvm.c:161: ak820_nvm_flush();
      003CE7 12 3A EA         [24] 1234 	lcall	_ak820_nvm_flush
                                   1235 ;	keyboards/ajazz/ak820/ak820_nvm.c:162: if (storage_failed) return false;
      003CEA 90 05 19         [24] 1236 	mov	dptr,#_storage_failed
      003CED E0               [24] 1237 	movx	a,@dptr
      003CEE 60 04            [24] 1238 	jz	00119$
      003CF0 75 82 00         [24] 1239 	mov	dpl, #0x00
                                   1240 ;	keyboards/ajazz/ak820/ak820_nvm.c:163: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003CF3 22               [24] 1241 	ret
      003CF4                       1242 00119$:
      003CF4 90 05 3C         [24] 1243 	mov	dptr,#_load_page_page_10000_84
      003CF7 E0               [24] 1244 	movx	a,@dptr
      003CF8 FE               [12] 1245 	mov	r6,a
      003CF9 A3               [24] 1246 	inc	dptr
      003CFA E0               [24] 1247 	movx	a,@dptr
      003CFB FF               [12] 1248 	mov	r7,a
      003CFC 7D 00            [12] 1249 	mov	r5,#0x00
      003CFE                       1250 00107$:
                                   1251 ;	keyboards/ajazz/ak820/ak820_nvm.c:164: page_data[i] = ak820_flash_read(AK820_NVM_BASE + page * AK820_FLASH_PAGE + i);
      003CFE ED               [12] 1252 	mov	a,r5
      003CFF 24 D5            [12] 1253 	add	a, #_page_data
      003D01 FB               [12] 1254 	mov	r3,a
      003D02 E4               [12] 1255 	clr	a
      003D03 34 04            [12] 1256 	addc	a, #(_page_data >> 8)
      003D05 FC               [12] 1257 	mov	r4,a
      003D06 8E 01            [24] 1258 	mov	ar1,r6
      003D08 8F 02            [24] 1259 	mov	ar2,r7
      003D0A EA               [12] 1260 	mov	a,r2
      003D0B 54 03            [12] 1261 	anl	a,#0x03
      003D0D A2 E0            [12] 1262 	mov	c,acc.0
      003D0F C9               [12] 1263 	xch	a,r1
      003D10 13               [12] 1264 	rrc	a
      003D11 C9               [12] 1265 	xch	a,r1
      003D12 13               [12] 1266 	rrc	a
      003D13 A2 E0            [12] 1267 	mov	c,acc.0
      003D15 C9               [12] 1268 	xch	a,r1
      003D16 13               [12] 1269 	rrc	a
      003D17 C9               [12] 1270 	xch	a,r1
      003D18 13               [12] 1271 	rrc	a
      003D19 C9               [12] 1272 	xch	a,r1
      003D1A 24 C7            [12] 1273 	add	a,#0xc7
      003D1C FA               [12] 1274 	mov	r2,a
      003D1D 8D 00            [24] 1275 	mov	ar0,r5
      003D1F C0 06            [24] 1276 	push	ar6
      003D21 C0 07            [24] 1277 	push	ar7
      003D23 7F 00            [12] 1278 	mov	r7,#0x00
      003D25 E8               [12] 1279 	mov	a,r0
      003D26 29               [12] 1280 	add	a, r1
      003D27 F9               [12] 1281 	mov	r1,a
      003D28 EF               [12] 1282 	mov	a,r7
      003D29 3A               [12] 1283 	addc	a, r2
      003D2A FA               [12] 1284 	mov	r2,a
      003D2B 89 82            [24] 1285 	mov	dpl, r1
      003D2D 8A 83            [24] 1286 	mov	dph, r2
      003D2F 12 35 12         [24] 1287 	lcall	_ak820_flash_read
      003D32 AF 82            [24] 1288 	mov	r7, dpl
      003D34 8B 82            [24] 1289 	mov	dpl,r3
      003D36 8C 83            [24] 1290 	mov	dph,r4
      003D38 EF               [12] 1291 	mov	a,r7
      003D39 F0               [24] 1292 	movx	@dptr,a
                                   1293 ;	keyboards/ajazz/ak820/ak820_nvm.c:163: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003D3A 0D               [12] 1294 	inc	r5
      003D3B BD 40 02         [24] 1295 	cjne	r5,#0x40,00152$
      003D3E 80 06            [24] 1296 	sjmp	00153$
      003D40                       1297 00152$:
      003D40 D0 07            [24] 1298 	pop	ar7
      003D42 D0 06            [24] 1299 	pop	ar6
      003D44 80 B8            [24] 1300 	sjmp	00107$
      003D46                       1301 00153$:
      003D46 D0 07            [24] 1302 	pop	ar7
      003D48 D0 06            [24] 1303 	pop	ar6
                                   1304 ;	keyboards/ajazz/ak820/ak820_nvm.c:166: cached_page = page;
      003D4A 90 05 15         [24] 1305 	mov	dptr,#_cached_page
      003D4D EE               [12] 1306 	mov	a,r6
      003D4E F0               [24] 1307 	movx	@dptr,a
      003D4F EF               [12] 1308 	mov	a,r7
      003D50 A3               [24] 1309 	inc	dptr
      003D51 F0               [24] 1310 	movx	@dptr,a
                                   1311 ;	keyboards/ajazz/ak820/ak820_nvm.c:167: page_valid = true;
      003D52 90 05 17         [24] 1312 	mov	dptr,#_page_valid
      003D55 74 01            [12] 1313 	mov	a,#0x01
      003D57 F0               [24] 1314 	movx	@dptr,a
                                   1315 ;	keyboards/ajazz/ak820/ak820_nvm.c:168: return true;
      003D58 75 82 01         [24] 1316 	mov	dpl, #0x01
                                   1317 ;	keyboards/ajazz/ak820/ak820_nvm.c:169: }
      003D5B 22               [24] 1318 	ret
                                   1319 ;------------------------------------------------------------
                                   1320 ;Allocation info for local variables in function 'eeprom_read_block'
                                   1321 ;------------------------------------------------------------
                                   1322 ;addr          Allocated with name '_eeprom_read_block_PARM_2'
                                   1323 ;len           Allocated with name '_eeprom_read_block_PARM_3'
                                   1324 ;buf           Allocated with name '_eeprom_read_block_buf_10000_90'
                                   1325 ;offset        Allocated with name '_eeprom_read_block_offset_10000_91'
                                   1326 ;out           Allocated with name '_eeprom_read_block_out_10000_91'
                                   1327 ;------------------------------------------------------------
                                   1328 ;	keyboards/ajazz/ak820/ak820_nvm.c:171: void eeprom_read_block(void *buf, const void *addr, size_t len) {
                                   1329 ;	-----------------------------------------
                                   1330 ;	 function eeprom_read_block
                                   1331 ;	-----------------------------------------
      003D5C                       1332 _eeprom_read_block:
      003D5C AF F0            [24] 1333 	mov	r7,b
      003D5E AE 83            [24] 1334 	mov	r6,dph
      003D60 E5 82            [12] 1335 	mov	a,dpl
      003D62 90 05 43         [24] 1336 	mov	dptr,#_eeprom_read_block_buf_10000_90
      003D65 F0               [24] 1337 	movx	@dptr,a
      003D66 EE               [12] 1338 	mov	a,r6
      003D67 A3               [24] 1339 	inc	dptr
      003D68 F0               [24] 1340 	movx	@dptr,a
      003D69 EF               [12] 1341 	mov	a,r7
      003D6A A3               [24] 1342 	inc	dptr
      003D6B F0               [24] 1343 	movx	@dptr,a
                                   1344 ;	keyboards/ajazz/ak820/ak820_nvm.c:172: uint16_t offset = (uint16_t)(uintptr_t)addr;
      003D6C 90 05 3E         [24] 1345 	mov	dptr,#_eeprom_read_block_PARM_2
      003D6F E0               [24] 1346 	movx	a,@dptr
      003D70 FE               [12] 1347 	mov	r6,a
      003D71 A3               [24] 1348 	inc	dptr
      003D72 E0               [24] 1349 	movx	a,@dptr
      003D73 FF               [12] 1350 	mov	r7,a
                                   1351 ;	keyboards/ajazz/ak820/ak820_nvm.c:173: uint8_t *out = (uint8_t *)buf;
      003D74 90 05 43         [24] 1352 	mov	dptr,#_eeprom_read_block_buf_10000_90
      003D77 E0               [24] 1353 	movx	a,@dptr
      003D78 FB               [12] 1354 	mov	r3,a
      003D79 A3               [24] 1355 	inc	dptr
      003D7A E0               [24] 1356 	movx	a,@dptr
      003D7B FC               [12] 1357 	mov	r4,a
      003D7C A3               [24] 1358 	inc	dptr
      003D7D E0               [24] 1359 	movx	a,@dptr
      003D7E FD               [12] 1360 	mov	r5,a
      003D7F 90 05 46         [24] 1361 	mov	dptr,#_eeprom_read_block_out_10000_91
      003D82 EB               [12] 1362 	mov	a,r3
      003D83 F0               [24] 1363 	movx	@dptr,a
      003D84 EC               [12] 1364 	mov	a,r4
      003D85 A3               [24] 1365 	inc	dptr
      003D86 F0               [24] 1366 	movx	@dptr,a
      003D87 ED               [12] 1367 	mov	a,r5
      003D88 A3               [24] 1368 	inc	dptr
      003D89 F0               [24] 1369 	movx	@dptr,a
                                   1370 ;	keyboards/ajazz/ak820/ak820_nvm.c:174: while (len--) {
      003D8A 90 05 41         [24] 1371 	mov	dptr,#_eeprom_read_block_PARM_3
      003D8D E0               [24] 1372 	movx	a,@dptr
      003D8E FC               [12] 1373 	mov	r4,a
      003D8F A3               [24] 1374 	inc	dptr
      003D90 E0               [24] 1375 	movx	a,@dptr
      003D91 FD               [12] 1376 	mov	r5,a
      003D92                       1377 00107$:
      003D92 8C 02            [24] 1378 	mov	ar2,r4
      003D94 8D 03            [24] 1379 	mov	ar3,r5
      003D96 1C               [12] 1380 	dec	r4
      003D97 BC FF 01         [24] 1381 	cjne	r4,#0xff,00148$
      003D9A 1D               [12] 1382 	dec	r5
      003D9B                       1383 00148$:
      003D9B EA               [12] 1384 	mov	a,r2
      003D9C 4B               [12] 1385 	orl	a,r3
      003D9D 70 01            [24] 1386 	jnz	00149$
      003D9F 22               [24] 1387 	ret
      003DA0                       1388 00149$:
                                   1389 ;	keyboards/ajazz/ak820/ak820_nvm.c:175: if (offset >= AK820_NVM_SIZE) { *out++ = 0; continue; }
      003DA0 8E 02            [24] 1390 	mov	ar2,r6
      003DA2 8F 03            [24] 1391 	mov	ar3,r7
      003DA4 74 D8            [12] 1392 	mov	a,#0x100 - 0x28
      003DA6 2B               [12] 1393 	add	a,r3
      003DA7 50 2C            [24] 1394 	jnc	00102$
      003DA9 C0 04            [24] 1395 	push	ar4
      003DAB C0 05            [24] 1396 	push	ar5
      003DAD 90 05 46         [24] 1397 	mov	dptr,#_eeprom_read_block_out_10000_91
      003DB0 E0               [24] 1398 	movx	a,@dptr
      003DB1 F8               [12] 1399 	mov	r0,a
      003DB2 A3               [24] 1400 	inc	dptr
      003DB3 E0               [24] 1401 	movx	a,@dptr
      003DB4 F9               [12] 1402 	mov	r1,a
      003DB5 A3               [24] 1403 	inc	dptr
      003DB6 E0               [24] 1404 	movx	a,@dptr
      003DB7 FD               [12] 1405 	mov	r5,a
      003DB8 88 82            [24] 1406 	mov	dpl,r0
      003DBA 89 83            [24] 1407 	mov	dph,r1
      003DBC 8D F0            [24] 1408 	mov	b,r5
      003DBE E4               [12] 1409 	clr	a
      003DBF 12 B5 5C         [24] 1410 	lcall	__gptrput
      003DC2 90 05 46         [24] 1411 	mov	dptr,#_eeprom_read_block_out_10000_91
      003DC5 04               [12] 1412 	inc	a
      003DC6 28               [12] 1413 	add	a, r0
      003DC7 F0               [24] 1414 	movx	@dptr,a
      003DC8 E4               [12] 1415 	clr	a
      003DC9 39               [12] 1416 	addc	a, r1
      003DCA A3               [24] 1417 	inc	dptr
      003DCB F0               [24] 1418 	movx	@dptr,a
      003DCC ED               [12] 1419 	mov	a,r5
      003DCD A3               [24] 1420 	inc	dptr
      003DCE F0               [24] 1421 	movx	@dptr,a
      003DCF D0 05            [24] 1422 	pop	ar5
      003DD1 D0 04            [24] 1423 	pop	ar4
      003DD3 80 BD            [24] 1424 	sjmp	00107$
      003DD5                       1425 00102$:
                                   1426 ;	keyboards/ajazz/ak820/ak820_nvm.c:176: if (page_valid && (offset / AK820_FLASH_PAGE) == cached_page)
      003DD5 90 05 17         [24] 1427 	mov	dptr,#_page_valid
      003DD8 E0               [24] 1428 	movx	a,@dptr
      003DD9 60 67            [24] 1429 	jz	00104$
      003DDB C0 04            [24] 1430 	push	ar4
      003DDD C0 05            [24] 1431 	push	ar5
      003DDF 8A 00            [24] 1432 	mov	ar0,r2
      003DE1 EB               [12] 1433 	mov	a,r3
      003DE2 A2 E7            [12] 1434 	mov	c,acc.7
      003DE4 C8               [12] 1435 	xch	a,r0
      003DE5 33               [12] 1436 	rlc	a
      003DE6 C8               [12] 1437 	xch	a,r0
      003DE7 33               [12] 1438 	rlc	a
      003DE8 A2 E7            [12] 1439 	mov	c,acc.7
      003DEA C8               [12] 1440 	xch	a,r0
      003DEB 33               [12] 1441 	rlc	a
      003DEC C8               [12] 1442 	xch	a,r0
      003DED 33               [12] 1443 	rlc	a
      003DEE C8               [12] 1444 	xch	a,r0
      003DEF 54 03            [12] 1445 	anl	a,#0x03
      003DF1 F9               [12] 1446 	mov	r1,a
      003DF2 90 05 15         [24] 1447 	mov	dptr,#_cached_page
      003DF5 E0               [24] 1448 	movx	a,@dptr
      003DF6 FC               [12] 1449 	mov	r4,a
      003DF7 A3               [24] 1450 	inc	dptr
      003DF8 E0               [24] 1451 	movx	a,@dptr
      003DF9 FD               [12] 1452 	mov	r5,a
      003DFA E8               [12] 1453 	mov	a,r0
      003DFB B5 04 06         [24] 1454 	cjne	a,ar4,00152$
      003DFE E9               [12] 1455 	mov	a,r1
      003DFF B5 05 02         [24] 1456 	cjne	a,ar5,00152$
      003E02 80 06            [24] 1457 	sjmp	00153$
      003E04                       1458 00152$:
      003E04 D0 05            [24] 1459 	pop	ar5
      003E06 D0 04            [24] 1460 	pop	ar4
      003E08 80 38            [24] 1461 	sjmp	00104$
      003E0A                       1462 00153$:
                                   1463 ;	keyboards/ajazz/ak820/ak820_nvm.c:177: *out++ = page_data[offset % AK820_FLASH_PAGE];
      003E0A 90 05 46         [24] 1464 	mov	dptr,#_eeprom_read_block_out_10000_91
      003E0D E0               [24] 1465 	movx	a,@dptr
      003E0E F8               [12] 1466 	mov	r0,a
      003E0F A3               [24] 1467 	inc	dptr
      003E10 E0               [24] 1468 	movx	a,@dptr
      003E11 F9               [12] 1469 	mov	r1,a
      003E12 A3               [24] 1470 	inc	dptr
      003E13 E0               [24] 1471 	movx	a,@dptr
      003E14 FD               [12] 1472 	mov	r5,a
      003E15 53 02 3F         [24] 1473 	anl	ar2,#0x3f
      003E18 7B 00            [12] 1474 	mov	r3,#0x00
      003E1A EA               [12] 1475 	mov	a,r2
      003E1B 24 D5            [12] 1476 	add	a, #_page_data
      003E1D F5 82            [12] 1477 	mov	dpl,a
      003E1F EB               [12] 1478 	mov	a,r3
      003E20 34 04            [12] 1479 	addc	a, #(_page_data >> 8)
      003E22 F5 83            [12] 1480 	mov	dph,a
      003E24 E0               [24] 1481 	movx	a,@dptr
      003E25 88 82            [24] 1482 	mov	dpl,r0
      003E27 89 83            [24] 1483 	mov	dph,r1
      003E29 8D F0            [24] 1484 	mov	b,r5
      003E2B 12 B5 5C         [24] 1485 	lcall	__gptrput
      003E2E 90 05 46         [24] 1486 	mov	dptr,#_eeprom_read_block_out_10000_91
      003E31 74 01            [12] 1487 	mov	a,#0x01
      003E33 28               [12] 1488 	add	a, r0
      003E34 F0               [24] 1489 	movx	@dptr,a
      003E35 E4               [12] 1490 	clr	a
      003E36 39               [12] 1491 	addc	a, r1
      003E37 A3               [24] 1492 	inc	dptr
      003E38 F0               [24] 1493 	movx	@dptr,a
      003E39 ED               [12] 1494 	mov	a,r5
      003E3A A3               [24] 1495 	inc	dptr
      003E3B F0               [24] 1496 	movx	@dptr,a
      003E3C D0 05            [24] 1497 	pop	ar5
      003E3E D0 04            [24] 1498 	pop	ar4
      003E40 80 3C            [24] 1499 	sjmp	00105$
      003E42                       1500 00104$:
                                   1501 ;	keyboards/ajazz/ak820/ak820_nvm.c:178: else *out++ = ak820_flash_read(AK820_NVM_BASE + offset);
      003E42 C0 04            [24] 1502 	push	ar4
      003E44 C0 05            [24] 1503 	push	ar5
      003E46 90 05 46         [24] 1504 	mov	dptr,#_eeprom_read_block_out_10000_91
      003E49 E0               [24] 1505 	movx	a,@dptr
      003E4A F9               [12] 1506 	mov	r1,a
      003E4B A3               [24] 1507 	inc	dptr
      003E4C E0               [24] 1508 	movx	a,@dptr
      003E4D FA               [12] 1509 	mov	r2,a
      003E4E A3               [24] 1510 	inc	dptr
      003E4F E0               [24] 1511 	movx	a,@dptr
      003E50 FB               [12] 1512 	mov	r3,a
      003E51 8E 00            [24] 1513 	mov	ar0,r6
      003E53 8F 05            [24] 1514 	mov	ar5,r7
      003E55 74 C7            [12] 1515 	mov	a,#0xc7
      003E57 2D               [12] 1516 	add	a, r5
      003E58 FD               [12] 1517 	mov	r5,a
      003E59 88 82            [24] 1518 	mov	dpl, r0
      003E5B 8D 83            [24] 1519 	mov	dph, r5
      003E5D 12 35 12         [24] 1520 	lcall	_ak820_flash_read
      003E60 AD 82            [24] 1521 	mov	r5, dpl
      003E62 89 82            [24] 1522 	mov	dpl,r1
      003E64 8A 83            [24] 1523 	mov	dph,r2
      003E66 8B F0            [24] 1524 	mov	b,r3
      003E68 ED               [12] 1525 	mov	a,r5
      003E69 12 B5 5C         [24] 1526 	lcall	__gptrput
      003E6C 90 05 46         [24] 1527 	mov	dptr,#_eeprom_read_block_out_10000_91
      003E6F 74 01            [12] 1528 	mov	a,#0x01
      003E71 29               [12] 1529 	add	a, r1
      003E72 F0               [24] 1530 	movx	@dptr,a
      003E73 E4               [12] 1531 	clr	a
      003E74 3A               [12] 1532 	addc	a, r2
      003E75 A3               [24] 1533 	inc	dptr
      003E76 F0               [24] 1534 	movx	@dptr,a
      003E77 EB               [12] 1535 	mov	a,r3
      003E78 A3               [24] 1536 	inc	dptr
      003E79 F0               [24] 1537 	movx	@dptr,a
                                   1538 ;	keyboards/ajazz/ak820/ak820_nvm.c:179: ++offset;
      003E7A D0 05            [24] 1539 	pop	ar5
      003E7C D0 04            [24] 1540 	pop	ar4
                                   1541 ;	keyboards/ajazz/ak820/ak820_nvm.c:178: else *out++ = ak820_flash_read(AK820_NVM_BASE + offset);
      003E7E                       1542 00105$:
                                   1543 ;	keyboards/ajazz/ak820/ak820_nvm.c:179: ++offset;
      003E7E 0E               [12] 1544 	inc	r6
      003E7F BE 00 01         [24] 1545 	cjne	r6,#0x00,00154$
      003E82 0F               [12] 1546 	inc	r7
      003E83                       1547 00154$:
                                   1548 ;	keyboards/ajazz/ak820/ak820_nvm.c:181: }
      003E83 02 3D 92         [24] 1549 	ljmp	00107$
                                   1550 ;------------------------------------------------------------
                                   1551 ;Allocation info for local variables in function 'eeprom_write_block'
                                   1552 ;------------------------------------------------------------
                                   1553 ;sloc0         Allocated with name '_eeprom_write_block_sloc0_1_0'
                                   1554 ;addr          Allocated with name '_eeprom_write_block_PARM_2'
                                   1555 ;len           Allocated with name '_eeprom_write_block_PARM_3'
                                   1556 ;buf           Allocated with name '_eeprom_write_block_buf_10000_96'
                                   1557 ;offset        Allocated with name '_eeprom_write_block_offset_10000_97'
                                   1558 ;in            Allocated with name '_eeprom_write_block_in_10000_97'
                                   1559 ;value         Allocated with name '_eeprom_write_block_value_20000_100'
                                   1560 ;------------------------------------------------------------
                                   1561 ;	keyboards/ajazz/ak820/ak820_nvm.c:183: void eeprom_write_block(const void *buf, void *addr, size_t len) {
                                   1562 ;	-----------------------------------------
                                   1563 ;	 function eeprom_write_block
                                   1564 ;	-----------------------------------------
      003E86                       1565 _eeprom_write_block:
      003E86 AF F0            [24] 1566 	mov	r7,b
      003E88 AE 83            [24] 1567 	mov	r6,dph
      003E8A E5 82            [12] 1568 	mov	a,dpl
      003E8C 90 05 4E         [24] 1569 	mov	dptr,#_eeprom_write_block_buf_10000_96
      003E8F F0               [24] 1570 	movx	@dptr,a
      003E90 EE               [12] 1571 	mov	a,r6
      003E91 A3               [24] 1572 	inc	dptr
      003E92 F0               [24] 1573 	movx	@dptr,a
      003E93 EF               [12] 1574 	mov	a,r7
      003E94 A3               [24] 1575 	inc	dptr
      003E95 F0               [24] 1576 	movx	@dptr,a
                                   1577 ;	keyboards/ajazz/ak820/ak820_nvm.c:184: uint16_t offset = (uint16_t)(uintptr_t)addr;
      003E96 90 05 49         [24] 1578 	mov	dptr,#_eeprom_write_block_PARM_2
      003E99 E0               [24] 1579 	movx	a,@dptr
      003E9A FE               [12] 1580 	mov	r6,a
      003E9B A3               [24] 1581 	inc	dptr
      003E9C E0               [24] 1582 	movx	a,@dptr
      003E9D FF               [12] 1583 	mov	r7,a
                                   1584 ;	keyboards/ajazz/ak820/ak820_nvm.c:185: const uint8_t *in = (const uint8_t *)buf;
      003E9E 90 05 4E         [24] 1585 	mov	dptr,#_eeprom_write_block_buf_10000_96
      003EA1 E0               [24] 1586 	movx	a,@dptr
      003EA2 FB               [12] 1587 	mov	r3,a
      003EA3 A3               [24] 1588 	inc	dptr
      003EA4 E0               [24] 1589 	movx	a,@dptr
      003EA5 FC               [12] 1590 	mov	r4,a
      003EA6 A3               [24] 1591 	inc	dptr
      003EA7 E0               [24] 1592 	movx	a,@dptr
      003EA8 FD               [12] 1593 	mov	r5,a
                                   1594 ;	keyboards/ajazz/ak820/ak820_nvm.c:187: if (offset > AK820_NVM_SIZE || len > AK820_NVM_SIZE - offset) {
      003EA9 8E 01            [24] 1595 	mov	ar1,r6
      003EAB 8F 02            [24] 1596 	mov	ar2,r7
      003EAD C3               [12] 1597 	clr	c
      003EAE E4               [12] 1598 	clr	a
      003EAF 99               [12] 1599 	subb	a,r1
      003EB0 74 28            [12] 1600 	mov	a,#0x28
      003EB2 9A               [12] 1601 	subb	a,r2
      003EB3 40 23            [24] 1602 	jc	00101$
                                   1603 ;	free result
      003EB5 C0 03            [24] 1604 	push	ar3
      003EB7 C0 04            [24] 1605 	push	ar4
      003EB9 C0 05            [24] 1606 	push	ar5
      003EBB E4               [12] 1607 	clr	a
      003EBC C3               [12] 1608 	clr	c
      003EBD 9E               [12] 1609 	subb	a,r6
      003EBE F9               [12] 1610 	mov	r1,a
      003EBF 74 28            [12] 1611 	mov	a,#0x28
      003EC1 9F               [12] 1612 	subb	a,r7
      003EC2 FA               [12] 1613 	mov	r2,a
      003EC3 90 05 4C         [24] 1614 	mov	dptr,#_eeprom_write_block_PARM_3
      003EC6 E0               [24] 1615 	movx	a,@dptr
      003EC7 F8               [12] 1616 	mov	r0,a
      003EC8 A3               [24] 1617 	inc	dptr
      003EC9 E0               [24] 1618 	movx	a,@dptr
      003ECA FD               [12] 1619 	mov	r5,a
      003ECB C3               [12] 1620 	clr	c
      003ECC E9               [12] 1621 	mov	a,r1
      003ECD 98               [12] 1622 	subb	a,r0
      003ECE EA               [12] 1623 	mov	a,r2
      003ECF 9D               [12] 1624 	subb	a,r5
      003ED0 D0 05            [24] 1625 	pop	ar5
      003ED2 D0 04            [24] 1626 	pop	ar4
      003ED4 D0 03            [24] 1627 	pop	ar3
      003ED6 50 06            [24] 1628 	jnc	00125$
                                   1629 ;	free result
      003ED8                       1630 00101$:
                                   1631 ;	keyboards/ajazz/ak820/ak820_nvm.c:188: nvm_fail(AK820_NVM_FAULT_WRITE_RANGE);
      003ED8 75 82 0E         [24] 1632 	mov	dpl, #0x0e
                                   1633 ;	keyboards/ajazz/ak820/ak820_nvm.c:189: return;
      003EDB 02 37 A6         [24] 1634 	ljmp	_nvm_fail
                                   1635 ;	keyboards/ajazz/ak820/ak820_nvm.c:191: while (len--) {
      003EDE                       1636 00125$:
      003EDE 8E 0C            [24] 1637 	mov	_eeprom_write_block_sloc0_1_0,r6
      003EE0 8F 0D            [24] 1638 	mov	(_eeprom_write_block_sloc0_1_0 + 1),r7
      003EE2 90 05 4C         [24] 1639 	mov	dptr,#_eeprom_write_block_PARM_3
      003EE5 E0               [24] 1640 	movx	a,@dptr
      003EE6 F9               [12] 1641 	mov	r1,a
      003EE7 A3               [24] 1642 	inc	dptr
      003EE8 E0               [24] 1643 	movx	a,@dptr
      003EE9 FA               [12] 1644 	mov	r2,a
      003EEA                       1645 00108$:
      003EEA 89 00            [24] 1646 	mov	ar0,r1
      003EEC 8A 07            [24] 1647 	mov	ar7,r2
      003EEE 19               [12] 1648 	dec	r1
      003EEF B9 FF 01         [24] 1649 	cjne	r1,#0xff,00159$
      003EF2 1A               [12] 1650 	dec	r2
      003EF3                       1651 00159$:
      003EF3 E8               [12] 1652 	mov	a,r0
      003EF4 4F               [12] 1653 	orl	a,r7
      003EF5 70 03            [24] 1654 	jnz	00160$
      003EF7 02 3F 8E         [24] 1655 	ljmp	00110$
      003EFA                       1656 00160$:
                                   1657 ;	keyboards/ajazz/ak820/ak820_nvm.c:192: uint8_t value = *in++;
      003EFA C0 01            [24] 1658 	push	ar1
      003EFC C0 02            [24] 1659 	push	ar2
      003EFE 8B 82            [24] 1660 	mov	dpl,r3
      003F00 8C 83            [24] 1661 	mov	dph,r4
      003F02 8D F0            [24] 1662 	mov	b,r5
      003F04 12 B5 97         [24] 1663 	lcall	__gptrget
      003F07 FF               [12] 1664 	mov	r7,a
      003F08 A3               [24] 1665 	inc	dptr
      003F09 AB 82            [24] 1666 	mov	r3,dpl
      003F0B AC 83            [24] 1667 	mov	r4,dph
                                   1668 ;	keyboards/ajazz/ak820/ak820_nvm.c:193: if (!load_page(offset / AK820_FLASH_PAGE)) return;
      003F0D A8 0C            [24] 1669 	mov	r0,_eeprom_write_block_sloc0_1_0
      003F0F AE 0D            [24] 1670 	mov	r6,(_eeprom_write_block_sloc0_1_0 + 1)
      003F11 88 01            [24] 1671 	mov	ar1,r0
      003F13 EE               [12] 1672 	mov	a,r6
      003F14 A2 E7            [12] 1673 	mov	c,acc.7
      003F16 C9               [12] 1674 	xch	a,r1
      003F17 33               [12] 1675 	rlc	a
      003F18 C9               [12] 1676 	xch	a,r1
      003F19 33               [12] 1677 	rlc	a
      003F1A A2 E7            [12] 1678 	mov	c,acc.7
      003F1C C9               [12] 1679 	xch	a,r1
      003F1D 33               [12] 1680 	rlc	a
      003F1E C9               [12] 1681 	xch	a,r1
      003F1F 33               [12] 1682 	rlc	a
      003F20 C9               [12] 1683 	xch	a,r1
      003F21 54 03            [12] 1684 	anl	a,#0x03
      003F23 FA               [12] 1685 	mov	r2,a
      003F24 89 82            [24] 1686 	mov	dpl, r1
      003F26 8A 83            [24] 1687 	mov	dph, r2
      003F28 C0 07            [24] 1688 	push	ar7
      003F2A C0 06            [24] 1689 	push	ar6
      003F2C C0 05            [24] 1690 	push	ar5
      003F2E C0 04            [24] 1691 	push	ar4
      003F30 C0 03            [24] 1692 	push	ar3
      003F32 C0 02            [24] 1693 	push	ar2
      003F34 C0 01            [24] 1694 	push	ar1
      003F36 C0 00            [24] 1695 	push	ar0
      003F38 12 3C B0         [24] 1696 	lcall	_load_page
      003F3B E5 82            [12] 1697 	mov	a, dpl
      003F3D D0 00            [24] 1698 	pop	ar0
      003F3F D0 01            [24] 1699 	pop	ar1
      003F41 D0 02            [24] 1700 	pop	ar2
      003F43 D0 03            [24] 1701 	pop	ar3
      003F45 D0 04            [24] 1702 	pop	ar4
      003F47 D0 05            [24] 1703 	pop	ar5
      003F49 D0 06            [24] 1704 	pop	ar6
      003F4B D0 07            [24] 1705 	pop	ar7
      003F4D D0 02            [24] 1706 	pop	ar2
      003F4F D0 01            [24] 1707 	pop	ar1
      003F51 70 01            [24] 1708 	jnz	00105$
      003F53 22               [24] 1709 	ret
      003F54                       1710 00105$:
                                   1711 ;	keyboards/ajazz/ak820/ak820_nvm.c:194: if (page_data[offset % AK820_FLASH_PAGE] != value) {
      003F54 C0 01            [24] 1712 	push	ar1
      003F56 C0 02            [24] 1713 	push	ar2
      003F58 53 00 3F         [24] 1714 	anl	ar0,#0x3f
      003F5B 7E 00            [12] 1715 	mov	r6,#0x00
      003F5D E8               [12] 1716 	mov	a,r0
      003F5E 24 D5            [12] 1717 	add	a, #_page_data
      003F60 F8               [12] 1718 	mov	r0,a
      003F61 EE               [12] 1719 	mov	a,r6
      003F62 34 04            [12] 1720 	addc	a, #(_page_data >> 8)
      003F64 FE               [12] 1721 	mov	r6,a
      003F65 88 82            [24] 1722 	mov	dpl,r0
      003F67 8E 83            [24] 1723 	mov	dph,r6
      003F69 E0               [24] 1724 	movx	a,@dptr
      003F6A B5 07 06         [24] 1725 	cjne	a,ar7,00162$
      003F6D D0 02            [24] 1726 	pop	ar2
      003F6F D0 01            [24] 1727 	pop	ar1
      003F71 80 10            [24] 1728 	sjmp	00107$
      003F73                       1729 00162$:
      003F73 D0 02            [24] 1730 	pop	ar2
      003F75 D0 01            [24] 1731 	pop	ar1
                                   1732 ;	keyboards/ajazz/ak820/ak820_nvm.c:195: page_data[offset % AK820_FLASH_PAGE] = value;
      003F77 88 82            [24] 1733 	mov	dpl,r0
      003F79 8E 83            [24] 1734 	mov	dph,r6
      003F7B EF               [12] 1735 	mov	a,r7
      003F7C F0               [24] 1736 	movx	@dptr,a
                                   1737 ;	keyboards/ajazz/ak820/ak820_nvm.c:196: page_dirty = true;
      003F7D 90 05 18         [24] 1738 	mov	dptr,#_page_dirty
      003F80 74 01            [12] 1739 	mov	a,#0x01
      003F82 F0               [24] 1740 	movx	@dptr,a
      003F83                       1741 00107$:
                                   1742 ;	keyboards/ajazz/ak820/ak820_nvm.c:198: ++offset;
      003F83 05 0C            [12] 1743 	inc	_eeprom_write_block_sloc0_1_0
      003F85 E4               [12] 1744 	clr	a
      003F86 B5 0C 02         [24] 1745 	cjne	a,_eeprom_write_block_sloc0_1_0,00163$
      003F89 05 0D            [12] 1746 	inc	(_eeprom_write_block_sloc0_1_0 + 1)
      003F8B                       1747 00163$:
      003F8B 02 3E EA         [24] 1748 	ljmp	00108$
      003F8E                       1749 00110$:
                                   1750 ;	keyboards/ajazz/ak820/ak820_nvm.c:200: if (!batch_depth) ak820_nvm_flush();
      003F8E 90 05 1A         [24] 1751 	mov	dptr,#_batch_depth
      003F91 E0               [24] 1752 	movx	a,@dptr
      003F92 70 03            [24] 1753 	jnz	00113$
                                   1754 ;	keyboards/ajazz/ak820/ak820_nvm.c:201: }
      003F94 02 3A EA         [24] 1755 	ljmp	_ak820_nvm_flush
      003F97                       1756 00113$:
      003F97 22               [24] 1757 	ret
                                   1758 ;------------------------------------------------------------
                                   1759 ;Allocation info for local variables in function 'eeprom_driver_erase'
                                   1760 ;------------------------------------------------------------
                                   1761 ;page          Allocated with name '_eeprom_driver_erase_page_10000_106'
                                   1762 ;i             Allocated with name '_eeprom_driver_erase_i_10000_106'
                                   1763 ;------------------------------------------------------------
                                   1764 ;	keyboards/ajazz/ak820/ak820_nvm.c:203: void eeprom_driver_erase(void) {
                                   1765 ;	-----------------------------------------
                                   1766 ;	 function eeprom_driver_erase
                                   1767 ;	-----------------------------------------
      003F98                       1768 _eeprom_driver_erase:
                                   1769 ;	keyboards/ajazz/ak820/ak820_nvm.c:206: ak820_nvm_flush();
      003F98 12 3A EA         [24] 1770 	lcall	_ak820_nvm_flush
                                   1771 ;	keyboards/ajazz/ak820/ak820_nvm.c:207: for (page = 0; page != AK820_NVM_SIZE / AK820_FLASH_PAGE && !storage_failed; ++page) {
      003F9B 7E 00            [12] 1772 	mov	r6,#0x00
      003F9D 7F 00            [12] 1773 	mov	r7,#0x00
      003F9F                       1774 00111$:
      003F9F 8E 04            [24] 1775 	mov	ar4,r6
      003FA1 8F 05            [24] 1776 	mov	ar5,r7
      003FA3 BC A0 04         [24] 1777 	cjne	r4,#0xa0,00165$
      003FA6 BD 00 01         [24] 1778 	cjne	r5,#0x00,00165$
      003FA9 22               [24] 1779 	ret
      003FAA                       1780 00165$:
      003FAA 90 05 19         [24] 1781 	mov	dptr,#_storage_failed
      003FAD E0               [24] 1782 	movx	a,@dptr
      003FAE 70 46            [24] 1783 	jnz	00113$
                                   1784 ;	keyboards/ajazz/ak820/ak820_nvm.c:208: if (!load_page(page)) return;
      003FB0 8E 82            [24] 1785 	mov	dpl, r6
      003FB2 8F 83            [24] 1786 	mov	dph, r7
      003FB4 C0 07            [24] 1787 	push	ar7
      003FB6 C0 06            [24] 1788 	push	ar6
      003FB8 12 3C B0         [24] 1789 	lcall	_load_page
      003FBB E5 82            [12] 1790 	mov	a, dpl
      003FBD D0 06            [24] 1791 	pop	ar6
      003FBF D0 07            [24] 1792 	pop	ar7
      003FC1 70 01            [24] 1793 	jnz	00126$
                                   1794 ;	keyboards/ajazz/ak820/ak820_nvm.c:209: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003FC3 22               [24] 1795 	ret
      003FC4                       1796 00126$:
      003FC4 7D 00            [12] 1797 	mov	r5,#0x00
      003FC6                       1798 00107$:
                                   1799 ;	keyboards/ajazz/ak820/ak820_nvm.c:210: if (page_data[i]) { page_data[i] = 0; page_dirty = true; }
      003FC6 ED               [12] 1800 	mov	a,r5
      003FC7 24 D5            [12] 1801 	add	a, #_page_data
      003FC9 FB               [12] 1802 	mov	r3,a
      003FCA E4               [12] 1803 	clr	a
      003FCB 34 04            [12] 1804 	addc	a, #(_page_data >> 8)
      003FCD FC               [12] 1805 	mov	r4,a
      003FCE 8B 82            [24] 1806 	mov	dpl,r3
      003FD0 8C 83            [24] 1807 	mov	dph,r4
      003FD2 E0               [24] 1808 	movx	a,@dptr
      003FD3 60 0B            [24] 1809 	jz	00108$
      003FD5 8B 82            [24] 1810 	mov	dpl,r3
      003FD7 8C 83            [24] 1811 	mov	dph,r4
      003FD9 E4               [12] 1812 	clr	a
      003FDA F0               [24] 1813 	movx	@dptr,a
      003FDB 90 05 18         [24] 1814 	mov	dptr,#_page_dirty
      003FDE 04               [12] 1815 	inc	a
      003FDF F0               [24] 1816 	movx	@dptr,a
      003FE0                       1817 00108$:
                                   1818 ;	keyboards/ajazz/ak820/ak820_nvm.c:209: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003FE0 0D               [12] 1819 	inc	r5
      003FE1 BD 40 E2         [24] 1820 	cjne	r5,#0x40,00107$
                                   1821 ;	keyboards/ajazz/ak820/ak820_nvm.c:212: ak820_nvm_flush();
      003FE4 C0 07            [24] 1822 	push	ar7
      003FE6 C0 06            [24] 1823 	push	ar6
      003FE8 12 3A EA         [24] 1824 	lcall	_ak820_nvm_flush
      003FEB D0 06            [24] 1825 	pop	ar6
      003FED D0 07            [24] 1826 	pop	ar7
                                   1827 ;	keyboards/ajazz/ak820/ak820_nvm.c:207: for (page = 0; page != AK820_NVM_SIZE / AK820_FLASH_PAGE && !storage_failed; ++page) {
      003FEF 0E               [12] 1828 	inc	r6
      003FF0 BE 00 AC         [24] 1829 	cjne	r6,#0x00,00111$
      003FF3 0F               [12] 1830 	inc	r7
      003FF4 80 A9            [24] 1831 	sjmp	00111$
      003FF6                       1832 00113$:
                                   1833 ;	keyboards/ajazz/ak820/ak820_nvm.c:214: }
      003FF6 22               [24] 1834 	ret
                                   1835 	.area CSEG    (CODE)
                                   1836 	.area CONST   (CODE)
                                   1837 	.area XINIT   (CODE)
                                   1838 	.area CABS    (ABS,CODE)
