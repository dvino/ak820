                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module process_tri_layer
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _update_tri_layer
                                     12 	.globl _layer_off
                                     13 	.globl _layer_on
                                     14 	.globl _get_tri_layer_adjust_layer
                                     15 	.globl _get_tri_layer_upper_layer
                                     16 	.globl _get_tri_layer_lower_layer
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
                                    260 	.globl _process_tri_layer_PARM_2
                                    261 	.globl _process_tri_layer
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
                                    524 ;--------------------------------------------------------
                                    525 ; overlayable items in internal ram
                                    526 ;--------------------------------------------------------
                                    527 ;--------------------------------------------------------
                                    528 ; indirectly addressable internal ram data
                                    529 ;--------------------------------------------------------
                                    530 	.area ISEG    (DATA)
                                    531 ;--------------------------------------------------------
                                    532 ; absolute internal ram data
                                    533 ;--------------------------------------------------------
                                    534 	.area IABS    (ABS,DATA)
                                    535 	.area IABS    (ABS,DATA)
                                    536 ;--------------------------------------------------------
                                    537 ; bit data
                                    538 ;--------------------------------------------------------
                                    539 	.area BSEG    (BIT)
                                    540 ;--------------------------------------------------------
                                    541 ; paged external ram data
                                    542 ;--------------------------------------------------------
                                    543 	.area PSEG    (PAG,XDATA)
                                    544 ;--------------------------------------------------------
                                    545 ; uninitialized external ram data
                                    546 ;--------------------------------------------------------
                                    547 	.area XSEG    (XDATA)
      0009CB                        548 _process_tri_layer_PARM_2:
      0009CB                        549 	.ds 3
      0009CE                        550 _process_tri_layer_keycode_10000_165:
      0009CE                        551 	.ds 2
      0009D0                        552 _process_tri_layer_layer_10000_166:
      0009D0                        553 	.ds 1
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
                                    589 ;Allocation info for local variables in function 'process_tri_layer'
                                    590 ;------------------------------------------------------------
                                    591 ;record        Allocated with name '_process_tri_layer_PARM_2'
                                    592 ;keycode       Allocated with name '_process_tri_layer_keycode_10000_165'
                                    593 ;layer         Allocated with name '_process_tri_layer_layer_10000_166'
                                    594 ;------------------------------------------------------------
                                    595 ;	quantum/process_keycode/process_tri_layer.c:8: bool process_tri_layer(uint16_t keycode, keyrecord_t *record) {
                                    596 ;	-----------------------------------------
                                    597 ;	 function process_tri_layer
                                    598 ;	-----------------------------------------
      009702                        599 _process_tri_layer:
                           000007   600 	ar7 = 0x07
                           000006   601 	ar6 = 0x06
                           000005   602 	ar5 = 0x05
                           000004   603 	ar4 = 0x04
                           000003   604 	ar3 = 0x03
                           000002   605 	ar2 = 0x02
                           000001   606 	ar1 = 0x01
                           000000   607 	ar0 = 0x00
      009702 AF 83            [24]  608 	mov	r7,dph
      009704 E5 82            [12]  609 	mov	a,dpl
      009706 90 09 CE         [24]  610 	mov	dptr,#_process_tri_layer_keycode_10000_165
      009709 F0               [24]  611 	movx	@dptr,a
      00970A EF               [12]  612 	mov	a,r7
      00970B A3               [24]  613 	inc	dptr
      00970C F0               [24]  614 	movx	@dptr,a
                                    615 ;	quantum/process_keycode/process_tri_layer.c:10: if (keycode == QK_TRI_LAYER_LOWER) {
      00970D 90 09 CE         [24]  616 	mov	dptr,#_process_tri_layer_keycode_10000_165
      009710 E0               [24]  617 	movx	a,@dptr
      009711 FE               [12]  618 	mov	r6,a
      009712 A3               [24]  619 	inc	dptr
      009713 E0               [24]  620 	movx	a,@dptr
      009714 FF               [12]  621 	mov	r7,a
      009715 BE 77 0E         [24]  622 	cjne	r6,#0x77,00105$
      009718 BF 7C 0B         [24]  623 	cjne	r7,#0x7c,00105$
                                    624 ;	quantum/process_keycode/process_tri_layer.c:11: layer = get_tri_layer_lower_layer();
      00971B 12 A0 3E         [24]  625 	lcall	_get_tri_layer_lower_layer
      00971E E5 82            [12]  626 	mov	a, dpl
      009720 90 09 D0         [24]  627 	mov	dptr,#_process_tri_layer_layer_10000_166
      009723 F0               [24]  628 	movx	@dptr,a
      009724 80 15            [24]  629 	sjmp	00106$
      009726                        630 00105$:
                                    631 ;	quantum/process_keycode/process_tri_layer.c:12: } else if (keycode == QK_TRI_LAYER_UPPER) {
      009726 BE 78 0E         [24]  632 	cjne	r6,#0x78,00102$
      009729 BF 7C 0B         [24]  633 	cjne	r7,#0x7c,00102$
                                    634 ;	quantum/process_keycode/process_tri_layer.c:13: layer = get_tri_layer_upper_layer();
      00972C 12 A0 45         [24]  635 	lcall	_get_tri_layer_upper_layer
      00972F E5 82            [12]  636 	mov	a, dpl
      009731 90 09 D0         [24]  637 	mov	dptr,#_process_tri_layer_layer_10000_166
      009734 F0               [24]  638 	movx	@dptr,a
      009735 80 04            [24]  639 	sjmp	00106$
      009737                        640 00102$:
                                    641 ;	quantum/process_keycode/process_tri_layer.c:15: return true;
      009737 75 82 01         [24]  642 	mov	dpl, #0x01
      00973A 22               [24]  643 	ret
      00973B                        644 00106$:
                                    645 ;	quantum/process_keycode/process_tri_layer.c:17: if (record->event.pressed) {
      00973B 90 09 CB         [24]  646 	mov	dptr,#_process_tri_layer_PARM_2
      00973E 12 73 B8         [24]  647 	lcall	_ak820_outline_0002
      009741 12 96 F4         [24]  648 	lcall	_ak820_outline_0018
      009744 12 B5 9A         [24]  649 	lcall	__gptrget
      009747 60 0B            [24]  650 	jz	00108$
                                    651 ;	quantum/process_keycode/process_tri_layer.c:18: layer_on(layer);
      009749 90 09 D0         [24]  652 	mov	dptr,#_process_tri_layer_layer_10000_166
      00974C E0               [24]  653 	movx	a,@dptr
      00974D F5 82            [12]  654 	mov	dpl,a
      00974F 12 74 B0         [24]  655 	lcall	_layer_on
      009752 80 09            [24]  656 	sjmp	00109$
      009754                        657 00108$:
                                    658 ;	quantum/process_keycode/process_tri_layer.c:20: layer_off(layer);
      009754 90 09 D0         [24]  659 	mov	dptr,#_process_tri_layer_layer_10000_166
      009757 E0               [24]  660 	movx	a,@dptr
      009758 F5 82            [12]  661 	mov	dpl,a
      00975A 12 74 D0         [24]  662 	lcall	_layer_off
      00975D                        663 00109$:
                                    664 ;	quantum/process_keycode/process_tri_layer.c:22: update_tri_layer(get_tri_layer_lower_layer(), get_tri_layer_upper_layer(), get_tri_layer_adjust_layer());
      00975D 12 A0 3E         [24]  665 	lcall	_get_tri_layer_lower_layer
      009760 AF 82            [24]  666 	mov	r7, dpl
      009762 C0 07            [24]  667 	push	ar7
      009764 12 A0 45         [24]  668 	lcall	_get_tri_layer_upper_layer
      009767 AE 82            [24]  669 	mov	r6, dpl
      009769 C0 06            [24]  670 	push	ar6
      00976B 12 A0 4C         [24]  671 	lcall	_get_tri_layer_adjust_layer
      00976E AD 82            [24]  672 	mov	r5, dpl
      009770 D0 06            [24]  673 	pop	ar6
      009772 D0 07            [24]  674 	pop	ar7
      009774 90 08 95         [24]  675 	mov	dptr,#_update_tri_layer_PARM_2
      009777 EE               [12]  676 	mov	a,r6
      009778 F0               [24]  677 	movx	@dptr,a
      009779 90 08 96         [24]  678 	mov	dptr,#_update_tri_layer_PARM_3
      00977C ED               [12]  679 	mov	a,r5
      00977D F0               [24]  680 	movx	@dptr,a
      00977E 8F 82            [24]  681 	mov	dpl, r7
      009780 12 77 E8         [24]  682 	lcall	_update_tri_layer
                                    683 ;	quantum/process_keycode/process_tri_layer.c:23: return false;
      009783 75 82 00         [24]  684 	mov	dpl, #0x00
                                    685 ;	quantum/process_keycode/process_tri_layer.c:24: }
      009786 22               [24]  686 	ret
                                    687 	.area CSEG    (CODE)
                                    688 	.area CONST   (CODE)
                                    689 	.area XINIT   (CODE)
                                    690 	.area CABS    (ABS,CODE)
                                    691 
                                    692 ; Experimental exact instruction outlining.
                                    693 	.globl _ak820_outline_0002
                                    694 	.globl _ak820_outline_0018
