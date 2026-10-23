                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module magic
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _magic
                                     12 	.globl _bootmagic
                                     13 	.globl _layer_state_set_kb
                                     14 	.globl _default_layer_set
                                     15 	.globl _eeconfig_read_keymap
                                     16 	.globl _eeconfig_read_default_layer
                                     17 	.globl _eeconfig_read_debug
                                     18 	.globl _eeconfig_init
                                     19 	.globl _eeconfig_is_enabled
                                     20 	.globl _ADC_START
                                     21 	.globl _S0_R_FIFO
                                     22 	.globl _S0_T_FIFO
                                     23 	.globl _S0_FREE
                                     24 	.globl _S0_IF_BYTE
                                     25 	.globl _S0_IF_FIRST
                                     26 	.globl _S0_IF_OV
                                     27 	.globl _S0_FST_ACT
                                     28 	.globl _CP_RL2
                                     29 	.globl _C_T2
                                     30 	.globl _TR2
                                     31 	.globl _EXEN2
                                     32 	.globl _TCLK
                                     33 	.globl _RCLK
                                     34 	.globl _EXF2
                                     35 	.globl _CAP1F
                                     36 	.globl _TF2
                                     37 	.globl _RI
                                     38 	.globl _TI
                                     39 	.globl _RB8
                                     40 	.globl _TB8
                                     41 	.globl _REN
                                     42 	.globl _SM2
                                     43 	.globl _SM1
                                     44 	.globl _SM0
                                     45 	.globl _IT0
                                     46 	.globl _IE0
                                     47 	.globl _IT1
                                     48 	.globl _IE1
                                     49 	.globl _TR0
                                     50 	.globl _TF0
                                     51 	.globl _TR1
                                     52 	.globl _TF1
                                     53 	.globl _P4_0
                                     54 	.globl _P4_1
                                     55 	.globl _P4_2
                                     56 	.globl _P4_3
                                     57 	.globl _P4_4
                                     58 	.globl _P4_5
                                     59 	.globl _P4_6
                                     60 	.globl _RXD
                                     61 	.globl _TXD
                                     62 	.globl _INT0
                                     63 	.globl _INT1
                                     64 	.globl _T0
                                     65 	.globl _T1
                                     66 	.globl _MOSI1
                                     67 	.globl _MISO1
                                     68 	.globl _SCK1
                                     69 	.globl _P3_0
                                     70 	.globl _P3_1
                                     71 	.globl _P3_2
                                     72 	.globl _P3_3
                                     73 	.globl _P3_4
                                     74 	.globl _P3_5
                                     75 	.globl _P3_6
                                     76 	.globl _P3_7
                                     77 	.globl _CAP1_
                                     78 	.globl _T2_
                                     79 	.globl _CAP2_
                                     80 	.globl _T2EX_
                                     81 	.globl _RXD1
                                     82 	.globl _TXD1
                                     83 	.globl _P2_0
                                     84 	.globl _P2_1
                                     85 	.globl _P2_2
                                     86 	.globl _P2_3
                                     87 	.globl _P2_4
                                     88 	.globl _P2_5
                                     89 	.globl _P2_6
                                     90 	.globl _P2_7
                                     91 	.globl _AIN0
                                     92 	.globl _AIN1
                                     93 	.globl _AIN2
                                     94 	.globl _AIN3
                                     95 	.globl _AIN4
                                     96 	.globl _AIN5
                                     97 	.globl _AIN6
                                     98 	.globl _AIN7
                                     99 	.globl _CAP1
                                    100 	.globl _T2
                                    101 	.globl _CAP2
                                    102 	.globl _T2EX
                                    103 	.globl _INT0_
                                    104 	.globl _SCS
                                    105 	.globl _MOSI
                                    106 	.globl _MISO
                                    107 	.globl _SCK
                                    108 	.globl _RXD1_
                                    109 	.globl _TXD1_
                                    110 	.globl _P1_0
                                    111 	.globl _P1_1
                                    112 	.globl _P1_2
                                    113 	.globl _P1_3
                                    114 	.globl _P1_4
                                    115 	.globl _P1_5
                                    116 	.globl _P1_6
                                    117 	.globl _P1_7
                                    118 	.globl _AIN8
                                    119 	.globl _AIN9
                                    120 	.globl _AIN10
                                    121 	.globl _AIN11
                                    122 	.globl _AIN12
                                    123 	.globl _AIN13
                                    124 	.globl _RXD_
                                    125 	.globl _TXD_
                                    126 	.globl _SCL0
                                    127 	.globl _SDA0
                                    128 	.globl _P0_0
                                    129 	.globl _P0_1
                                    130 	.globl _P0_2
                                    131 	.globl _P0_3
                                    132 	.globl _P0_4
                                    133 	.globl _P0_5
                                    134 	.globl _P0_6
                                    135 	.globl _P0_7
                                    136 	.globl _IE_SPI0
                                    137 	.globl _IE_USB
                                    138 	.globl _IE_ADC
                                    139 	.globl _IE_UART1
                                    140 	.globl _IE_PWM_I2C
                                    141 	.globl _IE_GPIO
                                    142 	.globl _IE_WDOG
                                    143 	.globl _PX0
                                    144 	.globl _PT0
                                    145 	.globl _PX1
                                    146 	.globl _PT1
                                    147 	.globl _PS
                                    148 	.globl _PT2
                                    149 	.globl _PL_FLAG
                                    150 	.globl _PH_FLAG
                                    151 	.globl _EX0
                                    152 	.globl _ET0
                                    153 	.globl _EX1
                                    154 	.globl _ET1
                                    155 	.globl _ES
                                    156 	.globl _ET2
                                    157 	.globl _E_DIS
                                    158 	.globl _EA
                                    159 	.globl _P
                                    160 	.globl _F1
                                    161 	.globl _OV
                                    162 	.globl _RS0
                                    163 	.globl _RS1
                                    164 	.globl _F0
                                    165 	.globl _AC
                                    166 	.globl _CY
                                    167 	.globl _I2CS_INT_ST
                                    168 	.globl _I2CX_INT
                                    169 	.globl _LED_STATUS
                                    170 	.globl _LED_DMA_H
                                    171 	.globl _LED_DMA_L
                                    172 	.globl _LED_DMA
                                    173 	.globl _LED_PWM_OE
                                    174 	.globl _LED_COMMON
                                    175 	.globl _ADC_CHAN
                                    176 	.globl _ADC_DAT_H
                                    177 	.globl _ADC_DAT_L
                                    178 	.globl _ADC_DAT
                                    179 	.globl _ADC_CTRL
                                    180 	.globl _SPI1_CK_SE
                                    181 	.globl _SPI1_CTRL
                                    182 	.globl _SPI1_DATA
                                    183 	.globl _SPI1_STAT
                                    184 	.globl _SIF1
                                    185 	.globl _SBAUD1
                                    186 	.globl _SBUF1
                                    187 	.globl _SCON1
                                    188 	.globl _SPI0_SETUP
                                    189 	.globl _SPI0_CK_SE
                                    190 	.globl _SPI0_CTRL
                                    191 	.globl _SPI0_DATA
                                    192 	.globl _SPI0_STAT
                                    193 	.globl _T2CAP1H
                                    194 	.globl _T2CAP1L
                                    195 	.globl _T2CAP1
                                    196 	.globl _TH2
                                    197 	.globl _TL2
                                    198 	.globl _T2COUNT
                                    199 	.globl _RCAP2H
                                    200 	.globl _RCAP2L
                                    201 	.globl _RCAP2
                                    202 	.globl _T2MOD
                                    203 	.globl _T2CON
                                    204 	.globl _SBUF
                                    205 	.globl _SCON
                                    206 	.globl _TH1
                                    207 	.globl _TH0
                                    208 	.globl _TL1
                                    209 	.globl _TL0
                                    210 	.globl _TMOD
                                    211 	.globl _TCON
                                    212 	.globl _XBUS_AUX
                                    213 	.globl _P7
                                    214 	.globl _P6_DIR
                                    215 	.globl _P6_OUT_PU
                                    216 	.globl _P6_IN
                                    217 	.globl _P5_DIR
                                    218 	.globl _P5_OUT_PU
                                    219 	.globl _P5_IN
                                    220 	.globl _P4_LED_KEY
                                    221 	.globl _P4_DIR_PU
                                    222 	.globl _P4_MOD_OC
                                    223 	.globl _P4
                                    224 	.globl _P3_DIR_PU
                                    225 	.globl _P3_MOD_OC
                                    226 	.globl _P3
                                    227 	.globl _P2_DIR_PU
                                    228 	.globl _P2_MOD_OC
                                    229 	.globl _P2
                                    230 	.globl _P1_DIR_PU
                                    231 	.globl _P1_MOD_OC
                                    232 	.globl _P1
                                    233 	.globl _P0_DIR_PU
                                    234 	.globl _P0_MOD_OC
                                    235 	.globl _P0
                                    236 	.globl _ROM_CTRL
                                    237 	.globl _ROM_DATA_HH
                                    238 	.globl _ROM_DATA_HL
                                    239 	.globl _ROM_DATA_HI
                                    240 	.globl _ROM_ADDR_H
                                    241 	.globl _ROM_ADDR_L
                                    242 	.globl _ROM_ADDR
                                    243 	.globl _GPIO_IE
                                    244 	.globl _IP_EX
                                    245 	.globl _IE_EX
                                    246 	.globl _IP
                                    247 	.globl _IE
                                    248 	.globl _WDOG_COUNT
                                    249 	.globl _RESET_KEEP
                                    250 	.globl _WAKE_CTRL
                                    251 	.globl _CLOCK_CFG
                                    252 	.globl _POWER_CFG
                                    253 	.globl _PCON
                                    254 	.globl _GLOBAL_CFG
                                    255 	.globl _SAFE_MOD
                                    256 	.globl _DPH
                                    257 	.globl _DPL
                                    258 	.globl _SP
                                    259 	.globl _A_INV
                                    260 	.globl _B
                                    261 	.globl _ACC
                                    262 	.globl _PSW
                                    263 	.globl _keymap_config
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
      0008BD                        550 _keymap_config::
      0008BD                        551 	.ds 2
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
                                    589 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_123'
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
                                    601 ;	 function magic
                                    602 ;	-----------------------------------------
      00790A                        603 _magic:
                                    604 ;	quantum/bootmagic/magic.c:40: if (!eeconfig_is_enabled()) {
      00790A 12 87 54         [24]  605 	lcall	_eeconfig_is_enabled
      00790D E5 82            [12]  606 	mov	a, dpl
      00790F 70 03            [24]  607 	jnz	00102$
                                    608 ;	quantum/bootmagic/magic.c:41: eeconfig_init();
      007911 12 87 3D         [24]  609 	lcall	_eeconfig_init
      007914                        610 00102$:
                                    611 ;	quantum/bootmagic/magic.c:45: debug_config.raw  = eeconfig_read_debug();
      007914 12 87 83         [24]  612 	lcall	_eeconfig_read_debug
      007917 AF 82            [24]  613 	mov	r7, dpl
      007919 90 0B FE         [24]  614 	mov	dptr,#_debug_config
      00791C EF               [12]  615 	mov	a,r7
      00791D F0               [24]  616 	movx	@dptr,a
                                    617 ;	quantum/bootmagic/magic.c:46: keymap_config.raw = eeconfig_read_keymap();
      00791E 12 87 95         [24]  618 	lcall	_eeconfig_read_keymap
      007921 AE 82            [24]  619 	mov	r6, dpl
      007923 AF 83            [24]  620 	mov	r7, dph
      007925 90 08 BD         [24]  621 	mov	dptr,#_keymap_config
      007928 EE               [12]  622 	mov	a,r6
      007929 F0               [24]  623 	movx	@dptr,a
      00792A EF               [12]  624 	mov	a,r7
      00792B A3               [24]  625 	inc	dptr
      00792C F0               [24]  626 	movx	@dptr,a
                                    627 ;	quantum/bootmagic/magic.c:48: bootmagic();
      00792D 12 79 07         [24]  628 	lcall	_bootmagic
                                    629 ;	quantum/bootmagic/magic.c:51: layer_state_t default_layer = (layer_state_t)eeconfig_read_default_layer();
      007930 12 87 8C         [24]  630 	lcall	_eeconfig_read_default_layer
                                    631 ;	quantum/bootmagic/magic.c:52: default_layer_set(default_layer);
      007933 12 74 1A         [24]  632 	lcall	_default_layer_set
                                    633 ;	quantum/bootmagic/magic.c:55: layer_state_set_kb((layer_state_t)layer_state);
      007936 90 0B AE         [24]  634 	mov	dptr,#_layer_state
      007939 E0               [24]  635 	movx	a,@dptr
      00793A F5 82            [12]  636 	mov	dpl,a
                                    637 ;	quantum/bootmagic/magic.c:56: }
      00793C 02 74 6C         [24]  638 	ljmp	_layer_state_set_kb
                                    639 	.area CSEG    (CODE)
                                    640 	.area CONST   (CODE)
                                    641 	.area XINIT   (CODE)
                                    642 	.area CABS    (ABS,CODE)
