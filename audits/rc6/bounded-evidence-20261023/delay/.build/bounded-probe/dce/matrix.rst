                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module matrix
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _matrix_scan_custom
                                     12 	.globl _matrix_init_custom
                                     13 	.globl _ak820_matrix_snapshot
                                     14 	.globl _ak820_board_init
                                     15 	.globl _debounce_init
                                     16 	.globl _debounce
                                     17 	.globl _ADC_START
                                     18 	.globl _S0_R_FIFO
                                     19 	.globl _S0_T_FIFO
                                     20 	.globl _S0_FREE
                                     21 	.globl _S0_IF_BYTE
                                     22 	.globl _S0_IF_FIRST
                                     23 	.globl _S0_IF_OV
                                     24 	.globl _S0_FST_ACT
                                     25 	.globl _CP_RL2
                                     26 	.globl _C_T2
                                     27 	.globl _TR2
                                     28 	.globl _EXEN2
                                     29 	.globl _TCLK
                                     30 	.globl _RCLK
                                     31 	.globl _EXF2
                                     32 	.globl _CAP1F
                                     33 	.globl _TF2
                                     34 	.globl _RI
                                     35 	.globl _TI
                                     36 	.globl _RB8
                                     37 	.globl _TB8
                                     38 	.globl _REN
                                     39 	.globl _SM2
                                     40 	.globl _SM1
                                     41 	.globl _SM0
                                     42 	.globl _IT0
                                     43 	.globl _IE0
                                     44 	.globl _IT1
                                     45 	.globl _IE1
                                     46 	.globl _TR0
                                     47 	.globl _TF0
                                     48 	.globl _TR1
                                     49 	.globl _TF1
                                     50 	.globl _P4_0
                                     51 	.globl _P4_1
                                     52 	.globl _P4_2
                                     53 	.globl _P4_3
                                     54 	.globl _P4_4
                                     55 	.globl _P4_5
                                     56 	.globl _P4_6
                                     57 	.globl _RXD
                                     58 	.globl _TXD
                                     59 	.globl _INT0
                                     60 	.globl _INT1
                                     61 	.globl _T0
                                     62 	.globl _T1
                                     63 	.globl _MOSI1
                                     64 	.globl _MISO1
                                     65 	.globl _SCK1
                                     66 	.globl _P3_0
                                     67 	.globl _P3_1
                                     68 	.globl _P3_2
                                     69 	.globl _P3_3
                                     70 	.globl _P3_4
                                     71 	.globl _P3_5
                                     72 	.globl _P3_6
                                     73 	.globl _P3_7
                                     74 	.globl _CAP1_
                                     75 	.globl _T2_
                                     76 	.globl _CAP2_
                                     77 	.globl _T2EX_
                                     78 	.globl _RXD1
                                     79 	.globl _TXD1
                                     80 	.globl _P2_0
                                     81 	.globl _P2_1
                                     82 	.globl _P2_2
                                     83 	.globl _P2_3
                                     84 	.globl _P2_4
                                     85 	.globl _P2_5
                                     86 	.globl _P2_6
                                     87 	.globl _P2_7
                                     88 	.globl _AIN0
                                     89 	.globl _AIN1
                                     90 	.globl _AIN2
                                     91 	.globl _AIN3
                                     92 	.globl _AIN4
                                     93 	.globl _AIN5
                                     94 	.globl _AIN6
                                     95 	.globl _AIN7
                                     96 	.globl _CAP1
                                     97 	.globl _T2
                                     98 	.globl _CAP2
                                     99 	.globl _T2EX
                                    100 	.globl _INT0_
                                    101 	.globl _SCS
                                    102 	.globl _MOSI
                                    103 	.globl _MISO
                                    104 	.globl _SCK
                                    105 	.globl _RXD1_
                                    106 	.globl _TXD1_
                                    107 	.globl _P1_0
                                    108 	.globl _P1_1
                                    109 	.globl _P1_2
                                    110 	.globl _P1_3
                                    111 	.globl _P1_4
                                    112 	.globl _P1_5
                                    113 	.globl _P1_6
                                    114 	.globl _P1_7
                                    115 	.globl _AIN8
                                    116 	.globl _AIN9
                                    117 	.globl _AIN10
                                    118 	.globl _AIN11
                                    119 	.globl _AIN12
                                    120 	.globl _AIN13
                                    121 	.globl _RXD_
                                    122 	.globl _TXD_
                                    123 	.globl _SCL0
                                    124 	.globl _SDA0
                                    125 	.globl _P0_0
                                    126 	.globl _P0_1
                                    127 	.globl _P0_2
                                    128 	.globl _P0_3
                                    129 	.globl _P0_4
                                    130 	.globl _P0_5
                                    131 	.globl _P0_6
                                    132 	.globl _P0_7
                                    133 	.globl _IE_SPI0
                                    134 	.globl _IE_USB
                                    135 	.globl _IE_ADC
                                    136 	.globl _IE_UART1
                                    137 	.globl _IE_PWM_I2C
                                    138 	.globl _IE_GPIO
                                    139 	.globl _IE_WDOG
                                    140 	.globl _PX0
                                    141 	.globl _PT0
                                    142 	.globl _PX1
                                    143 	.globl _PT1
                                    144 	.globl _PS
                                    145 	.globl _PT2
                                    146 	.globl _PL_FLAG
                                    147 	.globl _PH_FLAG
                                    148 	.globl _EX0
                                    149 	.globl _ET0
                                    150 	.globl _EX1
                                    151 	.globl _ET1
                                    152 	.globl _ES
                                    153 	.globl _ET2
                                    154 	.globl _E_DIS
                                    155 	.globl _EA
                                    156 	.globl _P
                                    157 	.globl _F1
                                    158 	.globl _OV
                                    159 	.globl _RS0
                                    160 	.globl _RS1
                                    161 	.globl _F0
                                    162 	.globl _AC
                                    163 	.globl _CY
                                    164 	.globl _I2CS_INT_ST
                                    165 	.globl _I2CX_INT
                                    166 	.globl _LED_STATUS
                                    167 	.globl _LED_DMA_H
                                    168 	.globl _LED_DMA_L
                                    169 	.globl _LED_DMA
                                    170 	.globl _LED_PWM_OE
                                    171 	.globl _LED_COMMON
                                    172 	.globl _ADC_CHAN
                                    173 	.globl _ADC_DAT_H
                                    174 	.globl _ADC_DAT_L
                                    175 	.globl _ADC_DAT
                                    176 	.globl _ADC_CTRL
                                    177 	.globl _SPI1_CK_SE
                                    178 	.globl _SPI1_CTRL
                                    179 	.globl _SPI1_DATA
                                    180 	.globl _SPI1_STAT
                                    181 	.globl _SIF1
                                    182 	.globl _SBAUD1
                                    183 	.globl _SBUF1
                                    184 	.globl _SCON1
                                    185 	.globl _SPI0_SETUP
                                    186 	.globl _SPI0_CK_SE
                                    187 	.globl _SPI0_CTRL
                                    188 	.globl _SPI0_DATA
                                    189 	.globl _SPI0_STAT
                                    190 	.globl _T2CAP1H
                                    191 	.globl _T2CAP1L
                                    192 	.globl _T2CAP1
                                    193 	.globl _TH2
                                    194 	.globl _TL2
                                    195 	.globl _T2COUNT
                                    196 	.globl _RCAP2H
                                    197 	.globl _RCAP2L
                                    198 	.globl _RCAP2
                                    199 	.globl _T2MOD
                                    200 	.globl _T2CON
                                    201 	.globl _SBUF
                                    202 	.globl _SCON
                                    203 	.globl _TH1
                                    204 	.globl _TH0
                                    205 	.globl _TL1
                                    206 	.globl _TL0
                                    207 	.globl _TMOD
                                    208 	.globl _TCON
                                    209 	.globl _XBUS_AUX
                                    210 	.globl _P7
                                    211 	.globl _P6_DIR
                                    212 	.globl _P6_OUT_PU
                                    213 	.globl _P6_IN
                                    214 	.globl _P5_DIR
                                    215 	.globl _P5_OUT_PU
                                    216 	.globl _P5_IN
                                    217 	.globl _P4_LED_KEY
                                    218 	.globl _P4_DIR_PU
                                    219 	.globl _P4_MOD_OC
                                    220 	.globl _P4
                                    221 	.globl _P3_DIR_PU
                                    222 	.globl _P3_MOD_OC
                                    223 	.globl _P3
                                    224 	.globl _P2_DIR_PU
                                    225 	.globl _P2_MOD_OC
                                    226 	.globl _P2
                                    227 	.globl _P1_DIR_PU
                                    228 	.globl _P1_MOD_OC
                                    229 	.globl _P1
                                    230 	.globl _P0_DIR_PU
                                    231 	.globl _P0_MOD_OC
                                    232 	.globl _P0
                                    233 	.globl _ROM_CTRL
                                    234 	.globl _ROM_DATA_HH
                                    235 	.globl _ROM_DATA_HL
                                    236 	.globl _ROM_DATA_HI
                                    237 	.globl _ROM_ADDR_H
                                    238 	.globl _ROM_ADDR_L
                                    239 	.globl _ROM_ADDR
                                    240 	.globl _GPIO_IE
                                    241 	.globl _IP_EX
                                    242 	.globl _IE_EX
                                    243 	.globl _IP
                                    244 	.globl _IE
                                    245 	.globl _WDOG_COUNT
                                    246 	.globl _RESET_KEEP
                                    247 	.globl _WAKE_CTRL
                                    248 	.globl _CLOCK_CFG
                                    249 	.globl _POWER_CFG
                                    250 	.globl _PCON
                                    251 	.globl _GLOBAL_CFG
                                    252 	.globl _SAFE_MOD
                                    253 	.globl _DPH
                                    254 	.globl _DPL
                                    255 	.globl _SP
                                    256 	.globl _A_INV
                                    257 	.globl _B
                                    258 	.globl _ACC
                                    259 	.globl _PSW
                                    260 	.globl _matrix_is_on_PARM_2
                                    261 	.globl _matrix
                                    262 	.globl _raw_matrix
                                    263 	.globl _matrix_is_on
                                    264 	.globl _matrix_get_row
                                    265 	.globl _matrix_init
                                    266 	.globl _matrix_scan
                                    267 	.globl _matrix_print
                                    268 ;--------------------------------------------------------
                                    269 ; special function registers
                                    270 ;--------------------------------------------------------
                                    271 	.area RSEG    (ABS,DATA)
      000000                        272 	.org 0x0000
                           0000D0   273 _PSW	=	0x00d0
                           0000E0   274 _ACC	=	0x00e0
                           0000F0   275 _B	=	0x00f0
                           0000FD   276 _A_INV	=	0x00fd
                           000081   277 _SP	=	0x0081
                           000082   278 _DPL	=	0x0082
                           000083   279 _DPH	=	0x0083
                           0000A1   280 _SAFE_MOD	=	0x00a1
                           0000B1   281 _GLOBAL_CFG	=	0x00b1
                           000087   282 _PCON	=	0x0087
                           0000BA   283 _POWER_CFG	=	0x00ba
                           0000B9   284 _CLOCK_CFG	=	0x00b9
                           0000A9   285 _WAKE_CTRL	=	0x00a9
                           0000FE   286 _RESET_KEEP	=	0x00fe
                           0000FF   287 _WDOG_COUNT	=	0x00ff
                           0000A8   288 _IE	=	0x00a8
                           0000B8   289 _IP	=	0x00b8
                           0000E8   290 _IE_EX	=	0x00e8
                           0000E9   291 _IP_EX	=	0x00e9
                           0000B2   292 _GPIO_IE	=	0x00b2
                           008584   293 _ROM_ADDR	=	0x8584
                           000084   294 _ROM_ADDR_L	=	0x0084
                           000085   295 _ROM_ADDR_H	=	0x0085
                           008F8E   296 _ROM_DATA_HI	=	0x8f8e
                           00008E   297 _ROM_DATA_HL	=	0x008e
                           00008F   298 _ROM_DATA_HH	=	0x008f
                           000086   299 _ROM_CTRL	=	0x0086
                           000080   300 _P0	=	0x0080
                           0000C4   301 _P0_MOD_OC	=	0x00c4
                           0000C5   302 _P0_DIR_PU	=	0x00c5
                           000090   303 _P1	=	0x0090
                           000092   304 _P1_MOD_OC	=	0x0092
                           000093   305 _P1_DIR_PU	=	0x0093
                           0000A0   306 _P2	=	0x00a0
                           000094   307 _P2_MOD_OC	=	0x0094
                           000095   308 _P2_DIR_PU	=	0x0095
                           0000B0   309 _P3	=	0x00b0
                           000096   310 _P3_MOD_OC	=	0x0096
                           000097   311 _P3_DIR_PU	=	0x0097
                           0000C0   312 _P4	=	0x00c0
                           0000C2   313 _P4_MOD_OC	=	0x00c2
                           0000C3   314 _P4_DIR_PU	=	0x00c3
                           0000C1   315 _P4_LED_KEY	=	0x00c1
                           0000AA   316 _P5_IN	=	0x00aa
                           0000AB   317 _P5_OUT_PU	=	0x00ab
                           0000AC   318 _P5_DIR	=	0x00ac
                           0000AD   319 _P6_IN	=	0x00ad
                           0000AE   320 _P6_OUT_PU	=	0x00ae
                           0000AF   321 _P6_DIR	=	0x00af
                           0000F1   322 _P7	=	0x00f1
                           0000A2   323 _XBUS_AUX	=	0x00a2
                           000088   324 _TCON	=	0x0088
                           000089   325 _TMOD	=	0x0089
                           00008A   326 _TL0	=	0x008a
                           00008B   327 _TL1	=	0x008b
                           00008C   328 _TH0	=	0x008c
                           00008D   329 _TH1	=	0x008d
                           000098   330 _SCON	=	0x0098
                           000099   331 _SBUF	=	0x0099
                           0000C8   332 _T2CON	=	0x00c8
                           0000C9   333 _T2MOD	=	0x00c9
                           00CBCA   334 _RCAP2	=	0xcbca
                           0000CA   335 _RCAP2L	=	0x00ca
                           0000CB   336 _RCAP2H	=	0x00cb
                           00CDCC   337 _T2COUNT	=	0xcdcc
                           0000CC   338 _TL2	=	0x00cc
                           0000CD   339 _TH2	=	0x00cd
                           00CFCE   340 _T2CAP1	=	0xcfce
                           0000CE   341 _T2CAP1L	=	0x00ce
                           0000CF   342 _T2CAP1H	=	0x00cf
                           0000F8   343 _SPI0_STAT	=	0x00f8
                           0000F9   344 _SPI0_DATA	=	0x00f9
                           0000FA   345 _SPI0_CTRL	=	0x00fa
                           0000FB   346 _SPI0_CK_SE	=	0x00fb
                           0000FC   347 _SPI0_SETUP	=	0x00fc
                           0000BC   348 _SCON1	=	0x00bc
                           0000BD   349 _SBUF1	=	0x00bd
                           0000BE   350 _SBAUD1	=	0x00be
                           0000BF   351 _SIF1	=	0x00bf
                           0000B4   352 _SPI1_STAT	=	0x00b4
                           0000B5   353 _SPI1_DATA	=	0x00b5
                           0000B6   354 _SPI1_CTRL	=	0x00b6
                           0000B7   355 _SPI1_CK_SE	=	0x00b7
                           0000F3   356 _ADC_CTRL	=	0x00f3
                           00F5F4   357 _ADC_DAT	=	0xf5f4
                           0000F4   358 _ADC_DAT_L	=	0x00f4
                           0000F5   359 _ADC_DAT_H	=	0x00f5
                           0000F6   360 _ADC_CHAN	=	0x00f6
                           0000A6   361 _LED_COMMON	=	0x00a6
                           0000A7   362 _LED_PWM_OE	=	0x00a7
                           00C7C6   363 _LED_DMA	=	0xc7c6
                           0000C6   364 _LED_DMA_L	=	0x00c6
                           0000C7   365 _LED_DMA_H	=	0x00c7
                           0000F7   366 _LED_STATUS	=	0x00f7
                           0000B3   367 _I2CX_INT	=	0x00b3
                           0000BB   368 _I2CS_INT_ST	=	0x00bb
                                    369 ;--------------------------------------------------------
                                    370 ; special function bits
                                    371 ;--------------------------------------------------------
                                    372 	.area RSEG    (ABS,DATA)
      000000                        373 	.org 0x0000
                           0000D7   374 _CY	=	0x00d7
                           0000D6   375 _AC	=	0x00d6
                           0000D5   376 _F0	=	0x00d5
                           0000D4   377 _RS1	=	0x00d4
                           0000D3   378 _RS0	=	0x00d3
                           0000D2   379 _OV	=	0x00d2
                           0000D1   380 _F1	=	0x00d1
                           0000D0   381 _P	=	0x00d0
                           0000AF   382 _EA	=	0x00af
                           0000AE   383 _E_DIS	=	0x00ae
                           0000AD   384 _ET2	=	0x00ad
                           0000AC   385 _ES	=	0x00ac
                           0000AB   386 _ET1	=	0x00ab
                           0000AA   387 _EX1	=	0x00aa
                           0000A9   388 _ET0	=	0x00a9
                           0000A8   389 _EX0	=	0x00a8
                           0000BF   390 _PH_FLAG	=	0x00bf
                           0000BE   391 _PL_FLAG	=	0x00be
                           0000BD   392 _PT2	=	0x00bd
                           0000BC   393 _PS	=	0x00bc
                           0000BB   394 _PT1	=	0x00bb
                           0000BA   395 _PX1	=	0x00ba
                           0000B9   396 _PT0	=	0x00b9
                           0000B8   397 _PX0	=	0x00b8
                           0000EF   398 _IE_WDOG	=	0x00ef
                           0000EE   399 _IE_GPIO	=	0x00ee
                           0000ED   400 _IE_PWM_I2C	=	0x00ed
                           0000EC   401 _IE_UART1	=	0x00ec
                           0000EB   402 _IE_ADC	=	0x00eb
                           0000E9   403 _IE_USB	=	0x00e9
                           0000E8   404 _IE_SPI0	=	0x00e8
                           000087   405 _P0_7	=	0x0087
                           000086   406 _P0_6	=	0x0086
                           000085   407 _P0_5	=	0x0085
                           000084   408 _P0_4	=	0x0084
                           000083   409 _P0_3	=	0x0083
                           000082   410 _P0_2	=	0x0082
                           000081   411 _P0_1	=	0x0081
                           000080   412 _P0_0	=	0x0080
                           000081   413 _SDA0	=	0x0081
                           000080   414 _SCL0	=	0x0080
                           000083   415 _TXD_	=	0x0083
                           000082   416 _RXD_	=	0x0082
                           000085   417 _AIN13	=	0x0085
                           000084   418 _AIN12	=	0x0084
                           000083   419 _AIN11	=	0x0083
                           000082   420 _AIN10	=	0x0082
                           000081   421 _AIN9	=	0x0081
                           000080   422 _AIN8	=	0x0080
                           000097   423 _P1_7	=	0x0097
                           000096   424 _P1_6	=	0x0096
                           000095   425 _P1_5	=	0x0095
                           000094   426 _P1_4	=	0x0094
                           000093   427 _P1_3	=	0x0093
                           000092   428 _P1_2	=	0x0092
                           000091   429 _P1_1	=	0x0091
                           000090   430 _P1_0	=	0x0090
                           000097   431 _TXD1_	=	0x0097
                           000096   432 _RXD1_	=	0x0096
                           000097   433 _SCK	=	0x0097
                           000096   434 _MISO	=	0x0096
                           000095   435 _MOSI	=	0x0095
                           000094   436 _SCS	=	0x0094
                           000092   437 _INT0_	=	0x0092
                           000091   438 _T2EX	=	0x0091
                           000091   439 _CAP2	=	0x0091
                           000090   440 _T2	=	0x0090
                           000090   441 _CAP1	=	0x0090
                           000097   442 _AIN7	=	0x0097
                           000096   443 _AIN6	=	0x0096
                           000095   444 _AIN5	=	0x0095
                           000094   445 _AIN4	=	0x0094
                           000093   446 _AIN3	=	0x0093
                           000092   447 _AIN2	=	0x0092
                           000091   448 _AIN1	=	0x0091
                           000090   449 _AIN0	=	0x0090
                           0000A7   450 _P2_7	=	0x00a7
                           0000A6   451 _P2_6	=	0x00a6
                           0000A5   452 _P2_5	=	0x00a5
                           0000A4   453 _P2_4	=	0x00a4
                           0000A3   454 _P2_3	=	0x00a3
                           0000A2   455 _P2_2	=	0x00a2
                           0000A1   456 _P2_1	=	0x00a1
                           0000A0   457 _P2_0	=	0x00a0
                           0000A7   458 _TXD1	=	0x00a7
                           0000A6   459 _RXD1	=	0x00a6
                           0000A5   460 _T2EX_	=	0x00a5
                           0000A5   461 _CAP2_	=	0x00a5
                           0000A4   462 _T2_	=	0x00a4
                           0000A4   463 _CAP1_	=	0x00a4
                           0000B7   464 _P3_7	=	0x00b7
                           0000B6   465 _P3_6	=	0x00b6
                           0000B5   466 _P3_5	=	0x00b5
                           0000B4   467 _P3_4	=	0x00b4
                           0000B3   468 _P3_3	=	0x00b3
                           0000B2   469 _P3_2	=	0x00b2
                           0000B1   470 _P3_1	=	0x00b1
                           0000B0   471 _P3_0	=	0x00b0
                           0000B7   472 _SCK1	=	0x00b7
                           0000B6   473 _MISO1	=	0x00b6
                           0000B5   474 _MOSI1	=	0x00b5
                           0000B5   475 _T1	=	0x00b5
                           0000B4   476 _T0	=	0x00b4
                           0000B3   477 _INT1	=	0x00b3
                           0000B2   478 _INT0	=	0x00b2
                           0000B1   479 _TXD	=	0x00b1
                           0000B0   480 _RXD	=	0x00b0
                           0000C6   481 _P4_6	=	0x00c6
                           0000C5   482 _P4_5	=	0x00c5
                           0000C4   483 _P4_4	=	0x00c4
                           0000C3   484 _P4_3	=	0x00c3
                           0000C2   485 _P4_2	=	0x00c2
                           0000C1   486 _P4_1	=	0x00c1
                           0000C0   487 _P4_0	=	0x00c0
                           00008F   488 _TF1	=	0x008f
                           00008E   489 _TR1	=	0x008e
                           00008D   490 _TF0	=	0x008d
                           00008C   491 _TR0	=	0x008c
                           00008B   492 _IE1	=	0x008b
                           00008A   493 _IT1	=	0x008a
                           000089   494 _IE0	=	0x0089
                           000088   495 _IT0	=	0x0088
                           00009F   496 _SM0	=	0x009f
                           00009E   497 _SM1	=	0x009e
                           00009D   498 _SM2	=	0x009d
                           00009C   499 _REN	=	0x009c
                           00009B   500 _TB8	=	0x009b
                           00009A   501 _RB8	=	0x009a
                           000099   502 _TI	=	0x0099
                           000098   503 _RI	=	0x0098
                           0000CF   504 _TF2	=	0x00cf
                           0000CF   505 _CAP1F	=	0x00cf
                           0000CE   506 _EXF2	=	0x00ce
                           0000CD   507 _RCLK	=	0x00cd
                           0000CC   508 _TCLK	=	0x00cc
                           0000CB   509 _EXEN2	=	0x00cb
                           0000CA   510 _TR2	=	0x00ca
                           0000C9   511 _C_T2	=	0x00c9
                           0000C8   512 _CP_RL2	=	0x00c8
                           0000FF   513 _S0_FST_ACT	=	0x00ff
                           0000FE   514 _S0_IF_OV	=	0x00fe
                           0000FD   515 _S0_IF_FIRST	=	0x00fd
                           0000FC   516 _S0_IF_BYTE	=	0x00fc
                           0000FB   517 _S0_FREE	=	0x00fb
                           0000FA   518 _S0_T_FIFO	=	0x00fa
                           0000F8   519 _S0_R_FIFO	=	0x00f8
                           0000F7   520 _ADC_START	=	0x00f7
                                    521 ;--------------------------------------------------------
                                    522 ; overlayable register banks
                                    523 ;--------------------------------------------------------
                                    524 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        525 	.ds 8
                                    526 ;--------------------------------------------------------
                                    527 ; internal ram data
                                    528 ;--------------------------------------------------------
                                    529 	.area DSEG    (DATA)
                                    530 ;--------------------------------------------------------
                                    531 ; overlayable items in internal ram
                                    532 ;--------------------------------------------------------
                                    533 ;--------------------------------------------------------
                                    534 ; indirectly addressable internal ram data
                                    535 ;--------------------------------------------------------
                                    536 	.area ISEG    (DATA)
                                    537 ;--------------------------------------------------------
                                    538 ; absolute internal ram data
                                    539 ;--------------------------------------------------------
                                    540 	.area IABS    (ABS,DATA)
                                    541 	.area IABS    (ABS,DATA)
                                    542 ;--------------------------------------------------------
                                    543 ; bit data
                                    544 ;--------------------------------------------------------
                                    545 	.area BSEG    (BIT)
      000008                        546 _matrix_is_on_sloc0_1_0:
      000008                        547 	.ds 1
                                    548 ;--------------------------------------------------------
                                    549 ; paged external ram data
                                    550 ;--------------------------------------------------------
                                    551 	.area PSEG    (PAG,XDATA)
                                    552 ;--------------------------------------------------------
                                    553 ; uninitialized external ram data
                                    554 ;--------------------------------------------------------
                                    555 	.area XSEG    (XDATA)
      000660                        556 _raw_matrix::
      000660                        557 	.ds 16
      000670                        558 _matrix::
      000670                        559 	.ds 16
      000680                        560 _matrix_is_on_PARM_2:
      000680                        561 	.ds 1
      000681                        562 _matrix_is_on_row_10000_83:
      000681                        563 	.ds 1
      000682                        564 _matrix_get_row_row_10000_85:
      000682                        565 	.ds 1
      000683                        566 _matrix_scan_custom_current_matrix_10000_103:
      000683                        567 	.ds 3
                                    568 ;--------------------------------------------------------
                                    569 ; absolute external ram data
                                    570 ;--------------------------------------------------------
                                    571 	.area XABS    (ABS,XDATA)
                                    572 ;--------------------------------------------------------
                                    573 ; initialized external ram data
                                    574 ;--------------------------------------------------------
                                    575 	.area XISEG   (XDATA)
                                    576 	.area HOME    (CODE)
                                    577 	.area GSINIT0 (CODE)
                                    578 	.area GSINIT1 (CODE)
                                    579 	.area GSINIT2 (CODE)
                                    580 	.area GSINIT3 (CODE)
                                    581 	.area GSINIT4 (CODE)
                                    582 	.area GSINIT5 (CODE)
                                    583 	.area GSINIT  (CODE)
                                    584 	.area GSFINAL (CODE)
                                    585 	.area CSEG    (CODE)
                                    586 ;--------------------------------------------------------
                                    587 ; global & static initialisations
                                    588 ;--------------------------------------------------------
                                    589 	.area HOME    (CODE)
                                    590 	.area GSINIT  (CODE)
                                    591 	.area GSFINAL (CODE)
                                    592 	.area GSINIT  (CODE)
                                    593 ;--------------------------------------------------------
                                    594 ; Home
                                    595 ;--------------------------------------------------------
                                    596 	.area HOME    (CODE)
                                    597 	.area HOME    (CODE)
                                    598 ;--------------------------------------------------------
                                    599 ; code
                                    600 ;--------------------------------------------------------
                                    601 	.area CSEG    (CODE)
                                    602 ;------------------------------------------------------------
                                    603 ;Allocation info for local variables in function 'matrix_rows'
                                    604 ;------------------------------------------------------------
                                    605 ;	keyboards/ajazz/ak820/matrix.c:17: uint8_t matrix_rows(void) { return MATRIX_ROWS; }
                                    606 ;	-----------------------------------------
                           000007   607 	ar7 = 0x07
                           000006   608 	ar6 = 0x06
                           000005   609 	ar5 = 0x05
                           000004   610 	ar4 = 0x04
                           000003   611 	ar3 = 0x03
                           000002   612 	ar2 = 0x02
                           000001   613 	ar1 = 0x01
                           000000   614 	ar0 = 0x00
                                    615 ;	 function matrix_is_on
                                    616 ;	-----------------------------------------
      00530F                        617 _matrix_is_on:
      00530F E5 82            [12]  618 	mov	a,dpl
      005311 90 06 81         [24]  619 	mov	dptr,#_matrix_is_on_row_10000_83
      005314 F0               [24]  620 	movx	@dptr,a
                                    621 ;	keyboards/ajazz/ak820/matrix.c:21: return row < MATRIX_ROWS && col < MATRIX_COLS && (matrix[row] & (MATRIX_ROW_SHIFTER << col));
      005315 E0               [24]  622 	movx	a,@dptr
      005316 FF               [12]  623 	mov	r7,a
      005317 BF 10 00         [24]  624 	cjne	r7,#0x10,00122$
      00531A                        625 00122$:
      00531A 50 35            [24]  626 	jnc	00103$
      00531C 90 06 80         [24]  627 	mov	dptr,#_matrix_is_on_PARM_2
      00531F E0               [24]  628 	movx	a,@dptr
      005320 FE               [12]  629 	mov	r6,a
      005321 BE 08 00         [24]  630 	cjne	r6,#0x08,00124$
      005324                        631 00124$:
      005324 50 2B            [24]  632 	jnc	00103$
      005326 EF               [12]  633 	mov	a,r7
      005327 24 70            [12]  634 	add	a, #_matrix
      005329 F5 82            [12]  635 	mov	dpl,a
      00532B E4               [12]  636 	clr	a
      00532C 34 06            [12]  637 	addc	a, #(_matrix >> 8)
      00532E F5 83            [12]  638 	mov	dph,a
      005330 E0               [24]  639 	movx	a,@dptr
      005331 FF               [12]  640 	mov	r7,a
      005332 8E F0            [24]  641 	mov	b,r6
      005334 05 F0            [12]  642 	inc	b
      005336 7E 01            [12]  643 	mov	r6,#0x01
      005338 7D 00            [12]  644 	mov	r5,#0x00
      00533A 80 06            [24]  645 	sjmp	00127$
      00533C                        646 00126$:
      00533C EE               [12]  647 	mov	a,r6
      00533D 2E               [12]  648 	add	a,r6
      00533E FE               [12]  649 	mov	r6,a
      00533F ED               [12]  650 	mov	a,r5
      005340 33               [12]  651 	rlc	a
      005341 FD               [12]  652 	mov	r5,a
      005342                        653 00127$:
      005342 D5 F0 F7         [24]  654 	djnz	b,00126$
      005345 7C 00            [12]  655 	mov	r4,#0x00
      005347 EF               [12]  656 	mov	a,r7
      005348 52 06            [12]  657 	anl	ar6,a
      00534A EC               [12]  658 	mov	a,r4
      00534B 52 05            [12]  659 	anl	ar5,a
      00534D EE               [12]  660 	mov	a,r6
      00534E 4D               [12]  661 	orl	a,r5
      00534F 70 04            [24]  662 	jnz	00104$
      005351                        663 00103$:
                                    664 ;	assignBit
      005351 C2 08            [12]  665 	clr	_matrix_is_on_sloc0_1_0
      005353 80 02            [24]  666 	sjmp	00105$
      005355                        667 00104$:
                                    668 ;	assignBit
      005355 D2 08            [12]  669 	setb	_matrix_is_on_sloc0_1_0
      005357                        670 00105$:
      005357 A2 08            [12]  671 	mov	c,_matrix_is_on_sloc0_1_0
      005359 E4               [12]  672 	clr	a
      00535A 33               [12]  673 	rlc	a
      00535B F5 82            [12]  674 	mov	dpl, a
                                    675 ;	keyboards/ajazz/ak820/matrix.c:22: }
      00535D 22               [24]  676 	ret
                                    677 ;------------------------------------------------------------
                                    678 ;Allocation info for local variables in function 'matrix_get_row'
                                    679 ;------------------------------------------------------------
                                    680 ;row           Allocated with name '_matrix_get_row_row_10000_85'
                                    681 ;------------------------------------------------------------
                                    682 ;	keyboards/ajazz/ak820/matrix.c:24: matrix_row_t matrix_get_row(uint8_t row) {
                                    683 ;	-----------------------------------------
                                    684 ;	 function matrix_get_row
                                    685 ;	-----------------------------------------
      00535E                        686 _matrix_get_row:
      00535E C0 07            [24]  687 	push	ar7
      005360 E5 82            [12]  688 	mov	a,dpl
      005362 90 06 82         [24]  689 	mov	dptr,#_matrix_get_row_row_10000_85
      005365 F0               [24]  690 	movx	@dptr,a
                                    691 ;	keyboards/ajazz/ak820/matrix.c:25: return row < MATRIX_ROWS ? matrix[row] : 0;
      005366 E0               [24]  692 	movx	a,@dptr
      005367 FF               [12]  693 	mov	r7,a
      005368 BF 10 00         [24]  694 	cjne	r7,#0x10,00112$
      00536B                        695 00112$:
      00536B 50 0E            [24]  696 	jnc	00103$
      00536D EF               [12]  697 	mov	a,r7
      00536E 24 70            [12]  698 	add	a, #_matrix
      005370 F5 82            [12]  699 	mov	dpl,a
      005372 E4               [12]  700 	clr	a
      005373 34 06            [12]  701 	addc	a, #(_matrix >> 8)
      005375 F5 83            [12]  702 	mov	dph,a
      005377 E0               [24]  703 	movx	a,@dptr
      005378 FF               [12]  704 	mov	r7,a
      005379 80 02            [24]  705 	sjmp	00104$
      00537B                        706 00103$:
      00537B 7F 00            [12]  707 	mov	r7,#0x00
      00537D                        708 00104$:
      00537D 8F 82            [24]  709 	mov	dpl, r7
                                    710 ;	keyboards/ajazz/ak820/matrix.c:26: }
      00537F D0 07            [24]  711 	pop	ar7
      005381 22               [24]  712 	ret
                                    713 ;------------------------------------------------------------
                                    714 ;Allocation info for local variables in function 'peek_matrix'
                                    715 ;------------------------------------------------------------
                                    716 ;col           Allocated with name '_peek_matrix_PARM_2'
                                    717 ;raw           Allocated with name '_peek_matrix_PARM_3'
                                    718 ;row           Allocated with name '_peek_matrix_row_10000_87'
                                    719 ;------------------------------------------------------------
                                    720 ;	keyboards/ajazz/ak820/matrix.c:28: bool peek_matrix(uint8_t row, uint8_t col, bool raw) {
                                    721 ;	-----------------------------------------
                                    722 ;	 function matrix_init_custom
                                    723 ;	-----------------------------------------
      005382                        724 _matrix_init_custom:
      005382 02 31 82         [24]  725 	ljmp	_ak820_board_init
                                    726 ;------------------------------------------------------------
                                    727 ;Allocation info for local variables in function 'matrix_scan_custom'
                                    728 ;------------------------------------------------------------
                                    729 ;current_matrix Allocated with name '_matrix_scan_custom_current_matrix_10000_103'
                                    730 ;------------------------------------------------------------
                                    731 ;	keyboards/ajazz/ak820/matrix.c:45: bool matrix_scan_custom(matrix_row_t current_matrix[]) { return ak820_matrix_snapshot(current_matrix); }
                                    732 ;	-----------------------------------------
                                    733 ;	 function matrix_scan_custom
                                    734 ;	-----------------------------------------
      005385                        735 _matrix_scan_custom:
      005385 AF F0            [24]  736 	mov	r7,b
      005387 AE 83            [24]  737 	mov	r6,dph
      005389 E5 82            [12]  738 	mov	a,dpl
      00538B 90 06 83         [24]  739 	mov	dptr,#_matrix_scan_custom_current_matrix_10000_103
      00538E F0               [24]  740 	movx	@dptr,a
      00538F EE               [12]  741 	mov	a,r6
      005390 A3               [24]  742 	inc	dptr
      005391 F0               [24]  743 	movx	@dptr,a
      005392 EF               [12]  744 	mov	a,r7
      005393 A3               [24]  745 	inc	dptr
      005394 F0               [24]  746 	movx	@dptr,a
      005395 90 06 83         [24]  747 	mov	dptr,#_matrix_scan_custom_current_matrix_10000_103
      005398 E0               [24]  748 	movx	a,@dptr
      005399 FD               [12]  749 	mov	r5,a
      00539A A3               [24]  750 	inc	dptr
      00539B E0               [24]  751 	movx	a,@dptr
      00539C FE               [12]  752 	mov	r6,a
      00539D A3               [24]  753 	inc	dptr
      00539E E0               [24]  754 	movx	a,@dptr
      00539F FF               [12]  755 	mov	r7,a
      0053A0 8D 82            [24]  756 	mov	dpl, r5
      0053A2 8E 83            [24]  757 	mov	dph, r6
      0053A4 8F F0            [24]  758 	mov	b, r7
      0053A6 02 32 F5         [24]  759 	ljmp	_ak820_matrix_snapshot
                                    760 ;------------------------------------------------------------
                                    761 ;Allocation info for local variables in function 'matrix_init'
                                    762 ;------------------------------------------------------------
                                    763 ;i             Allocated with name '_matrix_init_i_10000_106'
                                    764 ;------------------------------------------------------------
                                    765 ;	keyboards/ajazz/ak820/matrix.c:47: void matrix_init(void) {
                                    766 ;	-----------------------------------------
                                    767 ;	 function matrix_init
                                    768 ;	-----------------------------------------
      0053A9                        769 _matrix_init:
                                    770 ;	keyboards/ajazz/ak820/matrix.c:49: for (i = 0; i < MATRIX_ROWS; ++i) {
      0053A9 7F 00            [12]  771 	mov	r7,#0x00
      0053AB                        772 00102$:
                                    773 ;	keyboards/ajazz/ak820/matrix.c:50: raw_matrix[i] = 0;
      0053AB EF               [12]  774 	mov	a,r7
      0053AC 24 60            [12]  775 	add	a, #_raw_matrix
      0053AE F5 82            [12]  776 	mov	dpl,a
      0053B0 E4               [12]  777 	clr	a
      0053B1 34 06            [12]  778 	addc	a, #(_raw_matrix >> 8)
      0053B3 F5 83            [12]  779 	mov	dph,a
      0053B5 E4               [12]  780 	clr	a
      0053B6 F0               [24]  781 	movx	@dptr,a
                                    782 ;	keyboards/ajazz/ak820/matrix.c:51: matrix[i] = 0;
      0053B7 EF               [12]  783 	mov	a,r7
      0053B8 24 70            [12]  784 	add	a, #_matrix
      0053BA F5 82            [12]  785 	mov	dpl,a
      0053BC E4               [12]  786 	clr	a
      0053BD 34 06            [12]  787 	addc	a, #(_matrix >> 8)
      0053BF F5 83            [12]  788 	mov	dph,a
      0053C1 E4               [12]  789 	clr	a
      0053C2 F0               [24]  790 	movx	@dptr,a
                                    791 ;	keyboards/ajazz/ak820/matrix.c:49: for (i = 0; i < MATRIX_ROWS; ++i) {
      0053C3 0F               [12]  792 	inc	r7
      0053C4 BF 10 00         [24]  793 	cjne	r7,#0x10,00121$
      0053C7                        794 00121$:
      0053C7 40 E2            [24]  795 	jc	00102$
                                    796 ;	keyboards/ajazz/ak820/matrix.c:53: debounce_init(MATRIX_ROWS);
      0053C9 75 82 10         [24]  797 	mov	dpl, #0x10
      0053CC 12 7A FD         [24]  798 	lcall	_debounce_init
                                    799 ;	keyboards/ajazz/ak820/matrix.c:54: matrix_init_custom();
                                    800 ;	keyboards/ajazz/ak820/matrix.c:55: matrix_init_kb();
                                    801 ;	keyboards/ajazz/ak820/matrix.c:56: }
      0053CF 02 53 82         [24]  802 	ljmp	_matrix_init_custom
                                    803 ;------------------------------------------------------------
                                    804 ;Allocation info for local variables in function 'matrix_scan'
                                    805 ;------------------------------------------------------------
                                    806 ;changed       Allocated with name '_matrix_scan_changed_10000_110'
                                    807 ;------------------------------------------------------------
                                    808 ;	keyboards/ajazz/ak820/matrix.c:58: uint8_t matrix_scan(void) {
                                    809 ;	-----------------------------------------
                                    810 ;	 function matrix_scan
                                    811 ;	-----------------------------------------
      0053D2                        812 _matrix_scan:
                                    813 ;	keyboards/ajazz/ak820/matrix.c:59: bool changed = matrix_scan_custom(raw_matrix);
      0053D2 90 06 60         [24]  814 	mov	dptr,#_raw_matrix
      0053D5 75 F0 00         [24]  815 	mov	b, #0x00
      0053D8 12 53 85         [24]  816 	lcall	_matrix_scan_custom
      0053DB AF 82            [24]  817 	mov	r7, dpl
                                    818 ;	keyboards/ajazz/ak820/matrix.c:60: changed = debounce(raw_matrix, matrix, MATRIX_ROWS, changed);
      0053DD 90 08 CE         [24]  819 	mov	dptr,#_debounce_PARM_2
      0053E0 74 70            [12]  820 	mov	a,#_matrix
      0053E2 F0               [24]  821 	movx	@dptr,a
      0053E3 74 06            [12]  822 	mov	a,#(_matrix >> 8)
      0053E5 A3               [24]  823 	inc	dptr
      0053E6 F0               [24]  824 	movx	@dptr,a
      0053E7 E4               [12]  825 	clr	a
      0053E8 A3               [24]  826 	inc	dptr
      0053E9 F0               [24]  827 	movx	@dptr,a
      0053EA 90 08 D1         [24]  828 	mov	dptr,#_debounce_PARM_3
      0053ED 74 10            [12]  829 	mov	a,#0x10
      0053EF F0               [24]  830 	movx	@dptr,a
      0053F0 90 08 D2         [24]  831 	mov	dptr,#_debounce_PARM_4
      0053F3 EF               [12]  832 	mov	a,r7
      0053F4 F0               [24]  833 	movx	@dptr,a
      0053F5 90 06 60         [24]  834 	mov	dptr,#_raw_matrix
      0053F8 75 F0 00         [24]  835 	mov	b, #0x00
                                    836 ;	keyboards/ajazz/ak820/matrix.c:62: return changed;
                                    837 ;	keyboards/ajazz/ak820/matrix.c:63: }
      0053FB 02 7A FE         [24]  838 	ljmp	_debounce
                                    839 ;------------------------------------------------------------
                                    840 ;Allocation info for local variables in function 'matrix_output_select_delay'
                                    841 ;------------------------------------------------------------
                                    842 ;	keyboards/ajazz/ak820/matrix.c:66: void matrix_output_select_delay(void) {}
                                    843 ;	-----------------------------------------
                                    844 ;	 function matrix_print
                                    845 ;	-----------------------------------------
      0053FE                        846 _matrix_print:
      0053FE 22               [24]  847 	ret
                                    848 	.area CSEG    (CODE)
                                    849 	.area CONST   (CODE)
                                    850 	.area XINIT   (CODE)
                                    851 	.area CABS    (ABS,CODE)
