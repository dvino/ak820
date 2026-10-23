                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module action_util
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _host_keyboard_send
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
                                    255 	.globl _actual_keyboard_report
                                    256 	.globl _send_keyboard_report
                                    257 	.globl _get_mods
                                    258 	.globl _add_mods
                                    259 	.globl _del_mods
                                    260 	.globl _clear_mods
                                    261 	.globl _get_weak_mods
                                    262 	.globl _add_weak_mods
                                    263 	.globl _del_weak_mods
                                    264 	.globl _clear_weak_mods
                                    265 ;--------------------------------------------------------
                                    266 ; special function registers
                                    267 ;--------------------------------------------------------
                                    268 	.area RSEG    (ABS,DATA)
      000000                        269 	.org 0x0000
                           0000D0   270 _PSW	=	0x00d0
                           0000E0   271 _ACC	=	0x00e0
                           0000F0   272 _B	=	0x00f0
                           0000FD   273 _A_INV	=	0x00fd
                           000081   274 _SP	=	0x0081
                           000082   275 _DPL	=	0x0082
                           000083   276 _DPH	=	0x0083
                           0000A1   277 _SAFE_MOD	=	0x00a1
                           0000B1   278 _GLOBAL_CFG	=	0x00b1
                           000087   279 _PCON	=	0x0087
                           0000BA   280 _POWER_CFG	=	0x00ba
                           0000B9   281 _CLOCK_CFG	=	0x00b9
                           0000A9   282 _WAKE_CTRL	=	0x00a9
                           0000FE   283 _RESET_KEEP	=	0x00fe
                           0000FF   284 _WDOG_COUNT	=	0x00ff
                           0000A8   285 _IE	=	0x00a8
                           0000B8   286 _IP	=	0x00b8
                           0000E8   287 _IE_EX	=	0x00e8
                           0000E9   288 _IP_EX	=	0x00e9
                           0000B2   289 _GPIO_IE	=	0x00b2
                           008584   290 _ROM_ADDR	=	0x8584
                           000084   291 _ROM_ADDR_L	=	0x0084
                           000085   292 _ROM_ADDR_H	=	0x0085
                           008F8E   293 _ROM_DATA_HI	=	0x8f8e
                           00008E   294 _ROM_DATA_HL	=	0x008e
                           00008F   295 _ROM_DATA_HH	=	0x008f
                           000086   296 _ROM_CTRL	=	0x0086
                           000080   297 _P0	=	0x0080
                           0000C4   298 _P0_MOD_OC	=	0x00c4
                           0000C5   299 _P0_DIR_PU	=	0x00c5
                           000090   300 _P1	=	0x0090
                           000092   301 _P1_MOD_OC	=	0x0092
                           000093   302 _P1_DIR_PU	=	0x0093
                           0000A0   303 _P2	=	0x00a0
                           000094   304 _P2_MOD_OC	=	0x0094
                           000095   305 _P2_DIR_PU	=	0x0095
                           0000B0   306 _P3	=	0x00b0
                           000096   307 _P3_MOD_OC	=	0x0096
                           000097   308 _P3_DIR_PU	=	0x0097
                           0000C0   309 _P4	=	0x00c0
                           0000C2   310 _P4_MOD_OC	=	0x00c2
                           0000C3   311 _P4_DIR_PU	=	0x00c3
                           0000C1   312 _P4_LED_KEY	=	0x00c1
                           0000AA   313 _P5_IN	=	0x00aa
                           0000AB   314 _P5_OUT_PU	=	0x00ab
                           0000AC   315 _P5_DIR	=	0x00ac
                           0000AD   316 _P6_IN	=	0x00ad
                           0000AE   317 _P6_OUT_PU	=	0x00ae
                           0000AF   318 _P6_DIR	=	0x00af
                           0000F1   319 _P7	=	0x00f1
                           0000A2   320 _XBUS_AUX	=	0x00a2
                           000088   321 _TCON	=	0x0088
                           000089   322 _TMOD	=	0x0089
                           00008A   323 _TL0	=	0x008a
                           00008B   324 _TL1	=	0x008b
                           00008C   325 _TH0	=	0x008c
                           00008D   326 _TH1	=	0x008d
                           000098   327 _SCON	=	0x0098
                           000099   328 _SBUF	=	0x0099
                           0000C8   329 _T2CON	=	0x00c8
                           0000C9   330 _T2MOD	=	0x00c9
                           00CBCA   331 _RCAP2	=	0xcbca
                           0000CA   332 _RCAP2L	=	0x00ca
                           0000CB   333 _RCAP2H	=	0x00cb
                           00CDCC   334 _T2COUNT	=	0xcdcc
                           0000CC   335 _TL2	=	0x00cc
                           0000CD   336 _TH2	=	0x00cd
                           00CFCE   337 _T2CAP1	=	0xcfce
                           0000CE   338 _T2CAP1L	=	0x00ce
                           0000CF   339 _T2CAP1H	=	0x00cf
                           0000F8   340 _SPI0_STAT	=	0x00f8
                           0000F9   341 _SPI0_DATA	=	0x00f9
                           0000FA   342 _SPI0_CTRL	=	0x00fa
                           0000FB   343 _SPI0_CK_SE	=	0x00fb
                           0000FC   344 _SPI0_SETUP	=	0x00fc
                           0000BC   345 _SCON1	=	0x00bc
                           0000BD   346 _SBUF1	=	0x00bd
                           0000BE   347 _SBAUD1	=	0x00be
                           0000BF   348 _SIF1	=	0x00bf
                           0000B4   349 _SPI1_STAT	=	0x00b4
                           0000B5   350 _SPI1_DATA	=	0x00b5
                           0000B6   351 _SPI1_CTRL	=	0x00b6
                           0000B7   352 _SPI1_CK_SE	=	0x00b7
                           0000F3   353 _ADC_CTRL	=	0x00f3
                           00F5F4   354 _ADC_DAT	=	0xf5f4
                           0000F4   355 _ADC_DAT_L	=	0x00f4
                           0000F5   356 _ADC_DAT_H	=	0x00f5
                           0000F6   357 _ADC_CHAN	=	0x00f6
                           0000A6   358 _LED_COMMON	=	0x00a6
                           0000A7   359 _LED_PWM_OE	=	0x00a7
                           00C7C6   360 _LED_DMA	=	0xc7c6
                           0000C6   361 _LED_DMA_L	=	0x00c6
                           0000C7   362 _LED_DMA_H	=	0x00c7
                           0000F7   363 _LED_STATUS	=	0x00f7
                           0000B3   364 _I2CX_INT	=	0x00b3
                           0000BB   365 _I2CS_INT_ST	=	0x00bb
                                    366 ;--------------------------------------------------------
                                    367 ; special function bits
                                    368 ;--------------------------------------------------------
                                    369 	.area RSEG    (ABS,DATA)
      000000                        370 	.org 0x0000
                           0000D7   371 _CY	=	0x00d7
                           0000D6   372 _AC	=	0x00d6
                           0000D5   373 _F0	=	0x00d5
                           0000D4   374 _RS1	=	0x00d4
                           0000D3   375 _RS0	=	0x00d3
                           0000D2   376 _OV	=	0x00d2
                           0000D1   377 _F1	=	0x00d1
                           0000D0   378 _P	=	0x00d0
                           0000AF   379 _EA	=	0x00af
                           0000AE   380 _E_DIS	=	0x00ae
                           0000AD   381 _ET2	=	0x00ad
                           0000AC   382 _ES	=	0x00ac
                           0000AB   383 _ET1	=	0x00ab
                           0000AA   384 _EX1	=	0x00aa
                           0000A9   385 _ET0	=	0x00a9
                           0000A8   386 _EX0	=	0x00a8
                           0000BF   387 _PH_FLAG	=	0x00bf
                           0000BE   388 _PL_FLAG	=	0x00be
                           0000BD   389 _PT2	=	0x00bd
                           0000BC   390 _PS	=	0x00bc
                           0000BB   391 _PT1	=	0x00bb
                           0000BA   392 _PX1	=	0x00ba
                           0000B9   393 _PT0	=	0x00b9
                           0000B8   394 _PX0	=	0x00b8
                           0000EF   395 _IE_WDOG	=	0x00ef
                           0000EE   396 _IE_GPIO	=	0x00ee
                           0000ED   397 _IE_PWM_I2C	=	0x00ed
                           0000EC   398 _IE_UART1	=	0x00ec
                           0000EB   399 _IE_ADC	=	0x00eb
                           0000E9   400 _IE_USB	=	0x00e9
                           0000E8   401 _IE_SPI0	=	0x00e8
                           000087   402 _P0_7	=	0x0087
                           000086   403 _P0_6	=	0x0086
                           000085   404 _P0_5	=	0x0085
                           000084   405 _P0_4	=	0x0084
                           000083   406 _P0_3	=	0x0083
                           000082   407 _P0_2	=	0x0082
                           000081   408 _P0_1	=	0x0081
                           000080   409 _P0_0	=	0x0080
                           000081   410 _SDA0	=	0x0081
                           000080   411 _SCL0	=	0x0080
                           000083   412 _TXD_	=	0x0083
                           000082   413 _RXD_	=	0x0082
                           000085   414 _AIN13	=	0x0085
                           000084   415 _AIN12	=	0x0084
                           000083   416 _AIN11	=	0x0083
                           000082   417 _AIN10	=	0x0082
                           000081   418 _AIN9	=	0x0081
                           000080   419 _AIN8	=	0x0080
                           000097   420 _P1_7	=	0x0097
                           000096   421 _P1_6	=	0x0096
                           000095   422 _P1_5	=	0x0095
                           000094   423 _P1_4	=	0x0094
                           000093   424 _P1_3	=	0x0093
                           000092   425 _P1_2	=	0x0092
                           000091   426 _P1_1	=	0x0091
                           000090   427 _P1_0	=	0x0090
                           000097   428 _TXD1_	=	0x0097
                           000096   429 _RXD1_	=	0x0096
                           000097   430 _SCK	=	0x0097
                           000096   431 _MISO	=	0x0096
                           000095   432 _MOSI	=	0x0095
                           000094   433 _SCS	=	0x0094
                           000092   434 _INT0_	=	0x0092
                           000091   435 _T2EX	=	0x0091
                           000091   436 _CAP2	=	0x0091
                           000090   437 _T2	=	0x0090
                           000090   438 _CAP1	=	0x0090
                           000097   439 _AIN7	=	0x0097
                           000096   440 _AIN6	=	0x0096
                           000095   441 _AIN5	=	0x0095
                           000094   442 _AIN4	=	0x0094
                           000093   443 _AIN3	=	0x0093
                           000092   444 _AIN2	=	0x0092
                           000091   445 _AIN1	=	0x0091
                           000090   446 _AIN0	=	0x0090
                           0000A7   447 _P2_7	=	0x00a7
                           0000A6   448 _P2_6	=	0x00a6
                           0000A5   449 _P2_5	=	0x00a5
                           0000A4   450 _P2_4	=	0x00a4
                           0000A3   451 _P2_3	=	0x00a3
                           0000A2   452 _P2_2	=	0x00a2
                           0000A1   453 _P2_1	=	0x00a1
                           0000A0   454 _P2_0	=	0x00a0
                           0000A7   455 _TXD1	=	0x00a7
                           0000A6   456 _RXD1	=	0x00a6
                           0000A5   457 _T2EX_	=	0x00a5
                           0000A5   458 _CAP2_	=	0x00a5
                           0000A4   459 _T2_	=	0x00a4
                           0000A4   460 _CAP1_	=	0x00a4
                           0000B7   461 _P3_7	=	0x00b7
                           0000B6   462 _P3_6	=	0x00b6
                           0000B5   463 _P3_5	=	0x00b5
                           0000B4   464 _P3_4	=	0x00b4
                           0000B3   465 _P3_3	=	0x00b3
                           0000B2   466 _P3_2	=	0x00b2
                           0000B1   467 _P3_1	=	0x00b1
                           0000B0   468 _P3_0	=	0x00b0
                           0000B7   469 _SCK1	=	0x00b7
                           0000B6   470 _MISO1	=	0x00b6
                           0000B5   471 _MOSI1	=	0x00b5
                           0000B5   472 _T1	=	0x00b5
                           0000B4   473 _T0	=	0x00b4
                           0000B3   474 _INT1	=	0x00b3
                           0000B2   475 _INT0	=	0x00b2
                           0000B1   476 _TXD	=	0x00b1
                           0000B0   477 _RXD	=	0x00b0
                           0000C6   478 _P4_6	=	0x00c6
                           0000C5   479 _P4_5	=	0x00c5
                           0000C4   480 _P4_4	=	0x00c4
                           0000C3   481 _P4_3	=	0x00c3
                           0000C2   482 _P4_2	=	0x00c2
                           0000C1   483 _P4_1	=	0x00c1
                           0000C0   484 _P4_0	=	0x00c0
                           00008F   485 _TF1	=	0x008f
                           00008E   486 _TR1	=	0x008e
                           00008D   487 _TF0	=	0x008d
                           00008C   488 _TR0	=	0x008c
                           00008B   489 _IE1	=	0x008b
                           00008A   490 _IT1	=	0x008a
                           000089   491 _IE0	=	0x0089
                           000088   492 _IT0	=	0x0088
                           00009F   493 _SM0	=	0x009f
                           00009E   494 _SM1	=	0x009e
                           00009D   495 _SM2	=	0x009d
                           00009C   496 _REN	=	0x009c
                           00009B   497 _TB8	=	0x009b
                           00009A   498 _RB8	=	0x009a
                           000099   499 _TI	=	0x0099
                           000098   500 _RI	=	0x0098
                           0000CF   501 _TF2	=	0x00cf
                           0000CF   502 _CAP1F	=	0x00cf
                           0000CE   503 _EXF2	=	0x00ce
                           0000CD   504 _RCLK	=	0x00cd
                           0000CC   505 _TCLK	=	0x00cc
                           0000CB   506 _EXEN2	=	0x00cb
                           0000CA   507 _TR2	=	0x00ca
                           0000C9   508 _C_T2	=	0x00c9
                           0000C8   509 _CP_RL2	=	0x00c8
                           0000FF   510 _S0_FST_ACT	=	0x00ff
                           0000FE   511 _S0_IF_OV	=	0x00fe
                           0000FD   512 _S0_IF_FIRST	=	0x00fd
                           0000FC   513 _S0_IF_BYTE	=	0x00fc
                           0000FB   514 _S0_FREE	=	0x00fb
                           0000FA   515 _S0_T_FIFO	=	0x00fa
                           0000F8   516 _S0_R_FIFO	=	0x00f8
                           0000F7   517 _ADC_START	=	0x00f7
                                    518 ;--------------------------------------------------------
                                    519 ; overlayable register banks
                                    520 ;--------------------------------------------------------
                                    521 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        522 	.ds 8
                                    523 ;--------------------------------------------------------
                                    524 ; internal ram data
                                    525 ;--------------------------------------------------------
                                    526 	.area DSEG    (DATA)
                                    527 ;--------------------------------------------------------
                                    528 ; overlayable items in internal ram
                                    529 ;--------------------------------------------------------
                                    530 ;--------------------------------------------------------
                                    531 ; indirectly addressable internal ram data
                                    532 ;--------------------------------------------------------
                                    533 	.area ISEG    (DATA)
                                    534 ;--------------------------------------------------------
                                    535 ; absolute internal ram data
                                    536 ;--------------------------------------------------------
                                    537 	.area IABS    (ABS,DATA)
                                    538 	.area IABS    (ABS,DATA)
                                    539 ;--------------------------------------------------------
                                    540 ; bit data
                                    541 ;--------------------------------------------------------
                                    542 	.area BSEG    (BIT)
                                    543 ;--------------------------------------------------------
                                    544 ; paged external ram data
                                    545 ;--------------------------------------------------------
                                    546 	.area PSEG    (PAG,XDATA)
                                    547 ;--------------------------------------------------------
                                    548 ; uninitialized external ram data
                                    549 ;--------------------------------------------------------
                                    550 	.area XSEG    (XDATA)
      000897                        551 _send_keyboard_report_last_report_10001_278:
      000897                        552 	.ds 32
      0008B7                        553 _send_keyboard_report_changed_10001_278:
      0008B7                        554 	.ds 1
      0008B8                        555 _add_mods_mods_10000_286:
      0008B8                        556 	.ds 1
      0008B9                        557 _del_mods_mods_10000_288:
      0008B9                        558 	.ds 1
      0008BA                        559 _add_weak_mods_mods_10000_296:
      0008BA                        560 	.ds 1
      0008BB                        561 _del_weak_mods_mods_10000_298:
      0008BB                        562 	.ds 1
                                    563 ;--------------------------------------------------------
                                    564 ; absolute external ram data
                                    565 ;--------------------------------------------------------
                                    566 	.area XABS    (ABS,XDATA)
                                    567 ;--------------------------------------------------------
                                    568 ; initialized external ram data
                                    569 ;--------------------------------------------------------
                                    570 	.area XISEG   (XDATA)
      000BAE                        571 _real_mods:
      000BAE                        572 	.ds 1
      000BAF                        573 _weak_mods:
      000BAF                        574 	.ds 1
      000BB0                        575 _actual_keyboard_report::
      000BB0                        576 	.ds 32
                                    577 	.area HOME    (CODE)
                                    578 	.area GSINIT0 (CODE)
                                    579 	.area GSINIT1 (CODE)
                                    580 	.area GSINIT2 (CODE)
                                    581 	.area GSINIT3 (CODE)
                                    582 	.area GSINIT4 (CODE)
                                    583 	.area GSINIT5 (CODE)
                                    584 	.area GSINIT  (CODE)
                                    585 	.area GSFINAL (CODE)
                                    586 	.area CSEG    (CODE)
                                    587 ;--------------------------------------------------------
                                    588 ; global & static initialisations
                                    589 ;--------------------------------------------------------
                                    590 	.area HOME    (CODE)
                                    591 	.area GSINIT  (CODE)
                                    592 	.area GSFINAL (CODE)
                                    593 	.area GSINIT  (CODE)
                                    594 ;--------------------------------------------------------
                                    595 ; Home
                                    596 ;--------------------------------------------------------
                                    597 	.area HOME    (CODE)
                                    598 	.area HOME    (CODE)
                                    599 ;--------------------------------------------------------
                                    600 ; code
                                    601 ;--------------------------------------------------------
                                    602 	.area CSEG    (CODE)
                                    603 ;------------------------------------------------------------
                                    604 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    605 ;------------------------------------------------------------
                                    606 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_40'
                                    607 ;------------------------------------------------------------
                                    608 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    609 ;	-----------------------------------------
                           000007   610 	ar7 = 0x07
                           000006   611 	ar6 = 0x06
                           000005   612 	ar5 = 0x05
                           000004   613 	ar4 = 0x04
                           000003   614 	ar3 = 0x03
                           000002   615 	ar2 = 0x02
                           000001   616 	ar1 = 0x01
                           000000   617 	ar0 = 0x00
                                    618 ;	 function send_keyboard_report
                                    619 ;	-----------------------------------------
      007809                        620 _send_keyboard_report:
                                    621 ;	quantum/action_util.c:251: keyboard_report->mods = real_mods;
      007809 90 0B AE         [24]  622 	mov	dptr,#_real_mods
      00780C E0               [24]  623 	movx	a,@dptr
      00780D FF               [12]  624 	mov	r7,a
      00780E 90 0B B0         [24]  625 	mov	dptr,#_actual_keyboard_report
      007811 F0               [24]  626 	movx	@dptr,a
                                    627 ;	quantum/action_util.c:252: keyboard_report->mods |= weak_mods;
      007812 90 0B AF         [24]  628 	mov	dptr,#_weak_mods
      007815 E0               [24]  629 	movx	a,@dptr
      007816 42 07            [12]  630 	orl	ar7,a
      007818 90 0B B0         [24]  631 	mov	dptr,#_actual_keyboard_report
      00781B EF               [12]  632 	mov	a,r7
      00781C F0               [24]  633 	movx	@dptr,a
                                    634 ;	quantum/action_util.c:282: bool changed = false;
      00781D 90 08 B7         [24]  635 	mov	dptr,#_send_keyboard_report_changed_10001_278
      007820 E4               [12]  636 	clr	a
      007821 F0               [24]  637 	movx	@dptr,a
                                    638 ;	quantum/action_util.c:284: uint8_t __xdata *dest = (uint8_t __xdata *)&last_report;
                                    639 ;	quantum/action_util.c:285: const uint8_t __xdata *src = (const uint8_t __xdata *)keyboard_report;
                                    640 ;	quantum/action_util.c:290: for (uint8_t i = 0; i < sizeof(report_keyboard_t); ++i) {
      007822 FF               [12]  641 	mov	r7,a
      007823                        642 00107$:
      007823 BF 20 00         [24]  643 	cjne	r7,#0x20,00140$
      007826                        644 00140$:
      007826 50 2F            [24]  645 	jnc	00103$
                                    646 ;	quantum/action_util.c:291: if (dest[i] != src[i]) {
      007828 EF               [12]  647 	mov	a,r7
      007829 24 97            [12]  648 	add	a, #_send_keyboard_report_last_report_10001_278
      00782B FD               [12]  649 	mov	r5,a
      00782C E4               [12]  650 	clr	a
      00782D 34 08            [12]  651 	addc	a, #(_send_keyboard_report_last_report_10001_278 >> 8)
      00782F FE               [12]  652 	mov	r6,a
      007830 8D 82            [24]  653 	mov	dpl,r5
      007832 8E 83            [24]  654 	mov	dph,r6
      007834 E0               [24]  655 	movx	a,@dptr
      007835 FC               [12]  656 	mov	r4,a
      007836 EF               [12]  657 	mov	a,r7
      007837 24 B0            [12]  658 	add	a, #_actual_keyboard_report
      007839 F5 82            [12]  659 	mov	dpl,a
      00783B E4               [12]  660 	clr	a
      00783C 34 0B            [12]  661 	addc	a, #(_actual_keyboard_report >> 8)
      00783E F5 83            [12]  662 	mov	dph,a
      007840 E0               [24]  663 	movx	a,@dptr
      007841 FB               [12]  664 	mov	r3,a
      007842 EC               [12]  665 	mov	a,r4
      007843 B5 03 02         [24]  666 	cjne	a,ar3,00142$
      007846 80 0C            [24]  667 	sjmp	00108$
      007848                        668 00142$:
                                    669 ;	quantum/action_util.c:292: dest[i] = src[i];
      007848 8D 82            [24]  670 	mov	dpl,r5
      00784A 8E 83            [24]  671 	mov	dph,r6
      00784C EB               [12]  672 	mov	a,r3
      00784D F0               [24]  673 	movx	@dptr,a
                                    674 ;	quantum/action_util.c:293: changed = true;
      00784E 90 08 B7         [24]  675 	mov	dptr,#_send_keyboard_report_changed_10001_278
      007851 74 01            [12]  676 	mov	a,#0x01
      007853 F0               [24]  677 	movx	@dptr,a
      007854                        678 00108$:
                                    679 ;	quantum/action_util.c:290: for (uint8_t i = 0; i < sizeof(report_keyboard_t); ++i) {
      007854 0F               [12]  680 	inc	r7
      007855 80 CC            [24]  681 	sjmp	00107$
      007857                        682 00103$:
                                    683 ;	quantum/action_util.c:296: if (changed) host_keyboard_send(keyboard_report);
      007857 90 08 B7         [24]  684 	mov	dptr,#_send_keyboard_report_changed_10001_278
      00785A E0               [24]  685 	movx	a,@dptr
      00785B 60 09            [24]  686 	jz	00109$
      00785D 90 0B B0         [24]  687 	mov	dptr,#_actual_keyboard_report
      007860 75 F0 00         [24]  688 	mov	b, #0x00
                                    689 ;	quantum/action_util.c:304: }
      007863 02 67 2A         [24]  690 	ljmp	_host_keyboard_send
      007866                        691 00109$:
      007866 22               [24]  692 	ret
                                    693 ;------------------------------------------------------------
                                    694 ;Allocation info for local variables in function 'get_mods'
                                    695 ;------------------------------------------------------------
                                    696 ;	quantum/action_util.c:310: uint8_t get_mods(void) {
                                    697 ;	-----------------------------------------
                                    698 ;	 function get_mods
                                    699 ;	-----------------------------------------
      007867                        700 _get_mods:
                                    701 ;	quantum/action_util.c:311: return real_mods;
      007867 90 0B AE         [24]  702 	mov	dptr,#_real_mods
      00786A E0               [24]  703 	movx	a,@dptr
      00786B F5 82            [12]  704 	mov	dpl,a
                                    705 ;	quantum/action_util.c:312: }
      00786D 22               [24]  706 	ret
                                    707 ;------------------------------------------------------------
                                    708 ;Allocation info for local variables in function 'add_mods'
                                    709 ;------------------------------------------------------------
                                    710 ;mods          Allocated with name '_add_mods_mods_10000_286'
                                    711 ;------------------------------------------------------------
                                    712 ;	quantum/action_util.c:317: void add_mods(uint8_t mods) {
                                    713 ;	-----------------------------------------
                                    714 ;	 function add_mods
                                    715 ;	-----------------------------------------
      00786E                        716 _add_mods:
      00786E E5 82            [12]  717 	mov	a,dpl
      007870 90 08 B8         [24]  718 	mov	dptr,#_add_mods_mods_10000_286
      007873 F0               [24]  719 	movx	@dptr,a
                                    720 ;	quantum/action_util.c:318: real_mods |= mods;
      007874 E0               [24]  721 	movx	a,@dptr
      007875 FF               [12]  722 	mov	r7,a
      007876 90 0B AE         [24]  723 	mov	dptr,#_real_mods
      007879 E0               [24]  724 	movx	a,@dptr
      00787A 4F               [12]  725 	orl	a,r7
      00787B F0               [24]  726 	movx	@dptr,a
                                    727 ;	quantum/action_util.c:319: }
      00787C 22               [24]  728 	ret
                                    729 ;------------------------------------------------------------
                                    730 ;Allocation info for local variables in function 'del_mods'
                                    731 ;------------------------------------------------------------
                                    732 ;mods          Allocated with name '_del_mods_mods_10000_288'
                                    733 ;------------------------------------------------------------
                                    734 ;	quantum/action_util.c:324: void del_mods(uint8_t mods) {
                                    735 ;	-----------------------------------------
                                    736 ;	 function del_mods
                                    737 ;	-----------------------------------------
      00787D                        738 _del_mods:
      00787D E5 82            [12]  739 	mov	a,dpl
      00787F 90 08 B9         [24]  740 	mov	dptr,#_del_mods_mods_10000_288
      007882 F0               [24]  741 	movx	@dptr,a
                                    742 ;	quantum/action_util.c:325: real_mods &= ~mods;
      007883 E0               [24]  743 	movx	a,@dptr
      007884 F4               [12]  744 	cpl	a
      007885 FF               [12]  745 	mov	r7,a
      007886 90 0B AE         [24]  746 	mov	dptr,#_real_mods
      007889 E0               [24]  747 	movx	a,@dptr
      00788A 5F               [12]  748 	anl	a,r7
      00788B F0               [24]  749 	movx	@dptr,a
                                    750 ;	quantum/action_util.c:326: }
      00788C 22               [24]  751 	ret
                                    752 ;------------------------------------------------------------
                                    753 ;Allocation info for local variables in function 'set_mods'
                                    754 ;------------------------------------------------------------
                                    755 ;mods          Allocated with name '_set_mods_mods_10000_290'
                                    756 ;------------------------------------------------------------
                                    757 ;	quantum/action_util.c:331: void set_mods(uint8_t mods) {
                                    758 ;	-----------------------------------------
                                    759 ;	 function clear_mods
                                    760 ;	-----------------------------------------
      00788D                        761 _clear_mods:
                                    762 ;	quantum/action_util.c:339: real_mods = 0;
      00788D 90 0B AE         [24]  763 	mov	dptr,#_real_mods
      007890 E4               [12]  764 	clr	a
      007891 F0               [24]  765 	movx	@dptr,a
                                    766 ;	quantum/action_util.c:340: }
      007892 22               [24]  767 	ret
                                    768 ;------------------------------------------------------------
                                    769 ;Allocation info for local variables in function 'get_weak_mods'
                                    770 ;------------------------------------------------------------
                                    771 ;	quantum/action_util.c:346: uint8_t get_weak_mods(void) {
                                    772 ;	-----------------------------------------
                                    773 ;	 function get_weak_mods
                                    774 ;	-----------------------------------------
      007893                        775 _get_weak_mods:
                                    776 ;	quantum/action_util.c:347: return weak_mods;
      007893 90 0B AF         [24]  777 	mov	dptr,#_weak_mods
      007896 E0               [24]  778 	movx	a,@dptr
      007897 F5 82            [12]  779 	mov	dpl,a
                                    780 ;	quantum/action_util.c:348: }
      007899 22               [24]  781 	ret
                                    782 ;------------------------------------------------------------
                                    783 ;Allocation info for local variables in function 'add_weak_mods'
                                    784 ;------------------------------------------------------------
                                    785 ;mods          Allocated with name '_add_weak_mods_mods_10000_296'
                                    786 ;------------------------------------------------------------
                                    787 ;	quantum/action_util.c:353: void add_weak_mods(uint8_t mods) {
                                    788 ;	-----------------------------------------
                                    789 ;	 function add_weak_mods
                                    790 ;	-----------------------------------------
      00789A                        791 _add_weak_mods:
      00789A E5 82            [12]  792 	mov	a,dpl
      00789C 90 08 BA         [24]  793 	mov	dptr,#_add_weak_mods_mods_10000_296
      00789F F0               [24]  794 	movx	@dptr,a
                                    795 ;	quantum/action_util.c:354: weak_mods |= mods;
      0078A0 E0               [24]  796 	movx	a,@dptr
      0078A1 FF               [12]  797 	mov	r7,a
      0078A2 90 0B AF         [24]  798 	mov	dptr,#_weak_mods
      0078A5 E0               [24]  799 	movx	a,@dptr
      0078A6 4F               [12]  800 	orl	a,r7
      0078A7 F0               [24]  801 	movx	@dptr,a
                                    802 ;	quantum/action_util.c:355: }
      0078A8 22               [24]  803 	ret
                                    804 ;------------------------------------------------------------
                                    805 ;Allocation info for local variables in function 'del_weak_mods'
                                    806 ;------------------------------------------------------------
                                    807 ;mods          Allocated with name '_del_weak_mods_mods_10000_298'
                                    808 ;------------------------------------------------------------
                                    809 ;	quantum/action_util.c:360: void del_weak_mods(uint8_t mods) {
                                    810 ;	-----------------------------------------
                                    811 ;	 function del_weak_mods
                                    812 ;	-----------------------------------------
      0078A9                        813 _del_weak_mods:
      0078A9 E5 82            [12]  814 	mov	a,dpl
      0078AB 90 08 BB         [24]  815 	mov	dptr,#_del_weak_mods_mods_10000_298
      0078AE F0               [24]  816 	movx	@dptr,a
                                    817 ;	quantum/action_util.c:361: weak_mods &= ~mods;
      0078AF E0               [24]  818 	movx	a,@dptr
      0078B0 F4               [12]  819 	cpl	a
      0078B1 FF               [12]  820 	mov	r7,a
      0078B2 90 0B AF         [24]  821 	mov	dptr,#_weak_mods
      0078B5 E0               [24]  822 	movx	a,@dptr
      0078B6 5F               [12]  823 	anl	a,r7
      0078B7 F0               [24]  824 	movx	@dptr,a
                                    825 ;	quantum/action_util.c:362: }
      0078B8 22               [24]  826 	ret
                                    827 ;------------------------------------------------------------
                                    828 ;Allocation info for local variables in function 'set_weak_mods'
                                    829 ;------------------------------------------------------------
                                    830 ;mods          Allocated with name '_set_weak_mods_mods_10000_300'
                                    831 ;------------------------------------------------------------
                                    832 ;	quantum/action_util.c:367: void set_weak_mods(uint8_t mods) {
                                    833 ;	-----------------------------------------
                                    834 ;	 function clear_weak_mods
                                    835 ;	-----------------------------------------
      0078B9                        836 _clear_weak_mods:
                                    837 ;	quantum/action_util.c:375: weak_mods = 0;
      0078B9 90 0B AF         [24]  838 	mov	dptr,#_weak_mods
      0078BC E4               [12]  839 	clr	a
      0078BD F0               [24]  840 	movx	@dptr,a
                                    841 ;	quantum/action_util.c:376: }
      0078BE 22               [24]  842 	ret
                                    843 ;------------------------------------------------------------
                                    844 ;Allocation info for local variables in function 'oneshot_locked_mods_changed_user'
                                    845 ;------------------------------------------------------------
                                    846 ;mods          Allocated with name '_oneshot_locked_mods_changed_user_mods_10000_304'
                                    847 ;------------------------------------------------------------
                                    848 ;	quantum/action_util.c:458: __attribute__((weak)) void oneshot_locked_mods_changed_user(uint8_t mods) {}
                                    849 ;	-----------------------------------------
                                    850 	.area CSEG    (CODE)
                                    851 	.area CONST   (CODE)
                                    852 	.area XINIT   (CODE)
      00BD6D                        853 __xinit__real_mods:
      00BD6D 00                     854 	.db #0x00	; 0
      00BD6E                        855 __xinit__weak_mods:
      00BD6E 00                     856 	.db #0x00	; 0
      00BD6F                        857 __xinit__actual_keyboard_report:
      00BD6F 00                     858 	.db #0x00	; 0
      00BD70 00                     859 	.db #0x00	; 0
      00BD71 00                     860 	.db #0x00	; 0
      00BD72 00                     861 	.db #0x00	; 0
      00BD73 00                     862 	.db #0x00	; 0
      00BD74 00                     863 	.db #0x00	; 0
      00BD75 00                     864 	.db #0x00	; 0
      00BD76 00                     865 	.db #0x00	; 0
      00BD77 00                     866 	.db 0x00
      00BD78 00                     867 	.db 0x00
      00BD79 00                     868 	.db 0x00
      00BD7A 00                     869 	.db 0x00
      00BD7B 00                     870 	.db 0x00
      00BD7C 00                     871 	.db 0x00
      00BD7D 00                     872 	.db 0x00
      00BD7E 00                     873 	.db 0x00
      00BD7F 00                     874 	.db 0x00
      00BD80 00                     875 	.db 0x00
      00BD81 00                     876 	.db 0x00
      00BD82 00                     877 	.db 0x00
      00BD83 00                     878 	.db 0x00
      00BD84 00                     879 	.db 0x00
      00BD85 00                     880 	.db 0x00
      00BD86 00                     881 	.db 0x00
      00BD87 00                     882 	.db 0x00
      00BD88 00                     883 	.db 0x00
      00BD89 00                     884 	.db 0x00
      00BD8A 00                     885 	.db 0x00
      00BD8B 00                     886 	.db 0x00
      00BD8C 00                     887 	.db 0x00
      00BD8D 00                     888 	.db 0x00
      00BD8E 00                     889 	.db 0x00
                                    890 	.area CABS    (ABS,CODE)
