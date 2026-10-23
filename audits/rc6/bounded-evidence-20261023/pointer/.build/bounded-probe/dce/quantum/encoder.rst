                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module encoder
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _encoder_wait_pullup_charge
                                     12 	.globl _tap_code_delay
                                     13 	.globl _action_exec
                                     14 	.globl _is_keyboard_master
                                     15 	.globl _timer_read
                                     16 	.globl _mDelayuS
                                     17 	.globl _readPin
                                     18 	.globl _pinModeInputHighQMK
                                     19 	.globl _ADC_START
                                     20 	.globl _S0_R_FIFO
                                     21 	.globl _S0_T_FIFO
                                     22 	.globl _S0_FREE
                                     23 	.globl _S0_IF_BYTE
                                     24 	.globl _S0_IF_FIRST
                                     25 	.globl _S0_IF_OV
                                     26 	.globl _S0_FST_ACT
                                     27 	.globl _CP_RL2
                                     28 	.globl _C_T2
                                     29 	.globl _TR2
                                     30 	.globl _EXEN2
                                     31 	.globl _TCLK
                                     32 	.globl _RCLK
                                     33 	.globl _EXF2
                                     34 	.globl _CAP1F
                                     35 	.globl _TF2
                                     36 	.globl _RI
                                     37 	.globl _TI
                                     38 	.globl _RB8
                                     39 	.globl _TB8
                                     40 	.globl _REN
                                     41 	.globl _SM2
                                     42 	.globl _SM1
                                     43 	.globl _SM0
                                     44 	.globl _IT0
                                     45 	.globl _IE0
                                     46 	.globl _IT1
                                     47 	.globl _IE1
                                     48 	.globl _TR0
                                     49 	.globl _TF0
                                     50 	.globl _TR1
                                     51 	.globl _TF1
                                     52 	.globl _P4_0
                                     53 	.globl _P4_1
                                     54 	.globl _P4_2
                                     55 	.globl _P4_3
                                     56 	.globl _P4_4
                                     57 	.globl _P4_5
                                     58 	.globl _P4_6
                                     59 	.globl _RXD
                                     60 	.globl _TXD
                                     61 	.globl _INT0
                                     62 	.globl _INT1
                                     63 	.globl _T0
                                     64 	.globl _T1
                                     65 	.globl _MOSI1
                                     66 	.globl _MISO1
                                     67 	.globl _SCK1
                                     68 	.globl _P3_0
                                     69 	.globl _P3_1
                                     70 	.globl _P3_2
                                     71 	.globl _P3_3
                                     72 	.globl _P3_4
                                     73 	.globl _P3_5
                                     74 	.globl _P3_6
                                     75 	.globl _P3_7
                                     76 	.globl _CAP1_
                                     77 	.globl _T2_
                                     78 	.globl _CAP2_
                                     79 	.globl _T2EX_
                                     80 	.globl _RXD1
                                     81 	.globl _TXD1
                                     82 	.globl _P2_0
                                     83 	.globl _P2_1
                                     84 	.globl _P2_2
                                     85 	.globl _P2_3
                                     86 	.globl _P2_4
                                     87 	.globl _P2_5
                                     88 	.globl _P2_6
                                     89 	.globl _P2_7
                                     90 	.globl _AIN0
                                     91 	.globl _AIN1
                                     92 	.globl _AIN2
                                     93 	.globl _AIN3
                                     94 	.globl _AIN4
                                     95 	.globl _AIN5
                                     96 	.globl _AIN6
                                     97 	.globl _AIN7
                                     98 	.globl _CAP1
                                     99 	.globl _T2
                                    100 	.globl _CAP2
                                    101 	.globl _T2EX
                                    102 	.globl _INT0_
                                    103 	.globl _SCS
                                    104 	.globl _MOSI
                                    105 	.globl _MISO
                                    106 	.globl _SCK
                                    107 	.globl _RXD1_
                                    108 	.globl _TXD1_
                                    109 	.globl _P1_0
                                    110 	.globl _P1_1
                                    111 	.globl _P1_2
                                    112 	.globl _P1_3
                                    113 	.globl _P1_4
                                    114 	.globl _P1_5
                                    115 	.globl _P1_6
                                    116 	.globl _P1_7
                                    117 	.globl _AIN8
                                    118 	.globl _AIN9
                                    119 	.globl _AIN10
                                    120 	.globl _AIN11
                                    121 	.globl _AIN12
                                    122 	.globl _AIN13
                                    123 	.globl _RXD_
                                    124 	.globl _TXD_
                                    125 	.globl _SCL0
                                    126 	.globl _SDA0
                                    127 	.globl _P0_0
                                    128 	.globl _P0_1
                                    129 	.globl _P0_2
                                    130 	.globl _P0_3
                                    131 	.globl _P0_4
                                    132 	.globl _P0_5
                                    133 	.globl _P0_6
                                    134 	.globl _P0_7
                                    135 	.globl _IE_SPI0
                                    136 	.globl _IE_USB
                                    137 	.globl _IE_ADC
                                    138 	.globl _IE_UART1
                                    139 	.globl _IE_PWM_I2C
                                    140 	.globl _IE_GPIO
                                    141 	.globl _IE_WDOG
                                    142 	.globl _PX0
                                    143 	.globl _PT0
                                    144 	.globl _PX1
                                    145 	.globl _PT1
                                    146 	.globl _PS
                                    147 	.globl _PT2
                                    148 	.globl _PL_FLAG
                                    149 	.globl _PH_FLAG
                                    150 	.globl _EX0
                                    151 	.globl _ET0
                                    152 	.globl _EX1
                                    153 	.globl _ET1
                                    154 	.globl _ES
                                    155 	.globl _ET2
                                    156 	.globl _E_DIS
                                    157 	.globl _EA
                                    158 	.globl _P
                                    159 	.globl _F1
                                    160 	.globl _OV
                                    161 	.globl _RS0
                                    162 	.globl _RS1
                                    163 	.globl _F0
                                    164 	.globl _AC
                                    165 	.globl _CY
                                    166 	.globl _I2CS_INT_ST
                                    167 	.globl _I2CX_INT
                                    168 	.globl _LED_STATUS
                                    169 	.globl _LED_DMA_H
                                    170 	.globl _LED_DMA_L
                                    171 	.globl _LED_DMA
                                    172 	.globl _LED_PWM_OE
                                    173 	.globl _LED_COMMON
                                    174 	.globl _ADC_CHAN
                                    175 	.globl _ADC_DAT_H
                                    176 	.globl _ADC_DAT_L
                                    177 	.globl _ADC_DAT
                                    178 	.globl _ADC_CTRL
                                    179 	.globl _SPI1_CK_SE
                                    180 	.globl _SPI1_CTRL
                                    181 	.globl _SPI1_DATA
                                    182 	.globl _SPI1_STAT
                                    183 	.globl _SIF1
                                    184 	.globl _SBAUD1
                                    185 	.globl _SBUF1
                                    186 	.globl _SCON1
                                    187 	.globl _SPI0_SETUP
                                    188 	.globl _SPI0_CK_SE
                                    189 	.globl _SPI0_CTRL
                                    190 	.globl _SPI0_DATA
                                    191 	.globl _SPI0_STAT
                                    192 	.globl _T2CAP1H
                                    193 	.globl _T2CAP1L
                                    194 	.globl _T2CAP1
                                    195 	.globl _TH2
                                    196 	.globl _TL2
                                    197 	.globl _T2COUNT
                                    198 	.globl _RCAP2H
                                    199 	.globl _RCAP2L
                                    200 	.globl _RCAP2
                                    201 	.globl _T2MOD
                                    202 	.globl _T2CON
                                    203 	.globl _SBUF
                                    204 	.globl _SCON
                                    205 	.globl _TH1
                                    206 	.globl _TH0
                                    207 	.globl _TL1
                                    208 	.globl _TL0
                                    209 	.globl _TMOD
                                    210 	.globl _TCON
                                    211 	.globl _XBUS_AUX
                                    212 	.globl _P7
                                    213 	.globl _P6_DIR
                                    214 	.globl _P6_OUT_PU
                                    215 	.globl _P6_IN
                                    216 	.globl _P5_DIR
                                    217 	.globl _P5_OUT_PU
                                    218 	.globl _P5_IN
                                    219 	.globl _P4_LED_KEY
                                    220 	.globl _P4_DIR_PU
                                    221 	.globl _P4_MOD_OC
                                    222 	.globl _P4
                                    223 	.globl _P3_DIR_PU
                                    224 	.globl _P3_MOD_OC
                                    225 	.globl _P3
                                    226 	.globl _P2_DIR_PU
                                    227 	.globl _P2_MOD_OC
                                    228 	.globl _P2
                                    229 	.globl _P1_DIR_PU
                                    230 	.globl _P1_MOD_OC
                                    231 	.globl _P1
                                    232 	.globl _P0_DIR_PU
                                    233 	.globl _P0_MOD_OC
                                    234 	.globl _P0
                                    235 	.globl _ROM_CTRL
                                    236 	.globl _ROM_DATA_HH
                                    237 	.globl _ROM_DATA_HL
                                    238 	.globl _ROM_DATA_HI
                                    239 	.globl _ROM_ADDR_H
                                    240 	.globl _ROM_ADDR_L
                                    241 	.globl _ROM_ADDR
                                    242 	.globl _GPIO_IE
                                    243 	.globl _IP_EX
                                    244 	.globl _IE_EX
                                    245 	.globl _IP
                                    246 	.globl _IE
                                    247 	.globl _WDOG_COUNT
                                    248 	.globl _RESET_KEEP
                                    249 	.globl _WAKE_CTRL
                                    250 	.globl _CLOCK_CFG
                                    251 	.globl _POWER_CFG
                                    252 	.globl _PCON
                                    253 	.globl _GLOBAL_CFG
                                    254 	.globl _SAFE_MOD
                                    255 	.globl _DPH
                                    256 	.globl _DPL
                                    257 	.globl _SP
                                    258 	.globl _A_INV
                                    259 	.globl _B
                                    260 	.globl _ACC
                                    261 	.globl _PSW
                                    262 	.globl _encoder_init
                                    263 	.globl _encoder_read
                                    264 ;--------------------------------------------------------
                                    265 ; special function registers
                                    266 ;--------------------------------------------------------
                                    267 	.area RSEG    (ABS,DATA)
      000000                        268 	.org 0x0000
                           0000D0   269 _PSW	=	0x00d0
                           0000E0   270 _ACC	=	0x00e0
                           0000F0   271 _B	=	0x00f0
                           0000FD   272 _A_INV	=	0x00fd
                           000081   273 _SP	=	0x0081
                           000082   274 _DPL	=	0x0082
                           000083   275 _DPH	=	0x0083
                           0000A1   276 _SAFE_MOD	=	0x00a1
                           0000B1   277 _GLOBAL_CFG	=	0x00b1
                           000087   278 _PCON	=	0x0087
                           0000BA   279 _POWER_CFG	=	0x00ba
                           0000B9   280 _CLOCK_CFG	=	0x00b9
                           0000A9   281 _WAKE_CTRL	=	0x00a9
                           0000FE   282 _RESET_KEEP	=	0x00fe
                           0000FF   283 _WDOG_COUNT	=	0x00ff
                           0000A8   284 _IE	=	0x00a8
                           0000B8   285 _IP	=	0x00b8
                           0000E8   286 _IE_EX	=	0x00e8
                           0000E9   287 _IP_EX	=	0x00e9
                           0000B2   288 _GPIO_IE	=	0x00b2
                           008584   289 _ROM_ADDR	=	0x8584
                           000084   290 _ROM_ADDR_L	=	0x0084
                           000085   291 _ROM_ADDR_H	=	0x0085
                           008F8E   292 _ROM_DATA_HI	=	0x8f8e
                           00008E   293 _ROM_DATA_HL	=	0x008e
                           00008F   294 _ROM_DATA_HH	=	0x008f
                           000086   295 _ROM_CTRL	=	0x0086
                           000080   296 _P0	=	0x0080
                           0000C4   297 _P0_MOD_OC	=	0x00c4
                           0000C5   298 _P0_DIR_PU	=	0x00c5
                           000090   299 _P1	=	0x0090
                           000092   300 _P1_MOD_OC	=	0x0092
                           000093   301 _P1_DIR_PU	=	0x0093
                           0000A0   302 _P2	=	0x00a0
                           000094   303 _P2_MOD_OC	=	0x0094
                           000095   304 _P2_DIR_PU	=	0x0095
                           0000B0   305 _P3	=	0x00b0
                           000096   306 _P3_MOD_OC	=	0x0096
                           000097   307 _P3_DIR_PU	=	0x0097
                           0000C0   308 _P4	=	0x00c0
                           0000C2   309 _P4_MOD_OC	=	0x00c2
                           0000C3   310 _P4_DIR_PU	=	0x00c3
                           0000C1   311 _P4_LED_KEY	=	0x00c1
                           0000AA   312 _P5_IN	=	0x00aa
                           0000AB   313 _P5_OUT_PU	=	0x00ab
                           0000AC   314 _P5_DIR	=	0x00ac
                           0000AD   315 _P6_IN	=	0x00ad
                           0000AE   316 _P6_OUT_PU	=	0x00ae
                           0000AF   317 _P6_DIR	=	0x00af
                           0000F1   318 _P7	=	0x00f1
                           0000A2   319 _XBUS_AUX	=	0x00a2
                           000088   320 _TCON	=	0x0088
                           000089   321 _TMOD	=	0x0089
                           00008A   322 _TL0	=	0x008a
                           00008B   323 _TL1	=	0x008b
                           00008C   324 _TH0	=	0x008c
                           00008D   325 _TH1	=	0x008d
                           000098   326 _SCON	=	0x0098
                           000099   327 _SBUF	=	0x0099
                           0000C8   328 _T2CON	=	0x00c8
                           0000C9   329 _T2MOD	=	0x00c9
                           00CBCA   330 _RCAP2	=	0xcbca
                           0000CA   331 _RCAP2L	=	0x00ca
                           0000CB   332 _RCAP2H	=	0x00cb
                           00CDCC   333 _T2COUNT	=	0xcdcc
                           0000CC   334 _TL2	=	0x00cc
                           0000CD   335 _TH2	=	0x00cd
                           00CFCE   336 _T2CAP1	=	0xcfce
                           0000CE   337 _T2CAP1L	=	0x00ce
                           0000CF   338 _T2CAP1H	=	0x00cf
                           0000F8   339 _SPI0_STAT	=	0x00f8
                           0000F9   340 _SPI0_DATA	=	0x00f9
                           0000FA   341 _SPI0_CTRL	=	0x00fa
                           0000FB   342 _SPI0_CK_SE	=	0x00fb
                           0000FC   343 _SPI0_SETUP	=	0x00fc
                           0000BC   344 _SCON1	=	0x00bc
                           0000BD   345 _SBUF1	=	0x00bd
                           0000BE   346 _SBAUD1	=	0x00be
                           0000BF   347 _SIF1	=	0x00bf
                           0000B4   348 _SPI1_STAT	=	0x00b4
                           0000B5   349 _SPI1_DATA	=	0x00b5
                           0000B6   350 _SPI1_CTRL	=	0x00b6
                           0000B7   351 _SPI1_CK_SE	=	0x00b7
                           0000F3   352 _ADC_CTRL	=	0x00f3
                           00F5F4   353 _ADC_DAT	=	0xf5f4
                           0000F4   354 _ADC_DAT_L	=	0x00f4
                           0000F5   355 _ADC_DAT_H	=	0x00f5
                           0000F6   356 _ADC_CHAN	=	0x00f6
                           0000A6   357 _LED_COMMON	=	0x00a6
                           0000A7   358 _LED_PWM_OE	=	0x00a7
                           00C7C6   359 _LED_DMA	=	0xc7c6
                           0000C6   360 _LED_DMA_L	=	0x00c6
                           0000C7   361 _LED_DMA_H	=	0x00c7
                           0000F7   362 _LED_STATUS	=	0x00f7
                           0000B3   363 _I2CX_INT	=	0x00b3
                           0000BB   364 _I2CS_INT_ST	=	0x00bb
                                    365 ;--------------------------------------------------------
                                    366 ; special function bits
                                    367 ;--------------------------------------------------------
                                    368 	.area RSEG    (ABS,DATA)
      000000                        369 	.org 0x0000
                           0000D7   370 _CY	=	0x00d7
                           0000D6   371 _AC	=	0x00d6
                           0000D5   372 _F0	=	0x00d5
                           0000D4   373 _RS1	=	0x00d4
                           0000D3   374 _RS0	=	0x00d3
                           0000D2   375 _OV	=	0x00d2
                           0000D1   376 _F1	=	0x00d1
                           0000D0   377 _P	=	0x00d0
                           0000AF   378 _EA	=	0x00af
                           0000AE   379 _E_DIS	=	0x00ae
                           0000AD   380 _ET2	=	0x00ad
                           0000AC   381 _ES	=	0x00ac
                           0000AB   382 _ET1	=	0x00ab
                           0000AA   383 _EX1	=	0x00aa
                           0000A9   384 _ET0	=	0x00a9
                           0000A8   385 _EX0	=	0x00a8
                           0000BF   386 _PH_FLAG	=	0x00bf
                           0000BE   387 _PL_FLAG	=	0x00be
                           0000BD   388 _PT2	=	0x00bd
                           0000BC   389 _PS	=	0x00bc
                           0000BB   390 _PT1	=	0x00bb
                           0000BA   391 _PX1	=	0x00ba
                           0000B9   392 _PT0	=	0x00b9
                           0000B8   393 _PX0	=	0x00b8
                           0000EF   394 _IE_WDOG	=	0x00ef
                           0000EE   395 _IE_GPIO	=	0x00ee
                           0000ED   396 _IE_PWM_I2C	=	0x00ed
                           0000EC   397 _IE_UART1	=	0x00ec
                           0000EB   398 _IE_ADC	=	0x00eb
                           0000E9   399 _IE_USB	=	0x00e9
                           0000E8   400 _IE_SPI0	=	0x00e8
                           000087   401 _P0_7	=	0x0087
                           000086   402 _P0_6	=	0x0086
                           000085   403 _P0_5	=	0x0085
                           000084   404 _P0_4	=	0x0084
                           000083   405 _P0_3	=	0x0083
                           000082   406 _P0_2	=	0x0082
                           000081   407 _P0_1	=	0x0081
                           000080   408 _P0_0	=	0x0080
                           000081   409 _SDA0	=	0x0081
                           000080   410 _SCL0	=	0x0080
                           000083   411 _TXD_	=	0x0083
                           000082   412 _RXD_	=	0x0082
                           000085   413 _AIN13	=	0x0085
                           000084   414 _AIN12	=	0x0084
                           000083   415 _AIN11	=	0x0083
                           000082   416 _AIN10	=	0x0082
                           000081   417 _AIN9	=	0x0081
                           000080   418 _AIN8	=	0x0080
                           000097   419 _P1_7	=	0x0097
                           000096   420 _P1_6	=	0x0096
                           000095   421 _P1_5	=	0x0095
                           000094   422 _P1_4	=	0x0094
                           000093   423 _P1_3	=	0x0093
                           000092   424 _P1_2	=	0x0092
                           000091   425 _P1_1	=	0x0091
                           000090   426 _P1_0	=	0x0090
                           000097   427 _TXD1_	=	0x0097
                           000096   428 _RXD1_	=	0x0096
                           000097   429 _SCK	=	0x0097
                           000096   430 _MISO	=	0x0096
                           000095   431 _MOSI	=	0x0095
                           000094   432 _SCS	=	0x0094
                           000092   433 _INT0_	=	0x0092
                           000091   434 _T2EX	=	0x0091
                           000091   435 _CAP2	=	0x0091
                           000090   436 _T2	=	0x0090
                           000090   437 _CAP1	=	0x0090
                           000097   438 _AIN7	=	0x0097
                           000096   439 _AIN6	=	0x0096
                           000095   440 _AIN5	=	0x0095
                           000094   441 _AIN4	=	0x0094
                           000093   442 _AIN3	=	0x0093
                           000092   443 _AIN2	=	0x0092
                           000091   444 _AIN1	=	0x0091
                           000090   445 _AIN0	=	0x0090
                           0000A7   446 _P2_7	=	0x00a7
                           0000A6   447 _P2_6	=	0x00a6
                           0000A5   448 _P2_5	=	0x00a5
                           0000A4   449 _P2_4	=	0x00a4
                           0000A3   450 _P2_3	=	0x00a3
                           0000A2   451 _P2_2	=	0x00a2
                           0000A1   452 _P2_1	=	0x00a1
                           0000A0   453 _P2_0	=	0x00a0
                           0000A7   454 _TXD1	=	0x00a7
                           0000A6   455 _RXD1	=	0x00a6
                           0000A5   456 _T2EX_	=	0x00a5
                           0000A5   457 _CAP2_	=	0x00a5
                           0000A4   458 _T2_	=	0x00a4
                           0000A4   459 _CAP1_	=	0x00a4
                           0000B7   460 _P3_7	=	0x00b7
                           0000B6   461 _P3_6	=	0x00b6
                           0000B5   462 _P3_5	=	0x00b5
                           0000B4   463 _P3_4	=	0x00b4
                           0000B3   464 _P3_3	=	0x00b3
                           0000B2   465 _P3_2	=	0x00b2
                           0000B1   466 _P3_1	=	0x00b1
                           0000B0   467 _P3_0	=	0x00b0
                           0000B7   468 _SCK1	=	0x00b7
                           0000B6   469 _MISO1	=	0x00b6
                           0000B5   470 _MOSI1	=	0x00b5
                           0000B5   471 _T1	=	0x00b5
                           0000B4   472 _T0	=	0x00b4
                           0000B3   473 _INT1	=	0x00b3
                           0000B2   474 _INT0	=	0x00b2
                           0000B1   475 _TXD	=	0x00b1
                           0000B0   476 _RXD	=	0x00b0
                           0000C6   477 _P4_6	=	0x00c6
                           0000C5   478 _P4_5	=	0x00c5
                           0000C4   479 _P4_4	=	0x00c4
                           0000C3   480 _P4_3	=	0x00c3
                           0000C2   481 _P4_2	=	0x00c2
                           0000C1   482 _P4_1	=	0x00c1
                           0000C0   483 _P4_0	=	0x00c0
                           00008F   484 _TF1	=	0x008f
                           00008E   485 _TR1	=	0x008e
                           00008D   486 _TF0	=	0x008d
                           00008C   487 _TR0	=	0x008c
                           00008B   488 _IE1	=	0x008b
                           00008A   489 _IT1	=	0x008a
                           000089   490 _IE0	=	0x0089
                           000088   491 _IT0	=	0x0088
                           00009F   492 _SM0	=	0x009f
                           00009E   493 _SM1	=	0x009e
                           00009D   494 _SM2	=	0x009d
                           00009C   495 _REN	=	0x009c
                           00009B   496 _TB8	=	0x009b
                           00009A   497 _RB8	=	0x009a
                           000099   498 _TI	=	0x0099
                           000098   499 _RI	=	0x0098
                           0000CF   500 _TF2	=	0x00cf
                           0000CF   501 _CAP1F	=	0x00cf
                           0000CE   502 _EXF2	=	0x00ce
                           0000CD   503 _RCLK	=	0x00cd
                           0000CC   504 _TCLK	=	0x00cc
                           0000CB   505 _EXEN2	=	0x00cb
                           0000CA   506 _TR2	=	0x00ca
                           0000C9   507 _C_T2	=	0x00c9
                           0000C8   508 _CP_RL2	=	0x00c8
                           0000FF   509 _S0_FST_ACT	=	0x00ff
                           0000FE   510 _S0_IF_OV	=	0x00fe
                           0000FD   511 _S0_IF_FIRST	=	0x00fd
                           0000FC   512 _S0_IF_BYTE	=	0x00fc
                           0000FB   513 _S0_FREE	=	0x00fb
                           0000FA   514 _S0_T_FIFO	=	0x00fa
                           0000F8   515 _S0_R_FIFO	=	0x00f8
                           0000F7   516 _ADC_START	=	0x00f7
                                    517 ;--------------------------------------------------------
                                    518 ; overlayable register banks
                                    519 ;--------------------------------------------------------
                                    520 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        521 	.ds 8
                                    522 ;--------------------------------------------------------
                                    523 ; internal ram data
                                    524 ;--------------------------------------------------------
                                    525 	.area DSEG    (DATA)
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
      000939                        550 _thisCount:
      000939                        551 	.ds 1
      00093A                        552 _encoder_exec_mapping_PARM_2:
      00093A                        553 	.ds 1
      00093B                        554 _encoder_exec_mapping_index_10000_165:
      00093B                        555 	.ds 1
      00093C                        556 _encoder_exec_mapping_dummy_event_30000_168:
      00093C                        557 	.ds 6
      000942                        558 _encoder_exec_mapping_dummy_event_30000_169:
      000942                        559 	.ds 6
      000948                        560 _encoder_exec_mapping_dummy_event_30000_171:
      000948                        561 	.ds 6
      00094E                        562 _encoder_exec_mapping_dummy_event_30000_172:
      00094E                        563 	.ds 6
      000954                        564 _encoder_update_PARM_2:
      000954                        565 	.ds 1
      000955                        566 _encoder_update_index_10000_173:
      000955                        567 	.ds 1
      000956                        568 _encoder_update_changed_10000_174:
      000956                        569 	.ds 1
      000957                        570 _encoder_read_changed_10000_180:
      000957                        571 	.ds 1
                                    572 ;--------------------------------------------------------
                                    573 ; absolute external ram data
                                    574 ;--------------------------------------------------------
                                    575 	.area XABS    (ABS,XDATA)
                                    576 ;--------------------------------------------------------
                                    577 ; initialized external ram data
                                    578 ;--------------------------------------------------------
                                    579 	.area XISEG   (XDATA)
      000BD4                        580 _encoders_pad_a:
      000BD4                        581 	.ds 1
      000BD5                        582 _encoders_pad_b:
      000BD5                        583 	.ds 1
      000BD6                        584 _encoder_LUT:
      000BD6                        585 	.ds 16
      000BE6                        586 _encoder_state:
      000BE6                        587 	.ds 1
      000BE7                        588 _encoder_pulses:
      000BE7                        589 	.ds 1
      000BE8                        590 _encoder_value:
      000BE8                        591 	.ds 1
                                    592 	.area HOME    (CODE)
                                    593 	.area GSINIT0 (CODE)
                                    594 	.area GSINIT1 (CODE)
                                    595 	.area GSINIT2 (CODE)
                                    596 	.area GSINIT3 (CODE)
                                    597 	.area GSINIT4 (CODE)
                                    598 	.area GSINIT5 (CODE)
                                    599 	.area GSINIT  (CODE)
                                    600 	.area GSFINAL (CODE)
                                    601 	.area CSEG    (CODE)
                                    602 ;--------------------------------------------------------
                                    603 ; global & static initialisations
                                    604 ;--------------------------------------------------------
                                    605 	.area HOME    (CODE)
                                    606 	.area GSINIT  (CODE)
                                    607 	.area GSFINAL (CODE)
                                    608 	.area GSINIT  (CODE)
                                    609 ;--------------------------------------------------------
                                    610 ; Home
                                    611 ;--------------------------------------------------------
                                    612 	.area HOME    (CODE)
                                    613 	.area HOME    (CODE)
                                    614 ;--------------------------------------------------------
                                    615 ; code
                                    616 ;--------------------------------------------------------
                                    617 	.area CSEG    (CODE)
                                    618 ;------------------------------------------------------------
                                    619 ;Allocation info for local variables in function 'encoder_wait_pullup_charge'
                                    620 ;------------------------------------------------------------
                                    621 ;i             Allocated with name '_encoder_wait_pullup_charge_i_30000_146'
                                    622 ;------------------------------------------------------------
                                    623 ;	quantum/encoder.c:77: __attribute__((weak)) void encoder_wait_pullup_charge(void) {
                                    624 ;	-----------------------------------------
                                    625 ;	 function encoder_wait_pullup_charge
                                    626 ;	-----------------------------------------
      0087DE                        627 _encoder_wait_pullup_charge:
                           000007   628 	ar7 = 0x07
                           000006   629 	ar6 = 0x06
                           000005   630 	ar5 = 0x05
                           000004   631 	ar4 = 0x04
                           000003   632 	ar3 = 0x03
                           000002   633 	ar2 = 0x02
                           000001   634 	ar1 = 0x01
                           000000   635 	ar0 = 0x00
                                    636 ;	quantum/encoder.c:78: wait_us(100);
      0087DE 7F 64            [12]  637 	mov	r7,#0x64
      0087E0                        638 00106$:
      0087E0 EF               [12]  639 	mov	a,r7
      0087E1 60 0D            [24]  640 	jz	00108$
      0087E3 90 00 01         [24]  641 	mov	dptr,#0x0001
      0087E6 C0 07            [24]  642 	push	ar7
      0087E8 12 52 22         [24]  643 	lcall	_mDelayuS
      0087EB D0 07            [24]  644 	pop	ar7
      0087ED 1F               [12]  645 	dec	r7
      0087EE 80 F0            [24]  646 	sjmp	00106$
      0087F0                        647 00108$:
                                    648 ;	quantum/encoder.c:79: }
      0087F0 22               [24]  649 	ret
                                    650 ;------------------------------------------------------------
                                    651 ;Allocation info for local variables in function 'encoder_update_user'
                                    652 ;------------------------------------------------------------
                                    653 ;clockwise     Allocated with name '_encoder_update_user_PARM_2'
                                    654 ;index         Allocated with name '_encoder_update_user_index_10000_148'
                                    655 ;------------------------------------------------------------
                                    656 ;	quantum/encoder.c:81: __attribute__((weak)) bool encoder_update_user(uint8_t index, bool clockwise) {
                                    657 ;	-----------------------------------------
                                    658 ;	 function encoder_init
                                    659 ;	-----------------------------------------
      0087F1                        660 _encoder_init:
                                    661 ;	quantum/encoder.c:122: thisCount                = NUM_ENCODERS;
      0087F1 90 09 39         [24]  662 	mov	dptr,#_thisCount
      0087F4 74 01            [12]  663 	mov	a,#0x01
      0087F6 F0               [24]  664 	movx	@dptr,a
                                    665 ;	quantum/encoder.c:165: for (uint8_t i = 0; i < thisCount; i++) {
      0087F7 7F 00            [12]  666 	mov	r7,#0x00
      0087F9                        667 00104$:
      0087F9 90 09 39         [24]  668 	mov	dptr,#_thisCount
      0087FC E0               [24]  669 	movx	a,@dptr
      0087FD FE               [12]  670 	mov	r6,a
      0087FE C3               [12]  671 	clr	c
      0087FF EF               [12]  672 	mov	a,r7
      008800 9E               [12]  673 	subb	a,r6
      008801 50 17            [24]  674 	jnc	00101$
                                    675 ;	quantum/encoder.c:166: setPinInputHigh(encoders_pad_a[i]);
      008803 12 8A AB         [24]  676 	lcall	_ak820_outline_0019
      008806 C0 07            [24]  677 	push	ar7
      008808 12 50 E4         [24]  678 	lcall	_pinModeInputHighQMK
      00880B D0 07            [24]  679 	pop	ar7
                                    680 ;	quantum/encoder.c:167: setPinInputHigh(encoders_pad_b[i]);
      00880D 12 8A B9         [24]  681 	lcall	_ak820_outline_0020
      008810 C0 07            [24]  682 	push	ar7
      008812 12 50 E4         [24]  683 	lcall	_pinModeInputHighQMK
      008815 D0 07            [24]  684 	pop	ar7
                                    685 ;	quantum/encoder.c:165: for (uint8_t i = 0; i < thisCount; i++) {
      008817 0F               [12]  686 	inc	r7
      008818 80 DF            [24]  687 	sjmp	00104$
      00881A                        688 00101$:
                                    689 ;	quantum/encoder.c:169: encoder_wait_pullup_charge();
      00881A 12 87 DE         [24]  690 	lcall	_encoder_wait_pullup_charge
                                    691 ;	quantum/encoder.c:170: for (uint8_t i = 0; i < thisCount; i++) {
      00881D 7F 00            [12]  692 	mov	r7,#0x00
      00881F                        693 00107$:
      00881F 90 09 39         [24]  694 	mov	dptr,#_thisCount
      008822 E0               [24]  695 	movx	a,@dptr
      008823 FE               [12]  696 	mov	r6,a
      008824 C3               [12]  697 	clr	c
      008825 EF               [12]  698 	mov	a,r7
      008826 9E               [12]  699 	subb	a,r6
      008827 50 25            [24]  700 	jnc	00109$
                                    701 ;	quantum/encoder.c:171: encoder_state[i] = (readPin(encoders_pad_a[i]) << 0) | (readPin(encoders_pad_b[i]) << 1);
      008829 EF               [12]  702 	mov	a,r7
      00882A 24 E6            [12]  703 	add	a, #_encoder_state
      00882C FD               [12]  704 	mov	r5,a
      00882D E4               [12]  705 	clr	a
      00882E 34 0B            [12]  706 	addc	a, #(_encoder_state >> 8)
      008830 FE               [12]  707 	mov	r6,a
      008831 12 8A AB         [24]  708 	lcall	_ak820_outline_0019
      008834 12 51 30         [24]  709 	lcall	_readPin
      008837 AC 82            [24]  710 	mov	r4, dpl
      008839 12 8A B9         [24]  711 	lcall	_ak820_outline_0020
      00883C 12 51 30         [24]  712 	lcall	_readPin
      00883F E5 82            [12]  713 	mov	a,dpl
      008841 25 82            [12]  714 	add	a,dpl
      008843 42 04            [12]  715 	orl	ar4,a
      008845 8D 82            [24]  716 	mov	dpl,r5
      008847 8E 83            [24]  717 	mov	dph,r6
      008849 EC               [12]  718 	mov	a,r4
      00884A F0               [24]  719 	movx	@dptr,a
                                    720 ;	quantum/encoder.c:170: for (uint8_t i = 0; i < thisCount; i++) {
      00884B 0F               [12]  721 	inc	r7
      00884C 80 D1            [24]  722 	sjmp	00107$
      00884E                        723 00109$:
                                    724 ;	quantum/encoder.c:173: }
      00884E 22               [24]  725 	ret
                                    726 ;------------------------------------------------------------
                                    727 ;Allocation info for local variables in function 'encoder_exec_mapping'
                                    728 ;------------------------------------------------------------
                                    729 ;clockwise     Allocated with name '_encoder_exec_mapping_PARM_2'
                                    730 ;index         Allocated with name '_encoder_exec_mapping_index_10000_165'
                                    731 ;dummy_event   Allocated with name '_encoder_exec_mapping_dummy_event_30000_168'
                                    732 ;dummy_event   Allocated with name '_encoder_exec_mapping_dummy_event_30000_169'
                                    733 ;dummy_event   Allocated with name '_encoder_exec_mapping_dummy_event_30000_171'
                                    734 ;dummy_event   Allocated with name '_encoder_exec_mapping_dummy_event_30000_172'
                                    735 ;------------------------------------------------------------
                                    736 ;	quantum/encoder.c:176: static void encoder_exec_mapping(uint8_t index, bool clockwise) {
                                    737 ;	-----------------------------------------
                                    738 ;	 function encoder_exec_mapping
                                    739 ;	-----------------------------------------
      00884F                        740 _encoder_exec_mapping:
      00884F E5 82            [12]  741 	mov	a,dpl
      008851 90 09 3B         [24]  742 	mov	dptr,#_encoder_exec_mapping_index_10000_165
      008854 F0               [24]  743 	movx	@dptr,a
                                    744 ;	quantum/encoder.c:179: if (clockwise) {
      008855 90 09 3A         [24]  745 	mov	dptr,#_encoder_exec_mapping_PARM_2
      008858 E0               [24]  746 	movx	a,@dptr
      008859 FF               [12]  747 	mov	r7,a
      00885A E0               [24]  748 	movx	a,@dptr
      00885B 60 3F            [24]  749 	jz	00102$
                                    750 ;	quantum/encoder.c:180: MAKE_ENCODER_CW_EVENT(index, true);
      00885D 90 09 3B         [24]  751 	mov	dptr,#_encoder_exec_mapping_index_10000_165
      008860 E0               [24]  752 	movx	a,@dptr
      008861 90 09 3C         [24]  753 	mov	dptr,#_encoder_exec_mapping_dummy_event_30000_168
      008864 F0               [24]  754 	movx	@dptr,a
      008865 90 09 3D         [24]  755 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_168 + 0x0001)
      008868 74 FD            [12]  756 	mov	a,#0xfd
      00886A F0               [24]  757 	movx	@dptr,a
      00886B 12 40 4E         [24]  758 	lcall	_timer_read
      00886E AD 82            [24]  759 	mov	r5, dpl
      008870 AE 83            [24]  760 	mov	r6, dph
      008872 90 09 3E         [24]  761 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_168 + 0x0002)
      008875 ED               [12]  762 	mov	a,r5
      008876 F0               [24]  763 	movx	@dptr,a
      008877 EE               [12]  764 	mov	a,r6
      008878 A3               [24]  765 	inc	dptr
      008879 F0               [24]  766 	movx	@dptr,a
      00887A 90 09 40         [24]  767 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_168 + 0x0004)
      00887D 74 02            [12]  768 	mov	a,#0x02
      00887F F0               [24]  769 	movx	@dptr,a
      008880 90 09 41         [24]  770 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_168 + 0x0005)
      008883 14               [12]  771 	dec	a
      008884 F0               [24]  772 	movx	@dptr,a
                                    773 ;	quantum/encoder.c:181: action_exec(dummy_event);
      008885 90 0B 8F         [24]  774 	mov	dptr,#___memcpy_PARM_2
      008888 74 3C            [12]  775 	mov	a,#_encoder_exec_mapping_dummy_event_30000_168
      00888A F0               [24]  776 	movx	@dptr,a
      00888B 74 09            [12]  777 	mov	a,#(_encoder_exec_mapping_dummy_event_30000_168 >> 8)
      00888D 12 8A 97         [24]  778 	lcall	_ak820_outline_0007
      008890 C0 07            [24]  779 	push	ar7
      008892 12 B4 9F         [24]  780 	lcall	___memcpy
      008895 12 6C E1         [24]  781 	lcall	_action_exec
      008898 D0 07            [24]  782 	pop	ar7
      00889A 80 3E            [24]  783 	sjmp	00103$
      00889C                        784 00102$:
                                    785 ;	quantum/encoder.c:183: MAKE_ENCODER_CCW_EVENT(index, true);
      00889C 90 09 3B         [24]  786 	mov	dptr,#_encoder_exec_mapping_index_10000_165
      00889F E0               [24]  787 	movx	a,@dptr
      0088A0 90 09 42         [24]  788 	mov	dptr,#_encoder_exec_mapping_dummy_event_30000_169
      0088A3 F0               [24]  789 	movx	@dptr,a
      0088A4 90 09 43         [24]  790 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_169 + 0x0001)
      0088A7 74 FC            [12]  791 	mov	a,#0xfc
      0088A9 F0               [24]  792 	movx	@dptr,a
      0088AA 12 40 4E         [24]  793 	lcall	_timer_read
      0088AD AD 82            [24]  794 	mov	r5, dpl
      0088AF AE 83            [24]  795 	mov	r6, dph
      0088B1 90 09 44         [24]  796 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_169 + 0x0002)
      0088B4 ED               [12]  797 	mov	a,r5
      0088B5 F0               [24]  798 	movx	@dptr,a
      0088B6 EE               [12]  799 	mov	a,r6
      0088B7 A3               [24]  800 	inc	dptr
      0088B8 F0               [24]  801 	movx	@dptr,a
      0088B9 90 09 46         [24]  802 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_169 + 0x0004)
      0088BC 74 03            [12]  803 	mov	a,#0x03
      0088BE F0               [24]  804 	movx	@dptr,a
      0088BF 90 09 47         [24]  805 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_169 + 0x0005)
      0088C2 74 01            [12]  806 	mov	a,#0x01
      0088C4 F0               [24]  807 	movx	@dptr,a
                                    808 ;	quantum/encoder.c:184: action_exec(dummy_event);
      0088C5 90 0B 8F         [24]  809 	mov	dptr,#___memcpy_PARM_2
      0088C8 74 42            [12]  810 	mov	a,#_encoder_exec_mapping_dummy_event_30000_169
      0088CA F0               [24]  811 	movx	@dptr,a
      0088CB 74 09            [12]  812 	mov	a,#(_encoder_exec_mapping_dummy_event_30000_169 >> 8)
      0088CD 12 8A 97         [24]  813 	lcall	_ak820_outline_0007
      0088D0 C0 07            [24]  814 	push	ar7
      0088D2 12 B4 9F         [24]  815 	lcall	___memcpy
      0088D5 12 6C E1         [24]  816 	lcall	_action_exec
      0088D8 D0 07            [24]  817 	pop	ar7
      0088DA                        818 00103$:
                                    819 ;	quantum/encoder.c:191: if (clockwise) {
      0088DA EF               [12]  820 	mov	a,r7
      0088DB 60 39            [24]  821 	jz	00105$
                                    822 ;	quantum/encoder.c:192: MAKE_ENCODER_CW_EVENT(index, false);
      0088DD 90 09 3B         [24]  823 	mov	dptr,#_encoder_exec_mapping_index_10000_165
      0088E0 E0               [24]  824 	movx	a,@dptr
      0088E1 90 09 48         [24]  825 	mov	dptr,#_encoder_exec_mapping_dummy_event_30000_171
      0088E4 F0               [24]  826 	movx	@dptr,a
      0088E5 90 09 49         [24]  827 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_171 + 0x0001)
      0088E8 74 FD            [12]  828 	mov	a,#0xfd
      0088EA F0               [24]  829 	movx	@dptr,a
      0088EB 12 40 4E         [24]  830 	lcall	_timer_read
      0088EE AE 82            [24]  831 	mov	r6, dpl
      0088F0 AF 83            [24]  832 	mov	r7, dph
      0088F2 90 09 4A         [24]  833 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_171 + 0x0002)
      0088F5 EE               [12]  834 	mov	a,r6
      0088F6 F0               [24]  835 	movx	@dptr,a
      0088F7 EF               [12]  836 	mov	a,r7
      0088F8 A3               [24]  837 	inc	dptr
      0088F9 F0               [24]  838 	movx	@dptr,a
      0088FA 90 09 4C         [24]  839 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_171 + 0x0004)
      0088FD 74 02            [12]  840 	mov	a,#0x02
      0088FF F0               [24]  841 	movx	@dptr,a
      008900 90 09 4D         [24]  842 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_171 + 0x0005)
      008903 E4               [12]  843 	clr	a
      008904 F0               [24]  844 	movx	@dptr,a
                                    845 ;	quantum/encoder.c:193: action_exec(dummy_event);
      008905 90 0B 8F         [24]  846 	mov	dptr,#___memcpy_PARM_2
      008908 74 48            [12]  847 	mov	a,#_encoder_exec_mapping_dummy_event_30000_171
      00890A F0               [24]  848 	movx	@dptr,a
      00890B 74 09            [12]  849 	mov	a,#(_encoder_exec_mapping_dummy_event_30000_171 >> 8)
      00890D 12 8A 97         [24]  850 	lcall	_ak820_outline_0007
      008910 12 B4 9F         [24]  851 	lcall	___memcpy
      008913 02 6C E1         [24]  852 	ljmp	_action_exec
      008916                        853 00105$:
                                    854 ;	quantum/encoder.c:195: MAKE_ENCODER_CCW_EVENT(index, false);
      008916 90 09 3B         [24]  855 	mov	dptr,#_encoder_exec_mapping_index_10000_165
      008919 E0               [24]  856 	movx	a,@dptr
      00891A 90 09 4E         [24]  857 	mov	dptr,#_encoder_exec_mapping_dummy_event_30000_172
      00891D F0               [24]  858 	movx	@dptr,a
      00891E 90 09 4F         [24]  859 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_172 + 0x0001)
      008921 74 FC            [12]  860 	mov	a,#0xfc
      008923 F0               [24]  861 	movx	@dptr,a
      008924 12 40 4E         [24]  862 	lcall	_timer_read
      008927 AE 82            [24]  863 	mov	r6, dpl
      008929 AF 83            [24]  864 	mov	r7, dph
      00892B 90 09 50         [24]  865 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_172 + 0x0002)
      00892E EE               [12]  866 	mov	a,r6
      00892F F0               [24]  867 	movx	@dptr,a
      008930 EF               [12]  868 	mov	a,r7
      008931 A3               [24]  869 	inc	dptr
      008932 F0               [24]  870 	movx	@dptr,a
      008933 90 09 52         [24]  871 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_172 + 0x0004)
      008936 74 03            [12]  872 	mov	a,#0x03
      008938 F0               [24]  873 	movx	@dptr,a
      008939 90 09 53         [24]  874 	mov	dptr,#(_encoder_exec_mapping_dummy_event_30000_172 + 0x0005)
      00893C E4               [12]  875 	clr	a
      00893D F0               [24]  876 	movx	@dptr,a
                                    877 ;	quantum/encoder.c:196: action_exec(dummy_event);
      00893E 90 0B 8F         [24]  878 	mov	dptr,#___memcpy_PARM_2
      008941 74 4E            [12]  879 	mov	a,#_encoder_exec_mapping_dummy_event_30000_172
      008943 F0               [24]  880 	movx	@dptr,a
      008944 74 09            [12]  881 	mov	a,#(_encoder_exec_mapping_dummy_event_30000_172 >> 8)
      008946 12 8A 97         [24]  882 	lcall	_ak820_outline_0007
      008949 12 B4 9F         [24]  883 	lcall	___memcpy
                                    884 ;	quantum/encoder.c:201: }
      00894C 02 6C E1         [24]  885 	ljmp	_action_exec
                                    886 ;------------------------------------------------------------
                                    887 ;Allocation info for local variables in function 'encoder_update'
                                    888 ;------------------------------------------------------------
                                    889 ;state         Allocated with name '_encoder_update_PARM_2'
                                    890 ;index         Allocated with name '_encoder_update_index_10000_173'
                                    891 ;changed       Allocated with name '_encoder_update_changed_10000_174'
                                    892 ;i             Allocated with name '_encoder_update_i_10000_174'
                                    893 ;resolution    Allocated with name '_encoder_update_resolution_10000_174'
                                    894 ;------------------------------------------------------------
                                    895 ;	quantum/encoder.c:204: static bool encoder_update(uint8_t index, uint8_t state) {
                                    896 ;	-----------------------------------------
                                    897 ;	 function encoder_update
                                    898 ;	-----------------------------------------
      00894F                        899 _encoder_update:
      00894F E5 82            [12]  900 	mov	a,dpl
      008951 90 09 55         [24]  901 	mov	dptr,#_encoder_update_index_10000_173
      008954 F0               [24]  902 	movx	@dptr,a
                                    903 ;	quantum/encoder.c:205: bool    changed = false;
      008955 90 09 56         [24]  904 	mov	dptr,#_encoder_update_changed_10000_174
      008958 E4               [12]  905 	clr	a
      008959 F0               [24]  906 	movx	@dptr,a
                                    907 ;	quantum/encoder.c:206: uint8_t i       = index;
      00895A 90 09 55         [24]  908 	mov	dptr,#_encoder_update_index_10000_173
      00895D E0               [24]  909 	movx	a,@dptr
                                    910 ;	quantum/encoder.c:217: encoder_pulses[i] += encoder_LUT[state & 0xF];
      00895E FF               [12]  911 	mov	r7,a
      00895F 24 E7            [12]  912 	add	a, #_encoder_pulses
      008961 FD               [12]  913 	mov	r5,a
      008962 E4               [12]  914 	clr	a
      008963 34 0B            [12]  915 	addc	a, #(_encoder_pulses >> 8)
      008965 FE               [12]  916 	mov	r6,a
      008966 8D 82            [24]  917 	mov	dpl,r5
      008968 8E 83            [24]  918 	mov	dph,r6
      00896A E0               [24]  919 	movx	a,@dptr
      00896B FC               [12]  920 	mov	r4,a
      00896C 90 09 54         [24]  921 	mov	dptr,#_encoder_update_PARM_2
      00896F E0               [24]  922 	movx	a,@dptr
      008970 FB               [12]  923 	mov	r3,a
      008971 74 0F            [12]  924 	mov	a,#0x0f
      008973 5B               [12]  925 	anl	a,r3
      008974 24 D6            [12]  926 	add	a, #_encoder_LUT
      008976 F5 82            [12]  927 	mov	dpl,a
      008978 E4               [12]  928 	clr	a
      008979 34 0B            [12]  929 	addc	a,#(_encoder_LUT >> 8)
      00897B F5 83            [12]  930 	mov	dph,a
      00897D E0               [24]  931 	movx	a,@dptr
      00897E 2C               [12]  932 	add	a, r4
      00897F FC               [12]  933 	mov	r4,a
      008980 8D 82            [24]  934 	mov	dpl,r5
      008982 8E 83            [24]  935 	mov	dph,r6
      008984 F0               [24]  936 	movx	@dptr,a
                                    937 ;	quantum/encoder.c:223: if (encoder_pulses[i] >= resolution) {
      008985 EC               [12]  938 	mov	a,r4
      008986 33               [12]  939 	rlc	a
      008987 95 E0            [12]  940 	subb	a,acc
      008989 FB               [12]  941 	mov	r3,a
      00898A C3               [12]  942 	clr	c
      00898B EC               [12]  943 	mov	a,r4
      00898C 94 02            [12]  944 	subb	a,#0x02
      00898E EB               [12]  945 	mov	a,r3
      00898F 64 80            [12]  946 	xrl	a,#0x80
      008991 94 80            [12]  947 	subb	a,#0x80
      008993 40 2D            [24]  948 	jc	00102$
                                    949 ;	quantum/encoder.c:226: encoder_value[index]++;
      008995 EF               [12]  950 	mov	a,r7
      008996 24 E8            [12]  951 	add	a, #_encoder_value
      008998 FB               [12]  952 	mov	r3,a
      008999 E4               [12]  953 	clr	a
      00899A 34 0B            [12]  954 	addc	a, #(_encoder_value >> 8)
      00899C FC               [12]  955 	mov	r4,a
      00899D 8B 82            [24]  956 	mov	dpl,r3
      00899F 8C 83            [24]  957 	mov	dph,r4
      0089A1 E0               [24]  958 	movx	a,@dptr
      0089A2 FA               [12]  959 	mov	r2,a
      0089A3 0A               [12]  960 	inc	r2
      0089A4 8B 82            [24]  961 	mov	dpl,r3
      0089A6 8C 83            [24]  962 	mov	dph,r4
      0089A8 EA               [12]  963 	mov	a,r2
      0089A9 F0               [24]  964 	movx	@dptr,a
                                    965 ;	quantum/encoder.c:227: changed = true;
      0089AA 90 09 56         [24]  966 	mov	dptr,#_encoder_update_changed_10000_174
      0089AD 74 01            [12]  967 	mov	a,#0x01
      0089AF F0               [24]  968 	movx	@dptr,a
                                    969 ;	quantum/encoder.c:232: encoder_exec_mapping(index, ENCODER_COUNTER_CLOCKWISE);
      0089B0 90 09 3A         [24]  970 	mov	dptr,#_encoder_exec_mapping_PARM_2
      0089B3 E4               [12]  971 	clr	a
      0089B4 F0               [24]  972 	movx	@dptr,a
      0089B5 8F 82            [24]  973 	mov	dpl, r7
      0089B7 C0 06            [24]  974 	push	ar6
      0089B9 C0 05            [24]  975 	push	ar5
      0089BB 12 88 4F         [24]  976 	lcall	_encoder_exec_mapping
      0089BE D0 05            [24]  977 	pop	ar5
      0089C0 D0 06            [24]  978 	pop	ar6
      0089C2                        979 00102$:
                                    980 ;	quantum/encoder.c:241: if (encoder_pulses[i] <= -resolution) { // direction is arbitrary here, but this clockwise
      0089C2 8D 82            [24]  981 	mov	dpl,r5
      0089C4 8E 83            [24]  982 	mov	dph,r6
      0089C6 E0               [24]  983 	movx	a,@dptr
      0089C7 FF               [12]  984 	mov	r7,a
      0089C8 33               [12]  985 	rlc	a
      0089C9 95 E0            [12]  986 	subb	a,acc
      0089CB FC               [12]  987 	mov	r4,a
      0089CC C3               [12]  988 	clr	c
      0089CD 74 FE            [12]  989 	mov	a,#0xfe
      0089CF 9F               [12]  990 	subb	a,r7
      0089D0 74 7F            [12]  991 	mov	a,#(0xff ^ 0x80)
      0089D2 8C F0            [24]  992 	mov	b,r4
      0089D4 63 F0 80         [24]  993 	xrl	b,#0x80
      0089D7 95 F0            [12]  994 	subb	a,b
      0089D9 40 30            [24]  995 	jc	00104$
                                    996 ;	free result
                                    997 ;	quantum/encoder.c:243: encoder_value[index]--;
      0089DB 90 09 55         [24]  998 	mov	dptr,#_encoder_update_index_10000_173
      0089DE E0               [24]  999 	movx	a,@dptr
      0089DF FF               [12] 1000 	mov	r7,a
      0089E0 24 E8            [12] 1001 	add	a, #_encoder_value
      0089E2 FB               [12] 1002 	mov	r3,a
      0089E3 E4               [12] 1003 	clr	a
      0089E4 34 0B            [12] 1004 	addc	a, #(_encoder_value >> 8)
      0089E6 FC               [12] 1005 	mov	r4,a
      0089E7 8B 82            [24] 1006 	mov	dpl,r3
      0089E9 8C 83            [24] 1007 	mov	dph,r4
      0089EB E0               [24] 1008 	movx	a,@dptr
      0089EC FA               [12] 1009 	mov	r2,a
      0089ED 1A               [12] 1010 	dec	r2
      0089EE 8B 82            [24] 1011 	mov	dpl,r3
      0089F0 8C 83            [24] 1012 	mov	dph,r4
      0089F2 EA               [12] 1013 	mov	a,r2
      0089F3 F0               [24] 1014 	movx	@dptr,a
                                   1015 ;	quantum/encoder.c:244: changed = true;
      0089F4 90 09 56         [24] 1016 	mov	dptr,#_encoder_update_changed_10000_174
      0089F7 74 01            [12] 1017 	mov	a,#0x01
      0089F9 F0               [24] 1018 	movx	@dptr,a
                                   1019 ;	quantum/encoder.c:249: encoder_exec_mapping(index, ENCODER_CLOCKWISE);
      0089FA 90 09 3A         [24] 1020 	mov	dptr,#_encoder_exec_mapping_PARM_2
      0089FD F0               [24] 1021 	movx	@dptr,a
      0089FE 8F 82            [24] 1022 	mov	dpl, r7
      008A00 C0 06            [24] 1023 	push	ar6
      008A02 C0 05            [24] 1024 	push	ar5
      008A04 12 88 4F         [24] 1025 	lcall	_encoder_exec_mapping
      008A07 D0 05            [24] 1026 	pop	ar5
      008A09 D0 06            [24] 1027 	pop	ar6
      008A0B                       1028 00104$:
                                   1029 ;	quantum/encoder.c:254: encoder_pulses[i] %= resolution;
      008A0B 8D 82            [24] 1030 	mov	dpl,r5
      008A0D 8E 83            [24] 1031 	mov	dph,r6
      008A0F E0               [24] 1032 	movx	a,@dptr
      008A10 A2 E7            [12] 1033 	mov	c,acc.7
      008A12 54 01            [12] 1034 	anl	a,#0x01
      008A14 60 04            [24] 1035 	jz	00123$
      008A16 50 02            [24] 1036 	jnc	00123$
      008A18 44 FE            [12] 1037 	orl	a,#0xfe
      008A1A                       1038 00123$:
      008A1A 8D 82            [24] 1039 	mov	dpl,r5
      008A1C 8E 83            [24] 1040 	mov	dph,r6
      008A1E F0               [24] 1041 	movx	@dptr,a
                                   1042 ;	quantum/encoder.c:259: return changed;
      008A1F 90 09 56         [24] 1043 	mov	dptr,#_encoder_update_changed_10000_174
      008A22 E0               [24] 1044 	movx	a,@dptr
                                   1045 ;	quantum/encoder.c:260: }
      008A23 F5 82            [12] 1046 	mov	dpl,a
      008A25 22               [24] 1047 	ret
                                   1048 ;------------------------------------------------------------
                                   1049 ;Allocation info for local variables in function 'encoder_read'
                                   1050 ;------------------------------------------------------------
                                   1051 ;changed       Allocated with name '_encoder_read_changed_10000_180'
                                   1052 ;i             Allocated with name '_encoder_read_i_20000_181'
                                   1053 ;new_status    Allocated with name '_encoder_read_new_status_30000_182'
                                   1054 ;------------------------------------------------------------
                                   1055 ;	quantum/encoder.c:262: bool encoder_read(void) {
                                   1056 ;	-----------------------------------------
                                   1057 ;	 function encoder_read
                                   1058 ;	-----------------------------------------
      008A26                       1059 _encoder_read:
                                   1060 ;	quantum/encoder.c:263: bool changed = false;
      008A26 90 09 57         [24] 1061 	mov	dptr,#_encoder_read_changed_10000_180
      008A29 E4               [12] 1062 	clr	a
      008A2A F0               [24] 1063 	movx	@dptr,a
                                   1064 ;	quantum/encoder.c:264: for (uint8_t i = 0; i < thisCount; i++) {
      008A2B FF               [12] 1065 	mov	r7,a
      008A2C                       1066 00105$:
      008A2C 90 09 39         [24] 1067 	mov	dptr,#_thisCount
      008A2F E0               [24] 1068 	movx	a,@dptr
      008A30 FE               [12] 1069 	mov	r6,a
      008A31 C3               [12] 1070 	clr	c
      008A32 EF               [12] 1071 	mov	a,r7
      008A33 9E               [12] 1072 	subb	a,r6
      008A34 50 5A            [24] 1073 	jnc	00103$
                                   1074 ;	quantum/encoder.c:265: uint8_t new_status = (readPin(encoders_pad_a[i]) << 0) | (readPin(encoders_pad_b[i]) << 1);
      008A36 12 8A AB         [24] 1075 	lcall	_ak820_outline_0019
      008A39 12 51 30         [24] 1076 	lcall	_readPin
      008A3C AE 82            [24] 1077 	mov	r6, dpl
      008A3E 12 8A B9         [24] 1078 	lcall	_ak820_outline_0020
      008A41 12 51 30         [24] 1079 	lcall	_readPin
      008A44 E5 82            [12] 1080 	mov	a,dpl
      008A46 25 82            [12] 1081 	add	a,dpl
      008A48 42 06            [12] 1082 	orl	ar6,a
                                   1083 ;	quantum/encoder.c:266: if ((encoder_state[i] & 0x3) != new_status) {
      008A4A EF               [12] 1084 	mov	a,r7
      008A4B 24 E6            [12] 1085 	add	a, #_encoder_state
      008A4D FC               [12] 1086 	mov	r4,a
      008A4E E4               [12] 1087 	clr	a
      008A4F 34 0B            [12] 1088 	addc	a, #(_encoder_state >> 8)
      008A51 FD               [12] 1089 	mov	r5,a
      008A52 8C 82            [24] 1090 	mov	dpl,r4
      008A54 8D 83            [24] 1091 	mov	dph,r5
      008A56 E0               [24] 1092 	movx	a,@dptr
      008A57 FB               [12] 1093 	mov	r3,a
      008A58 FA               [12] 1094 	mov	r2,a
      008A59 53 02 03         [24] 1095 	anl	ar2,#0x03
      008A5C 8E 01            [24] 1096 	mov	ar1,r6
      008A5E EA               [12] 1097 	mov	a,r2
      008A5F B5 01 02         [24] 1098 	cjne	a,ar1,00132$
      008A62 80 29            [24] 1099 	sjmp	00106$
      008A64                       1100 00132$:
                                   1101 ;	quantum/encoder.c:267: encoder_state[i] <<= 2;
      008A64 EB               [12] 1102 	mov	a,r3
      008A65 2B               [12] 1103 	add	a,r3
      008A66 25 E0            [12] 1104 	add	a,acc
      008A68 FB               [12] 1105 	mov	r3,a
      008A69 8C 82            [24] 1106 	mov	dpl,r4
      008A6B 8D 83            [24] 1107 	mov	dph,r5
      008A6D F0               [24] 1108 	movx	@dptr,a
                                   1109 ;	quantum/encoder.c:268: encoder_state[i] |= new_status;
      008A6E EB               [12] 1110 	mov	a,r3
      008A6F 42 06            [12] 1111 	orl	ar6,a
      008A71 8C 82            [24] 1112 	mov	dpl,r4
      008A73 8D 83            [24] 1113 	mov	dph,r5
      008A75 EE               [12] 1114 	mov	a,r6
      008A76 F0               [24] 1115 	movx	@dptr,a
                                   1116 ;	quantum/encoder.c:269: changed |= encoder_update(i, encoder_state[i]);
      008A77 90 09 54         [24] 1117 	mov	dptr,#_encoder_update_PARM_2
      008A7A EE               [12] 1118 	mov	a,r6
      008A7B F0               [24] 1119 	movx	@dptr,a
      008A7C 8F 82            [24] 1120 	mov	dpl, r7
      008A7E C0 07            [24] 1121 	push	ar7
      008A80 12 89 4F         [24] 1122 	lcall	_encoder_update
      008A83 AE 82            [24] 1123 	mov	r6, dpl
      008A85 D0 07            [24] 1124 	pop	ar7
      008A87 90 09 57         [24] 1125 	mov	dptr,#_encoder_read_changed_10000_180
      008A8A E0               [24] 1126 	movx	a,@dptr
      008A8B 4E               [12] 1127 	orl	a,r6
      008A8C F0               [24] 1128 	movx	@dptr,a
      008A8D                       1129 00106$:
                                   1130 ;	quantum/encoder.c:264: for (uint8_t i = 0; i < thisCount; i++) {
      008A8D 0F               [12] 1131 	inc	r7
      008A8E 80 9C            [24] 1132 	sjmp	00105$
      008A90                       1133 00103$:
                                   1134 ;	quantum/encoder.c:272: return changed;
      008A90 90 09 57         [24] 1135 	mov	dptr,#_encoder_read_changed_10000_180
      008A93 E0               [24] 1136 	movx	a,@dptr
                                   1137 ;	quantum/encoder.c:273: }
      008A94 F5 82            [12] 1138 	mov	dpl,a
      008A96 22               [24] 1139 	ret
                                   1140 	.area CSEG    (CODE)
                                   1141 	.area CONST   (CODE)
                                   1142 	.area XINIT   (CODE)
      00BD93                       1143 __xinit__encoders_pad_a:
      00BD93 39                    1144 	.db #0x39	; 57	'9'
      00BD94                       1145 __xinit__encoders_pad_b:
      00BD94 38                    1146 	.db #0x38	; 56	'8'
      00BD95                       1147 __xinit__encoder_LUT:
      00BD95 00                    1148 	.db #0x00	;  0
      00BD96 FF                    1149 	.db #0xff	; -1
      00BD97 01                    1150 	.db #0x01	;  1
      00BD98 00                    1151 	.db #0x00	;  0
      00BD99 01                    1152 	.db #0x01	;  1
      00BD9A 00                    1153 	.db #0x00	;  0
      00BD9B 00                    1154 	.db #0x00	;  0
      00BD9C FF                    1155 	.db #0xff	; -1
      00BD9D FF                    1156 	.db #0xff	; -1
      00BD9E 00                    1157 	.db #0x00	;  0
      00BD9F 00                    1158 	.db #0x00	;  0
      00BDA0 01                    1159 	.db #0x01	;  1
      00BDA1 00                    1160 	.db #0x00	;  0
      00BDA2 01                    1161 	.db #0x01	;  1
      00BDA3 FF                    1162 	.db #0xff	; -1
      00BDA4 00                    1163 	.db #0x00	;  0
      00BDA5                       1164 __xinit__encoder_state:
      00BDA5 00                    1165 	.db #0x00	; 0
      00BDA6                       1166 __xinit__encoder_pulses:
      00BDA6 00                    1167 	.db #0x00	;  0
      00BDA7                       1168 __xinit__encoder_value:
      00BDA7 00                    1169 	.db #0x00	; 0
                                   1170 	.area CABS    (ABS,CODE)
                                   1171 
                                   1172 ; Experimental exact instruction outlining.
                                   1173 	.globl _ak820_outline_0007
                                   1174 	.globl _ak820_outline_0019
                                   1175 	.globl _ak820_outline_0020
                                   1176 
                                   1177 	.area CSEG (CODE)
                                   1178 ; function ak820_outline_0007
      008A97                       1179 _ak820_outline_0007:
      008A97 A3               [24] 1180 	inc	dptr
      008A98 F0               [24] 1181 	movx	@dptr,a
      008A99 E4               [12] 1182 	clr	a
      008A9A A3               [24] 1183 	inc	dptr
      008A9B F0               [24] 1184 	movx	@dptr,a
      008A9C 90 0B 92         [24] 1185 	mov	dptr,#___memcpy_PARM_3
      008A9F 74 06            [12] 1186 	mov	a,#0x06
      008AA1 F0               [24] 1187 	movx	@dptr,a
      008AA2 E4               [12] 1188 	clr	a
      008AA3 A3               [24] 1189 	inc	dptr
      008AA4 F0               [24] 1190 	movx	@dptr,a
      008AA5 90 07 3B         [24] 1191 	mov	dptr,#_action_exec_PARM_1
      008AA8 F5 F0            [12] 1192 	mov	b,a
      008AAA 22               [24] 1193 	ret
                                   1194 
                                   1195 	.area CSEG (CODE)
                                   1196 ; function ak820_outline_0019
      008AAB                       1197 _ak820_outline_0019:
      008AAB EF               [12] 1198 	mov	a,r7
      008AAC 24 D4            [12] 1199 	add	a,#_encoders_pad_a
      008AAE F5 82            [12] 1200 	mov	dpl,a
      008AB0 E4               [12] 1201 	clr	a
      008AB1 34 0B            [12] 1202 	addc	a,#(_encoders_pad_a>>8)
      008AB3 F5 83            [12] 1203 	mov	dph,a
      008AB5 E0               [24] 1204 	movx	a,@dptr
      008AB6 F5 82            [12] 1205 	mov	dpl,a
      008AB8 22               [24] 1206 	ret
                                   1207 
                                   1208 	.area CSEG (CODE)
                                   1209 ; function ak820_outline_0020
      008AB9                       1210 _ak820_outline_0020:
      008AB9 EF               [12] 1211 	mov	a,r7
      008ABA 24 D5            [12] 1212 	add	a,#_encoders_pad_b
      008ABC F5 82            [12] 1213 	mov	dpl,a
      008ABE E4               [12] 1214 	clr	a
      008ABF 34 0B            [12] 1215 	addc	a,#(_encoders_pad_b>>8)
      008AC1 F5 83            [12] 1216 	mov	dph,a
      008AC3 E0               [24] 1217 	movx	a,@dptr
      008AC4 F5 82            [12] 1218 	mov	dpl,a
      008AC6 22               [24] 1219 	ret
