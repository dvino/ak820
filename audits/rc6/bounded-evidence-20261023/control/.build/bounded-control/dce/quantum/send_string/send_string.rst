                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module send_string
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _ascii_to_keycode_lut
                                     12 	.globl _ascii_to_dead_lut
                                     13 	.globl _ascii_to_altgr_lut
                                     14 	.globl _ascii_to_shift_lut
                                     15 	.globl _tap_code
                                     16 	.globl _unregister_code
                                     17 	.globl _register_code
                                     18 	.globl _mDelaymS
                                     19 	.globl _rand
                                     20 	.globl _ADC_START
                                     21 	.globl _S0_R_FIFO
                                     22 	.globl _S0_T_FIFO
                                     23 	.globl _S0_FREE
                                     24 	.globl _S0_IF_BYTE
                                     25 	.globl _S0_IF_FIRST
                                     26 	.globl _S0_IF_OV
                                     27 	.globl _S0_FST_ACT
                                     28 	.globl _CP_RL2
                                     29 	.globl _C_T2
                                     30 	.globl _TR2
                                     31 	.globl _EXEN2
                                     32 	.globl _TCLK
                                     33 	.globl _RCLK
                                     34 	.globl _EXF2
                                     35 	.globl _CAP1F
                                     36 	.globl _TF2
                                     37 	.globl _RI
                                     38 	.globl _TI
                                     39 	.globl _RB8
                                     40 	.globl _TB8
                                     41 	.globl _REN
                                     42 	.globl _SM2
                                     43 	.globl _SM1
                                     44 	.globl _SM0
                                     45 	.globl _IT0
                                     46 	.globl _IE0
                                     47 	.globl _IT1
                                     48 	.globl _IE1
                                     49 	.globl _TR0
                                     50 	.globl _TF0
                                     51 	.globl _TR1
                                     52 	.globl _TF1
                                     53 	.globl _P4_0
                                     54 	.globl _P4_1
                                     55 	.globl _P4_2
                                     56 	.globl _P4_3
                                     57 	.globl _P4_4
                                     58 	.globl _P4_5
                                     59 	.globl _P4_6
                                     60 	.globl _RXD
                                     61 	.globl _TXD
                                     62 	.globl _INT0
                                     63 	.globl _INT1
                                     64 	.globl _T0
                                     65 	.globl _T1
                                     66 	.globl _MOSI1
                                     67 	.globl _MISO1
                                     68 	.globl _SCK1
                                     69 	.globl _P3_0
                                     70 	.globl _P3_1
                                     71 	.globl _P3_2
                                     72 	.globl _P3_3
                                     73 	.globl _P3_4
                                     74 	.globl _P3_5
                                     75 	.globl _P3_6
                                     76 	.globl _P3_7
                                     77 	.globl _CAP1_
                                     78 	.globl _T2_
                                     79 	.globl _CAP2_
                                     80 	.globl _T2EX_
                                     81 	.globl _RXD1
                                     82 	.globl _TXD1
                                     83 	.globl _P2_0
                                     84 	.globl _P2_1
                                     85 	.globl _P2_2
                                     86 	.globl _P2_3
                                     87 	.globl _P2_4
                                     88 	.globl _P2_5
                                     89 	.globl _P2_6
                                     90 	.globl _P2_7
                                     91 	.globl _AIN0
                                     92 	.globl _AIN1
                                     93 	.globl _AIN2
                                     94 	.globl _AIN3
                                     95 	.globl _AIN4
                                     96 	.globl _AIN5
                                     97 	.globl _AIN6
                                     98 	.globl _AIN7
                                     99 	.globl _CAP1
                                    100 	.globl _T2
                                    101 	.globl _CAP2
                                    102 	.globl _T2EX
                                    103 	.globl _INT0_
                                    104 	.globl _SCS
                                    105 	.globl _MOSI
                                    106 	.globl _MISO
                                    107 	.globl _SCK
                                    108 	.globl _RXD1_
                                    109 	.globl _TXD1_
                                    110 	.globl _P1_0
                                    111 	.globl _P1_1
                                    112 	.globl _P1_2
                                    113 	.globl _P1_3
                                    114 	.globl _P1_4
                                    115 	.globl _P1_5
                                    116 	.globl _P1_6
                                    117 	.globl _P1_7
                                    118 	.globl _AIN8
                                    119 	.globl _AIN9
                                    120 	.globl _AIN10
                                    121 	.globl _AIN11
                                    122 	.globl _AIN12
                                    123 	.globl _AIN13
                                    124 	.globl _RXD_
                                    125 	.globl _TXD_
                                    126 	.globl _SCL0
                                    127 	.globl _SDA0
                                    128 	.globl _P0_0
                                    129 	.globl _P0_1
                                    130 	.globl _P0_2
                                    131 	.globl _P0_3
                                    132 	.globl _P0_4
                                    133 	.globl _P0_5
                                    134 	.globl _P0_6
                                    135 	.globl _P0_7
                                    136 	.globl _IE_SPI0
                                    137 	.globl _IE_USB
                                    138 	.globl _IE_ADC
                                    139 	.globl _IE_UART1
                                    140 	.globl _IE_PWM_I2C
                                    141 	.globl _IE_GPIO
                                    142 	.globl _IE_WDOG
                                    143 	.globl _PX0
                                    144 	.globl _PT0
                                    145 	.globl _PX1
                                    146 	.globl _PT1
                                    147 	.globl _PS
                                    148 	.globl _PT2
                                    149 	.globl _PL_FLAG
                                    150 	.globl _PH_FLAG
                                    151 	.globl _EX0
                                    152 	.globl _ET0
                                    153 	.globl _EX1
                                    154 	.globl _ET1
                                    155 	.globl _ES
                                    156 	.globl _ET2
                                    157 	.globl _E_DIS
                                    158 	.globl _EA
                                    159 	.globl _P
                                    160 	.globl _F1
                                    161 	.globl _OV
                                    162 	.globl _RS0
                                    163 	.globl _RS1
                                    164 	.globl _F0
                                    165 	.globl _AC
                                    166 	.globl _CY
                                    167 	.globl _I2CS_INT_ST
                                    168 	.globl _I2CX_INT
                                    169 	.globl _LED_STATUS
                                    170 	.globl _LED_DMA_H
                                    171 	.globl _LED_DMA_L
                                    172 	.globl _LED_DMA
                                    173 	.globl _LED_PWM_OE
                                    174 	.globl _LED_COMMON
                                    175 	.globl _ADC_CHAN
                                    176 	.globl _ADC_DAT_H
                                    177 	.globl _ADC_DAT_L
                                    178 	.globl _ADC_DAT
                                    179 	.globl _ADC_CTRL
                                    180 	.globl _SPI1_CK_SE
                                    181 	.globl _SPI1_CTRL
                                    182 	.globl _SPI1_DATA
                                    183 	.globl _SPI1_STAT
                                    184 	.globl _SIF1
                                    185 	.globl _SBAUD1
                                    186 	.globl _SBUF1
                                    187 	.globl _SCON1
                                    188 	.globl _SPI0_SETUP
                                    189 	.globl _SPI0_CK_SE
                                    190 	.globl _SPI0_CTRL
                                    191 	.globl _SPI0_DATA
                                    192 	.globl _SPI0_STAT
                                    193 	.globl _T2CAP1H
                                    194 	.globl _T2CAP1L
                                    195 	.globl _T2CAP1
                                    196 	.globl _TH2
                                    197 	.globl _TL2
                                    198 	.globl _T2COUNT
                                    199 	.globl _RCAP2H
                                    200 	.globl _RCAP2L
                                    201 	.globl _RCAP2
                                    202 	.globl _T2MOD
                                    203 	.globl _T2CON
                                    204 	.globl _SBUF
                                    205 	.globl _SCON
                                    206 	.globl _TH1
                                    207 	.globl _TH0
                                    208 	.globl _TL1
                                    209 	.globl _TL0
                                    210 	.globl _TMOD
                                    211 	.globl _TCON
                                    212 	.globl _XBUS_AUX
                                    213 	.globl _P7
                                    214 	.globl _P6_DIR
                                    215 	.globl _P6_OUT_PU
                                    216 	.globl _P6_IN
                                    217 	.globl _P5_DIR
                                    218 	.globl _P5_OUT_PU
                                    219 	.globl _P5_IN
                                    220 	.globl _P4_LED_KEY
                                    221 	.globl _P4_DIR_PU
                                    222 	.globl _P4_MOD_OC
                                    223 	.globl _P4
                                    224 	.globl _P3_DIR_PU
                                    225 	.globl _P3_MOD_OC
                                    226 	.globl _P3
                                    227 	.globl _P2_DIR_PU
                                    228 	.globl _P2_MOD_OC
                                    229 	.globl _P2
                                    230 	.globl _P1_DIR_PU
                                    231 	.globl _P1_MOD_OC
                                    232 	.globl _P1
                                    233 	.globl _P0_DIR_PU
                                    234 	.globl _P0_MOD_OC
                                    235 	.globl _P0
                                    236 	.globl _ROM_CTRL
                                    237 	.globl _ROM_DATA_HH
                                    238 	.globl _ROM_DATA_HL
                                    239 	.globl _ROM_DATA_HI
                                    240 	.globl _ROM_ADDR_H
                                    241 	.globl _ROM_ADDR_L
                                    242 	.globl _ROM_ADDR
                                    243 	.globl _GPIO_IE
                                    244 	.globl _IP_EX
                                    245 	.globl _IE_EX
                                    246 	.globl _IP
                                    247 	.globl _IE
                                    248 	.globl _WDOG_COUNT
                                    249 	.globl _RESET_KEEP
                                    250 	.globl _WAKE_CTRL
                                    251 	.globl _CLOCK_CFG
                                    252 	.globl _POWER_CFG
                                    253 	.globl _PCON
                                    254 	.globl _GLOBAL_CFG
                                    255 	.globl _SAFE_MOD
                                    256 	.globl _DPH
                                    257 	.globl _DPL
                                    258 	.globl _SP
                                    259 	.globl _A_INV
                                    260 	.globl _B
                                    261 	.globl _ACC
                                    262 	.globl _PSW
                                    263 	.globl _send_char
                                    264 ;--------------------------------------------------------
                                    265 ; special function registers
                                    266 ;--------------------------------------------------------
                                    267 	.area RSEG    (ABS,DATA)
      000000                        268 	.org 0x0000
                           0000D0   269 _PSW	=	0x00d0
                           0000E0   270 _ACC	=	0x00e0
                           0000F0   271 _B	=	0x00f0
                           0000FD   272 _A_INV	=	0x00fd
                           000081   273 _SP	=	0x0081
                           000082   274 _DPL	=	0x0082
                           000083   275 _DPH	=	0x0083
                           0000A1   276 _SAFE_MOD	=	0x00a1
                           0000B1   277 _GLOBAL_CFG	=	0x00b1
                           000087   278 _PCON	=	0x0087
                           0000BA   279 _POWER_CFG	=	0x00ba
                           0000B9   280 _CLOCK_CFG	=	0x00b9
                           0000A9   281 _WAKE_CTRL	=	0x00a9
                           0000FE   282 _RESET_KEEP	=	0x00fe
                           0000FF   283 _WDOG_COUNT	=	0x00ff
                           0000A8   284 _IE	=	0x00a8
                           0000B8   285 _IP	=	0x00b8
                           0000E8   286 _IE_EX	=	0x00e8
                           0000E9   287 _IP_EX	=	0x00e9
                           0000B2   288 _GPIO_IE	=	0x00b2
                           008584   289 _ROM_ADDR	=	0x8584
                           000084   290 _ROM_ADDR_L	=	0x0084
                           000085   291 _ROM_ADDR_H	=	0x0085
                           008F8E   292 _ROM_DATA_HI	=	0x8f8e
                           00008E   293 _ROM_DATA_HL	=	0x008e
                           00008F   294 _ROM_DATA_HH	=	0x008f
                           000086   295 _ROM_CTRL	=	0x0086
                           000080   296 _P0	=	0x0080
                           0000C4   297 _P0_MOD_OC	=	0x00c4
                           0000C5   298 _P0_DIR_PU	=	0x00c5
                           000090   299 _P1	=	0x0090
                           000092   300 _P1_MOD_OC	=	0x0092
                           000093   301 _P1_DIR_PU	=	0x0093
                           0000A0   302 _P2	=	0x00a0
                           000094   303 _P2_MOD_OC	=	0x0094
                           000095   304 _P2_DIR_PU	=	0x0095
                           0000B0   305 _P3	=	0x00b0
                           000096   306 _P3_MOD_OC	=	0x0096
                           000097   307 _P3_DIR_PU	=	0x0097
                           0000C0   308 _P4	=	0x00c0
                           0000C2   309 _P4_MOD_OC	=	0x00c2
                           0000C3   310 _P4_DIR_PU	=	0x00c3
                           0000C1   311 _P4_LED_KEY	=	0x00c1
                           0000AA   312 _P5_IN	=	0x00aa
                           0000AB   313 _P5_OUT_PU	=	0x00ab
                           0000AC   314 _P5_DIR	=	0x00ac
                           0000AD   315 _P6_IN	=	0x00ad
                           0000AE   316 _P6_OUT_PU	=	0x00ae
                           0000AF   317 _P6_DIR	=	0x00af
                           0000F1   318 _P7	=	0x00f1
                           0000A2   319 _XBUS_AUX	=	0x00a2
                           000088   320 _TCON	=	0x0088
                           000089   321 _TMOD	=	0x0089
                           00008A   322 _TL0	=	0x008a
                           00008B   323 _TL1	=	0x008b
                           00008C   324 _TH0	=	0x008c
                           00008D   325 _TH1	=	0x008d
                           000098   326 _SCON	=	0x0098
                           000099   327 _SBUF	=	0x0099
                           0000C8   328 _T2CON	=	0x00c8
                           0000C9   329 _T2MOD	=	0x00c9
                           00CBCA   330 _RCAP2	=	0xcbca
                           0000CA   331 _RCAP2L	=	0x00ca
                           0000CB   332 _RCAP2H	=	0x00cb
                           00CDCC   333 _T2COUNT	=	0xcdcc
                           0000CC   334 _TL2	=	0x00cc
                           0000CD   335 _TH2	=	0x00cd
                           00CFCE   336 _T2CAP1	=	0xcfce
                           0000CE   337 _T2CAP1L	=	0x00ce
                           0000CF   338 _T2CAP1H	=	0x00cf
                           0000F8   339 _SPI0_STAT	=	0x00f8
                           0000F9   340 _SPI0_DATA	=	0x00f9
                           0000FA   341 _SPI0_CTRL	=	0x00fa
                           0000FB   342 _SPI0_CK_SE	=	0x00fb
                           0000FC   343 _SPI0_SETUP	=	0x00fc
                           0000BC   344 _SCON1	=	0x00bc
                           0000BD   345 _SBUF1	=	0x00bd
                           0000BE   346 _SBAUD1	=	0x00be
                           0000BF   347 _SIF1	=	0x00bf
                           0000B4   348 _SPI1_STAT	=	0x00b4
                           0000B5   349 _SPI1_DATA	=	0x00b5
                           0000B6   350 _SPI1_CTRL	=	0x00b6
                           0000B7   351 _SPI1_CK_SE	=	0x00b7
                           0000F3   352 _ADC_CTRL	=	0x00f3
                           00F5F4   353 _ADC_DAT	=	0xf5f4
                           0000F4   354 _ADC_DAT_L	=	0x00f4
                           0000F5   355 _ADC_DAT_H	=	0x00f5
                           0000F6   356 _ADC_CHAN	=	0x00f6
                           0000A6   357 _LED_COMMON	=	0x00a6
                           0000A7   358 _LED_PWM_OE	=	0x00a7
                           00C7C6   359 _LED_DMA	=	0xc7c6
                           0000C6   360 _LED_DMA_L	=	0x00c6
                           0000C7   361 _LED_DMA_H	=	0x00c7
                           0000F7   362 _LED_STATUS	=	0x00f7
                           0000B3   363 _I2CX_INT	=	0x00b3
                           0000BB   364 _I2CS_INT_ST	=	0x00bb
                                    365 ;--------------------------------------------------------
                                    366 ; special function bits
                                    367 ;--------------------------------------------------------
                                    368 	.area RSEG    (ABS,DATA)
      000000                        369 	.org 0x0000
                           0000D7   370 _CY	=	0x00d7
                           0000D6   371 _AC	=	0x00d6
                           0000D5   372 _F0	=	0x00d5
                           0000D4   373 _RS1	=	0x00d4
                           0000D3   374 _RS0	=	0x00d3
                           0000D2   375 _OV	=	0x00d2
                           0000D1   376 _F1	=	0x00d1
                           0000D0   377 _P	=	0x00d0
                           0000AF   378 _EA	=	0x00af
                           0000AE   379 _E_DIS	=	0x00ae
                           0000AD   380 _ET2	=	0x00ad
                           0000AC   381 _ES	=	0x00ac
                           0000AB   382 _ET1	=	0x00ab
                           0000AA   383 _EX1	=	0x00aa
                           0000A9   384 _ET0	=	0x00a9
                           0000A8   385 _EX0	=	0x00a8
                           0000BF   386 _PH_FLAG	=	0x00bf
                           0000BE   387 _PL_FLAG	=	0x00be
                           0000BD   388 _PT2	=	0x00bd
                           0000BC   389 _PS	=	0x00bc
                           0000BB   390 _PT1	=	0x00bb
                           0000BA   391 _PX1	=	0x00ba
                           0000B9   392 _PT0	=	0x00b9
                           0000B8   393 _PX0	=	0x00b8
                           0000EF   394 _IE_WDOG	=	0x00ef
                           0000EE   395 _IE_GPIO	=	0x00ee
                           0000ED   396 _IE_PWM_I2C	=	0x00ed
                           0000EC   397 _IE_UART1	=	0x00ec
                           0000EB   398 _IE_ADC	=	0x00eb
                           0000E9   399 _IE_USB	=	0x00e9
                           0000E8   400 _IE_SPI0	=	0x00e8
                           000087   401 _P0_7	=	0x0087
                           000086   402 _P0_6	=	0x0086
                           000085   403 _P0_5	=	0x0085
                           000084   404 _P0_4	=	0x0084
                           000083   405 _P0_3	=	0x0083
                           000082   406 _P0_2	=	0x0082
                           000081   407 _P0_1	=	0x0081
                           000080   408 _P0_0	=	0x0080
                           000081   409 _SDA0	=	0x0081
                           000080   410 _SCL0	=	0x0080
                           000083   411 _TXD_	=	0x0083
                           000082   412 _RXD_	=	0x0082
                           000085   413 _AIN13	=	0x0085
                           000084   414 _AIN12	=	0x0084
                           000083   415 _AIN11	=	0x0083
                           000082   416 _AIN10	=	0x0082
                           000081   417 _AIN9	=	0x0081
                           000080   418 _AIN8	=	0x0080
                           000097   419 _P1_7	=	0x0097
                           000096   420 _P1_6	=	0x0096
                           000095   421 _P1_5	=	0x0095
                           000094   422 _P1_4	=	0x0094
                           000093   423 _P1_3	=	0x0093
                           000092   424 _P1_2	=	0x0092
                           000091   425 _P1_1	=	0x0091
                           000090   426 _P1_0	=	0x0090
                           000097   427 _TXD1_	=	0x0097
                           000096   428 _RXD1_	=	0x0096
                           000097   429 _SCK	=	0x0097
                           000096   430 _MISO	=	0x0096
                           000095   431 _MOSI	=	0x0095
                           000094   432 _SCS	=	0x0094
                           000092   433 _INT0_	=	0x0092
                           000091   434 _T2EX	=	0x0091
                           000091   435 _CAP2	=	0x0091
                           000090   436 _T2	=	0x0090
                           000090   437 _CAP1	=	0x0090
                           000097   438 _AIN7	=	0x0097
                           000096   439 _AIN6	=	0x0096
                           000095   440 _AIN5	=	0x0095
                           000094   441 _AIN4	=	0x0094
                           000093   442 _AIN3	=	0x0093
                           000092   443 _AIN2	=	0x0092
                           000091   444 _AIN1	=	0x0091
                           000090   445 _AIN0	=	0x0090
                           0000A7   446 _P2_7	=	0x00a7
                           0000A6   447 _P2_6	=	0x00a6
                           0000A5   448 _P2_5	=	0x00a5
                           0000A4   449 _P2_4	=	0x00a4
                           0000A3   450 _P2_3	=	0x00a3
                           0000A2   451 _P2_2	=	0x00a2
                           0000A1   452 _P2_1	=	0x00a1
                           0000A0   453 _P2_0	=	0x00a0
                           0000A7   454 _TXD1	=	0x00a7
                           0000A6   455 _RXD1	=	0x00a6
                           0000A5   456 _T2EX_	=	0x00a5
                           0000A5   457 _CAP2_	=	0x00a5
                           0000A4   458 _T2_	=	0x00a4
                           0000A4   459 _CAP1_	=	0x00a4
                           0000B7   460 _P3_7	=	0x00b7
                           0000B6   461 _P3_6	=	0x00b6
                           0000B5   462 _P3_5	=	0x00b5
                           0000B4   463 _P3_4	=	0x00b4
                           0000B3   464 _P3_3	=	0x00b3
                           0000B2   465 _P3_2	=	0x00b2
                           0000B1   466 _P3_1	=	0x00b1
                           0000B0   467 _P3_0	=	0x00b0
                           0000B7   468 _SCK1	=	0x00b7
                           0000B6   469 _MISO1	=	0x00b6
                           0000B5   470 _MOSI1	=	0x00b5
                           0000B5   471 _T1	=	0x00b5
                           0000B4   472 _T0	=	0x00b4
                           0000B3   473 _INT1	=	0x00b3
                           0000B2   474 _INT0	=	0x00b2
                           0000B1   475 _TXD	=	0x00b1
                           0000B0   476 _RXD	=	0x00b0
                           0000C6   477 _P4_6	=	0x00c6
                           0000C5   478 _P4_5	=	0x00c5
                           0000C4   479 _P4_4	=	0x00c4
                           0000C3   480 _P4_3	=	0x00c3
                           0000C2   481 _P4_2	=	0x00c2
                           0000C1   482 _P4_1	=	0x00c1
                           0000C0   483 _P4_0	=	0x00c0
                           00008F   484 _TF1	=	0x008f
                           00008E   485 _TR1	=	0x008e
                           00008D   486 _TF0	=	0x008d
                           00008C   487 _TR0	=	0x008c
                           00008B   488 _IE1	=	0x008b
                           00008A   489 _IT1	=	0x008a
                           000089   490 _IE0	=	0x0089
                           000088   491 _IT0	=	0x0088
                           00009F   492 _SM0	=	0x009f
                           00009E   493 _SM1	=	0x009e
                           00009D   494 _SM2	=	0x009d
                           00009C   495 _REN	=	0x009c
                           00009B   496 _TB8	=	0x009b
                           00009A   497 _RB8	=	0x009a
                           000099   498 _TI	=	0x0099
                           000098   499 _RI	=	0x0098
                           0000CF   500 _TF2	=	0x00cf
                           0000CF   501 _CAP1F	=	0x00cf
                           0000CE   502 _EXF2	=	0x00ce
                           0000CD   503 _RCLK	=	0x00cd
                           0000CC   504 _TCLK	=	0x00cc
                           0000CB   505 _EXEN2	=	0x00cb
                           0000CA   506 _TR2	=	0x00ca
                           0000C9   507 _C_T2	=	0x00c9
                           0000C8   508 _CP_RL2	=	0x00c8
                           0000FF   509 _S0_FST_ACT	=	0x00ff
                           0000FE   510 _S0_IF_OV	=	0x00fe
                           0000FD   511 _S0_IF_FIRST	=	0x00fd
                           0000FC   512 _S0_IF_BYTE	=	0x00fc
                           0000FB   513 _S0_FREE	=	0x00fb
                           0000FA   514 _S0_T_FIFO	=	0x00fa
                           0000F8   515 _S0_R_FIFO	=	0x00f8
                           0000F7   516 _ADC_START	=	0x00f7
                                    517 ;--------------------------------------------------------
                                    518 ; overlayable register banks
                                    519 ;--------------------------------------------------------
                                    520 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        521 	.ds 8
                                    522 ;--------------------------------------------------------
                                    523 ; internal ram data
                                    524 ;--------------------------------------------------------
                                    525 	.area DSEG    (DATA)
      00001D                        526 _send_char_sloc0_1_0:
      00001D                        527 	.ds 1
      00001E                        528 _send_char_sloc1_1_0:
      00001E                        529 	.ds 1
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
                                    546 ;--------------------------------------------------------
                                    547 ; paged external ram data
                                    548 ;--------------------------------------------------------
                                    549 	.area PSEG    (PAG,XDATA)
                                    550 ;--------------------------------------------------------
                                    551 ; uninitialized external ram data
                                    552 ;--------------------------------------------------------
                                    553 	.area XSEG    (XDATA)
      000A45                        554 _send_char_ascii_code_10000_240:
      000A45                        555 	.ds 1
                                    556 ;--------------------------------------------------------
                                    557 ; absolute external ram data
                                    558 ;--------------------------------------------------------
                                    559 	.area XABS    (ABS,XDATA)
                                    560 ;--------------------------------------------------------
                                    561 ; initialized external ram data
                                    562 ;--------------------------------------------------------
                                    563 	.area XISEG   (XDATA)
                                    564 	.area HOME    (CODE)
                                    565 	.area GSINIT0 (CODE)
                                    566 	.area GSINIT1 (CODE)
                                    567 	.area GSINIT2 (CODE)
                                    568 	.area GSINIT3 (CODE)
                                    569 	.area GSINIT4 (CODE)
                                    570 	.area GSINIT5 (CODE)
                                    571 	.area GSINIT  (CODE)
                                    572 	.area GSFINAL (CODE)
                                    573 	.area CSEG    (CODE)
                                    574 ;--------------------------------------------------------
                                    575 ; global & static initialisations
                                    576 ;--------------------------------------------------------
                                    577 	.area HOME    (CODE)
                                    578 	.area GSINIT  (CODE)
                                    579 	.area GSFINAL (CODE)
                                    580 	.area GSINIT  (CODE)
                                    581 ;--------------------------------------------------------
                                    582 ; Home
                                    583 ;--------------------------------------------------------
                                    584 	.area HOME    (CODE)
                                    585 	.area HOME    (CODE)
                                    586 ;--------------------------------------------------------
                                    587 ; code
                                    588 ;--------------------------------------------------------
                                    589 	.area CSEG    (CODE)
                                    590 ;------------------------------------------------------------
                                    591 ;Allocation info for local variables in function 'send_string'
                                    592 ;------------------------------------------------------------
                                    593 ;string        Allocated with name '_send_string_string_10000_212'
                                    594 ;------------------------------------------------------------
                                    595 ;	quantum/send_string/send_string.c:155: void send_string(const char *string) {
                                    596 ;	-----------------------------------------
                           000007   597 	ar7 = 0x07
                           000006   598 	ar6 = 0x06
                           000005   599 	ar5 = 0x05
                           000004   600 	ar4 = 0x04
                           000003   601 	ar3 = 0x03
                           000002   602 	ar2 = 0x02
                           000001   603 	ar1 = 0x01
                           000000   604 	ar0 = 0x00
                                    605 ;	 function send_char
                                    606 ;	-----------------------------------------
      009F92                        607 _send_char:
      009F92 E5 82            [12]  608 	mov	a,dpl
      009F94 90 0A 45         [24]  609 	mov	dptr,#_send_char_ascii_code_10000_240
      009F97 F0               [24]  610 	movx	@dptr,a
                                    611 ;	quantum/send_string/send_string.c:210: uint8_t keycode    = pgm_read_byte(&ascii_to_keycode_lut[(uint8_t)ascii_code]);
      009F98 E0               [24]  612 	movx	a,@dptr
      009F99 FF               [12]  613 	mov	r7,a
      009F9A 90 B9 AD         [24]  614 	mov	dptr,#_ascii_to_keycode_lut
      009F9D 93               [24]  615 	movc	a,@a+dptr
      009F9E FE               [12]  616 	mov	r6,a
                                    617 ;	quantum/send_string/send_string.c:211: bool    is_shifted = PGM_LOADBIT(ascii_to_shift_lut, (uint8_t)ascii_code);
      009F9F EF               [12]  618 	mov	a,r7
      009FA0 C4               [12]  619 	swap	a
      009FA1 23               [12]  620 	rl	a
      009FA2 54 1F            [12]  621 	anl	a,#0x1f
      009FA4 FD               [12]  622 	mov	r5,a
      009FA5 90 B9 7D         [24]  623 	mov	dptr,#_ascii_to_shift_lut
      009FA8 93               [24]  624 	movc	a,@a+dptr
      009FA9 FC               [12]  625 	mov	r4,a
      009FAA 53 07 07         [24]  626 	anl	ar7,#0x07
      009FAD 8F F0            [24]  627 	mov	b,r7
      009FAF 05 F0            [12]  628 	inc	b
      009FB1 EC               [12]  629 	mov	a,r4
      009FB2 80 02            [24]  630 	sjmp	00149$
      009FB4                        631 00148$:
      009FB4 C3               [12]  632 	clr	c
      009FB5 13               [12]  633 	rrc	a
      009FB6                        634 00149$:
      009FB6 D5 F0 FB         [24]  635 	djnz	b,00148$
      009FB9 54 01            [12]  636 	anl	a,#0x01
      009FBB F5 1D            [12]  637 	mov	_send_char_sloc0_1_0,a
                                    638 ;	quantum/send_string/send_string.c:212: bool    is_altgred = PGM_LOADBIT(ascii_to_altgr_lut, (uint8_t)ascii_code);
      009FBD ED               [12]  639 	mov	a,r5
      009FBE 90 B9 8D         [24]  640 	mov	dptr,#_ascii_to_altgr_lut
      009FC1 93               [24]  641 	movc	a,@a+dptr
      009FC2 FC               [12]  642 	mov	r4,a
      009FC3 8F F0            [24]  643 	mov	b,r7
      009FC5 05 F0            [12]  644 	inc	b
      009FC7 EC               [12]  645 	mov	a,r4
      009FC8 80 02            [24]  646 	sjmp	00151$
      009FCA                        647 00150$:
      009FCA C3               [12]  648 	clr	c
      009FCB 13               [12]  649 	rrc	a
      009FCC                        650 00151$:
      009FCC D5 F0 FB         [24]  651 	djnz	b,00150$
      009FCF 54 01            [12]  652 	anl	a,#0x01
      009FD1 F5 1E            [12]  653 	mov	_send_char_sloc1_1_0,a
                                    654 ;	quantum/send_string/send_string.c:213: bool    is_dead    = PGM_LOADBIT(ascii_to_dead_lut, (uint8_t)ascii_code);
      009FD3 ED               [12]  655 	mov	a,r5
      009FD4 90 B9 9D         [24]  656 	mov	dptr,#_ascii_to_dead_lut
      009FD7 93               [24]  657 	movc	a,@a+dptr
      009FD8 FD               [12]  658 	mov	r5,a
      009FD9 8F F0            [24]  659 	mov	b,r7
      009FDB 05 F0            [12]  660 	inc	b
      009FDD ED               [12]  661 	mov	a,r5
      009FDE 80 02            [24]  662 	sjmp	00153$
      009FE0                        663 00152$:
      009FE0 C3               [12]  664 	clr	c
      009FE1 13               [12]  665 	rrc	a
      009FE2                        666 00153$:
      009FE2 D5 F0 FB         [24]  667 	djnz	b,00152$
      009FE5 54 01            [12]  668 	anl	a,#0x01
      009FE7 FF               [12]  669 	mov	r7,a
                                    670 ;	quantum/send_string/send_string.c:215: if (is_shifted) {
      009FE8 E5 1D            [12]  671 	mov	a,_send_char_sloc0_1_0
      009FEA 60 0E            [24]  672 	jz	00102$
                                    673 ;	quantum/send_string/send_string.c:216: register_code(KC_LEFT_SHIFT);
      009FEC 75 82 E1         [24]  674 	mov	dpl, #0xe1
      009FEF C0 07            [24]  675 	push	ar7
      009FF1 C0 06            [24]  676 	push	ar6
      009FF3 12 71 9F         [24]  677 	lcall	_register_code
      009FF6 D0 06            [24]  678 	pop	ar6
      009FF8 D0 07            [24]  679 	pop	ar7
      009FFA                        680 00102$:
                                    681 ;	quantum/send_string/send_string.c:218: if (is_altgred) {
      009FFA E5 1E            [12]  682 	mov	a,_send_char_sloc1_1_0
      009FFC 60 0E            [24]  683 	jz	00104$
                                    684 ;	quantum/send_string/send_string.c:219: register_code(KC_RIGHT_ALT);
      009FFE 75 82 E6         [24]  685 	mov	dpl, #0xe6
      00A001 C0 07            [24]  686 	push	ar7
      00A003 C0 06            [24]  687 	push	ar6
      00A005 12 71 9F         [24]  688 	lcall	_register_code
      00A008 D0 06            [24]  689 	pop	ar6
      00A00A D0 07            [24]  690 	pop	ar7
      00A00C                        691 00104$:
                                    692 ;	quantum/send_string/send_string.c:221: tap_code(keycode);
      00A00C 8E 82            [24]  693 	mov	dpl, r6
      00A00E C0 07            [24]  694 	push	ar7
      00A010 12 73 26         [24]  695 	lcall	_tap_code
      00A013 D0 07            [24]  696 	pop	ar7
                                    697 ;	quantum/send_string/send_string.c:222: if (is_altgred) {
      00A015 E5 1E            [12]  698 	mov	a,_send_char_sloc1_1_0
      00A017 60 0A            [24]  699 	jz	00106$
                                    700 ;	quantum/send_string/send_string.c:223: unregister_code(KC_RIGHT_ALT);
      00A019 75 82 E6         [24]  701 	mov	dpl, #0xe6
      00A01C C0 07            [24]  702 	push	ar7
      00A01E 12 72 7F         [24]  703 	lcall	_unregister_code
      00A021 D0 07            [24]  704 	pop	ar7
      00A023                        705 00106$:
                                    706 ;	quantum/send_string/send_string.c:225: if (is_shifted) {
      00A023 E5 1D            [12]  707 	mov	a,_send_char_sloc0_1_0
      00A025 60 0A            [24]  708 	jz	00108$
                                    709 ;	quantum/send_string/send_string.c:226: unregister_code(KC_LEFT_SHIFT);
      00A027 75 82 E1         [24]  710 	mov	dpl, #0xe1
      00A02A C0 07            [24]  711 	push	ar7
      00A02C 12 72 7F         [24]  712 	lcall	_unregister_code
      00A02F D0 07            [24]  713 	pop	ar7
      00A031                        714 00108$:
                                    715 ;	quantum/send_string/send_string.c:228: if (is_dead) {
      00A031 EF               [12]  716 	mov	a,r7
      00A032 60 06            [24]  717 	jz	00111$
                                    718 ;	quantum/send_string/send_string.c:229: tap_code(KC_SPACE);
      00A034 75 82 2C         [24]  719 	mov	dpl, #0x2c
                                    720 ;	quantum/send_string/send_string.c:231: }
      00A037 02 73 26         [24]  721 	ljmp	_tap_code
      00A03A                        722 00111$:
      00A03A 22               [24]  723 	ret
                                    724 ;------------------------------------------------------------
                                    725 ;Allocation info for local variables in function 'send_dword'
                                    726 ;------------------------------------------------------------
                                    727 ;number        Allocated with name '_send_dword_number_10000_252'
                                    728 ;------------------------------------------------------------
                                    729 ;	quantum/send_string/send_string.c:233: void send_dword(uint32_t number) {
                                    730 ;	-----------------------------------------
                                    731 	.area CSEG    (CODE)
                                    732 	.area CONST   (CODE)
                                    733 	.area CONST   (CODE)
      00B97D                        734 _ascii_to_shift_lut:
      00B97D 00                     735 	.db #0x00	; 0
      00B97E 00                     736 	.db #0x00	; 0
      00B97F 00                     737 	.db #0x00	; 0
      00B980 00                     738 	.db #0x00	; 0
      00B981 7E                     739 	.db #0x7e	; 126
      00B982 0F                     740 	.db #0x0f	; 15
      00B983 00                     741 	.db #0x00	; 0
      00B984 D4                     742 	.db #0xd4	; 212
      00B985 FF                     743 	.db #0xff	; 255
      00B986 FF                     744 	.db #0xff	; 255
      00B987 FF                     745 	.db #0xff	; 255
      00B988 C7                     746 	.db #0xc7	; 199
      00B989 00                     747 	.db #0x00	; 0
      00B98A 00                     748 	.db #0x00	; 0
      00B98B 00                     749 	.db #0x00	; 0
      00B98C 78                     750 	.db #0x78	; 120	'x'
                                    751 	.area CSEG    (CODE)
                                    752 	.area CONST   (CODE)
      00B98D                        753 _ascii_to_altgr_lut:
      00B98D 00                     754 	.db #0x00	; 0
      00B98E 00                     755 	.db #0x00	; 0
      00B98F 00                     756 	.db #0x00	; 0
      00B990 00                     757 	.db #0x00	; 0
      00B991 00                     758 	.db #0x00	; 0
      00B992 00                     759 	.db #0x00	; 0
      00B993 00                     760 	.db #0x00	; 0
      00B994 00                     761 	.db #0x00	; 0
      00B995 00                     762 	.db #0x00	; 0
      00B996 00                     763 	.db #0x00	; 0
      00B997 00                     764 	.db #0x00	; 0
      00B998 00                     765 	.db #0x00	; 0
      00B999 00                     766 	.db #0x00	; 0
      00B99A 00                     767 	.db #0x00	; 0
      00B99B 00                     768 	.db #0x00	; 0
      00B99C 00                     769 	.db #0x00	; 0
                                    770 	.area CSEG    (CODE)
                                    771 	.area CONST   (CODE)
      00B99D                        772 _ascii_to_dead_lut:
      00B99D 00                     773 	.db #0x00	; 0
      00B99E 00                     774 	.db #0x00	; 0
      00B99F 00                     775 	.db #0x00	; 0
      00B9A0 00                     776 	.db #0x00	; 0
      00B9A1 00                     777 	.db #0x00	; 0
      00B9A2 00                     778 	.db #0x00	; 0
      00B9A3 00                     779 	.db #0x00	; 0
      00B9A4 00                     780 	.db #0x00	; 0
      00B9A5 00                     781 	.db #0x00	; 0
      00B9A6 00                     782 	.db #0x00	; 0
      00B9A7 00                     783 	.db #0x00	; 0
      00B9A8 00                     784 	.db #0x00	; 0
      00B9A9 00                     785 	.db #0x00	; 0
      00B9AA 00                     786 	.db #0x00	; 0
      00B9AB 00                     787 	.db #0x00	; 0
      00B9AC 00                     788 	.db #0x00	; 0
                                    789 	.area CSEG    (CODE)
                                    790 	.area CONST   (CODE)
      00B9AD                        791 _ascii_to_keycode_lut:
      00B9AD 00                     792 	.db #0x00	; 0
      00B9AE 00                     793 	.db #0x00	; 0
      00B9AF 00                     794 	.db #0x00	; 0
      00B9B0 00                     795 	.db #0x00	; 0
      00B9B1 00                     796 	.db #0x00	; 0
      00B9B2 00                     797 	.db #0x00	; 0
      00B9B3 00                     798 	.db #0x00	; 0
      00B9B4 00                     799 	.db #0x00	; 0
      00B9B5 2A                     800 	.db #0x2a	; 42
      00B9B6 2B                     801 	.db #0x2b	; 43
      00B9B7 28                     802 	.db #0x28	; 40
      00B9B8 00                     803 	.db #0x00	; 0
      00B9B9 00                     804 	.db #0x00	; 0
      00B9BA 00                     805 	.db #0x00	; 0
      00B9BB 00                     806 	.db #0x00	; 0
      00B9BC 00                     807 	.db #0x00	; 0
      00B9BD 00                     808 	.db #0x00	; 0
      00B9BE 00                     809 	.db #0x00	; 0
      00B9BF 00                     810 	.db #0x00	; 0
      00B9C0 00                     811 	.db #0x00	; 0
      00B9C1 00                     812 	.db #0x00	; 0
      00B9C2 00                     813 	.db #0x00	; 0
      00B9C3 00                     814 	.db #0x00	; 0
      00B9C4 00                     815 	.db #0x00	; 0
      00B9C5 00                     816 	.db #0x00	; 0
      00B9C6 00                     817 	.db #0x00	; 0
      00B9C7 00                     818 	.db #0x00	; 0
      00B9C8 29                     819 	.db #0x29	; 41
      00B9C9 00                     820 	.db #0x00	; 0
      00B9CA 00                     821 	.db #0x00	; 0
      00B9CB 00                     822 	.db #0x00	; 0
      00B9CC 00                     823 	.db #0x00	; 0
      00B9CD 2C                     824 	.db #0x2c	; 44
      00B9CE 1E                     825 	.db #0x1e	; 30
      00B9CF 34                     826 	.db #0x34	; 52	'4'
      00B9D0 20                     827 	.db #0x20	; 32
      00B9D1 21                     828 	.db #0x21	; 33
      00B9D2 22                     829 	.db #0x22	; 34
      00B9D3 24                     830 	.db #0x24	; 36
      00B9D4 34                     831 	.db #0x34	; 52	'4'
      00B9D5 26                     832 	.db #0x26	; 38
      00B9D6 27                     833 	.db #0x27	; 39
      00B9D7 25                     834 	.db #0x25	; 37
      00B9D8 2E                     835 	.db #0x2e	; 46
      00B9D9 36                     836 	.db #0x36	; 54	'6'
      00B9DA 2D                     837 	.db #0x2d	; 45
      00B9DB 37                     838 	.db #0x37	; 55	'7'
      00B9DC 38                     839 	.db #0x38	; 56	'8'
      00B9DD 27                     840 	.db #0x27	; 39
      00B9DE 1E                     841 	.db #0x1e	; 30
      00B9DF 1F                     842 	.db #0x1f	; 31
      00B9E0 20                     843 	.db #0x20	; 32
      00B9E1 21                     844 	.db #0x21	; 33
      00B9E2 22                     845 	.db #0x22	; 34
      00B9E3 23                     846 	.db #0x23	; 35
      00B9E4 24                     847 	.db #0x24	; 36
      00B9E5 25                     848 	.db #0x25	; 37
      00B9E6 26                     849 	.db #0x26	; 38
      00B9E7 33                     850 	.db #0x33	; 51	'3'
      00B9E8 33                     851 	.db #0x33	; 51	'3'
      00B9E9 36                     852 	.db #0x36	; 54	'6'
      00B9EA 2E                     853 	.db #0x2e	; 46
      00B9EB 37                     854 	.db #0x37	; 55	'7'
      00B9EC 38                     855 	.db #0x38	; 56	'8'
      00B9ED 1F                     856 	.db #0x1f	; 31
      00B9EE 04                     857 	.db #0x04	; 4
      00B9EF 05                     858 	.db #0x05	; 5
      00B9F0 06                     859 	.db #0x06	; 6
      00B9F1 07                     860 	.db #0x07	; 7
      00B9F2 08                     861 	.db #0x08	; 8
      00B9F3 09                     862 	.db #0x09	; 9
      00B9F4 0A                     863 	.db #0x0a	; 10
      00B9F5 0B                     864 	.db #0x0b	; 11
      00B9F6 0C                     865 	.db #0x0c	; 12
      00B9F7 0D                     866 	.db #0x0d	; 13
      00B9F8 0E                     867 	.db #0x0e	; 14
      00B9F9 0F                     868 	.db #0x0f	; 15
      00B9FA 10                     869 	.db #0x10	; 16
      00B9FB 11                     870 	.db #0x11	; 17
      00B9FC 12                     871 	.db #0x12	; 18
      00B9FD 13                     872 	.db #0x13	; 19
      00B9FE 14                     873 	.db #0x14	; 20
      00B9FF 15                     874 	.db #0x15	; 21
      00BA00 16                     875 	.db #0x16	; 22
      00BA01 17                     876 	.db #0x17	; 23
      00BA02 18                     877 	.db #0x18	; 24
      00BA03 19                     878 	.db #0x19	; 25
      00BA04 1A                     879 	.db #0x1a	; 26
      00BA05 1B                     880 	.db #0x1b	; 27
      00BA06 1C                     881 	.db #0x1c	; 28
      00BA07 1D                     882 	.db #0x1d	; 29
      00BA08 2F                     883 	.db #0x2f	; 47
      00BA09 31                     884 	.db #0x31	; 49	'1'
      00BA0A 30                     885 	.db #0x30	; 48	'0'
      00BA0B 23                     886 	.db #0x23	; 35
      00BA0C 2D                     887 	.db #0x2d	; 45
      00BA0D 35                     888 	.db #0x35	; 53	'5'
      00BA0E 04                     889 	.db #0x04	; 4
      00BA0F 05                     890 	.db #0x05	; 5
      00BA10 06                     891 	.db #0x06	; 6
      00BA11 07                     892 	.db #0x07	; 7
      00BA12 08                     893 	.db #0x08	; 8
      00BA13 09                     894 	.db #0x09	; 9
      00BA14 0A                     895 	.db #0x0a	; 10
      00BA15 0B                     896 	.db #0x0b	; 11
      00BA16 0C                     897 	.db #0x0c	; 12
      00BA17 0D                     898 	.db #0x0d	; 13
      00BA18 0E                     899 	.db #0x0e	; 14
      00BA19 0F                     900 	.db #0x0f	; 15
      00BA1A 10                     901 	.db #0x10	; 16
      00BA1B 11                     902 	.db #0x11	; 17
      00BA1C 12                     903 	.db #0x12	; 18
      00BA1D 13                     904 	.db #0x13	; 19
      00BA1E 14                     905 	.db #0x14	; 20
      00BA1F 15                     906 	.db #0x15	; 21
      00BA20 16                     907 	.db #0x16	; 22
      00BA21 17                     908 	.db #0x17	; 23
      00BA22 18                     909 	.db #0x18	; 24
      00BA23 19                     910 	.db #0x19	; 25
      00BA24 1A                     911 	.db #0x1a	; 26
      00BA25 1B                     912 	.db #0x1b	; 27
      00BA26 1C                     913 	.db #0x1c	; 28
      00BA27 1D                     914 	.db #0x1d	; 29
      00BA28 2F                     915 	.db #0x2f	; 47
      00BA29 31                     916 	.db #0x31	; 49	'1'
      00BA2A 30                     917 	.db #0x30	; 48	'0'
      00BA2B 35                     918 	.db #0x35	; 53	'5'
      00BA2C 4C                     919 	.db #0x4c	; 76	'L'
                                    920 	.area CSEG    (CODE)
                                    921 	.area XINIT   (CODE)
                                    922 	.area CABS    (ABS,CODE)
