                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module sym_defer_g
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _timer_elapsed
                                     12 	.globl _timer_read
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
                                    256 	.globl _debounce_PARM_4
                                    257 	.globl _debounce_PARM_3
                                    258 	.globl _debounce_PARM_2
                                    259 	.globl _debounce_init
                                    260 	.globl _debounce
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
      000017                        523 _debounce_sloc0_1_0:
      000017                        524 	.ds 1
                                    525 ;--------------------------------------------------------
                                    526 ; overlayable items in internal ram
                                    527 ;--------------------------------------------------------
                                    528 ;--------------------------------------------------------
                                    529 ; indirectly addressable internal ram data
                                    530 ;--------------------------------------------------------
                                    531 	.area ISEG    (DATA)
                                    532 ;--------------------------------------------------------
                                    533 ; absolute internal ram data
                                    534 ;--------------------------------------------------------
                                    535 	.area IABS    (ABS,DATA)
                                    536 	.area IABS    (ABS,DATA)
                                    537 ;--------------------------------------------------------
                                    538 ; bit data
                                    539 ;--------------------------------------------------------
                                    540 	.area BSEG    (BIT)
                                    541 ;--------------------------------------------------------
                                    542 ; paged external ram data
                                    543 ;--------------------------------------------------------
                                    544 	.area PSEG    (PAG,XDATA)
                                    545 ;--------------------------------------------------------
                                    546 ; uninitialized external ram data
                                    547 ;--------------------------------------------------------
                                    548 	.area XSEG    (XDATA)
      0008CC                        549 _debouncing_time:
      0008CC                        550 	.ds 2
      0008CE                        551 _debounce_PARM_2:
      0008CE                        552 	.ds 3
      0008D1                        553 _debounce_PARM_3:
      0008D1                        554 	.ds 1
      0008D2                        555 _debounce_PARM_4:
      0008D2                        556 	.ds 1
      0008D3                        557 _debounce_raw_10000_118:
      0008D3                        558 	.ds 3
      0008D6                        559 _debounce_cooked_changed_10000_119:
      0008D6                        560 	.ds 1
                                    561 ;--------------------------------------------------------
                                    562 ; absolute external ram data
                                    563 ;--------------------------------------------------------
                                    564 	.area XABS    (ABS,XDATA)
                                    565 ;--------------------------------------------------------
                                    566 ; initialized external ram data
                                    567 ;--------------------------------------------------------
                                    568 	.area XISEG   (XDATA)
      000BD4                        569 _debouncing:
      000BD4                        570 	.ds 1
                                    571 	.area HOME    (CODE)
                                    572 	.area GSINIT0 (CODE)
                                    573 	.area GSINIT1 (CODE)
                                    574 	.area GSINIT2 (CODE)
                                    575 	.area GSINIT3 (CODE)
                                    576 	.area GSINIT4 (CODE)
                                    577 	.area GSINIT5 (CODE)
                                    578 	.area GSINIT  (CODE)
                                    579 	.area GSFINAL (CODE)
                                    580 	.area CSEG    (CODE)
                                    581 ;--------------------------------------------------------
                                    582 ; global & static initialisations
                                    583 ;--------------------------------------------------------
                                    584 	.area HOME    (CODE)
                                    585 	.area GSINIT  (CODE)
                                    586 	.area GSFINAL (CODE)
                                    587 	.area GSINIT  (CODE)
                                    588 ;--------------------------------------------------------
                                    589 ; Home
                                    590 ;--------------------------------------------------------
                                    591 	.area HOME    (CODE)
                                    592 	.area HOME    (CODE)
                                    593 ;--------------------------------------------------------
                                    594 ; code
                                    595 ;--------------------------------------------------------
                                    596 	.area CSEG    (CODE)
                                    597 ;------------------------------------------------------------
                                    598 ;Allocation info for local variables in function 'debounce_init'
                                    599 ;------------------------------------------------------------
                                    600 ;num_rows      Allocated with name '_debounce_init_num_rows_10000_115'
                                    601 ;------------------------------------------------------------
                                    602 ;	quantum/debounce/sym_defer_g.c:32: void debounce_init(uint8_t num_rows) {}
                                    603 ;	-----------------------------------------
                                    604 ;	 function debounce_init
                                    605 ;	-----------------------------------------
      007AFD                        606 _debounce_init:
                           000007   607 	ar7 = 0x07
                           000006   608 	ar6 = 0x06
                           000005   609 	ar5 = 0x05
                           000004   610 	ar4 = 0x04
                           000003   611 	ar3 = 0x03
                           000002   612 	ar2 = 0x02
                           000001   613 	ar1 = 0x01
                           000000   614 	ar0 = 0x00
      007AFD 22               [24]  615 	ret
                                    616 ;------------------------------------------------------------
                                    617 ;Allocation info for local variables in function 'debounce'
                                    618 ;------------------------------------------------------------
                                    619 ;sloc0         Allocated with name '_debounce_sloc0_1_0'
                                    620 ;cooked        Allocated with name '_debounce_PARM_2'
                                    621 ;num_rows      Allocated with name '_debounce_PARM_3'
                                    622 ;changed       Allocated with name '_debounce_PARM_4'
                                    623 ;raw           Allocated with name '_debounce_raw_10000_118'
                                    624 ;__200000060   Allocated with name '_debounce___200000060_20000_119'
                                    625 ;cooked_changed Allocated with name '_debounce_cooked_changed_10000_119'
                                    626 ;__400000058   Allocated with name '_debounce___400000058_40000_121'
                                    627 ;__300000061   Allocated with name '_debounce___300000061_30000_131'
                                    628 ;last          Allocated with name '_debounce_last_40000_132'
                                    629 ;dest          Allocated with name '_debounce_dest_30000_123'
                                    630 ;src           Allocated with name '_debounce_src_30000_123'
                                    631 ;i             Allocated with name '_debounce_i_40000_124'
                                    632 ;------------------------------------------------------------
                                    633 ;	quantum/debounce/sym_defer_g.c:34: bool debounce(matrix_row_t raw[], matrix_row_t cooked[], uint8_t num_rows, bool changed) {
                                    634 ;	-----------------------------------------
                                    635 ;	 function debounce
                                    636 ;	-----------------------------------------
      007AFE                        637 _debounce:
      007AFE AF F0            [24]  638 	mov	r7,b
      007B00 AE 83            [24]  639 	mov	r6,dph
      007B02 E5 82            [12]  640 	mov	a,dpl
      007B04 90 08 D3         [24]  641 	mov	dptr,#_debounce_raw_10000_118
      007B07 F0               [24]  642 	movx	@dptr,a
      007B08 EE               [12]  643 	mov	a,r6
      007B09 A3               [24]  644 	inc	dptr
      007B0A F0               [24]  645 	movx	@dptr,a
      007B0B EF               [12]  646 	mov	a,r7
      007B0C A3               [24]  647 	inc	dptr
      007B0D F0               [24]  648 	movx	@dptr,a
                                    649 ;	quantum/debounce/sym_defer_g.c:35: bool cooked_changed = false;
      007B0E 90 08 D6         [24]  650 	mov	dptr,#_debounce_cooked_changed_10000_119
      007B11 E4               [12]  651 	clr	a
      007B12 F0               [24]  652 	movx	@dptr,a
                                    653 ;	quantum/debounce/sym_defer_g.c:37: if (changed) {
      007B13 90 08 D2         [24]  654 	mov	dptr,#_debounce_PARM_4
      007B16 E0               [24]  655 	movx	a,@dptr
      007B17 60 16            [24]  656 	jz	00102$
                                    657 ;	quantum/debounce/sym_defer_g.c:38: debouncing      = true;
      007B19 90 0B D4         [24]  658 	mov	dptr,#_debouncing
      007B1C 74 01            [12]  659 	mov	a,#0x01
      007B1E F0               [24]  660 	movx	@dptr,a
                                    661 ;	platforms/timer.h:62: return timer_read();
      007B1F 12 40 6D         [24]  662 	lcall	_timer_read
      007B22 E5 82            [12]  663 	mov	a, dpl
      007B24 85 83 F0         [24]  664 	mov	b, dph
                                    665 ;	quantum/debounce/sym_defer_g.c:39: debouncing_time = timer_read_fast();
      007B27 90 08 CC         [24]  666 	mov	dptr,#_debouncing_time
      007B2A F0               [24]  667 	movx	@dptr,a
      007B2B E5 F0            [12]  668 	mov	a,b
      007B2D A3               [24]  669 	inc	dptr
      007B2E F0               [24]  670 	movx	@dptr,a
      007B2F                        671 00102$:
                                    672 ;	quantum/debounce/sym_defer_g.c:42: if (debouncing && timer_elapsed_fast(debouncing_time) >= DEBOUNCE) {
      007B2F 90 0B D4         [24]  673 	mov	dptr,#_debouncing
      007B32 E0               [24]  674 	movx	a,@dptr
      007B33 60 6A            [24]  675 	jz	00107$
      007B35 90 08 CC         [24]  676 	mov	dptr,#_debouncing_time
      007B38 12 73 CF         [24]  677 	lcall	_ak820_outline_0013
                                    678 ;	platforms/timer.h:65: return timer_elapsed(last);
      007B3B 12 40 70         [24]  679 	lcall	_timer_elapsed
      007B3E AE 82            [24]  680 	mov	r6, dpl
      007B40 AF 83            [24]  681 	mov	r7, dph
                                    682 ;	quantum/debounce/sym_defer_g.c:42: if (debouncing && timer_elapsed_fast(debouncing_time) >= DEBOUNCE) {
      007B42 C3               [12]  683 	clr	c
      007B43 EE               [12]  684 	mov	a,r6
      007B44 94 05            [12]  685 	subb	a,#0x05
      007B46 EF               [12]  686 	mov	a,r7
      007B47 94 00            [12]  687 	subb	a,#0x00
      007B49 40 54            [24]  688 	jc	00107$
                                    689 ;	quantum/debounce/sym_defer_g.c:44: matrix_row_t __xdata *dest = (matrix_row_t __xdata *)cooked;
      007B4B 90 08 CE         [24]  690 	mov	dptr,#_debounce_PARM_2
      007B4E E0               [24]  691 	movx	a,@dptr
      007B4F FE               [12]  692 	mov	r6,a
      007B50 A3               [24]  693 	inc	dptr
      007B51 E0               [24]  694 	movx	a,@dptr
      007B52 FF               [12]  695 	mov	r7,a
                                    696 ;	quantum/debounce/sym_defer_g.c:45: const matrix_row_t __xdata *src = (const matrix_row_t __xdata *)raw;
      007B53 90 08 D3         [24]  697 	mov	dptr,#_debounce_raw_10000_118
      007B56 E0               [24]  698 	movx	a,@dptr
      007B57 FC               [12]  699 	mov	r4,a
      007B58 A3               [24]  700 	inc	dptr
      007B59 E0               [24]  701 	movx	a,@dptr
      007B5A FD               [12]  702 	mov	r5,a
                                    703 ;	quantum/debounce/sym_defer_g.c:50: for (uint8_t i = 0; i < num_rows; ++i) {
      007B5B 90 08 D1         [24]  704 	mov	dptr,#_debounce_PARM_3
      007B5E E0               [24]  705 	movx	a,@dptr
      007B5F FB               [12]  706 	mov	r3,a
      007B60 7A 00            [12]  707 	mov	r2,#0x00
      007B62                        708 00112$:
      007B62 C3               [12]  709 	clr	c
      007B63 EA               [12]  710 	mov	a,r2
      007B64 9B               [12]  711 	subb	a,r3
      007B65 50 33            [24]  712 	jnc	00105$
                                    713 ;	quantum/debounce/sym_defer_g.c:51: if (dest[i] != src[i]) {
      007B67 C0 03            [24]  714 	push	ar3
      007B69 EA               [12]  715 	mov	a,r2
      007B6A 2E               [12]  716 	add	a, r6
      007B6B F8               [12]  717 	mov	r0,a
      007B6C E4               [12]  718 	clr	a
      007B6D 3F               [12]  719 	addc	a, r7
      007B6E F9               [12]  720 	mov	r1,a
      007B6F 88 82            [24]  721 	mov	dpl,r0
      007B71 89 83            [24]  722 	mov	dph,r1
      007B73 E0               [24]  723 	movx	a,@dptr
      007B74 FB               [12]  724 	mov	r3,a
      007B75 EA               [12]  725 	mov	a,r2
      007B76 2C               [12]  726 	add	a, r4
      007B77 F5 82            [12]  727 	mov	dpl,a
      007B79 E4               [12]  728 	clr	a
      007B7A 3D               [12]  729 	addc	a, r5
      007B7B F5 83            [12]  730 	mov	dph,a
      007B7D E0               [24]  731 	movx	a,@dptr
      007B7E F5 17            [12]  732 	mov	_debounce_sloc0_1_0,a
      007B80 EB               [12]  733 	mov	a,r3
      007B81 B5 17 04         [24]  734 	cjne	a,_debounce_sloc0_1_0,00163$
      007B84 D0 03            [24]  735 	pop	ar3
      007B86 80 0F            [24]  736 	sjmp	00113$
      007B88                        737 00163$:
      007B88 D0 03            [24]  738 	pop	ar3
                                    739 ;	quantum/debounce/sym_defer_g.c:52: dest[i] = src[i];
      007B8A 88 82            [24]  740 	mov	dpl,r0
      007B8C 89 83            [24]  741 	mov	dph,r1
      007B8E E5 17            [12]  742 	mov	a,_debounce_sloc0_1_0
      007B90 F0               [24]  743 	movx	@dptr,a
                                    744 ;	quantum/debounce/sym_defer_g.c:53: cooked_changed = true;
      007B91 90 08 D6         [24]  745 	mov	dptr,#_debounce_cooked_changed_10000_119
      007B94 74 01            [12]  746 	mov	a,#0x01
      007B96 F0               [24]  747 	movx	@dptr,a
      007B97                        748 00113$:
                                    749 ;	quantum/debounce/sym_defer_g.c:50: for (uint8_t i = 0; i < num_rows; ++i) {
      007B97 0A               [12]  750 	inc	r2
      007B98 80 C8            [24]  751 	sjmp	00112$
      007B9A                        752 00105$:
                                    753 ;	quantum/debounce/sym_defer_g.c:56: debouncing = false;
      007B9A 90 0B D4         [24]  754 	mov	dptr,#_debouncing
      007B9D E4               [12]  755 	clr	a
      007B9E F0               [24]  756 	movx	@dptr,a
      007B9F                        757 00107$:
                                    758 ;	quantum/debounce/sym_defer_g.c:59: return cooked_changed;
      007B9F 90 08 D6         [24]  759 	mov	dptr,#_debounce_cooked_changed_10000_119
      007BA2 E0               [24]  760 	movx	a,@dptr
                                    761 ;	quantum/debounce/sym_defer_g.c:60: }
      007BA3 F5 82            [12]  762 	mov	dpl,a
      007BA5 22               [24]  763 	ret
                                    764 ;------------------------------------------------------------
                                    765 ;Allocation info for local variables in function 'debounce_free'
                                    766 ;------------------------------------------------------------
                                    767 ;	quantum/debounce/sym_defer_g.c:62: void debounce_free(void) {}
                                    768 ;	-----------------------------------------
                                    769 	.area CSEG    (CODE)
                                    770 	.area CONST   (CODE)
                                    771 	.area XINIT   (CODE)
      00BDB4                        772 __xinit__debouncing:
      00BDB4 00                     773 	.db #0x00	;  0
                                    774 	.area CABS    (ABS,CODE)
                                    775 
                                    776 ; Experimental exact instruction outlining.
                                    777 	.globl _ak820_outline_0013
