                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module ak820_flash
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _ADC_START
                                     12 	.globl _S0_R_FIFO
                                     13 	.globl _S0_T_FIFO
                                     14 	.globl _S0_FREE
                                     15 	.globl _S0_IF_BYTE
                                     16 	.globl _S0_IF_FIRST
                                     17 	.globl _S0_IF_OV
                                     18 	.globl _S0_FST_ACT
                                     19 	.globl _CP_RL2
                                     20 	.globl _C_T2
                                     21 	.globl _TR2
                                     22 	.globl _EXEN2
                                     23 	.globl _TCLK
                                     24 	.globl _RCLK
                                     25 	.globl _EXF2
                                     26 	.globl _CAP1F
                                     27 	.globl _TF2
                                     28 	.globl _RI
                                     29 	.globl _TI
                                     30 	.globl _RB8
                                     31 	.globl _TB8
                                     32 	.globl _REN
                                     33 	.globl _SM2
                                     34 	.globl _SM1
                                     35 	.globl _SM0
                                     36 	.globl _IT0
                                     37 	.globl _IE0
                                     38 	.globl _IT1
                                     39 	.globl _IE1
                                     40 	.globl _TR0
                                     41 	.globl _TF0
                                     42 	.globl _TR1
                                     43 	.globl _TF1
                                     44 	.globl _P4_0
                                     45 	.globl _P4_1
                                     46 	.globl _P4_2
                                     47 	.globl _P4_3
                                     48 	.globl _P4_4
                                     49 	.globl _P4_5
                                     50 	.globl _P4_6
                                     51 	.globl _RXD
                                     52 	.globl _TXD
                                     53 	.globl _INT0
                                     54 	.globl _INT1
                                     55 	.globl _T0
                                     56 	.globl _T1
                                     57 	.globl _MOSI1
                                     58 	.globl _MISO1
                                     59 	.globl _SCK1
                                     60 	.globl _P3_0
                                     61 	.globl _P3_1
                                     62 	.globl _P3_2
                                     63 	.globl _P3_3
                                     64 	.globl _P3_4
                                     65 	.globl _P3_5
                                     66 	.globl _P3_6
                                     67 	.globl _P3_7
                                     68 	.globl _CAP1_
                                     69 	.globl _T2_
                                     70 	.globl _CAP2_
                                     71 	.globl _T2EX_
                                     72 	.globl _RXD1
                                     73 	.globl _TXD1
                                     74 	.globl _P2_0
                                     75 	.globl _P2_1
                                     76 	.globl _P2_2
                                     77 	.globl _P2_3
                                     78 	.globl _P2_4
                                     79 	.globl _P2_5
                                     80 	.globl _P2_6
                                     81 	.globl _P2_7
                                     82 	.globl _AIN0
                                     83 	.globl _AIN1
                                     84 	.globl _AIN2
                                     85 	.globl _AIN3
                                     86 	.globl _AIN4
                                     87 	.globl _AIN5
                                     88 	.globl _AIN6
                                     89 	.globl _AIN7
                                     90 	.globl _CAP1
                                     91 	.globl _T2
                                     92 	.globl _CAP2
                                     93 	.globl _T2EX
                                     94 	.globl _INT0_
                                     95 	.globl _SCS
                                     96 	.globl _MOSI
                                     97 	.globl _MISO
                                     98 	.globl _SCK
                                     99 	.globl _RXD1_
                                    100 	.globl _TXD1_
                                    101 	.globl _P1_0
                                    102 	.globl _P1_1
                                    103 	.globl _P1_2
                                    104 	.globl _P1_3
                                    105 	.globl _P1_4
                                    106 	.globl _P1_5
                                    107 	.globl _P1_6
                                    108 	.globl _P1_7
                                    109 	.globl _AIN8
                                    110 	.globl _AIN9
                                    111 	.globl _AIN10
                                    112 	.globl _AIN11
                                    113 	.globl _AIN12
                                    114 	.globl _AIN13
                                    115 	.globl _RXD_
                                    116 	.globl _TXD_
                                    117 	.globl _SCL0
                                    118 	.globl _SDA0
                                    119 	.globl _P0_0
                                    120 	.globl _P0_1
                                    121 	.globl _P0_2
                                    122 	.globl _P0_3
                                    123 	.globl _P0_4
                                    124 	.globl _P0_5
                                    125 	.globl _P0_6
                                    126 	.globl _P0_7
                                    127 	.globl _IE_SPI0
                                    128 	.globl _IE_USB
                                    129 	.globl _IE_ADC
                                    130 	.globl _IE_UART1
                                    131 	.globl _IE_PWM_I2C
                                    132 	.globl _IE_GPIO
                                    133 	.globl _IE_WDOG
                                    134 	.globl _PX0
                                    135 	.globl _PT0
                                    136 	.globl _PX1
                                    137 	.globl _PT1
                                    138 	.globl _PS
                                    139 	.globl _PT2
                                    140 	.globl _PL_FLAG
                                    141 	.globl _PH_FLAG
                                    142 	.globl _EX0
                                    143 	.globl _ET0
                                    144 	.globl _EX1
                                    145 	.globl _ET1
                                    146 	.globl _ES
                                    147 	.globl _ET2
                                    148 	.globl _E_DIS
                                    149 	.globl _EA
                                    150 	.globl _P
                                    151 	.globl _F1
                                    152 	.globl _OV
                                    153 	.globl _RS0
                                    154 	.globl _RS1
                                    155 	.globl _F0
                                    156 	.globl _AC
                                    157 	.globl _CY
                                    158 	.globl _I2CS_INT_ST
                                    159 	.globl _I2CX_INT
                                    160 	.globl _LED_STATUS
                                    161 	.globl _LED_DMA_H
                                    162 	.globl _LED_DMA_L
                                    163 	.globl _LED_DMA
                                    164 	.globl _LED_PWM_OE
                                    165 	.globl _LED_COMMON
                                    166 	.globl _ADC_CHAN
                                    167 	.globl _ADC_DAT_H
                                    168 	.globl _ADC_DAT_L
                                    169 	.globl _ADC_DAT
                                    170 	.globl _ADC_CTRL
                                    171 	.globl _SPI1_CK_SE
                                    172 	.globl _SPI1_CTRL
                                    173 	.globl _SPI1_DATA
                                    174 	.globl _SPI1_STAT
                                    175 	.globl _SIF1
                                    176 	.globl _SBAUD1
                                    177 	.globl _SBUF1
                                    178 	.globl _SCON1
                                    179 	.globl _SPI0_SETUP
                                    180 	.globl _SPI0_CK_SE
                                    181 	.globl _SPI0_CTRL
                                    182 	.globl _SPI0_DATA
                                    183 	.globl _SPI0_STAT
                                    184 	.globl _T2CAP1H
                                    185 	.globl _T2CAP1L
                                    186 	.globl _T2CAP1
                                    187 	.globl _TH2
                                    188 	.globl _TL2
                                    189 	.globl _T2COUNT
                                    190 	.globl _RCAP2H
                                    191 	.globl _RCAP2L
                                    192 	.globl _RCAP2
                                    193 	.globl _T2MOD
                                    194 	.globl _T2CON
                                    195 	.globl _SBUF
                                    196 	.globl _SCON
                                    197 	.globl _TH1
                                    198 	.globl _TH0
                                    199 	.globl _TL1
                                    200 	.globl _TL0
                                    201 	.globl _TMOD
                                    202 	.globl _TCON
                                    203 	.globl _XBUS_AUX
                                    204 	.globl _P7
                                    205 	.globl _P6_DIR
                                    206 	.globl _P6_OUT_PU
                                    207 	.globl _P6_IN
                                    208 	.globl _P5_DIR
                                    209 	.globl _P5_OUT_PU
                                    210 	.globl _P5_IN
                                    211 	.globl _P4_LED_KEY
                                    212 	.globl _P4_DIR_PU
                                    213 	.globl _P4_MOD_OC
                                    214 	.globl _P4
                                    215 	.globl _P3_DIR_PU
                                    216 	.globl _P3_MOD_OC
                                    217 	.globl _P3
                                    218 	.globl _P2_DIR_PU
                                    219 	.globl _P2_MOD_OC
                                    220 	.globl _P2
                                    221 	.globl _P1_DIR_PU
                                    222 	.globl _P1_MOD_OC
                                    223 	.globl _P1
                                    224 	.globl _P0_DIR_PU
                                    225 	.globl _P0_MOD_OC
                                    226 	.globl _P0
                                    227 	.globl _ROM_CTRL
                                    228 	.globl _ROM_DATA_HH
                                    229 	.globl _ROM_DATA_HL
                                    230 	.globl _ROM_DATA_HI
                                    231 	.globl _ROM_ADDR_H
                                    232 	.globl _ROM_ADDR_L
                                    233 	.globl _ROM_ADDR
                                    234 	.globl _GPIO_IE
                                    235 	.globl _IP_EX
                                    236 	.globl _IE_EX
                                    237 	.globl _IP
                                    238 	.globl _IE
                                    239 	.globl _WDOG_COUNT
                                    240 	.globl _RESET_KEEP
                                    241 	.globl _WAKE_CTRL
                                    242 	.globl _CLOCK_CFG
                                    243 	.globl _POWER_CFG
                                    244 	.globl _PCON
                                    245 	.globl _GLOBAL_CFG
                                    246 	.globl _SAFE_MOD
                                    247 	.globl _DPH
                                    248 	.globl _DPL
                                    249 	.globl _SP
                                    250 	.globl _A_INV
                                    251 	.globl _B
                                    252 	.globl _ACC
                                    253 	.globl _PSW
                                    254 	.globl _ak820_flash_program_page_PARM_2
                                    255 	.globl _ak820_flash_program_PARM_2
                                    256 	.globl _ak820_flash_diagnostic
                                    257 	.globl _ak820_flash_read
                                    258 	.globl _ak820_flash_erase
                                    259 	.globl _ak820_flash_program
                                    260 	.globl _ak820_flash_program_page
                                    261 ;--------------------------------------------------------
                                    262 ; special function registers
                                    263 ;--------------------------------------------------------
                                    264 	.area RSEG    (ABS,DATA)
      000000                        265 	.org 0x0000
                           0000D0   266 _PSW	=	0x00d0
                           0000E0   267 _ACC	=	0x00e0
                           0000F0   268 _B	=	0x00f0
                           0000FD   269 _A_INV	=	0x00fd
                           000081   270 _SP	=	0x0081
                           000082   271 _DPL	=	0x0082
                           000083   272 _DPH	=	0x0083
                           0000A1   273 _SAFE_MOD	=	0x00a1
                           0000B1   274 _GLOBAL_CFG	=	0x00b1
                           000087   275 _PCON	=	0x0087
                           0000BA   276 _POWER_CFG	=	0x00ba
                           0000B9   277 _CLOCK_CFG	=	0x00b9
                           0000A9   278 _WAKE_CTRL	=	0x00a9
                           0000FE   279 _RESET_KEEP	=	0x00fe
                           0000FF   280 _WDOG_COUNT	=	0x00ff
                           0000A8   281 _IE	=	0x00a8
                           0000B8   282 _IP	=	0x00b8
                           0000E8   283 _IE_EX	=	0x00e8
                           0000E9   284 _IP_EX	=	0x00e9
                           0000B2   285 _GPIO_IE	=	0x00b2
                           008584   286 _ROM_ADDR	=	0x8584
                           000084   287 _ROM_ADDR_L	=	0x0084
                           000085   288 _ROM_ADDR_H	=	0x0085
                           008F8E   289 _ROM_DATA_HI	=	0x8f8e
                           00008E   290 _ROM_DATA_HL	=	0x008e
                           00008F   291 _ROM_DATA_HH	=	0x008f
                           000086   292 _ROM_CTRL	=	0x0086
                           000080   293 _P0	=	0x0080
                           0000C4   294 _P0_MOD_OC	=	0x00c4
                           0000C5   295 _P0_DIR_PU	=	0x00c5
                           000090   296 _P1	=	0x0090
                           000092   297 _P1_MOD_OC	=	0x0092
                           000093   298 _P1_DIR_PU	=	0x0093
                           0000A0   299 _P2	=	0x00a0
                           000094   300 _P2_MOD_OC	=	0x0094
                           000095   301 _P2_DIR_PU	=	0x0095
                           0000B0   302 _P3	=	0x00b0
                           000096   303 _P3_MOD_OC	=	0x0096
                           000097   304 _P3_DIR_PU	=	0x0097
                           0000C0   305 _P4	=	0x00c0
                           0000C2   306 _P4_MOD_OC	=	0x00c2
                           0000C3   307 _P4_DIR_PU	=	0x00c3
                           0000C1   308 _P4_LED_KEY	=	0x00c1
                           0000AA   309 _P5_IN	=	0x00aa
                           0000AB   310 _P5_OUT_PU	=	0x00ab
                           0000AC   311 _P5_DIR	=	0x00ac
                           0000AD   312 _P6_IN	=	0x00ad
                           0000AE   313 _P6_OUT_PU	=	0x00ae
                           0000AF   314 _P6_DIR	=	0x00af
                           0000F1   315 _P7	=	0x00f1
                           0000A2   316 _XBUS_AUX	=	0x00a2
                           000088   317 _TCON	=	0x0088
                           000089   318 _TMOD	=	0x0089
                           00008A   319 _TL0	=	0x008a
                           00008B   320 _TL1	=	0x008b
                           00008C   321 _TH0	=	0x008c
                           00008D   322 _TH1	=	0x008d
                           000098   323 _SCON	=	0x0098
                           000099   324 _SBUF	=	0x0099
                           0000C8   325 _T2CON	=	0x00c8
                           0000C9   326 _T2MOD	=	0x00c9
                           00CBCA   327 _RCAP2	=	0xcbca
                           0000CA   328 _RCAP2L	=	0x00ca
                           0000CB   329 _RCAP2H	=	0x00cb
                           00CDCC   330 _T2COUNT	=	0xcdcc
                           0000CC   331 _TL2	=	0x00cc
                           0000CD   332 _TH2	=	0x00cd
                           00CFCE   333 _T2CAP1	=	0xcfce
                           0000CE   334 _T2CAP1L	=	0x00ce
                           0000CF   335 _T2CAP1H	=	0x00cf
                           0000F8   336 _SPI0_STAT	=	0x00f8
                           0000F9   337 _SPI0_DATA	=	0x00f9
                           0000FA   338 _SPI0_CTRL	=	0x00fa
                           0000FB   339 _SPI0_CK_SE	=	0x00fb
                           0000FC   340 _SPI0_SETUP	=	0x00fc
                           0000BC   341 _SCON1	=	0x00bc
                           0000BD   342 _SBUF1	=	0x00bd
                           0000BE   343 _SBAUD1	=	0x00be
                           0000BF   344 _SIF1	=	0x00bf
                           0000B4   345 _SPI1_STAT	=	0x00b4
                           0000B5   346 _SPI1_DATA	=	0x00b5
                           0000B6   347 _SPI1_CTRL	=	0x00b6
                           0000B7   348 _SPI1_CK_SE	=	0x00b7
                           0000F3   349 _ADC_CTRL	=	0x00f3
                           00F5F4   350 _ADC_DAT	=	0xf5f4
                           0000F4   351 _ADC_DAT_L	=	0x00f4
                           0000F5   352 _ADC_DAT_H	=	0x00f5
                           0000F6   353 _ADC_CHAN	=	0x00f6
                           0000A6   354 _LED_COMMON	=	0x00a6
                           0000A7   355 _LED_PWM_OE	=	0x00a7
                           00C7C6   356 _LED_DMA	=	0xc7c6
                           0000C6   357 _LED_DMA_L	=	0x00c6
                           0000C7   358 _LED_DMA_H	=	0x00c7
                           0000F7   359 _LED_STATUS	=	0x00f7
                           0000B3   360 _I2CX_INT	=	0x00b3
                           0000BB   361 _I2CS_INT_ST	=	0x00bb
                                    362 ;--------------------------------------------------------
                                    363 ; special function bits
                                    364 ;--------------------------------------------------------
                                    365 	.area RSEG    (ABS,DATA)
      000000                        366 	.org 0x0000
                           0000D7   367 _CY	=	0x00d7
                           0000D6   368 _AC	=	0x00d6
                           0000D5   369 _F0	=	0x00d5
                           0000D4   370 _RS1	=	0x00d4
                           0000D3   371 _RS0	=	0x00d3
                           0000D2   372 _OV	=	0x00d2
                           0000D1   373 _F1	=	0x00d1
                           0000D0   374 _P	=	0x00d0
                           0000AF   375 _EA	=	0x00af
                           0000AE   376 _E_DIS	=	0x00ae
                           0000AD   377 _ET2	=	0x00ad
                           0000AC   378 _ES	=	0x00ac
                           0000AB   379 _ET1	=	0x00ab
                           0000AA   380 _EX1	=	0x00aa
                           0000A9   381 _ET0	=	0x00a9
                           0000A8   382 _EX0	=	0x00a8
                           0000BF   383 _PH_FLAG	=	0x00bf
                           0000BE   384 _PL_FLAG	=	0x00be
                           0000BD   385 _PT2	=	0x00bd
                           0000BC   386 _PS	=	0x00bc
                           0000BB   387 _PT1	=	0x00bb
                           0000BA   388 _PX1	=	0x00ba
                           0000B9   389 _PT0	=	0x00b9
                           0000B8   390 _PX0	=	0x00b8
                           0000EF   391 _IE_WDOG	=	0x00ef
                           0000EE   392 _IE_GPIO	=	0x00ee
                           0000ED   393 _IE_PWM_I2C	=	0x00ed
                           0000EC   394 _IE_UART1	=	0x00ec
                           0000EB   395 _IE_ADC	=	0x00eb
                           0000E9   396 _IE_USB	=	0x00e9
                           0000E8   397 _IE_SPI0	=	0x00e8
                           000087   398 _P0_7	=	0x0087
                           000086   399 _P0_6	=	0x0086
                           000085   400 _P0_5	=	0x0085
                           000084   401 _P0_4	=	0x0084
                           000083   402 _P0_3	=	0x0083
                           000082   403 _P0_2	=	0x0082
                           000081   404 _P0_1	=	0x0081
                           000080   405 _P0_0	=	0x0080
                           000081   406 _SDA0	=	0x0081
                           000080   407 _SCL0	=	0x0080
                           000083   408 _TXD_	=	0x0083
                           000082   409 _RXD_	=	0x0082
                           000085   410 _AIN13	=	0x0085
                           000084   411 _AIN12	=	0x0084
                           000083   412 _AIN11	=	0x0083
                           000082   413 _AIN10	=	0x0082
                           000081   414 _AIN9	=	0x0081
                           000080   415 _AIN8	=	0x0080
                           000097   416 _P1_7	=	0x0097
                           000096   417 _P1_6	=	0x0096
                           000095   418 _P1_5	=	0x0095
                           000094   419 _P1_4	=	0x0094
                           000093   420 _P1_3	=	0x0093
                           000092   421 _P1_2	=	0x0092
                           000091   422 _P1_1	=	0x0091
                           000090   423 _P1_0	=	0x0090
                           000097   424 _TXD1_	=	0x0097
                           000096   425 _RXD1_	=	0x0096
                           000097   426 _SCK	=	0x0097
                           000096   427 _MISO	=	0x0096
                           000095   428 _MOSI	=	0x0095
                           000094   429 _SCS	=	0x0094
                           000092   430 _INT0_	=	0x0092
                           000091   431 _T2EX	=	0x0091
                           000091   432 _CAP2	=	0x0091
                           000090   433 _T2	=	0x0090
                           000090   434 _CAP1	=	0x0090
                           000097   435 _AIN7	=	0x0097
                           000096   436 _AIN6	=	0x0096
                           000095   437 _AIN5	=	0x0095
                           000094   438 _AIN4	=	0x0094
                           000093   439 _AIN3	=	0x0093
                           000092   440 _AIN2	=	0x0092
                           000091   441 _AIN1	=	0x0091
                           000090   442 _AIN0	=	0x0090
                           0000A7   443 _P2_7	=	0x00a7
                           0000A6   444 _P2_6	=	0x00a6
                           0000A5   445 _P2_5	=	0x00a5
                           0000A4   446 _P2_4	=	0x00a4
                           0000A3   447 _P2_3	=	0x00a3
                           0000A2   448 _P2_2	=	0x00a2
                           0000A1   449 _P2_1	=	0x00a1
                           0000A0   450 _P2_0	=	0x00a0
                           0000A7   451 _TXD1	=	0x00a7
                           0000A6   452 _RXD1	=	0x00a6
                           0000A5   453 _T2EX_	=	0x00a5
                           0000A5   454 _CAP2_	=	0x00a5
                           0000A4   455 _T2_	=	0x00a4
                           0000A4   456 _CAP1_	=	0x00a4
                           0000B7   457 _P3_7	=	0x00b7
                           0000B6   458 _P3_6	=	0x00b6
                           0000B5   459 _P3_5	=	0x00b5
                           0000B4   460 _P3_4	=	0x00b4
                           0000B3   461 _P3_3	=	0x00b3
                           0000B2   462 _P3_2	=	0x00b2
                           0000B1   463 _P3_1	=	0x00b1
                           0000B0   464 _P3_0	=	0x00b0
                           0000B7   465 _SCK1	=	0x00b7
                           0000B6   466 _MISO1	=	0x00b6
                           0000B5   467 _MOSI1	=	0x00b5
                           0000B5   468 _T1	=	0x00b5
                           0000B4   469 _T0	=	0x00b4
                           0000B3   470 _INT1	=	0x00b3
                           0000B2   471 _INT0	=	0x00b2
                           0000B1   472 _TXD	=	0x00b1
                           0000B0   473 _RXD	=	0x00b0
                           0000C6   474 _P4_6	=	0x00c6
                           0000C5   475 _P4_5	=	0x00c5
                           0000C4   476 _P4_4	=	0x00c4
                           0000C3   477 _P4_3	=	0x00c3
                           0000C2   478 _P4_2	=	0x00c2
                           0000C1   479 _P4_1	=	0x00c1
                           0000C0   480 _P4_0	=	0x00c0
                           00008F   481 _TF1	=	0x008f
                           00008E   482 _TR1	=	0x008e
                           00008D   483 _TF0	=	0x008d
                           00008C   484 _TR0	=	0x008c
                           00008B   485 _IE1	=	0x008b
                           00008A   486 _IT1	=	0x008a
                           000089   487 _IE0	=	0x0089
                           000088   488 _IT0	=	0x0088
                           00009F   489 _SM0	=	0x009f
                           00009E   490 _SM1	=	0x009e
                           00009D   491 _SM2	=	0x009d
                           00009C   492 _REN	=	0x009c
                           00009B   493 _TB8	=	0x009b
                           00009A   494 _RB8	=	0x009a
                           000099   495 _TI	=	0x0099
                           000098   496 _RI	=	0x0098
                           0000CF   497 _TF2	=	0x00cf
                           0000CF   498 _CAP1F	=	0x00cf
                           0000CE   499 _EXF2	=	0x00ce
                           0000CD   500 _RCLK	=	0x00cd
                           0000CC   501 _TCLK	=	0x00cc
                           0000CB   502 _EXEN2	=	0x00cb
                           0000CA   503 _TR2	=	0x00ca
                           0000C9   504 _C_T2	=	0x00c9
                           0000C8   505 _CP_RL2	=	0x00c8
                           0000FF   506 _S0_FST_ACT	=	0x00ff
                           0000FE   507 _S0_IF_OV	=	0x00fe
                           0000FD   508 _S0_IF_FIRST	=	0x00fd
                           0000FC   509 _S0_IF_BYTE	=	0x00fc
                           0000FB   510 _S0_FREE	=	0x00fb
                           0000FA   511 _S0_T_FIFO	=	0x00fa
                           0000F8   512 _S0_R_FIFO	=	0x00f8
                           0000F7   513 _ADC_START	=	0x00f7
                                    514 ;--------------------------------------------------------
                                    515 ; overlayable register banks
                                    516 ;--------------------------------------------------------
                                    517 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        518 	.ds 8
                                    519 ;--------------------------------------------------------
                                    520 ; internal ram data
                                    521 ;--------------------------------------------------------
                                    522 	.area DSEG    (DATA)
      000008                        523 _ak820_flash_program_sloc0_1_0:
      000008                        524 	.ds 2
                                    525 ;--------------------------------------------------------
                                    526 ; overlayable items in internal ram
                                    527 ;--------------------------------------------------------
                                    528 ;--------------------------------------------------------
                                    529 ; indirectly addressable internal ram data
                                    530 ;--------------------------------------------------------
                                    531 	.area ISEG    (DATA)
                                    532 ;--------------------------------------------------------
                                    533 ; absolute internal ram data
                                    534 ;--------------------------------------------------------
                                    535 	.area IABS    (ABS,DATA)
                                    536 	.area IABS    (ABS,DATA)
                                    537 ;--------------------------------------------------------
                                    538 ; bit data
                                    539 ;--------------------------------------------------------
                                    540 	.area BSEG    (BIT)
      000000                        541 _flash_operation_sloc0_1_0:
      000000                        542 	.ds 1
                                    543 ;--------------------------------------------------------
                                    544 ; paged external ram data
                                    545 ;--------------------------------------------------------
                                    546 	.area PSEG    (PAG,XDATA)
                                    547 ;--------------------------------------------------------
                                    548 ; uninitialized external ram data
                                    549 ;--------------------------------------------------------
                                    550 	.area XSEG    (XDATA)
      00041B                        551 _ak820_flash_diagnostic::
      00041B                        552 	.ds 6
      000421                        553 _block_storage:
      000421                        554 	.ds 127
      0004A0                        555 _block_data:
      0004A0                        556 	.ds 2
      0004A2                        557 _ak820_flash_read_address_10000_15:
      0004A2                        558 	.ds 2
      0004A4                        559 _flash_operation_PARM_2:
      0004A4                        560 	.ds 1
      0004A5                        561 _flash_operation_PARM_3:
      0004A5                        562 	.ds 1
      0004A6                        563 _flash_operation_address_10000_17:
      0004A6                        564 	.ds 2
      0004A8                        565 _flash_operation_previous_ie_10000_18:
      0004A8                        566 	.ds 1
      0004A9                        567 _flash_operation_before_10000_18:
      0004A9                        568 	.ds 1
      0004AA                        569 _flash_operation_status_10000_18:
      0004AA                        570 	.ds 1
      0004AB                        571 _ak820_flash_erase_address_10000_23:
      0004AB                        572 	.ds 2
      0004AD                        573 _ak820_flash_program_PARM_2:
      0004AD                        574 	.ds 1
      0004AE                        575 _ak820_flash_program_address_10000_30:
      0004AE                        576 	.ds 2
      0004B0                        577 _ak820_flash_program_page_PARM_2:
      0004B0                        578 	.ds 2
      0004B2                        579 _ak820_flash_program_page_address_10000_34:
      0004B2                        580 	.ds 2
                                    581 ;--------------------------------------------------------
                                    582 ; absolute external ram data
                                    583 ;--------------------------------------------------------
                                    584 	.area XABS    (ABS,XDATA)
                                    585 ;--------------------------------------------------------
                                    586 ; initialized external ram data
                                    587 ;--------------------------------------------------------
                                    588 	.area XISEG   (XDATA)
                                    589 	.area HOME    (CODE)
                                    590 	.area GSINIT0 (CODE)
                                    591 	.area GSINIT1 (CODE)
                                    592 	.area GSINIT2 (CODE)
                                    593 	.area GSINIT3 (CODE)
                                    594 	.area GSINIT4 (CODE)
                                    595 	.area GSINIT5 (CODE)
                                    596 	.area GSINIT  (CODE)
                                    597 	.area GSFINAL (CODE)
                                    598 	.area CSEG    (CODE)
                                    599 ;--------------------------------------------------------
                                    600 ; global & static initialisations
                                    601 ;--------------------------------------------------------
                                    602 	.area HOME    (CODE)
                                    603 	.area GSINIT  (CODE)
                                    604 	.area GSFINAL (CODE)
                                    605 	.area GSINIT  (CODE)
                                    606 ;--------------------------------------------------------
                                    607 ; Home
                                    608 ;--------------------------------------------------------
                                    609 	.area HOME    (CODE)
                                    610 	.area HOME    (CODE)
                                    611 ;--------------------------------------------------------
                                    612 ; code
                                    613 ;--------------------------------------------------------
                                    614 	.area CSEG    (CODE)
                                    615 ;------------------------------------------------------------
                                    616 ;Allocation info for local variables in function 'program_block'
                                    617 ;------------------------------------------------------------
                                    618 ;data          Allocated with name '_program_block_data_10000_11'
                                    619 ;------------------------------------------------------------
                                    620 ;	keyboards/ajazz/ak820/ak820_flash.c:19: static uint16_t program_block(const uint8_t __xdata *data) __naked {
                                    621 ;	-----------------------------------------
                                    622 ;	 function program_block
                                    623 ;	-----------------------------------------
      0034EE                        624 _program_block:
                                    625 ;	naked function: no prologue.
                                    626 ;	keyboards/ajazz/ak820/ak820_flash.c:31: __endasm;
      0034EE E5 86            [12]  627 	mov a, _ROM_CTRL
      0034F0 F5 F0            [12]  628 	mov b, a
      0034F2 30 E6 05         [24]  629 	jnb acc.6, 00001$
      0034F5 75 86 9A         [24]  630 	mov _ROM_CTRL, #0x9a
      0034F8 E5 86            [12]  631 	mov a, _ROM_CTRL
      0034FA                        632 00001$:
      0034FA F5 82            [12]  633 	mov dpl, a
      0034FC 85 F0 83         [24]  634 	mov dph, b
      0034FF 22               [24]  635 	ret
                                    636 ;	keyboards/ajazz/ak820/ak820_flash.c:32: }
                                    637 ;	naked function: no epilogue.
                                    638 ;------------------------------------------------------------
                                    639 ;Allocation info for local variables in function 'erase_page'
                                    640 ;------------------------------------------------------------
                                    641 ;	keyboards/ajazz/ak820/ak820_flash.c:39: static uint16_t erase_page(void) __naked {
                                    642 ;	-----------------------------------------
                                    643 ;	 function erase_page
                                    644 ;	-----------------------------------------
      003500                        645 _erase_page:
                                    646 ;	naked function: no prologue.
                                    647 ;	keyboards/ajazz/ak820/ak820_flash.c:50: __endasm;
      003500 E5 86            [12]  648 	mov a, _ROM_CTRL
      003502 F5 F0            [12]  649 	mov b, a
      003504 30 E6 05         [24]  650 	jnb acc.6, 00002$
      003507 75 86 A6         [24]  651 	mov _ROM_CTRL, #0xa6
      00350A E5 86            [12]  652 	mov a, _ROM_CTRL
      00350C                        653 00002$:
      00350C F5 82            [12]  654 	mov dpl, a
      00350E 85 F0 83         [24]  655 	mov dph, b
      003511 22               [24]  656 	ret
                                    657 ;	keyboards/ajazz/ak820/ak820_flash.c:51: }
                                    658 ;	naked function: no epilogue.
                                    659 ;------------------------------------------------------------
                                    660 ;Allocation info for local variables in function 'ak820_flash_read'
                                    661 ;------------------------------------------------------------
                                    662 ;address       Allocated with name '_ak820_flash_read_address_10000_15'
                                    663 ;------------------------------------------------------------
                                    664 ;	keyboards/ajazz/ak820/ak820_flash.c:53: uint8_t ak820_flash_read(uint16_t address) {
                                    665 ;	-----------------------------------------
                                    666 ;	 function ak820_flash_read
                                    667 ;	-----------------------------------------
      003512                        668 _ak820_flash_read:
                           000007   669 	ar7 = 0x07
                           000006   670 	ar6 = 0x06
                           000005   671 	ar5 = 0x05
                           000004   672 	ar4 = 0x04
                           000003   673 	ar3 = 0x03
                           000002   674 	ar2 = 0x02
                           000001   675 	ar1 = 0x01
                           000000   676 	ar0 = 0x00
      003512 C0 07            [24]  677 	push	ar7
      003514 C0 06            [24]  678 	push	ar6
      003516 AF 83            [24]  679 	mov	r7,dph
      003518 E5 82            [12]  680 	mov	a,dpl
      00351A 90 04 A2         [24]  681 	mov	dptr,#_ak820_flash_read_address_10000_15
      00351D F0               [24]  682 	movx	@dptr,a
      00351E EF               [12]  683 	mov	a,r7
      00351F A3               [24]  684 	inc	dptr
      003520 F0               [24]  685 	movx	@dptr,a
                                    686 ;	keyboards/ajazz/ak820/ak820_flash.c:54: return *((const __code uint8_t *)address);
      003521 90 04 A2         [24]  687 	mov	dptr,#_ak820_flash_read_address_10000_15
      003524 E0               [24]  688 	movx	a,@dptr
      003525 FE               [12]  689 	mov	r6,a
      003526 A3               [24]  690 	inc	dptr
      003527 E0               [24]  691 	movx	a,@dptr
      003528 FF               [12]  692 	mov	r7,a
      003529 8E 82            [24]  693 	mov	dpl,r6
      00352B 8F 83            [24]  694 	mov	dph,r7
      00352D E4               [12]  695 	clr	a
      00352E 93               [24]  696 	movc	a,@a+dptr
      00352F F5 82            [12]  697 	mov	dpl,a
                                    698 ;	keyboards/ajazz/ak820/ak820_flash.c:55: }
      003531 D0 06            [24]  699 	pop	ar6
      003533 D0 07            [24]  700 	pop	ar7
      003535 22               [24]  701 	ret
                                    702 ;------------------------------------------------------------
                                    703 ;Allocation info for local variables in function 'flash_operation'
                                    704 ;------------------------------------------------------------
                                    705 ;value         Allocated with name '_flash_operation_PARM_2'
                                    706 ;operation     Allocated with name '_flash_operation_PARM_3'
                                    707 ;address       Allocated with name '_flash_operation_address_10000_17'
                                    708 ;previous_ie   Allocated with name '_flash_operation_previous_ie_10000_18'
                                    709 ;before        Allocated with name '_flash_operation_before_10000_18'
                                    710 ;status        Allocated with name '_flash_operation_status_10000_18'
                                    711 ;states        Allocated with name '_flash_operation_states_30000_21'
                                    712 ;states        Allocated with name '_flash_operation_states_30000_22'
                                    713 ;------------------------------------------------------------
                                    714 ;	keyboards/ajazz/ak820/ak820_flash.c:57: static bool flash_operation(uint16_t address, uint8_t value, uint8_t operation) {
                                    715 ;	-----------------------------------------
                                    716 ;	 function flash_operation
                                    717 ;	-----------------------------------------
      003536                        718 _flash_operation:
      003536 AF 83            [24]  719 	mov	r7,dph
      003538 E5 82            [12]  720 	mov	a,dpl
      00353A 90 04 A6         [24]  721 	mov	dptr,#_flash_operation_address_10000_17
      00353D F0               [24]  722 	movx	@dptr,a
      00353E EF               [12]  723 	mov	a,r7
      00353F A3               [24]  724 	inc	dptr
      003540 F0               [24]  725 	movx	@dptr,a
                                    726 ;	keyboards/ajazz/ak820/ak820_flash.c:59: if (address < AK820_NVM_BASE || address >= AK820_NVM_WRITE_END) return false;
      003541 90 04 A6         [24]  727 	mov	dptr,#_flash_operation_address_10000_17
      003544 E0               [24]  728 	movx	a,@dptr
      003545 FE               [12]  729 	mov	r6,a
      003546 A3               [24]  730 	inc	dptr
      003547 E0               [24]  731 	movx	a,@dptr
      003548 FF               [12]  732 	mov	r7,a
      003549 C3               [12]  733 	clr	c
      00354A 94 C7            [12]  734 	subb	a,#0xc7
      00354C 40 08            [24]  735 	jc	00101$
      00354E EE               [12]  736 	mov	a,r6
      00354F 94 80            [12]  737 	subb	a,#0x80
      003551 EF               [12]  738 	mov	a,r7
      003552 94 EF            [12]  739 	subb	a,#0xef
      003554 40 04            [24]  740 	jc	00102$
      003556                        741 00101$:
      003556 75 82 00         [24]  742 	mov	dpl, #0x00
      003559 22               [24]  743 	ret
      00355A                        744 00102$:
                                    745 ;	keyboards/ajazz/ak820/ak820_flash.c:60: ak820_flash_diagnostic[0] = 1;
      00355A 90 04 1B         [24]  746 	mov	dptr,#_ak820_flash_diagnostic
      00355D 74 01            [12]  747 	mov	a,#0x01
      00355F F0               [24]  748 	movx	@dptr,a
                                    749 ;	keyboards/ajazz/ak820/ak820_flash.c:61: ak820_flash_diagnostic[1] = operation ? operation : 0x9A;
      003560 90 04 A5         [24]  750 	mov	dptr,#_flash_operation_PARM_3
      003563 E0               [24]  751 	movx	a,@dptr
      003564 FF               [12]  752 	mov	r7,a
      003565 60 04            [24]  753 	jz	00109$
      003567 8F 06            [24]  754 	mov	ar6,r7
      003569 80 02            [24]  755 	sjmp	00110$
      00356B                        756 00109$:
      00356B 7E 9A            [12]  757 	mov	r6,#0x9a
      00356D                        758 00110$:
      00356D 90 04 1C         [24]  759 	mov	dptr,#(_ak820_flash_diagnostic + 0x0001)
      003570 EE               [12]  760 	mov	a,r6
      003571 F0               [24]  761 	movx	@dptr,a
                                    762 ;	keyboards/ajazz/ak820/ak820_flash.c:62: ak820_flash_diagnostic[4] = (uint8_t)address;
      003572 90 04 A6         [24]  763 	mov	dptr,#_flash_operation_address_10000_17
      003575 E0               [24]  764 	movx	a,@dptr
      003576 FD               [12]  765 	mov	r5,a
      003577 A3               [24]  766 	inc	dptr
      003578 E0               [24]  767 	movx	a,@dptr
      003579 FE               [12]  768 	mov	r6,a
      00357A 8D 04            [24]  769 	mov	ar4,r5
      00357C 90 04 1F         [24]  770 	mov	dptr,#(_ak820_flash_diagnostic + 0x0004)
      00357F EC               [12]  771 	mov	a,r4
      003580 F0               [24]  772 	movx	@dptr,a
                                    773 ;	keyboards/ajazz/ak820/ak820_flash.c:63: ak820_flash_diagnostic[5] = (uint8_t)(address >> 8);
      003581 8E 05            [24]  774 	mov	ar5,r6
      003583 90 04 20         [24]  775 	mov	dptr,#(_ak820_flash_diagnostic + 0x0005)
      003586 ED               [12]  776 	mov	a,r5
      003587 F0               [24]  777 	movx	@dptr,a
                                    778 ;	keyboards/ajazz/ak820/ak820_flash.c:64: previous_ie = IE;
      003588 90 04 A8         [24]  779 	mov	dptr,#_flash_operation_previous_ie_10000_18
      00358B E5 A8            [12]  780 	mov	a,_IE
      00358D F0               [24]  781 	movx	@dptr,a
                                    782 ;	keyboards/ajazz/ak820/ak820_flash.c:65: EA = 0;
                                    783 ;	assignBit
      00358E C2 AF            [12]  784 	clr	_EA
                                    785 ;	keyboards/ajazz/ak820/ak820_flash.c:66: SAFE_MOD = 0x55;
      003590 75 A1 55         [24]  786 	mov	_SAFE_MOD,#0x55
                                    787 ;	keyboards/ajazz/ak820/ak820_flash.c:67: SAFE_MOD = 0xAA;
      003593 75 A1 AA         [24]  788 	mov	_SAFE_MOD,#0xaa
                                    789 ;	keyboards/ajazz/ak820/ak820_flash.c:68: GLOBAL_CFG |= 0x08;  // CODE_WE
      003596 43 B1 08         [24]  790 	orl	_GLOBAL_CFG,#0x08
                                    791 ;	keyboards/ajazz/ak820/ak820_flash.c:69: ROM_ADDR_L = (uint8_t)address;
      003599 8C 84            [24]  792 	mov	_ROM_ADDR_L,r4
                                    793 ;	keyboards/ajazz/ak820/ak820_flash.c:70: ROM_ADDR_H = (uint8_t)(address >> 8);
      00359B 8D 85            [24]  794 	mov	_ROM_ADDR_H,r5
                                    795 ;	keyboards/ajazz/ak820/ak820_flash.c:73: ROM_BUF_MOD = operation ? 0x80 : AK820_FLASH_PAGE - 1;
      00359D EF               [12]  796 	mov	a,r7
      00359E 60 04            [24]  797 	jz	00111$
      0035A0 7E 80            [12]  798 	mov	r6,#0x80
      0035A2 80 02            [24]  799 	sjmp	00112$
      0035A4                        800 00111$:
      0035A4 7E 3F            [12]  801 	mov	r6,#0x3f
      0035A6                        802 00112$:
      0035A6 8E 8F            [24]  803 	mov	_ROM_DATA_HH,r6
                                    804 ;	keyboards/ajazz/ak820/ak820_flash.c:74: ROM_DAT_BUF = value;
      0035A8 90 04 A4         [24]  805 	mov	dptr,#_flash_operation_PARM_2
      0035AB E0               [24]  806 	movx	a,@dptr
      0035AC F5 8E            [12]  807 	mov	_ROM_DATA_HL,a
                                    808 ;	keyboards/ajazz/ak820/ak820_flash.c:75: if (operation) {
      0035AE EF               [12]  809 	mov	a,r7
      0035AF 60 13            [24]  810 	jz	00105$
                                    811 ;	keyboards/ajazz/ak820/ak820_flash.c:76: uint16_t states = erase_page();
      0035B1 12 35 00         [24]  812 	lcall	_erase_page
      0035B4 AE 82            [24]  813 	mov	r6, dpl
      0035B6 AF 83            [24]  814 	mov	r7, dph
                                    815 ;	keyboards/ajazz/ak820/ak820_flash.c:77: before = (uint8_t)(states >> 8);
      0035B8 90 04 A9         [24]  816 	mov	dptr,#_flash_operation_before_10000_18
      0035BB EF               [12]  817 	mov	a,r7
      0035BC F0               [24]  818 	movx	@dptr,a
                                    819 ;	keyboards/ajazz/ak820/ak820_flash.c:78: status = (uint8_t)states;
      0035BD 90 04 AA         [24]  820 	mov	dptr,#_flash_operation_status_10000_18
      0035C0 EE               [12]  821 	mov	a,r6
      0035C1 F0               [24]  822 	movx	@dptr,a
      0035C2 80 1D            [24]  823 	sjmp	00106$
      0035C4                        824 00105$:
                                    825 ;	keyboards/ajazz/ak820/ak820_flash.c:80: uint16_t states = program_block(block_data);
      0035C4 90 04 A0         [24]  826 	mov	dptr,#_block_data
      0035C7 E0               [24]  827 	movx	a,@dptr
      0035C8 FE               [12]  828 	mov	r6,a
      0035C9 A3               [24]  829 	inc	dptr
      0035CA E0               [24]  830 	movx	a,@dptr
      0035CB FF               [12]  831 	mov	r7,a
      0035CC 8E 82            [24]  832 	mov	dpl, r6
      0035CE 8F 83            [24]  833 	mov	dph, r7
      0035D0 12 34 EE         [24]  834 	lcall	_program_block
      0035D3 AE 82            [24]  835 	mov	r6, dpl
      0035D5 AF 83            [24]  836 	mov	r7, dph
                                    837 ;	keyboards/ajazz/ak820/ak820_flash.c:81: before = (uint8_t)(states >> 8);
      0035D7 90 04 A9         [24]  838 	mov	dptr,#_flash_operation_before_10000_18
      0035DA EF               [12]  839 	mov	a,r7
      0035DB F0               [24]  840 	movx	@dptr,a
                                    841 ;	keyboards/ajazz/ak820/ak820_flash.c:82: status = (uint8_t)states;
      0035DC 90 04 AA         [24]  842 	mov	dptr,#_flash_operation_status_10000_18
      0035DF EE               [12]  843 	mov	a,r6
      0035E0 F0               [24]  844 	movx	@dptr,a
      0035E1                        845 00106$:
                                    846 ;	keyboards/ajazz/ak820/ak820_flash.c:84: ak820_flash_diagnostic[2] = before;
      0035E1 90 04 A9         [24]  847 	mov	dptr,#_flash_operation_before_10000_18
      0035E4 E0               [24]  848 	movx	a,@dptr
      0035E5 FF               [12]  849 	mov	r7,a
      0035E6 90 04 1D         [24]  850 	mov	dptr,#(_ak820_flash_diagnostic + 0x0002)
      0035E9 F0               [24]  851 	movx	@dptr,a
                                    852 ;	keyboards/ajazz/ak820/ak820_flash.c:85: ak820_flash_diagnostic[3] = status;
      0035EA 90 04 AA         [24]  853 	mov	dptr,#_flash_operation_status_10000_18
      0035ED E0               [24]  854 	movx	a,@dptr
      0035EE FE               [12]  855 	mov	r6,a
      0035EF 90 04 1E         [24]  856 	mov	dptr,#(_ak820_flash_diagnostic + 0x0003)
      0035F2 F0               [24]  857 	movx	@dptr,a
                                    858 ;	keyboards/ajazz/ak820/ak820_flash.c:86: SAFE_MOD = 0x55;
      0035F3 75 A1 55         [24]  859 	mov	_SAFE_MOD,#0x55
                                    860 ;	keyboards/ajazz/ak820/ak820_flash.c:87: SAFE_MOD = 0xAA;
      0035F6 75 A1 AA         [24]  861 	mov	_SAFE_MOD,#0xaa
                                    862 ;	keyboards/ajazz/ak820/ak820_flash.c:88: GLOBAL_CFG &= (uint8_t)~0x08;
      0035F9 53 B1 F7         [24]  863 	anl	_GLOBAL_CFG,#0xf7
                                    864 ;	keyboards/ajazz/ak820/ak820_flash.c:89: SAFE_MOD = 0;
      0035FC 75 A1 00         [24]  865 	mov	_SAFE_MOD,#0x00
                                    866 ;	keyboards/ajazz/ak820/ak820_flash.c:90: IE = previous_ie;
      0035FF 90 04 A8         [24]  867 	mov	dptr,#_flash_operation_previous_ie_10000_18
      003602 E0               [24]  868 	movx	a,@dptr
      003603 F5 A8            [12]  869 	mov	_IE,a
                                    870 ;	keyboards/ajazz/ak820/ak820_flash.c:91: return (before & 0x40) && !(status & 0x02);
      003605 EF               [12]  871 	mov	a,r7
      003606 23               [12]  872 	rl	a
      003607 23               [12]  873 	rl	a
      003608 54 01            [12]  874 	anl	a,#0x01
      00360A 60 06            [24]  875 	jz	00113$
      00360C EE               [12]  876 	mov	a,r6
      00360D 03               [12]  877 	rr	a
      00360E 54 01            [12]  878 	anl	a,#0x01
      003610 60 04            [24]  879 	jz	00114$
      003612                        880 00113$:
                                    881 ;	assignBit
      003612 C2 00            [12]  882 	clr	_flash_operation_sloc0_1_0
      003614 80 02            [24]  883 	sjmp	00115$
      003616                        884 00114$:
                                    885 ;	assignBit
      003616 D2 00            [12]  886 	setb	_flash_operation_sloc0_1_0
      003618                        887 00115$:
      003618 A2 00            [12]  888 	mov	c,_flash_operation_sloc0_1_0
      00361A E4               [12]  889 	clr	a
      00361B 33               [12]  890 	rlc	a
      00361C F5 82            [12]  891 	mov	dpl, a
                                    892 ;	keyboards/ajazz/ak820/ak820_flash.c:92: }
      00361E 22               [24]  893 	ret
                                    894 ;------------------------------------------------------------
                                    895 ;Allocation info for local variables in function 'ak820_flash_erase'
                                    896 ;------------------------------------------------------------
                                    897 ;address       Allocated with name '_ak820_flash_erase_address_10000_23'
                                    898 ;i             Allocated with name '_ak820_flash_erase_i_10000_24'
                                    899 ;------------------------------------------------------------
                                    900 ;	keyboards/ajazz/ak820/ak820_flash.c:94: bool ak820_flash_erase(uint16_t address) {
                                    901 ;	-----------------------------------------
                                    902 ;	 function ak820_flash_erase
                                    903 ;	-----------------------------------------
      00361F                        904 _ak820_flash_erase:
      00361F AF 83            [24]  905 	mov	r7,dph
      003621 E5 82            [12]  906 	mov	a,dpl
      003623 90 04 AB         [24]  907 	mov	dptr,#_ak820_flash_erase_address_10000_23
      003626 F0               [24]  908 	movx	@dptr,a
      003627 EF               [12]  909 	mov	a,r7
      003628 A3               [24]  910 	inc	dptr
      003629 F0               [24]  911 	movx	@dptr,a
                                    912 ;	keyboards/ajazz/ak820/ak820_flash.c:96: if (address & (AK820_FLASH_PAGE - 1)) return false;
      00362A 90 04 AB         [24]  913 	mov	dptr,#_ak820_flash_erase_address_10000_23
      00362D E0               [24]  914 	movx	a,@dptr
      00362E FE               [12]  915 	mov	r6,a
      00362F A3               [24]  916 	inc	dptr
      003630 E0               [24]  917 	movx	a,@dptr
      003631 FF               [12]  918 	mov	r7,a
      003632 EE               [12]  919 	mov	a,r6
      003633 54 3F            [12]  920 	anl	a,#0x3f
      003635 60 04            [24]  921 	jz	00102$
      003637 75 82 00         [24]  922 	mov	dpl, #0x00
      00363A 22               [24]  923 	ret
      00363B                        924 00102$:
                                    925 ;	keyboards/ajazz/ak820/ak820_flash.c:97: if (!flash_operation(address, 0, 0xA6)) return false;
      00363B 90 04 A4         [24]  926 	mov	dptr,#_flash_operation_PARM_2
      00363E E4               [12]  927 	clr	a
      00363F F0               [24]  928 	movx	@dptr,a
      003640 90 04 A5         [24]  929 	mov	dptr,#_flash_operation_PARM_3
      003643 74 A6            [12]  930 	mov	a,#0xa6
      003645 F0               [24]  931 	movx	@dptr,a
      003646 8E 82            [24]  932 	mov	dpl, r6
      003648 8F 83            [24]  933 	mov	dph, r7
      00364A 12 35 36         [24]  934 	lcall	_flash_operation
      00364D E5 82            [12]  935 	mov	a, dpl
      00364F 70 03            [24]  936 	jnz	00120$
      003651 F5 82            [12]  937 	mov	dpl,a
                                    938 ;	keyboards/ajazz/ak820/ak820_flash.c:100: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003653 22               [24]  939 	ret
      003654                        940 00120$:
      003654 7F 00            [12]  941 	mov	r7,#0x00
      003656                        942 00108$:
                                    943 ;	keyboards/ajazz/ak820/ak820_flash.c:101: if (ak820_flash_read(address + i) != 0) return false;
      003656 8F 05            [24]  944 	mov	ar5,r7
      003658 7E 00            [12]  945 	mov	r6,#0x00
      00365A 90 04 AB         [24]  946 	mov	dptr,#_ak820_flash_erase_address_10000_23
      00365D E0               [24]  947 	movx	a,@dptr
      00365E FB               [12]  948 	mov	r3,a
      00365F A3               [24]  949 	inc	dptr
      003660 E0               [24]  950 	movx	a,@dptr
      003661 FC               [12]  951 	mov	r4,a
      003662 ED               [12]  952 	mov	a,r5
      003663 2B               [12]  953 	add	a, r3
      003664 FB               [12]  954 	mov	r3,a
      003665 EE               [12]  955 	mov	a,r6
      003666 3C               [12]  956 	addc	a, r4
      003667 FC               [12]  957 	mov	r4,a
      003668 8B 82            [24]  958 	mov	dpl, r3
      00366A 8C 83            [24]  959 	mov	dph, r4
      00366C 12 35 12         [24]  960 	lcall	_ak820_flash_read
      00366F E5 82            [12]  961 	mov	a, dpl
      003671 60 04            [24]  962 	jz	00109$
      003673 75 82 00         [24]  963 	mov	dpl, #0x00
      003676 22               [24]  964 	ret
      003677                        965 00109$:
                                    966 ;	keyboards/ajazz/ak820/ak820_flash.c:100: for (i = 0; i != AK820_FLASH_PAGE; ++i) {
      003677 0F               [12]  967 	inc	r7
      003678 BF 40 DB         [24]  968 	cjne	r7,#0x40,00108$
                                    969 ;	keyboards/ajazz/ak820/ak820_flash.c:103: return true;
      00367B 75 82 01         [24]  970 	mov	dpl, #0x01
                                    971 ;	keyboards/ajazz/ak820/ak820_flash.c:104: }
      00367E 22               [24]  972 	ret
                                    973 ;------------------------------------------------------------
                                    974 ;Allocation info for local variables in function 'ak820_flash_program'
                                    975 ;------------------------------------------------------------
                                    976 ;sloc0         Allocated with name '_ak820_flash_program_sloc0_1_0'
                                    977 ;value         Allocated with name '_ak820_flash_program_PARM_2'
                                    978 ;address       Allocated with name '_ak820_flash_program_address_10000_30'
                                    979 ;i             Allocated with name '_ak820_flash_program_i_10000_31'
                                    980 ;offset        Allocated with name '_ak820_flash_program_offset_10000_31'
                                    981 ;page          Allocated with name '_ak820_flash_program_page_10000_31'
                                    982 ;------------------------------------------------------------
                                    983 ;	keyboards/ajazz/ak820/ak820_flash.c:106: bool ak820_flash_program(uint16_t address, uint8_t value) {
                                    984 ;	-----------------------------------------
                                    985 ;	 function ak820_flash_program
                                    986 ;	-----------------------------------------
      00367F                        987 _ak820_flash_program:
      00367F AF 83            [24]  988 	mov	r7,dph
      003681 E5 82            [12]  989 	mov	a,dpl
      003683 90 04 AE         [24]  990 	mov	dptr,#_ak820_flash_program_address_10000_30
      003686 F0               [24]  991 	movx	@dptr,a
      003687 EF               [12]  992 	mov	a,r7
      003688 A3               [24]  993 	inc	dptr
      003689 F0               [24]  994 	movx	@dptr,a
                                    995 ;	keyboards/ajazz/ak820/ak820_flash.c:110: if (address < AK820_NVM_BASE || address >= AK820_NVM_WRITE_END) return false;
      00368A 90 04 AE         [24]  996 	mov	dptr,#_ak820_flash_program_address_10000_30
      00368D E0               [24]  997 	movx	a,@dptr
      00368E FE               [12]  998 	mov	r6,a
      00368F A3               [24]  999 	inc	dptr
      003690 E0               [24] 1000 	movx	a,@dptr
      003691 FF               [12] 1001 	mov	r7,a
      003692 8E 04            [24] 1002 	mov	ar4,r6
      003694 8F 05            [24] 1003 	mov	ar5,r7
      003696 74 39            [12] 1004 	mov	a,#0x100 - 0xc7
      003698 2D               [12] 1005 	add	a,r5
      003699 50 09            [24] 1006 	jnc	00101$
      00369B C3               [12] 1007 	clr	c
      00369C EC               [12] 1008 	mov	a,r4
      00369D 94 80            [12] 1009 	subb	a,#0x80
      00369F ED               [12] 1010 	mov	a,r5
      0036A0 94 EF            [12] 1011 	subb	a,#0xef
      0036A2 40 04            [24] 1012 	jc	00102$
      0036A4                       1013 00101$:
      0036A4 75 82 00         [24] 1014 	mov	dpl, #0x00
      0036A7 22               [24] 1015 	ret
      0036A8                       1016 00102$:
                                   1017 ;	keyboards/ajazz/ak820/ak820_flash.c:111: offset = address & (AK820_FLASH_PAGE - 1);
      0036A8 74 3F            [12] 1018 	mov	a,#0x3f
      0036AA 5E               [12] 1019 	anl	a,r6
      0036AB FF               [12] 1020 	mov	r7,a
                                   1021 ;	keyboards/ajazz/ak820/ak820_flash.c:112: page = address & ~(AK820_FLASH_PAGE - 1);
      0036AC 53 04 C0         [24] 1022 	anl	ar4,#0xc0
                                   1023 ;	keyboards/ajazz/ak820/ak820_flash.c:113: block_data = (uint8_t __xdata *)(((uint16_t)block_storage + AK820_FLASH_PAGE - 1) & ~(AK820_FLASH_PAGE - 1));
      0036AF 7B 21            [12] 1024 	mov	r3,#_block_storage
      0036B1 7E 04            [12] 1025 	mov	r6,#(_block_storage >> 8)
      0036B3 74 3F            [12] 1026 	mov	a,#0x3f
      0036B5 2B               [12] 1027 	add	a, r3
      0036B6 FB               [12] 1028 	mov	r3,a
      0036B7 E4               [12] 1029 	clr	a
      0036B8 3E               [12] 1030 	addc	a, r6
      0036B9 FE               [12] 1031 	mov	r6,a
      0036BA 53 03 C0         [24] 1032 	anl	ar3,#0xc0
      0036BD 90 04 A0         [24] 1033 	mov	dptr,#_block_data
      0036C0 EB               [12] 1034 	mov	a,r3
      0036C1 F0               [24] 1035 	movx	@dptr,a
      0036C2 EE               [12] 1036 	mov	a,r6
      0036C3 A3               [24] 1037 	inc	dptr
      0036C4 F0               [24] 1038 	movx	@dptr,a
                                   1039 ;	keyboards/ajazz/ak820/ak820_flash.c:119: for (i = 0; i != AK820_FLASH_PAGE; ++i) block_data[i] = ak820_flash_read(page + i);
      0036C5 7E 00            [12] 1040 	mov	r6,#0x00
      0036C7                       1041 00105$:
      0036C7 C0 07            [24] 1042 	push	ar7
      0036C9 90 04 A0         [24] 1043 	mov	dptr,#_block_data
      0036CC E0               [24] 1044 	movx	a,@dptr
      0036CD FA               [12] 1045 	mov	r2,a
      0036CE A3               [24] 1046 	inc	dptr
      0036CF E0               [24] 1047 	movx	a,@dptr
      0036D0 FB               [12] 1048 	mov	r3,a
      0036D1 EE               [12] 1049 	mov	a,r6
      0036D2 2A               [12] 1050 	add	a, r2
      0036D3 FA               [12] 1051 	mov	r2,a
      0036D4 E4               [12] 1052 	clr	a
      0036D5 3B               [12] 1053 	addc	a, r3
      0036D6 FB               [12] 1054 	mov	r3,a
      0036D7 8E 08            [24] 1055 	mov	_ak820_flash_program_sloc0_1_0,r6
      0036D9 75 09 00         [24] 1056 	mov	(_ak820_flash_program_sloc0_1_0 + 1),#0x00
      0036DC 8C 01            [24] 1057 	mov	ar1,r4
      0036DE 8D 07            [24] 1058 	mov	ar7,r5
      0036E0 E5 08            [12] 1059 	mov	a,_ak820_flash_program_sloc0_1_0
      0036E2 29               [12] 1060 	add	a, r1
      0036E3 F9               [12] 1061 	mov	r1,a
      0036E4 E5 09            [12] 1062 	mov	a,(_ak820_flash_program_sloc0_1_0 + 1)
      0036E6 3F               [12] 1063 	addc	a, r7
      0036E7 FF               [12] 1064 	mov	r7,a
      0036E8 89 82            [24] 1065 	mov	dpl, r1
      0036EA 8F 83            [24] 1066 	mov	dph, r7
      0036EC 12 35 12         [24] 1067 	lcall	_ak820_flash_read
      0036EF AF 82            [24] 1068 	mov	r7, dpl
      0036F1 8A 82            [24] 1069 	mov	dpl,r2
      0036F3 8B 83            [24] 1070 	mov	dph,r3
      0036F5 EF               [12] 1071 	mov	a,r7
      0036F6 F0               [24] 1072 	movx	@dptr,a
      0036F7 0E               [12] 1073 	inc	r6
      0036F8 BE 40 02         [24] 1074 	cjne	r6,#0x40,00133$
      0036FB 80 04            [24] 1075 	sjmp	00134$
      0036FD                       1076 00133$:
      0036FD D0 07            [24] 1077 	pop	ar7
      0036FF 80 C6            [24] 1078 	sjmp	00105$
      003701                       1079 00134$:
      003701 D0 07            [24] 1080 	pop	ar7
                                   1081 ;	keyboards/ajazz/ak820/ak820_flash.c:120: block_data[offset] |= value;
      003703 90 04 A0         [24] 1082 	mov	dptr,#_block_data
      003706 E0               [24] 1083 	movx	a,@dptr
      003707 FB               [12] 1084 	mov	r3,a
      003708 A3               [24] 1085 	inc	dptr
      003709 E0               [24] 1086 	movx	a,@dptr
      00370A FE               [12] 1087 	mov	r6,a
      00370B EF               [12] 1088 	mov	a,r7
      00370C 2B               [12] 1089 	add	a, r3
      00370D FF               [12] 1090 	mov	r7,a
      00370E E4               [12] 1091 	clr	a
      00370F 3E               [12] 1092 	addc	a, r6
      003710 FA               [12] 1093 	mov	r2,a
      003711 8F 82            [24] 1094 	mov	dpl,r7
      003713 8A 83            [24] 1095 	mov	dph,r2
      003715 E0               [24] 1096 	movx	a,@dptr
      003716 FE               [12] 1097 	mov	r6,a
      003717 90 04 AD         [24] 1098 	mov	dptr,#_ak820_flash_program_PARM_2
      00371A E0               [24] 1099 	movx	a,@dptr
      00371B 42 06            [12] 1100 	orl	ar6,a
      00371D 8F 82            [24] 1101 	mov	dpl,r7
      00371F 8A 83            [24] 1102 	mov	dph,r2
      003721 EE               [12] 1103 	mov	a,r6
      003722 F0               [24] 1104 	movx	@dptr,a
                                   1105 ;	keyboards/ajazz/ak820/ak820_flash.c:121: return flash_operation(page, 0, 0);
      003723 90 04 A4         [24] 1106 	mov	dptr,#_flash_operation_PARM_2
      003726 E4               [12] 1107 	clr	a
      003727 F0               [24] 1108 	movx	@dptr,a
      003728 90 04 A5         [24] 1109 	mov	dptr,#_flash_operation_PARM_3
      00372B F0               [24] 1110 	movx	@dptr,a
      00372C 8C 82            [24] 1111 	mov	dpl, r4
      00372E 8D 83            [24] 1112 	mov	dph, r5
                                   1113 ;	keyboards/ajazz/ak820/ak820_flash.c:122: }
      003730 02 35 36         [24] 1114 	ljmp	_flash_operation
                                   1115 ;------------------------------------------------------------
                                   1116 ;Allocation info for local variables in function 'ak820_flash_program_page'
                                   1117 ;------------------------------------------------------------
                                   1118 ;data          Allocated with name '_ak820_flash_program_page_PARM_2'
                                   1119 ;address       Allocated with name '_ak820_flash_program_page_address_10000_34'
                                   1120 ;i             Allocated with name '_ak820_flash_program_page_i_10000_35'
                                   1121 ;------------------------------------------------------------
                                   1122 ;	keyboards/ajazz/ak820/ak820_flash.c:124: bool ak820_flash_program_page(uint16_t address, const uint8_t __xdata *data) {
                                   1123 ;	-----------------------------------------
                                   1124 ;	 function ak820_flash_program_page
                                   1125 ;	-----------------------------------------
      003733                       1126 _ak820_flash_program_page:
      003733 AF 83            [24] 1127 	mov	r7,dph
      003735 E5 82            [12] 1128 	mov	a,dpl
      003737 90 04 B2         [24] 1129 	mov	dptr,#_ak820_flash_program_page_address_10000_34
      00373A F0               [24] 1130 	movx	@dptr,a
      00373B EF               [12] 1131 	mov	a,r7
      00373C A3               [24] 1132 	inc	dptr
      00373D F0               [24] 1133 	movx	@dptr,a
                                   1134 ;	keyboards/ajazz/ak820/ak820_flash.c:126: if (address & (AK820_FLASH_PAGE - 1)) return false;
      00373E 90 04 B2         [24] 1135 	mov	dptr,#_ak820_flash_program_page_address_10000_34
      003741 E0               [24] 1136 	movx	a,@dptr
      003742 FE               [12] 1137 	mov	r6,a
      003743 A3               [24] 1138 	inc	dptr
      003744 E0               [24] 1139 	movx	a,@dptr
      003745 EE               [12] 1140 	mov	a,r6
      003746 54 3F            [12] 1141 	anl	a,#0x3f
      003748 60 04            [24] 1142 	jz	00102$
      00374A 75 82 00         [24] 1143 	mov	dpl, #0x00
      00374D 22               [24] 1144 	ret
      00374E                       1145 00102$:
                                   1146 ;	keyboards/ajazz/ak820/ak820_flash.c:127: block_data = (uint8_t __xdata *)(((uint16_t)block_storage + AK820_FLASH_PAGE - 1) & ~(AK820_FLASH_PAGE - 1));
      00374E 7E 21            [12] 1147 	mov	r6,#_block_storage
      003750 7F 04            [12] 1148 	mov	r7,#(_block_storage >> 8)
      003752 74 3F            [12] 1149 	mov	a,#0x3f
      003754 2E               [12] 1150 	add	a, r6
      003755 FE               [12] 1151 	mov	r6,a
      003756 E4               [12] 1152 	clr	a
      003757 3F               [12] 1153 	addc	a, r7
      003758 FF               [12] 1154 	mov	r7,a
      003759 53 06 C0         [24] 1155 	anl	ar6,#0xc0
      00375C 90 04 A0         [24] 1156 	mov	dptr,#_block_data
      00375F EE               [12] 1157 	mov	a,r6
      003760 F0               [24] 1158 	movx	@dptr,a
      003761 EF               [12] 1159 	mov	a,r7
      003762 A3               [24] 1160 	inc	dptr
      003763 F0               [24] 1161 	movx	@dptr,a
                                   1162 ;	keyboards/ajazz/ak820/ak820_flash.c:128: for (i = 0; i != AK820_FLASH_PAGE; ++i) block_data[i] = data[i];
      003764 90 04 B0         [24] 1163 	mov	dptr,#_ak820_flash_program_page_PARM_2
      003767 E0               [24] 1164 	movx	a,@dptr
      003768 FE               [12] 1165 	mov	r6,a
      003769 A3               [24] 1166 	inc	dptr
      00376A E0               [24] 1167 	movx	a,@dptr
      00376B FF               [12] 1168 	mov	r7,a
      00376C 7D 00            [12] 1169 	mov	r5,#0x00
      00376E                       1170 00104$:
      00376E 90 04 A0         [24] 1171 	mov	dptr,#_block_data
      003771 E0               [24] 1172 	movx	a,@dptr
      003772 FB               [12] 1173 	mov	r3,a
      003773 A3               [24] 1174 	inc	dptr
      003774 E0               [24] 1175 	movx	a,@dptr
      003775 FC               [12] 1176 	mov	r4,a
      003776 ED               [12] 1177 	mov	a,r5
      003777 2B               [12] 1178 	add	a, r3
      003778 FB               [12] 1179 	mov	r3,a
      003779 E4               [12] 1180 	clr	a
      00377A 3C               [12] 1181 	addc	a, r4
      00377B FC               [12] 1182 	mov	r4,a
      00377C ED               [12] 1183 	mov	a,r5
      00377D 2E               [12] 1184 	add	a, r6
      00377E F5 82            [12] 1185 	mov	dpl,a
      003780 E4               [12] 1186 	clr	a
      003781 3F               [12] 1187 	addc	a, r7
      003782 F5 83            [12] 1188 	mov	dph,a
      003784 E0               [24] 1189 	movx	a,@dptr
      003785 8B 82            [24] 1190 	mov	dpl,r3
      003787 8C 83            [24] 1191 	mov	dph,r4
      003789 F0               [24] 1192 	movx	@dptr,a
      00378A 0D               [12] 1193 	inc	r5
      00378B BD 40 E0         [24] 1194 	cjne	r5,#0x40,00104$
                                   1195 ;	keyboards/ajazz/ak820/ak820_flash.c:129: return flash_operation(address, 0, 0);
      00378E 90 04 B2         [24] 1196 	mov	dptr,#_ak820_flash_program_page_address_10000_34
      003791 E0               [24] 1197 	movx	a,@dptr
      003792 FE               [12] 1198 	mov	r6,a
      003793 A3               [24] 1199 	inc	dptr
      003794 E0               [24] 1200 	movx	a,@dptr
      003795 FF               [12] 1201 	mov	r7,a
      003796 90 04 A4         [24] 1202 	mov	dptr,#_flash_operation_PARM_2
      003799 E4               [12] 1203 	clr	a
      00379A F0               [24] 1204 	movx	@dptr,a
      00379B 90 04 A5         [24] 1205 	mov	dptr,#_flash_operation_PARM_3
      00379E F0               [24] 1206 	movx	@dptr,a
      00379F 8E 82            [24] 1207 	mov	dpl, r6
      0037A1 8F 83            [24] 1208 	mov	dph, r7
                                   1209 ;	keyboards/ajazz/ak820/ak820_flash.c:130: }
      0037A3 02 35 36         [24] 1210 	ljmp	_flash_operation
                                   1211 	.area CSEG    (CODE)
                                   1212 	.area CONST   (CODE)
                                   1213 	.area XINIT   (CODE)
                                   1214 	.area CABS    (ABS,CODE)
