                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module color
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
                                    254 	.globl _hsv_to_rgb_into_PARM_3
                                    255 	.globl _hsv_to_rgb_into_PARM_1
                                    256 	.globl _hsv_to_rgb_into
                                    257 ;--------------------------------------------------------
                                    258 ; special function registers
                                    259 ;--------------------------------------------------------
                                    260 	.area RSEG    (ABS,DATA)
      000000                        261 	.org 0x0000
                           0000D0   262 _PSW	=	0x00d0
                           0000E0   263 _ACC	=	0x00e0
                           0000F0   264 _B	=	0x00f0
                           0000FD   265 _A_INV	=	0x00fd
                           000081   266 _SP	=	0x0081
                           000082   267 _DPL	=	0x0082
                           000083   268 _DPH	=	0x0083
                           0000A1   269 _SAFE_MOD	=	0x00a1
                           0000B1   270 _GLOBAL_CFG	=	0x00b1
                           000087   271 _PCON	=	0x0087
                           0000BA   272 _POWER_CFG	=	0x00ba
                           0000B9   273 _CLOCK_CFG	=	0x00b9
                           0000A9   274 _WAKE_CTRL	=	0x00a9
                           0000FE   275 _RESET_KEEP	=	0x00fe
                           0000FF   276 _WDOG_COUNT	=	0x00ff
                           0000A8   277 _IE	=	0x00a8
                           0000B8   278 _IP	=	0x00b8
                           0000E8   279 _IE_EX	=	0x00e8
                           0000E9   280 _IP_EX	=	0x00e9
                           0000B2   281 _GPIO_IE	=	0x00b2
                           008584   282 _ROM_ADDR	=	0x8584
                           000084   283 _ROM_ADDR_L	=	0x0084
                           000085   284 _ROM_ADDR_H	=	0x0085
                           008F8E   285 _ROM_DATA_HI	=	0x8f8e
                           00008E   286 _ROM_DATA_HL	=	0x008e
                           00008F   287 _ROM_DATA_HH	=	0x008f
                           000086   288 _ROM_CTRL	=	0x0086
                           000080   289 _P0	=	0x0080
                           0000C4   290 _P0_MOD_OC	=	0x00c4
                           0000C5   291 _P0_DIR_PU	=	0x00c5
                           000090   292 _P1	=	0x0090
                           000092   293 _P1_MOD_OC	=	0x0092
                           000093   294 _P1_DIR_PU	=	0x0093
                           0000A0   295 _P2	=	0x00a0
                           000094   296 _P2_MOD_OC	=	0x0094
                           000095   297 _P2_DIR_PU	=	0x0095
                           0000B0   298 _P3	=	0x00b0
                           000096   299 _P3_MOD_OC	=	0x0096
                           000097   300 _P3_DIR_PU	=	0x0097
                           0000C0   301 _P4	=	0x00c0
                           0000C2   302 _P4_MOD_OC	=	0x00c2
                           0000C3   303 _P4_DIR_PU	=	0x00c3
                           0000C1   304 _P4_LED_KEY	=	0x00c1
                           0000AA   305 _P5_IN	=	0x00aa
                           0000AB   306 _P5_OUT_PU	=	0x00ab
                           0000AC   307 _P5_DIR	=	0x00ac
                           0000AD   308 _P6_IN	=	0x00ad
                           0000AE   309 _P6_OUT_PU	=	0x00ae
                           0000AF   310 _P6_DIR	=	0x00af
                           0000F1   311 _P7	=	0x00f1
                           0000A2   312 _XBUS_AUX	=	0x00a2
                           000088   313 _TCON	=	0x0088
                           000089   314 _TMOD	=	0x0089
                           00008A   315 _TL0	=	0x008a
                           00008B   316 _TL1	=	0x008b
                           00008C   317 _TH0	=	0x008c
                           00008D   318 _TH1	=	0x008d
                           000098   319 _SCON	=	0x0098
                           000099   320 _SBUF	=	0x0099
                           0000C8   321 _T2CON	=	0x00c8
                           0000C9   322 _T2MOD	=	0x00c9
                           00CBCA   323 _RCAP2	=	0xcbca
                           0000CA   324 _RCAP2L	=	0x00ca
                           0000CB   325 _RCAP2H	=	0x00cb
                           00CDCC   326 _T2COUNT	=	0xcdcc
                           0000CC   327 _TL2	=	0x00cc
                           0000CD   328 _TH2	=	0x00cd
                           00CFCE   329 _T2CAP1	=	0xcfce
                           0000CE   330 _T2CAP1L	=	0x00ce
                           0000CF   331 _T2CAP1H	=	0x00cf
                           0000F8   332 _SPI0_STAT	=	0x00f8
                           0000F9   333 _SPI0_DATA	=	0x00f9
                           0000FA   334 _SPI0_CTRL	=	0x00fa
                           0000FB   335 _SPI0_CK_SE	=	0x00fb
                           0000FC   336 _SPI0_SETUP	=	0x00fc
                           0000BC   337 _SCON1	=	0x00bc
                           0000BD   338 _SBUF1	=	0x00bd
                           0000BE   339 _SBAUD1	=	0x00be
                           0000BF   340 _SIF1	=	0x00bf
                           0000B4   341 _SPI1_STAT	=	0x00b4
                           0000B5   342 _SPI1_DATA	=	0x00b5
                           0000B6   343 _SPI1_CTRL	=	0x00b6
                           0000B7   344 _SPI1_CK_SE	=	0x00b7
                           0000F3   345 _ADC_CTRL	=	0x00f3
                           00F5F4   346 _ADC_DAT	=	0xf5f4
                           0000F4   347 _ADC_DAT_L	=	0x00f4
                           0000F5   348 _ADC_DAT_H	=	0x00f5
                           0000F6   349 _ADC_CHAN	=	0x00f6
                           0000A6   350 _LED_COMMON	=	0x00a6
                           0000A7   351 _LED_PWM_OE	=	0x00a7
                           00C7C6   352 _LED_DMA	=	0xc7c6
                           0000C6   353 _LED_DMA_L	=	0x00c6
                           0000C7   354 _LED_DMA_H	=	0x00c7
                           0000F7   355 _LED_STATUS	=	0x00f7
                           0000B3   356 _I2CX_INT	=	0x00b3
                           0000BB   357 _I2CS_INT_ST	=	0x00bb
                                    358 ;--------------------------------------------------------
                                    359 ; special function bits
                                    360 ;--------------------------------------------------------
                                    361 	.area RSEG    (ABS,DATA)
      000000                        362 	.org 0x0000
                           0000D7   363 _CY	=	0x00d7
                           0000D6   364 _AC	=	0x00d6
                           0000D5   365 _F0	=	0x00d5
                           0000D4   366 _RS1	=	0x00d4
                           0000D3   367 _RS0	=	0x00d3
                           0000D2   368 _OV	=	0x00d2
                           0000D1   369 _F1	=	0x00d1
                           0000D0   370 _P	=	0x00d0
                           0000AF   371 _EA	=	0x00af
                           0000AE   372 _E_DIS	=	0x00ae
                           0000AD   373 _ET2	=	0x00ad
                           0000AC   374 _ES	=	0x00ac
                           0000AB   375 _ET1	=	0x00ab
                           0000AA   376 _EX1	=	0x00aa
                           0000A9   377 _ET0	=	0x00a9
                           0000A8   378 _EX0	=	0x00a8
                           0000BF   379 _PH_FLAG	=	0x00bf
                           0000BE   380 _PL_FLAG	=	0x00be
                           0000BD   381 _PT2	=	0x00bd
                           0000BC   382 _PS	=	0x00bc
                           0000BB   383 _PT1	=	0x00bb
                           0000BA   384 _PX1	=	0x00ba
                           0000B9   385 _PT0	=	0x00b9
                           0000B8   386 _PX0	=	0x00b8
                           0000EF   387 _IE_WDOG	=	0x00ef
                           0000EE   388 _IE_GPIO	=	0x00ee
                           0000ED   389 _IE_PWM_I2C	=	0x00ed
                           0000EC   390 _IE_UART1	=	0x00ec
                           0000EB   391 _IE_ADC	=	0x00eb
                           0000E9   392 _IE_USB	=	0x00e9
                           0000E8   393 _IE_SPI0	=	0x00e8
                           000087   394 _P0_7	=	0x0087
                           000086   395 _P0_6	=	0x0086
                           000085   396 _P0_5	=	0x0085
                           000084   397 _P0_4	=	0x0084
                           000083   398 _P0_3	=	0x0083
                           000082   399 _P0_2	=	0x0082
                           000081   400 _P0_1	=	0x0081
                           000080   401 _P0_0	=	0x0080
                           000081   402 _SDA0	=	0x0081
                           000080   403 _SCL0	=	0x0080
                           000083   404 _TXD_	=	0x0083
                           000082   405 _RXD_	=	0x0082
                           000085   406 _AIN13	=	0x0085
                           000084   407 _AIN12	=	0x0084
                           000083   408 _AIN11	=	0x0083
                           000082   409 _AIN10	=	0x0082
                           000081   410 _AIN9	=	0x0081
                           000080   411 _AIN8	=	0x0080
                           000097   412 _P1_7	=	0x0097
                           000096   413 _P1_6	=	0x0096
                           000095   414 _P1_5	=	0x0095
                           000094   415 _P1_4	=	0x0094
                           000093   416 _P1_3	=	0x0093
                           000092   417 _P1_2	=	0x0092
                           000091   418 _P1_1	=	0x0091
                           000090   419 _P1_0	=	0x0090
                           000097   420 _TXD1_	=	0x0097
                           000096   421 _RXD1_	=	0x0096
                           000097   422 _SCK	=	0x0097
                           000096   423 _MISO	=	0x0096
                           000095   424 _MOSI	=	0x0095
                           000094   425 _SCS	=	0x0094
                           000092   426 _INT0_	=	0x0092
                           000091   427 _T2EX	=	0x0091
                           000091   428 _CAP2	=	0x0091
                           000090   429 _T2	=	0x0090
                           000090   430 _CAP1	=	0x0090
                           000097   431 _AIN7	=	0x0097
                           000096   432 _AIN6	=	0x0096
                           000095   433 _AIN5	=	0x0095
                           000094   434 _AIN4	=	0x0094
                           000093   435 _AIN3	=	0x0093
                           000092   436 _AIN2	=	0x0092
                           000091   437 _AIN1	=	0x0091
                           000090   438 _AIN0	=	0x0090
                           0000A7   439 _P2_7	=	0x00a7
                           0000A6   440 _P2_6	=	0x00a6
                           0000A5   441 _P2_5	=	0x00a5
                           0000A4   442 _P2_4	=	0x00a4
                           0000A3   443 _P2_3	=	0x00a3
                           0000A2   444 _P2_2	=	0x00a2
                           0000A1   445 _P2_1	=	0x00a1
                           0000A0   446 _P2_0	=	0x00a0
                           0000A7   447 _TXD1	=	0x00a7
                           0000A6   448 _RXD1	=	0x00a6
                           0000A5   449 _T2EX_	=	0x00a5
                           0000A5   450 _CAP2_	=	0x00a5
                           0000A4   451 _T2_	=	0x00a4
                           0000A4   452 _CAP1_	=	0x00a4
                           0000B7   453 _P3_7	=	0x00b7
                           0000B6   454 _P3_6	=	0x00b6
                           0000B5   455 _P3_5	=	0x00b5
                           0000B4   456 _P3_4	=	0x00b4
                           0000B3   457 _P3_3	=	0x00b3
                           0000B2   458 _P3_2	=	0x00b2
                           0000B1   459 _P3_1	=	0x00b1
                           0000B0   460 _P3_0	=	0x00b0
                           0000B7   461 _SCK1	=	0x00b7
                           0000B6   462 _MISO1	=	0x00b6
                           0000B5   463 _MOSI1	=	0x00b5
                           0000B5   464 _T1	=	0x00b5
                           0000B4   465 _T0	=	0x00b4
                           0000B3   466 _INT1	=	0x00b3
                           0000B2   467 _INT0	=	0x00b2
                           0000B1   468 _TXD	=	0x00b1
                           0000B0   469 _RXD	=	0x00b0
                           0000C6   470 _P4_6	=	0x00c6
                           0000C5   471 _P4_5	=	0x00c5
                           0000C4   472 _P4_4	=	0x00c4
                           0000C3   473 _P4_3	=	0x00c3
                           0000C2   474 _P4_2	=	0x00c2
                           0000C1   475 _P4_1	=	0x00c1
                           0000C0   476 _P4_0	=	0x00c0
                           00008F   477 _TF1	=	0x008f
                           00008E   478 _TR1	=	0x008e
                           00008D   479 _TF0	=	0x008d
                           00008C   480 _TR0	=	0x008c
                           00008B   481 _IE1	=	0x008b
                           00008A   482 _IT1	=	0x008a
                           000089   483 _IE0	=	0x0089
                           000088   484 _IT0	=	0x0088
                           00009F   485 _SM0	=	0x009f
                           00009E   486 _SM1	=	0x009e
                           00009D   487 _SM2	=	0x009d
                           00009C   488 _REN	=	0x009c
                           00009B   489 _TB8	=	0x009b
                           00009A   490 _RB8	=	0x009a
                           000099   491 _TI	=	0x0099
                           000098   492 _RI	=	0x0098
                           0000CF   493 _TF2	=	0x00cf
                           0000CF   494 _CAP1F	=	0x00cf
                           0000CE   495 _EXF2	=	0x00ce
                           0000CD   496 _RCLK	=	0x00cd
                           0000CC   497 _TCLK	=	0x00cc
                           0000CB   498 _EXEN2	=	0x00cb
                           0000CA   499 _TR2	=	0x00ca
                           0000C9   500 _C_T2	=	0x00c9
                           0000C8   501 _CP_RL2	=	0x00c8
                           0000FF   502 _S0_FST_ACT	=	0x00ff
                           0000FE   503 _S0_IF_OV	=	0x00fe
                           0000FD   504 _S0_IF_FIRST	=	0x00fd
                           0000FC   505 _S0_IF_BYTE	=	0x00fc
                           0000FB   506 _S0_FREE	=	0x00fb
                           0000FA   507 _S0_T_FIFO	=	0x00fa
                           0000F8   508 _S0_R_FIFO	=	0x00f8
                           0000F7   509 _ADC_START	=	0x00f7
                                    510 ;--------------------------------------------------------
                                    511 ; overlayable register banks
                                    512 ;--------------------------------------------------------
                                    513 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        514 	.ds 8
                                    515 ;--------------------------------------------------------
                                    516 ; internal ram data
                                    517 ;--------------------------------------------------------
                                    518 	.area DSEG    (DATA)
                                    519 ;--------------------------------------------------------
                                    520 ; overlayable items in internal ram
                                    521 ;--------------------------------------------------------
                                    522 ;--------------------------------------------------------
                                    523 ; indirectly addressable internal ram data
                                    524 ;--------------------------------------------------------
                                    525 	.area ISEG    (DATA)
                                    526 ;--------------------------------------------------------
                                    527 ; absolute internal ram data
                                    528 ;--------------------------------------------------------
                                    529 	.area IABS    (ABS,DATA)
                                    530 	.area IABS    (ABS,DATA)
                                    531 ;--------------------------------------------------------
                                    532 ; bit data
                                    533 ;--------------------------------------------------------
                                    534 	.area BSEG    (BIT)
                                    535 ;--------------------------------------------------------
                                    536 ; paged external ram data
                                    537 ;--------------------------------------------------------
                                    538 	.area PSEG    (PAG,XDATA)
                                    539 ;--------------------------------------------------------
                                    540 ; uninitialized external ram data
                                    541 ;--------------------------------------------------------
                                    542 	.area XSEG    (XDATA)
      0008C1                        543 _mulhi8_PARM_2:
      0008C1                        544 	.ds 1
      0008C2                        545 _hsv_to_rgb_into_PARM_1:
      0008C2                        546 	.ds 3
      0008C5                        547 _hsv_to_rgb_into_PARM_3:
      0008C5                        548 	.ds 2
      0008C7                        549 _hsv_to_rgb_into_use_cie_10000_55:
      0008C7                        550 	.ds 1
      0008C8                        551 _hsv_to_rgb_into_rgb_10000_56:
      0008C8                        552 	.ds 3
      0008CB                        553 _hsv_to_rgb_into_v_10000_56:
      0008CB                        554 	.ds 1
                                    555 ;--------------------------------------------------------
                                    556 ; absolute external ram data
                                    557 ;--------------------------------------------------------
                                    558 	.area XABS    (ABS,XDATA)
                                    559 ;--------------------------------------------------------
                                    560 ; initialized external ram data
                                    561 ;--------------------------------------------------------
                                    562 	.area XISEG   (XDATA)
                                    563 	.area HOME    (CODE)
                                    564 	.area GSINIT0 (CODE)
                                    565 	.area GSINIT1 (CODE)
                                    566 	.area GSINIT2 (CODE)
                                    567 	.area GSINIT3 (CODE)
                                    568 	.area GSINIT4 (CODE)
                                    569 	.area GSINIT5 (CODE)
                                    570 	.area GSINIT  (CODE)
                                    571 	.area GSFINAL (CODE)
                                    572 	.area CSEG    (CODE)
                                    573 ;--------------------------------------------------------
                                    574 ; global & static initialisations
                                    575 ;--------------------------------------------------------
                                    576 	.area HOME    (CODE)
                                    577 	.area GSINIT  (CODE)
                                    578 	.area GSFINAL (CODE)
                                    579 	.area GSINIT  (CODE)
                                    580 ;--------------------------------------------------------
                                    581 ; Home
                                    582 ;--------------------------------------------------------
                                    583 	.area HOME    (CODE)
                                    584 	.area HOME    (CODE)
                                    585 ;--------------------------------------------------------
                                    586 ; code
                                    587 ;--------------------------------------------------------
                                    588 	.area CSEG    (CODE)
                                    589 ;------------------------------------------------------------
                                    590 ;Allocation info for local variables in function 'mulhi8'
                                    591 ;------------------------------------------------------------
                                    592 ;y             Allocated with name '_mulhi8_PARM_2'
                                    593 ;x             Allocated with name '_mulhi8_x_10000_53'
                                    594 ;------------------------------------------------------------
                                    595 ;	quantum/color.c:31: static uint8_t mulhi8(uint8_t x, uint8_t y) __naked {
                                    596 ;	-----------------------------------------
                                    597 ;	 function mulhi8
                                    598 ;	-----------------------------------------
      00793F                        599 _mulhi8:
                                    600 ;	naked function: no prologue.
                                    601 ;	quantum/color.c:40: __endasm;
      00793F 85 82 F0         [24]  602 	mov b,dpl
      007942 90 08 C1         [24]  603 	mov dptr,#_mulhi8_PARM_2
      007945 E0               [24]  604 	movx a,@dptr
      007946 A4               [48]  605 	mul ab
      007947 85 F0 82         [24]  606 	mov dpl,b
      00794A 22               [24]  607 	ret
                                    608 ;	quantum/color.c:41: }
                                    609 ;	naked function: no epilogue.
                                    610 ;------------------------------------------------------------
                                    611 ;Allocation info for local variables in function 'hsv_to_rgb_into'
                                    612 ;------------------------------------------------------------
                                    613 ;hsv           Allocated with name '_hsv_to_rgb_into_PARM_1'
                                    614 ;output        Allocated with name '_hsv_to_rgb_into_PARM_3'
                                    615 ;use_cie       Allocated with name '_hsv_to_rgb_into_use_cie_10000_55'
                                    616 ;rgb           Allocated with name '_hsv_to_rgb_into_rgb_10000_56'
                                    617 ;region        Allocated with name '_hsv_to_rgb_into_region_10000_56'
                                    618 ;remainder     Allocated with name '_hsv_to_rgb_into_remainder_10000_56'
                                    619 ;p             Allocated with name '_hsv_to_rgb_into_p_10000_56'
                                    620 ;q             Allocated with name '_hsv_to_rgb_into_q_10000_56'
                                    621 ;t             Allocated with name '_hsv_to_rgb_into_t_10000_56'
                                    622 ;h             Allocated with name '_hsv_to_rgb_into_h_10000_56'
                                    623 ;s             Allocated with name '_hsv_to_rgb_into_s_10000_56'
                                    624 ;v             Allocated with name '_hsv_to_rgb_into_v_10000_56'
                                    625 ;scaled        Allocated with name '_hsv_to_rgb_into_scaled_10001_65'
                                    626 ;------------------------------------------------------------
                                    627 ;	quantum/color.c:49: void hsv_to_rgb_into(HSV hsv, bool use_cie, RGB __xdata *output) {
                                    628 ;	-----------------------------------------
                                    629 ;	 function hsv_to_rgb_into
                                    630 ;	-----------------------------------------
      00794B                        631 _hsv_to_rgb_into:
                           000007   632 	ar7 = 0x07
                           000006   633 	ar6 = 0x06
                           000005   634 	ar5 = 0x05
                           000004   635 	ar4 = 0x04
                           000003   636 	ar3 = 0x03
                           000002   637 	ar2 = 0x02
                           000001   638 	ar1 = 0x01
                           000000   639 	ar0 = 0x00
      00794B E5 82            [12]  640 	mov	a,dpl
      00794D 90 08 C7         [24]  641 	mov	dptr,#_hsv_to_rgb_into_use_cie_10000_55
      007950 F0               [24]  642 	movx	@dptr,a
                                    643 ;	quantum/color.c:57: if (hsv.s == 0) {
      007951 90 08 C3         [24]  644 	mov	dptr,#(_hsv_to_rgb_into_PARM_1 + 0x0001)
      007954 E0               [24]  645 	movx	a,@dptr
      007955 FF               [12]  646 	mov	r7,a
      007956 70 51            [24]  647 	jnz	00105$
                                    648 ;	quantum/color.c:59: if (use_cie) {
      007958 90 08 C7         [24]  649 	mov	dptr,#_hsv_to_rgb_into_use_cie_10000_55
      00795B E0               [24]  650 	movx	a,@dptr
      00795C 60 1D            [24]  651 	jz	00102$
                                    652 ;	quantum/color.c:60: rgb.r = rgb.g = rgb.b = pgm_read_byte(&CIE1931_CURVE[CIE_INDEX(hsv.v)]);
      00795E 90 08 C4         [24]  653 	mov	dptr,#(_hsv_to_rgb_into_PARM_1 + 0x0002)
      007961 E0               [24]  654 	movx	a,@dptr
      007962 C4               [12]  655 	swap	a
      007963 23               [12]  656 	rl	a
      007964 54 1F            [12]  657 	anl	a,#0x1f
      007966 90 B9 24         [24]  658 	mov	dptr,#_CIE1931_CURVE
      007969 93               [24]  659 	movc	a,@a+dptr
      00796A FE               [12]  660 	mov	r6,a
      00796B 90 08 CA         [24]  661 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0002)
      00796E F0               [24]  662 	movx	@dptr,a
      00796F 90 08 C8         [24]  663 	mov	dptr,#_hsv_to_rgb_into_rgb_10000_56
      007972 EE               [12]  664 	mov	a,r6
      007973 F0               [24]  665 	movx	@dptr,a
      007974 90 08 C9         [24]  666 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0001)
      007977 EE               [12]  667 	mov	a,r6
      007978 F0               [24]  668 	movx	@dptr,a
      007979 80 18            [24]  669 	sjmp	00103$
      00797B                        670 00102$:
                                    671 ;	quantum/color.c:62: rgb.r = hsv.v;
      00797B 90 08 C4         [24]  672 	mov	dptr,#(_hsv_to_rgb_into_PARM_1 + 0x0002)
      00797E E0               [24]  673 	movx	a,@dptr
      00797F 90 08 C9         [24]  674 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0001)
      007982 F0               [24]  675 	movx	@dptr,a
                                    676 ;	quantum/color.c:63: rgb.g = hsv.v;
      007983 90 08 C4         [24]  677 	mov	dptr,#(_hsv_to_rgb_into_PARM_1 + 0x0002)
      007986 E0               [24]  678 	movx	a,@dptr
      007987 90 08 C8         [24]  679 	mov	dptr,#_hsv_to_rgb_into_rgb_10000_56
      00798A F0               [24]  680 	movx	@dptr,a
                                    681 ;	quantum/color.c:64: rgb.b = hsv.v;
      00798B 90 08 C4         [24]  682 	mov	dptr,#(_hsv_to_rgb_into_PARM_1 + 0x0002)
      00798E E0               [24]  683 	movx	a,@dptr
      00798F 90 08 CA         [24]  684 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0002)
      007992 F0               [24]  685 	movx	@dptr,a
      007993                        686 00103$:
                                    687 ;	quantum/color.c:72: *output = rgb;
      007993 90 08 C5         [24]  688 	mov	dptr,#_hsv_to_rgb_into_PARM_3
      007996 E0               [24]  689 	movx	a,@dptr
      007997 FC               [12]  690 	mov	r4,a
      007998 A3               [24]  691 	inc	dptr
      007999 E0               [24]  692 	movx	a,@dptr
      00799A FD               [12]  693 	mov	r5,a
      00799B 7E 00            [12]  694 	mov	r6,#0x00
      00799D 12 7A E6         [24]  695 	lcall	_ak820_outline_0024
      0079A0 8C 82            [24]  696 	mov	dpl, r4
      0079A2 8D 83            [24]  697 	mov	dph, r5
      0079A4 8E F0            [24]  698 	mov	b, r6
                                    699 ;	quantum/color.c:73: return;
      0079A6 02 B4 C1         [24]  700 	ljmp	___memcpy
      0079A9                        701 00105$:
                                    702 ;	quantum/color.c:79: h = hsv.h;
      0079A9 90 08 C2         [24]  703 	mov	dptr,#_hsv_to_rgb_into_PARM_1
      0079AC E0               [24]  704 	movx	a,@dptr
      0079AD FE               [12]  705 	mov	r6,a
                                    706 ;	quantum/color.c:82: if (use_cie) {
      0079AE 90 08 C7         [24]  707 	mov	dptr,#_hsv_to_rgb_into_use_cie_10000_55
      0079B1 E0               [24]  708 	movx	a,@dptr
      0079B2 60 12            [24]  709 	jz	00107$
                                    710 ;	quantum/color.c:83: v = pgm_read_byte(&CIE1931_CURVE[CIE_INDEX(hsv.v)]);
      0079B4 90 08 C4         [24]  711 	mov	dptr,#(_hsv_to_rgb_into_PARM_1 + 0x0002)
      0079B7 E0               [24]  712 	movx	a,@dptr
      0079B8 C4               [12]  713 	swap	a
      0079B9 23               [12]  714 	rl	a
      0079BA 54 1F            [12]  715 	anl	a,#0x1f
      0079BC 90 B9 24         [24]  716 	mov	dptr,#_CIE1931_CURVE
      0079BF 93               [24]  717 	movc	a,@a+dptr
      0079C0 90 08 CB         [24]  718 	mov	dptr,#_hsv_to_rgb_into_v_10000_56
      0079C3 F0               [24]  719 	movx	@dptr,a
      0079C4 80 08            [24]  720 	sjmp	00108$
      0079C6                        721 00107$:
                                    722 ;	quantum/color.c:85: v = hsv.v;
      0079C6 90 08 C4         [24]  723 	mov	dptr,#(_hsv_to_rgb_into_PARM_1 + 0x0002)
      0079C9 E0               [24]  724 	movx	a,@dptr
      0079CA 90 08 CB         [24]  725 	mov	dptr,#_hsv_to_rgb_into_v_10000_56
      0079CD F0               [24]  726 	movx	@dptr,a
      0079CE                        727 00108$:
                                    728 ;	quantum/color.c:91: uint16_t scaled = (uint16_t)h * 6;
      0079CE 8E 05            [24]  729 	mov	ar5,r6
      0079D0 ED               [12]  730 	mov	a,r5
      0079D1 75 F0 06         [24]  731 	mov	b,#0x06
      0079D4 A4               [48]  732 	mul	ab
      0079D5 FD               [12]  733 	mov	r5,a
      0079D6 AC F0            [24]  734 	mov	r4,b
                                    735 ;	quantum/color.c:92: region = (scaled + 1 + (scaled >> 8)) >> 8;
      0079D8 8D 02            [24]  736 	mov	ar2,r5
      0079DA 8C 03            [24]  737 	mov	ar3,r4
      0079DC 0A               [12]  738 	inc	r2
      0079DD BA 00 01         [24]  739 	cjne	r2,#0x00,00150$
      0079E0 0B               [12]  740 	inc	r3
      0079E1                        741 00150$:
      0079E1 8C 05            [24]  742 	mov	ar5,r4
      0079E3 7C 00            [12]  743 	mov	r4,#0x00
      0079E5 ED               [12]  744 	mov	a,r5
      0079E6 2A               [12]  745 	add	a, r2
      0079E7 EC               [12]  746 	mov	a,r4
      0079E8 3B               [12]  747 	addc	a, r3
      0079E9 FD               [12]  748 	mov	r5,a
                                    749 ;	quantum/color.c:93: remainder = (h * 2 - region * 85) * 3;
      0079EA EE               [12]  750 	mov	a,r6
      0079EB 2E               [12]  751 	add	a,r6
      0079EC FE               [12]  752 	mov	r6,a
      0079ED 8D 04            [24]  753 	mov	ar4,r5
      0079EF EC               [12]  754 	mov	a,r4
      0079F0 75 F0 55         [24]  755 	mov	b,#0x55
      0079F3 A4               [48]  756 	mul	ab
      0079F4 D3               [12]  757 	setb	c
      0079F5 9E               [12]  758 	subb	a,r6
      0079F6 F4               [12]  759 	cpl	a
      0079F7 75 F0 03         [24]  760 	mov	b,#0x03
      0079FA A4               [48]  761 	mul	ab
      0079FB FE               [12]  762 	mov	r6,a
                                    763 ;	quantum/color.c:95: p = mulhi8(v, 255 - s);
      0079FC 90 08 CB         [24]  764 	mov	dptr,#_hsv_to_rgb_into_v_10000_56
      0079FF E0               [24]  765 	movx	a,@dptr
      007A00 FC               [12]  766 	mov	r4,a
      007A01 8F 03            [24]  767 	mov	ar3,r7
      007A03 90 08 C1         [24]  768 	mov	dptr,#_mulhi8_PARM_2
      007A06 74 FF            [12]  769 	mov	a,#0xff
      007A08 C3               [12]  770 	clr	c
      007A09 9B               [12]  771 	subb	a,r3
      007A0A F0               [24]  772 	movx	@dptr,a
      007A0B 8C 82            [24]  773 	mov	dpl, r4
      007A0D 12 79 3F         [24]  774 	lcall	_mulhi8
      007A10 AB 82            [24]  775 	mov	r3, dpl
                                    776 ;	quantum/color.c:96: q = mulhi8(v, 255 - mulhi8(s, remainder));
      007A12 90 08 C1         [24]  777 	mov	dptr,#_mulhi8_PARM_2
      007A15 EE               [12]  778 	mov	a,r6
      007A16 F0               [24]  779 	movx	@dptr,a
      007A17 8F 82            [24]  780 	mov	dpl, r7
      007A19 12 79 3F         [24]  781 	lcall	_mulhi8
      007A1C AA 82            [24]  782 	mov	r2, dpl
      007A1E 90 08 C1         [24]  783 	mov	dptr,#_mulhi8_PARM_2
      007A21 74 FF            [12]  784 	mov	a,#0xff
      007A23 C3               [12]  785 	clr	c
      007A24 9A               [12]  786 	subb	a,r2
      007A25 F0               [24]  787 	movx	@dptr,a
      007A26 8C 82            [24]  788 	mov	dpl, r4
      007A28 12 79 3F         [24]  789 	lcall	_mulhi8
      007A2B AA 82            [24]  790 	mov	r2, dpl
                                    791 ;	quantum/color.c:97: t = mulhi8(v, 255 - mulhi8(s, 255 - remainder));
      007A2D 90 08 C1         [24]  792 	mov	dptr,#_mulhi8_PARM_2
      007A30 74 FF            [12]  793 	mov	a,#0xff
      007A32 C3               [12]  794 	clr	c
      007A33 9E               [12]  795 	subb	a,r6
      007A34 F0               [24]  796 	movx	@dptr,a
      007A35 8F 82            [24]  797 	mov	dpl, r7
      007A37 12 79 3F         [24]  798 	lcall	_mulhi8
      007A3A AF 82            [24]  799 	mov	r7, dpl
      007A3C 90 08 C1         [24]  800 	mov	dptr,#_mulhi8_PARM_2
      007A3F 74 FF            [12]  801 	mov	a,#0xff
      007A41 C3               [12]  802 	clr	c
      007A42 9F               [12]  803 	subb	a,r7
      007A43 F0               [24]  804 	movx	@dptr,a
      007A44 8C 82            [24]  805 	mov	dpl, r4
      007A46 12 79 3F         [24]  806 	lcall	_mulhi8
      007A49 AF 82            [24]  807 	mov	r7, dpl
                                    808 ;	quantum/color.c:99: switch (region) {
      007A4B ED               [12]  809 	mov	a,r5
      007A4C 24 F9            [12]  810 	add	a,#0xff - 0x06
      007A4E 40 6E            [24]  811 	jc	00115$
                                    812 ;	free result
      007A50 ED               [12]  813 	mov	a,r5
      007A51 2D               [12]  814 	add	a,r5
      007A52 2D               [12]  815 	add	a,r5
      007A53 90 7A 57         [24]  816 	mov	dptr,#00152$
      007A56 73               [24]  817 	jmp	@a+dptr
      007A57                        818 00152$:
      007A57 02 7A 69         [24]  819 	ljmp	00110$
      007A5A 02 7A 7A         [24]  820 	ljmp	00111$
      007A5D 02 7A 8B         [24]  821 	ljmp	00112$
      007A60 02 7A 9C         [24]  822 	ljmp	00113$
      007A63 02 7A AD         [24]  823 	ljmp	00114$
      007A66 02 7A BE         [24]  824 	ljmp	00115$
                                    825 ;	quantum/color.c:101: case 0:
      007A69                        826 00110$:
                                    827 ;	quantum/color.c:102: rgb.r = v;
      007A69 90 08 C9         [24]  828 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0001)
      007A6C EC               [12]  829 	mov	a,r4
      007A6D F0               [24]  830 	movx	@dptr,a
                                    831 ;	quantum/color.c:103: rgb.g = t;
      007A6E 90 08 C8         [24]  832 	mov	dptr,#_hsv_to_rgb_into_rgb_10000_56
      007A71 EF               [12]  833 	mov	a,r7
      007A72 F0               [24]  834 	movx	@dptr,a
                                    835 ;	quantum/color.c:104: rgb.b = p;
      007A73 90 08 CA         [24]  836 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0002)
      007A76 EB               [12]  837 	mov	a,r3
      007A77 F0               [24]  838 	movx	@dptr,a
                                    839 ;	quantum/color.c:105: break;
                                    840 ;	quantum/color.c:106: case 1:
      007A78 80 56            [24]  841 	sjmp	00116$
      007A7A                        842 00111$:
                                    843 ;	quantum/color.c:107: rgb.r = q;
      007A7A 90 08 C9         [24]  844 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0001)
      007A7D EA               [12]  845 	mov	a,r2
      007A7E F0               [24]  846 	movx	@dptr,a
                                    847 ;	quantum/color.c:108: rgb.g = v;
      007A7F 90 08 C8         [24]  848 	mov	dptr,#_hsv_to_rgb_into_rgb_10000_56
      007A82 EC               [12]  849 	mov	a,r4
      007A83 F0               [24]  850 	movx	@dptr,a
                                    851 ;	quantum/color.c:109: rgb.b = p;
      007A84 90 08 CA         [24]  852 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0002)
      007A87 EB               [12]  853 	mov	a,r3
      007A88 F0               [24]  854 	movx	@dptr,a
                                    855 ;	quantum/color.c:110: break;
                                    856 ;	quantum/color.c:111: case 2:
      007A89 80 45            [24]  857 	sjmp	00116$
      007A8B                        858 00112$:
                                    859 ;	quantum/color.c:112: rgb.r = p;
      007A8B 90 08 C9         [24]  860 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0001)
      007A8E EB               [12]  861 	mov	a,r3
      007A8F F0               [24]  862 	movx	@dptr,a
                                    863 ;	quantum/color.c:113: rgb.g = v;
      007A90 90 08 C8         [24]  864 	mov	dptr,#_hsv_to_rgb_into_rgb_10000_56
      007A93 EC               [12]  865 	mov	a,r4
      007A94 F0               [24]  866 	movx	@dptr,a
                                    867 ;	quantum/color.c:114: rgb.b = t;
      007A95 90 08 CA         [24]  868 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0002)
      007A98 EF               [12]  869 	mov	a,r7
      007A99 F0               [24]  870 	movx	@dptr,a
                                    871 ;	quantum/color.c:115: break;
                                    872 ;	quantum/color.c:116: case 3:
      007A9A 80 34            [24]  873 	sjmp	00116$
      007A9C                        874 00113$:
                                    875 ;	quantum/color.c:117: rgb.r = p;
      007A9C 90 08 C9         [24]  876 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0001)
      007A9F EB               [12]  877 	mov	a,r3
      007AA0 F0               [24]  878 	movx	@dptr,a
                                    879 ;	quantum/color.c:118: rgb.g = q;
      007AA1 90 08 C8         [24]  880 	mov	dptr,#_hsv_to_rgb_into_rgb_10000_56
      007AA4 EA               [12]  881 	mov	a,r2
      007AA5 F0               [24]  882 	movx	@dptr,a
                                    883 ;	quantum/color.c:119: rgb.b = v;
      007AA6 90 08 CA         [24]  884 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0002)
      007AA9 EC               [12]  885 	mov	a,r4
      007AAA F0               [24]  886 	movx	@dptr,a
                                    887 ;	quantum/color.c:120: break;
                                    888 ;	quantum/color.c:121: case 4:
      007AAB 80 23            [24]  889 	sjmp	00116$
      007AAD                        890 00114$:
                                    891 ;	quantum/color.c:122: rgb.r = t;
      007AAD 90 08 C9         [24]  892 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0001)
      007AB0 EF               [12]  893 	mov	a,r7
      007AB1 F0               [24]  894 	movx	@dptr,a
                                    895 ;	quantum/color.c:123: rgb.g = p;
      007AB2 90 08 C8         [24]  896 	mov	dptr,#_hsv_to_rgb_into_rgb_10000_56
      007AB5 EB               [12]  897 	mov	a,r3
      007AB6 F0               [24]  898 	movx	@dptr,a
                                    899 ;	quantum/color.c:124: rgb.b = v;
      007AB7 90 08 CA         [24]  900 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0002)
      007ABA EC               [12]  901 	mov	a,r4
      007ABB F0               [24]  902 	movx	@dptr,a
                                    903 ;	quantum/color.c:125: break;
                                    904 ;	quantum/color.c:126: default:
      007ABC 80 12            [24]  905 	sjmp	00116$
      007ABE                        906 00115$:
                                    907 ;	quantum/color.c:127: rgb.r = v;
      007ABE 90 08 CB         [24]  908 	mov	dptr,#_hsv_to_rgb_into_v_10000_56
      007AC1 E0               [24]  909 	movx	a,@dptr
      007AC2 90 08 C9         [24]  910 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0001)
      007AC5 F0               [24]  911 	movx	@dptr,a
                                    912 ;	quantum/color.c:128: rgb.g = p;
      007AC6 90 08 C8         [24]  913 	mov	dptr,#_hsv_to_rgb_into_rgb_10000_56
      007AC9 EB               [12]  914 	mov	a,r3
      007ACA F0               [24]  915 	movx	@dptr,a
                                    916 ;	quantum/color.c:129: rgb.b = q;
      007ACB 90 08 CA         [24]  917 	mov	dptr,#(_hsv_to_rgb_into_rgb_10000_56 + 0x0002)
      007ACE EA               [12]  918 	mov	a,r2
      007ACF F0               [24]  919 	movx	@dptr,a
                                    920 ;	quantum/color.c:131: }
      007AD0                        921 00116$:
                                    922 ;	quantum/color.c:134: *output = rgb;
      007AD0 90 08 C5         [24]  923 	mov	dptr,#_hsv_to_rgb_into_PARM_3
      007AD3 E0               [24]  924 	movx	a,@dptr
      007AD4 FD               [12]  925 	mov	r5,a
      007AD5 A3               [24]  926 	inc	dptr
      007AD6 E0               [24]  927 	movx	a,@dptr
      007AD7 FE               [12]  928 	mov	r6,a
      007AD8 7F 00            [12]  929 	mov	r7,#0x00
      007ADA 12 7A E6         [24]  930 	lcall	_ak820_outline_0024
      007ADD 8D 82            [24]  931 	mov	dpl, r5
      007ADF 8E 83            [24]  932 	mov	dph, r6
      007AE1 8F F0            [24]  933 	mov	b, r7
                                    934 ;	quantum/color.c:138: }
      007AE3 02 B4 C1         [24]  935 	ljmp	___memcpy
                                    936 ;------------------------------------------------------------
                                    937 ;Allocation info for local variables in function 'hsv_to_rgb_impl'
                                    938 ;------------------------------------------------------------
                                    939 ;hsv           Allocated with name '_hsv_to_rgb_impl_PARM_1'
                                    940 ;use_cie       Allocated with name '_hsv_to_rgb_impl_PARM_2'
                                    941 ;rgb           Allocated with name '_hsv_to_rgb_impl_rgb_10000_69'
                                    942 ;------------------------------------------------------------
                                    943 ;	quantum/color.c:143: RGB hsv_to_rgb_impl(HSV hsv, bool use_cie) {
                                    944 ;	-----------------------------------------
                                    945 	.area CSEG    (CODE)
                                    946 	.area CONST   (CODE)
                                    947 	.area XINIT   (CODE)
                                    948 	.area CABS    (ABS,CODE)
                                    949 
                                    950 ; Experimental exact instruction outlining.
                                    951 	.globl _ak820_outline_0024
                                    952 
                                    953 	.area CSEG (CODE)
                                    954 ; function ak820_outline_0024
      007AE6                        955 _ak820_outline_0024:
      007AE6 90 0B 90         [24]  956 	mov	dptr,#___memcpy_PARM_2
      007AE9 74 C8            [12]  957 	mov	a,#_hsv_to_rgb_into_rgb_10000_56
      007AEB F0               [24]  958 	movx	@dptr,a
      007AEC 74 08            [12]  959 	mov	a,#(_hsv_to_rgb_into_rgb_10000_56>>8)
      007AEE A3               [24]  960 	inc	dptr
      007AEF F0               [24]  961 	movx	@dptr,a
      007AF0 E4               [12]  962 	clr	a
      007AF1 A3               [24]  963 	inc	dptr
      007AF2 F0               [24]  964 	movx	@dptr,a
      007AF3 90 0B 93         [24]  965 	mov	dptr,#___memcpy_PARM_3
      007AF6 74 03            [12]  966 	mov	a,#0x03
      007AF8 F0               [24]  967 	movx	@dptr,a
      007AF9 E4               [12]  968 	clr	a
      007AFA A3               [24]  969 	inc	dptr
      007AFB F0               [24]  970 	movx	@dptr,a
      007AFC 22               [24]  971 	ret
