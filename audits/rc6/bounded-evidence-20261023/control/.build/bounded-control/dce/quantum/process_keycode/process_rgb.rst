                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module process_rgb
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _rgb_matrix_step
                                     12 	.globl _rgb_matrix_get_mode
                                     13 	.globl _rgb_matrix_mode
                                     14 	.globl _rgb_matrix_toggle
                                     15 	.globl _get_mods
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
                                    259 	.globl _process_rgb_PARM_2
                                    260 	.globl _process_rgb
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
      0009C5                        547 _process_rgb_PARM_2:
      0009C5                        548 	.ds 3
      0009C8                        549 _process_rgb_keycode_10000_265:
      0009C8                        550 	.ds 2
      0009CA                        551 _process_rgb_action_50000_270:
      0009CA                        552 	.ds 1
                                    553 ;--------------------------------------------------------
                                    554 ; absolute external ram data
                                    555 ;--------------------------------------------------------
                                    556 	.area XABS    (ABS,XDATA)
                                    557 ;--------------------------------------------------------
                                    558 ; initialized external ram data
                                    559 ;--------------------------------------------------------
                                    560 	.area XISEG   (XDATA)
                                    561 	.area HOME    (CODE)
                                    562 	.area GSINIT0 (CODE)
                                    563 	.area GSINIT1 (CODE)
                                    564 	.area GSINIT2 (CODE)
                                    565 	.area GSINIT3 (CODE)
                                    566 	.area GSINIT4 (CODE)
                                    567 	.area GSINIT5 (CODE)
                                    568 	.area GSINIT  (CODE)
                                    569 	.area GSFINAL (CODE)
                                    570 	.area CSEG    (CODE)
                                    571 ;--------------------------------------------------------
                                    572 ; global & static initialisations
                                    573 ;--------------------------------------------------------
                                    574 	.area HOME    (CODE)
                                    575 	.area GSINIT  (CODE)
                                    576 	.area GSFINAL (CODE)
                                    577 	.area GSINIT  (CODE)
                                    578 ;--------------------------------------------------------
                                    579 ; Home
                                    580 ;--------------------------------------------------------
                                    581 	.area HOME    (CODE)
                                    582 	.area HOME    (CODE)
                                    583 ;--------------------------------------------------------
                                    584 ; code
                                    585 ;--------------------------------------------------------
                                    586 	.area CSEG    (CODE)
                                    587 ;------------------------------------------------------------
                                    588 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    589 ;------------------------------------------------------------
                                    590 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_122'
                                    591 ;------------------------------------------------------------
                                    592 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    593 ;	-----------------------------------------
                           000007   594 	ar7 = 0x07
                           000006   595 	ar6 = 0x06
                           000005   596 	ar5 = 0x05
                           000004   597 	ar4 = 0x04
                           000003   598 	ar3 = 0x03
                           000002   599 	ar2 = 0x02
                           000001   600 	ar1 = 0x01
                           000000   601 	ar0 = 0x00
                                    602 ;	 function process_rgb
                                    603 ;	-----------------------------------------
      0095D5                        604 _process_rgb:
      0095D5 AF 83            [24]  605 	mov	r7,dph
      0095D7 E5 82            [12]  606 	mov	a,dpl
      0095D9 90 09 C8         [24]  607 	mov	dptr,#_process_rgb_keycode_10000_265
      0095DC F0               [24]  608 	movx	@dptr,a
      0095DD EF               [12]  609 	mov	a,r7
      0095DE A3               [24]  610 	inc	dptr
      0095DF F0               [24]  611 	movx	@dptr,a
                                    612 ;	quantum/process_keycode/process_rgb.c:88: if (!record->event.pressed) {
      0095E0 90 09 C5         [24]  613 	mov	dptr,#_process_rgb_PARM_2
      0095E3 12 73 B8         [24]  614 	lcall	_ak820_outline_0002
      0095E6 12 96 F1         [24]  615 	lcall	_ak820_outline_0018
      0095E9 12 B5 97         [24]  616 	lcall	__gptrget
      0095EC 60 03            [24]  617 	jz	00164$
      0095EE 02 96 ED         [24]  618 	ljmp	00119$
      0095F1                        619 00164$:
                                    620 ;	quantum/process_keycode/process_rgb.c:93: uint8_t shifted = get_mods() & MOD_MASK_SHIFT;
      0095F1 12 78 86         [24]  621 	lcall	_get_mods
      0095F4 E5 82            [12]  622 	mov	a, dpl
      0095F6 54 22            [12]  623 	anl	a,#0x22
      0095F8 FF               [12]  624 	mov	r7,a
                                    625 ;	quantum/process_keycode/process_rgb.c:96: if (keycode >= RGB_MODE_FORWARD && keycode <= RGB_SPD) {
      0095F9 90 09 C8         [24]  626 	mov	dptr,#_process_rgb_keycode_10000_265
      0095FC E0               [24]  627 	movx	a,@dptr
      0095FD FD               [12]  628 	mov	r5,a
      0095FE A3               [24]  629 	inc	dptr
      0095FF E0               [24]  630 	movx	a,@dptr
      009600 FE               [12]  631 	mov	r6,a
      009601 8D 03            [24]  632 	mov	ar3,r5
      009603 8E 04            [24]  633 	mov	ar4,r6
      009605 C3               [12]  634 	clr	c
      009606 EB               [12]  635 	mov	a,r3
      009607 94 21            [12]  636 	subb	a,#0x21
      009609 EC               [12]  637 	mov	a,r4
      00960A 94 78            [12]  638 	subb	a,#0x78
      00960C 40 46            [24]  639 	jc	00104$
      00960E 74 2A            [12]  640 	mov	a,#0x2a
      009610 9B               [12]  641 	subb	a,r3
      009611 74 78            [12]  642 	mov	a,#0x78
      009613 9C               [12]  643 	subb	a,r4
      009614 40 3E            [24]  644 	jc	00104$
                                    645 ;	free result
                                    646 ;	quantum/process_keycode/process_rgb.c:97: uint8_t action = (uint8_t)(keycode - RGB_MODE_FORWARD);
      009616 ED               [12]  647 	mov	a,r5
      009617 24 DF            [12]  648 	add	a,#0xdf
      009619 FD               [12]  649 	mov	r5,a
      00961A 90 09 CA         [24]  650 	mov	dptr,#_process_rgb_action_50000_270
      00961D F0               [24]  651 	movx	@dptr,a
                                    652 ;	quantum/process_keycode/process_rgb.c:98: if (shifted) action ^= 1;
      00961E EF               [12]  653 	mov	a,r7
      00961F 60 07            [24]  654 	jz	00102$
      009621 90 09 CA         [24]  655 	mov	dptr,#_process_rgb_action_50000_270
      009624 74 01            [12]  656 	mov	a,#0x01
      009626 6D               [12]  657 	xrl	a,r5
      009627 F0               [24]  658 	movx	@dptr,a
      009628                        659 00102$:
                                    660 ;	quantum/process_keycode/process_rgb.c:99: ak820_rgb_actions[action]();
      009628 90 09 CA         [24]  661 	mov	dptr,#_process_rgb_action_50000_270
      00962B E0               [24]  662 	movx	a,@dptr
      00962C 75 F0 02         [24]  663 	mov	b,#0x02
      00962F A4               [48]  664 	mul	ab
      009630 24 41            [12]  665 	add	a, #_ak820_rgb_actions
      009632 F5 82            [12]  666 	mov	dpl,a
      009634 74 B9            [12]  667 	mov	a,#(_ak820_rgb_actions >> 8)
      009636 35 F0            [12]  668 	addc	a, b
      009638 F5 83            [12]  669 	mov	dph,a
      00963A E4               [12]  670 	clr	a
      00963B 93               [24]  671 	movc	a,@a+dptr
      00963C FE               [12]  672 	mov	r6,a
      00963D A3               [24]  673 	inc	dptr
      00963E E4               [12]  674 	clr	a
      00963F 93               [24]  675 	movc	a,@a+dptr
      009640 FF               [12]  676 	mov	r7,a
      009641 C0 07            [24]  677 	push	ar7
      009643 C0 06            [24]  678 	push	ar6
      009645 8E 82            [24]  679 	mov	dpl,r6
      009647 8F 83            [24]  680 	mov	dph,r7
      009649 12 30 75         [24]  681 	lcall	__sdcc_call_dptr
      00964C D0 06            [24]  682 	pop	ar6
      00964E D0 07            [24]  683 	pop	ar7
                                    684 ;	quantum/process_keycode/process_rgb.c:100: return false;
      009650 75 82 00         [24]  685 	mov	dpl, #0x00
      009653 22               [24]  686 	ret
      009654                        687 00104$:
                                    688 ;	quantum/process_keycode/process_rgb.c:103: switch (keycode) {
      009654 90 09 C8         [24]  689 	mov	dptr,#_process_rgb_keycode_10000_265
      009657 E0               [24]  690 	movx	a,@dptr
      009658 FE               [12]  691 	mov	r6,a
      009659 A3               [24]  692 	inc	dptr
      00965A E0               [24]  693 	movx	a,@dptr
      00965B FF               [12]  694 	mov	r7,a
      00965C C3               [12]  695 	clr	c
      00965D EE               [12]  696 	mov	a,r6
      00965E 94 20            [12]  697 	subb	a,#0x20
      009660 EF               [12]  698 	mov	a,r7
      009661 94 78            [12]  699 	subb	a,#0x78
      009663 50 03            [24]  700 	jnc	00168$
      009665 02 96 ED         [24]  701 	ljmp	00119$
      009668                        702 00168$:
      009668 C3               [12]  703 	clr	c
      009669 74 34            [12]  704 	mov	a,#0x34
      00966B 9E               [12]  705 	subb	a,r6
      00966C 74 78            [12]  706 	mov	a,#0x78
      00966E 9F               [12]  707 	subb	a,r7
      00966F 40 7C            [24]  708 	jc	00119$
                                    709 ;	free result
      009671 EE               [12]  710 	mov	a,r6
      009672 24 E0            [12]  711 	add	a,#0xe0
      009674 FE               [12]  712 	mov	r6,a
      009675 24 0A            [12]  713 	add	a,#(00170$-3-.)
      009677 83               [24]  714 	movc	a,@a+pc
      009678 F5 82            [12]  715 	mov	dpl,a
      00967A EE               [12]  716 	mov	a,r6
      00967B 24 19            [12]  717 	add	a,#(00171$-3-.)
      00967D 83               [24]  718 	movc	a,@a+pc
      00967E F5 83            [12]  719 	mov	dph,a
      009680 E4               [12]  720 	clr	a
      009681 73               [24]  721 	jmp	@a+dptr
      009682                        722 00170$:
      009682 AC                     723 	.db	00106$
      009683 ED                     724 	.db	00119$
      009684 ED                     725 	.db	00119$
      009685 ED                     726 	.db	00119$
      009686 ED                     727 	.db	00119$
      009687 ED                     728 	.db	00119$
      009688 ED                     729 	.db	00119$
      009689 ED                     730 	.db	00119$
      00968A ED                     731 	.db	00119$
      00968B ED                     732 	.db	00119$
      00968C ED                     733 	.db	00119$
      00968D B3                     734 	.db	00107$
      00968E BD                     735 	.db	00108$
      00968F C7                     736 	.db	00109$
      009690 D1                     737 	.db	00110$
      009691 D5                     738 	.db	00111$
      009692 D9                     739 	.db	00112$
      009693 DD                     740 	.db	00113$
      009694 E1                     741 	.db	00114$
      009695 E5                     742 	.db	00115$
      009696 E9                     743 	.db	00116$
      009697                        744 00171$:
      009697 96                     745 	.db	00106$>>8
      009698 96                     746 	.db	00119$>>8
      009699 96                     747 	.db	00119$>>8
      00969A 96                     748 	.db	00119$>>8
      00969B 96                     749 	.db	00119$>>8
      00969C 96                     750 	.db	00119$>>8
      00969D 96                     751 	.db	00119$>>8
      00969E 96                     752 	.db	00119$>>8
      00969F 96                     753 	.db	00119$>>8
      0096A0 96                     754 	.db	00119$>>8
      0096A1 96                     755 	.db	00119$>>8
      0096A2 96                     756 	.db	00107$>>8
      0096A3 96                     757 	.db	00108$>>8
      0096A4 96                     758 	.db	00109$>>8
      0096A5 96                     759 	.db	00110$>>8
      0096A6 96                     760 	.db	00111$>>8
      0096A7 96                     761 	.db	00112$>>8
      0096A8 96                     762 	.db	00113$>>8
      0096A9 96                     763 	.db	00114$>>8
      0096AA 96                     764 	.db	00115$>>8
      0096AB 96                     765 	.db	00116$>>8
                                    766 ;	quantum/process_keycode/process_rgb.c:104: case RGB_TOG:
      0096AC                        767 00106$:
                                    768 ;	quantum/process_keycode/process_rgb.c:109: rgb_matrix_toggle();
      0096AC 12 50 B2         [24]  769 	lcall	_rgb_matrix_toggle
                                    770 ;	quantum/process_keycode/process_rgb.c:111: return false;
      0096AF 75 82 00         [24]  771 	mov	dpl, #0x00
                                    772 ;	quantum/process_keycode/process_rgb.c:194: case RGB_MODE_PLAIN:
      0096B2 22               [24]  773 	ret
      0096B3                        774 00107$:
                                    775 ;	quantum/process_keycode/process_rgb.c:199: rgb_matrix_mode(RGB_MATRIX_SOLID_COLOR);
      0096B3 75 82 01         [24]  776 	mov	dpl, #0x01
      0096B6 12 50 F4         [24]  777 	lcall	_rgb_matrix_mode
                                    778 ;	quantum/process_keycode/process_rgb.c:201: return false;
      0096B9 75 82 00         [24]  779 	mov	dpl, #0x00
                                    780 ;	quantum/process_keycode/process_rgb.c:202: case RGB_MODE_BREATHE:
      0096BC 22               [24]  781 	ret
      0096BD                        782 00108$:
                                    783 ;	quantum/process_keycode/process_rgb.c:207: rgb_matrix_mode(RGB_MATRIX_BREATHING);
      0096BD 75 82 02         [24]  784 	mov	dpl, #0x02
      0096C0 12 50 F4         [24]  785 	lcall	_rgb_matrix_mode
                                    786 ;	quantum/process_keycode/process_rgb.c:209: return false;
      0096C3 75 82 00         [24]  787 	mov	dpl, #0x00
                                    788 ;	quantum/process_keycode/process_rgb.c:210: case RGB_MODE_RAINBOW:
      0096C6 22               [24]  789 	ret
      0096C7                        790 00109$:
                                    791 ;	quantum/process_keycode/process_rgb.c:215: rgb_matrix_mode(RGB_MATRIX_CYCLE_LEFT_RIGHT);
      0096C7 75 82 04         [24]  792 	mov	dpl, #0x04
      0096CA 12 50 F4         [24]  793 	lcall	_rgb_matrix_mode
                                    794 ;	quantum/process_keycode/process_rgb.c:217: return false;
      0096CD 75 82 00         [24]  795 	mov	dpl, #0x00
                                    796 ;	quantum/process_keycode/process_rgb.c:218: case RGB_MODE_SWIRL:
      0096D0 22               [24]  797 	ret
      0096D1                        798 00110$:
                                    799 ;	quantum/process_keycode/process_rgb.c:225: return false;
      0096D1 75 82 00         [24]  800 	mov	dpl, #0x00
                                    801 ;	quantum/process_keycode/process_rgb.c:226: case RGB_MODE_SNAKE:
      0096D4 22               [24]  802 	ret
      0096D5                        803 00111$:
                                    804 ;	quantum/process_keycode/process_rgb.c:230: return false;
      0096D5 75 82 00         [24]  805 	mov	dpl, #0x00
                                    806 ;	quantum/process_keycode/process_rgb.c:231: case RGB_MODE_KNIGHT:
      0096D8 22               [24]  807 	ret
      0096D9                        808 00112$:
                                    809 ;	quantum/process_keycode/process_rgb.c:235: return false;
      0096D9 75 82 00         [24]  810 	mov	dpl, #0x00
                                    811 ;	quantum/process_keycode/process_rgb.c:236: case RGB_MODE_XMAS:
      0096DC 22               [24]  812 	ret
      0096DD                        813 00113$:
                                    814 ;	quantum/process_keycode/process_rgb.c:240: return false;
      0096DD 75 82 00         [24]  815 	mov	dpl, #0x00
                                    816 ;	quantum/process_keycode/process_rgb.c:241: case RGB_MODE_GRADIENT:
      0096E0 22               [24]  817 	ret
      0096E1                        818 00114$:
                                    819 ;	quantum/process_keycode/process_rgb.c:245: return false;
      0096E1 75 82 00         [24]  820 	mov	dpl, #0x00
                                    821 ;	quantum/process_keycode/process_rgb.c:246: case RGB_MODE_RGBTEST:
      0096E4 22               [24]  822 	ret
      0096E5                        823 00115$:
                                    824 ;	quantum/process_keycode/process_rgb.c:250: return false;
      0096E5 75 82 00         [24]  825 	mov	dpl, #0x00
                                    826 ;	quantum/process_keycode/process_rgb.c:251: case RGB_MODE_TWINKLE:
      0096E8 22               [24]  827 	ret
      0096E9                        828 00116$:
                                    829 ;	quantum/process_keycode/process_rgb.c:255: return false;
      0096E9 75 82 00         [24]  830 	mov	dpl, #0x00
                                    831 ;	quantum/process_keycode/process_rgb.c:256: }
      0096EC 22               [24]  832 	ret
      0096ED                        833 00119$:
                                    834 ;	quantum/process_keycode/process_rgb.c:259: return true;
      0096ED 75 82 01         [24]  835 	mov	dpl, #0x01
                                    836 ;	quantum/process_keycode/process_rgb.c:260: }
      0096F0 22               [24]  837 	ret
                                    838 	.area CSEG    (CODE)
                                    839 	.area CONST   (CODE)
                                    840 	.area CONST   (CODE)
      00B941                        841 _ak820_rgb_actions:
      00B941 B8 50                  842 	.byte _rgb_matrix_step, (_rgb_matrix_step >> 8)
      00B943 BE 50                  843 	.byte _rgb_matrix_step_reverse, (_rgb_matrix_step_reverse >> 8)
      00B945 C4 50                  844 	.byte _rgb_matrix_increase_hue, (_rgb_matrix_increase_hue >> 8)
      00B947 CA 50                  845 	.byte _rgb_matrix_decrease_hue, (_rgb_matrix_decrease_hue >> 8)
      00B949 D0 50                  846 	.byte _rgb_matrix_increase_sat, (_rgb_matrix_increase_sat >> 8)
      00B94B D6 50                  847 	.byte _rgb_matrix_decrease_sat, (_rgb_matrix_decrease_sat >> 8)
      00B94D DC 50                  848 	.byte _rgb_matrix_increase_val, (_rgb_matrix_increase_val >> 8)
      00B94F E2 50                  849 	.byte _rgb_matrix_decrease_val, (_rgb_matrix_decrease_val >> 8)
      00B951 E8 50                  850 	.byte _rgb_matrix_increase_speed, (_rgb_matrix_increase_speed >> 8)
      00B953 EE 50                  851 	.byte _rgb_matrix_decrease_speed, (_rgb_matrix_decrease_speed >> 8)
                                    852 	.area CSEG    (CODE)
                                    853 	.area XINIT   (CODE)
                                    854 	.area CABS    (ABS,CODE)
                                    855 
                                    856 ; Experimental exact instruction outlining.
                                    857 	.globl _ak820_outline_0002
                                    858 	.globl _ak820_outline_0018
                                    859 
                                    860 	.area CSEG (CODE)
                                    861 ; function ak820_outline_0018
      0096F1                        862 _ak820_outline_0018:
      0096F1 74 05            [12]  863 	mov	a,#0x05
      0096F3 2D               [12]  864 	add	a,r5
      0096F4 FD               [12]  865 	mov	r5,a
      0096F5 E4               [12]  866 	clr	a
      0096F6 3E               [12]  867 	addc	a,r6
      0096F7 FE               [12]  868 	mov	r6,a
      0096F8 8D 82            [24]  869 	mov	dpl,r5
      0096FA 8E 83            [24]  870 	mov	dph,r6
      0096FC 8F F0            [24]  871 	mov	b,r7
      0096FE 22               [24]  872 	ret
