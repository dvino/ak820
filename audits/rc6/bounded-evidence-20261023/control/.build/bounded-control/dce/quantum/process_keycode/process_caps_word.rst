                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module process_caps_word
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _clear_weak_mods
                                     12 	.globl _get_mods
                                     13 	.globl _send_keyboard_report
                                     14 	.globl _is_caps_word_on
                                     15 	.globl _caps_word_toggle
                                     16 	.globl _caps_word_off
                                     17 	.globl _caps_word_reset_idle_timer
                                     18 	.globl _caps_word_press_user
                                     19 	.globl _ADC_START
                                     20 	.globl _S0_R_FIFO
                                     21 	.globl _S0_T_FIFO
                                     22 	.globl _S0_FREE
                                     23 	.globl _S0_IF_BYTE
                                     24 	.globl _S0_IF_FIRST
                                     25 	.globl _S0_IF_OV
                                     26 	.globl _S0_FST_ACT
                                     27 	.globl _CP_RL2
                                     28 	.globl _C_T2
                                     29 	.globl _TR2
                                     30 	.globl _EXEN2
                                     31 	.globl _TCLK
                                     32 	.globl _RCLK
                                     33 	.globl _EXF2
                                     34 	.globl _CAP1F
                                     35 	.globl _TF2
                                     36 	.globl _RI
                                     37 	.globl _TI
                                     38 	.globl _RB8
                                     39 	.globl _TB8
                                     40 	.globl _REN
                                     41 	.globl _SM2
                                     42 	.globl _SM1
                                     43 	.globl _SM0
                                     44 	.globl _IT0
                                     45 	.globl _IE0
                                     46 	.globl _IT1
                                     47 	.globl _IE1
                                     48 	.globl _TR0
                                     49 	.globl _TF0
                                     50 	.globl _TR1
                                     51 	.globl _TF1
                                     52 	.globl _P4_0
                                     53 	.globl _P4_1
                                     54 	.globl _P4_2
                                     55 	.globl _P4_3
                                     56 	.globl _P4_4
                                     57 	.globl _P4_5
                                     58 	.globl _P4_6
                                     59 	.globl _RXD
                                     60 	.globl _TXD
                                     61 	.globl _INT0
                                     62 	.globl _INT1
                                     63 	.globl _T0
                                     64 	.globl _T1
                                     65 	.globl _MOSI1
                                     66 	.globl _MISO1
                                     67 	.globl _SCK1
                                     68 	.globl _P3_0
                                     69 	.globl _P3_1
                                     70 	.globl _P3_2
                                     71 	.globl _P3_3
                                     72 	.globl _P3_4
                                     73 	.globl _P3_5
                                     74 	.globl _P3_6
                                     75 	.globl _P3_7
                                     76 	.globl _CAP1_
                                     77 	.globl _T2_
                                     78 	.globl _CAP2_
                                     79 	.globl _T2EX_
                                     80 	.globl _RXD1
                                     81 	.globl _TXD1
                                     82 	.globl _P2_0
                                     83 	.globl _P2_1
                                     84 	.globl _P2_2
                                     85 	.globl _P2_3
                                     86 	.globl _P2_4
                                     87 	.globl _P2_5
                                     88 	.globl _P2_6
                                     89 	.globl _P2_7
                                     90 	.globl _AIN0
                                     91 	.globl _AIN1
                                     92 	.globl _AIN2
                                     93 	.globl _AIN3
                                     94 	.globl _AIN4
                                     95 	.globl _AIN5
                                     96 	.globl _AIN6
                                     97 	.globl _AIN7
                                     98 	.globl _CAP1
                                     99 	.globl _T2
                                    100 	.globl _CAP2
                                    101 	.globl _T2EX
                                    102 	.globl _INT0_
                                    103 	.globl _SCS
                                    104 	.globl _MOSI
                                    105 	.globl _MISO
                                    106 	.globl _SCK
                                    107 	.globl _RXD1_
                                    108 	.globl _TXD1_
                                    109 	.globl _P1_0
                                    110 	.globl _P1_1
                                    111 	.globl _P1_2
                                    112 	.globl _P1_3
                                    113 	.globl _P1_4
                                    114 	.globl _P1_5
                                    115 	.globl _P1_6
                                    116 	.globl _P1_7
                                    117 	.globl _AIN8
                                    118 	.globl _AIN9
                                    119 	.globl _AIN10
                                    120 	.globl _AIN11
                                    121 	.globl _AIN12
                                    122 	.globl _AIN13
                                    123 	.globl _RXD_
                                    124 	.globl _TXD_
                                    125 	.globl _SCL0
                                    126 	.globl _SDA0
                                    127 	.globl _P0_0
                                    128 	.globl _P0_1
                                    129 	.globl _P0_2
                                    130 	.globl _P0_3
                                    131 	.globl _P0_4
                                    132 	.globl _P0_5
                                    133 	.globl _P0_6
                                    134 	.globl _P0_7
                                    135 	.globl _IE_SPI0
                                    136 	.globl _IE_USB
                                    137 	.globl _IE_ADC
                                    138 	.globl _IE_UART1
                                    139 	.globl _IE_PWM_I2C
                                    140 	.globl _IE_GPIO
                                    141 	.globl _IE_WDOG
                                    142 	.globl _PX0
                                    143 	.globl _PT0
                                    144 	.globl _PX1
                                    145 	.globl _PT1
                                    146 	.globl _PS
                                    147 	.globl _PT2
                                    148 	.globl _PL_FLAG
                                    149 	.globl _PH_FLAG
                                    150 	.globl _EX0
                                    151 	.globl _ET0
                                    152 	.globl _EX1
                                    153 	.globl _ET1
                                    154 	.globl _ES
                                    155 	.globl _ET2
                                    156 	.globl _E_DIS
                                    157 	.globl _EA
                                    158 	.globl _P
                                    159 	.globl _F1
                                    160 	.globl _OV
                                    161 	.globl _RS0
                                    162 	.globl _RS1
                                    163 	.globl _F0
                                    164 	.globl _AC
                                    165 	.globl _CY
                                    166 	.globl _I2CS_INT_ST
                                    167 	.globl _I2CX_INT
                                    168 	.globl _LED_STATUS
                                    169 	.globl _LED_DMA_H
                                    170 	.globl _LED_DMA_L
                                    171 	.globl _LED_DMA
                                    172 	.globl _LED_PWM_OE
                                    173 	.globl _LED_COMMON
                                    174 	.globl _ADC_CHAN
                                    175 	.globl _ADC_DAT_H
                                    176 	.globl _ADC_DAT_L
                                    177 	.globl _ADC_DAT
                                    178 	.globl _ADC_CTRL
                                    179 	.globl _SPI1_CK_SE
                                    180 	.globl _SPI1_CTRL
                                    181 	.globl _SPI1_DATA
                                    182 	.globl _SPI1_STAT
                                    183 	.globl _SIF1
                                    184 	.globl _SBAUD1
                                    185 	.globl _SBUF1
                                    186 	.globl _SCON1
                                    187 	.globl _SPI0_SETUP
                                    188 	.globl _SPI0_CK_SE
                                    189 	.globl _SPI0_CTRL
                                    190 	.globl _SPI0_DATA
                                    191 	.globl _SPI0_STAT
                                    192 	.globl _T2CAP1H
                                    193 	.globl _T2CAP1L
                                    194 	.globl _T2CAP1
                                    195 	.globl _TH2
                                    196 	.globl _TL2
                                    197 	.globl _T2COUNT
                                    198 	.globl _RCAP2H
                                    199 	.globl _RCAP2L
                                    200 	.globl _RCAP2
                                    201 	.globl _T2MOD
                                    202 	.globl _T2CON
                                    203 	.globl _SBUF
                                    204 	.globl _SCON
                                    205 	.globl _TH1
                                    206 	.globl _TH0
                                    207 	.globl _TL1
                                    208 	.globl _TL0
                                    209 	.globl _TMOD
                                    210 	.globl _TCON
                                    211 	.globl _XBUS_AUX
                                    212 	.globl _P7
                                    213 	.globl _P6_DIR
                                    214 	.globl _P6_OUT_PU
                                    215 	.globl _P6_IN
                                    216 	.globl _P5_DIR
                                    217 	.globl _P5_OUT_PU
                                    218 	.globl _P5_IN
                                    219 	.globl _P4_LED_KEY
                                    220 	.globl _P4_DIR_PU
                                    221 	.globl _P4_MOD_OC
                                    222 	.globl _P4
                                    223 	.globl _P3_DIR_PU
                                    224 	.globl _P3_MOD_OC
                                    225 	.globl _P3
                                    226 	.globl _P2_DIR_PU
                                    227 	.globl _P2_MOD_OC
                                    228 	.globl _P2
                                    229 	.globl _P1_DIR_PU
                                    230 	.globl _P1_MOD_OC
                                    231 	.globl _P1
                                    232 	.globl _P0_DIR_PU
                                    233 	.globl _P0_MOD_OC
                                    234 	.globl _P0
                                    235 	.globl _ROM_CTRL
                                    236 	.globl _ROM_DATA_HH
                                    237 	.globl _ROM_DATA_HL
                                    238 	.globl _ROM_DATA_HI
                                    239 	.globl _ROM_ADDR_H
                                    240 	.globl _ROM_ADDR_L
                                    241 	.globl _ROM_ADDR
                                    242 	.globl _GPIO_IE
                                    243 	.globl _IP_EX
                                    244 	.globl _IE_EX
                                    245 	.globl _IP
                                    246 	.globl _IE
                                    247 	.globl _WDOG_COUNT
                                    248 	.globl _RESET_KEEP
                                    249 	.globl _WAKE_CTRL
                                    250 	.globl _CLOCK_CFG
                                    251 	.globl _POWER_CFG
                                    252 	.globl _PCON
                                    253 	.globl _GLOBAL_CFG
                                    254 	.globl _SAFE_MOD
                                    255 	.globl _DPH
                                    256 	.globl _DPL
                                    257 	.globl _SP
                                    258 	.globl _A_INV
                                    259 	.globl _B
                                    260 	.globl _ACC
                                    261 	.globl _PSW
                                    262 	.globl _process_caps_word_PARM_2
                                    263 	.globl _process_caps_word
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
                                    526 ;--------------------------------------------------------
                                    527 ; overlayable items in internal ram
                                    528 ;--------------------------------------------------------
                                    529 ;--------------------------------------------------------
                                    530 ; indirectly addressable internal ram data
                                    531 ;--------------------------------------------------------
                                    532 	.area ISEG    (DATA)
                                    533 ;--------------------------------------------------------
                                    534 ; absolute internal ram data
                                    535 ;--------------------------------------------------------
                                    536 	.area IABS    (ABS,DATA)
                                    537 	.area IABS    (ABS,DATA)
                                    538 ;--------------------------------------------------------
                                    539 ; bit data
                                    540 ;--------------------------------------------------------
                                    541 	.area BSEG    (BIT)
                                    542 ;--------------------------------------------------------
                                    543 ; paged external ram data
                                    544 ;--------------------------------------------------------
                                    545 	.area PSEG    (PAG,XDATA)
                                    546 ;--------------------------------------------------------
                                    547 ; uninitialized external ram data
                                    548 ;--------------------------------------------------------
                                    549 	.area XSEG    (XDATA)
      0009A2                        550 _process_caps_word_PARM_2:
      0009A2                        551 	.ds 3
      0009A5                        552 _process_caps_word_keycode_10000_237:
      0009A5                        553 	.ds 2
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
                                    589 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    590 ;------------------------------------------------------------
                                    591 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_175'
                                    592 ;------------------------------------------------------------
                                    593 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    594 ;	-----------------------------------------
                           000007   595 	ar7 = 0x07
                           000006   596 	ar6 = 0x06
                           000005   597 	ar5 = 0x05
                           000004   598 	ar4 = 0x04
                           000003   599 	ar3 = 0x03
                           000002   600 	ar2 = 0x02
                           000001   601 	ar1 = 0x01
                           000000   602 	ar0 = 0x00
                                    603 ;	 function process_caps_word
                                    604 ;	-----------------------------------------
      0091B0                        605 _process_caps_word:
      0091B0 AF 83            [24]  606 	mov	r7,dph
      0091B2 E5 82            [12]  607 	mov	a,dpl
      0091B4 90 09 A5         [24]  608 	mov	dptr,#_process_caps_word_keycode_10000_237
      0091B7 F0               [24]  609 	movx	@dptr,a
      0091B8 EF               [12]  610 	mov	a,r7
      0091B9 A3               [24]  611 	inc	dptr
      0091BA F0               [24]  612 	movx	@dptr,a
                                    613 ;	quantum/process_keycode/process_caps_word.c:78: keyrecord_t __xdata* record = (keyrecord_t __xdata*)event_record;
      0091BB 90 09 A2         [24]  614 	mov	dptr,#_process_caps_word_PARM_2
      0091BE E0               [24]  615 	movx	a,@dptr
      0091BF FE               [12]  616 	mov	r6,a
      0091C0 A3               [24]  617 	inc	dptr
      0091C1 E0               [24]  618 	movx	a,@dptr
      0091C2 FF               [12]  619 	mov	r7,a
                                    620 ;	quantum/process_keycode/process_caps_word.c:82: if (keycode == QK_CAPS_WORD_TOGGLE) {
      0091C3 90 09 A5         [24]  621 	mov	dptr,#_process_caps_word_keycode_10000_237
      0091C6 E0               [24]  622 	movx	a,@dptr
      0091C7 FC               [12]  623 	mov	r4,a
      0091C8 A3               [24]  624 	inc	dptr
      0091C9 E0               [24]  625 	movx	a,@dptr
      0091CA FD               [12]  626 	mov	r5,a
      0091CB BC 73 18         [24]  627 	cjne	r4,#0x73,00104$
      0091CE BD 7C 15         [24]  628 	cjne	r5,#0x7c,00104$
                                    629 ;	quantum/process_keycode/process_caps_word.c:83: if (record->event.pressed) {
      0091D1 74 05            [12]  630 	mov	a,#0x05
      0091D3 2E               [12]  631 	add	a, r6
      0091D4 FA               [12]  632 	mov	r2,a
      0091D5 E4               [12]  633 	clr	a
      0091D6 3F               [12]  634 	addc	a, r7
      0091D7 FB               [12]  635 	mov	r3,a
      0091D8 8A 82            [24]  636 	mov	dpl,r2
      0091DA 8B 83            [24]  637 	mov	dph,r3
      0091DC E0               [24]  638 	movx	a,@dptr
      0091DD 60 03            [24]  639 	jz	00102$
                                    640 ;	quantum/process_keycode/process_caps_word.c:84: caps_word_toggle();
      0091DF 12 2F 34         [24]  641 	lcall	_caps_word_toggle
      0091E2                        642 00102$:
                                    643 ;	quantum/process_keycode/process_caps_word.c:86: return false;
      0091E2 75 82 00         [24]  644 	mov	dpl, #0x00
      0091E5 22               [24]  645 	ret
      0091E6                        646 00104$:
                                    647 ;	quantum/process_keycode/process_caps_word.c:97: const uint8_t mods = get_mods();
      0091E6 12 78 86         [24]  648 	lcall	_get_mods
      0091E9 AB 82            [24]  649 	mov	r3, dpl
                                    650 ;	quantum/process_keycode/process_caps_word.c:100: if (!is_caps_word_on()) {
      0091EB C0 07            [24]  651 	push	ar7
      0091ED C0 06            [24]  652 	push	ar6
      0091EF C0 05            [24]  653 	push	ar5
      0091F1 C0 04            [24]  654 	push	ar4
      0091F3 C0 03            [24]  655 	push	ar3
      0091F5 12 2F 40         [24]  656 	lcall	_is_caps_word_on
      0091F8 E5 82            [12]  657 	mov	a, dpl
      0091FA D0 03            [24]  658 	pop	ar3
      0091FC D0 04            [24]  659 	pop	ar4
      0091FE D0 05            [24]  660 	pop	ar5
      009200 D0 06            [24]  661 	pop	ar6
      009202 D0 07            [24]  662 	pop	ar7
      009204 70 04            [24]  663 	jnz	00106$
                                    664 ;	quantum/process_keycode/process_caps_word.c:147: return true;
      009206 75 82 01         [24]  665 	mov	dpl, #0x01
      009209 22               [24]  666 	ret
      00920A                        667 00106$:
                                    668 ;	quantum/process_keycode/process_caps_word.c:151: caps_word_reset_idle_timer();
      00920A C0 07            [24]  669 	push	ar7
      00920C C0 06            [24]  670 	push	ar6
      00920E C0 05            [24]  671 	push	ar5
      009210 C0 04            [24]  672 	push	ar4
      009212 C0 03            [24]  673 	push	ar3
      009214 12 2E EB         [24]  674 	lcall	_caps_word_reset_idle_timer
      009217 D0 03            [24]  675 	pop	ar3
      009219 D0 04            [24]  676 	pop	ar4
      00921B D0 05            [24]  677 	pop	ar5
      00921D D0 06            [24]  678 	pop	ar6
      00921F D0 07            [24]  679 	pop	ar7
                                    680 ;	quantum/process_keycode/process_caps_word.c:155: if (!record->event.pressed) {
      009221 74 05            [12]  681 	mov	a,#0x05
      009223 2E               [12]  682 	add	a, r6
      009224 FE               [12]  683 	mov	r6,a
      009225 E4               [12]  684 	clr	a
      009226 3F               [12]  685 	addc	a, r7
      009227 FF               [12]  686 	mov	r7,a
      009228 8E 82            [24]  687 	mov	dpl,r6
      00922A 8F 83            [24]  688 	mov	dph,r7
      00922C E0               [24]  689 	movx	a,@dptr
      00922D 70 04            [24]  690 	jnz	00108$
                                    691 ;	quantum/process_keycode/process_caps_word.c:156: return true;
      00922F 75 82 01         [24]  692 	mov	dpl, #0x01
      009232 22               [24]  693 	ret
      009233                        694 00108$:
                                    695 ;	quantum/process_keycode/process_caps_word.c:159: if (!(mods & ~(MOD_MASK_SHIFT | MOD_BIT(KC_RALT)))) {
      009233 EB               [12]  696 	mov	a,r3
      009234 54 9D            [12]  697 	anl	a,#0x9d
      009236 60 03            [24]  698 	jz	00227$
      009238 02 92 D3         [24]  699 	ljmp	00127$
      00923B                        700 00227$:
                                    701 ;	quantum/process_keycode/process_caps_word.c:162: if ( (keycode >= QK_MOMENTARY && keycode <= QK_MOMENTARY_MAX) ||
      00923B C3               [12]  702 	clr	c
      00923C EC               [12]  703 	mov	a,r4
      00923D 94 20            [12]  704 	subb	a,#0x20
      00923F ED               [12]  705 	mov	a,r5
      009240 94 52            [12]  706 	subb	a,#0x52
      009242 40 08            [24]  707 	jc	00113$
      009244 74 3F            [12]  708 	mov	a,#0x3f
      009246 9C               [12]  709 	subb	a,r4
      009247 74 52            [12]  710 	mov	a,#0x52
      009249 9D               [12]  711 	subb	a,r5
      00924A 50 66            [24]  712 	jnc	00109$
                                    713 ;	free result
      00924C                        714 00113$:
                                    715 ;	quantum/process_keycode/process_caps_word.c:163: (keycode >= QK_TO               && keycode <= QK_TO_MAX) ||
      00924C 74 AE            [12]  716 	mov	a,#0x100 - 0x52
      00924E 2D               [12]  717 	add	a,r5
      00924F 50 09            [24]  718 	jnc	00115$
      009251 C3               [12]  719 	clr	c
      009252 74 1F            [12]  720 	mov	a,#0x1f
      009254 9C               [12]  721 	subb	a,r4
      009255 74 52            [12]  722 	mov	a,#0x52
      009257 9D               [12]  723 	subb	a,r5
      009258 50 58            [24]  724 	jnc	00109$
                                    725 ;	free result
      00925A                        726 00115$:
                                    727 ;	quantum/process_keycode/process_caps_word.c:164: (keycode >= QK_TOGGLE_LAYER     && keycode <= QK_TOGGLE_LAYER_MAX) ||
      00925A C3               [12]  728 	clr	c
      00925B EC               [12]  729 	mov	a,r4
      00925C 94 60            [12]  730 	subb	a,#0x60
      00925E ED               [12]  731 	mov	a,r5
      00925F 94 52            [12]  732 	subb	a,#0x52
      009261 40 08            [24]  733 	jc	00117$
      009263 74 7F            [12]  734 	mov	a,#0x7f
      009265 9C               [12]  735 	subb	a,r4
      009266 74 52            [12]  736 	mov	a,#0x52
      009268 9D               [12]  737 	subb	a,r5
      009269 50 47            [24]  738 	jnc	00109$
                                    739 ;	free result
      00926B                        740 00117$:
                                    741 ;	quantum/process_keycode/process_caps_word.c:165: (keycode >= QK_LAYER_TAP_TOGGLE && keycode <= QK_LAYER_TAP_TOGGLE_MAX) ||
      00926B C3               [12]  742 	clr	c
      00926C EC               [12]  743 	mov	a,r4
      00926D 94 C0            [12]  744 	subb	a,#0xc0
      00926F ED               [12]  745 	mov	a,r5
      009270 94 52            [12]  746 	subb	a,#0x52
      009272 40 08            [24]  747 	jc	00119$
      009274 74 DF            [12]  748 	mov	a,#0xdf
      009276 9C               [12]  749 	subb	a,r4
      009277 74 52            [12]  750 	mov	a,#0x52
      009279 9D               [12]  751 	subb	a,r5
      00927A 50 36            [24]  752 	jnc	00109$
                                    753 ;	free result
      00927C                        754 00119$:
                                    755 ;	quantum/process_keycode/process_caps_word.c:166: (keycode >= QK_ONE_SHOT_LAYER   && keycode <= QK_ONE_SHOT_LAYER_MAX) ||
      00927C C3               [12]  756 	clr	c
      00927D EC               [12]  757 	mov	a,r4
      00927E 94 80            [12]  758 	subb	a,#0x80
      009280 ED               [12]  759 	mov	a,r5
      009281 94 52            [12]  760 	subb	a,#0x52
      009283 40 08            [24]  761 	jc	00121$
      009285 74 9F            [12]  762 	mov	a,#0x9f
      009287 9C               [12]  763 	subb	a,r4
      009288 74 52            [12]  764 	mov	a,#0x52
      00928A 9D               [12]  765 	subb	a,r5
      00928B 50 25            [24]  766 	jnc	00109$
                                    767 ;	free result
      00928D                        768 00121$:
                                    769 ;	quantum/process_keycode/process_caps_word.c:167: (keycode >= QK_TRI_LAYER_LOWER  && keycode <= QK_TRI_LAYER_UPPER) ||
      00928D C3               [12]  770 	clr	c
      00928E EC               [12]  771 	mov	a,r4
      00928F 94 77            [12]  772 	subb	a,#0x77
      009291 ED               [12]  773 	mov	a,r5
      009292 94 7C            [12]  774 	subb	a,#0x7c
      009294 40 08            [24]  775 	jc	00122$
      009296 74 78            [12]  776 	mov	a,#0x78
      009298 9C               [12]  777 	subb	a,r4
      009299 74 7C            [12]  778 	mov	a,#0x7c
      00929B 9D               [12]  779 	subb	a,r5
      00929C 50 14            [24]  780 	jnc	00109$
                                    781 ;	free result
      00929E                        782 00122$:
                                    783 ;	quantum/process_keycode/process_caps_word.c:169: (keycode == KC_RALT) ||
      00929E 90 09 A5         [24]  784 	mov	dptr,#_process_caps_word_keycode_10000_237
      0092A1 12 86 24         [24]  785 	lcall	_ak820_outline_0012
      0092A4 BC E6 05         [24]  786 	cjne	r4,#0xe6,00240$
      0092A7 BD 00 02         [24]  787 	cjne	r5,#0x00,00240$
      0092AA 80 06            [24]  788 	sjmp	00109$
      0092AC                        789 00240$:
                                    790 ;	quantum/process_keycode/process_caps_word.c:170: (keycode == OSM(MOD_RALT)) )
      0092AC BC B4 07         [24]  791 	cjne	r4,#0xb4,00110$
      0092AF BD 52 04         [24]  792 	cjne	r5,#0x52,00110$
      0092B2                        793 00109$:
                                    794 ;	quantum/process_keycode/process_caps_word.c:171: return true;
      0092B2 75 82 01         [24]  795 	mov	dpl, #0x01
      0092B5 22               [24]  796 	ret
      0092B6                        797 00110$:
                                    798 ;	quantum/process_keycode/process_caps_word.c:241: clear_weak_mods();
      0092B6 C0 07            [24]  799 	push	ar7
      0092B8 C0 06            [24]  800 	push	ar6
      0092BA 12 78 D8         [24]  801 	lcall	_clear_weak_mods
      0092BD D0 06            [24]  802 	pop	ar6
      0092BF D0 07            [24]  803 	pop	ar7
                                    804 ;	quantum/process_keycode/process_caps_word.c:243: if (caps_word_press_user(keycode)) {
      0092C1 8E 82            [24]  805 	mov	dpl, r6
      0092C3 8F 83            [24]  806 	mov	dph, r7
      0092C5 12 2F 48         [24]  807 	lcall	_caps_word_press_user
      0092C8 E5 82            [12]  808 	mov	a, dpl
      0092CA 60 07            [24]  809 	jz	00127$
                                    810 ;	quantum/process_keycode/process_caps_word.c:249: send_keyboard_report();
      0092CC 12 78 28         [24]  811 	lcall	_send_keyboard_report
                                    812 ;	quantum/process_keycode/process_caps_word.c:250: return true;
      0092CF 75 82 01         [24]  813 	mov	dpl, #0x01
      0092D2 22               [24]  814 	ret
      0092D3                        815 00127$:
                                    816 ;	quantum/process_keycode/process_caps_word.c:254: caps_word_off();
      0092D3 12 2F 1C         [24]  817 	lcall	_caps_word_off
                                    818 ;	quantum/process_keycode/process_caps_word.c:258: return true;
      0092D6 75 82 01         [24]  819 	mov	dpl, #0x01
                                    820 ;	quantum/process_keycode/process_caps_word.c:259: }
      0092D9 22               [24]  821 	ret
                                    822 	.area CSEG    (CODE)
                                    823 	.area CONST   (CODE)
                                    824 	.area XINIT   (CODE)
                                    825 	.area CABS    (ABS,CODE)
                                    826 
                                    827 ; Experimental exact instruction outlining.
                                    828 	.globl _ak820_outline_0012
