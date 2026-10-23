                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module ak820_boot
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _bootloader_jump
                                     12 	.globl _mcu_reset
                                     13 	.globl _ak820_nvm_flush
                                     14 	.globl _ADC_START
                                     15 	.globl _S0_R_FIFO
                                     16 	.globl _S0_T_FIFO
                                     17 	.globl _S0_FREE
                                     18 	.globl _S0_IF_BYTE
                                     19 	.globl _S0_IF_FIRST
                                     20 	.globl _S0_IF_OV
                                     21 	.globl _S0_FST_ACT
                                     22 	.globl _CP_RL2
                                     23 	.globl _C_T2
                                     24 	.globl _TR2
                                     25 	.globl _EXEN2
                                     26 	.globl _TCLK
                                     27 	.globl _RCLK
                                     28 	.globl _EXF2
                                     29 	.globl _CAP1F
                                     30 	.globl _TF2
                                     31 	.globl _RI
                                     32 	.globl _TI
                                     33 	.globl _RB8
                                     34 	.globl _TB8
                                     35 	.globl _REN
                                     36 	.globl _SM2
                                     37 	.globl _SM1
                                     38 	.globl _SM0
                                     39 	.globl _IT0
                                     40 	.globl _IE0
                                     41 	.globl _IT1
                                     42 	.globl _IE1
                                     43 	.globl _TR0
                                     44 	.globl _TF0
                                     45 	.globl _TR1
                                     46 	.globl _TF1
                                     47 	.globl _P4_0
                                     48 	.globl _P4_1
                                     49 	.globl _P4_2
                                     50 	.globl _P4_3
                                     51 	.globl _P4_4
                                     52 	.globl _P4_5
                                     53 	.globl _P4_6
                                     54 	.globl _RXD
                                     55 	.globl _TXD
                                     56 	.globl _INT0
                                     57 	.globl _INT1
                                     58 	.globl _T0
                                     59 	.globl _T1
                                     60 	.globl _MOSI1
                                     61 	.globl _MISO1
                                     62 	.globl _SCK1
                                     63 	.globl _P3_0
                                     64 	.globl _P3_1
                                     65 	.globl _P3_2
                                     66 	.globl _P3_3
                                     67 	.globl _P3_4
                                     68 	.globl _P3_5
                                     69 	.globl _P3_6
                                     70 	.globl _P3_7
                                     71 	.globl _CAP1_
                                     72 	.globl _T2_
                                     73 	.globl _CAP2_
                                     74 	.globl _T2EX_
                                     75 	.globl _RXD1
                                     76 	.globl _TXD1
                                     77 	.globl _P2_0
                                     78 	.globl _P2_1
                                     79 	.globl _P2_2
                                     80 	.globl _P2_3
                                     81 	.globl _P2_4
                                     82 	.globl _P2_5
                                     83 	.globl _P2_6
                                     84 	.globl _P2_7
                                     85 	.globl _AIN0
                                     86 	.globl _AIN1
                                     87 	.globl _AIN2
                                     88 	.globl _AIN3
                                     89 	.globl _AIN4
                                     90 	.globl _AIN5
                                     91 	.globl _AIN6
                                     92 	.globl _AIN7
                                     93 	.globl _CAP1
                                     94 	.globl _T2
                                     95 	.globl _CAP2
                                     96 	.globl _T2EX
                                     97 	.globl _INT0_
                                     98 	.globl _SCS
                                     99 	.globl _MOSI
                                    100 	.globl _MISO
                                    101 	.globl _SCK
                                    102 	.globl _RXD1_
                                    103 	.globl _TXD1_
                                    104 	.globl _P1_0
                                    105 	.globl _P1_1
                                    106 	.globl _P1_2
                                    107 	.globl _P1_3
                                    108 	.globl _P1_4
                                    109 	.globl _P1_5
                                    110 	.globl _P1_6
                                    111 	.globl _P1_7
                                    112 	.globl _AIN8
                                    113 	.globl _AIN9
                                    114 	.globl _AIN10
                                    115 	.globl _AIN11
                                    116 	.globl _AIN12
                                    117 	.globl _AIN13
                                    118 	.globl _RXD_
                                    119 	.globl _TXD_
                                    120 	.globl _SCL0
                                    121 	.globl _SDA0
                                    122 	.globl _P0_0
                                    123 	.globl _P0_1
                                    124 	.globl _P0_2
                                    125 	.globl _P0_3
                                    126 	.globl _P0_4
                                    127 	.globl _P0_5
                                    128 	.globl _P0_6
                                    129 	.globl _P0_7
                                    130 	.globl _IE_SPI0
                                    131 	.globl _IE_USB
                                    132 	.globl _IE_ADC
                                    133 	.globl _IE_UART1
                                    134 	.globl _IE_PWM_I2C
                                    135 	.globl _IE_GPIO
                                    136 	.globl _IE_WDOG
                                    137 	.globl _PX0
                                    138 	.globl _PT0
                                    139 	.globl _PX1
                                    140 	.globl _PT1
                                    141 	.globl _PS
                                    142 	.globl _PT2
                                    143 	.globl _PL_FLAG
                                    144 	.globl _PH_FLAG
                                    145 	.globl _EX0
                                    146 	.globl _ET0
                                    147 	.globl _EX1
                                    148 	.globl _ET1
                                    149 	.globl _ES
                                    150 	.globl _ET2
                                    151 	.globl _E_DIS
                                    152 	.globl _EA
                                    153 	.globl _P
                                    154 	.globl _F1
                                    155 	.globl _OV
                                    156 	.globl _RS0
                                    157 	.globl _RS1
                                    158 	.globl _F0
                                    159 	.globl _AC
                                    160 	.globl _CY
                                    161 	.globl _I2CS_INT_ST
                                    162 	.globl _I2CX_INT
                                    163 	.globl _LED_STATUS
                                    164 	.globl _LED_DMA_H
                                    165 	.globl _LED_DMA_L
                                    166 	.globl _LED_DMA
                                    167 	.globl _LED_PWM_OE
                                    168 	.globl _LED_COMMON
                                    169 	.globl _ADC_CHAN
                                    170 	.globl _ADC_DAT_H
                                    171 	.globl _ADC_DAT_L
                                    172 	.globl _ADC_DAT
                                    173 	.globl _ADC_CTRL
                                    174 	.globl _SPI1_CK_SE
                                    175 	.globl _SPI1_CTRL
                                    176 	.globl _SPI1_DATA
                                    177 	.globl _SPI1_STAT
                                    178 	.globl _SIF1
                                    179 	.globl _SBAUD1
                                    180 	.globl _SBUF1
                                    181 	.globl _SCON1
                                    182 	.globl _SPI0_SETUP
                                    183 	.globl _SPI0_CK_SE
                                    184 	.globl _SPI0_CTRL
                                    185 	.globl _SPI0_DATA
                                    186 	.globl _SPI0_STAT
                                    187 	.globl _T2CAP1H
                                    188 	.globl _T2CAP1L
                                    189 	.globl _T2CAP1
                                    190 	.globl _TH2
                                    191 	.globl _TL2
                                    192 	.globl _T2COUNT
                                    193 	.globl _RCAP2H
                                    194 	.globl _RCAP2L
                                    195 	.globl _RCAP2
                                    196 	.globl _T2MOD
                                    197 	.globl _T2CON
                                    198 	.globl _SBUF
                                    199 	.globl _SCON
                                    200 	.globl _TH1
                                    201 	.globl _TH0
                                    202 	.globl _TL1
                                    203 	.globl _TL0
                                    204 	.globl _TMOD
                                    205 	.globl _TCON
                                    206 	.globl _XBUS_AUX
                                    207 	.globl _P7
                                    208 	.globl _P6_DIR
                                    209 	.globl _P6_OUT_PU
                                    210 	.globl _P6_IN
                                    211 	.globl _P5_DIR
                                    212 	.globl _P5_OUT_PU
                                    213 	.globl _P5_IN
                                    214 	.globl _P4_LED_KEY
                                    215 	.globl _P4_DIR_PU
                                    216 	.globl _P4_MOD_OC
                                    217 	.globl _P4
                                    218 	.globl _P3_DIR_PU
                                    219 	.globl _P3_MOD_OC
                                    220 	.globl _P3
                                    221 	.globl _P2_DIR_PU
                                    222 	.globl _P2_MOD_OC
                                    223 	.globl _P2
                                    224 	.globl _P1_DIR_PU
                                    225 	.globl _P1_MOD_OC
                                    226 	.globl _P1
                                    227 	.globl _P0_DIR_PU
                                    228 	.globl _P0_MOD_OC
                                    229 	.globl _P0
                                    230 	.globl _ROM_CTRL
                                    231 	.globl _ROM_DATA_HH
                                    232 	.globl _ROM_DATA_HL
                                    233 	.globl _ROM_DATA_HI
                                    234 	.globl _ROM_ADDR_H
                                    235 	.globl _ROM_ADDR_L
                                    236 	.globl _ROM_ADDR
                                    237 	.globl _GPIO_IE
                                    238 	.globl _IP_EX
                                    239 	.globl _IE_EX
                                    240 	.globl _IP
                                    241 	.globl _IE
                                    242 	.globl _WDOG_COUNT
                                    243 	.globl _RESET_KEEP
                                    244 	.globl _WAKE_CTRL
                                    245 	.globl _CLOCK_CFG
                                    246 	.globl _POWER_CFG
                                    247 	.globl _PCON
                                    248 	.globl _GLOBAL_CFG
                                    249 	.globl _SAFE_MOD
                                    250 	.globl _DPH
                                    251 	.globl _DPL
                                    252 	.globl _SP
                                    253 	.globl _A_INV
                                    254 	.globl _B
                                    255 	.globl _ACC
                                    256 	.globl _PSW
                                    257 ;--------------------------------------------------------
                                    258 ; special function registers
                                    259 ;--------------------------------------------------------
                                    260 	.area RSEG    (ABS,DATA)
      000000                        261 	.org 0x0000
                           0000D0   262 _PSW	=	0x00d0
                           0000E0   263 _ACC	=	0x00e0
                           0000F0   264 _B	=	0x00f0
                           0000FD   265 _A_INV	=	0x00fd
                           000081   266 _SP	=	0x0081
                           000082   267 _DPL	=	0x0082
                           000083   268 _DPH	=	0x0083
                           0000A1   269 _SAFE_MOD	=	0x00a1
                           0000B1   270 _GLOBAL_CFG	=	0x00b1
                           000087   271 _PCON	=	0x0087
                           0000BA   272 _POWER_CFG	=	0x00ba
                           0000B9   273 _CLOCK_CFG	=	0x00b9
                           0000A9   274 _WAKE_CTRL	=	0x00a9
                           0000FE   275 _RESET_KEEP	=	0x00fe
                           0000FF   276 _WDOG_COUNT	=	0x00ff
                           0000A8   277 _IE	=	0x00a8
                           0000B8   278 _IP	=	0x00b8
                           0000E8   279 _IE_EX	=	0x00e8
                           0000E9   280 _IP_EX	=	0x00e9
                           0000B2   281 _GPIO_IE	=	0x00b2
                           008584   282 _ROM_ADDR	=	0x8584
                           000084   283 _ROM_ADDR_L	=	0x0084
                           000085   284 _ROM_ADDR_H	=	0x0085
                           008F8E   285 _ROM_DATA_HI	=	0x8f8e
                           00008E   286 _ROM_DATA_HL	=	0x008e
                           00008F   287 _ROM_DATA_HH	=	0x008f
                           000086   288 _ROM_CTRL	=	0x0086
                           000080   289 _P0	=	0x0080
                           0000C4   290 _P0_MOD_OC	=	0x00c4
                           0000C5   291 _P0_DIR_PU	=	0x00c5
                           000090   292 _P1	=	0x0090
                           000092   293 _P1_MOD_OC	=	0x0092
                           000093   294 _P1_DIR_PU	=	0x0093
                           0000A0   295 _P2	=	0x00a0
                           000094   296 _P2_MOD_OC	=	0x0094
                           000095   297 _P2_DIR_PU	=	0x0095
                           0000B0   298 _P3	=	0x00b0
                           000096   299 _P3_MOD_OC	=	0x0096
                           000097   300 _P3_DIR_PU	=	0x0097
                           0000C0   301 _P4	=	0x00c0
                           0000C2   302 _P4_MOD_OC	=	0x00c2
                           0000C3   303 _P4_DIR_PU	=	0x00c3
                           0000C1   304 _P4_LED_KEY	=	0x00c1
                           0000AA   305 _P5_IN	=	0x00aa
                           0000AB   306 _P5_OUT_PU	=	0x00ab
                           0000AC   307 _P5_DIR	=	0x00ac
                           0000AD   308 _P6_IN	=	0x00ad
                           0000AE   309 _P6_OUT_PU	=	0x00ae
                           0000AF   310 _P6_DIR	=	0x00af
                           0000F1   311 _P7	=	0x00f1
                           0000A2   312 _XBUS_AUX	=	0x00a2
                           000088   313 _TCON	=	0x0088
                           000089   314 _TMOD	=	0x0089
                           00008A   315 _TL0	=	0x008a
                           00008B   316 _TL1	=	0x008b
                           00008C   317 _TH0	=	0x008c
                           00008D   318 _TH1	=	0x008d
                           000098   319 _SCON	=	0x0098
                           000099   320 _SBUF	=	0x0099
                           0000C8   321 _T2CON	=	0x00c8
                           0000C9   322 _T2MOD	=	0x00c9
                           00CBCA   323 _RCAP2	=	0xcbca
                           0000CA   324 _RCAP2L	=	0x00ca
                           0000CB   325 _RCAP2H	=	0x00cb
                           00CDCC   326 _T2COUNT	=	0xcdcc
                           0000CC   327 _TL2	=	0x00cc
                           0000CD   328 _TH2	=	0x00cd
                           00CFCE   329 _T2CAP1	=	0xcfce
                           0000CE   330 _T2CAP1L	=	0x00ce
                           0000CF   331 _T2CAP1H	=	0x00cf
                           0000F8   332 _SPI0_STAT	=	0x00f8
                           0000F9   333 _SPI0_DATA	=	0x00f9
                           0000FA   334 _SPI0_CTRL	=	0x00fa
                           0000FB   335 _SPI0_CK_SE	=	0x00fb
                           0000FC   336 _SPI0_SETUP	=	0x00fc
                           0000BC   337 _SCON1	=	0x00bc
                           0000BD   338 _SBUF1	=	0x00bd
                           0000BE   339 _SBAUD1	=	0x00be
                           0000BF   340 _SIF1	=	0x00bf
                           0000B4   341 _SPI1_STAT	=	0x00b4
                           0000B5   342 _SPI1_DATA	=	0x00b5
                           0000B6   343 _SPI1_CTRL	=	0x00b6
                           0000B7   344 _SPI1_CK_SE	=	0x00b7
                           0000F3   345 _ADC_CTRL	=	0x00f3
                           00F5F4   346 _ADC_DAT	=	0xf5f4
                           0000F4   347 _ADC_DAT_L	=	0x00f4
                           0000F5   348 _ADC_DAT_H	=	0x00f5
                           0000F6   349 _ADC_CHAN	=	0x00f6
                           0000A6   350 _LED_COMMON	=	0x00a6
                           0000A7   351 _LED_PWM_OE	=	0x00a7
                           00C7C6   352 _LED_DMA	=	0xc7c6
                           0000C6   353 _LED_DMA_L	=	0x00c6
                           0000C7   354 _LED_DMA_H	=	0x00c7
                           0000F7   355 _LED_STATUS	=	0x00f7
                           0000B3   356 _I2CX_INT	=	0x00b3
                           0000BB   357 _I2CS_INT_ST	=	0x00bb
                                    358 ;--------------------------------------------------------
                                    359 ; special function bits
                                    360 ;--------------------------------------------------------
                                    361 	.area RSEG    (ABS,DATA)
      000000                        362 	.org 0x0000
                           0000D7   363 _CY	=	0x00d7
                           0000D6   364 _AC	=	0x00d6
                           0000D5   365 _F0	=	0x00d5
                           0000D4   366 _RS1	=	0x00d4
                           0000D3   367 _RS0	=	0x00d3
                           0000D2   368 _OV	=	0x00d2
                           0000D1   369 _F1	=	0x00d1
                           0000D0   370 _P	=	0x00d0
                           0000AF   371 _EA	=	0x00af
                           0000AE   372 _E_DIS	=	0x00ae
                           0000AD   373 _ET2	=	0x00ad
                           0000AC   374 _ES	=	0x00ac
                           0000AB   375 _ET1	=	0x00ab
                           0000AA   376 _EX1	=	0x00aa
                           0000A9   377 _ET0	=	0x00a9
                           0000A8   378 _EX0	=	0x00a8
                           0000BF   379 _PH_FLAG	=	0x00bf
                           0000BE   380 _PL_FLAG	=	0x00be
                           0000BD   381 _PT2	=	0x00bd
                           0000BC   382 _PS	=	0x00bc
                           0000BB   383 _PT1	=	0x00bb
                           0000BA   384 _PX1	=	0x00ba
                           0000B9   385 _PT0	=	0x00b9
                           0000B8   386 _PX0	=	0x00b8
                           0000EF   387 _IE_WDOG	=	0x00ef
                           0000EE   388 _IE_GPIO	=	0x00ee
                           0000ED   389 _IE_PWM_I2C	=	0x00ed
                           0000EC   390 _IE_UART1	=	0x00ec
                           0000EB   391 _IE_ADC	=	0x00eb
                           0000E9   392 _IE_USB	=	0x00e9
                           0000E8   393 _IE_SPI0	=	0x00e8
                           000087   394 _P0_7	=	0x0087
                           000086   395 _P0_6	=	0x0086
                           000085   396 _P0_5	=	0x0085
                           000084   397 _P0_4	=	0x0084
                           000083   398 _P0_3	=	0x0083
                           000082   399 _P0_2	=	0x0082
                           000081   400 _P0_1	=	0x0081
                           000080   401 _P0_0	=	0x0080
                           000081   402 _SDA0	=	0x0081
                           000080   403 _SCL0	=	0x0080
                           000083   404 _TXD_	=	0x0083
                           000082   405 _RXD_	=	0x0082
                           000085   406 _AIN13	=	0x0085
                           000084   407 _AIN12	=	0x0084
                           000083   408 _AIN11	=	0x0083
                           000082   409 _AIN10	=	0x0082
                           000081   410 _AIN9	=	0x0081
                           000080   411 _AIN8	=	0x0080
                           000097   412 _P1_7	=	0x0097
                           000096   413 _P1_6	=	0x0096
                           000095   414 _P1_5	=	0x0095
                           000094   415 _P1_4	=	0x0094
                           000093   416 _P1_3	=	0x0093
                           000092   417 _P1_2	=	0x0092
                           000091   418 _P1_1	=	0x0091
                           000090   419 _P1_0	=	0x0090
                           000097   420 _TXD1_	=	0x0097
                           000096   421 _RXD1_	=	0x0096
                           000097   422 _SCK	=	0x0097
                           000096   423 _MISO	=	0x0096
                           000095   424 _MOSI	=	0x0095
                           000094   425 _SCS	=	0x0094
                           000092   426 _INT0_	=	0x0092
                           000091   427 _T2EX	=	0x0091
                           000091   428 _CAP2	=	0x0091
                           000090   429 _T2	=	0x0090
                           000090   430 _CAP1	=	0x0090
                           000097   431 _AIN7	=	0x0097
                           000096   432 _AIN6	=	0x0096
                           000095   433 _AIN5	=	0x0095
                           000094   434 _AIN4	=	0x0094
                           000093   435 _AIN3	=	0x0093
                           000092   436 _AIN2	=	0x0092
                           000091   437 _AIN1	=	0x0091
                           000090   438 _AIN0	=	0x0090
                           0000A7   439 _P2_7	=	0x00a7
                           0000A6   440 _P2_6	=	0x00a6
                           0000A5   441 _P2_5	=	0x00a5
                           0000A4   442 _P2_4	=	0x00a4
                           0000A3   443 _P2_3	=	0x00a3
                           0000A2   444 _P2_2	=	0x00a2
                           0000A1   445 _P2_1	=	0x00a1
                           0000A0   446 _P2_0	=	0x00a0
                           0000A7   447 _TXD1	=	0x00a7
                           0000A6   448 _RXD1	=	0x00a6
                           0000A5   449 _T2EX_	=	0x00a5
                           0000A5   450 _CAP2_	=	0x00a5
                           0000A4   451 _T2_	=	0x00a4
                           0000A4   452 _CAP1_	=	0x00a4
                           0000B7   453 _P3_7	=	0x00b7
                           0000B6   454 _P3_6	=	0x00b6
                           0000B5   455 _P3_5	=	0x00b5
                           0000B4   456 _P3_4	=	0x00b4
                           0000B3   457 _P3_3	=	0x00b3
                           0000B2   458 _P3_2	=	0x00b2
                           0000B1   459 _P3_1	=	0x00b1
                           0000B0   460 _P3_0	=	0x00b0
                           0000B7   461 _SCK1	=	0x00b7
                           0000B6   462 _MISO1	=	0x00b6
                           0000B5   463 _MOSI1	=	0x00b5
                           0000B5   464 _T1	=	0x00b5
                           0000B4   465 _T0	=	0x00b4
                           0000B3   466 _INT1	=	0x00b3
                           0000B2   467 _INT0	=	0x00b2
                           0000B1   468 _TXD	=	0x00b1
                           0000B0   469 _RXD	=	0x00b0
                           0000C6   470 _P4_6	=	0x00c6
                           0000C5   471 _P4_5	=	0x00c5
                           0000C4   472 _P4_4	=	0x00c4
                           0000C3   473 _P4_3	=	0x00c3
                           0000C2   474 _P4_2	=	0x00c2
                           0000C1   475 _P4_1	=	0x00c1
                           0000C0   476 _P4_0	=	0x00c0
                           00008F   477 _TF1	=	0x008f
                           00008E   478 _TR1	=	0x008e
                           00008D   479 _TF0	=	0x008d
                           00008C   480 _TR0	=	0x008c
                           00008B   481 _IE1	=	0x008b
                           00008A   482 _IT1	=	0x008a
                           000089   483 _IE0	=	0x0089
                           000088   484 _IT0	=	0x0088
                           00009F   485 _SM0	=	0x009f
                           00009E   486 _SM1	=	0x009e
                           00009D   487 _SM2	=	0x009d
                           00009C   488 _REN	=	0x009c
                           00009B   489 _TB8	=	0x009b
                           00009A   490 _RB8	=	0x009a
                           000099   491 _TI	=	0x0099
                           000098   492 _RI	=	0x0098
                           0000CF   493 _TF2	=	0x00cf
                           0000CF   494 _CAP1F	=	0x00cf
                           0000CE   495 _EXF2	=	0x00ce
                           0000CD   496 _RCLK	=	0x00cd
                           0000CC   497 _TCLK	=	0x00cc
                           0000CB   498 _EXEN2	=	0x00cb
                           0000CA   499 _TR2	=	0x00ca
                           0000C9   500 _C_T2	=	0x00c9
                           0000C8   501 _CP_RL2	=	0x00c8
                           0000FF   502 _S0_FST_ACT	=	0x00ff
                           0000FE   503 _S0_IF_OV	=	0x00fe
                           0000FD   504 _S0_IF_FIRST	=	0x00fd
                           0000FC   505 _S0_IF_BYTE	=	0x00fc
                           0000FB   506 _S0_FREE	=	0x00fb
                           0000FA   507 _S0_T_FIFO	=	0x00fa
                           0000F8   508 _S0_R_FIFO	=	0x00f8
                           0000F7   509 _ADC_START	=	0x00f7
                                    510 ;--------------------------------------------------------
                                    511 ; overlayable register banks
                                    512 ;--------------------------------------------------------
                                    513 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        514 	.ds 8
                                    515 ;--------------------------------------------------------
                                    516 ; internal ram data
                                    517 ;--------------------------------------------------------
                                    518 	.area DSEG    (DATA)
                                    519 ;--------------------------------------------------------
                                    520 ; overlayable items in internal ram
                                    521 ;--------------------------------------------------------
                                    522 ;--------------------------------------------------------
                                    523 ; indirectly addressable internal ram data
                                    524 ;--------------------------------------------------------
                                    525 	.area ISEG    (DATA)
                                    526 ;--------------------------------------------------------
                                    527 ; absolute internal ram data
                                    528 ;--------------------------------------------------------
                                    529 	.area IABS    (ABS,DATA)
                                    530 	.area IABS    (ABS,DATA)
                                    531 ;--------------------------------------------------------
                                    532 ; bit data
                                    533 ;--------------------------------------------------------
                                    534 	.area BSEG    (BIT)
                                    535 ;--------------------------------------------------------
                                    536 ; paged external ram data
                                    537 ;--------------------------------------------------------
                                    538 	.area PSEG    (PAG,XDATA)
                                    539 ;--------------------------------------------------------
                                    540 ; uninitialized external ram data
                                    541 ;--------------------------------------------------------
                                    542 	.area XSEG    (XDATA)
      00041A                        543 _bootloader_jump_saved_ie_10000_15:
      00041A                        544 	.ds 1
                                    545 ;--------------------------------------------------------
                                    546 ; absolute external ram data
                                    547 ;--------------------------------------------------------
                                    548 	.area XABS    (ABS,XDATA)
                                    549 ;--------------------------------------------------------
                                    550 ; initialized external ram data
                                    551 ;--------------------------------------------------------
                                    552 	.area XISEG   (XDATA)
                                    553 	.area HOME    (CODE)
                                    554 	.area GSINIT0 (CODE)
                                    555 	.area GSINIT1 (CODE)
                                    556 	.area GSINIT2 (CODE)
                                    557 	.area GSINIT3 (CODE)
                                    558 	.area GSINIT4 (CODE)
                                    559 	.area GSINIT5 (CODE)
                                    560 	.area GSINIT  (CODE)
                                    561 	.area GSFINAL (CODE)
                                    562 	.area CSEG    (CODE)
                                    563 ;--------------------------------------------------------
                                    564 ; global & static initialisations
                                    565 ;--------------------------------------------------------
                                    566 	.area HOME    (CODE)
                                    567 	.area GSINIT  (CODE)
                                    568 	.area GSFINAL (CODE)
                                    569 	.area GSINIT  (CODE)
                                    570 ;--------------------------------------------------------
                                    571 ; Home
                                    572 ;--------------------------------------------------------
                                    573 	.area HOME    (CODE)
                                    574 	.area HOME    (CODE)
                                    575 ;--------------------------------------------------------
                                    576 ; code
                                    577 ;--------------------------------------------------------
                                    578 	.area CSEG    (CODE)
                                    579 ;------------------------------------------------------------
                                    580 ;Allocation info for local variables in function 'mcu_reset'
                                    581 ;------------------------------------------------------------
                                    582 ;	keyboards/ajazz/ak820/ak820_boot.c:5: void mcu_reset(void) {
                                    583 ;	-----------------------------------------
                                    584 ;	 function mcu_reset
                                    585 ;	-----------------------------------------
      003487                        586 _mcu_reset:
                           000007   587 	ar7 = 0x07
                           000006   588 	ar6 = 0x06
                           000005   589 	ar5 = 0x05
                           000004   590 	ar4 = 0x04
                           000003   591 	ar3 = 0x03
                           000002   592 	ar2 = 0x02
                           000001   593 	ar1 = 0x01
                           000000   594 	ar0 = 0x00
                                    595 ;	keyboards/ajazz/ak820/ak820_boot.c:6: EA = 0;
                                    596 ;	assignBit
      003487 C2 AF            [12]  597 	clr	_EA
                                    598 ;	keyboards/ajazz/ak820/ak820_boot.c:7: SAFE_MOD = 0x55;
      003489 75 A1 55         [24]  599 	mov	_SAFE_MOD,#0x55
                                    600 ;	keyboards/ajazz/ak820/ak820_boot.c:8: SAFE_MOD = 0xAA;
      00348C 75 A1 AA         [24]  601 	mov	_SAFE_MOD,#0xaa
                                    602 ;	keyboards/ajazz/ak820/ak820_boot.c:9: GLOBAL_CFG |= 0x10;
      00348F 43 B1 10         [24]  603 	orl	_GLOBAL_CFG,#0x10
                                    604 ;	keyboards/ajazz/ak820/ak820_boot.c:10: while (1) { }
      003492                        605 00102$:
                                    606 ;	keyboards/ajazz/ak820/ak820_boot.c:11: }
      003492 80 FE            [24]  607 	sjmp	00102$
                                    608 ;------------------------------------------------------------
                                    609 ;Allocation info for local variables in function 'bootloader_jump'
                                    610 ;------------------------------------------------------------
                                    611 ;saved_ie      Allocated with name '_bootloader_jump_saved_ie_10000_15'
                                    612 ;marker        Allocated with name '_bootloader_jump_marker_10000_15'
                                    613 ;------------------------------------------------------------
                                    614 ;	keyboards/ajazz/ak820/ak820_boot.c:13: void bootloader_jump(void) {
                                    615 ;	-----------------------------------------
                                    616 ;	 function bootloader_jump
                                    617 ;	-----------------------------------------
      003494                        618 _bootloader_jump:
                                    619 ;	keyboards/ajazz/ak820/ak820_boot.c:16: uint8_t saved_ie = IE;
      003494 90 04 1A         [24]  620 	mov	dptr,#_bootloader_jump_saved_ie_10000_15
      003497 E5 A8            [12]  621 	mov	a,_IE
      003499 F0               [24]  622 	movx	@dptr,a
                                    623 ;	keyboards/ajazz/ak820/ak820_boot.c:20: ak820_nvm_flush();
      00349A 12 3A CB         [24]  624 	lcall	_ak820_nvm_flush
                                    625 ;	keyboards/ajazz/ak820/ak820_boot.c:21: EA = 0;
                                    626 ;	assignBit
      00349D C2 AF            [12]  627 	clr	_EA
                                    628 ;	keyboards/ajazz/ak820/ak820_boot.c:22: SAFE_MOD = 0x55;
      00349F 75 A1 55         [24]  629 	mov	_SAFE_MOD,#0x55
                                    630 ;	keyboards/ajazz/ak820/ak820_boot.c:23: SAFE_MOD = 0xAA;
      0034A2 75 A1 AA         [24]  631 	mov	_SAFE_MOD,#0xaa
                                    632 ;	keyboards/ajazz/ak820/ak820_boot.c:24: GLOBAL_CFG |= 0x08;
      0034A5 43 B1 08         [24]  633 	orl	_GLOBAL_CFG,#0x08
                                    634 ;	keyboards/ajazz/ak820/ak820_boot.c:25: ROM_ADDR_L = 0xC0;
      0034A8 75 84 C0         [24]  635 	mov	_ROM_ADDR_L,#0xc0
                                    636 ;	keyboards/ajazz/ak820/ak820_boot.c:26: ROM_ADDR_H = 0x27;
      0034AB 75 85 27         [24]  637 	mov	_ROM_ADDR_H,#0x27
                                    638 ;	keyboards/ajazz/ak820/ak820_boot.c:27: ROM_BUF_MOD = 0x80;
      0034AE 75 8F 80         [24]  639 	mov	_ROM_DATA_HH,#0x80
                                    640 ;	keyboards/ajazz/ak820/ak820_boot.c:28: ROM_DAT_BUF = 0;
      0034B1 75 8E 00         [24]  641 	mov	_ROM_DATA_HL,#0x00
                                    642 ;	keyboards/ajazz/ak820/ak820_boot.c:29: if (ROM_STATUS & 0x40) ROM_CTRL = 0xA6;
      0034B4 E5 86            [12]  643 	mov	a,_ROM_CTRL
      0034B6 30 E6 03         [24]  644 	jnb	acc.6,00102$
      0034B9 75 86 A6         [24]  645 	mov	_ROM_CTRL,#0xa6
      0034BC                        646 00102$:
                                    647 ;	keyboards/ajazz/ak820/ak820_boot.c:30: SAFE_MOD = 0x55;
      0034BC 75 A1 55         [24]  648 	mov	_SAFE_MOD,#0x55
                                    649 ;	keyboards/ajazz/ak820/ak820_boot.c:31: SAFE_MOD = 0xAA;
      0034BF 75 A1 AA         [24]  650 	mov	_SAFE_MOD,#0xaa
                                    651 ;	keyboards/ajazz/ak820/ak820_boot.c:32: GLOBAL_CFG &= (uint8_t)~0x08;
      0034C2 53 B1 F7         [24]  652 	anl	_GLOBAL_CFG,#0xf7
                                    653 ;	keyboards/ajazz/ak820/ak820_boot.c:33: SAFE_MOD = 0;
      0034C5 75 A1 00         [24]  654 	mov	_SAFE_MOD,#0x00
                                    655 ;	keyboards/ajazz/ak820/ak820_boot.c:35: if (marker[0] || marker[1] || marker[2] || marker[3]) {
      0034C8 90 27 C0         [24]  656 	mov	dptr,#0x27c0
      0034CB E4               [12]  657 	clr	a
      0034CC 93               [24]  658 	movc	a,@a+dptr
      0034CD 70 15            [24]  659 	jnz	00103$
      0034CF 90 27 C1         [24]  660 	mov	dptr,#0x27c1
      0034D2 E4               [12]  661 	clr	a
      0034D3 93               [24]  662 	movc	a,@a+dptr
      0034D4 70 0E            [24]  663 	jnz	00103$
      0034D6 90 27 C2         [24]  664 	mov	dptr,#0x27c2
      0034D9 E4               [12]  665 	clr	a
      0034DA 93               [24]  666 	movc	a,@a+dptr
      0034DB 70 07            [24]  667 	jnz	00103$
      0034DD 90 27 C3         [24]  668 	mov	dptr,#0x27c3
      0034E0 E4               [12]  669 	clr	a
      0034E1 93               [24]  670 	movc	a,@a+dptr
      0034E2 60 07            [24]  671 	jz	00104$
      0034E4                        672 00103$:
                                    673 ;	keyboards/ajazz/ak820/ak820_boot.c:36: IE = saved_ie;
      0034E4 90 04 1A         [24]  674 	mov	dptr,#_bootloader_jump_saved_ie_10000_15
      0034E7 E0               [24]  675 	movx	a,@dptr
      0034E8 F5 A8            [12]  676 	mov	_IE,a
                                    677 ;	keyboards/ajazz/ak820/ak820_boot.c:37: return;
      0034EA 22               [24]  678 	ret
      0034EB                        679 00104$:
                                    680 ;	keyboards/ajazz/ak820/ak820_boot.c:39: mcu_reset();
                                    681 ;	keyboards/ajazz/ak820/ak820_boot.c:40: }
      0034EB 02 34 87         [24]  682 	ljmp	_mcu_reset
                                    683 	.area CSEG    (CODE)
                                    684 	.area CONST   (CODE)
                                    685 	.area XINIT   (CODE)
                                    686 	.area CABS    (ABS,CODE)
