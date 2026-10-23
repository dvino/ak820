                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module keymap_introspection
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _ak820_led_points
                                     12 	.globl _encoder_map
                                     13 	.globl _keymaps
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
                                    257 	.globl _keycode_at_encodermap_location_raw_PARM_3
                                    258 	.globl _keycode_at_encodermap_location_raw_PARM_2
                                    259 	.globl _keycode_at_keymap_location_raw_PARM_3
                                    260 	.globl _keycode_at_keymap_location_raw_PARM_2
                                    261 	.globl _keyboard_post_init_user
                                    262 	.globl _keycode_at_keymap_location_raw
                                    263 	.globl _keycode_at_encodermap_location_raw
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
      000993                        550 _keycode_at_keymap_location_raw_PARM_2:
      000993                        551 	.ds 1
      000994                        552 _keycode_at_keymap_location_raw_PARM_3:
      000994                        553 	.ds 1
      000995                        554 _keycode_at_keymap_location_raw_layer_num_10000_585:
      000995                        555 	.ds 1
      000996                        556 _keycode_at_encodermap_location_raw_PARM_2:
      000996                        557 	.ds 1
      000997                        558 _keycode_at_encodermap_location_raw_PARM_3:
      000997                        559 	.ds 1
      000998                        560 _keycode_at_encodermap_location_raw_layer_num_10000_593:
      000998                        561 	.ds 1
                                    562 ;--------------------------------------------------------
                                    563 ; absolute external ram data
                                    564 ;--------------------------------------------------------
                                    565 	.area XABS    (ABS,XDATA)
                                    566 ;--------------------------------------------------------
                                    567 ; initialized external ram data
                                    568 ;--------------------------------------------------------
                                    569 	.area XISEG   (XDATA)
                                    570 	.area HOME    (CODE)
                                    571 	.area GSINIT0 (CODE)
                                    572 	.area GSINIT1 (CODE)
                                    573 	.area GSINIT2 (CODE)
                                    574 	.area GSINIT3 (CODE)
                                    575 	.area GSINIT4 (CODE)
                                    576 	.area GSINIT5 (CODE)
                                    577 	.area GSINIT  (CODE)
                                    578 	.area GSFINAL (CODE)
                                    579 	.area CSEG    (CODE)
                                    580 ;--------------------------------------------------------
                                    581 ; global & static initialisations
                                    582 ;--------------------------------------------------------
                                    583 	.area HOME    (CODE)
                                    584 	.area GSINIT  (CODE)
                                    585 	.area GSFINAL (CODE)
                                    586 	.area GSINIT  (CODE)
                                    587 ;--------------------------------------------------------
                                    588 ; Home
                                    589 ;--------------------------------------------------------
                                    590 	.area HOME    (CODE)
                                    591 	.area HOME    (CODE)
                                    592 ;--------------------------------------------------------
                                    593 ; code
                                    594 ;--------------------------------------------------------
                                    595 	.area CSEG    (CODE)
                                    596 ;------------------------------------------------------------
                                    597 ;Allocation info for local variables in function 'rgb_matrix_check_finished_leds'
                                    598 ;------------------------------------------------------------
                                    599 ;led_idx       Allocated with name '_rgb_matrix_check_finished_leds_led_idx_10000_193'
                                    600 ;------------------------------------------------------------
                                    601 ;	quantum/rgb_matrix/rgb_matrix.h:260: static inline bool rgb_matrix_check_finished_leds(uint8_t led_idx) {
                                    602 ;	-----------------------------------------
                           000007   603 	ar7 = 0x07
                           000006   604 	ar6 = 0x06
                           000005   605 	ar5 = 0x05
                           000004   606 	ar4 = 0x04
                           000003   607 	ar3 = 0x03
                           000002   608 	ar2 = 0x02
                           000001   609 	ar1 = 0x01
                           000000   610 	ar0 = 0x00
                                    611 ;	 function keyboard_post_init_user
                                    612 ;	-----------------------------------------
      009012                        613 _keyboard_post_init_user:
      009012 22               [24]  614 	ret
                                    615 ;------------------------------------------------------------
                                    616 ;Allocation info for local variables in function 'keymap_layer_count_raw'
                                    617 ;------------------------------------------------------------
                                    618 ;	quantum/keymap_introspection.c:20: uint8_t keymap_layer_count_raw(void) {
                                    619 ;	-----------------------------------------
                                    620 ;	 function keycode_at_keymap_location_raw
                                    621 ;	-----------------------------------------
      009013                        622 _keycode_at_keymap_location_raw:
      009013 E5 82            [12]  623 	mov	a,dpl
      009015 90 09 95         [24]  624 	mov	dptr,#_keycode_at_keymap_location_raw_layer_num_10000_585
      009018 F0               [24]  625 	movx	@dptr,a
                                    626 ;	quantum/keymap_introspection.c:37: if (layer_num < NUM_KEYMAP_LAYERS_RAW && row < MATRIX_ROWS && column < MATRIX_COLS) {
      009019 E0               [24]  627 	movx	a,@dptr
      00901A FF               [12]  628 	mov	r7,a
      00901B BF 02 00         [24]  629 	cjne	r7,#0x02,00128$
      00901E                        630 00128$:
      00901E 50 3E            [24]  631 	jnc	00102$
      009020 90 09 93         [24]  632 	mov	dptr,#_keycode_at_keymap_location_raw_PARM_2
      009023 E0               [24]  633 	movx	a,@dptr
      009024 FE               [12]  634 	mov	r6,a
      009025 BE 10 00         [24]  635 	cjne	r6,#0x10,00130$
      009028                        636 00130$:
      009028 50 34            [24]  637 	jnc	00102$
      00902A 90 09 94         [24]  638 	mov	dptr,#_keycode_at_keymap_location_raw_PARM_3
      00902D E0               [24]  639 	movx	a,@dptr
      00902E FD               [12]  640 	mov	r5,a
      00902F BD 08 00         [24]  641 	cjne	r5,#0x08,00132$
      009032                        642 00132$:
      009032 50 2A            [24]  643 	jnc	00102$
                                    644 ;	quantum/keymap_introspection.c:38: return pgm_read_word(&keymaps[layer_num][row][column]);
      009034 8F 04            [24]  645 	mov	ar4,r7
      009036 E4               [12]  646 	clr	a
      009037 24 78            [12]  647 	add	a,#_keymaps
      009039 FF               [12]  648 	mov	r7,a
      00903A EC               [12]  649 	mov	a,r4
      00903B 34 B6            [12]  650 	addc	a, #(_keymaps >> 8)
      00903D FC               [12]  651 	mov	r4,a
      00903E EE               [12]  652 	mov	a,r6
      00903F 75 F0 10         [24]  653 	mov	b,#0x10
      009042 A4               [48]  654 	mul	ab
      009043 2F               [12]  655 	add	a, r7
      009044 FF               [12]  656 	mov	r7,a
      009045 EC               [12]  657 	mov	a,r4
      009046 35 F0            [12]  658 	addc	a, b
      009048 FC               [12]  659 	mov	r4,a
      009049 ED               [12]  660 	mov	a,r5
      00904A 2D               [12]  661 	add	a,r5
      00904B 2F               [12]  662 	add	a, r7
      00904C F5 82            [12]  663 	mov	dpl,a
      00904E E4               [12]  664 	clr	a
      00904F 3C               [12]  665 	addc	a, r4
      009050 F5 83            [12]  666 	mov	dph,a
      009052 E4               [12]  667 	clr	a
      009053 93               [24]  668 	movc	a,@a+dptr
      009054 FE               [12]  669 	mov	r6,a
      009055 A3               [24]  670 	inc	dptr
      009056 E4               [12]  671 	clr	a
      009057 93               [24]  672 	movc	a,@a+dptr
      009058 FF               [12]  673 	mov	r7,a
      009059 8E 82            [24]  674 	mov	dpl, r6
      00905B 8F 83            [24]  675 	mov	dph, r7
      00905D 22               [24]  676 	ret
      00905E                        677 00102$:
                                    678 ;	quantum/keymap_introspection.c:40: return KC_TRNS;
      00905E 90 00 01         [24]  679 	mov	dptr,#0x0001
                                    680 ;	quantum/keymap_introspection.c:41: }
      009061 22               [24]  681 	ret
                                    682 ;------------------------------------------------------------
                                    683 ;Allocation info for local variables in function 'encodermap_layer_count_raw'
                                    684 ;------------------------------------------------------------
                                    685 ;	quantum/keymap_introspection.c:56: uint8_t encodermap_layer_count_raw(void) {
                                    686 ;	-----------------------------------------
                                    687 ;	 function keycode_at_encodermap_location_raw
                                    688 ;	-----------------------------------------
      009062                        689 _keycode_at_encodermap_location_raw:
      009062 E5 82            [12]  690 	mov	a,dpl
      009064 90 09 98         [24]  691 	mov	dptr,#_keycode_at_encodermap_location_raw_layer_num_10000_593
      009067 F0               [24]  692 	movx	@dptr,a
                                    693 ;	quantum/keymap_introspection.c:67: if (layer_num < NUM_ENCODERMAP_LAYERS_RAW && encoder_idx < NUM_ENCODERS) {
      009068 E0               [24]  694 	movx	a,@dptr
      009069 FF               [12]  695 	mov	r7,a
      00906A BF 02 00         [24]  696 	cjne	r7,#0x02,00129$
      00906D                        697 00129$:
      00906D 50 44            [24]  698 	jnc	00102$
      00906F 90 09 96         [24]  699 	mov	dptr,#_keycode_at_encodermap_location_raw_PARM_2
      009072 E0               [24]  700 	movx	a,@dptr
      009073 FE               [12]  701 	mov	r6,a
      009074 BE 01 00         [24]  702 	cjne	r6,#0x01,00131$
      009077                        703 00131$:
      009077 50 3A            [24]  704 	jnc	00102$
                                    705 ;	quantum/keymap_introspection.c:68: return pgm_read_word(&encoder_map[layer_num][encoder_idx][clockwise ? 0 : 1]);
      009079 EF               [12]  706 	mov	a,r7
      00907A 75 F0 04         [24]  707 	mov	b,#0x04
      00907D A4               [48]  708 	mul	ab
      00907E 24 78            [12]  709 	add	a, #_encoder_map
      009080 FE               [12]  710 	mov	r6,a
      009081 74 B8            [12]  711 	mov	a,#(_encoder_map >> 8)
      009083 35 F0            [12]  712 	addc	a, b
      009085 FF               [12]  713 	mov	r7,a
      009086 E4               [12]  714 	clr	a
      009087 2F               [12]  715 	add	a, r7
      009088 FF               [12]  716 	mov	r7,a
      009089 90 09 97         [24]  717 	mov	dptr,#_keycode_at_encodermap_location_raw_PARM_3
      00908C E0               [24]  718 	movx	a,@dptr
      00908D 60 06            [24]  719 	jz	00106$
      00908F 7C 00            [12]  720 	mov	r4,#0x00
      009091 7D 00            [12]  721 	mov	r5,#0x00
      009093 80 04            [24]  722 	sjmp	00107$
      009095                        723 00106$:
      009095 7C 01            [12]  724 	mov	r4,#0x01
      009097 7D 00            [12]  725 	mov	r5,#0x00
      009099                        726 00107$:
      009099 EC               [12]  727 	mov	a,r4
      00909A 2C               [12]  728 	add	a,r4
      00909B FC               [12]  729 	mov	r4,a
      00909C ED               [12]  730 	mov	a,r5
      00909D 33               [12]  731 	rlc	a
      00909E FD               [12]  732 	mov	r5,a
      00909F EC               [12]  733 	mov	a,r4
      0090A0 2E               [12]  734 	add	a, r6
      0090A1 F5 82            [12]  735 	mov	dpl,a
      0090A3 ED               [12]  736 	mov	a,r5
      0090A4 3F               [12]  737 	addc	a, r7
      0090A5 F5 83            [12]  738 	mov	dph,a
      0090A7 E4               [12]  739 	clr	a
      0090A8 93               [24]  740 	movc	a,@a+dptr
      0090A9 FE               [12]  741 	mov	r6,a
      0090AA A3               [24]  742 	inc	dptr
      0090AB E4               [12]  743 	clr	a
      0090AC 93               [24]  744 	movc	a,@a+dptr
      0090AD FF               [12]  745 	mov	r7,a
      0090AE 8E 82            [24]  746 	mov	dpl, r6
      0090B0 8F 83            [24]  747 	mov	dph, r7
      0090B2 22               [24]  748 	ret
      0090B3                        749 00102$:
                                    750 ;	quantum/keymap_introspection.c:70: return KC_TRNS;
      0090B3 90 00 01         [24]  751 	mov	dptr,#0x0001
                                    752 ;	quantum/keymap_introspection.c:71: }
      0090B6 22               [24]  753 	ret
                                    754 	.area CSEG    (CODE)
                                    755 	.area CONST   (CODE)
                                    756 	.area CONST   (CODE)
      00B678                        757 _keymaps:
      00B678 29 00                  758 	.byte #0x29, #0x00	; 41
      00B67A 35 00                  759 	.byte #0x35, #0x00	; 53
      00B67C 2B 00                  760 	.byte #0x2b, #0x00	; 43
      00B67E 39 00                  761 	.byte #0x39, #0x00	; 57
      00B680 E1 00                  762 	.byte #0xe1, #0x00	; 225
      00B682 E0 00                  763 	.byte #0xe0, #0x00	; 224
      00B684 00 00                  764 	.byte #0x00, #0x00	; 0
      00B686 00 00                  765 	.byte #0x00, #0x00	; 0
      00B688 3A 00                  766 	.byte #0x3a, #0x00	; 58
      00B68A 1E 00                  767 	.byte #0x1e, #0x00	; 30
      00B68C 14 00                  768 	.byte #0x14, #0x00	; 20
      00B68E 04 00                  769 	.byte #0x04, #0x00	; 4
      00B690 00 00                  770 	.byte #0x00, #0x00	; 0
      00B692 E3 00                  771 	.byte #0xe3, #0x00	; 227
      00B694 00 00                  772 	.byte #0x00, #0x00	; 0
      00B696 00 00                  773 	.byte #0x00, #0x00	; 0
      00B698 3B 00                  774 	.byte #0x3b, #0x00	; 59
      00B69A 1F 00                  775 	.byte #0x1f, #0x00	; 31
      00B69C 1A 00                  776 	.byte #0x1a, #0x00	; 26
      00B69E 16 00                  777 	.byte #0x16, #0x00	; 22
      00B6A0 1D 00                  778 	.byte #0x1d, #0x00	; 29
      00B6A2 E2 00                  779 	.byte #0xe2, #0x00	; 226
      00B6A4 00 00                  780 	.byte #0x00, #0x00	; 0
      00B6A6 00 00                  781 	.byte #0x00, #0x00	; 0
      00B6A8 3C 00                  782 	.byte #0x3c, #0x00	; 60
      00B6AA 20 00                  783 	.byte #0x20, #0x00	; 32
      00B6AC 08 00                  784 	.byte #0x08, #0x00	; 8
      00B6AE 07 00                  785 	.byte #0x07, #0x00	; 7
      00B6B0 1B 00                  786 	.byte #0x1b, #0x00	; 27
      00B6B2 00 00                  787 	.byte #0x00, #0x00	; 0
      00B6B4 00 00                  788 	.byte #0x00, #0x00	; 0
      00B6B6 00 00                  789 	.byte #0x00, #0x00	; 0
      00B6B8 3D 00                  790 	.byte #0x3d, #0x00	; 61
      00B6BA 21 00                  791 	.byte #0x21, #0x00	; 33
      00B6BC 15 00                  792 	.byte #0x15, #0x00	; 21
      00B6BE 09 00                  793 	.byte #0x09, #0x00	; 9
      00B6C0 06 00                  794 	.byte #0x06, #0x00	; 6
      00B6C2 00 00                  795 	.byte #0x00, #0x00	; 0
      00B6C4 00 00                  796 	.byte #0x00, #0x00	; 0
      00B6C6 00 00                  797 	.byte #0x00, #0x00	; 0
      00B6C8 3E 00                  798 	.byte #0x3e, #0x00	; 62
      00B6CA 22 00                  799 	.byte #0x22, #0x00	; 34
      00B6CC 17 00                  800 	.byte #0x17, #0x00	; 23
      00B6CE 0A 00                  801 	.byte #0x0a, #0x00	; 10
      00B6D0 19 00                  802 	.byte #0x19, #0x00	; 25
      00B6D2 2C 00                  803 	.byte #0x2c, #0x00	; 44
      00B6D4 00 00                  804 	.byte #0x00, #0x00	; 0
      00B6D6 00 00                  805 	.byte #0x00, #0x00	; 0
      00B6D8 3F 00                  806 	.byte #0x3f, #0x00	; 63
      00B6DA 23 00                  807 	.byte #0x23, #0x00	; 35
      00B6DC 1C 00                  808 	.byte #0x1c, #0x00	; 28
      00B6DE 0B 00                  809 	.byte #0x0b, #0x00	; 11
      00B6E0 05 00                  810 	.byte #0x05, #0x00	; 5
      00B6E2 00 00                  811 	.byte #0x00, #0x00	; 0
      00B6E4 00 00                  812 	.byte #0x00, #0x00	; 0
      00B6E6 00 00                  813 	.byte #0x00, #0x00	; 0
      00B6E8 40 00                  814 	.byte #0x40, #0x00	; 64
      00B6EA 24 00                  815 	.byte #0x24, #0x00	; 36
      00B6EC 18 00                  816 	.byte #0x18, #0x00	; 24
      00B6EE 0D 00                  817 	.byte #0x0d, #0x00	; 13
      00B6F0 11 00                  818 	.byte #0x11, #0x00	; 17
      00B6F2 00 00                  819 	.byte #0x00, #0x00	; 0
      00B6F4 00 00                  820 	.byte #0x00, #0x00	; 0
      00B6F6 00 00                  821 	.byte #0x00, #0x00	; 0
      00B6F8 41 00                  822 	.byte #0x41, #0x00	; 65
      00B6FA 25 00                  823 	.byte #0x25, #0x00	; 37
      00B6FC 0C 00                  824 	.byte #0x0c, #0x00	; 12
      00B6FE 0E 00                  825 	.byte #0x0e, #0x00	; 14
      00B700 10 00                  826 	.byte #0x10, #0x00	; 16
      00B702 00 00                  827 	.byte #0x00, #0x00	; 0
      00B704 00 00                  828 	.byte #0x00, #0x00	; 0
      00B706 00 00                  829 	.byte #0x00, #0x00	; 0
      00B708 42 00                  830 	.byte #0x42, #0x00	; 66
      00B70A 26 00                  831 	.byte #0x26, #0x00	; 38
      00B70C 12 00                  832 	.byte #0x12, #0x00	; 18
      00B70E 0F 00                  833 	.byte #0x0f, #0x00	; 15
      00B710 36 00                  834 	.byte #0x36, #0x00	; 54
      00B712 E6 00                  835 	.byte #0xe6, #0x00	; 230
      00B714 00 00                  836 	.byte #0x00, #0x00	; 0
      00B716 00 00                  837 	.byte #0x00, #0x00	; 0
      00B718 43 00                  838 	.byte #0x43, #0x00	; 67
      00B71A 27 00                  839 	.byte #0x27, #0x00	; 39
      00B71C 13 00                  840 	.byte #0x13, #0x00	; 19
      00B71E 33 00                  841 	.byte #0x33, #0x00	; 51
      00B720 37 00                  842 	.byte #0x37, #0x00	; 55
      00B722 21 52                  843 	.byte #0x21, #0x52	; 21025
      00B724 00 00                  844 	.byte #0x00, #0x00	; 0
      00B726 00 00                  845 	.byte #0x00, #0x00	; 0
      00B728 44 00                  846 	.byte #0x44, #0x00	; 68
      00B72A 2D 00                  847 	.byte #0x2d, #0x00	; 45
      00B72C 2F 00                  848 	.byte #0x2f, #0x00	; 47
      00B72E 34 00                  849 	.byte #0x34, #0x00	; 52
      00B730 38 00                  850 	.byte #0x38, #0x00	; 56
      00B732 E4 00                  851 	.byte #0xe4, #0x00	; 228
      00B734 00 00                  852 	.byte #0x00, #0x00	; 0
      00B736 00 00                  853 	.byte #0x00, #0x00	; 0
      00B738 45 00                  854 	.byte #0x45, #0x00	; 69
      00B73A 2E 00                  855 	.byte #0x2e, #0x00	; 46
      00B73C 30 00                  856 	.byte #0x30, #0x00	; 48
      00B73E 00 00                  857 	.byte #0x00, #0x00	; 0
      00B740 00 00                  858 	.byte #0x00, #0x00	; 0
      00B742 00 00                  859 	.byte #0x00, #0x00	; 0
      00B744 00 00                  860 	.byte #0x00, #0x00	; 0
      00B746 00 00                  861 	.byte #0x00, #0x00	; 0
      00B748 AE 00                  862 	.byte #0xae, #0x00	; 174
      00B74A 2A 00                  863 	.byte #0x2a, #0x00	; 42
      00B74C 31 00                  864 	.byte #0x31, #0x00	; 49
      00B74E 28 00                  865 	.byte #0x28, #0x00	; 40
      00B750 E5 00                  866 	.byte #0xe5, #0x00	; 229
      00B752 50 00                  867 	.byte #0x50, #0x00	; 80
      00B754 00 00                  868 	.byte #0x00, #0x00	; 0
      00B756 00 00                  869 	.byte #0x00, #0x00	; 0
      00B758 00 00                  870 	.byte #0x00, #0x00	; 0
      00B75A 00 00                  871 	.byte #0x00, #0x00	; 0
      00B75C 4C 00                  872 	.byte #0x4c, #0x00	; 76
      00B75E 4E 00                  873 	.byte #0x4e, #0x00	; 78
      00B760 52 00                  874 	.byte #0x52, #0x00	; 82
      00B762 51 00                  875 	.byte #0x51, #0x00	; 81
      00B764 00 00                  876 	.byte #0x00, #0x00	; 0
      00B766 00 00                  877 	.byte #0x00, #0x00	; 0
      00B768 00 00                  878 	.byte #0x00, #0x00	; 0
      00B76A 4A 00                  879 	.byte #0x4a, #0x00	; 74
      00B76C 4B 00                  880 	.byte #0x4b, #0x00	; 75
      00B76E 4D 00                  881 	.byte #0x4d, #0x00	; 77
      00B770 00 00                  882 	.byte #0x00, #0x00	; 0
      00B772 4F 00                  883 	.byte #0x4f, #0x00	; 79
      00B774 00 00                  884 	.byte #0x00, #0x00	; 0
      00B776 00 00                  885 	.byte #0x00, #0x00	; 0
      00B778 01 00                  886 	.byte #0x01, #0x00	; 1
      00B77A 01 00                  887 	.byte #0x01, #0x00	; 1
      00B77C 01 00                  888 	.byte #0x01, #0x00	; 1
      00B77E 01 00                  889 	.byte #0x01, #0x00	; 1
      00B780 01 00                  890 	.byte #0x01, #0x00	; 1
      00B782 01 00                  891 	.byte #0x01, #0x00	; 1
      00B784 00 00                  892 	.byte #0x00, #0x00	; 0
      00B786 00 00                  893 	.byte #0x00, #0x00	; 0
      00B788 B3 00                  894 	.byte #0xb3, #0x00	; 179
      00B78A 01 00                  895 	.byte #0x01, #0x00	; 1
      00B78C 01 00                  896 	.byte #0x01, #0x00	; 1
      00B78E 01 00                  897 	.byte #0x01, #0x00	; 1
      00B790 00 00                  898 	.byte #0x00, #0x00	; 0
      00B792 01 00                  899 	.byte #0x01, #0x00	; 1
      00B794 00 00                  900 	.byte #0x00, #0x00	; 0
      00B796 00 00                  901 	.byte #0x00, #0x00	; 0
      00B798 B5 00                  902 	.byte #0xb5, #0x00	; 181
      00B79A 01 00                  903 	.byte #0x01, #0x00	; 1
      00B79C 01 00                  904 	.byte #0x01, #0x00	; 1
      00B79E 01 00                  905 	.byte #0x01, #0x00	; 1
      00B7A0 01 00                  906 	.byte #0x01, #0x00	; 1
      00B7A2 01 00                  907 	.byte #0x01, #0x00	; 1
      00B7A4 00 00                  908 	.byte #0x00, #0x00	; 0
      00B7A6 00 00                  909 	.byte #0x00, #0x00	; 0
      00B7A8 B2 00                  910 	.byte #0xb2, #0x00	; 178
      00B7AA 01 00                  911 	.byte #0x01, #0x00	; 1
      00B7AC 01 00                  912 	.byte #0x01, #0x00	; 1
      00B7AE 01 00                  913 	.byte #0x01, #0x00	; 1
      00B7B0 01 00                  914 	.byte #0x01, #0x00	; 1
      00B7B2 00 00                  915 	.byte #0x00, #0x00	; 0
      00B7B4 00 00                  916 	.byte #0x00, #0x00	; 0
      00B7B6 00 00                  917 	.byte #0x00, #0x00	; 0
      00B7B8 AF 00                  918 	.byte #0xaf, #0x00	; 175
      00B7BA 01 00                  919 	.byte #0x01, #0x00	; 1
      00B7BC 01 00                  920 	.byte #0x01, #0x00	; 1
      00B7BE 01 00                  921 	.byte #0x01, #0x00	; 1
      00B7C0 01 00                  922 	.byte #0x01, #0x00	; 1
      00B7C2 00 00                  923 	.byte #0x00, #0x00	; 0
      00B7C4 00 00                  924 	.byte #0x00, #0x00	; 0
      00B7C6 00 00                  925 	.byte #0x00, #0x00	; 0
      00B7C8 AC 00                  926 	.byte #0xac, #0x00	; 172
      00B7CA 01 00                  927 	.byte #0x01, #0x00	; 1
      00B7CC 01 00                  928 	.byte #0x01, #0x00	; 1
      00B7CE 01 00                  929 	.byte #0x01, #0x00	; 1
      00B7D0 01 00                  930 	.byte #0x01, #0x00	; 1
      00B7D2 01 00                  931 	.byte #0x01, #0x00	; 1
      00B7D4 00 00                  932 	.byte #0x00, #0x00	; 0
      00B7D6 00 00                  933 	.byte #0x00, #0x00	; 0
      00B7D8 AB 00                  934 	.byte #0xab, #0x00	; 171
      00B7DA 01 00                  935 	.byte #0x01, #0x00	; 1
      00B7DC 01 00                  936 	.byte #0x01, #0x00	; 1
      00B7DE 01 00                  937 	.byte #0x01, #0x00	; 1
      00B7E0 01 00                  938 	.byte #0x01, #0x00	; 1
      00B7E2 00 00                  939 	.byte #0x00, #0x00	; 0
      00B7E4 00 00                  940 	.byte #0x00, #0x00	; 0
      00B7E6 00 00                  941 	.byte #0x00, #0x00	; 0
      00B7E8 AE 00                  942 	.byte #0xae, #0x00	; 174
      00B7EA 01 00                  943 	.byte #0x01, #0x00	; 1
      00B7EC 01 00                  944 	.byte #0x01, #0x00	; 1
      00B7EE 01 00                  945 	.byte #0x01, #0x00	; 1
      00B7F0 01 00                  946 	.byte #0x01, #0x00	; 1
      00B7F2 00 00                  947 	.byte #0x00, #0x00	; 0
      00B7F4 00 00                  948 	.byte #0x00, #0x00	; 0
      00B7F6 00 00                  949 	.byte #0x00, #0x00	; 0
      00B7F8 AD 00                  950 	.byte #0xad, #0x00	; 173
      00B7FA 01 00                  951 	.byte #0x01, #0x00	; 1
      00B7FC 01 00                  952 	.byte #0x01, #0x00	; 1
      00B7FE 01 00                  953 	.byte #0x01, #0x00	; 1
      00B800 01 00                  954 	.byte #0x01, #0x00	; 1
      00B802 00 00                  955 	.byte #0x00, #0x00	; 0
      00B804 00 00                  956 	.byte #0x00, #0x00	; 0
      00B806 00 00                  957 	.byte #0x00, #0x00	; 0
      00B808 A8 00                  958 	.byte #0xa8, #0x00	; 168
      00B80A 01 00                  959 	.byte #0x01, #0x00	; 1
      00B80C 01 00                  960 	.byte #0x01, #0x00	; 1
      00B80E 01 00                  961 	.byte #0x01, #0x00	; 1
      00B810 01 00                  962 	.byte #0x01, #0x00	; 1
      00B812 01 00                  963 	.byte #0x01, #0x00	; 1
      00B814 00 00                  964 	.byte #0x00, #0x00	; 0
      00B816 00 00                  965 	.byte #0x00, #0x00	; 0
      00B818 AA 00                  966 	.byte #0xaa, #0x00	; 170
      00B81A 01 00                  967 	.byte #0x01, #0x00	; 1
      00B81C 01 00                  968 	.byte #0x01, #0x00	; 1
      00B81E 01 00                  969 	.byte #0x01, #0x00	; 1
      00B820 01 00                  970 	.byte #0x01, #0x00	; 1
      00B822 01 00                  971 	.byte #0x01, #0x00	; 1
      00B824 00 00                  972 	.byte #0x00, #0x00	; 0
      00B826 00 00                  973 	.byte #0x00, #0x00	; 0
      00B828 A9 00                  974 	.byte #0xa9, #0x00	; 169
      00B82A 01 00                  975 	.byte #0x01, #0x00	; 1
      00B82C 01 00                  976 	.byte #0x01, #0x00	; 1
      00B82E 01 00                  977 	.byte #0x01, #0x00	; 1
      00B830 01 00                  978 	.byte #0x01, #0x00	; 1
      00B832 01 00                  979 	.byte #0x01, #0x00	; 1
      00B834 00 00                  980 	.byte #0x00, #0x00	; 0
      00B836 00 00                  981 	.byte #0x00, #0x00	; 0
      00B838 01 00                  982 	.byte #0x01, #0x00	; 1
      00B83A 01 00                  983 	.byte #0x01, #0x00	; 1
      00B83C 01 00                  984 	.byte #0x01, #0x00	; 1
      00B83E 00 00                  985 	.byte #0x00, #0x00	; 0
      00B840 00 00                  986 	.byte #0x00, #0x00	; 0
      00B842 00 00                  987 	.byte #0x00, #0x00	; 0
      00B844 00 00                  988 	.byte #0x00, #0x00	; 0
      00B846 00 00                  989 	.byte #0x00, #0x00	; 0
      00B848 A8 00                  990 	.byte #0xa8, #0x00	; 168
      00B84A 01 00                  991 	.byte #0x01, #0x00	; 1
      00B84C 01 00                  992 	.byte #0x01, #0x00	; 1
      00B84E 01 00                  993 	.byte #0x01, #0x00	; 1
      00B850 01 00                  994 	.byte #0x01, #0x00	; 1
      00B852 2A 78                  995 	.byte #0x2a, #0x78	; 30762
      00B854 00 00                  996 	.byte #0x00, #0x00	; 0
      00B856 00 00                  997 	.byte #0x00, #0x00	; 0
      00B858 00 00                  998 	.byte #0x00, #0x00	; 0
      00B85A 00 00                  999 	.byte #0x00, #0x00	; 0
      00B85C 20 78                 1000 	.byte #0x20, #0x78	; 30752
      00B85E 23 78                 1001 	.byte #0x23, #0x78	; 30755
      00B860 27 78                 1002 	.byte #0x27, #0x78	; 30759
      00B862 28 78                 1003 	.byte #0x28, #0x78	; 30760
      00B864 00 00                 1004 	.byte #0x00, #0x00	; 0
      00B866 00 00                 1005 	.byte #0x00, #0x00	; 0
      00B868 00 00                 1006 	.byte #0x00, #0x00	; 0
      00B86A 21 78                 1007 	.byte #0x21, #0x78	; 30753
      00B86C 22 78                 1008 	.byte #0x22, #0x78	; 30754
      00B86E 24 78                 1009 	.byte #0x24, #0x78	; 30756
      00B870 00 00                 1010 	.byte #0x00, #0x00	; 0
      00B872 29 78                 1011 	.byte #0x29, #0x78	; 30761
      00B874 00 00                 1012 	.byte #0x00, #0x00	; 0
      00B876 00 00                 1013 	.byte #0x00, #0x00	; 0
                                   1014 	.area CSEG    (CODE)
                                   1015 	.area CONST   (CODE)
      00B878                       1016 _encoder_map:
      00B878 A9 00                 1017 	.byte #0xa9, #0x00	; 169
      00B87A AA 00                 1018 	.byte #0xaa, #0x00	; 170
      00B87C BB 00                 1019 	.byte #0xbb, #0x00	; 187
      00B87E BC 00                 1020 	.byte #0xbc, #0x00	; 188
                                   1021 	.area CSEG    (CODE)
                                   1022 	.area CONST   (CODE)
      00B880                       1023 _ak820_led_points:
      00B880 07                    1024 	.db #0x07	; 7
      00B881 00                    1025 	.db #0x00	; 0
      00B882 19                    1026 	.db #0x19	; 25
      00B883 00                    1027 	.db #0x00	; 0
      00B884 27                    1028 	.db #0x27	; 39
      00B885 00                    1029 	.db #0x00	; 0
      00B886 35                    1030 	.db #0x35	; 53	'5'
      00B887 00                    1031 	.db #0x00	; 0
      00B888 44                    1032 	.db #0x44	; 68	'D'
      00B889 00                    1033 	.db #0x00	; 0
      00B88A 55                    1034 	.db #0x55	; 85	'U'
      00B88B 00                    1035 	.db #0x00	; 0
      00B88C 64                    1036 	.db #0x64	; 100	'd'
      00B88D 00                    1037 	.db #0x00	; 0
      00B88E 72                    1038 	.db #0x72	; 114	'r'
      00B88F 00                    1039 	.db #0x00	; 0
      00B890 80                    1040 	.db #0x80	; 128
      00B891 00                    1041 	.db #0x00	; 0
      00B892 92                    1042 	.db #0x92	; 146
      00B893 00                    1043 	.db #0x00	; 0
      00B894 A0                    1044 	.db #0xa0	; 160
      00B895 00                    1045 	.db #0x00	; 0
      00B896 AE                    1046 	.db #0xae	; 174
      00B897 00                    1047 	.db #0x00	; 0
      00B898 BC                    1048 	.db #0xbc	; 188
      00B899 00                    1049 	.db #0x00	; 0
      00B89A CB                    1050 	.db #0xcb	; 203
      00B89B 00                    1051 	.db #0x00	; 0
      00B89C 07                    1052 	.db #0x07	; 7
      00B89D 0D                    1053 	.db #0x0d	; 13
      00B89E 15                    1054 	.db #0x15	; 21
      00B89F 0D                    1055 	.db #0x0d	; 13
      00B8A0 24                    1056 	.db #0x24	; 36
      00B8A1 0D                    1057 	.db #0x0d	; 13
      00B8A2 32                    1058 	.db #0x32	; 50	'2'
      00B8A3 0D                    1059 	.db #0x0d	; 13
      00B8A4 40                    1060 	.db #0x40	; 64
      00B8A5 0D                    1061 	.db #0x0d	; 13
      00B8A6 4E                    1062 	.db #0x4e	; 78	'N'
      00B8A7 0D                    1063 	.db #0x0d	; 13
      00B8A8 5C                    1064 	.db #0x5c	; 92
      00B8A9 0D                    1065 	.db #0x0d	; 13
      00B8AA 6B                    1066 	.db #0x6b	; 107	'k'
      00B8AB 0D                    1067 	.db #0x0d	; 13
      00B8AC 79                    1068 	.db #0x79	; 121	'y'
      00B8AD 0D                    1069 	.db #0x0d	; 13
      00B8AE 87                    1070 	.db #0x87	; 135
      00B8AF 0D                    1071 	.db #0x0d	; 13
      00B8B0 95                    1072 	.db #0x95	; 149
      00B8B1 0D                    1073 	.db #0x0d	; 13
      00B8B2 A4                    1074 	.db #0xa4	; 164
      00B8B3 0D                    1075 	.db #0x0d	; 13
      00B8B4 B2                    1076 	.db #0xb2	; 178
      00B8B5 0D                    1077 	.db #0x0d	; 13
      00B8B6 C7                    1078 	.db #0xc7	; 199
      00B8B7 0D                    1079 	.db #0x0d	; 13
      00B8B8 E0                    1080 	.db #0xe0	; 224
      00B8B9 0D                    1081 	.db #0x0d	; 13
      00B8BA 0B                    1082 	.db #0x0b	; 11
      00B8BB 1A                    1083 	.db #0x1a	; 26
      00B8BC 1C                    1084 	.db #0x1c	; 28
      00B8BD 1A                    1085 	.db #0x1a	; 26
      00B8BE 2B                    1086 	.db #0x2b	; 43
      00B8BF 1A                    1087 	.db #0x1a	; 26
      00B8C0 39                    1088 	.db #0x39	; 57	'9'
      00B8C1 1A                    1089 	.db #0x1a	; 26
      00B8C2 47                    1090 	.db #0x47	; 71	'G'
      00B8C3 1A                    1091 	.db #0x1a	; 26
      00B8C4 55                    1092 	.db #0x55	; 85	'U'
      00B8C5 1A                    1093 	.db #0x1a	; 26
      00B8C6 64                    1094 	.db #0x64	; 100	'd'
      00B8C7 1A                    1095 	.db #0x1a	; 26
      00B8C8 72                    1096 	.db #0x72	; 114	'r'
      00B8C9 1A                    1097 	.db #0x1a	; 26
      00B8CA 80                    1098 	.db #0x80	; 128
      00B8CB 1A                    1099 	.db #0x1a	; 26
      00B8CC 8E                    1100 	.db #0x8e	; 142
      00B8CD 1A                    1101 	.db #0x1a	; 26
      00B8CE 9C                    1102 	.db #0x9c	; 156
      00B8CF 1A                    1103 	.db #0x1a	; 26
      00B8D0 AB                    1104 	.db #0xab	; 171
      00B8D1 1A                    1105 	.db #0x1a	; 26
      00B8D2 B9                    1106 	.db #0xb9	; 185
      00B8D3 1A                    1107 	.db #0x1a	; 26
      00B8D4 CB                    1108 	.db #0xcb	; 203
      00B8D5 1A                    1109 	.db #0x1a	; 26
      00B8D6 E0                    1110 	.db #0xe0	; 224
      00B8D7 1A                    1111 	.db #0x1a	; 26
      00B8D8 0C                    1112 	.db #0x0c	; 12
      00B8D9 26                    1113 	.db #0x26	; 38
      00B8DA 20                    1114 	.db #0x20	; 32
      00B8DB 26                    1115 	.db #0x26	; 38
      00B8DC 2E                    1116 	.db #0x2e	; 46
      00B8DD 26                    1117 	.db #0x26	; 38
      00B8DE 3C                    1118 	.db #0x3c	; 60
      00B8DF 26                    1119 	.db #0x26	; 38
      00B8E0 4B                    1120 	.db #0x4b	; 75	'K'
      00B8E1 26                    1121 	.db #0x26	; 38
      00B8E2 59                    1122 	.db #0x59	; 89	'Y'
      00B8E3 26                    1123 	.db #0x26	; 38
      00B8E4 67                    1124 	.db #0x67	; 103	'g'
      00B8E5 26                    1125 	.db #0x26	; 38
      00B8E6 75                    1126 	.db #0x75	; 117	'u'
      00B8E7 26                    1127 	.db #0x26	; 38
      00B8E8 84                    1128 	.db #0x84	; 132
      00B8E9 26                    1129 	.db #0x26	; 38
      00B8EA 92                    1130 	.db #0x92	; 146
      00B8EB 26                    1131 	.db #0x26	; 38
      00B8EC A0                    1132 	.db #0xa0	; 160
      00B8ED 26                    1133 	.db #0x26	; 38
      00B8EE AE                    1134 	.db #0xae	; 174
      00B8EF 26                    1135 	.db #0x26	; 38
      00B8F0 C5                    1136 	.db #0xc5	; 197
      00B8F1 26                    1137 	.db #0x26	; 38
      00B8F2 E0                    1138 	.db #0xe0	; 224
      00B8F3 26                    1139 	.db #0x26	; 38
      00B8F4 10                    1140 	.db #0x10	; 16
      00B8F5 33                    1141 	.db #0x33	; 51	'3'
      00B8F6 27                    1142 	.db #0x27	; 39
      00B8F7 33                    1143 	.db #0x33	; 51	'3'
      00B8F8 35                    1144 	.db #0x35	; 53	'5'
      00B8F9 33                    1145 	.db #0x33	; 51	'3'
      00B8FA 44                    1146 	.db #0x44	; 68	'D'
      00B8FB 33                    1147 	.db #0x33	; 51	'3'
      00B8FC 52                    1148 	.db #0x52	; 82	'R'
      00B8FD 33                    1149 	.db #0x33	; 51	'3'
      00B8FE 60                    1150 	.db #0x60	; 96
      00B8FF 33                    1151 	.db #0x33	; 51	'3'
      00B900 6E                    1152 	.db #0x6e	; 110	'n'
      00B901 33                    1153 	.db #0x33	; 51	'3'
      00B902 7C                    1154 	.db #0x7c	; 124
      00B903 33                    1155 	.db #0x33	; 51	'3'
      00B904 8B                    1156 	.db #0x8b	; 139
      00B905 33                    1157 	.db #0x33	; 51	'3'
      00B906 99                    1158 	.db #0x99	; 153
      00B907 33                    1159 	.db #0x33	; 51	'3'
      00B908 A7                    1160 	.db #0xa7	; 167
      00B909 33                    1161 	.db #0x33	; 51	'3'
      00B90A BB                    1162 	.db #0xbb	; 187
      00B90B 33                    1163 	.db #0x33	; 51	'3'
      00B90C D2                    1164 	.db #0xd2	; 210
      00B90D 33                    1165 	.db #0x33	; 51	'3'
      00B90E E0                    1166 	.db #0xe0	; 224
      00B90F 33                    1167 	.db #0x33	; 51	'3'
      00B910 09                    1168 	.db #0x09	; 9
      00B911 40                    1169 	.db #0x40	; 64
      00B912 1B                    1170 	.db #0x1b	; 27
      00B913 40                    1171 	.db #0x40	; 64
      00B914 2C                    1172 	.db #0x2c	; 44
      00B915 40                    1173 	.db #0x40	; 64
      00B916 62                    1174 	.db #0x62	; 98	'b'
      00B917 40                    1175 	.db #0x40	; 64
      00B918 95                    1176 	.db #0x95	; 149
      00B919 40                    1177 	.db #0x40	; 64
      00B91A A4                    1178 	.db #0xa4	; 164
      00B91B 40                    1179 	.db #0x40	; 64
      00B91C B2                    1180 	.db #0xb2	; 178
      00B91D 40                    1181 	.db #0x40	; 64
      00B91E C4                    1182 	.db #0xc4	; 196
      00B91F 40                    1183 	.db #0x40	; 64
      00B920 D2                    1184 	.db #0xd2	; 210
      00B921 40                    1185 	.db #0x40	; 64
      00B922 E0                    1186 	.db #0xe0	; 224
      00B923 40                    1187 	.db #0x40	; 64
                                   1188 	.area CSEG    (CODE)
                                   1189 	.area XINIT   (CODE)
                                   1190 	.area CABS    (ABS,CODE)
