                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module usb_device_state
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
                                    254 	.globl _usb_device_state
                                    255 	.globl _usb_device_state_set_resume_PARM_2
                                    256 	.globl _usb_device_state_set_suspend_PARM_2
                                    257 	.globl _usb_device_state_set_configuration_PARM_2
                                    258 	.globl _notify_usb_device_state_change_kb
                                    259 	.globl _notify_usb_device_state_change_user
                                    260 	.globl _usb_device_state_set_configuration
                                    261 	.globl _usb_device_state_set_suspend
                                    262 	.globl _usb_device_state_set_resume
                                    263 	.globl _usb_device_state_init
                                    264 ;--------------------------------------------------------
                                    265 ; special function registers
                                    266 ;--------------------------------------------------------
                                    267 	.area RSEG    (ABS,DATA)
      000000                        268 	.org 0x0000
                           0000D0   269 _PSW	=	0x00d0
                           0000E0   270 _ACC	=	0x00e0
                           0000F0   271 _B	=	0x00f0
                           0000FD   272 _A_INV	=	0x00fd
                           000081   273 _SP	=	0x0081
                           000082   274 _DPL	=	0x0082
                           000083   275 _DPH	=	0x0083
                           0000A1   276 _SAFE_MOD	=	0x00a1
                           0000B1   277 _GLOBAL_CFG	=	0x00b1
                           000087   278 _PCON	=	0x0087
                           0000BA   279 _POWER_CFG	=	0x00ba
                           0000B9   280 _CLOCK_CFG	=	0x00b9
                           0000A9   281 _WAKE_CTRL	=	0x00a9
                           0000FE   282 _RESET_KEEP	=	0x00fe
                           0000FF   283 _WDOG_COUNT	=	0x00ff
                           0000A8   284 _IE	=	0x00a8
                           0000B8   285 _IP	=	0x00b8
                           0000E8   286 _IE_EX	=	0x00e8
                           0000E9   287 _IP_EX	=	0x00e9
                           0000B2   288 _GPIO_IE	=	0x00b2
                           008584   289 _ROM_ADDR	=	0x8584
                           000084   290 _ROM_ADDR_L	=	0x0084
                           000085   291 _ROM_ADDR_H	=	0x0085
                           008F8E   292 _ROM_DATA_HI	=	0x8f8e
                           00008E   293 _ROM_DATA_HL	=	0x008e
                           00008F   294 _ROM_DATA_HH	=	0x008f
                           000086   295 _ROM_CTRL	=	0x0086
                           000080   296 _P0	=	0x0080
                           0000C4   297 _P0_MOD_OC	=	0x00c4
                           0000C5   298 _P0_DIR_PU	=	0x00c5
                           000090   299 _P1	=	0x0090
                           000092   300 _P1_MOD_OC	=	0x0092
                           000093   301 _P1_DIR_PU	=	0x0093
                           0000A0   302 _P2	=	0x00a0
                           000094   303 _P2_MOD_OC	=	0x0094
                           000095   304 _P2_DIR_PU	=	0x0095
                           0000B0   305 _P3	=	0x00b0
                           000096   306 _P3_MOD_OC	=	0x0096
                           000097   307 _P3_DIR_PU	=	0x0097
                           0000C0   308 _P4	=	0x00c0
                           0000C2   309 _P4_MOD_OC	=	0x00c2
                           0000C3   310 _P4_DIR_PU	=	0x00c3
                           0000C1   311 _P4_LED_KEY	=	0x00c1
                           0000AA   312 _P5_IN	=	0x00aa
                           0000AB   313 _P5_OUT_PU	=	0x00ab
                           0000AC   314 _P5_DIR	=	0x00ac
                           0000AD   315 _P6_IN	=	0x00ad
                           0000AE   316 _P6_OUT_PU	=	0x00ae
                           0000AF   317 _P6_DIR	=	0x00af
                           0000F1   318 _P7	=	0x00f1
                           0000A2   319 _XBUS_AUX	=	0x00a2
                           000088   320 _TCON	=	0x0088
                           000089   321 _TMOD	=	0x0089
                           00008A   322 _TL0	=	0x008a
                           00008B   323 _TL1	=	0x008b
                           00008C   324 _TH0	=	0x008c
                           00008D   325 _TH1	=	0x008d
                           000098   326 _SCON	=	0x0098
                           000099   327 _SBUF	=	0x0099
                           0000C8   328 _T2CON	=	0x00c8
                           0000C9   329 _T2MOD	=	0x00c9
                           00CBCA   330 _RCAP2	=	0xcbca
                           0000CA   331 _RCAP2L	=	0x00ca
                           0000CB   332 _RCAP2H	=	0x00cb
                           00CDCC   333 _T2COUNT	=	0xcdcc
                           0000CC   334 _TL2	=	0x00cc
                           0000CD   335 _TH2	=	0x00cd
                           00CFCE   336 _T2CAP1	=	0xcfce
                           0000CE   337 _T2CAP1L	=	0x00ce
                           0000CF   338 _T2CAP1H	=	0x00cf
                           0000F8   339 _SPI0_STAT	=	0x00f8
                           0000F9   340 _SPI0_DATA	=	0x00f9
                           0000FA   341 _SPI0_CTRL	=	0x00fa
                           0000FB   342 _SPI0_CK_SE	=	0x00fb
                           0000FC   343 _SPI0_SETUP	=	0x00fc
                           0000BC   344 _SCON1	=	0x00bc
                           0000BD   345 _SBUF1	=	0x00bd
                           0000BE   346 _SBAUD1	=	0x00be
                           0000BF   347 _SIF1	=	0x00bf
                           0000B4   348 _SPI1_STAT	=	0x00b4
                           0000B5   349 _SPI1_DATA	=	0x00b5
                           0000B6   350 _SPI1_CTRL	=	0x00b6
                           0000B7   351 _SPI1_CK_SE	=	0x00b7
                           0000F3   352 _ADC_CTRL	=	0x00f3
                           00F5F4   353 _ADC_DAT	=	0xf5f4
                           0000F4   354 _ADC_DAT_L	=	0x00f4
                           0000F5   355 _ADC_DAT_H	=	0x00f5
                           0000F6   356 _ADC_CHAN	=	0x00f6
                           0000A6   357 _LED_COMMON	=	0x00a6
                           0000A7   358 _LED_PWM_OE	=	0x00a7
                           00C7C6   359 _LED_DMA	=	0xc7c6
                           0000C6   360 _LED_DMA_L	=	0x00c6
                           0000C7   361 _LED_DMA_H	=	0x00c7
                           0000F7   362 _LED_STATUS	=	0x00f7
                           0000B3   363 _I2CX_INT	=	0x00b3
                           0000BB   364 _I2CS_INT_ST	=	0x00bb
                                    365 ;--------------------------------------------------------
                                    366 ; special function bits
                                    367 ;--------------------------------------------------------
                                    368 	.area RSEG    (ABS,DATA)
      000000                        369 	.org 0x0000
                           0000D7   370 _CY	=	0x00d7
                           0000D6   371 _AC	=	0x00d6
                           0000D5   372 _F0	=	0x00d5
                           0000D4   373 _RS1	=	0x00d4
                           0000D3   374 _RS0	=	0x00d3
                           0000D2   375 _OV	=	0x00d2
                           0000D1   376 _F1	=	0x00d1
                           0000D0   377 _P	=	0x00d0
                           0000AF   378 _EA	=	0x00af
                           0000AE   379 _E_DIS	=	0x00ae
                           0000AD   380 _ET2	=	0x00ad
                           0000AC   381 _ES	=	0x00ac
                           0000AB   382 _ET1	=	0x00ab
                           0000AA   383 _EX1	=	0x00aa
                           0000A9   384 _ET0	=	0x00a9
                           0000A8   385 _EX0	=	0x00a8
                           0000BF   386 _PH_FLAG	=	0x00bf
                           0000BE   387 _PL_FLAG	=	0x00be
                           0000BD   388 _PT2	=	0x00bd
                           0000BC   389 _PS	=	0x00bc
                           0000BB   390 _PT1	=	0x00bb
                           0000BA   391 _PX1	=	0x00ba
                           0000B9   392 _PT0	=	0x00b9
                           0000B8   393 _PX0	=	0x00b8
                           0000EF   394 _IE_WDOG	=	0x00ef
                           0000EE   395 _IE_GPIO	=	0x00ee
                           0000ED   396 _IE_PWM_I2C	=	0x00ed
                           0000EC   397 _IE_UART1	=	0x00ec
                           0000EB   398 _IE_ADC	=	0x00eb
                           0000E9   399 _IE_USB	=	0x00e9
                           0000E8   400 _IE_SPI0	=	0x00e8
                           000087   401 _P0_7	=	0x0087
                           000086   402 _P0_6	=	0x0086
                           000085   403 _P0_5	=	0x0085
                           000084   404 _P0_4	=	0x0084
                           000083   405 _P0_3	=	0x0083
                           000082   406 _P0_2	=	0x0082
                           000081   407 _P0_1	=	0x0081
                           000080   408 _P0_0	=	0x0080
                           000081   409 _SDA0	=	0x0081
                           000080   410 _SCL0	=	0x0080
                           000083   411 _TXD_	=	0x0083
                           000082   412 _RXD_	=	0x0082
                           000085   413 _AIN13	=	0x0085
                           000084   414 _AIN12	=	0x0084
                           000083   415 _AIN11	=	0x0083
                           000082   416 _AIN10	=	0x0082
                           000081   417 _AIN9	=	0x0081
                           000080   418 _AIN8	=	0x0080
                           000097   419 _P1_7	=	0x0097
                           000096   420 _P1_6	=	0x0096
                           000095   421 _P1_5	=	0x0095
                           000094   422 _P1_4	=	0x0094
                           000093   423 _P1_3	=	0x0093
                           000092   424 _P1_2	=	0x0092
                           000091   425 _P1_1	=	0x0091
                           000090   426 _P1_0	=	0x0090
                           000097   427 _TXD1_	=	0x0097
                           000096   428 _RXD1_	=	0x0096
                           000097   429 _SCK	=	0x0097
                           000096   430 _MISO	=	0x0096
                           000095   431 _MOSI	=	0x0095
                           000094   432 _SCS	=	0x0094
                           000092   433 _INT0_	=	0x0092
                           000091   434 _T2EX	=	0x0091
                           000091   435 _CAP2	=	0x0091
                           000090   436 _T2	=	0x0090
                           000090   437 _CAP1	=	0x0090
                           000097   438 _AIN7	=	0x0097
                           000096   439 _AIN6	=	0x0096
                           000095   440 _AIN5	=	0x0095
                           000094   441 _AIN4	=	0x0094
                           000093   442 _AIN3	=	0x0093
                           000092   443 _AIN2	=	0x0092
                           000091   444 _AIN1	=	0x0091
                           000090   445 _AIN0	=	0x0090
                           0000A7   446 _P2_7	=	0x00a7
                           0000A6   447 _P2_6	=	0x00a6
                           0000A5   448 _P2_5	=	0x00a5
                           0000A4   449 _P2_4	=	0x00a4
                           0000A3   450 _P2_3	=	0x00a3
                           0000A2   451 _P2_2	=	0x00a2
                           0000A1   452 _P2_1	=	0x00a1
                           0000A0   453 _P2_0	=	0x00a0
                           0000A7   454 _TXD1	=	0x00a7
                           0000A6   455 _RXD1	=	0x00a6
                           0000A5   456 _T2EX_	=	0x00a5
                           0000A5   457 _CAP2_	=	0x00a5
                           0000A4   458 _T2_	=	0x00a4
                           0000A4   459 _CAP1_	=	0x00a4
                           0000B7   460 _P3_7	=	0x00b7
                           0000B6   461 _P3_6	=	0x00b6
                           0000B5   462 _P3_5	=	0x00b5
                           0000B4   463 _P3_4	=	0x00b4
                           0000B3   464 _P3_3	=	0x00b3
                           0000B2   465 _P3_2	=	0x00b2
                           0000B1   466 _P3_1	=	0x00b1
                           0000B0   467 _P3_0	=	0x00b0
                           0000B7   468 _SCK1	=	0x00b7
                           0000B6   469 _MISO1	=	0x00b6
                           0000B5   470 _MOSI1	=	0x00b5
                           0000B5   471 _T1	=	0x00b5
                           0000B4   472 _T0	=	0x00b4
                           0000B3   473 _INT1	=	0x00b3
                           0000B2   474 _INT0	=	0x00b2
                           0000B1   475 _TXD	=	0x00b1
                           0000B0   476 _RXD	=	0x00b0
                           0000C6   477 _P4_6	=	0x00c6
                           0000C5   478 _P4_5	=	0x00c5
                           0000C4   479 _P4_4	=	0x00c4
                           0000C3   480 _P4_3	=	0x00c3
                           0000C2   481 _P4_2	=	0x00c2
                           0000C1   482 _P4_1	=	0x00c1
                           0000C0   483 _P4_0	=	0x00c0
                           00008F   484 _TF1	=	0x008f
                           00008E   485 _TR1	=	0x008e
                           00008D   486 _TF0	=	0x008d
                           00008C   487 _TR0	=	0x008c
                           00008B   488 _IE1	=	0x008b
                           00008A   489 _IT1	=	0x008a
                           000089   490 _IE0	=	0x0089
                           000088   491 _IT0	=	0x0088
                           00009F   492 _SM0	=	0x009f
                           00009E   493 _SM1	=	0x009e
                           00009D   494 _SM2	=	0x009d
                           00009C   495 _REN	=	0x009c
                           00009B   496 _TB8	=	0x009b
                           00009A   497 _RB8	=	0x009a
                           000099   498 _TI	=	0x0099
                           000098   499 _RI	=	0x0098
                           0000CF   500 _TF2	=	0x00cf
                           0000CF   501 _CAP1F	=	0x00cf
                           0000CE   502 _EXF2	=	0x00ce
                           0000CD   503 _RCLK	=	0x00cd
                           0000CC   504 _TCLK	=	0x00cc
                           0000CB   505 _EXEN2	=	0x00cb
                           0000CA   506 _TR2	=	0x00ca
                           0000C9   507 _C_T2	=	0x00c9
                           0000C8   508 _CP_RL2	=	0x00c8
                           0000FF   509 _S0_FST_ACT	=	0x00ff
                           0000FE   510 _S0_IF_OV	=	0x00fe
                           0000FD   511 _S0_IF_FIRST	=	0x00fd
                           0000FC   512 _S0_IF_BYTE	=	0x00fc
                           0000FB   513 _S0_FREE	=	0x00fb
                           0000FA   514 _S0_T_FIFO	=	0x00fa
                           0000F8   515 _S0_R_FIFO	=	0x00f8
                           0000F7   516 _ADC_START	=	0x00f7
                                    517 ;--------------------------------------------------------
                                    518 ; overlayable register banks
                                    519 ;--------------------------------------------------------
                                    520 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        521 	.ds 8
                                    522 ;--------------------------------------------------------
                                    523 ; internal ram data
                                    524 ;--------------------------------------------------------
                                    525 	.area DSEG    (DATA)
                                    526 ;--------------------------------------------------------
                                    527 ; overlayable items in internal ram
                                    528 ;--------------------------------------------------------
                                    529 ;--------------------------------------------------------
                                    530 ; indirectly addressable internal ram data
                                    531 ;--------------------------------------------------------
                                    532 	.area ISEG    (DATA)
                                    533 ;--------------------------------------------------------
                                    534 ; absolute internal ram data
                                    535 ;--------------------------------------------------------
                                    536 	.area IABS    (ABS,DATA)
                                    537 	.area IABS    (ABS,DATA)
                                    538 ;--------------------------------------------------------
                                    539 ; bit data
                                    540 ;--------------------------------------------------------
                                    541 	.area BSEG    (BIT)
                                    542 ;--------------------------------------------------------
                                    543 ; paged external ram data
                                    544 ;--------------------------------------------------------
                                    545 	.area PSEG    (PAG,XDATA)
                                    546 ;--------------------------------------------------------
                                    547 ; uninitialized external ram data
                                    548 ;--------------------------------------------------------
                                    549 	.area XSEG    (XDATA)
      000733                        550 _notify_usb_device_state_change_kb_usb_device_state_10000_47:
      000733                        551 	.ds 1
      000734                        552 _notify_usb_device_state_change_usb_device_state_10000_52:
      000734                        553 	.ds 1
      000735                        554 _usb_device_state_set_configuration_PARM_2:
      000735                        555 	.ds 1
      000736                        556 _usb_device_state_set_configuration_isConfigured_10000_54:
      000736                        557 	.ds 1
      000737                        558 _usb_device_state_set_suspend_PARM_2:
      000737                        559 	.ds 1
      000738                        560 _usb_device_state_set_resume_PARM_2:
      000738                        561 	.ds 1
      000739                        562 _usb_device_state_set_resume_isConfigured_10000_58:
      000739                        563 	.ds 1
                                    564 ;--------------------------------------------------------
                                    565 ; absolute external ram data
                                    566 ;--------------------------------------------------------
                                    567 	.area XABS    (ABS,XDATA)
                                    568 ;--------------------------------------------------------
                                    569 ; initialized external ram data
                                    570 ;--------------------------------------------------------
                                    571 	.area XISEG   (XDATA)
      000BAB                        572 _usb_device_state::
      000BAB                        573 	.ds 1
                                    574 	.area HOME    (CODE)
                                    575 	.area GSINIT0 (CODE)
                                    576 	.area GSINIT1 (CODE)
                                    577 	.area GSINIT2 (CODE)
                                    578 	.area GSINIT3 (CODE)
                                    579 	.area GSINIT4 (CODE)
                                    580 	.area GSINIT5 (CODE)
                                    581 	.area GSINIT  (CODE)
                                    582 	.area GSFINAL (CODE)
                                    583 	.area CSEG    (CODE)
                                    584 ;--------------------------------------------------------
                                    585 ; global & static initialisations
                                    586 ;--------------------------------------------------------
                                    587 	.area HOME    (CODE)
                                    588 	.area GSINIT  (CODE)
                                    589 	.area GSFINAL (CODE)
                                    590 	.area GSINIT  (CODE)
                                    591 ;--------------------------------------------------------
                                    592 ; Home
                                    593 ;--------------------------------------------------------
                                    594 	.area HOME    (CODE)
                                    595 	.area HOME    (CODE)
                                    596 ;--------------------------------------------------------
                                    597 ; code
                                    598 ;--------------------------------------------------------
                                    599 	.area CSEG    (CODE)
                                    600 ;------------------------------------------------------------
                                    601 ;Allocation info for local variables in function 'notify_usb_device_state_change_kb'
                                    602 ;------------------------------------------------------------
                                    603 ;usb_device_state Allocated with name '_notify_usb_device_state_change_kb_usb_device_state_10000_47'
                                    604 ;------------------------------------------------------------
                                    605 ;	tmk_core/protocol/usb_device_state.c:26: __attribute__((weak)) void notify_usb_device_state_change_kb(enum usb_device_state usb_device_state) {
                                    606 ;	-----------------------------------------
                                    607 ;	 function notify_usb_device_state_change_kb
                                    608 ;	-----------------------------------------
      006C9D                        609 _notify_usb_device_state_change_kb:
                           000007   610 	ar7 = 0x07
                           000006   611 	ar6 = 0x06
                           000005   612 	ar5 = 0x05
                           000004   613 	ar4 = 0x04
                           000003   614 	ar3 = 0x03
                           000002   615 	ar2 = 0x02
                           000001   616 	ar1 = 0x01
                           000000   617 	ar0 = 0x00
      006C9D E5 82            [12]  618 	mov	a,dpl
      006C9F 90 07 33         [24]  619 	mov	dptr,#_notify_usb_device_state_change_kb_usb_device_state_10000_47
      006CA2 F0               [24]  620 	movx	@dptr,a
                                    621 ;	tmk_core/protocol/usb_device_state.c:27: notify_usb_device_state_change_user(usb_device_state);
      006CA3 E0               [24]  622 	movx	a,@dptr
      006CA4 F5 82            [12]  623 	mov	dpl,a
                                    624 ;	tmk_core/protocol/usb_device_state.c:28: }
      006CA6 02 6C A9         [24]  625 	ljmp	_notify_usb_device_state_change_user
                                    626 ;------------------------------------------------------------
                                    627 ;Allocation info for local variables in function 'notify_usb_device_state_change_user'
                                    628 ;------------------------------------------------------------
                                    629 ;usb_device_state Allocated with name '_notify_usb_device_state_change_user_usb_device_state_10000_49'
                                    630 ;------------------------------------------------------------
                                    631 ;	tmk_core/protocol/usb_device_state.c:30: __attribute__((weak)) void notify_usb_device_state_change_user(enum usb_device_state usb_device_state) {}
                                    632 ;	-----------------------------------------
                                    633 ;	 function notify_usb_device_state_change_user
                                    634 ;	-----------------------------------------
      006CA9                        635 _notify_usb_device_state_change_user:
      006CA9 22               [24]  636 	ret
                                    637 ;------------------------------------------------------------
                                    638 ;Allocation info for local variables in function 'notify_usb_device_state_change'
                                    639 ;------------------------------------------------------------
                                    640 ;usb_device_state Allocated with name '_notify_usb_device_state_change_usb_device_state_10000_52'
                                    641 ;------------------------------------------------------------
                                    642 ;	tmk_core/protocol/usb_device_state.c:32: static void notify_usb_device_state_change(enum usb_device_state usb_device_state) {
                                    643 ;	-----------------------------------------
                                    644 ;	 function notify_usb_device_state_change
                                    645 ;	-----------------------------------------
      006CAA                        646 _notify_usb_device_state_change:
      006CAA E5 82            [12]  647 	mov	a,dpl
      006CAC 90 07 34         [24]  648 	mov	dptr,#_notify_usb_device_state_change_usb_device_state_10000_52
      006CAF F0               [24]  649 	movx	@dptr,a
                                    650 ;	tmk_core/protocol/usb_device_state.c:36: notify_usb_device_state_change_kb(usb_device_state);
      006CB0 E0               [24]  651 	movx	a,@dptr
      006CB1 F5 82            [12]  652 	mov	dpl,a
                                    653 ;	tmk_core/protocol/usb_device_state.c:37: }
      006CB3 02 6C 9D         [24]  654 	ljmp	_notify_usb_device_state_change_kb
                                    655 ;------------------------------------------------------------
                                    656 ;Allocation info for local variables in function 'usb_device_state_set_configuration'
                                    657 ;------------------------------------------------------------
                                    658 ;configurationNumber Allocated with name '_usb_device_state_set_configuration_PARM_2'
                                    659 ;isConfigured  Allocated with name '_usb_device_state_set_configuration_isConfigured_10000_54'
                                    660 ;------------------------------------------------------------
                                    661 ;	tmk_core/protocol/usb_device_state.c:39: void usb_device_state_set_configuration(bool isConfigured, uint8_t configurationNumber) {
                                    662 ;	-----------------------------------------
                                    663 ;	 function usb_device_state_set_configuration
                                    664 ;	-----------------------------------------
      006CB6                        665 _usb_device_state_set_configuration:
      006CB6 E5 82            [12]  666 	mov	a,dpl
      006CB8 90 07 36         [24]  667 	mov	dptr,#_usb_device_state_set_configuration_isConfigured_10000_54
      006CBB F0               [24]  668 	movx	@dptr,a
                                    669 ;	tmk_core/protocol/usb_device_state.c:40: usb_device_state = isConfigured ? USB_DEVICE_STATE_CONFIGURED : USB_DEVICE_STATE_INIT;
      006CBC E0               [24]  670 	movx	a,@dptr
      006CBD 60 04            [24]  671 	jz	00103$
      006CBF 7F 02            [12]  672 	mov	r7,#0x02
      006CC1 80 02            [24]  673 	sjmp	00104$
      006CC3                        674 00103$:
      006CC3 7F 01            [12]  675 	mov	r7,#0x01
      006CC5                        676 00104$:
      006CC5 90 0B AB         [24]  677 	mov	dptr,#_usb_device_state
      006CC8 EF               [12]  678 	mov	a,r7
      006CC9 F0               [24]  679 	movx	@dptr,a
                                    680 ;	tmk_core/protocol/usb_device_state.c:41: notify_usb_device_state_change(usb_device_state);
      006CCA 8F 82            [24]  681 	mov	dpl, r7
                                    682 ;	tmk_core/protocol/usb_device_state.c:42: }
      006CCC 02 6C AA         [24]  683 	ljmp	_notify_usb_device_state_change
                                    684 ;------------------------------------------------------------
                                    685 ;Allocation info for local variables in function 'usb_device_state_set_suspend'
                                    686 ;------------------------------------------------------------
                                    687 ;configurationNumber Allocated with name '_usb_device_state_set_suspend_PARM_2'
                                    688 ;isConfigured  Allocated with name '_usb_device_state_set_suspend_isConfigured_10000_56'
                                    689 ;------------------------------------------------------------
                                    690 ;	tmk_core/protocol/usb_device_state.c:44: void usb_device_state_set_suspend(bool isConfigured, uint8_t configurationNumber) {
                                    691 ;	-----------------------------------------
                                    692 ;	 function usb_device_state_set_suspend
                                    693 ;	-----------------------------------------
      006CCF                        694 _usb_device_state_set_suspend:
                                    695 ;	tmk_core/protocol/usb_device_state.c:45: usb_device_state = USB_DEVICE_STATE_SUSPEND;
      006CCF 90 0B AB         [24]  696 	mov	dptr,#_usb_device_state
      006CD2 74 03            [12]  697 	mov	a,#0x03
      006CD4 F0               [24]  698 	movx	@dptr,a
                                    699 ;	tmk_core/protocol/usb_device_state.c:46: notify_usb_device_state_change(usb_device_state);
      006CD5 75 82 03         [24]  700 	mov	dpl, #0x03
                                    701 ;	tmk_core/protocol/usb_device_state.c:47: }
      006CD8 02 6C AA         [24]  702 	ljmp	_notify_usb_device_state_change
                                    703 ;------------------------------------------------------------
                                    704 ;Allocation info for local variables in function 'usb_device_state_set_resume'
                                    705 ;------------------------------------------------------------
                                    706 ;configurationNumber Allocated with name '_usb_device_state_set_resume_PARM_2'
                                    707 ;isConfigured  Allocated with name '_usb_device_state_set_resume_isConfigured_10000_58'
                                    708 ;------------------------------------------------------------
                                    709 ;	tmk_core/protocol/usb_device_state.c:49: void usb_device_state_set_resume(bool isConfigured, uint8_t configurationNumber) {
                                    710 ;	-----------------------------------------
                                    711 ;	 function usb_device_state_set_resume
                                    712 ;	-----------------------------------------
      006CDB                        713 _usb_device_state_set_resume:
      006CDB E5 82            [12]  714 	mov	a,dpl
      006CDD 90 07 39         [24]  715 	mov	dptr,#_usb_device_state_set_resume_isConfigured_10000_58
      006CE0 F0               [24]  716 	movx	@dptr,a
                                    717 ;	tmk_core/protocol/usb_device_state.c:50: usb_device_state = isConfigured ? USB_DEVICE_STATE_CONFIGURED : USB_DEVICE_STATE_INIT;
      006CE1 E0               [24]  718 	movx	a,@dptr
      006CE2 60 04            [24]  719 	jz	00103$
      006CE4 7F 02            [12]  720 	mov	r7,#0x02
      006CE6 80 02            [24]  721 	sjmp	00104$
      006CE8                        722 00103$:
      006CE8 7F 01            [12]  723 	mov	r7,#0x01
      006CEA                        724 00104$:
      006CEA 90 0B AB         [24]  725 	mov	dptr,#_usb_device_state
      006CED EF               [12]  726 	mov	a,r7
      006CEE F0               [24]  727 	movx	@dptr,a
                                    728 ;	tmk_core/protocol/usb_device_state.c:51: notify_usb_device_state_change(usb_device_state);
      006CEF 8F 82            [24]  729 	mov	dpl, r7
                                    730 ;	tmk_core/protocol/usb_device_state.c:52: }
      006CF1 02 6C AA         [24]  731 	ljmp	_notify_usb_device_state_change
                                    732 ;------------------------------------------------------------
                                    733 ;Allocation info for local variables in function 'usb_device_state_set_reset'
                                    734 ;------------------------------------------------------------
                                    735 ;	tmk_core/protocol/usb_device_state.c:54: void usb_device_state_set_reset(void) {
                                    736 ;	-----------------------------------------
                                    737 ;	 function usb_device_state_init
                                    738 ;	-----------------------------------------
      006CF4                        739 _usb_device_state_init:
                                    740 ;	tmk_core/protocol/usb_device_state.c:60: usb_device_state = USB_DEVICE_STATE_INIT;
      006CF4 90 0B AB         [24]  741 	mov	dptr,#_usb_device_state
      006CF7 74 01            [12]  742 	mov	a,#0x01
      006CF9 F0               [24]  743 	movx	@dptr,a
                                    744 ;	tmk_core/protocol/usb_device_state.c:61: notify_usb_device_state_change(usb_device_state);
      006CFA 75 82 01         [24]  745 	mov	dpl, #0x01
                                    746 ;	tmk_core/protocol/usb_device_state.c:62: }
      006CFD 02 6C AA         [24]  747 	ljmp	_notify_usb_device_state_change
                                    748 	.area CSEG    (CODE)
                                    749 	.area CONST   (CODE)
                                    750 	.area XINIT   (CODE)
      00BD8B                        751 __xinit__usb_device_state:
      00BD8B 00                     752 	.db #0x00	; 0
                                    753 	.area CABS    (ABS,CODE)
