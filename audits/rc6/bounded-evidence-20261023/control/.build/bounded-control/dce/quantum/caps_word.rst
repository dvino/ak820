                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module caps_word
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _caps_word_press_user
                                     12 	.globl _add_weak_mods
                                     13 	.globl _clear_mods
                                     14 	.globl _unregister_weak_mods
                                     15 	.globl _timer_read
                                     16 	.globl _ADC_START
                                     17 	.globl _S0_R_FIFO
                                     18 	.globl _S0_T_FIFO
                                     19 	.globl _S0_FREE
                                     20 	.globl _S0_IF_BYTE
                                     21 	.globl _S0_IF_FIRST
                                     22 	.globl _S0_IF_OV
                                     23 	.globl _S0_FST_ACT
                                     24 	.globl _CP_RL2
                                     25 	.globl _C_T2
                                     26 	.globl _TR2
                                     27 	.globl _EXEN2
                                     28 	.globl _TCLK
                                     29 	.globl _RCLK
                                     30 	.globl _EXF2
                                     31 	.globl _CAP1F
                                     32 	.globl _TF2
                                     33 	.globl _RI
                                     34 	.globl _TI
                                     35 	.globl _RB8
                                     36 	.globl _TB8
                                     37 	.globl _REN
                                     38 	.globl _SM2
                                     39 	.globl _SM1
                                     40 	.globl _SM0
                                     41 	.globl _IT0
                                     42 	.globl _IE0
                                     43 	.globl _IT1
                                     44 	.globl _IE1
                                     45 	.globl _TR0
                                     46 	.globl _TF0
                                     47 	.globl _TR1
                                     48 	.globl _TF1
                                     49 	.globl _P4_0
                                     50 	.globl _P4_1
                                     51 	.globl _P4_2
                                     52 	.globl _P4_3
                                     53 	.globl _P4_4
                                     54 	.globl _P4_5
                                     55 	.globl _P4_6
                                     56 	.globl _RXD
                                     57 	.globl _TXD
                                     58 	.globl _INT0
                                     59 	.globl _INT1
                                     60 	.globl _T0
                                     61 	.globl _T1
                                     62 	.globl _MOSI1
                                     63 	.globl _MISO1
                                     64 	.globl _SCK1
                                     65 	.globl _P3_0
                                     66 	.globl _P3_1
                                     67 	.globl _P3_2
                                     68 	.globl _P3_3
                                     69 	.globl _P3_4
                                     70 	.globl _P3_5
                                     71 	.globl _P3_6
                                     72 	.globl _P3_7
                                     73 	.globl _CAP1_
                                     74 	.globl _T2_
                                     75 	.globl _CAP2_
                                     76 	.globl _T2EX_
                                     77 	.globl _RXD1
                                     78 	.globl _TXD1
                                     79 	.globl _P2_0
                                     80 	.globl _P2_1
                                     81 	.globl _P2_2
                                     82 	.globl _P2_3
                                     83 	.globl _P2_4
                                     84 	.globl _P2_5
                                     85 	.globl _P2_6
                                     86 	.globl _P2_7
                                     87 	.globl _AIN0
                                     88 	.globl _AIN1
                                     89 	.globl _AIN2
                                     90 	.globl _AIN3
                                     91 	.globl _AIN4
                                     92 	.globl _AIN5
                                     93 	.globl _AIN6
                                     94 	.globl _AIN7
                                     95 	.globl _CAP1
                                     96 	.globl _T2
                                     97 	.globl _CAP2
                                     98 	.globl _T2EX
                                     99 	.globl _INT0_
                                    100 	.globl _SCS
                                    101 	.globl _MOSI
                                    102 	.globl _MISO
                                    103 	.globl _SCK
                                    104 	.globl _RXD1_
                                    105 	.globl _TXD1_
                                    106 	.globl _P1_0
                                    107 	.globl _P1_1
                                    108 	.globl _P1_2
                                    109 	.globl _P1_3
                                    110 	.globl _P1_4
                                    111 	.globl _P1_5
                                    112 	.globl _P1_6
                                    113 	.globl _P1_7
                                    114 	.globl _AIN8
                                    115 	.globl _AIN9
                                    116 	.globl _AIN10
                                    117 	.globl _AIN11
                                    118 	.globl _AIN12
                                    119 	.globl _AIN13
                                    120 	.globl _RXD_
                                    121 	.globl _TXD_
                                    122 	.globl _SCL0
                                    123 	.globl _SDA0
                                    124 	.globl _P0_0
                                    125 	.globl _P0_1
                                    126 	.globl _P0_2
                                    127 	.globl _P0_3
                                    128 	.globl _P0_4
                                    129 	.globl _P0_5
                                    130 	.globl _P0_6
                                    131 	.globl _P0_7
                                    132 	.globl _IE_SPI0
                                    133 	.globl _IE_USB
                                    134 	.globl _IE_ADC
                                    135 	.globl _IE_UART1
                                    136 	.globl _IE_PWM_I2C
                                    137 	.globl _IE_GPIO
                                    138 	.globl _IE_WDOG
                                    139 	.globl _PX0
                                    140 	.globl _PT0
                                    141 	.globl _PX1
                                    142 	.globl _PT1
                                    143 	.globl _PS
                                    144 	.globl _PT2
                                    145 	.globl _PL_FLAG
                                    146 	.globl _PH_FLAG
                                    147 	.globl _EX0
                                    148 	.globl _ET0
                                    149 	.globl _EX1
                                    150 	.globl _ET1
                                    151 	.globl _ES
                                    152 	.globl _ET2
                                    153 	.globl _E_DIS
                                    154 	.globl _EA
                                    155 	.globl _P
                                    156 	.globl _F1
                                    157 	.globl _OV
                                    158 	.globl _RS0
                                    159 	.globl _RS1
                                    160 	.globl _F0
                                    161 	.globl _AC
                                    162 	.globl _CY
                                    163 	.globl _I2CS_INT_ST
                                    164 	.globl _I2CX_INT
                                    165 	.globl _LED_STATUS
                                    166 	.globl _LED_DMA_H
                                    167 	.globl _LED_DMA_L
                                    168 	.globl _LED_DMA
                                    169 	.globl _LED_PWM_OE
                                    170 	.globl _LED_COMMON
                                    171 	.globl _ADC_CHAN
                                    172 	.globl _ADC_DAT_H
                                    173 	.globl _ADC_DAT_L
                                    174 	.globl _ADC_DAT
                                    175 	.globl _ADC_CTRL
                                    176 	.globl _SPI1_CK_SE
                                    177 	.globl _SPI1_CTRL
                                    178 	.globl _SPI1_DATA
                                    179 	.globl _SPI1_STAT
                                    180 	.globl _SIF1
                                    181 	.globl _SBAUD1
                                    182 	.globl _SBUF1
                                    183 	.globl _SCON1
                                    184 	.globl _SPI0_SETUP
                                    185 	.globl _SPI0_CK_SE
                                    186 	.globl _SPI0_CTRL
                                    187 	.globl _SPI0_DATA
                                    188 	.globl _SPI0_STAT
                                    189 	.globl _T2CAP1H
                                    190 	.globl _T2CAP1L
                                    191 	.globl _T2CAP1
                                    192 	.globl _TH2
                                    193 	.globl _TL2
                                    194 	.globl _T2COUNT
                                    195 	.globl _RCAP2H
                                    196 	.globl _RCAP2L
                                    197 	.globl _RCAP2
                                    198 	.globl _T2MOD
                                    199 	.globl _T2CON
                                    200 	.globl _SBUF
                                    201 	.globl _SCON
                                    202 	.globl _TH1
                                    203 	.globl _TH0
                                    204 	.globl _TL1
                                    205 	.globl _TL0
                                    206 	.globl _TMOD
                                    207 	.globl _TCON
                                    208 	.globl _XBUS_AUX
                                    209 	.globl _P7
                                    210 	.globl _P6_DIR
                                    211 	.globl _P6_OUT_PU
                                    212 	.globl _P6_IN
                                    213 	.globl _P5_DIR
                                    214 	.globl _P5_OUT_PU
                                    215 	.globl _P5_IN
                                    216 	.globl _P4_LED_KEY
                                    217 	.globl _P4_DIR_PU
                                    218 	.globl _P4_MOD_OC
                                    219 	.globl _P4
                                    220 	.globl _P3_DIR_PU
                                    221 	.globl _P3_MOD_OC
                                    222 	.globl _P3
                                    223 	.globl _P2_DIR_PU
                                    224 	.globl _P2_MOD_OC
                                    225 	.globl _P2
                                    226 	.globl _P1_DIR_PU
                                    227 	.globl _P1_MOD_OC
                                    228 	.globl _P1
                                    229 	.globl _P0_DIR_PU
                                    230 	.globl _P0_MOD_OC
                                    231 	.globl _P0
                                    232 	.globl _ROM_CTRL
                                    233 	.globl _ROM_DATA_HH
                                    234 	.globl _ROM_DATA_HL
                                    235 	.globl _ROM_DATA_HI
                                    236 	.globl _ROM_ADDR_H
                                    237 	.globl _ROM_ADDR_L
                                    238 	.globl _ROM_ADDR
                                    239 	.globl _GPIO_IE
                                    240 	.globl _IP_EX
                                    241 	.globl _IE_EX
                                    242 	.globl _IP
                                    243 	.globl _IE
                                    244 	.globl _WDOG_COUNT
                                    245 	.globl _RESET_KEEP
                                    246 	.globl _WAKE_CTRL
                                    247 	.globl _CLOCK_CFG
                                    248 	.globl _POWER_CFG
                                    249 	.globl _PCON
                                    250 	.globl _GLOBAL_CFG
                                    251 	.globl _SAFE_MOD
                                    252 	.globl _DPH
                                    253 	.globl _DPL
                                    254 	.globl _SP
                                    255 	.globl _A_INV
                                    256 	.globl _B
                                    257 	.globl _ACC
                                    258 	.globl _PSW
                                    259 	.globl _caps_word_task
                                    260 	.globl _caps_word_reset_idle_timer
                                    261 	.globl _caps_word_on
                                    262 	.globl _caps_word_off
                                    263 	.globl _caps_word_toggle
                                    264 	.globl _is_caps_word_on
                                    265 	.globl _caps_word_set_user
                                    266 ;--------------------------------------------------------
                                    267 ; special function registers
                                    268 ;--------------------------------------------------------
                                    269 	.area RSEG    (ABS,DATA)
      000000                        270 	.org 0x0000
                           0000D0   271 _PSW	=	0x00d0
                           0000E0   272 _ACC	=	0x00e0
                           0000F0   273 _B	=	0x00f0
                           0000FD   274 _A_INV	=	0x00fd
                           000081   275 _SP	=	0x0081
                           000082   276 _DPL	=	0x0082
                           000083   277 _DPH	=	0x0083
                           0000A1   278 _SAFE_MOD	=	0x00a1
                           0000B1   279 _GLOBAL_CFG	=	0x00b1
                           000087   280 _PCON	=	0x0087
                           0000BA   281 _POWER_CFG	=	0x00ba
                           0000B9   282 _CLOCK_CFG	=	0x00b9
                           0000A9   283 _WAKE_CTRL	=	0x00a9
                           0000FE   284 _RESET_KEEP	=	0x00fe
                           0000FF   285 _WDOG_COUNT	=	0x00ff
                           0000A8   286 _IE	=	0x00a8
                           0000B8   287 _IP	=	0x00b8
                           0000E8   288 _IE_EX	=	0x00e8
                           0000E9   289 _IP_EX	=	0x00e9
                           0000B2   290 _GPIO_IE	=	0x00b2
                           008584   291 _ROM_ADDR	=	0x8584
                           000084   292 _ROM_ADDR_L	=	0x0084
                           000085   293 _ROM_ADDR_H	=	0x0085
                           008F8E   294 _ROM_DATA_HI	=	0x8f8e
                           00008E   295 _ROM_DATA_HL	=	0x008e
                           00008F   296 _ROM_DATA_HH	=	0x008f
                           000086   297 _ROM_CTRL	=	0x0086
                           000080   298 _P0	=	0x0080
                           0000C4   299 _P0_MOD_OC	=	0x00c4
                           0000C5   300 _P0_DIR_PU	=	0x00c5
                           000090   301 _P1	=	0x0090
                           000092   302 _P1_MOD_OC	=	0x0092
                           000093   303 _P1_DIR_PU	=	0x0093
                           0000A0   304 _P2	=	0x00a0
                           000094   305 _P2_MOD_OC	=	0x0094
                           000095   306 _P2_DIR_PU	=	0x0095
                           0000B0   307 _P3	=	0x00b0
                           000096   308 _P3_MOD_OC	=	0x0096
                           000097   309 _P3_DIR_PU	=	0x0097
                           0000C0   310 _P4	=	0x00c0
                           0000C2   311 _P4_MOD_OC	=	0x00c2
                           0000C3   312 _P4_DIR_PU	=	0x00c3
                           0000C1   313 _P4_LED_KEY	=	0x00c1
                           0000AA   314 _P5_IN	=	0x00aa
                           0000AB   315 _P5_OUT_PU	=	0x00ab
                           0000AC   316 _P5_DIR	=	0x00ac
                           0000AD   317 _P6_IN	=	0x00ad
                           0000AE   318 _P6_OUT_PU	=	0x00ae
                           0000AF   319 _P6_DIR	=	0x00af
                           0000F1   320 _P7	=	0x00f1
                           0000A2   321 _XBUS_AUX	=	0x00a2
                           000088   322 _TCON	=	0x0088
                           000089   323 _TMOD	=	0x0089
                           00008A   324 _TL0	=	0x008a
                           00008B   325 _TL1	=	0x008b
                           00008C   326 _TH0	=	0x008c
                           00008D   327 _TH1	=	0x008d
                           000098   328 _SCON	=	0x0098
                           000099   329 _SBUF	=	0x0099
                           0000C8   330 _T2CON	=	0x00c8
                           0000C9   331 _T2MOD	=	0x00c9
                           00CBCA   332 _RCAP2	=	0xcbca
                           0000CA   333 _RCAP2L	=	0x00ca
                           0000CB   334 _RCAP2H	=	0x00cb
                           00CDCC   335 _T2COUNT	=	0xcdcc
                           0000CC   336 _TL2	=	0x00cc
                           0000CD   337 _TH2	=	0x00cd
                           00CFCE   338 _T2CAP1	=	0xcfce
                           0000CE   339 _T2CAP1L	=	0x00ce
                           0000CF   340 _T2CAP1H	=	0x00cf
                           0000F8   341 _SPI0_STAT	=	0x00f8
                           0000F9   342 _SPI0_DATA	=	0x00f9
                           0000FA   343 _SPI0_CTRL	=	0x00fa
                           0000FB   344 _SPI0_CK_SE	=	0x00fb
                           0000FC   345 _SPI0_SETUP	=	0x00fc
                           0000BC   346 _SCON1	=	0x00bc
                           0000BD   347 _SBUF1	=	0x00bd
                           0000BE   348 _SBAUD1	=	0x00be
                           0000BF   349 _SIF1	=	0x00bf
                           0000B4   350 _SPI1_STAT	=	0x00b4
                           0000B5   351 _SPI1_DATA	=	0x00b5
                           0000B6   352 _SPI1_CTRL	=	0x00b6
                           0000B7   353 _SPI1_CK_SE	=	0x00b7
                           0000F3   354 _ADC_CTRL	=	0x00f3
                           00F5F4   355 _ADC_DAT	=	0xf5f4
                           0000F4   356 _ADC_DAT_L	=	0x00f4
                           0000F5   357 _ADC_DAT_H	=	0x00f5
                           0000F6   358 _ADC_CHAN	=	0x00f6
                           0000A6   359 _LED_COMMON	=	0x00a6
                           0000A7   360 _LED_PWM_OE	=	0x00a7
                           00C7C6   361 _LED_DMA	=	0xc7c6
                           0000C6   362 _LED_DMA_L	=	0x00c6
                           0000C7   363 _LED_DMA_H	=	0x00c7
                           0000F7   364 _LED_STATUS	=	0x00f7
                           0000B3   365 _I2CX_INT	=	0x00b3
                           0000BB   366 _I2CS_INT_ST	=	0x00bb
                                    367 ;--------------------------------------------------------
                                    368 ; special function bits
                                    369 ;--------------------------------------------------------
                                    370 	.area RSEG    (ABS,DATA)
      000000                        371 	.org 0x0000
                           0000D7   372 _CY	=	0x00d7
                           0000D6   373 _AC	=	0x00d6
                           0000D5   374 _F0	=	0x00d5
                           0000D4   375 _RS1	=	0x00d4
                           0000D3   376 _RS0	=	0x00d3
                           0000D2   377 _OV	=	0x00d2
                           0000D1   378 _F1	=	0x00d1
                           0000D0   379 _P	=	0x00d0
                           0000AF   380 _EA	=	0x00af
                           0000AE   381 _E_DIS	=	0x00ae
                           0000AD   382 _ET2	=	0x00ad
                           0000AC   383 _ES	=	0x00ac
                           0000AB   384 _ET1	=	0x00ab
                           0000AA   385 _EX1	=	0x00aa
                           0000A9   386 _ET0	=	0x00a9
                           0000A8   387 _EX0	=	0x00a8
                           0000BF   388 _PH_FLAG	=	0x00bf
                           0000BE   389 _PL_FLAG	=	0x00be
                           0000BD   390 _PT2	=	0x00bd
                           0000BC   391 _PS	=	0x00bc
                           0000BB   392 _PT1	=	0x00bb
                           0000BA   393 _PX1	=	0x00ba
                           0000B9   394 _PT0	=	0x00b9
                           0000B8   395 _PX0	=	0x00b8
                           0000EF   396 _IE_WDOG	=	0x00ef
                           0000EE   397 _IE_GPIO	=	0x00ee
                           0000ED   398 _IE_PWM_I2C	=	0x00ed
                           0000EC   399 _IE_UART1	=	0x00ec
                           0000EB   400 _IE_ADC	=	0x00eb
                           0000E9   401 _IE_USB	=	0x00e9
                           0000E8   402 _IE_SPI0	=	0x00e8
                           000087   403 _P0_7	=	0x0087
                           000086   404 _P0_6	=	0x0086
                           000085   405 _P0_5	=	0x0085
                           000084   406 _P0_4	=	0x0084
                           000083   407 _P0_3	=	0x0083
                           000082   408 _P0_2	=	0x0082
                           000081   409 _P0_1	=	0x0081
                           000080   410 _P0_0	=	0x0080
                           000081   411 _SDA0	=	0x0081
                           000080   412 _SCL0	=	0x0080
                           000083   413 _TXD_	=	0x0083
                           000082   414 _RXD_	=	0x0082
                           000085   415 _AIN13	=	0x0085
                           000084   416 _AIN12	=	0x0084
                           000083   417 _AIN11	=	0x0083
                           000082   418 _AIN10	=	0x0082
                           000081   419 _AIN9	=	0x0081
                           000080   420 _AIN8	=	0x0080
                           000097   421 _P1_7	=	0x0097
                           000096   422 _P1_6	=	0x0096
                           000095   423 _P1_5	=	0x0095
                           000094   424 _P1_4	=	0x0094
                           000093   425 _P1_3	=	0x0093
                           000092   426 _P1_2	=	0x0092
                           000091   427 _P1_1	=	0x0091
                           000090   428 _P1_0	=	0x0090
                           000097   429 _TXD1_	=	0x0097
                           000096   430 _RXD1_	=	0x0096
                           000097   431 _SCK	=	0x0097
                           000096   432 _MISO	=	0x0096
                           000095   433 _MOSI	=	0x0095
                           000094   434 _SCS	=	0x0094
                           000092   435 _INT0_	=	0x0092
                           000091   436 _T2EX	=	0x0091
                           000091   437 _CAP2	=	0x0091
                           000090   438 _T2	=	0x0090
                           000090   439 _CAP1	=	0x0090
                           000097   440 _AIN7	=	0x0097
                           000096   441 _AIN6	=	0x0096
                           000095   442 _AIN5	=	0x0095
                           000094   443 _AIN4	=	0x0094
                           000093   444 _AIN3	=	0x0093
                           000092   445 _AIN2	=	0x0092
                           000091   446 _AIN1	=	0x0091
                           000090   447 _AIN0	=	0x0090
                           0000A7   448 _P2_7	=	0x00a7
                           0000A6   449 _P2_6	=	0x00a6
                           0000A5   450 _P2_5	=	0x00a5
                           0000A4   451 _P2_4	=	0x00a4
                           0000A3   452 _P2_3	=	0x00a3
                           0000A2   453 _P2_2	=	0x00a2
                           0000A1   454 _P2_1	=	0x00a1
                           0000A0   455 _P2_0	=	0x00a0
                           0000A7   456 _TXD1	=	0x00a7
                           0000A6   457 _RXD1	=	0x00a6
                           0000A5   458 _T2EX_	=	0x00a5
                           0000A5   459 _CAP2_	=	0x00a5
                           0000A4   460 _T2_	=	0x00a4
                           0000A4   461 _CAP1_	=	0x00a4
                           0000B7   462 _P3_7	=	0x00b7
                           0000B6   463 _P3_6	=	0x00b6
                           0000B5   464 _P3_5	=	0x00b5
                           0000B4   465 _P3_4	=	0x00b4
                           0000B3   466 _P3_3	=	0x00b3
                           0000B2   467 _P3_2	=	0x00b2
                           0000B1   468 _P3_1	=	0x00b1
                           0000B0   469 _P3_0	=	0x00b0
                           0000B7   470 _SCK1	=	0x00b7
                           0000B6   471 _MISO1	=	0x00b6
                           0000B5   472 _MOSI1	=	0x00b5
                           0000B5   473 _T1	=	0x00b5
                           0000B4   474 _T0	=	0x00b4
                           0000B3   475 _INT1	=	0x00b3
                           0000B2   476 _INT0	=	0x00b2
                           0000B1   477 _TXD	=	0x00b1
                           0000B0   478 _RXD	=	0x00b0
                           0000C6   479 _P4_6	=	0x00c6
                           0000C5   480 _P4_5	=	0x00c5
                           0000C4   481 _P4_4	=	0x00c4
                           0000C3   482 _P4_3	=	0x00c3
                           0000C2   483 _P4_2	=	0x00c2
                           0000C1   484 _P4_1	=	0x00c1
                           0000C0   485 _P4_0	=	0x00c0
                           00008F   486 _TF1	=	0x008f
                           00008E   487 _TR1	=	0x008e
                           00008D   488 _TF0	=	0x008d
                           00008C   489 _TR0	=	0x008c
                           00008B   490 _IE1	=	0x008b
                           00008A   491 _IT1	=	0x008a
                           000089   492 _IE0	=	0x0089
                           000088   493 _IT0	=	0x0088
                           00009F   494 _SM0	=	0x009f
                           00009E   495 _SM1	=	0x009e
                           00009D   496 _SM2	=	0x009d
                           00009C   497 _REN	=	0x009c
                           00009B   498 _TB8	=	0x009b
                           00009A   499 _RB8	=	0x009a
                           000099   500 _TI	=	0x0099
                           000098   501 _RI	=	0x0098
                           0000CF   502 _TF2	=	0x00cf
                           0000CF   503 _CAP1F	=	0x00cf
                           0000CE   504 _EXF2	=	0x00ce
                           0000CD   505 _RCLK	=	0x00cd
                           0000CC   506 _TCLK	=	0x00cc
                           0000CB   507 _EXEN2	=	0x00cb
                           0000CA   508 _TR2	=	0x00ca
                           0000C9   509 _C_T2	=	0x00c9
                           0000C8   510 _CP_RL2	=	0x00c8
                           0000FF   511 _S0_FST_ACT	=	0x00ff
                           0000FE   512 _S0_IF_OV	=	0x00fe
                           0000FD   513 _S0_IF_FIRST	=	0x00fd
                           0000FC   514 _S0_IF_BYTE	=	0x00fc
                           0000FB   515 _S0_FREE	=	0x00fb
                           0000FA   516 _S0_T_FIFO	=	0x00fa
                           0000F8   517 _S0_R_FIFO	=	0x00f8
                           0000F7   518 _ADC_START	=	0x00f7
                                    519 ;--------------------------------------------------------
                                    520 ; overlayable register banks
                                    521 ;--------------------------------------------------------
                                    522 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        523 	.ds 8
                                    524 ;--------------------------------------------------------
                                    525 ; internal ram data
                                    526 ;--------------------------------------------------------
                                    527 	.area DSEG    (DATA)
                                    528 ;--------------------------------------------------------
                                    529 ; overlayable items in internal ram
                                    530 ;--------------------------------------------------------
                                    531 ;--------------------------------------------------------
                                    532 ; indirectly addressable internal ram data
                                    533 ;--------------------------------------------------------
                                    534 	.area ISEG    (DATA)
                                    535 ;--------------------------------------------------------
                                    536 ; absolute internal ram data
                                    537 ;--------------------------------------------------------
                                    538 	.area IABS    (ABS,DATA)
                                    539 	.area IABS    (ABS,DATA)
                                    540 ;--------------------------------------------------------
                                    541 ; bit data
                                    542 ;--------------------------------------------------------
                                    543 	.area BSEG    (BIT)
      00000E                        544 _caps_word_press_user_sloc0_1_0:
      00000E                        545 	.ds 1
                                    546 ;--------------------------------------------------------
                                    547 ; paged external ram data
                                    548 ;--------------------------------------------------------
                                    549 	.area PSEG    (PAG,XDATA)
                                    550 ;--------------------------------------------------------
                                    551 ; uninitialized external ram data
                                    552 ;--------------------------------------------------------
                                    553 	.area XSEG    (XDATA)
      0008BF                        554 _caps_word_press_user_keycode_10000_242:
      0008BF                        555 	.ds 2
                                    556 ;--------------------------------------------------------
                                    557 ; absolute external ram data
                                    558 ;--------------------------------------------------------
                                    559 	.area XABS    (ABS,XDATA)
                                    560 ;--------------------------------------------------------
                                    561 ; initialized external ram data
                                    562 ;--------------------------------------------------------
                                    563 	.area XISEG   (XDATA)
      000BD1                        564 _caps_word_active:
      000BD1                        565 	.ds 1
      000BD2                        566 _idle_timer:
      000BD2                        567 	.ds 2
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
                                    579 ; global & static initialisations
                                    580 ;--------------------------------------------------------
                                    581 	.area HOME    (CODE)
                                    582 	.area GSINIT  (CODE)
                                    583 	.area GSFINAL (CODE)
                                    584 	.area GSINIT  (CODE)
                                    585 ;--------------------------------------------------------
                                    586 ; Home
                                    587 ;--------------------------------------------------------
                                    588 	.area HOME    (CODE)
                                    589 	.area HOME    (CODE)
                                    590 ;--------------------------------------------------------
                                    591 ; code
                                    592 ;--------------------------------------------------------
                                    593 	.area AK820LOW(CODE)
                                    594 ;------------------------------------------------------------
                                    595 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    596 ;------------------------------------------------------------
                                    597 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_128'
                                    598 ;------------------------------------------------------------
                                    599 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    600 ;	-----------------------------------------
                           000007   601 	ar7 = 0x07
                           000006   602 	ar6 = 0x06
                           000005   603 	ar5 = 0x05
                           000004   604 	ar4 = 0x04
                           000003   605 	ar3 = 0x03
                           000002   606 	ar2 = 0x02
                           000001   607 	ar1 = 0x01
                           000000   608 	ar0 = 0x00
                                    609 ;	 function caps_word_task
                                    610 ;	-----------------------------------------
      002EC2                        611 _caps_word_task:
                                    612 ;	quantum/caps_word.c:42: if (caps_word_active && timer_expired(timer_read(), idle_timer)) {
      002EC2 90 0B D1         [24]  613 	mov	dptr,#_caps_word_active
      002EC5 E0               [24]  614 	movx	a,@dptr
      002EC6 60 22            [24]  615 	jz	00104$
      002EC8 12 40 6D         [24]  616 	lcall	_timer_read
      002ECB AE 82            [24]  617 	mov	r6, dpl
      002ECD AF 83            [24]  618 	mov	r7, dph
      002ECF 90 0B D2         [24]  619 	mov	dptr,#_idle_timer
      002ED2 E0               [24]  620 	movx	a,@dptr
      002ED3 FC               [12]  621 	mov	r4,a
      002ED4 A3               [24]  622 	inc	dptr
      002ED5 E0               [24]  623 	movx	a,@dptr
      002ED6 FD               [12]  624 	mov	r5,a
      002ED7 EE               [12]  625 	mov	a,r6
      002ED8 C3               [12]  626 	clr	c
      002ED9 9C               [12]  627 	subb	a,r4
      002EDA FE               [12]  628 	mov	r6,a
      002EDB EF               [12]  629 	mov	a,r7
      002EDC 9D               [12]  630 	subb	a,r5
      002EDD FF               [12]  631 	mov	r7,a
      002EDE C3               [12]  632 	clr	c
      002EDF EE               [12]  633 	mov	a,r6
      002EE0 94 FF            [12]  634 	subb	a,#0xff
      002EE2 EF               [12]  635 	mov	a,r7
      002EE3 94 7F            [12]  636 	subb	a,#0x7f
      002EE5 50 03            [24]  637 	jnc	00104$
                                    638 ;	quantum/caps_word.c:43: caps_word_off();
                                    639 ;	quantum/caps_word.c:45: }
      002EE7 02 2F 1C         [24]  640 	ljmp	_caps_word_off
      002EEA                        641 00104$:
      002EEA 22               [24]  642 	ret
                                    643 ;------------------------------------------------------------
                                    644 ;Allocation info for local variables in function 'caps_word_reset_idle_timer'
                                    645 ;------------------------------------------------------------
                                    646 ;	quantum/caps_word.c:47: void caps_word_reset_idle_timer(void) {
                                    647 ;	-----------------------------------------
                                    648 ;	 function caps_word_reset_idle_timer
                                    649 ;	-----------------------------------------
      002EEB                        650 _caps_word_reset_idle_timer:
                                    651 ;	quantum/caps_word.c:48: idle_timer = timer_read() + CAPS_WORD_IDLE_TIMEOUT;
      002EEB 12 40 6D         [24]  652 	lcall	_timer_read
      002EEE AE 82            [24]  653 	mov	r6, dpl
      002EF0 AF 83            [24]  654 	mov	r7, dph
      002EF2 74 88            [12]  655 	mov	a,#0x88
      002EF4 2E               [12]  656 	add	a, r6
      002EF5 FE               [12]  657 	mov	r6,a
      002EF6 74 13            [12]  658 	mov	a,#0x13
      002EF8 3F               [12]  659 	addc	a, r7
      002EF9 FF               [12]  660 	mov	r7,a
      002EFA 90 0B D2         [24]  661 	mov	dptr,#_idle_timer
      002EFD EE               [12]  662 	mov	a,r6
      002EFE F0               [24]  663 	movx	@dptr,a
      002EFF EF               [12]  664 	mov	a,r7
      002F00 A3               [24]  665 	inc	dptr
      002F01 F0               [24]  666 	movx	@dptr,a
                                    667 ;	quantum/caps_word.c:49: }
      002F02 22               [24]  668 	ret
                                    669 ;------------------------------------------------------------
                                    670 ;Allocation info for local variables in function 'caps_word_on'
                                    671 ;------------------------------------------------------------
                                    672 ;	quantum/caps_word.c:54: void caps_word_on(void) {
                                    673 ;	-----------------------------------------
                                    674 ;	 function caps_word_on
                                    675 ;	-----------------------------------------
      002F03                        676 _caps_word_on:
                                    677 ;	quantum/caps_word.c:55: if (caps_word_active) {
      002F03 90 0B D1         [24]  678 	mov	dptr,#_caps_word_active
      002F06 E0               [24]  679 	movx	a,@dptr
      002F07 60 01            [24]  680 	jz	00102$
                                    681 ;	quantum/caps_word.c:56: return;
      002F09 22               [24]  682 	ret
      002F0A                        683 00102$:
                                    684 ;	quantum/caps_word.c:59: clear_mods();
      002F0A 12 78 AC         [24]  685 	lcall	_clear_mods
                                    686 ;	quantum/caps_word.c:64: caps_word_reset_idle_timer();
      002F0D 12 2E EB         [24]  687 	lcall	_caps_word_reset_idle_timer
                                    688 ;	quantum/caps_word.c:67: caps_word_active = true;
      002F10 90 0B D1         [24]  689 	mov	dptr,#_caps_word_active
      002F13 74 01            [12]  690 	mov	a,#0x01
      002F15 F0               [24]  691 	movx	@dptr,a
                                    692 ;	quantum/caps_word.c:68: caps_word_set_user(true);
      002F16 75 82 01         [24]  693 	mov	dpl, #0x01
                                    694 ;	quantum/caps_word.c:69: }
      002F19 02 2F 47         [24]  695 	ljmp	_caps_word_set_user
                                    696 ;------------------------------------------------------------
                                    697 ;Allocation info for local variables in function 'caps_word_off'
                                    698 ;------------------------------------------------------------
                                    699 ;	quantum/caps_word.c:71: void caps_word_off(void) {
                                    700 ;	-----------------------------------------
                                    701 ;	 function caps_word_off
                                    702 ;	-----------------------------------------
      002F1C                        703 _caps_word_off:
                                    704 ;	quantum/caps_word.c:72: if (!caps_word_active) {
      002F1C 90 0B D1         [24]  705 	mov	dptr,#_caps_word_active
      002F1F E0               [24]  706 	movx	a,@dptr
      002F20 70 01            [24]  707 	jnz	00102$
                                    708 ;	quantum/caps_word.c:73: return;
      002F22 22               [24]  709 	ret
      002F23                        710 00102$:
                                    711 ;	quantum/caps_word.c:76: unregister_weak_mods(MOD_MASK_SHIFT); // Make sure weak shift is off.
      002F23 75 82 22         [24]  712 	mov	dpl, #0x22
      002F26 12 73 80         [24]  713 	lcall	_unregister_weak_mods
                                    714 ;	quantum/caps_word.c:77: caps_word_active = false;
      002F29 90 0B D1         [24]  715 	mov	dptr,#_caps_word_active
      002F2C E4               [12]  716 	clr	a
      002F2D F0               [24]  717 	movx	@dptr,a
                                    718 ;	quantum/caps_word.c:78: caps_word_set_user(false);
      002F2E 75 82 00         [24]  719 	mov	dpl, #0x00
                                    720 ;	quantum/caps_word.c:79: }
      002F31 02 2F 47         [24]  721 	ljmp	_caps_word_set_user
                                    722 ;------------------------------------------------------------
                                    723 ;Allocation info for local variables in function 'caps_word_toggle'
                                    724 ;------------------------------------------------------------
                                    725 ;	quantum/caps_word.c:81: void caps_word_toggle(void) {
                                    726 ;	-----------------------------------------
                                    727 ;	 function caps_word_toggle
                                    728 ;	-----------------------------------------
      002F34                        729 _caps_word_toggle:
                                    730 ;	quantum/caps_word.c:82: if (caps_word_active) {
      002F34 90 0B D1         [24]  731 	mov	dptr,#_caps_word_active
      002F37 E0               [24]  732 	movx	a,@dptr
      002F38 60 03            [24]  733 	jz	00102$
                                    734 ;	quantum/caps_word.c:83: caps_word_off();
      002F3A 02 2F 1C         [24]  735 	ljmp	_caps_word_off
      002F3D                        736 00102$:
                                    737 ;	quantum/caps_word.c:85: caps_word_on();
                                    738 ;	quantum/caps_word.c:87: }
      002F3D 02 2F 03         [24]  739 	ljmp	_caps_word_on
                                    740 ;------------------------------------------------------------
                                    741 ;Allocation info for local variables in function 'is_caps_word_on'
                                    742 ;------------------------------------------------------------
                                    743 ;	quantum/caps_word.c:89: bool is_caps_word_on(void) {
                                    744 ;	-----------------------------------------
                                    745 ;	 function is_caps_word_on
                                    746 ;	-----------------------------------------
      002F40                        747 _is_caps_word_on:
                                    748 ;	quantum/caps_word.c:90: return caps_word_active;
      002F40 90 0B D1         [24]  749 	mov	dptr,#_caps_word_active
      002F43 E0               [24]  750 	movx	a,@dptr
                                    751 ;	quantum/caps_word.c:91: }
      002F44 F5 82            [12]  752 	mov	dpl,a
      002F46 22               [24]  753 	ret
                                    754 ;------------------------------------------------------------
                                    755 ;Allocation info for local variables in function 'caps_word_set_user'
                                    756 ;------------------------------------------------------------
                                    757 ;active        Allocated with name '_caps_word_set_user_active_10000_239'
                                    758 ;------------------------------------------------------------
                                    759 ;	quantum/caps_word.c:93: __attribute__((weak)) void caps_word_set_user(bool active) {}
                                    760 ;	-----------------------------------------
                                    761 ;	 function caps_word_set_user
                                    762 ;	-----------------------------------------
      002F47                        763 _caps_word_set_user:
      002F47 22               [24]  764 	ret
                                    765 ;------------------------------------------------------------
                                    766 ;Allocation info for local variables in function 'caps_word_press_user'
                                    767 ;------------------------------------------------------------
                                    768 ;keycode       Allocated with name '_caps_word_press_user_keycode_10000_242'
                                    769 ;------------------------------------------------------------
                                    770 ;	quantum/caps_word.c:97: __attribute__((weak)) bool caps_word_press_user(uint16_t keycode) {
                                    771 ;	-----------------------------------------
                                    772 ;	 function caps_word_press_user
                                    773 ;	-----------------------------------------
      002F48                        774 _caps_word_press_user:
      002F48 AF 83            [24]  775 	mov	r7,dph
      002F4A E5 82            [12]  776 	mov	a,dpl
      002F4C 90 08 BF         [24]  777 	mov	dptr,#_caps_word_press_user_keycode_10000_242
      002F4F F0               [24]  778 	movx	@dptr,a
      002F50 EF               [12]  779 	mov	a,r7
      002F51 A3               [24]  780 	inc	dptr
      002F52 F0               [24]  781 	movx	@dptr,a
                                    782 ;	quantum/caps_word.c:98: if ((keycode >= KC_A && keycode <= KC_Z) || keycode == KC_MINS) {
      002F53 90 08 BF         [24]  783 	mov	dptr,#_caps_word_press_user_keycode_10000_242
      002F56 E0               [24]  784 	movx	a,@dptr
      002F57 FE               [12]  785 	mov	r6,a
      002F58 A3               [24]  786 	inc	dptr
      002F59 E0               [24]  787 	movx	a,@dptr
      002F5A FF               [12]  788 	mov	r7,a
      002F5B C3               [12]  789 	clr	c
      002F5C EE               [12]  790 	mov	a,r6
      002F5D 94 04            [12]  791 	subb	a,#0x04
      002F5F EF               [12]  792 	mov	a,r7
      002F60 94 00            [12]  793 	subb	a,#0x00
      002F62 40 07            [24]  794 	jc	00104$
      002F64 74 1D            [12]  795 	mov	a,#0x1d
      002F66 9E               [12]  796 	subb	a,r6
      002F67 E4               [12]  797 	clr	a
      002F68 9F               [12]  798 	subb	a,r7
      002F69 50 06            [24]  799 	jnc	00101$
                                    800 ;	free result
      002F6B                        801 00104$:
      002F6B BE 2D 0D         [24]  802 	cjne	r6,#0x2d,00102$
      002F6E BF 00 0A         [24]  803 	cjne	r7,#0x00,00102$
      002F71                        804 00101$:
                                    805 ;	quantum/caps_word.c:99: add_weak_mods(MOD_BIT(KC_LSFT));
      002F71 75 82 02         [24]  806 	mov	dpl, #0x02
      002F74 12 78 B9         [24]  807 	lcall	_add_weak_mods
                                    808 ;	quantum/caps_word.c:100: return true;
      002F77 75 82 01         [24]  809 	mov	dpl, #0x01
      002F7A 22               [24]  810 	ret
      002F7B                        811 00102$:
                                    812 ;	quantum/caps_word.c:102: return (keycode >= KC_1 && keycode <= KC_0) || keycode == KC_BSPC ||
      002F7B C3               [12]  813 	clr	c
      002F7C EE               [12]  814 	mov	a,r6
      002F7D 94 1E            [12]  815 	subb	a,#0x1e
      002F7F EF               [12]  816 	mov	a,r7
      002F80 94 00            [12]  817 	subb	a,#0x00
      002F82 40 07            [24]  818 	jc	00118$
      002F84 74 27            [12]  819 	mov	a,#0x27
      002F86 9E               [12]  820 	subb	a,r6
      002F87 E4               [12]  821 	clr	a
      002F88 9F               [12]  822 	subb	a,r7
      002F89 50 1C            [24]  823 	jnc	00108$
                                    824 ;	free result
      002F8B                        825 00118$:
      002F8B BE 2A 05         [24]  826 	cjne	r6,#0x2a,00160$
      002F8E BF 00 02         [24]  827 	cjne	r7,#0x00,00160$
      002F91 80 14            [24]  828 	sjmp	00108$
      002F93                        829 00160$:
                                    830 ;	quantum/caps_word.c:103: keycode == KC_DEL || keycode == KC_UNDS;
      002F93 BE 4C 05         [24]  831 	cjne	r6,#0x4c,00161$
      002F96 BF 00 02         [24]  832 	cjne	r7,#0x00,00161$
      002F99 80 0C            [24]  833 	sjmp	00108$
      002F9B                        834 00161$:
      002F9B BE 2D 05         [24]  835 	cjne	r6,#0x2d,00162$
      002F9E BF 02 02         [24]  836 	cjne	r7,#0x02,00162$
      002FA1 80 04            [24]  837 	sjmp	00108$
      002FA3                        838 00162$:
                                    839 ;	assignBit
      002FA3 C2 0E            [12]  840 	clr	_caps_word_press_user_sloc0_1_0
      002FA5 80 02            [24]  841 	sjmp	00109$
      002FA7                        842 00108$:
                                    843 ;	assignBit
      002FA7 D2 0E            [12]  844 	setb	_caps_word_press_user_sloc0_1_0
      002FA9                        845 00109$:
      002FA9 A2 0E            [12]  846 	mov	c,_caps_word_press_user_sloc0_1_0
      002FAB E4               [12]  847 	clr	a
      002FAC 33               [12]  848 	rlc	a
      002FAD F5 82            [12]  849 	mov	dpl, a
                                    850 ;	quantum/caps_word.c:104: }
      002FAF 22               [24]  851 	ret
                                    852 	.area AK820LOW(CODE)
                                    853 	.area CONST   (CODE)
                                    854 	.area XINIT   (CODE)
      00BDAE                        855 __xinit__caps_word_active:
      00BDAE 00                     856 	.db #0x00	;  0
      00BDAF                        857 __xinit__idle_timer:
      00BDAF 00 00                  858 	.byte #0x00, #0x00	; 0
                                    859 	.area CABS    (ABS,CODE)
