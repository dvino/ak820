                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module ak820_timer
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
                                    254 	.globl _timer_count
                                    255 	.globl _timer_init
                                    256 	.globl _ak820_timer_irq
                                    257 	.globl _timer_read32
                                    258 	.globl _timer_read
                                    259 	.globl _timer_elapsed
                                    260 	.globl _timer_elapsed32
                                    261 ;--------------------------------------------------------
                                    262 ; special function registers
                                    263 ;--------------------------------------------------------
                                    264 	.area RSEG    (ABS,DATA)
      000000                        265 	.org 0x0000
                           0000D0   266 _PSW	=	0x00d0
                           0000E0   267 _ACC	=	0x00e0
                           0000F0   268 _B	=	0x00f0
                           0000FD   269 _A_INV	=	0x00fd
                           000081   270 _SP	=	0x0081
                           000082   271 _DPL	=	0x0082
                           000083   272 _DPH	=	0x0083
                           0000A1   273 _SAFE_MOD	=	0x00a1
                           0000B1   274 _GLOBAL_CFG	=	0x00b1
                           000087   275 _PCON	=	0x0087
                           0000BA   276 _POWER_CFG	=	0x00ba
                           0000B9   277 _CLOCK_CFG	=	0x00b9
                           0000A9   278 _WAKE_CTRL	=	0x00a9
                           0000FE   279 _RESET_KEEP	=	0x00fe
                           0000FF   280 _WDOG_COUNT	=	0x00ff
                           0000A8   281 _IE	=	0x00a8
                           0000B8   282 _IP	=	0x00b8
                           0000E8   283 _IE_EX	=	0x00e8
                           0000E9   284 _IP_EX	=	0x00e9
                           0000B2   285 _GPIO_IE	=	0x00b2
                           008584   286 _ROM_ADDR	=	0x8584
                           000084   287 _ROM_ADDR_L	=	0x0084
                           000085   288 _ROM_ADDR_H	=	0x0085
                           008F8E   289 _ROM_DATA_HI	=	0x8f8e
                           00008E   290 _ROM_DATA_HL	=	0x008e
                           00008F   291 _ROM_DATA_HH	=	0x008f
                           000086   292 _ROM_CTRL	=	0x0086
                           000080   293 _P0	=	0x0080
                           0000C4   294 _P0_MOD_OC	=	0x00c4
                           0000C5   295 _P0_DIR_PU	=	0x00c5
                           000090   296 _P1	=	0x0090
                           000092   297 _P1_MOD_OC	=	0x0092
                           000093   298 _P1_DIR_PU	=	0x0093
                           0000A0   299 _P2	=	0x00a0
                           000094   300 _P2_MOD_OC	=	0x0094
                           000095   301 _P2_DIR_PU	=	0x0095
                           0000B0   302 _P3	=	0x00b0
                           000096   303 _P3_MOD_OC	=	0x0096
                           000097   304 _P3_DIR_PU	=	0x0097
                           0000C0   305 _P4	=	0x00c0
                           0000C2   306 _P4_MOD_OC	=	0x00c2
                           0000C3   307 _P4_DIR_PU	=	0x00c3
                           0000C1   308 _P4_LED_KEY	=	0x00c1
                           0000AA   309 _P5_IN	=	0x00aa
                           0000AB   310 _P5_OUT_PU	=	0x00ab
                           0000AC   311 _P5_DIR	=	0x00ac
                           0000AD   312 _P6_IN	=	0x00ad
                           0000AE   313 _P6_OUT_PU	=	0x00ae
                           0000AF   314 _P6_DIR	=	0x00af
                           0000F1   315 _P7	=	0x00f1
                           0000A2   316 _XBUS_AUX	=	0x00a2
                           000088   317 _TCON	=	0x0088
                           000089   318 _TMOD	=	0x0089
                           00008A   319 _TL0	=	0x008a
                           00008B   320 _TL1	=	0x008b
                           00008C   321 _TH0	=	0x008c
                           00008D   322 _TH1	=	0x008d
                           000098   323 _SCON	=	0x0098
                           000099   324 _SBUF	=	0x0099
                           0000C8   325 _T2CON	=	0x00c8
                           0000C9   326 _T2MOD	=	0x00c9
                           00CBCA   327 _RCAP2	=	0xcbca
                           0000CA   328 _RCAP2L	=	0x00ca
                           0000CB   329 _RCAP2H	=	0x00cb
                           00CDCC   330 _T2COUNT	=	0xcdcc
                           0000CC   331 _TL2	=	0x00cc
                           0000CD   332 _TH2	=	0x00cd
                           00CFCE   333 _T2CAP1	=	0xcfce
                           0000CE   334 _T2CAP1L	=	0x00ce
                           0000CF   335 _T2CAP1H	=	0x00cf
                           0000F8   336 _SPI0_STAT	=	0x00f8
                           0000F9   337 _SPI0_DATA	=	0x00f9
                           0000FA   338 _SPI0_CTRL	=	0x00fa
                           0000FB   339 _SPI0_CK_SE	=	0x00fb
                           0000FC   340 _SPI0_SETUP	=	0x00fc
                           0000BC   341 _SCON1	=	0x00bc
                           0000BD   342 _SBUF1	=	0x00bd
                           0000BE   343 _SBAUD1	=	0x00be
                           0000BF   344 _SIF1	=	0x00bf
                           0000B4   345 _SPI1_STAT	=	0x00b4
                           0000B5   346 _SPI1_DATA	=	0x00b5
                           0000B6   347 _SPI1_CTRL	=	0x00b6
                           0000B7   348 _SPI1_CK_SE	=	0x00b7
                           0000F3   349 _ADC_CTRL	=	0x00f3
                           00F5F4   350 _ADC_DAT	=	0xf5f4
                           0000F4   351 _ADC_DAT_L	=	0x00f4
                           0000F5   352 _ADC_DAT_H	=	0x00f5
                           0000F6   353 _ADC_CHAN	=	0x00f6
                           0000A6   354 _LED_COMMON	=	0x00a6
                           0000A7   355 _LED_PWM_OE	=	0x00a7
                           00C7C6   356 _LED_DMA	=	0xc7c6
                           0000C6   357 _LED_DMA_L	=	0x00c6
                           0000C7   358 _LED_DMA_H	=	0x00c7
                           0000F7   359 _LED_STATUS	=	0x00f7
                           0000B3   360 _I2CX_INT	=	0x00b3
                           0000BB   361 _I2CS_INT_ST	=	0x00bb
                                    362 ;--------------------------------------------------------
                                    363 ; special function bits
                                    364 ;--------------------------------------------------------
                                    365 	.area RSEG    (ABS,DATA)
      000000                        366 	.org 0x0000
                           0000D7   367 _CY	=	0x00d7
                           0000D6   368 _AC	=	0x00d6
                           0000D5   369 _F0	=	0x00d5
                           0000D4   370 _RS1	=	0x00d4
                           0000D3   371 _RS0	=	0x00d3
                           0000D2   372 _OV	=	0x00d2
                           0000D1   373 _F1	=	0x00d1
                           0000D0   374 _P	=	0x00d0
                           0000AF   375 _EA	=	0x00af
                           0000AE   376 _E_DIS	=	0x00ae
                           0000AD   377 _ET2	=	0x00ad
                           0000AC   378 _ES	=	0x00ac
                           0000AB   379 _ET1	=	0x00ab
                           0000AA   380 _EX1	=	0x00aa
                           0000A9   381 _ET0	=	0x00a9
                           0000A8   382 _EX0	=	0x00a8
                           0000BF   383 _PH_FLAG	=	0x00bf
                           0000BE   384 _PL_FLAG	=	0x00be
                           0000BD   385 _PT2	=	0x00bd
                           0000BC   386 _PS	=	0x00bc
                           0000BB   387 _PT1	=	0x00bb
                           0000BA   388 _PX1	=	0x00ba
                           0000B9   389 _PT0	=	0x00b9
                           0000B8   390 _PX0	=	0x00b8
                           0000EF   391 _IE_WDOG	=	0x00ef
                           0000EE   392 _IE_GPIO	=	0x00ee
                           0000ED   393 _IE_PWM_I2C	=	0x00ed
                           0000EC   394 _IE_UART1	=	0x00ec
                           0000EB   395 _IE_ADC	=	0x00eb
                           0000E9   396 _IE_USB	=	0x00e9
                           0000E8   397 _IE_SPI0	=	0x00e8
                           000087   398 _P0_7	=	0x0087
                           000086   399 _P0_6	=	0x0086
                           000085   400 _P0_5	=	0x0085
                           000084   401 _P0_4	=	0x0084
                           000083   402 _P0_3	=	0x0083
                           000082   403 _P0_2	=	0x0082
                           000081   404 _P0_1	=	0x0081
                           000080   405 _P0_0	=	0x0080
                           000081   406 _SDA0	=	0x0081
                           000080   407 _SCL0	=	0x0080
                           000083   408 _TXD_	=	0x0083
                           000082   409 _RXD_	=	0x0082
                           000085   410 _AIN13	=	0x0085
                           000084   411 _AIN12	=	0x0084
                           000083   412 _AIN11	=	0x0083
                           000082   413 _AIN10	=	0x0082
                           000081   414 _AIN9	=	0x0081
                           000080   415 _AIN8	=	0x0080
                           000097   416 _P1_7	=	0x0097
                           000096   417 _P1_6	=	0x0096
                           000095   418 _P1_5	=	0x0095
                           000094   419 _P1_4	=	0x0094
                           000093   420 _P1_3	=	0x0093
                           000092   421 _P1_2	=	0x0092
                           000091   422 _P1_1	=	0x0091
                           000090   423 _P1_0	=	0x0090
                           000097   424 _TXD1_	=	0x0097
                           000096   425 _RXD1_	=	0x0096
                           000097   426 _SCK	=	0x0097
                           000096   427 _MISO	=	0x0096
                           000095   428 _MOSI	=	0x0095
                           000094   429 _SCS	=	0x0094
                           000092   430 _INT0_	=	0x0092
                           000091   431 _T2EX	=	0x0091
                           000091   432 _CAP2	=	0x0091
                           000090   433 _T2	=	0x0090
                           000090   434 _CAP1	=	0x0090
                           000097   435 _AIN7	=	0x0097
                           000096   436 _AIN6	=	0x0096
                           000095   437 _AIN5	=	0x0095
                           000094   438 _AIN4	=	0x0094
                           000093   439 _AIN3	=	0x0093
                           000092   440 _AIN2	=	0x0092
                           000091   441 _AIN1	=	0x0091
                           000090   442 _AIN0	=	0x0090
                           0000A7   443 _P2_7	=	0x00a7
                           0000A6   444 _P2_6	=	0x00a6
                           0000A5   445 _P2_5	=	0x00a5
                           0000A4   446 _P2_4	=	0x00a4
                           0000A3   447 _P2_3	=	0x00a3
                           0000A2   448 _P2_2	=	0x00a2
                           0000A1   449 _P2_1	=	0x00a1
                           0000A0   450 _P2_0	=	0x00a0
                           0000A7   451 _TXD1	=	0x00a7
                           0000A6   452 _RXD1	=	0x00a6
                           0000A5   453 _T2EX_	=	0x00a5
                           0000A5   454 _CAP2_	=	0x00a5
                           0000A4   455 _T2_	=	0x00a4
                           0000A4   456 _CAP1_	=	0x00a4
                           0000B7   457 _P3_7	=	0x00b7
                           0000B6   458 _P3_6	=	0x00b6
                           0000B5   459 _P3_5	=	0x00b5
                           0000B4   460 _P3_4	=	0x00b4
                           0000B3   461 _P3_3	=	0x00b3
                           0000B2   462 _P3_2	=	0x00b2
                           0000B1   463 _P3_1	=	0x00b1
                           0000B0   464 _P3_0	=	0x00b0
                           0000B7   465 _SCK1	=	0x00b7
                           0000B6   466 _MISO1	=	0x00b6
                           0000B5   467 _MOSI1	=	0x00b5
                           0000B5   468 _T1	=	0x00b5
                           0000B4   469 _T0	=	0x00b4
                           0000B3   470 _INT1	=	0x00b3
                           0000B2   471 _INT0	=	0x00b2
                           0000B1   472 _TXD	=	0x00b1
                           0000B0   473 _RXD	=	0x00b0
                           0000C6   474 _P4_6	=	0x00c6
                           0000C5   475 _P4_5	=	0x00c5
                           0000C4   476 _P4_4	=	0x00c4
                           0000C3   477 _P4_3	=	0x00c3
                           0000C2   478 _P4_2	=	0x00c2
                           0000C1   479 _P4_1	=	0x00c1
                           0000C0   480 _P4_0	=	0x00c0
                           00008F   481 _TF1	=	0x008f
                           00008E   482 _TR1	=	0x008e
                           00008D   483 _TF0	=	0x008d
                           00008C   484 _TR0	=	0x008c
                           00008B   485 _IE1	=	0x008b
                           00008A   486 _IT1	=	0x008a
                           000089   487 _IE0	=	0x0089
                           000088   488 _IT0	=	0x0088
                           00009F   489 _SM0	=	0x009f
                           00009E   490 _SM1	=	0x009e
                           00009D   491 _SM2	=	0x009d
                           00009C   492 _REN	=	0x009c
                           00009B   493 _TB8	=	0x009b
                           00009A   494 _RB8	=	0x009a
                           000099   495 _TI	=	0x0099
                           000098   496 _RI	=	0x0098
                           0000CF   497 _TF2	=	0x00cf
                           0000CF   498 _CAP1F	=	0x00cf
                           0000CE   499 _EXF2	=	0x00ce
                           0000CD   500 _RCLK	=	0x00cd
                           0000CC   501 _TCLK	=	0x00cc
                           0000CB   502 _EXEN2	=	0x00cb
                           0000CA   503 _TR2	=	0x00ca
                           0000C9   504 _C_T2	=	0x00c9
                           0000C8   505 _CP_RL2	=	0x00c8
                           0000FF   506 _S0_FST_ACT	=	0x00ff
                           0000FE   507 _S0_IF_OV	=	0x00fe
                           0000FD   508 _S0_IF_FIRST	=	0x00fd
                           0000FC   509 _S0_IF_BYTE	=	0x00fc
                           0000FB   510 _S0_FREE	=	0x00fb
                           0000FA   511 _S0_T_FIFO	=	0x00fa
                           0000F8   512 _S0_R_FIFO	=	0x00f8
                           0000F7   513 _ADC_START	=	0x00f7
                                    514 ;--------------------------------------------------------
                                    515 ; overlayable register banks
                                    516 ;--------------------------------------------------------
                                    517 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        518 	.ds 8
                                    519 ;--------------------------------------------------------
                                    520 ; internal ram data
                                    521 ;--------------------------------------------------------
                                    522 	.area DSEG    (DATA)
                                    523 ;--------------------------------------------------------
                                    524 ; overlayable items in internal ram
                                    525 ;--------------------------------------------------------
                                    526 ;--------------------------------------------------------
                                    527 ; indirectly addressable internal ram data
                                    528 ;--------------------------------------------------------
                                    529 	.area ISEG    (DATA)
                                    530 ;--------------------------------------------------------
                                    531 ; absolute internal ram data
                                    532 ;--------------------------------------------------------
                                    533 	.area IABS    (ABS,DATA)
                                    534 	.area IABS    (ABS,DATA)
                                    535 ;--------------------------------------------------------
                                    536 ; bit data
                                    537 ;--------------------------------------------------------
                                    538 	.area BSEG    (BIT)
      000005                        539 _timer_read32_sloc0_1_0:
      000005                        540 	.ds 1
                                    541 ;--------------------------------------------------------
                                    542 ; paged external ram data
                                    543 ;--------------------------------------------------------
                                    544 	.area PSEG    (PAG,XDATA)
                                    545 ;--------------------------------------------------------
                                    546 ; uninitialized external ram data
                                    547 ;--------------------------------------------------------
                                    548 	.area XSEG    (XDATA)
      000550                        549 _timer_count::
      000550                        550 	.ds 4
      000554                        551 _timer_elapsed_last_10000_75:
      000554                        552 	.ds 2
      000556                        553 _timer_elapsed32_last_10000_77:
      000556                        554 	.ds 4
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
                                    590 ;Allocation info for local variables in function 'timer_reload'
                                    591 ;------------------------------------------------------------
                                    592 ;reload        Allocated with name '_timer_reload_reload_10000_62'
                                    593 ;------------------------------------------------------------
                                    594 ;	keyboards/ajazz/ak820/ak820_timer.c:8: static void timer_reload(void) {
                                    595 ;	-----------------------------------------
                                    596 ;	 function timer_reload
                                    597 ;	-----------------------------------------
      003FD8                        598 _timer_reload:
                           000007   599 	ar7 = 0x07
                           000006   600 	ar6 = 0x06
                           000005   601 	ar5 = 0x05
                           000004   602 	ar4 = 0x04
                           000003   603 	ar3 = 0x03
                           000002   604 	ar2 = 0x02
                           000001   605 	ar1 = 0x01
                           000000   606 	ar0 = 0x00
                                    607 ;	keyboards/ajazz/ak820/ak820_timer.c:11: TL0 = (uint8_t)reload;
      003FD8 75 8A 96         [24]  608 	mov	_TL0,#0x96
                                    609 ;	keyboards/ajazz/ak820/ak820_timer.c:12: TH0 = (uint8_t)(reload >> 8);
      003FDB 75 8C F5         [24]  610 	mov	_TH0,#0xf5
                                    611 ;	keyboards/ajazz/ak820/ak820_timer.c:13: }
      003FDE 22               [24]  612 	ret
                                    613 ;------------------------------------------------------------
                                    614 ;Allocation info for local variables in function 'timer_init'
                                    615 ;------------------------------------------------------------
                                    616 ;	keyboards/ajazz/ak820/ak820_timer.c:15: void timer_init(void) {
                                    617 ;	-----------------------------------------
                                    618 ;	 function timer_init
                                    619 ;	-----------------------------------------
      003FDF                        620 _timer_init:
                                    621 ;	keyboards/ajazz/ak820/ak820_timer.c:16: EA = 0;
                                    622 ;	assignBit
      003FDF C2 AF            [12]  623 	clr	_EA
                                    624 ;	keyboards/ajazz/ak820/ak820_timer.c:17: timer_count = 0;
      003FE1 90 05 50         [24]  625 	mov	dptr,#_timer_count
      003FE4 E4               [12]  626 	clr	a
      003FE5 F0               [24]  627 	movx	@dptr,a
      003FE6 A3               [24]  628 	inc	dptr
      003FE7 F0               [24]  629 	movx	@dptr,a
      003FE8 A3               [24]  630 	inc	dptr
      003FE9 F0               [24]  631 	movx	@dptr,a
      003FEA A3               [24]  632 	inc	dptr
      003FEB F0               [24]  633 	movx	@dptr,a
                                    634 ;	keyboards/ajazz/ak820/ak820_timer.c:18: T2MOD &= (uint8_t)~bT0_CLK;
      003FEC 53 C9 EF         [24]  635 	anl	_T2MOD,#0xef
                                    636 ;	keyboards/ajazz/ak820/ak820_timer.c:19: TMOD = (TMOD & 0xF0) | 0x01;
      003FEF E5 89            [12]  637 	mov	a,_TMOD
      003FF1 54 F0            [12]  638 	anl	a,#0xf0
      003FF3 44 01            [12]  639 	orl	a,#0x01
      003FF5 F5 89            [12]  640 	mov	_TMOD,a
                                    641 ;	keyboards/ajazz/ak820/ak820_timer.c:20: timer_reload();
      003FF7 12 3F D8         [24]  642 	lcall	_timer_reload
                                    643 ;	keyboards/ajazz/ak820/ak820_timer.c:21: TF0 = 0;
                                    644 ;	assignBit
      003FFA C2 8D            [12]  645 	clr	_TF0
                                    646 ;	keyboards/ajazz/ak820/ak820_timer.c:22: ET0 = 1;
                                    647 ;	assignBit
      003FFC D2 A9            [12]  648 	setb	_ET0
                                    649 ;	keyboards/ajazz/ak820/ak820_timer.c:23: TR0 = 1;
                                    650 ;	assignBit
      003FFE D2 8C            [12]  651 	setb	_TR0
                                    652 ;	keyboards/ajazz/ak820/ak820_timer.c:24: EA = 1;
                                    653 ;	assignBit
      004000 D2 AF            [12]  654 	setb	_EA
                                    655 ;	keyboards/ajazz/ak820/ak820_timer.c:25: }
      004002 22               [24]  656 	ret
                                    657 ;------------------------------------------------------------
                                    658 ;Allocation info for local variables in function 'ak820_timer_irq'
                                    659 ;------------------------------------------------------------
                                    660 ;	keyboards/ajazz/ak820/ak820_timer.c:29: void ak820_timer_irq(void) {
                                    661 ;	-----------------------------------------
                                    662 ;	 function ak820_timer_irq
                                    663 ;	-----------------------------------------
      004003                        664 _ak820_timer_irq:
                                    665 ;	keyboards/ajazz/ak820/ak820_timer.c:30: timer_reload();
      004003 12 3F D8         [24]  666 	lcall	_timer_reload
                                    667 ;	keyboards/ajazz/ak820/ak820_timer.c:31: ++timer_count;
      004006 90 05 50         [24]  668 	mov	dptr,#_timer_count
      004009 E0               [24]  669 	movx	a,@dptr
      00400A 24 01            [12]  670 	add	a, #0x01
      00400C F0               [24]  671 	movx	@dptr,a
      00400D A3               [24]  672 	inc	dptr
      00400E E0               [24]  673 	movx	a,@dptr
      00400F 34 00            [12]  674 	addc	a, #0x00
      004011 F0               [24]  675 	movx	@dptr,a
      004012 A3               [24]  676 	inc	dptr
      004013 E0               [24]  677 	movx	a,@dptr
      004014 34 00            [12]  678 	addc	a, #0x00
      004016 F0               [24]  679 	movx	@dptr,a
      004017 A3               [24]  680 	inc	dptr
      004018 E0               [24]  681 	movx	a,@dptr
      004019 34 00            [12]  682 	addc	a, #0x00
      00401B F0               [24]  683 	movx	@dptr,a
                                    684 ;	keyboards/ajazz/ak820/ak820_timer.c:32: }
      00401C 22               [24]  685 	ret
                                    686 ;------------------------------------------------------------
                                    687 ;Allocation info for local variables in function 'timer_clear'
                                    688 ;------------------------------------------------------------
                                    689 ;	keyboards/ajazz/ak820/ak820_timer.c:34: void timer_clear(void) { __critical { timer_count = 0; } }
                                    690 ;	-----------------------------------------
                                    691 ;	 function timer_read32
                                    692 ;	-----------------------------------------
      00401D                        693 _timer_read32:
      00401D C0 07            [24]  694 	push	ar7
      00401F C0 06            [24]  695 	push	ar6
      004021 C0 05            [24]  696 	push	ar5
      004023 C0 04            [24]  697 	push	ar4
                                    698 ;	keyboards/ajazz/ak820/ak820_timer.c:37: __critical { value = timer_count; }
      004025 D2 05            [12]  699 	setb	_timer_read32_sloc0_1_0
      004027 10 AF 02         [24]  700 	jbc	ea,00103$
      00402A C2 05            [12]  701 	clr	_timer_read32_sloc0_1_0
      00402C                        702 00103$:
      00402C 90 05 50         [24]  703 	mov	dptr,#_timer_count
      00402F E0               [24]  704 	movx	a,@dptr
      004030 FC               [12]  705 	mov	r4,a
      004031 A3               [24]  706 	inc	dptr
      004032 E0               [24]  707 	movx	a,@dptr
      004033 FD               [12]  708 	mov	r5,a
      004034 A3               [24]  709 	inc	dptr
      004035 E0               [24]  710 	movx	a,@dptr
      004036 FE               [12]  711 	mov	r6,a
      004037 A3               [24]  712 	inc	dptr
      004038 E0               [24]  713 	movx	a,@dptr
      004039 FF               [12]  714 	mov	r7,a
      00403A A2 05            [12]  715 	mov	c,_timer_read32_sloc0_1_0
      00403C 92 AF            [24]  716 	mov	ea,c
                                    717 ;	keyboards/ajazz/ak820/ak820_timer.c:38: return value;
      00403E 8C 82            [24]  718 	mov	dpl, r4
      004040 8D 83            [24]  719 	mov	dph, r5
      004042 8E F0            [24]  720 	mov	b, r6
      004044 EF               [12]  721 	mov	a, r7
                                    722 ;	keyboards/ajazz/ak820/ak820_timer.c:39: }
      004045 D0 04            [24]  723 	pop	ar4
      004047 D0 05            [24]  724 	pop	ar5
      004049 D0 06            [24]  725 	pop	ar6
      00404B D0 07            [24]  726 	pop	ar7
      00404D 22               [24]  727 	ret
                                    728 ;------------------------------------------------------------
                                    729 ;Allocation info for local variables in function 'timer_read'
                                    730 ;------------------------------------------------------------
                                    731 ;	keyboards/ajazz/ak820/ak820_timer.c:40: uint16_t timer_read(void) { return (uint16_t)timer_read32(); }
                                    732 ;	-----------------------------------------
                                    733 ;	 function timer_read
                                    734 ;	-----------------------------------------
      00404E                        735 _timer_read:
      00404E 02 40 1D         [24]  736 	ljmp	_timer_read32
                                    737 ;------------------------------------------------------------
                                    738 ;Allocation info for local variables in function 'timer_elapsed'
                                    739 ;------------------------------------------------------------
                                    740 ;last          Allocated with name '_timer_elapsed_last_10000_75'
                                    741 ;------------------------------------------------------------
                                    742 ;	keyboards/ajazz/ak820/ak820_timer.c:41: uint16_t timer_elapsed(uint16_t last) { return (uint16_t)(timer_read() - last); }
                                    743 ;	-----------------------------------------
                                    744 ;	 function timer_elapsed
                                    745 ;	-----------------------------------------
      004051                        746 _timer_elapsed:
      004051 AF 83            [24]  747 	mov	r7,dph
      004053 E5 82            [12]  748 	mov	a,dpl
      004055 90 05 54         [24]  749 	mov	dptr,#_timer_elapsed_last_10000_75
      004058 F0               [24]  750 	movx	@dptr,a
      004059 EF               [12]  751 	mov	a,r7
      00405A A3               [24]  752 	inc	dptr
      00405B F0               [24]  753 	movx	@dptr,a
      00405C 12 40 4E         [24]  754 	lcall	_timer_read
      00405F AE 82            [24]  755 	mov	r6, dpl
      004061 AF 83            [24]  756 	mov	r7, dph
      004063 90 05 54         [24]  757 	mov	dptr,#_timer_elapsed_last_10000_75
      004066 E0               [24]  758 	movx	a,@dptr
      004067 FC               [12]  759 	mov	r4,a
      004068 A3               [24]  760 	inc	dptr
      004069 E0               [24]  761 	movx	a,@dptr
      00406A FD               [12]  762 	mov	r5,a
      00406B EE               [12]  763 	mov	a,r6
      00406C C3               [12]  764 	clr	c
      00406D 9C               [12]  765 	subb	a,r4
      00406E FE               [12]  766 	mov	r6,a
      00406F EF               [12]  767 	mov	a,r7
      004070 9D               [12]  768 	subb	a,r5
      004071 8E 82            [24]  769 	mov	dpl,r6
      004073 F5 83            [12]  770 	mov	dph,a
      004075 22               [24]  771 	ret
                                    772 ;------------------------------------------------------------
                                    773 ;Allocation info for local variables in function 'timer_elapsed32'
                                    774 ;------------------------------------------------------------
                                    775 ;last          Allocated with name '_timer_elapsed32_last_10000_77'
                                    776 ;------------------------------------------------------------
                                    777 ;	keyboards/ajazz/ak820/ak820_timer.c:42: uint32_t timer_elapsed32(uint32_t last) { return timer_read32() - last; }
                                    778 ;	-----------------------------------------
                                    779 ;	 function timer_elapsed32
                                    780 ;	-----------------------------------------
      004076                        781 _timer_elapsed32:
      004076 AF 82            [24]  782 	mov	r7,dpl
      004078 AE 83            [24]  783 	mov	r6,dph
      00407A AD F0            [24]  784 	mov	r5,b
      00407C FC               [12]  785 	mov	r4,a
      00407D 90 05 56         [24]  786 	mov	dptr,#_timer_elapsed32_last_10000_77
      004080 EF               [12]  787 	mov	a,r7
      004081 F0               [24]  788 	movx	@dptr,a
      004082 EE               [12]  789 	mov	a,r6
      004083 A3               [24]  790 	inc	dptr
      004084 F0               [24]  791 	movx	@dptr,a
      004085 ED               [12]  792 	mov	a,r5
      004086 A3               [24]  793 	inc	dptr
      004087 F0               [24]  794 	movx	@dptr,a
      004088 EC               [12]  795 	mov	a,r4
      004089 A3               [24]  796 	inc	dptr
      00408A F0               [24]  797 	movx	@dptr,a
      00408B 12 40 1D         [24]  798 	lcall	_timer_read32
      00408E AC 82            [24]  799 	mov	r4, dpl
      004090 AD 83            [24]  800 	mov	r5, dph
      004092 AE F0            [24]  801 	mov	r6, b
      004094 FF               [12]  802 	mov	r7, a
      004095 90 05 56         [24]  803 	mov	dptr,#_timer_elapsed32_last_10000_77
      004098 E0               [24]  804 	movx	a,@dptr
      004099 F8               [12]  805 	mov	r0,a
      00409A A3               [24]  806 	inc	dptr
      00409B E0               [24]  807 	movx	a,@dptr
      00409C F9               [12]  808 	mov	r1,a
      00409D A3               [24]  809 	inc	dptr
      00409E E0               [24]  810 	movx	a,@dptr
      00409F FA               [12]  811 	mov	r2,a
      0040A0 A3               [24]  812 	inc	dptr
      0040A1 E0               [24]  813 	movx	a,@dptr
      0040A2 FB               [12]  814 	mov	r3,a
      0040A3 EC               [12]  815 	mov	a,r4
      0040A4 C3               [12]  816 	clr	c
      0040A5 98               [12]  817 	subb	a,r0
      0040A6 FC               [12]  818 	mov	r4,a
      0040A7 ED               [12]  819 	mov	a,r5
      0040A8 99               [12]  820 	subb	a,r1
      0040A9 FD               [12]  821 	mov	r5,a
      0040AA EE               [12]  822 	mov	a,r6
      0040AB 9A               [12]  823 	subb	a,r2
      0040AC FE               [12]  824 	mov	r6,a
      0040AD EF               [12]  825 	mov	a,r7
      0040AE 9B               [12]  826 	subb	a,r3
      0040AF 8C 82            [24]  827 	mov	dpl,r4
      0040B1 8D 83            [24]  828 	mov	dph,r5
      0040B3 8E F0            [24]  829 	mov	b,r6
      0040B5 22               [24]  830 	ret
                                    831 	.area CSEG    (CODE)
                                    832 	.area CONST   (CODE)
                                    833 	.area XINIT   (CODE)
                                    834 	.area CABS    (ABS,CODE)
