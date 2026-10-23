                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module sendchar
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
                                    254 	.globl _sendchar
                                    255 ;--------------------------------------------------------
                                    256 ; special function registers
                                    257 ;--------------------------------------------------------
                                    258 	.area RSEG    (ABS,DATA)
      000000                        259 	.org 0x0000
                           0000D0   260 _PSW	=	0x00d0
                           0000E0   261 _ACC	=	0x00e0
                           0000F0   262 _B	=	0x00f0
                           0000FD   263 _A_INV	=	0x00fd
                           000081   264 _SP	=	0x0081
                           000082   265 _DPL	=	0x0082
                           000083   266 _DPH	=	0x0083
                           0000A1   267 _SAFE_MOD	=	0x00a1
                           0000B1   268 _GLOBAL_CFG	=	0x00b1
                           000087   269 _PCON	=	0x0087
                           0000BA   270 _POWER_CFG	=	0x00ba
                           0000B9   271 _CLOCK_CFG	=	0x00b9
                           0000A9   272 _WAKE_CTRL	=	0x00a9
                           0000FE   273 _RESET_KEEP	=	0x00fe
                           0000FF   274 _WDOG_COUNT	=	0x00ff
                           0000A8   275 _IE	=	0x00a8
                           0000B8   276 _IP	=	0x00b8
                           0000E8   277 _IE_EX	=	0x00e8
                           0000E9   278 _IP_EX	=	0x00e9
                           0000B2   279 _GPIO_IE	=	0x00b2
                           008584   280 _ROM_ADDR	=	0x8584
                           000084   281 _ROM_ADDR_L	=	0x0084
                           000085   282 _ROM_ADDR_H	=	0x0085
                           008F8E   283 _ROM_DATA_HI	=	0x8f8e
                           00008E   284 _ROM_DATA_HL	=	0x008e
                           00008F   285 _ROM_DATA_HH	=	0x008f
                           000086   286 _ROM_CTRL	=	0x0086
                           000080   287 _P0	=	0x0080
                           0000C4   288 _P0_MOD_OC	=	0x00c4
                           0000C5   289 _P0_DIR_PU	=	0x00c5
                           000090   290 _P1	=	0x0090
                           000092   291 _P1_MOD_OC	=	0x0092
                           000093   292 _P1_DIR_PU	=	0x0093
                           0000A0   293 _P2	=	0x00a0
                           000094   294 _P2_MOD_OC	=	0x0094
                           000095   295 _P2_DIR_PU	=	0x0095
                           0000B0   296 _P3	=	0x00b0
                           000096   297 _P3_MOD_OC	=	0x0096
                           000097   298 _P3_DIR_PU	=	0x0097
                           0000C0   299 _P4	=	0x00c0
                           0000C2   300 _P4_MOD_OC	=	0x00c2
                           0000C3   301 _P4_DIR_PU	=	0x00c3
                           0000C1   302 _P4_LED_KEY	=	0x00c1
                           0000AA   303 _P5_IN	=	0x00aa
                           0000AB   304 _P5_OUT_PU	=	0x00ab
                           0000AC   305 _P5_DIR	=	0x00ac
                           0000AD   306 _P6_IN	=	0x00ad
                           0000AE   307 _P6_OUT_PU	=	0x00ae
                           0000AF   308 _P6_DIR	=	0x00af
                           0000F1   309 _P7	=	0x00f1
                           0000A2   310 _XBUS_AUX	=	0x00a2
                           000088   311 _TCON	=	0x0088
                           000089   312 _TMOD	=	0x0089
                           00008A   313 _TL0	=	0x008a
                           00008B   314 _TL1	=	0x008b
                           00008C   315 _TH0	=	0x008c
                           00008D   316 _TH1	=	0x008d
                           000098   317 _SCON	=	0x0098
                           000099   318 _SBUF	=	0x0099
                           0000C8   319 _T2CON	=	0x00c8
                           0000C9   320 _T2MOD	=	0x00c9
                           00CBCA   321 _RCAP2	=	0xcbca
                           0000CA   322 _RCAP2L	=	0x00ca
                           0000CB   323 _RCAP2H	=	0x00cb
                           00CDCC   324 _T2COUNT	=	0xcdcc
                           0000CC   325 _TL2	=	0x00cc
                           0000CD   326 _TH2	=	0x00cd
                           00CFCE   327 _T2CAP1	=	0xcfce
                           0000CE   328 _T2CAP1L	=	0x00ce
                           0000CF   329 _T2CAP1H	=	0x00cf
                           0000F8   330 _SPI0_STAT	=	0x00f8
                           0000F9   331 _SPI0_DATA	=	0x00f9
                           0000FA   332 _SPI0_CTRL	=	0x00fa
                           0000FB   333 _SPI0_CK_SE	=	0x00fb
                           0000FC   334 _SPI0_SETUP	=	0x00fc
                           0000BC   335 _SCON1	=	0x00bc
                           0000BD   336 _SBUF1	=	0x00bd
                           0000BE   337 _SBAUD1	=	0x00be
                           0000BF   338 _SIF1	=	0x00bf
                           0000B4   339 _SPI1_STAT	=	0x00b4
                           0000B5   340 _SPI1_DATA	=	0x00b5
                           0000B6   341 _SPI1_CTRL	=	0x00b6
                           0000B7   342 _SPI1_CK_SE	=	0x00b7
                           0000F3   343 _ADC_CTRL	=	0x00f3
                           00F5F4   344 _ADC_DAT	=	0xf5f4
                           0000F4   345 _ADC_DAT_L	=	0x00f4
                           0000F5   346 _ADC_DAT_H	=	0x00f5
                           0000F6   347 _ADC_CHAN	=	0x00f6
                           0000A6   348 _LED_COMMON	=	0x00a6
                           0000A7   349 _LED_PWM_OE	=	0x00a7
                           00C7C6   350 _LED_DMA	=	0xc7c6
                           0000C6   351 _LED_DMA_L	=	0x00c6
                           0000C7   352 _LED_DMA_H	=	0x00c7
                           0000F7   353 _LED_STATUS	=	0x00f7
                           0000B3   354 _I2CX_INT	=	0x00b3
                           0000BB   355 _I2CS_INT_ST	=	0x00bb
                                    356 ;--------------------------------------------------------
                                    357 ; special function bits
                                    358 ;--------------------------------------------------------
                                    359 	.area RSEG    (ABS,DATA)
      000000                        360 	.org 0x0000
                           0000D7   361 _CY	=	0x00d7
                           0000D6   362 _AC	=	0x00d6
                           0000D5   363 _F0	=	0x00d5
                           0000D4   364 _RS1	=	0x00d4
                           0000D3   365 _RS0	=	0x00d3
                           0000D2   366 _OV	=	0x00d2
                           0000D1   367 _F1	=	0x00d1
                           0000D0   368 _P	=	0x00d0
                           0000AF   369 _EA	=	0x00af
                           0000AE   370 _E_DIS	=	0x00ae
                           0000AD   371 _ET2	=	0x00ad
                           0000AC   372 _ES	=	0x00ac
                           0000AB   373 _ET1	=	0x00ab
                           0000AA   374 _EX1	=	0x00aa
                           0000A9   375 _ET0	=	0x00a9
                           0000A8   376 _EX0	=	0x00a8
                           0000BF   377 _PH_FLAG	=	0x00bf
                           0000BE   378 _PL_FLAG	=	0x00be
                           0000BD   379 _PT2	=	0x00bd
                           0000BC   380 _PS	=	0x00bc
                           0000BB   381 _PT1	=	0x00bb
                           0000BA   382 _PX1	=	0x00ba
                           0000B9   383 _PT0	=	0x00b9
                           0000B8   384 _PX0	=	0x00b8
                           0000EF   385 _IE_WDOG	=	0x00ef
                           0000EE   386 _IE_GPIO	=	0x00ee
                           0000ED   387 _IE_PWM_I2C	=	0x00ed
                           0000EC   388 _IE_UART1	=	0x00ec
                           0000EB   389 _IE_ADC	=	0x00eb
                           0000E9   390 _IE_USB	=	0x00e9
                           0000E8   391 _IE_SPI0	=	0x00e8
                           000087   392 _P0_7	=	0x0087
                           000086   393 _P0_6	=	0x0086
                           000085   394 _P0_5	=	0x0085
                           000084   395 _P0_4	=	0x0084
                           000083   396 _P0_3	=	0x0083
                           000082   397 _P0_2	=	0x0082
                           000081   398 _P0_1	=	0x0081
                           000080   399 _P0_0	=	0x0080
                           000081   400 _SDA0	=	0x0081
                           000080   401 _SCL0	=	0x0080
                           000083   402 _TXD_	=	0x0083
                           000082   403 _RXD_	=	0x0082
                           000085   404 _AIN13	=	0x0085
                           000084   405 _AIN12	=	0x0084
                           000083   406 _AIN11	=	0x0083
                           000082   407 _AIN10	=	0x0082
                           000081   408 _AIN9	=	0x0081
                           000080   409 _AIN8	=	0x0080
                           000097   410 _P1_7	=	0x0097
                           000096   411 _P1_6	=	0x0096
                           000095   412 _P1_5	=	0x0095
                           000094   413 _P1_4	=	0x0094
                           000093   414 _P1_3	=	0x0093
                           000092   415 _P1_2	=	0x0092
                           000091   416 _P1_1	=	0x0091
                           000090   417 _P1_0	=	0x0090
                           000097   418 _TXD1_	=	0x0097
                           000096   419 _RXD1_	=	0x0096
                           000097   420 _SCK	=	0x0097
                           000096   421 _MISO	=	0x0096
                           000095   422 _MOSI	=	0x0095
                           000094   423 _SCS	=	0x0094
                           000092   424 _INT0_	=	0x0092
                           000091   425 _T2EX	=	0x0091
                           000091   426 _CAP2	=	0x0091
                           000090   427 _T2	=	0x0090
                           000090   428 _CAP1	=	0x0090
                           000097   429 _AIN7	=	0x0097
                           000096   430 _AIN6	=	0x0096
                           000095   431 _AIN5	=	0x0095
                           000094   432 _AIN4	=	0x0094
                           000093   433 _AIN3	=	0x0093
                           000092   434 _AIN2	=	0x0092
                           000091   435 _AIN1	=	0x0091
                           000090   436 _AIN0	=	0x0090
                           0000A7   437 _P2_7	=	0x00a7
                           0000A6   438 _P2_6	=	0x00a6
                           0000A5   439 _P2_5	=	0x00a5
                           0000A4   440 _P2_4	=	0x00a4
                           0000A3   441 _P2_3	=	0x00a3
                           0000A2   442 _P2_2	=	0x00a2
                           0000A1   443 _P2_1	=	0x00a1
                           0000A0   444 _P2_0	=	0x00a0
                           0000A7   445 _TXD1	=	0x00a7
                           0000A6   446 _RXD1	=	0x00a6
                           0000A5   447 _T2EX_	=	0x00a5
                           0000A5   448 _CAP2_	=	0x00a5
                           0000A4   449 _T2_	=	0x00a4
                           0000A4   450 _CAP1_	=	0x00a4
                           0000B7   451 _P3_7	=	0x00b7
                           0000B6   452 _P3_6	=	0x00b6
                           0000B5   453 _P3_5	=	0x00b5
                           0000B4   454 _P3_4	=	0x00b4
                           0000B3   455 _P3_3	=	0x00b3
                           0000B2   456 _P3_2	=	0x00b2
                           0000B1   457 _P3_1	=	0x00b1
                           0000B0   458 _P3_0	=	0x00b0
                           0000B7   459 _SCK1	=	0x00b7
                           0000B6   460 _MISO1	=	0x00b6
                           0000B5   461 _MOSI1	=	0x00b5
                           0000B5   462 _T1	=	0x00b5
                           0000B4   463 _T0	=	0x00b4
                           0000B3   464 _INT1	=	0x00b3
                           0000B2   465 _INT0	=	0x00b2
                           0000B1   466 _TXD	=	0x00b1
                           0000B0   467 _RXD	=	0x00b0
                           0000C6   468 _P4_6	=	0x00c6
                           0000C5   469 _P4_5	=	0x00c5
                           0000C4   470 _P4_4	=	0x00c4
                           0000C3   471 _P4_3	=	0x00c3
                           0000C2   472 _P4_2	=	0x00c2
                           0000C1   473 _P4_1	=	0x00c1
                           0000C0   474 _P4_0	=	0x00c0
                           00008F   475 _TF1	=	0x008f
                           00008E   476 _TR1	=	0x008e
                           00008D   477 _TF0	=	0x008d
                           00008C   478 _TR0	=	0x008c
                           00008B   479 _IE1	=	0x008b
                           00008A   480 _IT1	=	0x008a
                           000089   481 _IE0	=	0x0089
                           000088   482 _IT0	=	0x0088
                           00009F   483 _SM0	=	0x009f
                           00009E   484 _SM1	=	0x009e
                           00009D   485 _SM2	=	0x009d
                           00009C   486 _REN	=	0x009c
                           00009B   487 _TB8	=	0x009b
                           00009A   488 _RB8	=	0x009a
                           000099   489 _TI	=	0x0099
                           000098   490 _RI	=	0x0098
                           0000CF   491 _TF2	=	0x00cf
                           0000CF   492 _CAP1F	=	0x00cf
                           0000CE   493 _EXF2	=	0x00ce
                           0000CD   494 _RCLK	=	0x00cd
                           0000CC   495 _TCLK	=	0x00cc
                           0000CB   496 _EXEN2	=	0x00cb
                           0000CA   497 _TR2	=	0x00ca
                           0000C9   498 _C_T2	=	0x00c9
                           0000C8   499 _CP_RL2	=	0x00c8
                           0000FF   500 _S0_FST_ACT	=	0x00ff
                           0000FE   501 _S0_IF_OV	=	0x00fe
                           0000FD   502 _S0_IF_FIRST	=	0x00fd
                           0000FC   503 _S0_IF_BYTE	=	0x00fc
                           0000FB   504 _S0_FREE	=	0x00fb
                           0000FA   505 _S0_T_FIFO	=	0x00fa
                           0000F8   506 _S0_R_FIFO	=	0x00f8
                           0000F7   507 _ADC_START	=	0x00f7
                                    508 ;--------------------------------------------------------
                                    509 ; overlayable register banks
                                    510 ;--------------------------------------------------------
                                    511 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        512 	.ds 8
                                    513 ;--------------------------------------------------------
                                    514 ; internal ram data
                                    515 ;--------------------------------------------------------
                                    516 	.area DSEG    (DATA)
                                    517 ;--------------------------------------------------------
                                    518 ; overlayable items in internal ram
                                    519 ;--------------------------------------------------------
                                    520 ;--------------------------------------------------------
                                    521 ; indirectly addressable internal ram data
                                    522 ;--------------------------------------------------------
                                    523 	.area ISEG    (DATA)
                                    524 ;--------------------------------------------------------
                                    525 ; absolute internal ram data
                                    526 ;--------------------------------------------------------
                                    527 	.area IABS    (ABS,DATA)
                                    528 	.area IABS    (ABS,DATA)
                                    529 ;--------------------------------------------------------
                                    530 ; bit data
                                    531 ;--------------------------------------------------------
                                    532 	.area BSEG    (BIT)
                                    533 ;--------------------------------------------------------
                                    534 ; paged external ram data
                                    535 ;--------------------------------------------------------
                                    536 	.area PSEG    (PAG,XDATA)
                                    537 ;--------------------------------------------------------
                                    538 ; uninitialized external ram data
                                    539 ;--------------------------------------------------------
                                    540 	.area XSEG    (XDATA)
                                    541 ;--------------------------------------------------------
                                    542 ; absolute external ram data
                                    543 ;--------------------------------------------------------
                                    544 	.area XABS    (ABS,XDATA)
                                    545 ;--------------------------------------------------------
                                    546 ; initialized external ram data
                                    547 ;--------------------------------------------------------
                                    548 	.area XISEG   (XDATA)
                                    549 	.area HOME    (CODE)
                                    550 	.area GSINIT0 (CODE)
                                    551 	.area GSINIT1 (CODE)
                                    552 	.area GSINIT2 (CODE)
                                    553 	.area GSINIT3 (CODE)
                                    554 	.area GSINIT4 (CODE)
                                    555 	.area GSINIT5 (CODE)
                                    556 	.area GSINIT  (CODE)
                                    557 	.area GSFINAL (CODE)
                                    558 	.area CSEG    (CODE)
                                    559 ;--------------------------------------------------------
                                    560 ; global & static initialisations
                                    561 ;--------------------------------------------------------
                                    562 	.area HOME    (CODE)
                                    563 	.area GSINIT  (CODE)
                                    564 	.area GSFINAL (CODE)
                                    565 	.area GSINIT  (CODE)
                                    566 ;--------------------------------------------------------
                                    567 ; Home
                                    568 ;--------------------------------------------------------
                                    569 	.area HOME    (CODE)
                                    570 	.area HOME    (CODE)
                                    571 ;--------------------------------------------------------
                                    572 ; code
                                    573 ;--------------------------------------------------------
                                    574 	.area CSEG    (CODE)
                                    575 ;------------------------------------------------------------
                                    576 ;Allocation info for local variables in function 'sendchar'
                                    577 ;------------------------------------------------------------
                                    578 ;c             Allocated with name '_sendchar_c_10000_42'
                                    579 ;------------------------------------------------------------
                                    580 ;	quantum/logging/sendchar.c:21: __attribute__((weak)) int8_t sendchar(uint8_t c) {
                                    581 ;	-----------------------------------------
                                    582 ;	 function sendchar
                                    583 ;	-----------------------------------------
      009189                        584 _sendchar:
                           000007   585 	ar7 = 0x07
                           000006   586 	ar6 = 0x06
                           000005   587 	ar5 = 0x05
                           000004   588 	ar4 = 0x04
                           000003   589 	ar3 = 0x03
                           000002   590 	ar2 = 0x02
                           000001   591 	ar1 = 0x01
                           000000   592 	ar0 = 0x00
                                    593 ;	quantum/logging/sendchar.c:22: return 0;
      009189 75 82 00         [24]  594 	mov	dpl, #0x00
                                    595 ;	quantum/logging/sendchar.c:23: }
      00918C 22               [24]  596 	ret
                                    597 	.area CSEG    (CODE)
                                    598 	.area CONST   (CODE)
                                    599 	.area XINIT   (CODE)
                                    600 	.area CABS    (ABS,CODE)
