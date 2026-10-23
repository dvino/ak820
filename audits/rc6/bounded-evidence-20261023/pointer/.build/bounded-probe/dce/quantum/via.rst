                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module via
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _raw_hid_receive_kb
                                     12 	.globl _vialrgb_save
                                     13 	.globl _vialrgb_set_value
                                     14 	.globl _vialrgb_get_value
                                     15 	.globl _ak820_nvm_schema_fault
                                     16 	.globl _raw_hid_send
                                     17 	.globl _dynamic_keymap_macro_send
                                     18 	.globl _dynamic_keymap_macro_reset
                                     19 	.globl _dynamic_keymap_macro_set_buffer
                                     20 	.globl _dynamic_keymap_macro_get_buffer
                                     21 	.globl _dynamic_keymap_macro_get_buffer_size
                                     22 	.globl _dynamic_keymap_macro_get_count
                                     23 	.globl _dynamic_keymap_set_buffer
                                     24 	.globl _dynamic_keymap_get_buffer
                                     25 	.globl _dynamic_keymap_reset
                                     26 	.globl _dynamic_keymap_set_keycode
                                     27 	.globl _dynamic_keymap_get_keycode
                                     28 	.globl _dynamic_keymap_get_layer_count
                                     29 	.globl _vial_handle_cmd
                                     30 	.globl _eeprom_update_byte
                                     31 	.globl _eeprom_read_byte
                                     32 	.globl _bootloader_jump
                                     33 	.globl _timer_read32
                                     34 	.globl _matrix_get_row
                                     35 	.globl _mDelaymS
                                     36 	.globl _ADC_START
                                     37 	.globl _S0_R_FIFO
                                     38 	.globl _S0_T_FIFO
                                     39 	.globl _S0_FREE
                                     40 	.globl _S0_IF_BYTE
                                     41 	.globl _S0_IF_FIRST
                                     42 	.globl _S0_IF_OV
                                     43 	.globl _S0_FST_ACT
                                     44 	.globl _CP_RL2
                                     45 	.globl _C_T2
                                     46 	.globl _TR2
                                     47 	.globl _EXEN2
                                     48 	.globl _TCLK
                                     49 	.globl _RCLK
                                     50 	.globl _EXF2
                                     51 	.globl _CAP1F
                                     52 	.globl _TF2
                                     53 	.globl _RI
                                     54 	.globl _TI
                                     55 	.globl _RB8
                                     56 	.globl _TB8
                                     57 	.globl _REN
                                     58 	.globl _SM2
                                     59 	.globl _SM1
                                     60 	.globl _SM0
                                     61 	.globl _IT0
                                     62 	.globl _IE0
                                     63 	.globl _IT1
                                     64 	.globl _IE1
                                     65 	.globl _TR0
                                     66 	.globl _TF0
                                     67 	.globl _TR1
                                     68 	.globl _TF1
                                     69 	.globl _P4_0
                                     70 	.globl _P4_1
                                     71 	.globl _P4_2
                                     72 	.globl _P4_3
                                     73 	.globl _P4_4
                                     74 	.globl _P4_5
                                     75 	.globl _P4_6
                                     76 	.globl _RXD
                                     77 	.globl _TXD
                                     78 	.globl _INT0
                                     79 	.globl _INT1
                                     80 	.globl _T0
                                     81 	.globl _T1
                                     82 	.globl _MOSI1
                                     83 	.globl _MISO1
                                     84 	.globl _SCK1
                                     85 	.globl _P3_0
                                     86 	.globl _P3_1
                                     87 	.globl _P3_2
                                     88 	.globl _P3_3
                                     89 	.globl _P3_4
                                     90 	.globl _P3_5
                                     91 	.globl _P3_6
                                     92 	.globl _P3_7
                                     93 	.globl _CAP1_
                                     94 	.globl _T2_
                                     95 	.globl _CAP2_
                                     96 	.globl _T2EX_
                                     97 	.globl _RXD1
                                     98 	.globl _TXD1
                                     99 	.globl _P2_0
                                    100 	.globl _P2_1
                                    101 	.globl _P2_2
                                    102 	.globl _P2_3
                                    103 	.globl _P2_4
                                    104 	.globl _P2_5
                                    105 	.globl _P2_6
                                    106 	.globl _P2_7
                                    107 	.globl _AIN0
                                    108 	.globl _AIN1
                                    109 	.globl _AIN2
                                    110 	.globl _AIN3
                                    111 	.globl _AIN4
                                    112 	.globl _AIN5
                                    113 	.globl _AIN6
                                    114 	.globl _AIN7
                                    115 	.globl _CAP1
                                    116 	.globl _T2
                                    117 	.globl _CAP2
                                    118 	.globl _T2EX
                                    119 	.globl _INT0_
                                    120 	.globl _SCS
                                    121 	.globl _MOSI
                                    122 	.globl _MISO
                                    123 	.globl _SCK
                                    124 	.globl _RXD1_
                                    125 	.globl _TXD1_
                                    126 	.globl _P1_0
                                    127 	.globl _P1_1
                                    128 	.globl _P1_2
                                    129 	.globl _P1_3
                                    130 	.globl _P1_4
                                    131 	.globl _P1_5
                                    132 	.globl _P1_6
                                    133 	.globl _P1_7
                                    134 	.globl _AIN8
                                    135 	.globl _AIN9
                                    136 	.globl _AIN10
                                    137 	.globl _AIN11
                                    138 	.globl _AIN12
                                    139 	.globl _AIN13
                                    140 	.globl _RXD_
                                    141 	.globl _TXD_
                                    142 	.globl _SCL0
                                    143 	.globl _SDA0
                                    144 	.globl _P0_0
                                    145 	.globl _P0_1
                                    146 	.globl _P0_2
                                    147 	.globl _P0_3
                                    148 	.globl _P0_4
                                    149 	.globl _P0_5
                                    150 	.globl _P0_6
                                    151 	.globl _P0_7
                                    152 	.globl _IE_SPI0
                                    153 	.globl _IE_USB
                                    154 	.globl _IE_ADC
                                    155 	.globl _IE_UART1
                                    156 	.globl _IE_PWM_I2C
                                    157 	.globl _IE_GPIO
                                    158 	.globl _IE_WDOG
                                    159 	.globl _PX0
                                    160 	.globl _PT0
                                    161 	.globl _PX1
                                    162 	.globl _PT1
                                    163 	.globl _PS
                                    164 	.globl _PT2
                                    165 	.globl _PL_FLAG
                                    166 	.globl _PH_FLAG
                                    167 	.globl _EX0
                                    168 	.globl _ET0
                                    169 	.globl _EX1
                                    170 	.globl _ET1
                                    171 	.globl _ES
                                    172 	.globl _ET2
                                    173 	.globl _E_DIS
                                    174 	.globl _EA
                                    175 	.globl _P
                                    176 	.globl _F1
                                    177 	.globl _OV
                                    178 	.globl _RS0
                                    179 	.globl _RS1
                                    180 	.globl _F0
                                    181 	.globl _AC
                                    182 	.globl _CY
                                    183 	.globl _I2CS_INT_ST
                                    184 	.globl _I2CX_INT
                                    185 	.globl _LED_STATUS
                                    186 	.globl _LED_DMA_H
                                    187 	.globl _LED_DMA_L
                                    188 	.globl _LED_DMA
                                    189 	.globl _LED_PWM_OE
                                    190 	.globl _LED_COMMON
                                    191 	.globl _ADC_CHAN
                                    192 	.globl _ADC_DAT_H
                                    193 	.globl _ADC_DAT_L
                                    194 	.globl _ADC_DAT
                                    195 	.globl _ADC_CTRL
                                    196 	.globl _SPI1_CK_SE
                                    197 	.globl _SPI1_CTRL
                                    198 	.globl _SPI1_DATA
                                    199 	.globl _SPI1_STAT
                                    200 	.globl _SIF1
                                    201 	.globl _SBAUD1
                                    202 	.globl _SBUF1
                                    203 	.globl _SCON1
                                    204 	.globl _SPI0_SETUP
                                    205 	.globl _SPI0_CK_SE
                                    206 	.globl _SPI0_CTRL
                                    207 	.globl _SPI0_DATA
                                    208 	.globl _SPI0_STAT
                                    209 	.globl _T2CAP1H
                                    210 	.globl _T2CAP1L
                                    211 	.globl _T2CAP1
                                    212 	.globl _TH2
                                    213 	.globl _TL2
                                    214 	.globl _T2COUNT
                                    215 	.globl _RCAP2H
                                    216 	.globl _RCAP2L
                                    217 	.globl _RCAP2
                                    218 	.globl _T2MOD
                                    219 	.globl _T2CON
                                    220 	.globl _SBUF
                                    221 	.globl _SCON
                                    222 	.globl _TH1
                                    223 	.globl _TH0
                                    224 	.globl _TL1
                                    225 	.globl _TL0
                                    226 	.globl _TMOD
                                    227 	.globl _TCON
                                    228 	.globl _XBUS_AUX
                                    229 	.globl _P7
                                    230 	.globl _P6_DIR
                                    231 	.globl _P6_OUT_PU
                                    232 	.globl _P6_IN
                                    233 	.globl _P5_DIR
                                    234 	.globl _P5_OUT_PU
                                    235 	.globl _P5_IN
                                    236 	.globl _P4_LED_KEY
                                    237 	.globl _P4_DIR_PU
                                    238 	.globl _P4_MOD_OC
                                    239 	.globl _P4
                                    240 	.globl _P3_DIR_PU
                                    241 	.globl _P3_MOD_OC
                                    242 	.globl _P3
                                    243 	.globl _P2_DIR_PU
                                    244 	.globl _P2_MOD_OC
                                    245 	.globl _P2
                                    246 	.globl _P1_DIR_PU
                                    247 	.globl _P1_MOD_OC
                                    248 	.globl _P1
                                    249 	.globl _P0_DIR_PU
                                    250 	.globl _P0_MOD_OC
                                    251 	.globl _P0
                                    252 	.globl _ROM_CTRL
                                    253 	.globl _ROM_DATA_HH
                                    254 	.globl _ROM_DATA_HL
                                    255 	.globl _ROM_DATA_HI
                                    256 	.globl _ROM_ADDR_H
                                    257 	.globl _ROM_ADDR_L
                                    258 	.globl _ROM_ADDR
                                    259 	.globl _GPIO_IE
                                    260 	.globl _IP_EX
                                    261 	.globl _IE_EX
                                    262 	.globl _IP
                                    263 	.globl _IE
                                    264 	.globl _WDOG_COUNT
                                    265 	.globl _RESET_KEEP
                                    266 	.globl _WAKE_CTRL
                                    267 	.globl _CLOCK_CFG
                                    268 	.globl _POWER_CFG
                                    269 	.globl _PCON
                                    270 	.globl _GLOBAL_CFG
                                    271 	.globl _SAFE_MOD
                                    272 	.globl _DPH
                                    273 	.globl _DPL
                                    274 	.globl _SP
                                    275 	.globl _A_INV
                                    276 	.globl _B
                                    277 	.globl _ACC
                                    278 	.globl _PSW
                                    279 	.globl _raw_hid_receive_PARM_2
                                    280 	.globl _raw_hid_receive_kb_PARM_2
                                    281 	.globl _process_record_via_PARM_2
                                    282 	.globl _via_eeprom_is_valid
                                    283 	.globl _via_eeprom_set_valid
                                    284 	.globl _via_init
                                    285 	.globl _eeconfig_init_via
                                    286 	.globl _via_get_layout_options
                                    287 	.globl _via_set_layout_options_kb
                                    288 	.globl _via_set_layout_options
                                    289 	.globl _process_record_via
                                    290 	.globl _raw_hid_receive
                                    291 ;--------------------------------------------------------
                                    292 ; special function registers
                                    293 ;--------------------------------------------------------
                                    294 	.area RSEG    (ABS,DATA)
      000000                        295 	.org 0x0000
                           0000D0   296 _PSW	=	0x00d0
                           0000E0   297 _ACC	=	0x00e0
                           0000F0   298 _B	=	0x00f0
                           0000FD   299 _A_INV	=	0x00fd
                           000081   300 _SP	=	0x0081
                           000082   301 _DPL	=	0x0082
                           000083   302 _DPH	=	0x0083
                           0000A1   303 _SAFE_MOD	=	0x00a1
                           0000B1   304 _GLOBAL_CFG	=	0x00b1
                           000087   305 _PCON	=	0x0087
                           0000BA   306 _POWER_CFG	=	0x00ba
                           0000B9   307 _CLOCK_CFG	=	0x00b9
                           0000A9   308 _WAKE_CTRL	=	0x00a9
                           0000FE   309 _RESET_KEEP	=	0x00fe
                           0000FF   310 _WDOG_COUNT	=	0x00ff
                           0000A8   311 _IE	=	0x00a8
                           0000B8   312 _IP	=	0x00b8
                           0000E8   313 _IE_EX	=	0x00e8
                           0000E9   314 _IP_EX	=	0x00e9
                           0000B2   315 _GPIO_IE	=	0x00b2
                           008584   316 _ROM_ADDR	=	0x8584
                           000084   317 _ROM_ADDR_L	=	0x0084
                           000085   318 _ROM_ADDR_H	=	0x0085
                           008F8E   319 _ROM_DATA_HI	=	0x8f8e
                           00008E   320 _ROM_DATA_HL	=	0x008e
                           00008F   321 _ROM_DATA_HH	=	0x008f
                           000086   322 _ROM_CTRL	=	0x0086
                           000080   323 _P0	=	0x0080
                           0000C4   324 _P0_MOD_OC	=	0x00c4
                           0000C5   325 _P0_DIR_PU	=	0x00c5
                           000090   326 _P1	=	0x0090
                           000092   327 _P1_MOD_OC	=	0x0092
                           000093   328 _P1_DIR_PU	=	0x0093
                           0000A0   329 _P2	=	0x00a0
                           000094   330 _P2_MOD_OC	=	0x0094
                           000095   331 _P2_DIR_PU	=	0x0095
                           0000B0   332 _P3	=	0x00b0
                           000096   333 _P3_MOD_OC	=	0x0096
                           000097   334 _P3_DIR_PU	=	0x0097
                           0000C0   335 _P4	=	0x00c0
                           0000C2   336 _P4_MOD_OC	=	0x00c2
                           0000C3   337 _P4_DIR_PU	=	0x00c3
                           0000C1   338 _P4_LED_KEY	=	0x00c1
                           0000AA   339 _P5_IN	=	0x00aa
                           0000AB   340 _P5_OUT_PU	=	0x00ab
                           0000AC   341 _P5_DIR	=	0x00ac
                           0000AD   342 _P6_IN	=	0x00ad
                           0000AE   343 _P6_OUT_PU	=	0x00ae
                           0000AF   344 _P6_DIR	=	0x00af
                           0000F1   345 _P7	=	0x00f1
                           0000A2   346 _XBUS_AUX	=	0x00a2
                           000088   347 _TCON	=	0x0088
                           000089   348 _TMOD	=	0x0089
                           00008A   349 _TL0	=	0x008a
                           00008B   350 _TL1	=	0x008b
                           00008C   351 _TH0	=	0x008c
                           00008D   352 _TH1	=	0x008d
                           000098   353 _SCON	=	0x0098
                           000099   354 _SBUF	=	0x0099
                           0000C8   355 _T2CON	=	0x00c8
                           0000C9   356 _T2MOD	=	0x00c9
                           00CBCA   357 _RCAP2	=	0xcbca
                           0000CA   358 _RCAP2L	=	0x00ca
                           0000CB   359 _RCAP2H	=	0x00cb
                           00CDCC   360 _T2COUNT	=	0xcdcc
                           0000CC   361 _TL2	=	0x00cc
                           0000CD   362 _TH2	=	0x00cd
                           00CFCE   363 _T2CAP1	=	0xcfce
                           0000CE   364 _T2CAP1L	=	0x00ce
                           0000CF   365 _T2CAP1H	=	0x00cf
                           0000F8   366 _SPI0_STAT	=	0x00f8
                           0000F9   367 _SPI0_DATA	=	0x00f9
                           0000FA   368 _SPI0_CTRL	=	0x00fa
                           0000FB   369 _SPI0_CK_SE	=	0x00fb
                           0000FC   370 _SPI0_SETUP	=	0x00fc
                           0000BC   371 _SCON1	=	0x00bc
                           0000BD   372 _SBUF1	=	0x00bd
                           0000BE   373 _SBAUD1	=	0x00be
                           0000BF   374 _SIF1	=	0x00bf
                           0000B4   375 _SPI1_STAT	=	0x00b4
                           0000B5   376 _SPI1_DATA	=	0x00b5
                           0000B6   377 _SPI1_CTRL	=	0x00b6
                           0000B7   378 _SPI1_CK_SE	=	0x00b7
                           0000F3   379 _ADC_CTRL	=	0x00f3
                           00F5F4   380 _ADC_DAT	=	0xf5f4
                           0000F4   381 _ADC_DAT_L	=	0x00f4
                           0000F5   382 _ADC_DAT_H	=	0x00f5
                           0000F6   383 _ADC_CHAN	=	0x00f6
                           0000A6   384 _LED_COMMON	=	0x00a6
                           0000A7   385 _LED_PWM_OE	=	0x00a7
                           00C7C6   386 _LED_DMA	=	0xc7c6
                           0000C6   387 _LED_DMA_L	=	0x00c6
                           0000C7   388 _LED_DMA_H	=	0x00c7
                           0000F7   389 _LED_STATUS	=	0x00f7
                           0000B3   390 _I2CX_INT	=	0x00b3
                           0000BB   391 _I2CS_INT_ST	=	0x00bb
                                    392 ;--------------------------------------------------------
                                    393 ; special function bits
                                    394 ;--------------------------------------------------------
                                    395 	.area RSEG    (ABS,DATA)
      000000                        396 	.org 0x0000
                           0000D7   397 _CY	=	0x00d7
                           0000D6   398 _AC	=	0x00d6
                           0000D5   399 _F0	=	0x00d5
                           0000D4   400 _RS1	=	0x00d4
                           0000D3   401 _RS0	=	0x00d3
                           0000D2   402 _OV	=	0x00d2
                           0000D1   403 _F1	=	0x00d1
                           0000D0   404 _P	=	0x00d0
                           0000AF   405 _EA	=	0x00af
                           0000AE   406 _E_DIS	=	0x00ae
                           0000AD   407 _ET2	=	0x00ad
                           0000AC   408 _ES	=	0x00ac
                           0000AB   409 _ET1	=	0x00ab
                           0000AA   410 _EX1	=	0x00aa
                           0000A9   411 _ET0	=	0x00a9
                           0000A8   412 _EX0	=	0x00a8
                           0000BF   413 _PH_FLAG	=	0x00bf
                           0000BE   414 _PL_FLAG	=	0x00be
                           0000BD   415 _PT2	=	0x00bd
                           0000BC   416 _PS	=	0x00bc
                           0000BB   417 _PT1	=	0x00bb
                           0000BA   418 _PX1	=	0x00ba
                           0000B9   419 _PT0	=	0x00b9
                           0000B8   420 _PX0	=	0x00b8
                           0000EF   421 _IE_WDOG	=	0x00ef
                           0000EE   422 _IE_GPIO	=	0x00ee
                           0000ED   423 _IE_PWM_I2C	=	0x00ed
                           0000EC   424 _IE_UART1	=	0x00ec
                           0000EB   425 _IE_ADC	=	0x00eb
                           0000E9   426 _IE_USB	=	0x00e9
                           0000E8   427 _IE_SPI0	=	0x00e8
                           000087   428 _P0_7	=	0x0087
                           000086   429 _P0_6	=	0x0086
                           000085   430 _P0_5	=	0x0085
                           000084   431 _P0_4	=	0x0084
                           000083   432 _P0_3	=	0x0083
                           000082   433 _P0_2	=	0x0082
                           000081   434 _P0_1	=	0x0081
                           000080   435 _P0_0	=	0x0080
                           000081   436 _SDA0	=	0x0081
                           000080   437 _SCL0	=	0x0080
                           000083   438 _TXD_	=	0x0083
                           000082   439 _RXD_	=	0x0082
                           000085   440 _AIN13	=	0x0085
                           000084   441 _AIN12	=	0x0084
                           000083   442 _AIN11	=	0x0083
                           000082   443 _AIN10	=	0x0082
                           000081   444 _AIN9	=	0x0081
                           000080   445 _AIN8	=	0x0080
                           000097   446 _P1_7	=	0x0097
                           000096   447 _P1_6	=	0x0096
                           000095   448 _P1_5	=	0x0095
                           000094   449 _P1_4	=	0x0094
                           000093   450 _P1_3	=	0x0093
                           000092   451 _P1_2	=	0x0092
                           000091   452 _P1_1	=	0x0091
                           000090   453 _P1_0	=	0x0090
                           000097   454 _TXD1_	=	0x0097
                           000096   455 _RXD1_	=	0x0096
                           000097   456 _SCK	=	0x0097
                           000096   457 _MISO	=	0x0096
                           000095   458 _MOSI	=	0x0095
                           000094   459 _SCS	=	0x0094
                           000092   460 _INT0_	=	0x0092
                           000091   461 _T2EX	=	0x0091
                           000091   462 _CAP2	=	0x0091
                           000090   463 _T2	=	0x0090
                           000090   464 _CAP1	=	0x0090
                           000097   465 _AIN7	=	0x0097
                           000096   466 _AIN6	=	0x0096
                           000095   467 _AIN5	=	0x0095
                           000094   468 _AIN4	=	0x0094
                           000093   469 _AIN3	=	0x0093
                           000092   470 _AIN2	=	0x0092
                           000091   471 _AIN1	=	0x0091
                           000090   472 _AIN0	=	0x0090
                           0000A7   473 _P2_7	=	0x00a7
                           0000A6   474 _P2_6	=	0x00a6
                           0000A5   475 _P2_5	=	0x00a5
                           0000A4   476 _P2_4	=	0x00a4
                           0000A3   477 _P2_3	=	0x00a3
                           0000A2   478 _P2_2	=	0x00a2
                           0000A1   479 _P2_1	=	0x00a1
                           0000A0   480 _P2_0	=	0x00a0
                           0000A7   481 _TXD1	=	0x00a7
                           0000A6   482 _RXD1	=	0x00a6
                           0000A5   483 _T2EX_	=	0x00a5
                           0000A5   484 _CAP2_	=	0x00a5
                           0000A4   485 _T2_	=	0x00a4
                           0000A4   486 _CAP1_	=	0x00a4
                           0000B7   487 _P3_7	=	0x00b7
                           0000B6   488 _P3_6	=	0x00b6
                           0000B5   489 _P3_5	=	0x00b5
                           0000B4   490 _P3_4	=	0x00b4
                           0000B3   491 _P3_3	=	0x00b3
                           0000B2   492 _P3_2	=	0x00b2
                           0000B1   493 _P3_1	=	0x00b1
                           0000B0   494 _P3_0	=	0x00b0
                           0000B7   495 _SCK1	=	0x00b7
                           0000B6   496 _MISO1	=	0x00b6
                           0000B5   497 _MOSI1	=	0x00b5
                           0000B5   498 _T1	=	0x00b5
                           0000B4   499 _T0	=	0x00b4
                           0000B3   500 _INT1	=	0x00b3
                           0000B2   501 _INT0	=	0x00b2
                           0000B1   502 _TXD	=	0x00b1
                           0000B0   503 _RXD	=	0x00b0
                           0000C6   504 _P4_6	=	0x00c6
                           0000C5   505 _P4_5	=	0x00c5
                           0000C4   506 _P4_4	=	0x00c4
                           0000C3   507 _P4_3	=	0x00c3
                           0000C2   508 _P4_2	=	0x00c2
                           0000C1   509 _P4_1	=	0x00c1
                           0000C0   510 _P4_0	=	0x00c0
                           00008F   511 _TF1	=	0x008f
                           00008E   512 _TR1	=	0x008e
                           00008D   513 _TF0	=	0x008d
                           00008C   514 _TR0	=	0x008c
                           00008B   515 _IE1	=	0x008b
                           00008A   516 _IT1	=	0x008a
                           000089   517 _IE0	=	0x0089
                           000088   518 _IT0	=	0x0088
                           00009F   519 _SM0	=	0x009f
                           00009E   520 _SM1	=	0x009e
                           00009D   521 _SM2	=	0x009d
                           00009C   522 _REN	=	0x009c
                           00009B   523 _TB8	=	0x009b
                           00009A   524 _RB8	=	0x009a
                           000099   525 _TI	=	0x0099
                           000098   526 _RI	=	0x0098
                           0000CF   527 _TF2	=	0x00cf
                           0000CF   528 _CAP1F	=	0x00cf
                           0000CE   529 _EXF2	=	0x00ce
                           0000CD   530 _RCLK	=	0x00cd
                           0000CC   531 _TCLK	=	0x00cc
                           0000CB   532 _EXEN2	=	0x00cb
                           0000CA   533 _TR2	=	0x00ca
                           0000C9   534 _C_T2	=	0x00c9
                           0000C8   535 _CP_RL2	=	0x00c8
                           0000FF   536 _S0_FST_ACT	=	0x00ff
                           0000FE   537 _S0_IF_OV	=	0x00fe
                           0000FD   538 _S0_IF_FIRST	=	0x00fd
                           0000FC   539 _S0_IF_BYTE	=	0x00fc
                           0000FB   540 _S0_FREE	=	0x00fb
                           0000FA   541 _S0_T_FIFO	=	0x00fa
                           0000F8   542 _S0_R_FIFO	=	0x00f8
                           0000F7   543 _ADC_START	=	0x00f7
                                    544 ;--------------------------------------------------------
                                    545 ; overlayable register banks
                                    546 ;--------------------------------------------------------
                                    547 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        548 	.ds 8
                                    549 ;--------------------------------------------------------
                                    550 ; internal ram data
                                    551 ;--------------------------------------------------------
                                    552 	.area DSEG    (DATA)
      000041                        553 _raw_hid_receive_sloc0_1_0:
      000041                        554 	.ds 4
      000045                        555 _raw_hid_receive_sloc1_1_0:
      000045                        556 	.ds 1
      000046                        557 _raw_hid_receive_sloc2_1_0:
      000046                        558 	.ds 1
      000047                        559 _raw_hid_receive_sloc3_1_0:
      000047                        560 	.ds 2
      000049                        561 _raw_hid_receive_sloc4_1_0:
      000049                        562 	.ds 2
                                    563 ;--------------------------------------------------------
                                    564 ; overlayable items in internal ram
                                    565 ;--------------------------------------------------------
                                    566 ;--------------------------------------------------------
                                    567 ; indirectly addressable internal ram data
                                    568 ;--------------------------------------------------------
                                    569 	.area ISEG    (DATA)
                                    570 ;--------------------------------------------------------
                                    571 ; absolute internal ram data
                                    572 ;--------------------------------------------------------
                                    573 	.area IABS    (ABS,DATA)
                                    574 	.area IABS    (ABS,DATA)
                                    575 ;--------------------------------------------------------
                                    576 ; bit data
                                    577 ;--------------------------------------------------------
                                    578 	.area BSEG    (BIT)
      000010                        579 _via_eeprom_is_valid_sloc0_1_0:
      000010                        580 	.ds 1
                                    581 ;--------------------------------------------------------
                                    582 ; paged external ram data
                                    583 ;--------------------------------------------------------
                                    584 	.area PSEG    (PAG,XDATA)
                                    585 ;--------------------------------------------------------
                                    586 ; uninitialized external ram data
                                    587 ;--------------------------------------------------------
                                    588 	.area XSEG    (XDATA)
      000A45                        589 _via_eeprom_set_valid_valid_10000_582:
      000A45                        590 	.ds 1
      000A46                        591 _via_set_layout_options_value_10000_598:
      000A46                        592 	.ds 4
      000A4A                        593 _process_record_via_PARM_2:
      000A4A                        594 	.ds 3
      000A4D                        595 _process_record_via_keycode_10000_600:
      000A4D                        596 	.ds 2
      000A4F                        597 _raw_hid_receive_kb_PARM_2:
      000A4F                        598 	.ds 1
      000A50                        599 _raw_hid_receive_kb_data_10000_606:
      000A50                        600 	.ds 3
      000A53                        601 _raw_hid_receive_PARM_2:
      000A53                        602 	.ds 1
      000A54                        603 _raw_hid_receive_packet_10000_608:
      000A54                        604 	.ds 3
                                    605 ;--------------------------------------------------------
                                    606 ; absolute external ram data
                                    607 ;--------------------------------------------------------
                                    608 	.area XABS    (ABS,XDATA)
                                    609 ;--------------------------------------------------------
                                    610 ; initialized external ram data
                                    611 ;--------------------------------------------------------
                                    612 	.area XISEG   (XDATA)
                                    613 	.area HOME    (CODE)
                                    614 	.area GSINIT0 (CODE)
                                    615 	.area GSINIT1 (CODE)
                                    616 	.area GSINIT2 (CODE)
                                    617 	.area GSINIT3 (CODE)
                                    618 	.area GSINIT4 (CODE)
                                    619 	.area GSINIT5 (CODE)
                                    620 	.area GSINIT  (CODE)
                                    621 	.area GSFINAL (CODE)
                                    622 	.area CSEG    (CODE)
                                    623 ;--------------------------------------------------------
                                    624 ; global & static initialisations
                                    625 ;--------------------------------------------------------
                                    626 	.area HOME    (CODE)
                                    627 	.area GSINIT  (CODE)
                                    628 	.area GSFINAL (CODE)
                                    629 	.area GSINIT  (CODE)
                                    630 ;--------------------------------------------------------
                                    631 ; Home
                                    632 ;--------------------------------------------------------
                                    633 	.area HOME    (CODE)
                                    634 	.area HOME    (CODE)
                                    635 ;--------------------------------------------------------
                                    636 ; code
                                    637 ;--------------------------------------------------------
                                    638 	.area CSEG    (CODE)
                                    639 ;------------------------------------------------------------
                                    640 ;Allocation info for local variables in function 'rgb_matrix_check_finished_leds'
                                    641 ;------------------------------------------------------------
                                    642 ;led_idx       Allocated with name '_rgb_matrix_check_finished_leds_led_idx_10000_193'
                                    643 ;------------------------------------------------------------
                                    644 ;	quantum/rgb_matrix/rgb_matrix.h:260: static inline bool rgb_matrix_check_finished_leds(uint8_t led_idx) {
                                    645 ;	-----------------------------------------
                           000007   646 	ar7 = 0x07
                           000006   647 	ar6 = 0x06
                           000005   648 	ar5 = 0x05
                           000004   649 	ar4 = 0x04
                           000003   650 	ar3 = 0x03
                           000002   651 	ar2 = 0x02
                           000001   652 	ar1 = 0x01
                           000000   653 	ar0 = 0x00
                                    654 ;	 function via_eeprom_is_valid
                                    655 ;	-----------------------------------------
      00A031                        656 _via_eeprom_is_valid:
                                    657 ;	quantum/via.c:103: return (eeprom_read_byte((uint8_t *)VIA_EEPROM_MAGIC_ADDR + 0) == magic0 && eeprom_read_byte((uint8_t *)VIA_EEPROM_MAGIC_ADDR + 1) == magic1 && eeprom_read_byte((uint8_t *)VIA_EEPROM_MAGIC_ADDR + 2) == magic2);
      00A031 90 00 25         [24]  658 	mov	dptr,#0x0025
      00A034 75 F0 00         [24]  659 	mov	b, #0x00
      00A037 12 43 FC         [24]  660 	lcall	_eeprom_read_byte
      00A03A AF 82            [24]  661 	mov	r7, dpl
      00A03C BF 02 1E         [24]  662 	cjne	r7,#0x02,00103$
      00A03F 90 00 26         [24]  663 	mov	dptr,#0x0026
      00A042 75 F0 00         [24]  664 	mov	b, #0x00
      00A045 12 43 FC         [24]  665 	lcall	_eeprom_read_byte
      00A048 AF 82            [24]  666 	mov	r7, dpl
      00A04A BF 20 10         [24]  667 	cjne	r7,#0x20,00103$
      00A04D 90 00 27         [24]  668 	mov	dptr,#0x0027
      00A050 75 F0 00         [24]  669 	mov	b, #0x00
      00A053 12 43 FC         [24]  670 	lcall	_eeprom_read_byte
      00A056 AF 82            [24]  671 	mov	r7, dpl
      00A058 BF 08 02         [24]  672 	cjne	r7,#0x08,00126$
      00A05B 80 04            [24]  673 	sjmp	00104$
      00A05D                        674 00126$:
      00A05D                        675 00103$:
                                    676 ;	assignBit
      00A05D C2 10            [12]  677 	clr	_via_eeprom_is_valid_sloc0_1_0
      00A05F 80 02            [24]  678 	sjmp	00105$
      00A061                        679 00104$:
                                    680 ;	assignBit
      00A061 D2 10            [12]  681 	setb	_via_eeprom_is_valid_sloc0_1_0
      00A063                        682 00105$:
      00A063 A2 10            [12]  683 	mov	c,_via_eeprom_is_valid_sloc0_1_0
      00A065 E4               [12]  684 	clr	a
      00A066 33               [12]  685 	rlc	a
      00A067 F5 82            [12]  686 	mov	dpl, a
                                    687 ;	quantum/via.c:104: }
      00A069 22               [24]  688 	ret
                                    689 ;------------------------------------------------------------
                                    690 ;Allocation info for local variables in function 'via_eeprom_set_valid'
                                    691 ;------------------------------------------------------------
                                    692 ;valid         Allocated with name '_via_eeprom_set_valid_valid_10000_582'
                                    693 ;magic0        Allocated with name '_via_eeprom_set_valid_magic0_10000_583'
                                    694 ;magic1        Allocated with name '_via_eeprom_set_valid_magic1_10000_583'
                                    695 ;magic2        Allocated with name '_via_eeprom_set_valid_magic2_10000_583'
                                    696 ;------------------------------------------------------------
                                    697 ;	quantum/via.c:108: void via_eeprom_set_valid(__xdata bool valid) {
                                    698 ;	-----------------------------------------
                                    699 ;	 function via_eeprom_set_valid
                                    700 ;	-----------------------------------------
      00A06A                        701 _via_eeprom_set_valid:
      00A06A E5 82            [12]  702 	mov	a,dpl
      00A06C 90 0A 45         [24]  703 	mov	dptr,#_via_eeprom_set_valid_valid_10000_582
      00A06F F0               [24]  704 	movx	@dptr,a
                                    705 ;	quantum/via.c:120: eeprom_update_byte((uint8_t *)VIA_EEPROM_MAGIC_ADDR + 0, valid ? magic0 : 0xFF);
      00A070 E0               [24]  706 	movx	a,@dptr
      00A071 60 04            [24]  707 	jz	00103$
      00A073 7F 02            [12]  708 	mov	r7,#0x02
      00A075 80 02            [24]  709 	sjmp	00104$
      00A077                        710 00103$:
      00A077 7F FF            [12]  711 	mov	r7,#0xff
      00A079                        712 00104$:
      00A079 90 05 B8         [24]  713 	mov	dptr,#_eeprom_update_byte_PARM_2
      00A07C EF               [12]  714 	mov	a,r7
      00A07D F0               [24]  715 	movx	@dptr,a
      00A07E 90 00 25         [24]  716 	mov	dptr,#0x0025
      00A081 75 F0 00         [24]  717 	mov	b, #0x00
      00A084 12 46 5D         [24]  718 	lcall	_eeprom_update_byte
                                    719 ;	quantum/via.c:121: eeprom_update_byte((uint8_t *)VIA_EEPROM_MAGIC_ADDR + 1, valid ? magic1 : 0xFF);
      00A087 90 0A 45         [24]  720 	mov	dptr,#_via_eeprom_set_valid_valid_10000_582
      00A08A E0               [24]  721 	movx	a,@dptr
      00A08B 60 04            [24]  722 	jz	00105$
      00A08D 7F 20            [12]  723 	mov	r7,#0x20
      00A08F 80 02            [24]  724 	sjmp	00106$
      00A091                        725 00105$:
      00A091 7F FF            [12]  726 	mov	r7,#0xff
      00A093                        727 00106$:
      00A093 90 05 B8         [24]  728 	mov	dptr,#_eeprom_update_byte_PARM_2
      00A096 EF               [12]  729 	mov	a,r7
      00A097 F0               [24]  730 	movx	@dptr,a
      00A098 90 00 26         [24]  731 	mov	dptr,#0x0026
      00A09B 75 F0 00         [24]  732 	mov	b, #0x00
      00A09E 12 46 5D         [24]  733 	lcall	_eeprom_update_byte
                                    734 ;	quantum/via.c:122: eeprom_update_byte((uint8_t *)VIA_EEPROM_MAGIC_ADDR + 2, valid ? magic2 : 0xFF);
      00A0A1 90 0A 45         [24]  735 	mov	dptr,#_via_eeprom_set_valid_valid_10000_582
      00A0A4 E0               [24]  736 	movx	a,@dptr
      00A0A5 60 04            [24]  737 	jz	00107$
      00A0A7 7F 08            [12]  738 	mov	r7,#0x08
      00A0A9 80 02            [24]  739 	sjmp	00108$
      00A0AB                        740 00107$:
      00A0AB 7F FF            [12]  741 	mov	r7,#0xff
      00A0AD                        742 00108$:
      00A0AD 90 05 B8         [24]  743 	mov	dptr,#_eeprom_update_byte_PARM_2
      00A0B0 EF               [12]  744 	mov	a,r7
      00A0B1 F0               [24]  745 	movx	@dptr,a
      00A0B2 90 00 27         [24]  746 	mov	dptr,#0x0027
      00A0B5 75 F0 00         [24]  747 	mov	b, #0x00
                                    748 ;	quantum/via.c:123: }
      00A0B8 02 46 5D         [24]  749 	ljmp	_eeprom_update_byte
                                    750 ;------------------------------------------------------------
                                    751 ;Allocation info for local variables in function 'via_init_kb'
                                    752 ;------------------------------------------------------------
                                    753 ;	quantum/via.c:131: __attribute__((weak)) void via_init_kb(void) {}
                                    754 ;	-----------------------------------------
                                    755 ;	 function via_init
                                    756 ;	-----------------------------------------
      00A0BB                        757 _via_init:
                                    758 ;	quantum/via.c:138: via_set_layout_options_kb(via_get_layout_options());
      00A0BB 12 A0 E7         [24]  759 	lcall	_via_get_layout_options
      00A0BE 12 A1 00         [24]  760 	lcall	_via_set_layout_options_kb
                                    761 ;	quantum/via.c:142: if (!via_eeprom_is_valid()) {
      00A0C1 12 A0 31         [24]  762 	lcall	_via_eeprom_is_valid
      00A0C4 E5 82            [12]  763 	mov	a, dpl
      00A0C6 70 03            [24]  764 	jnz	00103$
                                    765 ;	quantum/via.c:147: ak820_nvm_schema_fault();
                                    766 ;	quantum/via.c:152: }
      00A0C8 02 3A C5         [24]  767 	ljmp	_ak820_nvm_schema_fault
      00A0CB                        768 00103$:
      00A0CB 22               [24]  769 	ret
                                    770 ;------------------------------------------------------------
                                    771 ;Allocation info for local variables in function 'eeconfig_init_via'
                                    772 ;------------------------------------------------------------
                                    773 ;	quantum/via.c:154: void eeconfig_init_via(void) {
                                    774 ;	-----------------------------------------
                                    775 ;	 function eeconfig_init_via
                                    776 ;	-----------------------------------------
      00A0CC                        777 _eeconfig_init_via:
                                    778 ;	quantum/via.c:156: via_eeprom_set_valid(false);
      00A0CC 75 82 00         [24]  779 	mov	dpl, #0x00
      00A0CF 12 A0 6A         [24]  780 	lcall	_via_eeprom_set_valid
                                    781 ;	quantum/via.c:158: via_set_layout_options(VIA_EEPROM_LAYOUT_OPTIONS_DEFAULT);
      00A0D2 90 00 00         [24]  782 	mov	dptr,#0x0000
      00A0D5 E4               [12]  783 	clr	a
      00A0D6 F5 F0            [12]  784 	mov	b,a
      00A0D8 12 A1 01         [24]  785 	lcall	_via_set_layout_options
                                    786 ;	quantum/via.c:160: dynamic_keymap_reset();
      00A0DB 12 7D 9D         [24]  787 	lcall	_dynamic_keymap_reset
                                    788 ;	quantum/via.c:162: dynamic_keymap_macro_reset();
      00A0DE 12 82 94         [24]  789 	lcall	_dynamic_keymap_macro_reset
                                    790 ;	quantum/via.c:164: via_eeprom_set_valid(true);
      00A0E1 75 82 01         [24]  791 	mov	dpl, #0x01
                                    792 ;	quantum/via.c:165: }
      00A0E4 02 A0 6A         [24]  793 	ljmp	_via_eeprom_set_valid
                                    794 ;------------------------------------------------------------
                                    795 ;Allocation info for local variables in function 'via_get_layout_options'
                                    796 ;------------------------------------------------------------
                                    797 ;	quantum/via.c:169: uint32_t via_get_layout_options(void) {
                                    798 ;	-----------------------------------------
                                    799 ;	 function via_get_layout_options
                                    800 ;	-----------------------------------------
      00A0E7                        801 _via_get_layout_options:
                                    802 ;	quantum/via.c:173: return eeprom_read_byte((uint8_t *)VIA_EEPROM_LAYOUT_OPTIONS_ADDR);
      00A0E7 90 00 28         [24]  803 	mov	dptr,#0x0028
      00A0EA 75 F0 00         [24]  804 	mov	b, #0x00
      00A0ED 12 43 FC         [24]  805 	lcall	_eeprom_read_byte
      00A0F0 AF 82            [24]  806 	mov	r7, dpl
      00A0F2 7E 00            [12]  807 	mov	r6,#0x00
      00A0F4 7D 00            [12]  808 	mov	r5,#0x00
      00A0F6 7C 00            [12]  809 	mov	r4,#0x00
      00A0F8 8F 82            [24]  810 	mov	dpl, r7
      00A0FA 8E 83            [24]  811 	mov	dph, r6
      00A0FC 8D F0            [24]  812 	mov	b, r5
      00A0FE EC               [12]  813 	mov	a, r4
                                    814 ;	quantum/via.c:185: }
      00A0FF 22               [24]  815 	ret
                                    816 ;------------------------------------------------------------
                                    817 ;Allocation info for local variables in function 'via_set_layout_options_kb'
                                    818 ;------------------------------------------------------------
                                    819 ;value         Allocated with name '_via_set_layout_options_kb_value_10000_595'
                                    820 ;------------------------------------------------------------
                                    821 ;	quantum/via.c:187: __attribute__((weak)) void via_set_layout_options_kb(uint32_t value) {}
                                    822 ;	-----------------------------------------
                                    823 ;	 function via_set_layout_options_kb
                                    824 ;	-----------------------------------------
      00A100                        825 _via_set_layout_options_kb:
      00A100 22               [24]  826 	ret
                                    827 ;------------------------------------------------------------
                                    828 ;Allocation info for local variables in function 'via_set_layout_options'
                                    829 ;------------------------------------------------------------
                                    830 ;value         Allocated with name '_via_set_layout_options_value_10000_598'
                                    831 ;------------------------------------------------------------
                                    832 ;	quantum/via.c:189: void via_set_layout_options(uint32_t value) {
                                    833 ;	-----------------------------------------
                                    834 ;	 function via_set_layout_options
                                    835 ;	-----------------------------------------
      00A101                        836 _via_set_layout_options:
      00A101 AF 82            [24]  837 	mov	r7,dpl
      00A103 AE 83            [24]  838 	mov	r6,dph
      00A105 AD F0            [24]  839 	mov	r5,b
      00A107 FC               [12]  840 	mov	r4,a
      00A108 90 0A 46         [24]  841 	mov	dptr,#_via_set_layout_options_value_10000_598
      00A10B 12 87 D2         [24]  842 	lcall	_ak820_outline_0028
                                    843 ;	quantum/via.c:192: eeprom_update_byte((uint8_t *)VIA_EEPROM_LAYOUT_OPTIONS_ADDR, (uint8_t)value);
      00A10E 90 0A 46         [24]  844 	mov	dptr,#_via_set_layout_options_value_10000_598
      00A111 E0               [24]  845 	movx	a,@dptr
      00A112 90 05 B8         [24]  846 	mov	dptr,#_eeprom_update_byte_PARM_2
      00A115 F0               [24]  847 	movx	@dptr,a
      00A116 90 00 28         [24]  848 	mov	dptr,#0x0028
      00A119 75 F0 00         [24]  849 	mov	b, #0x00
                                    850 ;	quantum/via.c:202: }
      00A11C 02 46 5D         [24]  851 	ljmp	_eeprom_update_byte
                                    852 ;------------------------------------------------------------
                                    853 ;Allocation info for local variables in function 'process_record_via'
                                    854 ;------------------------------------------------------------
                                    855 ;record        Allocated with name '_process_record_via_PARM_2'
                                    856 ;keycode       Allocated with name '_process_record_via_keycode_10000_600'
                                    857 ;id            Allocated with name '_process_record_via_id_50000_605'
                                    858 ;------------------------------------------------------------
                                    859 ;	quantum/via.c:205: bool process_record_via(uint16_t keycode, keyrecord_t *record) {
                                    860 ;	-----------------------------------------
                                    861 ;	 function process_record_via
                                    862 ;	-----------------------------------------
      00A11F                        863 _process_record_via:
      00A11F AF 83            [24]  864 	mov	r7,dph
      00A121 E5 82            [12]  865 	mov	a,dpl
      00A123 90 0A 4D         [24]  866 	mov	dptr,#_process_record_via_keycode_10000_600
      00A126 F0               [24]  867 	movx	@dptr,a
      00A127 EF               [12]  868 	mov	a,r7
      00A128 A3               [24]  869 	inc	dptr
      00A129 F0               [24]  870 	movx	@dptr,a
                                    871 ;	quantum/via.c:207: if (record->event.pressed) {
      00A12A 90 0A 4A         [24]  872 	mov	dptr,#_process_record_via_PARM_2
      00A12D 12 73 99         [24]  873 	lcall	_ak820_outline_0002
      00A130 12 96 D2         [24]  874 	lcall	_ak820_outline_0018
      00A133 12 B5 78         [24]  875 	lcall	__gptrget
      00A136 60 1D            [24]  876 	jz	00105$
                                    877 ;	quantum/via.c:208: if (keycode >= QK_MACRO && keycode <= QK_MACRO_MAX) {
      00A138 90 0A 4D         [24]  878 	mov	dptr,#_process_record_via_keycode_10000_600
      00A13B 12 86 05         [24]  879 	lcall	_ak820_outline_0012
      00A13E 74 89            [12]  880 	mov	a,#0x100 - 0x77
      00A140 2D               [12]  881 	add	a,r5
      00A141 50 12            [24]  882 	jnc	00105$
      00A143 C3               [12]  883 	clr	c
      00A144 74 7F            [12]  884 	mov	a,#0x7f
      00A146 9C               [12]  885 	subb	a,r4
      00A147 74 77            [12]  886 	mov	a,#0x77
      00A149 9D               [12]  887 	subb	a,r5
      00A14A 40 09            [24]  888 	jc	00105$
                                    889 ;	free result
                                    890 ;	quantum/via.c:209: uint8_t id = keycode - QK_MACRO;
                                    891 ;	quantum/via.c:210: dynamic_keymap_macro_send(id);
      00A14C 8E 82            [24]  892 	mov	dpl, r6
      00A14E 12 82 BE         [24]  893 	lcall	_dynamic_keymap_macro_send
                                    894 ;	quantum/via.c:211: return false;
      00A151 75 82 00         [24]  895 	mov	dpl, #0x00
      00A154 22               [24]  896 	ret
      00A155                        897 00105$:
                                    898 ;	quantum/via.c:215: return true;
      00A155 75 82 01         [24]  899 	mov	dpl, #0x01
                                    900 ;	quantum/via.c:216: }
      00A158 22               [24]  901 	ret
                                    902 ;------------------------------------------------------------
                                    903 ;Allocation info for local variables in function 'raw_hid_receive_kb'
                                    904 ;------------------------------------------------------------
                                    905 ;length        Allocated with name '_raw_hid_receive_kb_PARM_2'
                                    906 ;data          Allocated with name '_raw_hid_receive_kb_data_10000_606'
                                    907 ;command_id    Allocated with name '_raw_hid_receive_kb_command_id_10000_607'
                                    908 ;------------------------------------------------------------
                                    909 ;	quantum/via.c:221: __attribute__((weak)) void raw_hid_receive_kb(uint8_t *data, uint8_t length) {
                                    910 ;	-----------------------------------------
                                    911 ;	 function raw_hid_receive_kb
                                    912 ;	-----------------------------------------
      00A159                        913 _raw_hid_receive_kb:
      00A159 AF F0            [24]  914 	mov	r7,b
      00A15B AE 83            [24]  915 	mov	r6,dph
      00A15D E5 82            [12]  916 	mov	a,dpl
      00A15F 90 0A 50         [24]  917 	mov	dptr,#_raw_hid_receive_kb_data_10000_606
      00A162 F0               [24]  918 	movx	@dptr,a
      00A163 EE               [12]  919 	mov	a,r6
      00A164 A3               [24]  920 	inc	dptr
      00A165 F0               [24]  921 	movx	@dptr,a
      00A166 EF               [12]  922 	mov	a,r7
      00A167 A3               [24]  923 	inc	dptr
      00A168 F0               [24]  924 	movx	@dptr,a
                                    925 ;	quantum/via.c:222: uint8_t *command_id = &(data[0]);
      00A169 90 0A 50         [24]  926 	mov	dptr,#_raw_hid_receive_kb_data_10000_606
      00A16C 12 73 99         [24]  927 	lcall	_ak820_outline_0002
                                    928 ;	quantum/via.c:223: *command_id         = id_unhandled;
      00A16F 8D 82            [24]  929 	mov	dpl,r5
      00A171 8E 83            [24]  930 	mov	dph,r6
      00A173 8F F0            [24]  931 	mov	b,r7
      00A175 74 FF            [12]  932 	mov	a,#0xff
                                    933 ;	quantum/via.c:224: }
      00A177 02 B5 3D         [24]  934 	ljmp	__gptrput
                                    935 ;------------------------------------------------------------
                                    936 ;Allocation info for local variables in function 'raw_hid_receive'
                                    937 ;------------------------------------------------------------
                                    938 ;sloc0         Allocated with name '_raw_hid_receive_sloc0_1_0'
                                    939 ;sloc1         Allocated with name '_raw_hid_receive_sloc1_1_0'
                                    940 ;sloc2         Allocated with name '_raw_hid_receive_sloc2_1_0'
                                    941 ;sloc3         Allocated with name '_raw_hid_receive_sloc3_1_0'
                                    942 ;sloc4         Allocated with name '_raw_hid_receive_sloc4_1_0'
                                    943 ;length        Allocated with name '_raw_hid_receive_PARM_2'
                                    944 ;packet        Allocated with name '_raw_hid_receive_packet_10000_608'
                                    945 ;data          Allocated with name '_raw_hid_receive_data_10000_609'
                                    946 ;command_id    Allocated with name '_raw_hid_receive_command_id_10000_609'
                                    947 ;command_data  Allocated with name '_raw_hid_receive_command_data_10000_609'
                                    948 ;cmd           Allocated with name '_raw_hid_receive_cmd_30001_615'
                                    949 ;value         Allocated with name '_raw_hid_receive_value_70000_623'
                                    950 ;value         Allocated with name '_raw_hid_receive_value_70000_624'
                                    951 ;i             Allocated with name '_raw_hid_receive_i_70001_627'
                                    952 ;row           Allocated with name '_raw_hid_receive_row_80001_628'
                                    953 ;value         Allocated with name '_raw_hid_receive_value_90001_629'
                                    954 ;value         Allocated with name '_raw_hid_receive_value_70000_634'
                                    955 ;keycode       Allocated with name '_raw_hid_receive_keycode_40000_636'
                                    956 ;size          Allocated with name '_raw_hid_receive_size_40000_645'
                                    957 ;offset        Allocated with name '_raw_hid_receive_offset_40000_646'
                                    958 ;size          Allocated with name '_raw_hid_receive_size_40000_646'
                                    959 ;offset        Allocated with name '_raw_hid_receive_offset_40001_651'
                                    960 ;size          Allocated with name '_raw_hid_receive_size_40001_651'
                                    961 ;offset        Allocated with name '_raw_hid_receive_offset_40000_656'
                                    962 ;size          Allocated with name '_raw_hid_receive_size_40000_656'
                                    963 ;offset        Allocated with name '_raw_hid_receive_offset_40000_658'
                                    964 ;size          Allocated with name '_raw_hid_receive_size_40000_658'
                                    965 ;i             Allocated with name '_raw_hid_receive_i_60000_663'
                                    966 ;------------------------------------------------------------
                                    967 ;	quantum/via.c:233: void raw_hid_receive(uint8_t *packet, uint8_t length) {
                                    968 ;	-----------------------------------------
                                    969 ;	 function raw_hid_receive
                                    970 ;	-----------------------------------------
      00A17A                        971 _raw_hid_receive:
      00A17A AF F0            [24]  972 	mov	r7,b
      00A17C AE 83            [24]  973 	mov	r6,dph
      00A17E E5 82            [12]  974 	mov	a,dpl
      00A180 90 0A 54         [24]  975 	mov	dptr,#_raw_hid_receive_packet_10000_608
      00A183 F0               [24]  976 	movx	@dptr,a
      00A184 EE               [12]  977 	mov	a,r6
      00A185 A3               [24]  978 	inc	dptr
      00A186 F0               [24]  979 	movx	@dptr,a
      00A187 EF               [12]  980 	mov	a,r7
      00A188 A3               [24]  981 	inc	dptr
      00A189 F0               [24]  982 	movx	@dptr,a
                                    983 ;	quantum/via.c:236: uint8_t __xdata *data = (uint8_t __xdata *)packet;
      00A18A 90 0A 54         [24]  984 	mov	dptr,#_raw_hid_receive_packet_10000_608
      00A18D E0               [24]  985 	movx	a,@dptr
      00A18E FE               [12]  986 	mov	r6,a
      00A18F A3               [24]  987 	inc	dptr
      00A190 E0               [24]  988 	movx	a,@dptr
      00A191 FF               [12]  989 	mov	r7,a
                                    990 ;	quantum/via.c:238: uint8_t __xdata *command_data = &data[1];
      00A192 74 01            [12]  991 	mov	a,#0x01
      00A194 2E               [12]  992 	add	a, r6
      00A195 FC               [12]  993 	mov	r4,a
      00A196 E4               [12]  994 	clr	a
      00A197 3F               [12]  995 	addc	a, r7
      00A198 FD               [12]  996 	mov	r5,a
                                    997 ;	quantum/via.c:245: if (length != 32) return;
      00A199 90 0A 53         [24]  998 	mov	dptr,#_raw_hid_receive_PARM_2
      00A19C E0               [24]  999 	movx	a,@dptr
      00A19D FB               [12] 1000 	mov	r3,a
      00A19E BB 20 02         [24] 1001 	cjne	r3,#0x20,00520$
      00A1A1 80 01            [24] 1002 	sjmp	00102$
      00A1A3                       1003 00520$:
      00A1A3 22               [24] 1004 	ret
      00A1A4                       1005 00102$:
                                   1006 ;	quantum/via.c:249: if (vial_unlock_in_progress) {
      00A1A4 90 0C 08         [24] 1007 	mov	dptr,#_vial_unlock_in_progress
      00A1A7 E0               [24] 1008 	movx	a,@dptr
      00A1A8 60 35            [24] 1009 	jz	00114$
                                   1010 ;	quantum/via.c:250: if (data[0] != id_vial_prefix) {
      00A1AA 8E 82            [24] 1011 	mov	dpl,r6
      00A1AC 8F 83            [24] 1012 	mov	dph,r7
      00A1AE E0               [24] 1013 	movx	a,@dptr
      00A1AF FA               [12] 1014 	mov	r2,a
      00A1B0 BA FE 02         [24] 1015 	cjne	r2,#0xfe,00522$
      00A1B3 80 01            [24] 1016 	sjmp	00104$
      00A1B5                       1017 00522$:
                                   1018 ;	quantum/via.c:252: return;
      00A1B5 22               [24] 1019 	ret
      00A1B6                       1020 00104$:
                                   1021 ;	quantum/via.c:257: uint8_t cmd = data[1];
      00A1B6 8C 82            [24] 1022 	mov	dpl,r4
      00A1B8 8D 83            [24] 1023 	mov	dph,r5
      00A1BA E0               [24] 1024 	movx	a,@dptr
                                   1025 ;	quantum/via.c:258: if (cmd != vial_get_keyboard_id && cmd != vial_get_size && cmd != vial_get_def && cmd != vial_get_unlock_status && cmd != vial_unlock_start && cmd != vial_unlock_poll && cmd != vial_lock)
      00A1BB FA               [12] 1026 	mov	r2,a
      00A1BC 60 21            [24] 1027 	jz	00114$
      00A1BE BA 01 02         [24] 1028 	cjne	r2,#0x01,00524$
      00A1C1 80 1C            [24] 1029 	sjmp	00114$
      00A1C3                       1030 00524$:
      00A1C3 BA 02 02         [24] 1031 	cjne	r2,#0x02,00525$
      00A1C6 80 17            [24] 1032 	sjmp	00114$
      00A1C8                       1033 00525$:
      00A1C8 BA 05 02         [24] 1034 	cjne	r2,#0x05,00526$
      00A1CB 80 12            [24] 1035 	sjmp	00114$
      00A1CD                       1036 00526$:
      00A1CD BA 06 02         [24] 1037 	cjne	r2,#0x06,00527$
      00A1D0 80 0D            [24] 1038 	sjmp	00114$
      00A1D2                       1039 00527$:
      00A1D2 BA 07 02         [24] 1040 	cjne	r2,#0x07,00528$
      00A1D5 80 08            [24] 1041 	sjmp	00114$
      00A1D7                       1042 00528$:
      00A1D7 BA 08 02         [24] 1043 	cjne	r2,#0x08,00529$
      00A1DA 80 03            [24] 1044 	sjmp	00530$
      00A1DC                       1045 00529$:
      00A1DC 02 A7 9E         [24] 1046 	ljmp	00171$
      00A1DF                       1047 00530$:
                                   1048 ;	quantum/via.c:259: goto skip;
      00A1DF                       1049 00114$:
                                   1050 ;	quantum/via.c:263: switch (*command_id) {
      00A1DF 8E 82            [24] 1051 	mov	dpl,r6
      00A1E1 8F 83            [24] 1052 	mov	dph,r7
      00A1E3 E0               [24] 1053 	movx	a,@dptr
      00A1E4 FA               [12] 1054 	mov	r2,a
      00A1E5 BA 01 02         [24] 1055 	cjne	r2,#0x01,00531$
      00A1E8 80 6E            [24] 1056 	sjmp	00115$
      00A1EA                       1057 00531$:
      00A1EA BA 02 02         [24] 1058 	cjne	r2,#0x02,00532$
      00A1ED 80 7B            [24] 1059 	sjmp	00116$
      00A1EF                       1060 00532$:
      00A1EF BA 03 03         [24] 1061 	cjne	r2,#0x03,00533$
      00A1F2 02 A3 3D         [24] 1062 	ljmp	00125$
      00A1F5                       1063 00533$:
      00A1F5 BA 04 03         [24] 1064 	cjne	r2,#0x04,00534$
      00A1F8 02 A3 DF         [24] 1065 	ljmp	00129$
      00A1FB                       1066 00534$:
      00A1FB BA 05 03         [24] 1067 	cjne	r2,#0x05,00535$
      00A1FE 02 A4 20         [24] 1068 	ljmp	00130$
      00A201                       1069 00535$:
      00A201 BA 06 03         [24] 1070 	cjne	r2,#0x06,00536$
      00A204 02 A4 9B         [24] 1071 	ljmp	00135$
      00A207                       1072 00536$:
      00A207 BA 07 03         [24] 1073 	cjne	r2,#0x07,00537$
      00A20A 02 A4 AD         [24] 1074 	ljmp	00136$
      00A20D                       1075 00537$:
      00A20D BA 08 03         [24] 1076 	cjne	r2,#0x08,00538$
      00A210 02 A4 CB         [24] 1077 	ljmp	00137$
      00A213                       1078 00538$:
      00A213 BA 09 03         [24] 1079 	cjne	r2,#0x09,00539$
      00A216 02 A4 E9         [24] 1080 	ljmp	00138$
      00A219                       1081 00539$:
      00A219 BA 0B 03         [24] 1082 	cjne	r2,#0x0b,00540$
      00A21C 02 A7 14         [24] 1083 	ljmp	00161$
      00A21F                       1084 00540$:
      00A21F BA 0C 03         [24] 1085 	cjne	r2,#0x0c,00541$
      00A222 02 A5 07         [24] 1086 	ljmp	00139$
      00A225                       1087 00541$:
      00A225 BA 0D 03         [24] 1088 	cjne	r2,#0x0d,00542$
      00A228 02 A5 29         [24] 1089 	ljmp	00140$
      00A22B                       1090 00542$:
      00A22B BA 0E 03         [24] 1091 	cjne	r2,#0x0e,00543$
      00A22E 02 A5 57         [24] 1092 	ljmp	00141$
      00A231                       1093 00543$:
      00A231 BA 0F 03         [24] 1094 	cjne	r2,#0x0f,00544$
      00A234 02 A5 AA         [24] 1095 	ljmp	00144$
      00A237                       1096 00544$:
      00A237 BA 10 03         [24] 1097 	cjne	r2,#0x10,00545$
      00A23A 02 A6 24         [24] 1098 	ljmp	00151$
      00A23D                       1099 00545$:
      00A23D BA 11 03         [24] 1100 	cjne	r2,#0x11,00546$
      00A240 02 A6 3D         [24] 1101 	ljmp	00154$
      00A243                       1102 00546$:
      00A243 BA 12 03         [24] 1103 	cjne	r2,#0x12,00547$
      00A246 02 A6 5F         [24] 1104 	ljmp	00155$
      00A249                       1105 00547$:
      00A249 BA 13 03         [24] 1106 	cjne	r2,#0x13,00548$
      00A24C 02 A6 B2         [24] 1107 	ljmp	00158$
      00A24F                       1108 00548$:
      00A24F BA FE 03         [24] 1109 	cjne	r2,#0xfe,00549$
      00A252 02 A7 5C         [24] 1110 	ljmp	00168$
      00A255                       1111 00549$:
      00A255 02 A7 7E         [24] 1112 	ljmp	00169$
                                   1113 ;	quantum/via.c:264: case id_get_protocol_version: {
      00A258                       1114 00115$:
                                   1115 ;	quantum/via.c:265: command_data[0] = VIA_PROTOCOL_VERSION >> 8;
      00A258 8C 82            [24] 1116 	mov	dpl,r4
      00A25A 8D 83            [24] 1117 	mov	dph,r5
      00A25C E4               [12] 1118 	clr	a
      00A25D F0               [24] 1119 	movx	@dptr,a
                                   1120 ;	quantum/via.c:266: command_data[1] = VIA_PROTOCOL_VERSION & 0xFF;
      00A25E 8E 82            [24] 1121 	mov	dpl,r6
      00A260 8F 83            [24] 1122 	mov	dph,r7
      00A262 A3               [24] 1123 	inc	dptr
      00A263 A3               [24] 1124 	inc	dptr
      00A264 74 09            [12] 1125 	mov	a,#0x09
      00A266 F0               [24] 1126 	movx	@dptr,a
                                   1127 ;	quantum/via.c:267: break;
      00A267 02 A7 9E         [24] 1128 	ljmp	00171$
                                   1129 ;	quantum/via.c:269: case id_get_keyboard_value: {
      00A26A                       1130 00116$:
                                   1131 ;	quantum/via.c:270: switch (command_data[0]) {
      00A26A 8C 82            [24] 1132 	mov	dpl,r4
      00A26C 8D 83            [24] 1133 	mov	dph,r5
      00A26E E0               [24] 1134 	movx	a,@dptr
      00A26F FA               [12] 1135 	mov	r2,a
      00A270 BA 01 02         [24] 1136 	cjne	r2,#0x01,00550$
      00A273 80 0E            [24] 1137 	sjmp	00117$
      00A275                       1138 00550$:
      00A275 BA 02 02         [24] 1139 	cjne	r2,#0x02,00551$
      00A278 80 3A            [24] 1140 	sjmp	00118$
      00A27A                       1141 00551$:
      00A27A BA 03 03         [24] 1142 	cjne	r2,#0x03,00552$
      00A27D 02 A2 F5         [24] 1143 	ljmp	00119$
      00A280                       1144 00552$:
      00A280 02 A3 1F         [24] 1145 	ljmp	00123$
                                   1146 ;	quantum/via.c:271: case id_uptime: {
      00A283                       1147 00117$:
                                   1148 ;	quantum/via.c:272: uint32_t value  = timer_read32();
      00A283 12 40 1D         [24] 1149 	lcall	_timer_read32
      00A286 85 82 41         [24] 1150 	mov	_raw_hid_receive_sloc0_1_0,dpl
      00A289 85 83 42         [24] 1151 	mov	(_raw_hid_receive_sloc0_1_0 + 1),dph
      00A28C 85 F0 43         [24] 1152 	mov	(_raw_hid_receive_sloc0_1_0 + 2),b
      00A28F F5 44            [12] 1153 	mov	(_raw_hid_receive_sloc0_1_0 + 3),a
                                   1154 ;	quantum/via.c:273: command_data[1] = (value >> 24) & 0xFF;
      00A291 8E 82            [24] 1155 	mov	dpl,r6
      00A293 8F 83            [24] 1156 	mov	dph,r7
      00A295 A3               [24] 1157 	inc	dptr
      00A296 A3               [24] 1158 	inc	dptr
      00A297 E5 44            [12] 1159 	mov	a,(_raw_hid_receive_sloc0_1_0 + 3)
      00A299 F0               [24] 1160 	movx	@dptr,a
                                   1161 ;	quantum/via.c:274: command_data[2] = (value >> 16) & 0xFF;
      00A29A 8E 82            [24] 1162 	mov	dpl,r6
      00A29C 8F 83            [24] 1163 	mov	dph,r7
      00A29E A3               [24] 1164 	inc	dptr
      00A29F A3               [24] 1165 	inc	dptr
      00A2A0 A3               [24] 1166 	inc	dptr
      00A2A1 E5 43            [12] 1167 	mov	a,(_raw_hid_receive_sloc0_1_0 + 2)
      00A2A3 F0               [24] 1168 	movx	@dptr,a
                                   1169 ;	quantum/via.c:275: command_data[3] = (value >> 8) & 0xFF;
      00A2A4 12 A7 AE         [24] 1170 	lcall	_ak820_outline_0006
      00A2A7 E5 42            [12] 1171 	mov	a,(_raw_hid_receive_sloc0_1_0 + 1)
      00A2A9 F0               [24] 1172 	movx	@dptr,a
                                   1173 ;	quantum/via.c:276: command_data[4] = value & 0xFF;
      00A2AA 12 A7 AE         [24] 1174 	lcall	_ak820_outline_0006
      00A2AD A3               [24] 1175 	inc	dptr
      00A2AE E5 41            [12] 1176 	mov	a,_raw_hid_receive_sloc0_1_0
      00A2B0 F0               [24] 1177 	movx	@dptr,a
                                   1178 ;	quantum/via.c:277: break;
      00A2B1 02 A7 9E         [24] 1179 	ljmp	00171$
                                   1180 ;	quantum/via.c:279: case id_layout_options: {
      00A2B4                       1181 00118$:
                                   1182 ;	quantum/via.c:280: uint32_t value  = via_get_layout_options();
      00A2B4 C0 03            [24] 1183 	push	ar3
      00A2B6 C0 07            [24] 1184 	push	ar7
      00A2B8 C0 06            [24] 1185 	push	ar6
      00A2BA C0 03            [24] 1186 	push	ar3
      00A2BC 12 A0 E7         [24] 1187 	lcall	_via_get_layout_options
      00A2BF 85 82 41         [24] 1188 	mov	_raw_hid_receive_sloc0_1_0,dpl
      00A2C2 85 83 42         [24] 1189 	mov	(_raw_hid_receive_sloc0_1_0 + 1),dph
      00A2C5 85 F0 43         [24] 1190 	mov	(_raw_hid_receive_sloc0_1_0 + 2),b
      00A2C8 F5 44            [12] 1191 	mov	(_raw_hid_receive_sloc0_1_0 + 3),a
      00A2CA D0 03            [24] 1192 	pop	ar3
      00A2CC D0 06            [24] 1193 	pop	ar6
      00A2CE D0 07            [24] 1194 	pop	ar7
                                   1195 ;	quantum/via.c:281: command_data[1] = (value >> 24) & 0xFF;
      00A2D0 8E 82            [24] 1196 	mov	dpl,r6
      00A2D2 8F 83            [24] 1197 	mov	dph,r7
      00A2D4 A3               [24] 1198 	inc	dptr
      00A2D5 A3               [24] 1199 	inc	dptr
      00A2D6 E5 44            [12] 1200 	mov	a,(_raw_hid_receive_sloc0_1_0 + 3)
      00A2D8 F0               [24] 1201 	movx	@dptr,a
                                   1202 ;	quantum/via.c:282: command_data[2] = (value >> 16) & 0xFF;
      00A2D9 8E 82            [24] 1203 	mov	dpl,r6
      00A2DB 8F 83            [24] 1204 	mov	dph,r7
      00A2DD A3               [24] 1205 	inc	dptr
      00A2DE A3               [24] 1206 	inc	dptr
      00A2DF A3               [24] 1207 	inc	dptr
      00A2E0 E5 43            [12] 1208 	mov	a,(_raw_hid_receive_sloc0_1_0 + 2)
      00A2E2 F0               [24] 1209 	movx	@dptr,a
                                   1210 ;	quantum/via.c:283: command_data[3] = (value >> 8) & 0xFF;
      00A2E3 12 A7 AE         [24] 1211 	lcall	_ak820_outline_0006
      00A2E6 E5 42            [12] 1212 	mov	a,(_raw_hid_receive_sloc0_1_0 + 1)
      00A2E8 F0               [24] 1213 	movx	@dptr,a
                                   1214 ;	quantum/via.c:284: command_data[4] = value & 0xFF;
      00A2E9 12 A7 AE         [24] 1215 	lcall	_ak820_outline_0006
      00A2EC A3               [24] 1216 	inc	dptr
      00A2ED E5 41            [12] 1217 	mov	a,_raw_hid_receive_sloc0_1_0
      00A2EF F0               [24] 1218 	movx	@dptr,a
                                   1219 ;	quantum/via.c:285: break;
      00A2F0 D0 03            [24] 1220 	pop	ar3
      00A2F2 02 A7 9E         [24] 1221 	ljmp	00171$
                                   1222 ;	quantum/via.c:287: case id_switch_matrix_state: {
      00A2F5                       1223 00119$:
                                   1224 ;	quantum/via.c:290: if (!vial_unlocked)
      00A2F5 90 0C 07         [24] 1225 	mov	dptr,#_vial_unlocked
      00A2F8 E0               [24] 1226 	movx	a,@dptr
      00A2F9 70 03            [24] 1227 	jnz	00553$
      00A2FB 02 A7 9E         [24] 1228 	ljmp	00171$
      00A2FE                       1229 00553$:
                                   1230 ;	quantum/via.c:296: for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
      00A2FE 7A 01            [12] 1231 	mov	r2,#0x01
      00A300 79 00            [12] 1232 	mov	r1,#0x00
      00A302                       1233 00173$:
      00A302 B9 10 00         [24] 1234 	cjne	r1,#0x10,00554$
      00A305                       1235 00554$:
      00A305 40 03            [24] 1236 	jc	00555$
      00A307 02 A7 9E         [24] 1237 	ljmp	00171$
      00A30A                       1238 00555$:
                                   1239 ;	quantum/via.c:297: matrix_row_t value = matrix_get_row(row);
      00A30A 89 82            [24] 1240 	mov	dpl, r1
      00A30C 12 53 3F         [24] 1241 	lcall	_matrix_get_row
      00A30F A8 82            [24] 1242 	mov	r0, dpl
                                   1243 ;	quantum/via.c:307: command_data[i++] = value & 0xFF;
      00A311 EA               [12] 1244 	mov	a,r2
      00A312 2C               [12] 1245 	add	a, r4
      00A313 F5 82            [12] 1246 	mov	dpl,a
      00A315 E4               [12] 1247 	clr	a
      00A316 3D               [12] 1248 	addc	a, r5
      00A317 F5 83            [12] 1249 	mov	dph,a
      00A319 0A               [12] 1250 	inc	r2
      00A31A E8               [12] 1251 	mov	a,r0
      00A31B F0               [24] 1252 	movx	@dptr,a
                                   1253 ;	quantum/via.c:296: for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
      00A31C 09               [12] 1254 	inc	r1
                                   1255 ;	quantum/via.c:312: default: {
      00A31D 80 E3            [24] 1256 	sjmp	00173$
      00A31F                       1257 00123$:
                                   1258 ;	quantum/via.c:313: raw_hid_receive_kb(data, length);
      00A31F 8E 00            [24] 1259 	mov	ar0,r6
      00A321 8F 01            [24] 1260 	mov	ar1,r7
      00A323 7A 00            [12] 1261 	mov	r2,#0x00
      00A325 90 0A 4F         [24] 1262 	mov	dptr,#_raw_hid_receive_kb_PARM_2
      00A328 12 A7 D7         [24] 1263 	lcall	_ak820_outline_0021
      00A32B C0 07            [24] 1264 	push	ar7
      00A32D C0 06            [24] 1265 	push	ar6
      00A32F C0 03            [24] 1266 	push	ar3
      00A331 12 A1 59         [24] 1267 	lcall	_raw_hid_receive_kb
      00A334 D0 03            [24] 1268 	pop	ar3
      00A336 D0 06            [24] 1269 	pop	ar6
      00A338 D0 07            [24] 1270 	pop	ar7
                                   1271 ;	quantum/via.c:317: break;
      00A33A 02 A7 9E         [24] 1272 	ljmp	00171$
                                   1273 ;	quantum/via.c:319: case id_set_keyboard_value: {
      00A33D                       1274 00125$:
                                   1275 ;	quantum/via.c:320: switch (command_data[0]) {
      00A33D 8C 82            [24] 1276 	mov	dpl,r4
      00A33F 8D 83            [24] 1277 	mov	dph,r5
      00A341 E0               [24] 1278 	movx	a,@dptr
      00A342 FA               [12] 1279 	mov	r2,a
      00A343 BA 02 02         [24] 1280 	cjne	r2,#0x02,00556$
      00A346 80 03            [24] 1281 	sjmp	00557$
      00A348                       1282 00556$:
      00A348 02 A3 C1         [24] 1283 	ljmp	00127$
      00A34B                       1284 00557$:
                                   1285 ;	quantum/via.c:322: uint32_t value = ((uint32_t)command_data[1] << 24) | ((uint32_t)command_data[2] << 16) | ((uint32_t)command_data[3] << 8) | (uint32_t)command_data[4];
      00A34B C0 03            [24] 1286 	push	ar3
      00A34D 8E 82            [24] 1287 	mov	dpl,r6
      00A34F 8F 83            [24] 1288 	mov	dph,r7
      00A351 A3               [24] 1289 	inc	dptr
      00A352 A3               [24] 1290 	inc	dptr
      00A353 E0               [24] 1291 	movx	a,@dptr
      00A354 F8               [12] 1292 	mov	r0,a
      00A355 79 00            [12] 1293 	mov	r1,#0x00
      00A357 7B 00            [12] 1294 	mov	r3,#0x00
      00A359 88 44            [24] 1295 	mov	(_raw_hid_receive_sloc0_1_0 + 3),r0
      00A35B 8B 41            [24] 1296 	mov	_raw_hid_receive_sloc0_1_0,r3
      00A35D 8B 42            [24] 1297 	mov	(_raw_hid_receive_sloc0_1_0 + 1),r3
      00A35F 8B 43            [24] 1298 	mov	(_raw_hid_receive_sloc0_1_0 + 2),r3
      00A361 12 A7 B7         [24] 1299 	lcall	_ak820_outline_0010
      00A364 F8               [12] 1300 	mov	r0,a
      00A365 89 03            [24] 1301 	mov	ar3,r1
      00A367 88 02            [24] 1302 	mov	ar2,r0
      00A369 E4               [12] 1303 	clr	a
      00A36A 42 41            [12] 1304 	orl	_raw_hid_receive_sloc0_1_0,a
      00A36C E9               [12] 1305 	mov	a,r1
      00A36D 42 42            [12] 1306 	orl	(_raw_hid_receive_sloc0_1_0 + 1),a
      00A36F EA               [12] 1307 	mov	a,r2
      00A370 42 43            [12] 1308 	orl	(_raw_hid_receive_sloc0_1_0 + 2),a
      00A372 EB               [12] 1309 	mov	a,r3
      00A373 42 44            [12] 1310 	orl	(_raw_hid_receive_sloc0_1_0 + 3),a
      00A375 12 A7 AE         [24] 1311 	lcall	_ak820_outline_0006
      00A378 E0               [24] 1312 	movx	a,@dptr
      00A379 F8               [12] 1313 	mov	r0,a
      00A37A 79 00            [12] 1314 	mov	r1,#0x00
      00A37C 7A 00            [12] 1315 	mov	r2,#0x00
      00A37E 8A 03            [24] 1316 	mov	ar3,r2
      00A380 89 02            [24] 1317 	mov	ar2,r1
      00A382 88 01            [24] 1318 	mov	ar1,r0
      00A384 E4               [12] 1319 	clr	a
      00A385 42 41            [12] 1320 	orl	_raw_hid_receive_sloc0_1_0,a
      00A387 E9               [12] 1321 	mov	a,r1
      00A388 42 42            [12] 1322 	orl	(_raw_hid_receive_sloc0_1_0 + 1),a
      00A38A EA               [12] 1323 	mov	a,r2
      00A38B 42 43            [12] 1324 	orl	(_raw_hid_receive_sloc0_1_0 + 2),a
      00A38D EB               [12] 1325 	mov	a,r3
      00A38E 42 44            [12] 1326 	orl	(_raw_hid_receive_sloc0_1_0 + 3),a
      00A390 12 A7 AE         [24] 1327 	lcall	_ak820_outline_0006
      00A393 A3               [24] 1328 	inc	dptr
      00A394 E0               [24] 1329 	movx	a,@dptr
      00A395 F8               [12] 1330 	mov	r0,a
      00A396 E4               [12] 1331 	clr	a
      00A397 F9               [12] 1332 	mov	r1,a
      00A398 FA               [12] 1333 	mov	r2,a
      00A399 FB               [12] 1334 	mov	r3,a
      00A39A E5 42            [12] 1335 	mov	a,(_raw_hid_receive_sloc0_1_0 + 1)
      00A39C 42 01            [12] 1336 	orl	ar1,a
      00A39E E5 43            [12] 1337 	mov	a,(_raw_hid_receive_sloc0_1_0 + 2)
      00A3A0 42 02            [12] 1338 	orl	ar2,a
      00A3A2 E5 44            [12] 1339 	mov	a,(_raw_hid_receive_sloc0_1_0 + 3)
      00A3A4 42 03            [12] 1340 	orl	ar3,a
                                   1341 ;	quantum/via.c:323: via_set_layout_options(value);
      00A3A6 88 82            [24] 1342 	mov	dpl, r0
      00A3A8 89 83            [24] 1343 	mov	dph, r1
      00A3AA 8A F0            [24] 1344 	mov	b, r2
      00A3AC EB               [12] 1345 	mov	a, r3
      00A3AD C0 07            [24] 1346 	push	ar7
      00A3AF C0 06            [24] 1347 	push	ar6
      00A3B1 C0 03            [24] 1348 	push	ar3
      00A3B3 12 A1 01         [24] 1349 	lcall	_via_set_layout_options
      00A3B6 D0 03            [24] 1350 	pop	ar3
      00A3B8 D0 06            [24] 1351 	pop	ar6
      00A3BA D0 07            [24] 1352 	pop	ar7
                                   1353 ;	quantum/via.c:324: break;
      00A3BC D0 03            [24] 1354 	pop	ar3
      00A3BE 02 A7 9E         [24] 1355 	ljmp	00171$
                                   1356 ;	quantum/via.c:326: default: {
      00A3C1                       1357 00127$:
                                   1358 ;	quantum/via.c:327: raw_hid_receive_kb(data, length);
      00A3C1 8E 00            [24] 1359 	mov	ar0,r6
      00A3C3 8F 01            [24] 1360 	mov	ar1,r7
      00A3C5 7A 00            [12] 1361 	mov	r2,#0x00
      00A3C7 90 0A 4F         [24] 1362 	mov	dptr,#_raw_hid_receive_kb_PARM_2
      00A3CA 12 A7 D7         [24] 1363 	lcall	_ak820_outline_0021
      00A3CD C0 07            [24] 1364 	push	ar7
      00A3CF C0 06            [24] 1365 	push	ar6
      00A3D1 C0 03            [24] 1366 	push	ar3
      00A3D3 12 A1 59         [24] 1367 	lcall	_raw_hid_receive_kb
      00A3D6 D0 03            [24] 1368 	pop	ar3
      00A3D8 D0 06            [24] 1369 	pop	ar6
      00A3DA D0 07            [24] 1370 	pop	ar7
                                   1371 ;	quantum/via.c:331: break;
      00A3DC 02 A7 9E         [24] 1372 	ljmp	00171$
                                   1373 ;	quantum/via.c:333: case id_dynamic_keymap_get_keycode: {
      00A3DF                       1374 00129$:
                                   1375 ;	quantum/via.c:334: uint16_t keycode = dynamic_keymap_get_keycode(command_data[0], command_data[1], command_data[2]);
      00A3DF 8C 82            [24] 1376 	mov	dpl,r4
      00A3E1 8D 83            [24] 1377 	mov	dph,r5
      00A3E3 E0               [24] 1378 	movx	a,@dptr
      00A3E4 FA               [12] 1379 	mov	r2,a
      00A3E5 8E 82            [24] 1380 	mov	dpl,r6
      00A3E7 8F 83            [24] 1381 	mov	dph,r7
      00A3E9 A3               [24] 1382 	inc	dptr
      00A3EA A3               [24] 1383 	inc	dptr
      00A3EB E0               [24] 1384 	movx	a,@dptr
      00A3EC F9               [12] 1385 	mov	r1,a
      00A3ED 12 A7 B7         [24] 1386 	lcall	_ak820_outline_0010
      00A3F0 F8               [12] 1387 	mov	r0,a
      00A3F1 90 08 D9         [24] 1388 	mov	dptr,#_dynamic_keymap_get_keycode_PARM_2
      00A3F4 E9               [12] 1389 	mov	a,r1
      00A3F5 F0               [24] 1390 	movx	@dptr,a
      00A3F6 90 08 DA         [24] 1391 	mov	dptr,#_dynamic_keymap_get_keycode_PARM_3
      00A3F9 E8               [12] 1392 	mov	a,r0
      00A3FA F0               [24] 1393 	movx	@dptr,a
      00A3FB 8A 82            [24] 1394 	mov	dpl, r2
      00A3FD C0 07            [24] 1395 	push	ar7
      00A3FF C0 06            [24] 1396 	push	ar6
      00A401 C0 03            [24] 1397 	push	ar3
      00A403 12 7B C5         [24] 1398 	lcall	_dynamic_keymap_get_keycode
      00A406 A9 82            [24] 1399 	mov	r1, dpl
      00A408 AA 83            [24] 1400 	mov	r2, dph
      00A40A D0 03            [24] 1401 	pop	ar3
      00A40C D0 06            [24] 1402 	pop	ar6
      00A40E D0 07            [24] 1403 	pop	ar7
                                   1404 ;	quantum/via.c:335: command_data[3]  = keycode >> 8;
      00A410 12 A7 AE         [24] 1405 	lcall	_ak820_outline_0006
      00A413 8A 00            [24] 1406 	mov	ar0,r2
      00A415 E8               [12] 1407 	mov	a,r0
      00A416 F0               [24] 1408 	movx	@dptr,a
                                   1409 ;	quantum/via.c:336: command_data[4]  = keycode & 0xFF;
      00A417 12 A7 AE         [24] 1410 	lcall	_ak820_outline_0006
      00A41A A3               [24] 1411 	inc	dptr
      00A41B E9               [12] 1412 	mov	a,r1
      00A41C F0               [24] 1413 	movx	@dptr,a
                                   1414 ;	quantum/via.c:337: break;
      00A41D 02 A7 9E         [24] 1415 	ljmp	00171$
                                   1416 ;	quantum/via.c:339: case id_dynamic_keymap_set_keycode: {
      00A420                       1417 00130$:
                                   1418 ;	quantum/via.c:343: if (!vial_unlocked && command_data[3] == (QK_BOOT >> 8) && command_data[4] == (QK_BOOT & 0xFF)) {
      00A420 90 0C 07         [24] 1419 	mov	dptr,#_vial_unlocked
      00A423 E0               [24] 1420 	movx	a,@dptr
      00A424 70 20            [24] 1421 	jnz	00132$
      00A426 12 A7 AE         [24] 1422 	lcall	_ak820_outline_0006
      00A429 E0               [24] 1423 	movx	a,@dptr
      00A42A FA               [12] 1424 	mov	r2,a
      00A42B BA 7C 18         [24] 1425 	cjne	r2,#0x7c,00132$
      00A42E 74 05            [12] 1426 	mov	a,#0x05
      00A430 2E               [12] 1427 	add	a, r6
      00A431 F9               [12] 1428 	mov	r1,a
      00A432 E4               [12] 1429 	clr	a
      00A433 3F               [12] 1430 	addc	a, r7
      00A434 FA               [12] 1431 	mov	r2,a
      00A435 89 82            [24] 1432 	mov	dpl,r1
      00A437 8A 83            [24] 1433 	mov	dph,r2
      00A439 E0               [24] 1434 	movx	a,@dptr
      00A43A 70 0A            [24] 1435 	jnz	00132$
                                   1436 ;	quantum/via.c:344: *command_id = id_unhandled;
      00A43C 8E 82            [24] 1437 	mov	dpl,r6
      00A43E 8F 83            [24] 1438 	mov	dph,r7
      00A440 74 FF            [12] 1439 	mov	a,#0xff
      00A442 F0               [24] 1440 	movx	@dptr,a
                                   1441 ;	quantum/via.c:345: break;
      00A443 02 A7 9E         [24] 1442 	ljmp	00171$
      00A446                       1443 00132$:
                                   1444 ;	quantum/via.c:348: dynamic_keymap_set_keycode(command_data[0], command_data[1], command_data[2], (command_data[3] << 8) | command_data[4]);
      00A446 C0 03            [24] 1445 	push	ar3
      00A448 8C 82            [24] 1446 	mov	dpl,r4
      00A44A 8D 83            [24] 1447 	mov	dph,r5
      00A44C E0               [24] 1448 	movx	a,@dptr
      00A44D F5 46            [12] 1449 	mov	_raw_hid_receive_sloc2_1_0,a
      00A44F 8E 82            [24] 1450 	mov	dpl,r6
      00A451 8F 83            [24] 1451 	mov	dph,r7
      00A453 A3               [24] 1452 	inc	dptr
      00A454 A3               [24] 1453 	inc	dptr
      00A455 E0               [24] 1454 	movx	a,@dptr
      00A456 F5 45            [12] 1455 	mov	_raw_hid_receive_sloc1_1_0,a
      00A458 12 A7 B7         [24] 1456 	lcall	_ak820_outline_0010
      00A45B F5 41            [12] 1457 	mov	_raw_hid_receive_sloc0_1_0,a
      00A45D 12 A7 AE         [24] 1458 	lcall	_ak820_outline_0006
      00A460 E0               [24] 1459 	movx	a,@dptr
      00A461 FB               [12] 1460 	mov	r3,a
      00A462 78 00            [12] 1461 	mov	r0,#0x00
      00A464 12 A7 AE         [24] 1462 	lcall	_ak820_outline_0006
      00A467 A3               [24] 1463 	inc	dptr
      00A468 E0               [24] 1464 	movx	a,@dptr
      00A469 7A 00            [12] 1465 	mov	r2,#0x00
      00A46B 42 00            [12] 1466 	orl	ar0,a
      00A46D EA               [12] 1467 	mov	a,r2
      00A46E 42 03            [12] 1468 	orl	ar3,a
      00A470 90 08 DC         [24] 1469 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_2
      00A473 E5 45            [12] 1470 	mov	a,_raw_hid_receive_sloc1_1_0
      00A475 F0               [24] 1471 	movx	@dptr,a
      00A476 90 08 DD         [24] 1472 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_3
      00A479 E5 41            [12] 1473 	mov	a,_raw_hid_receive_sloc0_1_0
      00A47B F0               [24] 1474 	movx	@dptr,a
      00A47C 90 08 DE         [24] 1475 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_4
      00A47F E8               [12] 1476 	mov	a,r0
      00A480 F0               [24] 1477 	movx	@dptr,a
      00A481 EB               [12] 1478 	mov	a,r3
      00A482 A3               [24] 1479 	inc	dptr
      00A483 F0               [24] 1480 	movx	@dptr,a
      00A484 85 46 82         [24] 1481 	mov	dpl, _raw_hid_receive_sloc2_1_0
      00A487 C0 07            [24] 1482 	push	ar7
      00A489 C0 06            [24] 1483 	push	ar6
      00A48B C0 03            [24] 1484 	push	ar3
      00A48D 12 7C 23         [24] 1485 	lcall	_dynamic_keymap_set_keycode
      00A490 D0 03            [24] 1486 	pop	ar3
      00A492 D0 06            [24] 1487 	pop	ar6
      00A494 D0 07            [24] 1488 	pop	ar7
                                   1489 ;	quantum/via.c:349: break;
      00A496 D0 03            [24] 1490 	pop	ar3
      00A498 02 A7 9E         [24] 1491 	ljmp	00171$
                                   1492 ;	quantum/via.c:351: case id_dynamic_keymap_reset: {
      00A49B                       1493 00135$:
                                   1494 ;	quantum/via.c:352: dynamic_keymap_reset();
      00A49B C0 07            [24] 1495 	push	ar7
      00A49D C0 06            [24] 1496 	push	ar6
      00A49F C0 03            [24] 1497 	push	ar3
      00A4A1 12 7D 9D         [24] 1498 	lcall	_dynamic_keymap_reset
      00A4A4 D0 03            [24] 1499 	pop	ar3
      00A4A6 D0 06            [24] 1500 	pop	ar6
      00A4A8 D0 07            [24] 1501 	pop	ar7
                                   1502 ;	quantum/via.c:353: break;
      00A4AA 02 A7 9E         [24] 1503 	ljmp	00171$
                                   1504 ;	quantum/via.c:355: case id_lighting_set_value: {
      00A4AD                       1505 00136$:
                                   1506 ;	quantum/via.c:363: vialrgb_set_value(data, length);
      00A4AD 8E 00            [24] 1507 	mov	ar0,r6
      00A4AF 8F 01            [24] 1508 	mov	ar1,r7
      00A4B1 7A 00            [12] 1509 	mov	r2,#0x00
      00A4B3 90 0B 88         [24] 1510 	mov	dptr,#_vialrgb_set_value_PARM_2
      00A4B6 12 A7 D7         [24] 1511 	lcall	_ak820_outline_0021
      00A4B9 C0 07            [24] 1512 	push	ar7
      00A4BB C0 06            [24] 1513 	push	ar6
      00A4BD C0 03            [24] 1514 	push	ar3
      00A4BF 12 B3 1A         [24] 1515 	lcall	_vialrgb_set_value
      00A4C2 D0 03            [24] 1516 	pop	ar3
      00A4C4 D0 06            [24] 1517 	pop	ar6
      00A4C6 D0 07            [24] 1518 	pop	ar7
                                   1519 ;	quantum/via.c:375: break;
      00A4C8 02 A7 9E         [24] 1520 	ljmp	00171$
                                   1521 ;	quantum/via.c:377: case id_lighting_get_value: {
      00A4CB                       1522 00137$:
                                   1523 ;	quantum/via.c:385: vialrgb_get_value(data, length);
      00A4CB 8E 00            [24] 1524 	mov	ar0,r6
      00A4CD 8F 01            [24] 1525 	mov	ar1,r7
      00A4CF 7A 00            [12] 1526 	mov	r2,#0x00
      00A4D1 90 0B 84         [24] 1527 	mov	dptr,#_vialrgb_get_value_PARM_2
      00A4D4 12 A7 D7         [24] 1528 	lcall	_ak820_outline_0021
      00A4D7 C0 07            [24] 1529 	push	ar7
      00A4D9 C0 06            [24] 1530 	push	ar6
      00A4DB C0 03            [24] 1531 	push	ar3
      00A4DD 12 B1 90         [24] 1532 	lcall	_vialrgb_get_value
      00A4E0 D0 03            [24] 1533 	pop	ar3
      00A4E2 D0 06            [24] 1534 	pop	ar6
      00A4E4 D0 07            [24] 1535 	pop	ar7
                                   1536 ;	quantum/via.c:397: break;
      00A4E6 02 A7 9E         [24] 1537 	ljmp	00171$
                                   1538 ;	quantum/via.c:399: case id_lighting_save: {
      00A4E9                       1539 00138$:
                                   1540 ;	quantum/via.c:407: vialrgb_save(data, length);
      00A4E9 8E 00            [24] 1541 	mov	ar0,r6
      00A4EB 8F 01            [24] 1542 	mov	ar1,r7
      00A4ED 7A 00            [12] 1543 	mov	r2,#0x00
      00A4EF 90 0B 8C         [24] 1544 	mov	dptr,#_vialrgb_save_PARM_2
      00A4F2 12 A7 D7         [24] 1545 	lcall	_ak820_outline_0021
      00A4F5 C0 07            [24] 1546 	push	ar7
      00A4F7 C0 06            [24] 1547 	push	ar6
      00A4F9 C0 03            [24] 1548 	push	ar3
      00A4FB 12 B3 CA         [24] 1549 	lcall	_vialrgb_save
      00A4FE D0 03            [24] 1550 	pop	ar3
      00A500 D0 06            [24] 1551 	pop	ar6
      00A502 D0 07            [24] 1552 	pop	ar7
                                   1553 ;	quantum/via.c:419: break;
      00A504 02 A7 9E         [24] 1554 	ljmp	00171$
                                   1555 ;	quantum/via.c:428: case id_dynamic_keymap_macro_get_count: {
      00A507                       1556 00139$:
                                   1557 ;	quantum/via.c:429: command_data[0] = dynamic_keymap_macro_get_count();
      00A507 C0 07            [24] 1558 	push	ar7
      00A509 C0 06            [24] 1559 	push	ar6
      00A50B C0 05            [24] 1560 	push	ar5
      00A50D C0 04            [24] 1561 	push	ar4
      00A50F C0 03            [24] 1562 	push	ar3
      00A511 12 81 F2         [24] 1563 	lcall	_dynamic_keymap_macro_get_count
      00A514 AA 82            [24] 1564 	mov	r2, dpl
      00A516 D0 03            [24] 1565 	pop	ar3
      00A518 D0 04            [24] 1566 	pop	ar4
      00A51A D0 05            [24] 1567 	pop	ar5
      00A51C D0 06            [24] 1568 	pop	ar6
      00A51E D0 07            [24] 1569 	pop	ar7
      00A520 8C 82            [24] 1570 	mov	dpl,r4
      00A522 8D 83            [24] 1571 	mov	dph,r5
      00A524 EA               [12] 1572 	mov	a,r2
      00A525 F0               [24] 1573 	movx	@dptr,a
                                   1574 ;	quantum/via.c:430: break;
      00A526 02 A7 9E         [24] 1575 	ljmp	00171$
                                   1576 ;	quantum/via.c:432: case id_dynamic_keymap_macro_get_buffer_size: {
      00A529                       1577 00140$:
                                   1578 ;	quantum/via.c:433: uint16_t size   = dynamic_keymap_macro_get_buffer_size();
      00A529 C0 07            [24] 1579 	push	ar7
      00A52B C0 06            [24] 1580 	push	ar6
      00A52D C0 05            [24] 1581 	push	ar5
      00A52F C0 04            [24] 1582 	push	ar4
      00A531 C0 03            [24] 1583 	push	ar3
      00A533 12 81 F6         [24] 1584 	lcall	_dynamic_keymap_macro_get_buffer_size
      00A536 A9 82            [24] 1585 	mov	r1, dpl
      00A538 AA 83            [24] 1586 	mov	r2, dph
      00A53A D0 03            [24] 1587 	pop	ar3
      00A53C D0 04            [24] 1588 	pop	ar4
      00A53E D0 05            [24] 1589 	pop	ar5
      00A540 D0 06            [24] 1590 	pop	ar6
      00A542 D0 07            [24] 1591 	pop	ar7
                                   1592 ;	quantum/via.c:434: command_data[0] = size >> 8;
      00A544 8A 00            [24] 1593 	mov	ar0,r2
      00A546 8C 82            [24] 1594 	mov	dpl,r4
      00A548 8D 83            [24] 1595 	mov	dph,r5
      00A54A E8               [12] 1596 	mov	a,r0
      00A54B F0               [24] 1597 	movx	@dptr,a
                                   1598 ;	quantum/via.c:435: command_data[1] = size & 0xFF;
      00A54C 8E 82            [24] 1599 	mov	dpl,r6
      00A54E 8F 83            [24] 1600 	mov	dph,r7
      00A550 A3               [24] 1601 	inc	dptr
      00A551 A3               [24] 1602 	inc	dptr
      00A552 E9               [12] 1603 	mov	a,r1
      00A553 F0               [24] 1604 	movx	@dptr,a
                                   1605 ;	quantum/via.c:436: break;
      00A554 02 A7 9E         [24] 1606 	ljmp	00171$
                                   1607 ;	quantum/via.c:438: case id_dynamic_keymap_macro_get_buffer: {
      00A557                       1608 00141$:
                                   1609 ;	quantum/via.c:439: uint16_t offset = (command_data[0] << 8) | command_data[1];
      00A557 C0 03            [24] 1610 	push	ar3
      00A559 12 A7 C0         [24] 1611 	lcall	_ak820_outline_0011
      00A55C 89 41            [24] 1612 	mov	_raw_hid_receive_sloc0_1_0,r1
      00A55E 8A 42            [24] 1613 	mov	(_raw_hid_receive_sloc0_1_0 + 1),r2
                                   1614 ;	quantum/via.c:440: uint16_t size   = command_data[2]; // size <= 28
      00A560 12 A7 B7         [24] 1615 	lcall	_ak820_outline_0010
      00A563 FB               [12] 1616 	mov	r3,a
                                   1617 ;	quantum/via.c:441: if (size <= 28)
      00A564 8B 47            [24] 1618 	mov	_raw_hid_receive_sloc3_1_0,r3
      00A566 75 48 00         [24] 1619 	mov	(_raw_hid_receive_sloc3_1_0 + 1),#0x00
      00A569 C3               [12] 1620 	clr	c
      00A56A 74 1C            [12] 1621 	mov	a,#0x1c
      00A56C 9B               [12] 1622 	subb	a,r3
      00A56D D0 03            [24] 1623 	pop	ar3
      00A56F 50 03            [24] 1624 	jnc	00562$
      00A571 02 A7 9E         [24] 1625 	ljmp	00171$
      00A574                       1626 00562$:
                                   1627 ;	free result
                                   1628 ;	quantum/via.c:442: dynamic_keymap_macro_get_buffer(offset, size, &command_data[3]);
      00A574 74 04            [12] 1629 	mov	a,#0x04
      00A576 2E               [12] 1630 	add	a, r6
      00A577 F9               [12] 1631 	mov	r1,a
      00A578 E4               [12] 1632 	clr	a
      00A579 3F               [12] 1633 	addc	a, r7
      00A57A F8               [12] 1634 	mov	r0,a
      00A57B 7A 00            [12] 1635 	mov	r2,#0x00
      00A57D 90 09 0F         [24] 1636 	mov	dptr,#_dynamic_keymap_macro_get_buffer_PARM_2
      00A580 E5 47            [12] 1637 	mov	a,_raw_hid_receive_sloc3_1_0
      00A582 F0               [24] 1638 	movx	@dptr,a
      00A583 E5 48            [12] 1639 	mov	a,(_raw_hid_receive_sloc3_1_0 + 1)
      00A585 A3               [24] 1640 	inc	dptr
      00A586 F0               [24] 1641 	movx	@dptr,a
      00A587 90 09 11         [24] 1642 	mov	dptr,#_dynamic_keymap_macro_get_buffer_PARM_3
      00A58A E9               [12] 1643 	mov	a,r1
      00A58B F0               [24] 1644 	movx	@dptr,a
      00A58C E8               [12] 1645 	mov	a,r0
      00A58D A3               [24] 1646 	inc	dptr
      00A58E F0               [24] 1647 	movx	@dptr,a
      00A58F EA               [12] 1648 	mov	a,r2
      00A590 A3               [24] 1649 	inc	dptr
      00A591 F0               [24] 1650 	movx	@dptr,a
      00A592 85 41 82         [24] 1651 	mov	dpl, _raw_hid_receive_sloc0_1_0
      00A595 85 42 83         [24] 1652 	mov	dph, (_raw_hid_receive_sloc0_1_0 + 1)
      00A598 C0 07            [24] 1653 	push	ar7
      00A59A C0 06            [24] 1654 	push	ar6
      00A59C C0 03            [24] 1655 	push	ar3
      00A59E 12 81 FA         [24] 1656 	lcall	_dynamic_keymap_macro_get_buffer
      00A5A1 D0 03            [24] 1657 	pop	ar3
      00A5A3 D0 06            [24] 1658 	pop	ar6
      00A5A5 D0 07            [24] 1659 	pop	ar7
                                   1660 ;	quantum/via.c:443: break;
      00A5A7 02 A7 9E         [24] 1661 	ljmp	00171$
                                   1662 ;	quantum/via.c:445: case id_dynamic_keymap_macro_set_buffer: {
      00A5AA                       1663 00144$:
                                   1664 ;	quantum/via.c:448: if (!vial_unlocked) {
      00A5AA 90 0C 07         [24] 1665 	mov	dptr,#_vial_unlocked
      00A5AD E0               [24] 1666 	movx	a,@dptr
      00A5AE 70 01            [24] 1667 	jnz	00146$
                                   1668 ;	quantum/via.c:450: return;
      00A5B0 22               [24] 1669 	ret
      00A5B1                       1670 00146$:
                                   1671 ;	quantum/via.c:456: uint16_t offset = (command_data[0] << 8) | command_data[1];
      00A5B1 C0 03            [24] 1672 	push	ar3
      00A5B3 12 A7 C0         [24] 1673 	lcall	_ak820_outline_0011
      00A5B6 89 47            [24] 1674 	mov	_raw_hid_receive_sloc3_1_0,r1
      00A5B8 8A 48            [24] 1675 	mov	(_raw_hid_receive_sloc3_1_0 + 1),r2
                                   1676 ;	quantum/via.c:457: uint16_t size   = command_data[2]; // size <= 28
      00A5BA 12 A7 B7         [24] 1677 	lcall	_ak820_outline_0010
      00A5BD F5 41            [12] 1678 	mov	_raw_hid_receive_sloc0_1_0, a
      00A5BF 75 42 00         [24] 1679 	mov	(_raw_hid_receive_sloc0_1_0 + 1),#0x00
                                   1680 ;	quantum/via.c:461: if (size > 28 || size > length - 4 || !dynamic_keymap_macro_set_buffer(offset, size, &command_data[3])) return;
      00A5C2 85 41 49         [24] 1681 	mov	_raw_hid_receive_sloc4_1_0,_raw_hid_receive_sloc0_1_0
      00A5C5 85 42 4A         [24] 1682 	mov	(_raw_hid_receive_sloc4_1_0 + 1),(_raw_hid_receive_sloc0_1_0 + 1)
      00A5C8 C3               [12] 1683 	clr	c
      00A5C9 74 1C            [12] 1684 	mov	a,#0x1c
      00A5CB 95 49            [12] 1685 	subb	a,_raw_hid_receive_sloc4_1_0
      00A5CD E4               [12] 1686 	clr	a
      00A5CE 95 4A            [12] 1687 	subb	a,(_raw_hid_receive_sloc4_1_0 + 1)
      00A5D0 D0 03            [24] 1688 	pop	ar3
      00A5D2 40 4F            [24] 1689 	jc	00147$
                                   1690 ;	free result
      00A5D4 8B 01            [24] 1691 	mov	ar1,r3
      00A5D6 7A 00            [12] 1692 	mov	r2,#0x00
      00A5D8 E9               [12] 1693 	mov	a,r1
      00A5D9 24 FC            [12] 1694 	add	a,#0xfc
      00A5DB F9               [12] 1695 	mov	r1,a
      00A5DC EA               [12] 1696 	mov	a,r2
      00A5DD 34 FF            [12] 1697 	addc	a,#0xff
      00A5DF FA               [12] 1698 	mov	r2,a
      00A5E0 C3               [12] 1699 	clr	c
      00A5E1 E9               [12] 1700 	mov	a,r1
      00A5E2 95 49            [12] 1701 	subb	a,_raw_hid_receive_sloc4_1_0
      00A5E4 EA               [12] 1702 	mov	a,r2
      00A5E5 95 4A            [12] 1703 	subb	a,(_raw_hid_receive_sloc4_1_0 + 1)
      00A5E7 40 3A            [24] 1704 	jc	00147$
                                   1705 ;	free result
      00A5E9 74 04            [12] 1706 	mov	a,#0x04
      00A5EB 2E               [12] 1707 	add	a, r6
      00A5EC F9               [12] 1708 	mov	r1,a
      00A5ED E4               [12] 1709 	clr	a
      00A5EE 3F               [12] 1710 	addc	a, r7
      00A5EF F8               [12] 1711 	mov	r0,a
      00A5F0 7A 00            [12] 1712 	mov	r2,#0x00
      00A5F2 90 09 16         [24] 1713 	mov	dptr,#_dynamic_keymap_macro_set_buffer_PARM_2
      00A5F5 E5 41            [12] 1714 	mov	a,_raw_hid_receive_sloc0_1_0
      00A5F7 F0               [24] 1715 	movx	@dptr,a
      00A5F8 E5 42            [12] 1716 	mov	a,(_raw_hid_receive_sloc0_1_0 + 1)
      00A5FA A3               [24] 1717 	inc	dptr
      00A5FB F0               [24] 1718 	movx	@dptr,a
      00A5FC 90 09 18         [24] 1719 	mov	dptr,#_dynamic_keymap_macro_set_buffer_PARM_3
      00A5FF E9               [12] 1720 	mov	a,r1
      00A600 F0               [24] 1721 	movx	@dptr,a
      00A601 E8               [12] 1722 	mov	a,r0
      00A602 A3               [24] 1723 	inc	dptr
      00A603 F0               [24] 1724 	movx	@dptr,a
      00A604 EA               [12] 1725 	mov	a,r2
      00A605 A3               [24] 1726 	inc	dptr
      00A606 F0               [24] 1727 	movx	@dptr,a
      00A607 85 47 82         [24] 1728 	mov	dpl, _raw_hid_receive_sloc3_1_0
      00A60A 85 48 83         [24] 1729 	mov	dph, (_raw_hid_receive_sloc3_1_0 + 1)
      00A60D C0 07            [24] 1730 	push	ar7
      00A60F C0 06            [24] 1731 	push	ar6
      00A611 C0 03            [24] 1732 	push	ar3
      00A613 12 82 54         [24] 1733 	lcall	_dynamic_keymap_macro_set_buffer
      00A616 E5 82            [12] 1734 	mov	a, dpl
      00A618 D0 03            [24] 1735 	pop	ar3
      00A61A D0 06            [24] 1736 	pop	ar6
      00A61C D0 07            [24] 1737 	pop	ar7
      00A61E 60 03            [24] 1738 	jz	00566$
      00A620 02 A7 9E         [24] 1739 	ljmp	00171$
      00A623                       1740 00566$:
      00A623                       1741 00147$:
      00A623 22               [24] 1742 	ret
                                   1743 ;	quantum/via.c:468: case id_dynamic_keymap_macro_reset: {
      00A624                       1744 00151$:
                                   1745 ;	quantum/via.c:470: if (!vial_unlocked) return;
      00A624 90 0C 07         [24] 1746 	mov	dptr,#_vial_unlocked
      00A627 E0               [24] 1747 	movx	a,@dptr
      00A628 70 01            [24] 1748 	jnz	00153$
      00A62A 22               [24] 1749 	ret
      00A62B                       1750 00153$:
                                   1751 ;	quantum/via.c:472: dynamic_keymap_macro_reset();
      00A62B C0 07            [24] 1752 	push	ar7
      00A62D C0 06            [24] 1753 	push	ar6
      00A62F C0 03            [24] 1754 	push	ar3
      00A631 12 82 94         [24] 1755 	lcall	_dynamic_keymap_macro_reset
      00A634 D0 03            [24] 1756 	pop	ar3
      00A636 D0 06            [24] 1757 	pop	ar6
      00A638 D0 07            [24] 1758 	pop	ar7
                                   1759 ;	quantum/via.c:473: break;
      00A63A 02 A7 9E         [24] 1760 	ljmp	00171$
                                   1761 ;	quantum/via.c:475: case id_dynamic_keymap_get_layer_count: {
      00A63D                       1762 00154$:
                                   1763 ;	quantum/via.c:476: command_data[0] = dynamic_keymap_get_layer_count();
      00A63D C0 07            [24] 1764 	push	ar7
      00A63F C0 06            [24] 1765 	push	ar6
      00A641 C0 05            [24] 1766 	push	ar5
      00A643 C0 04            [24] 1767 	push	ar4
      00A645 C0 03            [24] 1768 	push	ar3
      00A647 12 7B 87         [24] 1769 	lcall	_dynamic_keymap_get_layer_count
      00A64A AA 82            [24] 1770 	mov	r2, dpl
      00A64C D0 03            [24] 1771 	pop	ar3
      00A64E D0 04            [24] 1772 	pop	ar4
      00A650 D0 05            [24] 1773 	pop	ar5
      00A652 D0 06            [24] 1774 	pop	ar6
      00A654 D0 07            [24] 1775 	pop	ar7
      00A656 8C 82            [24] 1776 	mov	dpl,r4
      00A658 8D 83            [24] 1777 	mov	dph,r5
      00A65A EA               [12] 1778 	mov	a,r2
      00A65B F0               [24] 1779 	movx	@dptr,a
                                   1780 ;	quantum/via.c:477: break;
      00A65C 02 A7 9E         [24] 1781 	ljmp	00171$
                                   1782 ;	quantum/via.c:479: case id_dynamic_keymap_get_buffer: {
      00A65F                       1783 00155$:
                                   1784 ;	quantum/via.c:480: uint16_t offset = (command_data[0] << 8) | command_data[1];
      00A65F C0 03            [24] 1785 	push	ar3
      00A661 12 A7 C0         [24] 1786 	lcall	_ak820_outline_0011
      00A664 89 49            [24] 1787 	mov	_raw_hid_receive_sloc4_1_0,r1
      00A666 8A 4A            [24] 1788 	mov	(_raw_hid_receive_sloc4_1_0 + 1),r2
                                   1789 ;	quantum/via.c:481: uint16_t size   = command_data[2]; // size <= 28
      00A668 12 A7 B7         [24] 1790 	lcall	_ak820_outline_0010
      00A66B FB               [12] 1791 	mov	r3,a
                                   1792 ;	quantum/via.c:482: if (size <= 28)
      00A66C 8B 47            [24] 1793 	mov	_raw_hid_receive_sloc3_1_0,r3
      00A66E 75 48 00         [24] 1794 	mov	(_raw_hid_receive_sloc3_1_0 + 1),#0x00
      00A671 C3               [12] 1795 	clr	c
      00A672 74 1C            [12] 1796 	mov	a,#0x1c
      00A674 9B               [12] 1797 	subb	a,r3
      00A675 D0 03            [24] 1798 	pop	ar3
      00A677 50 03            [24] 1799 	jnc	00568$
      00A679 02 A7 9E         [24] 1800 	ljmp	00171$
      00A67C                       1801 00568$:
                                   1802 ;	free result
                                   1803 ;	quantum/via.c:483: dynamic_keymap_get_buffer(offset, size, &command_data[3]);
      00A67C 74 04            [12] 1804 	mov	a,#0x04
      00A67E 2E               [12] 1805 	add	a, r6
      00A67F F9               [12] 1806 	mov	r1,a
      00A680 E4               [12] 1807 	clr	a
      00A681 3F               [12] 1808 	addc	a, r7
      00A682 F8               [12] 1809 	mov	r0,a
      00A683 7A 00            [12] 1810 	mov	r2,#0x00
      00A685 90 08 F8         [24] 1811 	mov	dptr,#_dynamic_keymap_get_buffer_PARM_2
      00A688 E5 47            [12] 1812 	mov	a,_raw_hid_receive_sloc3_1_0
      00A68A F0               [24] 1813 	movx	@dptr,a
      00A68B E5 48            [12] 1814 	mov	a,(_raw_hid_receive_sloc3_1_0 + 1)
      00A68D A3               [24] 1815 	inc	dptr
      00A68E F0               [24] 1816 	movx	@dptr,a
      00A68F 90 08 FA         [24] 1817 	mov	dptr,#_dynamic_keymap_get_buffer_PARM_3
      00A692 E9               [12] 1818 	mov	a,r1
      00A693 F0               [24] 1819 	movx	@dptr,a
      00A694 E8               [12] 1820 	mov	a,r0
      00A695 A3               [24] 1821 	inc	dptr
      00A696 F0               [24] 1822 	movx	@dptr,a
      00A697 EA               [12] 1823 	mov	a,r2
      00A698 A3               [24] 1824 	inc	dptr
      00A699 F0               [24] 1825 	movx	@dptr,a
      00A69A 85 49 82         [24] 1826 	mov	dpl, _raw_hid_receive_sloc4_1_0
      00A69D 85 4A 83         [24] 1827 	mov	dph, (_raw_hid_receive_sloc4_1_0 + 1)
      00A6A0 C0 07            [24] 1828 	push	ar7
      00A6A2 C0 06            [24] 1829 	push	ar6
      00A6A4 C0 03            [24] 1830 	push	ar3
      00A6A6 12 7F 6D         [24] 1831 	lcall	_dynamic_keymap_get_buffer
      00A6A9 D0 03            [24] 1832 	pop	ar3
      00A6AB D0 06            [24] 1833 	pop	ar6
      00A6AD D0 07            [24] 1834 	pop	ar7
                                   1835 ;	quantum/via.c:484: break;
      00A6AF 02 A7 9E         [24] 1836 	ljmp	00171$
                                   1837 ;	quantum/via.c:486: case id_dynamic_keymap_set_buffer: {
      00A6B2                       1838 00158$:
                                   1839 ;	quantum/via.c:487: uint16_t offset = (command_data[0] << 8) | command_data[1];
      00A6B2 8C 82            [24] 1840 	mov	dpl,r4
      00A6B4 8D 83            [24] 1841 	mov	dph,r5
      00A6B6 E0               [24] 1842 	movx	a,@dptr
      00A6B7 FD               [12] 1843 	mov	r5,a
      00A6B8 7C 00            [12] 1844 	mov	r4,#0x00
      00A6BA 8E 82            [24] 1845 	mov	dpl,r6
      00A6BC 8F 83            [24] 1846 	mov	dph,r7
      00A6BE A3               [24] 1847 	inc	dptr
      00A6BF A3               [24] 1848 	inc	dptr
      00A6C0 E0               [24] 1849 	movx	a,@dptr
      00A6C1 7A 00            [12] 1850 	mov	r2,#0x00
      00A6C3 42 04            [12] 1851 	orl	ar4,a
      00A6C5 EA               [12] 1852 	mov	a,r2
      00A6C6 42 05            [12] 1853 	orl	ar5,a
      00A6C8 8C 49            [24] 1854 	mov	_raw_hid_receive_sloc4_1_0,r4
      00A6CA 8D 4A            [24] 1855 	mov	(_raw_hid_receive_sloc4_1_0 + 1),r5
                                   1856 ;	quantum/via.c:488: uint16_t size   = command_data[2]; // size <= 28
      00A6CC 12 A7 B7         [24] 1857 	lcall	_ak820_outline_0010
      00A6CF F9               [12] 1858 	mov	r1,a
      00A6D0 7A 00            [12] 1859 	mov	r2,#0x00
                                   1860 ;	quantum/via.c:489: if (size <= 28)
      00A6D2 89 00            [24] 1861 	mov	ar0,r1
      00A6D4 E8               [12] 1862 	mov	a,r0
      00A6D5 24 E3            [12] 1863 	add	a,#0xff - 0x1c
      00A6D7 50 03            [24] 1864 	jnc	00569$
      00A6D9 02 A7 9E         [24] 1865 	ljmp	00171$
      00A6DC                       1866 00569$:
                                   1867 ;	free result
                                   1868 ;	quantum/via.c:490: dynamic_keymap_set_buffer(offset, size, &command_data[3]);
      00A6DC C0 03            [24] 1869 	push	ar3
      00A6DE 74 04            [12] 1870 	mov	a,#0x04
      00A6E0 2E               [12] 1871 	add	a, r6
      00A6E1 F8               [12] 1872 	mov	r0,a
      00A6E2 E4               [12] 1873 	clr	a
      00A6E3 3F               [12] 1874 	addc	a, r7
      00A6E4 FB               [12] 1875 	mov	r3,a
      00A6E5 7D 00            [12] 1876 	mov	r5,#0x00
      00A6E7 90 08 FF         [24] 1877 	mov	dptr,#_dynamic_keymap_set_buffer_PARM_2
      00A6EA E9               [12] 1878 	mov	a,r1
      00A6EB F0               [24] 1879 	movx	@dptr,a
      00A6EC EA               [12] 1880 	mov	a,r2
      00A6ED A3               [24] 1881 	inc	dptr
      00A6EE F0               [24] 1882 	movx	@dptr,a
      00A6EF 90 09 01         [24] 1883 	mov	dptr,#_dynamic_keymap_set_buffer_PARM_3
      00A6F2 E8               [12] 1884 	mov	a,r0
      00A6F3 F0               [24] 1885 	movx	@dptr,a
      00A6F4 EB               [12] 1886 	mov	a,r3
      00A6F5 A3               [24] 1887 	inc	dptr
      00A6F6 F0               [24] 1888 	movx	@dptr,a
      00A6F7 ED               [12] 1889 	mov	a,r5
      00A6F8 A3               [24] 1890 	inc	dptr
      00A6F9 F0               [24] 1891 	movx	@dptr,a
      00A6FA 85 49 82         [24] 1892 	mov	dpl, _raw_hid_receive_sloc4_1_0
      00A6FD 85 4A 83         [24] 1893 	mov	dph, (_raw_hid_receive_sloc4_1_0 + 1)
      00A700 C0 07            [24] 1894 	push	ar7
      00A702 C0 06            [24] 1895 	push	ar6
      00A704 C0 03            [24] 1896 	push	ar3
      00A706 12 7F BD         [24] 1897 	lcall	_dynamic_keymap_set_buffer
      00A709 D0 03            [24] 1898 	pop	ar3
      00A70B D0 06            [24] 1899 	pop	ar6
      00A70D D0 07            [24] 1900 	pop	ar7
                                   1901 ;	quantum/via.c:491: break;
      00A70F D0 03            [24] 1902 	pop	ar3
      00A711 02 A7 9E         [24] 1903 	ljmp	00171$
                                   1904 ;	quantum/via.c:495: case id_bootloader_jump: {
      00A714                       1905 00161$:
                                   1906 ;	quantum/via.c:497: if (!vial_unlocked)
      00A714 90 0C 07         [24] 1907 	mov	dptr,#_vial_unlocked
      00A717 E0               [24] 1908 	movx	a,@dptr
      00A718 70 03            [24] 1909 	jnz	00570$
      00A71A 02 A7 9E         [24] 1910 	ljmp	00171$
      00A71D                       1911 00570$:
                                   1912 ;	quantum/via.c:501: raw_hid_send(data, length);
      00A71D 8E 02            [24] 1913 	mov	ar2,r6
      00A71F 8F 04            [24] 1914 	mov	ar4,r7
      00A721 7D 00            [12] 1915 	mov	r5,#0x00
      00A723 90 05 86         [24] 1916 	mov	dptr,#_raw_hid_send_PARM_2
      00A726 EB               [12] 1917 	mov	a,r3
      00A727 F0               [24] 1918 	movx	@dptr,a
      00A728 8A 82            [24] 1919 	mov	dpl, r2
      00A72A 8C 83            [24] 1920 	mov	dph, r4
      00A72C 8D F0            [24] 1921 	mov	b, r5
      00A72E C0 07            [24] 1922 	push	ar7
      00A730 C0 06            [24] 1923 	push	ar6
      00A732 C0 03            [24] 1924 	push	ar3
      00A734 12 41 BE         [24] 1925 	lcall	_raw_hid_send
      00A737 D0 03            [24] 1926 	pop	ar3
      00A739 D0 06            [24] 1927 	pop	ar6
      00A73B D0 07            [24] 1928 	pop	ar7
                                   1929 ;	quantum/via.c:503: wait_ms(100);
      00A73D 7D 64            [12] 1930 	mov	r5,#0x64
      00A73F                       1931 00176$:
      00A73F ED               [12] 1932 	mov	a,r5
      00A740 60 09            [24] 1933 	jz	00166$
      00A742 90 00 01         [24] 1934 	mov	dptr,#0x0001
      00A745 12 52 5E         [24] 1935 	lcall	_mDelaymS
      00A748 1D               [12] 1936 	dec	r5
      00A749 80 F4            [24] 1937 	sjmp	00176$
      00A74B                       1938 00166$:
                                   1939 ;	quantum/via.c:504: bootloader_jump();
      00A74B C0 07            [24] 1940 	push	ar7
      00A74D C0 06            [24] 1941 	push	ar6
      00A74F C0 03            [24] 1942 	push	ar3
      00A751 12 34 94         [24] 1943 	lcall	_bootloader_jump
      00A754 D0 03            [24] 1944 	pop	ar3
      00A756 D0 06            [24] 1945 	pop	ar6
      00A758 D0 07            [24] 1946 	pop	ar7
                                   1947 ;	quantum/via.c:505: break;
                                   1948 ;	quantum/via.c:509: case id_vial_prefix: {
      00A75A 80 42            [24] 1949 	sjmp	00171$
      00A75C                       1950 00168$:
                                   1951 ;	quantum/via.c:510: vial_handle_cmd(data, length);
      00A75C 8E 02            [24] 1952 	mov	ar2,r6
      00A75E 8F 04            [24] 1953 	mov	ar4,r7
      00A760 7D 00            [12] 1954 	mov	r5,#0x00
      00A762 90 0A 63         [24] 1955 	mov	dptr,#_vial_handle_cmd_PARM_2
      00A765 EB               [12] 1956 	mov	a,r3
      00A766 F0               [24] 1957 	movx	@dptr,a
      00A767 8A 82            [24] 1958 	mov	dpl, r2
      00A769 8C 83            [24] 1959 	mov	dph, r4
      00A76B 8D F0            [24] 1960 	mov	b, r5
      00A76D C0 07            [24] 1961 	push	ar7
      00A76F C0 06            [24] 1962 	push	ar6
      00A771 C0 03            [24] 1963 	push	ar3
      00A773 12 AA 03         [24] 1964 	lcall	_vial_handle_cmd
      00A776 D0 03            [24] 1965 	pop	ar3
      00A778 D0 06            [24] 1966 	pop	ar6
      00A77A D0 07            [24] 1967 	pop	ar7
                                   1968 ;	quantum/via.c:511: break;
                                   1969 ;	quantum/via.c:514: default: {
      00A77C 80 20            [24] 1970 	sjmp	00171$
      00A77E                       1971 00169$:
                                   1972 ;	quantum/via.c:516: raw_hid_receive_kb(data, length);
      00A77E 8E 02            [24] 1973 	mov	ar2,r6
      00A780 8F 04            [24] 1974 	mov	ar4,r7
      00A782 7D 00            [12] 1975 	mov	r5,#0x00
      00A784 90 0A 4F         [24] 1976 	mov	dptr,#_raw_hid_receive_kb_PARM_2
      00A787 EB               [12] 1977 	mov	a,r3
      00A788 F0               [24] 1978 	movx	@dptr,a
      00A789 8A 82            [24] 1979 	mov	dpl, r2
      00A78B 8C 83            [24] 1980 	mov	dph, r4
      00A78D 8D F0            [24] 1981 	mov	b, r5
      00A78F C0 07            [24] 1982 	push	ar7
      00A791 C0 06            [24] 1983 	push	ar6
      00A793 C0 03            [24] 1984 	push	ar3
      00A795 12 A1 59         [24] 1985 	lcall	_raw_hid_receive_kb
      00A798 D0 03            [24] 1986 	pop	ar3
      00A79A D0 06            [24] 1987 	pop	ar6
      00A79C D0 07            [24] 1988 	pop	ar7
                                   1989 ;	quantum/via.c:521: skip:
      00A79E                       1990 00171$:
                                   1991 ;	quantum/via.c:525: raw_hid_send(data, length);
      00A79E 7D 00            [12] 1992 	mov	r5,#0x00
      00A7A0 90 05 86         [24] 1993 	mov	dptr,#_raw_hid_send_PARM_2
      00A7A3 EB               [12] 1994 	mov	a,r3
      00A7A4 F0               [24] 1995 	movx	@dptr,a
      00A7A5 8E 82            [24] 1996 	mov	dpl, r6
      00A7A7 8F 83            [24] 1997 	mov	dph, r7
      00A7A9 8D F0            [24] 1998 	mov	b, r5
                                   1999 ;	quantum/via.c:526: }
      00A7AB 02 41 BE         [24] 2000 	ljmp	_raw_hid_send
                                   2001 	.area CSEG    (CODE)
                                   2002 	.area CONST   (CODE)
                                   2003 	.area XINIT   (CODE)
                                   2004 	.area CABS    (ABS,CODE)
                                   2005 
                                   2006 ; Experimental exact instruction outlining.
                                   2007 	.globl _ak820_outline_0002
                                   2008 	.globl _ak820_outline_0006
                                   2009 	.globl _ak820_outline_0010
                                   2010 	.globl _ak820_outline_0011
                                   2011 	.globl _ak820_outline_0012
                                   2012 	.globl _ak820_outline_0018
                                   2013 	.globl _ak820_outline_0021
                                   2014 	.globl _ak820_outline_0028
                                   2015 
                                   2016 	.area CSEG (CODE)
                                   2017 ; function ak820_outline_0006
      00A7AE                       2018 _ak820_outline_0006:
      00A7AE 8E 82            [24] 2019 	mov	dpl,r6
      00A7B0 8F 83            [24] 2020 	mov	dph,r7
      00A7B2 A3               [24] 2021 	inc	dptr
      00A7B3 A3               [24] 2022 	inc	dptr
      00A7B4 A3               [24] 2023 	inc	dptr
      00A7B5 A3               [24] 2024 	inc	dptr
      00A7B6 22               [24] 2025 	ret
                                   2026 
                                   2027 	.area CSEG (CODE)
                                   2028 ; function ak820_outline_0010
      00A7B7                       2029 _ak820_outline_0010:
      00A7B7 8E 82            [24] 2030 	mov	dpl,r6
      00A7B9 8F 83            [24] 2031 	mov	dph,r7
      00A7BB A3               [24] 2032 	inc	dptr
      00A7BC A3               [24] 2033 	inc	dptr
      00A7BD A3               [24] 2034 	inc	dptr
      00A7BE E0               [24] 2035 	movx	a,@dptr
      00A7BF 22               [24] 2036 	ret
                                   2037 
                                   2038 	.area CSEG (CODE)
                                   2039 ; function ak820_outline_0011
      00A7C0                       2040 _ak820_outline_0011:
      00A7C0 8C 82            [24] 2041 	mov	dpl,r4
      00A7C2 8D 83            [24] 2042 	mov	dph,r5
      00A7C4 E0               [24] 2043 	movx	a,@dptr
      00A7C5 FA               [12] 2044 	mov	r2,a
      00A7C6 79 00            [12] 2045 	mov	r1,#0x00
      00A7C8 8E 82            [24] 2046 	mov	dpl,r6
      00A7CA 8F 83            [24] 2047 	mov	dph,r7
      00A7CC A3               [24] 2048 	inc	dptr
      00A7CD A3               [24] 2049 	inc	dptr
      00A7CE E0               [24] 2050 	movx	a,@dptr
      00A7CF 7B 00            [12] 2051 	mov	r3,#0x00
      00A7D1 42 01            [12] 2052 	orl	ar1,a
      00A7D3 EB               [12] 2053 	mov	a,r3
      00A7D4 42 02            [12] 2054 	orl	ar2,a
      00A7D6 22               [24] 2055 	ret
                                   2056 
                                   2057 	.area CSEG (CODE)
                                   2058 ; function ak820_outline_0021
      00A7D7                       2059 _ak820_outline_0021:
      00A7D7 EB               [12] 2060 	mov	a,r3
      00A7D8 F0               [24] 2061 	movx	@dptr,a
      00A7D9 88 82            [24] 2062 	mov	dpl,r0
      00A7DB 89 83            [24] 2063 	mov	dph,r1
      00A7DD 8A F0            [24] 2064 	mov	b,r2
      00A7DF 22               [24] 2065 	ret
