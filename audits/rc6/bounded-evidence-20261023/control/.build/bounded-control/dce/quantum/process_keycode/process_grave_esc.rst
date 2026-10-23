                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module process_grave_esc
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _update_source_keycode_cache
                                     12 	.globl _get_weak_mods
                                     13 	.globl _get_mods
                                     14 	.globl _send_keyboard_report
                                     15 	.globl _del_key_from_report
                                     16 	.globl _add_key_to_report
                                     17 	.globl _ADC_START
                                     18 	.globl _S0_R_FIFO
                                     19 	.globl _S0_T_FIFO
                                     20 	.globl _S0_FREE
                                     21 	.globl _S0_IF_BYTE
                                     22 	.globl _S0_IF_FIRST
                                     23 	.globl _S0_IF_OV
                                     24 	.globl _S0_FST_ACT
                                     25 	.globl _CP_RL2
                                     26 	.globl _C_T2
                                     27 	.globl _TR2
                                     28 	.globl _EXEN2
                                     29 	.globl _TCLK
                                     30 	.globl _RCLK
                                     31 	.globl _EXF2
                                     32 	.globl _CAP1F
                                     33 	.globl _TF2
                                     34 	.globl _RI
                                     35 	.globl _TI
                                     36 	.globl _RB8
                                     37 	.globl _TB8
                                     38 	.globl _REN
                                     39 	.globl _SM2
                                     40 	.globl _SM1
                                     41 	.globl _SM0
                                     42 	.globl _IT0
                                     43 	.globl _IE0
                                     44 	.globl _IT1
                                     45 	.globl _IE1
                                     46 	.globl _TR0
                                     47 	.globl _TF0
                                     48 	.globl _TR1
                                     49 	.globl _TF1
                                     50 	.globl _P4_0
                                     51 	.globl _P4_1
                                     52 	.globl _P4_2
                                     53 	.globl _P4_3
                                     54 	.globl _P4_4
                                     55 	.globl _P4_5
                                     56 	.globl _P4_6
                                     57 	.globl _RXD
                                     58 	.globl _TXD
                                     59 	.globl _INT0
                                     60 	.globl _INT1
                                     61 	.globl _T0
                                     62 	.globl _T1
                                     63 	.globl _MOSI1
                                     64 	.globl _MISO1
                                     65 	.globl _SCK1
                                     66 	.globl _P3_0
                                     67 	.globl _P3_1
                                     68 	.globl _P3_2
                                     69 	.globl _P3_3
                                     70 	.globl _P3_4
                                     71 	.globl _P3_5
                                     72 	.globl _P3_6
                                     73 	.globl _P3_7
                                     74 	.globl _CAP1_
                                     75 	.globl _T2_
                                     76 	.globl _CAP2_
                                     77 	.globl _T2EX_
                                     78 	.globl _RXD1
                                     79 	.globl _TXD1
                                     80 	.globl _P2_0
                                     81 	.globl _P2_1
                                     82 	.globl _P2_2
                                     83 	.globl _P2_3
                                     84 	.globl _P2_4
                                     85 	.globl _P2_5
                                     86 	.globl _P2_6
                                     87 	.globl _P2_7
                                     88 	.globl _AIN0
                                     89 	.globl _AIN1
                                     90 	.globl _AIN2
                                     91 	.globl _AIN3
                                     92 	.globl _AIN4
                                     93 	.globl _AIN5
                                     94 	.globl _AIN6
                                     95 	.globl _AIN7
                                     96 	.globl _CAP1
                                     97 	.globl _T2
                                     98 	.globl _CAP2
                                     99 	.globl _T2EX
                                    100 	.globl _INT0_
                                    101 	.globl _SCS
                                    102 	.globl _MOSI
                                    103 	.globl _MISO
                                    104 	.globl _SCK
                                    105 	.globl _RXD1_
                                    106 	.globl _TXD1_
                                    107 	.globl _P1_0
                                    108 	.globl _P1_1
                                    109 	.globl _P1_2
                                    110 	.globl _P1_3
                                    111 	.globl _P1_4
                                    112 	.globl _P1_5
                                    113 	.globl _P1_6
                                    114 	.globl _P1_7
                                    115 	.globl _AIN8
                                    116 	.globl _AIN9
                                    117 	.globl _AIN10
                                    118 	.globl _AIN11
                                    119 	.globl _AIN12
                                    120 	.globl _AIN13
                                    121 	.globl _RXD_
                                    122 	.globl _TXD_
                                    123 	.globl _SCL0
                                    124 	.globl _SDA0
                                    125 	.globl _P0_0
                                    126 	.globl _P0_1
                                    127 	.globl _P0_2
                                    128 	.globl _P0_3
                                    129 	.globl _P0_4
                                    130 	.globl _P0_5
                                    131 	.globl _P0_6
                                    132 	.globl _P0_7
                                    133 	.globl _IE_SPI0
                                    134 	.globl _IE_USB
                                    135 	.globl _IE_ADC
                                    136 	.globl _IE_UART1
                                    137 	.globl _IE_PWM_I2C
                                    138 	.globl _IE_GPIO
                                    139 	.globl _IE_WDOG
                                    140 	.globl _PX0
                                    141 	.globl _PT0
                                    142 	.globl _PX1
                                    143 	.globl _PT1
                                    144 	.globl _PS
                                    145 	.globl _PT2
                                    146 	.globl _PL_FLAG
                                    147 	.globl _PH_FLAG
                                    148 	.globl _EX0
                                    149 	.globl _ET0
                                    150 	.globl _EX1
                                    151 	.globl _ET1
                                    152 	.globl _ES
                                    153 	.globl _ET2
                                    154 	.globl _E_DIS
                                    155 	.globl _EA
                                    156 	.globl _P
                                    157 	.globl _F1
                                    158 	.globl _OV
                                    159 	.globl _RS0
                                    160 	.globl _RS1
                                    161 	.globl _F0
                                    162 	.globl _AC
                                    163 	.globl _CY
                                    164 	.globl _I2CS_INT_ST
                                    165 	.globl _I2CX_INT
                                    166 	.globl _LED_STATUS
                                    167 	.globl _LED_DMA_H
                                    168 	.globl _LED_DMA_L
                                    169 	.globl _LED_DMA
                                    170 	.globl _LED_PWM_OE
                                    171 	.globl _LED_COMMON
                                    172 	.globl _ADC_CHAN
                                    173 	.globl _ADC_DAT_H
                                    174 	.globl _ADC_DAT_L
                                    175 	.globl _ADC_DAT
                                    176 	.globl _ADC_CTRL
                                    177 	.globl _SPI1_CK_SE
                                    178 	.globl _SPI1_CTRL
                                    179 	.globl _SPI1_DATA
                                    180 	.globl _SPI1_STAT
                                    181 	.globl _SIF1
                                    182 	.globl _SBAUD1
                                    183 	.globl _SBUF1
                                    184 	.globl _SCON1
                                    185 	.globl _SPI0_SETUP
                                    186 	.globl _SPI0_CK_SE
                                    187 	.globl _SPI0_CTRL
                                    188 	.globl _SPI0_DATA
                                    189 	.globl _SPI0_STAT
                                    190 	.globl _T2CAP1H
                                    191 	.globl _T2CAP1L
                                    192 	.globl _T2CAP1
                                    193 	.globl _TH2
                                    194 	.globl _TL2
                                    195 	.globl _T2COUNT
                                    196 	.globl _RCAP2H
                                    197 	.globl _RCAP2L
                                    198 	.globl _RCAP2
                                    199 	.globl _T2MOD
                                    200 	.globl _T2CON
                                    201 	.globl _SBUF
                                    202 	.globl _SCON
                                    203 	.globl _TH1
                                    204 	.globl _TH0
                                    205 	.globl _TL1
                                    206 	.globl _TL0
                                    207 	.globl _TMOD
                                    208 	.globl _TCON
                                    209 	.globl _XBUS_AUX
                                    210 	.globl _P7
                                    211 	.globl _P6_DIR
                                    212 	.globl _P6_OUT_PU
                                    213 	.globl _P6_IN
                                    214 	.globl _P5_DIR
                                    215 	.globl _P5_OUT_PU
                                    216 	.globl _P5_IN
                                    217 	.globl _P4_LED_KEY
                                    218 	.globl _P4_DIR_PU
                                    219 	.globl _P4_MOD_OC
                                    220 	.globl _P4
                                    221 	.globl _P3_DIR_PU
                                    222 	.globl _P3_MOD_OC
                                    223 	.globl _P3
                                    224 	.globl _P2_DIR_PU
                                    225 	.globl _P2_MOD_OC
                                    226 	.globl _P2
                                    227 	.globl _P1_DIR_PU
                                    228 	.globl _P1_MOD_OC
                                    229 	.globl _P1
                                    230 	.globl _P0_DIR_PU
                                    231 	.globl _P0_MOD_OC
                                    232 	.globl _P0
                                    233 	.globl _ROM_CTRL
                                    234 	.globl _ROM_DATA_HH
                                    235 	.globl _ROM_DATA_HL
                                    236 	.globl _ROM_DATA_HI
                                    237 	.globl _ROM_ADDR_H
                                    238 	.globl _ROM_ADDR_L
                                    239 	.globl _ROM_ADDR
                                    240 	.globl _GPIO_IE
                                    241 	.globl _IP_EX
                                    242 	.globl _IE_EX
                                    243 	.globl _IP
                                    244 	.globl _IE
                                    245 	.globl _WDOG_COUNT
                                    246 	.globl _RESET_KEEP
                                    247 	.globl _WAKE_CTRL
                                    248 	.globl _CLOCK_CFG
                                    249 	.globl _POWER_CFG
                                    250 	.globl _PCON
                                    251 	.globl _GLOBAL_CFG
                                    252 	.globl _SAFE_MOD
                                    253 	.globl _DPH
                                    254 	.globl _DPL
                                    255 	.globl _SP
                                    256 	.globl _A_INV
                                    257 	.globl _B
                                    258 	.globl _ACC
                                    259 	.globl _PSW
                                    260 	.globl _process_grave_esc_PARM_2
                                    261 	.globl _process_grave_esc
                                    262 ;--------------------------------------------------------
                                    263 ; special function registers
                                    264 ;--------------------------------------------------------
                                    265 	.area RSEG    (ABS,DATA)
      000000                        266 	.org 0x0000
                           0000D0   267 _PSW	=	0x00d0
                           0000E0   268 _ACC	=	0x00e0
                           0000F0   269 _B	=	0x00f0
                           0000FD   270 _A_INV	=	0x00fd
                           000081   271 _SP	=	0x0081
                           000082   272 _DPL	=	0x0082
                           000083   273 _DPH	=	0x0083
                           0000A1   274 _SAFE_MOD	=	0x00a1
                           0000B1   275 _GLOBAL_CFG	=	0x00b1
                           000087   276 _PCON	=	0x0087
                           0000BA   277 _POWER_CFG	=	0x00ba
                           0000B9   278 _CLOCK_CFG	=	0x00b9
                           0000A9   279 _WAKE_CTRL	=	0x00a9
                           0000FE   280 _RESET_KEEP	=	0x00fe
                           0000FF   281 _WDOG_COUNT	=	0x00ff
                           0000A8   282 _IE	=	0x00a8
                           0000B8   283 _IP	=	0x00b8
                           0000E8   284 _IE_EX	=	0x00e8
                           0000E9   285 _IP_EX	=	0x00e9
                           0000B2   286 _GPIO_IE	=	0x00b2
                           008584   287 _ROM_ADDR	=	0x8584
                           000084   288 _ROM_ADDR_L	=	0x0084
                           000085   289 _ROM_ADDR_H	=	0x0085
                           008F8E   290 _ROM_DATA_HI	=	0x8f8e
                           00008E   291 _ROM_DATA_HL	=	0x008e
                           00008F   292 _ROM_DATA_HH	=	0x008f
                           000086   293 _ROM_CTRL	=	0x0086
                           000080   294 _P0	=	0x0080
                           0000C4   295 _P0_MOD_OC	=	0x00c4
                           0000C5   296 _P0_DIR_PU	=	0x00c5
                           000090   297 _P1	=	0x0090
                           000092   298 _P1_MOD_OC	=	0x0092
                           000093   299 _P1_DIR_PU	=	0x0093
                           0000A0   300 _P2	=	0x00a0
                           000094   301 _P2_MOD_OC	=	0x0094
                           000095   302 _P2_DIR_PU	=	0x0095
                           0000B0   303 _P3	=	0x00b0
                           000096   304 _P3_MOD_OC	=	0x0096
                           000097   305 _P3_DIR_PU	=	0x0097
                           0000C0   306 _P4	=	0x00c0
                           0000C2   307 _P4_MOD_OC	=	0x00c2
                           0000C3   308 _P4_DIR_PU	=	0x00c3
                           0000C1   309 _P4_LED_KEY	=	0x00c1
                           0000AA   310 _P5_IN	=	0x00aa
                           0000AB   311 _P5_OUT_PU	=	0x00ab
                           0000AC   312 _P5_DIR	=	0x00ac
                           0000AD   313 _P6_IN	=	0x00ad
                           0000AE   314 _P6_OUT_PU	=	0x00ae
                           0000AF   315 _P6_DIR	=	0x00af
                           0000F1   316 _P7	=	0x00f1
                           0000A2   317 _XBUS_AUX	=	0x00a2
                           000088   318 _TCON	=	0x0088
                           000089   319 _TMOD	=	0x0089
                           00008A   320 _TL0	=	0x008a
                           00008B   321 _TL1	=	0x008b
                           00008C   322 _TH0	=	0x008c
                           00008D   323 _TH1	=	0x008d
                           000098   324 _SCON	=	0x0098
                           000099   325 _SBUF	=	0x0099
                           0000C8   326 _T2CON	=	0x00c8
                           0000C9   327 _T2MOD	=	0x00c9
                           00CBCA   328 _RCAP2	=	0xcbca
                           0000CA   329 _RCAP2L	=	0x00ca
                           0000CB   330 _RCAP2H	=	0x00cb
                           00CDCC   331 _T2COUNT	=	0xcdcc
                           0000CC   332 _TL2	=	0x00cc
                           0000CD   333 _TH2	=	0x00cd
                           00CFCE   334 _T2CAP1	=	0xcfce
                           0000CE   335 _T2CAP1L	=	0x00ce
                           0000CF   336 _T2CAP1H	=	0x00cf
                           0000F8   337 _SPI0_STAT	=	0x00f8
                           0000F9   338 _SPI0_DATA	=	0x00f9
                           0000FA   339 _SPI0_CTRL	=	0x00fa
                           0000FB   340 _SPI0_CK_SE	=	0x00fb
                           0000FC   341 _SPI0_SETUP	=	0x00fc
                           0000BC   342 _SCON1	=	0x00bc
                           0000BD   343 _SBUF1	=	0x00bd
                           0000BE   344 _SBAUD1	=	0x00be
                           0000BF   345 _SIF1	=	0x00bf
                           0000B4   346 _SPI1_STAT	=	0x00b4
                           0000B5   347 _SPI1_DATA	=	0x00b5
                           0000B6   348 _SPI1_CTRL	=	0x00b6
                           0000B7   349 _SPI1_CK_SE	=	0x00b7
                           0000F3   350 _ADC_CTRL	=	0x00f3
                           00F5F4   351 _ADC_DAT	=	0xf5f4
                           0000F4   352 _ADC_DAT_L	=	0x00f4
                           0000F5   353 _ADC_DAT_H	=	0x00f5
                           0000F6   354 _ADC_CHAN	=	0x00f6
                           0000A6   355 _LED_COMMON	=	0x00a6
                           0000A7   356 _LED_PWM_OE	=	0x00a7
                           00C7C6   357 _LED_DMA	=	0xc7c6
                           0000C6   358 _LED_DMA_L	=	0x00c6
                           0000C7   359 _LED_DMA_H	=	0x00c7
                           0000F7   360 _LED_STATUS	=	0x00f7
                           0000B3   361 _I2CX_INT	=	0x00b3
                           0000BB   362 _I2CS_INT_ST	=	0x00bb
                                    363 ;--------------------------------------------------------
                                    364 ; special function bits
                                    365 ;--------------------------------------------------------
                                    366 	.area RSEG    (ABS,DATA)
      000000                        367 	.org 0x0000
                           0000D7   368 _CY	=	0x00d7
                           0000D6   369 _AC	=	0x00d6
                           0000D5   370 _F0	=	0x00d5
                           0000D4   371 _RS1	=	0x00d4
                           0000D3   372 _RS0	=	0x00d3
                           0000D2   373 _OV	=	0x00d2
                           0000D1   374 _F1	=	0x00d1
                           0000D0   375 _P	=	0x00d0
                           0000AF   376 _EA	=	0x00af
                           0000AE   377 _E_DIS	=	0x00ae
                           0000AD   378 _ET2	=	0x00ad
                           0000AC   379 _ES	=	0x00ac
                           0000AB   380 _ET1	=	0x00ab
                           0000AA   381 _EX1	=	0x00aa
                           0000A9   382 _ET0	=	0x00a9
                           0000A8   383 _EX0	=	0x00a8
                           0000BF   384 _PH_FLAG	=	0x00bf
                           0000BE   385 _PL_FLAG	=	0x00be
                           0000BD   386 _PT2	=	0x00bd
                           0000BC   387 _PS	=	0x00bc
                           0000BB   388 _PT1	=	0x00bb
                           0000BA   389 _PX1	=	0x00ba
                           0000B9   390 _PT0	=	0x00b9
                           0000B8   391 _PX0	=	0x00b8
                           0000EF   392 _IE_WDOG	=	0x00ef
                           0000EE   393 _IE_GPIO	=	0x00ee
                           0000ED   394 _IE_PWM_I2C	=	0x00ed
                           0000EC   395 _IE_UART1	=	0x00ec
                           0000EB   396 _IE_ADC	=	0x00eb
                           0000E9   397 _IE_USB	=	0x00e9
                           0000E8   398 _IE_SPI0	=	0x00e8
                           000087   399 _P0_7	=	0x0087
                           000086   400 _P0_6	=	0x0086
                           000085   401 _P0_5	=	0x0085
                           000084   402 _P0_4	=	0x0084
                           000083   403 _P0_3	=	0x0083
                           000082   404 _P0_2	=	0x0082
                           000081   405 _P0_1	=	0x0081
                           000080   406 _P0_0	=	0x0080
                           000081   407 _SDA0	=	0x0081
                           000080   408 _SCL0	=	0x0080
                           000083   409 _TXD_	=	0x0083
                           000082   410 _RXD_	=	0x0082
                           000085   411 _AIN13	=	0x0085
                           000084   412 _AIN12	=	0x0084
                           000083   413 _AIN11	=	0x0083
                           000082   414 _AIN10	=	0x0082
                           000081   415 _AIN9	=	0x0081
                           000080   416 _AIN8	=	0x0080
                           000097   417 _P1_7	=	0x0097
                           000096   418 _P1_6	=	0x0096
                           000095   419 _P1_5	=	0x0095
                           000094   420 _P1_4	=	0x0094
                           000093   421 _P1_3	=	0x0093
                           000092   422 _P1_2	=	0x0092
                           000091   423 _P1_1	=	0x0091
                           000090   424 _P1_0	=	0x0090
                           000097   425 _TXD1_	=	0x0097
                           000096   426 _RXD1_	=	0x0096
                           000097   427 _SCK	=	0x0097
                           000096   428 _MISO	=	0x0096
                           000095   429 _MOSI	=	0x0095
                           000094   430 _SCS	=	0x0094
                           000092   431 _INT0_	=	0x0092
                           000091   432 _T2EX	=	0x0091
                           000091   433 _CAP2	=	0x0091
                           000090   434 _T2	=	0x0090
                           000090   435 _CAP1	=	0x0090
                           000097   436 _AIN7	=	0x0097
                           000096   437 _AIN6	=	0x0096
                           000095   438 _AIN5	=	0x0095
                           000094   439 _AIN4	=	0x0094
                           000093   440 _AIN3	=	0x0093
                           000092   441 _AIN2	=	0x0092
                           000091   442 _AIN1	=	0x0091
                           000090   443 _AIN0	=	0x0090
                           0000A7   444 _P2_7	=	0x00a7
                           0000A6   445 _P2_6	=	0x00a6
                           0000A5   446 _P2_5	=	0x00a5
                           0000A4   447 _P2_4	=	0x00a4
                           0000A3   448 _P2_3	=	0x00a3
                           0000A2   449 _P2_2	=	0x00a2
                           0000A1   450 _P2_1	=	0x00a1
                           0000A0   451 _P2_0	=	0x00a0
                           0000A7   452 _TXD1	=	0x00a7
                           0000A6   453 _RXD1	=	0x00a6
                           0000A5   454 _T2EX_	=	0x00a5
                           0000A5   455 _CAP2_	=	0x00a5
                           0000A4   456 _T2_	=	0x00a4
                           0000A4   457 _CAP1_	=	0x00a4
                           0000B7   458 _P3_7	=	0x00b7
                           0000B6   459 _P3_6	=	0x00b6
                           0000B5   460 _P3_5	=	0x00b5
                           0000B4   461 _P3_4	=	0x00b4
                           0000B3   462 _P3_3	=	0x00b3
                           0000B2   463 _P3_2	=	0x00b2
                           0000B1   464 _P3_1	=	0x00b1
                           0000B0   465 _P3_0	=	0x00b0
                           0000B7   466 _SCK1	=	0x00b7
                           0000B6   467 _MISO1	=	0x00b6
                           0000B5   468 _MOSI1	=	0x00b5
                           0000B5   469 _T1	=	0x00b5
                           0000B4   470 _T0	=	0x00b4
                           0000B3   471 _INT1	=	0x00b3
                           0000B2   472 _INT0	=	0x00b2
                           0000B1   473 _TXD	=	0x00b1
                           0000B0   474 _RXD	=	0x00b0
                           0000C6   475 _P4_6	=	0x00c6
                           0000C5   476 _P4_5	=	0x00c5
                           0000C4   477 _P4_4	=	0x00c4
                           0000C3   478 _P4_3	=	0x00c3
                           0000C2   479 _P4_2	=	0x00c2
                           0000C1   480 _P4_1	=	0x00c1
                           0000C0   481 _P4_0	=	0x00c0
                           00008F   482 _TF1	=	0x008f
                           00008E   483 _TR1	=	0x008e
                           00008D   484 _TF0	=	0x008d
                           00008C   485 _TR0	=	0x008c
                           00008B   486 _IE1	=	0x008b
                           00008A   487 _IT1	=	0x008a
                           000089   488 _IE0	=	0x0089
                           000088   489 _IT0	=	0x0088
                           00009F   490 _SM0	=	0x009f
                           00009E   491 _SM1	=	0x009e
                           00009D   492 _SM2	=	0x009d
                           00009C   493 _REN	=	0x009c
                           00009B   494 _TB8	=	0x009b
                           00009A   495 _RB8	=	0x009a
                           000099   496 _TI	=	0x0099
                           000098   497 _RI	=	0x0098
                           0000CF   498 _TF2	=	0x00cf
                           0000CF   499 _CAP1F	=	0x00cf
                           0000CE   500 _EXF2	=	0x00ce
                           0000CD   501 _RCLK	=	0x00cd
                           0000CC   502 _TCLK	=	0x00cc
                           0000CB   503 _EXEN2	=	0x00cb
                           0000CA   504 _TR2	=	0x00ca
                           0000C9   505 _C_T2	=	0x00c9
                           0000C8   506 _CP_RL2	=	0x00c8
                           0000FF   507 _S0_FST_ACT	=	0x00ff
                           0000FE   508 _S0_IF_OV	=	0x00fe
                           0000FD   509 _S0_IF_FIRST	=	0x00fd
                           0000FC   510 _S0_IF_BYTE	=	0x00fc
                           0000FB   511 _S0_FREE	=	0x00fb
                           0000FA   512 _S0_T_FIFO	=	0x00fa
                           0000F8   513 _S0_R_FIFO	=	0x00f8
                           0000F7   514 _ADC_START	=	0x00f7
                                    515 ;--------------------------------------------------------
                                    516 ; overlayable register banks
                                    517 ;--------------------------------------------------------
                                    518 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        519 	.ds 8
                                    520 ;--------------------------------------------------------
                                    521 ; internal ram data
                                    522 ;--------------------------------------------------------
                                    523 	.area DSEG    (DATA)
      00001A                        524 _process_grave_esc_sloc0_1_0:
      00001A                        525 	.ds 3
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
      0009A7                        550 _process_grave_esc_PARM_2:
      0009A7                        551 	.ds 3
      0009AA                        552 _process_grave_esc_keycode_10000_220:
      0009AA                        553 	.ds 2
                                    554 ;--------------------------------------------------------
                                    555 ; absolute external ram data
                                    556 ;--------------------------------------------------------
                                    557 	.area XABS    (ABS,XDATA)
                                    558 ;--------------------------------------------------------
                                    559 ; initialized external ram data
                                    560 ;--------------------------------------------------------
                                    561 	.area XISEG   (XDATA)
      000C01                        562 _grave_esc_was_shifted:
      000C01                        563 	.ds 1
                                    564 	.area HOME    (CODE)
                                    565 	.area GSINIT0 (CODE)
                                    566 	.area GSINIT1 (CODE)
                                    567 	.area GSINIT2 (CODE)
                                    568 	.area GSINIT3 (CODE)
                                    569 	.area GSINIT4 (CODE)
                                    570 	.area GSINIT5 (CODE)
                                    571 	.area GSINIT  (CODE)
                                    572 	.area GSFINAL (CODE)
                                    573 	.area CSEG    (CODE)
                                    574 ;--------------------------------------------------------
                                    575 ; global & static initialisations
                                    576 ;--------------------------------------------------------
                                    577 	.area HOME    (CODE)
                                    578 	.area GSINIT  (CODE)
                                    579 	.area GSFINAL (CODE)
                                    580 	.area GSINIT  (CODE)
                                    581 ;--------------------------------------------------------
                                    582 ; Home
                                    583 ;--------------------------------------------------------
                                    584 	.area HOME    (CODE)
                                    585 	.area HOME    (CODE)
                                    586 ;--------------------------------------------------------
                                    587 ; code
                                    588 ;--------------------------------------------------------
                                    589 	.area CSEG    (CODE)
                                    590 ;------------------------------------------------------------
                                    591 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    592 ;------------------------------------------------------------
                                    593 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_122'
                                    594 ;------------------------------------------------------------
                                    595 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    596 ;	-----------------------------------------
                           000007   597 	ar7 = 0x07
                           000006   598 	ar6 = 0x06
                           000005   599 	ar5 = 0x05
                           000004   600 	ar4 = 0x04
                           000003   601 	ar3 = 0x03
                           000002   602 	ar2 = 0x02
                           000001   603 	ar1 = 0x01
                           000000   604 	ar0 = 0x00
                                    605 ;	 function process_grave_esc
                                    606 ;	-----------------------------------------
      0092DA                        607 _process_grave_esc:
      0092DA AF 83            [24]  608 	mov	r7,dph
      0092DC E5 82            [12]  609 	mov	a,dpl
      0092DE 90 09 AA         [24]  610 	mov	dptr,#_process_grave_esc_keycode_10000_220
      0092E1 F0               [24]  611 	movx	@dptr,a
      0092E2 EF               [12]  612 	mov	a,r7
      0092E3 A3               [24]  613 	inc	dptr
      0092E4 F0               [24]  614 	movx	@dptr,a
                                    615 ;	quantum/process_keycode/process_grave_esc.c:31: if (keycode == QK_GRAVE_ESCAPE) {
      0092E5 90 09 AA         [24]  616 	mov	dptr,#_process_grave_esc_keycode_10000_220
      0092E8 E0               [24]  617 	movx	a,@dptr
      0092E9 FE               [12]  618 	mov	r6,a
      0092EA A3               [24]  619 	inc	dptr
      0092EB E0               [24]  620 	movx	a,@dptr
      0092EC FF               [12]  621 	mov	r7,a
      0092ED BE 16 05         [24]  622 	cjne	r6,#0x16,00186$
      0092F0 BF 7C 02         [24]  623 	cjne	r7,#0x7c,00186$
      0092F3 80 03            [24]  624 	sjmp	00187$
      0092F5                        625 00186$:
      0092F5 02 93 DE         [24]  626 	ljmp	00126$
      0092F8                        627 00187$:
                                    628 ;	quantum/process_keycode/process_grave_esc.c:34: const uint8_t mods    = get_mods() | get_weak_mods();
      0092F8 12 78 86         [24]  629 	lcall	_get_mods
      0092FB AF 82            [24]  630 	mov	r7, dpl
      0092FD 12 78 B2         [24]  631 	lcall	_get_weak_mods
      009300 E5 82            [12]  632 	mov	a,dpl
      009302 4F               [12]  633 	orl	a,r7
                                    634 ;	quantum/process_keycode/process_grave_esc.c:35: uint8_t       shifted = mods & MOD_MASK_SG;
      009303 54 AA            [12]  635 	anl	a,#0xaa
      009305 FF               [12]  636 	mov	r7,a
                                    637 ;	quantum/process_keycode/process_grave_esc.c:67: if (record->event.pressed) {
      009306 90 09 A7         [24]  638 	mov	dptr,#_process_grave_esc_PARM_2
      009309 E0               [24]  639 	movx	a,@dptr
      00930A FC               [12]  640 	mov	r4,a
      00930B A3               [24]  641 	inc	dptr
      00930C E0               [24]  642 	movx	a,@dptr
      00930D FD               [12]  643 	mov	r5,a
      00930E A3               [24]  644 	inc	dptr
      00930F E0               [24]  645 	movx	a,@dptr
      009310 FE               [12]  646 	mov	r6,a
      009311 74 05            [12]  647 	mov	a,#0x05
      009313 2C               [12]  648 	add	a, r4
      009314 F9               [12]  649 	mov	r1,a
      009315 E4               [12]  650 	clr	a
      009316 3D               [12]  651 	addc	a, r5
      009317 FA               [12]  652 	mov	r2,a
      009318 8E 03            [24]  653 	mov	ar3,r6
      00931A 89 82            [24]  654 	mov	dpl,r1
      00931C 8A 83            [24]  655 	mov	dph,r2
      00931E 8B F0            [24]  656 	mov	b,r3
      009320 12 B5 97         [24]  657 	lcall	__gptrget
      009323 70 03            [24]  658 	jnz	00188$
      009325 02 93 BD         [24]  659 	ljmp	00123$
      009328                        660 00188$:
                                    661 ;	quantum/process_keycode/process_grave_esc.c:71: uint16_t resolved = shifted ? KC_GRAVE : KC_ESCAPE;
      009328 EF               [12]  662 	mov	a,r7
      009329 60 04            [24]  663 	jz	00131$
      00932B 7B 35            [12]  664 	mov	r3,#0x35
      00932D 80 02            [24]  665 	sjmp	00132$
      00932F                        666 00131$:
      00932F 7B 29            [12]  667 	mov	r3,#0x29
      009331                        668 00132$:
      009331 8B 02            [24]  669 	mov	ar2,r3
      009333 7B 00            [12]  670 	mov	r3,#0x00
                                    671 ;	quantum/process_keycode/process_grave_esc.c:73: if (record->keycode) {
      009335 74 06            [12]  672 	mov	a,#0x06
      009337 2C               [12]  673 	add	a, r4
      009338 F5 1A            [12]  674 	mov	_process_grave_esc_sloc0_1_0,a
      00933A E4               [12]  675 	clr	a
      00933B 3D               [12]  676 	addc	a, r5
      00933C F5 1B            [12]  677 	mov	(_process_grave_esc_sloc0_1_0 + 1),a
      00933E 8E 1C            [24]  678 	mov	(_process_grave_esc_sloc0_1_0 + 2),r6
      009340 85 1A 82         [24]  679 	mov	dpl,_process_grave_esc_sloc0_1_0
      009343 85 1B 83         [24]  680 	mov	dph,(_process_grave_esc_sloc0_1_0 + 1)
      009346 85 1C F0         [24]  681 	mov	b,(_process_grave_esc_sloc0_1_0 + 2)
      009349 12 B5 97         [24]  682 	lcall	__gptrget
      00934C F8               [12]  683 	mov	r0,a
      00934D A3               [24]  684 	inc	dptr
      00934E 12 B5 97         [24]  685 	lcall	__gptrget
      009351 48               [12]  686 	orl	a,r0
      009352 60 14            [24]  687 	jz	00120$
                                    688 ;	quantum/process_keycode/process_grave_esc.c:74: record->keycode = resolved;
      009354 85 1A 82         [24]  689 	mov	dpl,_process_grave_esc_sloc0_1_0
      009357 85 1B 83         [24]  690 	mov	dph,(_process_grave_esc_sloc0_1_0 + 1)
      00935A 85 1C F0         [24]  691 	mov	b,(_process_grave_esc_sloc0_1_0 + 2)
      00935D EA               [12]  692 	mov	a,r2
      00935E 12 B5 5C         [24]  693 	lcall	__gptrput
      009361 A3               [24]  694 	inc	dptr
      009362 EB               [12]  695 	mov	a,r3
      009363 12 B5 5C         [24]  696 	lcall	__gptrput
      009366 80 3C            [24]  697 	sjmp	00121$
      009368                        698 00120$:
                                    699 ;	quantum/process_keycode/process_grave_esc.c:77: if (!update_source_keycode_cache(record->event.key, resolved)) {
      009368 90 0B 90         [24]  700 	mov	dptr,#___memcpy_PARM_2
      00936B EC               [12]  701 	mov	a,r4
      00936C F0               [24]  702 	movx	@dptr,a
      00936D ED               [12]  703 	mov	a,r5
      00936E A3               [24]  704 	inc	dptr
      00936F F0               [24]  705 	movx	@dptr,a
      009370 EE               [12]  706 	mov	a,r6
      009371 A3               [24]  707 	inc	dptr
      009372 F0               [24]  708 	movx	@dptr,a
      009373 90 0B 93         [24]  709 	mov	dptr,#___memcpy_PARM_3
      009376 74 02            [12]  710 	mov	a,#0x02
      009378 F0               [24]  711 	movx	@dptr,a
      009379 E4               [12]  712 	clr	a
      00937A A3               [24]  713 	inc	dptr
      00937B F0               [24]  714 	movx	@dptr,a
      00937C 90 08 7E         [24]  715 	mov	dptr,#_update_source_keycode_cache_PARM_1
      00937F F5 F0            [12]  716 	mov	b,a
      009381 C0 07            [24]  717 	push	ar7
      009383 C0 03            [24]  718 	push	ar3
      009385 C0 02            [24]  719 	push	ar2
      009387 12 B4 BE         [24]  720 	lcall	___memcpy
      00938A D0 02            [24]  721 	pop	ar2
      00938C D0 03            [24]  722 	pop	ar3
      00938E 8A 82            [24]  723 	mov	dpl, r2
      009390 8B 83            [24]  724 	mov	dph, r3
      009392 12 75 74         [24]  725 	lcall	_update_source_keycode_cache
      009395 E5 82            [12]  726 	mov	a, dpl
      009397 D0 07            [24]  727 	pop	ar7
      009399 70 09            [24]  728 	jnz	00121$
                                    729 ;	quantum/process_keycode/process_grave_esc.c:78: grave_esc_was_shifted = shifted;
      00939B 90 0C 01         [24]  730 	mov	dptr,#_grave_esc_was_shifted
                                    731 ;	assignBit
      00939E EF               [12]  732 	mov	a,r7
      00939F 24 FF            [12]  733 	add	a,#0xff
      0093A1 E4               [12]  734 	clr	a
      0093A2 33               [12]  735 	rlc	a
      0093A3 F0               [24]  736 	movx	@dptr,a
      0093A4                        737 00121$:
                                    738 ;	quantum/process_keycode/process_grave_esc.c:83: add_key(shifted ? KC_GRAVE : KC_ESCAPE);
      0093A4 EF               [12]  739 	mov	a,r7
      0093A5 60 04            [24]  740 	jz	00133$
      0093A7 7F 35            [12]  741 	mov	r7,#0x35
      0093A9 80 02            [24]  742 	sjmp	00134$
      0093AB                        743 00133$:
      0093AB 7F 29            [12]  744 	mov	r7,#0x29
      0093AD                        745 00134$:
                                    746 ;	quantum/action_util.h:39: add_key_to_report(keyboard_report, key);
      0093AD 90 07 28         [24]  747 	mov	dptr,#_add_key_to_report_PARM_2
      0093B0 EF               [12]  748 	mov	a,r7
      0093B1 F0               [24]  749 	movx	@dptr,a
      0093B2 90 0B B1         [24]  750 	mov	dptr,#_actual_keyboard_report
      0093B5 75 F0 00         [24]  751 	mov	b, #0x00
      0093B8 12 6B 84         [24]  752 	lcall	_add_key_to_report
                                    753 ;	quantum/process_keycode/process_grave_esc.c:83: add_key(shifted ? KC_GRAVE : KC_ESCAPE);
      0093BB 80 1A            [24]  754 	sjmp	00124$
      0093BD                        755 00123$:
                                    756 ;	quantum/process_keycode/process_grave_esc.c:85: del_key(grave_esc_was_shifted ? KC_GRAVE : KC_ESCAPE);
      0093BD 90 0C 01         [24]  757 	mov	dptr,#_grave_esc_was_shifted
      0093C0 E0               [24]  758 	movx	a,@dptr
      0093C1 60 04            [24]  759 	jz	00135$
      0093C3 7F 35            [12]  760 	mov	r7,#0x35
      0093C5 80 02            [24]  761 	sjmp	00136$
      0093C7                        762 00135$:
      0093C7 7F 29            [12]  763 	mov	r7,#0x29
      0093C9                        764 00136$:
                                    765 ;	quantum/action_util.h:43: del_key_from_report(keyboard_report, key);
      0093C9 90 07 2C         [24]  766 	mov	dptr,#_del_key_from_report_PARM_2
      0093CC EF               [12]  767 	mov	a,r7
      0093CD F0               [24]  768 	movx	@dptr,a
      0093CE 90 0B B1         [24]  769 	mov	dptr,#_actual_keyboard_report
      0093D1 75 F0 00         [24]  770 	mov	b, #0x00
      0093D4 12 6B D9         [24]  771 	lcall	_del_key_from_report
                                    772 ;	quantum/process_keycode/process_grave_esc.c:85: del_key(grave_esc_was_shifted ? KC_GRAVE : KC_ESCAPE);
      0093D7                        773 00124$:
                                    774 ;	quantum/process_keycode/process_grave_esc.c:88: send_keyboard_report();
      0093D7 12 78 28         [24]  775 	lcall	_send_keyboard_report
                                    776 ;	quantum/process_keycode/process_grave_esc.c:89: return false;
      0093DA 75 82 00         [24]  777 	mov	dpl, #0x00
      0093DD 22               [24]  778 	ret
      0093DE                        779 00126$:
                                    780 ;	quantum/process_keycode/process_grave_esc.c:93: return true;
      0093DE 75 82 01         [24]  781 	mov	dpl, #0x01
                                    782 ;	quantum/process_keycode/process_grave_esc.c:94: }
      0093E1 22               [24]  783 	ret
                                    784 	.area CSEG    (CODE)
                                    785 	.area CONST   (CODE)
                                    786 	.area XINIT   (CODE)
      00BDDE                        787 __xinit__grave_esc_was_shifted:
      00BDDE 00                     788 	.db #0x00	;  0
                                    789 	.area CABS    (ABS,CODE)
