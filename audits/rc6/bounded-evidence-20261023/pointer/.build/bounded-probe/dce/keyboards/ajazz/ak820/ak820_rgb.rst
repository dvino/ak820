                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module ak820_rgb
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _eeprom_update_block
                                     12 	.globl _eeprom_read_block
                                     13 	.globl _timer_elapsed
                                     14 	.globl _timer_read
                                     15 	.globl _hsv_to_rgb_into
                                     16 	.globl _memset
                                     17 	.globl _ADC_START
                                     18 	.globl _S0_R_FIFO
                                     19 	.globl _S0_T_FIFO
                                     20 	.globl _S0_FREE
                                     21 	.globl _S0_IF_BYTE
                                     22 	.globl _S0_IF_FIRST
                                     23 	.globl _S0_IF_OV
                                     24 	.globl _S0_FST_ACT
                                     25 	.globl _CP_RL2
                                     26 	.globl _C_T2
                                     27 	.globl _TR2
                                     28 	.globl _EXEN2
                                     29 	.globl _TCLK
                                     30 	.globl _RCLK
                                     31 	.globl _EXF2
                                     32 	.globl _CAP1F
                                     33 	.globl _TF2
                                     34 	.globl _RI
                                     35 	.globl _TI
                                     36 	.globl _RB8
                                     37 	.globl _TB8
                                     38 	.globl _REN
                                     39 	.globl _SM2
                                     40 	.globl _SM1
                                     41 	.globl _SM0
                                     42 	.globl _IT0
                                     43 	.globl _IE0
                                     44 	.globl _IT1
                                     45 	.globl _IE1
                                     46 	.globl _TR0
                                     47 	.globl _TF0
                                     48 	.globl _TR1
                                     49 	.globl _TF1
                                     50 	.globl _P4_0
                                     51 	.globl _P4_1
                                     52 	.globl _P4_2
                                     53 	.globl _P4_3
                                     54 	.globl _P4_4
                                     55 	.globl _P4_5
                                     56 	.globl _P4_6
                                     57 	.globl _RXD
                                     58 	.globl _TXD
                                     59 	.globl _INT0
                                     60 	.globl _INT1
                                     61 	.globl _T0
                                     62 	.globl _T1
                                     63 	.globl _MOSI1
                                     64 	.globl _MISO1
                                     65 	.globl _SCK1
                                     66 	.globl _P3_0
                                     67 	.globl _P3_1
                                     68 	.globl _P3_2
                                     69 	.globl _P3_3
                                     70 	.globl _P3_4
                                     71 	.globl _P3_5
                                     72 	.globl _P3_6
                                     73 	.globl _P3_7
                                     74 	.globl _CAP1_
                                     75 	.globl _T2_
                                     76 	.globl _CAP2_
                                     77 	.globl _T2EX_
                                     78 	.globl _RXD1
                                     79 	.globl _TXD1
                                     80 	.globl _P2_0
                                     81 	.globl _P2_1
                                     82 	.globl _P2_2
                                     83 	.globl _P2_3
                                     84 	.globl _P2_4
                                     85 	.globl _P2_5
                                     86 	.globl _P2_6
                                     87 	.globl _P2_7
                                     88 	.globl _AIN0
                                     89 	.globl _AIN1
                                     90 	.globl _AIN2
                                     91 	.globl _AIN3
                                     92 	.globl _AIN4
                                     93 	.globl _AIN5
                                     94 	.globl _AIN6
                                     95 	.globl _AIN7
                                     96 	.globl _CAP1
                                     97 	.globl _T2
                                     98 	.globl _CAP2
                                     99 	.globl _T2EX
                                    100 	.globl _INT0_
                                    101 	.globl _SCS
                                    102 	.globl _MOSI
                                    103 	.globl _MISO
                                    104 	.globl _SCK
                                    105 	.globl _RXD1_
                                    106 	.globl _TXD1_
                                    107 	.globl _P1_0
                                    108 	.globl _P1_1
                                    109 	.globl _P1_2
                                    110 	.globl _P1_3
                                    111 	.globl _P1_4
                                    112 	.globl _P1_5
                                    113 	.globl _P1_6
                                    114 	.globl _P1_7
                                    115 	.globl _AIN8
                                    116 	.globl _AIN9
                                    117 	.globl _AIN10
                                    118 	.globl _AIN11
                                    119 	.globl _AIN12
                                    120 	.globl _AIN13
                                    121 	.globl _RXD_
                                    122 	.globl _TXD_
                                    123 	.globl _SCL0
                                    124 	.globl _SDA0
                                    125 	.globl _P0_0
                                    126 	.globl _P0_1
                                    127 	.globl _P0_2
                                    128 	.globl _P0_3
                                    129 	.globl _P0_4
                                    130 	.globl _P0_5
                                    131 	.globl _P0_6
                                    132 	.globl _P0_7
                                    133 	.globl _IE_SPI0
                                    134 	.globl _IE_USB
                                    135 	.globl _IE_ADC
                                    136 	.globl _IE_UART1
                                    137 	.globl _IE_PWM_I2C
                                    138 	.globl _IE_GPIO
                                    139 	.globl _IE_WDOG
                                    140 	.globl _PX0
                                    141 	.globl _PT0
                                    142 	.globl _PX1
                                    143 	.globl _PT1
                                    144 	.globl _PS
                                    145 	.globl _PT2
                                    146 	.globl _PL_FLAG
                                    147 	.globl _PH_FLAG
                                    148 	.globl _EX0
                                    149 	.globl _ET0
                                    150 	.globl _EX1
                                    151 	.globl _ET1
                                    152 	.globl _ES
                                    153 	.globl _ET2
                                    154 	.globl _E_DIS
                                    155 	.globl _EA
                                    156 	.globl _P
                                    157 	.globl _F1
                                    158 	.globl _OV
                                    159 	.globl _RS0
                                    160 	.globl _RS1
                                    161 	.globl _F0
                                    162 	.globl _AC
                                    163 	.globl _CY
                                    164 	.globl _I2CS_INT_ST
                                    165 	.globl _I2CX_INT
                                    166 	.globl _LED_STATUS
                                    167 	.globl _LED_DMA_H
                                    168 	.globl _LED_DMA_L
                                    169 	.globl _LED_DMA
                                    170 	.globl _LED_PWM_OE
                                    171 	.globl _LED_COMMON
                                    172 	.globl _ADC_CHAN
                                    173 	.globl _ADC_DAT_H
                                    174 	.globl _ADC_DAT_L
                                    175 	.globl _ADC_DAT
                                    176 	.globl _ADC_CTRL
                                    177 	.globl _SPI1_CK_SE
                                    178 	.globl _SPI1_CTRL
                                    179 	.globl _SPI1_DATA
                                    180 	.globl _SPI1_STAT
                                    181 	.globl _SIF1
                                    182 	.globl _SBAUD1
                                    183 	.globl _SBUF1
                                    184 	.globl _SCON1
                                    185 	.globl _SPI0_SETUP
                                    186 	.globl _SPI0_CK_SE
                                    187 	.globl _SPI0_CTRL
                                    188 	.globl _SPI0_DATA
                                    189 	.globl _SPI0_STAT
                                    190 	.globl _T2CAP1H
                                    191 	.globl _T2CAP1L
                                    192 	.globl _T2CAP1
                                    193 	.globl _TH2
                                    194 	.globl _TL2
                                    195 	.globl _T2COUNT
                                    196 	.globl _RCAP2H
                                    197 	.globl _RCAP2L
                                    198 	.globl _RCAP2
                                    199 	.globl _T2MOD
                                    200 	.globl _T2CON
                                    201 	.globl _SBUF
                                    202 	.globl _SCON
                                    203 	.globl _TH1
                                    204 	.globl _TH0
                                    205 	.globl _TL1
                                    206 	.globl _TL0
                                    207 	.globl _TMOD
                                    208 	.globl _TCON
                                    209 	.globl _XBUS_AUX
                                    210 	.globl _P7
                                    211 	.globl _P6_DIR
                                    212 	.globl _P6_OUT_PU
                                    213 	.globl _P6_IN
                                    214 	.globl _P5_DIR
                                    215 	.globl _P5_OUT_PU
                                    216 	.globl _P5_IN
                                    217 	.globl _P4_LED_KEY
                                    218 	.globl _P4_DIR_PU
                                    219 	.globl _P4_MOD_OC
                                    220 	.globl _P4
                                    221 	.globl _P3_DIR_PU
                                    222 	.globl _P3_MOD_OC
                                    223 	.globl _P3
                                    224 	.globl _P2_DIR_PU
                                    225 	.globl _P2_MOD_OC
                                    226 	.globl _P2
                                    227 	.globl _P1_DIR_PU
                                    228 	.globl _P1_MOD_OC
                                    229 	.globl _P1
                                    230 	.globl _P0_DIR_PU
                                    231 	.globl _P0_MOD_OC
                                    232 	.globl _P0
                                    233 	.globl _ROM_CTRL
                                    234 	.globl _ROM_DATA_HH
                                    235 	.globl _ROM_DATA_HL
                                    236 	.globl _ROM_DATA_HI
                                    237 	.globl _ROM_ADDR_H
                                    238 	.globl _ROM_ADDR_L
                                    239 	.globl _ROM_ADDR
                                    240 	.globl _GPIO_IE
                                    241 	.globl _IP_EX
                                    242 	.globl _IE_EX
                                    243 	.globl _IP
                                    244 	.globl _IE
                                    245 	.globl _WDOG_COUNT
                                    246 	.globl _RESET_KEEP
                                    247 	.globl _WAKE_CTRL
                                    248 	.globl _CLOCK_CFG
                                    249 	.globl _POWER_CFG
                                    250 	.globl _PCON
                                    251 	.globl _GLOBAL_CFG
                                    252 	.globl _SAFE_MOD
                                    253 	.globl _DPH
                                    254 	.globl _DPL
                                    255 	.globl _SP
                                    256 	.globl _A_INV
                                    257 	.globl _B
                                    258 	.globl _ACC
                                    259 	.globl _PSW
                                    260 	.globl _rgb_matrix_sethsv_noeeprom_PARM_3
                                    261 	.globl _rgb_matrix_sethsv_noeeprom_PARM_2
                                    262 	.globl _process_rgb_matrix_PARM_3
                                    263 	.globl _process_rgb_matrix_PARM_2
                                    264 	.globl _rgb_matrix_set_color_all_PARM_3
                                    265 	.globl _rgb_matrix_set_color_all_PARM_2
                                    266 	.globl _rgb_matrix_set_color_PARM_4
                                    267 	.globl _rgb_matrix_set_color_PARM_3
                                    268 	.globl _rgb_matrix_set_color_PARM_2
                                    269 	.globl _rgb_matrix_config
                                    270 	.globl _eeconfig_update_rgb_matrix
                                    271 	.globl _eeconfig_update_rgb_matrix_default
                                    272 	.globl _rgb_matrix_reload_from_eeprom
                                    273 	.globl _rgb_matrix_init
                                    274 	.globl _rgb_matrix_set_color
                                    275 	.globl _rgb_matrix_set_color_all
                                    276 	.globl _rgb_matrix_task
                                    277 	.globl _process_rgb_matrix
                                    278 	.globl _rgb_matrix_set_suspend_state
                                    279 	.globl _rgb_matrix_is_enabled
                                    280 	.globl _rgb_matrix_get_mode
                                    281 	.globl _rgb_matrix_get_hue
                                    282 	.globl _rgb_matrix_get_sat
                                    283 	.globl _rgb_matrix_get_val
                                    284 	.globl _rgb_matrix_get_speed
                                    285 	.globl _rgb_matrix_toggle_noeeprom
                                    286 	.globl _rgb_matrix_enable_noeeprom
                                    287 	.globl _rgb_matrix_disable_noeeprom
                                    288 	.globl _rgb_matrix_mode_noeeprom
                                    289 	.globl _rgb_matrix_step_noeeprom
                                    290 	.globl _rgb_matrix_step_reverse_noeeprom
                                    291 	.globl _rgb_matrix_sethsv_noeeprom
                                    292 	.globl _rgb_matrix_set_speed_noeeprom
                                    293 	.globl _rgb_matrix_increase_hue_noeeprom
                                    294 	.globl _rgb_matrix_decrease_hue_noeeprom
                                    295 	.globl _rgb_matrix_increase_sat_noeeprom
                                    296 	.globl _rgb_matrix_decrease_sat_noeeprom
                                    297 	.globl _rgb_matrix_increase_val_noeeprom
                                    298 	.globl _rgb_matrix_decrease_val_noeeprom
                                    299 	.globl _rgb_matrix_increase_speed_noeeprom
                                    300 	.globl _rgb_matrix_decrease_speed_noeeprom
                                    301 	.globl _rgb_matrix_toggle
                                    302 	.globl _rgb_matrix_step
                                    303 	.globl _rgb_matrix_step_reverse
                                    304 	.globl _rgb_matrix_increase_hue
                                    305 	.globl _rgb_matrix_decrease_hue
                                    306 	.globl _rgb_matrix_increase_sat
                                    307 	.globl _rgb_matrix_decrease_sat
                                    308 	.globl _rgb_matrix_increase_val
                                    309 	.globl _rgb_matrix_decrease_val
                                    310 	.globl _rgb_matrix_increase_speed
                                    311 	.globl _rgb_matrix_decrease_speed
                                    312 	.globl _rgb_matrix_mode
                                    313 ;--------------------------------------------------------
                                    314 ; special function registers
                                    315 ;--------------------------------------------------------
                                    316 	.area RSEG    (ABS,DATA)
      000000                        317 	.org 0x0000
                           0000D0   318 _PSW	=	0x00d0
                           0000E0   319 _ACC	=	0x00e0
                           0000F0   320 _B	=	0x00f0
                           0000FD   321 _A_INV	=	0x00fd
                           000081   322 _SP	=	0x0081
                           000082   323 _DPL	=	0x0082
                           000083   324 _DPH	=	0x0083
                           0000A1   325 _SAFE_MOD	=	0x00a1
                           0000B1   326 _GLOBAL_CFG	=	0x00b1
                           000087   327 _PCON	=	0x0087
                           0000BA   328 _POWER_CFG	=	0x00ba
                           0000B9   329 _CLOCK_CFG	=	0x00b9
                           0000A9   330 _WAKE_CTRL	=	0x00a9
                           0000FE   331 _RESET_KEEP	=	0x00fe
                           0000FF   332 _WDOG_COUNT	=	0x00ff
                           0000A8   333 _IE	=	0x00a8
                           0000B8   334 _IP	=	0x00b8
                           0000E8   335 _IE_EX	=	0x00e8
                           0000E9   336 _IP_EX	=	0x00e9
                           0000B2   337 _GPIO_IE	=	0x00b2
                           008584   338 _ROM_ADDR	=	0x8584
                           000084   339 _ROM_ADDR_L	=	0x0084
                           000085   340 _ROM_ADDR_H	=	0x0085
                           008F8E   341 _ROM_DATA_HI	=	0x8f8e
                           00008E   342 _ROM_DATA_HL	=	0x008e
                           00008F   343 _ROM_DATA_HH	=	0x008f
                           000086   344 _ROM_CTRL	=	0x0086
                           000080   345 _P0	=	0x0080
                           0000C4   346 _P0_MOD_OC	=	0x00c4
                           0000C5   347 _P0_DIR_PU	=	0x00c5
                           000090   348 _P1	=	0x0090
                           000092   349 _P1_MOD_OC	=	0x0092
                           000093   350 _P1_DIR_PU	=	0x0093
                           0000A0   351 _P2	=	0x00a0
                           000094   352 _P2_MOD_OC	=	0x0094
                           000095   353 _P2_DIR_PU	=	0x0095
                           0000B0   354 _P3	=	0x00b0
                           000096   355 _P3_MOD_OC	=	0x0096
                           000097   356 _P3_DIR_PU	=	0x0097
                           0000C0   357 _P4	=	0x00c0
                           0000C2   358 _P4_MOD_OC	=	0x00c2
                           0000C3   359 _P4_DIR_PU	=	0x00c3
                           0000C1   360 _P4_LED_KEY	=	0x00c1
                           0000AA   361 _P5_IN	=	0x00aa
                           0000AB   362 _P5_OUT_PU	=	0x00ab
                           0000AC   363 _P5_DIR	=	0x00ac
                           0000AD   364 _P6_IN	=	0x00ad
                           0000AE   365 _P6_OUT_PU	=	0x00ae
                           0000AF   366 _P6_DIR	=	0x00af
                           0000F1   367 _P7	=	0x00f1
                           0000A2   368 _XBUS_AUX	=	0x00a2
                           000088   369 _TCON	=	0x0088
                           000089   370 _TMOD	=	0x0089
                           00008A   371 _TL0	=	0x008a
                           00008B   372 _TL1	=	0x008b
                           00008C   373 _TH0	=	0x008c
                           00008D   374 _TH1	=	0x008d
                           000098   375 _SCON	=	0x0098
                           000099   376 _SBUF	=	0x0099
                           0000C8   377 _T2CON	=	0x00c8
                           0000C9   378 _T2MOD	=	0x00c9
                           00CBCA   379 _RCAP2	=	0xcbca
                           0000CA   380 _RCAP2L	=	0x00ca
                           0000CB   381 _RCAP2H	=	0x00cb
                           00CDCC   382 _T2COUNT	=	0xcdcc
                           0000CC   383 _TL2	=	0x00cc
                           0000CD   384 _TH2	=	0x00cd
                           00CFCE   385 _T2CAP1	=	0xcfce
                           0000CE   386 _T2CAP1L	=	0x00ce
                           0000CF   387 _T2CAP1H	=	0x00cf
                           0000F8   388 _SPI0_STAT	=	0x00f8
                           0000F9   389 _SPI0_DATA	=	0x00f9
                           0000FA   390 _SPI0_CTRL	=	0x00fa
                           0000FB   391 _SPI0_CK_SE	=	0x00fb
                           0000FC   392 _SPI0_SETUP	=	0x00fc
                           0000BC   393 _SCON1	=	0x00bc
                           0000BD   394 _SBUF1	=	0x00bd
                           0000BE   395 _SBAUD1	=	0x00be
                           0000BF   396 _SIF1	=	0x00bf
                           0000B4   397 _SPI1_STAT	=	0x00b4
                           0000B5   398 _SPI1_DATA	=	0x00b5
                           0000B6   399 _SPI1_CTRL	=	0x00b6
                           0000B7   400 _SPI1_CK_SE	=	0x00b7
                           0000F3   401 _ADC_CTRL	=	0x00f3
                           00F5F4   402 _ADC_DAT	=	0xf5f4
                           0000F4   403 _ADC_DAT_L	=	0x00f4
                           0000F5   404 _ADC_DAT_H	=	0x00f5
                           0000F6   405 _ADC_CHAN	=	0x00f6
                           0000A6   406 _LED_COMMON	=	0x00a6
                           0000A7   407 _LED_PWM_OE	=	0x00a7
                           00C7C6   408 _LED_DMA	=	0xc7c6
                           0000C6   409 _LED_DMA_L	=	0x00c6
                           0000C7   410 _LED_DMA_H	=	0x00c7
                           0000F7   411 _LED_STATUS	=	0x00f7
                           0000B3   412 _I2CX_INT	=	0x00b3
                           0000BB   413 _I2CS_INT_ST	=	0x00bb
                                    414 ;--------------------------------------------------------
                                    415 ; special function bits
                                    416 ;--------------------------------------------------------
                                    417 	.area RSEG    (ABS,DATA)
      000000                        418 	.org 0x0000
                           0000D7   419 _CY	=	0x00d7
                           0000D6   420 _AC	=	0x00d6
                           0000D5   421 _F0	=	0x00d5
                           0000D4   422 _RS1	=	0x00d4
                           0000D3   423 _RS0	=	0x00d3
                           0000D2   424 _OV	=	0x00d2
                           0000D1   425 _F1	=	0x00d1
                           0000D0   426 _P	=	0x00d0
                           0000AF   427 _EA	=	0x00af
                           0000AE   428 _E_DIS	=	0x00ae
                           0000AD   429 _ET2	=	0x00ad
                           0000AC   430 _ES	=	0x00ac
                           0000AB   431 _ET1	=	0x00ab
                           0000AA   432 _EX1	=	0x00aa
                           0000A9   433 _ET0	=	0x00a9
                           0000A8   434 _EX0	=	0x00a8
                           0000BF   435 _PH_FLAG	=	0x00bf
                           0000BE   436 _PL_FLAG	=	0x00be
                           0000BD   437 _PT2	=	0x00bd
                           0000BC   438 _PS	=	0x00bc
                           0000BB   439 _PT1	=	0x00bb
                           0000BA   440 _PX1	=	0x00ba
                           0000B9   441 _PT0	=	0x00b9
                           0000B8   442 _PX0	=	0x00b8
                           0000EF   443 _IE_WDOG	=	0x00ef
                           0000EE   444 _IE_GPIO	=	0x00ee
                           0000ED   445 _IE_PWM_I2C	=	0x00ed
                           0000EC   446 _IE_UART1	=	0x00ec
                           0000EB   447 _IE_ADC	=	0x00eb
                           0000E9   448 _IE_USB	=	0x00e9
                           0000E8   449 _IE_SPI0	=	0x00e8
                           000087   450 _P0_7	=	0x0087
                           000086   451 _P0_6	=	0x0086
                           000085   452 _P0_5	=	0x0085
                           000084   453 _P0_4	=	0x0084
                           000083   454 _P0_3	=	0x0083
                           000082   455 _P0_2	=	0x0082
                           000081   456 _P0_1	=	0x0081
                           000080   457 _P0_0	=	0x0080
                           000081   458 _SDA0	=	0x0081
                           000080   459 _SCL0	=	0x0080
                           000083   460 _TXD_	=	0x0083
                           000082   461 _RXD_	=	0x0082
                           000085   462 _AIN13	=	0x0085
                           000084   463 _AIN12	=	0x0084
                           000083   464 _AIN11	=	0x0083
                           000082   465 _AIN10	=	0x0082
                           000081   466 _AIN9	=	0x0081
                           000080   467 _AIN8	=	0x0080
                           000097   468 _P1_7	=	0x0097
                           000096   469 _P1_6	=	0x0096
                           000095   470 _P1_5	=	0x0095
                           000094   471 _P1_4	=	0x0094
                           000093   472 _P1_3	=	0x0093
                           000092   473 _P1_2	=	0x0092
                           000091   474 _P1_1	=	0x0091
                           000090   475 _P1_0	=	0x0090
                           000097   476 _TXD1_	=	0x0097
                           000096   477 _RXD1_	=	0x0096
                           000097   478 _SCK	=	0x0097
                           000096   479 _MISO	=	0x0096
                           000095   480 _MOSI	=	0x0095
                           000094   481 _SCS	=	0x0094
                           000092   482 _INT0_	=	0x0092
                           000091   483 _T2EX	=	0x0091
                           000091   484 _CAP2	=	0x0091
                           000090   485 _T2	=	0x0090
                           000090   486 _CAP1	=	0x0090
                           000097   487 _AIN7	=	0x0097
                           000096   488 _AIN6	=	0x0096
                           000095   489 _AIN5	=	0x0095
                           000094   490 _AIN4	=	0x0094
                           000093   491 _AIN3	=	0x0093
                           000092   492 _AIN2	=	0x0092
                           000091   493 _AIN1	=	0x0091
                           000090   494 _AIN0	=	0x0090
                           0000A7   495 _P2_7	=	0x00a7
                           0000A6   496 _P2_6	=	0x00a6
                           0000A5   497 _P2_5	=	0x00a5
                           0000A4   498 _P2_4	=	0x00a4
                           0000A3   499 _P2_3	=	0x00a3
                           0000A2   500 _P2_2	=	0x00a2
                           0000A1   501 _P2_1	=	0x00a1
                           0000A0   502 _P2_0	=	0x00a0
                           0000A7   503 _TXD1	=	0x00a7
                           0000A6   504 _RXD1	=	0x00a6
                           0000A5   505 _T2EX_	=	0x00a5
                           0000A5   506 _CAP2_	=	0x00a5
                           0000A4   507 _T2_	=	0x00a4
                           0000A4   508 _CAP1_	=	0x00a4
                           0000B7   509 _P3_7	=	0x00b7
                           0000B6   510 _P3_6	=	0x00b6
                           0000B5   511 _P3_5	=	0x00b5
                           0000B4   512 _P3_4	=	0x00b4
                           0000B3   513 _P3_3	=	0x00b3
                           0000B2   514 _P3_2	=	0x00b2
                           0000B1   515 _P3_1	=	0x00b1
                           0000B0   516 _P3_0	=	0x00b0
                           0000B7   517 _SCK1	=	0x00b7
                           0000B6   518 _MISO1	=	0x00b6
                           0000B5   519 _MOSI1	=	0x00b5
                           0000B5   520 _T1	=	0x00b5
                           0000B4   521 _T0	=	0x00b4
                           0000B3   522 _INT1	=	0x00b3
                           0000B2   523 _INT0	=	0x00b2
                           0000B1   524 _TXD	=	0x00b1
                           0000B0   525 _RXD	=	0x00b0
                           0000C6   526 _P4_6	=	0x00c6
                           0000C5   527 _P4_5	=	0x00c5
                           0000C4   528 _P4_4	=	0x00c4
                           0000C3   529 _P4_3	=	0x00c3
                           0000C2   530 _P4_2	=	0x00c2
                           0000C1   531 _P4_1	=	0x00c1
                           0000C0   532 _P4_0	=	0x00c0
                           00008F   533 _TF1	=	0x008f
                           00008E   534 _TR1	=	0x008e
                           00008D   535 _TF0	=	0x008d
                           00008C   536 _TR0	=	0x008c
                           00008B   537 _IE1	=	0x008b
                           00008A   538 _IT1	=	0x008a
                           000089   539 _IE0	=	0x0089
                           000088   540 _IT0	=	0x0088
                           00009F   541 _SM0	=	0x009f
                           00009E   542 _SM1	=	0x009e
                           00009D   543 _SM2	=	0x009d
                           00009C   544 _REN	=	0x009c
                           00009B   545 _TB8	=	0x009b
                           00009A   546 _RB8	=	0x009a
                           000099   547 _TI	=	0x0099
                           000098   548 _RI	=	0x0098
                           0000CF   549 _TF2	=	0x00cf
                           0000CF   550 _CAP1F	=	0x00cf
                           0000CE   551 _EXF2	=	0x00ce
                           0000CD   552 _RCLK	=	0x00cd
                           0000CC   553 _TCLK	=	0x00cc
                           0000CB   554 _EXEN2	=	0x00cb
                           0000CA   555 _TR2	=	0x00ca
                           0000C9   556 _C_T2	=	0x00c9
                           0000C8   557 _CP_RL2	=	0x00c8
                           0000FF   558 _S0_FST_ACT	=	0x00ff
                           0000FE   559 _S0_IF_OV	=	0x00fe
                           0000FD   560 _S0_IF_FIRST	=	0x00fd
                           0000FC   561 _S0_IF_BYTE	=	0x00fc
                           0000FB   562 _S0_FREE	=	0x00fb
                           0000FA   563 _S0_T_FIFO	=	0x00fa
                           0000F8   564 _S0_R_FIFO	=	0x00f8
                           0000F7   565 _ADC_START	=	0x00f7
                                    566 ;--------------------------------------------------------
                                    567 ; overlayable register banks
                                    568 ;--------------------------------------------------------
                                    569 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        570 	.ds 8
                                    571 ;--------------------------------------------------------
                                    572 ; internal ram data
                                    573 ;--------------------------------------------------------
                                    574 	.area DSEG    (DATA)
                                    575 ;--------------------------------------------------------
                                    576 ; overlayable items in internal ram
                                    577 ;--------------------------------------------------------
                                    578 ;--------------------------------------------------------
                                    579 ; indirectly addressable internal ram data
                                    580 ;--------------------------------------------------------
                                    581 	.area ISEG    (DATA)
                                    582 ;--------------------------------------------------------
                                    583 ; absolute internal ram data
                                    584 ;--------------------------------------------------------
                                    585 	.area IABS    (ABS,DATA)
                                    586 	.area IABS    (ABS,DATA)
                                    587 ;--------------------------------------------------------
                                    588 ; bit data
                                    589 ;--------------------------------------------------------
                                    590 	.area BSEG    (BIT)
      000007                        591 _rgb_matrix_task_sloc0_1_0:
      000007                        592 	.ds 1
                                    593 ;--------------------------------------------------------
                                    594 ; paged external ram data
                                    595 ;--------------------------------------------------------
                                    596 	.area PSEG    (PAG,XDATA)
                                    597 ;--------------------------------------------------------
                                    598 ; uninitialized external ram data
                                    599 ;--------------------------------------------------------
                                    600 	.area XSEG    (XDATA)
      0005C8                        601 _rgb_matrix_config::
      0005C8                        602 	.ds 8
      0005D0                        603 _suspended:
      0005D0                        604 	.ds 1
      0005D1                        605 _dirty:
      0005D1                        606 	.ds 1
      0005D2                        607 _rendering:
      0005D2                        608 	.ds 1
      0005D3                        609 _changed_at:
      0005D3                        610 	.ds 2
      0005D5                        611 _frame_at:
      0005D5                        612 	.ds 2
      0005D7                        613 _phase:
      0005D7                        614 	.ds 2
      0005D9                        615 _led_index:
      0005D9                        616 	.ds 1
      0005DA                        617 _frame_mode:
      0005DA                        618 	.ds 1
      0005DB                        619 _frame_hue:
      0005DB                        620 	.ds 1
      0005DC                        621 _frame_sat:
      0005DC                        622 	.ds 1
      0005DD                        623 _frame_val:
      0005DD                        624 	.ds 1
      0005DE                        625 _frame_flags:
      0005DE                        626 	.ds 1
      0005DF                        627 _frame_phase:
      0005DF                        628 	.ds 1
      0005E0                        629 _reactive_age:
      0005E0                        630 	.ds 82
      000632                        631 _reactive_at:
      000632                        632 	.ds 2
      000634                        633 _add_sat_PARM_2:
      000634                        634 	.ds 1
      000635                        635 _add_sat_x_10000_250:
      000635                        636 	.ds 1
      000636                        637 _sub_sat_PARM_2:
      000636                        638 	.ds 1
      000637                        639 _sub_sat_x_10000_252:
      000637                        640 	.ds 1
      000638                        641 _rgb_matrix_set_color_PARM_2:
      000638                        642 	.ds 1
      000639                        643 _rgb_matrix_set_color_PARM_3:
      000639                        644 	.ds 1
      00063A                        645 _rgb_matrix_set_color_PARM_4:
      00063A                        646 	.ds 1
      00063B                        647 _rgb_matrix_set_color_index_10000_268:
      00063B                        648 	.ds 2
      00063D                        649 _rgb_matrix_set_color_all_PARM_2:
      00063D                        650 	.ds 1
      00063E                        651 _rgb_matrix_set_color_all_PARM_3:
      00063E                        652 	.ds 1
      00063F                        653 _rgb_matrix_set_color_all_r_10000_271:
      00063F                        654 	.ds 1
      000640                        655 _sine8_theta_10000_273:
      000640                        656 	.ds 1
      000641                        657 _sine8_offset_10000_274:
      000641                        658 	.ds 1
      000642                        659 _sine8_fraction_10000_274:
      000642                        660 	.ds 1
      000643                        661 _breathing_cie_value_10000_277:
      000643                        662 	.ds 1
      000644                        663 _rgb_matrix_task_end_10000_282:
      000644                        664 	.ds 1
      000645                        665 _rgb_matrix_task_hsv_10000_282:
      000645                        666 	.ds 3
      000648                        667 _rgb_matrix_task_rgb_10000_282:
      000648                        668 	.ds 3
      00064B                        669 _process_rgb_matrix_PARM_2:
      00064B                        670 	.ds 1
      00064C                        671 _process_rgb_matrix_PARM_3:
      00064C                        672 	.ds 1
      00064D                        673 _process_rgb_matrix_row_10000_302:
      00064D                        674 	.ds 1
      00064E                        675 _rgb_matrix_set_suspend_state_state_10000_309:
      00064E                        676 	.ds 1
      00064F                        677 _rgb_matrix_mode_noeeprom_mode_10000_338:
      00064F                        678 	.ds 1
      000650                        679 _rgb_matrix_sethsv_noeeprom_PARM_2:
      000650                        680 	.ds 1
      000651                        681 _rgb_matrix_sethsv_noeeprom_PARM_3:
      000651                        682 	.ds 1
      000652                        683 _rgb_matrix_sethsv_noeeprom_hue_10000_346:
      000652                        684 	.ds 2
      000654                        685 _rgb_matrix_set_speed_noeeprom_speed_10000_348:
      000654                        686 	.ds 1
      000655                        687 _rgb_matrix_mode_mode_10000_394:
      000655                        688 	.ds 1
                                    689 ;--------------------------------------------------------
                                    690 ; absolute external ram data
                                    691 ;--------------------------------------------------------
                                    692 	.area XABS    (ABS,XDATA)
                                    693 ;--------------------------------------------------------
                                    694 ; initialized external ram data
                                    695 ;--------------------------------------------------------
                                    696 	.area XISEG   (XDATA)
                                    697 	.area HOME    (CODE)
                                    698 	.area GSINIT0 (CODE)
                                    699 	.area GSINIT1 (CODE)
                                    700 	.area GSINIT2 (CODE)
                                    701 	.area GSINIT3 (CODE)
                                    702 	.area GSINIT4 (CODE)
                                    703 	.area GSINIT5 (CODE)
                                    704 	.area GSINIT  (CODE)
                                    705 	.area GSFINAL (CODE)
                                    706 	.area CSEG    (CODE)
                                    707 ;--------------------------------------------------------
                                    708 ; global & static initialisations
                                    709 ;--------------------------------------------------------
                                    710 	.area HOME    (CODE)
                                    711 	.area GSINIT  (CODE)
                                    712 	.area GSFINAL (CODE)
                                    713 	.area GSINIT  (CODE)
                                    714 ;--------------------------------------------------------
                                    715 ; Home
                                    716 ;--------------------------------------------------------
                                    717 	.area HOME    (CODE)
                                    718 	.area HOME    (CODE)
                                    719 ;--------------------------------------------------------
                                    720 ; code
                                    721 ;--------------------------------------------------------
                                    722 	.area CSEG    (CODE)
                                    723 ;------------------------------------------------------------
                                    724 ;Allocation info for local variables in function 'rgb_matrix_check_finished_leds'
                                    725 ;------------------------------------------------------------
                                    726 ;led_idx       Allocated with name '_rgb_matrix_check_finished_leds_led_idx_10000_166'
                                    727 ;------------------------------------------------------------
                                    728 ;	quantum/rgb_matrix/rgb_matrix.h:260: static inline bool rgb_matrix_check_finished_leds(uint8_t led_idx) {
                                    729 ;	-----------------------------------------
                           000007   730 	ar7 = 0x07
                           000006   731 	ar6 = 0x06
                           000005   732 	ar5 = 0x05
                           000004   733 	ar4 = 0x04
                           000003   734 	ar3 = 0x03
                           000002   735 	ar2 = 0x02
                           000001   736 	ar1 = 0x01
                           000000   737 	ar0 = 0x00
                                    738 ;	 function clear_reactive
                                    739 ;	-----------------------------------------
      004799                        740 _clear_reactive:
                                    741 ;	keyboards/ajazz/ak820/ak820_rgb.c:38: memset(reactive_age, 0, sizeof(reactive_age));
      004799 90 0B 97         [24]  742 	mov	dptr,#_memset_PARM_2
      00479C E4               [12]  743 	clr	a
      00479D F0               [24]  744 	movx	@dptr,a
      00479E 90 0B 98         [24]  745 	mov	dptr,#_memset_PARM_3
      0047A1 74 52            [12]  746 	mov	a,#0x52
      0047A3 F0               [24]  747 	movx	@dptr,a
      0047A4 E4               [12]  748 	clr	a
      0047A5 A3               [24]  749 	inc	dptr
      0047A6 F0               [24]  750 	movx	@dptr,a
      0047A7 90 05 E0         [24]  751 	mov	dptr,#_reactive_age
      0047AA F5 F0            [12]  752 	mov	b,a
      0047AC 12 B5 15         [24]  753 	lcall	_memset
                                    754 ;	keyboards/ajazz/ak820/ak820_rgb.c:39: reactive_at = timer_read();
      0047AF 12 40 4E         [24]  755 	lcall	_timer_read
      0047B2 E5 82            [12]  756 	mov	a, dpl
      0047B4 85 83 F0         [24]  757 	mov	b, dph
      0047B7 90 06 32         [24]  758 	mov	dptr,#_reactive_at
      0047BA F0               [24]  759 	movx	@dptr,a
      0047BB E5 F0            [12]  760 	mov	a,b
      0047BD A3               [24]  761 	inc	dptr
      0047BE F0               [24]  762 	movx	@dptr,a
                                    763 ;	keyboards/ajazz/ak820/ak820_rgb.c:40: }
      0047BF 22               [24]  764 	ret
                                    765 ;------------------------------------------------------------
                                    766 ;Allocation info for local variables in function 'age_reactive'
                                    767 ;------------------------------------------------------------
                                    768 ;ticks         Allocated with name '_age_reactive_ticks_10000_246'
                                    769 ;i             Allocated with name '_age_reactive_i_10000_246'
                                    770 ;------------------------------------------------------------
                                    771 ;	keyboards/ajazz/ak820/ak820_rgb.c:42: static void age_reactive(void) {
                                    772 ;	-----------------------------------------
                                    773 ;	 function age_reactive
                                    774 ;	-----------------------------------------
      0047C0                        775 _age_reactive:
                                    776 ;	keyboards/ajazz/ak820/ak820_rgb.c:43: uint16_t ticks = timer_elapsed(reactive_at) >> 4;
      0047C0 90 06 32         [24]  777 	mov	dptr,#_reactive_at
      0047C3 E0               [24]  778 	movx	a,@dptr
      0047C4 FE               [12]  779 	mov	r6,a
      0047C5 A3               [24]  780 	inc	dptr
      0047C6 E0               [24]  781 	movx	a,@dptr
      0047C7 FF               [12]  782 	mov	r7,a
      0047C8 8E 82            [24]  783 	mov	dpl, r6
      0047CA 8F 83            [24]  784 	mov	dph, r7
      0047CC 12 40 51         [24]  785 	lcall	_timer_elapsed
      0047CF AE 82            [24]  786 	mov	r6, dpl
      0047D1 E5 83            [12]  787 	mov	a,dph
      0047D3 C4               [12]  788 	swap	a
      0047D4 CE               [12]  789 	xch	a,r6
      0047D5 C4               [12]  790 	swap	a
      0047D6 54 0F            [12]  791 	anl	a,#0x0f
      0047D8 6E               [12]  792 	xrl	a,r6
      0047D9 CE               [12]  793 	xch	a,r6
      0047DA 54 0F            [12]  794 	anl	a,#0x0f
      0047DC CE               [12]  795 	xch	a,r6
      0047DD 6E               [12]  796 	xrl	a,r6
      0047DE CE               [12]  797 	xch	a,r6
                                    798 ;	keyboards/ajazz/ak820/ak820_rgb.c:45: if (!ticks) return;
      0047DF FF               [12]  799 	mov	r7,a
      0047E0 4E               [12]  800 	orl	a,r6
      0047E1 70 01            [24]  801 	jnz	00102$
      0047E3 22               [24]  802 	ret
      0047E4                        803 00102$:
                                    804 ;	keyboards/ajazz/ak820/ak820_rgb.c:46: reactive_at += ticks << 4;
      0047E4 8E 04            [24]  805 	mov	ar4,r6
      0047E6 EF               [12]  806 	mov	a,r7
      0047E7 C4               [12]  807 	swap	a
      0047E8 54 F0            [12]  808 	anl	a,#0xf0
      0047EA CC               [12]  809 	xch	a,r4
      0047EB C4               [12]  810 	swap	a
      0047EC CC               [12]  811 	xch	a,r4
      0047ED 6C               [12]  812 	xrl	a,r4
      0047EE CC               [12]  813 	xch	a,r4
      0047EF 54 F0            [12]  814 	anl	a,#0xf0
      0047F1 CC               [12]  815 	xch	a,r4
      0047F2 6C               [12]  816 	xrl	a,r4
      0047F3 FD               [12]  817 	mov	r5,a
      0047F4 90 06 32         [24]  818 	mov	dptr,#_reactive_at
      0047F7 E0               [24]  819 	movx	a,@dptr
      0047F8 FA               [12]  820 	mov	r2,a
      0047F9 A3               [24]  821 	inc	dptr
      0047FA E0               [24]  822 	movx	a,@dptr
      0047FB FB               [12]  823 	mov	r3,a
      0047FC 90 06 32         [24]  824 	mov	dptr,#_reactive_at
      0047FF EC               [12]  825 	mov	a,r4
      004800 2A               [12]  826 	add	a, r2
      004801 F0               [24]  827 	movx	@dptr,a
      004802 ED               [12]  828 	mov	a,r5
      004803 3B               [12]  829 	addc	a, r3
      004804 A3               [24]  830 	inc	dptr
      004805 F0               [24]  831 	movx	@dptr,a
                                    832 ;	keyboards/ajazz/ak820/ak820_rgb.c:47: for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
      004806 7D 00            [12]  833 	mov	r5,#0x00
      004808                        834 00104$:
                                    835 ;	keyboards/ajazz/ak820/ak820_rgb.c:48: reactive_age[i] = ticks >= reactive_age[i] ? 0 : reactive_age[i] - ticks;
      004808 ED               [12]  836 	mov	a,r5
      004809 24 E0            [12]  837 	add	a, #_reactive_age
      00480B FB               [12]  838 	mov	r3,a
      00480C E4               [12]  839 	clr	a
      00480D 34 05            [12]  840 	addc	a, #(_reactive_age >> 8)
      00480F FC               [12]  841 	mov	r4,a
      004810 8B 82            [24]  842 	mov	dpl,r3
      004812 8C 83            [24]  843 	mov	dph,r4
      004814 E0               [24]  844 	movx	a,@dptr
      004815 F9               [12]  845 	mov	r1,a
      004816 7A 00            [12]  846 	mov	r2,#0x00
      004818 C3               [12]  847 	clr	c
      004819 EE               [12]  848 	mov	a,r6
      00481A 99               [12]  849 	subb	a,r1
      00481B EF               [12]  850 	mov	a,r7
      00481C 9A               [12]  851 	subb	a,r2
      00481D 40 04            [24]  852 	jc	00108$
      00481F 7A 00            [12]  853 	mov	r2,#0x00
      004821 80 0A            [24]  854 	sjmp	00109$
      004823                        855 00108$:
      004823 8B 82            [24]  856 	mov	dpl,r3
      004825 8C 83            [24]  857 	mov	dph,r4
      004827 E0               [24]  858 	movx	a,@dptr
      004828 8E 00            [24]  859 	mov	ar0,r6
      00482A C3               [12]  860 	clr	c
      00482B 98               [12]  861 	subb	a,r0
      00482C FA               [12]  862 	mov	r2,a
      00482D                        863 00109$:
      00482D 8B 82            [24]  864 	mov	dpl,r3
      00482F 8C 83            [24]  865 	mov	dph,r4
      004831 EA               [12]  866 	mov	a,r2
      004832 F0               [24]  867 	movx	@dptr,a
                                    868 ;	keyboards/ajazz/ak820/ak820_rgb.c:47: for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
      004833 0D               [12]  869 	inc	r5
      004834 BD 52 00         [24]  870 	cjne	r5,#0x52,00134$
      004837                        871 00134$:
      004837 40 CF            [24]  872 	jc	00104$
                                    873 ;	keyboards/ajazz/ak820/ak820_rgb.c:50: }
      004839 22               [24]  874 	ret
                                    875 ;------------------------------------------------------------
                                    876 ;Allocation info for local variables in function 'add_sat'
                                    877 ;------------------------------------------------------------
                                    878 ;y             Allocated with name '_add_sat_PARM_2'
                                    879 ;x             Allocated with name '_add_sat_x_10000_250'
                                    880 ;------------------------------------------------------------
                                    881 ;	keyboards/ajazz/ak820/ak820_rgb.c:52: static uint8_t add_sat(uint8_t x, uint8_t y) {
                                    882 ;	-----------------------------------------
                                    883 ;	 function add_sat
                                    884 ;	-----------------------------------------
      00483A                        885 _add_sat:
      00483A E5 82            [12]  886 	mov	a,dpl
      00483C 90 06 35         [24]  887 	mov	dptr,#_add_sat_x_10000_250
      00483F F0               [24]  888 	movx	@dptr,a
                                    889 ;	keyboards/ajazz/ak820/ak820_rgb.c:53: return x > (uint8_t)(255 - y) ? 255 : x + y;
      004840 90 06 34         [24]  890 	mov	dptr,#_add_sat_PARM_2
      004843 E0               [24]  891 	movx	a,@dptr
      004844 FF               [12]  892 	mov	r7,a
      004845 FE               [12]  893 	mov	r6,a
      004846 74 FF            [12]  894 	mov	a,#0xff
      004848 C3               [12]  895 	clr	c
      004849 9E               [12]  896 	subb	a,r6
      00484A FE               [12]  897 	mov	r6,a
      00484B 90 06 35         [24]  898 	mov	dptr,#_add_sat_x_10000_250
      00484E E0               [24]  899 	movx	a,@dptr
      00484F FD               [12]  900 	mov	r5,a
      004850 C3               [12]  901 	clr	c
      004851 EE               [12]  902 	mov	a,r6
      004852 9D               [12]  903 	subb	a,r5
      004853 50 04            [24]  904 	jnc	00103$
                                    905 ;	free result
      004855 7E FF            [12]  906 	mov	r6,#0xff
      004857 80 03            [24]  907 	sjmp	00104$
      004859                        908 00103$:
      004859 EF               [12]  909 	mov	a,r7
      00485A 2D               [12]  910 	add	a, r5
      00485B FE               [12]  911 	mov	r6,a
      00485C                        912 00104$:
      00485C 8E 82            [24]  913 	mov	dpl, r6
                                    914 ;	keyboards/ajazz/ak820/ak820_rgb.c:54: }
      00485E 22               [24]  915 	ret
                                    916 ;------------------------------------------------------------
                                    917 ;Allocation info for local variables in function 'sub_sat'
                                    918 ;------------------------------------------------------------
                                    919 ;y             Allocated with name '_sub_sat_PARM_2'
                                    920 ;x             Allocated with name '_sub_sat_x_10000_252'
                                    921 ;------------------------------------------------------------
                                    922 ;	keyboards/ajazz/ak820/ak820_rgb.c:56: static uint8_t sub_sat(uint8_t x, uint8_t y) {
                                    923 ;	-----------------------------------------
                                    924 ;	 function sub_sat
                                    925 ;	-----------------------------------------
      00485F                        926 _sub_sat:
      00485F E5 82            [12]  927 	mov	a,dpl
      004861 90 06 37         [24]  928 	mov	dptr,#_sub_sat_x_10000_252
      004864 F0               [24]  929 	movx	@dptr,a
                                    930 ;	keyboards/ajazz/ak820/ak820_rgb.c:57: return x < y ? 0 : x - y;
      004865 E0               [24]  931 	movx	a,@dptr
      004866 FF               [12]  932 	mov	r7,a
      004867 90 06 36         [24]  933 	mov	dptr,#_sub_sat_PARM_2
      00486A E0               [24]  934 	movx	a,@dptr
      00486B FE               [12]  935 	mov	r6,a
      00486C C3               [12]  936 	clr	c
      00486D EF               [12]  937 	mov	a,r7
      00486E 9E               [12]  938 	subb	a,r6
      00486F 50 04            [24]  939 	jnc	00103$
      004871 7D 00            [12]  940 	mov	r5,#0x00
      004873 80 04            [24]  941 	sjmp	00104$
      004875                        942 00103$:
      004875 EF               [12]  943 	mov	a,r7
      004876 C3               [12]  944 	clr	c
      004877 9E               [12]  945 	subb	a,r6
      004878 FD               [12]  946 	mov	r5,a
      004879                        947 00104$:
      004879 8D 82            [24]  948 	mov	dpl, r5
                                    949 ;	keyboards/ajazz/ak820/ak820_rgb.c:58: }
      00487B 22               [24]  950 	ret
                                    951 ;------------------------------------------------------------
                                    952 ;Allocation info for local variables in function 'mark_dirty'
                                    953 ;------------------------------------------------------------
                                    954 ;	keyboards/ajazz/ak820/ak820_rgb.c:60: static void mark_dirty(void) {
                                    955 ;	-----------------------------------------
                                    956 ;	 function mark_dirty
                                    957 ;	-----------------------------------------
      00487C                        958 _mark_dirty:
                                    959 ;	keyboards/ajazz/ak820/ak820_rgb.c:61: dirty = true;
      00487C 90 05 D1         [24]  960 	mov	dptr,#_dirty
      00487F 74 01            [12]  961 	mov	a,#0x01
      004881 F0               [24]  962 	movx	@dptr,a
                                    963 ;	keyboards/ajazz/ak820/ak820_rgb.c:62: changed_at = timer_read();
      004882 12 40 4E         [24]  964 	lcall	_timer_read
      004885 E5 82            [12]  965 	mov	a, dpl
      004887 85 83 F0         [24]  966 	mov	b, dph
      00488A 90 05 D3         [24]  967 	mov	dptr,#_changed_at
      00488D F0               [24]  968 	movx	@dptr,a
      00488E E5 F0            [12]  969 	mov	a,b
      004890 A3               [24]  970 	inc	dptr
      004891 F0               [24]  971 	movx	@dptr,a
                                    972 ;	keyboards/ajazz/ak820/ak820_rgb.c:63: }
      004892 22               [24]  973 	ret
                                    974 ;------------------------------------------------------------
                                    975 ;Allocation info for local variables in function 'eeconfig_update_rgb_matrix'
                                    976 ;------------------------------------------------------------
                                    977 ;raw           Allocated with name '_eeconfig_update_rgb_matrix_raw_10000_257'
                                    978 ;------------------------------------------------------------
                                    979 ;	keyboards/ajazz/ak820/ak820_rgb.c:65: void eeconfig_update_rgb_matrix(void) {
                                    980 ;	-----------------------------------------
                                    981 ;	 function eeconfig_update_rgb_matrix
                                    982 ;	-----------------------------------------
      004893                        983 _eeconfig_update_rgb_matrix:
                                    984 ;	keyboards/ajazz/ak820/ak820_rgb.c:67: uint8_t *raw = (uint8_t *)&rgb_matrix_config;
                                    985 ;	keyboards/ajazz/ak820/ak820_rgb.c:68: raw[6] = raw[7] = 0;
      004893 90 05 CF         [24]  986 	mov	dptr,#(_rgb_matrix_config + 0x0007)
      004896 E4               [12]  987 	clr	a
      004897 F0               [24]  988 	movx	@dptr,a
      004898 90 05 CE         [24]  989 	mov	dptr,#(_rgb_matrix_config + 0x0006)
      00489B F0               [24]  990 	movx	@dptr,a
                                    991 ;	keyboards/ajazz/ak820/ak820_rgb.c:69: eeprom_update_block(&rgb_matrix_config, EECONFIG_RGB_MATRIX, sizeof(rgb_matrix_config));
      00489C 90 05 B0         [24]  992 	mov	dptr,#_eeprom_update_block_PARM_2
      00489F 74 18            [12]  993 	mov	a,#0x18
      0048A1 F0               [24]  994 	movx	@dptr,a
      0048A2 E4               [12]  995 	clr	a
      0048A3 A3               [24]  996 	inc	dptr
      0048A4 F0               [24]  997 	movx	@dptr,a
      0048A5 A3               [24]  998 	inc	dptr
      0048A6 F0               [24]  999 	movx	@dptr,a
      0048A7 90 05 B3         [24] 1000 	mov	dptr,#_eeprom_update_block_PARM_3
      0048AA 74 08            [12] 1001 	mov	a,#0x08
      0048AC F0               [24] 1002 	movx	@dptr,a
      0048AD E4               [12] 1003 	clr	a
      0048AE A3               [24] 1004 	inc	dptr
      0048AF F0               [24] 1005 	movx	@dptr,a
      0048B0 90 05 C8         [24] 1006 	mov	dptr,#_rgb_matrix_config
      0048B3 F5 F0            [12] 1007 	mov	b,a
      0048B5 12 45 B0         [24] 1008 	lcall	_eeprom_update_block
                                   1009 ;	keyboards/ajazz/ak820/ak820_rgb.c:70: dirty = false;
      0048B8 90 05 D1         [24] 1010 	mov	dptr,#_dirty
      0048BB E4               [12] 1011 	clr	a
      0048BC F0               [24] 1012 	movx	@dptr,a
                                   1013 ;	keyboards/ajazz/ak820/ak820_rgb.c:71: }
      0048BD 22               [24] 1014 	ret
                                   1015 ;------------------------------------------------------------
                                   1016 ;Allocation info for local variables in function 'eeconfig_update_rgb_matrix_default'
                                   1017 ;------------------------------------------------------------
                                   1018 ;	keyboards/ajazz/ak820/ak820_rgb.c:73: void eeconfig_update_rgb_matrix_default(void) {
                                   1019 ;	-----------------------------------------
                                   1020 ;	 function eeconfig_update_rgb_matrix_default
                                   1021 ;	-----------------------------------------
      0048BE                       1022 _eeconfig_update_rgb_matrix_default:
                                   1023 ;	keyboards/ajazz/ak820/ak820_rgb.c:74: memset(&rgb_matrix_config, 0, sizeof(rgb_matrix_config));
      0048BE 90 0B 97         [24] 1024 	mov	dptr,#_memset_PARM_2
      0048C1 E4               [12] 1025 	clr	a
      0048C2 F0               [24] 1026 	movx	@dptr,a
      0048C3 90 0B 98         [24] 1027 	mov	dptr,#_memset_PARM_3
      0048C6 74 08            [12] 1028 	mov	a,#0x08
      0048C8 F0               [24] 1029 	movx	@dptr,a
      0048C9 E4               [12] 1030 	clr	a
      0048CA A3               [24] 1031 	inc	dptr
      0048CB F0               [24] 1032 	movx	@dptr,a
      0048CC 90 05 C8         [24] 1033 	mov	dptr,#_rgb_matrix_config
      0048CF F5 F0            [12] 1034 	mov	b,a
      0048D1 12 B5 15         [24] 1035 	lcall	_memset
                                   1036 ;	keyboards/ajazz/ak820/ak820_rgb.c:75: rgb_matrix_config.enable = 1;
      0048D4 90 05 C8         [24] 1037 	mov	dptr,#_rgb_matrix_config
      0048D7 E0               [24] 1038 	movx	a,@dptr
      0048D8 54 FC            [12] 1039 	anl	a,#0xfc
      0048DA 44 01            [12] 1040 	orl	a,#0x01
      0048DC F0               [24] 1041 	movx	@dptr,a
                                   1042 ;	keyboards/ajazz/ak820/ak820_rgb.c:76: rgb_matrix_config.mode = RGB_MATRIX_DEFAULT_MODE;
      0048DD 90 05 C8         [24] 1043 	mov	dptr,#_rgb_matrix_config
      0048E0 E0               [24] 1044 	movx	a,@dptr
      0048E1 54 03            [12] 1045 	anl	a,#0x03
      0048E3 44 04            [12] 1046 	orl	a,#0x04
      0048E5 F0               [24] 1047 	movx	@dptr,a
                                   1048 ;	keyboards/ajazz/ak820/ak820_rgb.c:77: rgb_matrix_config.hsv.h = 0;
      0048E6 90 05 C9         [24] 1049 	mov	dptr,#(_rgb_matrix_config + 0x0001)
      0048E9 E4               [12] 1050 	clr	a
      0048EA F0               [24] 1051 	movx	@dptr,a
                                   1052 ;	keyboards/ajazz/ak820/ak820_rgb.c:78: rgb_matrix_config.hsv.s = 255;
      0048EB 90 05 CA         [24] 1053 	mov	dptr,#(_rgb_matrix_config + 0x0002)
      0048EE 14               [12] 1054 	dec	a
      0048EF F0               [24] 1055 	movx	@dptr,a
                                   1056 ;	keyboards/ajazz/ak820/ak820_rgb.c:79: rgb_matrix_config.hsv.v = RGB_MATRIX_DEFAULT_VAL;
      0048F0 90 05 CB         [24] 1057 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      0048F3 74 50            [12] 1058 	mov	a,#0x50
      0048F5 F0               [24] 1059 	movx	@dptr,a
                                   1060 ;	keyboards/ajazz/ak820/ak820_rgb.c:80: rgb_matrix_config.speed = RGB_MATRIX_DEFAULT_SPD;
      0048F6 90 05 CC         [24] 1061 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      0048F9 74 60            [12] 1062 	mov	a,#0x60
      0048FB F0               [24] 1063 	movx	@dptr,a
                                   1064 ;	keyboards/ajazz/ak820/ak820_rgb.c:81: rgb_matrix_config.flags = LED_FLAG_ALL;
      0048FC 90 05 CD         [24] 1065 	mov	dptr,#(_rgb_matrix_config + 0x0005)
      0048FF 74 FF            [12] 1066 	mov	a,#0xff
      004901 F0               [24] 1067 	movx	@dptr,a
                                   1068 ;	keyboards/ajazz/ak820/ak820_rgb.c:82: eeconfig_update_rgb_matrix();
                                   1069 ;	keyboards/ajazz/ak820/ak820_rgb.c:83: }
      004902 02 48 93         [24] 1070 	ljmp	_eeconfig_update_rgb_matrix
                                   1071 ;------------------------------------------------------------
                                   1072 ;Allocation info for local variables in function 'rgb_matrix_reload_from_eeprom'
                                   1073 ;------------------------------------------------------------
                                   1074 ;	keyboards/ajazz/ak820/ak820_rgb.c:85: void rgb_matrix_reload_from_eeprom(void) {
                                   1075 ;	-----------------------------------------
                                   1076 ;	 function rgb_matrix_reload_from_eeprom
                                   1077 ;	-----------------------------------------
      004905                       1078 _rgb_matrix_reload_from_eeprom:
                                   1079 ;	keyboards/ajazz/ak820/ak820_rgb.c:86: eeprom_read_block(&rgb_matrix_config, EECONFIG_RGB_MATRIX, sizeof(rgb_matrix_config));
      004905 90 05 3D         [24] 1080 	mov	dptr,#_eeprom_read_block_PARM_2
      004908 74 18            [12] 1081 	mov	a,#0x18
      00490A F0               [24] 1082 	movx	@dptr,a
      00490B E4               [12] 1083 	clr	a
      00490C A3               [24] 1084 	inc	dptr
      00490D F0               [24] 1085 	movx	@dptr,a
      00490E A3               [24] 1086 	inc	dptr
      00490F F0               [24] 1087 	movx	@dptr,a
      004910 90 05 40         [24] 1088 	mov	dptr,#_eeprom_read_block_PARM_3
      004913 74 08            [12] 1089 	mov	a,#0x08
      004915 F0               [24] 1090 	movx	@dptr,a
      004916 E4               [12] 1091 	clr	a
      004917 A3               [24] 1092 	inc	dptr
      004918 F0               [24] 1093 	movx	@dptr,a
      004919 90 05 C8         [24] 1094 	mov	dptr,#_rgb_matrix_config
      00491C F5 F0            [12] 1095 	mov	b,a
      00491E 12 3D 3D         [24] 1096 	lcall	_eeprom_read_block
                                   1097 ;	keyboards/ajazz/ak820/ak820_rgb.c:87: if (!rgb_matrix_config.mode || rgb_matrix_config.mode >= RGB_MATRIX_EFFECT_MAX || rgb_matrix_config.enable > 1) {
      004921 90 05 C8         [24] 1098 	mov	dptr,#_rgb_matrix_config
      004924 E0               [24] 1099 	movx	a,@dptr
      004925 54 FC            [12] 1100 	anl	a,#0xfc
      004927 60 19            [24] 1101 	jz	00101$
      004929 90 05 C8         [24] 1102 	mov	dptr,#_rgb_matrix_config
      00492C E0               [24] 1103 	movx	a,@dptr
      00492D 03               [12] 1104 	rr	a
      00492E 03               [12] 1105 	rr	a
      00492F 54 3F            [12] 1106 	anl	a,#0x3f
      004931 C3               [12] 1107 	clr	c
      004932 64 80            [12] 1108 	xrl	a,#0x80
      004934 94 87            [12] 1109 	subb	a,#0x87
      004936 50 0A            [24] 1110 	jnc	00101$
      004938 90 05 C8         [24] 1111 	mov	dptr,#_rgb_matrix_config
      00493B E0               [24] 1112 	movx	a,@dptr
      00493C 54 03            [12] 1113 	anl	a,#0x03
      00493E 24 FE            [12] 1114 	add	a,#0xff - 0x01
      004940 50 03            [24] 1115 	jnc	00102$
                                   1116 ;	free result
      004942                       1117 00101$:
                                   1118 ;	keyboards/ajazz/ak820/ak820_rgb.c:88: eeconfig_update_rgb_matrix_default();
      004942 12 48 BE         [24] 1119 	lcall	_eeconfig_update_rgb_matrix_default
      004945                       1120 00102$:
                                   1121 ;	keyboards/ajazz/ak820/ak820_rgb.c:90: if (rgb_matrix_config.hsv.v > RGB_MATRIX_MAXIMUM_BRIGHTNESS) {
      004945 90 05 CB         [24] 1122 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      004948 E0               [24] 1123 	movx	a,@dptr
      004949 24 5F            [12] 1124 	add	a,#0xff - 0xa0
      00494B 50 06            [24] 1125 	jnc	00106$
                                   1126 ;	free result
                                   1127 ;	keyboards/ajazz/ak820/ak820_rgb.c:91: rgb_matrix_config.hsv.v = RGB_MATRIX_MAXIMUM_BRIGHTNESS;
      00494D 90 05 CB         [24] 1128 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      004950 74 A0            [12] 1129 	mov	a,#0xa0
      004952 F0               [24] 1130 	movx	@dptr,a
      004953                       1131 00106$:
                                   1132 ;	keyboards/ajazz/ak820/ak820_rgb.c:93: dirty = false;
      004953 90 05 D1         [24] 1133 	mov	dptr,#_dirty
      004956 E4               [12] 1134 	clr	a
      004957 F0               [24] 1135 	movx	@dptr,a
                                   1136 ;	keyboards/ajazz/ak820/ak820_rgb.c:94: rendering = false;
      004958 90 05 D2         [24] 1137 	mov	dptr,#_rendering
      00495B F0               [24] 1138 	movx	@dptr,a
                                   1139 ;	keyboards/ajazz/ak820/ak820_rgb.c:95: clear_reactive();
                                   1140 ;	keyboards/ajazz/ak820/ak820_rgb.c:96: }
      00495C 02 47 99         [24] 1141 	ljmp	_clear_reactive
                                   1142 ;------------------------------------------------------------
                                   1143 ;Allocation info for local variables in function 'rgb_matrix_init'
                                   1144 ;------------------------------------------------------------
                                   1145 ;	keyboards/ajazz/ak820/ak820_rgb.c:98: void rgb_matrix_init(void) {
                                   1146 ;	-----------------------------------------
                                   1147 ;	 function rgb_matrix_init
                                   1148 ;	-----------------------------------------
      00495F                       1149 _rgb_matrix_init:
                                   1150 ;	keyboards/ajazz/ak820/ak820_rgb.c:99: rgb_matrix_driver.init();
      00495F 90 B5 FA         [24] 1151 	mov	dptr,#_rgb_matrix_driver
      004962 E4               [12] 1152 	clr	a
      004963 93               [24] 1153 	movc	a,@a+dptr
      004964 FE               [12] 1154 	mov	r6,a
      004965 A3               [24] 1155 	inc	dptr
      004966 E4               [12] 1156 	clr	a
      004967 93               [24] 1157 	movc	a,@a+dptr
      004968 FF               [12] 1158 	mov	r7,a
      004969 C0 07            [24] 1159 	push	ar7
      00496B C0 06            [24] 1160 	push	ar6
      00496D 8E 82            [24] 1161 	mov	dpl,r6
      00496F 8F 83            [24] 1162 	mov	dph,r7
      004971 12 30 75         [24] 1163 	lcall	__sdcc_call_dptr
      004974 D0 06            [24] 1164 	pop	ar6
      004976 D0 07            [24] 1165 	pop	ar7
                                   1166 ;	keyboards/ajazz/ak820/ak820_rgb.c:100: rgb_matrix_reload_from_eeprom();
      004978 12 49 05         [24] 1167 	lcall	_rgb_matrix_reload_from_eeprom
                                   1168 ;	keyboards/ajazz/ak820/ak820_rgb.c:101: frame_at = timer_read() - RGB_MATRIX_LED_FLUSH_LIMIT;
      00497B 12 40 4E         [24] 1169 	lcall	_timer_read
      00497E AE 82            [24] 1170 	mov	r6, dpl
      004980 AF 83            [24] 1171 	mov	r7, dph
      004982 EE               [12] 1172 	mov	a,r6
      004983 24 F0            [12] 1173 	add	a,#0xf0
      004985 FE               [12] 1174 	mov	r6,a
      004986 EF               [12] 1175 	mov	a,r7
      004987 34 FF            [12] 1176 	addc	a,#0xff
      004989 FF               [12] 1177 	mov	r7,a
      00498A 90 05 D5         [24] 1178 	mov	dptr,#_frame_at
      00498D EE               [12] 1179 	mov	a,r6
      00498E F0               [24] 1180 	movx	@dptr,a
      00498F EF               [12] 1181 	mov	a,r7
      004990 A3               [24] 1182 	inc	dptr
      004991 F0               [24] 1183 	movx	@dptr,a
                                   1184 ;	keyboards/ajazz/ak820/ak820_rgb.c:102: }
      004992 22               [24] 1185 	ret
                                   1186 ;------------------------------------------------------------
                                   1187 ;Allocation info for local variables in function 'rgb_matrix_set_color'
                                   1188 ;------------------------------------------------------------
                                   1189 ;r             Allocated with name '_rgb_matrix_set_color_PARM_2'
                                   1190 ;g             Allocated with name '_rgb_matrix_set_color_PARM_3'
                                   1191 ;b             Allocated with name '_rgb_matrix_set_color_PARM_4'
                                   1192 ;index         Allocated with name '_rgb_matrix_set_color_index_10000_268'
                                   1193 ;------------------------------------------------------------
                                   1194 ;	keyboards/ajazz/ak820/ak820_rgb.c:104: void rgb_matrix_set_color(int index, uint8_t r, uint8_t g, uint8_t b) {
                                   1195 ;	-----------------------------------------
                                   1196 ;	 function rgb_matrix_set_color
                                   1197 ;	-----------------------------------------
      004993                       1198 _rgb_matrix_set_color:
      004993 AF 83            [24] 1199 	mov	r7,dph
      004995 E5 82            [12] 1200 	mov	a,dpl
      004997 90 06 3B         [24] 1201 	mov	dptr,#_rgb_matrix_set_color_index_10000_268
      00499A F0               [24] 1202 	movx	@dptr,a
      00499B EF               [12] 1203 	mov	a,r7
      00499C A3               [24] 1204 	inc	dptr
      00499D F0               [24] 1205 	movx	@dptr,a
                                   1206 ;	keyboards/ajazz/ak820/ak820_rgb.c:105: if (index >= 0 && index < RGB_MATRIX_LED_COUNT) rgb_matrix_driver.set_color(index, r, g, b);
      00499E 90 06 3B         [24] 1207 	mov	dptr,#_rgb_matrix_set_color_index_10000_268
      0049A1 E0               [24] 1208 	movx	a,@dptr
      0049A2 FE               [12] 1209 	mov	r6,a
      0049A3 A3               [24] 1210 	inc	dptr
      0049A4 E0               [24] 1211 	movx	a,@dptr
      0049A5 FF               [12] 1212 	mov	r7,a
      0049A6 20 E7 43         [24] 1213 	jb	acc.7,00104$
      0049A9 C3               [12] 1214 	clr	c
      0049AA EE               [12] 1215 	mov	a,r6
      0049AB 94 52            [12] 1216 	subb	a,#0x52
      0049AD EF               [12] 1217 	mov	a,r7
      0049AE 64 80            [12] 1218 	xrl	a,#0x80
      0049B0 94 80            [12] 1219 	subb	a,#0x80
      0049B2 50 38            [24] 1220 	jnc	00104$
      0049B4 90 B5 FC         [24] 1221 	mov	dptr,#(_rgb_matrix_driver + 0x0002)
      0049B7 E4               [12] 1222 	clr	a
      0049B8 93               [24] 1223 	movc	a,@a+dptr
      0049B9 FC               [12] 1224 	mov	r4,a
      0049BA A3               [24] 1225 	inc	dptr
      0049BB E4               [12] 1226 	clr	a
      0049BC 93               [24] 1227 	movc	a,@a+dptr
      0049BD FD               [12] 1228 	mov	r5,a
      0049BE C0 05            [24] 1229 	push	ar5
      0049C0 C0 04            [24] 1230 	push	ar4
      0049C2 90 06 3A         [24] 1231 	mov	dptr,#_rgb_matrix_set_color_PARM_4
      0049C5 E0               [24] 1232 	movx	a,@dptr
      0049C6 C0 E0            [24] 1233 	push	acc
      0049C8 90 06 39         [24] 1234 	mov	dptr,#_rgb_matrix_set_color_PARM_3
      0049CB E0               [24] 1235 	movx	a,@dptr
      0049CC C0 E0            [24] 1236 	push	acc
      0049CE 90 06 38         [24] 1237 	mov	dptr,#_rgb_matrix_set_color_PARM_2
      0049D1 E0               [24] 1238 	movx	a,@dptr
      0049D2 C0 E0            [24] 1239 	push	acc
      0049D4 12 49 D9         [24] 1240 	lcall	00122$
      0049D7 80 09            [24] 1241 	sjmp	00123$
      0049D9                       1242 00122$:
      0049D9 C0 04            [24] 1243 	push	ar4
      0049DB C0 05            [24] 1244 	push	ar5
      0049DD 8E 82            [24] 1245 	mov	dpl, r6
      0049DF 8F 83            [24] 1246 	mov	dph, r7
      0049E1 22               [24] 1247 	ret
      0049E2                       1248 00123$:
      0049E2 15 81            [12] 1249 	dec	sp
      0049E4 15 81            [12] 1250 	dec	sp
      0049E6 15 81            [12] 1251 	dec	sp
      0049E8 D0 04            [24] 1252 	pop	ar4
      0049EA D0 05            [24] 1253 	pop	ar5
      0049EC                       1254 00104$:
                                   1255 ;	keyboards/ajazz/ak820/ak820_rgb.c:106: }
      0049EC 22               [24] 1256 	ret
                                   1257 ;------------------------------------------------------------
                                   1258 ;Allocation info for local variables in function 'rgb_matrix_set_color_all'
                                   1259 ;------------------------------------------------------------
                                   1260 ;g             Allocated with name '_rgb_matrix_set_color_all_PARM_2'
                                   1261 ;b             Allocated with name '_rgb_matrix_set_color_all_PARM_3'
                                   1262 ;r             Allocated with name '_rgb_matrix_set_color_all_r_10000_271'
                                   1263 ;------------------------------------------------------------
                                   1264 ;	keyboards/ajazz/ak820/ak820_rgb.c:108: void rgb_matrix_set_color_all(uint8_t r, uint8_t g, uint8_t b) {
                                   1265 ;	-----------------------------------------
                                   1266 ;	 function rgb_matrix_set_color_all
                                   1267 ;	-----------------------------------------
      0049ED                       1268 _rgb_matrix_set_color_all:
      0049ED E5 82            [12] 1269 	mov	a,dpl
      0049EF 90 06 3F         [24] 1270 	mov	dptr,#_rgb_matrix_set_color_all_r_10000_271
      0049F2 F0               [24] 1271 	movx	@dptr,a
                                   1272 ;	keyboards/ajazz/ak820/ak820_rgb.c:109: rgb_matrix_driver.set_color_all(r, g, b);
      0049F3 90 B5 FE         [24] 1273 	mov	dptr,#(_rgb_matrix_driver + 0x0004)
      0049F6 E4               [12] 1274 	clr	a
      0049F7 93               [24] 1275 	movc	a,@a+dptr
      0049F8 FE               [12] 1276 	mov	r6,a
      0049F9 A3               [24] 1277 	inc	dptr
      0049FA E4               [12] 1278 	clr	a
      0049FB 93               [24] 1279 	movc	a,@a+dptr
      0049FC FF               [12] 1280 	mov	r7,a
      0049FD 90 06 3F         [24] 1281 	mov	dptr,#_rgb_matrix_set_color_all_r_10000_271
      004A00 E0               [24] 1282 	movx	a,@dptr
      004A01 FD               [12] 1283 	mov	r5,a
      004A02 C0 07            [24] 1284 	push	ar7
      004A04 C0 06            [24] 1285 	push	ar6
      004A06 90 06 3E         [24] 1286 	mov	dptr,#_rgb_matrix_set_color_all_PARM_3
      004A09 E0               [24] 1287 	movx	a,@dptr
      004A0A C0 E0            [24] 1288 	push	acc
      004A0C 90 06 3D         [24] 1289 	mov	dptr,#_rgb_matrix_set_color_all_PARM_2
      004A0F E0               [24] 1290 	movx	a,@dptr
      004A10 C0 E0            [24] 1291 	push	acc
      004A12 12 4A 17         [24] 1292 	lcall	00103$
      004A15 80 07            [24] 1293 	sjmp	00104$
      004A17                       1294 00103$:
      004A17 C0 06            [24] 1295 	push	ar6
      004A19 C0 07            [24] 1296 	push	ar7
      004A1B 8D 82            [24] 1297 	mov	dpl, r5
      004A1D 22               [24] 1298 	ret
      004A1E                       1299 00104$:
      004A1E 15 81            [12] 1300 	dec	sp
      004A20 15 81            [12] 1301 	dec	sp
      004A22 D0 06            [24] 1302 	pop	ar6
      004A24 D0 07            [24] 1303 	pop	ar7
                                   1304 ;	keyboards/ajazz/ak820/ak820_rgb.c:110: }
      004A26 22               [24] 1305 	ret
                                   1306 ;------------------------------------------------------------
                                   1307 ;Allocation info for local variables in function 'sine8'
                                   1308 ;------------------------------------------------------------
                                   1309 ;theta         Allocated with name '_sine8_theta_10000_273'
                                   1310 ;offset        Allocated with name '_sine8_offset_10000_274'
                                   1311 ;section       Allocated with name '_sine8_section_10000_274'
                                   1312 ;fraction      Allocated with name '_sine8_fraction_10000_274'
                                   1313 ;value         Allocated with name '_sine8_value_10000_274'
                                   1314 ;------------------------------------------------------------
                                   1315 ;	keyboards/ajazz/ak820/ak820_rgb.c:113: static uint8_t sine8(uint8_t theta) {
                                   1316 ;	-----------------------------------------
                                   1317 ;	 function sine8
                                   1318 ;	-----------------------------------------
      004A27                       1319 _sine8:
      004A27 E5 82            [12] 1320 	mov	a,dpl
      004A29 90 06 40         [24] 1321 	mov	dptr,#_sine8_theta_10000_273
      004A2C F0               [24] 1322 	movx	@dptr,a
                                   1323 ;	keyboards/ajazz/ak820/ak820_rgb.c:115: uint8_t offset = theta;
      004A2D E0               [24] 1324 	movx	a,@dptr
      004A2E FF               [12] 1325 	mov	r7,a
      004A2F 90 06 41         [24] 1326 	mov	dptr,#_sine8_offset_10000_274
      004A32 F0               [24] 1327 	movx	@dptr,a
                                   1328 ;	keyboards/ajazz/ak820/ak820_rgb.c:117: if (theta & 0x40) offset = 255 - offset;
      004A33 EF               [12] 1329 	mov	a,r7
      004A34 30 E6 08         [24] 1330 	jnb	acc.6,00102$
      004A37 90 06 41         [24] 1331 	mov	dptr,#_sine8_offset_10000_274
      004A3A 74 FF            [12] 1332 	mov	a,#0xff
      004A3C C3               [12] 1333 	clr	c
      004A3D 9F               [12] 1334 	subb	a,r7
      004A3E F0               [24] 1335 	movx	@dptr,a
      004A3F                       1336 00102$:
                                   1337 ;	keyboards/ajazz/ak820/ak820_rgb.c:118: offset &= 0x3f;
      004A3F 90 06 41         [24] 1338 	mov	dptr,#_sine8_offset_10000_274
      004A42 E0               [24] 1339 	movx	a,@dptr
      004A43 53 E0 3F         [24] 1340 	anl	acc,#0x3f
      004A46 F0               [24] 1341 	movx	@dptr,a
                                   1342 ;	keyboards/ajazz/ak820/ak820_rgb.c:119: fraction = offset & 15;
      004A47 90 06 41         [24] 1343 	mov	dptr,#_sine8_offset_10000_274
      004A4A E0               [24] 1344 	movx	a,@dptr
      004A4B 54 0F            [12] 1345 	anl	a,#0x0f
      004A4D FF               [12] 1346 	mov	r7,a
      004A4E 90 06 42         [24] 1347 	mov	dptr,#_sine8_fraction_10000_274
      004A51 F0               [24] 1348 	movx	@dptr,a
                                   1349 ;	keyboards/ajazz/ak820/ak820_rgb.c:120: if (theta & 0x40) ++fraction;
      004A52 90 06 40         [24] 1350 	mov	dptr,#_sine8_theta_10000_273
      004A55 E0               [24] 1351 	movx	a,@dptr
      004A56 30 E6 06         [24] 1352 	jnb	acc.6,00104$
      004A59 90 06 42         [24] 1353 	mov	dptr,#_sine8_fraction_10000_274
      004A5C EF               [12] 1354 	mov	a,r7
      004A5D 04               [12] 1355 	inc	a
      004A5E F0               [24] 1356 	movx	@dptr,a
      004A5F                       1357 00104$:
                                   1358 ;	keyboards/ajazz/ak820/ak820_rgb.c:121: section = (offset >> 4) * 2;
      004A5F 90 06 41         [24] 1359 	mov	dptr,#_sine8_offset_10000_274
      004A62 E0               [24] 1360 	movx	a,@dptr
      004A63 C4               [12] 1361 	swap	a
      004A64 54 0F            [12] 1362 	anl	a,#0x0f
                                   1363 ;	keyboards/ajazz/ak820/ak820_rgb.c:122: value = coefficients[section] + (((uint16_t)coefficients[section + 1] * fraction) >> 4);
      004A66 25 E0            [12] 1364 	add	a,acc
      004A68 FF               [12] 1365 	mov	r7,a
      004A69 90 B6 02         [24] 1366 	mov	dptr,#_sine8_coefficients_10000_274
      004A6C 93               [24] 1367 	movc	a,@a+dptr
      004A6D FE               [12] 1368 	mov	r6,a
      004A6E 0F               [12] 1369 	inc	r7
      004A6F EF               [12] 1370 	mov	a,r7
      004A70 90 B6 02         [24] 1371 	mov	dptr,#_sine8_coefficients_10000_274
      004A73 93               [24] 1372 	movc	a,@a+dptr
      004A74 FF               [12] 1373 	mov	r7,a
      004A75 90 06 42         [24] 1374 	mov	dptr,#_sine8_fraction_10000_274
      004A78 E0               [24] 1375 	movx	a,@dptr
      004A79 8F F0            [24] 1376 	mov	b,r7
      004A7B A4               [48] 1377 	mul	ab
      004A7C FF               [12] 1378 	mov	r7,a
      004A7D E5 F0            [12] 1379 	mov	a,b
      004A7F C4               [12] 1380 	swap	a
      004A80 CF               [12] 1381 	xch	a,r7
      004A81 C4               [12] 1382 	swap	a
      004A82 54 0F            [12] 1383 	anl	a,#0x0f
      004A84 6F               [12] 1384 	xrl	a,r7
      004A85 CF               [12] 1385 	xch	a,r7
      004A86 54 0F            [12] 1386 	anl	a,#0x0f
      004A88 CF               [12] 1387 	xch	a,r7
      004A89 6F               [12] 1388 	xrl	a,r7
      004A8A CF               [12] 1389 	xch	a,r7
      004A8B EF               [12] 1390 	mov	a,r7
      004A8C 2E               [12] 1391 	add	a, r6
      004A8D FF               [12] 1392 	mov	r7,a
                                   1393 ;	keyboards/ajazz/ak820/ak820_rgb.c:123: return (theta & 0x80) ? 128 - value : 128 + value;
      004A8E 90 06 40         [24] 1394 	mov	dptr,#_sine8_theta_10000_273
      004A91 E0               [24] 1395 	movx	a,@dptr
      004A92 30 E7 09         [24] 1396 	jnb	acc.7,00107$
      004A95 8F 06            [24] 1397 	mov	ar6,r7
      004A97 74 80            [12] 1398 	mov	a,#0x80
      004A99 C3               [12] 1399 	clr	c
      004A9A 9E               [12] 1400 	subb	a,r6
      004A9B FE               [12] 1401 	mov	r6,a
      004A9C 80 04            [24] 1402 	sjmp	00108$
      004A9E                       1403 00107$:
      004A9E 74 80            [12] 1404 	mov	a,#0x80
      004AA0 2F               [12] 1405 	add	a, r7
      004AA1 FE               [12] 1406 	mov	r6,a
      004AA2                       1407 00108$:
      004AA2 8E 82            [24] 1408 	mov	dpl, r6
                                   1409 ;	keyboards/ajazz/ak820/ak820_rgb.c:124: }
      004AA4 22               [24] 1410 	ret
                                   1411 ;------------------------------------------------------------
                                   1412 ;Allocation info for local variables in function 'breathing_cie'
                                   1413 ;------------------------------------------------------------
                                   1414 ;value         Allocated with name '_breathing_cie_value_10000_277'
                                   1415 ;index         Allocated with name '_breathing_cie_index_10000_278'
                                   1416 ;low           Allocated with name '_breathing_cie_low_10000_278'
                                   1417 ;delta         Allocated with name '_breathing_cie_delta_10001_280'
                                   1418 ;fraction      Allocated with name '_breathing_cie_fraction_10001_280'
                                   1419 ;product       Allocated with name '_breathing_cie_product_10001_280'
                                   1420 ;------------------------------------------------------------
                                   1421 ;	keyboards/ajazz/ak820/ak820_rgb.c:131: static uint8_t breathing_cie(uint8_t value) {
                                   1422 ;	-----------------------------------------
                                   1423 ;	 function breathing_cie
                                   1424 ;	-----------------------------------------
      004AA5                       1425 _breathing_cie:
      004AA5 E5 82            [12] 1426 	mov	a,dpl
      004AA7 90 06 43         [24] 1427 	mov	dptr,#_breathing_cie_value_10000_277
      004AAA F0               [24] 1428 	movx	@dptr,a
                                   1429 ;	keyboards/ajazz/ak820/ak820_rgb.c:135: uint8_t index = value >> 3;
      004AAB E0               [24] 1430 	movx	a,@dptr
      004AAC FF               [12] 1431 	mov	r7,a
      004AAD C4               [12] 1432 	swap	a
      004AAE 23               [12] 1433 	rl	a
      004AAF 54 1F            [12] 1434 	anl	a,#0x1f
                                   1435 ;	keyboards/ajazz/ak820/ak820_rgb.c:136: uint8_t low = pgm_read_byte(&CIE1931_CURVE[index]);
      004AB1 FE               [12] 1436 	mov	r6,a
      004AB2 90 B9 02         [24] 1437 	mov	dptr,#_CIE1931_CURVE
      004AB5 93               [24] 1438 	movc	a,@a+dptr
      004AB6 FD               [12] 1439 	mov	r5,a
                                   1440 ;	keyboards/ajazz/ak820/ak820_rgb.c:137: if (index == 31) return low;
      004AB7 BE 1F 03         [24] 1441 	cjne	r6,#0x1f,00102$
      004ABA 8D 82            [24] 1442 	mov	dpl, r5
      004ABC 22               [24] 1443 	ret
      004ABD                       1444 00102$:
                                   1445 ;	keyboards/ajazz/ak820/ak820_rgb.c:138: uint8_t delta = pgm_read_byte(&CIE1931_CURVE[index + 1]) - low;
      004ABD EE               [12] 1446 	mov	a,r6
      004ABE 04               [12] 1447 	inc	a
      004ABF 90 B9 02         [24] 1448 	mov	dptr,#_CIE1931_CURVE
      004AC2 93               [24] 1449 	movc	a,@a+dptr
      004AC3 C3               [12] 1450 	clr	c
      004AC4 9D               [12] 1451 	subb	a,r5
      004AC5 FE               [12] 1452 	mov	r6,a
                                   1453 ;	keyboards/ajazz/ak820/ak820_rgb.c:139: uint8_t fraction = value & 7;
      004AC6 74 07            [12] 1454 	mov	a,#0x07
      004AC8 5F               [12] 1455 	anl	a,r7
                                   1456 ;	keyboards/ajazz/ak820/ak820_rgb.c:140: uint8_t product = (uint8_t)(delta * fraction);
      004AC9 F5 F0            [12] 1457 	mov	b,a
      004ACB EE               [12] 1458 	mov	a,r6
      004ACC A4               [48] 1459 	mul	ab
                                   1460 ;	keyboards/ajazz/ak820/ak820_rgb.c:141: return low + (product >> 3);
      004ACD C4               [12] 1461 	swap	a
      004ACE 23               [12] 1462 	rl	a
      004ACF 54 1F            [12] 1463 	anl	a,#0x1f
      004AD1 2D               [12] 1464 	add	a, r5
                                   1465 ;	keyboards/ajazz/ak820/ak820_rgb.c:143: }
      004AD2 F5 82            [12] 1466 	mov	dpl,a
      004AD4 22               [24] 1467 	ret
                                   1468 ;------------------------------------------------------------
                                   1469 ;Allocation info for local variables in function 'rgb_matrix_task'
                                   1470 ;------------------------------------------------------------
                                   1471 ;end           Allocated with name '_rgb_matrix_task_end_10000_282'
                                   1472 ;hsv           Allocated with name '_rgb_matrix_task_hsv_10000_282'
                                   1473 ;rgb           Allocated with name '_rgb_matrix_task_rgb_10000_282'
                                   1474 ;shift         Allocated with name '_rgb_matrix_task_shift_60000_297'
                                   1475 ;duration      Allocated with name '_rgb_matrix_task_duration_60000_297'
                                   1476 ;age           Allocated with name '_rgb_matrix_task_age_60000_297'
                                   1477 ;------------------------------------------------------------
                                   1478 ;	keyboards/ajazz/ak820/ak820_rgb.c:146: void rgb_matrix_task(void) {
                                   1479 ;	-----------------------------------------
                                   1480 ;	 function rgb_matrix_task
                                   1481 ;	-----------------------------------------
      004AD5                       1482 _rgb_matrix_task:
                                   1483 ;	keyboards/ajazz/ak820/ak820_rgb.c:150: age_reactive();
      004AD5 12 47 C0         [24] 1484 	lcall	_age_reactive
                                   1485 ;	keyboards/ajazz/ak820/ak820_rgb.c:151: if (dirty && timer_elapsed(changed_at) >= 1000) eeconfig_update_rgb_matrix();
      004AD8 90 05 D1         [24] 1486 	mov	dptr,#_dirty
      004ADB E0               [24] 1487 	movx	a,@dptr
      004ADC 60 1F            [24] 1488 	jz	00102$
      004ADE 90 05 D3         [24] 1489 	mov	dptr,#_changed_at
      004AE1 E0               [24] 1490 	movx	a,@dptr
      004AE2 FE               [12] 1491 	mov	r6,a
      004AE3 A3               [24] 1492 	inc	dptr
      004AE4 E0               [24] 1493 	movx	a,@dptr
      004AE5 FF               [12] 1494 	mov	r7,a
      004AE6 8E 82            [24] 1495 	mov	dpl, r6
      004AE8 8F 83            [24] 1496 	mov	dph, r7
      004AEA 12 40 51         [24] 1497 	lcall	_timer_elapsed
      004AED AE 82            [24] 1498 	mov	r6, dpl
      004AEF AF 83            [24] 1499 	mov	r7, dph
      004AF1 C3               [12] 1500 	clr	c
      004AF2 EE               [12] 1501 	mov	a,r6
      004AF3 94 E8            [12] 1502 	subb	a,#0xe8
      004AF5 EF               [12] 1503 	mov	a,r7
      004AF6 94 03            [12] 1504 	subb	a,#0x03
      004AF8 40 03            [24] 1505 	jc	00102$
      004AFA 12 48 93         [24] 1506 	lcall	_eeconfig_update_rgb_matrix
      004AFD                       1507 00102$:
                                   1508 ;	keyboards/ajazz/ak820/ak820_rgb.c:152: if (!rendering) {
      004AFD 90 05 D2         [24] 1509 	mov	dptr,#_rendering
      004B00 E0               [24] 1510 	movx	a,@dptr
      004B01 60 03            [24] 1511 	jz	00253$
      004B03 02 4B D6         [24] 1512 	ljmp	00109$
      004B06                       1513 00253$:
                                   1514 ;	keyboards/ajazz/ak820/ak820_rgb.c:153: if (timer_elapsed(frame_at) < RGB_MATRIX_LED_FLUSH_LIMIT) return;
      004B06 90 05 D5         [24] 1515 	mov	dptr,#_frame_at
      004B09 E0               [24] 1516 	movx	a,@dptr
      004B0A FE               [12] 1517 	mov	r6,a
      004B0B A3               [24] 1518 	inc	dptr
      004B0C E0               [24] 1519 	movx	a,@dptr
      004B0D FF               [12] 1520 	mov	r7,a
      004B0E 8E 82            [24] 1521 	mov	dpl, r6
      004B10 8F 83            [24] 1522 	mov	dph, r7
      004B12 12 40 51         [24] 1523 	lcall	_timer_elapsed
      004B15 AE 82            [24] 1524 	mov	r6, dpl
      004B17 AF 83            [24] 1525 	mov	r7, dph
      004B19 C3               [12] 1526 	clr	c
      004B1A EE               [12] 1527 	mov	a,r6
      004B1B 94 10            [12] 1528 	subb	a,#0x10
      004B1D EF               [12] 1529 	mov	a,r7
      004B1E 94 00            [12] 1530 	subb	a,#0x00
      004B20 50 01            [24] 1531 	jnc	00105$
      004B22 22               [24] 1532 	ret
      004B23                       1533 00105$:
                                   1534 ;	keyboards/ajazz/ak820/ak820_rgb.c:154: frame_at = timer_read();
      004B23 12 40 4E         [24] 1535 	lcall	_timer_read
      004B26 E5 82            [12] 1536 	mov	a, dpl
      004B28 85 83 F0         [24] 1537 	mov	b, dph
      004B2B 90 05 D5         [24] 1538 	mov	dptr,#_frame_at
      004B2E F0               [24] 1539 	movx	@dptr,a
      004B2F E5 F0            [12] 1540 	mov	a,b
      004B31 A3               [24] 1541 	inc	dptr
      004B32 F0               [24] 1542 	movx	@dptr,a
                                   1543 ;	keyboards/ajazz/ak820/ak820_rgb.c:155: phase += (uint16_t)rgb_matrix_config.speed + 32;
      004B33 90 05 CC         [24] 1544 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      004B36 E0               [24] 1545 	movx	a,@dptr
      004B37 FF               [12] 1546 	mov	r7,a
      004B38 7E 00            [12] 1547 	mov	r6,#0x00
      004B3A 74 20            [12] 1548 	mov	a,#0x20
      004B3C 2F               [12] 1549 	add	a, r7
      004B3D FF               [12] 1550 	mov	r7,a
      004B3E E4               [12] 1551 	clr	a
      004B3F 3E               [12] 1552 	addc	a, r6
      004B40 FE               [12] 1553 	mov	r6,a
      004B41 90 05 D7         [24] 1554 	mov	dptr,#_phase
      004B44 E0               [24] 1555 	movx	a,@dptr
      004B45 FC               [12] 1556 	mov	r4,a
      004B46 A3               [24] 1557 	inc	dptr
      004B47 E0               [24] 1558 	movx	a,@dptr
      004B48 FD               [12] 1559 	mov	r5,a
      004B49 EF               [12] 1560 	mov	a,r7
      004B4A 2C               [12] 1561 	add	a, r4
      004B4B FF               [12] 1562 	mov	r7,a
      004B4C EE               [12] 1563 	mov	a,r6
      004B4D 3D               [12] 1564 	addc	a, r5
      004B4E FE               [12] 1565 	mov	r6,a
      004B4F 90 05 D7         [24] 1566 	mov	dptr,#_phase
      004B52 EF               [12] 1567 	mov	a,r7
      004B53 F0               [24] 1568 	movx	@dptr,a
      004B54 EE               [12] 1569 	mov	a,r6
      004B55 A3               [24] 1570 	inc	dptr
      004B56 F0               [24] 1571 	movx	@dptr,a
                                   1572 ;	keyboards/ajazz/ak820/ak820_rgb.c:156: frame_phase = phase >> 8;
      004B57 90 05 D7         [24] 1573 	mov	dptr,#_phase
      004B5A E0               [24] 1574 	movx	a,@dptr
      004B5B A3               [24] 1575 	inc	dptr
      004B5C E0               [24] 1576 	movx	a,@dptr
      004B5D FF               [12] 1577 	mov	r7,a
      004B5E 90 05 DF         [24] 1578 	mov	dptr,#_frame_phase
      004B61 F0               [24] 1579 	movx	@dptr,a
                                   1580 ;	keyboards/ajazz/ak820/ak820_rgb.c:157: frame_mode = suspended || !rgb_matrix_config.enable ? RGB_MATRIX_NONE : rgb_matrix_config.mode;
      004B62 90 05 D0         [24] 1581 	mov	dptr,#_suspended
      004B65 E0               [24] 1582 	movx	a,@dptr
      004B66 70 08            [24] 1583 	jnz	00134$
      004B68 90 05 C8         [24] 1584 	mov	dptr,#_rgb_matrix_config
      004B6B E0               [24] 1585 	movx	a,@dptr
      004B6C 54 03            [12] 1586 	anl	a,#0x03
      004B6E 70 04            [24] 1587 	jnz	00131$
      004B70                       1588 00134$:
      004B70 7E 00            [12] 1589 	mov	r6,#0x00
      004B72 80 09            [24] 1590 	sjmp	00132$
      004B74                       1591 00131$:
      004B74 90 05 C8         [24] 1592 	mov	dptr,#_rgb_matrix_config
      004B77 E0               [24] 1593 	movx	a,@dptr
      004B78 03               [12] 1594 	rr	a
      004B79 03               [12] 1595 	rr	a
      004B7A 54 3F            [12] 1596 	anl	a,#0x3f
      004B7C FE               [12] 1597 	mov	r6,a
      004B7D                       1598 00132$:
      004B7D 90 05 DA         [24] 1599 	mov	dptr,#_frame_mode
      004B80 EE               [12] 1600 	mov	a,r6
      004B81 F0               [24] 1601 	movx	@dptr,a
                                   1602 ;	keyboards/ajazz/ak820/ak820_rgb.c:158: frame_hue = rgb_matrix_config.hsv.h;
      004B82 90 05 C9         [24] 1603 	mov	dptr,#(_rgb_matrix_config + 0x0001)
      004B85 E0               [24] 1604 	movx	a,@dptr
      004B86 90 05 DB         [24] 1605 	mov	dptr,#_frame_hue
      004B89 F0               [24] 1606 	movx	@dptr,a
                                   1607 ;	keyboards/ajazz/ak820/ak820_rgb.c:159: frame_sat = rgb_matrix_config.hsv.s;
      004B8A 90 05 CA         [24] 1608 	mov	dptr,#(_rgb_matrix_config + 0x0002)
      004B8D E0               [24] 1609 	movx	a,@dptr
      004B8E 90 05 DC         [24] 1610 	mov	dptr,#_frame_sat
      004B91 F0               [24] 1611 	movx	@dptr,a
                                   1612 ;	keyboards/ajazz/ak820/ak820_rgb.c:160: frame_val = rgb_matrix_config.hsv.v;
      004B92 90 05 CB         [24] 1613 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      004B95 E0               [24] 1614 	movx	a,@dptr
      004B96 FD               [12] 1615 	mov	r5,a
      004B97 90 05 DD         [24] 1616 	mov	dptr,#_frame_val
      004B9A F0               [24] 1617 	movx	@dptr,a
                                   1618 ;	keyboards/ajazz/ak820/ak820_rgb.c:161: frame_flags = rgb_matrix_config.flags;
      004B9B 90 05 CD         [24] 1619 	mov	dptr,#(_rgb_matrix_config + 0x0005)
      004B9E E0               [24] 1620 	movx	a,@dptr
      004B9F 90 05 DE         [24] 1621 	mov	dptr,#_frame_flags
      004BA2 F0               [24] 1622 	movx	@dptr,a
                                   1623 ;	keyboards/ajazz/ak820/ak820_rgb.c:162: if (frame_mode == RGB_MATRIX_BREATHING) {
      004BA3 BE 02 26         [24] 1624 	cjne	r6,#0x02,00107$
                                   1625 ;	keyboards/ajazz/ak820/ak820_rgb.c:163: frame_val = ((uint16_t)frame_val * sine8(frame_phase - 64)) >> 8;
      004BA6 EF               [12] 1626 	mov	a,r7
      004BA7 24 C0            [12] 1627 	add	a,#0xc0
      004BA9 F5 82            [12] 1628 	mov	dpl,a
      004BAB C0 05            [24] 1629 	push	ar5
      004BAD 12 4A 27         [24] 1630 	lcall	_sine8
      004BB0 AF 82            [24] 1631 	mov	r7, dpl
      004BB2 D0 05            [24] 1632 	pop	ar5
      004BB4 8D F0            [24] 1633 	mov	b,r5
      004BB6 EF               [12] 1634 	mov	a,r7
      004BB7 A4               [48] 1635 	mul	ab
      004BB8 AE F0            [24] 1636 	mov	r6,b
      004BBA 8E 05            [24] 1637 	mov	ar5,r6
      004BBC 90 05 DD         [24] 1638 	mov	dptr,#_frame_val
      004BBF ED               [12] 1639 	mov	a,r5
      004BC0 F0               [24] 1640 	movx	@dptr,a
                                   1641 ;	keyboards/ajazz/ak820/ak820_rgb.c:165: frame_val = breathing_cie(frame_val);
      004BC1 8D 82            [24] 1642 	mov	dpl, r5
      004BC3 12 4A A5         [24] 1643 	lcall	_breathing_cie
      004BC6 E5 82            [12] 1644 	mov	a, dpl
      004BC8 90 05 DD         [24] 1645 	mov	dptr,#_frame_val
      004BCB F0               [24] 1646 	movx	@dptr,a
      004BCC                       1647 00107$:
                                   1648 ;	keyboards/ajazz/ak820/ak820_rgb.c:168: led_index = 0;
      004BCC 90 05 D9         [24] 1649 	mov	dptr,#_led_index
      004BCF E4               [12] 1650 	clr	a
      004BD0 F0               [24] 1651 	movx	@dptr,a
                                   1652 ;	keyboards/ajazz/ak820/ak820_rgb.c:169: rendering = true;
      004BD1 90 05 D2         [24] 1653 	mov	dptr,#_rendering
      004BD4 04               [12] 1654 	inc	a
      004BD5 F0               [24] 1655 	movx	@dptr,a
      004BD6                       1656 00109$:
                                   1657 ;	keyboards/ajazz/ak820/ak820_rgb.c:171: end = led_index + 8;
      004BD6 90 05 D9         [24] 1658 	mov	dptr,#_led_index
      004BD9 E0               [24] 1659 	movx	a,@dptr
      004BDA 24 08            [12] 1660 	add	a,#0x08
      004BDC FF               [12] 1661 	mov	r7,a
      004BDD 90 06 44         [24] 1662 	mov	dptr,#_rgb_matrix_task_end_10000_282
      004BE0 F0               [24] 1663 	movx	@dptr,a
                                   1664 ;	keyboards/ajazz/ak820/ak820_rgb.c:172: if (end > RGB_MATRIX_LED_COUNT) end = RGB_MATRIX_LED_COUNT;
      004BE1 EF               [12] 1665 	mov	a,r7
      004BE2 24 AD            [12] 1666 	add	a,#0xff - 0x52
      004BE4 50 06            [24] 1667 	jnc	00169$
                                   1668 ;	free result
      004BE6 90 06 44         [24] 1669 	mov	dptr,#_rgb_matrix_task_end_10000_282
      004BE9 74 52            [12] 1670 	mov	a,#0x52
      004BEB F0               [24] 1671 	movx	@dptr,a
                                   1672 ;	keyboards/ajazz/ak820/ak820_rgb.c:173: while (led_index < end) {
      004BEC                       1673 00169$:
      004BEC 90 06 44         [24] 1674 	mov	dptr,#_rgb_matrix_task_end_10000_282
      004BEF E0               [24] 1675 	movx	a,@dptr
      004BF0 FF               [12] 1676 	mov	r7,a
      004BF1                       1677 00124$:
      004BF1 90 05 D9         [24] 1678 	mov	dptr,#_led_index
      004BF4 E0               [24] 1679 	movx	a,@dptr
      004BF5 FE               [12] 1680 	mov	r6,a
      004BF6 C3               [12] 1681 	clr	c
      004BF7 9F               [12] 1682 	subb	a,r7
      004BF8 40 03            [24] 1683 	jc	00260$
      004BFA 02 4D B9         [24] 1684 	ljmp	00126$
      004BFD                       1685 00260$:
                                   1686 ;	keyboards/ajazz/ak820/ak820_rgb.c:174: if (!frame_mode || !(LED_FLAG_KEYLIGHT & frame_flags)) {
      004BFD 90 05 DA         [24] 1687 	mov	dptr,#_frame_mode
      004C00 E0               [24] 1688 	movx	a,@dptr
      004C01 60 07            [24] 1689 	jz	00120$
      004C03 90 05 DE         [24] 1690 	mov	dptr,#_frame_flags
      004C06 E0               [24] 1691 	movx	a,@dptr
      004C07 20 E2 22         [24] 1692 	jb	acc.2,00121$
      004C0A                       1693 00120$:
                                   1694 ;	keyboards/ajazz/ak820/ak820_rgb.c:175: rgb_matrix_set_color(led_index, 0, 0, 0);
      004C0A 90 05 D9         [24] 1695 	mov	dptr,#_led_index
      004C0D E0               [24] 1696 	movx	a,@dptr
      004C0E FC               [12] 1697 	mov	r4,a
      004C0F 7D 00            [12] 1698 	mov	r5,#0x00
      004C11 90 06 38         [24] 1699 	mov	dptr,#_rgb_matrix_set_color_PARM_2
      004C14 E4               [12] 1700 	clr	a
      004C15 F0               [24] 1701 	movx	@dptr,a
      004C16 90 06 39         [24] 1702 	mov	dptr,#_rgb_matrix_set_color_PARM_3
      004C19 F0               [24] 1703 	movx	@dptr,a
      004C1A 90 06 3A         [24] 1704 	mov	dptr,#_rgb_matrix_set_color_PARM_4
      004C1D F0               [24] 1705 	movx	@dptr,a
      004C1E 8C 82            [24] 1706 	mov	dpl, r4
      004C20 8D 83            [24] 1707 	mov	dph, r5
      004C22 C0 07            [24] 1708 	push	ar7
      004C24 12 49 93         [24] 1709 	lcall	_rgb_matrix_set_color
      004C27 D0 07            [24] 1710 	pop	ar7
      004C29 02 4D AF         [24] 1711 	ljmp	00122$
      004C2C                       1712 00121$:
                                   1713 ;	keyboards/ajazz/ak820/ak820_rgb.c:177: hsv.h = frame_hue;
      004C2C 90 05 DB         [24] 1714 	mov	dptr,#_frame_hue
      004C2F E0               [24] 1715 	movx	a,@dptr
      004C30 90 06 45         [24] 1716 	mov	dptr,#_rgb_matrix_task_hsv_10000_282
      004C33 F0               [24] 1717 	movx	@dptr,a
                                   1718 ;	keyboards/ajazz/ak820/ak820_rgb.c:178: hsv.s = frame_sat;
      004C34 90 05 DC         [24] 1719 	mov	dptr,#_frame_sat
      004C37 E0               [24] 1720 	movx	a,@dptr
      004C38 90 06 46         [24] 1721 	mov	dptr,#(_rgb_matrix_task_hsv_10000_282 + 0x0001)
      004C3B F0               [24] 1722 	movx	@dptr,a
                                   1723 ;	keyboards/ajazz/ak820/ak820_rgb.c:179: hsv.v = frame_val;
      004C3C 90 05 DD         [24] 1724 	mov	dptr,#_frame_val
      004C3F E0               [24] 1725 	movx	a,@dptr
      004C40 90 06 47         [24] 1726 	mov	dptr,#(_rgb_matrix_task_hsv_10000_282 + 0x0002)
      004C43 F0               [24] 1727 	movx	@dptr,a
                                   1728 ;	keyboards/ajazz/ak820/ak820_rgb.c:180: if (frame_mode == RGB_MATRIX_CYCLE_ALL) hsv.h += frame_phase;
      004C44 90 05 DA         [24] 1729 	mov	dptr,#_frame_mode
      004C47 E0               [24] 1730 	movx	a,@dptr
      004C48 FD               [12] 1731 	mov	r5,a
      004C49 BD 03 0E         [24] 1732 	cjne	r5,#0x03,00113$
      004C4C 90 06 45         [24] 1733 	mov	dptr,#_rgb_matrix_task_hsv_10000_282
      004C4F E0               [24] 1734 	movx	a,@dptr
      004C50 FD               [12] 1735 	mov	r5,a
      004C51 90 05 DF         [24] 1736 	mov	dptr,#_frame_phase
      004C54 E0               [24] 1737 	movx	a,@dptr
      004C55 2D               [12] 1738 	add	a, r5
      004C56 90 06 45         [24] 1739 	mov	dptr,#_rgb_matrix_task_hsv_10000_282
      004C59 F0               [24] 1740 	movx	@dptr,a
      004C5A                       1741 00113$:
                                   1742 ;	keyboards/ajazz/ak820/ak820_rgb.c:181: if (frame_mode == RGB_MATRIX_CYCLE_LEFT_RIGHT) hsv.h += ak820_led_points[led_index].x - frame_phase;
      004C5A 90 05 DA         [24] 1743 	mov	dptr,#_frame_mode
      004C5D E0               [24] 1744 	movx	a,@dptr
      004C5E FD               [12] 1745 	mov	r5,a
      004C5F BD 04 27         [24] 1746 	cjne	r5,#0x04,00115$
      004C62 90 06 45         [24] 1747 	mov	dptr,#_rgb_matrix_task_hsv_10000_282
      004C65 E0               [24] 1748 	movx	a,@dptr
      004C66 FD               [12] 1749 	mov	r5,a
      004C67 90 05 D9         [24] 1750 	mov	dptr,#_led_index
      004C6A E0               [24] 1751 	movx	a,@dptr
      004C6B 75 F0 02         [24] 1752 	mov	b,#0x02
      004C6E A4               [48] 1753 	mul	ab
      004C6F 24 5E            [12] 1754 	add	a, #_ak820_led_points
      004C71 F5 82            [12] 1755 	mov	dpl,a
      004C73 74 B8            [12] 1756 	mov	a,#(_ak820_led_points >> 8)
      004C75 35 F0            [12] 1757 	addc	a, b
      004C77 F5 83            [12] 1758 	mov	dph,a
      004C79 E4               [12] 1759 	clr	a
      004C7A 93               [24] 1760 	movc	a,@a+dptr
      004C7B FC               [12] 1761 	mov	r4,a
      004C7C 90 05 DF         [24] 1762 	mov	dptr,#_frame_phase
      004C7F E0               [24] 1763 	movx	a,@dptr
      004C80 FB               [12] 1764 	mov	r3,a
      004C81 EC               [12] 1765 	mov	a,r4
      004C82 C3               [12] 1766 	clr	c
      004C83 9B               [12] 1767 	subb	a,r3
      004C84 2D               [12] 1768 	add	a, r5
      004C85 90 06 45         [24] 1769 	mov	dptr,#_rgb_matrix_task_hsv_10000_282
      004C88 F0               [24] 1770 	movx	@dptr,a
      004C89                       1771 00115$:
                                   1772 ;	keyboards/ajazz/ak820/ak820_rgb.c:182: if (frame_mode == RGB_MATRIX_SOLID_REACTIVE_SIMPLE) {
      004C89 90 05 DA         [24] 1773 	mov	dptr,#_frame_mode
      004C8C E0               [24] 1774 	movx	a,@dptr
      004C8D FD               [12] 1775 	mov	r5,a
      004C8E BD 06 5A         [24] 1776 	cjne	r5,#0x06,00117$
                                   1777 ;	keyboards/ajazz/ak820/ak820_rgb.c:184: uint8_t shift = 7 - (rgb_matrix_config.speed >> 6);
      004C91 90 05 CC         [24] 1778 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      004C94 E0               [24] 1779 	movx	a,@dptr
      004C95 23               [12] 1780 	rl	a
      004C96 23               [12] 1781 	rl	a
      004C97 54 03            [12] 1782 	anl	a,#0x03
      004C99 FD               [12] 1783 	mov	r5,a
      004C9A 74 07            [12] 1784 	mov	a,#0x07
      004C9C C3               [12] 1785 	clr	c
      004C9D 9D               [12] 1786 	subb	a,r5
      004C9E FD               [12] 1787 	mov	r5,a
                                   1788 ;	keyboards/ajazz/ak820/ak820_rgb.c:185: uint8_t duration = 1 << shift;
      004C9F 8D F0            [24] 1789 	mov	b,r5
      004CA1 05 F0            [12] 1790 	inc	b
      004CA3 74 01            [12] 1791 	mov	a,#0x01
      004CA5 80 02            [24] 1792 	sjmp	00270$
      004CA7                       1793 00269$:
      004CA7 25 E0            [12] 1794 	add	a,acc
      004CA9                       1795 00270$:
      004CA9 D5 F0 FB         [24] 1796 	djnz	b,00269$
      004CAC FC               [12] 1797 	mov	r4,a
                                   1798 ;	keyboards/ajazz/ak820/ak820_rgb.c:186: uint8_t age = reactive_age[led_index];
      004CAD 90 05 D9         [24] 1799 	mov	dptr,#_led_index
      004CB0 E0               [24] 1800 	movx	a,@dptr
      004CB1 24 E0            [12] 1801 	add	a, #_reactive_age
      004CB3 F5 82            [12] 1802 	mov	dpl,a
      004CB5 E4               [12] 1803 	clr	a
      004CB6 34 05            [12] 1804 	addc	a, #(_reactive_age >> 8)
      004CB8 F5 83            [12] 1805 	mov	dph,a
      004CBA E0               [24] 1806 	movx	a,@dptr
                                   1807 ;	keyboards/ajazz/ak820/ak820_rgb.c:187: hsv.v = age >= duration ? frame_val : ((uint16_t)frame_val * age) >> shift;
      004CBB FB               [12] 1808 	mov	r3,a
      004CBC C3               [12] 1809 	clr	c
      004CBD 9C               [12] 1810 	subb	a,r4
      004CBE 40 07            [24] 1811 	jc	00136$
      004CC0 90 05 DD         [24] 1812 	mov	dptr,#_frame_val
      004CC3 E0               [24] 1813 	movx	a,@dptr
      004CC4 FA               [12] 1814 	mov	r2,a
      004CC5 80 1F            [24] 1815 	sjmp	00137$
      004CC7                       1816 00136$:
      004CC7 90 05 DD         [24] 1817 	mov	dptr,#_frame_val
      004CCA E0               [24] 1818 	movx	a,@dptr
      004CCB F5 F0            [12] 1819 	mov	b, a
      004CCD EB               [12] 1820 	mov	a,r3
      004CCE A4               [48] 1821 	mul	ab
      004CCF F9               [12] 1822 	mov	r1,a
      004CD0 AB F0            [24] 1823 	mov	r3,b
      004CD2 8D F0            [24] 1824 	mov	b,r5
      004CD4 05 F0            [12] 1825 	inc	b
      004CD6 AA 01            [24] 1826 	mov	r2,ar1
      004CD8 AC 03            [24] 1827 	mov	r4,ar3
      004CDA 80 07            [24] 1828 	sjmp	00273$
      004CDC                       1829 00272$:
      004CDC C3               [12] 1830 	clr	c
      004CDD EC               [12] 1831 	mov	a,r4
      004CDE 13               [12] 1832 	rrc	a
      004CDF FC               [12] 1833 	mov	r4,a
      004CE0 EA               [12] 1834 	mov	a,r2
      004CE1 13               [12] 1835 	rrc	a
      004CE2 FA               [12] 1836 	mov	r2,a
      004CE3                       1837 00273$:
      004CE3 D5 F0 F6         [24] 1838 	djnz	b,00272$
      004CE6                       1839 00137$:
      004CE6 90 06 47         [24] 1840 	mov	dptr,#(_rgb_matrix_task_hsv_10000_282 + 0x0002)
      004CE9 EA               [12] 1841 	mov	a,r2
      004CEA F0               [24] 1842 	movx	@dptr,a
      004CEB                       1843 00117$:
                                   1844 ;	keyboards/ajazz/ak820/ak820_rgb.c:189: if (frame_mode == RGB_MATRIX_VIALRGB_DIRECT) {
      004CEB 90 05 DA         [24] 1845 	mov	dptr,#_frame_mode
      004CEE E0               [24] 1846 	movx	a,@dptr
      004CEF FD               [12] 1847 	mov	r5,a
      004CF0 BD 05 4C         [24] 1848 	cjne	r5,#0x05,00119$
                                   1849 ;	keyboards/ajazz/ak820/ak820_rgb.c:190: hsv.h = g_direct_mode_colors[led_index].h;
      004CF3 90 05 D9         [24] 1850 	mov	dptr,#_led_index
      004CF6 E0               [24] 1851 	movx	a,@dptr
      004CF7 75 F0 03         [24] 1852 	mov	b,#0x03
      004CFA A4               [48] 1853 	mul	ab
      004CFB 24 7B            [12] 1854 	add	a, #_g_direct_mode_colors
      004CFD F5 82            [12] 1855 	mov	dpl,a
      004CFF 74 0A            [12] 1856 	mov	a,#(_g_direct_mode_colors >> 8)
      004D01 35 F0            [12] 1857 	addc	a, b
      004D03 F5 83            [12] 1858 	mov	dph,a
      004D05 E0               [24] 1859 	movx	a,@dptr
      004D06 90 06 45         [24] 1860 	mov	dptr,#_rgb_matrix_task_hsv_10000_282
      004D09 F0               [24] 1861 	movx	@dptr,a
                                   1862 ;	keyboards/ajazz/ak820/ak820_rgb.c:191: hsv.s = g_direct_mode_colors[led_index].s;
      004D0A 90 05 D9         [24] 1863 	mov	dptr,#_led_index
      004D0D E0               [24] 1864 	movx	a,@dptr
      004D0E 75 F0 03         [24] 1865 	mov	b,#0x03
      004D11 A4               [48] 1866 	mul	ab
      004D12 24 7B            [12] 1867 	add	a, #_g_direct_mode_colors
      004D14 FC               [12] 1868 	mov	r4,a
      004D15 74 0A            [12] 1869 	mov	a,#(_g_direct_mode_colors >> 8)
      004D17 35 F0            [12] 1870 	addc	a, b
      004D19 FD               [12] 1871 	mov	r5,a
      004D1A 8C 82            [24] 1872 	mov	dpl,r4
      004D1C 8D 83            [24] 1873 	mov	dph,r5
      004D1E A3               [24] 1874 	inc	dptr
      004D1F E0               [24] 1875 	movx	a,@dptr
      004D20 90 06 46         [24] 1876 	mov	dptr,#(_rgb_matrix_task_hsv_10000_282 + 0x0001)
      004D23 F0               [24] 1877 	movx	@dptr,a
                                   1878 ;	keyboards/ajazz/ak820/ak820_rgb.c:192: hsv.v = g_direct_mode_colors[led_index].v;
      004D24 90 05 D9         [24] 1879 	mov	dptr,#_led_index
      004D27 E0               [24] 1880 	movx	a,@dptr
      004D28 75 F0 03         [24] 1881 	mov	b,#0x03
      004D2B A4               [48] 1882 	mul	ab
      004D2C 24 7B            [12] 1883 	add	a, #_g_direct_mode_colors
      004D2E FC               [12] 1884 	mov	r4,a
      004D2F 74 0A            [12] 1885 	mov	a,#(_g_direct_mode_colors >> 8)
      004D31 35 F0            [12] 1886 	addc	a, b
      004D33 FD               [12] 1887 	mov	r5,a
      004D34 8C 82            [24] 1888 	mov	dpl,r4
      004D36 8D 83            [24] 1889 	mov	dph,r5
      004D38 A3               [24] 1890 	inc	dptr
      004D39 A3               [24] 1891 	inc	dptr
      004D3A E0               [24] 1892 	movx	a,@dptr
      004D3B 90 06 47         [24] 1893 	mov	dptr,#(_rgb_matrix_task_hsv_10000_282 + 0x0002)
      004D3E F0               [24] 1894 	movx	@dptr,a
      004D3F                       1895 00119$:
                                   1896 ;	keyboards/ajazz/ak820/ak820_rgb.c:197: hsv_to_rgb_into(hsv, frame_mode != RGB_MATRIX_BREATHING, &rgb);
      004D3F 90 05 DA         [24] 1897 	mov	dptr,#_frame_mode
      004D42 E0               [24] 1898 	movx	a,@dptr
      004D43 FD               [12] 1899 	mov	r5,a
      004D44 BD 02 03         [24] 1900 	cjne	r5,#0x02,00276$
      004D47 D3               [12] 1901 	setb	c
      004D48 80 01            [24] 1902 	sjmp	00277$
      004D4A                       1903 00276$:
      004D4A C3               [12] 1904 	clr	c
      004D4B                       1905 00277$:
      004D4B B3               [12] 1906 	cpl	c
      004D4C 92 07            [24] 1907 	mov	_rgb_matrix_task_sloc0_1_0,c
      004D4E 90 0B 8F         [24] 1908 	mov	dptr,#___memcpy_PARM_2
      004D51 74 45            [12] 1909 	mov	a,#_rgb_matrix_task_hsv_10000_282
      004D53 F0               [24] 1910 	movx	@dptr,a
      004D54 74 06            [12] 1911 	mov	a,#(_rgb_matrix_task_hsv_10000_282 >> 8)
      004D56 A3               [24] 1912 	inc	dptr
      004D57 F0               [24] 1913 	movx	@dptr,a
      004D58 E4               [12] 1914 	clr	a
      004D59 A3               [24] 1915 	inc	dptr
      004D5A F0               [24] 1916 	movx	@dptr,a
      004D5B 90 0B 92         [24] 1917 	mov	dptr,#___memcpy_PARM_3
      004D5E 74 03            [12] 1918 	mov	a,#0x03
      004D60 F0               [24] 1919 	movx	@dptr,a
      004D61 E4               [12] 1920 	clr	a
      004D62 A3               [24] 1921 	inc	dptr
      004D63 F0               [24] 1922 	movx	@dptr,a
      004D64 90 08 C1         [24] 1923 	mov	dptr,#_hsv_to_rgb_into_PARM_1
      004D67 F5 F0            [12] 1924 	mov	b,a
      004D69 C0 07            [24] 1925 	push	ar7
      004D6B 12 B4 9F         [24] 1926 	lcall	___memcpy
      004D6E 90 08 C4         [24] 1927 	mov	dptr,#_hsv_to_rgb_into_PARM_3
      004D71 74 48            [12] 1928 	mov	a,#_rgb_matrix_task_rgb_10000_282
      004D73 F0               [24] 1929 	movx	@dptr,a
      004D74 74 06            [12] 1930 	mov	a,#(_rgb_matrix_task_rgb_10000_282 >> 8)
      004D76 A3               [24] 1931 	inc	dptr
      004D77 F0               [24] 1932 	movx	@dptr,a
      004D78 A2 07            [12] 1933 	mov	c,_rgb_matrix_task_sloc0_1_0
      004D7A E4               [12] 1934 	clr	a
      004D7B 33               [12] 1935 	rlc	a
      004D7C F5 82            [12] 1936 	mov	dpl, a
      004D7E 12 79 2C         [24] 1937 	lcall	_hsv_to_rgb_into
                                   1938 ;	keyboards/ajazz/ak820/ak820_rgb.c:201: rgb_matrix_set_color(led_index, rgb.r, rgb.g, rgb.b);
      004D81 90 05 D9         [24] 1939 	mov	dptr,#_led_index
      004D84 E0               [24] 1940 	movx	a,@dptr
      004D85 FC               [12] 1941 	mov	r4,a
      004D86 7D 00            [12] 1942 	mov	r5,#0x00
      004D88 90 06 49         [24] 1943 	mov	dptr,#(_rgb_matrix_task_rgb_10000_282 + 0x0001)
      004D8B E0               [24] 1944 	movx	a,@dptr
      004D8C FB               [12] 1945 	mov	r3,a
      004D8D 90 06 48         [24] 1946 	mov	dptr,#_rgb_matrix_task_rgb_10000_282
      004D90 E0               [24] 1947 	movx	a,@dptr
      004D91 FA               [12] 1948 	mov	r2,a
      004D92 90 06 4A         [24] 1949 	mov	dptr,#(_rgb_matrix_task_rgb_10000_282 + 0x0002)
      004D95 E0               [24] 1950 	movx	a,@dptr
      004D96 F9               [12] 1951 	mov	r1,a
      004D97 90 06 38         [24] 1952 	mov	dptr,#_rgb_matrix_set_color_PARM_2
      004D9A EB               [12] 1953 	mov	a,r3
      004D9B F0               [24] 1954 	movx	@dptr,a
      004D9C 90 06 39         [24] 1955 	mov	dptr,#_rgb_matrix_set_color_PARM_3
      004D9F EA               [12] 1956 	mov	a,r2
      004DA0 F0               [24] 1957 	movx	@dptr,a
      004DA1 90 06 3A         [24] 1958 	mov	dptr,#_rgb_matrix_set_color_PARM_4
      004DA4 E9               [12] 1959 	mov	a,r1
      004DA5 F0               [24] 1960 	movx	@dptr,a
      004DA6 8C 82            [24] 1961 	mov	dpl, r4
      004DA8 8D 83            [24] 1962 	mov	dph, r5
      004DAA 12 49 93         [24] 1963 	lcall	_rgb_matrix_set_color
      004DAD D0 07            [24] 1964 	pop	ar7
      004DAF                       1965 00122$:
                                   1966 ;	keyboards/ajazz/ak820/ak820_rgb.c:203: ++led_index;
      004DAF 90 05 D9         [24] 1967 	mov	dptr,#_led_index
      004DB2 E0               [24] 1968 	movx	a,@dptr
      004DB3 24 01            [12] 1969 	add	a, #0x01
      004DB5 F0               [24] 1970 	movx	@dptr,a
      004DB6 02 4B F1         [24] 1971 	ljmp	00124$
      004DB9                       1972 00126$:
                                   1973 ;	keyboards/ajazz/ak820/ak820_rgb.c:205: if (led_index == RGB_MATRIX_LED_COUNT) {
      004DB9 BE 52 1E         [24] 1974 	cjne	r6,#0x52,00129$
                                   1975 ;	keyboards/ajazz/ak820/ak820_rgb.c:206: rgb_matrix_driver.flush();
      004DBC 90 B6 00         [24] 1976 	mov	dptr,#(_rgb_matrix_driver + 0x0006)
      004DBF E4               [12] 1977 	clr	a
      004DC0 93               [24] 1978 	movc	a,@a+dptr
      004DC1 FE               [12] 1979 	mov	r6,a
      004DC2 A3               [24] 1980 	inc	dptr
      004DC3 E4               [12] 1981 	clr	a
      004DC4 93               [24] 1982 	movc	a,@a+dptr
      004DC5 FF               [12] 1983 	mov	r7,a
      004DC6 C0 07            [24] 1984 	push	ar7
      004DC8 C0 06            [24] 1985 	push	ar6
      004DCA 8E 82            [24] 1986 	mov	dpl,r6
      004DCC 8F 83            [24] 1987 	mov	dph,r7
      004DCE 12 30 75         [24] 1988 	lcall	__sdcc_call_dptr
      004DD1 D0 06            [24] 1989 	pop	ar6
      004DD3 D0 07            [24] 1990 	pop	ar7
                                   1991 ;	keyboards/ajazz/ak820/ak820_rgb.c:207: rendering = false;
      004DD5 90 05 D2         [24] 1992 	mov	dptr,#_rendering
      004DD8 E4               [12] 1993 	clr	a
      004DD9 F0               [24] 1994 	movx	@dptr,a
      004DDA                       1995 00129$:
                                   1996 ;	keyboards/ajazz/ak820/ak820_rgb.c:209: }
      004DDA 22               [24] 1997 	ret
                                   1998 ;------------------------------------------------------------
                                   1999 ;Allocation info for local variables in function 'process_rgb_matrix'
                                   2000 ;------------------------------------------------------------
                                   2001 ;col           Allocated with name '_process_rgb_matrix_PARM_2'
                                   2002 ;pressed       Allocated with name '_process_rgb_matrix_PARM_3'
                                   2003 ;row           Allocated with name '_process_rgb_matrix_row_10000_302'
                                   2004 ;i             Allocated with name '_process_rgb_matrix_i_10000_303'
                                   2005 ;slot          Allocated with name '_process_rgb_matrix_slot_10000_303'
                                   2006 ;------------------------------------------------------------
                                   2007 ;	keyboards/ajazz/ak820/ak820_rgb.c:211: void process_rgb_matrix(uint8_t row, uint8_t col, bool pressed) {
                                   2008 ;	-----------------------------------------
                                   2009 ;	 function process_rgb_matrix
                                   2010 ;	-----------------------------------------
      004DDB                       2011 _process_rgb_matrix:
      004DDB E5 82            [12] 2012 	mov	a,dpl
      004DDD 90 06 4D         [24] 2013 	mov	dptr,#_process_rgb_matrix_row_10000_302
      004DE0 F0               [24] 2014 	movx	@dptr,a
                                   2015 ;	keyboards/ajazz/ak820/ak820_rgb.c:213: if (!pressed || suspended || !rgb_matrix_config.enable ||
      004DE1 90 06 4C         [24] 2016 	mov	dptr,#_process_rgb_matrix_PARM_3
      004DE4 E0               [24] 2017 	movx	a,@dptr
      004DE5 60 2E            [24] 2018 	jz	00101$
      004DE7 90 05 D0         [24] 2019 	mov	dptr,#_suspended
      004DEA E0               [24] 2020 	movx	a,@dptr
      004DEB 70 28            [24] 2021 	jnz	00101$
      004DED 90 05 C8         [24] 2022 	mov	dptr,#_rgb_matrix_config
      004DF0 E0               [24] 2023 	movx	a,@dptr
      004DF1 54 03            [12] 2024 	anl	a,#0x03
      004DF3 60 20            [24] 2025 	jz	00101$
                                   2026 ;	keyboards/ajazz/ak820/ak820_rgb.c:214: rgb_matrix_config.mode != RGB_MATRIX_SOLID_REACTIVE_SIMPLE || row >= MATRIX_ROWS || col >= MATRIX_COLS) return;
      004DF5 90 05 C8         [24] 2027 	mov	dptr,#_rgb_matrix_config
      004DF8 E0               [24] 2028 	movx	a,@dptr
      004DF9 03               [12] 2029 	rr	a
      004DFA 03               [12] 2030 	rr	a
      004DFB 54 3F            [12] 2031 	anl	a,#0x3f
      004DFD FF               [12] 2032 	mov	r7,a
      004DFE BF 06 14         [24] 2033 	cjne	r7,#0x06,00101$
      004E01 90 06 4D         [24] 2034 	mov	dptr,#_process_rgb_matrix_row_10000_302
      004E04 E0               [24] 2035 	movx	a,@dptr
      004E05 FF               [12] 2036 	mov	r7,a
      004E06 BF 10 00         [24] 2037 	cjne	r7,#0x10,00169$
      004E09                       2038 00169$:
      004E09 50 0A            [24] 2039 	jnc	00101$
      004E0B 90 06 4B         [24] 2040 	mov	dptr,#_process_rgb_matrix_PARM_2
      004E0E E0               [24] 2041 	movx	a,@dptr
      004E0F FE               [12] 2042 	mov	r6,a
      004E10 BE 08 00         [24] 2043 	cjne	r6,#0x08,00171$
      004E13                       2044 00171$:
      004E13 40 01            [24] 2045 	jc	00102$
      004E15                       2046 00101$:
      004E15 22               [24] 2047 	ret
      004E16                       2048 00102$:
                                   2049 ;	keyboards/ajazz/ak820/ak820_rgb.c:215: age_reactive();
      004E16 C0 07            [24] 2050 	push	ar7
      004E18 C0 06            [24] 2051 	push	ar6
      004E1A 12 47 C0         [24] 2052 	lcall	_age_reactive
      004E1D D0 06            [24] 2053 	pop	ar6
      004E1F D0 07            [24] 2054 	pop	ar7
                                   2055 ;	keyboards/ajazz/ak820/ak820_rgb.c:216: slot = row * MATRIX_COLS + col;
      004E21 EF               [12] 2056 	mov	a,r7
      004E22 C4               [12] 2057 	swap	a
      004E23 03               [12] 2058 	rr	a
      004E24 54 F8            [12] 2059 	anl	a,#0xf8
      004E26 2E               [12] 2060 	add	a,r6
      004E27 FF               [12] 2061 	mov	r7,a
                                   2062 ;	keyboards/ajazz/ak820/ak820_rgb.c:217: for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
      004E28 7E 00            [12] 2063 	mov	r6,#0x00
      004E2A                       2064 00111$:
                                   2065 ;	keyboards/ajazz/ak820/ak820_rgb.c:218: if (ak820_rgb_slots[i] == slot) {
      004E2A EE               [12] 2066 	mov	a,r6
      004E2B 90 B5 A8         [24] 2067 	mov	dptr,#_ak820_rgb_slots
      004E2E 93               [24] 2068 	movc	a,@a+dptr
      004E2F B5 07 2F         [24] 2069 	cjne	a,ar7,00112$
                                   2070 ;	keyboards/ajazz/ak820/ak820_rgb.c:219: reactive_age[i] = 128 >> (rgb_matrix_config.speed >> 6);
      004E32 EE               [12] 2071 	mov	a,r6
      004E33 24 E0            [12] 2072 	add	a, #_reactive_age
      004E35 FC               [12] 2073 	mov	r4,a
      004E36 E4               [12] 2074 	clr	a
      004E37 34 05            [12] 2075 	addc	a, #(_reactive_age >> 8)
      004E39 FD               [12] 2076 	mov	r5,a
      004E3A 90 05 CC         [24] 2077 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      004E3D E0               [24] 2078 	movx	a,@dptr
      004E3E 23               [12] 2079 	rl	a
      004E3F 23               [12] 2080 	rl	a
      004E40 54 03            [12] 2081 	anl	a,#0x03
      004E42 F5 F0            [12] 2082 	mov	b, a
      004E44 05 F0            [12] 2083 	inc	b
      004E46 7B 80            [12] 2084 	mov	r3,#0x80
      004E48 E4               [12] 2085 	clr	a
      004E49 FA               [12] 2086 	mov	r2,a
      004E4A 33               [12] 2087 	rlc	a
      004E4B 92 D2            [24] 2088 	mov	ov,c
      004E4D 80 08            [24] 2089 	sjmp	00176$
      004E4F                       2090 00175$:
      004E4F A2 D2            [12] 2091 	mov	c,ov
      004E51 EA               [12] 2092 	mov	a,r2
      004E52 13               [12] 2093 	rrc	a
      004E53 FA               [12] 2094 	mov	r2,a
      004E54 EB               [12] 2095 	mov	a,r3
      004E55 13               [12] 2096 	rrc	a
      004E56 FB               [12] 2097 	mov	r3,a
      004E57                       2098 00176$:
      004E57 D5 F0 F5         [24] 2099 	djnz	b,00175$
      004E5A 8C 82            [24] 2100 	mov	dpl,r4
      004E5C 8D 83            [24] 2101 	mov	dph,r5
      004E5E EB               [12] 2102 	mov	a,r3
      004E5F F0               [24] 2103 	movx	@dptr,a
                                   2104 ;	keyboards/ajazz/ak820/ak820_rgb.c:220: return;
      004E60 22               [24] 2105 	ret
      004E61                       2106 00112$:
                                   2107 ;	keyboards/ajazz/ak820/ak820_rgb.c:217: for (i = 0; i < RGB_MATRIX_LED_COUNT; ++i) {
      004E61 0E               [12] 2108 	inc	r6
      004E62 BE 52 00         [24] 2109 	cjne	r6,#0x52,00177$
      004E65                       2110 00177$:
      004E65 40 C3            [24] 2111 	jc	00111$
                                   2112 ;	keyboards/ajazz/ak820/ak820_rgb.c:223: }
      004E67 22               [24] 2113 	ret
                                   2114 ;------------------------------------------------------------
                                   2115 ;Allocation info for local variables in function 'rgb_matrix_set_suspend_state'
                                   2116 ;------------------------------------------------------------
                                   2117 ;state         Allocated with name '_rgb_matrix_set_suspend_state_state_10000_309'
                                   2118 ;------------------------------------------------------------
                                   2119 ;	keyboards/ajazz/ak820/ak820_rgb.c:225: void rgb_matrix_set_suspend_state(bool state) {
                                   2120 ;	-----------------------------------------
                                   2121 ;	 function rgb_matrix_set_suspend_state
                                   2122 ;	-----------------------------------------
      004E68                       2123 _rgb_matrix_set_suspend_state:
      004E68 E5 82            [12] 2124 	mov	a,dpl
      004E6A 90 06 4E         [24] 2125 	mov	dptr,#_rgb_matrix_set_suspend_state_state_10000_309
      004E6D F0               [24] 2126 	movx	@dptr,a
                                   2127 ;	keyboards/ajazz/ak820/ak820_rgb.c:226: suspended = state;
      004E6E E0               [24] 2128 	movx	a,@dptr
      004E6F FF               [12] 2129 	mov	r7,a
      004E70 90 05 D0         [24] 2130 	mov	dptr,#_suspended
      004E73 F0               [24] 2131 	movx	@dptr,a
                                   2132 ;	keyboards/ajazz/ak820/ak820_rgb.c:227: rendering = false;
      004E74 90 05 D2         [24] 2133 	mov	dptr,#_rendering
      004E77 E4               [12] 2134 	clr	a
      004E78 F0               [24] 2135 	movx	@dptr,a
                                   2136 ;	keyboards/ajazz/ak820/ak820_rgb.c:228: clear_reactive();
      004E79 C0 07            [24] 2137 	push	ar7
      004E7B 12 47 99         [24] 2138 	lcall	_clear_reactive
      004E7E D0 07            [24] 2139 	pop	ar7
                                   2140 ;	keyboards/ajazz/ak820/ak820_rgb.c:229: if (state) {
      004E80 EF               [12] 2141 	mov	a,r7
      004E81 60 28            [24] 2142 	jz	00103$
                                   2143 ;	keyboards/ajazz/ak820/ak820_rgb.c:230: rgb_matrix_set_color_all(0, 0, 0);
      004E83 90 06 3D         [24] 2144 	mov	dptr,#_rgb_matrix_set_color_all_PARM_2
      004E86 E4               [12] 2145 	clr	a
      004E87 F0               [24] 2146 	movx	@dptr,a
      004E88 90 06 3E         [24] 2147 	mov	dptr,#_rgb_matrix_set_color_all_PARM_3
      004E8B F0               [24] 2148 	movx	@dptr,a
      004E8C 75 82 00         [24] 2149 	mov	dpl, #0x00
      004E8F 12 49 ED         [24] 2150 	lcall	_rgb_matrix_set_color_all
                                   2151 ;	keyboards/ajazz/ak820/ak820_rgb.c:231: rgb_matrix_driver.flush();
      004E92 90 B6 00         [24] 2152 	mov	dptr,#(_rgb_matrix_driver + 0x0006)
      004E95 E4               [12] 2153 	clr	a
      004E96 93               [24] 2154 	movc	a,@a+dptr
      004E97 FE               [12] 2155 	mov	r6,a
      004E98 A3               [24] 2156 	inc	dptr
      004E99 E4               [12] 2157 	clr	a
      004E9A 93               [24] 2158 	movc	a,@a+dptr
      004E9B FF               [12] 2159 	mov	r7,a
      004E9C C0 07            [24] 2160 	push	ar7
      004E9E C0 06            [24] 2161 	push	ar6
      004EA0 8E 82            [24] 2162 	mov	dpl,r6
      004EA2 8F 83            [24] 2163 	mov	dph,r7
      004EA4 12 30 75         [24] 2164 	lcall	__sdcc_call_dptr
      004EA7 D0 06            [24] 2165 	pop	ar6
      004EA9 D0 07            [24] 2166 	pop	ar7
      004EAB                       2167 00103$:
                                   2168 ;	keyboards/ajazz/ak820/ak820_rgb.c:233: }
      004EAB 22               [24] 2169 	ret
                                   2170 ;------------------------------------------------------------
                                   2171 ;Allocation info for local variables in function 'rgb_matrix_get_suspend_state'
                                   2172 ;------------------------------------------------------------
                                   2173 ;	keyboards/ajazz/ak820/ak820_rgb.c:235: bool rgb_matrix_get_suspend_state(void) { return suspended; }
                                   2174 ;	-----------------------------------------
                                   2175 ;	 function rgb_matrix_is_enabled
                                   2176 ;	-----------------------------------------
      004EAC                       2177 _rgb_matrix_is_enabled:
      004EAC 90 05 C8         [24] 2178 	mov	dptr,#_rgb_matrix_config
      004EAF E0               [24] 2179 	movx	a,@dptr
      004EB0 54 03            [12] 2180 	anl	a,#0x03
      004EB2 F5 82            [12] 2181 	mov	dpl,a
      004EB4 22               [24] 2182 	ret
                                   2183 ;------------------------------------------------------------
                                   2184 ;Allocation info for local variables in function 'rgb_matrix_get_mode'
                                   2185 ;------------------------------------------------------------
                                   2186 ;	keyboards/ajazz/ak820/ak820_rgb.c:237: uint8_t rgb_matrix_get_mode(void) { return rgb_matrix_config.mode; }
                                   2187 ;	-----------------------------------------
                                   2188 ;	 function rgb_matrix_get_mode
                                   2189 ;	-----------------------------------------
      004EB5                       2190 _rgb_matrix_get_mode:
      004EB5 90 05 C8         [24] 2191 	mov	dptr,#_rgb_matrix_config
      004EB8 E0               [24] 2192 	movx	a,@dptr
      004EB9 03               [12] 2193 	rr	a
      004EBA 03               [12] 2194 	rr	a
      004EBB 54 3F            [12] 2195 	anl	a,#0x3f
      004EBD F5 82            [12] 2196 	mov	dpl,a
      004EBF 22               [24] 2197 	ret
                                   2198 ;------------------------------------------------------------
                                   2199 ;Allocation info for local variables in function 'rgb_matrix_get_hsv'
                                   2200 ;------------------------------------------------------------
                                   2201 ;	keyboards/ajazz/ak820/ak820_rgb.c:238: HSV rgb_matrix_get_hsv(void) { return rgb_matrix_config.hsv; }
                                   2202 ;	-----------------------------------------
                                   2203 ;	 function rgb_matrix_get_hue
                                   2204 ;	-----------------------------------------
      004EC0                       2205 _rgb_matrix_get_hue:
      004EC0 90 05 C9         [24] 2206 	mov	dptr,#(_rgb_matrix_config + 0x0001)
      004EC3 E0               [24] 2207 	movx	a,@dptr
      004EC4 F5 82            [12] 2208 	mov	dpl,a
      004EC6 22               [24] 2209 	ret
                                   2210 ;------------------------------------------------------------
                                   2211 ;Allocation info for local variables in function 'rgb_matrix_get_sat'
                                   2212 ;------------------------------------------------------------
                                   2213 ;	keyboards/ajazz/ak820/ak820_rgb.c:240: uint8_t rgb_matrix_get_sat(void) { return rgb_matrix_config.hsv.s; }
                                   2214 ;	-----------------------------------------
                                   2215 ;	 function rgb_matrix_get_sat
                                   2216 ;	-----------------------------------------
      004EC7                       2217 _rgb_matrix_get_sat:
      004EC7 90 05 CA         [24] 2218 	mov	dptr,#(_rgb_matrix_config + 0x0002)
      004ECA E0               [24] 2219 	movx	a,@dptr
      004ECB F5 82            [12] 2220 	mov	dpl,a
      004ECD 22               [24] 2221 	ret
                                   2222 ;------------------------------------------------------------
                                   2223 ;Allocation info for local variables in function 'rgb_matrix_get_val'
                                   2224 ;------------------------------------------------------------
                                   2225 ;	keyboards/ajazz/ak820/ak820_rgb.c:241: uint8_t rgb_matrix_get_val(void) { return rgb_matrix_config.hsv.v; }
                                   2226 ;	-----------------------------------------
                                   2227 ;	 function rgb_matrix_get_val
                                   2228 ;	-----------------------------------------
      004ECE                       2229 _rgb_matrix_get_val:
      004ECE 90 05 CB         [24] 2230 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      004ED1 E0               [24] 2231 	movx	a,@dptr
      004ED2 F5 82            [12] 2232 	mov	dpl,a
      004ED4 22               [24] 2233 	ret
                                   2234 ;------------------------------------------------------------
                                   2235 ;Allocation info for local variables in function 'rgb_matrix_get_speed'
                                   2236 ;------------------------------------------------------------
                                   2237 ;	keyboards/ajazz/ak820/ak820_rgb.c:242: uint8_t rgb_matrix_get_speed(void) { return rgb_matrix_config.speed; }
                                   2238 ;	-----------------------------------------
                                   2239 ;	 function rgb_matrix_get_speed
                                   2240 ;	-----------------------------------------
      004ED5                       2241 _rgb_matrix_get_speed:
      004ED5 90 05 CC         [24] 2242 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      004ED8 E0               [24] 2243 	movx	a,@dptr
      004ED9 F5 82            [12] 2244 	mov	dpl,a
      004EDB 22               [24] 2245 	ret
                                   2246 ;------------------------------------------------------------
                                   2247 ;Allocation info for local variables in function 'rgb_matrix_get_flags'
                                   2248 ;------------------------------------------------------------
                                   2249 ;	keyboards/ajazz/ak820/ak820_rgb.c:243: led_flags_t rgb_matrix_get_flags(void) { return rgb_matrix_config.flags; }
                                   2250 ;	-----------------------------------------
                                   2251 ;	 function rgb_matrix_toggle_noeeprom
                                   2252 ;	-----------------------------------------
      004EDC                       2253 _rgb_matrix_toggle_noeeprom:
      004EDC 90 05 C8         [24] 2254 	mov	dptr,#_rgb_matrix_config
      004EDF E0               [24] 2255 	movx	a,@dptr
      004EE0 54 03            [12] 2256 	anl	a,#0x03
      004EE2 FF               [12] 2257 	mov	r7,a
      004EE3 63 07 01         [24] 2258 	xrl	ar7,#0x01
      004EE6 90 05 C8         [24] 2259 	mov	dptr,#_rgb_matrix_config
      004EE9 EF               [12] 2260 	mov	a,r7
      004EEA 54 03            [12] 2261 	anl	a,#0x03
      004EEC F5 F0            [12] 2262 	mov	b,a
      004EEE E0               [24] 2263 	movx	a,@dptr
      004EEF 54 FC            [12] 2264 	anl	a,#0xfc
      004EF1 45 F0            [12] 2265 	orl	a,b
      004EF3 F0               [24] 2266 	movx	@dptr,a
      004EF4 90 05 D2         [24] 2267 	mov	dptr,#_rendering
      004EF7 E4               [12] 2268 	clr	a
      004EF8 F0               [24] 2269 	movx	@dptr,a
      004EF9 02 47 99         [24] 2270 	ljmp	_clear_reactive
                                   2271 ;------------------------------------------------------------
                                   2272 ;Allocation info for local variables in function 'rgb_matrix_enable_noeeprom'
                                   2273 ;------------------------------------------------------------
                                   2274 ;	keyboards/ajazz/ak820/ak820_rgb.c:246: void rgb_matrix_enable_noeeprom(void) { if (!rgb_matrix_config.enable) clear_reactive(); rgb_matrix_config.enable = 1; rendering = false; }
                                   2275 ;	-----------------------------------------
                                   2276 ;	 function rgb_matrix_enable_noeeprom
                                   2277 ;	-----------------------------------------
      004EFC                       2278 _rgb_matrix_enable_noeeprom:
      004EFC 90 05 C8         [24] 2279 	mov	dptr,#_rgb_matrix_config
      004EFF E0               [24] 2280 	movx	a,@dptr
      004F00 54 03            [12] 2281 	anl	a,#0x03
      004F02 70 03            [24] 2282 	jnz	00102$
      004F04 12 47 99         [24] 2283 	lcall	_clear_reactive
      004F07                       2284 00102$:
      004F07 90 05 C8         [24] 2285 	mov	dptr,#_rgb_matrix_config
      004F0A E0               [24] 2286 	movx	a,@dptr
      004F0B 54 FC            [12] 2287 	anl	a,#0xfc
      004F0D 44 01            [12] 2288 	orl	a,#0x01
      004F0F F0               [24] 2289 	movx	@dptr,a
      004F10 90 05 D2         [24] 2290 	mov	dptr,#_rendering
      004F13 E4               [12] 2291 	clr	a
      004F14 F0               [24] 2292 	movx	@dptr,a
      004F15 22               [24] 2293 	ret
                                   2294 ;------------------------------------------------------------
                                   2295 ;Allocation info for local variables in function 'rgb_matrix_disable_noeeprom'
                                   2296 ;------------------------------------------------------------
                                   2297 ;	keyboards/ajazz/ak820/ak820_rgb.c:247: void rgb_matrix_disable_noeeprom(void) { rgb_matrix_config.enable = 0; rendering = false; clear_reactive(); }
                                   2298 ;	-----------------------------------------
                                   2299 ;	 function rgb_matrix_disable_noeeprom
                                   2300 ;	-----------------------------------------
      004F16                       2301 _rgb_matrix_disable_noeeprom:
      004F16 90 05 C8         [24] 2302 	mov	dptr,#_rgb_matrix_config
      004F19 E0               [24] 2303 	movx	a,@dptr
      004F1A 54 FC            [12] 2304 	anl	a,#0xfc
      004F1C F0               [24] 2305 	movx	@dptr,a
      004F1D 90 05 D2         [24] 2306 	mov	dptr,#_rendering
      004F20 E4               [12] 2307 	clr	a
      004F21 F0               [24] 2308 	movx	@dptr,a
      004F22 02 47 99         [24] 2309 	ljmp	_clear_reactive
                                   2310 ;------------------------------------------------------------
                                   2311 ;Allocation info for local variables in function 'rgb_matrix_mode_noeeprom'
                                   2312 ;------------------------------------------------------------
                                   2313 ;mode          Allocated with name '_rgb_matrix_mode_noeeprom_mode_10000_338'
                                   2314 ;------------------------------------------------------------
                                   2315 ;	keyboards/ajazz/ak820/ak820_rgb.c:248: void rgb_matrix_mode_noeeprom(uint8_t mode) {
                                   2316 ;	-----------------------------------------
                                   2317 ;	 function rgb_matrix_mode_noeeprom
                                   2318 ;	-----------------------------------------
      004F25                       2319 _rgb_matrix_mode_noeeprom:
      004F25 E5 82            [12] 2320 	mov	a,dpl
      004F27 90 06 4F         [24] 2321 	mov	dptr,#_rgb_matrix_mode_noeeprom_mode_10000_338
      004F2A F0               [24] 2322 	movx	@dptr,a
                                   2323 ;	keyboards/ajazz/ak820/ak820_rgb.c:249: if (!mode || mode >= RGB_MATRIX_EFFECT_MAX) return;
      004F2B E0               [24] 2324 	movx	a,@dptr
      004F2C FF               [12] 2325 	mov	r7,a
      004F2D 60 05            [24] 2326 	jz	00101$
      004F2F BF 07 00         [24] 2327 	cjne	r7,#0x07,00123$
      004F32                       2328 00123$:
      004F32 40 01            [24] 2329 	jc	00102$
      004F34                       2330 00101$:
      004F34 22               [24] 2331 	ret
      004F35                       2332 00102$:
                                   2333 ;	keyboards/ajazz/ak820/ak820_rgb.c:250: if (mode != rgb_matrix_config.mode) clear_reactive();
      004F35 90 05 C8         [24] 2334 	mov	dptr,#_rgb_matrix_config
      004F38 E0               [24] 2335 	movx	a,@dptr
      004F39 03               [12] 2336 	rr	a
      004F3A 03               [12] 2337 	rr	a
      004F3B 54 3F            [12] 2338 	anl	a,#0x3f
      004F3D FE               [12] 2339 	mov	r6,a
      004F3E EF               [12] 2340 	mov	a,r7
      004F3F B5 06 02         [24] 2341 	cjne	a,ar6,00125$
      004F42 80 03            [24] 2342 	sjmp	00105$
      004F44                       2343 00125$:
      004F44 12 47 99         [24] 2344 	lcall	_clear_reactive
      004F47                       2345 00105$:
                                   2346 ;	keyboards/ajazz/ak820/ak820_rgb.c:251: rgb_matrix_config.mode = mode;
      004F47 90 06 4F         [24] 2347 	mov	dptr,#_rgb_matrix_mode_noeeprom_mode_10000_338
      004F4A E0               [24] 2348 	movx	a,@dptr
      004F4B 90 05 C8         [24] 2349 	mov	dptr,#_rgb_matrix_config
      004F4E 25 E0            [12] 2350 	add	a,acc
      004F50 25 E0            [12] 2351 	add	a,acc
      004F52 54 FC            [12] 2352 	anl	a,#0xfc
      004F54 F5 F0            [12] 2353 	mov	b,a
      004F56 E0               [24] 2354 	movx	a,@dptr
      004F57 54 03            [12] 2355 	anl	a,#0x03
      004F59 45 F0            [12] 2356 	orl	a,b
      004F5B F0               [24] 2357 	movx	@dptr,a
                                   2358 ;	keyboards/ajazz/ak820/ak820_rgb.c:252: rendering = false;
      004F5C 90 05 D2         [24] 2359 	mov	dptr,#_rendering
      004F5F E4               [12] 2360 	clr	a
      004F60 F0               [24] 2361 	movx	@dptr,a
                                   2362 ;	keyboards/ajazz/ak820/ak820_rgb.c:253: }
      004F61 22               [24] 2363 	ret
                                   2364 ;------------------------------------------------------------
                                   2365 ;Allocation info for local variables in function 'rgb_matrix_step_noeeprom'
                                   2366 ;------------------------------------------------------------
                                   2367 ;	keyboards/ajazz/ak820/ak820_rgb.c:254: void rgb_matrix_step_noeeprom(void) {
                                   2368 ;	-----------------------------------------
                                   2369 ;	 function rgb_matrix_step_noeeprom
                                   2370 ;	-----------------------------------------
      004F62                       2371 _rgb_matrix_step_noeeprom:
                                   2372 ;	keyboards/ajazz/ak820/ak820_rgb.c:255: rgb_matrix_mode_noeeprom(rgb_matrix_config.mode + 1 >= RGB_MATRIX_EFFECT_MAX ? 1 : rgb_matrix_config.mode + 1);
      004F62 90 05 C8         [24] 2373 	mov	dptr,#_rgb_matrix_config
      004F65 E0               [24] 2374 	movx	a,@dptr
      004F66 03               [12] 2375 	rr	a
      004F67 03               [12] 2376 	rr	a
      004F68 54 3F            [12] 2377 	anl	a,#0x3f
      004F6A FF               [12] 2378 	mov	r7,a
      004F6B 0F               [12] 2379 	inc	r7
      004F6C BF 07 00         [24] 2380 	cjne	r7,#0x07,00112$
      004F6F                       2381 00112$:
      004F6F 40 04            [24] 2382 	jc	00103$
      004F71 7F 01            [12] 2383 	mov	r7,#0x01
      004F73 80 0C            [24] 2384 	sjmp	00104$
      004F75                       2385 00103$:
      004F75 90 05 C8         [24] 2386 	mov	dptr,#_rgb_matrix_config
      004F78 E0               [24] 2387 	movx	a,@dptr
      004F79 03               [12] 2388 	rr	a
      004F7A 03               [12] 2389 	rr	a
      004F7B 54 3F            [12] 2390 	anl	a,#0x3f
      004F7D FE               [12] 2391 	mov	r6,a
      004F7E 0E               [12] 2392 	inc	r6
      004F7F 8E 07            [24] 2393 	mov	ar7,r6
      004F81                       2394 00104$:
      004F81 8F 82            [24] 2395 	mov	dpl, r7
                                   2396 ;	keyboards/ajazz/ak820/ak820_rgb.c:256: }
      004F83 02 4F 25         [24] 2397 	ljmp	_rgb_matrix_mode_noeeprom
                                   2398 ;------------------------------------------------------------
                                   2399 ;Allocation info for local variables in function 'rgb_matrix_step_reverse_noeeprom'
                                   2400 ;------------------------------------------------------------
                                   2401 ;	keyboards/ajazz/ak820/ak820_rgb.c:257: void rgb_matrix_step_reverse_noeeprom(void) {
                                   2402 ;	-----------------------------------------
                                   2403 ;	 function rgb_matrix_step_reverse_noeeprom
                                   2404 ;	-----------------------------------------
      004F86                       2405 _rgb_matrix_step_reverse_noeeprom:
                                   2406 ;	keyboards/ajazz/ak820/ak820_rgb.c:258: rgb_matrix_mode_noeeprom(rgb_matrix_config.mode <= 1 ? RGB_MATRIX_EFFECT_MAX - 1 : rgb_matrix_config.mode - 1);
      004F86 90 05 C8         [24] 2407 	mov	dptr,#_rgb_matrix_config
      004F89 E0               [24] 2408 	movx	a,@dptr
      004F8A 03               [12] 2409 	rr	a
      004F8B 03               [12] 2410 	rr	a
      004F8C 54 3F            [12] 2411 	anl	a,#0x3f
      004F8E 24 FE            [12] 2412 	add	a,#0xff - 0x01
      004F90 40 04            [24] 2413 	jc	00103$
                                   2414 ;	free result
      004F92 7F 06            [12] 2415 	mov	r7,#0x06
      004F94 80 0A            [24] 2416 	sjmp	00104$
      004F96                       2417 00103$:
      004F96 90 05 C8         [24] 2418 	mov	dptr,#_rgb_matrix_config
      004F99 E0               [24] 2419 	movx	a,@dptr
      004F9A 03               [12] 2420 	rr	a
      004F9B 03               [12] 2421 	rr	a
      004F9C 54 3F            [12] 2422 	anl	a,#0x3f
      004F9E 14               [12] 2423 	dec	a
      004F9F FF               [12] 2424 	mov	r7,a
      004FA0                       2425 00104$:
      004FA0 8F 82            [24] 2426 	mov	dpl, r7
                                   2427 ;	keyboards/ajazz/ak820/ak820_rgb.c:259: }
      004FA2 02 4F 25         [24] 2428 	ljmp	_rgb_matrix_mode_noeeprom
                                   2429 ;------------------------------------------------------------
                                   2430 ;Allocation info for local variables in function 'rgb_matrix_sethsv_noeeprom'
                                   2431 ;------------------------------------------------------------
                                   2432 ;sat           Allocated with name '_rgb_matrix_sethsv_noeeprom_PARM_2'
                                   2433 ;val           Allocated with name '_rgb_matrix_sethsv_noeeprom_PARM_3'
                                   2434 ;hue           Allocated with name '_rgb_matrix_sethsv_noeeprom_hue_10000_346'
                                   2435 ;------------------------------------------------------------
                                   2436 ;	keyboards/ajazz/ak820/ak820_rgb.c:260: void rgb_matrix_sethsv_noeeprom(uint16_t hue, uint8_t sat, uint8_t val) {
                                   2437 ;	-----------------------------------------
                                   2438 ;	 function rgb_matrix_sethsv_noeeprom
                                   2439 ;	-----------------------------------------
      004FA5                       2440 _rgb_matrix_sethsv_noeeprom:
      004FA5 AF 83            [24] 2441 	mov	r7,dph
      004FA7 E5 82            [12] 2442 	mov	a,dpl
      004FA9 90 06 52         [24] 2443 	mov	dptr,#_rgb_matrix_sethsv_noeeprom_hue_10000_346
      004FAC F0               [24] 2444 	movx	@dptr,a
      004FAD EF               [12] 2445 	mov	a,r7
      004FAE A3               [24] 2446 	inc	dptr
      004FAF F0               [24] 2447 	movx	@dptr,a
                                   2448 ;	keyboards/ajazz/ak820/ak820_rgb.c:261: rgb_matrix_config.hsv.h = hue;
      004FB0 90 06 52         [24] 2449 	mov	dptr,#_rgb_matrix_sethsv_noeeprom_hue_10000_346
      004FB3 E0               [24] 2450 	movx	a,@dptr
      004FB4 90 05 C9         [24] 2451 	mov	dptr,#(_rgb_matrix_config + 0x0001)
      004FB7 F0               [24] 2452 	movx	@dptr,a
                                   2453 ;	keyboards/ajazz/ak820/ak820_rgb.c:262: rgb_matrix_config.hsv.s = sat;
      004FB8 90 06 50         [24] 2454 	mov	dptr,#_rgb_matrix_sethsv_noeeprom_PARM_2
      004FBB E0               [24] 2455 	movx	a,@dptr
      004FBC FF               [12] 2456 	mov	r7,a
      004FBD 90 05 CA         [24] 2457 	mov	dptr,#(_rgb_matrix_config + 0x0002)
      004FC0 F0               [24] 2458 	movx	@dptr,a
                                   2459 ;	keyboards/ajazz/ak820/ak820_rgb.c:263: rgb_matrix_config.hsv.v = val > RGB_MATRIX_MAXIMUM_BRIGHTNESS ? RGB_MATRIX_MAXIMUM_BRIGHTNESS : val;
      004FC1 90 06 51         [24] 2460 	mov	dptr,#_rgb_matrix_sethsv_noeeprom_PARM_3
      004FC4 E0               [24] 2461 	movx	a,@dptr
      004FC5 FF               [12] 2462 	mov  r7,a
      004FC6 24 5F            [12] 2463 	add	a,#0xff - 0xa0
      004FC8 50 04            [24] 2464 	jnc	00103$
                                   2465 ;	free result
      004FCA 7E A0            [12] 2466 	mov	r6,#0xa0
      004FCC 80 02            [24] 2467 	sjmp	00104$
      004FCE                       2468 00103$:
      004FCE 8F 06            [24] 2469 	mov	ar6,r7
      004FD0                       2470 00104$:
      004FD0 90 05 CB         [24] 2471 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      004FD3 EE               [12] 2472 	mov	a,r6
      004FD4 F0               [24] 2473 	movx	@dptr,a
                                   2474 ;	keyboards/ajazz/ak820/ak820_rgb.c:264: }
      004FD5 22               [24] 2475 	ret
                                   2476 ;------------------------------------------------------------
                                   2477 ;Allocation info for local variables in function 'rgb_matrix_set_speed_noeeprom'
                                   2478 ;------------------------------------------------------------
                                   2479 ;speed         Allocated with name '_rgb_matrix_set_speed_noeeprom_speed_10000_348'
                                   2480 ;------------------------------------------------------------
                                   2481 ;	keyboards/ajazz/ak820/ak820_rgb.c:265: void rgb_matrix_set_speed_noeeprom(uint8_t speed) { rgb_matrix_config.speed = speed; }
                                   2482 ;	-----------------------------------------
                                   2483 ;	 function rgb_matrix_set_speed_noeeprom
                                   2484 ;	-----------------------------------------
      004FD6                       2485 _rgb_matrix_set_speed_noeeprom:
      004FD6 E5 82            [12] 2486 	mov	a,dpl
      004FD8 90 06 54         [24] 2487 	mov	dptr,#_rgb_matrix_set_speed_noeeprom_speed_10000_348
      004FDB F0               [24] 2488 	movx	@dptr,a
      004FDC E0               [24] 2489 	movx	a,@dptr
      004FDD 90 05 CC         [24] 2490 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      004FE0 F0               [24] 2491 	movx	@dptr,a
      004FE1 22               [24] 2492 	ret
                                   2493 ;------------------------------------------------------------
                                   2494 ;Allocation info for local variables in function 'rgb_matrix_set_flags_noeeprom'
                                   2495 ;------------------------------------------------------------
                                   2496 ;flags         Allocated with name '_rgb_matrix_set_flags_noeeprom_flags_10000_350'
                                   2497 ;------------------------------------------------------------
                                   2498 ;	keyboards/ajazz/ak820/ak820_rgb.c:266: void rgb_matrix_set_flags_noeeprom(led_flags_t flags) { rgb_matrix_config.flags = flags; }
                                   2499 ;	-----------------------------------------
                                   2500 ;	 function rgb_matrix_increase_hue_noeeprom
                                   2501 ;	-----------------------------------------
      004FE2                       2502 _rgb_matrix_increase_hue_noeeprom:
      004FE2 90 05 C9         [24] 2503 	mov	dptr,#(_rgb_matrix_config + 0x0001)
      004FE5 E0               [24] 2504 	movx	a,@dptr
      004FE6 24 08            [12] 2505 	add	a,#0x08
      004FE8 90 05 C9         [24] 2506 	mov	dptr,#(_rgb_matrix_config + 0x0001)
      004FEB F0               [24] 2507 	movx	@dptr,a
      004FEC 22               [24] 2508 	ret
                                   2509 ;------------------------------------------------------------
                                   2510 ;Allocation info for local variables in function 'rgb_matrix_decrease_hue_noeeprom'
                                   2511 ;------------------------------------------------------------
                                   2512 ;	keyboards/ajazz/ak820/ak820_rgb.c:269: void rgb_matrix_decrease_hue_noeeprom(void) { rgb_matrix_config.hsv.h -= 8; }
                                   2513 ;	-----------------------------------------
                                   2514 ;	 function rgb_matrix_decrease_hue_noeeprom
                                   2515 ;	-----------------------------------------
      004FED                       2516 _rgb_matrix_decrease_hue_noeeprom:
      004FED 90 05 C9         [24] 2517 	mov	dptr,#(_rgb_matrix_config + 0x0001)
      004FF0 E0               [24] 2518 	movx	a,@dptr
      004FF1 24 F8            [12] 2519 	add	a,#0xf8
      004FF3 90 05 C9         [24] 2520 	mov	dptr,#(_rgb_matrix_config + 0x0001)
      004FF6 F0               [24] 2521 	movx	@dptr,a
      004FF7 22               [24] 2522 	ret
                                   2523 ;------------------------------------------------------------
                                   2524 ;Allocation info for local variables in function 'rgb_matrix_increase_sat_noeeprom'
                                   2525 ;------------------------------------------------------------
                                   2526 ;	keyboards/ajazz/ak820/ak820_rgb.c:270: void rgb_matrix_increase_sat_noeeprom(void) { rgb_matrix_config.hsv.s = add_sat(rgb_matrix_config.hsv.s, 16); }
                                   2527 ;	-----------------------------------------
                                   2528 ;	 function rgb_matrix_increase_sat_noeeprom
                                   2529 ;	-----------------------------------------
      004FF8                       2530 _rgb_matrix_increase_sat_noeeprom:
      004FF8 90 05 CA         [24] 2531 	mov	dptr,#(_rgb_matrix_config + 0x0002)
      004FFB E0               [24] 2532 	movx	a,@dptr
      004FFC FF               [12] 2533 	mov	r7,a
      004FFD 90 06 34         [24] 2534 	mov	dptr,#_add_sat_PARM_2
      005000 74 10            [12] 2535 	mov	a,#0x10
      005002 F0               [24] 2536 	movx	@dptr,a
      005003 8F 82            [24] 2537 	mov	dpl, r7
      005005 12 48 3A         [24] 2538 	lcall	_add_sat
      005008 AF 82            [24] 2539 	mov	r7, dpl
      00500A 90 05 CA         [24] 2540 	mov	dptr,#(_rgb_matrix_config + 0x0002)
      00500D EF               [12] 2541 	mov	a,r7
      00500E F0               [24] 2542 	movx	@dptr,a
      00500F 22               [24] 2543 	ret
                                   2544 ;------------------------------------------------------------
                                   2545 ;Allocation info for local variables in function 'rgb_matrix_decrease_sat_noeeprom'
                                   2546 ;------------------------------------------------------------
                                   2547 ;	keyboards/ajazz/ak820/ak820_rgb.c:271: void rgb_matrix_decrease_sat_noeeprom(void) { rgb_matrix_config.hsv.s = sub_sat(rgb_matrix_config.hsv.s, 16); }
                                   2548 ;	-----------------------------------------
                                   2549 ;	 function rgb_matrix_decrease_sat_noeeprom
                                   2550 ;	-----------------------------------------
      005010                       2551 _rgb_matrix_decrease_sat_noeeprom:
      005010 90 05 CA         [24] 2552 	mov	dptr,#(_rgb_matrix_config + 0x0002)
      005013 E0               [24] 2553 	movx	a,@dptr
      005014 FF               [12] 2554 	mov	r7,a
      005015 90 06 36         [24] 2555 	mov	dptr,#_sub_sat_PARM_2
      005018 74 10            [12] 2556 	mov	a,#0x10
      00501A F0               [24] 2557 	movx	@dptr,a
      00501B 8F 82            [24] 2558 	mov	dpl, r7
      00501D 12 48 5F         [24] 2559 	lcall	_sub_sat
      005020 AF 82            [24] 2560 	mov	r7, dpl
      005022 90 05 CA         [24] 2561 	mov	dptr,#(_rgb_matrix_config + 0x0002)
      005025 EF               [12] 2562 	mov	a,r7
      005026 F0               [24] 2563 	movx	@dptr,a
      005027 22               [24] 2564 	ret
                                   2565 ;------------------------------------------------------------
                                   2566 ;Allocation info for local variables in function 'rgb_matrix_increase_val_noeeprom'
                                   2567 ;------------------------------------------------------------
                                   2568 ;val           Allocated with name '_rgb_matrix_increase_val_noeeprom_val_10000_361'
                                   2569 ;------------------------------------------------------------
                                   2570 ;	keyboards/ajazz/ak820/ak820_rgb.c:272: void rgb_matrix_increase_val_noeeprom(void) {
                                   2571 ;	-----------------------------------------
                                   2572 ;	 function rgb_matrix_increase_val_noeeprom
                                   2573 ;	-----------------------------------------
      005028                       2574 _rgb_matrix_increase_val_noeeprom:
                                   2575 ;	keyboards/ajazz/ak820/ak820_rgb.c:273: uint8_t val = add_sat(rgb_matrix_config.hsv.v, 16);
      005028 90 05 CB         [24] 2576 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      00502B E0               [24] 2577 	movx	a,@dptr
      00502C FF               [12] 2578 	mov	r7,a
      00502D 90 06 34         [24] 2579 	mov	dptr,#_add_sat_PARM_2
      005030 74 10            [12] 2580 	mov	a,#0x10
      005032 F0               [24] 2581 	movx	@dptr,a
      005033 8F 82            [24] 2582 	mov	dpl, r7
      005035 12 48 3A         [24] 2583 	lcall	_add_sat
                                   2584 ;	keyboards/ajazz/ak820/ak820_rgb.c:274: rgb_matrix_config.hsv.v = val > RGB_MATRIX_MAXIMUM_BRIGHTNESS ? RGB_MATRIX_MAXIMUM_BRIGHTNESS : val;
      005038 E5 82            [12] 2585 	mov	a,dpl
      00503A FF               [12] 2586 	mov	r7,a
      00503B 24 5F            [12] 2587 	add	a,#0xff - 0xa0
      00503D 50 04            [24] 2588 	jnc	00103$
                                   2589 ;	free result
      00503F 7E A0            [12] 2590 	mov	r6,#0xa0
      005041 80 02            [24] 2591 	sjmp	00104$
      005043                       2592 00103$:
      005043 8F 06            [24] 2593 	mov	ar6,r7
      005045                       2594 00104$:
      005045 90 05 CB         [24] 2595 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      005048 EE               [12] 2596 	mov	a,r6
      005049 F0               [24] 2597 	movx	@dptr,a
                                   2598 ;	keyboards/ajazz/ak820/ak820_rgb.c:275: }
      00504A 22               [24] 2599 	ret
                                   2600 ;------------------------------------------------------------
                                   2601 ;Allocation info for local variables in function 'rgb_matrix_decrease_val_noeeprom'
                                   2602 ;------------------------------------------------------------
                                   2603 ;	keyboards/ajazz/ak820/ak820_rgb.c:276: void rgb_matrix_decrease_val_noeeprom(void) { rgb_matrix_config.hsv.v = sub_sat(rgb_matrix_config.hsv.v, 16); }
                                   2604 ;	-----------------------------------------
                                   2605 ;	 function rgb_matrix_decrease_val_noeeprom
                                   2606 ;	-----------------------------------------
      00504B                       2607 _rgb_matrix_decrease_val_noeeprom:
      00504B 90 05 CB         [24] 2608 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      00504E E0               [24] 2609 	movx	a,@dptr
      00504F FF               [12] 2610 	mov	r7,a
      005050 90 06 36         [24] 2611 	mov	dptr,#_sub_sat_PARM_2
      005053 74 10            [12] 2612 	mov	a,#0x10
      005055 F0               [24] 2613 	movx	@dptr,a
      005056 8F 82            [24] 2614 	mov	dpl, r7
      005058 12 48 5F         [24] 2615 	lcall	_sub_sat
      00505B AF 82            [24] 2616 	mov	r7, dpl
      00505D 90 05 CB         [24] 2617 	mov	dptr,#(_rgb_matrix_config + 0x0003)
      005060 EF               [12] 2618 	mov	a,r7
      005061 F0               [24] 2619 	movx	@dptr,a
      005062 22               [24] 2620 	ret
                                   2621 ;------------------------------------------------------------
                                   2622 ;Allocation info for local variables in function 'rgb_matrix_increase_speed_noeeprom'
                                   2623 ;------------------------------------------------------------
                                   2624 ;	keyboards/ajazz/ak820/ak820_rgb.c:277: void rgb_matrix_increase_speed_noeeprom(void) { rgb_matrix_config.speed = add_sat(rgb_matrix_config.speed, 16); }
                                   2625 ;	-----------------------------------------
                                   2626 ;	 function rgb_matrix_increase_speed_noeeprom
                                   2627 ;	-----------------------------------------
      005063                       2628 _rgb_matrix_increase_speed_noeeprom:
      005063 90 05 CC         [24] 2629 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      005066 E0               [24] 2630 	movx	a,@dptr
      005067 FF               [12] 2631 	mov	r7,a
      005068 90 06 34         [24] 2632 	mov	dptr,#_add_sat_PARM_2
      00506B 74 10            [12] 2633 	mov	a,#0x10
      00506D F0               [24] 2634 	movx	@dptr,a
      00506E 8F 82            [24] 2635 	mov	dpl, r7
      005070 12 48 3A         [24] 2636 	lcall	_add_sat
      005073 AF 82            [24] 2637 	mov	r7, dpl
      005075 90 05 CC         [24] 2638 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      005078 EF               [12] 2639 	mov	a,r7
      005079 F0               [24] 2640 	movx	@dptr,a
      00507A 22               [24] 2641 	ret
                                   2642 ;------------------------------------------------------------
                                   2643 ;Allocation info for local variables in function 'rgb_matrix_decrease_speed_noeeprom'
                                   2644 ;------------------------------------------------------------
                                   2645 ;	keyboards/ajazz/ak820/ak820_rgb.c:278: void rgb_matrix_decrease_speed_noeeprom(void) { rgb_matrix_config.speed = sub_sat(rgb_matrix_config.speed, 16); }
                                   2646 ;	-----------------------------------------
                                   2647 ;	 function rgb_matrix_decrease_speed_noeeprom
                                   2648 ;	-----------------------------------------
      00507B                       2649 _rgb_matrix_decrease_speed_noeeprom:
      00507B 90 05 CC         [24] 2650 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      00507E E0               [24] 2651 	movx	a,@dptr
      00507F FF               [12] 2652 	mov	r7,a
      005080 90 06 36         [24] 2653 	mov	dptr,#_sub_sat_PARM_2
      005083 74 10            [12] 2654 	mov	a,#0x10
      005085 F0               [24] 2655 	movx	@dptr,a
      005086 8F 82            [24] 2656 	mov	dpl, r7
      005088 12 48 5F         [24] 2657 	lcall	_sub_sat
      00508B AF 82            [24] 2658 	mov	r7, dpl
      00508D 90 05 CC         [24] 2659 	mov	dptr,#(_rgb_matrix_config + 0x0004)
      005090 EF               [12] 2660 	mov	a,r7
      005091 F0               [24] 2661 	movx	@dptr,a
      005092 22               [24] 2662 	ret
                                   2663 ;------------------------------------------------------------
                                   2664 ;Allocation info for local variables in function 'rgb_matrix_toggle'
                                   2665 ;------------------------------------------------------------
                                   2666 ;	keyboards/ajazz/ak820/ak820_rgb.c:281: PERSIST_WRAPPER(rgb_matrix_toggle)
                                   2667 ;	-----------------------------------------
                                   2668 ;	 function rgb_matrix_toggle
                                   2669 ;	-----------------------------------------
      005093                       2670 _rgb_matrix_toggle:
      005093 12 4E DC         [24] 2671 	lcall	_rgb_matrix_toggle_noeeprom
      005096 02 48 7C         [24] 2672 	ljmp	_mark_dirty
                                   2673 ;------------------------------------------------------------
                                   2674 ;Allocation info for local variables in function 'rgb_matrix_enable'
                                   2675 ;------------------------------------------------------------
                                   2676 ;	keyboards/ajazz/ak820/ak820_rgb.c:282: PERSIST_WRAPPER(rgb_matrix_enable)
                                   2677 ;	-----------------------------------------
                                   2678 ;	 function rgb_matrix_step
                                   2679 ;	-----------------------------------------
      005099                       2680 _rgb_matrix_step:
      005099 12 4F 62         [24] 2681 	lcall	_rgb_matrix_step_noeeprom
      00509C 02 48 7C         [24] 2682 	ljmp	_mark_dirty
                                   2683 ;------------------------------------------------------------
                                   2684 ;Allocation info for local variables in function 'rgb_matrix_step_reverse'
                                   2685 ;------------------------------------------------------------
                                   2686 ;	keyboards/ajazz/ak820/ak820_rgb.c:285: PERSIST_WRAPPER(rgb_matrix_step_reverse)
                                   2687 ;	-----------------------------------------
                                   2688 ;	 function rgb_matrix_step_reverse
                                   2689 ;	-----------------------------------------
      00509F                       2690 _rgb_matrix_step_reverse:
      00509F 12 4F 86         [24] 2691 	lcall	_rgb_matrix_step_reverse_noeeprom
      0050A2 02 48 7C         [24] 2692 	ljmp	_mark_dirty
                                   2693 ;------------------------------------------------------------
                                   2694 ;Allocation info for local variables in function 'rgb_matrix_increase_hue'
                                   2695 ;------------------------------------------------------------
                                   2696 ;	keyboards/ajazz/ak820/ak820_rgb.c:286: PERSIST_WRAPPER(rgb_matrix_increase_hue)
                                   2697 ;	-----------------------------------------
                                   2698 ;	 function rgb_matrix_increase_hue
                                   2699 ;	-----------------------------------------
      0050A5                       2700 _rgb_matrix_increase_hue:
      0050A5 12 4F E2         [24] 2701 	lcall	_rgb_matrix_increase_hue_noeeprom
      0050A8 02 48 7C         [24] 2702 	ljmp	_mark_dirty
                                   2703 ;------------------------------------------------------------
                                   2704 ;Allocation info for local variables in function 'rgb_matrix_decrease_hue'
                                   2705 ;------------------------------------------------------------
                                   2706 ;	keyboards/ajazz/ak820/ak820_rgb.c:287: PERSIST_WRAPPER(rgb_matrix_decrease_hue)
                                   2707 ;	-----------------------------------------
                                   2708 ;	 function rgb_matrix_decrease_hue
                                   2709 ;	-----------------------------------------
      0050AB                       2710 _rgb_matrix_decrease_hue:
      0050AB 12 4F ED         [24] 2711 	lcall	_rgb_matrix_decrease_hue_noeeprom
      0050AE 02 48 7C         [24] 2712 	ljmp	_mark_dirty
                                   2713 ;------------------------------------------------------------
                                   2714 ;Allocation info for local variables in function 'rgb_matrix_increase_sat'
                                   2715 ;------------------------------------------------------------
                                   2716 ;	keyboards/ajazz/ak820/ak820_rgb.c:288: PERSIST_WRAPPER(rgb_matrix_increase_sat)
                                   2717 ;	-----------------------------------------
                                   2718 ;	 function rgb_matrix_increase_sat
                                   2719 ;	-----------------------------------------
      0050B1                       2720 _rgb_matrix_increase_sat:
      0050B1 12 4F F8         [24] 2721 	lcall	_rgb_matrix_increase_sat_noeeprom
      0050B4 02 48 7C         [24] 2722 	ljmp	_mark_dirty
                                   2723 ;------------------------------------------------------------
                                   2724 ;Allocation info for local variables in function 'rgb_matrix_decrease_sat'
                                   2725 ;------------------------------------------------------------
                                   2726 ;	keyboards/ajazz/ak820/ak820_rgb.c:289: PERSIST_WRAPPER(rgb_matrix_decrease_sat)
                                   2727 ;	-----------------------------------------
                                   2728 ;	 function rgb_matrix_decrease_sat
                                   2729 ;	-----------------------------------------
      0050B7                       2730 _rgb_matrix_decrease_sat:
      0050B7 12 50 10         [24] 2731 	lcall	_rgb_matrix_decrease_sat_noeeprom
      0050BA 02 48 7C         [24] 2732 	ljmp	_mark_dirty
                                   2733 ;------------------------------------------------------------
                                   2734 ;Allocation info for local variables in function 'rgb_matrix_increase_val'
                                   2735 ;------------------------------------------------------------
                                   2736 ;	keyboards/ajazz/ak820/ak820_rgb.c:290: PERSIST_WRAPPER(rgb_matrix_increase_val)
                                   2737 ;	-----------------------------------------
                                   2738 ;	 function rgb_matrix_increase_val
                                   2739 ;	-----------------------------------------
      0050BD                       2740 _rgb_matrix_increase_val:
      0050BD 12 50 28         [24] 2741 	lcall	_rgb_matrix_increase_val_noeeprom
      0050C0 02 48 7C         [24] 2742 	ljmp	_mark_dirty
                                   2743 ;------------------------------------------------------------
                                   2744 ;Allocation info for local variables in function 'rgb_matrix_decrease_val'
                                   2745 ;------------------------------------------------------------
                                   2746 ;	keyboards/ajazz/ak820/ak820_rgb.c:291: PERSIST_WRAPPER(rgb_matrix_decrease_val)
                                   2747 ;	-----------------------------------------
                                   2748 ;	 function rgb_matrix_decrease_val
                                   2749 ;	-----------------------------------------
      0050C3                       2750 _rgb_matrix_decrease_val:
      0050C3 12 50 4B         [24] 2751 	lcall	_rgb_matrix_decrease_val_noeeprom
      0050C6 02 48 7C         [24] 2752 	ljmp	_mark_dirty
                                   2753 ;------------------------------------------------------------
                                   2754 ;Allocation info for local variables in function 'rgb_matrix_increase_speed'
                                   2755 ;------------------------------------------------------------
                                   2756 ;	keyboards/ajazz/ak820/ak820_rgb.c:292: PERSIST_WRAPPER(rgb_matrix_increase_speed)
                                   2757 ;	-----------------------------------------
                                   2758 ;	 function rgb_matrix_increase_speed
                                   2759 ;	-----------------------------------------
      0050C9                       2760 _rgb_matrix_increase_speed:
      0050C9 12 50 63         [24] 2761 	lcall	_rgb_matrix_increase_speed_noeeprom
      0050CC 02 48 7C         [24] 2762 	ljmp	_mark_dirty
                                   2763 ;------------------------------------------------------------
                                   2764 ;Allocation info for local variables in function 'rgb_matrix_decrease_speed'
                                   2765 ;------------------------------------------------------------
                                   2766 ;	keyboards/ajazz/ak820/ak820_rgb.c:293: PERSIST_WRAPPER(rgb_matrix_decrease_speed)
                                   2767 ;	-----------------------------------------
                                   2768 ;	 function rgb_matrix_decrease_speed
                                   2769 ;	-----------------------------------------
      0050CF                       2770 _rgb_matrix_decrease_speed:
      0050CF 12 50 7B         [24] 2771 	lcall	_rgb_matrix_decrease_speed_noeeprom
      0050D2 02 48 7C         [24] 2772 	ljmp	_mark_dirty
                                   2773 ;------------------------------------------------------------
                                   2774 ;Allocation info for local variables in function 'rgb_matrix_mode'
                                   2775 ;------------------------------------------------------------
                                   2776 ;mode          Allocated with name '_rgb_matrix_mode_mode_10000_394'
                                   2777 ;------------------------------------------------------------
                                   2778 ;	keyboards/ajazz/ak820/ak820_rgb.c:296: void rgb_matrix_mode(uint8_t mode) { rgb_matrix_mode_noeeprom(mode); mark_dirty(); }
                                   2779 ;	-----------------------------------------
                                   2780 ;	 function rgb_matrix_mode
                                   2781 ;	-----------------------------------------
      0050D5                       2782 _rgb_matrix_mode:
      0050D5 E5 82            [12] 2783 	mov	a,dpl
      0050D7 90 06 55         [24] 2784 	mov	dptr,#_rgb_matrix_mode_mode_10000_394
      0050DA F0               [24] 2785 	movx	@dptr,a
      0050DB E0               [24] 2786 	movx	a,@dptr
      0050DC F5 82            [12] 2787 	mov	dpl,a
      0050DE 12 4F 25         [24] 2788 	lcall	_rgb_matrix_mode_noeeprom
      0050E1 02 48 7C         [24] 2789 	ljmp	_mark_dirty
                                   2790 ;------------------------------------------------------------
                                   2791 ;Allocation info for local variables in function 'rgb_matrix_sethsv'
                                   2792 ;------------------------------------------------------------
                                   2793 ;sat           Allocated with name '_rgb_matrix_sethsv_PARM_2'
                                   2794 ;val           Allocated with name '_rgb_matrix_sethsv_PARM_3'
                                   2795 ;hue           Allocated with name '_rgb_matrix_sethsv_hue_10000_396'
                                   2796 ;------------------------------------------------------------
                                   2797 ;	keyboards/ajazz/ak820/ak820_rgb.c:297: void rgb_matrix_sethsv(uint16_t hue, uint8_t sat, uint8_t val) { rgb_matrix_sethsv_noeeprom(hue, sat, val); mark_dirty(); }
                                   2798 ;	-----------------------------------------
                                   2799 	.area CSEG    (CODE)
                                   2800 	.area CONST   (CODE)
                                   2801 	.area CONST   (CODE)
      00B602                       2802 _sine8_coefficients_10000_274:
      00B602 00                    2803 	.db #0x00	; 0
      00B603 31                    2804 	.db #0x31	; 49	'1'
      00B604 31                    2805 	.db #0x31	; 49	'1'
      00B605 29                    2806 	.db #0x29	; 41
      00B606 5A                    2807 	.db #0x5a	; 90	'Z'
      00B607 1B                    2808 	.db #0x1b	; 27
      00B608 75                    2809 	.db #0x75	; 117	'u'
      00B609 0A                    2810 	.db #0x0a	; 10
                                   2811 	.area CSEG    (CODE)
                                   2812 	.area XINIT   (CODE)
                                   2813 	.area CABS    (ABS,CODE)
