                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module dynamic_keymap
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _dynamic_keymap_encoder_to_eeprom_address
                                     12 	.globl _ak820_macro_reset
                                     13 	.globl _ak820_macro_write
                                     14 	.globl _ak820_macro_length
                                     15 	.globl _ak820_macro_ready
                                     16 	.globl _send_char
                                     17 	.globl _keycode_at_encodermap_location_raw
                                     18 	.globl _keycode_at_keymap_location_raw
                                     19 	.globl _vial_keycode_tap
                                     20 	.globl _vial_keycode_up
                                     21 	.globl _vial_keycode_down
                                     22 	.globl _tap_code
                                     23 	.globl _unregister_code
                                     24 	.globl _register_code
                                     25 	.globl _mDelaymS
                                     26 	.globl _eeprom_update_byte
                                     27 	.globl _eeprom_write_block
                                     28 	.globl _eeprom_read_block
                                     29 	.globl _eeprom_read_byte
                                     30 	.globl _ADC_START
                                     31 	.globl _S0_R_FIFO
                                     32 	.globl _S0_T_FIFO
                                     33 	.globl _S0_FREE
                                     34 	.globl _S0_IF_BYTE
                                     35 	.globl _S0_IF_FIRST
                                     36 	.globl _S0_IF_OV
                                     37 	.globl _S0_FST_ACT
                                     38 	.globl _CP_RL2
                                     39 	.globl _C_T2
                                     40 	.globl _TR2
                                     41 	.globl _EXEN2
                                     42 	.globl _TCLK
                                     43 	.globl _RCLK
                                     44 	.globl _EXF2
                                     45 	.globl _CAP1F
                                     46 	.globl _TF2
                                     47 	.globl _RI
                                     48 	.globl _TI
                                     49 	.globl _RB8
                                     50 	.globl _TB8
                                     51 	.globl _REN
                                     52 	.globl _SM2
                                     53 	.globl _SM1
                                     54 	.globl _SM0
                                     55 	.globl _IT0
                                     56 	.globl _IE0
                                     57 	.globl _IT1
                                     58 	.globl _IE1
                                     59 	.globl _TR0
                                     60 	.globl _TF0
                                     61 	.globl _TR1
                                     62 	.globl _TF1
                                     63 	.globl _P4_0
                                     64 	.globl _P4_1
                                     65 	.globl _P4_2
                                     66 	.globl _P4_3
                                     67 	.globl _P4_4
                                     68 	.globl _P4_5
                                     69 	.globl _P4_6
                                     70 	.globl _RXD
                                     71 	.globl _TXD
                                     72 	.globl _INT0
                                     73 	.globl _INT1
                                     74 	.globl _T0
                                     75 	.globl _T1
                                     76 	.globl _MOSI1
                                     77 	.globl _MISO1
                                     78 	.globl _SCK1
                                     79 	.globl _P3_0
                                     80 	.globl _P3_1
                                     81 	.globl _P3_2
                                     82 	.globl _P3_3
                                     83 	.globl _P3_4
                                     84 	.globl _P3_5
                                     85 	.globl _P3_6
                                     86 	.globl _P3_7
                                     87 	.globl _CAP1_
                                     88 	.globl _T2_
                                     89 	.globl _CAP2_
                                     90 	.globl _T2EX_
                                     91 	.globl _RXD1
                                     92 	.globl _TXD1
                                     93 	.globl _P2_0
                                     94 	.globl _P2_1
                                     95 	.globl _P2_2
                                     96 	.globl _P2_3
                                     97 	.globl _P2_4
                                     98 	.globl _P2_5
                                     99 	.globl _P2_6
                                    100 	.globl _P2_7
                                    101 	.globl _AIN0
                                    102 	.globl _AIN1
                                    103 	.globl _AIN2
                                    104 	.globl _AIN3
                                    105 	.globl _AIN4
                                    106 	.globl _AIN5
                                    107 	.globl _AIN6
                                    108 	.globl _AIN7
                                    109 	.globl _CAP1
                                    110 	.globl _T2
                                    111 	.globl _CAP2
                                    112 	.globl _T2EX
                                    113 	.globl _INT0_
                                    114 	.globl _SCS
                                    115 	.globl _MOSI
                                    116 	.globl _MISO
                                    117 	.globl _SCK
                                    118 	.globl _RXD1_
                                    119 	.globl _TXD1_
                                    120 	.globl _P1_0
                                    121 	.globl _P1_1
                                    122 	.globl _P1_2
                                    123 	.globl _P1_3
                                    124 	.globl _P1_4
                                    125 	.globl _P1_5
                                    126 	.globl _P1_6
                                    127 	.globl _P1_7
                                    128 	.globl _AIN8
                                    129 	.globl _AIN9
                                    130 	.globl _AIN10
                                    131 	.globl _AIN11
                                    132 	.globl _AIN12
                                    133 	.globl _AIN13
                                    134 	.globl _RXD_
                                    135 	.globl _TXD_
                                    136 	.globl _SCL0
                                    137 	.globl _SDA0
                                    138 	.globl _P0_0
                                    139 	.globl _P0_1
                                    140 	.globl _P0_2
                                    141 	.globl _P0_3
                                    142 	.globl _P0_4
                                    143 	.globl _P0_5
                                    144 	.globl _P0_6
                                    145 	.globl _P0_7
                                    146 	.globl _IE_SPI0
                                    147 	.globl _IE_USB
                                    148 	.globl _IE_ADC
                                    149 	.globl _IE_UART1
                                    150 	.globl _IE_PWM_I2C
                                    151 	.globl _IE_GPIO
                                    152 	.globl _IE_WDOG
                                    153 	.globl _PX0
                                    154 	.globl _PT0
                                    155 	.globl _PX1
                                    156 	.globl _PT1
                                    157 	.globl _PS
                                    158 	.globl _PT2
                                    159 	.globl _PL_FLAG
                                    160 	.globl _PH_FLAG
                                    161 	.globl _EX0
                                    162 	.globl _ET0
                                    163 	.globl _EX1
                                    164 	.globl _ET1
                                    165 	.globl _ES
                                    166 	.globl _ET2
                                    167 	.globl _E_DIS
                                    168 	.globl _EA
                                    169 	.globl _P
                                    170 	.globl _F1
                                    171 	.globl _OV
                                    172 	.globl _RS0
                                    173 	.globl _RS1
                                    174 	.globl _F0
                                    175 	.globl _AC
                                    176 	.globl _CY
                                    177 	.globl _I2CS_INT_ST
                                    178 	.globl _I2CX_INT
                                    179 	.globl _LED_STATUS
                                    180 	.globl _LED_DMA_H
                                    181 	.globl _LED_DMA_L
                                    182 	.globl _LED_DMA
                                    183 	.globl _LED_PWM_OE
                                    184 	.globl _LED_COMMON
                                    185 	.globl _ADC_CHAN
                                    186 	.globl _ADC_DAT_H
                                    187 	.globl _ADC_DAT_L
                                    188 	.globl _ADC_DAT
                                    189 	.globl _ADC_CTRL
                                    190 	.globl _SPI1_CK_SE
                                    191 	.globl _SPI1_CTRL
                                    192 	.globl _SPI1_DATA
                                    193 	.globl _SPI1_STAT
                                    194 	.globl _SIF1
                                    195 	.globl _SBAUD1
                                    196 	.globl _SBUF1
                                    197 	.globl _SCON1
                                    198 	.globl _SPI0_SETUP
                                    199 	.globl _SPI0_CK_SE
                                    200 	.globl _SPI0_CTRL
                                    201 	.globl _SPI0_DATA
                                    202 	.globl _SPI0_STAT
                                    203 	.globl _T2CAP1H
                                    204 	.globl _T2CAP1L
                                    205 	.globl _T2CAP1
                                    206 	.globl _TH2
                                    207 	.globl _TL2
                                    208 	.globl _T2COUNT
                                    209 	.globl _RCAP2H
                                    210 	.globl _RCAP2L
                                    211 	.globl _RCAP2
                                    212 	.globl _T2MOD
                                    213 	.globl _T2CON
                                    214 	.globl _SBUF
                                    215 	.globl _SCON
                                    216 	.globl _TH1
                                    217 	.globl _TH0
                                    218 	.globl _TL1
                                    219 	.globl _TL0
                                    220 	.globl _TMOD
                                    221 	.globl _TCON
                                    222 	.globl _XBUS_AUX
                                    223 	.globl _P7
                                    224 	.globl _P6_DIR
                                    225 	.globl _P6_OUT_PU
                                    226 	.globl _P6_IN
                                    227 	.globl _P5_DIR
                                    228 	.globl _P5_OUT_PU
                                    229 	.globl _P5_IN
                                    230 	.globl _P4_LED_KEY
                                    231 	.globl _P4_DIR_PU
                                    232 	.globl _P4_MOD_OC
                                    233 	.globl _P4
                                    234 	.globl _P3_DIR_PU
                                    235 	.globl _P3_MOD_OC
                                    236 	.globl _P3
                                    237 	.globl _P2_DIR_PU
                                    238 	.globl _P2_MOD_OC
                                    239 	.globl _P2
                                    240 	.globl _P1_DIR_PU
                                    241 	.globl _P1_MOD_OC
                                    242 	.globl _P1
                                    243 	.globl _P0_DIR_PU
                                    244 	.globl _P0_MOD_OC
                                    245 	.globl _P0
                                    246 	.globl _ROM_CTRL
                                    247 	.globl _ROM_DATA_HH
                                    248 	.globl _ROM_DATA_HL
                                    249 	.globl _ROM_DATA_HI
                                    250 	.globl _ROM_ADDR_H
                                    251 	.globl _ROM_ADDR_L
                                    252 	.globl _ROM_ADDR
                                    253 	.globl _GPIO_IE
                                    254 	.globl _IP_EX
                                    255 	.globl _IE_EX
                                    256 	.globl _IP
                                    257 	.globl _IE
                                    258 	.globl _WDOG_COUNT
                                    259 	.globl _RESET_KEEP
                                    260 	.globl _WAKE_CTRL
                                    261 	.globl _CLOCK_CFG
                                    262 	.globl _POWER_CFG
                                    263 	.globl _PCON
                                    264 	.globl _GLOBAL_CFG
                                    265 	.globl _SAFE_MOD
                                    266 	.globl _DPH
                                    267 	.globl _DPL
                                    268 	.globl _SP
                                    269 	.globl _A_INV
                                    270 	.globl _B
                                    271 	.globl _ACC
                                    272 	.globl _PSW
                                    273 	.globl _dynamic_keymap_macro_set_buffer_PARM_3
                                    274 	.globl _dynamic_keymap_macro_set_buffer_PARM_2
                                    275 	.globl _dynamic_keymap_macro_get_buffer_PARM_3
                                    276 	.globl _dynamic_keymap_macro_get_buffer_PARM_2
                                    277 	.globl _keycode_at_encodermap_location_PARM_3
                                    278 	.globl _keycode_at_encodermap_location_PARM_2
                                    279 	.globl _keycode_at_keymap_location_PARM_3
                                    280 	.globl _keycode_at_keymap_location_PARM_2
                                    281 	.globl _dynamic_keymap_set_buffer_PARM_3
                                    282 	.globl _dynamic_keymap_set_buffer_PARM_2
                                    283 	.globl _dynamic_keymap_get_buffer_PARM_3
                                    284 	.globl _dynamic_keymap_get_buffer_PARM_2
                                    285 	.globl _dynamic_keymap_set_encoder_PARM_4
                                    286 	.globl _dynamic_keymap_set_encoder_PARM_3
                                    287 	.globl _dynamic_keymap_set_encoder_PARM_2
                                    288 	.globl _dynamic_keymap_get_encoder_PARM_3
                                    289 	.globl _dynamic_keymap_get_encoder_PARM_2
                                    290 	.globl _dynamic_keymap_encoder_to_eeprom_address_PARM_2
                                    291 	.globl _dynamic_keymap_set_keycode_PARM_4
                                    292 	.globl _dynamic_keymap_set_keycode_PARM_3
                                    293 	.globl _dynamic_keymap_set_keycode_PARM_2
                                    294 	.globl _dynamic_keymap_get_keycode_PARM_3
                                    295 	.globl _dynamic_keymap_get_keycode_PARM_2
                                    296 	.globl _dynamic_keymap_key_to_eeprom_address_PARM_3
                                    297 	.globl _dynamic_keymap_key_to_eeprom_address_PARM_2
                                    298 	.globl _dynamic_keymap_get_layer_count
                                    299 	.globl _dynamic_keymap_key_to_eeprom_address
                                    300 	.globl _dynamic_keymap_get_keycode
                                    301 	.globl _dynamic_keymap_set_keycode
                                    302 	.globl _dynamic_keymap_get_encoder
                                    303 	.globl _dynamic_keymap_set_encoder
                                    304 	.globl _dynamic_keymap_reset
                                    305 	.globl _dynamic_keymap_get_buffer
                                    306 	.globl _dynamic_keymap_set_buffer
                                    307 	.globl _keycode_at_keymap_location
                                    308 	.globl _keycode_at_encodermap_location
                                    309 	.globl _dynamic_keymap_macro_get_count
                                    310 	.globl _dynamic_keymap_macro_get_buffer_size
                                    311 	.globl _dynamic_keymap_macro_get_buffer
                                    312 	.globl _dynamic_keymap_macro_set_buffer
                                    313 	.globl _dynamic_keymap_macro_reset
                                    314 	.globl _dynamic_keymap_macro_send
                                    315 ;--------------------------------------------------------
                                    316 ; special function registers
                                    317 ;--------------------------------------------------------
                                    318 	.area RSEG    (ABS,DATA)
      000000                        319 	.org 0x0000
                           0000D0   320 _PSW	=	0x00d0
                           0000E0   321 _ACC	=	0x00e0
                           0000F0   322 _B	=	0x00f0
                           0000FD   323 _A_INV	=	0x00fd
                           000081   324 _SP	=	0x0081
                           000082   325 _DPL	=	0x0082
                           000083   326 _DPH	=	0x0083
                           0000A1   327 _SAFE_MOD	=	0x00a1
                           0000B1   328 _GLOBAL_CFG	=	0x00b1
                           000087   329 _PCON	=	0x0087
                           0000BA   330 _POWER_CFG	=	0x00ba
                           0000B9   331 _CLOCK_CFG	=	0x00b9
                           0000A9   332 _WAKE_CTRL	=	0x00a9
                           0000FE   333 _RESET_KEEP	=	0x00fe
                           0000FF   334 _WDOG_COUNT	=	0x00ff
                           0000A8   335 _IE	=	0x00a8
                           0000B8   336 _IP	=	0x00b8
                           0000E8   337 _IE_EX	=	0x00e8
                           0000E9   338 _IP_EX	=	0x00e9
                           0000B2   339 _GPIO_IE	=	0x00b2
                           008584   340 _ROM_ADDR	=	0x8584
                           000084   341 _ROM_ADDR_L	=	0x0084
                           000085   342 _ROM_ADDR_H	=	0x0085
                           008F8E   343 _ROM_DATA_HI	=	0x8f8e
                           00008E   344 _ROM_DATA_HL	=	0x008e
                           00008F   345 _ROM_DATA_HH	=	0x008f
                           000086   346 _ROM_CTRL	=	0x0086
                           000080   347 _P0	=	0x0080
                           0000C4   348 _P0_MOD_OC	=	0x00c4
                           0000C5   349 _P0_DIR_PU	=	0x00c5
                           000090   350 _P1	=	0x0090
                           000092   351 _P1_MOD_OC	=	0x0092
                           000093   352 _P1_DIR_PU	=	0x0093
                           0000A0   353 _P2	=	0x00a0
                           000094   354 _P2_MOD_OC	=	0x0094
                           000095   355 _P2_DIR_PU	=	0x0095
                           0000B0   356 _P3	=	0x00b0
                           000096   357 _P3_MOD_OC	=	0x0096
                           000097   358 _P3_DIR_PU	=	0x0097
                           0000C0   359 _P4	=	0x00c0
                           0000C2   360 _P4_MOD_OC	=	0x00c2
                           0000C3   361 _P4_DIR_PU	=	0x00c3
                           0000C1   362 _P4_LED_KEY	=	0x00c1
                           0000AA   363 _P5_IN	=	0x00aa
                           0000AB   364 _P5_OUT_PU	=	0x00ab
                           0000AC   365 _P5_DIR	=	0x00ac
                           0000AD   366 _P6_IN	=	0x00ad
                           0000AE   367 _P6_OUT_PU	=	0x00ae
                           0000AF   368 _P6_DIR	=	0x00af
                           0000F1   369 _P7	=	0x00f1
                           0000A2   370 _XBUS_AUX	=	0x00a2
                           000088   371 _TCON	=	0x0088
                           000089   372 _TMOD	=	0x0089
                           00008A   373 _TL0	=	0x008a
                           00008B   374 _TL1	=	0x008b
                           00008C   375 _TH0	=	0x008c
                           00008D   376 _TH1	=	0x008d
                           000098   377 _SCON	=	0x0098
                           000099   378 _SBUF	=	0x0099
                           0000C8   379 _T2CON	=	0x00c8
                           0000C9   380 _T2MOD	=	0x00c9
                           00CBCA   381 _RCAP2	=	0xcbca
                           0000CA   382 _RCAP2L	=	0x00ca
                           0000CB   383 _RCAP2H	=	0x00cb
                           00CDCC   384 _T2COUNT	=	0xcdcc
                           0000CC   385 _TL2	=	0x00cc
                           0000CD   386 _TH2	=	0x00cd
                           00CFCE   387 _T2CAP1	=	0xcfce
                           0000CE   388 _T2CAP1L	=	0x00ce
                           0000CF   389 _T2CAP1H	=	0x00cf
                           0000F8   390 _SPI0_STAT	=	0x00f8
                           0000F9   391 _SPI0_DATA	=	0x00f9
                           0000FA   392 _SPI0_CTRL	=	0x00fa
                           0000FB   393 _SPI0_CK_SE	=	0x00fb
                           0000FC   394 _SPI0_SETUP	=	0x00fc
                           0000BC   395 _SCON1	=	0x00bc
                           0000BD   396 _SBUF1	=	0x00bd
                           0000BE   397 _SBAUD1	=	0x00be
                           0000BF   398 _SIF1	=	0x00bf
                           0000B4   399 _SPI1_STAT	=	0x00b4
                           0000B5   400 _SPI1_DATA	=	0x00b5
                           0000B6   401 _SPI1_CTRL	=	0x00b6
                           0000B7   402 _SPI1_CK_SE	=	0x00b7
                           0000F3   403 _ADC_CTRL	=	0x00f3
                           00F5F4   404 _ADC_DAT	=	0xf5f4
                           0000F4   405 _ADC_DAT_L	=	0x00f4
                           0000F5   406 _ADC_DAT_H	=	0x00f5
                           0000F6   407 _ADC_CHAN	=	0x00f6
                           0000A6   408 _LED_COMMON	=	0x00a6
                           0000A7   409 _LED_PWM_OE	=	0x00a7
                           00C7C6   410 _LED_DMA	=	0xc7c6
                           0000C6   411 _LED_DMA_L	=	0x00c6
                           0000C7   412 _LED_DMA_H	=	0x00c7
                           0000F7   413 _LED_STATUS	=	0x00f7
                           0000B3   414 _I2CX_INT	=	0x00b3
                           0000BB   415 _I2CS_INT_ST	=	0x00bb
                                    416 ;--------------------------------------------------------
                                    417 ; special function bits
                                    418 ;--------------------------------------------------------
                                    419 	.area RSEG    (ABS,DATA)
      000000                        420 	.org 0x0000
                           0000D7   421 _CY	=	0x00d7
                           0000D6   422 _AC	=	0x00d6
                           0000D5   423 _F0	=	0x00d5
                           0000D4   424 _RS1	=	0x00d4
                           0000D3   425 _RS0	=	0x00d3
                           0000D2   426 _OV	=	0x00d2
                           0000D1   427 _F1	=	0x00d1
                           0000D0   428 _P	=	0x00d0
                           0000AF   429 _EA	=	0x00af
                           0000AE   430 _E_DIS	=	0x00ae
                           0000AD   431 _ET2	=	0x00ad
                           0000AC   432 _ES	=	0x00ac
                           0000AB   433 _ET1	=	0x00ab
                           0000AA   434 _EX1	=	0x00aa
                           0000A9   435 _ET0	=	0x00a9
                           0000A8   436 _EX0	=	0x00a8
                           0000BF   437 _PH_FLAG	=	0x00bf
                           0000BE   438 _PL_FLAG	=	0x00be
                           0000BD   439 _PT2	=	0x00bd
                           0000BC   440 _PS	=	0x00bc
                           0000BB   441 _PT1	=	0x00bb
                           0000BA   442 _PX1	=	0x00ba
                           0000B9   443 _PT0	=	0x00b9
                           0000B8   444 _PX0	=	0x00b8
                           0000EF   445 _IE_WDOG	=	0x00ef
                           0000EE   446 _IE_GPIO	=	0x00ee
                           0000ED   447 _IE_PWM_I2C	=	0x00ed
                           0000EC   448 _IE_UART1	=	0x00ec
                           0000EB   449 _IE_ADC	=	0x00eb
                           0000E9   450 _IE_USB	=	0x00e9
                           0000E8   451 _IE_SPI0	=	0x00e8
                           000087   452 _P0_7	=	0x0087
                           000086   453 _P0_6	=	0x0086
                           000085   454 _P0_5	=	0x0085
                           000084   455 _P0_4	=	0x0084
                           000083   456 _P0_3	=	0x0083
                           000082   457 _P0_2	=	0x0082
                           000081   458 _P0_1	=	0x0081
                           000080   459 _P0_0	=	0x0080
                           000081   460 _SDA0	=	0x0081
                           000080   461 _SCL0	=	0x0080
                           000083   462 _TXD_	=	0x0083
                           000082   463 _RXD_	=	0x0082
                           000085   464 _AIN13	=	0x0085
                           000084   465 _AIN12	=	0x0084
                           000083   466 _AIN11	=	0x0083
                           000082   467 _AIN10	=	0x0082
                           000081   468 _AIN9	=	0x0081
                           000080   469 _AIN8	=	0x0080
                           000097   470 _P1_7	=	0x0097
                           000096   471 _P1_6	=	0x0096
                           000095   472 _P1_5	=	0x0095
                           000094   473 _P1_4	=	0x0094
                           000093   474 _P1_3	=	0x0093
                           000092   475 _P1_2	=	0x0092
                           000091   476 _P1_1	=	0x0091
                           000090   477 _P1_0	=	0x0090
                           000097   478 _TXD1_	=	0x0097
                           000096   479 _RXD1_	=	0x0096
                           000097   480 _SCK	=	0x0097
                           000096   481 _MISO	=	0x0096
                           000095   482 _MOSI	=	0x0095
                           000094   483 _SCS	=	0x0094
                           000092   484 _INT0_	=	0x0092
                           000091   485 _T2EX	=	0x0091
                           000091   486 _CAP2	=	0x0091
                           000090   487 _T2	=	0x0090
                           000090   488 _CAP1	=	0x0090
                           000097   489 _AIN7	=	0x0097
                           000096   490 _AIN6	=	0x0096
                           000095   491 _AIN5	=	0x0095
                           000094   492 _AIN4	=	0x0094
                           000093   493 _AIN3	=	0x0093
                           000092   494 _AIN2	=	0x0092
                           000091   495 _AIN1	=	0x0091
                           000090   496 _AIN0	=	0x0090
                           0000A7   497 _P2_7	=	0x00a7
                           0000A6   498 _P2_6	=	0x00a6
                           0000A5   499 _P2_5	=	0x00a5
                           0000A4   500 _P2_4	=	0x00a4
                           0000A3   501 _P2_3	=	0x00a3
                           0000A2   502 _P2_2	=	0x00a2
                           0000A1   503 _P2_1	=	0x00a1
                           0000A0   504 _P2_0	=	0x00a0
                           0000A7   505 _TXD1	=	0x00a7
                           0000A6   506 _RXD1	=	0x00a6
                           0000A5   507 _T2EX_	=	0x00a5
                           0000A5   508 _CAP2_	=	0x00a5
                           0000A4   509 _T2_	=	0x00a4
                           0000A4   510 _CAP1_	=	0x00a4
                           0000B7   511 _P3_7	=	0x00b7
                           0000B6   512 _P3_6	=	0x00b6
                           0000B5   513 _P3_5	=	0x00b5
                           0000B4   514 _P3_4	=	0x00b4
                           0000B3   515 _P3_3	=	0x00b3
                           0000B2   516 _P3_2	=	0x00b2
                           0000B1   517 _P3_1	=	0x00b1
                           0000B0   518 _P3_0	=	0x00b0
                           0000B7   519 _SCK1	=	0x00b7
                           0000B6   520 _MISO1	=	0x00b6
                           0000B5   521 _MOSI1	=	0x00b5
                           0000B5   522 _T1	=	0x00b5
                           0000B4   523 _T0	=	0x00b4
                           0000B3   524 _INT1	=	0x00b3
                           0000B2   525 _INT0	=	0x00b2
                           0000B1   526 _TXD	=	0x00b1
                           0000B0   527 _RXD	=	0x00b0
                           0000C6   528 _P4_6	=	0x00c6
                           0000C5   529 _P4_5	=	0x00c5
                           0000C4   530 _P4_4	=	0x00c4
                           0000C3   531 _P4_3	=	0x00c3
                           0000C2   532 _P4_2	=	0x00c2
                           0000C1   533 _P4_1	=	0x00c1
                           0000C0   534 _P4_0	=	0x00c0
                           00008F   535 _TF1	=	0x008f
                           00008E   536 _TR1	=	0x008e
                           00008D   537 _TF0	=	0x008d
                           00008C   538 _TR0	=	0x008c
                           00008B   539 _IE1	=	0x008b
                           00008A   540 _IT1	=	0x008a
                           000089   541 _IE0	=	0x0089
                           000088   542 _IT0	=	0x0088
                           00009F   543 _SM0	=	0x009f
                           00009E   544 _SM1	=	0x009e
                           00009D   545 _SM2	=	0x009d
                           00009C   546 _REN	=	0x009c
                           00009B   547 _TB8	=	0x009b
                           00009A   548 _RB8	=	0x009a
                           000099   549 _TI	=	0x0099
                           000098   550 _RI	=	0x0098
                           0000CF   551 _TF2	=	0x00cf
                           0000CF   552 _CAP1F	=	0x00cf
                           0000CE   553 _EXF2	=	0x00ce
                           0000CD   554 _RCLK	=	0x00cd
                           0000CC   555 _TCLK	=	0x00cc
                           0000CB   556 _EXEN2	=	0x00cb
                           0000CA   557 _TR2	=	0x00ca
                           0000C9   558 _C_T2	=	0x00c9
                           0000C8   559 _CP_RL2	=	0x00c8
                           0000FF   560 _S0_FST_ACT	=	0x00ff
                           0000FE   561 _S0_IF_OV	=	0x00fe
                           0000FD   562 _S0_IF_FIRST	=	0x00fd
                           0000FC   563 _S0_IF_BYTE	=	0x00fc
                           0000FB   564 _S0_FREE	=	0x00fb
                           0000FA   565 _S0_T_FIFO	=	0x00fa
                           0000F8   566 _S0_R_FIFO	=	0x00f8
                           0000F7   567 _ADC_START	=	0x00f7
                                    568 ;--------------------------------------------------------
                                    569 ; overlayable register banks
                                    570 ;--------------------------------------------------------
                                    571 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        572 	.ds 8
                                    573 ;--------------------------------------------------------
                                    574 ; internal ram data
                                    575 ;--------------------------------------------------------
                                    576 	.area DSEG    (DATA)
      000031                        577 _dynamic_keymap_set_encoder_sloc0_1_0:
      000031                        578 	.ds 2
      000033                        579 _ak820_dynamic_read_buffer_sloc0_1_0:
      000033                        580 	.ds 3
      000036                        581 _ak820_dynamic_read_buffer_sloc1_1_0:
      000036                        582 	.ds 1
      000037                        583 _dynamic_keymap_set_buffer_sloc0_1_0:
      000037                        584 	.ds 3
      00003A                        585 _dynamic_keymap_set_buffer_sloc1_1_0:
      00003A                        586 	.ds 2
      00003C                        587 _dynamic_keymap_set_buffer_sloc2_1_0:
      00003C                        588 	.ds 2
      00003E                        589 _dynamic_keymap_set_buffer_sloc3_1_0:
      00003E                        590 	.ds 1
      00003F                        591 _dynamic_keymap_macro_get_buffer_sloc0_1_0:
      00003F                        592 	.ds 2
                                    593 ;--------------------------------------------------------
                                    594 ; overlayable items in internal ram
                                    595 ;--------------------------------------------------------
                                    596 ;--------------------------------------------------------
                                    597 ; indirectly addressable internal ram data
                                    598 ;--------------------------------------------------------
                                    599 	.area ISEG    (DATA)
                                    600 ;--------------------------------------------------------
                                    601 ; absolute internal ram data
                                    602 ;--------------------------------------------------------
                                    603 	.area IABS    (ABS,DATA)
                                    604 	.area IABS    (ABS,DATA)
                                    605 ;--------------------------------------------------------
                                    606 ; bit data
                                    607 ;--------------------------------------------------------
                                    608 	.area BSEG    (BIT)
                                    609 ;--------------------------------------------------------
                                    610 ; paged external ram data
                                    611 ;--------------------------------------------------------
                                    612 	.area PSEG    (PAG,XDATA)
                                    613 ;--------------------------------------------------------
                                    614 ; uninitialized external ram data
                                    615 ;--------------------------------------------------------
                                    616 	.area XSEG    (XDATA)
      0008D6                        617 _dynamic_keymap_key_to_eeprom_address_PARM_2:
      0008D6                        618 	.ds 1
      0008D7                        619 _dynamic_keymap_key_to_eeprom_address_PARM_3:
      0008D7                        620 	.ds 1
      0008D8                        621 _dynamic_keymap_key_to_eeprom_address_layer_10000_271:
      0008D8                        622 	.ds 1
      0008D9                        623 _dynamic_keymap_get_keycode_PARM_2:
      0008D9                        624 	.ds 1
      0008DA                        625 _dynamic_keymap_get_keycode_PARM_3:
      0008DA                        626 	.ds 1
      0008DB                        627 _dynamic_keymap_get_keycode_layer_10000_273:
      0008DB                        628 	.ds 1
      0008DC                        629 _dynamic_keymap_set_keycode_PARM_2:
      0008DC                        630 	.ds 1
      0008DD                        631 _dynamic_keymap_set_keycode_PARM_3:
      0008DD                        632 	.ds 1
      0008DE                        633 _dynamic_keymap_set_keycode_PARM_4:
      0008DE                        634 	.ds 2
      0008E0                        635 _dynamic_keymap_set_keycode_layer_10000_277:
      0008E0                        636 	.ds 1
      0008E1                        637 _dynamic_keymap_encoder_to_eeprom_address_PARM_2:
      0008E1                        638 	.ds 1
      0008E2                        639 _dynamic_keymap_encoder_to_eeprom_address_layer_10000_281:
      0008E2                        640 	.ds 1
      0008E3                        641 _dynamic_keymap_get_encoder_PARM_2:
      0008E3                        642 	.ds 1
      0008E4                        643 _dynamic_keymap_get_encoder_PARM_3:
      0008E4                        644 	.ds 1
      0008E5                        645 _dynamic_keymap_get_encoder_layer_10000_283:
      0008E5                        646 	.ds 1
      0008E6                        647 _dynamic_keymap_set_encoder_PARM_2:
      0008E6                        648 	.ds 1
      0008E7                        649 _dynamic_keymap_set_encoder_PARM_3:
      0008E7                        650 	.ds 1
      0008E8                        651 _dynamic_keymap_set_encoder_PARM_4:
      0008E8                        652 	.ds 2
      0008EA                        653 _dynamic_keymap_set_encoder_layer_10000_287:
      0008EA                        654 	.ds 1
      0008EB                        655 _dynamic_keymap_reset_vial_unlocked_prev_10000_292:
      0008EB                        656 	.ds 1
      0008EC                        657 _ak820_dynamic_read_buffer_PARM_2:
      0008EC                        658 	.ds 2
      0008EE                        659 _ak820_dynamic_read_buffer_PARM_3:
      0008EE                        660 	.ds 2
      0008F0                        661 _ak820_dynamic_read_buffer_PARM_4:
      0008F0                        662 	.ds 2
      0008F2                        663 _ak820_dynamic_read_buffer_PARM_5:
      0008F2                        664 	.ds 3
      0008F5                        665 _ak820_dynamic_read_buffer_base_10000_301:
      0008F5                        666 	.ds 2
      0008F7                        667 _ak820_dynamic_read_buffer_available_10000_302:
      0008F7                        668 	.ds 1
      0008F8                        669 _dynamic_keymap_get_buffer_PARM_2:
      0008F8                        670 	.ds 2
      0008FA                        671 _dynamic_keymap_get_buffer_PARM_3:
      0008FA                        672 	.ds 3
      0008FD                        673 _dynamic_keymap_get_buffer_offset_10000_308:
      0008FD                        674 	.ds 2
      0008FF                        675 _dynamic_keymap_set_buffer_PARM_2:
      0008FF                        676 	.ds 2
      000901                        677 _dynamic_keymap_set_buffer_PARM_3:
      000901                        678 	.ds 3
      000904                        679 _dynamic_keymap_set_buffer_offset_10000_310:
      000904                        680 	.ds 2
      000906                        681 _dynamic_keymap_set_buffer_chk_offset_30001_317:
      000906                        682 	.ds 1
      000907                        683 _dynamic_keymap_set_buffer_chk_sz_30001_317:
      000907                        684 	.ds 1
      000908                        685 _dynamic_keymap_set_buffer_i_40001_324:
      000908                        686 	.ds 1
      000909                        687 _keycode_at_keymap_location_PARM_2:
      000909                        688 	.ds 1
      00090A                        689 _keycode_at_keymap_location_PARM_3:
      00090A                        690 	.ds 1
      00090B                        691 _keycode_at_keymap_location_layer_num_10000_328:
      00090B                        692 	.ds 1
      00090C                        693 _keycode_at_encodermap_location_PARM_2:
      00090C                        694 	.ds 1
      00090D                        695 _keycode_at_encodermap_location_PARM_3:
      00090D                        696 	.ds 1
      00090E                        697 _keycode_at_encodermap_location_layer_num_10000_332:
      00090E                        698 	.ds 1
      00090F                        699 _dynamic_keymap_macro_get_buffer_PARM_2:
      00090F                        700 	.ds 2
      000911                        701 _dynamic_keymap_macro_get_buffer_PARM_3:
      000911                        702 	.ds 3
      000914                        703 _dynamic_keymap_macro_get_buffer_offset_10000_340:
      000914                        704 	.ds 2
      000916                        705 _dynamic_keymap_macro_set_buffer_PARM_2:
      000916                        706 	.ds 2
      000918                        707 _dynamic_keymap_macro_set_buffer_PARM_3:
      000918                        708 	.ds 3
      00091B                        709 _dynamic_keymap_macro_set_buffer_offset_10000_342:
      00091B                        710 	.ds 2
      00091D                        711 _decode_keycode_kc_10000_346:
      00091D                        712 	.ds 2
      00091F                        713 _dynamic_keymap_macro_send_id_10000_349:
      00091F                        714 	.ds 1
      000920                        715 _dynamic_keymap_macro_send_sending_10000_350:
      000920                        716 	.ds 1
      000921                        717 _dynamic_keymap_macro_send_p_10001_355:
      000921                        718 	.ds 3
      000924                        719 _dynamic_keymap_macro_send_data_10003_362:
      000924                        720 	.ds 4
                                    721 ;--------------------------------------------------------
                                    722 ; absolute external ram data
                                    723 ;--------------------------------------------------------
                                    724 	.area XABS    (ABS,XDATA)
                                    725 ;--------------------------------------------------------
                                    726 ; initialized external ram data
                                    727 ;--------------------------------------------------------
                                    728 	.area XISEG   (XDATA)
                                    729 	.area HOME    (CODE)
                                    730 	.area GSINIT0 (CODE)
                                    731 	.area GSINIT1 (CODE)
                                    732 	.area GSINIT2 (CODE)
                                    733 	.area GSINIT3 (CODE)
                                    734 	.area GSINIT4 (CODE)
                                    735 	.area GSINIT5 (CODE)
                                    736 	.area GSINIT  (CODE)
                                    737 	.area GSFINAL (CODE)
                                    738 	.area CSEG    (CODE)
                                    739 ;--------------------------------------------------------
                                    740 ; global & static initialisations
                                    741 ;--------------------------------------------------------
                                    742 	.area HOME    (CODE)
                                    743 	.area GSINIT  (CODE)
                                    744 	.area GSFINAL (CODE)
                                    745 	.area GSINIT  (CODE)
                                    746 ;--------------------------------------------------------
                                    747 ; Home
                                    748 ;--------------------------------------------------------
                                    749 	.area HOME    (CODE)
                                    750 	.area HOME    (CODE)
                                    751 ;--------------------------------------------------------
                                    752 ; code
                                    753 ;--------------------------------------------------------
                                    754 	.area CSEG    (CODE)
                                    755 ;------------------------------------------------------------
                                    756 ;Allocation info for local variables in function 'dynamic_keymap_get_layer_count'
                                    757 ;------------------------------------------------------------
                                    758 ;	quantum/dynamic_keymap.c:155: uint8_t dynamic_keymap_get_layer_count(void) {
                                    759 ;	-----------------------------------------
                                    760 ;	 function dynamic_keymap_get_layer_count
                                    761 ;	-----------------------------------------
      007B87                        762 _dynamic_keymap_get_layer_count:
                           000007   763 	ar7 = 0x07
                           000006   764 	ar6 = 0x06
                           000005   765 	ar5 = 0x05
                           000004   766 	ar4 = 0x04
                           000003   767 	ar3 = 0x03
                           000002   768 	ar2 = 0x02
                           000001   769 	ar1 = 0x01
                           000000   770 	ar0 = 0x00
                                    771 ;	quantum/dynamic_keymap.c:156: return DYNAMIC_KEYMAP_LAYER_COUNT;
      007B87 75 82 06         [24]  772 	mov	dpl, #0x06
                                    773 ;	quantum/dynamic_keymap.c:157: }
      007B8A 22               [24]  774 	ret
                                    775 ;------------------------------------------------------------
                                    776 ;Allocation info for local variables in function 'dynamic_keymap_key_to_eeprom_address'
                                    777 ;------------------------------------------------------------
                                    778 ;row           Allocated with name '_dynamic_keymap_key_to_eeprom_address_PARM_2'
                                    779 ;column        Allocated with name '_dynamic_keymap_key_to_eeprom_address_PARM_3'
                                    780 ;layer         Allocated with name '_dynamic_keymap_key_to_eeprom_address_layer_10000_271'
                                    781 ;------------------------------------------------------------
                                    782 ;	quantum/dynamic_keymap.c:159: void *dynamic_keymap_key_to_eeprom_address(uint8_t layer, uint8_t row, uint8_t column) {
                                    783 ;	-----------------------------------------
                                    784 ;	 function dynamic_keymap_key_to_eeprom_address
                                    785 ;	-----------------------------------------
      007B8B                        786 _dynamic_keymap_key_to_eeprom_address:
      007B8B E5 82            [12]  787 	mov	a,dpl
      007B8D 90 08 D8         [24]  788 	mov	dptr,#_dynamic_keymap_key_to_eeprom_address_layer_10000_271
      007B90 F0               [24]  789 	movx	@dptr,a
                                    790 ;	quantum/dynamic_keymap.c:161: return ((uint8_t *)DYNAMIC_KEYMAP_EEPROM_ADDR) + (layer * MATRIX_ROWS * MATRIX_COLS * 2) + (row * MATRIX_COLS * 2) + (column * 2);
      007B91 E0               [24]  791 	movx	a,@dptr
      007B92 FF               [12]  792 	mov	r7,a
      007B93 7E 00            [12]  793 	mov	r6,#0x00
      007B95 74 40            [12]  794 	mov	a,#0x40
      007B97 2E               [12]  795 	add	a, r6
      007B98 FE               [12]  796 	mov	r6,a
      007B99 E4               [12]  797 	clr	a
      007B9A 3F               [12]  798 	addc	a, r7
      007B9B FF               [12]  799 	mov	r7,a
      007B9C 7D 00            [12]  800 	mov	r5,#0x00
      007B9E 90 08 D6         [24]  801 	mov	dptr,#_dynamic_keymap_key_to_eeprom_address_PARM_2
      007BA1 E0               [24]  802 	movx	a,@dptr
      007BA2 75 F0 10         [24]  803 	mov	b,#0x10
      007BA5 A4               [48]  804 	mul	ab
      007BA6 2E               [12]  805 	add	a, r6
      007BA7 FE               [12]  806 	mov	r6,a
      007BA8 EF               [12]  807 	mov	a,r7
      007BA9 35 F0            [12]  808 	addc	a, b
      007BAB FF               [12]  809 	mov	r7,a
      007BAC 90 08 D7         [24]  810 	mov	dptr,#_dynamic_keymap_key_to_eeprom_address_PARM_3
      007BAF E0               [24]  811 	movx	a,@dptr
      007BB0 7C 00            [12]  812 	mov	r4,#0x00
      007BB2 25 E0            [12]  813 	add	a,acc
      007BB4 FB               [12]  814 	mov	r3,a
      007BB5 EC               [12]  815 	mov	a,r4
      007BB6 33               [12]  816 	rlc	a
      007BB7 FC               [12]  817 	mov	r4,a
      007BB8 EB               [12]  818 	mov	a,r3
      007BB9 2E               [12]  819 	add	a, r6
      007BBA FE               [12]  820 	mov	r6,a
      007BBB EC               [12]  821 	mov	a,r4
      007BBC 3F               [12]  822 	addc	a, r7
      007BBD FF               [12]  823 	mov	r7,a
      007BBE 8E 82            [24]  824 	mov	dpl, r6
      007BC0 8F 83            [24]  825 	mov	dph, r7
      007BC2 8D F0            [24]  826 	mov	b, r5
                                    827 ;	quantum/dynamic_keymap.c:162: }
      007BC4 22               [24]  828 	ret
                                    829 ;------------------------------------------------------------
                                    830 ;Allocation info for local variables in function 'dynamic_keymap_get_keycode'
                                    831 ;------------------------------------------------------------
                                    832 ;row           Allocated with name '_dynamic_keymap_get_keycode_PARM_2'
                                    833 ;column        Allocated with name '_dynamic_keymap_get_keycode_PARM_3'
                                    834 ;layer         Allocated with name '_dynamic_keymap_get_keycode_layer_10000_273'
                                    835 ;address       Allocated with name '_dynamic_keymap_get_keycode_address_10001_276'
                                    836 ;keycode       Allocated with name '_dynamic_keymap_get_keycode_keycode_10001_276'
                                    837 ;------------------------------------------------------------
                                    838 ;	quantum/dynamic_keymap.c:164: uint16_t dynamic_keymap_get_keycode(uint8_t layer, uint8_t row, uint8_t column) {
                                    839 ;	-----------------------------------------
                                    840 ;	 function dynamic_keymap_get_keycode
                                    841 ;	-----------------------------------------
      007BC5                        842 _dynamic_keymap_get_keycode:
      007BC5 E5 82            [12]  843 	mov	a,dpl
      007BC7 90 08 DB         [24]  844 	mov	dptr,#_dynamic_keymap_get_keycode_layer_10000_273
      007BCA F0               [24]  845 	movx	@dptr,a
                                    846 ;	quantum/dynamic_keymap.c:165: if (layer >= DYNAMIC_KEYMAP_LAYER_COUNT || row >= MATRIX_ROWS || column >= MATRIX_COLS) return KC_NO;
      007BCB E0               [24]  847 	movx	a,@dptr
      007BCC FF               [12]  848 	mov	r7,a
      007BCD BF 06 00         [24]  849 	cjne	r7,#0x06,00121$
      007BD0                        850 00121$:
      007BD0 50 14            [24]  851 	jnc	00101$
      007BD2 90 08 D9         [24]  852 	mov	dptr,#_dynamic_keymap_get_keycode_PARM_2
      007BD5 E0               [24]  853 	movx	a,@dptr
      007BD6 FE               [12]  854 	mov	r6,a
      007BD7 BE 10 00         [24]  855 	cjne	r6,#0x10,00123$
      007BDA                        856 00123$:
      007BDA 50 0A            [24]  857 	jnc	00101$
      007BDC 90 08 DA         [24]  858 	mov	dptr,#_dynamic_keymap_get_keycode_PARM_3
      007BDF E0               [24]  859 	movx	a,@dptr
      007BE0 FD               [12]  860 	mov	r5,a
      007BE1 BD 08 00         [24]  861 	cjne	r5,#0x08,00125$
      007BE4                        862 00125$:
      007BE4 40 04            [24]  863 	jc	00102$
      007BE6                        864 00101$:
      007BE6 90 00 00         [24]  865 	mov	dptr,#0x0000
      007BE9 22               [24]  866 	ret
      007BEA                        867 00102$:
                                    868 ;	quantum/dynamic_keymap.c:166: uint8_t *address = dynamic_keymap_key_to_eeprom_address(layer, row, column);
      007BEA 90 08 D6         [24]  869 	mov	dptr,#_dynamic_keymap_key_to_eeprom_address_PARM_2
      007BED EE               [12]  870 	mov	a,r6
      007BEE F0               [24]  871 	movx	@dptr,a
      007BEF 90 08 D7         [24]  872 	mov	dptr,#_dynamic_keymap_key_to_eeprom_address_PARM_3
      007BF2 ED               [12]  873 	mov	a,r5
      007BF3 F0               [24]  874 	movx	@dptr,a
      007BF4 8F 82            [24]  875 	mov	dpl, r7
      007BF6 12 7B 8B         [24]  876 	lcall	_dynamic_keymap_key_to_eeprom_address
                                    877 ;	quantum/dynamic_keymap.c:168: uint16_t keycode = eeprom_read_byte(address) << 8;
      007BF9 AD 82            [24]  878 	mov	r5,dpl
      007BFB AE 83            [24]  879 	mov	r6,dph
      007BFD AF F0            [24]  880 	mov	r7,b
      007BFF 12 43 FC         [24]  881 	lcall	_eeprom_read_byte
      007C02 AB 82            [24]  882 	mov	r3,dpl
      007C04 7C 00            [12]  883 	mov	r4,#0x00
                                    884 ;	quantum/dynamic_keymap.c:169: keycode |= eeprom_read_byte(address + 1);
      007C06 0D               [12]  885 	inc	r5
      007C07 BD 00 01         [24]  886 	cjne	r5,#0x00,00127$
      007C0A 0E               [12]  887 	inc	r6
      007C0B                        888 00127$:
      007C0B 8D 82            [24]  889 	mov	dpl, r5
      007C0D 8E 83            [24]  890 	mov	dph, r6
      007C0F 8F F0            [24]  891 	mov	b, r7
      007C11 12 43 FC         [24]  892 	lcall	_eeprom_read_byte
      007C14 AF 82            [24]  893 	mov	r7, dpl
      007C16 7E 00            [12]  894 	mov	r6,#0x00
      007C18 EF               [12]  895 	mov	a,r7
      007C19 42 04            [12]  896 	orl	ar4,a
      007C1B EE               [12]  897 	mov	a,r6
      007C1C 42 03            [12]  898 	orl	ar3,a
                                    899 ;	quantum/dynamic_keymap.c:170: return keycode;
      007C1E 8C 82            [24]  900 	mov	dpl, r4
      007C20 8B 83            [24]  901 	mov	dph, r3
                                    902 ;	quantum/dynamic_keymap.c:171: }
      007C22 22               [24]  903 	ret
                                    904 ;------------------------------------------------------------
                                    905 ;Allocation info for local variables in function 'dynamic_keymap_set_keycode'
                                    906 ;------------------------------------------------------------
                                    907 ;row           Allocated with name '_dynamic_keymap_set_keycode_PARM_2'
                                    908 ;column        Allocated with name '_dynamic_keymap_set_keycode_PARM_3'
                                    909 ;keycode       Allocated with name '_dynamic_keymap_set_keycode_PARM_4'
                                    910 ;layer         Allocated with name '_dynamic_keymap_set_keycode_layer_10000_277'
                                    911 ;address       Allocated with name '_dynamic_keymap_set_keycode_address_10001_280'
                                    912 ;------------------------------------------------------------
                                    913 ;	quantum/dynamic_keymap.c:173: void dynamic_keymap_set_keycode(uint8_t layer, uint8_t row, uint8_t column, uint16_t keycode) {
                                    914 ;	-----------------------------------------
                                    915 ;	 function dynamic_keymap_set_keycode
                                    916 ;	-----------------------------------------
      007C23                        917 _dynamic_keymap_set_keycode:
      007C23 E5 82            [12]  918 	mov	a,dpl
      007C25 90 08 E0         [24]  919 	mov	dptr,#_dynamic_keymap_set_keycode_layer_10000_277
      007C28 F0               [24]  920 	movx	@dptr,a
                                    921 ;	quantum/dynamic_keymap.c:174: if (layer >= DYNAMIC_KEYMAP_LAYER_COUNT || row >= MATRIX_ROWS || column >= MATRIX_COLS) return;
      007C29 E0               [24]  922 	movx	a,@dptr
      007C2A FF               [12]  923 	mov	r7,a
      007C2B BF 06 00         [24]  924 	cjne	r7,#0x06,00121$
      007C2E                        925 00121$:
      007C2E 50 14            [24]  926 	jnc	00101$
      007C30 90 08 DC         [24]  927 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_2
      007C33 E0               [24]  928 	movx	a,@dptr
      007C34 FE               [12]  929 	mov	r6,a
      007C35 BE 10 00         [24]  930 	cjne	r6,#0x10,00123$
      007C38                        931 00123$:
      007C38 50 0A            [24]  932 	jnc	00101$
      007C3A 90 08 DD         [24]  933 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_3
      007C3D E0               [24]  934 	movx	a,@dptr
      007C3E FD               [12]  935 	mov	r5,a
      007C3F BD 08 00         [24]  936 	cjne	r5,#0x08,00125$
      007C42                        937 00125$:
      007C42 40 01            [24]  938 	jc	00102$
      007C44                        939 00101$:
      007C44 22               [24]  940 	ret
      007C45                        941 00102$:
                                    942 ;	quantum/dynamic_keymap.c:175: uint8_t *address = dynamic_keymap_key_to_eeprom_address(layer, row, column);
      007C45 90 08 D6         [24]  943 	mov	dptr,#_dynamic_keymap_key_to_eeprom_address_PARM_2
      007C48 EE               [12]  944 	mov	a,r6
      007C49 F0               [24]  945 	movx	@dptr,a
      007C4A 90 08 D7         [24]  946 	mov	dptr,#_dynamic_keymap_key_to_eeprom_address_PARM_3
      007C4D ED               [12]  947 	mov	a,r5
      007C4E F0               [24]  948 	movx	@dptr,a
      007C4F 8F 82            [24]  949 	mov	dpl, r7
      007C51 12 7B 8B         [24]  950 	lcall	_dynamic_keymap_key_to_eeprom_address
      007C54 AD 82            [24]  951 	mov	r5, dpl
      007C56 AE 83            [24]  952 	mov	r6, dph
      007C58 AF F0            [24]  953 	mov	r7, b
                                    954 ;	quantum/dynamic_keymap.c:177: eeprom_update_byte(address, (uint8_t)(keycode >> 8));
      007C5A 90 08 DE         [24]  955 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_4
      007C5D E0               [24]  956 	movx	a,@dptr
      007C5E FB               [12]  957 	mov	r3,a
      007C5F A3               [24]  958 	inc	dptr
      007C60 E0               [24]  959 	movx	a,@dptr
      007C61 90 05 B8         [24]  960 	mov	dptr,#_eeprom_update_byte_PARM_2
      007C64 F0               [24]  961 	movx	@dptr,a
      007C65 8D 82            [24]  962 	mov	dpl, r5
      007C67 8E 83            [24]  963 	mov	dph, r6
      007C69 8F F0            [24]  964 	mov	b, r7
      007C6B 12 46 5D         [24]  965 	lcall	_eeprom_update_byte
                                    966 ;	quantum/dynamic_keymap.c:178: eeprom_update_byte(address + 1, (uint8_t)(keycode & 0xFF));
      007C6E 0D               [12]  967 	inc	r5
      007C6F BD 00 01         [24]  968 	cjne	r5,#0x00,00127$
      007C72 0E               [12]  969 	inc	r6
      007C73                        970 00127$:
      007C73 90 05 B8         [24]  971 	mov	dptr,#_eeprom_update_byte_PARM_2
      007C76 EB               [12]  972 	mov	a,r3
      007C77 F0               [24]  973 	movx	@dptr,a
      007C78 8D 82            [24]  974 	mov	dpl, r5
      007C7A 8E 83            [24]  975 	mov	dph, r6
      007C7C 8F F0            [24]  976 	mov	b, r7
                                    977 ;	quantum/dynamic_keymap.c:179: }
      007C7E 02 46 5D         [24]  978 	ljmp	_eeprom_update_byte
                                    979 ;------------------------------------------------------------
                                    980 ;Allocation info for local variables in function 'dynamic_keymap_encoder_to_eeprom_address'
                                    981 ;------------------------------------------------------------
                                    982 ;encoder_id    Allocated with name '_dynamic_keymap_encoder_to_eeprom_address_PARM_2'
                                    983 ;layer         Allocated with name '_dynamic_keymap_encoder_to_eeprom_address_layer_10000_281'
                                    984 ;------------------------------------------------------------
                                    985 ;	quantum/dynamic_keymap.c:182: void *dynamic_keymap_encoder_to_eeprom_address(uint8_t layer, uint8_t encoder_id) {
                                    986 ;	-----------------------------------------
                                    987 ;	 function dynamic_keymap_encoder_to_eeprom_address
                                    988 ;	-----------------------------------------
      007C81                        989 _dynamic_keymap_encoder_to_eeprom_address:
      007C81 E5 82            [12]  990 	mov	a,dpl
      007C83 90 08 E2         [24]  991 	mov	dptr,#_dynamic_keymap_encoder_to_eeprom_address_layer_10000_281
      007C86 F0               [24]  992 	movx	@dptr,a
                                    993 ;	quantum/dynamic_keymap.c:183: return ((uint8_t *)DYNAMIC_KEYMAP_ENCODER_EEPROM_ADDR) + (layer * NUM_ENCODERS * 2 * 2) + (encoder_id * 2 * 2);
      007C87 E0               [24]  994 	movx	a,@dptr
      007C88 75 F0 04         [24]  995 	mov	b,#0x04
      007C8B A4               [48]  996 	mul	ab
      007C8C 24 40            [12]  997 	add	a, #0x40
      007C8E FD               [12]  998 	mov	r5,a
      007C8F 74 06            [12]  999 	mov	a,#0x06
      007C91 35 F0            [12] 1000 	addc	a, b
      007C93 FE               [12] 1001 	mov	r6,a
      007C94 7F 00            [12] 1002 	mov	r7,#0x00
      007C96 90 08 E1         [24] 1003 	mov	dptr,#_dynamic_keymap_encoder_to_eeprom_address_PARM_2
      007C99 E0               [24] 1004 	movx	a,@dptr
      007C9A 75 F0 04         [24] 1005 	mov	b,#0x04
      007C9D A4               [48] 1006 	mul	ab
      007C9E 2D               [12] 1007 	add	a, r5
      007C9F FD               [12] 1008 	mov	r5,a
      007CA0 EE               [12] 1009 	mov	a,r6
      007CA1 35 F0            [12] 1010 	addc	a, b
      007CA3 FE               [12] 1011 	mov	r6,a
      007CA4 8D 82            [24] 1012 	mov	dpl, r5
      007CA6 8E 83            [24] 1013 	mov	dph, r6
      007CA8 8F F0            [24] 1014 	mov	b, r7
                                   1015 ;	quantum/dynamic_keymap.c:184: }
      007CAA 22               [24] 1016 	ret
                                   1017 ;------------------------------------------------------------
                                   1018 ;Allocation info for local variables in function 'dynamic_keymap_get_encoder'
                                   1019 ;------------------------------------------------------------
                                   1020 ;encoder_id    Allocated with name '_dynamic_keymap_get_encoder_PARM_2'
                                   1021 ;clockwise     Allocated with name '_dynamic_keymap_get_encoder_PARM_3'
                                   1022 ;layer         Allocated with name '_dynamic_keymap_get_encoder_layer_10000_283'
                                   1023 ;address       Allocated with name '_dynamic_keymap_get_encoder_address_10001_286'
                                   1024 ;keycode       Allocated with name '_dynamic_keymap_get_encoder_keycode_10001_286'
                                   1025 ;------------------------------------------------------------
                                   1026 ;	quantum/dynamic_keymap.c:186: uint16_t dynamic_keymap_get_encoder(uint8_t layer, uint8_t encoder_id, bool clockwise) {
                                   1027 ;	-----------------------------------------
                                   1028 ;	 function dynamic_keymap_get_encoder
                                   1029 ;	-----------------------------------------
      007CAB                       1030 _dynamic_keymap_get_encoder:
      007CAB E5 82            [12] 1031 	mov	a,dpl
      007CAD 90 08 E5         [24] 1032 	mov	dptr,#_dynamic_keymap_get_encoder_layer_10000_283
      007CB0 F0               [24] 1033 	movx	@dptr,a
                                   1034 ;	quantum/dynamic_keymap.c:187: if (layer >= DYNAMIC_KEYMAP_LAYER_COUNT || encoder_id >= NUM_ENCODERS) return KC_NO;
      007CB1 E0               [24] 1035 	movx	a,@dptr
      007CB2 FF               [12] 1036 	mov	r7,a
      007CB3 BF 06 00         [24] 1037 	cjne	r7,#0x06,00131$
      007CB6                       1038 00131$:
      007CB6 50 0A            [24] 1039 	jnc	00101$
      007CB8 90 08 E3         [24] 1040 	mov	dptr,#_dynamic_keymap_get_encoder_PARM_2
      007CBB E0               [24] 1041 	movx	a,@dptr
      007CBC FE               [12] 1042 	mov	r6,a
      007CBD BE 01 00         [24] 1043 	cjne	r6,#0x01,00133$
      007CC0                       1044 00133$:
      007CC0 40 04            [24] 1045 	jc	00102$
      007CC2                       1046 00101$:
      007CC2 90 00 00         [24] 1047 	mov	dptr,#0x0000
      007CC5 22               [24] 1048 	ret
      007CC6                       1049 00102$:
                                   1050 ;	quantum/dynamic_keymap.c:188: uint8_t *address = dynamic_keymap_encoder_to_eeprom_address(layer, encoder_id);
      007CC6 90 08 E1         [24] 1051 	mov	dptr,#_dynamic_keymap_encoder_to_eeprom_address_PARM_2
      007CC9 E4               [12] 1052 	clr	a
      007CCA F0               [24] 1053 	movx	@dptr,a
      007CCB 8F 82            [24] 1054 	mov	dpl, r7
      007CCD 12 7C 81         [24] 1055 	lcall	_dynamic_keymap_encoder_to_eeprom_address
      007CD0 AD 82            [24] 1056 	mov	r5, dpl
      007CD2 AE 83            [24] 1057 	mov	r6, dph
      007CD4 AF F0            [24] 1058 	mov	r7, b
                                   1059 ;	quantum/dynamic_keymap.c:190: uint16_t keycode = ((uint16_t)eeprom_read_byte(address + (clockwise ? 0 : 2))) << 8;
      007CD6 90 08 E4         [24] 1060 	mov	dptr,#_dynamic_keymap_get_encoder_PARM_3
      007CD9 E0               [24] 1061 	movx	a,@dptr
      007CDA FC               [12] 1062 	mov	r4,a
      007CDB E0               [24] 1063 	movx	a,@dptr
      007CDC 60 04            [24] 1064 	jz	00106$
      007CDE 7B 00            [12] 1065 	mov	r3,#0x00
      007CE0 80 02            [24] 1066 	sjmp	00107$
      007CE2                       1067 00106$:
      007CE2 7B 02            [12] 1068 	mov	r3,#0x02
      007CE4                       1069 00107$:
      007CE4 EB               [12] 1070 	mov	a,r3
      007CE5 2D               [12] 1071 	add	a, r5
      007CE6 F9               [12] 1072 	mov	r1,a
      007CE7 E4               [12] 1073 	clr	a
      007CE8 3E               [12] 1074 	addc	a, r6
      007CE9 FA               [12] 1075 	mov	r2,a
      007CEA 8F 03            [24] 1076 	mov	ar3,r7
      007CEC 89 82            [24] 1077 	mov	dpl, r1
      007CEE 8A 83            [24] 1078 	mov	dph, r2
      007CF0 8B F0            [24] 1079 	mov	b, r3
      007CF2 12 43 FC         [24] 1080 	lcall	_eeprom_read_byte
      007CF5 AA 82            [24] 1081 	mov	r2,dpl
      007CF7 7B 00            [12] 1082 	mov	r3,#0x00
                                   1083 ;	quantum/dynamic_keymap.c:191: keycode |= eeprom_read_byte(address + (clockwise ? 0 : 2) + 1);
      007CF9 EC               [12] 1084 	mov	a,r4
      007CFA 60 04            [24] 1085 	jz	00108$
      007CFC 7C 00            [12] 1086 	mov	r4,#0x00
      007CFE 80 02            [24] 1087 	sjmp	00109$
      007D00                       1088 00108$:
      007D00 7C 02            [12] 1089 	mov	r4,#0x02
      007D02                       1090 00109$:
      007D02 EC               [12] 1091 	mov	a,r4
      007D03 2D               [12] 1092 	add	a, r5
      007D04 FD               [12] 1093 	mov	r5,a
      007D05 E4               [12] 1094 	clr	a
      007D06 3E               [12] 1095 	addc	a, r6
      007D07 FE               [12] 1096 	mov	r6,a
      007D08 0D               [12] 1097 	inc	r5
      007D09 BD 00 01         [24] 1098 	cjne	r5,#0x00,00137$
      007D0C 0E               [12] 1099 	inc	r6
      007D0D                       1100 00137$:
      007D0D 8D 82            [24] 1101 	mov	dpl, r5
      007D0F 8E 83            [24] 1102 	mov	dph, r6
      007D11 8F F0            [24] 1103 	mov	b, r7
      007D13 12 43 FC         [24] 1104 	lcall	_eeprom_read_byte
      007D16 AF 82            [24] 1105 	mov	r7, dpl
      007D18 7E 00            [12] 1106 	mov	r6,#0x00
      007D1A EF               [12] 1107 	mov	a,r7
      007D1B 42 03            [12] 1108 	orl	ar3,a
      007D1D EE               [12] 1109 	mov	a,r6
      007D1E 42 02            [12] 1110 	orl	ar2,a
                                   1111 ;	quantum/dynamic_keymap.c:192: return keycode;
      007D20 8B 82            [24] 1112 	mov	dpl, r3
      007D22 8A 83            [24] 1113 	mov	dph, r2
                                   1114 ;	quantum/dynamic_keymap.c:193: }
      007D24 22               [24] 1115 	ret
                                   1116 ;------------------------------------------------------------
                                   1117 ;Allocation info for local variables in function 'dynamic_keymap_set_encoder'
                                   1118 ;------------------------------------------------------------
                                   1119 ;sloc0         Allocated with name '_dynamic_keymap_set_encoder_sloc0_1_0'
                                   1120 ;encoder_id    Allocated with name '_dynamic_keymap_set_encoder_PARM_2'
                                   1121 ;clockwise     Allocated with name '_dynamic_keymap_set_encoder_PARM_3'
                                   1122 ;keycode       Allocated with name '_dynamic_keymap_set_encoder_PARM_4'
                                   1123 ;layer         Allocated with name '_dynamic_keymap_set_encoder_layer_10000_287'
                                   1124 ;address       Allocated with name '_dynamic_keymap_set_encoder_address_10001_290'
                                   1125 ;------------------------------------------------------------
                                   1126 ;	quantum/dynamic_keymap.c:195: void dynamic_keymap_set_encoder(uint8_t layer, uint8_t encoder_id, bool clockwise, uint16_t keycode) {
                                   1127 ;	-----------------------------------------
                                   1128 ;	 function dynamic_keymap_set_encoder
                                   1129 ;	-----------------------------------------
      007D25                       1130 _dynamic_keymap_set_encoder:
      007D25 E5 82            [12] 1131 	mov	a,dpl
      007D27 90 08 EA         [24] 1132 	mov	dptr,#_dynamic_keymap_set_encoder_layer_10000_287
      007D2A F0               [24] 1133 	movx	@dptr,a
                                   1134 ;	quantum/dynamic_keymap.c:196: if (layer >= DYNAMIC_KEYMAP_LAYER_COUNT || encoder_id >= NUM_ENCODERS) return;
      007D2B E0               [24] 1135 	movx	a,@dptr
      007D2C FF               [12] 1136 	mov	r7,a
      007D2D BF 06 00         [24] 1137 	cjne	r7,#0x06,00131$
      007D30                       1138 00131$:
      007D30 50 0A            [24] 1139 	jnc	00101$
      007D32 90 08 E6         [24] 1140 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_2
      007D35 E0               [24] 1141 	movx	a,@dptr
      007D36 FE               [12] 1142 	mov	r6,a
      007D37 BE 01 00         [24] 1143 	cjne	r6,#0x01,00133$
      007D3A                       1144 00133$:
      007D3A 40 01            [24] 1145 	jc	00102$
      007D3C                       1146 00101$:
      007D3C 22               [24] 1147 	ret
      007D3D                       1148 00102$:
                                   1149 ;	quantum/dynamic_keymap.c:197: uint8_t *address = dynamic_keymap_encoder_to_eeprom_address(layer, encoder_id);
      007D3D 90 08 E1         [24] 1150 	mov	dptr,#_dynamic_keymap_encoder_to_eeprom_address_PARM_2
      007D40 E4               [12] 1151 	clr	a
      007D41 F0               [24] 1152 	movx	@dptr,a
      007D42 8F 82            [24] 1153 	mov	dpl, r7
      007D44 12 7C 81         [24] 1154 	lcall	_dynamic_keymap_encoder_to_eeprom_address
      007D47 AD 82            [24] 1155 	mov	r5, dpl
      007D49 AE 83            [24] 1156 	mov	r6, dph
      007D4B AF F0            [24] 1157 	mov	r7, b
                                   1158 ;	quantum/dynamic_keymap.c:199: eeprom_update_byte(address + (clockwise ? 0 : 2), (uint8_t)(keycode >> 8));
      007D4D 90 08 E7         [24] 1159 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_3
      007D50 E0               [24] 1160 	movx	a,@dptr
      007D51 FC               [12] 1161 	mov	r4,a
      007D52 E0               [24] 1162 	movx	a,@dptr
      007D53 60 04            [24] 1163 	jz	00106$
      007D55 7B 00            [12] 1164 	mov	r3,#0x00
      007D57 80 02            [24] 1165 	sjmp	00107$
      007D59                       1166 00106$:
      007D59 7B 02            [12] 1167 	mov	r3,#0x02
      007D5B                       1168 00107$:
      007D5B EB               [12] 1169 	mov	a,r3
      007D5C 2D               [12] 1170 	add	a, r5
      007D5D F9               [12] 1171 	mov	r1,a
      007D5E E4               [12] 1172 	clr	a
      007D5F 3E               [12] 1173 	addc	a, r6
      007D60 FA               [12] 1174 	mov	r2,a
      007D61 8F 03            [24] 1175 	mov	ar3,r7
      007D63 90 08 E8         [24] 1176 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_4
      007D66 E0               [24] 1177 	movx	a,@dptr
      007D67 F5 31            [12] 1178 	mov	_dynamic_keymap_set_encoder_sloc0_1_0,a
      007D69 A3               [24] 1179 	inc	dptr
      007D6A E0               [24] 1180 	movx	a,@dptr
      007D6B F5 32            [12] 1181 	mov	(_dynamic_keymap_set_encoder_sloc0_1_0 + 1),a
      007D6D 90 05 B8         [24] 1182 	mov	dptr,#_eeprom_update_byte_PARM_2
      007D70 F0               [24] 1183 	movx	@dptr,a
      007D71 89 82            [24] 1184 	mov	dpl, r1
      007D73 8A 83            [24] 1185 	mov	dph, r2
      007D75 8B F0            [24] 1186 	mov	b, r3
      007D77 12 46 5D         [24] 1187 	lcall	_eeprom_update_byte
                                   1188 ;	quantum/dynamic_keymap.c:200: eeprom_update_byte(address + (clockwise ? 0 : 2) + 1, (uint8_t)(keycode & 0xFF));
      007D7A EC               [12] 1189 	mov	a,r4
      007D7B 60 04            [24] 1190 	jz	00108$
      007D7D 7C 00            [12] 1191 	mov	r4,#0x00
      007D7F 80 02            [24] 1192 	sjmp	00109$
      007D81                       1193 00108$:
      007D81 7C 02            [12] 1194 	mov	r4,#0x02
      007D83                       1195 00109$:
      007D83 EC               [12] 1196 	mov	a,r4
      007D84 2D               [12] 1197 	add	a, r5
      007D85 FD               [12] 1198 	mov	r5,a
      007D86 E4               [12] 1199 	clr	a
      007D87 3E               [12] 1200 	addc	a, r6
      007D88 FE               [12] 1201 	mov	r6,a
      007D89 0D               [12] 1202 	inc	r5
      007D8A BD 00 01         [24] 1203 	cjne	r5,#0x00,00137$
      007D8D 0E               [12] 1204 	inc	r6
      007D8E                       1205 00137$:
      007D8E 90 05 B8         [24] 1206 	mov	dptr,#_eeprom_update_byte_PARM_2
      007D91 E5 31            [12] 1207 	mov	a,_dynamic_keymap_set_encoder_sloc0_1_0
      007D93 F0               [24] 1208 	movx	@dptr,a
      007D94 8D 82            [24] 1209 	mov	dpl, r5
      007D96 8E 83            [24] 1210 	mov	dph, r6
      007D98 8F F0            [24] 1211 	mov	b, r7
                                   1212 ;	quantum/dynamic_keymap.c:201: }
      007D9A 02 46 5D         [24] 1213 	ljmp	_eeprom_update_byte
                                   1214 ;------------------------------------------------------------
                                   1215 ;Allocation info for local variables in function 'dynamic_keymap_reset'
                                   1216 ;------------------------------------------------------------
                                   1217 ;vial_unlocked_prev Allocated with name '_dynamic_keymap_reset_vial_unlocked_prev_10000_292'
                                   1218 ;layer         Allocated with name '_dynamic_keymap_reset_layer_20000_293'
                                   1219 ;row           Allocated with name '_dynamic_keymap_reset_row_40000_295'
                                   1220 ;column        Allocated with name '_dynamic_keymap_reset_column_60000_297'
                                   1221 ;encoder       Allocated with name '_dynamic_keymap_reset_encoder_40000_299'
                                   1222 ;------------------------------------------------------------
                                   1223 ;	quantum/dynamic_keymap.c:288: void dynamic_keymap_reset(void) {
                                   1224 ;	-----------------------------------------
                                   1225 ;	 function dynamic_keymap_reset
                                   1226 ;	-----------------------------------------
      007D9D                       1227 _dynamic_keymap_reset:
                                   1228 ;	quantum/dynamic_keymap.c:299: bool vial_unlocked_prev = vial_unlocked;
      007D9D 90 0C 07         [24] 1229 	mov	dptr,#_vial_unlocked
      007DA0 E0               [24] 1230 	movx	a,@dptr
      007DA1 90 08 EB         [24] 1231 	mov	dptr,#_dynamic_keymap_reset_vial_unlocked_prev_10000_292
      007DA4 F0               [24] 1232 	movx	@dptr,a
                                   1233 ;	quantum/dynamic_keymap.c:300: vial_unlocked = 1;
      007DA5 90 0C 07         [24] 1234 	mov	dptr,#_vial_unlocked
      007DA8 74 01            [12] 1235 	mov	a,#0x01
      007DAA F0               [24] 1236 	movx	@dptr,a
                                   1237 ;	quantum/dynamic_keymap.c:304: for (reset_index_t layer = 0; layer < DYNAMIC_KEYMAP_LAYER_COUNT; layer++) {
      007DAB 7F 00            [12] 1238 	mov	r7,#0x00
      007DAD                       1239 00115$:
      007DAD BF 06 00         [24] 1240 	cjne	r7,#0x06,00179$
      007DB0                       1241 00179$:
      007DB0 40 03            [24] 1242 	jc	00180$
      007DB2 02 7E 92         [24] 1243 	ljmp	00104$
      007DB5                       1244 00180$:
                                   1245 ;	quantum/dynamic_keymap.c:305: for (reset_index_t row = 0; row < MATRIX_ROWS; row++) {
      007DB5 8F 06            [24] 1246 	mov	ar6,r7
      007DB7 7D 00            [12] 1247 	mov	r5,#0x00
      007DB9                       1248 00109$:
      007DB9 BD 10 00         [24] 1249 	cjne	r5,#0x10,00181$
      007DBC                       1250 00181$:
      007DBC 50 5D            [24] 1251 	jnc	00102$
                                   1252 ;	quantum/dynamic_keymap.c:306: for (reset_index_t column = 0; column < MATRIX_COLS; column++) {
      007DBE 8D 04            [24] 1253 	mov	ar4,r5
      007DC0 7B 00            [12] 1254 	mov	r3,#0x00
      007DC2                       1255 00106$:
      007DC2 BB 08 00         [24] 1256 	cjne	r3,#0x08,00183$
      007DC5                       1257 00183$:
      007DC5 50 51            [24] 1258 	jnc	00110$
                                   1259 ;	quantum/dynamic_keymap.c:307: dynamic_keymap_set_keycode(layer, row, column, keycode_at_keymap_location_raw(layer, row, column));
      007DC7 90 09 92         [24] 1260 	mov	dptr,#_keycode_at_keymap_location_raw_PARM_2
      007DCA EC               [12] 1261 	mov	a,r4
      007DCB F0               [24] 1262 	movx	@dptr,a
      007DCC 90 09 93         [24] 1263 	mov	dptr,#_keycode_at_keymap_location_raw_PARM_3
      007DCF EB               [12] 1264 	mov	a,r3
      007DD0 F0               [24] 1265 	movx	@dptr,a
      007DD1 8E 82            [24] 1266 	mov	dpl, r6
      007DD3 C0 07            [24] 1267 	push	ar7
      007DD5 C0 06            [24] 1268 	push	ar6
      007DD7 C0 05            [24] 1269 	push	ar5
      007DD9 C0 04            [24] 1270 	push	ar4
      007DDB C0 03            [24] 1271 	push	ar3
      007DDD 12 8F F1         [24] 1272 	lcall	_keycode_at_keymap_location_raw
      007DE0 A9 82            [24] 1273 	mov	r1, dpl
      007DE2 AA 83            [24] 1274 	mov	r2, dph
      007DE4 D0 03            [24] 1275 	pop	ar3
      007DE6 D0 04            [24] 1276 	pop	ar4
      007DE8 D0 05            [24] 1277 	pop	ar5
      007DEA D0 06            [24] 1278 	pop	ar6
      007DEC 90 08 DC         [24] 1279 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_2
      007DEF EC               [12] 1280 	mov	a,r4
      007DF0 F0               [24] 1281 	movx	@dptr,a
      007DF1 90 08 DD         [24] 1282 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_3
      007DF4 EB               [12] 1283 	mov	a,r3
      007DF5 F0               [24] 1284 	movx	@dptr,a
      007DF6 90 08 DE         [24] 1285 	mov	dptr,#_dynamic_keymap_set_keycode_PARM_4
      007DF9 E9               [12] 1286 	mov	a,r1
      007DFA F0               [24] 1287 	movx	@dptr,a
      007DFB EA               [12] 1288 	mov	a,r2
      007DFC A3               [24] 1289 	inc	dptr
      007DFD F0               [24] 1290 	movx	@dptr,a
      007DFE 8E 82            [24] 1291 	mov	dpl, r6
      007E00 C0 06            [24] 1292 	push	ar6
      007E02 C0 05            [24] 1293 	push	ar5
      007E04 C0 04            [24] 1294 	push	ar4
      007E06 C0 03            [24] 1295 	push	ar3
      007E08 12 7C 23         [24] 1296 	lcall	_dynamic_keymap_set_keycode
      007E0B D0 03            [24] 1297 	pop	ar3
      007E0D D0 04            [24] 1298 	pop	ar4
      007E0F D0 05            [24] 1299 	pop	ar5
      007E11 D0 06            [24] 1300 	pop	ar6
      007E13 D0 07            [24] 1301 	pop	ar7
                                   1302 ;	quantum/dynamic_keymap.c:306: for (reset_index_t column = 0; column < MATRIX_COLS; column++) {
      007E15 0B               [12] 1303 	inc	r3
      007E16 80 AA            [24] 1304 	sjmp	00106$
      007E18                       1305 00110$:
                                   1306 ;	quantum/dynamic_keymap.c:305: for (reset_index_t row = 0; row < MATRIX_ROWS; row++) {
      007E18 0D               [12] 1307 	inc	r5
      007E19 80 9E            [24] 1308 	sjmp	00109$
      007E1B                       1309 00102$:
                                   1310 ;	quantum/dynamic_keymap.c:311: for (reset_index_t encoder = 0; encoder < NUM_ENCODERS; encoder++) {
      007E1B 8F 06            [24] 1311 	mov	ar6,r7
      007E1D 7D 00            [12] 1312 	mov	r5,#0x00
      007E1F                       1313 00112$:
      007E1F BD 01 00         [24] 1314 	cjne	r5,#0x01,00185$
      007E22                       1315 00185$:
      007E22 50 6A            [24] 1316 	jnc	00116$
                                   1317 ;	quantum/dynamic_keymap.c:312: dynamic_keymap_set_encoder(layer, encoder, true, keycode_at_encodermap_location_raw(layer, encoder, true));
      007E24 90 09 95         [24] 1318 	mov	dptr,#_keycode_at_encodermap_location_raw_PARM_2
      007E27 E4               [12] 1319 	clr	a
      007E28 F0               [24] 1320 	movx	@dptr,a
      007E29 90 09 96         [24] 1321 	mov	dptr,#_keycode_at_encodermap_location_raw_PARM_3
      007E2C 04               [12] 1322 	inc	a
      007E2D F0               [24] 1323 	movx	@dptr,a
      007E2E 8E 82            [24] 1324 	mov	dpl, r6
      007E30 C0 07            [24] 1325 	push	ar7
      007E32 C0 06            [24] 1326 	push	ar6
      007E34 12 90 40         [24] 1327 	lcall	_keycode_at_encodermap_location_raw
      007E37 AB 82            [24] 1328 	mov	r3, dpl
      007E39 AC 83            [24] 1329 	mov	r4, dph
      007E3B D0 06            [24] 1330 	pop	ar6
      007E3D 90 08 E6         [24] 1331 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_2
      007E40 E4               [12] 1332 	clr	a
      007E41 F0               [24] 1333 	movx	@dptr,a
      007E42 90 08 E7         [24] 1334 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_3
      007E45 04               [12] 1335 	inc	a
      007E46 F0               [24] 1336 	movx	@dptr,a
      007E47 90 08 E8         [24] 1337 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_4
      007E4A EB               [12] 1338 	mov	a,r3
      007E4B F0               [24] 1339 	movx	@dptr,a
      007E4C EC               [12] 1340 	mov	a,r4
      007E4D A3               [24] 1341 	inc	dptr
      007E4E F0               [24] 1342 	movx	@dptr,a
      007E4F 8E 82            [24] 1343 	mov	dpl, r6
      007E51 C0 06            [24] 1344 	push	ar6
      007E53 12 7D 25         [24] 1345 	lcall	_dynamic_keymap_set_encoder
      007E56 D0 06            [24] 1346 	pop	ar6
                                   1347 ;	quantum/dynamic_keymap.c:313: dynamic_keymap_set_encoder(layer, encoder, false, keycode_at_encodermap_location_raw(layer, encoder, false));
      007E58 90 09 95         [24] 1348 	mov	dptr,#_keycode_at_encodermap_location_raw_PARM_2
      007E5B E4               [12] 1349 	clr	a
      007E5C F0               [24] 1350 	movx	@dptr,a
      007E5D 90 09 96         [24] 1351 	mov	dptr,#_keycode_at_encodermap_location_raw_PARM_3
      007E60 F0               [24] 1352 	movx	@dptr,a
      007E61 8E 82            [24] 1353 	mov	dpl, r6
      007E63 C0 06            [24] 1354 	push	ar6
      007E65 12 90 40         [24] 1355 	lcall	_keycode_at_encodermap_location_raw
      007E68 AB 82            [24] 1356 	mov	r3, dpl
      007E6A AC 83            [24] 1357 	mov	r4, dph
      007E6C D0 06            [24] 1358 	pop	ar6
      007E6E 90 08 E6         [24] 1359 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_2
      007E71 E4               [12] 1360 	clr	a
      007E72 F0               [24] 1361 	movx	@dptr,a
      007E73 90 08 E7         [24] 1362 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_3
      007E76 F0               [24] 1363 	movx	@dptr,a
      007E77 90 08 E8         [24] 1364 	mov	dptr,#_dynamic_keymap_set_encoder_PARM_4
      007E7A EB               [12] 1365 	mov	a,r3
      007E7B F0               [24] 1366 	movx	@dptr,a
      007E7C EC               [12] 1367 	mov	a,r4
      007E7D A3               [24] 1368 	inc	dptr
      007E7E F0               [24] 1369 	movx	@dptr,a
      007E7F 8E 82            [24] 1370 	mov	dpl, r6
      007E81 C0 06            [24] 1371 	push	ar6
      007E83 12 7D 25         [24] 1372 	lcall	_dynamic_keymap_set_encoder
      007E86 D0 06            [24] 1373 	pop	ar6
      007E88 D0 07            [24] 1374 	pop	ar7
                                   1375 ;	quantum/dynamic_keymap.c:311: for (reset_index_t encoder = 0; encoder < NUM_ENCODERS; encoder++) {
      007E8A 7D 01            [12] 1376 	mov	r5,#0x01
      007E8C 80 91            [24] 1377 	sjmp	00112$
      007E8E                       1378 00116$:
                                   1379 ;	quantum/dynamic_keymap.c:304: for (reset_index_t layer = 0; layer < DYNAMIC_KEYMAP_LAYER_COUNT; layer++) {
      007E8E 0F               [12] 1380 	inc	r7
      007E8F 02 7D AD         [24] 1381 	ljmp	00115$
      007E92                       1382 00104$:
                                   1383 ;	quantum/dynamic_keymap.c:345: vial_unlocked = vial_unlocked_prev;
      007E92 90 08 EB         [24] 1384 	mov	dptr,#_dynamic_keymap_reset_vial_unlocked_prev_10000_292
      007E95 E0               [24] 1385 	movx	a,@dptr
      007E96 90 0C 07         [24] 1386 	mov	dptr,#_vial_unlocked
      007E99 F0               [24] 1387 	movx	@dptr,a
                                   1388 ;	quantum/dynamic_keymap.c:347: }
      007E9A 22               [24] 1389 	ret
                                   1390 ;------------------------------------------------------------
                                   1391 ;Allocation info for local variables in function 'ak820_dynamic_read_buffer'
                                   1392 ;------------------------------------------------------------
                                   1393 ;sloc0         Allocated with name '_ak820_dynamic_read_buffer_sloc0_1_0'
                                   1394 ;sloc1         Allocated with name '_ak820_dynamic_read_buffer_sloc1_1_0'
                                   1395 ;limit         Allocated with name '_ak820_dynamic_read_buffer_PARM_2'
                                   1396 ;offset        Allocated with name '_ak820_dynamic_read_buffer_PARM_3'
                                   1397 ;size          Allocated with name '_ak820_dynamic_read_buffer_PARM_4'
                                   1398 ;data          Allocated with name '_ak820_dynamic_read_buffer_PARM_5'
                                   1399 ;base          Allocated with name '_ak820_dynamic_read_buffer_base_10000_301'
                                   1400 ;target        Allocated with name '_ak820_dynamic_read_buffer_target_10000_302'
                                   1401 ;available     Allocated with name '_ak820_dynamic_read_buffer_available_10000_302'
                                   1402 ;remaining     Allocated with name '_ak820_dynamic_read_buffer_remaining_30000_305'
                                   1403 ;i             Allocated with name '_ak820_dynamic_read_buffer_i_20000_307'
                                   1404 ;------------------------------------------------------------
                                   1405 ;	quantum/dynamic_keymap.c:352: static void ak820_dynamic_read_buffer(uint16_t base, uint16_t limit, uint16_t offset, uint16_t size, uint8_t *data) {
                                   1406 ;	-----------------------------------------
                                   1407 ;	 function ak820_dynamic_read_buffer
                                   1408 ;	-----------------------------------------
      007E9B                       1409 _ak820_dynamic_read_buffer:
      007E9B AF 83            [24] 1410 	mov	r7,dph
      007E9D E5 82            [12] 1411 	mov	a,dpl
      007E9F 90 08 F5         [24] 1412 	mov	dptr,#_ak820_dynamic_read_buffer_base_10000_301
      007EA2 F0               [24] 1413 	movx	@dptr,a
      007EA3 EF               [12] 1414 	mov	a,r7
      007EA4 A3               [24] 1415 	inc	dptr
      007EA5 F0               [24] 1416 	movx	@dptr,a
                                   1417 ;	quantum/dynamic_keymap.c:353: uint8_t DYNAMIC_BUFFER_MEM *target = (uint8_t DYNAMIC_BUFFER_MEM *)data;
      007EA6 90 08 F2         [24] 1418 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_5
      007EA9 E0               [24] 1419 	movx	a,@dptr
      007EAA F5 33            [12] 1420 	mov	_ak820_dynamic_read_buffer_sloc0_1_0,a
      007EAC A3               [24] 1421 	inc	dptr
      007EAD E0               [24] 1422 	movx	a,@dptr
      007EAE F5 34            [12] 1423 	mov	(_ak820_dynamic_read_buffer_sloc0_1_0 + 1),a
      007EB0 A3               [24] 1424 	inc	dptr
      007EB1 E0               [24] 1425 	movx	a,@dptr
      007EB2 F5 35            [12] 1426 	mov	(_ak820_dynamic_read_buffer_sloc0_1_0 + 2),a
      007EB4 AB 33            [24] 1427 	mov	r3,_ak820_dynamic_read_buffer_sloc0_1_0
      007EB6 AC 34            [24] 1428 	mov	r4,(_ak820_dynamic_read_buffer_sloc0_1_0 + 1)
                                   1429 ;	quantum/dynamic_keymap.c:354: uint8_t available = 0;
      007EB8 90 08 F7         [24] 1430 	mov	dptr,#_ak820_dynamic_read_buffer_available_10000_302
      007EBB E4               [12] 1431 	clr	a
      007EBC F0               [24] 1432 	movx	@dptr,a
                                   1433 ;	quantum/dynamic_keymap.c:355: if (size > 28) return;
      007EBD 90 08 F0         [24] 1434 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_4
      007EC0 E0               [24] 1435 	movx	a,@dptr
      007EC1 F9               [12] 1436 	mov	r1,a
      007EC2 A3               [24] 1437 	inc	dptr
      007EC3 E0               [24] 1438 	movx	a,@dptr
      007EC4 FA               [12] 1439 	mov	r2,a
      007EC5 89 00            [24] 1440 	mov	ar0,r1
      007EC7 8A 07            [24] 1441 	mov	ar7,r2
      007EC9 C3               [12] 1442 	clr	c
      007ECA 74 1C            [12] 1443 	mov	a,#0x1c
      007ECC 98               [12] 1444 	subb	a,r0
      007ECD E4               [12] 1445 	clr	a
      007ECE 9F               [12] 1446 	subb	a,r7
      007ECF 50 01            [24] 1447 	jnc	00102$
                                   1448 ;	free result
      007ED1 22               [24] 1449 	ret
      007ED2                       1450 00102$:
                                   1451 ;	quantum/dynamic_keymap.c:356: if (offset < limit) {
      007ED2 90 08 EE         [24] 1452 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_3
      007ED5 E0               [24] 1453 	movx	a,@dptr
      007ED6 FE               [12] 1454 	mov	r6,a
      007ED7 A3               [24] 1455 	inc	dptr
      007ED8 E0               [24] 1456 	movx	a,@dptr
      007ED9 FF               [12] 1457 	mov	r7,a
      007EDA 90 08 EC         [24] 1458 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_2
      007EDD E0               [24] 1459 	movx	a,@dptr
      007EDE F8               [12] 1460 	mov	r0,a
      007EDF A3               [24] 1461 	inc	dptr
      007EE0 E0               [24] 1462 	movx	a,@dptr
      007EE1 FD               [12] 1463 	mov	r5,a
      007EE2 C3               [12] 1464 	clr	c
      007EE3 EE               [12] 1465 	mov	a,r6
      007EE4 98               [12] 1466 	subb	a,r0
      007EE5 EF               [12] 1467 	mov	a,r7
      007EE6 9D               [12] 1468 	subb	a,r5
      007EE7 50 17            [24] 1469 	jnc	00104$
                                   1470 ;	quantum/dynamic_keymap.c:357: uint16_t remaining = limit - offset;
      007EE9 E8               [12] 1471 	mov	a,r0
      007EEA C3               [12] 1472 	clr	c
      007EEB 9E               [12] 1473 	subb	a,r6
      007EEC F8               [12] 1474 	mov	r0,a
      007EED ED               [12] 1475 	mov	a,r5
      007EEE 9F               [12] 1476 	subb	a,r7
      007EEF FD               [12] 1477 	mov	r5,a
                                   1478 ;	quantum/dynamic_keymap.c:358: available = remaining < size ? remaining : size;
      007EF0 C3               [12] 1479 	clr	c
      007EF1 E8               [12] 1480 	mov	a,r0
      007EF2 99               [12] 1481 	subb	a,r1
      007EF3 ED               [12] 1482 	mov	a,r5
      007EF4 9A               [12] 1483 	subb	a,r2
      007EF5 40 04            [24] 1484 	jc	00114$
      007EF7 89 00            [24] 1485 	mov	ar0,r1
      007EF9 8A 05            [24] 1486 	mov	ar5,r2
      007EFB                       1487 00114$:
      007EFB 90 08 F7         [24] 1488 	mov	dptr,#_ak820_dynamic_read_buffer_available_10000_302
      007EFE E8               [12] 1489 	mov	a,r0
      007EFF F0               [24] 1490 	movx	@dptr,a
      007F00                       1491 00104$:
                                   1492 ;	quantum/dynamic_keymap.c:360: if (available) eeprom_read_block(data, (const void *)(uintptr_t)(base + offset), available);
      007F00 90 08 F7         [24] 1493 	mov	dptr,#_ak820_dynamic_read_buffer_available_10000_302
      007F03 E0               [24] 1494 	movx	a,@dptr
      007F04 F5 36            [12] 1495 	mov	_ak820_dynamic_read_buffer_sloc1_1_0,a
      007F06 E0               [24] 1496 	movx	a,@dptr
      007F07 60 46            [24] 1497 	jz	00106$
      007F09 C0 03            [24] 1498 	push	ar3
      007F0B C0 04            [24] 1499 	push	ar4
      007F0D 90 08 F5         [24] 1500 	mov	dptr,#_ak820_dynamic_read_buffer_base_10000_301
      007F10 E0               [24] 1501 	movx	a,@dptr
      007F11 FC               [12] 1502 	mov	r4,a
      007F12 A3               [24] 1503 	inc	dptr
      007F13 E0               [24] 1504 	movx	a,@dptr
      007F14 FD               [12] 1505 	mov	r5,a
      007F15 EE               [12] 1506 	mov	a,r6
      007F16 2C               [12] 1507 	add	a, r4
      007F17 FE               [12] 1508 	mov	r6,a
      007F18 EF               [12] 1509 	mov	a,r7
      007F19 3D               [12] 1510 	addc	a, r5
      007F1A FF               [12] 1511 	mov	r7,a
      007F1B 90 05 3D         [24] 1512 	mov	dptr,#_eeprom_read_block_PARM_2
      007F1E EE               [12] 1513 	mov	a,r6
      007F1F F0               [24] 1514 	movx	@dptr,a
      007F20 EF               [12] 1515 	mov	a,r7
      007F21 A3               [24] 1516 	inc	dptr
      007F22 F0               [24] 1517 	movx	@dptr,a
      007F23 E4               [12] 1518 	clr	a
      007F24 A3               [24] 1519 	inc	dptr
      007F25 F0               [24] 1520 	movx	@dptr,a
      007F26 90 05 40         [24] 1521 	mov	dptr,#_eeprom_read_block_PARM_3
      007F29 E5 36            [12] 1522 	mov	a,_ak820_dynamic_read_buffer_sloc1_1_0
      007F2B F0               [24] 1523 	movx	@dptr,a
      007F2C E4               [12] 1524 	clr	a
      007F2D A3               [24] 1525 	inc	dptr
      007F2E F0               [24] 1526 	movx	@dptr,a
      007F2F 85 33 82         [24] 1527 	mov	dpl, _ak820_dynamic_read_buffer_sloc0_1_0
      007F32 85 34 83         [24] 1528 	mov	dph, (_ak820_dynamic_read_buffer_sloc0_1_0 + 1)
      007F35 85 35 F0         [24] 1529 	mov	b, (_ak820_dynamic_read_buffer_sloc0_1_0 + 2)
      007F38 C0 04            [24] 1530 	push	ar4
      007F3A C0 03            [24] 1531 	push	ar3
      007F3C C0 02            [24] 1532 	push	ar2
      007F3E C0 01            [24] 1533 	push	ar1
      007F40 12 3D 3D         [24] 1534 	lcall	_eeprom_read_block
      007F43 D0 01            [24] 1535 	pop	ar1
      007F45 D0 02            [24] 1536 	pop	ar2
      007F47 D0 03            [24] 1537 	pop	ar3
      007F49 D0 04            [24] 1538 	pop	ar4
                                   1539 ;	quantum/dynamic_keymap.c:361: for (uint8_t i = available; i < size; ++i) target[i] = 0;
      007F4B D0 04            [24] 1540 	pop	ar4
      007F4D D0 03            [24] 1541 	pop	ar3
                                   1542 ;	quantum/dynamic_keymap.c:360: if (available) eeprom_read_block(data, (const void *)(uintptr_t)(base + offset), available);
      007F4F                       1543 00106$:
                                   1544 ;	quantum/dynamic_keymap.c:361: for (uint8_t i = available; i < size; ++i) target[i] = 0;
      007F4F 90 08 F7         [24] 1545 	mov	dptr,#_ak820_dynamic_read_buffer_available_10000_302
      007F52 E0               [24] 1546 	movx	a,@dptr
      007F53 FF               [12] 1547 	mov	r7,a
      007F54                       1548 00109$:
      007F54 8F 05            [24] 1549 	mov	ar5,r7
      007F56 7E 00            [12] 1550 	mov	r6,#0x00
      007F58 C3               [12] 1551 	clr	c
      007F59 ED               [12] 1552 	mov	a,r5
      007F5A 99               [12] 1553 	subb	a,r1
      007F5B EE               [12] 1554 	mov	a,r6
      007F5C 9A               [12] 1555 	subb	a,r2
      007F5D 50 0D            [24] 1556 	jnc	00111$
      007F5F EF               [12] 1557 	mov	a,r7
      007F60 2B               [12] 1558 	add	a, r3
      007F61 F5 82            [12] 1559 	mov	dpl,a
      007F63 E4               [12] 1560 	clr	a
      007F64 3C               [12] 1561 	addc	a, r4
      007F65 F5 83            [12] 1562 	mov	dph,a
      007F67 E4               [12] 1563 	clr	a
      007F68 F0               [24] 1564 	movx	@dptr,a
      007F69 0F               [12] 1565 	inc	r7
      007F6A 80 E8            [24] 1566 	sjmp	00109$
      007F6C                       1567 00111$:
                                   1568 ;	quantum/dynamic_keymap.c:362: }
      007F6C 22               [24] 1569 	ret
                                   1570 ;------------------------------------------------------------
                                   1571 ;Allocation info for local variables in function 'dynamic_keymap_get_buffer'
                                   1572 ;------------------------------------------------------------
                                   1573 ;size          Allocated with name '_dynamic_keymap_get_buffer_PARM_2'
                                   1574 ;data          Allocated with name '_dynamic_keymap_get_buffer_PARM_3'
                                   1575 ;offset        Allocated with name '_dynamic_keymap_get_buffer_offset_10000_308'
                                   1576 ;------------------------------------------------------------
                                   1577 ;	quantum/dynamic_keymap.c:365: void dynamic_keymap_get_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
                                   1578 ;	-----------------------------------------
                                   1579 ;	 function dynamic_keymap_get_buffer
                                   1580 ;	-----------------------------------------
      007F6D                       1581 _dynamic_keymap_get_buffer:
      007F6D AF 83            [24] 1582 	mov	r7,dph
      007F6F E5 82            [12] 1583 	mov	a,dpl
      007F71 90 08 FD         [24] 1584 	mov	dptr,#_dynamic_keymap_get_buffer_offset_10000_308
      007F74 F0               [24] 1585 	movx	@dptr,a
      007F75 EF               [12] 1586 	mov	a,r7
      007F76 A3               [24] 1587 	inc	dptr
      007F77 F0               [24] 1588 	movx	@dptr,a
                                   1589 ;	quantum/dynamic_keymap.c:368: DYNAMIC_KEYMAP_LAYER_COUNT * MATRIX_ROWS * MATRIX_COLS * 2, offset, size, data);
      007F78 90 08 FD         [24] 1590 	mov	dptr,#_dynamic_keymap_get_buffer_offset_10000_308
      007F7B E0               [24] 1591 	movx	a,@dptr
      007F7C FE               [12] 1592 	mov	r6,a
      007F7D A3               [24] 1593 	inc	dptr
      007F7E E0               [24] 1594 	movx	a,@dptr
      007F7F FF               [12] 1595 	mov	r7,a
      007F80 90 08 F8         [24] 1596 	mov	dptr,#_dynamic_keymap_get_buffer_PARM_2
      007F83 E0               [24] 1597 	movx	a,@dptr
      007F84 FC               [12] 1598 	mov	r4,a
      007F85 A3               [24] 1599 	inc	dptr
      007F86 E0               [24] 1600 	movx	a,@dptr
      007F87 FD               [12] 1601 	mov	r5,a
      007F88 90 08 FA         [24] 1602 	mov	dptr,#_dynamic_keymap_get_buffer_PARM_3
      007F8B E0               [24] 1603 	movx	a,@dptr
      007F8C F9               [12] 1604 	mov	r1,a
      007F8D A3               [24] 1605 	inc	dptr
      007F8E E0               [24] 1606 	movx	a,@dptr
      007F8F FA               [12] 1607 	mov	r2,a
      007F90 A3               [24] 1608 	inc	dptr
      007F91 E0               [24] 1609 	movx	a,@dptr
      007F92 FB               [12] 1610 	mov	r3,a
      007F93 90 08 EC         [24] 1611 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_2
      007F96 E4               [12] 1612 	clr	a
      007F97 F0               [24] 1613 	movx	@dptr,a
      007F98 74 06            [12] 1614 	mov	a,#0x06
      007F9A A3               [24] 1615 	inc	dptr
      007F9B F0               [24] 1616 	movx	@dptr,a
      007F9C 90 08 EE         [24] 1617 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_3
      007F9F EE               [12] 1618 	mov	a,r6
      007FA0 F0               [24] 1619 	movx	@dptr,a
      007FA1 EF               [12] 1620 	mov	a,r7
      007FA2 A3               [24] 1621 	inc	dptr
      007FA3 F0               [24] 1622 	movx	@dptr,a
      007FA4 90 08 F0         [24] 1623 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_4
      007FA7 EC               [12] 1624 	mov	a,r4
      007FA8 F0               [24] 1625 	movx	@dptr,a
      007FA9 ED               [12] 1626 	mov	a,r5
      007FAA A3               [24] 1627 	inc	dptr
      007FAB F0               [24] 1628 	movx	@dptr,a
      007FAC 90 08 F2         [24] 1629 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_5
      007FAF E9               [12] 1630 	mov	a,r1
      007FB0 F0               [24] 1631 	movx	@dptr,a
      007FB1 EA               [12] 1632 	mov	a,r2
      007FB2 A3               [24] 1633 	inc	dptr
      007FB3 F0               [24] 1634 	movx	@dptr,a
      007FB4 EB               [12] 1635 	mov	a,r3
      007FB5 A3               [24] 1636 	inc	dptr
      007FB6 F0               [24] 1637 	movx	@dptr,a
      007FB7 90 00 40         [24] 1638 	mov	dptr,#0x0040
                                   1639 ;	quantum/dynamic_keymap.c:390: }
      007FBA 02 7E 9B         [24] 1640 	ljmp	_ak820_dynamic_read_buffer
                                   1641 ;------------------------------------------------------------
                                   1642 ;Allocation info for local variables in function 'dynamic_keymap_set_buffer'
                                   1643 ;------------------------------------------------------------
                                   1644 ;sloc0         Allocated with name '_dynamic_keymap_set_buffer_sloc0_1_0'
                                   1645 ;sloc1         Allocated with name '_dynamic_keymap_set_buffer_sloc1_1_0'
                                   1646 ;sloc2         Allocated with name '_dynamic_keymap_set_buffer_sloc2_1_0'
                                   1647 ;sloc3         Allocated with name '_dynamic_keymap_set_buffer_sloc3_1_0'
                                   1648 ;size          Allocated with name '_dynamic_keymap_set_buffer_PARM_2'
                                   1649 ;data          Allocated with name '_dynamic_keymap_set_buffer_PARM_3'
                                   1650 ;offset        Allocated with name '_dynamic_keymap_set_buffer_offset_10000_310'
                                   1651 ;dynamic_keymap_eeprom_size Allocated with name '_dynamic_keymap_set_buffer_dynamic_keymap_eeprom_size_10000_311'
                                   1652 ;target        Allocated with name '_dynamic_keymap_set_buffer_target_10000_311'
                                   1653 ;buffer        Allocated with name '_dynamic_keymap_set_buffer_buffer_10000_311'
                                   1654 ;count         Allocated with name '_dynamic_keymap_set_buffer_count_10001_314'
                                   1655 ;chk_offset    Allocated with name '_dynamic_keymap_set_buffer_chk_offset_30001_317'
                                   1656 ;chk_sz        Allocated with name '_dynamic_keymap_set_buffer_chk_sz_30001_317'
                                   1657 ;kc            Allocated with name '_dynamic_keymap_set_buffer_kc_50001_319'
                                   1658 ;kc            Allocated with name '_dynamic_keymap_set_buffer_kc_50001_322'
                                   1659 ;i             Allocated with name '_dynamic_keymap_set_buffer_i_40001_324'
                                   1660 ;kc            Allocated with name '_dynamic_keymap_set_buffer_kc_50001_325'
                                   1661 ;------------------------------------------------------------
                                   1662 ;	quantum/dynamic_keymap.c:392: void dynamic_keymap_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
                                   1663 ;	-----------------------------------------
                                   1664 ;	 function dynamic_keymap_set_buffer
                                   1665 ;	-----------------------------------------
      007FBD                       1666 _dynamic_keymap_set_buffer:
      007FBD AF 83            [24] 1667 	mov	r7,dph
      007FBF E5 82            [12] 1668 	mov	a,dpl
      007FC1 90 09 04         [24] 1669 	mov	dptr,#_dynamic_keymap_set_buffer_offset_10000_310
      007FC4 F0               [24] 1670 	movx	@dptr,a
      007FC5 EF               [12] 1671 	mov	a,r7
      007FC6 A3               [24] 1672 	inc	dptr
      007FC7 F0               [24] 1673 	movx	@dptr,a
                                   1674 ;	quantum/dynamic_keymap.c:394: uint8_t DYNAMIC_BUFFER_MEM *target = (uint8_t DYNAMIC_BUFFER_MEM *)(DYNAMIC_KEYMAP_EEPROM_ADDR + offset);
      007FC8 90 09 04         [24] 1675 	mov	dptr,#_dynamic_keymap_set_buffer_offset_10000_310
      007FCB 12 86 05         [24] 1676 	lcall	_ak820_outline_0012
      007FCE 74 40            [12] 1677 	mov	a,#0x40
      007FD0 2C               [12] 1678 	add	a, r4
      007FD1 FA               [12] 1679 	mov	r2,a
      007FD2 E4               [12] 1680 	clr	a
      007FD3 3D               [12] 1681 	addc	a, r5
      007FD4 FB               [12] 1682 	mov	r3,a
                                   1683 ;	quantum/dynamic_keymap.c:395: uint8_t DYNAMIC_BUFFER_MEM *buffer = (uint8_t DYNAMIC_BUFFER_MEM *)data;
      007FD5 90 09 01         [24] 1684 	mov	dptr,#_dynamic_keymap_set_buffer_PARM_3
      007FD8 E0               [24] 1685 	movx	a,@dptr
      007FD9 F5 37            [12] 1686 	mov	_dynamic_keymap_set_buffer_sloc0_1_0,a
      007FDB A3               [24] 1687 	inc	dptr
      007FDC E0               [24] 1688 	movx	a,@dptr
      007FDD F5 38            [12] 1689 	mov	(_dynamic_keymap_set_buffer_sloc0_1_0 + 1),a
      007FDF A3               [24] 1690 	inc	dptr
      007FE0 E0               [24] 1691 	movx	a,@dptr
      007FE1 F5 39            [12] 1692 	mov	(_dynamic_keymap_set_buffer_sloc0_1_0 + 2),a
      007FE3 A8 37            [24] 1693 	mov	r0,_dynamic_keymap_set_buffer_sloc0_1_0
      007FE5 A9 38            [24] 1694 	mov	r1,(_dynamic_keymap_set_buffer_sloc0_1_0 + 1)
                                   1695 ;	quantum/dynamic_keymap.c:399: if (!size) return;
      007FE7 90 08 FF         [24] 1696 	mov	dptr,#_dynamic_keymap_set_buffer_PARM_2
      007FEA E0               [24] 1697 	movx	a,@dptr
      007FEB F5 3A            [12] 1698 	mov	_dynamic_keymap_set_buffer_sloc1_1_0,a
      007FED A3               [24] 1699 	inc	dptr
      007FEE E0               [24] 1700 	movx	a,@dptr
      007FEF F5 3B            [12] 1701 	mov	(_dynamic_keymap_set_buffer_sloc1_1_0 + 1),a
      007FF1 E5 3A            [12] 1702 	mov	a,_dynamic_keymap_set_buffer_sloc1_1_0
      007FF3 45 3B            [12] 1703 	orl	a,(_dynamic_keymap_set_buffer_sloc1_1_0 + 1)
      007FF5 70 01            [24] 1704 	jnz	00102$
      007FF7 22               [24] 1705 	ret
      007FF8                       1706 00102$:
                                   1707 ;	quantum/dynamic_keymap.c:401: if (size > 28) return;
      007FF8 85 3A 3C         [24] 1708 	mov	_dynamic_keymap_set_buffer_sloc2_1_0,_dynamic_keymap_set_buffer_sloc1_1_0
      007FFB 85 3B 3D         [24] 1709 	mov	(_dynamic_keymap_set_buffer_sloc2_1_0 + 1),(_dynamic_keymap_set_buffer_sloc1_1_0 + 1)
      007FFE C3               [12] 1710 	clr	c
      007FFF 74 1C            [12] 1711 	mov	a,#0x1c
      008001 95 3C            [12] 1712 	subb	a,_dynamic_keymap_set_buffer_sloc2_1_0
      008003 E4               [12] 1713 	clr	a
      008004 95 3D            [12] 1714 	subb	a,(_dynamic_keymap_set_buffer_sloc2_1_0 + 1)
      008006 50 01            [24] 1715 	jnc	00104$
                                   1716 ;	free result
      008008 22               [24] 1717 	ret
      008009                       1718 00104$:
                                   1719 ;	quantum/dynamic_keymap.c:403: dynamic_buffer_size_t count = size;
      008009 85 3A 3E         [24] 1720 	mov	_dynamic_keymap_set_buffer_sloc3_1_0,_dynamic_keymap_set_buffer_sloc1_1_0
                                   1721 ;	quantum/dynamic_keymap.c:407: if (offset >= dynamic_keymap_eeprom_size || dynamic_keymap_eeprom_size - offset < size)
      00800C 74 FA            [12] 1722 	mov	a,#0x100 - 0x06
      00800E 2F               [12] 1723 	add	a,r7
      00800F 40 11            [24] 1724 	jc	00105$
      008011 E4               [12] 1725 	clr	a
      008012 C3               [12] 1726 	clr	c
      008013 9E               [12] 1727 	subb	a,r6
      008014 FE               [12] 1728 	mov	r6,a
      008015 74 06            [12] 1729 	mov	a,#0x06
      008017 9F               [12] 1730 	subb	a,r7
      008018 FF               [12] 1731 	mov	r7,a
      008019 C3               [12] 1732 	clr	c
      00801A EE               [12] 1733 	mov	a,r6
      00801B 95 3A            [12] 1734 	subb	a,_dynamic_keymap_set_buffer_sloc1_1_0
      00801D EF               [12] 1735 	mov	a,r7
      00801E 95 3B            [12] 1736 	subb	a,(_dynamic_keymap_set_buffer_sloc1_1_0 + 1)
      008020 50 01            [24] 1737 	jnc	00106$
      008022                       1738 00105$:
                                   1739 ;	quantum/dynamic_keymap.c:408: return;
      008022 22               [24] 1740 	ret
      008023                       1741 00106$:
                                   1742 ;	quantum/dynamic_keymap.c:412: if (!vial_unlocked) {
      008023 90 0C 07         [24] 1743 	mov	dptr,#_vial_unlocked
      008026 E0               [24] 1744 	movx	a,@dptr
      008027 60 03            [24] 1745 	jz	00207$
      008029 02 81 5C         [24] 1746 	ljmp	00120$
      00802C                       1747 00207$:
                                   1748 ;	quantum/dynamic_keymap.c:414: dynamic_buffer_size_t chk_offset = 0;
      00802C 90 09 06         [24] 1749 	mov	dptr,#_dynamic_keymap_set_buffer_chk_offset_30001_317
      00802F E4               [12] 1750 	clr	a
      008030 F0               [24] 1751 	movx	@dptr,a
                                   1752 ;	quantum/dynamic_keymap.c:415: dynamic_buffer_size_t chk_sz = count;
      008031 90 09 07         [24] 1753 	mov	dptr,#_dynamic_keymap_set_buffer_chk_sz_30001_317
      008034 E5 3E            [12] 1754 	mov	a,_dynamic_keymap_set_buffer_sloc3_1_0
      008036 F0               [24] 1755 	movx	@dptr,a
                                   1756 ;	quantum/dynamic_keymap.c:418: if (offset % 2 != 0) {
      008037 EC               [12] 1757 	mov	a,r4
      008038 30 E0 36         [24] 1758 	jnb	acc.0,00111$
                                   1759 ;	quantum/dynamic_keymap.c:419: uint16_t kc = (eeprom_read_byte(target - 1) << 8) | buffer[0];
      00803B EA               [12] 1760 	mov	a,r2
      00803C 24 FF            [12] 1761 	add	a,#0xff
      00803E FE               [12] 1762 	mov	r6,a
      00803F EB               [12] 1763 	mov	a,r3
      008040 34 FF            [12] 1764 	addc	a,#0xff
      008042 FF               [12] 1765 	mov	r7,a
      008043 7D 00            [12] 1766 	mov	r5,#0x00
      008045 8E 82            [24] 1767 	mov	dpl, r6
      008047 8F 83            [24] 1768 	mov	dph, r7
      008049 8D F0            [24] 1769 	mov	b, r5
      00804B 12 43 FC         [24] 1770 	lcall	_eeprom_read_byte
      00804E AE 82            [24] 1771 	mov	r6,dpl
      008050 7F 00            [12] 1772 	mov	r7,#0x00
      008052 88 82            [24] 1773 	mov	dpl,r0
      008054 89 83            [24] 1774 	mov	dph,r1
      008056 E0               [24] 1775 	movx	a,@dptr
      008057 7C 00            [12] 1776 	mov	r4,#0x00
      008059 42 07            [12] 1777 	orl	ar7,a
      00805B EC               [12] 1778 	mov	a,r4
      00805C 42 06            [12] 1779 	orl	ar6,a
                                   1780 ;	quantum/dynamic_keymap.c:420: if (kc == QK_BOOT)
      00805E BF 00 0A         [24] 1781 	cjne	r7,#0x00,00109$
      008061 BE 7C 07         [24] 1782 	cjne	r6,#0x7c,00109$
                                   1783 ;	quantum/dynamic_keymap.c:421: buffer[0] = 0xFF;
      008064 88 82            [24] 1784 	mov	dpl,r0
      008066 89 83            [24] 1785 	mov	dph,r1
      008068 74 FF            [12] 1786 	mov	a,#0xff
      00806A F0               [24] 1787 	movx	@dptr,a
      00806B                       1788 00109$:
                                   1789 ;	quantum/dynamic_keymap.c:424: chk_offset += 1;
      00806B 90 09 06         [24] 1790 	mov	dptr,#_dynamic_keymap_set_buffer_chk_offset_30001_317
      00806E 74 01            [12] 1791 	mov	a,#0x01
      008070 F0               [24] 1792 	movx	@dptr,a
      008071                       1793 00111$:
                                   1794 ;	quantum/dynamic_keymap.c:428: if ((offset + size) % 2 != 0) {
      008071 90 09 04         [24] 1795 	mov	dptr,#_dynamic_keymap_set_buffer_offset_10000_310
      008074 E0               [24] 1796 	movx	a,@dptr
      008075 FE               [12] 1797 	mov	r6,a
      008076 A3               [24] 1798 	inc	dptr
      008077 E0               [24] 1799 	movx	a,@dptr
      008078 FF               [12] 1800 	mov	r7,a
      008079 E5 3A            [12] 1801 	mov	a,_dynamic_keymap_set_buffer_sloc1_1_0
      00807B 2E               [12] 1802 	add	a, r6
      00807C FE               [12] 1803 	mov	r6,a
      00807D E5 3B            [12] 1804 	mov	a,(_dynamic_keymap_set_buffer_sloc1_1_0 + 1)
      00807F 3F               [12] 1805 	addc	a, r7
      008080 EE               [12] 1806 	mov	a,r6
      008081 30 E0 63         [24] 1807 	jnb	acc.0,00115$
                                   1808 ;	quantum/dynamic_keymap.c:429: uint16_t kc = (buffer[count - 1] << 8) | eeprom_read_byte(target + count);
      008084 AE 3E            [24] 1809 	mov	r6,_dynamic_keymap_set_buffer_sloc3_1_0
      008086 7F 00            [12] 1810 	mov	r7,#0x00
      008088 EE               [12] 1811 	mov	a,r6
      008089 24 FF            [12] 1812 	add	a,#0xff
      00808B FC               [12] 1813 	mov	r4,a
      00808C EF               [12] 1814 	mov	a,r7
      00808D 34 FF            [12] 1815 	addc	a,#0xff
      00808F FD               [12] 1816 	mov	r5,a
      008090 EC               [12] 1817 	mov	a,r4
      008091 28               [12] 1818 	add	a, r0
      008092 F5 82            [12] 1819 	mov	dpl,a
      008094 ED               [12] 1820 	mov	a,r5
      008095 39               [12] 1821 	addc	a, r1
      008096 F5 83            [12] 1822 	mov	dph,a
      008098 E0               [24] 1823 	movx	a,@dptr
      008099 FC               [12] 1824 	mov	r4,a
      00809A 7D 00            [12] 1825 	mov	r5,#0x00
      00809C E5 3E            [12] 1826 	mov	a,_dynamic_keymap_set_buffer_sloc3_1_0
      00809E 2A               [12] 1827 	add	a, r2
      00809F FA               [12] 1828 	mov	r2,a
      0080A0 E4               [12] 1829 	clr	a
      0080A1 3B               [12] 1830 	addc	a, r3
      0080A2 FB               [12] 1831 	mov	r3,a
      0080A3 C0 00            [24] 1832 	push	ar0
      0080A5 C0 01            [24] 1833 	push	ar1
      0080A7 8B 01            [24] 1834 	mov	ar1,r3
      0080A9 7B 00            [12] 1835 	mov	r3,#0x00
      0080AB 8A 82            [24] 1836 	mov	dpl, r2
      0080AD 89 83            [24] 1837 	mov	dph, r1
      0080AF 8B F0            [24] 1838 	mov	b, r3
      0080B1 12 43 FC         [24] 1839 	lcall	_eeprom_read_byte
      0080B4 AB 82            [24] 1840 	mov	r3, dpl
      0080B6 7A 00            [12] 1841 	mov	r2,#0x00
      0080B8 EB               [12] 1842 	mov	a,r3
      0080B9 42 05            [12] 1843 	orl	ar5,a
      0080BB EA               [12] 1844 	mov	a,r2
      0080BC 42 04            [12] 1845 	orl	ar4,a
                                   1846 ;	quantum/dynamic_keymap.c:430: if (kc == QK_BOOT)
      0080BE BD 00 05         [24] 1847 	cjne	r5,#0x00,00212$
      0080C1 BC 7C 02         [24] 1848 	cjne	r4,#0x7c,00212$
      0080C4 80 06            [24] 1849 	sjmp	00213$
      0080C6                       1850 00212$:
      0080C6 D0 01            [24] 1851 	pop	ar1
      0080C8 D0 00            [24] 1852 	pop	ar0
      0080CA 80 14            [24] 1853 	sjmp	00113$
      0080CC                       1854 00213$:
      0080CC D0 01            [24] 1855 	pop	ar1
      0080CE D0 00            [24] 1856 	pop	ar0
                                   1857 ;	quantum/dynamic_keymap.c:431: buffer[count - 1] = 0xFF;
      0080D0 1E               [12] 1858 	dec	r6
      0080D1 BE FF 01         [24] 1859 	cjne	r6,#0xff,00214$
      0080D4 1F               [12] 1860 	dec	r7
      0080D5                       1861 00214$:
      0080D5 EE               [12] 1862 	mov	a,r6
      0080D6 28               [12] 1863 	add	a, r0
      0080D7 F5 82            [12] 1864 	mov	dpl,a
      0080D9 EF               [12] 1865 	mov	a,r7
      0080DA 39               [12] 1866 	addc	a, r1
      0080DB F5 83            [12] 1867 	mov	dph,a
      0080DD 74 FF            [12] 1868 	mov	a,#0xff
      0080DF F0               [24] 1869 	movx	@dptr,a
      0080E0                       1870 00113$:
                                   1871 ;	quantum/dynamic_keymap.c:434: chk_sz -= 1;
      0080E0 E5 3E            [12] 1872 	mov	a,_dynamic_keymap_set_buffer_sloc3_1_0
      0080E2 14               [12] 1873 	dec	a
      0080E3 90 09 07         [24] 1874 	mov	dptr,#_dynamic_keymap_set_buffer_chk_sz_30001_317
      0080E6 F0               [24] 1875 	movx	@dptr,a
      0080E7                       1876 00115$:
                                   1877 ;	quantum/dynamic_keymap.c:438: for (dynamic_buffer_size_t i = chk_offset; i < chk_sz; i += 2) {
      0080E7 90 09 06         [24] 1878 	mov	dptr,#_dynamic_keymap_set_buffer_chk_offset_30001_317
      0080EA E0               [24] 1879 	movx	a,@dptr
      0080EB 90 09 08         [24] 1880 	mov	dptr,#_dynamic_keymap_set_buffer_i_40001_324
      0080EE F0               [24] 1881 	movx	@dptr,a
      0080EF 90 09 07         [24] 1882 	mov	dptr,#_dynamic_keymap_set_buffer_chk_sz_30001_317
      0080F2 E0               [24] 1883 	movx	a,@dptr
      0080F3 FF               [12] 1884 	mov	r7,a
      0080F4                       1885 00122$:
      0080F4 90 09 08         [24] 1886 	mov	dptr,#_dynamic_keymap_set_buffer_i_40001_324
      0080F7 E0               [24] 1887 	movx	a,@dptr
      0080F8 FE               [12] 1888 	mov	r6,a
      0080F9 C3               [12] 1889 	clr	c
      0080FA 9F               [12] 1890 	subb	a,r7
      0080FB 50 5F            [24] 1891 	jnc	00120$
                                   1892 ;	quantum/dynamic_keymap.c:439: uint16_t kc = (buffer[i] << 8) | buffer[i + 1];
      0080FD C0 07            [24] 1893 	push	ar7
      0080FF EE               [12] 1894 	mov	a,r6
      008100 28               [12] 1895 	add	a, r0
      008101 FC               [12] 1896 	mov	r4,a
      008102 E4               [12] 1897 	clr	a
      008103 39               [12] 1898 	addc	a, r1
      008104 FD               [12] 1899 	mov	r5,a
      008105 8C 82            [24] 1900 	mov	dpl,r4
      008107 8D 83            [24] 1901 	mov	dph,r5
      008109 E0               [24] 1902 	movx	a,@dptr
      00810A FA               [12] 1903 	mov	r2,a
      00810B 7B 00            [12] 1904 	mov	r3,#0x00
      00810D 8E 3A            [24] 1905 	mov	_dynamic_keymap_set_buffer_sloc1_1_0,r6
      00810F 8B 3B            [24] 1906 	mov	(_dynamic_keymap_set_buffer_sloc1_1_0 + 1),r3
      008111 74 01            [12] 1907 	mov	a,#0x01
      008113 25 3A            [12] 1908 	add	a, _dynamic_keymap_set_buffer_sloc1_1_0
      008115 FE               [12] 1909 	mov	r6,a
      008116 E4               [12] 1910 	clr	a
      008117 35 3B            [12] 1911 	addc	a, (_dynamic_keymap_set_buffer_sloc1_1_0 + 1)
      008119 FF               [12] 1912 	mov	r7,a
      00811A EE               [12] 1913 	mov	a,r6
      00811B 28               [12] 1914 	add	a, r0
      00811C F5 82            [12] 1915 	mov	dpl,a
      00811E EF               [12] 1916 	mov	a,r7
      00811F 39               [12] 1917 	addc	a, r1
      008120 F5 83            [12] 1918 	mov	dph,a
      008122 E0               [24] 1919 	movx	a,@dptr
      008123 7E 00            [12] 1920 	mov	r6,#0x00
      008125 42 03            [12] 1921 	orl	ar3,a
      008127 EE               [12] 1922 	mov	a,r6
      008128 42 02            [12] 1923 	orl	ar2,a
                                   1924 ;	quantum/dynamic_keymap.c:440: if (kc == QK_BOOT) {
      00812A BB 00 05         [24] 1925 	cjne	r3,#0x00,00216$
      00812D BA 7C 02         [24] 1926 	cjne	r2,#0x7c,00216$
      008130 80 04            [24] 1927 	sjmp	00217$
      008132                       1928 00216$:
      008132 D0 07            [24] 1929 	pop	ar7
      008134 80 1D            [24] 1930 	sjmp	00123$
      008136                       1931 00217$:
      008136 D0 07            [24] 1932 	pop	ar7
                                   1933 ;	quantum/dynamic_keymap.c:441: buffer[i] = 0xFF;
      008138 8C 82            [24] 1934 	mov	dpl,r4
      00813A 8D 83            [24] 1935 	mov	dph,r5
      00813C 74 FF            [12] 1936 	mov	a,#0xff
      00813E F0               [24] 1937 	movx	@dptr,a
                                   1938 ;	quantum/dynamic_keymap.c:442: buffer[i + 1] = 0xFF;
      00813F 74 01            [12] 1939 	mov	a,#0x01
      008141 25 3A            [12] 1940 	add	a, _dynamic_keymap_set_buffer_sloc1_1_0
      008143 FD               [12] 1941 	mov	r5,a
      008144 E4               [12] 1942 	clr	a
      008145 35 3B            [12] 1943 	addc	a, (_dynamic_keymap_set_buffer_sloc1_1_0 + 1)
      008147 FE               [12] 1944 	mov	r6,a
      008148 ED               [12] 1945 	mov	a,r5
      008149 28               [12] 1946 	add	a, r0
      00814A F5 82            [12] 1947 	mov	dpl,a
      00814C EE               [12] 1948 	mov	a,r6
      00814D 39               [12] 1949 	addc	a, r1
      00814E F5 83            [12] 1950 	mov	dph,a
      008150 74 FF            [12] 1951 	mov	a,#0xff
      008152 F0               [24] 1952 	movx	@dptr,a
      008153                       1953 00123$:
                                   1954 ;	quantum/dynamic_keymap.c:438: for (dynamic_buffer_size_t i = chk_offset; i < chk_sz; i += 2) {
      008153 90 09 08         [24] 1955 	mov	dptr,#_dynamic_keymap_set_buffer_i_40001_324
      008156 E0               [24] 1956 	movx	a,@dptr
      008157 24 02            [12] 1957 	add	a,#0x02
      008159 F0               [24] 1958 	movx	@dptr,a
      00815A 80 98            [24] 1959 	sjmp	00122$
      00815C                       1960 00120$:
                                   1961 ;	quantum/dynamic_keymap.c:453: eeprom_write_block(data, (void *)(uintptr_t)(DYNAMIC_KEYMAP_EEPROM_ADDR + offset), size);
      00815C AD 37            [24] 1962 	mov	r5,_dynamic_keymap_set_buffer_sloc0_1_0
      00815E AE 38            [24] 1963 	mov	r6,(_dynamic_keymap_set_buffer_sloc0_1_0 + 1)
      008160 AF 39            [24] 1964 	mov	r7,(_dynamic_keymap_set_buffer_sloc0_1_0 + 2)
      008162 90 09 04         [24] 1965 	mov	dptr,#_dynamic_keymap_set_buffer_offset_10000_310
      008165 E0               [24] 1966 	movx	a,@dptr
      008166 FB               [12] 1967 	mov	r3,a
      008167 A3               [24] 1968 	inc	dptr
      008168 E0               [24] 1969 	movx	a,@dptr
      008169 FC               [12] 1970 	mov	r4,a
      00816A 74 40            [12] 1971 	mov	a,#0x40
      00816C 2B               [12] 1972 	add	a, r3
      00816D FB               [12] 1973 	mov	r3,a
      00816E E4               [12] 1974 	clr	a
      00816F 3C               [12] 1975 	addc	a, r4
      008170 FC               [12] 1976 	mov	r4,a
      008171 90 05 48         [24] 1977 	mov	dptr,#_eeprom_write_block_PARM_2
      008174 EB               [12] 1978 	mov	a,r3
      008175 F0               [24] 1979 	movx	@dptr,a
      008176 EC               [12] 1980 	mov	a,r4
      008177 A3               [24] 1981 	inc	dptr
      008178 F0               [24] 1982 	movx	@dptr,a
      008179 E4               [12] 1983 	clr	a
      00817A A3               [24] 1984 	inc	dptr
      00817B F0               [24] 1985 	movx	@dptr,a
      00817C 90 05 4B         [24] 1986 	mov	dptr,#_eeprom_write_block_PARM_3
      00817F E5 3C            [12] 1987 	mov	a,_dynamic_keymap_set_buffer_sloc2_1_0
      008181 F0               [24] 1988 	movx	@dptr,a
      008182 E5 3D            [12] 1989 	mov	a,(_dynamic_keymap_set_buffer_sloc2_1_0 + 1)
      008184 A3               [24] 1990 	inc	dptr
      008185 F0               [24] 1991 	movx	@dptr,a
      008186 8D 82            [24] 1992 	mov	dpl, r5
      008188 8E 83            [24] 1993 	mov	dph, r6
      00818A 8F F0            [24] 1994 	mov	b, r7
                                   1995 ;	quantum/dynamic_keymap.c:463: }
      00818C 02 3E 67         [24] 1996 	ljmp	_eeprom_write_block
                                   1997 ;------------------------------------------------------------
                                   1998 ;Allocation info for local variables in function 'keycode_at_keymap_location'
                                   1999 ;------------------------------------------------------------
                                   2000 ;row           Allocated with name '_keycode_at_keymap_location_PARM_2'
                                   2001 ;column        Allocated with name '_keycode_at_keymap_location_PARM_3'
                                   2002 ;layer_num     Allocated with name '_keycode_at_keymap_location_layer_num_10000_328'
                                   2003 ;------------------------------------------------------------
                                   2004 ;	quantum/dynamic_keymap.c:465: uint16_t keycode_at_keymap_location(uint8_t layer_num, uint8_t row, uint8_t column) {
                                   2005 ;	-----------------------------------------
                                   2006 ;	 function keycode_at_keymap_location
                                   2007 ;	-----------------------------------------
      00818F                       2008 _keycode_at_keymap_location:
      00818F E5 82            [12] 2009 	mov	a,dpl
      008191 90 09 0B         [24] 2010 	mov	dptr,#_keycode_at_keymap_location_layer_num_10000_328
      008194 F0               [24] 2011 	movx	@dptr,a
                                   2012 ;	quantum/dynamic_keymap.c:466: if (layer_num < DYNAMIC_KEYMAP_LAYER_COUNT && row < MATRIX_ROWS && column < MATRIX_COLS) {
      008195 E0               [24] 2013 	movx	a,@dptr
      008196 FF               [12] 2014 	mov	r7,a
      008197 BF 06 00         [24] 2015 	cjne	r7,#0x06,00128$
      00819A                       2016 00128$:
      00819A 50 23            [24] 2017 	jnc	00102$
      00819C 90 09 09         [24] 2018 	mov	dptr,#_keycode_at_keymap_location_PARM_2
      00819F E0               [24] 2019 	movx	a,@dptr
      0081A0 FE               [12] 2020 	mov	r6,a
      0081A1 BE 10 00         [24] 2021 	cjne	r6,#0x10,00130$
      0081A4                       2022 00130$:
      0081A4 50 19            [24] 2023 	jnc	00102$
      0081A6 90 09 0A         [24] 2024 	mov	dptr,#_keycode_at_keymap_location_PARM_3
      0081A9 E0               [24] 2025 	movx	a,@dptr
      0081AA FD               [12] 2026 	mov	r5,a
      0081AB BD 08 00         [24] 2027 	cjne	r5,#0x08,00132$
      0081AE                       2028 00132$:
      0081AE 50 0F            [24] 2029 	jnc	00102$
                                   2030 ;	quantum/dynamic_keymap.c:467: return dynamic_keymap_get_keycode(layer_num, row, column);
      0081B0 90 08 D9         [24] 2031 	mov	dptr,#_dynamic_keymap_get_keycode_PARM_2
      0081B3 EE               [12] 2032 	mov	a,r6
      0081B4 F0               [24] 2033 	movx	@dptr,a
      0081B5 90 08 DA         [24] 2034 	mov	dptr,#_dynamic_keymap_get_keycode_PARM_3
      0081B8 ED               [12] 2035 	mov	a,r5
      0081B9 F0               [24] 2036 	movx	@dptr,a
      0081BA 8F 82            [24] 2037 	mov	dpl, r7
      0081BC 02 7B C5         [24] 2038 	ljmp	_dynamic_keymap_get_keycode
      0081BF                       2039 00102$:
                                   2040 ;	quantum/dynamic_keymap.c:469: return KC_NO;
      0081BF 90 00 00         [24] 2041 	mov	dptr,#0x0000
                                   2042 ;	quantum/dynamic_keymap.c:470: }
      0081C2 22               [24] 2043 	ret
                                   2044 ;------------------------------------------------------------
                                   2045 ;Allocation info for local variables in function 'keycode_at_encodermap_location'
                                   2046 ;------------------------------------------------------------
                                   2047 ;encoder_idx   Allocated with name '_keycode_at_encodermap_location_PARM_2'
                                   2048 ;clockwise     Allocated with name '_keycode_at_encodermap_location_PARM_3'
                                   2049 ;layer_num     Allocated with name '_keycode_at_encodermap_location_layer_num_10000_332'
                                   2050 ;------------------------------------------------------------
                                   2051 ;	quantum/dynamic_keymap.c:473: uint16_t keycode_at_encodermap_location(uint8_t layer_num, uint8_t encoder_idx, bool clockwise) {
                                   2052 ;	-----------------------------------------
                                   2053 ;	 function keycode_at_encodermap_location
                                   2054 ;	-----------------------------------------
      0081C3                       2055 _keycode_at_encodermap_location:
      0081C3 E5 82            [12] 2056 	mov	a,dpl
      0081C5 90 09 0E         [24] 2057 	mov	dptr,#_keycode_at_encodermap_location_layer_num_10000_332
      0081C8 F0               [24] 2058 	movx	@dptr,a
                                   2059 ;	quantum/dynamic_keymap.c:474: if (layer_num < DYNAMIC_KEYMAP_LAYER_COUNT && encoder_idx < NUM_ENCODERS) {
      0081C9 E0               [24] 2060 	movx	a,@dptr
      0081CA FF               [12] 2061 	mov	r7,a
      0081CB BF 06 00         [24] 2062 	cjne	r7,#0x06,00120$
      0081CE                       2063 00120$:
      0081CE 50 1E            [24] 2064 	jnc	00102$
      0081D0 90 09 0C         [24] 2065 	mov	dptr,#_keycode_at_encodermap_location_PARM_2
      0081D3 E0               [24] 2066 	movx	a,@dptr
      0081D4 FE               [12] 2067 	mov	r6,a
      0081D5 BE 01 00         [24] 2068 	cjne	r6,#0x01,00122$
      0081D8                       2069 00122$:
      0081D8 50 14            [24] 2070 	jnc	00102$
                                   2071 ;	quantum/dynamic_keymap.c:475: return dynamic_keymap_get_encoder(layer_num, encoder_idx, clockwise);
      0081DA 90 09 0D         [24] 2072 	mov	dptr,#_keycode_at_encodermap_location_PARM_3
      0081DD E0               [24] 2073 	movx	a,@dptr
      0081DE FE               [12] 2074 	mov	r6,a
      0081DF 90 08 E3         [24] 2075 	mov	dptr,#_dynamic_keymap_get_encoder_PARM_2
      0081E2 E4               [12] 2076 	clr	a
      0081E3 F0               [24] 2077 	movx	@dptr,a
      0081E4 90 08 E4         [24] 2078 	mov	dptr,#_dynamic_keymap_get_encoder_PARM_3
      0081E7 EE               [12] 2079 	mov	a,r6
      0081E8 F0               [24] 2080 	movx	@dptr,a
      0081E9 8F 82            [24] 2081 	mov	dpl, r7
      0081EB 02 7C AB         [24] 2082 	ljmp	_dynamic_keymap_get_encoder
      0081EE                       2083 00102$:
                                   2084 ;	quantum/dynamic_keymap.c:477: return KC_NO;
      0081EE 90 00 00         [24] 2085 	mov	dptr,#0x0000
                                   2086 ;	quantum/dynamic_keymap.c:478: }
      0081F1 22               [24] 2087 	ret
                                   2088 ;------------------------------------------------------------
                                   2089 ;Allocation info for local variables in function 'dynamic_keymap_macro_get_count'
                                   2090 ;------------------------------------------------------------
                                   2091 ;	quantum/dynamic_keymap.c:481: uint8_t dynamic_keymap_macro_get_count(void) {
                                   2092 ;	-----------------------------------------
                                   2093 ;	 function dynamic_keymap_macro_get_count
                                   2094 ;	-----------------------------------------
      0081F2                       2095 _dynamic_keymap_macro_get_count:
                                   2096 ;	quantum/dynamic_keymap.c:482: return DYNAMIC_KEYMAP_MACRO_COUNT;
      0081F2 75 82 10         [24] 2097 	mov	dpl, #0x10
                                   2098 ;	quantum/dynamic_keymap.c:483: }
      0081F5 22               [24] 2099 	ret
                                   2100 ;------------------------------------------------------------
                                   2101 ;Allocation info for local variables in function 'dynamic_keymap_macro_get_buffer_size'
                                   2102 ;------------------------------------------------------------
                                   2103 ;	quantum/dynamic_keymap.c:485: uint16_t dynamic_keymap_macro_get_buffer_size(void) {
                                   2104 ;	-----------------------------------------
                                   2105 ;	 function dynamic_keymap_macro_get_buffer_size
                                   2106 ;	-----------------------------------------
      0081F6                       2107 _dynamic_keymap_macro_get_buffer_size:
                                   2108 ;	quantum/dynamic_keymap.c:486: return DYNAMIC_KEYMAP_MACRO_EEPROM_SIZE;
      0081F6 90 20 00         [24] 2109 	mov	dptr,#0x2000
                                   2110 ;	quantum/dynamic_keymap.c:487: }
      0081F9 22               [24] 2111 	ret
                                   2112 ;------------------------------------------------------------
                                   2113 ;Allocation info for local variables in function 'dynamic_keymap_macro_get_buffer'
                                   2114 ;------------------------------------------------------------
                                   2115 ;sloc0         Allocated with name '_dynamic_keymap_macro_get_buffer_sloc0_1_0'
                                   2116 ;size          Allocated with name '_dynamic_keymap_macro_get_buffer_PARM_2'
                                   2117 ;data          Allocated with name '_dynamic_keymap_macro_get_buffer_PARM_3'
                                   2118 ;offset        Allocated with name '_dynamic_keymap_macro_get_buffer_offset_10000_340'
                                   2119 ;------------------------------------------------------------
                                   2120 ;	quantum/dynamic_keymap.c:489: void dynamic_keymap_macro_get_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
                                   2121 ;	-----------------------------------------
                                   2122 ;	 function dynamic_keymap_macro_get_buffer
                                   2123 ;	-----------------------------------------
      0081FA                       2124 _dynamic_keymap_macro_get_buffer:
      0081FA AF 83            [24] 2125 	mov	r7,dph
      0081FC E5 82            [12] 2126 	mov	a,dpl
      0081FE 90 09 14         [24] 2127 	mov	dptr,#_dynamic_keymap_macro_get_buffer_offset_10000_340
      008201 F0               [24] 2128 	movx	@dptr,a
      008202 EF               [12] 2129 	mov	a,r7
      008203 A3               [24] 2130 	inc	dptr
      008204 F0               [24] 2131 	movx	@dptr,a
                                   2132 ;	quantum/dynamic_keymap.c:492: ak820_macro_length(), offset, size, data);
      008205 12 2A E5         [24] 2133 	lcall	_ak820_macro_length
      008208 AE 82            [24] 2134 	mov	r6, dpl
      00820A AF 83            [24] 2135 	mov	r7, dph
      00820C 90 09 14         [24] 2136 	mov	dptr,#_dynamic_keymap_macro_get_buffer_offset_10000_340
      00820F E0               [24] 2137 	movx	a,@dptr
      008210 FC               [12] 2138 	mov	r4,a
      008211 A3               [24] 2139 	inc	dptr
      008212 E0               [24] 2140 	movx	a,@dptr
      008213 FD               [12] 2141 	mov	r5,a
      008214 90 09 0F         [24] 2142 	mov	dptr,#_dynamic_keymap_macro_get_buffer_PARM_2
      008217 E0               [24] 2143 	movx	a,@dptr
      008218 F5 3F            [12] 2144 	mov	_dynamic_keymap_macro_get_buffer_sloc0_1_0,a
      00821A A3               [24] 2145 	inc	dptr
      00821B E0               [24] 2146 	movx	a,@dptr
      00821C F5 40            [12] 2147 	mov	(_dynamic_keymap_macro_get_buffer_sloc0_1_0 + 1),a
      00821E 90 09 11         [24] 2148 	mov	dptr,#_dynamic_keymap_macro_get_buffer_PARM_3
      008221 E0               [24] 2149 	movx	a,@dptr
      008222 F8               [12] 2150 	mov	r0,a
      008223 A3               [24] 2151 	inc	dptr
      008224 E0               [24] 2152 	movx	a,@dptr
      008225 F9               [12] 2153 	mov	r1,a
      008226 A3               [24] 2154 	inc	dptr
      008227 E0               [24] 2155 	movx	a,@dptr
      008228 FB               [12] 2156 	mov	r3,a
      008229 90 08 EC         [24] 2157 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_2
      00822C EE               [12] 2158 	mov	a,r6
      00822D F0               [24] 2159 	movx	@dptr,a
      00822E EF               [12] 2160 	mov	a,r7
      00822F A3               [24] 2161 	inc	dptr
      008230 F0               [24] 2162 	movx	@dptr,a
      008231 90 08 EE         [24] 2163 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_3
      008234 EC               [12] 2164 	mov	a,r4
      008235 F0               [24] 2165 	movx	@dptr,a
      008236 ED               [12] 2166 	mov	a,r5
      008237 A3               [24] 2167 	inc	dptr
      008238 F0               [24] 2168 	movx	@dptr,a
      008239 90 08 F0         [24] 2169 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_4
      00823C E5 3F            [12] 2170 	mov	a,_dynamic_keymap_macro_get_buffer_sloc0_1_0
      00823E F0               [24] 2171 	movx	@dptr,a
      00823F E5 40            [12] 2172 	mov	a,(_dynamic_keymap_macro_get_buffer_sloc0_1_0 + 1)
      008241 A3               [24] 2173 	inc	dptr
      008242 F0               [24] 2174 	movx	@dptr,a
      008243 90 08 F2         [24] 2175 	mov	dptr,#_ak820_dynamic_read_buffer_PARM_5
      008246 E8               [12] 2176 	mov	a,r0
      008247 F0               [24] 2177 	movx	@dptr,a
      008248 E9               [12] 2178 	mov	a,r1
      008249 A3               [24] 2179 	inc	dptr
      00824A F0               [24] 2180 	movx	@dptr,a
      00824B EB               [12] 2181 	mov	a,r3
      00824C A3               [24] 2182 	inc	dptr
      00824D F0               [24] 2183 	movx	@dptr,a
      00824E 90 08 00         [24] 2184 	mov	dptr,#0x0800
                                   2185 ;	quantum/dynamic_keymap.c:514: }
      008251 02 7E 9B         [24] 2186 	ljmp	_ak820_dynamic_read_buffer
                                   2187 ;------------------------------------------------------------
                                   2188 ;Allocation info for local variables in function 'dynamic_keymap_macro_set_buffer'
                                   2189 ;------------------------------------------------------------
                                   2190 ;size          Allocated with name '_dynamic_keymap_macro_set_buffer_PARM_2'
                                   2191 ;data          Allocated with name '_dynamic_keymap_macro_set_buffer_PARM_3'
                                   2192 ;offset        Allocated with name '_dynamic_keymap_macro_set_buffer_offset_10000_342'
                                   2193 ;------------------------------------------------------------
                                   2194 ;	quantum/dynamic_keymap.c:517: bool dynamic_keymap_macro_set_buffer(uint16_t offset, uint16_t size, uint8_t *data) {
                                   2195 ;	-----------------------------------------
                                   2196 ;	 function dynamic_keymap_macro_set_buffer
                                   2197 ;	-----------------------------------------
      008254                       2198 _dynamic_keymap_macro_set_buffer:
      008254 AF 83            [24] 2199 	mov	r7,dph
      008256 E5 82            [12] 2200 	mov	a,dpl
      008258 90 09 1B         [24] 2201 	mov	dptr,#_dynamic_keymap_macro_set_buffer_offset_10000_342
      00825B F0               [24] 2202 	movx	@dptr,a
      00825C EF               [12] 2203 	mov	a,r7
      00825D A3               [24] 2204 	inc	dptr
      00825E F0               [24] 2205 	movx	@dptr,a
                                   2206 ;	quantum/dynamic_keymap.c:518: return ak820_macro_write(offset, size, data);
      00825F 90 09 1B         [24] 2207 	mov	dptr,#_dynamic_keymap_macro_set_buffer_offset_10000_342
      008262 E0               [24] 2208 	movx	a,@dptr
      008263 FE               [12] 2209 	mov	r6,a
      008264 A3               [24] 2210 	inc	dptr
      008265 E0               [24] 2211 	movx	a,@dptr
      008266 FF               [12] 2212 	mov	r7,a
      008267 90 09 16         [24] 2213 	mov	dptr,#_dynamic_keymap_macro_set_buffer_PARM_2
      00826A E0               [24] 2214 	movx	a,@dptr
      00826B FC               [12] 2215 	mov	r4,a
      00826C A3               [24] 2216 	inc	dptr
      00826D E0               [24] 2217 	movx	a,@dptr
      00826E FD               [12] 2218 	mov	r5,a
      00826F 90 09 18         [24] 2219 	mov	dptr,#_dynamic_keymap_macro_set_buffer_PARM_3
      008272 E0               [24] 2220 	movx	a,@dptr
      008273 F9               [12] 2221 	mov	r1,a
      008274 A3               [24] 2222 	inc	dptr
      008275 E0               [24] 2223 	movx	a,@dptr
      008276 FA               [12] 2224 	mov	r2,a
      008277 A3               [24] 2225 	inc	dptr
      008278 E0               [24] 2226 	movx	a,@dptr
      008279 FB               [12] 2227 	mov	r3,a
      00827A 90 04 CC         [24] 2228 	mov	dptr,#_ak820_macro_write_PARM_2
      00827D EC               [12] 2229 	mov	a,r4
      00827E F0               [24] 2230 	movx	@dptr,a
      00827F ED               [12] 2231 	mov	a,r5
      008280 A3               [24] 2232 	inc	dptr
      008281 F0               [24] 2233 	movx	@dptr,a
      008282 90 04 CE         [24] 2234 	mov	dptr,#_ak820_macro_write_PARM_3
      008285 E9               [12] 2235 	mov	a,r1
      008286 F0               [24] 2236 	movx	@dptr,a
      008287 EA               [12] 2237 	mov	a,r2
      008288 A3               [24] 2238 	inc	dptr
      008289 F0               [24] 2239 	movx	@dptr,a
      00828A EB               [12] 2240 	mov	a,r3
      00828B A3               [24] 2241 	inc	dptr
      00828C F0               [24] 2242 	movx	@dptr,a
      00828D 8E 82            [24] 2243 	mov	dpl, r6
      00828F 8F 83            [24] 2244 	mov	dph, r7
                                   2245 ;	quantum/dynamic_keymap.c:519: }
      008291 02 2A FF         [24] 2246 	ljmp	_ak820_macro_write
                                   2247 ;------------------------------------------------------------
                                   2248 ;Allocation info for local variables in function 'dynamic_keymap_macro_reset'
                                   2249 ;------------------------------------------------------------
                                   2250 ;	quantum/dynamic_keymap.c:534: void dynamic_keymap_macro_reset(void) {
                                   2251 ;	-----------------------------------------
                                   2252 ;	 function dynamic_keymap_macro_reset
                                   2253 ;	-----------------------------------------
      008294                       2254 _dynamic_keymap_macro_reset:
                                   2255 ;	quantum/dynamic_keymap.c:536: ak820_macro_reset();
                                   2256 ;	quantum/dynamic_keymap.c:545: }
      008294 02 2E 6B         [24] 2257 	ljmp	_ak820_macro_reset
                                   2258 ;------------------------------------------------------------
                                   2259 ;Allocation info for local variables in function 'decode_keycode'
                                   2260 ;------------------------------------------------------------
                                   2261 ;kc            Allocated with name '_decode_keycode_kc_10000_346'
                                   2262 ;------------------------------------------------------------
                                   2263 ;	quantum/dynamic_keymap.c:547: static uint16_t decode_keycode(uint16_t kc) {
                                   2264 ;	-----------------------------------------
                                   2265 ;	 function decode_keycode
                                   2266 ;	-----------------------------------------
      008297                       2267 _decode_keycode:
      008297 AF 83            [24] 2268 	mov	r7,dph
      008299 E5 82            [12] 2269 	mov	a,dpl
      00829B 90 09 1D         [24] 2270 	mov	dptr,#_decode_keycode_kc_10000_346
      00829E F0               [24] 2271 	movx	@dptr,a
      00829F EF               [12] 2272 	mov	a,r7
      0082A0 A3               [24] 2273 	inc	dptr
      0082A1 F0               [24] 2274 	movx	@dptr,a
                                   2275 ;	quantum/dynamic_keymap.c:549: if (kc > 0xFF00)
      0082A2 90 09 1D         [24] 2276 	mov	dptr,#_decode_keycode_kc_10000_346
      0082A5 12 86 05         [24] 2277 	lcall	_ak820_outline_0012
      0082A8 C3               [12] 2278 	clr	c
      0082A9 E4               [12] 2279 	clr	a
      0082AA 9C               [12] 2280 	subb	a,r4
      0082AB 74 FF            [12] 2281 	mov	a,#0xff
      0082AD 9D               [12] 2282 	subb	a,r5
      0082AE 50 09            [24] 2283 	jnc	00102$
                                   2284 ;	free result
                                   2285 ;	quantum/dynamic_keymap.c:550: return (kc & 0xFF) << 8;
      0082B0 8C 05            [24] 2286 	mov	ar5,r4
      0082B2 7C 00            [12] 2287 	mov	r4,#0x00
      0082B4 8C 82            [24] 2288 	mov	dpl, r4
      0082B6 8D 83            [24] 2289 	mov	dph, r5
      0082B8 22               [24] 2290 	ret
      0082B9                       2291 00102$:
                                   2292 ;	quantum/dynamic_keymap.c:551: return kc;
      0082B9 8E 82            [24] 2293 	mov	dpl, r6
      0082BB 8F 83            [24] 2294 	mov	dph, r7
                                   2295 ;	quantum/dynamic_keymap.c:552: }
      0082BD 22               [24] 2296 	ret
                                   2297 ;------------------------------------------------------------
                                   2298 ;Allocation info for local variables in function 'dynamic_keymap_macro_send'
                                   2299 ;------------------------------------------------------------
                                   2300 ;id            Allocated with name '_dynamic_keymap_macro_send_id_10000_349'
                                   2301 ;sending       Allocated with name '_dynamic_keymap_macro_send_sending_10000_350'
                                   2302 ;p             Allocated with name '_dynamic_keymap_macro_send_p_10001_355'
                                   2303 ;end           Allocated with name '_dynamic_keymap_macro_send_end_10002_356'
                                   2304 ;data          Allocated with name '_dynamic_keymap_macro_send_data_10003_362'
                                   2305 ;kc            Allocated with name '_dynamic_keymap_macro_send_kc_110003_380'
                                   2306 ;d0            Allocated with name '_dynamic_keymap_macro_send_d0_80003_384'
                                   2307 ;d1            Allocated with name '_dynamic_keymap_macro_send_d1_80003_384'
                                   2308 ;ms            Allocated with name '_dynamic_keymap_macro_send_ms_80004_386'
                                   2309 ;i             Allocated with name '_dynamic_keymap_macro_send_i_100004_388'
                                   2310 ;delay         Allocated with name '_dynamic_keymap_macro_send_delay_50003_392'
                                   2311 ;i             Allocated with name '_dynamic_keymap_macro_send_i_70003_394'
                                   2312 ;------------------------------------------------------------
                                   2313 ;	quantum/dynamic_keymap.c:554: void dynamic_keymap_macro_send(uint8_t id) {
                                   2314 ;	-----------------------------------------
                                   2315 ;	 function dynamic_keymap_macro_send
                                   2316 ;	-----------------------------------------
      0082BE                       2317 _dynamic_keymap_macro_send:
      0082BE E5 82            [12] 2318 	mov	a,dpl
      0082C0 90 09 1F         [24] 2319 	mov	dptr,#_dynamic_keymap_macro_send_id_10000_349
      0082C3 F0               [24] 2320 	movx	@dptr,a
                                   2321 ;	quantum/dynamic_keymap.c:559: if (sending) return;
      0082C4 90 09 20         [24] 2322 	mov	dptr,#_dynamic_keymap_macro_send_sending_10000_350
      0082C7 E0               [24] 2323 	movx	a,@dptr
      0082C8 60 01            [24] 2324 	jz	00102$
      0082CA 22               [24] 2325 	ret
      0082CB                       2326 00102$:
                                   2327 ;	quantum/dynamic_keymap.c:561: if (id >= DYNAMIC_KEYMAP_MACRO_COUNT) {
      0082CB 90 09 1F         [24] 2328 	mov	dptr,#_dynamic_keymap_macro_send_id_10000_349
      0082CE E0               [24] 2329 	movx	a,@dptr
      0082CF FF               [12] 2330 	mov	r7,a
      0082D0 BF 10 00         [24] 2331 	cjne	r7,#0x10,00414$
      0082D3                       2332 00414$:
      0082D3 40 01            [24] 2333 	jc	00104$
                                   2334 ;	quantum/dynamic_keymap.c:562: return;
      0082D5 22               [24] 2335 	ret
      0082D6                       2336 00104$:
                                   2337 ;	quantum/dynamic_keymap.c:568: if (!ak820_macro_ready()) return;
      0082D6 C0 07            [24] 2338 	push	ar7
      0082D8 12 2A AC         [24] 2339 	lcall	_ak820_macro_ready
      0082DB E5 82            [12] 2340 	mov	a, dpl
      0082DD D0 07            [24] 2341 	pop	ar7
      0082DF 70 01            [24] 2342 	jnz	00106$
      0082E1 22               [24] 2343 	ret
      0082E2                       2344 00106$:
                                   2345 ;	quantum/dynamic_keymap.c:583: p         = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR);
      0082E2 90 09 21         [24] 2346 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      0082E5 E4               [12] 2347 	clr	a
      0082E6 F0               [24] 2348 	movx	@dptr,a
      0082E7 74 08            [12] 2349 	mov	a,#0x08
      0082E9 A3               [24] 2350 	inc	dptr
      0082EA F0               [24] 2351 	movx	@dptr,a
      0082EB E4               [12] 2352 	clr	a
      0082EC A3               [24] 2353 	inc	dptr
      0082ED F0               [24] 2354 	movx	@dptr,a
                                   2355 ;	quantum/dynamic_keymap.c:585: uint8_t *end = (uint8_t *)(DYNAMIC_KEYMAP_MACRO_EEPROM_ADDR + ak820_macro_length());
      0082EE C0 07            [24] 2356 	push	ar7
      0082F0 12 2A E5         [24] 2357 	lcall	_ak820_macro_length
      0082F3 AD 82            [24] 2358 	mov	r5, dpl
      0082F5 AE 83            [24] 2359 	mov	r6, dph
      0082F7 D0 07            [24] 2360 	pop	ar7
      0082F9 74 08            [12] 2361 	mov	a,#0x08
      0082FB 2E               [12] 2362 	add	a, r6
      0082FC FC               [12] 2363 	mov	r4,a
      0082FD 7E 00            [12] 2364 	mov	r6,#0x00
                                   2365 ;	quantum/dynamic_keymap.c:589: while (id > 0) {
      0082FF 79 00            [12] 2366 	mov	r1,#0x00
      008301 7A 08            [12] 2367 	mov	r2,#0x08
      008303 7B 00            [12] 2368 	mov	r3,#0x00
      008305                       2369 00111$:
      008305 EF               [12] 2370 	mov	a,r7
      008306 60 3D            [24] 2371 	jz	00113$
                                   2372 ;	quantum/dynamic_keymap.c:593: if (p == end) {
      008308 C0 05            [24] 2373 	push	ar5
      00830A C0 04            [24] 2374 	push	ar4
      00830C C0 06            [24] 2375 	push	ar6
      00830E 89 82            [24] 2376 	mov	dpl,r1
      008310 8A 83            [24] 2377 	mov	dph,r2
      008312 8B F0            [24] 2378 	mov	b,r3
      008314 12 30 77         [24] 2379 	lcall	___gptr_cmp
      008317 15 81            [12] 2380 	dec	sp
      008319 15 81            [12] 2381 	dec	sp
      00831B 15 81            [12] 2382 	dec	sp
      00831D 70 01            [24] 2383 	jnz	00108$
                                   2384 ;	quantum/dynamic_keymap.c:594: return;
      00831F 22               [24] 2385 	ret
      008320                       2386 00108$:
                                   2387 ;	quantum/dynamic_keymap.c:596: if (eeprom_read_byte(p) == 0) {
      008320 89 82            [24] 2388 	mov	dpl, r1
      008322 8A 83            [24] 2389 	mov	dph, r2
      008324 8B F0            [24] 2390 	mov	b, r3
      008326 12 43 FC         [24] 2391 	lcall	_eeprom_read_byte
      008329 E5 82            [12] 2392 	mov	a, dpl
      00832B 70 06            [24] 2393 	jnz	00110$
                                   2394 ;	quantum/dynamic_keymap.c:597: --id;
      00832D 1F               [12] 2395 	dec	r7
      00832E 90 09 1F         [24] 2396 	mov	dptr,#_dynamic_keymap_macro_send_id_10000_349
      008331 EF               [12] 2397 	mov	a,r7
      008332 F0               [24] 2398 	movx	@dptr,a
      008333                       2399 00110$:
                                   2400 ;	quantum/dynamic_keymap.c:599: ++p;
      008333 09               [12] 2401 	inc	r1
      008334 B9 00 01         [24] 2402 	cjne	r1,#0x00,00421$
      008337 0A               [12] 2403 	inc	r2
      008338                       2404 00421$:
      008338 90 09 21         [24] 2405 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      00833B E9               [12] 2406 	mov	a,r1
      00833C F0               [24] 2407 	movx	@dptr,a
      00833D EA               [12] 2408 	mov	a,r2
      00833E A3               [24] 2409 	inc	dptr
      00833F F0               [24] 2410 	movx	@dptr,a
      008340 EB               [12] 2411 	mov	a,r3
      008341 A3               [24] 2412 	inc	dptr
      008342 F0               [24] 2413 	movx	@dptr,a
      008343 80 C0            [24] 2414 	sjmp	00111$
      008345                       2415 00113$:
                                   2416 ;	quantum/dynamic_keymap.c:605: sending = true;
      008345 90 09 20         [24] 2417 	mov	dptr,#_dynamic_keymap_macro_send_sending_10000_350
      008348 74 01            [12] 2418 	mov	a,#0x01
      00834A F0               [24] 2419 	movx	@dptr,a
                                   2420 ;	quantum/dynamic_keymap.c:609: char data[4] = {0, 0, 0, 0};
      00834B 90 09 24         [24] 2421 	mov	dptr,#_dynamic_keymap_macro_send_data_10003_362
      00834E E4               [12] 2422 	clr	a
      00834F F0               [24] 2423 	movx	@dptr,a
      008350 90 09 25         [24] 2424 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      008353 F0               [24] 2425 	movx	@dptr,a
      008354 90 09 26         [24] 2426 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0002)
      008357 F0               [24] 2427 	movx	@dptr,a
      008358 90 09 27         [24] 2428 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0003)
      00835B F0               [24] 2429 	movx	@dptr,a
                                   2430 ;	quantum/dynamic_keymap.c:612: while (p < end) {
      00835C 8C 07            [24] 2431 	mov	ar7,r4
      00835E                       2432 00166$:
      00835E 90 09 21         [24] 2433 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      008361 E0               [24] 2434 	movx	a,@dptr
      008362 FA               [12] 2435 	mov	r2,a
      008363 A3               [24] 2436 	inc	dptr
      008364 E0               [24] 2437 	movx	a,@dptr
      008365 FB               [12] 2438 	mov	r3,a
      008366 A3               [24] 2439 	inc	dptr
      008367 E0               [24] 2440 	movx	a,@dptr
      008368 FC               [12] 2441 	mov	r4,a
      008369 C0 05            [24] 2442 	push	ar5
      00836B C0 07            [24] 2443 	push	ar7
      00836D C0 06            [24] 2444 	push	ar6
      00836F 8A 82            [24] 2445 	mov	dpl,r2
      008371 8B 83            [24] 2446 	mov	dph,r3
      008373 8C F0            [24] 2447 	mov	b,r4
      008375 12 30 77         [24] 2448 	lcall	___gptr_cmp
      008378 15 81            [12] 2449 	dec	sp
      00837A 15 81            [12] 2450 	dec	sp
      00837C 15 81            [12] 2451 	dec	sp
      00837E 40 03            [24] 2452 	jc	00422$
      008380 02 85 E6         [24] 2453 	ljmp	00168$
      008383                       2454 00422$:
                                   2455 ;	quantum/dynamic_keymap.c:613: data[0] = eeprom_read_byte(p++);
      008383 C0 05            [24] 2456 	push	ar5
      008385 C0 07            [24] 2457 	push	ar7
      008387 8A 00            [24] 2458 	mov	ar0,r2
      008389 8B 01            [24] 2459 	mov	ar1,r3
      00838B 8C 07            [24] 2460 	mov	ar7,r4
      00838D 90 09 21         [24] 2461 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      008390 74 01            [12] 2462 	mov	a,#0x01
      008392 2A               [12] 2463 	add	a, r2
      008393 F0               [24] 2464 	movx	@dptr,a
      008394 E4               [12] 2465 	clr	a
      008395 3B               [12] 2466 	addc	a, r3
      008396 A3               [24] 2467 	inc	dptr
      008397 F0               [24] 2468 	movx	@dptr,a
      008398 EC               [12] 2469 	mov	a,r4
      008399 A3               [24] 2470 	inc	dptr
      00839A F0               [24] 2471 	movx	@dptr,a
      00839B 88 82            [24] 2472 	mov	dpl, r0
      00839D 89 83            [24] 2473 	mov	dph, r1
      00839F 8F F0            [24] 2474 	mov	b, r7
      0083A1 12 43 FC         [24] 2475 	lcall	_eeprom_read_byte
      0083A4 AF 82            [24] 2476 	mov	r7, dpl
      0083A6 90 09 24         [24] 2477 	mov	dptr,#_dynamic_keymap_macro_send_data_10003_362
      0083A9 EF               [12] 2478 	mov	a,r7
      0083AA F0               [24] 2479 	movx	@dptr,a
                                   2480 ;	quantum/dynamic_keymap.c:614: data[1] = 0;
      0083AB 90 09 25         [24] 2481 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      0083AE E4               [12] 2482 	clr	a
      0083AF F0               [24] 2483 	movx	@dptr,a
                                   2484 ;	quantum/dynamic_keymap.c:616: if (data[0] == 0) {
      0083B0 90 09 24         [24] 2485 	mov	dptr,#_dynamic_keymap_macro_send_data_10003_362
      0083B3 E0               [24] 2486 	movx	a,@dptr
      0083B4 D0 07            [24] 2487 	pop	ar7
      0083B6 D0 05            [24] 2488 	pop	ar5
      0083B8 70 03            [24] 2489 	jnz	00423$
      0083BA 02 85 E6         [24] 2490 	ljmp	00168$
      0083BD                       2491 00423$:
                                   2492 ;	quantum/dynamic_keymap.c:619: if (data[0] == SS_QMK_PREFIX) {
      0083BD 90 09 24         [24] 2493 	mov	dptr,#_dynamic_keymap_macro_send_data_10003_362
      0083C0 E0               [24] 2494 	movx	a,@dptr
      0083C1 FC               [12] 2495 	mov	r4,a
      0083C2 BC 01 02         [24] 2496 	cjne	r4,#0x01,00424$
      0083C5 80 03            [24] 2497 	sjmp	00425$
      0083C7                       2498 00424$:
      0083C7 02 85 C4         [24] 2499 	ljmp	00164$
      0083CA                       2500 00425$:
                                   2501 ;	quantum/dynamic_keymap.c:622: data[1] = eeprom_read_byte(p++);
      0083CA 90 09 21         [24] 2502 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      0083CD E0               [24] 2503 	movx	a,@dptr
      0083CE FA               [12] 2504 	mov	r2,a
      0083CF A3               [24] 2505 	inc	dptr
      0083D0 E0               [24] 2506 	movx	a,@dptr
      0083D1 12 85 EC         [24] 2507 	lcall	_ak820_outline_0003
      0083D4 12 43 FC         [24] 2508 	lcall	_eeprom_read_byte
      0083D7 AC 82            [24] 2509 	mov	r4, dpl
      0083D9 90 09 25         [24] 2510 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      0083DC EC               [12] 2511 	mov	a,r4
      0083DD F0               [24] 2512 	movx	@dptr,a
                                   2513 ;	quantum/dynamic_keymap.c:623: if (data[1] == 0)
      0083DE EC               [12] 2514 	mov	a,r4
      0083DF 70 03            [24] 2515 	jnz	00426$
      0083E1 02 85 E6         [24] 2516 	ljmp	00168$
      0083E4                       2517 00426$:
                                   2518 ;	quantum/dynamic_keymap.c:625: if (data[1] == SS_TAP_CODE || data[1] == SS_DOWN_CODE || data[1] == SS_UP_CODE) {
      0083E4 90 09 25         [24] 2519 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      0083E7 E0               [24] 2520 	movx	a,@dptr
      0083E8 FC               [12] 2521 	mov	r4,a
      0083E9 BC 01 02         [24] 2522 	cjne	r4,#0x01,00427$
      0083EC 80 17            [24] 2523 	sjmp	00151$
      0083EE                       2524 00427$:
      0083EE 90 09 25         [24] 2525 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      0083F1 E0               [24] 2526 	movx	a,@dptr
      0083F2 FC               [12] 2527 	mov	r4,a
      0083F3 BC 02 02         [24] 2528 	cjne	r4,#0x02,00428$
      0083F6 80 0D            [24] 2529 	sjmp	00151$
      0083F8                       2530 00428$:
      0083F8 90 09 25         [24] 2531 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      0083FB E0               [24] 2532 	movx	a,@dptr
      0083FC FC               [12] 2533 	mov	r4,a
      0083FD BC 03 02         [24] 2534 	cjne	r4,#0x03,00429$
      008400 80 03            [24] 2535 	sjmp	00430$
      008402                       2536 00429$:
      008402 02 84 77         [24] 2537 	ljmp	00152$
      008405                       2538 00430$:
      008405                       2539 00151$:
                                   2540 ;	quantum/dynamic_keymap.c:627: data[2] = eeprom_read_byte(p++);
      008405 90 09 21         [24] 2541 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      008408 E0               [24] 2542 	movx	a,@dptr
      008409 FA               [12] 2543 	mov	r2,a
      00840A A3               [24] 2544 	inc	dptr
      00840B E0               [24] 2545 	movx	a,@dptr
      00840C 12 85 EC         [24] 2546 	lcall	_ak820_outline_0003
      00840F 12 43 FC         [24] 2547 	lcall	_eeprom_read_byte
      008412 AC 82            [24] 2548 	mov	r4, dpl
      008414 90 09 26         [24] 2549 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0002)
      008417 EC               [12] 2550 	mov	a,r4
      008418 F0               [24] 2551 	movx	@dptr,a
                                   2552 ;	quantum/dynamic_keymap.c:631: if (data[2] != 0) {
      008419 EC               [12] 2553 	mov	a,r4
      00841A 70 03            [24] 2554 	jnz	00431$
      00841C 02 83 5E         [24] 2555 	ljmp	00166$
      00841F                       2556 00431$:
                                   2557 ;	quantum/dynamic_keymap.c:632: if (data[1] == SS_TAP_CODE) tap_code((uint8_t)data[2]);
      00841F 90 09 25         [24] 2558 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      008422 E0               [24] 2559 	movx	a,@dptr
      008423 FC               [12] 2560 	mov	r4,a
      008424 BC 01 18         [24] 2561 	cjne	r4,#0x01,00122$
      008427 90 09 26         [24] 2562 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0002)
      00842A E0               [24] 2563 	movx	a,@dptr
      00842B F5 82            [12] 2564 	mov	dpl,a
      00842D C0 07            [24] 2565 	push	ar7
      00842F C0 06            [24] 2566 	push	ar6
      008431 C0 05            [24] 2567 	push	ar5
      008433 12 73 07         [24] 2568 	lcall	_tap_code
      008436 D0 05            [24] 2569 	pop	ar5
      008438 D0 06            [24] 2570 	pop	ar6
      00843A D0 07            [24] 2571 	pop	ar7
      00843C 02 83 5E         [24] 2572 	ljmp	00166$
      00843F                       2573 00122$:
                                   2574 ;	quantum/dynamic_keymap.c:633: else if (data[1] == SS_DOWN_CODE) register_code((uint8_t)data[2]);
      00843F 90 09 25         [24] 2575 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      008442 E0               [24] 2576 	movx	a,@dptr
      008443 FC               [12] 2577 	mov	r4,a
      008444 BC 02 18         [24] 2578 	cjne	r4,#0x02,00119$
      008447 90 09 26         [24] 2579 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0002)
      00844A E0               [24] 2580 	movx	a,@dptr
      00844B F5 82            [12] 2581 	mov	dpl,a
      00844D C0 07            [24] 2582 	push	ar7
      00844F C0 06            [24] 2583 	push	ar6
      008451 C0 05            [24] 2584 	push	ar5
      008453 12 71 80         [24] 2585 	lcall	_register_code
      008456 D0 05            [24] 2586 	pop	ar5
      008458 D0 06            [24] 2587 	pop	ar6
      00845A D0 07            [24] 2588 	pop	ar7
      00845C 02 83 5E         [24] 2589 	ljmp	00166$
      00845F                       2590 00119$:
                                   2591 ;	quantum/dynamic_keymap.c:634: else unregister_code((uint8_t)data[2]);
      00845F 90 09 26         [24] 2592 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0002)
      008462 E0               [24] 2593 	movx	a,@dptr
      008463 F5 82            [12] 2594 	mov	dpl,a
      008465 C0 07            [24] 2595 	push	ar7
      008467 C0 06            [24] 2596 	push	ar6
      008469 C0 05            [24] 2597 	push	ar5
      00846B 12 72 60         [24] 2598 	lcall	_unregister_code
      00846E D0 05            [24] 2599 	pop	ar5
      008470 D0 06            [24] 2600 	pop	ar6
      008472 D0 07            [24] 2601 	pop	ar7
      008474 02 83 5E         [24] 2602 	ljmp	00166$
      008477                       2603 00152$:
                                   2604 ;	quantum/dynamic_keymap.c:641: } else if (data[1] == VIAL_MACRO_EXT_TAP || data[1] == VIAL_MACRO_EXT_DOWN || data[1] == VIAL_MACRO_EXT_UP) {
      008477 90 09 25         [24] 2605 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      00847A E0               [24] 2606 	movx	a,@dptr
      00847B FC               [12] 2607 	mov	r4,a
      00847C BC 05 02         [24] 2608 	cjne	r4,#0x05,00436$
      00847F 80 17            [24] 2609 	sjmp	00146$
      008481                       2610 00436$:
      008481 90 09 25         [24] 2611 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      008484 E0               [24] 2612 	movx	a,@dptr
      008485 FC               [12] 2613 	mov	r4,a
      008486 BC 06 02         [24] 2614 	cjne	r4,#0x06,00437$
      008489 80 0D            [24] 2615 	sjmp	00146$
      00848B                       2616 00437$:
      00848B 90 09 25         [24] 2617 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      00848E E0               [24] 2618 	movx	a,@dptr
      00848F FC               [12] 2619 	mov	r4,a
      008490 BC 07 02         [24] 2620 	cjne	r4,#0x07,00438$
      008493 80 03            [24] 2621 	sjmp	00439$
      008495                       2622 00438$:
      008495 02 85 52         [24] 2623 	ljmp	00147$
      008498                       2624 00439$:
      008498                       2625 00146$:
                                   2626 ;	quantum/dynamic_keymap.c:642: data[2] = eeprom_read_byte(p++);
      008498 90 09 21         [24] 2627 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      00849B E0               [24] 2628 	movx	a,@dptr
      00849C FA               [12] 2629 	mov	r2,a
      00849D A3               [24] 2630 	inc	dptr
      00849E E0               [24] 2631 	movx	a,@dptr
      00849F 12 85 EC         [24] 2632 	lcall	_ak820_outline_0003
      0084A2 12 43 FC         [24] 2633 	lcall	_eeprom_read_byte
      0084A5 AC 82            [24] 2634 	mov	r4, dpl
      0084A7 90 09 26         [24] 2635 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0002)
      0084AA EC               [12] 2636 	mov	a,r4
      0084AB F0               [24] 2637 	movx	@dptr,a
                                   2638 ;	quantum/dynamic_keymap.c:643: if (data[2] != 0) {
      0084AC EC               [12] 2639 	mov	a,r4
      0084AD 70 03            [24] 2640 	jnz	00440$
      0084AF 02 83 5E         [24] 2641 	ljmp	00166$
      0084B2                       2642 00440$:
                                   2643 ;	quantum/dynamic_keymap.c:644: data[3] = eeprom_read_byte(p++);
      0084B2 90 09 21         [24] 2644 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      0084B5 E0               [24] 2645 	movx	a,@dptr
      0084B6 FA               [12] 2646 	mov	r2,a
      0084B7 A3               [24] 2647 	inc	dptr
      0084B8 E0               [24] 2648 	movx	a,@dptr
      0084B9 12 85 EC         [24] 2649 	lcall	_ak820_outline_0003
      0084BC 12 43 FC         [24] 2650 	lcall	_eeprom_read_byte
      0084BF AC 82            [24] 2651 	mov	r4, dpl
      0084C1 90 09 27         [24] 2652 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0003)
      0084C4 EC               [12] 2653 	mov	a,r4
      0084C5 F0               [24] 2654 	movx	@dptr,a
                                   2655 ;	quantum/dynamic_keymap.c:645: if (data[3] != 0) {
      0084C6 EC               [12] 2656 	mov	a,r4
      0084C7 70 03            [24] 2657 	jnz	00441$
      0084C9 02 83 5E         [24] 2658 	ljmp	00166$
      0084CC                       2659 00441$:
                                   2660 ;	quantum/dynamic_keymap.c:648: kc = (uint8_t)data[2] | ((uint16_t)(uint8_t)data[3] << 8);
      0084CC 90 09 26         [24] 2661 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0002)
      0084CF E0               [24] 2662 	movx	a,@dptr
      0084D0 FC               [12] 2663 	mov	r4,a
      0084D1 90 09 27         [24] 2664 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0003)
      0084D4 E0               [24] 2665 	movx	a,@dptr
      0084D5 FA               [12] 2666 	mov	r2,a
      0084D6 7B 00            [12] 2667 	mov	r3,#0x00
      0084D8 8C 01            [24] 2668 	mov	ar1,r4
      0084DA 7C 00            [12] 2669 	mov	r4,#0x00
      0084DC E9               [12] 2670 	mov	a,r1
      0084DD 42 03            [12] 2671 	orl	ar3,a
      0084DF EC               [12] 2672 	mov	a,r4
      0084E0 42 02            [12] 2673 	orl	ar2,a
                                   2674 ;	quantum/dynamic_keymap.c:652: kc = decode_keycode(kc);
      0084E2 8B 82            [24] 2675 	mov	dpl, r3
      0084E4 8A 83            [24] 2676 	mov	dph, r2
      0084E6 C0 07            [24] 2677 	push	ar7
      0084E8 C0 06            [24] 2678 	push	ar6
      0084EA C0 05            [24] 2679 	push	ar5
      0084EC 12 82 97         [24] 2680 	lcall	_decode_keycode
      0084EF AB 82            [24] 2681 	mov	r3, dpl
      0084F1 AC 83            [24] 2682 	mov	r4, dph
      0084F3 D0 05            [24] 2683 	pop	ar5
      0084F5 D0 06            [24] 2684 	pop	ar6
      0084F7 D0 07            [24] 2685 	pop	ar7
                                   2686 ;	quantum/dynamic_keymap.c:653: switch (data[1]) {
      0084F9 90 09 25         [24] 2687 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      0084FC E0               [24] 2688 	movx	a,@dptr
      0084FD FA               [12] 2689 	mov	r2,a
      0084FE BA 05 02         [24] 2690 	cjne	r2,#0x05,00442$
      008501 80 0D            [24] 2691 	sjmp	00126$
      008503                       2692 00442$:
      008503 BA 06 02         [24] 2693 	cjne	r2,#0x06,00443$
      008506 80 1E            [24] 2694 	sjmp	00127$
      008508                       2695 00443$:
      008508 BA 07 02         [24] 2696 	cjne	r2,#0x07,00444$
      00850B 80 2F            [24] 2697 	sjmp	00128$
      00850D                       2698 00444$:
      00850D 02 83 5E         [24] 2699 	ljmp	00166$
                                   2700 ;	quantum/dynamic_keymap.c:654: case VIAL_MACRO_EXT_TAP:
      008510                       2701 00126$:
                                   2702 ;	quantum/dynamic_keymap.c:655: vial_keycode_tap(kc);
      008510 8B 82            [24] 2703 	mov	dpl, r3
      008512 8C 83            [24] 2704 	mov	dph, r4
      008514 C0 07            [24] 2705 	push	ar7
      008516 C0 06            [24] 2706 	push	ar6
      008518 C0 05            [24] 2707 	push	ar5
      00851A 12 AE 16         [24] 2708 	lcall	_vial_keycode_tap
      00851D D0 05            [24] 2709 	pop	ar5
      00851F D0 06            [24] 2710 	pop	ar6
      008521 D0 07            [24] 2711 	pop	ar7
                                   2712 ;	quantum/dynamic_keymap.c:656: break;
      008523 02 83 5E         [24] 2713 	ljmp	00166$
                                   2714 ;	quantum/dynamic_keymap.c:657: case VIAL_MACRO_EXT_DOWN:
      008526                       2715 00127$:
                                   2716 ;	quantum/dynamic_keymap.c:658: vial_keycode_down(kc);
      008526 8B 82            [24] 2717 	mov	dpl, r3
      008528 8C 83            [24] 2718 	mov	dph, r4
      00852A C0 07            [24] 2719 	push	ar7
      00852C C0 06            [24] 2720 	push	ar6
      00852E C0 05            [24] 2721 	push	ar5
      008530 12 AD 71         [24] 2722 	lcall	_vial_keycode_down
      008533 D0 05            [24] 2723 	pop	ar5
      008535 D0 06            [24] 2724 	pop	ar6
      008537 D0 07            [24] 2725 	pop	ar7
                                   2726 ;	quantum/dynamic_keymap.c:659: break;
      008539 02 83 5E         [24] 2727 	ljmp	00166$
                                   2728 ;	quantum/dynamic_keymap.c:660: case VIAL_MACRO_EXT_UP:
      00853C                       2729 00128$:
                                   2730 ;	quantum/dynamic_keymap.c:661: vial_keycode_up(kc);
      00853C 8B 82            [24] 2731 	mov	dpl, r3
      00853E 8C 83            [24] 2732 	mov	dph, r4
      008540 C0 07            [24] 2733 	push	ar7
      008542 C0 06            [24] 2734 	push	ar6
      008544 C0 05            [24] 2735 	push	ar5
      008546 12 AD C4         [24] 2736 	lcall	_vial_keycode_up
      008549 D0 05            [24] 2737 	pop	ar5
      00854B D0 06            [24] 2738 	pop	ar6
      00854D D0 07            [24] 2739 	pop	ar7
                                   2740 ;	quantum/dynamic_keymap.c:663: }
      00854F 02 83 5E         [24] 2741 	ljmp	00166$
      008552                       2742 00147$:
                                   2743 ;	quantum/dynamic_keymap.c:666: } else if (data[1] == SS_DELAY_CODE) {
      008552 90 09 25         [24] 2744 	mov	dptr,#(_dynamic_keymap_macro_send_data_10003_362 + 0x0001)
      008555 E0               [24] 2745 	movx	a,@dptr
      008556 FC               [12] 2746 	mov	r4,a
      008557 BC 04 02         [24] 2747 	cjne	r4,#0x04,00445$
      00855A 80 03            [24] 2748 	sjmp	00446$
      00855C                       2749 00445$:
      00855C 02 83 5E         [24] 2750 	ljmp	00166$
      00855F                       2751 00446$:
                                   2752 ;	quantum/dynamic_keymap.c:668: uint8_t d0 = eeprom_read_byte(p++);
      00855F 90 09 21         [24] 2753 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      008562 E0               [24] 2754 	movx	a,@dptr
      008563 FA               [12] 2755 	mov	r2,a
      008564 A3               [24] 2756 	inc	dptr
      008565 E0               [24] 2757 	movx	a,@dptr
      008566 12 85 EC         [24] 2758 	lcall	_ak820_outline_0003
      008569 12 43 FC         [24] 2759 	lcall	_eeprom_read_byte
      00856C AC 82            [24] 2760 	mov	r4, dpl
                                   2761 ;	quantum/dynamic_keymap.c:669: uint8_t d1 = eeprom_read_byte(p++);
      00856E 90 09 21         [24] 2762 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      008571 E0               [24] 2763 	movx	a,@dptr
      008572 F9               [12] 2764 	mov	r1,a
      008573 A3               [24] 2765 	inc	dptr
      008574 E0               [24] 2766 	movx	a,@dptr
      008575 FA               [12] 2767 	mov	r2,a
      008576 A3               [24] 2768 	inc	dptr
      008577 E0               [24] 2769 	movx	a,@dptr
      008578 FB               [12] 2770 	mov	r3,a
      008579 90 09 21         [24] 2771 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      00857C 74 01            [12] 2772 	mov	a,#0x01
      00857E 29               [12] 2773 	add	a, r1
      00857F F0               [24] 2774 	movx	@dptr,a
      008580 E4               [12] 2775 	clr	a
      008581 3A               [12] 2776 	addc	a, r2
      008582 A3               [24] 2777 	inc	dptr
      008583 F0               [24] 2778 	movx	@dptr,a
      008584 EB               [12] 2779 	mov	a,r3
      008585 A3               [24] 2780 	inc	dptr
      008586 F0               [24] 2781 	movx	@dptr,a
      008587 89 82            [24] 2782 	mov	dpl, r1
      008589 8A 83            [24] 2783 	mov	dph, r2
      00858B 8B F0            [24] 2784 	mov	b, r3
      00858D 12 43 FC         [24] 2785 	lcall	_eeprom_read_byte
      008590 AB 82            [24] 2786 	mov	r3, dpl
                                   2787 ;	quantum/dynamic_keymap.c:670: if (d0 == 0 || d1 == 0)
      008592 EC               [12] 2788 	mov	a,r4
      008593 60 51            [24] 2789 	jz	00168$
      008595 EB               [12] 2790 	mov	a,r3
      008596 60 4E            [24] 2791 	jz	00168$
                                   2792 ;	quantum/dynamic_keymap.c:673: uint16_t ms = (uint16_t)(d0 - 1) + (uint16_t)(d1 - 1) * 255u;
      008598 1C               [12] 2793 	dec	r4
      008599 1B               [12] 2794 	dec	r3
      00859A EB               [12] 2795 	mov	a,r3
      00859B 75 F0 FF         [24] 2796 	mov	b,#0xff
      00859E A4               [48] 2797 	mul	ab
      00859F FB               [12] 2798 	mov	r3,a
      0085A0 AA F0            [24] 2799 	mov	r2,b
      0085A2 8C 01            [24] 2800 	mov	ar1,r4
      0085A4 7C 00            [12] 2801 	mov	r4,#0x00
      0085A6 EB               [12] 2802 	mov	a,r3
      0085A7 29               [12] 2803 	add	a, r1
      0085A8 FB               [12] 2804 	mov	r3,a
      0085A9 EA               [12] 2805 	mov	a,r2
      0085AA 3C               [12] 2806 	addc	a, r4
      0085AB FA               [12] 2807 	mov	r2,a
                                   2808 ;	quantum/dynamic_keymap.c:674: while (ms--) wait_ms(1);
      0085AC                       2809 00141$:
      0085AC 8B 01            [24] 2810 	mov	ar1,r3
      0085AE 8A 04            [24] 2811 	mov	ar4,r2
      0085B0 1B               [12] 2812 	dec	r3
      0085B1 BB FF 01         [24] 2813 	cjne	r3,#0xff,00449$
      0085B4 1A               [12] 2814 	dec	r2
      0085B5                       2815 00449$:
      0085B5 E9               [12] 2816 	mov	a,r1
      0085B6 4C               [12] 2817 	orl	a,r4
      0085B7 70 03            [24] 2818 	jnz	00450$
      0085B9 02 83 5E         [24] 2819 	ljmp	00166$
      0085BC                       2820 00450$:
      0085BC 90 00 01         [24] 2821 	mov	dptr,#0x0001
      0085BF 12 52 5E         [24] 2822 	lcall	_mDelaymS
      0085C2 80 E8            [24] 2823 	sjmp	00141$
      0085C4                       2824 00164$:
                                   2825 ;	quantum/dynamic_keymap.c:680: if ((uint8_t)data[0] >= 128) break;
      0085C4 90 09 24         [24] 2826 	mov	dptr,#_dynamic_keymap_macro_send_data_10003_362
      0085C7 E0               [24] 2827 	movx	a,@dptr
      0085C8 FC               [12] 2828 	mov	r4,a
      0085C9 BC 80 00         [24] 2829 	cjne	r4,#0x80,00451$
      0085CC                       2830 00451$:
      0085CC 50 18            [24] 2831 	jnc	00168$
                                   2832 ;	quantum/dynamic_keymap.c:684: send_char(data[0]);
      0085CE 90 09 24         [24] 2833 	mov	dptr,#_dynamic_keymap_macro_send_data_10003_362
      0085D1 E0               [24] 2834 	movx	a,@dptr
      0085D2 F5 82            [12] 2835 	mov	dpl,a
      0085D4 C0 07            [24] 2836 	push	ar7
      0085D6 C0 06            [24] 2837 	push	ar6
      0085D8 C0 05            [24] 2838 	push	ar5
      0085DA 12 9F 73         [24] 2839 	lcall	_send_char
      0085DD D0 05            [24] 2840 	pop	ar5
      0085DF D0 06            [24] 2841 	pop	ar6
      0085E1 D0 07            [24] 2842 	pop	ar7
                                   2843 ;	quantum/dynamic_keymap.c:685: for (uint8_t delay = DYNAMIC_KEYMAP_MACRO_DELAY; delay; --delay) wait_ms(1);
      0085E3 02 83 5E         [24] 2844 	ljmp	00166$
      0085E6                       2845 00168$:
                                   2846 ;	quantum/dynamic_keymap.c:692: sending = false;
      0085E6 90 09 20         [24] 2847 	mov	dptr,#_dynamic_keymap_macro_send_sending_10000_350
      0085E9 E4               [12] 2848 	clr	a
      0085EA F0               [24] 2849 	movx	@dptr,a
                                   2850 ;	quantum/dynamic_keymap.c:694: }
      0085EB 22               [24] 2851 	ret
                                   2852 	.area CSEG    (CODE)
                                   2853 	.area CONST   (CODE)
                                   2854 	.area XINIT   (CODE)
                                   2855 	.area CABS    (ABS,CODE)
                                   2856 
                                   2857 ; Experimental exact instruction outlining.
                                   2858 	.globl _ak820_outline_0003
                                   2859 	.globl _ak820_outline_0012
                                   2860 
                                   2861 	.area CSEG (CODE)
                                   2862 ; function ak820_outline_0003
      0085EC                       2863 _ak820_outline_0003:
      0085EC FB               [12] 2864 	mov	r3,a
      0085ED A3               [24] 2865 	inc	dptr
      0085EE E0               [24] 2866 	movx	a,@dptr
      0085EF FC               [12] 2867 	mov	r4,a
      0085F0 90 09 21         [24] 2868 	mov	dptr,#_dynamic_keymap_macro_send_p_10001_355
      0085F3 74 01            [12] 2869 	mov	a,#0x01
      0085F5 2A               [12] 2870 	add	a,r2
      0085F6 F0               [24] 2871 	movx	@dptr,a
      0085F7 E4               [12] 2872 	clr	a
      0085F8 3B               [12] 2873 	addc	a,r3
      0085F9 A3               [24] 2874 	inc	dptr
      0085FA F0               [24] 2875 	movx	@dptr,a
      0085FB EC               [12] 2876 	mov	a,r4
      0085FC A3               [24] 2877 	inc	dptr
      0085FD F0               [24] 2878 	movx	@dptr,a
      0085FE 8A 82            [24] 2879 	mov	dpl,r2
      008600 8B 83            [24] 2880 	mov	dph,r3
      008602 8C F0            [24] 2881 	mov	b,r4
      008604 22               [24] 2882 	ret
                                   2883 
                                   2884 	.area CSEG (CODE)
                                   2885 ; function ak820_outline_0012
      008605                       2886 _ak820_outline_0012:
      008605 E0               [24] 2887 	movx	a,@dptr
      008606 FE               [12] 2888 	mov	r6,a
      008607 A3               [24] 2889 	inc	dptr
      008608 E0               [24] 2890 	movx	a,@dptr
      008609 FF               [12] 2891 	mov	r7,a
      00860A 8E 04            [24] 2892 	mov	ar4,r6
      00860C 8F 05            [24] 2893 	mov	ar5,r7
      00860E 22               [24] 2894 	ret
