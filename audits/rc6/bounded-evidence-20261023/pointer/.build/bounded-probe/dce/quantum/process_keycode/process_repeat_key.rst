                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module process_repeat_key
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _get_weak_mods
                                     12 	.globl _get_mods
                                     13 	.globl _alt_repeat_key_invoke
                                     14 	.globl _repeat_key_invoke
                                     15 	.globl _get_repeat_key_count
                                     16 	.globl _set_last_record
                                     17 	.globl _set_last_mods
                                     18 	.globl _ADC_START
                                     19 	.globl _S0_R_FIFO
                                     20 	.globl _S0_T_FIFO
                                     21 	.globl _S0_FREE
                                     22 	.globl _S0_IF_BYTE
                                     23 	.globl _S0_IF_FIRST
                                     24 	.globl _S0_IF_OV
                                     25 	.globl _S0_FST_ACT
                                     26 	.globl _CP_RL2
                                     27 	.globl _C_T2
                                     28 	.globl _TR2
                                     29 	.globl _EXEN2
                                     30 	.globl _TCLK
                                     31 	.globl _RCLK
                                     32 	.globl _EXF2
                                     33 	.globl _CAP1F
                                     34 	.globl _TF2
                                     35 	.globl _RI
                                     36 	.globl _TI
                                     37 	.globl _RB8
                                     38 	.globl _TB8
                                     39 	.globl _REN
                                     40 	.globl _SM2
                                     41 	.globl _SM1
                                     42 	.globl _SM0
                                     43 	.globl _IT0
                                     44 	.globl _IE0
                                     45 	.globl _IT1
                                     46 	.globl _IE1
                                     47 	.globl _TR0
                                     48 	.globl _TF0
                                     49 	.globl _TR1
                                     50 	.globl _TF1
                                     51 	.globl _P4_0
                                     52 	.globl _P4_1
                                     53 	.globl _P4_2
                                     54 	.globl _P4_3
                                     55 	.globl _P4_4
                                     56 	.globl _P4_5
                                     57 	.globl _P4_6
                                     58 	.globl _RXD
                                     59 	.globl _TXD
                                     60 	.globl _INT0
                                     61 	.globl _INT1
                                     62 	.globl _T0
                                     63 	.globl _T1
                                     64 	.globl _MOSI1
                                     65 	.globl _MISO1
                                     66 	.globl _SCK1
                                     67 	.globl _P3_0
                                     68 	.globl _P3_1
                                     69 	.globl _P3_2
                                     70 	.globl _P3_3
                                     71 	.globl _P3_4
                                     72 	.globl _P3_5
                                     73 	.globl _P3_6
                                     74 	.globl _P3_7
                                     75 	.globl _CAP1_
                                     76 	.globl _T2_
                                     77 	.globl _CAP2_
                                     78 	.globl _T2EX_
                                     79 	.globl _RXD1
                                     80 	.globl _TXD1
                                     81 	.globl _P2_0
                                     82 	.globl _P2_1
                                     83 	.globl _P2_2
                                     84 	.globl _P2_3
                                     85 	.globl _P2_4
                                     86 	.globl _P2_5
                                     87 	.globl _P2_6
                                     88 	.globl _P2_7
                                     89 	.globl _AIN0
                                     90 	.globl _AIN1
                                     91 	.globl _AIN2
                                     92 	.globl _AIN3
                                     93 	.globl _AIN4
                                     94 	.globl _AIN5
                                     95 	.globl _AIN6
                                     96 	.globl _AIN7
                                     97 	.globl _CAP1
                                     98 	.globl _T2
                                     99 	.globl _CAP2
                                    100 	.globl _T2EX
                                    101 	.globl _INT0_
                                    102 	.globl _SCS
                                    103 	.globl _MOSI
                                    104 	.globl _MISO
                                    105 	.globl _SCK
                                    106 	.globl _RXD1_
                                    107 	.globl _TXD1_
                                    108 	.globl _P1_0
                                    109 	.globl _P1_1
                                    110 	.globl _P1_2
                                    111 	.globl _P1_3
                                    112 	.globl _P1_4
                                    113 	.globl _P1_5
                                    114 	.globl _P1_6
                                    115 	.globl _P1_7
                                    116 	.globl _AIN8
                                    117 	.globl _AIN9
                                    118 	.globl _AIN10
                                    119 	.globl _AIN11
                                    120 	.globl _AIN12
                                    121 	.globl _AIN13
                                    122 	.globl _RXD_
                                    123 	.globl _TXD_
                                    124 	.globl _SCL0
                                    125 	.globl _SDA0
                                    126 	.globl _P0_0
                                    127 	.globl _P0_1
                                    128 	.globl _P0_2
                                    129 	.globl _P0_3
                                    130 	.globl _P0_4
                                    131 	.globl _P0_5
                                    132 	.globl _P0_6
                                    133 	.globl _P0_7
                                    134 	.globl _IE_SPI0
                                    135 	.globl _IE_USB
                                    136 	.globl _IE_ADC
                                    137 	.globl _IE_UART1
                                    138 	.globl _IE_PWM_I2C
                                    139 	.globl _IE_GPIO
                                    140 	.globl _IE_WDOG
                                    141 	.globl _PX0
                                    142 	.globl _PT0
                                    143 	.globl _PX1
                                    144 	.globl _PT1
                                    145 	.globl _PS
                                    146 	.globl _PT2
                                    147 	.globl _PL_FLAG
                                    148 	.globl _PH_FLAG
                                    149 	.globl _EX0
                                    150 	.globl _ET0
                                    151 	.globl _EX1
                                    152 	.globl _ET1
                                    153 	.globl _ES
                                    154 	.globl _ET2
                                    155 	.globl _E_DIS
                                    156 	.globl _EA
                                    157 	.globl _P
                                    158 	.globl _F1
                                    159 	.globl _OV
                                    160 	.globl _RS0
                                    161 	.globl _RS1
                                    162 	.globl _F0
                                    163 	.globl _AC
                                    164 	.globl _CY
                                    165 	.globl _I2CS_INT_ST
                                    166 	.globl _I2CX_INT
                                    167 	.globl _LED_STATUS
                                    168 	.globl _LED_DMA_H
                                    169 	.globl _LED_DMA_L
                                    170 	.globl _LED_DMA
                                    171 	.globl _LED_PWM_OE
                                    172 	.globl _LED_COMMON
                                    173 	.globl _ADC_CHAN
                                    174 	.globl _ADC_DAT_H
                                    175 	.globl _ADC_DAT_L
                                    176 	.globl _ADC_DAT
                                    177 	.globl _ADC_CTRL
                                    178 	.globl _SPI1_CK_SE
                                    179 	.globl _SPI1_CTRL
                                    180 	.globl _SPI1_DATA
                                    181 	.globl _SPI1_STAT
                                    182 	.globl _SIF1
                                    183 	.globl _SBAUD1
                                    184 	.globl _SBUF1
                                    185 	.globl _SCON1
                                    186 	.globl _SPI0_SETUP
                                    187 	.globl _SPI0_CK_SE
                                    188 	.globl _SPI0_CTRL
                                    189 	.globl _SPI0_DATA
                                    190 	.globl _SPI0_STAT
                                    191 	.globl _T2CAP1H
                                    192 	.globl _T2CAP1L
                                    193 	.globl _T2CAP1
                                    194 	.globl _TH2
                                    195 	.globl _TL2
                                    196 	.globl _T2COUNT
                                    197 	.globl _RCAP2H
                                    198 	.globl _RCAP2L
                                    199 	.globl _RCAP2
                                    200 	.globl _T2MOD
                                    201 	.globl _T2CON
                                    202 	.globl _SBUF
                                    203 	.globl _SCON
                                    204 	.globl _TH1
                                    205 	.globl _TH0
                                    206 	.globl _TL1
                                    207 	.globl _TL0
                                    208 	.globl _TMOD
                                    209 	.globl _TCON
                                    210 	.globl _XBUS_AUX
                                    211 	.globl _P7
                                    212 	.globl _P6_DIR
                                    213 	.globl _P6_OUT_PU
                                    214 	.globl _P6_IN
                                    215 	.globl _P5_DIR
                                    216 	.globl _P5_OUT_PU
                                    217 	.globl _P5_IN
                                    218 	.globl _P4_LED_KEY
                                    219 	.globl _P4_DIR_PU
                                    220 	.globl _P4_MOD_OC
                                    221 	.globl _P4
                                    222 	.globl _P3_DIR_PU
                                    223 	.globl _P3_MOD_OC
                                    224 	.globl _P3
                                    225 	.globl _P2_DIR_PU
                                    226 	.globl _P2_MOD_OC
                                    227 	.globl _P2
                                    228 	.globl _P1_DIR_PU
                                    229 	.globl _P1_MOD_OC
                                    230 	.globl _P1
                                    231 	.globl _P0_DIR_PU
                                    232 	.globl _P0_MOD_OC
                                    233 	.globl _P0
                                    234 	.globl _ROM_CTRL
                                    235 	.globl _ROM_DATA_HH
                                    236 	.globl _ROM_DATA_HL
                                    237 	.globl _ROM_DATA_HI
                                    238 	.globl _ROM_ADDR_H
                                    239 	.globl _ROM_ADDR_L
                                    240 	.globl _ROM_ADDR
                                    241 	.globl _GPIO_IE
                                    242 	.globl _IP_EX
                                    243 	.globl _IE_EX
                                    244 	.globl _IP
                                    245 	.globl _IE
                                    246 	.globl _WDOG_COUNT
                                    247 	.globl _RESET_KEEP
                                    248 	.globl _WAKE_CTRL
                                    249 	.globl _CLOCK_CFG
                                    250 	.globl _POWER_CFG
                                    251 	.globl _PCON
                                    252 	.globl _GLOBAL_CFG
                                    253 	.globl _SAFE_MOD
                                    254 	.globl _DPH
                                    255 	.globl _DPL
                                    256 	.globl _SP
                                    257 	.globl _A_INV
                                    258 	.globl _B
                                    259 	.globl _ACC
                                    260 	.globl _PSW
                                    261 	.globl _process_repeat_key_PARM_2
                                    262 	.globl _process_last_key_PARM_2
                                    263 	.globl _remember_last_key_user_PARM_3
                                    264 	.globl _remember_last_key_user_PARM_2
                                    265 	.globl _remember_last_key_user
                                    266 	.globl _process_last_key
                                    267 	.globl _process_repeat_key
                                    268 ;--------------------------------------------------------
                                    269 ; special function registers
                                    270 ;--------------------------------------------------------
                                    271 	.area RSEG    (ABS,DATA)
      000000                        272 	.org 0x0000
                           0000D0   273 _PSW	=	0x00d0
                           0000E0   274 _ACC	=	0x00e0
                           0000F0   275 _B	=	0x00f0
                           0000FD   276 _A_INV	=	0x00fd
                           000081   277 _SP	=	0x0081
                           000082   278 _DPL	=	0x0082
                           000083   279 _DPH	=	0x0083
                           0000A1   280 _SAFE_MOD	=	0x00a1
                           0000B1   281 _GLOBAL_CFG	=	0x00b1
                           000087   282 _PCON	=	0x0087
                           0000BA   283 _POWER_CFG	=	0x00ba
                           0000B9   284 _CLOCK_CFG	=	0x00b9
                           0000A9   285 _WAKE_CTRL	=	0x00a9
                           0000FE   286 _RESET_KEEP	=	0x00fe
                           0000FF   287 _WDOG_COUNT	=	0x00ff
                           0000A8   288 _IE	=	0x00a8
                           0000B8   289 _IP	=	0x00b8
                           0000E8   290 _IE_EX	=	0x00e8
                           0000E9   291 _IP_EX	=	0x00e9
                           0000B2   292 _GPIO_IE	=	0x00b2
                           008584   293 _ROM_ADDR	=	0x8584
                           000084   294 _ROM_ADDR_L	=	0x0084
                           000085   295 _ROM_ADDR_H	=	0x0085
                           008F8E   296 _ROM_DATA_HI	=	0x8f8e
                           00008E   297 _ROM_DATA_HL	=	0x008e
                           00008F   298 _ROM_DATA_HH	=	0x008f
                           000086   299 _ROM_CTRL	=	0x0086
                           000080   300 _P0	=	0x0080
                           0000C4   301 _P0_MOD_OC	=	0x00c4
                           0000C5   302 _P0_DIR_PU	=	0x00c5
                           000090   303 _P1	=	0x0090
                           000092   304 _P1_MOD_OC	=	0x0092
                           000093   305 _P1_DIR_PU	=	0x0093
                           0000A0   306 _P2	=	0x00a0
                           000094   307 _P2_MOD_OC	=	0x0094
                           000095   308 _P2_DIR_PU	=	0x0095
                           0000B0   309 _P3	=	0x00b0
                           000096   310 _P3_MOD_OC	=	0x0096
                           000097   311 _P3_DIR_PU	=	0x0097
                           0000C0   312 _P4	=	0x00c0
                           0000C2   313 _P4_MOD_OC	=	0x00c2
                           0000C3   314 _P4_DIR_PU	=	0x00c3
                           0000C1   315 _P4_LED_KEY	=	0x00c1
                           0000AA   316 _P5_IN	=	0x00aa
                           0000AB   317 _P5_OUT_PU	=	0x00ab
                           0000AC   318 _P5_DIR	=	0x00ac
                           0000AD   319 _P6_IN	=	0x00ad
                           0000AE   320 _P6_OUT_PU	=	0x00ae
                           0000AF   321 _P6_DIR	=	0x00af
                           0000F1   322 _P7	=	0x00f1
                           0000A2   323 _XBUS_AUX	=	0x00a2
                           000088   324 _TCON	=	0x0088
                           000089   325 _TMOD	=	0x0089
                           00008A   326 _TL0	=	0x008a
                           00008B   327 _TL1	=	0x008b
                           00008C   328 _TH0	=	0x008c
                           00008D   329 _TH1	=	0x008d
                           000098   330 _SCON	=	0x0098
                           000099   331 _SBUF	=	0x0099
                           0000C8   332 _T2CON	=	0x00c8
                           0000C9   333 _T2MOD	=	0x00c9
                           00CBCA   334 _RCAP2	=	0xcbca
                           0000CA   335 _RCAP2L	=	0x00ca
                           0000CB   336 _RCAP2H	=	0x00cb
                           00CDCC   337 _T2COUNT	=	0xcdcc
                           0000CC   338 _TL2	=	0x00cc
                           0000CD   339 _TH2	=	0x00cd
                           00CFCE   340 _T2CAP1	=	0xcfce
                           0000CE   341 _T2CAP1L	=	0x00ce
                           0000CF   342 _T2CAP1H	=	0x00cf
                           0000F8   343 _SPI0_STAT	=	0x00f8
                           0000F9   344 _SPI0_DATA	=	0x00f9
                           0000FA   345 _SPI0_CTRL	=	0x00fa
                           0000FB   346 _SPI0_CK_SE	=	0x00fb
                           0000FC   347 _SPI0_SETUP	=	0x00fc
                           0000BC   348 _SCON1	=	0x00bc
                           0000BD   349 _SBUF1	=	0x00bd
                           0000BE   350 _SBAUD1	=	0x00be
                           0000BF   351 _SIF1	=	0x00bf
                           0000B4   352 _SPI1_STAT	=	0x00b4
                           0000B5   353 _SPI1_DATA	=	0x00b5
                           0000B6   354 _SPI1_CTRL	=	0x00b6
                           0000B7   355 _SPI1_CK_SE	=	0x00b7
                           0000F3   356 _ADC_CTRL	=	0x00f3
                           00F5F4   357 _ADC_DAT	=	0xf5f4
                           0000F4   358 _ADC_DAT_L	=	0x00f4
                           0000F5   359 _ADC_DAT_H	=	0x00f5
                           0000F6   360 _ADC_CHAN	=	0x00f6
                           0000A6   361 _LED_COMMON	=	0x00a6
                           0000A7   362 _LED_PWM_OE	=	0x00a7
                           00C7C6   363 _LED_DMA	=	0xc7c6
                           0000C6   364 _LED_DMA_L	=	0x00c6
                           0000C7   365 _LED_DMA_H	=	0x00c7
                           0000F7   366 _LED_STATUS	=	0x00f7
                           0000B3   367 _I2CX_INT	=	0x00b3
                           0000BB   368 _I2CS_INT_ST	=	0x00bb
                                    369 ;--------------------------------------------------------
                                    370 ; special function bits
                                    371 ;--------------------------------------------------------
                                    372 	.area RSEG    (ABS,DATA)
      000000                        373 	.org 0x0000
                           0000D7   374 _CY	=	0x00d7
                           0000D6   375 _AC	=	0x00d6
                           0000D5   376 _F0	=	0x00d5
                           0000D4   377 _RS1	=	0x00d4
                           0000D3   378 _RS0	=	0x00d3
                           0000D2   379 _OV	=	0x00d2
                           0000D1   380 _F1	=	0x00d1
                           0000D0   381 _P	=	0x00d0
                           0000AF   382 _EA	=	0x00af
                           0000AE   383 _E_DIS	=	0x00ae
                           0000AD   384 _ET2	=	0x00ad
                           0000AC   385 _ES	=	0x00ac
                           0000AB   386 _ET1	=	0x00ab
                           0000AA   387 _EX1	=	0x00aa
                           0000A9   388 _ET0	=	0x00a9
                           0000A8   389 _EX0	=	0x00a8
                           0000BF   390 _PH_FLAG	=	0x00bf
                           0000BE   391 _PL_FLAG	=	0x00be
                           0000BD   392 _PT2	=	0x00bd
                           0000BC   393 _PS	=	0x00bc
                           0000BB   394 _PT1	=	0x00bb
                           0000BA   395 _PX1	=	0x00ba
                           0000B9   396 _PT0	=	0x00b9
                           0000B8   397 _PX0	=	0x00b8
                           0000EF   398 _IE_WDOG	=	0x00ef
                           0000EE   399 _IE_GPIO	=	0x00ee
                           0000ED   400 _IE_PWM_I2C	=	0x00ed
                           0000EC   401 _IE_UART1	=	0x00ec
                           0000EB   402 _IE_ADC	=	0x00eb
                           0000E9   403 _IE_USB	=	0x00e9
                           0000E8   404 _IE_SPI0	=	0x00e8
                           000087   405 _P0_7	=	0x0087
                           000086   406 _P0_6	=	0x0086
                           000085   407 _P0_5	=	0x0085
                           000084   408 _P0_4	=	0x0084
                           000083   409 _P0_3	=	0x0083
                           000082   410 _P0_2	=	0x0082
                           000081   411 _P0_1	=	0x0081
                           000080   412 _P0_0	=	0x0080
                           000081   413 _SDA0	=	0x0081
                           000080   414 _SCL0	=	0x0080
                           000083   415 _TXD_	=	0x0083
                           000082   416 _RXD_	=	0x0082
                           000085   417 _AIN13	=	0x0085
                           000084   418 _AIN12	=	0x0084
                           000083   419 _AIN11	=	0x0083
                           000082   420 _AIN10	=	0x0082
                           000081   421 _AIN9	=	0x0081
                           000080   422 _AIN8	=	0x0080
                           000097   423 _P1_7	=	0x0097
                           000096   424 _P1_6	=	0x0096
                           000095   425 _P1_5	=	0x0095
                           000094   426 _P1_4	=	0x0094
                           000093   427 _P1_3	=	0x0093
                           000092   428 _P1_2	=	0x0092
                           000091   429 _P1_1	=	0x0091
                           000090   430 _P1_0	=	0x0090
                           000097   431 _TXD1_	=	0x0097
                           000096   432 _RXD1_	=	0x0096
                           000097   433 _SCK	=	0x0097
                           000096   434 _MISO	=	0x0096
                           000095   435 _MOSI	=	0x0095
                           000094   436 _SCS	=	0x0094
                           000092   437 _INT0_	=	0x0092
                           000091   438 _T2EX	=	0x0091
                           000091   439 _CAP2	=	0x0091
                           000090   440 _T2	=	0x0090
                           000090   441 _CAP1	=	0x0090
                           000097   442 _AIN7	=	0x0097
                           000096   443 _AIN6	=	0x0096
                           000095   444 _AIN5	=	0x0095
                           000094   445 _AIN4	=	0x0094
                           000093   446 _AIN3	=	0x0093
                           000092   447 _AIN2	=	0x0092
                           000091   448 _AIN1	=	0x0091
                           000090   449 _AIN0	=	0x0090
                           0000A7   450 _P2_7	=	0x00a7
                           0000A6   451 _P2_6	=	0x00a6
                           0000A5   452 _P2_5	=	0x00a5
                           0000A4   453 _P2_4	=	0x00a4
                           0000A3   454 _P2_3	=	0x00a3
                           0000A2   455 _P2_2	=	0x00a2
                           0000A1   456 _P2_1	=	0x00a1
                           0000A0   457 _P2_0	=	0x00a0
                           0000A7   458 _TXD1	=	0x00a7
                           0000A6   459 _RXD1	=	0x00a6
                           0000A5   460 _T2EX_	=	0x00a5
                           0000A5   461 _CAP2_	=	0x00a5
                           0000A4   462 _T2_	=	0x00a4
                           0000A4   463 _CAP1_	=	0x00a4
                           0000B7   464 _P3_7	=	0x00b7
                           0000B6   465 _P3_6	=	0x00b6
                           0000B5   466 _P3_5	=	0x00b5
                           0000B4   467 _P3_4	=	0x00b4
                           0000B3   468 _P3_3	=	0x00b3
                           0000B2   469 _P3_2	=	0x00b2
                           0000B1   470 _P3_1	=	0x00b1
                           0000B0   471 _P3_0	=	0x00b0
                           0000B7   472 _SCK1	=	0x00b7
                           0000B6   473 _MISO1	=	0x00b6
                           0000B5   474 _MOSI1	=	0x00b5
                           0000B5   475 _T1	=	0x00b5
                           0000B4   476 _T0	=	0x00b4
                           0000B3   477 _INT1	=	0x00b3
                           0000B2   478 _INT0	=	0x00b2
                           0000B1   479 _TXD	=	0x00b1
                           0000B0   480 _RXD	=	0x00b0
                           0000C6   481 _P4_6	=	0x00c6
                           0000C5   482 _P4_5	=	0x00c5
                           0000C4   483 _P4_4	=	0x00c4
                           0000C3   484 _P4_3	=	0x00c3
                           0000C2   485 _P4_2	=	0x00c2
                           0000C1   486 _P4_1	=	0x00c1
                           0000C0   487 _P4_0	=	0x00c0
                           00008F   488 _TF1	=	0x008f
                           00008E   489 _TR1	=	0x008e
                           00008D   490 _TF0	=	0x008d
                           00008C   491 _TR0	=	0x008c
                           00008B   492 _IE1	=	0x008b
                           00008A   493 _IT1	=	0x008a
                           000089   494 _IE0	=	0x0089
                           000088   495 _IT0	=	0x0088
                           00009F   496 _SM0	=	0x009f
                           00009E   497 _SM1	=	0x009e
                           00009D   498 _SM2	=	0x009d
                           00009C   499 _REN	=	0x009c
                           00009B   500 _TB8	=	0x009b
                           00009A   501 _RB8	=	0x009a
                           000099   502 _TI	=	0x0099
                           000098   503 _RI	=	0x0098
                           0000CF   504 _TF2	=	0x00cf
                           0000CF   505 _CAP1F	=	0x00cf
                           0000CE   506 _EXF2	=	0x00ce
                           0000CD   507 _RCLK	=	0x00cd
                           0000CC   508 _TCLK	=	0x00cc
                           0000CB   509 _EXEN2	=	0x00cb
                           0000CA   510 _TR2	=	0x00ca
                           0000C9   511 _C_T2	=	0x00c9
                           0000C8   512 _CP_RL2	=	0x00c8
                           0000FF   513 _S0_FST_ACT	=	0x00ff
                           0000FE   514 _S0_IF_OV	=	0x00fe
                           0000FD   515 _S0_IF_FIRST	=	0x00fd
                           0000FC   516 _S0_IF_BYTE	=	0x00fc
                           0000FB   517 _S0_FREE	=	0x00fb
                           0000FA   518 _S0_T_FIFO	=	0x00fa
                           0000F8   519 _S0_R_FIFO	=	0x00f8
                           0000F7   520 _ADC_START	=	0x00f7
                                    521 ;--------------------------------------------------------
                                    522 ; overlayable register banks
                                    523 ;--------------------------------------------------------
                                    524 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        525 	.ds 8
                                    526 ;--------------------------------------------------------
                                    527 ; internal ram data
                                    528 ;--------------------------------------------------------
                                    529 	.area DSEG    (DATA)
                                    530 ;--------------------------------------------------------
                                    531 ; overlayable items in internal ram
                                    532 ;--------------------------------------------------------
                                    533 ;--------------------------------------------------------
                                    534 ; indirectly addressable internal ram data
                                    535 ;--------------------------------------------------------
                                    536 	.area ISEG    (DATA)
                                    537 ;--------------------------------------------------------
                                    538 ; absolute internal ram data
                                    539 ;--------------------------------------------------------
                                    540 	.area IABS    (ABS,DATA)
                                    541 	.area IABS    (ABS,DATA)
                                    542 ;--------------------------------------------------------
                                    543 ; bit data
                                    544 ;--------------------------------------------------------
                                    545 	.area BSEG    (BIT)
                                    546 ;--------------------------------------------------------
                                    547 ; paged external ram data
                                    548 ;--------------------------------------------------------
                                    549 	.area PSEG    (PAG,XDATA)
                                    550 ;--------------------------------------------------------
                                    551 ; uninitialized external ram data
                                    552 ;--------------------------------------------------------
                                    553 	.area XSEG    (XDATA)
      0009AB                        554 _remember_last_key_user_PARM_2:
      0009AB                        555 	.ds 3
      0009AE                        556 _remember_last_key_user_PARM_3:
      0009AE                        557 	.ds 3
      0009B1                        558 _remember_last_key_PARM_2:
      0009B1                        559 	.ds 3
      0009B4                        560 _remember_last_key_PARM_3:
      0009B4                        561 	.ds 3
      0009B7                        562 _remember_last_key_keycode_10000_228:
      0009B7                        563 	.ds 2
      0009B9                        564 _process_last_key_PARM_2:
      0009B9                        565 	.ds 3
      0009BC                        566 _process_last_key_keycode_10000_231:
      0009BC                        567 	.ds 2
      0009BE                        568 _process_last_key_remembered_mods_30000_236:
      0009BE                        569 	.ds 1
      0009BF                        570 _process_repeat_key_PARM_2:
      0009BF                        571 	.ds 3
      0009C2                        572 _process_repeat_key_keycode_10000_239:
      0009C2                        573 	.ds 2
                                    574 ;--------------------------------------------------------
                                    575 ; absolute external ram data
                                    576 ;--------------------------------------------------------
                                    577 	.area XABS    (ABS,XDATA)
                                    578 ;--------------------------------------------------------
                                    579 ; initialized external ram data
                                    580 ;--------------------------------------------------------
                                    581 	.area XISEG   (XDATA)
                                    582 	.area HOME    (CODE)
                                    583 	.area GSINIT0 (CODE)
                                    584 	.area GSINIT1 (CODE)
                                    585 	.area GSINIT2 (CODE)
                                    586 	.area GSINIT3 (CODE)
                                    587 	.area GSINIT4 (CODE)
                                    588 	.area GSINIT5 (CODE)
                                    589 	.area GSINIT  (CODE)
                                    590 	.area GSFINAL (CODE)
                                    591 	.area CSEG    (CODE)
                                    592 ;--------------------------------------------------------
                                    593 ; global & static initialisations
                                    594 ;--------------------------------------------------------
                                    595 	.area HOME    (CODE)
                                    596 	.area GSINIT  (CODE)
                                    597 	.area GSFINAL (CODE)
                                    598 	.area GSINIT  (CODE)
                                    599 ;--------------------------------------------------------
                                    600 ; Home
                                    601 ;--------------------------------------------------------
                                    602 	.area HOME    (CODE)
                                    603 	.area HOME    (CODE)
                                    604 ;--------------------------------------------------------
                                    605 ; code
                                    606 ;--------------------------------------------------------
                                    607 	.area CSEG    (CODE)
                                    608 ;------------------------------------------------------------
                                    609 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    610 ;------------------------------------------------------------
                                    611 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_164'
                                    612 ;------------------------------------------------------------
                                    613 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    614 ;	-----------------------------------------
                           000007   615 	ar7 = 0x07
                           000006   616 	ar6 = 0x06
                           000005   617 	ar5 = 0x05
                           000004   618 	ar4 = 0x04
                           000003   619 	ar3 = 0x03
                           000002   620 	ar2 = 0x02
                           000001   621 	ar1 = 0x01
                           000000   622 	ar0 = 0x00
                                    623 ;	 function remember_last_key_user
                                    624 ;	-----------------------------------------
      0093C3                        625 _remember_last_key_user:
                                    626 ;	quantum/process_keycode/process_repeat_key.c:23: return true;
      0093C3 75 82 01         [24]  627 	mov	dpl, #0x01
                                    628 ;	quantum/process_keycode/process_repeat_key.c:24: }
      0093C6 22               [24]  629 	ret
                                    630 ;------------------------------------------------------------
                                    631 ;Allocation info for local variables in function 'remember_last_key'
                                    632 ;------------------------------------------------------------
                                    633 ;record        Allocated with name '_remember_last_key_PARM_2'
                                    634 ;remembered_mods Allocated with name '_remember_last_key_PARM_3'
                                    635 ;keycode       Allocated with name '_remember_last_key_keycode_10000_228'
                                    636 ;------------------------------------------------------------
                                    637 ;	quantum/process_keycode/process_repeat_key.c:26: static bool remember_last_key(uint16_t keycode, keyrecord_t* record, uint8_t* remembered_mods) {
                                    638 ;	-----------------------------------------
                                    639 ;	 function remember_last_key
                                    640 ;	-----------------------------------------
      0093C7                        641 _remember_last_key:
      0093C7 AF 83            [24]  642 	mov	r7,dph
      0093C9 E5 82            [12]  643 	mov	a,dpl
      0093CB 90 09 B7         [24]  644 	mov	dptr,#_remember_last_key_keycode_10000_228
      0093CE F0               [24]  645 	movx	@dptr,a
      0093CF EF               [12]  646 	mov	a,r7
      0093D0 A3               [24]  647 	inc	dptr
      0093D1 F0               [24]  648 	movx	@dptr,a
                                    649 ;	quantum/process_keycode/process_repeat_key.c:29: if (keycode == KC_NO || keycode == KC_TRANSPARENT ||
      0093D2 90 09 B7         [24]  650 	mov	dptr,#_remember_last_key_keycode_10000_228
      0093D5 E0               [24]  651 	movx	a,@dptr
      0093D6 FE               [12]  652 	mov	r6,a
      0093D7 A3               [24]  653 	inc	dptr
      0093D8 E0               [24]  654 	movx	a,@dptr
      0093D9 FF               [12]  655 	mov	r7,a
      0093DA 90 09 B7         [24]  656 	mov	dptr,#_remember_last_key_keycode_10000_228
      0093DD E0               [24]  657 	movx	a,@dptr
      0093DE F5 F0            [12]  658 	mov	b,a
      0093E0 A3               [24]  659 	inc	dptr
      0093E1 E0               [24]  660 	movx	a,@dptr
      0093E2 45 F0            [12]  661 	orl	a,b
      0093E4 70 03            [24]  662 	jnz	00224$
      0093E6 02 94 A3         [24]  663 	ljmp	00101$
      0093E9                        664 00224$:
      0093E9 BE 01 06         [24]  665 	cjne	r6,#0x01,00225$
      0093EC BF 00 03         [24]  666 	cjne	r7,#0x00,00225$
      0093EF 02 94 A3         [24]  667 	ljmp	00101$
      0093F2                        668 00225$:
                                    669 ;	quantum/process_keycode/process_repeat_key.c:30: (keycode >= QK_MOMENTARY && keycode <= QK_MOMENTARY_MAX) ||
      0093F2 C3               [12]  670 	clr	c
      0093F3 EE               [12]  671 	mov	a,r6
      0093F4 94 20            [12]  672 	subb	a,#0x20
      0093F6 EF               [12]  673 	mov	a,r7
      0093F7 94 52            [12]  674 	subb	a,#0x52
      0093F9 40 0B            [24]  675 	jc	00107$
      0093FB 74 3F            [12]  676 	mov	a,#0x3f
      0093FD 9E               [12]  677 	subb	a,r6
      0093FE 74 52            [12]  678 	mov	a,#0x52
      009400 9F               [12]  679 	subb	a,r7
      009401 40 03            [24]  680 	jc	00227$
      009403 02 94 A3         [24]  681 	ljmp	00101$
      009406                        682 00227$:
                                    683 ;	free result
      009406                        684 00107$:
                                    685 ;	quantum/process_keycode/process_repeat_key.c:31: (keycode >= QK_LAYER_MOD && keycode <= QK_LAYER_MOD_MAX) ||
      009406 90 09 B7         [24]  686 	mov	dptr,#_remember_last_key_keycode_10000_228
      009409 E0               [24]  687 	movx	a,@dptr
      00940A FE               [12]  688 	mov	r6,a
      00940B A3               [24]  689 	inc	dptr
      00940C E0               [24]  690 	movx	a,@dptr
      00940D FF               [12]  691 	mov	r7,a
      00940E C3               [12]  692 	clr	c
      00940F 94 50            [12]  693 	subb	a,#0x50
      009411 40 0B            [24]  694 	jc	00109$
      009413 74 FF            [12]  695 	mov	a,#0xff
      009415 9E               [12]  696 	subb	a,r6
      009416 74 51            [12]  697 	mov	a,#0x51
      009418 9F               [12]  698 	subb	a,r7
      009419 40 03            [24]  699 	jc	00229$
      00941B 02 94 A3         [24]  700 	ljmp	00101$
      00941E                        701 00229$:
                                    702 ;	free result
      00941E                        703 00109$:
                                    704 ;	quantum/process_keycode/process_repeat_key.c:32: (keycode >= QK_DEF_LAYER && keycode <= QK_DEF_LAYER_MAX) ||
      00941E C3               [12]  705 	clr	c
      00941F EE               [12]  706 	mov	a,r6
      009420 94 40            [12]  707 	subb	a,#0x40
      009422 EF               [12]  708 	mov	a,r7
      009423 94 52            [12]  709 	subb	a,#0x52
      009425 40 08            [24]  710 	jc	00111$
      009427 74 5F            [12]  711 	mov	a,#0x5f
      009429 9E               [12]  712 	subb	a,r6
      00942A 74 52            [12]  713 	mov	a,#0x52
      00942C 9F               [12]  714 	subb	a,r7
      00942D 50 74            [24]  715 	jnc	00101$
                                    716 ;	free result
      00942F                        717 00111$:
                                    718 ;	quantum/process_keycode/process_repeat_key.c:33: (keycode >= QK_TO && keycode <= QK_TO_MAX) ||
      00942F 74 AE            [12]  719 	mov	a,#0x100 - 0x52
      009431 2F               [12]  720 	add	a,r7
      009432 50 09            [24]  721 	jnc	00113$
      009434 C3               [12]  722 	clr	c
      009435 74 1F            [12]  723 	mov	a,#0x1f
      009437 9E               [12]  724 	subb	a,r6
      009438 74 52            [12]  725 	mov	a,#0x52
      00943A 9F               [12]  726 	subb	a,r7
      00943B 50 66            [24]  727 	jnc	00101$
                                    728 ;	free result
      00943D                        729 00113$:
                                    730 ;	quantum/process_keycode/process_repeat_key.c:34: (keycode >= QK_TOGGLE_LAYER && keycode <= QK_TOGGLE_LAYER_MAX) ||
      00943D C3               [12]  731 	clr	c
      00943E EE               [12]  732 	mov	a,r6
      00943F 94 60            [12]  733 	subb	a,#0x60
      009441 EF               [12]  734 	mov	a,r7
      009442 94 52            [12]  735 	subb	a,#0x52
      009444 40 08            [24]  736 	jc	00115$
      009446 74 7F            [12]  737 	mov	a,#0x7f
      009448 9E               [12]  738 	subb	a,r6
      009449 74 52            [12]  739 	mov	a,#0x52
      00944B 9F               [12]  740 	subb	a,r7
      00944C 50 55            [24]  741 	jnc	00101$
                                    742 ;	free result
      00944E                        743 00115$:
                                    744 ;	quantum/process_keycode/process_repeat_key.c:35: (keycode >= QK_LAYER_TAP_TOGGLE && keycode <= QK_LAYER_TAP_TOGGLE_MAX) ||
      00944E C3               [12]  745 	clr	c
      00944F EE               [12]  746 	mov	a,r6
      009450 94 C0            [12]  747 	subb	a,#0xc0
      009452 EF               [12]  748 	mov	a,r7
      009453 94 52            [12]  749 	subb	a,#0x52
      009455 40 08            [24]  750 	jc	00117$
      009457 74 DF            [12]  751 	mov	a,#0xdf
      009459 9E               [12]  752 	subb	a,r6
      00945A 74 52            [12]  753 	mov	a,#0x52
      00945C 9F               [12]  754 	subb	a,r7
      00945D 50 44            [24]  755 	jnc	00101$
                                    756 ;	free result
      00945F                        757 00117$:
                                    758 ;	quantum/process_keycode/process_repeat_key.c:36: (keycode >= KC_LCTL && keycode <= KC_RGUI) ||
      00945F C3               [12]  759 	clr	c
      009460 EE               [12]  760 	mov	a,r6
      009461 94 E0            [12]  761 	subb	a,#0xe0
      009463 EF               [12]  762 	mov	a,r7
      009464 94 00            [12]  763 	subb	a,#0x00
      009466 40 07            [24]  764 	jc	00118$
      009468 74 E7            [12]  765 	mov	a,#0xe7
      00946A 9E               [12]  766 	subb	a,r6
      00946B E4               [12]  767 	clr	a
      00946C 9F               [12]  768 	subb	a,r7
      00946D 50 34            [24]  769 	jnc	00101$
                                    770 ;	free result
      00946F                        771 00118$:
                                    772 ;	quantum/process_keycode/process_repeat_key.c:37: keycode == KC_HYPR || keycode == KC_MEH || keycode == QK_REPEAT_KEY
      00946F 90 09 B7         [24]  773 	mov	dptr,#_remember_last_key_keycode_10000_228
      009472 12 86 05         [24]  774 	lcall	_ak820_outline_0012
      009475 BC 00 05         [24]  775 	cjne	r4,#0x00,00240$
      009478 BD 0F 02         [24]  776 	cjne	r5,#0x0f,00240$
      00947B 80 26            [24]  777 	sjmp	00101$
      00947D                        778 00240$:
      00947D BC 00 05         [24]  779 	cjne	r4,#0x00,00241$
      009480 BD 07 02         [24]  780 	cjne	r5,#0x07,00241$
      009483 80 1E            [24]  781 	sjmp	00101$
      009485                        782 00241$:
                                    783 ;	quantum/process_keycode/process_repeat_key.c:39: || keycode == QK_ALT_REPEAT_KEY
      009485 BC 79 05         [24]  784 	cjne	r4,#0x79,00242$
      009488 BD 7C 02         [24]  785 	cjne	r5,#0x7c,00242$
      00948B 80 16            [24]  786 	sjmp	00101$
      00948D                        787 00242$:
                                    788 ;	quantum/process_keycode/process_repeat_key.c:46: || keycode == QK_TRI_LAYER_LOWER || keycode == QK_TRI_LAYER_UPPER
      00948D BC 7A 05         [24]  789 	cjne	r4,#0x7a,00243$
      009490 BD 7C 02         [24]  790 	cjne	r5,#0x7c,00243$
      009493 80 0E            [24]  791 	sjmp	00101$
      009495                        792 00243$:
      009495 BC 77 05         [24]  793 	cjne	r4,#0x77,00244$
      009498 BD 7C 02         [24]  794 	cjne	r5,#0x7c,00244$
      00949B 80 06            [24]  795 	sjmp	00101$
      00949D                        796 00244$:
                                    797 ;	quantum/process_keycode/process_repeat_key.c:48: ) return false;
      00949D BC 78 07         [24]  798 	cjne	r4,#0x78,00102$
      0094A0 BD 7C 04         [24]  799 	cjne	r5,#0x7c,00102$
      0094A3                        800 00101$:
      0094A3 75 82 00         [24]  801 	mov	dpl, #0x00
      0094A6 22               [24]  802 	ret
      0094A7                        803 00102$:
                                    804 ;	quantum/process_keycode/process_repeat_key.c:61: return remember_last_key_user(keycode, record, remembered_mods);
      0094A7 90 09 B1         [24]  805 	mov	dptr,#_remember_last_key_PARM_2
      0094AA 12 95 AD         [24]  806 	lcall	_ak820_outline_0004
      0094AD 90 09 B4         [24]  807 	mov	dptr,#_remember_last_key_PARM_3
      0094B0 E0               [24]  808 	movx	a,@dptr
      0094B1 F8               [12]  809 	mov	r0,a
      0094B2 A3               [24]  810 	inc	dptr
      0094B3 E0               [24]  811 	movx	a,@dptr
      0094B4 F9               [12]  812 	mov	r1,a
      0094B5 A3               [24]  813 	inc	dptr
      0094B6 E0               [24]  814 	movx	a,@dptr
      0094B7 FA               [12]  815 	mov	r2,a
      0094B8 90 09 AB         [24]  816 	mov	dptr,#_remember_last_key_user_PARM_2
      0094BB EB               [12]  817 	mov	a,r3
      0094BC F0               [24]  818 	movx	@dptr,a
      0094BD EC               [12]  819 	mov	a,r4
      0094BE A3               [24]  820 	inc	dptr
      0094BF F0               [24]  821 	movx	@dptr,a
      0094C0 ED               [12]  822 	mov	a,r5
      0094C1 A3               [24]  823 	inc	dptr
      0094C2 F0               [24]  824 	movx	@dptr,a
      0094C3 90 09 AE         [24]  825 	mov	dptr,#_remember_last_key_user_PARM_3
      0094C6 E8               [12]  826 	mov	a,r0
      0094C7 F0               [24]  827 	movx	@dptr,a
      0094C8 E9               [12]  828 	mov	a,r1
      0094C9 A3               [24]  829 	inc	dptr
      0094CA F0               [24]  830 	movx	@dptr,a
      0094CB EA               [12]  831 	mov	a,r2
      0094CC A3               [24]  832 	inc	dptr
      0094CD F0               [24]  833 	movx	@dptr,a
      0094CE 8E 82            [24]  834 	mov	dpl, r6
      0094D0 8F 83            [24]  835 	mov	dph, r7
                                    836 ;	quantum/process_keycode/process_repeat_key.c:62: }
      0094D2 02 93 C3         [24]  837 	ljmp	_remember_last_key_user
                                    838 ;------------------------------------------------------------
                                    839 ;Allocation info for local variables in function 'process_last_key'
                                    840 ;------------------------------------------------------------
                                    841 ;record        Allocated with name '_process_last_key_PARM_2'
                                    842 ;keycode       Allocated with name '_process_last_key_keycode_10000_231'
                                    843 ;remembered_mods Allocated with name '_process_last_key_remembered_mods_30000_236'
                                    844 ;------------------------------------------------------------
                                    845 ;	quantum/process_keycode/process_repeat_key.c:64: bool process_last_key(uint16_t keycode, keyrecord_t* record) {
                                    846 ;	-----------------------------------------
                                    847 ;	 function process_last_key
                                    848 ;	-----------------------------------------
      0094D5                        849 _process_last_key:
      0094D5 AF 83            [24]  850 	mov	r7,dph
      0094D7 E5 82            [12]  851 	mov	a,dpl
      0094D9 90 09 BC         [24]  852 	mov	dptr,#_process_last_key_keycode_10000_231
      0094DC F0               [24]  853 	movx	@dptr,a
      0094DD EF               [12]  854 	mov	a,r7
      0094DE A3               [24]  855 	inc	dptr
      0094DF F0               [24]  856 	movx	@dptr,a
                                    857 ;	quantum/process_keycode/process_repeat_key.c:65: if (get_repeat_key_count()) {
      0094E0 12 9C 57         [24]  858 	lcall	_get_repeat_key_count
      0094E3 E5 82            [12]  859 	mov	a, dpl
      0094E5 60 04            [24]  860 	jz	00102$
                                    861 ;	quantum/process_keycode/process_repeat_key.c:66: return true;
      0094E7 75 82 01         [24]  862 	mov	dpl, #0x01
      0094EA 22               [24]  863 	ret
      0094EB                        864 00102$:
                                    865 ;	quantum/process_keycode/process_repeat_key.c:69: if (record->event.pressed) {
      0094EB 90 09 B9         [24]  866 	mov	dptr,#_process_last_key_PARM_2
      0094EE 12 73 99         [24]  867 	lcall	_ak820_outline_0002
      0094F1 74 05            [12]  868 	mov	a,#0x05
      0094F3 12 73 A2         [24]  869 	lcall	_ak820_outline_0009
      0094F6 12 B5 78         [24]  870 	lcall	__gptrget
      0094F9 60 5A            [24]  871 	jz	00106$
                                    872 ;	quantum/process_keycode/process_repeat_key.c:70: uint8_t remembered_mods = get_mods() | get_weak_mods();
      0094FB 12 78 67         [24]  873 	lcall	_get_mods
      0094FE AC 82            [24]  874 	mov	r4, dpl
      009500 12 78 93         [24]  875 	lcall	_get_weak_mods
      009503 AB 82            [24]  876 	mov	r3, dpl
      009505 90 09 BE         [24]  877 	mov	dptr,#_process_last_key_remembered_mods_30000_236
      009508 EB               [12]  878 	mov	a,r3
      009509 4C               [12]  879 	orl	a,r4
      00950A F0               [24]  880 	movx	@dptr,a
                                    881 ;	quantum/process_keycode/process_repeat_key.c:75: if (remember_last_key(keycode, record, &remembered_mods)) {
      00950B 90 09 BC         [24]  882 	mov	dptr,#_process_last_key_keycode_10000_231
      00950E E0               [24]  883 	movx	a,@dptr
      00950F FB               [12]  884 	mov	r3,a
      009510 A3               [24]  885 	inc	dptr
      009511 E0               [24]  886 	movx	a,@dptr
      009512 FC               [12]  887 	mov	r4,a
      009513 90 09 B1         [24]  888 	mov	dptr,#_remember_last_key_PARM_2
      009516 12 73 BA         [24]  889 	lcall	_ak820_outline_0015
      009519 90 09 B4         [24]  890 	mov	dptr,#_remember_last_key_PARM_3
      00951C 74 BE            [12]  891 	mov	a,#_process_last_key_remembered_mods_30000_236
      00951E F0               [24]  892 	movx	@dptr,a
      00951F 74 09            [12]  893 	mov	a,#(_process_last_key_remembered_mods_30000_236 >> 8)
      009521 A3               [24]  894 	inc	dptr
      009522 F0               [24]  895 	movx	@dptr,a
      009523 E4               [12]  896 	clr	a
      009524 A3               [24]  897 	inc	dptr
      009525 F0               [24]  898 	movx	@dptr,a
      009526 8B 82            [24]  899 	mov	dpl, r3
      009528 8C 83            [24]  900 	mov	dph, r4
      00952A C0 04            [24]  901 	push	ar4
      00952C C0 03            [24]  902 	push	ar3
      00952E 12 93 C7         [24]  903 	lcall	_remember_last_key
      009531 E5 82            [12]  904 	mov	a, dpl
      009533 D0 03            [24]  905 	pop	ar3
      009535 D0 04            [24]  906 	pop	ar4
      009537 60 1C            [24]  907 	jz	00106$
                                    908 ;	quantum/process_keycode/process_repeat_key.c:76: set_last_record(keycode, record);
      009539 90 09 B9         [24]  909 	mov	dptr,#_process_last_key_PARM_2
      00953C 12 73 99         [24]  910 	lcall	_ak820_outline_0002
      00953F 90 0A 29         [24]  911 	mov	dptr,#_set_last_record_PARM_2
      009542 12 73 BA         [24]  912 	lcall	_ak820_outline_0015
      009545 8B 82            [24]  913 	mov	dpl, r3
      009547 8C 83            [24]  914 	mov	dph, r4
      009549 12 9B D0         [24]  915 	lcall	_set_last_record
                                    916 ;	quantum/process_keycode/process_repeat_key.c:77: set_last_mods(remembered_mods);
      00954C 90 09 BE         [24]  917 	mov	dptr,#_process_last_key_remembered_mods_30000_236
      00954F E0               [24]  918 	movx	a,@dptr
      009550 F5 82            [12]  919 	mov	dpl,a
      009552 12 9B C4         [24]  920 	lcall	_set_last_mods
      009555                        921 00106$:
                                    922 ;	quantum/process_keycode/process_repeat_key.c:81: return true;
      009555 75 82 01         [24]  923 	mov	dpl, #0x01
                                    924 ;	quantum/process_keycode/process_repeat_key.c:82: }
      009558 22               [24]  925 	ret
                                    926 ;------------------------------------------------------------
                                    927 ;Allocation info for local variables in function 'process_repeat_key'
                                    928 ;------------------------------------------------------------
                                    929 ;record        Allocated with name '_process_repeat_key_PARM_2'
                                    930 ;keycode       Allocated with name '_process_repeat_key_keycode_10000_239'
                                    931 ;------------------------------------------------------------
                                    932 ;	quantum/process_keycode/process_repeat_key.c:84: bool process_repeat_key(uint16_t keycode, keyrecord_t* record) {
                                    933 ;	-----------------------------------------
                                    934 ;	 function process_repeat_key
                                    935 ;	-----------------------------------------
      009559                        936 _process_repeat_key:
      009559 AF 83            [24]  937 	mov	r7,dph
      00955B E5 82            [12]  938 	mov	a,dpl
      00955D 90 09 C2         [24]  939 	mov	dptr,#_process_repeat_key_keycode_10000_239
      009560 F0               [24]  940 	movx	@dptr,a
      009561 EF               [12]  941 	mov	a,r7
      009562 A3               [24]  942 	inc	dptr
      009563 F0               [24]  943 	movx	@dptr,a
                                    944 ;	quantum/process_keycode/process_repeat_key.c:85: if (get_repeat_key_count()) {
      009564 12 9C 57         [24]  945 	lcall	_get_repeat_key_count
      009567 E5 82            [12]  946 	mov	a, dpl
      009569 60 04            [24]  947 	jz	00102$
                                    948 ;	quantum/process_keycode/process_repeat_key.c:86: return true;
      00956B 75 82 01         [24]  949 	mov	dpl, #0x01
      00956E 22               [24]  950 	ret
      00956F                        951 00102$:
                                    952 ;	quantum/process_keycode/process_repeat_key.c:89: if (keycode == QK_REPEAT_KEY) {
      00956F 90 09 C2         [24]  953 	mov	dptr,#_process_repeat_key_keycode_10000_239
      009572 E0               [24]  954 	movx	a,@dptr
      009573 FE               [12]  955 	mov	r6,a
      009574 A3               [24]  956 	inc	dptr
      009575 E0               [24]  957 	movx	a,@dptr
      009576 FF               [12]  958 	mov	r7,a
      009577 BE 79 16         [24]  959 	cjne	r6,#0x79,00106$
      00957A BF 7C 13         [24]  960 	cjne	r7,#0x7c,00106$
                                    961 ;	quantum/process_keycode/process_repeat_key.c:90: repeat_key_invoke(&record->event);
      00957D 90 09 BF         [24]  962 	mov	dptr,#_process_repeat_key_PARM_2
      009580 12 95 AD         [24]  963 	lcall	_ak820_outline_0004
      009583 8B 82            [24]  964 	mov	dpl, r3
      009585 8C 83            [24]  965 	mov	dph, r4
      009587 8D F0            [24]  966 	mov	b, r5
      009589 12 9D 85         [24]  967 	lcall	_repeat_key_invoke
                                    968 ;	quantum/process_keycode/process_repeat_key.c:91: return false;
      00958C 75 82 00         [24]  969 	mov	dpl, #0x00
      00958F 22               [24]  970 	ret
      009590                        971 00106$:
                                    972 ;	quantum/process_keycode/process_repeat_key.c:93: } else if (keycode == QK_ALT_REPEAT_KEY) {
      009590 BE 7A 16         [24]  973 	cjne	r6,#0x7a,00107$
      009593 BF 7C 13         [24]  974 	cjne	r7,#0x7c,00107$
                                    975 ;	quantum/process_keycode/process_repeat_key.c:94: alt_repeat_key_invoke(&record->event);
      009596 90 09 BF         [24]  976 	mov	dptr,#_process_repeat_key_PARM_2
      009599 12 73 99         [24]  977 	lcall	_ak820_outline_0002
      00959C 8D 82            [24]  978 	mov	dpl, r5
      00959E 8E 83            [24]  979 	mov	dph, r6
      0095A0 8F F0            [24]  980 	mov	b, r7
      0095A2 12 9F 4A         [24]  981 	lcall	_alt_repeat_key_invoke
                                    982 ;	quantum/process_keycode/process_repeat_key.c:95: return false;
      0095A5 75 82 00         [24]  983 	mov	dpl, #0x00
      0095A8 22               [24]  984 	ret
      0095A9                        985 00107$:
                                    986 ;	quantum/process_keycode/process_repeat_key.c:99: return true;
      0095A9 75 82 01         [24]  987 	mov	dpl, #0x01
                                    988 ;	quantum/process_keycode/process_repeat_key.c:100: }
      0095AC 22               [24]  989 	ret
                                    990 	.area CSEG    (CODE)
                                    991 	.area CONST   (CODE)
                                    992 	.area XINIT   (CODE)
                                    993 	.area CABS    (ABS,CODE)
                                    994 
                                    995 ; Experimental exact instruction outlining.
                                    996 	.globl _ak820_outline_0002
                                    997 	.globl _ak820_outline_0004
                                    998 	.globl _ak820_outline_0009
                                    999 	.globl _ak820_outline_0012
                                   1000 	.globl _ak820_outline_0015
                                   1001 
                                   1002 	.area CSEG (CODE)
                                   1003 ; function ak820_outline_0004
      0095AD                       1004 _ak820_outline_0004:
      0095AD E0               [24] 1005 	movx	a,@dptr
      0095AE FB               [12] 1006 	mov	r3,a
      0095AF A3               [24] 1007 	inc	dptr
      0095B0 E0               [24] 1008 	movx	a,@dptr
      0095B1 FC               [12] 1009 	mov	r4,a
      0095B2 A3               [24] 1010 	inc	dptr
      0095B3 E0               [24] 1011 	movx	a,@dptr
      0095B4 FD               [12] 1012 	mov	r5,a
      0095B5 22               [24] 1013 	ret
