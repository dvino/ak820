                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module usb_descriptor
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _SerialNumberString
                                     12 	.globl _ProductString
                                     13 	.globl _ManufacturerString
                                     14 	.globl _LanguageString
                                     15 	.globl _ConfigurationDescriptor
                                     16 	.globl _DeviceDescriptor
                                     17 	.globl _RawReport_size
                                     18 	.globl _RawReport
                                     19 	.globl _SharedReport_size
                                     20 	.globl _SharedReport
                                     21 	.globl _KeyboardReport_size
                                     22 	.globl _KeyboardReport
                                     23 	.globl _ADC_START
                                     24 	.globl _S0_R_FIFO
                                     25 	.globl _S0_T_FIFO
                                     26 	.globl _S0_FREE
                                     27 	.globl _S0_IF_BYTE
                                     28 	.globl _S0_IF_FIRST
                                     29 	.globl _S0_IF_OV
                                     30 	.globl _S0_FST_ACT
                                     31 	.globl _CP_RL2
                                     32 	.globl _C_T2
                                     33 	.globl _TR2
                                     34 	.globl _EXEN2
                                     35 	.globl _TCLK
                                     36 	.globl _RCLK
                                     37 	.globl _EXF2
                                     38 	.globl _CAP1F
                                     39 	.globl _TF2
                                     40 	.globl _RI
                                     41 	.globl _TI
                                     42 	.globl _RB8
                                     43 	.globl _TB8
                                     44 	.globl _REN
                                     45 	.globl _SM2
                                     46 	.globl _SM1
                                     47 	.globl _SM0
                                     48 	.globl _IT0
                                     49 	.globl _IE0
                                     50 	.globl _IT1
                                     51 	.globl _IE1
                                     52 	.globl _TR0
                                     53 	.globl _TF0
                                     54 	.globl _TR1
                                     55 	.globl _TF1
                                     56 	.globl _P4_0
                                     57 	.globl _P4_1
                                     58 	.globl _P4_2
                                     59 	.globl _P4_3
                                     60 	.globl _P4_4
                                     61 	.globl _P4_5
                                     62 	.globl _P4_6
                                     63 	.globl _RXD
                                     64 	.globl _TXD
                                     65 	.globl _INT0
                                     66 	.globl _INT1
                                     67 	.globl _T0
                                     68 	.globl _T1
                                     69 	.globl _MOSI1
                                     70 	.globl _MISO1
                                     71 	.globl _SCK1
                                     72 	.globl _P3_0
                                     73 	.globl _P3_1
                                     74 	.globl _P3_2
                                     75 	.globl _P3_3
                                     76 	.globl _P3_4
                                     77 	.globl _P3_5
                                     78 	.globl _P3_6
                                     79 	.globl _P3_7
                                     80 	.globl _CAP1_
                                     81 	.globl _T2_
                                     82 	.globl _CAP2_
                                     83 	.globl _T2EX_
                                     84 	.globl _RXD1
                                     85 	.globl _TXD1
                                     86 	.globl _P2_0
                                     87 	.globl _P2_1
                                     88 	.globl _P2_2
                                     89 	.globl _P2_3
                                     90 	.globl _P2_4
                                     91 	.globl _P2_5
                                     92 	.globl _P2_6
                                     93 	.globl _P2_7
                                     94 	.globl _AIN0
                                     95 	.globl _AIN1
                                     96 	.globl _AIN2
                                     97 	.globl _AIN3
                                     98 	.globl _AIN4
                                     99 	.globl _AIN5
                                    100 	.globl _AIN6
                                    101 	.globl _AIN7
                                    102 	.globl _CAP1
                                    103 	.globl _T2
                                    104 	.globl _CAP2
                                    105 	.globl _T2EX
                                    106 	.globl _INT0_
                                    107 	.globl _SCS
                                    108 	.globl _MOSI
                                    109 	.globl _MISO
                                    110 	.globl _SCK
                                    111 	.globl _RXD1_
                                    112 	.globl _TXD1_
                                    113 	.globl _P1_0
                                    114 	.globl _P1_1
                                    115 	.globl _P1_2
                                    116 	.globl _P1_3
                                    117 	.globl _P1_4
                                    118 	.globl _P1_5
                                    119 	.globl _P1_6
                                    120 	.globl _P1_7
                                    121 	.globl _AIN8
                                    122 	.globl _AIN9
                                    123 	.globl _AIN10
                                    124 	.globl _AIN11
                                    125 	.globl _AIN12
                                    126 	.globl _AIN13
                                    127 	.globl _RXD_
                                    128 	.globl _TXD_
                                    129 	.globl _SCL0
                                    130 	.globl _SDA0
                                    131 	.globl _P0_0
                                    132 	.globl _P0_1
                                    133 	.globl _P0_2
                                    134 	.globl _P0_3
                                    135 	.globl _P0_4
                                    136 	.globl _P0_5
                                    137 	.globl _P0_6
                                    138 	.globl _P0_7
                                    139 	.globl _IE_SPI0
                                    140 	.globl _IE_USB
                                    141 	.globl _IE_ADC
                                    142 	.globl _IE_UART1
                                    143 	.globl _IE_PWM_I2C
                                    144 	.globl _IE_GPIO
                                    145 	.globl _IE_WDOG
                                    146 	.globl _PX0
                                    147 	.globl _PT0
                                    148 	.globl _PX1
                                    149 	.globl _PT1
                                    150 	.globl _PS
                                    151 	.globl _PT2
                                    152 	.globl _PL_FLAG
                                    153 	.globl _PH_FLAG
                                    154 	.globl _EX0
                                    155 	.globl _ET0
                                    156 	.globl _EX1
                                    157 	.globl _ET1
                                    158 	.globl _ES
                                    159 	.globl _ET2
                                    160 	.globl _E_DIS
                                    161 	.globl _EA
                                    162 	.globl _P
                                    163 	.globl _F1
                                    164 	.globl _OV
                                    165 	.globl _RS0
                                    166 	.globl _RS1
                                    167 	.globl _F0
                                    168 	.globl _AC
                                    169 	.globl _CY
                                    170 	.globl _I2CS_INT_ST
                                    171 	.globl _I2CX_INT
                                    172 	.globl _LED_STATUS
                                    173 	.globl _LED_DMA_H
                                    174 	.globl _LED_DMA_L
                                    175 	.globl _LED_DMA
                                    176 	.globl _LED_PWM_OE
                                    177 	.globl _LED_COMMON
                                    178 	.globl _ADC_CHAN
                                    179 	.globl _ADC_DAT_H
                                    180 	.globl _ADC_DAT_L
                                    181 	.globl _ADC_DAT
                                    182 	.globl _ADC_CTRL
                                    183 	.globl _SPI1_CK_SE
                                    184 	.globl _SPI1_CTRL
                                    185 	.globl _SPI1_DATA
                                    186 	.globl _SPI1_STAT
                                    187 	.globl _SIF1
                                    188 	.globl _SBAUD1
                                    189 	.globl _SBUF1
                                    190 	.globl _SCON1
                                    191 	.globl _SPI0_SETUP
                                    192 	.globl _SPI0_CK_SE
                                    193 	.globl _SPI0_CTRL
                                    194 	.globl _SPI0_DATA
                                    195 	.globl _SPI0_STAT
                                    196 	.globl _T2CAP1H
                                    197 	.globl _T2CAP1L
                                    198 	.globl _T2CAP1
                                    199 	.globl _TH2
                                    200 	.globl _TL2
                                    201 	.globl _T2COUNT
                                    202 	.globl _RCAP2H
                                    203 	.globl _RCAP2L
                                    204 	.globl _RCAP2
                                    205 	.globl _T2MOD
                                    206 	.globl _T2CON
                                    207 	.globl _SBUF
                                    208 	.globl _SCON
                                    209 	.globl _TH1
                                    210 	.globl _TH0
                                    211 	.globl _TL1
                                    212 	.globl _TL0
                                    213 	.globl _TMOD
                                    214 	.globl _TCON
                                    215 	.globl _XBUS_AUX
                                    216 	.globl _P7
                                    217 	.globl _P6_DIR
                                    218 	.globl _P6_OUT_PU
                                    219 	.globl _P6_IN
                                    220 	.globl _P5_DIR
                                    221 	.globl _P5_OUT_PU
                                    222 	.globl _P5_IN
                                    223 	.globl _P4_LED_KEY
                                    224 	.globl _P4_DIR_PU
                                    225 	.globl _P4_MOD_OC
                                    226 	.globl _P4
                                    227 	.globl _P3_DIR_PU
                                    228 	.globl _P3_MOD_OC
                                    229 	.globl _P3
                                    230 	.globl _P2_DIR_PU
                                    231 	.globl _P2_MOD_OC
                                    232 	.globl _P2
                                    233 	.globl _P1_DIR_PU
                                    234 	.globl _P1_MOD_OC
                                    235 	.globl _P1
                                    236 	.globl _P0_DIR_PU
                                    237 	.globl _P0_MOD_OC
                                    238 	.globl _P0
                                    239 	.globl _ROM_CTRL
                                    240 	.globl _ROM_DATA_HH
                                    241 	.globl _ROM_DATA_HL
                                    242 	.globl _ROM_DATA_HI
                                    243 	.globl _ROM_ADDR_H
                                    244 	.globl _ROM_ADDR_L
                                    245 	.globl _ROM_ADDR
                                    246 	.globl _GPIO_IE
                                    247 	.globl _IP_EX
                                    248 	.globl _IE_EX
                                    249 	.globl _IP
                                    250 	.globl _IE
                                    251 	.globl _WDOG_COUNT
                                    252 	.globl _RESET_KEEP
                                    253 	.globl _WAKE_CTRL
                                    254 	.globl _CLOCK_CFG
                                    255 	.globl _POWER_CFG
                                    256 	.globl _PCON
                                    257 	.globl _GLOBAL_CFG
                                    258 	.globl _SAFE_MOD
                                    259 	.globl _DPH
                                    260 	.globl _DPL
                                    261 	.globl _SP
                                    262 	.globl _A_INV
                                    263 	.globl _B
                                    264 	.globl _ACC
                                    265 	.globl _PSW
                                    266 ;--------------------------------------------------------
                                    267 ; special function registers
                                    268 ;--------------------------------------------------------
                                    269 	.area RSEG    (ABS,DATA)
      000000                        270 	.org 0x0000
                           0000D0   271 _PSW	=	0x00d0
                           0000E0   272 _ACC	=	0x00e0
                           0000F0   273 _B	=	0x00f0
                           0000FD   274 _A_INV	=	0x00fd
                           000081   275 _SP	=	0x0081
                           000082   276 _DPL	=	0x0082
                           000083   277 _DPH	=	0x0083
                           0000A1   278 _SAFE_MOD	=	0x00a1
                           0000B1   279 _GLOBAL_CFG	=	0x00b1
                           000087   280 _PCON	=	0x0087
                           0000BA   281 _POWER_CFG	=	0x00ba
                           0000B9   282 _CLOCK_CFG	=	0x00b9
                           0000A9   283 _WAKE_CTRL	=	0x00a9
                           0000FE   284 _RESET_KEEP	=	0x00fe
                           0000FF   285 _WDOG_COUNT	=	0x00ff
                           0000A8   286 _IE	=	0x00a8
                           0000B8   287 _IP	=	0x00b8
                           0000E8   288 _IE_EX	=	0x00e8
                           0000E9   289 _IP_EX	=	0x00e9
                           0000B2   290 _GPIO_IE	=	0x00b2
                           008584   291 _ROM_ADDR	=	0x8584
                           000084   292 _ROM_ADDR_L	=	0x0084
                           000085   293 _ROM_ADDR_H	=	0x0085
                           008F8E   294 _ROM_DATA_HI	=	0x8f8e
                           00008E   295 _ROM_DATA_HL	=	0x008e
                           00008F   296 _ROM_DATA_HH	=	0x008f
                           000086   297 _ROM_CTRL	=	0x0086
                           000080   298 _P0	=	0x0080
                           0000C4   299 _P0_MOD_OC	=	0x00c4
                           0000C5   300 _P0_DIR_PU	=	0x00c5
                           000090   301 _P1	=	0x0090
                           000092   302 _P1_MOD_OC	=	0x0092
                           000093   303 _P1_DIR_PU	=	0x0093
                           0000A0   304 _P2	=	0x00a0
                           000094   305 _P2_MOD_OC	=	0x0094
                           000095   306 _P2_DIR_PU	=	0x0095
                           0000B0   307 _P3	=	0x00b0
                           000096   308 _P3_MOD_OC	=	0x0096
                           000097   309 _P3_DIR_PU	=	0x0097
                           0000C0   310 _P4	=	0x00c0
                           0000C2   311 _P4_MOD_OC	=	0x00c2
                           0000C3   312 _P4_DIR_PU	=	0x00c3
                           0000C1   313 _P4_LED_KEY	=	0x00c1
                           0000AA   314 _P5_IN	=	0x00aa
                           0000AB   315 _P5_OUT_PU	=	0x00ab
                           0000AC   316 _P5_DIR	=	0x00ac
                           0000AD   317 _P6_IN	=	0x00ad
                           0000AE   318 _P6_OUT_PU	=	0x00ae
                           0000AF   319 _P6_DIR	=	0x00af
                           0000F1   320 _P7	=	0x00f1
                           0000A2   321 _XBUS_AUX	=	0x00a2
                           000088   322 _TCON	=	0x0088
                           000089   323 _TMOD	=	0x0089
                           00008A   324 _TL0	=	0x008a
                           00008B   325 _TL1	=	0x008b
                           00008C   326 _TH0	=	0x008c
                           00008D   327 _TH1	=	0x008d
                           000098   328 _SCON	=	0x0098
                           000099   329 _SBUF	=	0x0099
                           0000C8   330 _T2CON	=	0x00c8
                           0000C9   331 _T2MOD	=	0x00c9
                           00CBCA   332 _RCAP2	=	0xcbca
                           0000CA   333 _RCAP2L	=	0x00ca
                           0000CB   334 _RCAP2H	=	0x00cb
                           00CDCC   335 _T2COUNT	=	0xcdcc
                           0000CC   336 _TL2	=	0x00cc
                           0000CD   337 _TH2	=	0x00cd
                           00CFCE   338 _T2CAP1	=	0xcfce
                           0000CE   339 _T2CAP1L	=	0x00ce
                           0000CF   340 _T2CAP1H	=	0x00cf
                           0000F8   341 _SPI0_STAT	=	0x00f8
                           0000F9   342 _SPI0_DATA	=	0x00f9
                           0000FA   343 _SPI0_CTRL	=	0x00fa
                           0000FB   344 _SPI0_CK_SE	=	0x00fb
                           0000FC   345 _SPI0_SETUP	=	0x00fc
                           0000BC   346 _SCON1	=	0x00bc
                           0000BD   347 _SBUF1	=	0x00bd
                           0000BE   348 _SBAUD1	=	0x00be
                           0000BF   349 _SIF1	=	0x00bf
                           0000B4   350 _SPI1_STAT	=	0x00b4
                           0000B5   351 _SPI1_DATA	=	0x00b5
                           0000B6   352 _SPI1_CTRL	=	0x00b6
                           0000B7   353 _SPI1_CK_SE	=	0x00b7
                           0000F3   354 _ADC_CTRL	=	0x00f3
                           00F5F4   355 _ADC_DAT	=	0xf5f4
                           0000F4   356 _ADC_DAT_L	=	0x00f4
                           0000F5   357 _ADC_DAT_H	=	0x00f5
                           0000F6   358 _ADC_CHAN	=	0x00f6
                           0000A6   359 _LED_COMMON	=	0x00a6
                           0000A7   360 _LED_PWM_OE	=	0x00a7
                           00C7C6   361 _LED_DMA	=	0xc7c6
                           0000C6   362 _LED_DMA_L	=	0x00c6
                           0000C7   363 _LED_DMA_H	=	0x00c7
                           0000F7   364 _LED_STATUS	=	0x00f7
                           0000B3   365 _I2CX_INT	=	0x00b3
                           0000BB   366 _I2CS_INT_ST	=	0x00bb
                                    367 ;--------------------------------------------------------
                                    368 ; special function bits
                                    369 ;--------------------------------------------------------
                                    370 	.area RSEG    (ABS,DATA)
      000000                        371 	.org 0x0000
                           0000D7   372 _CY	=	0x00d7
                           0000D6   373 _AC	=	0x00d6
                           0000D5   374 _F0	=	0x00d5
                           0000D4   375 _RS1	=	0x00d4
                           0000D3   376 _RS0	=	0x00d3
                           0000D2   377 _OV	=	0x00d2
                           0000D1   378 _F1	=	0x00d1
                           0000D0   379 _P	=	0x00d0
                           0000AF   380 _EA	=	0x00af
                           0000AE   381 _E_DIS	=	0x00ae
                           0000AD   382 _ET2	=	0x00ad
                           0000AC   383 _ES	=	0x00ac
                           0000AB   384 _ET1	=	0x00ab
                           0000AA   385 _EX1	=	0x00aa
                           0000A9   386 _ET0	=	0x00a9
                           0000A8   387 _EX0	=	0x00a8
                           0000BF   388 _PH_FLAG	=	0x00bf
                           0000BE   389 _PL_FLAG	=	0x00be
                           0000BD   390 _PT2	=	0x00bd
                           0000BC   391 _PS	=	0x00bc
                           0000BB   392 _PT1	=	0x00bb
                           0000BA   393 _PX1	=	0x00ba
                           0000B9   394 _PT0	=	0x00b9
                           0000B8   395 _PX0	=	0x00b8
                           0000EF   396 _IE_WDOG	=	0x00ef
                           0000EE   397 _IE_GPIO	=	0x00ee
                           0000ED   398 _IE_PWM_I2C	=	0x00ed
                           0000EC   399 _IE_UART1	=	0x00ec
                           0000EB   400 _IE_ADC	=	0x00eb
                           0000E9   401 _IE_USB	=	0x00e9
                           0000E8   402 _IE_SPI0	=	0x00e8
                           000087   403 _P0_7	=	0x0087
                           000086   404 _P0_6	=	0x0086
                           000085   405 _P0_5	=	0x0085
                           000084   406 _P0_4	=	0x0084
                           000083   407 _P0_3	=	0x0083
                           000082   408 _P0_2	=	0x0082
                           000081   409 _P0_1	=	0x0081
                           000080   410 _P0_0	=	0x0080
                           000081   411 _SDA0	=	0x0081
                           000080   412 _SCL0	=	0x0080
                           000083   413 _TXD_	=	0x0083
                           000082   414 _RXD_	=	0x0082
                           000085   415 _AIN13	=	0x0085
                           000084   416 _AIN12	=	0x0084
                           000083   417 _AIN11	=	0x0083
                           000082   418 _AIN10	=	0x0082
                           000081   419 _AIN9	=	0x0081
                           000080   420 _AIN8	=	0x0080
                           000097   421 _P1_7	=	0x0097
                           000096   422 _P1_6	=	0x0096
                           000095   423 _P1_5	=	0x0095
                           000094   424 _P1_4	=	0x0094
                           000093   425 _P1_3	=	0x0093
                           000092   426 _P1_2	=	0x0092
                           000091   427 _P1_1	=	0x0091
                           000090   428 _P1_0	=	0x0090
                           000097   429 _TXD1_	=	0x0097
                           000096   430 _RXD1_	=	0x0096
                           000097   431 _SCK	=	0x0097
                           000096   432 _MISO	=	0x0096
                           000095   433 _MOSI	=	0x0095
                           000094   434 _SCS	=	0x0094
                           000092   435 _INT0_	=	0x0092
                           000091   436 _T2EX	=	0x0091
                           000091   437 _CAP2	=	0x0091
                           000090   438 _T2	=	0x0090
                           000090   439 _CAP1	=	0x0090
                           000097   440 _AIN7	=	0x0097
                           000096   441 _AIN6	=	0x0096
                           000095   442 _AIN5	=	0x0095
                           000094   443 _AIN4	=	0x0094
                           000093   444 _AIN3	=	0x0093
                           000092   445 _AIN2	=	0x0092
                           000091   446 _AIN1	=	0x0091
                           000090   447 _AIN0	=	0x0090
                           0000A7   448 _P2_7	=	0x00a7
                           0000A6   449 _P2_6	=	0x00a6
                           0000A5   450 _P2_5	=	0x00a5
                           0000A4   451 _P2_4	=	0x00a4
                           0000A3   452 _P2_3	=	0x00a3
                           0000A2   453 _P2_2	=	0x00a2
                           0000A1   454 _P2_1	=	0x00a1
                           0000A0   455 _P2_0	=	0x00a0
                           0000A7   456 _TXD1	=	0x00a7
                           0000A6   457 _RXD1	=	0x00a6
                           0000A5   458 _T2EX_	=	0x00a5
                           0000A5   459 _CAP2_	=	0x00a5
                           0000A4   460 _T2_	=	0x00a4
                           0000A4   461 _CAP1_	=	0x00a4
                           0000B7   462 _P3_7	=	0x00b7
                           0000B6   463 _P3_6	=	0x00b6
                           0000B5   464 _P3_5	=	0x00b5
                           0000B4   465 _P3_4	=	0x00b4
                           0000B3   466 _P3_3	=	0x00b3
                           0000B2   467 _P3_2	=	0x00b2
                           0000B1   468 _P3_1	=	0x00b1
                           0000B0   469 _P3_0	=	0x00b0
                           0000B7   470 _SCK1	=	0x00b7
                           0000B6   471 _MISO1	=	0x00b6
                           0000B5   472 _MOSI1	=	0x00b5
                           0000B5   473 _T1	=	0x00b5
                           0000B4   474 _T0	=	0x00b4
                           0000B3   475 _INT1	=	0x00b3
                           0000B2   476 _INT0	=	0x00b2
                           0000B1   477 _TXD	=	0x00b1
                           0000B0   478 _RXD	=	0x00b0
                           0000C6   479 _P4_6	=	0x00c6
                           0000C5   480 _P4_5	=	0x00c5
                           0000C4   481 _P4_4	=	0x00c4
                           0000C3   482 _P4_3	=	0x00c3
                           0000C2   483 _P4_2	=	0x00c2
                           0000C1   484 _P4_1	=	0x00c1
                           0000C0   485 _P4_0	=	0x00c0
                           00008F   486 _TF1	=	0x008f
                           00008E   487 _TR1	=	0x008e
                           00008D   488 _TF0	=	0x008d
                           00008C   489 _TR0	=	0x008c
                           00008B   490 _IE1	=	0x008b
                           00008A   491 _IT1	=	0x008a
                           000089   492 _IE0	=	0x0089
                           000088   493 _IT0	=	0x0088
                           00009F   494 _SM0	=	0x009f
                           00009E   495 _SM1	=	0x009e
                           00009D   496 _SM2	=	0x009d
                           00009C   497 _REN	=	0x009c
                           00009B   498 _TB8	=	0x009b
                           00009A   499 _RB8	=	0x009a
                           000099   500 _TI	=	0x0099
                           000098   501 _RI	=	0x0098
                           0000CF   502 _TF2	=	0x00cf
                           0000CF   503 _CAP1F	=	0x00cf
                           0000CE   504 _EXF2	=	0x00ce
                           0000CD   505 _RCLK	=	0x00cd
                           0000CC   506 _TCLK	=	0x00cc
                           0000CB   507 _EXEN2	=	0x00cb
                           0000CA   508 _TR2	=	0x00ca
                           0000C9   509 _C_T2	=	0x00c9
                           0000C8   510 _CP_RL2	=	0x00c8
                           0000FF   511 _S0_FST_ACT	=	0x00ff
                           0000FE   512 _S0_IF_OV	=	0x00fe
                           0000FD   513 _S0_IF_FIRST	=	0x00fd
                           0000FC   514 _S0_IF_BYTE	=	0x00fc
                           0000FB   515 _S0_FREE	=	0x00fb
                           0000FA   516 _S0_T_FIFO	=	0x00fa
                           0000F8   517 _S0_R_FIFO	=	0x00f8
                           0000F7   518 _ADC_START	=	0x00f7
                                    519 ;--------------------------------------------------------
                                    520 ; overlayable register banks
                                    521 ;--------------------------------------------------------
                                    522 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        523 	.ds 8
                                    524 ;--------------------------------------------------------
                                    525 ; internal ram data
                                    526 ;--------------------------------------------------------
                                    527 	.area DSEG    (DATA)
                                    528 ;--------------------------------------------------------
                                    529 ; overlayable items in internal ram
                                    530 ;--------------------------------------------------------
                                    531 ;--------------------------------------------------------
                                    532 ; indirectly addressable internal ram data
                                    533 ;--------------------------------------------------------
                                    534 	.area ISEG    (DATA)
                                    535 ;--------------------------------------------------------
                                    536 ; absolute internal ram data
                                    537 ;--------------------------------------------------------
                                    538 	.area IABS    (ABS,DATA)
                                    539 	.area IABS    (ABS,DATA)
                                    540 ;--------------------------------------------------------
                                    541 ; bit data
                                    542 ;--------------------------------------------------------
                                    543 	.area BSEG    (BIT)
                                    544 ;--------------------------------------------------------
                                    545 ; paged external ram data
                                    546 ;--------------------------------------------------------
                                    547 	.area PSEG    (PAG,XDATA)
                                    548 ;--------------------------------------------------------
                                    549 ; uninitialized external ram data
                                    550 ;--------------------------------------------------------
                                    551 	.area XSEG    (XDATA)
                                    552 ;--------------------------------------------------------
                                    553 ; absolute external ram data
                                    554 ;--------------------------------------------------------
                                    555 	.area XABS    (ABS,XDATA)
                                    556 ;--------------------------------------------------------
                                    557 ; initialized external ram data
                                    558 ;--------------------------------------------------------
                                    559 	.area XISEG   (XDATA)
                                    560 	.area HOME    (CODE)
                                    561 	.area GSINIT0 (CODE)
                                    562 	.area GSINIT1 (CODE)
                                    563 	.area GSINIT2 (CODE)
                                    564 	.area GSINIT3 (CODE)
                                    565 	.area GSINIT4 (CODE)
                                    566 	.area GSINIT5 (CODE)
                                    567 	.area GSINIT  (CODE)
                                    568 	.area GSFINAL (CODE)
                                    569 	.area CSEG    (CODE)
                                    570 ;--------------------------------------------------------
                                    571 ; global & static initialisations
                                    572 ;--------------------------------------------------------
                                    573 	.area HOME    (CODE)
                                    574 	.area GSINIT  (CODE)
                                    575 	.area GSFINAL (CODE)
                                    576 	.area GSINIT  (CODE)
                                    577 ;--------------------------------------------------------
                                    578 ; Home
                                    579 ;--------------------------------------------------------
                                    580 	.area HOME    (CODE)
                                    581 	.area HOME    (CODE)
                                    582 ;--------------------------------------------------------
                                    583 ; code
                                    584 ;--------------------------------------------------------
                                    585 	.area CSEG    (CODE)
                                    586 ;------------------------------------------------------------
                                    587 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    588 ;------------------------------------------------------------
                                    589 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_49'
                                    590 ;------------------------------------------------------------
                                    591 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    592 ;	-----------------------------------------
                           000007   593 	ar7 = 0x07
                           000006   594 	ar6 = 0x06
                           000005   595 	ar5 = 0x05
                           000004   596 	ar4 = 0x04
                           000003   597 	ar3 = 0x03
                           000002   598 	ar2 = 0x02
                           000001   599 	ar1 = 0x01
                           000000   600 	ar0 = 0x00
                                    601 	.area CSEG    (CODE)
                                    602 	.area CONST   (CODE)
                                    603 	.area CONST   (CODE)
      00BBD0                        604 __str_0:
      00BBD0 41 00                  605 	.byte 65,0
      00BBD2 00 00                  606 	.byte 0,0
                                    607 	.area CSEG    (CODE)
                                    608 	.area CONST   (CODE)
      00BBD4                        609 _KeyboardReport:
      00BBD4 05                     610 	.db #0x05	; 5
      00BBD5 01                     611 	.db #0x01	; 1
      00BBD6 09                     612 	.db #0x09	; 9
      00BBD7 06                     613 	.db #0x06	; 6
      00BBD8 A1                     614 	.db #0xa1	; 161
      00BBD9 01                     615 	.db #0x01	; 1
      00BBDA 05                     616 	.db #0x05	; 5
      00BBDB 07                     617 	.db #0x07	; 7
      00BBDC 19                     618 	.db #0x19	; 25
      00BBDD E0                     619 	.db #0xe0	; 224
      00BBDE 29                     620 	.db #0x29	; 41
      00BBDF E7                     621 	.db #0xe7	; 231
      00BBE0 15                     622 	.db #0x15	; 21
      00BBE1 00                     623 	.db #0x00	; 0
      00BBE2 25                     624 	.db #0x25	; 37
      00BBE3 01                     625 	.db #0x01	; 1
      00BBE4 95                     626 	.db #0x95	; 149
      00BBE5 08                     627 	.db #0x08	; 8
      00BBE6 75                     628 	.db #0x75	; 117	'u'
      00BBE7 01                     629 	.db #0x01	; 1
      00BBE8 81                     630 	.db #0x81	; 129
      00BBE9 02                     631 	.db #0x02	; 2
      00BBEA 95                     632 	.db #0x95	; 149
      00BBEB 01                     633 	.db #0x01	; 1
      00BBEC 75                     634 	.db #0x75	; 117	'u'
      00BBED 08                     635 	.db #0x08	; 8
      00BBEE 81                     636 	.db #0x81	; 129
      00BBEF 01                     637 	.db #0x01	; 1
      00BBF0 05                     638 	.db #0x05	; 5
      00BBF1 07                     639 	.db #0x07	; 7
      00BBF2 19                     640 	.db #0x19	; 25
      00BBF3 00                     641 	.db #0x00	; 0
      00BBF4 29                     642 	.db #0x29	; 41
      00BBF5 FF                     643 	.db #0xff	; 255
      00BBF6 15                     644 	.db #0x15	; 21
      00BBF7 00                     645 	.db #0x00	; 0
      00BBF8 26                     646 	.db #0x26	; 38
      00BBF9 FF                     647 	.db #0xff	; 255
      00BBFA 00                     648 	.db #0x00	; 0
      00BBFB 95                     649 	.db #0x95	; 149
      00BBFC 06                     650 	.db #0x06	; 6
      00BBFD 75                     651 	.db #0x75	; 117	'u'
      00BBFE 08                     652 	.db #0x08	; 8
      00BBFF 81                     653 	.db #0x81	; 129
      00BC00 00                     654 	.db #0x00	; 0
      00BC01 05                     655 	.db #0x05	; 5
      00BC02 08                     656 	.db #0x08	; 8
      00BC03 19                     657 	.db #0x19	; 25
      00BC04 01                     658 	.db #0x01	; 1
      00BC05 29                     659 	.db #0x29	; 41
      00BC06 05                     660 	.db #0x05	; 5
      00BC07 15                     661 	.db #0x15	; 21
      00BC08 00                     662 	.db #0x00	; 0
      00BC09 25                     663 	.db #0x25	; 37
      00BC0A 01                     664 	.db #0x01	; 1
      00BC0B 95                     665 	.db #0x95	; 149
      00BC0C 05                     666 	.db #0x05	; 5
      00BC0D 75                     667 	.db #0x75	; 117	'u'
      00BC0E 01                     668 	.db #0x01	; 1
      00BC0F 91                     669 	.db #0x91	; 145
      00BC10 02                     670 	.db #0x02	; 2
      00BC11 95                     671 	.db #0x95	; 149
      00BC12 01                     672 	.db #0x01	; 1
      00BC13 75                     673 	.db #0x75	; 117	'u'
      00BC14 03                     674 	.db #0x03	; 3
      00BC15 91                     675 	.db #0x91	; 145
      00BC16 01                     676 	.db #0x01	; 1
      00BC17 C0                     677 	.db #0xc0	; 192
                                    678 	.area CSEG    (CODE)
                                    679 	.area CONST   (CODE)
      00BC18                        680 _KeyboardReport_size:
      00BC18 44                     681 	.db #0x44	; 68	'D'
                                    682 	.area CSEG    (CODE)
                                    683 	.area CONST   (CODE)
      00BC19                        684 _SharedReport:
      00BC19 05                     685 	.db #0x05	; 5
      00BC1A 01                     686 	.db #0x01	; 1
      00BC1B 09                     687 	.db #0x09	; 9
      00BC1C 80                     688 	.db #0x80	; 128
      00BC1D A1                     689 	.db #0xa1	; 161
      00BC1E 01                     690 	.db #0x01	; 1
      00BC1F 85                     691 	.db #0x85	; 133
      00BC20 03                     692 	.db #0x03	; 3
      00BC21 19                     693 	.db #0x19	; 25
      00BC22 01                     694 	.db #0x01	; 1
      00BC23 2A                     695 	.db #0x2a	; 42
      00BC24 B7                     696 	.db #0xb7	; 183
      00BC25 00                     697 	.db #0x00	; 0
      00BC26 15                     698 	.db #0x15	; 21
      00BC27 01                     699 	.db #0x01	; 1
      00BC28 26                     700 	.db #0x26	; 38
      00BC29 B7                     701 	.db #0xb7	; 183
      00BC2A 00                     702 	.db #0x00	; 0
      00BC2B 95                     703 	.db #0x95	; 149
      00BC2C 01                     704 	.db #0x01	; 1
      00BC2D 75                     705 	.db #0x75	; 117	'u'
      00BC2E 10                     706 	.db #0x10	; 16
      00BC2F 81                     707 	.db #0x81	; 129
      00BC30 00                     708 	.db #0x00	; 0
      00BC31 C0                     709 	.db #0xc0	; 192
      00BC32 05                     710 	.db #0x05	; 5
      00BC33 0C                     711 	.db #0x0c	; 12
      00BC34 09                     712 	.db #0x09	; 9
      00BC35 01                     713 	.db #0x01	; 1
      00BC36 A1                     714 	.db #0xa1	; 161
      00BC37 01                     715 	.db #0x01	; 1
      00BC38 85                     716 	.db #0x85	; 133
      00BC39 04                     717 	.db #0x04	; 4
      00BC3A 19                     718 	.db #0x19	; 25
      00BC3B 01                     719 	.db #0x01	; 1
      00BC3C 2A                     720 	.db #0x2a	; 42
      00BC3D A0                     721 	.db #0xa0	; 160
      00BC3E 02                     722 	.db #0x02	; 2
      00BC3F 15                     723 	.db #0x15	; 21
      00BC40 01                     724 	.db #0x01	; 1
      00BC41 26                     725 	.db #0x26	; 38
      00BC42 A0                     726 	.db #0xa0	; 160
      00BC43 02                     727 	.db #0x02	; 2
      00BC44 95                     728 	.db #0x95	; 149
      00BC45 01                     729 	.db #0x01	; 1
      00BC46 75                     730 	.db #0x75	; 117	'u'
      00BC47 10                     731 	.db #0x10	; 16
      00BC48 81                     732 	.db #0x81	; 129
      00BC49 00                     733 	.db #0x00	; 0
      00BC4A C0                     734 	.db #0xc0	; 192
      00BC4B 05                     735 	.db #0x05	; 5
      00BC4C 01                     736 	.db #0x01	; 1
      00BC4D 09                     737 	.db #0x09	; 9
      00BC4E 06                     738 	.db #0x06	; 6
      00BC4F A1                     739 	.db #0xa1	; 161
      00BC50 01                     740 	.db #0x01	; 1
      00BC51 85                     741 	.db #0x85	; 133
      00BC52 06                     742 	.db #0x06	; 6
      00BC53 05                     743 	.db #0x05	; 5
      00BC54 07                     744 	.db #0x07	; 7
      00BC55 19                     745 	.db #0x19	; 25
      00BC56 E0                     746 	.db #0xe0	; 224
      00BC57 29                     747 	.db #0x29	; 41
      00BC58 E7                     748 	.db #0xe7	; 231
      00BC59 15                     749 	.db #0x15	; 21
      00BC5A 00                     750 	.db #0x00	; 0
      00BC5B 25                     751 	.db #0x25	; 37
      00BC5C 01                     752 	.db #0x01	; 1
      00BC5D 95                     753 	.db #0x95	; 149
      00BC5E 08                     754 	.db #0x08	; 8
      00BC5F 75                     755 	.db #0x75	; 117	'u'
      00BC60 01                     756 	.db #0x01	; 1
      00BC61 81                     757 	.db #0x81	; 129
      00BC62 02                     758 	.db #0x02	; 2
      00BC63 05                     759 	.db #0x05	; 5
      00BC64 07                     760 	.db #0x07	; 7
      00BC65 19                     761 	.db #0x19	; 25
      00BC66 00                     762 	.db #0x00	; 0
      00BC67 29                     763 	.db #0x29	; 41
      00BC68 EF                     764 	.db #0xef	; 239
      00BC69 15                     765 	.db #0x15	; 21
      00BC6A 00                     766 	.db #0x00	; 0
      00BC6B 25                     767 	.db #0x25	; 37
      00BC6C 01                     768 	.db #0x01	; 1
      00BC6D 95                     769 	.db #0x95	; 149
      00BC6E F0                     770 	.db #0xf0	; 240
      00BC6F 75                     771 	.db #0x75	; 117	'u'
      00BC70 01                     772 	.db #0x01	; 1
      00BC71 81                     773 	.db #0x81	; 129
      00BC72 02                     774 	.db #0x02	; 2
      00BC73 05                     775 	.db #0x05	; 5
      00BC74 08                     776 	.db #0x08	; 8
      00BC75 19                     777 	.db #0x19	; 25
      00BC76 01                     778 	.db #0x01	; 1
      00BC77 29                     779 	.db #0x29	; 41
      00BC78 05                     780 	.db #0x05	; 5
      00BC79 95                     781 	.db #0x95	; 149
      00BC7A 05                     782 	.db #0x05	; 5
      00BC7B 75                     783 	.db #0x75	; 117	'u'
      00BC7C 01                     784 	.db #0x01	; 1
      00BC7D 91                     785 	.db #0x91	; 145
      00BC7E 02                     786 	.db #0x02	; 2
      00BC7F 95                     787 	.db #0x95	; 149
      00BC80 01                     788 	.db #0x01	; 1
      00BC81 75                     789 	.db #0x75	; 117	'u'
      00BC82 03                     790 	.db #0x03	; 3
      00BC83 91                     791 	.db #0x91	; 145
      00BC84 01                     792 	.db #0x01	; 1
      00BC85 C0                     793 	.db #0xc0	; 192
                                    794 	.area CSEG    (CODE)
                                    795 	.area CONST   (CODE)
      00BC86                        796 _SharedReport_size:
      00BC86 6D                     797 	.db #0x6d	; 109	'm'
                                    798 	.area CSEG    (CODE)
                                    799 	.area CONST   (CODE)
      00BC87                        800 _RawReport:
      00BC87 06                     801 	.db #0x06	; 6
      00BC88 60                     802 	.db #0x60	; 96
      00BC89 FF                     803 	.db #0xff	; 255
      00BC8A 09                     804 	.db #0x09	; 9
      00BC8B 61                     805 	.db #0x61	; 97	'a'
      00BC8C A1                     806 	.db #0xa1	; 161
      00BC8D 01                     807 	.db #0x01	; 1
      00BC8E 09                     808 	.db #0x09	; 9
      00BC8F 62                     809 	.db #0x62	; 98	'b'
      00BC90 15                     810 	.db #0x15	; 21
      00BC91 00                     811 	.db #0x00	; 0
      00BC92 26                     812 	.db #0x26	; 38
      00BC93 FF                     813 	.db #0xff	; 255
      00BC94 00                     814 	.db #0x00	; 0
      00BC95 95                     815 	.db #0x95	; 149
      00BC96 20                     816 	.db #0x20	; 32
      00BC97 75                     817 	.db #0x75	; 117	'u'
      00BC98 08                     818 	.db #0x08	; 8
      00BC99 81                     819 	.db #0x81	; 129
      00BC9A 02                     820 	.db #0x02	; 2
      00BC9B 09                     821 	.db #0x09	; 9
      00BC9C 63                     822 	.db #0x63	; 99	'c'
      00BC9D 15                     823 	.db #0x15	; 21
      00BC9E 00                     824 	.db #0x00	; 0
      00BC9F 26                     825 	.db #0x26	; 38
      00BCA0 FF                     826 	.db #0xff	; 255
      00BCA1 00                     827 	.db #0x00	; 0
      00BCA2 95                     828 	.db #0x95	; 149
      00BCA3 20                     829 	.db #0x20	; 32
      00BCA4 75                     830 	.db #0x75	; 117	'u'
      00BCA5 08                     831 	.db #0x08	; 8
      00BCA6 91                     832 	.db #0x91	; 145
      00BCA7 02                     833 	.db #0x02	; 2
      00BCA8 09                     834 	.db #0x09	; 9
      00BCA9 64                     835 	.db #0x64	; 100	'd'
      00BCAA 95                     836 	.db #0x95	; 149
      00BCAB 08                     837 	.db #0x08	; 8
      00BCAC B1                     838 	.db #0xb1	; 177
      00BCAD 02                     839 	.db #0x02	; 2
      00BCAE C0                     840 	.db #0xc0	; 192
                                    841 	.area CSEG    (CODE)
                                    842 	.area CONST   (CODE)
      00BCAF                        843 _RawReport_size:
      00BCAF 28                     844 	.db #0x28	; 40
                                    845 	.area CSEG    (CODE)
                                    846 	.area CONST   (CODE)
      00BCB0                        847 _DeviceDescriptor:
      00BCB0 12                     848 	.db #0x12	; 18
      00BCB1 01                     849 	.db #0x01	; 1
      00BCB2 00 02                  850 	.byte #0x00, #0x02	; 512
      00BCB4 00                     851 	.db #0x00	; 0
      00BCB5 00                     852 	.db #0x00	; 0
      00BCB6 00                     853 	.db #0x00	; 0
      00BCB7 40                     854 	.db #0x40	; 64
      00BCB8 0F 32                  855 	.byte #0x0f, #0x32	; 12815
      00BCBA 5B 50                  856 	.byte #0x5b, #0x50	; 20571
      00BCBC 00 01                  857 	.byte #0x00, #0x01	; 256
      00BCBE 01                     858 	.db #0x01	; 1
      00BCBF 02                     859 	.db #0x02	; 2
      00BCC0 03                     860 	.db #0x03	; 3
      00BCC1 01                     861 	.db #0x01	; 1
                                    862 	.area CSEG    (CODE)
                                    863 	.area CONST   (CODE)
      00BCC2                        864 _ConfigurationDescriptor:
      00BCC2 09                     865 	.db #0x09	; 9
      00BCC3 02                     866 	.db #0x02	; 2
      00BCC4 54 00                  867 	.byte #0x54, #0x00	; 84
      00BCC6 03                     868 	.db #0x03	; 3
      00BCC7 01                     869 	.db #0x01	; 1
      00BCC8 00                     870 	.db #0x00	; 0
      00BCC9 A0                     871 	.db #0xa0	; 160
      00BCCA FA                     872 	.db #0xfa	; 250
      00BCCB 09                     873 	.db #0x09	; 9
      00BCCC 04                     874 	.db #0x04	; 4
      00BCCD 00                     875 	.db #0x00	; 0
      00BCCE 00                     876 	.db #0x00	; 0
      00BCCF 01                     877 	.db #0x01	; 1
      00BCD0 03                     878 	.db #0x03	; 3
      00BCD1 01                     879 	.db #0x01	; 1
      00BCD2 01                     880 	.db #0x01	; 1
      00BCD3 00                     881 	.db #0x00	; 0
      00BCD4 09                     882 	.db #0x09	; 9
      00BCD5 21                     883 	.db #0x21	; 33
      00BCD6 11 01                  884 	.byte #0x11, #0x01	; 273
      00BCD8 00                     885 	.db #0x00	; 0
      00BCD9 01                     886 	.db #0x01	; 1
      00BCDA 22                     887 	.db #0x22	; 34
      00BCDB 44 00                  888 	.byte #0x44, #0x00	; 68
      00BCDD 07                     889 	.db #0x07	; 7
      00BCDE 05                     890 	.db #0x05	; 5
      00BCDF 81                     891 	.db #0x81	; 129
      00BCE0 03                     892 	.db #0x03	; 3
      00BCE1 08 00                  893 	.byte #0x08, #0x00	; 8
      00BCE3 01                     894 	.db #0x01	; 1
      00BCE4 09                     895 	.db #0x09	; 9
      00BCE5 04                     896 	.db #0x04	; 4
      00BCE6 01                     897 	.db #0x01	; 1
      00BCE7 00                     898 	.db #0x00	; 0
      00BCE8 01                     899 	.db #0x01	; 1
      00BCE9 03                     900 	.db #0x03	; 3
      00BCEA 00                     901 	.db #0x00	; 0
      00BCEB 00                     902 	.db #0x00	; 0
      00BCEC 00                     903 	.db #0x00	; 0
      00BCED 09                     904 	.db #0x09	; 9
      00BCEE 21                     905 	.db #0x21	; 33
      00BCEF 11 01                  906 	.byte #0x11, #0x01	; 273
      00BCF1 00                     907 	.db #0x00	; 0
      00BCF2 01                     908 	.db #0x01	; 1
      00BCF3 22                     909 	.db #0x22	; 34
      00BCF4 28 00                  910 	.byte #0x28, #0x00	; 40
      00BCF6 07                     911 	.db #0x07	; 7
      00BCF7 05                     912 	.db #0x05	; 5
      00BCF8 83                     913 	.db #0x83	; 131
      00BCF9 03                     914 	.db #0x03	; 3
      00BCFA 20 00                  915 	.byte #0x20, #0x00	; 32
      00BCFC 01                     916 	.db #0x01	; 1
      00BCFD 09                     917 	.db #0x09	; 9
      00BCFE 04                     918 	.db #0x04	; 4
      00BCFF 02                     919 	.db #0x02	; 2
      00BD00 00                     920 	.db #0x00	; 0
      00BD01 01                     921 	.db #0x01	; 1
      00BD02 03                     922 	.db #0x03	; 3
      00BD03 00                     923 	.db #0x00	; 0
      00BD04 00                     924 	.db #0x00	; 0
      00BD05 00                     925 	.db #0x00	; 0
      00BD06 09                     926 	.db #0x09	; 9
      00BD07 21                     927 	.db #0x21	; 33
      00BD08 11 01                  928 	.byte #0x11, #0x01	; 273
      00BD0A 00                     929 	.db #0x00	; 0
      00BD0B 01                     930 	.db #0x01	; 1
      00BD0C 22                     931 	.db #0x22	; 34
      00BD0D 6D 00                  932 	.byte #0x6d, #0x00	; 109
      00BD0F 07                     933 	.db #0x07	; 7
      00BD10 05                     934 	.db #0x05	; 5
      00BD11 82                     935 	.db #0x82	; 130
      00BD12 03                     936 	.db #0x03	; 3
      00BD13 20 00                  937 	.byte #0x20, #0x00	; 32
      00BD15 01                     938 	.db #0x01	; 1
                                    939 	.area CSEG    (CODE)
                                    940 	.area CONST   (CODE)
      00BD16                        941 _LanguageString:
      00BD16 04                     942 	.db #0x04	; 4
      00BD17 03                     943 	.db #0x03	; 3
      00BD18 09 04                  944 	.byte #0x09, #0x04	; 1033
                                    945 	.area CSEG    (CODE)
                                    946 	.area CONST   (CODE)
      00BD1A                        947 _ManufacturerString:
      00BD1A 0C                     948 	.db #0x0c	; 12
      00BD1B 03                     949 	.db #0x03	; 3
      00BD1C 41 00                  950 	.byte 65,0
      00BD1E 4A 00                  951 	.byte 74,0
      00BD20 41 00                  952 	.byte 65,0
      00BD22 5A 00                  953 	.byte 90,0
      00BD24 5A 00                  954 	.byte 90,0
      00BD26 00 00                  955 	.byte 0,0
                                    956 	.area CSEG    (CODE)
                                    957 	.area CONST   (CODE)
      00BD28                        958 _ProductString:
      00BD28 36                     959 	.db #0x36	; 54	'6'
      00BD29 03                     960 	.db #0x03	; 3
      00BD2A 41 00                  961 	.byte 65,0
      00BD2C 4B 00                  962 	.byte 75,0
      00BD2E 38 00                  963 	.byte 56,0
      00BD30 32 00                  964 	.byte 50,0
      00BD32 30 00                  965 	.byte 48,0
      00BD34 20 00                  966 	.byte 32,0
      00BD36 77 00                  967 	.byte 119,0
      00BD38 69 00                  968 	.byte 105,0
      00BD3A 72 00                  969 	.byte 114,0
      00BD3C 65 00                  970 	.byte 101,0
      00BD3E 64 00                  971 	.byte 100,0
      00BD40 20 00                  972 	.byte 32,0
      00BD42 52 00                  973 	.byte 82,0
      00BD44 47 00                  974 	.byte 71,0
      00BD46 42 00                  975 	.byte 66,0
      00BD48 20 00                  976 	.byte 32,0
      00BD4A 28 00                  977 	.byte 40,0
      00BD4C 56 00                  978 	.byte 86,0
      00BD4E 53 00                  979 	.byte 83,0
      00BD50 31 00                  980 	.byte 49,0
      00BD52 31 00                  981 	.byte 49,0
      00BD54 4B 00                  982 	.byte 75,0
      00BD56 32 00                  983 	.byte 50,0
      00BD58 38 00                  984 	.byte 56,0
      00BD5A 41 00                  985 	.byte 65,0
      00BD5C 29 00                  986 	.byte 41,0
      00BD5E 00 00                  987 	.byte 0,0
                                    988 	.area CSEG    (CODE)
                                    989 	.area CONST   (CODE)
      00BD60                        990 _SerialNumberString:
      00BD60 1C                     991 	.db #0x1c	; 28
      00BD61 03                     992 	.db #0x03	; 3
      00BD62 76 00                  993 	.byte 118,0
      00BD64 69 00                  994 	.byte 105,0
      00BD66 61 00                  995 	.byte 97,0
      00BD68 6C 00                  996 	.byte 108,0
      00BD6A 3A 00                  997 	.byte 58,0
      00BD6C 66 00                  998 	.byte 102,0
      00BD6E 36 00                  999 	.byte 54,0
      00BD70 34 00                 1000 	.byte 52,0
      00BD72 63 00                 1001 	.byte 99,0
      00BD74 32 00                 1002 	.byte 50,0
      00BD76 62 00                 1003 	.byte 98,0
      00BD78 33 00                 1004 	.byte 51,0
      00BD7A 63 00                 1005 	.byte 99,0
      00BD7C 00 00                 1006 	.byte 0,0
                                   1007 	.area CSEG    (CODE)
                                   1008 	.area XINIT   (CODE)
                                   1009 	.area CABS    (ABS,CODE)
