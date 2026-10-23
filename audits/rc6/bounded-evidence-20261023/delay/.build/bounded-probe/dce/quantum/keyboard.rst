                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module keyboard
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _quantum_task
                                     12 	.globl _switch_events
                                     13 	.globl _quantum_init
                                     14 	.globl _should_process_keypress
                                     15 	.globl _last_encoder_activity_trigger
                                     16 	.globl _last_matrix_activity_trigger
                                     17 	.globl _caps_word_task
                                     18 	.globl _vial_unlock_task
                                     19 	.globl _vial_init
                                     20 	.globl _eeprom_driver_init
                                     21 	.globl _via_init
                                     22 	.globl _encoder_read
                                     23 	.globl _encoder_init
                                     24 	.globl _rgb_matrix_init
                                     25 	.globl _rgb_matrix_task
                                     26 	.globl _process_rgb_matrix
                                     27 	.globl _action_exec
                                     28 	.globl _print_set_sendchar
                                     29 	.globl _sendchar
                                     30 	.globl _led_task
                                     31 	.globl _led_init_ports
                                     32 	.globl _magic
                                     33 	.globl _matrix_print
                                     34 	.globl _matrix_get_row
                                     35 	.globl _matrix_scan
                                     36 	.globl _matrix_init
                                     37 	.globl _keyboard_post_init_user
                                     38 	.globl _timer_elapsed32
                                     39 	.globl _timer_read32
                                     40 	.globl _timer_read
                                     41 	.globl _timer_init
                                     42 	.globl _ADC_START
                                     43 	.globl _S0_R_FIFO
                                     44 	.globl _S0_T_FIFO
                                     45 	.globl _S0_FREE
                                     46 	.globl _S0_IF_BYTE
                                     47 	.globl _S0_IF_FIRST
                                     48 	.globl _S0_IF_OV
                                     49 	.globl _S0_FST_ACT
                                     50 	.globl _CP_RL2
                                     51 	.globl _C_T2
                                     52 	.globl _TR2
                                     53 	.globl _EXEN2
                                     54 	.globl _TCLK
                                     55 	.globl _RCLK
                                     56 	.globl _EXF2
                                     57 	.globl _CAP1F
                                     58 	.globl _TF2
                                     59 	.globl _RI
                                     60 	.globl _TI
                                     61 	.globl _RB8
                                     62 	.globl _TB8
                                     63 	.globl _REN
                                     64 	.globl _SM2
                                     65 	.globl _SM1
                                     66 	.globl _SM0
                                     67 	.globl _IT0
                                     68 	.globl _IE0
                                     69 	.globl _IT1
                                     70 	.globl _IE1
                                     71 	.globl _TR0
                                     72 	.globl _TF0
                                     73 	.globl _TR1
                                     74 	.globl _TF1
                                     75 	.globl _P4_0
                                     76 	.globl _P4_1
                                     77 	.globl _P4_2
                                     78 	.globl _P4_3
                                     79 	.globl _P4_4
                                     80 	.globl _P4_5
                                     81 	.globl _P4_6
                                     82 	.globl _RXD
                                     83 	.globl _TXD
                                     84 	.globl _INT0
                                     85 	.globl _INT1
                                     86 	.globl _T0
                                     87 	.globl _T1
                                     88 	.globl _MOSI1
                                     89 	.globl _MISO1
                                     90 	.globl _SCK1
                                     91 	.globl _P3_0
                                     92 	.globl _P3_1
                                     93 	.globl _P3_2
                                     94 	.globl _P3_3
                                     95 	.globl _P3_4
                                     96 	.globl _P3_5
                                     97 	.globl _P3_6
                                     98 	.globl _P3_7
                                     99 	.globl _CAP1_
                                    100 	.globl _T2_
                                    101 	.globl _CAP2_
                                    102 	.globl _T2EX_
                                    103 	.globl _RXD1
                                    104 	.globl _TXD1
                                    105 	.globl _P2_0
                                    106 	.globl _P2_1
                                    107 	.globl _P2_2
                                    108 	.globl _P2_3
                                    109 	.globl _P2_4
                                    110 	.globl _P2_5
                                    111 	.globl _P2_6
                                    112 	.globl _P2_7
                                    113 	.globl _AIN0
                                    114 	.globl _AIN1
                                    115 	.globl _AIN2
                                    116 	.globl _AIN3
                                    117 	.globl _AIN4
                                    118 	.globl _AIN5
                                    119 	.globl _AIN6
                                    120 	.globl _AIN7
                                    121 	.globl _CAP1
                                    122 	.globl _T2
                                    123 	.globl _CAP2
                                    124 	.globl _T2EX
                                    125 	.globl _INT0_
                                    126 	.globl _SCS
                                    127 	.globl _MOSI
                                    128 	.globl _MISO
                                    129 	.globl _SCK
                                    130 	.globl _RXD1_
                                    131 	.globl _TXD1_
                                    132 	.globl _P1_0
                                    133 	.globl _P1_1
                                    134 	.globl _P1_2
                                    135 	.globl _P1_3
                                    136 	.globl _P1_4
                                    137 	.globl _P1_5
                                    138 	.globl _P1_6
                                    139 	.globl _P1_7
                                    140 	.globl _AIN8
                                    141 	.globl _AIN9
                                    142 	.globl _AIN10
                                    143 	.globl _AIN11
                                    144 	.globl _AIN12
                                    145 	.globl _AIN13
                                    146 	.globl _RXD_
                                    147 	.globl _TXD_
                                    148 	.globl _SCL0
                                    149 	.globl _SDA0
                                    150 	.globl _P0_0
                                    151 	.globl _P0_1
                                    152 	.globl _P0_2
                                    153 	.globl _P0_3
                                    154 	.globl _P0_4
                                    155 	.globl _P0_5
                                    156 	.globl _P0_6
                                    157 	.globl _P0_7
                                    158 	.globl _IE_SPI0
                                    159 	.globl _IE_USB
                                    160 	.globl _IE_ADC
                                    161 	.globl _IE_UART1
                                    162 	.globl _IE_PWM_I2C
                                    163 	.globl _IE_GPIO
                                    164 	.globl _IE_WDOG
                                    165 	.globl _PX0
                                    166 	.globl _PT0
                                    167 	.globl _PX1
                                    168 	.globl _PT1
                                    169 	.globl _PS
                                    170 	.globl _PT2
                                    171 	.globl _PL_FLAG
                                    172 	.globl _PH_FLAG
                                    173 	.globl _EX0
                                    174 	.globl _ET0
                                    175 	.globl _EX1
                                    176 	.globl _ET1
                                    177 	.globl _ES
                                    178 	.globl _ET2
                                    179 	.globl _E_DIS
                                    180 	.globl _EA
                                    181 	.globl _P
                                    182 	.globl _F1
                                    183 	.globl _OV
                                    184 	.globl _RS0
                                    185 	.globl _RS1
                                    186 	.globl _F0
                                    187 	.globl _AC
                                    188 	.globl _CY
                                    189 	.globl _I2CS_INT_ST
                                    190 	.globl _I2CX_INT
                                    191 	.globl _LED_STATUS
                                    192 	.globl _LED_DMA_H
                                    193 	.globl _LED_DMA_L
                                    194 	.globl _LED_DMA
                                    195 	.globl _LED_PWM_OE
                                    196 	.globl _LED_COMMON
                                    197 	.globl _ADC_CHAN
                                    198 	.globl _ADC_DAT_H
                                    199 	.globl _ADC_DAT_L
                                    200 	.globl _ADC_DAT
                                    201 	.globl _ADC_CTRL
                                    202 	.globl _SPI1_CK_SE
                                    203 	.globl _SPI1_CTRL
                                    204 	.globl _SPI1_DATA
                                    205 	.globl _SPI1_STAT
                                    206 	.globl _SIF1
                                    207 	.globl _SBAUD1
                                    208 	.globl _SBUF1
                                    209 	.globl _SCON1
                                    210 	.globl _SPI0_SETUP
                                    211 	.globl _SPI0_CK_SE
                                    212 	.globl _SPI0_CTRL
                                    213 	.globl _SPI0_DATA
                                    214 	.globl _SPI0_STAT
                                    215 	.globl _T2CAP1H
                                    216 	.globl _T2CAP1L
                                    217 	.globl _T2CAP1
                                    218 	.globl _TH2
                                    219 	.globl _TL2
                                    220 	.globl _T2COUNT
                                    221 	.globl _RCAP2H
                                    222 	.globl _RCAP2L
                                    223 	.globl _RCAP2
                                    224 	.globl _T2MOD
                                    225 	.globl _T2CON
                                    226 	.globl _SBUF
                                    227 	.globl _SCON
                                    228 	.globl _TH1
                                    229 	.globl _TH0
                                    230 	.globl _TL1
                                    231 	.globl _TL0
                                    232 	.globl _TMOD
                                    233 	.globl _TCON
                                    234 	.globl _XBUS_AUX
                                    235 	.globl _P7
                                    236 	.globl _P6_DIR
                                    237 	.globl _P6_OUT_PU
                                    238 	.globl _P6_IN
                                    239 	.globl _P5_DIR
                                    240 	.globl _P5_OUT_PU
                                    241 	.globl _P5_IN
                                    242 	.globl _P4_LED_KEY
                                    243 	.globl _P4_DIR_PU
                                    244 	.globl _P4_MOD_OC
                                    245 	.globl _P4
                                    246 	.globl _P3_DIR_PU
                                    247 	.globl _P3_MOD_OC
                                    248 	.globl _P3
                                    249 	.globl _P2_DIR_PU
                                    250 	.globl _P2_MOD_OC
                                    251 	.globl _P2
                                    252 	.globl _P1_DIR_PU
                                    253 	.globl _P1_MOD_OC
                                    254 	.globl _P1
                                    255 	.globl _P0_DIR_PU
                                    256 	.globl _P0_MOD_OC
                                    257 	.globl _P0
                                    258 	.globl _ROM_CTRL
                                    259 	.globl _ROM_DATA_HH
                                    260 	.globl _ROM_DATA_HL
                                    261 	.globl _ROM_DATA_HI
                                    262 	.globl _ROM_ADDR_H
                                    263 	.globl _ROM_ADDR_L
                                    264 	.globl _ROM_ADDR
                                    265 	.globl _GPIO_IE
                                    266 	.globl _IP_EX
                                    267 	.globl _IE_EX
                                    268 	.globl _IP
                                    269 	.globl _IE
                                    270 	.globl _WDOG_COUNT
                                    271 	.globl _RESET_KEEP
                                    272 	.globl _WAKE_CTRL
                                    273 	.globl _CLOCK_CFG
                                    274 	.globl _POWER_CFG
                                    275 	.globl _PCON
                                    276 	.globl _GLOBAL_CFG
                                    277 	.globl _SAFE_MOD
                                    278 	.globl _DPH
                                    279 	.globl _DPL
                                    280 	.globl _SP
                                    281 	.globl _A_INV
                                    282 	.globl _B
                                    283 	.globl _ACC
                                    284 	.globl _PSW
                                    285 	.globl _switch_events_PARM_3
                                    286 	.globl _switch_events_PARM_2
                                    287 	.globl _keyboard_post_init_kb
                                    288 	.globl _matrix_can_read
                                    289 	.globl _keyboard_setup
                                    290 	.globl _is_keyboard_master
                                    291 	.globl _housekeeping_task
                                    292 	.globl _keyboard_init
                                    293 	.globl _keyboard_task
                                    294 ;--------------------------------------------------------
                                    295 ; special function registers
                                    296 ;--------------------------------------------------------
                                    297 	.area RSEG    (ABS,DATA)
      000000                        298 	.org 0x0000
                           0000D0   299 _PSW	=	0x00d0
                           0000E0   300 _ACC	=	0x00e0
                           0000F0   301 _B	=	0x00f0
                           0000FD   302 _A_INV	=	0x00fd
                           000081   303 _SP	=	0x0081
                           000082   304 _DPL	=	0x0082
                           000083   305 _DPH	=	0x0083
                           0000A1   306 _SAFE_MOD	=	0x00a1
                           0000B1   307 _GLOBAL_CFG	=	0x00b1
                           000087   308 _PCON	=	0x0087
                           0000BA   309 _POWER_CFG	=	0x00ba
                           0000B9   310 _CLOCK_CFG	=	0x00b9
                           0000A9   311 _WAKE_CTRL	=	0x00a9
                           0000FE   312 _RESET_KEEP	=	0x00fe
                           0000FF   313 _WDOG_COUNT	=	0x00ff
                           0000A8   314 _IE	=	0x00a8
                           0000B8   315 _IP	=	0x00b8
                           0000E8   316 _IE_EX	=	0x00e8
                           0000E9   317 _IP_EX	=	0x00e9
                           0000B2   318 _GPIO_IE	=	0x00b2
                           008584   319 _ROM_ADDR	=	0x8584
                           000084   320 _ROM_ADDR_L	=	0x0084
                           000085   321 _ROM_ADDR_H	=	0x0085
                           008F8E   322 _ROM_DATA_HI	=	0x8f8e
                           00008E   323 _ROM_DATA_HL	=	0x008e
                           00008F   324 _ROM_DATA_HH	=	0x008f
                           000086   325 _ROM_CTRL	=	0x0086
                           000080   326 _P0	=	0x0080
                           0000C4   327 _P0_MOD_OC	=	0x00c4
                           0000C5   328 _P0_DIR_PU	=	0x00c5
                           000090   329 _P1	=	0x0090
                           000092   330 _P1_MOD_OC	=	0x0092
                           000093   331 _P1_DIR_PU	=	0x0093
                           0000A0   332 _P2	=	0x00a0
                           000094   333 _P2_MOD_OC	=	0x0094
                           000095   334 _P2_DIR_PU	=	0x0095
                           0000B0   335 _P3	=	0x00b0
                           000096   336 _P3_MOD_OC	=	0x0096
                           000097   337 _P3_DIR_PU	=	0x0097
                           0000C0   338 _P4	=	0x00c0
                           0000C2   339 _P4_MOD_OC	=	0x00c2
                           0000C3   340 _P4_DIR_PU	=	0x00c3
                           0000C1   341 _P4_LED_KEY	=	0x00c1
                           0000AA   342 _P5_IN	=	0x00aa
                           0000AB   343 _P5_OUT_PU	=	0x00ab
                           0000AC   344 _P5_DIR	=	0x00ac
                           0000AD   345 _P6_IN	=	0x00ad
                           0000AE   346 _P6_OUT_PU	=	0x00ae
                           0000AF   347 _P6_DIR	=	0x00af
                           0000F1   348 _P7	=	0x00f1
                           0000A2   349 _XBUS_AUX	=	0x00a2
                           000088   350 _TCON	=	0x0088
                           000089   351 _TMOD	=	0x0089
                           00008A   352 _TL0	=	0x008a
                           00008B   353 _TL1	=	0x008b
                           00008C   354 _TH0	=	0x008c
                           00008D   355 _TH1	=	0x008d
                           000098   356 _SCON	=	0x0098
                           000099   357 _SBUF	=	0x0099
                           0000C8   358 _T2CON	=	0x00c8
                           0000C9   359 _T2MOD	=	0x00c9
                           00CBCA   360 _RCAP2	=	0xcbca
                           0000CA   361 _RCAP2L	=	0x00ca
                           0000CB   362 _RCAP2H	=	0x00cb
                           00CDCC   363 _T2COUNT	=	0xcdcc
                           0000CC   364 _TL2	=	0x00cc
                           0000CD   365 _TH2	=	0x00cd
                           00CFCE   366 _T2CAP1	=	0xcfce
                           0000CE   367 _T2CAP1L	=	0x00ce
                           0000CF   368 _T2CAP1H	=	0x00cf
                           0000F8   369 _SPI0_STAT	=	0x00f8
                           0000F9   370 _SPI0_DATA	=	0x00f9
                           0000FA   371 _SPI0_CTRL	=	0x00fa
                           0000FB   372 _SPI0_CK_SE	=	0x00fb
                           0000FC   373 _SPI0_SETUP	=	0x00fc
                           0000BC   374 _SCON1	=	0x00bc
                           0000BD   375 _SBUF1	=	0x00bd
                           0000BE   376 _SBAUD1	=	0x00be
                           0000BF   377 _SIF1	=	0x00bf
                           0000B4   378 _SPI1_STAT	=	0x00b4
                           0000B5   379 _SPI1_DATA	=	0x00b5
                           0000B6   380 _SPI1_CTRL	=	0x00b6
                           0000B7   381 _SPI1_CK_SE	=	0x00b7
                           0000F3   382 _ADC_CTRL	=	0x00f3
                           00F5F4   383 _ADC_DAT	=	0xf5f4
                           0000F4   384 _ADC_DAT_L	=	0x00f4
                           0000F5   385 _ADC_DAT_H	=	0x00f5
                           0000F6   386 _ADC_CHAN	=	0x00f6
                           0000A6   387 _LED_COMMON	=	0x00a6
                           0000A7   388 _LED_PWM_OE	=	0x00a7
                           00C7C6   389 _LED_DMA	=	0xc7c6
                           0000C6   390 _LED_DMA_L	=	0x00c6
                           0000C7   391 _LED_DMA_H	=	0x00c7
                           0000F7   392 _LED_STATUS	=	0x00f7
                           0000B3   393 _I2CX_INT	=	0x00b3
                           0000BB   394 _I2CS_INT_ST	=	0x00bb
                                    395 ;--------------------------------------------------------
                                    396 ; special function bits
                                    397 ;--------------------------------------------------------
                                    398 	.area RSEG    (ABS,DATA)
      000000                        399 	.org 0x0000
                           0000D7   400 _CY	=	0x00d7
                           0000D6   401 _AC	=	0x00d6
                           0000D5   402 _F0	=	0x00d5
                           0000D4   403 _RS1	=	0x00d4
                           0000D3   404 _RS0	=	0x00d3
                           0000D2   405 _OV	=	0x00d2
                           0000D1   406 _F1	=	0x00d1
                           0000D0   407 _P	=	0x00d0
                           0000AF   408 _EA	=	0x00af
                           0000AE   409 _E_DIS	=	0x00ae
                           0000AD   410 _ET2	=	0x00ad
                           0000AC   411 _ES	=	0x00ac
                           0000AB   412 _ET1	=	0x00ab
                           0000AA   413 _EX1	=	0x00aa
                           0000A9   414 _ET0	=	0x00a9
                           0000A8   415 _EX0	=	0x00a8
                           0000BF   416 _PH_FLAG	=	0x00bf
                           0000BE   417 _PL_FLAG	=	0x00be
                           0000BD   418 _PT2	=	0x00bd
                           0000BC   419 _PS	=	0x00bc
                           0000BB   420 _PT1	=	0x00bb
                           0000BA   421 _PX1	=	0x00ba
                           0000B9   422 _PT0	=	0x00b9
                           0000B8   423 _PX0	=	0x00b8
                           0000EF   424 _IE_WDOG	=	0x00ef
                           0000EE   425 _IE_GPIO	=	0x00ee
                           0000ED   426 _IE_PWM_I2C	=	0x00ed
                           0000EC   427 _IE_UART1	=	0x00ec
                           0000EB   428 _IE_ADC	=	0x00eb
                           0000E9   429 _IE_USB	=	0x00e9
                           0000E8   430 _IE_SPI0	=	0x00e8
                           000087   431 _P0_7	=	0x0087
                           000086   432 _P0_6	=	0x0086
                           000085   433 _P0_5	=	0x0085
                           000084   434 _P0_4	=	0x0084
                           000083   435 _P0_3	=	0x0083
                           000082   436 _P0_2	=	0x0082
                           000081   437 _P0_1	=	0x0081
                           000080   438 _P0_0	=	0x0080
                           000081   439 _SDA0	=	0x0081
                           000080   440 _SCL0	=	0x0080
                           000083   441 _TXD_	=	0x0083
                           000082   442 _RXD_	=	0x0082
                           000085   443 _AIN13	=	0x0085
                           000084   444 _AIN12	=	0x0084
                           000083   445 _AIN11	=	0x0083
                           000082   446 _AIN10	=	0x0082
                           000081   447 _AIN9	=	0x0081
                           000080   448 _AIN8	=	0x0080
                           000097   449 _P1_7	=	0x0097
                           000096   450 _P1_6	=	0x0096
                           000095   451 _P1_5	=	0x0095
                           000094   452 _P1_4	=	0x0094
                           000093   453 _P1_3	=	0x0093
                           000092   454 _P1_2	=	0x0092
                           000091   455 _P1_1	=	0x0091
                           000090   456 _P1_0	=	0x0090
                           000097   457 _TXD1_	=	0x0097
                           000096   458 _RXD1_	=	0x0096
                           000097   459 _SCK	=	0x0097
                           000096   460 _MISO	=	0x0096
                           000095   461 _MOSI	=	0x0095
                           000094   462 _SCS	=	0x0094
                           000092   463 _INT0_	=	0x0092
                           000091   464 _T2EX	=	0x0091
                           000091   465 _CAP2	=	0x0091
                           000090   466 _T2	=	0x0090
                           000090   467 _CAP1	=	0x0090
                           000097   468 _AIN7	=	0x0097
                           000096   469 _AIN6	=	0x0096
                           000095   470 _AIN5	=	0x0095
                           000094   471 _AIN4	=	0x0094
                           000093   472 _AIN3	=	0x0093
                           000092   473 _AIN2	=	0x0092
                           000091   474 _AIN1	=	0x0091
                           000090   475 _AIN0	=	0x0090
                           0000A7   476 _P2_7	=	0x00a7
                           0000A6   477 _P2_6	=	0x00a6
                           0000A5   478 _P2_5	=	0x00a5
                           0000A4   479 _P2_4	=	0x00a4
                           0000A3   480 _P2_3	=	0x00a3
                           0000A2   481 _P2_2	=	0x00a2
                           0000A1   482 _P2_1	=	0x00a1
                           0000A0   483 _P2_0	=	0x00a0
                           0000A7   484 _TXD1	=	0x00a7
                           0000A6   485 _RXD1	=	0x00a6
                           0000A5   486 _T2EX_	=	0x00a5
                           0000A5   487 _CAP2_	=	0x00a5
                           0000A4   488 _T2_	=	0x00a4
                           0000A4   489 _CAP1_	=	0x00a4
                           0000B7   490 _P3_7	=	0x00b7
                           0000B6   491 _P3_6	=	0x00b6
                           0000B5   492 _P3_5	=	0x00b5
                           0000B4   493 _P3_4	=	0x00b4
                           0000B3   494 _P3_3	=	0x00b3
                           0000B2   495 _P3_2	=	0x00b2
                           0000B1   496 _P3_1	=	0x00b1
                           0000B0   497 _P3_0	=	0x00b0
                           0000B7   498 _SCK1	=	0x00b7
                           0000B6   499 _MISO1	=	0x00b6
                           0000B5   500 _MOSI1	=	0x00b5
                           0000B5   501 _T1	=	0x00b5
                           0000B4   502 _T0	=	0x00b4
                           0000B3   503 _INT1	=	0x00b3
                           0000B2   504 _INT0	=	0x00b2
                           0000B1   505 _TXD	=	0x00b1
                           0000B0   506 _RXD	=	0x00b0
                           0000C6   507 _P4_6	=	0x00c6
                           0000C5   508 _P4_5	=	0x00c5
                           0000C4   509 _P4_4	=	0x00c4
                           0000C3   510 _P4_3	=	0x00c3
                           0000C2   511 _P4_2	=	0x00c2
                           0000C1   512 _P4_1	=	0x00c1
                           0000C0   513 _P4_0	=	0x00c0
                           00008F   514 _TF1	=	0x008f
                           00008E   515 _TR1	=	0x008e
                           00008D   516 _TF0	=	0x008d
                           00008C   517 _TR0	=	0x008c
                           00008B   518 _IE1	=	0x008b
                           00008A   519 _IT1	=	0x008a
                           000089   520 _IE0	=	0x0089
                           000088   521 _IT0	=	0x0088
                           00009F   522 _SM0	=	0x009f
                           00009E   523 _SM1	=	0x009e
                           00009D   524 _SM2	=	0x009d
                           00009C   525 _REN	=	0x009c
                           00009B   526 _TB8	=	0x009b
                           00009A   527 _RB8	=	0x009a
                           000099   528 _TI	=	0x0099
                           000098   529 _RI	=	0x0098
                           0000CF   530 _TF2	=	0x00cf
                           0000CF   531 _CAP1F	=	0x00cf
                           0000CE   532 _EXF2	=	0x00ce
                           0000CD   533 _RCLK	=	0x00cd
                           0000CC   534 _TCLK	=	0x00cc
                           0000CB   535 _EXEN2	=	0x00cb
                           0000CA   536 _TR2	=	0x00ca
                           0000C9   537 _C_T2	=	0x00c9
                           0000C8   538 _CP_RL2	=	0x00c8
                           0000FF   539 _S0_FST_ACT	=	0x00ff
                           0000FE   540 _S0_IF_OV	=	0x00fe
                           0000FD   541 _S0_IF_FIRST	=	0x00fd
                           0000FC   542 _S0_IF_BYTE	=	0x00fc
                           0000FB   543 _S0_FREE	=	0x00fb
                           0000FA   544 _S0_T_FIFO	=	0x00fa
                           0000F8   545 _S0_R_FIFO	=	0x00f8
                           0000F7   546 _ADC_START	=	0x00f7
                                    547 ;--------------------------------------------------------
                                    548 ; overlayable register banks
                                    549 ;--------------------------------------------------------
                                    550 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        551 	.ds 8
                                    552 ;--------------------------------------------------------
                                    553 ; internal ram data
                                    554 ;--------------------------------------------------------
                                    555 	.area DSEG    (DATA)
      000019                        556 _matrix_task_sloc0_1_0:
      000019                        557 	.ds 1
                                    558 ;--------------------------------------------------------
                                    559 ; overlayable items in internal ram
                                    560 ;--------------------------------------------------------
                                    561 	.area	OSEG    (OVR,DATA)
                                    562 ;--------------------------------------------------------
                                    563 ; indirectly addressable internal ram data
                                    564 ;--------------------------------------------------------
                                    565 	.area ISEG    (DATA)
                                    566 ;--------------------------------------------------------
                                    567 ; absolute internal ram data
                                    568 ;--------------------------------------------------------
                                    569 	.area IABS    (ABS,DATA)
                                    570 	.area IABS    (ABS,DATA)
                                    571 ;--------------------------------------------------------
                                    572 ; bit data
                                    573 ;--------------------------------------------------------
                                    574 	.area BSEG    (BIT)
                                    575 ;--------------------------------------------------------
                                    576 ; paged external ram data
                                    577 ;--------------------------------------------------------
                                    578 	.area PSEG    (PAG,XDATA)
                                    579 ;--------------------------------------------------------
                                    580 ; uninitialized external ram data
                                    581 ;--------------------------------------------------------
                                    582 	.area XSEG    (XDATA)
      000959                        583 _switch_events_PARM_2:
      000959                        584 	.ds 1
      00095A                        585 _switch_events_PARM_3:
      00095A                        586 	.ds 1
      00095B                        587 _switch_events_row_10000_483:
      00095B                        588 	.ds 1
      00095C                        589 _generate_tick_event_last_tick_10000_486:
      00095C                        590 	.ds 2
      00095E                        591 _matrix_task_last_tick_60000_515:
      00095E                        592 	.ds 2
      000960                        593 _matrix_task_dummy_event_70000_516:
      000960                        594 	.ds 6
      000966                        595 _matrix_task_matrix_previous_10001_493:
      000966                        596 	.ds 16
      000976                        597 _matrix_task_matrix_changed_10002_494:
      000976                        598 	.ds 1
      000977                        599 _matrix_task_last_tick_60002_519:
      000977                        600 	.ds 2
      000979                        601 _matrix_task_dummy_event_70002_520:
      000979                        602 	.ds 6
      00097F                        603 _matrix_task_col_mask_30004_506:
      00097F                        604 	.ds 1
      000980                        605 _matrix_task_dummy_event_90004_512:
      000980                        606 	.ds 6
                                    607 ;--------------------------------------------------------
                                    608 ; absolute external ram data
                                    609 ;--------------------------------------------------------
                                    610 	.area XABS    (ABS,XDATA)
                                    611 ;--------------------------------------------------------
                                    612 ; initialized external ram data
                                    613 ;--------------------------------------------------------
                                    614 	.area XISEG   (XDATA)
      000BEA                        615 _last_input_modification_time:
      000BEA                        616 	.ds 4
      000BEE                        617 _last_matrix_modification_time:
      000BEE                        618 	.ds 4
      000BF2                        619 _last_encoder_modification_time:
      000BF2                        620 	.ds 4
      000BF6                        621 _last_pointing_device_modification_time:
      000BF6                        622 	.ds 4
                                    623 	.area HOME    (CODE)
                                    624 	.area GSINIT0 (CODE)
                                    625 	.area GSINIT1 (CODE)
                                    626 	.area GSINIT2 (CODE)
                                    627 	.area GSINIT3 (CODE)
                                    628 	.area GSINIT4 (CODE)
                                    629 	.area GSINIT5 (CODE)
                                    630 	.area GSINIT  (CODE)
                                    631 	.area GSFINAL (CODE)
                                    632 	.area CSEG    (CODE)
                                    633 ;--------------------------------------------------------
                                    634 ; global & static initialisations
                                    635 ;--------------------------------------------------------
                                    636 	.area HOME    (CODE)
                                    637 	.area GSINIT  (CODE)
                                    638 	.area GSFINAL (CODE)
                                    639 	.area GSINIT  (CODE)
                                    640 ;------------------------------------------------------------
                                    641 ;Allocation info for local variables in function 'generate_tick_event'
                                    642 ;------------------------------------------------------------
                                    643 ;last_tick     Allocated with name '_generate_tick_event_last_tick_10000_486'
                                    644 ;now           Allocated with name '_generate_tick_event_now_10000_486'
                                    645 ;dummy_event   Allocated with name '_generate_tick_event_dummy_event_30000_488'
                                    646 ;------------------------------------------------------------
                                    647 ;	quantum/keyboard.c:539: static uint16_t last_tick = 0;
      003108 90 09 5C         [24]  648 	mov	dptr,#_generate_tick_event_last_tick_10000_486
      00310B E4               [12]  649 	clr	a
      00310C F0               [24]  650 	movx	@dptr,a
      00310D A3               [24]  651 	inc	dptr
      00310E F0               [24]  652 	movx	@dptr,a
                                    653 ;------------------------------------------------------------
                                    654 ;Allocation info for local variables in function 'matrix_task'
                                    655 ;------------------------------------------------------------
                                    656 ;sloc0         Allocated with name '_matrix_task_sloc0_1_0'
                                    657 ;last_tick     Allocated with name '_matrix_task_last_tick_60000_515'
                                    658 ;now           Allocated with name '_matrix_task_now_60000_515'
                                    659 ;dummy_event   Allocated with name '_matrix_task_dummy_event_70000_516'
                                    660 ;matrix_previous Allocated with name '_matrix_task_matrix_previous_10001_493'
                                    661 ;matrix_changed Allocated with name '_matrix_task_matrix_changed_10002_494'
                                    662 ;row           Allocated with name '_matrix_task_row_20002_495'
                                    663 ;last_tick     Allocated with name '_matrix_task_last_tick_60002_519'
                                    664 ;now           Allocated with name '_matrix_task_now_60002_519'
                                    665 ;dummy_event   Allocated with name '_matrix_task_dummy_event_70002_520'
                                    666 ;process_keypress Allocated with name '_matrix_task_process_keypress_10003_501'
                                    667 ;row           Allocated with name '_matrix_task_row_20003_502'
                                    668 ;__400030088   Allocated with name '_matrix_task___400030088_40003_503'
                                    669 ;current_row   Allocated with name '_matrix_task_current_row_30003_503'
                                    670 ;row_changes   Allocated with name '_matrix_task_row_changes_30003_503'
                                    671 ;__500030089   Allocated with name '_matrix_task___500030089_50003_521'
                                    672 ;__500030090   Allocated with name '_matrix_task___500030090_50003_521'
                                    673 ;row           Allocated with name '_matrix_task_row_60003_522'
                                    674 ;rowdata       Allocated with name '_matrix_task_rowdata_60003_522'
                                    675 ;col_mask      Allocated with name '_matrix_task_col_mask_30004_506'
                                    676 ;col           Allocated with name '_matrix_task_col_40004_507'
                                    677 ;key_pressed   Allocated with name '_matrix_task_key_pressed_70004_510'
                                    678 ;dummy_event   Allocated with name '_matrix_task_dummy_event_90004_512'
                                    679 ;------------------------------------------------------------
                                    680 ;	quantum/keyboard.c:539: static uint16_t last_tick = 0;
      00310F 90 09 5E         [24]  681 	mov	dptr,#_matrix_task_last_tick_60000_515
      003112 E4               [12]  682 	clr	a
      003113 F0               [24]  683 	movx	@dptr,a
      003114 A3               [24]  684 	inc	dptr
      003115 F0               [24]  685 	movx	@dptr,a
      003116 90 09 77         [24]  686 	mov	dptr,#_matrix_task_last_tick_60002_519
      003119 F0               [24]  687 	movx	@dptr,a
      00311A A3               [24]  688 	inc	dptr
      00311B F0               [24]  689 	movx	@dptr,a
                                    690 ;--------------------------------------------------------
                                    691 ; Home
                                    692 ;--------------------------------------------------------
                                    693 	.area HOME    (CODE)
                                    694 	.area HOME    (CODE)
                                    695 ;--------------------------------------------------------
                                    696 ; code
                                    697 ;--------------------------------------------------------
                                    698 	.area CSEG    (CODE)
                                    699 ;------------------------------------------------------------
                                    700 ;Allocation info for local variables in function 'IS_KEYEVENT'
                                    701 ;------------------------------------------------------------
                                    702 ;event         Allocated with name '_IS_KEYEVENT_PARM_1'
                                    703 ;------------------------------------------------------------
                                    704 ;	quantum/keyboard.c:31: bool IS_KEYEVENT(const keyevent_t event) {
                                    705 ;	-----------------------------------------
                           000007   706 	ar7 = 0x07
                           000006   707 	ar6 = 0x06
                           000005   708 	ar5 = 0x05
                           000004   709 	ar4 = 0x04
                           000003   710 	ar3 = 0x03
                           000002   711 	ar2 = 0x02
                           000001   712 	ar1 = 0x01
                           000000   713 	ar0 = 0x00
                                    714 ;	 function last_matrix_activity_trigger
                                    715 ;	-----------------------------------------
      008AE9                        716 _last_matrix_activity_trigger:
                                    717 ;	quantum/keyboard.c:185: last_matrix_modification_time = last_input_modification_time = sync_timer_read32();
      008AE9 12 40 3C         [24]  718 	lcall	_timer_read32
      008AEC AC 82            [24]  719 	mov	r4, dpl
      008AEE AD 83            [24]  720 	mov	r5, dph
      008AF0 AE F0            [24]  721 	mov	r6, b
      008AF2 FF               [12]  722 	mov	r7, a
      008AF3 90 0B EA         [24]  723 	mov	dptr,#_last_input_modification_time
      008AF6 12 87 E8         [24]  724 	lcall	_ak820_outline_0008
      008AF9 90 0B EE         [24]  725 	mov	dptr,#_last_matrix_modification_time
      008AFC 12 87 E8         [24]  726 	lcall	_ak820_outline_0008
                                    727 ;	quantum/keyboard.c:186: }
      008AFF 22               [24]  728 	ret
                                    729 ;------------------------------------------------------------
                                    730 ;Allocation info for local variables in function 'last_encoder_activity_time'
                                    731 ;------------------------------------------------------------
                                    732 ;	quantum/keyboard.c:189: uint32_t        last_encoder_activity_time(void) {
                                    733 ;	-----------------------------------------
                                    734 ;	 function last_encoder_activity_trigger
                                    735 ;	-----------------------------------------
      008B00                        736 _last_encoder_activity_trigger:
                                    737 ;	quantum/keyboard.c:196: last_encoder_modification_time = last_input_modification_time = sync_timer_read32();
      008B00 12 40 3C         [24]  738 	lcall	_timer_read32
      008B03 AC 82            [24]  739 	mov	r4, dpl
      008B05 AD 83            [24]  740 	mov	r5, dph
      008B07 AE F0            [24]  741 	mov	r6, b
      008B09 FF               [12]  742 	mov	r7, a
      008B0A 90 0B EA         [24]  743 	mov	dptr,#_last_input_modification_time
      008B0D 12 87 E8         [24]  744 	lcall	_ak820_outline_0008
      008B10 90 0B F2         [24]  745 	mov	dptr,#_last_encoder_modification_time
      008B13 12 87 E8         [24]  746 	lcall	_ak820_outline_0008
                                    747 ;	quantum/keyboard.c:197: }
      008B16 22               [24]  748 	ret
                                    749 ;------------------------------------------------------------
                                    750 ;Allocation info for local variables in function 'last_pointing_device_activity_time'
                                    751 ;------------------------------------------------------------
                                    752 ;	quantum/keyboard.c:200: uint32_t        last_pointing_device_activity_time(void) {
                                    753 ;	-----------------------------------------
                                    754 ;	 function keyboard_post_init_kb
                                    755 ;	-----------------------------------------
      008B17                        756 _keyboard_post_init_kb:
                                    757 ;	quantum/keyboard.c:340: keyboard_post_init_user();
                                    758 ;	quantum/keyboard.c:341: }
      008B17 02 90 12         [24]  759 	ljmp	_keyboard_post_init_user
                                    760 ;------------------------------------------------------------
                                    761 ;Allocation info for local variables in function 'matrix_can_read'
                                    762 ;------------------------------------------------------------
                                    763 ;	quantum/keyboard.c:347: __attribute__((weak)) bool matrix_can_read(void) {
                                    764 ;	-----------------------------------------
                                    765 ;	 function matrix_can_read
                                    766 ;	-----------------------------------------
      008B1A                        767 _matrix_can_read:
                                    768 ;	quantum/keyboard.c:348: return true;
      008B1A 75 82 01         [24]  769 	mov	dpl, #0x01
                                    770 ;	quantum/keyboard.c:349: }
      008B1D 22               [24]  771 	ret
                                    772 ;------------------------------------------------------------
                                    773 ;Allocation info for local variables in function 'keyboard_setup'
                                    774 ;------------------------------------------------------------
                                    775 ;	quantum/keyboard.c:355: void keyboard_setup(void) {
                                    776 ;	-----------------------------------------
                                    777 ;	 function keyboard_setup
                                    778 ;	-----------------------------------------
      008B1E                        779 _keyboard_setup:
                                    780 ;	quantum/keyboard.c:356: print_set_sendchar(sendchar);
      008B1E 90 91 89         [24]  781 	mov	dptr,#_sendchar
      008B21 12 91 57         [24]  782 	lcall	_print_set_sendchar
                                    783 ;	quantum/keyboard.c:358: eeprom_driver_init();
      008B24 12 3A B7         [24]  784 	lcall	_eeprom_driver_init
                                    785 ;	quantum/keyboard.c:361: vial_init();
                                    786 ;	quantum/keyboard.c:367: keyboard_pre_init_kb();
                                    787 ;	quantum/keyboard.c:368: }
      008B27 02 A8 BA         [24]  788 	ljmp	_vial_init
                                    789 ;------------------------------------------------------------
                                    790 ;Allocation info for local variables in function 'is_keyboard_master'
                                    791 ;------------------------------------------------------------
                                    792 ;	quantum/keyboard.c:376: __attribute__((weak)) bool is_keyboard_master(void) {
                                    793 ;	-----------------------------------------
                                    794 ;	 function is_keyboard_master
                                    795 ;	-----------------------------------------
      008B2A                        796 _is_keyboard_master:
                                    797 ;	quantum/keyboard.c:377: return true;
      008B2A 75 82 01         [24]  798 	mov	dpl, #0x01
                                    799 ;	quantum/keyboard.c:378: }
      008B2D 22               [24]  800 	ret
                                    801 ;------------------------------------------------------------
                                    802 ;Allocation info for local variables in function 'is_keyboard_left'
                                    803 ;------------------------------------------------------------
                                    804 ;	quantum/keyboard.c:384: __attribute__((weak)) bool is_keyboard_left(void) {
                                    805 ;	-----------------------------------------
                                    806 ;	 function should_process_keypress
                                    807 ;	-----------------------------------------
      008B2E                        808 _should_process_keypress:
                                    809 ;	quantum/keyboard.c:396: return is_keyboard_master();
                                    810 ;	quantum/keyboard.c:397: }
      008B2E 02 8B 2A         [24]  811 	ljmp	_is_keyboard_master
                                    812 ;------------------------------------------------------------
                                    813 ;Allocation info for local variables in function 'housekeeping_task_kb'
                                    814 ;------------------------------------------------------------
                                    815 ;	quantum/keyboard.c:404: __attribute__((weak)) void housekeeping_task_kb(void) {}
                                    816 ;	-----------------------------------------
                                    817 ;	 function housekeeping_task
                                    818 ;	-----------------------------------------
      008B31                        819 _housekeeping_task:
                                    820 ;	quantum/keyboard.c:419: housekeeping_task_user();
                                    821 ;	quantum/keyboard.c:420: }
      008B31 22               [24]  822 	ret
                                    823 ;------------------------------------------------------------
                                    824 ;Allocation info for local variables in function 'quantum_init'
                                    825 ;------------------------------------------------------------
                                    826 ;	quantum/keyboard.c:426: void quantum_init(void) {
                                    827 ;	-----------------------------------------
                                    828 ;	 function quantum_init
                                    829 ;	-----------------------------------------
      008B32                        830 _quantum_init:
                                    831 ;	quantum/keyboard.c:427: magic();
      008B32 12 79 0A         [24]  832 	lcall	_magic
                                    833 ;	quantum/keyboard.c:428: led_init_ports();
      008B35 12 90 F4         [24]  834 	lcall	_led_init_ports
                                    835 ;	quantum/keyboard.c:439: rgb_matrix_init();
                                    836 ;	quantum/keyboard.c:447: }
      008B38 02 49 7E         [24]  837 	ljmp	_rgb_matrix_init
                                    838 ;------------------------------------------------------------
                                    839 ;Allocation info for local variables in function 'keyboard_init'
                                    840 ;------------------------------------------------------------
                                    841 ;	quantum/keyboard.c:453: void keyboard_init(void) {
                                    842 ;	-----------------------------------------
                                    843 ;	 function keyboard_init
                                    844 ;	-----------------------------------------
      008B3B                        845 _keyboard_init:
                                    846 ;	quantum/keyboard.c:454: timer_init();
      008B3B 12 3F FE         [24]  847 	lcall	_timer_init
                                    848 ;	quantum/keyboard.c:457: via_init();
      008B3E 12 A0 DD         [24]  849 	lcall	_via_init
                                    850 ;	quantum/keyboard.c:463: encoder_init();
      008B41 12 88 13         [24]  851 	lcall	_encoder_init
                                    852 ;	quantum/keyboard.c:465: matrix_init();
      008B44 12 53 A9         [24]  853 	lcall	_matrix_init
                                    854 ;	quantum/keyboard.c:466: quantum_init();
      008B47 12 8B 32         [24]  855 	lcall	_quantum_init
                                    856 ;	quantum/keyboard.c:516: keyboard_post_init_kb(); /* Always keep this last */
                                    857 ;	quantum/keyboard.c:517: }
      008B4A 02 8B 17         [24]  858 	ljmp	_keyboard_post_init_kb
                                    859 ;------------------------------------------------------------
                                    860 ;Allocation info for local variables in function 'switch_events'
                                    861 ;------------------------------------------------------------
                                    862 ;col           Allocated with name '_switch_events_PARM_2'
                                    863 ;pressed       Allocated with name '_switch_events_PARM_3'
                                    864 ;row           Allocated with name '_switch_events_row_10000_483'
                                    865 ;------------------------------------------------------------
                                    866 ;	quantum/keyboard.c:524: void switch_events(uint8_t row, uint8_t col, bool pressed) {
                                    867 ;	-----------------------------------------
                                    868 ;	 function switch_events
                                    869 ;	-----------------------------------------
      008B4D                        870 _switch_events:
      008B4D E5 82            [12]  871 	mov	a,dpl
      008B4F 90 09 5B         [24]  872 	mov	dptr,#_switch_events_row_10000_483
      008B52 F0               [24]  873 	movx	@dptr,a
                                    874 ;	quantum/keyboard.c:529: process_rgb_matrix(row, col, pressed);
      008B53 E0               [24]  875 	movx	a,@dptr
      008B54 FF               [12]  876 	mov	r7,a
      008B55 90 09 59         [24]  877 	mov	dptr,#_switch_events_PARM_2
      008B58 E0               [24]  878 	movx	a,@dptr
      008B59 FE               [12]  879 	mov	r6,a
      008B5A 90 09 5A         [24]  880 	mov	dptr,#_switch_events_PARM_3
      008B5D E0               [24]  881 	movx	a,@dptr
      008B5E FD               [12]  882 	mov	r5,a
      008B5F 90 06 4C         [24]  883 	mov	dptr,#_process_rgb_matrix_PARM_2
      008B62 EE               [12]  884 	mov	a,r6
      008B63 F0               [24]  885 	movx	@dptr,a
      008B64 90 06 4D         [24]  886 	mov	dptr,#_process_rgb_matrix_PARM_3
      008B67 ED               [12]  887 	mov	a,r5
      008B68 F0               [24]  888 	movx	@dptr,a
      008B69 8F 82            [24]  889 	mov	dpl, r7
                                    890 ;	quantum/keyboard.c:531: }
      008B6B 02 4D FA         [24]  891 	ljmp	_process_rgb_matrix
                                    892 ;------------------------------------------------------------
                                    893 ;Allocation info for local variables in function 'generate_tick_event'
                                    894 ;------------------------------------------------------------
                                    895 ;last_tick     Allocated with name '_generate_tick_event_last_tick_10000_486'
                                    896 ;now           Allocated with name '_generate_tick_event_now_10000_486'
                                    897 ;dummy_event   Allocated with name '_generate_tick_event_dummy_event_30000_488'
                                    898 ;------------------------------------------------------------
                                    899 ;	quantum/keyboard.c:537: static inline void generate_tick_event(void) {
                                    900 ;	-----------------------------------------
                                    901 ;	 function matrix_task
                                    902 ;	-----------------------------------------
      008B6E                        903 _matrix_task:
                                    904 ;	quantum/keyboard.c:557: if (!matrix_can_read()) {
      008B6E 12 8B 1A         [24]  905 	lcall	_matrix_can_read
      008B71 E5 82            [12]  906 	mov	a, dpl
      008B73 70 5E            [24]  907 	jnz	00102$
                                    908 ;	quantum/keyboard.c:540: const uint16_t  now       = timer_read();
      008B75 12 40 6D         [24]  909 	lcall	_timer_read
      008B78 AE 82            [24]  910 	mov	r6, dpl
      008B7A AF 83            [24]  911 	mov	r7, dph
                                    912 ;	quantum/keyboard.c:541: if (TIMER_DIFF_16(now, last_tick) != 0) {
      008B7C 90 09 5E         [24]  913 	mov	dptr,#_matrix_task_last_tick_60000_515
      008B7F E0               [24]  914 	movx	a,@dptr
      008B80 FC               [12]  915 	mov	r4,a
      008B81 A3               [24]  916 	inc	dptr
      008B82 E0               [24]  917 	movx	a,@dptr
      008B83 FD               [12]  918 	mov	r5,a
      008B84 EE               [12]  919 	mov	a,r6
      008B85 C3               [12]  920 	clr	c
      008B86 9C               [12]  921 	subb	a,r4
      008B87 FC               [12]  922 	mov	r4,a
      008B88 EF               [12]  923 	mov	a,r7
      008B89 9D               [12]  924 	subb	a,r5
      008B8A 4C               [12]  925 	orl	a,r4
      008B8B 60 42            [24]  926 	jz	00120$
                                    927 ;	quantum/keyboard.c:543: MAKE_TICK_EVENT;
      008B8D 90 09 60         [24]  928 	mov	dptr,#_matrix_task_dummy_event_70000_516
      008B90 E4               [12]  929 	clr	a
      008B91 F0               [24]  930 	movx	@dptr,a
      008B92 90 09 61         [24]  931 	mov	dptr,#(_matrix_task_dummy_event_70000_516 + 0x0001)
      008B95 F0               [24]  932 	movx	@dptr,a
      008B96 12 40 6D         [24]  933 	lcall	_timer_read
      008B99 AC 82            [24]  934 	mov	r4, dpl
      008B9B AD 83            [24]  935 	mov	r5, dph
      008B9D 90 09 62         [24]  936 	mov	dptr,#(_matrix_task_dummy_event_70000_516 + 0x0002)
      008BA0 EC               [12]  937 	mov	a,r4
      008BA1 F0               [24]  938 	movx	@dptr,a
      008BA2 ED               [12]  939 	mov	a,r5
      008BA3 A3               [24]  940 	inc	dptr
      008BA4 F0               [24]  941 	movx	@dptr,a
      008BA5 90 09 64         [24]  942 	mov	dptr,#(_matrix_task_dummy_event_70000_516 + 0x0004)
      008BA8 E4               [12]  943 	clr	a
      008BA9 F0               [24]  944 	movx	@dptr,a
      008BAA 90 09 65         [24]  945 	mov	dptr,#(_matrix_task_dummy_event_70000_516 + 0x0005)
      008BAD F0               [24]  946 	movx	@dptr,a
                                    947 ;	quantum/keyboard.c:544: action_exec(dummy_event);
      008BAE 90 0B 90         [24]  948 	mov	dptr,#___memcpy_PARM_2
      008BB1 74 60            [12]  949 	mov	a,#_matrix_task_dummy_event_70000_516
      008BB3 F0               [24]  950 	movx	@dptr,a
      008BB4 74 09            [12]  951 	mov	a,#(_matrix_task_dummy_event_70000_516 >> 8)
      008BB6 12 8D 89         [24]  952 	lcall	_ak820_outline_0014
      008BB9 C0 07            [24]  953 	push	ar7
      008BBB C0 06            [24]  954 	push	ar6
      008BBD 12 B4 C1         [24]  955 	lcall	___memcpy
      008BC0 12 6D 00         [24]  956 	lcall	_action_exec
      008BC3 D0 06            [24]  957 	pop	ar6
      008BC5 D0 07            [24]  958 	pop	ar7
                                    959 ;	quantum/keyboard.c:545: last_tick = now;
      008BC7 90 09 5E         [24]  960 	mov	dptr,#_matrix_task_last_tick_60000_515
      008BCA EE               [12]  961 	mov	a,r6
      008BCB F0               [24]  962 	movx	@dptr,a
      008BCC EF               [12]  963 	mov	a,r7
      008BCD A3               [24]  964 	inc	dptr
      008BCE F0               [24]  965 	movx	@dptr,a
                                    966 ;	quantum/keyboard.c:558: generate_tick_event();
      008BCF                        967 00120$:
                                    968 ;	quantum/keyboard.c:559: return false;
      008BCF 75 82 00         [24]  969 	mov	dpl, #0x00
      008BD2 22               [24]  970 	ret
      008BD3                        971 00102$:
                                    972 ;	quantum/keyboard.c:564: matrix_scan();
      008BD3 12 53 D2         [24]  973 	lcall	_matrix_scan
                                    974 ;	quantum/keyboard.c:568: vial_unlock_task();
      008BD6 12 A8 02         [24]  975 	lcall	_vial_unlock_task
                                    976 ;	quantum/keyboard.c:570: bool matrix_changed = false;
      008BD9 90 09 76         [24]  977 	mov	dptr,#_matrix_task_matrix_changed_10002_494
      008BDC E4               [12]  978 	clr	a
      008BDD F0               [24]  979 	movx	@dptr,a
                                    980 ;	quantum/keyboard.c:571: for (uint8_t row = 0; row < MATRIX_ROWS && !matrix_changed; row++) {
      008BDE FF               [12]  981 	mov	r7,a
      008BDF                        982 00127$:
      008BDF BF 10 00         [24]  983 	cjne	r7,#0x10,00247$
      008BE2                        984 00247$:
      008BE2 50 25            [24]  985 	jnc	00103$
      008BE4 90 09 76         [24]  986 	mov	dptr,#_matrix_task_matrix_changed_10002_494
      008BE7 E0               [24]  987 	movx	a,@dptr
      008BE8 70 1F            [24]  988 	jnz	00103$
                                    989 ;	quantum/keyboard.c:572: matrix_changed |= matrix_previous[row] ^ matrix_get_row(row);
      008BEA EF               [12]  990 	mov	a,r7
      008BEB 24 66            [12]  991 	add	a, #_matrix_task_matrix_previous_10001_493
      008BED F5 82            [12]  992 	mov	dpl,a
      008BEF E4               [12]  993 	clr	a
      008BF0 34 09            [12]  994 	addc	a, #(_matrix_task_matrix_previous_10001_493 >> 8)
      008BF2 F5 83            [12]  995 	mov	dph,a
      008BF4 E0               [24]  996 	movx	a,@dptr
      008BF5 FE               [12]  997 	mov	r6,a
      008BF6 8F 82            [24]  998 	mov	dpl, r7
      008BF8 12 53 5E         [24]  999 	lcall	_matrix_get_row
      008BFB E5 82            [12] 1000 	mov	a,dpl
      008BFD 6E               [12] 1001 	xrl	a,r6
                                   1002 ;	assignBit
      008BFE 90 09 76         [24] 1003 	mov	dptr,#_matrix_task_matrix_changed_10002_494
      008C01 24 FF            [12] 1004 	add	a,#0xff
      008C03 E4               [12] 1005 	clr	a
      008C04 33               [12] 1006 	rlc	a
      008C05 F0               [24] 1007 	movx	@dptr,a
                                   1008 ;	quantum/keyboard.c:571: for (uint8_t row = 0; row < MATRIX_ROWS && !matrix_changed; row++) {
      008C06 0F               [12] 1009 	inc	r7
      008C07 80 D6            [24] 1010 	sjmp	00127$
      008C09                       1011 00103$:
                                   1012 ;	quantum/keyboard.c:578: if (!matrix_changed) {
      008C09 90 09 76         [24] 1013 	mov	dptr,#_matrix_task_matrix_changed_10002_494
      008C0C E0               [24] 1014 	movx	a,@dptr
      008C0D 70 5E            [24] 1015 	jnz	00105$
                                   1016 ;	quantum/keyboard.c:540: const uint16_t  now       = timer_read();
      008C0F 12 40 6D         [24] 1017 	lcall	_timer_read
      008C12 AE 82            [24] 1018 	mov	r6, dpl
      008C14 AF 83            [24] 1019 	mov	r7, dph
                                   1020 ;	quantum/keyboard.c:541: if (TIMER_DIFF_16(now, last_tick) != 0) {
      008C16 90 09 77         [24] 1021 	mov	dptr,#_matrix_task_last_tick_60002_519
      008C19 E0               [24] 1022 	movx	a,@dptr
      008C1A FC               [12] 1023 	mov	r4,a
      008C1B A3               [24] 1024 	inc	dptr
      008C1C E0               [24] 1025 	movx	a,@dptr
      008C1D FD               [12] 1026 	mov	r5,a
      008C1E EE               [12] 1027 	mov	a,r6
      008C1F C3               [12] 1028 	clr	c
      008C20 9C               [12] 1029 	subb	a,r4
      008C21 FC               [12] 1030 	mov	r4,a
      008C22 EF               [12] 1031 	mov	a,r7
      008C23 9D               [12] 1032 	subb	a,r5
      008C24 4C               [12] 1033 	orl	a,r4
      008C25 60 42            [24] 1034 	jz	00123$
                                   1035 ;	quantum/keyboard.c:543: MAKE_TICK_EVENT;
      008C27 90 09 79         [24] 1036 	mov	dptr,#_matrix_task_dummy_event_70002_520
      008C2A E4               [12] 1037 	clr	a
      008C2B F0               [24] 1038 	movx	@dptr,a
      008C2C 90 09 7A         [24] 1039 	mov	dptr,#(_matrix_task_dummy_event_70002_520 + 0x0001)
      008C2F F0               [24] 1040 	movx	@dptr,a
      008C30 12 40 6D         [24] 1041 	lcall	_timer_read
      008C33 AC 82            [24] 1042 	mov	r4, dpl
      008C35 AD 83            [24] 1043 	mov	r5, dph
      008C37 90 09 7B         [24] 1044 	mov	dptr,#(_matrix_task_dummy_event_70002_520 + 0x0002)
      008C3A EC               [12] 1045 	mov	a,r4
      008C3B F0               [24] 1046 	movx	@dptr,a
      008C3C ED               [12] 1047 	mov	a,r5
      008C3D A3               [24] 1048 	inc	dptr
      008C3E F0               [24] 1049 	movx	@dptr,a
      008C3F 90 09 7D         [24] 1050 	mov	dptr,#(_matrix_task_dummy_event_70002_520 + 0x0004)
      008C42 E4               [12] 1051 	clr	a
      008C43 F0               [24] 1052 	movx	@dptr,a
      008C44 90 09 7E         [24] 1053 	mov	dptr,#(_matrix_task_dummy_event_70002_520 + 0x0005)
      008C47 F0               [24] 1054 	movx	@dptr,a
                                   1055 ;	quantum/keyboard.c:544: action_exec(dummy_event);
      008C48 90 0B 90         [24] 1056 	mov	dptr,#___memcpy_PARM_2
      008C4B 74 79            [12] 1057 	mov	a,#_matrix_task_dummy_event_70002_520
      008C4D F0               [24] 1058 	movx	@dptr,a
      008C4E 74 09            [12] 1059 	mov	a,#(_matrix_task_dummy_event_70002_520 >> 8)
      008C50 12 8D 89         [24] 1060 	lcall	_ak820_outline_0014
      008C53 C0 07            [24] 1061 	push	ar7
      008C55 C0 06            [24] 1062 	push	ar6
      008C57 12 B4 C1         [24] 1063 	lcall	___memcpy
      008C5A 12 6D 00         [24] 1064 	lcall	_action_exec
      008C5D D0 06            [24] 1065 	pop	ar6
      008C5F D0 07            [24] 1066 	pop	ar7
                                   1067 ;	quantum/keyboard.c:545: last_tick = now;
      008C61 90 09 77         [24] 1068 	mov	dptr,#_matrix_task_last_tick_60002_519
      008C64 EE               [12] 1069 	mov	a,r6
      008C65 F0               [24] 1070 	movx	@dptr,a
      008C66 EF               [12] 1071 	mov	a,r7
      008C67 A3               [24] 1072 	inc	dptr
      008C68 F0               [24] 1073 	movx	@dptr,a
                                   1074 ;	quantum/keyboard.c:579: generate_tick_event();
      008C69                       1075 00123$:
                                   1076 ;	quantum/keyboard.c:580: return matrix_changed;
      008C69 75 82 00         [24] 1077 	mov	dpl, #0x00
      008C6C 22               [24] 1078 	ret
      008C6D                       1079 00105$:
                                   1080 ;	quantum/keyboard.c:583: if (debug_config.matrix) {
      008C6D 90 0B FE         [24] 1081 	mov	dptr,#_debug_config
      008C70 E0               [24] 1082 	movx	a,@dptr
      008C71 30 E1 03         [24] 1083 	jnb	acc.1,00107$
                                   1084 ;	quantum/keyboard.c:584: matrix_print();
      008C74 12 53 FE         [24] 1085 	lcall	_matrix_print
      008C77                       1086 00107$:
                                   1087 ;	quantum/keyboard.c:587: const bool process_keypress = should_process_keypress();
      008C77 12 8B 2E         [24] 1088 	lcall	_should_process_keypress
      008C7A AF 82            [24] 1089 	mov	r7, dpl
                                   1090 ;	quantum/keyboard.c:589: for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
      008C7C 7E 00            [12] 1091 	mov	r6,#0x00
      008C7E                       1092 00133$:
      008C7E BE 10 00         [24] 1093 	cjne	r6,#0x10,00253$
      008C81                       1094 00253$:
      008C81 40 03            [24] 1095 	jc	00254$
      008C83 02 8D 65         [24] 1096 	ljmp	00117$
      008C86                       1097 00254$:
                                   1098 ;	quantum/keyboard.c:590: const matrix_row_t current_row = matrix_get_row(row);
      008C86 8E 82            [24] 1099 	mov	dpl, r6
      008C88 12 53 5E         [24] 1100 	lcall	_matrix_get_row
      008C8B AD 82            [24] 1101 	mov	r5, dpl
                                   1102 ;	quantum/keyboard.c:591: const matrix_row_t row_changes = current_row ^ matrix_previous[row];
      008C8D EE               [12] 1103 	mov	a,r6
      008C8E 24 66            [12] 1104 	add	a, #_matrix_task_matrix_previous_10001_493
      008C90 F5 82            [12] 1105 	mov	dpl,a
      008C92 E4               [12] 1106 	clr	a
      008C93 34 09            [12] 1107 	addc	a, #(_matrix_task_matrix_previous_10001_493 >> 8)
      008C95 F5 83            [12] 1108 	mov	dph,a
      008C97 E0               [24] 1109 	movx	a,@dptr
      008C98 FC               [12] 1110 	mov	r4,a
      008C99 ED               [12] 1111 	mov	a,r5
      008C9A 62 04            [12] 1112 	xrl	ar4,a
                                   1113 ;	quantum/keyboard.c:593: if (!row_changes || has_ghost_in_row(row, current_row)) {
      008C9C EC               [12] 1114 	mov	a,r4
      008C9D 70 03            [24] 1115 	jnz	00255$
      008C9F 02 8D 61         [24] 1116 	ljmp	00116$
      008CA2                       1117 00255$:
                                   1118 ;	quantum/keyboard.c:597: matrix_row_t col_mask = 1;
      008CA2 90 09 7F         [24] 1119 	mov	dptr,#_matrix_task_col_mask_30004_506
      008CA5 74 01            [12] 1120 	mov	a,#0x01
      008CA7 F0               [24] 1121 	movx	@dptr,a
                                   1122 ;	quantum/keyboard.c:598: for (uint8_t col = 0; col < MATRIX_COLS; col++, col_mask <<= 1) {
      008CA8 8E 19            [24] 1123 	mov	_matrix_task_sloc0_1_0,r6
      008CAA 8E 02            [24] 1124 	mov	ar2,r6
      008CAC 79 00            [12] 1125 	mov	r1,#0x00
      008CAE                       1126 00130$:
      008CAE B9 08 00         [24] 1127 	cjne	r1,#0x08,00256$
      008CB1                       1128 00256$:
      008CB1 40 03            [24] 1129 	jc	00257$
      008CB3 02 8D 55         [24] 1130 	ljmp	00115$
      008CB6                       1131 00257$:
                                   1132 ;	quantum/keyboard.c:599: if (row_changes & col_mask) {
      008CB6 90 09 7F         [24] 1133 	mov	dptr,#_matrix_task_col_mask_30004_506
      008CB9 E0               [24] 1134 	movx	a,@dptr
      008CBA F8               [12] 1135 	mov	r0,a
      008CBB 5C               [12] 1136 	anl	a,r4
      008CBC 70 03            [24] 1137 	jnz	00258$
      008CBE 02 8D 4A         [24] 1138 	ljmp	00131$
      008CC1                       1139 00258$:
                                   1140 ;	quantum/keyboard.c:600: const bool key_pressed = current_row & col_mask;
      008CC1 ED               [12] 1141 	mov	a,r5
      008CC2 52 00            [12] 1142 	anl	ar0,a
                                   1143 ;	assignBit
      008CC4 E8               [12] 1144 	mov	a,r0
      008CC5 24 FF            [12] 1145 	add	a,#0xff
      008CC7 E4               [12] 1146 	clr	a
      008CC8 33               [12] 1147 	rlc	a
      008CC9 F8               [12] 1148 	mov	r0,a
                                   1149 ;	quantum/keyboard.c:602: if (process_keypress) {
      008CCA EF               [12] 1150 	mov	a,r7
      008CCB 60 56            [24] 1151 	jz	00112$
                                   1152 ;	quantum/keyboard.c:604: MAKE_KEYEVENT(row, col, key_pressed);
      008CCD C0 02            [24] 1153 	push	ar2
      008CCF 90 09 80         [24] 1154 	mov	dptr,#_matrix_task_dummy_event_90004_512
      008CD2 E9               [12] 1155 	mov	a,r1
      008CD3 F0               [24] 1156 	movx	@dptr,a
      008CD4 90 09 81         [24] 1157 	mov	dptr,#(_matrix_task_dummy_event_90004_512 + 0x0001)
      008CD7 E5 19            [12] 1158 	mov	a,_matrix_task_sloc0_1_0
      008CD9 F0               [24] 1159 	movx	@dptr,a
      008CDA 12 40 6D         [24] 1160 	lcall	_timer_read
      008CDD AA 82            [24] 1161 	mov	r2, dpl
      008CDF AB 83            [24] 1162 	mov	r3, dph
      008CE1 90 09 82         [24] 1163 	mov	dptr,#(_matrix_task_dummy_event_90004_512 + 0x0002)
      008CE4 EA               [12] 1164 	mov	a,r2
      008CE5 F0               [24] 1165 	movx	@dptr,a
      008CE6 EB               [12] 1166 	mov	a,r3
      008CE7 A3               [24] 1167 	inc	dptr
      008CE8 F0               [24] 1168 	movx	@dptr,a
      008CE9 90 09 84         [24] 1169 	mov	dptr,#(_matrix_task_dummy_event_90004_512 + 0x0004)
      008CEC 74 01            [12] 1170 	mov	a,#0x01
      008CEE F0               [24] 1171 	movx	@dptr,a
      008CEF 90 09 85         [24] 1172 	mov	dptr,#(_matrix_task_dummy_event_90004_512 + 0x0005)
      008CF2 E8               [12] 1173 	mov	a,r0
      008CF3 F0               [24] 1174 	movx	@dptr,a
                                   1175 ;	quantum/keyboard.c:605: action_exec(dummy_event);
      008CF4 90 0B 90         [24] 1176 	mov	dptr,#___memcpy_PARM_2
      008CF7 74 80            [12] 1177 	mov	a,#_matrix_task_dummy_event_90004_512
      008CF9 F0               [24] 1178 	movx	@dptr,a
      008CFA 74 09            [12] 1179 	mov	a,#(_matrix_task_dummy_event_90004_512 >> 8)
      008CFC 12 8D 89         [24] 1180 	lcall	_ak820_outline_0014
      008CFF C0 07            [24] 1181 	push	ar7
      008D01 C0 06            [24] 1182 	push	ar6
      008D03 C0 05            [24] 1183 	push	ar5
      008D05 C0 04            [24] 1184 	push	ar4
      008D07 C0 02            [24] 1185 	push	ar2
      008D09 C0 01            [24] 1186 	push	ar1
      008D0B C0 00            [24] 1187 	push	ar0
      008D0D 12 B4 C1         [24] 1188 	lcall	___memcpy
      008D10 12 6D 00         [24] 1189 	lcall	_action_exec
      008D13 D0 00            [24] 1190 	pop	ar0
      008D15 D0 01            [24] 1191 	pop	ar1
      008D17 D0 02            [24] 1192 	pop	ar2
      008D19 D0 04            [24] 1193 	pop	ar4
      008D1B D0 05            [24] 1194 	pop	ar5
      008D1D D0 06            [24] 1195 	pop	ar6
      008D1F D0 07            [24] 1196 	pop	ar7
                                   1197 ;	quantum/keyboard.c:615: return matrix_changed;
      008D21 D0 02            [24] 1198 	pop	ar2
                                   1199 ;	quantum/keyboard.c:605: action_exec(dummy_event);
      008D23                       1200 00112$:
                                   1201 ;	quantum/keyboard.c:608: switch_events(row, col, key_pressed);
      008D23 90 09 59         [24] 1202 	mov	dptr,#_switch_events_PARM_2
      008D26 E9               [12] 1203 	mov	a,r1
      008D27 F0               [24] 1204 	movx	@dptr,a
      008D28 90 09 5A         [24] 1205 	mov	dptr,#_switch_events_PARM_3
      008D2B E8               [12] 1206 	mov	a,r0
      008D2C F0               [24] 1207 	movx	@dptr,a
      008D2D 8A 82            [24] 1208 	mov	dpl, r2
      008D2F C0 07            [24] 1209 	push	ar7
      008D31 C0 06            [24] 1210 	push	ar6
      008D33 C0 05            [24] 1211 	push	ar5
      008D35 C0 04            [24] 1212 	push	ar4
      008D37 C0 02            [24] 1213 	push	ar2
      008D39 C0 01            [24] 1214 	push	ar1
      008D3B 12 8B 4D         [24] 1215 	lcall	_switch_events
      008D3E D0 01            [24] 1216 	pop	ar1
      008D40 D0 02            [24] 1217 	pop	ar2
      008D42 D0 04            [24] 1218 	pop	ar4
      008D44 D0 05            [24] 1219 	pop	ar5
      008D46 D0 06            [24] 1220 	pop	ar6
      008D48 D0 07            [24] 1221 	pop	ar7
      008D4A                       1222 00131$:
                                   1223 ;	quantum/keyboard.c:598: for (uint8_t col = 0; col < MATRIX_COLS; col++, col_mask <<= 1) {
      008D4A 09               [12] 1224 	inc	r1
      008D4B 90 09 7F         [24] 1225 	mov	dptr,#_matrix_task_col_mask_30004_506
      008D4E E0               [24] 1226 	movx	a,@dptr
      008D4F 25 E0            [12] 1227 	add	a,acc
      008D51 F0               [24] 1228 	movx	@dptr,a
      008D52 02 8C AE         [24] 1229 	ljmp	00130$
      008D55                       1230 00115$:
                                   1231 ;	quantum/keyboard.c:612: matrix_previous[row] = current_row;
      008D55 EE               [12] 1232 	mov	a,r6
      008D56 24 66            [12] 1233 	add	a, #_matrix_task_matrix_previous_10001_493
      008D58 F5 82            [12] 1234 	mov	dpl,a
      008D5A E4               [12] 1235 	clr	a
      008D5B 34 09            [12] 1236 	addc	a, #(_matrix_task_matrix_previous_10001_493 >> 8)
      008D5D F5 83            [12] 1237 	mov	dph,a
      008D5F ED               [12] 1238 	mov	a,r5
      008D60 F0               [24] 1239 	movx	@dptr,a
      008D61                       1240 00116$:
                                   1241 ;	quantum/keyboard.c:589: for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
      008D61 0E               [12] 1242 	inc	r6
      008D62 02 8C 7E         [24] 1243 	ljmp	00133$
      008D65                       1244 00117$:
                                   1245 ;	quantum/keyboard.c:615: return matrix_changed;
      008D65 75 82 01         [24] 1246 	mov	dpl, #0x01
                                   1247 ;	quantum/keyboard.c:616: }
      008D68 22               [24] 1248 	ret
                                   1249 ;------------------------------------------------------------
                                   1250 ;Allocation info for local variables in function 'quantum_task'
                                   1251 ;------------------------------------------------------------
                                   1252 ;	quantum/keyboard.c:622: void quantum_task(void) {
                                   1253 ;	-----------------------------------------
                                   1254 ;	 function quantum_task
                                   1255 ;	-----------------------------------------
      008D69                       1256 _quantum_task:
                                   1257 ;	quantum/keyboard.c:689: caps_word_task();
                                   1258 ;	quantum/keyboard.c:695: }
      008D69 02 2E C2         [24] 1259 	ljmp	_caps_word_task
                                   1260 ;------------------------------------------------------------
                                   1261 ;Allocation info for local variables in function 'keyboard_task'
                                   1262 ;------------------------------------------------------------
                                   1263 ;activity_has_occurred Allocated with name '_keyboard_task_activity_has_occurred_10000_527'
                                   1264 ;------------------------------------------------------------
                                   1265 ;	quantum/keyboard.c:698: void keyboard_task(void) {
                                   1266 ;	-----------------------------------------
                                   1267 ;	 function keyboard_task
                                   1268 ;	-----------------------------------------
      008D6C                       1269 _keyboard_task:
                                   1270 ;	quantum/keyboard.c:700: if (matrix_task()) {
      008D6C 12 8B 6E         [24] 1271 	lcall	_matrix_task
      008D6F E5 82            [12] 1272 	mov	a, dpl
      008D71 60 03            [24] 1273 	jz	00102$
                                   1274 ;	quantum/keyboard.c:701: last_matrix_activity_trigger();
      008D73 12 8A E9         [24] 1275 	lcall	_last_matrix_activity_trigger
                                   1276 ;	quantum/keyboard.c:702: activity_has_occurred = true;
      008D76                       1277 00102$:
                                   1278 ;	quantum/keyboard.c:705: quantum_task();
      008D76 12 8D 69         [24] 1279 	lcall	_quantum_task
                                   1280 ;	quantum/keyboard.c:719: rgb_matrix_task();
      008D79 12 4A F4         [24] 1281 	lcall	_rgb_matrix_task
                                   1282 ;	quantum/keyboard.c:729: if (encoder_read()) {
      008D7C 12 8A 48         [24] 1283 	lcall	_encoder_read
      008D7F E5 82            [12] 1284 	mov	a, dpl
      008D81 60 03            [24] 1285 	jz	00104$
                                   1286 ;	quantum/keyboard.c:730: last_encoder_activity_trigger();
      008D83 12 8B 00         [24] 1287 	lcall	_last_encoder_activity_trigger
                                   1288 ;	quantum/keyboard.c:731: activity_has_occurred = true;
      008D86                       1289 00104$:
                                   1290 ;	quantum/keyboard.c:785: led_task();
                                   1291 ;	quantum/keyboard.c:786: }
      008D86 02 91 16         [24] 1292 	ljmp	_led_task
                                   1293 	.area CSEG    (CODE)
                                   1294 	.area CONST   (CODE)
                                   1295 	.area XINIT   (CODE)
      00BDCA                       1296 __xinit__last_input_modification_time:
      00BDCA 00 00 00 00           1297 	.byte #0x00, #0x00, #0x00, #0x00	; 0
      00BDCE                       1298 __xinit__last_matrix_modification_time:
      00BDCE 00 00 00 00           1299 	.byte #0x00, #0x00, #0x00, #0x00	; 0
      00BDD2                       1300 __xinit__last_encoder_modification_time:
      00BDD2 00 00 00 00           1301 	.byte #0x00, #0x00, #0x00, #0x00	; 0
      00BDD6                       1302 __xinit__last_pointing_device_modification_time:
      00BDD6 00 00 00 00           1303 	.byte #0x00, #0x00, #0x00, #0x00	; 0
                                   1304 	.area CABS    (ABS,CODE)
                                   1305 
                                   1306 ; Experimental exact instruction outlining.
                                   1307 	.globl _ak820_outline_0008
                                   1308 	.globl _ak820_outline_0014
                                   1309 
                                   1310 	.area CSEG (CODE)
                                   1311 ; function ak820_outline_0014
      008D89                       1312 _ak820_outline_0014:
      008D89 A3               [24] 1313 	inc	dptr
      008D8A F0               [24] 1314 	movx	@dptr,a
      008D8B E4               [12] 1315 	clr	a
      008D8C A3               [24] 1316 	inc	dptr
      008D8D F0               [24] 1317 	movx	@dptr,a
      008D8E 90 0B 93         [24] 1318 	mov	dptr,#___memcpy_PARM_3
      008D91 74 06            [12] 1319 	mov	a,#0x06
      008D93 F0               [24] 1320 	movx	@dptr,a
      008D94 E4               [12] 1321 	clr	a
      008D95 A3               [24] 1322 	inc	dptr
      008D96 F0               [24] 1323 	movx	@dptr,a
      008D97 90 07 3C         [24] 1324 	mov	dptr,#_action_exec_PARM_1
      008D9A F5 F0            [12] 1325 	mov	b,a
      008D9C 22               [24] 1326 	ret
