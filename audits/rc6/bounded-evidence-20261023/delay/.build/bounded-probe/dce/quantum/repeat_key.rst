                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module repeat_key
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _unregister_weak_mods
                                     12 	.globl _register_weak_mods
                                     13 	.globl _process_record
                                     14 	.globl _memset
                                     15 	.globl _ADC_START
                                     16 	.globl _S0_R_FIFO
                                     17 	.globl _S0_T_FIFO
                                     18 	.globl _S0_FREE
                                     19 	.globl _S0_IF_BYTE
                                     20 	.globl _S0_IF_FIRST
                                     21 	.globl _S0_IF_OV
                                     22 	.globl _S0_FST_ACT
                                     23 	.globl _CP_RL2
                                     24 	.globl _C_T2
                                     25 	.globl _TR2
                                     26 	.globl _EXEN2
                                     27 	.globl _TCLK
                                     28 	.globl _RCLK
                                     29 	.globl _EXF2
                                     30 	.globl _CAP1F
                                     31 	.globl _TF2
                                     32 	.globl _RI
                                     33 	.globl _TI
                                     34 	.globl _RB8
                                     35 	.globl _TB8
                                     36 	.globl _REN
                                     37 	.globl _SM2
                                     38 	.globl _SM1
                                     39 	.globl _SM0
                                     40 	.globl _IT0
                                     41 	.globl _IE0
                                     42 	.globl _IT1
                                     43 	.globl _IE1
                                     44 	.globl _TR0
                                     45 	.globl _TF0
                                     46 	.globl _TR1
                                     47 	.globl _TF1
                                     48 	.globl _P4_0
                                     49 	.globl _P4_1
                                     50 	.globl _P4_2
                                     51 	.globl _P4_3
                                     52 	.globl _P4_4
                                     53 	.globl _P4_5
                                     54 	.globl _P4_6
                                     55 	.globl _RXD
                                     56 	.globl _TXD
                                     57 	.globl _INT0
                                     58 	.globl _INT1
                                     59 	.globl _T0
                                     60 	.globl _T1
                                     61 	.globl _MOSI1
                                     62 	.globl _MISO1
                                     63 	.globl _SCK1
                                     64 	.globl _P3_0
                                     65 	.globl _P3_1
                                     66 	.globl _P3_2
                                     67 	.globl _P3_3
                                     68 	.globl _P3_4
                                     69 	.globl _P3_5
                                     70 	.globl _P3_6
                                     71 	.globl _P3_7
                                     72 	.globl _CAP1_
                                     73 	.globl _T2_
                                     74 	.globl _CAP2_
                                     75 	.globl _T2EX_
                                     76 	.globl _RXD1
                                     77 	.globl _TXD1
                                     78 	.globl _P2_0
                                     79 	.globl _P2_1
                                     80 	.globl _P2_2
                                     81 	.globl _P2_3
                                     82 	.globl _P2_4
                                     83 	.globl _P2_5
                                     84 	.globl _P2_6
                                     85 	.globl _P2_7
                                     86 	.globl _AIN0
                                     87 	.globl _AIN1
                                     88 	.globl _AIN2
                                     89 	.globl _AIN3
                                     90 	.globl _AIN4
                                     91 	.globl _AIN5
                                     92 	.globl _AIN6
                                     93 	.globl _AIN7
                                     94 	.globl _CAP1
                                     95 	.globl _T2
                                     96 	.globl _CAP2
                                     97 	.globl _T2EX
                                     98 	.globl _INT0_
                                     99 	.globl _SCS
                                    100 	.globl _MOSI
                                    101 	.globl _MISO
                                    102 	.globl _SCK
                                    103 	.globl _RXD1_
                                    104 	.globl _TXD1_
                                    105 	.globl _P1_0
                                    106 	.globl _P1_1
                                    107 	.globl _P1_2
                                    108 	.globl _P1_3
                                    109 	.globl _P1_4
                                    110 	.globl _P1_5
                                    111 	.globl _P1_6
                                    112 	.globl _P1_7
                                    113 	.globl _AIN8
                                    114 	.globl _AIN9
                                    115 	.globl _AIN10
                                    116 	.globl _AIN11
                                    117 	.globl _AIN12
                                    118 	.globl _AIN13
                                    119 	.globl _RXD_
                                    120 	.globl _TXD_
                                    121 	.globl _SCL0
                                    122 	.globl _SDA0
                                    123 	.globl _P0_0
                                    124 	.globl _P0_1
                                    125 	.globl _P0_2
                                    126 	.globl _P0_3
                                    127 	.globl _P0_4
                                    128 	.globl _P0_5
                                    129 	.globl _P0_6
                                    130 	.globl _P0_7
                                    131 	.globl _IE_SPI0
                                    132 	.globl _IE_USB
                                    133 	.globl _IE_ADC
                                    134 	.globl _IE_UART1
                                    135 	.globl _IE_PWM_I2C
                                    136 	.globl _IE_GPIO
                                    137 	.globl _IE_WDOG
                                    138 	.globl _PX0
                                    139 	.globl _PT0
                                    140 	.globl _PX1
                                    141 	.globl _PT1
                                    142 	.globl _PS
                                    143 	.globl _PT2
                                    144 	.globl _PL_FLAG
                                    145 	.globl _PH_FLAG
                                    146 	.globl _EX0
                                    147 	.globl _ET0
                                    148 	.globl _EX1
                                    149 	.globl _ET1
                                    150 	.globl _ES
                                    151 	.globl _ET2
                                    152 	.globl _E_DIS
                                    153 	.globl _EA
                                    154 	.globl _P
                                    155 	.globl _F1
                                    156 	.globl _OV
                                    157 	.globl _RS0
                                    158 	.globl _RS1
                                    159 	.globl _F0
                                    160 	.globl _AC
                                    161 	.globl _CY
                                    162 	.globl _I2CS_INT_ST
                                    163 	.globl _I2CX_INT
                                    164 	.globl _LED_STATUS
                                    165 	.globl _LED_DMA_H
                                    166 	.globl _LED_DMA_L
                                    167 	.globl _LED_DMA
                                    168 	.globl _LED_PWM_OE
                                    169 	.globl _LED_COMMON
                                    170 	.globl _ADC_CHAN
                                    171 	.globl _ADC_DAT_H
                                    172 	.globl _ADC_DAT_L
                                    173 	.globl _ADC_DAT
                                    174 	.globl _ADC_CTRL
                                    175 	.globl _SPI1_CK_SE
                                    176 	.globl _SPI1_CTRL
                                    177 	.globl _SPI1_DATA
                                    178 	.globl _SPI1_STAT
                                    179 	.globl _SIF1
                                    180 	.globl _SBAUD1
                                    181 	.globl _SBUF1
                                    182 	.globl _SCON1
                                    183 	.globl _SPI0_SETUP
                                    184 	.globl _SPI0_CK_SE
                                    185 	.globl _SPI0_CTRL
                                    186 	.globl _SPI0_DATA
                                    187 	.globl _SPI0_STAT
                                    188 	.globl _T2CAP1H
                                    189 	.globl _T2CAP1L
                                    190 	.globl _T2CAP1
                                    191 	.globl _TH2
                                    192 	.globl _TL2
                                    193 	.globl _T2COUNT
                                    194 	.globl _RCAP2H
                                    195 	.globl _RCAP2L
                                    196 	.globl _RCAP2
                                    197 	.globl _T2MOD
                                    198 	.globl _T2CON
                                    199 	.globl _SBUF
                                    200 	.globl _SCON
                                    201 	.globl _TH1
                                    202 	.globl _TH0
                                    203 	.globl _TL1
                                    204 	.globl _TL0
                                    205 	.globl _TMOD
                                    206 	.globl _TCON
                                    207 	.globl _XBUS_AUX
                                    208 	.globl _P7
                                    209 	.globl _P6_DIR
                                    210 	.globl _P6_OUT_PU
                                    211 	.globl _P6_IN
                                    212 	.globl _P5_DIR
                                    213 	.globl _P5_OUT_PU
                                    214 	.globl _P5_IN
                                    215 	.globl _P4_LED_KEY
                                    216 	.globl _P4_DIR_PU
                                    217 	.globl _P4_MOD_OC
                                    218 	.globl _P4
                                    219 	.globl _P3_DIR_PU
                                    220 	.globl _P3_MOD_OC
                                    221 	.globl _P3
                                    222 	.globl _P2_DIR_PU
                                    223 	.globl _P2_MOD_OC
                                    224 	.globl _P2
                                    225 	.globl _P1_DIR_PU
                                    226 	.globl _P1_MOD_OC
                                    227 	.globl _P1
                                    228 	.globl _P0_DIR_PU
                                    229 	.globl _P0_MOD_OC
                                    230 	.globl _P0
                                    231 	.globl _ROM_CTRL
                                    232 	.globl _ROM_DATA_HH
                                    233 	.globl _ROM_DATA_HL
                                    234 	.globl _ROM_DATA_HI
                                    235 	.globl _ROM_ADDR_H
                                    236 	.globl _ROM_ADDR_L
                                    237 	.globl _ROM_ADDR
                                    238 	.globl _GPIO_IE
                                    239 	.globl _IP_EX
                                    240 	.globl _IE_EX
                                    241 	.globl _IP
                                    242 	.globl _IE
                                    243 	.globl _WDOG_COUNT
                                    244 	.globl _RESET_KEEP
                                    245 	.globl _WAKE_CTRL
                                    246 	.globl _CLOCK_CFG
                                    247 	.globl _POWER_CFG
                                    248 	.globl _PCON
                                    249 	.globl _GLOBAL_CFG
                                    250 	.globl _SAFE_MOD
                                    251 	.globl _DPH
                                    252 	.globl _DPL
                                    253 	.globl _SP
                                    254 	.globl _A_INV
                                    255 	.globl _B
                                    256 	.globl _ACC
                                    257 	.globl _PSW
                                    258 	.globl _get_alt_repeat_key_keycode_user_PARM_2
                                    259 	.globl _set_last_record_PARM_2
                                    260 	.globl _repeat_key_cancel
                                    261 	.globl _set_last_mods
                                    262 	.globl _set_last_record
                                    263 	.globl _get_repeat_key_count
                                    264 	.globl _repeat_key_invoke
                                    265 	.globl _get_alt_repeat_key_keycode
                                    266 	.globl _alt_repeat_key_invoke
                                    267 	.globl _get_alt_repeat_key_keycode_user
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
                                    533 	.area	OSEG    (OVR,DATA)
      00005D                        534 _find_alt_keycode_sloc0_1_0:
      00005D                        535 	.ds 3
                                    536 ;--------------------------------------------------------
                                    537 ; indirectly addressable internal ram data
                                    538 ;--------------------------------------------------------
                                    539 	.area ISEG    (DATA)
                                    540 ;--------------------------------------------------------
                                    541 ; absolute internal ram data
                                    542 ;--------------------------------------------------------
                                    543 	.area IABS    (ABS,DATA)
                                    544 	.area IABS    (ABS,DATA)
                                    545 ;--------------------------------------------------------
                                    546 ; bit data
                                    547 ;--------------------------------------------------------
                                    548 	.area BSEG    (BIT)
                                    549 ;--------------------------------------------------------
                                    550 ; paged external ram data
                                    551 ;--------------------------------------------------------
                                    552 	.area PSEG    (PAG,XDATA)
                                    553 ;--------------------------------------------------------
                                    554 ; uninitialized external ram data
                                    555 ;--------------------------------------------------------
                                    556 	.area XSEG    (XDATA)
      000A17                        557 _last_record:
      000A17                        558 	.ds 8
      000A1F                        559 _registered_record:
      000A1F                        560 	.ds 8
      000A27                        561 _registered_repeat_count:
      000A27                        562 	.ds 1
      000A28                        563 _registered_mods:
      000A28                        564 	.ds 1
      000A29                        565 _set_last_mods_mods_10000_169:
      000A29                        566 	.ds 1
      000A2A                        567 _set_last_record_PARM_2:
      000A2A                        568 	.ds 3
      000A2D                        569 _set_last_record_keycode_10000_171:
      000A2D                        570 	.ds 2
      000A2F                        571 _update_last_repeat_count_dir_10000_173:
      000A2F                        572 	.ds 1
      000A30                        573 _repeat_invoke_PARM_2:
      000A30                        574 	.ds 1
      000A31                        575 _repeat_invoke_event_10000_181:
      000A31                        576 	.ds 3
      000A34                        577 _repeat_key_invoke_event_10000_195:
      000A34                        578 	.ds 3
      000A37                        579 _find_alt_keycode_PARM_2:
      000A37                        580 	.ds 1
      000A38                        581 _find_alt_keycode_PARM_3:
      000A38                        582 	.ds 1
      000A39                        583 _find_alt_keycode_table_10000_197:
      000A39                        584 	.ds 3
      000A3C                        585 _get_alt_repeat_key_keycode_keycode_10000_204:
      000A3C                        586 	.ds 2
      000A3E                        587 _get_alt_repeat_key_keycode_mods_10000_204:
      000A3E                        588 	.ds 1
      000A3F                        589 _get_alt_repeat_key_keycode_alt_keycode_10000_204:
      000A3F                        590 	.ds 2
      000A41                        591 _alt_repeat_key_invoke_event_10000_218:
      000A41                        592 	.ds 3
      000A44                        593 _get_alt_repeat_key_keycode_user_PARM_2:
      000A44                        594 	.ds 1
                                    595 ;--------------------------------------------------------
                                    596 ; absolute external ram data
                                    597 ;--------------------------------------------------------
                                    598 	.area XABS    (ABS,XDATA)
                                    599 ;--------------------------------------------------------
                                    600 ; initialized external ram data
                                    601 ;--------------------------------------------------------
                                    602 	.area XISEG   (XDATA)
      000C02                        603 _last_mods:
      000C02                        604 	.ds 1
      000C03                        605 _last_repeat_count:
      000C03                        606 	.ds 1
      000C04                        607 _processing_repeat_count:
      000C04                        608 	.ds 1
                                    609 	.area HOME    (CODE)
                                    610 	.area GSINIT0 (CODE)
                                    611 	.area GSINIT1 (CODE)
                                    612 	.area GSINIT2 (CODE)
                                    613 	.area GSINIT3 (CODE)
                                    614 	.area GSINIT4 (CODE)
                                    615 	.area GSINIT5 (CODE)
                                    616 	.area GSINIT  (CODE)
                                    617 	.area GSFINAL (CODE)
                                    618 	.area CSEG    (CODE)
                                    619 ;--------------------------------------------------------
                                    620 ; global & static initialisations
                                    621 ;--------------------------------------------------------
                                    622 	.area HOME    (CODE)
                                    623 	.area GSINIT  (CODE)
                                    624 	.area GSFINAL (CODE)
                                    625 	.area GSINIT  (CODE)
                                    626 ;--------------------------------------------------------
                                    627 ; Home
                                    628 ;--------------------------------------------------------
                                    629 	.area HOME    (CODE)
                                    630 	.area HOME    (CODE)
                                    631 ;--------------------------------------------------------
                                    632 ; code
                                    633 ;--------------------------------------------------------
                                    634 	.area CSEG    (CODE)
                                    635 ;------------------------------------------------------------
                                    636 ;Allocation info for local variables in function 'repeat_key_cancel'
                                    637 ;------------------------------------------------------------
                                    638 ;	quantum/repeat_key.c:36: void repeat_key_cancel(void) {
                                    639 ;	-----------------------------------------
                                    640 ;	 function repeat_key_cancel
                                    641 ;	-----------------------------------------
      009BDE                        642 _repeat_key_cancel:
                           000007   643 	ar7 = 0x07
                           000006   644 	ar6 = 0x06
                           000005   645 	ar5 = 0x05
                           000004   646 	ar4 = 0x04
                           000003   647 	ar3 = 0x03
                           000002   648 	ar2 = 0x02
                           000001   649 	ar1 = 0x01
                           000000   650 	ar0 = 0x00
                                    651 ;	quantum/repeat_key.c:37: registered_record.keycode = 0;
      009BDE 90 0A 25         [24]  652 	mov	dptr,#(_registered_record + 0x0006)
      009BE1 E4               [12]  653 	clr	a
      009BE2 F0               [24]  654 	movx	@dptr,a
      009BE3 A3               [24]  655 	inc	dptr
      009BE4 F0               [24]  656 	movx	@dptr,a
                                    657 ;	quantum/repeat_key.c:38: }
      009BE5 22               [24]  658 	ret
                                    659 ;------------------------------------------------------------
                                    660 ;Allocation info for local variables in function 'get_last_keycode'
                                    661 ;------------------------------------------------------------
                                    662 ;	quantum/repeat_key.c:40: uint16_t get_last_keycode(void) {
                                    663 ;	-----------------------------------------
                                    664 ;	 function set_last_mods
                                    665 ;	-----------------------------------------
      009BE6                        666 _set_last_mods:
      009BE6 E5 82            [12]  667 	mov	a,dpl
      009BE8 90 0A 29         [24]  668 	mov	dptr,#_set_last_mods_mods_10000_169
      009BEB F0               [24]  669 	movx	@dptr,a
                                    670 ;	quantum/repeat_key.c:58: last_mods = mods;
      009BEC E0               [24]  671 	movx	a,@dptr
      009BED 90 0C 02         [24]  672 	mov	dptr,#_last_mods
      009BF0 F0               [24]  673 	movx	@dptr,a
                                    674 ;	quantum/repeat_key.c:59: }
      009BF1 22               [24]  675 	ret
                                    676 ;------------------------------------------------------------
                                    677 ;Allocation info for local variables in function 'set_last_record'
                                    678 ;------------------------------------------------------------
                                    679 ;record        Allocated with name '_set_last_record_PARM_2'
                                    680 ;keycode       Allocated with name '_set_last_record_keycode_10000_171'
                                    681 ;------------------------------------------------------------
                                    682 ;	quantum/repeat_key.c:61: void set_last_record(uint16_t keycode, keyrecord_t* record) {
                                    683 ;	-----------------------------------------
                                    684 ;	 function set_last_record
                                    685 ;	-----------------------------------------
      009BF2                        686 _set_last_record:
      009BF2 AF 83            [24]  687 	mov	r7,dph
      009BF4 E5 82            [12]  688 	mov	a,dpl
      009BF6 90 0A 2D         [24]  689 	mov	dptr,#_set_last_record_keycode_10000_171
      009BF9 F0               [24]  690 	movx	@dptr,a
      009BFA EF               [12]  691 	mov	a,r7
      009BFB A3               [24]  692 	inc	dptr
      009BFC F0               [24]  693 	movx	@dptr,a
                                    694 ;	quantum/repeat_key.c:62: last_record         = *record;
      009BFD 90 0A 2A         [24]  695 	mov	dptr,#_set_last_record_PARM_2
      009C00 12 73 B8         [24]  696 	lcall	_ak820_outline_0002
      009C03 90 0B 90         [24]  697 	mov	dptr,#___memcpy_PARM_2
      009C06 12 73 D9         [24]  698 	lcall	_ak820_outline_0015
      009C09 90 0B 93         [24]  699 	mov	dptr,#___memcpy_PARM_3
      009C0C 74 08            [12]  700 	mov	a,#0x08
      009C0E F0               [24]  701 	movx	@dptr,a
      009C0F E4               [12]  702 	clr	a
      009C10 A3               [24]  703 	inc	dptr
      009C11 F0               [24]  704 	movx	@dptr,a
      009C12 90 0A 17         [24]  705 	mov	dptr,#_last_record
      009C15 F5 F0            [12]  706 	mov	b,a
      009C17 12 B4 C1         [24]  707 	lcall	___memcpy
                                    708 ;	quantum/repeat_key.c:63: last_record.keycode = keycode;
      009C1A 90 0A 2D         [24]  709 	mov	dptr,#_set_last_record_keycode_10000_171
      009C1D E0               [24]  710 	movx	a,@dptr
      009C1E FE               [12]  711 	mov	r6,a
      009C1F A3               [24]  712 	inc	dptr
      009C20 E0               [24]  713 	movx	a,@dptr
      009C21 FF               [12]  714 	mov	r7,a
      009C22 90 0A 1D         [24]  715 	mov	dptr,#(_last_record + 0x0006)
      009C25 EE               [12]  716 	mov	a,r6
      009C26 F0               [24]  717 	movx	@dptr,a
      009C27 EF               [12]  718 	mov	a,r7
      009C28 A3               [24]  719 	inc	dptr
      009C29 F0               [24]  720 	movx	@dptr,a
                                    721 ;	quantum/repeat_key.c:64: last_repeat_count   = 0;
      009C2A 90 0C 03         [24]  722 	mov	dptr,#_last_repeat_count
      009C2D E4               [12]  723 	clr	a
      009C2E F0               [24]  724 	movx	@dptr,a
                                    725 ;	quantum/repeat_key.c:65: }
      009C2F 22               [24]  726 	ret
                                    727 ;------------------------------------------------------------
                                    728 ;Allocation info for local variables in function 'update_last_repeat_count'
                                    729 ;------------------------------------------------------------
                                    730 ;dir           Allocated with name '_update_last_repeat_count_dir_10000_173'
                                    731 ;------------------------------------------------------------
                                    732 ;	quantum/repeat_key.c:68: static void update_last_repeat_count(int8_t dir) {
                                    733 ;	-----------------------------------------
                                    734 ;	 function update_last_repeat_count
                                    735 ;	-----------------------------------------
      009C30                        736 _update_last_repeat_count:
      009C30 E5 82            [12]  737 	mov	a,dpl
      009C32 90 0A 2F         [24]  738 	mov	dptr,#_update_last_repeat_count_dir_10000_173
      009C35 F0               [24]  739 	movx	@dptr,a
                                    740 ;	quantum/repeat_key.c:69: if ((dir < 0) != (last_repeat_count < 0)) {
      009C36 E0               [24]  741 	movx	a,@dptr
      009C37 FF               [12]  742 	mov	r7,a
      009C38 33               [12]  743 	rlc	a
      009C39 E4               [12]  744 	clr	a
      009C3A 33               [12]  745 	rlc	a
      009C3B FE               [12]  746 	mov	r6,a
      009C3C 90 0C 03         [24]  747 	mov	dptr,#_last_repeat_count
      009C3F E0               [24]  748 	movx	a,@dptr
      009C40 FD               [12]  749 	mov	r5,a
      009C41 33               [12]  750 	rlc	a
      009C42 E4               [12]  751 	clr	a
      009C43 33               [12]  752 	rlc	a
      009C44 FC               [12]  753 	mov	r4,a
      009C45 EE               [12]  754 	mov	a,r6
      009C46 B5 04 02         [24]  755 	cjne	a,ar4,00131$
      009C49 80 06            [24]  756 	sjmp	00104$
      009C4B                        757 00131$:
                                    758 ;	quantum/repeat_key.c:70: last_repeat_count = dir;
      009C4B 90 0C 03         [24]  759 	mov	dptr,#_last_repeat_count
      009C4E EF               [12]  760 	mov	a,r7
      009C4F F0               [24]  761 	movx	@dptr,a
      009C50 22               [24]  762 	ret
      009C51                        763 00104$:
                                    764 ;	quantum/repeat_key.c:71: } else if (dir < 0 ? last_repeat_count > -127 : last_repeat_count < 127) {
      009C51 EE               [12]  765 	mov	a,r6
      009C52 60 0F            [24]  766 	jz	00108$
      009C54 C3               [12]  767 	clr	c
      009C55 74 01            [12]  768 	mov	a,#(0x81 ^ 0x80)
      009C57 8D F0            [24]  769 	mov	b,r5
      009C59 63 F0 80         [24]  770 	xrl	b,#0x80
      009C5C 95 F0            [12]  771 	subb	a,b
      009C5E E4               [12]  772 	clr	a
      009C5F 33               [12]  773 	rlc	a
      009C60 FF               [12]  774 	mov	r7,a
                                    775 ;	free result
      009C61 80 09            [24]  776 	sjmp	00109$
      009C63                        777 00108$:
      009C63 C3               [12]  778 	clr	c
      009C64 ED               [12]  779 	mov	a,r5
      009C65 64 80            [12]  780 	xrl	a,#0x80
      009C67 94 FF            [12]  781 	subb	a,#0xff
      009C69 E4               [12]  782 	clr	a
      009C6A 33               [12]  783 	rlc	a
      009C6B FF               [12]  784 	mov	r7,a
      009C6C                        785 00109$:
      009C6C EF               [12]  786 	mov	a,r7
      009C6D 60 09            [24]  787 	jz	00106$
                                    788 ;	quantum/repeat_key.c:72: last_repeat_count += dir;
      009C6F 90 0A 2F         [24]  789 	mov	dptr,#_update_last_repeat_count_dir_10000_173
      009C72 E0               [24]  790 	movx	a,@dptr
      009C73 90 0C 03         [24]  791 	mov	dptr,#_last_repeat_count
      009C76 2D               [12]  792 	add	a, r5
      009C77 F0               [24]  793 	movx	@dptr,a
      009C78                        794 00106$:
                                    795 ;	quantum/repeat_key.c:74: }
      009C78 22               [24]  796 	ret
                                    797 ;------------------------------------------------------------
                                    798 ;Allocation info for local variables in function 'get_repeat_key_count'
                                    799 ;------------------------------------------------------------
                                    800 ;	quantum/repeat_key.c:76: int8_t get_repeat_key_count(void) {
                                    801 ;	-----------------------------------------
                                    802 ;	 function get_repeat_key_count
                                    803 ;	-----------------------------------------
      009C79                        804 _get_repeat_key_count:
                                    805 ;	quantum/repeat_key.c:77: return processing_repeat_count;
      009C79 90 0C 04         [24]  806 	mov	dptr,#_processing_repeat_count
      009C7C E0               [24]  807 	movx	a,@dptr
                                    808 ;	quantum/repeat_key.c:78: }
      009C7D F5 82            [12]  809 	mov	dpl,a
      009C7F 22               [24]  810 	ret
                                    811 ;------------------------------------------------------------
                                    812 ;Allocation info for local variables in function 'repeat_invoke'
                                    813 ;------------------------------------------------------------
                                    814 ;alternate     Allocated with name '_repeat_invoke_PARM_2'
                                    815 ;event         Allocated with name '_repeat_invoke_event_10000_181'
                                    816 ;------------------------------------------------------------
                                    817 ;	quantum/repeat_key.c:80: static void repeat_invoke(const keyevent_t* event, bool alternate) {
                                    818 ;	-----------------------------------------
                                    819 ;	 function repeat_invoke
                                    820 ;	-----------------------------------------
      009C80                        821 _repeat_invoke:
      009C80 AF F0            [24]  822 	mov	r7,b
      009C82 AE 83            [24]  823 	mov	r6,dph
      009C84 E5 82            [12]  824 	mov	a,dpl
      009C86 90 0A 31         [24]  825 	mov	dptr,#_repeat_invoke_event_10000_181
      009C89 F0               [24]  826 	movx	@dptr,a
      009C8A EE               [12]  827 	mov	a,r6
      009C8B A3               [24]  828 	inc	dptr
      009C8C F0               [24]  829 	movx	@dptr,a
      009C8D EF               [12]  830 	mov	a,r7
      009C8E A3               [24]  831 	inc	dptr
      009C8F F0               [24]  832 	movx	@dptr,a
                                    833 ;	quantum/repeat_key.c:88: if (processing_repeat_count) {
      009C90 90 0C 04         [24]  834 	mov	dptr,#_processing_repeat_count
      009C93 E0               [24]  835 	movx	a,@dptr
      009C94 60 01            [24]  836 	jz	00102$
                                    837 ;	quantum/repeat_key.c:89: return;
      009C96 22               [24]  838 	ret
      009C97                        839 00102$:
                                    840 ;	quantum/repeat_key.c:92: if (event->pressed) {
      009C97 90 0A 31         [24]  841 	mov	dptr,#_repeat_invoke_event_10000_181
      009C9A 12 73 B8         [24]  842 	lcall	_ak820_outline_0002
      009C9D 74 05            [12]  843 	mov	a,#0x05
      009C9F 12 73 C1         [24]  844 	lcall	_ak820_outline_0009
      009CA2 12 B5 9A         [24]  845 	lcall	__gptrget
      009CA5 70 03            [24]  846 	jnz	00187$
      009CA7 02 9D 2B         [24]  847 	ljmp	00115$
      009CAA                        848 00187$:
                                    849 ;	quantum/repeat_key.c:95: if (registered_record.keycode || !last_record.keycode) return;
      009CAA 90 0A 25         [24]  850 	mov	dptr,#(_registered_record + 0x0006)
      009CAD E0               [24]  851 	movx	a,@dptr
      009CAE FB               [12]  852 	mov	r3,a
      009CAF A3               [24]  853 	inc	dptr
      009CB0 E0               [24]  854 	movx	a,@dptr
      009CB1 4B               [12]  855 	orl	a,r3
      009CB2 70 0A            [24]  856 	jnz	00103$
      009CB4 90 0A 1D         [24]  857 	mov	dptr,#(_last_record + 0x0006)
      009CB7 E0               [24]  858 	movx	a,@dptr
      009CB8 FB               [12]  859 	mov	r3,a
      009CB9 A3               [24]  860 	inc	dptr
      009CBA E0               [24]  861 	movx	a,@dptr
      009CBB 4B               [12]  862 	orl	a,r3
      009CBC 70 01            [24]  863 	jnz	00104$
      009CBE                        864 00103$:
      009CBE 22               [24]  865 	ret
      009CBF                        866 00104$:
                                    867 ;	quantum/repeat_key.c:96: registered_record = last_record;
      009CBF 90 0B 90         [24]  868 	mov	dptr,#___memcpy_PARM_2
      009CC2 74 17            [12]  869 	mov	a,#_last_record
      009CC4 F0               [24]  870 	movx	@dptr,a
      009CC5 74 0A            [12]  871 	mov	a,#(_last_record >> 8)
      009CC7 A3               [24]  872 	inc	dptr
      009CC8 F0               [24]  873 	movx	@dptr,a
      009CC9 E4               [12]  874 	clr	a
      009CCA A3               [24]  875 	inc	dptr
      009CCB F0               [24]  876 	movx	@dptr,a
      009CCC 90 0B 93         [24]  877 	mov	dptr,#___memcpy_PARM_3
      009CCF 74 08            [12]  878 	mov	a,#0x08
      009CD1 F0               [24]  879 	movx	@dptr,a
      009CD2 E4               [12]  880 	clr	a
      009CD3 A3               [24]  881 	inc	dptr
      009CD4 F0               [24]  882 	movx	@dptr,a
      009CD5 90 0A 1F         [24]  883 	mov	dptr,#_registered_record
      009CD8 F5 F0            [12]  884 	mov	b,a
      009CDA 12 B4 C1         [24]  885 	lcall	___memcpy
                                    886 ;	quantum/repeat_key.c:97: registered_mods = last_mods;
      009CDD 90 0C 02         [24]  887 	mov	dptr,#_last_mods
      009CE0 E0               [24]  888 	movx	a,@dptr
      009CE1 90 0A 28         [24]  889 	mov	dptr,#_registered_mods
      009CE4 F0               [24]  890 	movx	@dptr,a
                                    891 ;	quantum/repeat_key.c:99: if (alternate) {
      009CE5 90 0A 30         [24]  892 	mov	dptr,#_repeat_invoke_PARM_2
      009CE8 E0               [24]  893 	movx	a,@dptr
      009CE9 FC               [12]  894 	mov	r4,a
      009CEA E0               [24]  895 	movx	a,@dptr
      009CEB 60 1D            [24]  896 	jz	00109$
                                    897 ;	quantum/repeat_key.c:100: registered_record.keycode = get_alt_repeat_key_keycode();
      009CED C0 04            [24]  898 	push	ar4
      009CEF 12 9E 3B         [24]  899 	lcall	_get_alt_repeat_key_keycode
      009CF2 AA 82            [24]  900 	mov	r2, dpl
      009CF4 AB 83            [24]  901 	mov	r3, dph
      009CF6 D0 04            [24]  902 	pop	ar4
      009CF8 90 0A 25         [24]  903 	mov	dptr,#(_registered_record + 0x0006)
      009CFB EA               [12]  904 	mov	a,r2
      009CFC F0               [24]  905 	movx	@dptr,a
      009CFD EB               [12]  906 	mov	a,r3
      009CFE A3               [24]  907 	inc	dptr
      009CFF F0               [24]  908 	movx	@dptr,a
                                    909 ;	quantum/repeat_key.c:101: if (!registered_record.keycode) return;
      009D00 EA               [12]  910 	mov	a,r2
      009D01 4B               [12]  911 	orl	a,r3
      009D02 70 01            [24]  912 	jnz	00107$
      009D04 22               [24]  913 	ret
      009D05                        914 00107$:
                                    915 ;	quantum/repeat_key.c:103: registered_mods = 0;
      009D05 90 0A 28         [24]  916 	mov	dptr,#_registered_mods
      009D08 E4               [12]  917 	clr	a
      009D09 F0               [24]  918 	movx	@dptr,a
      009D0A                        919 00109$:
                                    920 ;	quantum/repeat_key.c:106: update_last_repeat_count(alternate ? -1 : 1);
      009D0A EC               [12]  921 	mov	a,r4
      009D0B 60 04            [24]  922 	jz	00121$
      009D0D 7C FF            [12]  923 	mov	r4,#0xff
      009D0F 80 02            [24]  924 	sjmp	00122$
      009D11                        925 00121$:
      009D11 7C 01            [12]  926 	mov	r4,#0x01
      009D13                        927 00122$:
      009D13 8C 82            [24]  928 	mov	dpl, r4
      009D15 12 9C 30         [24]  929 	lcall	_update_last_repeat_count
                                    930 ;	quantum/repeat_key.c:107: register_weak_mods(registered_mods);
      009D18 90 0A 28         [24]  931 	mov	dptr,#_registered_mods
      009D1B E0               [24]  932 	movx	a,@dptr
      009D1C F5 82            [12]  933 	mov	dpl,a
      009D1E 12 73 6C         [24]  934 	lcall	_register_weak_mods
                                    935 ;	quantum/repeat_key.c:108: registered_repeat_count = last_repeat_count;
      009D21 90 0C 03         [24]  936 	mov	dptr,#_last_repeat_count
      009D24 E0               [24]  937 	movx	a,@dptr
      009D25 90 0A 27         [24]  938 	mov	dptr,#_registered_repeat_count
      009D28 F0               [24]  939 	movx	@dptr,a
      009D29 80 32            [24]  940 	sjmp	00116$
      009D2B                        941 00115$:
                                    942 ;	quantum/repeat_key.c:111: if (!registered_record.keycode || event->key.row != registered_record.event.key.row ||
      009D2B 90 0A 25         [24]  943 	mov	dptr,#(_registered_record + 0x0006)
      009D2E E0               [24]  944 	movx	a,@dptr
      009D2F FB               [12]  945 	mov	r3,a
      009D30 A3               [24]  946 	inc	dptr
      009D31 E0               [24]  947 	movx	a,@dptr
      009D32 4B               [12]  948 	orl	a,r3
      009D33 60 27            [24]  949 	jz	00110$
      009D35 74 01            [12]  950 	mov	a,#0x01
      009D37 12 73 C1         [24]  951 	lcall	_ak820_outline_0009
      009D3A 12 B5 9A         [24]  952 	lcall	__gptrget
      009D3D FA               [12]  953 	mov	r2,a
      009D3E 90 0A 20         [24]  954 	mov	dptr,#(_registered_record + 0x0001)
      009D41 E0               [24]  955 	movx	a,@dptr
      009D42 FC               [12]  956 	mov	r4,a
      009D43 EA               [12]  957 	mov	a,r2
      009D44 B5 04 15         [24]  958 	cjne	a,ar4,00110$
                                    959 ;	quantum/repeat_key.c:112: event->key.col != registered_record.event.key.col) return;
      009D47 8D 82            [24]  960 	mov	dpl,r5
      009D49 8E 83            [24]  961 	mov	dph,r6
      009D4B 8F F0            [24]  962 	mov	b,r7
      009D4D 12 B5 9A         [24]  963 	lcall	__gptrget
      009D50 FD               [12]  964 	mov	r5,a
      009D51 90 0A 1F         [24]  965 	mov	dptr,#_registered_record
      009D54 E0               [24]  966 	movx	a,@dptr
      009D55 FF               [12]  967 	mov	r7,a
      009D56 ED               [12]  968 	mov	a,r5
      009D57 B5 07 02         [24]  969 	cjne	a,ar7,00196$
      009D5A 80 01            [24]  970 	sjmp	00116$
      009D5C                        971 00196$:
      009D5C                        972 00110$:
      009D5C 22               [24]  973 	ret
      009D5D                        974 00116$:
                                    975 ;	quantum/repeat_key.c:116: registered_record.event = *event;
      009D5D 90 0A 31         [24]  976 	mov	dptr,#_repeat_invoke_event_10000_181
      009D60 12 73 B8         [24]  977 	lcall	_ak820_outline_0002
      009D63 90 0B 90         [24]  978 	mov	dptr,#___memcpy_PARM_2
      009D66 12 73 D9         [24]  979 	lcall	_ak820_outline_0015
      009D69 90 0B 93         [24]  980 	mov	dptr,#___memcpy_PARM_3
      009D6C 74 06            [12]  981 	mov	a,#0x06
      009D6E F0               [24]  982 	movx	@dptr,a
      009D6F E4               [12]  983 	clr	a
      009D70 A3               [24]  984 	inc	dptr
      009D71 F0               [24]  985 	movx	@dptr,a
      009D72 90 0A 1F         [24]  986 	mov	dptr,#_registered_record
      009D75 F5 F0            [12]  987 	mov	b,a
      009D77 12 B4 C1         [24]  988 	lcall	___memcpy
                                    989 ;	quantum/repeat_key.c:117: processing_repeat_count = registered_repeat_count;
      009D7A 90 0A 27         [24]  990 	mov	dptr,#_registered_repeat_count
      009D7D E0               [24]  991 	movx	a,@dptr
      009D7E 90 0C 04         [24]  992 	mov	dptr,#_processing_repeat_count
      009D81 F0               [24]  993 	movx	@dptr,a
                                    994 ;	quantum/repeat_key.c:118: process_record(&registered_record);
      009D82 90 0A 1F         [24]  995 	mov	dptr,#_registered_record
      009D85 75 F0 00         [24]  996 	mov	b, #0x00
      009D88 12 6D 4B         [24]  997 	lcall	_process_record
                                    998 ;	quantum/repeat_key.c:119: processing_repeat_count = 0;
      009D8B 90 0C 04         [24]  999 	mov	dptr,#_processing_repeat_count
      009D8E E4               [12] 1000 	clr	a
      009D8F F0               [24] 1001 	movx	@dptr,a
                                   1002 ;	quantum/repeat_key.c:125: if (!registered_record.event.pressed) {
      009D90 90 0A 24         [24] 1003 	mov	dptr,#(_registered_record + 0x0005)
      009D93 E0               [24] 1004 	movx	a,@dptr
      009D94 70 10            [24] 1005 	jnz	00119$
                                   1006 ;	quantum/repeat_key.c:126: unregister_weak_mods(registered_mods);
      009D96 90 0A 28         [24] 1007 	mov	dptr,#_registered_mods
      009D99 E0               [24] 1008 	movx	a,@dptr
      009D9A F5 82            [12] 1009 	mov	dpl,a
      009D9C 12 73 80         [24] 1010 	lcall	_unregister_weak_mods
                                   1011 ;	quantum/repeat_key.c:127: registered_record.keycode = 0;
      009D9F 90 0A 25         [24] 1012 	mov	dptr,#(_registered_record + 0x0006)
      009DA2 E4               [12] 1013 	clr	a
      009DA3 F0               [24] 1014 	movx	@dptr,a
      009DA4 A3               [24] 1015 	inc	dptr
      009DA5 F0               [24] 1016 	movx	@dptr,a
      009DA6                       1017 00119$:
                                   1018 ;	quantum/repeat_key.c:129: }
      009DA6 22               [24] 1019 	ret
                                   1020 ;------------------------------------------------------------
                                   1021 ;Allocation info for local variables in function 'repeat_key_invoke'
                                   1022 ;------------------------------------------------------------
                                   1023 ;event         Allocated with name '_repeat_key_invoke_event_10000_195'
                                   1024 ;------------------------------------------------------------
                                   1025 ;	quantum/repeat_key.c:131: void repeat_key_invoke(const keyevent_t* event) {
                                   1026 ;	-----------------------------------------
                                   1027 ;	 function repeat_key_invoke
                                   1028 ;	-----------------------------------------
      009DA7                       1029 _repeat_key_invoke:
      009DA7 AF F0            [24] 1030 	mov	r7,b
      009DA9 AE 83            [24] 1031 	mov	r6,dph
      009DAB E5 82            [12] 1032 	mov	a,dpl
      009DAD 90 0A 34         [24] 1033 	mov	dptr,#_repeat_key_invoke_event_10000_195
      009DB0 F0               [24] 1034 	movx	@dptr,a
      009DB1 EE               [12] 1035 	mov	a,r6
      009DB2 A3               [24] 1036 	inc	dptr
      009DB3 F0               [24] 1037 	movx	@dptr,a
      009DB4 EF               [12] 1038 	mov	a,r7
      009DB5 A3               [24] 1039 	inc	dptr
      009DB6 F0               [24] 1040 	movx	@dptr,a
                                   1041 ;	quantum/repeat_key.c:132: repeat_invoke(event, false);
      009DB7 90 0A 34         [24] 1042 	mov	dptr,#_repeat_key_invoke_event_10000_195
      009DBA 12 73 B8         [24] 1043 	lcall	_ak820_outline_0002
      009DBD 90 0A 30         [24] 1044 	mov	dptr,#_repeat_invoke_PARM_2
      009DC0 E4               [12] 1045 	clr	a
      009DC1 F0               [24] 1046 	movx	@dptr,a
      009DC2 8D 82            [24] 1047 	mov	dpl, r5
      009DC4 8E 83            [24] 1048 	mov	dph, r6
      009DC6 8F F0            [24] 1049 	mov	b, r7
                                   1050 ;	quantum/repeat_key.c:133: }
      009DC8 02 9C 80         [24] 1051 	ljmp	_repeat_invoke
                                   1052 ;------------------------------------------------------------
                                   1053 ;Allocation info for local variables in function 'find_alt_keycode'
                                   1054 ;------------------------------------------------------------
                                   1055 ;table_size_bytes Allocated with name '_find_alt_keycode_PARM_2'
                                   1056 ;target        Allocated with name '_find_alt_keycode_PARM_3'
                                   1057 ;table         Allocated with name '_find_alt_keycode_table_10000_197'
                                   1058 ;keycodes      Allocated with name '_find_alt_keycode_keycodes_10000_198'
                                   1059 ;i             Allocated with name '_find_alt_keycode_i_20000_199'
                                   1060 ;sloc0         Allocated with name '_find_alt_keycode_sloc0_1_0'
                                   1061 ;------------------------------------------------------------
                                   1062 ;	quantum/repeat_key.c:149: static uint8_t find_alt_keycode(const uint8_t (*table)[2], uint8_t table_size_bytes, uint8_t target) {
                                   1063 ;	-----------------------------------------
                                   1064 ;	 function find_alt_keycode
                                   1065 ;	-----------------------------------------
      009DCB                       1066 _find_alt_keycode:
      009DCB AF F0            [24] 1067 	mov	r7,b
      009DCD AE 83            [24] 1068 	mov	r6,dph
      009DCF E5 82            [12] 1069 	mov	a,dpl
      009DD1 90 0A 39         [24] 1070 	mov	dptr,#_find_alt_keycode_table_10000_197
      009DD4 F0               [24] 1071 	movx	@dptr,a
      009DD5 EE               [12] 1072 	mov	a,r6
      009DD6 A3               [24] 1073 	inc	dptr
      009DD7 F0               [24] 1074 	movx	@dptr,a
      009DD8 EF               [12] 1075 	mov	a,r7
      009DD9 A3               [24] 1076 	inc	dptr
      009DDA F0               [24] 1077 	movx	@dptr,a
                                   1078 ;	quantum/repeat_key.c:150: const uint8_t* keycodes = (const uint8_t*)table;
      009DDB 90 0A 39         [24] 1079 	mov	dptr,#_find_alt_keycode_table_10000_197
      009DDE E0               [24] 1080 	movx	a,@dptr
      009DDF F5 5D            [12] 1081 	mov	_find_alt_keycode_sloc0_1_0,a
      009DE1 A3               [24] 1082 	inc	dptr
      009DE2 E0               [24] 1083 	movx	a,@dptr
      009DE3 F5 5E            [12] 1084 	mov	(_find_alt_keycode_sloc0_1_0 + 1),a
      009DE5 A3               [24] 1085 	inc	dptr
      009DE6 E0               [24] 1086 	movx	a,@dptr
      009DE7 F5 5F            [12] 1087 	mov	(_find_alt_keycode_sloc0_1_0 + 2),a
                                   1088 ;	quantum/repeat_key.c:151: for (uint8_t i = 0; i < table_size_bytes; ++i) {
      009DE9 90 0A 38         [24] 1089 	mov	dptr,#_find_alt_keycode_PARM_3
      009DEC E0               [24] 1090 	movx	a,@dptr
      009DED FC               [12] 1091 	mov	r4,a
      009DEE 90 0A 37         [24] 1092 	mov	dptr,#_find_alt_keycode_PARM_2
      009DF1 E0               [24] 1093 	movx	a,@dptr
      009DF2 FB               [12] 1094 	mov	r3,a
      009DF3 7A 00            [12] 1095 	mov	r2,#0x00
      009DF5                       1096 00105$:
      009DF5 C3               [12] 1097 	clr	c
      009DF6 EA               [12] 1098 	mov	a,r2
      009DF7 9B               [12] 1099 	subb	a,r3
      009DF8 50 3D            [24] 1100 	jnc	00103$
                                   1101 ;	quantum/repeat_key.c:152: if (target == pgm_read_byte(keycodes + i)) {
      009DFA C0 03            [24] 1102 	push	ar3
      009DFC EA               [12] 1103 	mov	a,r2
      009DFD 25 5D            [12] 1104 	add	a, _find_alt_keycode_sloc0_1_0
      009DFF F8               [12] 1105 	mov	r0,a
      009E00 E4               [12] 1106 	clr	a
      009E01 35 5E            [12] 1107 	addc	a, (_find_alt_keycode_sloc0_1_0 + 1)
      009E03 F9               [12] 1108 	mov	r1,a
      009E04 AB 5F            [24] 1109 	mov	r3,(_find_alt_keycode_sloc0_1_0 + 2)
      009E06 88 82            [24] 1110 	mov	dpl,r0
      009E08 89 83            [24] 1111 	mov	dph,r1
      009E0A 8B F0            [24] 1112 	mov	b,r3
      009E0C 12 B5 9A         [24] 1113 	lcall	__gptrget
      009E0F F8               [12] 1114 	mov	r0,a
      009E10 EC               [12] 1115 	mov	a,r4
      009E11 B5 00 02         [24] 1116 	cjne	a,ar0,00131$
      009E14 80 04            [24] 1117 	sjmp	00132$
      009E16                       1118 00131$:
      009E16 D0 03            [24] 1119 	pop	ar3
      009E18 80 1A            [24] 1120 	sjmp	00106$
      009E1A                       1121 00132$:
      009E1A D0 03            [24] 1122 	pop	ar3
                                   1123 ;	quantum/repeat_key.c:154: return pgm_read_byte(keycodes + (i ^ 1));
      009E1C 74 01            [12] 1124 	mov	a,#0x01
      009E1E 6A               [12] 1125 	xrl	a,r2
      009E1F 25 5D            [12] 1126 	add	a, _find_alt_keycode_sloc0_1_0
      009E21 F8               [12] 1127 	mov	r0,a
      009E22 E4               [12] 1128 	clr	a
      009E23 35 5E            [12] 1129 	addc	a,(_find_alt_keycode_sloc0_1_0 + 1)
      009E25 F9               [12] 1130 	mov	r1,a
      009E26 AF 5F            [24] 1131 	mov	r7,(_find_alt_keycode_sloc0_1_0 + 2)
      009E28 88 82            [24] 1132 	mov	dpl,r0
      009E2A 89 83            [24] 1133 	mov	dph,r1
      009E2C 8F F0            [24] 1134 	mov	b,r7
      009E2E 12 B5 9A         [24] 1135 	lcall	__gptrget
      009E31 F5 82            [12] 1136 	mov	dpl,a
      009E33 22               [24] 1137 	ret
      009E34                       1138 00106$:
                                   1139 ;	quantum/repeat_key.c:151: for (uint8_t i = 0; i < table_size_bytes; ++i) {
      009E34 0A               [12] 1140 	inc	r2
      009E35 80 BE            [24] 1141 	sjmp	00105$
      009E37                       1142 00103$:
                                   1143 ;	quantum/repeat_key.c:157: return KC_NO;
      009E37 75 82 00         [24] 1144 	mov	dpl, #0x00
                                   1145 ;	quantum/repeat_key.c:158: }
      009E3A 22               [24] 1146 	ret
                                   1147 ;------------------------------------------------------------
                                   1148 ;Allocation info for local variables in function 'get_alt_repeat_key_keycode'
                                   1149 ;------------------------------------------------------------
                                   1150 ;keycode       Allocated with name '_get_alt_repeat_key_keycode_keycode_10000_204'
                                   1151 ;mods          Allocated with name '_get_alt_repeat_key_keycode_mods_10000_204'
                                   1152 ;alt_keycode   Allocated with name '_get_alt_repeat_key_keycode_alt_keycode_10000_204'
                                   1153 ;------------------------------------------------------------
                                   1154 ;	quantum/repeat_key.c:160: uint16_t get_alt_repeat_key_keycode(void) {
                                   1155 ;	-----------------------------------------
                                   1156 ;	 function get_alt_repeat_key_keycode
                                   1157 ;	-----------------------------------------
      009E3B                       1158 _get_alt_repeat_key_keycode:
                                   1159 ;	quantum/repeat_key.c:161: uint16_t keycode = last_record.keycode;
      009E3B 90 0A 1D         [24] 1160 	mov	dptr,#(_last_record + 0x0006)
      009E3E E0               [24] 1161 	movx	a,@dptr
      009E3F FE               [12] 1162 	mov	r6,a
      009E40 A3               [24] 1163 	inc	dptr
      009E41 E0               [24] 1164 	movx	a,@dptr
      009E42 FF               [12] 1165 	mov	r7,a
      009E43 90 0A 3C         [24] 1166 	mov	dptr,#_get_alt_repeat_key_keycode_keycode_10000_204
      009E46 EE               [12] 1167 	mov	a,r6
      009E47 F0               [24] 1168 	movx	@dptr,a
      009E48 EF               [12] 1169 	mov	a,r7
      009E49 A3               [24] 1170 	inc	dptr
      009E4A F0               [24] 1171 	movx	@dptr,a
                                   1172 ;	quantum/repeat_key.c:162: uint8_t  mods    = last_mods;
      009E4B 90 0C 02         [24] 1173 	mov	dptr,#_last_mods
      009E4E E0               [24] 1174 	movx	a,@dptr
      009E4F FD               [12] 1175 	mov	r5,a
      009E50 90 0A 3E         [24] 1176 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009E53 F0               [24] 1177 	movx	@dptr,a
                                   1178 ;	quantum/repeat_key.c:166: uint16_t alt_keycode = get_alt_repeat_key_keycode_user(keycode, mods);
      009E54 90 0A 44         [24] 1179 	mov	dptr,#_get_alt_repeat_key_keycode_user_PARM_2
      009E57 ED               [12] 1180 	mov	a,r5
      009E58 F0               [24] 1181 	movx	@dptr,a
      009E59 8E 82            [24] 1182 	mov	dpl, r6
      009E5B 8F 83            [24] 1183 	mov	dph, r7
      009E5D C0 07            [24] 1184 	push	ar7
      009E5F C0 06            [24] 1185 	push	ar6
      009E61 12 9F 91         [24] 1186 	lcall	_get_alt_repeat_key_keycode_user
      009E64 AC 82            [24] 1187 	mov	r4, dpl
      009E66 AD 83            [24] 1188 	mov	r5, dph
      009E68 D0 06            [24] 1189 	pop	ar6
      009E6A D0 07            [24] 1190 	pop	ar7
                                   1191 ;	quantum/repeat_key.c:168: if (alt_keycode != KC_TRANSPARENT) {
      009E6C 8C 02            [24] 1192 	mov	ar2,r4
      009E6E 8D 03            [24] 1193 	mov	ar3,r5
      009E70 BA 01 05         [24] 1194 	cjne	r2,#0x01,00176$
      009E73 BB 00 02         [24] 1195 	cjne	r3,#0x00,00176$
      009E76 80 05            [24] 1196 	sjmp	00102$
      009E78                       1197 00176$:
                                   1198 ;	quantum/repeat_key.c:169: return alt_keycode;
      009E78 8C 82            [24] 1199 	mov	dpl, r4
      009E7A 8D 83            [24] 1200 	mov	dph, r5
      009E7C 22               [24] 1201 	ret
      009E7D                       1202 00102$:
                                   1203 ;	quantum/repeat_key.c:174: mods = ((mods & 0xf0) ? /* set right hand bit */ 0x10 : 0)
      009E7D 90 0A 3E         [24] 1204 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009E80 E0               [24] 1205 	movx	a,@dptr
      009E81 54 F0            [12] 1206 	anl	a,#0xf0
      009E83 60 02            [24] 1207 	jz	00118$
      009E85 74 10            [12] 1208 	mov	a,#0x10
      009E87                       1209 00118$:
      009E87 FD               [12] 1210 	mov	r5,a
                                   1211 ;	quantum/repeat_key.c:176: | (((mods >> 4) | mods) & 0xf);
      009E88 90 0A 3E         [24] 1212 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009E8B E0               [24] 1213 	movx	a,@dptr
      009E8C FC               [12] 1214 	mov	r4,a
      009E8D C4               [12] 1215 	swap	a
      009E8E 54 0F            [12] 1216 	anl	a,#0x0f
      009E90 4C               [12] 1217 	orl	a,r4
      009E91 54 0F            [12] 1218 	anl	a,#0x0f
      009E93 4D               [12] 1219 	orl	a,r5
      009E94 F0               [24] 1220 	movx	@dptr,a
                                   1221 ;	quantum/repeat_key.c:179: if (keycode >= QK_MODS && keycode <= QK_MODS_MAX) {
      009E95 8E 04            [24] 1222 	mov	ar4,r6
      009E97 8F 05            [24] 1223 	mov	ar5,r7
      009E99 74 FF            [12] 1224 	mov	a,#0x100 - 0x01
      009E9B 2D               [12] 1225 	add	a,r5
      009E9C 50 1E            [24] 1226 	jnc	00115$
      009E9E C3               [12] 1227 	clr	c
      009E9F 74 FF            [12] 1228 	mov	a,#0xff
      009EA1 9C               [12] 1229 	subb	a,r4
      009EA2 74 1F            [12] 1230 	mov	a,#0x1f
      009EA4 9D               [12] 1231 	subb	a,r5
      009EA5 40 15            [24] 1232 	jc	00115$
                                   1233 ;	free result
                                   1234 ;	quantum/repeat_key.c:180: mods |= QK_MODS_GET_MODS(keycode);
      009EA7 8F 06            [24] 1235 	mov	ar6,r7
      009EA9 53 06 1F         [24] 1236 	anl	ar6,#0x1f
      009EAC 90 0A 3E         [24] 1237 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009EAF E0               [24] 1238 	movx	a,@dptr
      009EB0 4E               [12] 1239 	orl	a,r6
      009EB1 F0               [24] 1240 	movx	@dptr,a
                                   1241 ;	quantum/repeat_key.c:181: keycode = QK_MODS_GET_BASIC_KEYCODE(keycode);
      009EB2 7D 00            [12] 1242 	mov	r5,#0x00
      009EB4 90 0A 3C         [24] 1243 	mov	dptr,#_get_alt_repeat_key_keycode_keycode_10000_204
      009EB7 EC               [12] 1244 	mov	a,r4
      009EB8 F0               [24] 1245 	movx	@dptr,a
      009EB9 ED               [12] 1246 	mov	a,r5
      009EBA A3               [24] 1247 	inc	dptr
      009EBB F0               [24] 1248 	movx	@dptr,a
                                   1249 ;	quantum/repeat_key.c:197: if (IS_QK_BASIC(keycode)) {
      009EBC                       1250 00115$:
      009EBC 90 0A 3C         [24] 1251 	mov	dptr,#_get_alt_repeat_key_keycode_keycode_10000_204
      009EBF 12 86 27         [24] 1252 	lcall	_ak820_outline_0012
      009EC2 C3               [12] 1253 	clr	c
      009EC3 74 FF            [12] 1254 	mov	a,#0xff
      009EC5 9C               [12] 1255 	subb	a,r4
      009EC6 E4               [12] 1256 	clr	a
      009EC7 9D               [12] 1257 	subb	a,r5
      009EC8 50 03            [24] 1258 	jnc	00180$
      009ECA 02 9F 68         [24] 1259 	ljmp	00114$
      009ECD                       1260 00180$:
                                   1261 ;	free result
                                   1262 ;	quantum/repeat_key.c:198: if ((mods & (MOD_LCTL | MOD_LALT | MOD_LGUI))) {
      009ECD 90 0A 3E         [24] 1263 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009ED0 E0               [24] 1264 	movx	a,@dptr
      009ED1 54 0D            [12] 1265 	anl	a,#0x0d
      009ED3 60 22            [24] 1266 	jz	00107$
                                   1267 ;	quantum/repeat_key.c:213: alt_keycode = find_alt_keycode(pairs, sizeof(pairs), keycode);
      009ED5 8E 05            [24] 1268 	mov	ar5,r6
      009ED7 90 0A 37         [24] 1269 	mov	dptr,#_find_alt_keycode_PARM_2
      009EDA 74 0A            [12] 1270 	mov	a,#0x0a
      009EDC F0               [24] 1271 	movx	@dptr,a
      009EDD 90 0A 38         [24] 1272 	mov	dptr,#_find_alt_keycode_PARM_3
      009EE0 ED               [12] 1273 	mov	a,r5
      009EE1 F0               [24] 1274 	movx	@dptr,a
      009EE2 90 B9 58         [24] 1275 	mov	dptr,#_get_alt_repeat_key_keycode_pairs_50000_212
      009EE5 75 F0 80         [24] 1276 	mov	b, #0x80
      009EE8 12 9D CB         [24] 1277 	lcall	_find_alt_keycode
      009EEB AD 82            [24] 1278 	mov	r5, dpl
      009EED 90 0A 3F         [24] 1279 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009EF0 ED               [12] 1280 	mov	a,r5
      009EF1 F0               [24] 1281 	movx	@dptr,a
      009EF2 E4               [12] 1282 	clr	a
      009EF3 A3               [24] 1283 	inc	dptr
      009EF4 F0               [24] 1284 	movx	@dptr,a
      009EF5 80 1E            [24] 1285 	sjmp	00108$
      009EF7                       1286 00107$:
                                   1287 ;	quantum/repeat_key.c:226: alt_keycode = find_alt_keycode(pairs, sizeof(pairs), keycode);
      009EF7 90 0A 37         [24] 1288 	mov	dptr,#_find_alt_keycode_PARM_2
      009EFA 74 08            [12] 1289 	mov	a,#0x08
      009EFC F0               [24] 1290 	movx	@dptr,a
      009EFD 90 0A 38         [24] 1291 	mov	dptr,#_find_alt_keycode_PARM_3
      009F00 EE               [12] 1292 	mov	a,r6
      009F01 F0               [24] 1293 	movx	@dptr,a
      009F02 90 B9 62         [24] 1294 	mov	dptr,#_get_alt_repeat_key_keycode_pairs_50000_213
      009F05 75 F0 80         [24] 1295 	mov	b, #0x80
      009F08 12 9D CB         [24] 1296 	lcall	_find_alt_keycode
      009F0B AF 82            [24] 1297 	mov	r7, dpl
      009F0D 90 0A 3F         [24] 1298 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009F10 EF               [12] 1299 	mov	a,r7
      009F11 F0               [24] 1300 	movx	@dptr,a
      009F12 E4               [12] 1301 	clr	a
      009F13 A3               [24] 1302 	inc	dptr
      009F14 F0               [24] 1303 	movx	@dptr,a
      009F15                       1304 00108$:
                                   1305 ;	quantum/repeat_key.c:229: if (!alt_keycode) {
      009F15 90 0A 3F         [24] 1306 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009F18 E0               [24] 1307 	movx	a,@dptr
      009F19 F5 F0            [12] 1308 	mov	b,a
      009F1B A3               [24] 1309 	inc	dptr
      009F1C E0               [24] 1310 	movx	a,@dptr
      009F1D 45 F0            [12] 1311 	orl	a,b
      009F1F 70 23            [24] 1312 	jnz	00110$
                                   1313 ;	quantum/repeat_key.c:254: alt_keycode = find_alt_keycode(pairs, sizeof(pairs), keycode);
      009F21 90 0A 3C         [24] 1314 	mov	dptr,#_get_alt_repeat_key_keycode_keycode_10000_204
      009F24 E0               [24] 1315 	movx	a,@dptr
      009F25 FF               [12] 1316 	mov	r7,a
      009F26 90 0A 37         [24] 1317 	mov	dptr,#_find_alt_keycode_PARM_2
      009F29 74 16            [12] 1318 	mov	a,#0x16
      009F2B F0               [24] 1319 	movx	@dptr,a
      009F2C 90 0A 38         [24] 1320 	mov	dptr,#_find_alt_keycode_PARM_3
      009F2F EF               [12] 1321 	mov	a,r7
      009F30 F0               [24] 1322 	movx	@dptr,a
      009F31 90 B9 6A         [24] 1323 	mov	dptr,#_get_alt_repeat_key_keycode_pairs_50000_215
      009F34 75 F0 80         [24] 1324 	mov	b, #0x80
      009F37 12 9D CB         [24] 1325 	lcall	_find_alt_keycode
      009F3A AF 82            [24] 1326 	mov	r7, dpl
      009F3C 90 0A 3F         [24] 1327 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009F3F EF               [12] 1328 	mov	a,r7
      009F40 F0               [24] 1329 	movx	@dptr,a
      009F41 E4               [12] 1330 	clr	a
      009F42 A3               [24] 1331 	inc	dptr
      009F43 F0               [24] 1332 	movx	@dptr,a
      009F44                       1333 00110$:
                                   1334 ;	quantum/repeat_key.c:257: if (alt_keycode) {
      009F44 90 0A 3F         [24] 1335 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009F47 E0               [24] 1336 	movx	a,@dptr
      009F48 FE               [12] 1337 	mov	r6,a
      009F49 A3               [24] 1338 	inc	dptr
      009F4A E0               [24] 1339 	movx	a,@dptr
      009F4B FF               [12] 1340 	mov	r7,a
      009F4C 90 0A 3F         [24] 1341 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009F4F E0               [24] 1342 	movx	a,@dptr
      009F50 F5 F0            [12] 1343 	mov	b,a
      009F52 A3               [24] 1344 	inc	dptr
      009F53 E0               [24] 1345 	movx	a,@dptr
      009F54 45 F0            [12] 1346 	orl	a,b
      009F56 60 10            [24] 1347 	jz	00114$
                                   1348 ;	quantum/repeat_key.c:259: return (mods << 8) | alt_keycode;
      009F58 90 0A 3E         [24] 1349 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009F5B E0               [24] 1350 	movx	a,@dptr
      009F5C FD               [12] 1351 	mov	r5,a
      009F5D E4               [12] 1352 	clr	a
      009F5E 42 06            [12] 1353 	orl	ar6,a
      009F60 ED               [12] 1354 	mov	a,r5
      009F61 42 07            [12] 1355 	orl	ar7,a
      009F63 8E 82            [24] 1356 	mov	dpl, r6
      009F65 8F 83            [24] 1357 	mov	dph, r7
      009F67 22               [24] 1358 	ret
      009F68                       1359 00114$:
                                   1360 ;	quantum/repeat_key.c:263: return KC_NO; // No alternate key found.
      009F68 90 00 00         [24] 1361 	mov	dptr,#0x0000
                                   1362 ;	quantum/repeat_key.c:264: }
      009F6B 22               [24] 1363 	ret
                                   1364 ;------------------------------------------------------------
                                   1365 ;Allocation info for local variables in function 'alt_repeat_key_invoke'
                                   1366 ;------------------------------------------------------------
                                   1367 ;event         Allocated with name '_alt_repeat_key_invoke_event_10000_218'
                                   1368 ;------------------------------------------------------------
                                   1369 ;	quantum/repeat_key.c:266: void alt_repeat_key_invoke(const keyevent_t* event) {
                                   1370 ;	-----------------------------------------
                                   1371 ;	 function alt_repeat_key_invoke
                                   1372 ;	-----------------------------------------
      009F6C                       1373 _alt_repeat_key_invoke:
      009F6C AF F0            [24] 1374 	mov	r7,b
      009F6E AE 83            [24] 1375 	mov	r6,dph
      009F70 E5 82            [12] 1376 	mov	a,dpl
      009F72 90 0A 41         [24] 1377 	mov	dptr,#_alt_repeat_key_invoke_event_10000_218
      009F75 F0               [24] 1378 	movx	@dptr,a
      009F76 EE               [12] 1379 	mov	a,r6
      009F77 A3               [24] 1380 	inc	dptr
      009F78 F0               [24] 1381 	movx	@dptr,a
      009F79 EF               [12] 1382 	mov	a,r7
      009F7A A3               [24] 1383 	inc	dptr
      009F7B F0               [24] 1384 	movx	@dptr,a
                                   1385 ;	quantum/repeat_key.c:268: repeat_invoke(event, true);
      009F7C 90 0A 41         [24] 1386 	mov	dptr,#_alt_repeat_key_invoke_event_10000_218
      009F7F 12 73 B8         [24] 1387 	lcall	_ak820_outline_0002
      009F82 90 0A 30         [24] 1388 	mov	dptr,#_repeat_invoke_PARM_2
      009F85 74 01            [12] 1389 	mov	a,#0x01
      009F87 F0               [24] 1390 	movx	@dptr,a
      009F88 8D 82            [24] 1391 	mov	dpl, r5
      009F8A 8E 83            [24] 1392 	mov	dph, r6
      009F8C 8F F0            [24] 1393 	mov	b, r7
                                   1394 ;	quantum/repeat_key.c:269: }
      009F8E 02 9C 80         [24] 1395 	ljmp	_repeat_invoke
                                   1396 ;------------------------------------------------------------
                                   1397 ;Allocation info for local variables in function 'get_alt_repeat_key_keycode_user'
                                   1398 ;------------------------------------------------------------
                                   1399 ;mods          Allocated with name '_get_alt_repeat_key_keycode_user_PARM_2'
                                   1400 ;keycode       Allocated with name '_get_alt_repeat_key_keycode_user_keycode_10000_220'
                                   1401 ;------------------------------------------------------------
                                   1402 ;	quantum/repeat_key.c:272: __attribute__((weak)) uint16_t get_alt_repeat_key_keycode_user(uint16_t keycode, uint8_t mods) {
                                   1403 ;	-----------------------------------------
                                   1404 ;	 function get_alt_repeat_key_keycode_user
                                   1405 ;	-----------------------------------------
      009F91                       1406 _get_alt_repeat_key_keycode_user:
                                   1407 ;	quantum/repeat_key.c:273: return KC_TRANSPARENT;
      009F91 90 00 01         [24] 1408 	mov	dptr,#0x0001
                                   1409 ;	quantum/repeat_key.c:274: }
      009F94 22               [24] 1410 	ret
                                   1411 	.area CSEG    (CODE)
                                   1412 	.area CONST   (CODE)
                                   1413 	.area CONST   (CODE)
      00B958                       1414 _get_alt_repeat_key_keycode_pairs_50000_212:
      00B958 09                    1415 	.db #0x09	; 9
      00B959 05                    1416 	.db #0x05	; 5
      00B95A 07                    1417 	.db #0x07	; 7
      00B95B 18                    1418 	.db #0x18	; 24
      00B95C 11                    1419 	.db #0x11	; 17
      00B95D 13                    1420 	.db #0x13	; 19
      00B95E 04                    1421 	.db #0x04	; 4
      00B95F 08                    1422 	.db #0x08	; 8
      00B960 12                    1423 	.db #0x12	; 18
      00B961 0C                    1424 	.db #0x0c	; 12
                                   1425 	.area CSEG    (CODE)
                                   1426 	.area CONST   (CODE)
      00B962                       1427 _get_alt_repeat_key_keycode_pairs_50000_213:
      00B962 0D                    1428 	.db #0x0d	; 13
      00B963 0E                    1429 	.db #0x0e	; 14
      00B964 0B                    1430 	.db #0x0b	; 11
      00B965 0F                    1431 	.db #0x0f	; 15
      00B966 1A                    1432 	.db #0x1a	; 26
      00B967 05                    1433 	.db #0x05	; 5
      00B968 08                    1434 	.db #0x08	; 8
      00B969 05                    1435 	.db #0x05	; 5
                                   1436 	.area CSEG    (CODE)
                                   1437 	.area CONST   (CODE)
      00B96A                       1438 _get_alt_repeat_key_keycode_pairs_50000_215:
      00B96A 50                    1439 	.db #0x50	; 80	'P'
      00B96B 4F                    1440 	.db #0x4f	; 79	'O'
      00B96C 52                    1441 	.db #0x52	; 82	'R'
      00B96D 51                    1442 	.db #0x51	; 81	'Q'
      00B96E 4A                    1443 	.db #0x4a	; 74	'J'
      00B96F 4D                    1444 	.db #0x4d	; 77	'M'
      00B970 4B                    1445 	.db #0x4b	; 75	'K'
      00B971 4E                    1446 	.db #0x4e	; 78	'N'
      00B972 2A                    1447 	.db #0x2a	; 42
      00B973 4C                    1448 	.db #0x4c	; 76	'L'
      00B974 2F                    1449 	.db #0x2f	; 47
      00B975 30                    1450 	.db #0x30	; 48	'0'
      00B976 B6                    1451 	.db #0xb6	; 182
      00B977 B7                    1452 	.db #0xb7	; 183
      00B978 AB                    1453 	.db #0xab	; 171
      00B979 AC                    1454 	.db #0xac	; 172
      00B97A BB                    1455 	.db #0xbb	; 187
      00B97B BC                    1456 	.db #0xbc	; 188
      00B97C A9                    1457 	.db #0xa9	; 169
      00B97D AA                    1458 	.db #0xaa	; 170
      00B97E BD                    1459 	.db #0xbd	; 189
      00B97F BE                    1460 	.db #0xbe	; 190
                                   1461 	.area CSEG    (CODE)
                                   1462 	.area XINIT   (CODE)
      00BDE2                       1463 __xinit__last_mods:
      00BDE2 00                    1464 	.db #0x00	; 0
      00BDE3                       1465 __xinit__last_repeat_count:
      00BDE3 00                    1466 	.db #0x00	;  0
      00BDE4                       1467 __xinit__processing_repeat_count:
      00BDE4 00                    1468 	.db #0x00	;  0
                                   1469 	.area CABS    (ABS,CODE)
                                   1470 
                                   1471 ; Experimental exact instruction outlining.
                                   1472 	.globl _ak820_outline_0002
                                   1473 	.globl _ak820_outline_0009
                                   1474 	.globl _ak820_outline_0012
                                   1475 	.globl _ak820_outline_0015
