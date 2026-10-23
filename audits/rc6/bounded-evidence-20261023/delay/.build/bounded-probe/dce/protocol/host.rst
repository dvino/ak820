                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module host
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
                                    254 	.globl _host_set_driver
                                    255 	.globl _host_keyboard_leds
                                    256 	.globl _host_keyboard_send
                                    257 	.globl _host_system_send
                                    258 	.globl _host_consumer_send
                                    259 	.globl _host_last_system_usage
                                    260 	.globl _host_last_consumer_usage
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
                                    539 ;--------------------------------------------------------
                                    540 ; paged external ram data
                                    541 ;--------------------------------------------------------
                                    542 	.area PSEG    (PAG,XDATA)
                                    543 ;--------------------------------------------------------
                                    544 ; uninitialized external ram data
                                    545 ;--------------------------------------------------------
                                    546 	.area XSEG    (XDATA)
      000700                        547 _driver:
      000700                        548 	.ds 2
      000702                        549 _host_set_driver_d_10000_176:
      000702                        550 	.ds 3
      000705                        551 _host_keyboard_send_report_10000_185:
      000705                        552 	.ds 3
      000708                        553 _host_extra_send_PARM_2:
      000708                        554 	.ds 2
      00070A                        555 _host_extra_send_report_id_10000_198:
      00070A                        556 	.ds 1
      00070B                        557 _host_extra_send_report_10001_201:
      00070B                        558 	.ds 3
      00070E                        559 _host_system_send_usage_10000_202:
      00070E                        560 	.ds 2
      000710                        561 _host_consumer_send_usage_10000_205:
      000710                        562 	.ds 2
                                    563 ;--------------------------------------------------------
                                    564 ; absolute external ram data
                                    565 ;--------------------------------------------------------
                                    566 	.area XABS    (ABS,XDATA)
                                    567 ;--------------------------------------------------------
                                    568 ; initialized external ram data
                                    569 ;--------------------------------------------------------
                                    570 	.area XISEG   (XDATA)
      000BA7                        571 _last_system_usage:
      000BA7                        572 	.ds 2
      000BA9                        573 _last_consumer_usage:
      000BA9                        574 	.ds 2
                                    575 	.area HOME    (CODE)
                                    576 	.area GSINIT0 (CODE)
                                    577 	.area GSINIT1 (CODE)
                                    578 	.area GSINIT2 (CODE)
                                    579 	.area GSINIT3 (CODE)
                                    580 	.area GSINIT4 (CODE)
                                    581 	.area GSINIT5 (CODE)
                                    582 	.area GSINIT  (CODE)
                                    583 	.area GSFINAL (CODE)
                                    584 	.area CSEG    (CODE)
                                    585 ;--------------------------------------------------------
                                    586 ; global & static initialisations
                                    587 ;--------------------------------------------------------
                                    588 	.area HOME    (CODE)
                                    589 	.area GSINIT  (CODE)
                                    590 	.area GSFINAL (CODE)
                                    591 	.area GSINIT  (CODE)
                                    592 ;--------------------------------------------------------
                                    593 ; Home
                                    594 ;--------------------------------------------------------
                                    595 	.area HOME    (CODE)
                                    596 	.area HOME    (CODE)
                                    597 ;--------------------------------------------------------
                                    598 ; code
                                    599 ;--------------------------------------------------------
                                    600 	.area CSEG    (CODE)
                                    601 ;------------------------------------------------------------
                                    602 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    603 ;------------------------------------------------------------
                                    604 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_98'
                                    605 ;------------------------------------------------------------
                                    606 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    607 ;	-----------------------------------------
                           000007   608 	ar7 = 0x07
                           000006   609 	ar6 = 0x06
                           000005   610 	ar5 = 0x05
                           000004   611 	ar4 = 0x04
                           000003   612 	ar3 = 0x03
                           000002   613 	ar2 = 0x02
                           000001   614 	ar1 = 0x01
                           000000   615 	ar0 = 0x00
                                    616 ;	 function host_set_driver
                                    617 ;	-----------------------------------------
      006701                        618 _host_set_driver:
      006701 AF F0            [24]  619 	mov	r7,b
      006703 AE 83            [24]  620 	mov	r6,dph
      006705 E5 82            [12]  621 	mov	a,dpl
      006707 90 07 02         [24]  622 	mov	dptr,#_host_set_driver_d_10000_176
      00670A F0               [24]  623 	movx	@dptr,a
      00670B EE               [12]  624 	mov	a,r6
      00670C A3               [24]  625 	inc	dptr
      00670D F0               [24]  626 	movx	@dptr,a
      00670E EF               [12]  627 	mov	a,r7
      00670F A3               [24]  628 	inc	dptr
      006710 F0               [24]  629 	movx	@dptr,a
                                    630 ;	tmk_core/protocol/host.c:53: driver = (host_driver_t __xdata *)d;
      006711 90 07 02         [24]  631 	mov	dptr,#_host_set_driver_d_10000_176
      006714 E0               [24]  632 	movx	a,@dptr
      006715 FE               [12]  633 	mov	r6,a
      006716 A3               [24]  634 	inc	dptr
      006717 E0               [24]  635 	movx	a,@dptr
      006718 FF               [12]  636 	mov	r7,a
      006719 90 07 00         [24]  637 	mov	dptr,#_driver
      00671C EE               [12]  638 	mov	a,r6
      00671D F0               [24]  639 	movx	@dptr,a
      00671E EF               [12]  640 	mov	a,r7
      00671F A3               [24]  641 	inc	dptr
      006720 F0               [24]  642 	movx	@dptr,a
                                    643 ;	tmk_core/protocol/host.c:57: }
      006721 22               [24]  644 	ret
                                    645 ;------------------------------------------------------------
                                    646 ;Allocation info for local variables in function 'host_get_driver'
                                    647 ;------------------------------------------------------------
                                    648 ;	tmk_core/protocol/host.c:59: host_driver_t *host_get_driver(void) {
                                    649 ;	-----------------------------------------
                                    650 ;	 function host_keyboard_leds
                                    651 ;	-----------------------------------------
      006722                        652 _host_keyboard_leds:
                                    653 ;	tmk_core/protocol/host.c:74: if (!driver) return 0;
      006722 90 07 00         [24]  654 	mov	dptr,#_driver
      006725 E0               [24]  655 	movx	a,@dptr
      006726 FE               [12]  656 	mov	r6,a
      006727 A3               [24]  657 	inc	dptr
      006728 E0               [24]  658 	movx	a,@dptr
      006729 FF               [12]  659 	mov	r7,a
      00672A 4E               [12]  660 	orl	a,r6
      00672B 70 03            [24]  661 	jnz	00102$
      00672D F5 82            [12]  662 	mov	dpl,a
      00672F 22               [24]  663 	ret
      006730                        664 00102$:
                                    665 ;	tmk_core/protocol/host.c:75: return (*driver->keyboard_leds)();
      006730 8E 82            [24]  666 	mov	dpl,r6
      006732 8F 83            [24]  667 	mov	dph,r7
      006734 E0               [24]  668 	movx	a,@dptr
      006735 FE               [12]  669 	mov	r6,a
      006736 A3               [24]  670 	inc	dptr
      006737 E0               [24]  671 	movx	a,@dptr
      006738 FF               [12]  672 	mov	r7,a
      006739 C0 07            [24]  673 	push	ar7
      00673B 8E 82            [24]  674 	mov	dpl,r6
      00673D 8F 83            [24]  675 	mov	dph,r7
      00673F 12 30 75         [24]  676 	lcall	__sdcc_call_dptr
      006742 AE 82            [24]  677 	mov	r6, dpl
      006744 D0 07            [24]  678 	pop	ar7
      006746 8E 82            [24]  679 	mov	dpl, r6
                                    680 ;	tmk_core/protocol/host.c:76: }
      006748 22               [24]  681 	ret
                                    682 ;------------------------------------------------------------
                                    683 ;Allocation info for local variables in function 'host_keyboard_led_state'
                                    684 ;------------------------------------------------------------
                                    685 ;usb_led       Allocated with name '_host_keyboard_led_state_usb_led_10000_184'
                                    686 ;usb_led_p2    Allocated with name '_host_keyboard_led_state_usb_led_p2_10000_184'
                                    687 ;usb_led_p     Allocated with name '_host_keyboard_led_state_usb_led_p_10000_184'
                                    688 ;------------------------------------------------------------
                                    689 ;	tmk_core/protocol/host.c:78: led_t host_keyboard_led_state(void) {
                                    690 ;	-----------------------------------------
                                    691 ;	 function host_keyboard_send
                                    692 ;	-----------------------------------------
      006749                        693 _host_keyboard_send:
      006749 AF F0            [24]  694 	mov	r7,b
      00674B AE 83            [24]  695 	mov	r6,dph
      00674D E5 82            [12]  696 	mov	a,dpl
      00674F 90 07 05         [24]  697 	mov	dptr,#_host_keyboard_send_report_10000_185
      006752 F0               [24]  698 	movx	@dptr,a
      006753 EE               [12]  699 	mov	a,r6
      006754 A3               [24]  700 	inc	dptr
      006755 F0               [24]  701 	movx	@dptr,a
      006756 EF               [12]  702 	mov	a,r7
      006757 A3               [24]  703 	inc	dptr
      006758 F0               [24]  704 	movx	@dptr,a
                                    705 ;	tmk_core/protocol/host.c:95: if (!driver) return;
      006759 90 07 00         [24]  706 	mov	dptr,#_driver
      00675C E0               [24]  707 	movx	a,@dptr
      00675D F5 F0            [12]  708 	mov	b,a
      00675F A3               [24]  709 	inc	dptr
      006760 E0               [24]  710 	movx	a,@dptr
      006761 45 F0            [12]  711 	orl	a,b
      006763 70 01            [24]  712 	jnz	00102$
      006765 22               [24]  713 	ret
      006766                        714 00102$:
                                    715 ;	tmk_core/protocol/host.c:97: if (keyboard_protocol && keymap_config.nkro) {
      006766 90 0B 9E         [24]  716 	mov	dptr,#_keyboard_protocol
      006769 E0               [24]  717 	movx	a,@dptr
      00676A 60 38            [24]  718 	jz	00104$
      00676C 90 08 BD         [24]  719 	mov	dptr,#_keymap_config
      00676F E0               [24]  720 	movx	a,@dptr
      006770 30 E7 31         [24]  721 	jnb	acc.7,00104$
                                    722 ;	tmk_core/protocol/host.c:101: report->nkro.mods      = report->mods;
      006773 90 07 05         [24]  723 	mov	dptr,#_host_keyboard_send_report_10000_185
      006776 E0               [24]  724 	movx	a,@dptr
      006777 FD               [12]  725 	mov	r5,a
      006778 A3               [24]  726 	inc	dptr
      006779 E0               [24]  727 	movx	a,@dptr
      00677A FE               [12]  728 	mov	r6,a
      00677B A3               [24]  729 	inc	dptr
      00677C E0               [24]  730 	movx	a,@dptr
      00677D FF               [12]  731 	mov	r7,a
      00677E 74 01            [12]  732 	mov	a,#0x01
      006780 2D               [12]  733 	add	a, r5
      006781 FA               [12]  734 	mov	r2,a
      006782 E4               [12]  735 	clr	a
      006783 3E               [12]  736 	addc	a, r6
      006784 FB               [12]  737 	mov	r3,a
      006785 8F 04            [24]  738 	mov	ar4,r7
      006787 8D 82            [24]  739 	mov	dpl,r5
      006789 8E 83            [24]  740 	mov	dph,r6
      00678B 8F F0            [24]  741 	mov	b,r7
      00678D 12 B5 9A         [24]  742 	lcall	__gptrget
      006790 8A 82            [24]  743 	mov	dpl,r2
      006792 8B 83            [24]  744 	mov	dph,r3
      006794 8C F0            [24]  745 	mov	b,r4
      006796 12 B5 5F         [24]  746 	lcall	__gptrput
                                    747 ;	tmk_core/protocol/host.c:102: report->nkro.report_id = REPORT_ID_NKRO;
      006799 8D 82            [24]  748 	mov	dpl,r5
      00679B 8E 83            [24]  749 	mov	dph,r6
      00679D 8F F0            [24]  750 	mov	b,r7
      00679F 74 06            [12]  751 	mov	a,#0x06
      0067A1 12 B5 5F         [24]  752 	lcall	__gptrput
      0067A4                        753 00104$:
                                    754 ;	tmk_core/protocol/host.c:110: (*driver->send_keyboard)(report);
      0067A4 90 07 00         [24]  755 	mov	dptr,#_driver
      0067A7 E0               [24]  756 	movx	a,@dptr
      0067A8 FE               [12]  757 	mov	r6,a
      0067A9 A3               [24]  758 	inc	dptr
      0067AA E0               [24]  759 	movx	a,@dptr
      0067AB FF               [12]  760 	mov	r7,a
      0067AC 8E 82            [24]  761 	mov	dpl,r6
      0067AE 8F 83            [24]  762 	mov	dph,r7
      0067B0 A3               [24]  763 	inc	dptr
      0067B1 A3               [24]  764 	inc	dptr
      0067B2 E0               [24]  765 	movx	a,@dptr
      0067B3 FE               [12]  766 	mov	r6,a
      0067B4 A3               [24]  767 	inc	dptr
      0067B5 E0               [24]  768 	movx	a,@dptr
      0067B6 FF               [12]  769 	mov	r7,a
      0067B7 90 07 05         [24]  770 	mov	dptr,#_host_keyboard_send_report_10000_185
      0067BA E0               [24]  771 	movx	a,@dptr
      0067BB FB               [12]  772 	mov	r3,a
      0067BC A3               [24]  773 	inc	dptr
      0067BD E0               [24]  774 	movx	a,@dptr
      0067BE FC               [12]  775 	mov	r4,a
      0067BF A3               [24]  776 	inc	dptr
      0067C0 E0               [24]  777 	movx	a,@dptr
      0067C1 FD               [12]  778 	mov	r5,a
      0067C2 C0 07            [24]  779 	push	ar7
      0067C4 C0 06            [24]  780 	push	ar6
      0067C6 12 67 CB         [24]  781 	lcall	00160$
      0067C9 80 0B            [24]  782 	sjmp	00161$
      0067CB                        783 00160$:
      0067CB C0 06            [24]  784 	push	ar6
      0067CD C0 07            [24]  785 	push	ar7
      0067CF 8B 82            [24]  786 	mov	dpl, r3
      0067D1 8C 83            [24]  787 	mov	dph, r4
      0067D3 8D F0            [24]  788 	mov	b, r5
      0067D5 22               [24]  789 	ret
      0067D6                        790 00161$:
      0067D6 D0 06            [24]  791 	pop	ar6
      0067D8 D0 07            [24]  792 	pop	ar7
                                    793 ;	tmk_core/protocol/host.c:112: if (debug_keyboard) {
      0067DA 90 0B FE         [24]  794 	mov	dptr,#_debug_config
      0067DD E0               [24]  795 	movx	a,@dptr
      0067DE 30 E2 0A         [24]  796 	jnb	acc.2,00112$
                                    797 ;	tmk_core/protocol/host.c:114: for (uint8_t i = 0; i < KEYBOARD_REPORT_SIZE; i++) {
      0067E1 7F 00            [12]  798 	mov	r7,#0x00
      0067E3                        799 00110$:
      0067E3 BF 08 00         [24]  800 	cjne	r7,#0x08,00163$
      0067E6                        801 00163$:
      0067E6 50 03            [24]  802 	jnc	00112$
      0067E8 0F               [12]  803 	inc	r7
      0067E9 80 F8            [24]  804 	sjmp	00110$
      0067EB                        805 00112$:
                                    806 ;	tmk_core/protocol/host.c:119: }
      0067EB 22               [24]  807 	ret
                                    808 ;------------------------------------------------------------
                                    809 ;Allocation info for local variables in function 'host_mouse_send'
                                    810 ;------------------------------------------------------------
                                    811 ;report        Allocated with name '_host_mouse_send_report_10000_195'
                                    812 ;------------------------------------------------------------
                                    813 ;	tmk_core/protocol/host.c:121: void host_mouse_send(report_mouse_t *report) {
                                    814 ;	-----------------------------------------
                                    815 ;	 function host_extra_send
                                    816 ;	-----------------------------------------
      0067EC                        817 _host_extra_send:
      0067EC E5 82            [12]  818 	mov	a,dpl
      0067EE 90 07 0A         [24]  819 	mov	dptr,#_host_extra_send_report_id_10000_198
      0067F1 F0               [24]  820 	movx	@dptr,a
                                    821 ;	tmk_core/protocol/host.c:142: if (!driver) return;
      0067F2 90 07 00         [24]  822 	mov	dptr,#_driver
      0067F5 E0               [24]  823 	movx	a,@dptr
      0067F6 F5 F0            [12]  824 	mov	b,a
      0067F8 A3               [24]  825 	inc	dptr
      0067F9 E0               [24]  826 	movx	a,@dptr
      0067FA 45 F0            [12]  827 	orl	a,b
      0067FC 70 01            [24]  828 	jnz	00102$
      0067FE 22               [24]  829 	ret
      0067FF                        830 00102$:
                                    831 ;	tmk_core/protocol/host.c:143: report_extra_t report = {
      0067FF 90 07 0A         [24]  832 	mov	dptr,#_host_extra_send_report_id_10000_198
      006802 E0               [24]  833 	movx	a,@dptr
      006803 90 07 0B         [24]  834 	mov	dptr,#_host_extra_send_report_10001_201
      006806 F0               [24]  835 	movx	@dptr,a
      006807 90 07 08         [24]  836 	mov	dptr,#_host_extra_send_PARM_2
      00680A E0               [24]  837 	movx	a,@dptr
      00680B FE               [12]  838 	mov	r6,a
      00680C A3               [24]  839 	inc	dptr
      00680D E0               [24]  840 	movx	a,@dptr
      00680E FF               [12]  841 	mov	r7,a
      00680F 90 07 0C         [24]  842 	mov	dptr,#(_host_extra_send_report_10001_201 + 0x0001)
      006812 EE               [12]  843 	mov	a,r6
      006813 F0               [24]  844 	movx	@dptr,a
      006814 EF               [12]  845 	mov	a,r7
      006815 A3               [24]  846 	inc	dptr
      006816 F0               [24]  847 	movx	@dptr,a
                                    848 ;	tmk_core/protocol/host.c:147: (*driver->send_extra)(&report);
      006817 90 07 00         [24]  849 	mov	dptr,#_driver
      00681A E0               [24]  850 	movx	a,@dptr
      00681B FE               [12]  851 	mov	r6,a
      00681C A3               [24]  852 	inc	dptr
      00681D E0               [24]  853 	movx	a,@dptr
      00681E FF               [12]  854 	mov	r7,a
      00681F 74 06            [12]  855 	mov	a,#0x06
      006821 2E               [12]  856 	add	a, r6
      006822 F5 82            [12]  857 	mov	dpl,a
      006824 E4               [12]  858 	clr	a
      006825 3F               [12]  859 	addc	a, r7
      006826 F5 83            [12]  860 	mov	dph,a
      006828 E0               [24]  861 	movx	a,@dptr
      006829 FE               [12]  862 	mov	r6,a
      00682A A3               [24]  863 	inc	dptr
      00682B E0               [24]  864 	movx	a,@dptr
      00682C FF               [12]  865 	mov	r7,a
      00682D C0 07            [24]  866 	push	ar7
      00682F C0 06            [24]  867 	push	ar6
      006831 12 68 36         [24]  868 	lcall	00113$
      006834 80 0B            [24]  869 	sjmp	00114$
      006836                        870 00113$:
      006836 C0 06            [24]  871 	push	ar6
      006838 C0 07            [24]  872 	push	ar7
      00683A 90 07 0B         [24]  873 	mov	dptr,#_host_extra_send_report_10001_201
      00683D 75 F0 00         [24]  874 	mov	b, #0x00
      006840 22               [24]  875 	ret
      006841                        876 00114$:
      006841 D0 06            [24]  877 	pop	ar6
      006843 D0 07            [24]  878 	pop	ar7
                                    879 ;	tmk_core/protocol/host.c:148: }
      006845 22               [24]  880 	ret
                                    881 ;------------------------------------------------------------
                                    882 ;Allocation info for local variables in function 'host_system_send'
                                    883 ;------------------------------------------------------------
                                    884 ;usage         Allocated with name '_host_system_send_usage_10000_202'
                                    885 ;------------------------------------------------------------
                                    886 ;	tmk_core/protocol/host.c:150: void host_system_send(uint16_t usage) {
                                    887 ;	-----------------------------------------
                                    888 ;	 function host_system_send
                                    889 ;	-----------------------------------------
      006846                        890 _host_system_send:
      006846 AF 83            [24]  891 	mov	r7,dph
      006848 E5 82            [12]  892 	mov	a,dpl
      00684A 90 07 0E         [24]  893 	mov	dptr,#_host_system_send_usage_10000_202
      00684D F0               [24]  894 	movx	@dptr,a
      00684E EF               [12]  895 	mov	a,r7
      00684F A3               [24]  896 	inc	dptr
      006850 F0               [24]  897 	movx	@dptr,a
                                    898 ;	tmk_core/protocol/host.c:151: if (usage == last_system_usage) return;
      006851 90 07 0E         [24]  899 	mov	dptr,#_host_system_send_usage_10000_202
      006854 E0               [24]  900 	movx	a,@dptr
      006855 FE               [12]  901 	mov	r6,a
      006856 A3               [24]  902 	inc	dptr
      006857 E0               [24]  903 	movx	a,@dptr
      006858 FF               [12]  904 	mov	r7,a
      006859 90 0B A7         [24]  905 	mov	dptr,#_last_system_usage
      00685C E0               [24]  906 	movx	a,@dptr
      00685D FC               [12]  907 	mov	r4,a
      00685E A3               [24]  908 	inc	dptr
      00685F E0               [24]  909 	movx	a,@dptr
      006860 FD               [12]  910 	mov	r5,a
      006861 EE               [12]  911 	mov	a,r6
      006862 B5 04 05         [24]  912 	cjne	a,ar4,00102$
      006865 EF               [12]  913 	mov	a,r7
      006866 B5 05 01         [24]  914 	cjne	a,ar5,00102$
      006869 22               [24]  915 	ret
      00686A                        916 00102$:
                                    917 ;	tmk_core/protocol/host.c:152: last_system_usage = usage;
      00686A 90 0B A7         [24]  918 	mov	dptr,#_last_system_usage
      00686D EE               [12]  919 	mov	a,r6
      00686E F0               [24]  920 	movx	@dptr,a
      00686F EF               [12]  921 	mov	a,r7
      006870 A3               [24]  922 	inc	dptr
      006871 F0               [24]  923 	movx	@dptr,a
                                    924 ;	tmk_core/protocol/host.c:154: host_extra_send(REPORT_ID_SYSTEM, usage);
      006872 90 07 08         [24]  925 	mov	dptr,#_host_extra_send_PARM_2
      006875 EE               [12]  926 	mov	a,r6
      006876 F0               [24]  927 	movx	@dptr,a
      006877 EF               [12]  928 	mov	a,r7
      006878 A3               [24]  929 	inc	dptr
      006879 F0               [24]  930 	movx	@dptr,a
      00687A 75 82 03         [24]  931 	mov	dpl, #0x03
                                    932 ;	tmk_core/protocol/host.c:155: }
      00687D 02 67 EC         [24]  933 	ljmp	_host_extra_send
                                    934 ;------------------------------------------------------------
                                    935 ;Allocation info for local variables in function 'host_consumer_send'
                                    936 ;------------------------------------------------------------
                                    937 ;usage         Allocated with name '_host_consumer_send_usage_10000_205'
                                    938 ;------------------------------------------------------------
                                    939 ;	tmk_core/protocol/host.c:157: void host_consumer_send(uint16_t usage) {
                                    940 ;	-----------------------------------------
                                    941 ;	 function host_consumer_send
                                    942 ;	-----------------------------------------
      006880                        943 _host_consumer_send:
      006880 AF 83            [24]  944 	mov	r7,dph
      006882 E5 82            [12]  945 	mov	a,dpl
      006884 90 07 10         [24]  946 	mov	dptr,#_host_consumer_send_usage_10000_205
      006887 F0               [24]  947 	movx	@dptr,a
      006888 EF               [12]  948 	mov	a,r7
      006889 A3               [24]  949 	inc	dptr
      00688A F0               [24]  950 	movx	@dptr,a
                                    951 ;	tmk_core/protocol/host.c:158: if (usage == last_consumer_usage) return;
      00688B 90 07 10         [24]  952 	mov	dptr,#_host_consumer_send_usage_10000_205
      00688E E0               [24]  953 	movx	a,@dptr
      00688F FE               [12]  954 	mov	r6,a
      006890 A3               [24]  955 	inc	dptr
      006891 E0               [24]  956 	movx	a,@dptr
      006892 FF               [12]  957 	mov	r7,a
      006893 90 0B A9         [24]  958 	mov	dptr,#_last_consumer_usage
      006896 E0               [24]  959 	movx	a,@dptr
      006897 FC               [12]  960 	mov	r4,a
      006898 A3               [24]  961 	inc	dptr
      006899 E0               [24]  962 	movx	a,@dptr
      00689A FD               [12]  963 	mov	r5,a
      00689B EE               [12]  964 	mov	a,r6
      00689C B5 04 05         [24]  965 	cjne	a,ar4,00102$
      00689F EF               [12]  966 	mov	a,r7
      0068A0 B5 05 01         [24]  967 	cjne	a,ar5,00102$
      0068A3 22               [24]  968 	ret
      0068A4                        969 00102$:
                                    970 ;	tmk_core/protocol/host.c:159: last_consumer_usage = usage;
      0068A4 90 0B A9         [24]  971 	mov	dptr,#_last_consumer_usage
      0068A7 EE               [12]  972 	mov	a,r6
      0068A8 F0               [24]  973 	movx	@dptr,a
      0068A9 EF               [12]  974 	mov	a,r7
      0068AA A3               [24]  975 	inc	dptr
      0068AB F0               [24]  976 	movx	@dptr,a
                                    977 ;	tmk_core/protocol/host.c:168: host_extra_send(REPORT_ID_CONSUMER, usage);
      0068AC 90 07 08         [24]  978 	mov	dptr,#_host_extra_send_PARM_2
      0068AF EE               [12]  979 	mov	a,r6
      0068B0 F0               [24]  980 	movx	@dptr,a
      0068B1 EF               [12]  981 	mov	a,r7
      0068B2 A3               [24]  982 	inc	dptr
      0068B3 F0               [24]  983 	movx	@dptr,a
      0068B4 75 82 04         [24]  984 	mov	dpl, #0x04
                                    985 ;	tmk_core/protocol/host.c:169: }
      0068B7 02 67 EC         [24]  986 	ljmp	_host_extra_send
                                    987 ;------------------------------------------------------------
                                    988 ;Allocation info for local variables in function 'host_last_system_usage'
                                    989 ;------------------------------------------------------------
                                    990 ;	tmk_core/protocol/host.c:264: uint16_t host_last_system_usage(void) {
                                    991 ;	-----------------------------------------
                                    992 ;	 function host_last_system_usage
                                    993 ;	-----------------------------------------
      0068BA                        994 _host_last_system_usage:
                                    995 ;	tmk_core/protocol/host.c:265: return last_system_usage;
      0068BA 90 0B A7         [24]  996 	mov	dptr,#_last_system_usage
      0068BD E0               [24]  997 	movx	a,@dptr
      0068BE FE               [12]  998 	mov	r6,a
      0068BF A3               [24]  999 	inc	dptr
      0068C0 E0               [24] 1000 	movx	a,@dptr
                                   1001 ;	tmk_core/protocol/host.c:266: }
      0068C1 8E 82            [24] 1002 	mov	dpl,r6
      0068C3 F5 83            [12] 1003 	mov	dph,a
      0068C5 22               [24] 1004 	ret
                                   1005 ;------------------------------------------------------------
                                   1006 ;Allocation info for local variables in function 'host_last_consumer_usage'
                                   1007 ;------------------------------------------------------------
                                   1008 ;	tmk_core/protocol/host.c:268: uint16_t host_last_consumer_usage(void) {
                                   1009 ;	-----------------------------------------
                                   1010 ;	 function host_last_consumer_usage
                                   1011 ;	-----------------------------------------
      0068C6                       1012 _host_last_consumer_usage:
                                   1013 ;	tmk_core/protocol/host.c:269: return last_consumer_usage;
      0068C6 90 0B A9         [24] 1014 	mov	dptr,#_last_consumer_usage
      0068C9 E0               [24] 1015 	movx	a,@dptr
      0068CA FE               [12] 1016 	mov	r6,a
      0068CB A3               [24] 1017 	inc	dptr
      0068CC E0               [24] 1018 	movx	a,@dptr
                                   1019 ;	tmk_core/protocol/host.c:270: }
      0068CD 8E 82            [24] 1020 	mov	dpl,r6
      0068CF F5 83            [12] 1021 	mov	dph,a
      0068D1 22               [24] 1022 	ret
                                   1023 	.area CSEG    (CODE)
                                   1024 	.area CONST   (CODE)
                                   1025 	.area XINIT   (CODE)
      00BD87                       1026 __xinit__last_system_usage:
      00BD87 00 00                 1027 	.byte #0x00, #0x00	; 0
      00BD89                       1028 __xinit__last_consumer_usage:
      00BD89 00 00                 1029 	.byte #0x00, #0x00	; 0
                                   1030 	.area CABS    (ABS,CODE)
