                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module usb_ak820
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-large
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _ak820_nvm_end
                                     12 	.globl _ak820_nvm_flush
                                     13 	.globl _ak820_nvm_begin
                                     14 	.globl _ak820_nvm_ok
                                     15 	.globl _ak820_nvm_diagnostic
                                     16 	.globl _mDelaymS
                                     17 	.globl _mDelayuS
                                     18 	.globl _raw_hid_receive
                                     19 	.globl _ADC_START
                                     20 	.globl _S0_R_FIFO
                                     21 	.globl _S0_T_FIFO
                                     22 	.globl _S0_FREE
                                     23 	.globl _S0_IF_BYTE
                                     24 	.globl _S0_IF_FIRST
                                     25 	.globl _S0_IF_OV
                                     26 	.globl _S0_FST_ACT
                                     27 	.globl _CP_RL2
                                     28 	.globl _C_T2
                                     29 	.globl _TR2
                                     30 	.globl _EXEN2
                                     31 	.globl _TCLK
                                     32 	.globl _RCLK
                                     33 	.globl _EXF2
                                     34 	.globl _CAP1F
                                     35 	.globl _TF2
                                     36 	.globl _RI
                                     37 	.globl _TI
                                     38 	.globl _RB8
                                     39 	.globl _TB8
                                     40 	.globl _REN
                                     41 	.globl _SM2
                                     42 	.globl _SM1
                                     43 	.globl _SM0
                                     44 	.globl _IT0
                                     45 	.globl _IE0
                                     46 	.globl _IT1
                                     47 	.globl _IE1
                                     48 	.globl _TR0
                                     49 	.globl _TF0
                                     50 	.globl _TR1
                                     51 	.globl _TF1
                                     52 	.globl _P4_0
                                     53 	.globl _P4_1
                                     54 	.globl _P4_2
                                     55 	.globl _P4_3
                                     56 	.globl _P4_4
                                     57 	.globl _P4_5
                                     58 	.globl _P4_6
                                     59 	.globl _RXD
                                     60 	.globl _TXD
                                     61 	.globl _INT0
                                     62 	.globl _INT1
                                     63 	.globl _T0
                                     64 	.globl _T1
                                     65 	.globl _MOSI1
                                     66 	.globl _MISO1
                                     67 	.globl _SCK1
                                     68 	.globl _P3_0
                                     69 	.globl _P3_1
                                     70 	.globl _P3_2
                                     71 	.globl _P3_3
                                     72 	.globl _P3_4
                                     73 	.globl _P3_5
                                     74 	.globl _P3_6
                                     75 	.globl _P3_7
                                     76 	.globl _CAP1_
                                     77 	.globl _T2_
                                     78 	.globl _CAP2_
                                     79 	.globl _T2EX_
                                     80 	.globl _RXD1
                                     81 	.globl _TXD1
                                     82 	.globl _P2_0
                                     83 	.globl _P2_1
                                     84 	.globl _P2_2
                                     85 	.globl _P2_3
                                     86 	.globl _P2_4
                                     87 	.globl _P2_5
                                     88 	.globl _P2_6
                                     89 	.globl _P2_7
                                     90 	.globl _AIN0
                                     91 	.globl _AIN1
                                     92 	.globl _AIN2
                                     93 	.globl _AIN3
                                     94 	.globl _AIN4
                                     95 	.globl _AIN5
                                     96 	.globl _AIN6
                                     97 	.globl _AIN7
                                     98 	.globl _CAP1
                                     99 	.globl _T2
                                    100 	.globl _CAP2
                                    101 	.globl _T2EX
                                    102 	.globl _INT0_
                                    103 	.globl _SCS
                                    104 	.globl _MOSI
                                    105 	.globl _MISO
                                    106 	.globl _SCK
                                    107 	.globl _RXD1_
                                    108 	.globl _TXD1_
                                    109 	.globl _P1_0
                                    110 	.globl _P1_1
                                    111 	.globl _P1_2
                                    112 	.globl _P1_3
                                    113 	.globl _P1_4
                                    114 	.globl _P1_5
                                    115 	.globl _P1_6
                                    116 	.globl _P1_7
                                    117 	.globl _AIN8
                                    118 	.globl _AIN9
                                    119 	.globl _AIN10
                                    120 	.globl _AIN11
                                    121 	.globl _AIN12
                                    122 	.globl _AIN13
                                    123 	.globl _RXD_
                                    124 	.globl _TXD_
                                    125 	.globl _SCL0
                                    126 	.globl _SDA0
                                    127 	.globl _P0_0
                                    128 	.globl _P0_1
                                    129 	.globl _P0_2
                                    130 	.globl _P0_3
                                    131 	.globl _P0_4
                                    132 	.globl _P0_5
                                    133 	.globl _P0_6
                                    134 	.globl _P0_7
                                    135 	.globl _IE_SPI0
                                    136 	.globl _IE_USB
                                    137 	.globl _IE_ADC
                                    138 	.globl _IE_UART1
                                    139 	.globl _IE_PWM_I2C
                                    140 	.globl _IE_GPIO
                                    141 	.globl _IE_WDOG
                                    142 	.globl _PX0
                                    143 	.globl _PT0
                                    144 	.globl _PX1
                                    145 	.globl _PT1
                                    146 	.globl _PS
                                    147 	.globl _PT2
                                    148 	.globl _PL_FLAG
                                    149 	.globl _PH_FLAG
                                    150 	.globl _EX0
                                    151 	.globl _ET0
                                    152 	.globl _EX1
                                    153 	.globl _ET1
                                    154 	.globl _ES
                                    155 	.globl _ET2
                                    156 	.globl _E_DIS
                                    157 	.globl _EA
                                    158 	.globl _P
                                    159 	.globl _F1
                                    160 	.globl _OV
                                    161 	.globl _RS0
                                    162 	.globl _RS1
                                    163 	.globl _F0
                                    164 	.globl _AC
                                    165 	.globl _CY
                                    166 	.globl _I2CS_INT_ST
                                    167 	.globl _I2CX_INT
                                    168 	.globl _LED_STATUS
                                    169 	.globl _LED_DMA_H
                                    170 	.globl _LED_DMA_L
                                    171 	.globl _LED_DMA
                                    172 	.globl _LED_PWM_OE
                                    173 	.globl _LED_COMMON
                                    174 	.globl _ADC_CHAN
                                    175 	.globl _ADC_DAT_H
                                    176 	.globl _ADC_DAT_L
                                    177 	.globl _ADC_DAT
                                    178 	.globl _ADC_CTRL
                                    179 	.globl _SPI1_CK_SE
                                    180 	.globl _SPI1_CTRL
                                    181 	.globl _SPI1_DATA
                                    182 	.globl _SPI1_STAT
                                    183 	.globl _SIF1
                                    184 	.globl _SBAUD1
                                    185 	.globl _SBUF1
                                    186 	.globl _SCON1
                                    187 	.globl _SPI0_SETUP
                                    188 	.globl _SPI0_CK_SE
                                    189 	.globl _SPI0_CTRL
                                    190 	.globl _SPI0_DATA
                                    191 	.globl _SPI0_STAT
                                    192 	.globl _T2CAP1H
                                    193 	.globl _T2CAP1L
                                    194 	.globl _T2CAP1
                                    195 	.globl _TH2
                                    196 	.globl _TL2
                                    197 	.globl _T2COUNT
                                    198 	.globl _RCAP2H
                                    199 	.globl _RCAP2L
                                    200 	.globl _RCAP2
                                    201 	.globl _T2MOD
                                    202 	.globl _T2CON
                                    203 	.globl _SBUF
                                    204 	.globl _SCON
                                    205 	.globl _TH1
                                    206 	.globl _TH0
                                    207 	.globl _TL1
                                    208 	.globl _TL0
                                    209 	.globl _TMOD
                                    210 	.globl _TCON
                                    211 	.globl _XBUS_AUX
                                    212 	.globl _P7
                                    213 	.globl _P6_DIR
                                    214 	.globl _P6_OUT_PU
                                    215 	.globl _P6_IN
                                    216 	.globl _P5_DIR
                                    217 	.globl _P5_OUT_PU
                                    218 	.globl _P5_IN
                                    219 	.globl _P4_LED_KEY
                                    220 	.globl _P4_DIR_PU
                                    221 	.globl _P4_MOD_OC
                                    222 	.globl _P4
                                    223 	.globl _P3_DIR_PU
                                    224 	.globl _P3_MOD_OC
                                    225 	.globl _P3
                                    226 	.globl _P2_DIR_PU
                                    227 	.globl _P2_MOD_OC
                                    228 	.globl _P2
                                    229 	.globl _P1_DIR_PU
                                    230 	.globl _P1_MOD_OC
                                    231 	.globl _P1
                                    232 	.globl _P0_DIR_PU
                                    233 	.globl _P0_MOD_OC
                                    234 	.globl _P0
                                    235 	.globl _ROM_CTRL
                                    236 	.globl _ROM_DATA_HH
                                    237 	.globl _ROM_DATA_HL
                                    238 	.globl _ROM_DATA_HI
                                    239 	.globl _ROM_ADDR_H
                                    240 	.globl _ROM_ADDR_L
                                    241 	.globl _ROM_ADDR
                                    242 	.globl _GPIO_IE
                                    243 	.globl _IP_EX
                                    244 	.globl _IE_EX
                                    245 	.globl _IP
                                    246 	.globl _IE
                                    247 	.globl _WDOG_COUNT
                                    248 	.globl _RESET_KEEP
                                    249 	.globl _WAKE_CTRL
                                    250 	.globl _CLOCK_CFG
                                    251 	.globl _POWER_CFG
                                    252 	.globl _PCON
                                    253 	.globl _GLOBAL_CFG
                                    254 	.globl _SAFE_MOD
                                    255 	.globl _DPH
                                    256 	.globl _DPL
                                    257 	.globl _SP
                                    258 	.globl _A_INV
                                    259 	.globl _B
                                    260 	.globl _ACC
                                    261 	.globl _PSW
                                    262 	.globl _ak820_usb_raw_send_PARM_2
                                    263 	.globl _ak820_usb_try_send_PARM_3
                                    264 	.globl _ak820_usb_try_send_PARM_2
                                    265 	.globl _ak820_usb_send_PARM_3
                                    266 	.globl _ak820_usb_send_PARM_2
                                    267 	.globl _ak820_main_heartbeat
                                    268 	.globl _ak820_boot_stage
                                    269 	.globl _KB_USB_SetReport
                                    270 	.globl _KB_USB_UpStatus
                                    271 	.globl _MCU_Sleep_Operate
                                    272 	.globl _USB_SleepStatus
                                    273 	.globl _USB_EnumStatus
                                    274 	.globl _D0UsbConfig
                                    275 	.globl _pD0Descr
                                    276 	.globl _D0SetupLen
                                    277 	.globl _D0SetupReqCode
                                    278 	.globl _USB_DeviceInterrupt
                                    279 	.globl _USB_Device_Init
                                    280 	.globl _USB_WakeUp_PC
                                    281 	.globl _ak820_usb_send
                                    282 	.globl _ak820_usb_try_send
                                    283 	.globl _ak820_usb_raw_send
                                    284 	.globl _ak820_usb_raw_task
                                    285 	.globl _ak820_usb_take_keyboard_reset
                                    286 ;--------------------------------------------------------
                                    287 ; special function registers
                                    288 ;--------------------------------------------------------
                                    289 	.area RSEG    (ABS,DATA)
      000000                        290 	.org 0x0000
                           0000D0   291 _PSW	=	0x00d0
                           0000E0   292 _ACC	=	0x00e0
                           0000F0   293 _B	=	0x00f0
                           0000FD   294 _A_INV	=	0x00fd
                           000081   295 _SP	=	0x0081
                           000082   296 _DPL	=	0x0082
                           000083   297 _DPH	=	0x0083
                           0000A1   298 _SAFE_MOD	=	0x00a1
                           0000B1   299 _GLOBAL_CFG	=	0x00b1
                           000087   300 _PCON	=	0x0087
                           0000BA   301 _POWER_CFG	=	0x00ba
                           0000B9   302 _CLOCK_CFG	=	0x00b9
                           0000A9   303 _WAKE_CTRL	=	0x00a9
                           0000FE   304 _RESET_KEEP	=	0x00fe
                           0000FF   305 _WDOG_COUNT	=	0x00ff
                           0000A8   306 _IE	=	0x00a8
                           0000B8   307 _IP	=	0x00b8
                           0000E8   308 _IE_EX	=	0x00e8
                           0000E9   309 _IP_EX	=	0x00e9
                           0000B2   310 _GPIO_IE	=	0x00b2
                           008584   311 _ROM_ADDR	=	0x8584
                           000084   312 _ROM_ADDR_L	=	0x0084
                           000085   313 _ROM_ADDR_H	=	0x0085
                           008F8E   314 _ROM_DATA_HI	=	0x8f8e
                           00008E   315 _ROM_DATA_HL	=	0x008e
                           00008F   316 _ROM_DATA_HH	=	0x008f
                           000086   317 _ROM_CTRL	=	0x0086
                           000080   318 _P0	=	0x0080
                           0000C4   319 _P0_MOD_OC	=	0x00c4
                           0000C5   320 _P0_DIR_PU	=	0x00c5
                           000090   321 _P1	=	0x0090
                           000092   322 _P1_MOD_OC	=	0x0092
                           000093   323 _P1_DIR_PU	=	0x0093
                           0000A0   324 _P2	=	0x00a0
                           000094   325 _P2_MOD_OC	=	0x0094
                           000095   326 _P2_DIR_PU	=	0x0095
                           0000B0   327 _P3	=	0x00b0
                           000096   328 _P3_MOD_OC	=	0x0096
                           000097   329 _P3_DIR_PU	=	0x0097
                           0000C0   330 _P4	=	0x00c0
                           0000C2   331 _P4_MOD_OC	=	0x00c2
                           0000C3   332 _P4_DIR_PU	=	0x00c3
                           0000C1   333 _P4_LED_KEY	=	0x00c1
                           0000AA   334 _P5_IN	=	0x00aa
                           0000AB   335 _P5_OUT_PU	=	0x00ab
                           0000AC   336 _P5_DIR	=	0x00ac
                           0000AD   337 _P6_IN	=	0x00ad
                           0000AE   338 _P6_OUT_PU	=	0x00ae
                           0000AF   339 _P6_DIR	=	0x00af
                           0000F1   340 _P7	=	0x00f1
                           0000A2   341 _XBUS_AUX	=	0x00a2
                           000088   342 _TCON	=	0x0088
                           000089   343 _TMOD	=	0x0089
                           00008A   344 _TL0	=	0x008a
                           00008B   345 _TL1	=	0x008b
                           00008C   346 _TH0	=	0x008c
                           00008D   347 _TH1	=	0x008d
                           000098   348 _SCON	=	0x0098
                           000099   349 _SBUF	=	0x0099
                           0000C8   350 _T2CON	=	0x00c8
                           0000C9   351 _T2MOD	=	0x00c9
                           00CBCA   352 _RCAP2	=	0xcbca
                           0000CA   353 _RCAP2L	=	0x00ca
                           0000CB   354 _RCAP2H	=	0x00cb
                           00CDCC   355 _T2COUNT	=	0xcdcc
                           0000CC   356 _TL2	=	0x00cc
                           0000CD   357 _TH2	=	0x00cd
                           00CFCE   358 _T2CAP1	=	0xcfce
                           0000CE   359 _T2CAP1L	=	0x00ce
                           0000CF   360 _T2CAP1H	=	0x00cf
                           0000F8   361 _SPI0_STAT	=	0x00f8
                           0000F9   362 _SPI0_DATA	=	0x00f9
                           0000FA   363 _SPI0_CTRL	=	0x00fa
                           0000FB   364 _SPI0_CK_SE	=	0x00fb
                           0000FC   365 _SPI0_SETUP	=	0x00fc
                           0000BC   366 _SCON1	=	0x00bc
                           0000BD   367 _SBUF1	=	0x00bd
                           0000BE   368 _SBAUD1	=	0x00be
                           0000BF   369 _SIF1	=	0x00bf
                           0000B4   370 _SPI1_STAT	=	0x00b4
                           0000B5   371 _SPI1_DATA	=	0x00b5
                           0000B6   372 _SPI1_CTRL	=	0x00b6
                           0000B7   373 _SPI1_CK_SE	=	0x00b7
                           0000F3   374 _ADC_CTRL	=	0x00f3
                           00F5F4   375 _ADC_DAT	=	0xf5f4
                           0000F4   376 _ADC_DAT_L	=	0x00f4
                           0000F5   377 _ADC_DAT_H	=	0x00f5
                           0000F6   378 _ADC_CHAN	=	0x00f6
                           0000A6   379 _LED_COMMON	=	0x00a6
                           0000A7   380 _LED_PWM_OE	=	0x00a7
                           00C7C6   381 _LED_DMA	=	0xc7c6
                           0000C6   382 _LED_DMA_L	=	0x00c6
                           0000C7   383 _LED_DMA_H	=	0x00c7
                           0000F7   384 _LED_STATUS	=	0x00f7
                           0000B3   385 _I2CX_INT	=	0x00b3
                           0000BB   386 _I2CS_INT_ST	=	0x00bb
                                    387 ;--------------------------------------------------------
                                    388 ; special function bits
                                    389 ;--------------------------------------------------------
                                    390 	.area RSEG    (ABS,DATA)
      000000                        391 	.org 0x0000
                           0000D7   392 _CY	=	0x00d7
                           0000D6   393 _AC	=	0x00d6
                           0000D5   394 _F0	=	0x00d5
                           0000D4   395 _RS1	=	0x00d4
                           0000D3   396 _RS0	=	0x00d3
                           0000D2   397 _OV	=	0x00d2
                           0000D1   398 _F1	=	0x00d1
                           0000D0   399 _P	=	0x00d0
                           0000AF   400 _EA	=	0x00af
                           0000AE   401 _E_DIS	=	0x00ae
                           0000AD   402 _ET2	=	0x00ad
                           0000AC   403 _ES	=	0x00ac
                           0000AB   404 _ET1	=	0x00ab
                           0000AA   405 _EX1	=	0x00aa
                           0000A9   406 _ET0	=	0x00a9
                           0000A8   407 _EX0	=	0x00a8
                           0000BF   408 _PH_FLAG	=	0x00bf
                           0000BE   409 _PL_FLAG	=	0x00be
                           0000BD   410 _PT2	=	0x00bd
                           0000BC   411 _PS	=	0x00bc
                           0000BB   412 _PT1	=	0x00bb
                           0000BA   413 _PX1	=	0x00ba
                           0000B9   414 _PT0	=	0x00b9
                           0000B8   415 _PX0	=	0x00b8
                           0000EF   416 _IE_WDOG	=	0x00ef
                           0000EE   417 _IE_GPIO	=	0x00ee
                           0000ED   418 _IE_PWM_I2C	=	0x00ed
                           0000EC   419 _IE_UART1	=	0x00ec
                           0000EB   420 _IE_ADC	=	0x00eb
                           0000E9   421 _IE_USB	=	0x00e9
                           0000E8   422 _IE_SPI0	=	0x00e8
                           000087   423 _P0_7	=	0x0087
                           000086   424 _P0_6	=	0x0086
                           000085   425 _P0_5	=	0x0085
                           000084   426 _P0_4	=	0x0084
                           000083   427 _P0_3	=	0x0083
                           000082   428 _P0_2	=	0x0082
                           000081   429 _P0_1	=	0x0081
                           000080   430 _P0_0	=	0x0080
                           000081   431 _SDA0	=	0x0081
                           000080   432 _SCL0	=	0x0080
                           000083   433 _TXD_	=	0x0083
                           000082   434 _RXD_	=	0x0082
                           000085   435 _AIN13	=	0x0085
                           000084   436 _AIN12	=	0x0084
                           000083   437 _AIN11	=	0x0083
                           000082   438 _AIN10	=	0x0082
                           000081   439 _AIN9	=	0x0081
                           000080   440 _AIN8	=	0x0080
                           000097   441 _P1_7	=	0x0097
                           000096   442 _P1_6	=	0x0096
                           000095   443 _P1_5	=	0x0095
                           000094   444 _P1_4	=	0x0094
                           000093   445 _P1_3	=	0x0093
                           000092   446 _P1_2	=	0x0092
                           000091   447 _P1_1	=	0x0091
                           000090   448 _P1_0	=	0x0090
                           000097   449 _TXD1_	=	0x0097
                           000096   450 _RXD1_	=	0x0096
                           000097   451 _SCK	=	0x0097
                           000096   452 _MISO	=	0x0096
                           000095   453 _MOSI	=	0x0095
                           000094   454 _SCS	=	0x0094
                           000092   455 _INT0_	=	0x0092
                           000091   456 _T2EX	=	0x0091
                           000091   457 _CAP2	=	0x0091
                           000090   458 _T2	=	0x0090
                           000090   459 _CAP1	=	0x0090
                           000097   460 _AIN7	=	0x0097
                           000096   461 _AIN6	=	0x0096
                           000095   462 _AIN5	=	0x0095
                           000094   463 _AIN4	=	0x0094
                           000093   464 _AIN3	=	0x0093
                           000092   465 _AIN2	=	0x0092
                           000091   466 _AIN1	=	0x0091
                           000090   467 _AIN0	=	0x0090
                           0000A7   468 _P2_7	=	0x00a7
                           0000A6   469 _P2_6	=	0x00a6
                           0000A5   470 _P2_5	=	0x00a5
                           0000A4   471 _P2_4	=	0x00a4
                           0000A3   472 _P2_3	=	0x00a3
                           0000A2   473 _P2_2	=	0x00a2
                           0000A1   474 _P2_1	=	0x00a1
                           0000A0   475 _P2_0	=	0x00a0
                           0000A7   476 _TXD1	=	0x00a7
                           0000A6   477 _RXD1	=	0x00a6
                           0000A5   478 _T2EX_	=	0x00a5
                           0000A5   479 _CAP2_	=	0x00a5
                           0000A4   480 _T2_	=	0x00a4
                           0000A4   481 _CAP1_	=	0x00a4
                           0000B7   482 _P3_7	=	0x00b7
                           0000B6   483 _P3_6	=	0x00b6
                           0000B5   484 _P3_5	=	0x00b5
                           0000B4   485 _P3_4	=	0x00b4
                           0000B3   486 _P3_3	=	0x00b3
                           0000B2   487 _P3_2	=	0x00b2
                           0000B1   488 _P3_1	=	0x00b1
                           0000B0   489 _P3_0	=	0x00b0
                           0000B7   490 _SCK1	=	0x00b7
                           0000B6   491 _MISO1	=	0x00b6
                           0000B5   492 _MOSI1	=	0x00b5
                           0000B5   493 _T1	=	0x00b5
                           0000B4   494 _T0	=	0x00b4
                           0000B3   495 _INT1	=	0x00b3
                           0000B2   496 _INT0	=	0x00b2
                           0000B1   497 _TXD	=	0x00b1
                           0000B0   498 _RXD	=	0x00b0
                           0000C6   499 _P4_6	=	0x00c6
                           0000C5   500 _P4_5	=	0x00c5
                           0000C4   501 _P4_4	=	0x00c4
                           0000C3   502 _P4_3	=	0x00c3
                           0000C2   503 _P4_2	=	0x00c2
                           0000C1   504 _P4_1	=	0x00c1
                           0000C0   505 _P4_0	=	0x00c0
                           00008F   506 _TF1	=	0x008f
                           00008E   507 _TR1	=	0x008e
                           00008D   508 _TF0	=	0x008d
                           00008C   509 _TR0	=	0x008c
                           00008B   510 _IE1	=	0x008b
                           00008A   511 _IT1	=	0x008a
                           000089   512 _IE0	=	0x0089
                           000088   513 _IT0	=	0x0088
                           00009F   514 _SM0	=	0x009f
                           00009E   515 _SM1	=	0x009e
                           00009D   516 _SM2	=	0x009d
                           00009C   517 _REN	=	0x009c
                           00009B   518 _TB8	=	0x009b
                           00009A   519 _RB8	=	0x009a
                           000099   520 _TI	=	0x0099
                           000098   521 _RI	=	0x0098
                           0000CF   522 _TF2	=	0x00cf
                           0000CF   523 _CAP1F	=	0x00cf
                           0000CE   524 _EXF2	=	0x00ce
                           0000CD   525 _RCLK	=	0x00cd
                           0000CC   526 _TCLK	=	0x00cc
                           0000CB   527 _EXEN2	=	0x00cb
                           0000CA   528 _TR2	=	0x00ca
                           0000C9   529 _C_T2	=	0x00c9
                           0000C8   530 _CP_RL2	=	0x00c8
                           0000FF   531 _S0_FST_ACT	=	0x00ff
                           0000FE   532 _S0_IF_OV	=	0x00fe
                           0000FD   533 _S0_IF_FIRST	=	0x00fd
                           0000FC   534 _S0_IF_BYTE	=	0x00fc
                           0000FB   535 _S0_FREE	=	0x00fb
                           0000FA   536 _S0_T_FIFO	=	0x00fa
                           0000F8   537 _S0_R_FIFO	=	0x00f8
                           0000F7   538 _ADC_START	=	0x00f7
                                    539 ;--------------------------------------------------------
                                    540 ; overlayable register banks
                                    541 ;--------------------------------------------------------
                                    542 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        543 	.ds 8
                                    544 ;--------------------------------------------------------
                                    545 ; internal ram data
                                    546 ;--------------------------------------------------------
                                    547 	.area DSEG    (DATA)
      000024                        548 _control_setup_sloc1_1_0:
      000024                        549 	.ds 2
      000026                        550 _control_setup_sloc2_1_0:
      000026                        551 	.ds 2
      000028                        552 _control_setup_sloc3_1_0:
      000028                        553 	.ds 1
      000029                        554 _ak820_usb_send_sloc1_1_0:
      000029                        555 	.ds 2
      00002B                        556 _ak820_usb_send_sloc2_1_0:
      00002B                        557 	.ds 2
      00002D                        558 _ak820_usb_send_sloc3_1_0:
      00002D                        559 	.ds 2
      00002F                        560 _ak820_usb_raw_task_sloc0_1_0:
      00002F                        561 	.ds 2
                                    562 ;--------------------------------------------------------
                                    563 ; overlayable items in internal ram
                                    564 ;--------------------------------------------------------
                                    565 ;--------------------------------------------------------
                                    566 ; indirectly addressable internal ram data
                                    567 ;--------------------------------------------------------
                                    568 	.area ISEG    (DATA)
                                    569 ;--------------------------------------------------------
                                    570 ; absolute internal ram data
                                    571 ;--------------------------------------------------------
                                    572 	.area IABS    (ABS,DATA)
                                    573 	.area IABS    (ABS,DATA)
                                    574 ;--------------------------------------------------------
                                    575 ; bit data
                                    576 ;--------------------------------------------------------
                                    577 	.area BSEG    (BIT)
      000009                        578 _control_setup_sloc0_1_0:
      000009                        579 	.ds 1
      00000A                        580 _ak820_usb_send_sloc0_1_0:
      00000A                        581 	.ds 1
      00000B                        582 _ak820_usb_try_send_sloc0_1_0:
      00000B                        583 	.ds 1
      00000C                        584 _ak820_usb_raw_task_sloc1_1_0:
      00000C                        585 	.ds 1
      00000D                        586 _ak820_usb_take_keyboard_reset_sloc0_1_0:
      00000D                        587 	.ds 1
                                    588 ;--------------------------------------------------------
                                    589 ; paged external ram data
                                    590 ;--------------------------------------------------------
                                    591 	.area PSEG    (PAG,XDATA)
                                    592 ;--------------------------------------------------------
                                    593 ; uninitialized external ram data
                                    594 ;--------------------------------------------------------
                                    595 	.area XSEG    (XDATA)
      000686                        596 _D0SetupReqCode::
      000686                        597 	.ds 1
      000687                        598 _D0SetupLen::
      000687                        599 	.ds 2
      000689                        600 _pD0Descr::
      000689                        601 	.ds 3
      00068C                        602 _D0UsbConfig::
      00068C                        603 	.ds 1
      00068D                        604 _USB_EnumStatus::
      00068D                        605 	.ds 1
      00068E                        606 _USB_SleepStatus::
      00068E                        607 	.ds 1
      00068F                        608 _MCU_Sleep_Operate::
      00068F                        609 	.ds 1
      000690                        610 _KB_USB_UpStatus::
      000690                        611 	.ds 1
      000691                        612 _KB_USB_SetReport::
      000691                        613 	.ds 1
      000692                        614 _ak820_boot_stage::
      000692                        615 	.ds 1
      000693                        616 _ak820_main_heartbeat::
      000693                        617 	.ds 1
      000694                        618 _raw_state:
      000694                        619 	.ds 1
      000695                        620 _raw_buffer:
      000695                        621 	.ds 32
      0006B5                        622 _raw_reply_without_nvm:
      0006B5                        623 	.ds 1
      0006B6                        624 _keyboard_reset:
      0006B6                        625 	.ds 1
      0006B7                        626 _input_snapshot:
      0006B7                        627 	.ds 46
      0006E5                        628 _control_phase:
      0006E5                        629 	.ds 1
      0006E6                        630 _output_kind:
      0006E6                        631 	.ds 1
      0006E7                        632 _output_report_id:
      0006E7                        633 	.ds 1
      0006E8                        634 _control_zlp:
      0006E8                        635 	.ds 1
      0006E9                        636 _control_pointer:
      0006E9                        637 	.ds 2
      0006EB                        638 _descriptor_select_PARM_2:
      0006EB                        639 	.ds 1
      0006EC                        640 _descriptor_select_PARM_3:
      0006EC                        641 	.ds 2
      0006EE                        642 _descriptor_select_type_10000_265:
      0006EE                        643 	.ds 1
      0006EF                        644 _control_setup_length_10000_286:
      0006EF                        645 	.ds 2
      0006F1                        646 _control_setup_offset_10000_286:
      0006F1                        647 	.ds 1
      0006F2                        648 _ak820_usb_send_PARM_2:
      0006F2                        649 	.ds 2
      0006F4                        650 _ak820_usb_send_PARM_3:
      0006F4                        651 	.ds 1
      0006F5                        652 _ak820_usb_send_endpoint_10000_412:
      0006F5                        653 	.ds 1
      0006F6                        654 _ak820_usb_send_offset_10000_413:
      0006F6                        655 	.ds 1
      0006F7                        656 _ak820_usb_try_send_PARM_2:
      0006F7                        657 	.ds 2
      0006F9                        658 _ak820_usb_try_send_PARM_3:
      0006F9                        659 	.ds 1
      0006FA                        660 _ak820_usb_try_send_endpoint_10000_433:
      0006FA                        661 	.ds 1
      0006FB                        662 _ak820_usb_try_send_sent_10000_434:
      0006FB                        663 	.ds 1
      0006FC                        664 _ak820_usb_raw_send_PARM_2:
      0006FC                        665 	.ds 1
      0006FD                        666 _ak820_usb_raw_send_report_10000_449:
      0006FD                        667 	.ds 3
                                    668 ;--------------------------------------------------------
                                    669 ; absolute external ram data
                                    670 ;--------------------------------------------------------
                                    671 	.area XABS    (ABS,XDATA)
                                    672 ;--------------------------------------------------------
                                    673 ; initialized external ram data
                                    674 ;--------------------------------------------------------
                                    675 	.area XISEG   (XDATA)
                                    676 	.area HOME    (CODE)
                                    677 	.area GSINIT0 (CODE)
                                    678 	.area GSINIT1 (CODE)
                                    679 	.area GSINIT2 (CODE)
                                    680 	.area GSINIT3 (CODE)
                                    681 	.area GSINIT4 (CODE)
                                    682 	.area GSINIT5 (CODE)
                                    683 	.area GSINIT  (CODE)
                                    684 	.area GSFINAL (CODE)
                                    685 	.area CSEG    (CODE)
                                    686 ;--------------------------------------------------------
                                    687 ; global & static initialisations
                                    688 ;--------------------------------------------------------
                                    689 	.area HOME    (CODE)
                                    690 	.area GSINIT  (CODE)
                                    691 	.area GSFINAL (CODE)
                                    692 	.area GSINIT  (CODE)
                                    693 ;--------------------------------------------------------
                                    694 ; Home
                                    695 ;--------------------------------------------------------
                                    696 	.area HOME    (CODE)
                                    697 	.area HOME    (CODE)
                                    698 ;--------------------------------------------------------
                                    699 ; code
                                    700 ;--------------------------------------------------------
                                    701 	.area CSEG    (CODE)
                                    702 ;------------------------------------------------------------
                                    703 ;Allocation info for local variables in function 'KEYCODE2SYSTEM'
                                    704 ;------------------------------------------------------------
                                    705 ;key           Allocated with name '_KEYCODE2SYSTEM_key_10000_45'
                                    706 ;------------------------------------------------------------
                                    707 ;	tmk_core/protocol/report.h:262: static inline uint16_t KEYCODE2SYSTEM(uint8_t key) {
                                    708 ;	-----------------------------------------
                           000007   709 	ar7 = 0x07
                           000006   710 	ar6 = 0x06
                           000005   711 	ar5 = 0x05
                           000004   712 	ar4 = 0x04
                           000003   713 	ar3 = 0x03
                           000002   714 	ar2 = 0x02
                           000001   715 	ar1 = 0x01
                           000000   716 	ar0 = 0x00
                                    717 ;	 function raw_abort
                                    718 ;	-----------------------------------------
      005400                        719 _raw_abort:
                                    720 ;	tmk_core/protocol/ch555/usb_ak820.c:87: if (raw_state == RAW_WORK || raw_state == RAW_TX_ACTIVE ||
      005400 90 06 94         [24]  721 	mov	dptr,#_raw_state
      005403 E0               [24]  722 	movx	a,@dptr
      005404 FF               [12]  723 	mov	r7,a
      005405 BF 03 02         [24]  724 	cjne	r7,#0x03,00130$
      005408 80 1C            [24]  725 	sjmp	00101$
      00540A                        726 00130$:
      00540A 90 06 94         [24]  727 	mov	dptr,#_raw_state
      00540D E0               [24]  728 	movx	a,@dptr
      00540E FF               [12]  729 	mov	r7,a
      00540F BF 04 02         [24]  730 	cjne	r7,#0x04,00131$
      005412 80 12            [24]  731 	sjmp	00101$
      005414                        732 00131$:
                                    733 ;	tmk_core/protocol/ch555/usb_ak820.c:88: raw_state == RAW_DRAINED || raw_state == RAW_CANCELLED)
      005414 90 06 94         [24]  734 	mov	dptr,#_raw_state
      005417 E0               [24]  735 	movx	a,@dptr
      005418 FF               [12]  736 	mov	r7,a
      005419 BF 06 02         [24]  737 	cjne	r7,#0x06,00132$
      00541C 80 08            [24]  738 	sjmp	00101$
      00541E                        739 00132$:
      00541E 90 06 94         [24]  740 	mov	dptr,#_raw_state
      005421 E0               [24]  741 	movx	a,@dptr
      005422 FF               [12]  742 	mov	r7,a
      005423 BF 07 08         [24]  743 	cjne	r7,#0x07,00102$
      005426                        744 00101$:
                                    745 ;	tmk_core/protocol/ch555/usb_ak820.c:89: raw_state = RAW_CANCELLED;
      005426 90 06 94         [24]  746 	mov	dptr,#_raw_state
      005429 74 07            [12]  747 	mov	a,#0x07
      00542B F0               [24]  748 	movx	@dptr,a
      00542C 80 05            [24]  749 	sjmp	00103$
      00542E                        750 00102$:
                                    751 ;	tmk_core/protocol/ch555/usb_ak820.c:91: raw_state = RAW_IDLE;
      00542E 90 06 94         [24]  752 	mov	dptr,#_raw_state
      005431 E4               [12]  753 	clr	a
      005432 F0               [24]  754 	movx	@dptr,a
      005433                        755 00103$:
                                    756 ;	tmk_core/protocol/ch555/usb_ak820.c:92: output_kind = OUTPUT_NONE;
      005433 90 06 E6         [24]  757 	mov	dptr,#_output_kind
      005436 E4               [12]  758 	clr	a
      005437 F0               [24]  759 	movx	@dptr,a
                                    760 ;	tmk_core/protocol/ch555/usb_ak820.c:93: }
      005438 22               [24]  761 	ret
                                    762 ;------------------------------------------------------------
                                    763 ;Allocation info for local variables in function 'raw_complete'
                                    764 ;------------------------------------------------------------
                                    765 ;	tmk_core/protocol/ch555/usb_ak820.c:95: static void raw_complete(void) {
                                    766 ;	-----------------------------------------
                                    767 ;	 function raw_complete
                                    768 ;	-----------------------------------------
      005439                        769 _raw_complete:
                                    770 ;	tmk_core/protocol/ch555/usb_ak820.c:96: if (raw_state == RAW_TX_ACTIVE) raw_state = RAW_DRAINED;
      005439 90 06 94         [24]  771 	mov	dptr,#_raw_state
      00543C E0               [24]  772 	movx	a,@dptr
      00543D FF               [12]  773 	mov	r7,a
      00543E BF 04 07         [24]  774 	cjne	r7,#0x04,00104$
      005441 90 06 94         [24]  775 	mov	dptr,#_raw_state
      005444 74 06            [12]  776 	mov	a,#0x06
      005446 F0               [24]  777 	movx	@dptr,a
      005447 22               [24]  778 	ret
      005448                        779 00104$:
                                    780 ;	tmk_core/protocol/ch555/usb_ak820.c:97: else if (raw_state == RAW_TX_WAIT) raw_state = RAW_IDLE;
      005448 90 06 94         [24]  781 	mov	dptr,#_raw_state
      00544B E0               [24]  782 	movx	a,@dptr
      00544C FF               [12]  783 	mov	r7,a
      00544D BF 05 05         [24]  784 	cjne	r7,#0x05,00106$
      005450 90 06 94         [24]  785 	mov	dptr,#_raw_state
      005453 E4               [12]  786 	clr	a
      005454 F0               [24]  787 	movx	@dptr,a
      005455                        788 00106$:
                                    789 ;	tmk_core/protocol/ch555/usb_ak820.c:98: }
      005455 22               [24]  790 	ret
                                    791 ;------------------------------------------------------------
                                    792 ;Allocation info for local variables in function 'endpoints_reset'
                                    793 ;------------------------------------------------------------
                                    794 ;i             Allocated with name '_endpoints_reset_i_10000_255'
                                    795 ;------------------------------------------------------------
                                    796 ;	tmk_core/protocol/ch555/usb_ak820.c:100: static void endpoints_reset(void) {
                                    797 ;	-----------------------------------------
                                    798 ;	 function endpoints_reset
                                    799 ;	-----------------------------------------
      005456                        800 _endpoints_reset:
                                    801 ;	tmk_core/protocol/ch555/usb_ak820.c:103: D0_EP_MOD = bUX_DEV_EN;
      005456 90 22 0C         [24]  802 	mov	dptr,#0x220c
      005459 74 01            [12]  803 	mov	a,#0x01
      00545B F0               [24]  804 	movx	@dptr,a
                                    805 ;	tmk_core/protocol/ch555/usb_ak820.c:104: D0_EP1RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
      00545C F5 82            [12]  806 	mov	dpl,a
      00545E 74 12            [12]  807 	mov	a,#0x12
      005460 F0               [24]  808 	movx	@dptr,a
                                    809 ;	tmk_core/protocol/ch555/usb_ak820.c:105: D0_EP2RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
      005461 A3               [24]  810 	inc	dptr
      005462 F0               [24]  811 	movx	@dptr,a
                                    812 ;	tmk_core/protocol/ch555/usb_ak820.c:106: D0_EP3RES = bUEP_X_AUTO_TOG | UEP_X_RES_NAK;
      005463 A3               [24]  813 	inc	dptr
      005464 F0               [24]  814 	movx	@dptr,a
                                    815 ;	tmk_core/protocol/ch555/usb_ak820.c:107: D0_EP1T_L = D0_EP2T_L = D0_EP3T_L = 0;
      005465 90 22 0B         [24]  816 	mov	dptr,#0x220b
      005468 E4               [12]  817 	clr	a
      005469 F0               [24]  818 	movx	@dptr,a
      00546A 15 82            [12]  819 	dec	dpl
      00546C F0               [24]  820 	movx	@dptr,a
      00546D 15 82            [12]  821 	dec	dpl
      00546F F0               [24]  822 	movx	@dptr,a
                                    823 ;	tmk_core/protocol/ch555/usb_ak820.c:108: for (i = 0; i < SNAPSHOT_SIZE; ++i) input_snapshot[i] = 0;
      005470 FF               [12]  824 	mov	r7,a
      005471                        825 00103$:
      005471 EF               [12]  826 	mov	a,r7
      005472 24 B7            [12]  827 	add	a, #_input_snapshot
      005474 F5 82            [12]  828 	mov	dpl,a
      005476 E4               [12]  829 	clr	a
      005477 34 06            [12]  830 	addc	a, #(_input_snapshot >> 8)
      005479 F5 83            [12]  831 	mov	dph,a
      00547B E4               [12]  832 	clr	a
      00547C F0               [24]  833 	movx	@dptr,a
      00547D 0F               [12]  834 	inc	r7
      00547E BF 2E 00         [24]  835 	cjne	r7,#0x2e,00139$
      005481                        836 00139$:
      005481 40 EE            [24]  837 	jc	00103$
                                    838 ;	tmk_core/protocol/ch555/usb_ak820.c:109: input_snapshot[SNAPSHOT_NKRO] = REPORT_ID_NKRO;
      005483 90 06 BF         [24]  839 	mov	dptr,#(_input_snapshot + 0x0008)
      005486 74 06            [12]  840 	mov	a,#0x06
      005488 F0               [24]  841 	movx	@dptr,a
                                    842 ;	tmk_core/protocol/ch555/usb_ak820.c:113: input_snapshot[SNAPSHOT_SYSTEM] = REPORT_ID_SYSTEM;
      005489 90 06 DF         [24]  843 	mov	dptr,#(_input_snapshot + 0x0028)
      00548C 03               [12]  844 	rr	a
      00548D F0               [24]  845 	movx	@dptr,a
                                    846 ;	tmk_core/protocol/ch555/usb_ak820.c:114: input_snapshot[SNAPSHOT_CONSUMER] = REPORT_ID_CONSUMER;
      00548E 90 06 E2         [24]  847 	mov	dptr,#(_input_snapshot + 0x002b)
      005491 04               [12]  848 	inc	a
      005492 F0               [24]  849 	movx	@dptr,a
                                    850 ;	tmk_core/protocol/ch555/usb_ak820.c:115: for (i = 0; i < RAW_EPSIZE; ++i) pUSB_BUF_DEV0[UX_EP3_ADDR + i] = 0;
      005493 7F 00            [12]  851 	mov	r7,#0x00
      005495                        852 00105$:
      005495 8F 06            [24]  853 	mov	ar6,r7
      005497 74 C0            [12]  854 	mov	a,#0xc0
      005499 2E               [12]  855 	add	a, r6
      00549A F5 82            [12]  856 	mov	dpl,a
      00549C 74 10            [12]  857 	mov	a,#0x10
      00549E 24 00            [12]  858 	add	a, #0x00
      0054A0 F5 83            [12]  859 	mov	dph,a
      0054A2 E4               [12]  860 	clr	a
      0054A3 F0               [24]  861 	movx	@dptr,a
      0054A4 0F               [12]  862 	inc	r7
      0054A5 BF 20 00         [24]  863 	cjne	r7,#0x20,00141$
      0054A8                        864 00141$:
      0054A8 40 EB            [24]  865 	jc	00105$
                                    866 ;	tmk_core/protocol/ch555/usb_ak820.c:116: raw_abort();
                                    867 ;	tmk_core/protocol/ch555/usb_ak820.c:117: }
      0054AA 02 54 00         [24]  868 	ljmp	_raw_abort
                                    869 ;------------------------------------------------------------
                                    870 ;Allocation info for local variables in function 'control_stall'
                                    871 ;------------------------------------------------------------
                                    872 ;	tmk_core/protocol/ch555/usb_ak820.c:119: static void control_stall(void) {
                                    873 ;	-----------------------------------------
                                    874 ;	 function control_stall
                                    875 ;	-----------------------------------------
      0054AD                        876 _control_stall:
                                    877 ;	tmk_core/protocol/ch555/usb_ak820.c:120: if (raw_state == RAW_RX) raw_state = RAW_IDLE;
      0054AD 90 06 94         [24]  878 	mov	dptr,#_raw_state
      0054B0 E0               [24]  879 	movx	a,@dptr
      0054B1 FF               [12]  880 	mov	r7,a
      0054B2 BF 01 05         [24]  881 	cjne	r7,#0x01,00102$
      0054B5 90 06 94         [24]  882 	mov	dptr,#_raw_state
      0054B8 E4               [12]  883 	clr	a
      0054B9 F0               [24]  884 	movx	@dptr,a
      0054BA                        885 00102$:
                                    886 ;	tmk_core/protocol/ch555/usb_ak820.c:121: output_kind = OUTPUT_NONE;
      0054BA 90 06 E6         [24]  887 	mov	dptr,#_output_kind
      0054BD E4               [12]  888 	clr	a
      0054BE F0               [24]  889 	movx	@dptr,a
                                    890 ;	tmk_core/protocol/ch555/usb_ak820.c:122: control_phase = CTRL_IDLE;
      0054BF 90 06 E5         [24]  891 	mov	dptr,#_control_phase
      0054C2 F0               [24]  892 	movx	@dptr,a
                                    893 ;	tmk_core/protocol/ch555/usb_ak820.c:123: D0SetupReqCode = 0xff;
      0054C3 90 06 86         [24]  894 	mov	dptr,#_D0SetupReqCode
      0054C6 14               [12]  895 	dec	a
      0054C7 F0               [24]  896 	movx	@dptr,a
                                    897 ;	tmk_core/protocol/ch555/usb_ak820.c:125: D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_STALL | UEP_T_RES_STALL;
      0054C8 90 22 00         [24]  898 	mov	dptr,#0x2200
      0054CB 74 CF            [12]  899 	mov	a,#0xcf
      0054CD F0               [24]  900 	movx	@dptr,a
                                    901 ;	tmk_core/protocol/ch555/usb_ak820.c:126: }
      0054CE 22               [24]  902 	ret
                                    903 ;------------------------------------------------------------
                                    904 ;Allocation info for local variables in function 'control_next'
                                    905 ;------------------------------------------------------------
                                    906 ;i             Allocated with name '_control_next_i_10000_262'
                                    907 ;length        Allocated with name '_control_next_length_10000_262'
                                    908 ;------------------------------------------------------------
                                    909 ;	tmk_core/protocol/ch555/usb_ak820.c:128: static void control_next(void) {
                                    910 ;	-----------------------------------------
                                    911 ;	 function control_next
                                    912 ;	-----------------------------------------
      0054CF                        913 _control_next:
                                    914 ;	tmk_core/protocol/ch555/usb_ak820.c:130: uint8_t length = D0SetupLen > DEF_ENDP0_SIZE ? DEF_ENDP0_SIZE : D0SetupLen;
      0054CF 90 06 87         [24]  915 	mov	dptr,#_D0SetupLen
      0054D2 E0               [24]  916 	movx	a,@dptr
      0054D3 FE               [12]  917 	mov	r6,a
      0054D4 A3               [24]  918 	inc	dptr
      0054D5 E0               [24]  919 	movx	a,@dptr
      0054D6 FF               [12]  920 	mov	r7,a
      0054D7 C3               [12]  921 	clr	c
      0054D8 74 40            [12]  922 	mov	a,#0x40
      0054DA 9E               [12]  923 	subb	a,r6
      0054DB E4               [12]  924 	clr	a
      0054DC 9F               [12]  925 	subb	a,r7
      0054DD 50 04            [24]  926 	jnc	00109$
                                    927 ;	free result
      0054DF 7E 40            [12]  928 	mov	r6,#0x40
      0054E1 80 07            [24]  929 	sjmp	00110$
      0054E3                        930 00109$:
      0054E3 90 06 87         [24]  931 	mov	dptr,#_D0SetupLen
      0054E6 E0               [24]  932 	movx	a,@dptr
      0054E7 FE               [12]  933 	mov	r6,a
      0054E8 A3               [24]  934 	inc	dptr
      0054E9 E0               [24]  935 	movx	a,@dptr
      0054EA                        936 00110$:
                                    937 ;	tmk_core/protocol/ch555/usb_ak820.c:131: for (i = 0; i < length; ++i) pD0_EP0_BUF[i] = *control_pointer++;
      0054EA 7F 00            [12]  938 	mov	r7,#0x00
      0054EC                        939 00105$:
      0054EC C3               [12]  940 	clr	c
      0054ED EF               [12]  941 	mov	a,r7
      0054EE 9E               [12]  942 	subb	a,r6
      0054EF 50 2A            [24]  943 	jnc	00101$
      0054F1 8F 04            [24]  944 	mov	ar4,r7
      0054F3 74 10            [12]  945 	mov	a,#0x10
      0054F5 24 00            [12]  946 	add	a, #0x00
      0054F7 FD               [12]  947 	mov	r5,a
      0054F8 90 06 E9         [24]  948 	mov	dptr,#_control_pointer
      0054FB E0               [24]  949 	movx	a,@dptr
      0054FC FA               [12]  950 	mov	r2,a
      0054FD A3               [24]  951 	inc	dptr
      0054FE E0               [24]  952 	movx	a,@dptr
      0054FF FB               [12]  953 	mov	r3,a
      005500 8A 82            [24]  954 	mov	dpl,r2
      005502 8B 83            [24]  955 	mov	dph,r3
      005504 E4               [12]  956 	clr	a
      005505 93               [24]  957 	movc	a,@a+dptr
      005506 F9               [12]  958 	mov	r1,a
      005507 90 06 E9         [24]  959 	mov	dptr,#_control_pointer
      00550A 74 01            [12]  960 	mov	a,#0x01
      00550C 2A               [12]  961 	add	a, r2
      00550D F0               [24]  962 	movx	@dptr,a
      00550E E4               [12]  963 	clr	a
      00550F 3B               [12]  964 	addc	a, r3
      005510 A3               [24]  965 	inc	dptr
      005511 F0               [24]  966 	movx	@dptr,a
      005512 8C 82            [24]  967 	mov	dpl,r4
      005514 8D 83            [24]  968 	mov	dph,r5
      005516 E9               [12]  969 	mov	a,r1
      005517 F0               [24]  970 	movx	@dptr,a
      005518 0F               [12]  971 	inc	r7
      005519 80 D1            [24]  972 	sjmp	00105$
      00551B                        973 00101$:
                                    974 ;	tmk_core/protocol/ch555/usb_ak820.c:132: D0SetupLen -= length;
      00551B 8E 05            [24]  975 	mov	ar5,r6
      00551D 7F 00            [12]  976 	mov	r7,#0x00
      00551F 90 06 87         [24]  977 	mov	dptr,#_D0SetupLen
      005522 E0               [24]  978 	movx	a,@dptr
      005523 FB               [12]  979 	mov	r3,a
      005524 A3               [24]  980 	inc	dptr
      005525 E0               [24]  981 	movx	a,@dptr
      005526 FC               [12]  982 	mov	r4,a
      005527 EB               [12]  983 	mov	a,r3
      005528 C3               [12]  984 	clr	c
      005529 9D               [12]  985 	subb	a,r5
      00552A FB               [12]  986 	mov	r3,a
      00552B EC               [12]  987 	mov	a,r4
      00552C 9F               [12]  988 	subb	a,r7
      00552D FC               [12]  989 	mov	r4,a
      00552E 90 06 87         [24]  990 	mov	dptr,#_D0SetupLen
      005531 EB               [12]  991 	mov	a,r3
      005532 F0               [24]  992 	movx	@dptr,a
      005533 EC               [12]  993 	mov	a,r4
      005534 A3               [24]  994 	inc	dptr
      005535 F0               [24]  995 	movx	@dptr,a
                                    996 ;	tmk_core/protocol/ch555/usb_ak820.c:133: if (!length) control_zlp = 0;
      005536 EE               [12]  997 	mov	a,r6
      005537 70 05            [24]  998 	jnz	00103$
      005539 90 06 E8         [24]  999 	mov	dptr,#_control_zlp
      00553C E4               [12] 1000 	clr	a
      00553D F0               [24] 1001 	movx	@dptr,a
      00553E                       1002 00103$:
                                   1003 ;	tmk_core/protocol/ch555/usb_ak820.c:134: D0_EP0T_L = length;
      00553E 90 22 08         [24] 1004 	mov	dptr,#0x2208
      005541 EE               [12] 1005 	mov	a,r6
      005542 F0               [24] 1006 	movx	@dptr,a
                                   1007 ;	tmk_core/protocol/ch555/usb_ak820.c:135: D0_EP0RES = (D0_EP0RES & (bUEP_T_TOG | bUEP_R_TOG)) | UEP_T_RES_ACK | UEP_R_RES_ACK;
      005543 90 22 00         [24] 1008 	mov	dptr,#0x2200
      005546 E0               [24] 1009 	movx	a,@dptr
      005547 54 C0            [12] 1010 	anl	a,#0xc0
      005549 F0               [24] 1011 	movx	@dptr,a
                                   1012 ;	tmk_core/protocol/ch555/usb_ak820.c:136: }
      00554A 22               [24] 1013 	ret
                                   1014 ;------------------------------------------------------------
                                   1015 ;Allocation info for local variables in function 'descriptor_select'
                                   1016 ;------------------------------------------------------------
                                   1017 ;index         Allocated with name '_descriptor_select_PARM_2'
                                   1018 ;interface     Allocated with name '_descriptor_select_PARM_3'
                                   1019 ;type          Allocated with name '_descriptor_select_type_10000_265'
                                   1020 ;------------------------------------------------------------
                                   1021 ;	tmk_core/protocol/ch555/usb_ak820.c:139: static uint16_t descriptor_select(uint8_t type, uint8_t index, uint16_t interface) {
                                   1022 ;	-----------------------------------------
                                   1023 ;	 function descriptor_select
                                   1024 ;	-----------------------------------------
      00554B                       1025 _descriptor_select:
      00554B E5 82            [12] 1026 	mov	a,dpl
      00554D 90 06 EE         [24] 1027 	mov	dptr,#_descriptor_select_type_10000_265
      005550 F0               [24] 1028 	movx	@dptr,a
                                   1029 ;	tmk_core/protocol/ch555/usb_ak820.c:140: if (type == USB_DESCR_TYP_DEVICE && !index && !interface) {
      005551 E0               [24] 1030 	movx	a,@dptr
      005552 FF               [12] 1031 	mov	r7,a
      005553 BF 01 20         [24] 1032 	cjne	r7,#0x01,00102$
      005556 90 06 EB         [24] 1033 	mov	dptr,#_descriptor_select_PARM_2
      005559 E0               [24] 1034 	movx	a,@dptr
      00555A 70 1A            [24] 1035 	jnz	00102$
      00555C 90 06 EC         [24] 1036 	mov	dptr,#_descriptor_select_PARM_3
      00555F E0               [24] 1037 	movx	a,@dptr
      005560 F5 F0            [12] 1038 	mov	b,a
      005562 A3               [24] 1039 	inc	dptr
      005563 E0               [24] 1040 	movx	a,@dptr
      005564 45 F0            [12] 1041 	orl	a,b
      005566 70 0E            [24] 1042 	jnz	00102$
                                   1043 ;	tmk_core/protocol/ch555/usb_ak820.c:141: control_pointer = (const uint8_t __code *)&DeviceDescriptor;
      005568 90 06 E9         [24] 1044 	mov	dptr,#_control_pointer
      00556B 74 B0            [12] 1045 	mov	a,#_DeviceDescriptor
      00556D F0               [24] 1046 	movx	@dptr,a
      00556E 74 BC            [12] 1047 	mov	a,#(_DeviceDescriptor >> 8)
      005570 A3               [24] 1048 	inc	dptr
      005571 F0               [24] 1049 	movx	@dptr,a
                                   1050 ;	tmk_core/protocol/ch555/usb_ak820.c:142: return sizeof(DeviceDescriptor);
      005572 90 00 12         [24] 1051 	mov	dptr,#0x0012
      005575 22               [24] 1052 	ret
      005576                       1053 00102$:
                                   1054 ;	tmk_core/protocol/ch555/usb_ak820.c:144: if (type == USB_DESCR_TYP_CONFIG && !index && !interface) {
      005576 90 06 EE         [24] 1055 	mov	dptr,#_descriptor_select_type_10000_265
      005579 E0               [24] 1056 	movx	a,@dptr
      00557A FF               [12] 1057 	mov	r7,a
      00557B BF 02 20         [24] 1058 	cjne	r7,#0x02,00106$
      00557E 90 06 EB         [24] 1059 	mov	dptr,#_descriptor_select_PARM_2
      005581 E0               [24] 1060 	movx	a,@dptr
      005582 70 1A            [24] 1061 	jnz	00106$
      005584 90 06 EC         [24] 1062 	mov	dptr,#_descriptor_select_PARM_3
      005587 E0               [24] 1063 	movx	a,@dptr
      005588 F5 F0            [12] 1064 	mov	b,a
      00558A A3               [24] 1065 	inc	dptr
      00558B E0               [24] 1066 	movx	a,@dptr
      00558C 45 F0            [12] 1067 	orl	a,b
      00558E 70 0E            [24] 1068 	jnz	00106$
                                   1069 ;	tmk_core/protocol/ch555/usb_ak820.c:145: control_pointer = (const uint8_t __code *)&ConfigurationDescriptor;
      005590 90 06 E9         [24] 1070 	mov	dptr,#_control_pointer
      005593 74 C2            [12] 1071 	mov	a,#_ConfigurationDescriptor
      005595 F0               [24] 1072 	movx	@dptr,a
      005596 74 BC            [12] 1073 	mov	a,#(_ConfigurationDescriptor >> 8)
      005598 A3               [24] 1074 	inc	dptr
      005599 F0               [24] 1075 	movx	@dptr,a
                                   1076 ;	tmk_core/protocol/ch555/usb_ak820.c:146: return sizeof(ConfigurationDescriptor);
      00559A 90 00 54         [24] 1077 	mov	dptr,#0x0054
      00559D 22               [24] 1078 	ret
      00559E                       1079 00106$:
                                   1080 ;	tmk_core/protocol/ch555/usb_ak820.c:148: if (type == USB_DESCR_TYP_STRING) {
      00559E 90 06 EE         [24] 1081 	mov	dptr,#_descriptor_select_type_10000_265
      0055A1 E0               [24] 1082 	movx	a,@dptr
      0055A2 FF               [12] 1083 	mov	r7,a
      0055A3 BF 03 02         [24] 1084 	cjne	r7,#0x03,00278$
      0055A6 80 03            [24] 1085 	sjmp	00279$
      0055A8                       1086 00278$:
      0055A8 02 56 42         [24] 1087 	ljmp	00119$
      0055AB                       1088 00279$:
                                   1089 ;	tmk_core/protocol/ch555/usb_ak820.c:149: if (interface != 0 && interface != 0x0409) return 0;
      0055AB 90 06 EC         [24] 1090 	mov	dptr,#_descriptor_select_PARM_3
      0055AE E0               [24] 1091 	movx	a,@dptr
      0055AF FD               [12] 1092 	mov	r5,a
      0055B0 A3               [24] 1093 	inc	dptr
      0055B1 E0               [24] 1094 	movx	a,@dptr
      0055B2 FE               [12] 1095 	mov	r6,a
      0055B3 90 06 EC         [24] 1096 	mov	dptr,#_descriptor_select_PARM_3
      0055B6 E0               [24] 1097 	movx	a,@dptr
      0055B7 F5 F0            [12] 1098 	mov	b,a
      0055B9 A3               [24] 1099 	inc	dptr
      0055BA E0               [24] 1100 	movx	a,@dptr
      0055BB 45 F0            [12] 1101 	orl	a,b
      0055BD 60 0C            [24] 1102 	jz	00110$
      0055BF BD 09 05         [24] 1103 	cjne	r5,#0x09,00281$
      0055C2 BE 04 02         [24] 1104 	cjne	r6,#0x04,00281$
      0055C5 80 04            [24] 1105 	sjmp	00110$
      0055C7                       1106 00281$:
      0055C7 90 00 00         [24] 1107 	mov	dptr,#0x0000
      0055CA 22               [24] 1108 	ret
      0055CB                       1109 00110$:
                                   1110 ;	tmk_core/protocol/ch555/usb_ak820.c:150: switch (index) {
      0055CB 90 06 EB         [24] 1111 	mov	dptr,#_descriptor_select_PARM_2
      0055CE E0               [24] 1112 	movx	a,@dptr
      0055CF FE               [12] 1113 	mov  r6,a
      0055D0 24 FC            [12] 1114 	add	a,#0xff - 0x03
      0055D2 40 6A            [24] 1115 	jc	00116$
                                   1116 ;	free result
      0055D4 EE               [12] 1117 	mov	a,r6
      0055D5 2E               [12] 1118 	add	a,r6
                                   1119 ;	tmk_core/protocol/ch555/usb_ak820.c:151: case 0: control_pointer = (const uint8_t __code *)&LanguageString; return LanguageString.Header.Size;
      0055D6 90 55 DA         [24] 1120 	mov	dptr,#00283$
      0055D9 73               [24] 1121 	jmp	@a+dptr
      0055DA                       1122 00283$:
      0055DA 80 06            [24] 1123 	sjmp	00112$
      0055DC 80 1B            [24] 1124 	sjmp	00113$
      0055DE 80 30            [24] 1125 	sjmp	00114$
      0055E0 80 45            [24] 1126 	sjmp	00115$
      0055E2                       1127 00112$:
      0055E2 90 06 E9         [24] 1128 	mov	dptr,#_control_pointer
      0055E5 74 16            [12] 1129 	mov	a,#_LanguageString
      0055E7 F0               [24] 1130 	movx	@dptr,a
      0055E8 74 BD            [12] 1131 	mov	a,#(_LanguageString >> 8)
      0055EA A3               [24] 1132 	inc	dptr
      0055EB F0               [24] 1133 	movx	@dptr,a
      0055EC 90 BD 16         [24] 1134 	mov	dptr,#_LanguageString
      0055EF E4               [12] 1135 	clr	a
      0055F0 93               [24] 1136 	movc	a,@a+dptr
      0055F1 FE               [12] 1137 	mov	r6,a
      0055F2 7D 00            [12] 1138 	mov	r5,#0x00
      0055F4 8E 82            [24] 1139 	mov	dpl, r6
      0055F6 8D 83            [24] 1140 	mov	dph, r5
      0055F8 22               [24] 1141 	ret
                                   1142 ;	tmk_core/protocol/ch555/usb_ak820.c:152: case 1: control_pointer = (const uint8_t __code *)&ManufacturerString; return ManufacturerString.Header.Size;
      0055F9                       1143 00113$:
      0055F9 90 06 E9         [24] 1144 	mov	dptr,#_control_pointer
      0055FC 74 1A            [12] 1145 	mov	a,#_ManufacturerString
      0055FE F0               [24] 1146 	movx	@dptr,a
      0055FF 74 BD            [12] 1147 	mov	a,#(_ManufacturerString >> 8)
      005601 A3               [24] 1148 	inc	dptr
      005602 F0               [24] 1149 	movx	@dptr,a
      005603 90 BD 1A         [24] 1150 	mov	dptr,#_ManufacturerString
      005606 E4               [12] 1151 	clr	a
      005607 93               [24] 1152 	movc	a,@a+dptr
      005608 FE               [12] 1153 	mov	r6,a
      005609 7D 00            [12] 1154 	mov	r5,#0x00
      00560B 8E 82            [24] 1155 	mov	dpl, r6
      00560D 8D 83            [24] 1156 	mov	dph, r5
      00560F 22               [24] 1157 	ret
                                   1158 ;	tmk_core/protocol/ch555/usb_ak820.c:153: case 2: control_pointer = (const uint8_t __code *)&ProductString; return ProductString.Header.Size;
      005610                       1159 00114$:
      005610 90 06 E9         [24] 1160 	mov	dptr,#_control_pointer
      005613 74 28            [12] 1161 	mov	a,#_ProductString
      005615 F0               [24] 1162 	movx	@dptr,a
      005616 74 BD            [12] 1163 	mov	a,#(_ProductString >> 8)
      005618 A3               [24] 1164 	inc	dptr
      005619 F0               [24] 1165 	movx	@dptr,a
      00561A 90 BD 28         [24] 1166 	mov	dptr,#_ProductString
      00561D E4               [12] 1167 	clr	a
      00561E 93               [24] 1168 	movc	a,@a+dptr
      00561F FE               [12] 1169 	mov	r6,a
      005620 7D 00            [12] 1170 	mov	r5,#0x00
      005622 8E 82            [24] 1171 	mov	dpl, r6
      005624 8D 83            [24] 1172 	mov	dph, r5
      005626 22               [24] 1173 	ret
                                   1174 ;	tmk_core/protocol/ch555/usb_ak820.c:155: case 3: control_pointer = (const uint8_t __code *)&SerialNumberString; return SerialNumberString.Header.Size;
      005627                       1175 00115$:
      005627 90 06 E9         [24] 1176 	mov	dptr,#_control_pointer
      00562A 74 60            [12] 1177 	mov	a,#_SerialNumberString
      00562C F0               [24] 1178 	movx	@dptr,a
      00562D 74 BD            [12] 1179 	mov	a,#(_SerialNumberString >> 8)
      00562F A3               [24] 1180 	inc	dptr
      005630 F0               [24] 1181 	movx	@dptr,a
      005631 90 BD 60         [24] 1182 	mov	dptr,#_SerialNumberString
      005634 E4               [12] 1183 	clr	a
      005635 93               [24] 1184 	movc	a,@a+dptr
      005636 FE               [12] 1185 	mov	r6,a
      005637 7D 00            [12] 1186 	mov	r5,#0x00
      005639 8E 82            [24] 1187 	mov	dpl, r6
      00563B 8D 83            [24] 1188 	mov	dph, r5
      00563D 22               [24] 1189 	ret
                                   1190 ;	tmk_core/protocol/ch555/usb_ak820.c:157: default: return 0;
      00563E                       1191 00116$:
      00563E 90 00 00         [24] 1192 	mov	dptr,#0x0000
      005641 22               [24] 1193 	ret
                                   1194 ;	tmk_core/protocol/ch555/usb_ak820.c:158: }
      005642                       1195 00119$:
                                   1196 ;	tmk_core/protocol/ch555/usb_ak820.c:160: if (index || interface >= TOTAL_INTERFACES) return 0;
      005642 90 06 EB         [24] 1197 	mov	dptr,#_descriptor_select_PARM_2
      005645 E0               [24] 1198 	movx	a,@dptr
      005646 70 11            [24] 1199 	jnz	00120$
      005648 90 06 EC         [24] 1200 	mov	dptr,#_descriptor_select_PARM_3
      00564B E0               [24] 1201 	movx	a,@dptr
      00564C FD               [12] 1202 	mov	r5,a
      00564D A3               [24] 1203 	inc	dptr
      00564E E0               [24] 1204 	movx	a,@dptr
      00564F FE               [12] 1205 	mov	r6,a
      005650 C3               [12] 1206 	clr	c
      005651 ED               [12] 1207 	mov	a,r5
      005652 94 03            [12] 1208 	subb	a,#0x03
      005654 EE               [12] 1209 	mov	a,r6
      005655 94 00            [12] 1210 	subb	a,#0x00
      005657 40 04            [24] 1211 	jc	00121$
      005659                       1212 00120$:
      005659 90 00 00         [24] 1213 	mov	dptr,#0x0000
      00565C 22               [24] 1214 	ret
      00565D                       1215 00121$:
                                   1216 ;	tmk_core/protocol/ch555/usb_ak820.c:161: if (type == USB_DESCR_TYP_REPORT) {
      00565D BF 22 60         [24] 1217 	cjne	r7,#0x22,00128$
                                   1218 ;	tmk_core/protocol/ch555/usb_ak820.c:162: switch (interface) {
      005660 8D 07            [24] 1219 	mov	ar7,r5
      005662 EF               [12] 1220 	mov	a,r7
      005663 60 10            [24] 1221 	jz	00123$
      005665 BD 01 05         [24] 1222 	cjne	r5,#0x01,00289$
      005668 BE 00 02         [24] 1223 	cjne	r6,#0x00,00289$
      00566B 80 21            [24] 1224 	sjmp	00124$
      00566D                       1225 00289$:
                                   1226 ;	tmk_core/protocol/ch555/usb_ak820.c:163: case KEYBOARD_INTERFACE:
      00566D BD 02 50         [24] 1227 	cjne	r5,#0x02,00128$
      005670 BE 00 4D         [24] 1228 	cjne	r6,#0x00,00128$
      005673 80 32            [24] 1229 	sjmp	00125$
      005675                       1230 00123$:
                                   1231 ;	tmk_core/protocol/ch555/usb_ak820.c:164: control_pointer = (const uint8_t __code *)KeyboardReport;
      005675 90 06 E9         [24] 1232 	mov	dptr,#_control_pointer
      005678 74 D4            [12] 1233 	mov	a,#_KeyboardReport
      00567A F0               [24] 1234 	movx	@dptr,a
      00567B 74 BB            [12] 1235 	mov	a,#(_KeyboardReport >> 8)
      00567D A3               [24] 1236 	inc	dptr
      00567E F0               [24] 1237 	movx	@dptr,a
                                   1238 ;	tmk_core/protocol/ch555/usb_ak820.c:165: return ConfigurationDescriptor.Keyboard_HID.HIDReportLength;
      00567F 90 BC DB         [24] 1239 	mov	dptr,#(_ConfigurationDescriptor + 0x0019)
      005682 E4               [12] 1240 	clr	a
      005683 93               [24] 1241 	movc	a,@a+dptr
      005684 FC               [12] 1242 	mov	r4,a
      005685 A3               [24] 1243 	inc	dptr
      005686 E4               [12] 1244 	clr	a
      005687 93               [24] 1245 	movc	a,@a+dptr
      005688 FF               [12] 1246 	mov	r7,a
      005689 8C 82            [24] 1247 	mov	dpl, r4
      00568B 8F 83            [24] 1248 	mov	dph, r7
      00568D 22               [24] 1249 	ret
                                   1250 ;	tmk_core/protocol/ch555/usb_ak820.c:166: case RAW_INTERFACE:
      00568E                       1251 00124$:
                                   1252 ;	tmk_core/protocol/ch555/usb_ak820.c:167: control_pointer = (const uint8_t __code *)RawReport;
      00568E 90 06 E9         [24] 1253 	mov	dptr,#_control_pointer
      005691 74 87            [12] 1254 	mov	a,#_RawReport
      005693 F0               [24] 1255 	movx	@dptr,a
      005694 74 BC            [12] 1256 	mov	a,#(_RawReport >> 8)
      005696 A3               [24] 1257 	inc	dptr
      005697 F0               [24] 1258 	movx	@dptr,a
                                   1259 ;	tmk_core/protocol/ch555/usb_ak820.c:168: return ConfigurationDescriptor.Raw_HID.HIDReportLength;
      005698 90 BC F4         [24] 1260 	mov	dptr,#(_ConfigurationDescriptor + 0x0032)
      00569B E4               [12] 1261 	clr	a
      00569C 93               [24] 1262 	movc	a,@a+dptr
      00569D FC               [12] 1263 	mov	r4,a
      00569E A3               [24] 1264 	inc	dptr
      00569F E4               [12] 1265 	clr	a
      0056A0 93               [24] 1266 	movc	a,@a+dptr
      0056A1 FF               [12] 1267 	mov	r7,a
      0056A2 8C 82            [24] 1268 	mov	dpl, r4
      0056A4 8F 83            [24] 1269 	mov	dph, r7
      0056A6 22               [24] 1270 	ret
                                   1271 ;	tmk_core/protocol/ch555/usb_ak820.c:170: case SHARED_INTERFACE:
      0056A7                       1272 00125$:
                                   1273 ;	tmk_core/protocol/ch555/usb_ak820.c:171: control_pointer = (const uint8_t __code *)SharedReport;
      0056A7 90 06 E9         [24] 1274 	mov	dptr,#_control_pointer
      0056AA 74 19            [12] 1275 	mov	a,#_SharedReport
      0056AC F0               [24] 1276 	movx	@dptr,a
      0056AD 74 BC            [12] 1277 	mov	a,#(_SharedReport >> 8)
      0056AF A3               [24] 1278 	inc	dptr
      0056B0 F0               [24] 1279 	movx	@dptr,a
                                   1280 ;	tmk_core/protocol/ch555/usb_ak820.c:172: return ConfigurationDescriptor.Shared_HID.HIDReportLength;
      0056B1 90 BD 0D         [24] 1281 	mov	dptr,#(_ConfigurationDescriptor + 0x004b)
      0056B4 E4               [12] 1282 	clr	a
      0056B5 93               [24] 1283 	movc	a,@a+dptr
      0056B6 FC               [12] 1284 	mov	r4,a
      0056B7 A3               [24] 1285 	inc	dptr
      0056B8 E4               [12] 1286 	clr	a
      0056B9 93               [24] 1287 	movc	a,@a+dptr
      0056BA FF               [12] 1288 	mov	r7,a
      0056BB 8C 82            [24] 1289 	mov	dpl, r4
      0056BD 8F 83            [24] 1290 	mov	dph, r7
                                   1291 ;	tmk_core/protocol/ch555/usb_ak820.c:174: }
      0056BF 22               [24] 1292 	ret
      0056C0                       1293 00128$:
                                   1294 ;	tmk_core/protocol/ch555/usb_ak820.c:176: if (type == USB_DESCR_TYP_HID) {
      0056C0 90 06 EE         [24] 1295 	mov	dptr,#_descriptor_select_type_10000_265
      0056C3 E0               [24] 1296 	movx	a,@dptr
      0056C4 FF               [12] 1297 	mov	r7,a
      0056C5 BF 21 48         [24] 1298 	cjne	r7,#0x21,00134$
                                   1299 ;	tmk_core/protocol/ch555/usb_ak820.c:177: switch (interface) {
      0056C8 8D 07            [24] 1300 	mov	ar7,r5
      0056CA EF               [12] 1301 	mov	a,r7
      0056CB 60 10            [24] 1302 	jz	00129$
      0056CD BD 01 05         [24] 1303 	cjne	r5,#0x01,00294$
      0056D0 BE 00 02         [24] 1304 	cjne	r6,#0x00,00294$
      0056D3 80 19            [24] 1305 	sjmp	00130$
      0056D5                       1306 00294$:
                                   1307 ;	tmk_core/protocol/ch555/usb_ak820.c:178: case KEYBOARD_INTERFACE: control_pointer = (const uint8_t __code *)&ConfigurationDescriptor.Keyboard_HID; return 9;
      0056D5 BD 02 38         [24] 1308 	cjne	r5,#0x02,00134$
      0056D8 BE 00 35         [24] 1309 	cjne	r6,#0x00,00134$
      0056DB 80 22            [24] 1310 	sjmp	00131$
      0056DD                       1311 00129$:
      0056DD 90 06 E9         [24] 1312 	mov	dptr,#_control_pointer
      0056E0 74 12            [12] 1313 	mov	a,#0x12
      0056E2 24 C2            [12] 1314 	add	a, #_ConfigurationDescriptor
      0056E4 F0               [24] 1315 	movx	@dptr,a
      0056E5 E4               [12] 1316 	clr	a
      0056E6 34 BC            [12] 1317 	addc	a, #(_ConfigurationDescriptor >> 8)
      0056E8 A3               [24] 1318 	inc	dptr
      0056E9 F0               [24] 1319 	movx	@dptr,a
      0056EA 90 00 09         [24] 1320 	mov	dptr,#0x0009
                                   1321 ;	tmk_core/protocol/ch555/usb_ak820.c:179: case RAW_INTERFACE: control_pointer = (const uint8_t __code *)&ConfigurationDescriptor.Raw_HID; return 9;
      0056ED 22               [24] 1322 	ret
      0056EE                       1323 00130$:
      0056EE 90 06 E9         [24] 1324 	mov	dptr,#_control_pointer
      0056F1 74 2B            [12] 1325 	mov	a,#0x2b
      0056F3 24 C2            [12] 1326 	add	a, #_ConfigurationDescriptor
      0056F5 F0               [24] 1327 	movx	@dptr,a
      0056F6 E4               [12] 1328 	clr	a
      0056F7 34 BC            [12] 1329 	addc	a, #(_ConfigurationDescriptor >> 8)
      0056F9 A3               [24] 1330 	inc	dptr
      0056FA F0               [24] 1331 	movx	@dptr,a
      0056FB 90 00 09         [24] 1332 	mov	dptr,#0x0009
                                   1333 ;	tmk_core/protocol/ch555/usb_ak820.c:181: case SHARED_INTERFACE: control_pointer = (const uint8_t __code *)&ConfigurationDescriptor.Shared_HID; return 9;
      0056FE 22               [24] 1334 	ret
      0056FF                       1335 00131$:
      0056FF 90 06 E9         [24] 1336 	mov	dptr,#_control_pointer
      005702 74 44            [12] 1337 	mov	a,#0x44
      005704 24 C2            [12] 1338 	add	a, #_ConfigurationDescriptor
      005706 F0               [24] 1339 	movx	@dptr,a
      005707 E4               [12] 1340 	clr	a
      005708 34 BC            [12] 1341 	addc	a, #(_ConfigurationDescriptor >> 8)
      00570A A3               [24] 1342 	inc	dptr
      00570B F0               [24] 1343 	movx	@dptr,a
      00570C 90 00 09         [24] 1344 	mov	dptr,#0x0009
                                   1345 ;	tmk_core/protocol/ch555/usb_ak820.c:183: }
      00570F 22               [24] 1346 	ret
      005710                       1347 00134$:
                                   1348 ;	tmk_core/protocol/ch555/usb_ak820.c:185: return 0;
      005710 90 00 00         [24] 1349 	mov	dptr,#0x0000
                                   1350 ;	tmk_core/protocol/ch555/usb_ak820.c:186: }
      005713 22               [24] 1351 	ret
                                   1352 ;------------------------------------------------------------
                                   1353 ;Allocation info for local variables in function 'control_setup'
                                   1354 ;------------------------------------------------------------
                                   1355 ;sloc1         Allocated with name '_control_setup_sloc1_1_0'
                                   1356 ;sloc2         Allocated with name '_control_setup_sloc2_1_0'
                                   1357 ;sloc3         Allocated with name '_control_setup_sloc3_1_0'
                                   1358 ;type          Allocated with name '_control_setup_type_10000_286'
                                   1359 ;value         Allocated with name '_control_setup_value_10000_286'
                                   1360 ;index         Allocated with name '_control_setup_index_10000_286'
                                   1361 ;length        Allocated with name '_control_setup_length_10000_286'
                                   1362 ;endpoint      Allocated with name '_control_setup_endpoint_10000_286'
                                   1363 ;i             Allocated with name '_control_setup_i_10000_286'
                                   1364 ;offset        Allocated with name '_control_setup_offset_10000_286'
                                   1365 ;report_id     Allocated with name '_control_setup_report_id_10000_286'
                                   1366 ;------------------------------------------------------------
                                   1367 ;	tmk_core/protocol/ch555/usb_ak820.c:188: static void control_setup(void) {
                                   1368 ;	-----------------------------------------
                                   1369 ;	 function control_setup
                                   1370 ;	-----------------------------------------
      005714                       1371 _control_setup:
                                   1372 ;	tmk_core/protocol/ch555/usb_ak820.c:189: uint8_t type = pD0_SETUP_REQ->bRequestType;
      005714 90 10 00         [24] 1373 	mov	dptr,#0x1000
      005717 E0               [24] 1374 	movx	a,@dptr
      005718 FF               [12] 1375 	mov	r7,a
                                   1376 ;	tmk_core/protocol/ch555/usb_ak820.c:190: uint16_t value = pD0_SETUP_REQ->wValueL | ((uint16_t)pD0_SETUP_REQ->wValueH << 8);
      005719 A3               [24] 1377 	inc	dptr
      00571A A3               [24] 1378 	inc	dptr
      00571B E0               [24] 1379 	movx	a,@dptr
      00571C FE               [12] 1380 	mov	r6,a
      00571D A3               [24] 1381 	inc	dptr
      00571E E0               [24] 1382 	movx	a,@dptr
      00571F FC               [12] 1383 	mov	r4,a
      005720 7D 00            [12] 1384 	mov	r5,#0x00
      005722 8E 03            [24] 1385 	mov	ar3,r6
      005724 7E 00            [12] 1386 	mov	r6,#0x00
      005726 ED               [12] 1387 	mov	a,r5
      005727 4B               [12] 1388 	orl	a,r3
      005728 FD               [12] 1389 	mov	r5,a
      005729 EC               [12] 1390 	mov	a,r4
      00572A 4E               [12] 1391 	orl	a,r6
      00572B FE               [12] 1392 	mov	r6,a
                                   1393 ;	tmk_core/protocol/ch555/usb_ak820.c:191: uint16_t index = pD0_SETUP_REQ->wIndexL | ((uint16_t)pD0_SETUP_REQ->wIndexH << 8);
      00572C A3               [24] 1394 	inc	dptr
      00572D E0               [24] 1395 	movx	a,@dptr
      00572E FC               [12] 1396 	mov	r4,a
      00572F A3               [24] 1397 	inc	dptr
      005730 E0               [24] 1398 	movx	a,@dptr
      005731 FA               [12] 1399 	mov	r2,a
      005732 7B 00            [12] 1400 	mov	r3,#0x00
      005734 8C 01            [24] 1401 	mov	ar1,r4
      005736 7C 00            [12] 1402 	mov	r4,#0x00
      005738 EB               [12] 1403 	mov	a,r3
      005739 49               [12] 1404 	orl	a,r1
      00573A FB               [12] 1405 	mov	r3,a
      00573B EA               [12] 1406 	mov	a,r2
      00573C 4C               [12] 1407 	orl	a,r4
      00573D FC               [12] 1408 	mov	r4,a
                                   1409 ;	tmk_core/protocol/ch555/usb_ak820.c:195: uint8_t offset = 0;
      00573E 90 06 F1         [24] 1410 	mov	dptr,#_control_setup_offset_10000_286
      005741 E4               [12] 1411 	clr	a
      005742 F0               [24] 1412 	movx	@dptr,a
                                   1413 ;	tmk_core/protocol/ch555/usb_ak820.c:197: if (raw_state == RAW_RX) raw_state = RAW_IDLE; /* abort only unfinished OUT */
      005743 90 06 94         [24] 1414 	mov	dptr,#_raw_state
      005746 E0               [24] 1415 	movx	a,@dptr
      005747 FA               [12] 1416 	mov	r2,a
      005748 BA 01 05         [24] 1417 	cjne	r2,#0x01,00102$
      00574B 90 06 94         [24] 1418 	mov	dptr,#_raw_state
      00574E E4               [12] 1419 	clr	a
      00574F F0               [24] 1420 	movx	@dptr,a
      005750                       1421 00102$:
                                   1422 ;	tmk_core/protocol/ch555/usb_ak820.c:198: output_kind = OUTPUT_NONE;
      005750 C0 07            [24] 1423 	push	ar7
      005752 90 06 E6         [24] 1424 	mov	dptr,#_output_kind
      005755 E4               [12] 1425 	clr	a
      005756 F0               [24] 1426 	movx	@dptr,a
                                   1427 ;	tmk_core/protocol/ch555/usb_ak820.c:199: control_phase = CTRL_IDLE;
      005757 90 06 E5         [24] 1428 	mov	dptr,#_control_phase
      00575A F0               [24] 1429 	movx	@dptr,a
                                   1430 ;	tmk_core/protocol/ch555/usb_ak820.c:200: control_zlp = 0;
      00575B 90 06 E8         [24] 1431 	mov	dptr,#_control_zlp
      00575E F0               [24] 1432 	movx	@dptr,a
                                   1433 ;	tmk_core/protocol/ch555/usb_ak820.c:201: D0SetupReqCode = pD0_SETUP_REQ->bRequest;
      00575F 90 10 01         [24] 1434 	mov	dptr,#0x1001
      005762 E0               [24] 1435 	movx	a,@dptr
      005763 90 06 86         [24] 1436 	mov	dptr,#_D0SetupReqCode
      005766 F0               [24] 1437 	movx	@dptr,a
                                   1438 ;	tmk_core/protocol/ch555/usb_ak820.c:202: D0SetupLen = pD0_SETUP_REQ->wLengthL | ((uint16_t)pD0_SETUP_REQ->wLengthH << 8);
      005767 90 10 06         [24] 1439 	mov	dptr,#0x1006
      00576A E0               [24] 1440 	movx	a,@dptr
      00576B FA               [12] 1441 	mov	r2,a
      00576C A3               [24] 1442 	inc	dptr
      00576D E0               [24] 1443 	movx	a,@dptr
      00576E F9               [12] 1444 	mov	r1,a
      00576F 78 00            [12] 1445 	mov	r0,#0x00
      005771 7F 00            [12] 1446 	mov	r7,#0x00
      005773 90 06 87         [24] 1447 	mov	dptr,#_D0SetupLen
      005776 E8               [12] 1448 	mov	a,r0
      005777 4A               [12] 1449 	orl	a,r2
      005778 F0               [24] 1450 	movx	@dptr,a
      005779 E9               [12] 1451 	mov	a,r1
      00577A 4F               [12] 1452 	orl	a,r7
      00577B A3               [24] 1453 	inc	dptr
      00577C F0               [24] 1454 	movx	@dptr,a
                                   1455 ;	tmk_core/protocol/ch555/usb_ak820.c:203: D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_NAK;
      00577D 90 22 00         [24] 1456 	mov	dptr,#0x2200
      005780 74 C2            [12] 1457 	mov	a,#0xc2
      005782 F0               [24] 1458 	movx	@dptr,a
                                   1459 ;	tmk_core/protocol/ch555/usb_ak820.c:204: D0_EP0T_L = 0;
      005783 90 22 08         [24] 1460 	mov	dptr,#0x2208
      005786 E4               [12] 1461 	clr	a
      005787 F0               [24] 1462 	movx	@dptr,a
                                   1463 ;	tmk_core/protocol/ch555/usb_ak820.c:206: if (D0SetupReqCode == USB_GET_DESCRIPTOR && (type == 0x80 || type == 0x81)) {
      005788 90 06 86         [24] 1464 	mov	dptr,#_D0SetupReqCode
      00578B E0               [24] 1465 	movx	a,@dptr
      00578C FF               [12] 1466 	mov	r7,a
      00578D BF 06 02         [24] 1467 	cjne	r7,#0x06,01280$
      005790 80 05            [24] 1468 	sjmp	01281$
      005792                       1469 01280$:
      005792 D0 07            [24] 1470 	pop	ar7
      005794 02 58 50         [24] 1471 	ljmp	00112$
      005797                       1472 01281$:
      005797 D0 07            [24] 1473 	pop	ar7
      005799 BF 80 02         [24] 1474 	cjne	r7,#0x80,01282$
      00579C 80 08            [24] 1475 	sjmp	00111$
      00579E                       1476 01282$:
      00579E BF 81 02         [24] 1477 	cjne	r7,#0x81,01283$
      0057A1 80 03            [24] 1478 	sjmp	01284$
      0057A3                       1479 01283$:
      0057A3 02 58 50         [24] 1480 	ljmp	00112$
      0057A6                       1481 01284$:
      0057A6                       1482 00111$:
                                   1483 ;	tmk_core/protocol/ch555/usb_ak820.c:207: if (((value >> 8) == USB_DESCR_TYP_HID || (value >> 8) == USB_DESCR_TYP_REPORT) != (type == 0x81)) {
      0057A6 8E 01            [24] 1484 	mov	ar1,r6
      0057A8 B9 21 02         [24] 1485 	cjne	r1,#0x21,01285$
      0057AB 80 09            [24] 1486 	sjmp	00301$
      0057AD                       1487 01285$:
      0057AD B9 22 02         [24] 1488 	cjne	r1,#0x22,01286$
      0057B0 80 04            [24] 1489 	sjmp	00301$
      0057B2                       1490 01286$:
                                   1491 ;	assignBit
      0057B2 C2 09            [12] 1492 	clr	_control_setup_sloc0_1_0
      0057B4 80 02            [24] 1493 	sjmp	00302$
      0057B6                       1494 00301$:
                                   1495 ;	assignBit
      0057B6 D2 09            [12] 1496 	setb	_control_setup_sloc0_1_0
      0057B8                       1497 00302$:
      0057B8 E4               [12] 1498 	clr	a
      0057B9 BF 81 01         [24] 1499 	cjne	r7,#0x81,01287$
      0057BC 04               [12] 1500 	inc	a
      0057BD                       1501 01287$:
      0057BD FA               [12] 1502 	mov	r2,a
      0057BE A2 09            [12] 1503 	mov	c,_control_setup_sloc0_1_0
      0057C0 E4               [12] 1504 	clr	a
      0057C1 33               [12] 1505 	rlc	a
      0057C2 B5 02 02         [24] 1506 	cjne	a,ar2,01289$
      0057C5 80 03            [24] 1507 	sjmp	00104$
      0057C7                       1508 01289$:
                                   1509 ;	tmk_core/protocol/ch555/usb_ak820.c:208: control_stall(); return;
      0057C7 02 54 AD         [24] 1510 	ljmp	_control_stall
      0057CA                       1511 00104$:
                                   1512 ;	tmk_core/protocol/ch555/usb_ak820.c:210: length = descriptor_select(value >> 8, value, index);
      0057CA 8E 02            [24] 1513 	mov	ar2,r6
      0057CC 90 06 EB         [24] 1514 	mov	dptr,#_descriptor_select_PARM_2
      0057CF ED               [12] 1515 	mov	a,r5
      0057D0 F0               [24] 1516 	movx	@dptr,a
      0057D1 90 06 EC         [24] 1517 	mov	dptr,#_descriptor_select_PARM_3
      0057D4 EB               [12] 1518 	mov	a,r3
      0057D5 F0               [24] 1519 	movx	@dptr,a
      0057D6 EC               [12] 1520 	mov	a,r4
      0057D7 A3               [24] 1521 	inc	dptr
      0057D8 F0               [24] 1522 	movx	@dptr,a
      0057D9 8A 82            [24] 1523 	mov	dpl, r2
      0057DB 12 55 4B         [24] 1524 	lcall	_descriptor_select
      0057DE 85 82 24         [24] 1525 	mov	_control_setup_sloc1_1_0,dpl
      0057E1 85 83 25         [24] 1526 	mov	(_control_setup_sloc1_1_0 + 1),dph
                                   1527 ;	tmk_core/protocol/ch555/usb_ak820.c:211: if (!length) { control_stall(); return; }
      0057E4 E5 24            [12] 1528 	mov	a,_control_setup_sloc1_1_0
      0057E6 45 25            [12] 1529 	orl	a,(_control_setup_sloc1_1_0 + 1)
      0057E8 70 03            [24] 1530 	jnz	00106$
      0057EA 02 54 AD         [24] 1531 	ljmp	_control_stall
      0057ED                       1532 00106$:
                                   1533 ;	tmk_core/protocol/ch555/usb_ak820.c:212: control_zlp = length < D0SetupLen && !(length & (DEF_ENDP0_SIZE - 1));
      0057ED 90 06 87         [24] 1534 	mov	dptr,#_D0SetupLen
      0057F0 E0               [24] 1535 	movx	a,@dptr
      0057F1 F8               [12] 1536 	mov	r0,a
      0057F2 A3               [24] 1537 	inc	dptr
      0057F3 E0               [24] 1538 	movx	a,@dptr
      0057F4 FA               [12] 1539 	mov	r2,a
      0057F5 C3               [12] 1540 	clr	c
      0057F6 E5 24            [12] 1541 	mov	a,_control_setup_sloc1_1_0
      0057F8 98               [12] 1542 	subb	a,r0
      0057F9 E5 25            [12] 1543 	mov	a,(_control_setup_sloc1_1_0 + 1)
      0057FB 9A               [12] 1544 	subb	a,r2
      0057FC 50 06            [24] 1545 	jnc	00303$
      0057FE E5 24            [12] 1546 	mov	a,_control_setup_sloc1_1_0
      005800 54 3F            [12] 1547 	anl	a,#0x3f
      005802 60 04            [24] 1548 	jz	00304$
      005804                       1549 00303$:
                                   1550 ;	assignBit
      005804 C2 09            [12] 1551 	clr	_control_setup_sloc0_1_0
      005806 80 02            [24] 1552 	sjmp	00305$
      005808                       1553 00304$:
                                   1554 ;	assignBit
      005808 D2 09            [12] 1555 	setb	_control_setup_sloc0_1_0
      00580A                       1556 00305$:
      00580A 90 06 E8         [24] 1557 	mov	dptr,#_control_zlp
      00580D A2 09            [12] 1558 	mov	c,_control_setup_sloc0_1_0
      00580F E4               [12] 1559 	clr	a
      005810 33               [12] 1560 	rlc	a
      005811 F0               [24] 1561 	movx	@dptr,a
                                   1562 ;	tmk_core/protocol/ch555/usb_ak820.c:213: if (D0SetupLen > length) D0SetupLen = length;
      005812 90 06 87         [24] 1563 	mov	dptr,#_D0SetupLen
      005815 E0               [24] 1564 	movx	a,@dptr
      005816 F9               [12] 1565 	mov	r1,a
      005817 A3               [24] 1566 	inc	dptr
      005818 E0               [24] 1567 	movx	a,@dptr
      005819 FA               [12] 1568 	mov	r2,a
      00581A C3               [12] 1569 	clr	c
      00581B E5 24            [12] 1570 	mov	a,_control_setup_sloc1_1_0
      00581D 99               [12] 1571 	subb	a,r1
      00581E E5 25            [12] 1572 	mov	a,(_control_setup_sloc1_1_0 + 1)
      005820 9A               [12] 1573 	subb	a,r2
      005821 50 0A            [24] 1574 	jnc	00108$
                                   1575 ;	free result
      005823 90 06 87         [24] 1576 	mov	dptr,#_D0SetupLen
      005826 E5 24            [12] 1577 	mov	a,_control_setup_sloc1_1_0
      005828 F0               [24] 1578 	movx	@dptr,a
      005829 E5 25            [12] 1579 	mov	a,(_control_setup_sloc1_1_0 + 1)
      00582B A3               [24] 1580 	inc	dptr
      00582C F0               [24] 1581 	movx	@dptr,a
      00582D                       1582 00108$:
                                   1583 ;	tmk_core/protocol/ch555/usb_ak820.c:214: control_phase = D0SetupLen ? CTRL_DATA_IN : CTRL_STATUS_OUT;
      00582D 90 06 87         [24] 1584 	mov	dptr,#_D0SetupLen
      005830 E0               [24] 1585 	movx	a,@dptr
      005831 F9               [12] 1586 	mov	r1,a
      005832 A3               [24] 1587 	inc	dptr
      005833 E0               [24] 1588 	movx	a,@dptr
      005834 49               [12] 1589 	orl	a,r1
      005835 60 04            [24] 1590 	jz	00306$
      005837 7A 01            [12] 1591 	mov	r2,#0x01
      005839 80 02            [24] 1592 	sjmp	00307$
      00583B                       1593 00306$:
      00583B 7A 02            [12] 1594 	mov	r2,#0x02
      00583D                       1595 00307$:
      00583D 90 06 E5         [24] 1596 	mov	dptr,#_control_phase
      005840 EA               [12] 1597 	mov	a,r2
      005841 F0               [24] 1598 	movx	@dptr,a
                                   1599 ;	tmk_core/protocol/ch555/usb_ak820.c:215: if (D0SetupLen) control_next();
      005842 90 06 87         [24] 1600 	mov	dptr,#_D0SetupLen
      005845 E0               [24] 1601 	movx	a,@dptr
      005846 F9               [12] 1602 	mov	r1,a
      005847 A3               [24] 1603 	inc	dptr
      005848 E0               [24] 1604 	movx	a,@dptr
      005849 49               [12] 1605 	orl	a,r1
      00584A 60 03            [24] 1606 	jz	00110$
                                   1607 ;	tmk_core/protocol/ch555/usb_ak820.c:216: return;
      00584C 02 54 CF         [24] 1608 	ljmp	_control_next
      00584F                       1609 00110$:
      00584F 22               [24] 1610 	ret
      005850                       1611 00112$:
                                   1612 ;	tmk_core/protocol/ch555/usb_ak820.c:218: if (type == 0x00 && D0SetupReqCode == USB_SET_ADDRESS && !index && !D0SetupLen && value <= 127) {
      005850 EF               [12] 1613 	mov	a,r7
      005851 70 33            [24] 1614 	jnz	00286$
      005853 90 06 86         [24] 1615 	mov	dptr,#_D0SetupReqCode
      005856 E0               [24] 1616 	movx	a,@dptr
      005857 FA               [12] 1617 	mov	r2,a
      005858 BA 05 2B         [24] 1618 	cjne	r2,#0x05,00286$
      00585B EB               [12] 1619 	mov	a,r3
      00585C 4C               [12] 1620 	orl	a,r4
      00585D 70 27            [24] 1621 	jnz	00286$
      00585F 90 06 87         [24] 1622 	mov	dptr,#_D0SetupLen
      005862 E0               [24] 1623 	movx	a,@dptr
      005863 F9               [12] 1624 	mov	r1,a
      005864 A3               [24] 1625 	inc	dptr
      005865 E0               [24] 1626 	movx	a,@dptr
      005866 49               [12] 1627 	orl	a,r1
      005867 70 1D            [24] 1628 	jnz	00286$
      005869 8D 01            [24] 1629 	mov	ar1,r5
      00586B 8E 02            [24] 1630 	mov	ar2,r6
      00586D C3               [12] 1631 	clr	c
      00586E 74 7F            [12] 1632 	mov	a,#0x7f
      005870 99               [12] 1633 	subb	a,r1
      005871 E4               [12] 1634 	clr	a
      005872 9A               [12] 1635 	subb	a,r2
      005873 40 11            [24] 1636 	jc	00286$
                                   1637 ;	free result
                                   1638 ;	tmk_core/protocol/ch555/usb_ak820.c:219: D0SetupLen = value; /* applied after status-IN ACK */
      005875 90 06 87         [24] 1639 	mov	dptr,#_D0SetupLen
      005878 ED               [12] 1640 	mov	a,r5
      005879 F0               [24] 1641 	movx	@dptr,a
      00587A EE               [12] 1642 	mov	a,r6
      00587B A3               [24] 1643 	inc	dptr
      00587C F0               [24] 1644 	movx	@dptr,a
                                   1645 ;	tmk_core/protocol/ch555/usb_ak820.c:220: control_phase = CTRL_STATUS_IN;
      00587D 90 06 E5         [24] 1646 	mov	dptr,#_control_phase
      005880 74 03            [12] 1647 	mov	a,#0x03
      005882 F0               [24] 1648 	movx	@dptr,a
      005883 02 5F 18         [24] 1649 	ljmp	00287$
      005886                       1650 00286$:
                                   1651 ;	tmk_core/protocol/ch555/usb_ak820.c:221: } else if (type == 0x00 && D0SetupReqCode == USB_SET_CONFIGURATION && !index && !D0SetupLen && value <= 1) {
      005886 EF               [12] 1652 	mov	a,r7
      005887 70 4F            [24] 1653 	jnz	00279$
      005889 90 06 86         [24] 1654 	mov	dptr,#_D0SetupReqCode
      00588C E0               [24] 1655 	movx	a,@dptr
      00588D FA               [12] 1656 	mov	r2,a
      00588E BA 09 47         [24] 1657 	cjne	r2,#0x09,00279$
      005891 EB               [12] 1658 	mov	a,r3
      005892 4C               [12] 1659 	orl	a,r4
      005893 70 43            [24] 1660 	jnz	00279$
      005895 90 06 87         [24] 1661 	mov	dptr,#_D0SetupLen
      005898 E0               [24] 1662 	movx	a,@dptr
      005899 F9               [12] 1663 	mov	r1,a
      00589A A3               [24] 1664 	inc	dptr
      00589B E0               [24] 1665 	movx	a,@dptr
      00589C 49               [12] 1666 	orl	a,r1
      00589D 70 39            [24] 1667 	jnz	00279$
      00589F 8D 01            [24] 1668 	mov	ar1,r5
      0058A1 8E 02            [24] 1669 	mov	ar2,r6
      0058A3 C3               [12] 1670 	clr	c
      0058A4 74 01            [12] 1671 	mov	a,#0x01
      0058A6 99               [12] 1672 	subb	a,r1
      0058A7 E4               [12] 1673 	clr	a
      0058A8 9A               [12] 1674 	subb	a,r2
      0058A9 40 2D            [24] 1675 	jc	00279$
                                   1676 ;	free result
                                   1677 ;	tmk_core/protocol/ch555/usb_ak820.c:222: endpoints_reset();
      0058AB C0 06            [24] 1678 	push	ar6
      0058AD C0 05            [24] 1679 	push	ar5
      0058AF 12 54 56         [24] 1680 	lcall	_endpoints_reset
      0058B2 D0 05            [24] 1681 	pop	ar5
      0058B4 D0 06            [24] 1682 	pop	ar6
                                   1683 ;	tmk_core/protocol/ch555/usb_ak820.c:223: D0UsbConfig = value;
      0058B6 90 06 8C         [24] 1684 	mov	dptr,#_D0UsbConfig
      0058B9 ED               [12] 1685 	mov	a,r5
      0058BA F0               [24] 1686 	movx	@dptr,a
                                   1687 ;	tmk_core/protocol/ch555/usb_ak820.c:224: USB_EnumStatus = value != 0;
      0058BB ED               [12] 1688 	mov	a,r5
      0058BC 4E               [12] 1689 	orl	a,r6
      0058BD B4 01 00         [24] 1690 	cjne	a,#0x01,01308$
      0058C0                       1691 01308$:
      0058C0 B3               [12] 1692 	cpl	c
      0058C1 92 09            [24] 1693 	mov	_control_setup_sloc0_1_0,c
      0058C3 90 06 8D         [24] 1694 	mov	dptr,#_USB_EnumStatus
      0058C6 E4               [12] 1695 	clr	a
      0058C7 33               [12] 1696 	rlc	a
      0058C8 F0               [24] 1697 	movx	@dptr,a
                                   1698 ;	tmk_core/protocol/ch555/usb_ak820.c:225: keyboard_reset = 1;
      0058C9 90 06 B6         [24] 1699 	mov	dptr,#_keyboard_reset
      0058CC 74 01            [12] 1700 	mov	a,#0x01
      0058CE F0               [24] 1701 	movx	@dptr,a
                                   1702 ;	tmk_core/protocol/ch555/usb_ak820.c:226: control_phase = CTRL_STATUS_IN;
      0058CF 90 06 E5         [24] 1703 	mov	dptr,#_control_phase
      0058D2 74 03            [12] 1704 	mov	a,#0x03
      0058D4 F0               [24] 1705 	movx	@dptr,a
      0058D5 02 5F 18         [24] 1706 	ljmp	00287$
      0058D8                       1707 00279$:
                                   1708 ;	tmk_core/protocol/ch555/usb_ak820.c:227: } else if (type == 0x80 && D0SetupReqCode == USB_GET_CONFIGURATION && !index && !value && D0SetupLen == 1) {
      0058D8 E4               [12] 1709 	clr	a
      0058D9 BF 80 01         [24] 1710 	cjne	r7,#0x80,01309$
      0058DC 04               [12] 1711 	inc	a
      0058DD                       1712 01309$:
      0058DD FA               [12] 1713 	mov	r2,a
      0058DE 60 34            [24] 1714 	jz	00272$
      0058E0 90 06 86         [24] 1715 	mov	dptr,#_D0SetupReqCode
      0058E3 E0               [24] 1716 	movx	a,@dptr
      0058E4 F9               [12] 1717 	mov	r1,a
      0058E5 B9 08 2C         [24] 1718 	cjne	r1,#0x08,00272$
      0058E8 EB               [12] 1719 	mov	a,r3
      0058E9 4C               [12] 1720 	orl	a,r4
      0058EA 70 28            [24] 1721 	jnz	00272$
      0058EC ED               [12] 1722 	mov	a,r5
      0058ED 4E               [12] 1723 	orl	a,r6
      0058EE 70 24            [24] 1724 	jnz	00272$
      0058F0 90 06 87         [24] 1725 	mov	dptr,#_D0SetupLen
      0058F3 E0               [24] 1726 	movx	a,@dptr
      0058F4 F8               [12] 1727 	mov	r0,a
      0058F5 A3               [24] 1728 	inc	dptr
      0058F6 E0               [24] 1729 	movx	a,@dptr
      0058F7 F9               [12] 1730 	mov	r1,a
      0058F8 B8 01 19         [24] 1731 	cjne	r0,#0x01,00272$
      0058FB B9 00 16         [24] 1732 	cjne	r1,#0x00,00272$
                                   1733 ;	tmk_core/protocol/ch555/usb_ak820.c:228: pD0_EP0_BUF[0] = D0UsbConfig;
      0058FE 90 06 8C         [24] 1734 	mov	dptr,#_D0UsbConfig
      005901 E0               [24] 1735 	movx	a,@dptr
      005902 90 10 00         [24] 1736 	mov	dptr,#0x1000
      005905 F0               [24] 1737 	movx	@dptr,a
                                   1738 ;	tmk_core/protocol/ch555/usb_ak820.c:229: D0_EP0T_L = 1;
      005906 90 22 08         [24] 1739 	mov	dptr,#0x2208
      005909 74 01            [12] 1740 	mov	a,#0x01
      00590B F0               [24] 1741 	movx	@dptr,a
                                   1742 ;	tmk_core/protocol/ch555/usb_ak820.c:230: control_phase = CTRL_STATUS_OUT;
      00590C 90 06 E5         [24] 1743 	mov	dptr,#_control_phase
      00590F 04               [12] 1744 	inc	a
      005910 F0               [24] 1745 	movx	@dptr,a
      005911 02 5F 18         [24] 1746 	ljmp	00287$
      005914                       1747 00272$:
                                   1748 ;	tmk_core/protocol/ch555/usb_ak820.c:231: } else if (type == 0x81 && D0SetupReqCode == USB_GET_INTERFACE && index < TOTAL_INTERFACES && !value && D0SetupLen == 1 && D0UsbConfig) {
      005914 E4               [12] 1749 	clr	a
      005915 BF 81 01         [24] 1750 	cjne	r7,#0x81,01318$
      005918 04               [12] 1751 	inc	a
      005919                       1752 01318$:
      005919 F5 24            [12] 1753 	mov	_control_setup_sloc1_1_0,a
      00591B 60 3B            [24] 1754 	jz	00264$
      00591D 90 06 86         [24] 1755 	mov	dptr,#_D0SetupReqCode
      005920 E0               [24] 1756 	movx	a,@dptr
      005921 F8               [12] 1757 	mov	r0,a
      005922 B8 0A 33         [24] 1758 	cjne	r0,#0x0a,00264$
      005925 C3               [12] 1759 	clr	c
      005926 EB               [12] 1760 	mov	a,r3
      005927 94 03            [12] 1761 	subb	a,#0x03
      005929 EC               [12] 1762 	mov	a,r4
      00592A 94 00            [12] 1763 	subb	a,#0x00
      00592C 50 2A            [24] 1764 	jnc	00264$
      00592E ED               [12] 1765 	mov	a,r5
      00592F 4E               [12] 1766 	orl	a,r6
      005930 70 26            [24] 1767 	jnz	00264$
      005932 90 06 87         [24] 1768 	mov	dptr,#_D0SetupLen
      005935 E0               [24] 1769 	movx	a,@dptr
      005936 F8               [12] 1770 	mov	r0,a
      005937 A3               [24] 1771 	inc	dptr
      005938 E0               [24] 1772 	movx	a,@dptr
      005939 F9               [12] 1773 	mov	r1,a
      00593A B8 01 1B         [24] 1774 	cjne	r0,#0x01,00264$
      00593D B9 00 18         [24] 1775 	cjne	r1,#0x00,00264$
      005940 90 06 8C         [24] 1776 	mov	dptr,#_D0UsbConfig
      005943 E0               [24] 1777 	movx	a,@dptr
      005944 60 12            [24] 1778 	jz	00264$
                                   1779 ;	tmk_core/protocol/ch555/usb_ak820.c:232: pD0_EP0_BUF[0] = 0;
      005946 90 10 00         [24] 1780 	mov	dptr,#0x1000
      005949 E4               [12] 1781 	clr	a
      00594A F0               [24] 1782 	movx	@dptr,a
                                   1783 ;	tmk_core/protocol/ch555/usb_ak820.c:233: D0_EP0T_L = 1;
      00594B 90 22 08         [24] 1784 	mov	dptr,#0x2208
      00594E 04               [12] 1785 	inc	a
      00594F F0               [24] 1786 	movx	@dptr,a
                                   1787 ;	tmk_core/protocol/ch555/usb_ak820.c:234: control_phase = CTRL_STATUS_OUT;
      005950 90 06 E5         [24] 1788 	mov	dptr,#_control_phase
      005953 04               [12] 1789 	inc	a
      005954 F0               [24] 1790 	movx	@dptr,a
      005955 02 5F 18         [24] 1791 	ljmp	00287$
      005958                       1792 00264$:
                                   1793 ;	tmk_core/protocol/ch555/usb_ak820.c:235: } else if (type == 0x01 && D0SetupReqCode == USB_SET_INTERFACE && index < TOTAL_INTERFACES && !value && !D0SetupLen && D0UsbConfig) {
      005958 BF 01 2E         [24] 1794 	cjne	r7,#0x01,00256$
      00595B 90 06 86         [24] 1795 	mov	dptr,#_D0SetupReqCode
      00595E E0               [24] 1796 	movx	a,@dptr
      00595F F8               [12] 1797 	mov	r0,a
      005960 B8 0B 26         [24] 1798 	cjne	r0,#0x0b,00256$
      005963 C3               [12] 1799 	clr	c
      005964 EB               [12] 1800 	mov	a,r3
      005965 94 03            [12] 1801 	subb	a,#0x03
      005967 EC               [12] 1802 	mov	a,r4
      005968 94 00            [12] 1803 	subb	a,#0x00
      00596A 50 1D            [24] 1804 	jnc	00256$
      00596C ED               [12] 1805 	mov	a,r5
      00596D 4E               [12] 1806 	orl	a,r6
      00596E 70 19            [24] 1807 	jnz	00256$
      005970 90 06 87         [24] 1808 	mov	dptr,#_D0SetupLen
      005973 E0               [24] 1809 	movx	a,@dptr
      005974 F8               [12] 1810 	mov	r0,a
      005975 A3               [24] 1811 	inc	dptr
      005976 E0               [24] 1812 	movx	a,@dptr
      005977 48               [12] 1813 	orl	a,r0
      005978 70 0F            [24] 1814 	jnz	00256$
      00597A 90 06 8C         [24] 1815 	mov	dptr,#_D0UsbConfig
      00597D E0               [24] 1816 	movx	a,@dptr
      00597E 60 09            [24] 1817 	jz	00256$
                                   1818 ;	tmk_core/protocol/ch555/usb_ak820.c:236: control_phase = CTRL_STATUS_IN;
      005980 90 06 E5         [24] 1819 	mov	dptr,#_control_phase
      005983 74 03            [12] 1820 	mov	a,#0x03
      005985 F0               [24] 1821 	movx	@dptr,a
      005986 02 5F 18         [24] 1822 	ljmp	00287$
      005989                       1823 00256$:
                                   1824 ;	tmk_core/protocol/ch555/usb_ak820.c:237: } else if (D0SetupReqCode == USB_GET_STATUS && !value && D0SetupLen == 2 &&
      005989 90 06 86         [24] 1825 	mov	dptr,#_D0SetupReqCode
      00598C E0               [24] 1826 	movx	a,@dptr
      00598D 60 03            [24] 1827 	jz	01336$
      00598F 02 5A 39         [24] 1828 	ljmp	00240$
      005992                       1829 01336$:
      005992 ED               [12] 1830 	mov	a,r5
      005993 4E               [12] 1831 	orl	a,r6
      005994 60 03            [24] 1832 	jz	01337$
      005996 02 5A 39         [24] 1833 	ljmp	00240$
      005999                       1834 01337$:
      005999 90 06 87         [24] 1835 	mov	dptr,#_D0SetupLen
      00599C E0               [24] 1836 	movx	a,@dptr
      00599D F8               [12] 1837 	mov	r0,a
      00599E A3               [24] 1838 	inc	dptr
      00599F E0               [24] 1839 	movx	a,@dptr
      0059A0 F9               [12] 1840 	mov	r1,a
      0059A1 B8 02 05         [24] 1841 	cjne	r0,#0x02,01338$
      0059A4 B9 00 02         [24] 1842 	cjne	r1,#0x00,01338$
      0059A7 80 03            [24] 1843 	sjmp	01339$
      0059A9                       1844 01338$:
      0059A9 02 5A 39         [24] 1845 	ljmp	00240$
      0059AC                       1846 01339$:
                                   1847 ;	tmk_core/protocol/ch555/usb_ak820.c:238: ((type == 0x80 && !index) || (type == 0x81 && index < TOTAL_INTERFACES && D0UsbConfig) ||
      0059AC EA               [12] 1848 	mov	a,r2
      0059AD 60 04            [24] 1849 	jz	00247$
      0059AF EB               [12] 1850 	mov	a,r3
      0059B0 4C               [12] 1851 	orl	a,r4
      0059B1 60 3C            [24] 1852 	jz	00239$
      0059B3                       1853 00247$:
      0059B3 E5 24            [12] 1854 	mov	a,_control_setup_sloc1_1_0
      0059B5 60 0F            [24] 1855 	jz	00253$
      0059B7 C3               [12] 1856 	clr	c
      0059B8 EB               [12] 1857 	mov	a,r3
      0059B9 94 03            [12] 1858 	subb	a,#0x03
      0059BB EC               [12] 1859 	mov	a,r4
      0059BC 94 00            [12] 1860 	subb	a,#0x00
      0059BE 50 06            [24] 1861 	jnc	00253$
      0059C0 90 06 8C         [24] 1862 	mov	dptr,#_D0UsbConfig
      0059C3 E0               [24] 1863 	movx	a,@dptr
      0059C4 70 29            [24] 1864 	jnz	00239$
      0059C6                       1865 00253$:
                                   1866 ;	tmk_core/protocol/ch555/usb_ak820.c:239: (type == 0x82 && D0UsbConfig && (index == 0 || index == 0x80 || (index >= 0x81 && index <= 0x83))))) {
      0059C6 BF 82 70         [24] 1867 	cjne	r7,#0x82,00240$
      0059C9 90 06 8C         [24] 1868 	mov	dptr,#_D0UsbConfig
      0059CC E0               [24] 1869 	movx	a,@dptr
      0059CD 60 6A            [24] 1870 	jz	00240$
      0059CF EB               [12] 1871 	mov	a,r3
      0059D0 4C               [12] 1872 	orl	a,r4
      0059D1 60 1C            [24] 1873 	jz	00239$
      0059D3 8B 00            [24] 1874 	mov	ar0,r3
      0059D5 8C 01            [24] 1875 	mov	ar1,r4
      0059D7 B8 80 05         [24] 1876 	cjne	r0,#0x80,01349$
      0059DA B9 00 02         [24] 1877 	cjne	r1,#0x00,01349$
      0059DD 80 10            [24] 1878 	sjmp	00239$
      0059DF                       1879 01349$:
      0059DF C3               [12] 1880 	clr	c
      0059E0 E8               [12] 1881 	mov	a,r0
      0059E1 94 81            [12] 1882 	subb	a,#0x81
      0059E3 E9               [12] 1883 	mov	a,r1
      0059E4 94 00            [12] 1884 	subb	a,#0x00
      0059E6 40 51            [24] 1885 	jc	00240$
      0059E8 74 83            [12] 1886 	mov	a,#0x83
      0059EA 98               [12] 1887 	subb	a,r0
      0059EB E4               [12] 1888 	clr	a
      0059EC 99               [12] 1889 	subb	a,r1
      0059ED 40 4A            [24] 1890 	jc	00240$
                                   1891 ;	free result
      0059EF                       1892 00239$:
                                   1893 ;	tmk_core/protocol/ch555/usb_ak820.c:240: endpoint = index & 7;
      0059EF 8B 01            [24] 1894 	mov	ar1,r3
      0059F1 53 01 07         [24] 1895 	anl	ar1,#0x07
                                   1896 ;	tmk_core/protocol/ch555/usb_ak820.c:241: pD0_EP0_BUF[0] = type == 0x80 ? ((USB_SleepStatus & 1) << 1) :
      0059F4 EA               [12] 1897 	mov	a,r2
      0059F5 60 0B            [24] 1898 	jz	00308$
      0059F7 90 06 8E         [24] 1899 	mov	dptr,#_USB_SleepStatus
      0059FA E0               [24] 1900 	movx	a,@dptr
      0059FB 54 01            [12] 1901 	anl	a,#0x01
      0059FD 25 E0            [12] 1902 	add	a,acc
      0059FF FA               [12] 1903 	mov	r2,a
      005A00 80 22            [24] 1904 	sjmp	00309$
      005A02                       1905 00308$:
                                   1906 ;	tmk_core/protocol/ch555/usb_ak820.c:242: ((type == 0x82 && endpoint && (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_STALL) ? 1 : 0);
      005A02 BF 82 1B         [24] 1907 	cjne	r7,#0x82,00310$
      005A05 E9               [12] 1908 	mov	a,r1
      005A06 60 18            [24] 1909 	jz	00310$
      005A08 89 00            [24] 1910 	mov	ar0,r1
      005A0A 79 00            [12] 1911 	mov	r1,#0x00
      005A0C 74 22            [12] 1912 	mov	a,#0x22
      005A0E 29               [12] 1913 	add	a, r1
      005A0F F9               [12] 1914 	mov	r1,a
      005A10 88 82            [24] 1915 	mov	dpl,r0
      005A12 89 83            [24] 1916 	mov	dph,r1
      005A14 E0               [24] 1917 	movx	a,@dptr
      005A15 F9               [12] 1918 	mov	r1,a
      005A16 53 01 03         [24] 1919 	anl	ar1,#0x03
      005A19 B9 03 04         [24] 1920 	cjne	r1,#0x03,00310$
      005A1C 79 01            [12] 1921 	mov	r1,#0x01
      005A1E 80 02            [24] 1922 	sjmp	00311$
      005A20                       1923 00310$:
      005A20 79 00            [12] 1924 	mov	r1,#0x00
      005A22                       1925 00311$:
      005A22 89 02            [24] 1926 	mov	ar2,r1
      005A24                       1927 00309$:
      005A24 90 10 00         [24] 1928 	mov	dptr,#0x1000
      005A27 EA               [12] 1929 	mov	a,r2
      005A28 F0               [24] 1930 	movx	@dptr,a
                                   1931 ;	tmk_core/protocol/ch555/usb_ak820.c:243: pD0_EP0_BUF[1] = 0;
      005A29 A3               [24] 1932 	inc	dptr
      005A2A E4               [12] 1933 	clr	a
      005A2B F0               [24] 1934 	movx	@dptr,a
                                   1935 ;	tmk_core/protocol/ch555/usb_ak820.c:244: D0_EP0T_L = 2;
      005A2C 90 22 08         [24] 1936 	mov	dptr,#0x2208
      005A2F 74 02            [12] 1937 	mov	a,#0x02
      005A31 F0               [24] 1938 	movx	@dptr,a
                                   1939 ;	tmk_core/protocol/ch555/usb_ak820.c:245: control_phase = CTRL_STATUS_OUT;
      005A32 90 06 E5         [24] 1940 	mov	dptr,#_control_phase
      005A35 F0               [24] 1941 	movx	@dptr,a
      005A36 02 5F 18         [24] 1942 	ljmp	00287$
      005A39                       1943 00240$:
                                   1944 ;	tmk_core/protocol/ch555/usb_ak820.c:246: } else if ((D0SetupReqCode == USB_SET_FEATURE || D0SetupReqCode == USB_CLEAR_FEATURE) && !D0SetupLen && D0UsbConfig) {
      005A39 90 06 86         [24] 1945 	mov	dptr,#_D0SetupReqCode
      005A3C E0               [24] 1946 	movx	a,@dptr
      005A3D FA               [12] 1947 	mov	r2,a
      005A3E BA 03 02         [24] 1948 	cjne	r2,#0x03,01358$
      005A41 80 0D            [24] 1949 	sjmp	00237$
      005A43                       1950 01358$:
      005A43 90 06 86         [24] 1951 	mov	dptr,#_D0SetupReqCode
      005A46 E0               [24] 1952 	movx	a,@dptr
      005A47 FA               [12] 1953 	mov	r2,a
      005A48 BA 01 02         [24] 1954 	cjne	r2,#0x01,01359$
      005A4B 80 03            [24] 1955 	sjmp	01360$
      005A4D                       1956 01359$:
      005A4D 02 5A EC         [24] 1957 	ljmp	00234$
      005A50                       1958 01360$:
      005A50                       1959 00237$:
      005A50 90 06 87         [24] 1960 	mov	dptr,#_D0SetupLen
      005A53 E0               [24] 1961 	movx	a,@dptr
      005A54 F9               [12] 1962 	mov	r1,a
      005A55 A3               [24] 1963 	inc	dptr
      005A56 E0               [24] 1964 	movx	a,@dptr
      005A57 49               [12] 1965 	orl	a,r1
      005A58 60 03            [24] 1966 	jz	01361$
      005A5A 02 5A EC         [24] 1967 	ljmp	00234$
      005A5D                       1968 01361$:
      005A5D 90 06 8C         [24] 1969 	mov	dptr,#_D0UsbConfig
      005A60 E0               [24] 1970 	movx	a,@dptr
      005A61 70 03            [24] 1971 	jnz	01362$
      005A63 02 5A EC         [24] 1972 	ljmp	00234$
      005A66                       1973 01362$:
                                   1974 ;	tmk_core/protocol/ch555/usb_ak820.c:247: if (type == 0x00 && value == 1 && !index) {
      005A66 EF               [12] 1975 	mov	a,r7
      005A67 70 2A            [24] 1976 	jnz	00127$
      005A69 8D 01            [24] 1977 	mov	ar1,r5
      005A6B 8E 02            [24] 1978 	mov	ar2,r6
      005A6D B9 01 23         [24] 1979 	cjne	r1,#0x01,00127$
      005A70 BA 00 20         [24] 1980 	cjne	r2,#0x00,00127$
      005A73 EB               [12] 1981 	mov	a,r3
      005A74 4C               [12] 1982 	orl	a,r4
      005A75 70 1C            [24] 1983 	jnz	00127$
                                   1984 ;	tmk_core/protocol/ch555/usb_ak820.c:248: if (D0SetupReqCode == USB_SET_FEATURE) USB_SleepStatus |= 1;
      005A77 90 06 86         [24] 1985 	mov	dptr,#_D0SetupReqCode
      005A7A E0               [24] 1986 	movx	a,@dptr
      005A7B FA               [12] 1987 	mov	r2,a
      005A7C BA 03 0A         [24] 1988 	cjne	r2,#0x03,00116$
      005A7F 90 06 8E         [24] 1989 	mov	dptr,#_USB_SleepStatus
      005A82 E0               [24] 1990 	movx	a,@dptr
      005A83 43 E0 01         [24] 1991 	orl	acc,#0x01
      005A86 F0               [24] 1992 	movx	@dptr,a
      005A87 80 5A            [24] 1993 	sjmp	00128$
      005A89                       1994 00116$:
                                   1995 ;	tmk_core/protocol/ch555/usb_ak820.c:249: else USB_SleepStatus &= ~1;
      005A89 90 06 8E         [24] 1996 	mov	dptr,#_USB_SleepStatus
      005A8C E0               [24] 1997 	movx	a,@dptr
      005A8D 53 E0 FE         [24] 1998 	anl	acc,#0xfe
      005A90 F0               [24] 1999 	movx	@dptr,a
      005A91 80 50            [24] 2000 	sjmp	00128$
      005A93                       2001 00127$:
                                   2002 ;	tmk_core/protocol/ch555/usb_ak820.c:250: } else if (type == 0x02 && !value && index >= 0x81 && index <= 0x83) {
      005A93 BF 02 4A         [24] 2003 	cjne	r7,#0x02,00121$
      005A96 ED               [12] 2004 	mov	a,r5
      005A97 4E               [12] 2005 	orl	a,r6
      005A98 70 46            [24] 2006 	jnz	00121$
      005A9A 8B 01            [24] 2007 	mov	ar1,r3
      005A9C 8C 02            [24] 2008 	mov	ar2,r4
      005A9E C3               [12] 2009 	clr	c
      005A9F E9               [12] 2010 	mov	a,r1
      005AA0 94 81            [12] 2011 	subb	a,#0x81
      005AA2 EA               [12] 2012 	mov	a,r2
      005AA3 94 00            [12] 2013 	subb	a,#0x00
      005AA5 40 39            [24] 2014 	jc	00121$
      005AA7 74 83            [12] 2015 	mov	a,#0x83
      005AA9 99               [12] 2016 	subb	a,r1
      005AAA E4               [12] 2017 	clr	a
      005AAB 9A               [12] 2018 	subb	a,r2
      005AAC 40 32            [24] 2019 	jc	00121$
                                   2020 ;	free result
                                   2021 ;	tmk_core/protocol/ch555/usb_ak820.c:251: endpoint = index & 7;
      005AAE 8B 02            [24] 2022 	mov	ar2,r3
      005AB0 53 02 07         [24] 2023 	anl	ar2,#0x07
                                   2024 ;	tmk_core/protocol/ch555/usb_ak820.c:253: EP_RESPONSE(endpoint) = bUEP_X_AUTO_TOG | (D0SetupReqCode == USB_SET_FEATURE ? UEP_X_RES_STALL : UEP_X_RES_NAK);
      005AB3 8A 00            [24] 2025 	mov	ar0,r2
      005AB5 79 00            [12] 2026 	mov	r1,#0x00
      005AB7 74 22            [12] 2027 	mov	a,#0x22
      005AB9 29               [12] 2028 	add	a, r1
      005ABA F9               [12] 2029 	mov	r1,a
      005ABB 88 24            [24] 2030 	mov	_control_setup_sloc1_1_0,r0
      005ABD 89 25            [24] 2031 	mov	(_control_setup_sloc1_1_0 + 1),r1
      005ABF 90 06 86         [24] 2032 	mov	dptr,#_D0SetupReqCode
      005AC2 E0               [24] 2033 	movx	a,@dptr
      005AC3 F9               [12] 2034 	mov	r1,a
      005AC4 B9 03 04         [24] 2035 	cjne	r1,#0x03,00318$
      005AC7 79 03            [12] 2036 	mov	r1,#0x03
      005AC9 80 02            [24] 2037 	sjmp	00319$
      005ACB                       2038 00318$:
      005ACB 79 02            [12] 2039 	mov	r1,#0x02
      005ACD                       2040 00319$:
      005ACD 43 01 10         [24] 2041 	orl	ar1,#0x10
      005AD0 85 24 82         [24] 2042 	mov	dpl,_control_setup_sloc1_1_0
      005AD3 85 25 83         [24] 2043 	mov	dph,(_control_setup_sloc1_1_0 + 1)
      005AD6 E9               [12] 2044 	mov	a,r1
      005AD7 F0               [24] 2045 	movx	@dptr,a
                                   2046 ;	tmk_core/protocol/ch555/usb_ak820.c:254: if (endpoint == RAW_IN_EPNUM) raw_complete();
      005AD8 BA 03 08         [24] 2047 	cjne	r2,#0x03,00128$
      005ADB 12 54 39         [24] 2048 	lcall	_raw_complete
      005ADE 80 03            [24] 2049 	sjmp	00128$
      005AE0                       2050 00121$:
                                   2051 ;	tmk_core/protocol/ch555/usb_ak820.c:255: } else { control_stall(); return; }
      005AE0 02 54 AD         [24] 2052 	ljmp	_control_stall
      005AE3                       2053 00128$:
                                   2054 ;	tmk_core/protocol/ch555/usb_ak820.c:256: control_phase = CTRL_STATUS_IN;
      005AE3 90 06 E5         [24] 2055 	mov	dptr,#_control_phase
      005AE6 74 03            [12] 2056 	mov	a,#0x03
      005AE8 F0               [24] 2057 	movx	@dptr,a
      005AE9 02 5F 18         [24] 2058 	ljmp	00287$
      005AEC                       2059 00234$:
                                   2060 ;	tmk_core/protocol/ch555/usb_ak820.c:257: } else if (type == 0xa1 && D0SetupReqCode == HID_GET_REPORT && D0UsbConfig && D0SetupLen) {
      005AEC E4               [12] 2061 	clr	a
      005AED BF A1 01         [24] 2062 	cjne	r7,#0xa1,01378$
      005AF0 04               [12] 2063 	inc	a
      005AF1                       2064 01378$:
      005AF1 FA               [12] 2065 	mov	r2,a
      005AF2 70 03            [24] 2066 	jnz	01380$
      005AF4 02 5D 6E         [24] 2067 	ljmp	00228$
      005AF7                       2068 01380$:
      005AF7 90 06 86         [24] 2069 	mov	dptr,#_D0SetupReqCode
      005AFA E0               [24] 2070 	movx	a,@dptr
      005AFB F9               [12] 2071 	mov	r1,a
      005AFC B9 01 02         [24] 2072 	cjne	r1,#0x01,01381$
      005AFF 80 03            [24] 2073 	sjmp	01382$
      005B01                       2074 01381$:
      005B01 02 5D 6E         [24] 2075 	ljmp	00228$
      005B04                       2076 01382$:
      005B04 90 06 8C         [24] 2077 	mov	dptr,#_D0UsbConfig
      005B07 E0               [24] 2078 	movx	a,@dptr
      005B08 70 03            [24] 2079 	jnz	01383$
      005B0A 02 5D 6E         [24] 2080 	ljmp	00228$
      005B0D                       2081 01383$:
      005B0D 90 06 87         [24] 2082 	mov	dptr,#_D0SetupLen
      005B10 E0               [24] 2083 	movx	a,@dptr
      005B11 F8               [12] 2084 	mov	r0,a
      005B12 A3               [24] 2085 	inc	dptr
      005B13 E0               [24] 2086 	movx	a,@dptr
      005B14 48               [12] 2087 	orl	a,r0
      005B15 70 03            [24] 2088 	jnz	01384$
      005B17 02 5D 6E         [24] 2089 	ljmp	00228$
      005B1A                       2090 01384$:
                                   2091 ;	tmk_core/protocol/ch555/usb_ak820.c:258: report_id = value;
      005B1A C0 03            [24] 2092 	push	ar3
      005B1C C0 04            [24] 2093 	push	ar4
      005B1E 8D 01            [24] 2094 	mov	ar1,r5
                                   2095 ;	tmk_core/protocol/ch555/usb_ak820.c:259: if ((value >> 8) == 1 && index == KEYBOARD_INTERFACE && !report_id) {
      005B20 8E 00            [24] 2096 	mov	ar0,r6
      005B22 B8 01 03         [24] 2097 	cjne	r0,#0x01,01385$
      005B25 E8               [12] 2098 	mov	a,r0
      005B26 80 01            [24] 2099 	sjmp	01386$
      005B28                       2100 01385$:
      005B28 E4               [12] 2101 	clr	a
      005B29                       2102 01386$:
      005B29 F5 24            [12] 2103 	mov	_control_setup_sloc1_1_0,a
      005B2B D0 04            [24] 2104 	pop	ar4
      005B2D D0 03            [24] 2105 	pop	ar3
      005B2F E5 24            [12] 2106 	mov	a,_control_setup_sloc1_1_0
      005B31 60 17            [24] 2107 	jz	00160$
      005B33 EB               [12] 2108 	mov	a,r3
      005B34 4C               [12] 2109 	orl	a,r4
      005B35 70 13            [24] 2110 	jnz	00160$
      005B37 E9               [12] 2111 	mov	a,r1
      005B38 70 10            [24] 2112 	jnz	00160$
                                   2113 ;	tmk_core/protocol/ch555/usb_ak820.c:260: length = KEYBOARD_EPSIZE;
      005B3A 90 06 EF         [24] 2114 	mov	dptr,#_control_setup_length_10000_286
      005B3D 74 08            [12] 2115 	mov	a,#0x08
      005B3F F0               [24] 2116 	movx	@dptr,a
      005B40 E4               [12] 2117 	clr	a
      005B41 A3               [24] 2118 	inc	dptr
      005B42 F0               [24] 2119 	movx	@dptr,a
                                   2120 ;	tmk_core/protocol/ch555/usb_ak820.c:261: offset = SNAPSHOT_KEYBOARD;
      005B43 90 06 F1         [24] 2121 	mov	dptr,#_control_setup_offset_10000_286
      005B46 F0               [24] 2122 	movx	@dptr,a
      005B47 02 5C CE         [24] 2123 	ljmp	00161$
      005B4A                       2124 00160$:
                                   2125 ;	tmk_core/protocol/ch555/usb_ak820.c:262: } else if ((value >> 8) == 1 && index == SHARED_INTERFACE &&
      005B4A E5 24            [12] 2126 	mov	a,_control_setup_sloc1_1_0
      005B4C 60 27            [24] 2127 	jz	00154$
      005B4E BB 02 24         [24] 2128 	cjne	r3,#0x02,00154$
      005B51 BC 00 21         [24] 2129 	cjne	r4,#0x00,00154$
                                   2130 ;	tmk_core/protocol/ch555/usb_ak820.c:263: report_id < sizeof(shared_lengths) && shared_lengths[report_id]) {
      005B54 B9 07 00         [24] 2131 	cjne	r1,#0x07,01393$
      005B57                       2132 01393$:
      005B57 50 1C            [24] 2133 	jnc	00154$
      005B59 E9               [12] 2134 	mov	a,r1
      005B5A 90 B6 3B         [24] 2135 	mov	dptr,#_shared_lengths
      005B5D 93               [24] 2136 	movc	a,@a+dptr
      005B5E F8               [12] 2137 	mov	r0,a
      005B5F 60 14            [24] 2138 	jz	00154$
                                   2139 ;	tmk_core/protocol/ch555/usb_ak820.c:264: length = shared_lengths[report_id];
      005B61 90 06 EF         [24] 2140 	mov	dptr,#_control_setup_length_10000_286
      005B64 E8               [12] 2141 	mov	a,r0
      005B65 F0               [24] 2142 	movx	@dptr,a
      005B66 E4               [12] 2143 	clr	a
      005B67 A3               [24] 2144 	inc	dptr
      005B68 F0               [24] 2145 	movx	@dptr,a
                                   2146 ;	tmk_core/protocol/ch555/usb_ak820.c:265: offset = shared_offsets[report_id];
      005B69 E9               [12] 2147 	mov	a,r1
      005B6A 90 B6 34         [24] 2148 	mov	dptr,#_shared_offsets
      005B6D 93               [24] 2149 	movc	a,@a+dptr
      005B6E 90 06 F1         [24] 2150 	mov	dptr,#_control_setup_offset_10000_286
      005B71 F0               [24] 2151 	movx	@dptr,a
      005B72 02 5C CE         [24] 2152 	ljmp	00161$
      005B75                       2153 00154$:
                                   2154 ;	tmk_core/protocol/ch555/usb_ak820.c:266: } else if ((value >> 8) == 1 && index == RAW_INTERFACE && !report_id) {
      005B75 E5 24            [12] 2155 	mov	a,_control_setup_sloc1_1_0
      005B77 60 7A            [24] 2156 	jz	00149$
      005B79 BB 01 77         [24] 2157 	cjne	r3,#0x01,00149$
      005B7C BC 00 74         [24] 2158 	cjne	r4,#0x00,00149$
      005B7F E9               [12] 2159 	mov	a,r1
      005B80 70 71            [24] 2160 	jnz	00149$
                                   2161 ;	tmk_core/protocol/ch555/usb_ak820.c:267: length = D0SetupLen < RAW_EPSIZE ? D0SetupLen : RAW_EPSIZE;
      005B82 90 06 87         [24] 2162 	mov	dptr,#_D0SetupLen
      005B85 E0               [24] 2163 	movx	a,@dptr
      005B86 F8               [12] 2164 	mov	r0,a
      005B87 A3               [24] 2165 	inc	dptr
      005B88 E0               [24] 2166 	movx	a,@dptr
      005B89 F9               [12] 2167 	mov	r1,a
      005B8A C3               [12] 2168 	clr	c
      005B8B E8               [12] 2169 	mov	a,r0
      005B8C 94 20            [12] 2170 	subb	a,#0x20
      005B8E E9               [12] 2171 	mov	a,r1
      005B8F 94 00            [12] 2172 	subb	a,#0x00
      005B91 50 0A            [24] 2173 	jnc	00320$
      005B93 90 06 87         [24] 2174 	mov	dptr,#_D0SetupLen
      005B96 E0               [24] 2175 	movx	a,@dptr
      005B97 F8               [12] 2176 	mov	r0,a
      005B98 A3               [24] 2177 	inc	dptr
      005B99 E0               [24] 2178 	movx	a,@dptr
      005B9A F9               [12] 2179 	mov	r1,a
      005B9B 80 04            [24] 2180 	sjmp	00321$
      005B9D                       2181 00320$:
      005B9D 78 20            [12] 2182 	mov	r0,#0x20
      005B9F 79 00            [12] 2183 	mov	r1,#0x00
      005BA1                       2184 00321$:
                                   2185 ;	tmk_core/protocol/ch555/usb_ak820.c:268: for (i = 0; i < length; ++i) pD0_EP0_BUF[i] = pUSB_BUF_DEV0[UX_EP3_ADDR + i];
      005BA1 75 24 00         [24] 2186 	mov	_control_setup_sloc1_1_0,#0x00
      005BA4                       2187 00293$:
      005BA4 C0 03            [24] 2188 	push	ar3
      005BA6 C0 04            [24] 2189 	push	ar4
      005BA8 AB 24            [24] 2190 	mov	r3,_control_setup_sloc1_1_0
      005BAA 7C 00            [12] 2191 	mov	r4,#0x00
      005BAC C3               [12] 2192 	clr	c
      005BAD EB               [12] 2193 	mov	a,r3
      005BAE 98               [12] 2194 	subb	a,r0
      005BAF EC               [12] 2195 	mov	a,r4
      005BB0 99               [12] 2196 	subb	a,r1
      005BB1 D0 04            [24] 2197 	pop	ar4
      005BB3 D0 03            [24] 2198 	pop	ar3
      005BB5 50 32            [24] 2199 	jnc	00131$
      005BB7 C0 00            [24] 2200 	push	ar0
      005BB9 C0 01            [24] 2201 	push	ar1
      005BBB 85 24 26         [24] 2202 	mov	_control_setup_sloc2_1_0,_control_setup_sloc1_1_0
      005BBE 74 10            [12] 2203 	mov	a,#0x10
      005BC0 24 00            [12] 2204 	add	a, #0x00
      005BC2 F5 27            [12] 2205 	mov	(_control_setup_sloc2_1_0 + 1),a
      005BC4 A8 24            [24] 2206 	mov	r0,_control_setup_sloc1_1_0
      005BC6 79 00            [12] 2207 	mov	r1,#0x00
      005BC8 74 C0            [12] 2208 	mov	a,#0xc0
      005BCA 28               [12] 2209 	add	a, r0
      005BCB F8               [12] 2210 	mov	r0,a
      005BCC E4               [12] 2211 	clr	a
      005BCD 39               [12] 2212 	addc	a, r1
      005BCE F9               [12] 2213 	mov	r1,a
      005BCF 88 82            [24] 2214 	mov	dpl,r0
      005BD1 74 10            [12] 2215 	mov	a,#0x10
      005BD3 29               [12] 2216 	add	a, r1
      005BD4 F5 83            [12] 2217 	mov	dph,a
      005BD6 E0               [24] 2218 	movx	a,@dptr
      005BD7 85 26 82         [24] 2219 	mov	dpl,_control_setup_sloc2_1_0
      005BDA 85 27 83         [24] 2220 	mov	dph,(_control_setup_sloc2_1_0 + 1)
      005BDD F0               [24] 2221 	movx	@dptr,a
      005BDE E5 24            [12] 2222 	mov	a,_control_setup_sloc1_1_0
      005BE0 04               [12] 2223 	inc	a
      005BE1 F5 24            [12] 2224 	mov	_control_setup_sloc1_1_0,a
      005BE3 D0 01            [24] 2225 	pop	ar1
      005BE5 D0 00            [24] 2226 	pop	ar0
      005BE7 80 BB            [24] 2227 	sjmp	00293$
      005BE9                       2228 00131$:
                                   2229 ;	tmk_core/protocol/ch555/usb_ak820.c:269: length = 0; /* data already copied */
      005BE9 90 06 EF         [24] 2230 	mov	dptr,#_control_setup_length_10000_286
      005BEC E4               [12] 2231 	clr	a
      005BED F0               [24] 2232 	movx	@dptr,a
      005BEE A3               [24] 2233 	inc	dptr
      005BEF F0               [24] 2234 	movx	@dptr,a
      005BF0 02 5C CE         [24] 2235 	ljmp	00161$
      005BF3                       2236 00149$:
                                   2237 ;	tmk_core/protocol/ch555/usb_ak820.c:270: } else if (value == 0x0200 && index == KEYBOARD_INTERFACE) {
      005BF3 8D 00            [24] 2238 	mov	ar0,r5
      005BF5 8E 01            [24] 2239 	mov	ar1,r6
      005BF7 B8 00 21         [24] 2240 	cjne	r0,#0x00,00145$
      005BFA B9 02 1E         [24] 2241 	cjne	r1,#0x02,00145$
      005BFD EB               [12] 2242 	mov	a,r3
      005BFE 4C               [12] 2243 	orl	a,r4
      005BFF 70 1A            [24] 2244 	jnz	00145$
                                   2245 ;	tmk_core/protocol/ch555/usb_ak820.c:271: pD0_EP0_BUF[0] = KB_USB_SetReport;
      005C01 90 06 91         [24] 2246 	mov	dptr,#_KB_USB_SetReport
      005C04 E0               [24] 2247 	movx	a,@dptr
      005C05 90 10 00         [24] 2248 	mov	dptr,#0x1000
      005C08 F0               [24] 2249 	movx	@dptr,a
                                   2250 ;	tmk_core/protocol/ch555/usb_ak820.c:272: length = 0;
      005C09 90 06 EF         [24] 2251 	mov	dptr,#_control_setup_length_10000_286
      005C0C E4               [12] 2252 	clr	a
      005C0D F0               [24] 2253 	movx	@dptr,a
      005C0E A3               [24] 2254 	inc	dptr
      005C0F F0               [24] 2255 	movx	@dptr,a
                                   2256 ;	tmk_core/protocol/ch555/usb_ak820.c:273: D0SetupLen = 1;
      005C10 90 06 87         [24] 2257 	mov	dptr,#_D0SetupLen
      005C13 04               [12] 2258 	inc	a
      005C14 F0               [24] 2259 	movx	@dptr,a
      005C15 E4               [12] 2260 	clr	a
      005C16 A3               [24] 2261 	inc	dptr
      005C17 F0               [24] 2262 	movx	@dptr,a
      005C18 02 5C CE         [24] 2263 	ljmp	00161$
      005C1B                       2264 00145$:
                                   2265 ;	tmk_core/protocol/ch555/usb_ak820.c:274: } else if (value == (0x0200 | REPORT_ID_NKRO) && index == SHARED_INTERFACE) {
      005C1B B8 06 41         [24] 2266 	cjne	r0,#0x06,00141$
      005C1E B9 02 3E         [24] 2267 	cjne	r1,#0x02,00141$
      005C21 BB 02 3B         [24] 2268 	cjne	r3,#0x02,00141$
      005C24 BC 00 38         [24] 2269 	cjne	r4,#0x00,00141$
                                   2270 ;	tmk_core/protocol/ch555/usb_ak820.c:275: pD0_EP0_BUF[0] = REPORT_ID_NKRO;
      005C27 C0 03            [24] 2271 	push	ar3
      005C29 C0 04            [24] 2272 	push	ar4
      005C2B 90 10 00         [24] 2273 	mov	dptr,#0x1000
      005C2E 74 06            [12] 2274 	mov	a,#0x06
      005C30 F0               [24] 2275 	movx	@dptr,a
                                   2276 ;	tmk_core/protocol/ch555/usb_ak820.c:276: pD0_EP0_BUF[1] = KB_USB_SetReport;
      005C31 90 06 91         [24] 2277 	mov	dptr,#_KB_USB_SetReport
      005C34 E0               [24] 2278 	movx	a,@dptr
      005C35 90 10 01         [24] 2279 	mov	dptr,#0x1001
      005C38 F0               [24] 2280 	movx	@dptr,a
                                   2281 ;	tmk_core/protocol/ch555/usb_ak820.c:277: length = 0;
      005C39 90 06 EF         [24] 2282 	mov	dptr,#_control_setup_length_10000_286
      005C3C E4               [12] 2283 	clr	a
      005C3D F0               [24] 2284 	movx	@dptr,a
      005C3E A3               [24] 2285 	inc	dptr
      005C3F F0               [24] 2286 	movx	@dptr,a
                                   2287 ;	tmk_core/protocol/ch555/usb_ak820.c:278: if (D0SetupLen > 2) D0SetupLen = 2;
      005C40 90 06 87         [24] 2288 	mov	dptr,#_D0SetupLen
      005C43 E0               [24] 2289 	movx	a,@dptr
      005C44 FB               [12] 2290 	mov	r3,a
      005C45 A3               [24] 2291 	inc	dptr
      005C46 E0               [24] 2292 	movx	a,@dptr
      005C47 FC               [12] 2293 	mov	r4,a
      005C48 C3               [12] 2294 	clr	c
      005C49 74 02            [12] 2295 	mov	a,#0x02
      005C4B 9B               [12] 2296 	subb	a,r3
      005C4C E4               [12] 2297 	clr	a
      005C4D 9C               [12] 2298 	subb	a,r4
      005C4E D0 04            [24] 2299 	pop	ar4
      005C50 D0 03            [24] 2300 	pop	ar3
      005C52 50 7A            [24] 2301 	jnc	00161$
                                   2302 ;	free result
      005C54 90 06 87         [24] 2303 	mov	dptr,#_D0SetupLen
      005C57 74 02            [12] 2304 	mov	a,#0x02
      005C59 F0               [24] 2305 	movx	@dptr,a
      005C5A E4               [12] 2306 	clr	a
      005C5B A3               [24] 2307 	inc	dptr
      005C5C F0               [24] 2308 	movx	@dptr,a
      005C5D 80 6F            [24] 2309 	sjmp	00161$
      005C5F                       2310 00141$:
                                   2311 ;	tmk_core/protocol/ch555/usb_ak820.c:279: } else if (value == 0x0300 && index == RAW_INTERFACE) {
      005C5F B8 00 69         [24] 2312 	cjne	r0,#0x00,00137$
      005C62 B9 03 66         [24] 2313 	cjne	r1,#0x03,00137$
      005C65 BB 01 63         [24] 2314 	cjne	r3,#0x01,00137$
      005C68 BC 00 60         [24] 2315 	cjne	r4,#0x00,00137$
                                   2316 ;	tmk_core/protocol/ch555/usb_ak820.c:282: pD0_EP0_BUF[0] = 'A';
      005C6B 90 10 00         [24] 2317 	mov	dptr,#0x1000
      005C6E 74 41            [12] 2318 	mov	a,#0x41
      005C70 F0               [24] 2319 	movx	@dptr,a
                                   2320 ;	tmk_core/protocol/ch555/usb_ak820.c:283: pD0_EP0_BUF[1] = 'K';
      005C71 A3               [24] 2321 	inc	dptr
      005C72 74 4B            [12] 2322 	mov	a,#0x4b
      005C74 F0               [24] 2323 	movx	@dptr,a
                                   2324 ;	tmk_core/protocol/ch555/usb_ak820.c:284: pD0_EP0_BUF[2] = 'B';
      005C75 A3               [24] 2325 	inc	dptr
      005C76 74 42            [12] 2326 	mov	a,#0x42
      005C78 F0               [24] 2327 	movx	@dptr,a
                                   2328 ;	tmk_core/protocol/ch555/usb_ak820.c:285: pD0_EP0_BUF[3] = 'T';
      005C79 A3               [24] 2329 	inc	dptr
      005C7A 74 54            [12] 2330 	mov	a,#0x54
      005C7C F0               [24] 2331 	movx	@dptr,a
                                   2332 ;	tmk_core/protocol/ch555/usb_ak820.c:286: pD0_EP0_BUF[4] = 1;
      005C7D A3               [24] 2333 	inc	dptr
      005C7E 74 01            [12] 2334 	mov	a,#0x01
      005C80 F0               [24] 2335 	movx	@dptr,a
                                   2336 ;	tmk_core/protocol/ch555/usb_ak820.c:287: pD0_EP0_BUF[5] = ak820_boot_stage;
      005C81 90 06 92         [24] 2337 	mov	dptr,#_ak820_boot_stage
      005C84 E0               [24] 2338 	movx	a,@dptr
      005C85 90 10 05         [24] 2339 	mov	dptr,#0x1005
      005C88 F0               [24] 2340 	movx	@dptr,a
                                   2341 ;	tmk_core/protocol/ch555/usb_ak820.c:288: pD0_EP0_BUF[6] = ak820_main_heartbeat;
      005C89 90 06 93         [24] 2342 	mov	dptr,#_ak820_main_heartbeat
      005C8C E0               [24] 2343 	movx	a,@dptr
      005C8D 90 10 06         [24] 2344 	mov	dptr,#0x1006
      005C90 F0               [24] 2345 	movx	@dptr,a
                                   2346 ;	tmk_core/protocol/ch555/usb_ak820.c:289: pD0_EP0_BUF[7] = (USB_EnumStatus ? 1 : 0) | (USB_SleepStatus & 2);
      005C91 90 06 8D         [24] 2347 	mov	dptr,#_USB_EnumStatus
      005C94 E0               [24] 2348 	movx	a,@dptr
      005C95 60 02            [24] 2349 	jz	00322$
      005C97 74 01            [12] 2350 	mov	a,#0x01
      005C99                       2351 00322$:
      005C99 F9               [12] 2352 	mov	r1,a
      005C9A 90 06 8E         [24] 2353 	mov	dptr,#_USB_SleepStatus
      005C9D E0               [24] 2354 	movx	a,@dptr
      005C9E 54 02            [12] 2355 	anl	a,#0x02
      005CA0 F8               [12] 2356 	mov	r0,a
      005CA1 E9               [12] 2357 	mov	a,r1
      005CA2 42 00            [12] 2358 	orl	ar0,a
      005CA4 90 10 07         [24] 2359 	mov	dptr,#0x1007
      005CA7 E8               [12] 2360 	mov	a,r0
      005CA8 F0               [24] 2361 	movx	@dptr,a
                                   2362 ;	tmk_core/protocol/ch555/usb_ak820.c:290: length = 0;
      005CA9 90 06 EF         [24] 2363 	mov	dptr,#_control_setup_length_10000_286
      005CAC E4               [12] 2364 	clr	a
      005CAD F0               [24] 2365 	movx	@dptr,a
      005CAE A3               [24] 2366 	inc	dptr
      005CAF F0               [24] 2367 	movx	@dptr,a
                                   2368 ;	tmk_core/protocol/ch555/usb_ak820.c:291: if (D0SetupLen > 8) D0SetupLen = 8;
      005CB0 90 06 87         [24] 2369 	mov	dptr,#_D0SetupLen
      005CB3 E0               [24] 2370 	movx	a,@dptr
      005CB4 F8               [12] 2371 	mov	r0,a
      005CB5 A3               [24] 2372 	inc	dptr
      005CB6 E0               [24] 2373 	movx	a,@dptr
      005CB7 F9               [12] 2374 	mov	r1,a
      005CB8 C3               [12] 2375 	clr	c
      005CB9 74 08            [12] 2376 	mov	a,#0x08
      005CBB 98               [12] 2377 	subb	a,r0
      005CBC E4               [12] 2378 	clr	a
      005CBD 99               [12] 2379 	subb	a,r1
      005CBE 50 0E            [24] 2380 	jnc	00161$
                                   2381 ;	free result
      005CC0 90 06 87         [24] 2382 	mov	dptr,#_D0SetupLen
      005CC3 74 08            [12] 2383 	mov	a,#0x08
      005CC5 F0               [24] 2384 	movx	@dptr,a
      005CC6 E4               [12] 2385 	clr	a
      005CC7 A3               [24] 2386 	inc	dptr
      005CC8 F0               [24] 2387 	movx	@dptr,a
      005CC9 80 03            [24] 2388 	sjmp	00161$
      005CCB                       2389 00137$:
                                   2390 ;	tmk_core/protocol/ch555/usb_ak820.c:292: } else { control_stall(); return; }
      005CCB 02 54 AD         [24] 2391 	ljmp	_control_stall
      005CCE                       2392 00161$:
                                   2393 ;	tmk_core/protocol/ch555/usb_ak820.c:293: if (length) {
      005CCE 90 06 EF         [24] 2394 	mov	dptr,#_control_setup_length_10000_286
      005CD1 E0               [24] 2395 	movx	a,@dptr
      005CD2 F5 26            [12] 2396 	mov	_control_setup_sloc2_1_0,a
      005CD4 A3               [24] 2397 	inc	dptr
      005CD5 E0               [24] 2398 	movx	a,@dptr
      005CD6 F5 27            [12] 2399 	mov	(_control_setup_sloc2_1_0 + 1),a
      005CD8 E5 26            [12] 2400 	mov	a,_control_setup_sloc2_1_0
      005CDA 45 27            [12] 2401 	orl	a,(_control_setup_sloc2_1_0 + 1)
      005CDC 60 60            [24] 2402 	jz	00171$
                                   2403 ;	tmk_core/protocol/ch555/usb_ak820.c:294: if (D0SetupLen > length) D0SetupLen = length;
      005CDE 90 06 87         [24] 2404 	mov	dptr,#_D0SetupLen
      005CE1 E0               [24] 2405 	movx	a,@dptr
      005CE2 F8               [12] 2406 	mov	r0,a
      005CE3 A3               [24] 2407 	inc	dptr
      005CE4 E0               [24] 2408 	movx	a,@dptr
      005CE5 F9               [12] 2409 	mov	r1,a
      005CE6 C3               [12] 2410 	clr	c
      005CE7 E5 26            [12] 2411 	mov	a,_control_setup_sloc2_1_0
      005CE9 98               [12] 2412 	subb	a,r0
      005CEA E5 27            [12] 2413 	mov	a,(_control_setup_sloc2_1_0 + 1)
      005CEC 99               [12] 2414 	subb	a,r1
      005CED 50 0A            [24] 2415 	jnc	00555$
                                   2416 ;	free result
      005CEF 90 06 87         [24] 2417 	mov	dptr,#_D0SetupLen
      005CF2 E5 26            [12] 2418 	mov	a,_control_setup_sloc2_1_0
      005CF4 F0               [24] 2419 	movx	@dptr,a
      005CF5 E5 27            [12] 2420 	mov	a,(_control_setup_sloc2_1_0 + 1)
      005CF7 A3               [24] 2421 	inc	dptr
      005CF8 F0               [24] 2422 	movx	@dptr,a
                                   2423 ;	tmk_core/protocol/ch555/usb_ak820.c:295: for (i = 0; i < D0SetupLen; ++i) pD0_EP0_BUF[i] = input_snapshot[offset + i];
      005CF9                       2424 00555$:
      005CF9 90 06 F1         [24] 2425 	mov	dptr,#_control_setup_offset_10000_286
      005CFC E0               [24] 2426 	movx	a,@dptr
      005CFD F5 28            [12] 2427 	mov	_control_setup_sloc3_1_0,a
      005CFF 75 26 00         [24] 2428 	mov	_control_setup_sloc2_1_0,#0x00
      005D02                       2429 00296$:
      005D02 90 06 87         [24] 2430 	mov	dptr,#_D0SetupLen
      005D05 E0               [24] 2431 	movx	a,@dptr
      005D06 F5 24            [12] 2432 	mov	_control_setup_sloc1_1_0,a
      005D08 A3               [24] 2433 	inc	dptr
      005D09 E0               [24] 2434 	movx	a,@dptr
      005D0A F5 25            [12] 2435 	mov	(_control_setup_sloc1_1_0 + 1),a
      005D0C A8 26            [24] 2436 	mov	r0,_control_setup_sloc2_1_0
      005D0E 79 00            [12] 2437 	mov	r1,#0x00
      005D10 C3               [12] 2438 	clr	c
      005D11 E8               [12] 2439 	mov	a,r0
      005D12 95 24            [12] 2440 	subb	a,_control_setup_sloc1_1_0
      005D14 E9               [12] 2441 	mov	a,r1
      005D15 95 25            [12] 2442 	subb	a,(_control_setup_sloc1_1_0 + 1)
      005D17 50 44            [24] 2443 	jnc	00172$
      005D19 85 26 24         [24] 2444 	mov	_control_setup_sloc1_1_0,_control_setup_sloc2_1_0
      005D1C 74 10            [12] 2445 	mov	a,#0x10
      005D1E 24 00            [12] 2446 	add	a, #0x00
      005D20 F5 25            [12] 2447 	mov	(_control_setup_sloc1_1_0 + 1),a
      005D22 E5 26            [12] 2448 	mov	a,_control_setup_sloc2_1_0
      005D24 25 28            [12] 2449 	add	a, _control_setup_sloc3_1_0
      005D26 24 B7            [12] 2450 	add	a, #_input_snapshot
      005D28 F5 82            [12] 2451 	mov	dpl,a
      005D2A E4               [12] 2452 	clr	a
      005D2B 34 06            [12] 2453 	addc	a,#(_input_snapshot >> 8)
      005D2D F5 83            [12] 2454 	mov	dph,a
      005D2F E0               [24] 2455 	movx	a,@dptr
      005D30 85 24 82         [24] 2456 	mov	dpl,_control_setup_sloc1_1_0
      005D33 85 25 83         [24] 2457 	mov	dph,(_control_setup_sloc1_1_0 + 1)
      005D36 F0               [24] 2458 	movx	@dptr,a
      005D37 E5 26            [12] 2459 	mov	a,_control_setup_sloc2_1_0
      005D39 04               [12] 2460 	inc	a
      005D3A F5 26            [12] 2461 	mov	_control_setup_sloc2_1_0,a
      005D3C 80 C4            [24] 2462 	sjmp	00296$
      005D3E                       2463 00171$:
                                   2464 ;	tmk_core/protocol/ch555/usb_ak820.c:296: } else if (index == RAW_INTERFACE && D0SetupLen > RAW_EPSIZE) D0SetupLen = RAW_EPSIZE;
      005D3E BB 01 1C         [24] 2465 	cjne	r3,#0x01,00172$
      005D41 BC 00 19         [24] 2466 	cjne	r4,#0x00,00172$
      005D44 90 06 87         [24] 2467 	mov	dptr,#_D0SetupLen
      005D47 E0               [24] 2468 	movx	a,@dptr
      005D48 F8               [12] 2469 	mov	r0,a
      005D49 A3               [24] 2470 	inc	dptr
      005D4A E0               [24] 2471 	movx	a,@dptr
      005D4B F9               [12] 2472 	mov	r1,a
      005D4C C3               [12] 2473 	clr	c
      005D4D 74 20            [12] 2474 	mov	a,#0x20
      005D4F 98               [12] 2475 	subb	a,r0
      005D50 E4               [12] 2476 	clr	a
      005D51 99               [12] 2477 	subb	a,r1
      005D52 50 09            [24] 2478 	jnc	00172$
                                   2479 ;	free result
      005D54 90 06 87         [24] 2480 	mov	dptr,#_D0SetupLen
      005D57 74 20            [12] 2481 	mov	a,#0x20
      005D59 F0               [24] 2482 	movx	@dptr,a
      005D5A E4               [12] 2483 	clr	a
      005D5B A3               [24] 2484 	inc	dptr
      005D5C F0               [24] 2485 	movx	@dptr,a
      005D5D                       2486 00172$:
                                   2487 ;	tmk_core/protocol/ch555/usb_ak820.c:297: D0_EP0T_L = D0SetupLen;
      005D5D 90 06 87         [24] 2488 	mov	dptr,#_D0SetupLen
      005D60 E0               [24] 2489 	movx	a,@dptr
      005D61 90 22 08         [24] 2490 	mov	dptr,#0x2208
      005D64 F0               [24] 2491 	movx	@dptr,a
                                   2492 ;	tmk_core/protocol/ch555/usb_ak820.c:298: control_phase = CTRL_STATUS_OUT;
      005D65 90 06 E5         [24] 2493 	mov	dptr,#_control_phase
      005D68 74 02            [12] 2494 	mov	a,#0x02
      005D6A F0               [24] 2495 	movx	@dptr,a
      005D6B 02 5F 18         [24] 2496 	ljmp	00287$
      005D6E                       2497 00228$:
                                   2498 ;	tmk_core/protocol/ch555/usb_ak820.c:299: } else if (type == 0x21 && D0SetupReqCode == HID_SET_REPORT && D0UsbConfig) {
      005D6E E4               [12] 2499 	clr	a
      005D6F BF 21 01         [24] 2500 	cjne	r7,#0x21,01422$
      005D72 04               [12] 2501 	inc	a
      005D73                       2502 01422$:
      005D73 FF               [12] 2503 	mov	r7,a
      005D74 70 03            [24] 2504 	jnz	01424$
      005D76 02 5E 18         [24] 2505 	ljmp	00223$
      005D79                       2506 01424$:
      005D79 90 06 86         [24] 2507 	mov	dptr,#_D0SetupReqCode
      005D7C E0               [24] 2508 	movx	a,@dptr
      005D7D F9               [12] 2509 	mov	r1,a
      005D7E B9 09 02         [24] 2510 	cjne	r1,#0x09,01425$
      005D81 80 03            [24] 2511 	sjmp	01426$
      005D83                       2512 01425$:
      005D83 02 5E 18         [24] 2513 	ljmp	00223$
      005D86                       2514 01426$:
      005D86 90 06 8C         [24] 2515 	mov	dptr,#_D0UsbConfig
      005D89 E0               [24] 2516 	movx	a,@dptr
      005D8A 70 03            [24] 2517 	jnz	01427$
      005D8C 02 5E 18         [24] 2518 	ljmp	00223$
      005D8F                       2519 01427$:
                                   2520 ;	tmk_core/protocol/ch555/usb_ak820.c:300: if (index == RAW_INTERFACE && value == 0x0200 && D0SetupLen == RAW_EPSIZE && raw_state == RAW_IDLE) {
      005D8F BB 01 2D         [24] 2521 	cjne	r3,#0x01,00184$
      005D92 BC 00 2A         [24] 2522 	cjne	r4,#0x00,00184$
      005D95 8D 00            [24] 2523 	mov	ar0,r5
      005D97 8E 01            [24] 2524 	mov	ar1,r6
      005D99 B8 00 23         [24] 2525 	cjne	r0,#0x00,00184$
      005D9C B9 02 20         [24] 2526 	cjne	r1,#0x02,00184$
      005D9F 90 06 87         [24] 2527 	mov	dptr,#_D0SetupLen
      005DA2 E0               [24] 2528 	movx	a,@dptr
      005DA3 F8               [12] 2529 	mov	r0,a
      005DA4 A3               [24] 2530 	inc	dptr
      005DA5 E0               [24] 2531 	movx	a,@dptr
      005DA6 F9               [12] 2532 	mov	r1,a
      005DA7 B8 20 15         [24] 2533 	cjne	r0,#0x20,00184$
      005DAA B9 00 12         [24] 2534 	cjne	r1,#0x00,00184$
      005DAD 90 06 94         [24] 2535 	mov	dptr,#_raw_state
      005DB0 E0               [24] 2536 	movx	a,@dptr
      005DB1 70 0C            [24] 2537 	jnz	00184$
                                   2538 ;	tmk_core/protocol/ch555/usb_ak820.c:301: raw_state = RAW_RX;
      005DB3 90 06 94         [24] 2539 	mov	dptr,#_raw_state
      005DB6 74 01            [12] 2540 	mov	a,#0x01
      005DB8 F0               [24] 2541 	movx	@dptr,a
                                   2542 ;	tmk_core/protocol/ch555/usb_ak820.c:302: output_kind = OUTPUT_RAW;
      005DB9 90 06 E6         [24] 2543 	mov	dptr,#_output_kind
      005DBC F0               [24] 2544 	movx	@dptr,a
      005DBD 80 52            [24] 2545 	sjmp	00185$
      005DBF                       2546 00184$:
                                   2547 ;	tmk_core/protocol/ch555/usb_ak820.c:303: } else if (index == KEYBOARD_INTERFACE && value == 0x0200 && D0SetupLen == 1) {
      005DBF EB               [12] 2548 	mov	a,r3
      005DC0 4C               [12] 2549 	orl	a,r4
      005DC1 70 20            [24] 2550 	jnz	00179$
      005DC3 8D 00            [24] 2551 	mov	ar0,r5
      005DC5 8E 01            [24] 2552 	mov	ar1,r6
      005DC7 B8 00 19         [24] 2553 	cjne	r0,#0x00,00179$
      005DCA B9 02 16         [24] 2554 	cjne	r1,#0x02,00179$
      005DCD 90 06 87         [24] 2555 	mov	dptr,#_D0SetupLen
      005DD0 E0               [24] 2556 	movx	a,@dptr
      005DD1 F8               [12] 2557 	mov	r0,a
      005DD2 A3               [24] 2558 	inc	dptr
      005DD3 E0               [24] 2559 	movx	a,@dptr
      005DD4 F9               [12] 2560 	mov	r1,a
      005DD5 B8 01 0B         [24] 2561 	cjne	r0,#0x01,00179$
      005DD8 B9 00 08         [24] 2562 	cjne	r1,#0x00,00179$
                                   2563 ;	tmk_core/protocol/ch555/usb_ak820.c:304: output_kind = OUTPUT_LED;
      005DDB 90 06 E6         [24] 2564 	mov	dptr,#_output_kind
      005DDE 74 02            [12] 2565 	mov	a,#0x02
      005DE0 F0               [24] 2566 	movx	@dptr,a
      005DE1 80 2E            [24] 2567 	sjmp	00185$
      005DE3                       2568 00179$:
                                   2569 ;	tmk_core/protocol/ch555/usb_ak820.c:306: } else if (index == SHARED_INTERFACE && value == (0x0200 | REPORT_ID_NKRO) && D0SetupLen == 2) {
      005DE3 BB 02 28         [24] 2570 	cjne	r3,#0x02,00174$
      005DE6 BC 00 25         [24] 2571 	cjne	r4,#0x00,00174$
      005DE9 8D 00            [24] 2572 	mov	ar0,r5
      005DEB 8E 01            [24] 2573 	mov	ar1,r6
      005DED B8 06 1E         [24] 2574 	cjne	r0,#0x06,00174$
      005DF0 B9 02 1B         [24] 2575 	cjne	r1,#0x02,00174$
      005DF3 90 06 87         [24] 2576 	mov	dptr,#_D0SetupLen
      005DF6 E0               [24] 2577 	movx	a,@dptr
      005DF7 F8               [12] 2578 	mov	r0,a
      005DF8 A3               [24] 2579 	inc	dptr
      005DF9 E0               [24] 2580 	movx	a,@dptr
      005DFA F9               [12] 2581 	mov	r1,a
      005DFB B8 02 10         [24] 2582 	cjne	r0,#0x02,00174$
      005DFE B9 00 0D         [24] 2583 	cjne	r1,#0x00,00174$
                                   2584 ;	tmk_core/protocol/ch555/usb_ak820.c:307: output_kind = OUTPUT_SHARED_LED;
      005E01 90 06 E6         [24] 2585 	mov	dptr,#_output_kind
      005E04 74 03            [12] 2586 	mov	a,#0x03
      005E06 F0               [24] 2587 	movx	@dptr,a
                                   2588 ;	tmk_core/protocol/ch555/usb_ak820.c:308: output_report_id = REPORT_ID_NKRO;
      005E07 90 06 E7         [24] 2589 	mov	dptr,#_output_report_id
      005E0A 23               [12] 2590 	rl	a
      005E0B F0               [24] 2591 	movx	@dptr,a
      005E0C 80 03            [24] 2592 	sjmp	00185$
      005E0E                       2593 00174$:
                                   2594 ;	tmk_core/protocol/ch555/usb_ak820.c:310: } else { control_stall(); return; }
      005E0E 02 54 AD         [24] 2595 	ljmp	_control_stall
      005E11                       2596 00185$:
                                   2597 ;	tmk_core/protocol/ch555/usb_ak820.c:311: control_phase = CTRL_DATA_OUT;
      005E11 90 06 E5         [24] 2598 	mov	dptr,#_control_phase
      005E14 74 04            [12] 2599 	mov	a,#0x04
      005E16 F0               [24] 2600 	movx	@dptr,a
                                   2601 ;	tmk_core/protocol/ch555/usb_ak820.c:312: return; /* OUT data must arrive before status-IN becomes ACK */
      005E17 22               [24] 2602 	ret
      005E18                       2603 00223$:
                                   2604 ;	tmk_core/protocol/ch555/usb_ak820.c:313: } else if (index == KEYBOARD_INTERFACE && D0UsbConfig && type == 0x21 && D0SetupReqCode == DEF_USB_SET_PROTOCOL && !D0SetupLen && value <= 1) {
      005E18 EB               [12] 2605 	mov	a,r3
      005E19 4C               [12] 2606 	orl	a,r4
      005E1A 70 3B            [24] 2607 	jnz	00215$
      005E1C 90 06 8C         [24] 2608 	mov	dptr,#_D0UsbConfig
      005E1F E0               [24] 2609 	movx	a,@dptr
      005E20 60 35            [24] 2610 	jz	00215$
      005E22 EF               [12] 2611 	mov	a,r7
      005E23 60 32            [24] 2612 	jz	00215$
      005E25 90 06 86         [24] 2613 	mov	dptr,#_D0SetupReqCode
      005E28 E0               [24] 2614 	movx	a,@dptr
      005E29 F9               [12] 2615 	mov	r1,a
      005E2A B9 0B 2A         [24] 2616 	cjne	r1,#0x0b,00215$
      005E2D 90 06 87         [24] 2617 	mov	dptr,#_D0SetupLen
      005E30 E0               [24] 2618 	movx	a,@dptr
      005E31 F8               [12] 2619 	mov	r0,a
      005E32 A3               [24] 2620 	inc	dptr
      005E33 E0               [24] 2621 	movx	a,@dptr
      005E34 48               [12] 2622 	orl	a,r0
      005E35 70 20            [24] 2623 	jnz	00215$
      005E37 8D 00            [24] 2624 	mov	ar0,r5
      005E39 8E 01            [24] 2625 	mov	ar1,r6
      005E3B C3               [12] 2626 	clr	c
      005E3C 74 01            [12] 2627 	mov	a,#0x01
      005E3E 98               [12] 2628 	subb	a,r0
      005E3F E4               [12] 2629 	clr	a
      005E40 99               [12] 2630 	subb	a,r1
      005E41 40 14            [24] 2631 	jc	00215$
                                   2632 ;	free result
                                   2633 ;	tmk_core/protocol/ch555/usb_ak820.c:314: keyboard_protocol = value;
      005E43 90 0B 9E         [24] 2634 	mov	dptr,#_keyboard_protocol
      005E46 ED               [12] 2635 	mov	a,r5
      005E47 F0               [24] 2636 	movx	@dptr,a
                                   2637 ;	tmk_core/protocol/ch555/usb_ak820.c:315: keyboard_reset = 1;
      005E48 90 06 B6         [24] 2638 	mov	dptr,#_keyboard_reset
      005E4B 74 01            [12] 2639 	mov	a,#0x01
      005E4D F0               [24] 2640 	movx	@dptr,a
                                   2641 ;	tmk_core/protocol/ch555/usb_ak820.c:316: control_phase = CTRL_STATUS_IN;
      005E4E 90 06 E5         [24] 2642 	mov	dptr,#_control_phase
      005E51 74 03            [12] 2643 	mov	a,#0x03
      005E53 F0               [24] 2644 	movx	@dptr,a
      005E54 02 5F 18         [24] 2645 	ljmp	00287$
      005E57                       2646 00215$:
                                   2647 ;	tmk_core/protocol/ch555/usb_ak820.c:317: } else if (index == KEYBOARD_INTERFACE && D0UsbConfig && type == 0xa1 && D0SetupReqCode == DEF_USB_GET_PROTOCOL && !value && D0SetupLen == 1) {
      005E57 EB               [12] 2648 	mov	a,r3
      005E58 4C               [12] 2649 	orl	a,r4
      005E59 70 39            [24] 2650 	jnz	00207$
      005E5B 90 06 8C         [24] 2651 	mov	dptr,#_D0UsbConfig
      005E5E E0               [24] 2652 	movx	a,@dptr
      005E5F 60 33            [24] 2653 	jz	00207$
      005E61 EA               [12] 2654 	mov	a,r2
      005E62 60 30            [24] 2655 	jz	00207$
      005E64 90 06 86         [24] 2656 	mov	dptr,#_D0SetupReqCode
      005E67 E0               [24] 2657 	movx	a,@dptr
      005E68 F9               [12] 2658 	mov	r1,a
      005E69 B9 03 28         [24] 2659 	cjne	r1,#0x03,00207$
      005E6C ED               [12] 2660 	mov	a,r5
      005E6D 4E               [12] 2661 	orl	a,r6
      005E6E 70 24            [24] 2662 	jnz	00207$
      005E70 90 06 87         [24] 2663 	mov	dptr,#_D0SetupLen
      005E73 E0               [24] 2664 	movx	a,@dptr
      005E74 F8               [12] 2665 	mov	r0,a
      005E75 A3               [24] 2666 	inc	dptr
      005E76 E0               [24] 2667 	movx	a,@dptr
      005E77 F9               [12] 2668 	mov	r1,a
      005E78 B8 01 19         [24] 2669 	cjne	r0,#0x01,00207$
      005E7B B9 00 16         [24] 2670 	cjne	r1,#0x00,00207$
                                   2671 ;	tmk_core/protocol/ch555/usb_ak820.c:318: pD0_EP0_BUF[0] = keyboard_protocol;
      005E7E 90 0B 9E         [24] 2672 	mov	dptr,#_keyboard_protocol
      005E81 E0               [24] 2673 	movx	a,@dptr
      005E82 90 10 00         [24] 2674 	mov	dptr,#0x1000
      005E85 F0               [24] 2675 	movx	@dptr,a
                                   2676 ;	tmk_core/protocol/ch555/usb_ak820.c:319: D0_EP0T_L = 1;
      005E86 90 22 08         [24] 2677 	mov	dptr,#0x2208
      005E89 74 01            [12] 2678 	mov	a,#0x01
      005E8B F0               [24] 2679 	movx	@dptr,a
                                   2680 ;	tmk_core/protocol/ch555/usb_ak820.c:320: control_phase = CTRL_STATUS_OUT;
      005E8C 90 06 E5         [24] 2681 	mov	dptr,#_control_phase
      005E8F 04               [12] 2682 	inc	a
      005E90 F0               [24] 2683 	movx	@dptr,a
      005E91 02 5F 18         [24] 2684 	ljmp	00287$
      005E94                       2685 00207$:
                                   2686 ;	tmk_core/protocol/ch555/usb_ak820.c:321: } else if (index < TOTAL_INTERFACES && D0UsbConfig && type == 0x21 && D0SetupReqCode == DEF_USB_SET_IDLE && !D0SetupLen) {
      005E94 C3               [12] 2687 	clr	c
      005E95 EB               [12] 2688 	mov	a,r3
      005E96 94 03            [12] 2689 	subb	a,#0x03
      005E98 EC               [12] 2690 	mov	a,r4
      005E99 94 00            [12] 2691 	subb	a,#0x00
      005E9B E4               [12] 2692 	clr	a
      005E9C 33               [12] 2693 	rlc	a
      005E9D F9               [12] 2694 	mov	r1,a
      005E9E 60 2C            [24] 2695 	jz	00200$
      005EA0 90 06 8C         [24] 2696 	mov	dptr,#_D0UsbConfig
      005EA3 E0               [24] 2697 	movx	a,@dptr
      005EA4 60 26            [24] 2698 	jz	00200$
      005EA6 EF               [12] 2699 	mov	a,r7
      005EA7 60 23            [24] 2700 	jz	00200$
      005EA9 90 06 86         [24] 2701 	mov	dptr,#_D0SetupReqCode
      005EAC E0               [24] 2702 	movx	a,@dptr
      005EAD FF               [12] 2703 	mov	r7,a
      005EAE BF 0A 1B         [24] 2704 	cjne	r7,#0x0a,00200$
      005EB1 90 06 87         [24] 2705 	mov	dptr,#_D0SetupLen
      005EB4 E0               [24] 2706 	movx	a,@dptr
      005EB5 F8               [12] 2707 	mov	r0,a
      005EB6 A3               [24] 2708 	inc	dptr
      005EB7 E0               [24] 2709 	movx	a,@dptr
      005EB8 48               [12] 2710 	orl	a,r0
      005EB9 70 11            [24] 2711 	jnz	00200$
                                   2712 ;	tmk_core/protocol/ch555/usb_ak820.c:322: if (index == KEYBOARD_INTERFACE) keyboard_idle = value >> 8;
      005EBB EB               [12] 2713 	mov	a,r3
      005EBC 4C               [12] 2714 	orl	a,r4
      005EBD 70 05            [24] 2715 	jnz	00190$
      005EBF 90 05 5B         [24] 2716 	mov	dptr,#_keyboard_idle
      005EC2 EE               [12] 2717 	mov	a,r6
      005EC3 F0               [24] 2718 	movx	@dptr,a
      005EC4                       2719 00190$:
                                   2720 ;	tmk_core/protocol/ch555/usb_ak820.c:323: control_phase = CTRL_STATUS_IN;
      005EC4 90 06 E5         [24] 2721 	mov	dptr,#_control_phase
      005EC7 74 03            [12] 2722 	mov	a,#0x03
      005EC9 F0               [24] 2723 	movx	@dptr,a
      005ECA 80 4C            [24] 2724 	sjmp	00287$
      005ECC                       2725 00200$:
                                   2726 ;	tmk_core/protocol/ch555/usb_ak820.c:324: } else if (index < TOTAL_INTERFACES && D0UsbConfig && type == 0xa1 && D0SetupReqCode == DEF_USB_GET_IDLE && !(value >> 8) && D0SetupLen == 1) {
      005ECC E9               [12] 2727 	mov	a,r1
      005ECD 60 46            [24] 2728 	jz	00192$
      005ECF 90 06 8C         [24] 2729 	mov	dptr,#_D0UsbConfig
      005ED2 E0               [24] 2730 	movx	a,@dptr
      005ED3 60 40            [24] 2731 	jz	00192$
      005ED5 EA               [12] 2732 	mov	a,r2
      005ED6 60 3D            [24] 2733 	jz	00192$
      005ED8 90 06 86         [24] 2734 	mov	dptr,#_D0SetupReqCode
      005EDB E0               [24] 2735 	movx	a,@dptr
      005EDC FF               [12] 2736 	mov	r7,a
      005EDD BF 02 35         [24] 2737 	cjne	r7,#0x02,00192$
      005EE0 8E 05            [24] 2738 	mov	ar5,r6
      005EE2 7E 00            [12] 2739 	mov	r6,#0x00
      005EE4 ED               [12] 2740 	mov	a,r5
      005EE5 4E               [12] 2741 	orl	a,r6
      005EE6 70 2D            [24] 2742 	jnz	00192$
      005EE8 90 06 87         [24] 2743 	mov	dptr,#_D0SetupLen
      005EEB E0               [24] 2744 	movx	a,@dptr
      005EEC FE               [12] 2745 	mov	r6,a
      005EED A3               [24] 2746 	inc	dptr
      005EEE E0               [24] 2747 	movx	a,@dptr
      005EEF FF               [12] 2748 	mov	r7,a
      005EF0 BE 01 22         [24] 2749 	cjne	r6,#0x01,00192$
      005EF3 BF 00 1F         [24] 2750 	cjne	r7,#0x00,00192$
                                   2751 ;	tmk_core/protocol/ch555/usb_ak820.c:325: pD0_EP0_BUF[0] = index == KEYBOARD_INTERFACE ? keyboard_idle : 0;
      005EF6 EB               [12] 2752 	mov	a,r3
      005EF7 4C               [12] 2753 	orl	a,r4
      005EF8 70 07            [24] 2754 	jnz	00324$
      005EFA 90 05 5B         [24] 2755 	mov	dptr,#_keyboard_idle
      005EFD E0               [24] 2756 	movx	a,@dptr
      005EFE FF               [12] 2757 	mov	r7,a
      005EFF 80 02            [24] 2758 	sjmp	00325$
      005F01                       2759 00324$:
      005F01 7F 00            [12] 2760 	mov	r7,#0x00
      005F03                       2761 00325$:
      005F03 90 10 00         [24] 2762 	mov	dptr,#0x1000
      005F06 EF               [12] 2763 	mov	a,r7
      005F07 F0               [24] 2764 	movx	@dptr,a
                                   2765 ;	tmk_core/protocol/ch555/usb_ak820.c:326: D0_EP0T_L = 1;
      005F08 90 22 08         [24] 2766 	mov	dptr,#0x2208
      005F0B 74 01            [12] 2767 	mov	a,#0x01
      005F0D F0               [24] 2768 	movx	@dptr,a
                                   2769 ;	tmk_core/protocol/ch555/usb_ak820.c:327: control_phase = CTRL_STATUS_OUT;
      005F0E 90 06 E5         [24] 2770 	mov	dptr,#_control_phase
      005F11 04               [12] 2771 	inc	a
      005F12 F0               [24] 2772 	movx	@dptr,a
      005F13 80 03            [24] 2773 	sjmp	00287$
      005F15                       2774 00192$:
                                   2775 ;	tmk_core/protocol/ch555/usb_ak820.c:328: } else { control_stall(); return; }
      005F15 02 54 AD         [24] 2776 	ljmp	_control_stall
      005F18                       2777 00287$:
                                   2778 ;	tmk_core/protocol/ch555/usb_ak820.c:329: D0_EP0RES = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
      005F18 90 22 00         [24] 2779 	mov	dptr,#0x2200
      005F1B 74 C0            [12] 2780 	mov	a,#0xc0
      005F1D F0               [24] 2781 	movx	@dptr,a
                                   2782 ;	tmk_core/protocol/ch555/usb_ak820.c:330: }
      005F1E 22               [24] 2783 	ret
                                   2784 ;------------------------------------------------------------
                                   2785 ;Allocation info for local variables in function 'control_out'
                                   2786 ;------------------------------------------------------------
                                   2787 ;i             Allocated with name '_control_out_i_10000_360'
                                   2788 ;------------------------------------------------------------
                                   2789 ;	tmk_core/protocol/ch555/usb_ak820.c:332: static void control_out(void) {
                                   2790 ;	-----------------------------------------
                                   2791 ;	 function control_out
                                   2792 ;	-----------------------------------------
      005F1F                       2793 _control_out:
                                   2794 ;	tmk_core/protocol/ch555/usb_ak820.c:334: if (!(D0_STATUS & bUXS_TOG_OK)) return; /* duplicate OUT is not a new request */
      005F1F 90 22 0F         [24] 2795 	mov	dptr,#0x220f
      005F22 E0               [24] 2796 	movx	a,@dptr
      005F23 20 E6 01         [24] 2797 	jb	acc.6,00102$
      005F26 22               [24] 2798 	ret
      005F27                       2799 00102$:
                                   2800 ;	tmk_core/protocol/ch555/usb_ak820.c:335: if (control_phase == CTRL_STATUS_OUT && D0_RX_LEN == 0) {
      005F27 90 06 E5         [24] 2801 	mov	dptr,#_control_phase
      005F2A E0               [24] 2802 	movx	a,@dptr
      005F2B FF               [12] 2803 	mov	r7,a
      005F2C BF 02 12         [24] 2804 	cjne	r7,#0x02,00104$
      005F2F 90 22 0E         [24] 2805 	mov	dptr,#0x220e
      005F32 E0               [24] 2806 	movx	a,@dptr
      005F33 70 0C            [24] 2807 	jnz	00104$
                                   2808 ;	tmk_core/protocol/ch555/usb_ak820.c:336: control_phase = CTRL_IDLE;
      005F35 90 06 E5         [24] 2809 	mov	dptr,#_control_phase
      005F38 E4               [12] 2810 	clr	a
      005F39 F0               [24] 2811 	movx	@dptr,a
                                   2812 ;	tmk_core/protocol/ch555/usb_ak820.c:337: D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
      005F3A 90 22 00         [24] 2813 	mov	dptr,#0x2200
      005F3D 74 02            [12] 2814 	mov	a,#0x02
      005F3F F0               [24] 2815 	movx	@dptr,a
                                   2816 ;	tmk_core/protocol/ch555/usb_ak820.c:338: return;
      005F40 22               [24] 2817 	ret
      005F41                       2818 00104$:
                                   2819 ;	tmk_core/protocol/ch555/usb_ak820.c:340: if (control_phase != CTRL_DATA_OUT || D0_RX_LEN != D0SetupLen) { control_stall(); return; }
      005F41 BF 04 19         [24] 2820 	cjne	r7,#0x04,00106$
      005F44 90 22 0E         [24] 2821 	mov	dptr,#0x220e
      005F47 E0               [24] 2822 	movx	a,@dptr
      005F48 FF               [12] 2823 	mov	r7,a
      005F49 90 06 87         [24] 2824 	mov	dptr,#_D0SetupLen
      005F4C E0               [24] 2825 	movx	a,@dptr
      005F4D FD               [12] 2826 	mov	r5,a
      005F4E A3               [24] 2827 	inc	dptr
      005F4F E0               [24] 2828 	movx	a,@dptr
      005F50 FE               [12] 2829 	mov	r6,a
      005F51 7C 00            [12] 2830 	mov	r4,#0x00
      005F53 EF               [12] 2831 	mov	a,r7
      005F54 B5 05 06         [24] 2832 	cjne	a,ar5,00209$
      005F57 EC               [12] 2833 	mov	a,r4
      005F58 B5 06 02         [24] 2834 	cjne	a,ar6,00209$
      005F5B 80 03            [24] 2835 	sjmp	00107$
      005F5D                       2836 00209$:
      005F5D                       2837 00106$:
      005F5D 02 54 AD         [24] 2838 	ljmp	_control_stall
      005F60                       2839 00107$:
                                   2840 ;	tmk_core/protocol/ch555/usb_ak820.c:341: if (output_kind == OUTPUT_RAW && raw_state == RAW_RX) {
      005F60 90 06 E6         [24] 2841 	mov	dptr,#_output_kind
      005F63 E0               [24] 2842 	movx	a,@dptr
      005F64 FF               [12] 2843 	mov	r7,a
      005F65 BF 01 2E         [24] 2844 	cjne	r7,#0x01,00118$
      005F68 90 06 94         [24] 2845 	mov	dptr,#_raw_state
      005F6B E0               [24] 2846 	movx	a,@dptr
      005F6C FE               [12] 2847 	mov	r6,a
      005F6D BE 01 26         [24] 2848 	cjne	r6,#0x01,00118$
                                   2849 ;	tmk_core/protocol/ch555/usb_ak820.c:342: for (i = 0; i < RAW_EPSIZE; ++i) raw_buffer[i] = pD0_EP0_BUF[i];
      005F70 7E 00            [12] 2850 	mov	r6,#0x00
      005F72                       2851 00121$:
      005F72 EE               [12] 2852 	mov	a,r6
      005F73 24 95            [12] 2853 	add	a, #_raw_buffer
      005F75 FC               [12] 2854 	mov	r4,a
      005F76 E4               [12] 2855 	clr	a
      005F77 34 06            [12] 2856 	addc	a, #(_raw_buffer >> 8)
      005F79 FD               [12] 2857 	mov	r5,a
      005F7A 8E 82            [24] 2858 	mov	dpl,r6
      005F7C 74 10            [12] 2859 	mov	a,#0x10
      005F7E 24 00            [12] 2860 	add	a, #0x00
      005F80 F5 83            [12] 2861 	mov	dph,a
      005F82 E0               [24] 2862 	movx	a,@dptr
      005F83 8C 82            [24] 2863 	mov	dpl,r4
      005F85 8D 83            [24] 2864 	mov	dph,r5
      005F87 F0               [24] 2865 	movx	@dptr,a
      005F88 0E               [12] 2866 	inc	r6
      005F89 BE 20 00         [24] 2867 	cjne	r6,#0x20,00214$
      005F8C                       2868 00214$:
      005F8C 40 E4            [24] 2869 	jc	00121$
                                   2870 ;	tmk_core/protocol/ch555/usb_ak820.c:343: raw_state = RAW_READY; /* publish only after the entire packet is copied */
      005F8E 90 06 94         [24] 2871 	mov	dptr,#_raw_state
      005F91 74 02            [12] 2872 	mov	a,#0x02
      005F93 F0               [24] 2873 	movx	@dptr,a
      005F94 80 2B            [24] 2874 	sjmp	00119$
      005F96                       2875 00118$:
                                   2876 ;	tmk_core/protocol/ch555/usb_ak820.c:344: } else if (output_kind == OUTPUT_LED) {
      005F96 BF 02 0A         [24] 2877 	cjne	r7,#0x02,00115$
                                   2878 ;	tmk_core/protocol/ch555/usb_ak820.c:345: KB_USB_SetReport = pD0_EP0_BUF[0];
      005F99 90 10 00         [24] 2879 	mov	dptr,#0x1000
      005F9C E0               [24] 2880 	movx	a,@dptr
      005F9D 90 06 91         [24] 2881 	mov	dptr,#_KB_USB_SetReport
      005FA0 F0               [24] 2882 	movx	@dptr,a
      005FA1 80 1E            [24] 2883 	sjmp	00119$
      005FA3                       2884 00115$:
                                   2885 ;	tmk_core/protocol/ch555/usb_ak820.c:346: } else if (output_kind == OUTPUT_SHARED_LED && pD0_EP0_BUF[0] == output_report_id) {
      005FA3 BF 03 18         [24] 2886 	cjne	r7,#0x03,00111$
      005FA6 90 10 00         [24] 2887 	mov	dptr,#0x1000
      005FA9 E0               [24] 2888 	movx	a,@dptr
      005FAA FF               [12] 2889 	mov	r7,a
      005FAB 90 06 E7         [24] 2890 	mov	dptr,#_output_report_id
      005FAE E0               [24] 2891 	movx	a,@dptr
      005FAF FE               [12] 2892 	mov	r6,a
      005FB0 EF               [12] 2893 	mov	a,r7
      005FB1 B5 06 0A         [24] 2894 	cjne	a,ar6,00111$
                                   2895 ;	tmk_core/protocol/ch555/usb_ak820.c:347: KB_USB_SetReport = pD0_EP0_BUF[1];
      005FB4 90 10 01         [24] 2896 	mov	dptr,#0x1001
      005FB7 E0               [24] 2897 	movx	a,@dptr
      005FB8 90 06 91         [24] 2898 	mov	dptr,#_KB_USB_SetReport
      005FBB F0               [24] 2899 	movx	@dptr,a
      005FBC 80 03            [24] 2900 	sjmp	00119$
      005FBE                       2901 00111$:
                                   2902 ;	tmk_core/protocol/ch555/usb_ak820.c:348: } else { control_stall(); return; }
      005FBE 02 54 AD         [24] 2903 	ljmp	_control_stall
      005FC1                       2904 00119$:
                                   2905 ;	tmk_core/protocol/ch555/usb_ak820.c:349: output_kind = OUTPUT_NONE;
      005FC1 90 06 E6         [24] 2906 	mov	dptr,#_output_kind
      005FC4 E4               [12] 2907 	clr	a
      005FC5 F0               [24] 2908 	movx	@dptr,a
                                   2909 ;	tmk_core/protocol/ch555/usb_ak820.c:350: D0SetupLen = 0;
      005FC6 90 06 87         [24] 2910 	mov	dptr,#_D0SetupLen
      005FC9 F0               [24] 2911 	movx	@dptr,a
      005FCA A3               [24] 2912 	inc	dptr
      005FCB F0               [24] 2913 	movx	@dptr,a
                                   2914 ;	tmk_core/protocol/ch555/usb_ak820.c:351: control_phase = CTRL_STATUS_IN;
      005FCC 90 06 E5         [24] 2915 	mov	dptr,#_control_phase
      005FCF 74 03            [12] 2916 	mov	a,#0x03
      005FD1 F0               [24] 2917 	movx	@dptr,a
                                   2918 ;	tmk_core/protocol/ch555/usb_ak820.c:352: D0_EP0T_L = 0;
      005FD2 90 22 08         [24] 2919 	mov	dptr,#0x2208
      005FD5 E4               [12] 2920 	clr	a
      005FD6 F0               [24] 2921 	movx	@dptr,a
                                   2922 ;	tmk_core/protocol/ch555/usb_ak820.c:353: D0_EP0RES = bUEP_T_TOG | UEP_R_RES_NAK | UEP_T_RES_ACK;
      005FD7 F5 82            [12] 2923 	mov	dpl,a
      005FD9 74 48            [12] 2924 	mov	a,#0x48
      005FDB F0               [24] 2925 	movx	@dptr,a
                                   2926 ;	tmk_core/protocol/ch555/usb_ak820.c:354: }
      005FDC 22               [24] 2927 	ret
                                   2928 ;------------------------------------------------------------
                                   2929 ;Allocation info for local variables in function 'control_in'
                                   2930 ;------------------------------------------------------------
                                   2931 ;	tmk_core/protocol/ch555/usb_ak820.c:356: static void control_in(void) {
                                   2932 ;	-----------------------------------------
                                   2933 ;	 function control_in
                                   2934 ;	-----------------------------------------
      005FDD                       2935 _control_in:
                                   2936 ;	tmk_core/protocol/ch555/usb_ak820.c:357: if (control_phase == CTRL_DATA_IN) {
      005FDD 90 06 E5         [24] 2937 	mov	dptr,#_control_phase
      005FE0 E0               [24] 2938 	movx	a,@dptr
      005FE1 FF               [12] 2939 	mov	r7,a
      005FE2 BF 01 22         [24] 2940 	cjne	r7,#0x01,00109$
                                   2941 ;	tmk_core/protocol/ch555/usb_ak820.c:358: if (D0SetupLen || control_zlp) {
      005FE5 90 06 87         [24] 2942 	mov	dptr,#_D0SetupLen
      005FE8 E0               [24] 2943 	movx	a,@dptr
      005FE9 FD               [12] 2944 	mov	r5,a
      005FEA A3               [24] 2945 	inc	dptr
      005FEB E0               [24] 2946 	movx	a,@dptr
      005FEC 4D               [12] 2947 	orl	a,r5
      005FED 70 06            [24] 2948 	jnz	00101$
      005FEF 90 06 E8         [24] 2949 	mov	dptr,#_control_zlp
      005FF2 E0               [24] 2950 	movx	a,@dptr
      005FF3 60 0A            [24] 2951 	jz	00102$
      005FF5                       2952 00101$:
                                   2953 ;	tmk_core/protocol/ch555/usb_ak820.c:359: D0_EP0RES ^= bUEP_T_TOG;
      005FF5 90 22 00         [24] 2954 	mov	dptr,#0x2200
      005FF8 E0               [24] 2955 	movx	a,@dptr
      005FF9 64 40            [12] 2956 	xrl	a,#0x40
      005FFB F0               [24] 2957 	movx	@dptr,a
                                   2958 ;	tmk_core/protocol/ch555/usb_ak820.c:360: control_next();
                                   2959 ;	tmk_core/protocol/ch555/usb_ak820.c:361: return;
      005FFC 02 54 CF         [24] 2960 	ljmp	_control_next
      005FFF                       2961 00102$:
                                   2962 ;	tmk_core/protocol/ch555/usb_ak820.c:363: control_phase = CTRL_STATUS_OUT;
      005FFF 90 06 E5         [24] 2963 	mov	dptr,#_control_phase
      006002 74 02            [12] 2964 	mov	a,#0x02
      006004 F0               [24] 2965 	movx	@dptr,a
      006005 80 18            [24] 2966 	sjmp	00110$
      006007                       2967 00109$:
                                   2968 ;	tmk_core/protocol/ch555/usb_ak820.c:364: } else if (control_phase == CTRL_STATUS_IN) {
      006007 BF 03 15         [24] 2969 	cjne	r7,#0x03,00110$
                                   2970 ;	tmk_core/protocol/ch555/usb_ak820.c:365: if (D0SetupReqCode == USB_SET_ADDRESS) D0_ADDR = D0SetupLen;
      00600A 90 06 86         [24] 2971 	mov	dptr,#_D0SetupReqCode
      00600D E0               [24] 2972 	movx	a,@dptr
      00600E FF               [12] 2973 	mov	r7,a
      00600F BF 05 08         [24] 2974 	cjne	r7,#0x05,00105$
      006012 90 06 87         [24] 2975 	mov	dptr,#_D0SetupLen
      006015 E0               [24] 2976 	movx	a,@dptr
      006016 90 22 07         [24] 2977 	mov	dptr,#0x2207
      006019 F0               [24] 2978 	movx	@dptr,a
      00601A                       2979 00105$:
                                   2980 ;	tmk_core/protocol/ch555/usb_ak820.c:366: control_phase = CTRL_IDLE;
      00601A 90 06 E5         [24] 2981 	mov	dptr,#_control_phase
      00601D E4               [12] 2982 	clr	a
      00601E F0               [24] 2983 	movx	@dptr,a
      00601F                       2984 00110$:
                                   2985 ;	tmk_core/protocol/ch555/usb_ak820.c:368: D0_EP0RES = bUEP_R_TOG | UEP_R_RES_ACK | UEP_T_RES_NAK;
      00601F 90 22 00         [24] 2986 	mov	dptr,#0x2200
      006022 74 82            [12] 2987 	mov	a,#0x82
      006024 F0               [24] 2988 	movx	@dptr,a
                                   2989 ;	tmk_core/protocol/ch555/usb_ak820.c:369: }
      006025 22               [24] 2990 	ret
                                   2991 ;------------------------------------------------------------
                                   2992 ;Allocation info for local variables in function 'USB_DeviceInterrupt'
                                   2993 ;------------------------------------------------------------
                                   2994 ;status        Allocated with name '_USB_DeviceInterrupt_status_10000_384'
                                   2995 ;endpoint      Allocated with name '_USB_DeviceInterrupt_endpoint_10000_384'
                                   2996 ;------------------------------------------------------------
                                   2997 ;	tmk_core/protocol/ch555/usb_ak820.c:371: void USB_DeviceInterrupt(void) {
                                   2998 ;	-----------------------------------------
                                   2999 ;	 function USB_DeviceInterrupt
                                   3000 ;	-----------------------------------------
      006026                       3001 _USB_DeviceInterrupt:
                                   3002 ;	tmk_core/protocol/ch555/usb_ak820.c:374: do {
      006026                       3003 00129$:
                                   3004 ;	tmk_core/protocol/ch555/usb_ak820.c:376: if (USB_IF & bUX_IF_BUS_RST) {
      006026 90 22 3D         [24] 3005 	mov	dptr,#0x223d
      006029 E0               [24] 3006 	movx	a,@dptr
      00602A 30 E0 4B         [24] 3007 	jnb	acc.0,00127$
                                   3008 ;	tmk_core/protocol/ch555/usb_ak820.c:377: endpoints_reset();
      00602D 12 54 56         [24] 3009 	lcall	_endpoints_reset
                                   3010 ;	tmk_core/protocol/ch555/usb_ak820.c:378: D0_ADDR = 0;
      006030 90 22 07         [24] 3011 	mov	dptr,#0x2207
      006033 E4               [12] 3012 	clr	a
      006034 F0               [24] 3013 	movx	@dptr,a
                                   3014 ;	tmk_core/protocol/ch555/usb_ak820.c:379: D0UsbConfig = USB_EnumStatus = USB_SleepStatus = 0;
      006035 90 06 8E         [24] 3015 	mov	dptr,#_USB_SleepStatus
      006038 F0               [24] 3016 	movx	@dptr,a
      006039 90 06 8D         [24] 3017 	mov	dptr,#_USB_EnumStatus
      00603C F0               [24] 3018 	movx	@dptr,a
      00603D 90 06 8C         [24] 3019 	mov	dptr,#_D0UsbConfig
      006040 F0               [24] 3020 	movx	@dptr,a
                                   3021 ;	tmk_core/protocol/ch555/usb_ak820.c:380: KB_USB_SetReport = 0;
      006041 90 06 91         [24] 3022 	mov	dptr,#_KB_USB_SetReport
      006044 F0               [24] 3023 	movx	@dptr,a
                                   3024 ;	tmk_core/protocol/ch555/usb_ak820.c:381: keyboard_protocol = 1;
      006045 90 0B 9E         [24] 3025 	mov	dptr,#_keyboard_protocol
      006048 04               [12] 3026 	inc	a
      006049 F0               [24] 3027 	movx	@dptr,a
                                   3028 ;	tmk_core/protocol/ch555/usb_ak820.c:382: keyboard_idle = 0;
      00604A 90 05 5B         [24] 3029 	mov	dptr,#_keyboard_idle
      00604D E4               [12] 3030 	clr	a
      00604E F0               [24] 3031 	movx	@dptr,a
                                   3032 ;	tmk_core/protocol/ch555/usb_ak820.c:383: keyboard_reset = 1;
      00604F 90 06 B6         [24] 3033 	mov	dptr,#_keyboard_reset
      006052 04               [12] 3034 	inc	a
      006053 F0               [24] 3035 	movx	@dptr,a
                                   3036 ;	tmk_core/protocol/ch555/usb_ak820.c:384: D0SetupReqCode = 0xff;
      006054 90 06 86         [24] 3037 	mov	dptr,#_D0SetupReqCode
      006057 74 FF            [12] 3038 	mov	a,#0xff
      006059 F0               [24] 3039 	movx	@dptr,a
                                   3040 ;	tmk_core/protocol/ch555/usb_ak820.c:385: D0SetupLen = 0;
      00605A 90 06 87         [24] 3041 	mov	dptr,#_D0SetupLen
      00605D E4               [12] 3042 	clr	a
      00605E F0               [24] 3043 	movx	@dptr,a
      00605F A3               [24] 3044 	inc	dptr
      006060 F0               [24] 3045 	movx	@dptr,a
                                   3046 ;	tmk_core/protocol/ch555/usb_ak820.c:386: control_phase = CTRL_IDLE;
      006061 90 06 E5         [24] 3047 	mov	dptr,#_control_phase
      006064 F0               [24] 3048 	movx	@dptr,a
                                   3049 ;	tmk_core/protocol/ch555/usb_ak820.c:387: D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
      006065 90 22 00         [24] 3050 	mov	dptr,#0x2200
      006068 74 02            [12] 3051 	mov	a,#0x02
      00606A F0               [24] 3052 	movx	@dptr,a
                                   3053 ;	tmk_core/protocol/ch555/usb_ak820.c:388: ACK_TRANSFER();
      00606B 90 22 0F         [24] 3054 	mov	dptr,#0x220f
      00606E E4               [12] 3055 	clr	a
      00606F F0               [24] 3056 	movx	@dptr,a
                                   3057 ;	tmk_core/protocol/ch555/usb_ak820.c:389: ACK_RESET();
      006070 90 22 3D         [24] 3058 	mov	dptr,#0x223d
      006073 04               [12] 3059 	inc	a
      006074 F0               [24] 3060 	movx	@dptr,a
      006075 02 61 0B         [24] 3061 	ljmp	00130$
      006078                       3062 00127$:
                                   3063 ;	tmk_core/protocol/ch555/usb_ak820.c:390: } else if (USB_IF & bUX_IF_D0_TRANS) {
      006078 90 22 3D         [24] 3064 	mov	dptr,#0x223d
      00607B E0               [24] 3065 	movx	a,@dptr
      00607C 30 E5 60         [24] 3066 	jnb	acc.5,00124$
                                   3067 ;	tmk_core/protocol/ch555/usb_ak820.c:391: status = D0_STATUS;
      00607F 90 22 0F         [24] 3068 	mov	dptr,#0x220f
      006082 E0               [24] 3069 	movx	a,@dptr
      006083 FF               [12] 3070 	mov	r7,a
                                   3071 ;	tmk_core/protocol/ch555/usb_ak820.c:392: endpoint = status & MASK_UXS_ENDP;
      006084 74 07            [12] 3072 	mov	a,#0x07
      006086 5F               [12] 3073 	anl	a,r7
      006087 FE               [12] 3074 	mov	r6,a
                                   3075 ;	tmk_core/protocol/ch555/usb_ak820.c:396: if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_OUT && !endpoint) {
      006088 EF               [12] 3076 	mov	a,r7
      006089 54 18            [12] 3077 	anl	a,#0x18
      00608B 70 08            [24] 3078 	jnz	00115$
      00608D EE               [12] 3079 	mov	a,r6
      00608E 70 05            [24] 3080 	jnz	00115$
                                   3081 ;	tmk_core/protocol/ch555/usb_ak820.c:397: control_out();
      006090 12 5F 1F         [24] 3082 	lcall	_control_out
      006093 80 43            [24] 3083 	sjmp	00116$
      006095                       3084 00115$:
                                   3085 ;	tmk_core/protocol/ch555/usb_ak820.c:398: } else if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_IN) {
      006095 8F 05            [24] 3086 	mov	ar5,r7
      006097 74 18            [12] 3087 	mov	a,#0x18
      006099 5D               [12] 3088 	anl	a,r5
      00609A FC               [12] 3089 	mov	r4,a
      00609B BC 10 2D         [24] 3090 	cjne	r4,#0x10,00112$
                                   3091 ;	tmk_core/protocol/ch555/usb_ak820.c:399: if (!endpoint) control_in();
      00609E EE               [12] 3092 	mov	a,r6
      00609F 70 05            [24] 3093 	jnz	00106$
      0060A1 12 5F DD         [24] 3094 	lcall	_control_in
      0060A4 80 32            [24] 3095 	sjmp	00116$
      0060A6                       3096 00106$:
                                   3097 ;	tmk_core/protocol/ch555/usb_ak820.c:400: else if (endpoint <= 3) {
      0060A6 EE               [12] 3098 	mov	a,r6
      0060A7 24 FC            [12] 3099 	add	a,#0xff - 0x03
      0060A9 40 2D            [24] 3100 	jc	00116$
                                   3101 ;	free result
                                   3102 ;	tmk_core/protocol/ch555/usb_ak820.c:401: EP_RESPONSE(endpoint) = (EP_RESPONSE(endpoint) & ~MASK_UEP_X_RES) | UEP_X_RES_NAK;
      0060AB 8E 04            [24] 3103 	mov	ar4,r6
      0060AD 7B 00            [12] 3104 	mov	r3,#0x00
      0060AF 74 22            [12] 3105 	mov	a,#0x22
      0060B1 2B               [12] 3106 	add	a, r3
      0060B2 FB               [12] 3107 	mov	r3,a
      0060B3 8C 82            [24] 3108 	mov	dpl,r4
      0060B5 8B 83            [24] 3109 	mov	dph,r3
      0060B7 E0               [24] 3110 	movx	a,@dptr
      0060B8 FA               [12] 3111 	mov	r2,a
      0060B9 74 FC            [12] 3112 	mov	a,#0xfc
      0060BB 5A               [12] 3113 	anl	a,r2
      0060BC 44 02            [12] 3114 	orl	a,#0x02
      0060BE 8C 82            [24] 3115 	mov	dpl,r4
      0060C0 8B 83            [24] 3116 	mov	dph,r3
      0060C2 F0               [24] 3117 	movx	@dptr,a
                                   3118 ;	tmk_core/protocol/ch555/usb_ak820.c:402: if (endpoint == RAW_IN_EPNUM) raw_complete();
      0060C3 BE 03 12         [24] 3119 	cjne	r6,#0x03,00116$
      0060C6 12 54 39         [24] 3120 	lcall	_raw_complete
      0060C9 80 0D            [24] 3121 	sjmp	00116$
      0060CB                       3122 00112$:
                                   3123 ;	tmk_core/protocol/ch555/usb_ak820.c:404: } else if ((status & MASK_UXS_TOKEN) == UXS_TOKEN_FREE && (status & bUXS_SETUP_ACT)) {
      0060CB 53 05 18         [24] 3124 	anl	ar5,#0x18
      0060CE BD 18 07         [24] 3125 	cjne	r5,#0x18,00116$
      0060D1 EF               [12] 3126 	mov	a,r7
      0060D2 30 E5 03         [24] 3127 	jnb	acc.5,00116$
                                   3128 ;	tmk_core/protocol/ch555/usb_ak820.c:405: control_setup();
      0060D5 12 57 14         [24] 3129 	lcall	_control_setup
      0060D8                       3130 00116$:
                                   3131 ;	tmk_core/protocol/ch555/usb_ak820.c:407: ACK_TRANSFER();
      0060D8 90 22 0F         [24] 3132 	mov	dptr,#0x220f
      0060DB E4               [12] 3133 	clr	a
      0060DC F0               [24] 3134 	movx	@dptr,a
      0060DD 80 2C            [24] 3135 	sjmp	00130$
      0060DF                       3136 00124$:
                                   3137 ;	tmk_core/protocol/ch555/usb_ak820.c:408: } else if (USB_IF & bUX_IF_SUSPEND) {
      0060DF 90 22 3D         [24] 3138 	mov	dptr,#0x223d
      0060E2 E0               [24] 3139 	movx	a,@dptr
      0060E3 30 E2 25         [24] 3140 	jnb	acc.2,00130$
                                   3141 ;	tmk_core/protocol/ch555/usb_ak820.c:409: if (USB_IF & bUX_SUSPEND) USB_SleepStatus |= 2;
      0060E6 90 22 3D         [24] 3142 	mov	dptr,#0x223d
      0060E9 E0               [24] 3143 	movx	a,@dptr
      0060EA 30 E3 0A         [24] 3144 	jnb	acc.3,00119$
      0060ED 90 06 8E         [24] 3145 	mov	dptr,#_USB_SleepStatus
      0060F0 E0               [24] 3146 	movx	a,@dptr
      0060F1 43 E0 02         [24] 3147 	orl	acc,#0x02
      0060F4 F0               [24] 3148 	movx	@dptr,a
      0060F5 80 0E            [24] 3149 	sjmp	00120$
      0060F7                       3150 00119$:
                                   3151 ;	tmk_core/protocol/ch555/usb_ak820.c:411: USB_SleepStatus &= ~2;
      0060F7 90 06 8E         [24] 3152 	mov	dptr,#_USB_SleepStatus
      0060FA E0               [24] 3153 	movx	a,@dptr
      0060FB 53 E0 FD         [24] 3154 	anl	acc,#0xfd
      0060FE F0               [24] 3155 	movx	@dptr,a
                                   3156 ;	tmk_core/protocol/ch555/usb_ak820.c:412: keyboard_reset = 1;
      0060FF 90 06 B6         [24] 3157 	mov	dptr,#_keyboard_reset
      006102 74 01            [12] 3158 	mov	a,#0x01
      006104 F0               [24] 3159 	movx	@dptr,a
      006105                       3160 00120$:
                                   3161 ;	tmk_core/protocol/ch555/usb_ak820.c:414: ACK_SUSPEND();
      006105 90 22 3D         [24] 3162 	mov	dptr,#0x223d
      006108 74 04            [12] 3163 	mov	a,#0x04
      00610A F0               [24] 3164 	movx	@dptr,a
      00610B                       3165 00130$:
                                   3166 ;	tmk_core/protocol/ch555/usb_ak820.c:416: } while (USB_IF & (bUX_IF_BUS_RST | bUX_IF_D0_TRANS | bUX_IF_SUSPEND));
      00610B 90 22 3D         [24] 3167 	mov	dptr,#0x223d
      00610E E0               [24] 3168 	movx	a,@dptr
      00610F 54 25            [12] 3169 	anl	a,#0x25
      006111 60 03            [24] 3170 	jz	00242$
      006113 02 60 26         [24] 3171 	ljmp	00129$
      006116                       3172 00242$:
                                   3173 ;	tmk_core/protocol/ch555/usb_ak820.c:417: }
      006116 22               [24] 3174 	ret
                                   3175 ;------------------------------------------------------------
                                   3176 ;Allocation info for local variables in function 'USB_Device_Init'
                                   3177 ;------------------------------------------------------------
                                   3178 ;	tmk_core/protocol/ch555/usb_ak820.c:420: void USB_Device_Init(void) {
                                   3179 ;	-----------------------------------------
                                   3180 ;	 function USB_Device_Init
                                   3181 ;	-----------------------------------------
      006117                       3182 _USB_Device_Init:
                                   3183 ;	tmk_core/protocol/ch555/usb_ak820.c:421: IE_USB = 0;
                                   3184 ;	assignBit
      006117 C2 E9            [12] 3185 	clr	_IE_USB
                                   3186 ;	tmk_core/protocol/ch555/usb_ak820.c:422: USB_CTRL = 0;
      006119 90 22 3C         [24] 3187 	mov	dptr,#0x223c
      00611C E4               [12] 3188 	clr	a
      00611D F0               [24] 3189 	movx	@dptr,a
                                   3190 ;	tmk_core/protocol/ch555/usb_ak820.c:423: raw_state = RAW_IDLE;
      00611E 90 06 94         [24] 3191 	mov	dptr,#_raw_state
      006121 F0               [24] 3192 	movx	@dptr,a
                                   3193 ;	tmk_core/protocol/ch555/usb_ak820.c:424: endpoints_reset();
      006122 12 54 56         [24] 3194 	lcall	_endpoints_reset
                                   3195 ;	tmk_core/protocol/ch555/usb_ak820.c:425: D0_ADDR = D0UsbConfig = USB_EnumStatus = USB_SleepStatus = 0;
      006125 90 06 8E         [24] 3196 	mov	dptr,#_USB_SleepStatus
      006128 E4               [12] 3197 	clr	a
      006129 F0               [24] 3198 	movx	@dptr,a
      00612A 90 06 8D         [24] 3199 	mov	dptr,#_USB_EnumStatus
      00612D F0               [24] 3200 	movx	@dptr,a
      00612E 90 06 8C         [24] 3201 	mov	dptr,#_D0UsbConfig
      006131 F0               [24] 3202 	movx	@dptr,a
      006132 90 22 07         [24] 3203 	mov	dptr,#0x2207
      006135 F0               [24] 3204 	movx	@dptr,a
                                   3205 ;	tmk_core/protocol/ch555/usb_ak820.c:426: KB_USB_SetReport = KB_USB_UpStatus = MCU_Sleep_Operate = 0;
      006136 90 06 8F         [24] 3206 	mov	dptr,#_MCU_Sleep_Operate
      006139 F0               [24] 3207 	movx	@dptr,a
      00613A 90 06 90         [24] 3208 	mov	dptr,#_KB_USB_UpStatus
      00613D F0               [24] 3209 	movx	@dptr,a
      00613E 90 06 91         [24] 3210 	mov	dptr,#_KB_USB_SetReport
      006141 F0               [24] 3211 	movx	@dptr,a
                                   3212 ;	tmk_core/protocol/ch555/usb_ak820.c:427: keyboard_protocol = 1;
      006142 90 0B 9E         [24] 3213 	mov	dptr,#_keyboard_protocol
      006145 04               [12] 3214 	inc	a
      006146 F0               [24] 3215 	movx	@dptr,a
                                   3216 ;	tmk_core/protocol/ch555/usb_ak820.c:428: keyboard_idle = 0;
      006147 90 05 5B         [24] 3217 	mov	dptr,#_keyboard_idle
      00614A E4               [12] 3218 	clr	a
      00614B F0               [24] 3219 	movx	@dptr,a
                                   3220 ;	tmk_core/protocol/ch555/usb_ak820.c:429: keyboard_reset = 0;
      00614C 90 06 B6         [24] 3221 	mov	dptr,#_keyboard_reset
      00614F F0               [24] 3222 	movx	@dptr,a
                                   3223 ;	tmk_core/protocol/ch555/usb_ak820.c:430: control_phase = CTRL_IDLE;
      006150 90 06 E5         [24] 3224 	mov	dptr,#_control_phase
      006153 F0               [24] 3225 	movx	@dptr,a
                                   3226 ;	tmk_core/protocol/ch555/usb_ak820.c:431: D0SetupReqCode = 0xff;
      006154 90 06 86         [24] 3227 	mov	dptr,#_D0SetupReqCode
      006157 14               [12] 3228 	dec	a
      006158 F0               [24] 3229 	movx	@dptr,a
                                   3230 ;	tmk_core/protocol/ch555/usb_ak820.c:432: D0SetupLen = 0;
      006159 90 06 87         [24] 3231 	mov	dptr,#_D0SetupLen
      00615C E4               [12] 3232 	clr	a
      00615D F0               [24] 3233 	movx	@dptr,a
      00615E A3               [24] 3234 	inc	dptr
      00615F F0               [24] 3235 	movx	@dptr,a
                                   3236 ;	tmk_core/protocol/ch555/usb_ak820.c:433: D0_EP0RES = UEP_R_RES_ACK | UEP_T_RES_NAK;
      006160 90 22 00         [24] 3237 	mov	dptr,#0x2200
      006163 74 02            [12] 3238 	mov	a,#0x02
      006165 F0               [24] 3239 	movx	@dptr,a
                                   3240 ;	tmk_core/protocol/ch555/usb_ak820.c:434: HB_ADDR = 0x7f;
      006166 90 22 37         [24] 3241 	mov	dptr,#0x2237
      006169 74 7F            [12] 3242 	mov	a,#0x7f
      00616B F0               [24] 3243 	movx	@dptr,a
                                   3244 ;	tmk_core/protocol/ch555/usb_ak820.c:435: ACK_ALL();
      00616C 90 22 3D         [24] 3245 	mov	dptr,#0x223d
      00616F 74 FF            [12] 3246 	mov	a,#0xff
      006171 F0               [24] 3247 	movx	@dptr,a
                                   3248 ;	tmk_core/protocol/ch555/usb_ak820.c:436: USB_IE = bUX_IE_SUSPEND | bUX_IE_TRANSFER | bUX_IE_BUS_RST;
      006172 90 22 3B         [24] 3249 	mov	dptr,#0x223b
      006175 74 07            [12] 3250 	mov	a,#0x07
      006177 F0               [24] 3251 	movx	@dptr,a
                                   3252 ;	tmk_core/protocol/ch555/usb_ak820.c:437: USB_CTRL = bUX_DP_PU_EN;
      006178 A3               [24] 3253 	inc	dptr
      006179 74 80            [12] 3254 	mov	a,#0x80
      00617B F0               [24] 3255 	movx	@dptr,a
                                   3256 ;	tmk_core/protocol/ch555/usb_ak820.c:438: IE_USB = 1;
                                   3257 ;	assignBit
      00617C D2 E9            [12] 3258 	setb	_IE_USB
                                   3259 ;	tmk_core/protocol/ch555/usb_ak820.c:439: }
      00617E 22               [24] 3260 	ret
                                   3261 ;------------------------------------------------------------
                                   3262 ;Allocation info for local variables in function 'USB_WakeUp_PC'
                                   3263 ;------------------------------------------------------------
                                   3264 ;saved         Allocated with name '_USB_WakeUp_PC_saved_10000_407'
                                   3265 ;i             Allocated with name '_USB_WakeUp_PC_i_30000_410'
                                   3266 ;------------------------------------------------------------
                                   3267 ;	tmk_core/protocol/ch555/usb_ak820.c:441: void USB_WakeUp_PC(void) {
                                   3268 ;	-----------------------------------------
                                   3269 ;	 function USB_WakeUp_PC
                                   3270 ;	-----------------------------------------
      00617F                       3271 _USB_WakeUp_PC:
                                   3272 ;	tmk_core/protocol/ch555/usb_ak820.c:443: if (USB_SleepStatus != 3) return;
      00617F 90 06 8E         [24] 3273 	mov	dptr,#_USB_SleepStatus
      006182 E0               [24] 3274 	movx	a,@dptr
      006183 FF               [12] 3275 	mov	r7,a
      006184 BF 03 22         [24] 3276 	cjne	r7,#0x03,00110$
                                   3277 ;	tmk_core/protocol/ch555/usb_ak820.c:444: saved = USB_CTRL;
      006187 90 22 3C         [24] 3278 	mov	dptr,#0x223c
      00618A E0               [24] 3279 	movx	a,@dptr
      00618B FF               [12] 3280 	mov	r7,a
                                   3281 ;	tmk_core/protocol/ch555/usb_ak820.c:445: USB_CTRL ^= bUX_DP_PU_EN | bUX_DM_PU_EN;
      00618C E0               [24] 3282 	movx	a,@dptr
      00618D FE               [12] 3283 	mov	r6,a
      00618E 63 06 C0         [24] 3284 	xrl	ar6,#0xc0
      006191 90 22 3C         [24] 3285 	mov	dptr,#0x223c
      006194 EE               [12] 3286 	mov	a,r6
      006195 F0               [24] 3287 	movx	@dptr,a
                                   3288 ;	tmk_core/protocol/ch555/usb_ak820.c:446: wait_ms(10);
      006196 7E 0A            [12] 3289 	mov	r6,#0x0a
      006198                       3290 00108$:
      006198 EE               [12] 3291 	mov	a,r6
      006199 60 09            [24] 3292 	jz	00105$
      00619B 90 00 01         [24] 3293 	mov	dptr,#0x0001
      00619E 12 52 7D         [24] 3294 	lcall	_mDelaymS
      0061A1 1E               [12] 3295 	dec	r6
      0061A2 80 F4            [24] 3296 	sjmp	00108$
      0061A4                       3297 00105$:
                                   3298 ;	tmk_core/protocol/ch555/usb_ak820.c:447: USB_CTRL = saved;
      0061A4 90 22 3C         [24] 3299 	mov	dptr,#0x223c
      0061A7 EF               [12] 3300 	mov	a,r7
      0061A8 F0               [24] 3301 	movx	@dptr,a
      0061A9                       3302 00110$:
                                   3303 ;	tmk_core/protocol/ch555/usb_ak820.c:448: }
      0061A9 22               [24] 3304 	ret
                                   3305 ;------------------------------------------------------------
                                   3306 ;Allocation info for local variables in function 'ak820_usb_send'
                                   3307 ;------------------------------------------------------------
                                   3308 ;sloc1         Allocated with name '_ak820_usb_send_sloc1_1_0'
                                   3309 ;sloc2         Allocated with name '_ak820_usb_send_sloc2_1_0'
                                   3310 ;sloc3         Allocated with name '_ak820_usb_send_sloc3_1_0'
                                   3311 ;report        Allocated with name '_ak820_usb_send_PARM_2'
                                   3312 ;length        Allocated with name '_ak820_usb_send_PARM_3'
                                   3313 ;endpoint      Allocated with name '_ak820_usb_send_endpoint_10000_412'
                                   3314 ;saved_ea      Allocated with name '_ak820_usb_send_saved_ea_10000_413'
                                   3315 ;i             Allocated with name '_ak820_usb_send_i_10000_413'
                                   3316 ;timeout       Allocated with name '_ak820_usb_send_timeout_10000_413'
                                   3317 ;offset        Allocated with name '_ak820_usb_send_offset_10000_413'
                                   3318 ;report_id     Allocated with name '_ak820_usb_send_report_id_10000_413'
                                   3319 ;i             Allocated with name '_ak820_usb_send_i_30000_425'
                                   3320 ;------------------------------------------------------------
                                   3321 ;	tmk_core/protocol/ch555/usb_ak820.c:450: bool ak820_usb_send(uint8_t endpoint, const uint8_t __xdata *report, uint8_t length) {
                                   3322 ;	-----------------------------------------
                                   3323 ;	 function ak820_usb_send
                                   3324 ;	-----------------------------------------
      0061AA                       3325 _ak820_usb_send:
      0061AA E5 82            [12] 3326 	mov	a,dpl
      0061AC 90 06 F5         [24] 3327 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      0061AF F0               [24] 3328 	movx	@dptr,a
                                   3329 ;	tmk_core/protocol/ch555/usb_ak820.c:454: uint8_t offset = SNAPSHOT_SIZE;
      0061B0 90 06 F6         [24] 3330 	mov	dptr,#_ak820_usb_send_offset_10000_413
      0061B3 74 2E            [12] 3331 	mov	a,#0x2e
      0061B5 F0               [24] 3332 	movx	@dptr,a
                                   3333 ;	tmk_core/protocol/ch555/usb_ak820.c:456: if (endpoint < 1 || endpoint > 3 || length > 64 || !USB_EnumStatus) return false;
      0061B6 90 06 F5         [24] 3334 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      0061B9 E0               [24] 3335 	movx	a,@dptr
      0061BA FF               [12] 3336 	mov	r7,a
      0061BB BF 01 00         [24] 3337 	cjne	r7,#0x01,00306$
      0061BE                       3338 00306$:
      0061BE 40 14            [24] 3339 	jc	00101$
      0061C0 EF               [12] 3340 	mov	a,r7
      0061C1 24 FC            [12] 3341 	add	a,#0xff - 0x03
      0061C3 40 0F            [24] 3342 	jc	00101$
                                   3343 ;	free result
      0061C5 90 06 F4         [24] 3344 	mov	dptr,#_ak820_usb_send_PARM_3
      0061C8 E0               [24] 3345 	movx	a,@dptr
      0061C9 FE               [12] 3346 	mov  r6,a
      0061CA 24 BF            [12] 3347 	add	a,#0xff - 0x40
      0061CC 40 06            [24] 3348 	jc	00101$
                                   3349 ;	free result
      0061CE 90 06 8D         [24] 3350 	mov	dptr,#_USB_EnumStatus
      0061D1 E0               [24] 3351 	movx	a,@dptr
      0061D2 70 04            [24] 3352 	jnz	00102$
      0061D4                       3353 00101$:
      0061D4 75 82 00         [24] 3354 	mov	dpl, #0x00
      0061D7 22               [24] 3355 	ret
      0061D8                       3356 00102$:
                                   3357 ;	tmk_core/protocol/ch555/usb_ak820.c:457: if (endpoint == KEYBOARD_IN_EPNUM) {
      0061D8 BF 01 10         [24] 3358 	cjne	r7,#0x01,00118$
                                   3359 ;	tmk_core/protocol/ch555/usb_ak820.c:458: if (length != KEYBOARD_EPSIZE) return false;
      0061DB BE 08 02         [24] 3360 	cjne	r6,#0x08,00313$
      0061DE 80 04            [24] 3361 	sjmp	00107$
      0061E0                       3362 00313$:
      0061E0 75 82 00         [24] 3363 	mov	dpl, #0x00
      0061E3 22               [24] 3364 	ret
      0061E4                       3365 00107$:
                                   3366 ;	tmk_core/protocol/ch555/usb_ak820.c:459: offset = SNAPSHOT_KEYBOARD;
      0061E4 90 06 F6         [24] 3367 	mov	dptr,#_ak820_usb_send_offset_10000_413
      0061E7 E4               [12] 3368 	clr	a
      0061E8 F0               [24] 3369 	movx	@dptr,a
      0061E9 80 3C            [24] 3370 	sjmp	00119$
      0061EB                       3371 00118$:
                                   3372 ;	tmk_core/protocol/ch555/usb_ak820.c:460: } else if (endpoint == SHARED_IN_EPNUM) {
      0061EB BF 02 30         [24] 3373 	cjne	r7,#0x02,00115$
                                   3374 ;	tmk_core/protocol/ch555/usb_ak820.c:461: report_id = report[0];
      0061EE 90 06 F2         [24] 3375 	mov	dptr,#_ak820_usb_send_PARM_2
      0061F1 E0               [24] 3376 	movx	a,@dptr
      0061F2 FD               [12] 3377 	mov	r5,a
      0061F3 A3               [24] 3378 	inc	dptr
      0061F4 E0               [24] 3379 	movx	a,@dptr
      0061F5 FF               [12] 3380 	mov	r7,a
      0061F6 8D 82            [24] 3381 	mov	dpl,r5
      0061F8 8F 83            [24] 3382 	mov	dph,r7
      0061FA E0               [24] 3383 	movx	a,@dptr
      0061FB FF               [12] 3384 	mov	r7,a
                                   3385 ;	tmk_core/protocol/ch555/usb_ak820.c:462: if (report_id >= sizeof(shared_lengths) || !shared_lengths[report_id] || length != shared_lengths[report_id]) return false;
      0061FC BF 07 00         [24] 3386 	cjne	r7,#0x07,00316$
      0061FF                       3387 00316$:
      0061FF 50 0E            [24] 3388 	jnc	00108$
      006201 EF               [12] 3389 	mov	a,r7
      006202 90 B6 3B         [24] 3390 	mov	dptr,#_shared_lengths
      006205 93               [24] 3391 	movc	a,@a+dptr
      006206 FD               [12] 3392 	mov	r5,a
      006207 60 06            [24] 3393 	jz	00108$
      006209 EE               [12] 3394 	mov	a,r6
      00620A B5 05 02         [24] 3395 	cjne	a,ar5,00319$
      00620D 80 04            [24] 3396 	sjmp	00109$
      00620F                       3397 00319$:
      00620F                       3398 00108$:
      00620F 75 82 00         [24] 3399 	mov	dpl, #0x00
      006212 22               [24] 3400 	ret
      006213                       3401 00109$:
                                   3402 ;	tmk_core/protocol/ch555/usb_ak820.c:463: offset = shared_offsets[report_id];
      006213 EF               [12] 3403 	mov	a,r7
      006214 90 B6 34         [24] 3404 	mov	dptr,#_shared_offsets
      006217 93               [24] 3405 	movc	a,@a+dptr
      006218 90 06 F6         [24] 3406 	mov	dptr,#_ak820_usb_send_offset_10000_413
      00621B F0               [24] 3407 	movx	@dptr,a
      00621C 80 09            [24] 3408 	sjmp	00119$
      00621E                       3409 00115$:
                                   3410 ;	tmk_core/protocol/ch555/usb_ak820.c:464: } else if (length != RAW_EPSIZE) return false;
      00621E BE 20 02         [24] 3411 	cjne	r6,#0x20,00320$
      006221 80 04            [24] 3412 	sjmp	00119$
      006223                       3413 00320$:
      006223 75 82 00         [24] 3414 	mov	dpl, #0x00
      006226 22               [24] 3415 	ret
      006227                       3416 00119$:
                                   3417 ;	tmk_core/protocol/ch555/usb_ak820.c:465: if (USB_SleepStatus & 2) { USB_WakeUp_PC(); return false; }
      006227 90 06 8E         [24] 3418 	mov	dptr,#_USB_SleepStatus
      00622A E0               [24] 3419 	movx	a,@dptr
      00622B 30 E1 07         [24] 3420 	jnb	acc.1,00184$
      00622E 12 61 7F         [24] 3421 	lcall	_USB_WakeUp_PC
      006231 75 82 00         [24] 3422 	mov	dpl, #0x00
      006234 22               [24] 3423 	ret
                                   3424 ;	tmk_core/protocol/ch555/usb_ak820.c:466: while ((EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_ACK && timeout--) wait_us(40);
      006235                       3425 00184$:
      006235 7F FA            [12] 3426 	mov	r7,#0xfa
      006237                       3427 00127$:
      006237 90 06 F5         [24] 3428 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      00623A E0               [24] 3429 	movx	a,@dptr
      00623B F5 29            [12] 3430 	mov	_ak820_usb_send_sloc1_1_0, a
      00623D 75 2A 00         [24] 3431 	mov	(_ak820_usb_send_sloc1_1_0 + 1),#0x00
      006240 AA 29            [24] 3432 	mov	r2,_ak820_usb_send_sloc1_1_0
      006242 74 22            [12] 3433 	mov	a,#0x22
      006244 25 2A            [12] 3434 	add	a, (_ak820_usb_send_sloc1_1_0 + 1)
      006246 FB               [12] 3435 	mov	r3,a
      006247 8A 82            [24] 3436 	mov	dpl,r2
      006249 8B 83            [24] 3437 	mov	dph,r3
      00624B E0               [24] 3438 	movx	a,@dptr
      00624C 54 03            [12] 3439 	anl	a,#0x03
      00624E 70 20            [24] 3440 	jnz	00129$
      006250 8F 03            [24] 3441 	mov	ar3,r7
      006252 1F               [12] 3442 	dec	r7
      006253 EB               [12] 3443 	mov	a,r3
      006254 60 1A            [24] 3444 	jz	00129$
      006256 7B 28            [12] 3445 	mov	r3,#0x28
      006258                       3446 00141$:
      006258 EB               [12] 3447 	mov	a,r3
      006259 60 DC            [24] 3448 	jz	00127$
      00625B 90 00 01         [24] 3449 	mov	dptr,#0x0001
      00625E C0 07            [24] 3450 	push	ar7
      006260 C0 06            [24] 3451 	push	ar6
      006262 C0 03            [24] 3452 	push	ar3
      006264 12 52 41         [24] 3453 	lcall	_mDelayuS
      006267 D0 03            [24] 3454 	pop	ar3
      006269 D0 06            [24] 3455 	pop	ar6
      00626B D0 07            [24] 3456 	pop	ar7
      00626D 1B               [12] 3457 	dec	r3
      00626E 80 E8            [24] 3458 	sjmp	00141$
      006270                       3459 00129$:
                                   3460 ;	tmk_core/protocol/ch555/usb_ak820.c:467: saved_ea = EA;
      006270 A2 AF            [12] 3461 	mov	c,_EA
      006272 E4               [12] 3462 	clr	a
      006273 33               [12] 3463 	rlc	a
      006274 FF               [12] 3464 	mov	r7,a
                                   3465 ;	tmk_core/protocol/ch555/usb_ak820.c:468: EA = 0;
                                   3466 ;	assignBit
      006275 C2 AF            [12] 3467 	clr	_EA
                                   3468 ;	tmk_core/protocol/ch555/usb_ak820.c:469: if (!USB_EnumStatus || (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) != UEP_X_RES_NAK ||
      006277 90 06 8D         [24] 3469 	mov	dptr,#_USB_EnumStatus
      00627A E0               [24] 3470 	movx	a,@dptr
      00627B 60 25            [24] 3471 	jz	00130$
      00627D 90 06 F5         [24] 3472 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      006280 E0               [24] 3473 	movx	a,@dptr
      006281 FB               [12] 3474 	mov	r3,a
      006282 F9               [12] 3475 	mov	r1,a
      006283 7A 00            [12] 3476 	mov	r2,#0x00
      006285 74 22            [12] 3477 	mov	a,#0x22
      006287 2A               [12] 3478 	add	a, r2
      006288 FA               [12] 3479 	mov	r2,a
      006289 89 82            [24] 3480 	mov	dpl,r1
      00628B 8A 83            [24] 3481 	mov	dph,r2
      00628D E0               [24] 3482 	movx	a,@dptr
      00628E FA               [12] 3483 	mov	r2,a
      00628F 53 02 03         [24] 3484 	anl	ar2,#0x03
      006292 BA 02 0D         [24] 3485 	cjne	r2,#0x02,00130$
                                   3486 ;	tmk_core/protocol/ch555/usb_ak820.c:470: (endpoint == RAW_IN_EPNUM && raw_state != RAW_WORK)) { EA = saved_ea; return false; }
      006295 BB 03 13         [24] 3487 	cjne	r3,#0x03,00192$
      006298 90 06 94         [24] 3488 	mov	dptr,#_raw_state
      00629B E0               [24] 3489 	movx	a,@dptr
      00629C FB               [12] 3490 	mov	r3,a
      00629D BB 03 02         [24] 3491 	cjne	r3,#0x03,00331$
      0062A0 80 09            [24] 3492 	sjmp	00192$
      0062A2                       3493 00331$:
      0062A2                       3494 00130$:
                                   3495 ;	assignBit
      0062A2 EF               [12] 3496 	mov	a,r7
      0062A3 24 FF            [12] 3497 	add	a,#0xff
      0062A5 92 AF            [24] 3498 	mov	_EA,c
      0062A7 75 82 00         [24] 3499 	mov	dpl, #0x00
      0062AA 22               [24] 3500 	ret
                                   3501 ;	tmk_core/protocol/ch555/usb_ak820.c:471: for (i = 0; i < length; ++i) {
      0062AB                       3502 00192$:
      0062AB 90 06 F2         [24] 3503 	mov	dptr,#_ak820_usb_send_PARM_2
      0062AE E0               [24] 3504 	movx	a,@dptr
      0062AF F5 2B            [12] 3505 	mov	_ak820_usb_send_sloc2_1_0,a
      0062B1 A3               [24] 3506 	inc	dptr
      0062B2 E0               [24] 3507 	movx	a,@dptr
      0062B3 F5 2C            [12] 3508 	mov	(_ak820_usb_send_sloc2_1_0 + 1),a
      0062B5 90 06 F6         [24] 3509 	mov	dptr,#_ak820_usb_send_offset_10000_413
      0062B8 E0               [24] 3510 	movx	a,@dptr
      0062B9 F9               [12] 3511 	mov	r1,a
      0062BA B9 2E 03         [24] 3512 	cjne	r1,#0x2e,00332$
      0062BD D3               [12] 3513 	setb	c
      0062BE 80 01            [24] 3514 	sjmp	00333$
      0062C0                       3515 00332$:
      0062C0 C3               [12] 3516 	clr	c
      0062C1                       3517 00333$:
      0062C1 92 0A            [24] 3518 	mov	_ak820_usb_send_sloc0_1_0,c
      0062C3 78 00            [12] 3519 	mov	r0,#0x00
      0062C5                       3520 00144$:
      0062C5 C3               [12] 3521 	clr	c
      0062C6 E8               [12] 3522 	mov	a,r0
      0062C7 9E               [12] 3523 	subb	a,r6
      0062C8 50 54            [24] 3524 	jnc	00137$
                                   3525 ;	tmk_core/protocol/ch555/usb_ak820.c:472: pUSB_BUF_DEV0[((uint16_t)endpoint << 6) + i] = report[i];
      0062CA C0 07            [24] 3526 	push	ar7
      0062CC 90 06 F5         [24] 3527 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      0062CF E0               [24] 3528 	movx	a,@dptr
      0062D0 FD               [12] 3529 	mov	r5,a
      0062D1 E4               [12] 3530 	clr	a
      0062D2 C3               [12] 3531 	clr	c
      0062D3 CD               [12] 3532 	xch	a,r5
      0062D4 13               [12] 3533 	rrc	a
      0062D5 CD               [12] 3534 	xch	a,r5
      0062D6 13               [12] 3535 	rrc	a
      0062D7 A2 E0            [12] 3536 	mov	c,acc.0
      0062D9 CD               [12] 3537 	xch	a,r5
      0062DA 13               [12] 3538 	rrc	a
      0062DB CD               [12] 3539 	xch	a,r5
      0062DC 13               [12] 3540 	rrc	a
      0062DD CD               [12] 3541 	xch	a,r5
      0062DE FF               [12] 3542 	mov	r7,a
      0062DF 88 03            [24] 3543 	mov	ar3,r0
      0062E1 7C 00            [12] 3544 	mov	r4,#0x00
      0062E3 EB               [12] 3545 	mov	a,r3
      0062E4 2D               [12] 3546 	add	a, r5
      0062E5 FD               [12] 3547 	mov	r5,a
      0062E6 EC               [12] 3548 	mov	a,r4
      0062E7 3F               [12] 3549 	addc	a, r7
      0062E8 24 10            [12] 3550 	add	a,#0x10
      0062EA FF               [12] 3551 	mov	r7,a
      0062EB E8               [12] 3552 	mov	a,r0
      0062EC 25 2B            [12] 3553 	add	a, _ak820_usb_send_sloc2_1_0
      0062EE F5 2D            [12] 3554 	mov	_ak820_usb_send_sloc3_1_0,a
      0062F0 E4               [12] 3555 	clr	a
      0062F1 35 2C            [12] 3556 	addc	a, (_ak820_usb_send_sloc2_1_0 + 1)
      0062F3 F5 2E            [12] 3557 	mov	(_ak820_usb_send_sloc3_1_0 + 1),a
      0062F5 85 2D 82         [24] 3558 	mov	dpl,_ak820_usb_send_sloc3_1_0
      0062F8 85 2E 83         [24] 3559 	mov	dph,(_ak820_usb_send_sloc3_1_0 + 1)
      0062FB E0               [24] 3560 	movx	a,@dptr
      0062FC 8D 82            [24] 3561 	mov	dpl,r5
      0062FE 8F 83            [24] 3562 	mov	dph,r7
      006300 F0               [24] 3563 	movx	@dptr,a
                                   3564 ;	tmk_core/protocol/ch555/usb_ak820.c:473: if (offset != SNAPSHOT_SIZE) input_snapshot[offset + i] = report[i];
      006301 D0 07            [24] 3565 	pop	ar7
      006303 20 0A 15         [24] 3566 	jb	_ak820_usb_send_sloc0_1_0,00145$
      006306 E8               [12] 3567 	mov	a,r0
      006307 29               [12] 3568 	add	a, r1
      006308 24 B7            [12] 3569 	add	a, #_input_snapshot
      00630A FC               [12] 3570 	mov	r4,a
      00630B E4               [12] 3571 	clr	a
      00630C 34 06            [12] 3572 	addc	a,#(_input_snapshot >> 8)
      00630E FD               [12] 3573 	mov	r5,a
      00630F 85 2D 82         [24] 3574 	mov	dpl,_ak820_usb_send_sloc3_1_0
      006312 85 2E 83         [24] 3575 	mov	dph,(_ak820_usb_send_sloc3_1_0 + 1)
      006315 E0               [24] 3576 	movx	a,@dptr
      006316 8C 82            [24] 3577 	mov	dpl,r4
      006318 8D 83            [24] 3578 	mov	dph,r5
      00631A F0               [24] 3579 	movx	@dptr,a
      00631B                       3580 00145$:
                                   3581 ;	tmk_core/protocol/ch555/usb_ak820.c:471: for (i = 0; i < length; ++i) {
      00631B 08               [12] 3582 	inc	r0
      00631C 80 A7            [24] 3583 	sjmp	00144$
      00631E                       3584 00137$:
                                   3585 ;	tmk_core/protocol/ch555/usb_ak820.c:475: EP_LENGTH(endpoint) = length;
      00631E 90 06 F5         [24] 3586 	mov	dptr,#_ak820_usb_send_endpoint_10000_412
      006321 E0               [24] 3587 	movx	a,@dptr
      006322 FD               [12] 3588 	mov	r5,a
      006323 FC               [12] 3589 	mov	r4,a
      006324 7B 00            [12] 3590 	mov	r3,#0x00
      006326 74 08            [12] 3591 	mov	a,#0x08
      006328 2C               [12] 3592 	add	a, r4
      006329 FC               [12] 3593 	mov	r4,a
      00632A 74 22            [12] 3594 	mov	a,#0x22
      00632C 3B               [12] 3595 	addc	a, r3
      00632D FB               [12] 3596 	mov	r3,a
      00632E 8C 82            [24] 3597 	mov	dpl,r4
      006330 8B 83            [24] 3598 	mov	dph,r3
      006332 EE               [12] 3599 	mov	a,r6
      006333 F0               [24] 3600 	movx	@dptr,a
                                   3601 ;	tmk_core/protocol/ch555/usb_ak820.c:476: if (endpoint == RAW_IN_EPNUM) raw_state = RAW_TX_ACTIVE;
      006334 BD 03 06         [24] 3602 	cjne	r5,#0x03,00139$
      006337 90 06 94         [24] 3603 	mov	dptr,#_raw_state
      00633A 74 04            [12] 3604 	mov	a,#0x04
      00633C F0               [24] 3605 	movx	@dptr,a
      00633D                       3606 00139$:
                                   3607 ;	tmk_core/protocol/ch555/usb_ak820.c:477: EP_RESPONSE(endpoint) = (EP_RESPONSE(endpoint) & ~MASK_UEP_X_RES) | UEP_X_RES_ACK;
      00633D AD 29            [24] 3608 	mov	r5,_ak820_usb_send_sloc1_1_0
      00633F 74 22            [12] 3609 	mov	a,#0x22
      006341 25 2A            [12] 3610 	add	a, (_ak820_usb_send_sloc1_1_0 + 1)
      006343 FE               [12] 3611 	mov	r6,a
      006344 8D 82            [24] 3612 	mov	dpl,r5
      006346 8E 83            [24] 3613 	mov	dph,r6
      006348 E0               [24] 3614 	movx	a,@dptr
      006349 FC               [12] 3615 	mov	r4,a
      00634A 53 04 FC         [24] 3616 	anl	ar4,#0xfc
      00634D 8D 82            [24] 3617 	mov	dpl,r5
      00634F 8E 83            [24] 3618 	mov	dph,r6
      006351 EC               [12] 3619 	mov	a,r4
      006352 F0               [24] 3620 	movx	@dptr,a
                                   3621 ;	tmk_core/protocol/ch555/usb_ak820.c:478: EA = saved_ea;
                                   3622 ;	assignBit
      006353 EF               [12] 3623 	mov	a,r7
      006354 24 FF            [12] 3624 	add	a,#0xff
      006356 92 AF            [24] 3625 	mov	_EA,c
                                   3626 ;	tmk_core/protocol/ch555/usb_ak820.c:479: return true;
      006358 75 82 01         [24] 3627 	mov	dpl, #0x01
                                   3628 ;	tmk_core/protocol/ch555/usb_ak820.c:480: }
      00635B 22               [24] 3629 	ret
                                   3630 ;------------------------------------------------------------
                                   3631 ;Allocation info for local variables in function 'ak820_usb_try_send'
                                   3632 ;------------------------------------------------------------
                                   3633 ;report        Allocated with name '_ak820_usb_try_send_PARM_2'
                                   3634 ;length        Allocated with name '_ak820_usb_try_send_PARM_3'
                                   3635 ;endpoint      Allocated with name '_ak820_usb_try_send_endpoint_10000_433'
                                   3636 ;saved_ea      Allocated with name '_ak820_usb_try_send_saved_ea_10000_434'
                                   3637 ;sent          Allocated with name '_ak820_usb_try_send_sent_10000_434'
                                   3638 ;------------------------------------------------------------
                                   3639 ;	tmk_core/protocol/ch555/usb_ak820.c:482: bool ak820_usb_try_send(uint8_t endpoint, const uint8_t __xdata *report, uint8_t length) {
                                   3640 ;	-----------------------------------------
                                   3641 ;	 function ak820_usb_try_send
                                   3642 ;	-----------------------------------------
      00635C                       3643 _ak820_usb_try_send:
      00635C E5 82            [12] 3644 	mov	a,dpl
      00635E 90 06 FA         [24] 3645 	mov	dptr,#_ak820_usb_try_send_endpoint_10000_433
      006361 F0               [24] 3646 	movx	@dptr,a
                                   3647 ;	tmk_core/protocol/ch555/usb_ak820.c:483: uint8_t saved_ea = EA;
                                   3648 ;	assignBit
      006362 A2 AF            [12] 3649 	mov	c,_EA
      006364 92 0B            [24] 3650 	mov	_ak820_usb_try_send_sloc0_1_0,c
                                   3651 ;	tmk_core/protocol/ch555/usb_ak820.c:484: bool sent = false;
      006366 90 06 FB         [24] 3652 	mov	dptr,#_ak820_usb_try_send_sent_10000_434
      006369 E4               [12] 3653 	clr	a
      00636A F0               [24] 3654 	movx	@dptr,a
                                   3655 ;	tmk_core/protocol/ch555/usb_ak820.c:485: EA = 0;
                                   3656 ;	assignBit
      00636B C2 AF            [12] 3657 	clr	_EA
                                   3658 ;	tmk_core/protocol/ch555/usb_ak820.c:489: if (endpoint >= 1 && endpoint <= 2 && USB_EnumStatus &&
      00636D 90 06 FA         [24] 3659 	mov	dptr,#_ak820_usb_try_send_endpoint_10000_433
      006370 E0               [24] 3660 	movx	a,@dptr
      006371 FF               [12] 3661 	mov	r7,a
      006372 BF 01 00         [24] 3662 	cjne	r7,#0x01,00152$
      006375                       3663 00152$:
      006375 40 4E            [24] 3664 	jc	00102$
      006377 EF               [12] 3665 	mov	a,r7
      006378 24 FD            [12] 3666 	add	a,#0xff - 0x02
      00637A 40 49            [24] 3667 	jc	00102$
                                   3668 ;	free result
      00637C 90 06 8D         [24] 3669 	mov	dptr,#_USB_EnumStatus
      00637F E0               [24] 3670 	movx	a,@dptr
      006380 60 43            [24] 3671 	jz	00102$
                                   3672 ;	tmk_core/protocol/ch555/usb_ak820.c:490: !(USB_SleepStatus & 2) && !keyboard_reset &&
      006382 90 06 8E         [24] 3673 	mov	dptr,#_USB_SleepStatus
      006385 E0               [24] 3674 	movx	a,@dptr
      006386 20 E1 3C         [24] 3675 	jb	acc.1,00102$
      006389 90 06 B6         [24] 3676 	mov	dptr,#_keyboard_reset
      00638C E0               [24] 3677 	movx	a,@dptr
                                   3678 ;	tmk_core/protocol/ch555/usb_ak820.c:491: (EP_RESPONSE(endpoint) & MASK_UEP_X_RES) == UEP_X_RES_NAK) {
      00638D 70 36            [24] 3679 	jnz	00102$
      00638F 8F 06            [24] 3680 	mov	ar6,r7
      006391 24 22            [12] 3681 	add	a,#0x22
      006393 FD               [12] 3682 	mov	r5,a
      006394 8E 82            [24] 3683 	mov	dpl,r6
      006396 8D 83            [24] 3684 	mov	dph,r5
      006398 E0               [24] 3685 	movx	a,@dptr
      006399 FE               [12] 3686 	mov	r6,a
      00639A 53 06 03         [24] 3687 	anl	ar6,#0x03
      00639D BE 02 25         [24] 3688 	cjne	r6,#0x02,00102$
                                   3689 ;	tmk_core/protocol/ch555/usb_ak820.c:492: sent = ak820_usb_send(endpoint, report, length);
      0063A0 90 06 F7         [24] 3690 	mov	dptr,#_ak820_usb_try_send_PARM_2
      0063A3 E0               [24] 3691 	movx	a,@dptr
      0063A4 FD               [12] 3692 	mov	r5,a
      0063A5 A3               [24] 3693 	inc	dptr
      0063A6 E0               [24] 3694 	movx	a,@dptr
      0063A7 FE               [12] 3695 	mov	r6,a
      0063A8 90 06 F9         [24] 3696 	mov	dptr,#_ak820_usb_try_send_PARM_3
      0063AB E0               [24] 3697 	movx	a,@dptr
      0063AC FC               [12] 3698 	mov	r4,a
      0063AD 90 06 F2         [24] 3699 	mov	dptr,#_ak820_usb_send_PARM_2
      0063B0 ED               [12] 3700 	mov	a,r5
      0063B1 F0               [24] 3701 	movx	@dptr,a
      0063B2 EE               [12] 3702 	mov	a,r6
      0063B3 A3               [24] 3703 	inc	dptr
      0063B4 F0               [24] 3704 	movx	@dptr,a
      0063B5 90 06 F4         [24] 3705 	mov	dptr,#_ak820_usb_send_PARM_3
      0063B8 EC               [12] 3706 	mov	a,r4
      0063B9 F0               [24] 3707 	movx	@dptr,a
      0063BA 8F 82            [24] 3708 	mov	dpl, r7
      0063BC 12 61 AA         [24] 3709 	lcall	_ak820_usb_send
      0063BF E5 82            [12] 3710 	mov	a, dpl
      0063C1 90 06 FB         [24] 3711 	mov	dptr,#_ak820_usb_try_send_sent_10000_434
      0063C4 F0               [24] 3712 	movx	@dptr,a
      0063C5                       3713 00102$:
                                   3714 ;	tmk_core/protocol/ch555/usb_ak820.c:494: EA = saved_ea;
                                   3715 ;	assignBit
      0063C5 A2 0B            [12] 3716 	mov	c,_ak820_usb_try_send_sloc0_1_0
      0063C7 92 AF            [24] 3717 	mov	_EA,c
                                   3718 ;	tmk_core/protocol/ch555/usb_ak820.c:495: return sent;
      0063C9 90 06 FB         [24] 3719 	mov	dptr,#_ak820_usb_try_send_sent_10000_434
      0063CC E0               [24] 3720 	movx	a,@dptr
                                   3721 ;	tmk_core/protocol/ch555/usb_ak820.c:496: }
      0063CD F5 82            [12] 3722 	mov	dpl,a
      0063CF 22               [24] 3723 	ret
                                   3724 ;------------------------------------------------------------
                                   3725 ;Allocation info for local variables in function 'raw_request_is_nonpersistent'
                                   3726 ;------------------------------------------------------------
                                   3727 ;	tmk_core/protocol/ch555/usb_ak820.c:501: static bool raw_request_is_nonpersistent(void) {
                                   3728 ;	-----------------------------------------
                                   3729 ;	 function raw_request_is_nonpersistent
                                   3730 ;	-----------------------------------------
      0063D0                       3731 _raw_request_is_nonpersistent:
                                   3732 ;	tmk_core/protocol/ch555/usb_ak820.c:502: switch (raw_buffer[0]) {
      0063D0 90 06 95         [24] 3733 	mov	dptr,#_raw_buffer
      0063D3 E0               [24] 3734 	movx	a,@dptr
      0063D4 FF               [12] 3735 	mov	r7,a
      0063D5 BF 01 02         [24] 3736 	cjne	r7,#0x01,00302$
      0063D8 80 35            [24] 3737 	sjmp	00108$
      0063DA                       3738 00302$:
      0063DA BF 02 02         [24] 3739 	cjne	r7,#0x02,00303$
      0063DD 80 34            [24] 3740 	sjmp	00109$
      0063DF                       3741 00303$:
      0063DF BF 04 02         [24] 3742 	cjne	r7,#0x04,00304$
      0063E2 80 2B            [24] 3743 	sjmp	00108$
      0063E4                       3744 00304$:
      0063E4 BF 08 02         [24] 3745 	cjne	r7,#0x08,00305$
      0063E7 80 49            [24] 3746 	sjmp	00116$
      0063E9                       3747 00305$:
      0063E9 BF 0B 02         [24] 3748 	cjne	r7,#0x0b,00306$
      0063EC 80 21            [24] 3749 	sjmp	00108$
      0063EE                       3750 00306$:
      0063EE BF 0C 02         [24] 3751 	cjne	r7,#0x0c,00307$
      0063F1 80 1C            [24] 3752 	sjmp	00108$
      0063F3                       3753 00307$:
      0063F3 BF 0D 02         [24] 3754 	cjne	r7,#0x0d,00308$
      0063F6 80 17            [24] 3755 	sjmp	00108$
      0063F8                       3756 00308$:
      0063F8 BF 0E 02         [24] 3757 	cjne	r7,#0x0e,00309$
      0063FB 80 12            [24] 3758 	sjmp	00108$
      0063FD                       3759 00309$:
      0063FD BF 11 02         [24] 3760 	cjne	r7,#0x11,00310$
      006400 80 0D            [24] 3761 	sjmp	00108$
      006402                       3762 00310$:
      006402 BF 12 02         [24] 3763 	cjne	r7,#0x12,00311$
      006405 80 08            [24] 3764 	sjmp	00108$
      006407                       3765 00311$:
      006407 BF FE 02         [24] 3766 	cjne	r7,#0xfe,00312$
      00640A 80 4A            [24] 3767 	sjmp	00124$
      00640C                       3768 00312$:
      00640C 02 64 AD         [24] 3769 	ljmp	00144$
                                   3770 ;	tmk_core/protocol/ch555/usb_ak820.c:510: case id_bootloader_jump:
      00640F                       3771 00108$:
                                   3772 ;	tmk_core/protocol/ch555/usb_ak820.c:511: return true;
      00640F 75 82 01         [24] 3773 	mov	dpl, #0x01
      006412 22               [24] 3774 	ret
                                   3775 ;	tmk_core/protocol/ch555/usb_ak820.c:512: case id_get_keyboard_value:
      006413                       3776 00109$:
                                   3777 ;	tmk_core/protocol/ch555/usb_ak820.c:513: switch (raw_buffer[1]) {
      006413 90 06 96         [24] 3778 	mov	dptr,#(_raw_buffer + 0x0001)
      006416 E0               [24] 3779 	movx	a,@dptr
      006417 FF               [12] 3780 	mov	r7,a
      006418 BF 01 02         [24] 3781 	cjne	r7,#0x01,00313$
      00641B 80 0D            [24] 3782 	sjmp	00113$
      00641D                       3783 00313$:
      00641D BF 02 02         [24] 3784 	cjne	r7,#0x02,00314$
      006420 80 08            [24] 3785 	sjmp	00113$
      006422                       3786 00314$:
      006422 BF 03 02         [24] 3787 	cjne	r7,#0x03,00315$
      006425 80 03            [24] 3788 	sjmp	00113$
      006427                       3789 00315$:
      006427 BF 04 04         [24] 3790 	cjne	r7,#0x04,00114$
                                   3791 ;	tmk_core/protocol/ch555/usb_ak820.c:517: case id_firmware_version:
      00642A                       3792 00113$:
                                   3793 ;	tmk_core/protocol/ch555/usb_ak820.c:518: return true;
      00642A 75 82 01         [24] 3794 	mov	dpl, #0x01
      00642D 22               [24] 3795 	ret
                                   3796 ;	tmk_core/protocol/ch555/usb_ak820.c:519: default: return false;
      00642E                       3797 00114$:
      00642E 75 82 00         [24] 3798 	mov	dpl, #0x00
      006431 22               [24] 3799 	ret
                                   3800 ;	tmk_core/protocol/ch555/usb_ak820.c:521: case id_lighting_get_value:
      006432                       3801 00116$:
                                   3802 ;	tmk_core/protocol/ch555/usb_ak820.c:522: switch (raw_buffer[1]) {
      006432 90 06 96         [24] 3803 	mov	dptr,#(_raw_buffer + 0x0001)
      006435 E0               [24] 3804 	movx	a,@dptr
      006436 FF               [12] 3805 	mov	r7,a
      006437 BF 40 02         [24] 3806 	cjne	r7,#0x40,00318$
      00643A 80 12            [24] 3807 	sjmp	00121$
      00643C                       3808 00318$:
      00643C BF 41 02         [24] 3809 	cjne	r7,#0x41,00319$
      00643F 80 0D            [24] 3810 	sjmp	00121$
      006441                       3811 00319$:
      006441 BF 42 02         [24] 3812 	cjne	r7,#0x42,00320$
      006444 80 08            [24] 3813 	sjmp	00121$
      006446                       3814 00320$:
      006446 BF 43 02         [24] 3815 	cjne	r7,#0x43,00321$
      006449 80 03            [24] 3816 	sjmp	00121$
      00644B                       3817 00321$:
      00644B BF 44 04         [24] 3818 	cjne	r7,#0x44,00122$
                                   3819 ;	tmk_core/protocol/ch555/usb_ak820.c:527: case vialrgb_get_led_info:
      00644E                       3820 00121$:
                                   3821 ;	tmk_core/protocol/ch555/usb_ak820.c:528: return true;
      00644E 75 82 01         [24] 3822 	mov	dpl, #0x01
                                   3823 ;	tmk_core/protocol/ch555/usb_ak820.c:529: default: return false;
      006451 22               [24] 3824 	ret
      006452                       3825 00122$:
      006452 75 82 00         [24] 3826 	mov	dpl, #0x00
                                   3827 ;	tmk_core/protocol/ch555/usb_ak820.c:531: case id_vial_prefix:
      006455 22               [24] 3828 	ret
      006456                       3829 00124$:
                                   3830 ;	tmk_core/protocol/ch555/usb_ak820.c:532: switch (raw_buffer[1]) {
      006456 90 06 96         [24] 3831 	mov	dptr,#(_raw_buffer + 0x0001)
      006459 E0               [24] 3832 	movx	a,@dptr
      00645A FF               [12] 3833 	mov  r7,a
      00645B 24 F2            [12] 3834 	add	a,#0xff - 0x0d
      00645D 40 4A            [24] 3835 	jc	00142$
                                   3836 ;	free result
      00645F EF               [12] 3837 	mov	a,r7
      006460 24 0A            [12] 3838 	add	a,#(00325$-3-.)
      006462 83               [24] 3839 	movc	a,@a+pc
      006463 F5 82            [12] 3840 	mov	dpl,a
      006465 EF               [12] 3841 	mov	a,r7
      006466 24 12            [12] 3842 	add	a,#(00326$-3-.)
      006468 83               [24] 3843 	movc	a,@a+pc
      006469 F5 83            [12] 3844 	mov	dph,a
      00646B E4               [12] 3845 	clr	a
      00646C 73               [24] 3846 	jmp	@a+dptr
      00646D                       3847 00325$:
      00646D 89                    3848 	.db	00134$
      00646E 89                    3849 	.db	00134$
      00646F 89                    3850 	.db	00134$
      006470 89                    3851 	.db	00134$
      006471 A9                    3852 	.db	00142$
      006472 89                    3853 	.db	00134$
      006473 89                    3854 	.db	00134$
      006474 89                    3855 	.db	00134$
      006475 89                    3856 	.db	00134$
      006476 89                    3857 	.db	00134$
      006477 89                    3858 	.db	00134$
      006478 A9                    3859 	.db	00142$
      006479 A9                    3860 	.db	00142$
      00647A 8D                    3861 	.db	00135$
      00647B                       3862 00326$:
      00647B 64                    3863 	.db	00134$>>8
      00647C 64                    3864 	.db	00134$>>8
      00647D 64                    3865 	.db	00134$>>8
      00647E 64                    3866 	.db	00134$>>8
      00647F 64                    3867 	.db	00142$>>8
      006480 64                    3868 	.db	00134$>>8
      006481 64                    3869 	.db	00134$>>8
      006482 64                    3870 	.db	00134$>>8
      006483 64                    3871 	.db	00134$>>8
      006484 64                    3872 	.db	00134$>>8
      006485 64                    3873 	.db	00134$>>8
      006486 64                    3874 	.db	00142$>>8
      006487 64                    3875 	.db	00142$>>8
      006488 64                    3876 	.db	00135$>>8
                                   3877 ;	tmk_core/protocol/ch555/usb_ak820.c:542: case vial_qmk_settings_get:
      006489                       3878 00134$:
                                   3879 ;	tmk_core/protocol/ch555/usb_ak820.c:543: return true;
      006489 75 82 01         [24] 3880 	mov	dpl, #0x01
                                   3881 ;	tmk_core/protocol/ch555/usb_ak820.c:544: case vial_dynamic_entry_op:
      00648C 22               [24] 3882 	ret
      00648D                       3883 00135$:
                                   3884 ;	tmk_core/protocol/ch555/usb_ak820.c:545: switch (raw_buffer[2]) {
      00648D 90 06 97         [24] 3885 	mov	dptr,#(_raw_buffer + 0x0002)
      006490 E0               [24] 3886 	movx	a,@dptr
      006491 FF               [12] 3887 	mov	r7,a
      006492 60 0D            [24] 3888 	jz	00139$
      006494 BF 01 02         [24] 3889 	cjne	r7,#0x01,00328$
      006497 80 08            [24] 3890 	sjmp	00139$
      006499                       3891 00328$:
      006499 BF 03 02         [24] 3892 	cjne	r7,#0x03,00329$
      00649C 80 03            [24] 3893 	sjmp	00139$
      00649E                       3894 00329$:
      00649E BF 05 04         [24] 3895 	cjne	r7,#0x05,00140$
                                   3896 ;	tmk_core/protocol/ch555/usb_ak820.c:549: case dynamic_vial_key_override_get:
      0064A1                       3897 00139$:
                                   3898 ;	tmk_core/protocol/ch555/usb_ak820.c:550: return true;
      0064A1 75 82 01         [24] 3899 	mov	dpl, #0x01
                                   3900 ;	tmk_core/protocol/ch555/usb_ak820.c:551: default: return false;
      0064A4 22               [24] 3901 	ret
      0064A5                       3902 00140$:
      0064A5 75 82 00         [24] 3903 	mov	dpl, #0x00
                                   3904 ;	tmk_core/protocol/ch555/usb_ak820.c:553: default: return false;
      0064A8 22               [24] 3905 	ret
      0064A9                       3906 00142$:
      0064A9 75 82 00         [24] 3907 	mov	dpl, #0x00
                                   3908 ;	tmk_core/protocol/ch555/usb_ak820.c:555: default: return false;
      0064AC 22               [24] 3909 	ret
      0064AD                       3910 00144$:
      0064AD 75 82 00         [24] 3911 	mov	dpl, #0x00
                                   3912 ;	tmk_core/protocol/ch555/usb_ak820.c:556: }
                                   3913 ;	tmk_core/protocol/ch555/usb_ak820.c:557: }
      0064B0 22               [24] 3914 	ret
                                   3915 ;------------------------------------------------------------
                                   3916 ;Allocation info for local variables in function 'ak820_usb_raw_send'
                                   3917 ;------------------------------------------------------------
                                   3918 ;length        Allocated with name '_ak820_usb_raw_send_PARM_2'
                                   3919 ;report        Allocated with name '_ak820_usb_raw_send_report_10000_449'
                                   3920 ;------------------------------------------------------------
                                   3921 ;	tmk_core/protocol/ch555/usb_ak820.c:559: void ak820_usb_raw_send(const uint8_t *report, uint8_t length) {
                                   3922 ;	-----------------------------------------
                                   3923 ;	 function ak820_usb_raw_send
                                   3924 ;	-----------------------------------------
      0064B1                       3925 _ak820_usb_raw_send:
      0064B1 AF F0            [24] 3926 	mov	r7,b
      0064B3 AE 83            [24] 3927 	mov	r6,dph
      0064B5 E5 82            [12] 3928 	mov	a,dpl
      0064B7 90 06 FD         [24] 3929 	mov	dptr,#_ak820_usb_raw_send_report_10000_449
      0064BA F0               [24] 3930 	movx	@dptr,a
      0064BB EE               [12] 3931 	mov	a,r6
      0064BC A3               [24] 3932 	inc	dptr
      0064BD F0               [24] 3933 	movx	@dptr,a
      0064BE EF               [12] 3934 	mov	a,r7
      0064BF A3               [24] 3935 	inc	dptr
      0064C0 F0               [24] 3936 	movx	@dptr,a
                                   3937 ;	tmk_core/protocol/ch555/usb_ak820.c:560: if (length != RAW_EPSIZE) return;
      0064C1 90 06 FC         [24] 3938 	mov	dptr,#_ak820_usb_raw_send_PARM_2
      0064C4 E0               [24] 3939 	movx	a,@dptr
      0064C5 FF               [12] 3940 	mov	r7,a
      0064C6 BF 20 2F         [24] 3941 	cjne	r7,#0x20,00106$
                                   3942 ;	tmk_core/protocol/ch555/usb_ak820.c:561: ak820_nvm_flush();
      0064C9 C0 07            [24] 3943 	push	ar7
      0064CB 12 3A EA         [24] 3944 	lcall	_ak820_nvm_flush
      0064CE D0 07            [24] 3945 	pop	ar7
                                   3946 ;	tmk_core/protocol/ch555/usb_ak820.c:562: if (raw_reply_without_nvm || ak820_nvm_ok()) ak820_usb_send(RAW_IN_EPNUM, (const uint8_t __xdata *)report, length);
      0064D0 90 06 B5         [24] 3947 	mov	dptr,#_raw_reply_without_nvm
      0064D3 E0               [24] 3948 	movx	a,@dptr
      0064D4 70 07            [24] 3949 	jnz	00103$
      0064D6 12 3A D2         [24] 3950 	lcall	_ak820_nvm_ok
      0064D9 E5 82            [12] 3951 	mov	a, dpl
      0064DB 60 1B            [24] 3952 	jz	00106$
      0064DD                       3953 00103$:
      0064DD 90 06 FD         [24] 3954 	mov	dptr,#_ak820_usb_raw_send_report_10000_449
      0064E0 E0               [24] 3955 	movx	a,@dptr
      0064E1 FD               [12] 3956 	mov	r5,a
      0064E2 A3               [24] 3957 	inc	dptr
      0064E3 E0               [24] 3958 	movx	a,@dptr
      0064E4 FE               [12] 3959 	mov	r6,a
      0064E5 90 06 F2         [24] 3960 	mov	dptr,#_ak820_usb_send_PARM_2
      0064E8 ED               [12] 3961 	mov	a,r5
      0064E9 F0               [24] 3962 	movx	@dptr,a
      0064EA EE               [12] 3963 	mov	a,r6
      0064EB A3               [24] 3964 	inc	dptr
      0064EC F0               [24] 3965 	movx	@dptr,a
      0064ED 90 06 F4         [24] 3966 	mov	dptr,#_ak820_usb_send_PARM_3
      0064F0 EF               [12] 3967 	mov	a,r7
      0064F1 F0               [24] 3968 	movx	@dptr,a
      0064F2 75 82 03         [24] 3969 	mov	dpl, #0x03
                                   3970 ;	tmk_core/protocol/ch555/usb_ak820.c:563: }
      0064F5 02 61 AA         [24] 3971 	ljmp	_ak820_usb_send
      0064F8                       3972 00106$:
      0064F8 22               [24] 3973 	ret
                                   3974 ;------------------------------------------------------------
                                   3975 ;Allocation info for local variables in function 'ak820_usb_raw_task'
                                   3976 ;------------------------------------------------------------
                                   3977 ;sloc0         Allocated with name '_ak820_usb_raw_task_sloc0_1_0'
                                   3978 ;i             Allocated with name '_ak820_usb_raw_task_i_10000_454'
                                   3979 ;length        Allocated with name '_ak820_usb_raw_task_length_10000_454'
                                   3980 ;address       Allocated with name '_ak820_usb_raw_task_address_10000_454'
                                   3981 ;saved_ea      Allocated with name '_ak820_usb_raw_task_saved_ea_10000_454'
                                   3982 ;------------------------------------------------------------
                                   3983 ;	tmk_core/protocol/ch555/usb_ak820.c:565: void ak820_usb_raw_task(void) {
                                   3984 ;	-----------------------------------------
                                   3985 ;	 function ak820_usb_raw_task
                                   3986 ;	-----------------------------------------
      0064F9                       3987 _ak820_usb_raw_task:
                                   3988 ;	tmk_core/protocol/ch555/usb_ak820.c:569: uint8_t saved_ea = EA;
      0064F9 A2 AF            [12] 3989 	mov	c,_EA
      0064FB E4               [12] 3990 	clr	a
      0064FC 33               [12] 3991 	rlc	a
      0064FD FF               [12] 3992 	mov	r7,a
                                   3993 ;	tmk_core/protocol/ch555/usb_ak820.c:570: EA = 0;
                                   3994 ;	assignBit
      0064FE C2 AF            [12] 3995 	clr	_EA
                                   3996 ;	tmk_core/protocol/ch555/usb_ak820.c:571: if (!USB_EnumStatus || raw_state != RAW_READY) { EA = saved_ea; return; }
      006500 90 06 8D         [24] 3997 	mov	dptr,#_USB_EnumStatus
      006503 E0               [24] 3998 	movx	a,@dptr
      006504 60 0A            [24] 3999 	jz	00101$
      006506 90 06 94         [24] 4000 	mov	dptr,#_raw_state
      006509 E0               [24] 4001 	movx	a,@dptr
      00650A FE               [12] 4002 	mov	r6,a
      00650B BE 02 02         [24] 4003 	cjne	r6,#0x02,00270$
      00650E 80 06            [24] 4004 	sjmp	00102$
      006510                       4005 00270$:
      006510                       4006 00101$:
                                   4007 ;	assignBit
      006510 EF               [12] 4008 	mov	a,r7
      006511 24 FF            [12] 4009 	add	a,#0xff
      006513 92 AF            [24] 4010 	mov	_EA,c
      006515 22               [24] 4011 	ret
      006516                       4012 00102$:
                                   4013 ;	tmk_core/protocol/ch555/usb_ak820.c:572: raw_state = RAW_WORK;
      006516 90 06 94         [24] 4014 	mov	dptr,#_raw_state
      006519 74 03            [12] 4015 	mov	a,#0x03
      00651B F0               [24] 4016 	movx	@dptr,a
                                   4017 ;	tmk_core/protocol/ch555/usb_ak820.c:573: EA = saved_ea;
                                   4018 ;	assignBit
      00651C EF               [12] 4019 	mov	a,r7
      00651D 24 FF            [12] 4020 	add	a,#0xff
      00651F 92 AF            [24] 4021 	mov	_EA,c
                                   4022 ;	tmk_core/protocol/ch555/usb_ak820.c:574: if (raw_buffer[0] == 0xfd && raw_buffer[1] == 0) {
      006521 90 06 95         [24] 4023 	mov	dptr,#_raw_buffer
      006524 E0               [24] 4024 	movx	a,@dptr
      006525 FF               [12] 4025 	mov	r7,a
      006526 E4               [12] 4026 	clr	a
      006527 BF FD 01         [24] 4027 	cjne	r7,#0xfd,00271$
      00652A 04               [12] 4028 	inc	a
      00652B                       4029 00271$:
      00652B FF               [12] 4030 	mov	r7,a
      00652C 70 03            [24] 4031 	jnz	00273$
      00652E 02 65 E8         [24] 4032 	ljmp	00118$
      006531                       4033 00273$:
      006531 90 06 96         [24] 4034 	mov	dptr,#(_raw_buffer + 0x0001)
      006534 E0               [24] 4035 	movx	a,@dptr
      006535 60 03            [24] 4036 	jz	00274$
      006537 02 65 E8         [24] 4037 	ljmp	00118$
      00653A                       4038 00274$:
                                   4039 ;	tmk_core/protocol/ch555/usb_ak820.c:577: address = ((uint16_t)raw_buffer[2] << 8) | raw_buffer[3];
      00653A 90 06 97         [24] 4040 	mov	dptr,#(_raw_buffer + 0x0002)
      00653D E0               [24] 4041 	movx	a,@dptr
      00653E FD               [12] 4042 	mov	r5,a
      00653F 7E 00            [12] 4043 	mov	r6,#0x00
      006541 90 06 98         [24] 4044 	mov	dptr,#(_raw_buffer + 0x0003)
      006544 E0               [24] 4045 	movx	a,@dptr
      006545 7B 00            [12] 4046 	mov	r3,#0x00
      006547 42 06            [12] 4047 	orl	ar6,a
      006549 EB               [12] 4048 	mov	a,r3
      00654A 42 05            [12] 4049 	orl	ar5,a
                                   4050 ;	tmk_core/protocol/ch555/usb_ak820.c:578: length = raw_buffer[4];
      00654C 90 06 99         [24] 4051 	mov	dptr,#(_raw_buffer + 0x0004)
      00654F E0               [24] 4052 	movx	a,@dptr
      006550 FC               [12] 4053 	mov	r4,a
                                   4054 ;	tmk_core/protocol/ch555/usb_ak820.c:579: for (i = 5; i < RAW_EPSIZE; ++i) raw_buffer[i] = 0;
      006551 7B 05            [12] 4055 	mov	r3,#0x05
      006553                       4056 00128$:
      006553 EB               [12] 4057 	mov	a,r3
      006554 24 95            [12] 4058 	add	a, #_raw_buffer
      006556 F5 82            [12] 4059 	mov	dpl,a
      006558 E4               [12] 4060 	clr	a
      006559 34 06            [12] 4061 	addc	a, #(_raw_buffer >> 8)
      00655B F5 83            [12] 4062 	mov	dph,a
      00655D E4               [12] 4063 	clr	a
      00655E F0               [24] 4064 	movx	@dptr,a
      00655F 0B               [12] 4065 	inc	r3
      006560 BB 20 00         [24] 4066 	cjne	r3,#0x20,00275$
      006563                       4067 00275$:
      006563 40 EE            [24] 4068 	jc	00128$
                                   4069 ;	tmk_core/protocol/ch555/usb_ak820.c:580: if (length > RAW_EPSIZE - 5 || (length && address > 0xffffu - (length - 1))) {
      006565 EC               [12] 4070 	mov	a,r4
      006566 24 E4            [12] 4071 	add	a,#0xff - 0x1b
      006568 40 1C            [24] 4072 	jc	00106$
                                   4073 ;	free result
      00656A EC               [12] 4074 	mov	a,r4
      00656B 60 26            [24] 4075 	jz	00165$
      00656D 8C 03            [24] 4076 	mov	ar3,r4
      00656F 1B               [12] 4077 	dec	r3
      006570 7A 00            [12] 4078 	mov	r2,#0x00
      006572 74 FF            [12] 4079 	mov	a,#0xff
      006574 C3               [12] 4080 	clr	c
      006575 9B               [12] 4081 	subb	a,r3
      006576 FB               [12] 4082 	mov	r3,a
      006577 74 FF            [12] 4083 	mov	a,#0xff
      006579 9A               [12] 4084 	subb	a,r2
      00657A FA               [12] 4085 	mov	r2,a
      00657B 8E 00            [24] 4086 	mov	ar0,r6
      00657D 8D 01            [24] 4087 	mov	ar1,r5
      00657F C3               [12] 4088 	clr	c
      006580 EB               [12] 4089 	mov	a,r3
      006581 98               [12] 4090 	subb	a,r0
      006582 EA               [12] 4091 	mov	a,r2
      006583 99               [12] 4092 	subb	a,r1
      006584 50 0D            [24] 4093 	jnc	00165$
                                   4094 ;	free result
      006586                       4095 00106$:
                                   4096 ;	tmk_core/protocol/ch555/usb_ak820.c:581: raw_buffer[1] = 0xff;
      006586 90 06 96         [24] 4097 	mov	dptr,#(_raw_buffer + 0x0001)
      006589 74 FF            [12] 4098 	mov	a,#0xff
      00658B F0               [24] 4099 	movx	@dptr,a
                                   4100 ;	tmk_core/protocol/ch555/usb_ak820.c:582: raw_buffer[4] = 0;
      00658C 90 06 99         [24] 4101 	mov	dptr,#(_raw_buffer + 0x0004)
      00658F E4               [12] 4102 	clr	a
      006590 F0               [24] 4103 	movx	@dptr,a
                                   4104 ;	tmk_core/protocol/ch555/usb_ak820.c:584: for (i = 0; i < length; ++i) raw_buffer[5 + i] = READ_CODE(address + i);
      006591 80 3C            [24] 4105 	sjmp	00108$
      006593                       4106 00165$:
      006593 7B 00            [12] 4107 	mov	r3,#0x00
      006595                       4108 00131$:
      006595 C3               [12] 4109 	clr	c
      006596 EB               [12] 4110 	mov	a,r3
      006597 9C               [12] 4111 	subb	a,r4
      006598 50 35            [24] 4112 	jnc	00108$
      00659A C0 04            [24] 4113 	push	ar4
      00659C 8B 02            [24] 4114 	mov	ar2,r3
      00659E 74 05            [12] 4115 	mov	a,#0x05
      0065A0 2A               [12] 4116 	add	a, r2
      0065A1 F9               [12] 4117 	mov	r1,a
      0065A2 33               [12] 4118 	rlc	a
      0065A3 95 E0            [12] 4119 	subb	a,acc
      0065A5 FA               [12] 4120 	mov	r2,a
      0065A6 E9               [12] 4121 	mov	a,r1
      0065A7 24 95            [12] 4122 	add	a, #_raw_buffer
      0065A9 F9               [12] 4123 	mov	r1,a
      0065AA EA               [12] 4124 	mov	a,r2
      0065AB 34 06            [12] 4125 	addc	a, #(_raw_buffer >> 8)
      0065AD FA               [12] 4126 	mov	r2,a
      0065AE 8B 2F            [24] 4127 	mov	_ak820_usb_raw_task_sloc0_1_0,r3
      0065B0 75 30 00         [24] 4128 	mov	(_ak820_usb_raw_task_sloc0_1_0 + 1),#0x00
      0065B3 8E 00            [24] 4129 	mov	ar0,r6
      0065B5 8D 04            [24] 4130 	mov	ar4,r5
      0065B7 E5 2F            [12] 4131 	mov	a,_ak820_usb_raw_task_sloc0_1_0
      0065B9 28               [12] 4132 	add	a, r0
      0065BA F8               [12] 4133 	mov	r0,a
      0065BB E5 30            [12] 4134 	mov	a,(_ak820_usb_raw_task_sloc0_1_0 + 1)
      0065BD 3C               [12] 4135 	addc	a, r4
      0065BE FC               [12] 4136 	mov	r4,a
      0065BF 88 82            [24] 4137 	mov	dpl,r0
      0065C1 8C 83            [24] 4138 	mov	dph,r4
      0065C3 E4               [12] 4139 	clr	a
      0065C4 93               [24] 4140 	movc	a,@a+dptr
      0065C5 89 82            [24] 4141 	mov	dpl,r1
      0065C7 8A 83            [24] 4142 	mov	dph,r2
      0065C9 F0               [24] 4143 	movx	@dptr,a
      0065CA 0B               [12] 4144 	inc	r3
      0065CB D0 04            [24] 4145 	pop	ar4
      0065CD 80 C6            [24] 4146 	sjmp	00131$
      0065CF                       4147 00108$:
                                   4148 ;	tmk_core/protocol/ch555/usb_ak820.c:588: ak820_usb_send(RAW_IN_EPNUM, raw_buffer, RAW_EPSIZE);
      0065CF 90 06 F2         [24] 4149 	mov	dptr,#_ak820_usb_send_PARM_2
      0065D2 74 95            [12] 4150 	mov	a,#_raw_buffer
      0065D4 F0               [24] 4151 	movx	@dptr,a
      0065D5 74 06            [12] 4152 	mov	a,#(_raw_buffer >> 8)
      0065D7 A3               [24] 4153 	inc	dptr
      0065D8 F0               [24] 4154 	movx	@dptr,a
      0065D9 90 06 F4         [24] 4155 	mov	dptr,#_ak820_usb_send_PARM_3
      0065DC 74 20            [12] 4156 	mov	a,#0x20
      0065DE F0               [24] 4157 	movx	@dptr,a
      0065DF 75 82 03         [24] 4158 	mov	dpl, #0x03
      0065E2 12 61 AA         [24] 4159 	lcall	_ak820_usb_send
      0065E5 02 66 A8         [24] 4160 	ljmp	00119$
      0065E8                       4161 00118$:
                                   4162 ;	tmk_core/protocol/ch555/usb_ak820.c:589: } else if (raw_buffer[0] == 0xfd && raw_buffer[1] == 1) {
      0065E8 EF               [12] 4163 	mov	a,r7
      0065E9 70 03            [24] 4164 	jnz	00281$
      0065EB 02 66 85         [24] 4165 	ljmp	00114$
      0065EE                       4166 00281$:
      0065EE 90 06 96         [24] 4167 	mov	dptr,#(_raw_buffer + 0x0001)
      0065F1 E0               [24] 4168 	movx	a,@dptr
      0065F2 FF               [12] 4169 	mov	r7,a
      0065F3 BF 01 02         [24] 4170 	cjne	r7,#0x01,00282$
      0065F6 80 03            [24] 4171 	sjmp	00283$
      0065F8                       4172 00282$:
      0065F8 02 66 85         [24] 4173 	ljmp	00114$
      0065FB                       4174 00283$:
                                   4175 ;	tmk_core/protocol/ch555/usb_ak820.c:592: for (i = 2; i < RAW_EPSIZE; ++i) raw_buffer[i] = 0;
      0065FB 7F 02            [12] 4176 	mov	r7,#0x02
      0065FD                       4177 00133$:
      0065FD EF               [12] 4178 	mov	a,r7
      0065FE 24 95            [12] 4179 	add	a, #_raw_buffer
      006600 F5 82            [12] 4180 	mov	dpl,a
      006602 E4               [12] 4181 	clr	a
      006603 34 06            [12] 4182 	addc	a, #(_raw_buffer >> 8)
      006605 F5 83            [12] 4183 	mov	dph,a
      006607 E4               [12] 4184 	clr	a
      006608 F0               [24] 4185 	movx	@dptr,a
      006609 0F               [12] 4186 	inc	r7
      00660A BF 20 00         [24] 4187 	cjne	r7,#0x20,00284$
      00660D                       4188 00284$:
      00660D 40 EE            [24] 4189 	jc	00133$
                                   4190 ;	tmk_core/protocol/ch555/usb_ak820.c:593: raw_buffer[2] = 1;
      00660F 90 06 97         [24] 4191 	mov	dptr,#(_raw_buffer + 0x0002)
      006612 74 01            [12] 4192 	mov	a,#0x01
      006614 F0               [24] 4193 	movx	@dptr,a
                                   4194 ;	tmk_core/protocol/ch555/usb_ak820.c:594: raw_buffer[3] = 0xa8;
      006615 90 06 98         [24] 4195 	mov	dptr,#(_raw_buffer + 0x0003)
      006618 74 A8            [12] 4196 	mov	a,#0xa8
      00661A F0               [24] 4197 	movx	@dptr,a
                                   4198 ;	tmk_core/protocol/ch555/usb_ak820.c:595: ak820_nvm_diagnostic(&raw_buffer[4]);
      00661B 90 06 99         [24] 4199 	mov	dptr,#(_raw_buffer + 0x0004)
      00661E 12 37 C1         [24] 4200 	lcall	_ak820_nvm_diagnostic
                                   4201 ;	tmk_core/protocol/ch555/usb_ak820.c:596: for (i = 0; i < 6; ++i) raw_buffer[11 + i] = ak820_flash_diagnostic[i];
      006621 7F 00            [12] 4202 	mov	r7,#0x00
      006623                       4203 00135$:
      006623 8F 06            [24] 4204 	mov	ar6,r7
      006625 74 0B            [12] 4205 	mov	a,#0x0b
      006627 2E               [12] 4206 	add	a, r6
      006628 24 95            [12] 4207 	add	a,#_raw_buffer
      00662A FE               [12] 4208 	mov	r6,a
      00662B E4               [12] 4209 	clr	a
      00662C 34 06            [12] 4210 	addc	a, #(_raw_buffer >> 8)
      00662E FD               [12] 4211 	mov	r5,a
      00662F EF               [12] 4212 	mov	a,r7
      006630 24 1B            [12] 4213 	add	a, #_ak820_flash_diagnostic
      006632 F5 82            [12] 4214 	mov	dpl,a
      006634 E4               [12] 4215 	clr	a
      006635 34 04            [12] 4216 	addc	a, #(_ak820_flash_diagnostic >> 8)
      006637 F5 83            [12] 4217 	mov	dph,a
      006639 E0               [24] 4218 	movx	a,@dptr
      00663A 8E 82            [24] 4219 	mov	dpl,r6
      00663C 8D 83            [24] 4220 	mov	dph,r5
      00663E F0               [24] 4221 	movx	@dptr,a
      00663F 0F               [12] 4222 	inc	r7
      006640 BF 06 00         [24] 4223 	cjne	r7,#0x06,00286$
      006643                       4224 00286$:
      006643 40 DE            [24] 4225 	jc	00135$
                                   4226 ;	tmk_core/protocol/ch555/usb_ak820.c:597: raw_buffer[17] = vial_unlocked;
      006645 90 0C 08         [24] 4227 	mov	dptr,#_vial_unlocked
      006648 E0               [24] 4228 	movx	a,@dptr
      006649 90 06 A6         [24] 4229 	mov	dptr,#(_raw_buffer + 0x0011)
      00664C F0               [24] 4230 	movx	@dptr,a
                                   4231 ;	tmk_core/protocol/ch555/usb_ak820.c:598: raw_buffer[18] = vial_unlock_in_progress;
      00664D 90 0C 09         [24] 4232 	mov	dptr,#_vial_unlock_in_progress
      006650 E0               [24] 4233 	movx	a,@dptr
      006651 90 06 A7         [24] 4234 	mov	dptr,#(_raw_buffer + 0x0012)
      006654 F0               [24] 4235 	movx	@dptr,a
                                   4236 ;	tmk_core/protocol/ch555/usb_ak820.c:599: raw_buffer[19] = USB_EnumStatus;
      006655 90 06 8D         [24] 4237 	mov	dptr,#_USB_EnumStatus
      006658 E0               [24] 4238 	movx	a,@dptr
      006659 90 06 A8         [24] 4239 	mov	dptr,#(_raw_buffer + 0x0013)
      00665C F0               [24] 4240 	movx	@dptr,a
                                   4241 ;	tmk_core/protocol/ch555/usb_ak820.c:600: raw_buffer[20] = USB_SleepStatus;
      00665D 90 06 8E         [24] 4242 	mov	dptr,#_USB_SleepStatus
      006660 E0               [24] 4243 	movx	a,@dptr
      006661 90 06 A9         [24] 4244 	mov	dptr,#(_raw_buffer + 0x0014)
      006664 F0               [24] 4245 	movx	@dptr,a
                                   4246 ;	tmk_core/protocol/ch555/usb_ak820.c:601: raw_buffer[21] = raw_state;
      006665 90 06 94         [24] 4247 	mov	dptr,#_raw_state
      006668 E0               [24] 4248 	movx	a,@dptr
      006669 90 06 AA         [24] 4249 	mov	dptr,#(_raw_buffer + 0x0015)
      00666C F0               [24] 4250 	movx	@dptr,a
                                   4251 ;	tmk_core/protocol/ch555/usb_ak820.c:602: ak820_usb_send(RAW_IN_EPNUM, raw_buffer, RAW_EPSIZE);
      00666D 90 06 F2         [24] 4252 	mov	dptr,#_ak820_usb_send_PARM_2
      006670 74 95            [12] 4253 	mov	a,#_raw_buffer
      006672 F0               [24] 4254 	movx	@dptr,a
      006673 74 06            [12] 4255 	mov	a,#(_raw_buffer >> 8)
      006675 A3               [24] 4256 	inc	dptr
      006676 F0               [24] 4257 	movx	@dptr,a
      006677 90 06 F4         [24] 4258 	mov	dptr,#_ak820_usb_send_PARM_3
      00667A 74 20            [12] 4259 	mov	a,#0x20
      00667C F0               [24] 4260 	movx	@dptr,a
      00667D 75 82 03         [24] 4261 	mov	dpl, #0x03
      006680 12 61 AA         [24] 4262 	lcall	_ak820_usb_send
      006683 80 23            [24] 4263 	sjmp	00119$
      006685                       4264 00114$:
                                   4265 ;	tmk_core/protocol/ch555/usb_ak820.c:604: raw_reply_without_nvm = raw_request_is_nonpersistent();
      006685 12 63 D0         [24] 4266 	lcall	_raw_request_is_nonpersistent
      006688 E5 82            [12] 4267 	mov	a, dpl
      00668A 90 06 B5         [24] 4268 	mov	dptr,#_raw_reply_without_nvm
      00668D F0               [24] 4269 	movx	@dptr,a
                                   4270 ;	tmk_core/protocol/ch555/usb_ak820.c:605: ak820_nvm_begin();
      00668E 12 3C 83         [24] 4271 	lcall	_ak820_nvm_begin
                                   4272 ;	tmk_core/protocol/ch555/usb_ak820.c:606: raw_hid_receive(raw_buffer, RAW_EPSIZE);
      006691 90 0A 54         [24] 4273 	mov	dptr,#_raw_hid_receive_PARM_2
      006694 74 20            [12] 4274 	mov	a,#0x20
      006696 F0               [24] 4275 	movx	@dptr,a
      006697 90 06 95         [24] 4276 	mov	dptr,#_raw_buffer
      00669A 75 F0 00         [24] 4277 	mov	b, #0x00
      00669D 12 A1 9C         [24] 4278 	lcall	_raw_hid_receive
                                   4279 ;	tmk_core/protocol/ch555/usb_ak820.c:607: ak820_nvm_end();
      0066A0 12 3C 98         [24] 4280 	lcall	_ak820_nvm_end
                                   4281 ;	tmk_core/protocol/ch555/usb_ak820.c:608: raw_reply_without_nvm = false;
      0066A3 90 06 B5         [24] 4282 	mov	dptr,#_raw_reply_without_nvm
      0066A6 E4               [12] 4283 	clr	a
      0066A7 F0               [24] 4284 	movx	@dptr,a
      0066A8                       4285 00119$:
                                   4286 ;	tmk_core/protocol/ch555/usb_ak820.c:610: saved_ea = EA;
                                   4287 ;	assignBit
      0066A8 A2 AF            [12] 4288 	mov	c,_EA
      0066AA 92 0C            [24] 4289 	mov	_ak820_usb_raw_task_sloc1_1_0,c
                                   4290 ;	tmk_core/protocol/ch555/usb_ak820.c:611: EA = 0;
                                   4291 ;	assignBit
      0066AC C2 AF            [12] 4292 	clr	_EA
                                   4293 ;	tmk_core/protocol/ch555/usb_ak820.c:613: if (raw_state == RAW_TX_ACTIVE) raw_state = RAW_TX_WAIT;
      0066AE 90 06 94         [24] 4294 	mov	dptr,#_raw_state
      0066B1 E0               [24] 4295 	movx	a,@dptr
      0066B2 FF               [12] 4296 	mov	r7,a
      0066B3 BF 04 08         [24] 4297 	cjne	r7,#0x04,00126$
      0066B6 90 06 94         [24] 4298 	mov	dptr,#_raw_state
      0066B9 74 05            [12] 4299 	mov	a,#0x05
      0066BB F0               [24] 4300 	movx	@dptr,a
      0066BC 80 21            [24] 4301 	sjmp	00127$
      0066BE                       4302 00126$:
                                   4303 ;	tmk_core/protocol/ch555/usb_ak820.c:614: else if (raw_state == RAW_WORK || raw_state == RAW_DRAINED || raw_state == RAW_CANCELLED) raw_state = RAW_IDLE;
      0066BE 90 06 94         [24] 4304 	mov	dptr,#_raw_state
      0066C1 E0               [24] 4305 	movx	a,@dptr
      0066C2 FF               [12] 4306 	mov	r7,a
      0066C3 BF 03 02         [24] 4307 	cjne	r7,#0x03,00290$
      0066C6 80 12            [24] 4308 	sjmp	00121$
      0066C8                       4309 00290$:
      0066C8 90 06 94         [24] 4310 	mov	dptr,#_raw_state
      0066CB E0               [24] 4311 	movx	a,@dptr
      0066CC FF               [12] 4312 	mov	r7,a
      0066CD BF 06 02         [24] 4313 	cjne	r7,#0x06,00291$
      0066D0 80 08            [24] 4314 	sjmp	00121$
      0066D2                       4315 00291$:
      0066D2 90 06 94         [24] 4316 	mov	dptr,#_raw_state
      0066D5 E0               [24] 4317 	movx	a,@dptr
      0066D6 FF               [12] 4318 	mov	r7,a
      0066D7 BF 07 05         [24] 4319 	cjne	r7,#0x07,00127$
      0066DA                       4320 00121$:
      0066DA 90 06 94         [24] 4321 	mov	dptr,#_raw_state
      0066DD E4               [12] 4322 	clr	a
      0066DE F0               [24] 4323 	movx	@dptr,a
      0066DF                       4324 00127$:
                                   4325 ;	tmk_core/protocol/ch555/usb_ak820.c:615: EA = saved_ea;
                                   4326 ;	assignBit
      0066DF A2 0C            [12] 4327 	mov	c,_ak820_usb_raw_task_sloc1_1_0
      0066E1 92 AF            [24] 4328 	mov	_EA,c
                                   4329 ;	tmk_core/protocol/ch555/usb_ak820.c:616: }
      0066E3 22               [24] 4330 	ret
                                   4331 ;------------------------------------------------------------
                                   4332 ;Allocation info for local variables in function 'ak820_usb_take_keyboard_reset'
                                   4333 ;------------------------------------------------------------
                                   4334 ;result        Allocated with name '_ak820_usb_take_keyboard_reset_result_10000_472'
                                   4335 ;saved_ea      Allocated with name '_ak820_usb_take_keyboard_reset_saved_ea_10000_472'
                                   4336 ;------------------------------------------------------------
                                   4337 ;	tmk_core/protocol/ch555/usb_ak820.c:618: bool ak820_usb_take_keyboard_reset(void) {
                                   4338 ;	-----------------------------------------
                                   4339 ;	 function ak820_usb_take_keyboard_reset
                                   4340 ;	-----------------------------------------
      0066E4                       4341 _ak820_usb_take_keyboard_reset:
                                   4342 ;	tmk_core/protocol/ch555/usb_ak820.c:620: uint8_t saved_ea = EA;
                                   4343 ;	assignBit
      0066E4 A2 AF            [12] 4344 	mov	c,_EA
      0066E6 92 0D            [24] 4345 	mov	_ak820_usb_take_keyboard_reset_sloc0_1_0,c
                                   4346 ;	tmk_core/protocol/ch555/usb_ak820.c:621: EA = 0;
                                   4347 ;	assignBit
      0066E8 C2 AF            [12] 4348 	clr	_EA
                                   4349 ;	tmk_core/protocol/ch555/usb_ak820.c:622: result = keyboard_reset;
      0066EA 90 06 B6         [24] 4350 	mov	dptr,#_keyboard_reset
      0066ED E0               [24] 4351 	movx	a,@dptr
      0066EE FF               [12] 4352 	mov	r7,a
                                   4353 ;	tmk_core/protocol/ch555/usb_ak820.c:623: keyboard_reset = 0;
      0066EF E4               [12] 4354 	clr	a
      0066F0 F0               [24] 4355 	movx	@dptr,a
                                   4356 ;	tmk_core/protocol/ch555/usb_ak820.c:624: EA = saved_ea;
                                   4357 ;	assignBit
      0066F1 A2 0D            [12] 4358 	mov	c,_ak820_usb_take_keyboard_reset_sloc0_1_0
      0066F3 92 AF            [24] 4359 	mov	_EA,c
                                   4360 ;	tmk_core/protocol/ch555/usb_ak820.c:625: return result != 0;
      0066F5 EF               [12] 4361 	mov	a,r7
      0066F6 B4 01 00         [24] 4362 	cjne	a,#0x01,00103$
      0066F9                       4363 00103$:
      0066F9 B3               [12] 4364 	cpl	c
      0066FA 92 0D            [24] 4365 	mov	_ak820_usb_take_keyboard_reset_sloc0_1_0,c
      0066FC E4               [12] 4366 	clr	a
      0066FD 33               [12] 4367 	rlc	a
      0066FE F5 82            [12] 4368 	mov	dpl, a
                                   4369 ;	tmk_core/protocol/ch555/usb_ak820.c:626: }
      006700 22               [24] 4370 	ret
                                   4371 	.area CSEG    (CODE)
                                   4372 	.area CONST   (CODE)
                                   4373 	.area CONST   (CODE)
      00B634                       4374 _shared_offsets:
      00B634 00                    4375 	.db #0x00	; 0
      00B635 00                    4376 	.db #0x00	; 0
      00B636 28                    4377 	.db #0x28	; 40
      00B637 28                    4378 	.db #0x28	; 40
      00B638 2B                    4379 	.db #0x2b	; 43
      00B639 00                    4380 	.db #0x00	; 0
      00B63A 08                    4381 	.db #0x08	; 8
                                   4382 	.area CSEG    (CODE)
                                   4383 	.area CONST   (CODE)
      00B63B                       4384 _shared_lengths:
      00B63B 00                    4385 	.db #0x00	; 0
      00B63C 00                    4386 	.db #0x00	; 0
      00B63D 00                    4387 	.db #0x00	; 0
      00B63E 03                    4388 	.db #0x03	; 3
      00B63F 03                    4389 	.db #0x03	; 3
      00B640 00                    4390 	.db #0x00	; 0
      00B641 20                    4391 	.db #0x20	; 32
                                   4392 	.area CSEG    (CODE)
                                   4393 	.area XINIT   (CODE)
                                   4394 	.area CABS    (ABS,CODE)
