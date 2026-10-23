                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module report
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _memset
                                     12 	.globl _ADC_START
                                     13 	.globl _S0_R_FIFO
                                     14 	.globl _S0_T_FIFO
                                     15 	.globl _S0_FREE
                                     16 	.globl _S0_IF_BYTE
                                     17 	.globl _S0_IF_FIRST
                                     18 	.globl _S0_IF_OV
                                     19 	.globl _S0_FST_ACT
                                     20 	.globl _CP_RL2
                                     21 	.globl _C_T2
                                     22 	.globl _TR2
                                     23 	.globl _EXEN2
                                     24 	.globl _TCLK
                                     25 	.globl _RCLK
                                     26 	.globl _EXF2
                                     27 	.globl _CAP1F
                                     28 	.globl _TF2
                                     29 	.globl _RI
                                     30 	.globl _TI
                                     31 	.globl _RB8
                                     32 	.globl _TB8
                                     33 	.globl _REN
                                     34 	.globl _SM2
                                     35 	.globl _SM1
                                     36 	.globl _SM0
                                     37 	.globl _IT0
                                     38 	.globl _IE0
                                     39 	.globl _IT1
                                     40 	.globl _IE1
                                     41 	.globl _TR0
                                     42 	.globl _TF0
                                     43 	.globl _TR1
                                     44 	.globl _TF1
                                     45 	.globl _P4_0
                                     46 	.globl _P4_1
                                     47 	.globl _P4_2
                                     48 	.globl _P4_3
                                     49 	.globl _P4_4
                                     50 	.globl _P4_5
                                     51 	.globl _P4_6
                                     52 	.globl _RXD
                                     53 	.globl _TXD
                                     54 	.globl _INT0
                                     55 	.globl _INT1
                                     56 	.globl _T0
                                     57 	.globl _T1
                                     58 	.globl _MOSI1
                                     59 	.globl _MISO1
                                     60 	.globl _SCK1
                                     61 	.globl _P3_0
                                     62 	.globl _P3_1
                                     63 	.globl _P3_2
                                     64 	.globl _P3_3
                                     65 	.globl _P3_4
                                     66 	.globl _P3_5
                                     67 	.globl _P3_6
                                     68 	.globl _P3_7
                                     69 	.globl _CAP1_
                                     70 	.globl _T2_
                                     71 	.globl _CAP2_
                                     72 	.globl _T2EX_
                                     73 	.globl _RXD1
                                     74 	.globl _TXD1
                                     75 	.globl _P2_0
                                     76 	.globl _P2_1
                                     77 	.globl _P2_2
                                     78 	.globl _P2_3
                                     79 	.globl _P2_4
                                     80 	.globl _P2_5
                                     81 	.globl _P2_6
                                     82 	.globl _P2_7
                                     83 	.globl _AIN0
                                     84 	.globl _AIN1
                                     85 	.globl _AIN2
                                     86 	.globl _AIN3
                                     87 	.globl _AIN4
                                     88 	.globl _AIN5
                                     89 	.globl _AIN6
                                     90 	.globl _AIN7
                                     91 	.globl _CAP1
                                     92 	.globl _T2
                                     93 	.globl _CAP2
                                     94 	.globl _T2EX
                                     95 	.globl _INT0_
                                     96 	.globl _SCS
                                     97 	.globl _MOSI
                                     98 	.globl _MISO
                                     99 	.globl _SCK
                                    100 	.globl _RXD1_
                                    101 	.globl _TXD1_
                                    102 	.globl _P1_0
                                    103 	.globl _P1_1
                                    104 	.globl _P1_2
                                    105 	.globl _P1_3
                                    106 	.globl _P1_4
                                    107 	.globl _P1_5
                                    108 	.globl _P1_6
                                    109 	.globl _P1_7
                                    110 	.globl _AIN8
                                    111 	.globl _AIN9
                                    112 	.globl _AIN10
                                    113 	.globl _AIN11
                                    114 	.globl _AIN12
                                    115 	.globl _AIN13
                                    116 	.globl _RXD_
                                    117 	.globl _TXD_
                                    118 	.globl _SCL0
                                    119 	.globl _SDA0
                                    120 	.globl _P0_0
                                    121 	.globl _P0_1
                                    122 	.globl _P0_2
                                    123 	.globl _P0_3
                                    124 	.globl _P0_4
                                    125 	.globl _P0_5
                                    126 	.globl _P0_6
                                    127 	.globl _P0_7
                                    128 	.globl _IE_SPI0
                                    129 	.globl _IE_USB
                                    130 	.globl _IE_ADC
                                    131 	.globl _IE_UART1
                                    132 	.globl _IE_PWM_I2C
                                    133 	.globl _IE_GPIO
                                    134 	.globl _IE_WDOG
                                    135 	.globl _PX0
                                    136 	.globl _PT0
                                    137 	.globl _PX1
                                    138 	.globl _PT1
                                    139 	.globl _PS
                                    140 	.globl _PT2
                                    141 	.globl _PL_FLAG
                                    142 	.globl _PH_FLAG
                                    143 	.globl _EX0
                                    144 	.globl _ET0
                                    145 	.globl _EX1
                                    146 	.globl _ET1
                                    147 	.globl _ES
                                    148 	.globl _ET2
                                    149 	.globl _E_DIS
                                    150 	.globl _EA
                                    151 	.globl _P
                                    152 	.globl _F1
                                    153 	.globl _OV
                                    154 	.globl _RS0
                                    155 	.globl _RS1
                                    156 	.globl _F0
                                    157 	.globl _AC
                                    158 	.globl _CY
                                    159 	.globl _I2CS_INT_ST
                                    160 	.globl _I2CX_INT
                                    161 	.globl _LED_STATUS
                                    162 	.globl _LED_DMA_H
                                    163 	.globl _LED_DMA_L
                                    164 	.globl _LED_DMA
                                    165 	.globl _LED_PWM_OE
                                    166 	.globl _LED_COMMON
                                    167 	.globl _ADC_CHAN
                                    168 	.globl _ADC_DAT_H
                                    169 	.globl _ADC_DAT_L
                                    170 	.globl _ADC_DAT
                                    171 	.globl _ADC_CTRL
                                    172 	.globl _SPI1_CK_SE
                                    173 	.globl _SPI1_CTRL
                                    174 	.globl _SPI1_DATA
                                    175 	.globl _SPI1_STAT
                                    176 	.globl _SIF1
                                    177 	.globl _SBAUD1
                                    178 	.globl _SBUF1
                                    179 	.globl _SCON1
                                    180 	.globl _SPI0_SETUP
                                    181 	.globl _SPI0_CK_SE
                                    182 	.globl _SPI0_CTRL
                                    183 	.globl _SPI0_DATA
                                    184 	.globl _SPI0_STAT
                                    185 	.globl _T2CAP1H
                                    186 	.globl _T2CAP1L
                                    187 	.globl _T2CAP1
                                    188 	.globl _TH2
                                    189 	.globl _TL2
                                    190 	.globl _T2COUNT
                                    191 	.globl _RCAP2H
                                    192 	.globl _RCAP2L
                                    193 	.globl _RCAP2
                                    194 	.globl _T2MOD
                                    195 	.globl _T2CON
                                    196 	.globl _SBUF
                                    197 	.globl _SCON
                                    198 	.globl _TH1
                                    199 	.globl _TH0
                                    200 	.globl _TL1
                                    201 	.globl _TL0
                                    202 	.globl _TMOD
                                    203 	.globl _TCON
                                    204 	.globl _XBUS_AUX
                                    205 	.globl _P7
                                    206 	.globl _P6_DIR
                                    207 	.globl _P6_OUT_PU
                                    208 	.globl _P6_IN
                                    209 	.globl _P5_DIR
                                    210 	.globl _P5_OUT_PU
                                    211 	.globl _P5_IN
                                    212 	.globl _P4_LED_KEY
                                    213 	.globl _P4_DIR_PU
                                    214 	.globl _P4_MOD_OC
                                    215 	.globl _P4
                                    216 	.globl _P3_DIR_PU
                                    217 	.globl _P3_MOD_OC
                                    218 	.globl _P3
                                    219 	.globl _P2_DIR_PU
                                    220 	.globl _P2_MOD_OC
                                    221 	.globl _P2
                                    222 	.globl _P1_DIR_PU
                                    223 	.globl _P1_MOD_OC
                                    224 	.globl _P1
                                    225 	.globl _P0_DIR_PU
                                    226 	.globl _P0_MOD_OC
                                    227 	.globl _P0
                                    228 	.globl _ROM_CTRL
                                    229 	.globl _ROM_DATA_HH
                                    230 	.globl _ROM_DATA_HL
                                    231 	.globl _ROM_DATA_HI
                                    232 	.globl _ROM_ADDR_H
                                    233 	.globl _ROM_ADDR_L
                                    234 	.globl _ROM_ADDR
                                    235 	.globl _GPIO_IE
                                    236 	.globl _IP_EX
                                    237 	.globl _IE_EX
                                    238 	.globl _IP
                                    239 	.globl _IE
                                    240 	.globl _WDOG_COUNT
                                    241 	.globl _RESET_KEEP
                                    242 	.globl _WAKE_CTRL
                                    243 	.globl _CLOCK_CFG
                                    244 	.globl _POWER_CFG
                                    245 	.globl _PCON
                                    246 	.globl _GLOBAL_CFG
                                    247 	.globl _SAFE_MOD
                                    248 	.globl _DPH
                                    249 	.globl _DPL
                                    250 	.globl _SP
                                    251 	.globl _A_INV
                                    252 	.globl _B
                                    253 	.globl _ACC
                                    254 	.globl _PSW
                                    255 	.globl _del_key_from_report_PARM_2
                                    256 	.globl _add_key_to_report_PARM_2
                                    257 	.globl _del_key_bit_PARM_2
                                    258 	.globl _add_key_bit_PARM_2
                                    259 	.globl _del_key_byte_PARM_2
                                    260 	.globl _add_key_byte_PARM_2
                                    261 	.globl _is_key_pressed_PARM_2
                                    262 	.globl _KEYCODE2CONSUMER
                                    263 	.globl _is_key_pressed
                                    264 	.globl _add_key_byte
                                    265 	.globl _del_key_byte
                                    266 	.globl _add_key_bit
                                    267 	.globl _del_key_bit
                                    268 	.globl _add_key_to_report
                                    269 	.globl _del_key_from_report
                                    270 	.globl _clear_keys_from_report
                                    271 ;--------------------------------------------------------
                                    272 ; special function registers
                                    273 ;--------------------------------------------------------
                                    274 	.area RSEG    (ABS,DATA)
      000000                        275 	.org 0x0000
                           0000D0   276 _PSW	=	0x00d0
                           0000E0   277 _ACC	=	0x00e0
                           0000F0   278 _B	=	0x00f0
                           0000FD   279 _A_INV	=	0x00fd
                           000081   280 _SP	=	0x0081
                           000082   281 _DPL	=	0x0082
                           000083   282 _DPH	=	0x0083
                           0000A1   283 _SAFE_MOD	=	0x00a1
                           0000B1   284 _GLOBAL_CFG	=	0x00b1
                           000087   285 _PCON	=	0x0087
                           0000BA   286 _POWER_CFG	=	0x00ba
                           0000B9   287 _CLOCK_CFG	=	0x00b9
                           0000A9   288 _WAKE_CTRL	=	0x00a9
                           0000FE   289 _RESET_KEEP	=	0x00fe
                           0000FF   290 _WDOG_COUNT	=	0x00ff
                           0000A8   291 _IE	=	0x00a8
                           0000B8   292 _IP	=	0x00b8
                           0000E8   293 _IE_EX	=	0x00e8
                           0000E9   294 _IP_EX	=	0x00e9
                           0000B2   295 _GPIO_IE	=	0x00b2
                           008584   296 _ROM_ADDR	=	0x8584
                           000084   297 _ROM_ADDR_L	=	0x0084
                           000085   298 _ROM_ADDR_H	=	0x0085
                           008F8E   299 _ROM_DATA_HI	=	0x8f8e
                           00008E   300 _ROM_DATA_HL	=	0x008e
                           00008F   301 _ROM_DATA_HH	=	0x008f
                           000086   302 _ROM_CTRL	=	0x0086
                           000080   303 _P0	=	0x0080
                           0000C4   304 _P0_MOD_OC	=	0x00c4
                           0000C5   305 _P0_DIR_PU	=	0x00c5
                           000090   306 _P1	=	0x0090
                           000092   307 _P1_MOD_OC	=	0x0092
                           000093   308 _P1_DIR_PU	=	0x0093
                           0000A0   309 _P2	=	0x00a0
                           000094   310 _P2_MOD_OC	=	0x0094
                           000095   311 _P2_DIR_PU	=	0x0095
                           0000B0   312 _P3	=	0x00b0
                           000096   313 _P3_MOD_OC	=	0x0096
                           000097   314 _P3_DIR_PU	=	0x0097
                           0000C0   315 _P4	=	0x00c0
                           0000C2   316 _P4_MOD_OC	=	0x00c2
                           0000C3   317 _P4_DIR_PU	=	0x00c3
                           0000C1   318 _P4_LED_KEY	=	0x00c1
                           0000AA   319 _P5_IN	=	0x00aa
                           0000AB   320 _P5_OUT_PU	=	0x00ab
                           0000AC   321 _P5_DIR	=	0x00ac
                           0000AD   322 _P6_IN	=	0x00ad
                           0000AE   323 _P6_OUT_PU	=	0x00ae
                           0000AF   324 _P6_DIR	=	0x00af
                           0000F1   325 _P7	=	0x00f1
                           0000A2   326 _XBUS_AUX	=	0x00a2
                           000088   327 _TCON	=	0x0088
                           000089   328 _TMOD	=	0x0089
                           00008A   329 _TL0	=	0x008a
                           00008B   330 _TL1	=	0x008b
                           00008C   331 _TH0	=	0x008c
                           00008D   332 _TH1	=	0x008d
                           000098   333 _SCON	=	0x0098
                           000099   334 _SBUF	=	0x0099
                           0000C8   335 _T2CON	=	0x00c8
                           0000C9   336 _T2MOD	=	0x00c9
                           00CBCA   337 _RCAP2	=	0xcbca
                           0000CA   338 _RCAP2L	=	0x00ca
                           0000CB   339 _RCAP2H	=	0x00cb
                           00CDCC   340 _T2COUNT	=	0xcdcc
                           0000CC   341 _TL2	=	0x00cc
                           0000CD   342 _TH2	=	0x00cd
                           00CFCE   343 _T2CAP1	=	0xcfce
                           0000CE   344 _T2CAP1L	=	0x00ce
                           0000CF   345 _T2CAP1H	=	0x00cf
                           0000F8   346 _SPI0_STAT	=	0x00f8
                           0000F9   347 _SPI0_DATA	=	0x00f9
                           0000FA   348 _SPI0_CTRL	=	0x00fa
                           0000FB   349 _SPI0_CK_SE	=	0x00fb
                           0000FC   350 _SPI0_SETUP	=	0x00fc
                           0000BC   351 _SCON1	=	0x00bc
                           0000BD   352 _SBUF1	=	0x00bd
                           0000BE   353 _SBAUD1	=	0x00be
                           0000BF   354 _SIF1	=	0x00bf
                           0000B4   355 _SPI1_STAT	=	0x00b4
                           0000B5   356 _SPI1_DATA	=	0x00b5
                           0000B6   357 _SPI1_CTRL	=	0x00b6
                           0000B7   358 _SPI1_CK_SE	=	0x00b7
                           0000F3   359 _ADC_CTRL	=	0x00f3
                           00F5F4   360 _ADC_DAT	=	0xf5f4
                           0000F4   361 _ADC_DAT_L	=	0x00f4
                           0000F5   362 _ADC_DAT_H	=	0x00f5
                           0000F6   363 _ADC_CHAN	=	0x00f6
                           0000A6   364 _LED_COMMON	=	0x00a6
                           0000A7   365 _LED_PWM_OE	=	0x00a7
                           00C7C6   366 _LED_DMA	=	0xc7c6
                           0000C6   367 _LED_DMA_L	=	0x00c6
                           0000C7   368 _LED_DMA_H	=	0x00c7
                           0000F7   369 _LED_STATUS	=	0x00f7
                           0000B3   370 _I2CX_INT	=	0x00b3
                           0000BB   371 _I2CS_INT_ST	=	0x00bb
                                    372 ;--------------------------------------------------------
                                    373 ; special function bits
                                    374 ;--------------------------------------------------------
                                    375 	.area RSEG    (ABS,DATA)
      000000                        376 	.org 0x0000
                           0000D7   377 _CY	=	0x00d7
                           0000D6   378 _AC	=	0x00d6
                           0000D5   379 _F0	=	0x00d5
                           0000D4   380 _RS1	=	0x00d4
                           0000D3   381 _RS0	=	0x00d3
                           0000D2   382 _OV	=	0x00d2
                           0000D1   383 _F1	=	0x00d1
                           0000D0   384 _P	=	0x00d0
                           0000AF   385 _EA	=	0x00af
                           0000AE   386 _E_DIS	=	0x00ae
                           0000AD   387 _ET2	=	0x00ad
                           0000AC   388 _ES	=	0x00ac
                           0000AB   389 _ET1	=	0x00ab
                           0000AA   390 _EX1	=	0x00aa
                           0000A9   391 _ET0	=	0x00a9
                           0000A8   392 _EX0	=	0x00a8
                           0000BF   393 _PH_FLAG	=	0x00bf
                           0000BE   394 _PL_FLAG	=	0x00be
                           0000BD   395 _PT2	=	0x00bd
                           0000BC   396 _PS	=	0x00bc
                           0000BB   397 _PT1	=	0x00bb
                           0000BA   398 _PX1	=	0x00ba
                           0000B9   399 _PT0	=	0x00b9
                           0000B8   400 _PX0	=	0x00b8
                           0000EF   401 _IE_WDOG	=	0x00ef
                           0000EE   402 _IE_GPIO	=	0x00ee
                           0000ED   403 _IE_PWM_I2C	=	0x00ed
                           0000EC   404 _IE_UART1	=	0x00ec
                           0000EB   405 _IE_ADC	=	0x00eb
                           0000E9   406 _IE_USB	=	0x00e9
                           0000E8   407 _IE_SPI0	=	0x00e8
                           000087   408 _P0_7	=	0x0087
                           000086   409 _P0_6	=	0x0086
                           000085   410 _P0_5	=	0x0085
                           000084   411 _P0_4	=	0x0084
                           000083   412 _P0_3	=	0x0083
                           000082   413 _P0_2	=	0x0082
                           000081   414 _P0_1	=	0x0081
                           000080   415 _P0_0	=	0x0080
                           000081   416 _SDA0	=	0x0081
                           000080   417 _SCL0	=	0x0080
                           000083   418 _TXD_	=	0x0083
                           000082   419 _RXD_	=	0x0082
                           000085   420 _AIN13	=	0x0085
                           000084   421 _AIN12	=	0x0084
                           000083   422 _AIN11	=	0x0083
                           000082   423 _AIN10	=	0x0082
                           000081   424 _AIN9	=	0x0081
                           000080   425 _AIN8	=	0x0080
                           000097   426 _P1_7	=	0x0097
                           000096   427 _P1_6	=	0x0096
                           000095   428 _P1_5	=	0x0095
                           000094   429 _P1_4	=	0x0094
                           000093   430 _P1_3	=	0x0093
                           000092   431 _P1_2	=	0x0092
                           000091   432 _P1_1	=	0x0091
                           000090   433 _P1_0	=	0x0090
                           000097   434 _TXD1_	=	0x0097
                           000096   435 _RXD1_	=	0x0096
                           000097   436 _SCK	=	0x0097
                           000096   437 _MISO	=	0x0096
                           000095   438 _MOSI	=	0x0095
                           000094   439 _SCS	=	0x0094
                           000092   440 _INT0_	=	0x0092
                           000091   441 _T2EX	=	0x0091
                           000091   442 _CAP2	=	0x0091
                           000090   443 _T2	=	0x0090
                           000090   444 _CAP1	=	0x0090
                           000097   445 _AIN7	=	0x0097
                           000096   446 _AIN6	=	0x0096
                           000095   447 _AIN5	=	0x0095
                           000094   448 _AIN4	=	0x0094
                           000093   449 _AIN3	=	0x0093
                           000092   450 _AIN2	=	0x0092
                           000091   451 _AIN1	=	0x0091
                           000090   452 _AIN0	=	0x0090
                           0000A7   453 _P2_7	=	0x00a7
                           0000A6   454 _P2_6	=	0x00a6
                           0000A5   455 _P2_5	=	0x00a5
                           0000A4   456 _P2_4	=	0x00a4
                           0000A3   457 _P2_3	=	0x00a3
                           0000A2   458 _P2_2	=	0x00a2
                           0000A1   459 _P2_1	=	0x00a1
                           0000A0   460 _P2_0	=	0x00a0
                           0000A7   461 _TXD1	=	0x00a7
                           0000A6   462 _RXD1	=	0x00a6
                           0000A5   463 _T2EX_	=	0x00a5
                           0000A5   464 _CAP2_	=	0x00a5
                           0000A4   465 _T2_	=	0x00a4
                           0000A4   466 _CAP1_	=	0x00a4
                           0000B7   467 _P3_7	=	0x00b7
                           0000B6   468 _P3_6	=	0x00b6
                           0000B5   469 _P3_5	=	0x00b5
                           0000B4   470 _P3_4	=	0x00b4
                           0000B3   471 _P3_3	=	0x00b3
                           0000B2   472 _P3_2	=	0x00b2
                           0000B1   473 _P3_1	=	0x00b1
                           0000B0   474 _P3_0	=	0x00b0
                           0000B7   475 _SCK1	=	0x00b7
                           0000B6   476 _MISO1	=	0x00b6
                           0000B5   477 _MOSI1	=	0x00b5
                           0000B5   478 _T1	=	0x00b5
                           0000B4   479 _T0	=	0x00b4
                           0000B3   480 _INT1	=	0x00b3
                           0000B2   481 _INT0	=	0x00b2
                           0000B1   482 _TXD	=	0x00b1
                           0000B0   483 _RXD	=	0x00b0
                           0000C6   484 _P4_6	=	0x00c6
                           0000C5   485 _P4_5	=	0x00c5
                           0000C4   486 _P4_4	=	0x00c4
                           0000C3   487 _P4_3	=	0x00c3
                           0000C2   488 _P4_2	=	0x00c2
                           0000C1   489 _P4_1	=	0x00c1
                           0000C0   490 _P4_0	=	0x00c0
                           00008F   491 _TF1	=	0x008f
                           00008E   492 _TR1	=	0x008e
                           00008D   493 _TF0	=	0x008d
                           00008C   494 _TR0	=	0x008c
                           00008B   495 _IE1	=	0x008b
                           00008A   496 _IT1	=	0x008a
                           000089   497 _IE0	=	0x0089
                           000088   498 _IT0	=	0x0088
                           00009F   499 _SM0	=	0x009f
                           00009E   500 _SM1	=	0x009e
                           00009D   501 _SM2	=	0x009d
                           00009C   502 _REN	=	0x009c
                           00009B   503 _TB8	=	0x009b
                           00009A   504 _RB8	=	0x009a
                           000099   505 _TI	=	0x0099
                           000098   506 _RI	=	0x0098
                           0000CF   507 _TF2	=	0x00cf
                           0000CF   508 _CAP1F	=	0x00cf
                           0000CE   509 _EXF2	=	0x00ce
                           0000CD   510 _RCLK	=	0x00cd
                           0000CC   511 _TCLK	=	0x00cc
                           0000CB   512 _EXEN2	=	0x00cb
                           0000CA   513 _TR2	=	0x00ca
                           0000C9   514 _C_T2	=	0x00c9
                           0000C8   515 _CP_RL2	=	0x00c8
                           0000FF   516 _S0_FST_ACT	=	0x00ff
                           0000FE   517 _S0_IF_OV	=	0x00fe
                           0000FD   518 _S0_IF_FIRST	=	0x00fd
                           0000FC   519 _S0_IF_BYTE	=	0x00fc
                           0000FB   520 _S0_FREE	=	0x00fb
                           0000FA   521 _S0_T_FIFO	=	0x00fa
                           0000F8   522 _S0_R_FIFO	=	0x00f8
                           0000F7   523 _ADC_START	=	0x00f7
                                    524 ;--------------------------------------------------------
                                    525 ; overlayable register banks
                                    526 ;--------------------------------------------------------
                                    527 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        528 	.ds 8
                                    529 ;--------------------------------------------------------
                                    530 ; internal ram data
                                    531 ;--------------------------------------------------------
                                    532 	.area DSEG    (DATA)
                                    533 ;--------------------------------------------------------
                                    534 ; overlayable items in internal ram
                                    535 ;--------------------------------------------------------
                                    536 ;--------------------------------------------------------
                                    537 ; indirectly addressable internal ram data
                                    538 ;--------------------------------------------------------
                                    539 	.area ISEG    (DATA)
                                    540 ;--------------------------------------------------------
                                    541 ; absolute internal ram data
                                    542 ;--------------------------------------------------------
                                    543 	.area IABS    (ABS,DATA)
                                    544 	.area IABS    (ABS,DATA)
                                    545 ;--------------------------------------------------------
                                    546 ; bit data
                                    547 ;--------------------------------------------------------
                                    548 	.area BSEG    (BIT)
                                    549 ;--------------------------------------------------------
                                    550 ; paged external ram data
                                    551 ;--------------------------------------------------------
                                    552 	.area PSEG    (PAG,XDATA)
                                    553 ;--------------------------------------------------------
                                    554 ; uninitialized external ram data
                                    555 ;--------------------------------------------------------
                                    556 	.area XSEG    (XDATA)
      000712                        557 _KEYCODE2CONSUMER_key_10000_118:
      000712                        558 	.ds 1
      000713                        559 _is_key_pressed_PARM_2:
      000713                        560 	.ds 1
      000714                        561 _is_key_pressed_keyboard_report_10000_132:
      000714                        562 	.ds 3
      000717                        563 _add_key_byte_PARM_2:
      000717                        564 	.ds 1
      000718                        565 _add_key_byte_keyboard_report_10000_145:
      000718                        566 	.ds 3
      00071B                        567 _add_key_byte_empty_10000_146:
      00071B                        568 	.ds 1
      00071C                        569 _del_key_byte_PARM_2:
      00071C                        570 	.ds 1
      00071D                        571 _del_key_byte_keyboard_report_10000_157:
      00071D                        572 	.ds 3
      000720                        573 _add_key_bit_PARM_2:
      000720                        574 	.ds 1
      000721                        575 _add_key_bit_keyboard_report_10000_163:
      000721                        576 	.ds 3
      000724                        577 _del_key_bit_PARM_2:
      000724                        578 	.ds 1
      000725                        579 _del_key_bit_keyboard_report_10000_168:
      000725                        580 	.ds 3
      000728                        581 _add_key_to_report_PARM_2:
      000728                        582 	.ds 1
      000729                        583 _add_key_to_report_keyboard_report_10000_173:
      000729                        584 	.ds 3
      00072C                        585 _del_key_from_report_PARM_2:
      00072C                        586 	.ds 1
      00072D                        587 _del_key_from_report_keyboard_report_10000_177:
      00072D                        588 	.ds 3
      000730                        589 _clear_keys_from_report_keyboard_report_10000_181:
      000730                        590 	.ds 3
                                    591 ;--------------------------------------------------------
                                    592 ; absolute external ram data
                                    593 ;--------------------------------------------------------
                                    594 	.area XABS    (ABS,XDATA)
                                    595 ;--------------------------------------------------------
                                    596 ; initialized external ram data
                                    597 ;--------------------------------------------------------
                                    598 	.area XISEG   (XDATA)
                                    599 	.area HOME    (CODE)
                                    600 	.area GSINIT0 (CODE)
                                    601 	.area GSINIT1 (CODE)
                                    602 	.area GSINIT2 (CODE)
                                    603 	.area GSINIT3 (CODE)
                                    604 	.area GSINIT4 (CODE)
                                    605 	.area GSINIT5 (CODE)
                                    606 	.area GSINIT  (CODE)
                                    607 	.area GSFINAL (CODE)
                                    608 	.area CSEG    (CODE)
                                    609 ;--------------------------------------------------------
                                    610 ; global & static initialisations
                                    611 ;--------------------------------------------------------
                                    612 	.area HOME    (CODE)
                                    613 	.area GSINIT  (CODE)
                                    614 	.area GSFINAL (CODE)
                                    615 	.area GSINIT  (CODE)
                                    616 ;--------------------------------------------------------
                                    617 ; Home
                                    618 ;--------------------------------------------------------
                                    619 	.area HOME    (CODE)
                                    620 	.area HOME    (CODE)
                                    621 ;--------------------------------------------------------
                                    622 ; code
                                    623 ;--------------------------------------------------------
                                    624 	.area CSEG    (CODE)
                                    625 ;------------------------------------------------------------
                                    626 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    627 ;------------------------------------------------------------
                                    628 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_40'
                                    629 ;------------------------------------------------------------
                                    630 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    631 ;	-----------------------------------------
                           000007   632 	ar7 = 0x07
                           000006   633 	ar6 = 0x06
                           000005   634 	ar5 = 0x05
                           000004   635 	ar4 = 0x04
                           000003   636 	ar3 = 0x03
                           000002   637 	ar2 = 0x02
                           000001   638 	ar1 = 0x01
                           000000   639 	ar0 = 0x00
                                    640 ;	 function KEYCODE2CONSUMER
                                    641 ;	-----------------------------------------
      0068D2                        642 _KEYCODE2CONSUMER:
      0068D2 E5 82            [12]  643 	mov	a,dpl
      0068D4 90 07 12         [24]  644 	mov	dptr,#_KEYCODE2CONSUMER_key_10000_118
      0068D7 F0               [24]  645 	movx	@dptr,a
                                    646 ;	tmk_core/protocol/report.c:38: if (key < KC_AUDIO_MUTE || key > KC_LAUNCHPAD) return 0;
      0068D8 E0               [24]  647 	movx	a,@dptr
      0068D9 FF               [12]  648 	mov	r7,a
      0068DA BF A8 00         [24]  649 	cjne	r7,#0xa8,00113$
      0068DD                        650 00113$:
      0068DD 40 05            [24]  651 	jc	00101$
      0068DF EF               [12]  652 	mov	a,r7
      0068E0 24 3D            [12]  653 	add	a,#0xff - 0xc2
      0068E2 50 04            [24]  654 	jnc	00102$
                                    655 ;	free result
      0068E4                        656 00101$:
      0068E4 90 00 00         [24]  657 	mov	dptr,#0x0000
      0068E7 22               [24]  658 	ret
      0068E8                        659 00102$:
                                    660 ;	tmk_core/protocol/report.c:39: return usages[key - KC_AUDIO_MUTE];
      0068E8 EF               [12]  661 	mov	a,r7
      0068E9 24 58            [12]  662 	add	a,#0x58
      0068EB FF               [12]  663 	mov	r7,a
      0068EC C2 D5            [12]  664 	clr	F0
      0068EE 75 F0 02         [24]  665 	mov	b,#0x02
      0068F1 EF               [12]  666 	mov	a,r7
      0068F2 30 E7 04         [24]  667 	jnb	acc.7,00116$
      0068F5 B2 D5            [12]  668 	cpl	F0
      0068F7 F4               [12]  669 	cpl	a
      0068F8 04               [12]  670 	inc	a
      0068F9                        671 00116$:
      0068F9 A4               [48]  672 	mul	ab
      0068FA 30 D5 0A         [24]  673 	jnb	F0,00117$
      0068FD F4               [12]  674 	cpl	a
      0068FE 24 01            [12]  675 	add	a,#0x01
      006900 C5 F0            [12]  676 	xch	a,b
      006902 F4               [12]  677 	cpl	a
      006903 34 00            [12]  678 	addc	a,#0x00
      006905 C5 F0            [12]  679 	xch	a,b
      006907                        680 00117$:
      006907 24 42            [12]  681 	add	a, #_KEYCODE2CONSUMER_usages_10000_119
      006909 F5 82            [12]  682 	mov	dpl,a
      00690B 74 B6            [12]  683 	mov	a,#(_KEYCODE2CONSUMER_usages_10000_119 >> 8)
      00690D 35 F0            [12]  684 	addc	a, b
      00690F F5 83            [12]  685 	mov	dph,a
      006911 E4               [12]  686 	clr	a
      006912 93               [24]  687 	movc	a,@a+dptr
      006913 FE               [12]  688 	mov	r6,a
      006914 A3               [24]  689 	inc	dptr
      006915 E4               [12]  690 	clr	a
      006916 93               [24]  691 	movc	a,@a+dptr
                                    692 ;	tmk_core/protocol/report.c:40: }
      006917 8E 82            [24]  693 	mov	dpl,r6
      006919 F5 83            [12]  694 	mov	dph,a
      00691B 22               [24]  695 	ret
                                    696 ;------------------------------------------------------------
                                    697 ;Allocation info for local variables in function 'has_anykey'
                                    698 ;------------------------------------------------------------
                                    699 ;keyboard_report Allocated with name '_has_anykey_keyboard_report_10000_121'
                                    700 ;cnt           Allocated with name '_has_anykey_cnt_10000_122'
                                    701 ;p             Allocated with name '_has_anykey_p_10000_122'
                                    702 ;lp            Allocated with name '_has_anykey_lp_10000_122'
                                    703 ;------------------------------------------------------------
                                    704 ;	tmk_core/protocol/report.c:57: uint8_t has_anykey(report_keyboard_t* keyboard_report) {
                                    705 ;	-----------------------------------------
                                    706 ;	 function is_key_pressed
                                    707 ;	-----------------------------------------
      00691C                        708 _is_key_pressed:
      00691C AF F0            [24]  709 	mov	r7,b
      00691E AE 83            [24]  710 	mov	r6,dph
      006920 E5 82            [12]  711 	mov	a,dpl
      006922 90 07 14         [24]  712 	mov	dptr,#_is_key_pressed_keyboard_report_10000_132
      006925 F0               [24]  713 	movx	@dptr,a
      006926 EE               [12]  714 	mov	a,r6
      006927 A3               [24]  715 	inc	dptr
      006928 F0               [24]  716 	movx	@dptr,a
      006929 EF               [12]  717 	mov	a,r7
      00692A A3               [24]  718 	inc	dptr
      00692B F0               [24]  719 	movx	@dptr,a
                                    720 ;	tmk_core/protocol/report.c:106: if (key == KC_NO) {
      00692C 90 07 13         [24]  721 	mov	dptr,#_is_key_pressed_PARM_2
      00692F E0               [24]  722 	movx	a,@dptr
      006930 FF               [12]  723 	mov	r7,a
                                    724 ;	tmk_core/protocol/report.c:107: return false;
      006931 70 03            [24]  725 	jnz	00102$
      006933 F5 82            [12]  726 	mov	dpl,a
      006935 22               [24]  727 	ret
      006936                        728 00102$:
                                    729 ;	tmk_core/protocol/report.c:110: if (keyboard_protocol && keymap_config.nkro) {
      006936 90 0B 9E         [24]  730 	mov	dptr,#_keyboard_protocol
      006939 E0               [24]  731 	movx	a,@dptr
      00693A 60 5D            [24]  732 	jz	00130$
      00693C 90 08 BD         [24]  733 	mov	dptr,#_keymap_config
      00693F E0               [24]  734 	movx	a,@dptr
      006940 30 E7 56         [24]  735 	jnb	acc.7,00130$
                                    736 ;	tmk_core/protocol/report.c:111: if ((key >> 3) < KEYBOARD_REPORT_BITS) {
      006943 EF               [12]  737 	mov	a,r7
      006944 C4               [12]  738 	swap	a
      006945 23               [12]  739 	rl	a
      006946 54 1F            [12]  740 	anl	a,#0x1f
      006948 FE               [12]  741 	mov	r6,a
      006949 BE 1E 00         [24]  742 	cjne	r6,#0x1e,00169$
      00694C                        743 00169$:
      00694C 50 47            [24]  744 	jnc	00104$
                                    745 ;	tmk_core/protocol/report.c:112: return keyboard_report->nkro.bits[key >> 3] & 1 << (key & 7);
      00694E 90 07 14         [24]  746 	mov	dptr,#_is_key_pressed_keyboard_report_10000_132
      006951 E0               [24]  747 	movx	a,@dptr
      006952 FB               [12]  748 	mov	r3,a
      006953 A3               [24]  749 	inc	dptr
      006954 E0               [24]  750 	movx	a,@dptr
      006955 FC               [12]  751 	mov	r4,a
      006956 A3               [24]  752 	inc	dptr
      006957 E0               [24]  753 	movx	a,@dptr
      006958 FD               [12]  754 	mov	r5,a
      006959 74 02            [12]  755 	mov	a,#0x02
      00695B 2B               [12]  756 	add	a, r3
      00695C FB               [12]  757 	mov	r3,a
      00695D E4               [12]  758 	clr	a
      00695E 3C               [12]  759 	addc	a, r4
      00695F FC               [12]  760 	mov	r4,a
      006960 EE               [12]  761 	mov	a,r6
      006961 2B               [12]  762 	add	a, r3
      006962 FB               [12]  763 	mov	r3,a
      006963 E4               [12]  764 	clr	a
      006964 3C               [12]  765 	addc	a, r4
      006965 FC               [12]  766 	mov	r4,a
      006966 74 07            [12]  767 	mov	a,#0x07
      006968 5F               [12]  768 	anl	a,r7
      006969 F5 F0            [12]  769 	mov	b, a
      00696B 05 F0            [12]  770 	inc	b
      00696D 7E 01            [12]  771 	mov	r6,#0x01
      00696F 7A 00            [12]  772 	mov	r2,#0x00
      006971 80 06            [24]  773 	sjmp	00172$
      006973                        774 00171$:
      006973 EE               [12]  775 	mov	a,r6
      006974 2E               [12]  776 	add	a,r6
      006975 FE               [12]  777 	mov	r6,a
      006976 EA               [12]  778 	mov	a,r2
      006977 33               [12]  779 	rlc	a
      006978 FA               [12]  780 	mov	r2,a
      006979                        781 00172$:
      006979 D5 F0 F7         [24]  782 	djnz	b,00171$
      00697C 8B 82            [24]  783 	mov	dpl,r3
      00697E 8C 83            [24]  784 	mov	dph,r4
      006980 8D F0            [24]  785 	mov	b,r5
      006982 12 B5 9A         [24]  786 	lcall	__gptrget
      006985 7D 00            [12]  787 	mov	r5,#0x00
      006987 52 06            [12]  788 	anl	ar6,a
      006989 ED               [12]  789 	mov	a,r5
      00698A 52 02            [12]  790 	anl	ar2,a
                                    791 ;	assignBit
      00698C EE               [12]  792 	mov	a,r6
      00698D 4A               [12]  793 	orl	a,r2
      00698E 24 FF            [12]  794 	add	a,#0xff
      006990 E4               [12]  795 	clr	a
      006991 33               [12]  796 	rlc	a
      006992 F5 82            [12]  797 	mov	dpl,a
      006994 22               [24]  798 	ret
      006995                        799 00104$:
                                    800 ;	tmk_core/protocol/report.c:114: return false;
      006995 75 82 00         [24]  801 	mov	dpl, #0x00
                                    802 ;	tmk_core/protocol/report.c:118: for (int i = 0; i < KEYBOARD_REPORT_KEYS; i++) {
      006998 22               [24]  803 	ret
      006999                        804 00130$:
      006999 90 07 14         [24]  805 	mov	dptr,#_is_key_pressed_keyboard_report_10000_132
      00699C E0               [24]  806 	movx	a,@dptr
      00699D FC               [12]  807 	mov	r4,a
      00699E A3               [24]  808 	inc	dptr
      00699F E0               [24]  809 	movx	a,@dptr
      0069A0 FD               [12]  810 	mov	r5,a
      0069A1 A3               [24]  811 	inc	dptr
      0069A2 E0               [24]  812 	movx	a,@dptr
      0069A3 FE               [12]  813 	mov	r6,a
      0069A4 74 02            [12]  814 	mov	a,#0x02
      0069A6 2C               [12]  815 	add	a, r4
      0069A7 FC               [12]  816 	mov	r4,a
      0069A8 E4               [12]  817 	clr	a
      0069A9 3D               [12]  818 	addc	a, r5
      0069AA FD               [12]  819 	mov	r5,a
      0069AB 7B 00            [12]  820 	mov	r3,#0x00
      0069AD                        821 00113$:
      0069AD BB 06 00         [24]  822 	cjne	r3,#0x06,00173$
      0069B0                        823 00173$:
      0069B0 50 1B            [24]  824 	jnc	00111$
                                    825 ;	tmk_core/protocol/report.c:119: if (keyboard_report->keys[i] == key) {
      0069B2 EB               [12]  826 	mov	a,r3
      0069B3 2C               [12]  827 	add	a, r4
      0069B4 F8               [12]  828 	mov	r0,a
      0069B5 E4               [12]  829 	clr	a
      0069B6 3D               [12]  830 	addc	a, r5
      0069B7 F9               [12]  831 	mov	r1,a
      0069B8 8E 02            [24]  832 	mov	ar2,r6
      0069BA 88 82            [24]  833 	mov	dpl,r0
      0069BC 89 83            [24]  834 	mov	dph,r1
      0069BE 8A F0            [24]  835 	mov	b,r2
      0069C0 12 B5 9A         [24]  836 	lcall	__gptrget
      0069C3 B5 07 04         [24]  837 	cjne	a,ar7,00114$
                                    838 ;	tmk_core/protocol/report.c:120: return true;
      0069C6 75 82 01         [24]  839 	mov	dpl, #0x01
      0069C9 22               [24]  840 	ret
      0069CA                        841 00114$:
                                    842 ;	tmk_core/protocol/report.c:118: for (int i = 0; i < KEYBOARD_REPORT_KEYS; i++) {
      0069CA 0B               [12]  843 	inc	r3
      0069CB 80 E0            [24]  844 	sjmp	00113$
      0069CD                        845 00111$:
                                    846 ;	tmk_core/protocol/report.c:123: return false;
      0069CD 75 82 00         [24]  847 	mov	dpl, #0x00
                                    848 ;	tmk_core/protocol/report.c:124: }
      0069D0 22               [24]  849 	ret
                                    850 ;------------------------------------------------------------
                                    851 ;Allocation info for local variables in function 'add_key_byte'
                                    852 ;------------------------------------------------------------
                                    853 ;code          Allocated with name '_add_key_byte_PARM_2'
                                    854 ;keyboard_report Allocated with name '_add_key_byte_keyboard_report_10000_145'
                                    855 ;i             Allocated with name '_add_key_byte_i_10000_146'
                                    856 ;empty         Allocated with name '_add_key_byte_empty_10000_146'
                                    857 ;------------------------------------------------------------
                                    858 ;	tmk_core/protocol/report.c:130: void add_key_byte(report_keyboard_t* keyboard_report, uint8_t code) {
                                    859 ;	-----------------------------------------
                                    860 ;	 function add_key_byte
                                    861 ;	-----------------------------------------
      0069D1                        862 _add_key_byte:
      0069D1 AF F0            [24]  863 	mov	r7,b
      0069D3 AE 83            [24]  864 	mov	r6,dph
      0069D5 E5 82            [12]  865 	mov	a,dpl
      0069D7 90 07 18         [24]  866 	mov	dptr,#_add_key_byte_keyboard_report_10000_145
      0069DA F0               [24]  867 	movx	@dptr,a
      0069DB EE               [12]  868 	mov	a,r6
      0069DC A3               [24]  869 	inc	dptr
      0069DD F0               [24]  870 	movx	@dptr,a
      0069DE EF               [12]  871 	mov	a,r7
      0069DF A3               [24]  872 	inc	dptr
      0069E0 F0               [24]  873 	movx	@dptr,a
                                    874 ;	tmk_core/protocol/report.c:176: int8_t empty = -1;
      0069E1 90 07 1B         [24]  875 	mov	dptr,#_add_key_byte_empty_10000_146
      0069E4 74 FF            [12]  876 	mov	a,#0xff
      0069E6 F0               [24]  877 	movx	@dptr,a
                                    878 ;	tmk_core/protocol/report.c:191: }
      0069E7 90 07 18         [24]  879 	mov	dptr,#_add_key_byte_keyboard_report_10000_145
      0069EA E0               [24]  880 	movx	a,@dptr
      0069EB FD               [12]  881 	mov	r5,a
      0069EC A3               [24]  882 	inc	dptr
      0069ED E0               [24]  883 	movx	a,@dptr
      0069EE FE               [12]  884 	mov	r6,a
      0069EF A3               [24]  885 	inc	dptr
      0069F0 E0               [24]  886 	movx	a,@dptr
      0069F1 FF               [12]  887 	mov	r7,a
      0069F2 74 02            [12]  888 	mov	a,#0x02
      0069F4 2D               [12]  889 	add	a, r5
      0069F5 FD               [12]  890 	mov	r5,a
      0069F6 E4               [12]  891 	clr	a
      0069F7 3E               [12]  892 	addc	a, r6
      0069F8 FE               [12]  893 	mov	r6,a
      0069F9 90 07 17         [24]  894 	mov	dptr,#_add_key_byte_PARM_2
      0069FC E0               [24]  895 	movx	a,@dptr
      0069FD FC               [12]  896 	mov	r4,a
      0069FE 7B 00            [12]  897 	mov	r3,#0x00
      006A00                        898 00112$:
                                    899 ;	tmk_core/protocol/report.c:177: for (; i < KEYBOARD_REPORT_KEYS; i++) {
      006A00 C3               [12]  900 	clr	c
      006A01 EB               [12]  901 	mov	a,r3
      006A02 64 80            [12]  902 	xrl	a,#0x80
      006A04 94 86            [12]  903 	subb	a,#0x86
      006A06 50 2A            [24]  904 	jnc	00106$
                                    905 ;	tmk_core/protocol/report.c:178: if (keyboard_report->keys[i] == code) {
      006A08 EB               [12]  906 	mov	a,r3
      006A09 2D               [12]  907 	add	a, r5
      006A0A F8               [12]  908 	mov	r0,a
      006A0B E4               [12]  909 	clr	a
      006A0C 3E               [12]  910 	addc	a, r6
      006A0D F9               [12]  911 	mov	r1,a
      006A0E 8F 02            [24]  912 	mov	ar2,r7
      006A10 88 82            [24]  913 	mov	dpl,r0
      006A12 89 83            [24]  914 	mov	dph,r1
      006A14 8A F0            [24]  915 	mov	b,r2
      006A16 12 B5 9A         [24]  916 	lcall	__gptrget
      006A19 FA               [12]  917 	mov	r2,a
      006A1A B5 04 02         [24]  918 	cjne	a,ar4,00167$
      006A1D 80 13            [24]  919 	sjmp	00106$
      006A1F                        920 00167$:
                                    921 ;	tmk_core/protocol/report.c:181: if (empty == -1 && keyboard_report->keys[i] == 0) {
      006A1F 90 07 1B         [24]  922 	mov	dptr,#_add_key_byte_empty_10000_146
      006A22 E0               [24]  923 	movx	a,@dptr
      006A23 F9               [12]  924 	mov	r1,a
      006A24 B9 FF 08         [24]  925 	cjne	r1,#0xff,00113$
      006A27 EA               [12]  926 	mov	a,r2
      006A28 70 05            [24]  927 	jnz	00113$
                                    928 ;	tmk_core/protocol/report.c:182: empty = i;
      006A2A 90 07 1B         [24]  929 	mov	dptr,#_add_key_byte_empty_10000_146
      006A2D EB               [12]  930 	mov	a,r3
      006A2E F0               [24]  931 	movx	@dptr,a
      006A2F                        932 00113$:
                                    933 ;	tmk_core/protocol/report.c:177: for (; i < KEYBOARD_REPORT_KEYS; i++) {
      006A2F 0B               [12]  934 	inc	r3
      006A30 80 CE            [24]  935 	sjmp	00112$
      006A32                        936 00106$:
                                    937 ;	tmk_core/protocol/report.c:185: if (i == KEYBOARD_REPORT_KEYS) {
      006A32 BB 06 2B         [24]  938 	cjne	r3,#0x06,00114$
                                    939 ;	tmk_core/protocol/report.c:186: if (empty != -1) {
      006A35 90 07 1B         [24]  940 	mov	dptr,#_add_key_byte_empty_10000_146
      006A38 E0               [24]  941 	movx	a,@dptr
      006A39 FF               [12]  942 	mov	r7,a
      006A3A BF FF 01         [24]  943 	cjne	r7,#0xff,00173$
      006A3D 22               [24]  944 	ret
      006A3E                        945 00173$:
                                    946 ;	tmk_core/protocol/report.c:187: keyboard_report->keys[empty] = code;
      006A3E 90 07 18         [24]  947 	mov	dptr,#_add_key_byte_keyboard_report_10000_145
      006A41 E0               [24]  948 	movx	a,@dptr
      006A42 FB               [12]  949 	mov	r3,a
      006A43 A3               [24]  950 	inc	dptr
      006A44 E0               [24]  951 	movx	a,@dptr
      006A45 FD               [12]  952 	mov	r5,a
      006A46 A3               [24]  953 	inc	dptr
      006A47 E0               [24]  954 	movx	a,@dptr
      006A48 FE               [12]  955 	mov	r6,a
      006A49 74 02            [12]  956 	mov	a,#0x02
      006A4B 2B               [12]  957 	add	a, r3
      006A4C FB               [12]  958 	mov	r3,a
      006A4D E4               [12]  959 	clr	a
      006A4E 3D               [12]  960 	addc	a, r5
      006A4F FD               [12]  961 	mov	r5,a
      006A50 EF               [12]  962 	mov	a,r7
      006A51 2B               [12]  963 	add	a, r3
      006A52 FB               [12]  964 	mov	r3,a
      006A53 E4               [12]  965 	clr	a
      006A54 3D               [12]  966 	addc	a, r5
      006A55 FD               [12]  967 	mov	r5,a
      006A56 8B 82            [24]  968 	mov	dpl,r3
      006A58 8D 83            [24]  969 	mov	dph,r5
      006A5A 8E F0            [24]  970 	mov	b,r6
      006A5C EC               [12]  971 	mov	a,r4
                                    972 ;	tmk_core/protocol/report.c:191: }
      006A5D 02 B5 5F         [24]  973 	ljmp	__gptrput
      006A60                        974 00114$:
      006A60 22               [24]  975 	ret
                                    976 ;------------------------------------------------------------
                                    977 ;Allocation info for local variables in function 'del_key_byte'
                                    978 ;------------------------------------------------------------
                                    979 ;code          Allocated with name '_del_key_byte_PARM_2'
                                    980 ;keyboard_report Allocated with name '_del_key_byte_keyboard_report_10000_157'
                                    981 ;i             Allocated with name '_del_key_byte_i_20000_159'
                                    982 ;------------------------------------------------------------
                                    983 ;	tmk_core/protocol/report.c:197: void del_key_byte(report_keyboard_t* keyboard_report, uint8_t code) {
                                    984 ;	-----------------------------------------
                                    985 ;	 function del_key_byte
                                    986 ;	-----------------------------------------
      006A61                        987 _del_key_byte:
      006A61 AF F0            [24]  988 	mov	r7,b
      006A63 AE 83            [24]  989 	mov	r6,dph
      006A65 E5 82            [12]  990 	mov	a,dpl
      006A67 90 07 1D         [24]  991 	mov	dptr,#_del_key_byte_keyboard_report_10000_157
      006A6A F0               [24]  992 	movx	@dptr,a
      006A6B EE               [12]  993 	mov	a,r6
      006A6C A3               [24]  994 	inc	dptr
      006A6D F0               [24]  995 	movx	@dptr,a
      006A6E EF               [12]  996 	mov	a,r7
      006A6F A3               [24]  997 	inc	dptr
      006A70 F0               [24]  998 	movx	@dptr,a
                                    999 ;	tmk_core/protocol/report.c:224: for (uint8_t i = 0; i < KEYBOARD_REPORT_KEYS; i++) {
      006A71 90 07 1D         [24] 1000 	mov	dptr,#_del_key_byte_keyboard_report_10000_157
      006A74 E0               [24] 1001 	movx	a,@dptr
      006A75 FD               [12] 1002 	mov	r5,a
      006A76 A3               [24] 1003 	inc	dptr
      006A77 E0               [24] 1004 	movx	a,@dptr
      006A78 FE               [12] 1005 	mov	r6,a
      006A79 A3               [24] 1006 	inc	dptr
      006A7A E0               [24] 1007 	movx	a,@dptr
      006A7B FF               [12] 1008 	mov	r7,a
      006A7C 74 02            [12] 1009 	mov	a,#0x02
      006A7E 2D               [12] 1010 	add	a, r5
      006A7F FD               [12] 1011 	mov	r5,a
      006A80 E4               [12] 1012 	clr	a
      006A81 3E               [12] 1013 	addc	a, r6
      006A82 FE               [12] 1014 	mov	r6,a
      006A83 90 07 1C         [24] 1015 	mov	dptr,#_del_key_byte_PARM_2
      006A86 E0               [24] 1016 	movx	a,@dptr
      006A87 FC               [12] 1017 	mov	r4,a
      006A88 7B 00            [12] 1018 	mov	r3,#0x00
      006A8A                       1019 00105$:
      006A8A BB 06 00         [24] 1020 	cjne	r3,#0x06,00131$
      006A8D                       1021 00131$:
      006A8D 50 37            [24] 1022 	jnc	00107$
                                   1023 ;	tmk_core/protocol/report.c:225: if (keyboard_report->keys[i] == code) {
      006A8F EB               [12] 1024 	mov	a,r3
      006A90 2D               [12] 1025 	add	a, r5
      006A91 F8               [12] 1026 	mov	r0,a
      006A92 E4               [12] 1027 	clr	a
      006A93 3E               [12] 1028 	addc	a, r6
      006A94 F9               [12] 1029 	mov	r1,a
      006A95 8F 02            [24] 1030 	mov	ar2,r7
      006A97 C0 05            [24] 1031 	push	ar5
      006A99 C0 06            [24] 1032 	push	ar6
      006A9B C0 07            [24] 1033 	push	ar7
      006A9D 88 82            [24] 1034 	mov	dpl,r0
      006A9F 89 83            [24] 1035 	mov	dph,r1
      006AA1 8A F0            [24] 1036 	mov	b,r2
      006AA3 12 B5 9A         [24] 1037 	lcall	__gptrget
      006AA6 B5 04 02         [24] 1038 	cjne	a,ar4,00133$
      006AA9 80 08            [24] 1039 	sjmp	00134$
      006AAB                       1040 00133$:
      006AAB D0 07            [24] 1041 	pop	ar7
      006AAD D0 06            [24] 1042 	pop	ar6
      006AAF D0 05            [24] 1043 	pop	ar5
      006AB1 80 10            [24] 1044 	sjmp	00106$
      006AB3                       1045 00134$:
      006AB3 D0 07            [24] 1046 	pop	ar7
      006AB5 D0 06            [24] 1047 	pop	ar6
      006AB7 D0 05            [24] 1048 	pop	ar5
                                   1049 ;	tmk_core/protocol/report.c:226: keyboard_report->keys[i] = 0;
      006AB9 88 82            [24] 1050 	mov	dpl,r0
      006ABB 89 83            [24] 1051 	mov	dph,r1
      006ABD 8A F0            [24] 1052 	mov	b,r2
      006ABF E4               [12] 1053 	clr	a
      006AC0 12 B5 5F         [24] 1054 	lcall	__gptrput
      006AC3                       1055 00106$:
                                   1056 ;	tmk_core/protocol/report.c:224: for (uint8_t i = 0; i < KEYBOARD_REPORT_KEYS; i++) {
      006AC3 0B               [12] 1057 	inc	r3
      006AC4 80 C4            [24] 1058 	sjmp	00105$
      006AC6                       1059 00107$:
                                   1060 ;	tmk_core/protocol/report.c:230: }
      006AC6 22               [24] 1061 	ret
                                   1062 ;------------------------------------------------------------
                                   1063 ;Allocation info for local variables in function 'add_key_bit'
                                   1064 ;------------------------------------------------------------
                                   1065 ;code          Allocated with name '_add_key_bit_PARM_2'
                                   1066 ;keyboard_report Allocated with name '_add_key_bit_keyboard_report_10000_163'
                                   1067 ;------------------------------------------------------------
                                   1068 ;	tmk_core/protocol/report.c:237: void add_key_bit(report_keyboard_t* keyboard_report, uint8_t code) {
                                   1069 ;	-----------------------------------------
                                   1070 ;	 function add_key_bit
                                   1071 ;	-----------------------------------------
      006AC7                       1072 _add_key_bit:
      006AC7 AF F0            [24] 1073 	mov	r7,b
      006AC9 AE 83            [24] 1074 	mov	r6,dph
      006ACB E5 82            [12] 1075 	mov	a,dpl
      006ACD 90 07 21         [24] 1076 	mov	dptr,#_add_key_bit_keyboard_report_10000_163
      006AD0 F0               [24] 1077 	movx	@dptr,a
      006AD1 EE               [12] 1078 	mov	a,r6
      006AD2 A3               [24] 1079 	inc	dptr
      006AD3 F0               [24] 1080 	movx	@dptr,a
      006AD4 EF               [12] 1081 	mov	a,r7
      006AD5 A3               [24] 1082 	inc	dptr
      006AD6 F0               [24] 1083 	movx	@dptr,a
                                   1084 ;	tmk_core/protocol/report.c:238: if ((code >> 3) < KEYBOARD_REPORT_BITS) {
      006AD7 90 07 20         [24] 1085 	mov	dptr,#_add_key_bit_PARM_2
      006ADA E0               [24] 1086 	movx	a,@dptr
      006ADB FF               [12] 1087 	mov	r7,a
      006ADC C4               [12] 1088 	swap	a
      006ADD 23               [12] 1089 	rl	a
      006ADE 54 1F            [12] 1090 	anl	a,#0x1f
      006AE0 FE               [12] 1091 	mov	r6,a
      006AE1 BE 1E 00         [24] 1092 	cjne	r6,#0x1e,00112$
      006AE4                       1093 00112$:
      006AE4 50 3E            [24] 1094 	jnc	00103$
                                   1095 ;	tmk_core/protocol/report.c:239: keyboard_report->nkro.bits[code >> 3] |= 1 << (code & 7);
      006AE6 90 07 21         [24] 1096 	mov	dptr,#_add_key_bit_keyboard_report_10000_163
      006AE9 E0               [24] 1097 	movx	a,@dptr
      006AEA FB               [12] 1098 	mov	r3,a
      006AEB A3               [24] 1099 	inc	dptr
      006AEC E0               [24] 1100 	movx	a,@dptr
      006AED FC               [12] 1101 	mov	r4,a
      006AEE A3               [24] 1102 	inc	dptr
      006AEF E0               [24] 1103 	movx	a,@dptr
      006AF0 FD               [12] 1104 	mov	r5,a
      006AF1 74 02            [12] 1105 	mov	a,#0x02
      006AF3 2B               [12] 1106 	add	a, r3
      006AF4 FB               [12] 1107 	mov	r3,a
      006AF5 E4               [12] 1108 	clr	a
      006AF6 3C               [12] 1109 	addc	a, r4
      006AF7 FC               [12] 1110 	mov	r4,a
      006AF8 EE               [12] 1111 	mov	a,r6
      006AF9 2B               [12] 1112 	add	a, r3
      006AFA FB               [12] 1113 	mov	r3,a
      006AFB E4               [12] 1114 	clr	a
      006AFC 3C               [12] 1115 	addc	a, r4
      006AFD FC               [12] 1116 	mov	r4,a
      006AFE 74 07            [12] 1117 	mov	a,#0x07
      006B00 5F               [12] 1118 	anl	a,r7
      006B01 F5 F0            [12] 1119 	mov	b,a
      006B03 05 F0            [12] 1120 	inc	b
      006B05 74 01            [12] 1121 	mov	a,#0x01
      006B07 80 02            [24] 1122 	sjmp	00115$
      006B09                       1123 00114$:
      006B09 25 E0            [12] 1124 	add	a,acc
      006B0B                       1125 00115$:
      006B0B D5 F0 FB         [24] 1126 	djnz	b,00114$
      006B0E FF               [12] 1127 	mov	r7,a
      006B0F 8B 82            [24] 1128 	mov	dpl,r3
      006B11 8C 83            [24] 1129 	mov	dph,r4
      006B13 8D F0            [24] 1130 	mov	b,r5
      006B15 12 B5 9A         [24] 1131 	lcall	__gptrget
      006B18 42 07            [12] 1132 	orl	ar7,a
      006B1A 8B 82            [24] 1133 	mov	dpl,r3
      006B1C 8C 83            [24] 1134 	mov	dph,r4
      006B1E 8D F0            [24] 1135 	mov	b,r5
      006B20 EF               [12] 1136 	mov	a,r7
                                   1137 ;	tmk_core/protocol/report.c:243: }
      006B21 02 B5 5F         [24] 1138 	ljmp	__gptrput
      006B24                       1139 00103$:
      006B24 22               [24] 1140 	ret
                                   1141 ;------------------------------------------------------------
                                   1142 ;Allocation info for local variables in function 'del_key_bit'
                                   1143 ;------------------------------------------------------------
                                   1144 ;code          Allocated with name '_del_key_bit_PARM_2'
                                   1145 ;keyboard_report Allocated with name '_del_key_bit_keyboard_report_10000_168'
                                   1146 ;------------------------------------------------------------
                                   1147 ;	tmk_core/protocol/report.c:249: void del_key_bit(report_keyboard_t* keyboard_report, uint8_t code) {
                                   1148 ;	-----------------------------------------
                                   1149 ;	 function del_key_bit
                                   1150 ;	-----------------------------------------
      006B25                       1151 _del_key_bit:
      006B25 AF F0            [24] 1152 	mov	r7,b
      006B27 AE 83            [24] 1153 	mov	r6,dph
      006B29 E5 82            [12] 1154 	mov	a,dpl
      006B2B 90 07 25         [24] 1155 	mov	dptr,#_del_key_bit_keyboard_report_10000_168
      006B2E F0               [24] 1156 	movx	@dptr,a
      006B2F EE               [12] 1157 	mov	a,r6
      006B30 A3               [24] 1158 	inc	dptr
      006B31 F0               [24] 1159 	movx	@dptr,a
      006B32 EF               [12] 1160 	mov	a,r7
      006B33 A3               [24] 1161 	inc	dptr
      006B34 F0               [24] 1162 	movx	@dptr,a
                                   1163 ;	tmk_core/protocol/report.c:250: if ((code >> 3) < KEYBOARD_REPORT_BITS) {
      006B35 90 07 24         [24] 1164 	mov	dptr,#_del_key_bit_PARM_2
      006B38 E0               [24] 1165 	movx	a,@dptr
      006B39 FF               [12] 1166 	mov	r7,a
      006B3A C4               [12] 1167 	swap	a
      006B3B 23               [12] 1168 	rl	a
      006B3C 54 1F            [12] 1169 	anl	a,#0x1f
      006B3E FE               [12] 1170 	mov	r6,a
      006B3F BE 1E 00         [24] 1171 	cjne	r6,#0x1e,00112$
      006B42                       1172 00112$:
      006B42 50 3F            [24] 1173 	jnc	00103$
                                   1174 ;	tmk_core/protocol/report.c:251: keyboard_report->nkro.bits[code >> 3] &= ~(1 << (code & 7));
      006B44 90 07 25         [24] 1175 	mov	dptr,#_del_key_bit_keyboard_report_10000_168
      006B47 E0               [24] 1176 	movx	a,@dptr
      006B48 FB               [12] 1177 	mov	r3,a
      006B49 A3               [24] 1178 	inc	dptr
      006B4A E0               [24] 1179 	movx	a,@dptr
      006B4B FC               [12] 1180 	mov	r4,a
      006B4C A3               [24] 1181 	inc	dptr
      006B4D E0               [24] 1182 	movx	a,@dptr
      006B4E FD               [12] 1183 	mov	r5,a
      006B4F 74 02            [12] 1184 	mov	a,#0x02
      006B51 2B               [12] 1185 	add	a, r3
      006B52 FB               [12] 1186 	mov	r3,a
      006B53 E4               [12] 1187 	clr	a
      006B54 3C               [12] 1188 	addc	a, r4
      006B55 FC               [12] 1189 	mov	r4,a
      006B56 EE               [12] 1190 	mov	a,r6
      006B57 2B               [12] 1191 	add	a, r3
      006B58 FB               [12] 1192 	mov	r3,a
      006B59 E4               [12] 1193 	clr	a
      006B5A 3C               [12] 1194 	addc	a, r4
      006B5B FC               [12] 1195 	mov	r4,a
      006B5C 74 07            [12] 1196 	mov	a,#0x07
      006B5E 5F               [12] 1197 	anl	a,r7
      006B5F F5 F0            [12] 1198 	mov	b,a
      006B61 05 F0            [12] 1199 	inc	b
      006B63 74 01            [12] 1200 	mov	a,#0x01
      006B65 80 02            [24] 1201 	sjmp	00115$
      006B67                       1202 00114$:
      006B67 25 E0            [12] 1203 	add	a,acc
      006B69                       1204 00115$:
      006B69 D5 F0 FB         [24] 1205 	djnz	b,00114$
      006B6C F4               [12] 1206 	cpl	a
      006B6D FF               [12] 1207 	mov	r7,a
      006B6E 8B 82            [24] 1208 	mov	dpl,r3
      006B70 8C 83            [24] 1209 	mov	dph,r4
      006B72 8D F0            [24] 1210 	mov	b,r5
      006B74 12 B5 9A         [24] 1211 	lcall	__gptrget
      006B77 52 07            [12] 1212 	anl	ar7,a
      006B79 8B 82            [24] 1213 	mov	dpl,r3
      006B7B 8C 83            [24] 1214 	mov	dph,r4
      006B7D 8D F0            [24] 1215 	mov	b,r5
      006B7F EF               [12] 1216 	mov	a,r7
                                   1217 ;	tmk_core/protocol/report.c:255: }
      006B80 02 B5 5F         [24] 1218 	ljmp	__gptrput
      006B83                       1219 00103$:
      006B83 22               [24] 1220 	ret
                                   1221 ;------------------------------------------------------------
                                   1222 ;Allocation info for local variables in function 'add_key_to_report'
                                   1223 ;------------------------------------------------------------
                                   1224 ;key           Allocated with name '_add_key_to_report_PARM_2'
                                   1225 ;keyboard_report Allocated with name '_add_key_to_report_keyboard_report_10000_173'
                                   1226 ;------------------------------------------------------------
                                   1227 ;	tmk_core/protocol/report.c:262: void add_key_to_report(report_keyboard_t* keyboard_report, uint8_t key) {
                                   1228 ;	-----------------------------------------
                                   1229 ;	 function add_key_to_report
                                   1230 ;	-----------------------------------------
      006B84                       1231 _add_key_to_report:
      006B84 AF F0            [24] 1232 	mov	r7,b
      006B86 AE 83            [24] 1233 	mov	r6,dph
      006B88 E5 82            [12] 1234 	mov	a,dpl
      006B8A 90 07 29         [24] 1235 	mov	dptr,#_add_key_to_report_keyboard_report_10000_173
      006B8D F0               [24] 1236 	movx	@dptr,a
      006B8E EE               [12] 1237 	mov	a,r6
      006B8F A3               [24] 1238 	inc	dptr
      006B90 F0               [24] 1239 	movx	@dptr,a
      006B91 EF               [12] 1240 	mov	a,r7
      006B92 A3               [24] 1241 	inc	dptr
      006B93 F0               [24] 1242 	movx	@dptr,a
                                   1243 ;	tmk_core/protocol/report.c:264: if (keyboard_protocol && keymap_config.nkro) {
      006B94 90 0B 9E         [24] 1244 	mov	dptr,#_keyboard_protocol
      006B97 E0               [24] 1245 	movx	a,@dptr
      006B98 60 23            [24] 1246 	jz	00102$
      006B9A 90 08 BD         [24] 1247 	mov	dptr,#_keymap_config
      006B9D E0               [24] 1248 	movx	a,@dptr
      006B9E 30 E7 1C         [24] 1249 	jnb	acc.7,00102$
                                   1250 ;	tmk_core/protocol/report.c:265: add_key_bit(keyboard_report, key);
      006BA1 90 07 29         [24] 1251 	mov	dptr,#_add_key_to_report_keyboard_report_10000_173
      006BA4 E0               [24] 1252 	movx	a,@dptr
      006BA5 FD               [12] 1253 	mov	r5,a
      006BA6 A3               [24] 1254 	inc	dptr
      006BA7 E0               [24] 1255 	movx	a,@dptr
      006BA8 FE               [12] 1256 	mov	r6,a
      006BA9 A3               [24] 1257 	inc	dptr
      006BAA E0               [24] 1258 	movx	a,@dptr
      006BAB FF               [12] 1259 	mov	r7,a
      006BAC 90 07 28         [24] 1260 	mov	dptr,#_add_key_to_report_PARM_2
      006BAF E0               [24] 1261 	movx	a,@dptr
      006BB0 90 07 20         [24] 1262 	mov	dptr,#_add_key_bit_PARM_2
      006BB3 F0               [24] 1263 	movx	@dptr,a
      006BB4 8D 82            [24] 1264 	mov	dpl, r5
      006BB6 8E 83            [24] 1265 	mov	dph, r6
      006BB8 8F F0            [24] 1266 	mov	b, r7
                                   1267 ;	tmk_core/protocol/report.c:266: return;
      006BBA 02 6A C7         [24] 1268 	ljmp	_add_key_bit
      006BBD                       1269 00102$:
                                   1270 ;	tmk_core/protocol/report.c:269: add_key_byte(keyboard_report, key);
      006BBD 90 07 29         [24] 1271 	mov	dptr,#_add_key_to_report_keyboard_report_10000_173
      006BC0 E0               [24] 1272 	movx	a,@dptr
      006BC1 FD               [12] 1273 	mov	r5,a
      006BC2 A3               [24] 1274 	inc	dptr
      006BC3 E0               [24] 1275 	movx	a,@dptr
      006BC4 FE               [12] 1276 	mov	r6,a
      006BC5 A3               [24] 1277 	inc	dptr
      006BC6 E0               [24] 1278 	movx	a,@dptr
      006BC7 FF               [12] 1279 	mov	r7,a
      006BC8 90 07 28         [24] 1280 	mov	dptr,#_add_key_to_report_PARM_2
      006BCB E0               [24] 1281 	movx	a,@dptr
      006BCC 90 07 17         [24] 1282 	mov	dptr,#_add_key_byte_PARM_2
      006BCF F0               [24] 1283 	movx	@dptr,a
      006BD0 8D 82            [24] 1284 	mov	dpl, r5
      006BD2 8E 83            [24] 1285 	mov	dph, r6
      006BD4 8F F0            [24] 1286 	mov	b, r7
                                   1287 ;	tmk_core/protocol/report.c:270: }
      006BD6 02 69 D1         [24] 1288 	ljmp	_add_key_byte
                                   1289 ;------------------------------------------------------------
                                   1290 ;Allocation info for local variables in function 'del_key_from_report'
                                   1291 ;------------------------------------------------------------
                                   1292 ;key           Allocated with name '_del_key_from_report_PARM_2'
                                   1293 ;keyboard_report Allocated with name '_del_key_from_report_keyboard_report_10000_177'
                                   1294 ;------------------------------------------------------------
                                   1295 ;	tmk_core/protocol/report.c:276: void del_key_from_report(report_keyboard_t* keyboard_report, uint8_t key) {
                                   1296 ;	-----------------------------------------
                                   1297 ;	 function del_key_from_report
                                   1298 ;	-----------------------------------------
      006BD9                       1299 _del_key_from_report:
      006BD9 AF F0            [24] 1300 	mov	r7,b
      006BDB AE 83            [24] 1301 	mov	r6,dph
      006BDD E5 82            [12] 1302 	mov	a,dpl
      006BDF 90 07 2D         [24] 1303 	mov	dptr,#_del_key_from_report_keyboard_report_10000_177
      006BE2 F0               [24] 1304 	movx	@dptr,a
      006BE3 EE               [12] 1305 	mov	a,r6
      006BE4 A3               [24] 1306 	inc	dptr
      006BE5 F0               [24] 1307 	movx	@dptr,a
      006BE6 EF               [12] 1308 	mov	a,r7
      006BE7 A3               [24] 1309 	inc	dptr
      006BE8 F0               [24] 1310 	movx	@dptr,a
                                   1311 ;	tmk_core/protocol/report.c:278: if (keyboard_protocol && keymap_config.nkro) {
      006BE9 90 0B 9E         [24] 1312 	mov	dptr,#_keyboard_protocol
      006BEC E0               [24] 1313 	movx	a,@dptr
      006BED 60 23            [24] 1314 	jz	00102$
      006BEF 90 08 BD         [24] 1315 	mov	dptr,#_keymap_config
      006BF2 E0               [24] 1316 	movx	a,@dptr
      006BF3 30 E7 1C         [24] 1317 	jnb	acc.7,00102$
                                   1318 ;	tmk_core/protocol/report.c:279: del_key_bit(keyboard_report, key);
      006BF6 90 07 2D         [24] 1319 	mov	dptr,#_del_key_from_report_keyboard_report_10000_177
      006BF9 E0               [24] 1320 	movx	a,@dptr
      006BFA FD               [12] 1321 	mov	r5,a
      006BFB A3               [24] 1322 	inc	dptr
      006BFC E0               [24] 1323 	movx	a,@dptr
      006BFD FE               [12] 1324 	mov	r6,a
      006BFE A3               [24] 1325 	inc	dptr
      006BFF E0               [24] 1326 	movx	a,@dptr
      006C00 FF               [12] 1327 	mov	r7,a
      006C01 90 07 2C         [24] 1328 	mov	dptr,#_del_key_from_report_PARM_2
      006C04 E0               [24] 1329 	movx	a,@dptr
      006C05 90 07 24         [24] 1330 	mov	dptr,#_del_key_bit_PARM_2
      006C08 F0               [24] 1331 	movx	@dptr,a
      006C09 8D 82            [24] 1332 	mov	dpl, r5
      006C0B 8E 83            [24] 1333 	mov	dph, r6
      006C0D 8F F0            [24] 1334 	mov	b, r7
                                   1335 ;	tmk_core/protocol/report.c:280: return;
      006C0F 02 6B 25         [24] 1336 	ljmp	_del_key_bit
      006C12                       1337 00102$:
                                   1338 ;	tmk_core/protocol/report.c:283: del_key_byte(keyboard_report, key);
      006C12 90 07 2D         [24] 1339 	mov	dptr,#_del_key_from_report_keyboard_report_10000_177
      006C15 E0               [24] 1340 	movx	a,@dptr
      006C16 FD               [12] 1341 	mov	r5,a
      006C17 A3               [24] 1342 	inc	dptr
      006C18 E0               [24] 1343 	movx	a,@dptr
      006C19 FE               [12] 1344 	mov	r6,a
      006C1A A3               [24] 1345 	inc	dptr
      006C1B E0               [24] 1346 	movx	a,@dptr
      006C1C FF               [12] 1347 	mov	r7,a
      006C1D 90 07 2C         [24] 1348 	mov	dptr,#_del_key_from_report_PARM_2
      006C20 E0               [24] 1349 	movx	a,@dptr
      006C21 90 07 1C         [24] 1350 	mov	dptr,#_del_key_byte_PARM_2
      006C24 F0               [24] 1351 	movx	@dptr,a
      006C25 8D 82            [24] 1352 	mov	dpl, r5
      006C27 8E 83            [24] 1353 	mov	dph, r6
      006C29 8F F0            [24] 1354 	mov	b, r7
                                   1355 ;	tmk_core/protocol/report.c:284: }
      006C2B 02 6A 61         [24] 1356 	ljmp	_del_key_byte
                                   1357 ;------------------------------------------------------------
                                   1358 ;Allocation info for local variables in function 'clear_keys_from_report'
                                   1359 ;------------------------------------------------------------
                                   1360 ;keyboard_report Allocated with name '_clear_keys_from_report_keyboard_report_10000_181'
                                   1361 ;------------------------------------------------------------
                                   1362 ;	tmk_core/protocol/report.c:290: void clear_keys_from_report(report_keyboard_t* keyboard_report) {
                                   1363 ;	-----------------------------------------
                                   1364 ;	 function clear_keys_from_report
                                   1365 ;	-----------------------------------------
      006C2E                       1366 _clear_keys_from_report:
      006C2E AF F0            [24] 1367 	mov	r7,b
      006C30 AE 83            [24] 1368 	mov	r6,dph
      006C32 E5 82            [12] 1369 	mov	a,dpl
      006C34 90 07 30         [24] 1370 	mov	dptr,#_clear_keys_from_report_keyboard_report_10000_181
      006C37 F0               [24] 1371 	movx	@dptr,a
      006C38 EE               [12] 1372 	mov	a,r6
      006C39 A3               [24] 1373 	inc	dptr
      006C3A F0               [24] 1374 	movx	@dptr,a
      006C3B EF               [12] 1375 	mov	a,r7
      006C3C A3               [24] 1376 	inc	dptr
      006C3D F0               [24] 1377 	movx	@dptr,a
                                   1378 ;	tmk_core/protocol/report.c:293: if (keyboard_protocol && keymap_config.nkro) {
      006C3E 90 0B 9E         [24] 1379 	mov	dptr,#_keyboard_protocol
      006C41 E0               [24] 1380 	movx	a,@dptr
      006C42 60 30            [24] 1381 	jz	00102$
      006C44 90 08 BD         [24] 1382 	mov	dptr,#_keymap_config
      006C47 E0               [24] 1383 	movx	a,@dptr
      006C48 30 E7 29         [24] 1384 	jnb	acc.7,00102$
                                   1385 ;	tmk_core/protocol/report.c:294: memset(keyboard_report->nkro.bits, 0, sizeof(keyboard_report->nkro.bits));
      006C4B 90 07 30         [24] 1386 	mov	dptr,#_clear_keys_from_report_keyboard_report_10000_181
      006C4E E0               [24] 1387 	movx	a,@dptr
      006C4F FD               [12] 1388 	mov	r5,a
      006C50 A3               [24] 1389 	inc	dptr
      006C51 E0               [24] 1390 	movx	a,@dptr
      006C52 FE               [12] 1391 	mov	r6,a
      006C53 A3               [24] 1392 	inc	dptr
      006C54 E0               [24] 1393 	movx	a,@dptr
      006C55 FF               [12] 1394 	mov	r7,a
      006C56 74 02            [12] 1395 	mov	a,#0x02
      006C58 2D               [12] 1396 	add	a, r5
      006C59 FD               [12] 1397 	mov	r5,a
      006C5A E4               [12] 1398 	clr	a
      006C5B 3E               [12] 1399 	addc	a, r6
      006C5C FE               [12] 1400 	mov	r6,a
      006C5D 90 0B 98         [24] 1401 	mov	dptr,#_memset_PARM_2
      006C60 E4               [12] 1402 	clr	a
      006C61 F0               [24] 1403 	movx	@dptr,a
      006C62 90 0B 99         [24] 1404 	mov	dptr,#_memset_PARM_3
      006C65 74 1E            [12] 1405 	mov	a,#0x1e
      006C67 F0               [24] 1406 	movx	@dptr,a
      006C68 E4               [12] 1407 	clr	a
      006C69 A3               [24] 1408 	inc	dptr
      006C6A F0               [24] 1409 	movx	@dptr,a
      006C6B 8D 82            [24] 1410 	mov	dpl, r5
      006C6D 8E 83            [24] 1411 	mov	dph, r6
      006C6F 8F F0            [24] 1412 	mov	b, r7
                                   1413 ;	tmk_core/protocol/report.c:295: return;
      006C71 02 B5 37         [24] 1414 	ljmp	_memset
      006C74                       1415 00102$:
                                   1416 ;	tmk_core/protocol/report.c:298: memset(keyboard_report->keys, 0, sizeof(keyboard_report->keys));
      006C74 90 07 30         [24] 1417 	mov	dptr,#_clear_keys_from_report_keyboard_report_10000_181
      006C77 E0               [24] 1418 	movx	a,@dptr
      006C78 FD               [12] 1419 	mov	r5,a
      006C79 A3               [24] 1420 	inc	dptr
      006C7A E0               [24] 1421 	movx	a,@dptr
      006C7B FE               [12] 1422 	mov	r6,a
      006C7C A3               [24] 1423 	inc	dptr
      006C7D E0               [24] 1424 	movx	a,@dptr
      006C7E FF               [12] 1425 	mov	r7,a
      006C7F 74 02            [12] 1426 	mov	a,#0x02
      006C81 2D               [12] 1427 	add	a, r5
      006C82 FD               [12] 1428 	mov	r5,a
      006C83 E4               [12] 1429 	clr	a
      006C84 3E               [12] 1430 	addc	a, r6
      006C85 FE               [12] 1431 	mov	r6,a
      006C86 90 0B 98         [24] 1432 	mov	dptr,#_memset_PARM_2
      006C89 E4               [12] 1433 	clr	a
      006C8A F0               [24] 1434 	movx	@dptr,a
      006C8B 90 0B 99         [24] 1435 	mov	dptr,#_memset_PARM_3
      006C8E 74 06            [12] 1436 	mov	a,#0x06
      006C90 F0               [24] 1437 	movx	@dptr,a
      006C91 E4               [12] 1438 	clr	a
      006C92 A3               [24] 1439 	inc	dptr
      006C93 F0               [24] 1440 	movx	@dptr,a
      006C94 8D 82            [24] 1441 	mov	dpl, r5
      006C96 8E 83            [24] 1442 	mov	dph, r6
      006C98 8F F0            [24] 1443 	mov	b, r7
                                   1444 ;	tmk_core/protocol/report.c:299: }
      006C9A 02 B5 37         [24] 1445 	ljmp	_memset
                                   1446 	.area CSEG    (CODE)
                                   1447 	.area CONST   (CODE)
                                   1448 	.area CONST   (CODE)
      00B642                       1449 _KEYCODE2CONSUMER_usages_10000_119:
      00B642 E2 00                 1450 	.byte #0xe2, #0x00	; 226
      00B644 E9 00                 1451 	.byte #0xe9, #0x00	; 233
      00B646 EA 00                 1452 	.byte #0xea, #0x00	; 234
      00B648 B5 00                 1453 	.byte #0xb5, #0x00	; 181
      00B64A B6 00                 1454 	.byte #0xb6, #0x00	; 182
      00B64C B7 00                 1455 	.byte #0xb7, #0x00	; 183
      00B64E CD 00                 1456 	.byte #0xcd, #0x00	; 205
      00B650 83 01                 1457 	.byte #0x83, #0x01	; 387
      00B652 CC 00                 1458 	.byte #0xcc, #0x00	; 204
      00B654 8A 01                 1459 	.byte #0x8a, #0x01	; 394
      00B656 92 01                 1460 	.byte #0x92, #0x01	; 402
      00B658 94 01                 1461 	.byte #0x94, #0x01	; 404
      00B65A 21 02                 1462 	.byte #0x21, #0x02	; 545
      00B65C 23 02                 1463 	.byte #0x23, #0x02	; 547
      00B65E 24 02                 1464 	.byte #0x24, #0x02	; 548
      00B660 25 02                 1465 	.byte #0x25, #0x02	; 549
      00B662 26 02                 1466 	.byte #0x26, #0x02	; 550
      00B664 27 02                 1467 	.byte #0x27, #0x02	; 551
      00B666 2A 02                 1468 	.byte #0x2a, #0x02	; 554
      00B668 B3 00                 1469 	.byte #0xb3, #0x00	; 179
      00B66A B4 00                 1470 	.byte #0xb4, #0x00	; 180
      00B66C 6F 00                 1471 	.byte #0x6f, #0x00	; 111
      00B66E 70 00                 1472 	.byte #0x70, #0x00	; 112
      00B670 9F 01                 1473 	.byte #0x9f, #0x01	; 415
      00B672 CB 01                 1474 	.byte #0xcb, #0x01	; 459
      00B674 9F 02                 1475 	.byte #0x9f, #0x02	; 671
      00B676 A0 02                 1476 	.byte #0xa0, #0x02	; 672
                                   1477 	.area CSEG    (CODE)
                                   1478 	.area XINIT   (CODE)
                                   1479 	.area CABS    (ABS,CODE)
