                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module sync_timer
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
                                    254 ;--------------------------------------------------------
                                    255 ; special function registers
                                    256 ;--------------------------------------------------------
                                    257 	.area RSEG    (ABS,DATA)
      000000                        258 	.org 0x0000
                           0000D0   259 _PSW	=	0x00d0
                           0000E0   260 _ACC	=	0x00e0
                           0000F0   261 _B	=	0x00f0
                           0000FD   262 _A_INV	=	0x00fd
                           000081   263 _SP	=	0x0081
                           000082   264 _DPL	=	0x0082
                           000083   265 _DPH	=	0x0083
                           0000A1   266 _SAFE_MOD	=	0x00a1
                           0000B1   267 _GLOBAL_CFG	=	0x00b1
                           000087   268 _PCON	=	0x0087
                           0000BA   269 _POWER_CFG	=	0x00ba
                           0000B9   270 _CLOCK_CFG	=	0x00b9
                           0000A9   271 _WAKE_CTRL	=	0x00a9
                           0000FE   272 _RESET_KEEP	=	0x00fe
                           0000FF   273 _WDOG_COUNT	=	0x00ff
                           0000A8   274 _IE	=	0x00a8
                           0000B8   275 _IP	=	0x00b8
                           0000E8   276 _IE_EX	=	0x00e8
                           0000E9   277 _IP_EX	=	0x00e9
                           0000B2   278 _GPIO_IE	=	0x00b2
                           008584   279 _ROM_ADDR	=	0x8584
                           000084   280 _ROM_ADDR_L	=	0x0084
                           000085   281 _ROM_ADDR_H	=	0x0085
                           008F8E   282 _ROM_DATA_HI	=	0x8f8e
                           00008E   283 _ROM_DATA_HL	=	0x008e
                           00008F   284 _ROM_DATA_HH	=	0x008f
                           000086   285 _ROM_CTRL	=	0x0086
                           000080   286 _P0	=	0x0080
                           0000C4   287 _P0_MOD_OC	=	0x00c4
                           0000C5   288 _P0_DIR_PU	=	0x00c5
                           000090   289 _P1	=	0x0090
                           000092   290 _P1_MOD_OC	=	0x0092
                           000093   291 _P1_DIR_PU	=	0x0093
                           0000A0   292 _P2	=	0x00a0
                           000094   293 _P2_MOD_OC	=	0x0094
                           000095   294 _P2_DIR_PU	=	0x0095
                           0000B0   295 _P3	=	0x00b0
                           000096   296 _P3_MOD_OC	=	0x0096
                           000097   297 _P3_DIR_PU	=	0x0097
                           0000C0   298 _P4	=	0x00c0
                           0000C2   299 _P4_MOD_OC	=	0x00c2
                           0000C3   300 _P4_DIR_PU	=	0x00c3
                           0000C1   301 _P4_LED_KEY	=	0x00c1
                           0000AA   302 _P5_IN	=	0x00aa
                           0000AB   303 _P5_OUT_PU	=	0x00ab
                           0000AC   304 _P5_DIR	=	0x00ac
                           0000AD   305 _P6_IN	=	0x00ad
                           0000AE   306 _P6_OUT_PU	=	0x00ae
                           0000AF   307 _P6_DIR	=	0x00af
                           0000F1   308 _P7	=	0x00f1
                           0000A2   309 _XBUS_AUX	=	0x00a2
                           000088   310 _TCON	=	0x0088
                           000089   311 _TMOD	=	0x0089
                           00008A   312 _TL0	=	0x008a
                           00008B   313 _TL1	=	0x008b
                           00008C   314 _TH0	=	0x008c
                           00008D   315 _TH1	=	0x008d
                           000098   316 _SCON	=	0x0098
                           000099   317 _SBUF	=	0x0099
                           0000C8   318 _T2CON	=	0x00c8
                           0000C9   319 _T2MOD	=	0x00c9
                           00CBCA   320 _RCAP2	=	0xcbca
                           0000CA   321 _RCAP2L	=	0x00ca
                           0000CB   322 _RCAP2H	=	0x00cb
                           00CDCC   323 _T2COUNT	=	0xcdcc
                           0000CC   324 _TL2	=	0x00cc
                           0000CD   325 _TH2	=	0x00cd
                           00CFCE   326 _T2CAP1	=	0xcfce
                           0000CE   327 _T2CAP1L	=	0x00ce
                           0000CF   328 _T2CAP1H	=	0x00cf
                           0000F8   329 _SPI0_STAT	=	0x00f8
                           0000F9   330 _SPI0_DATA	=	0x00f9
                           0000FA   331 _SPI0_CTRL	=	0x00fa
                           0000FB   332 _SPI0_CK_SE	=	0x00fb
                           0000FC   333 _SPI0_SETUP	=	0x00fc
                           0000BC   334 _SCON1	=	0x00bc
                           0000BD   335 _SBUF1	=	0x00bd
                           0000BE   336 _SBAUD1	=	0x00be
                           0000BF   337 _SIF1	=	0x00bf
                           0000B4   338 _SPI1_STAT	=	0x00b4
                           0000B5   339 _SPI1_DATA	=	0x00b5
                           0000B6   340 _SPI1_CTRL	=	0x00b6
                           0000B7   341 _SPI1_CK_SE	=	0x00b7
                           0000F3   342 _ADC_CTRL	=	0x00f3
                           00F5F4   343 _ADC_DAT	=	0xf5f4
                           0000F4   344 _ADC_DAT_L	=	0x00f4
                           0000F5   345 _ADC_DAT_H	=	0x00f5
                           0000F6   346 _ADC_CHAN	=	0x00f6
                           0000A6   347 _LED_COMMON	=	0x00a6
                           0000A7   348 _LED_PWM_OE	=	0x00a7
                           00C7C6   349 _LED_DMA	=	0xc7c6
                           0000C6   350 _LED_DMA_L	=	0x00c6
                           0000C7   351 _LED_DMA_H	=	0x00c7
                           0000F7   352 _LED_STATUS	=	0x00f7
                           0000B3   353 _I2CX_INT	=	0x00b3
                           0000BB   354 _I2CS_INT_ST	=	0x00bb
                                    355 ;--------------------------------------------------------
                                    356 ; special function bits
                                    357 ;--------------------------------------------------------
                                    358 	.area RSEG    (ABS,DATA)
      000000                        359 	.org 0x0000
                           0000D7   360 _CY	=	0x00d7
                           0000D6   361 _AC	=	0x00d6
                           0000D5   362 _F0	=	0x00d5
                           0000D4   363 _RS1	=	0x00d4
                           0000D3   364 _RS0	=	0x00d3
                           0000D2   365 _OV	=	0x00d2
                           0000D1   366 _F1	=	0x00d1
                           0000D0   367 _P	=	0x00d0
                           0000AF   368 _EA	=	0x00af
                           0000AE   369 _E_DIS	=	0x00ae
                           0000AD   370 _ET2	=	0x00ad
                           0000AC   371 _ES	=	0x00ac
                           0000AB   372 _ET1	=	0x00ab
                           0000AA   373 _EX1	=	0x00aa
                           0000A9   374 _ET0	=	0x00a9
                           0000A8   375 _EX0	=	0x00a8
                           0000BF   376 _PH_FLAG	=	0x00bf
                           0000BE   377 _PL_FLAG	=	0x00be
                           0000BD   378 _PT2	=	0x00bd
                           0000BC   379 _PS	=	0x00bc
                           0000BB   380 _PT1	=	0x00bb
                           0000BA   381 _PX1	=	0x00ba
                           0000B9   382 _PT0	=	0x00b9
                           0000B8   383 _PX0	=	0x00b8
                           0000EF   384 _IE_WDOG	=	0x00ef
                           0000EE   385 _IE_GPIO	=	0x00ee
                           0000ED   386 _IE_PWM_I2C	=	0x00ed
                           0000EC   387 _IE_UART1	=	0x00ec
                           0000EB   388 _IE_ADC	=	0x00eb
                           0000E9   389 _IE_USB	=	0x00e9
                           0000E8   390 _IE_SPI0	=	0x00e8
                           000087   391 _P0_7	=	0x0087
                           000086   392 _P0_6	=	0x0086
                           000085   393 _P0_5	=	0x0085
                           000084   394 _P0_4	=	0x0084
                           000083   395 _P0_3	=	0x0083
                           000082   396 _P0_2	=	0x0082
                           000081   397 _P0_1	=	0x0081
                           000080   398 _P0_0	=	0x0080
                           000081   399 _SDA0	=	0x0081
                           000080   400 _SCL0	=	0x0080
                           000083   401 _TXD_	=	0x0083
                           000082   402 _RXD_	=	0x0082
                           000085   403 _AIN13	=	0x0085
                           000084   404 _AIN12	=	0x0084
                           000083   405 _AIN11	=	0x0083
                           000082   406 _AIN10	=	0x0082
                           000081   407 _AIN9	=	0x0081
                           000080   408 _AIN8	=	0x0080
                           000097   409 _P1_7	=	0x0097
                           000096   410 _P1_6	=	0x0096
                           000095   411 _P1_5	=	0x0095
                           000094   412 _P1_4	=	0x0094
                           000093   413 _P1_3	=	0x0093
                           000092   414 _P1_2	=	0x0092
                           000091   415 _P1_1	=	0x0091
                           000090   416 _P1_0	=	0x0090
                           000097   417 _TXD1_	=	0x0097
                           000096   418 _RXD1_	=	0x0096
                           000097   419 _SCK	=	0x0097
                           000096   420 _MISO	=	0x0096
                           000095   421 _MOSI	=	0x0095
                           000094   422 _SCS	=	0x0094
                           000092   423 _INT0_	=	0x0092
                           000091   424 _T2EX	=	0x0091
                           000091   425 _CAP2	=	0x0091
                           000090   426 _T2	=	0x0090
                           000090   427 _CAP1	=	0x0090
                           000097   428 _AIN7	=	0x0097
                           000096   429 _AIN6	=	0x0096
                           000095   430 _AIN5	=	0x0095
                           000094   431 _AIN4	=	0x0094
                           000093   432 _AIN3	=	0x0093
                           000092   433 _AIN2	=	0x0092
                           000091   434 _AIN1	=	0x0091
                           000090   435 _AIN0	=	0x0090
                           0000A7   436 _P2_7	=	0x00a7
                           0000A6   437 _P2_6	=	0x00a6
                           0000A5   438 _P2_5	=	0x00a5
                           0000A4   439 _P2_4	=	0x00a4
                           0000A3   440 _P2_3	=	0x00a3
                           0000A2   441 _P2_2	=	0x00a2
                           0000A1   442 _P2_1	=	0x00a1
                           0000A0   443 _P2_0	=	0x00a0
                           0000A7   444 _TXD1	=	0x00a7
                           0000A6   445 _RXD1	=	0x00a6
                           0000A5   446 _T2EX_	=	0x00a5
                           0000A5   447 _CAP2_	=	0x00a5
                           0000A4   448 _T2_	=	0x00a4
                           0000A4   449 _CAP1_	=	0x00a4
                           0000B7   450 _P3_7	=	0x00b7
                           0000B6   451 _P3_6	=	0x00b6
                           0000B5   452 _P3_5	=	0x00b5
                           0000B4   453 _P3_4	=	0x00b4
                           0000B3   454 _P3_3	=	0x00b3
                           0000B2   455 _P3_2	=	0x00b2
                           0000B1   456 _P3_1	=	0x00b1
                           0000B0   457 _P3_0	=	0x00b0
                           0000B7   458 _SCK1	=	0x00b7
                           0000B6   459 _MISO1	=	0x00b6
                           0000B5   460 _MOSI1	=	0x00b5
                           0000B5   461 _T1	=	0x00b5
                           0000B4   462 _T0	=	0x00b4
                           0000B3   463 _INT1	=	0x00b3
                           0000B2   464 _INT0	=	0x00b2
                           0000B1   465 _TXD	=	0x00b1
                           0000B0   466 _RXD	=	0x00b0
                           0000C6   467 _P4_6	=	0x00c6
                           0000C5   468 _P4_5	=	0x00c5
                           0000C4   469 _P4_4	=	0x00c4
                           0000C3   470 _P4_3	=	0x00c3
                           0000C2   471 _P4_2	=	0x00c2
                           0000C1   472 _P4_1	=	0x00c1
                           0000C0   473 _P4_0	=	0x00c0
                           00008F   474 _TF1	=	0x008f
                           00008E   475 _TR1	=	0x008e
                           00008D   476 _TF0	=	0x008d
                           00008C   477 _TR0	=	0x008c
                           00008B   478 _IE1	=	0x008b
                           00008A   479 _IT1	=	0x008a
                           000089   480 _IE0	=	0x0089
                           000088   481 _IT0	=	0x0088
                           00009F   482 _SM0	=	0x009f
                           00009E   483 _SM1	=	0x009e
                           00009D   484 _SM2	=	0x009d
                           00009C   485 _REN	=	0x009c
                           00009B   486 _TB8	=	0x009b
                           00009A   487 _RB8	=	0x009a
                           000099   488 _TI	=	0x0099
                           000098   489 _RI	=	0x0098
                           0000CF   490 _TF2	=	0x00cf
                           0000CF   491 _CAP1F	=	0x00cf
                           0000CE   492 _EXF2	=	0x00ce
                           0000CD   493 _RCLK	=	0x00cd
                           0000CC   494 _TCLK	=	0x00cc
                           0000CB   495 _EXEN2	=	0x00cb
                           0000CA   496 _TR2	=	0x00ca
                           0000C9   497 _C_T2	=	0x00c9
                           0000C8   498 _CP_RL2	=	0x00c8
                           0000FF   499 _S0_FST_ACT	=	0x00ff
                           0000FE   500 _S0_IF_OV	=	0x00fe
                           0000FD   501 _S0_IF_FIRST	=	0x00fd
                           0000FC   502 _S0_IF_BYTE	=	0x00fc
                           0000FB   503 _S0_FREE	=	0x00fb
                           0000FA   504 _S0_T_FIFO	=	0x00fa
                           0000F8   505 _S0_R_FIFO	=	0x00f8
                           0000F7   506 _ADC_START	=	0x00f7
                                    507 ;--------------------------------------------------------
                                    508 ; overlayable register banks
                                    509 ;--------------------------------------------------------
                                    510 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        511 	.ds 8
                                    512 ;--------------------------------------------------------
                                    513 ; internal ram data
                                    514 ;--------------------------------------------------------
                                    515 	.area DSEG    (DATA)
                                    516 ;--------------------------------------------------------
                                    517 ; overlayable items in internal ram
                                    518 ;--------------------------------------------------------
                                    519 ;--------------------------------------------------------
                                    520 ; indirectly addressable internal ram data
                                    521 ;--------------------------------------------------------
                                    522 	.area ISEG    (DATA)
                                    523 ;--------------------------------------------------------
                                    524 ; absolute internal ram data
                                    525 ;--------------------------------------------------------
                                    526 	.area IABS    (ABS,DATA)
                                    527 	.area IABS    (ABS,DATA)
                                    528 ;--------------------------------------------------------
                                    529 ; bit data
                                    530 ;--------------------------------------------------------
                                    531 	.area BSEG    (BIT)
                                    532 ;--------------------------------------------------------
                                    533 ; paged external ram data
                                    534 ;--------------------------------------------------------
                                    535 	.area PSEG    (PAG,XDATA)
                                    536 ;--------------------------------------------------------
                                    537 ; uninitialized external ram data
                                    538 ;--------------------------------------------------------
                                    539 	.area XSEG    (XDATA)
                                    540 ;--------------------------------------------------------
                                    541 ; absolute external ram data
                                    542 ;--------------------------------------------------------
                                    543 	.area XABS    (ABS,XDATA)
                                    544 ;--------------------------------------------------------
                                    545 ; initialized external ram data
                                    546 ;--------------------------------------------------------
                                    547 	.area XISEG   (XDATA)
                                    548 	.area HOME    (CODE)
                                    549 	.area GSINIT0 (CODE)
                                    550 	.area GSINIT1 (CODE)
                                    551 	.area GSINIT2 (CODE)
                                    552 	.area GSINIT3 (CODE)
                                    553 	.area GSINIT4 (CODE)
                                    554 	.area GSINIT5 (CODE)
                                    555 	.area GSINIT  (CODE)
                                    556 	.area GSFINAL (CODE)
                                    557 	.area CSEG    (CODE)
                                    558 ;--------------------------------------------------------
                                    559 ; global & static initialisations
                                    560 ;--------------------------------------------------------
                                    561 	.area HOME    (CODE)
                                    562 	.area GSINIT  (CODE)
                                    563 	.area GSFINAL (CODE)
                                    564 	.area GSINIT  (CODE)
                                    565 ;--------------------------------------------------------
                                    566 ; Home
                                    567 ;--------------------------------------------------------
                                    568 	.area HOME    (CODE)
                                    569 	.area HOME    (CODE)
                                    570 ;--------------------------------------------------------
                                    571 ; code
                                    572 ;--------------------------------------------------------
                                    573 	.area CSEG    (CODE)
                                    574 	.area CSEG    (CODE)
                                    575 	.area CONST   (CODE)
                                    576 	.area XINIT   (CODE)
                                    577 	.area CABS    (ABS,CODE)
