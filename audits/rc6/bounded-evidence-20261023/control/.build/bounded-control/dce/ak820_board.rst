                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module ak820_board
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _rgb_matrix_driver
                                     12 	.globl _ak820_rgb_slots
                                     13 	.globl _ADC_START
                                     14 	.globl _S0_R_FIFO
                                     15 	.globl _S0_T_FIFO
                                     16 	.globl _S0_FREE
                                     17 	.globl _S0_IF_BYTE
                                     18 	.globl _S0_IF_FIRST
                                     19 	.globl _S0_IF_OV
                                     20 	.globl _S0_FST_ACT
                                     21 	.globl _CP_RL2
                                     22 	.globl _C_T2
                                     23 	.globl _TR2
                                     24 	.globl _EXEN2
                                     25 	.globl _TCLK
                                     26 	.globl _RCLK
                                     27 	.globl _EXF2
                                     28 	.globl _CAP1F
                                     29 	.globl _TF2
                                     30 	.globl _RI
                                     31 	.globl _TI
                                     32 	.globl _RB8
                                     33 	.globl _TB8
                                     34 	.globl _REN
                                     35 	.globl _SM2
                                     36 	.globl _SM1
                                     37 	.globl _SM0
                                     38 	.globl _IT0
                                     39 	.globl _IE0
                                     40 	.globl _IT1
                                     41 	.globl _IE1
                                     42 	.globl _TR0
                                     43 	.globl _TF0
                                     44 	.globl _TR1
                                     45 	.globl _TF1
                                     46 	.globl _P4_0
                                     47 	.globl _P4_1
                                     48 	.globl _P4_2
                                     49 	.globl _P4_3
                                     50 	.globl _P4_4
                                     51 	.globl _P4_5
                                     52 	.globl _P4_6
                                     53 	.globl _RXD
                                     54 	.globl _TXD
                                     55 	.globl _INT0
                                     56 	.globl _INT1
                                     57 	.globl _T0
                                     58 	.globl _T1
                                     59 	.globl _MOSI1
                                     60 	.globl _MISO1
                                     61 	.globl _SCK1
                                     62 	.globl _P3_0
                                     63 	.globl _P3_1
                                     64 	.globl _P3_2
                                     65 	.globl _P3_3
                                     66 	.globl _P3_4
                                     67 	.globl _P3_5
                                     68 	.globl _P3_6
                                     69 	.globl _P3_7
                                     70 	.globl _CAP1_
                                     71 	.globl _T2_
                                     72 	.globl _CAP2_
                                     73 	.globl _T2EX_
                                     74 	.globl _RXD1
                                     75 	.globl _TXD1
                                     76 	.globl _P2_0
                                     77 	.globl _P2_1
                                     78 	.globl _P2_2
                                     79 	.globl _P2_3
                                     80 	.globl _P2_4
                                     81 	.globl _P2_5
                                     82 	.globl _P2_6
                                     83 	.globl _P2_7
                                     84 	.globl _AIN0
                                     85 	.globl _AIN1
                                     86 	.globl _AIN2
                                     87 	.globl _AIN3
                                     88 	.globl _AIN4
                                     89 	.globl _AIN5
                                     90 	.globl _AIN6
                                     91 	.globl _AIN7
                                     92 	.globl _CAP1
                                     93 	.globl _T2
                                     94 	.globl _CAP2
                                     95 	.globl _T2EX
                                     96 	.globl _INT0_
                                     97 	.globl _SCS
                                     98 	.globl _MOSI
                                     99 	.globl _MISO
                                    100 	.globl _SCK
                                    101 	.globl _RXD1_
                                    102 	.globl _TXD1_
                                    103 	.globl _P1_0
                                    104 	.globl _P1_1
                                    105 	.globl _P1_2
                                    106 	.globl _P1_3
                                    107 	.globl _P1_4
                                    108 	.globl _P1_5
                                    109 	.globl _P1_6
                                    110 	.globl _P1_7
                                    111 	.globl _AIN8
                                    112 	.globl _AIN9
                                    113 	.globl _AIN10
                                    114 	.globl _AIN11
                                    115 	.globl _AIN12
                                    116 	.globl _AIN13
                                    117 	.globl _RXD_
                                    118 	.globl _TXD_
                                    119 	.globl _SCL0
                                    120 	.globl _SDA0
                                    121 	.globl _P0_0
                                    122 	.globl _P0_1
                                    123 	.globl _P0_2
                                    124 	.globl _P0_3
                                    125 	.globl _P0_4
                                    126 	.globl _P0_5
                                    127 	.globl _P0_6
                                    128 	.globl _P0_7
                                    129 	.globl _IE_SPI0
                                    130 	.globl _IE_USB
                                    131 	.globl _IE_ADC
                                    132 	.globl _IE_UART1
                                    133 	.globl _IE_PWM_I2C
                                    134 	.globl _IE_GPIO
                                    135 	.globl _IE_WDOG
                                    136 	.globl _PX0
                                    137 	.globl _PT0
                                    138 	.globl _PX1
                                    139 	.globl _PT1
                                    140 	.globl _PS
                                    141 	.globl _PT2
                                    142 	.globl _PL_FLAG
                                    143 	.globl _PH_FLAG
                                    144 	.globl _EX0
                                    145 	.globl _ET0
                                    146 	.globl _EX1
                                    147 	.globl _ET1
                                    148 	.globl _ES
                                    149 	.globl _ET2
                                    150 	.globl _E_DIS
                                    151 	.globl _EA
                                    152 	.globl _P
                                    153 	.globl _F1
                                    154 	.globl _OV
                                    155 	.globl _RS0
                                    156 	.globl _RS1
                                    157 	.globl _F0
                                    158 	.globl _AC
                                    159 	.globl _CY
                                    160 	.globl _I2CS_INT_ST
                                    161 	.globl _I2CX_INT
                                    162 	.globl _LED_STATUS
                                    163 	.globl _LED_DMA_H
                                    164 	.globl _LED_DMA_L
                                    165 	.globl _LED_DMA
                                    166 	.globl _LED_PWM_OE
                                    167 	.globl _LED_COMMON
                                    168 	.globl _ADC_CHAN
                                    169 	.globl _ADC_DAT_H
                                    170 	.globl _ADC_DAT_L
                                    171 	.globl _ADC_DAT
                                    172 	.globl _ADC_CTRL
                                    173 	.globl _SPI1_CK_SE
                                    174 	.globl _SPI1_CTRL
                                    175 	.globl _SPI1_DATA
                                    176 	.globl _SPI1_STAT
                                    177 	.globl _SIF1
                                    178 	.globl _SBAUD1
                                    179 	.globl _SBUF1
                                    180 	.globl _SCON1
                                    181 	.globl _SPI0_SETUP
                                    182 	.globl _SPI0_CK_SE
                                    183 	.globl _SPI0_CTRL
                                    184 	.globl _SPI0_DATA
                                    185 	.globl _SPI0_STAT
                                    186 	.globl _T2CAP1H
                                    187 	.globl _T2CAP1L
                                    188 	.globl _T2CAP1
                                    189 	.globl _TH2
                                    190 	.globl _TL2
                                    191 	.globl _T2COUNT
                                    192 	.globl _RCAP2H
                                    193 	.globl _RCAP2L
                                    194 	.globl _RCAP2
                                    195 	.globl _T2MOD
                                    196 	.globl _T2CON
                                    197 	.globl _SBUF
                                    198 	.globl _SCON
                                    199 	.globl _TH1
                                    200 	.globl _TH0
                                    201 	.globl _TL1
                                    202 	.globl _TL0
                                    203 	.globl _TMOD
                                    204 	.globl _TCON
                                    205 	.globl _XBUS_AUX
                                    206 	.globl _P7
                                    207 	.globl _P6_DIR
                                    208 	.globl _P6_OUT_PU
                                    209 	.globl _P6_IN
                                    210 	.globl _P5_DIR
                                    211 	.globl _P5_OUT_PU
                                    212 	.globl _P5_IN
                                    213 	.globl _P4_LED_KEY
                                    214 	.globl _P4_DIR_PU
                                    215 	.globl _P4_MOD_OC
                                    216 	.globl _P4
                                    217 	.globl _P3_DIR_PU
                                    218 	.globl _P3_MOD_OC
                                    219 	.globl _P3
                                    220 	.globl _P2_DIR_PU
                                    221 	.globl _P2_MOD_OC
                                    222 	.globl _P2
                                    223 	.globl _P1_DIR_PU
                                    224 	.globl _P1_MOD_OC
                                    225 	.globl _P1
                                    226 	.globl _P0_DIR_PU
                                    227 	.globl _P0_MOD_OC
                                    228 	.globl _P0
                                    229 	.globl _ROM_CTRL
                                    230 	.globl _ROM_DATA_HH
                                    231 	.globl _ROM_DATA_HL
                                    232 	.globl _ROM_DATA_HI
                                    233 	.globl _ROM_ADDR_H
                                    234 	.globl _ROM_ADDR_L
                                    235 	.globl _ROM_ADDR
                                    236 	.globl _GPIO_IE
                                    237 	.globl _IP_EX
                                    238 	.globl _IE_EX
                                    239 	.globl _IP
                                    240 	.globl _IE
                                    241 	.globl _WDOG_COUNT
                                    242 	.globl _RESET_KEEP
                                    243 	.globl _WAKE_CTRL
                                    244 	.globl _CLOCK_CFG
                                    245 	.globl _POWER_CFG
                                    246 	.globl _PCON
                                    247 	.globl _GLOBAL_CFG
                                    248 	.globl _SAFE_MOD
                                    249 	.globl _DPH
                                    250 	.globl _DPL
                                    251 	.globl _SP
                                    252 	.globl _A_INV
                                    253 	.globl _B
                                    254 	.globl _ACC
                                    255 	.globl _PSW
                                    256 	.globl _ak820_set_slot_rgb_PARM_4
                                    257 	.globl _ak820_set_slot_rgb_PARM_3
                                    258 	.globl _ak820_set_slot_rgb_PARM_2
                                    259 	.globl _ak820_scan_sample
                                    260 	.globl _ak820_scan_ready
                                    261 	.globl _ak820_scan_rows
                                    262 	.globl _ak820_led_dma
                                    263 	.globl _ak820_clock_init
                                    264 	.globl _ak820_board_init
                                    265 	.globl _ak820_led_irq
                                    266 	.globl _ak820_matrix_snapshot
                                    267 	.globl _ak820_set_slot_rgb
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
      00005D                        534 _ak820_matrix_snapshot_sloc0_1_0:
      00005D                        535 	.ds 3
                                    536 	.area	OSEG    (OVR,DATA)
      00005D                        537 _ak820_set_slot_rgb_sloc0_1_0:
      00005D                        538 	.ds 1
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
                           000200   560 _ak820_led_dma	=	0x0200
      000400                        561 _ak820_scan_rows::
      000400                        562 	.ds 16
      000410                        563 _ak820_scan_ready::
      000410                        564 	.ds 1
      000411                        565 _ak820_scan_sample::
      000411                        566 	.ds 1
      000412                        567 _ak820_matrix_snapshot_rows_10000_59:
      000412                        568 	.ds 3
      000415                        569 _ak820_matrix_snapshot_changed_10000_60:
      000415                        570 	.ds 1
      000416                        571 _ak820_set_slot_rgb_PARM_2:
      000416                        572 	.ds 1
      000417                        573 _ak820_set_slot_rgb_PARM_3:
      000417                        574 	.ds 1
      000418                        575 _ak820_set_slot_rgb_PARM_4:
      000418                        576 	.ds 1
      000419                        577 _ak820_set_slot_rgb_slot_10000_69:
      000419                        578 	.ds 1
                                    579 ;--------------------------------------------------------
                                    580 ; absolute external ram data
                                    581 ;--------------------------------------------------------
                                    582 	.area XABS    (ABS,XDATA)
                                    583 ;--------------------------------------------------------
                                    584 ; initialized external ram data
                                    585 ;--------------------------------------------------------
                                    586 	.area XISEG   (XDATA)
                                    587 	.area HOME    (CODE)
                                    588 	.area GSINIT0 (CODE)
                                    589 	.area GSINIT1 (CODE)
                                    590 	.area GSINIT2 (CODE)
                                    591 	.area GSINIT3 (CODE)
                                    592 	.area GSINIT4 (CODE)
                                    593 	.area GSINIT5 (CODE)
                                    594 	.area GSINIT  (CODE)
                                    595 	.area GSFINAL (CODE)
                                    596 	.area CSEG    (CODE)
                                    597 ;--------------------------------------------------------
                                    598 ; global & static initialisations
                                    599 ;--------------------------------------------------------
                                    600 	.area HOME    (CODE)
                                    601 	.area GSINIT  (CODE)
                                    602 	.area GSFINAL (CODE)
                                    603 	.area GSINIT  (CODE)
                                    604 ;--------------------------------------------------------
                                    605 ; Home
                                    606 ;--------------------------------------------------------
                                    607 	.area HOME    (CODE)
                                    608 	.area HOME    (CODE)
                                    609 ;--------------------------------------------------------
                                    610 ; code
                                    611 ;--------------------------------------------------------
                                    612 	.area CSEG    (CODE)
                                    613 ;------------------------------------------------------------
                                    614 ;Allocation info for local variables in function 'ak820_clock_init'
                                    615 ;------------------------------------------------------------
                                    616 ;	keyboards/ajazz/ak820/ak820_board.c:35: void ak820_clock_init(void) __naked {
                                    617 ;	-----------------------------------------
                                    618 ;	 function ak820_clock_init
                                    619 ;	-----------------------------------------
      003164                        620 _ak820_clock_init:
                                    621 ;	naked function: no prologue.
                                    622 ;	keyboards/ajazz/ak820/ak820_board.c:50: __endasm;
      003164 75 A1 55         [24]  623 	mov 0xa1, #0x55
      003167 75 A1 AA         [24]  624 	mov 0xa1, #0xaa
      00316A 43 B9 80         [24]  625 	orl 0xb9, #0x80
      00316D 53 B9 BF         [24]  626 	anl 0xb9, #0xbf
      003170 75 A1 55         [24]  627 	mov 0xa1, #0x55
      003173 75 A1 AA         [24]  628 	mov 0xa1, #0xaa
      003176 E5 B9            [12]  629 	mov a, 0xb9
      003178 54 F8            [12]  630 	anl a, #0xf8
      00317A 44 06            [12]  631 	orl a, #0x06
      00317C F5 B9            [12]  632 	mov 0xb9, a
      00317E E4               [12]  633 	clr a
      00317F F5 A1            [12]  634 	mov 0xa1, a
      003181 22               [24]  635 	ret
                                    636 ;	keyboards/ajazz/ak820/ak820_board.c:51: }
                                    637 ;	naked function: no epilogue.
                                    638 ;------------------------------------------------------------
                                    639 ;Allocation info for local variables in function 'ak820_board_init'
                                    640 ;------------------------------------------------------------
                                    641 ;i             Allocated with name '_ak820_board_init_i_10000_52'
                                    642 ;------------------------------------------------------------
                                    643 ;	keyboards/ajazz/ak820/ak820_board.c:53: void ak820_board_init(void) {
                                    644 ;	-----------------------------------------
                                    645 ;	 function ak820_board_init
                                    646 ;	-----------------------------------------
      003182                        647 _ak820_board_init:
                           000007   648 	ar7 = 0x07
                           000006   649 	ar6 = 0x06
                           000005   650 	ar5 = 0x05
                           000004   651 	ar4 = 0x04
                           000003   652 	ar3 = 0x03
                           000002   653 	ar2 = 0x02
                           000001   654 	ar1 = 0x01
                           000000   655 	ar0 = 0x00
                                    656 ;	keyboards/ajazz/ak820/ak820_board.c:56: IE_PWM_I2C = 0;
                                    657 ;	assignBit
      003182 C2 ED            [12]  658 	clr	_IE_PWM_I2C
                                    659 ;	keyboards/ajazz/ak820/ak820_board.c:57: for (i = 0; i < AK820_LED_DMA_BYTES; ++i) {
      003184 7E 00            [12]  660 	mov	r6,#0x00
      003186 7F 00            [12]  661 	mov	r7,#0x00
      003188                        662 00103$:
                                    663 ;	keyboards/ajazz/ak820/ak820_board.c:58: ak820_led_dma[i] = 0;
      003188 8E 82            [24]  664 	mov	dpl,r6
      00318A 74 02            [12]  665 	mov	a,#(_ak820_led_dma >> 8)
      00318C 2F               [12]  666 	add	a,r7
      00318D F5 83            [12]  667 	mov	dph,a
      00318F E4               [12]  668 	clr	a
      003190 F0               [24]  669 	movx	@dptr,a
                                    670 ;	keyboards/ajazz/ak820/ak820_board.c:57: for (i = 0; i < AK820_LED_DMA_BYTES; ++i) {
      003191 0E               [12]  671 	inc	r6
      003192 BE 00 01         [24]  672 	cjne	r6,#0x00,00139$
      003195 0F               [12]  673 	inc	r7
      003196                        674 00139$:
      003196 8E 04            [24]  675 	mov	ar4,r6
      003198 8F 05            [24]  676 	mov	ar5,r7
      00319A 74 FE            [12]  677 	mov	a,#0x100 - 0x02
      00319C 2D               [12]  678 	add	a,r5
      00319D 50 E9            [24]  679 	jnc	00103$
                                    680 ;	keyboards/ajazz/ak820/ak820_board.c:60: for (i = 0; i < AK820_SCAN_ROWS; ++i) {
      00319F 7E 00            [12]  681 	mov	r6,#0x00
      0031A1 7F 00            [12]  682 	mov	r7,#0x00
      0031A3                        683 00105$:
                                    684 ;	keyboards/ajazz/ak820/ak820_board.c:61: ak820_scan_rows[i] = 0;
      0031A3 EE               [12]  685 	mov	a,r6
      0031A4 24 00            [12]  686 	add	a, #_ak820_scan_rows
      0031A6 F5 82            [12]  687 	mov	dpl,a
      0031A8 EF               [12]  688 	mov	a,r7
      0031A9 34 04            [12]  689 	addc	a, #(_ak820_scan_rows >> 8)
      0031AB F5 83            [12]  690 	mov	dph,a
      0031AD E4               [12]  691 	clr	a
      0031AE F0               [24]  692 	movx	@dptr,a
                                    693 ;	keyboards/ajazz/ak820/ak820_board.c:60: for (i = 0; i < AK820_SCAN_ROWS; ++i) {
      0031AF 0E               [12]  694 	inc	r6
      0031B0 BE 00 01         [24]  695 	cjne	r6,#0x00,00141$
      0031B3 0F               [12]  696 	inc	r7
      0031B4                        697 00141$:
      0031B4 8E 04            [24]  698 	mov	ar4,r6
      0031B6 8F 05            [24]  699 	mov	ar5,r7
      0031B8 C3               [12]  700 	clr	c
      0031B9 EC               [12]  701 	mov	a,r4
      0031BA 94 10            [12]  702 	subb	a,#0x10
      0031BC ED               [12]  703 	mov	a,r5
      0031BD 94 00            [12]  704 	subb	a,#0x00
      0031BF 40 E2            [24]  705 	jc	00105$
                                    706 ;	keyboards/ajazz/ak820/ak820_board.c:63: ak820_scan_ready  = 0;
      0031C1 90 04 10         [24]  707 	mov	dptr,#_ak820_scan_ready
      0031C4 E4               [12]  708 	clr	a
      0031C5 F0               [24]  709 	movx	@dptr,a
                                    710 ;	keyboards/ajazz/ak820/ak820_board.c:64: ak820_scan_sample = 0;
      0031C6 90 04 11         [24]  711 	mov	dptr,#_ak820_scan_sample
      0031C9 F0               [24]  712 	movx	@dptr,a
                                    713 ;	keyboards/ajazz/ak820/ak820_board.c:67: P4 = P2 = P1 = P3 = P0 = 0xff;
      0031CA 75 80 FF         [24]  714 	mov	_P0,#0xff
      0031CD 75 B0 FF         [24]  715 	mov	_P3,#0xff
      0031D0 75 90 FF         [24]  716 	mov	_P1,#0xff
      0031D3 75 A0 FF         [24]  717 	mov	_P2,#0xff
      0031D6 75 C0 FF         [24]  718 	mov	_P4,#0xff
                                    719 ;	keyboards/ajazz/ak820/ak820_board.c:68: P1_MOD_OC = P2_MOD_OC = P4_MOD_OC = P3_MOD_OC = P0_MOD_OC = 0;
      0031D9 F5 C4            [12]  720 	mov	_P0_MOD_OC,a
      0031DB F5 96            [12]  721 	mov	_P3_MOD_OC,a
      0031DD F5 C2            [12]  722 	mov	_P4_MOD_OC,a
      0031DF F5 94            [12]  723 	mov	_P2_MOD_OC,a
      0031E1 F5 92            [12]  724 	mov	_P1_MOD_OC,a
                                    725 ;	keyboards/ajazz/ak820/ak820_board.c:70: LED_CTRL    = 0x01;
      0031E3 90 21 D1         [24]  726 	mov	dptr,#0x21d1
      0031E6 04               [12]  727 	inc	a
      0031E7 F0               [24]  728 	movx	@dptr,a
                                    729 ;	keyboards/ajazz/ak820/ak820_board.c:71: LED_CYCLE   = 0x30;
      0031E8 A3               [24]  730 	inc	dptr
      0031E9 74 30            [12]  731 	mov	a,#0x30
      0031EB F0               [24]  732 	movx	@dptr,a
                                    733 ;	keyboards/ajazz/ak820/ak820_board.c:72: LED_FRAME   = 0x50;
      0031EC A3               [24]  734 	inc	dptr
      0031ED 74 50            [12]  735 	mov	a,#0x50
      0031EF F0               [24]  736 	movx	@dptr,a
                                    737 ;	keyboards/ajazz/ak820/ak820_board.c:73: LED_DMA_H   = AK820_LED_DMA_ADDRESS >> 8;
      0031F0 75 C7 02         [24]  738 	mov	_LED_DMA_H,#0x02
                                    739 ;	keyboards/ajazz/ak820/ak820_board.c:74: LED_DMA_L   = AK820_LED_DMA_ADDRESS & 0xff;
      0031F3 75 C6 00         [24]  740 	mov	_LED_DMA_L,#0x00
                                    741 ;	keyboards/ajazz/ak820/ak820_board.c:75: LED_INT_ADJ = 0;
      0031F6 90 21 D8         [24]  742 	mov	dptr,#0x21d8
      0031F9 E4               [12]  743 	clr	a
      0031FA F0               [24]  744 	movx	@dptr,a
                                    745 ;	keyboards/ajazz/ak820/ak820_board.c:76: LED_PWM_OE  = 0xff;
      0031FB 75 A7 FF         [24]  746 	mov	_LED_PWM_OE,#0xff
                                    747 ;	keyboards/ajazz/ak820/ak820_board.c:77: LED_COMMON  = 0xff;
      0031FE 75 A6 FF         [24]  748 	mov	_LED_COMMON,#0xff
                                    749 ;	keyboards/ajazz/ak820/ak820_board.c:78: LED_CTRL    = 0xfd;
      003201 90 21 D1         [24]  750 	mov	dptr,#0x21d1
      003204 74 FD            [12]  751 	mov	a,#0xfd
      003206 F0               [24]  752 	movx	@dptr,a
                                    753 ;	keyboards/ajazz/ak820/ak820_board.c:81: P7 = 0x03;
      003207 75 F1 03         [24]  754 	mov	_P7,#0x03
                                    755 ;	keyboards/ajazz/ak820/ak820_board.c:83: LED_STATUS |= 0x40;
      00320A 43 F7 40         [24]  756 	orl	_LED_STATUS,#0x40
                                    757 ;	keyboards/ajazz/ak820/ak820_board.c:84: IE_PWM_I2C = 1;
                                    758 ;	assignBit
      00320D D2 ED            [12]  759 	setb	_IE_PWM_I2C
                                    760 ;	keyboards/ajazz/ak820/ak820_board.c:85: LED_RED_ADJ = LED_GRE_ADJ = LED_BLU_ADJ = 0;
      00320F 90 21 DB         [24]  761 	mov	dptr,#0x21db
      003212 E4               [12]  762 	clr	a
      003213 F0               [24]  763 	movx	@dptr,a
      003214 15 82            [12]  764 	dec	dpl
      003216 F0               [24]  765 	movx	@dptr,a
      003217 15 82            [12]  766 	dec	dpl
      003219 F0               [24]  767 	movx	@dptr,a
                                    768 ;	keyboards/ajazz/ak820/ak820_board.c:86: }
      00321A 22               [24]  769 	ret
                                    770 ;------------------------------------------------------------
                                    771 ;Allocation info for local variables in function 'ak820_led_irq'
                                    772 ;------------------------------------------------------------
                                    773 ;	keyboards/ajazz/ak820/ak820_board.c:96: void ak820_led_irq(void) __naked {
                                    774 ;	-----------------------------------------
                                    775 ;	 function ak820_led_irq
                                    776 ;	-----------------------------------------
      00321B                        777 _ak820_led_irq:
                                    778 ;	naked function: no prologue.
                                    779 ;	keyboards/ajazz/ak820/ak820_board.c:260: __endasm;
      00321B 05 A6            [12]  780 	inc 0xa6
      00321D E5 A6            [12]  781 	mov a, 0xa6
      00321F 54 0F            [12]  782 	anl a, #0x0f
      003221 FE               [12]  783 	mov r6, a
      003222 70 09            [24]  784 	jnz 00001$
      003224 75 A6 10         [24]  785 	mov 0xa6, #0x10
      003227 75 C7 02         [24]  786 	mov 0xc7, #0x02
      00322A 75 C6 00         [24]  787 	mov 0xc6, #0x00
      00322D                        788 00001$:
      00322D 12 32 88         [24]  789 	lcall 00010$
                                    790 ; Native D5ED..D617, only the sample XRAM address is relocated.
      003230 75 C1 FF         [24]  791 	mov 0xc1, #0xff
      003233 75 C2 FF         [24]  792 	mov 0xc2, #0xff
      003236 00               [12]  793 	nop
      003237 00               [12]  794 	nop
      003238 90 21 D1         [24]  795 	mov dptr, #0x21d1
      00323B E0               [24]  796 	movx a, @dptr
      00323C 00               [12]  797 	nop
      00323D 00               [12]  798 	nop
      00323E 00               [12]  799 	nop
      00323F 00               [12]  800 	nop
      003240 00               [12]  801 	nop
      003241 00               [12]  802 	nop
      003242 00               [12]  803 	nop
      003243 00               [12]  804 	nop
      003244 00               [12]  805 	nop
      003245 00               [12]  806 	nop
      003246 00               [12]  807 	nop
      003247 00               [12]  808 	nop
      003248 00               [12]  809 	nop
      003249 00               [12]  810 	nop
      00324A 00               [12]  811 	nop
      00324B 00               [12]  812 	nop
      00324C 00               [12]  813 	nop
      00324D 00               [12]  814 	nop
      00324E 00               [12]  815 	nop
      00324F 00               [12]  816 	nop
      003250 00               [12]  817 	nop
      003251 00               [12]  818 	nop
      003252 00               [12]  819 	nop
      003253 00               [12]  820 	nop
      003254 00               [12]  821 	nop
      003255 90 04 11         [24]  822 	mov dptr, #_ak820_scan_sample
      003258 E5 C0            [12]  823 	mov a, 0xc0
      00325A F0               [24]  824 	movx @dptr, a
      00325B E4               [12]  825 	clr a
      00325C F5 C2            [12]  826 	mov 0xc2, a
      00325E F5 C1            [12]  827 	mov 0xc1, a
      003260 75 A7 FF         [24]  828 	mov 0xa7, #0xff
      003263 75 B0 FF         [24]  829 	mov 0xb0, #0xff
      003266 75 80 FF         [24]  830 	mov 0x80, #0xff
      003269 90 04 11         [24]  831 	mov dptr, #_ak820_scan_sample
      00326C E0               [24]  832 	movx a, @dptr
      00326D F4               [12]  833 	cpl a
      00326E FD               [12]  834 	mov r5, a
      00326F 90 04 00         [24]  835 	mov dptr, #_ak820_scan_rows
      003272 E5 82            [12]  836 	mov a, dpl
      003274 2E               [12]  837 	add a, r6
      003275 F5 82            [12]  838 	mov dpl, a
      003277 E4               [12]  839 	clr a
      003278 35 83            [12]  840 	addc a, dph
      00327A F5 83            [12]  841 	mov dph, a
      00327C ED               [12]  842 	mov a, r5
      00327D F0               [24]  843 	movx @dptr, a
      00327E BE 0F 06         [24]  844 	cjne r6, #0x0f, 00002$
      003281 90 04 10         [24]  845 	mov dptr, #_ak820_scan_ready
      003284 74 01            [12]  846 	mov a, #1
      003286 F0               [24]  847 	movx @dptr, a
      003287                        848 00002$:
      003287 22               [24]  849 	ret
                                    850 ; Native E274..E29D: the32 MOVX operations feed the peripheral DMA.
      003288                        851 00010$:
      003288 D2 AE            [12]  852 	setb 0xae
      00328A D2 D0            [12]  853 	setb 0xd0
      00328C E0               [24]  854 	movx a, @dptr
      00328D E0               [24]  855 	movx a, @dptr
      00328E E0               [24]  856 	movx a, @dptr
      00328F E0               [24]  857 	movx a, @dptr
      003290 E0               [24]  858 	movx a, @dptr
      003291 E0               [24]  859 	movx a, @dptr
      003292 E0               [24]  860 	movx a, @dptr
      003293 E0               [24]  861 	movx a, @dptr
      003294 00               [12]  862 	nop
      003295 E0               [24]  863 	movx a, @dptr
      003296 E0               [24]  864 	movx a, @dptr
      003297 E0               [24]  865 	movx a, @dptr
      003298 E0               [24]  866 	movx a, @dptr
      003299 E0               [24]  867 	movx a, @dptr
      00329A E0               [24]  868 	movx a, @dptr
      00329B E0               [24]  869 	movx a, @dptr
      00329C E0               [24]  870 	movx a, @dptr
      00329D 00               [12]  871 	nop
      00329E E0               [24]  872 	movx a, @dptr
      00329F E0               [24]  873 	movx a, @dptr
      0032A0 E0               [24]  874 	movx a, @dptr
      0032A1 E0               [24]  875 	movx a, @dptr
      0032A2 E0               [24]  876 	movx a, @dptr
      0032A3 E0               [24]  877 	movx a, @dptr
      0032A4 E0               [24]  878 	movx a, @dptr
      0032A5 E0               [24]  879 	movx a, @dptr
      0032A6 00               [12]  880 	nop
      0032A7 E0               [24]  881 	movx a, @dptr
      0032A8 E0               [24]  882 	movx a, @dptr
      0032A9 E0               [24]  883 	movx a, @dptr
      0032AA E0               [24]  884 	movx a, @dptr
      0032AB E0               [24]  885 	movx a, @dptr
      0032AC E0               [24]  886 	movx a, @dptr
      0032AD E0               [24]  887 	movx a, @dptr
      0032AE E0               [24]  888 	movx a, @dptr
      0032AF C2 AE            [12]  889 	clr 0xae
                                    890 ; Native E29D..E2E0, with the jump table relocated locally.
      0032B1 E5 A6            [12]  891 	mov a, 0xa6
      0032B3 10 E4 08         [24]  892 	jbc 0xe4, 00011$
      0032B6 54 01            [12]  893 	anl a, #1
      0032B8 04               [12]  894 	inc a
      0032B9 F4               [12]  895 	cpl a
      0032BA 14               [12]  896 	dec a
      0032BB 52 F1            [12]  897 	anl 0xf1, a
      0032BD 22               [24]  898 	ret
      0032BE                        899 00011$:
      0032BE FF               [12]  900 	mov r7, a
      0032BF 2F               [12]  901 	add a, r7
      0032C0 2F               [12]  902 	add a, r7
      0032C1 90 32 C5         [24]  903 	mov dptr, #00012$
      0032C4 73               [24]  904 	jmp @a+dptr
      0032C5                        905 00012$:
      0032C5 C2 80            [12]  906 	clr 0x80
      0032C7 22               [24]  907 	ret
      0032C8 C2 81            [12]  908 	clr 0x81
      0032CA 22               [24]  909 	ret
      0032CB C2 82            [12]  910 	clr 0x82
      0032CD 22               [24]  911 	ret
      0032CE C2 83            [12]  912 	clr 0x83
      0032D0 22               [24]  913 	ret
      0032D1 C2 84            [12]  914 	clr 0x84
      0032D3 22               [24]  915 	ret
      0032D4 C2 85            [12]  916 	clr 0x85
      0032D6 22               [24]  917 	ret
      0032D7 C2 86            [12]  918 	clr 0x86
      0032D9 22               [24]  919 	ret
      0032DA C2 87            [12]  920 	clr 0x87
      0032DC 22               [24]  921 	ret
      0032DD C2 B0            [12]  922 	clr 0xb0
      0032DF 22               [24]  923 	ret
      0032E0 C2 B1            [12]  924 	clr 0xb1
      0032E2 22               [24]  925 	ret
      0032E3 C2 B2            [12]  926 	clr 0xb2
      0032E5 22               [24]  927 	ret
      0032E6 C2 B3            [12]  928 	clr 0xb3
      0032E8 22               [24]  929 	ret
      0032E9 C2 B4            [12]  930 	clr 0xb4
      0032EB 22               [24]  931 	ret
      0032EC C2 B5            [12]  932 	clr 0xb5
      0032EE 22               [24]  933 	ret
      0032EF C2 B6            [12]  934 	clr 0xb6
      0032F1 22               [24]  935 	ret
      0032F2 C2 B7            [12]  936 	clr 0xb7
      0032F4 22               [24]  937 	ret
                                    938 ;	keyboards/ajazz/ak820/ak820_board.c:261: }
                                    939 ;	naked function: no epilogue.
                                    940 ;------------------------------------------------------------
                                    941 ;Allocation info for local variables in function 'ak820_matrix_snapshot'
                                    942 ;------------------------------------------------------------
                                    943 ;rows          Allocated with name '_ak820_matrix_snapshot_rows_10000_59'
                                    944 ;row           Allocated with name '_ak820_matrix_snapshot_row_10000_60'
                                    945 ;value         Allocated with name '_ak820_matrix_snapshot_value_10000_60'
                                    946 ;irq_enabled   Allocated with name '_ak820_matrix_snapshot_irq_enabled_10000_60'
                                    947 ;changed       Allocated with name '_ak820_matrix_snapshot_changed_10000_60'
                                    948 ;sloc0         Allocated with name '_ak820_matrix_snapshot_sloc0_1_0'
                                    949 ;------------------------------------------------------------
                                    950 ;	keyboards/ajazz/ak820/ak820_board.c:263: bool ak820_matrix_snapshot(uint8_t *rows) {
                                    951 ;	-----------------------------------------
                                    952 ;	 function ak820_matrix_snapshot
                                    953 ;	-----------------------------------------
      0032F5                        954 _ak820_matrix_snapshot:
      0032F5 AF F0            [24]  955 	mov	r7,b
      0032F7 AE 83            [24]  956 	mov	r6,dph
      0032F9 E5 82            [12]  957 	mov	a,dpl
      0032FB 90 04 12         [24]  958 	mov	dptr,#_ak820_matrix_snapshot_rows_10000_59
      0032FE F0               [24]  959 	movx	@dptr,a
      0032FF EE               [12]  960 	mov	a,r6
      003300 A3               [24]  961 	inc	dptr
      003301 F0               [24]  962 	movx	@dptr,a
      003302 EF               [12]  963 	mov	a,r7
      003303 A3               [24]  964 	inc	dptr
      003304 F0               [24]  965 	movx	@dptr,a
                                    966 ;	keyboards/ajazz/ak820/ak820_board.c:267: bool changed = false;
      003305 90 04 15         [24]  967 	mov	dptr,#_ak820_matrix_snapshot_changed_10000_60
      003308 E4               [12]  968 	clr	a
      003309 F0               [24]  969 	movx	@dptr,a
                                    970 ;	keyboards/ajazz/ak820/ak820_board.c:269: if (!ak820_scan_ready) {
      00330A 90 04 10         [24]  971 	mov	dptr,#_ak820_scan_ready
      00330D E0               [24]  972 	movx	a,@dptr
                                    973 ;	keyboards/ajazz/ak820/ak820_board.c:270: return false;
      00330E 70 03            [24]  974 	jnz	00102$
      003310 F5 82            [12]  975 	mov	dpl,a
      003312 22               [24]  976 	ret
      003313                        977 00102$:
                                    978 ;	keyboards/ajazz/ak820/ak820_board.c:274: irq_enabled = IE_EX & 0x20;
      003313 E5 E8            [12]  979 	mov	a,_IE_EX
      003315 54 20            [12]  980 	anl	a,#0x20
      003317 FF               [12]  981 	mov	r7,a
                                    982 ;	keyboards/ajazz/ak820/ak820_board.c:275: IE_PWM_I2C = 0;
                                    983 ;	assignBit
      003318 C2 ED            [12]  984 	clr	_IE_PWM_I2C
                                    985 ;	keyboards/ajazz/ak820/ak820_board.c:276: ak820_scan_ready = 0;
      00331A 90 04 10         [24]  986 	mov	dptr,#_ak820_scan_ready
      00331D E4               [12]  987 	clr	a
      00331E F0               [24]  988 	movx	@dptr,a
                                    989 ;	keyboards/ajazz/ak820/ak820_board.c:277: for (row = 0; row < AK820_SCAN_ROWS; ++row) {
      00331F 90 04 12         [24]  990 	mov	dptr,#_ak820_matrix_snapshot_rows_10000_59
      003322 E0               [24]  991 	movx	a,@dptr
      003323 FC               [12]  992 	mov	r4,a
      003324 A3               [24]  993 	inc	dptr
      003325 E0               [24]  994 	movx	a,@dptr
      003326 FD               [12]  995 	mov	r5,a
      003327 A3               [24]  996 	inc	dptr
      003328 E0               [24]  997 	movx	a,@dptr
      003329 FE               [12]  998 	mov	r6,a
      00332A 7B 00            [12]  999 	mov	r3,#0x00
      00332C                       1000 00108$:
                                   1001 ;	keyboards/ajazz/ak820/ak820_board.c:278: value = ak820_scan_rows[row];
      00332C EB               [12] 1002 	mov	a,r3
      00332D 24 00            [12] 1003 	add	a, #_ak820_scan_rows
      00332F F5 82            [12] 1004 	mov	dpl,a
      003331 E4               [12] 1005 	clr	a
      003332 34 04            [12] 1006 	addc	a, #(_ak820_scan_rows >> 8)
      003334 F5 83            [12] 1007 	mov	dph,a
      003336 E0               [24] 1008 	movx	a,@dptr
      003337 FA               [12] 1009 	mov	r2,a
                                   1010 ;	keyboards/ajazz/ak820/ak820_board.c:280: value &= ak820_matrix_mask[row];
      003338 EB               [12] 1011 	mov	a,r3
      003339 90 B5 B7         [24] 1012 	mov	dptr,#_ak820_matrix_mask
      00333C 93               [24] 1013 	movc	a,@a+dptr
      00333D 52 02            [12] 1014 	anl	ar2,a
                                   1015 ;	keyboards/ajazz/ak820/ak820_board.c:282: if (rows[row] != value) {
      00333F EB               [12] 1016 	mov	a,r3
      003340 2C               [12] 1017 	add	a, r4
      003341 F5 5D            [12] 1018 	mov	_ak820_matrix_snapshot_sloc0_1_0,a
      003343 E4               [12] 1019 	clr	a
      003344 3D               [12] 1020 	addc	a, r5
      003345 F5 5E            [12] 1021 	mov	(_ak820_matrix_snapshot_sloc0_1_0 + 1),a
      003347 8E 5F            [24] 1022 	mov	(_ak820_matrix_snapshot_sloc0_1_0 + 2),r6
      003349 85 5D 82         [24] 1023 	mov	dpl,_ak820_matrix_snapshot_sloc0_1_0
      00334C 85 5E 83         [24] 1024 	mov	dph,(_ak820_matrix_snapshot_sloc0_1_0 + 1)
      00334F 85 5F F0         [24] 1025 	mov	b,(_ak820_matrix_snapshot_sloc0_1_0 + 2)
      003352 12 B5 97         [24] 1026 	lcall	__gptrget
      003355 B5 02 02         [24] 1027 	cjne	a,ar2,00149$
      003358 80 13            [24] 1028 	sjmp	00109$
      00335A                       1029 00149$:
                                   1030 ;	keyboards/ajazz/ak820/ak820_board.c:283: rows[row] = value;
      00335A 85 5D 82         [24] 1031 	mov	dpl,_ak820_matrix_snapshot_sloc0_1_0
      00335D 85 5E 83         [24] 1032 	mov	dph,(_ak820_matrix_snapshot_sloc0_1_0 + 1)
      003360 85 5F F0         [24] 1033 	mov	b,(_ak820_matrix_snapshot_sloc0_1_0 + 2)
      003363 EA               [12] 1034 	mov	a,r2
      003364 12 B5 5C         [24] 1035 	lcall	__gptrput
                                   1036 ;	keyboards/ajazz/ak820/ak820_board.c:284: changed = true;
      003367 90 04 15         [24] 1037 	mov	dptr,#_ak820_matrix_snapshot_changed_10000_60
      00336A 74 01            [12] 1038 	mov	a,#0x01
      00336C F0               [24] 1039 	movx	@dptr,a
      00336D                       1040 00109$:
                                   1041 ;	keyboards/ajazz/ak820/ak820_board.c:277: for (row = 0; row < AK820_SCAN_ROWS; ++row) {
      00336D 0B               [12] 1042 	inc	r3
      00336E BB 10 00         [24] 1043 	cjne	r3,#0x10,00150$
      003371                       1044 00150$:
      003371 40 B9            [24] 1045 	jc	00108$
                                   1046 ;	keyboards/ajazz/ak820/ak820_board.c:287: if (irq_enabled) {
      003373 EF               [12] 1047 	mov	a,r7
      003374 60 02            [24] 1048 	jz	00107$
                                   1049 ;	keyboards/ajazz/ak820/ak820_board.c:288: IE_PWM_I2C = 1;
                                   1050 ;	assignBit
      003376 D2 ED            [12] 1051 	setb	_IE_PWM_I2C
      003378                       1052 00107$:
                                   1053 ;	keyboards/ajazz/ak820/ak820_board.c:290: return changed;
      003378 90 04 15         [24] 1054 	mov	dptr,#_ak820_matrix_snapshot_changed_10000_60
      00337B E0               [24] 1055 	movx	a,@dptr
                                   1056 ;	keyboards/ajazz/ak820/ak820_board.c:291: }
      00337C F5 82            [12] 1057 	mov	dpl,a
      00337E 22               [24] 1058 	ret
                                   1059 ;------------------------------------------------------------
                                   1060 ;Allocation info for local variables in function 'ak820_set_slot_rgb'
                                   1061 ;------------------------------------------------------------
                                   1062 ;r             Allocated with name '_ak820_set_slot_rgb_PARM_2'
                                   1063 ;g             Allocated with name '_ak820_set_slot_rgb_PARM_3'
                                   1064 ;b             Allocated with name '_ak820_set_slot_rgb_PARM_4'
                                   1065 ;slot          Allocated with name '_ak820_set_slot_rgb_slot_10000_69'
                                   1066 ;offset        Allocated with name '_ak820_set_slot_rgb_offset_10000_70'
                                   1067 ;irq_enabled   Allocated with name '_ak820_set_slot_rgb_irq_enabled_10000_70'
                                   1068 ;sloc0         Allocated with name '_ak820_set_slot_rgb_sloc0_1_0'
                                   1069 ;------------------------------------------------------------
                                   1070 ;	keyboards/ajazz/ak820/ak820_board.c:293: void ak820_set_slot_rgb(uint8_t slot, uint8_t r, uint8_t g, uint8_t b) {
                                   1071 ;	-----------------------------------------
                                   1072 ;	 function ak820_set_slot_rgb
                                   1073 ;	-----------------------------------------
      00337F                       1074 _ak820_set_slot_rgb:
      00337F E5 82            [12] 1075 	mov	a,dpl
      003381 90 04 19         [24] 1076 	mov	dptr,#_ak820_set_slot_rgb_slot_10000_69
      003384 F0               [24] 1077 	movx	@dptr,a
                                   1078 ;	keyboards/ajazz/ak820/ak820_board.c:296: if (slot >= AK820_SCAN_ROWS * AK820_SCAN_COLS) {
      003385 E0               [24] 1079 	movx	a,@dptr
      003386 FF               [12] 1080 	mov	r7,a
      003387 BF 80 00         [24] 1081 	cjne	r7,#0x80,00130$
      00338A                       1082 00130$:
      00338A 40 01            [24] 1083 	jc	00102$
                                   1084 ;	keyboards/ajazz/ak820/ak820_board.c:297: return;
      00338C 22               [24] 1085 	ret
      00338D                       1086 00102$:
                                   1087 ;	keyboards/ajazz/ak820/ak820_board.c:299: offset = (uint16_t)slot * 4;
      00338D 7E 00            [12] 1088 	mov	r6,#0x00
      00338F EF               [12] 1089 	mov	a,r7
      003390 2F               [12] 1090 	add	a,r7
      003391 FF               [12] 1091 	mov	r7,a
      003392 EE               [12] 1092 	mov	a,r6
      003393 33               [12] 1093 	rlc	a
      003394 FE               [12] 1094 	mov	r6,a
      003395 EF               [12] 1095 	mov	a,r7
      003396 2F               [12] 1096 	add	a,r7
      003397 FF               [12] 1097 	mov	r7,a
      003398 EE               [12] 1098 	mov	a,r6
      003399 33               [12] 1099 	rlc	a
      00339A FE               [12] 1100 	mov	r6,a
                                   1101 ;	keyboards/ajazz/ak820/ak820_board.c:300: irq_enabled = IE_EX & 0x20;
      00339B E5 E8            [12] 1102 	mov	a,_IE_EX
      00339D 54 20            [12] 1103 	anl	a,#0x20
      00339F FD               [12] 1104 	mov	r5,a
                                   1105 ;	keyboards/ajazz/ak820/ak820_board.c:301: IE_PWM_I2C = 0;
                                   1106 ;	assignBit
      0033A0 C2 ED            [12] 1107 	clr	_IE_PWM_I2C
                                   1108 ;	keyboards/ajazz/ak820/ak820_board.c:304: ak820_led_dma[offset]     = (r | g | b) ? 0xff : 0;
      0033A2 8F 03            [24] 1109 	mov	ar3,r7
      0033A4 74 02            [12] 1110 	mov	a,#(_ak820_led_dma >> 8)
      0033A6 2E               [12] 1111 	add	a,r6
      0033A7 FC               [12] 1112 	mov	r4,a
      0033A8 90 04 17         [24] 1113 	mov	dptr,#_ak820_set_slot_rgb_PARM_3
      0033AB E0               [24] 1114 	movx	a,@dptr
      0033AC FA               [12] 1115 	mov	r2,a
      0033AD 90 04 16         [24] 1116 	mov	dptr,#_ak820_set_slot_rgb_PARM_2
      0033B0 E0               [24] 1117 	movx	a,@dptr
      0033B1 F9               [12] 1118 	mov	r1,a
      0033B2 4A               [12] 1119 	orl	a,r2
      0033B3 F8               [12] 1120 	mov	r0,a
      0033B4 90 04 18         [24] 1121 	mov	dptr,#_ak820_set_slot_rgb_PARM_4
      0033B7 E0               [24] 1122 	movx	a,@dptr
      0033B8 F5 5D            [12] 1123 	mov	_ak820_set_slot_rgb_sloc0_1_0,a
      0033BA 48               [12] 1124 	orl	a,r0
      0033BB 60 02            [24] 1125 	jz	00107$
      0033BD 74 FF            [12] 1126 	mov	a,#0xff
      0033BF                       1127 00107$:
      0033BF F8               [12] 1128 	mov	r0,a
      0033C0 8B 82            [24] 1129 	mov	dpl,r3
      0033C2 8C 83            [24] 1130 	mov	dph,r4
      0033C4 E8               [12] 1131 	mov	a,r0
      0033C5 F0               [24] 1132 	movx	@dptr,a
                                   1133 ;	keyboards/ajazz/ak820/ak820_board.c:305: ak820_led_dma[offset + 1] = r;
      0033C6 74 01            [12] 1134 	mov	a,#0x01
      0033C8 2F               [12] 1135 	add	a, r7
      0033C9 FB               [12] 1136 	mov	r3,a
      0033CA E4               [12] 1137 	clr	a
      0033CB 3E               [12] 1138 	addc	a, r6
      0033CC FC               [12] 1139 	mov	r4,a
      0033CD 8B 82            [24] 1140 	mov	dpl,r3
      0033CF 74 02            [12] 1141 	mov	a,#(_ak820_led_dma >> 8)
      0033D1 2C               [12] 1142 	add	a,r4
      0033D2 F5 83            [12] 1143 	mov	dph,a
      0033D4 E9               [12] 1144 	mov	a,r1
      0033D5 F0               [24] 1145 	movx	@dptr,a
                                   1146 ;	keyboards/ajazz/ak820/ak820_board.c:306: ak820_led_dma[offset + 2] = g;
      0033D6 74 02            [12] 1147 	mov	a,#0x02
      0033D8 2F               [12] 1148 	add	a, r7
      0033D9 FB               [12] 1149 	mov	r3,a
      0033DA E4               [12] 1150 	clr	a
      0033DB 3E               [12] 1151 	addc	a, r6
      0033DC FC               [12] 1152 	mov	r4,a
      0033DD 8B 82            [24] 1153 	mov	dpl,r3
      0033DF 74 02            [12] 1154 	mov	a,#(_ak820_led_dma >> 8)
      0033E1 2C               [12] 1155 	add	a,r4
      0033E2 F5 83            [12] 1156 	mov	dph,a
      0033E4 EA               [12] 1157 	mov	a,r2
      0033E5 F0               [24] 1158 	movx	@dptr,a
                                   1159 ;	keyboards/ajazz/ak820/ak820_board.c:307: ak820_led_dma[offset + 3] = b;
      0033E6 74 03            [12] 1160 	mov	a,#0x03
      0033E8 2F               [12] 1161 	add	a, r7
      0033E9 FF               [12] 1162 	mov	r7,a
      0033EA E4               [12] 1163 	clr	a
      0033EB 3E               [12] 1164 	addc	a, r6
      0033EC FE               [12] 1165 	mov	r6,a
      0033ED 8F 82            [24] 1166 	mov	dpl,r7
      0033EF 74 02            [12] 1167 	mov	a,#(_ak820_led_dma >> 8)
      0033F1 2E               [12] 1168 	add	a,r6
      0033F2 F5 83            [12] 1169 	mov	dph,a
      0033F4 E5 5D            [12] 1170 	mov	a,_ak820_set_slot_rgb_sloc0_1_0
      0033F6 F0               [24] 1171 	movx	@dptr,a
                                   1172 ;	keyboards/ajazz/ak820/ak820_board.c:308: if (irq_enabled) {
      0033F7 ED               [12] 1173 	mov	a,r5
      0033F8 60 02            [24] 1174 	jz	00105$
                                   1175 ;	keyboards/ajazz/ak820/ak820_board.c:309: IE_PWM_I2C = 1;
                                   1176 ;	assignBit
      0033FA D2 ED            [12] 1177 	setb	_IE_PWM_I2C
      0033FC                       1178 00105$:
                                   1179 ;	keyboards/ajazz/ak820/ak820_board.c:311: }
      0033FC 22               [24] 1180 	ret
                                   1181 ;------------------------------------------------------------
                                   1182 ;Allocation info for local variables in function 'rgb_matrix_check_finished_leds'
                                   1183 ;------------------------------------------------------------
                                   1184 ;led_idx       Allocated with name '_rgb_matrix_check_finished_leds_led_idx_10000_197'
                                   1185 ;------------------------------------------------------------
                                   1186 ;	quantum/rgb_matrix/rgb_matrix.h:260: static inline bool rgb_matrix_check_finished_leds(uint8_t led_idx) {
                                   1187 ;	-----------------------------------------
                                   1188 ;	 function ak820_rgb_init
                                   1189 ;	-----------------------------------------
      0033FD                       1190 _ak820_rgb_init:
                                   1191 ;	keyboards/ajazz/ak820/ak820_board.c:325: }
      0033FD 22               [24] 1192 	ret
                                   1193 ;------------------------------------------------------------
                                   1194 ;Allocation info for local variables in function 'ak820_rgb_set_color'
                                   1195 ;------------------------------------------------------------
                                   1196 ;r             Allocated to stack - _bp -3 +1 
                                   1197 ;g             Allocated to stack - _bp -4 +1 
                                   1198 ;b             Allocated to stack - _bp -5 +1 
                                   1199 ;index         Allocated to registers r6 r7 
                                   1200 ;------------------------------------------------------------
                                   1201 ;	keyboards/ajazz/ak820/ak820_board.c:328: static void ak820_rgb_set_color(int index, uint8_t r, uint8_t g, uint8_t b) __reentrant {
                                   1202 ;	-----------------------------------------
                                   1203 ;	 function ak820_rgb_set_color
                                   1204 ;	-----------------------------------------
      0033FE                       1205 _ak820_rgb_set_color:
      0033FE C0 1F            [24] 1206 	push	_bp
      003400 85 81 1F         [24] 1207 	mov	_bp,sp
      003403 AE 82            [24] 1208 	mov	r6, dpl
                                   1209 ;	keyboards/ajazz/ak820/ak820_board.c:329: if (index < 0 || index >= RGB_MATRIX_LED_COUNT) {
      003405 E5 83            [12] 1210 	mov	a,dph
      003407 FF               [12] 1211 	mov	r7,a
      003408 20 E7 3B         [24] 1212 	jb	acc.7,00104$
      00340B C3               [12] 1213 	clr	c
      00340C EE               [12] 1214 	mov	a,r6
      00340D 94 52            [12] 1215 	subb	a,#0x52
      00340F EF               [12] 1216 	mov	a,r7
      003410 64 80            [12] 1217 	xrl	a,#0x80
      003412 94 80            [12] 1218 	subb	a,#0x80
                                   1219 ;	keyboards/ajazz/ak820/ak820_board.c:330: return;
      003414 50 30            [24] 1220 	jnc	00104$
                                   1221 ;	keyboards/ajazz/ak820/ak820_board.c:333: ak820_set_slot_rgb(ak820_rgb_slots[index], r, g, b);
      003416 EE               [12] 1222 	mov	a,r6
      003417 24 C7            [12] 1223 	add	a, #_ak820_rgb_slots
      003419 F5 82            [12] 1224 	mov	dpl,a
      00341B EF               [12] 1225 	mov	a,r7
      00341C 34 B5            [12] 1226 	addc	a, #(_ak820_rgb_slots >> 8)
      00341E F5 83            [12] 1227 	mov	dph,a
      003420 E4               [12] 1228 	clr	a
      003421 93               [24] 1229 	movc	a,@a+dptr
      003422 FF               [12] 1230 	mov	r7,a
      003423 E5 1F            [12] 1231 	mov	a,_bp
      003425 24 FD            [12] 1232 	add	a,#0xfd
      003427 F8               [12] 1233 	mov	r0,a
      003428 90 04 16         [24] 1234 	mov	dptr,#_ak820_set_slot_rgb_PARM_2
      00342B E6               [12] 1235 	mov	a,@r0
      00342C F0               [24] 1236 	movx	@dptr,a
      00342D E5 1F            [12] 1237 	mov	a,_bp
      00342F 24 FC            [12] 1238 	add	a,#0xfc
      003431 F8               [12] 1239 	mov	r0,a
      003432 90 04 17         [24] 1240 	mov	dptr,#_ak820_set_slot_rgb_PARM_3
      003435 E6               [12] 1241 	mov	a,@r0
      003436 F0               [24] 1242 	movx	@dptr,a
      003437 E5 1F            [12] 1243 	mov	a,_bp
      003439 24 FB            [12] 1244 	add	a,#0xfb
      00343B F8               [12] 1245 	mov	r0,a
      00343C 90 04 18         [24] 1246 	mov	dptr,#_ak820_set_slot_rgb_PARM_4
      00343F E6               [12] 1247 	mov	a,@r0
      003440 F0               [24] 1248 	movx	@dptr,a
      003441 8F 82            [24] 1249 	mov	dpl, r7
      003443 12 33 7F         [24] 1250 	lcall	_ak820_set_slot_rgb
      003446                       1251 00104$:
                                   1252 ;	keyboards/ajazz/ak820/ak820_board.c:337: }
      003446 D0 1F            [24] 1253 	pop	_bp
      003448 22               [24] 1254 	ret
                                   1255 ;------------------------------------------------------------
                                   1256 ;Allocation info for local variables in function 'ak820_rgb_set_color_all'
                                   1257 ;------------------------------------------------------------
                                   1258 ;g             Allocated to stack - _bp -3 +1 
                                   1259 ;b             Allocated to stack - _bp -4 +1 
                                   1260 ;r             Allocated to registers r7 
                                   1261 ;i             Allocated to registers r6 
                                   1262 ;------------------------------------------------------------
                                   1263 ;	keyboards/ajazz/ak820/ak820_board.c:339: static void ak820_rgb_set_color_all(uint8_t r, uint8_t g, uint8_t b) __reentrant {
                                   1264 ;	-----------------------------------------
                                   1265 ;	 function ak820_rgb_set_color_all
                                   1266 ;	-----------------------------------------
      003449                       1267 _ak820_rgb_set_color_all:
      003449 C0 1F            [24] 1268 	push	_bp
      00344B 85 81 1F         [24] 1269 	mov	_bp,sp
      00344E AF 82            [24] 1270 	mov	r7, dpl
                                   1271 ;	keyboards/ajazz/ak820/ak820_board.c:341: for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
      003450 7E 00            [12] 1272 	mov	r6,#0x00
      003452                       1273 00102$:
                                   1274 ;	keyboards/ajazz/ak820/ak820_board.c:342: ak820_rgb_set_color(i, r, g, b);
      003452 8E 04            [24] 1275 	mov	ar4,r6
      003454 7D 00            [12] 1276 	mov	r5,#0x00
      003456 C0 07            [24] 1277 	push	ar7
      003458 C0 06            [24] 1278 	push	ar6
      00345A E5 1F            [12] 1279 	mov	a,_bp
      00345C 24 FC            [12] 1280 	add	a,#0xfc
      00345E F8               [12] 1281 	mov	r0,a
      00345F E6               [12] 1282 	mov	a,@r0
      003460 C0 E0            [24] 1283 	push	acc
      003462 E5 1F            [12] 1284 	mov	a,_bp
      003464 24 FD            [12] 1285 	add	a,#0xfd
      003466 F8               [12] 1286 	mov	r0,a
      003467 E6               [12] 1287 	mov	a,@r0
      003468 C0 E0            [24] 1288 	push	acc
      00346A C0 07            [24] 1289 	push	ar7
      00346C 8C 82            [24] 1290 	mov	dpl, r4
      00346E 8D 83            [24] 1291 	mov	dph, r5
      003470 12 33 FE         [24] 1292 	lcall	_ak820_rgb_set_color
      003473 15 81            [12] 1293 	dec	sp
      003475 15 81            [12] 1294 	dec	sp
      003477 15 81            [12] 1295 	dec	sp
      003479 D0 06            [24] 1296 	pop	ar6
      00347B D0 07            [24] 1297 	pop	ar7
                                   1298 ;	keyboards/ajazz/ak820/ak820_board.c:341: for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
      00347D 0E               [12] 1299 	inc	r6
      00347E BE 52 00         [24] 1300 	cjne	r6,#0x52,00114$
      003481                       1301 00114$:
      003481 40 CF            [24] 1302 	jc	00102$
                                   1303 ;	keyboards/ajazz/ak820/ak820_board.c:344: }
      003483 D0 1F            [24] 1304 	pop	_bp
      003485 22               [24] 1305 	ret
                                   1306 ;------------------------------------------------------------
                                   1307 ;Allocation info for local variables in function 'ak820_rgb_flush'
                                   1308 ;------------------------------------------------------------
                                   1309 ;	keyboards/ajazz/ak820/ak820_board.c:346: static void ak820_rgb_flush(void) {
                                   1310 ;	-----------------------------------------
                                   1311 ;	 function ak820_rgb_flush
                                   1312 ;	-----------------------------------------
      003486                       1313 _ak820_rgb_flush:
                                   1314 ;	keyboards/ajazz/ak820/ak820_board.c:348: }
      003486 22               [24] 1315 	ret
                                   1316 	.area CSEG    (CODE)
                                   1317 	.area CONST   (CODE)
                                   1318 	.area CONST   (CODE)
      00B5B7                       1319 _ak820_matrix_mask:
      00B5B7 3F                    1320 	.db #0x3f	; 63
      00B5B8 2F                    1321 	.db #0x2f	; 47
      00B5B9 3F                    1322 	.db #0x3f	; 63
      00B5BA 1F                    1323 	.db #0x1f	; 31
      00B5BB 1F                    1324 	.db #0x1f	; 31
      00B5BC 3F                    1325 	.db #0x3f	; 63
      00B5BD 1F                    1326 	.db #0x1f	; 31
      00B5BE 1F                    1327 	.db #0x1f	; 31
      00B5BF 1F                    1328 	.db #0x1f	; 31
      00B5C0 3F                    1329 	.db #0x3f	; 63
      00B5C1 3F                    1330 	.db #0x3f	; 63
      00B5C2 3F                    1331 	.db #0x3f	; 63
      00B5C3 07                    1332 	.db #0x07	; 7
      00B5C4 3F                    1333 	.db #0x3f	; 63
      00B5C5 3C                    1334 	.db #0x3c	; 60
      00B5C6 2E                    1335 	.db #0x2e	; 46
                                   1336 	.area CSEG    (CODE)
                                   1337 	.area CONST   (CODE)
      00B5C7                       1338 _ak820_rgb_slots:
      00B5C7 00                    1339 	.db #0x00	; 0
      00B5C8 08                    1340 	.db #0x08	; 8
      00B5C9 10                    1341 	.db #0x10	; 16
      00B5CA 18                    1342 	.db #0x18	; 24
      00B5CB 20                    1343 	.db #0x20	; 32
      00B5CC 28                    1344 	.db #0x28	; 40
      00B5CD 30                    1345 	.db #0x30	; 48	'0'
      00B5CE 38                    1346 	.db #0x38	; 56	'8'
      00B5CF 40                    1347 	.db #0x40	; 64
      00B5D0 48                    1348 	.db #0x48	; 72	'H'
      00B5D1 50                    1349 	.db #0x50	; 80	'P'
      00B5D2 58                    1350 	.db #0x58	; 88	'X'
      00B5D3 60                    1351 	.db #0x60	; 96
      00B5D4 72                    1352 	.db #0x72	; 114	'r'
      00B5D5 01                    1353 	.db #0x01	; 1
      00B5D6 09                    1354 	.db #0x09	; 9
      00B5D7 11                    1355 	.db #0x11	; 17
      00B5D8 19                    1356 	.db #0x19	; 25
      00B5D9 21                    1357 	.db #0x21	; 33
      00B5DA 29                    1358 	.db #0x29	; 41
      00B5DB 31                    1359 	.db #0x31	; 49	'1'
      00B5DC 39                    1360 	.db #0x39	; 57	'9'
      00B5DD 41                    1361 	.db #0x41	; 65	'A'
      00B5DE 49                    1362 	.db #0x49	; 73	'I'
      00B5DF 51                    1363 	.db #0x51	; 81	'Q'
      00B5E0 59                    1364 	.db #0x59	; 89	'Y'
      00B5E1 61                    1365 	.db #0x61	; 97	'a'
      00B5E2 69                    1366 	.db #0x69	; 105	'i'
      00B5E3 79                    1367 	.db #0x79	; 121	'y'
      00B5E4 02                    1368 	.db #0x02	; 2
      00B5E5 0A                    1369 	.db #0x0a	; 10
      00B5E6 12                    1370 	.db #0x12	; 18
      00B5E7 1A                    1371 	.db #0x1a	; 26
      00B5E8 22                    1372 	.db #0x22	; 34
      00B5E9 2A                    1373 	.db #0x2a	; 42
      00B5EA 32                    1374 	.db #0x32	; 50	'2'
      00B5EB 3A                    1375 	.db #0x3a	; 58
      00B5EC 42                    1376 	.db #0x42	; 66	'B'
      00B5ED 4A                    1377 	.db #0x4a	; 74	'J'
      00B5EE 52                    1378 	.db #0x52	; 82	'R'
      00B5EF 5A                    1379 	.db #0x5a	; 90	'Z'
      00B5F0 62                    1380 	.db #0x62	; 98	'b'
      00B5F1 6A                    1381 	.db #0x6a	; 106	'j'
      00B5F2 7A                    1382 	.db #0x7a	; 122	'z'
      00B5F3 03                    1383 	.db #0x03	; 3
      00B5F4 0B                    1384 	.db #0x0b	; 11
      00B5F5 13                    1385 	.db #0x13	; 19
      00B5F6 1B                    1386 	.db #0x1b	; 27
      00B5F7 23                    1387 	.db #0x23	; 35
      00B5F8 2B                    1388 	.db #0x2b	; 43
      00B5F9 33                    1389 	.db #0x33	; 51	'3'
      00B5FA 3B                    1390 	.db #0x3b	; 59
      00B5FB 43                    1391 	.db #0x43	; 67	'C'
      00B5FC 4B                    1392 	.db #0x4b	; 75	'K'
      00B5FD 53                    1393 	.db #0x53	; 83	'S'
      00B5FE 5B                    1394 	.db #0x5b	; 91
      00B5FF 6B                    1395 	.db #0x6b	; 107	'k'
      00B600 73                    1396 	.db #0x73	; 115	's'
      00B601 04                    1397 	.db #0x04	; 4
      00B602 14                    1398 	.db #0x14	; 20
      00B603 1C                    1399 	.db #0x1c	; 28
      00B604 24                    1400 	.db #0x24	; 36
      00B605 2C                    1401 	.db #0x2c	; 44
      00B606 34                    1402 	.db #0x34	; 52	'4'
      00B607 3C                    1403 	.db #0x3c	; 60
      00B608 44                    1404 	.db #0x44	; 68	'D'
      00B609 4C                    1405 	.db #0x4c	; 76	'L'
      00B60A 54                    1406 	.db #0x54	; 84	'T'
      00B60B 5C                    1407 	.db #0x5c	; 92
      00B60C 6C                    1408 	.db #0x6c	; 108	'l'
      00B60D 74                    1409 	.db #0x74	; 116	't'
      00B60E 7B                    1410 	.db #0x7b	; 123
      00B60F 05                    1411 	.db #0x05	; 5
      00B610 0D                    1412 	.db #0x0d	; 13
      00B611 15                    1413 	.db #0x15	; 21
      00B612 2D                    1414 	.db #0x2d	; 45
      00B613 4D                    1415 	.db #0x4d	; 77	'M'
      00B614 55                    1416 	.db #0x55	; 85	'U'
      00B615 5D                    1417 	.db #0x5d	; 93
      00B616 6D                    1418 	.db #0x6d	; 109	'm'
      00B617 75                    1419 	.db #0x75	; 117	'u'
      00B618 7D                    1420 	.db #0x7d	; 125
                                   1421 	.area CSEG    (CODE)
                                   1422 	.area CONST   (CODE)
      00B619                       1423 _rgb_matrix_driver:
      00B619 FD 33                 1424 	.byte _ak820_rgb_init, (_ak820_rgb_init >> 8)
      00B61B FE 33                 1425 	.byte _ak820_rgb_set_color, (_ak820_rgb_set_color >> 8)
      00B61D 49 34                 1426 	.byte _ak820_rgb_set_color_all, (_ak820_rgb_set_color_all >> 8)
      00B61F 86 34                 1427 	.byte _ak820_rgb_flush, (_ak820_rgb_flush >> 8)
                                   1428 	.area CSEG    (CODE)
                                   1429 	.area XINIT   (CODE)
                                   1430 	.area CABS    (ABS,CODE)
