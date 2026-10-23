                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module vial
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _unregister_code16
                                     12 	.globl _register_code16
                                     13 	.globl _get_tri_layer_adjust_layer
                                     14 	.globl _get_tri_layer_upper_layer
                                     15 	.globl _get_tri_layer_lower_layer
                                     16 	.globl _read_source_keycode_cache
                                     17 	.globl _update_tri_layer
                                     18 	.globl _layer_off
                                     19 	.globl _matrix_is_on
                                     20 	.globl _dynamic_keymap_set_encoder
                                     21 	.globl _dynamic_keymap_get_encoder
                                     22 	.globl _repeat_key_cancel
                                     23 	.globl _clear_keyboard
                                     24 	.globl _action_exec
                                     25 	.globl _timer_elapsed32
                                     26 	.globl _timer_read32
                                     27 	.globl _timer_read
                                     28 	.globl _ADC_START
                                     29 	.globl _S0_R_FIFO
                                     30 	.globl _S0_T_FIFO
                                     31 	.globl _S0_FREE
                                     32 	.globl _S0_IF_BYTE
                                     33 	.globl _S0_IF_FIRST
                                     34 	.globl _S0_IF_OV
                                     35 	.globl _S0_FST_ACT
                                     36 	.globl _CP_RL2
                                     37 	.globl _C_T2
                                     38 	.globl _TR2
                                     39 	.globl _EXEN2
                                     40 	.globl _TCLK
                                     41 	.globl _RCLK
                                     42 	.globl _EXF2
                                     43 	.globl _CAP1F
                                     44 	.globl _TF2
                                     45 	.globl _RI
                                     46 	.globl _TI
                                     47 	.globl _RB8
                                     48 	.globl _TB8
                                     49 	.globl _REN
                                     50 	.globl _SM2
                                     51 	.globl _SM1
                                     52 	.globl _SM0
                                     53 	.globl _IT0
                                     54 	.globl _IE0
                                     55 	.globl _IT1
                                     56 	.globl _IE1
                                     57 	.globl _TR0
                                     58 	.globl _TF0
                                     59 	.globl _TR1
                                     60 	.globl _TF1
                                     61 	.globl _P4_0
                                     62 	.globl _P4_1
                                     63 	.globl _P4_2
                                     64 	.globl _P4_3
                                     65 	.globl _P4_4
                                     66 	.globl _P4_5
                                     67 	.globl _P4_6
                                     68 	.globl _RXD
                                     69 	.globl _TXD
                                     70 	.globl _INT0
                                     71 	.globl _INT1
                                     72 	.globl _T0
                                     73 	.globl _T1
                                     74 	.globl _MOSI1
                                     75 	.globl _MISO1
                                     76 	.globl _SCK1
                                     77 	.globl _P3_0
                                     78 	.globl _P3_1
                                     79 	.globl _P3_2
                                     80 	.globl _P3_3
                                     81 	.globl _P3_4
                                     82 	.globl _P3_5
                                     83 	.globl _P3_6
                                     84 	.globl _P3_7
                                     85 	.globl _CAP1_
                                     86 	.globl _T2_
                                     87 	.globl _CAP2_
                                     88 	.globl _T2EX_
                                     89 	.globl _RXD1
                                     90 	.globl _TXD1
                                     91 	.globl _P2_0
                                     92 	.globl _P2_1
                                     93 	.globl _P2_2
                                     94 	.globl _P2_3
                                     95 	.globl _P2_4
                                     96 	.globl _P2_5
                                     97 	.globl _P2_6
                                     98 	.globl _P2_7
                                     99 	.globl _AIN0
                                    100 	.globl _AIN1
                                    101 	.globl _AIN2
                                    102 	.globl _AIN3
                                    103 	.globl _AIN4
                                    104 	.globl _AIN5
                                    105 	.globl _AIN6
                                    106 	.globl _AIN7
                                    107 	.globl _CAP1
                                    108 	.globl _T2
                                    109 	.globl _CAP2
                                    110 	.globl _T2EX
                                    111 	.globl _INT0_
                                    112 	.globl _SCS
                                    113 	.globl _MOSI
                                    114 	.globl _MISO
                                    115 	.globl _SCK
                                    116 	.globl _RXD1_
                                    117 	.globl _TXD1_
                                    118 	.globl _P1_0
                                    119 	.globl _P1_1
                                    120 	.globl _P1_2
                                    121 	.globl _P1_3
                                    122 	.globl _P1_4
                                    123 	.globl _P1_5
                                    124 	.globl _P1_6
                                    125 	.globl _P1_7
                                    126 	.globl _AIN8
                                    127 	.globl _AIN9
                                    128 	.globl _AIN10
                                    129 	.globl _AIN11
                                    130 	.globl _AIN12
                                    131 	.globl _AIN13
                                    132 	.globl _RXD_
                                    133 	.globl _TXD_
                                    134 	.globl _SCL0
                                    135 	.globl _SDA0
                                    136 	.globl _P0_0
                                    137 	.globl _P0_1
                                    138 	.globl _P0_2
                                    139 	.globl _P0_3
                                    140 	.globl _P0_4
                                    141 	.globl _P0_5
                                    142 	.globl _P0_6
                                    143 	.globl _P0_7
                                    144 	.globl _IE_SPI0
                                    145 	.globl _IE_USB
                                    146 	.globl _IE_ADC
                                    147 	.globl _IE_UART1
                                    148 	.globl _IE_PWM_I2C
                                    149 	.globl _IE_GPIO
                                    150 	.globl _IE_WDOG
                                    151 	.globl _PX0
                                    152 	.globl _PT0
                                    153 	.globl _PX1
                                    154 	.globl _PT1
                                    155 	.globl _PS
                                    156 	.globl _PT2
                                    157 	.globl _PL_FLAG
                                    158 	.globl _PH_FLAG
                                    159 	.globl _EX0
                                    160 	.globl _ET0
                                    161 	.globl _EX1
                                    162 	.globl _ET1
                                    163 	.globl _ES
                                    164 	.globl _ET2
                                    165 	.globl _E_DIS
                                    166 	.globl _EA
                                    167 	.globl _P
                                    168 	.globl _F1
                                    169 	.globl _OV
                                    170 	.globl _RS0
                                    171 	.globl _RS1
                                    172 	.globl _F0
                                    173 	.globl _AC
                                    174 	.globl _CY
                                    175 	.globl _I2CS_INT_ST
                                    176 	.globl _I2CX_INT
                                    177 	.globl _LED_STATUS
                                    178 	.globl _LED_DMA_H
                                    179 	.globl _LED_DMA_L
                                    180 	.globl _LED_DMA
                                    181 	.globl _LED_PWM_OE
                                    182 	.globl _LED_COMMON
                                    183 	.globl _ADC_CHAN
                                    184 	.globl _ADC_DAT_H
                                    185 	.globl _ADC_DAT_L
                                    186 	.globl _ADC_DAT
                                    187 	.globl _ADC_CTRL
                                    188 	.globl _SPI1_CK_SE
                                    189 	.globl _SPI1_CTRL
                                    190 	.globl _SPI1_DATA
                                    191 	.globl _SPI1_STAT
                                    192 	.globl _SIF1
                                    193 	.globl _SBAUD1
                                    194 	.globl _SBUF1
                                    195 	.globl _SCON1
                                    196 	.globl _SPI0_SETUP
                                    197 	.globl _SPI0_CK_SE
                                    198 	.globl _SPI0_CTRL
                                    199 	.globl _SPI0_DATA
                                    200 	.globl _SPI0_STAT
                                    201 	.globl _T2CAP1H
                                    202 	.globl _T2CAP1L
                                    203 	.globl _T2CAP1
                                    204 	.globl _TH2
                                    205 	.globl _TL2
                                    206 	.globl _T2COUNT
                                    207 	.globl _RCAP2H
                                    208 	.globl _RCAP2L
                                    209 	.globl _RCAP2
                                    210 	.globl _T2MOD
                                    211 	.globl _T2CON
                                    212 	.globl _SBUF
                                    213 	.globl _SCON
                                    214 	.globl _TH1
                                    215 	.globl _TH0
                                    216 	.globl _TL1
                                    217 	.globl _TL0
                                    218 	.globl _TMOD
                                    219 	.globl _TCON
                                    220 	.globl _XBUS_AUX
                                    221 	.globl _P7
                                    222 	.globl _P6_DIR
                                    223 	.globl _P6_OUT_PU
                                    224 	.globl _P6_IN
                                    225 	.globl _P5_DIR
                                    226 	.globl _P5_OUT_PU
                                    227 	.globl _P5_IN
                                    228 	.globl _P4_LED_KEY
                                    229 	.globl _P4_DIR_PU
                                    230 	.globl _P4_MOD_OC
                                    231 	.globl _P4
                                    232 	.globl _P3_DIR_PU
                                    233 	.globl _P3_MOD_OC
                                    234 	.globl _P3
                                    235 	.globl _P2_DIR_PU
                                    236 	.globl _P2_MOD_OC
                                    237 	.globl _P2
                                    238 	.globl _P1_DIR_PU
                                    239 	.globl _P1_MOD_OC
                                    240 	.globl _P1
                                    241 	.globl _P0_DIR_PU
                                    242 	.globl _P0_MOD_OC
                                    243 	.globl _P0
                                    244 	.globl _ROM_CTRL
                                    245 	.globl _ROM_DATA_HH
                                    246 	.globl _ROM_DATA_HL
                                    247 	.globl _ROM_DATA_HI
                                    248 	.globl _ROM_ADDR_H
                                    249 	.globl _ROM_ADDR_L
                                    250 	.globl _ROM_ADDR
                                    251 	.globl _GPIO_IE
                                    252 	.globl _IP_EX
                                    253 	.globl _IE_EX
                                    254 	.globl _IP
                                    255 	.globl _IE
                                    256 	.globl _WDOG_COUNT
                                    257 	.globl _RESET_KEEP
                                    258 	.globl _WAKE_CTRL
                                    259 	.globl _CLOCK_CFG
                                    260 	.globl _POWER_CFG
                                    261 	.globl _PCON
                                    262 	.globl _GLOBAL_CFG
                                    263 	.globl _SAFE_MOD
                                    264 	.globl _DPH
                                    265 	.globl _DPL
                                    266 	.globl _SP
                                    267 	.globl _A_INV
                                    268 	.globl _B
                                    269 	.globl _ACC
                                    270 	.globl _PSW
                                    271 	.globl _vial_unlock_in_progress
                                    272 	.globl _vial_unlocked
                                    273 	.globl _g_vial_magic_keycode_override
                                    274 	.globl _vial_handle_cmd_PARM_2
                                    275 	.globl _vial_unlock_task
                                    276 	.globl _vial_init
                                    277 	.globl _vial_handle_cmd
                                    278 	.globl _vial_keycode_down
                                    279 	.globl _vial_keycode_up
                                    280 	.globl _vial_keycode_tap
                                    281 ;--------------------------------------------------------
                                    282 ; special function registers
                                    283 ;--------------------------------------------------------
                                    284 	.area RSEG    (ABS,DATA)
      000000                        285 	.org 0x0000
                           0000D0   286 _PSW	=	0x00d0
                           0000E0   287 _ACC	=	0x00e0
                           0000F0   288 _B	=	0x00f0
                           0000FD   289 _A_INV	=	0x00fd
                           000081   290 _SP	=	0x0081
                           000082   291 _DPL	=	0x0082
                           000083   292 _DPH	=	0x0083
                           0000A1   293 _SAFE_MOD	=	0x00a1
                           0000B1   294 _GLOBAL_CFG	=	0x00b1
                           000087   295 _PCON	=	0x0087
                           0000BA   296 _POWER_CFG	=	0x00ba
                           0000B9   297 _CLOCK_CFG	=	0x00b9
                           0000A9   298 _WAKE_CTRL	=	0x00a9
                           0000FE   299 _RESET_KEEP	=	0x00fe
                           0000FF   300 _WDOG_COUNT	=	0x00ff
                           0000A8   301 _IE	=	0x00a8
                           0000B8   302 _IP	=	0x00b8
                           0000E8   303 _IE_EX	=	0x00e8
                           0000E9   304 _IP_EX	=	0x00e9
                           0000B2   305 _GPIO_IE	=	0x00b2
                           008584   306 _ROM_ADDR	=	0x8584
                           000084   307 _ROM_ADDR_L	=	0x0084
                           000085   308 _ROM_ADDR_H	=	0x0085
                           008F8E   309 _ROM_DATA_HI	=	0x8f8e
                           00008E   310 _ROM_DATA_HL	=	0x008e
                           00008F   311 _ROM_DATA_HH	=	0x008f
                           000086   312 _ROM_CTRL	=	0x0086
                           000080   313 _P0	=	0x0080
                           0000C4   314 _P0_MOD_OC	=	0x00c4
                           0000C5   315 _P0_DIR_PU	=	0x00c5
                           000090   316 _P1	=	0x0090
                           000092   317 _P1_MOD_OC	=	0x0092
                           000093   318 _P1_DIR_PU	=	0x0093
                           0000A0   319 _P2	=	0x00a0
                           000094   320 _P2_MOD_OC	=	0x0094
                           000095   321 _P2_DIR_PU	=	0x0095
                           0000B0   322 _P3	=	0x00b0
                           000096   323 _P3_MOD_OC	=	0x0096
                           000097   324 _P3_DIR_PU	=	0x0097
                           0000C0   325 _P4	=	0x00c0
                           0000C2   326 _P4_MOD_OC	=	0x00c2
                           0000C3   327 _P4_DIR_PU	=	0x00c3
                           0000C1   328 _P4_LED_KEY	=	0x00c1
                           0000AA   329 _P5_IN	=	0x00aa
                           0000AB   330 _P5_OUT_PU	=	0x00ab
                           0000AC   331 _P5_DIR	=	0x00ac
                           0000AD   332 _P6_IN	=	0x00ad
                           0000AE   333 _P6_OUT_PU	=	0x00ae
                           0000AF   334 _P6_DIR	=	0x00af
                           0000F1   335 _P7	=	0x00f1
                           0000A2   336 _XBUS_AUX	=	0x00a2
                           000088   337 _TCON	=	0x0088
                           000089   338 _TMOD	=	0x0089
                           00008A   339 _TL0	=	0x008a
                           00008B   340 _TL1	=	0x008b
                           00008C   341 _TH0	=	0x008c
                           00008D   342 _TH1	=	0x008d
                           000098   343 _SCON	=	0x0098
                           000099   344 _SBUF	=	0x0099
                           0000C8   345 _T2CON	=	0x00c8
                           0000C9   346 _T2MOD	=	0x00c9
                           00CBCA   347 _RCAP2	=	0xcbca
                           0000CA   348 _RCAP2L	=	0x00ca
                           0000CB   349 _RCAP2H	=	0x00cb
                           00CDCC   350 _T2COUNT	=	0xcdcc
                           0000CC   351 _TL2	=	0x00cc
                           0000CD   352 _TH2	=	0x00cd
                           00CFCE   353 _T2CAP1	=	0xcfce
                           0000CE   354 _T2CAP1L	=	0x00ce
                           0000CF   355 _T2CAP1H	=	0x00cf
                           0000F8   356 _SPI0_STAT	=	0x00f8
                           0000F9   357 _SPI0_DATA	=	0x00f9
                           0000FA   358 _SPI0_CTRL	=	0x00fa
                           0000FB   359 _SPI0_CK_SE	=	0x00fb
                           0000FC   360 _SPI0_SETUP	=	0x00fc
                           0000BC   361 _SCON1	=	0x00bc
                           0000BD   362 _SBUF1	=	0x00bd
                           0000BE   363 _SBAUD1	=	0x00be
                           0000BF   364 _SIF1	=	0x00bf
                           0000B4   365 _SPI1_STAT	=	0x00b4
                           0000B5   366 _SPI1_DATA	=	0x00b5
                           0000B6   367 _SPI1_CTRL	=	0x00b6
                           0000B7   368 _SPI1_CK_SE	=	0x00b7
                           0000F3   369 _ADC_CTRL	=	0x00f3
                           00F5F4   370 _ADC_DAT	=	0xf5f4
                           0000F4   371 _ADC_DAT_L	=	0x00f4
                           0000F5   372 _ADC_DAT_H	=	0x00f5
                           0000F6   373 _ADC_CHAN	=	0x00f6
                           0000A6   374 _LED_COMMON	=	0x00a6
                           0000A7   375 _LED_PWM_OE	=	0x00a7
                           00C7C6   376 _LED_DMA	=	0xc7c6
                           0000C6   377 _LED_DMA_L	=	0x00c6
                           0000C7   378 _LED_DMA_H	=	0x00c7
                           0000F7   379 _LED_STATUS	=	0x00f7
                           0000B3   380 _I2CX_INT	=	0x00b3
                           0000BB   381 _I2CS_INT_ST	=	0x00bb
                                    382 ;--------------------------------------------------------
                                    383 ; special function bits
                                    384 ;--------------------------------------------------------
                                    385 	.area RSEG    (ABS,DATA)
      000000                        386 	.org 0x0000
                           0000D7   387 _CY	=	0x00d7
                           0000D6   388 _AC	=	0x00d6
                           0000D5   389 _F0	=	0x00d5
                           0000D4   390 _RS1	=	0x00d4
                           0000D3   391 _RS0	=	0x00d3
                           0000D2   392 _OV	=	0x00d2
                           0000D1   393 _F1	=	0x00d1
                           0000D0   394 _P	=	0x00d0
                           0000AF   395 _EA	=	0x00af
                           0000AE   396 _E_DIS	=	0x00ae
                           0000AD   397 _ET2	=	0x00ad
                           0000AC   398 _ES	=	0x00ac
                           0000AB   399 _ET1	=	0x00ab
                           0000AA   400 _EX1	=	0x00aa
                           0000A9   401 _ET0	=	0x00a9
                           0000A8   402 _EX0	=	0x00a8
                           0000BF   403 _PH_FLAG	=	0x00bf
                           0000BE   404 _PL_FLAG	=	0x00be
                           0000BD   405 _PT2	=	0x00bd
                           0000BC   406 _PS	=	0x00bc
                           0000BB   407 _PT1	=	0x00bb
                           0000BA   408 _PX1	=	0x00ba
                           0000B9   409 _PT0	=	0x00b9
                           0000B8   410 _PX0	=	0x00b8
                           0000EF   411 _IE_WDOG	=	0x00ef
                           0000EE   412 _IE_GPIO	=	0x00ee
                           0000ED   413 _IE_PWM_I2C	=	0x00ed
                           0000EC   414 _IE_UART1	=	0x00ec
                           0000EB   415 _IE_ADC	=	0x00eb
                           0000E9   416 _IE_USB	=	0x00e9
                           0000E8   417 _IE_SPI0	=	0x00e8
                           000087   418 _P0_7	=	0x0087
                           000086   419 _P0_6	=	0x0086
                           000085   420 _P0_5	=	0x0085
                           000084   421 _P0_4	=	0x0084
                           000083   422 _P0_3	=	0x0083
                           000082   423 _P0_2	=	0x0082
                           000081   424 _P0_1	=	0x0081
                           000080   425 _P0_0	=	0x0080
                           000081   426 _SDA0	=	0x0081
                           000080   427 _SCL0	=	0x0080
                           000083   428 _TXD_	=	0x0083
                           000082   429 _RXD_	=	0x0082
                           000085   430 _AIN13	=	0x0085
                           000084   431 _AIN12	=	0x0084
                           000083   432 _AIN11	=	0x0083
                           000082   433 _AIN10	=	0x0082
                           000081   434 _AIN9	=	0x0081
                           000080   435 _AIN8	=	0x0080
                           000097   436 _P1_7	=	0x0097
                           000096   437 _P1_6	=	0x0096
                           000095   438 _P1_5	=	0x0095
                           000094   439 _P1_4	=	0x0094
                           000093   440 _P1_3	=	0x0093
                           000092   441 _P1_2	=	0x0092
                           000091   442 _P1_1	=	0x0091
                           000090   443 _P1_0	=	0x0090
                           000097   444 _TXD1_	=	0x0097
                           000096   445 _RXD1_	=	0x0096
                           000097   446 _SCK	=	0x0097
                           000096   447 _MISO	=	0x0096
                           000095   448 _MOSI	=	0x0095
                           000094   449 _SCS	=	0x0094
                           000092   450 _INT0_	=	0x0092
                           000091   451 _T2EX	=	0x0091
                           000091   452 _CAP2	=	0x0091
                           000090   453 _T2	=	0x0090
                           000090   454 _CAP1	=	0x0090
                           000097   455 _AIN7	=	0x0097
                           000096   456 _AIN6	=	0x0096
                           000095   457 _AIN5	=	0x0095
                           000094   458 _AIN4	=	0x0094
                           000093   459 _AIN3	=	0x0093
                           000092   460 _AIN2	=	0x0092
                           000091   461 _AIN1	=	0x0091
                           000090   462 _AIN0	=	0x0090
                           0000A7   463 _P2_7	=	0x00a7
                           0000A6   464 _P2_6	=	0x00a6
                           0000A5   465 _P2_5	=	0x00a5
                           0000A4   466 _P2_4	=	0x00a4
                           0000A3   467 _P2_3	=	0x00a3
                           0000A2   468 _P2_2	=	0x00a2
                           0000A1   469 _P2_1	=	0x00a1
                           0000A0   470 _P2_0	=	0x00a0
                           0000A7   471 _TXD1	=	0x00a7
                           0000A6   472 _RXD1	=	0x00a6
                           0000A5   473 _T2EX_	=	0x00a5
                           0000A5   474 _CAP2_	=	0x00a5
                           0000A4   475 _T2_	=	0x00a4
                           0000A4   476 _CAP1_	=	0x00a4
                           0000B7   477 _P3_7	=	0x00b7
                           0000B6   478 _P3_6	=	0x00b6
                           0000B5   479 _P3_5	=	0x00b5
                           0000B4   480 _P3_4	=	0x00b4
                           0000B3   481 _P3_3	=	0x00b3
                           0000B2   482 _P3_2	=	0x00b2
                           0000B1   483 _P3_1	=	0x00b1
                           0000B0   484 _P3_0	=	0x00b0
                           0000B7   485 _SCK1	=	0x00b7
                           0000B6   486 _MISO1	=	0x00b6
                           0000B5   487 _MOSI1	=	0x00b5
                           0000B5   488 _T1	=	0x00b5
                           0000B4   489 _T0	=	0x00b4
                           0000B3   490 _INT1	=	0x00b3
                           0000B2   491 _INT0	=	0x00b2
                           0000B1   492 _TXD	=	0x00b1
                           0000B0   493 _RXD	=	0x00b0
                           0000C6   494 _P4_6	=	0x00c6
                           0000C5   495 _P4_5	=	0x00c5
                           0000C4   496 _P4_4	=	0x00c4
                           0000C3   497 _P4_3	=	0x00c3
                           0000C2   498 _P4_2	=	0x00c2
                           0000C1   499 _P4_1	=	0x00c1
                           0000C0   500 _P4_0	=	0x00c0
                           00008F   501 _TF1	=	0x008f
                           00008E   502 _TR1	=	0x008e
                           00008D   503 _TF0	=	0x008d
                           00008C   504 _TR0	=	0x008c
                           00008B   505 _IE1	=	0x008b
                           00008A   506 _IT1	=	0x008a
                           000089   507 _IE0	=	0x0089
                           000088   508 _IT0	=	0x0088
                           00009F   509 _SM0	=	0x009f
                           00009E   510 _SM1	=	0x009e
                           00009D   511 _SM2	=	0x009d
                           00009C   512 _REN	=	0x009c
                           00009B   513 _TB8	=	0x009b
                           00009A   514 _RB8	=	0x009a
                           000099   515 _TI	=	0x0099
                           000098   516 _RI	=	0x0098
                           0000CF   517 _TF2	=	0x00cf
                           0000CF   518 _CAP1F	=	0x00cf
                           0000CE   519 _EXF2	=	0x00ce
                           0000CD   520 _RCLK	=	0x00cd
                           0000CC   521 _TCLK	=	0x00cc
                           0000CB   522 _EXEN2	=	0x00cb
                           0000CA   523 _TR2	=	0x00ca
                           0000C9   524 _C_T2	=	0x00c9
                           0000C8   525 _CP_RL2	=	0x00c8
                           0000FF   526 _S0_FST_ACT	=	0x00ff
                           0000FE   527 _S0_IF_OV	=	0x00fe
                           0000FD   528 _S0_IF_FIRST	=	0x00fd
                           0000FC   529 _S0_IF_BYTE	=	0x00fc
                           0000FB   530 _S0_FREE	=	0x00fb
                           0000FA   531 _S0_T_FIFO	=	0x00fa
                           0000F8   532 _S0_R_FIFO	=	0x00f8
                           0000F7   533 _ADC_START	=	0x00f7
                                    534 ;--------------------------------------------------------
                                    535 ; overlayable register banks
                                    536 ;--------------------------------------------------------
                                    537 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        538 	.ds 8
                                    539 ;--------------------------------------------------------
                                    540 ; internal ram data
                                    541 ;--------------------------------------------------------
                                    542 	.area DSEG    (DATA)
      00004B                        543 _vial_handle_cmd_sloc0_1_0:
      00004B                        544 	.ds 2
      00004D                        545 _vial_handle_cmd_sloc1_1_0:
      00004D                        546 	.ds 2
      00004F                        547 _vial_handle_cmd_sloc2_1_0:
      00004F                        548 	.ds 2
      000051                        549 _vial_handle_cmd_sloc3_1_0:
      000051                        550 	.ds 2
                                    551 ;--------------------------------------------------------
                                    552 ; overlayable items in internal ram
                                    553 ;--------------------------------------------------------
                                    554 ;--------------------------------------------------------
                                    555 ; indirectly addressable internal ram data
                                    556 ;--------------------------------------------------------
                                    557 	.area ISEG    (DATA)
                                    558 ;--------------------------------------------------------
                                    559 ; absolute internal ram data
                                    560 ;--------------------------------------------------------
                                    561 	.area IABS    (ABS,DATA)
                                    562 	.area IABS    (ABS,DATA)
                                    563 ;--------------------------------------------------------
                                    564 ; bit data
                                    565 ;--------------------------------------------------------
                                    566 	.area BSEG    (BIT)
                                    567 ;--------------------------------------------------------
                                    568 ; paged external ram data
                                    569 ;--------------------------------------------------------
                                    570 	.area PSEG    (PAG,XDATA)
                                    571 ;--------------------------------------------------------
                                    572 ; uninitialized external ram data
                                    573 ;--------------------------------------------------------
                                    574 	.area XSEG    (XDATA)
      000A58                        575 _vial_unlock_timer:
      000A58                        576 	.ds 4
      000A5C                        577 _vial_unlock_holding:
      000A5C                        578 	.ds 1
      000A5D                        579 _vial_keycode_firewall_in_10000_581:
      000A5D                        580 	.ds 2
      000A5F                        581 _vial_fill_packet_PARM_2:
      000A5F                        582 	.ds 1
      000A60                        583 _vial_fill_packet_msg_10000_584:
      000A60                        584 	.ds 2
      000A62                        585 _vial_release_held_state_key_10000_588:
      000A62                        586 	.ds 2
      000A64                        587 _vial_handle_cmd_PARM_2:
      000A64                        588 	.ds 1
      000A65                        589 _vial_handle_cmd_data_10000_601:
      000A65                        590 	.ds 3
      000A68                        591 _g_vial_magic_keycode_override::
      000A68                        592 	.ds 2
      000A6A                        593 _vial_keycode_down_keycode_10000_629:
      000A6A                        594 	.ds 2
      000A6C                        595 _vial_keycode_down_dummy_event_30000_633:
      000A6C                        596 	.ds 6
      000A72                        597 _vial_keycode_up_keycode_10000_634:
      000A72                        598 	.ds 2
      000A74                        599 _vial_keycode_up_dummy_event_30000_638:
      000A74                        600 	.ds 6
      000A7A                        601 _vial_keycode_tap_keycode_10000_639:
      000A7A                        602 	.ds 2
                                    603 ;--------------------------------------------------------
                                    604 ; absolute external ram data
                                    605 ;--------------------------------------------------------
                                    606 	.area XABS    (ABS,XDATA)
                                    607 ;--------------------------------------------------------
                                    608 ; initialized external ram data
                                    609 ;--------------------------------------------------------
                                    610 	.area XISEG   (XDATA)
      000C08                        611 _vial_unlocked::
      000C08                        612 	.ds 1
      000C09                        613 _vial_unlock_in_progress::
      000C09                        614 	.ds 1
      000C0A                        615 _vial_unlock_counter:
      000C0A                        616 	.ds 1
      000C0B                        617 _vial_unlock_combo_rows:
      000C0B                        618 	.ds 2
      000C0D                        619 _vial_unlock_combo_cols:
      000C0D                        620 	.ds 2
                                    621 	.area HOME    (CODE)
                                    622 	.area GSINIT0 (CODE)
                                    623 	.area GSINIT1 (CODE)
                                    624 	.area GSINIT2 (CODE)
                                    625 	.area GSINIT3 (CODE)
                                    626 	.area GSINIT4 (CODE)
                                    627 	.area GSINIT5 (CODE)
                                    628 	.area GSINIT  (CODE)
                                    629 	.area GSFINAL (CODE)
                                    630 	.area CSEG    (CODE)
                                    631 ;--------------------------------------------------------
                                    632 ; global & static initialisations
                                    633 ;--------------------------------------------------------
                                    634 	.area HOME    (CODE)
                                    635 	.area GSINIT  (CODE)
                                    636 	.area GSFINAL (CODE)
                                    637 	.area GSINIT  (CODE)
                                    638 ;--------------------------------------------------------
                                    639 ; Home
                                    640 ;--------------------------------------------------------
                                    641 	.area HOME    (CODE)
                                    642 	.area HOME    (CODE)
                                    643 ;--------------------------------------------------------
                                    644 ; code
                                    645 ;--------------------------------------------------------
                                    646 	.area CSEG    (CODE)
                                    647 ;------------------------------------------------------------
                                    648 ;Allocation info for local variables in function 'rgb_matrix_check_finished_leds'
                                    649 ;------------------------------------------------------------
                                    650 ;led_idx       Allocated with name '_rgb_matrix_check_finished_leds_led_idx_10000_297'
                                    651 ;------------------------------------------------------------
                                    652 ;	quantum/rgb_matrix/rgb_matrix.h:260: static inline bool rgb_matrix_check_finished_leds(uint8_t led_idx) {
                                    653 ;	-----------------------------------------
                           000007   654 	ar7 = 0x07
                           000006   655 	ar6 = 0x06
                           000005   656 	ar5 = 0x05
                           000004   657 	ar4 = 0x04
                           000003   658 	ar3 = 0x03
                           000002   659 	ar2 = 0x02
                           000001   660 	ar1 = 0x01
                           000000   661 	ar0 = 0x00
                                    662 ;	 function vial_unlock_task
                                    663 ;	-----------------------------------------
      00A7FF                        664 _vial_unlock_task:
                                    665 ;	quantum/vial.c:61: if (!vial_unlock_in_progress) return;
      00A7FF 90 0C 09         [24]  666 	mov	dptr,#_vial_unlock_in_progress
      00A802 E0               [24]  667 	movx	a,@dptr
      00A803 70 01            [24]  668 	jnz	00131$
      00A805 22               [24]  669 	ret
                                    670 ;	quantum/vial.c:62: for (uint8_t i = 0; i < VIAL_UNLOCK_NUM_KEYS; ++i) {
      00A806                        671 00131$:
      00A806 7F 00            [12]  672 	mov	r7,#0x00
      00A808                        673 00115$:
      00A808 BF 02 00         [24]  674 	cjne	r7,#0x02,00184$
      00A80B                        675 00184$:
      00A80B 50 37            [24]  676 	jnc	00105$
                                    677 ;	quantum/vial.c:63: if (!matrix_is_on(vial_unlock_combo_rows[i], vial_unlock_combo_cols[i])) {
      00A80D EF               [12]  678 	mov	a,r7
      00A80E 24 0B            [12]  679 	add	a, #_vial_unlock_combo_rows
      00A810 F5 82            [12]  680 	mov	dpl,a
      00A812 E4               [12]  681 	clr	a
      00A813 34 0C            [12]  682 	addc	a, #(_vial_unlock_combo_rows >> 8)
      00A815 F5 83            [12]  683 	mov	dph,a
      00A817 E0               [24]  684 	movx	a,@dptr
      00A818 FE               [12]  685 	mov	r6,a
      00A819 EF               [12]  686 	mov	a,r7
      00A81A 24 0D            [12]  687 	add	a, #_vial_unlock_combo_cols
      00A81C F5 82            [12]  688 	mov	dpl,a
      00A81E E4               [12]  689 	clr	a
      00A81F 34 0C            [12]  690 	addc	a, #(_vial_unlock_combo_cols >> 8)
      00A821 F5 83            [12]  691 	mov	dph,a
      00A823 E0               [24]  692 	movx	a,@dptr
      00A824 90 06 80         [24]  693 	mov	dptr,#_matrix_is_on_PARM_2
      00A827 F0               [24]  694 	movx	@dptr,a
      00A828 8E 82            [24]  695 	mov	dpl, r6
      00A82A C0 07            [24]  696 	push	ar7
      00A82C 12 53 0F         [24]  697 	lcall	_matrix_is_on
      00A82F E5 82            [12]  698 	mov	a, dpl
      00A831 D0 07            [24]  699 	pop	ar7
      00A833 70 0C            [24]  700 	jnz	00116$
                                    701 ;	quantum/vial.c:64: vial_unlock_holding = false;
      00A835 90 0A 5C         [24]  702 	mov	dptr,#_vial_unlock_holding
      00A838 E4               [12]  703 	clr	a
      00A839 F0               [24]  704 	movx	@dptr,a
                                    705 ;	quantum/vial.c:65: vial_unlock_counter = VIAL_UNLOCK_COUNTER_MAX;
      00A83A 90 0C 0A         [24]  706 	mov	dptr,#_vial_unlock_counter
      00A83D 74 1E            [12]  707 	mov	a,#0x1e
      00A83F F0               [24]  708 	movx	@dptr,a
                                    709 ;	quantum/vial.c:66: return;
      00A840 22               [24]  710 	ret
      00A841                        711 00116$:
                                    712 ;	quantum/vial.c:62: for (uint8_t i = 0; i < VIAL_UNLOCK_NUM_KEYS; ++i) {
      00A841 0F               [12]  713 	inc	r7
      00A842 80 C4            [24]  714 	sjmp	00115$
      00A844                        715 00105$:
                                    716 ;	quantum/vial.c:69: if (!vial_unlock_holding) {
      00A844 90 0A 5C         [24]  717 	mov	dptr,#_vial_unlock_holding
      00A847 E0               [24]  718 	movx	a,@dptr
      00A848 70 16            [24]  719 	jnz	00107$
                                    720 ;	quantum/vial.c:70: vial_unlock_holding = true;
      00A84A 90 0A 5C         [24]  721 	mov	dptr,#_vial_unlock_holding
      00A84D 74 01            [12]  722 	mov	a,#0x01
      00A84F F0               [24]  723 	movx	@dptr,a
                                    724 ;	quantum/vial.c:71: vial_unlock_timer = timer_read32();
      00A850 12 40 3C         [24]  725 	lcall	_timer_read32
      00A853 AC 82            [24]  726 	mov	r4, dpl
      00A855 AD 83            [24]  727 	mov	r5, dph
      00A857 AE F0            [24]  728 	mov	r6, b
      00A859 FF               [12]  729 	mov	r7, a
      00A85A 90 0A 58         [24]  730 	mov	dptr,#_vial_unlock_timer
      00A85D 12 87 E5         [24]  731 	lcall	_ak820_outline_0008
      00A860                        732 00107$:
                                    733 ;	quantum/vial.c:73: uint32_t elapsed = timer_elapsed32(vial_unlock_timer);
      00A860 90 0A 58         [24]  734 	mov	dptr,#_vial_unlock_timer
      00A863 E0               [24]  735 	movx	a,@dptr
      00A864 FC               [12]  736 	mov	r4,a
      00A865 A3               [24]  737 	inc	dptr
      00A866 E0               [24]  738 	movx	a,@dptr
      00A867 FD               [12]  739 	mov	r5,a
      00A868 A3               [24]  740 	inc	dptr
      00A869 E0               [24]  741 	movx	a,@dptr
      00A86A FE               [12]  742 	mov	r6,a
      00A86B A3               [24]  743 	inc	dptr
      00A86C E0               [24]  744 	movx	a,@dptr
      00A86D 8C 82            [24]  745 	mov	dpl,r4
      00A86F 8D 83            [24]  746 	mov	dph,r5
      00A871 8E F0            [24]  747 	mov	b,r6
      00A873 12 40 95         [24]  748 	lcall	_timer_elapsed32
      00A876 AC 82            [24]  749 	mov	r4, dpl
      00A878 AD 83            [24]  750 	mov	r5, dph
      00A87A AE F0            [24]  751 	mov	r6, b
      00A87C FF               [12]  752 	mov	r7, a
                                    753 ;	quantum/vial.c:77: while (counter && elapsed >= VIAL_UNLOCK_COUNTER_TICK_MS) {
      00A87D 7B 1E            [12]  754 	mov	r3,#0x1e
      00A87F                        755 00109$:
      00A87F EB               [12]  756 	mov	a,r3
      00A880 60 22            [24]  757 	jz	00111$
      00A882 C3               [12]  758 	clr	c
      00A883 EC               [12]  759 	mov	a,r4
      00A884 94 64            [12]  760 	subb	a,#0x64
      00A886 ED               [12]  761 	mov	a,r5
      00A887 94 00            [12]  762 	subb	a,#0x00
      00A889 EE               [12]  763 	mov	a,r6
      00A88A 94 00            [12]  764 	subb	a,#0x00
      00A88C EF               [12]  765 	mov	a,r7
      00A88D 94 00            [12]  766 	subb	a,#0x00
      00A88F 40 13            [24]  767 	jc	00111$
                                    768 ;	quantum/vial.c:78: elapsed -= VIAL_UNLOCK_COUNTER_TICK_MS;
      00A891 EC               [12]  769 	mov	a,r4
      00A892 24 9C            [12]  770 	add	a,#0x9c
      00A894 FC               [12]  771 	mov	r4,a
      00A895 ED               [12]  772 	mov	a,r5
      00A896 34 FF            [12]  773 	addc	a,#0xff
      00A898 FD               [12]  774 	mov	r5,a
      00A899 EE               [12]  775 	mov	a,r6
      00A89A 34 FF            [12]  776 	addc	a,#0xff
      00A89C FE               [12]  777 	mov	r6,a
      00A89D EF               [12]  778 	mov	a,r7
      00A89E 34 FF            [12]  779 	addc	a,#0xff
      00A8A0 FF               [12]  780 	mov	r7,a
                                    781 ;	quantum/vial.c:79: --counter;
      00A8A1 1B               [12]  782 	dec	r3
      00A8A2 80 DB            [24]  783 	sjmp	00109$
      00A8A4                        784 00111$:
                                    785 ;	quantum/vial.c:81: vial_unlock_counter = counter;
      00A8A4 90 0C 0A         [24]  786 	mov	dptr,#_vial_unlock_counter
      00A8A7 EB               [12]  787 	mov	a,r3
      00A8A8 F0               [24]  788 	movx	@dptr,a
                                    789 ;	quantum/vial.c:82: if (!counter) {
      00A8A9 EB               [12]  790 	mov	a,r3
      00A8AA 70 0A            [24]  791 	jnz	00117$
                                    792 ;	quantum/vial.c:83: vial_unlock_in_progress = 0;
      00A8AC 90 0C 09         [24]  793 	mov	dptr,#_vial_unlock_in_progress
      00A8AF E4               [12]  794 	clr	a
      00A8B0 F0               [24]  795 	movx	@dptr,a
                                    796 ;	quantum/vial.c:84: vial_unlocked = 1;
      00A8B1 90 0C 08         [24]  797 	mov	dptr,#_vial_unlocked
      00A8B4 04               [12]  798 	inc	a
      00A8B5 F0               [24]  799 	movx	@dptr,a
      00A8B6                        800 00117$:
                                    801 ;	quantum/vial.c:87: }
      00A8B6 22               [24]  802 	ret
                                    803 ;------------------------------------------------------------
                                    804 ;Allocation info for local variables in function 'vial_init'
                                    805 ;------------------------------------------------------------
                                    806 ;	quantum/vial.c:101: void vial_init(void) {
                                    807 ;	-----------------------------------------
                                    808 ;	 function vial_init
                                    809 ;	-----------------------------------------
      00A8B7                        810 _vial_init:
                                    811 ;	quantum/vial.c:111: }
      00A8B7 22               [24]  812 	ret
                                    813 ;------------------------------------------------------------
                                    814 ;Allocation info for local variables in function 'vial_keycode_firewall'
                                    815 ;------------------------------------------------------------
                                    816 ;in            Allocated with name '_vial_keycode_firewall_in_10000_581'
                                    817 ;------------------------------------------------------------
                                    818 ;	quantum/vial.c:113: __attribute__((unused)) static uint16_t vial_keycode_firewall(uint16_t in) {
                                    819 ;	-----------------------------------------
                                    820 ;	 function vial_keycode_firewall
                                    821 ;	-----------------------------------------
      00A8B8                        822 _vial_keycode_firewall:
      00A8B8 AF 83            [24]  823 	mov	r7,dph
      00A8BA E5 82            [12]  824 	mov	a,dpl
      00A8BC 90 0A 5D         [24]  825 	mov	dptr,#_vial_keycode_firewall_in_10000_581
      00A8BF F0               [24]  826 	movx	@dptr,a
      00A8C0 EF               [12]  827 	mov	a,r7
      00A8C1 A3               [24]  828 	inc	dptr
      00A8C2 F0               [24]  829 	movx	@dptr,a
                                    830 ;	quantum/vial.c:114: if (in == QK_BOOT && !vial_unlocked)
      00A8C3 90 0A 5D         [24]  831 	mov	dptr,#_vial_keycode_firewall_in_10000_581
      00A8C6 12 86 24         [24]  832 	lcall	_ak820_outline_0012
      00A8C9 BC 00 0D         [24]  833 	cjne	r4,#0x00,00102$
      00A8CC BD 7C 0A         [24]  834 	cjne	r5,#0x7c,00102$
      00A8CF 90 0C 08         [24]  835 	mov	dptr,#_vial_unlocked
      00A8D2 E0               [24]  836 	movx	a,@dptr
      00A8D3 70 04            [24]  837 	jnz	00102$
                                    838 ;	quantum/vial.c:115: return 0;
      00A8D5 90 00 00         [24]  839 	mov	dptr,#0x0000
      00A8D8 22               [24]  840 	ret
      00A8D9                        841 00102$:
                                    842 ;	quantum/vial.c:116: return in;
      00A8D9 8E 82            [24]  843 	mov	dpl, r6
      00A8DB 8F 83            [24]  844 	mov	dph, r7
                                    845 ;	quantum/vial.c:117: }
      00A8DD 22               [24]  846 	ret
                                    847 ;------------------------------------------------------------
                                    848 ;Allocation info for local variables in function 'vial_fill_packet'
                                    849 ;------------------------------------------------------------
                                    850 ;value         Allocated with name '_vial_fill_packet_PARM_2'
                                    851 ;msg           Allocated with name '_vial_fill_packet_msg_10000_584'
                                    852 ;i             Allocated with name '_vial_fill_packet_i_20000_586'
                                    853 ;------------------------------------------------------------
                                    854 ;	quantum/vial.c:120: static void vial_fill_packet(uint8_t __xdata *msg, uint8_t value) {
                                    855 ;	-----------------------------------------
                                    856 ;	 function vial_fill_packet
                                    857 ;	-----------------------------------------
      00A8DE                        858 _vial_fill_packet:
      00A8DE AF 83            [24]  859 	mov	r7,dph
      00A8E0 E5 82            [12]  860 	mov	a,dpl
      00A8E2 90 0A 60         [24]  861 	mov	dptr,#_vial_fill_packet_msg_10000_584
      00A8E5 F0               [24]  862 	movx	@dptr,a
      00A8E6 EF               [12]  863 	mov	a,r7
      00A8E7 A3               [24]  864 	inc	dptr
      00A8E8 F0               [24]  865 	movx	@dptr,a
                                    866 ;	quantum/vial.c:121: for (uint8_t i = 0; i < VIAL_RAW_EPSIZE; ++i) msg[i] = value;
      00A8E9 90 0A 60         [24]  867 	mov	dptr,#_vial_fill_packet_msg_10000_584
      00A8EC E0               [24]  868 	movx	a,@dptr
      00A8ED FE               [12]  869 	mov	r6,a
      00A8EE A3               [24]  870 	inc	dptr
      00A8EF E0               [24]  871 	movx	a,@dptr
      00A8F0 FF               [12]  872 	mov	r7,a
      00A8F1 90 0A 5F         [24]  873 	mov	dptr,#_vial_fill_packet_PARM_2
      00A8F4 E0               [24]  874 	movx	a,@dptr
      00A8F5 FD               [12]  875 	mov	r5,a
      00A8F6 7C 00            [12]  876 	mov	r4,#0x00
      00A8F8                        877 00103$:
      00A8F8 BC 20 00         [24]  878 	cjne	r4,#0x20,00122$
      00A8FB                        879 00122$:
      00A8FB 50 0D            [24]  880 	jnc	00105$
      00A8FD EC               [12]  881 	mov	a,r4
      00A8FE 2E               [12]  882 	add	a, r6
      00A8FF F5 82            [12]  883 	mov	dpl,a
      00A901 E4               [12]  884 	clr	a
      00A902 3F               [12]  885 	addc	a, r7
      00A903 F5 83            [12]  886 	mov	dph,a
      00A905 ED               [12]  887 	mov	a,r5
      00A906 F0               [24]  888 	movx	@dptr,a
      00A907 0C               [12]  889 	inc	r4
      00A908 80 EE            [24]  890 	sjmp	00103$
      00A90A                        891 00105$:
                                    892 ;	quantum/vial.c:122: }
      00A90A 22               [24]  893 	ret
                                    894 ;------------------------------------------------------------
                                    895 ;Allocation info for local variables in function 'vial_release_held_state'
                                    896 ;------------------------------------------------------------
                                    897 ;key           Allocated with name '_vial_release_held_state_key_10000_588'
                                    898 ;keycode       Allocated with name '_vial_release_held_state_keycode_70000_594'
                                    899 ;------------------------------------------------------------
                                    900 ;	quantum/vial.c:133: static void vial_release_held_state(void) {
                                    901 ;	-----------------------------------------
                                    902 ;	 function vial_release_held_state
                                    903 ;	-----------------------------------------
      00A90B                        904 _vial_release_held_state:
                                    905 ;	quantum/vial.c:135: for (key.row = 0; key.row < MATRIX_ROWS; ++key.row) {
      00A90B 90 0A 63         [24]  906 	mov	dptr,#(_vial_release_held_state_key_10000_588 + 0x0001)
      00A90E E4               [12]  907 	clr	a
      00A90F F0               [24]  908 	movx	@dptr,a
      00A910                        909 00120$:
      00A910 90 0A 63         [24]  910 	mov	dptr,#(_vial_release_held_state_key_10000_588 + 0x0001)
      00A913 E0               [24]  911 	movx	a,@dptr
      00A914 FF               [12]  912 	mov	r7,a
      00A915 BF 10 00         [24]  913 	cjne	r7,#0x10,00203$
      00A918                        914 00203$:
      00A918 40 03            [24]  915 	jc	00204$
      00A91A 02 AA 1C         [24]  916 	ljmp	00115$
      00A91D                        917 00204$:
                                    918 ;	quantum/vial.c:136: for (key.col = 0; key.col < MATRIX_COLS; ++key.col) {
      00A91D 90 0A 62         [24]  919 	mov	dptr,#_vial_release_held_state_key_10000_588
      00A920 E4               [12]  920 	clr	a
      00A921 F0               [24]  921 	movx	@dptr,a
      00A922                        922 00117$:
      00A922 90 0A 62         [24]  923 	mov	dptr,#_vial_release_held_state_key_10000_588
      00A925 E0               [24]  924 	movx	a,@dptr
      00A926 FF               [12]  925 	mov	r7,a
      00A927 BF 08 00         [24]  926 	cjne	r7,#0x08,00205$
      00A92A                        927 00205$:
      00A92A 40 03            [24]  928 	jc	00206$
      00A92C 02 AA 0E         [24]  929 	ljmp	00121$
      00A92F                        930 00206$:
                                    931 ;	quantum/vial.c:137: if (matrix_is_on(key.row, key.col)) {
      00A92F 90 0A 63         [24]  932 	mov	dptr,#(_vial_release_held_state_key_10000_588 + 0x0001)
      00A932 E0               [24]  933 	movx	a,@dptr
      00A933 FF               [12]  934 	mov	r7,a
      00A934 90 0A 62         [24]  935 	mov	dptr,#_vial_release_held_state_key_10000_588
      00A937 E0               [24]  936 	movx	a,@dptr
      00A938 90 06 80         [24]  937 	mov	dptr,#_matrix_is_on_PARM_2
      00A93B F0               [24]  938 	movx	@dptr,a
      00A93C 8F 82            [24]  939 	mov	dpl, r7
      00A93E 12 53 0F         [24]  940 	lcall	_matrix_is_on
      00A941 E5 82            [12]  941 	mov	a, dpl
      00A943 70 03            [24]  942 	jnz	00207$
      00A945 02 AA 00         [24]  943 	ljmp	00118$
      00A948                        944 00207$:
                                    945 ;	quantum/vial.c:138: uint16_t keycode = read_source_keycode_cache(key);
      00A948 90 0B 90         [24]  946 	mov	dptr,#___memcpy_PARM_2
      00A94B 74 62            [12]  947 	mov	a,#_vial_release_held_state_key_10000_588
      00A94D F0               [24]  948 	movx	@dptr,a
      00A94E 74 0A            [12]  949 	mov	a,#(_vial_release_held_state_key_10000_588 >> 8)
      00A950 A3               [24]  950 	inc	dptr
      00A951 F0               [24]  951 	movx	@dptr,a
      00A952 E4               [12]  952 	clr	a
      00A953 A3               [24]  953 	inc	dptr
      00A954 F0               [24]  954 	movx	@dptr,a
      00A955 90 0B 93         [24]  955 	mov	dptr,#___memcpy_PARM_3
      00A958 74 02            [12]  956 	mov	a,#0x02
      00A95A F0               [24]  957 	movx	@dptr,a
      00A95B E4               [12]  958 	clr	a
      00A95C A3               [24]  959 	inc	dptr
      00A95D F0               [24]  960 	movx	@dptr,a
      00A95E 90 08 85         [24]  961 	mov	dptr,#_read_source_keycode_cache_PARM_1
      00A961 F5 F0            [12]  962 	mov	b,a
      00A963 12 B4 BE         [24]  963 	lcall	___memcpy
      00A966 12 76 19         [24]  964 	lcall	_read_source_keycode_cache
      00A969 AE 82            [24]  965 	mov	r6, dpl
      00A96B AF 83            [24]  966 	mov	r7, dph
                                    967 ;	quantum/vial.c:139: if (keycode >= QK_MOMENTARY && keycode <= QK_MOMENTARY_MAX) {
      00A96D 8E 04            [24]  968 	mov	ar4,r6
      00A96F 8F 05            [24]  969 	mov	ar5,r7
      00A971 C3               [12]  970 	clr	c
      00A972 EC               [12]  971 	mov	a,r4
      00A973 94 20            [12]  972 	subb	a,#0x20
      00A975 ED               [12]  973 	mov	a,r5
      00A976 94 52            [12]  974 	subb	a,#0x52
      00A978 40 14            [24]  975 	jc	00109$
      00A97A 74 3F            [12]  976 	mov	a,#0x3f
      00A97C 9C               [12]  977 	subb	a,r4
      00A97D 74 52            [12]  978 	mov	a,#0x52
      00A97F 9D               [12]  979 	subb	a,r5
      00A980 40 0C            [24]  980 	jc	00109$
                                    981 ;	free result
                                    982 ;	quantum/vial.c:140: layer_off(QK_MOMENTARY_GET_LAYER(keycode));
      00A982 8E 03            [24]  983 	mov	ar3,r6
      00A984 53 03 1F         [24]  984 	anl	ar3,#0x1f
      00A987 8B 82            [24]  985 	mov	dpl, r3
      00A989 12 74 D0         [24]  986 	lcall	_layer_off
      00A98C 80 72            [24]  987 	sjmp	00118$
      00A98E                        988 00109$:
                                    989 ;	quantum/vial.c:141: } else if (keycode >= QK_LAYER_MOD && keycode <= QK_LAYER_MOD_MAX) {
      00A98E 74 B0            [12]  990 	mov	a,#0x100 - 0x50
      00A990 2D               [12]  991 	add	a,r5
      00A991 50 22            [24]  992 	jnc	00105$
      00A993 C3               [12]  993 	clr	c
      00A994 74 FF            [12]  994 	mov	a,#0xff
      00A996 9C               [12]  995 	subb	a,r4
      00A997 74 51            [12]  996 	mov	a,#0x51
      00A999 9D               [12]  997 	subb	a,r5
      00A99A 40 19            [24]  998 	jc	00105$
                                    999 ;	free result
                                   1000 ;	quantum/vial.c:142: layer_off(QK_LAYER_MOD_GET_LAYER(keycode));
      00A99C EF               [12] 1001 	mov	a,r7
      00A99D C4               [12] 1002 	swap	a
      00A99E 03               [12] 1003 	rr	a
      00A99F CE               [12] 1004 	xch	a,r6
      00A9A0 C4               [12] 1005 	swap	a
      00A9A1 03               [12] 1006 	rr	a
      00A9A2 54 07            [12] 1007 	anl	a,#0x07
      00A9A4 6E               [12] 1008 	xrl	a,r6
      00A9A5 CE               [12] 1009 	xch	a,r6
      00A9A6 54 07            [12] 1010 	anl	a,#0x07
      00A9A8 CE               [12] 1011 	xch	a,r6
      00A9A9 6E               [12] 1012 	xrl	a,r6
      00A9AA CE               [12] 1013 	xch	a,r6
      00A9AB 53 06 0F         [24] 1014 	anl	ar6,#0x0f
      00A9AE 8E 82            [24] 1015 	mov	dpl, r6
      00A9B0 12 74 D0         [24] 1016 	lcall	_layer_off
      00A9B3 80 4B            [24] 1017 	sjmp	00118$
      00A9B5                       1018 00105$:
                                   1019 ;	quantum/vial.c:144: } else if (keycode == QK_TRI_LAYER_LOWER || keycode == QK_TRI_LAYER_UPPER) {
      00A9B5 E4               [12] 1020 	clr	a
      00A9B6 BC 77 04         [24] 1021 	cjne	r4,#0x77,00212$
      00A9B9 BD 7C 01         [24] 1022 	cjne	r5,#0x7c,00212$
      00A9BC 04               [12] 1023 	inc	a
      00A9BD                       1024 00212$:
      00A9BD FF               [12] 1025 	mov	r7,a
      00A9BE 70 06            [24] 1026 	jnz	00101$
      00A9C0 BC 78 3D         [24] 1027 	cjne	r4,#0x78,00118$
      00A9C3 BD 7C 3A         [24] 1028 	cjne	r5,#0x7c,00118$
      00A9C6                       1029 00101$:
                                   1030 ;	quantum/vial.c:145: layer_off(keycode == QK_TRI_LAYER_LOWER ? get_tri_layer_lower_layer() : get_tri_layer_upper_layer());
      00A9C6 EF               [12] 1031 	mov	a,r7
      00A9C7 60 07            [24] 1032 	jz	00124$
      00A9C9 12 A0 3B         [24] 1033 	lcall	_get_tri_layer_lower_layer
      00A9CC AF 82            [24] 1034 	mov	r7, dpl
      00A9CE 80 05            [24] 1035 	sjmp	00125$
      00A9D0                       1036 00124$:
      00A9D0 12 A0 42         [24] 1037 	lcall	_get_tri_layer_upper_layer
      00A9D3 AF 82            [24] 1038 	mov	r7, dpl
      00A9D5                       1039 00125$:
      00A9D5 8F 82            [24] 1040 	mov	dpl, r7
      00A9D7 12 74 D0         [24] 1041 	lcall	_layer_off
                                   1042 ;	quantum/vial.c:146: update_tri_layer(get_tri_layer_lower_layer(), get_tri_layer_upper_layer(), get_tri_layer_adjust_layer());
      00A9DA 12 A0 3B         [24] 1043 	lcall	_get_tri_layer_lower_layer
      00A9DD AF 82            [24] 1044 	mov	r7, dpl
      00A9DF C0 07            [24] 1045 	push	ar7
      00A9E1 12 A0 42         [24] 1046 	lcall	_get_tri_layer_upper_layer
      00A9E4 AE 82            [24] 1047 	mov	r6, dpl
      00A9E6 C0 06            [24] 1048 	push	ar6
      00A9E8 12 A0 49         [24] 1049 	lcall	_get_tri_layer_adjust_layer
      00A9EB AD 82            [24] 1050 	mov	r5, dpl
      00A9ED D0 06            [24] 1051 	pop	ar6
      00A9EF D0 07            [24] 1052 	pop	ar7
      00A9F1 90 08 95         [24] 1053 	mov	dptr,#_update_tri_layer_PARM_2
      00A9F4 EE               [12] 1054 	mov	a,r6
      00A9F5 F0               [24] 1055 	movx	@dptr,a
      00A9F6 90 08 96         [24] 1056 	mov	dptr,#_update_tri_layer_PARM_3
      00A9F9 ED               [12] 1057 	mov	a,r5
      00A9FA F0               [24] 1058 	movx	@dptr,a
      00A9FB 8F 82            [24] 1059 	mov	dpl, r7
      00A9FD 12 77 E8         [24] 1060 	lcall	_update_tri_layer
      00AA00                       1061 00118$:
                                   1062 ;	quantum/vial.c:136: for (key.col = 0; key.col < MATRIX_COLS; ++key.col) {
      00AA00 90 0A 62         [24] 1063 	mov	dptr,#_vial_release_held_state_key_10000_588
      00AA03 E0               [24] 1064 	movx	a,@dptr
      00AA04 FF               [12] 1065 	mov	r7,a
      00AA05 0F               [12] 1066 	inc	r7
      00AA06 90 0A 62         [24] 1067 	mov	dptr,#_vial_release_held_state_key_10000_588
      00AA09 EF               [12] 1068 	mov	a,r7
      00AA0A F0               [24] 1069 	movx	@dptr,a
      00AA0B 02 A9 22         [24] 1070 	ljmp	00117$
      00AA0E                       1071 00121$:
                                   1072 ;	quantum/vial.c:135: for (key.row = 0; key.row < MATRIX_ROWS; ++key.row) {
      00AA0E 90 0A 63         [24] 1073 	mov	dptr,#(_vial_release_held_state_key_10000_588 + 0x0001)
      00AA11 E0               [24] 1074 	movx	a,@dptr
      00AA12 FF               [12] 1075 	mov	r7,a
      00AA13 0F               [12] 1076 	inc	r7
      00AA14 90 0A 63         [24] 1077 	mov	dptr,#(_vial_release_held_state_key_10000_588 + 0x0001)
      00AA17 EF               [12] 1078 	mov	a,r7
      00AA18 F0               [24] 1079 	movx	@dptr,a
      00AA19 02 A9 10         [24] 1080 	ljmp	00120$
      00AA1C                       1081 00115$:
                                   1082 ;	quantum/vial.c:153: repeat_key_cancel();
      00AA1C 12 9B DB         [24] 1083 	lcall	_repeat_key_cancel
                                   1084 ;	quantum/vial.c:155: clear_keyboard();
                                   1085 ;	quantum/vial.c:156: }
      00AA1F 02 73 94         [24] 1086 	ljmp	_clear_keyboard
                                   1087 ;------------------------------------------------------------
                                   1088 ;Allocation info for local variables in function 'vial_handle_cmd'
                                   1089 ;------------------------------------------------------------
                                   1090 ;sloc0         Allocated with name '_vial_handle_cmd_sloc0_1_0'
                                   1091 ;sloc1         Allocated with name '_vial_handle_cmd_sloc1_1_0'
                                   1092 ;sloc2         Allocated with name '_vial_handle_cmd_sloc2_1_0'
                                   1093 ;sloc3         Allocated with name '_vial_handle_cmd_sloc3_1_0'
                                   1094 ;length        Allocated with name '_vial_handle_cmd_PARM_2'
                                   1095 ;data          Allocated with name '_vial_handle_cmd_data_10000_601'
                                   1096 ;msg           Allocated with name '_vial_handle_cmd_msg_10000_602'
                                   1097 ;i             Allocated with name '_vial_handle_cmd_i_50000_607'
                                   1098 ;sz            Allocated with name '_vial_handle_cmd_sz_40000_608'
                                   1099 ;page          Allocated with name '_vial_handle_cmd_page_40001_611'
                                   1100 ;start         Allocated with name '_vial_handle_cmd_start_40002_613'
                                   1101 ;remaining     Allocated with name '_vial_handle_cmd_remaining_40002_613'
                                   1102 ;count         Allocated with name '_vial_handle_cmd_count_40002_613'
                                   1103 ;i             Allocated with name '_vial_handle_cmd_i_50002_614'
                                   1104 ;layer         Allocated with name '_vial_handle_cmd_layer_40000_615'
                                   1105 ;idx           Allocated with name '_vial_handle_cmd_idx_40000_615'
                                   1106 ;keycode       Allocated with name '_vial_handle_cmd_keycode_40000_615'
                                   1107 ;i             Allocated with name '_vial_handle_cmd_i_50000_618'
                                   1108 ;------------------------------------------------------------
                                   1109 ;	quantum/vial.c:159: void vial_handle_cmd(uint8_t *data, uint8_t length) {
                                   1110 ;	-----------------------------------------
                                   1111 ;	 function vial_handle_cmd
                                   1112 ;	-----------------------------------------
      00AA22                       1113 _vial_handle_cmd:
      00AA22 AF F0            [24] 1114 	mov	r7,b
      00AA24 AE 83            [24] 1115 	mov	r6,dph
      00AA26 E5 82            [12] 1116 	mov	a,dpl
      00AA28 90 0A 65         [24] 1117 	mov	dptr,#_vial_handle_cmd_data_10000_601
      00AA2B F0               [24] 1118 	movx	@dptr,a
      00AA2C EE               [12] 1119 	mov	a,r6
      00AA2D A3               [24] 1120 	inc	dptr
      00AA2E F0               [24] 1121 	movx	@dptr,a
      00AA2F EF               [12] 1122 	mov	a,r7
      00AA30 A3               [24] 1123 	inc	dptr
      00AA31 F0               [24] 1124 	movx	@dptr,a
                                   1125 ;	quantum/vial.c:163: uint8_t __xdata *msg = (uint8_t __xdata *)data;
      00AA32 90 0A 65         [24] 1126 	mov	dptr,#_vial_handle_cmd_data_10000_601
      00AA35 E0               [24] 1127 	movx	a,@dptr
      00AA36 FE               [12] 1128 	mov	r6,a
      00AA37 A3               [24] 1129 	inc	dptr
      00AA38 E0               [24] 1130 	movx	a,@dptr
      00AA39 FF               [12] 1131 	mov	r7,a
                                   1132 ;	quantum/vial.c:168: if (length != VIAL_RAW_EPSIZE)
      00AA3A 90 0A 64         [24] 1133 	mov	dptr,#_vial_handle_cmd_PARM_2
      00AA3D E0               [24] 1134 	movx	a,@dptr
      00AA3E FD               [12] 1135 	mov	r5,a
      00AA3F BD 20 02         [24] 1136 	cjne	r5,#0x20,00233$
      00AA42 80 01            [24] 1137 	sjmp	00102$
      00AA44                       1138 00233$:
                                   1139 ;	quantum/vial.c:169: return;
      00AA44 22               [24] 1140 	ret
      00AA45                       1141 00102$:
                                   1142 ;	quantum/vial.c:172: switch (msg[1]) {
      00AA45 74 01            [12] 1143 	mov	a,#0x01
      00AA47 2E               [12] 1144 	add	a, r6
      00AA48 FC               [12] 1145 	mov	r4,a
      00AA49 E4               [12] 1146 	clr	a
      00AA4A 3F               [12] 1147 	addc	a, r7
      00AA4B FD               [12] 1148 	mov	r5,a
      00AA4C 8C 82            [24] 1149 	mov	dpl,r4
      00AA4E 8D 83            [24] 1150 	mov	dph,r5
      00AA50 E0               [24] 1151 	movx	a,@dptr
      00AA51 FB               [12] 1152 	mov  r3,a
      00AA52 24 F2            [12] 1153 	add	a,#0xff - 0x0d
      00AA54 50 01            [24] 1154 	jnc	00234$
      00AA56 22               [24] 1155 	ret
      00AA57                       1156 00234$:
                                   1157 ;	free result
      00AA57 EB               [12] 1158 	mov	a,r3
      00AA58 24 0A            [12] 1159 	add	a,#(00235$-3-.)
      00AA5A 83               [24] 1160 	movc	a,@a+pc
      00AA5B F5 82            [12] 1161 	mov	dpl,a
      00AA5D EB               [12] 1162 	mov	a,r3
      00AA5E 24 12            [12] 1163 	add	a,#(00236$-3-.)
      00AA60 83               [24] 1164 	movc	a,@a+pc
      00AA61 F5 83            [12] 1165 	mov	dph,a
      00AA63 E4               [12] 1166 	clr	a
      00AA64 73               [24] 1167 	jmp	@a+dptr
      00AA65                       1168 00235$:
      00AA65 81                    1169 	.db	00103$
      00AA66 DC                    1170 	.db	00105$
      00AA67 FB                    1171 	.db	00106$
      00AA68 8C                    1172 	.db	00112$
      00AA69 1C                    1173 	.db	00113$
      00AA6A 72                    1174 	.db	00114$
      00AA6B F5                    1175 	.db	00116$
      00AA6C 10                    1176 	.db	00119$
      00AA6D 33                    1177 	.db	00120$
      00AA6E 41                    1178 	.db	00121$
      00AA6F 8F                    1179 	.db	00135$
      00AA70 8F                    1180 	.db	00135$
      00AA71 8F                    1181 	.db	00135$
      00AA72 4E                    1182 	.db	00122$
      00AA73                       1183 00236$:
      00AA73 AA                    1184 	.db	00103$>>8
      00AA74 AA                    1185 	.db	00105$>>8
      00AA75 AA                    1186 	.db	00106$>>8
      00AA76 AB                    1187 	.db	00112$>>8
      00AA77 AC                    1188 	.db	00113$>>8
      00AA78 AC                    1189 	.db	00114$>>8
      00AA79 AC                    1190 	.db	00116$>>8
      00AA7A AD                    1191 	.db	00119$>>8
      00AA7B AD                    1192 	.db	00120$>>8
      00AA7C AD                    1193 	.db	00121$>>8
      00AA7D AD                    1194 	.db	00135$>>8
      00AA7E AD                    1195 	.db	00135$>>8
      00AA7F AD                    1196 	.db	00135$>>8
      00AA80 AD                    1197 	.db	00122$>>8
                                   1198 ;	quantum/vial.c:174: case vial_get_keyboard_id: {
      00AA81                       1199 00103$:
                                   1200 ;	quantum/vial.c:177: VIAL_FILL_PACKET(msg, 0, length);
      00AA81 90 0A 5F         [24] 1201 	mov	dptr,#_vial_fill_packet_PARM_2
      00AA84 E4               [12] 1202 	clr	a
      00AA85 F0               [24] 1203 	movx	@dptr,a
      00AA86 8E 82            [24] 1204 	mov	dpl, r6
      00AA88 8F 83            [24] 1205 	mov	dph, r7
      00AA8A C0 07            [24] 1206 	push	ar7
      00AA8C C0 06            [24] 1207 	push	ar6
      00AA8E 12 A8 DE         [24] 1208 	lcall	_vial_fill_packet
      00AA91 D0 06            [24] 1209 	pop	ar6
      00AA93 D0 07            [24] 1210 	pop	ar7
                                   1211 ;	quantum/vial.c:178: msg[0] = VIAL_PROTOCOL_VERSION & 0xFF;
      00AA95 8E 82            [24] 1212 	mov	dpl,r6
      00AA97 8F 83            [24] 1213 	mov	dph,r7
      00AA99 74 06            [12] 1214 	mov	a,#0x06
      00AA9B F0               [24] 1215 	movx	@dptr,a
                                   1216 ;	quantum/vial.c:179: msg[1] = (VIAL_PROTOCOL_VERSION >> 8) & 0xFF;
      00AA9C 8E 82            [24] 1217 	mov	dpl,r6
      00AA9E 8F 83            [24] 1218 	mov	dph,r7
      00AAA0 A3               [24] 1219 	inc	dptr
      00AAA1 E4               [12] 1220 	clr	a
      00AAA2 F0               [24] 1221 	movx	@dptr,a
                                   1222 ;	quantum/vial.c:180: msg[2] = (VIAL_PROTOCOL_VERSION >> 16) & 0xFF;
      00AAA3 8E 82            [24] 1223 	mov	dpl,r6
      00AAA5 8F 83            [24] 1224 	mov	dph,r7
      00AAA7 A3               [24] 1225 	inc	dptr
      00AAA8 A3               [24] 1226 	inc	dptr
      00AAA9 F0               [24] 1227 	movx	@dptr,a
                                   1228 ;	quantum/vial.c:181: msg[3] = (VIAL_PROTOCOL_VERSION >> 24) & 0xFF;
      00AAAA 8E 82            [24] 1229 	mov	dpl,r6
      00AAAC 8F 83            [24] 1230 	mov	dph,r7
      00AAAE A3               [24] 1231 	inc	dptr
      00AAAF A3               [24] 1232 	inc	dptr
      00AAB0 A3               [24] 1233 	inc	dptr
      00AAB1 F0               [24] 1234 	movx	@dptr,a
                                   1235 ;	quantum/vial.c:182: for (uint8_t i = 0; i < 8; ++i) msg[4 + i] = pgm_read_byte(&keyboard_uid[i]);
      00AAB2 FB               [12] 1236 	mov	r3,a
      00AAB3                       1237 00127$:
      00AAB3 BB 08 00         [24] 1238 	cjne	r3,#0x08,00237$
      00AAB6                       1239 00237$:
      00AAB6 50 17            [24] 1240 	jnc	00104$
      00AAB8 8B 02            [24] 1241 	mov	ar2,r3
      00AABA 74 04            [12] 1242 	mov	a,#0x04
      00AABC 2A               [12] 1243 	add	a, r2
      00AABD 2E               [12] 1244 	add	a, r6
      00AABE F9               [12] 1245 	mov	r1,a
      00AABF E4               [12] 1246 	clr	a
      00AAC0 3F               [12] 1247 	addc	a,r7
      00AAC1 FA               [12] 1248 	mov	r2,a
      00AAC2 EB               [12] 1249 	mov	a,r3
      00AAC3 90 BB A9         [24] 1250 	mov	dptr,#_vial_handle_cmd_keyboard_uid_40000_606
      00AAC6 93               [24] 1251 	movc	a,@a+dptr
      00AAC7 89 82            [24] 1252 	mov	dpl,r1
      00AAC9 8A 83            [24] 1253 	mov	dph,r2
      00AACB F0               [24] 1254 	movx	@dptr,a
      00AACC 0B               [12] 1255 	inc	r3
      00AACD 80 E4            [24] 1256 	sjmp	00127$
      00AACF                       1257 00104$:
                                   1258 ;	quantum/vial.c:184: msg[12] = 1; /* bit flag to indicate vialrgb is supported - so third-party apps don't have to query json */
      00AACF 74 0C            [12] 1259 	mov	a,#0x0c
      00AAD1 2E               [12] 1260 	add	a, r6
      00AAD2 F5 82            [12] 1261 	mov	dpl,a
      00AAD4 E4               [12] 1262 	clr	a
      00AAD5 3F               [12] 1263 	addc	a, r7
      00AAD6 F5 83            [12] 1264 	mov	dph,a
      00AAD8 74 01            [12] 1265 	mov	a,#0x01
      00AADA F0               [24] 1266 	movx	@dptr,a
                                   1267 ;	quantum/vial.c:186: break;
      00AADB 22               [24] 1268 	ret
                                   1269 ;	quantum/vial.c:189: case vial_get_size: {
      00AADC                       1270 00105$:
                                   1271 ;	quantum/vial.c:191: msg[0] = sz & 0xFF;
      00AADC 8E 82            [24] 1272 	mov	dpl,r6
      00AADE 8F 83            [24] 1273 	mov	dph,r7
      00AAE0 74 7C            [12] 1274 	mov	a,#0x7c
      00AAE2 F0               [24] 1275 	movx	@dptr,a
                                   1276 ;	quantum/vial.c:192: msg[1] = (sz >> 8) & 0xFF;
      00AAE3 8C 82            [24] 1277 	mov	dpl,r4
      00AAE5 8D 83            [24] 1278 	mov	dph,r5
      00AAE7 74 01            [12] 1279 	mov	a,#0x01
      00AAE9 F0               [24] 1280 	movx	@dptr,a
                                   1281 ;	quantum/vial.c:193: msg[2] = (sz >> 16) & 0xFF;
      00AAEA 8E 82            [24] 1282 	mov	dpl,r6
      00AAEC 8F 83            [24] 1283 	mov	dph,r7
      00AAEE A3               [24] 1284 	inc	dptr
      00AAEF A3               [24] 1285 	inc	dptr
      00AAF0 E4               [12] 1286 	clr	a
      00AAF1 F0               [24] 1287 	movx	@dptr,a
                                   1288 ;	quantum/vial.c:194: msg[3] = (sz >> 24) & 0xFF;
      00AAF2 8E 82            [24] 1289 	mov	dpl,r6
      00AAF4 8F 83            [24] 1290 	mov	dph,r7
      00AAF6 A3               [24] 1291 	inc	dptr
      00AAF7 A3               [24] 1292 	inc	dptr
      00AAF8 A3               [24] 1293 	inc	dptr
      00AAF9 F0               [24] 1294 	movx	@dptr,a
                                   1295 ;	quantum/vial.c:195: break;
      00AAFA 22               [24] 1296 	ret
                                   1297 ;	quantum/vial.c:198: case vial_get_def: {
      00AAFB                       1298 00106$:
                                   1299 ;	quantum/vial.c:205: if (msg[4] | msg[5]) return;
      00AAFB 12 A7 CD         [24] 1300 	lcall	_ak820_outline_0006
      00AAFE E0               [24] 1301 	movx	a,@dptr
      00AAFF FB               [12] 1302 	mov	r3,a
      00AB00 12 A7 CD         [24] 1303 	lcall	_ak820_outline_0006
      00AB03 A3               [24] 1304 	inc	dptr
      00AB04 E0               [24] 1305 	movx	a,@dptr
      00AB05 4B               [12] 1306 	orl	a,r3
      00AB06 60 01            [24] 1307 	jz	00108$
      00AB08 22               [24] 1308 	ret
      00AB09                       1309 00108$:
                                   1310 ;	quantum/vial.c:206: uint16_t page = (uint16_t)msg[2] | ((uint16_t)msg[3] << 8);
      00AB09 8E 82            [24] 1311 	mov	dpl,r6
      00AB0B 8F 83            [24] 1312 	mov	dph,r7
      00AB0D A3               [24] 1313 	inc	dptr
      00AB0E A3               [24] 1314 	inc	dptr
      00AB0F E0               [24] 1315 	movx	a,@dptr
      00AB10 FB               [12] 1316 	mov	r3,a
      00AB11 7A 00            [12] 1317 	mov	r2,#0x00
      00AB13 12 A7 D6         [24] 1318 	lcall	_ak820_outline_0010
      00AB16 F9               [12] 1319 	mov	r1,a
      00AB17 E4               [12] 1320 	clr	a
      00AB18 42 03            [12] 1321 	orl	ar3,a
      00AB1A E9               [12] 1322 	mov	a,r1
      00AB1B 42 02            [12] 1323 	orl	ar2,a
                                   1324 ;	quantum/vial.c:207: if (page >= (sizeof(keyboard_definition) + VIAL_RAW_EPSIZE - 1) / VIAL_RAW_EPSIZE) return;
      00AB1D C3               [12] 1325 	clr	c
      00AB1E EB               [12] 1326 	mov	a,r3
      00AB1F 94 0C            [12] 1327 	subb	a,#0x0c
      00AB21 EA               [12] 1328 	mov	a,r2
      00AB22 94 00            [12] 1329 	subb	a,#0x00
      00AB24 40 01            [24] 1330 	jc	00110$
      00AB26 22               [24] 1331 	ret
      00AB27                       1332 00110$:
                                   1333 ;	quantum/vial.c:208: uint16_t start = page * VIAL_RAW_EPSIZE;
      00AB27 EA               [12] 1334 	mov	a,r2
      00AB28 C4               [12] 1335 	swap	a
      00AB29 23               [12] 1336 	rl	a
      00AB2A 54 E0            [12] 1337 	anl	a,#0xe0
      00AB2C CB               [12] 1338 	xch	a,r3
      00AB2D C4               [12] 1339 	swap	a
      00AB2E 23               [12] 1340 	rl	a
      00AB2F CB               [12] 1341 	xch	a,r3
      00AB30 6B               [12] 1342 	xrl	a,r3
      00AB31 CB               [12] 1343 	xch	a,r3
      00AB32 54 E0            [12] 1344 	anl	a,#0xe0
      00AB34 CB               [12] 1345 	xch	a,r3
      00AB35 6B               [12] 1346 	xrl	a,r3
      00AB36 FA               [12] 1347 	mov	r2,a
      00AB37 8B 4B            [24] 1348 	mov	_vial_handle_cmd_sloc0_1_0,r3
      00AB39 8A 4C            [24] 1349 	mov	(_vial_handle_cmd_sloc0_1_0 + 1),r2
                                   1350 ;	quantum/vial.c:209: uint16_t remaining = sizeof(keyboard_definition) - start;
      00AB3B 74 7C            [12] 1351 	mov	a,#0x7c
      00AB3D C3               [12] 1352 	clr	c
      00AB3E 95 4B            [12] 1353 	subb	a,_vial_handle_cmd_sloc0_1_0
      00AB40 F8               [12] 1354 	mov	r0,a
      00AB41 74 01            [12] 1355 	mov	a,#0x01
      00AB43 95 4C            [12] 1356 	subb	a,(_vial_handle_cmd_sloc0_1_0 + 1)
      00AB45 F9               [12] 1357 	mov	r1,a
                                   1358 ;	quantum/vial.c:210: uint8_t count = remaining < VIAL_RAW_EPSIZE ? remaining : VIAL_RAW_EPSIZE;
      00AB46 C3               [12] 1359 	clr	c
      00AB47 E8               [12] 1360 	mov	a,r0
      00AB48 94 20            [12] 1361 	subb	a,#0x20
      00AB4A E9               [12] 1362 	mov	a,r1
      00AB4B 94 00            [12] 1363 	subb	a,#0x00
      00AB4D 40 02            [24] 1364 	jc	00138$
      00AB4F 78 20            [12] 1365 	mov	r0,#0x20
      00AB51                       1366 00138$:
                                   1367 ;	quantum/vial.c:211: for (uint8_t i = 0; i < count; ++i) msg[i] = pgm_read_byte(&keyboard_definition[start + i]);
      00AB51 79 00            [12] 1368 	mov	r1,#0x00
      00AB53                       1369 00130$:
      00AB53 C3               [12] 1370 	clr	c
      00AB54 E9               [12] 1371 	mov	a,r1
      00AB55 98               [12] 1372 	subb	a,r0
      00AB56 40 01            [24] 1373 	jc	00242$
      00AB58 22               [24] 1374 	ret
      00AB59                       1375 00242$:
      00AB59 C0 00            [24] 1376 	push	ar0
      00AB5B E9               [12] 1377 	mov	a,r1
      00AB5C 2E               [12] 1378 	add	a, r6
      00AB5D F5 4D            [12] 1379 	mov	_vial_handle_cmd_sloc1_1_0,a
      00AB5F E4               [12] 1380 	clr	a
      00AB60 3F               [12] 1381 	addc	a, r7
      00AB61 F5 4E            [12] 1382 	mov	(_vial_handle_cmd_sloc1_1_0 + 1),a
      00AB63 89 4F            [24] 1383 	mov	_vial_handle_cmd_sloc2_1_0,r1
      00AB65 75 50 00         [24] 1384 	mov	(_vial_handle_cmd_sloc2_1_0 + 1),#0x00
      00AB68 A8 4B            [24] 1385 	mov	r0,_vial_handle_cmd_sloc0_1_0
      00AB6A AB 4C            [24] 1386 	mov	r3,(_vial_handle_cmd_sloc0_1_0 + 1)
      00AB6C E5 4F            [12] 1387 	mov	a,_vial_handle_cmd_sloc2_1_0
      00AB6E 28               [12] 1388 	add	a, r0
      00AB6F F8               [12] 1389 	mov	r0,a
      00AB70 E5 50            [12] 1390 	mov	a,(_vial_handle_cmd_sloc2_1_0 + 1)
      00AB72 3B               [12] 1391 	addc	a, r3
      00AB73 FB               [12] 1392 	mov	r3,a
      00AB74 E8               [12] 1393 	mov	a,r0
      00AB75 24 2D            [12] 1394 	add	a, #_keyboard_definition
      00AB77 F5 82            [12] 1395 	mov	dpl,a
      00AB79 EB               [12] 1396 	mov	a,r3
      00AB7A 34 BA            [12] 1397 	addc	a, #(_keyboard_definition >> 8)
      00AB7C F5 83            [12] 1398 	mov	dph,a
      00AB7E E4               [12] 1399 	clr	a
      00AB7F 93               [24] 1400 	movc	a,@a+dptr
      00AB80 85 4D 82         [24] 1401 	mov	dpl,_vial_handle_cmd_sloc1_1_0
      00AB83 85 4E 83         [24] 1402 	mov	dph,(_vial_handle_cmd_sloc1_1_0 + 1)
      00AB86 F0               [24] 1403 	movx	@dptr,a
      00AB87 09               [12] 1404 	inc	r1
      00AB88 D0 00            [24] 1405 	pop	ar0
                                   1406 ;	quantum/vial.c:225: case vial_get_encoder: {
      00AB8A 80 C7            [24] 1407 	sjmp	00130$
      00AB8C                       1408 00112$:
                                   1409 ;	quantum/vial.c:226: uint8_t layer = msg[2];
      00AB8C 74 02            [12] 1410 	mov	a,#0x02
      00AB8E 2E               [12] 1411 	add	a, r6
      00AB8F FA               [12] 1412 	mov	r2,a
      00AB90 E4               [12] 1413 	clr	a
      00AB91 3F               [12] 1414 	addc	a, r7
      00AB92 FB               [12] 1415 	mov	r3,a
      00AB93 8A 82            [24] 1416 	mov	dpl,r2
      00AB95 8B 83            [24] 1417 	mov	dph,r3
      00AB97 E0               [24] 1418 	movx	a,@dptr
      00AB98 F5 4F            [12] 1419 	mov	_vial_handle_cmd_sloc2_1_0,a
                                   1420 ;	quantum/vial.c:227: uint8_t idx = msg[3];
      00AB9A 74 03            [12] 1421 	mov	a,#0x03
      00AB9C 2E               [12] 1422 	add	a, r6
      00AB9D F5 4D            [12] 1423 	mov	_vial_handle_cmd_sloc1_1_0,a
      00AB9F E4               [12] 1424 	clr	a
      00ABA0 3F               [12] 1425 	addc	a, r7
      00ABA1 F5 4E            [12] 1426 	mov	(_vial_handle_cmd_sloc1_1_0 + 1),a
      00ABA3 85 4D 82         [24] 1427 	mov	dpl,_vial_handle_cmd_sloc1_1_0
      00ABA6 85 4E 83         [24] 1428 	mov	dph,(_vial_handle_cmd_sloc1_1_0 + 1)
      00ABA9 E0               [24] 1429 	movx	a,@dptr
                                   1430 ;	quantum/vial.c:228: uint16_t keycode = dynamic_keymap_get_encoder(layer, idx, 0);
      00ABAA F5 4B            [12] 1431 	mov	_vial_handle_cmd_sloc0_1_0,a
      00ABAC 90 08 E4         [24] 1432 	mov	dptr,#_dynamic_keymap_get_encoder_PARM_2
      00ABAF F0               [24] 1433 	movx	@dptr,a
      00ABB0 90 08 E5         [24] 1434 	mov	dptr,#_dynamic_keymap_get_encoder_PARM_3
      00ABB3 E4               [12] 1435 	clr	a
      00ABB4 F0               [24] 1436 	movx	@dptr,a
      00ABB5 85 4F 82         [24] 1437 	mov	dpl, _vial_handle_cmd_sloc2_1_0
      00ABB8 C0 07            [24] 1438 	push	ar7
      00ABBA C0 06            [24] 1439 	push	ar6
      00ABBC C0 05            [24] 1440 	push	ar5
      00ABBE C0 04            [24] 1441 	push	ar4
      00ABC0 C0 03            [24] 1442 	push	ar3
      00ABC2 C0 02            [24] 1443 	push	ar2
      00ABC4 12 7C CA         [24] 1444 	lcall	_dynamic_keymap_get_encoder
      00ABC7 85 82 51         [24] 1445 	mov	_vial_handle_cmd_sloc3_1_0,dpl
      00ABCA 85 83 52         [24] 1446 	mov	(_vial_handle_cmd_sloc3_1_0 + 1),dph
      00ABCD D0 02            [24] 1447 	pop	ar2
      00ABCF D0 03            [24] 1448 	pop	ar3
      00ABD1 D0 04            [24] 1449 	pop	ar4
      00ABD3 D0 05            [24] 1450 	pop	ar5
      00ABD5 D0 06            [24] 1451 	pop	ar6
      00ABD7 D0 07            [24] 1452 	pop	ar7
                                   1453 ;	quantum/vial.c:229: msg[0]  = keycode >> 8;
      00ABD9 A9 52            [24] 1454 	mov	r1,(_vial_handle_cmd_sloc3_1_0 + 1)
      00ABDB 8E 82            [24] 1455 	mov	dpl,r6
      00ABDD 8F 83            [24] 1456 	mov	dph,r7
      00ABDF E9               [12] 1457 	mov	a,r1
      00ABE0 F0               [24] 1458 	movx	@dptr,a
                                   1459 ;	quantum/vial.c:230: msg[1]  = keycode & 0xFF;
      00ABE1 A8 51            [24] 1460 	mov	r0,_vial_handle_cmd_sloc3_1_0
      00ABE3 8C 82            [24] 1461 	mov	dpl,r4
      00ABE5 8D 83            [24] 1462 	mov	dph,r5
      00ABE7 E8               [12] 1463 	mov	a,r0
      00ABE8 F0               [24] 1464 	movx	@dptr,a
                                   1465 ;	quantum/vial.c:231: keycode = dynamic_keymap_get_encoder(layer, idx, 1);
      00ABE9 90 08 E4         [24] 1466 	mov	dptr,#_dynamic_keymap_get_encoder_PARM_2
      00ABEC E5 4B            [12] 1467 	mov	a,_vial_handle_cmd_sloc0_1_0
      00ABEE F0               [24] 1468 	movx	@dptr,a
      00ABEF 90 08 E5         [24] 1469 	mov	dptr,#_dynamic_keymap_get_encoder_PARM_3
      00ABF2 74 01            [12] 1470 	mov	a,#0x01
      00ABF4 F0               [24] 1471 	movx	@dptr,a
      00ABF5 85 4F 82         [24] 1472 	mov	dpl, _vial_handle_cmd_sloc2_1_0
      00ABF8 C0 03            [24] 1473 	push	ar3
      00ABFA C0 02            [24] 1474 	push	ar2
      00ABFC 12 7C CA         [24] 1475 	lcall	_dynamic_keymap_get_encoder
      00ABFF 85 82 51         [24] 1476 	mov	_vial_handle_cmd_sloc3_1_0,dpl
      00AC02 85 83 52         [24] 1477 	mov	(_vial_handle_cmd_sloc3_1_0 + 1),dph
      00AC05 D0 02            [24] 1478 	pop	ar2
      00AC07 D0 03            [24] 1479 	pop	ar3
                                   1480 ;	quantum/vial.c:232: msg[2] = keycode >> 8;
      00AC09 A9 52            [24] 1481 	mov	r1,(_vial_handle_cmd_sloc3_1_0 + 1)
      00AC0B 8A 82            [24] 1482 	mov	dpl,r2
      00AC0D 8B 83            [24] 1483 	mov	dph,r3
      00AC0F E9               [12] 1484 	mov	a,r1
      00AC10 F0               [24] 1485 	movx	@dptr,a
                                   1486 ;	quantum/vial.c:233: msg[3] = keycode & 0xFF;
      00AC11 A8 51            [24] 1487 	mov	r0,_vial_handle_cmd_sloc3_1_0
      00AC13 85 4D 82         [24] 1488 	mov	dpl,_vial_handle_cmd_sloc1_1_0
      00AC16 85 4E 83         [24] 1489 	mov	dph,(_vial_handle_cmd_sloc1_1_0 + 1)
      00AC19 E8               [12] 1490 	mov	a,r0
      00AC1A F0               [24] 1491 	movx	@dptr,a
                                   1492 ;	quantum/vial.c:234: break;
      00AC1B 22               [24] 1493 	ret
                                   1494 ;	quantum/vial.c:236: case vial_set_encoder: {
      00AC1C                       1495 00113$:
                                   1496 ;	quantum/vial.c:237: dynamic_keymap_set_encoder(msg[2], msg[3], msg[4], vial_keycode_firewall((msg[5] << 8) | msg[6]));
      00AC1C 8E 82            [24] 1497 	mov	dpl,r6
      00AC1E 8F 83            [24] 1498 	mov	dph,r7
      00AC20 A3               [24] 1499 	inc	dptr
      00AC21 A3               [24] 1500 	inc	dptr
      00AC22 E0               [24] 1501 	movx	a,@dptr
      00AC23 F5 4D            [12] 1502 	mov	_vial_handle_cmd_sloc1_1_0,a
      00AC25 12 A7 D6         [24] 1503 	lcall	_ak820_outline_0010
      00AC28 F5 4F            [12] 1504 	mov	_vial_handle_cmd_sloc2_1_0,a
      00AC2A 12 A7 CD         [24] 1505 	lcall	_ak820_outline_0006
      00AC2D E0               [24] 1506 	movx	a,@dptr
                                   1507 ;	assignBit
      00AC2E 24 FF            [12] 1508 	add	a,#0xff
      00AC30 E4               [12] 1509 	clr	a
      00AC31 33               [12] 1510 	rlc	a
      00AC32 F5 51            [12] 1511 	mov	_vial_handle_cmd_sloc3_1_0,a
      00AC34 12 A7 CD         [24] 1512 	lcall	_ak820_outline_0006
      00AC37 A3               [24] 1513 	inc	dptr
      00AC38 E0               [24] 1514 	movx	a,@dptr
      00AC39 F9               [12] 1515 	mov	r1,a
      00AC3A 78 00            [12] 1516 	mov	r0,#0x00
      00AC3C 74 06            [12] 1517 	mov	a,#0x06
      00AC3E 2E               [12] 1518 	add	a, r6
      00AC3F F5 82            [12] 1519 	mov	dpl,a
      00AC41 E4               [12] 1520 	clr	a
      00AC42 3F               [12] 1521 	addc	a, r7
      00AC43 F5 83            [12] 1522 	mov	dph,a
      00AC45 E0               [24] 1523 	movx	a,@dptr
      00AC46 7B 00            [12] 1524 	mov	r3,#0x00
      00AC48 42 00            [12] 1525 	orl	ar0,a
      00AC4A EB               [12] 1526 	mov	a,r3
      00AC4B 42 01            [12] 1527 	orl	ar1,a
      00AC4D 88 82            [24] 1528 	mov	dpl, r0
      00AC4F 89 83            [24] 1529 	mov	dph, r1
      00AC51 12 A8 B8         [24] 1530 	lcall	_vial_keycode_firewall
      00AC54 AA 82            [24] 1531 	mov	r2, dpl
      00AC56 AB 83            [24] 1532 	mov	r3, dph
      00AC58 90 08 E7         [24] 1533 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_2
      00AC5B E5 4F            [12] 1534 	mov	a,_vial_handle_cmd_sloc2_1_0
      00AC5D F0               [24] 1535 	movx	@dptr,a
      00AC5E 90 08 E8         [24] 1536 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_3
      00AC61 E5 51            [12] 1537 	mov	a,_vial_handle_cmd_sloc3_1_0
      00AC63 F0               [24] 1538 	movx	@dptr,a
      00AC64 90 08 E9         [24] 1539 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_4
      00AC67 EA               [12] 1540 	mov	a,r2
      00AC68 F0               [24] 1541 	movx	@dptr,a
      00AC69 EB               [12] 1542 	mov	a,r3
      00AC6A A3               [24] 1543 	inc	dptr
      00AC6B F0               [24] 1544 	movx	@dptr,a
      00AC6C 85 4D 82         [24] 1545 	mov	dpl, _vial_handle_cmd_sloc1_1_0
                                   1546 ;	quantum/vial.c:238: break;
      00AC6F 02 7D 44         [24] 1547 	ljmp	_dynamic_keymap_set_encoder
                                   1548 ;	quantum/vial.c:241: case vial_get_unlock_status: {
      00AC72                       1549 00114$:
                                   1550 ;	quantum/vial.c:243: VIAL_FILL_PACKET(msg, 0xFF, length);
      00AC72 90 0A 5F         [24] 1551 	mov	dptr,#_vial_fill_packet_PARM_2
      00AC75 74 FF            [12] 1552 	mov	a,#0xff
      00AC77 F0               [24] 1553 	movx	@dptr,a
      00AC78 8E 82            [24] 1554 	mov	dpl, r6
      00AC7A 8F 83            [24] 1555 	mov	dph, r7
      00AC7C C0 07            [24] 1556 	push	ar7
      00AC7E C0 06            [24] 1557 	push	ar6
      00AC80 12 A8 DE         [24] 1558 	lcall	_vial_fill_packet
      00AC83 D0 06            [24] 1559 	pop	ar6
      00AC85 D0 07            [24] 1560 	pop	ar7
                                   1561 ;	quantum/vial.c:245: msg[0] = vial_unlocked;
      00AC87 90 0C 08         [24] 1562 	mov	dptr,#_vial_unlocked
      00AC8A E0               [24] 1563 	movx	a,@dptr
      00AC8B 8E 82            [24] 1564 	mov	dpl,r6
      00AC8D 8F 83            [24] 1565 	mov	dph,r7
      00AC8F F0               [24] 1566 	movx	@dptr,a
                                   1567 ;	quantum/vial.c:247: msg[1] = vial_unlock_in_progress;
      00AC90 74 01            [12] 1568 	mov	a,#0x01
      00AC92 2E               [12] 1569 	add	a, r6
      00AC93 FA               [12] 1570 	mov	r2,a
      00AC94 E4               [12] 1571 	clr	a
      00AC95 3F               [12] 1572 	addc	a, r7
      00AC96 FB               [12] 1573 	mov	r3,a
      00AC97 90 0C 09         [24] 1574 	mov	dptr,#_vial_unlock_in_progress
      00AC9A E0               [24] 1575 	movx	a,@dptr
      00AC9B 8A 82            [24] 1576 	mov	dpl,r2
      00AC9D 8B 83            [24] 1577 	mov	dph,r3
      00AC9F F0               [24] 1578 	movx	@dptr,a
                                   1579 ;	quantum/vial.c:250: for (uint8_t i = 0; i < VIAL_UNLOCK_NUM_KEYS; ++i) {
      00ACA0 7B 00            [12] 1580 	mov	r3,#0x00
      00ACA2                       1581 00133$:
      00ACA2 BB 02 00         [24] 1582 	cjne	r3,#0x02,00243$
      00ACA5                       1583 00243$:
      00ACA5 40 01            [24] 1584 	jc	00244$
      00ACA7 22               [24] 1585 	ret
      00ACA8                       1586 00244$:
                                   1587 ;	quantum/vial.c:251: msg[2 + i * 2] = vial_unlock_combo_rows[i];
      00ACA8 8B 01            [24] 1588 	mov	ar1,r3
      00ACAA 7A 00            [12] 1589 	mov	r2,#0x00
      00ACAC E9               [12] 1590 	mov	a,r1
      00ACAD 29               [12] 1591 	add	a,r1
      00ACAE F5 51            [12] 1592 	mov	_vial_handle_cmd_sloc3_1_0,a
      00ACB0 EA               [12] 1593 	mov	a,r2
      00ACB1 33               [12] 1594 	rlc	a
      00ACB2 F5 52            [12] 1595 	mov	(_vial_handle_cmd_sloc3_1_0 + 1),a
      00ACB4 74 02            [12] 1596 	mov	a,#0x02
      00ACB6 25 51            [12] 1597 	add	a, _vial_handle_cmd_sloc3_1_0
      00ACB8 F8               [12] 1598 	mov	r0,a
      00ACB9 E4               [12] 1599 	clr	a
      00ACBA 35 52            [12] 1600 	addc	a, (_vial_handle_cmd_sloc3_1_0 + 1)
      00ACBC FA               [12] 1601 	mov	r2,a
      00ACBD E8               [12] 1602 	mov	a,r0
      00ACBE 2E               [12] 1603 	add	a, r6
      00ACBF F8               [12] 1604 	mov	r0,a
      00ACC0 EA               [12] 1605 	mov	a,r2
      00ACC1 3F               [12] 1606 	addc	a, r7
      00ACC2 FA               [12] 1607 	mov	r2,a
      00ACC3 EB               [12] 1608 	mov	a,r3
      00ACC4 24 0B            [12] 1609 	add	a, #_vial_unlock_combo_rows
      00ACC6 F5 82            [12] 1610 	mov	dpl,a
      00ACC8 E4               [12] 1611 	clr	a
      00ACC9 34 0C            [12] 1612 	addc	a, #(_vial_unlock_combo_rows >> 8)
      00ACCB F5 83            [12] 1613 	mov	dph,a
      00ACCD E0               [24] 1614 	movx	a,@dptr
      00ACCE 88 82            [24] 1615 	mov	dpl,r0
      00ACD0 8A 83            [24] 1616 	mov	dph,r2
      00ACD2 F0               [24] 1617 	movx	@dptr,a
                                   1618 ;	quantum/vial.c:252: msg[2 + i * 2 + 1] = vial_unlock_combo_cols[i];
      00ACD3 74 03            [12] 1619 	mov	a,#0x03
      00ACD5 25 51            [12] 1620 	add	a, _vial_handle_cmd_sloc3_1_0
      00ACD7 F9               [12] 1621 	mov	r1,a
      00ACD8 E4               [12] 1622 	clr	a
      00ACD9 35 52            [12] 1623 	addc	a, (_vial_handle_cmd_sloc3_1_0 + 1)
      00ACDB FA               [12] 1624 	mov	r2,a
      00ACDC E9               [12] 1625 	mov	a,r1
      00ACDD 2E               [12] 1626 	add	a, r6
      00ACDE F9               [12] 1627 	mov	r1,a
      00ACDF EA               [12] 1628 	mov	a,r2
      00ACE0 3F               [12] 1629 	addc	a, r7
      00ACE1 FA               [12] 1630 	mov	r2,a
      00ACE2 EB               [12] 1631 	mov	a,r3
      00ACE3 24 0D            [12] 1632 	add	a, #_vial_unlock_combo_cols
      00ACE5 F5 82            [12] 1633 	mov	dpl,a
      00ACE7 E4               [12] 1634 	clr	a
      00ACE8 34 0C            [12] 1635 	addc	a, #(_vial_unlock_combo_cols >> 8)
      00ACEA F5 83            [12] 1636 	mov	dph,a
      00ACEC E0               [24] 1637 	movx	a,@dptr
      00ACED 89 82            [24] 1638 	mov	dpl,r1
      00ACEF 8A 83            [24] 1639 	mov	dph,r2
      00ACF1 F0               [24] 1640 	movx	@dptr,a
                                   1641 ;	quantum/vial.c:250: for (uint8_t i = 0; i < VIAL_UNLOCK_NUM_KEYS; ++i) {
      00ACF2 0B               [12] 1642 	inc	r3
                                   1643 ;	quantum/vial.c:257: case vial_unlock_start: {
      00ACF3 80 AD            [24] 1644 	sjmp	00133$
      00ACF5                       1645 00116$:
                                   1646 ;	quantum/vial.c:259: if (!vial_unlock_in_progress) vial_release_held_state();
      00ACF5 90 0C 09         [24] 1647 	mov	dptr,#_vial_unlock_in_progress
      00ACF8 E0               [24] 1648 	movx	a,@dptr
      00ACF9 70 03            [24] 1649 	jnz	00118$
      00ACFB 12 A9 0B         [24] 1650 	lcall	_vial_release_held_state
      00ACFE                       1651 00118$:
                                   1652 ;	quantum/vial.c:261: vial_unlock_in_progress = 1;
      00ACFE 90 0C 09         [24] 1653 	mov	dptr,#_vial_unlock_in_progress
      00AD01 74 01            [12] 1654 	mov	a,#0x01
      00AD03 F0               [24] 1655 	movx	@dptr,a
                                   1656 ;	quantum/vial.c:262: vial_unlock_counter = VIAL_UNLOCK_COUNTER_MAX;
      00AD04 90 0C 0A         [24] 1657 	mov	dptr,#_vial_unlock_counter
      00AD07 74 1E            [12] 1658 	mov	a,#0x1e
      00AD09 F0               [24] 1659 	movx	@dptr,a
                                   1660 ;	quantum/vial.c:264: vial_unlock_holding = false;
      00AD0A 90 0A 5C         [24] 1661 	mov	dptr,#_vial_unlock_holding
      00AD0D E4               [12] 1662 	clr	a
      00AD0E F0               [24] 1663 	movx	@dptr,a
                                   1664 ;	quantum/vial.c:266: break;
      00AD0F 22               [24] 1665 	ret
                                   1666 ;	quantum/vial.c:268: case vial_unlock_poll: {
      00AD10                       1667 00119$:
                                   1668 ;	quantum/vial.c:269: msg[0] = vial_unlocked;
      00AD10 90 0C 08         [24] 1669 	mov	dptr,#_vial_unlocked
      00AD13 E0               [24] 1670 	movx	a,@dptr
      00AD14 8E 82            [24] 1671 	mov	dpl,r6
      00AD16 8F 83            [24] 1672 	mov	dph,r7
      00AD18 F0               [24] 1673 	movx	@dptr,a
                                   1674 ;	quantum/vial.c:270: msg[1] = vial_unlock_in_progress;
      00AD19 90 0C 09         [24] 1675 	mov	dptr,#_vial_unlock_in_progress
      00AD1C E0               [24] 1676 	movx	a,@dptr
      00AD1D 8C 82            [24] 1677 	mov	dpl,r4
      00AD1F 8D 83            [24] 1678 	mov	dph,r5
      00AD21 F0               [24] 1679 	movx	@dptr,a
                                   1680 ;	quantum/vial.c:271: msg[2] = vial_unlock_counter;
      00AD22 74 02            [12] 1681 	mov	a,#0x02
      00AD24 2E               [12] 1682 	add	a, r6
      00AD25 FC               [12] 1683 	mov	r4,a
      00AD26 E4               [12] 1684 	clr	a
      00AD27 3F               [12] 1685 	addc	a, r7
      00AD28 FD               [12] 1686 	mov	r5,a
      00AD29 90 0C 0A         [24] 1687 	mov	dptr,#_vial_unlock_counter
      00AD2C E0               [24] 1688 	movx	a,@dptr
      00AD2D 8C 82            [24] 1689 	mov	dpl,r4
      00AD2F 8D 83            [24] 1690 	mov	dph,r5
      00AD31 F0               [24] 1691 	movx	@dptr,a
                                   1692 ;	quantum/vial.c:272: break;
                                   1693 ;	quantum/vial.c:274: case vial_lock: {
      00AD32 22               [24] 1694 	ret
      00AD33                       1695 00120$:
                                   1696 ;	quantum/vial.c:276: vial_unlocked = 0;
      00AD33 90 0C 08         [24] 1697 	mov	dptr,#_vial_unlocked
      00AD36 E4               [12] 1698 	clr	a
      00AD37 F0               [24] 1699 	movx	@dptr,a
                                   1700 ;	quantum/vial.c:277: vial_unlock_in_progress = 0;
      00AD38 90 0C 09         [24] 1701 	mov	dptr,#_vial_unlock_in_progress
      00AD3B F0               [24] 1702 	movx	@dptr,a
                                   1703 ;	quantum/vial.c:278: vial_unlock_holding = false;
      00AD3C 90 0A 5C         [24] 1704 	mov	dptr,#_vial_unlock_holding
      00AD3F F0               [24] 1705 	movx	@dptr,a
                                   1706 ;	quantum/vial.c:280: break;
                                   1707 ;	quantum/vial.c:282: case vial_qmk_settings_query: {
      00AD40 22               [24] 1708 	ret
      00AD41                       1709 00121$:
                                   1710 ;	quantum/vial.c:287: VIAL_FILL_PACKET(msg, 0xFF, length); /* indicate that we don't support any qsid */
      00AD41 90 0A 5F         [24] 1711 	mov	dptr,#_vial_fill_packet_PARM_2
      00AD44 74 FF            [12] 1712 	mov	a,#0xff
      00AD46 F0               [24] 1713 	movx	@dptr,a
      00AD47 8E 82            [24] 1714 	mov	dpl, r6
      00AD49 8F 83            [24] 1715 	mov	dph, r7
                                   1716 ;	quantum/vial.c:289: break;
                                   1717 ;	quantum/vial.c:309: case vial_dynamic_entry_op: {
      00AD4B 02 A8 DE         [24] 1718 	ljmp	_vial_fill_packet
      00AD4E                       1719 00122$:
                                   1720 ;	quantum/vial.c:310: switch (msg[2]) {
      00AD4E 74 02            [12] 1721 	mov	a,#0x02
      00AD50 2E               [12] 1722 	add	a, r6
      00AD51 FC               [12] 1723 	mov	r4,a
      00AD52 E4               [12] 1724 	clr	a
      00AD53 3F               [12] 1725 	addc	a, r7
      00AD54 FD               [12] 1726 	mov	r5,a
      00AD55 8C 82            [24] 1727 	mov	dpl,r4
      00AD57 8D 83            [24] 1728 	mov	dph,r5
      00AD59 E0               [24] 1729 	movx	a,@dptr
      00AD5A 70 33            [24] 1730 	jnz	00135$
                                   1731 ;	quantum/vial.c:312: VIAL_FILL_PACKET(msg, 0, length);
      00AD5C 90 0A 5F         [24] 1732 	mov	dptr,#_vial_fill_packet_PARM_2
      00AD5F E4               [12] 1733 	clr	a
      00AD60 F0               [24] 1734 	movx	@dptr,a
      00AD61 8E 82            [24] 1735 	mov	dpl, r6
      00AD63 8F 83            [24] 1736 	mov	dph, r7
      00AD65 C0 07            [24] 1737 	push	ar7
      00AD67 C0 06            [24] 1738 	push	ar6
      00AD69 12 A8 DE         [24] 1739 	lcall	_vial_fill_packet
      00AD6C D0 06            [24] 1740 	pop	ar6
      00AD6E D0 07            [24] 1741 	pop	ar7
                                   1742 ;	quantum/vial.c:313: msg[0] = VIAL_TAP_DANCE_ENTRIES;
      00AD70 8E 82            [24] 1743 	mov	dpl,r6
      00AD72 8F 83            [24] 1744 	mov	dph,r7
      00AD74 E4               [12] 1745 	clr	a
      00AD75 F0               [24] 1746 	movx	@dptr,a
                                   1747 ;	quantum/vial.c:314: msg[1] = VIAL_COMBO_ENTRIES;
      00AD76 8E 82            [24] 1748 	mov	dpl,r6
      00AD78 8F 83            [24] 1749 	mov	dph,r7
      00AD7A A3               [24] 1750 	inc	dptr
      00AD7B F0               [24] 1751 	movx	@dptr,a
                                   1752 ;	quantum/vial.c:315: msg[2] = VIAL_KEY_OVERRIDE_ENTRIES;
      00AD7C 8E 82            [24] 1753 	mov	dpl,r6
      00AD7E 8F 83            [24] 1754 	mov	dph,r7
      00AD80 A3               [24] 1755 	inc	dptr
      00AD81 A3               [24] 1756 	inc	dptr
      00AD82 F0               [24] 1757 	movx	@dptr,a
                                   1758 ;	quantum/vial.c:317: msg[VIAL_RAW_EPSIZE - 1] = 1; /* Standard Vial feature bit 0. */
      00AD83 74 1F            [12] 1759 	mov	a,#0x1f
      00AD85 2E               [12] 1760 	add	a, r6
      00AD86 F5 82            [12] 1761 	mov	dpl,a
      00AD88 E4               [12] 1762 	clr	a
      00AD89 3F               [12] 1763 	addc	a, r7
      00AD8A F5 83            [12] 1764 	mov	dph,a
      00AD8C 74 01            [12] 1765 	mov	a,#0x01
      00AD8E F0               [24] 1766 	movx	@dptr,a
                                   1767 ;	quantum/vial.c:382: }
      00AD8F                       1768 00135$:
                                   1769 ;	quantum/vial.c:383: }
      00AD8F 22               [24] 1770 	ret
                                   1771 ;------------------------------------------------------------
                                   1772 ;Allocation info for local variables in function 'vial_keycode_down'
                                   1773 ;------------------------------------------------------------
                                   1774 ;keycode       Allocated with name '_vial_keycode_down_keycode_10000_629'
                                   1775 ;dummy_event   Allocated with name '_vial_keycode_down_dummy_event_30000_633'
                                   1776 ;------------------------------------------------------------
                                   1777 ;	quantum/vial.c:387: void vial_keycode_down(uint16_t keycode) {
                                   1778 ;	-----------------------------------------
                                   1779 ;	 function vial_keycode_down
                                   1780 ;	-----------------------------------------
      00AD90                       1781 _vial_keycode_down:
      00AD90 AF 83            [24] 1782 	mov	r7,dph
      00AD92 E5 82            [12] 1783 	mov	a,dpl
      00AD94 90 0A 6A         [24] 1784 	mov	dptr,#_vial_keycode_down_keycode_10000_629
      00AD97 F0               [24] 1785 	movx	@dptr,a
      00AD98 EF               [12] 1786 	mov	a,r7
      00AD99 A3               [24] 1787 	inc	dptr
      00AD9A F0               [24] 1788 	movx	@dptr,a
                                   1789 ;	quantum/vial.c:388: g_vial_magic_keycode_override = keycode;
      00AD9B 90 0A 6A         [24] 1790 	mov	dptr,#_vial_keycode_down_keycode_10000_629
      00AD9E 12 AE 58         [24] 1791 	lcall	_ak820_outline_0016
                                   1792 ;	quantum/vial.c:390: if (keycode <= QK_MODS_MAX) {
      00ADA1 40 07            [24] 1793 	jc	00102$
                                   1794 ;	free result
                                   1795 ;	quantum/vial.c:391: register_code16(keycode);
      00ADA3 8E 82            [24] 1796 	mov	dpl, r6
      00ADA5 8F 83            [24] 1797 	mov	dph, r7
      00ADA7 02 97 B1         [24] 1798 	ljmp	_register_code16
      00ADAA                       1799 00102$:
                                   1800 ;	quantum/vial.c:393: keyevent_t dummy_event = {
      00ADAA 90 0A 70         [24] 1801 	mov	dptr,#(_vial_keycode_down_dummy_event_30000_633 + 0x0004)
      00ADAD 74 01            [12] 1802 	mov	a,#0x01
      00ADAF F0               [24] 1803 	movx	@dptr,a
      00ADB0 90 0A 6D         [24] 1804 	mov	dptr,#(_vial_keycode_down_dummy_event_30000_633 + 0x0001)
      00ADB3 74 F0            [12] 1805 	mov	a,#0xf0
      00ADB5 F0               [24] 1806 	movx	@dptr,a
      00ADB6 90 0A 6C         [24] 1807 	mov	dptr,#_vial_keycode_down_dummy_event_30000_633
      00ADB9 F0               [24] 1808 	movx	@dptr,a
      00ADBA 90 0A 71         [24] 1809 	mov	dptr,#(_vial_keycode_down_dummy_event_30000_633 + 0x0005)
      00ADBD 74 01            [12] 1810 	mov	a,#0x01
      00ADBF F0               [24] 1811 	movx	@dptr,a
      00ADC0 12 40 6D         [24] 1812 	lcall	_timer_read
      00ADC3 AE 82            [24] 1813 	mov	r6, dpl
      00ADC5 AF 83            [24] 1814 	mov	r7, dph
      00ADC7 43 06 01         [24] 1815 	orl	ar6,#0x01
      00ADCA 90 0A 6E         [24] 1816 	mov	dptr,#(_vial_keycode_down_dummy_event_30000_633 + 0x0002)
      00ADCD EE               [12] 1817 	mov	a,r6
      00ADCE F0               [24] 1818 	movx	@dptr,a
      00ADCF EF               [12] 1819 	mov	a,r7
      00ADD0 A3               [24] 1820 	inc	dptr
      00ADD1 F0               [24] 1821 	movx	@dptr,a
                                   1822 ;	quantum/vial.c:397: action_exec(dummy_event);
      00ADD2 90 0B 90         [24] 1823 	mov	dptr,#___memcpy_PARM_2
      00ADD5 74 6C            [12] 1824 	mov	a,#_vial_keycode_down_dummy_event_30000_633
      00ADD7 F0               [24] 1825 	movx	@dptr,a
      00ADD8 74 0A            [12] 1826 	mov	a,#(_vial_keycode_down_dummy_event_30000_633 >> 8)
      00ADDA 12 AE 71         [24] 1827 	lcall	_ak820_outline_0026
      00ADDD 12 B4 BE         [24] 1828 	lcall	___memcpy
                                   1829 ;	quantum/vial.c:399: }
      00ADE0 02 6D 00         [24] 1830 	ljmp	_action_exec
                                   1831 ;------------------------------------------------------------
                                   1832 ;Allocation info for local variables in function 'vial_keycode_up'
                                   1833 ;------------------------------------------------------------
                                   1834 ;keycode       Allocated with name '_vial_keycode_up_keycode_10000_634'
                                   1835 ;dummy_event   Allocated with name '_vial_keycode_up_dummy_event_30000_638'
                                   1836 ;------------------------------------------------------------
                                   1837 ;	quantum/vial.c:401: void vial_keycode_up(uint16_t keycode) {
                                   1838 ;	-----------------------------------------
                                   1839 ;	 function vial_keycode_up
                                   1840 ;	-----------------------------------------
      00ADE3                       1841 _vial_keycode_up:
      00ADE3 AF 83            [24] 1842 	mov	r7,dph
      00ADE5 E5 82            [12] 1843 	mov	a,dpl
      00ADE7 90 0A 72         [24] 1844 	mov	dptr,#_vial_keycode_up_keycode_10000_634
      00ADEA F0               [24] 1845 	movx	@dptr,a
      00ADEB EF               [12] 1846 	mov	a,r7
      00ADEC A3               [24] 1847 	inc	dptr
      00ADED F0               [24] 1848 	movx	@dptr,a
                                   1849 ;	quantum/vial.c:402: g_vial_magic_keycode_override = keycode;
      00ADEE 90 0A 72         [24] 1850 	mov	dptr,#_vial_keycode_up_keycode_10000_634
      00ADF1 12 AE 58         [24] 1851 	lcall	_ak820_outline_0016
                                   1852 ;	quantum/vial.c:404: if (keycode <= QK_MODS_MAX) {
      00ADF4 40 07            [24] 1853 	jc	00102$
                                   1854 ;	free result
                                   1855 ;	quantum/vial.c:405: unregister_code16(keycode);
      00ADF6 8E 82            [24] 1856 	mov	dpl, r6
      00ADF8 8F 83            [24] 1857 	mov	dph, r7
      00ADFA 02 98 00         [24] 1858 	ljmp	_unregister_code16
      00ADFD                       1859 00102$:
                                   1860 ;	quantum/vial.c:407: keyevent_t dummy_event = {
      00ADFD 90 0A 78         [24] 1861 	mov	dptr,#(_vial_keycode_up_dummy_event_30000_638 + 0x0004)
      00AE00 74 01            [12] 1862 	mov	a,#0x01
      00AE02 F0               [24] 1863 	movx	@dptr,a
      00AE03 90 0A 75         [24] 1864 	mov	dptr,#(_vial_keycode_up_dummy_event_30000_638 + 0x0001)
      00AE06 74 F0            [12] 1865 	mov	a,#0xf0
      00AE08 F0               [24] 1866 	movx	@dptr,a
      00AE09 90 0A 74         [24] 1867 	mov	dptr,#_vial_keycode_up_dummy_event_30000_638
      00AE0C F0               [24] 1868 	movx	@dptr,a
      00AE0D 90 0A 79         [24] 1869 	mov	dptr,#(_vial_keycode_up_dummy_event_30000_638 + 0x0005)
      00AE10 E4               [12] 1870 	clr	a
      00AE11 F0               [24] 1871 	movx	@dptr,a
      00AE12 12 40 6D         [24] 1872 	lcall	_timer_read
      00AE15 AE 82            [24] 1873 	mov	r6, dpl
      00AE17 AF 83            [24] 1874 	mov	r7, dph
      00AE19 43 06 01         [24] 1875 	orl	ar6,#0x01
      00AE1C 90 0A 76         [24] 1876 	mov	dptr,#(_vial_keycode_up_dummy_event_30000_638 + 0x0002)
      00AE1F EE               [12] 1877 	mov	a,r6
      00AE20 F0               [24] 1878 	movx	@dptr,a
      00AE21 EF               [12] 1879 	mov	a,r7
      00AE22 A3               [24] 1880 	inc	dptr
      00AE23 F0               [24] 1881 	movx	@dptr,a
                                   1882 ;	quantum/vial.c:411: action_exec(dummy_event);
      00AE24 90 0B 90         [24] 1883 	mov	dptr,#___memcpy_PARM_2
      00AE27 74 74            [12] 1884 	mov	a,#_vial_keycode_up_dummy_event_30000_638
      00AE29 F0               [24] 1885 	movx	@dptr,a
      00AE2A 74 0A            [12] 1886 	mov	a,#(_vial_keycode_up_dummy_event_30000_638 >> 8)
      00AE2C 12 AE 71         [24] 1887 	lcall	_ak820_outline_0026
      00AE2F 12 B4 BE         [24] 1888 	lcall	___memcpy
                                   1889 ;	quantum/vial.c:413: }
      00AE32 02 6D 00         [24] 1890 	ljmp	_action_exec
                                   1891 ;------------------------------------------------------------
                                   1892 ;Allocation info for local variables in function 'vial_keycode_tap'
                                   1893 ;------------------------------------------------------------
                                   1894 ;keycode       Allocated with name '_vial_keycode_tap_keycode_10000_639'
                                   1895 ;i             Allocated with name '_vial_keycode_tap_i_30000_642'
                                   1896 ;------------------------------------------------------------
                                   1897 ;	quantum/vial.c:415: void vial_keycode_tap(uint16_t keycode) {
                                   1898 ;	-----------------------------------------
                                   1899 ;	 function vial_keycode_tap
                                   1900 ;	-----------------------------------------
      00AE35                       1901 _vial_keycode_tap:
      00AE35 AF 83            [24] 1902 	mov	r7,dph
      00AE37 E5 82            [12] 1903 	mov	a,dpl
      00AE39 90 0A 7A         [24] 1904 	mov	dptr,#_vial_keycode_tap_keycode_10000_639
      00AE3C F0               [24] 1905 	movx	@dptr,a
      00AE3D EF               [12] 1906 	mov	a,r7
      00AE3E A3               [24] 1907 	inc	dptr
      00AE3F F0               [24] 1908 	movx	@dptr,a
                                   1909 ;	quantum/vial.c:416: vial_keycode_down(keycode);
      00AE40 90 0A 7A         [24] 1910 	mov	dptr,#_vial_keycode_tap_keycode_10000_639
      00AE43 12 73 CF         [24] 1911 	lcall	_ak820_outline_0013
      00AE46 C0 07            [24] 1912 	push	ar7
      00AE48 C0 06            [24] 1913 	push	ar6
      00AE4A 12 AD 90         [24] 1914 	lcall	_vial_keycode_down
      00AE4D D0 06            [24] 1915 	pop	ar6
      00AE4F D0 07            [24] 1916 	pop	ar7
                                   1917 ;	quantum/vial.c:418: vial_keycode_up(keycode);
      00AE51 8E 82            [24] 1918 	mov	dpl, r6
      00AE53 8F 83            [24] 1919 	mov	dph, r7
                                   1920 ;	quantum/vial.c:419: }
      00AE55 02 AD E3         [24] 1921 	ljmp	_vial_keycode_up
                                   1922 ;------------------------------------------------------------
                                   1923 ;Allocation info for local variables in function 'process_record_vial'
                                   1924 ;------------------------------------------------------------
                                   1925 ;record        Allocated with name '_process_record_vial_PARM_2'
                                   1926 ;keycode       Allocated with name '_process_record_vial_keycode_10000_644'
                                   1927 ;------------------------------------------------------------
                                   1928 ;	quantum/vial.c:629: bool process_record_vial(uint16_t keycode, keyrecord_t *record) {
                                   1929 ;	-----------------------------------------
                                   1930 	.area CSEG    (CODE)
                                   1931 	.area CONST   (CODE)
                                   1932 	.area CONST   (CODE)
      00BA2D                       1933 _keyboard_definition:
      00BA2D FD                    1934 	.db #0xfd	; 253
      00BA2E 37                    1935 	.db #0x37	; 55	'7'
      00BA2F 7A                    1936 	.db #0x7a	; 122	'z'
      00BA30 58                    1937 	.db #0x58	; 88	'X'
      00BA31 5A                    1938 	.db #0x5a	; 90	'Z'
      00BA32 00                    1939 	.db #0x00	; 0
      00BA33 00                    1940 	.db #0x00	; 0
      00BA34 04                    1941 	.db #0x04	; 4
      00BA35 E6                    1942 	.db #0xe6	; 230
      00BA36 D6                    1943 	.db #0xd6	; 214
      00BA37 B4                    1944 	.db #0xb4	; 180
      00BA38 46                    1945 	.db #0x46	; 70	'F'
      00BA39 02                    1946 	.db #0x02	; 2
      00BA3A 00                    1947 	.db #0x00	; 0
      00BA3B 21                    1948 	.db #0x21	; 33
      00BA3C 01                    1949 	.db #0x01	; 1
      00BA3D 00                    1950 	.db #0x00	; 0
      00BA3E 00                    1951 	.db #0x00	; 0
      00BA3F 00                    1952 	.db #0x00	; 0
      00BA40 00                    1953 	.db #0x00	; 0
      00BA41 37                    1954 	.db #0x37	; 55	'7'
      00BA42 27                    1955 	.db #0x27	; 39
      00BA43 97                    1956 	.db #0x97	; 151
      00BA44 D6                    1957 	.db #0xd6	; 214
      00BA45 E0                    1958 	.db #0xe0	; 224
      00BA46 03                    1959 	.db #0x03	; 3
      00BA47 CB                    1960 	.db #0xcb	; 203
      00BA48 01                    1961 	.db #0x01	; 1
      00BA49 3C                    1962 	.db #0x3c	; 60
      00BA4A 00                    1963 	.db #0x00	; 0
      00BA4B 00                    1964 	.db #0x00	; 0
      00BA4C 3D                    1965 	.db #0x3d	; 61
      00BA4D 88                    1966 	.db #0x88	; 136
      00BA4E CD                    1967 	.db #0xcd	; 205
      00BA4F A5                    1968 	.db #0xa5	; 165
      00BA50 AA                    1969 	.db #0xaa	; 170
      00BA51 E5                    1970 	.db #0xe5	; 229
      00BA52 A8                    1971 	.db #0xa8	; 168
      00BA53 76                    1972 	.db #0x76	; 118	'v'
      00BA54 F6                    1973 	.db #0xf6	; 246
      00BA55 43                    1974 	.db #0x43	; 67	'C'
      00BA56 0E                    1975 	.db #0x0e	; 14
      00BA57 D2                    1976 	.db #0xd2	; 210
      00BA58 90                    1977 	.db #0x90	; 144
      00BA59 7D                    1978 	.db #0x7d	; 125
      00BA5A 94                    1979 	.db #0x94	; 148
      00BA5B 79                    1980 	.db #0x79	; 121	'y'
      00BA5C 78                    1981 	.db #0x78	; 120	'x'
      00BA5D EF                    1982 	.db #0xef	; 239
      00BA5E 49                    1983 	.db #0x49	; 73	'I'
      00BA5F 3E                    1984 	.db #0x3e	; 62
      00BA60 EF                    1985 	.db #0xef	; 239
      00BA61 FD                    1986 	.db #0xfd	; 253
      00BA62 8F                    1987 	.db #0x8f	; 143
      00BA63 EF                    1988 	.db #0xef	; 239
      00BA64 00                    1989 	.db #0x00	; 0
      00BA65 C6                    1990 	.db #0xc6	; 198
      00BA66 D1                    1991 	.db #0xd1	; 209
      00BA67 DB                    1992 	.db #0xdb	; 219
      00BA68 FB                    1993 	.db #0xfb	; 251
      00BA69 EB                    1994 	.db #0xeb	; 235
      00BA6A DE                    1995 	.db #0xde	; 222
      00BA6B 66                    1996 	.db #0x66	; 102	'f'
      00BA6C 63                    1997 	.db #0x63	; 99	'c'
      00BA6D 0C                    1998 	.db #0x0c	; 12
      00BA6E 92                    1999 	.db #0x92	; 146
      00BA6F 7B                    2000 	.db #0x7b	; 123
      00BA70 F9                    2001 	.db #0xf9	; 249
      00BA71 D4                    2002 	.db #0xd4	; 212
      00BA72 7A                    2003 	.db #0x7a	; 122	'z'
      00BA73 4F                    2004 	.db #0x4f	; 79	'O'
      00BA74 83                    2005 	.db #0x83	; 131
      00BA75 4B                    2006 	.db #0x4b	; 75	'K'
      00BA76 86                    2007 	.db #0x86	; 134
      00BA77 0E                    2008 	.db #0x0e	; 14
      00BA78 6A                    2009 	.db #0x6a	; 106	'j'
      00BA79 F2                    2010 	.db #0xf2	; 242
      00BA7A 22                    2011 	.db #0x22	; 34
      00BA7B 22                    2012 	.db #0x22	; 34
      00BA7C 0B                    2013 	.db #0x0b	; 11
      00BA7D 03                    2014 	.db #0x03	; 3
      00BA7E BA                    2015 	.db #0xba	; 186
      00BA7F 67                    2016 	.db #0x67	; 103	'g'
      00BA80 9B                    2017 	.db #0x9b	; 155
      00BA81 7A                    2018 	.db #0x7a	; 122	'z'
      00BA82 E1                    2019 	.db #0xe1	; 225
      00BA83 BC                    2020 	.db #0xbc	; 188
      00BA84 37                    2021 	.db #0x37	; 55	'7'
      00BA85 26                    2022 	.db #0x26	; 38
      00BA86 46                    2023 	.db #0x46	; 70	'F'
      00BA87 78                    2024 	.db #0x78	; 120	'x'
      00BA88 05                    2025 	.db #0x05	; 5
      00BA89 0D                    2026 	.db #0x0d	; 13
      00BA8A 95                    2027 	.db #0x95	; 149
      00BA8B 02                    2028 	.db #0x02	; 2
      00BA8C E4                    2029 	.db #0xe4	; 228
      00BA8D 18                    2030 	.db #0x18	; 24
      00BA8E CA                    2031 	.db #0xca	; 202
      00BA8F 33                    2032 	.db #0x33	; 51	'3'
      00BA90 EA                    2033 	.db #0xea	; 234
      00BA91 24                    2034 	.db #0x24	; 36
      00BA92 C8                    2035 	.db #0xc8	; 200
      00BA93 81                    2036 	.db #0x81	; 129
      00BA94 4E                    2037 	.db #0x4e	; 78	'N'
      00BA95 47                    2038 	.db #0x47	; 71	'G'
      00BA96 A8                    2039 	.db #0xa8	; 168
      00BA97 44                    2040 	.db #0x44	; 68	'D'
      00BA98 DD                    2041 	.db #0xdd	; 221
      00BA99 91                    2042 	.db #0x91	; 145
      00BA9A 6D                    2043 	.db #0x6d	; 109	'm'
      00BA9B 69                    2044 	.db #0x69	; 105	'i'
      00BA9C DB                    2045 	.db #0xdb	; 219
      00BA9D 4F                    2046 	.db #0x4f	; 79	'O'
      00BA9E 3A                    2047 	.db #0x3a	; 58
      00BA9F 43                    2048 	.db #0x43	; 67	'C'
      00BAA0 9D                    2049 	.db #0x9d	; 157
      00BAA1 26                    2050 	.db #0x26	; 38
      00BAA2 49                    2051 	.db #0x49	; 73	'I'
      00BAA3 4C                    2052 	.db #0x4c	; 76	'L'
      00BAA4 EF                    2053 	.db #0xef	; 239
      00BAA5 2B                    2054 	.db #0x2b	; 43
      00BAA6 D8                    2055 	.db #0xd8	; 216
      00BAA7 55                    2056 	.db #0x55	; 85	'U'
      00BAA8 95                    2057 	.db #0x95	; 149
      00BAA9 70                    2058 	.db #0x70	; 112	'p'
      00BAAA B1                    2059 	.db #0xb1	; 177
      00BAAB CC                    2060 	.db #0xcc	; 204
      00BAAC CF                    2061 	.db #0xcf	; 207
      00BAAD 13                    2062 	.db #0x13	; 19
      00BAAE 32                    2063 	.db #0x32	; 50	'2'
      00BAAF 6A                    2064 	.db #0x6a	; 106	'j'
      00BAB0 A1                    2065 	.db #0xa1	; 161
      00BAB1 FF                    2066 	.db #0xff	; 255
      00BAB2 99                    2067 	.db #0x99	; 153
      00BAB3 61                    2068 	.db #0x61	; 97	'a'
      00BAB4 95                    2069 	.db #0x95	; 149
      00BAB5 B1                    2070 	.db #0xb1	; 177
      00BAB6 89                    2071 	.db #0x89	; 137
      00BAB7 9B                    2072 	.db #0x9b	; 155
      00BAB8 11                    2073 	.db #0x11	; 17
      00BAB9 D9                    2074 	.db #0xd9	; 217
      00BABA 35                    2075 	.db #0x35	; 53	'5'
      00BABB 78                    2076 	.db #0x78	; 120	'x'
      00BABC ED                    2077 	.db #0xed	; 237
      00BABD CD                    2078 	.db #0xcd	; 205
      00BABE 94                    2079 	.db #0x94	; 148
      00BABF 6E                    2080 	.db #0x6e	; 110	'n'
      00BAC0 60                    2081 	.db #0x60	; 96
      00BAC1 8E                    2082 	.db #0x8e	; 142
      00BAC2 63                    2083 	.db #0x63	; 99	'c'
      00BAC3 8B                    2084 	.db #0x8b	; 139
      00BAC4 FF                    2085 	.db #0xff	; 255
      00BAC5 4E                    2086 	.db #0x4e	; 78	'N'
      00BAC6 20                    2087 	.db #0x20	; 32
      00BAC7 7A                    2088 	.db #0x7a	; 122	'z'
      00BAC8 B5                    2089 	.db #0xb5	; 181
      00BAC9 87                    2090 	.db #0x87	; 135
      00BACA C2                    2091 	.db #0xc2	; 194
      00BACB 35                    2092 	.db #0x35	; 53	'5'
      00BACC A4                    2093 	.db #0xa4	; 164
      00BACD 6D                    2094 	.db #0x6d	; 109	'm'
      00BACE 18                    2095 	.db #0x18	; 24
      00BACF C1                    2096 	.db #0xc1	; 193
      00BAD0 A3                    2097 	.db #0xa3	; 163
      00BAD1 DB                    2098 	.db #0xdb	; 219
      00BAD2 53                    2099 	.db #0x53	; 83	'S'
      00BAD3 1D                    2100 	.db #0x1d	; 29
      00BAD4 EC                    2101 	.db #0xec	; 236
      00BAD5 F0                    2102 	.db #0xf0	; 240
      00BAD6 BF                    2103 	.db #0xbf	; 191
      00BAD7 4A                    2104 	.db #0x4a	; 74	'J'
      00BAD8 4C                    2105 	.db #0x4c	; 76	'L'
      00BAD9 4A                    2106 	.db #0x4a	; 74	'J'
      00BADA C4                    2107 	.db #0xc4	; 196
      00BADB AA                    2108 	.db #0xaa	; 170
      00BADC 37                    2109 	.db #0x37	; 55	'7'
      00BADD 19                    2110 	.db #0x19	; 25
      00BADE 34                    2111 	.db #0x34	; 52	'4'
      00BADF 3F                    2112 	.db #0x3f	; 63
      00BAE0 A1                    2113 	.db #0xa1	; 161
      00BAE1 D3                    2114 	.db #0xd3	; 211
      00BAE2 1A                    2115 	.db #0x1a	; 26
      00BAE3 5C                    2116 	.db #0x5c	; 92
      00BAE4 03                    2117 	.db #0x03	; 3
      00BAE5 4D                    2118 	.db #0x4d	; 77	'M'
      00BAE6 BC                    2119 	.db #0xbc	; 188
      00BAE7 10                    2120 	.db #0x10	; 16
      00BAE8 2E                    2121 	.db #0x2e	; 46
      00BAE9 80                    2122 	.db #0x80	; 128
      00BAEA F7                    2123 	.db #0xf7	; 247
      00BAEB D6                    2124 	.db #0xd6	; 214
      00BAEC 82                    2125 	.db #0x82	; 130
      00BAED 24                    2126 	.db #0x24	; 36
      00BAEE 4C                    2127 	.db #0x4c	; 76	'L'
      00BAEF 87                    2128 	.db #0x87	; 135
      00BAF0 B9                    2129 	.db #0xb9	; 185
      00BAF1 F8                    2130 	.db #0xf8	; 248
      00BAF2 BE                    2131 	.db #0xbe	; 190
      00BAF3 67                    2132 	.db #0x67	; 103	'g'
      00BAF4 96                    2133 	.db #0x96	; 150
      00BAF5 89                    2134 	.db #0x89	; 137
      00BAF6 30                    2135 	.db #0x30	; 48	'0'
      00BAF7 C8                    2136 	.db #0xc8	; 200
      00BAF8 8D                    2137 	.db #0x8d	; 141
      00BAF9 2C                    2138 	.db #0x2c	; 44
      00BAFA F5                    2139 	.db #0xf5	; 245
      00BAFB 06                    2140 	.db #0x06	; 6
      00BAFC 05                    2141 	.db #0x05	; 5
      00BAFD 7C                    2142 	.db #0x7c	; 124
      00BAFE 48                    2143 	.db #0x48	; 72	'H'
      00BAFF 1B                    2144 	.db #0x1b	; 27
      00BB00 76                    2145 	.db #0x76	; 118	'v'
      00BB01 AA                    2146 	.db #0xaa	; 170
      00BB02 3D                    2147 	.db #0x3d	; 61
      00BB03 28                    2148 	.db #0x28	; 40
      00BB04 FC                    2149 	.db #0xfc	; 252
      00BB05 80                    2150 	.db #0x80	; 128
      00BB06 75                    2151 	.db #0x75	; 117	'u'
      00BB07 EB                    2152 	.db #0xeb	; 235
      00BB08 78                    2153 	.db #0x78	; 120	'x'
      00BB09 D0                    2154 	.db #0xd0	; 208
      00BB0A 8A                    2155 	.db #0x8a	; 138
      00BB0B 8F                    2156 	.db #0x8f	; 143
      00BB0C 27                    2157 	.db #0x27	; 39
      00BB0D F7                    2158 	.db #0xf7	; 247
      00BB0E F2                    2159 	.db #0xf2	; 242
      00BB0F EB                    2160 	.db #0xeb	; 235
      00BB10 58                    2161 	.db #0x58	; 88	'X'
      00BB11 37                    2162 	.db #0x37	; 55	'7'
      00BB12 3C                    2163 	.db #0x3c	; 60
      00BB13 2B                    2164 	.db #0x2b	; 43
      00BB14 6F                    2165 	.db #0x6f	; 111	'o'
      00BB15 0E                    2166 	.db #0x0e	; 14
      00BB16 C7                    2167 	.db #0xc7	; 199
      00BB17 E2                    2168 	.db #0xe2	; 226
      00BB18 A0                    2169 	.db #0xa0	; 160
      00BB19 97                    2170 	.db #0x97	; 151
      00BB1A EE                    2171 	.db #0xee	; 238
      00BB1B FD                    2172 	.db #0xfd	; 253
      00BB1C 9F                    2173 	.db #0x9f	; 159
      00BB1D 45                    2174 	.db #0x45	; 69	'E'
      00BB1E 17                    2175 	.db #0x17	; 23
      00BB1F 94                    2176 	.db #0x94	; 148
      00BB20 E6                    2177 	.db #0xe6	; 230
      00BB21 E7                    2178 	.db #0xe7	; 231
      00BB22 FA                    2179 	.db #0xfa	; 250
      00BB23 4C                    2180 	.db #0x4c	; 76	'L'
      00BB24 7A                    2181 	.db #0x7a	; 122	'z'
      00BB25 D6                    2182 	.db #0xd6	; 214
      00BB26 7A                    2183 	.db #0x7a	; 122	'z'
      00BB27 7B                    2184 	.db #0x7b	; 123
      00BB28 ED                    2185 	.db #0xed	; 237
      00BB29 10                    2186 	.db #0x10	; 16
      00BB2A C5                    2187 	.db #0xc5	; 197
      00BB2B BC                    2188 	.db #0xbc	; 188
      00BB2C E3                    2189 	.db #0xe3	; 227
      00BB2D A9                    2190 	.db #0xa9	; 169
      00BB2E 1F                    2191 	.db #0x1f	; 31
      00BB2F CF                    2192 	.db #0xcf	; 207
      00BB30 C4                    2193 	.db #0xc4	; 196
      00BB31 9D                    2194 	.db #0x9d	; 157
      00BB32 DC                    2195 	.db #0xdc	; 220
      00BB33 45                    2196 	.db #0x45	; 69	'E'
      00BB34 2A                    2197 	.db #0x2a	; 42
      00BB35 69                    2198 	.db #0x69	; 105	'i'
      00BB36 57                    2199 	.db #0x57	; 87	'W'
      00BB37 8F                    2200 	.db #0x8f	; 143
      00BB38 EC                    2201 	.db #0xec	; 236
      00BB39 85                    2202 	.db #0x85	; 133
      00BB3A 6C                    2203 	.db #0x6c	; 108	'l'
      00BB3B 43                    2204 	.db #0x43	; 67	'C'
      00BB3C 1C                    2205 	.db #0x1c	; 28
      00BB3D BA                    2206 	.db #0xba	; 186
      00BB3E 89                    2207 	.db #0x89	; 137
      00BB3F 68                    2208 	.db #0x68	; 104	'h'
      00BB40 4A                    2209 	.db #0x4a	; 74	'J'
      00BB41 1C                    2210 	.db #0x1c	; 28
      00BB42 91                    2211 	.db #0x91	; 145
      00BB43 3F                    2212 	.db #0x3f	; 63
      00BB44 D1                    2213 	.db #0xd1	; 209
      00BB45 B3                    2214 	.db #0xb3	; 179
      00BB46 96                    2215 	.db #0x96	; 150
      00BB47 1D                    2216 	.db #0x1d	; 29
      00BB48 7C                    2217 	.db #0x7c	; 124
      00BB49 14                    2218 	.db #0x14	; 20
      00BB4A 77                    2219 	.db #0x77	; 119	'w'
      00BB4B 9C                    2220 	.db #0x9c	; 156
      00BB4C 74                    2221 	.db #0x74	; 116	't'
      00BB4D 36                    2222 	.db #0x36	; 54	'6'
      00BB4E FF                    2223 	.db #0xff	; 255
      00BB4F 2C                    2224 	.db #0x2c	; 44
      00BB50 66                    2225 	.db #0x66	; 102	'f'
      00BB51 AF                    2226 	.db #0xaf	; 175
      00BB52 0F                    2227 	.db #0x0f	; 15
      00BB53 3C                    2228 	.db #0x3c	; 60
      00BB54 A2                    2229 	.db #0xa2	; 162
      00BB55 23                    2230 	.db #0x23	; 35
      00BB56 85                    2231 	.db #0x85	; 133
      00BB57 05                    2232 	.db #0x05	; 5
      00BB58 87                    2233 	.db #0x87	; 135
      00BB59 DA                    2234 	.db #0xda	; 218
      00BB5A 61                    2235 	.db #0x61	; 97	'a'
      00BB5B 5E                    2236 	.db #0x5e	; 94
      00BB5C 42                    2237 	.db #0x42	; 66	'B'
      00BB5D 54                    2238 	.db #0x54	; 84	'T'
      00BB5E 60                    2239 	.db #0x60	; 96
      00BB5F 23                    2240 	.db #0x23	; 35
      00BB60 CA                    2241 	.db #0xca	; 202
      00BB61 BC                    2242 	.db #0xbc	; 188
      00BB62 B3                    2243 	.db #0xb3	; 179
      00BB63 18                    2244 	.db #0x18	; 24
      00BB64 1D                    2245 	.db #0x1d	; 29
      00BB65 F8                    2246 	.db #0xf8	; 248
      00BB66 0A                    2247 	.db #0x0a	; 10
      00BB67 55                    2248 	.db #0x55	; 85	'U'
      00BB68 CD                    2249 	.db #0xcd	; 205
      00BB69 A3                    2250 	.db #0xa3	; 163
      00BB6A DE                    2251 	.db #0xde	; 222
      00BB6B FF                    2252 	.db #0xff	; 255
      00BB6C B2                    2253 	.db #0xb2	; 178
      00BB6D 2A                    2254 	.db #0x2a	; 42
      00BB6E 35                    2255 	.db #0x35	; 53	'5'
      00BB6F 00                    2256 	.db #0x00	; 0
      00BB70 D6                    2257 	.db #0xd6	; 214
      00BB71 7B                    2258 	.db #0x7b	; 123
      00BB72 E8                    2259 	.db #0xe8	; 232
      00BB73 F2                    2260 	.db #0xf2	; 242
      00BB74 1A                    2261 	.db #0x1a	; 26
      00BB75 BC                    2262 	.db #0xbc	; 188
      00BB76 F5                    2263 	.db #0xf5	; 245
      00BB77 7E                    2264 	.db #0x7e	; 126
      00BB78 48                    2265 	.db #0x48	; 72	'H'
      00BB79 72                    2266 	.db #0x72	; 114	'r'
      00BB7A E0                    2267 	.db #0xe0	; 224
      00BB7B E4                    2268 	.db #0xe4	; 228
      00BB7C E0                    2269 	.db #0xe0	; 224
      00BB7D 27                    2270 	.db #0x27	; 39
      00BB7E 87                    2271 	.db #0x87	; 135
      00BB7F 9A                    2272 	.db #0x9a	; 154
      00BB80 51                    2273 	.db #0x51	; 81	'Q'
      00BB81 D4                    2274 	.db #0xd4	; 212
      00BB82 DD                    2275 	.db #0xdd	; 221
      00BB83 C3                    2276 	.db #0xc3	; 195
      00BB84 AA                    2277 	.db #0xaa	; 170
      00BB85 49                    2278 	.db #0x49	; 73	'I'
      00BB86 5A                    2279 	.db #0x5a	; 90	'Z'
      00BB87 2A                    2280 	.db #0x2a	; 42
      00BB88 00                    2281 	.db #0x00	; 0
      00BB89 A0                    2282 	.db #0xa0	; 160
      00BB8A 8C                    2283 	.db #0x8c	; 140
      00BB8B FF                    2284 	.db #0xff	; 255
      00BB8C 74                    2285 	.db #0x74	; 116	't'
      00BB8D BF                    2286 	.db #0xbf	; 191
      00BB8E EC                    2287 	.db #0xec	; 236
      00BB8F 1D                    2288 	.db #0x1d	; 29
      00BB90 F1                    2289 	.db #0xf1	; 241
      00BB91 00                    2290 	.db #0x00	; 0
      00BB92 01                    2291 	.db #0x01	; 1
      00BB93 D8                    2292 	.db #0xd8	; 216
      00BB94 02                    2293 	.db #0x02	; 2
      00BB95 CC                    2294 	.db #0xcc	; 204
      00BB96 07                    2295 	.db #0x07	; 7
      00BB97 00                    2296 	.db #0x00	; 0
      00BB98 00                    2297 	.db #0x00	; 0
      00BB99 C4                    2298 	.db #0xc4	; 196
      00BB9A 5E                    2299 	.db #0x5e	; 94
      00BB9B 2C                    2300 	.db #0x2c	; 44
      00BB9C 7E                    2301 	.db #0x7e	; 126
      00BB9D B1                    2302 	.db #0xb1	; 177
      00BB9E C4                    2303 	.db #0xc4	; 196
      00BB9F 67                    2304 	.db #0x67	; 103	'g'
      00BBA0 FB                    2305 	.db #0xfb	; 251
      00BBA1 02                    2306 	.db #0x02	; 2
      00BBA2 00                    2307 	.db #0x00	; 0
      00BBA3 00                    2308 	.db #0x00	; 0
      00BBA4 00                    2309 	.db #0x00	; 0
      00BBA5 00                    2310 	.db #0x00	; 0
      00BBA6 04                    2311 	.db #0x04	; 4
      00BBA7 59                    2312 	.db #0x59	; 89	'Y'
      00BBA8 5A                    2313 	.db #0x5a	; 90	'Z'
                                   2314 	.area CSEG    (CODE)
                                   2315 	.area CONST   (CODE)
      00BBA9                       2316 _vial_handle_cmd_keyboard_uid_40000_606:
      00BBA9 04                    2317 	.db #0x04	; 4
      00BBAA 70                    2318 	.db #0x70	; 112	'p'
      00BBAB FF                    2319 	.db #0xff	; 255
      00BBAC 90                    2320 	.db #0x90	; 144
      00BBAD 01                    2321 	.db #0x01	; 1
      00BBAE B9                    2322 	.db #0xb9	; 185
      00BBAF 15                    2323 	.db #0x15	; 21
      00BBB0 D3                    2324 	.db #0xd3	; 211
                                   2325 	.area CSEG    (CODE)
                                   2326 	.area XINIT   (CODE)
      00BDE5                       2327 __xinit__vial_unlocked:
      00BDE5 00                    2328 	.db #0x00	;  0
      00BDE6                       2329 __xinit__vial_unlock_in_progress:
      00BDE6 00                    2330 	.db #0x00	;  0
      00BDE7                       2331 __xinit__vial_unlock_counter:
      00BDE7 00                    2332 	.db #0x00	; 0
      00BDE8                       2333 __xinit__vial_unlock_combo_rows:
      00BDE8 00                    2334 	.db #0x00	; 0
      00BDE9 00                    2335 	.db #0x00	; 0
      00BDEA                       2336 __xinit__vial_unlock_combo_cols:
      00BDEA 00                    2337 	.db #0x00	; 0
      00BDEB 05                    2338 	.db #0x05	; 5
                                   2339 	.area CABS    (ABS,CODE)
                                   2340 
                                   2341 ; Experimental exact instruction outlining.
                                   2342 	.globl _ak820_outline_0006
                                   2343 	.globl _ak820_outline_0008
                                   2344 	.globl _ak820_outline_0010
                                   2345 	.globl _ak820_outline_0012
                                   2346 	.globl _ak820_outline_0013
                                   2347 	.globl _ak820_outline_0016
                                   2348 	.globl _ak820_outline_0026
                                   2349 
                                   2350 	.area CSEG (CODE)
                                   2351 ; function ak820_outline_0016
      00AE58                       2352 _ak820_outline_0016:
      00AE58 E0               [24] 2353 	movx	a,@dptr
      00AE59 FE               [12] 2354 	mov	r6,a
      00AE5A A3               [24] 2355 	inc	dptr
      00AE5B E0               [24] 2356 	movx	a,@dptr
      00AE5C FF               [12] 2357 	mov	r7,a
      00AE5D 90 0A 68         [24] 2358 	mov	dptr,#_g_vial_magic_keycode_override
      00AE60 EE               [12] 2359 	mov	a,r6
      00AE61 F0               [24] 2360 	movx	@dptr,a
      00AE62 EF               [12] 2361 	mov	a,r7
      00AE63 A3               [24] 2362 	inc	dptr
      00AE64 F0               [24] 2363 	movx	@dptr,a
      00AE65 8E 04            [24] 2364 	mov	ar4,r6
      00AE67 8F 05            [24] 2365 	mov	ar5,r7
      00AE69 C3               [12] 2366 	clr	c
      00AE6A 74 FF            [12] 2367 	mov	a,#0xff
      00AE6C 9C               [12] 2368 	subb	a,r4
      00AE6D 74 1F            [12] 2369 	mov	a,#0x1f
      00AE6F 9D               [12] 2370 	subb	a,r5
      00AE70 22               [24] 2371 	ret
                                   2372 
                                   2373 	.area CSEG (CODE)
                                   2374 ; function ak820_outline_0026
      00AE71                       2375 _ak820_outline_0026:
      00AE71 A3               [24] 2376 	inc	dptr
      00AE72 F0               [24] 2377 	movx	@dptr,a
      00AE73 E4               [12] 2378 	clr	a
      00AE74 A3               [24] 2379 	inc	dptr
      00AE75 F0               [24] 2380 	movx	@dptr,a
      00AE76 90 0B 93         [24] 2381 	mov	dptr,#___memcpy_PARM_3
      00AE79 74 06            [12] 2382 	mov	a,#0x06
      00AE7B F0               [24] 2383 	movx	@dptr,a
      00AE7C E4               [12] 2384 	clr	a
      00AE7D A3               [24] 2385 	inc	dptr
      00AE7E F0               [24] 2386 	movx	@dptr,a
      00AE7F 90 07 3C         [24] 2387 	mov	dptr,#_action_exec_PARM_1
      00AE82 F5 F0            [12] 2388 	mov	b,a
      00AE84 22               [24] 2389 	ret
