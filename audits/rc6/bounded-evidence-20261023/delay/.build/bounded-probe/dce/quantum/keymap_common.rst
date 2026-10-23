                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module keymap_common
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _KEYCODE2CONSUMER
                                     12 	.globl _keycode_at_encodermap_location
                                     13 	.globl _keycode_at_keymap_location
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
                                    257 	.globl _keymap_key_to_keycode_PARM_2
                                    258 	.globl _action_for_key_PARM_2
                                    259 	.globl _action_for_key
                                    260 	.globl _action_for_keycode
                                    261 	.globl _keymap_key_to_keycode
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
      000986                        548 _action_for_key_PARM_2:
      000986                        549 	.ds 2
      000988                        550 _action_for_key_layer_10000_301:
      000988                        551 	.ds 1
      000989                        552 _action_for_keycode_keycode_10000_303:
      000989                        553 	.ds 2
      00098B                        554 _action_for_keycode_kind_10000_304:
      00098B                        555 	.ds 1
      00098C                        556 _action_for_keycode_mods_10000_304:
      00098C                        557 	.ds 1
      00098D                        558 _action_for_keycode___400000076_40000_306:
      00098D                        559 	.ds 2
      00098F                        560 _action_for_keycode_key_60000_320:
      00098F                        561 	.ds 1
      000990                        562 _keymap_key_to_keycode_PARM_2:
      000990                        563 	.ds 2
      000992                        564 _keymap_key_to_keycode_layer_10000_323:
      000992                        565 	.ds 1
                                    566 ;--------------------------------------------------------
                                    567 ; absolute external ram data
                                    568 ;--------------------------------------------------------
                                    569 	.area XABS    (ABS,XDATA)
                                    570 ;--------------------------------------------------------
                                    571 ; initialized external ram data
                                    572 ;--------------------------------------------------------
                                    573 	.area XISEG   (XDATA)
                                    574 	.area HOME    (CODE)
                                    575 	.area GSINIT0 (CODE)
                                    576 	.area GSINIT1 (CODE)
                                    577 	.area GSINIT2 (CODE)
                                    578 	.area GSINIT3 (CODE)
                                    579 	.area GSINIT4 (CODE)
                                    580 	.area GSINIT5 (CODE)
                                    581 	.area GSINIT  (CODE)
                                    582 	.area GSFINAL (CODE)
                                    583 	.area CSEG    (CODE)
                                    584 ;--------------------------------------------------------
                                    585 ; global & static initialisations
                                    586 ;--------------------------------------------------------
                                    587 	.area HOME    (CODE)
                                    588 	.area GSINIT  (CODE)
                                    589 	.area GSFINAL (CODE)
                                    590 	.area GSINIT  (CODE)
                                    591 ;--------------------------------------------------------
                                    592 ; Home
                                    593 ;--------------------------------------------------------
                                    594 	.area HOME    (CODE)
                                    595 	.area HOME    (CODE)
                                    596 ;--------------------------------------------------------
                                    597 ; code
                                    598 ;--------------------------------------------------------
                                    599 	.area CSEG    (CODE)
                                    600 ;------------------------------------------------------------
                                    601 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    602 ;------------------------------------------------------------
                                    603 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_107'
                                    604 ;------------------------------------------------------------
                                    605 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    606 ;	-----------------------------------------
                           000007   607 	ar7 = 0x07
                           000006   608 	ar6 = 0x06
                           000005   609 	ar5 = 0x05
                           000004   610 	ar4 = 0x04
                           000003   611 	ar3 = 0x03
                           000002   612 	ar2 = 0x02
                           000001   613 	ar1 = 0x01
                           000000   614 	ar0 = 0x00
                                    615 ;	 function action_for_key
                                    616 ;	-----------------------------------------
      008D9D                        617 _action_for_key:
      008D9D E5 82            [12]  618 	mov	a,dpl
      008D9F 90 09 88         [24]  619 	mov	dptr,#_action_for_key_layer_10000_301
      008DA2 F0               [24]  620 	movx	@dptr,a
                                    621 ;	quantum/keymap_common.c:59: uint16_t keycode = keymap_key_to_keycode(layer, key);
      008DA3 E0               [24]  622 	movx	a,@dptr
      008DA4 FF               [12]  623 	mov	r7,a
      008DA5 90 0B 90         [24]  624 	mov	dptr,#___memcpy_PARM_2
      008DA8 74 86            [12]  625 	mov	a,#_action_for_key_PARM_2
      008DAA F0               [24]  626 	movx	@dptr,a
      008DAB 74 09            [12]  627 	mov	a,#(_action_for_key_PARM_2 >> 8)
      008DAD A3               [24]  628 	inc	dptr
      008DAE F0               [24]  629 	movx	@dptr,a
      008DAF E4               [12]  630 	clr	a
      008DB0 A3               [24]  631 	inc	dptr
      008DB1 F0               [24]  632 	movx	@dptr,a
      008DB2 90 0B 93         [24]  633 	mov	dptr,#___memcpy_PARM_3
      008DB5 74 02            [12]  634 	mov	a,#0x02
      008DB7 F0               [24]  635 	movx	@dptr,a
      008DB8 E4               [12]  636 	clr	a
      008DB9 A3               [24]  637 	inc	dptr
      008DBA F0               [24]  638 	movx	@dptr,a
      008DBB 90 09 90         [24]  639 	mov	dptr,#_keymap_key_to_keycode_PARM_2
      008DBE F5 F0            [12]  640 	mov	b,a
      008DC0 C0 07            [24]  641 	push	ar7
      008DC2 12 B4 C1         [24]  642 	lcall	___memcpy
      008DC5 D0 07            [24]  643 	pop	ar7
      008DC7 8F 82            [24]  644 	mov	dpl, r7
      008DC9 12 8F 7D         [24]  645 	lcall	_keymap_key_to_keycode
                                    646 ;	quantum/keymap_common.c:61: return action_for_keycode(keycode);
      008DCC AF 83            [24]  647 	mov  r7,dph
                                    648 ;	quantum/keymap_common.c:62: }
      008DCE 02 8D D1         [24]  649 	ljmp	_action_for_keycode
                                    650 ;------------------------------------------------------------
                                    651 ;Allocation info for local variables in function 'action_for_keycode'
                                    652 ;------------------------------------------------------------
                                    653 ;keycode       Allocated with name '_action_for_keycode_keycode_10000_303'
                                    654 ;kind          Allocated with name '_action_for_keycode_kind_10000_304'
                                    655 ;key           Allocated with name '_action_for_keycode_key_10000_304'
                                    656 ;mods          Allocated with name '_action_for_keycode_mods_10000_304'
                                    657 ;__400000076   Allocated with name '_action_for_keycode___400000076_40000_306'
                                    658 ;__500000077   Allocated with name '_action_for_keycode___500000077_50000_319'
                                    659 ;key           Allocated with name '_action_for_keycode_key_60000_320'
                                    660 ;layer         Allocated with name '_action_for_keycode_layer_30000_314'
                                    661 ;------------------------------------------------------------
                                    662 ;	quantum/keymap_common.c:64: uint16_t action_for_keycode(uint16_t keycode) {
                                    663 ;	-----------------------------------------
                                    664 ;	 function action_for_keycode
                                    665 ;	-----------------------------------------
      008DD1                        666 _action_for_keycode:
      008DD1 AF 83            [24]  667 	mov	r7,dph
      008DD3 E5 82            [12]  668 	mov	a,dpl
      008DD5 90 09 89         [24]  669 	mov	dptr,#_action_for_keycode_keycode_10000_303
      008DD8 F0               [24]  670 	movx	@dptr,a
      008DD9 EF               [12]  671 	mov	a,r7
      008DDA A3               [24]  672 	inc	dptr
      008DDB F0               [24]  673 	movx	@dptr,a
                                    674 ;	quantum/keymap_common.c:87: uint8_t kind = (uint8_t)(keycode >> 8);
      008DDC 90 09 89         [24]  675 	mov	dptr,#_action_for_keycode_keycode_10000_303
      008DDF E0               [24]  676 	movx	a,@dptr
      008DE0 FE               [12]  677 	mov	r6,a
      008DE1 A3               [24]  678 	inc	dptr
      008DE2 E0               [24]  679 	movx	a,@dptr
      008DE3 FF               [12]  680 	mov	r7,a
                                    681 ;	quantum/keymap_common.c:88: uint8_t key = (uint8_t)keycode;
                                    682 ;	quantum/keymap_common.c:90: if (!kind) {
      008DE4 FD               [12]  683 	mov	r5,a
      008DE5 8E 04            [24]  684 	mov	ar4,r6
      008DE7 60 03            [24]  685 	jz	00270$
      008DE9 02 8E 92         [24]  686 	ljmp	00117$
      008DEC                        687 00270$:
                                    688 ;	quantum/keymap_common.c:91: if ((key >= KC_A && key <= KC_EXSEL) ||
      008DEC BC 04 00         [24]  689 	cjne	r4,#0x04,00271$
      008DEF                        690 00271$:
      008DEF 40 05            [24]  691 	jc	00105$
      008DF1 EC               [12]  692 	mov	a,r4
      008DF2 24 5B            [12]  693 	add	a,#0xff - 0xa4
      008DF4 50 0D            [24]  694 	jnc	00101$
                                    695 ;	free result
      008DF6                        696 00105$:
                                    697 ;	quantum/keymap_common.c:92: (key >= KC_LEFT_CTRL && key <= KC_RIGHT_GUI) || key == KC_TRANSPARENT)
      008DF6 BC E0 00         [24]  698 	cjne	r4,#0xe0,00274$
      008DF9                        699 00274$:
      008DF9 40 05            [24]  700 	jc	00106$
      008DFB EC               [12]  701 	mov	a,r4
      008DFC 24 18            [12]  702 	add	a,#0xff - 0xe7
      008DFE 50 03            [24]  703 	jnc	00101$
                                    704 ;	free result
      008E00                        705 00106$:
      008E00 BC 01 09         [24]  706 	cjne	r4,#0x01,00102$
      008E03                        707 00101$:
                                    708 ;	quantum/keymap_common.c:93: return ACTION_KEY(key);
      008E03 8C 02            [24]  709 	mov	ar2,r4
      008E05 7B 00            [12]  710 	mov	r3,#0x00
      008E07 8A 82            [24]  711 	mov	dpl, r2
      008E09 8B 83            [24]  712 	mov	dph, r3
      008E0B 22               [24]  713 	ret
      008E0C                        714 00102$:
                                    715 ;	quantum/keymap_common.c:95: if (key >= KC_SYSTEM_POWER && key <= KC_SYSTEM_WAKE)
      008E0C BC A5 00         [24]  716 	cjne	r4,#0xa5,00279$
      008E0F                        717 00279$:
      008E0F 40 4C            [24]  718 	jc	00108$
      008E11 EC               [12]  719 	mov	a,r4
      008E12 24 58            [12]  720 	add	a,#0xff - 0xa7
      008E14 40 47            [24]  721 	jc	00108$
                                    722 ;	free result
                                    723 ;	tmk_core/protocol/report.h:263: switch (key) {
      008E16 BC A5 02         [24]  724 	cjne	r4,#0xa5,00282$
      008E19 80 0A            [24]  725 	sjmp	00136$
      008E1B                        726 00282$:
      008E1B BC A6 02         [24]  727 	cjne	r4,#0xa6,00283$
      008E1E 80 10            [24]  728 	sjmp	00137$
      008E20                        729 00283$:
                                    730 ;	tmk_core/protocol/report.h:264: case KC_SYSTEM_POWER:
      008E20 BC A7 23         [24]  731 	cjne	r4,#0xa7,00139$
      008E23 80 16            [24]  732 	sjmp	00138$
      008E25                        733 00136$:
                                    734 ;	tmk_core/protocol/report.h:265: return SYSTEM_POWER_DOWN;
      008E25 90 09 8D         [24]  735 	mov	dptr,#_action_for_keycode___400000076_40000_306
      008E28 74 81            [12]  736 	mov	a,#0x81
      008E2A F0               [24]  737 	movx	@dptr,a
      008E2B E4               [12]  738 	clr	a
      008E2C A3               [24]  739 	inc	dptr
      008E2D F0               [24]  740 	movx	@dptr,a
                                    741 ;	tmk_core/protocol/report.h:266: case KC_SYSTEM_SLEEP:
      008E2E 80 1D            [24]  742 	sjmp	00141$
      008E30                        743 00137$:
                                    744 ;	tmk_core/protocol/report.h:267: return SYSTEM_SLEEP;
      008E30 90 09 8D         [24]  745 	mov	dptr,#_action_for_keycode___400000076_40000_306
      008E33 74 82            [12]  746 	mov	a,#0x82
      008E35 F0               [24]  747 	movx	@dptr,a
      008E36 E4               [12]  748 	clr	a
      008E37 A3               [24]  749 	inc	dptr
      008E38 F0               [24]  750 	movx	@dptr,a
                                    751 ;	tmk_core/protocol/report.h:268: case KC_SYSTEM_WAKE:
      008E39 80 12            [24]  752 	sjmp	00141$
      008E3B                        753 00138$:
                                    754 ;	tmk_core/protocol/report.h:269: return SYSTEM_WAKE_UP;
      008E3B 90 09 8D         [24]  755 	mov	dptr,#_action_for_keycode___400000076_40000_306
      008E3E 74 83            [12]  756 	mov	a,#0x83
      008E40 F0               [24]  757 	movx	@dptr,a
      008E41 E4               [12]  758 	clr	a
      008E42 A3               [24]  759 	inc	dptr
      008E43 F0               [24]  760 	movx	@dptr,a
                                    761 ;	tmk_core/protocol/report.h:270: default:
      008E44 80 07            [24]  762 	sjmp	00141$
      008E46                        763 00139$:
                                    764 ;	tmk_core/protocol/report.h:271: return 0;
      008E46 90 09 8D         [24]  765 	mov	dptr,#_action_for_keycode___400000076_40000_306
      008E49 E4               [12]  766 	clr	a
      008E4A F0               [24]  767 	movx	@dptr,a
      008E4B A3               [24]  768 	inc	dptr
      008E4C F0               [24]  769 	movx	@dptr,a
                                    770 ;	quantum/keymap_common.c:96: return ACTION_USAGE_SYSTEM(KEYCODE2SYSTEM(key));
      008E4D                        771 00141$:
      008E4D 90 09 8D         [24]  772 	mov	dptr,#_action_for_keycode___400000076_40000_306
      008E50 E0               [24]  773 	movx	a,@dptr
      008E51 FA               [12]  774 	mov	r2,a
      008E52 A3               [24]  775 	inc	dptr
      008E53 E0               [24]  776 	movx	a,@dptr
      008E54 FB               [12]  777 	mov	r3,a
      008E55 43 03 40         [24]  778 	orl	ar3,#0x40
      008E58 8A 82            [24]  779 	mov	dpl, r2
      008E5A 8B 83            [24]  780 	mov	dph, r3
      008E5C 22               [24]  781 	ret
      008E5D                        782 00108$:
                                    783 ;	quantum/keymap_common.c:97: if (key >= KC_AUDIO_MUTE && key <= KC_LAUNCHPAD)
      008E5D BC A8 00         [24]  784 	cjne	r4,#0xa8,00285$
      008E60                        785 00285$:
      008E60 40 16            [24]  786 	jc	00111$
      008E62 EC               [12]  787 	mov	a,r4
      008E63 24 3D            [12]  788 	add	a,#0xff - 0xc2
      008E65 40 11            [24]  789 	jc	00111$
                                    790 ;	free result
                                    791 ;	quantum/keymap_common.c:98: return ACTION_USAGE_CONSUMER(KEYCODE2CONSUMER(key));
      008E67 8C 82            [24]  792 	mov	dpl, r4
      008E69 12 68 D2         [24]  793 	lcall	_KEYCODE2CONSUMER
      008E6C AA 82            [24]  794 	mov	r2, dpl
      008E6E AB 83            [24]  795 	mov	r3, dph
      008E70 43 03 44         [24]  796 	orl	ar3,#0x44
      008E73 8A 82            [24]  797 	mov	dpl, r2
      008E75 8B 83            [24]  798 	mov	dph, r3
      008E77 22               [24]  799 	ret
      008E78                        800 00111$:
                                    801 ;	quantum/keymap_common.c:100: if (key >= KC_MS_UP && key <= KC_MS_ACCEL2) return ACTION_MOUSEKEY(key);
      008E78 BC CD 00         [24]  802 	cjne	r4,#0xcd,00288$
      008E7B                        803 00288$:
      008E7B 40 11            [24]  804 	jc	00114$
      008E7D EC               [12]  805 	mov	a,r4
      008E7E 24 20            [12]  806 	add	a,#0xff - 0xdf
      008E80 40 0C            [24]  807 	jc	00114$
                                    808 ;	free result
      008E82 8C 02            [24]  809 	mov	ar2,r4
      008E84 7B 00            [12]  810 	mov	r3,#0x00
      008E86 43 03 50         [24]  811 	orl	ar3,#0x50
      008E89 8A 82            [24]  812 	mov	dpl, r2
      008E8B 8B 83            [24]  813 	mov	dph, r3
      008E8D 22               [24]  814 	ret
      008E8E                        815 00114$:
                                    816 ;	quantum/keymap_common.c:101: return ACTION_NO;
      008E8E 90 00 00         [24]  817 	mov	dptr,#0x0000
      008E91 22               [24]  818 	ret
      008E92                        819 00117$:
                                    820 ;	quantum/keymap_common.c:103: if (kind < 0x20) return keycode; /* Encoded modifier+basic actions. */
      008E92 BD 20 00         [24]  821 	cjne	r5,#0x20,00291$
      008E95                        822 00291$:
      008E95 50 05            [24]  823 	jnc	00119$
      008E97 8E 82            [24]  824 	mov	dpl, r6
      008E99 8F 83            [24]  825 	mov	dph, r7
      008E9B 22               [24]  826 	ret
      008E9C                        827 00119$:
                                    828 ;	quantum/keymap_common.c:104: if (kind < 0x50) return ACTION_KEY(key); /* MT and LT: existing tap-only fallback. */
      008E9C BD 50 00         [24]  829 	cjne	r5,#0x50,00293$
      008E9F                        830 00293$:
      008E9F 50 09            [24]  831 	jnc	00121$
      008EA1 8C 06            [24]  832 	mov	ar6,r4
      008EA3 7F 00            [12]  833 	mov	r7,#0x00
      008EA5 8E 82            [24]  834 	mov	dpl, r6
      008EA7 8F 83            [24]  835 	mov	dph, r7
      008EA9 22               [24]  836 	ret
      008EAA                        837 00121$:
                                    838 ;	quantum/keymap_common.c:105: if (kind < 0x52) {
      008EAA BD 52 00         [24]  839 	cjne	r5,#0x52,00295$
      008EAD                        840 00295$:
      008EAD 50 3A            [24]  841 	jnc	00125$
                                    842 ;	quantum/keymap_common.c:106: uint8_t layer = ((kind & 1u) << 3) | (key >> 5);
      008EAF 74 01            [12]  843 	mov	a,#0x01
      008EB1 5D               [12]  844 	anl	a,r5
      008EB2 C4               [12]  845 	swap	a
      008EB3 03               [12]  846 	rr	a
      008EB4 54 F8            [12]  847 	anl	a,#0xf8
      008EB6 FF               [12]  848 	mov	r7,a
      008EB7 EC               [12]  849 	mov	a,r4
      008EB8 C4               [12]  850 	swap	a
      008EB9 03               [12]  851 	rr	a
      008EBA 54 07            [12]  852 	anl	a,#0x07
      008EBC 42 07            [12]  853 	orl	ar7,a
                                    854 ;	quantum/keymap_common.c:107: mods = key & 0x1f;
      008EBE 74 1F            [12]  855 	mov	a,#0x1f
      008EC0 5C               [12]  856 	anl	a,r4
      008EC1 FE               [12]  857 	mov	r6,a
      008EC2 90 09 8C         [24]  858 	mov	dptr,#_action_for_keycode_mods_10000_304
      008EC5 F0               [24]  859 	movx	@dptr,a
                                    860 ;	quantum/keymap_common.c:108: if (mods & 0x10) mods <<= 4; /* Discard the 5-bit right-mod marker. */
      008EC6 EE               [12]  861 	mov	a,r6
      008EC7 30 E4 08         [24]  862 	jnb	acc.4,00123$
      008ECA EE               [12]  863 	mov	a,r6
      008ECB C4               [12]  864 	swap	a
      008ECC 54 F0            [12]  865 	anl	a,#0xf0
      008ECE 90 09 8C         [24]  866 	mov	dptr,#_action_for_keycode_mods_10000_304
      008ED1 F0               [24]  867 	movx	@dptr,a
      008ED2                        868 00123$:
                                    869 ;	quantum/keymap_common.c:109: return ACTION_LAYER_MODS(layer, mods);
      008ED2 8F 06            [24]  870 	mov	ar6,r7
      008ED4 7F 00            [12]  871 	mov	r7,#0x00
      008ED6 90 09 8C         [24]  872 	mov	dptr,#_action_for_keycode_mods_10000_304
      008ED9 E0               [24]  873 	movx	a,@dptr
      008EDA 7B 00            [12]  874 	mov	r3,#0x00
      008EDC 42 07            [12]  875 	orl	ar7,a
      008EDE EB               [12]  876 	mov	a,r3
      008EDF 42 06            [12]  877 	orl	ar6,a
      008EE1 43 06 90         [24]  878 	orl	ar6,#0x90
      008EE4 8F 82            [24]  879 	mov	dpl, r7
      008EE6 8E 83            [24]  880 	mov	dph, r6
      008EE8 22               [24]  881 	ret
      008EE9                        882 00125$:
                                    883 ;	quantum/keymap_common.c:111: if (kind != 0x52) return ACTION_NO;
      008EE9 BD 52 02         [24]  884 	cjne	r5,#0x52,00298$
      008EEC 80 04            [24]  885 	sjmp	00127$
      008EEE                        886 00298$:
      008EEE 90 00 00         [24]  887 	mov	dptr,#0x0000
      008EF1 22               [24]  888 	ret
      008EF2                        889 00127$:
                                    890 ;	quantum/keymap_common.c:112: mods = key & 0x1f;
      008EF2 74 1F            [12]  891 	mov	a,#0x1f
      008EF4 5C               [12]  892 	anl	a,r4
      008EF5 FF               [12]  893 	mov	r7,a
                                    894 ;	quantum/keymap_common.c:113: switch (key >> 5) {
      008EF6 EC               [12]  895 	mov	a,r4
      008EF7 C4               [12]  896 	swap	a
      008EF8 03               [12]  897 	rr	a
      008EF9 54 07            [12]  898 	anl	a,#0x07
      008EFB FE               [12]  899 	mov  r6,a
      008EFC 24 F9            [12]  900 	add	a,#0xff - 0x06
      008EFE 40 49            [24]  901 	jc	00134$
                                    902 ;	free result
      008F00 EE               [12]  903 	mov	a,r6
      008F01 2E               [12]  904 	add	a,r6
                                    905 ;	quantum/keymap_common.c:114: case 0: kind = (ACT_LAYER << 4) | (OP_BIT_SET << 2) | ON_PRESS; break;
      008F02 90 8F 06         [24]  906 	mov	dptr,#00300$
      008F05 73               [24]  907 	jmp	@a+dptr
      008F06                        908 00300$:
      008F06 80 0C            [24]  909 	sjmp	00128$
      008F08 80 12            [24]  910 	sjmp	00129$
      008F0A 80 21            [24]  911 	sjmp	00130$
      008F0C 80 27            [24]  912 	sjmp	00132$
      008F0E 80 39            [24]  913 	sjmp	00134$
      008F10 80 2B            [24]  914 	sjmp	00133$
      008F12 80 21            [24]  915 	sjmp	00132$
      008F14                        916 00128$:
      008F14 90 09 8B         [24]  917 	mov	dptr,#_action_for_keycode_kind_10000_304
      008F17 74 8D            [12]  918 	mov	a,#0x8d
      008F19 F0               [24]  919 	movx	@dptr,a
                                    920 ;	quantum/keymap_common.c:115: case 1: return ACTION_LAYER_MOMENTARY(mods);
      008F1A 80 31            [24]  921 	sjmp	00135$
      008F1C                        922 00129$:
      008F1C 8F 05            [24]  923 	mov	ar5,r7
      008F1E 8D 06            [24]  924 	mov	ar6,r5
      008F20 7D 00            [12]  925 	mov	r5,#0x00
      008F22 43 05 F1         [24]  926 	orl	ar5,#0xf1
      008F25 43 06 A0         [24]  927 	orl	ar6,#0xa0
      008F28 8D 82            [24]  928 	mov	dpl, r5
      008F2A 8E 83            [24]  929 	mov	dph, r6
                                    930 ;	quantum/keymap_common.c:116: case 2: kind = (ACT_LAYER << 4) | (OP_BIT_SET << 2); break;
      008F2C 22               [24]  931 	ret
      008F2D                        932 00130$:
      008F2D 90 09 8B         [24]  933 	mov	dptr,#_action_for_keycode_kind_10000_304
      008F30 74 8C            [12]  934 	mov	a,#0x8c
      008F32 F0               [24]  935 	movx	@dptr,a
                                    936 ;	quantum/keymap_common.c:118: case 6: kind = (ACT_LAYER << 4) | (OP_BIT_XOR << 2) | ON_RELEASE; break;
      008F33 80 18            [24]  937 	sjmp	00135$
      008F35                        938 00132$:
      008F35 90 09 8B         [24]  939 	mov	dptr,#_action_for_keycode_kind_10000_304
      008F38 74 8A            [12]  940 	mov	a,#0x8a
      008F3A F0               [24]  941 	movx	@dptr,a
                                    942 ;	quantum/keymap_common.c:119: case 5: return ACTION_MODS(mods); /* Existing held-mod fallback for OSM. */
      008F3B 80 10            [24]  943 	sjmp	00135$
      008F3D                        944 00133$:
      008F3D 53 07 1F         [24]  945 	anl	ar7,#0x1f
      008F40 8F 06            [24]  946 	mov	ar6,r7
      008F42 7F 00            [12]  947 	mov	r7,#0x00
      008F44 8F 82            [24]  948 	mov	dpl, r7
      008F46 8E 83            [24]  949 	mov	dph, r6
                                    950 ;	quantum/keymap_common.c:120: default: return ACTION_NO;
      008F48 22               [24]  951 	ret
      008F49                        952 00134$:
      008F49 90 00 00         [24]  953 	mov	dptr,#0x0000
                                    954 ;	quantum/keymap_common.c:121: }
      008F4C 22               [24]  955 	ret
      008F4D                        956 00135$:
                                    957 ;	quantum/keymap_common.c:123: key = ((key & 0x1c) << 3) | (1u << (key & 3));
      008F4D 8C 07            [24]  958 	mov	ar7,r4
      008F4F 53 07 1C         [24]  959 	anl	ar7,#0x1c
      008F52 EF               [12]  960 	mov	a,r7
      008F53 C4               [12]  961 	swap	a
      008F54 03               [12]  962 	rr	a
      008F55 54 F8            [12]  963 	anl	a,#0xf8
      008F57 FF               [12]  964 	mov	r7,a
      008F58 74 03            [12]  965 	mov	a,#0x03
      008F5A 5C               [12]  966 	anl	a,r4
      008F5B F5 F0            [12]  967 	mov	b,a
      008F5D 05 F0            [12]  968 	inc	b
      008F5F 74 01            [12]  969 	mov	a,#0x01
      008F61 80 02            [24]  970 	sjmp	00302$
      008F63                        971 00301$:
      008F63 25 E0            [12]  972 	add	a,acc
      008F65                        973 00302$:
      008F65 D5 F0 FB         [24]  974 	djnz	b,00301$
      008F68 42 07            [12]  975 	orl	ar7,a
                                    976 ;	quantum/keymap_common.c:124: return ((uint16_t)kind << 8) | key;
      008F6A 90 09 8B         [24]  977 	mov	dptr,#_action_for_keycode_kind_10000_304
      008F6D E0               [24]  978 	movx	a,@dptr
      008F6E FE               [12]  979 	mov	r6,a
      008F6F E4               [12]  980 	clr	a
      008F70 FD               [12]  981 	mov	r5,a
      008F71 FC               [12]  982 	mov	r4,a
      008F72 EF               [12]  983 	mov	a,r7
      008F73 42 05            [12]  984 	orl	ar5,a
      008F75 EC               [12]  985 	mov	a,r4
      008F76 42 06            [12]  986 	orl	ar6,a
      008F78 8D 82            [24]  987 	mov	dpl, r5
      008F7A 8E 83            [24]  988 	mov	dph, r6
                                    989 ;	quantum/keymap_common.c:269: }
      008F7C 22               [24]  990 	ret
                                    991 ;------------------------------------------------------------
                                    992 ;Allocation info for local variables in function 'keymap_key_to_keycode'
                                    993 ;------------------------------------------------------------
                                    994 ;key           Allocated with name '_keymap_key_to_keycode_PARM_2'
                                    995 ;layer         Allocated with name '_keymap_key_to_keycode_layer_10000_323'
                                    996 ;------------------------------------------------------------
                                    997 ;	quantum/keymap_common.c:272: __attribute__((weak)) uint16_t keymap_key_to_keycode(uint8_t layer, keypos_t key) {
                                    998 ;	-----------------------------------------
                                    999 ;	 function keymap_key_to_keycode
                                   1000 ;	-----------------------------------------
      008F7D                       1001 _keymap_key_to_keycode:
      008F7D E5 82            [12] 1002 	mov	a,dpl
      008F7F 90 09 92         [24] 1003 	mov	dptr,#_keymap_key_to_keycode_layer_10000_323
      008F82 F0               [24] 1004 	movx	@dptr,a
                                   1005 ;	quantum/keymap_common.c:277: if (vial_unlock_in_progress) {
      008F83 90 0C 09         [24] 1006 	mov	dptr,#_vial_unlock_in_progress
      008F86 E0               [24] 1007 	movx	a,@dptr
      008F87 60 04            [24] 1008 	jz	00102$
                                   1009 ;	quantum/keymap_common.c:278: return KC_NO;
      008F89 90 00 00         [24] 1010 	mov	dptr,#0x0000
      008F8C 22               [24] 1011 	ret
      008F8D                       1012 00102$:
                                   1013 ;	quantum/keymap_common.c:280: if (key.row == VIAL_MATRIX_MAGIC && key.col == VIAL_MATRIX_MAGIC) {
      008F8D 90 09 91         [24] 1014 	mov	dptr,#(_keymap_key_to_keycode_PARM_2 + 0x0001)
      008F90 E0               [24] 1015 	movx	a,@dptr
      008F91 FF               [12] 1016 	mov	r7,a
      008F92 BF F0 15         [24] 1017 	cjne	r7,#0xf0,00104$
      008F95 90 09 90         [24] 1018 	mov	dptr,#_keymap_key_to_keycode_PARM_2
      008F98 E0               [24] 1019 	movx	a,@dptr
      008F99 FE               [12] 1020 	mov	r6,a
      008F9A BE F0 0D         [24] 1021 	cjne	r6,#0xf0,00104$
                                   1022 ;	quantum/keymap_common.c:281: return g_vial_magic_keycode_override;
      008F9D 90 0A 68         [24] 1023 	mov	dptr,#_g_vial_magic_keycode_override
      008FA0 E0               [24] 1024 	movx	a,@dptr
      008FA1 FD               [12] 1025 	mov	r5,a
      008FA2 A3               [24] 1026 	inc	dptr
      008FA3 E0               [24] 1027 	movx	a,@dptr
      008FA4 FE               [12] 1028 	mov	r6,a
      008FA5 8D 82            [24] 1029 	mov	dpl, r5
      008FA7 8E 83            [24] 1030 	mov	dph, r6
      008FA9 22               [24] 1031 	ret
      008FAA                       1032 00104$:
                                   1033 ;	quantum/keymap_common.c:284: if (key.row < MATRIX_ROWS && key.col < MATRIX_COLS) {
      008FAA BF 10 00         [24] 1034 	cjne	r7,#0x10,00187$
      008FAD                       1035 00187$:
      008FAD 50 1E            [24] 1036 	jnc	00114$
      008FAF 90 09 90         [24] 1037 	mov	dptr,#_keymap_key_to_keycode_PARM_2
      008FB2 E0               [24] 1038 	movx	a,@dptr
      008FB3 FE               [12] 1039 	mov	r6,a
      008FB4 BE 08 00         [24] 1040 	cjne	r6,#0x08,00189$
      008FB7                       1041 00189$:
      008FB7 50 14            [24] 1042 	jnc	00114$
                                   1043 ;	quantum/keymap_common.c:286: return keycode_at_keymap_location(layer, key.row, key.col);
      008FB9 90 09 92         [24] 1044 	mov	dptr,#_keymap_key_to_keycode_layer_10000_323
      008FBC E0               [24] 1045 	movx	a,@dptr
      008FBD FD               [12] 1046 	mov	r5,a
      008FBE 90 09 0A         [24] 1047 	mov	dptr,#_keycode_at_keymap_location_PARM_2
      008FC1 EF               [12] 1048 	mov	a,r7
      008FC2 F0               [24] 1049 	movx	@dptr,a
      008FC3 90 09 0B         [24] 1050 	mov	dptr,#_keycode_at_keymap_location_PARM_3
      008FC6 EE               [12] 1051 	mov	a,r6
      008FC7 F0               [24] 1052 	movx	@dptr,a
      008FC8 8D 82            [24] 1053 	mov	dpl, r5
      008FCA 02 81 AE         [24] 1054 	ljmp	_keycode_at_keymap_location
      008FCD                       1055 00114$:
                                   1056 ;	quantum/keymap_common.c:289: else if (key.row == KEYLOC_ENCODER_CW && key.col < NUM_ENCODERS) {
      008FCD BF FD 1E         [24] 1057 	cjne	r7,#0xfd,00110$
      008FD0 90 09 90         [24] 1058 	mov	dptr,#_keymap_key_to_keycode_PARM_2
      008FD3 E0               [24] 1059 	movx	a,@dptr
      008FD4 FE               [12] 1060 	mov	r6,a
      008FD5 BE 01 00         [24] 1061 	cjne	r6,#0x01,00193$
      008FD8                       1062 00193$:
      008FD8 50 14            [24] 1063 	jnc	00110$
                                   1064 ;	quantum/keymap_common.c:290: return keycode_at_encodermap_location(layer, key.col, true);
      008FDA 90 09 92         [24] 1065 	mov	dptr,#_keymap_key_to_keycode_layer_10000_323
      008FDD E0               [24] 1066 	movx	a,@dptr
      008FDE FE               [12] 1067 	mov	r6,a
      008FDF 90 09 0D         [24] 1068 	mov	dptr,#_keycode_at_encodermap_location_PARM_2
      008FE2 E4               [12] 1069 	clr	a
      008FE3 F0               [24] 1070 	movx	@dptr,a
      008FE4 90 09 0E         [24] 1071 	mov	dptr,#_keycode_at_encodermap_location_PARM_3
      008FE7 04               [12] 1072 	inc	a
      008FE8 F0               [24] 1073 	movx	@dptr,a
      008FE9 8E 82            [24] 1074 	mov	dpl, r6
      008FEB 02 81 E2         [24] 1075 	ljmp	_keycode_at_encodermap_location
      008FEE                       1076 00110$:
                                   1077 ;	quantum/keymap_common.c:291: } else if (key.row == KEYLOC_ENCODER_CCW && key.col < NUM_ENCODERS) {
      008FEE BF FC 1D         [24] 1078 	cjne	r7,#0xfc,00115$
      008FF1 90 09 90         [24] 1079 	mov	dptr,#_keymap_key_to_keycode_PARM_2
      008FF4 E0               [24] 1080 	movx	a,@dptr
      008FF5 FF               [12] 1081 	mov	r7,a
      008FF6 BF 01 00         [24] 1082 	cjne	r7,#0x01,00197$
      008FF9                       1083 00197$:
      008FF9 50 13            [24] 1084 	jnc	00115$
                                   1085 ;	quantum/keymap_common.c:292: return keycode_at_encodermap_location(layer, key.col, false);
      008FFB 90 09 92         [24] 1086 	mov	dptr,#_keymap_key_to_keycode_layer_10000_323
      008FFE E0               [24] 1087 	movx	a,@dptr
      008FFF FF               [12] 1088 	mov	r7,a
      009000 90 09 0D         [24] 1089 	mov	dptr,#_keycode_at_encodermap_location_PARM_2
      009003 E4               [12] 1090 	clr	a
      009004 F0               [24] 1091 	movx	@dptr,a
      009005 90 09 0E         [24] 1092 	mov	dptr,#_keycode_at_encodermap_location_PARM_3
      009008 F0               [24] 1093 	movx	@dptr,a
      009009 8F 82            [24] 1094 	mov	dpl, r7
      00900B 02 81 E2         [24] 1095 	ljmp	_keycode_at_encodermap_location
      00900E                       1096 00115$:
                                   1097 ;	quantum/keymap_common.c:295: return KC_NO;
      00900E 90 00 00         [24] 1098 	mov	dptr,#0x0000
                                   1099 ;	quantum/keymap_common.c:296: }
      009011 22               [24] 1100 	ret
                                   1101 	.area CSEG    (CODE)
                                   1102 	.area CONST   (CODE)
                                   1103 	.area XINIT   (CODE)
                                   1104 	.area CABS    (ABS,CODE)
