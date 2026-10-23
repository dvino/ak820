                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module quantum
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _shutdown_quantum
                                     12 	.globl _extract_mod_bits
                                     13 	.globl _process_tri_layer
                                     14 	.globl _process_rgb
                                     15 	.globl _process_grave_esc
                                     16 	.globl _process_repeat_key
                                     17 	.globl _process_last_key
                                     18 	.globl _process_caps_word
                                     19 	.globl _process_record_via
                                     20 	.globl _mcu_reset
                                     21 	.globl _bootloader_jump
                                     22 	.globl _layer_switch_get_layer
                                     23 	.globl _read_source_keycode_cache
                                     24 	.globl _update_source_layers_cache
                                     25 	.globl _default_layer_set
                                     26 	.globl _clear_keyboard
                                     27 	.globl _unregister_weak_mods
                                     28 	.globl _register_weak_mods
                                     29 	.globl _unregister_mods
                                     30 	.globl _register_mods
                                     31 	.globl _unregister_code
                                     32 	.globl _register_code
                                     33 	.globl _eeconfig_disable
                                     34 	.globl _keymap_key_to_keycode
                                     35 	.globl _rgb_matrix_set_suspend_state
                                     36 	.globl _rgb_matrix_task
                                     37 	.globl _mDelaymS
                                     38 	.globl _ADC_START
                                     39 	.globl _S0_R_FIFO
                                     40 	.globl _S0_T_FIFO
                                     41 	.globl _S0_FREE
                                     42 	.globl _S0_IF_BYTE
                                     43 	.globl _S0_IF_FIRST
                                     44 	.globl _S0_IF_OV
                                     45 	.globl _S0_FST_ACT
                                     46 	.globl _CP_RL2
                                     47 	.globl _C_T2
                                     48 	.globl _TR2
                                     49 	.globl _EXEN2
                                     50 	.globl _TCLK
                                     51 	.globl _RCLK
                                     52 	.globl _EXF2
                                     53 	.globl _CAP1F
                                     54 	.globl _TF2
                                     55 	.globl _RI
                                     56 	.globl _TI
                                     57 	.globl _RB8
                                     58 	.globl _TB8
                                     59 	.globl _REN
                                     60 	.globl _SM2
                                     61 	.globl _SM1
                                     62 	.globl _SM0
                                     63 	.globl _IT0
                                     64 	.globl _IE0
                                     65 	.globl _IT1
                                     66 	.globl _IE1
                                     67 	.globl _TR0
                                     68 	.globl _TF0
                                     69 	.globl _TR1
                                     70 	.globl _TF1
                                     71 	.globl _P4_0
                                     72 	.globl _P4_1
                                     73 	.globl _P4_2
                                     74 	.globl _P4_3
                                     75 	.globl _P4_4
                                     76 	.globl _P4_5
                                     77 	.globl _P4_6
                                     78 	.globl _RXD
                                     79 	.globl _TXD
                                     80 	.globl _INT0
                                     81 	.globl _INT1
                                     82 	.globl _T0
                                     83 	.globl _T1
                                     84 	.globl _MOSI1
                                     85 	.globl _MISO1
                                     86 	.globl _SCK1
                                     87 	.globl _P3_0
                                     88 	.globl _P3_1
                                     89 	.globl _P3_2
                                     90 	.globl _P3_3
                                     91 	.globl _P3_4
                                     92 	.globl _P3_5
                                     93 	.globl _P3_6
                                     94 	.globl _P3_7
                                     95 	.globl _CAP1_
                                     96 	.globl _T2_
                                     97 	.globl _CAP2_
                                     98 	.globl _T2EX_
                                     99 	.globl _RXD1
                                    100 	.globl _TXD1
                                    101 	.globl _P2_0
                                    102 	.globl _P2_1
                                    103 	.globl _P2_2
                                    104 	.globl _P2_3
                                    105 	.globl _P2_4
                                    106 	.globl _P2_5
                                    107 	.globl _P2_6
                                    108 	.globl _P2_7
                                    109 	.globl _AIN0
                                    110 	.globl _AIN1
                                    111 	.globl _AIN2
                                    112 	.globl _AIN3
                                    113 	.globl _AIN4
                                    114 	.globl _AIN5
                                    115 	.globl _AIN6
                                    116 	.globl _AIN7
                                    117 	.globl _CAP1
                                    118 	.globl _T2
                                    119 	.globl _CAP2
                                    120 	.globl _T2EX
                                    121 	.globl _INT0_
                                    122 	.globl _SCS
                                    123 	.globl _MOSI
                                    124 	.globl _MISO
                                    125 	.globl _SCK
                                    126 	.globl _RXD1_
                                    127 	.globl _TXD1_
                                    128 	.globl _P1_0
                                    129 	.globl _P1_1
                                    130 	.globl _P1_2
                                    131 	.globl _P1_3
                                    132 	.globl _P1_4
                                    133 	.globl _P1_5
                                    134 	.globl _P1_6
                                    135 	.globl _P1_7
                                    136 	.globl _AIN8
                                    137 	.globl _AIN9
                                    138 	.globl _AIN10
                                    139 	.globl _AIN11
                                    140 	.globl _AIN12
                                    141 	.globl _AIN13
                                    142 	.globl _RXD_
                                    143 	.globl _TXD_
                                    144 	.globl _SCL0
                                    145 	.globl _SDA0
                                    146 	.globl _P0_0
                                    147 	.globl _P0_1
                                    148 	.globl _P0_2
                                    149 	.globl _P0_3
                                    150 	.globl _P0_4
                                    151 	.globl _P0_5
                                    152 	.globl _P0_6
                                    153 	.globl _P0_7
                                    154 	.globl _IE_SPI0
                                    155 	.globl _IE_USB
                                    156 	.globl _IE_ADC
                                    157 	.globl _IE_UART1
                                    158 	.globl _IE_PWM_I2C
                                    159 	.globl _IE_GPIO
                                    160 	.globl _IE_WDOG
                                    161 	.globl _PX0
                                    162 	.globl _PT0
                                    163 	.globl _PX1
                                    164 	.globl _PT1
                                    165 	.globl _PS
                                    166 	.globl _PT2
                                    167 	.globl _PL_FLAG
                                    168 	.globl _PH_FLAG
                                    169 	.globl _EX0
                                    170 	.globl _ET0
                                    171 	.globl _EX1
                                    172 	.globl _ET1
                                    173 	.globl _ES
                                    174 	.globl _ET2
                                    175 	.globl _E_DIS
                                    176 	.globl _EA
                                    177 	.globl _P
                                    178 	.globl _F1
                                    179 	.globl _OV
                                    180 	.globl _RS0
                                    181 	.globl _RS1
                                    182 	.globl _F0
                                    183 	.globl _AC
                                    184 	.globl _CY
                                    185 	.globl _I2CS_INT_ST
                                    186 	.globl _I2CX_INT
                                    187 	.globl _LED_STATUS
                                    188 	.globl _LED_DMA_H
                                    189 	.globl _LED_DMA_L
                                    190 	.globl _LED_DMA
                                    191 	.globl _LED_PWM_OE
                                    192 	.globl _LED_COMMON
                                    193 	.globl _ADC_CHAN
                                    194 	.globl _ADC_DAT_H
                                    195 	.globl _ADC_DAT_L
                                    196 	.globl _ADC_DAT
                                    197 	.globl _ADC_CTRL
                                    198 	.globl _SPI1_CK_SE
                                    199 	.globl _SPI1_CTRL
                                    200 	.globl _SPI1_DATA
                                    201 	.globl _SPI1_STAT
                                    202 	.globl _SIF1
                                    203 	.globl _SBAUD1
                                    204 	.globl _SBUF1
                                    205 	.globl _SCON1
                                    206 	.globl _SPI0_SETUP
                                    207 	.globl _SPI0_CK_SE
                                    208 	.globl _SPI0_CTRL
                                    209 	.globl _SPI0_DATA
                                    210 	.globl _SPI0_STAT
                                    211 	.globl _T2CAP1H
                                    212 	.globl _T2CAP1L
                                    213 	.globl _T2CAP1
                                    214 	.globl _TH2
                                    215 	.globl _TL2
                                    216 	.globl _T2COUNT
                                    217 	.globl _RCAP2H
                                    218 	.globl _RCAP2L
                                    219 	.globl _RCAP2
                                    220 	.globl _T2MOD
                                    221 	.globl _T2CON
                                    222 	.globl _SBUF
                                    223 	.globl _SCON
                                    224 	.globl _TH1
                                    225 	.globl _TH0
                                    226 	.globl _TL1
                                    227 	.globl _TL0
                                    228 	.globl _TMOD
                                    229 	.globl _TCON
                                    230 	.globl _XBUS_AUX
                                    231 	.globl _P7
                                    232 	.globl _P6_DIR
                                    233 	.globl _P6_OUT_PU
                                    234 	.globl _P6_IN
                                    235 	.globl _P5_DIR
                                    236 	.globl _P5_OUT_PU
                                    237 	.globl _P5_IN
                                    238 	.globl _P4_LED_KEY
                                    239 	.globl _P4_DIR_PU
                                    240 	.globl _P4_MOD_OC
                                    241 	.globl _P4
                                    242 	.globl _P3_DIR_PU
                                    243 	.globl _P3_MOD_OC
                                    244 	.globl _P3
                                    245 	.globl _P2_DIR_PU
                                    246 	.globl _P2_MOD_OC
                                    247 	.globl _P2
                                    248 	.globl _P1_DIR_PU
                                    249 	.globl _P1_MOD_OC
                                    250 	.globl _P1
                                    251 	.globl _P0_DIR_PU
                                    252 	.globl _P0_MOD_OC
                                    253 	.globl _P0
                                    254 	.globl _ROM_CTRL
                                    255 	.globl _ROM_DATA_HH
                                    256 	.globl _ROM_DATA_HL
                                    257 	.globl _ROM_DATA_HI
                                    258 	.globl _ROM_ADDR_H
                                    259 	.globl _ROM_ADDR_L
                                    260 	.globl _ROM_ADDR
                                    261 	.globl _GPIO_IE
                                    262 	.globl _IP_EX
                                    263 	.globl _IE_EX
                                    264 	.globl _IP
                                    265 	.globl _IE
                                    266 	.globl _WDOG_COUNT
                                    267 	.globl _RESET_KEEP
                                    268 	.globl _WAKE_CTRL
                                    269 	.globl _CLOCK_CFG
                                    270 	.globl _POWER_CFG
                                    271 	.globl _PCON
                                    272 	.globl _GLOBAL_CFG
                                    273 	.globl _SAFE_MOD
                                    274 	.globl _DPH
                                    275 	.globl _DPL
                                    276 	.globl _SP
                                    277 	.globl _A_INV
                                    278 	.globl _B
                                    279 	.globl _ACC
                                    280 	.globl _PSW
                                    281 	.globl _process_record_quantum_helper_PARM_2
                                    282 	.globl _get_event_keycode_PARM_1
                                    283 	.globl _get_record_keycode_PARM_2
                                    284 	.globl _post_process_record_user_PARM_2
                                    285 	.globl _post_process_record_kb_PARM_2
                                    286 	.globl _process_record_user_PARM_2
                                    287 	.globl _process_record_kb_PARM_2
                                    288 	.globl _pre_process_record_user_PARM_2
                                    289 	.globl _pre_process_record_kb_PARM_2
                                    290 	.globl _register_code16
                                    291 	.globl _unregister_code16
                                    292 	.globl _pre_process_record_kb
                                    293 	.globl _pre_process_record_user
                                    294 	.globl _process_action_kb
                                    295 	.globl _process_record_kb
                                    296 	.globl _process_record_user
                                    297 	.globl _post_process_record_kb
                                    298 	.globl _post_process_record_user
                                    299 	.globl _reset_keyboard
                                    300 	.globl _soft_reset_keyboard
                                    301 	.globl _get_record_keycode
                                    302 	.globl _get_event_keycode
                                    303 	.globl _pre_process_record_quantum
                                    304 	.globl _post_process_record_quantum
                                    305 	.globl _process_record_quantum
                                    306 	.globl _process_record_quantum_helper
                                    307 	.globl _shutdown_user
                                    308 ;--------------------------------------------------------
                                    309 ; special function registers
                                    310 ;--------------------------------------------------------
                                    311 	.area RSEG    (ABS,DATA)
      000000                        312 	.org 0x0000
                           0000D0   313 _PSW	=	0x00d0
                           0000E0   314 _ACC	=	0x00e0
                           0000F0   315 _B	=	0x00f0
                           0000FD   316 _A_INV	=	0x00fd
                           000081   317 _SP	=	0x0081
                           000082   318 _DPL	=	0x0082
                           000083   319 _DPH	=	0x0083
                           0000A1   320 _SAFE_MOD	=	0x00a1
                           0000B1   321 _GLOBAL_CFG	=	0x00b1
                           000087   322 _PCON	=	0x0087
                           0000BA   323 _POWER_CFG	=	0x00ba
                           0000B9   324 _CLOCK_CFG	=	0x00b9
                           0000A9   325 _WAKE_CTRL	=	0x00a9
                           0000FE   326 _RESET_KEEP	=	0x00fe
                           0000FF   327 _WDOG_COUNT	=	0x00ff
                           0000A8   328 _IE	=	0x00a8
                           0000B8   329 _IP	=	0x00b8
                           0000E8   330 _IE_EX	=	0x00e8
                           0000E9   331 _IP_EX	=	0x00e9
                           0000B2   332 _GPIO_IE	=	0x00b2
                           008584   333 _ROM_ADDR	=	0x8584
                           000084   334 _ROM_ADDR_L	=	0x0084
                           000085   335 _ROM_ADDR_H	=	0x0085
                           008F8E   336 _ROM_DATA_HI	=	0x8f8e
                           00008E   337 _ROM_DATA_HL	=	0x008e
                           00008F   338 _ROM_DATA_HH	=	0x008f
                           000086   339 _ROM_CTRL	=	0x0086
                           000080   340 _P0	=	0x0080
                           0000C4   341 _P0_MOD_OC	=	0x00c4
                           0000C5   342 _P0_DIR_PU	=	0x00c5
                           000090   343 _P1	=	0x0090
                           000092   344 _P1_MOD_OC	=	0x0092
                           000093   345 _P1_DIR_PU	=	0x0093
                           0000A0   346 _P2	=	0x00a0
                           000094   347 _P2_MOD_OC	=	0x0094
                           000095   348 _P2_DIR_PU	=	0x0095
                           0000B0   349 _P3	=	0x00b0
                           000096   350 _P3_MOD_OC	=	0x0096
                           000097   351 _P3_DIR_PU	=	0x0097
                           0000C0   352 _P4	=	0x00c0
                           0000C2   353 _P4_MOD_OC	=	0x00c2
                           0000C3   354 _P4_DIR_PU	=	0x00c3
                           0000C1   355 _P4_LED_KEY	=	0x00c1
                           0000AA   356 _P5_IN	=	0x00aa
                           0000AB   357 _P5_OUT_PU	=	0x00ab
                           0000AC   358 _P5_DIR	=	0x00ac
                           0000AD   359 _P6_IN	=	0x00ad
                           0000AE   360 _P6_OUT_PU	=	0x00ae
                           0000AF   361 _P6_DIR	=	0x00af
                           0000F1   362 _P7	=	0x00f1
                           0000A2   363 _XBUS_AUX	=	0x00a2
                           000088   364 _TCON	=	0x0088
                           000089   365 _TMOD	=	0x0089
                           00008A   366 _TL0	=	0x008a
                           00008B   367 _TL1	=	0x008b
                           00008C   368 _TH0	=	0x008c
                           00008D   369 _TH1	=	0x008d
                           000098   370 _SCON	=	0x0098
                           000099   371 _SBUF	=	0x0099
                           0000C8   372 _T2CON	=	0x00c8
                           0000C9   373 _T2MOD	=	0x00c9
                           00CBCA   374 _RCAP2	=	0xcbca
                           0000CA   375 _RCAP2L	=	0x00ca
                           0000CB   376 _RCAP2H	=	0x00cb
                           00CDCC   377 _T2COUNT	=	0xcdcc
                           0000CC   378 _TL2	=	0x00cc
                           0000CD   379 _TH2	=	0x00cd
                           00CFCE   380 _T2CAP1	=	0xcfce
                           0000CE   381 _T2CAP1L	=	0x00ce
                           0000CF   382 _T2CAP1H	=	0x00cf
                           0000F8   383 _SPI0_STAT	=	0x00f8
                           0000F9   384 _SPI0_DATA	=	0x00f9
                           0000FA   385 _SPI0_CTRL	=	0x00fa
                           0000FB   386 _SPI0_CK_SE	=	0x00fb
                           0000FC   387 _SPI0_SETUP	=	0x00fc
                           0000BC   388 _SCON1	=	0x00bc
                           0000BD   389 _SBUF1	=	0x00bd
                           0000BE   390 _SBAUD1	=	0x00be
                           0000BF   391 _SIF1	=	0x00bf
                           0000B4   392 _SPI1_STAT	=	0x00b4
                           0000B5   393 _SPI1_DATA	=	0x00b5
                           0000B6   394 _SPI1_CTRL	=	0x00b6
                           0000B7   395 _SPI1_CK_SE	=	0x00b7
                           0000F3   396 _ADC_CTRL	=	0x00f3
                           00F5F4   397 _ADC_DAT	=	0xf5f4
                           0000F4   398 _ADC_DAT_L	=	0x00f4
                           0000F5   399 _ADC_DAT_H	=	0x00f5
                           0000F6   400 _ADC_CHAN	=	0x00f6
                           0000A6   401 _LED_COMMON	=	0x00a6
                           0000A7   402 _LED_PWM_OE	=	0x00a7
                           00C7C6   403 _LED_DMA	=	0xc7c6
                           0000C6   404 _LED_DMA_L	=	0x00c6
                           0000C7   405 _LED_DMA_H	=	0x00c7
                           0000F7   406 _LED_STATUS	=	0x00f7
                           0000B3   407 _I2CX_INT	=	0x00b3
                           0000BB   408 _I2CS_INT_ST	=	0x00bb
                                    409 ;--------------------------------------------------------
                                    410 ; special function bits
                                    411 ;--------------------------------------------------------
                                    412 	.area RSEG    (ABS,DATA)
      000000                        413 	.org 0x0000
                           0000D7   414 _CY	=	0x00d7
                           0000D6   415 _AC	=	0x00d6
                           0000D5   416 _F0	=	0x00d5
                           0000D4   417 _RS1	=	0x00d4
                           0000D3   418 _RS0	=	0x00d3
                           0000D2   419 _OV	=	0x00d2
                           0000D1   420 _F1	=	0x00d1
                           0000D0   421 _P	=	0x00d0
                           0000AF   422 _EA	=	0x00af
                           0000AE   423 _E_DIS	=	0x00ae
                           0000AD   424 _ET2	=	0x00ad
                           0000AC   425 _ES	=	0x00ac
                           0000AB   426 _ET1	=	0x00ab
                           0000AA   427 _EX1	=	0x00aa
                           0000A9   428 _ET0	=	0x00a9
                           0000A8   429 _EX0	=	0x00a8
                           0000BF   430 _PH_FLAG	=	0x00bf
                           0000BE   431 _PL_FLAG	=	0x00be
                           0000BD   432 _PT2	=	0x00bd
                           0000BC   433 _PS	=	0x00bc
                           0000BB   434 _PT1	=	0x00bb
                           0000BA   435 _PX1	=	0x00ba
                           0000B9   436 _PT0	=	0x00b9
                           0000B8   437 _PX0	=	0x00b8
                           0000EF   438 _IE_WDOG	=	0x00ef
                           0000EE   439 _IE_GPIO	=	0x00ee
                           0000ED   440 _IE_PWM_I2C	=	0x00ed
                           0000EC   441 _IE_UART1	=	0x00ec
                           0000EB   442 _IE_ADC	=	0x00eb
                           0000E9   443 _IE_USB	=	0x00e9
                           0000E8   444 _IE_SPI0	=	0x00e8
                           000087   445 _P0_7	=	0x0087
                           000086   446 _P0_6	=	0x0086
                           000085   447 _P0_5	=	0x0085
                           000084   448 _P0_4	=	0x0084
                           000083   449 _P0_3	=	0x0083
                           000082   450 _P0_2	=	0x0082
                           000081   451 _P0_1	=	0x0081
                           000080   452 _P0_0	=	0x0080
                           000081   453 _SDA0	=	0x0081
                           000080   454 _SCL0	=	0x0080
                           000083   455 _TXD_	=	0x0083
                           000082   456 _RXD_	=	0x0082
                           000085   457 _AIN13	=	0x0085
                           000084   458 _AIN12	=	0x0084
                           000083   459 _AIN11	=	0x0083
                           000082   460 _AIN10	=	0x0082
                           000081   461 _AIN9	=	0x0081
                           000080   462 _AIN8	=	0x0080
                           000097   463 _P1_7	=	0x0097
                           000096   464 _P1_6	=	0x0096
                           000095   465 _P1_5	=	0x0095
                           000094   466 _P1_4	=	0x0094
                           000093   467 _P1_3	=	0x0093
                           000092   468 _P1_2	=	0x0092
                           000091   469 _P1_1	=	0x0091
                           000090   470 _P1_0	=	0x0090
                           000097   471 _TXD1_	=	0x0097
                           000096   472 _RXD1_	=	0x0096
                           000097   473 _SCK	=	0x0097
                           000096   474 _MISO	=	0x0096
                           000095   475 _MOSI	=	0x0095
                           000094   476 _SCS	=	0x0094
                           000092   477 _INT0_	=	0x0092
                           000091   478 _T2EX	=	0x0091
                           000091   479 _CAP2	=	0x0091
                           000090   480 _T2	=	0x0090
                           000090   481 _CAP1	=	0x0090
                           000097   482 _AIN7	=	0x0097
                           000096   483 _AIN6	=	0x0096
                           000095   484 _AIN5	=	0x0095
                           000094   485 _AIN4	=	0x0094
                           000093   486 _AIN3	=	0x0093
                           000092   487 _AIN2	=	0x0092
                           000091   488 _AIN1	=	0x0091
                           000090   489 _AIN0	=	0x0090
                           0000A7   490 _P2_7	=	0x00a7
                           0000A6   491 _P2_6	=	0x00a6
                           0000A5   492 _P2_5	=	0x00a5
                           0000A4   493 _P2_4	=	0x00a4
                           0000A3   494 _P2_3	=	0x00a3
                           0000A2   495 _P2_2	=	0x00a2
                           0000A1   496 _P2_1	=	0x00a1
                           0000A0   497 _P2_0	=	0x00a0
                           0000A7   498 _TXD1	=	0x00a7
                           0000A6   499 _RXD1	=	0x00a6
                           0000A5   500 _T2EX_	=	0x00a5
                           0000A5   501 _CAP2_	=	0x00a5
                           0000A4   502 _T2_	=	0x00a4
                           0000A4   503 _CAP1_	=	0x00a4
                           0000B7   504 _P3_7	=	0x00b7
                           0000B6   505 _P3_6	=	0x00b6
                           0000B5   506 _P3_5	=	0x00b5
                           0000B4   507 _P3_4	=	0x00b4
                           0000B3   508 _P3_3	=	0x00b3
                           0000B2   509 _P3_2	=	0x00b2
                           0000B1   510 _P3_1	=	0x00b1
                           0000B0   511 _P3_0	=	0x00b0
                           0000B7   512 _SCK1	=	0x00b7
                           0000B6   513 _MISO1	=	0x00b6
                           0000B5   514 _MOSI1	=	0x00b5
                           0000B5   515 _T1	=	0x00b5
                           0000B4   516 _T0	=	0x00b4
                           0000B3   517 _INT1	=	0x00b3
                           0000B2   518 _INT0	=	0x00b2
                           0000B1   519 _TXD	=	0x00b1
                           0000B0   520 _RXD	=	0x00b0
                           0000C6   521 _P4_6	=	0x00c6
                           0000C5   522 _P4_5	=	0x00c5
                           0000C4   523 _P4_4	=	0x00c4
                           0000C3   524 _P4_3	=	0x00c3
                           0000C2   525 _P4_2	=	0x00c2
                           0000C1   526 _P4_1	=	0x00c1
                           0000C0   527 _P4_0	=	0x00c0
                           00008F   528 _TF1	=	0x008f
                           00008E   529 _TR1	=	0x008e
                           00008D   530 _TF0	=	0x008d
                           00008C   531 _TR0	=	0x008c
                           00008B   532 _IE1	=	0x008b
                           00008A   533 _IT1	=	0x008a
                           000089   534 _IE0	=	0x0089
                           000088   535 _IT0	=	0x0088
                           00009F   536 _SM0	=	0x009f
                           00009E   537 _SM1	=	0x009e
                           00009D   538 _SM2	=	0x009d
                           00009C   539 _REN	=	0x009c
                           00009B   540 _TB8	=	0x009b
                           00009A   541 _RB8	=	0x009a
                           000099   542 _TI	=	0x0099
                           000098   543 _RI	=	0x0098
                           0000CF   544 _TF2	=	0x00cf
                           0000CF   545 _CAP1F	=	0x00cf
                           0000CE   546 _EXF2	=	0x00ce
                           0000CD   547 _RCLK	=	0x00cd
                           0000CC   548 _TCLK	=	0x00cc
                           0000CB   549 _EXEN2	=	0x00cb
                           0000CA   550 _TR2	=	0x00ca
                           0000C9   551 _C_T2	=	0x00c9
                           0000C8   552 _CP_RL2	=	0x00c8
                           0000FF   553 _S0_FST_ACT	=	0x00ff
                           0000FE   554 _S0_IF_OV	=	0x00fe
                           0000FD   555 _S0_IF_FIRST	=	0x00fd
                           0000FC   556 _S0_IF_BYTE	=	0x00fc
                           0000FB   557 _S0_FREE	=	0x00fb
                           0000FA   558 _S0_T_FIFO	=	0x00fa
                           0000F8   559 _S0_R_FIFO	=	0x00f8
                           0000F7   560 _ADC_START	=	0x00f7
                                    561 ;--------------------------------------------------------
                                    562 ; overlayable register banks
                                    563 ;--------------------------------------------------------
                                    564 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        565 	.ds 8
                                    566 ;--------------------------------------------------------
                                    567 ; internal ram data
                                    568 ;--------------------------------------------------------
                                    569 	.area DSEG    (DATA)
                                    570 ;--------------------------------------------------------
                                    571 ; overlayable items in internal ram
                                    572 ;--------------------------------------------------------
                                    573 ;--------------------------------------------------------
                                    574 ; indirectly addressable internal ram data
                                    575 ;--------------------------------------------------------
                                    576 	.area ISEG    (DATA)
                                    577 ;--------------------------------------------------------
                                    578 ; absolute internal ram data
                                    579 ;--------------------------------------------------------
                                    580 	.area IABS    (ABS,DATA)
                                    581 	.area IABS    (ABS,DATA)
                                    582 ;--------------------------------------------------------
                                    583 ; bit data
                                    584 ;--------------------------------------------------------
                                    585 	.area BSEG    (BIT)
      00000F                        586 _pre_process_record_quantum_sloc0_1_0:
      00000F                        587 	.ds 1
                                    588 ;--------------------------------------------------------
                                    589 ; paged external ram data
                                    590 ;--------------------------------------------------------
                                    591 	.area PSEG    (PAG,XDATA)
                                    592 ;--------------------------------------------------------
                                    593 ; uninitialized external ram data
                                    594 ;--------------------------------------------------------
                                    595 	.area XSEG    (XDATA)
      0009D1                        596 _extract_mod_bits_code_10000_569:
      0009D1                        597 	.ds 2
      0009D3                        598 _register_code16_code_10000_575:
      0009D3                        599 	.ds 2
      0009D5                        600 _unregister_code16_code_10000_580:
      0009D5                        601 	.ds 2
      0009D7                        602 _pre_process_record_kb_PARM_2:
      0009D7                        603 	.ds 3
      0009DA                        604 _pre_process_record_kb_keycode_10000_594:
      0009DA                        605 	.ds 2
      0009DC                        606 _pre_process_record_user_PARM_2:
      0009DC                        607 	.ds 3
      0009DF                        608 _process_record_kb_PARM_2:
      0009DF                        609 	.ds 3
      0009E2                        610 _process_record_kb_keycode_10000_600:
      0009E2                        611 	.ds 2
      0009E4                        612 _process_record_user_PARM_2:
      0009E4                        613 	.ds 3
      0009E7                        614 _post_process_record_kb_PARM_2:
      0009E7                        615 	.ds 3
      0009EA                        616 _post_process_record_kb_keycode_10000_604:
      0009EA                        617 	.ds 2
      0009EC                        618 _post_process_record_user_PARM_2:
      0009EC                        619 	.ds 3
      0009EF                        620 _get_record_keycode_PARM_2:
      0009EF                        621 	.ds 1
      0009F0                        622 _get_record_keycode_record_10000_618:
      0009F0                        623 	.ds 3
      0009F3                        624 _get_event_keycode_PARM_1:
      0009F3                        625 	.ds 6
      0009F9                        626 _get_event_keycode_update_layer_cache_10000_622:
      0009F9                        627 	.ds 1
      0009FA                        628 _pre_process_record_quantum_record_10000_628:
      0009FA                        629 	.ds 3
      0009FD                        630 _post_process_record_quantum_record_10000_630:
      0009FD                        631 	.ds 3
      000A00                        632 _process_record_quantum_record_10000_632:
      000A00                        633 	.ds 3
      000A03                        634 _process_record_quantum_helper_PARM_2:
      000A03                        635 	.ds 3
      000A06                        636 _process_record_quantum_helper_keycode_10000_634:
      000A06                        637 	.ds 2
      000A08                        638 _get_u8_str_buf_10000_660:
      000A08                        639 	.ds 4
      000A0C                        640 _get_u8_str_last_num_10000_660:
      000A0C                        641 	.ds 1
      000A0D                        642 _get_u8_str_last_pad_10000_660:
      000A0D                        643 	.ds 1
      000A0E                        644 _get_u16_str_buf_10000_664:
      000A0E                        645 	.ds 6
      000A14                        646 _get_u16_str_last_num_10000_664:
      000A14                        647 	.ds 2
      000A16                        648 _get_u16_str_last_pad_10000_664:
      000A16                        649 	.ds 1
                                    650 ;--------------------------------------------------------
                                    651 ; absolute external ram data
                                    652 ;--------------------------------------------------------
                                    653 	.area XABS    (ABS,XDATA)
                                    654 ;--------------------------------------------------------
                                    655 ; initialized external ram data
                                    656 ;--------------------------------------------------------
                                    657 	.area XISEG   (XDATA)
                                    658 	.area HOME    (CODE)
                                    659 	.area GSINIT0 (CODE)
                                    660 	.area GSINIT1 (CODE)
                                    661 	.area GSINIT2 (CODE)
                                    662 	.area GSINIT3 (CODE)
                                    663 	.area GSINIT4 (CODE)
                                    664 	.area GSINIT5 (CODE)
                                    665 	.area GSINIT  (CODE)
                                    666 	.area GSFINAL (CODE)
                                    667 	.area CSEG    (CODE)
                                    668 ;--------------------------------------------------------
                                    669 ; global & static initialisations
                                    670 ;--------------------------------------------------------
                                    671 	.area HOME    (CODE)
                                    672 	.area GSINIT  (CODE)
                                    673 	.area GSFINAL (CODE)
                                    674 	.area GSINIT  (CODE)
                                    675 ;------------------------------------------------------------
                                    676 ;Allocation info for local variables in function 'get_u8_str'
                                    677 ;------------------------------------------------------------
                                    678 ;curr_pad      Allocated with name '_get_u8_str_PARM_2'
                                    679 ;curr_num      Allocated with name '_get_u8_str_curr_num_10000_659'
                                    680 ;buf           Allocated with name '_get_u8_str_buf_10000_660'
                                    681 ;last_num      Allocated with name '_get_u8_str_last_num_10000_660'
                                    682 ;last_pad      Allocated with name '_get_u8_str_last_pad_10000_660'
                                    683 ;------------------------------------------------------------
                                    684 ;	quantum/quantum.c:674: static char    buf[4]   = {0};
      003121 90 0A 08         [24]  685 	mov	dptr,#_get_u8_str_buf_10000_660
      003124 E4               [12]  686 	clr	a
      003125 F0               [24]  687 	movx	@dptr,a
      003126 90 0A 09         [24]  688 	mov	dptr,#(_get_u8_str_buf_10000_660 + 0x0001)
      003129 F0               [24]  689 	movx	@dptr,a
      00312A 90 0A 0A         [24]  690 	mov	dptr,#(_get_u8_str_buf_10000_660 + 0x0002)
      00312D F0               [24]  691 	movx	@dptr,a
      00312E 90 0A 0B         [24]  692 	mov	dptr,#(_get_u8_str_buf_10000_660 + 0x0003)
      003131 F0               [24]  693 	movx	@dptr,a
                                    694 ;	quantum/quantum.c:675: static uint8_t last_num = 0xFF;
      003132 90 0A 0C         [24]  695 	mov	dptr,#_get_u8_str_last_num_10000_660
      003135 14               [12]  696 	dec	a
      003136 F0               [24]  697 	movx	@dptr,a
                                    698 ;	quantum/quantum.c:676: static char    last_pad = '\0';
      003137 90 0A 0D         [24]  699 	mov	dptr,#_get_u8_str_last_pad_10000_660
      00313A E4               [12]  700 	clr	a
      00313B F0               [24]  701 	movx	@dptr,a
                                    702 ;------------------------------------------------------------
                                    703 ;Allocation info for local variables in function 'get_u16_str'
                                    704 ;------------------------------------------------------------
                                    705 ;curr_pad      Allocated with name '_get_u16_str_PARM_2'
                                    706 ;curr_num      Allocated with name '_get_u16_str_curr_num_10000_663'
                                    707 ;buf           Allocated with name '_get_u16_str_buf_10000_664'
                                    708 ;last_num      Allocated with name '_get_u16_str_last_num_10000_664'
                                    709 ;last_pad      Allocated with name '_get_u16_str_last_pad_10000_664'
                                    710 ;------------------------------------------------------------
                                    711 ;	quantum/quantum.c:694: static char     buf[6]   = {0};
      00313C 90 0A 0E         [24]  712 	mov	dptr,#_get_u16_str_buf_10000_664
      00313F E4               [12]  713 	clr	a
      003140 F0               [24]  714 	movx	@dptr,a
      003141 90 0A 0F         [24]  715 	mov	dptr,#(_get_u16_str_buf_10000_664 + 0x0001)
      003144 F0               [24]  716 	movx	@dptr,a
      003145 90 0A 10         [24]  717 	mov	dptr,#(_get_u16_str_buf_10000_664 + 0x0002)
      003148 F0               [24]  718 	movx	@dptr,a
      003149 90 0A 11         [24]  719 	mov	dptr,#(_get_u16_str_buf_10000_664 + 0x0003)
      00314C F0               [24]  720 	movx	@dptr,a
      00314D 90 0A 12         [24]  721 	mov	dptr,#(_get_u16_str_buf_10000_664 + 0x0004)
      003150 F0               [24]  722 	movx	@dptr,a
      003151 90 0A 13         [24]  723 	mov	dptr,#(_get_u16_str_buf_10000_664 + 0x0005)
      003154 F0               [24]  724 	movx	@dptr,a
                                    725 ;	quantum/quantum.c:695: static uint16_t last_num = 0xFF;
      003155 90 0A 14         [24]  726 	mov	dptr,#_get_u16_str_last_num_10000_664
      003158 14               [12]  727 	dec	a
      003159 F0               [24]  728 	movx	@dptr,a
      00315A E4               [12]  729 	clr	a
      00315B A3               [24]  730 	inc	dptr
      00315C F0               [24]  731 	movx	@dptr,a
                                    732 ;	quantum/quantum.c:696: static char     last_pad = '\0';
      00315D 90 0A 16         [24]  733 	mov	dptr,#_get_u16_str_last_pad_10000_664
      003160 F0               [24]  734 	movx	@dptr,a
                                    735 ;--------------------------------------------------------
                                    736 ; Home
                                    737 ;--------------------------------------------------------
                                    738 	.area HOME    (CODE)
                                    739 	.area HOME    (CODE)
                                    740 ;--------------------------------------------------------
                                    741 ; code
                                    742 ;--------------------------------------------------------
                                    743 	.area CSEG    (CODE)
                                    744 ;------------------------------------------------------------
                                    745 ;Allocation info for local variables in function 'rgb_matrix_check_finished_leds'
                                    746 ;------------------------------------------------------------
                                    747 ;led_idx       Allocated with name '_rgb_matrix_check_finished_leds_led_idx_10000_193'
                                    748 ;------------------------------------------------------------
                                    749 ;	quantum/rgb_matrix/rgb_matrix.h:260: static inline bool rgb_matrix_check_finished_leds(uint8_t led_idx) {
                                    750 ;	-----------------------------------------
                           000007   751 	ar7 = 0x07
                           000006   752 	ar6 = 0x06
                           000005   753 	ar5 = 0x05
                           000004   754 	ar4 = 0x04
                           000003   755 	ar3 = 0x03
                           000002   756 	ar2 = 0x02
                           000001   757 	ar1 = 0x01
                           000000   758 	ar0 = 0x00
                                    759 ;	 function extract_mod_bits
                                    760 ;	-----------------------------------------
      009787                        761 _extract_mod_bits:
      009787 AF 83            [24]  762 	mov	r7,dph
      009789 E5 82            [12]  763 	mov	a,dpl
      00978B 90 09 D1         [24]  764 	mov	dptr,#_extract_mod_bits_code_10000_569
      00978E F0               [24]  765 	movx	@dptr,a
      00978F EF               [12]  766 	mov	a,r7
      009790 A3               [24]  767 	inc	dptr
      009791 F0               [24]  768 	movx	@dptr,a
                                    769 ;	quantum/quantum.c:101: uint8_t mods = (uint8_t)(code >> 8);
      009792 90 09 D1         [24]  770 	mov	dptr,#_extract_mod_bits_code_10000_569
      009795 E0               [24]  771 	movx	a,@dptr
      009796 A3               [24]  772 	inc	dptr
      009797 E0               [24]  773 	movx	a,@dptr
                                    774 ;	quantum/quantum.c:102: if (!mods || mods > (QK_MODS_MAX >> 8)) return 0;
      009798 FF               [12]  775 	mov	r7,a
      009799 60 05            [24]  776 	jz	00101$
      00979B EF               [12]  777 	mov	a,r7
      00979C 24 E0            [12]  778 	add	a,#0xff - 0x1f
      00979E 50 04            [24]  779 	jnc	00102$
                                    780 ;	free result
      0097A0                        781 00101$:
      0097A0 75 82 00         [24]  782 	mov	dpl, #0x00
      0097A3 22               [24]  783 	ret
      0097A4                        784 00102$:
                                    785 ;	quantum/quantum.c:103: return (mods & 0x10) ? (uint8_t)(mods << 4) : mods;
      0097A4 EF               [12]  786 	mov	a,r7
      0097A5 30 E4 07         [24]  787 	jnb	acc.4,00106$
      0097A8 EF               [12]  788 	mov	a,r7
      0097A9 C4               [12]  789 	swap	a
      0097AA 54 F0            [12]  790 	anl	a,#0xf0
      0097AC FE               [12]  791 	mov	r6,a
      0097AD 80 02            [24]  792 	sjmp	00107$
      0097AF                        793 00106$:
      0097AF 8F 06            [24]  794 	mov	ar6,r7
      0097B1                        795 00107$:
      0097B1 8E 82            [24]  796 	mov	dpl, r6
                                    797 ;	quantum/quantum.c:131: }
      0097B3 22               [24]  798 	ret
                                    799 ;------------------------------------------------------------
                                    800 ;Allocation info for local variables in function 'do_code16'
                                    801 ;------------------------------------------------------------
                                    802 ;f             Allocated with name '_do_code16_PARM_2'
                                    803 ;code          Allocated with name '_do_code16_code_10000_572'
                                    804 ;------------------------------------------------------------
                                    805 ;	quantum/quantum.c:133: void do_code16(uint16_t code, void (*f)(uint8_t)) {
                                    806 ;	-----------------------------------------
                                    807 ;	 function register_code16
                                    808 ;	-----------------------------------------
      0097B4                        809 _register_code16:
      0097B4 AF 83            [24]  810 	mov	r7,dph
      0097B6 E5 82            [12]  811 	mov	a,dpl
      0097B8 90 09 D3         [24]  812 	mov	dptr,#_register_code16_code_10000_575
      0097BB F0               [24]  813 	movx	@dptr,a
      0097BC EF               [12]  814 	mov	a,r7
      0097BD A3               [24]  815 	inc	dptr
      0097BE F0               [24]  816 	movx	@dptr,a
                                    817 ;	quantum/quantum.c:139: uint8_t mods = extract_mod_bits(code);
      0097BF 90 09 D3         [24]  818 	mov	dptr,#_register_code16_code_10000_575
      0097C2 12 73 CF         [24]  819 	lcall	_ak820_outline_0013
      0097C5 C0 07            [24]  820 	push	ar7
      0097C7 C0 06            [24]  821 	push	ar6
      0097C9 12 97 87         [24]  822 	lcall	_extract_mod_bits
      0097CC AD 82            [24]  823 	mov	r5, dpl
      0097CE D0 06            [24]  824 	pop	ar6
      0097D0 D0 07            [24]  825 	pop	ar7
                                    826 ;	quantum/quantum.c:140: if (IS_MODIFIER_KEYCODE(code) || code == KC_NO) {
      0097D2 C3               [12]  827 	clr	c
      0097D3 EE               [12]  828 	mov	a,r6
      0097D4 94 E0            [12]  829 	subb	a,#0xe0
      0097D6 EF               [12]  830 	mov	a,r7
      0097D7 94 00            [12]  831 	subb	a,#0x00
      0097D9 40 07            [24]  832 	jc	00105$
      0097DB 74 E7            [12]  833 	mov	a,#0xe7
      0097DD 9E               [12]  834 	subb	a,r6
      0097DE E4               [12]  835 	clr	a
      0097DF 9F               [12]  836 	subb	a,r7
      0097E0 50 0C            [24]  837 	jnc	00101$
                                    838 ;	free result
      0097E2                        839 00105$:
      0097E2 90 09 D3         [24]  840 	mov	dptr,#_register_code16_code_10000_575
      0097E5 E0               [24]  841 	movx	a,@dptr
      0097E6 F5 F0            [12]  842 	mov	b,a
      0097E8 A3               [24]  843 	inc	dptr
      0097E9 E0               [24]  844 	movx	a,@dptr
      0097EA 45 F0            [12]  845 	orl	a,b
      0097EC 70 07            [24]  846 	jnz	00102$
      0097EE                        847 00101$:
                                    848 ;	quantum/quantum.c:141: register_mods(mods);
      0097EE 8D 82            [24]  849 	mov	dpl, r5
      0097F0 12 73 44         [24]  850 	lcall	_register_mods
      0097F3 80 05            [24]  851 	sjmp	00103$
      0097F5                        852 00102$:
                                    853 ;	quantum/quantum.c:143: register_weak_mods(mods);
      0097F5 8D 82            [24]  854 	mov	dpl, r5
      0097F7 12 73 6C         [24]  855 	lcall	_register_weak_mods
      0097FA                        856 00103$:
                                    857 ;	quantum/quantum.c:145: register_code(code);
      0097FA 90 09 D3         [24]  858 	mov	dptr,#_register_code16_code_10000_575
      0097FD E0               [24]  859 	movx	a,@dptr
      0097FE F5 82            [12]  860 	mov	dpl,a
                                    861 ;	quantum/quantum.c:155: }
      009800 02 71 9F         [24]  862 	ljmp	_register_code
                                    863 ;------------------------------------------------------------
                                    864 ;Allocation info for local variables in function 'unregister_code16'
                                    865 ;------------------------------------------------------------
                                    866 ;code          Allocated with name '_unregister_code16_code_10000_580'
                                    867 ;mods          Allocated with name '_unregister_code16_mods_10000_581'
                                    868 ;------------------------------------------------------------
                                    869 ;	quantum/quantum.c:157: __attribute__((weak)) void unregister_code16(uint16_t code) {
                                    870 ;	-----------------------------------------
                                    871 ;	 function unregister_code16
                                    872 ;	-----------------------------------------
      009803                        873 _unregister_code16:
      009803 AF 83            [24]  874 	mov	r7,dph
      009805 E5 82            [12]  875 	mov	a,dpl
      009807 90 09 D5         [24]  876 	mov	dptr,#_unregister_code16_code_10000_580
      00980A F0               [24]  877 	movx	@dptr,a
      00980B EF               [12]  878 	mov	a,r7
      00980C A3               [24]  879 	inc	dptr
      00980D F0               [24]  880 	movx	@dptr,a
                                    881 ;	quantum/quantum.c:159: uint8_t mods = extract_mod_bits(code);
      00980E 90 09 D5         [24]  882 	mov	dptr,#_unregister_code16_code_10000_580
      009811 12 73 CF         [24]  883 	lcall	_ak820_outline_0013
      009814 C0 07            [24]  884 	push	ar7
      009816 C0 06            [24]  885 	push	ar6
      009818 12 97 87         [24]  886 	lcall	_extract_mod_bits
      00981B AD 82            [24]  887 	mov	r5, dpl
      00981D D0 06            [24]  888 	pop	ar6
                                    889 ;	quantum/quantum.c:160: unregister_code(code);
      00981F 8E 04            [24]  890 	mov	ar4,r6
      009821 8C 82            [24]  891 	mov	dpl, r4
      009823 C0 06            [24]  892 	push	ar6
      009825 C0 05            [24]  893 	push	ar5
      009827 12 72 7F         [24]  894 	lcall	_unregister_code
      00982A D0 05            [24]  895 	pop	ar5
      00982C D0 06            [24]  896 	pop	ar6
      00982E D0 07            [24]  897 	pop	ar7
                                    898 ;	quantum/quantum.c:161: if (IS_MODIFIER_KEYCODE(code) || code == KC_NO) {
      009830 C3               [12]  899 	clr	c
      009831 EE               [12]  900 	mov	a,r6
      009832 94 E0            [12]  901 	subb	a,#0xe0
      009834 EF               [12]  902 	mov	a,r7
      009835 94 00            [12]  903 	subb	a,#0x00
      009837 40 07            [24]  904 	jc	00105$
      009839 74 E7            [12]  905 	mov	a,#0xe7
      00983B 9E               [12]  906 	subb	a,r6
      00983C E4               [12]  907 	clr	a
      00983D 9F               [12]  908 	subb	a,r7
      00983E 50 0C            [24]  909 	jnc	00101$
                                    910 ;	free result
      009840                        911 00105$:
      009840 90 09 D5         [24]  912 	mov	dptr,#_unregister_code16_code_10000_580
      009843 E0               [24]  913 	movx	a,@dptr
      009844 F5 F0            [12]  914 	mov	b,a
      009846 A3               [24]  915 	inc	dptr
      009847 E0               [24]  916 	movx	a,@dptr
      009848 45 F0            [12]  917 	orl	a,b
      00984A 70 05            [24]  918 	jnz	00102$
      00984C                        919 00101$:
                                    920 ;	quantum/quantum.c:162: unregister_mods(mods);
      00984C 8D 82            [24]  921 	mov	dpl, r5
      00984E 02 73 58         [24]  922 	ljmp	_unregister_mods
      009851                        923 00102$:
                                    924 ;	quantum/quantum.c:164: unregister_weak_mods(mods);
      009851 8D 82            [24]  925 	mov	dpl, r5
                                    926 ;	quantum/quantum.c:175: }
      009853 02 73 80         [24]  927 	ljmp	_unregister_weak_mods
                                    928 ;------------------------------------------------------------
                                    929 ;Allocation info for local variables in function 'tap_code16_delay'
                                    930 ;------------------------------------------------------------
                                    931 ;delay         Allocated with name '_tap_code16_delay_PARM_2'
                                    932 ;code          Allocated with name '_tap_code16_delay_code_10000_585'
                                    933 ;i             Allocated with name '_tap_code16_delay_i_20000_587'
                                    934 ;i             Allocated with name '_tap_code16_delay_i_50000_590'
                                    935 ;------------------------------------------------------------
                                    936 ;	quantum/quantum.c:182: __attribute__((weak)) void tap_code16_delay(uint16_t code, uint16_t delay) {
                                    937 ;	-----------------------------------------
                                    938 ;	 function pre_process_record_kb
                                    939 ;	-----------------------------------------
      009856                        940 _pre_process_record_kb:
      009856 AF 83            [24]  941 	mov	r7,dph
      009858 E5 82            [12]  942 	mov	a,dpl
      00985A 90 09 DA         [24]  943 	mov	dptr,#_pre_process_record_kb_keycode_10000_594
      00985D F0               [24]  944 	movx	@dptr,a
      00985E EF               [12]  945 	mov	a,r7
      00985F A3               [24]  946 	inc	dptr
      009860 F0               [24]  947 	movx	@dptr,a
                                    948 ;	quantum/quantum.c:199: return pre_process_record_user(keycode, record);
      009861 90 09 DA         [24]  949 	mov	dptr,#_pre_process_record_kb_keycode_10000_594
      009864 E0               [24]  950 	movx	a,@dptr
      009865 FE               [12]  951 	mov	r6,a
      009866 A3               [24]  952 	inc	dptr
      009867 E0               [24]  953 	movx	a,@dptr
      009868 FF               [12]  954 	mov	r7,a
      009869 90 09 D7         [24]  955 	mov	dptr,#_pre_process_record_kb_PARM_2
      00986C 12 95 CF         [24]  956 	lcall	_ak820_outline_0004
      00986F 90 09 DC         [24]  957 	mov	dptr,#_pre_process_record_user_PARM_2
      009872 12 9B BA         [24]  958 	lcall	_ak820_outline_0000
                                    959 ;	quantum/quantum.c:200: }
      009875 02 98 78         [24]  960 	ljmp	_pre_process_record_user
                                    961 ;------------------------------------------------------------
                                    962 ;Allocation info for local variables in function 'pre_process_record_user'
                                    963 ;------------------------------------------------------------
                                    964 ;record        Allocated with name '_pre_process_record_user_PARM_2'
                                    965 ;keycode       Allocated with name '_pre_process_record_user_keycode_10000_596'
                                    966 ;------------------------------------------------------------
                                    967 ;	quantum/quantum.c:202: __attribute__((weak)) bool pre_process_record_user(uint16_t keycode, keyrecord_t *record) {
                                    968 ;	-----------------------------------------
                                    969 ;	 function pre_process_record_user
                                    970 ;	-----------------------------------------
      009878                        971 _pre_process_record_user:
                                    972 ;	quantum/quantum.c:203: return true;
      009878 75 82 01         [24]  973 	mov	dpl, #0x01
                                    974 ;	quantum/quantum.c:204: }
      00987B 22               [24]  975 	ret
                                    976 ;------------------------------------------------------------
                                    977 ;Allocation info for local variables in function 'process_action_kb'
                                    978 ;------------------------------------------------------------
                                    979 ;record        Allocated with name '_process_action_kb_record_10000_598'
                                    980 ;------------------------------------------------------------
                                    981 ;	quantum/quantum.c:206: __attribute__((weak)) bool process_action_kb(keyrecord_t *record) {
                                    982 ;	-----------------------------------------
                                    983 ;	 function process_action_kb
                                    984 ;	-----------------------------------------
      00987C                        985 _process_action_kb:
                                    986 ;	quantum/quantum.c:207: return true;
      00987C 75 82 01         [24]  987 	mov	dpl, #0x01
                                    988 ;	quantum/quantum.c:208: }
      00987F 22               [24]  989 	ret
                                    990 ;------------------------------------------------------------
                                    991 ;Allocation info for local variables in function 'process_record_kb'
                                    992 ;------------------------------------------------------------
                                    993 ;record        Allocated with name '_process_record_kb_PARM_2'
                                    994 ;keycode       Allocated with name '_process_record_kb_keycode_10000_600'
                                    995 ;------------------------------------------------------------
                                    996 ;	quantum/quantum.c:210: __attribute__((weak)) bool process_record_kb(uint16_t keycode, keyrecord_t *record) {
                                    997 ;	-----------------------------------------
                                    998 ;	 function process_record_kb
                                    999 ;	-----------------------------------------
      009880                       1000 _process_record_kb:
      009880 AF 83            [24] 1001 	mov	r7,dph
      009882 E5 82            [12] 1002 	mov	a,dpl
      009884 90 09 E2         [24] 1003 	mov	dptr,#_process_record_kb_keycode_10000_600
      009887 F0               [24] 1004 	movx	@dptr,a
      009888 EF               [12] 1005 	mov	a,r7
      009889 A3               [24] 1006 	inc	dptr
      00988A F0               [24] 1007 	movx	@dptr,a
                                   1008 ;	quantum/quantum.c:211: return process_record_user(keycode, record);
      00988B 90 09 E2         [24] 1009 	mov	dptr,#_process_record_kb_keycode_10000_600
      00988E E0               [24] 1010 	movx	a,@dptr
      00988F FE               [12] 1011 	mov	r6,a
      009890 A3               [24] 1012 	inc	dptr
      009891 E0               [24] 1013 	movx	a,@dptr
      009892 FF               [12] 1014 	mov	r7,a
      009893 90 09 DF         [24] 1015 	mov	dptr,#_process_record_kb_PARM_2
      009896 12 95 CF         [24] 1016 	lcall	_ak820_outline_0004
      009899 90 09 E4         [24] 1017 	mov	dptr,#_process_record_user_PARM_2
      00989C 12 9B BA         [24] 1018 	lcall	_ak820_outline_0000
                                   1019 ;	quantum/quantum.c:212: }
      00989F 02 98 A2         [24] 1020 	ljmp	_process_record_user
                                   1021 ;------------------------------------------------------------
                                   1022 ;Allocation info for local variables in function 'process_record_user'
                                   1023 ;------------------------------------------------------------
                                   1024 ;record        Allocated with name '_process_record_user_PARM_2'
                                   1025 ;keycode       Allocated with name '_process_record_user_keycode_10000_602'
                                   1026 ;------------------------------------------------------------
                                   1027 ;	quantum/quantum.c:214: __attribute__((weak)) bool process_record_user(uint16_t keycode, keyrecord_t *record) {
                                   1028 ;	-----------------------------------------
                                   1029 ;	 function process_record_user
                                   1030 ;	-----------------------------------------
      0098A2                       1031 _process_record_user:
                                   1032 ;	quantum/quantum.c:215: return true;
      0098A2 75 82 01         [24] 1033 	mov	dpl, #0x01
                                   1034 ;	quantum/quantum.c:216: }
      0098A5 22               [24] 1035 	ret
                                   1036 ;------------------------------------------------------------
                                   1037 ;Allocation info for local variables in function 'post_process_record_kb'
                                   1038 ;------------------------------------------------------------
                                   1039 ;record        Allocated with name '_post_process_record_kb_PARM_2'
                                   1040 ;keycode       Allocated with name '_post_process_record_kb_keycode_10000_604'
                                   1041 ;------------------------------------------------------------
                                   1042 ;	quantum/quantum.c:218: __attribute__((weak)) void post_process_record_kb(uint16_t keycode, keyrecord_t *record) {
                                   1043 ;	-----------------------------------------
                                   1044 ;	 function post_process_record_kb
                                   1045 ;	-----------------------------------------
      0098A6                       1046 _post_process_record_kb:
      0098A6 AF 83            [24] 1047 	mov	r7,dph
      0098A8 E5 82            [12] 1048 	mov	a,dpl
      0098AA 90 09 EA         [24] 1049 	mov	dptr,#_post_process_record_kb_keycode_10000_604
      0098AD F0               [24] 1050 	movx	@dptr,a
      0098AE EF               [12] 1051 	mov	a,r7
      0098AF A3               [24] 1052 	inc	dptr
      0098B0 F0               [24] 1053 	movx	@dptr,a
                                   1054 ;	quantum/quantum.c:219: post_process_record_user(keycode, record);
      0098B1 90 09 EA         [24] 1055 	mov	dptr,#_post_process_record_kb_keycode_10000_604
      0098B4 E0               [24] 1056 	movx	a,@dptr
      0098B5 FE               [12] 1057 	mov	r6,a
      0098B6 A3               [24] 1058 	inc	dptr
      0098B7 E0               [24] 1059 	movx	a,@dptr
      0098B8 FF               [12] 1060 	mov	r7,a
      0098B9 90 09 E7         [24] 1061 	mov	dptr,#_post_process_record_kb_PARM_2
      0098BC 12 95 CF         [24] 1062 	lcall	_ak820_outline_0004
      0098BF 90 09 EC         [24] 1063 	mov	dptr,#_post_process_record_user_PARM_2
      0098C2 12 9B BA         [24] 1064 	lcall	_ak820_outline_0000
                                   1065 ;	quantum/quantum.c:220: }
      0098C5 02 98 C8         [24] 1066 	ljmp	_post_process_record_user
                                   1067 ;------------------------------------------------------------
                                   1068 ;Allocation info for local variables in function 'post_process_record_user'
                                   1069 ;------------------------------------------------------------
                                   1070 ;record        Allocated with name '_post_process_record_user_PARM_2'
                                   1071 ;keycode       Allocated with name '_post_process_record_user_keycode_10000_606'
                                   1072 ;------------------------------------------------------------
                                   1073 ;	quantum/quantum.c:222: __attribute__((weak)) void post_process_record_user(uint16_t keycode, keyrecord_t *record) {}
                                   1074 ;	-----------------------------------------
                                   1075 ;	 function post_process_record_user
                                   1076 ;	-----------------------------------------
      0098C8                       1077 _post_process_record_user:
      0098C8 22               [24] 1078 	ret
                                   1079 ;------------------------------------------------------------
                                   1080 ;Allocation info for local variables in function 'shutdown_quantum'
                                   1081 ;------------------------------------------------------------
                                   1082 ;i             Allocated with name '_shutdown_quantum_i_30000_612'
                                   1083 ;------------------------------------------------------------
                                   1084 ;	quantum/quantum.c:224: void shutdown_quantum(void) {
                                   1085 ;	-----------------------------------------
                                   1086 ;	 function shutdown_quantum
                                   1087 ;	-----------------------------------------
      0098C9                       1088 _shutdown_quantum:
                                   1089 ;	quantum/quantum.c:225: clear_keyboard();
      0098C9 12 73 94         [24] 1090 	lcall	_clear_keyboard
                                   1091 ;	quantum/quantum.c:240: shutdown_user();
      0098CC 12 9B B9         [24] 1092 	lcall	_shutdown_user
                                   1093 ;	quantum/quantum.c:241: wait_ms(250);
      0098CF 7F FA            [12] 1094 	mov	r7,#0xfa
      0098D1                       1095 00106$:
      0098D1 EF               [12] 1096 	mov	a,r7
      0098D2 60 09            [24] 1097 	jz	00108$
      0098D4 90 00 01         [24] 1098 	mov	dptr,#0x0001
      0098D7 12 52 7D         [24] 1099 	lcall	_mDelaymS
      0098DA 1F               [12] 1100 	dec	r7
      0098DB 80 F4            [24] 1101 	sjmp	00106$
      0098DD                       1102 00108$:
                                   1103 ;	quantum/quantum.c:246: }
      0098DD 22               [24] 1104 	ret
                                   1105 ;------------------------------------------------------------
                                   1106 ;Allocation info for local variables in function 'reset_keyboard'
                                   1107 ;------------------------------------------------------------
                                   1108 ;	quantum/quantum.c:248: void reset_keyboard(void) {
                                   1109 ;	-----------------------------------------
                                   1110 ;	 function reset_keyboard
                                   1111 ;	-----------------------------------------
      0098DE                       1112 _reset_keyboard:
                                   1113 ;	quantum/quantum.c:249: shutdown_quantum();
      0098DE 12 98 C9         [24] 1114 	lcall	_shutdown_quantum
                                   1115 ;	quantum/quantum.c:250: bootloader_jump();
                                   1116 ;	quantum/quantum.c:251: }
      0098E1 02 34 94         [24] 1117 	ljmp	_bootloader_jump
                                   1118 ;------------------------------------------------------------
                                   1119 ;Allocation info for local variables in function 'soft_reset_keyboard'
                                   1120 ;------------------------------------------------------------
                                   1121 ;	quantum/quantum.c:253: void soft_reset_keyboard(void) {
                                   1122 ;	-----------------------------------------
                                   1123 ;	 function soft_reset_keyboard
                                   1124 ;	-----------------------------------------
      0098E4                       1125 _soft_reset_keyboard:
                                   1126 ;	quantum/quantum.c:254: shutdown_quantum();
      0098E4 12 98 C9         [24] 1127 	lcall	_shutdown_quantum
                                   1128 ;	quantum/quantum.c:255: mcu_reset();
                                   1129 ;	quantum/quantum.c:256: }
      0098E7 02 34 87         [24] 1130 	ljmp	_mcu_reset
                                   1131 ;------------------------------------------------------------
                                   1132 ;Allocation info for local variables in function 'get_record_keycode'
                                   1133 ;------------------------------------------------------------
                                   1134 ;update_layer_cache Allocated with name '_get_record_keycode_PARM_2'
                                   1135 ;record        Allocated with name '_get_record_keycode_record_10000_618'
                                   1136 ;------------------------------------------------------------
                                   1137 ;	quantum/quantum.c:259: uint16_t get_record_keycode(keyrecord_t *record, bool update_layer_cache) {
                                   1138 ;	-----------------------------------------
                                   1139 ;	 function get_record_keycode
                                   1140 ;	-----------------------------------------
      0098EA                       1141 _get_record_keycode:
      0098EA AF F0            [24] 1142 	mov	r7,b
      0098EC AE 83            [24] 1143 	mov	r6,dph
      0098EE E5 82            [12] 1144 	mov	a,dpl
      0098F0 90 09 F0         [24] 1145 	mov	dptr,#_get_record_keycode_record_10000_618
      0098F3 F0               [24] 1146 	movx	@dptr,a
      0098F4 EE               [12] 1147 	mov	a,r6
      0098F5 A3               [24] 1148 	inc	dptr
      0098F6 F0               [24] 1149 	movx	@dptr,a
      0098F7 EF               [12] 1150 	mov	a,r7
      0098F8 A3               [24] 1151 	inc	dptr
      0098F9 F0               [24] 1152 	movx	@dptr,a
                                   1153 ;	quantum/quantum.c:261: if (record->keycode) {
      0098FA 90 09 F0         [24] 1154 	mov	dptr,#_get_record_keycode_record_10000_618
      0098FD 12 73 B8         [24] 1155 	lcall	_ak820_outline_0002
      009900 74 06            [12] 1156 	mov	a,#0x06
      009902 2D               [12] 1157 	add	a, r5
      009903 FB               [12] 1158 	mov	r3,a
      009904 E4               [12] 1159 	clr	a
      009905 3E               [12] 1160 	addc	a, r6
      009906 FA               [12] 1161 	mov	r2,a
      009907 8F 04            [24] 1162 	mov	ar4,r7
      009909 8B 82            [24] 1163 	mov	dpl,r3
      00990B 8A 83            [24] 1164 	mov	dph,r2
      00990D 8C F0            [24] 1165 	mov	b,r4
      00990F 12 B5 9A         [24] 1166 	lcall	__gptrget
      009912 FB               [12] 1167 	mov	r3,a
      009913 A3               [24] 1168 	inc	dptr
      009914 12 B5 9A         [24] 1169 	lcall	__gptrget
      009917 FC               [12] 1170 	mov	r4,a
      009918 4B               [12] 1171 	orl	a,r3
      009919 60 05            [24] 1172 	jz	00102$
                                   1173 ;	quantum/quantum.c:262: return record->keycode;
      00991B 8B 82            [24] 1174 	mov	dpl, r3
      00991D 8C 83            [24] 1175 	mov	dph, r4
      00991F 22               [24] 1176 	ret
      009920                       1177 00102$:
                                   1178 ;	quantum/quantum.c:265: return get_event_keycode(record->event, update_layer_cache);
      009920 90 09 EF         [24] 1179 	mov	dptr,#_get_record_keycode_PARM_2
      009923 E0               [24] 1180 	movx	a,@dptr
      009924 FC               [12] 1181 	mov	r4,a
      009925 90 0B 90         [24] 1182 	mov	dptr,#___memcpy_PARM_2
      009928 12 73 D9         [24] 1183 	lcall	_ak820_outline_0015
      00992B 90 0B 93         [24] 1184 	mov	dptr,#___memcpy_PARM_3
      00992E 74 06            [12] 1185 	mov	a,#0x06
      009930 F0               [24] 1186 	movx	@dptr,a
      009931 E4               [12] 1187 	clr	a
      009932 A3               [24] 1188 	inc	dptr
      009933 F0               [24] 1189 	movx	@dptr,a
      009934 90 09 F3         [24] 1190 	mov	dptr,#_get_event_keycode_PARM_1
      009937 F5 F0            [12] 1191 	mov	b,a
      009939 C0 04            [24] 1192 	push	ar4
      00993B 12 B4 C1         [24] 1193 	lcall	___memcpy
      00993E D0 04            [24] 1194 	pop	ar4
      009940 8C 82            [24] 1195 	mov	dpl, r4
                                   1196 ;	quantum/quantum.c:266: }
      009942 02 99 45         [24] 1197 	ljmp	_get_event_keycode
                                   1198 ;------------------------------------------------------------
                                   1199 ;Allocation info for local variables in function 'get_event_keycode'
                                   1200 ;------------------------------------------------------------
                                   1201 ;event         Allocated with name '_get_event_keycode_PARM_1'
                                   1202 ;update_layer_cache Allocated with name '_get_event_keycode_update_layer_cache_10000_622'
                                   1203 ;layer         Allocated with name '_get_event_keycode_layer_30000_625'
                                   1204 ;------------------------------------------------------------
                                   1205 ;	quantum/quantum.c:274: uint16_t get_event_keycode(keyevent_t event, bool update_layer_cache) {
                                   1206 ;	-----------------------------------------
                                   1207 ;	 function get_event_keycode
                                   1208 ;	-----------------------------------------
      009945                       1209 _get_event_keycode:
      009945 E5 82            [12] 1210 	mov	a,dpl
      009947 90 09 F9         [24] 1211 	mov	dptr,#_get_event_keycode_update_layer_cache_10000_622
      00994A F0               [24] 1212 	movx	@dptr,a
                                   1213 ;	quantum/quantum.c:277: if (!disable_action_cache) {
      00994B 90 0B AC         [24] 1214 	mov	dptr,#_disable_action_cache
      00994E E0               [24] 1215 	movx	a,@dptr
      00994F 70 3E            [24] 1216 	jnz	00105$
                                   1217 ;	quantum/quantum.c:280: if (event.pressed && update_layer_cache) {
      009951 90 09 F8         [24] 1218 	mov	dptr,#(_get_event_keycode_PARM_1 + 0x0005)
      009954 E0               [24] 1219 	movx	a,@dptr
      009955 60 2A            [24] 1220 	jz	00102$
      009957 90 09 F9         [24] 1221 	mov	dptr,#_get_event_keycode_update_layer_cache_10000_622
      00995A E0               [24] 1222 	movx	a,@dptr
      00995B 60 24            [24] 1223 	jz	00102$
                                   1224 ;	quantum/quantum.c:281: layer = layer_switch_get_layer(event.key);
      00995D 12 9B C7         [24] 1225 	lcall	_ak820_outline_0005
      009960 90 08 8A         [24] 1226 	mov	dptr,#_layer_switch_get_layer_PARM_1
      009963 F5 F0            [12] 1227 	mov	b,a
      009965 12 B4 C1         [24] 1228 	lcall	___memcpy
      009968 12 76 E3         [24] 1229 	lcall	_layer_switch_get_layer
      00996B AF 82            [24] 1230 	mov	r7, dpl
                                   1231 ;	quantum/quantum.c:282: update_source_layers_cache(event.key, layer);
      00996D 12 9B C7         [24] 1232 	lcall	_ak820_outline_0005
      009970 90 08 82         [24] 1233 	mov	dptr,#_update_source_layers_cache_PARM_1
      009973 F5 F0            [12] 1234 	mov	b,a
      009975 C0 07            [24] 1235 	push	ar7
      009977 12 B4 C1         [24] 1236 	lcall	___memcpy
      00997A D0 07            [24] 1237 	pop	ar7
      00997C 8F 82            [24] 1238 	mov	dpl, r7
      00997E 12 75 B5         [24] 1239 	lcall	_update_source_layers_cache
      009981                       1240 00102$:
                                   1241 ;	quantum/quantum.c:285: return read_source_keycode_cache(event.key);
      009981 12 9B C7         [24] 1242 	lcall	_ak820_outline_0005
      009984 90 08 85         [24] 1243 	mov	dptr,#_read_source_keycode_cache_PARM_1
      009987 F5 F0            [12] 1244 	mov	b,a
      009989 12 B4 C1         [24] 1245 	lcall	___memcpy
      00998C 02 76 19         [24] 1246 	ljmp	_read_source_keycode_cache
      00998F                       1247 00105$:
                                   1248 ;	quantum/quantum.c:297: return keymap_key_to_keycode(layer_switch_get_layer(event.key), event.key);
      00998F 12 9B C7         [24] 1249 	lcall	_ak820_outline_0005
      009992 90 08 8A         [24] 1250 	mov	dptr,#_layer_switch_get_layer_PARM_1
      009995 F5 F0            [12] 1251 	mov	b,a
      009997 12 B4 C1         [24] 1252 	lcall	___memcpy
      00999A 12 76 E3         [24] 1253 	lcall	_layer_switch_get_layer
      00999D AF 82            [24] 1254 	mov	r7, dpl
      00999F 12 9B C7         [24] 1255 	lcall	_ak820_outline_0005
      0099A2 90 09 90         [24] 1256 	mov	dptr,#_keymap_key_to_keycode_PARM_2
      0099A5 F5 F0            [12] 1257 	mov	b,a
      0099A7 C0 07            [24] 1258 	push	ar7
      0099A9 12 B4 C1         [24] 1259 	lcall	___memcpy
      0099AC D0 07            [24] 1260 	pop	ar7
      0099AE 8F 82            [24] 1261 	mov	dpl, r7
                                   1262 ;	quantum/quantum.c:298: }
      0099B0 02 8F 7D         [24] 1263 	ljmp	_keymap_key_to_keycode
                                   1264 ;------------------------------------------------------------
                                   1265 ;Allocation info for local variables in function 'pre_process_record_quantum'
                                   1266 ;------------------------------------------------------------
                                   1267 ;record        Allocated with name '_pre_process_record_quantum_record_10000_628'
                                   1268 ;keycode       Allocated with name '_pre_process_record_quantum_keycode_10000_629'
                                   1269 ;------------------------------------------------------------
                                   1270 ;	quantum/quantum.c:301: bool pre_process_record_quantum(keyrecord_t *record) {
                                   1271 ;	-----------------------------------------
                                   1272 ;	 function pre_process_record_quantum
                                   1273 ;	-----------------------------------------
      0099B3                       1274 _pre_process_record_quantum:
      0099B3 AF F0            [24] 1275 	mov	r7,b
      0099B5 AE 83            [24] 1276 	mov	r6,dph
      0099B7 E5 82            [12] 1277 	mov	a,dpl
      0099B9 90 09 FA         [24] 1278 	mov	dptr,#_pre_process_record_quantum_record_10000_628
      0099BC F0               [24] 1279 	movx	@dptr,a
      0099BD EE               [12] 1280 	mov	a,r6
      0099BE A3               [24] 1281 	inc	dptr
      0099BF F0               [24] 1282 	movx	@dptr,a
      0099C0 EF               [12] 1283 	mov	a,r7
      0099C1 A3               [24] 1284 	inc	dptr
      0099C2 F0               [24] 1285 	movx	@dptr,a
                                   1286 ;	quantum/quantum.c:302: uint16_t keycode = get_record_keycode(record, true);
      0099C3 90 09 FA         [24] 1287 	mov	dptr,#_pre_process_record_quantum_record_10000_628
      0099C6 12 73 B8         [24] 1288 	lcall	_ak820_outline_0002
      0099C9 90 09 EF         [24] 1289 	mov	dptr,#_get_record_keycode_PARM_2
      0099CC 74 01            [12] 1290 	mov	a,#0x01
      0099CE F0               [24] 1291 	movx	@dptr,a
      0099CF 8D 82            [24] 1292 	mov	dpl, r5
      0099D1 8E 83            [24] 1293 	mov	dph, r6
      0099D3 8F F0            [24] 1294 	mov	b, r7
      0099D5 12 98 EA         [24] 1295 	lcall	_get_record_keycode
      0099D8 AE 82            [24] 1296 	mov	r6, dpl
      0099DA AF 83            [24] 1297 	mov	r7, dph
                                   1298 ;	quantum/quantum.c:303: return pre_process_record_kb(keycode, record) &&
      0099DC 90 09 FA         [24] 1299 	mov	dptr,#_pre_process_record_quantum_record_10000_628
      0099DF 12 95 CF         [24] 1300 	lcall	_ak820_outline_0004
      0099E2 90 09 D7         [24] 1301 	mov	dptr,#_pre_process_record_kb_PARM_2
      0099E5 12 9B BA         [24] 1302 	lcall	_ak820_outline_0000
      0099E8 12 98 56         [24] 1303 	lcall	_pre_process_record_kb
      0099EB E5 82            [12] 1304 	mov	a, dpl
      0099ED 70 04            [24] 1305 	jnz	00104$
                                   1306 ;	quantum/quantum.c:307: true;
                                   1307 ;	assignBit
      0099EF C2 0F            [12] 1308 	clr	_pre_process_record_quantum_sloc0_1_0
      0099F1 80 02            [24] 1309 	sjmp	00105$
      0099F3                       1310 00104$:
                                   1311 ;	assignBit
      0099F3 D2 0F            [12] 1312 	setb	_pre_process_record_quantum_sloc0_1_0
      0099F5                       1313 00105$:
      0099F5 A2 0F            [12] 1314 	mov	c,_pre_process_record_quantum_sloc0_1_0
      0099F7 E4               [12] 1315 	clr	a
      0099F8 33               [12] 1316 	rlc	a
      0099F9 F5 82            [12] 1317 	mov	dpl, a
                                   1318 ;	quantum/quantum.c:308: }
      0099FB 22               [24] 1319 	ret
                                   1320 ;------------------------------------------------------------
                                   1321 ;Allocation info for local variables in function 'post_process_record_quantum'
                                   1322 ;------------------------------------------------------------
                                   1323 ;record        Allocated with name '_post_process_record_quantum_record_10000_630'
                                   1324 ;keycode       Allocated with name '_post_process_record_quantum_keycode_10000_631'
                                   1325 ;------------------------------------------------------------
                                   1326 ;	quantum/quantum.c:311: void post_process_record_quantum(keyrecord_t *record) {
                                   1327 ;	-----------------------------------------
                                   1328 ;	 function post_process_record_quantum
                                   1329 ;	-----------------------------------------
      0099FC                       1330 _post_process_record_quantum:
      0099FC AF F0            [24] 1331 	mov	r7,b
      0099FE AE 83            [24] 1332 	mov	r6,dph
      009A00 E5 82            [12] 1333 	mov	a,dpl
      009A02 90 09 FD         [24] 1334 	mov	dptr,#_post_process_record_quantum_record_10000_630
      009A05 F0               [24] 1335 	movx	@dptr,a
      009A06 EE               [12] 1336 	mov	a,r6
      009A07 A3               [24] 1337 	inc	dptr
      009A08 F0               [24] 1338 	movx	@dptr,a
      009A09 EF               [12] 1339 	mov	a,r7
      009A0A A3               [24] 1340 	inc	dptr
      009A0B F0               [24] 1341 	movx	@dptr,a
                                   1342 ;	quantum/quantum.c:312: uint16_t keycode = get_record_keycode(record, false);
      009A0C 90 09 FD         [24] 1343 	mov	dptr,#_post_process_record_quantum_record_10000_630
      009A0F 12 73 B8         [24] 1344 	lcall	_ak820_outline_0002
      009A12 90 09 EF         [24] 1345 	mov	dptr,#_get_record_keycode_PARM_2
      009A15 E4               [12] 1346 	clr	a
      009A16 F0               [24] 1347 	movx	@dptr,a
      009A17 8D 82            [24] 1348 	mov	dpl, r5
      009A19 8E 83            [24] 1349 	mov	dph, r6
      009A1B 8F F0            [24] 1350 	mov	b, r7
      009A1D 12 98 EA         [24] 1351 	lcall	_get_record_keycode
      009A20 AE 82            [24] 1352 	mov	r6, dpl
      009A22 AF 83            [24] 1353 	mov	r7, dph
                                   1354 ;	quantum/quantum.c:313: post_process_record_kb(keycode, record);
      009A24 90 09 FD         [24] 1355 	mov	dptr,#_post_process_record_quantum_record_10000_630
      009A27 12 95 CF         [24] 1356 	lcall	_ak820_outline_0004
      009A2A 90 09 E7         [24] 1357 	mov	dptr,#_post_process_record_kb_PARM_2
      009A2D 12 9B BA         [24] 1358 	lcall	_ak820_outline_0000
                                   1359 ;	quantum/quantum.c:314: }
      009A30 02 98 A6         [24] 1360 	ljmp	_post_process_record_kb
                                   1361 ;------------------------------------------------------------
                                   1362 ;Allocation info for local variables in function 'process_record_quantum'
                                   1363 ;------------------------------------------------------------
                                   1364 ;record        Allocated with name '_process_record_quantum_record_10000_632'
                                   1365 ;keycode       Allocated with name '_process_record_quantum_keycode_10000_633'
                                   1366 ;------------------------------------------------------------
                                   1367 ;	quantum/quantum.c:316: bool process_record_quantum(keyrecord_t *record) {
                                   1368 ;	-----------------------------------------
                                   1369 ;	 function process_record_quantum
                                   1370 ;	-----------------------------------------
      009A33                       1371 _process_record_quantum:
      009A33 AF F0            [24] 1372 	mov	r7,b
      009A35 AE 83            [24] 1373 	mov	r6,dph
      009A37 E5 82            [12] 1374 	mov	a,dpl
      009A39 90 0A 00         [24] 1375 	mov	dptr,#_process_record_quantum_record_10000_632
      009A3C F0               [24] 1376 	movx	@dptr,a
      009A3D EE               [12] 1377 	mov	a,r6
      009A3E A3               [24] 1378 	inc	dptr
      009A3F F0               [24] 1379 	movx	@dptr,a
      009A40 EF               [12] 1380 	mov	a,r7
      009A41 A3               [24] 1381 	inc	dptr
      009A42 F0               [24] 1382 	movx	@dptr,a
                                   1383 ;	quantum/quantum.c:317: uint16_t keycode = get_record_keycode(record, true);
      009A43 90 0A 00         [24] 1384 	mov	dptr,#_process_record_quantum_record_10000_632
      009A46 12 73 B8         [24] 1385 	lcall	_ak820_outline_0002
      009A49 90 09 EF         [24] 1386 	mov	dptr,#_get_record_keycode_PARM_2
      009A4C 74 01            [12] 1387 	mov	a,#0x01
      009A4E F0               [24] 1388 	movx	@dptr,a
      009A4F 8D 82            [24] 1389 	mov	dpl, r5
      009A51 8E 83            [24] 1390 	mov	dph, r6
      009A53 8F F0            [24] 1391 	mov	b, r7
      009A55 12 98 EA         [24] 1392 	lcall	_get_record_keycode
      009A58 AE 82            [24] 1393 	mov	r6, dpl
      009A5A AF 83            [24] 1394 	mov	r7, dph
                                   1395 ;	quantum/quantum.c:318: return process_record_quantum_helper(keycode, record);
      009A5C 90 0A 00         [24] 1396 	mov	dptr,#_process_record_quantum_record_10000_632
      009A5F 12 95 CF         [24] 1397 	lcall	_ak820_outline_0004
      009A62 90 0A 03         [24] 1398 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009A65 12 9B BA         [24] 1399 	lcall	_ak820_outline_0000
                                   1400 ;	quantum/quantum.c:319: }
      009A68 02 9A 6B         [24] 1401 	ljmp	_process_record_quantum_helper
                                   1402 ;------------------------------------------------------------
                                   1403 ;Allocation info for local variables in function 'process_record_quantum_helper'
                                   1404 ;------------------------------------------------------------
                                   1405 ;record        Allocated with name '_process_record_quantum_helper_PARM_2'
                                   1406 ;keycode       Allocated with name '_process_record_quantum_helper_keycode_10000_634'
                                   1407 ;------------------------------------------------------------
                                   1408 ;	quantum/quantum.c:323: bool process_record_quantum_helper(uint16_t keycode, keyrecord_t *record) {
                                   1409 ;	-----------------------------------------
                                   1410 ;	 function process_record_quantum_helper
                                   1411 ;	-----------------------------------------
      009A6B                       1412 _process_record_quantum_helper:
      009A6B AF 83            [24] 1413 	mov	r7,dph
      009A6D E5 82            [12] 1414 	mov	a,dpl
      009A6F 90 0A 06         [24] 1415 	mov	dptr,#_process_record_quantum_helper_keycode_10000_634
      009A72 F0               [24] 1416 	movx	@dptr,a
      009A73 EF               [12] 1417 	mov	a,r7
      009A74 A3               [24] 1418 	inc	dptr
      009A75 F0               [24] 1419 	movx	@dptr,a
                                   1420 ;	quantum/quantum.c:368: process_last_key(keycode, record) && process_repeat_key(keycode, record) &&
      009A76 90 0A 06         [24] 1421 	mov	dptr,#_process_record_quantum_helper_keycode_10000_634
      009A79 E0               [24] 1422 	movx	a,@dptr
      009A7A FE               [12] 1423 	mov	r6,a
      009A7B A3               [24] 1424 	inc	dptr
      009A7C E0               [24] 1425 	movx	a,@dptr
      009A7D FF               [12] 1426 	mov	r7,a
      009A7E 90 0A 03         [24] 1427 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009A81 12 95 CF         [24] 1428 	lcall	_ak820_outline_0004
      009A84 90 09 BA         [24] 1429 	mov	dptr,#_process_last_key_PARM_2
      009A87 12 9B BA         [24] 1430 	lcall	_ak820_outline_0000
      009A8A C0 07            [24] 1431 	push	ar7
      009A8C C0 06            [24] 1432 	push	ar6
      009A8E 12 94 F7         [24] 1433 	lcall	_process_last_key
      009A91 E5 82            [12] 1434 	mov	a, dpl
      009A93 D0 06            [24] 1435 	pop	ar6
      009A95 D0 07            [24] 1436 	pop	ar7
      009A97 70 03            [24] 1437 	jnz	00196$
      009A99 02 9B 62         [24] 1438 	ljmp	00101$
      009A9C                       1439 00196$:
      009A9C 90 0A 03         [24] 1440 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009A9F 12 95 CF         [24] 1441 	lcall	_ak820_outline_0004
      009AA2 90 09 C0         [24] 1442 	mov	dptr,#_process_repeat_key_PARM_2
      009AA5 12 9B BA         [24] 1443 	lcall	_ak820_outline_0000
      009AA8 C0 07            [24] 1444 	push	ar7
      009AAA C0 06            [24] 1445 	push	ar6
      009AAC 12 95 7B         [24] 1446 	lcall	_process_repeat_key
      009AAF E5 82            [12] 1447 	mov	a, dpl
      009AB1 D0 06            [24] 1448 	pop	ar6
      009AB3 D0 07            [24] 1449 	pop	ar7
      009AB5 70 03            [24] 1450 	jnz	00197$
      009AB7 02 9B 62         [24] 1451 	ljmp	00101$
      009ABA                       1452 00197$:
                                   1453 ;	quantum/quantum.c:377: process_record_via(keycode, record) &&
      009ABA 90 0A 03         [24] 1454 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009ABD 12 95 CF         [24] 1455 	lcall	_ak820_outline_0004
      009AC0 90 0A 4B         [24] 1456 	mov	dptr,#_process_record_via_PARM_2
      009AC3 12 9B BA         [24] 1457 	lcall	_ak820_outline_0000
      009AC6 C0 07            [24] 1458 	push	ar7
      009AC8 C0 06            [24] 1459 	push	ar6
      009ACA 12 A1 41         [24] 1460 	lcall	_process_record_via
      009ACD E5 82            [12] 1461 	mov	a, dpl
      009ACF D0 06            [24] 1462 	pop	ar6
      009AD1 D0 07            [24] 1463 	pop	ar7
      009AD3 70 03            [24] 1464 	jnz	00198$
      009AD5 02 9B 62         [24] 1465 	ljmp	00101$
      009AD8                       1466 00198$:
                                   1467 ;	quantum/quantum.c:387: process_record_kb(keycode, record) &&
      009AD8 90 0A 03         [24] 1468 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009ADB 12 95 CF         [24] 1469 	lcall	_ak820_outline_0004
      009ADE 90 09 DF         [24] 1470 	mov	dptr,#_process_record_kb_PARM_2
      009AE1 12 9B BA         [24] 1471 	lcall	_ak820_outline_0000
      009AE4 C0 07            [24] 1472 	push	ar7
      009AE6 C0 06            [24] 1473 	push	ar6
      009AE8 12 98 80         [24] 1474 	lcall	_process_record_kb
      009AEB E5 82            [12] 1475 	mov	a, dpl
      009AED D0 06            [24] 1476 	pop	ar6
      009AEF D0 07            [24] 1477 	pop	ar7
      009AF1 70 03            [24] 1478 	jnz	00199$
      009AF3 02 9B 62         [24] 1479 	ljmp	00101$
      009AF6                       1480 00199$:
                                   1481 ;	quantum/quantum.c:410: process_caps_word(keycode, record) &&
      009AF6 90 0A 03         [24] 1482 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009AF9 12 95 CF         [24] 1483 	lcall	_ak820_outline_0004
      009AFC 90 09 A2         [24] 1484 	mov	dptr,#_process_caps_word_PARM_2
      009AFF 12 9B BA         [24] 1485 	lcall	_ak820_outline_0000
      009B02 C0 07            [24] 1486 	push	ar7
      009B04 C0 06            [24] 1487 	push	ar6
      009B06 12 91 B3         [24] 1488 	lcall	_process_caps_word
      009B09 E5 82            [12] 1489 	mov	a, dpl
      009B0B D0 06            [24] 1490 	pop	ar6
      009B0D D0 07            [24] 1491 	pop	ar7
      009B0F 60 51            [24] 1492 	jz	00101$
                                   1493 ;	quantum/quantum.c:437: process_grave_esc(keycode, record) &&
      009B11 90 0A 03         [24] 1494 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009B14 12 95 CF         [24] 1495 	lcall	_ak820_outline_0004
      009B17 90 09 A7         [24] 1496 	mov	dptr,#_process_grave_esc_PARM_2
      009B1A 12 9B BA         [24] 1497 	lcall	_ak820_outline_0000
      009B1D C0 07            [24] 1498 	push	ar7
      009B1F C0 06            [24] 1499 	push	ar6
      009B21 12 92 DD         [24] 1500 	lcall	_process_grave_esc
      009B24 E5 82            [12] 1501 	mov	a, dpl
      009B26 D0 06            [24] 1502 	pop	ar6
      009B28 D0 07            [24] 1503 	pop	ar7
      009B2A 60 36            [24] 1504 	jz	00101$
                                   1505 ;	quantum/quantum.c:440: process_rgb(keycode, record) &&
      009B2C 90 0A 03         [24] 1506 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009B2F 12 95 CF         [24] 1507 	lcall	_ak820_outline_0004
      009B32 90 09 C5         [24] 1508 	mov	dptr,#_process_rgb_PARM_2
      009B35 12 9B BA         [24] 1509 	lcall	_ak820_outline_0000
      009B38 C0 07            [24] 1510 	push	ar7
      009B3A C0 06            [24] 1511 	push	ar6
      009B3C 12 95 D8         [24] 1512 	lcall	_process_rgb
      009B3F E5 82            [12] 1513 	mov	a, dpl
      009B41 D0 06            [24] 1514 	pop	ar6
      009B43 D0 07            [24] 1515 	pop	ar7
      009B45 60 1B            [24] 1516 	jz	00101$
                                   1517 ;	quantum/quantum.c:452: process_tri_layer(keycode, record) &&
      009B47 90 0A 03         [24] 1518 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009B4A 12 95 CF         [24] 1519 	lcall	_ak820_outline_0004
      009B4D 90 09 CB         [24] 1520 	mov	dptr,#_process_tri_layer_PARM_2
      009B50 12 9B BA         [24] 1521 	lcall	_ak820_outline_0000
      009B53 C0 07            [24] 1522 	push	ar7
      009B55 C0 06            [24] 1523 	push	ar6
      009B57 12 97 02         [24] 1524 	lcall	_process_tri_layer
      009B5A E5 82            [12] 1525 	mov	a, dpl
      009B5C D0 06            [24] 1526 	pop	ar6
      009B5E D0 07            [24] 1527 	pop	ar7
      009B60 70 04            [24] 1528 	jnz	00102$
                                   1529 ;	quantum/quantum.c:454: true)) {
      009B62                       1530 00101$:
                                   1531 ;	quantum/quantum.c:455: return false;
      009B62 75 82 00         [24] 1532 	mov	dpl, #0x00
      009B65 22               [24] 1533 	ret
      009B66                       1534 00102$:
                                   1535 ;	quantum/quantum.c:458: if (record->event.pressed) {
      009B66 90 0A 03         [24] 1536 	mov	dptr,#_process_record_quantum_helper_PARM_2
      009B69 12 95 CF         [24] 1537 	lcall	_ak820_outline_0004
      009B6C 74 05            [12] 1538 	mov	a,#0x05
      009B6E 2B               [12] 1539 	add	a, r3
      009B6F F8               [12] 1540 	mov	r0,a
      009B70 E4               [12] 1541 	clr	a
      009B71 3C               [12] 1542 	addc	a, r4
      009B72 F9               [12] 1543 	mov	r1,a
      009B73 8D 02            [24] 1544 	mov	ar2,r5
      009B75 88 82            [24] 1545 	mov	dpl,r0
      009B77 89 83            [24] 1546 	mov	dph,r1
      009B79 8A F0            [24] 1547 	mov	b,r2
      009B7B 12 B5 9A         [24] 1548 	lcall	__gptrget
      009B7E 60 30            [24] 1549 	jz	00116$
                                   1550 ;	quantum/quantum.c:459: switch (keycode) {
      009B80 BE 00 05         [24] 1551 	cjne	r6,#0x00,00205$
      009B83 BF 7C 02         [24] 1552 	cjne	r7,#0x7c,00205$
      009B86 80 10            [24] 1553 	sjmp	00111$
      009B88                       1554 00205$:
      009B88 BE 01 05         [24] 1555 	cjne	r6,#0x01,00206$
      009B8B BF 7C 02         [24] 1556 	cjne	r7,#0x7c,00206$
      009B8E 80 0F            [24] 1557 	sjmp	00112$
      009B90                       1558 00206$:
                                   1559 ;	quantum/quantum.c:461: case QK_BOOTLOADER:
      009B90 BE 03 1D         [24] 1560 	cjne	r6,#0x03,00116$
      009B93 BF 7C 1A         [24] 1561 	cjne	r7,#0x7c,00116$
      009B96 80 0E            [24] 1562 	sjmp	00113$
      009B98                       1563 00111$:
                                   1564 ;	quantum/quantum.c:462: reset_keyboard();
      009B98 12 98 DE         [24] 1565 	lcall	_reset_keyboard
                                   1566 ;	quantum/quantum.c:463: return false;
      009B9B 75 82 00         [24] 1567 	mov	dpl, #0x00
                                   1568 ;	quantum/quantum.c:464: case QK_REBOOT:
      009B9E 22               [24] 1569 	ret
      009B9F                       1570 00112$:
                                   1571 ;	quantum/quantum.c:465: soft_reset_keyboard();
      009B9F 12 98 E4         [24] 1572 	lcall	_soft_reset_keyboard
                                   1573 ;	quantum/quantum.c:466: return false;
      009BA2 75 82 00         [24] 1574 	mov	dpl, #0x00
                                   1575 ;	quantum/quantum.c:478: case QK_CLEAR_EEPROM:
      009BA5 22               [24] 1576 	ret
      009BA6                       1577 00113$:
                                   1578 ;	quantum/quantum.c:482: eeconfig_disable();
      009BA6 12 87 40         [24] 1579 	lcall	_eeconfig_disable
                                   1580 ;	quantum/quantum.c:483: soft_reset_keyboard();
      009BA9 12 98 E4         [24] 1581 	lcall	_soft_reset_keyboard
                                   1582 ;	quantum/quantum.c:485: return false;
      009BAC 75 82 00         [24] 1583 	mov	dpl, #0x00
                                   1584 ;	quantum/quantum.c:540: }
      009BAF 22               [24] 1585 	ret
      009BB0                       1586 00116$:
                                   1587 ;	quantum/quantum.c:543: return process_action_kb(record);
      009BB0 8B 82            [24] 1588 	mov	dpl, r3
      009BB2 8C 83            [24] 1589 	mov	dph, r4
      009BB4 8D F0            [24] 1590 	mov	b, r5
                                   1591 ;	quantum/quantum.c:544: }
      009BB6 02 98 7C         [24] 1592 	ljmp	_process_action_kb
                                   1593 ;------------------------------------------------------------
                                   1594 ;Allocation info for local variables in function 'set_single_persistent_default_layer'
                                   1595 ;------------------------------------------------------------
                                   1596 ;default_layer Allocated with name '_set_single_persistent_default_layer_default_layer_10000_642'
                                   1597 ;------------------------------------------------------------
                                   1598 ;	quantum/quantum.c:546: void set_single_persistent_default_layer(uint8_t default_layer) {
                                   1599 ;	-----------------------------------------
                                   1600 ;	 function shutdown_user
                                   1601 ;	-----------------------------------------
      009BB9                       1602 _shutdown_user:
      009BB9 22               [24] 1603 	ret
                                   1604 ;------------------------------------------------------------
                                   1605 ;Allocation info for local variables in function 'suspend_power_down_quantum'
                                   1606 ;------------------------------------------------------------
                                   1607 ;	quantum/quantum.c:562: void suspend_power_down_quantum(void) {
                                   1608 ;	-----------------------------------------
                                   1609 	.area CSEG    (CODE)
                                   1610 	.area CONST   (CODE)
                                   1611 	.area XINIT   (CODE)
                                   1612 	.area CABS    (ABS,CODE)
                                   1613 
                                   1614 ; Experimental exact instruction outlining.
                                   1615 	.globl _ak820_outline_0000
                                   1616 	.globl _ak820_outline_0002
                                   1617 	.globl _ak820_outline_0004
                                   1618 	.globl _ak820_outline_0005
                                   1619 	.globl _ak820_outline_0013
                                   1620 	.globl _ak820_outline_0015
                                   1621 
                                   1622 	.area CSEG (CODE)
                                   1623 ; function ak820_outline_0000
      009BBA                       1624 _ak820_outline_0000:
      009BBA EB               [12] 1625 	mov	a,r3
      009BBB F0               [24] 1626 	movx	@dptr,a
      009BBC EC               [12] 1627 	mov	a,r4
      009BBD A3               [24] 1628 	inc	dptr
      009BBE F0               [24] 1629 	movx	@dptr,a
      009BBF ED               [12] 1630 	mov	a,r5
      009BC0 A3               [24] 1631 	inc	dptr
      009BC1 F0               [24] 1632 	movx	@dptr,a
      009BC2 8E 82            [24] 1633 	mov	dpl,r6
      009BC4 8F 83            [24] 1634 	mov	dph,r7
      009BC6 22               [24] 1635 	ret
                                   1636 
                                   1637 	.area CSEG (CODE)
                                   1638 ; function ak820_outline_0005
      009BC7                       1639 _ak820_outline_0005:
      009BC7 90 0B 90         [24] 1640 	mov	dptr,#___memcpy_PARM_2
      009BCA 74 F3            [12] 1641 	mov	a,#_get_event_keycode_PARM_1
      009BCC F0               [24] 1642 	movx	@dptr,a
      009BCD 74 09            [12] 1643 	mov	a,#(_get_event_keycode_PARM_1>>8)
      009BCF A3               [24] 1644 	inc	dptr
      009BD0 F0               [24] 1645 	movx	@dptr,a
      009BD1 E4               [12] 1646 	clr	a
      009BD2 A3               [24] 1647 	inc	dptr
      009BD3 F0               [24] 1648 	movx	@dptr,a
      009BD4 90 0B 93         [24] 1649 	mov	dptr,#___memcpy_PARM_3
      009BD7 74 02            [12] 1650 	mov	a,#0x02
      009BD9 F0               [24] 1651 	movx	@dptr,a
      009BDA E4               [12] 1652 	clr	a
      009BDB A3               [24] 1653 	inc	dptr
      009BDC F0               [24] 1654 	movx	@dptr,a
      009BDD 22               [24] 1655 	ret
