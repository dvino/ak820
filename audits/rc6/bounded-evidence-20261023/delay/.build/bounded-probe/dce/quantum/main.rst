                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module main
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _protocol_post_task
                                     12 	.globl _protocol_pre_task
                                     13 	.globl _protocol_post_init
                                     14 	.globl _protocol_pre_init
                                     15 	.globl _protocol_setup
                                     16 	.globl _platform_setup
                                     17 	.globl _housekeeping_task
                                     18 	.globl _keyboard_task
                                     19 	.globl _keyboard_init
                                     20 	.globl _keyboard_setup
                                     21 	.globl _ADC_START
                                     22 	.globl _S0_R_FIFO
                                     23 	.globl _S0_T_FIFO
                                     24 	.globl _S0_FREE
                                     25 	.globl _S0_IF_BYTE
                                     26 	.globl _S0_IF_FIRST
                                     27 	.globl _S0_IF_OV
                                     28 	.globl _S0_FST_ACT
                                     29 	.globl _CP_RL2
                                     30 	.globl _C_T2
                                     31 	.globl _TR2
                                     32 	.globl _EXEN2
                                     33 	.globl _TCLK
                                     34 	.globl _RCLK
                                     35 	.globl _EXF2
                                     36 	.globl _CAP1F
                                     37 	.globl _TF2
                                     38 	.globl _RI
                                     39 	.globl _TI
                                     40 	.globl _RB8
                                     41 	.globl _TB8
                                     42 	.globl _REN
                                     43 	.globl _SM2
                                     44 	.globl _SM1
                                     45 	.globl _SM0
                                     46 	.globl _IT0
                                     47 	.globl _IE0
                                     48 	.globl _IT1
                                     49 	.globl _IE1
                                     50 	.globl _TR0
                                     51 	.globl _TF0
                                     52 	.globl _TR1
                                     53 	.globl _TF1
                                     54 	.globl _P4_0
                                     55 	.globl _P4_1
                                     56 	.globl _P4_2
                                     57 	.globl _P4_3
                                     58 	.globl _P4_4
                                     59 	.globl _P4_5
                                     60 	.globl _P4_6
                                     61 	.globl _RXD
                                     62 	.globl _TXD
                                     63 	.globl _INT0
                                     64 	.globl _INT1
                                     65 	.globl _T0
                                     66 	.globl _T1
                                     67 	.globl _MOSI1
                                     68 	.globl _MISO1
                                     69 	.globl _SCK1
                                     70 	.globl _P3_0
                                     71 	.globl _P3_1
                                     72 	.globl _P3_2
                                     73 	.globl _P3_3
                                     74 	.globl _P3_4
                                     75 	.globl _P3_5
                                     76 	.globl _P3_6
                                     77 	.globl _P3_7
                                     78 	.globl _CAP1_
                                     79 	.globl _T2_
                                     80 	.globl _CAP2_
                                     81 	.globl _T2EX_
                                     82 	.globl _RXD1
                                     83 	.globl _TXD1
                                     84 	.globl _P2_0
                                     85 	.globl _P2_1
                                     86 	.globl _P2_2
                                     87 	.globl _P2_3
                                     88 	.globl _P2_4
                                     89 	.globl _P2_5
                                     90 	.globl _P2_6
                                     91 	.globl _P2_7
                                     92 	.globl _AIN0
                                     93 	.globl _AIN1
                                     94 	.globl _AIN2
                                     95 	.globl _AIN3
                                     96 	.globl _AIN4
                                     97 	.globl _AIN5
                                     98 	.globl _AIN6
                                     99 	.globl _AIN7
                                    100 	.globl _CAP1
                                    101 	.globl _T2
                                    102 	.globl _CAP2
                                    103 	.globl _T2EX
                                    104 	.globl _INT0_
                                    105 	.globl _SCS
                                    106 	.globl _MOSI
                                    107 	.globl _MISO
                                    108 	.globl _SCK
                                    109 	.globl _RXD1_
                                    110 	.globl _TXD1_
                                    111 	.globl _P1_0
                                    112 	.globl _P1_1
                                    113 	.globl _P1_2
                                    114 	.globl _P1_3
                                    115 	.globl _P1_4
                                    116 	.globl _P1_5
                                    117 	.globl _P1_6
                                    118 	.globl _P1_7
                                    119 	.globl _AIN8
                                    120 	.globl _AIN9
                                    121 	.globl _AIN10
                                    122 	.globl _AIN11
                                    123 	.globl _AIN12
                                    124 	.globl _AIN13
                                    125 	.globl _RXD_
                                    126 	.globl _TXD_
                                    127 	.globl _SCL0
                                    128 	.globl _SDA0
                                    129 	.globl _P0_0
                                    130 	.globl _P0_1
                                    131 	.globl _P0_2
                                    132 	.globl _P0_3
                                    133 	.globl _P0_4
                                    134 	.globl _P0_5
                                    135 	.globl _P0_6
                                    136 	.globl _P0_7
                                    137 	.globl _IE_SPI0
                                    138 	.globl _IE_USB
                                    139 	.globl _IE_ADC
                                    140 	.globl _IE_UART1
                                    141 	.globl _IE_PWM_I2C
                                    142 	.globl _IE_GPIO
                                    143 	.globl _IE_WDOG
                                    144 	.globl _PX0
                                    145 	.globl _PT0
                                    146 	.globl _PX1
                                    147 	.globl _PT1
                                    148 	.globl _PS
                                    149 	.globl _PT2
                                    150 	.globl _PL_FLAG
                                    151 	.globl _PH_FLAG
                                    152 	.globl _EX0
                                    153 	.globl _ET0
                                    154 	.globl _EX1
                                    155 	.globl _ET1
                                    156 	.globl _ES
                                    157 	.globl _ET2
                                    158 	.globl _E_DIS
                                    159 	.globl _EA
                                    160 	.globl _P
                                    161 	.globl _F1
                                    162 	.globl _OV
                                    163 	.globl _RS0
                                    164 	.globl _RS1
                                    165 	.globl _F0
                                    166 	.globl _AC
                                    167 	.globl _CY
                                    168 	.globl _I2CS_INT_ST
                                    169 	.globl _I2CX_INT
                                    170 	.globl _LED_STATUS
                                    171 	.globl _LED_DMA_H
                                    172 	.globl _LED_DMA_L
                                    173 	.globl _LED_DMA
                                    174 	.globl _LED_PWM_OE
                                    175 	.globl _LED_COMMON
                                    176 	.globl _ADC_CHAN
                                    177 	.globl _ADC_DAT_H
                                    178 	.globl _ADC_DAT_L
                                    179 	.globl _ADC_DAT
                                    180 	.globl _ADC_CTRL
                                    181 	.globl _SPI1_CK_SE
                                    182 	.globl _SPI1_CTRL
                                    183 	.globl _SPI1_DATA
                                    184 	.globl _SPI1_STAT
                                    185 	.globl _SIF1
                                    186 	.globl _SBAUD1
                                    187 	.globl _SBUF1
                                    188 	.globl _SCON1
                                    189 	.globl _SPI0_SETUP
                                    190 	.globl _SPI0_CK_SE
                                    191 	.globl _SPI0_CTRL
                                    192 	.globl _SPI0_DATA
                                    193 	.globl _SPI0_STAT
                                    194 	.globl _T2CAP1H
                                    195 	.globl _T2CAP1L
                                    196 	.globl _T2CAP1
                                    197 	.globl _TH2
                                    198 	.globl _TL2
                                    199 	.globl _T2COUNT
                                    200 	.globl _RCAP2H
                                    201 	.globl _RCAP2L
                                    202 	.globl _RCAP2
                                    203 	.globl _T2MOD
                                    204 	.globl _T2CON
                                    205 	.globl _SBUF
                                    206 	.globl _SCON
                                    207 	.globl _TH1
                                    208 	.globl _TH0
                                    209 	.globl _TL1
                                    210 	.globl _TL0
                                    211 	.globl _TMOD
                                    212 	.globl _TCON
                                    213 	.globl _XBUS_AUX
                                    214 	.globl _P7
                                    215 	.globl _P6_DIR
                                    216 	.globl _P6_OUT_PU
                                    217 	.globl _P6_IN
                                    218 	.globl _P5_DIR
                                    219 	.globl _P5_OUT_PU
                                    220 	.globl _P5_IN
                                    221 	.globl _P4_LED_KEY
                                    222 	.globl _P4_DIR_PU
                                    223 	.globl _P4_MOD_OC
                                    224 	.globl _P4
                                    225 	.globl _P3_DIR_PU
                                    226 	.globl _P3_MOD_OC
                                    227 	.globl _P3
                                    228 	.globl _P2_DIR_PU
                                    229 	.globl _P2_MOD_OC
                                    230 	.globl _P2
                                    231 	.globl _P1_DIR_PU
                                    232 	.globl _P1_MOD_OC
                                    233 	.globl _P1
                                    234 	.globl _P0_DIR_PU
                                    235 	.globl _P0_MOD_OC
                                    236 	.globl _P0
                                    237 	.globl _ROM_CTRL
                                    238 	.globl _ROM_DATA_HH
                                    239 	.globl _ROM_DATA_HL
                                    240 	.globl _ROM_DATA_HI
                                    241 	.globl _ROM_ADDR_H
                                    242 	.globl _ROM_ADDR_L
                                    243 	.globl _ROM_ADDR
                                    244 	.globl _GPIO_IE
                                    245 	.globl _IP_EX
                                    246 	.globl _IE_EX
                                    247 	.globl _IP
                                    248 	.globl _IE
                                    249 	.globl _WDOG_COUNT
                                    250 	.globl _RESET_KEEP
                                    251 	.globl _WAKE_CTRL
                                    252 	.globl _CLOCK_CFG
                                    253 	.globl _POWER_CFG
                                    254 	.globl _PCON
                                    255 	.globl _GLOBAL_CFG
                                    256 	.globl _SAFE_MOD
                                    257 	.globl _DPH
                                    258 	.globl _DPL
                                    259 	.globl _SP
                                    260 	.globl _A_INV
                                    261 	.globl _B
                                    262 	.globl _ACC
                                    263 	.globl _PSW
                                    264 	.globl _protocol_init
                                    265 	.globl _protocol_task
                                    266 	.globl _main
                                    267 ;--------------------------------------------------------
                                    268 ; special function registers
                                    269 ;--------------------------------------------------------
                                    270 	.area RSEG    (ABS,DATA)
      000000                        271 	.org 0x0000
                           0000D0   272 _PSW	=	0x00d0
                           0000E0   273 _ACC	=	0x00e0
                           0000F0   274 _B	=	0x00f0
                           0000FD   275 _A_INV	=	0x00fd
                           000081   276 _SP	=	0x0081
                           000082   277 _DPL	=	0x0082
                           000083   278 _DPH	=	0x0083
                           0000A1   279 _SAFE_MOD	=	0x00a1
                           0000B1   280 _GLOBAL_CFG	=	0x00b1
                           000087   281 _PCON	=	0x0087
                           0000BA   282 _POWER_CFG	=	0x00ba
                           0000B9   283 _CLOCK_CFG	=	0x00b9
                           0000A9   284 _WAKE_CTRL	=	0x00a9
                           0000FE   285 _RESET_KEEP	=	0x00fe
                           0000FF   286 _WDOG_COUNT	=	0x00ff
                           0000A8   287 _IE	=	0x00a8
                           0000B8   288 _IP	=	0x00b8
                           0000E8   289 _IE_EX	=	0x00e8
                           0000E9   290 _IP_EX	=	0x00e9
                           0000B2   291 _GPIO_IE	=	0x00b2
                           008584   292 _ROM_ADDR	=	0x8584
                           000084   293 _ROM_ADDR_L	=	0x0084
                           000085   294 _ROM_ADDR_H	=	0x0085
                           008F8E   295 _ROM_DATA_HI	=	0x8f8e
                           00008E   296 _ROM_DATA_HL	=	0x008e
                           00008F   297 _ROM_DATA_HH	=	0x008f
                           000086   298 _ROM_CTRL	=	0x0086
                           000080   299 _P0	=	0x0080
                           0000C4   300 _P0_MOD_OC	=	0x00c4
                           0000C5   301 _P0_DIR_PU	=	0x00c5
                           000090   302 _P1	=	0x0090
                           000092   303 _P1_MOD_OC	=	0x0092
                           000093   304 _P1_DIR_PU	=	0x0093
                           0000A0   305 _P2	=	0x00a0
                           000094   306 _P2_MOD_OC	=	0x0094
                           000095   307 _P2_DIR_PU	=	0x0095
                           0000B0   308 _P3	=	0x00b0
                           000096   309 _P3_MOD_OC	=	0x0096
                           000097   310 _P3_DIR_PU	=	0x0097
                           0000C0   311 _P4	=	0x00c0
                           0000C2   312 _P4_MOD_OC	=	0x00c2
                           0000C3   313 _P4_DIR_PU	=	0x00c3
                           0000C1   314 _P4_LED_KEY	=	0x00c1
                           0000AA   315 _P5_IN	=	0x00aa
                           0000AB   316 _P5_OUT_PU	=	0x00ab
                           0000AC   317 _P5_DIR	=	0x00ac
                           0000AD   318 _P6_IN	=	0x00ad
                           0000AE   319 _P6_OUT_PU	=	0x00ae
                           0000AF   320 _P6_DIR	=	0x00af
                           0000F1   321 _P7	=	0x00f1
                           0000A2   322 _XBUS_AUX	=	0x00a2
                           000088   323 _TCON	=	0x0088
                           000089   324 _TMOD	=	0x0089
                           00008A   325 _TL0	=	0x008a
                           00008B   326 _TL1	=	0x008b
                           00008C   327 _TH0	=	0x008c
                           00008D   328 _TH1	=	0x008d
                           000098   329 _SCON	=	0x0098
                           000099   330 _SBUF	=	0x0099
                           0000C8   331 _T2CON	=	0x00c8
                           0000C9   332 _T2MOD	=	0x00c9
                           00CBCA   333 _RCAP2	=	0xcbca
                           0000CA   334 _RCAP2L	=	0x00ca
                           0000CB   335 _RCAP2H	=	0x00cb
                           00CDCC   336 _T2COUNT	=	0xcdcc
                           0000CC   337 _TL2	=	0x00cc
                           0000CD   338 _TH2	=	0x00cd
                           00CFCE   339 _T2CAP1	=	0xcfce
                           0000CE   340 _T2CAP1L	=	0x00ce
                           0000CF   341 _T2CAP1H	=	0x00cf
                           0000F8   342 _SPI0_STAT	=	0x00f8
                           0000F9   343 _SPI0_DATA	=	0x00f9
                           0000FA   344 _SPI0_CTRL	=	0x00fa
                           0000FB   345 _SPI0_CK_SE	=	0x00fb
                           0000FC   346 _SPI0_SETUP	=	0x00fc
                           0000BC   347 _SCON1	=	0x00bc
                           0000BD   348 _SBUF1	=	0x00bd
                           0000BE   349 _SBAUD1	=	0x00be
                           0000BF   350 _SIF1	=	0x00bf
                           0000B4   351 _SPI1_STAT	=	0x00b4
                           0000B5   352 _SPI1_DATA	=	0x00b5
                           0000B6   353 _SPI1_CTRL	=	0x00b6
                           0000B7   354 _SPI1_CK_SE	=	0x00b7
                           0000F3   355 _ADC_CTRL	=	0x00f3
                           00F5F4   356 _ADC_DAT	=	0xf5f4
                           0000F4   357 _ADC_DAT_L	=	0x00f4
                           0000F5   358 _ADC_DAT_H	=	0x00f5
                           0000F6   359 _ADC_CHAN	=	0x00f6
                           0000A6   360 _LED_COMMON	=	0x00a6
                           0000A7   361 _LED_PWM_OE	=	0x00a7
                           00C7C6   362 _LED_DMA	=	0xc7c6
                           0000C6   363 _LED_DMA_L	=	0x00c6
                           0000C7   364 _LED_DMA_H	=	0x00c7
                           0000F7   365 _LED_STATUS	=	0x00f7
                           0000B3   366 _I2CX_INT	=	0x00b3
                           0000BB   367 _I2CS_INT_ST	=	0x00bb
                                    368 ;--------------------------------------------------------
                                    369 ; special function bits
                                    370 ;--------------------------------------------------------
                                    371 	.area RSEG    (ABS,DATA)
      000000                        372 	.org 0x0000
                           0000D7   373 _CY	=	0x00d7
                           0000D6   374 _AC	=	0x00d6
                           0000D5   375 _F0	=	0x00d5
                           0000D4   376 _RS1	=	0x00d4
                           0000D3   377 _RS0	=	0x00d3
                           0000D2   378 _OV	=	0x00d2
                           0000D1   379 _F1	=	0x00d1
                           0000D0   380 _P	=	0x00d0
                           0000AF   381 _EA	=	0x00af
                           0000AE   382 _E_DIS	=	0x00ae
                           0000AD   383 _ET2	=	0x00ad
                           0000AC   384 _ES	=	0x00ac
                           0000AB   385 _ET1	=	0x00ab
                           0000AA   386 _EX1	=	0x00aa
                           0000A9   387 _ET0	=	0x00a9
                           0000A8   388 _EX0	=	0x00a8
                           0000BF   389 _PH_FLAG	=	0x00bf
                           0000BE   390 _PL_FLAG	=	0x00be
                           0000BD   391 _PT2	=	0x00bd
                           0000BC   392 _PS	=	0x00bc
                           0000BB   393 _PT1	=	0x00bb
                           0000BA   394 _PX1	=	0x00ba
                           0000B9   395 _PT0	=	0x00b9
                           0000B8   396 _PX0	=	0x00b8
                           0000EF   397 _IE_WDOG	=	0x00ef
                           0000EE   398 _IE_GPIO	=	0x00ee
                           0000ED   399 _IE_PWM_I2C	=	0x00ed
                           0000EC   400 _IE_UART1	=	0x00ec
                           0000EB   401 _IE_ADC	=	0x00eb
                           0000E9   402 _IE_USB	=	0x00e9
                           0000E8   403 _IE_SPI0	=	0x00e8
                           000087   404 _P0_7	=	0x0087
                           000086   405 _P0_6	=	0x0086
                           000085   406 _P0_5	=	0x0085
                           000084   407 _P0_4	=	0x0084
                           000083   408 _P0_3	=	0x0083
                           000082   409 _P0_2	=	0x0082
                           000081   410 _P0_1	=	0x0081
                           000080   411 _P0_0	=	0x0080
                           000081   412 _SDA0	=	0x0081
                           000080   413 _SCL0	=	0x0080
                           000083   414 _TXD_	=	0x0083
                           000082   415 _RXD_	=	0x0082
                           000085   416 _AIN13	=	0x0085
                           000084   417 _AIN12	=	0x0084
                           000083   418 _AIN11	=	0x0083
                           000082   419 _AIN10	=	0x0082
                           000081   420 _AIN9	=	0x0081
                           000080   421 _AIN8	=	0x0080
                           000097   422 _P1_7	=	0x0097
                           000096   423 _P1_6	=	0x0096
                           000095   424 _P1_5	=	0x0095
                           000094   425 _P1_4	=	0x0094
                           000093   426 _P1_3	=	0x0093
                           000092   427 _P1_2	=	0x0092
                           000091   428 _P1_1	=	0x0091
                           000090   429 _P1_0	=	0x0090
                           000097   430 _TXD1_	=	0x0097
                           000096   431 _RXD1_	=	0x0096
                           000097   432 _SCK	=	0x0097
                           000096   433 _MISO	=	0x0096
                           000095   434 _MOSI	=	0x0095
                           000094   435 _SCS	=	0x0094
                           000092   436 _INT0_	=	0x0092
                           000091   437 _T2EX	=	0x0091
                           000091   438 _CAP2	=	0x0091
                           000090   439 _T2	=	0x0090
                           000090   440 _CAP1	=	0x0090
                           000097   441 _AIN7	=	0x0097
                           000096   442 _AIN6	=	0x0096
                           000095   443 _AIN5	=	0x0095
                           000094   444 _AIN4	=	0x0094
                           000093   445 _AIN3	=	0x0093
                           000092   446 _AIN2	=	0x0092
                           000091   447 _AIN1	=	0x0091
                           000090   448 _AIN0	=	0x0090
                           0000A7   449 _P2_7	=	0x00a7
                           0000A6   450 _P2_6	=	0x00a6
                           0000A5   451 _P2_5	=	0x00a5
                           0000A4   452 _P2_4	=	0x00a4
                           0000A3   453 _P2_3	=	0x00a3
                           0000A2   454 _P2_2	=	0x00a2
                           0000A1   455 _P2_1	=	0x00a1
                           0000A0   456 _P2_0	=	0x00a0
                           0000A7   457 _TXD1	=	0x00a7
                           0000A6   458 _RXD1	=	0x00a6
                           0000A5   459 _T2EX_	=	0x00a5
                           0000A5   460 _CAP2_	=	0x00a5
                           0000A4   461 _T2_	=	0x00a4
                           0000A4   462 _CAP1_	=	0x00a4
                           0000B7   463 _P3_7	=	0x00b7
                           0000B6   464 _P3_6	=	0x00b6
                           0000B5   465 _P3_5	=	0x00b5
                           0000B4   466 _P3_4	=	0x00b4
                           0000B3   467 _P3_3	=	0x00b3
                           0000B2   468 _P3_2	=	0x00b2
                           0000B1   469 _P3_1	=	0x00b1
                           0000B0   470 _P3_0	=	0x00b0
                           0000B7   471 _SCK1	=	0x00b7
                           0000B6   472 _MISO1	=	0x00b6
                           0000B5   473 _MOSI1	=	0x00b5
                           0000B5   474 _T1	=	0x00b5
                           0000B4   475 _T0	=	0x00b4
                           0000B3   476 _INT1	=	0x00b3
                           0000B2   477 _INT0	=	0x00b2
                           0000B1   478 _TXD	=	0x00b1
                           0000B0   479 _RXD	=	0x00b0
                           0000C6   480 _P4_6	=	0x00c6
                           0000C5   481 _P4_5	=	0x00c5
                           0000C4   482 _P4_4	=	0x00c4
                           0000C3   483 _P4_3	=	0x00c3
                           0000C2   484 _P4_2	=	0x00c2
                           0000C1   485 _P4_1	=	0x00c1
                           0000C0   486 _P4_0	=	0x00c0
                           00008F   487 _TF1	=	0x008f
                           00008E   488 _TR1	=	0x008e
                           00008D   489 _TF0	=	0x008d
                           00008C   490 _TR0	=	0x008c
                           00008B   491 _IE1	=	0x008b
                           00008A   492 _IT1	=	0x008a
                           000089   493 _IE0	=	0x0089
                           000088   494 _IT0	=	0x0088
                           00009F   495 _SM0	=	0x009f
                           00009E   496 _SM1	=	0x009e
                           00009D   497 _SM2	=	0x009d
                           00009C   498 _REN	=	0x009c
                           00009B   499 _TB8	=	0x009b
                           00009A   500 _RB8	=	0x009a
                           000099   501 _TI	=	0x0099
                           000098   502 _RI	=	0x0098
                           0000CF   503 _TF2	=	0x00cf
                           0000CF   504 _CAP1F	=	0x00cf
                           0000CE   505 _EXF2	=	0x00ce
                           0000CD   506 _RCLK	=	0x00cd
                           0000CC   507 _TCLK	=	0x00cc
                           0000CB   508 _EXEN2	=	0x00cb
                           0000CA   509 _TR2	=	0x00ca
                           0000C9   510 _C_T2	=	0x00c9
                           0000C8   511 _CP_RL2	=	0x00c8
                           0000FF   512 _S0_FST_ACT	=	0x00ff
                           0000FE   513 _S0_IF_OV	=	0x00fe
                           0000FD   514 _S0_IF_FIRST	=	0x00fd
                           0000FC   515 _S0_IF_BYTE	=	0x00fc
                           0000FB   516 _S0_FREE	=	0x00fb
                           0000FA   517 _S0_T_FIFO	=	0x00fa
                           0000F8   518 _S0_R_FIFO	=	0x00f8
                           0000F7   519 _ADC_START	=	0x00f7
                                    520 ;--------------------------------------------------------
                                    521 ; overlayable register banks
                                    522 ;--------------------------------------------------------
                                    523 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        524 	.ds 8
                                    525 ;--------------------------------------------------------
                                    526 ; internal ram data
                                    527 ;--------------------------------------------------------
                                    528 	.area DSEG    (DATA)
                                    529 ;--------------------------------------------------------
                                    530 ; overlayable items in internal ram
                                    531 ;--------------------------------------------------------
                                    532 ;--------------------------------------------------------
                                    533 ; Stack segment in internal ram
                                    534 ;--------------------------------------------------------
                                    535 	.area SSEG
      000063                        536 __start__stack:
      000063                        537 	.ds	1
                                    538 
                                    539 ;--------------------------------------------------------
                                    540 ; indirectly addressable internal ram data
                                    541 ;--------------------------------------------------------
                                    542 	.area ISEG    (DATA)
                                    543 ;--------------------------------------------------------
                                    544 ; absolute internal ram data
                                    545 ;--------------------------------------------------------
                                    546 	.area IABS    (ABS,DATA)
                                    547 	.area IABS    (ABS,DATA)
                                    548 ;--------------------------------------------------------
                                    549 ; bit data
                                    550 ;--------------------------------------------------------
                                    551 	.area BSEG    (BIT)
                                    552 ;--------------------------------------------------------
                                    553 ; paged external ram data
                                    554 ;--------------------------------------------------------
                                    555 	.area PSEG    (PAG,XDATA)
                                    556 ;--------------------------------------------------------
                                    557 ; uninitialized external ram data
                                    558 ;--------------------------------------------------------
                                    559 	.area XSEG    (XDATA)
                                    560 ;--------------------------------------------------------
                                    561 ; absolute external ram data
                                    562 ;--------------------------------------------------------
                                    563 	.area XABS    (ABS,XDATA)
                                    564 ;--------------------------------------------------------
                                    565 ; initialized external ram data
                                    566 ;--------------------------------------------------------
                                    567 	.area XISEG   (XDATA)
                                    568 	.area HOME    (CODE)
                                    569 	.area GSINIT0 (CODE)
                                    570 	.area GSINIT1 (CODE)
                                    571 	.area GSINIT2 (CODE)
                                    572 	.area GSINIT3 (CODE)
                                    573 	.area GSINIT4 (CODE)
                                    574 	.area GSINIT5 (CODE)
                                    575 	.area GSINIT  (CODE)
                                    576 	.area GSFINAL (CODE)
                                    577 	.area CSEG    (CODE)
                                    578 ;--------------------------------------------------------
                                    579 ; interrupt vector
                                    580 ;--------------------------------------------------------
                                    581 	.area HOME    (CODE)
      003027                        582 __interrupt_vect:
      003027 02 30 A5         [24]  583 	ljmp	__sdcc_gsinit_startup
                                    584 ; restartable atomic support routines
      00302A                        585 	.ds	5
      00302F                        586 sdcc_atomic_exchange_rollback_start::
      00302F 00               [12]  587 	nop
      003030 00               [12]  588 	nop
      003031                        589 sdcc_atomic_exchange_pdata_impl:
      003031 E2               [24]  590 	movx	a, @r0
      003032 FB               [12]  591 	mov	r3, a
      003033 EA               [12]  592 	mov	a, r2
      003034 F2               [24]  593 	movx	@r0, a
      003035 80 2C            [24]  594 	sjmp	sdcc_atomic_exchange_exit
      003037 00               [12]  595 	nop
      003038 00               [12]  596 	nop
      003039                        597 sdcc_atomic_exchange_xdata_impl:
      003039 E0               [24]  598 	movx	a, @dptr
      00303A FB               [12]  599 	mov	r3, a
      00303B EA               [12]  600 	mov	a, r2
      00303C F0               [24]  601 	movx	@dptr, a
      00303D 80 24            [24]  602 	sjmp	sdcc_atomic_exchange_exit
      00303F                        603 sdcc_atomic_compare_exchange_idata_impl:
      00303F E6               [12]  604 	mov	a, @r0
      003040 B5 02 02         [24]  605 	cjne	a, ar2, .+#5
      003043 EB               [12]  606 	mov	a, r3
      003044 F6               [12]  607 	mov	@r0, a
      003045 22               [24]  608 	ret
      003046 00               [12]  609 	nop
      003047                        610 sdcc_atomic_compare_exchange_pdata_impl:
      003047 E2               [24]  611 	movx	a, @r0
      003048 B5 02 02         [24]  612 	cjne	a, ar2, .+#5
      00304B EB               [12]  613 	mov	a, r3
      00304C F2               [24]  614 	movx	@r0, a
      00304D 22               [24]  615 	ret
      00304E 00               [12]  616 	nop
      00304F                        617 sdcc_atomic_compare_exchange_xdata_impl:
      00304F E0               [24]  618 	movx	a, @dptr
      003050 B5 02 02         [24]  619 	cjne	a, ar2, .+#5
      003053 EB               [12]  620 	mov	a, r3
      003054 F0               [24]  621 	movx	@dptr, a
      003055 22               [24]  622 	ret
      003056                        623 sdcc_atomic_exchange_rollback_end::
                                    624 
      003056                        625 sdcc_atomic_exchange_gptr_impl::
      003056 30 F6 E0         [24]  626 	jnb	b.6, sdcc_atomic_exchange_xdata_impl
      003059 A8 82            [24]  627 	mov	r0, dpl
      00305B 20 F5 D3         [24]  628 	jb	b.5, sdcc_atomic_exchange_pdata_impl
      00305E                        629 sdcc_atomic_exchange_idata_impl:
      00305E EA               [12]  630 	mov	a, r2
      00305F C6               [12]  631 	xch	a, @r0
      003060 F5 82            [12]  632 	mov	dpl, a
      003062 22               [24]  633 	ret
      003063                        634 sdcc_atomic_exchange_exit:
      003063 8B 82            [24]  635 	mov	dpl, r3
      003065 22               [24]  636 	ret
      003066                        637 sdcc_atomic_compare_exchange_gptr_impl::
      003066 30 F6 E6         [24]  638 	jnb	b.6, sdcc_atomic_compare_exchange_xdata_impl
      003069 A8 82            [24]  639 	mov	r0, dpl
      00306B 20 F5 D9         [24]  640 	jb	b.5, sdcc_atomic_compare_exchange_pdata_impl
      00306E 80 CF            [24]  641 	sjmp	sdcc_atomic_compare_exchange_idata_impl
                                    642 ;--------------------------------------------------------
                                    643 ; global & static initialisations
                                    644 ;--------------------------------------------------------
                                    645 	.area HOME    (CODE)
                                    646 	.area GSINIT  (CODE)
                                    647 	.area GSFINAL (CODE)
                                    648 	.area GSINIT  (CODE)
                                    649 	.globl __sdcc_gsinit_startup
                                    650 	.globl __sdcc_program_startup
                                    651 	.globl __start__stack
                                    652 	.globl __mcs51_genXINIT
                                    653 	.globl __mcs51_genXRAMCLEAR
                                    654 	.globl __mcs51_genRAMCLEAR
                                    655 	.area GSFINAL (CODE)
      003161 02 30 70         [24]  656 	ljmp	__sdcc_program_startup
                                    657 ;--------------------------------------------------------
                                    658 ; Home
                                    659 ;--------------------------------------------------------
                                    660 	.area HOME    (CODE)
                                    661 	.area HOME    (CODE)
      003070                        662 __sdcc_program_startup:
      003070 12 91 9F         [24]  663 	lcall	_main
      003073                        664 __sdcc_program_exit:
      003073 80 FE            [24]  665 	sjmp	.
                                    666 ;	return from main will return to caller
                                    667 ;--------------------------------------------------------
                                    668 ; code
                                    669 ;--------------------------------------------------------
                                    670 	.area CSEG    (CODE)
                                    671 ;------------------------------------------------------------
                                    672 ;Allocation info for local variables in function 'protocol_init'
                                    673 ;------------------------------------------------------------
                                    674 ;	quantum/main.c:32: void protocol_init(void) {
                                    675 ;	-----------------------------------------
                                    676 ;	 function protocol_init
                                    677 ;	-----------------------------------------
      00918D                        678 _protocol_init:
                           000007   679 	ar7 = 0x07
                           000006   680 	ar6 = 0x06
                           000005   681 	ar5 = 0x05
                           000004   682 	ar4 = 0x04
                           000003   683 	ar3 = 0x03
                           000002   684 	ar2 = 0x02
                           000001   685 	ar1 = 0x01
                           000000   686 	ar0 = 0x00
                                    687 ;	quantum/main.c:33: protocol_pre_init();
      00918D 12 42 0F         [24]  688 	lcall	_protocol_pre_init
                                    689 ;	quantum/main.c:35: keyboard_init();
      009190 12 8B 3B         [24]  690 	lcall	_keyboard_init
                                    691 ;	quantum/main.c:37: protocol_post_init();
                                    692 ;	quantum/main.c:38: }
      009193 02 42 1B         [24]  693 	ljmp	_protocol_post_init
                                    694 ;------------------------------------------------------------
                                    695 ;Allocation info for local variables in function 'protocol_task'
                                    696 ;------------------------------------------------------------
                                    697 ;	quantum/main.c:41: void protocol_task(void) {
                                    698 ;	-----------------------------------------
                                    699 ;	 function protocol_task
                                    700 ;	-----------------------------------------
      009196                        701 _protocol_task:
                                    702 ;	quantum/main.c:42: protocol_pre_task();
      009196 12 42 2E         [24]  703 	lcall	_protocol_pre_task
                                    704 ;	quantum/main.c:44: keyboard_task();
      009199 12 8D 6C         [24]  705 	lcall	_keyboard_task
                                    706 ;	quantum/main.c:46: protocol_post_task();
                                    707 ;	quantum/main.c:47: }
      00919C 02 42 FE         [24]  708 	ljmp	_protocol_post_task
                                    709 ;------------------------------------------------------------
                                    710 ;Allocation info for local variables in function 'main'
                                    711 ;------------------------------------------------------------
                                    712 ;	quantum/main.c:54: int main(void) {
                                    713 ;	-----------------------------------------
                                    714 ;	 function main
                                    715 ;	-----------------------------------------
      00919F                        716 _main:
                                    717 ;	quantum/main.c:55: platform_setup();
      00919F 12 53 FF         [24]  718 	lcall	_platform_setup
                                    719 ;	quantum/main.c:56: protocol_setup();
      0091A2 12 42 09         [24]  720 	lcall	_protocol_setup
                                    721 ;	quantum/main.c:57: keyboard_setup();
      0091A5 12 8B 1E         [24]  722 	lcall	_keyboard_setup
                                    723 ;	quantum/main.c:59: protocol_init();
      0091A8 12 91 8D         [24]  724 	lcall	_protocol_init
                                    725 ;	quantum/main.c:64: while (true) {
      0091AB                        726 00102$:
                                    727 ;	quantum/main.c:65: protocol_task();
      0091AB 12 91 96         [24]  728 	lcall	_protocol_task
                                    729 ;	quantum/main.c:79: housekeeping_task();
      0091AE 12 8B 31         [24]  730 	lcall	_housekeeping_task
                                    731 ;	quantum/main.c:81: }
      0091B1 80 F8            [24]  732 	sjmp	00102$
                                    733 	.area CSEG    (CODE)
                                    734 	.area CONST   (CODE)
                                    735 	.area XINIT   (CODE)
                                    736 	.area CABS    (ABS,CODE)
