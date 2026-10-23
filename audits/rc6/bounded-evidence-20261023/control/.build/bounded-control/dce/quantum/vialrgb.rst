                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module vialrgb
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _rgb_matrix_get_speed
                                     12 	.globl _rgb_matrix_set_speed_noeeprom
                                     13 	.globl _rgb_matrix_get_val
                                     14 	.globl _rgb_matrix_get_sat
                                     15 	.globl _rgb_matrix_get_hue
                                     16 	.globl _rgb_matrix_sethsv_noeeprom
                                     17 	.globl _rgb_matrix_get_mode
                                     18 	.globl _rgb_matrix_mode_noeeprom
                                     19 	.globl _rgb_matrix_is_enabled
                                     20 	.globl _rgb_matrix_disable_noeeprom
                                     21 	.globl _rgb_matrix_enable_noeeprom
                                     22 	.globl _eeconfig_update_rgb_matrix
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
                                    266 	.globl _vialrgb_save_PARM_2
                                    267 	.globl _vialrgb_set_value_PARM_2
                                    268 	.globl _vialrgb_get_value_PARM_2
                                    269 	.globl _g_direct_mode_colors
                                    270 	.globl _vialrgb_get_value
                                    271 	.globl _vialrgb_set_value
                                    272 	.globl _vialrgb_save
                                    273 ;--------------------------------------------------------
                                    274 ; special function registers
                                    275 ;--------------------------------------------------------
                                    276 	.area RSEG    (ABS,DATA)
      000000                        277 	.org 0x0000
                           0000D0   278 _PSW	=	0x00d0
                           0000E0   279 _ACC	=	0x00e0
                           0000F0   280 _B	=	0x00f0
                           0000FD   281 _A_INV	=	0x00fd
                           000081   282 _SP	=	0x0081
                           000082   283 _DPL	=	0x0082
                           000083   284 _DPH	=	0x0083
                           0000A1   285 _SAFE_MOD	=	0x00a1
                           0000B1   286 _GLOBAL_CFG	=	0x00b1
                           000087   287 _PCON	=	0x0087
                           0000BA   288 _POWER_CFG	=	0x00ba
                           0000B9   289 _CLOCK_CFG	=	0x00b9
                           0000A9   290 _WAKE_CTRL	=	0x00a9
                           0000FE   291 _RESET_KEEP	=	0x00fe
                           0000FF   292 _WDOG_COUNT	=	0x00ff
                           0000A8   293 _IE	=	0x00a8
                           0000B8   294 _IP	=	0x00b8
                           0000E8   295 _IE_EX	=	0x00e8
                           0000E9   296 _IP_EX	=	0x00e9
                           0000B2   297 _GPIO_IE	=	0x00b2
                           008584   298 _ROM_ADDR	=	0x8584
                           000084   299 _ROM_ADDR_L	=	0x0084
                           000085   300 _ROM_ADDR_H	=	0x0085
                           008F8E   301 _ROM_DATA_HI	=	0x8f8e
                           00008E   302 _ROM_DATA_HL	=	0x008e
                           00008F   303 _ROM_DATA_HH	=	0x008f
                           000086   304 _ROM_CTRL	=	0x0086
                           000080   305 _P0	=	0x0080
                           0000C4   306 _P0_MOD_OC	=	0x00c4
                           0000C5   307 _P0_DIR_PU	=	0x00c5
                           000090   308 _P1	=	0x0090
                           000092   309 _P1_MOD_OC	=	0x0092
                           000093   310 _P1_DIR_PU	=	0x0093
                           0000A0   311 _P2	=	0x00a0
                           000094   312 _P2_MOD_OC	=	0x0094
                           000095   313 _P2_DIR_PU	=	0x0095
                           0000B0   314 _P3	=	0x00b0
                           000096   315 _P3_MOD_OC	=	0x0096
                           000097   316 _P3_DIR_PU	=	0x0097
                           0000C0   317 _P4	=	0x00c0
                           0000C2   318 _P4_MOD_OC	=	0x00c2
                           0000C3   319 _P4_DIR_PU	=	0x00c3
                           0000C1   320 _P4_LED_KEY	=	0x00c1
                           0000AA   321 _P5_IN	=	0x00aa
                           0000AB   322 _P5_OUT_PU	=	0x00ab
                           0000AC   323 _P5_DIR	=	0x00ac
                           0000AD   324 _P6_IN	=	0x00ad
                           0000AE   325 _P6_OUT_PU	=	0x00ae
                           0000AF   326 _P6_DIR	=	0x00af
                           0000F1   327 _P7	=	0x00f1
                           0000A2   328 _XBUS_AUX	=	0x00a2
                           000088   329 _TCON	=	0x0088
                           000089   330 _TMOD	=	0x0089
                           00008A   331 _TL0	=	0x008a
                           00008B   332 _TL1	=	0x008b
                           00008C   333 _TH0	=	0x008c
                           00008D   334 _TH1	=	0x008d
                           000098   335 _SCON	=	0x0098
                           000099   336 _SBUF	=	0x0099
                           0000C8   337 _T2CON	=	0x00c8
                           0000C9   338 _T2MOD	=	0x00c9
                           00CBCA   339 _RCAP2	=	0xcbca
                           0000CA   340 _RCAP2L	=	0x00ca
                           0000CB   341 _RCAP2H	=	0x00cb
                           00CDCC   342 _T2COUNT	=	0xcdcc
                           0000CC   343 _TL2	=	0x00cc
                           0000CD   344 _TH2	=	0x00cd
                           00CFCE   345 _T2CAP1	=	0xcfce
                           0000CE   346 _T2CAP1L	=	0x00ce
                           0000CF   347 _T2CAP1H	=	0x00cf
                           0000F8   348 _SPI0_STAT	=	0x00f8
                           0000F9   349 _SPI0_DATA	=	0x00f9
                           0000FA   350 _SPI0_CTRL	=	0x00fa
                           0000FB   351 _SPI0_CK_SE	=	0x00fb
                           0000FC   352 _SPI0_SETUP	=	0x00fc
                           0000BC   353 _SCON1	=	0x00bc
                           0000BD   354 _SBUF1	=	0x00bd
                           0000BE   355 _SBAUD1	=	0x00be
                           0000BF   356 _SIF1	=	0x00bf
                           0000B4   357 _SPI1_STAT	=	0x00b4
                           0000B5   358 _SPI1_DATA	=	0x00b5
                           0000B6   359 _SPI1_CTRL	=	0x00b6
                           0000B7   360 _SPI1_CK_SE	=	0x00b7
                           0000F3   361 _ADC_CTRL	=	0x00f3
                           00F5F4   362 _ADC_DAT	=	0xf5f4
                           0000F4   363 _ADC_DAT_L	=	0x00f4
                           0000F5   364 _ADC_DAT_H	=	0x00f5
                           0000F6   365 _ADC_CHAN	=	0x00f6
                           0000A6   366 _LED_COMMON	=	0x00a6
                           0000A7   367 _LED_PWM_OE	=	0x00a7
                           00C7C6   368 _LED_DMA	=	0xc7c6
                           0000C6   369 _LED_DMA_L	=	0x00c6
                           0000C7   370 _LED_DMA_H	=	0x00c7
                           0000F7   371 _LED_STATUS	=	0x00f7
                           0000B3   372 _I2CX_INT	=	0x00b3
                           0000BB   373 _I2CS_INT_ST	=	0x00bb
                                    374 ;--------------------------------------------------------
                                    375 ; special function bits
                                    376 ;--------------------------------------------------------
                                    377 	.area RSEG    (ABS,DATA)
      000000                        378 	.org 0x0000
                           0000D7   379 _CY	=	0x00d7
                           0000D6   380 _AC	=	0x00d6
                           0000D5   381 _F0	=	0x00d5
                           0000D4   382 _RS1	=	0x00d4
                           0000D3   383 _RS0	=	0x00d3
                           0000D2   384 _OV	=	0x00d2
                           0000D1   385 _F1	=	0x00d1
                           0000D0   386 _P	=	0x00d0
                           0000AF   387 _EA	=	0x00af
                           0000AE   388 _E_DIS	=	0x00ae
                           0000AD   389 _ET2	=	0x00ad
                           0000AC   390 _ES	=	0x00ac
                           0000AB   391 _ET1	=	0x00ab
                           0000AA   392 _EX1	=	0x00aa
                           0000A9   393 _ET0	=	0x00a9
                           0000A8   394 _EX0	=	0x00a8
                           0000BF   395 _PH_FLAG	=	0x00bf
                           0000BE   396 _PL_FLAG	=	0x00be
                           0000BD   397 _PT2	=	0x00bd
                           0000BC   398 _PS	=	0x00bc
                           0000BB   399 _PT1	=	0x00bb
                           0000BA   400 _PX1	=	0x00ba
                           0000B9   401 _PT0	=	0x00b9
                           0000B8   402 _PX0	=	0x00b8
                           0000EF   403 _IE_WDOG	=	0x00ef
                           0000EE   404 _IE_GPIO	=	0x00ee
                           0000ED   405 _IE_PWM_I2C	=	0x00ed
                           0000EC   406 _IE_UART1	=	0x00ec
                           0000EB   407 _IE_ADC	=	0x00eb
                           0000E9   408 _IE_USB	=	0x00e9
                           0000E8   409 _IE_SPI0	=	0x00e8
                           000087   410 _P0_7	=	0x0087
                           000086   411 _P0_6	=	0x0086
                           000085   412 _P0_5	=	0x0085
                           000084   413 _P0_4	=	0x0084
                           000083   414 _P0_3	=	0x0083
                           000082   415 _P0_2	=	0x0082
                           000081   416 _P0_1	=	0x0081
                           000080   417 _P0_0	=	0x0080
                           000081   418 _SDA0	=	0x0081
                           000080   419 _SCL0	=	0x0080
                           000083   420 _TXD_	=	0x0083
                           000082   421 _RXD_	=	0x0082
                           000085   422 _AIN13	=	0x0085
                           000084   423 _AIN12	=	0x0084
                           000083   424 _AIN11	=	0x0083
                           000082   425 _AIN10	=	0x0082
                           000081   426 _AIN9	=	0x0081
                           000080   427 _AIN8	=	0x0080
                           000097   428 _P1_7	=	0x0097
                           000096   429 _P1_6	=	0x0096
                           000095   430 _P1_5	=	0x0095
                           000094   431 _P1_4	=	0x0094
                           000093   432 _P1_3	=	0x0093
                           000092   433 _P1_2	=	0x0092
                           000091   434 _P1_1	=	0x0091
                           000090   435 _P1_0	=	0x0090
                           000097   436 _TXD1_	=	0x0097
                           000096   437 _RXD1_	=	0x0096
                           000097   438 _SCK	=	0x0097
                           000096   439 _MISO	=	0x0096
                           000095   440 _MOSI	=	0x0095
                           000094   441 _SCS	=	0x0094
                           000092   442 _INT0_	=	0x0092
                           000091   443 _T2EX	=	0x0091
                           000091   444 _CAP2	=	0x0091
                           000090   445 _T2	=	0x0090
                           000090   446 _CAP1	=	0x0090
                           000097   447 _AIN7	=	0x0097
                           000096   448 _AIN6	=	0x0096
                           000095   449 _AIN5	=	0x0095
                           000094   450 _AIN4	=	0x0094
                           000093   451 _AIN3	=	0x0093
                           000092   452 _AIN2	=	0x0092
                           000091   453 _AIN1	=	0x0091
                           000090   454 _AIN0	=	0x0090
                           0000A7   455 _P2_7	=	0x00a7
                           0000A6   456 _P2_6	=	0x00a6
                           0000A5   457 _P2_5	=	0x00a5
                           0000A4   458 _P2_4	=	0x00a4
                           0000A3   459 _P2_3	=	0x00a3
                           0000A2   460 _P2_2	=	0x00a2
                           0000A1   461 _P2_1	=	0x00a1
                           0000A0   462 _P2_0	=	0x00a0
                           0000A7   463 _TXD1	=	0x00a7
                           0000A6   464 _RXD1	=	0x00a6
                           0000A5   465 _T2EX_	=	0x00a5
                           0000A5   466 _CAP2_	=	0x00a5
                           0000A4   467 _T2_	=	0x00a4
                           0000A4   468 _CAP1_	=	0x00a4
                           0000B7   469 _P3_7	=	0x00b7
                           0000B6   470 _P3_6	=	0x00b6
                           0000B5   471 _P3_5	=	0x00b5
                           0000B4   472 _P3_4	=	0x00b4
                           0000B3   473 _P3_3	=	0x00b3
                           0000B2   474 _P3_2	=	0x00b2
                           0000B1   475 _P3_1	=	0x00b1
                           0000B0   476 _P3_0	=	0x00b0
                           0000B7   477 _SCK1	=	0x00b7
                           0000B6   478 _MISO1	=	0x00b6
                           0000B5   479 _MOSI1	=	0x00b5
                           0000B5   480 _T1	=	0x00b5
                           0000B4   481 _T0	=	0x00b4
                           0000B3   482 _INT1	=	0x00b3
                           0000B2   483 _INT0	=	0x00b2
                           0000B1   484 _TXD	=	0x00b1
                           0000B0   485 _RXD	=	0x00b0
                           0000C6   486 _P4_6	=	0x00c6
                           0000C5   487 _P4_5	=	0x00c5
                           0000C4   488 _P4_4	=	0x00c4
                           0000C3   489 _P4_3	=	0x00c3
                           0000C2   490 _P4_2	=	0x00c2
                           0000C1   491 _P4_1	=	0x00c1
                           0000C0   492 _P4_0	=	0x00c0
                           00008F   493 _TF1	=	0x008f
                           00008E   494 _TR1	=	0x008e
                           00008D   495 _TF0	=	0x008d
                           00008C   496 _TR0	=	0x008c
                           00008B   497 _IE1	=	0x008b
                           00008A   498 _IT1	=	0x008a
                           000089   499 _IE0	=	0x0089
                           000088   500 _IT0	=	0x0088
                           00009F   501 _SM0	=	0x009f
                           00009E   502 _SM1	=	0x009e
                           00009D   503 _SM2	=	0x009d
                           00009C   504 _REN	=	0x009c
                           00009B   505 _TB8	=	0x009b
                           00009A   506 _RB8	=	0x009a
                           000099   507 _TI	=	0x0099
                           000098   508 _RI	=	0x0098
                           0000CF   509 _TF2	=	0x00cf
                           0000CF   510 _CAP1F	=	0x00cf
                           0000CE   511 _EXF2	=	0x00ce
                           0000CD   512 _RCLK	=	0x00cd
                           0000CC   513 _TCLK	=	0x00cc
                           0000CB   514 _EXEN2	=	0x00cb
                           0000CA   515 _TR2	=	0x00ca
                           0000C9   516 _C_T2	=	0x00c9
                           0000C8   517 _CP_RL2	=	0x00c8
                           0000FF   518 _S0_FST_ACT	=	0x00ff
                           0000FE   519 _S0_IF_OV	=	0x00fe
                           0000FD   520 _S0_IF_FIRST	=	0x00fd
                           0000FC   521 _S0_IF_BYTE	=	0x00fc
                           0000FB   522 _S0_FREE	=	0x00fb
                           0000FA   523 _S0_T_FIFO	=	0x00fa
                           0000F8   524 _S0_R_FIFO	=	0x00f8
                           0000F7   525 _ADC_START	=	0x00f7
                                    526 ;--------------------------------------------------------
                                    527 ; overlayable register banks
                                    528 ;--------------------------------------------------------
                                    529 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        530 	.ds 8
                                    531 ;--------------------------------------------------------
                                    532 ; internal ram data
                                    533 ;--------------------------------------------------------
                                    534 	.area DSEG    (DATA)
      000053                        535 _fast_set_leds_sloc0_1_0:
      000053                        536 	.ds 2
      000055                        537 _fast_set_leds_sloc1_1_0:
      000055                        538 	.ds 2
      000057                        539 _vialrgb_get_value_sloc0_1_0:
      000057                        540 	.ds 2
      000059                        541 _vialrgb_get_value_sloc1_1_0:
      000059                        542 	.ds 2
      00005B                        543 _vialrgb_set_value_sloc0_1_0:
      00005B                        544 	.ds 2
                                    545 ;--------------------------------------------------------
                                    546 ; overlayable items in internal ram
                                    547 ;--------------------------------------------------------
                                    548 ;--------------------------------------------------------
                                    549 ; indirectly addressable internal ram data
                                    550 ;--------------------------------------------------------
                                    551 	.area ISEG    (DATA)
                                    552 ;--------------------------------------------------------
                                    553 ; absolute internal ram data
                                    554 ;--------------------------------------------------------
                                    555 	.area IABS    (ABS,DATA)
                                    556 	.area IABS    (ABS,DATA)
                                    557 ;--------------------------------------------------------
                                    558 ; bit data
                                    559 ;--------------------------------------------------------
                                    560 	.area BSEG    (BIT)
                                    561 ;--------------------------------------------------------
                                    562 ; paged external ram data
                                    563 ;--------------------------------------------------------
                                    564 	.area PSEG    (PAG,XDATA)
                                    565 ;--------------------------------------------------------
                                    566 ; uninitialized external ram data
                                    567 ;--------------------------------------------------------
                                    568 	.area XSEG    (XDATA)
      000A7C                        569 _g_direct_mode_colors::
      000A7C                        570 	.ds 246
      000B72                        571 _get_supported_PARM_2:
      000B72                        572 	.ds 1
      000B73                        573 _get_supported_args_10000_251:
      000B73                        574 	.ds 2
      000B75                        575 _qmk_id_to_vialrgb_id_id_10000_258:
      000B75                        576 	.ds 2
      000B77                        577 _vialrgb_id_to_qmk_id_id_10000_263:
      000B77                        578 	.ds 2
      000B79                        579 _set_mode_mode_10000_271:
      000B79                        580 	.ds 2
      000B7B                        581 _get_matrix_pos_for_led_PARM_2:
      000B7B                        582 	.ds 2
      000B7D                        583 _get_matrix_pos_for_led_led_10000_276:
      000B7D                        584 	.ds 2
      000B7F                        585 _fast_set_leds_PARM_2:
      000B7F                        586 	.ds 1
      000B80                        587 _fast_set_leds_args_10000_278:
      000B80                        588 	.ds 2
      000B82                        589 _fast_set_leds_first_index_10001_281:
      000B82                        590 	.ds 2
      000B84                        591 _fast_set_leds_num_leds_10001_281:
      000B84                        592 	.ds 1
      000B85                        593 _vialrgb_get_value_PARM_2:
      000B85                        594 	.ds 1
      000B86                        595 _vialrgb_get_value_data_10000_287:
      000B86                        596 	.ds 3
      000B89                        597 _vialrgb_set_value_PARM_2:
      000B89                        598 	.ds 1
      000B8A                        599 _vialrgb_set_value_data_10000_298:
      000B8A                        600 	.ds 3
      000B8D                        601 _vialrgb_save_PARM_2:
      000B8D                        602 	.ds 1
                                    603 ;--------------------------------------------------------
                                    604 ; absolute external ram data
                                    605 ;--------------------------------------------------------
                                    606 	.area XABS    (ABS,XDATA)
                                    607 ;--------------------------------------------------------
                                    608 ; initialized external ram data
                                    609 ;--------------------------------------------------------
                                    610 	.area XISEG   (XDATA)
                                    611 	.area HOME    (CODE)
                                    612 	.area GSINIT0 (CODE)
                                    613 	.area GSINIT1 (CODE)
                                    614 	.area GSINIT2 (CODE)
                                    615 	.area GSINIT3 (CODE)
                                    616 	.area GSINIT4 (CODE)
                                    617 	.area GSINIT5 (CODE)
                                    618 	.area GSINIT  (CODE)
                                    619 	.area GSFINAL (CODE)
                                    620 	.area CSEG    (CODE)
                                    621 ;--------------------------------------------------------
                                    622 ; global & static initialisations
                                    623 ;--------------------------------------------------------
                                    624 	.area HOME    (CODE)
                                    625 	.area GSINIT  (CODE)
                                    626 	.area GSFINAL (CODE)
                                    627 	.area GSINIT  (CODE)
                                    628 ;--------------------------------------------------------
                                    629 ; Home
                                    630 ;--------------------------------------------------------
                                    631 	.area HOME    (CODE)
                                    632 	.area HOME    (CODE)
                                    633 ;--------------------------------------------------------
                                    634 ; code
                                    635 ;--------------------------------------------------------
                                    636 	.area CSEG    (CODE)
                                    637 ;------------------------------------------------------------
                                    638 ;Allocation info for local variables in function 'rgb_matrix_check_finished_leds'
                                    639 ;------------------------------------------------------------
                                    640 ;led_idx       Allocated with name '_rgb_matrix_check_finished_leds_led_idx_10000_167'
                                    641 ;------------------------------------------------------------
                                    642 ;	quantum/rgb_matrix/rgb_matrix.h:260: static inline bool rgb_matrix_check_finished_leds(uint8_t led_idx) {
                                    643 ;	-----------------------------------------
                           000007   644 	ar7 = 0x07
                           000006   645 	ar6 = 0x06
                           000005   646 	ar5 = 0x05
                           000004   647 	ar4 = 0x04
                           000003   648 	ar3 = 0x03
                           000002   649 	ar2 = 0x02
                           000001   650 	ar1 = 0x01
                           000000   651 	ar0 = 0x00
                                    652 ;	 function get_supported
                                    653 ;	-----------------------------------------
      00AE85                        654 _get_supported:
      00AE85 AF 83            [24]  655 	mov	r7,dph
      00AE87 E5 82            [12]  656 	mov	a,dpl
      00AE89 90 0B 73         [24]  657 	mov	dptr,#_get_supported_args_10000_251
      00AE8C F0               [24]  658 	movx	@dptr,a
      00AE8D EF               [12]  659 	mov	a,r7
      00AE8E A3               [24]  660 	inc	dptr
      00AE8F F0               [24]  661 	movx	@dptr,a
                                    662 ;	quantum/vialrgb.c:29: uint16_t gt = (uint16_t)args[0] | ((uint16_t)args[1] << 8);
      00AE90 90 0B 73         [24]  663 	mov	dptr,#_get_supported_args_10000_251
      00AE93 12 73 CF         [24]  664 	lcall	_ak820_outline_0013
      00AE96 E0               [24]  665 	movx	a,@dptr
      00AE97 FD               [12]  666 	mov	r5,a
      00AE98 7C 00            [12]  667 	mov	r4,#0x00
      00AE9A 8E 82            [24]  668 	mov	dpl,r6
      00AE9C 8F 83            [24]  669 	mov	dph,r7
      00AE9E A3               [24]  670 	inc	dptr
      00AE9F E0               [24]  671 	movx	a,@dptr
      00AEA0 FA               [12]  672 	mov	r2,a
      00AEA1 E4               [12]  673 	clr	a
      00AEA2 42 05            [12]  674 	orl	ar5,a
      00AEA4 EA               [12]  675 	mov	a,r2
      00AEA5 42 04            [12]  676 	orl	ar4,a
                                    677 ;	quantum/vialrgb.c:30: for (uint8_t i = 0; i < length; ++i) args[i] = 0xff;
      00AEA7 90 0B 72         [24]  678 	mov	dptr,#_get_supported_PARM_2
      00AEAA E0               [24]  679 	movx	a,@dptr
      00AEAB FB               [12]  680 	mov	r3,a
      00AEAC 7A 00            [12]  681 	mov	r2,#0x00
      00AEAE                        682 00107$:
      00AEAE C3               [12]  683 	clr	c
      00AEAF EA               [12]  684 	mov	a,r2
      00AEB0 9B               [12]  685 	subb	a,r3
      00AEB1 50 0E            [24]  686 	jnc	00101$
      00AEB3 EA               [12]  687 	mov	a,r2
      00AEB4 2E               [12]  688 	add	a, r6
      00AEB5 F5 82            [12]  689 	mov	dpl,a
      00AEB7 E4               [12]  690 	clr	a
      00AEB8 3F               [12]  691 	addc	a, r7
      00AEB9 F5 83            [12]  692 	mov	dph,a
      00AEBB 74 FF            [12]  693 	mov	a,#0xff
      00AEBD F0               [24]  694 	movx	@dptr,a
      00AEBE 0A               [12]  695 	inc	r2
      00AEBF 80 ED            [24]  696 	sjmp	00107$
      00AEC1                        697 00101$:
                                    698 ;	quantum/vialrgb.c:31: for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
      00AEC1 8D 06            [24]  699 	mov	ar6,r5
      00AEC3 8C 07            [24]  700 	mov	ar7,r4
      00AEC5 8B 05            [24]  701 	mov	ar5,r3
      00AEC7 90 0B 73         [24]  702 	mov	dptr,#_get_supported_args_10000_251
      00AECA E0               [24]  703 	movx	a,@dptr
      00AECB FB               [12]  704 	mov	r3,a
      00AECC A3               [24]  705 	inc	dptr
      00AECD E0               [24]  706 	movx	a,@dptr
      00AECE FC               [12]  707 	mov	r4,a
      00AECF 7A 00            [12]  708 	mov	r2,#0x00
      00AED1                        709 00110$:
      00AED1 BA 07 00         [24]  710 	cjne	r2,#0x07,00159$
      00AED4                        711 00159$:
      00AED4 50 4F            [24]  712 	jnc	00127$
                                    713 ;	quantum/vialrgb.c:32: uint16_t id = pgm_read_word(&supported_modes[i].vialrgb_id);
      00AED6 EA               [12]  714 	mov	a,r2
      00AED7 75 F0 04         [24]  715 	mov	b,#0x04
      00AEDA A4               [48]  716 	mul	ab
      00AEDB 24 B1            [12]  717 	add	a, #_supported_modes
      00AEDD F5 82            [12]  718 	mov	dpl,a
      00AEDF 74 BB            [12]  719 	mov	a,#(_supported_modes >> 8)
      00AEE1 35 F0            [12]  720 	addc	a, b
      00AEE3 F5 83            [12]  721 	mov	dph,a
      00AEE5 E4               [12]  722 	clr	a
      00AEE6 93               [24]  723 	movc	a,@a+dptr
      00AEE7 F8               [12]  724 	mov	r0,a
      00AEE8 A3               [24]  725 	inc	dptr
      00AEE9 E4               [12]  726 	clr	a
      00AEEA 93               [24]  727 	movc	a,@a+dptr
      00AEEB F9               [12]  728 	mov	r1,a
                                    729 ;	quantum/vialrgb.c:33: if (id > gt && length >= sizeof(id)) {
      00AEEC C3               [12]  730 	clr	c
      00AEED EE               [12]  731 	mov	a,r6
      00AEEE 98               [12]  732 	subb	a,r0
      00AEEF EF               [12]  733 	mov	a,r7
      00AEF0 99               [12]  734 	subb	a,r1
      00AEF1 50 2F            [24]  735 	jnc	00111$
                                    736 ;	free result
      00AEF3 BD 02 00         [24]  737 	cjne	r5,#0x02,00162$
      00AEF6                        738 00162$:
      00AEF6 40 2A            [24]  739 	jc	00111$
                                    740 ;	quantum/vialrgb.c:34: args[0] = id;
      00AEF8 C0 06            [24]  741 	push	ar6
      00AEFA C0 07            [24]  742 	push	ar7
      00AEFC 88 07            [24]  743 	mov	ar7,r0
      00AEFE 8B 82            [24]  744 	mov	dpl,r3
      00AF00 8C 83            [24]  745 	mov	dph,r4
      00AF02 EF               [12]  746 	mov	a,r7
      00AF03 F0               [24]  747 	movx	@dptr,a
                                    748 ;	quantum/vialrgb.c:35: args[1] = id >> 8;
      00AF04 8B 82            [24]  749 	mov	dpl,r3
      00AF06 8C 83            [24]  750 	mov	dph,r4
      00AF08 A3               [24]  751 	inc	dptr
      00AF09 89 00            [24]  752 	mov	ar0,r1
      00AF0B E8               [12]  753 	mov	a,r0
      00AF0C F0               [24]  754 	movx	@dptr,a
                                    755 ;	quantum/vialrgb.c:36: length -= sizeof(id);
      00AF0D 1D               [12]  756 	dec	r5
      00AF0E 1D               [12]  757 	dec	r5
                                    758 ;	quantum/vialrgb.c:37: args += sizeof(id);
      00AF0F 74 02            [12]  759 	mov	a,#0x02
      00AF11 2B               [12]  760 	add	a, r3
      00AF12 FB               [12]  761 	mov	r3,a
      00AF13 E4               [12]  762 	clr	a
      00AF14 3C               [12]  763 	addc	a, r4
      00AF15 FC               [12]  764 	mov	r4,a
      00AF16 90 0B 73         [24]  765 	mov	dptr,#_get_supported_args_10000_251
      00AF19 EB               [12]  766 	mov	a,r3
      00AF1A F0               [24]  767 	movx	@dptr,a
      00AF1B EC               [12]  768 	mov	a,r4
      00AF1C A3               [24]  769 	inc	dptr
      00AF1D F0               [24]  770 	movx	@dptr,a
                                    771 ;	quantum/vialrgb.c:31: for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
      00AF1E D0 07            [24]  772 	pop	ar7
      00AF20 D0 06            [24]  773 	pop	ar6
                                    774 ;	quantum/vialrgb.c:37: args += sizeof(id);
      00AF22                        775 00111$:
                                    776 ;	quantum/vialrgb.c:31: for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
      00AF22 0A               [12]  777 	inc	r2
      00AF23 80 AC            [24]  778 	sjmp	00110$
      00AF25                        779 00127$:
      00AF25 90 0B 73         [24]  780 	mov	dptr,#_get_supported_args_10000_251
      00AF28 EB               [12]  781 	mov	a,r3
      00AF29 F0               [24]  782 	movx	@dptr,a
      00AF2A EC               [12]  783 	mov	a,r4
      00AF2B A3               [24]  784 	inc	dptr
      00AF2C F0               [24]  785 	movx	@dptr,a
                                    786 ;	quantum/vialrgb.c:40: }
      00AF2D 22               [24]  787 	ret
                                    788 ;------------------------------------------------------------
                                    789 ;Allocation info for local variables in function 'qmk_id_to_vialrgb_id'
                                    790 ;------------------------------------------------------------
                                    791 ;id            Allocated with name '_qmk_id_to_vialrgb_id_id_10000_258'
                                    792 ;i             Allocated with name '_qmk_id_to_vialrgb_id_i_20000_260'
                                    793 ;qmk_id        Allocated with name '_qmk_id_to_vialrgb_id_qmk_id_30000_261'
                                    794 ;vialrgb_id    Allocated with name '_qmk_id_to_vialrgb_id_vialrgb_id_30000_261'
                                    795 ;------------------------------------------------------------
                                    796 ;	quantum/vialrgb.c:42: static uint16_t qmk_id_to_vialrgb_id(uint16_t id) {
                                    797 ;	-----------------------------------------
                                    798 ;	 function qmk_id_to_vialrgb_id
                                    799 ;	-----------------------------------------
      00AF2E                        800 _qmk_id_to_vialrgb_id:
      00AF2E AF 83            [24]  801 	mov	r7,dph
      00AF30 E5 82            [12]  802 	mov	a,dpl
      00AF32 90 0B 75         [24]  803 	mov	dptr,#_qmk_id_to_vialrgb_id_id_10000_258
      00AF35 F0               [24]  804 	movx	@dptr,a
      00AF36 EF               [12]  805 	mov	a,r7
      00AF37 A3               [24]  806 	inc	dptr
      00AF38 F0               [24]  807 	movx	@dptr,a
                                    808 ;	quantum/vialrgb.c:43: for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
      00AF39 90 0B 75         [24]  809 	mov	dptr,#_qmk_id_to_vialrgb_id_id_10000_258
      00AF3C E0               [24]  810 	movx	a,@dptr
      00AF3D FE               [12]  811 	mov	r6,a
      00AF3E A3               [24]  812 	inc	dptr
      00AF3F E0               [24]  813 	movx	a,@dptr
      00AF40 FF               [12]  814 	mov	r7,a
      00AF41 7D 00            [12]  815 	mov	r5,#0x00
      00AF43                        816 00105$:
      00AF43 BD 07 00         [24]  817 	cjne	r5,#0x07,00130$
      00AF46                        818 00130$:
      00AF46 50 24            [24]  819 	jnc	00103$
                                    820 ;	quantum/vialrgb.c:44: uint16_t qmk_id = pgm_read_word(&supported_modes[i].qmk_id);
      00AF48 12 B3 F5         [24]  821 	lcall	_ak820_outline_0025
      00AF4B 93               [24]  822 	movc	a,@a+dptr
      00AF4C F9               [12]  823 	mov	r1,a
      00AF4D A3               [24]  824 	inc	dptr
      00AF4E E4               [12]  825 	clr	a
      00AF4F 93               [24]  826 	movc	a,@a+dptr
      00AF50 FA               [12]  827 	mov	r2,a
                                    828 ;	quantum/vialrgb.c:45: uint16_t vialrgb_id = pgm_read_word(&supported_modes[i].vialrgb_id);
      00AF51 8B 82            [24]  829 	mov	dpl,r3
      00AF53 8C 83            [24]  830 	mov	dph,r4
      00AF55 E4               [12]  831 	clr	a
      00AF56 93               [24]  832 	movc	a,@a+dptr
      00AF57 FB               [12]  833 	mov	r3,a
      00AF58 A3               [24]  834 	inc	dptr
      00AF59 E4               [12]  835 	clr	a
      00AF5A 93               [24]  836 	movc	a,@a+dptr
      00AF5B FC               [12]  837 	mov	r4,a
                                    838 ;	quantum/vialrgb.c:46: if (qmk_id == id)
      00AF5C E9               [12]  839 	mov	a,r1
      00AF5D B5 06 09         [24]  840 	cjne	a,ar6,00106$
      00AF60 EA               [12]  841 	mov	a,r2
      00AF61 B5 07 05         [24]  842 	cjne	a,ar7,00106$
                                    843 ;	quantum/vialrgb.c:47: return vialrgb_id;
      00AF64 8B 82            [24]  844 	mov	dpl, r3
      00AF66 8C 83            [24]  845 	mov	dph, r4
      00AF68 22               [24]  846 	ret
      00AF69                        847 00106$:
                                    848 ;	quantum/vialrgb.c:43: for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
      00AF69 0D               [12]  849 	inc	r5
      00AF6A 80 D7            [24]  850 	sjmp	00105$
      00AF6C                        851 00103$:
                                    852 ;	quantum/vialrgb.c:49: return 0;
      00AF6C 90 00 00         [24]  853 	mov	dptr,#0x0000
                                    854 ;	quantum/vialrgb.c:50: }
      00AF6F 22               [24]  855 	ret
                                    856 ;------------------------------------------------------------
                                    857 ;Allocation info for local variables in function 'vialrgb_id_to_qmk_id'
                                    858 ;------------------------------------------------------------
                                    859 ;id            Allocated with name '_vialrgb_id_to_qmk_id_id_10000_263'
                                    860 ;i             Allocated with name '_vialrgb_id_to_qmk_id_i_20000_265'
                                    861 ;qmk_id        Allocated with name '_vialrgb_id_to_qmk_id_qmk_id_30000_266'
                                    862 ;vialrgb_id    Allocated with name '_vialrgb_id_to_qmk_id_vialrgb_id_30000_266'
                                    863 ;------------------------------------------------------------
                                    864 ;	quantum/vialrgb.c:52: static uint16_t vialrgb_id_to_qmk_id(uint16_t id) {
                                    865 ;	-----------------------------------------
                                    866 ;	 function vialrgb_id_to_qmk_id
                                    867 ;	-----------------------------------------
      00AF70                        868 _vialrgb_id_to_qmk_id:
      00AF70 AF 83            [24]  869 	mov	r7,dph
      00AF72 E5 82            [12]  870 	mov	a,dpl
      00AF74 90 0B 77         [24]  871 	mov	dptr,#_vialrgb_id_to_qmk_id_id_10000_263
      00AF77 F0               [24]  872 	movx	@dptr,a
      00AF78 EF               [12]  873 	mov	a,r7
      00AF79 A3               [24]  874 	inc	dptr
      00AF7A F0               [24]  875 	movx	@dptr,a
                                    876 ;	quantum/vialrgb.c:53: for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
      00AF7B 90 0B 77         [24]  877 	mov	dptr,#_vialrgb_id_to_qmk_id_id_10000_263
      00AF7E E0               [24]  878 	movx	a,@dptr
      00AF7F FE               [12]  879 	mov	r6,a
      00AF80 A3               [24]  880 	inc	dptr
      00AF81 E0               [24]  881 	movx	a,@dptr
      00AF82 FF               [12]  882 	mov	r7,a
      00AF83 7D 00            [12]  883 	mov	r5,#0x00
      00AF85                        884 00105$:
      00AF85 BD 07 00         [24]  885 	cjne	r5,#0x07,00130$
      00AF88                        886 00130$:
      00AF88 50 24            [24]  887 	jnc	00103$
                                    888 ;	quantum/vialrgb.c:54: uint16_t qmk_id = pgm_read_word(&supported_modes[i].qmk_id);
      00AF8A 12 B3 F5         [24]  889 	lcall	_ak820_outline_0025
      00AF8D 93               [24]  890 	movc	a,@a+dptr
      00AF8E F9               [12]  891 	mov	r1,a
      00AF8F A3               [24]  892 	inc	dptr
      00AF90 E4               [12]  893 	clr	a
      00AF91 93               [24]  894 	movc	a,@a+dptr
      00AF92 FA               [12]  895 	mov	r2,a
                                    896 ;	quantum/vialrgb.c:55: uint16_t vialrgb_id = pgm_read_word(&supported_modes[i].vialrgb_id);
      00AF93 8B 82            [24]  897 	mov	dpl,r3
      00AF95 8C 83            [24]  898 	mov	dph,r4
      00AF97 E4               [12]  899 	clr	a
      00AF98 93               [24]  900 	movc	a,@a+dptr
      00AF99 FB               [12]  901 	mov	r3,a
      00AF9A A3               [24]  902 	inc	dptr
      00AF9B E4               [12]  903 	clr	a
      00AF9C 93               [24]  904 	movc	a,@a+dptr
      00AF9D FC               [12]  905 	mov	r4,a
                                    906 ;	quantum/vialrgb.c:56: if (vialrgb_id == id)
      00AF9E EB               [12]  907 	mov	a,r3
      00AF9F B5 06 09         [24]  908 	cjne	a,ar6,00106$
      00AFA2 EC               [12]  909 	mov	a,r4
      00AFA3 B5 07 05         [24]  910 	cjne	a,ar7,00106$
                                    911 ;	quantum/vialrgb.c:57: return qmk_id;
      00AFA6 89 82            [24]  912 	mov	dpl, r1
      00AFA8 8A 83            [24]  913 	mov	dph, r2
      00AFAA 22               [24]  914 	ret
      00AFAB                        915 00106$:
                                    916 ;	quantum/vialrgb.c:53: for (uint8_t i = 0; i < SUPPORTED_MODES_LENGTH; ++i) {
      00AFAB 0D               [12]  917 	inc	r5
      00AFAC 80 D7            [24]  918 	sjmp	00105$
      00AFAE                        919 00103$:
                                    920 ;	quantum/vialrgb.c:59: return 0;
      00AFAE 90 00 00         [24]  921 	mov	dptr,#0x0000
                                    922 ;	quantum/vialrgb.c:60: }
      00AFB1 22               [24]  923 	ret
                                    924 ;------------------------------------------------------------
                                    925 ;Allocation info for local variables in function 'get_mode'
                                    926 ;------------------------------------------------------------
                                    927 ;	quantum/vialrgb.c:62: static uint16_t get_mode(void) {
                                    928 ;	-----------------------------------------
                                    929 ;	 function get_mode
                                    930 ;	-----------------------------------------
      00AFB2                        931 _get_mode:
                                    932 ;	quantum/vialrgb.c:64: if (!rgb_matrix_is_enabled())
      00AFB2 12 4E CB         [24]  933 	lcall	_rgb_matrix_is_enabled
      00AFB5 E5 82            [12]  934 	mov	a, dpl
      00AFB7 70 04            [24]  935 	jnz	00102$
                                    936 ;	quantum/vialrgb.c:65: return VIALRGB_EFFECT_OFF;
      00AFB9 90 00 00         [24]  937 	mov	dptr,#0x0000
      00AFBC 22               [24]  938 	ret
      00AFBD                        939 00102$:
                                    940 ;	quantum/vialrgb.c:66: return qmk_id_to_vialrgb_id(rgb_matrix_get_mode());
      00AFBD 12 4E D4         [24]  941 	lcall	_rgb_matrix_get_mode
      00AFC0 7E 00            [12]  942 	mov	r6,#0x00
      00AFC2 8E 83            [24]  943 	mov	dph, r6
                                    944 ;	quantum/vialrgb.c:67: }
      00AFC4 02 AF 2E         [24]  945 	ljmp	_qmk_id_to_vialrgb_id
                                    946 ;------------------------------------------------------------
                                    947 ;Allocation info for local variables in function 'set_mode'
                                    948 ;------------------------------------------------------------
                                    949 ;mode          Allocated with name '_set_mode_mode_10000_271'
                                    950 ;------------------------------------------------------------
                                    951 ;	quantum/vialrgb.c:69: static void set_mode(uint16_t mode) {
                                    952 ;	-----------------------------------------
                                    953 ;	 function set_mode
                                    954 ;	-----------------------------------------
      00AFC7                        955 _set_mode:
      00AFC7 AF 83            [24]  956 	mov	r7,dph
      00AFC9 E5 82            [12]  957 	mov	a,dpl
      00AFCB 90 0B 79         [24]  958 	mov	dptr,#_set_mode_mode_10000_271
      00AFCE F0               [24]  959 	movx	@dptr,a
      00AFCF EF               [12]  960 	mov	a,r7
      00AFD0 A3               [24]  961 	inc	dptr
      00AFD1 F0               [24]  962 	movx	@dptr,a
                                    963 ;	quantum/vialrgb.c:71: if (mode == VIALRGB_EFFECT_OFF) {
      00AFD2 90 0B 79         [24]  964 	mov	dptr,#_set_mode_mode_10000_271
      00AFD5 E0               [24]  965 	movx	a,@dptr
      00AFD6 FE               [12]  966 	mov	r6,a
      00AFD7 A3               [24]  967 	inc	dptr
      00AFD8 E0               [24]  968 	movx	a,@dptr
      00AFD9 FF               [12]  969 	mov	r7,a
      00AFDA 90 0B 79         [24]  970 	mov	dptr,#_set_mode_mode_10000_271
      00AFDD E0               [24]  971 	movx	a,@dptr
      00AFDE F5 F0            [12]  972 	mov	b,a
      00AFE0 A3               [24]  973 	inc	dptr
      00AFE1 E0               [24]  974 	movx	a,@dptr
      00AFE2 45 F0            [12]  975 	orl	a,b
      00AFE4 70 03            [24]  976 	jnz	00102$
                                    977 ;	quantum/vialrgb.c:72: rgb_matrix_disable_noeeprom();
      00AFE6 02 4F 35         [24]  978 	ljmp	_rgb_matrix_disable_noeeprom
      00AFE9                        979 00102$:
                                    980 ;	quantum/vialrgb.c:74: rgb_matrix_enable_noeeprom();
      00AFE9 C0 07            [24]  981 	push	ar7
      00AFEB C0 06            [24]  982 	push	ar6
      00AFED 12 4F 1B         [24]  983 	lcall	_rgb_matrix_enable_noeeprom
      00AFF0 D0 06            [24]  984 	pop	ar6
      00AFF2 D0 07            [24]  985 	pop	ar7
                                    986 ;	quantum/vialrgb.c:75: rgb_matrix_mode_noeeprom(vialrgb_id_to_qmk_id(mode));
      00AFF4 8E 82            [24]  987 	mov	dpl, r6
      00AFF6 8F 83            [24]  988 	mov	dph, r7
      00AFF8 12 AF 70         [24]  989 	lcall	_vialrgb_id_to_qmk_id
                                    990 ;	quantum/vialrgb.c:77: }
      00AFFB 02 4F 44         [24]  991 	ljmp	_rgb_matrix_mode_noeeprom
                                    992 ;------------------------------------------------------------
                                    993 ;Allocation info for local variables in function 'get_matrix_pos_for_led'
                                    994 ;------------------------------------------------------------
                                    995 ;output        Allocated with name '_get_matrix_pos_for_led_PARM_2'
                                    996 ;led           Allocated with name '_get_matrix_pos_for_led_led_10000_276'
                                    997 ;slot          Allocated with name '_get_matrix_pos_for_led_slot_10000_277'
                                    998 ;------------------------------------------------------------
                                    999 ;	quantum/vialrgb.c:80: static void get_matrix_pos_for_led(uint16_t led, uint8_t VIALRGB_BUFFER *output) {
                                   1000 ;	-----------------------------------------
                                   1001 ;	 function get_matrix_pos_for_led
                                   1002 ;	-----------------------------------------
      00AFFE                       1003 _get_matrix_pos_for_led:
      00AFFE AF 83            [24] 1004 	mov	r7,dph
      00B000 E5 82            [12] 1005 	mov	a,dpl
      00B002 90 0B 7D         [24] 1006 	mov	dptr,#_get_matrix_pos_for_led_led_10000_276
      00B005 F0               [24] 1007 	movx	@dptr,a
      00B006 EF               [12] 1008 	mov	a,r7
      00B007 A3               [24] 1009 	inc	dptr
      00B008 F0               [24] 1010 	movx	@dptr,a
                                   1011 ;	quantum/vialrgb.c:82: uint8_t slot = ak820_rgb_slots[led];
      00B009 90 0B 7D         [24] 1012 	mov	dptr,#_get_matrix_pos_for_led_led_10000_276
      00B00C E0               [24] 1013 	movx	a,@dptr
      00B00D FE               [12] 1014 	mov	r6,a
      00B00E A3               [24] 1015 	inc	dptr
      00B00F E0               [24] 1016 	movx	a,@dptr
      00B010 FF               [12] 1017 	mov	r7,a
      00B011 EE               [12] 1018 	mov	a,r6
      00B012 24 C7            [12] 1019 	add	a, #_ak820_rgb_slots
      00B014 F5 82            [12] 1020 	mov	dpl,a
      00B016 EF               [12] 1021 	mov	a,r7
      00B017 34 B5            [12] 1022 	addc	a, #(_ak820_rgb_slots >> 8)
      00B019 F5 83            [12] 1023 	mov	dph,a
      00B01B E4               [12] 1024 	clr	a
      00B01C 93               [24] 1025 	movc	a,@a+dptr
      00B01D FF               [12] 1026 	mov	r7,a
                                   1027 ;	quantum/vialrgb.c:83: output[0] = slot >> 3;
      00B01E 90 0B 7B         [24] 1028 	mov	dptr,#_get_matrix_pos_for_led_PARM_2
      00B021 E0               [24] 1029 	movx	a,@dptr
      00B022 FD               [12] 1030 	mov	r5,a
      00B023 A3               [24] 1031 	inc	dptr
      00B024 E0               [24] 1032 	movx	a,@dptr
      00B025 FE               [12] 1033 	mov	r6,a
      00B026 EF               [12] 1034 	mov	a,r7
      00B027 C4               [12] 1035 	swap	a
      00B028 23               [12] 1036 	rl	a
      00B029 54 1F            [12] 1037 	anl	a,#0x1f
      00B02B 8D 82            [24] 1038 	mov	dpl,r5
      00B02D 8E 83            [24] 1039 	mov	dph,r6
      00B02F F0               [24] 1040 	movx	@dptr,a
                                   1041 ;	quantum/vialrgb.c:84: output[1] = slot & 7;
      00B030 8D 82            [24] 1042 	mov	dpl,r5
      00B032 8E 83            [24] 1043 	mov	dph,r6
      00B034 A3               [24] 1044 	inc	dptr
      00B035 53 07 07         [24] 1045 	anl	ar7,#0x07
      00B038 EF               [12] 1046 	mov	a,r7
      00B039 F0               [24] 1047 	movx	@dptr,a
                                   1048 ;	quantum/vialrgb.c:97: }
      00B03A 22               [24] 1049 	ret
                                   1050 ;------------------------------------------------------------
                                   1051 ;Allocation info for local variables in function 'fast_set_leds'
                                   1052 ;------------------------------------------------------------
                                   1053 ;sloc0         Allocated with name '_fast_set_leds_sloc0_1_0'
                                   1054 ;sloc1         Allocated with name '_fast_set_leds_sloc1_1_0'
                                   1055 ;length        Allocated with name '_fast_set_leds_PARM_2'
                                   1056 ;args          Allocated with name '_fast_set_leds_args_10000_278'
                                   1057 ;first_index   Allocated with name '_fast_set_leds_first_index_10001_281'
                                   1058 ;num_leds      Allocated with name '_fast_set_leds_num_leds_10001_281'
                                   1059 ;i             Allocated with name '_fast_set_leds_i_20001_284'
                                   1060 ;color         Allocated with name '_fast_set_leds_color_30001_285'
                                   1061 ;val           Allocated with name '_fast_set_leds_val_30002_286'
                                   1062 ;------------------------------------------------------------
                                   1063 ;	quantum/vialrgb.c:99: static void fast_set_leds(uint8_t VIALRGB_BUFFER *args, uint8_t length) {
                                   1064 ;	-----------------------------------------
                                   1065 ;	 function fast_set_leds
                                   1066 ;	-----------------------------------------
      00B03B                       1067 _fast_set_leds:
      00B03B AF 83            [24] 1068 	mov	r7,dph
      00B03D E5 82            [12] 1069 	mov	a,dpl
      00B03F 90 0B 80         [24] 1070 	mov	dptr,#_fast_set_leds_args_10000_278
      00B042 F0               [24] 1071 	movx	@dptr,a
      00B043 EF               [12] 1072 	mov	a,r7
      00B044 A3               [24] 1073 	inc	dptr
      00B045 F0               [24] 1074 	movx	@dptr,a
                                   1075 ;	quantum/vialrgb.c:102: if (length < 3) return;
      00B046 90 0B 7F         [24] 1076 	mov	dptr,#_fast_set_leds_PARM_2
      00B049 E0               [24] 1077 	movx	a,@dptr
      00B04A FF               [12] 1078 	mov	r7,a
      00B04B BF 03 00         [24] 1079 	cjne	r7,#0x03,00159$
      00B04E                       1080 00159$:
      00B04E 50 01            [24] 1081 	jnc	00102$
      00B050 22               [24] 1082 	ret
      00B051                       1083 00102$:
                                   1084 ;	quantum/vialrgb.c:104: uint16_t first_index = (uint16_t)args[0] | ((uint16_t)args[1] << 8);
      00B051 90 0B 80         [24] 1085 	mov	dptr,#_fast_set_leds_args_10000_278
      00B054 E0               [24] 1086 	movx	a,@dptr
      00B055 FD               [12] 1087 	mov	r5,a
      00B056 A3               [24] 1088 	inc	dptr
      00B057 E0               [24] 1089 	movx	a,@dptr
      00B058 FE               [12] 1090 	mov	r6,a
      00B059 8D 82            [24] 1091 	mov	dpl,r5
      00B05B 8E 83            [24] 1092 	mov	dph,r6
      00B05D E0               [24] 1093 	movx	a,@dptr
      00B05E FC               [12] 1094 	mov	r4,a
      00B05F 7B 00            [12] 1095 	mov	r3,#0x00
      00B061 8D 82            [24] 1096 	mov	dpl,r5
      00B063 8E 83            [24] 1097 	mov	dph,r6
      00B065 A3               [24] 1098 	inc	dptr
      00B066 E0               [24] 1099 	movx	a,@dptr
      00B067 FA               [12] 1100 	mov	r2,a
      00B068 79 00            [12] 1101 	mov	r1,#0x00
      00B06A 90 0B 82         [24] 1102 	mov	dptr,#_fast_set_leds_first_index_10001_281
      00B06D E9               [12] 1103 	mov	a,r1
      00B06E 4C               [12] 1104 	orl	a,r4
      00B06F F0               [24] 1105 	movx	@dptr,a
      00B070 EA               [12] 1106 	mov	a,r2
      00B071 4B               [12] 1107 	orl	a,r3
      00B072 A3               [24] 1108 	inc	dptr
      00B073 F0               [24] 1109 	movx	@dptr,a
                                   1110 ;	quantum/vialrgb.c:105: uint8_t num_leds = args[2];
      00B074 8D 82            [24] 1111 	mov	dpl,r5
      00B076 8E 83            [24] 1112 	mov	dph,r6
      00B078 A3               [24] 1113 	inc	dptr
      00B079 A3               [24] 1114 	inc	dptr
      00B07A E0               [24] 1115 	movx	a,@dptr
      00B07B 90 0B 84         [24] 1116 	mov	dptr,#_fast_set_leds_num_leds_10001_281
      00B07E F0               [24] 1117 	movx	@dptr,a
                                   1118 ;	quantum/vialrgb.c:106: length -= 3;
      00B07F EF               [12] 1119 	mov	a,r7
      00B080 24 FD            [12] 1120 	add	a,#0xfd
      00B082 90 0B 7F         [24] 1121 	mov	dptr,#_fast_set_leds_PARM_2
      00B085 F0               [24] 1122 	movx	@dptr,a
                                   1123 ;	quantum/vialrgb.c:107: args += 3;
      00B086 90 0B 80         [24] 1124 	mov	dptr,#_fast_set_leds_args_10000_278
      00B089 74 03            [12] 1125 	mov	a,#0x03
      00B08B 2D               [12] 1126 	add	a, r5
      00B08C F0               [24] 1127 	movx	@dptr,a
      00B08D E4               [12] 1128 	clr	a
      00B08E 3E               [12] 1129 	addc	a, r6
      00B08F A3               [24] 1130 	inc	dptr
      00B090 F0               [24] 1131 	movx	@dptr,a
                                   1132 ;	quantum/vialrgb.c:110: if ((uint16_t)num_leds * 3u > length || first_index >= RGB_MATRIX_LED_COUNT) return;
      00B091 90 0B 84         [24] 1133 	mov	dptr,#_fast_set_leds_num_leds_10001_281
      00B094 E0               [24] 1134 	movx	a,@dptr
      00B095 FF               [12] 1135 	mov	r7,a
      00B096 75 F0 03         [24] 1136 	mov	b,#0x03
      00B099 A4               [48] 1137 	mul	ab
      00B09A FE               [12] 1138 	mov	r6,a
      00B09B AD F0            [24] 1139 	mov	r5,b
      00B09D 90 0B 7F         [24] 1140 	mov	dptr,#_fast_set_leds_PARM_2
      00B0A0 E0               [24] 1141 	movx	a,@dptr
      00B0A1 FB               [12] 1142 	mov	r3,a
      00B0A2 7C 00            [12] 1143 	mov	r4,#0x00
      00B0A4 C3               [12] 1144 	clr	c
      00B0A5 EB               [12] 1145 	mov	a,r3
      00B0A6 9E               [12] 1146 	subb	a,r6
      00B0A7 EC               [12] 1147 	mov	a,r4
      00B0A8 9D               [12] 1148 	subb	a,r5
      00B0A9 40 15            [24] 1149 	jc	00103$
                                   1150 ;	free result
      00B0AB 90 0B 82         [24] 1151 	mov	dptr,#_fast_set_leds_first_index_10001_281
      00B0AE E0               [24] 1152 	movx	a,@dptr
      00B0AF FD               [12] 1153 	mov	r5,a
      00B0B0 A3               [24] 1154 	inc	dptr
      00B0B1 E0               [24] 1155 	movx	a,@dptr
      00B0B2 FE               [12] 1156 	mov	r6,a
      00B0B3 8D 03            [24] 1157 	mov	ar3,r5
      00B0B5 8E 04            [24] 1158 	mov	ar4,r6
      00B0B7 C3               [12] 1159 	clr	c
      00B0B8 EB               [12] 1160 	mov	a,r3
      00B0B9 94 52            [12] 1161 	subb	a,#0x52
      00B0BB EC               [12] 1162 	mov	a,r4
      00B0BC 94 00            [12] 1163 	subb	a,#0x00
      00B0BE 40 01            [24] 1164 	jc	00104$
      00B0C0                       1165 00103$:
      00B0C0 22               [24] 1166 	ret
      00B0C1                       1167 00104$:
                                   1168 ;	quantum/vialrgb.c:111: if (num_leds > RGB_MATRIX_LED_COUNT - first_index) num_leds = RGB_MATRIX_LED_COUNT - first_index;
      00B0C1 74 52            [12] 1169 	mov	a,#0x52
      00B0C3 C3               [12] 1170 	clr	c
      00B0C4 9D               [12] 1171 	subb	a,r5
      00B0C5 FB               [12] 1172 	mov	r3,a
      00B0C6 E4               [12] 1173 	clr	a
      00B0C7 9E               [12] 1174 	subb	a,r6
      00B0C8 FC               [12] 1175 	mov	r4,a
      00B0C9 7A 00            [12] 1176 	mov	r2,#0x00
      00B0CB C3               [12] 1177 	clr	c
      00B0CC EB               [12] 1178 	mov	a,r3
      00B0CD 9F               [12] 1179 	subb	a,r7
      00B0CE EC               [12] 1180 	mov	a,r4
      00B0CF 9A               [12] 1181 	subb	a,r2
      00B0D0 50 08            [24] 1182 	jnc	00127$
                                   1183 ;	free result
      00B0D2 90 0B 84         [24] 1184 	mov	dptr,#_fast_set_leds_num_leds_10001_281
      00B0D5 74 52            [12] 1185 	mov	a,#0x52
      00B0D7 C3               [12] 1186 	clr	c
      00B0D8 9D               [12] 1187 	subb	a,r5
      00B0D9 F0               [24] 1188 	movx	@dptr,a
                                   1189 ;	quantum/vialrgb.c:113: for (uint8_t i = 0; i < num_leds; ++i) {
      00B0DA                       1190 00127$:
      00B0DA 90 0B 84         [24] 1191 	mov	dptr,#_fast_set_leds_num_leds_10001_281
      00B0DD E0               [24] 1192 	movx	a,@dptr
      00B0DE FF               [12] 1193 	mov	r7,a
      00B0DF 90 0B 82         [24] 1194 	mov	dptr,#_fast_set_leds_first_index_10001_281
      00B0E2 E0               [24] 1195 	movx	a,@dptr
      00B0E3 FD               [12] 1196 	mov	r5,a
      00B0E4 A3               [24] 1197 	inc	dptr
      00B0E5 E0               [24] 1198 	movx	a,@dptr
      00B0E6 FE               [12] 1199 	mov	r6,a
      00B0E7 7C 00            [12] 1200 	mov	r4,#0x00
      00B0E9                       1201 00110$:
      00B0E9 C3               [12] 1202 	clr	c
      00B0EA EC               [12] 1203 	mov	a,r4
      00B0EB 9F               [12] 1204 	subb	a,r7
      00B0EC 40 01            [24] 1205 	jc	00164$
      00B0EE 22               [24] 1206 	ret
      00B0EF                       1207 00164$:
                                   1208 ;	quantum/vialrgb.c:114: HSV VIALRGB_BUFFER *color = &g_direct_mode_colors[first_index++];
      00B0EF C0 07            [24] 1209 	push	ar7
      00B0F1 90 0B 9C         [24] 1210 	mov	dptr,#__mulint_PARM_2
      00B0F4 ED               [12] 1211 	mov	a,r5
      00B0F5 F0               [24] 1212 	movx	@dptr,a
      00B0F6 EE               [12] 1213 	mov	a,r6
      00B0F7 A3               [24] 1214 	inc	dptr
      00B0F8 F0               [24] 1215 	movx	@dptr,a
      00B0F9 90 00 03         [24] 1216 	mov	dptr,#0x0003
      00B0FC C0 07            [24] 1217 	push	ar7
      00B0FE C0 06            [24] 1218 	push	ar6
      00B100 C0 05            [24] 1219 	push	ar5
      00B102 C0 04            [24] 1220 	push	ar4
      00B104 12 B5 77         [24] 1221 	lcall	__mulint
      00B107 AA 82            [24] 1222 	mov	r2, dpl
      00B109 AB 83            [24] 1223 	mov	r3, dph
      00B10B D0 04            [24] 1224 	pop	ar4
      00B10D D0 05            [24] 1225 	pop	ar5
      00B10F D0 06            [24] 1226 	pop	ar6
      00B111 D0 07            [24] 1227 	pop	ar7
      00B113 0D               [12] 1228 	inc	r5
      00B114 BD 00 01         [24] 1229 	cjne	r5,#0x00,00165$
      00B117 0E               [12] 1230 	inc	r6
      00B118                       1231 00165$:
      00B118 EA               [12] 1232 	mov	a,r2
      00B119 24 7C            [12] 1233 	add	a, #_g_direct_mode_colors
      00B11B FA               [12] 1234 	mov	r2,a
      00B11C EB               [12] 1235 	mov	a,r3
      00B11D 34 0A            [12] 1236 	addc	a, #(_g_direct_mode_colors >> 8)
      00B11F FB               [12] 1237 	mov	r3,a
                                   1238 ;	quantum/vialrgb.c:115: color->h = *args++;
      00B120 8A 53            [24] 1239 	mov	_fast_set_leds_sloc0_1_0,r2
      00B122 8B 54            [24] 1240 	mov	(_fast_set_leds_sloc0_1_0 + 1),r3
      00B124 90 0B 80         [24] 1241 	mov	dptr,#_fast_set_leds_args_10000_278
      00B127 E0               [24] 1242 	movx	a,@dptr
      00B128 F9               [12] 1243 	mov	r1,a
      00B129 A3               [24] 1244 	inc	dptr
      00B12A E0               [24] 1245 	movx	a,@dptr
      00B12B FF               [12] 1246 	mov	r7,a
      00B12C 89 82            [24] 1247 	mov	dpl,r1
      00B12E 8F 83            [24] 1248 	mov	dph,r7
      00B130 E0               [24] 1249 	movx	a,@dptr
      00B131 F8               [12] 1250 	mov	r0,a
      00B132 90 0B 80         [24] 1251 	mov	dptr,#_fast_set_leds_args_10000_278
      00B135 74 01            [12] 1252 	mov	a,#0x01
      00B137 29               [12] 1253 	add	a, r1
      00B138 F0               [24] 1254 	movx	@dptr,a
      00B139 E4               [12] 1255 	clr	a
      00B13A 3F               [12] 1256 	addc	a, r7
      00B13B A3               [24] 1257 	inc	dptr
      00B13C F0               [24] 1258 	movx	@dptr,a
      00B13D 85 53 82         [24] 1259 	mov	dpl,_fast_set_leds_sloc0_1_0
      00B140 85 54 83         [24] 1260 	mov	dph,(_fast_set_leds_sloc0_1_0 + 1)
      00B143 E8               [12] 1261 	mov	a,r0
      00B144 F0               [24] 1262 	movx	@dptr,a
                                   1263 ;	quantum/vialrgb.c:116: color->s = *args++;
      00B145 74 01            [12] 1264 	mov	a,#0x01
      00B147 2A               [12] 1265 	add	a, r2
      00B148 F5 53            [12] 1266 	mov	_fast_set_leds_sloc0_1_0,a
      00B14A E4               [12] 1267 	clr	a
      00B14B 3B               [12] 1268 	addc	a, r3
      00B14C F5 54            [12] 1269 	mov	(_fast_set_leds_sloc0_1_0 + 1),a
      00B14E 90 0B 80         [24] 1270 	mov	dptr,#_fast_set_leds_args_10000_278
      00B151 E0               [24] 1271 	movx	a,@dptr
      00B152 F8               [12] 1272 	mov	r0,a
      00B153 A3               [24] 1273 	inc	dptr
      00B154 E0               [24] 1274 	movx	a,@dptr
      00B155 FF               [12] 1275 	mov	r7,a
      00B156 88 82            [24] 1276 	mov	dpl,r0
      00B158 8F 83            [24] 1277 	mov	dph,r7
      00B15A E0               [24] 1278 	movx	a,@dptr
      00B15B F9               [12] 1279 	mov	r1,a
      00B15C 90 0B 80         [24] 1280 	mov	dptr,#_fast_set_leds_args_10000_278
      00B15F 74 01            [12] 1281 	mov	a,#0x01
      00B161 28               [12] 1282 	add	a, r0
      00B162 F0               [24] 1283 	movx	@dptr,a
      00B163 E4               [12] 1284 	clr	a
      00B164 3F               [12] 1285 	addc	a, r7
      00B165 A3               [24] 1286 	inc	dptr
      00B166 F0               [24] 1287 	movx	@dptr,a
      00B167 85 53 82         [24] 1288 	mov	dpl,_fast_set_leds_sloc0_1_0
      00B16A 85 54 83         [24] 1289 	mov	dph,(_fast_set_leds_sloc0_1_0 + 1)
      00B16D E9               [12] 1290 	mov	a,r1
      00B16E F0               [24] 1291 	movx	@dptr,a
                                   1292 ;	quantum/vialrgb.c:117: uint8_t val = *args++;
      00B16F 90 0B 80         [24] 1293 	mov	dptr,#_fast_set_leds_args_10000_278
      00B172 E0               [24] 1294 	movx	a,@dptr
      00B173 F9               [12] 1295 	mov	r1,a
      00B174 A3               [24] 1296 	inc	dptr
      00B175 E0               [24] 1297 	movx	a,@dptr
      00B176 FF               [12] 1298 	mov	r7,a
      00B177 89 82            [24] 1299 	mov	dpl,r1
      00B179 8F 83            [24] 1300 	mov	dph,r7
      00B17B E0               [24] 1301 	movx	a,@dptr
      00B17C F5 53            [12] 1302 	mov	_fast_set_leds_sloc0_1_0,a
      00B17E 90 0B 80         [24] 1303 	mov	dptr,#_fast_set_leds_args_10000_278
      00B181 74 01            [12] 1304 	mov	a,#0x01
      00B183 29               [12] 1305 	add	a, r1
      00B184 F0               [24] 1306 	movx	@dptr,a
      00B185 E4               [12] 1307 	clr	a
      00B186 3F               [12] 1308 	addc	a, r7
      00B187 A3               [24] 1309 	inc	dptr
      00B188 F0               [24] 1310 	movx	@dptr,a
                                   1311 ;	quantum/vialrgb.c:118: color->v = (val > RGB_MATRIX_MAXIMUM_BRIGHTNESS) ? RGB_MATRIX_MAXIMUM_BRIGHTNESS : val;
      00B189 74 02            [12] 1312 	mov	a,#0x02
      00B18B 2A               [12] 1313 	add	a, r2
      00B18C F5 55            [12] 1314 	mov	_fast_set_leds_sloc1_1_0,a
      00B18E E4               [12] 1315 	clr	a
      00B18F 3B               [12] 1316 	addc	a, r3
      00B190 F5 56            [12] 1317 	mov	(_fast_set_leds_sloc1_1_0 + 1),a
      00B192 C3               [12] 1318 	clr	c
      00B193 74 A0            [12] 1319 	mov	a,#0xa0
      00B195 95 53            [12] 1320 	subb	a,_fast_set_leds_sloc0_1_0
      00B197 D0 07            [24] 1321 	pop	ar7
      00B199 50 04            [24] 1322 	jnc	00114$
                                   1323 ;	free result
      00B19B 7B A0            [12] 1324 	mov	r3,#0xa0
      00B19D 80 04            [24] 1325 	sjmp	00115$
      00B19F                       1326 00114$:
      00B19F AA 53            [24] 1327 	mov	r2,_fast_set_leds_sloc0_1_0
      00B1A1 8A 03            [24] 1328 	mov	ar3,r2
      00B1A3                       1329 00115$:
      00B1A3 85 55 82         [24] 1330 	mov	dpl,_fast_set_leds_sloc1_1_0
      00B1A6 85 56 83         [24] 1331 	mov	dph,(_fast_set_leds_sloc1_1_0 + 1)
      00B1A9 EB               [12] 1332 	mov	a,r3
      00B1AA F0               [24] 1333 	movx	@dptr,a
                                   1334 ;	quantum/vialrgb.c:113: for (uint8_t i = 0; i < num_leds; ++i) {
      00B1AB 0C               [12] 1335 	inc	r4
                                   1336 ;	quantum/vialrgb.c:120: }
      00B1AC 02 B0 E9         [24] 1337 	ljmp	00110$
                                   1338 ;------------------------------------------------------------
                                   1339 ;Allocation info for local variables in function 'vialrgb_get_value'
                                   1340 ;------------------------------------------------------------
                                   1341 ;sloc0         Allocated with name '_vialrgb_get_value_sloc0_1_0'
                                   1342 ;sloc1         Allocated with name '_vialrgb_get_value_sloc1_1_0'
                                   1343 ;length        Allocated with name '_vialrgb_get_value_PARM_2'
                                   1344 ;data          Allocated with name '_vialrgb_get_value_data_10000_287'
                                   1345 ;args          Allocated with name '_vialrgb_get_value_args_10001_290'
                                   1346 ;cmd           Allocated with name '_vialrgb_get_value_cmd_10001_290'
                                   1347 ;vialrgb_id    Allocated with name '_vialrgb_get_value_vialrgb_id_40001_293'
                                   1348 ;led           Allocated with name '_vialrgb_get_value_led_40001_296'
                                   1349 ;------------------------------------------------------------
                                   1350 ;	quantum/vialrgb.c:123: void vialrgb_get_value(uint8_t *data, uint8_t length) {
                                   1351 ;	-----------------------------------------
                                   1352 ;	 function vialrgb_get_value
                                   1353 ;	-----------------------------------------
      00B1AF                       1354 _vialrgb_get_value:
      00B1AF AF F0            [24] 1355 	mov	r7,b
      00B1B1 AE 83            [24] 1356 	mov	r6,dph
      00B1B3 E5 82            [12] 1357 	mov	a,dpl
      00B1B5 90 0B 86         [24] 1358 	mov	dptr,#_vialrgb_get_value_data_10000_287
      00B1B8 F0               [24] 1359 	movx	@dptr,a
      00B1B9 EE               [12] 1360 	mov	a,r6
      00B1BA A3               [24] 1361 	inc	dptr
      00B1BB F0               [24] 1362 	movx	@dptr,a
      00B1BC EF               [12] 1363 	mov	a,r7
      00B1BD A3               [24] 1364 	inc	dptr
      00B1BE F0               [24] 1365 	movx	@dptr,a
                                   1366 ;	quantum/vialrgb.c:124: if (length != VIAL_RAW_EPSIZE) return;
      00B1BF 90 0B 85         [24] 1367 	mov	dptr,#_vialrgb_get_value_PARM_2
      00B1C2 E0               [24] 1368 	movx	a,@dptr
      00B1C3 FF               [12] 1369 	mov	r7,a
      00B1C4 BF 20 02         [24] 1370 	cjne	r7,#0x20,00162$
      00B1C7 80 01            [24] 1371 	sjmp	00102$
      00B1C9                       1372 00162$:
      00B1C9 22               [24] 1373 	ret
      00B1CA                       1374 00102$:
                                   1375 ;	quantum/vialrgb.c:127: uint8_t VIALRGB_BUFFER *args = (uint8_t VIALRGB_BUFFER *)data + 2;
      00B1CA 90 0B 86         [24] 1376 	mov	dptr,#_vialrgb_get_value_data_10000_287
      00B1CD 12 B4 0A         [24] 1377 	lcall	_ak820_outline_0027
                                   1378 ;	quantum/vialrgb.c:128: uint8_t cmd = args[-1];
                                   1379 ;	quantum/vialrgb.c:129: switch (cmd) {
      00B1D0 BA 40 02         [24] 1380 	cjne	r2,#0x40,00163$
      00B1D3 80 18            [24] 1381 	sjmp	00103$
      00B1D5                       1382 00163$:
      00B1D5 BA 41 02         [24] 1383 	cjne	r2,#0x41,00164$
      00B1D8 80 25            [24] 1384 	sjmp	00104$
      00B1DA                       1385 00164$:
      00B1DA BA 42 03         [24] 1386 	cjne	r2,#0x42,00165$
      00B1DD 02 B2 A5         [24] 1387 	ljmp	00105$
      00B1E0                       1388 00165$:
      00B1E0 BA 43 03         [24] 1389 	cjne	r2,#0x43,00166$
      00B1E3 02 B2 B3         [24] 1390 	ljmp	00106$
      00B1E6                       1391 00166$:
      00B1E6 BA 44 03         [24] 1392 	cjne	r2,#0x44,00167$
      00B1E9 02 B2 BF         [24] 1393 	ljmp	00107$
      00B1EC                       1394 00167$:
      00B1EC 22               [24] 1395 	ret
                                   1396 ;	quantum/vialrgb.c:130: case vialrgb_get_info:
      00B1ED                       1397 00103$:
                                   1398 ;	quantum/vialrgb.c:131: args[0] = VIALRGB_PROTOCOL_VERSION & 0xFF;
      00B1ED 8B 82            [24] 1399 	mov	dpl,r3
      00B1EF 8C 83            [24] 1400 	mov	dph,r4
      00B1F1 74 01            [12] 1401 	mov	a,#0x01
      00B1F3 12 B3 EC         [24] 1402 	lcall	_ak820_outline_0023
                                   1403 ;	quantum/vialrgb.c:132: args[1] = VIALRGB_PROTOCOL_VERSION >> 8;
      00B1F6 E4               [12] 1404 	clr	a
      00B1F7 12 B3 EC         [24] 1405 	lcall	_ak820_outline_0023
                                   1406 ;	quantum/vialrgb.c:133: args[2] = RGB_MATRIX_MAXIMUM_BRIGHTNESS;
      00B1FA A3               [24] 1407 	inc	dptr
      00B1FB 74 A0            [12] 1408 	mov	a,#0xa0
      00B1FD F0               [24] 1409 	movx	@dptr,a
                                   1410 ;	quantum/vialrgb.c:134: break;
      00B1FE 22               [24] 1411 	ret
                                   1412 ;	quantum/vialrgb.c:135: case vialrgb_get_mode: {
      00B1FF                       1413 00104$:
                                   1414 ;	quantum/vialrgb.c:136: uint16_t vialrgb_id = get_mode();
      00B1FF C0 06            [24] 1415 	push	ar6
      00B201 C0 05            [24] 1416 	push	ar5
      00B203 C0 04            [24] 1417 	push	ar4
      00B205 C0 03            [24] 1418 	push	ar3
      00B207 12 AF B2         [24] 1419 	lcall	_get_mode
      00B20A A9 82            [24] 1420 	mov	r1, dpl
      00B20C AA 83            [24] 1421 	mov	r2, dph
      00B20E D0 03            [24] 1422 	pop	ar3
      00B210 D0 04            [24] 1423 	pop	ar4
      00B212 D0 05            [24] 1424 	pop	ar5
      00B214 D0 06            [24] 1425 	pop	ar6
                                   1426 ;	quantum/vialrgb.c:137: args[0] = vialrgb_id & 0xFF;
      00B216 89 00            [24] 1427 	mov	ar0,r1
      00B218 8B 82            [24] 1428 	mov	dpl,r3
      00B21A 8C 83            [24] 1429 	mov	dph,r4
      00B21C E8               [12] 1430 	mov	a,r0
      00B21D 12 B3 EC         [24] 1431 	lcall	_ak820_outline_0023
                                   1432 ;	quantum/vialrgb.c:138: args[1] = vialrgb_id >> 8;
      00B220 8A 01            [24] 1433 	mov	ar1,r2
      00B222 E9               [12] 1434 	mov	a,r1
      00B223 F0               [24] 1435 	movx	@dptr,a
                                   1436 ;	quantum/vialrgb.c:139: args[2] = rgb_matrix_get_speed();
      00B224 74 04            [12] 1437 	mov	a,#0x04
      00B226 2D               [12] 1438 	add	a, r5
      00B227 F9               [12] 1439 	mov	r1,a
      00B228 E4               [12] 1440 	clr	a
      00B229 3E               [12] 1441 	addc	a, r6
      00B22A FA               [12] 1442 	mov	r2,a
      00B22B C0 06            [24] 1443 	push	ar6
      00B22D C0 05            [24] 1444 	push	ar5
      00B22F C0 02            [24] 1445 	push	ar2
      00B231 C0 01            [24] 1446 	push	ar1
      00B233 12 4E F4         [24] 1447 	lcall	_rgb_matrix_get_speed
      00B236 A8 82            [24] 1448 	mov	r0, dpl
      00B238 D0 01            [24] 1449 	pop	ar1
      00B23A D0 02            [24] 1450 	pop	ar2
      00B23C D0 05            [24] 1451 	pop	ar5
      00B23E D0 06            [24] 1452 	pop	ar6
      00B240 89 82            [24] 1453 	mov	dpl,r1
      00B242 8A 83            [24] 1454 	mov	dph,r2
      00B244 E8               [12] 1455 	mov	a,r0
      00B245 F0               [24] 1456 	movx	@dptr,a
                                   1457 ;	quantum/vialrgb.c:140: args[3] = rgb_matrix_get_hue();
      00B246 74 05            [12] 1458 	mov	a,#0x05
      00B248 2D               [12] 1459 	add	a, r5
      00B249 F9               [12] 1460 	mov	r1,a
      00B24A E4               [12] 1461 	clr	a
      00B24B 3E               [12] 1462 	addc	a, r6
      00B24C FA               [12] 1463 	mov	r2,a
      00B24D C0 06            [24] 1464 	push	ar6
      00B24F C0 05            [24] 1465 	push	ar5
      00B251 C0 02            [24] 1466 	push	ar2
      00B253 C0 01            [24] 1467 	push	ar1
      00B255 12 4E DF         [24] 1468 	lcall	_rgb_matrix_get_hue
      00B258 A8 82            [24] 1469 	mov	r0, dpl
      00B25A D0 01            [24] 1470 	pop	ar1
      00B25C D0 02            [24] 1471 	pop	ar2
      00B25E D0 05            [24] 1472 	pop	ar5
      00B260 D0 06            [24] 1473 	pop	ar6
      00B262 89 82            [24] 1474 	mov	dpl,r1
      00B264 8A 83            [24] 1475 	mov	dph,r2
      00B266 E8               [12] 1476 	mov	a,r0
      00B267 F0               [24] 1477 	movx	@dptr,a
                                   1478 ;	quantum/vialrgb.c:141: args[4] = rgb_matrix_get_sat();
      00B268 74 06            [12] 1479 	mov	a,#0x06
      00B26A 2D               [12] 1480 	add	a, r5
      00B26B F9               [12] 1481 	mov	r1,a
      00B26C E4               [12] 1482 	clr	a
      00B26D 3E               [12] 1483 	addc	a, r6
      00B26E FA               [12] 1484 	mov	r2,a
      00B26F C0 06            [24] 1485 	push	ar6
      00B271 C0 05            [24] 1486 	push	ar5
      00B273 C0 02            [24] 1487 	push	ar2
      00B275 C0 01            [24] 1488 	push	ar1
      00B277 12 4E E6         [24] 1489 	lcall	_rgb_matrix_get_sat
      00B27A A8 82            [24] 1490 	mov	r0, dpl
      00B27C D0 01            [24] 1491 	pop	ar1
      00B27E D0 02            [24] 1492 	pop	ar2
      00B280 D0 05            [24] 1493 	pop	ar5
      00B282 D0 06            [24] 1494 	pop	ar6
      00B284 89 82            [24] 1495 	mov	dpl,r1
      00B286 8A 83            [24] 1496 	mov	dph,r2
      00B288 E8               [12] 1497 	mov	a,r0
      00B289 F0               [24] 1498 	movx	@dptr,a
                                   1499 ;	quantum/vialrgb.c:142: args[5] = rgb_matrix_get_val();
      00B28A 74 07            [12] 1500 	mov	a,#0x07
      00B28C 2D               [12] 1501 	add	a, r5
      00B28D F9               [12] 1502 	mov	r1,a
      00B28E E4               [12] 1503 	clr	a
      00B28F 3E               [12] 1504 	addc	a, r6
      00B290 FA               [12] 1505 	mov	r2,a
      00B291 C0 02            [24] 1506 	push	ar2
      00B293 C0 01            [24] 1507 	push	ar1
      00B295 12 4E ED         [24] 1508 	lcall	_rgb_matrix_get_val
      00B298 A8 82            [24] 1509 	mov	r0, dpl
      00B29A D0 01            [24] 1510 	pop	ar1
      00B29C D0 02            [24] 1511 	pop	ar2
      00B29E 89 82            [24] 1512 	mov	dpl,r1
      00B2A0 8A 83            [24] 1513 	mov	dph,r2
      00B2A2 E8               [12] 1514 	mov	a,r0
      00B2A3 F0               [24] 1515 	movx	@dptr,a
                                   1516 ;	quantum/vialrgb.c:143: break;
      00B2A4 22               [24] 1517 	ret
                                   1518 ;	quantum/vialrgb.c:145: case vialrgb_get_supported: {
      00B2A5                       1519 00105$:
                                   1520 ;	quantum/vialrgb.c:146: get_supported(args, length - 2);
      00B2A5 EF               [12] 1521 	mov	a,r7
      00B2A6 24 FE            [12] 1522 	add	a,#0xfe
      00B2A8 90 0B 72         [24] 1523 	mov	dptr,#_get_supported_PARM_2
      00B2AB F0               [24] 1524 	movx	@dptr,a
      00B2AC 8B 82            [24] 1525 	mov	dpl, r3
      00B2AE 8C 83            [24] 1526 	mov	dph, r4
                                   1527 ;	quantum/vialrgb.c:147: break;
      00B2B0 02 AE 85         [24] 1528 	ljmp	_get_supported
                                   1529 ;	quantum/vialrgb.c:150: case vialrgb_get_number_leds: {
      00B2B3                       1530 00106$:
                                   1531 ;	quantum/vialrgb.c:151: args[0] = RGB_MATRIX_LED_COUNT & 0xFF;
      00B2B3 8B 82            [24] 1532 	mov	dpl,r3
      00B2B5 8C 83            [24] 1533 	mov	dph,r4
      00B2B7 74 52            [12] 1534 	mov	a,#0x52
      00B2B9 12 B3 EC         [24] 1535 	lcall	_ak820_outline_0023
                                   1536 ;	quantum/vialrgb.c:152: args[1] = RGB_MATRIX_LED_COUNT >> 8;
      00B2BC E4               [12] 1537 	clr	a
      00B2BD F0               [24] 1538 	movx	@dptr,a
                                   1539 ;	quantum/vialrgb.c:153: break;
      00B2BE 22               [24] 1540 	ret
                                   1541 ;	quantum/vialrgb.c:155: case vialrgb_get_led_info: {
      00B2BF                       1542 00107$:
                                   1543 ;	quantum/vialrgb.c:156: uint16_t led = (uint16_t)args[0] | ((uint16_t)args[1] << 8);
      00B2BF 8B 82            [24] 1544 	mov	dpl,r3
      00B2C1 8C 83            [24] 1545 	mov	dph,r4
      00B2C3 E0               [24] 1546 	movx	a,@dptr
      00B2C4 FF               [12] 1547 	mov	r7,a
      00B2C5 7A 00            [12] 1548 	mov	r2,#0x00
      00B2C7 74 03            [12] 1549 	mov	a,#0x03
      00B2C9 2D               [12] 1550 	add	a, r5
      00B2CA F8               [12] 1551 	mov	r0,a
      00B2CB E4               [12] 1552 	clr	a
      00B2CC 3E               [12] 1553 	addc	a, r6
      00B2CD F9               [12] 1554 	mov	r1,a
      00B2CE C0 03            [24] 1555 	push	ar3
      00B2D0 C0 04            [24] 1556 	push	ar4
      00B2D2 88 82            [24] 1557 	mov	dpl,r0
      00B2D4 89 83            [24] 1558 	mov	dph,r1
      00B2D6 E0               [24] 1559 	movx	a,@dptr
      00B2D7 FB               [12] 1560 	mov	r3,a
      00B2D8 E4               [12] 1561 	clr	a
      00B2D9 4F               [12] 1562 	orl	a,r7
      00B2DA F5 57            [12] 1563 	mov	_vialrgb_get_value_sloc0_1_0,a
      00B2DC EB               [12] 1564 	mov	a,r3
      00B2DD 4A               [12] 1565 	orl	a,r2
      00B2DE F5 58            [12] 1566 	mov	(_vialrgb_get_value_sloc0_1_0 + 1),a
                                   1567 ;	quantum/vialrgb.c:157: if (led >= RGB_MATRIX_LED_COUNT) return;
      00B2E0 AC 57            [24] 1568 	mov	r4,_vialrgb_get_value_sloc0_1_0
      00B2E2 AF 58            [24] 1569 	mov	r7,(_vialrgb_get_value_sloc0_1_0 + 1)
      00B2E4 C3               [12] 1570 	clr	c
      00B2E5 EC               [12] 1571 	mov	a,r4
      00B2E6 94 52            [12] 1572 	subb	a,#0x52
      00B2E8 EF               [12] 1573 	mov	a,r7
      00B2E9 94 00            [12] 1574 	subb	a,#0x00
      00B2EB D0 04            [24] 1575 	pop	ar4
      00B2ED D0 03            [24] 1576 	pop	ar3
      00B2EF 40 01            [24] 1577 	jc	00109$
      00B2F1 22               [24] 1578 	ret
      00B2F2                       1579 00109$:
                                   1580 ;	quantum/vialrgb.c:159: args[0] = ak820_led_points[led].x;
      00B2F2 E5 57            [12] 1581 	mov	a,_vialrgb_get_value_sloc0_1_0
      00B2F4 25 57            [12] 1582 	add	a,_vialrgb_get_value_sloc0_1_0
      00B2F6 FA               [12] 1583 	mov	r2,a
      00B2F7 E5 58            [12] 1584 	mov	a,(_vialrgb_get_value_sloc0_1_0 + 1)
      00B2F9 33               [12] 1585 	rlc	a
      00B2FA FF               [12] 1586 	mov	r7,a
      00B2FB EA               [12] 1587 	mov	a,r2
      00B2FC 24 7D            [12] 1588 	add	a, #_ak820_led_points
      00B2FE F5 59            [12] 1589 	mov	_vialrgb_get_value_sloc1_1_0,a
      00B300 EF               [12] 1590 	mov	a,r7
      00B301 34 B8            [12] 1591 	addc	a, #(_ak820_led_points >> 8)
      00B303 F5 5A            [12] 1592 	mov	(_vialrgb_get_value_sloc1_1_0 + 1),a
      00B305 85 59 82         [24] 1593 	mov	dpl,_vialrgb_get_value_sloc1_1_0
      00B308 85 5A 83         [24] 1594 	mov	dph,(_vialrgb_get_value_sloc1_1_0 + 1)
      00B30B E4               [12] 1595 	clr	a
      00B30C 93               [24] 1596 	movc	a,@a+dptr
      00B30D 8B 82            [24] 1597 	mov	dpl,r3
      00B30F 8C 83            [24] 1598 	mov	dph,r4
      00B311 F0               [24] 1599 	movx	@dptr,a
                                   1600 ;	quantum/vialrgb.c:160: args[1] = ak820_led_points[led].y;
      00B312 85 59 82         [24] 1601 	mov	dpl,_vialrgb_get_value_sloc1_1_0
      00B315 85 5A 83         [24] 1602 	mov	dph,(_vialrgb_get_value_sloc1_1_0 + 1)
      00B318 A3               [24] 1603 	inc	dptr
      00B319 E4               [12] 1604 	clr	a
      00B31A 93               [24] 1605 	movc	a,@a+dptr
      00B31B 88 82            [24] 1606 	mov	dpl,r0
      00B31D 89 83            [24] 1607 	mov	dph,r1
      00B31F 12 B3 EC         [24] 1608 	lcall	_ak820_outline_0023
                                   1609 ;	quantum/vialrgb.c:161: args[2] = LED_FLAG_KEYLIGHT;
      00B322 A3               [24] 1610 	inc	dptr
      00B323 74 04            [12] 1611 	mov	a,#0x04
      00B325 F0               [24] 1612 	movx	@dptr,a
                                   1613 ;	quantum/vialrgb.c:170: get_matrix_pos_for_led(led, &args[3]);
      00B326 90 0B 7B         [24] 1614 	mov	dptr,#_get_matrix_pos_for_led_PARM_2
      00B329 04               [12] 1615 	inc	a
      00B32A 2D               [12] 1616 	add	a, r5
      00B32B F0               [24] 1617 	movx	@dptr,a
      00B32C E4               [12] 1618 	clr	a
      00B32D 3E               [12] 1619 	addc	a, r6
      00B32E A3               [24] 1620 	inc	dptr
      00B32F F0               [24] 1621 	movx	@dptr,a
      00B330 85 57 82         [24] 1622 	mov	dpl, _vialrgb_get_value_sloc0_1_0
      00B333 85 58 83         [24] 1623 	mov	dph, (_vialrgb_get_value_sloc0_1_0 + 1)
                                   1624 ;	quantum/vialrgb.c:174: }
                                   1625 ;	quantum/vialrgb.c:175: }
      00B336 02 AF FE         [24] 1626 	ljmp	_get_matrix_pos_for_led
                                   1627 ;------------------------------------------------------------
                                   1628 ;Allocation info for local variables in function 'vialrgb_set_value'
                                   1629 ;------------------------------------------------------------
                                   1630 ;sloc0         Allocated with name '_vialrgb_set_value_sloc0_1_0'
                                   1631 ;length        Allocated with name '_vialrgb_set_value_PARM_2'
                                   1632 ;data          Allocated with name '_vialrgb_set_value_data_10000_298'
                                   1633 ;args          Allocated with name '_vialrgb_set_value_args_10001_301'
                                   1634 ;cmd           Allocated with name '_vialrgb_set_value_cmd_10001_301'
                                   1635 ;vialrgb_id    Allocated with name '_vialrgb_set_value_vialrgb_id_40001_304'
                                   1636 ;------------------------------------------------------------
                                   1637 ;	quantum/vialrgb.c:177: void vialrgb_set_value(uint8_t *data, uint8_t length) {
                                   1638 ;	-----------------------------------------
                                   1639 ;	 function vialrgb_set_value
                                   1640 ;	-----------------------------------------
      00B339                       1641 _vialrgb_set_value:
      00B339 AF F0            [24] 1642 	mov	r7,b
      00B33B AE 83            [24] 1643 	mov	r6,dph
      00B33D E5 82            [12] 1644 	mov	a,dpl
      00B33F 90 0B 8A         [24] 1645 	mov	dptr,#_vialrgb_set_value_data_10000_298
      00B342 F0               [24] 1646 	movx	@dptr,a
      00B343 EE               [12] 1647 	mov	a,r6
      00B344 A3               [24] 1648 	inc	dptr
      00B345 F0               [24] 1649 	movx	@dptr,a
      00B346 EF               [12] 1650 	mov	a,r7
      00B347 A3               [24] 1651 	inc	dptr
      00B348 F0               [24] 1652 	movx	@dptr,a
                                   1653 ;	quantum/vialrgb.c:178: if (length != VIAL_RAW_EPSIZE) return;
      00B349 90 0B 89         [24] 1654 	mov	dptr,#_vialrgb_set_value_PARM_2
      00B34C E0               [24] 1655 	movx	a,@dptr
      00B34D FF               [12] 1656 	mov	r7,a
      00B34E BF 20 02         [24] 1657 	cjne	r7,#0x20,00129$
      00B351 80 01            [24] 1658 	sjmp	00102$
      00B353                       1659 00129$:
      00B353 22               [24] 1660 	ret
      00B354                       1661 00102$:
                                   1662 ;	quantum/vialrgb.c:181: uint8_t VIALRGB_BUFFER *args = (uint8_t VIALRGB_BUFFER *)data + 2;
      00B354 90 0B 8A         [24] 1663 	mov	dptr,#_vialrgb_set_value_data_10000_298
      00B357 12 B4 0A         [24] 1664 	lcall	_ak820_outline_0027
                                   1665 ;	quantum/vialrgb.c:182: uint8_t cmd = args[-1];
                                   1666 ;	quantum/vialrgb.c:183: switch (cmd) {
      00B35A BA 41 02         [24] 1667 	cjne	r2,#0x41,00130$
      00B35D 80 06            [24] 1668 	sjmp	00103$
      00B35F                       1669 00130$:
      00B35F BA 42 02         [24] 1670 	cjne	r2,#0x42,00131$
      00B362 80 77            [24] 1671 	sjmp	00104$
      00B364                       1672 00131$:
      00B364 22               [24] 1673 	ret
                                   1674 ;	quantum/vialrgb.c:184: case vialrgb_set_mode: {
      00B365                       1675 00103$:
                                   1676 ;	quantum/vialrgb.c:185: uint16_t vialrgb_id = args[0] | (args[1] << 8);
      00B365 8B 82            [24] 1677 	mov	dpl,r3
      00B367 8C 83            [24] 1678 	mov	dph,r4
      00B369 E0               [24] 1679 	movx	a,@dptr
      00B36A FA               [12] 1680 	mov	r2,a
      00B36B 8D 82            [24] 1681 	mov	dpl,r5
      00B36D 8E 83            [24] 1682 	mov	dph,r6
      00B36F A3               [24] 1683 	inc	dptr
      00B370 A3               [24] 1684 	inc	dptr
      00B371 A3               [24] 1685 	inc	dptr
      00B372 E0               [24] 1686 	movx	a,@dptr
      00B373 F8               [12] 1687 	mov	r0,a
      00B374 79 00            [12] 1688 	mov	r1,#0x00
      00B376 88 5C            [24] 1689 	mov	(_vialrgb_set_value_sloc0_1_0 + 1),r0
      00B378 89 5B            [24] 1690 	mov	_vialrgb_set_value_sloc0_1_0,r1
      00B37A 8A 01            [24] 1691 	mov	ar1,r2
      00B37C 7A 00            [12] 1692 	mov	r2,#0x00
      00B37E E5 5C            [12] 1693 	mov	a,(_vialrgb_set_value_sloc0_1_0 + 1)
      00B380 42 02            [12] 1694 	orl	ar2,a
                                   1695 ;	quantum/vialrgb.c:186: set_mode(vialrgb_id);
      00B382 89 82            [24] 1696 	mov	dpl, r1
      00B384 8A 83            [24] 1697 	mov	dph, r2
      00B386 C0 06            [24] 1698 	push	ar6
      00B388 C0 05            [24] 1699 	push	ar5
      00B38A 12 AF C7         [24] 1700 	lcall	_set_mode
      00B38D D0 05            [24] 1701 	pop	ar5
      00B38F D0 06            [24] 1702 	pop	ar6
                                   1703 ;	quantum/vialrgb.c:187: rgb_matrix_set_speed_noeeprom(args[2]);
      00B391 8D 82            [24] 1704 	mov	dpl,r5
      00B393 8E 83            [24] 1705 	mov	dph,r6
      00B395 A3               [24] 1706 	inc	dptr
      00B396 A3               [24] 1707 	inc	dptr
      00B397 A3               [24] 1708 	inc	dptr
      00B398 A3               [24] 1709 	inc	dptr
      00B399 E0               [24] 1710 	movx	a,@dptr
      00B39A F5 82            [12] 1711 	mov	dpl,a
      00B39C C0 06            [24] 1712 	push	ar6
      00B39E C0 05            [24] 1713 	push	ar5
      00B3A0 12 4F F5         [24] 1714 	lcall	_rgb_matrix_set_speed_noeeprom
      00B3A3 D0 05            [24] 1715 	pop	ar5
      00B3A5 D0 06            [24] 1716 	pop	ar6
                                   1717 ;	quantum/vialrgb.c:188: rgb_matrix_sethsv_noeeprom(args[3], args[4], args[5]);
      00B3A7 8D 82            [24] 1718 	mov	dpl,r5
      00B3A9 8E 83            [24] 1719 	mov	dph,r6
      00B3AB A3               [24] 1720 	inc	dptr
      00B3AC A3               [24] 1721 	inc	dptr
      00B3AD A3               [24] 1722 	inc	dptr
      00B3AE A3               [24] 1723 	inc	dptr
      00B3AF A3               [24] 1724 	inc	dptr
      00B3B0 E0               [24] 1725 	movx	a,@dptr
      00B3B1 F9               [12] 1726 	mov	r1,a
      00B3B2 7A 00            [12] 1727 	mov	r2,#0x00
      00B3B4 74 06            [12] 1728 	mov	a,#0x06
      00B3B6 2D               [12] 1729 	add	a, r5
      00B3B7 F5 82            [12] 1730 	mov	dpl,a
      00B3B9 E4               [12] 1731 	clr	a
      00B3BA 3E               [12] 1732 	addc	a, r6
      00B3BB F5 83            [12] 1733 	mov	dph,a
      00B3BD E0               [24] 1734 	movx	a,@dptr
      00B3BE F8               [12] 1735 	mov	r0,a
      00B3BF 74 07            [12] 1736 	mov	a,#0x07
      00B3C1 2D               [12] 1737 	add	a, r5
      00B3C2 F5 82            [12] 1738 	mov	dpl,a
      00B3C4 E4               [12] 1739 	clr	a
      00B3C5 3E               [12] 1740 	addc	a, r6
      00B3C6 F5 83            [12] 1741 	mov	dph,a
      00B3C8 E0               [24] 1742 	movx	a,@dptr
      00B3C9 FE               [12] 1743 	mov	r6,a
      00B3CA 90 06 51         [24] 1744 	mov	dptr,#_rgb_matrix_sethsv_noeeprom_PARM_2
      00B3CD E8               [12] 1745 	mov	a,r0
      00B3CE F0               [24] 1746 	movx	@dptr,a
      00B3CF 90 06 52         [24] 1747 	mov	dptr,#_rgb_matrix_sethsv_noeeprom_PARM_3
      00B3D2 EE               [12] 1748 	mov	a,r6
      00B3D3 F0               [24] 1749 	movx	@dptr,a
      00B3D4 89 82            [24] 1750 	mov	dpl, r1
      00B3D6 8A 83            [24] 1751 	mov	dph, r2
                                   1752 ;	quantum/vialrgb.c:189: break;
                                   1753 ;	quantum/vialrgb.c:192: case vialrgb_direct_fastset: {
      00B3D8 02 4F C4         [24] 1754 	ljmp	_rgb_matrix_sethsv_noeeprom
      00B3DB                       1755 00104$:
                                   1756 ;	quantum/vialrgb.c:193: fast_set_leds(args, length - 2);
      00B3DB EF               [12] 1757 	mov	a,r7
      00B3DC 24 FE            [12] 1758 	add	a,#0xfe
      00B3DE 90 0B 7F         [24] 1759 	mov	dptr,#_fast_set_leds_PARM_2
      00B3E1 F0               [24] 1760 	movx	@dptr,a
      00B3E2 8B 82            [24] 1761 	mov	dpl, r3
      00B3E4 8C 83            [24] 1762 	mov	dph, r4
                                   1763 ;	quantum/vialrgb.c:197: }
                                   1764 ;	quantum/vialrgb.c:198: }
      00B3E6 02 B0 3B         [24] 1765 	ljmp	_fast_set_leds
                                   1766 ;------------------------------------------------------------
                                   1767 ;Allocation info for local variables in function 'vialrgb_save'
                                   1768 ;------------------------------------------------------------
                                   1769 ;length        Allocated with name '_vialrgb_save_PARM_2'
                                   1770 ;data          Allocated with name '_vialrgb_save_data_10000_306'
                                   1771 ;------------------------------------------------------------
                                   1772 ;	quantum/vialrgb.c:200: void vialrgb_save(uint8_t *data, uint8_t length) {
                                   1773 ;	-----------------------------------------
                                   1774 ;	 function vialrgb_save
                                   1775 ;	-----------------------------------------
      00B3E9                       1776 _vialrgb_save:
                                   1777 ;	quantum/vialrgb.c:204: eeconfig_update_rgb_matrix();
                                   1778 ;	quantum/vialrgb.c:205: }
      00B3E9 02 48 B2         [24] 1779 	ljmp	_eeconfig_update_rgb_matrix
                                   1780 	.area CSEG    (CODE)
                                   1781 	.area CONST   (CODE)
                                   1782 	.area CONST   (CODE)
      00BBB1                       1783 _supported_modes:
      00BBB1 00 00                 1784 	.byte #0x00, #0x00	; 0
      00BBB3 00 00                 1785 	.byte #0x00, #0x00	; 0
      00BBB5 01 00                 1786 	.byte #0x01, #0x00	; 1
      00BBB7 05 00                 1787 	.byte #0x05, #0x00	; 5
      00BBB9 02 00                 1788 	.byte #0x02, #0x00	; 2
      00BBBB 01 00                 1789 	.byte #0x01, #0x00	; 1
      00BBBD 06 00                 1790 	.byte #0x06, #0x00	; 6
      00BBBF 02 00                 1791 	.byte #0x02, #0x00	; 2
      00BBC1 0D 00                 1792 	.byte #0x0d, #0x00	; 13
      00BBC3 03 00                 1793 	.byte #0x03, #0x00	; 3
      00BBC5 0E 00                 1794 	.byte #0x0e, #0x00	; 14
      00BBC7 04 00                 1795 	.byte #0x04, #0x00	; 4
      00BBC9 1F 00                 1796 	.byte #0x1f, #0x00	; 31
      00BBCB 06 00                 1797 	.byte #0x06, #0x00	; 6
                                   1798 	.area CSEG    (CODE)
                                   1799 	.area XINIT   (CODE)
                                   1800 	.area CABS    (ABS,CODE)
                                   1801 
                                   1802 ; Experimental exact instruction outlining.
                                   1803 	.globl _ak820_outline_0013
                                   1804 	.globl _ak820_outline_0023
                                   1805 	.globl _ak820_outline_0025
                                   1806 	.globl _ak820_outline_0027
                                   1807 
                                   1808 	.area CSEG (CODE)
                                   1809 ; function ak820_outline_0023
      00B3EC                       1810 _ak820_outline_0023:
      00B3EC F0               [24] 1811 	movx	@dptr,a
      00B3ED 8D 82            [24] 1812 	mov	dpl,r5
      00B3EF 8E 83            [24] 1813 	mov	dph,r6
      00B3F1 A3               [24] 1814 	inc	dptr
      00B3F2 A3               [24] 1815 	inc	dptr
      00B3F3 A3               [24] 1816 	inc	dptr
      00B3F4 22               [24] 1817 	ret
                                   1818 
                                   1819 	.area CSEG (CODE)
                                   1820 ; function ak820_outline_0025
      00B3F5                       1821 _ak820_outline_0025:
      00B3F5 ED               [12] 1822 	mov	a,r5
      00B3F6 75 F0 04         [24] 1823 	mov	b,#0x04
      00B3F9 A4               [48] 1824 	mul	ab
      00B3FA 24 B1            [12] 1825 	add	a,#_supported_modes
      00B3FC FB               [12] 1826 	mov	r3,a
      00B3FD 74 BB            [12] 1827 	mov	a,#(_supported_modes>>8)
      00B3FF 35 F0            [12] 1828 	addc	a,b
      00B401 FC               [12] 1829 	mov	r4,a
      00B402 8B 82            [24] 1830 	mov	dpl,r3
      00B404 8C 83            [24] 1831 	mov	dph,r4
      00B406 A3               [24] 1832 	inc	dptr
      00B407 A3               [24] 1833 	inc	dptr
      00B408 E4               [12] 1834 	clr	a
      00B409 22               [24] 1835 	ret
                                   1836 
                                   1837 	.area CSEG (CODE)
                                   1838 ; function ak820_outline_0027
      00B40A                       1839 _ak820_outline_0027:
      00B40A E0               [24] 1840 	movx	a,@dptr
      00B40B FD               [12] 1841 	mov	r5,a
      00B40C A3               [24] 1842 	inc	dptr
      00B40D E0               [24] 1843 	movx	a,@dptr
      00B40E FE               [12] 1844 	mov	r6,a
      00B40F 74 02            [12] 1845 	mov	a,#0x02
      00B411 2D               [12] 1846 	add	a,r5
      00B412 FB               [12] 1847 	mov	r3,a
      00B413 E4               [12] 1848 	clr	a
      00B414 3E               [12] 1849 	addc	a,r6
      00B415 FC               [12] 1850 	mov	r4,a
      00B416 8D 82            [24] 1851 	mov	dpl,r5
      00B418 8E 83            [24] 1852 	mov	dph,r6
      00B41A A3               [24] 1853 	inc	dptr
      00B41B E0               [24] 1854 	movx	a,@dptr
      00B41C FA               [12] 1855 	mov	r2,a
      00B41D 22               [24] 1856 	ret
