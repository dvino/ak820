                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module gpio
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _pin_to_pinmask
                                     12 	.globl _ADC_START
                                     13 	.globl _S0_R_FIFO
                                     14 	.globl _S0_T_FIFO
                                     15 	.globl _S0_FREE
                                     16 	.globl _S0_IF_BYTE
                                     17 	.globl _S0_IF_FIRST
                                     18 	.globl _S0_IF_OV
                                     19 	.globl _S0_FST_ACT
                                     20 	.globl _CP_RL2
                                     21 	.globl _C_T2
                                     22 	.globl _TR2
                                     23 	.globl _EXEN2
                                     24 	.globl _TCLK
                                     25 	.globl _RCLK
                                     26 	.globl _EXF2
                                     27 	.globl _CAP1F
                                     28 	.globl _TF2
                                     29 	.globl _RI
                                     30 	.globl _TI
                                     31 	.globl _RB8
                                     32 	.globl _TB8
                                     33 	.globl _REN
                                     34 	.globl _SM2
                                     35 	.globl _SM1
                                     36 	.globl _SM0
                                     37 	.globl _IT0
                                     38 	.globl _IE0
                                     39 	.globl _IT1
                                     40 	.globl _IE1
                                     41 	.globl _TR0
                                     42 	.globl _TF0
                                     43 	.globl _TR1
                                     44 	.globl _TF1
                                     45 	.globl _P4_0
                                     46 	.globl _P4_1
                                     47 	.globl _P4_2
                                     48 	.globl _P4_3
                                     49 	.globl _P4_4
                                     50 	.globl _P4_5
                                     51 	.globl _P4_6
                                     52 	.globl _RXD
                                     53 	.globl _TXD
                                     54 	.globl _INT0
                                     55 	.globl _INT1
                                     56 	.globl _T0
                                     57 	.globl _T1
                                     58 	.globl _MOSI1
                                     59 	.globl _MISO1
                                     60 	.globl _SCK1
                                     61 	.globl _P3_0
                                     62 	.globl _P3_1
                                     63 	.globl _P3_2
                                     64 	.globl _P3_3
                                     65 	.globl _P3_4
                                     66 	.globl _P3_5
                                     67 	.globl _P3_6
                                     68 	.globl _P3_7
                                     69 	.globl _CAP1_
                                     70 	.globl _T2_
                                     71 	.globl _CAP2_
                                     72 	.globl _T2EX_
                                     73 	.globl _RXD1
                                     74 	.globl _TXD1
                                     75 	.globl _P2_0
                                     76 	.globl _P2_1
                                     77 	.globl _P2_2
                                     78 	.globl _P2_3
                                     79 	.globl _P2_4
                                     80 	.globl _P2_5
                                     81 	.globl _P2_6
                                     82 	.globl _P2_7
                                     83 	.globl _AIN0
                                     84 	.globl _AIN1
                                     85 	.globl _AIN2
                                     86 	.globl _AIN3
                                     87 	.globl _AIN4
                                     88 	.globl _AIN5
                                     89 	.globl _AIN6
                                     90 	.globl _AIN7
                                     91 	.globl _CAP1
                                     92 	.globl _T2
                                     93 	.globl _CAP2
                                     94 	.globl _T2EX
                                     95 	.globl _INT0_
                                     96 	.globl _SCS
                                     97 	.globl _MOSI
                                     98 	.globl _MISO
                                     99 	.globl _SCK
                                    100 	.globl _RXD1_
                                    101 	.globl _TXD1_
                                    102 	.globl _P1_0
                                    103 	.globl _P1_1
                                    104 	.globl _P1_2
                                    105 	.globl _P1_3
                                    106 	.globl _P1_4
                                    107 	.globl _P1_5
                                    108 	.globl _P1_6
                                    109 	.globl _P1_7
                                    110 	.globl _AIN8
                                    111 	.globl _AIN9
                                    112 	.globl _AIN10
                                    113 	.globl _AIN11
                                    114 	.globl _AIN12
                                    115 	.globl _AIN13
                                    116 	.globl _RXD_
                                    117 	.globl _TXD_
                                    118 	.globl _SCL0
                                    119 	.globl _SDA0
                                    120 	.globl _P0_0
                                    121 	.globl _P0_1
                                    122 	.globl _P0_2
                                    123 	.globl _P0_3
                                    124 	.globl _P0_4
                                    125 	.globl _P0_5
                                    126 	.globl _P0_6
                                    127 	.globl _P0_7
                                    128 	.globl _IE_SPI0
                                    129 	.globl _IE_USB
                                    130 	.globl _IE_ADC
                                    131 	.globl _IE_UART1
                                    132 	.globl _IE_PWM_I2C
                                    133 	.globl _IE_GPIO
                                    134 	.globl _IE_WDOG
                                    135 	.globl _PX0
                                    136 	.globl _PT0
                                    137 	.globl _PX1
                                    138 	.globl _PT1
                                    139 	.globl _PS
                                    140 	.globl _PT2
                                    141 	.globl _PL_FLAG
                                    142 	.globl _PH_FLAG
                                    143 	.globl _EX0
                                    144 	.globl _ET0
                                    145 	.globl _EX1
                                    146 	.globl _ET1
                                    147 	.globl _ES
                                    148 	.globl _ET2
                                    149 	.globl _E_DIS
                                    150 	.globl _EA
                                    151 	.globl _P
                                    152 	.globl _F1
                                    153 	.globl _OV
                                    154 	.globl _RS0
                                    155 	.globl _RS1
                                    156 	.globl _F0
                                    157 	.globl _AC
                                    158 	.globl _CY
                                    159 	.globl _I2CS_INT_ST
                                    160 	.globl _I2CX_INT
                                    161 	.globl _LED_STATUS
                                    162 	.globl _LED_DMA_H
                                    163 	.globl _LED_DMA_L
                                    164 	.globl _LED_DMA
                                    165 	.globl _LED_PWM_OE
                                    166 	.globl _LED_COMMON
                                    167 	.globl _ADC_CHAN
                                    168 	.globl _ADC_DAT_H
                                    169 	.globl _ADC_DAT_L
                                    170 	.globl _ADC_DAT
                                    171 	.globl _ADC_CTRL
                                    172 	.globl _SPI1_CK_SE
                                    173 	.globl _SPI1_CTRL
                                    174 	.globl _SPI1_DATA
                                    175 	.globl _SPI1_STAT
                                    176 	.globl _SIF1
                                    177 	.globl _SBAUD1
                                    178 	.globl _SBUF1
                                    179 	.globl _SCON1
                                    180 	.globl _SPI0_SETUP
                                    181 	.globl _SPI0_CK_SE
                                    182 	.globl _SPI0_CTRL
                                    183 	.globl _SPI0_DATA
                                    184 	.globl _SPI0_STAT
                                    185 	.globl _T2CAP1H
                                    186 	.globl _T2CAP1L
                                    187 	.globl _T2CAP1
                                    188 	.globl _TH2
                                    189 	.globl _TL2
                                    190 	.globl _T2COUNT
                                    191 	.globl _RCAP2H
                                    192 	.globl _RCAP2L
                                    193 	.globl _RCAP2
                                    194 	.globl _T2MOD
                                    195 	.globl _T2CON
                                    196 	.globl _SBUF
                                    197 	.globl _SCON
                                    198 	.globl _TH1
                                    199 	.globl _TH0
                                    200 	.globl _TL1
                                    201 	.globl _TL0
                                    202 	.globl _TMOD
                                    203 	.globl _TCON
                                    204 	.globl _XBUS_AUX
                                    205 	.globl _P7
                                    206 	.globl _P6_DIR
                                    207 	.globl _P6_OUT_PU
                                    208 	.globl _P6_IN
                                    209 	.globl _P5_DIR
                                    210 	.globl _P5_OUT_PU
                                    211 	.globl _P5_IN
                                    212 	.globl _P4_LED_KEY
                                    213 	.globl _P4_DIR_PU
                                    214 	.globl _P4_MOD_OC
                                    215 	.globl _P4
                                    216 	.globl _P3_DIR_PU
                                    217 	.globl _P3_MOD_OC
                                    218 	.globl _P3
                                    219 	.globl _P2_DIR_PU
                                    220 	.globl _P2_MOD_OC
                                    221 	.globl _P2
                                    222 	.globl _P1_DIR_PU
                                    223 	.globl _P1_MOD_OC
                                    224 	.globl _P1
                                    225 	.globl _P0_DIR_PU
                                    226 	.globl _P0_MOD_OC
                                    227 	.globl _P0
                                    228 	.globl _ROM_CTRL
                                    229 	.globl _ROM_DATA_HH
                                    230 	.globl _ROM_DATA_HL
                                    231 	.globl _ROM_DATA_HI
                                    232 	.globl _ROM_ADDR_H
                                    233 	.globl _ROM_ADDR_L
                                    234 	.globl _ROM_ADDR
                                    235 	.globl _GPIO_IE
                                    236 	.globl _IP_EX
                                    237 	.globl _IE_EX
                                    238 	.globl _IP
                                    239 	.globl _IE
                                    240 	.globl _WDOG_COUNT
                                    241 	.globl _RESET_KEEP
                                    242 	.globl _WAKE_CTRL
                                    243 	.globl _CLOCK_CFG
                                    244 	.globl _POWER_CFG
                                    245 	.globl _PCON
                                    246 	.globl _GLOBAL_CFG
                                    247 	.globl _SAFE_MOD
                                    248 	.globl _DPH
                                    249 	.globl _DPL
                                    250 	.globl _SP
                                    251 	.globl _A_INV
                                    252 	.globl _B
                                    253 	.globl _ACC
                                    254 	.globl _PSW
                                    255 	.globl _pinModeInputHighQMK
                                    256 	.globl _readPin
                                    257 	.globl _writePinHigh
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
                                    517 ; internal ram data
                                    518 ;--------------------------------------------------------
                                    519 	.area DSEG    (DATA)
                                    520 ;--------------------------------------------------------
                                    521 ; overlayable items in internal ram
                                    522 ;--------------------------------------------------------
                                    523 	.area	OSEG    (OVR,DATA)
                                    524 	.area	OSEG    (OVR,DATA)
                                    525 	.area	OSEG    (OVR,DATA)
                                    526 	.area	OSEG    (OVR,DATA)
                                    527 ;--------------------------------------------------------
                                    528 ; indirectly addressable internal ram data
                                    529 ;--------------------------------------------------------
                                    530 	.area ISEG    (DATA)
                                    531 ;--------------------------------------------------------
                                    532 ; absolute internal ram data
                                    533 ;--------------------------------------------------------
                                    534 	.area IABS    (ABS,DATA)
                                    535 	.area IABS    (ABS,DATA)
                                    536 ;--------------------------------------------------------
                                    537 ; bit data
                                    538 ;--------------------------------------------------------
                                    539 	.area BSEG    (BIT)
                                    540 ;--------------------------------------------------------
                                    541 ; paged external ram data
                                    542 ;--------------------------------------------------------
                                    543 	.area PSEG    (PAG,XDATA)
                                    544 ;--------------------------------------------------------
                                    545 ; uninitialized external ram data
                                    546 ;--------------------------------------------------------
                                    547 	.area XSEG    (XDATA)
      000657                        548 _pinModeInputHighQMK_pin_10000_10:
      000657                        549 	.ds 1
      000658                        550 _readPin_pin_10000_34:
      000658                        551 	.ds 1
      000659                        552 _writePinHigh_pin_10000_38:
      000659                        553 	.ds 1
                                    554 ;--------------------------------------------------------
                                    555 ; absolute external ram data
                                    556 ;--------------------------------------------------------
                                    557 	.area XABS    (ABS,XDATA)
                                    558 ;--------------------------------------------------------
                                    559 ; initialized external ram data
                                    560 ;--------------------------------------------------------
                                    561 	.area XISEG   (XDATA)
                                    562 	.area HOME    (CODE)
                                    563 	.area GSINIT0 (CODE)
                                    564 	.area GSINIT1 (CODE)
                                    565 	.area GSINIT2 (CODE)
                                    566 	.area GSINIT3 (CODE)
                                    567 	.area GSINIT4 (CODE)
                                    568 	.area GSINIT5 (CODE)
                                    569 	.area GSINIT  (CODE)
                                    570 	.area GSFINAL (CODE)
                                    571 	.area CSEG    (CODE)
                                    572 ;--------------------------------------------------------
                                    573 ; global & static initialisations
                                    574 ;--------------------------------------------------------
                                    575 	.area HOME    (CODE)
                                    576 	.area GSINIT  (CODE)
                                    577 	.area GSFINAL (CODE)
                                    578 	.area GSINIT  (CODE)
                                    579 ;--------------------------------------------------------
                                    580 ; Home
                                    581 ;--------------------------------------------------------
                                    582 	.area HOME    (CODE)
                                    583 	.area HOME    (CODE)
                                    584 ;--------------------------------------------------------
                                    585 ; code
                                    586 ;--------------------------------------------------------
                                    587 	.area CSEG    (CODE)
                                    588 ;------------------------------------------------------------
                                    589 ;Allocation info for local variables in function 'pinModeInputHighQMK'
                                    590 ;------------------------------------------------------------
                                    591 ;port          Allocated to registers r6 
                                    592 ;pinmask       Allocated to registers r5 
                                    593 ;pin           Allocated with name '_pinModeInputHighQMK_pin_10000_10'
                                    594 ;------------------------------------------------------------
                                    595 ;	lib/ch555/gpio.c:10: void pinModeInputHighQMK(uint8_t pin) {
                                    596 ;	-----------------------------------------
                                    597 ;	 function pinModeInputHighQMK
                                    598 ;	-----------------------------------------
      005103                        599 _pinModeInputHighQMK:
                           000007   600 	ar7 = 0x07
                           000006   601 	ar6 = 0x06
                           000005   602 	ar5 = 0x05
                           000004   603 	ar4 = 0x04
                           000003   604 	ar3 = 0x03
                           000002   605 	ar2 = 0x02
                           000001   606 	ar1 = 0x01
                           000000   607 	ar0 = 0x00
      005103 E5 82            [12]  608 	mov	a,dpl
      005105 90 06 57         [24]  609 	mov	dptr,#_pinModeInputHighQMK_pin_10000_10
      005108 F0               [24]  610 	movx	@dptr,a
                                    611 ;	lib/ch555/gpio.c:11: __data uint8_t port = PORTx(pin);
      005109 E0               [24]  612 	movx	a,@dptr
      00510A FF               [12]  613 	mov	r7,a
      00510B C4               [12]  614 	swap	a
      00510C 23               [12]  615 	rl	a
      00510D 54 1F            [12]  616 	anl	a,#0x1f
      00510F FE               [12]  617 	mov	r6,a
                                    618 ;	lib/ch555/gpio.c:12: __data uint8_t pinmask  = PIN_MASK(pin);
      005110 74 07            [12]  619 	mov	a,#0x07
      005112 5F               [12]  620 	anl	a,r7
      005113 90 B6 2C         [24]  621 	mov	dptr,#_pin_to_pinmask
      005116 93               [24]  622 	movc	a,@a+dptr
      005117 FD               [12]  623 	mov	r5,a
                                    624 ;	lib/ch555/gpio.c:15: switch (port) {
      005118 EE               [12]  625 	mov	a,r6
      005119 24 F8            [12]  626 	add	a,#0xff - 0x07
      00511B 40 31            [24]  627 	jc	00108$
                                    628 ;	free result
      00511D EE               [12]  629 	mov	a,r6
      00511E 24 0A            [12]  630 	add	a,#(00118$-3-.)
      005120 83               [24]  631 	movc	a,@a+pc
      005121 F5 82            [12]  632 	mov	dpl,a
      005123 EE               [12]  633 	mov	a,r6
      005124 24 0C            [12]  634 	add	a,#(00119$-3-.)
      005126 83               [24]  635 	movc	a,@a+pc
      005127 F5 83            [12]  636 	mov	dph,a
      005129 E4               [12]  637 	clr	a
      00512A 73               [24]  638 	jmp	@a+dptr
      00512B                        639 00118$:
      00512B 49                     640 	.db	00106$
      00512C 49                     641 	.db	00106$
      00512D 49                     642 	.db	00106$
      00512E 49                     643 	.db	00106$
      00512F 49                     644 	.db	00106$
      005130 4E                     645 	.db	00108$
      005131 4E                     646 	.db	00108$
      005132 3B                     647 	.db	00101$
      005133                        648 00119$:
      005133 51                     649 	.db	00106$>>8
      005134 51                     650 	.db	00106$>>8
      005135 51                     651 	.db	00106$>>8
      005136 51                     652 	.db	00106$>>8
      005137 51                     653 	.db	00106$>>8
      005138 51                     654 	.db	00108$>>8
      005139 51                     655 	.db	00108$>>8
      00513A 51                     656 	.db	00101$>>8
                                    657 ;	lib/ch555/gpio.c:17: case PORT7:
      00513B                        658 00101$:
                                    659 ;	lib/ch555/gpio.c:18: P7 &= ~(pinmask<<2); // _DIR
      00513B ED               [12]  660 	mov	a,r5
      00513C 2D               [12]  661 	add	a,r5
      00513D 25 E0            [12]  662 	add	a,acc
      00513F FE               [12]  663 	mov	r6,a
      005140 74 FF            [12]  664 	mov	a,#0xff
      005142 6E               [12]  665 	xrl	a,r6
      005143 52 F1            [12]  666 	anl	_P7,a
                                    667 ;	lib/ch555/gpio.c:19: P7 |=  pinmask; // _OUT_PU
      005145 ED               [12]  668 	mov	a,r5
      005146 42 F1            [12]  669 	orl	_P7,a
                                    670 ;	lib/ch555/gpio.c:20: break;
                                    671 ;	lib/ch555/gpio.c:37: case PORT4:
      005148 22               [24]  672 	ret
      005149                        673 00106$:
                                    674 ;	lib/ch555/gpio.c:39: writePinHigh(pin);
      005149 8F 82            [24]  675 	mov	dpl, r7
                                    676 ;	lib/ch555/gpio.c:42: }
                                    677 ;	lib/ch555/gpio.c:44: }
      00514B 02 51 F1         [24]  678 	ljmp	_writePinHigh
      00514E                        679 00108$:
      00514E 22               [24]  680 	ret
                                    681 ;------------------------------------------------------------
                                    682 ;Allocation info for local variables in function 'pinModeOutputQMK'
                                    683 ;------------------------------------------------------------
                                    684 ;pin           Allocated with name '_pinModeOutputQMK_pin_10000_14'
                                    685 ;port          Allocated to registers r6 
                                    686 ;pinmask       Allocated to registers r7 
                                    687 ;------------------------------------------------------------
                                    688 ;	lib/ch555/gpio.c:45: void pinModeOutputQMK(uint8_t pin) {
                                    689 ;	-----------------------------------------
                                    690 ;	 function readPin
                                    691 ;	-----------------------------------------
      00514F                        692 _readPin:
      00514F C0 07            [24]  693 	push	ar7
      005151 C0 06            [24]  694 	push	ar6
      005153 C0 05            [24]  695 	push	ar5
      005155 C0 04            [24]  696 	push	ar4
      005157 E5 82            [12]  697 	mov	a,dpl
      005159 90 06 58         [24]  698 	mov	dptr,#_readPin_pin_10000_34
      00515C F0               [24]  699 	movx	@dptr,a
                                    700 ;	lib/ch555/gpio.c:227: __data uint8_t port = PORTx(pin);
      00515D E0               [24]  701 	movx	a,@dptr
      00515E FF               [12]  702 	mov	r7,a
      00515F C4               [12]  703 	swap	a
      005160 23               [12]  704 	rl	a
      005161 54 1F            [12]  705 	anl	a,#0x1f
      005163 FE               [12]  706 	mov	r6,a
                                    707 ;	lib/ch555/gpio.c:228: __data uint8_t pinmask  = PIN_MASK(pin);
      005164 74 07            [12]  708 	mov	a,#0x07
      005166 5F               [12]  709 	anl	a,r7
      005167 90 B6 2C         [24]  710 	mov	dptr,#_pin_to_pinmask
      00516A 93               [24]  711 	movc	a,@a+dptr
      00516B FF               [12]  712 	mov	r7,a
                                    713 ;	lib/ch555/gpio.c:229: switch (port) {
      00516C EE               [12]  714 	mov	a,r6
      00516D 24 F8            [12]  715 	add	a,#0xff - 0x07
      00516F 40 74            [24]  716 	jc	00107$
                                    717 ;	free result
      005171 EE               [12]  718 	mov	a,r6
      005172 24 0A            [12]  719 	add	a,#(00119$-3-.)
      005174 83               [24]  720 	movc	a,@a+pc
      005175 F5 82            [12]  721 	mov	dpl,a
      005177 EE               [12]  722 	mov	a,r6
      005178 24 0C            [12]  723 	add	a,#(00120$-3-.)
      00517A 83               [24]  724 	movc	a,@a+pc
      00517B F5 83            [12]  725 	mov	dph,a
      00517D E4               [12]  726 	clr	a
      00517E 73               [24]  727 	jmp	@a+dptr
      00517F                        728 00119$:
      00517F 8F                     729 	.db	00101$
      005180 9A                     730 	.db	00102$
      005181 A5                     731 	.db	00103$
      005182 B0                     732 	.db	00104$
      005183 BB                     733 	.db	00105$
      005184 E5                     734 	.db	00107$
      005185 E5                     735 	.db	00107$
      005186 C6                     736 	.db	00106$
      005187                        737 00120$:
      005187 51                     738 	.db	00101$>>8
      005188 51                     739 	.db	00102$>>8
      005189 51                     740 	.db	00103$>>8
      00518A 51                     741 	.db	00104$>>8
      00518B 51                     742 	.db	00105$>>8
      00518C 51                     743 	.db	00107$>>8
      00518D 51                     744 	.db	00107$>>8
      00518E 51                     745 	.db	00106$>>8
                                    746 ;	lib/ch555/gpio.c:231: case PORT0:
      00518F                        747 00101$:
                                    748 ;	lib/ch555/gpio.c:232: return ((bool)(P0 & pinmask));
      00518F EF               [12]  749 	mov	a,r7
      005190 55 80            [12]  750 	anl	a,_P0
                                    751 ;	assignBit
      005192 24 FF            [12]  752 	add	a,#0xff
      005194 E4               [12]  753 	clr	a
      005195 33               [12]  754 	rlc	a
      005196 F5 82            [12]  755 	mov	dpl,a
                                    756 ;	lib/ch555/gpio.c:236: case PORT1:
      005198 80 4E            [24]  757 	sjmp	00109$
      00519A                        758 00102$:
                                    759 ;	lib/ch555/gpio.c:237: return ((bool)(P1 & pinmask));
      00519A EF               [12]  760 	mov	a,r7
      00519B 55 90            [12]  761 	anl	a,_P1
                                    762 ;	assignBit
      00519D 24 FF            [12]  763 	add	a,#0xff
      00519F E4               [12]  764 	clr	a
      0051A0 33               [12]  765 	rlc	a
      0051A1 F5 82            [12]  766 	mov	dpl,a
                                    767 ;	lib/ch555/gpio.c:241: case PORT2:
      0051A3 80 43            [24]  768 	sjmp	00109$
      0051A5                        769 00103$:
                                    770 ;	lib/ch555/gpio.c:242: return ((bool)(P2 & pinmask));
      0051A5 EF               [12]  771 	mov	a,r7
      0051A6 55 A0            [12]  772 	anl	a,_P2
                                    773 ;	assignBit
      0051A8 24 FF            [12]  774 	add	a,#0xff
      0051AA E4               [12]  775 	clr	a
      0051AB 33               [12]  776 	rlc	a
      0051AC F5 82            [12]  777 	mov	dpl,a
                                    778 ;	lib/ch555/gpio.c:246: case PORT3:
      0051AE 80 38            [24]  779 	sjmp	00109$
      0051B0                        780 00104$:
                                    781 ;	lib/ch555/gpio.c:247: return ((bool)(P3 & pinmask));
      0051B0 EF               [12]  782 	mov	a,r7
      0051B1 55 B0            [12]  783 	anl	a,_P3
                                    784 ;	assignBit
      0051B3 24 FF            [12]  785 	add	a,#0xff
      0051B5 E4               [12]  786 	clr	a
      0051B6 33               [12]  787 	rlc	a
      0051B7 F5 82            [12]  788 	mov	dpl,a
                                    789 ;	lib/ch555/gpio.c:251: case PORT4:
      0051B9 80 2D            [24]  790 	sjmp	00109$
      0051BB                        791 00105$:
                                    792 ;	lib/ch555/gpio.c:252: return ((bool)(P4 & pinmask));
      0051BB EF               [12]  793 	mov	a,r7
      0051BC 55 C0            [12]  794 	anl	a,_P4
                                    795 ;	assignBit
      0051BE 24 FF            [12]  796 	add	a,#0xff
      0051C0 E4               [12]  797 	clr	a
      0051C1 33               [12]  798 	rlc	a
      0051C2 F5 82            [12]  799 	mov	dpl,a
                                    800 ;	lib/ch555/gpio.c:256: case PORT7:
      0051C4 80 22            [24]  801 	sjmp	00109$
      0051C6                        802 00106$:
                                    803 ;	lib/ch555/gpio.c:257: return ((bool)(P7 & (pinmask<<4))); // bP7_{0,1}_IN
      0051C6 E4               [12]  804 	clr	a
      0051C7 CF               [12]  805 	xch	a,r7
      0051C8 C4               [12]  806 	swap	a
      0051C9 CF               [12]  807 	xch	a,r7
      0051CA 6F               [12]  808 	xrl	a,r7
      0051CB CF               [12]  809 	xch	a,r7
      0051CC 54 F0            [12]  810 	anl	a,#0xf0
      0051CE CF               [12]  811 	xch	a,r7
      0051CF 6F               [12]  812 	xrl	a,r7
      0051D0 FE               [12]  813 	mov	r6,a
      0051D1 AC F1            [24]  814 	mov	r4,_P7
      0051D3 7D 00            [12]  815 	mov	r5,#0x00
      0051D5 EC               [12]  816 	mov	a,r4
      0051D6 52 07            [12]  817 	anl	ar7,a
      0051D8 ED               [12]  818 	mov	a,r5
      0051D9 52 06            [12]  819 	anl	ar6,a
                                    820 ;	assignBit
      0051DB EF               [12]  821 	mov	a,r7
      0051DC 4E               [12]  822 	orl	a,r6
      0051DD 24 FF            [12]  823 	add	a,#0xff
      0051DF E4               [12]  824 	clr	a
      0051E0 33               [12]  825 	rlc	a
      0051E1 F5 82            [12]  826 	mov	dpl,a
                                    827 ;	lib/ch555/gpio.c:260: default:
      0051E3 80 03            [24]  828 	sjmp	00109$
      0051E5                        829 00107$:
                                    830 ;	lib/ch555/gpio.c:261: return -1;
      0051E5 75 82 FF         [24]  831 	mov	dpl, #0xff
                                    832 ;	lib/ch555/gpio.c:263: }
      0051E8                        833 00109$:
                                    834 ;	lib/ch555/gpio.c:264: }
      0051E8 D0 04            [24]  835 	pop	ar4
      0051EA D0 05            [24]  836 	pop	ar5
      0051EC D0 06            [24]  837 	pop	ar6
      0051EE D0 07            [24]  838 	pop	ar7
      0051F0 22               [24]  839 	ret
                                    840 ;------------------------------------------------------------
                                    841 ;Allocation info for local variables in function 'writePinHigh'
                                    842 ;------------------------------------------------------------
                                    843 ;pin           Allocated with name '_writePinHigh_pin_10000_38'
                                    844 ;port          Allocated to registers r6 
                                    845 ;pinmask       Allocated to registers r7 
                                    846 ;------------------------------------------------------------
                                    847 ;	lib/ch555/gpio.c:265: void writePinHigh(uint8_t pin) {
                                    848 ;	-----------------------------------------
                                    849 ;	 function writePinHigh
                                    850 ;	-----------------------------------------
      0051F1                        851 _writePinHigh:
      0051F1 E5 82            [12]  852 	mov	a,dpl
      0051F3 90 06 59         [24]  853 	mov	dptr,#_writePinHigh_pin_10000_38
      0051F6 F0               [24]  854 	movx	@dptr,a
                                    855 ;	lib/ch555/gpio.c:266: __data uint8_t port = PORTx(pin);
      0051F7 E0               [24]  856 	movx	a,@dptr
      0051F8 FF               [12]  857 	mov	r7,a
      0051F9 C4               [12]  858 	swap	a
      0051FA 23               [12]  859 	rl	a
      0051FB 54 1F            [12]  860 	anl	a,#0x1f
      0051FD FE               [12]  861 	mov	r6,a
                                    862 ;	lib/ch555/gpio.c:267: __data uint8_t pinmask  = PIN_MASK(pin);
      0051FE 74 07            [12]  863 	mov	a,#0x07
      005200 5F               [12]  864 	anl	a,r7
      005201 90 B6 2C         [24]  865 	mov	dptr,#_pin_to_pinmask
      005204 93               [24]  866 	movc	a,@a+dptr
      005205 FF               [12]  867 	mov	r7,a
                                    868 ;	lib/ch555/gpio.c:268: switch (port) {
      005206 EE               [12]  869 	mov	a,r6
      005207 24 F8            [12]  870 	add	a,#0xff - 0x07
      005209 40 35            [24]  871 	jc	00108$
                                    872 ;	free result
      00520B EE               [12]  873 	mov	a,r6
      00520C 24 0A            [12]  874 	add	a,#(00118$-3-.)
      00520E 83               [24]  875 	movc	a,@a+pc
      00520F F5 82            [12]  876 	mov	dpl,a
      005211 EE               [12]  877 	mov	a,r6
      005212 24 0C            [12]  878 	add	a,#(00119$-3-.)
      005214 83               [24]  879 	movc	a,@a+pc
      005215 F5 83            [12]  880 	mov	dph,a
      005217 E4               [12]  881 	clr	a
      005218 73               [24]  882 	jmp	@a+dptr
      005219                        883 00118$:
      005219 29                     884 	.db	00101$
      00521A 2D                     885 	.db	00102$
      00521B 31                     886 	.db	00103$
      00521C 35                     887 	.db	00104$
      00521D 39                     888 	.db	00105$
      00521E 40                     889 	.db	00108$
      00521F 40                     890 	.db	00108$
      005220 3D                     891 	.db	00106$
      005221                        892 00119$:
      005221 52                     893 	.db	00101$>>8
      005222 52                     894 	.db	00102$>>8
      005223 52                     895 	.db	00103$>>8
      005224 52                     896 	.db	00104$>>8
      005225 52                     897 	.db	00105$>>8
      005226 52                     898 	.db	00108$>>8
      005227 52                     899 	.db	00108$>>8
      005228 52                     900 	.db	00106$>>8
                                    901 ;	lib/ch555/gpio.c:270: case PORT0:
      005229                        902 00101$:
                                    903 ;	lib/ch555/gpio.c:271: P0 |=  pinmask;
      005229 EF               [12]  904 	mov	a,r7
      00522A 42 80            [12]  905 	orl	_P0,a
                                    906 ;	lib/ch555/gpio.c:272: break;
                                    907 ;	lib/ch555/gpio.c:275: case PORT1:
      00522C 22               [24]  908 	ret
      00522D                        909 00102$:
                                    910 ;	lib/ch555/gpio.c:276: P1 |=  pinmask;
      00522D EF               [12]  911 	mov	a,r7
      00522E 42 90            [12]  912 	orl	_P1,a
                                    913 ;	lib/ch555/gpio.c:277: break;
                                    914 ;	lib/ch555/gpio.c:280: case PORT2:
      005230 22               [24]  915 	ret
      005231                        916 00103$:
                                    917 ;	lib/ch555/gpio.c:281: P2 |=  pinmask;
      005231 EF               [12]  918 	mov	a,r7
      005232 42 A0            [12]  919 	orl	_P2,a
                                    920 ;	lib/ch555/gpio.c:282: break;
                                    921 ;	lib/ch555/gpio.c:285: case PORT3:
      005234 22               [24]  922 	ret
      005235                        923 00104$:
                                    924 ;	lib/ch555/gpio.c:286: P3 |=  pinmask;
      005235 EF               [12]  925 	mov	a,r7
      005236 42 B0            [12]  926 	orl	_P3,a
                                    927 ;	lib/ch555/gpio.c:287: break;
                                    928 ;	lib/ch555/gpio.c:290: case PORT4:
      005238 22               [24]  929 	ret
      005239                        930 00105$:
                                    931 ;	lib/ch555/gpio.c:291: P4 |=  pinmask;
      005239 EF               [12]  932 	mov	a,r7
      00523A 42 C0            [12]  933 	orl	_P4,a
                                    934 ;	lib/ch555/gpio.c:292: break;
                                    935 ;	lib/ch555/gpio.c:295: case PORT7:
      00523C 22               [24]  936 	ret
      00523D                        937 00106$:
                                    938 ;	lib/ch555/gpio.c:296: P7 |=  pinmask; // _OUT_PU
      00523D EF               [12]  939 	mov	a,r7
      00523E 42 F1            [12]  940 	orl	_P7,a
                                    941 ;	lib/ch555/gpio.c:299: }
      005240                        942 00108$:
                                    943 ;	lib/ch555/gpio.c:300: }
      005240 22               [24]  944 	ret
                                    945 ;------------------------------------------------------------
                                    946 ;Allocation info for local variables in function 'writePinLow'
                                    947 ;------------------------------------------------------------
                                    948 ;pin           Allocated with name '_writePinLow_pin_10000_42'
                                    949 ;port          Allocated to registers r6 
                                    950 ;pinmask       Allocated to registers r7 
                                    951 ;------------------------------------------------------------
                                    952 ;	lib/ch555/gpio.c:301: void writePinLow(uint8_t pin) {
                                    953 ;	-----------------------------------------
                                    954 	.area CSEG    (CODE)
                                    955 	.area CONST   (CODE)
                                    956 	.area CONST   (CODE)
      00B62C                        957 _pin_to_pinmask:
      00B62C 01                     958 	.db #0x01	; 1
      00B62D 02                     959 	.db #0x02	; 2
      00B62E 04                     960 	.db #0x04	; 4
      00B62F 08                     961 	.db #0x08	; 8
      00B630 10                     962 	.db #0x10	; 16
      00B631 20                     963 	.db #0x20	; 32
      00B632 40                     964 	.db #0x40	; 64
      00B633 80                     965 	.db #0x80	; 128
                                    966 	.area CSEG    (CODE)
                                    967 	.area XINIT   (CODE)
                                    968 	.area CABS    (ABS,CODE)
