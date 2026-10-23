                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module eeconfig
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _eeconfig_init_via
                                     12 	.globl _via_eeprom_set_valid
                                     13 	.globl _via_eeprom_is_valid
                                     14 	.globl _eeprom_driver_erase
                                     15 	.globl _eeprom_update_block
                                     16 	.globl _eeprom_update_dword
                                     17 	.globl _eeprom_update_word
                                     18 	.globl _eeprom_update_byte
                                     19 	.globl _eeprom_read_dword
                                     20 	.globl _eeprom_read_word
                                     21 	.globl _eeprom_read_byte
                                     22 	.globl _ADC_START
                                     23 	.globl _S0_R_FIFO
                                     24 	.globl _S0_T_FIFO
                                     25 	.globl _S0_FREE
                                     26 	.globl _S0_IF_BYTE
                                     27 	.globl _S0_IF_FIRST
                                     28 	.globl _S0_IF_OV
                                     29 	.globl _S0_FST_ACT
                                     30 	.globl _CP_RL2
                                     31 	.globl _C_T2
                                     32 	.globl _TR2
                                     33 	.globl _EXEN2
                                     34 	.globl _TCLK
                                     35 	.globl _RCLK
                                     36 	.globl _EXF2
                                     37 	.globl _CAP1F
                                     38 	.globl _TF2
                                     39 	.globl _RI
                                     40 	.globl _TI
                                     41 	.globl _RB8
                                     42 	.globl _TB8
                                     43 	.globl _REN
                                     44 	.globl _SM2
                                     45 	.globl _SM1
                                     46 	.globl _SM0
                                     47 	.globl _IT0
                                     48 	.globl _IE0
                                     49 	.globl _IT1
                                     50 	.globl _IE1
                                     51 	.globl _TR0
                                     52 	.globl _TF0
                                     53 	.globl _TR1
                                     54 	.globl _TF1
                                     55 	.globl _P4_0
                                     56 	.globl _P4_1
                                     57 	.globl _P4_2
                                     58 	.globl _P4_3
                                     59 	.globl _P4_4
                                     60 	.globl _P4_5
                                     61 	.globl _P4_6
                                     62 	.globl _RXD
                                     63 	.globl _TXD
                                     64 	.globl _INT0
                                     65 	.globl _INT1
                                     66 	.globl _T0
                                     67 	.globl _T1
                                     68 	.globl _MOSI1
                                     69 	.globl _MISO1
                                     70 	.globl _SCK1
                                     71 	.globl _P3_0
                                     72 	.globl _P3_1
                                     73 	.globl _P3_2
                                     74 	.globl _P3_3
                                     75 	.globl _P3_4
                                     76 	.globl _P3_5
                                     77 	.globl _P3_6
                                     78 	.globl _P3_7
                                     79 	.globl _CAP1_
                                     80 	.globl _T2_
                                     81 	.globl _CAP2_
                                     82 	.globl _T2EX_
                                     83 	.globl _RXD1
                                     84 	.globl _TXD1
                                     85 	.globl _P2_0
                                     86 	.globl _P2_1
                                     87 	.globl _P2_2
                                     88 	.globl _P2_3
                                     89 	.globl _P2_4
                                     90 	.globl _P2_5
                                     91 	.globl _P2_6
                                     92 	.globl _P2_7
                                     93 	.globl _AIN0
                                     94 	.globl _AIN1
                                     95 	.globl _AIN2
                                     96 	.globl _AIN3
                                     97 	.globl _AIN4
                                     98 	.globl _AIN5
                                     99 	.globl _AIN6
                                    100 	.globl _AIN7
                                    101 	.globl _CAP1
                                    102 	.globl _T2
                                    103 	.globl _CAP2
                                    104 	.globl _T2EX
                                    105 	.globl _INT0_
                                    106 	.globl _SCS
                                    107 	.globl _MOSI
                                    108 	.globl _MISO
                                    109 	.globl _SCK
                                    110 	.globl _RXD1_
                                    111 	.globl _TXD1_
                                    112 	.globl _P1_0
                                    113 	.globl _P1_1
                                    114 	.globl _P1_2
                                    115 	.globl _P1_3
                                    116 	.globl _P1_4
                                    117 	.globl _P1_5
                                    118 	.globl _P1_6
                                    119 	.globl _P1_7
                                    120 	.globl _AIN8
                                    121 	.globl _AIN9
                                    122 	.globl _AIN10
                                    123 	.globl _AIN11
                                    124 	.globl _AIN12
                                    125 	.globl _AIN13
                                    126 	.globl _RXD_
                                    127 	.globl _TXD_
                                    128 	.globl _SCL0
                                    129 	.globl _SDA0
                                    130 	.globl _P0_0
                                    131 	.globl _P0_1
                                    132 	.globl _P0_2
                                    133 	.globl _P0_3
                                    134 	.globl _P0_4
                                    135 	.globl _P0_5
                                    136 	.globl _P0_6
                                    137 	.globl _P0_7
                                    138 	.globl _IE_SPI0
                                    139 	.globl _IE_USB
                                    140 	.globl _IE_ADC
                                    141 	.globl _IE_UART1
                                    142 	.globl _IE_PWM_I2C
                                    143 	.globl _IE_GPIO
                                    144 	.globl _IE_WDOG
                                    145 	.globl _PX0
                                    146 	.globl _PT0
                                    147 	.globl _PX1
                                    148 	.globl _PT1
                                    149 	.globl _PS
                                    150 	.globl _PT2
                                    151 	.globl _PL_FLAG
                                    152 	.globl _PH_FLAG
                                    153 	.globl _EX0
                                    154 	.globl _ET0
                                    155 	.globl _EX1
                                    156 	.globl _ET1
                                    157 	.globl _ES
                                    158 	.globl _ET2
                                    159 	.globl _E_DIS
                                    160 	.globl _EA
                                    161 	.globl _P
                                    162 	.globl _F1
                                    163 	.globl _OV
                                    164 	.globl _RS0
                                    165 	.globl _RS1
                                    166 	.globl _F0
                                    167 	.globl _AC
                                    168 	.globl _CY
                                    169 	.globl _I2CS_INT_ST
                                    170 	.globl _I2CX_INT
                                    171 	.globl _LED_STATUS
                                    172 	.globl _LED_DMA_H
                                    173 	.globl _LED_DMA_L
                                    174 	.globl _LED_DMA
                                    175 	.globl _LED_PWM_OE
                                    176 	.globl _LED_COMMON
                                    177 	.globl _ADC_CHAN
                                    178 	.globl _ADC_DAT_H
                                    179 	.globl _ADC_DAT_L
                                    180 	.globl _ADC_DAT
                                    181 	.globl _ADC_CTRL
                                    182 	.globl _SPI1_CK_SE
                                    183 	.globl _SPI1_CTRL
                                    184 	.globl _SPI1_DATA
                                    185 	.globl _SPI1_STAT
                                    186 	.globl _SIF1
                                    187 	.globl _SBAUD1
                                    188 	.globl _SBUF1
                                    189 	.globl _SCON1
                                    190 	.globl _SPI0_SETUP
                                    191 	.globl _SPI0_CK_SE
                                    192 	.globl _SPI0_CTRL
                                    193 	.globl _SPI0_DATA
                                    194 	.globl _SPI0_STAT
                                    195 	.globl _T2CAP1H
                                    196 	.globl _T2CAP1L
                                    197 	.globl _T2CAP1
                                    198 	.globl _TH2
                                    199 	.globl _TL2
                                    200 	.globl _T2COUNT
                                    201 	.globl _RCAP2H
                                    202 	.globl _RCAP2L
                                    203 	.globl _RCAP2
                                    204 	.globl _T2MOD
                                    205 	.globl _T2CON
                                    206 	.globl _SBUF
                                    207 	.globl _SCON
                                    208 	.globl _TH1
                                    209 	.globl _TH0
                                    210 	.globl _TL1
                                    211 	.globl _TL0
                                    212 	.globl _TMOD
                                    213 	.globl _TCON
                                    214 	.globl _XBUS_AUX
                                    215 	.globl _P7
                                    216 	.globl _P6_DIR
                                    217 	.globl _P6_OUT_PU
                                    218 	.globl _P6_IN
                                    219 	.globl _P5_DIR
                                    220 	.globl _P5_OUT_PU
                                    221 	.globl _P5_IN
                                    222 	.globl _P4_LED_KEY
                                    223 	.globl _P4_DIR_PU
                                    224 	.globl _P4_MOD_OC
                                    225 	.globl _P4
                                    226 	.globl _P3_DIR_PU
                                    227 	.globl _P3_MOD_OC
                                    228 	.globl _P3
                                    229 	.globl _P2_DIR_PU
                                    230 	.globl _P2_MOD_OC
                                    231 	.globl _P2
                                    232 	.globl _P1_DIR_PU
                                    233 	.globl _P1_MOD_OC
                                    234 	.globl _P1
                                    235 	.globl _P0_DIR_PU
                                    236 	.globl _P0_MOD_OC
                                    237 	.globl _P0
                                    238 	.globl _ROM_CTRL
                                    239 	.globl _ROM_DATA_HH
                                    240 	.globl _ROM_DATA_HL
                                    241 	.globl _ROM_DATA_HI
                                    242 	.globl _ROM_ADDR_H
                                    243 	.globl _ROM_ADDR_L
                                    244 	.globl _ROM_ADDR
                                    245 	.globl _GPIO_IE
                                    246 	.globl _IP_EX
                                    247 	.globl _IE_EX
                                    248 	.globl _IP
                                    249 	.globl _IE
                                    250 	.globl _WDOG_COUNT
                                    251 	.globl _RESET_KEEP
                                    252 	.globl _WAKE_CTRL
                                    253 	.globl _CLOCK_CFG
                                    254 	.globl _POWER_CFG
                                    255 	.globl _PCON
                                    256 	.globl _GLOBAL_CFG
                                    257 	.globl _SAFE_MOD
                                    258 	.globl _DPH
                                    259 	.globl _DPL
                                    260 	.globl _SP
                                    261 	.globl _A_INV
                                    262 	.globl _B
                                    263 	.globl _ACC
                                    264 	.globl _PSW
                                    265 	.globl _eeconfig_init_user
                                    266 	.globl _eeconfig_init_kb
                                    267 	.globl _eeconfig_init_quantum
                                    268 	.globl _eeconfig_init
                                    269 	.globl _eeconfig_disable
                                    270 	.globl _eeconfig_is_enabled
                                    271 	.globl _eeconfig_read_debug
                                    272 	.globl _eeconfig_read_default_layer
                                    273 	.globl _eeconfig_read_keymap
                                    274 	.globl _eeconfig_update_kb
                                    275 	.globl _eeconfig_update_user
                                    276 ;--------------------------------------------------------
                                    277 ; special function registers
                                    278 ;--------------------------------------------------------
                                    279 	.area RSEG    (ABS,DATA)
      000000                        280 	.org 0x0000
                           0000D0   281 _PSW	=	0x00d0
                           0000E0   282 _ACC	=	0x00e0
                           0000F0   283 _B	=	0x00f0
                           0000FD   284 _A_INV	=	0x00fd
                           000081   285 _SP	=	0x0081
                           000082   286 _DPL	=	0x0082
                           000083   287 _DPH	=	0x0083
                           0000A1   288 _SAFE_MOD	=	0x00a1
                           0000B1   289 _GLOBAL_CFG	=	0x00b1
                           000087   290 _PCON	=	0x0087
                           0000BA   291 _POWER_CFG	=	0x00ba
                           0000B9   292 _CLOCK_CFG	=	0x00b9
                           0000A9   293 _WAKE_CTRL	=	0x00a9
                           0000FE   294 _RESET_KEEP	=	0x00fe
                           0000FF   295 _WDOG_COUNT	=	0x00ff
                           0000A8   296 _IE	=	0x00a8
                           0000B8   297 _IP	=	0x00b8
                           0000E8   298 _IE_EX	=	0x00e8
                           0000E9   299 _IP_EX	=	0x00e9
                           0000B2   300 _GPIO_IE	=	0x00b2
                           008584   301 _ROM_ADDR	=	0x8584
                           000084   302 _ROM_ADDR_L	=	0x0084
                           000085   303 _ROM_ADDR_H	=	0x0085
                           008F8E   304 _ROM_DATA_HI	=	0x8f8e
                           00008E   305 _ROM_DATA_HL	=	0x008e
                           00008F   306 _ROM_DATA_HH	=	0x008f
                           000086   307 _ROM_CTRL	=	0x0086
                           000080   308 _P0	=	0x0080
                           0000C4   309 _P0_MOD_OC	=	0x00c4
                           0000C5   310 _P0_DIR_PU	=	0x00c5
                           000090   311 _P1	=	0x0090
                           000092   312 _P1_MOD_OC	=	0x0092
                           000093   313 _P1_DIR_PU	=	0x0093
                           0000A0   314 _P2	=	0x00a0
                           000094   315 _P2_MOD_OC	=	0x0094
                           000095   316 _P2_DIR_PU	=	0x0095
                           0000B0   317 _P3	=	0x00b0
                           000096   318 _P3_MOD_OC	=	0x0096
                           000097   319 _P3_DIR_PU	=	0x0097
                           0000C0   320 _P4	=	0x00c0
                           0000C2   321 _P4_MOD_OC	=	0x00c2
                           0000C3   322 _P4_DIR_PU	=	0x00c3
                           0000C1   323 _P4_LED_KEY	=	0x00c1
                           0000AA   324 _P5_IN	=	0x00aa
                           0000AB   325 _P5_OUT_PU	=	0x00ab
                           0000AC   326 _P5_DIR	=	0x00ac
                           0000AD   327 _P6_IN	=	0x00ad
                           0000AE   328 _P6_OUT_PU	=	0x00ae
                           0000AF   329 _P6_DIR	=	0x00af
                           0000F1   330 _P7	=	0x00f1
                           0000A2   331 _XBUS_AUX	=	0x00a2
                           000088   332 _TCON	=	0x0088
                           000089   333 _TMOD	=	0x0089
                           00008A   334 _TL0	=	0x008a
                           00008B   335 _TL1	=	0x008b
                           00008C   336 _TH0	=	0x008c
                           00008D   337 _TH1	=	0x008d
                           000098   338 _SCON	=	0x0098
                           000099   339 _SBUF	=	0x0099
                           0000C8   340 _T2CON	=	0x00c8
                           0000C9   341 _T2MOD	=	0x00c9
                           00CBCA   342 _RCAP2	=	0xcbca
                           0000CA   343 _RCAP2L	=	0x00ca
                           0000CB   344 _RCAP2H	=	0x00cb
                           00CDCC   345 _T2COUNT	=	0xcdcc
                           0000CC   346 _TL2	=	0x00cc
                           0000CD   347 _TH2	=	0x00cd
                           00CFCE   348 _T2CAP1	=	0xcfce
                           0000CE   349 _T2CAP1L	=	0x00ce
                           0000CF   350 _T2CAP1H	=	0x00cf
                           0000F8   351 _SPI0_STAT	=	0x00f8
                           0000F9   352 _SPI0_DATA	=	0x00f9
                           0000FA   353 _SPI0_CTRL	=	0x00fa
                           0000FB   354 _SPI0_CK_SE	=	0x00fb
                           0000FC   355 _SPI0_SETUP	=	0x00fc
                           0000BC   356 _SCON1	=	0x00bc
                           0000BD   357 _SBUF1	=	0x00bd
                           0000BE   358 _SBAUD1	=	0x00be
                           0000BF   359 _SIF1	=	0x00bf
                           0000B4   360 _SPI1_STAT	=	0x00b4
                           0000B5   361 _SPI1_DATA	=	0x00b5
                           0000B6   362 _SPI1_CTRL	=	0x00b6
                           0000B7   363 _SPI1_CK_SE	=	0x00b7
                           0000F3   364 _ADC_CTRL	=	0x00f3
                           00F5F4   365 _ADC_DAT	=	0xf5f4
                           0000F4   366 _ADC_DAT_L	=	0x00f4
                           0000F5   367 _ADC_DAT_H	=	0x00f5
                           0000F6   368 _ADC_CHAN	=	0x00f6
                           0000A6   369 _LED_COMMON	=	0x00a6
                           0000A7   370 _LED_PWM_OE	=	0x00a7
                           00C7C6   371 _LED_DMA	=	0xc7c6
                           0000C6   372 _LED_DMA_L	=	0x00c6
                           0000C7   373 _LED_DMA_H	=	0x00c7
                           0000F7   374 _LED_STATUS	=	0x00f7
                           0000B3   375 _I2CX_INT	=	0x00b3
                           0000BB   376 _I2CS_INT_ST	=	0x00bb
                                    377 ;--------------------------------------------------------
                                    378 ; special function bits
                                    379 ;--------------------------------------------------------
                                    380 	.area RSEG    (ABS,DATA)
      000000                        381 	.org 0x0000
                           0000D7   382 _CY	=	0x00d7
                           0000D6   383 _AC	=	0x00d6
                           0000D5   384 _F0	=	0x00d5
                           0000D4   385 _RS1	=	0x00d4
                           0000D3   386 _RS0	=	0x00d3
                           0000D2   387 _OV	=	0x00d2
                           0000D1   388 _F1	=	0x00d1
                           0000D0   389 _P	=	0x00d0
                           0000AF   390 _EA	=	0x00af
                           0000AE   391 _E_DIS	=	0x00ae
                           0000AD   392 _ET2	=	0x00ad
                           0000AC   393 _ES	=	0x00ac
                           0000AB   394 _ET1	=	0x00ab
                           0000AA   395 _EX1	=	0x00aa
                           0000A9   396 _ET0	=	0x00a9
                           0000A8   397 _EX0	=	0x00a8
                           0000BF   398 _PH_FLAG	=	0x00bf
                           0000BE   399 _PL_FLAG	=	0x00be
                           0000BD   400 _PT2	=	0x00bd
                           0000BC   401 _PS	=	0x00bc
                           0000BB   402 _PT1	=	0x00bb
                           0000BA   403 _PX1	=	0x00ba
                           0000B9   404 _PT0	=	0x00b9
                           0000B8   405 _PX0	=	0x00b8
                           0000EF   406 _IE_WDOG	=	0x00ef
                           0000EE   407 _IE_GPIO	=	0x00ee
                           0000ED   408 _IE_PWM_I2C	=	0x00ed
                           0000EC   409 _IE_UART1	=	0x00ec
                           0000EB   410 _IE_ADC	=	0x00eb
                           0000E9   411 _IE_USB	=	0x00e9
                           0000E8   412 _IE_SPI0	=	0x00e8
                           000087   413 _P0_7	=	0x0087
                           000086   414 _P0_6	=	0x0086
                           000085   415 _P0_5	=	0x0085
                           000084   416 _P0_4	=	0x0084
                           000083   417 _P0_3	=	0x0083
                           000082   418 _P0_2	=	0x0082
                           000081   419 _P0_1	=	0x0081
                           000080   420 _P0_0	=	0x0080
                           000081   421 _SDA0	=	0x0081
                           000080   422 _SCL0	=	0x0080
                           000083   423 _TXD_	=	0x0083
                           000082   424 _RXD_	=	0x0082
                           000085   425 _AIN13	=	0x0085
                           000084   426 _AIN12	=	0x0084
                           000083   427 _AIN11	=	0x0083
                           000082   428 _AIN10	=	0x0082
                           000081   429 _AIN9	=	0x0081
                           000080   430 _AIN8	=	0x0080
                           000097   431 _P1_7	=	0x0097
                           000096   432 _P1_6	=	0x0096
                           000095   433 _P1_5	=	0x0095
                           000094   434 _P1_4	=	0x0094
                           000093   435 _P1_3	=	0x0093
                           000092   436 _P1_2	=	0x0092
                           000091   437 _P1_1	=	0x0091
                           000090   438 _P1_0	=	0x0090
                           000097   439 _TXD1_	=	0x0097
                           000096   440 _RXD1_	=	0x0096
                           000097   441 _SCK	=	0x0097
                           000096   442 _MISO	=	0x0096
                           000095   443 _MOSI	=	0x0095
                           000094   444 _SCS	=	0x0094
                           000092   445 _INT0_	=	0x0092
                           000091   446 _T2EX	=	0x0091
                           000091   447 _CAP2	=	0x0091
                           000090   448 _T2	=	0x0090
                           000090   449 _CAP1	=	0x0090
                           000097   450 _AIN7	=	0x0097
                           000096   451 _AIN6	=	0x0096
                           000095   452 _AIN5	=	0x0095
                           000094   453 _AIN4	=	0x0094
                           000093   454 _AIN3	=	0x0093
                           000092   455 _AIN2	=	0x0092
                           000091   456 _AIN1	=	0x0091
                           000090   457 _AIN0	=	0x0090
                           0000A7   458 _P2_7	=	0x00a7
                           0000A6   459 _P2_6	=	0x00a6
                           0000A5   460 _P2_5	=	0x00a5
                           0000A4   461 _P2_4	=	0x00a4
                           0000A3   462 _P2_3	=	0x00a3
                           0000A2   463 _P2_2	=	0x00a2
                           0000A1   464 _P2_1	=	0x00a1
                           0000A0   465 _P2_0	=	0x00a0
                           0000A7   466 _TXD1	=	0x00a7
                           0000A6   467 _RXD1	=	0x00a6
                           0000A5   468 _T2EX_	=	0x00a5
                           0000A5   469 _CAP2_	=	0x00a5
                           0000A4   470 _T2_	=	0x00a4
                           0000A4   471 _CAP1_	=	0x00a4
                           0000B7   472 _P3_7	=	0x00b7
                           0000B6   473 _P3_6	=	0x00b6
                           0000B5   474 _P3_5	=	0x00b5
                           0000B4   475 _P3_4	=	0x00b4
                           0000B3   476 _P3_3	=	0x00b3
                           0000B2   477 _P3_2	=	0x00b2
                           0000B1   478 _P3_1	=	0x00b1
                           0000B0   479 _P3_0	=	0x00b0
                           0000B7   480 _SCK1	=	0x00b7
                           0000B6   481 _MISO1	=	0x00b6
                           0000B5   482 _MOSI1	=	0x00b5
                           0000B5   483 _T1	=	0x00b5
                           0000B4   484 _T0	=	0x00b4
                           0000B3   485 _INT1	=	0x00b3
                           0000B2   486 _INT0	=	0x00b2
                           0000B1   487 _TXD	=	0x00b1
                           0000B0   488 _RXD	=	0x00b0
                           0000C6   489 _P4_6	=	0x00c6
                           0000C5   490 _P4_5	=	0x00c5
                           0000C4   491 _P4_4	=	0x00c4
                           0000C3   492 _P4_3	=	0x00c3
                           0000C2   493 _P4_2	=	0x00c2
                           0000C1   494 _P4_1	=	0x00c1
                           0000C0   495 _P4_0	=	0x00c0
                           00008F   496 _TF1	=	0x008f
                           00008E   497 _TR1	=	0x008e
                           00008D   498 _TF0	=	0x008d
                           00008C   499 _TR0	=	0x008c
                           00008B   500 _IE1	=	0x008b
                           00008A   501 _IT1	=	0x008a
                           000089   502 _IE0	=	0x0089
                           000088   503 _IT0	=	0x0088
                           00009F   504 _SM0	=	0x009f
                           00009E   505 _SM1	=	0x009e
                           00009D   506 _SM2	=	0x009d
                           00009C   507 _REN	=	0x009c
                           00009B   508 _TB8	=	0x009b
                           00009A   509 _RB8	=	0x009a
                           000099   510 _TI	=	0x0099
                           000098   511 _RI	=	0x0098
                           0000CF   512 _TF2	=	0x00cf
                           0000CF   513 _CAP1F	=	0x00cf
                           0000CE   514 _EXF2	=	0x00ce
                           0000CD   515 _RCLK	=	0x00cd
                           0000CC   516 _TCLK	=	0x00cc
                           0000CB   517 _EXEN2	=	0x00cb
                           0000CA   518 _TR2	=	0x00ca
                           0000C9   519 _C_T2	=	0x00c9
                           0000C8   520 _CP_RL2	=	0x00c8
                           0000FF   521 _S0_FST_ACT	=	0x00ff
                           0000FE   522 _S0_IF_OV	=	0x00fe
                           0000FD   523 _S0_IF_FIRST	=	0x00fd
                           0000FC   524 _S0_IF_BYTE	=	0x00fc
                           0000FB   525 _S0_FREE	=	0x00fb
                           0000FA   526 _S0_T_FIFO	=	0x00fa
                           0000F8   527 _S0_R_FIFO	=	0x00f8
                           0000F7   528 _ADC_START	=	0x00f7
                                    529 ;--------------------------------------------------------
                                    530 ; overlayable register banks
                                    531 ;--------------------------------------------------------
                                    532 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        533 	.ds 8
                                    534 ;--------------------------------------------------------
                                    535 ; internal ram data
                                    536 ;--------------------------------------------------------
                                    537 	.area DSEG    (DATA)
      000018                        538 _eeconfig_is_enabled_sloc0_1_0:
      000018                        539 	.ds 1
                                    540 ;--------------------------------------------------------
                                    541 ; overlayable items in internal ram
                                    542 ;--------------------------------------------------------
                                    543 ;--------------------------------------------------------
                                    544 ; indirectly addressable internal ram data
                                    545 ;--------------------------------------------------------
                                    546 	.area ISEG    (DATA)
                                    547 ;--------------------------------------------------------
                                    548 ; absolute internal ram data
                                    549 ;--------------------------------------------------------
                                    550 	.area IABS    (ABS,DATA)
                                    551 	.area IABS    (ABS,DATA)
                                    552 ;--------------------------------------------------------
                                    553 ; bit data
                                    554 ;--------------------------------------------------------
                                    555 	.area BSEG    (BIT)
                                    556 ;--------------------------------------------------------
                                    557 ; paged external ram data
                                    558 ;--------------------------------------------------------
                                    559 	.area PSEG    (PAG,XDATA)
                                    560 ;--------------------------------------------------------
                                    561 ; uninitialized external ram data
                                    562 ;--------------------------------------------------------
                                    563 	.area XSEG    (XDATA)
      000929                        564 _eeconfig_init_quantum_dummy_10001_235:
      000929                        565 	.ds 8
      000931                        566 _eeconfig_is_enabled_is_eeprom_enabled_10000_243:
      000931                        567 	.ds 1
      000932                        568 _eeconfig_update_kb_val_10000_268:
      000932                        569 	.ds 4
      000936                        570 _eeconfig_update_user_val_10000_272:
      000936                        571 	.ds 4
                                    572 ;--------------------------------------------------------
                                    573 ; absolute external ram data
                                    574 ;--------------------------------------------------------
                                    575 	.area XABS    (ABS,XDATA)
                                    576 ;--------------------------------------------------------
                                    577 ; initialized external ram data
                                    578 ;--------------------------------------------------------
                                    579 	.area XISEG   (XDATA)
                                    580 	.area HOME    (CODE)
                                    581 	.area GSINIT0 (CODE)
                                    582 	.area GSINIT1 (CODE)
                                    583 	.area GSINIT2 (CODE)
                                    584 	.area GSINIT3 (CODE)
                                    585 	.area GSINIT4 (CODE)
                                    586 	.area GSINIT5 (CODE)
                                    587 	.area GSINIT  (CODE)
                                    588 	.area GSFINAL (CODE)
                                    589 	.area CSEG    (CODE)
                                    590 ;--------------------------------------------------------
                                    591 ; global & static initialisations
                                    592 ;--------------------------------------------------------
                                    593 	.area HOME    (CODE)
                                    594 	.area GSINIT  (CODE)
                                    595 	.area GSFINAL (CODE)
                                    596 	.area GSINIT  (CODE)
                                    597 ;--------------------------------------------------------
                                    598 ; Home
                                    599 ;--------------------------------------------------------
                                    600 	.area HOME    (CODE)
                                    601 	.area HOME    (CODE)
                                    602 ;--------------------------------------------------------
                                    603 ; code
                                    604 ;--------------------------------------------------------
                                    605 	.area CSEG    (CODE)
                                    606 ;------------------------------------------------------------
                                    607 ;Allocation info for local variables in function 'eeconfig_init_user'
                                    608 ;------------------------------------------------------------
                                    609 ;	quantum/eeconfig.c:27: __attribute__((weak)) void eeconfig_init_user(void) {
                                    610 ;	-----------------------------------------
                                    611 ;	 function eeconfig_init_user
                                    612 ;	-----------------------------------------
      00862E                        613 _eeconfig_init_user:
                           000007   614 	ar7 = 0x07
                           000006   615 	ar6 = 0x06
                           000005   616 	ar5 = 0x05
                           000004   617 	ar4 = 0x04
                           000003   618 	ar3 = 0x03
                           000002   619 	ar2 = 0x02
                           000001   620 	ar1 = 0x01
                           000000   621 	ar0 = 0x00
                                    622 ;	quantum/eeconfig.c:30: eeconfig_update_user(0);
      00862E 90 00 00         [24]  623 	mov	dptr,#0x0000
      008631 E4               [12]  624 	clr	a
      008632 F5 F0            [12]  625 	mov	b,a
                                    626 ;	quantum/eeconfig.c:32: }
      008634 02 87 C0         [24]  627 	ljmp	_eeconfig_update_user
                                    628 ;------------------------------------------------------------
                                    629 ;Allocation info for local variables in function 'eeconfig_init_kb'
                                    630 ;------------------------------------------------------------
                                    631 ;	quantum/eeconfig.c:34: __attribute__((weak)) void eeconfig_init_kb(void) {
                                    632 ;	-----------------------------------------
                                    633 ;	 function eeconfig_init_kb
                                    634 ;	-----------------------------------------
      008637                        635 _eeconfig_init_kb:
                                    636 ;	quantum/eeconfig.c:37: eeconfig_update_kb(0);
      008637 90 00 00         [24]  637 	mov	dptr,#0x0000
      00863A E4               [12]  638 	clr	a
      00863B F5 F0            [12]  639 	mov	b,a
      00863D 12 87 9B         [24]  640 	lcall	_eeconfig_update_kb
                                    641 ;	quantum/eeconfig.c:40: eeconfig_init_user();
                                    642 ;	quantum/eeconfig.c:41: }
      008640 02 86 2E         [24]  643 	ljmp	_eeconfig_init_user
                                    644 ;------------------------------------------------------------
                                    645 ;Allocation info for local variables in function 'eeconfig_init_quantum'
                                    646 ;------------------------------------------------------------
                                    647 ;dummy         Allocated with name '_eeconfig_init_quantum_dummy_10001_235'
                                    648 ;------------------------------------------------------------
                                    649 ;	quantum/eeconfig.c:46: void eeconfig_init_quantum(void) {
                                    650 ;	-----------------------------------------
                                    651 ;	 function eeconfig_init_quantum
                                    652 ;	-----------------------------------------
      008643                        653 _eeconfig_init_quantum:
                                    654 ;	quantum/eeconfig.c:48: eeprom_driver_erase();
      008643 12 3F 98         [24]  655 	lcall	_eeprom_driver_erase
                                    656 ;	quantum/eeconfig.c:51: eeprom_update_word(EECONFIG_MAGIC, EECONFIG_MAGIC_NUMBER);
      008646 90 05 BD         [24]  657 	mov	dptr,#_eeprom_update_word_PARM_2
      008649 74 E6            [12]  658 	mov	a,#0xe6
      00864B F0               [24]  659 	movx	@dptr,a
      00864C 74 FE            [12]  660 	mov	a,#0xfe
      00864E A3               [24]  661 	inc	dptr
      00864F F0               [24]  662 	movx	@dptr,a
      008650 90 00 00         [24]  663 	mov	dptr,#0x0000
      008653 75 F0 00         [24]  664 	mov	b, #0x00
      008656 12 46 F7         [24]  665 	lcall	_eeprom_update_word
                                    666 ;	quantum/eeconfig.c:52: eeprom_update_byte(EECONFIG_DEBUG, 0);
      008659 90 05 B9         [24]  667 	mov	dptr,#_eeprom_update_byte_PARM_2
      00865C E4               [12]  668 	clr	a
      00865D F0               [24]  669 	movx	@dptr,a
      00865E 90 00 02         [24]  670 	mov	dptr,#0x0002
      008661 F5 F0            [12]  671 	mov	b,a
      008663 12 46 7C         [24]  672 	lcall	_eeprom_update_byte
                                    673 ;	quantum/eeconfig.c:53: eeprom_update_byte(EECONFIG_DEFAULT_LAYER, 0);
      008666 90 05 B9         [24]  674 	mov	dptr,#_eeprom_update_byte_PARM_2
      008669 E4               [12]  675 	clr	a
      00866A F0               [24]  676 	movx	@dptr,a
      00866B 90 00 03         [24]  677 	mov	dptr,#0x0003
      00866E F5 F0            [12]  678 	mov	b,a
      008670 12 46 7C         [24]  679 	lcall	_eeprom_update_byte
                                    680 ;	quantum/eeconfig.c:54: default_layer_state = 0;
      008673 90 0B AD         [24]  681 	mov	dptr,#_default_layer_state
      008676 E4               [12]  682 	clr	a
      008677 F0               [24]  683 	movx	@dptr,a
                                    684 ;	quantum/eeconfig.c:56: eeprom_update_word(EECONFIG_KEYMAP, 0x1400);
      008678 90 05 BD         [24]  685 	mov	dptr,#_eeprom_update_word_PARM_2
      00867B F0               [24]  686 	movx	@dptr,a
      00867C 74 14            [12]  687 	mov	a,#0x14
      00867E A3               [24]  688 	inc	dptr
      00867F F0               [24]  689 	movx	@dptr,a
      008680 90 00 04         [24]  690 	mov	dptr,#0x0004
      008683 75 F0 00         [24]  691 	mov	b, #0x00
      008686 12 46 F7         [24]  692 	lcall	_eeprom_update_word
                                    693 ;	quantum/eeconfig.c:57: eeprom_update_byte(EECONFIG_BACKLIGHT, 0);
      008689 90 05 B9         [24]  694 	mov	dptr,#_eeprom_update_byte_PARM_2
      00868C E4               [12]  695 	clr	a
      00868D F0               [24]  696 	movx	@dptr,a
      00868E 90 00 06         [24]  697 	mov	dptr,#0x0006
      008691 F5 F0            [12]  698 	mov	b,a
      008693 12 46 7C         [24]  699 	lcall	_eeprom_update_byte
                                    700 ;	quantum/eeconfig.c:58: eeprom_update_byte(EECONFIG_AUDIO, 0xFF); // On by default
      008696 90 05 B9         [24]  701 	mov	dptr,#_eeprom_update_byte_PARM_2
      008699 74 FF            [12]  702 	mov	a,#0xff
      00869B F0               [24]  703 	movx	@dptr,a
      00869C 90 00 07         [24]  704 	mov	dptr,#0x0007
      00869F 75 F0 00         [24]  705 	mov	b, #0x00
      0086A2 12 46 7C         [24]  706 	lcall	_eeprom_update_byte
                                    707 ;	quantum/eeconfig.c:59: eeprom_update_dword(EECONFIG_RGBLIGHT, 0);
      0086A5 90 05 C2         [24]  708 	mov	dptr,#_eeprom_update_dword_PARM_2
      0086A8 E4               [12]  709 	clr	a
      0086A9 F0               [24]  710 	movx	@dptr,a
      0086AA A3               [24]  711 	inc	dptr
      0086AB F0               [24]  712 	movx	@dptr,a
      0086AC A3               [24]  713 	inc	dptr
      0086AD F0               [24]  714 	movx	@dptr,a
      0086AE A3               [24]  715 	inc	dptr
      0086AF F0               [24]  716 	movx	@dptr,a
      0086B0 90 00 08         [24]  717 	mov	dptr,#0x0008
      0086B3 F5 F0            [12]  718 	mov	b,a
      0086B5 12 47 4C         [24]  719 	lcall	_eeprom_update_dword
                                    720 ;	quantum/eeconfig.c:60: eeprom_update_byte(EECONFIG_RGBLIGHT_EXTENDED, 0);
      0086B8 90 05 B9         [24]  721 	mov	dptr,#_eeprom_update_byte_PARM_2
      0086BB E4               [12]  722 	clr	a
      0086BC F0               [24]  723 	movx	@dptr,a
      0086BD 90 00 24         [24]  724 	mov	dptr,#0x0024
      0086C0 F5 F0            [12]  725 	mov	b,a
      0086C2 12 46 7C         [24]  726 	lcall	_eeprom_update_byte
                                    727 ;	quantum/eeconfig.c:61: eeprom_update_byte(EECONFIG_VELOCIKEY, 0);
      0086C5 90 05 B9         [24]  728 	mov	dptr,#_eeprom_update_byte_PARM_2
      0086C8 E4               [12]  729 	clr	a
      0086C9 F0               [24]  730 	movx	@dptr,a
      0086CA 90 00 17         [24]  731 	mov	dptr,#0x0017
      0086CD F5 F0            [12]  732 	mov	b,a
      0086CF 12 46 7C         [24]  733 	lcall	_eeprom_update_byte
                                    734 ;	quantum/eeconfig.c:62: eeprom_update_byte(EECONFIG_UNICODEMODE, 0);
      0086D2 90 05 B9         [24]  735 	mov	dptr,#_eeprom_update_byte_PARM_2
      0086D5 E4               [12]  736 	clr	a
      0086D6 F0               [24]  737 	movx	@dptr,a
      0086D7 90 00 0C         [24]  738 	mov	dptr,#0x000c
      0086DA F5 F0            [12]  739 	mov	b,a
      0086DC 12 46 7C         [24]  740 	lcall	_eeprom_update_byte
                                    741 ;	quantum/eeconfig.c:63: eeprom_update_byte(EECONFIG_STENOMODE, 0);
      0086DF 90 05 B9         [24]  742 	mov	dptr,#_eeprom_update_byte_PARM_2
      0086E2 E4               [12]  743 	clr	a
      0086E3 F0               [24]  744 	movx	@dptr,a
      0086E4 90 00 0D         [24]  745 	mov	dptr,#0x000d
      0086E7 F5 F0            [12]  746 	mov	b,a
      0086E9 12 46 7C         [24]  747 	lcall	_eeprom_update_byte
                                    748 ;	quantum/eeconfig.c:64: uint64_t dummy = 0;
      0086EC 90 09 29         [24]  749 	mov	dptr,#_eeconfig_init_quantum_dummy_10001_235
      0086EF E4               [12]  750 	clr	a
      0086F0 F0               [24]  751 	movx	@dptr,a
      0086F1 A3               [24]  752 	inc	dptr
      0086F2 F0               [24]  753 	movx	@dptr,a
      0086F3 A3               [24]  754 	inc	dptr
      0086F4 F0               [24]  755 	movx	@dptr,a
      0086F5 A3               [24]  756 	inc	dptr
      0086F6 F0               [24]  757 	movx	@dptr,a
      0086F7 A3               [24]  758 	inc	dptr
      0086F8 F0               [24]  759 	movx	@dptr,a
      0086F9 A3               [24]  760 	inc	dptr
      0086FA F0               [24]  761 	movx	@dptr,a
      0086FB A3               [24]  762 	inc	dptr
      0086FC F0               [24]  763 	movx	@dptr,a
      0086FD A3               [24]  764 	inc	dptr
      0086FE F0               [24]  765 	movx	@dptr,a
                                    766 ;	quantum/eeconfig.c:65: eeprom_update_block(&dummy, EECONFIG_RGB_MATRIX, sizeof(uint64_t));
      0086FF 90 05 B1         [24]  767 	mov	dptr,#_eeprom_update_block_PARM_2
      008702 74 18            [12]  768 	mov	a,#0x18
      008704 F0               [24]  769 	movx	@dptr,a
      008705 E4               [12]  770 	clr	a
      008706 A3               [24]  771 	inc	dptr
      008707 F0               [24]  772 	movx	@dptr,a
      008708 A3               [24]  773 	inc	dptr
      008709 F0               [24]  774 	movx	@dptr,a
      00870A 90 05 B4         [24]  775 	mov	dptr,#_eeprom_update_block_PARM_3
      00870D 74 08            [12]  776 	mov	a,#0x08
      00870F F0               [24]  777 	movx	@dptr,a
      008710 E4               [12]  778 	clr	a
      008711 A3               [24]  779 	inc	dptr
      008712 F0               [24]  780 	movx	@dptr,a
      008713 90 09 29         [24]  781 	mov	dptr,#_eeconfig_init_quantum_dummy_10001_235
      008716 F5 F0            [12]  782 	mov	b,a
      008718 12 45 CF         [24]  783 	lcall	_eeprom_update_block
                                    784 ;	quantum/eeconfig.c:66: eeprom_update_dword(EECONFIG_HAPTIC, 0);
      00871B 90 05 C2         [24]  785 	mov	dptr,#_eeprom_update_dword_PARM_2
      00871E E4               [12]  786 	clr	a
      00871F F0               [24]  787 	movx	@dptr,a
      008720 A3               [24]  788 	inc	dptr
      008721 F0               [24]  789 	movx	@dptr,a
      008722 A3               [24]  790 	inc	dptr
      008723 F0               [24]  791 	movx	@dptr,a
      008724 A3               [24]  792 	inc	dptr
      008725 F0               [24]  793 	movx	@dptr,a
      008726 90 00 20         [24]  794 	mov	dptr,#0x0020
      008729 F5 F0            [12]  795 	mov	b,a
      00872B 12 47 4C         [24]  796 	lcall	_eeprom_update_dword
                                    797 ;	quantum/eeconfig.c:83: via_eeprom_set_valid(false);
      00872E 75 82 00         [24]  798 	mov	dpl, #0x00
      008731 12 A0 89         [24]  799 	lcall	_via_eeprom_set_valid
                                    800 ;	quantum/eeconfig.c:84: eeconfig_init_via();
      008734 12 A0 EB         [24]  801 	lcall	_eeconfig_init_via
                                    802 ;	quantum/eeconfig.c:87: eeconfig_init_kb();
                                    803 ;	quantum/eeconfig.c:88: }
      008737 02 86 37         [24]  804 	ljmp	_eeconfig_init_kb
                                    805 ;------------------------------------------------------------
                                    806 ;Allocation info for local variables in function 'eeconfig_init'
                                    807 ;------------------------------------------------------------
                                    808 ;	quantum/eeconfig.c:94: void eeconfig_init(void) {
                                    809 ;	-----------------------------------------
                                    810 ;	 function eeconfig_init
                                    811 ;	-----------------------------------------
      00873A                        812 _eeconfig_init:
                                    813 ;	quantum/eeconfig.c:95: eeconfig_init_quantum();
                                    814 ;	quantum/eeconfig.c:96: }
      00873A 02 86 43         [24]  815 	ljmp	_eeconfig_init_quantum
                                    816 ;------------------------------------------------------------
                                    817 ;Allocation info for local variables in function 'eeconfig_enable'
                                    818 ;------------------------------------------------------------
                                    819 ;	quantum/eeconfig.c:102: void eeconfig_enable(void) {
                                    820 ;	-----------------------------------------
                                    821 ;	 function eeconfig_disable
                                    822 ;	-----------------------------------------
      00873D                        823 _eeconfig_disable:
                                    824 ;	quantum/eeconfig.c:112: eeprom_driver_erase();
      00873D 12 3F 98         [24]  825 	lcall	_eeprom_driver_erase
                                    826 ;	quantum/eeconfig.c:114: eeprom_update_word(EECONFIG_MAGIC, EECONFIG_MAGIC_NUMBER_OFF);
      008740 90 05 BD         [24]  827 	mov	dptr,#_eeprom_update_word_PARM_2
      008743 74 FF            [12]  828 	mov	a,#0xff
      008745 F0               [24]  829 	movx	@dptr,a
      008746 A3               [24]  830 	inc	dptr
      008747 F0               [24]  831 	movx	@dptr,a
      008748 90 00 00         [24]  832 	mov	dptr,#0x0000
      00874B 75 F0 00         [24]  833 	mov	b, #0x00
                                    834 ;	quantum/eeconfig.c:115: }
      00874E 02 46 F7         [24]  835 	ljmp	_eeprom_update_word
                                    836 ;------------------------------------------------------------
                                    837 ;Allocation info for local variables in function 'eeconfig_is_enabled'
                                    838 ;------------------------------------------------------------
                                    839 ;sloc0         Allocated with name '_eeconfig_is_enabled_sloc0_1_0'
                                    840 ;is_eeprom_enabled Allocated with name '_eeconfig_is_enabled_is_eeprom_enabled_10000_243'
                                    841 ;------------------------------------------------------------
                                    842 ;	quantum/eeconfig.c:121: __xdata bool eeconfig_is_enabled(void) {
                                    843 ;	-----------------------------------------
                                    844 ;	 function eeconfig_is_enabled
                                    845 ;	-----------------------------------------
      008751                        846 _eeconfig_is_enabled:
                                    847 ;	quantum/eeconfig.c:122: __xdata bool is_eeprom_enabled = (eeprom_read_word(EECONFIG_MAGIC) == EECONFIG_MAGIC_NUMBER);
      008751 90 00 00         [24]  848 	mov	dptr,#0x0000
      008754 75 F0 00         [24]  849 	mov	b, #0x00
      008757 12 44 8A         [24]  850 	lcall	_eeprom_read_word
      00875A AE 82            [24]  851 	mov	r6, dpl
      00875C AF 83            [24]  852 	mov	r7, dph
      00875E E4               [12]  853 	clr	a
      00875F BE E6 04         [24]  854 	cjne	r6,#0xe6,00112$
      008762 BF FE 01         [24]  855 	cjne	r7,#0xfe,00112$
      008765 04               [12]  856 	inc	a
      008766                        857 00112$:
      008766 F5 18            [12]  858 	mov	_eeconfig_is_enabled_sloc0_1_0,a
      008768 90 09 31         [24]  859 	mov	dptr,#_eeconfig_is_enabled_is_eeprom_enabled_10000_243
      00876B F0               [24]  860 	movx	@dptr,a
                                    861 ;	quantum/eeconfig.c:124: if (is_eeprom_enabled) {
      00876C E5 18            [12]  862 	mov	a,_eeconfig_is_enabled_sloc0_1_0
      00876E 60 09            [24]  863 	jz	00102$
                                    864 ;	quantum/eeconfig.c:125: is_eeprom_enabled = via_eeprom_is_valid();
      008770 12 A0 50         [24]  865 	lcall	_via_eeprom_is_valid
      008773 E5 82            [12]  866 	mov	a, dpl
      008775 90 09 31         [24]  867 	mov	dptr,#_eeconfig_is_enabled_is_eeprom_enabled_10000_243
      008778 F0               [24]  868 	movx	@dptr,a
      008779                        869 00102$:
                                    870 ;	quantum/eeconfig.c:128: return is_eeprom_enabled;
      008779 90 09 31         [24]  871 	mov	dptr,#_eeconfig_is_enabled_is_eeprom_enabled_10000_243
      00877C E0               [24]  872 	movx	a,@dptr
                                    873 ;	quantum/eeconfig.c:129: }
      00877D F5 82            [12]  874 	mov	dpl,a
      00877F 22               [24]  875 	ret
                                    876 ;------------------------------------------------------------
                                    877 ;Allocation info for local variables in function 'eeconfig_is_disabled'
                                    878 ;------------------------------------------------------------
                                    879 ;sloc0         Allocated with name '_eeconfig_is_disabled_sloc0_1_0'
                                    880 ;is_eeprom_disabled Allocated with name '_eeconfig_is_disabled_is_eeprom_disabled_10000_247'
                                    881 ;------------------------------------------------------------
                                    882 ;	quantum/eeconfig.c:135: __xdata bool eeconfig_is_disabled(void) {
                                    883 ;	-----------------------------------------
                                    884 ;	 function eeconfig_read_debug
                                    885 ;	-----------------------------------------
      008780                        886 _eeconfig_read_debug:
                                    887 ;	quantum/eeconfig.c:150: return eeprom_read_byte(EECONFIG_DEBUG);
      008780 90 00 02         [24]  888 	mov	dptr,#0x0002
      008783 75 F0 00         [24]  889 	mov	b, #0x00
                                    890 ;	quantum/eeconfig.c:151: }
      008786 02 44 1B         [24]  891 	ljmp	_eeprom_read_byte
                                    892 ;------------------------------------------------------------
                                    893 ;Allocation info for local variables in function 'eeconfig_update_debug'
                                    894 ;------------------------------------------------------------
                                    895 ;val           Allocated with name '_eeconfig_update_debug_val_10000_252'
                                    896 ;------------------------------------------------------------
                                    897 ;	quantum/eeconfig.c:156: void eeconfig_update_debug(uint8_t val) {
                                    898 ;	-----------------------------------------
                                    899 ;	 function eeconfig_read_default_layer
                                    900 ;	-----------------------------------------
      008789                        901 _eeconfig_read_default_layer:
                                    902 ;	quantum/eeconfig.c:165: return eeprom_read_byte(EECONFIG_DEFAULT_LAYER);
      008789 90 00 03         [24]  903 	mov	dptr,#0x0003
      00878C 75 F0 00         [24]  904 	mov	b, #0x00
                                    905 ;	quantum/eeconfig.c:166: }
      00878F 02 44 1B         [24]  906 	ljmp	_eeprom_read_byte
                                    907 ;------------------------------------------------------------
                                    908 ;Allocation info for local variables in function 'eeconfig_update_default_layer'
                                    909 ;------------------------------------------------------------
                                    910 ;val           Allocated with name '_eeconfig_update_default_layer_val_10000_256'
                                    911 ;------------------------------------------------------------
                                    912 ;	quantum/eeconfig.c:171: void eeconfig_update_default_layer(uint8_t val) {
                                    913 ;	-----------------------------------------
                                    914 ;	 function eeconfig_read_keymap
                                    915 ;	-----------------------------------------
      008792                        916 _eeconfig_read_keymap:
                                    917 ;	quantum/eeconfig.c:180: return eeprom_read_word(EECONFIG_KEYMAP);
      008792 90 00 04         [24]  918 	mov	dptr,#0x0004
      008795 75 F0 00         [24]  919 	mov	b, #0x00
                                    920 ;	quantum/eeconfig.c:181: }
      008798 02 44 8A         [24]  921 	ljmp	_eeprom_read_word
                                    922 ;------------------------------------------------------------
                                    923 ;Allocation info for local variables in function 'eeconfig_update_keymap'
                                    924 ;------------------------------------------------------------
                                    925 ;val           Allocated with name '_eeconfig_update_keymap_val_10000_260'
                                    926 ;------------------------------------------------------------
                                    927 ;	quantum/eeconfig.c:186: void eeconfig_update_keymap(uint16_t val) {
                                    928 ;	-----------------------------------------
                                    929 ;	 function eeconfig_update_kb
                                    930 ;	-----------------------------------------
      00879B                        931 _eeconfig_update_kb:
      00879B AF 82            [24]  932 	mov	r7,dpl
      00879D AE 83            [24]  933 	mov	r6,dph
      00879F AD F0            [24]  934 	mov	r5,b
      0087A1 FC               [12]  935 	mov	r4,a
      0087A2 90 09 32         [24]  936 	mov	dptr,#_eeconfig_update_kb_val_10000_268
      0087A5 12 87 F1         [24]  937 	lcall	_ak820_outline_0028
                                    938 ;	quantum/eeconfig.c:218: eeprom_update_dword(EECONFIG_KEYBOARD, val);
      0087A8 90 09 32         [24]  939 	mov	dptr,#_eeconfig_update_kb_val_10000_268
      0087AB E0               [24]  940 	movx	a,@dptr
      0087AC FC               [12]  941 	mov	r4,a
      0087AD A3               [24]  942 	inc	dptr
      0087AE 12 73 B8         [24]  943 	lcall	_ak820_outline_0002
      0087B1 90 05 C2         [24]  944 	mov	dptr,#_eeprom_update_dword_PARM_2
      0087B4 12 87 E5         [24]  945 	lcall	_ak820_outline_0008
      0087B7 90 00 0F         [24]  946 	mov	dptr,#0x000f
      0087BA 75 F0 00         [24]  947 	mov	b, #0x00
                                    948 ;	quantum/eeconfig.c:219: }
      0087BD 02 47 4C         [24]  949 	ljmp	_eeprom_update_dword
                                    950 ;------------------------------------------------------------
                                    951 ;Allocation info for local variables in function 'eeconfig_read_user'
                                    952 ;------------------------------------------------------------
                                    953 ;	quantum/eeconfig.c:227: uint32_t eeconfig_read_user(void) {
                                    954 ;	-----------------------------------------
                                    955 ;	 function eeconfig_update_user
                                    956 ;	-----------------------------------------
      0087C0                        957 _eeconfig_update_user:
      0087C0 AF 82            [24]  958 	mov	r7,dpl
      0087C2 AE 83            [24]  959 	mov	r6,dph
      0087C4 AD F0            [24]  960 	mov	r5,b
      0087C6 FC               [12]  961 	mov	r4,a
      0087C7 90 09 36         [24]  962 	mov	dptr,#_eeconfig_update_user_val_10000_272
      0087CA 12 87 F1         [24]  963 	lcall	_ak820_outline_0028
                                    964 ;	quantum/eeconfig.c:235: eeprom_update_dword(EECONFIG_USER, val);
      0087CD 90 09 36         [24]  965 	mov	dptr,#_eeconfig_update_user_val_10000_272
      0087D0 E0               [24]  966 	movx	a,@dptr
      0087D1 FC               [12]  967 	mov	r4,a
      0087D2 A3               [24]  968 	inc	dptr
      0087D3 12 73 B8         [24]  969 	lcall	_ak820_outline_0002
      0087D6 90 05 C2         [24]  970 	mov	dptr,#_eeprom_update_dword_PARM_2
      0087D9 12 87 E5         [24]  971 	lcall	_ak820_outline_0008
      0087DC 90 00 13         [24]  972 	mov	dptr,#0x0013
      0087DF 75 F0 00         [24]  973 	mov	b, #0x00
                                    974 ;	quantum/eeconfig.c:236: }
      0087E2 02 47 4C         [24]  975 	ljmp	_eeprom_update_dword
                                    976 ;------------------------------------------------------------
                                    977 ;Allocation info for local variables in function 'eeconfig_read_haptic'
                                    978 ;------------------------------------------------------------
                                    979 ;	quantum/eeconfig.c:243: uint32_t eeconfig_read_haptic(void) {
                                    980 ;	-----------------------------------------
                                    981 	.area CSEG    (CODE)
                                    982 	.area CONST   (CODE)
                                    983 	.area XINIT   (CODE)
                                    984 	.area CABS    (ABS,CODE)
                                    985 
                                    986 ; Experimental exact instruction outlining.
                                    987 	.globl _ak820_outline_0002
                                    988 	.globl _ak820_outline_0008
                                    989 	.globl _ak820_outline_0028
                                    990 
                                    991 	.area CSEG (CODE)
                                    992 ; function ak820_outline_0008
      0087E5                        993 _ak820_outline_0008:
      0087E5 EC               [12]  994 	mov	a,r4
      0087E6 F0               [24]  995 	movx	@dptr,a
      0087E7 ED               [12]  996 	mov	a,r5
      0087E8 A3               [24]  997 	inc	dptr
      0087E9 F0               [24]  998 	movx	@dptr,a
      0087EA EE               [12]  999 	mov	a,r6
      0087EB A3               [24] 1000 	inc	dptr
      0087EC F0               [24] 1001 	movx	@dptr,a
      0087ED EF               [12] 1002 	mov	a,r7
      0087EE A3               [24] 1003 	inc	dptr
      0087EF F0               [24] 1004 	movx	@dptr,a
      0087F0 22               [24] 1005 	ret
                                   1006 
                                   1007 	.area CSEG (CODE)
                                   1008 ; function ak820_outline_0028
      0087F1                       1009 _ak820_outline_0028:
      0087F1 EF               [12] 1010 	mov	a,r7
      0087F2 F0               [24] 1011 	movx	@dptr,a
      0087F3 EE               [12] 1012 	mov	a,r6
      0087F4 A3               [24] 1013 	inc	dptr
      0087F5 F0               [24] 1014 	movx	@dptr,a
      0087F6 ED               [12] 1015 	mov	a,r5
      0087F7 A3               [24] 1016 	inc	dptr
      0087F8 F0               [24] 1017 	movx	@dptr,a
      0087F9 EC               [12] 1018 	mov	a,r4
      0087FA A3               [24] 1019 	inc	dptr
      0087FB F0               [24] 1020 	movx	@dptr,a
      0087FC 22               [24] 1021 	ret
