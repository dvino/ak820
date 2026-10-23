                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module action_layer
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _keymap_key_to_keycode
                                     12 	.globl _action_for_keycode
                                     13 	.globl _action_for_key
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
                                    257 	.globl _layer_state
                                    258 	.globl _default_layer_state
                                    259 	.globl _update_tri_layer_PARM_3
                                    260 	.globl _update_tri_layer_PARM_2
                                    261 	.globl _update_tri_layer_state_PARM_4
                                    262 	.globl _update_tri_layer_state_PARM_3
                                    263 	.globl _update_tri_layer_state_PARM_2
                                    264 	.globl _layer_switch_get_action_PARM_1
                                    265 	.globl _layer_switch_get_layer_PARM_1
                                    266 	.globl _store_or_get_action_PARM_2
                                    267 	.globl _read_source_keycode_cache_PARM_1
                                    268 	.globl _update_source_layers_cache_PARM_1
                                    269 	.globl _update_source_keycode_cache_PARM_1
                                    270 	.globl _default_layer_state_set_user
                                    271 	.globl _default_layer_state_set_kb
                                    272 	.globl _default_layer_set
                                    273 	.globl _default_layer_or
                                    274 	.globl _default_layer_and
                                    275 	.globl _default_layer_xor
                                    276 	.globl _layer_state_set_user
                                    277 	.globl _layer_state_set_kb
                                    278 	.globl _layer_state_set
                                    279 	.globl _layer_clear
                                    280 	.globl _layer_move
                                    281 	.globl _layer_on
                                    282 	.globl _layer_off
                                    283 	.globl _layer_or
                                    284 	.globl _layer_and
                                    285 	.globl _layer_xor
                                    286 	.globl _update_source_keycode_cache
                                    287 	.globl _update_source_layers_cache
                                    288 	.globl _read_source_keycode_cache
                                    289 	.globl _store_or_get_action
                                    290 	.globl _layer_switch_get_layer
                                    291 	.globl _layer_switch_get_action
                                    292 	.globl _update_tri_layer_state
                                    293 	.globl _update_tri_layer
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
                                    556 ;--------------------------------------------------------
                                    557 ; overlayable items in internal ram
                                    558 ;--------------------------------------------------------
                                    559 ;--------------------------------------------------------
                                    560 ; indirectly addressable internal ram data
                                    561 ;--------------------------------------------------------
                                    562 	.area ISEG    (DATA)
                                    563 ;--------------------------------------------------------
                                    564 ; absolute internal ram data
                                    565 ;--------------------------------------------------------
                                    566 	.area IABS    (ABS,DATA)
                                    567 	.area IABS    (ABS,DATA)
                                    568 ;--------------------------------------------------------
                                    569 ; bit data
                                    570 ;--------------------------------------------------------
                                    571 	.area BSEG    (BIT)
                                    572 ;--------------------------------------------------------
                                    573 ; paged external ram data
                                    574 ;--------------------------------------------------------
                                    575 	.area PSEG    (PAG,XDATA)
                                    576 ;--------------------------------------------------------
                                    577 ; uninitialized external ram data
                                    578 ;--------------------------------------------------------
                                    579 	.area XSEG    (XDATA)
      000769                        580 _default_layer_state_set_user_state_10000_225:
      000769                        581 	.ds 1
      00076A                        582 _default_layer_state_set_kb_state_10000_227:
      00076A                        583 	.ds 1
      00076B                        584 _default_layer_state_set_state_10000_229:
      00076B                        585 	.ds 1
      00076C                        586 _default_layer_set_state_10000_234:
      00076C                        587 	.ds 1
      00076D                        588 _default_layer_or_state_10000_236:
      00076D                        589 	.ds 1
      00076E                        590 _default_layer_and_state_10000_238:
      00076E                        591 	.ds 1
      00076F                        592 _default_layer_xor_state_10000_240:
      00076F                        593 	.ds 1
      000770                        594 _layer_state_set_user_state_10000_242:
      000770                        595 	.ds 1
      000771                        596 _layer_state_set_kb_state_10000_244:
      000771                        597 	.ds 1
      000772                        598 _layer_state_set_state_10000_246:
      000772                        599 	.ds 1
      000773                        600 _layer_move_layer_10000_259:
      000773                        601 	.ds 1
      000774                        602 _layer_on_layer_10000_261:
      000774                        603 	.ds 1
      000775                        604 _layer_off_layer_10000_263:
      000775                        605 	.ds 1
      000776                        606 _layer_or_state_10000_267:
      000776                        607 	.ds 1
      000777                        608 _layer_and_state_10000_269:
      000777                        609 	.ds 1
      000778                        610 _layer_xor_state_10000_271:
      000778                        611 	.ds 1
      000779                        612 _source_keycodes_cache:
      000779                        613 	.ds 256
      000879                        614 _encoder_source_keycodes_cache:
      000879                        615 	.ds 2
      00087B                        616 _source_keycode_cache_slot_PARM_1:
      00087B                        617 	.ds 2
      00087D                        618 _update_source_keycode_cache_PARM_1:
      00087D                        619 	.ds 2
      00087F                        620 _update_source_keycode_cache_keycode_10000_279:
      00087F                        621 	.ds 2
      000881                        622 _update_source_layers_cache_PARM_1:
      000881                        623 	.ds 2
      000883                        624 _update_source_layers_cache_layer_10000_282:
      000883                        625 	.ds 1
      000884                        626 _read_source_keycode_cache_PARM_1:
      000884                        627 	.ds 2
      000886                        628 _store_or_get_action_PARM_2:
      000886                        629 	.ds 2
      000888                        630 _store_or_get_action_pressed_10000_290:
      000888                        631 	.ds 1
      000889                        632 _layer_switch_get_layer_PARM_1:
      000889                        633 	.ds 2
      00088B                        634 _layer_switch_get_layer_action_10000_296:
      00088B                        635 	.ds 2
      00088D                        636 _layer_switch_get_layer_layers_10001_297:
      00088D                        637 	.ds 1
      00088E                        638 _layer_switch_get_action_PARM_1:
      00088E                        639 	.ds 2
      000890                        640 _update_tri_layer_state_PARM_2:
      000890                        641 	.ds 1
      000891                        642 _update_tri_layer_state_PARM_3:
      000891                        643 	.ds 1
      000892                        644 _update_tri_layer_state_PARM_4:
      000892                        645 	.ds 1
      000893                        646 _update_tri_layer_state_state_10000_306:
      000893                        647 	.ds 1
      000894                        648 _update_tri_layer_PARM_2:
      000894                        649 	.ds 1
      000895                        650 _update_tri_layer_PARM_3:
      000895                        651 	.ds 1
      000896                        652 _update_tri_layer_layer1_10000_308:
      000896                        653 	.ds 1
                                    654 ;--------------------------------------------------------
                                    655 ; absolute external ram data
                                    656 ;--------------------------------------------------------
                                    657 	.area XABS    (ABS,XDATA)
                                    658 ;--------------------------------------------------------
                                    659 ; initialized external ram data
                                    660 ;--------------------------------------------------------
                                    661 	.area XISEG   (XDATA)
      000BAC                        662 _default_layer_state::
      000BAC                        663 	.ds 1
      000BAD                        664 _layer_state::
      000BAD                        665 	.ds 1
                                    666 	.area HOME    (CODE)
                                    667 	.area GSINIT0 (CODE)
                                    668 	.area GSINIT1 (CODE)
                                    669 	.area GSINIT2 (CODE)
                                    670 	.area GSINIT3 (CODE)
                                    671 	.area GSINIT4 (CODE)
                                    672 	.area GSINIT5 (CODE)
                                    673 	.area GSINIT  (CODE)
                                    674 	.area GSFINAL (CODE)
                                    675 	.area CSEG    (CODE)
                                    676 ;--------------------------------------------------------
                                    677 ; global & static initialisations
                                    678 ;--------------------------------------------------------
                                    679 	.area HOME    (CODE)
                                    680 	.area GSINIT  (CODE)
                                    681 	.area GSFINAL (CODE)
                                    682 	.area GSINIT  (CODE)
                                    683 ;--------------------------------------------------------
                                    684 ; Home
                                    685 ;--------------------------------------------------------
                                    686 	.area HOME    (CODE)
                                    687 	.area HOME    (CODE)
                                    688 ;--------------------------------------------------------
                                    689 ; code
                                    690 ;--------------------------------------------------------
                                    691 	.area CSEG    (CODE)
                                    692 ;------------------------------------------------------------
                                    693 ;Allocation info for local variables in function 'default_layer_state_set_user'
                                    694 ;------------------------------------------------------------
                                    695 ;state         Allocated with name '_default_layer_state_set_user_state_10000_225'
                                    696 ;------------------------------------------------------------
                                    697 ;	quantum/action_layer.c:24: __attribute__((weak)) layer_state_t default_layer_state_set_user(layer_state_t state) {
                                    698 ;	-----------------------------------------
                                    699 ;	 function default_layer_state_set_user
                                    700 ;	-----------------------------------------
      0073CC                        701 _default_layer_state_set_user:
                           000007   702 	ar7 = 0x07
                           000006   703 	ar6 = 0x06
                           000005   704 	ar5 = 0x05
                           000004   705 	ar4 = 0x04
                           000003   706 	ar3 = 0x03
                           000002   707 	ar2 = 0x02
                           000001   708 	ar1 = 0x01
                           000000   709 	ar0 = 0x00
      0073CC E5 82            [12]  710 	mov	a,dpl
      0073CE 90 07 69         [24]  711 	mov	dptr,#_default_layer_state_set_user_state_10000_225
      0073D1 F0               [24]  712 	movx	@dptr,a
                                    713 ;	quantum/action_layer.c:25: return state;
      0073D2 E0               [24]  714 	movx	a,@dptr
                                    715 ;	quantum/action_layer.c:26: }
      0073D3 F5 82            [12]  716 	mov	dpl,a
      0073D5 22               [24]  717 	ret
                                    718 ;------------------------------------------------------------
                                    719 ;Allocation info for local variables in function 'default_layer_state_set_kb'
                                    720 ;------------------------------------------------------------
                                    721 ;state         Allocated with name '_default_layer_state_set_kb_state_10000_227'
                                    722 ;------------------------------------------------------------
                                    723 ;	quantum/action_layer.c:32: __attribute__((weak)) layer_state_t default_layer_state_set_kb(layer_state_t state) {
                                    724 ;	-----------------------------------------
                                    725 ;	 function default_layer_state_set_kb
                                    726 ;	-----------------------------------------
      0073D6                        727 _default_layer_state_set_kb:
      0073D6 E5 82            [12]  728 	mov	a,dpl
      0073D8 90 07 6A         [24]  729 	mov	dptr,#_default_layer_state_set_kb_state_10000_227
      0073DB F0               [24]  730 	movx	@dptr,a
                                    731 ;	quantum/action_layer.c:33: return default_layer_state_set_user(state);
      0073DC E0               [24]  732 	movx	a,@dptr
      0073DD F5 82            [12]  733 	mov	dpl,a
                                    734 ;	quantum/action_layer.c:34: }
      0073DF 02 73 CC         [24]  735 	ljmp	_default_layer_state_set_user
                                    736 ;------------------------------------------------------------
                                    737 ;Allocation info for local variables in function 'default_layer_state_set'
                                    738 ;------------------------------------------------------------
                                    739 ;state         Allocated with name '_default_layer_state_set_state_10000_229'
                                    740 ;------------------------------------------------------------
                                    741 ;	quantum/action_layer.c:40: static void default_layer_state_set(layer_state_t state) {
                                    742 ;	-----------------------------------------
                                    743 ;	 function default_layer_state_set
                                    744 ;	-----------------------------------------
      0073E2                        745 _default_layer_state_set:
      0073E2 E5 82            [12]  746 	mov	a,dpl
      0073E4 90 07 6B         [24]  747 	mov	dptr,#_default_layer_state_set_state_10000_229
      0073E7 F0               [24]  748 	movx	@dptr,a
                                    749 ;	quantum/action_layer.c:41: state = default_layer_state_set_kb(state);
      0073E8 E0               [24]  750 	movx	a,@dptr
      0073E9 F5 82            [12]  751 	mov	dpl,a
      0073EB 12 73 D6         [24]  752 	lcall	_default_layer_state_set_kb
      0073EE AF 82            [24]  753 	mov	r7, dpl
      0073F0 90 07 6B         [24]  754 	mov	dptr,#_default_layer_state_set_state_10000_229
      0073F3 EF               [12]  755 	mov	a,r7
      0073F4 F0               [24]  756 	movx	@dptr,a
                                    757 ;	quantum/action_layer.c:45: default_layer_state = state;
      0073F5 90 0B AC         [24]  758 	mov	dptr,#_default_layer_state
      0073F8 EF               [12]  759 	mov	a,r7
      0073F9 F0               [24]  760 	movx	@dptr,a
                                    761 ;	quantum/action_layer.c:47: ac_dprintf("\n");
                                    762 ;	quantum/action_layer.c:53: }
      0073FA 22               [24]  763 	ret
                                    764 ;------------------------------------------------------------
                                    765 ;Allocation info for local variables in function 'default_layer_set'
                                    766 ;------------------------------------------------------------
                                    767 ;state         Allocated with name '_default_layer_set_state_10000_234'
                                    768 ;------------------------------------------------------------
                                    769 ;	quantum/action_layer.c:69: void default_layer_set(layer_state_t state) {
                                    770 ;	-----------------------------------------
                                    771 ;	 function default_layer_set
                                    772 ;	-----------------------------------------
      0073FB                        773 _default_layer_set:
      0073FB E5 82            [12]  774 	mov	a,dpl
      0073FD 90 07 6C         [24]  775 	mov	dptr,#_default_layer_set_state_10000_234
      007400 F0               [24]  776 	movx	@dptr,a
                                    777 ;	quantum/action_layer.c:70: default_layer_state_set(state);
      007401 E0               [24]  778 	movx	a,@dptr
      007402 F5 82            [12]  779 	mov	dpl,a
                                    780 ;	quantum/action_layer.c:71: }
      007404 02 73 E2         [24]  781 	ljmp	_default_layer_state_set
                                    782 ;------------------------------------------------------------
                                    783 ;Allocation info for local variables in function 'default_layer_or'
                                    784 ;------------------------------------------------------------
                                    785 ;state         Allocated with name '_default_layer_or_state_10000_236'
                                    786 ;------------------------------------------------------------
                                    787 ;	quantum/action_layer.c:78: void default_layer_or(layer_state_t state) {
                                    788 ;	-----------------------------------------
                                    789 ;	 function default_layer_or
                                    790 ;	-----------------------------------------
      007407                        791 _default_layer_or:
      007407 E5 82            [12]  792 	mov	a,dpl
      007409 90 07 6D         [24]  793 	mov	dptr,#_default_layer_or_state_10000_236
      00740C F0               [24]  794 	movx	@dptr,a
                                    795 ;	quantum/action_layer.c:79: default_layer_state_set(default_layer_state | state);
      00740D E0               [24]  796 	movx	a,@dptr
      00740E FF               [12]  797 	mov	r7,a
      00740F 90 0B AC         [24]  798 	mov	dptr,#_default_layer_state
      007412 E0               [24]  799 	movx	a,@dptr
      007413 42 07            [12]  800 	orl	ar7,a
      007415 8F 82            [24]  801 	mov	dpl, r7
                                    802 ;	quantum/action_layer.c:80: }
      007417 02 73 E2         [24]  803 	ljmp	_default_layer_state_set
                                    804 ;------------------------------------------------------------
                                    805 ;Allocation info for local variables in function 'default_layer_and'
                                    806 ;------------------------------------------------------------
                                    807 ;state         Allocated with name '_default_layer_and_state_10000_238'
                                    808 ;------------------------------------------------------------
                                    809 ;	quantum/action_layer.c:85: void default_layer_and(layer_state_t state) {
                                    810 ;	-----------------------------------------
                                    811 ;	 function default_layer_and
                                    812 ;	-----------------------------------------
      00741A                        813 _default_layer_and:
      00741A E5 82            [12]  814 	mov	a,dpl
      00741C 90 07 6E         [24]  815 	mov	dptr,#_default_layer_and_state_10000_238
      00741F F0               [24]  816 	movx	@dptr,a
                                    817 ;	quantum/action_layer.c:86: default_layer_state_set(default_layer_state & state);
      007420 90 0B AC         [24]  818 	mov	dptr,#_default_layer_state
      007423 E0               [24]  819 	movx	a,@dptr
      007424 FF               [12]  820 	mov	r7,a
      007425 90 07 6E         [24]  821 	mov	dptr,#_default_layer_and_state_10000_238
      007428 E0               [24]  822 	movx	a,@dptr
      007429 52 07            [12]  823 	anl	ar7,a
      00742B 8F 82            [24]  824 	mov	dpl, r7
                                    825 ;	quantum/action_layer.c:87: }
      00742D 02 73 E2         [24]  826 	ljmp	_default_layer_state_set
                                    827 ;------------------------------------------------------------
                                    828 ;Allocation info for local variables in function 'default_layer_xor'
                                    829 ;------------------------------------------------------------
                                    830 ;state         Allocated with name '_default_layer_xor_state_10000_240'
                                    831 ;------------------------------------------------------------
                                    832 ;	quantum/action_layer.c:92: void default_layer_xor(layer_state_t state) {
                                    833 ;	-----------------------------------------
                                    834 ;	 function default_layer_xor
                                    835 ;	-----------------------------------------
      007430                        836 _default_layer_xor:
      007430 E5 82            [12]  837 	mov	a,dpl
      007432 90 07 6F         [24]  838 	mov	dptr,#_default_layer_xor_state_10000_240
      007435 F0               [24]  839 	movx	@dptr,a
                                    840 ;	quantum/action_layer.c:93: default_layer_state_set(default_layer_state ^ state);
      007436 E0               [24]  841 	movx	a,@dptr
      007437 FF               [12]  842 	mov	r7,a
      007438 90 0B AC         [24]  843 	mov	dptr,#_default_layer_state
      00743B E0               [24]  844 	movx	a,@dptr
      00743C 62 07            [12]  845 	xrl	ar7,a
      00743E 8F 82            [24]  846 	mov	dpl, r7
                                    847 ;	quantum/action_layer.c:94: }
      007440 02 73 E2         [24]  848 	ljmp	_default_layer_state_set
                                    849 ;------------------------------------------------------------
                                    850 ;Allocation info for local variables in function 'layer_state_set_user'
                                    851 ;------------------------------------------------------------
                                    852 ;state         Allocated with name '_layer_state_set_user_state_10000_242'
                                    853 ;------------------------------------------------------------
                                    854 ;	quantum/action_layer.c:106: __attribute__((weak)) layer_state_t layer_state_set_user(layer_state_t state) {
                                    855 ;	-----------------------------------------
                                    856 ;	 function layer_state_set_user
                                    857 ;	-----------------------------------------
      007443                        858 _layer_state_set_user:
      007443 E5 82            [12]  859 	mov	a,dpl
      007445 90 07 70         [24]  860 	mov	dptr,#_layer_state_set_user_state_10000_242
      007448 F0               [24]  861 	movx	@dptr,a
                                    862 ;	quantum/action_layer.c:107: return state;
      007449 E0               [24]  863 	movx	a,@dptr
                                    864 ;	quantum/action_layer.c:108: }
      00744A F5 82            [12]  865 	mov	dpl,a
      00744C 22               [24]  866 	ret
                                    867 ;------------------------------------------------------------
                                    868 ;Allocation info for local variables in function 'layer_state_set_kb'
                                    869 ;------------------------------------------------------------
                                    870 ;state         Allocated with name '_layer_state_set_kb_state_10000_244'
                                    871 ;------------------------------------------------------------
                                    872 ;	quantum/action_layer.c:114: __attribute__((weak)) layer_state_t layer_state_set_kb(layer_state_t state) {
                                    873 ;	-----------------------------------------
                                    874 ;	 function layer_state_set_kb
                                    875 ;	-----------------------------------------
      00744D                        876 _layer_state_set_kb:
      00744D E5 82            [12]  877 	mov	a,dpl
      00744F 90 07 71         [24]  878 	mov	dptr,#_layer_state_set_kb_state_10000_244
      007452 F0               [24]  879 	movx	@dptr,a
                                    880 ;	quantum/action_layer.c:115: return layer_state_set_user(state);
      007453 E0               [24]  881 	movx	a,@dptr
      007454 F5 82            [12]  882 	mov	dpl,a
                                    883 ;	quantum/action_layer.c:116: }
      007456 02 74 43         [24]  884 	ljmp	_layer_state_set_user
                                    885 ;------------------------------------------------------------
                                    886 ;Allocation info for local variables in function 'layer_state_set'
                                    887 ;------------------------------------------------------------
                                    888 ;state         Allocated with name '_layer_state_set_state_10000_246'
                                    889 ;------------------------------------------------------------
                                    890 ;	quantum/action_layer.c:122: void layer_state_set(layer_state_t state) {
                                    891 ;	-----------------------------------------
                                    892 ;	 function layer_state_set
                                    893 ;	-----------------------------------------
      007459                        894 _layer_state_set:
      007459 E5 82            [12]  895 	mov	a,dpl
      00745B 90 07 72         [24]  896 	mov	dptr,#_layer_state_set_state_10000_246
      00745E F0               [24]  897 	movx	@dptr,a
                                    898 ;	quantum/action_layer.c:123: state = layer_state_set_kb(state);
      00745F E0               [24]  899 	movx	a,@dptr
      007460 F5 82            [12]  900 	mov	dpl,a
      007462 12 74 4D         [24]  901 	lcall	_layer_state_set_kb
      007465 AF 82            [24]  902 	mov	r7, dpl
      007467 90 07 72         [24]  903 	mov	dptr,#_layer_state_set_state_10000_246
      00746A EF               [12]  904 	mov	a,r7
      00746B F0               [24]  905 	movx	@dptr,a
                                    906 ;	quantum/action_layer.c:127: layer_state = state;
      00746C 90 0B AD         [24]  907 	mov	dptr,#_layer_state
      00746F EF               [12]  908 	mov	a,r7
      007470 F0               [24]  909 	movx	@dptr,a
                                    910 ;	quantum/action_layer.c:129: ac_dprintf("\n");
                                    911 ;	quantum/action_layer.c:135: }
      007471 22               [24]  912 	ret
                                    913 ;------------------------------------------------------------
                                    914 ;Allocation info for local variables in function 'layer_clear'
                                    915 ;------------------------------------------------------------
                                    916 ;	quantum/action_layer.c:141: void layer_clear(void) {
                                    917 ;	-----------------------------------------
                                    918 ;	 function layer_clear
                                    919 ;	-----------------------------------------
      007472                        920 _layer_clear:
                                    921 ;	quantum/action_layer.c:142: layer_state_set(0);
      007472 75 82 00         [24]  922 	mov	dpl, #0x00
                                    923 ;	quantum/action_layer.c:143: }
      007475 02 74 59         [24]  924 	ljmp	_layer_state_set
                                    925 ;------------------------------------------------------------
                                    926 ;Allocation info for local variables in function 'layer_state_is'
                                    927 ;------------------------------------------------------------
                                    928 ;layer         Allocated with name '_layer_state_is_layer_10000_253'
                                    929 ;------------------------------------------------------------
                                    930 ;	quantum/action_layer.c:149: bool layer_state_is(uint8_t layer) {
                                    931 ;	-----------------------------------------
                                    932 ;	 function layer_move
                                    933 ;	-----------------------------------------
      007478                        934 _layer_move:
      007478 E5 82            [12]  935 	mov	a,dpl
      00747A 90 07 73         [24]  936 	mov	dptr,#_layer_move_layer_10000_259
      00747D F0               [24]  937 	movx	@dptr,a
                                    938 ;	quantum/action_layer.c:169: layer_state_set((layer_state_t)1 << layer);
      00747E E0               [24]  939 	movx	a,@dptr
      00747F F5 F0            [12]  940 	mov	b, a
      007481 05 F0            [12]  941 	inc	b
      007483 74 01            [12]  942 	mov	a,#0x01
      007485 80 02            [24]  943 	sjmp	00104$
      007487                        944 00103$:
      007487 25 E0            [12]  945 	add	a,acc
      007489                        946 00104$:
      007489 D5 F0 FB         [24]  947 	djnz	b,00103$
      00748C F5 82            [12]  948 	mov	dpl,a
                                    949 ;	quantum/action_layer.c:170: }
      00748E 02 74 59         [24]  950 	ljmp	_layer_state_set
                                    951 ;------------------------------------------------------------
                                    952 ;Allocation info for local variables in function 'layer_on'
                                    953 ;------------------------------------------------------------
                                    954 ;layer         Allocated with name '_layer_on_layer_10000_261'
                                    955 ;------------------------------------------------------------
                                    956 ;	quantum/action_layer.c:176: void layer_on(uint8_t layer) {
                                    957 ;	-----------------------------------------
                                    958 ;	 function layer_on
                                    959 ;	-----------------------------------------
      007491                        960 _layer_on:
      007491 E5 82            [12]  961 	mov	a,dpl
      007493 90 07 74         [24]  962 	mov	dptr,#_layer_on_layer_10000_261
      007496 F0               [24]  963 	movx	@dptr,a
                                    964 ;	quantum/action_layer.c:177: layer_state_set(layer_state | ((layer_state_t)1 << layer));
      007497 E0               [24]  965 	movx	a,@dptr
      007498 F5 F0            [12]  966 	mov	b, a
      00749A 05 F0            [12]  967 	inc	b
      00749C 74 01            [12]  968 	mov	a,#0x01
      00749E 80 02            [24]  969 	sjmp	00104$
      0074A0                        970 00103$:
      0074A0 25 E0            [12]  971 	add	a,acc
      0074A2                        972 00104$:
      0074A2 D5 F0 FB         [24]  973 	djnz	b,00103$
      0074A5 FF               [12]  974 	mov	r7,a
      0074A6 90 0B AD         [24]  975 	mov	dptr,#_layer_state
      0074A9 E0               [24]  976 	movx	a,@dptr
      0074AA 42 07            [12]  977 	orl	ar7,a
      0074AC 8F 82            [24]  978 	mov	dpl, r7
                                    979 ;	quantum/action_layer.c:178: }
      0074AE 02 74 59         [24]  980 	ljmp	_layer_state_set
                                    981 ;------------------------------------------------------------
                                    982 ;Allocation info for local variables in function 'layer_off'
                                    983 ;------------------------------------------------------------
                                    984 ;layer         Allocated with name '_layer_off_layer_10000_263'
                                    985 ;------------------------------------------------------------
                                    986 ;	quantum/action_layer.c:184: void layer_off(uint8_t layer) {
                                    987 ;	-----------------------------------------
                                    988 ;	 function layer_off
                                    989 ;	-----------------------------------------
      0074B1                        990 _layer_off:
      0074B1 E5 82            [12]  991 	mov	a,dpl
      0074B3 90 07 75         [24]  992 	mov	dptr,#_layer_off_layer_10000_263
      0074B6 F0               [24]  993 	movx	@dptr,a
                                    994 ;	quantum/action_layer.c:185: layer_state_set(layer_state & ~((layer_state_t)1 << layer));
      0074B7 E0               [24]  995 	movx	a,@dptr
      0074B8 F5 F0            [12]  996 	mov	b, a
      0074BA 05 F0            [12]  997 	inc	b
      0074BC 74 01            [12]  998 	mov	a,#0x01
      0074BE 80 02            [24]  999 	sjmp	00104$
      0074C0                       1000 00103$:
      0074C0 25 E0            [12] 1001 	add	a,acc
      0074C2                       1002 00104$:
      0074C2 D5 F0 FB         [24] 1003 	djnz	b,00103$
      0074C5 F4               [12] 1004 	cpl	a
      0074C6 FF               [12] 1005 	mov	r7,a
      0074C7 90 0B AD         [24] 1006 	mov	dptr,#_layer_state
      0074CA E0               [24] 1007 	movx	a,@dptr
      0074CB 52 07            [12] 1008 	anl	ar7,a
      0074CD 8F 82            [24] 1009 	mov	dpl, r7
                                   1010 ;	quantum/action_layer.c:186: }
      0074CF 02 74 59         [24] 1011 	ljmp	_layer_state_set
                                   1012 ;------------------------------------------------------------
                                   1013 ;Allocation info for local variables in function 'layer_invert'
                                   1014 ;------------------------------------------------------------
                                   1015 ;layer         Allocated with name '_layer_invert_layer_10000_265'
                                   1016 ;------------------------------------------------------------
                                   1017 ;	quantum/action_layer.c:192: void layer_invert(uint8_t layer) {
                                   1018 ;	-----------------------------------------
                                   1019 ;	 function layer_or
                                   1020 ;	-----------------------------------------
      0074D2                       1021 _layer_or:
      0074D2 E5 82            [12] 1022 	mov	a,dpl
      0074D4 90 07 76         [24] 1023 	mov	dptr,#_layer_or_state_10000_267
      0074D7 F0               [24] 1024 	movx	@dptr,a
                                   1025 ;	quantum/action_layer.c:201: layer_state_set(layer_state | state);
      0074D8 E0               [24] 1026 	movx	a,@dptr
      0074D9 FF               [12] 1027 	mov	r7,a
      0074DA 90 0B AD         [24] 1028 	mov	dptr,#_layer_state
      0074DD E0               [24] 1029 	movx	a,@dptr
      0074DE 42 07            [12] 1030 	orl	ar7,a
      0074E0 8F 82            [24] 1031 	mov	dpl, r7
                                   1032 ;	quantum/action_layer.c:202: }
      0074E2 02 74 59         [24] 1033 	ljmp	_layer_state_set
                                   1034 ;------------------------------------------------------------
                                   1035 ;Allocation info for local variables in function 'layer_and'
                                   1036 ;------------------------------------------------------------
                                   1037 ;state         Allocated with name '_layer_and_state_10000_269'
                                   1038 ;------------------------------------------------------------
                                   1039 ;	quantum/action_layer.c:207: void layer_and(layer_state_t state) {
                                   1040 ;	-----------------------------------------
                                   1041 ;	 function layer_and
                                   1042 ;	-----------------------------------------
      0074E5                       1043 _layer_and:
      0074E5 E5 82            [12] 1044 	mov	a,dpl
      0074E7 90 07 77         [24] 1045 	mov	dptr,#_layer_and_state_10000_269
      0074EA F0               [24] 1046 	movx	@dptr,a
                                   1047 ;	quantum/action_layer.c:208: layer_state_set(layer_state & state);
      0074EB 90 0B AD         [24] 1048 	mov	dptr,#_layer_state
      0074EE E0               [24] 1049 	movx	a,@dptr
      0074EF FF               [12] 1050 	mov	r7,a
      0074F0 90 07 77         [24] 1051 	mov	dptr,#_layer_and_state_10000_269
      0074F3 E0               [24] 1052 	movx	a,@dptr
      0074F4 52 07            [12] 1053 	anl	ar7,a
      0074F6 8F 82            [24] 1054 	mov	dpl, r7
                                   1055 ;	quantum/action_layer.c:209: }
      0074F8 02 74 59         [24] 1056 	ljmp	_layer_state_set
                                   1057 ;------------------------------------------------------------
                                   1058 ;Allocation info for local variables in function 'layer_xor'
                                   1059 ;------------------------------------------------------------
                                   1060 ;state         Allocated with name '_layer_xor_state_10000_271'
                                   1061 ;------------------------------------------------------------
                                   1062 ;	quantum/action_layer.c:214: void layer_xor(layer_state_t state) {
                                   1063 ;	-----------------------------------------
                                   1064 ;	 function layer_xor
                                   1065 ;	-----------------------------------------
      0074FB                       1066 _layer_xor:
      0074FB E5 82            [12] 1067 	mov	a,dpl
      0074FD 90 07 78         [24] 1068 	mov	dptr,#_layer_xor_state_10000_271
      007500 F0               [24] 1069 	movx	@dptr,a
                                   1070 ;	quantum/action_layer.c:215: layer_state_set(layer_state ^ state);
      007501 E0               [24] 1071 	movx	a,@dptr
      007502 FF               [12] 1072 	mov	r7,a
      007503 90 0B AD         [24] 1073 	mov	dptr,#_layer_state
      007506 E0               [24] 1074 	movx	a,@dptr
      007507 62 07            [12] 1075 	xrl	ar7,a
      007509 8F 82            [24] 1076 	mov	dpl, r7
                                   1077 ;	quantum/action_layer.c:216: }
      00750B 02 74 59         [24] 1078 	ljmp	_layer_state_set
                                   1079 ;------------------------------------------------------------
                                   1080 ;Allocation info for local variables in function 'source_keycode_cache_slot'
                                   1081 ;------------------------------------------------------------
                                   1082 ;key           Allocated with name '_source_keycode_cache_slot_PARM_1'
                                   1083 ;------------------------------------------------------------
                                   1084 ;	quantum/action_layer.c:258: static uint16_t SOURCE_CACHE_MEM *source_keycode_cache_slot(keypos_t key) {
                                   1085 ;	-----------------------------------------
                                   1086 ;	 function source_keycode_cache_slot
                                   1087 ;	-----------------------------------------
      00750E                       1088 _source_keycode_cache_slot:
                                   1089 ;	quantum/action_layer.c:259: if (key.row < MATRIX_ROWS && key.col < MATRIX_COLS) {
      00750E 90 08 7C         [24] 1090 	mov	dptr,#(_source_keycode_cache_slot_PARM_1 + 0x0001)
      007511 E0               [24] 1091 	movx	a,@dptr
      007512 FF               [12] 1092 	mov	r7,a
      007513 BF 10 00         [24] 1093 	cjne	r7,#0x10,00138$
      007516                       1094 00138$:
      007516 50 23            [24] 1095 	jnc	00102$
      007518 90 08 7B         [24] 1096 	mov	dptr,#_source_keycode_cache_slot_PARM_1
      00751B E0               [24] 1097 	movx	a,@dptr
      00751C FE               [12] 1098 	mov	r6,a
      00751D BE 08 00         [24] 1099 	cjne	r6,#0x08,00140$
      007520                       1100 00140$:
      007520 50 19            [24] 1101 	jnc	00102$
                                   1102 ;	quantum/action_layer.c:260: return &source_keycodes_cache[(uint8_t)(key.row * MATRIX_COLS + key.col)];
      007522 8F 05            [24] 1103 	mov	ar5,r7
      007524 ED               [12] 1104 	mov	a,r5
      007525 C4               [12] 1105 	swap	a
      007526 03               [12] 1106 	rr	a
      007527 54 F8            [12] 1107 	anl	a,#0xf8
      007529 2E               [12] 1108 	add	a,r6
      00752A 75 F0 02         [24] 1109 	mov	b,#0x02
      00752D A4               [48] 1110 	mul	ab
      00752E 24 79            [12] 1111 	add	a, #_source_keycodes_cache
      007530 FD               [12] 1112 	mov	r5,a
      007531 74 07            [12] 1113 	mov	a,#(_source_keycodes_cache >> 8)
      007533 35 F0            [12] 1114 	addc	a, b
      007535 FE               [12] 1115 	mov	r6,a
      007536 8D 82            [24] 1116 	mov	dpl, r5
      007538 8E 83            [24] 1117 	mov	dph, r6
      00753A 22               [24] 1118 	ret
      00753B                       1119 00102$:
                                   1120 ;	quantum/action_layer.c:263: if ((key.row == KEYLOC_ENCODER_CW || key.row == KEYLOC_ENCODER_CCW) && key.col < NUM_ENCODERS) {
      00753B BF FD 02         [24] 1121 	cjne	r7,#0xfd,00142$
      00753E 80 03            [24] 1122 	sjmp	00107$
      007540                       1123 00142$:
      007540 BF FC 0E         [24] 1124 	cjne	r7,#0xfc,00105$
      007543                       1125 00107$:
      007543 90 08 7B         [24] 1126 	mov	dptr,#_source_keycode_cache_slot_PARM_1
      007546 E0               [24] 1127 	movx	a,@dptr
      007547 FF               [12] 1128 	mov	r7,a
      007548 BF 01 00         [24] 1129 	cjne	r7,#0x01,00145$
      00754B                       1130 00145$:
      00754B 50 04            [24] 1131 	jnc	00105$
                                   1132 ;	quantum/action_layer.c:264: return &encoder_source_keycodes_cache[key.col];
      00754D 90 08 79         [24] 1133 	mov	dptr,#_encoder_source_keycodes_cache
      007550 22               [24] 1134 	ret
      007551                       1135 00105$:
                                   1136 ;	quantum/action_layer.c:267: return 0;
      007551 90 00 00         [24] 1137 	mov	dptr,#0x0000
                                   1138 ;	quantum/action_layer.c:268: }
      007554 22               [24] 1139 	ret
                                   1140 ;------------------------------------------------------------
                                   1141 ;Allocation info for local variables in function 'update_source_keycode_cache'
                                   1142 ;------------------------------------------------------------
                                   1143 ;key           Allocated with name '_update_source_keycode_cache_PARM_1'
                                   1144 ;keycode       Allocated with name '_update_source_keycode_cache_keycode_10000_279'
                                   1145 ;slot          Allocated with name '_update_source_keycode_cache_slot_10000_280'
                                   1146 ;------------------------------------------------------------
                                   1147 ;	quantum/action_layer.c:272: bool update_source_keycode_cache(keypos_t key, uint16_t keycode) {
                                   1148 ;	-----------------------------------------
                                   1149 ;	 function update_source_keycode_cache
                                   1150 ;	-----------------------------------------
      007555                       1151 _update_source_keycode_cache:
      007555 AF 83            [24] 1152 	mov	r7,dph
      007557 E5 82            [12] 1153 	mov	a,dpl
      007559 90 08 7F         [24] 1154 	mov	dptr,#_update_source_keycode_cache_keycode_10000_279
      00755C F0               [24] 1155 	movx	@dptr,a
      00755D EF               [12] 1156 	mov	a,r7
      00755E A3               [24] 1157 	inc	dptr
      00755F F0               [24] 1158 	movx	@dptr,a
                                   1159 ;	quantum/action_layer.c:273: uint16_t SOURCE_CACHE_MEM *slot = source_keycode_cache_slot(key);
      007560 90 0B 8F         [24] 1160 	mov	dptr,#___memcpy_PARM_2
      007563 74 7D            [12] 1161 	mov	a,#_update_source_keycode_cache_PARM_1
      007565 F0               [24] 1162 	movx	@dptr,a
      007566 74 08            [12] 1163 	mov	a,#(_update_source_keycode_cache_PARM_1 >> 8)
      007568 12 77 FA         [24] 1164 	lcall	_ak820_outline_0001
      00756B 90 08 7B         [24] 1165 	mov	dptr,#_source_keycode_cache_slot_PARM_1
      00756E F5 F0            [12] 1166 	mov	b,a
      007570 12 B4 9F         [24] 1167 	lcall	___memcpy
      007573 12 75 0E         [24] 1168 	lcall	_source_keycode_cache_slot
      007576 AE 82            [24] 1169 	mov	r6, dpl
      007578 AF 83            [24] 1170 	mov	r7, dph
                                   1171 ;	quantum/action_layer.c:274: if (!slot) return false;
      00757A EE               [12] 1172 	mov	a,r6
      00757B 4F               [12] 1173 	orl	a,r7
      00757C 70 03            [24] 1174 	jnz	00102$
      00757E F5 82            [12] 1175 	mov	dpl,a
      007580 22               [24] 1176 	ret
      007581                       1177 00102$:
                                   1178 ;	quantum/action_layer.c:275: *slot = keycode;
      007581 90 08 7F         [24] 1179 	mov	dptr,#_update_source_keycode_cache_keycode_10000_279
      007584 E0               [24] 1180 	movx	a,@dptr
      007585 FC               [12] 1181 	mov	r4,a
      007586 A3               [24] 1182 	inc	dptr
      007587 E0               [24] 1183 	movx	a,@dptr
      007588 FD               [12] 1184 	mov	r5,a
      007589 8E 82            [24] 1185 	mov	dpl,r6
      00758B 8F 83            [24] 1186 	mov	dph,r7
      00758D EC               [12] 1187 	mov	a,r4
      00758E F0               [24] 1188 	movx	@dptr,a
      00758F ED               [12] 1189 	mov	a,r5
      007590 A3               [24] 1190 	inc	dptr
      007591 F0               [24] 1191 	movx	@dptr,a
                                   1192 ;	quantum/action_layer.c:276: return true;
      007592 75 82 01         [24] 1193 	mov	dpl, #0x01
                                   1194 ;	quantum/action_layer.c:277: }
      007595 22               [24] 1195 	ret
                                   1196 ;------------------------------------------------------------
                                   1197 ;Allocation info for local variables in function 'update_source_layers_cache'
                                   1198 ;------------------------------------------------------------
                                   1199 ;key           Allocated with name '_update_source_layers_cache_PARM_1'
                                   1200 ;layer         Allocated with name '_update_source_layers_cache_layer_10000_282'
                                   1201 ;slot          Allocated with name '_update_source_layers_cache_slot_10000_283'
                                   1202 ;------------------------------------------------------------
                                   1203 ;	quantum/action_layer.c:279: void update_source_layers_cache(keypos_t key, uint8_t layer) {
                                   1204 ;	-----------------------------------------
                                   1205 ;	 function update_source_layers_cache
                                   1206 ;	-----------------------------------------
      007596                       1207 _update_source_layers_cache:
      007596 E5 82            [12] 1208 	mov	a,dpl
      007598 90 08 83         [24] 1209 	mov	dptr,#_update_source_layers_cache_layer_10000_282
      00759B F0               [24] 1210 	movx	@dptr,a
                                   1211 ;	quantum/action_layer.c:280: uint16_t SOURCE_CACHE_MEM *slot = source_keycode_cache_slot(key);
      00759C 90 0B 8F         [24] 1212 	mov	dptr,#___memcpy_PARM_2
      00759F 74 81            [12] 1213 	mov	a,#_update_source_layers_cache_PARM_1
      0075A1 F0               [24] 1214 	movx	@dptr,a
      0075A2 74 08            [12] 1215 	mov	a,#(_update_source_layers_cache_PARM_1 >> 8)
      0075A4 12 77 FA         [24] 1216 	lcall	_ak820_outline_0001
      0075A7 90 08 7B         [24] 1217 	mov	dptr,#_source_keycode_cache_slot_PARM_1
      0075AA F5 F0            [12] 1218 	mov	b,a
      0075AC 12 B4 9F         [24] 1219 	lcall	___memcpy
      0075AF 12 75 0E         [24] 1220 	lcall	_source_keycode_cache_slot
      0075B2 AE 82            [24] 1221 	mov	r6, dpl
      0075B4 AF 83            [24] 1222 	mov	r7, dph
                                   1223 ;	quantum/action_layer.c:281: if (!slot) return;
      0075B6 EE               [12] 1224 	mov	a,r6
      0075B7 4F               [12] 1225 	orl	a,r7
      0075B8 70 01            [24] 1226 	jnz	00102$
      0075BA 22               [24] 1227 	ret
      0075BB                       1228 00102$:
                                   1229 ;	quantum/action_layer.c:282: layer &= (1u << MAX_LAYER_BITS) - 1;
      0075BB 90 08 83         [24] 1230 	mov	dptr,#_update_source_layers_cache_layer_10000_282
      0075BE E0               [24] 1231 	movx	a,@dptr
      0075BF 53 E0 07         [24] 1232 	anl	acc,#0x07
      0075C2 F0               [24] 1233 	movx	@dptr,a
                                   1234 ;	quantum/action_layer.c:293: *slot = keymap_key_to_keycode(layer, key);
      0075C3 90 08 83         [24] 1235 	mov	dptr,#_update_source_layers_cache_layer_10000_282
      0075C6 E0               [24] 1236 	movx	a,@dptr
      0075C7 FD               [12] 1237 	mov	r5,a
      0075C8 90 0B 8F         [24] 1238 	mov	dptr,#___memcpy_PARM_2
      0075CB 74 81            [12] 1239 	mov	a,#_update_source_layers_cache_PARM_1
      0075CD F0               [24] 1240 	movx	@dptr,a
      0075CE 74 08            [12] 1241 	mov	a,#(_update_source_layers_cache_PARM_1 >> 8)
      0075D0 12 77 FA         [24] 1242 	lcall	_ak820_outline_0001
      0075D3 90 09 8F         [24] 1243 	mov	dptr,#_keymap_key_to_keycode_PARM_2
      0075D6 F5 F0            [12] 1244 	mov	b,a
      0075D8 C0 07            [24] 1245 	push	ar7
      0075DA C0 06            [24] 1246 	push	ar6
      0075DC C0 05            [24] 1247 	push	ar5
      0075DE 12 B4 9F         [24] 1248 	lcall	___memcpy
      0075E1 D0 05            [24] 1249 	pop	ar5
      0075E3 8D 82            [24] 1250 	mov	dpl, r5
      0075E5 12 8F 5B         [24] 1251 	lcall	_keymap_key_to_keycode
      0075E8 AC 82            [24] 1252 	mov	r4, dpl
      0075EA AD 83            [24] 1253 	mov	r5, dph
      0075EC D0 06            [24] 1254 	pop	ar6
      0075EE D0 07            [24] 1255 	pop	ar7
      0075F0 8E 82            [24] 1256 	mov	dpl,r6
      0075F2 8F 83            [24] 1257 	mov	dph,r7
      0075F4 EC               [12] 1258 	mov	a,r4
      0075F5 F0               [24] 1259 	movx	@dptr,a
      0075F6 ED               [12] 1260 	mov	a,r5
      0075F7 A3               [24] 1261 	inc	dptr
      0075F8 F0               [24] 1262 	movx	@dptr,a
                                   1263 ;	quantum/action_layer.c:294: }
      0075F9 22               [24] 1264 	ret
                                   1265 ;------------------------------------------------------------
                                   1266 ;Allocation info for local variables in function 'read_source_keycode_cache'
                                   1267 ;------------------------------------------------------------
                                   1268 ;key           Allocated with name '_read_source_keycode_cache_PARM_1'
                                   1269 ;slot          Allocated with name '_read_source_keycode_cache_slot_10001_289'
                                   1270 ;------------------------------------------------------------
                                   1271 ;	quantum/action_layer.c:315: uint16_t read_source_keycode_cache(keypos_t key) {
                                   1272 ;	-----------------------------------------
                                   1273 ;	 function read_source_keycode_cache
                                   1274 ;	-----------------------------------------
      0075FA                       1275 _read_source_keycode_cache:
                                   1276 ;	quantum/action_layer.c:318: if (vial_unlock_in_progress) return KC_NO;
      0075FA 90 0C 08         [24] 1277 	mov	dptr,#_vial_unlock_in_progress
      0075FD E0               [24] 1278 	movx	a,@dptr
      0075FE 60 04            [24] 1279 	jz	00102$
      007600 90 00 00         [24] 1280 	mov	dptr,#0x0000
      007603 22               [24] 1281 	ret
      007604                       1282 00102$:
                                   1283 ;	quantum/action_layer.c:319: if (key.row == VIAL_MATRIX_MAGIC && key.col == VIAL_MATRIX_MAGIC) return g_vial_magic_keycode_override;
      007604 90 08 85         [24] 1284 	mov	dptr,#(_read_source_keycode_cache_PARM_1 + 0x0001)
      007607 E0               [24] 1285 	movx	a,@dptr
      007608 FF               [12] 1286 	mov	r7,a
      007609 BF F0 0F         [24] 1287 	cjne	r7,#0xf0,00104$
      00760C 90 08 84         [24] 1288 	mov	dptr,#_read_source_keycode_cache_PARM_1
      00760F E0               [24] 1289 	movx	a,@dptr
      007610 FF               [12] 1290 	mov	r7,a
      007611 BF F0 07         [24] 1291 	cjne	r7,#0xf0,00104$
      007614 90 0A 67         [24] 1292 	mov	dptr,#_g_vial_magic_keycode_override
      007617 12 73 B0         [24] 1293 	lcall	_ak820_outline_0013
      00761A 22               [24] 1294 	ret
      00761B                       1295 00104$:
                                   1296 ;	quantum/action_layer.c:321: uint16_t SOURCE_CACHE_MEM *slot = source_keycode_cache_slot(key);
      00761B 90 0B 8F         [24] 1297 	mov	dptr,#___memcpy_PARM_2
      00761E 74 84            [12] 1298 	mov	a,#_read_source_keycode_cache_PARM_1
      007620 F0               [24] 1299 	movx	@dptr,a
      007621 74 08            [12] 1300 	mov	a,#(_read_source_keycode_cache_PARM_1 >> 8)
      007623 12 77 FA         [24] 1301 	lcall	_ak820_outline_0001
      007626 90 08 7B         [24] 1302 	mov	dptr,#_source_keycode_cache_slot_PARM_1
      007629 F5 F0            [12] 1303 	mov	b,a
      00762B 12 B4 9F         [24] 1304 	lcall	___memcpy
      00762E 12 75 0E         [24] 1305 	lcall	_source_keycode_cache_slot
      007631 AE 82            [24] 1306 	mov	r6, dpl
      007633 AF 83            [24] 1307 	mov	r7, dph
                                   1308 ;	quantum/action_layer.c:322: return slot ? *slot : KC_NO;
      007635 EE               [12] 1309 	mov	a,r6
      007636 4F               [12] 1310 	orl	a,r7
      007637 60 0B            [24] 1311 	jz	00108$
      007639 8E 82            [24] 1312 	mov	dpl,r6
      00763B 8F 83            [24] 1313 	mov	dph,r7
      00763D E0               [24] 1314 	movx	a,@dptr
      00763E FE               [12] 1315 	mov	r6,a
      00763F A3               [24] 1316 	inc	dptr
      007640 E0               [24] 1317 	movx	a,@dptr
      007641 FF               [12] 1318 	mov	r7,a
      007642 80 04            [24] 1319 	sjmp	00109$
      007644                       1320 00108$:
      007644 7E 00            [12] 1321 	mov	r6,#0x00
      007646 7F 00            [12] 1322 	mov	r7,#0x00
      007648                       1323 00109$:
      007648 8E 82            [24] 1324 	mov	dpl, r6
      00764A 8F 83            [24] 1325 	mov	dph, r7
                                   1326 ;	quantum/action_layer.c:323: }
      00764C 22               [24] 1327 	ret
                                   1328 ;------------------------------------------------------------
                                   1329 ;Allocation info for local variables in function 'store_or_get_action'
                                   1330 ;------------------------------------------------------------
                                   1331 ;key           Allocated with name '_store_or_get_action_PARM_2'
                                   1332 ;pressed       Allocated with name '_store_or_get_action_pressed_10000_290'
                                   1333 ;------------------------------------------------------------
                                   1334 ;	quantum/action_layer.c:412: uint16_t store_or_get_action(bool pressed, keypos_t key) {
                                   1335 ;	-----------------------------------------
                                   1336 ;	 function store_or_get_action
                                   1337 ;	-----------------------------------------
      00764D                       1338 _store_or_get_action:
      00764D E5 82            [12] 1339 	mov	a,dpl
      00764F 90 08 88         [24] 1340 	mov	dptr,#_store_or_get_action_pressed_10000_290
      007652 F0               [24] 1341 	movx	@dptr,a
                                   1342 ;	quantum/action_layer.c:414: if (disable_action_cache) {
      007653 90 0B AB         [24] 1343 	mov	dptr,#_disable_action_cache
      007656 E0               [24] 1344 	movx	a,@dptr
      007657 60 16            [24] 1345 	jz	00102$
                                   1346 ;	quantum/action_layer.c:415: return layer_switch_get_action(key);
      007659 90 0B 8F         [24] 1347 	mov	dptr,#___memcpy_PARM_2
      00765C 74 86            [12] 1348 	mov	a,#_store_or_get_action_PARM_2
      00765E F0               [24] 1349 	movx	@dptr,a
      00765F 74 08            [12] 1350 	mov	a,#(_store_or_get_action_PARM_2 >> 8)
      007661 12 77 FA         [24] 1351 	lcall	_ak820_outline_0001
      007664 90 08 8E         [24] 1352 	mov	dptr,#_layer_switch_get_action_PARM_1
      007667 F5 F0            [12] 1353 	mov	b,a
      007669 12 B4 9F         [24] 1354 	lcall	___memcpy
      00766C 02 77 41         [24] 1355 	ljmp	_layer_switch_get_action
      00766F                       1356 00102$:
                                   1357 ;	quantum/action_layer.c:419: if (pressed) update_source_layers_cache(key, layer_switch_get_layer(key));
      00766F 90 08 88         [24] 1358 	mov	dptr,#_store_or_get_action_pressed_10000_290
      007672 E0               [24] 1359 	movx	a,@dptr
      007673 60 34            [24] 1360 	jz	00104$
      007675 90 0B 8F         [24] 1361 	mov	dptr,#___memcpy_PARM_2
      007678 74 86            [12] 1362 	mov	a,#_store_or_get_action_PARM_2
      00767A F0               [24] 1363 	movx	@dptr,a
      00767B 74 08            [12] 1364 	mov	a,#(_store_or_get_action_PARM_2 >> 8)
      00767D 12 77 FA         [24] 1365 	lcall	_ak820_outline_0001
      007680 90 08 89         [24] 1366 	mov	dptr,#_layer_switch_get_layer_PARM_1
      007683 F5 F0            [12] 1367 	mov	b,a
      007685 12 B4 9F         [24] 1368 	lcall	___memcpy
      007688 12 76 C4         [24] 1369 	lcall	_layer_switch_get_layer
      00768B AF 82            [24] 1370 	mov	r7, dpl
      00768D 90 0B 8F         [24] 1371 	mov	dptr,#___memcpy_PARM_2
      007690 74 86            [12] 1372 	mov	a,#_store_or_get_action_PARM_2
      007692 F0               [24] 1373 	movx	@dptr,a
      007693 74 08            [12] 1374 	mov	a,#(_store_or_get_action_PARM_2 >> 8)
      007695 12 77 FA         [24] 1375 	lcall	_ak820_outline_0001
      007698 90 08 81         [24] 1376 	mov	dptr,#_update_source_layers_cache_PARM_1
      00769B F5 F0            [12] 1377 	mov	b,a
      00769D C0 07            [24] 1378 	push	ar7
      00769F 12 B4 9F         [24] 1379 	lcall	___memcpy
      0076A2 D0 07            [24] 1380 	pop	ar7
      0076A4 8F 82            [24] 1381 	mov	dpl, r7
      0076A6 12 75 96         [24] 1382 	lcall	_update_source_layers_cache
      0076A9                       1383 00104$:
                                   1384 ;	quantum/action_layer.c:420: return action_for_keycode(read_source_keycode_cache(key));
      0076A9 90 0B 8F         [24] 1385 	mov	dptr,#___memcpy_PARM_2
      0076AC 74 86            [12] 1386 	mov	a,#_store_or_get_action_PARM_2
      0076AE F0               [24] 1387 	movx	@dptr,a
      0076AF 74 08            [12] 1388 	mov	a,#(_store_or_get_action_PARM_2 >> 8)
      0076B1 12 77 FA         [24] 1389 	lcall	_ak820_outline_0001
      0076B4 90 08 84         [24] 1390 	mov	dptr,#_read_source_keycode_cache_PARM_1
      0076B7 F5 F0            [12] 1391 	mov	b,a
      0076B9 12 B4 9F         [24] 1392 	lcall	___memcpy
      0076BC 12 75 FA         [24] 1393 	lcall	_read_source_keycode_cache
      0076BF AF 83            [24] 1394 	mov  r7,dph
                                   1395 ;	quantum/action_layer.c:434: }
      0076C1 02 8D AF         [24] 1396 	ljmp	_action_for_keycode
                                   1397 ;------------------------------------------------------------
                                   1398 ;Allocation info for local variables in function 'layer_switch_get_layer'
                                   1399 ;------------------------------------------------------------
                                   1400 ;key           Allocated with name '_layer_switch_get_layer_PARM_1'
                                   1401 ;action        Allocated with name '_layer_switch_get_layer_action_10000_296'
                                   1402 ;layers        Allocated with name '_layer_switch_get_layer_layers_10001_297'
                                   1403 ;i             Allocated with name '_layer_switch_get_layer_i_20001_298'
                                   1404 ;------------------------------------------------------------
                                   1405 ;	quantum/action_layer.c:440: uint8_t layer_switch_get_layer(keypos_t key) {
                                   1406 ;	-----------------------------------------
                                   1407 ;	 function layer_switch_get_layer
                                   1408 ;	-----------------------------------------
      0076C4                       1409 _layer_switch_get_layer:
                                   1410 ;	quantum/action_layer.c:443: action.code = ACTION_TRANSPARENT;
      0076C4 90 08 8B         [24] 1411 	mov	dptr,#_layer_switch_get_layer_action_10000_296
      0076C7 74 01            [12] 1412 	mov	a,#0x01
      0076C9 F0               [24] 1413 	movx	@dptr,a
      0076CA E4               [12] 1414 	clr	a
      0076CB A3               [24] 1415 	inc	dptr
      0076CC F0               [24] 1416 	movx	@dptr,a
                                   1417 ;	quantum/action_layer.c:445: layer_state_t layers = layer_state | default_layer_state;
      0076CD 90 0B AC         [24] 1418 	mov	dptr,#_default_layer_state
      0076D0 E0               [24] 1419 	movx	a,@dptr
      0076D1 FF               [12] 1420 	mov	r7,a
      0076D2 90 0B AD         [24] 1421 	mov	dptr,#_layer_state
      0076D5 E0               [24] 1422 	movx	a,@dptr
      0076D6 90 08 8D         [24] 1423 	mov	dptr,#_layer_switch_get_layer_layers_10001_297
      0076D9 4F               [12] 1424 	orl	a,r7
      0076DA F0               [24] 1425 	movx	@dptr,a
                                   1426 ;	quantum/action_layer.c:447: for (int8_t i = MAX_LAYER - 1; i >= 0; i--) {
      0076DB 7F 05            [12] 1427 	mov	r7,#0x05
      0076DD                       1428 00107$:
      0076DD EF               [12] 1429 	mov	a,r7
      0076DE 20 E7 5C         [24] 1430 	jb	acc.7,00105$
                                   1431 ;	quantum/action_layer.c:448: if (layers & ((layer_state_t)1 << i)) {
      0076E1 8F F0            [24] 1432 	mov	b,r7
      0076E3 05 F0            [12] 1433 	inc	b
      0076E5 7D 01            [12] 1434 	mov	r5,#0x01
      0076E7 7E 00            [12] 1435 	mov	r6,#0x00
      0076E9 80 06            [24] 1436 	sjmp	00141$
      0076EB                       1437 00140$:
      0076EB ED               [12] 1438 	mov	a,r5
      0076EC 2D               [12] 1439 	add	a,r5
      0076ED FD               [12] 1440 	mov	r5,a
      0076EE EE               [12] 1441 	mov	a,r6
      0076EF 33               [12] 1442 	rlc	a
      0076F0 FE               [12] 1443 	mov	r6,a
      0076F1                       1444 00141$:
      0076F1 D5 F0 F7         [24] 1445 	djnz	b,00140$
      0076F4 90 08 8D         [24] 1446 	mov	dptr,#_layer_switch_get_layer_layers_10001_297
      0076F7 E0               [24] 1447 	movx	a,@dptr
      0076F8 7C 00            [12] 1448 	mov	r4,#0x00
      0076FA 52 05            [12] 1449 	anl	ar5,a
      0076FC EC               [12] 1450 	mov	a,r4
      0076FD 52 06            [12] 1451 	anl	ar6,a
      0076FF ED               [12] 1452 	mov	a,r5
      007700 4E               [12] 1453 	orl	a,r6
      007701 60 37            [24] 1454 	jz	00108$
                                   1455 ;	quantum/action_layer.c:449: action.code = action_for_key(i, key);
      007703 90 0B 8F         [24] 1456 	mov	dptr,#___memcpy_PARM_2
      007706 74 89            [12] 1457 	mov	a,#_layer_switch_get_layer_PARM_1
      007708 F0               [24] 1458 	movx	@dptr,a
      007709 74 08            [12] 1459 	mov	a,#(_layer_switch_get_layer_PARM_1 >> 8)
      00770B 12 77 FA         [24] 1460 	lcall	_ak820_outline_0001
      00770E 90 09 85         [24] 1461 	mov	dptr,#_action_for_key_PARM_2
      007711 F5 F0            [12] 1462 	mov	b,a
      007713 C0 07            [24] 1463 	push	ar7
      007715 12 B4 9F         [24] 1464 	lcall	___memcpy
      007718 D0 07            [24] 1465 	pop	ar7
      00771A 8F 82            [24] 1466 	mov	dpl, r7
      00771C C0 07            [24] 1467 	push	ar7
      00771E 12 8D 7B         [24] 1468 	lcall	_action_for_key
      007721 AD 82            [24] 1469 	mov	r5, dpl
      007723 AE 83            [24] 1470 	mov	r6, dph
      007725 D0 07            [24] 1471 	pop	ar7
      007727 90 08 8B         [24] 1472 	mov	dptr,#_layer_switch_get_layer_action_10000_296
      00772A ED               [12] 1473 	mov	a,r5
      00772B F0               [24] 1474 	movx	@dptr,a
      00772C EE               [12] 1475 	mov	a,r6
      00772D A3               [24] 1476 	inc	dptr
      00772E F0               [24] 1477 	movx	@dptr,a
                                   1478 ;	quantum/action_layer.c:450: if (action.code != ACTION_TRANSPARENT) {
      00772F BD 01 05         [24] 1479 	cjne	r5,#0x01,00143$
      007732 BE 00 02         [24] 1480 	cjne	r6,#0x00,00143$
      007735 80 03            [24] 1481 	sjmp	00108$
      007737                       1482 00143$:
                                   1483 ;	quantum/action_layer.c:451: return i;
      007737 8F 82            [24] 1484 	mov	dpl, r7
      007739 22               [24] 1485 	ret
      00773A                       1486 00108$:
                                   1487 ;	quantum/action_layer.c:447: for (int8_t i = MAX_LAYER - 1; i >= 0; i--) {
      00773A 1F               [12] 1488 	dec	r7
      00773B 80 A0            [24] 1489 	sjmp	00107$
      00773D                       1490 00105$:
                                   1491 ;	quantum/action_layer.c:456: return 0;
      00773D 75 82 00         [24] 1492 	mov	dpl, #0x00
                                   1493 ;	quantum/action_layer.c:461: }
      007740 22               [24] 1494 	ret
                                   1495 ;------------------------------------------------------------
                                   1496 ;Allocation info for local variables in function 'layer_switch_get_action'
                                   1497 ;------------------------------------------------------------
                                   1498 ;key           Allocated with name '_layer_switch_get_action_PARM_1'
                                   1499 ;layer         Allocated with name '_layer_switch_get_action_layer_10000_305'
                                   1500 ;action        Allocated with name '_layer_switch_get_action_action_10000_305'
                                   1501 ;------------------------------------------------------------
                                   1502 ;	quantum/action_layer.c:467: uint16_t layer_switch_get_action(keypos_t key) {
                                   1503 ;	-----------------------------------------
                                   1504 ;	 function layer_switch_get_action
                                   1505 ;	-----------------------------------------
      007741                       1506 _layer_switch_get_action:
                                   1507 ;	quantum/action_layer.c:469: uint8_t layer = layer_switch_get_layer(key);
      007741 90 0B 8F         [24] 1508 	mov	dptr,#___memcpy_PARM_2
      007744 74 8E            [12] 1509 	mov	a,#_layer_switch_get_action_PARM_1
      007746 F0               [24] 1510 	movx	@dptr,a
      007747 74 08            [12] 1511 	mov	a,#(_layer_switch_get_action_PARM_1 >> 8)
      007749 12 77 FA         [24] 1512 	lcall	_ak820_outline_0001
      00774C 90 08 89         [24] 1513 	mov	dptr,#_layer_switch_get_layer_PARM_1
      00774F F5 F0            [12] 1514 	mov	b,a
      007751 12 B4 9F         [24] 1515 	lcall	___memcpy
      007754 12 76 C4         [24] 1516 	lcall	_layer_switch_get_layer
      007757 AF 82            [24] 1517 	mov	r7, dpl
                                   1518 ;	quantum/action_layer.c:472: action = action_for_key(layer, key);
      007759 90 0B 8F         [24] 1519 	mov	dptr,#___memcpy_PARM_2
      00775C 74 8E            [12] 1520 	mov	a,#_layer_switch_get_action_PARM_1
      00775E F0               [24] 1521 	movx	@dptr,a
      00775F 74 08            [12] 1522 	mov	a,#(_layer_switch_get_action_PARM_1 >> 8)
      007761 12 77 FA         [24] 1523 	lcall	_ak820_outline_0001
      007764 90 09 85         [24] 1524 	mov	dptr,#_action_for_key_PARM_2
      007767 F5 F0            [12] 1525 	mov	b,a
      007769 C0 07            [24] 1526 	push	ar7
      00776B 12 B4 9F         [24] 1527 	lcall	___memcpy
      00776E D0 07            [24] 1528 	pop	ar7
      007770 8F 82            [24] 1529 	mov	dpl, r7
                                   1530 ;	quantum/action_layer.c:474: return action;
                                   1531 ;	quantum/action_layer.c:475: }
      007772 02 8D 7B         [24] 1532 	ljmp	_action_for_key
                                   1533 ;------------------------------------------------------------
                                   1534 ;Allocation info for local variables in function 'update_tri_layer_state'
                                   1535 ;------------------------------------------------------------
                                   1536 ;layer1        Allocated with name '_update_tri_layer_state_PARM_2'
                                   1537 ;layer2        Allocated with name '_update_tri_layer_state_PARM_3'
                                   1538 ;layer3        Allocated with name '_update_tri_layer_state_PARM_4'
                                   1539 ;state         Allocated with name '_update_tri_layer_state_state_10000_306'
                                   1540 ;mask12        Allocated with name '_update_tri_layer_state_mask12_10000_307'
                                   1541 ;mask3         Allocated with name '_update_tri_layer_state_mask3_10000_307'
                                   1542 ;------------------------------------------------------------
                                   1543 ;	quantum/action_layer.c:478: layer_state_t update_tri_layer_state(layer_state_t state, uint8_t layer1, uint8_t layer2, uint8_t layer3) {
                                   1544 ;	-----------------------------------------
                                   1545 ;	 function update_tri_layer_state
                                   1546 ;	-----------------------------------------
      007775                       1547 _update_tri_layer_state:
      007775 E5 82            [12] 1548 	mov	a,dpl
      007777 90 08 93         [24] 1549 	mov	dptr,#_update_tri_layer_state_state_10000_306
      00777A F0               [24] 1550 	movx	@dptr,a
                                   1551 ;	quantum/action_layer.c:479: layer_state_t mask12 = ((layer_state_t)1 << layer1) | ((layer_state_t)1 << layer2);
      00777B 90 08 90         [24] 1552 	mov	dptr,#_update_tri_layer_state_PARM_2
      00777E E0               [24] 1553 	movx	a,@dptr
      00777F F5 F0            [12] 1554 	mov	b, a
      007781 05 F0            [12] 1555 	inc	b
      007783 74 01            [12] 1556 	mov	a,#0x01
      007785 80 02            [24] 1557 	sjmp	00113$
      007787                       1558 00112$:
      007787 25 E0            [12] 1559 	add	a,acc
      007789                       1560 00113$:
      007789 D5 F0 FB         [24] 1561 	djnz	b,00112$
      00778C FF               [12] 1562 	mov	r7,a
      00778D 90 08 91         [24] 1563 	mov	dptr,#_update_tri_layer_state_PARM_3
      007790 E0               [24] 1564 	movx	a,@dptr
      007791 F5 F0            [12] 1565 	mov	b, a
      007793 05 F0            [12] 1566 	inc	b
      007795 74 01            [12] 1567 	mov	a,#0x01
      007797 80 02            [24] 1568 	sjmp	00115$
      007799                       1569 00114$:
      007799 25 E0            [12] 1570 	add	a,acc
      00779B                       1571 00115$:
      00779B D5 F0 FB         [24] 1572 	djnz	b,00114$
      00779E 42 07            [12] 1573 	orl	ar7,a
                                   1574 ;	quantum/action_layer.c:480: layer_state_t mask3  = (layer_state_t)1 << layer3;
      0077A0 90 08 92         [24] 1575 	mov	dptr,#_update_tri_layer_state_PARM_4
      0077A3 E0               [24] 1576 	movx	a,@dptr
      0077A4 F5 F0            [12] 1577 	mov	b, a
      0077A6 05 F0            [12] 1578 	inc	b
      0077A8 74 01            [12] 1579 	mov	a,#0x01
      0077AA 80 02            [24] 1580 	sjmp	00117$
      0077AC                       1581 00116$:
      0077AC 25 E0            [12] 1582 	add	a,acc
      0077AE                       1583 00117$:
      0077AE D5 F0 FB         [24] 1584 	djnz	b,00116$
      0077B1 FE               [12] 1585 	mov	r6,a
                                   1586 ;	quantum/action_layer.c:481: return (state & mask12) == mask12 ? (state | mask3) : (state & ~mask3);
      0077B2 90 08 93         [24] 1587 	mov	dptr,#_update_tri_layer_state_state_10000_306
      0077B5 E0               [24] 1588 	movx	a,@dptr
      0077B6 FD               [12] 1589 	mov	r5,a
      0077B7 EF               [12] 1590 	mov	a,r7
      0077B8 5D               [12] 1591 	anl	a,r5
      0077B9 B5 07 05         [24] 1592 	cjne	a,ar7,00103$
      0077BC EE               [12] 1593 	mov	a,r6
      0077BD 4D               [12] 1594 	orl	a,r5
      0077BE FF               [12] 1595 	mov	r7,a
      0077BF 80 05            [24] 1596 	sjmp	00104$
      0077C1                       1597 00103$:
      0077C1 74 FF            [12] 1598 	mov	a,#0xff
      0077C3 6E               [12] 1599 	xrl	a,r6
      0077C4 5D               [12] 1600 	anl	a,r5
      0077C5 FF               [12] 1601 	mov	r7,a
      0077C6                       1602 00104$:
      0077C6 8F 82            [24] 1603 	mov	dpl, r7
                                   1604 ;	quantum/action_layer.c:482: }
      0077C8 22               [24] 1605 	ret
                                   1606 ;------------------------------------------------------------
                                   1607 ;Allocation info for local variables in function 'update_tri_layer'
                                   1608 ;------------------------------------------------------------
                                   1609 ;layer2        Allocated with name '_update_tri_layer_PARM_2'
                                   1610 ;layer3        Allocated with name '_update_tri_layer_PARM_3'
                                   1611 ;layer1        Allocated with name '_update_tri_layer_layer1_10000_308'
                                   1612 ;------------------------------------------------------------
                                   1613 ;	quantum/action_layer.c:484: void update_tri_layer(uint8_t layer1, uint8_t layer2, uint8_t layer3) {
                                   1614 ;	-----------------------------------------
                                   1615 ;	 function update_tri_layer
                                   1616 ;	-----------------------------------------
      0077C9                       1617 _update_tri_layer:
      0077C9 E5 82            [12] 1618 	mov	a,dpl
      0077CB 90 08 96         [24] 1619 	mov	dptr,#_update_tri_layer_layer1_10000_308
      0077CE F0               [24] 1620 	movx	@dptr,a
                                   1621 ;	quantum/action_layer.c:485: layer_state_set(update_tri_layer_state(layer_state, layer1, layer2, layer3));
      0077CF 90 0B AD         [24] 1622 	mov	dptr,#_layer_state
      0077D2 E0               [24] 1623 	movx	a,@dptr
      0077D3 FF               [12] 1624 	mov	r7,a
      0077D4 90 08 96         [24] 1625 	mov	dptr,#_update_tri_layer_layer1_10000_308
      0077D7 E0               [24] 1626 	movx	a,@dptr
      0077D8 FE               [12] 1627 	mov	r6,a
      0077D9 90 08 94         [24] 1628 	mov	dptr,#_update_tri_layer_PARM_2
      0077DC E0               [24] 1629 	movx	a,@dptr
      0077DD FD               [12] 1630 	mov	r5,a
      0077DE 90 08 95         [24] 1631 	mov	dptr,#_update_tri_layer_PARM_3
      0077E1 E0               [24] 1632 	movx	a,@dptr
      0077E2 FC               [12] 1633 	mov	r4,a
      0077E3 90 08 90         [24] 1634 	mov	dptr,#_update_tri_layer_state_PARM_2
      0077E6 EE               [12] 1635 	mov	a,r6
      0077E7 F0               [24] 1636 	movx	@dptr,a
      0077E8 90 08 91         [24] 1637 	mov	dptr,#_update_tri_layer_state_PARM_3
      0077EB ED               [12] 1638 	mov	a,r5
      0077EC F0               [24] 1639 	movx	@dptr,a
      0077ED 90 08 92         [24] 1640 	mov	dptr,#_update_tri_layer_state_PARM_4
      0077F0 EC               [12] 1641 	mov	a,r4
      0077F1 F0               [24] 1642 	movx	@dptr,a
      0077F2 8F 82            [24] 1643 	mov	dpl, r7
      0077F4 12 77 75         [24] 1644 	lcall	_update_tri_layer_state
                                   1645 ;	quantum/action_layer.c:486: }
      0077F7 02 74 59         [24] 1646 	ljmp	_layer_state_set
                                   1647 	.area CSEG    (CODE)
                                   1648 	.area CONST   (CODE)
                                   1649 	.area XINIT   (CODE)
      00BD6B                       1650 __xinit__default_layer_state:
      00BD6B 00                    1651 	.db #0x00	; 0
      00BD6C                       1652 __xinit__layer_state:
      00BD6C 00                    1653 	.db #0x00	; 0
                                   1654 	.area CABS    (ABS,CODE)
                                   1655 
                                   1656 ; Experimental exact instruction outlining.
                                   1657 	.globl _ak820_outline_0001
                                   1658 	.globl _ak820_outline_0013
                                   1659 
                                   1660 	.area CSEG (CODE)
                                   1661 ; function ak820_outline_0001
      0077FA                       1662 _ak820_outline_0001:
      0077FA A3               [24] 1663 	inc	dptr
      0077FB F0               [24] 1664 	movx	@dptr,a
      0077FC E4               [12] 1665 	clr	a
      0077FD A3               [24] 1666 	inc	dptr
      0077FE F0               [24] 1667 	movx	@dptr,a
      0077FF 90 0B 92         [24] 1668 	mov	dptr,#___memcpy_PARM_3
      007802 74 02            [12] 1669 	mov	a,#0x02
      007804 F0               [24] 1670 	movx	@dptr,a
      007805 E4               [12] 1671 	clr	a
      007806 A3               [24] 1672 	inc	dptr
      007807 F0               [24] 1673 	movx	@dptr,a
      007808 22               [24] 1674 	ret
