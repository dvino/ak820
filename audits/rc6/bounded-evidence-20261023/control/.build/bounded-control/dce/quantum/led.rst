                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module led
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _timer_elapsed32
                                     12 	.globl _timer_read32
                                     13 	.globl _host_keyboard_leds
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
                                    257 	.globl _led_update_ports_PARM_1
                                    258 	.globl _led_update_kb_PARM_1
                                    259 	.globl _led_update_user_PARM_1
                                    260 	.globl _led_update_user
                                    261 	.globl _led_update_kb
                                    262 	.globl _led_update_ports
                                    263 	.globl _led_init_ports
                                    264 	.globl _led_set
                                    265 	.globl _led_task
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
      000999                        552 _led_update_user_PARM_1:
      000999                        553 	.ds 1
      00099A                        554 _led_update_kb_PARM_1:
      00099A                        555 	.ds 1
      00099B                        556 _led_update_ports_PARM_1:
      00099B                        557 	.ds 1
      00099C                        558 _led_set_usb_led_10000_157:
      00099C                        559 	.ds 1
      00099D                        560 _led_set_usb_led_casted_10001_159:
      00099D                        561 	.ds 1
      00099E                        562 _led_task_last_led_status_10000_165:
      00099E                        563 	.ds 1
                                    564 ;--------------------------------------------------------
                                    565 ; absolute external ram data
                                    566 ;--------------------------------------------------------
                                    567 	.area XABS    (ABS,XDATA)
                                    568 ;--------------------------------------------------------
                                    569 ; initialized external ram data
                                    570 ;--------------------------------------------------------
                                    571 	.area XISEG   (XDATA)
      000BFA                        572 _last_led_modification_time:
      000BFA                        573 	.ds 4
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
                                    591 ;------------------------------------------------------------
                                    592 ;Allocation info for local variables in function 'led_task'
                                    593 ;------------------------------------------------------------
                                    594 ;last_led_status Allocated with name '_led_task_last_led_status_10000_165'
                                    595 ;led_status    Allocated with name '_led_task_led_status_10000_165'
                                    596 ;------------------------------------------------------------
                                    597 ;	quantum/led.c:181: static uint8_t last_led_status = 0;
      00311C 90 09 9E         [24]  598 	mov	dptr,#_led_task_last_led_status_10000_165
      00311F E4               [12]  599 	clr	a
      003120 F0               [24]  600 	movx	@dptr,a
                                    601 ;--------------------------------------------------------
                                    602 ; Home
                                    603 ;--------------------------------------------------------
                                    604 	.area HOME    (CODE)
                                    605 	.area HOME    (CODE)
                                    606 ;--------------------------------------------------------
                                    607 ; code
                                    608 ;--------------------------------------------------------
                                    609 	.area CSEG    (CODE)
                                    610 ;------------------------------------------------------------
                                    611 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    612 ;------------------------------------------------------------
                                    613 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_51'
                                    614 ;------------------------------------------------------------
                                    615 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    616 ;	-----------------------------------------
                           000007   617 	ar7 = 0x07
                           000006   618 	ar6 = 0x06
                           000005   619 	ar5 = 0x05
                           000004   620 	ar4 = 0x04
                           000003   621 	ar3 = 0x03
                           000002   622 	ar2 = 0x02
                           000001   623 	ar1 = 0x01
                           000000   624 	ar0 = 0x00
                                    625 ;	 function led_update_user
                                    626 ;	-----------------------------------------
      0090B4                        627 _led_update_user:
                                    628 ;	quantum/led.c:77: return true;
      0090B4 75 82 01         [24]  629 	mov	dpl, #0x01
                                    630 ;	quantum/led.c:78: }
      0090B7 22               [24]  631 	ret
                                    632 ;------------------------------------------------------------
                                    633 ;Allocation info for local variables in function 'led_update_kb'
                                    634 ;------------------------------------------------------------
                                    635 ;led_state     Allocated with name '_led_update_kb_PARM_1'
                                    636 ;res           Allocated with name '_led_update_kb_res_10000_148'
                                    637 ;------------------------------------------------------------
                                    638 ;	quantum/led.c:84: __attribute__((weak)) bool led_update_kb(led_t led_state) {
                                    639 ;	-----------------------------------------
                                    640 ;	 function led_update_kb
                                    641 ;	-----------------------------------------
      0090B8                        642 _led_update_kb:
                                    643 ;	quantum/led.c:85: bool res = led_update_user(led_state);
      0090B8 90 0B 90         [24]  644 	mov	dptr,#___memcpy_PARM_2
      0090BB 74 9A            [12]  645 	mov	a,#_led_update_kb_PARM_1
      0090BD F0               [24]  646 	movx	@dptr,a
      0090BE 74 09            [12]  647 	mov	a,#(_led_update_kb_PARM_1 >> 8)
      0090C0 12 91 42         [24]  648 	lcall	_ak820_outline_0017
      0090C3 90 09 99         [24]  649 	mov	dptr,#_led_update_user_PARM_1
      0090C6 F5 F0            [12]  650 	mov	b,a
      0090C8 12 B4 BE         [24]  651 	lcall	___memcpy
      0090CB 12 90 B4         [24]  652 	lcall	_led_update_user
                                    653 ;	quantum/led.c:86: if (res) {
      0090CE E5 82            [12]  654 	mov	a,dpl
      0090D0 FF               [12]  655 	mov	r7,a
      0090D1 60 1A            [24]  656 	jz	00102$
                                    657 ;	quantum/led.c:87: led_update_ports(led_state);
      0090D3 90 0B 90         [24]  658 	mov	dptr,#___memcpy_PARM_2
      0090D6 74 9A            [12]  659 	mov	a,#_led_update_kb_PARM_1
      0090D8 F0               [24]  660 	movx	@dptr,a
      0090D9 74 09            [12]  661 	mov	a,#(_led_update_kb_PARM_1 >> 8)
      0090DB 12 91 42         [24]  662 	lcall	_ak820_outline_0017
      0090DE 90 09 9B         [24]  663 	mov	dptr,#_led_update_ports_PARM_1
      0090E1 F5 F0            [12]  664 	mov	b,a
      0090E3 C0 07            [24]  665 	push	ar7
      0090E5 12 B4 BE         [24]  666 	lcall	___memcpy
      0090E8 12 90 F0         [24]  667 	lcall	_led_update_ports
      0090EB D0 07            [24]  668 	pop	ar7
      0090ED                        669 00102$:
                                    670 ;	quantum/led.c:89: return res;
      0090ED 8F 82            [24]  671 	mov	dpl, r7
                                    672 ;	quantum/led.c:90: }
      0090EF 22               [24]  673 	ret
                                    674 ;------------------------------------------------------------
                                    675 ;Allocation info for local variables in function 'led_update_ports'
                                    676 ;------------------------------------------------------------
                                    677 ;led_state     Allocated with name '_led_update_ports_PARM_1'
                                    678 ;------------------------------------------------------------
                                    679 ;	quantum/led.c:94: __attribute__((weak)) void led_update_ports(led_t led_state) {
                                    680 ;	-----------------------------------------
                                    681 ;	 function led_update_ports
                                    682 ;	-----------------------------------------
      0090F0                        683 _led_update_ports:
                                    684 ;	quantum/led.c:115: }
      0090F0 22               [24]  685 	ret
                                    686 ;------------------------------------------------------------
                                    687 ;Allocation info for local variables in function 'led_init_ports'
                                    688 ;------------------------------------------------------------
                                    689 ;	quantum/led.c:119: __attribute__((weak)) void led_init_ports(void) {
                                    690 ;	-----------------------------------------
                                    691 ;	 function led_init_ports
                                    692 ;	-----------------------------------------
      0090F1                        693 _led_init_ports:
                                    694 ;	quantum/led.c:140: }
      0090F1 22               [24]  695 	ret
                                    696 ;------------------------------------------------------------
                                    697 ;Allocation info for local variables in function 'led_set'
                                    698 ;------------------------------------------------------------
                                    699 ;usb_led       Allocated with name '_led_set_usb_led_10000_157'
                                    700 ;usb_led_casted Allocated with name '_led_set_usb_led_casted_10001_159'
                                    701 ;------------------------------------------------------------
                                    702 ;	quantum/led.c:144: __attribute__((weak)) void led_set(uint8_t usb_led) {
                                    703 ;	-----------------------------------------
                                    704 ;	 function led_set
                                    705 ;	-----------------------------------------
      0090F2                        706 _led_set:
      0090F2 E5 82            [12]  707 	mov	a,dpl
      0090F4 90 09 9C         [24]  708 	mov	dptr,#_led_set_usb_led_10000_157
      0090F7 F0               [24]  709 	movx	@dptr,a
                                    710 ;	quantum/led.c:153: usb_led_casted.raw = usb_led;
      0090F8 E0               [24]  711 	movx	a,@dptr
      0090F9 90 09 9D         [24]  712 	mov	dptr,#_led_set_usb_led_casted_10001_159
      0090FC F0               [24]  713 	movx	@dptr,a
                                    714 ;	quantum/led.c:154: led_update_kb(usb_led_casted);
      0090FD 90 0B 90         [24]  715 	mov	dptr,#___memcpy_PARM_2
      009100 74 9D            [12]  716 	mov	a,#_led_set_usb_led_casted_10001_159
      009102 F0               [24]  717 	movx	@dptr,a
      009103 74 09            [12]  718 	mov	a,#(_led_set_usb_led_casted_10001_159 >> 8)
      009105 12 91 42         [24]  719 	lcall	_ak820_outline_0017
      009108 90 09 9A         [24]  720 	mov	dptr,#_led_update_kb_PARM_1
      00910B F5 F0            [12]  721 	mov	b,a
      00910D 12 B4 BE         [24]  722 	lcall	___memcpy
                                    723 ;	quantum/led.c:155: }
      009110 02 90 B8         [24]  724 	ljmp	_led_update_kb
                                    725 ;------------------------------------------------------------
                                    726 ;Allocation info for local variables in function 'led_suspend'
                                    727 ;------------------------------------------------------------
                                    728 ;leds_off      Allocated with name '_led_suspend_leds_off_10000_161'
                                    729 ;------------------------------------------------------------
                                    730 ;	quantum/led.c:159: void led_suspend(void) {
                                    731 ;	-----------------------------------------
                                    732 ;	 function led_task
                                    733 ;	-----------------------------------------
      009113                        734 _led_task:
                                    735 ;	quantum/led.c:184: uint8_t led_status = host_keyboard_leds();
      009113 12 67 22         [24]  736 	lcall	_host_keyboard_leds
      009116 AF 82            [24]  737 	mov	r7, dpl
                                    738 ;	quantum/led.c:185: if (last_led_status != led_status) {
      009118 90 09 9E         [24]  739 	mov	dptr,#_led_task_last_led_status_10000_165
      00911B E0               [24]  740 	movx	a,@dptr
      00911C B5 07 01         [24]  741 	cjne	a,ar7,00114$
      00911F 22               [24]  742 	ret
      009120                        743 00114$:
                                    744 ;	quantum/led.c:186: last_led_status            = led_status;
      009120 90 09 9E         [24]  745 	mov	dptr,#_led_task_last_led_status_10000_165
      009123 EF               [12]  746 	mov	a,r7
      009124 F0               [24]  747 	movx	@dptr,a
                                    748 ;	quantum/led.c:187: last_led_modification_time = timer_read32();
      009125 12 40 3C         [24]  749 	lcall	_timer_read32
      009128 AB 82            [24]  750 	mov	r3, dpl
      00912A AC 83            [24]  751 	mov	r4, dph
      00912C AD F0            [24]  752 	mov	r5, b
      00912E FE               [12]  753 	mov	r6, a
      00912F 90 0B FA         [24]  754 	mov	dptr,#_last_led_modification_time
      009132 EB               [12]  755 	mov	a,r3
      009133 F0               [24]  756 	movx	@dptr,a
      009134 EC               [12]  757 	mov	a,r4
      009135 A3               [24]  758 	inc	dptr
      009136 F0               [24]  759 	movx	@dptr,a
      009137 ED               [12]  760 	mov	a,r5
      009138 A3               [24]  761 	inc	dptr
      009139 F0               [24]  762 	movx	@dptr,a
      00913A EE               [12]  763 	mov	a,r6
      00913B A3               [24]  764 	inc	dptr
      00913C F0               [24]  765 	movx	@dptr,a
                                    766 ;	quantum/led.c:194: led_set(led_status);
      00913D 8F 82            [24]  767 	mov	dpl, r7
                                    768 ;	quantum/led.c:196: }
      00913F 02 90 F2         [24]  769 	ljmp	_led_set
                                    770 	.area CSEG    (CODE)
                                    771 	.area CONST   (CODE)
                                    772 	.area XINIT   (CODE)
      00BDD7                        773 __xinit__last_led_modification_time:
      00BDD7 00 00 00 00            774 	.byte #0x00, #0x00, #0x00, #0x00	; 0
                                    775 	.area CABS    (ABS,CODE)
                                    776 
                                    777 ; Experimental exact instruction outlining.
                                    778 	.globl _ak820_outline_0017
                                    779 
                                    780 	.area CSEG (CODE)
                                    781 ; function ak820_outline_0017
      009142                        782 _ak820_outline_0017:
      009142 A3               [24]  783 	inc	dptr
      009143 F0               [24]  784 	movx	@dptr,a
      009144 E4               [12]  785 	clr	a
      009145 A3               [24]  786 	inc	dptr
      009146 F0               [24]  787 	movx	@dptr,a
      009147 90 0B 93         [24]  788 	mov	dptr,#___memcpy_PARM_3
      00914A 04               [12]  789 	inc	a
      00914B F0               [24]  790 	movx	@dptr,a
      00914C E4               [12]  791 	clr	a
      00914D A3               [24]  792 	inc	dptr
      00914E F0               [24]  793 	movx	@dptr,a
      00914F 22               [24]  794 	ret
