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
      000A16                        557 _last_record:
      000A16                        558 	.ds 8
      000A1E                        559 _registered_record:
      000A1E                        560 	.ds 8
      000A26                        561 _registered_repeat_count:
      000A26                        562 	.ds 1
      000A27                        563 _registered_mods:
      000A27                        564 	.ds 1
      000A28                        565 _set_last_mods_mods_10000_169:
      000A28                        566 	.ds 1
      000A29                        567 _set_last_record_PARM_2:
      000A29                        568 	.ds 3
      000A2C                        569 _set_last_record_keycode_10000_171:
      000A2C                        570 	.ds 2
      000A2E                        571 _update_last_repeat_count_dir_10000_173:
      000A2E                        572 	.ds 1
      000A2F                        573 _repeat_invoke_PARM_2:
      000A2F                        574 	.ds 1
      000A30                        575 _repeat_invoke_event_10000_181:
      000A30                        576 	.ds 3
      000A33                        577 _repeat_key_invoke_event_10000_195:
      000A33                        578 	.ds 3
      000A36                        579 _find_alt_keycode_PARM_2:
      000A36                        580 	.ds 1
      000A37                        581 _find_alt_keycode_PARM_3:
      000A37                        582 	.ds 1
      000A38                        583 _find_alt_keycode_table_10000_197:
      000A38                        584 	.ds 3
      000A3B                        585 _get_alt_repeat_key_keycode_keycode_10000_204:
      000A3B                        586 	.ds 2
      000A3D                        587 _get_alt_repeat_key_keycode_mods_10000_204:
      000A3D                        588 	.ds 1
      000A3E                        589 _get_alt_repeat_key_keycode_alt_keycode_10000_204:
      000A3E                        590 	.ds 2
      000A40                        591 _alt_repeat_key_invoke_event_10000_218:
      000A40                        592 	.ds 3
      000A43                        593 _get_alt_repeat_key_keycode_user_PARM_2:
      000A43                        594 	.ds 1
                                    595 ;--------------------------------------------------------
                                    596 ; absolute external ram data
                                    597 ;--------------------------------------------------------
                                    598 	.area XABS    (ABS,XDATA)
                                    599 ;--------------------------------------------------------
                                    600 ; initialized external ram data
                                    601 ;--------------------------------------------------------
                                    602 	.area XISEG   (XDATA)
      000C01                        603 _last_mods:
      000C01                        604 	.ds 1
      000C02                        605 _last_repeat_count:
      000C02                        606 	.ds 1
      000C03                        607 _processing_repeat_count:
      000C03                        608 	.ds 1
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
      009BBC                        642 _repeat_key_cancel:
                           000007   643 	ar7 = 0x07
                           000006   644 	ar6 = 0x06
                           000005   645 	ar5 = 0x05
                           000004   646 	ar4 = 0x04
                           000003   647 	ar3 = 0x03
                           000002   648 	ar2 = 0x02
                           000001   649 	ar1 = 0x01
                           000000   650 	ar0 = 0x00
                                    651 ;	quantum/repeat_key.c:37: registered_record.keycode = 0;
      009BBC 90 0A 24         [24]  652 	mov	dptr,#(_registered_record + 0x0006)
      009BBF E4               [12]  653 	clr	a
      009BC0 F0               [24]  654 	movx	@dptr,a
      009BC1 A3               [24]  655 	inc	dptr
      009BC2 F0               [24]  656 	movx	@dptr,a
                                    657 ;	quantum/repeat_key.c:38: }
      009BC3 22               [24]  658 	ret
                                    659 ;------------------------------------------------------------
                                    660 ;Allocation info for local variables in function 'get_last_keycode'
                                    661 ;------------------------------------------------------------
                                    662 ;	quantum/repeat_key.c:40: uint16_t get_last_keycode(void) {
                                    663 ;	-----------------------------------------
                                    664 ;	 function set_last_mods
                                    665 ;	-----------------------------------------
      009BC4                        666 _set_last_mods:
      009BC4 E5 82            [12]  667 	mov	a,dpl
      009BC6 90 0A 28         [24]  668 	mov	dptr,#_set_last_mods_mods_10000_169
      009BC9 F0               [24]  669 	movx	@dptr,a
                                    670 ;	quantum/repeat_key.c:58: last_mods = mods;
      009BCA E0               [24]  671 	movx	a,@dptr
      009BCB 90 0C 01         [24]  672 	mov	dptr,#_last_mods
      009BCE F0               [24]  673 	movx	@dptr,a
                                    674 ;	quantum/repeat_key.c:59: }
      009BCF 22               [24]  675 	ret
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
      009BD0                        686 _set_last_record:
      009BD0 AF 83            [24]  687 	mov	r7,dph
      009BD2 E5 82            [12]  688 	mov	a,dpl
      009BD4 90 0A 2C         [24]  689 	mov	dptr,#_set_last_record_keycode_10000_171
      009BD7 F0               [24]  690 	movx	@dptr,a
      009BD8 EF               [12]  691 	mov	a,r7
      009BD9 A3               [24]  692 	inc	dptr
      009BDA F0               [24]  693 	movx	@dptr,a
                                    694 ;	quantum/repeat_key.c:62: last_record         = *record;
      009BDB 90 0A 29         [24]  695 	mov	dptr,#_set_last_record_PARM_2
      009BDE 12 73 99         [24]  696 	lcall	_ak820_outline_0002
      009BE1 90 0B 8F         [24]  697 	mov	dptr,#___memcpy_PARM_2
      009BE4 12 73 BA         [24]  698 	lcall	_ak820_outline_0015
      009BE7 90 0B 92         [24]  699 	mov	dptr,#___memcpy_PARM_3
      009BEA 74 08            [12]  700 	mov	a,#0x08
      009BEC F0               [24]  701 	movx	@dptr,a
      009BED E4               [12]  702 	clr	a
      009BEE A3               [24]  703 	inc	dptr
      009BEF F0               [24]  704 	movx	@dptr,a
      009BF0 90 0A 16         [24]  705 	mov	dptr,#_last_record
      009BF3 F5 F0            [12]  706 	mov	b,a
      009BF5 12 B4 9F         [24]  707 	lcall	___memcpy
                                    708 ;	quantum/repeat_key.c:63: last_record.keycode = keycode;
      009BF8 90 0A 2C         [24]  709 	mov	dptr,#_set_last_record_keycode_10000_171
      009BFB E0               [24]  710 	movx	a,@dptr
      009BFC FE               [12]  711 	mov	r6,a
      009BFD A3               [24]  712 	inc	dptr
      009BFE E0               [24]  713 	movx	a,@dptr
      009BFF FF               [12]  714 	mov	r7,a
      009C00 90 0A 1C         [24]  715 	mov	dptr,#(_last_record + 0x0006)
      009C03 EE               [12]  716 	mov	a,r6
      009C04 F0               [24]  717 	movx	@dptr,a
      009C05 EF               [12]  718 	mov	a,r7
      009C06 A3               [24]  719 	inc	dptr
      009C07 F0               [24]  720 	movx	@dptr,a
                                    721 ;	quantum/repeat_key.c:64: last_repeat_count   = 0;
      009C08 90 0C 02         [24]  722 	mov	dptr,#_last_repeat_count
      009C0B E4               [12]  723 	clr	a
      009C0C F0               [24]  724 	movx	@dptr,a
                                    725 ;	quantum/repeat_key.c:65: }
      009C0D 22               [24]  726 	ret
                                    727 ;------------------------------------------------------------
                                    728 ;Allocation info for local variables in function 'update_last_repeat_count'
                                    729 ;------------------------------------------------------------
                                    730 ;dir           Allocated with name '_update_last_repeat_count_dir_10000_173'
                                    731 ;------------------------------------------------------------
                                    732 ;	quantum/repeat_key.c:68: static void update_last_repeat_count(int8_t dir) {
                                    733 ;	-----------------------------------------
                                    734 ;	 function update_last_repeat_count
                                    735 ;	-----------------------------------------
      009C0E                        736 _update_last_repeat_count:
      009C0E E5 82            [12]  737 	mov	a,dpl
      009C10 90 0A 2E         [24]  738 	mov	dptr,#_update_last_repeat_count_dir_10000_173
      009C13 F0               [24]  739 	movx	@dptr,a
                                    740 ;	quantum/repeat_key.c:69: if ((dir < 0) != (last_repeat_count < 0)) {
      009C14 E0               [24]  741 	movx	a,@dptr
      009C15 FF               [12]  742 	mov	r7,a
      009C16 33               [12]  743 	rlc	a
      009C17 E4               [12]  744 	clr	a
      009C18 33               [12]  745 	rlc	a
      009C19 FE               [12]  746 	mov	r6,a
      009C1A 90 0C 02         [24]  747 	mov	dptr,#_last_repeat_count
      009C1D E0               [24]  748 	movx	a,@dptr
      009C1E FD               [12]  749 	mov	r5,a
      009C1F 33               [12]  750 	rlc	a
      009C20 E4               [12]  751 	clr	a
      009C21 33               [12]  752 	rlc	a
      009C22 FC               [12]  753 	mov	r4,a
      009C23 EE               [12]  754 	mov	a,r6
      009C24 B5 04 02         [24]  755 	cjne	a,ar4,00131$
      009C27 80 06            [24]  756 	sjmp	00104$
      009C29                        757 00131$:
                                    758 ;	quantum/repeat_key.c:70: last_repeat_count = dir;
      009C29 90 0C 02         [24]  759 	mov	dptr,#_last_repeat_count
      009C2C EF               [12]  760 	mov	a,r7
      009C2D F0               [24]  761 	movx	@dptr,a
      009C2E 22               [24]  762 	ret
      009C2F                        763 00104$:
                                    764 ;	quantum/repeat_key.c:71: } else if (dir < 0 ? last_repeat_count > -127 : last_repeat_count < 127) {
      009C2F EE               [12]  765 	mov	a,r6
      009C30 60 0F            [24]  766 	jz	00108$
      009C32 C3               [12]  767 	clr	c
      009C33 74 01            [12]  768 	mov	a,#(0x81 ^ 0x80)
      009C35 8D F0            [24]  769 	mov	b,r5
      009C37 63 F0 80         [24]  770 	xrl	b,#0x80
      009C3A 95 F0            [12]  771 	subb	a,b
      009C3C E4               [12]  772 	clr	a
      009C3D 33               [12]  773 	rlc	a
      009C3E FF               [12]  774 	mov	r7,a
                                    775 ;	free result
      009C3F 80 09            [24]  776 	sjmp	00109$
      009C41                        777 00108$:
      009C41 C3               [12]  778 	clr	c
      009C42 ED               [12]  779 	mov	a,r5
      009C43 64 80            [12]  780 	xrl	a,#0x80
      009C45 94 FF            [12]  781 	subb	a,#0xff
      009C47 E4               [12]  782 	clr	a
      009C48 33               [12]  783 	rlc	a
      009C49 FF               [12]  784 	mov	r7,a
      009C4A                        785 00109$:
      009C4A EF               [12]  786 	mov	a,r7
      009C4B 60 09            [24]  787 	jz	00106$
                                    788 ;	quantum/repeat_key.c:72: last_repeat_count += dir;
      009C4D 90 0A 2E         [24]  789 	mov	dptr,#_update_last_repeat_count_dir_10000_173
      009C50 E0               [24]  790 	movx	a,@dptr
      009C51 90 0C 02         [24]  791 	mov	dptr,#_last_repeat_count
      009C54 2D               [12]  792 	add	a, r5
      009C55 F0               [24]  793 	movx	@dptr,a
      009C56                        794 00106$:
                                    795 ;	quantum/repeat_key.c:74: }
      009C56 22               [24]  796 	ret
                                    797 ;------------------------------------------------------------
                                    798 ;Allocation info for local variables in function 'get_repeat_key_count'
                                    799 ;------------------------------------------------------------
                                    800 ;	quantum/repeat_key.c:76: int8_t get_repeat_key_count(void) {
                                    801 ;	-----------------------------------------
                                    802 ;	 function get_repeat_key_count
                                    803 ;	-----------------------------------------
      009C57                        804 _get_repeat_key_count:
                                    805 ;	quantum/repeat_key.c:77: return processing_repeat_count;
      009C57 90 0C 03         [24]  806 	mov	dptr,#_processing_repeat_count
      009C5A E0               [24]  807 	movx	a,@dptr
                                    808 ;	quantum/repeat_key.c:78: }
      009C5B F5 82            [12]  809 	mov	dpl,a
      009C5D 22               [24]  810 	ret
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
      009C5E                        821 _repeat_invoke:
      009C5E AF F0            [24]  822 	mov	r7,b
      009C60 AE 83            [24]  823 	mov	r6,dph
      009C62 E5 82            [12]  824 	mov	a,dpl
      009C64 90 0A 30         [24]  825 	mov	dptr,#_repeat_invoke_event_10000_181
      009C67 F0               [24]  826 	movx	@dptr,a
      009C68 EE               [12]  827 	mov	a,r6
      009C69 A3               [24]  828 	inc	dptr
      009C6A F0               [24]  829 	movx	@dptr,a
      009C6B EF               [12]  830 	mov	a,r7
      009C6C A3               [24]  831 	inc	dptr
      009C6D F0               [24]  832 	movx	@dptr,a
                                    833 ;	quantum/repeat_key.c:88: if (processing_repeat_count) {
      009C6E 90 0C 03         [24]  834 	mov	dptr,#_processing_repeat_count
      009C71 E0               [24]  835 	movx	a,@dptr
      009C72 60 01            [24]  836 	jz	00102$
                                    837 ;	quantum/repeat_key.c:89: return;
      009C74 22               [24]  838 	ret
      009C75                        839 00102$:
                                    840 ;	quantum/repeat_key.c:92: if (event->pressed) {
      009C75 90 0A 30         [24]  841 	mov	dptr,#_repeat_invoke_event_10000_181
      009C78 12 73 99         [24]  842 	lcall	_ak820_outline_0002
      009C7B 74 05            [12]  843 	mov	a,#0x05
      009C7D 12 73 A2         [24]  844 	lcall	_ak820_outline_0009
      009C80 12 B5 78         [24]  845 	lcall	__gptrget
      009C83 70 03            [24]  846 	jnz	00187$
      009C85 02 9D 09         [24]  847 	ljmp	00115$
      009C88                        848 00187$:
                                    849 ;	quantum/repeat_key.c:95: if (registered_record.keycode || !last_record.keycode) return;
      009C88 90 0A 24         [24]  850 	mov	dptr,#(_registered_record + 0x0006)
      009C8B E0               [24]  851 	movx	a,@dptr
      009C8C FB               [12]  852 	mov	r3,a
      009C8D A3               [24]  853 	inc	dptr
      009C8E E0               [24]  854 	movx	a,@dptr
      009C8F 4B               [12]  855 	orl	a,r3
      009C90 70 0A            [24]  856 	jnz	00103$
      009C92 90 0A 1C         [24]  857 	mov	dptr,#(_last_record + 0x0006)
      009C95 E0               [24]  858 	movx	a,@dptr
      009C96 FB               [12]  859 	mov	r3,a
      009C97 A3               [24]  860 	inc	dptr
      009C98 E0               [24]  861 	movx	a,@dptr
      009C99 4B               [12]  862 	orl	a,r3
      009C9A 70 01            [24]  863 	jnz	00104$
      009C9C                        864 00103$:
      009C9C 22               [24]  865 	ret
      009C9D                        866 00104$:
                                    867 ;	quantum/repeat_key.c:96: registered_record = last_record;
      009C9D 90 0B 8F         [24]  868 	mov	dptr,#___memcpy_PARM_2
      009CA0 74 16            [12]  869 	mov	a,#_last_record
      009CA2 F0               [24]  870 	movx	@dptr,a
      009CA3 74 0A            [12]  871 	mov	a,#(_last_record >> 8)
      009CA5 A3               [24]  872 	inc	dptr
      009CA6 F0               [24]  873 	movx	@dptr,a
      009CA7 E4               [12]  874 	clr	a
      009CA8 A3               [24]  875 	inc	dptr
      009CA9 F0               [24]  876 	movx	@dptr,a
      009CAA 90 0B 92         [24]  877 	mov	dptr,#___memcpy_PARM_3
      009CAD 74 08            [12]  878 	mov	a,#0x08
      009CAF F0               [24]  879 	movx	@dptr,a
      009CB0 E4               [12]  880 	clr	a
      009CB1 A3               [24]  881 	inc	dptr
      009CB2 F0               [24]  882 	movx	@dptr,a
      009CB3 90 0A 1E         [24]  883 	mov	dptr,#_registered_record
      009CB6 F5 F0            [12]  884 	mov	b,a
      009CB8 12 B4 9F         [24]  885 	lcall	___memcpy
                                    886 ;	quantum/repeat_key.c:97: registered_mods = last_mods;
      009CBB 90 0C 01         [24]  887 	mov	dptr,#_last_mods
      009CBE E0               [24]  888 	movx	a,@dptr
      009CBF 90 0A 27         [24]  889 	mov	dptr,#_registered_mods
      009CC2 F0               [24]  890 	movx	@dptr,a
                                    891 ;	quantum/repeat_key.c:99: if (alternate) {
      009CC3 90 0A 2F         [24]  892 	mov	dptr,#_repeat_invoke_PARM_2
      009CC6 E0               [24]  893 	movx	a,@dptr
      009CC7 FC               [12]  894 	mov	r4,a
      009CC8 E0               [24]  895 	movx	a,@dptr
      009CC9 60 1D            [24]  896 	jz	00109$
                                    897 ;	quantum/repeat_key.c:100: registered_record.keycode = get_alt_repeat_key_keycode();
      009CCB C0 04            [24]  898 	push	ar4
      009CCD 12 9E 19         [24]  899 	lcall	_get_alt_repeat_key_keycode
      009CD0 AA 82            [24]  900 	mov	r2, dpl
      009CD2 AB 83            [24]  901 	mov	r3, dph
      009CD4 D0 04            [24]  902 	pop	ar4
      009CD6 90 0A 24         [24]  903 	mov	dptr,#(_registered_record + 0x0006)
      009CD9 EA               [12]  904 	mov	a,r2
      009CDA F0               [24]  905 	movx	@dptr,a
      009CDB EB               [12]  906 	mov	a,r3
      009CDC A3               [24]  907 	inc	dptr
      009CDD F0               [24]  908 	movx	@dptr,a
                                    909 ;	quantum/repeat_key.c:101: if (!registered_record.keycode) return;
      009CDE EA               [12]  910 	mov	a,r2
      009CDF 4B               [12]  911 	orl	a,r3
      009CE0 70 01            [24]  912 	jnz	00107$
      009CE2 22               [24]  913 	ret
      009CE3                        914 00107$:
                                    915 ;	quantum/repeat_key.c:103: registered_mods = 0;
      009CE3 90 0A 27         [24]  916 	mov	dptr,#_registered_mods
      009CE6 E4               [12]  917 	clr	a
      009CE7 F0               [24]  918 	movx	@dptr,a
      009CE8                        919 00109$:
                                    920 ;	quantum/repeat_key.c:106: update_last_repeat_count(alternate ? -1 : 1);
      009CE8 EC               [12]  921 	mov	a,r4
      009CE9 60 04            [24]  922 	jz	00121$
      009CEB 7C FF            [12]  923 	mov	r4,#0xff
      009CED 80 02            [24]  924 	sjmp	00122$
      009CEF                        925 00121$:
      009CEF 7C 01            [12]  926 	mov	r4,#0x01
      009CF1                        927 00122$:
      009CF1 8C 82            [24]  928 	mov	dpl, r4
      009CF3 12 9C 0E         [24]  929 	lcall	_update_last_repeat_count
                                    930 ;	quantum/repeat_key.c:107: register_weak_mods(registered_mods);
      009CF6 90 0A 27         [24]  931 	mov	dptr,#_registered_mods
      009CF9 E0               [24]  932 	movx	a,@dptr
      009CFA F5 82            [12]  933 	mov	dpl,a
      009CFC 12 73 4D         [24]  934 	lcall	_register_weak_mods
                                    935 ;	quantum/repeat_key.c:108: registered_repeat_count = last_repeat_count;
      009CFF 90 0C 02         [24]  936 	mov	dptr,#_last_repeat_count
      009D02 E0               [24]  937 	movx	a,@dptr
      009D03 90 0A 26         [24]  938 	mov	dptr,#_registered_repeat_count
      009D06 F0               [24]  939 	movx	@dptr,a
      009D07 80 32            [24]  940 	sjmp	00116$
      009D09                        941 00115$:
                                    942 ;	quantum/repeat_key.c:111: if (!registered_record.keycode || event->key.row != registered_record.event.key.row ||
      009D09 90 0A 24         [24]  943 	mov	dptr,#(_registered_record + 0x0006)
      009D0C E0               [24]  944 	movx	a,@dptr
      009D0D FB               [12]  945 	mov	r3,a
      009D0E A3               [24]  946 	inc	dptr
      009D0F E0               [24]  947 	movx	a,@dptr
      009D10 4B               [12]  948 	orl	a,r3
      009D11 60 27            [24]  949 	jz	00110$
      009D13 74 01            [12]  950 	mov	a,#0x01
      009D15 12 73 A2         [24]  951 	lcall	_ak820_outline_0009
      009D18 12 B5 78         [24]  952 	lcall	__gptrget
      009D1B FA               [12]  953 	mov	r2,a
      009D1C 90 0A 1F         [24]  954 	mov	dptr,#(_registered_record + 0x0001)
      009D1F E0               [24]  955 	movx	a,@dptr
      009D20 FC               [12]  956 	mov	r4,a
      009D21 EA               [12]  957 	mov	a,r2
      009D22 B5 04 15         [24]  958 	cjne	a,ar4,00110$
                                    959 ;	quantum/repeat_key.c:112: event->key.col != registered_record.event.key.col) return;
      009D25 8D 82            [24]  960 	mov	dpl,r5
      009D27 8E 83            [24]  961 	mov	dph,r6
      009D29 8F F0            [24]  962 	mov	b,r7
      009D2B 12 B5 78         [24]  963 	lcall	__gptrget
      009D2E FD               [12]  964 	mov	r5,a
      009D2F 90 0A 1E         [24]  965 	mov	dptr,#_registered_record
      009D32 E0               [24]  966 	movx	a,@dptr
      009D33 FF               [12]  967 	mov	r7,a
      009D34 ED               [12]  968 	mov	a,r5
      009D35 B5 07 02         [24]  969 	cjne	a,ar7,00196$
      009D38 80 01            [24]  970 	sjmp	00116$
      009D3A                        971 00196$:
      009D3A                        972 00110$:
      009D3A 22               [24]  973 	ret
      009D3B                        974 00116$:
                                    975 ;	quantum/repeat_key.c:116: registered_record.event = *event;
      009D3B 90 0A 30         [24]  976 	mov	dptr,#_repeat_invoke_event_10000_181
      009D3E 12 73 99         [24]  977 	lcall	_ak820_outline_0002
      009D41 90 0B 8F         [24]  978 	mov	dptr,#___memcpy_PARM_2
      009D44 12 73 BA         [24]  979 	lcall	_ak820_outline_0015
      009D47 90 0B 92         [24]  980 	mov	dptr,#___memcpy_PARM_3
      009D4A 74 06            [12]  981 	mov	a,#0x06
      009D4C F0               [24]  982 	movx	@dptr,a
      009D4D E4               [12]  983 	clr	a
      009D4E A3               [24]  984 	inc	dptr
      009D4F F0               [24]  985 	movx	@dptr,a
      009D50 90 0A 1E         [24]  986 	mov	dptr,#_registered_record
      009D53 F5 F0            [12]  987 	mov	b,a
      009D55 12 B4 9F         [24]  988 	lcall	___memcpy
                                    989 ;	quantum/repeat_key.c:117: processing_repeat_count = registered_repeat_count;
      009D58 90 0A 26         [24]  990 	mov	dptr,#_registered_repeat_count
      009D5B E0               [24]  991 	movx	a,@dptr
      009D5C 90 0C 03         [24]  992 	mov	dptr,#_processing_repeat_count
      009D5F F0               [24]  993 	movx	@dptr,a
                                    994 ;	quantum/repeat_key.c:118: process_record(&registered_record);
      009D60 90 0A 1E         [24]  995 	mov	dptr,#_registered_record
      009D63 75 F0 00         [24]  996 	mov	b, #0x00
      009D66 12 6D 2C         [24]  997 	lcall	_process_record
                                    998 ;	quantum/repeat_key.c:119: processing_repeat_count = 0;
      009D69 90 0C 03         [24]  999 	mov	dptr,#_processing_repeat_count
      009D6C E4               [12] 1000 	clr	a
      009D6D F0               [24] 1001 	movx	@dptr,a
                                   1002 ;	quantum/repeat_key.c:125: if (!registered_record.event.pressed) {
      009D6E 90 0A 23         [24] 1003 	mov	dptr,#(_registered_record + 0x0005)
      009D71 E0               [24] 1004 	movx	a,@dptr
      009D72 70 10            [24] 1005 	jnz	00119$
                                   1006 ;	quantum/repeat_key.c:126: unregister_weak_mods(registered_mods);
      009D74 90 0A 27         [24] 1007 	mov	dptr,#_registered_mods
      009D77 E0               [24] 1008 	movx	a,@dptr
      009D78 F5 82            [12] 1009 	mov	dpl,a
      009D7A 12 73 61         [24] 1010 	lcall	_unregister_weak_mods
                                   1011 ;	quantum/repeat_key.c:127: registered_record.keycode = 0;
      009D7D 90 0A 24         [24] 1012 	mov	dptr,#(_registered_record + 0x0006)
      009D80 E4               [12] 1013 	clr	a
      009D81 F0               [24] 1014 	movx	@dptr,a
      009D82 A3               [24] 1015 	inc	dptr
      009D83 F0               [24] 1016 	movx	@dptr,a
      009D84                       1017 00119$:
                                   1018 ;	quantum/repeat_key.c:129: }
      009D84 22               [24] 1019 	ret
                                   1020 ;------------------------------------------------------------
                                   1021 ;Allocation info for local variables in function 'repeat_key_invoke'
                                   1022 ;------------------------------------------------------------
                                   1023 ;event         Allocated with name '_repeat_key_invoke_event_10000_195'
                                   1024 ;------------------------------------------------------------
                                   1025 ;	quantum/repeat_key.c:131: void repeat_key_invoke(const keyevent_t* event) {
                                   1026 ;	-----------------------------------------
                                   1027 ;	 function repeat_key_invoke
                                   1028 ;	-----------------------------------------
      009D85                       1029 _repeat_key_invoke:
      009D85 AF F0            [24] 1030 	mov	r7,b
      009D87 AE 83            [24] 1031 	mov	r6,dph
      009D89 E5 82            [12] 1032 	mov	a,dpl
      009D8B 90 0A 33         [24] 1033 	mov	dptr,#_repeat_key_invoke_event_10000_195
      009D8E F0               [24] 1034 	movx	@dptr,a
      009D8F EE               [12] 1035 	mov	a,r6
      009D90 A3               [24] 1036 	inc	dptr
      009D91 F0               [24] 1037 	movx	@dptr,a
      009D92 EF               [12] 1038 	mov	a,r7
      009D93 A3               [24] 1039 	inc	dptr
      009D94 F0               [24] 1040 	movx	@dptr,a
                                   1041 ;	quantum/repeat_key.c:132: repeat_invoke(event, false);
      009D95 90 0A 33         [24] 1042 	mov	dptr,#_repeat_key_invoke_event_10000_195
      009D98 12 73 99         [24] 1043 	lcall	_ak820_outline_0002
      009D9B 90 0A 2F         [24] 1044 	mov	dptr,#_repeat_invoke_PARM_2
      009D9E E4               [12] 1045 	clr	a
      009D9F F0               [24] 1046 	movx	@dptr,a
      009DA0 8D 82            [24] 1047 	mov	dpl, r5
      009DA2 8E 83            [24] 1048 	mov	dph, r6
      009DA4 8F F0            [24] 1049 	mov	b, r7
                                   1050 ;	quantum/repeat_key.c:133: }
      009DA6 02 9C 5E         [24] 1051 	ljmp	_repeat_invoke
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
      009DA9                       1066 _find_alt_keycode:
      009DA9 AF F0            [24] 1067 	mov	r7,b
      009DAB AE 83            [24] 1068 	mov	r6,dph
      009DAD E5 82            [12] 1069 	mov	a,dpl
      009DAF 90 0A 38         [24] 1070 	mov	dptr,#_find_alt_keycode_table_10000_197
      009DB2 F0               [24] 1071 	movx	@dptr,a
      009DB3 EE               [12] 1072 	mov	a,r6
      009DB4 A3               [24] 1073 	inc	dptr
      009DB5 F0               [24] 1074 	movx	@dptr,a
      009DB6 EF               [12] 1075 	mov	a,r7
      009DB7 A3               [24] 1076 	inc	dptr
      009DB8 F0               [24] 1077 	movx	@dptr,a
                                   1078 ;	quantum/repeat_key.c:150: const uint8_t* keycodes = (const uint8_t*)table;
      009DB9 90 0A 38         [24] 1079 	mov	dptr,#_find_alt_keycode_table_10000_197
      009DBC E0               [24] 1080 	movx	a,@dptr
      009DBD F5 5D            [12] 1081 	mov	_find_alt_keycode_sloc0_1_0,a
      009DBF A3               [24] 1082 	inc	dptr
      009DC0 E0               [24] 1083 	movx	a,@dptr
      009DC1 F5 5E            [12] 1084 	mov	(_find_alt_keycode_sloc0_1_0 + 1),a
      009DC3 A3               [24] 1085 	inc	dptr
      009DC4 E0               [24] 1086 	movx	a,@dptr
      009DC5 F5 5F            [12] 1087 	mov	(_find_alt_keycode_sloc0_1_0 + 2),a
                                   1088 ;	quantum/repeat_key.c:151: for (uint8_t i = 0; i < table_size_bytes; ++i) {
      009DC7 90 0A 37         [24] 1089 	mov	dptr,#_find_alt_keycode_PARM_3
      009DCA E0               [24] 1090 	movx	a,@dptr
      009DCB FC               [12] 1091 	mov	r4,a
      009DCC 90 0A 36         [24] 1092 	mov	dptr,#_find_alt_keycode_PARM_2
      009DCF E0               [24] 1093 	movx	a,@dptr
      009DD0 FB               [12] 1094 	mov	r3,a
      009DD1 7A 00            [12] 1095 	mov	r2,#0x00
      009DD3                       1096 00105$:
      009DD3 C3               [12] 1097 	clr	c
      009DD4 EA               [12] 1098 	mov	a,r2
      009DD5 9B               [12] 1099 	subb	a,r3
      009DD6 50 3D            [24] 1100 	jnc	00103$
                                   1101 ;	quantum/repeat_key.c:152: if (target == pgm_read_byte(keycodes + i)) {
      009DD8 C0 03            [24] 1102 	push	ar3
      009DDA EA               [12] 1103 	mov	a,r2
      009DDB 25 5D            [12] 1104 	add	a, _find_alt_keycode_sloc0_1_0
      009DDD F8               [12] 1105 	mov	r0,a
      009DDE E4               [12] 1106 	clr	a
      009DDF 35 5E            [12] 1107 	addc	a, (_find_alt_keycode_sloc0_1_0 + 1)
      009DE1 F9               [12] 1108 	mov	r1,a
      009DE2 AB 5F            [24] 1109 	mov	r3,(_find_alt_keycode_sloc0_1_0 + 2)
      009DE4 88 82            [24] 1110 	mov	dpl,r0
      009DE6 89 83            [24] 1111 	mov	dph,r1
      009DE8 8B F0            [24] 1112 	mov	b,r3
      009DEA 12 B5 78         [24] 1113 	lcall	__gptrget
      009DED F8               [12] 1114 	mov	r0,a
      009DEE EC               [12] 1115 	mov	a,r4
      009DEF B5 00 02         [24] 1116 	cjne	a,ar0,00131$
      009DF2 80 04            [24] 1117 	sjmp	00132$
      009DF4                       1118 00131$:
      009DF4 D0 03            [24] 1119 	pop	ar3
      009DF6 80 1A            [24] 1120 	sjmp	00106$
      009DF8                       1121 00132$:
      009DF8 D0 03            [24] 1122 	pop	ar3
                                   1123 ;	quantum/repeat_key.c:154: return pgm_read_byte(keycodes + (i ^ 1));
      009DFA 74 01            [12] 1124 	mov	a,#0x01
      009DFC 6A               [12] 1125 	xrl	a,r2
      009DFD 25 5D            [12] 1126 	add	a, _find_alt_keycode_sloc0_1_0
      009DFF F8               [12] 1127 	mov	r0,a
      009E00 E4               [12] 1128 	clr	a
      009E01 35 5E            [12] 1129 	addc	a,(_find_alt_keycode_sloc0_1_0 + 1)
      009E03 F9               [12] 1130 	mov	r1,a
      009E04 AF 5F            [24] 1131 	mov	r7,(_find_alt_keycode_sloc0_1_0 + 2)
      009E06 88 82            [24] 1132 	mov	dpl,r0
      009E08 89 83            [24] 1133 	mov	dph,r1
      009E0A 8F F0            [24] 1134 	mov	b,r7
      009E0C 12 B5 78         [24] 1135 	lcall	__gptrget
      009E0F F5 82            [12] 1136 	mov	dpl,a
      009E11 22               [24] 1137 	ret
      009E12                       1138 00106$:
                                   1139 ;	quantum/repeat_key.c:151: for (uint8_t i = 0; i < table_size_bytes; ++i) {
      009E12 0A               [12] 1140 	inc	r2
      009E13 80 BE            [24] 1141 	sjmp	00105$
      009E15                       1142 00103$:
                                   1143 ;	quantum/repeat_key.c:157: return KC_NO;
      009E15 75 82 00         [24] 1144 	mov	dpl, #0x00
                                   1145 ;	quantum/repeat_key.c:158: }
      009E18 22               [24] 1146 	ret
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
      009E19                       1158 _get_alt_repeat_key_keycode:
                                   1159 ;	quantum/repeat_key.c:161: uint16_t keycode = last_record.keycode;
      009E19 90 0A 1C         [24] 1160 	mov	dptr,#(_last_record + 0x0006)
      009E1C E0               [24] 1161 	movx	a,@dptr
      009E1D FE               [12] 1162 	mov	r6,a
      009E1E A3               [24] 1163 	inc	dptr
      009E1F E0               [24] 1164 	movx	a,@dptr
      009E20 FF               [12] 1165 	mov	r7,a
      009E21 90 0A 3B         [24] 1166 	mov	dptr,#_get_alt_repeat_key_keycode_keycode_10000_204
      009E24 EE               [12] 1167 	mov	a,r6
      009E25 F0               [24] 1168 	movx	@dptr,a
      009E26 EF               [12] 1169 	mov	a,r7
      009E27 A3               [24] 1170 	inc	dptr
      009E28 F0               [24] 1171 	movx	@dptr,a
                                   1172 ;	quantum/repeat_key.c:162: uint8_t  mods    = last_mods;
      009E29 90 0C 01         [24] 1173 	mov	dptr,#_last_mods
      009E2C E0               [24] 1174 	movx	a,@dptr
      009E2D FD               [12] 1175 	mov	r5,a
      009E2E 90 0A 3D         [24] 1176 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009E31 F0               [24] 1177 	movx	@dptr,a
                                   1178 ;	quantum/repeat_key.c:166: uint16_t alt_keycode = get_alt_repeat_key_keycode_user(keycode, mods);
      009E32 90 0A 43         [24] 1179 	mov	dptr,#_get_alt_repeat_key_keycode_user_PARM_2
      009E35 ED               [12] 1180 	mov	a,r5
      009E36 F0               [24] 1181 	movx	@dptr,a
      009E37 8E 82            [24] 1182 	mov	dpl, r6
      009E39 8F 83            [24] 1183 	mov	dph, r7
      009E3B C0 07            [24] 1184 	push	ar7
      009E3D C0 06            [24] 1185 	push	ar6
      009E3F 12 9F 6F         [24] 1186 	lcall	_get_alt_repeat_key_keycode_user
      009E42 AC 82            [24] 1187 	mov	r4, dpl
      009E44 AD 83            [24] 1188 	mov	r5, dph
      009E46 D0 06            [24] 1189 	pop	ar6
      009E48 D0 07            [24] 1190 	pop	ar7
                                   1191 ;	quantum/repeat_key.c:168: if (alt_keycode != KC_TRANSPARENT) {
      009E4A 8C 02            [24] 1192 	mov	ar2,r4
      009E4C 8D 03            [24] 1193 	mov	ar3,r5
      009E4E BA 01 05         [24] 1194 	cjne	r2,#0x01,00176$
      009E51 BB 00 02         [24] 1195 	cjne	r3,#0x00,00176$
      009E54 80 05            [24] 1196 	sjmp	00102$
      009E56                       1197 00176$:
                                   1198 ;	quantum/repeat_key.c:169: return alt_keycode;
      009E56 8C 82            [24] 1199 	mov	dpl, r4
      009E58 8D 83            [24] 1200 	mov	dph, r5
      009E5A 22               [24] 1201 	ret
      009E5B                       1202 00102$:
                                   1203 ;	quantum/repeat_key.c:174: mods = ((mods & 0xf0) ? /* set right hand bit */ 0x10 : 0)
      009E5B 90 0A 3D         [24] 1204 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009E5E E0               [24] 1205 	movx	a,@dptr
      009E5F 54 F0            [12] 1206 	anl	a,#0xf0
      009E61 60 02            [24] 1207 	jz	00118$
      009E63 74 10            [12] 1208 	mov	a,#0x10
      009E65                       1209 00118$:
      009E65 FD               [12] 1210 	mov	r5,a
                                   1211 ;	quantum/repeat_key.c:176: | (((mods >> 4) | mods) & 0xf);
      009E66 90 0A 3D         [24] 1212 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009E69 E0               [24] 1213 	movx	a,@dptr
      009E6A FC               [12] 1214 	mov	r4,a
      009E6B C4               [12] 1215 	swap	a
      009E6C 54 0F            [12] 1216 	anl	a,#0x0f
      009E6E 4C               [12] 1217 	orl	a,r4
      009E6F 54 0F            [12] 1218 	anl	a,#0x0f
      009E71 4D               [12] 1219 	orl	a,r5
      009E72 F0               [24] 1220 	movx	@dptr,a
                                   1221 ;	quantum/repeat_key.c:179: if (keycode >= QK_MODS && keycode <= QK_MODS_MAX) {
      009E73 8E 04            [24] 1222 	mov	ar4,r6
      009E75 8F 05            [24] 1223 	mov	ar5,r7
      009E77 74 FF            [12] 1224 	mov	a,#0x100 - 0x01
      009E79 2D               [12] 1225 	add	a,r5
      009E7A 50 1E            [24] 1226 	jnc	00115$
      009E7C C3               [12] 1227 	clr	c
      009E7D 74 FF            [12] 1228 	mov	a,#0xff
      009E7F 9C               [12] 1229 	subb	a,r4
      009E80 74 1F            [12] 1230 	mov	a,#0x1f
      009E82 9D               [12] 1231 	subb	a,r5
      009E83 40 15            [24] 1232 	jc	00115$
                                   1233 ;	free result
                                   1234 ;	quantum/repeat_key.c:180: mods |= QK_MODS_GET_MODS(keycode);
      009E85 8F 06            [24] 1235 	mov	ar6,r7
      009E87 53 06 1F         [24] 1236 	anl	ar6,#0x1f
      009E8A 90 0A 3D         [24] 1237 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009E8D E0               [24] 1238 	movx	a,@dptr
      009E8E 4E               [12] 1239 	orl	a,r6
      009E8F F0               [24] 1240 	movx	@dptr,a
                                   1241 ;	quantum/repeat_key.c:181: keycode = QK_MODS_GET_BASIC_KEYCODE(keycode);
      009E90 7D 00            [12] 1242 	mov	r5,#0x00
      009E92 90 0A 3B         [24] 1243 	mov	dptr,#_get_alt_repeat_key_keycode_keycode_10000_204
      009E95 EC               [12] 1244 	mov	a,r4
      009E96 F0               [24] 1245 	movx	@dptr,a
      009E97 ED               [12] 1246 	mov	a,r5
      009E98 A3               [24] 1247 	inc	dptr
      009E99 F0               [24] 1248 	movx	@dptr,a
                                   1249 ;	quantum/repeat_key.c:197: if (IS_QK_BASIC(keycode)) {
      009E9A                       1250 00115$:
      009E9A 90 0A 3B         [24] 1251 	mov	dptr,#_get_alt_repeat_key_keycode_keycode_10000_204
      009E9D 12 86 05         [24] 1252 	lcall	_ak820_outline_0012
      009EA0 C3               [12] 1253 	clr	c
      009EA1 74 FF            [12] 1254 	mov	a,#0xff
      009EA3 9C               [12] 1255 	subb	a,r4
      009EA4 E4               [12] 1256 	clr	a
      009EA5 9D               [12] 1257 	subb	a,r5
      009EA6 50 03            [24] 1258 	jnc	00180$
      009EA8 02 9F 46         [24] 1259 	ljmp	00114$
      009EAB                       1260 00180$:
                                   1261 ;	free result
                                   1262 ;	quantum/repeat_key.c:198: if ((mods & (MOD_LCTL | MOD_LALT | MOD_LGUI))) {
      009EAB 90 0A 3D         [24] 1263 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009EAE E0               [24] 1264 	movx	a,@dptr
      009EAF 54 0D            [12] 1265 	anl	a,#0x0d
      009EB1 60 22            [24] 1266 	jz	00107$
                                   1267 ;	quantum/repeat_key.c:213: alt_keycode = find_alt_keycode(pairs, sizeof(pairs), keycode);
      009EB3 8E 05            [24] 1268 	mov	ar5,r6
      009EB5 90 0A 36         [24] 1269 	mov	dptr,#_find_alt_keycode_PARM_2
      009EB8 74 0A            [12] 1270 	mov	a,#0x0a
      009EBA F0               [24] 1271 	movx	@dptr,a
      009EBB 90 0A 37         [24] 1272 	mov	dptr,#_find_alt_keycode_PARM_3
      009EBE ED               [12] 1273 	mov	a,r5
      009EBF F0               [24] 1274 	movx	@dptr,a
      009EC0 90 B9 36         [24] 1275 	mov	dptr,#_get_alt_repeat_key_keycode_pairs_50000_212
      009EC3 75 F0 80         [24] 1276 	mov	b, #0x80
      009EC6 12 9D A9         [24] 1277 	lcall	_find_alt_keycode
      009EC9 AD 82            [24] 1278 	mov	r5, dpl
      009ECB 90 0A 3E         [24] 1279 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009ECE ED               [12] 1280 	mov	a,r5
      009ECF F0               [24] 1281 	movx	@dptr,a
      009ED0 E4               [12] 1282 	clr	a
      009ED1 A3               [24] 1283 	inc	dptr
      009ED2 F0               [24] 1284 	movx	@dptr,a
      009ED3 80 1E            [24] 1285 	sjmp	00108$
      009ED5                       1286 00107$:
                                   1287 ;	quantum/repeat_key.c:226: alt_keycode = find_alt_keycode(pairs, sizeof(pairs), keycode);
      009ED5 90 0A 36         [24] 1288 	mov	dptr,#_find_alt_keycode_PARM_2
      009ED8 74 08            [12] 1289 	mov	a,#0x08
      009EDA F0               [24] 1290 	movx	@dptr,a
      009EDB 90 0A 37         [24] 1291 	mov	dptr,#_find_alt_keycode_PARM_3
      009EDE EE               [12] 1292 	mov	a,r6
      009EDF F0               [24] 1293 	movx	@dptr,a
      009EE0 90 B9 40         [24] 1294 	mov	dptr,#_get_alt_repeat_key_keycode_pairs_50000_213
      009EE3 75 F0 80         [24] 1295 	mov	b, #0x80
      009EE6 12 9D A9         [24] 1296 	lcall	_find_alt_keycode
      009EE9 AF 82            [24] 1297 	mov	r7, dpl
      009EEB 90 0A 3E         [24] 1298 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009EEE EF               [12] 1299 	mov	a,r7
      009EEF F0               [24] 1300 	movx	@dptr,a
      009EF0 E4               [12] 1301 	clr	a
      009EF1 A3               [24] 1302 	inc	dptr
      009EF2 F0               [24] 1303 	movx	@dptr,a
      009EF3                       1304 00108$:
                                   1305 ;	quantum/repeat_key.c:229: if (!alt_keycode) {
      009EF3 90 0A 3E         [24] 1306 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009EF6 E0               [24] 1307 	movx	a,@dptr
      009EF7 F5 F0            [12] 1308 	mov	b,a
      009EF9 A3               [24] 1309 	inc	dptr
      009EFA E0               [24] 1310 	movx	a,@dptr
      009EFB 45 F0            [12] 1311 	orl	a,b
      009EFD 70 23            [24] 1312 	jnz	00110$
                                   1313 ;	quantum/repeat_key.c:254: alt_keycode = find_alt_keycode(pairs, sizeof(pairs), keycode);
      009EFF 90 0A 3B         [24] 1314 	mov	dptr,#_get_alt_repeat_key_keycode_keycode_10000_204
      009F02 E0               [24] 1315 	movx	a,@dptr
      009F03 FF               [12] 1316 	mov	r7,a
      009F04 90 0A 36         [24] 1317 	mov	dptr,#_find_alt_keycode_PARM_2
      009F07 74 16            [12] 1318 	mov	a,#0x16
      009F09 F0               [24] 1319 	movx	@dptr,a
      009F0A 90 0A 37         [24] 1320 	mov	dptr,#_find_alt_keycode_PARM_3
      009F0D EF               [12] 1321 	mov	a,r7
      009F0E F0               [24] 1322 	movx	@dptr,a
      009F0F 90 B9 48         [24] 1323 	mov	dptr,#_get_alt_repeat_key_keycode_pairs_50000_215
      009F12 75 F0 80         [24] 1324 	mov	b, #0x80
      009F15 12 9D A9         [24] 1325 	lcall	_find_alt_keycode
      009F18 AF 82            [24] 1326 	mov	r7, dpl
      009F1A 90 0A 3E         [24] 1327 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009F1D EF               [12] 1328 	mov	a,r7
      009F1E F0               [24] 1329 	movx	@dptr,a
      009F1F E4               [12] 1330 	clr	a
      009F20 A3               [24] 1331 	inc	dptr
      009F21 F0               [24] 1332 	movx	@dptr,a
      009F22                       1333 00110$:
                                   1334 ;	quantum/repeat_key.c:257: if (alt_keycode) {
      009F22 90 0A 3E         [24] 1335 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009F25 E0               [24] 1336 	movx	a,@dptr
      009F26 FE               [12] 1337 	mov	r6,a
      009F27 A3               [24] 1338 	inc	dptr
      009F28 E0               [24] 1339 	movx	a,@dptr
      009F29 FF               [12] 1340 	mov	r7,a
      009F2A 90 0A 3E         [24] 1341 	mov	dptr,#_get_alt_repeat_key_keycode_alt_keycode_10000_204
      009F2D E0               [24] 1342 	movx	a,@dptr
      009F2E F5 F0            [12] 1343 	mov	b,a
      009F30 A3               [24] 1344 	inc	dptr
      009F31 E0               [24] 1345 	movx	a,@dptr
      009F32 45 F0            [12] 1346 	orl	a,b
      009F34 60 10            [24] 1347 	jz	00114$
                                   1348 ;	quantum/repeat_key.c:259: return (mods << 8) | alt_keycode;
      009F36 90 0A 3D         [24] 1349 	mov	dptr,#_get_alt_repeat_key_keycode_mods_10000_204
      009F39 E0               [24] 1350 	movx	a,@dptr
      009F3A FD               [12] 1351 	mov	r5,a
      009F3B E4               [12] 1352 	clr	a
      009F3C 42 06            [12] 1353 	orl	ar6,a
      009F3E ED               [12] 1354 	mov	a,r5
      009F3F 42 07            [12] 1355 	orl	ar7,a
      009F41 8E 82            [24] 1356 	mov	dpl, r6
      009F43 8F 83            [24] 1357 	mov	dph, r7
      009F45 22               [24] 1358 	ret
      009F46                       1359 00114$:
                                   1360 ;	quantum/repeat_key.c:263: return KC_NO; // No alternate key found.
      009F46 90 00 00         [24] 1361 	mov	dptr,#0x0000
                                   1362 ;	quantum/repeat_key.c:264: }
      009F49 22               [24] 1363 	ret
                                   1364 ;------------------------------------------------------------
                                   1365 ;Allocation info for local variables in function 'alt_repeat_key_invoke'
                                   1366 ;------------------------------------------------------------
                                   1367 ;event         Allocated with name '_alt_repeat_key_invoke_event_10000_218'
                                   1368 ;------------------------------------------------------------
                                   1369 ;	quantum/repeat_key.c:266: void alt_repeat_key_invoke(const keyevent_t* event) {
                                   1370 ;	-----------------------------------------
                                   1371 ;	 function alt_repeat_key_invoke
                                   1372 ;	-----------------------------------------
      009F4A                       1373 _alt_repeat_key_invoke:
      009F4A AF F0            [24] 1374 	mov	r7,b
      009F4C AE 83            [24] 1375 	mov	r6,dph
      009F4E E5 82            [12] 1376 	mov	a,dpl
      009F50 90 0A 40         [24] 1377 	mov	dptr,#_alt_repeat_key_invoke_event_10000_218
      009F53 F0               [24] 1378 	movx	@dptr,a
      009F54 EE               [12] 1379 	mov	a,r6
      009F55 A3               [24] 1380 	inc	dptr
      009F56 F0               [24] 1381 	movx	@dptr,a
      009F57 EF               [12] 1382 	mov	a,r7
      009F58 A3               [24] 1383 	inc	dptr
      009F59 F0               [24] 1384 	movx	@dptr,a
                                   1385 ;	quantum/repeat_key.c:268: repeat_invoke(event, true);
      009F5A 90 0A 40         [24] 1386 	mov	dptr,#_alt_repeat_key_invoke_event_10000_218
      009F5D 12 73 99         [24] 1387 	lcall	_ak820_outline_0002
      009F60 90 0A 2F         [24] 1388 	mov	dptr,#_repeat_invoke_PARM_2
      009F63 74 01            [12] 1389 	mov	a,#0x01
      009F65 F0               [24] 1390 	movx	@dptr,a
      009F66 8D 82            [24] 1391 	mov	dpl, r5
      009F68 8E 83            [24] 1392 	mov	dph, r6
      009F6A 8F F0            [24] 1393 	mov	b, r7
                                   1394 ;	quantum/repeat_key.c:269: }
      009F6C 02 9C 5E         [24] 1395 	ljmp	_repeat_invoke
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
      009F6F                       1406 _get_alt_repeat_key_keycode_user:
                                   1407 ;	quantum/repeat_key.c:273: return KC_TRANSPARENT;
      009F6F 90 00 01         [24] 1408 	mov	dptr,#0x0001
                                   1409 ;	quantum/repeat_key.c:274: }
      009F72 22               [24] 1410 	ret
                                   1411 	.area CSEG    (CODE)
                                   1412 	.area CONST   (CODE)
                                   1413 	.area CONST   (CODE)
      00B936                       1414 _get_alt_repeat_key_keycode_pairs_50000_212:
      00B936 09                    1415 	.db #0x09	; 9
      00B937 05                    1416 	.db #0x05	; 5
      00B938 07                    1417 	.db #0x07	; 7
      00B939 18                    1418 	.db #0x18	; 24
      00B93A 11                    1419 	.db #0x11	; 17
      00B93B 13                    1420 	.db #0x13	; 19
      00B93C 04                    1421 	.db #0x04	; 4
      00B93D 08                    1422 	.db #0x08	; 8
      00B93E 12                    1423 	.db #0x12	; 18
      00B93F 0C                    1424 	.db #0x0c	; 12
                                   1425 	.area CSEG    (CODE)
                                   1426 	.area CONST   (CODE)
      00B940                       1427 _get_alt_repeat_key_keycode_pairs_50000_213:
      00B940 0D                    1428 	.db #0x0d	; 13
      00B941 0E                    1429 	.db #0x0e	; 14
      00B942 0B                    1430 	.db #0x0b	; 11
      00B943 0F                    1431 	.db #0x0f	; 15
      00B944 1A                    1432 	.db #0x1a	; 26
      00B945 05                    1433 	.db #0x05	; 5
      00B946 08                    1434 	.db #0x08	; 8
      00B947 05                    1435 	.db #0x05	; 5
                                   1436 	.area CSEG    (CODE)
                                   1437 	.area CONST   (CODE)
      00B948                       1438 _get_alt_repeat_key_keycode_pairs_50000_215:
      00B948 50                    1439 	.db #0x50	; 80	'P'
      00B949 4F                    1440 	.db #0x4f	; 79	'O'
      00B94A 52                    1441 	.db #0x52	; 82	'R'
      00B94B 51                    1442 	.db #0x51	; 81	'Q'
      00B94C 4A                    1443 	.db #0x4a	; 74	'J'
      00B94D 4D                    1444 	.db #0x4d	; 77	'M'
      00B94E 4B                    1445 	.db #0x4b	; 75	'K'
      00B94F 4E                    1446 	.db #0x4e	; 78	'N'
      00B950 2A                    1447 	.db #0x2a	; 42
      00B951 4C                    1448 	.db #0x4c	; 76	'L'
      00B952 2F                    1449 	.db #0x2f	; 47
      00B953 30                    1450 	.db #0x30	; 48	'0'
      00B954 B6                    1451 	.db #0xb6	; 182
      00B955 B7                    1452 	.db #0xb7	; 183
      00B956 AB                    1453 	.db #0xab	; 171
      00B957 AC                    1454 	.db #0xac	; 172
      00B958 BB                    1455 	.db #0xbb	; 187
      00B959 BC                    1456 	.db #0xbc	; 188
      00B95A A9                    1457 	.db #0xa9	; 169
      00B95B AA                    1458 	.db #0xaa	; 170
      00B95C BD                    1459 	.db #0xbd	; 189
      00B95D BE                    1460 	.db #0xbe	; 190
                                   1461 	.area CSEG    (CODE)
                                   1462 	.area XINIT   (CODE)
      00BDC0                       1463 __xinit__last_mods:
      00BDC0 00                    1464 	.db #0x00	; 0
      00BDC1                       1465 __xinit__last_repeat_count:
      00BDC1 00                    1466 	.db #0x00	;  0
      00BDC2                       1467 __xinit__processing_repeat_count:
      00BDC2 00                    1468 	.db #0x00	;  0
                                   1469 	.area CABS    (ABS,CODE)
                                   1470 
                                   1471 ; Experimental exact instruction outlining.
                                   1472 	.globl _ak820_outline_0002
                                   1473 	.globl _ak820_outline_0009
                                   1474 	.globl _ak820_outline_0012
                                   1475 	.globl _ak820_outline_0015
