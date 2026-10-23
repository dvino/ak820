                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module suspend
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _matrix_get_row
                                     12 	.globl _matrix_scan
                                     13 	.globl _ADC_START
                                     14 	.globl _S0_R_FIFO
                                     15 	.globl _S0_T_FIFO
                                     16 	.globl _S0_FREE
                                     17 	.globl _S0_IF_BYTE
                                     18 	.globl _S0_IF_FIRST
                                     19 	.globl _S0_IF_OV
                                     20 	.globl _S0_FST_ACT
                                     21 	.globl _CP_RL2
                                     22 	.globl _C_T2
                                     23 	.globl _TR2
                                     24 	.globl _EXEN2
                                     25 	.globl _TCLK
                                     26 	.globl _RCLK
                                     27 	.globl _EXF2
                                     28 	.globl _CAP1F
                                     29 	.globl _TF2
                                     30 	.globl _RI
                                     31 	.globl _TI
                                     32 	.globl _RB8
                                     33 	.globl _TB8
                                     34 	.globl _REN
                                     35 	.globl _SM2
                                     36 	.globl _SM1
                                     37 	.globl _SM0
                                     38 	.globl _IT0
                                     39 	.globl _IE0
                                     40 	.globl _IT1
                                     41 	.globl _IE1
                                     42 	.globl _TR0
                                     43 	.globl _TF0
                                     44 	.globl _TR1
                                     45 	.globl _TF1
                                     46 	.globl _P4_0
                                     47 	.globl _P4_1
                                     48 	.globl _P4_2
                                     49 	.globl _P4_3
                                     50 	.globl _P4_4
                                     51 	.globl _P4_5
                                     52 	.globl _P4_6
                                     53 	.globl _RXD
                                     54 	.globl _TXD
                                     55 	.globl _INT0
                                     56 	.globl _INT1
                                     57 	.globl _T0
                                     58 	.globl _T1
                                     59 	.globl _MOSI1
                                     60 	.globl _MISO1
                                     61 	.globl _SCK1
                                     62 	.globl _P3_0
                                     63 	.globl _P3_1
                                     64 	.globl _P3_2
                                     65 	.globl _P3_3
                                     66 	.globl _P3_4
                                     67 	.globl _P3_5
                                     68 	.globl _P3_6
                                     69 	.globl _P3_7
                                     70 	.globl _CAP1_
                                     71 	.globl _T2_
                                     72 	.globl _CAP2_
                                     73 	.globl _T2EX_
                                     74 	.globl _RXD1
                                     75 	.globl _TXD1
                                     76 	.globl _P2_0
                                     77 	.globl _P2_1
                                     78 	.globl _P2_2
                                     79 	.globl _P2_3
                                     80 	.globl _P2_4
                                     81 	.globl _P2_5
                                     82 	.globl _P2_6
                                     83 	.globl _P2_7
                                     84 	.globl _AIN0
                                     85 	.globl _AIN1
                                     86 	.globl _AIN2
                                     87 	.globl _AIN3
                                     88 	.globl _AIN4
                                     89 	.globl _AIN5
                                     90 	.globl _AIN6
                                     91 	.globl _AIN7
                                     92 	.globl _CAP1
                                     93 	.globl _T2
                                     94 	.globl _CAP2
                                     95 	.globl _T2EX
                                     96 	.globl _INT0_
                                     97 	.globl _SCS
                                     98 	.globl _MOSI
                                     99 	.globl _MISO
                                    100 	.globl _SCK
                                    101 	.globl _RXD1_
                                    102 	.globl _TXD1_
                                    103 	.globl _P1_0
                                    104 	.globl _P1_1
                                    105 	.globl _P1_2
                                    106 	.globl _P1_3
                                    107 	.globl _P1_4
                                    108 	.globl _P1_5
                                    109 	.globl _P1_6
                                    110 	.globl _P1_7
                                    111 	.globl _AIN8
                                    112 	.globl _AIN9
                                    113 	.globl _AIN10
                                    114 	.globl _AIN11
                                    115 	.globl _AIN12
                                    116 	.globl _AIN13
                                    117 	.globl _RXD_
                                    118 	.globl _TXD_
                                    119 	.globl _SCL0
                                    120 	.globl _SDA0
                                    121 	.globl _P0_0
                                    122 	.globl _P0_1
                                    123 	.globl _P0_2
                                    124 	.globl _P0_3
                                    125 	.globl _P0_4
                                    126 	.globl _P0_5
                                    127 	.globl _P0_6
                                    128 	.globl _P0_7
                                    129 	.globl _IE_SPI0
                                    130 	.globl _IE_USB
                                    131 	.globl _IE_ADC
                                    132 	.globl _IE_UART1
                                    133 	.globl _IE_PWM_I2C
                                    134 	.globl _IE_GPIO
                                    135 	.globl _IE_WDOG
                                    136 	.globl _PX0
                                    137 	.globl _PT0
                                    138 	.globl _PX1
                                    139 	.globl _PT1
                                    140 	.globl _PS
                                    141 	.globl _PT2
                                    142 	.globl _PL_FLAG
                                    143 	.globl _PH_FLAG
                                    144 	.globl _EX0
                                    145 	.globl _ET0
                                    146 	.globl _EX1
                                    147 	.globl _ET1
                                    148 	.globl _ES
                                    149 	.globl _ET2
                                    150 	.globl _E_DIS
                                    151 	.globl _EA
                                    152 	.globl _P
                                    153 	.globl _F1
                                    154 	.globl _OV
                                    155 	.globl _RS0
                                    156 	.globl _RS1
                                    157 	.globl _F0
                                    158 	.globl _AC
                                    159 	.globl _CY
                                    160 	.globl _I2CS_INT_ST
                                    161 	.globl _I2CX_INT
                                    162 	.globl _LED_STATUS
                                    163 	.globl _LED_DMA_H
                                    164 	.globl _LED_DMA_L
                                    165 	.globl _LED_DMA
                                    166 	.globl _LED_PWM_OE
                                    167 	.globl _LED_COMMON
                                    168 	.globl _ADC_CHAN
                                    169 	.globl _ADC_DAT_H
                                    170 	.globl _ADC_DAT_L
                                    171 	.globl _ADC_DAT
                                    172 	.globl _ADC_CTRL
                                    173 	.globl _SPI1_CK_SE
                                    174 	.globl _SPI1_CTRL
                                    175 	.globl _SPI1_DATA
                                    176 	.globl _SPI1_STAT
                                    177 	.globl _SIF1
                                    178 	.globl _SBAUD1
                                    179 	.globl _SBUF1
                                    180 	.globl _SCON1
                                    181 	.globl _SPI0_SETUP
                                    182 	.globl _SPI0_CK_SE
                                    183 	.globl _SPI0_CTRL
                                    184 	.globl _SPI0_DATA
                                    185 	.globl _SPI0_STAT
                                    186 	.globl _T2CAP1H
                                    187 	.globl _T2CAP1L
                                    188 	.globl _T2CAP1
                                    189 	.globl _TH2
                                    190 	.globl _TL2
                                    191 	.globl _T2COUNT
                                    192 	.globl _RCAP2H
                                    193 	.globl _RCAP2L
                                    194 	.globl _RCAP2
                                    195 	.globl _T2MOD
                                    196 	.globl _T2CON
                                    197 	.globl _SBUF
                                    198 	.globl _SCON
                                    199 	.globl _TH1
                                    200 	.globl _TH0
                                    201 	.globl _TL1
                                    202 	.globl _TL0
                                    203 	.globl _TMOD
                                    204 	.globl _TCON
                                    205 	.globl _XBUS_AUX
                                    206 	.globl _P7
                                    207 	.globl _P6_DIR
                                    208 	.globl _P6_OUT_PU
                                    209 	.globl _P6_IN
                                    210 	.globl _P5_DIR
                                    211 	.globl _P5_OUT_PU
                                    212 	.globl _P5_IN
                                    213 	.globl _P4_LED_KEY
                                    214 	.globl _P4_DIR_PU
                                    215 	.globl _P4_MOD_OC
                                    216 	.globl _P4
                                    217 	.globl _P3_DIR_PU
                                    218 	.globl _P3_MOD_OC
                                    219 	.globl _P3
                                    220 	.globl _P2_DIR_PU
                                    221 	.globl _P2_MOD_OC
                                    222 	.globl _P2
                                    223 	.globl _P1_DIR_PU
                                    224 	.globl _P1_MOD_OC
                                    225 	.globl _P1
                                    226 	.globl _P0_DIR_PU
                                    227 	.globl _P0_MOD_OC
                                    228 	.globl _P0
                                    229 	.globl _ROM_CTRL
                                    230 	.globl _ROM_DATA_HH
                                    231 	.globl _ROM_DATA_HL
                                    232 	.globl _ROM_DATA_HI
                                    233 	.globl _ROM_ADDR_H
                                    234 	.globl _ROM_ADDR_L
                                    235 	.globl _ROM_ADDR
                                    236 	.globl _GPIO_IE
                                    237 	.globl _IP_EX
                                    238 	.globl _IE_EX
                                    239 	.globl _IP
                                    240 	.globl _IE
                                    241 	.globl _WDOG_COUNT
                                    242 	.globl _RESET_KEEP
                                    243 	.globl _WAKE_CTRL
                                    244 	.globl _CLOCK_CFG
                                    245 	.globl _POWER_CFG
                                    246 	.globl _PCON
                                    247 	.globl _GLOBAL_CFG
                                    248 	.globl _SAFE_MOD
                                    249 	.globl _DPH
                                    250 	.globl _DPL
                                    251 	.globl _SP
                                    252 	.globl _A_INV
                                    253 	.globl _B
                                    254 	.globl _ACC
                                    255 	.globl _PSW
                                    256 ;--------------------------------------------------------
                                    257 ; special function registers
                                    258 ;--------------------------------------------------------
                                    259 	.area RSEG    (ABS,DATA)
      000000                        260 	.org 0x0000
                           0000D0   261 _PSW	=	0x00d0
                           0000E0   262 _ACC	=	0x00e0
                           0000F0   263 _B	=	0x00f0
                           0000FD   264 _A_INV	=	0x00fd
                           000081   265 _SP	=	0x0081
                           000082   266 _DPL	=	0x0082
                           000083   267 _DPH	=	0x0083
                           0000A1   268 _SAFE_MOD	=	0x00a1
                           0000B1   269 _GLOBAL_CFG	=	0x00b1
                           000087   270 _PCON	=	0x0087
                           0000BA   271 _POWER_CFG	=	0x00ba
                           0000B9   272 _CLOCK_CFG	=	0x00b9
                           0000A9   273 _WAKE_CTRL	=	0x00a9
                           0000FE   274 _RESET_KEEP	=	0x00fe
                           0000FF   275 _WDOG_COUNT	=	0x00ff
                           0000A8   276 _IE	=	0x00a8
                           0000B8   277 _IP	=	0x00b8
                           0000E8   278 _IE_EX	=	0x00e8
                           0000E9   279 _IP_EX	=	0x00e9
                           0000B2   280 _GPIO_IE	=	0x00b2
                           008584   281 _ROM_ADDR	=	0x8584
                           000084   282 _ROM_ADDR_L	=	0x0084
                           000085   283 _ROM_ADDR_H	=	0x0085
                           008F8E   284 _ROM_DATA_HI	=	0x8f8e
                           00008E   285 _ROM_DATA_HL	=	0x008e
                           00008F   286 _ROM_DATA_HH	=	0x008f
                           000086   287 _ROM_CTRL	=	0x0086
                           000080   288 _P0	=	0x0080
                           0000C4   289 _P0_MOD_OC	=	0x00c4
                           0000C5   290 _P0_DIR_PU	=	0x00c5
                           000090   291 _P1	=	0x0090
                           000092   292 _P1_MOD_OC	=	0x0092
                           000093   293 _P1_DIR_PU	=	0x0093
                           0000A0   294 _P2	=	0x00a0
                           000094   295 _P2_MOD_OC	=	0x0094
                           000095   296 _P2_DIR_PU	=	0x0095
                           0000B0   297 _P3	=	0x00b0
                           000096   298 _P3_MOD_OC	=	0x0096
                           000097   299 _P3_DIR_PU	=	0x0097
                           0000C0   300 _P4	=	0x00c0
                           0000C2   301 _P4_MOD_OC	=	0x00c2
                           0000C3   302 _P4_DIR_PU	=	0x00c3
                           0000C1   303 _P4_LED_KEY	=	0x00c1
                           0000AA   304 _P5_IN	=	0x00aa
                           0000AB   305 _P5_OUT_PU	=	0x00ab
                           0000AC   306 _P5_DIR	=	0x00ac
                           0000AD   307 _P6_IN	=	0x00ad
                           0000AE   308 _P6_OUT_PU	=	0x00ae
                           0000AF   309 _P6_DIR	=	0x00af
                           0000F1   310 _P7	=	0x00f1
                           0000A2   311 _XBUS_AUX	=	0x00a2
                           000088   312 _TCON	=	0x0088
                           000089   313 _TMOD	=	0x0089
                           00008A   314 _TL0	=	0x008a
                           00008B   315 _TL1	=	0x008b
                           00008C   316 _TH0	=	0x008c
                           00008D   317 _TH1	=	0x008d
                           000098   318 _SCON	=	0x0098
                           000099   319 _SBUF	=	0x0099
                           0000C8   320 _T2CON	=	0x00c8
                           0000C9   321 _T2MOD	=	0x00c9
                           00CBCA   322 _RCAP2	=	0xcbca
                           0000CA   323 _RCAP2L	=	0x00ca
                           0000CB   324 _RCAP2H	=	0x00cb
                           00CDCC   325 _T2COUNT	=	0xcdcc
                           0000CC   326 _TL2	=	0x00cc
                           0000CD   327 _TH2	=	0x00cd
                           00CFCE   328 _T2CAP1	=	0xcfce
                           0000CE   329 _T2CAP1L	=	0x00ce
                           0000CF   330 _T2CAP1H	=	0x00cf
                           0000F8   331 _SPI0_STAT	=	0x00f8
                           0000F9   332 _SPI0_DATA	=	0x00f9
                           0000FA   333 _SPI0_CTRL	=	0x00fa
                           0000FB   334 _SPI0_CK_SE	=	0x00fb
                           0000FC   335 _SPI0_SETUP	=	0x00fc
                           0000BC   336 _SCON1	=	0x00bc
                           0000BD   337 _SBUF1	=	0x00bd
                           0000BE   338 _SBAUD1	=	0x00be
                           0000BF   339 _SIF1	=	0x00bf
                           0000B4   340 _SPI1_STAT	=	0x00b4
                           0000B5   341 _SPI1_DATA	=	0x00b5
                           0000B6   342 _SPI1_CTRL	=	0x00b6
                           0000B7   343 _SPI1_CK_SE	=	0x00b7
                           0000F3   344 _ADC_CTRL	=	0x00f3
                           00F5F4   345 _ADC_DAT	=	0xf5f4
                           0000F4   346 _ADC_DAT_L	=	0x00f4
                           0000F5   347 _ADC_DAT_H	=	0x00f5
                           0000F6   348 _ADC_CHAN	=	0x00f6
                           0000A6   349 _LED_COMMON	=	0x00a6
                           0000A7   350 _LED_PWM_OE	=	0x00a7
                           00C7C6   351 _LED_DMA	=	0xc7c6
                           0000C6   352 _LED_DMA_L	=	0x00c6
                           0000C7   353 _LED_DMA_H	=	0x00c7
                           0000F7   354 _LED_STATUS	=	0x00f7
                           0000B3   355 _I2CX_INT	=	0x00b3
                           0000BB   356 _I2CS_INT_ST	=	0x00bb
                                    357 ;--------------------------------------------------------
                                    358 ; special function bits
                                    359 ;--------------------------------------------------------
                                    360 	.area RSEG    (ABS,DATA)
      000000                        361 	.org 0x0000
                           0000D7   362 _CY	=	0x00d7
                           0000D6   363 _AC	=	0x00d6
                           0000D5   364 _F0	=	0x00d5
                           0000D4   365 _RS1	=	0x00d4
                           0000D3   366 _RS0	=	0x00d3
                           0000D2   367 _OV	=	0x00d2
                           0000D1   368 _F1	=	0x00d1
                           0000D0   369 _P	=	0x00d0
                           0000AF   370 _EA	=	0x00af
                           0000AE   371 _E_DIS	=	0x00ae
                           0000AD   372 _ET2	=	0x00ad
                           0000AC   373 _ES	=	0x00ac
                           0000AB   374 _ET1	=	0x00ab
                           0000AA   375 _EX1	=	0x00aa
                           0000A9   376 _ET0	=	0x00a9
                           0000A8   377 _EX0	=	0x00a8
                           0000BF   378 _PH_FLAG	=	0x00bf
                           0000BE   379 _PL_FLAG	=	0x00be
                           0000BD   380 _PT2	=	0x00bd
                           0000BC   381 _PS	=	0x00bc
                           0000BB   382 _PT1	=	0x00bb
                           0000BA   383 _PX1	=	0x00ba
                           0000B9   384 _PT0	=	0x00b9
                           0000B8   385 _PX0	=	0x00b8
                           0000EF   386 _IE_WDOG	=	0x00ef
                           0000EE   387 _IE_GPIO	=	0x00ee
                           0000ED   388 _IE_PWM_I2C	=	0x00ed
                           0000EC   389 _IE_UART1	=	0x00ec
                           0000EB   390 _IE_ADC	=	0x00eb
                           0000E9   391 _IE_USB	=	0x00e9
                           0000E8   392 _IE_SPI0	=	0x00e8
                           000087   393 _P0_7	=	0x0087
                           000086   394 _P0_6	=	0x0086
                           000085   395 _P0_5	=	0x0085
                           000084   396 _P0_4	=	0x0084
                           000083   397 _P0_3	=	0x0083
                           000082   398 _P0_2	=	0x0082
                           000081   399 _P0_1	=	0x0081
                           000080   400 _P0_0	=	0x0080
                           000081   401 _SDA0	=	0x0081
                           000080   402 _SCL0	=	0x0080
                           000083   403 _TXD_	=	0x0083
                           000082   404 _RXD_	=	0x0082
                           000085   405 _AIN13	=	0x0085
                           000084   406 _AIN12	=	0x0084
                           000083   407 _AIN11	=	0x0083
                           000082   408 _AIN10	=	0x0082
                           000081   409 _AIN9	=	0x0081
                           000080   410 _AIN8	=	0x0080
                           000097   411 _P1_7	=	0x0097
                           000096   412 _P1_6	=	0x0096
                           000095   413 _P1_5	=	0x0095
                           000094   414 _P1_4	=	0x0094
                           000093   415 _P1_3	=	0x0093
                           000092   416 _P1_2	=	0x0092
                           000091   417 _P1_1	=	0x0091
                           000090   418 _P1_0	=	0x0090
                           000097   419 _TXD1_	=	0x0097
                           000096   420 _RXD1_	=	0x0096
                           000097   421 _SCK	=	0x0097
                           000096   422 _MISO	=	0x0096
                           000095   423 _MOSI	=	0x0095
                           000094   424 _SCS	=	0x0094
                           000092   425 _INT0_	=	0x0092
                           000091   426 _T2EX	=	0x0091
                           000091   427 _CAP2	=	0x0091
                           000090   428 _T2	=	0x0090
                           000090   429 _CAP1	=	0x0090
                           000097   430 _AIN7	=	0x0097
                           000096   431 _AIN6	=	0x0096
                           000095   432 _AIN5	=	0x0095
                           000094   433 _AIN4	=	0x0094
                           000093   434 _AIN3	=	0x0093
                           000092   435 _AIN2	=	0x0092
                           000091   436 _AIN1	=	0x0091
                           000090   437 _AIN0	=	0x0090
                           0000A7   438 _P2_7	=	0x00a7
                           0000A6   439 _P2_6	=	0x00a6
                           0000A5   440 _P2_5	=	0x00a5
                           0000A4   441 _P2_4	=	0x00a4
                           0000A3   442 _P2_3	=	0x00a3
                           0000A2   443 _P2_2	=	0x00a2
                           0000A1   444 _P2_1	=	0x00a1
                           0000A0   445 _P2_0	=	0x00a0
                           0000A7   446 _TXD1	=	0x00a7
                           0000A6   447 _RXD1	=	0x00a6
                           0000A5   448 _T2EX_	=	0x00a5
                           0000A5   449 _CAP2_	=	0x00a5
                           0000A4   450 _T2_	=	0x00a4
                           0000A4   451 _CAP1_	=	0x00a4
                           0000B7   452 _P3_7	=	0x00b7
                           0000B6   453 _P3_6	=	0x00b6
                           0000B5   454 _P3_5	=	0x00b5
                           0000B4   455 _P3_4	=	0x00b4
                           0000B3   456 _P3_3	=	0x00b3
                           0000B2   457 _P3_2	=	0x00b2
                           0000B1   458 _P3_1	=	0x00b1
                           0000B0   459 _P3_0	=	0x00b0
                           0000B7   460 _SCK1	=	0x00b7
                           0000B6   461 _MISO1	=	0x00b6
                           0000B5   462 _MOSI1	=	0x00b5
                           0000B5   463 _T1	=	0x00b5
                           0000B4   464 _T0	=	0x00b4
                           0000B3   465 _INT1	=	0x00b3
                           0000B2   466 _INT0	=	0x00b2
                           0000B1   467 _TXD	=	0x00b1
                           0000B0   468 _RXD	=	0x00b0
                           0000C6   469 _P4_6	=	0x00c6
                           0000C5   470 _P4_5	=	0x00c5
                           0000C4   471 _P4_4	=	0x00c4
                           0000C3   472 _P4_3	=	0x00c3
                           0000C2   473 _P4_2	=	0x00c2
                           0000C1   474 _P4_1	=	0x00c1
                           0000C0   475 _P4_0	=	0x00c0
                           00008F   476 _TF1	=	0x008f
                           00008E   477 _TR1	=	0x008e
                           00008D   478 _TF0	=	0x008d
                           00008C   479 _TR0	=	0x008c
                           00008B   480 _IE1	=	0x008b
                           00008A   481 _IT1	=	0x008a
                           000089   482 _IE0	=	0x0089
                           000088   483 _IT0	=	0x0088
                           00009F   484 _SM0	=	0x009f
                           00009E   485 _SM1	=	0x009e
                           00009D   486 _SM2	=	0x009d
                           00009C   487 _REN	=	0x009c
                           00009B   488 _TB8	=	0x009b
                           00009A   489 _RB8	=	0x009a
                           000099   490 _TI	=	0x0099
                           000098   491 _RI	=	0x0098
                           0000CF   492 _TF2	=	0x00cf
                           0000CF   493 _CAP1F	=	0x00cf
                           0000CE   494 _EXF2	=	0x00ce
                           0000CD   495 _RCLK	=	0x00cd
                           0000CC   496 _TCLK	=	0x00cc
                           0000CB   497 _EXEN2	=	0x00cb
                           0000CA   498 _TR2	=	0x00ca
                           0000C9   499 _C_T2	=	0x00c9
                           0000C8   500 _CP_RL2	=	0x00c8
                           0000FF   501 _S0_FST_ACT	=	0x00ff
                           0000FE   502 _S0_IF_OV	=	0x00fe
                           0000FD   503 _S0_IF_FIRST	=	0x00fd
                           0000FC   504 _S0_IF_BYTE	=	0x00fc
                           0000FB   505 _S0_FREE	=	0x00fb
                           0000FA   506 _S0_T_FIFO	=	0x00fa
                           0000F8   507 _S0_R_FIFO	=	0x00f8
                           0000F7   508 _ADC_START	=	0x00f7
                                    509 ;--------------------------------------------------------
                                    510 ; overlayable register banks
                                    511 ;--------------------------------------------------------
                                    512 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        513 	.ds 8
                                    514 ;--------------------------------------------------------
                                    515 ; internal ram data
                                    516 ;--------------------------------------------------------
                                    517 	.area DSEG    (DATA)
                                    518 ;--------------------------------------------------------
                                    519 ; overlayable items in internal ram
                                    520 ;--------------------------------------------------------
                                    521 ;--------------------------------------------------------
                                    522 ; indirectly addressable internal ram data
                                    523 ;--------------------------------------------------------
                                    524 	.area ISEG    (DATA)
                                    525 ;--------------------------------------------------------
                                    526 ; absolute internal ram data
                                    527 ;--------------------------------------------------------
                                    528 	.area IABS    (ABS,DATA)
                                    529 	.area IABS    (ABS,DATA)
                                    530 ;--------------------------------------------------------
                                    531 ; bit data
                                    532 ;--------------------------------------------------------
                                    533 	.area BSEG    (BIT)
                                    534 ;--------------------------------------------------------
                                    535 ; paged external ram data
                                    536 ;--------------------------------------------------------
                                    537 	.area PSEG    (PAG,XDATA)
                                    538 ;--------------------------------------------------------
                                    539 ; uninitialized external ram data
                                    540 ;--------------------------------------------------------
                                    541 	.area XSEG    (XDATA)
                                    542 ;--------------------------------------------------------
                                    543 ; absolute external ram data
                                    544 ;--------------------------------------------------------
                                    545 	.area XABS    (ABS,XDATA)
                                    546 ;--------------------------------------------------------
                                    547 ; initialized external ram data
                                    548 ;--------------------------------------------------------
                                    549 	.area XISEG   (XDATA)
                                    550 	.area HOME    (CODE)
                                    551 	.area GSINIT0 (CODE)
                                    552 	.area GSINIT1 (CODE)
                                    553 	.area GSINIT2 (CODE)
                                    554 	.area GSINIT3 (CODE)
                                    555 	.area GSINIT4 (CODE)
                                    556 	.area GSINIT5 (CODE)
                                    557 	.area GSINIT  (CODE)
                                    558 	.area GSFINAL (CODE)
                                    559 	.area CSEG    (CODE)
                                    560 ;--------------------------------------------------------
                                    561 ; global & static initialisations
                                    562 ;--------------------------------------------------------
                                    563 	.area HOME    (CODE)
                                    564 	.area GSINIT  (CODE)
                                    565 	.area GSFINAL (CODE)
                                    566 	.area GSINIT  (CODE)
                                    567 ;--------------------------------------------------------
                                    568 ; Home
                                    569 ;--------------------------------------------------------
                                    570 	.area HOME    (CODE)
                                    571 	.area HOME    (CODE)
                                    572 ;--------------------------------------------------------
                                    573 ; code
                                    574 ;--------------------------------------------------------
                                    575 	.area CSEG    (CODE)
                                    576 ;------------------------------------------------------------
                                    577 ;Allocation info for local variables in function 'matrix_power_up'
                                    578 ;------------------------------------------------------------
                                    579 ;	platforms/suspend.c:9: __attribute__((weak)) void matrix_power_up(void) {}
                                    580 ;	-----------------------------------------
                           000007   581 	ar7 = 0x07
                           000006   582 	ar6 = 0x06
                           000005   583 	ar5 = 0x05
                           000004   584 	ar4 = 0x04
                           000003   585 	ar3 = 0x03
                           000002   586 	ar2 = 0x02
                           000001   587 	ar1 = 0x01
                           000000   588 	ar0 = 0x00
                                    589 	.area CSEG    (CODE)
                                    590 	.area CONST   (CODE)
                                    591 	.area XINIT   (CODE)
                                    592 	.area CABS    (ABS,CODE)
