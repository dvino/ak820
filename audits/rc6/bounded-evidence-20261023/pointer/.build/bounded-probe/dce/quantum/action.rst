                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module action
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _pre_process_record_quantum
                                     12 	.globl _clear_weak_mods
                                     13 	.globl _del_weak_mods
                                     14 	.globl _add_weak_mods
                                     15 	.globl _clear_mods
                                     16 	.globl _del_mods
                                     17 	.globl _add_mods
                                     18 	.globl _send_keyboard_report
                                     19 	.globl _layer_switch_get_action
                                     20 	.globl _store_or_get_action
                                     21 	.globl _layer_xor
                                     22 	.globl _layer_and
                                     23 	.globl _layer_or
                                     24 	.globl _layer_off
                                     25 	.globl _layer_on
                                     26 	.globl _layer_move
                                     27 	.globl _layer_clear
                                     28 	.globl _layer_state_set
                                     29 	.globl _default_layer_xor
                                     30 	.globl _default_layer_and
                                     31 	.globl _default_layer_or
                                     32 	.globl _default_layer_set
                                     33 	.globl _post_process_record_quantum
                                     34 	.globl _process_record_quantum
                                     35 	.globl _action_for_keycode
                                     36 	.globl _mDelaymS
                                     37 	.globl _host_consumer_send
                                     38 	.globl _host_system_send
                                     39 	.globl _host_keyboard_leds
                                     40 	.globl _led_set
                                     41 	.globl _clear_keys_from_report
                                     42 	.globl _del_key_from_report
                                     43 	.globl _add_key_to_report
                                     44 	.globl _is_key_pressed
                                     45 	.globl _KEYCODE2CONSUMER
                                     46 	.globl _ADC_START
                                     47 	.globl _S0_R_FIFO
                                     48 	.globl _S0_T_FIFO
                                     49 	.globl _S0_FREE
                                     50 	.globl _S0_IF_BYTE
                                     51 	.globl _S0_IF_FIRST
                                     52 	.globl _S0_IF_OV
                                     53 	.globl _S0_FST_ACT
                                     54 	.globl _CP_RL2
                                     55 	.globl _C_T2
                                     56 	.globl _TR2
                                     57 	.globl _EXEN2
                                     58 	.globl _TCLK
                                     59 	.globl _RCLK
                                     60 	.globl _EXF2
                                     61 	.globl _CAP1F
                                     62 	.globl _TF2
                                     63 	.globl _RI
                                     64 	.globl _TI
                                     65 	.globl _RB8
                                     66 	.globl _TB8
                                     67 	.globl _REN
                                     68 	.globl _SM2
                                     69 	.globl _SM1
                                     70 	.globl _SM0
                                     71 	.globl _IT0
                                     72 	.globl _IE0
                                     73 	.globl _IT1
                                     74 	.globl _IE1
                                     75 	.globl _TR0
                                     76 	.globl _TF0
                                     77 	.globl _TR1
                                     78 	.globl _TF1
                                     79 	.globl _P4_0
                                     80 	.globl _P4_1
                                     81 	.globl _P4_2
                                     82 	.globl _P4_3
                                     83 	.globl _P4_4
                                     84 	.globl _P4_5
                                     85 	.globl _P4_6
                                     86 	.globl _RXD
                                     87 	.globl _TXD
                                     88 	.globl _INT0
                                     89 	.globl _INT1
                                     90 	.globl _T0
                                     91 	.globl _T1
                                     92 	.globl _MOSI1
                                     93 	.globl _MISO1
                                     94 	.globl _SCK1
                                     95 	.globl _P3_0
                                     96 	.globl _P3_1
                                     97 	.globl _P3_2
                                     98 	.globl _P3_3
                                     99 	.globl _P3_4
                                    100 	.globl _P3_5
                                    101 	.globl _P3_6
                                    102 	.globl _P3_7
                                    103 	.globl _CAP1_
                                    104 	.globl _T2_
                                    105 	.globl _CAP2_
                                    106 	.globl _T2EX_
                                    107 	.globl _RXD1
                                    108 	.globl _TXD1
                                    109 	.globl _P2_0
                                    110 	.globl _P2_1
                                    111 	.globl _P2_2
                                    112 	.globl _P2_3
                                    113 	.globl _P2_4
                                    114 	.globl _P2_5
                                    115 	.globl _P2_6
                                    116 	.globl _P2_7
                                    117 	.globl _AIN0
                                    118 	.globl _AIN1
                                    119 	.globl _AIN2
                                    120 	.globl _AIN3
                                    121 	.globl _AIN4
                                    122 	.globl _AIN5
                                    123 	.globl _AIN6
                                    124 	.globl _AIN7
                                    125 	.globl _CAP1
                                    126 	.globl _T2
                                    127 	.globl _CAP2
                                    128 	.globl _T2EX
                                    129 	.globl _INT0_
                                    130 	.globl _SCS
                                    131 	.globl _MOSI
                                    132 	.globl _MISO
                                    133 	.globl _SCK
                                    134 	.globl _RXD1_
                                    135 	.globl _TXD1_
                                    136 	.globl _P1_0
                                    137 	.globl _P1_1
                                    138 	.globl _P1_2
                                    139 	.globl _P1_3
                                    140 	.globl _P1_4
                                    141 	.globl _P1_5
                                    142 	.globl _P1_6
                                    143 	.globl _P1_7
                                    144 	.globl _AIN8
                                    145 	.globl _AIN9
                                    146 	.globl _AIN10
                                    147 	.globl _AIN11
                                    148 	.globl _AIN12
                                    149 	.globl _AIN13
                                    150 	.globl _RXD_
                                    151 	.globl _TXD_
                                    152 	.globl _SCL0
                                    153 	.globl _SDA0
                                    154 	.globl _P0_0
                                    155 	.globl _P0_1
                                    156 	.globl _P0_2
                                    157 	.globl _P0_3
                                    158 	.globl _P0_4
                                    159 	.globl _P0_5
                                    160 	.globl _P0_6
                                    161 	.globl _P0_7
                                    162 	.globl _IE_SPI0
                                    163 	.globl _IE_USB
                                    164 	.globl _IE_ADC
                                    165 	.globl _IE_UART1
                                    166 	.globl _IE_PWM_I2C
                                    167 	.globl _IE_GPIO
                                    168 	.globl _IE_WDOG
                                    169 	.globl _PX0
                                    170 	.globl _PT0
                                    171 	.globl _PX1
                                    172 	.globl _PT1
                                    173 	.globl _PS
                                    174 	.globl _PT2
                                    175 	.globl _PL_FLAG
                                    176 	.globl _PH_FLAG
                                    177 	.globl _EX0
                                    178 	.globl _ET0
                                    179 	.globl _EX1
                                    180 	.globl _ET1
                                    181 	.globl _ES
                                    182 	.globl _ET2
                                    183 	.globl _E_DIS
                                    184 	.globl _EA
                                    185 	.globl _P
                                    186 	.globl _F1
                                    187 	.globl _OV
                                    188 	.globl _RS0
                                    189 	.globl _RS1
                                    190 	.globl _F0
                                    191 	.globl _AC
                                    192 	.globl _CY
                                    193 	.globl _I2CS_INT_ST
                                    194 	.globl _I2CX_INT
                                    195 	.globl _LED_STATUS
                                    196 	.globl _LED_DMA_H
                                    197 	.globl _LED_DMA_L
                                    198 	.globl _LED_DMA
                                    199 	.globl _LED_PWM_OE
                                    200 	.globl _LED_COMMON
                                    201 	.globl _ADC_CHAN
                                    202 	.globl _ADC_DAT_H
                                    203 	.globl _ADC_DAT_L
                                    204 	.globl _ADC_DAT
                                    205 	.globl _ADC_CTRL
                                    206 	.globl _SPI1_CK_SE
                                    207 	.globl _SPI1_CTRL
                                    208 	.globl _SPI1_DATA
                                    209 	.globl _SPI1_STAT
                                    210 	.globl _SIF1
                                    211 	.globl _SBAUD1
                                    212 	.globl _SBUF1
                                    213 	.globl _SCON1
                                    214 	.globl _SPI0_SETUP
                                    215 	.globl _SPI0_CK_SE
                                    216 	.globl _SPI0_CTRL
                                    217 	.globl _SPI0_DATA
                                    218 	.globl _SPI0_STAT
                                    219 	.globl _T2CAP1H
                                    220 	.globl _T2CAP1L
                                    221 	.globl _T2CAP1
                                    222 	.globl _TH2
                                    223 	.globl _TL2
                                    224 	.globl _T2COUNT
                                    225 	.globl _RCAP2H
                                    226 	.globl _RCAP2L
                                    227 	.globl _RCAP2
                                    228 	.globl _T2MOD
                                    229 	.globl _T2CON
                                    230 	.globl _SBUF
                                    231 	.globl _SCON
                                    232 	.globl _TH1
                                    233 	.globl _TH0
                                    234 	.globl _TL1
                                    235 	.globl _TL0
                                    236 	.globl _TMOD
                                    237 	.globl _TCON
                                    238 	.globl _XBUS_AUX
                                    239 	.globl _P7
                                    240 	.globl _P6_DIR
                                    241 	.globl _P6_OUT_PU
                                    242 	.globl _P6_IN
                                    243 	.globl _P5_DIR
                                    244 	.globl _P5_OUT_PU
                                    245 	.globl _P5_IN
                                    246 	.globl _P4_LED_KEY
                                    247 	.globl _P4_DIR_PU
                                    248 	.globl _P4_MOD_OC
                                    249 	.globl _P4
                                    250 	.globl _P3_DIR_PU
                                    251 	.globl _P3_MOD_OC
                                    252 	.globl _P3
                                    253 	.globl _P2_DIR_PU
                                    254 	.globl _P2_MOD_OC
                                    255 	.globl _P2
                                    256 	.globl _P1_DIR_PU
                                    257 	.globl _P1_MOD_OC
                                    258 	.globl _P1
                                    259 	.globl _P0_DIR_PU
                                    260 	.globl _P0_MOD_OC
                                    261 	.globl _P0
                                    262 	.globl _ROM_CTRL
                                    263 	.globl _ROM_DATA_HH
                                    264 	.globl _ROM_DATA_HL
                                    265 	.globl _ROM_DATA_HI
                                    266 	.globl _ROM_ADDR_H
                                    267 	.globl _ROM_ADDR_L
                                    268 	.globl _ROM_ADDR
                                    269 	.globl _GPIO_IE
                                    270 	.globl _IP_EX
                                    271 	.globl _IE_EX
                                    272 	.globl _IP
                                    273 	.globl _IE
                                    274 	.globl _WDOG_COUNT
                                    275 	.globl _RESET_KEEP
                                    276 	.globl _WAKE_CTRL
                                    277 	.globl _CLOCK_CFG
                                    278 	.globl _POWER_CFG
                                    279 	.globl _PCON
                                    280 	.globl _GLOBAL_CFG
                                    281 	.globl _SAFE_MOD
                                    282 	.globl _DPH
                                    283 	.globl _DPL
                                    284 	.globl _SP
                                    285 	.globl _A_INV
                                    286 	.globl _B
                                    287 	.globl _ACC
                                    288 	.globl _PSW
                                    289 	.globl _disable_action_cache
                                    290 	.globl _tap_code_delay_PARM_2
                                    291 	.globl _process_action_PARM_2
                                    292 	.globl _action_exec_PARM_1
                                    293 	.globl _tp_buttons
                                    294 	.globl _action_exec
                                    295 	.globl _process_record
                                    296 	.globl _process_record_handler
                                    297 	.globl _process_action
                                    298 	.globl _register_code
                                    299 	.globl _unregister_code
                                    300 	.globl _tap_code_delay
                                    301 	.globl _tap_code
                                    302 	.globl _register_mods
                                    303 	.globl _unregister_mods
                                    304 	.globl _register_weak_mods
                                    305 	.globl _unregister_weak_mods
                                    306 	.globl _clear_keyboard
                                    307 	.globl _clear_keyboard_but_mods
                                    308 	.globl _clear_keyboard_but_mods_and_keys
                                    309 ;--------------------------------------------------------
                                    310 ; special function registers
                                    311 ;--------------------------------------------------------
                                    312 	.area RSEG    (ABS,DATA)
      000000                        313 	.org 0x0000
                           0000D0   314 _PSW	=	0x00d0
                           0000E0   315 _ACC	=	0x00e0
                           0000F0   316 _B	=	0x00f0
                           0000FD   317 _A_INV	=	0x00fd
                           000081   318 _SP	=	0x0081
                           000082   319 _DPL	=	0x0082
                           000083   320 _DPH	=	0x0083
                           0000A1   321 _SAFE_MOD	=	0x00a1
                           0000B1   322 _GLOBAL_CFG	=	0x00b1
                           000087   323 _PCON	=	0x0087
                           0000BA   324 _POWER_CFG	=	0x00ba
                           0000B9   325 _CLOCK_CFG	=	0x00b9
                           0000A9   326 _WAKE_CTRL	=	0x00a9
                           0000FE   327 _RESET_KEEP	=	0x00fe
                           0000FF   328 _WDOG_COUNT	=	0x00ff
                           0000A8   329 _IE	=	0x00a8
                           0000B8   330 _IP	=	0x00b8
                           0000E8   331 _IE_EX	=	0x00e8
                           0000E9   332 _IP_EX	=	0x00e9
                           0000B2   333 _GPIO_IE	=	0x00b2
                           008584   334 _ROM_ADDR	=	0x8584
                           000084   335 _ROM_ADDR_L	=	0x0084
                           000085   336 _ROM_ADDR_H	=	0x0085
                           008F8E   337 _ROM_DATA_HI	=	0x8f8e
                           00008E   338 _ROM_DATA_HL	=	0x008e
                           00008F   339 _ROM_DATA_HH	=	0x008f
                           000086   340 _ROM_CTRL	=	0x0086
                           000080   341 _P0	=	0x0080
                           0000C4   342 _P0_MOD_OC	=	0x00c4
                           0000C5   343 _P0_DIR_PU	=	0x00c5
                           000090   344 _P1	=	0x0090
                           000092   345 _P1_MOD_OC	=	0x0092
                           000093   346 _P1_DIR_PU	=	0x0093
                           0000A0   347 _P2	=	0x00a0
                           000094   348 _P2_MOD_OC	=	0x0094
                           000095   349 _P2_DIR_PU	=	0x0095
                           0000B0   350 _P3	=	0x00b0
                           000096   351 _P3_MOD_OC	=	0x0096
                           000097   352 _P3_DIR_PU	=	0x0097
                           0000C0   353 _P4	=	0x00c0
                           0000C2   354 _P4_MOD_OC	=	0x00c2
                           0000C3   355 _P4_DIR_PU	=	0x00c3
                           0000C1   356 _P4_LED_KEY	=	0x00c1
                           0000AA   357 _P5_IN	=	0x00aa
                           0000AB   358 _P5_OUT_PU	=	0x00ab
                           0000AC   359 _P5_DIR	=	0x00ac
                           0000AD   360 _P6_IN	=	0x00ad
                           0000AE   361 _P6_OUT_PU	=	0x00ae
                           0000AF   362 _P6_DIR	=	0x00af
                           0000F1   363 _P7	=	0x00f1
                           0000A2   364 _XBUS_AUX	=	0x00a2
                           000088   365 _TCON	=	0x0088
                           000089   366 _TMOD	=	0x0089
                           00008A   367 _TL0	=	0x008a
                           00008B   368 _TL1	=	0x008b
                           00008C   369 _TH0	=	0x008c
                           00008D   370 _TH1	=	0x008d
                           000098   371 _SCON	=	0x0098
                           000099   372 _SBUF	=	0x0099
                           0000C8   373 _T2CON	=	0x00c8
                           0000C9   374 _T2MOD	=	0x00c9
                           00CBCA   375 _RCAP2	=	0xcbca
                           0000CA   376 _RCAP2L	=	0x00ca
                           0000CB   377 _RCAP2H	=	0x00cb
                           00CDCC   378 _T2COUNT	=	0xcdcc
                           0000CC   379 _TL2	=	0x00cc
                           0000CD   380 _TH2	=	0x00cd
                           00CFCE   381 _T2CAP1	=	0xcfce
                           0000CE   382 _T2CAP1L	=	0x00ce
                           0000CF   383 _T2CAP1H	=	0x00cf
                           0000F8   384 _SPI0_STAT	=	0x00f8
                           0000F9   385 _SPI0_DATA	=	0x00f9
                           0000FA   386 _SPI0_CTRL	=	0x00fa
                           0000FB   387 _SPI0_CK_SE	=	0x00fb
                           0000FC   388 _SPI0_SETUP	=	0x00fc
                           0000BC   389 _SCON1	=	0x00bc
                           0000BD   390 _SBUF1	=	0x00bd
                           0000BE   391 _SBAUD1	=	0x00be
                           0000BF   392 _SIF1	=	0x00bf
                           0000B4   393 _SPI1_STAT	=	0x00b4
                           0000B5   394 _SPI1_DATA	=	0x00b5
                           0000B6   395 _SPI1_CTRL	=	0x00b6
                           0000B7   396 _SPI1_CK_SE	=	0x00b7
                           0000F3   397 _ADC_CTRL	=	0x00f3
                           00F5F4   398 _ADC_DAT	=	0xf5f4
                           0000F4   399 _ADC_DAT_L	=	0x00f4
                           0000F5   400 _ADC_DAT_H	=	0x00f5
                           0000F6   401 _ADC_CHAN	=	0x00f6
                           0000A6   402 _LED_COMMON	=	0x00a6
                           0000A7   403 _LED_PWM_OE	=	0x00a7
                           00C7C6   404 _LED_DMA	=	0xc7c6
                           0000C6   405 _LED_DMA_L	=	0x00c6
                           0000C7   406 _LED_DMA_H	=	0x00c7
                           0000F7   407 _LED_STATUS	=	0x00f7
                           0000B3   408 _I2CX_INT	=	0x00b3
                           0000BB   409 _I2CS_INT_ST	=	0x00bb
                                    410 ;--------------------------------------------------------
                                    411 ; special function bits
                                    412 ;--------------------------------------------------------
                                    413 	.area RSEG    (ABS,DATA)
      000000                        414 	.org 0x0000
                           0000D7   415 _CY	=	0x00d7
                           0000D6   416 _AC	=	0x00d6
                           0000D5   417 _F0	=	0x00d5
                           0000D4   418 _RS1	=	0x00d4
                           0000D3   419 _RS0	=	0x00d3
                           0000D2   420 _OV	=	0x00d2
                           0000D1   421 _F1	=	0x00d1
                           0000D0   422 _P	=	0x00d0
                           0000AF   423 _EA	=	0x00af
                           0000AE   424 _E_DIS	=	0x00ae
                           0000AD   425 _ET2	=	0x00ad
                           0000AC   426 _ES	=	0x00ac
                           0000AB   427 _ET1	=	0x00ab
                           0000AA   428 _EX1	=	0x00aa
                           0000A9   429 _ET0	=	0x00a9
                           0000A8   430 _EX0	=	0x00a8
                           0000BF   431 _PH_FLAG	=	0x00bf
                           0000BE   432 _PL_FLAG	=	0x00be
                           0000BD   433 _PT2	=	0x00bd
                           0000BC   434 _PS	=	0x00bc
                           0000BB   435 _PT1	=	0x00bb
                           0000BA   436 _PX1	=	0x00ba
                           0000B9   437 _PT0	=	0x00b9
                           0000B8   438 _PX0	=	0x00b8
                           0000EF   439 _IE_WDOG	=	0x00ef
                           0000EE   440 _IE_GPIO	=	0x00ee
                           0000ED   441 _IE_PWM_I2C	=	0x00ed
                           0000EC   442 _IE_UART1	=	0x00ec
                           0000EB   443 _IE_ADC	=	0x00eb
                           0000E9   444 _IE_USB	=	0x00e9
                           0000E8   445 _IE_SPI0	=	0x00e8
                           000087   446 _P0_7	=	0x0087
                           000086   447 _P0_6	=	0x0086
                           000085   448 _P0_5	=	0x0085
                           000084   449 _P0_4	=	0x0084
                           000083   450 _P0_3	=	0x0083
                           000082   451 _P0_2	=	0x0082
                           000081   452 _P0_1	=	0x0081
                           000080   453 _P0_0	=	0x0080
                           000081   454 _SDA0	=	0x0081
                           000080   455 _SCL0	=	0x0080
                           000083   456 _TXD_	=	0x0083
                           000082   457 _RXD_	=	0x0082
                           000085   458 _AIN13	=	0x0085
                           000084   459 _AIN12	=	0x0084
                           000083   460 _AIN11	=	0x0083
                           000082   461 _AIN10	=	0x0082
                           000081   462 _AIN9	=	0x0081
                           000080   463 _AIN8	=	0x0080
                           000097   464 _P1_7	=	0x0097
                           000096   465 _P1_6	=	0x0096
                           000095   466 _P1_5	=	0x0095
                           000094   467 _P1_4	=	0x0094
                           000093   468 _P1_3	=	0x0093
                           000092   469 _P1_2	=	0x0092
                           000091   470 _P1_1	=	0x0091
                           000090   471 _P1_0	=	0x0090
                           000097   472 _TXD1_	=	0x0097
                           000096   473 _RXD1_	=	0x0096
                           000097   474 _SCK	=	0x0097
                           000096   475 _MISO	=	0x0096
                           000095   476 _MOSI	=	0x0095
                           000094   477 _SCS	=	0x0094
                           000092   478 _INT0_	=	0x0092
                           000091   479 _T2EX	=	0x0091
                           000091   480 _CAP2	=	0x0091
                           000090   481 _T2	=	0x0090
                           000090   482 _CAP1	=	0x0090
                           000097   483 _AIN7	=	0x0097
                           000096   484 _AIN6	=	0x0096
                           000095   485 _AIN5	=	0x0095
                           000094   486 _AIN4	=	0x0094
                           000093   487 _AIN3	=	0x0093
                           000092   488 _AIN2	=	0x0092
                           000091   489 _AIN1	=	0x0091
                           000090   490 _AIN0	=	0x0090
                           0000A7   491 _P2_7	=	0x00a7
                           0000A6   492 _P2_6	=	0x00a6
                           0000A5   493 _P2_5	=	0x00a5
                           0000A4   494 _P2_4	=	0x00a4
                           0000A3   495 _P2_3	=	0x00a3
                           0000A2   496 _P2_2	=	0x00a2
                           0000A1   497 _P2_1	=	0x00a1
                           0000A0   498 _P2_0	=	0x00a0
                           0000A7   499 _TXD1	=	0x00a7
                           0000A6   500 _RXD1	=	0x00a6
                           0000A5   501 _T2EX_	=	0x00a5
                           0000A5   502 _CAP2_	=	0x00a5
                           0000A4   503 _T2_	=	0x00a4
                           0000A4   504 _CAP1_	=	0x00a4
                           0000B7   505 _P3_7	=	0x00b7
                           0000B6   506 _P3_6	=	0x00b6
                           0000B5   507 _P3_5	=	0x00b5
                           0000B4   508 _P3_4	=	0x00b4
                           0000B3   509 _P3_3	=	0x00b3
                           0000B2   510 _P3_2	=	0x00b2
                           0000B1   511 _P3_1	=	0x00b1
                           0000B0   512 _P3_0	=	0x00b0
                           0000B7   513 _SCK1	=	0x00b7
                           0000B6   514 _MISO1	=	0x00b6
                           0000B5   515 _MOSI1	=	0x00b5
                           0000B5   516 _T1	=	0x00b5
                           0000B4   517 _T0	=	0x00b4
                           0000B3   518 _INT1	=	0x00b3
                           0000B2   519 _INT0	=	0x00b2
                           0000B1   520 _TXD	=	0x00b1
                           0000B0   521 _RXD	=	0x00b0
                           0000C6   522 _P4_6	=	0x00c6
                           0000C5   523 _P4_5	=	0x00c5
                           0000C4   524 _P4_4	=	0x00c4
                           0000C3   525 _P4_3	=	0x00c3
                           0000C2   526 _P4_2	=	0x00c2
                           0000C1   527 _P4_1	=	0x00c1
                           0000C0   528 _P4_0	=	0x00c0
                           00008F   529 _TF1	=	0x008f
                           00008E   530 _TR1	=	0x008e
                           00008D   531 _TF0	=	0x008d
                           00008C   532 _TR0	=	0x008c
                           00008B   533 _IE1	=	0x008b
                           00008A   534 _IT1	=	0x008a
                           000089   535 _IE0	=	0x0089
                           000088   536 _IT0	=	0x0088
                           00009F   537 _SM0	=	0x009f
                           00009E   538 _SM1	=	0x009e
                           00009D   539 _SM2	=	0x009d
                           00009C   540 _REN	=	0x009c
                           00009B   541 _TB8	=	0x009b
                           00009A   542 _RB8	=	0x009a
                           000099   543 _TI	=	0x0099
                           000098   544 _RI	=	0x0098
                           0000CF   545 _TF2	=	0x00cf
                           0000CF   546 _CAP1F	=	0x00cf
                           0000CE   547 _EXF2	=	0x00ce
                           0000CD   548 _RCLK	=	0x00cd
                           0000CC   549 _TCLK	=	0x00cc
                           0000CB   550 _EXEN2	=	0x00cb
                           0000CA   551 _TR2	=	0x00ca
                           0000C9   552 _C_T2	=	0x00c9
                           0000C8   553 _CP_RL2	=	0x00c8
                           0000FF   554 _S0_FST_ACT	=	0x00ff
                           0000FE   555 _S0_IF_OV	=	0x00fe
                           0000FD   556 _S0_IF_FIRST	=	0x00fd
                           0000FC   557 _S0_IF_BYTE	=	0x00fc
                           0000FB   558 _S0_FREE	=	0x00fb
                           0000FA   559 _S0_T_FIFO	=	0x00fa
                           0000F8   560 _S0_R_FIFO	=	0x00f8
                           0000F7   561 _ADC_START	=	0x00f7
                                    562 ;--------------------------------------------------------
                                    563 ; overlayable register banks
                                    564 ;--------------------------------------------------------
                                    565 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        566 	.ds 8
                                    567 ;--------------------------------------------------------
                                    568 ; internal ram data
                                    569 ;--------------------------------------------------------
                                    570 	.area DSEG    (DATA)
                                    571 ;--------------------------------------------------------
                                    572 ; overlayable items in internal ram
                                    573 ;--------------------------------------------------------
                                    574 ;--------------------------------------------------------
                                    575 ; indirectly addressable internal ram data
                                    576 ;--------------------------------------------------------
                                    577 	.area ISEG    (DATA)
                                    578 ;--------------------------------------------------------
                                    579 ; absolute internal ram data
                                    580 ;--------------------------------------------------------
                                    581 	.area IABS    (ABS,DATA)
                                    582 	.area IABS    (ABS,DATA)
                                    583 ;--------------------------------------------------------
                                    584 ; bit data
                                    585 ;--------------------------------------------------------
                                    586 	.area BSEG    (BIT)
                                    587 ;--------------------------------------------------------
                                    588 ; paged external ram data
                                    589 ;--------------------------------------------------------
                                    590 	.area PSEG    (PAG,XDATA)
                                    591 ;--------------------------------------------------------
                                    592 ; uninitialized external ram data
                                    593 ;--------------------------------------------------------
                                    594 	.area XSEG    (XDATA)
      000739                        595 _tp_buttons::
      000739                        596 	.ds 2
      00073B                        597 _action_exec_PARM_1:
      00073B                        598 	.ds 6
      000741                        599 _action_exec_record_10001_587:
      000741                        600 	.ds 8
      000749                        601 _process_record_record_10000_592:
      000749                        602 	.ds 3
      00074C                        603 _process_record_handler_record_10000_598:
      00074C                        604 	.ds 3
      00074F                        605 _process_record_handler_action_10000_599:
      00074F                        606 	.ds 2
      000751                        607 _process_action_PARM_2:
      000751                        608 	.ds 2
      000753                        609 _process_action_record_10000_610:
      000753                        610 	.ds 3
      000756                        611 _process_action_event_10000_611:
      000756                        612 	.ds 6
      00075C                        613 _register_code_code_10000_666:
      00075C                        614 	.ds 1
      00075D                        615 _register_code___700000092_70000_678:
      00075D                        616 	.ds 2
      00075F                        617 _register_code_key_80000_690:
      00075F                        618 	.ds 1
      000760                        619 _unregister_code_code_10000_693:
      000760                        620 	.ds 1
      000761                        621 _tap_code_delay_PARM_2:
      000761                        622 	.ds 2
      000763                        623 _tap_code_delay_code_10000_710:
      000763                        624 	.ds 1
      000764                        625 _tap_code_code_10000_717:
      000764                        626 	.ds 1
      000765                        627 _register_mods_mods_10000_719:
      000765                        628 	.ds 1
      000766                        629 _unregister_mods_mods_10000_723:
      000766                        630 	.ds 1
      000767                        631 _register_weak_mods_mods_10000_727:
      000767                        632 	.ds 1
      000768                        633 _unregister_weak_mods_mods_10000_731:
      000768                        634 	.ds 1
                                    635 ;--------------------------------------------------------
                                    636 ; absolute external ram data
                                    637 ;--------------------------------------------------------
                                    638 	.area XABS    (ABS,XDATA)
                                    639 ;--------------------------------------------------------
                                    640 ; initialized external ram data
                                    641 ;--------------------------------------------------------
                                    642 	.area XISEG   (XDATA)
      000BAB                        643 _disable_action_cache::
      000BAB                        644 	.ds 1
                                    645 	.area HOME    (CODE)
                                    646 	.area GSINIT0 (CODE)
                                    647 	.area GSINIT1 (CODE)
                                    648 	.area GSINIT2 (CODE)
                                    649 	.area GSINIT3 (CODE)
                                    650 	.area GSINIT4 (CODE)
                                    651 	.area GSINIT5 (CODE)
                                    652 	.area GSINIT  (CODE)
                                    653 	.area GSFINAL (CODE)
                                    654 	.area CSEG    (CODE)
                                    655 ;--------------------------------------------------------
                                    656 ; global & static initialisations
                                    657 ;--------------------------------------------------------
                                    658 	.area HOME    (CODE)
                                    659 	.area GSINIT  (CODE)
                                    660 	.area GSFINAL (CODE)
                                    661 	.area GSINIT  (CODE)
                                    662 ;--------------------------------------------------------
                                    663 ; Home
                                    664 ;--------------------------------------------------------
                                    665 	.area HOME    (CODE)
                                    666 	.area HOME    (CODE)
                                    667 ;--------------------------------------------------------
                                    668 ; code
                                    669 ;--------------------------------------------------------
                                    670 	.area CSEG    (CODE)
                                    671 ;------------------------------------------------------------
                                    672 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    673 ;------------------------------------------------------------
                                    674 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_40'
                                    675 ;------------------------------------------------------------
                                    676 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    677 ;	-----------------------------------------
                           000007   678 	ar7 = 0x07
                           000006   679 	ar6 = 0x06
                           000005   680 	ar5 = 0x05
                           000004   681 	ar4 = 0x04
                           000003   682 	ar3 = 0x03
                           000002   683 	ar2 = 0x02
                           000001   684 	ar1 = 0x01
                           000000   685 	ar0 = 0x00
                                    686 ;	 function action_exec
                                    687 ;	-----------------------------------------
      006CE1                        688 _action_exec:
                                    689 ;	quantum/action.c:89: if (event.pressed) {
      006CE1 90 07 40         [24]  690 	mov	dptr,#(_action_exec_PARM_1 + 0x0005)
      006CE4 E0               [24]  691 	movx	a,@dptr
      006CE5 60 03            [24]  692 	jz	00102$
                                    693 ;	quantum/action.c:91: clear_weak_mods();
      006CE7 12 78 B9         [24]  694 	lcall	_clear_weak_mods
      006CEA                        695 00102$:
                                    696 ;	quantum/action.c:103: record.event = event;
      006CEA 90 0B 8F         [24]  697 	mov	dptr,#___memcpy_PARM_2
      006CED 74 3B            [12]  698 	mov	a,#_action_exec_PARM_1
      006CEF F0               [24]  699 	movx	@dptr,a
      006CF0 74 07            [12]  700 	mov	a,#(_action_exec_PARM_1 >> 8)
      006CF2 A3               [24]  701 	inc	dptr
      006CF3 F0               [24]  702 	movx	@dptr,a
      006CF4 E4               [12]  703 	clr	a
      006CF5 A3               [24]  704 	inc	dptr
      006CF6 F0               [24]  705 	movx	@dptr,a
      006CF7 90 0B 92         [24]  706 	mov	dptr,#___memcpy_PARM_3
      006CFA 74 06            [12]  707 	mov	a,#0x06
      006CFC F0               [24]  708 	movx	@dptr,a
      006CFD E4               [12]  709 	clr	a
      006CFE A3               [24]  710 	inc	dptr
      006CFF F0               [24]  711 	movx	@dptr,a
      006D00 90 07 41         [24]  712 	mov	dptr,#_action_exec_record_10001_587
      006D03 F5 F0            [12]  713 	mov	b,a
      006D05 12 B4 9F         [24]  714 	lcall	___memcpy
                                    715 ;	quantum/action.c:107: record.keycode = 0;
      006D08 90 07 47         [24]  716 	mov	dptr,#(_action_exec_record_10001_587 + 0x0006)
      006D0B E4               [12]  717 	clr	a
      006D0C F0               [24]  718 	movx	@dptr,a
      006D0D A3               [24]  719 	inc	dptr
      006D0E F0               [24]  720 	movx	@dptr,a
                                    721 ;	quantum/action.c:138: if (IS_NOEVENT(record.event) || pre_process_record_quantum(&record)) {
      006D0F 90 07 45         [24]  722 	mov	dptr,#(_action_exec_record_10001_587 + 0x0004)
      006D12 E0               [24]  723 	movx	a,@dptr
      006D13 60 0D            [24]  724 	jz	00103$
      006D15 90 07 41         [24]  725 	mov	dptr,#_action_exec_record_10001_587
      006D18 75 F0 00         [24]  726 	mov	b, #0x00
      006D1B 12 99 91         [24]  727 	lcall	_pre_process_record_quantum
      006D1E E5 82            [12]  728 	mov	a, dpl
      006D20 60 09            [24]  729 	jz	00106$
      006D22                        730 00103$:
                                    731 ;	quantum/action.c:139: process_record(&record);
      006D22 90 07 41         [24]  732 	mov	dptr,#_action_exec_record_10001_587
      006D25 75 F0 00         [24]  733 	mov	b, #0x00
                                    734 ;	quantum/action.c:149: }
      006D28 02 6D 2C         [24]  735 	ljmp	_process_record
      006D2B                        736 00106$:
      006D2B 22               [24]  737 	ret
                                    738 ;------------------------------------------------------------
                                    739 ;Allocation info for local variables in function 'process_record_nocache'
                                    740 ;------------------------------------------------------------
                                    741 ;record        Allocated with name '_process_record_nocache_record_10000_590'
                                    742 ;------------------------------------------------------------
                                    743 ;	quantum/action.c:233: void process_record_nocache(keyrecord_t *record) {
                                    744 ;	-----------------------------------------
                                    745 ;	 function process_record
                                    746 ;	-----------------------------------------
      006D2C                        747 _process_record:
      006D2C AF F0            [24]  748 	mov	r7,b
      006D2E AE 83            [24]  749 	mov	r6,dph
      006D30 E5 82            [12]  750 	mov	a,dpl
      006D32 90 07 49         [24]  751 	mov	dptr,#_process_record_record_10000_592
      006D35 F0               [24]  752 	movx	@dptr,a
      006D36 EE               [12]  753 	mov	a,r6
      006D37 A3               [24]  754 	inc	dptr
      006D38 F0               [24]  755 	movx	@dptr,a
      006D39 EF               [12]  756 	mov	a,r7
      006D3A A3               [24]  757 	inc	dptr
      006D3B F0               [24]  758 	movx	@dptr,a
                                    759 ;	quantum/action.c:287: if (IS_NOEVENT(record->event)) {
      006D3C 90 07 49         [24]  760 	mov	dptr,#_process_record_record_10000_592
      006D3F 12 73 99         [24]  761 	lcall	_ak820_outline_0002
      006D42 74 04            [12]  762 	mov	a,#0x04
      006D44 12 73 A2         [24]  763 	lcall	_ak820_outline_0009
      006D47 12 B5 78         [24]  764 	lcall	__gptrget
      006D4A 70 01            [24]  765 	jnz	00102$
                                    766 ;	quantum/action.c:288: return;
      006D4C 22               [24]  767 	ret
      006D4D                        768 00102$:
                                    769 ;	quantum/action.c:291: if (!process_record_quantum(record)) {
      006D4D 8D 82            [24]  770 	mov	dpl, r5
      006D4F 8E 83            [24]  771 	mov	dph, r6
      006D51 8F F0            [24]  772 	mov	b, r7
      006D53 C0 07            [24]  773 	push	ar7
      006D55 C0 06            [24]  774 	push	ar6
      006D57 C0 05            [24]  775 	push	ar5
      006D59 12 9A 11         [24]  776 	lcall	_process_record_quantum
      006D5C E5 82            [12]  777 	mov	a, dpl
      006D5E D0 05            [24]  778 	pop	ar5
      006D60 D0 06            [24]  779 	pop	ar6
      006D62 D0 07            [24]  780 	pop	ar7
      006D64 70 01            [24]  781 	jnz	00104$
                                    782 ;	quantum/action.c:297: return;
      006D66 22               [24]  783 	ret
      006D67                        784 00104$:
                                    785 ;	quantum/action.c:300: process_record_handler(record);
      006D67 8D 82            [24]  786 	mov	dpl, r5
      006D69 8E 83            [24]  787 	mov	dph, r6
      006D6B 8F F0            [24]  788 	mov	b, r7
      006D6D 12 6D 7F         [24]  789 	lcall	_process_record_handler
                                    790 ;	quantum/action.c:301: post_process_record_quantum(record);
      006D70 90 07 49         [24]  791 	mov	dptr,#_process_record_record_10000_592
      006D73 12 73 99         [24]  792 	lcall	_ak820_outline_0002
      006D76 8D 82            [24]  793 	mov	dpl, r5
      006D78 8E 83            [24]  794 	mov	dph, r6
      006D7A 8F F0            [24]  795 	mov	b, r7
                                    796 ;	quantum/action.c:302: }
      006D7C 02 99 DA         [24]  797 	ljmp	_post_process_record_quantum
                                    798 ;------------------------------------------------------------
                                    799 ;Allocation info for local variables in function 'process_record_handler'
                                    800 ;------------------------------------------------------------
                                    801 ;record        Allocated with name '_process_record_handler_record_10000_598'
                                    802 ;action        Allocated with name '_process_record_handler_action_10000_599'
                                    803 ;------------------------------------------------------------
                                    804 ;	quantum/action.c:304: void process_record_handler(keyrecord_t *record) {
                                    805 ;	-----------------------------------------
                                    806 ;	 function process_record_handler
                                    807 ;	-----------------------------------------
      006D7F                        808 _process_record_handler:
      006D7F AF F0            [24]  809 	mov	r7,b
      006D81 AE 83            [24]  810 	mov	r6,dph
      006D83 E5 82            [12]  811 	mov	a,dpl
      006D85 90 07 4C         [24]  812 	mov	dptr,#_process_record_handler_record_10000_598
      006D88 F0               [24]  813 	movx	@dptr,a
      006D89 EE               [12]  814 	mov	a,r6
      006D8A A3               [24]  815 	inc	dptr
      006D8B F0               [24]  816 	movx	@dptr,a
      006D8C EF               [12]  817 	mov	a,r7
      006D8D A3               [24]  818 	inc	dptr
      006D8E F0               [24]  819 	movx	@dptr,a
                                    820 ;	quantum/action.c:308: if (record->keycode) {
      006D8F 90 07 4C         [24]  821 	mov	dptr,#_process_record_handler_record_10000_598
      006D92 12 73 99         [24]  822 	lcall	_ak820_outline_0002
      006D95 74 06            [12]  823 	mov	a,#0x06
      006D97 2D               [12]  824 	add	a, r5
      006D98 FB               [12]  825 	mov	r3,a
      006D99 E4               [12]  826 	clr	a
      006D9A 3E               [12]  827 	addc	a, r6
      006D9B FA               [12]  828 	mov	r2,a
      006D9C 8F 04            [24]  829 	mov	ar4,r7
      006D9E 8B 82            [24]  830 	mov	dpl,r3
      006DA0 8A 83            [24]  831 	mov	dph,r2
      006DA2 8C F0            [24]  832 	mov	b,r4
      006DA4 12 B5 78         [24]  833 	lcall	__gptrget
      006DA7 FB               [12]  834 	mov	r3,a
      006DA8 A3               [24]  835 	inc	dptr
      006DA9 12 B5 78         [24]  836 	lcall	__gptrget
      006DAC FC               [12]  837 	mov	r4,a
      006DAD 4B               [12]  838 	orl	a,r3
      006DAE 60 15            [24]  839 	jz	00102$
                                    840 ;	quantum/action.c:309: action.code = action_for_keycode(record->keycode);
      006DB0 8B 82            [24]  841 	mov	dpl, r3
      006DB2 8C 83            [24]  842 	mov	dph, r4
      006DB4 12 8D AF         [24]  843 	lcall	_action_for_keycode
      006DB7 AB 82            [24]  844 	mov	r3, dpl
      006DB9 AC 83            [24]  845 	mov	r4, dph
      006DBB 90 07 4F         [24]  846 	mov	dptr,#_process_record_handler_action_10000_599
      006DBE EB               [12]  847 	mov	a,r3
      006DBF F0               [24]  848 	movx	@dptr,a
      006DC0 EC               [12]  849 	mov	a,r4
      006DC1 A3               [24]  850 	inc	dptr
      006DC2 F0               [24]  851 	movx	@dptr,a
      006DC3 80 35            [24]  852 	sjmp	00104$
      006DC5                        853 00102$:
                                    854 ;	quantum/action.c:311: action.code = store_or_get_action(record->event.pressed, record->event.key);
      006DC5 74 05            [12]  855 	mov	a,#0x05
      006DC7 12 73 A2         [24]  856 	lcall	_ak820_outline_0009
      006DCA 12 B5 78         [24]  857 	lcall	__gptrget
      006DCD FA               [12]  858 	mov	r2,a
      006DCE 90 0B 8F         [24]  859 	mov	dptr,#___memcpy_PARM_2
      006DD1 12 73 BA         [24]  860 	lcall	_ak820_outline_0015
      006DD4 90 0B 92         [24]  861 	mov	dptr,#___memcpy_PARM_3
      006DD7 74 02            [12]  862 	mov	a,#0x02
      006DD9 F0               [24]  863 	movx	@dptr,a
      006DDA E4               [12]  864 	clr	a
      006DDB A3               [24]  865 	inc	dptr
      006DDC F0               [24]  866 	movx	@dptr,a
      006DDD 90 08 86         [24]  867 	mov	dptr,#_store_or_get_action_PARM_2
      006DE0 F5 F0            [12]  868 	mov	b,a
      006DE2 C0 02            [24]  869 	push	ar2
      006DE4 12 B4 9F         [24]  870 	lcall	___memcpy
      006DE7 D0 02            [24]  871 	pop	ar2
      006DE9 8A 82            [24]  872 	mov	dpl, r2
      006DEB 12 76 4D         [24]  873 	lcall	_store_or_get_action
      006DEE AE 82            [24]  874 	mov	r6, dpl
      006DF0 AF 83            [24]  875 	mov	r7, dph
      006DF2 90 07 4F         [24]  876 	mov	dptr,#_process_record_handler_action_10000_599
      006DF5 EE               [12]  877 	mov	a,r6
      006DF6 F0               [24]  878 	movx	@dptr,a
      006DF7 EF               [12]  879 	mov	a,r7
      006DF8 A3               [24]  880 	inc	dptr
      006DF9 F0               [24]  881 	movx	@dptr,a
                                    882 ;	quantum/action.c:317: ac_dprintf("ACTION: ");
      006DFA                        883 00104$:
                                    884 ;	quantum/action.c:328: process_action(record, action);
      006DFA 90 07 4C         [24]  885 	mov	dptr,#_process_record_handler_record_10000_598
      006DFD 12 73 99         [24]  886 	lcall	_ak820_outline_0002
      006E00 90 0B 8F         [24]  887 	mov	dptr,#___memcpy_PARM_2
      006E03 74 4F            [12]  888 	mov	a,#_process_record_handler_action_10000_599
      006E05 F0               [24]  889 	movx	@dptr,a
      006E06 74 07            [12]  890 	mov	a,#(_process_record_handler_action_10000_599 >> 8)
      006E08 A3               [24]  891 	inc	dptr
      006E09 F0               [24]  892 	movx	@dptr,a
      006E0A E4               [12]  893 	clr	a
      006E0B A3               [24]  894 	inc	dptr
      006E0C F0               [24]  895 	movx	@dptr,a
      006E0D 90 0B 92         [24]  896 	mov	dptr,#___memcpy_PARM_3
      006E10 74 02            [12]  897 	mov	a,#0x02
      006E12 F0               [24]  898 	movx	@dptr,a
      006E13 E4               [12]  899 	clr	a
      006E14 A3               [24]  900 	inc	dptr
      006E15 F0               [24]  901 	movx	@dptr,a
      006E16 90 07 51         [24]  902 	mov	dptr,#_process_action_PARM_2
      006E19 F5 F0            [12]  903 	mov	b,a
      006E1B C0 07            [24]  904 	push	ar7
      006E1D C0 06            [24]  905 	push	ar6
      006E1F C0 05            [24]  906 	push	ar5
      006E21 12 B4 9F         [24]  907 	lcall	___memcpy
      006E24 D0 05            [24]  908 	pop	ar5
      006E26 D0 06            [24]  909 	pop	ar6
      006E28 D0 07            [24]  910 	pop	ar7
      006E2A 8D 82            [24]  911 	mov	dpl, r5
      006E2C 8E 83            [24]  912 	mov	dph, r6
      006E2E 8F F0            [24]  913 	mov	b, r7
                                    914 ;	quantum/action.c:329: }
      006E30 02 6E 33         [24]  915 	ljmp	_process_action
                                    916 ;------------------------------------------------------------
                                    917 ;Allocation info for local variables in function 'register_mouse'
                                    918 ;------------------------------------------------------------
                                    919 ;pressed       Allocated with name '_register_mouse_PARM_2'
                                    920 ;mouse_keycode Allocated with name '_register_mouse_mouse_keycode_10000_607'
                                    921 ;------------------------------------------------------------
                                    922 ;	quantum/action.c:341: void register_mouse(uint8_t mouse_keycode, bool pressed) {
                                    923 ;	-----------------------------------------
                                    924 ;	 function process_action
                                    925 ;	-----------------------------------------
      006E33                        926 _process_action:
      006E33 AF F0            [24]  927 	mov	r7,b
      006E35 AE 83            [24]  928 	mov	r6,dph
      006E37 E5 82            [12]  929 	mov	a,dpl
      006E39 90 07 53         [24]  930 	mov	dptr,#_process_action_record_10000_610
      006E3C F0               [24]  931 	movx	@dptr,a
      006E3D EE               [12]  932 	mov	a,r6
      006E3E A3               [24]  933 	inc	dptr
      006E3F F0               [24]  934 	movx	@dptr,a
      006E40 EF               [12]  935 	mov	a,r7
      006E41 A3               [24]  936 	inc	dptr
      006E42 F0               [24]  937 	movx	@dptr,a
                                    938 ;	quantum/action.c:395: event = record->event;
      006E43 90 07 53         [24]  939 	mov	dptr,#_process_action_record_10000_610
      006E46 12 73 99         [24]  940 	lcall	_ak820_outline_0002
      006E49 90 0B 8F         [24]  941 	mov	dptr,#___memcpy_PARM_2
      006E4C 12 73 BA         [24]  942 	lcall	_ak820_outline_0015
      006E4F 90 0B 92         [24]  943 	mov	dptr,#___memcpy_PARM_3
      006E52 74 06            [12]  944 	mov	a,#0x06
      006E54 F0               [24]  945 	movx	@dptr,a
      006E55 E4               [12]  946 	clr	a
      006E56 A3               [24]  947 	inc	dptr
      006E57 F0               [24]  948 	movx	@dptr,a
      006E58 90 07 56         [24]  949 	mov	dptr,#_process_action_event_10000_611
      006E5B F5 F0            [12]  950 	mov	b,a
      006E5D 12 B4 9F         [24]  951 	lcall	___memcpy
                                    952 ;	quantum/action.c:419: switch (action.kind.id) {
      006E60 90 07 52         [24]  953 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      006E63 E0               [24]  954 	movx	a,@dptr
      006E64 C4               [12]  955 	swap	a
      006E65 54 0F            [12]  956 	anl	a,#0x0f
      006E67 FF               [12]  957 	mov  r7,a
      006E68 24 F4            [12]  958 	add	a,#0xff - 0x0b
      006E6A 50 03            [24]  959 	jnc	00426$
      006E6C 02 71 69         [24]  960 	ljmp	00180$
      006E6F                        961 00426$:
                                    962 ;	free result
      006E6F EF               [12]  963 	mov	a,r7
      006E70 24 0A            [12]  964 	add	a,#(00427$-3-.)
      006E72 83               [24]  965 	movc	a,@a+pc
      006E73 F5 82            [12]  966 	mov	dpl,a
      006E75 EF               [12]  967 	mov	a,r7
      006E76 24 10            [12]  968 	add	a,#(00428$-3-.)
      006E78 83               [24]  969 	movc	a,@a+pc
      006E79 F5 83            [12]  970 	mov	dph,a
      006E7B E4               [12]  971 	clr	a
      006E7C 73               [24]  972 	jmp	@a+dptr
      006E7D                        973 00427$:
      006E7D 95                     974 	.db	00102$
      006E7E 95                     975 	.db	00102$
      006E7F 69                     976 	.db	00180$
      006E80 69                     977 	.db	00180$
      006E81 33                     978 	.db	00123$
      006E82 69                     979 	.db	00180$
      006E83 69                     980 	.db	00180$
      006E84 69                     981 	.db	00180$
      006E85 86                     982 	.db	00128$
      006E86 B2                     983 	.db	00146$
      006E87 E6                     984 	.db	00151$
      006E88 E6                     985 	.db	00151$
      006E89                        986 00428$:
      006E89 6E                     987 	.db	00102$>>8
      006E8A 6E                     988 	.db	00102$>>8
      006E8B 71                     989 	.db	00180$>>8
      006E8C 71                     990 	.db	00180$>>8
      006E8D 6F                     991 	.db	00123$>>8
      006E8E 71                     992 	.db	00180$>>8
      006E8F 71                     993 	.db	00180$>>8
      006E90 71                     994 	.db	00180$>>8
      006E91 6F                     995 	.db	00128$>>8
      006E92 70                     996 	.db	00146$>>8
      006E93 70                     997 	.db	00151$>>8
      006E94 70                     998 	.db	00151$>>8
                                    999 ;	quantum/action.c:422: case ACT_RMODS: {
      006E95                       1000 00102$:
                                   1001 ;	quantum/action.c:423: mods = (action.kind.id == ACT_LMODS) ? action.key.mods : action.key.mods << 4;
      006E95 90 07 52         [24] 1002 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      006E98 E0               [24] 1003 	movx	a,@dptr
      006E99 54 F0            [12] 1004 	anl	a,#0xf0
      006E9B 70 09            [24] 1005 	jnz	00193$
      006E9D 90 07 52         [24] 1006 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      006EA0 E0               [24] 1007 	movx	a,@dptr
      006EA1 54 0F            [12] 1008 	anl	a,#0x0f
      006EA3 FF               [12] 1009 	mov	r7,a
      006EA4 80 0A            [24] 1010 	sjmp	00194$
      006EA6                       1011 00193$:
      006EA6 90 07 52         [24] 1012 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      006EA9 E0               [24] 1013 	movx	a,@dptr
      006EAA 54 0F            [12] 1014 	anl	a,#0x0f
      006EAC C4               [12] 1015 	swap	a
      006EAD 54 F0            [12] 1016 	anl	a,#0xf0
      006EAF FF               [12] 1017 	mov	r7,a
      006EB0                       1018 00194$:
                                   1019 ;	quantum/action.c:425: if (event.pressed) {
      006EB0 90 07 5B         [24] 1020 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      006EB3 E0               [24] 1021 	movx	a,@dptr
      006EB4 60 3B            [24] 1022 	jz	00119$
                                   1023 ;	quantum/action.c:426: if (mods) {
      006EB6 EF               [12] 1024 	mov	a,r7
      006EB7 60 2C            [24] 1025 	jz	00110$
                                   1026 ;	quantum/action.c:427: if (IS_MODIFIER_KEYCODE(action.key.code) || action.key.code == KC_NO) {
      006EB9 90 07 51         [24] 1027 	mov	dptr,#_process_action_PARM_2
      006EBC E0               [24] 1028 	movx	a,@dptr
      006EBD FE               [12] 1029 	mov	r6,a
      006EBE BE E0 00         [24] 1030 	cjne	r6,#0xe0,00432$
      006EC1                       1031 00432$:
      006EC1 40 08            [24] 1032 	jc	00108$
      006EC3 90 07 51         [24] 1033 	mov	dptr,#_process_action_PARM_2
      006EC6 E0               [24] 1034 	movx	a,@dptr
      006EC7 24 18            [12] 1035 	add	a,#0xff - 0xe7
      006EC9 50 0B            [24] 1036 	jnc	00104$
                                   1037 ;	free result
      006ECB                       1038 00108$:
      006ECB 7D 51            [12] 1039 	mov	r5,#_process_action_PARM_2
      006ECD 7E 07            [12] 1040 	mov	r6,#(_process_action_PARM_2 >> 8)
      006ECF 8D 82            [24] 1041 	mov	dpl,r5
      006ED1 8E 83            [24] 1042 	mov	dph,r6
      006ED3 E0               [24] 1043 	movx	a,@dptr
      006ED4 70 07            [24] 1044 	jnz	00105$
      006ED6                       1045 00104$:
                                   1046 ;	quantum/action.c:431: add_mods(mods);
      006ED6 8F 82            [24] 1047 	mov	dpl, r7
      006ED8 12 78 6E         [24] 1048 	lcall	_add_mods
      006EDB 80 05            [24] 1049 	sjmp	00106$
      006EDD                       1050 00105$:
                                   1051 ;	quantum/action.c:433: add_weak_mods(mods);
      006EDD 8F 82            [24] 1052 	mov	dpl, r7
      006EDF 12 78 9A         [24] 1053 	lcall	_add_weak_mods
      006EE2                       1054 00106$:
                                   1055 ;	quantum/action.c:435: send_keyboard_report();
      006EE2 12 78 09         [24] 1056 	lcall	_send_keyboard_report
      006EE5                       1057 00110$:
                                   1058 ;	quantum/action.c:437: register_code(action.key.code);
      006EE5 90 07 51         [24] 1059 	mov	dptr,#_process_action_PARM_2
      006EE8 E0               [24] 1060 	movx	a,@dptr
      006EE9 F5 82            [12] 1061 	mov	dpl,a
      006EEB 12 71 80         [24] 1062 	lcall	_register_code
      006EEE 02 71 69         [24] 1063 	ljmp	00180$
      006EF1                       1064 00119$:
                                   1065 ;	quantum/action.c:439: unregister_code(action.key.code);
      006EF1 90 07 51         [24] 1066 	mov	dptr,#_process_action_PARM_2
      006EF4 E0               [24] 1067 	movx	a,@dptr
      006EF5 F5 82            [12] 1068 	mov	dpl,a
      006EF7 C0 07            [24] 1069 	push	ar7
      006EF9 12 72 60         [24] 1070 	lcall	_unregister_code
      006EFC D0 07            [24] 1071 	pop	ar7
                                   1072 ;	quantum/action.c:440: if (mods) {
      006EFE EF               [12] 1073 	mov	a,r7
      006EFF 70 03            [24] 1074 	jnz	00436$
      006F01 02 71 69         [24] 1075 	ljmp	00180$
      006F04                       1076 00436$:
                                   1077 ;	quantum/action.c:441: if (IS_MODIFIER_KEYCODE(action.key.code) || action.key.code == KC_NO) {
      006F04 90 07 51         [24] 1078 	mov	dptr,#_process_action_PARM_2
      006F07 E0               [24] 1079 	movx	a,@dptr
      006F08 FE               [12] 1080 	mov	r6,a
      006F09 BE E0 00         [24] 1081 	cjne	r6,#0xe0,00437$
      006F0C                       1082 00437$:
      006F0C 40 08            [24] 1083 	jc	00115$
      006F0E 90 07 51         [24] 1084 	mov	dptr,#_process_action_PARM_2
      006F11 E0               [24] 1085 	movx	a,@dptr
      006F12 24 18            [12] 1086 	add	a,#0xff - 0xe7
      006F14 50 0B            [24] 1087 	jnc	00111$
                                   1088 ;	free result
      006F16                       1089 00115$:
      006F16 7D 51            [12] 1090 	mov	r5,#_process_action_PARM_2
      006F18 7E 07            [12] 1091 	mov	r6,#(_process_action_PARM_2 >> 8)
      006F1A 8D 82            [24] 1092 	mov	dpl,r5
      006F1C 8E 83            [24] 1093 	mov	dph,r6
      006F1E E0               [24] 1094 	movx	a,@dptr
      006F1F 70 07            [24] 1095 	jnz	00112$
      006F21                       1096 00111$:
                                   1097 ;	quantum/action.c:442: del_mods(mods);
      006F21 8F 82            [24] 1098 	mov	dpl, r7
      006F23 12 78 7D         [24] 1099 	lcall	_del_mods
      006F26 80 05            [24] 1100 	sjmp	00113$
      006F28                       1101 00112$:
                                   1102 ;	quantum/action.c:444: del_weak_mods(mods);
      006F28 8F 82            [24] 1103 	mov	dpl, r7
      006F2A 12 78 A9         [24] 1104 	lcall	_del_weak_mods
      006F2D                       1105 00113$:
                                   1106 ;	quantum/action.c:446: send_keyboard_report();
      006F2D 12 78 09         [24] 1107 	lcall	_send_keyboard_report
                                   1108 ;	quantum/action.c:449: } break;
      006F30 02 71 69         [24] 1109 	ljmp	00180$
                                   1110 ;	quantum/action.c:526: case ACT_USAGE:
      006F33                       1111 00123$:
                                   1112 ;	quantum/action.c:527: switch (action.usage.page) {
      006F33 90 07 52         [24] 1113 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      006F36 E0               [24] 1114 	movx	a,@dptr
      006F37 03               [12] 1115 	rr	a
      006F38 03               [12] 1116 	rr	a
      006F39 54 03            [12] 1117 	anl	a,#0x03
      006F3B FF               [12] 1118 	mov	r7,a
      006F3C 60 08            [24] 1119 	jz	00124$
      006F3E BF 01 02         [24] 1120 	cjne	r7,#0x01,00442$
      006F41 80 23            [24] 1121 	sjmp	00125$
      006F43                       1122 00442$:
      006F43 02 71 69         [24] 1123 	ljmp	00180$
                                   1124 ;	quantum/action.c:528: case PAGE_SYSTEM:
      006F46                       1125 00124$:
                                   1126 ;	quantum/action.c:529: host_system_send(event.pressed ? action.usage.code : 0);
      006F46 90 07 5B         [24] 1127 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      006F49 E0               [24] 1128 	movx	a,@dptr
      006F4A 60 0C            [24] 1129 	jz	00195$
      006F4C 90 07 51         [24] 1130 	mov	dptr,#_process_action_PARM_2
      006F4F E0               [24] 1131 	movx	a,@dptr
      006F50 FE               [12] 1132 	mov	r6,a
      006F51 A3               [24] 1133 	inc	dptr
      006F52 E0               [24] 1134 	movx	a,@dptr
      006F53 54 03            [12] 1135 	anl	a,#0x03
      006F55 FF               [12] 1136 	mov	r7,a
      006F56 80 04            [24] 1137 	sjmp	00196$
      006F58                       1138 00195$:
      006F58 7E 00            [12] 1139 	mov	r6,#0x00
      006F5A 7F 00            [12] 1140 	mov	r7,#0x00
      006F5C                       1141 00196$:
      006F5C 8E 82            [24] 1142 	mov	dpl, r6
      006F5E 8F 83            [24] 1143 	mov	dph, r7
      006F60 12 68 27         [24] 1144 	lcall	_host_system_send
                                   1145 ;	quantum/action.c:530: break;
      006F63 02 71 69         [24] 1146 	ljmp	00180$
                                   1147 ;	quantum/action.c:531: case PAGE_CONSUMER:
      006F66                       1148 00125$:
                                   1149 ;	quantum/action.c:532: host_consumer_send(event.pressed ? action.usage.code : 0);
      006F66 90 07 5B         [24] 1150 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      006F69 E0               [24] 1151 	movx	a,@dptr
      006F6A 60 0C            [24] 1152 	jz	00197$
      006F6C 90 07 51         [24] 1153 	mov	dptr,#_process_action_PARM_2
      006F6F E0               [24] 1154 	movx	a,@dptr
      006F70 FE               [12] 1155 	mov	r6,a
      006F71 A3               [24] 1156 	inc	dptr
      006F72 E0               [24] 1157 	movx	a,@dptr
      006F73 54 03            [12] 1158 	anl	a,#0x03
      006F75 FF               [12] 1159 	mov	r7,a
      006F76 80 04            [24] 1160 	sjmp	00198$
      006F78                       1161 00197$:
      006F78 7E 00            [12] 1162 	mov	r6,#0x00
      006F7A 7F 00            [12] 1163 	mov	r7,#0x00
      006F7C                       1164 00198$:
      006F7C 8E 82            [24] 1165 	mov	dpl, r6
      006F7E 8F 83            [24] 1166 	mov	dph, r7
      006F80 12 68 61         [24] 1167 	lcall	_host_consumer_send
                                   1168 ;	quantum/action.c:535: break;
      006F83 02 71 69         [24] 1169 	ljmp	00180$
                                   1170 ;	quantum/action.c:542: case ACT_LAYER:
      006F86                       1171 00128$:
                                   1172 ;	quantum/action.c:543: if (action.layer_bitop.on == 0) {
      006F86 90 07 52         [24] 1173 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      006F89 E0               [24] 1174 	movx	a,@dptr
      006F8A 54 03            [12] 1175 	anl	a,#0x03
      006F8C 60 03            [24] 1176 	jz	00445$
      006F8E 02 70 14         [24] 1177 	ljmp	00144$
      006F91                       1178 00445$:
                                   1179 ;	quantum/action.c:545: if (!event.pressed) {
      006F91 90 07 5B         [24] 1180 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      006F94 E0               [24] 1181 	movx	a,@dptr
      006F95 60 03            [24] 1182 	jz	00446$
      006F97 02 71 69         [24] 1183 	ljmp	00180$
      006F9A                       1184 00446$:
                                   1185 ;	quantum/action.c:546: uint8_t       shift = action.layer_bitop.part * 4;
      006F9A 90 07 51         [24] 1186 	mov	dptr,#_process_action_PARM_2
      006F9D E0               [24] 1187 	movx	a,@dptr
      006F9E C4               [12] 1188 	swap	a
      006F9F 03               [12] 1189 	rr	a
      006FA0 54 07            [12] 1190 	anl	a,#0x07
      006FA2 25 E0            [12] 1191 	add	a,acc
      006FA4 25 E0            [12] 1192 	add	a,acc
      006FA6 FF               [12] 1193 	mov	r7,a
                                   1194 ;	quantum/action.c:547: layer_state_t bits  = ((layer_state_t)action.layer_bitop.bits) << shift;
      006FA7 90 07 51         [24] 1195 	mov	dptr,#_process_action_PARM_2
      006FAA E0               [24] 1196 	movx	a,@dptr
      006FAB 54 0F            [12] 1197 	anl	a,#0x0f
      006FAD FE               [12] 1198 	mov	r6,a
      006FAE 8F F0            [24] 1199 	mov	b,r7
      006FB0 05 F0            [12] 1200 	inc	b
      006FB2 EE               [12] 1201 	mov	a,r6
      006FB3 80 02            [24] 1202 	sjmp	00448$
      006FB5                       1203 00447$:
      006FB5 25 E0            [12] 1204 	add	a,acc
      006FB7                       1205 00448$:
      006FB7 D5 F0 FB         [24] 1206 	djnz	b,00447$
      006FBA FE               [12] 1207 	mov	r6,a
                                   1208 ;	quantum/action.c:548: layer_state_t mask  = (action.layer_bitop.xbit) ? ~(((layer_state_t)0xf) << shift) : 0;
      006FBB 90 07 51         [24] 1209 	mov	dptr,#_process_action_PARM_2
      006FBE E0               [24] 1210 	movx	a,@dptr
      006FBF 30 E4 11         [24] 1211 	jnb	acc.4,00199$
      006FC2 8F F0            [24] 1212 	mov	b,r7
      006FC4 05 F0            [12] 1213 	inc	b
      006FC6 74 0F            [12] 1214 	mov	a,#0x0f
      006FC8 80 02            [24] 1215 	sjmp	00451$
      006FCA                       1216 00450$:
      006FCA 25 E0            [12] 1217 	add	a,acc
      006FCC                       1218 00451$:
      006FCC D5 F0 FB         [24] 1219 	djnz	b,00450$
      006FCF F4               [12] 1220 	cpl	a
      006FD0 FF               [12] 1221 	mov	r7,a
      006FD1 80 02            [24] 1222 	sjmp	00200$
      006FD3                       1223 00199$:
      006FD3 7F 00            [12] 1224 	mov	r7,#0x00
      006FD5                       1225 00200$:
                                   1226 ;	quantum/action.c:549: switch (action.layer_bitop.op) {
      006FD5 90 07 52         [24] 1227 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      006FD8 E0               [24] 1228 	movx	a,@dptr
      006FD9 03               [12] 1229 	rr	a
      006FDA 03               [12] 1230 	rr	a
      006FDB 54 03            [12] 1231 	anl	a,#0x03
      006FDD FD               [12] 1232 	mov	r5,a
      006FDE 2D               [12] 1233 	add	a,r5
                                   1234 ;	quantum/action.c:550: case OP_BIT_AND:
      006FDF 90 6F E3         [24] 1235 	mov	dptr,#00452$
      006FE2 73               [24] 1236 	jmp	@a+dptr
      006FE3                       1237 00452$:
      006FE3 80 06            [24] 1238 	sjmp	00129$
      006FE5 80 0E            [24] 1239 	sjmp	00130$
      006FE7 80 16            [24] 1240 	sjmp	00131$
      006FE9 80 1E            [24] 1241 	sjmp	00132$
      006FEB                       1242 00129$:
                                   1243 ;	quantum/action.c:551: default_layer_and(bits | mask);
      006FEB EF               [12] 1244 	mov	a,r7
      006FEC 4E               [12] 1245 	orl	a,r6
      006FED F5 82            [12] 1246 	mov	dpl,a
      006FEF 12 74 1A         [24] 1247 	lcall	_default_layer_and
                                   1248 ;	quantum/action.c:552: break;
      006FF2 02 71 69         [24] 1249 	ljmp	00180$
                                   1250 ;	quantum/action.c:553: case OP_BIT_OR:
      006FF5                       1251 00130$:
                                   1252 ;	quantum/action.c:554: default_layer_or(bits | mask);
      006FF5 EF               [12] 1253 	mov	a,r7
      006FF6 4E               [12] 1254 	orl	a,r6
      006FF7 F5 82            [12] 1255 	mov	dpl,a
      006FF9 12 74 07         [24] 1256 	lcall	_default_layer_or
                                   1257 ;	quantum/action.c:555: break;
      006FFC 02 71 69         [24] 1258 	ljmp	00180$
                                   1259 ;	quantum/action.c:556: case OP_BIT_XOR:
      006FFF                       1260 00131$:
                                   1261 ;	quantum/action.c:557: default_layer_xor(bits | mask);
      006FFF EF               [12] 1262 	mov	a,r7
      007000 4E               [12] 1263 	orl	a,r6
      007001 F5 82            [12] 1264 	mov	dpl,a
      007003 12 74 30         [24] 1265 	lcall	_default_layer_xor
                                   1266 ;	quantum/action.c:558: break;
      007006 02 71 69         [24] 1267 	ljmp	00180$
                                   1268 ;	quantum/action.c:559: case OP_BIT_SET:
      007009                       1269 00132$:
                                   1270 ;	quantum/action.c:560: default_layer_set(bits | mask);
      007009 EF               [12] 1271 	mov	a,r7
      00700A 42 06            [12] 1272 	orl	ar6,a
      00700C 8E 82            [24] 1273 	mov	dpl, r6
      00700E 12 73 FB         [24] 1274 	lcall	_default_layer_set
                                   1275 ;	quantum/action.c:562: }
      007011 02 71 69         [24] 1276 	ljmp	00180$
      007014                       1277 00144$:
                                   1278 ;	quantum/action.c:566: if (event.pressed ? (action.layer_bitop.on & ON_PRESS) : (action.layer_bitop.on & ON_RELEASE)) {
      007014 90 07 5B         [24] 1279 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      007017 E0               [24] 1280 	movx	a,@dptr
      007018 60 0C            [24] 1281 	jz	00201$
      00701A 90 07 52         [24] 1282 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      00701D E0               [24] 1283 	movx	a,@dptr
      00701E 54 03            [12] 1284 	anl	a,#0x03
      007020 FF               [12] 1285 	mov	r7,a
      007021 53 07 01         [24] 1286 	anl	ar7,#0x01
      007024 80 0C            [24] 1287 	sjmp	00202$
      007026                       1288 00201$:
      007026 90 07 52         [24] 1289 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      007029 E0               [24] 1290 	movx	a,@dptr
      00702A 54 03            [12] 1291 	anl	a,#0x03
      00702C FE               [12] 1292 	mov	r6,a
      00702D 53 06 02         [24] 1293 	anl	ar6,#0x02
      007030 8E 07            [24] 1294 	mov	ar7,r6
      007032                       1295 00202$:
      007032 EF               [12] 1296 	mov	a,r7
      007033 70 03            [24] 1297 	jnz	00454$
      007035 02 71 69         [24] 1298 	ljmp	00180$
      007038                       1299 00454$:
                                   1300 ;	quantum/action.c:567: uint8_t       shift = action.layer_bitop.part * 4;
      007038 90 07 51         [24] 1301 	mov	dptr,#_process_action_PARM_2
      00703B E0               [24] 1302 	movx	a,@dptr
      00703C C4               [12] 1303 	swap	a
      00703D 03               [12] 1304 	rr	a
      00703E 54 07            [12] 1305 	anl	a,#0x07
      007040 25 E0            [12] 1306 	add	a,acc
      007042 25 E0            [12] 1307 	add	a,acc
      007044 FF               [12] 1308 	mov	r7,a
                                   1309 ;	quantum/action.c:568: layer_state_t bits  = ((layer_state_t)action.layer_bitop.bits) << shift;
      007045 90 07 51         [24] 1310 	mov	dptr,#_process_action_PARM_2
      007048 E0               [24] 1311 	movx	a,@dptr
      007049 54 0F            [12] 1312 	anl	a,#0x0f
      00704B FE               [12] 1313 	mov	r6,a
      00704C 8F F0            [24] 1314 	mov	b,r7
      00704E 05 F0            [12] 1315 	inc	b
      007050 EE               [12] 1316 	mov	a,r6
      007051 80 02            [24] 1317 	sjmp	00456$
      007053                       1318 00455$:
      007053 25 E0            [12] 1319 	add	a,acc
      007055                       1320 00456$:
      007055 D5 F0 FB         [24] 1321 	djnz	b,00455$
      007058 FE               [12] 1322 	mov	r6,a
                                   1323 ;	quantum/action.c:569: layer_state_t mask  = (action.layer_bitop.xbit) ? ~(((layer_state_t)0xf) << shift) : 0;
      007059 90 07 51         [24] 1324 	mov	dptr,#_process_action_PARM_2
      00705C E0               [24] 1325 	movx	a,@dptr
      00705D 30 E4 11         [24] 1326 	jnb	acc.4,00203$
      007060 8F F0            [24] 1327 	mov	b,r7
      007062 05 F0            [12] 1328 	inc	b
      007064 74 0F            [12] 1329 	mov	a,#0x0f
      007066 80 02            [24] 1330 	sjmp	00459$
      007068                       1331 00458$:
      007068 25 E0            [12] 1332 	add	a,acc
      00706A                       1333 00459$:
      00706A D5 F0 FB         [24] 1334 	djnz	b,00458$
      00706D F4               [12] 1335 	cpl	a
      00706E FF               [12] 1336 	mov	r7,a
      00706F 80 02            [24] 1337 	sjmp	00204$
      007071                       1338 00203$:
      007071 7F 00            [12] 1339 	mov	r7,#0x00
      007073                       1340 00204$:
                                   1341 ;	quantum/action.c:570: switch (action.layer_bitop.op) {
      007073 90 07 52         [24] 1342 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      007076 E0               [24] 1343 	movx	a,@dptr
      007077 03               [12] 1344 	rr	a
      007078 03               [12] 1345 	rr	a
      007079 54 03            [12] 1346 	anl	a,#0x03
      00707B FD               [12] 1347 	mov	r5,a
      00707C 2D               [12] 1348 	add	a,r5
                                   1349 ;	quantum/action.c:571: case OP_BIT_AND:
      00707D 90 70 81         [24] 1350 	mov	dptr,#00460$
      007080 73               [24] 1351 	jmp	@a+dptr
      007081                       1352 00460$:
      007081 80 06            [24] 1353 	sjmp	00136$
      007083 80 0E            [24] 1354 	sjmp	00137$
      007085 80 16            [24] 1355 	sjmp	00138$
      007087 80 1E            [24] 1356 	sjmp	00139$
      007089                       1357 00136$:
                                   1358 ;	quantum/action.c:572: layer_and(bits | mask);
      007089 EF               [12] 1359 	mov	a,r7
      00708A 4E               [12] 1360 	orl	a,r6
      00708B F5 82            [12] 1361 	mov	dpl,a
      00708D 12 74 E5         [24] 1362 	lcall	_layer_and
                                   1363 ;	quantum/action.c:573: break;
      007090 02 71 69         [24] 1364 	ljmp	00180$
                                   1365 ;	quantum/action.c:574: case OP_BIT_OR:
      007093                       1366 00137$:
                                   1367 ;	quantum/action.c:575: layer_or(bits | mask);
      007093 EF               [12] 1368 	mov	a,r7
      007094 4E               [12] 1369 	orl	a,r6
      007095 F5 82            [12] 1370 	mov	dpl,a
      007097 12 74 D2         [24] 1371 	lcall	_layer_or
                                   1372 ;	quantum/action.c:576: break;
      00709A 02 71 69         [24] 1373 	ljmp	00180$
                                   1374 ;	quantum/action.c:577: case OP_BIT_XOR:
      00709D                       1375 00138$:
                                   1376 ;	quantum/action.c:578: layer_xor(bits | mask);
      00709D EF               [12] 1377 	mov	a,r7
      00709E 4E               [12] 1378 	orl	a,r6
      00709F F5 82            [12] 1379 	mov	dpl,a
      0070A1 12 74 FB         [24] 1380 	lcall	_layer_xor
                                   1381 ;	quantum/action.c:579: break;
      0070A4 02 71 69         [24] 1382 	ljmp	00180$
                                   1383 ;	quantum/action.c:580: case OP_BIT_SET:
      0070A7                       1384 00139$:
                                   1385 ;	quantum/action.c:581: layer_state_set(bits | mask);
      0070A7 EF               [12] 1386 	mov	a,r7
      0070A8 42 06            [12] 1387 	orl	ar6,a
      0070AA 8E 82            [24] 1388 	mov	dpl, r6
      0070AC 12 74 59         [24] 1389 	lcall	_layer_state_set
                                   1390 ;	quantum/action.c:586: break;
      0070AF 02 71 69         [24] 1391 	ljmp	00180$
                                   1392 ;	quantum/action.c:587: case ACT_LAYER_MODS:
      0070B2                       1393 00146$:
                                   1394 ;	quantum/action.c:588: if (event.pressed) {
      0070B2 90 07 5B         [24] 1395 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      0070B5 E0               [24] 1396 	movx	a,@dptr
      0070B6 60 17            [24] 1397 	jz	00148$
                                   1398 ;	quantum/action.c:589: layer_on(action.layer_mods.layer);
      0070B8 90 07 52         [24] 1399 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      0070BB E0               [24] 1400 	movx	a,@dptr
      0070BC 54 0F            [12] 1401 	anl	a,#0x0f
      0070BE F5 82            [12] 1402 	mov	dpl,a
      0070C0 12 74 91         [24] 1403 	lcall	_layer_on
                                   1404 ;	quantum/action.c:590: register_mods(action.layer_mods.mods);
      0070C3 90 07 51         [24] 1405 	mov	dptr,#_process_action_PARM_2
      0070C6 E0               [24] 1406 	movx	a,@dptr
      0070C7 F5 82            [12] 1407 	mov	dpl,a
      0070C9 12 73 25         [24] 1408 	lcall	_register_mods
      0070CC 02 71 69         [24] 1409 	ljmp	00180$
      0070CF                       1410 00148$:
                                   1411 ;	quantum/action.c:592: unregister_mods(action.layer_mods.mods);
      0070CF 90 07 51         [24] 1412 	mov	dptr,#_process_action_PARM_2
      0070D2 E0               [24] 1413 	movx	a,@dptr
      0070D3 F5 82            [12] 1414 	mov	dpl,a
      0070D5 12 73 39         [24] 1415 	lcall	_unregister_mods
                                   1416 ;	quantum/action.c:593: layer_off(action.layer_mods.layer);
      0070D8 90 07 52         [24] 1417 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      0070DB E0               [24] 1418 	movx	a,@dptr
      0070DC 54 0F            [12] 1419 	anl	a,#0x0f
      0070DE F5 82            [12] 1420 	mov	dpl,a
      0070E0 12 74 B1         [24] 1421 	lcall	_layer_off
                                   1422 ;	quantum/action.c:595: break;
      0070E3 02 71 69         [24] 1423 	ljmp	00180$
                                   1424 ;	quantum/action.c:597: case ACT_LAYER_TAP_EXT:
      0070E6                       1425 00151$:
                                   1426 ;	quantum/action.c:598: switch (action.layer_tap.code) {
      0070E6 90 07 51         [24] 1427 	mov	dptr,#_process_action_PARM_2
      0070E9 E0               [24] 1428 	movx	a,@dptr
      0070EA FF               [12] 1429 	mov	r7,a
      0070EB BF F1 02         [24] 1430 	cjne	r7,#0xf1,00462$
      0070EE 80 0A            [24] 1431 	sjmp	00153$
      0070F0                       1432 00462$:
      0070F0 BF F2 02         [24] 1433 	cjne	r7,#0xf2,00463$
      0070F3 80 1B            [24] 1434 	sjmp	00154$
      0070F5                       1435 00463$:
                                   1436 ;	quantum/action.c:614: momentary_layer_action:
      0070F5 BF F3 41         [24] 1437 	cjne	r7,#0xf3,00159$
      0070F8 80 2C            [24] 1438 	sjmp	00155$
      0070FA                       1439 00153$:
                                   1440 ;	quantum/action.c:615: event.pressed ? layer_on(action.layer_tap.val) : layer_off(action.layer_tap.val);
      0070FA 90 07 5B         [24] 1441 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      0070FD E0               [24] 1442 	movx	a,@dptr
      0070FE 60 08            [24] 1443 	jz	00205$
      007100 12 73 C3         [24] 1444 	lcall	_ak820_outline_0022
      007103 12 74 91         [24] 1445 	lcall	_layer_on
      007106 80 61            [24] 1446 	sjmp	00180$
      007108                       1447 00205$:
      007108 12 73 C3         [24] 1448 	lcall	_ak820_outline_0022
      00710B 12 74 B1         [24] 1449 	lcall	_layer_off
                                   1450 ;	quantum/action.c:616: break;
                                   1451 ;	quantum/action.c:617: case OP_OFF_ON:
      00710E 80 59            [24] 1452 	sjmp	00180$
      007110                       1453 00154$:
                                   1454 ;	quantum/action.c:618: event.pressed ? layer_off(action.layer_tap.val) : layer_on(action.layer_tap.val);
      007110 90 07 5B         [24] 1455 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      007113 E0               [24] 1456 	movx	a,@dptr
      007114 60 08            [24] 1457 	jz	00207$
      007116 12 73 C3         [24] 1458 	lcall	_ak820_outline_0022
      007119 12 74 B1         [24] 1459 	lcall	_layer_off
      00711C 80 4B            [24] 1460 	sjmp	00180$
      00711E                       1461 00207$:
      00711E 12 73 C3         [24] 1462 	lcall	_ak820_outline_0022
      007121 12 74 91         [24] 1463 	lcall	_layer_on
                                   1464 ;	quantum/action.c:619: break;
                                   1465 ;	quantum/action.c:620: case OP_SET_CLEAR:
      007124 80 43            [24] 1466 	sjmp	00180$
      007126                       1467 00155$:
                                   1468 ;	quantum/action.c:621: event.pressed ? layer_move(action.layer_tap.val) : layer_clear();
      007126 90 07 5B         [24] 1469 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      007129 E0               [24] 1470 	movx	a,@dptr
      00712A 60 08            [24] 1471 	jz	00209$
      00712C 12 73 C3         [24] 1472 	lcall	_ak820_outline_0022
      00712F 12 74 78         [24] 1473 	lcall	_layer_move
      007132 80 35            [24] 1474 	sjmp	00180$
      007134                       1475 00209$:
      007134 12 74 72         [24] 1476 	lcall	_layer_clear
                                   1477 ;	quantum/action.c:622: break;
                                   1478 ;	quantum/action.c:668: default:
      007137 80 30            [24] 1479 	sjmp	00180$
      007139                       1480 00159$:
                                   1481 ;	quantum/action.c:675: if (event.pressed) {
      007139 90 07 5B         [24] 1482 	mov	dptr,#(_process_action_event_10000_611 + 0x0005)
      00713C E0               [24] 1483 	movx	a,@dptr
      00713D 60 0B            [24] 1484 	jz	00162$
                                   1485 ;	quantum/action.c:677: register_code(action.layer_tap.code);
      00713F 90 07 51         [24] 1486 	mov	dptr,#_process_action_PARM_2
      007142 E0               [24] 1487 	movx	a,@dptr
      007143 F5 82            [12] 1488 	mov	dpl,a
      007145 12 71 80         [24] 1489 	lcall	_register_code
                                   1490 ;	quantum/action.c:679: ac_dprintf("KEYMAP_TAP_KEY: Tap: unregister_code\n");
      007148 80 1F            [24] 1491 	sjmp	00180$
      00714A                       1492 00162$:
                                   1493 ;	quantum/action.c:680: if (action.layer_tap.code == KC_CAPS) {
      00714A 90 07 51         [24] 1494 	mov	dptr,#_process_action_PARM_2
      00714D E0               [24] 1495 	movx	a,@dptr
      00714E FF               [12] 1496 	mov	r7,a
      00714F BF 39 0E         [24] 1497 	cjne	r7,#0x39,00174$
                                   1498 ;	quantum/action.c:681: wait_ms(TAP_HOLD_CAPS_DELAY);
      007152 7F 50            [12] 1499 	mov	r7,#0x50
      007154                       1500 00186$:
      007154 EF               [12] 1501 	mov	a,r7
      007155 60 09            [24] 1502 	jz	00174$
      007157 90 00 01         [24] 1503 	mov	dptr,#0x0001
      00715A 12 52 5E         [24] 1504 	lcall	_mDelaymS
      00715D 1F               [12] 1505 	dec	r7
                                   1506 ;	quantum/action.c:683: wait_ms(TAP_CODE_DELAY);
      00715E 80 F4            [24] 1507 	sjmp	00186$
      007160                       1508 00174$:
                                   1509 ;	quantum/action.c:685: unregister_code(action.layer_tap.code);
      007160 90 07 51         [24] 1510 	mov	dptr,#_process_action_PARM_2
      007163 E0               [24] 1511 	movx	a,@dptr
      007164 F5 82            [12] 1512 	mov	dpl,a
      007166 12 72 60         [24] 1513 	lcall	_unregister_code
                                   1514 ;	quantum/action.c:768: }
      007169                       1515 00180$:
                                   1516 ;	quantum/action.c:789: switch (action.kind.id) {
      007169 90 07 52         [24] 1517 	mov	dptr,#(_process_action_PARM_2 + 0x0001)
      00716C E0               [24] 1518 	movx	a,@dptr
      00716D C4               [12] 1519 	swap	a
      00716E 54 0F            [12] 1520 	anl	a,#0x0f
      007170 FF               [12] 1521 	mov	r7,a
      007171 BF 08 02         [24] 1522 	cjne	r7,#0x08,00472$
      007174 80 03            [24] 1523 	sjmp	00182$
      007176                       1524 00472$:
      007176 BF 09 06         [24] 1525 	cjne	r7,#0x09,00191$
                                   1526 ;	quantum/action.c:791: case ACT_LAYER_MODS:
      007179                       1527 00182$:
                                   1528 ;	quantum/action.c:796: led_set(host_keyboard_leds());
      007179 12 67 03         [24] 1529 	lcall	_host_keyboard_leds
                                   1530 ;	quantum/action.c:800: }
                                   1531 ;	quantum/action.c:853: }
      00717C 02 90 D3         [24] 1532 	ljmp	_led_set
      00717F                       1533 00191$:
      00717F 22               [24] 1534 	ret
                                   1535 ;------------------------------------------------------------
                                   1536 ;Allocation info for local variables in function 'register_code'
                                   1537 ;------------------------------------------------------------
                                   1538 ;code          Allocated with name '_register_code_code_10000_666'
                                   1539 ;__700000088   Allocated with name '_register_code___700000088_70000_683'
                                   1540 ;key           Allocated with name '_register_code_key_80000_684'
                                   1541 ;__500000090   Allocated with name '_register_code___500000090_50000_686'
                                   1542 ;key           Allocated with name '_register_code_key_60000_687'
                                   1543 ;__700000092   Allocated with name '_register_code___700000092_70000_678'
                                   1544 ;__700000093   Allocated with name '_register_code___700000093_70000_689'
                                   1545 ;key           Allocated with name '_register_code_key_80000_690'
                                   1546 ;------------------------------------------------------------
                                   1547 ;	quantum/action.c:859: __attribute__((weak)) void register_code(uint8_t code) {
                                   1548 ;	-----------------------------------------
                                   1549 ;	 function register_code
                                   1550 ;	-----------------------------------------
      007180                       1551 _register_code:
      007180 E5 82            [12] 1552 	mov	a,dpl
      007182 90 07 5C         [24] 1553 	mov	dptr,#_register_code_code_10000_666
      007185 F0               [24] 1554 	movx	@dptr,a
                                   1555 ;	quantum/action.c:860: if (code == KC_NO) {
      007186 E0               [24] 1556 	movx	a,@dptr
      007187 FF               [12] 1557 	mov	r7,a
      007188 70 01            [24] 1558 	jnz	00125$
                                   1559 ;	quantum/action.c:861: return;
      00718A 22               [24] 1560 	ret
      00718B                       1561 00125$:
                                   1562 ;	quantum/action.c:896: } else if (IS_BASIC_KEYCODE(code)) {
      00718B BF 04 00         [24] 1563 	cjne	r7,#0x04,00231$
      00718E                       1564 00231$:
      00718E 40 40            [24] 1565 	jc	00121$
      007190 EF               [12] 1566 	mov	a,r7
      007191 24 5B            [12] 1567 	add	a,#0xff - 0xa4
      007193 40 3B            [24] 1568 	jc	00121$
                                   1569 ;	free result
                                   1570 ;	quantum/action.c:903: if (is_key_pressed(keyboard_report, code)) {
      007195 90 07 12         [24] 1571 	mov	dptr,#_is_key_pressed_PARM_2
      007198 EF               [12] 1572 	mov	a,r7
      007199 F0               [24] 1573 	movx	@dptr,a
      00719A 90 0B B0         [24] 1574 	mov	dptr,#_actual_keyboard_report
      00719D 75 F0 00         [24] 1575 	mov	b, #0x00
      0071A0 C0 07            [24] 1576 	push	ar7
      0071A2 12 68 FD         [24] 1577 	lcall	_is_key_pressed
      0071A5 E5 82            [12] 1578 	mov	a, dpl
      0071A7 D0 07            [24] 1579 	pop	ar7
      0071A9 60 11            [24] 1580 	jz	00104$
                                   1581 ;	quantum/action_util.h:43: del_key_from_report(keyboard_report, key);
      0071AB 90 07 2B         [24] 1582 	mov	dptr,#_del_key_from_report_PARM_2
      0071AE EF               [12] 1583 	mov	a,r7
      0071AF F0               [24] 1584 	movx	@dptr,a
      0071B0 90 0B B0         [24] 1585 	mov	dptr,#_actual_keyboard_report
      0071B3 75 F0 00         [24] 1586 	mov	b, #0x00
      0071B6 12 6B BA         [24] 1587 	lcall	_del_key_from_report
                                   1588 ;	quantum/action.c:905: send_keyboard_report();
      0071B9 12 78 09         [24] 1589 	lcall	_send_keyboard_report
      0071BC                       1590 00104$:
                                   1591 ;	quantum/action.c:907: add_key(code);
      0071BC 90 07 5C         [24] 1592 	mov	dptr,#_register_code_code_10000_666
      0071BF E0               [24] 1593 	movx	a,@dptr
                                   1594 ;	quantum/action_util.h:39: add_key_to_report(keyboard_report, key);
      0071C0 90 07 27         [24] 1595 	mov	dptr,#_add_key_to_report_PARM_2
      0071C3 F0               [24] 1596 	movx	@dptr,a
      0071C4 90 0B B0         [24] 1597 	mov	dptr,#_actual_keyboard_report
      0071C7 75 F0 00         [24] 1598 	mov	b, #0x00
      0071CA 12 6B 65         [24] 1599 	lcall	_add_key_to_report
                                   1600 ;	quantum/action.c:908: send_keyboard_report();
      0071CD 02 78 09         [24] 1601 	ljmp	_send_keyboard_report
      0071D0                       1602 00121$:
                                   1603 ;	quantum/action.c:909: } else if (IS_MODIFIER_KEYCODE(code)) {
      0071D0 90 07 5C         [24] 1604 	mov	dptr,#_register_code_code_10000_666
      0071D3 E0               [24] 1605 	movx	a,@dptr
      0071D4 FF               [12] 1606 	mov	r7,a
      0071D5 BF E0 00         [24] 1607 	cjne	r7,#0xe0,00235$
      0071D8                       1608 00235$:
      0071D8 40 1D            [24] 1609 	jc	00117$
      0071DA EF               [12] 1610 	mov	a,r7
      0071DB 24 18            [12] 1611 	add	a,#0xff - 0xe7
      0071DD 40 18            [24] 1612 	jc	00117$
                                   1613 ;	free result
                                   1614 ;	quantum/action.c:910: add_mods(MOD_BIT(code));
      0071DF 74 07            [12] 1615 	mov	a,#0x07
      0071E1 5F               [12] 1616 	anl	a,r7
      0071E2 F5 F0            [12] 1617 	mov	b,a
      0071E4 05 F0            [12] 1618 	inc	b
      0071E6 74 01            [12] 1619 	mov	a,#0x01
      0071E8 80 02            [24] 1620 	sjmp	00239$
      0071EA                       1621 00238$:
      0071EA 25 E0            [12] 1622 	add	a,acc
      0071EC                       1623 00239$:
      0071EC D5 F0 FB         [24] 1624 	djnz	b,00238$
      0071EF F5 82            [12] 1625 	mov	dpl,a
      0071F1 12 78 6E         [24] 1626 	lcall	_add_mods
                                   1627 ;	quantum/action.c:911: send_keyboard_report();
      0071F4 02 78 09         [24] 1628 	ljmp	_send_keyboard_report
      0071F7                       1629 00117$:
                                   1630 ;	quantum/action.c:914: } else if (IS_SYSTEM_KEYCODE(code)) {
      0071F7 90 07 5C         [24] 1631 	mov	dptr,#_register_code_code_10000_666
      0071FA E0               [24] 1632 	movx	a,@dptr
      0071FB FF               [12] 1633 	mov	r7,a
      0071FC BF A5 00         [24] 1634 	cjne	r7,#0xa5,00240$
      0071FF                       1635 00240$:
      0071FF 40 45            [24] 1636 	jc	00113$
      007201 EF               [12] 1637 	mov	a,r7
      007202 24 58            [12] 1638 	add	a,#0xff - 0xa7
      007204 40 40            [24] 1639 	jc	00113$
                                   1640 ;	free result
                                   1641 ;	tmk_core/protocol/report.h:263: switch (key) {
      007206 BF A5 02         [24] 1642 	cjne	r7,#0xa5,00243$
      007209 80 0A            [24] 1643 	sjmp	00129$
      00720B                       1644 00243$:
      00720B BF A6 02         [24] 1645 	cjne	r7,#0xa6,00244$
      00720E 80 10            [24] 1646 	sjmp	00130$
      007210                       1647 00244$:
                                   1648 ;	tmk_core/protocol/report.h:264: case KC_SYSTEM_POWER:
      007210 BF A7 23         [24] 1649 	cjne	r7,#0xa7,00132$
      007213 80 16            [24] 1650 	sjmp	00131$
      007215                       1651 00129$:
                                   1652 ;	tmk_core/protocol/report.h:265: return SYSTEM_POWER_DOWN;
      007215 90 07 5D         [24] 1653 	mov	dptr,#_register_code___700000092_70000_678
      007218 74 81            [12] 1654 	mov	a,#0x81
      00721A F0               [24] 1655 	movx	@dptr,a
      00721B E4               [12] 1656 	clr	a
      00721C A3               [24] 1657 	inc	dptr
      00721D F0               [24] 1658 	movx	@dptr,a
                                   1659 ;	tmk_core/protocol/report.h:266: case KC_SYSTEM_SLEEP:
      00721E 80 1D            [24] 1660 	sjmp	00134$
      007220                       1661 00130$:
                                   1662 ;	tmk_core/protocol/report.h:267: return SYSTEM_SLEEP;
      007220 90 07 5D         [24] 1663 	mov	dptr,#_register_code___700000092_70000_678
      007223 74 82            [12] 1664 	mov	a,#0x82
      007225 F0               [24] 1665 	movx	@dptr,a
      007226 E4               [12] 1666 	clr	a
      007227 A3               [24] 1667 	inc	dptr
      007228 F0               [24] 1668 	movx	@dptr,a
                                   1669 ;	tmk_core/protocol/report.h:268: case KC_SYSTEM_WAKE:
      007229 80 12            [24] 1670 	sjmp	00134$
      00722B                       1671 00131$:
                                   1672 ;	tmk_core/protocol/report.h:269: return SYSTEM_WAKE_UP;
      00722B 90 07 5D         [24] 1673 	mov	dptr,#_register_code___700000092_70000_678
      00722E 74 83            [12] 1674 	mov	a,#0x83
      007230 F0               [24] 1675 	movx	@dptr,a
      007231 E4               [12] 1676 	clr	a
      007232 A3               [24] 1677 	inc	dptr
      007233 F0               [24] 1678 	movx	@dptr,a
                                   1679 ;	tmk_core/protocol/report.h:270: default:
      007234 80 07            [24] 1680 	sjmp	00134$
      007236                       1681 00132$:
                                   1682 ;	tmk_core/protocol/report.h:271: return 0;
      007236 90 07 5D         [24] 1683 	mov	dptr,#_register_code___700000092_70000_678
      007239 E4               [12] 1684 	clr	a
      00723A F0               [24] 1685 	movx	@dptr,a
      00723B A3               [24] 1686 	inc	dptr
      00723C F0               [24] 1687 	movx	@dptr,a
                                   1688 ;	quantum/action.c:915: host_system_send(KEYCODE2SYSTEM(code));
      00723D                       1689 00134$:
      00723D 90 07 5D         [24] 1690 	mov	dptr,#_register_code___700000092_70000_678
      007240 12 73 B0         [24] 1691 	lcall	_ak820_outline_0013
      007243 02 68 27         [24] 1692 	ljmp	_host_system_send
      007246                       1693 00113$:
                                   1694 ;	quantum/action.c:916: } else if (IS_CONSUMER_KEYCODE(code)) {
      007246 90 07 5C         [24] 1695 	mov	dptr,#_register_code_code_10000_666
      007249 E0               [24] 1696 	movx	a,@dptr
      00724A FF               [12] 1697 	mov	r7,a
      00724B BF A8 00         [24] 1698 	cjne	r7,#0xa8,00246$
      00724E                       1699 00246$:
      00724E 40 0F            [24] 1700 	jc	00135$
      007250 EF               [12] 1701 	mov	a,r7
      007251 24 3D            [12] 1702 	add	a,#0xff - 0xc2
      007253 40 0A            [24] 1703 	jc	00135$
                                   1704 ;	free result
                                   1705 ;	quantum/action.c:917: host_consumer_send(KEYCODE2CONSUMER(code));
      007255 8F 82            [24] 1706 	mov	dpl, r7
      007257 12 68 B3         [24] 1707 	lcall	_KEYCODE2CONSUMER
      00725A AF 83            [24] 1708 	mov  r7,dph
                                   1709 ;	quantum/action.c:921: register_mouse(code, true);
                                   1710 ;	quantum/action.c:923: }
      00725C 02 68 61         [24] 1711 	ljmp	_host_consumer_send
      00725F                       1712 00135$:
      00725F 22               [24] 1713 	ret
                                   1714 ;------------------------------------------------------------
                                   1715 ;Allocation info for local variables in function 'unregister_code'
                                   1716 ;------------------------------------------------------------
                                   1717 ;code          Allocated with name '_unregister_code_code_10000_693'
                                   1718 ;__500000095   Allocated with name '_unregister_code___500000095_50000_707'
                                   1719 ;key           Allocated with name '_unregister_code_key_60000_708'
                                   1720 ;------------------------------------------------------------
                                   1721 ;	quantum/action.c:929: __attribute__((weak)) void unregister_code(uint8_t code) {
                                   1722 ;	-----------------------------------------
                                   1723 ;	 function unregister_code
                                   1724 ;	-----------------------------------------
      007260                       1725 _unregister_code:
      007260 E5 82            [12] 1726 	mov	a,dpl
      007262 90 07 60         [24] 1727 	mov	dptr,#_unregister_code_code_10000_693
      007265 F0               [24] 1728 	movx	@dptr,a
                                   1729 ;	quantum/action.c:930: if (code == KC_NO) {
      007266 E0               [24] 1730 	movx	a,@dptr
      007267 FF               [12] 1731 	mov	r7,a
      007268 70 01            [24] 1732 	jnz	00121$
                                   1733 ;	quantum/action.c:931: return;
      00726A 22               [24] 1734 	ret
      00726B                       1735 00121$:
                                   1736 ;	quantum/action.c:963: } else if (IS_BASIC_KEYCODE(code)) {
      00726B BF 04 00         [24] 1737 	cjne	r7,#0x04,00192$
      00726E                       1738 00192$:
      00726E 40 16            [24] 1739 	jc	00117$
      007270 EF               [12] 1740 	mov	a,r7
      007271 24 5B            [12] 1741 	add	a,#0xff - 0xa4
      007273 40 11            [24] 1742 	jc	00117$
                                   1743 ;	free result
                                   1744 ;	quantum/action_util.h:43: del_key_from_report(keyboard_report, key);
      007275 90 07 2B         [24] 1745 	mov	dptr,#_del_key_from_report_PARM_2
      007278 EF               [12] 1746 	mov	a,r7
      007279 F0               [24] 1747 	movx	@dptr,a
      00727A 90 0B B0         [24] 1748 	mov	dptr,#_actual_keyboard_report
      00727D 75 F0 00         [24] 1749 	mov	b, #0x00
      007280 12 6B BA         [24] 1750 	lcall	_del_key_from_report
                                   1751 ;	quantum/action.c:965: send_keyboard_report();
      007283 02 78 09         [24] 1752 	ljmp	_send_keyboard_report
      007286                       1753 00117$:
                                   1754 ;	quantum/action.c:966: } else if (IS_MODIFIER_KEYCODE(code)) {
      007286 90 07 60         [24] 1755 	mov	dptr,#_unregister_code_code_10000_693
      007289 E0               [24] 1756 	movx	a,@dptr
      00728A FF               [12] 1757 	mov	r7,a
      00728B BF E0 00         [24] 1758 	cjne	r7,#0xe0,00195$
      00728E                       1759 00195$:
      00728E 40 1D            [24] 1760 	jc	00113$
      007290 EF               [12] 1761 	mov	a,r7
      007291 24 18            [12] 1762 	add	a,#0xff - 0xe7
      007293 40 18            [24] 1763 	jc	00113$
                                   1764 ;	free result
                                   1765 ;	quantum/action.c:967: del_mods(MOD_BIT(code));
      007295 74 07            [12] 1766 	mov	a,#0x07
      007297 5F               [12] 1767 	anl	a,r7
      007298 F5 F0            [12] 1768 	mov	b,a
      00729A 05 F0            [12] 1769 	inc	b
      00729C 74 01            [12] 1770 	mov	a,#0x01
      00729E 80 02            [24] 1771 	sjmp	00199$
      0072A0                       1772 00198$:
      0072A0 25 E0            [12] 1773 	add	a,acc
      0072A2                       1774 00199$:
      0072A2 D5 F0 FB         [24] 1775 	djnz	b,00198$
      0072A5 F5 82            [12] 1776 	mov	dpl,a
      0072A7 12 78 7D         [24] 1777 	lcall	_del_mods
                                   1778 ;	quantum/action.c:968: send_keyboard_report();
      0072AA 02 78 09         [24] 1779 	ljmp	_send_keyboard_report
      0072AD                       1780 00113$:
                                   1781 ;	quantum/action.c:971: } else if (IS_SYSTEM_KEYCODE(code)) {
      0072AD 90 07 60         [24] 1782 	mov	dptr,#_unregister_code_code_10000_693
      0072B0 E0               [24] 1783 	movx	a,@dptr
      0072B1 FF               [12] 1784 	mov	r7,a
      0072B2 BF A5 00         [24] 1785 	cjne	r7,#0xa5,00200$
      0072B5                       1786 00200$:
      0072B5 40 0B            [24] 1787 	jc	00109$
      0072B7 EF               [12] 1788 	mov	a,r7
      0072B8 24 58            [12] 1789 	add	a,#0xff - 0xa7
      0072BA 40 06            [24] 1790 	jc	00109$
                                   1791 ;	free result
                                   1792 ;	quantum/action.c:972: host_system_send(0);
      0072BC 90 00 00         [24] 1793 	mov	dptr,#0x0000
      0072BF 02 68 27         [24] 1794 	ljmp	_host_system_send
      0072C2                       1795 00109$:
                                   1796 ;	quantum/action.c:973: } else if (IS_CONSUMER_KEYCODE(code)) {
      0072C2 90 07 60         [24] 1797 	mov	dptr,#_unregister_code_code_10000_693
      0072C5 E0               [24] 1798 	movx	a,@dptr
      0072C6 FF               [12] 1799 	mov	r7,a
      0072C7 BF A8 00         [24] 1800 	cjne	r7,#0xa8,00203$
      0072CA                       1801 00203$:
      0072CA 40 0B            [24] 1802 	jc	00124$
      0072CC EF               [12] 1803 	mov	a,r7
      0072CD 24 3D            [12] 1804 	add	a,#0xff - 0xc2
      0072CF 40 06            [24] 1805 	jc	00124$
                                   1806 ;	free result
                                   1807 ;	quantum/action.c:974: host_consumer_send(0);
      0072D1 90 00 00         [24] 1808 	mov	dptr,#0x0000
                                   1809 ;	quantum/action.c:978: register_mouse(code, false);
                                   1810 ;	quantum/action.c:980: }
      0072D4 02 68 61         [24] 1811 	ljmp	_host_consumer_send
      0072D7                       1812 00124$:
      0072D7 22               [24] 1813 	ret
                                   1814 ;------------------------------------------------------------
                                   1815 ;Allocation info for local variables in function 'tap_code_delay'
                                   1816 ;------------------------------------------------------------
                                   1817 ;delay         Allocated with name '_tap_code_delay_PARM_2'
                                   1818 ;code          Allocated with name '_tap_code_delay_code_10000_710'
                                   1819 ;i             Allocated with name '_tap_code_delay_i_20000_712'
                                   1820 ;i             Allocated with name '_tap_code_delay_i_50000_715'
                                   1821 ;------------------------------------------------------------
                                   1822 ;	quantum/action.c:987: __attribute__((weak)) void tap_code_delay(uint8_t code, uint16_t delay) {
                                   1823 ;	-----------------------------------------
                                   1824 ;	 function tap_code_delay
                                   1825 ;	-----------------------------------------
      0072D8                       1826 _tap_code_delay:
      0072D8 E5 82            [12] 1827 	mov	a,dpl
      0072DA 90 07 63         [24] 1828 	mov	dptr,#_tap_code_delay_code_10000_710
      0072DD F0               [24] 1829 	movx	@dptr,a
                                   1830 ;	quantum/action.c:988: register_code(code);
      0072DE E0               [24] 1831 	movx	a,@dptr
      0072DF FF               [12] 1832 	mov	r7,a
      0072E0 F5 82            [12] 1833 	mov	dpl,a
      0072E2 C0 07            [24] 1834 	push	ar7
      0072E4 12 71 80         [24] 1835 	lcall	_register_code
      0072E7 D0 07            [24] 1836 	pop	ar7
                                   1837 ;	quantum/action.c:989: for (uint16_t i = delay; i > 0; i--) {
      0072E9 90 07 61         [24] 1838 	mov	dptr,#_tap_code_delay_PARM_2
      0072EC E0               [24] 1839 	movx	a,@dptr
      0072ED FD               [12] 1840 	mov	r5,a
      0072EE A3               [24] 1841 	inc	dptr
      0072EF E0               [24] 1842 	movx	a,@dptr
      0072F0 FE               [12] 1843 	mov	r6,a
      0072F1                       1844 00110$:
      0072F1 ED               [12] 1845 	mov	a,r5
      0072F2 4E               [12] 1846 	orl	a,r6
      0072F3 60 0D            [24] 1847 	jz	00105$
                                   1848 ;	quantum/action.c:990: wait_ms(1);
      0072F5 90 00 01         [24] 1849 	mov	dptr,#0x0001
      0072F8 12 52 5E         [24] 1850 	lcall	_mDelaymS
                                   1851 ;	quantum/action.c:989: for (uint16_t i = delay; i > 0; i--) {
      0072FB 1D               [12] 1852 	dec	r5
      0072FC BD FF 01         [24] 1853 	cjne	r5,#0xff,00141$
      0072FF 1E               [12] 1854 	dec	r6
      007300                       1855 00141$:
      007300 80 EF            [24] 1856 	sjmp	00110$
      007302                       1857 00105$:
                                   1858 ;	quantum/action.c:992: unregister_code(code);
      007302 8F 82            [24] 1859 	mov	dpl, r7
                                   1860 ;	quantum/action.c:993: }
      007304 02 72 60         [24] 1861 	ljmp	_unregister_code
                                   1862 ;------------------------------------------------------------
                                   1863 ;Allocation info for local variables in function 'tap_code'
                                   1864 ;------------------------------------------------------------
                                   1865 ;code          Allocated with name '_tap_code_code_10000_717'
                                   1866 ;------------------------------------------------------------
                                   1867 ;	quantum/action.c:999: __attribute__((weak)) void tap_code(uint8_t code) {
                                   1868 ;	-----------------------------------------
                                   1869 ;	 function tap_code
                                   1870 ;	-----------------------------------------
      007307                       1871 _tap_code:
      007307 E5 82            [12] 1872 	mov	a,dpl
      007309 90 07 64         [24] 1873 	mov	dptr,#_tap_code_code_10000_717
      00730C F0               [24] 1874 	movx	@dptr,a
                                   1875 ;	quantum/action.c:1000: tap_code_delay(code, code == KC_CAPS ? QS_tap_hold_caps_delay : QS_tap_code_delay);
      00730D E0               [24] 1876 	movx	a,@dptr
      00730E FF               [12] 1877 	mov	r7,a
      00730F BF 39 04         [24] 1878 	cjne	r7,#0x39,00103$
      007312 7E 50            [12] 1879 	mov	r6,#0x50
      007314 80 02            [24] 1880 	sjmp	00104$
      007316                       1881 00103$:
      007316 7E 00            [12] 1882 	mov	r6,#0x00
      007318                       1883 00104$:
      007318 90 07 61         [24] 1884 	mov	dptr,#_tap_code_delay_PARM_2
      00731B EE               [12] 1885 	mov	a,r6
      00731C F0               [24] 1886 	movx	@dptr,a
      00731D E4               [12] 1887 	clr	a
      00731E A3               [24] 1888 	inc	dptr
      00731F F0               [24] 1889 	movx	@dptr,a
      007320 8F 82            [24] 1890 	mov	dpl, r7
                                   1891 ;	quantum/action.c:1001: }
      007322 02 72 D8         [24] 1892 	ljmp	_tap_code_delay
                                   1893 ;------------------------------------------------------------
                                   1894 ;Allocation info for local variables in function 'register_mods'
                                   1895 ;------------------------------------------------------------
                                   1896 ;mods          Allocated with name '_register_mods_mods_10000_719'
                                   1897 ;------------------------------------------------------------
                                   1898 ;	quantum/action.c:1007: __attribute__((weak)) void register_mods(uint8_t mods) {
                                   1899 ;	-----------------------------------------
                                   1900 ;	 function register_mods
                                   1901 ;	-----------------------------------------
      007325                       1902 _register_mods:
      007325 E5 82            [12] 1903 	mov	a,dpl
      007327 90 07 65         [24] 1904 	mov	dptr,#_register_mods_mods_10000_719
      00732A F0               [24] 1905 	movx	@dptr,a
                                   1906 ;	quantum/action.c:1008: if (mods) {
      00732B E0               [24] 1907 	movx	a,@dptr
      00732C FF               [12] 1908 	mov	r7,a
      00732D E0               [24] 1909 	movx	a,@dptr
      00732E 60 08            [24] 1910 	jz	00103$
                                   1911 ;	quantum/action.c:1009: add_mods(mods);
      007330 8F 82            [24] 1912 	mov	dpl, r7
      007332 12 78 6E         [24] 1913 	lcall	_add_mods
                                   1914 ;	quantum/action.c:1010: send_keyboard_report();
                                   1915 ;	quantum/action.c:1012: }
      007335 02 78 09         [24] 1916 	ljmp	_send_keyboard_report
      007338                       1917 00103$:
      007338 22               [24] 1918 	ret
                                   1919 ;------------------------------------------------------------
                                   1920 ;Allocation info for local variables in function 'unregister_mods'
                                   1921 ;------------------------------------------------------------
                                   1922 ;mods          Allocated with name '_unregister_mods_mods_10000_723'
                                   1923 ;------------------------------------------------------------
                                   1924 ;	quantum/action.c:1018: __attribute__((weak)) void unregister_mods(uint8_t mods) {
                                   1925 ;	-----------------------------------------
                                   1926 ;	 function unregister_mods
                                   1927 ;	-----------------------------------------
      007339                       1928 _unregister_mods:
      007339 E5 82            [12] 1929 	mov	a,dpl
      00733B 90 07 66         [24] 1930 	mov	dptr,#_unregister_mods_mods_10000_723
      00733E F0               [24] 1931 	movx	@dptr,a
                                   1932 ;	quantum/action.c:1019: if (mods) {
      00733F E0               [24] 1933 	movx	a,@dptr
      007340 FF               [12] 1934 	mov	r7,a
      007341 E0               [24] 1935 	movx	a,@dptr
      007342 60 08            [24] 1936 	jz	00103$
                                   1937 ;	quantum/action.c:1020: del_mods(mods);
      007344 8F 82            [24] 1938 	mov	dpl, r7
      007346 12 78 7D         [24] 1939 	lcall	_del_mods
                                   1940 ;	quantum/action.c:1021: send_keyboard_report();
                                   1941 ;	quantum/action.c:1023: }
      007349 02 78 09         [24] 1942 	ljmp	_send_keyboard_report
      00734C                       1943 00103$:
      00734C 22               [24] 1944 	ret
                                   1945 ;------------------------------------------------------------
                                   1946 ;Allocation info for local variables in function 'register_weak_mods'
                                   1947 ;------------------------------------------------------------
                                   1948 ;mods          Allocated with name '_register_weak_mods_mods_10000_727'
                                   1949 ;------------------------------------------------------------
                                   1950 ;	quantum/action.c:1029: __attribute__((weak)) void register_weak_mods(uint8_t mods) {
                                   1951 ;	-----------------------------------------
                                   1952 ;	 function register_weak_mods
                                   1953 ;	-----------------------------------------
      00734D                       1954 _register_weak_mods:
      00734D E5 82            [12] 1955 	mov	a,dpl
      00734F 90 07 67         [24] 1956 	mov	dptr,#_register_weak_mods_mods_10000_727
      007352 F0               [24] 1957 	movx	@dptr,a
                                   1958 ;	quantum/action.c:1030: if (mods) {
      007353 E0               [24] 1959 	movx	a,@dptr
      007354 FF               [12] 1960 	mov	r7,a
      007355 E0               [24] 1961 	movx	a,@dptr
      007356 60 08            [24] 1962 	jz	00103$
                                   1963 ;	quantum/action.c:1031: add_weak_mods(mods);
      007358 8F 82            [24] 1964 	mov	dpl, r7
      00735A 12 78 9A         [24] 1965 	lcall	_add_weak_mods
                                   1966 ;	quantum/action.c:1032: send_keyboard_report();
                                   1967 ;	quantum/action.c:1034: }
      00735D 02 78 09         [24] 1968 	ljmp	_send_keyboard_report
      007360                       1969 00103$:
      007360 22               [24] 1970 	ret
                                   1971 ;------------------------------------------------------------
                                   1972 ;Allocation info for local variables in function 'unregister_weak_mods'
                                   1973 ;------------------------------------------------------------
                                   1974 ;mods          Allocated with name '_unregister_weak_mods_mods_10000_731'
                                   1975 ;------------------------------------------------------------
                                   1976 ;	quantum/action.c:1040: __attribute__((weak)) void unregister_weak_mods(uint8_t mods) {
                                   1977 ;	-----------------------------------------
                                   1978 ;	 function unregister_weak_mods
                                   1979 ;	-----------------------------------------
      007361                       1980 _unregister_weak_mods:
      007361 E5 82            [12] 1981 	mov	a,dpl
      007363 90 07 68         [24] 1982 	mov	dptr,#_unregister_weak_mods_mods_10000_731
      007366 F0               [24] 1983 	movx	@dptr,a
                                   1984 ;	quantum/action.c:1041: if (mods) {
      007367 E0               [24] 1985 	movx	a,@dptr
      007368 FF               [12] 1986 	mov	r7,a
      007369 E0               [24] 1987 	movx	a,@dptr
      00736A 60 08            [24] 1988 	jz	00103$
                                   1989 ;	quantum/action.c:1042: del_weak_mods(mods);
      00736C 8F 82            [24] 1990 	mov	dpl, r7
      00736E 12 78 A9         [24] 1991 	lcall	_del_weak_mods
                                   1992 ;	quantum/action.c:1043: send_keyboard_report();
                                   1993 ;	quantum/action.c:1045: }
      007371 02 78 09         [24] 1994 	ljmp	_send_keyboard_report
      007374                       1995 00103$:
      007374 22               [24] 1996 	ret
                                   1997 ;------------------------------------------------------------
                                   1998 ;Allocation info for local variables in function 'clear_keyboard'
                                   1999 ;------------------------------------------------------------
                                   2000 ;	quantum/action.c:1051: void clear_keyboard(void) {
                                   2001 ;	-----------------------------------------
                                   2002 ;	 function clear_keyboard
                                   2003 ;	-----------------------------------------
      007375                       2004 _clear_keyboard:
                                   2005 ;	quantum/action.c:1052: clear_mods();
      007375 12 78 8D         [24] 2006 	lcall	_clear_mods
                                   2007 ;	quantum/action.c:1053: clear_keyboard_but_mods();
                                   2008 ;	quantum/action.c:1054: }
      007378 02 73 7B         [24] 2009 	ljmp	_clear_keyboard_but_mods
                                   2010 ;------------------------------------------------------------
                                   2011 ;Allocation info for local variables in function 'clear_keyboard_but_mods'
                                   2012 ;------------------------------------------------------------
                                   2013 ;	quantum/action.c:1060: void clear_keyboard_but_mods(void) {
                                   2014 ;	-----------------------------------------
                                   2015 ;	 function clear_keyboard_but_mods
                                   2016 ;	-----------------------------------------
      00737B                       2017 _clear_keyboard_but_mods:
                                   2018 ;	quantum/action_util.h:47: clear_keys_from_report(keyboard_report);
      00737B 90 0B B0         [24] 2019 	mov	dptr,#_actual_keyboard_report
      00737E 75 F0 00         [24] 2020 	mov	b, #0x00
      007381 12 6C 0F         [24] 2021 	lcall	_clear_keys_from_report
                                   2022 ;	quantum/action.c:1062: clear_keyboard_but_mods_and_keys();
                                   2023 ;	quantum/action.c:1063: }
      007384 02 73 87         [24] 2024 	ljmp	_clear_keyboard_but_mods_and_keys
                                   2025 ;------------------------------------------------------------
                                   2026 ;Allocation info for local variables in function 'clear_keyboard_but_mods_and_keys'
                                   2027 ;------------------------------------------------------------
                                   2028 ;	quantum/action.c:1069: void clear_keyboard_but_mods_and_keys(void) {
                                   2029 ;	-----------------------------------------
                                   2030 ;	 function clear_keyboard_but_mods_and_keys
                                   2031 ;	-----------------------------------------
      007387                       2032 _clear_keyboard_but_mods_and_keys:
                                   2033 ;	quantum/action.c:1071: host_system_send(0);
      007387 90 00 00         [24] 2034 	mov	dptr,#0x0000
      00738A 12 68 27         [24] 2035 	lcall	_host_system_send
                                   2036 ;	quantum/action.c:1072: host_consumer_send(0);
      00738D 90 00 00         [24] 2037 	mov	dptr,#0x0000
      007390 12 68 61         [24] 2038 	lcall	_host_consumer_send
                                   2039 ;	quantum/action.c:1074: clear_weak_mods();
      007393 12 78 B9         [24] 2040 	lcall	_clear_weak_mods
                                   2041 ;	quantum/action.c:1075: send_keyboard_report();
                                   2042 ;	quantum/action.c:1083: }
      007396 02 78 09         [24] 2043 	ljmp	_send_keyboard_report
                                   2044 ;------------------------------------------------------------
                                   2045 ;Allocation info for local variables in function 'is_tap_record'
                                   2046 ;------------------------------------------------------------
                                   2047 ;record        Allocated with name '_is_tap_record_record_10000_744'
                                   2048 ;action        Allocated with name '_is_tap_record_action_10001_748'
                                   2049 ;------------------------------------------------------------
                                   2050 ;	quantum/action.c:1089: bool is_tap_record(keyrecord_t *record) {
                                   2051 ;	-----------------------------------------
                                   2052 	.area CSEG    (CODE)
                                   2053 	.area CONST   (CODE)
                                   2054 	.area XINIT   (CODE)
      00BD6A                       2055 __xinit__disable_action_cache:
      00BD6A 00                    2056 	.db #0x00	;  0
                                   2057 	.area CABS    (ABS,CODE)
                                   2058 
                                   2059 ; Experimental exact instruction outlining.
                                   2060 	.globl _ak820_outline_0002
                                   2061 	.globl _ak820_outline_0009
                                   2062 	.globl _ak820_outline_0013
                                   2063 	.globl _ak820_outline_0015
                                   2064 	.globl _ak820_outline_0022
                                   2065 
                                   2066 	.area CSEG (CODE)
                                   2067 ; function ak820_outline_0002
      007399                       2068 _ak820_outline_0002:
      007399 E0               [24] 2069 	movx	a,@dptr
      00739A FD               [12] 2070 	mov	r5,a
      00739B A3               [24] 2071 	inc	dptr
      00739C E0               [24] 2072 	movx	a,@dptr
      00739D FE               [12] 2073 	mov	r6,a
      00739E A3               [24] 2074 	inc	dptr
      00739F E0               [24] 2075 	movx	a,@dptr
      0073A0 FF               [12] 2076 	mov	r7,a
      0073A1 22               [24] 2077 	ret
                                   2078 
                                   2079 	.area CSEG (CODE)
                                   2080 ; function ak820_outline_0009
      0073A2                       2081 _ak820_outline_0009:
      0073A2 2D               [12] 2082 	add	a,r5
      0073A3 FA               [12] 2083 	mov	r2,a
      0073A4 E4               [12] 2084 	clr	a
      0073A5 3E               [12] 2085 	addc	a,r6
      0073A6 FB               [12] 2086 	mov	r3,a
      0073A7 8F 04            [24] 2087 	mov	ar4,r7
      0073A9 8A 82            [24] 2088 	mov	dpl,r2
      0073AB 8B 83            [24] 2089 	mov	dph,r3
      0073AD 8C F0            [24] 2090 	mov	b,r4
      0073AF 22               [24] 2091 	ret
                                   2092 
                                   2093 	.area CSEG (CODE)
                                   2094 ; function ak820_outline_0013
      0073B0                       2095 _ak820_outline_0013:
      0073B0 E0               [24] 2096 	movx	a,@dptr
      0073B1 FE               [12] 2097 	mov	r6,a
      0073B2 A3               [24] 2098 	inc	dptr
      0073B3 E0               [24] 2099 	movx	a,@dptr
      0073B4 FF               [12] 2100 	mov	r7,a
      0073B5 8E 82            [24] 2101 	mov	dpl,r6
      0073B7 8F 83            [24] 2102 	mov	dph,r7
      0073B9 22               [24] 2103 	ret
                                   2104 
                                   2105 	.area CSEG (CODE)
                                   2106 ; function ak820_outline_0015
      0073BA                       2107 _ak820_outline_0015:
      0073BA ED               [12] 2108 	mov	a,r5
      0073BB F0               [24] 2109 	movx	@dptr,a
      0073BC EE               [12] 2110 	mov	a,r6
      0073BD A3               [24] 2111 	inc	dptr
      0073BE F0               [24] 2112 	movx	@dptr,a
      0073BF EF               [12] 2113 	mov	a,r7
      0073C0 A3               [24] 2114 	inc	dptr
      0073C1 F0               [24] 2115 	movx	@dptr,a
      0073C2 22               [24] 2116 	ret
                                   2117 
                                   2118 	.area CSEG (CODE)
                                   2119 ; function ak820_outline_0022
      0073C3                       2120 _ak820_outline_0022:
      0073C3 90 07 52         [24] 2121 	mov	dptr,#(_process_action_PARM_2+0x0001)
      0073C6 E0               [24] 2122 	movx	a,@dptr
      0073C7 54 1F            [12] 2123 	anl	a,#0x1f
      0073C9 F5 82            [12] 2124 	mov	dpl,a
      0073CB 22               [24] 2125 	ret
