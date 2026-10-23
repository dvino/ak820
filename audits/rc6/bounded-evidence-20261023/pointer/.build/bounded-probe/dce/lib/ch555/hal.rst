                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module hal
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _ADC_START
                                     12 	.globl _S0_R_FIFO
                                     13 	.globl _S0_T_FIFO
                                     14 	.globl _S0_FREE
                                     15 	.globl _S0_IF_BYTE
                                     16 	.globl _S0_IF_FIRST
                                     17 	.globl _S0_IF_OV
                                     18 	.globl _S0_FST_ACT
                                     19 	.globl _CP_RL2
                                     20 	.globl _C_T2
                                     21 	.globl _TR2
                                     22 	.globl _EXEN2
                                     23 	.globl _TCLK
                                     24 	.globl _RCLK
                                     25 	.globl _EXF2
                                     26 	.globl _CAP1F
                                     27 	.globl _TF2
                                     28 	.globl _RI
                                     29 	.globl _TI
                                     30 	.globl _RB8
                                     31 	.globl _TB8
                                     32 	.globl _REN
                                     33 	.globl _SM2
                                     34 	.globl _SM1
                                     35 	.globl _SM0
                                     36 	.globl _IT0
                                     37 	.globl _IE0
                                     38 	.globl _IT1
                                     39 	.globl _IE1
                                     40 	.globl _TR0
                                     41 	.globl _TF0
                                     42 	.globl _TR1
                                     43 	.globl _TF1
                                     44 	.globl _P4_0
                                     45 	.globl _P4_1
                                     46 	.globl _P4_2
                                     47 	.globl _P4_3
                                     48 	.globl _P4_4
                                     49 	.globl _P4_5
                                     50 	.globl _P4_6
                                     51 	.globl _RXD
                                     52 	.globl _TXD
                                     53 	.globl _INT0
                                     54 	.globl _INT1
                                     55 	.globl _T0
                                     56 	.globl _T1
                                     57 	.globl _MOSI1
                                     58 	.globl _MISO1
                                     59 	.globl _SCK1
                                     60 	.globl _P3_0
                                     61 	.globl _P3_1
                                     62 	.globl _P3_2
                                     63 	.globl _P3_3
                                     64 	.globl _P3_4
                                     65 	.globl _P3_5
                                     66 	.globl _P3_6
                                     67 	.globl _P3_7
                                     68 	.globl _CAP1_
                                     69 	.globl _T2_
                                     70 	.globl _CAP2_
                                     71 	.globl _T2EX_
                                     72 	.globl _RXD1
                                     73 	.globl _TXD1
                                     74 	.globl _P2_0
                                     75 	.globl _P2_1
                                     76 	.globl _P2_2
                                     77 	.globl _P2_3
                                     78 	.globl _P2_4
                                     79 	.globl _P2_5
                                     80 	.globl _P2_6
                                     81 	.globl _P2_7
                                     82 	.globl _AIN0
                                     83 	.globl _AIN1
                                     84 	.globl _AIN2
                                     85 	.globl _AIN3
                                     86 	.globl _AIN4
                                     87 	.globl _AIN5
                                     88 	.globl _AIN6
                                     89 	.globl _AIN7
                                     90 	.globl _CAP1
                                     91 	.globl _T2
                                     92 	.globl _CAP2
                                     93 	.globl _T2EX
                                     94 	.globl _INT0_
                                     95 	.globl _SCS
                                     96 	.globl _MOSI
                                     97 	.globl _MISO
                                     98 	.globl _SCK
                                     99 	.globl _RXD1_
                                    100 	.globl _TXD1_
                                    101 	.globl _P1_0
                                    102 	.globl _P1_1
                                    103 	.globl _P1_2
                                    104 	.globl _P1_3
                                    105 	.globl _P1_4
                                    106 	.globl _P1_5
                                    107 	.globl _P1_6
                                    108 	.globl _P1_7
                                    109 	.globl _AIN8
                                    110 	.globl _AIN9
                                    111 	.globl _AIN10
                                    112 	.globl _AIN11
                                    113 	.globl _AIN12
                                    114 	.globl _AIN13
                                    115 	.globl _RXD_
                                    116 	.globl _TXD_
                                    117 	.globl _SCL0
                                    118 	.globl _SDA0
                                    119 	.globl _P0_0
                                    120 	.globl _P0_1
                                    121 	.globl _P0_2
                                    122 	.globl _P0_3
                                    123 	.globl _P0_4
                                    124 	.globl _P0_5
                                    125 	.globl _P0_6
                                    126 	.globl _P0_7
                                    127 	.globl _IE_SPI0
                                    128 	.globl _IE_USB
                                    129 	.globl _IE_ADC
                                    130 	.globl _IE_UART1
                                    131 	.globl _IE_PWM_I2C
                                    132 	.globl _IE_GPIO
                                    133 	.globl _IE_WDOG
                                    134 	.globl _PX0
                                    135 	.globl _PT0
                                    136 	.globl _PX1
                                    137 	.globl _PT1
                                    138 	.globl _PS
                                    139 	.globl _PT2
                                    140 	.globl _PL_FLAG
                                    141 	.globl _PH_FLAG
                                    142 	.globl _EX0
                                    143 	.globl _ET0
                                    144 	.globl _EX1
                                    145 	.globl _ET1
                                    146 	.globl _ES
                                    147 	.globl _ET2
                                    148 	.globl _E_DIS
                                    149 	.globl _EA
                                    150 	.globl _P
                                    151 	.globl _F1
                                    152 	.globl _OV
                                    153 	.globl _RS0
                                    154 	.globl _RS1
                                    155 	.globl _F0
                                    156 	.globl _AC
                                    157 	.globl _CY
                                    158 	.globl _I2CS_INT_ST
                                    159 	.globl _I2CX_INT
                                    160 	.globl _LED_STATUS
                                    161 	.globl _LED_DMA_H
                                    162 	.globl _LED_DMA_L
                                    163 	.globl _LED_DMA
                                    164 	.globl _LED_PWM_OE
                                    165 	.globl _LED_COMMON
                                    166 	.globl _ADC_CHAN
                                    167 	.globl _ADC_DAT_H
                                    168 	.globl _ADC_DAT_L
                                    169 	.globl _ADC_DAT
                                    170 	.globl _ADC_CTRL
                                    171 	.globl _SPI1_CK_SE
                                    172 	.globl _SPI1_CTRL
                                    173 	.globl _SPI1_DATA
                                    174 	.globl _SPI1_STAT
                                    175 	.globl _SIF1
                                    176 	.globl _SBAUD1
                                    177 	.globl _SBUF1
                                    178 	.globl _SCON1
                                    179 	.globl _SPI0_SETUP
                                    180 	.globl _SPI0_CK_SE
                                    181 	.globl _SPI0_CTRL
                                    182 	.globl _SPI0_DATA
                                    183 	.globl _SPI0_STAT
                                    184 	.globl _T2CAP1H
                                    185 	.globl _T2CAP1L
                                    186 	.globl _T2CAP1
                                    187 	.globl _TH2
                                    188 	.globl _TL2
                                    189 	.globl _T2COUNT
                                    190 	.globl _RCAP2H
                                    191 	.globl _RCAP2L
                                    192 	.globl _RCAP2
                                    193 	.globl _T2MOD
                                    194 	.globl _T2CON
                                    195 	.globl _SBUF
                                    196 	.globl _SCON
                                    197 	.globl _TH1
                                    198 	.globl _TH0
                                    199 	.globl _TL1
                                    200 	.globl _TL0
                                    201 	.globl _TMOD
                                    202 	.globl _TCON
                                    203 	.globl _XBUS_AUX
                                    204 	.globl _P7
                                    205 	.globl _P6_DIR
                                    206 	.globl _P6_OUT_PU
                                    207 	.globl _P6_IN
                                    208 	.globl _P5_DIR
                                    209 	.globl _P5_OUT_PU
                                    210 	.globl _P5_IN
                                    211 	.globl _P4_LED_KEY
                                    212 	.globl _P4_DIR_PU
                                    213 	.globl _P4_MOD_OC
                                    214 	.globl _P4
                                    215 	.globl _P3_DIR_PU
                                    216 	.globl _P3_MOD_OC
                                    217 	.globl _P3
                                    218 	.globl _P2_DIR_PU
                                    219 	.globl _P2_MOD_OC
                                    220 	.globl _P2
                                    221 	.globl _P1_DIR_PU
                                    222 	.globl _P1_MOD_OC
                                    223 	.globl _P1
                                    224 	.globl _P0_DIR_PU
                                    225 	.globl _P0_MOD_OC
                                    226 	.globl _P0
                                    227 	.globl _ROM_CTRL
                                    228 	.globl _ROM_DATA_HH
                                    229 	.globl _ROM_DATA_HL
                                    230 	.globl _ROM_DATA_HI
                                    231 	.globl _ROM_ADDR_H
                                    232 	.globl _ROM_ADDR_L
                                    233 	.globl _ROM_ADDR
                                    234 	.globl _GPIO_IE
                                    235 	.globl _IP_EX
                                    236 	.globl _IE_EX
                                    237 	.globl _IP
                                    238 	.globl _IE
                                    239 	.globl _WDOG_COUNT
                                    240 	.globl _RESET_KEEP
                                    241 	.globl _WAKE_CTRL
                                    242 	.globl _CLOCK_CFG
                                    243 	.globl _POWER_CFG
                                    244 	.globl _PCON
                                    245 	.globl _GLOBAL_CFG
                                    246 	.globl _SAFE_MOD
                                    247 	.globl _DPH
                                    248 	.globl _DPL
                                    249 	.globl _SP
                                    250 	.globl _A_INV
                                    251 	.globl _B
                                    252 	.globl _ACC
                                    253 	.globl _PSW
                                    254 	.globl _mDelayuS
                                    255 	.globl _mDelaymS
                                    256 	.globl _getchar
                                    257 	.globl _putchar
                                    258 ;--------------------------------------------------------
                                    259 ; special function registers
                                    260 ;--------------------------------------------------------
                                    261 	.area RSEG    (ABS,DATA)
      000000                        262 	.org 0x0000
                           0000D0   263 _PSW	=	0x00d0
                           0000E0   264 _ACC	=	0x00e0
                           0000F0   265 _B	=	0x00f0
                           0000FD   266 _A_INV	=	0x00fd
                           000081   267 _SP	=	0x0081
                           000082   268 _DPL	=	0x0082
                           000083   269 _DPH	=	0x0083
                           0000A1   270 _SAFE_MOD	=	0x00a1
                           0000B1   271 _GLOBAL_CFG	=	0x00b1
                           000087   272 _PCON	=	0x0087
                           0000BA   273 _POWER_CFG	=	0x00ba
                           0000B9   274 _CLOCK_CFG	=	0x00b9
                           0000A9   275 _WAKE_CTRL	=	0x00a9
                           0000FE   276 _RESET_KEEP	=	0x00fe
                           0000FF   277 _WDOG_COUNT	=	0x00ff
                           0000A8   278 _IE	=	0x00a8
                           0000B8   279 _IP	=	0x00b8
                           0000E8   280 _IE_EX	=	0x00e8
                           0000E9   281 _IP_EX	=	0x00e9
                           0000B2   282 _GPIO_IE	=	0x00b2
                           008584   283 _ROM_ADDR	=	0x8584
                           000084   284 _ROM_ADDR_L	=	0x0084
                           000085   285 _ROM_ADDR_H	=	0x0085
                           008F8E   286 _ROM_DATA_HI	=	0x8f8e
                           00008E   287 _ROM_DATA_HL	=	0x008e
                           00008F   288 _ROM_DATA_HH	=	0x008f
                           000086   289 _ROM_CTRL	=	0x0086
                           000080   290 _P0	=	0x0080
                           0000C4   291 _P0_MOD_OC	=	0x00c4
                           0000C5   292 _P0_DIR_PU	=	0x00c5
                           000090   293 _P1	=	0x0090
                           000092   294 _P1_MOD_OC	=	0x0092
                           000093   295 _P1_DIR_PU	=	0x0093
                           0000A0   296 _P2	=	0x00a0
                           000094   297 _P2_MOD_OC	=	0x0094
                           000095   298 _P2_DIR_PU	=	0x0095
                           0000B0   299 _P3	=	0x00b0
                           000096   300 _P3_MOD_OC	=	0x0096
                           000097   301 _P3_DIR_PU	=	0x0097
                           0000C0   302 _P4	=	0x00c0
                           0000C2   303 _P4_MOD_OC	=	0x00c2
                           0000C3   304 _P4_DIR_PU	=	0x00c3
                           0000C1   305 _P4_LED_KEY	=	0x00c1
                           0000AA   306 _P5_IN	=	0x00aa
                           0000AB   307 _P5_OUT_PU	=	0x00ab
                           0000AC   308 _P5_DIR	=	0x00ac
                           0000AD   309 _P6_IN	=	0x00ad
                           0000AE   310 _P6_OUT_PU	=	0x00ae
                           0000AF   311 _P6_DIR	=	0x00af
                           0000F1   312 _P7	=	0x00f1
                           0000A2   313 _XBUS_AUX	=	0x00a2
                           000088   314 _TCON	=	0x0088
                           000089   315 _TMOD	=	0x0089
                           00008A   316 _TL0	=	0x008a
                           00008B   317 _TL1	=	0x008b
                           00008C   318 _TH0	=	0x008c
                           00008D   319 _TH1	=	0x008d
                           000098   320 _SCON	=	0x0098
                           000099   321 _SBUF	=	0x0099
                           0000C8   322 _T2CON	=	0x00c8
                           0000C9   323 _T2MOD	=	0x00c9
                           00CBCA   324 _RCAP2	=	0xcbca
                           0000CA   325 _RCAP2L	=	0x00ca
                           0000CB   326 _RCAP2H	=	0x00cb
                           00CDCC   327 _T2COUNT	=	0xcdcc
                           0000CC   328 _TL2	=	0x00cc
                           0000CD   329 _TH2	=	0x00cd
                           00CFCE   330 _T2CAP1	=	0xcfce
                           0000CE   331 _T2CAP1L	=	0x00ce
                           0000CF   332 _T2CAP1H	=	0x00cf
                           0000F8   333 _SPI0_STAT	=	0x00f8
                           0000F9   334 _SPI0_DATA	=	0x00f9
                           0000FA   335 _SPI0_CTRL	=	0x00fa
                           0000FB   336 _SPI0_CK_SE	=	0x00fb
                           0000FC   337 _SPI0_SETUP	=	0x00fc
                           0000BC   338 _SCON1	=	0x00bc
                           0000BD   339 _SBUF1	=	0x00bd
                           0000BE   340 _SBAUD1	=	0x00be
                           0000BF   341 _SIF1	=	0x00bf
                           0000B4   342 _SPI1_STAT	=	0x00b4
                           0000B5   343 _SPI1_DATA	=	0x00b5
                           0000B6   344 _SPI1_CTRL	=	0x00b6
                           0000B7   345 _SPI1_CK_SE	=	0x00b7
                           0000F3   346 _ADC_CTRL	=	0x00f3
                           00F5F4   347 _ADC_DAT	=	0xf5f4
                           0000F4   348 _ADC_DAT_L	=	0x00f4
                           0000F5   349 _ADC_DAT_H	=	0x00f5
                           0000F6   350 _ADC_CHAN	=	0x00f6
                           0000A6   351 _LED_COMMON	=	0x00a6
                           0000A7   352 _LED_PWM_OE	=	0x00a7
                           00C7C6   353 _LED_DMA	=	0xc7c6
                           0000C6   354 _LED_DMA_L	=	0x00c6
                           0000C7   355 _LED_DMA_H	=	0x00c7
                           0000F7   356 _LED_STATUS	=	0x00f7
                           0000B3   357 _I2CX_INT	=	0x00b3
                           0000BB   358 _I2CS_INT_ST	=	0x00bb
                                    359 ;--------------------------------------------------------
                                    360 ; special function bits
                                    361 ;--------------------------------------------------------
                                    362 	.area RSEG    (ABS,DATA)
      000000                        363 	.org 0x0000
                           0000D7   364 _CY	=	0x00d7
                           0000D6   365 _AC	=	0x00d6
                           0000D5   366 _F0	=	0x00d5
                           0000D4   367 _RS1	=	0x00d4
                           0000D3   368 _RS0	=	0x00d3
                           0000D2   369 _OV	=	0x00d2
                           0000D1   370 _F1	=	0x00d1
                           0000D0   371 _P	=	0x00d0
                           0000AF   372 _EA	=	0x00af
                           0000AE   373 _E_DIS	=	0x00ae
                           0000AD   374 _ET2	=	0x00ad
                           0000AC   375 _ES	=	0x00ac
                           0000AB   376 _ET1	=	0x00ab
                           0000AA   377 _EX1	=	0x00aa
                           0000A9   378 _ET0	=	0x00a9
                           0000A8   379 _EX0	=	0x00a8
                           0000BF   380 _PH_FLAG	=	0x00bf
                           0000BE   381 _PL_FLAG	=	0x00be
                           0000BD   382 _PT2	=	0x00bd
                           0000BC   383 _PS	=	0x00bc
                           0000BB   384 _PT1	=	0x00bb
                           0000BA   385 _PX1	=	0x00ba
                           0000B9   386 _PT0	=	0x00b9
                           0000B8   387 _PX0	=	0x00b8
                           0000EF   388 _IE_WDOG	=	0x00ef
                           0000EE   389 _IE_GPIO	=	0x00ee
                           0000ED   390 _IE_PWM_I2C	=	0x00ed
                           0000EC   391 _IE_UART1	=	0x00ec
                           0000EB   392 _IE_ADC	=	0x00eb
                           0000E9   393 _IE_USB	=	0x00e9
                           0000E8   394 _IE_SPI0	=	0x00e8
                           000087   395 _P0_7	=	0x0087
                           000086   396 _P0_6	=	0x0086
                           000085   397 _P0_5	=	0x0085
                           000084   398 _P0_4	=	0x0084
                           000083   399 _P0_3	=	0x0083
                           000082   400 _P0_2	=	0x0082
                           000081   401 _P0_1	=	0x0081
                           000080   402 _P0_0	=	0x0080
                           000081   403 _SDA0	=	0x0081
                           000080   404 _SCL0	=	0x0080
                           000083   405 _TXD_	=	0x0083
                           000082   406 _RXD_	=	0x0082
                           000085   407 _AIN13	=	0x0085
                           000084   408 _AIN12	=	0x0084
                           000083   409 _AIN11	=	0x0083
                           000082   410 _AIN10	=	0x0082
                           000081   411 _AIN9	=	0x0081
                           000080   412 _AIN8	=	0x0080
                           000097   413 _P1_7	=	0x0097
                           000096   414 _P1_6	=	0x0096
                           000095   415 _P1_5	=	0x0095
                           000094   416 _P1_4	=	0x0094
                           000093   417 _P1_3	=	0x0093
                           000092   418 _P1_2	=	0x0092
                           000091   419 _P1_1	=	0x0091
                           000090   420 _P1_0	=	0x0090
                           000097   421 _TXD1_	=	0x0097
                           000096   422 _RXD1_	=	0x0096
                           000097   423 _SCK	=	0x0097
                           000096   424 _MISO	=	0x0096
                           000095   425 _MOSI	=	0x0095
                           000094   426 _SCS	=	0x0094
                           000092   427 _INT0_	=	0x0092
                           000091   428 _T2EX	=	0x0091
                           000091   429 _CAP2	=	0x0091
                           000090   430 _T2	=	0x0090
                           000090   431 _CAP1	=	0x0090
                           000097   432 _AIN7	=	0x0097
                           000096   433 _AIN6	=	0x0096
                           000095   434 _AIN5	=	0x0095
                           000094   435 _AIN4	=	0x0094
                           000093   436 _AIN3	=	0x0093
                           000092   437 _AIN2	=	0x0092
                           000091   438 _AIN1	=	0x0091
                           000090   439 _AIN0	=	0x0090
                           0000A7   440 _P2_7	=	0x00a7
                           0000A6   441 _P2_6	=	0x00a6
                           0000A5   442 _P2_5	=	0x00a5
                           0000A4   443 _P2_4	=	0x00a4
                           0000A3   444 _P2_3	=	0x00a3
                           0000A2   445 _P2_2	=	0x00a2
                           0000A1   446 _P2_1	=	0x00a1
                           0000A0   447 _P2_0	=	0x00a0
                           0000A7   448 _TXD1	=	0x00a7
                           0000A6   449 _RXD1	=	0x00a6
                           0000A5   450 _T2EX_	=	0x00a5
                           0000A5   451 _CAP2_	=	0x00a5
                           0000A4   452 _T2_	=	0x00a4
                           0000A4   453 _CAP1_	=	0x00a4
                           0000B7   454 _P3_7	=	0x00b7
                           0000B6   455 _P3_6	=	0x00b6
                           0000B5   456 _P3_5	=	0x00b5
                           0000B4   457 _P3_4	=	0x00b4
                           0000B3   458 _P3_3	=	0x00b3
                           0000B2   459 _P3_2	=	0x00b2
                           0000B1   460 _P3_1	=	0x00b1
                           0000B0   461 _P3_0	=	0x00b0
                           0000B7   462 _SCK1	=	0x00b7
                           0000B6   463 _MISO1	=	0x00b6
                           0000B5   464 _MOSI1	=	0x00b5
                           0000B5   465 _T1	=	0x00b5
                           0000B4   466 _T0	=	0x00b4
                           0000B3   467 _INT1	=	0x00b3
                           0000B2   468 _INT0	=	0x00b2
                           0000B1   469 _TXD	=	0x00b1
                           0000B0   470 _RXD	=	0x00b0
                           0000C6   471 _P4_6	=	0x00c6
                           0000C5   472 _P4_5	=	0x00c5
                           0000C4   473 _P4_4	=	0x00c4
                           0000C3   474 _P4_3	=	0x00c3
                           0000C2   475 _P4_2	=	0x00c2
                           0000C1   476 _P4_1	=	0x00c1
                           0000C0   477 _P4_0	=	0x00c0
                           00008F   478 _TF1	=	0x008f
                           00008E   479 _TR1	=	0x008e
                           00008D   480 _TF0	=	0x008d
                           00008C   481 _TR0	=	0x008c
                           00008B   482 _IE1	=	0x008b
                           00008A   483 _IT1	=	0x008a
                           000089   484 _IE0	=	0x0089
                           000088   485 _IT0	=	0x0088
                           00009F   486 _SM0	=	0x009f
                           00009E   487 _SM1	=	0x009e
                           00009D   488 _SM2	=	0x009d
                           00009C   489 _REN	=	0x009c
                           00009B   490 _TB8	=	0x009b
                           00009A   491 _RB8	=	0x009a
                           000099   492 _TI	=	0x0099
                           000098   493 _RI	=	0x0098
                           0000CF   494 _TF2	=	0x00cf
                           0000CF   495 _CAP1F	=	0x00cf
                           0000CE   496 _EXF2	=	0x00ce
                           0000CD   497 _RCLK	=	0x00cd
                           0000CC   498 _TCLK	=	0x00cc
                           0000CB   499 _EXEN2	=	0x00cb
                           0000CA   500 _TR2	=	0x00ca
                           0000C9   501 _C_T2	=	0x00c9
                           0000C8   502 _CP_RL2	=	0x00c8
                           0000FF   503 _S0_FST_ACT	=	0x00ff
                           0000FE   504 _S0_IF_OV	=	0x00fe
                           0000FD   505 _S0_IF_FIRST	=	0x00fd
                           0000FC   506 _S0_IF_BYTE	=	0x00fc
                           0000FB   507 _S0_FREE	=	0x00fb
                           0000FA   508 _S0_T_FIFO	=	0x00fa
                           0000F8   509 _S0_R_FIFO	=	0x00f8
                           0000F7   510 _ADC_START	=	0x00f7
                                    511 ;--------------------------------------------------------
                                    512 ; overlayable register banks
                                    513 ;--------------------------------------------------------
                                    514 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        515 	.ds 8
                                    516 ;--------------------------------------------------------
                                    517 ; overlayable bit register bank
                                    518 ;--------------------------------------------------------
                                    519 	.area BIT_BANK	(REL,OVR,DATA)
      000023                        520 bits:
      000023                        521 	.ds 1
                           008000   522 	b0 = bits[0]
                           008100   523 	b1 = bits[1]
                           008200   524 	b2 = bits[2]
                           008300   525 	b3 = bits[3]
                           008400   526 	b4 = bits[4]
                           008500   527 	b5 = bits[5]
                           008600   528 	b6 = bits[6]
                           008700   529 	b7 = bits[7]
                                    530 ;--------------------------------------------------------
                                    531 ; internal ram data
                                    532 ;--------------------------------------------------------
                                    533 	.area DSEG    (DATA)
                                    534 ;--------------------------------------------------------
                                    535 ; overlayable items in internal ram
                                    536 ;--------------------------------------------------------
                                    537 ;--------------------------------------------------------
                                    538 ; indirectly addressable internal ram data
                                    539 ;--------------------------------------------------------
                                    540 	.area ISEG    (DATA)
                                    541 ;--------------------------------------------------------
                                    542 ; absolute internal ram data
                                    543 ;--------------------------------------------------------
                                    544 	.area IABS    (ABS,DATA)
                                    545 	.area IABS    (ABS,DATA)
                                    546 ;--------------------------------------------------------
                                    547 ; bit data
                                    548 ;--------------------------------------------------------
                                    549 	.area BSEG    (BIT)
                                    550 ;--------------------------------------------------------
                                    551 ; paged external ram data
                                    552 ;--------------------------------------------------------
                                    553 	.area PSEG    (PAG,XDATA)
                                    554 ;--------------------------------------------------------
                                    555 ; uninitialized external ram data
                                    556 ;--------------------------------------------------------
                                    557 	.area XSEG    (XDATA)
      000659                        558 _mDelayuS_n_10000_52:
      000659                        559 	.ds 2
      00065B                        560 _mDelaymS_n_10000_55:
      00065B                        561 	.ds 2
      00065D                        562 _putchar_c_10000_66:
      00065D                        563 	.ds 2
                                    564 ;--------------------------------------------------------
                                    565 ; absolute external ram data
                                    566 ;--------------------------------------------------------
                                    567 	.area XABS    (ABS,XDATA)
                                    568 ;--------------------------------------------------------
                                    569 ; initialized external ram data
                                    570 ;--------------------------------------------------------
                                    571 	.area XISEG   (XDATA)
                                    572 	.area HOME    (CODE)
                                    573 	.area GSINIT0 (CODE)
                                    574 	.area GSINIT1 (CODE)
                                    575 	.area GSINIT2 (CODE)
                                    576 	.area GSINIT3 (CODE)
                                    577 	.area GSINIT4 (CODE)
                                    578 	.area GSINIT5 (CODE)
                                    579 	.area GSINIT  (CODE)
                                    580 	.area GSFINAL (CODE)
                                    581 	.area CSEG    (CODE)
                                    582 ;--------------------------------------------------------
                                    583 ; global & static initialisations
                                    584 ;--------------------------------------------------------
                                    585 	.area HOME    (CODE)
                                    586 	.area GSINIT  (CODE)
                                    587 	.area GSFINAL (CODE)
                                    588 	.area GSINIT  (CODE)
                                    589 ;--------------------------------------------------------
                                    590 ; Home
                                    591 ;--------------------------------------------------------
                                    592 	.area HOME    (CODE)
                                    593 	.area HOME    (CODE)
                                    594 ;--------------------------------------------------------
                                    595 ; code
                                    596 ;--------------------------------------------------------
                                    597 	.area CSEG    (CODE)
                                    598 ;------------------------------------------------------------
                                    599 ;Allocation info for local variables in function 'CfgFsys'
                                    600 ;------------------------------------------------------------
                                    601 ;	lib/ch555/hal.c:23: void CfgFsys(void)  
                                    602 ;	-----------------------------------------
                           000007   603 	ar7 = 0x07
                           000006   604 	ar6 = 0x06
                           000005   605 	ar5 = 0x05
                           000004   606 	ar4 = 0x04
                           000003   607 	ar3 = 0x03
                           000002   608 	ar2 = 0x02
                           000001   609 	ar1 = 0x01
                           000000   610 	ar0 = 0x00
                                    611 ;	 function mDelayuS
                                    612 ;	-----------------------------------------
      005222                        613 _mDelayuS:
      005222 AF 83            [24]  614 	mov	r7,dph
      005224 E5 82            [12]  615 	mov	a,dpl
      005226 90 06 59         [24]  616 	mov	dptr,#_mDelayuS_n_10000_52
      005229 F0               [24]  617 	movx	@dptr,a
      00522A EF               [12]  618 	mov	a,r7
      00522B A3               [24]  619 	inc	dptr
      00522C F0               [24]  620 	movx	@dptr,a
                                    621 ;	lib/ch555/hal.c:101: while(n){  // total = 12~13 Fsys cycles, 1uS @Fsys=12MHz
      00522D 90 06 59         [24]  622 	mov	dptr,#_mDelayuS_n_10000_52
      005230 E0               [24]  623 	movx	a,@dptr
      005231 FE               [12]  624 	mov	r6,a
      005232 A3               [24]  625 	inc	dptr
      005233 E0               [24]  626 	movx	a,@dptr
      005234 FF               [12]  627 	mov	r7,a
      005235                        628 00101$:
      005235 EE               [12]  629 	mov	a,r6
      005236 4F               [12]  630 	orl	a,r7
      005237 60 1D            [24]  631 	jz	00110$
                                    632 ;	lib/ch555/hal.c:102: ++ SAFE_MOD;  // 2 Fsys cycles, for higher Fsys, add operation here
      005239 05 A1            [12]  633 	inc	_SAFE_MOD
                                    634 ;	lib/ch555/hal.c:105: ++ SAFE_MOD;
      00523B 05 A1            [12]  635 	inc	_SAFE_MOD
                                    636 ;	lib/ch555/hal.c:108: ++ SAFE_MOD;
      00523D 05 A1            [12]  637 	inc	_SAFE_MOD
                                    638 ;	lib/ch555/hal.c:111: ++ SAFE_MOD;
      00523F 05 A1            [12]  639 	inc	_SAFE_MOD
                                    640 ;	lib/ch555/hal.c:114: ++ SAFE_MOD;
      005241 05 A1            [12]  641 	inc	_SAFE_MOD
                                    642 ;	lib/ch555/hal.c:117: ++ SAFE_MOD;
      005243 05 A1            [12]  643 	inc	_SAFE_MOD
                                    644 ;	lib/ch555/hal.c:120: ++ SAFE_MOD;
      005245 05 A1            [12]  645 	inc	_SAFE_MOD
                                    646 ;	lib/ch555/hal.c:123: -- n;
      005247 1E               [12]  647 	dec	r6
      005248 BE FF 01         [24]  648 	cjne	r6,#0xff,00122$
      00524B 1F               [12]  649 	dec	r7
      00524C                        650 00122$:
      00524C 90 06 59         [24]  651 	mov	dptr,#_mDelayuS_n_10000_52
      00524F EE               [12]  652 	mov	a,r6
      005250 F0               [24]  653 	movx	@dptr,a
      005251 EF               [12]  654 	mov	a,r7
      005252 A3               [24]  655 	inc	dptr
      005253 F0               [24]  656 	movx	@dptr,a
      005254 80 DF            [24]  657 	sjmp	00101$
      005256                        658 00110$:
      005256 90 06 59         [24]  659 	mov	dptr,#_mDelayuS_n_10000_52
      005259 E4               [12]  660 	clr	a
      00525A F0               [24]  661 	movx	@dptr,a
      00525B A3               [24]  662 	inc	dptr
      00525C F0               [24]  663 	movx	@dptr,a
                                    664 ;	lib/ch555/hal.c:125: }
      00525D 22               [24]  665 	ret
                                    666 ;------------------------------------------------------------
                                    667 ;Allocation info for local variables in function 'mDelaymS'
                                    668 ;------------------------------------------------------------
                                    669 ;n             Allocated with name '_mDelaymS_n_10000_55'
                                    670 ;------------------------------------------------------------
                                    671 ;	lib/ch555/hal.c:133: void mDelaymS(UINT16 n)                                                    
                                    672 ;	-----------------------------------------
                                    673 ;	 function mDelaymS
                                    674 ;	-----------------------------------------
      00525E                        675 _mDelaymS:
      00525E C0 07            [24]  676 	push	ar7
      005260 C0 06            [24]  677 	push	ar6
      005262 AF 83            [24]  678 	mov	r7,dph
      005264 E5 82            [12]  679 	mov	a,dpl
      005266 90 06 5B         [24]  680 	mov	dptr,#_mDelaymS_n_10000_55
      005269 F0               [24]  681 	movx	@dptr,a
      00526A EF               [12]  682 	mov	a,r7
      00526B A3               [24]  683 	inc	dptr
      00526C F0               [24]  684 	movx	@dptr,a
                                    685 ;	lib/ch555/hal.c:135: while(n){
      00526D 90 06 5B         [24]  686 	mov	dptr,#_mDelaymS_n_10000_55
      005270 E0               [24]  687 	movx	a,@dptr
      005271 FE               [12]  688 	mov	r6,a
      005272 A3               [24]  689 	inc	dptr
      005273 E0               [24]  690 	movx	a,@dptr
      005274 FF               [12]  691 	mov	r7,a
      005275                        692 00101$:
      005275 EE               [12]  693 	mov	a,r6
      005276 4F               [12]  694 	orl	a,r7
      005277 60 35            [24]  695 	jz	00110$
                                    696 ;	lib/ch555/hal.c:136: mDelayuS(1000);
      005279 90 03 E8         [24]  697 	mov	dptr,#0x03e8
      00527C C0 07            [24]  698 	push	ar7
      00527E C0 06            [24]  699 	push	ar6
      005280 C0 05            [24]  700 	push	ar5
      005282 C0 04            [24]  701 	push	ar4
      005284 C0 03            [24]  702 	push	ar3
      005286 C0 02            [24]  703 	push	ar2
      005288 C0 01            [24]  704 	push	ar1
      00528A C0 00            [24]  705 	push	ar0
      00528C 12 52 22         [24]  706 	lcall	_mDelayuS
      00528F D0 00            [24]  707 	pop	ar0
      005291 D0 01            [24]  708 	pop	ar1
      005293 D0 02            [24]  709 	pop	ar2
      005295 D0 03            [24]  710 	pop	ar3
      005297 D0 04            [24]  711 	pop	ar4
      005299 D0 05            [24]  712 	pop	ar5
      00529B D0 06            [24]  713 	pop	ar6
      00529D D0 07            [24]  714 	pop	ar7
                                    715 ;	lib/ch555/hal.c:137: -- n;
      00529F 1E               [12]  716 	dec	r6
      0052A0 BE FF 01         [24]  717 	cjne	r6,#0xff,00122$
      0052A3 1F               [12]  718 	dec	r7
      0052A4                        719 00122$:
      0052A4 90 06 5B         [24]  720 	mov	dptr,#_mDelaymS_n_10000_55
      0052A7 EE               [12]  721 	mov	a,r6
      0052A8 F0               [24]  722 	movx	@dptr,a
      0052A9 EF               [12]  723 	mov	a,r7
      0052AA A3               [24]  724 	inc	dptr
      0052AB F0               [24]  725 	movx	@dptr,a
      0052AC 80 C7            [24]  726 	sjmp	00101$
      0052AE                        727 00110$:
      0052AE 90 06 5B         [24]  728 	mov	dptr,#_mDelaymS_n_10000_55
      0052B1 E4               [12]  729 	clr	a
      0052B2 F0               [24]  730 	movx	@dptr,a
      0052B3 A3               [24]  731 	inc	dptr
      0052B4 F0               [24]  732 	movx	@dptr,a
                                    733 ;	lib/ch555/hal.c:139: }                                         
      0052B5 D0 06            [24]  734 	pop	ar6
      0052B7 D0 07            [24]  735 	pop	ar7
      0052B9 22               [24]  736 	ret
                                    737 ;------------------------------------------------------------
                                    738 ;Allocation info for local variables in function 'CH555UART1Alter'
                                    739 ;------------------------------------------------------------
                                    740 ;	lib/ch555/hal.c:218: void CH555UART1Alter(void) {
                                    741 ;	-----------------------------------------
                                    742 ;	 function getchar
                                    743 ;	-----------------------------------------
      0052BA                        744 _getchar:
                                    745 ;	lib/ch555/hal.c:244: while (!(SIF1&bU1RI));//Query reception, interrupt mode is not required
      0052BA                        746 00101$:
      0052BA E5 BF            [12]  747 	mov	a,_SIF1
      0052BC 30 E0 FB         [24]  748 	jnb	acc.0,00101$
                                    749 ;	lib/ch555/hal.c:245: SIF1  = bU1RI;
      0052BF 75 BF 01         [24]  750 	mov	_SIF1,#0x01
                                    751 ;	lib/ch555/hal.c:246: return (int)SBUF1;
      0052C2 AE BD            [24]  752 	mov	r6,_SBUF1
      0052C4 7F 00            [12]  753 	mov	r7,#0x00
      0052C6 8E 82            [24]  754 	mov	dpl, r6
      0052C8 8F 83            [24]  755 	mov	dph, r7
                                    756 ;	lib/ch555/hal.c:247: }
      0052CA 22               [24]  757 	ret
                                    758 ;------------------------------------------------------------
                                    759 ;Allocation info for local variables in function 'putchar'
                                    760 ;------------------------------------------------------------
                                    761 ;c             Allocated with name '_putchar_c_10000_66'
                                    762 ;------------------------------------------------------------
                                    763 ;	lib/ch555/hal.c:249: int putchar(int c) {
                                    764 ;	-----------------------------------------
                                    765 ;	 function putchar
                                    766 ;	-----------------------------------------
      0052CB                        767 _putchar:
      0052CB AF 83            [24]  768 	mov	r7,dph
      0052CD E5 82            [12]  769 	mov	a,dpl
      0052CF 90 06 5D         [24]  770 	mov	dptr,#_putchar_c_10000_66
      0052D2 F0               [24]  771 	movx	@dptr,a
      0052D3 EF               [12]  772 	mov	a,r7
      0052D4 A3               [24]  773 	inc	dptr
      0052D5 F0               [24]  774 	movx	@dptr,a
                                    775 ;	lib/ch555/hal.c:250: SBUF1 = c & 0xff;
      0052D6 90 06 5D         [24]  776 	mov	dptr,#_putchar_c_10000_66
      0052D9 E0               [24]  777 	movx	a,@dptr
      0052DA F5 BD            [12]  778 	mov	_SBUF1,a
                                    779 ;	lib/ch555/hal.c:251: while (!(SIF1&bU1TI));//For query sending, the following two statements are not needed in the interrupt mode, but ti=0 is required before sending.
      0052DC                        780 00101$:
      0052DC E5 BF            [12]  781 	mov	a,_SIF1
      0052DE 30 E1 FB         [24]  782 	jnb	acc.1,00101$
                                    783 ;	lib/ch555/hal.c:252: SIF1  = bU1TI;
      0052E1 75 BF 02         [24]  784 	mov	_SIF1,#0x02
                                    785 ;	lib/ch555/hal.c:253: return c;
      0052E4 90 06 5D         [24]  786 	mov	dptr,#_putchar_c_10000_66
      0052E7 E0               [24]  787 	movx	a,@dptr
      0052E8 FE               [12]  788 	mov	r6,a
      0052E9 A3               [24]  789 	inc	dptr
      0052EA E0               [24]  790 	movx	a,@dptr
                                    791 ;	lib/ch555/hal.c:254: }
      0052EB 8E 82            [24]  792 	mov	dpl,r6
      0052ED F5 83            [12]  793 	mov	dph,a
      0052EF 22               [24]  794 	ret
                                    795 ;------------------------------------------------------------
                                    796 ;Allocation info for local variables in function 'CH555WDTModeSelect'
                                    797 ;------------------------------------------------------------
                                    798 ;mode          Allocated with name '_CH555WDTModeSelect_mode_10000_68'
                                    799 ;------------------------------------------------------------
                                    800 ;	lib/ch555/hal.c:265: void CH555WDTModeSelect(UINT8 mode)
                                    801 ;	-----------------------------------------
                                    802 	.area CSEG    (CODE)
                                    803 	.area CONST   (CODE)
                                    804 	.area XINIT   (CODE)
                                    805 	.area CABS    (ABS,CODE)
